from __future__ import annotations

from typing import AsyncIterator

import pytest

from vaifstudio import RetryPolicy, VaifClient

BASE = "https://api.test.vaif"
PROJECT = "proj_123"
KEY = "vk_pub_test"

# No sleeping in unit tests: every delay collapses to zero.
FAST_RETRY = RetryPolicy(max_retries=3, base_delay=0.0, max_delay=0.0)


@pytest.fixture
async def client() -> AsyncIterator[VaifClient]:
    c = VaifClient(PROJECT, KEY, base_url=BASE, retry=FAST_RETRY)
    try:
        yield c
    finally:
        await c.close()


def data_url(table: str, suffix: str = "") -> str:
    return f"{BASE}/v1/data/{PROJECT}/{table}{suffix}"


def auth_url(suffix: str) -> str:
    return f"{BASE}/projects/{PROJECT}/auth/{suffix}"
