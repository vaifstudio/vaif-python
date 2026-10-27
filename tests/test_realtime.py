from __future__ import annotations

import asyncio
import json
import time
from unittest.mock import patch

import httpx
import pytest
import respx

from tests.conftest import auth_url
from tests.test_auth import HeldResponse, login_response
from vaifstudio import VaifAuthError, VaifClient, VaifError, VaifNetworkError, VaifTimeoutError


class FakeSocket:
    def __init__(self, frames: list[dict | str]) -> None:
        self.frames: asyncio.Queue[str] = asyncio.Queue()
        for frame in frames:
            self.frames.put_nowait(frame if isinstance(frame, str) else json.dumps(frame))
        self.sent: list[dict] = []
        self.closed = False

    async def send(self, frame: str) -> None:
        self.sent.append(json.loads(frame))

    async def recv(self) -> str:
        return await self.frames.get()

    async def close(self) -> None:
        self.closed = True


async def test_authenticated_subscription_waits_for_ack_and_filters_events(
    client: VaifClient,
) -> None:
    socket = FakeSocket(
        [
            {"type": "welcome", "heartbeatIntervalMs": 30000},
            {"type": "subscribed", "channel": "table:todos"},
            "bad json",
            {"type": "db_change", "table": "other", "op": "INSERT"},
            {"type": "db_change", "table": "todos", "op": "DELETE"},
            {"type": "db_change", "table": "todos", "op": "INSERT", "record": {"id": "one"}},
        ]
    )

    async def connect(url: str, **kwargs):
        assert url == "wss://api.test.vaif/realtime/ws"
        assert kwargs["proxy"] is None  # credentials must not pass through environment proxies
        return socket

    client.auth.set_session("user-token")
    with patch("vaifstudio.realtime.connect", connect):
        async with client.realtime.subscribe("todos", event="INSERT") as subscription:
            result = await asyncio.wait_for(anext(subscription), 1)
            assert result["record"]["id"] == "one"
            assert socket.sent[:2] == [
                {"type": "auth", "apiKey": "vk_pub_test", "accessToken": "user-token"},
                {"type": "subscribe", "channel": "table:todos"},
            ]
    assert socket.sent[-1] == {"type": "unsubscribe", "channel": "table:todos"}
    assert socket.closed


@pytest.mark.parametrize(
    "frames,error_type,code",
    [
        (
            [{"type": "welcome"}, {"type": "error", "code": "FORBIDDEN", "message": "Denied"}],
            VaifError,
            "FORBIDDEN",
        ),
        (
            [{"type": "welcome"}, {"type": "subscribed", "channel": "table:unrelated"}],
            VaifTimeoutError,
            "REALTIME_CLOSED",
        ),
        ([], VaifTimeoutError, "REALTIME_CLOSED"),
    ],
)
async def test_refusal_or_missing_ack_closes_connection(
    client: VaifClient, frames: list[dict], error_type: type[VaifError], code: str
) -> None:
    socket = FakeSocket(frames)

    async def connect(*args, **kwargs):
        return socket

    with patch("vaifstudio.realtime.connect", connect), pytest.raises(error_type) as caught:
        async with client.realtime.subscribe("todos", timeout=0.01):
            pytest.fail("Must wait for the correct subscribed acknowledgment")
    assert caught.value.code == code
    assert socket.closed


def _refused_handshake() -> Exception:
    from websockets.datastructures import Headers
    from websockets.exceptions import InvalidStatus
    from websockets.http11 import Response

    return InvalidStatus(Response(403, "Forbidden", Headers()))


@pytest.mark.parametrize(
    "failure,error_type,status,message",
    [
        (
            ConnectionRefusedError(61, "Connect call failed"),
            VaifNetworkError,
            None,
            "Could not open the realtime connection: ConnectionRefusedError",
        ),
        (
            TimeoutError(),
            VaifTimeoutError,
            None,
            "Timed out opening the realtime subscription (timeout: 15.0 seconds)",
        ),
        (
            _refused_handshake(),
            VaifNetworkError,
            403,
            "The realtime handshake was refused with HTTP 403",
        ),
    ],
)
async def test_a_connection_that_cannot_open_raises_a_typed_error(
    client: VaifClient,
    failure: Exception,
    error_type: type[VaifError],
    status: int | None,
    message: str,
) -> None:
    async def connect(*args, **kwargs):
        raise failure

    with patch("vaifstudio.realtime.connect", connect), pytest.raises(VaifError) as caught:
        async with client.realtime.subscribe("todos"):
            pytest.fail("A connection that did not open must not enter")
    assert type(caught.value) is error_type
    assert caught.value.code == "REALTIME_CLOSED"
    assert caught.value.status == status
    assert caught.value.message == message
    assert caught.value.__cause__ is failure
    assert client.realtime._subscriptions == set()


async def test_a_refused_tcp_connection_raises_a_network_error() -> None:
    import socket as sockets

    # A port that was free a moment ago: nothing listens on it.
    with sockets.socket() as probe:
        probe.bind(("127.0.0.1", 0))
        port = probe.getsockname()[1]
    async with VaifClient("proj_123", "vk_pub_test", base_url=f"http://127.0.0.1:{port}") as c:
        with pytest.raises(VaifNetworkError) as caught:
            async with c.realtime.subscribe("todos", timeout=5):
                pytest.fail("Nothing listens on the port")
    assert caught.value.code == "REALTIME_CLOSED"
    assert caught.value.message.startswith("Could not open the realtime connection: ")


async def test_a_handshake_that_never_finishes_raises_a_timeout_error() -> None:
    # A real server that accepts the TCP connection and never answers the
    # WebSocket upgrade, so the websockets library's own open timeout fires.
    held: list[asyncio.StreamWriter] = []

    async def accept(_reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        held.append(writer)

    server = await asyncio.start_server(accept, "127.0.0.1", 0)
    port = server.sockets[0].getsockname()[1]
    try:
        async with VaifClient("proj_123", "vk_pub_test", base_url=f"http://127.0.0.1:{port}") as c:
            with pytest.raises(VaifTimeoutError) as caught:
                async with c.realtime.subscribe("todos", timeout=0.2):
                    pytest.fail("The handshake never finished")
    finally:
        for writer in held:
            writer.close()
        server.close()
        await server.wait_closed()
    assert caught.value.code == "REALTIME_CLOSED"
    assert (
        caught.value.message == "Timed out opening the realtime subscription (timeout: 0.2 seconds)"
    )


async def test_a_socket_closed_before_the_first_frame_raises_a_typed_error(
    client: VaifClient,
) -> None:
    from websockets.exceptions import ConnectionClosedError
    from websockets.frames import Close

    class ClosedOnSend(FakeSocket):
        async def send(self, frame: str) -> None:
            raise ConnectionClosedError(Close(1011, "server restart"), None)

    socket = ClosedOnSend([])

    async def connect(*args, **kwargs):
        return socket

    with patch("vaifstudio.realtime.connect", connect), pytest.raises(VaifNetworkError) as caught:
        async with client.realtime.subscribe("todos"):
            pytest.fail("A closed socket must not enter")
    assert caught.value.code == "REALTIME_CLOSED"
    assert caught.value.status == 1011
    assert socket.closed


async def test_client_close_closes_subscriptions(client: VaifClient) -> None:
    socket = FakeSocket([{"type": "welcome"}, {"type": "subscribed", "channel": "table:todos"}])

    async def connect(*args, **kwargs):
        return socket

    with patch("vaifstudio.realtime.connect", connect):
        await client.realtime.subscribe("todos").__aenter__()
        await client.close()
    assert socket.closed


@respx.mock
async def test_heartbeat_refreshes_auth_and_pings(client: VaifClient) -> None:
    refresh = respx.post(auth_url("refresh")).mock(return_value=login_response("new", "rt_new"))
    socket = FakeSocket(
        [
            {"type": "welcome", "heartbeatIntervalMs": 10},
            {"type": "subscribed", "channel": "table:todos"},
        ]
    )

    async def connect(*args, **kwargs):
        return socket

    client.auth.set_session("old", "rt_old")
    with patch("vaifstudio.realtime.connect", connect):
        async with client.realtime.subscribe("todos"):
            # The same session's token rotates; the user does not change.
            await client.auth.refresh_session()

            async def wait_ping():
                while {"type": "ping"} not in socket.sent:
                    await asyncio.sleep(0.001)

            await asyncio.wait_for(wait_ping(), 1)
    assert refresh.call_count == 1
    assert {"type": "auth", "accessToken": "new"} in socket.sent


@pytest.mark.parametrize("table,event", [("bad/name", "*"), ("todos", "WRONG")])
async def test_realtime_invalid_subscription(client: VaifClient, table: str, event: str) -> None:
    with pytest.raises(ValueError):
        client.realtime.subscribe(table, event=event)


async def test_websocket_redirects_are_never_followed() -> None:
    from websockets.datastructures import Headers
    from websockets.exceptions import InvalidStatus
    from websockets.http11 import Response

    from vaifstudio.realtime import _DirectConnect

    refusal = InvalidStatus(
        Response(302, "Found", Headers({"Location": "wss://remote.example/ws"}))
    )
    connection = _DirectConnect("ws://localhost:3147/realtime/ws", proxy=None)
    assert connection.process_redirect(refusal) is refusal


async def test_canceled_handshake_closes_socket(client: VaifClient) -> None:
    socket = FakeSocket([])

    async def connect(*args, **kwargs):
        return socket

    with patch("vaifstudio.realtime.connect", connect):
        task = asyncio.create_task(client.realtime.subscribe("todos").__aenter__())
        while not socket.sent:
            await asyncio.sleep(0)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
    assert socket.closed


class ClosingSocket(FakeSocket):
    """A socket whose peer closes after the queued frames, as a refused server does."""

    def __init__(
        self, frames: list[dict | str], code: int = 4001, reason: str = "UNAUTHORIZED"
    ) -> None:
        super().__init__(frames)
        self.code, self.reason = code, reason

    async def recv(self) -> str:
        if self.frames.empty():
            from websockets.exceptions import ConnectionClosedError
            from websockets.frames import Close

            raise ConnectionClosedError(Close(self.code, self.reason), None)
        return await self.frames.get()


class HeartbeatSocket(ClosingSocket):
    async def close(self) -> None:
        # A real close waits for the closing handshake: the reader wakes
        # before the heartbeat task has finished raising.
        self.closed = True
        for _ in range(20):
            await asyncio.sleep(0)

    async def recv(self) -> str:
        if self.frames.empty():
            # Block until the heartbeat's own close() wakes the reader.
            while not self.closed:
                await asyncio.sleep(0.001)
        return await super().recv()


async def test_error_frame_without_code_keeps_server_error_name(client: VaifClient) -> None:
    # The API's subscribe refusal names the failure in `error`, not `code`:
    # {"type": "error", "error": "InvalidChannel", ...}.
    socket = FakeSocket(
        [
            {"type": "welcome"},
            {
                "type": "error",
                "error": "InvalidChannel",
                "channel": "table:todos",
                "message": "Bad",
            },
        ]
    )

    async def connect(*args, **kwargs):
        return socket

    with patch("vaifstudio.realtime.connect", connect), pytest.raises(VaifError) as caught:
        async with client.realtime.subscribe("todos", timeout=1):
            pytest.fail("A refused subscription must not enter")
    assert caught.value.code == "InvalidChannel"


async def test_connection_loss_is_a_typed_network_error(client: VaifClient) -> None:
    socket = ClosingSocket(
        [{"type": "welcome"}, {"type": "subscribed", "channel": "table:todos"}],
        code=1011,
        reason="server restart",
    )

    async def connect(*args, **kwargs):
        return socket

    with patch("vaifstudio.realtime.connect", connect):
        async with client.realtime.subscribe("todos") as subscription:
            with pytest.raises(VaifNetworkError) as caught:
                await asyncio.wait_for(anext(subscription), 1)
    assert caught.value.code == "REALTIME_CLOSED"
    assert caught.value.status == 1011


async def test_handshake_close_is_a_typed_error(client: VaifClient) -> None:
    socket = ClosingSocket([], code=4001, reason="UNAUTHORIZED")

    async def connect(*args, **kwargs):
        return socket

    with patch("vaifstudio.realtime.connect", connect), pytest.raises(VaifError) as caught:
        async with client.realtime.subscribe("todos", timeout=1):
            pytest.fail("A refused handshake must not enter")
    assert caught.value.code == "UNAUTHORIZED"
    assert socket.closed


async def test_heartbeat_failure_is_raised_instead_of_the_close_it_caused(
    client: VaifClient,
) -> None:
    socket = HeartbeatSocket(
        [
            {"type": "welcome", "heartbeatIntervalMs": 10},
            {"type": "subscribed", "channel": "table:todos"},
        ],
        code=1000,
        reason="",
    )

    async def connect(*args, **kwargs):
        return socket

    client.auth.set_session("token")
    with patch("vaifstudio.realtime.connect", connect):
        async with client.realtime.subscribe("todos") as subscription:
            client.auth._set(None, "SIGNED_OUT")  # the session is cleared elsewhere
            with pytest.raises(VaifAuthError) as caught:
                await asyncio.wait_for(anext(subscription), 1)
    assert caught.value.code == "NOT_SIGNED_IN"


@pytest.mark.parametrize(
    "base_url,expected",
    [
        ("https://api.example.com", "wss://api.example.com/realtime/ws"),
        ("HTTPS://api.example.com", "wss://api.example.com/realtime/ws"),
        ("Https://api.example.com:8443/v2/", "wss://api.example.com:8443/v2/realtime/ws"),
        ("http://localhost:3147", "ws://localhost:3147/realtime/ws"),
        ("HTTP://localhost:3147/", "ws://localhost:3147/realtime/ws"),
        ("http://127.0.0.1:3147", "ws://127.0.0.1:3147/realtime/ws"),
        ("http://[::1]:3147", "ws://[::1]:3147/realtime/ws"),
    ],
)
def test_realtime_url_is_wss_for_https_and_ws_only_for_loopback(
    base_url: str, expected: str
) -> None:
    from vaifstudio.realtime import realtime_url

    assert realtime_url(base_url) == expected


@pytest.mark.parametrize(
    "base_url",
    [
        "http://api.example.com",
        "HTTP://api.example.com",
        "http://localhost.example.com",
        "http://192.168.1.10:3147",
        "ftp://api.example.com",
        "ws://localhost:3147",
        "wss://api.example.com",
        "https://user:secret@api.example.com",
        "api.example.com",
        "https://",
        "",
    ],
)
def test_realtime_url_refuses_every_other_scheme_and_host(base_url: str) -> None:
    from vaifstudio.realtime import realtime_url

    with pytest.raises(VaifError) as caught:
        realtime_url(base_url)
    assert caught.value.code == "INVALID_REALTIME_URL"
    assert caught.value.message == (
        "Realtime needs an https base URL (http only for localhost, 127.0.0.1 or ::1)"
    )


async def test_an_uppercase_https_base_url_opens_a_wss_socket() -> None:
    dialed: list[str] = []

    async def connect(url: str, **kwargs):
        dialed.append(url)
        return FakeSocket([{"type": "welcome"}, {"type": "subscribed", "channel": "table:todos"}])

    async with VaifClient("proj_123", "vk_pub_test", base_url="HTTPS://api.test.vaif") as c:
        with patch("vaifstudio.realtime.connect", connect):
            async with c.realtime.subscribe("todos"):
                pass
    assert dialed == ["wss://api.test.vaif/realtime/ws"]


async def test_an_unsafe_base_url_is_refused_before_the_token_is_read() -> None:
    import httpx

    requests: list[str] = []

    def transport(request: httpx.Request) -> httpx.Response:
        requests.append(str(request.url))
        return httpx.Response(500)

    async def connect(url: str, **kwargs):
        pytest.fail("No socket may be opened for an unsafe base URL")

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(transport))
    async with VaifClient("proj_123", "vk_pub_test", http_client=http_client) as c:
        # VaifClient refuses this base URL; set it directly to test the
        # realtime check on its own.
        c._transport.base_url = "http://api.example.com"
        # An expired session: reading the token would call the refresh route.
        c.auth.set_session("at", "rt", expires_at=0.0)
        with patch("vaifstudio.realtime.connect", connect), pytest.raises(VaifError) as caught:
            async with c.realtime.subscribe("todos"):
                pytest.fail("An unsafe base URL must not open a subscription")
    await http_client.aclose()
    assert caught.value.code == "INVALID_REALTIME_URL"
    assert requests == []


async def test_a_socket_error_while_reading_raises_a_network_error(client: VaifClient) -> None:
    class BrokenReader(FakeSocket):
        async def recv(self) -> str:
            if self.frames.empty():
                raise OSError(54, "Connection reset by peer")
            return await self.frames.get()

    socket = BrokenReader([{"type": "welcome"}, {"type": "subscribed", "channel": "table:todos"}])

    async def connect(*args, **kwargs):
        return socket

    with patch("vaifstudio.realtime.connect", connect):
        async with client.realtime.subscribe("todos") as subscription:
            with pytest.raises(VaifNetworkError) as caught:
                await asyncio.wait_for(anext(subscription), 1)
    assert caught.value.code == "REALTIME_CLOSED"
    assert caught.value.message == "Realtime connection failed: ConnectionResetError"
    assert isinstance(caught.value.__cause__, ConnectionResetError)


async def test_a_heartbeat_that_fails_unexpectedly_raises_a_network_error(
    client: VaifClient,
) -> None:
    failure = RuntimeError("cannot call send while another coroutine is sending")

    class BusySocket(FakeSocket):
        async def send(self, frame: str) -> None:
            if json.loads(frame) == {"type": "ping"}:
                raise failure
            await super().send(frame)

        async def recv(self) -> str:
            if self.frames.empty():
                while not self.closed:
                    await asyncio.sleep(0.001)
                from websockets.exceptions import ConnectionClosedOK
                from websockets.frames import Close

                raise ConnectionClosedOK(Close(1000, ""), None)
            return await self.frames.get()

        async def close(self) -> None:
            self.closed = True

    socket = BusySocket(
        [
            {"type": "welcome", "heartbeatIntervalMs": 10},
            {"type": "subscribed", "channel": "table:todos"},
        ]
    )

    async def connect(*args, **kwargs):
        return socket

    with patch("vaifstudio.realtime.connect", connect):
        async with client.realtime.subscribe("todos") as subscription:
            with pytest.raises(VaifNetworkError) as caught:
                await asyncio.wait_for(anext(subscription), 1)
    assert caught.value.code == "REALTIME_CLOSED"
    assert caught.value.message == "Realtime heartbeat failed: RuntimeError"
    assert caught.value.__cause__ is failure


@respx.mock
async def test_a_subscription_is_not_opened_as_the_user_who_replaced_it_during_the_refresh(
    client: VaifClient,
) -> None:
    # User A's token is about to expire, so opening waits on a refresh. A
    # signs out and B signs in meanwhile. The socket must not open as B.
    held = HeldResponse(login_response("at_a2", "rt_a2"))
    respx.post(auth_url("refresh")).mock(side_effect=held)
    respx.post(auth_url("logout")).mock(return_value=httpx.Response(200, json={"ok": True}))
    connections: list[str] = []

    async def connect(url: str, **kwargs):
        connections.append(url)
        return FakeSocket([])

    client.auth.set_session("at_a", "rt_a", expires_at=time.time() + 5)
    with patch("vaifstudio.realtime.connect", connect):
        opening = asyncio.ensure_future(client.realtime.subscribe("todos").__aenter__())
        await held.arrived.wait()
        await client.auth.sign_out()
        client.auth.set_session("at_b", "rt_b")
        held.release.set()
        with pytest.raises(VaifAuthError) as caught:
            await asyncio.wait_for(opening, 1)
    assert caught.value.code == "NOT_SIGNED_IN"
    assert connections == []


async def test_the_heartbeat_does_not_authenticate_the_socket_as_another_user(
    client: VaifClient,
) -> None:
    socket = HeartbeatSocket(
        [
            {"type": "welcome", "heartbeatIntervalMs": 10},
            {"type": "subscribed", "channel": "table:todos"},
        ],
        code=1000,
        reason="",
    )

    async def connect(*args, **kwargs):
        return socket

    client.auth.set_session("at_a", "rt_a")
    with patch("vaifstudio.realtime.connect", connect):
        async with client.realtime.subscribe("todos") as subscription:
            client.auth.set_session("at_b", "rt_b")  # another user signs in
            with pytest.raises(VaifAuthError) as caught:
                await asyncio.wait_for(anext(subscription), 1)
    assert caught.value.code == "NOT_SIGNED_IN"
    assert {"type": "auth", "apiKey": "vk_pub_test", "accessToken": "at_a"} in socket.sent
    assert [frame for frame in socket.sent if frame.get("accessToken") == "at_b"] == []
    assert {"type": "ping"} not in socket.sent
    assert socket.closed


@respx.mock
async def test_the_heartbeat_does_not_use_a_session_set_during_its_own_refresh(
    client: VaifClient,
) -> None:
    # The refresh the heartbeat starts for user A's expiring token is still
    # running when B's session is set. B's token must not reach the socket.
    held = HeldResponse(login_response("at_a2", "rt_a2"))
    respx.post(auth_url("refresh")).mock(side_effect=held)
    socket = HeartbeatSocket(
        [
            {"type": "welcome", "heartbeatIntervalMs": 10},
            {"type": "subscribed", "channel": "table:todos"},
        ],
        code=1000,
        reason="",
    )

    async def connect(*args, **kwargs):
        return socket

    client.auth.set_session("at_a", "rt_a", expires_at=time.time() + 40)
    with patch("vaifstudio.realtime.connect", connect):
        async with client.realtime.subscribe("todos") as subscription:
            # Outside the 30-second leeway when opened; inside 60 seconds.
            with patch("vaifstudio.auth.REFRESH_LEEWAY_SECONDS", 60.0):
                await asyncio.wait_for(held.arrived.wait(), 1)
                client.auth.set_session("at_b", "rt_b")
                held.release.set()
                with pytest.raises(VaifAuthError) as caught:
                    await asyncio.wait_for(anext(subscription), 1)
    assert caught.value.code == "NOT_SIGNED_IN"
    assert [frame for frame in socket.sent if frame.get("accessToken") == "at_b"] == []
    assert {"type": "ping"} not in socket.sent


async def test_a_subscription_sends_no_credentials_if_the_user_changed_while_it_connected(
    client: VaifClient,
) -> None:
    socket = FakeSocket([])
    reached = asyncio.Event()
    proceed = asyncio.Event()

    async def connect(url: str, **kwargs):
        reached.set()
        await proceed.wait()
        return socket

    client.auth.set_session("at_a", "rt_a")
    with patch("vaifstudio.realtime.connect", connect):
        opening = asyncio.ensure_future(client.realtime.subscribe("todos").__aenter__())
        await asyncio.wait_for(reached.wait(), 1)
        client.auth.set_session("at_b", "rt_b")  # another user signs in
        proceed.set()
        with pytest.raises(VaifAuthError) as caught:
            await asyncio.wait_for(opening, 1)
    assert caught.value.code == "NOT_SIGNED_IN"
    assert [frame for frame in socket.sent if frame["type"] == "auth"] == []
    assert socket.closed
