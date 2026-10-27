"""Bounded retry policy with exponential backoff and jitter.

Only replay-safe methods (GET, HEAD, OPTIONS) are retried on 429/5xx and on
network errors, plus two requests that repeat no work: the one behind
``storage.create_signed_url()`` and the object-store ``PUT`` in
``storage.upload()``. A request that never reached the server (connection
refused, DNS failure, connect timeout) is retried for every method, because
nothing was executed. ``functions.invoke()`` accepts ``idempotent=True`` when
the caller knows a replay is harmless.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import FrozenSet, Optional

REPLAY_SAFE_METHODS: FrozenSet[str] = frozenset({"GET", "HEAD", "OPTIONS"})
DEFAULT_RETRY_STATUSES: FrozenSet[int] = frozenset({429, 500, 502, 503, 504})


@dataclass(frozen=True)
class RetryPolicy:
    """How transient failures are retried.

    Attributes:
        max_retries: Retries after the first attempt (0 disables retries).
        base_delay: Delay before the first retry, in seconds.
        max_delay: Cap on the backoff before jitter (up to 25% more) and on
            Retry-After, in seconds.
        multiplier: Exponential growth factor between retries.
        retry_on: HTTP statuses treated as transient.
        retry_on_network_error: Retry replay-safe requests on network errors.
    """

    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    multiplier: float = 2.0
    retry_on: FrozenSet[int] = field(default_factory=lambda: DEFAULT_RETRY_STATUSES)
    retry_on_network_error: bool = True

    def __post_init__(self) -> None:
        if self.max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        if self.base_delay < 0 or self.max_delay < 0:
            raise ValueError("retry delays must be >= 0")

    def delay_for(self, attempt: int, retry_after: Optional[float] = None) -> float:
        """Seconds to wait before retry number ``attempt`` (0-based)."""
        if retry_after is not None and retry_after > 0:
            return min(retry_after, self.max_delay)
        delay = min(self.base_delay * (self.multiplier**attempt), self.max_delay)
        # Up to 25% jitter so many clients do not retry in lockstep.
        return delay + delay * random.random() * 0.25


NO_RETRY = RetryPolicy(max_retries=0)

__all__ = ["RetryPolicy", "NO_RETRY", "REPLAY_SAFE_METHODS", "DEFAULT_RETRY_STATUSES"]
