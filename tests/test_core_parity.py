from __future__ import annotations

import json

import pytest
import respx

from tests.conftest import BASE, auth_url, data_url
from tests.test_auth import login_response
from vaifstudio import VaifClient, VaifError


@pytest.mark.parametrize("name", ["post_auth_signup", "post_auth_forgot_password"])
@respx.mock
async def test_generated_console_only_before_transport(client: VaifClient, name: str) -> None:
    with pytest.raises(VaifError) as caught:
        await getattr(client.operations, name)(body={"email": "a@example.com"})
    assert caught.value.code == "CONSOLE_ONLY"
    assert "https://console.vaif.studio/" in str(caught.value)
    assert not respx.calls


@pytest.mark.parametrize(
    "name,args",
    [("sign_up", ("a@example.com", "pw")), ("request_password_reset", ("a@example.com",))],
)
@respx.mock
async def test_platform_auth_is_console_only(name: str, args: tuple[str, ...]) -> None:
    async with VaifClient(None, "key", base_url=BASE) as client:
        with pytest.raises(VaifError) as caught:
            await getattr(client.auth, name)(*args)
        assert caught.value.code == "CONSOLE_ONLY"
        assert caught.value.__class__.__name__ == "VaifConsoleOnlyError"
        assert caught.value.console_url.startswith("https://console.vaif.studio/")
        assert not respx.calls


@pytest.mark.parametrize(
    "name,suffix,args,body",
    [
        ("enroll_start", "enroll-start", (), None),
        (
            "enroll_confirm",
            "enroll-confirm",
            ("enroll1", "123456"),
            {"enrollToken": "enroll1", "code": "123456"},
        ),
        ("disable", "disable", ("123456",), {"code": "123456"}),
        ("regenerate_codes", "regenerate-codes", ("123456",), {"code": "123456"}),
    ],
)
@respx.mock
async def test_mfa_management(
    client: VaifClient, name: str, suffix: str, args: tuple[str, ...], body: dict | None
) -> None:
    route = respx.post(auth_url("mfa/" + suffix)).respond(
        200, json={"ok": True, "backupCodes": ["one-use"]}
    )
    client.auth.set_session("at")
    result = await getattr(client.auth.mfa, name)(*args)
    assert result["ok"] is True
    request = route.calls.last.request
    assert request.headers["authorization"] == "Bearer at"
    assert (json.loads(request.content) if request.content else None) == body


@respx.mock
async def test_oauth_pkce_url_and_exchange(client: VaifClient) -> None:
    # RFC 7636, Appendix B: this verifier's S256 challenge.
    verifier = "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
    route = respx.post(auth_url("oauth/google/start")).respond(
        200, json={"url": "https://accounts.example/consent", "expiresIn": 600}
    )
    result = await client.auth.get_oauth_sign_in_url(
        "google",
        redirect_url="https://app.example/callback",
        code_verifier=verifier,
        state="state1",
    )
    payload = json.loads(route.calls.last.request.content)
    assert payload == {
        "redirectUrl": "https://app.example/callback",
        "codeChallenge": "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM",
        "codeChallengeMethod": "S256",
        "state": "state1",
    }
    assert result["code_verifier"] == verifier and result["state"] == "state1"
    assert result["url"] == "https://accounts.example/consent"
    exchange = respx.post(auth_url("oauth/token")).mock(return_value=login_response())
    signed_in = await client.auth.handle_oauth_callback(
        "one-use-code", state="state1", code_verifier=verifier, expected_state="state1"
    )
    assert signed_in.session.access_token == "at_1"
    assert client.auth.session.refresh_token == "rt_1"
    assert json.loads(exchange.calls.last.request.content) == {
        "code": "one-use-code",
        "codeVerifier": verifier,
    }


@pytest.mark.parametrize("verifier", ["", "short", "!" * 43, "x" * 129])
@respx.mock
async def test_invalid_pkce_never_sends(client: VaifClient, verifier: str) -> None:
    with pytest.raises(ValueError):
        await client.auth.get_oauth_sign_in_url(
            "google", redirect_url="https://app.example/cb", code_verifier=verifier
        )
    assert not respx.calls


@respx.mock
async def test_oauth_state_mismatch_never_sends(client: VaifClient) -> None:
    with pytest.raises(VaifError) as caught:
        await client.auth.handle_oauth_callback(
            "code", state="attacker", expected_state="original", code_verifier="v" * 43
        )
    assert caught.value.code == "OAUTH_STATE_MISMATCH"
    assert not respx.calls


@respx.mock
async def test_oauth_mfa_and_providers(client: VaifClient) -> None:
    respx.post(auth_url("oauth/token")).respond(
        200, json={"mfaRequired": True, "challengeToken": "challenge"}
    )
    result = await client.auth.handle_oauth_callback(
        "code", state="s", expected_state="s", code_verifier="v" * 43
    )
    assert result.mfa_required and result.challenge_token == "challenge"
    assert client.auth.session is None
    respx.get(auth_url("oauth/providers")).respond(
        200, json={"providers": [{"provider": "google"}]}
    )
    assert (await client.auth.list_oauth_providers())["providers"][0]["provider"] == "google"


@respx.mock
async def test_storage_delete_encodes_bucket_and_key(client: VaifClient) -> None:
    route = respx.delete(BASE + "/buckets/bucket%2Fid/files").respond(
        200, json={"ok": True, "deleted": True}
    )
    await client.storage.delete("folder/a & b.txt", bucket_id="bucket/id")
    assert route.calls.last.request.url.params["key"] == "folder/a & b.txt"


@respx.mock
async def test_range_count_and_immutable_query(client: VaifClient) -> None:
    route = respx.get(data_url("todos")).respond(200, json={"data": [{"id": "one"}], "count": 42})
    base = client.from_("todos").eq("done", False)
    result = await base.select("id").order("id").range(10, 19).list()
    assert result.count == 42
    assert dict(route.calls.last.request.url.params) == {
        "where": '{"field":"done","operator":"eq","value":false}',
        "select": "id",
        "orderBy": "id",
        "orderDir": "asc",
        "limit": "10",
        "offset": "10",
    }
    assert await base.count() == 42
    assert route.calls.last.request.url.params["limit"] == "1"
    await base.list()
    assert "offset" not in route.calls.last.request.url.params


@pytest.mark.parametrize("start,end", [(-1, 5), (3, 2), (0, 1000), (True, 3), (1.5, 3)])
async def test_invalid_range(client: VaifClient, start: int, end: int) -> None:
    with pytest.raises(ValueError):
        client.from_("todos").range(start, end)


@pytest.mark.parametrize(
    "name,project_operation,url",
    [
        (
            "post_auth_signup",
            "post_projects_by_project_id_auth_signup",
            "https://console.vaif.studio/register",
        ),
        (
            "post_auth_forgot_password",
            "post_projects_by_project_id_auth_forgot_password",
            "https://console.vaif.studio/forgot-password",
        ),
    ],
)
@respx.mock
async def test_generated_console_only_names_the_project_operation(
    client: VaifClient, name: str, project_operation: str, url: str
) -> None:
    # The error names the operation that raised it, and the message sends app
    # developers to the project-scoped operation.
    with pytest.raises(VaifError) as caught:
        await getattr(client.operations, name)(body={"email": "a@example.com"})
    assert caught.value.method == name + "()"
    assert caught.value.console_url == url
    assert project_operation in str(caught.value)
    assert hasattr(client.operations, project_operation)
    assert not respx.calls


async def test_platform_auth_console_only_message_names_the_console_page() -> None:
    async with VaifClient(None, "key", base_url=BASE) as platform:
        with pytest.raises(VaifError) as caught:
            await platform.auth.sign_up("a@example.com", "pw")
    assert str(caught.value) == (
        "Create your VAIF Studio account in the console at "
        "https://console.vaif.studio/register. To sign up users of your own app, "
        "create the client with your project_id."
    )
    assert caught.value.method == "auth.sign_up()"


@pytest.mark.parametrize(
    "call",
    [
        lambda auth: auth.sign_in("a@example.com", "pw"),
        lambda auth: auth.verify_mfa("challenge", "123456"),
        lambda auth: auth.get_user(),
        lambda auth: auth.reset_password("token", "new password"),
        lambda auth: auth.mfa.enroll_start(),
        lambda auth: auth.list_oauth_providers(),
    ],
)
@respx.mock
async def test_platform_client_auth_needs_a_project_before_any_request(call) -> None:
    # The Python SDK's auth is for your app's users (/projects/{id}/auth). VAIF
    # Studio accounts sign in through the console's session cookie, which this
    # client does not hold; a platform client says so instead of half-working.
    async with VaifClient(None, "key", base_url=BASE) as platform:
        platform.auth.set_session("account-token")
        with pytest.raises(VaifError) as caught:
            await call(platform.auth)
    assert caught.value.code == "PROJECT_ID_REQUIRED"
    assert not respx.calls
