"""Async table-change subscriptions on the API's authenticated WebSocket protocol.

Each subscription owns a socket. Use an async context manager and iterate events;
connection loss is surfaced to the caller, who may open a new subscription.
"""

from __future__ import annotations

import asyncio
import json
from contextlib import suppress
from typing import TYPE_CHECKING, Any, NoReturn, Optional
from urllib.parse import urlsplit, urlunsplit

from websockets.asyncio.client import ClientConnection
from websockets.asyncio.client import connect as WebSocketConnect
from websockets.exceptions import ConnectionClosed, InvalidStatus, WebSocketException

from vaifstudio._http import LOOPBACK_HOSTS
from vaifstudio.database import _identifier
from vaifstudio.exceptions import VaifAuthError, VaifError, VaifNetworkError, VaifTimeoutError

if TYPE_CHECKING:
    from vaifstudio.client import VaifClient


class _DirectConnect(WebSocketConnect):
    def process_redirect(self, exc: Exception) -> Exception:
        # A redirected handshake must never forward the first auth frame elsewhere.
        return exc


connect = _DirectConnect


def realtime_url(base_url: str) -> str:
    """The WebSocket URL for the API at ``base_url``.

    An ``https`` base URL, in any letter case, becomes ``wss``. An ``http``
    base URL becomes ``ws`` only for ``localhost``, ``127.0.0.1`` and ``::1``.
    Any other scheme or host, or a URL with user information, raises
    ``VaifError`` with code ``INVALID_REALTIME_URL``.
    """
    refused = VaifError(
        "Realtime needs an https base URL (http only for localhost, 127.0.0.1 or ::1)",
        code="INVALID_REALTIME_URL",
    )
    try:
        parts = urlsplit(base_url.strip())
        hostname = parts.hostname
        has_user_info = parts.username is not None or parts.password is not None
    except ValueError:
        raise refused from None
    if not hostname or has_user_info:
        raise refused
    scheme = parts.scheme.lower()
    if scheme == "https":
        ws_scheme = "wss"
    elif scheme == "http" and hostname in LOOPBACK_HOSTS:
        ws_scheme = "ws"
    else:
        raise refused
    return urlunsplit((ws_scheme, parts.netloc, parts.path.rstrip("/") + "/realtime/ws", "", ""))


class RealtimeClient:
    def __init__(self, client: VaifClient) -> None:
        self._client = client
        self._subscriptions: set[RealtimeSubscription] = set()

    def subscribe(
        self,
        table: str,
        *,
        event: str = "*",
        timeout: float = 15.0,
    ) -> RealtimeSubscription:
        """Subscribe to INSERT, UPDATE, DELETE, or all (*) changes for a table.

        Enter the returned context before writing rows: entry waits for the
        server's subscription acknowledgment. No automatic reconnect or replay.
        """
        if not self._client.project_id:
            raise ValueError("project_id is required for realtime")
        _identifier(table, "table")
        if event not in {"*", "INSERT", "UPDATE", "DELETE"}:
            raise ValueError("event must be *, INSERT, UPDATE, or DELETE")
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        return RealtimeSubscription(self, table, event, timeout)

    async def close(self) -> None:
        for subscription in list(self._subscriptions):
            await subscription.close()


class RealtimeSubscription:
    def __init__(self, owner: RealtimeClient, table: str, event: str, timeout: float) -> None:
        self._owner = owner
        self._table = table
        self._event = event
        self._timeout = timeout
        self._channel = "table:" + table
        self._socket: Optional[ClientConnection] = None
        self._heartbeat: Optional[asyncio.Task[None]] = None
        self._token: Optional[str] = None
        # The auth generation the subscription opened under: the socket
        # belongs to that session and is never authenticated as another one.
        self._generation = 0
        self._failure: Optional[Exception] = None

    async def __aenter__(self) -> RealtimeSubscription:
        if self._socket is not None:
            raise RuntimeError("Subscription is already open")
        client = self._owner._client
        # Refused before the session is read, so an unsafe URL never causes a
        # token refresh either.
        url = realtime_url(client.base_url)
        try:
            self._generation = client.auth._generation
            self._token = await client.auth._bearer()
            # Send credentials in the first frame, never in URLs or proxy headers.
            self._socket = await connect(url, open_timeout=self._timeout, proxy=None)
            self._owner._subscriptions.add(self)
            # The connection took time: no credentials for a session that is
            # no longer the current one.
            self._require_same_session()
            frame: dict[str, Any] = {"type": "auth", "apiKey": client._transport._api_key}
            if self._token:
                frame["accessToken"] = self._token
            await self._send(frame)
            welcome = await asyncio.wait_for(self._until("welcome"), self._timeout)
            interval = welcome.get("heartbeatIntervalMs", 30000)
            interval = (
                float(interval) / 1000
                if isinstance(interval, (int, float)) and interval > 0
                else 30.0
            )
            self._heartbeat = asyncio.create_task(self._keep_alive(interval))
            await self._send({"type": "subscribe", "channel": self._channel})
            await asyncio.wait_for(self._until("subscribed"), self._timeout)
            return self
        except BaseException as exc:
            await self.close()
            error = self._open_error(exc) if isinstance(exc, Exception) else None
            if error is not None:
                raise error from exc
            raise

    def _open_error(self, exc: Exception) -> Optional[VaifError]:
        """The ``VaifError`` for a subscription that did not open, or ``None`` to re-raise."""
        if isinstance(exc, VaifError):
            return None
        # asyncio.TimeoutError is a separate class before Python 3.11.
        if isinstance(exc, (TimeoutError, asyncio.TimeoutError)):
            return VaifTimeoutError(
                f"Timed out opening the realtime subscription (timeout: {self._timeout} seconds)",
                code="REALTIME_CLOSED",
            )
        if isinstance(exc, InvalidStatus):
            status = exc.response.status_code
            return VaifNetworkError(
                f"The realtime handshake was refused with HTTP {status}",
                status=status,
                code="REALTIME_CLOSED",
            )
        if isinstance(exc, (OSError, WebSocketException)):
            return VaifNetworkError(
                f"Could not open the realtime connection: {type(exc).__name__}",
                code="REALTIME_CLOSED",
            )
        return None

    async def _send(self, frame: dict[str, Any]) -> None:
        if self._socket is not None:
            try:
                await self._socket.send(json.dumps(frame))
            except (OSError, WebSocketException) as exc:
                self._raise_socket_failure(exc)

    async def _read(self) -> dict[str, Any]:
        if self._socket is None:
            raise StopAsyncIteration
        while True:
            try:
                raw = await self._socket.recv()
            except (OSError, WebSocketException) as exc:
                self._raise_socket_failure(exc)
            try:
                frame = json.loads(raw)
            except (ValueError, TypeError):
                continue
            if not isinstance(frame, dict):
                continue
            if frame.get("type") == "error":
                code = frame.get("code") or frame.get("error")
                raise VaifError(
                    str(frame.get("message", "Realtime request refused")),
                    code=code if isinstance(code, str) else None,
                    body=frame,
                )
            return frame

    def _raise_socket_failure(self, exc: Exception) -> NoReturn:
        """Raise the ``VaifError`` for a failed socket read or write."""
        # A heartbeat that failed (session cleared) closed the socket itself:
        # its error is the cause, not the close it produced.
        if self._failure is not None:
            raise self._failure
        if isinstance(exc, ConnectionClosed):
            raise self._closed_error(exc) from exc
        raise VaifNetworkError(
            f"Realtime connection failed: {type(exc).__name__}", code="REALTIME_CLOSED"
        ) from exc

    def _closed_error(self, closed: ConnectionClosed) -> VaifError:
        received = closed.rcvd
        code = received.code if received is not None else None
        reason = received.reason if received is not None else ""
        # The API refuses with a 4xxx close whose reason is its error code
        # (UNAUTHORIZED, TOKEN_EXPIRED, FORBIDDEN, ...).
        if code is not None and 4000 <= code < 5000 and reason:
            error_type = VaifAuthError if code in (4001, 4002, 4003) else VaifError
            return error_type("Realtime connection refused: " + reason, status=code, code=reason)
        return VaifNetworkError(
            "Realtime connection closed" + (": " + reason if reason else ""),
            status=code,
            code="REALTIME_CLOSED",
        )

    async def _until(self, kind: str) -> dict[str, Any]:
        while True:
            frame = await self._read()
            if frame.get("type") == kind and (
                kind != "subscribed" or frame.get("channel") == self._channel
            ):
                return frame

    def _require_same_session(self) -> None:
        """Raise ``NOT_SIGNED_IN`` unless the session the socket opened with is still current.

        A token that only rotated is the same session. A sign-out, or any other
        session installed since the subscription opened, ends it: the next
        subscription starts from the session then current.
        """
        auth = self._owner._client.auth
        if auth._generation != self._generation:
            raise VaifAuthError(
                "Session cleared; open a new subscription"
                if auth.session is None
                else "The signed-in session changed; open a new subscription",
                code="NOT_SIGNED_IN",
            )

    async def _keep_alive(self, interval: float) -> None:
        try:
            while True:
                await asyncio.sleep(interval)
                # Before the read, so another user's session is not refreshed
                # on this subscription's behalf; after it, in case the session
                # changed while the token was being refreshed.
                self._require_same_session()
                token = await self._owner._client.auth._bearer()
                self._require_same_session()
                if token != self._token:
                    await self._send({"type": "auth", "accessToken": token})
                    self._token = token
                await self._send({"type": "ping"})
        except asyncio.CancelledError:
            raise
        except Exception as failure:
            # Record the failure BEFORE closing: the close wakes the reader,
            # which must raise this error rather than the close it caused.
            if isinstance(failure, VaifError):
                self._failure = failure
            else:
                self._failure = VaifNetworkError(
                    f"Realtime heartbeat failed: {type(failure).__name__}",
                    code="REALTIME_CLOSED",
                )
                self._failure.__cause__ = failure
            if self._socket is not None:
                await self._socket.close()
            raise

    def __aiter__(self) -> RealtimeSubscription:
        return self

    async def __anext__(self) -> dict[str, Any]:
        while True:
            if self._failure is not None:
                raise self._failure
            frame = await self._read()
            if (
                frame.get("type") == "db_change"
                and frame.get("table") == self._table
                and (self._event == "*" or frame.get("op") == self._event)
                and (not frame.get("channels") or self._channel in frame["channels"])
            ):
                return frame

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    async def close(self) -> None:
        heartbeat, self._heartbeat = self._heartbeat, None
        if heartbeat is not None:
            heartbeat.cancel()
            with suppress(asyncio.CancelledError, Exception):
                await heartbeat
        socket, self._socket = self._socket, None
        self._owner._subscriptions.discard(self)
        if socket is not None:
            try:
                with suppress(Exception):
                    await socket.send(json.dumps({"type": "unsubscribe", "channel": self._channel}))
            finally:
                await socket.close()
