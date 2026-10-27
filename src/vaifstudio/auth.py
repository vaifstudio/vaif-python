"""End-user authentication for a VAIF project (``/projects/:projectId/auth``)."""

from __future__ import annotations

import asyncio
import base64
import hashlib
import logging
import re
import secrets
import time
from contextlib import suppress
from typing import TYPE_CHECKING, Any, Callable, Mapping, Optional
from urllib.parse import unquote

import httpx

from vaifstudio._http import REFRESH_COOKIE, path_segment, response_json
from vaifstudio.exceptions import VaifAuthError, VaifConsoleOnlyError, VaifError
from vaifstudio.types import Session, SignInResult, SignUpResult, User

if TYPE_CHECKING:
    from vaifstudio.client import VaifClient

logger = logging.getLogger("vaifstudio")

#: Refresh this many seconds before the access token expires.
REFRESH_LEEWAY_SECONDS = 30.0

SessionListener = Callable[[str, Optional[Session]], Any]


def refresh_token_from(response: httpx.Response) -> Optional[str]:
    """Read the rotating refresh token from the ``Set-Cookie`` header.

    The API delivers it only as an HttpOnly cookie, so a native client reads
    it here and sends it back explicitly on refresh.
    """
    for header in response.headers.get_list("set-cookie"):
        name, sep, rest = header.partition("=")
        if not sep or name.strip() != REFRESH_COOKIE:
            continue
        value = unquote(rest.split(";", 1)[0].strip())
        return value or None
    return None


def _session_from(body: Mapping[str, Any], refresh_token: Optional[str]) -> Session:
    token = body.get("accessToken")
    if not isinstance(token, str) or not token:
        raise VaifError("The API response did not include an access token", body=dict(body))
    expires_in = body.get("expiresIn")
    lifetime = float(expires_in) if isinstance(expires_in, (int, float)) else 900.0
    user = body.get("user")
    return Session(
        access_token=token,
        expires_at=time.time() + lifetime,
        refresh_token=refresh_token,
        user=User.from_api(user) if isinstance(user, Mapping) else None,
    )


def _storage_error() -> VaifError:
    return VaifError(
        "Signed out, but a session listener failed while clearing the saved session, "
        "so it may be restored on the next start",
        code="SESSION_STORAGE_FAILED",
    )


def _save_error() -> VaifError:
    return VaifError(
        "Signed in, but a session listener failed while saving the session, "
        "so the next start may restore an earlier saved session or none",
        code="SESSION_STORAGE_FAILED",
    )


class AuthClient:
    """Sign end users in and out and keep their session fresh.

    Sessions live in memory. Register ``on_session_change`` to persist them
    (for example in the OS keychain) and ``set_session`` to restore one.
    """

    def __init__(self, client: VaifClient, session: Optional[Session] = None) -> None:
        self._client = client
        self._session = session
        self._refresh_task: Optional[asyncio.Future[Session]] = None
        # The session the in-flight refresh started from.
        self._refresh_from: Optional[Session] = None
        # Counts sign-ins and sign-outs, but not token refreshes, so a request
        # can tell whether the user changed while it was in flight.
        self._generation = 0
        self._listeners: list[SessionListener] = []
        self.mfa = MfaClient(self)

    # ---------------------------------------------------------------- state

    @property
    def session(self) -> Optional[Session]:
        """The current session, or ``None`` when signed out."""
        return self._session

    def on_session_change(self, listener: SessionListener) -> Callable[[], None]:
        """Call ``listener(event, session)`` on SIGNED_IN, TOKEN_REFRESHED, SIGNED_OUT.

        A listener that raises is logged and does not stop the change or the
        other listeners. ``sign_out()`` and the calls that sign a user in
        also raise ``VaifError`` with code ``SESSION_STORAGE_FAILED`` after
        the change, so a session that could not be saved or cleared is
        reported. Returns a function that unregisters the listener.
        """
        self._listeners.append(listener)

        def unsubscribe() -> None:
            if listener in self._listeners:
                self._listeners.remove(listener)

        return unsubscribe

    def set_session(
        self,
        access_token: str,
        refresh_token: Optional[str] = None,
        *,
        expires_at: Optional[float] = None,
        user: Optional[User] = None,
    ) -> Session:
        """Restore a previously persisted session.

        A listener that raises is logged; nothing is raised for it.
        """
        if not access_token:
            raise ValueError("access_token must not be empty")
        session = Session(
            access_token=access_token,
            # Unknown expiry: treat as fresh and rely on 401-triggered refresh.
            expires_at=expires_at if expires_at is not None else time.time() + 3600.0,
            refresh_token=refresh_token,
            user=user,
        )
        self._set(session, "SIGNED_IN")
        return session

    def _set(self, session: Optional[Session], event: str) -> Optional[Exception]:
        """Install ``session`` and tell every listener.

        A listener that raises does not stop the change or the other
        listeners. The first exception is logged with the others and
        returned, so ``sign_out()`` can report a saved session it could not
        clear.
        """
        if event != "TOKEN_REFRESHED":
            self._generation += 1
        self._session = session
        first: Optional[Exception] = None
        for listener in list(self._listeners):
            try:
                listener(event, session)
            except Exception as exc:
                logger.exception("vaifstudio: session listener raised")
                first = first or exc
        return first

    def _signed_in(self, session: Session) -> None:
        """Install the session a sign-in returned.

        The session stays installed when a listener raises. The error is
        raised after it, because a store that could neither save the new
        session nor delete an older one leaves the older one restorable, and
        nothing else tells the caller.
        """
        failure = self._set(session, "SIGNED_IN")
        if failure is not None:
            raise _save_error() from failure

    def _path(self, suffix: str) -> str:
        # Auth here is for your app's users. VAIF Studio accounts sign in to the
        # console (a session cookie this client never holds), and their sign-up
        # and reset raise VaifConsoleOnlyError first, so a platform client
        # (project_id None) has no auth route to call.
        self._require_project()
        return f"/projects/{path_segment(self._client.project_id, 'project_id')}/auth/{suffix}"

    # ------------------------------------------------------------ requests

    async def sign_up(
        self,
        email: str,
        password: str,
        *,
        metadata: Optional[Mapping[str, Any]] = None,
        phone: Optional[str] = None,
    ) -> SignUpResult:
        """Create an account with email and password.

        When the API returns a session, the user is signed in; see
        :meth:`sign_in` for a listener that fails to save it.
        """
        if not self._client.project_id:
            raise VaifConsoleOnlyError("auth.sign_up()")
        payload: dict[str, Any] = {"email": email, "password": password}
        if metadata is not None:
            payload["metadata"] = dict(metadata)
        if phone is not None:
            payload["phone"] = phone
        response = await self._client._transport.request("POST", self._path("signup"), json=payload)
        body = response_json(response) or {}
        user_data = body.get("user")
        user = User.from_api(user_data) if isinstance(user_data, Mapping) else None
        if body.get("accessToken"):
            session = _session_from(body, refresh_token_from(response))
            self._signed_in(session)
            return SignUpResult(session=session, user=session.user or user)
        return SignUpResult(
            user=user,
            pending_verification=bool(body.get("pendingVerification", True)),
            message=body.get("message"),
        )

    async def sign_in(self, email: str, password: str) -> SignInResult:
        """Sign in with email and password.

        When the user has MFA enrolled the result carries ``mfa_required`` and a
        ``challenge_token``; finish with :meth:`verify_mfa`.

        The session is installed before the listeners are called. If one
        raises, for example because it could not save the session, the user
        stays signed in and ``VaifError`` with code ``SESSION_STORAGE_FAILED``
        is raised, with the listener's exception as ``__cause__``: a session
        saved earlier could otherwise be restored on the next start without
        any sign of it. :meth:`verify_mfa`, :meth:`handle_oauth_callback` and
        :meth:`sign_up` do the same.
        """
        response = await self._client._transport.request(
            "POST", self._path("login"), json={"email": email, "password": password}
        )
        body = response_json(response) or {}
        if body.get("mfaRequired"):
            return SignInResult(mfa_required=True, challenge_token=body.get("challengeToken"))
        session = _session_from(body, refresh_token_from(response))
        self._signed_in(session)
        return SignInResult(session=session)

    async def verify_mfa(self, challenge_token: str, code: str) -> Session:
        """Complete an MFA sign-in with a TOTP or backup code."""
        response = await self._client._transport.request(
            "POST",
            self._path("mfa/verify"),
            json={"challengeToken": challenge_token, "code": code},
        )
        session = _session_from(response_json(response) or {}, refresh_token_from(response))
        self._signed_in(session)
        return session

    async def refresh_session(self) -> Session:
        """Exchange the refresh token for a new access token.

        Concurrent callers for the same session share a single in-flight
        refresh, so a burst of requests with an expired token triggers exactly
        one network call. A refresh that started from an earlier session is
        not shared.
        """
        current = self._session
        task = self._refresh_task
        if task is None or task.done() or self._refresh_from is not current:
            task = asyncio.ensure_future(self._refresh_once(current))
            # Retrieve the exception even if every awaiter was canceled.
            task.add_done_callback(lambda t: t.cancelled() or t.exception())
            self._refresh_task = task
            self._refresh_from = current
        return await asyncio.shield(task)

    async def _refresh_once(self, current: Optional[Session]) -> Session:
        if current is None or not current.refresh_token:
            raise VaifAuthError(
                "No refresh token available; sign in again", code="NO_REFRESH_TOKEN"
            )
        try:
            response = await self._client._transport.request(
                "POST",
                self._path("refresh"),
                headers={"Cookie": f"{REFRESH_COOKIE}={current.refresh_token}"},
            )
        except VaifAuthError:
            # Revoked or expired refresh token: the session is over.
            if self._session is current:
                self._set(None, "SIGNED_OUT")
            raise
        # The session can change while the request is in flight. A refresh
        # that finishes after sign_out() must not sign the user back in, and
        # one that finishes after set_session() or a sign-in must not replace
        # the newer session.
        if self._session is not current:
            if self._session is None:
                await self._revoke_rotated(response)
                raise VaifAuthError(
                    "Signed out while the session was being refreshed", code="NOT_SIGNED_IN"
                )
            return self._session
        rotated = refresh_token_from(response) or current.refresh_token
        session = _session_from(response_json(response) or {}, rotated)
        if session.user is None and current.user is not None:
            session = Session(
                access_token=session.access_token,
                expires_at=session.expires_at,
                refresh_token=session.refresh_token,
                user=current.user,
            )
        self._set(session, "TOKEN_REFRESHED")
        return session

    async def _revoke_rotated(self, response: httpx.Response) -> None:
        """Revoke the refresh token a refresh issued after ``sign_out()``.

        ``sign_out()`` names the refresh token it knew. If the rotation reached
        the server first, that token no longer identifies a session, and the
        rotated one, which this client discards, would stay valid. Best effort:
        a failure here is not raised.
        """
        rotated = refresh_token_from(response)
        if not rotated:
            return
        with suppress(VaifError):
            await self._client._transport.request(
                "POST", self._path("logout"), json={"refreshToken": rotated}
            )

    async def sign_out(self) -> None:
        """Clear the session locally, then ask the server to revoke it.

        The server revokes every session of the user. The request carries the
        access token and the refresh token, so the server can identify the
        user after the access token has expired. The local session is cleared
        before the request is sent, so it is cleared even if the request
        fails; an HTTP 401 from the server is not raised.

        Listeners receive ``SIGNED_OUT`` before the request. If one raises,
        for example because it could not delete a saved session, ``sign_out()``
        still asks the server to revoke the session and then raises
        ``VaifError`` with code ``SESSION_STORAGE_FAILED`` and the listener's
        exception as ``__cause__``: a saved session left behind could
        otherwise be restored on the next start.
        """
        current = self._session
        if current is None:
            return
        storage_failure = self._set(None, "SIGNED_OUT")
        body = {"refreshToken": current.refresh_token} if current.refresh_token else None
        try:
            await self._client._transport.request(
                "POST", self._path("logout"), bearer=current.access_token, json=body
            )
        except VaifError as exc:
            # Raised inside this handler, the storage error keeps the request's
            # error as __context__.
            if storage_failure is not None:
                raise _storage_error() from storage_failure
            if not (isinstance(exc, VaifAuthError) and exc.status == 401):
                raise
        if storage_failure is not None:
            raise _storage_error() from storage_failure

    async def get_user(self) -> User:
        """Fetch the signed-in user's profile."""
        response = await self._client._send("GET", self._path("me"), require_session=True)
        body = response_json(response) or {}
        user = body.get("user")
        if not isinstance(user, Mapping):
            raise VaifError("The API response did not include a user", body=body)
        return User.from_api(user)

    async def request_password_reset(self, email: str) -> None:
        """Email a password-reset link. Succeeds whether or not the address exists."""
        if not self._client.project_id:
            raise VaifConsoleOnlyError("auth.request_password_reset()", password_reset=True)
        await self._client._transport.request(
            "POST", self._path("forgot-password"), json={"email": email}
        )

    async def reset_password(self, token: str, new_password: str) -> None:
        """Set a new password using the token from the reset email."""
        await self._client._transport.request(
            "POST", self._path("reset-password"), json={"token": token, "password": new_password}
        )

    def _require_project(self) -> None:
        if not self._client.project_id:
            raise VaifError(
                "Auth is for the users of your own app: create the client with your "
                "project_id. VAIF Studio accounts sign in at https://console.vaif.studio.",
                code="PROJECT_ID_REQUIRED",
            )

    @staticmethod
    def _check_verifier(verifier: str) -> str:
        if not re.fullmatch(r"[A-Za-z0-9._~-]{43,128}", verifier):
            raise ValueError("code_verifier must be 43-128 PKCE characters")
        return verifier

    async def get_oauth_sign_in_url(
        self,
        provider: str,
        *,
        redirect_url: str,
        code_verifier: Optional[str] = None,
        state: Optional[str] = None,
    ) -> dict[str, Any]:
        """Get a provider consent URL. Persist the returned state and verifier securely."""
        self._require_project()
        if not provider or not redirect_url:
            raise ValueError("provider and redirect_url are required")
        verifier = self._check_verifier(
            code_verifier if code_verifier is not None else secrets.token_urlsafe(32)
        )
        state = state if state is not None else secrets.token_urlsafe(16)
        if not state or len(state) > 512:
            raise ValueError("state must be non-empty and at most 512 characters")
        challenge = (
            base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest())
            .decode()
            .rstrip("=")
        )
        response = await self._client._transport.request(
            "POST",
            self._path(f"oauth/{path_segment(provider, 'provider')}/start"),
            json={
                "redirectUrl": redirect_url,
                "codeChallenge": challenge,
                "codeChallengeMethod": "S256",
                "state": state,
            },
        )
        body = response_json(response) or {}
        if not isinstance(body.get("url"), str):
            raise VaifError("The API response did not include an OAuth URL", body=body)
        return {
            "url": body["url"],
            "state": state,
            "code_verifier": verifier,
            "expires_in": body.get("expiresIn"),
        }

    async def handle_oauth_callback(
        self,
        code: str,
        *,
        state: str,
        expected_state: str,
        code_verifier: str,
    ) -> SignInResult:
        """Exchange a one-use code after checking state against your saved sign-in state."""
        self._require_project()
        if (
            not state
            or not expected_state
            or not secrets.compare_digest(state.encode(), expected_state.encode())
        ):
            raise VaifError(
                "OAuth state does not match the saved sign-in state", code="OAUTH_STATE_MISMATCH"
            )
        if not code:
            raise VaifError("OAuth code is required", code="OAUTH_MISSING_CODE")
        self._check_verifier(code_verifier)
        response = await self._client._transport.request(
            "POST",
            self._path("oauth/token"),
            json={"code": code, "codeVerifier": code_verifier},
        )
        body = response_json(response) or {}
        if body.get("mfaRequired"):
            return SignInResult(mfa_required=True, challenge_token=body.get("challengeToken"))
        session = _session_from(body, refresh_token_from(response))
        self._signed_in(session)
        return SignInResult(session=session)

    async def list_oauth_providers(self) -> dict[str, Any]:
        """List enabled social sign-in providers for the project."""
        self._require_project()
        response = await self._client._transport.request("GET", self._path("oauth/providers"))
        return dict(response_json(response) or {})

    # ------------------------------------------------------------ internal

    async def _bearer(self) -> Optional[str]:
        """Access token for an outgoing request, refreshed first if about to expire.

        Raises ``VaifAuthError`` with code ``NOT_SIGNED_IN`` when the user
        signs out, or another session is installed, while the token is being
        refreshed: the caller started as one user and must not go on as
        another. A refresh that only rotates the session's own token does not
        count as a change.
        """
        session = self._session
        if session is None:
            return None
        if session.refresh_token and session.is_expired(REFRESH_LEEWAY_SECONDS):
            generation = self._generation
            session = await self.refresh_session()
            if self._generation != generation:
                raise VaifAuthError(
                    "The signed-in session changed while its access token was being refreshed",
                    code="NOT_SIGNED_IN",
                )
        return session.access_token

    async def _retry_token(self, bearer: str, generation: int) -> Optional[str]:
        """The access token to send a request again with after an HTTP 401.

        ``bearer`` is the access token the request carried, and ``generation``
        the value of ``_generation`` when it was sent. Returns ``None`` when
        the request must not be sent again: the session has no refresh token,
        or the user signed out or another session was installed before or
        during the refresh. A request is never sent again with another user's
        access token or without one.
        """
        current = self._session
        if self._generation != generation or current is None or not current.refresh_token:
            return None
        if current.access_token != bearer:
            # Another request already refreshed this session.
            return current.access_token
        refreshed = await self.refresh_session()
        if self._generation != generation:
            return None
        return refreshed.access_token


class MfaClient:
    """Project-user TOTP enrollment and management. Keep secrets and backup codes private."""

    def __init__(self, auth: AuthClient) -> None:
        self._auth = auth

    async def _post(self, suffix: str, body: Optional[dict[str, Any]] = None) -> dict[str, Any]:
        kwargs: dict[str, Any] = {} if body is None else {"json": body}
        response = await self._auth._client._send(
            "POST",
            self._auth._path("mfa/" + suffix),
            require_session=True,
            **kwargs,
        )
        return dict(response_json(response) or {})

    async def enroll_start(self) -> dict[str, Any]:
        return await self._post("enroll-start")

    async def enroll_confirm(self, enroll_token: str, code: str) -> dict[str, Any]:
        return await self._post("enroll-confirm", {"enrollToken": enroll_token, "code": code})

    async def verify(self, challenge_token: str, code: str) -> Session:
        return await self._auth.verify_mfa(challenge_token, code)

    async def disable(self, code: str) -> dict[str, Any]:
        return await self._post("disable", {"code": code})

    async def regenerate_codes(self, code: str) -> dict[str, Any]:
        return await self._post("regenerate-codes", {"code": code})
