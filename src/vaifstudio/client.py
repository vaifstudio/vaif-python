"""The VAIF client: one object per project, shared by every module."""

from __future__ import annotations

from typing import Any, Mapping, Optional, cast

import httpx

from vaifstudio._generated import Operations
from vaifstudio._http import RUN_ID_HEADER, HttpTransport
from vaifstudio.auth import AuthClient
from vaifstudio.copilot import CopilotClient
from vaifstudio.database import QueryBuilder
from vaifstudio.exceptions import VaifAuthError
from vaifstudio.functions import FunctionsClient
from vaifstudio.realtime import RealtimeClient
from vaifstudio.retry import RetryPolicy
from vaifstudio.storage import StorageClient
from vaifstudio.types import Session

DEFAULT_BASE_URL = "https://api.vaif.studio"
DEFAULT_TIMEOUT = 30.0


class VaifClient:
    """Async client for a VAIF Studio project.

    Args:
        project_id: The project's id.
        api_key: A project API key (``vk_pub_...`` for apps, ``vk_srv_...``
            for trusted servers only). Sent as ``x-vaif-key``.
        base_url: API origin. Must use https; http is accepted only for
            localhost, 127.0.0.1 and ::1.
        timeout: Per-request timeout in seconds.
        retry: Retry policy for transient failures.
        headers: Extra headers sent with every request.
        http_client: Bring your own ``httpx.AsyncClient`` (you close it).
        session: Restore a previously persisted end-user session.

    Use it as an async context manager, or call :meth:`close` when done.
    """

    def __init__(
        self,
        project_id: Optional[str],
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        retry: Optional[RetryPolicy] = None,
        headers: Optional[Mapping[str, str]] = None,
        http_client: Optional[httpx.AsyncClient] = None,
        session: Optional[Session] = None,
    ) -> None:
        if project_id == "":
            raise ValueError("project_id must not be empty")
        self.project_id = project_id or ""
        self._transport = HttpTransport(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout,
            retry=retry or RetryPolicy(),
            headers=headers,
            http_client=http_client,
        )
        self.auth = AuthClient(self, session)
        self.storage = StorageClient(self)
        self.functions = FunctionsClient(self)
        self.realtime = RealtimeClient(self)
        # The complete operation surface generated from the API's OpenAPI
        # description: one coroutine per route, sent through ``_send`` so it
        # carries the same key, session and retries as the modules above.
        # A binary read that the API redirects to a signed link is read like
        # ``storage.download()`` reads one: without the key or the session.
        # ``await client.operations.get_projects_by_project_id(path={...})``.
        self.operations = Operations(self._send, self._transport.get_signed)

    @property
    def base_url(self) -> str:
        return self._transport.base_url

    def copilot(self, account_token: str) -> CopilotClient:
        """VAIF Verament calls for a VAIF account: plan, then confirm the plan card.

        Verament acts for your VAIF account, not a project end user, so it
        takes the account's access token. See :mod:`vaifstudio.copilot`.
        """
        return CopilotClient(self, account_token)

    def from_(self, table: str) -> QueryBuilder:
        """Start a query against ``table`` (``from`` is a Python keyword)."""
        if not self.project_id:
            raise ValueError("project_id is required for table queries")
        return QueryBuilder(self, table)

    table = from_

    async def close(self) -> None:
        """Release the HTTP connection pool."""
        await self.realtime.close()
        await self._transport.aclose()

    async def __aenter__(self) -> VaifClient:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    async def _send(
        self,
        method: str,
        path: str,
        *,
        require_session: bool = False,
        **kwargs: Any,
    ) -> httpx.Response:
        """Send a request as the signed-in user (if any).

        A session token that is about to expire is refreshed first. If the user
        signs out, or another session is installed, while that refresh runs,
        nothing is sent and ``VaifAuthError`` with code ``NOT_SIGNED_IN`` is
        raised (see ``AuthClient._bearer``).

        A 401 on a request that carried a session token triggers one refresh
        and one resend: the API refuses an invalid or expired token before the
        route's handler runs, so the resend cannot repeat work. The request is
        sent again only while the user who sent it is still signed in, and
        only with that user's refreshed token (see ``AuthClient._retry_token``).
        A function's own 401, which the invoke route relays after the function
        has run, carries ``X-Vaif-Run-Id`` and is raised as it is. A
        caller-supplied ``Authorization`` header is not a session token: it is
        sent as given and a 401 on it does not refresh the session.
        """
        raw_headers = kwargs.get("headers")
        extra = cast(Mapping[str, str], raw_headers) if isinstance(raw_headers, Mapping) else None
        # Do not read or refresh the session when the caller already named a
        # bearer: _bearer() may rotate the refresh token, and a 401 on their
        # header must not be retried as the end-user session.
        explicit_authorization = self._transport.supplies_authorization(extra)
        generation = self.auth._generation
        bearer = None if explicit_authorization else await self.auth._bearer()
        if require_session and not explicit_authorization and bearer is None:
            raise VaifAuthError("Not signed in", code="NOT_SIGNED_IN")
        try:
            return await self._transport.request(method, path, bearer=bearer, **kwargs)
        except VaifAuthError as exc:
            if (
                explicit_authorization
                or exc.status != 401
                or bearer is None
                or RUN_ID_HEADER in exc.headers
            ):
                raise
            fresh = await self.auth._retry_token(bearer, generation)
            if fresh is None:
                raise
            return await self._transport.request(method, path, bearer=fresh, **kwargs)


def create_client(project_id: Optional[str], api_key: str, **kwargs: Any) -> VaifClient:
    """Create a :class:`VaifClient`. Keyword arguments are passed through."""
    return VaifClient(project_id, api_key, **kwargs)


__all__ = ["VaifClient", "create_client", "DEFAULT_BASE_URL", "DEFAULT_TIMEOUT"]
