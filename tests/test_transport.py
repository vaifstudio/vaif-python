from __future__ import annotations

import httpx
import pytest
import respx

from tests.conftest import BASE, FAST_RETRY, KEY, PROJECT, data_url
from vaifstudio import (
    NO_RETRY,
    VaifAuthError,
    VaifClient,
    VaifConflictError,
    VaifError,
    VaifNetworkError,
    VaifNotFoundError,
    VaifRateLimitError,
    VaifServerError,
    VaifTimeoutError,
    VaifValidationError,
    __version__,
)
from vaifstudio.retry import RetryPolicy


def test_rejects_plain_http_for_remote_hosts() -> None:
    with pytest.raises(ValueError, match="https"):
        VaifClient(PROJECT, KEY, base_url="http://api.vaif.studio")


def test_allows_http_for_localhost_and_strips_slash() -> None:
    c = VaifClient(PROJECT, KEY, base_url="http://localhost:3000/")
    assert c.base_url == "http://localhost:3000"


# Plain http would send the project key and bearer token in cleartext.
@pytest.mark.parametrize(
    ("base_url", "normalized"),
    [
        ("https://api.example.com/", "https://api.example.com"),
        ("HTTPS://api.example.com", "HTTPS://api.example.com"),
        ("http://localhost:3000", "http://localhost:3000"),
        ("http://127.0.0.1:3000", "http://127.0.0.1:3000"),
        ("http://[::1]:3000", "http://[::1]:3000"),
    ],
)
def test_base_url_accepts_https_and_loopback_http(base_url: str, normalized: str) -> None:
    assert VaifClient(PROJECT, KEY, base_url=base_url).base_url == normalized


@pytest.mark.parametrize(
    "base_url",
    ["http://api.example.com", "HTTP://api.example.com", "http://localhost.example.com"],
)
def test_base_url_refuses_http_for_other_hosts(base_url: str) -> None:
    with pytest.raises(ValueError) as caught:
        VaifClient(PROJECT, KEY, base_url=base_url)
    assert str(caught.value) == (
        "base_url must use https (http is accepted only for localhost, 127.0.0.1 and ::1)"
    )


def test_requires_project_and_key() -> None:
    with pytest.raises(ValueError):
        VaifClient("", KEY)
    with pytest.raises(ValueError):
        VaifClient(PROJECT, "")


@respx.mock
async def test_sends_key_version_and_user_agent(client: VaifClient) -> None:
    route = respx.get(data_url("todos")).mock(
        return_value=httpx.Response(200, json={"data": [], "count": 0})
    )
    await client.from_("todos").list()
    request = route.calls.last.request
    assert request.headers["x-vaif-key"] == KEY
    assert request.headers["accept-versions"] == "v1"
    assert request.headers["user-agent"] == f"vaif-python/{__version__}"
    assert "authorization" not in request.headers


@pytest.mark.parametrize(
    ("status", "body", "error_type", "code"),
    [
        (
            400,
            {"error": "BadRequest", "code": "INVALID_COLUMN", "message": "no col"},
            VaifValidationError,
            "INVALID_COLUMN",
        ),
        (
            401,
            {"error": "INVALID_CREDENTIALS", "message": "bad"},
            VaifAuthError,
            "INVALID_CREDENTIALS",
        ),
        (403, {"error": "FORBIDDEN", "message": "nope"}, VaifAuthError, "FORBIDDEN"),
        (
            404,
            {"error": "NOT_FOUND", "message": "Record not found"},
            VaifNotFoundError,
            "NOT_FOUND",
        ),
        (409, {"error": "CONFLICT", "message": "dupe"}, VaifConflictError, "CONFLICT"),
        (422, {"message": "bad entity"}, VaifValidationError, None),
        (402, {"error": "PAYMENT_REQUIRED", "message": "upgrade"}, VaifError, "PAYMENT_REQUIRED"),
    ],
)
@respx.mock
async def test_maps_status_codes_to_typed_errors(
    client: VaifClient, status: int, body: dict, error_type: type, code: str | None
) -> None:
    respx.get(data_url("todos")).mock(
        return_value=httpx.Response(status, json={**body, "requestId": "req_1"})
    )
    with pytest.raises(error_type) as info:
        await client.from_("todos").list()
    assert info.value.status == status
    assert info.value.code == code
    assert info.value.request_id == "req_1"
    assert info.value.message == body["message"]


@respx.mock
async def test_retries_get_on_503_then_succeeds(client: VaifClient) -> None:
    route = respx.get(data_url("todos")).mock(
        side_effect=[
            httpx.Response(503, json={"error": "Unavailable"}),
            httpx.Response(502),
            httpx.Response(200, json={"data": [{"id": 1}], "count": 1}),
        ]
    )
    result = await client.from_("todos").list()
    assert route.call_count == 3
    assert result.count == 1


@respx.mock
async def test_retry_budget_is_bounded(client: VaifClient) -> None:
    route = respx.get(data_url("todos")).mock(return_value=httpx.Response(500))
    with pytest.raises(VaifServerError):
        await client.from_("todos").list()
    assert route.call_count == FAST_RETRY.max_retries + 1


@respx.mock
async def test_does_not_replay_post_on_5xx(client: VaifClient) -> None:
    route = respx.post(data_url("todos")).mock(return_value=httpx.Response(503))
    with pytest.raises(VaifServerError):
        await client.from_("todos").insert({"title": "x"})
    assert route.call_count == 1


@respx.mock
async def test_does_not_replay_post_on_read_timeout(client: VaifClient) -> None:
    route = respx.post(data_url("todos")).mock(side_effect=httpx.ReadTimeout("slow"))
    with pytest.raises(VaifTimeoutError):
        await client.from_("todos").insert({"title": "x"})
    assert route.call_count == 1


@respx.mock
async def test_retries_any_method_when_connection_never_opened(client: VaifClient) -> None:
    route = respx.post(data_url("todos")).mock(
        side_effect=[
            httpx.ConnectError("refused"),
            httpx.Response(200, json={"data": {"id": 7}}),
        ]
    )
    row = await client.from_("todos").insert({"title": "x"})
    assert row == {"id": 7}
    assert route.call_count == 2


@respx.mock
async def test_get_read_timeout_is_retried_then_raised(client: VaifClient) -> None:
    route = respx.get(data_url("todos")).mock(side_effect=httpx.ReadTimeout("slow"))
    with pytest.raises(VaifTimeoutError):
        await client.from_("todos").list()
    assert route.call_count == 4


@respx.mock
async def test_network_error_is_typed() -> None:
    c = VaifClient(PROJECT, KEY, base_url=BASE, retry=NO_RETRY)
    respx.get(data_url("todos")).mock(side_effect=httpx.ConnectError("dns"))
    with pytest.raises(VaifNetworkError):
        await c.from_("todos").list()
    await c.close()


@respx.mock
async def test_rate_limit_honors_retry_after_and_exposes_it() -> None:
    policy = RetryPolicy(max_retries=1, base_delay=0.0, max_delay=0.0)
    c = VaifClient(PROJECT, KEY, base_url=BASE, retry=policy)
    route = respx.get(data_url("todos")).mock(
        return_value=httpx.Response(
            429, headers={"Retry-After": "7"}, json={"error": "RateLimited"}
        )
    )
    with pytest.raises(VaifRateLimitError) as info:
        await c.from_("todos").list()
    assert info.value.retry_after == 7.0
    assert route.call_count == 2
    await c.close()


def test_retry_delay_is_exponential_capped_and_prefers_retry_after() -> None:
    policy = RetryPolicy(base_delay=1.0, max_delay=5.0, multiplier=2.0)
    assert 1.0 <= policy.delay_for(0) <= 1.25
    assert 4.0 <= policy.delay_for(2) <= 5.0
    assert 5.0 <= policy.delay_for(10) <= 6.25
    assert policy.delay_for(0, retry_after=3.0) == 3.0
    assert policy.delay_for(0, retry_after=60.0) == 5.0


@respx.mock
async def test_custom_headers_and_injected_client() -> None:
    async with httpx.AsyncClient() as http:
        c = VaifClient(PROJECT, KEY, base_url=BASE, http_client=http, headers={"X-App": "demo"})
        route = respx.get(data_url("todos")).mock(
            return_value=httpx.Response(200, json={"data": [], "count": 0})
        )
        await c.from_("todos").list()
        assert route.calls.last.request.headers["x-app"] == "demo"
        await c.close()
        assert not http.is_closed  # caller owns the injected client


async def test_context_manager_closes() -> None:
    async with VaifClient(PROJECT, KEY, base_url=BASE) as c:
        assert c.project_id == PROJECT


@pytest.mark.parametrize("follow_redirects", [False, True])
async def test_api_redirects_are_not_followed_so_credentials_stay_on_the_api_origin(
    follow_redirects: bool,
) -> None:
    # Even a client passed in with follow_redirects=True must not carry the
    # project key or the session token to the redirect's origin.
    requests: list[httpx.Request] = []

    def answer(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        if request.url.host == "api.test.vaif":
            return httpx.Response(307, headers={"Location": "https://elsewhere.example/collect"})
        return httpx.Response(200, json={"data": [], "count": 0})

    async with httpx.AsyncClient(
        transport=httpx.MockTransport(answer), follow_redirects=follow_redirects
    ) as http:
        c = VaifClient(PROJECT, KEY, base_url=BASE, http_client=http, retry=NO_RETRY)
        c.auth.set_session("at_user")
        with pytest.raises(VaifError) as info:
            await c.from_("todos").list()
        await c.close()

    assert [str(r.url.host) for r in requests] == ["api.test.vaif"]
    assert info.value.status == 307
    assert info.value.code == "REDIRECT_NOT_FOLLOWED"
    assert info.value.headers["location"] == "https://elsewhere.example/collect"
    assert info.value.message == (
        "The API answered with a redirect (HTTP 307), which the SDK does not follow"
    )


@respx.mock
async def test_a_redirect_error_keeps_no_signed_query_string(client: VaifClient) -> None:
    # A signed URL's query string and user information are credentials. The
    # error keeps where the redirect pointed, not the signature.
    respx.get(data_url("todos")).mock(
        return_value=httpx.Response(
            307,
            headers={
                "Location": "https://user:pw_secret@files.example/a.txt?X-Amz-Signature=sig_secret#part",
                "X-Request-Id": "req_1",
            },
        )
    )
    with pytest.raises(VaifError) as info:
        await client.from_("todos").list()
    assert info.value.code == "REDIRECT_NOT_FOLLOWED"
    assert info.value.headers["location"] == "https://files.example/a.txt"
    assert info.value.headers["x-request-id"] == "req_1"
    shown = repr(info.value) + str(info.value) + repr(dict(info.value.headers))
    assert "sig_secret" not in shown
    assert "pw_secret" not in shown


@respx.mock
async def test_a_response_that_cannot_be_decoded_raises_a_network_error(
    client: VaifClient,
) -> None:
    # httpx raises DecodingError (a RequestError, not a TransportError) for a
    # body whose Content-Encoding does not match it.
    respx.get(data_url("todos")).mock(
        return_value=httpx.Response(
            200,
            headers={"Content-Encoding": "gzip"},
            stream=httpx.ByteStream(b"not gzip"),
        )
    )
    with pytest.raises(VaifNetworkError) as info:
        await client.from_("todos").list()
    assert info.value.message == "Could not read the API response: DecodingError"
    assert isinstance(info.value.__cause__, httpx.DecodingError)
