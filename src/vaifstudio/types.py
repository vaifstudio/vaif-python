"""Public data types returned by the SDK."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional

Row = Dict[str, Any]


@dataclass(frozen=True)
class User:
    """A project end user (``/projects/:projectId/auth``)."""

    id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    provider: Optional[str] = None
    metadata: Any = None
    email_verified_at: Optional[str] = None
    created_at: Optional[str] = None
    raw: Mapping[str, Any] = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_api(cls, data: Mapping[str, Any]) -> User:
        return cls(
            id=str(data.get("id", "")),
            email=data.get("email"),
            phone=data.get("phone"),
            provider=data.get("provider"),
            metadata=data.get("metadata"),
            email_verified_at=data.get("emailVerifiedAt"),
            created_at=data.get("createdAt"),
            raw=dict(data),
        )


@dataclass(frozen=True)
class Session:
    """An authenticated end-user session.

    ``refresh_token`` is the opaque rotating token the API issues in the
    ``project_refresh_token`` cookie. Persist it securely if the session
    should survive restarts, and restore it with ``auth.set_session``.
    Neither token appears in ``repr()``, so logging a session does not log
    a credential.
    """

    access_token: str = field(repr=False)
    expires_at: float
    refresh_token: Optional[str] = field(default=None, repr=False)
    user: Optional[User] = None

    @property
    def expires_in(self) -> float:
        """Seconds until the access token expires (negative when expired)."""
        return self.expires_at - time.time()

    def is_expired(self, leeway: float = 0.0) -> bool:
        return self.expires_in <= leeway


@dataclass(frozen=True)
class SignInResult:
    """Outcome of ``auth.sign_in``: a session, or an MFA challenge to complete."""

    session: Optional[Session] = None
    mfa_required: bool = False
    challenge_token: Optional[str] = field(default=None, repr=False)


@dataclass(frozen=True)
class SignUpResult:
    """Outcome of ``auth.sign_up``.

    ``session`` is ``None`` when the API answers ``pendingVerification`` (for
    example when the address already has an account: the API does not reveal
    which addresses exist).
    """

    session: Optional[Session] = None
    user: Optional[User] = None
    pending_verification: bool = False
    message: Optional[str] = None


@dataclass(frozen=True)
class ListResult:
    """Rows from a list query and the total number of matching rows."""

    data: List[Row]
    count: int


@dataclass(frozen=True)
class Page:
    """One page of an offset-paginated query."""

    data: List[Row]
    total: int
    page: int
    page_size: int

    @property
    def page_count(self) -> int:
        return (self.total + self.page_size - 1) // self.page_size if self.page_size else 0

    @property
    def has_next(self) -> bool:
        return self.page < self.page_count

    @property
    def has_previous(self) -> bool:
        return self.page > 1


@dataclass(frozen=True)
class UploadResult:
    """Result of ``storage.upload``."""

    key: str
    bucket: Optional[str]
    size: int


@dataclass(frozen=True)
class FunctionResponse:
    """The HTTP response produced by a function invocation."""

    status: int
    headers: Mapping[str, str]
    data: Any


__all__ = [
    "Row",
    "User",
    "Session",
    "SignInResult",
    "SignUpResult",
    "ListResult",
    "Page",
    "UploadResult",
    "FunctionResponse",
]
