"""HTTP transport: headers, timeouts, bounded retries and error mapping."""

from __future__ import annotations

import asyncio
import email.utils
import time
from typing import Any, Mapping, Optional
from urllib.parse import quote, urljoin, urlsplit, urlunsplit

import httpx

from vaifstudio._version import __version__
from vaifstudio.exceptions import (
    VaifAuthError,
    VaifConflictError,
    VaifError,
    VaifNetworkError,
    VaifNotFoundError,
    VaifRateLimitError,
    VaifServerError,
    VaifTimeoutError,
    VaifValidationError,
)
from vaifstudio.retry import REPLAY_SAFE_METHODS, RetryPolicy

API_KEY_HEADER = "x-vaif-key"
#: The cookie that carries an end user's rotating refresh token.
REFRESH_COOKIE = "project_refresh_token"
#: Set by the API on every response a function produced, and only on those.
RUN_ID_HEADER = "x-vaif-run-id"
#: The only hosts reached over plain http or ws: local development.
LOOPBACK_HOSTS = frozenset({"localhost", "127.0.0.1", "::1"})


def header_present(headers: Optional[Mapping[str, str]], name: str) -> bool:
    """True when ``headers`` already carries ``name``, compared case-insensitively."""
    if not headers:
        return False
    target = name.lower()
    return any(str(key).lower() == target for key in headers)


def path_segment(value: Any, what: str) -> str:
    """``value`` percent-encoded as one URL path segment.

    ``.`` and ``..`` pass through percent-encoding unchanged, and the HTTP
    stack then removes them as dot segments, so the request would reach a
    different route with the same key and session. They raise ``ValueError``.
    """
    text = str(value)
    if text in (".", ".."):
        raise ValueError(f"{what} must not be {text!r}: it would change the request path")
    return quote(text, safe="")


def normalize_base_url(base_url: str) -> str:
    """Validate and normalize the API base URL.

    HTTPS is required so API keys and tokens never travel in cleartext. Plain
    HTTP is accepted only for loopback hosts (local development).
    """
    if not base_url:
        raise ValueError("base_url must not be empty")
    parts = urlsplit(base_url)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        raise ValueError("base_url must be an absolute http(s) URL")
    if parts.scheme == "http" and parts.hostname not in LOOPBACK_HOSTS:
        raise ValueError(
            "base_url must use https (http is accepted only for localhost, 127.0.0.1 and ::1)"
        )
    return base_url.rstrip("/")


#: Redirects followed when reading a signed storage URL.
MAX_STORAGE_REDIRECTS = 5


def check_storage_url(url: str) -> str:
    """Return ``url`` if it is an absolute https URL, or http to a loopback host.

    Signed upload and download URLs carry their own authorization, so one
    sent over plain http could be read and replayed. Anything else raises
    ``VaifError`` with code ``INSECURE_STORAGE_URL``.
    """
    try:
        parts = urlsplit(url)
        hostname = parts.hostname
    except ValueError:
        hostname = None
        parts = None
    scheme = parts.scheme.lower() if parts is not None else ""
    if hostname and (scheme == "https" or (scheme == "http" and hostname in LOOPBACK_HOSTS)):
        return url
    raise VaifError(
        "The storage URL must use https (http only for localhost, 127.0.0.1 or ::1)",
        code="INSECURE_STORAGE_URL",
    )


def without_credentials(url: str) -> str:
    """``url`` without its user information, query string and fragment.

    A signed URL's query string grants access to an object, and user
    information is a credential, so neither is kept on an error.
    """
    try:
        parts = urlsplit(url)
    except ValueError:
        return ""
    netloc = parts.netloc.rpartition("@")[2]
    return urlunsplit((parts.scheme, netloc, parts.path, "", ""))


def error_headers(response: httpx.Response) -> httpx.Headers:
    """The response headers kept on an error, with ``Location`` stripped of credentials."""
    headers = httpx.Headers(response.headers)
    if "location" in headers:
        headers["location"] = without_credentials(headers["location"])
    return headers


def _parse_retry_after(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    value = value.strip()
    try:
        return max(0.0, float(value))
    except ValueError:
        pass
    try:
        when = email.utils.parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if when is None:
        return None
    return max(0.0, when.timestamp() - time.time())


def _decode_body(response: httpx.Response) -> Any:
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError:
        return response.text


def error_from_response(response: httpx.Response) -> VaifError:
    """Map a non-2xx response to the matching :class:`VaifError` subclass."""
    body = _decode_body(response)
    message: Optional[str] = None
    code: Optional[str] = None
    details: Any = None
    request_id: Optional[str] = None
    if isinstance(body, dict):
        raw_message = body.get("message")
        raw_error = body.get("error")
        raw_code = body.get("code")
        # The copilot routes nest the code and message in an envelope:
        # {"error": {"code", "message", "statusCode", "retryable", ...}, "message"}
        # (a refused plan confirm: PLAN_ALREADY_CONFIRMED, PLAN_STALE, PLAN_EXPIRED, ...).
        envelope = raw_error if isinstance(raw_error, dict) else {}
        nested_message = envelope.get("message")
        nested_code = envelope.get("code")
        if isinstance(raw_message, str) and raw_message:
            message = raw_message
        elif isinstance(nested_message, str) and nested_message:
            message = nested_message
        elif isinstance(raw_error, str) and raw_error:
            message = raw_error
        if isinstance(raw_code, str) and raw_code:
            code = raw_code
        elif isinstance(nested_code, str) and nested_code:
            code = nested_code
        elif isinstance(raw_error, str) and raw_error:
            code = raw_error
        details = body.get("details")
        if isinstance(body.get("requestId"), str):
            request_id = body["requestId"]
    elif isinstance(body, str) and body and len(body) < 500:
        message = body
    if message is None:
        message = response.reason_phrase or f"HTTP {response.status_code}"
    request_id = request_id or response.headers.get("x-request-id")
    status = response.status_code
    kwargs: dict[str, Any] = {
        "status": status,
        "code": code,
        "details": details,
        "request_id": request_id,
        "body": body,
        "headers": error_headers(response),
    }
    if status in (400, 422):
        return VaifValidationError(message, **kwargs)
    if status in (401, 403):
        return VaifAuthError(message, **kwargs)
    if status == 404:
        return VaifNotFoundError(message, **kwargs)
    if status == 409:
        return VaifConflictError(message, **kwargs)
    if status == 429:
        retry_after = _parse_retry_after(response.headers.get("retry-after"))
        return VaifRateLimitError(message, retry_after=retry_after, **kwargs)
    if status >= 500:
        return VaifServerError(message, **kwargs)
    return VaifError(message, **kwargs)


def redirect_error(response: httpx.Response) -> VaifError:
    """The error for a redirect the SDK did not follow.

    ``headers`` keeps ``Location`` without its user information, query string
    and fragment (see :func:`without_credentials`).
    """
    return VaifError(
        f"The API answered with a redirect (HTTP {response.status_code}), "
        "which the SDK does not follow",
        status=response.status_code,
        code="REDIRECT_NOT_FOLLOWED",
        request_id=response.headers.get("x-request-id"),
        headers=error_headers(response),
    )


class HttpTransport:
    """Sends requests with the project key, timeouts and bounded retries."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        timeout: float,
        retry: RetryPolicy,
        headers: Optional[Mapping[str, str]] = None,
        http_client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        if not api_key:
            raise ValueError("api_key must not be empty")
        if timeout <= 0:
            raise ValueError("timeout must be > 0 seconds")
        self.base_url = normalize_base_url(base_url)
        self._api_key = api_key
        self._timeout = timeout
        self.retry = retry
        self._headers = dict(headers or {})
        self._owns_client = http_client is None
        self._client = http_client or httpx.AsyncClient(timeout=timeout)

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    def _build_headers(
        self, extra: Optional[Mapping[str, str]], bearer: Optional[str]
    ) -> dict[str, str]:
        headers = {
            "Accept": "application/json",
            "Accept-Versions": "v1",
            "User-Agent": f"vaif-python/{__version__}",
            **self._headers,
        }
        if extra:
            headers.update(extra)
        headers[API_KEY_HEADER] = self._api_key
        # A caller-supplied Authorization wins, including over the session
        # bearer: overwriting it would make console calls fail with 401 while
        # an end-user session is active.
        if bearer and not header_present(headers, "authorization"):
            headers["Authorization"] = f"Bearer {bearer}"
        return headers

    def supplies_authorization(self, extra: Optional[Mapping[str, str]]) -> bool:
        """True when the client or this request already set Authorization."""
        client_set = header_present(self._headers, "authorization")
        request_set = header_present(extra, "authorization")
        return client_set or request_set

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Mapping[str, Any]] = None,
        json: Any = None,
        content: Any = None,
        headers: Optional[Mapping[str, str]] = None,
        bearer: Optional[str] = None,
        idempotent: Optional[bool] = None,
        timeout: Optional[float] = None,
        retry: Optional[RetryPolicy] = None,
        allow_redirect: bool = False,
    ) -> httpx.Response:
        """Send a request and return the successful response.

        Raises a :class:`VaifError` subclass for non-2xx responses and network
        failures once the retry budget is spent. A redirect is never followed.
        With ``allow_redirect``, it is returned instead of raised, for the
        caller to read the signed link it points to with :meth:`get_signed`.
        """
        method = method.upper()
        policy = retry or self.retry
        replay_safe = idempotent if idempotent is not None else method in REPLAY_SAFE_METHODS
        url = f"{self.base_url}{path}"
        request_headers = self._build_headers(headers, bearer)
        request_timeout = timeout if timeout is not None else self._timeout
        attempt = 0
        while True:
            try:
                response = await self._client.request(
                    method,
                    url,
                    params=params,
                    json=json,
                    content=content,
                    headers=request_headers,
                    timeout=request_timeout,
                    # Never follow a redirect, even on a client passed in with
                    # follow_redirects=True: the next request would carry the
                    # project key and the session token to another origin.
                    follow_redirects=False,
                )
            except (httpx.ConnectError, httpx.ConnectTimeout) as exc:
                # The request never reached the server: safe to retry any method.
                if attempt < policy.max_retries and policy.retry_on_network_error:
                    await asyncio.sleep(policy.delay_for(attempt))
                    attempt += 1
                    continue
                if isinstance(exc, httpx.ConnectTimeout):
                    raise VaifTimeoutError("Timed out connecting to the VAIF API") from exc
                raise VaifNetworkError(
                    f"Could not connect to the VAIF API: {type(exc).__name__}"
                ) from exc
            except httpx.TimeoutException as exc:
                if replay_safe and attempt < policy.max_retries and policy.retry_on_network_error:
                    await asyncio.sleep(policy.delay_for(attempt))
                    attempt += 1
                    continue
                raise VaifTimeoutError(f"Request timed out after {request_timeout}s") from exc
            except httpx.TransportError as exc:
                if replay_safe and attempt < policy.max_retries and policy.retry_on_network_error:
                    await asyncio.sleep(policy.delay_for(attempt))
                    attempt += 1
                    continue
                raise VaifNetworkError(f"Network error: {type(exc).__name__}") from exc
            except httpx.RequestError as exc:
                # For example DecodingError: a body that does not match its
                # Content-Encoding. Repeating the request would not change it.
                raise VaifNetworkError(
                    f"Could not read the API response: {type(exc).__name__}"
                ) from exc

            # The SDK reads the refresh cookie explicitly (see auth.py) and
            # sends it explicitly, so no cookie jar keeps it: one session's
            # refresh token must not travel on another session's requests.
            # The SDK's own client keeps no cookies at all; a client passed
            # in keeps its other cookies.
            if self._owns_client:
                self._client.cookies.clear()
            else:
                self._client.cookies.delete(REFRESH_COOKIE)

            if response.is_success:
                return response
            if response.is_redirect:
                if allow_redirect:
                    return response
                raise redirect_error(response)
            error = error_from_response(response)
            transient = response.status_code in policy.retry_on
            if replay_safe and transient and attempt < policy.max_retries:
                retry_after = error.retry_after if isinstance(error, VaifRateLimitError) else None
                await asyncio.sleep(policy.delay_for(attempt, retry_after))
                attempt += 1
                continue
            raise error

    async def put_presigned(self, url: str, content: bytes, content_type: str) -> None:
        """PUT bytes to a presigned storage URL.

        The URL points at the object store, not the VAIF API, so none of the
        client's headers (API key, bearer token) are sent. A PUT of the same
        bytes to the same key is idempotent, so it is retried like a GET.
        """
        check_storage_url(url)
        policy = self.retry
        attempt = 0
        while True:
            try:
                response = await self._client.put(
                    url,
                    content=content,
                    headers={"Content-Type": content_type},
                    timeout=self._timeout,
                    follow_redirects=False,
                )
            except httpx.TimeoutException as exc:
                if attempt < policy.max_retries and policy.retry_on_network_error:
                    await asyncio.sleep(policy.delay_for(attempt))
                    attempt += 1
                    continue
                raise VaifTimeoutError("Timed out uploading to storage") from exc
            except httpx.RequestError as exc:
                if attempt < policy.max_retries and policy.retry_on_network_error:
                    await asyncio.sleep(policy.delay_for(attempt))
                    attempt += 1
                    continue
                raise VaifNetworkError(f"Network error uploading: {type(exc).__name__}") from exc
            if self._owns_client:
                self._client.cookies.clear()
            if response.is_success:
                return
            if response.status_code in policy.retry_on and attempt < policy.max_retries:
                await asyncio.sleep(policy.delay_for(attempt))
                attempt += 1
                continue
            error = error_from_response(response)
            error.code = error.code or "STORAGE_UPLOAD_FAILED"
            raise error

    async def get_signed(self, url: str) -> bytes:
        """GET the bytes behind a signed download URL.

        The URL points at the file host, not the VAIF API, so none of the
        client's headers (API key, bearer token, custom headers) are sent.
        Redirects are followed by the SDK, at most ``MAX_STORAGE_REDIRECTS``,
        and only to https URLs (http only for loopback hosts). A GET is
        replay-safe, so it is retried like any other GET.
        """
        policy = self.retry
        current = check_storage_url(url)
        attempt = 0
        redirects = 0
        while True:
            try:
                response = await self._client.get(
                    current, timeout=self._timeout, follow_redirects=False
                )
            except httpx.TimeoutException as exc:
                if attempt < policy.max_retries and policy.retry_on_network_error:
                    await asyncio.sleep(policy.delay_for(attempt))
                    attempt += 1
                    continue
                raise VaifTimeoutError("Timed out downloading from storage") from exc
            except httpx.RequestError as exc:
                if attempt < policy.max_retries and policy.retry_on_network_error:
                    await asyncio.sleep(policy.delay_for(attempt))
                    attempt += 1
                    continue
                raise VaifNetworkError(f"Network error downloading: {type(exc).__name__}") from exc
            if self._owns_client:
                self._client.cookies.clear()
            if response.is_success:
                return response.content
            if response.is_redirect:
                if redirects >= MAX_STORAGE_REDIRECTS:
                    raise VaifError(
                        "The storage download was redirected more than "
                        f"{MAX_STORAGE_REDIRECTS} times",
                        status=response.status_code,
                        code="STORAGE_DOWNLOAD_FAILED",
                    )
                redirects += 1
                current = check_storage_url(urljoin(current, response.headers["location"]))
                continue
            if response.status_code in policy.retry_on and attempt < policy.max_retries:
                await asyncio.sleep(policy.delay_for(attempt))
                attempt += 1
                continue
            error = error_from_response(response)
            error.code = error.code or "STORAGE_DOWNLOAD_FAILED"
            raise error


def response_json(response: httpx.Response) -> Any:
    """Decode a JSON body, returning ``None`` for an empty body."""
    if not response.content:
        return None
    try:
        return response.json()
    except ValueError as exc:
        raise VaifError(
            "The API returned a non-JSON response",
            status=response.status_code,
            body=response.text[:500],
        ) from exc
