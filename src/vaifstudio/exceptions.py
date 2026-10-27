"""Typed errors raised by the VAIF SDK.

Every failure surfaces as a :class:`VaifError` subclass, so callers can catch
the base class or branch on the specific type. ``code`` carries the server's
machine-readable error code (``INVALID_CREDENTIALS``, ``INVALID_COLUMN``,
``NOT_FOUND`` ...) when the API sends one.
"""

from __future__ import annotations

from typing import Any, Mapping, Optional

import httpx

CONSOLE_SIGN_UP_URL = "https://console.vaif.studio/register"
CONSOLE_PASSWORD_RESET_URL = "https://console.vaif.studio/forgot-password"


class VaifError(Exception):
    """Base class for every error raised by the SDK.

    ``headers`` holds the HTTP response headers, matched case-insensitively.
    It is empty when the error did not come from an HTTP response.
    """

    def __init__(
        self,
        message: str,
        *,
        status: Optional[int] = None,
        code: Optional[str] = None,
        details: Any = None,
        request_id: Optional[str] = None,
        body: Any = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.details = details
        self.request_id = request_id
        self.body = body
        self.headers = httpx.Headers(headers)

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(message={self.message!r}, status={self.status!r}, "
            f"code={self.code!r}, request_id={self.request_id!r})"
        )


class VaifConsoleOnlyError(VaifError):
    """Platform account creation and password reset happen in the console.

    Code ``CONSOLE_ONLY``, raised before any request. ``console_url`` is the
    console page to send the person to; ``method`` names the SDK call that
    raised it.
    """

    def __init__(
        self,
        method: str,
        *,
        password_reset: bool = False,
        own_app: str = "create the client with your project_id",
    ) -> None:
        self.method = method
        self.console_url = CONSOLE_PASSWORD_RESET_URL if password_reset else CONSOLE_SIGN_UP_URL
        if password_reset:
            message = (
                f"Reset your VAIF Studio password in the console at {self.console_url}. "
                f"To reset passwords for users of your own app, {own_app}."
            )
        else:
            message = (
                f"Create your VAIF Studio account in the console at {self.console_url}. "
                f"To sign up users of your own app, {own_app}."
            )
        super().__init__(message, code="CONSOLE_ONLY")


class VaifValidationError(VaifError):
    """The request was rejected as invalid (HTTP 400 / 422)."""


class VaifAuthError(VaifError):
    """Authentication or authorization failed (HTTP 401 / 403)."""


class VaifNotFoundError(VaifError):
    """The resource does not exist (HTTP 404)."""


class VaifConflictError(VaifError):
    """The request conflicts with current state (HTTP 409)."""


class VaifRateLimitError(VaifError):
    """Too many requests (HTTP 429). ``retry_after`` is in seconds when known."""

    def __init__(self, message: str, *, retry_after: Optional[float] = None, **kwargs: Any) -> None:
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class VaifServerError(VaifError):
    """The server failed to handle the request (HTTP 5xx)."""


class VaifNetworkError(VaifError):
    """The request could not be completed at the network level."""


class VaifTimeoutError(VaifNetworkError):
    """The request timed out."""


__all__ = [
    "VaifError",
    "VaifConsoleOnlyError",
    "VaifValidationError",
    "VaifAuthError",
    "VaifNotFoundError",
    "VaifConflictError",
    "VaifRateLimitError",
    "VaifServerError",
    "VaifNetworkError",
    "VaifTimeoutError",
]
