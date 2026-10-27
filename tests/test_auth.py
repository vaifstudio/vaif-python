from __future__ import annotations

import asyncio
import json
import time

import httpx
import pytest
import respx

from tests.conftest import auth_url, data_url
from vaifstudio import Session, SignInResult, VaifAuthError, VaifClient

USER = {"id": "u1", "email": "ada@example.com", "phone": None, "provider": "email", "metadata": {}}


def login_response(
    token: str = "at_1", refresh: str = "rt_1", expires_in: int = 900
) -> httpx.Response:
    return httpx.Response(
        200,
        json={"ok": True, "accessToken": token, "expiresIn": expires_in, "user": USER},
        headers={
            "set-cookie": f"project_refresh_token={refresh}; Max-Age=2592000; Path=/projects/proj_123/auth; HttpOnly; SameSite=Lax"
        },
    )


@respx.mock
async def test_sign_in_stores_session_and_refresh_cookie(client: VaifClient) -> None:
    route = respx.post(auth_url("login")).mock(return_value=login_response())
    events: list[str] = []
    client.auth.on_session_change(lambda event, _s: events.append(event))

    result = await client.auth.sign_in("ada@example.com", "pw")

    assert json.loads(route.calls.last.request.content) == {
        "email": "ada@example.com",
        "password": "pw",
    }
    assert result.session is not None and not result.mfa_required
    session = client.auth.session
    assert session is not None
    assert session.access_token == "at_1"
    assert session.refresh_token == "rt_1"
    assert session.user is not None and session.user.email == "ada@example.com"
    assert 890 < session.expires_in <= 900
    assert events == ["SIGNED_IN"]


@respx.mock
async def test_signed_in_requests_carry_bearer(client: VaifClient) -> None:
    respx.post(auth_url("login")).mock(return_value=login_response())
    route = respx.get(data_url("todos")).mock(
        return_value=httpx.Response(200, json={"data": [], "count": 0})
    )
    await client.auth.sign_in("ada@example.com", "pw")
    await client.from_("todos").list()
    assert route.calls.last.request.headers["authorization"] == "Bearer at_1"


@respx.mock
async def test_sign_in_with_mfa_then_verify(client: VaifClient) -> None:
    respx.post(auth_url("login")).mock(
        return_value=httpx.Response(
            200, json={"ok": True, "mfaRequired": True, "challengeToken": "ch_1"}
        )
    )
    verify = respx.post(auth_url("mfa/verify")).mock(return_value=login_response("at_mfa"))

    result = await client.auth.sign_in("ada@example.com", "pw")
    assert result.mfa_required and result.challenge_token == "ch_1"
    assert client.auth.session is None

    session = await client.auth.verify_mfa("ch_1", "123456")
    assert json.loads(verify.calls.last.request.content) == {
        "challengeToken": "ch_1",
        "code": "123456",
    }
    assert session.access_token == "at_mfa"
    assert client.auth.session == session


@respx.mock
async def test_bad_credentials_raise_auth_error(client: VaifClient) -> None:
    respx.post(auth_url("login")).mock(
        return_value=httpx.Response(
            401, json={"error": "INVALID_CREDENTIALS", "message": "Invalid email or password"}
        )
    )
    with pytest.raises(VaifAuthError) as info:
        await client.auth.sign_in("ada@example.com", "bad")
    assert info.value.code == "INVALID_CREDENTIALS"
    assert client.auth.session is None


@respx.mock
async def test_sign_up_with_session_and_pending_verification(client: VaifClient) -> None:
    route = respx.post(auth_url("signup")).mock(
        side_effect=[
            login_response("at_new"),
            httpx.Response(
                201, json={"ok": True, "pendingVerification": True, "message": "Check your email"}
            ),
        ]
    )
    created = await client.auth.sign_up("new@example.com", "pw", metadata={"plan": "free"})
    assert created.session is not None and created.session.access_token == "at_new"
    assert json.loads(route.calls[0].request.content)["metadata"] == {"plan": "free"}

    respx.post(auth_url("logout")).mock(return_value=httpx.Response(200, json={"ok": True}))
    await client.auth.sign_out()
    pending = await client.auth.sign_up("taken@example.com", "pw")
    assert pending.session is None and pending.pending_verification
    assert pending.message == "Check your email"


@respx.mock
async def test_refresh_is_single_flight_and_rotates(client: VaifClient) -> None:
    respx.post(auth_url("login")).mock(return_value=login_response())
    refresh = respx.post(auth_url("refresh")).mock(
        side_effect=lambda request: login_response("at_2", "rt_2")
    )
    await client.auth.sign_in("ada@example.com", "pw")
    events: list[str] = []
    client.auth.on_session_change(lambda event, _s: events.append(event))

    sessions = await asyncio.gather(*(client.auth.refresh_session() for _ in range(10)))

    assert events == ["TOKEN_REFRESHED"]
    assert refresh.call_count == 1
    assert refresh.calls.last.request.headers["cookie"] == "project_refresh_token=rt_1"
    assert {s.access_token for s in sessions} == {"at_2"}
    assert client.auth.session is not None
    assert client.auth.session.refresh_token == "rt_2"

    await client.auth.refresh_session()
    assert refresh.calls.last.request.headers["cookie"] == "project_refresh_token=rt_2"


@respx.mock
async def test_expiring_session_refreshes_before_request(client: VaifClient) -> None:
    refresh = respx.post(auth_url("refresh")).mock(return_value=login_response("at_fresh"))
    route = respx.get(data_url("todos")).mock(
        return_value=httpx.Response(200, json={"data": [], "count": 0})
    )
    client.auth.set_session("at_old", "rt_old", expires_at=time.time() + 5)

    await asyncio.gather(client.from_("todos").list(), client.from_("todos").list())

    assert refresh.call_count == 1
    assert all(c.request.headers["authorization"] == "Bearer at_fresh" for c in route.calls)


@respx.mock
async def test_401_triggers_one_refresh_and_one_retry(client: VaifClient) -> None:
    respx.post(auth_url("refresh")).mock(return_value=login_response("at_new"))
    route = respx.get(auth_url("me")).mock(
        side_effect=[
            httpx.Response(
                401, json={"error": "UNAUTHORIZED", "message": "Invalid or expired token"}
            ),
            httpx.Response(200, json={"user": USER}),
        ]
    )
    client.auth.set_session("at_revoked", "rt_1")
    user = await client.auth.get_user()
    assert user.id == "u1"
    assert [c.request.headers["authorization"] for c in route.calls] == [
        "Bearer at_revoked",
        "Bearer at_new",
    ]


@respx.mock
async def test_failed_refresh_signs_out(client: VaifClient) -> None:
    respx.post(auth_url("refresh")).mock(
        return_value=httpx.Response(
            401, json={"error": "UNAUTHORIZED", "message": "Invalid or expired refresh token"}
        )
    )
    events: list[str] = []
    client.auth.set_session("at", "rt_dead", expires_at=time.time() - 1)
    client.auth.on_session_change(lambda event, _s: events.append(event))
    with pytest.raises(VaifAuthError):
        await client.from_("todos").list()
    assert client.auth.session is None
    assert events == ["SIGNED_OUT"]


class HeldResponse:
    """A route whose first request is answered only when the test releases it.

    Later requests are answered with ``then`` at once. ``requests`` lists every
    request in the order it arrived, including one still being held.
    """

    def __init__(self, response: httpx.Response, then: httpx.Response | None = None) -> None:
        self.arrived = asyncio.Event()
        self.release = asyncio.Event()
        self.response = response
        self.then = then
        self.requests: list[httpx.Request] = []

    async def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if len(self.requests) > 1 and self.then is not None:
            return self.then
        self.arrived.set()
        await self.release.wait()
        return self.response


@respx.mock
async def test_refresh_finishing_after_sign_out_does_not_restore_the_session(
    client: VaifClient,
) -> None:
    held = HeldResponse(login_response("at_2", "rt_2"))
    respx.post(auth_url("refresh")).mock(side_effect=held)
    respx.post(auth_url("logout")).mock(return_value=httpx.Response(200, json={"ok": True}))
    client.auth.set_session("at_1", "rt_1")
    events: list[str] = []
    client.auth.on_session_change(lambda event, _s: events.append(event))

    refreshing = asyncio.ensure_future(client.auth.refresh_session())
    await held.arrived.wait()
    await client.auth.sign_out()
    held.release.set()

    with pytest.raises(VaifAuthError) as info:
        await refreshing
    assert info.value.code == "NOT_SIGNED_IN"
    assert client.auth.session is None
    assert events == ["SIGNED_OUT"]


@pytest.mark.parametrize("revoke_status", [200, 503])
@respx.mock
async def test_refresh_finishing_after_sign_out_revokes_the_rotated_token(
    client: VaifClient, revoke_status: int
) -> None:
    # sign_out() names rt_1. If the rotation reached the server first, rt_1 no
    # longer identifies a session, so the rotated rt_2 is revoked as well. A
    # failure of that second request does not change what the refresh raises.
    held = HeldResponse(login_response("at_2", "rt_2"))
    respx.post(auth_url("refresh")).mock(side_effect=held)
    logout = respx.post(auth_url("logout")).mock(
        side_effect=[
            httpx.Response(200, json={"ok": True}),
            httpx.Response(revoke_status, json={"ok": revoke_status == 200}),
        ]
    )
    client.auth.set_session("at_1", "rt_1", expires_at=time.time() - 60)

    refreshing = asyncio.ensure_future(client.auth.refresh_session())
    await held.arrived.wait()
    await client.auth.sign_out()
    held.release.set()

    with pytest.raises(VaifAuthError) as info:
        await refreshing
    assert info.value.code == "NOT_SIGNED_IN"
    assert logout.call_count == 2
    first, second = (call.request for call in logout.calls)
    assert json.loads(first.content) == {"refreshToken": "rt_1"}
    assert json.loads(second.content) == {"refreshToken": "rt_2"}
    assert "authorization" not in second.headers
    assert client.auth.session is None


@respx.mock
async def test_refresh_finishing_after_set_session_keeps_the_newer_session(
    client: VaifClient,
) -> None:
    held = HeldResponse(login_response("at_2", "rt_2"))
    respx.post(auth_url("refresh")).mock(side_effect=held)
    client.auth.set_session("at_1", "rt_1")
    events: list[str] = []
    client.auth.on_session_change(lambda event, _s: events.append(event))

    refreshing = asyncio.ensure_future(client.auth.refresh_session())
    await held.arrived.wait()
    client.auth.set_session("at_other", "rt_other")
    held.release.set()

    session = await refreshing
    assert session.access_token == "at_other"
    assert client.auth.session is not None
    assert client.auth.session.access_token == "at_other"
    assert client.auth.session.refresh_token == "rt_other"
    assert events == ["SIGNED_IN"]


UNAUTHORIZED = {"error": "UNAUTHORIZED", "message": "Invalid or expired token"}


@respx.mock
async def test_a_401_after_the_user_changed_is_not_sent_again_with_the_new_users_token(
    client: VaifClient,
) -> None:
    # An insert sent as user A is refused with 401 after A signed out and B
    # signed in. Sent again with B's token, the row would be written as B.
    held = HeldResponse(httpx.Response(401, json=UNAUTHORIZED))
    insert = respx.post(data_url("todos")).mock(side_effect=held)
    held.then = httpx.Response(201, json={"data": {"id": "row_b"}})
    refresh = respx.post(auth_url("refresh")).mock(return_value=login_response("at_a2", "rt_a2"))
    respx.post(auth_url("logout")).mock(return_value=httpx.Response(200, json={"ok": True}))
    client.auth.set_session("at_a", "rt_a")

    inserting = asyncio.ensure_future(client.from_("todos").insert({"title": "from A"}))
    await held.arrived.wait()
    await client.auth.sign_out()
    client.auth.set_session("at_b", "rt_b")
    held.release.set()

    with pytest.raises(VaifAuthError) as info:
        await inserting
    assert info.value.status == 401
    assert [c.request.headers["authorization"] for c in insert.calls] == ["Bearer at_a"]
    assert refresh.call_count == 0
    assert client.auth.session is not None
    assert client.auth.session.access_token == "at_b"


@respx.mock
async def test_a_401_retry_is_not_sent_with_a_session_set_during_its_refresh(
    client: VaifClient,
) -> None:
    # The refresh for user A's retry is still running when B's session is set.
    # The retry must not go out with B's token.
    held = HeldResponse(login_response("at_a2", "rt_a2"))
    respx.post(auth_url("refresh")).mock(side_effect=held)
    me = respx.get(auth_url("me")).mock(
        side_effect=[
            httpx.Response(401, json=UNAUTHORIZED),
            httpx.Response(200, json={"user": USER}),
        ]
    )
    client.auth.set_session("at_a", "rt_a")

    getting = asyncio.ensure_future(client.auth.get_user())
    await held.arrived.wait()
    client.auth.set_session("at_b", "rt_b")
    held.release.set()

    with pytest.raises(VaifAuthError) as info:
        await getting
    assert info.value.status == 401
    assert [c.request.headers["authorization"] for c in me.calls] == ["Bearer at_a"]
    assert client.auth.session is not None
    assert client.auth.session.access_token == "at_b"
    assert client.auth.session.refresh_token == "rt_b"


@respx.mock
async def test_a_refresh_of_a_new_session_does_not_wait_on_the_previous_sessions_refresh(
    client: VaifClient,
) -> None:
    held = HeldResponse(login_response("at_a2", "rt_a2"), then=login_response("at_b2", "rt_b2"))
    respx.post(auth_url("refresh")).mock(side_effect=held)
    client.auth.set_session("at_a", "rt_a")

    first = asyncio.ensure_future(client.auth.refresh_session())
    await held.arrived.wait()
    client.auth.set_session("at_b", "rt_b")
    second = await asyncio.wait_for(client.auth.refresh_session(), 2.0)

    assert second.access_token == "at_b2"
    assert [request.headers["cookie"] for request in held.requests] == [
        "project_refresh_token=rt_a",
        "project_refresh_token=rt_b",
    ]
    held.release.set()
    await first
    assert client.auth.session is not None
    assert client.auth.session.access_token == "at_b2"
    assert client.auth.session.refresh_token == "rt_b2"


@respx.mock
async def test_a_request_is_not_sent_as_the_user_who_replaced_it_during_its_refresh(
    client: VaifClient,
) -> None:
    # User A's token is about to expire, so the insert waits on a refresh. A
    # signs out and B signs in while it waits. Sent with B's token, the row
    # would be written as B.
    held = HeldResponse(login_response("at_a2", "rt_a2"))
    refresh = respx.post(auth_url("refresh")).mock(side_effect=held)
    insert = respx.post(data_url("todos")).mock(
        return_value=httpx.Response(201, json={"data": {"id": "row_b"}})
    )
    respx.post(auth_url("logout")).mock(return_value=httpx.Response(200, json={"ok": True}))
    client.auth.set_session("at_a", "rt_a", expires_at=time.time() + 5)

    inserting = asyncio.ensure_future(client.from_("todos").insert({"title": "from A"}))
    await held.arrived.wait()
    await client.auth.sign_out()
    client.auth.set_session("at_b", "rt_b")
    held.release.set()

    with pytest.raises(VaifAuthError) as info:
        await inserting
    assert info.value.code == "NOT_SIGNED_IN"
    assert refresh.call_count == 1
    assert insert.call_count == 0
    assert client.auth.session is not None
    assert client.auth.session.access_token == "at_b"
    assert client.auth.session.refresh_token == "rt_b"


@respx.mock
async def test_a_request_that_waited_on_its_own_sessions_refresh_is_sent_with_the_new_token(
    client: VaifClient,
) -> None:
    # The same user's rotation during the wait is not a change of user.
    refresh = respx.post(auth_url("refresh")).mock(return_value=login_response("at_a2", "rt_a2"))
    insert = respx.post(data_url("todos")).mock(
        return_value=httpx.Response(201, json={"data": {"id": "row_a"}})
    )
    client.auth.set_session("at_a", "rt_a", expires_at=time.time() + 5)

    row = await client.from_("todos").insert({"title": "from A"})

    assert row == {"id": "row_a"}
    assert refresh.call_count == 1
    assert [c.request.headers["authorization"] for c in insert.calls] == ["Bearer at_a2"]


async def test_refresh_without_token_fails_fast(client: VaifClient) -> None:
    client.auth.set_session("at_only")
    with pytest.raises(VaifAuthError) as info:
        await client.auth.refresh_session()
    assert info.value.code == "NO_REFRESH_TOKEN"


@respx.mock
async def test_sign_out_sends_the_refresh_token_and_clears_the_session(client: VaifClient) -> None:
    # The API answers 200 whether or not it found a session to revoke. It
    # finds one by a valid access token or, once that has expired, by the
    # refresh token in the body.
    logout = respx.post(auth_url("logout")).mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    client.auth.set_session("at_1", "rt_1")
    await client.auth.sign_out()
    request = logout.calls.last.request
    assert request.headers["authorization"] == "Bearer at_1"
    assert json.loads(request.content) == {"refreshToken": "rt_1"}
    assert client.auth.session is None

    client.auth.set_session("at_expired", "rt_2", expires_at=time.time() - 60)
    await client.auth.sign_out()
    assert json.loads(logout.calls.last.request.content) == {"refreshToken": "rt_2"}
    assert client.auth.session is None

    client.auth.set_session("at_only")
    await client.auth.sign_out()
    assert logout.calls.last.request.content == b""

    await client.auth.sign_out()  # no session: no request
    assert logout.call_count == 3


async def test_get_user_requires_session(client: VaifClient) -> None:
    with pytest.raises(VaifAuthError) as info:
        await client.auth.get_user()
    assert info.value.code == "NOT_SIGNED_IN"


@respx.mock
async def test_password_reset_calls(client: VaifClient) -> None:
    forgot = respx.post(auth_url("forgot-password")).mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    reset = respx.post(auth_url("reset-password")).mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    await client.auth.request_password_reset("ada@example.com")
    await client.auth.reset_password("tok", "new-pw")
    assert json.loads(forgot.calls.last.request.content) == {"email": "ada@example.com"}
    assert json.loads(reset.calls.last.request.content) == {"token": "tok", "password": "new-pw"}


def test_restored_session_round_trip(client: VaifClient) -> None:
    restored = client.auth.set_session("at_secret", "rt_secret", expires_at=123.0)
    assert restored == Session(
        access_token="at_secret", expires_at=123.0, refresh_token="rt_secret"
    )


def test_session_repr_keeps_both_tokens_out_of_logs() -> None:
    session = Session(access_token="at_secret", expires_at=123.0, refresh_token="rt_secret")
    assert repr(session) == "Session(expires_at=123.0, user=None)"
    assert repr(SignInResult(session=session)) == (
        "SignInResult(session=Session(expires_at=123.0, user=None), mfa_required=False)"
    )


@respx.mock
async def test_sign_out_raises_when_a_listener_cannot_clear_the_saved_session(
    client: VaifClient,
) -> None:
    from vaifstudio import VaifError

    failure = OSError("keychain is locked")
    logout = respx.post(auth_url("logout")).mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    client.auth.set_session("at_1", "rt_1")

    def listener(event: str, _session: object) -> None:
        if event == "SIGNED_OUT":
            raise failure

    client.auth.on_session_change(listener)
    with pytest.raises(VaifError) as info:
        await client.auth.sign_out()
    assert info.value.code == "SESSION_STORAGE_FAILED"
    assert info.value.message == (
        "Signed out, but a session listener failed while clearing the saved session, "
        "so it may be restored on the next start"
    )
    assert info.value.__cause__ is failure
    assert logout.call_count == 1
    assert client.auth.session is None


@respx.mock
async def test_sign_out_reports_the_listener_failure_when_the_server_is_unreachable(
    client: VaifClient,
) -> None:
    from vaifstudio import VaifError

    respx.post(auth_url("logout")).mock(side_effect=httpx.ConnectError("offline"))
    client.auth.set_session("at_1", "rt_1")

    def listener(_event: str, _session: object) -> None:
        raise OSError("keychain is locked")

    client.auth.on_session_change(listener)
    with pytest.raises(VaifError) as info:
        await client.auth.sign_out()
    assert info.value.code == "SESSION_STORAGE_FAILED"
    assert type(info.value.__context__).__name__ == "VaifNetworkError"


async def test_a_client_passed_in_keeps_no_refresh_cookie_between_users() -> None:
    # One httpx client shared by the VaifClients of two end users: the API's
    # refresh cookie for the first user must not travel on the second's calls.
    requests: list[httpx.Request] = []

    def api(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.path.endswith("/login"):
            return login_response("at_ada", "rt_ada")
        return httpx.Response(200, json={"ok": True})

    async with httpx.AsyncClient(transport=httpx.MockTransport(api)) as shared:
        ada = VaifClient(
            "proj_123", "vk_pub_test", base_url="https://api.test.vaif", http_client=shared
        )
        bob = VaifClient(
            "proj_123", "vk_pub_test", base_url="https://api.test.vaif", http_client=shared
        )
        shared.cookies.set("app_preference", "dark", domain="api.test.vaif")
        await ada.auth.sign_in("ada@example.com", "pw")
        assert [c.name for c in shared.cookies.jar] == ["app_preference"]

        bob.auth.set_session("at_bob", "rt_bob", expires_at=time.time() - 60)
        await bob.auth.sign_out()

    logout = requests[-1]
    assert logout.url.path == "/projects/proj_123/auth/logout"
    assert logout.headers["cookie"] == "app_preference=dark"
    assert json.loads(logout.content) == {"refreshToken": "rt_bob"}
