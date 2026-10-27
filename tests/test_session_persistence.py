"""Saving a session across restarts, as the README's "Persisting a session" teaches.

The SDK keeps sessions in memory and reports every change to
``on_session_change`` listeners; the application saves them. These tests run
the README's example itself, so the documented pattern is the tested one.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable, Optional

import httpx
import pytest
import respx

from tests.conftest import BASE, FAST_RETRY, KEY, PROJECT, auth_url
from tests.test_auth import login_response
from vaifstudio import VaifClient, VaifError

README = Path(__file__).resolve().parents[1] / "README.md"


class SecureStore:
    """A stand-in for the OS keychain: get returns None when nothing is saved."""

    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.fail_save = False
        self.fail_delete = False

    def get(self, key: str) -> Optional[str]:
        return self.values.get(key)

    def save(self, key: str, value: str) -> None:
        if self.fail_save:
            raise OSError("keychain is locked")
        self.values[key] = value

    def delete(self, key: str) -> None:
        if self.fail_delete:
            raise OSError("keychain is locked")
        self.values.pop(key, None)


def readme_example(store: SecureStore) -> dict[str, Callable[..., Any]]:
    text = README.read_text(encoding="utf-8")
    section = text[text.index("### Persisting a session") :]
    code = re.search(r"```python\n(.*?)\n```", section, re.S)
    assert code is not None, "README: no example under 'Persisting a session'"
    namespace: dict[str, Any] = {"secure_store": store}
    exec(compile(code.group(1), str(README), "exec"), namespace)
    return namespace


def test_the_saved_session_is_keyed_by_api_origin_and_project() -> None:
    example = readme_example(SecureStore())
    first = VaifClient(PROJECT, KEY, base_url="https://api.vaif.studio")
    second = VaifClient(PROJECT, KEY, base_url="https://api.eu.example.com")
    assert example["session_key"](first) == "vaif-session:https://api.vaif.studio|proj_123"
    assert example["session_key"](second) == "vaif-session:https://api.eu.example.com|proj_123"


@respx.mock
async def test_clients_for_one_project_at_different_base_urls_share_no_session() -> None:
    store = SecureStore()
    example = readme_example(store)
    respx.post(auth_url("login")).mock(return_value=login_response("at_1", "rt_1"))

    async with VaifClient(PROJECT, KEY, base_url=BASE, retry=FAST_RETRY) as signed_in:
        example["restore_session"](signed_in)
        example["persist_sessions"](signed_in)
        await signed_in.auth.sign_in("ada@example.com", "pw")
    assert list(store.values) == ["vaif-session:https://api.test.vaif|proj_123"]

    async with VaifClient(PROJECT, KEY, base_url="https://api.other.example") as other:
        example["restore_session"](other)
        assert other.auth.session is None
    async with VaifClient(PROJECT, KEY, base_url=BASE) as same:
        example["restore_session"](same)
        assert same.auth.session is not None
        assert same.auth.session.refresh_token == "rt_1"


@respx.mock
async def test_a_session_that_cannot_be_saved_leaves_no_older_session_restorable() -> None:
    store = SecureStore()
    example = readme_example(store)
    respx.post(auth_url("login")).mock(return_value=login_response("at_1", "rt_1"))
    respx.post(auth_url("refresh")).mock(return_value=login_response("at_2", "rt_2"))

    async with VaifClient(PROJECT, KEY, base_url=BASE, retry=FAST_RETRY) as vaif:
        example["persist_sessions"](vaif)
        await vaif.auth.sign_in("ada@example.com", "pw")
        saved = json.loads(store.values["vaif-session:https://api.test.vaif|proj_123"])
        assert saved["refresh_token"] == "rt_1"

        store.fail_save = True
        await vaif.auth.refresh_session()  # rotates rt_1; rt_2 cannot be saved
    assert store.values == {}


@respx.mock
async def test_sign_out_raises_when_the_saved_session_cannot_be_cleared() -> None:
    store = SecureStore()
    example = readme_example(store)
    respx.post(auth_url("login")).mock(return_value=login_response("at_1", "rt_1"))
    logout = respx.post(auth_url("logout")).mock(
        return_value=httpx.Response(200, json={"ok": True})
    )

    async with VaifClient(PROJECT, KEY, base_url=BASE, retry=FAST_RETRY) as vaif:
        example["persist_sessions"](vaif)
        await vaif.auth.sign_in("ada@example.com", "pw")
        store.fail_delete = True
        with pytest.raises(VaifError) as info:
            await vaif.auth.sign_out()
        assert vaif.auth.session is None
    assert info.value.code == "SESSION_STORAGE_FAILED"
    assert isinstance(info.value.__cause__, OSError)
    # The server revoked the session before the error was raised.
    assert json.loads(logout.calls.last.request.content) == {"refreshToken": "rt_1"}
    assert list(store.values) == ["vaif-session:https://api.test.vaif|proj_123"]


VERIFIER = "v" * 43


async def _sign_in_as_bob(vaif: VaifClient, how: str) -> None:
    """Install user B's session through each call that signs a user in."""
    if how == "sign_in":
        await vaif.auth.sign_in("bob@example.com", "pw")
    elif how == "sign_up":
        await vaif.auth.sign_up("bob@example.com", "pw")
    elif how == "verify_mfa":
        await vaif.auth.verify_mfa("challenge_1", "123456")
    else:
        await vaif.auth.handle_oauth_callback(
            "code_1", state="s", expected_state="s", code_verifier=VERIFIER
        )


@pytest.mark.parametrize("how", ["sign_in", "sign_up", "verify_mfa", "oauth_callback"])
@pytest.mark.parametrize("delete_fails", [False, True], ids=["delete_works", "delete_fails"])
@respx.mock
async def test_a_sign_in_that_cannot_save_the_new_session_raises(
    how: str, delete_fails: bool
) -> None:
    # User A signed in earlier and is saved. The store then refuses to save
    # B's session, and, when delete_fails, to delete A's: A's session would be
    # restored on the next start. The caller is told, because nothing else
    # shows it.
    store = SecureStore()
    example = readme_example(store)
    key = "vaif-session:https://api.test.vaif|proj_123"
    for route in ("signup", "login", "mfa/verify", "oauth/token"):
        respx.post(auth_url(route)).mock(return_value=login_response("at_a", "rt_a"))

    async with VaifClient(PROJECT, KEY, base_url=BASE, retry=FAST_RETRY) as vaif:
        example["persist_sessions"](vaif)
        await vaif.auth.sign_in("ada@example.com", "pw")
        assert json.loads(store.values[key])["refresh_token"] == "rt_a"

        for route in ("signup", "login", "mfa/verify", "oauth/token"):
            respx.post(auth_url(route)).mock(return_value=login_response("at_b", "rt_b"))
        store.fail_save = True
        store.fail_delete = delete_fails
        with pytest.raises(VaifError) as info:
            await _sign_in_as_bob(vaif, how)

        assert info.value.code == "SESSION_STORAGE_FAILED"
        assert isinstance(info.value.__cause__, OSError)
        # B is signed in for this run of the application.
        assert vaif.auth.session is not None
        assert vaif.auth.session.access_token == "at_b"
    if delete_fails:
        assert json.loads(store.values[key])["refresh_token"] == "rt_a"
    else:
        assert store.values == {}


@pytest.mark.parametrize("how", ["sign_in", "sign_up", "verify_mfa", "oauth_callback"])
@respx.mock
async def test_a_sign_in_that_is_saved_raises_nothing(how: str) -> None:
    store = SecureStore()
    example = readme_example(store)
    for route in ("signup", "login", "mfa/verify", "oauth/token"):
        respx.post(auth_url(route)).mock(return_value=login_response("at_b", "rt_b"))

    async with VaifClient(PROJECT, KEY, base_url=BASE, retry=FAST_RETRY) as vaif:
        example["persist_sessions"](vaif)
        await _sign_in_as_bob(vaif, how)
    saved = json.loads(store.values["vaif-session:https://api.test.vaif|proj_123"])
    assert saved["refresh_token"] == "rt_b"
