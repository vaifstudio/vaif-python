"""End-to-end run against a real VAIF API.

Skipped unless these are set (a throwaway project is expected):

    VAIF_IT_BASE_URL    e.g. http://127.0.0.1:3791
    VAIF_IT_PROJECT_ID  project id
    VAIF_IT_API_KEY     project key with crud + storage + functions scopes
    VAIF_IT_TABLE       table with a text column "name" (default: sdk_items)
"""

from __future__ import annotations

import os
import uuid

import pytest

from vaifstudio import VaifAuthError, VaifClient, VaifNotFoundError, VaifValidationError

BASE_URL = os.environ.get("VAIF_IT_BASE_URL")
PROJECT_ID = os.environ.get("VAIF_IT_PROJECT_ID")
API_KEY = os.environ.get("VAIF_IT_API_KEY")
TABLE = os.environ.get("VAIF_IT_TABLE", "sdk_items")

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        not (BASE_URL and PROJECT_ID and API_KEY), reason="VAIF_IT_* environment not set"
    ),
]


def make_client() -> VaifClient:
    assert BASE_URL and PROJECT_ID and API_KEY
    return VaifClient(PROJECT_ID, API_KEY, base_url=BASE_URL, timeout=20.0)


async def test_auth_lifecycle() -> None:
    email = f"py-{uuid.uuid4().hex[:10]}@example.com"
    password = f"Pw-{uuid.uuid4().hex}"
    async with make_client() as vaif:
        signed_up = await vaif.auth.sign_up(email, password, metadata={"sdk": "python"})
        assert signed_up.session is not None
        assert signed_up.session.refresh_token, "refresh cookie was not captured"

        await vaif.auth.sign_out()
        assert vaif.auth.session is None

        with pytest.raises(VaifAuthError):
            await vaif.auth.sign_in(email, password + "-wrong")

        result = await vaif.auth.sign_in(email, password)
        assert result.session is not None
        me = await vaif.auth.get_user()
        assert me.email == email

        first = vaif.auth.session
        assert first is not None
        refreshed = await vaif.auth.refresh_session()
        assert refreshed.refresh_token and refreshed.refresh_token != first.refresh_token
        assert (await vaif.auth.get_user()).id == me.id

        await vaif.auth.sign_out()
        # The revoked refresh token must no longer work.
        vaif.auth.set_session(refreshed.access_token, refreshed.refresh_token)
        with pytest.raises(VaifAuthError):
            await vaif.auth.refresh_session()


async def test_data_crud_filters_and_pagination() -> None:
    marker = uuid.uuid4().hex[:8]
    async with make_client() as vaif:
        table = vaif.from_(TABLE)
        created = await table.insert({"name": f"{marker}-a"})
        assert created["name"] == f"{marker}-a"
        rows = await table.insert_many([{"name": f"{marker}-b"}, {"name": f"{marker}-c"}])
        assert len(rows) == 2

        fetched = await table.get(created["id"])
        assert fetched["id"] == created["id"]

        mine = table.like("name", f"{marker}-%")
        listed = await mine.order("name").list()
        assert [r["name"] for r in listed.data] == [f"{marker}-a", f"{marker}-b", f"{marker}-c"]
        assert listed.count == 3

        page = await mine.order("name").paginate(page=2, page_size=2)
        assert page.total == 3 and [r["name"] for r in page.data] == [f"{marker}-c"]
        assert not page.has_next

        only_b = await mine.eq("name", f"{marker}-b").select("id", "name").list()
        assert only_b.count == 1 and set(only_b.data[0]) == {"id", "name"}

        updated = await table.update(created["id"], {"name": f"{marker}-z"})
        assert updated["name"] == f"{marker}-z"

        for row in [created, *rows]:
            await table.delete(row["id"])
        with pytest.raises(VaifNotFoundError):
            await table.get(created["id"])

        with pytest.raises(VaifValidationError) as info:
            await table.eq("no_such_column", 1).list()
        assert info.value.code == "INVALID_COLUMN"


async def test_storage_round_trip() -> None:
    key = f"sdk-it/python-{uuid.uuid4().hex}.txt"
    payload = b"hello from the python sdk"
    async with make_client() as vaif:
        uploaded = await vaif.storage.upload(key, payload, content_type="text/plain")
        assert uploaded.size == len(payload)
        assert await vaif.storage.download(key) == payload
        url = await vaif.storage.create_signed_url(key)
        assert url.startswith("http")
        with pytest.raises(VaifNotFoundError):
            await vaif.storage.download(f"sdk-it/missing-{uuid.uuid4().hex}.txt")


async def test_functions_unknown_function_is_not_found() -> None:
    async with make_client() as vaif:
        with pytest.raises(VaifNotFoundError):
            await vaif.functions.invoke(f"missing-{uuid.uuid4().hex[:8]}", {"x": 1})
