"""A value that becomes a URL path segment cannot be "." or "..".

httpx removes dot segments from a request path, so ``delete("..")`` on a table
would send ``DELETE /v1/data/proj_123`` and ``get(".")`` would send
``GET /v1/data/proj_123/todos``: another route, with the same key and session.
Percent-encoding does not help, because ``.`` and ``..`` are unreserved.
"""

from __future__ import annotations

from typing import Any, Awaitable, Callable

import httpx
import pytest
import respx

from tests.conftest import BASE, FAST_RETRY, KEY, PROJECT, data_url
from vaifstudio import VaifClient

Case = Callable[[VaifClient, str], Awaitable[Any]]


async def _row_get(client: VaifClient, segment: str) -> Any:
    return await client.from_("todos").get(segment)


async def _row_update(client: VaifClient, segment: str) -> Any:
    return await client.from_("todos").update(segment, {"done": True})


async def _row_delete(client: VaifClient, segment: str) -> Any:
    return await client.from_("todos").delete(segment)


async def _operation_path(client: VaifClient, segment: str) -> Any:
    return await client.operations.get_projects_by_project_id(path={"projectId": segment})


async def _function_name(client: VaifClient, segment: str) -> Any:
    return await client.functions.invoke(segment)


async def _copilot_job(client: VaifClient, segment: str) -> Any:
    return await client.copilot("account_token").get_job(segment)


async def _copilot_session(client: VaifClient, segment: str) -> Any:
    return await client.copilot("account_token").get_session(segment)


async def _storage_list(client: VaifClient, segment: str) -> Any:
    return await client.storage.list(segment)


async def _storage_delete(client: VaifClient, segment: str) -> Any:
    return await client.storage.delete("avatars/u1.png", bucket_id=segment)


async def _oauth_provider(client: VaifClient, segment: str) -> Any:
    return await client.auth.get_oauth_sign_in_url(segment, redirect_url="https://app.example/cb")


async def _project_id_in_auth(client: VaifClient, segment: str) -> Any:
    async with VaifClient(segment, KEY, base_url=BASE, retry=FAST_RETRY) as other:
        return await other.auth.sign_in("ada@example.com", "pw")


async def _project_id_in_data(client: VaifClient, segment: str) -> Any:
    async with VaifClient(segment, KEY, base_url=BASE, retry=FAST_RETRY) as other:
        return await other.from_("todos").list()


CASES: dict[str, Case] = {
    "row get": _row_get,
    "row update": _row_update,
    "row delete": _row_delete,
    "operation path parameter": _operation_path,
    "function name": _function_name,
    "copilot job id": _copilot_job,
    "copilot session id": _copilot_session,
    "storage list bucket id": _storage_list,
    "storage delete bucket id": _storage_delete,
    "oauth provider": _oauth_provider,
    "project id in auth": _project_id_in_auth,
    "project id in data": _project_id_in_data,
}


@pytest.mark.parametrize("segment", [".", ".."])
@pytest.mark.parametrize("case", list(CASES), ids=list(CASES))
@respx.mock
async def test_a_dot_segment_is_refused_before_any_request(
    client: VaifClient, case: str, segment: str
) -> None:
    anywhere = respx.route().mock(return_value=httpx.Response(200, json={"data": {}, "count": 0}))

    with pytest.raises(ValueError, match="must not be"):
        await CASES[case](client, segment)

    assert anywhere.call_count == 0


@pytest.mark.parametrize("segment", ["...", "..x", "x..", ".hidden", "a.b", "v1.0.0"])
@respx.mock
async def test_a_value_that_only_contains_dots_is_sent_as_written(
    client: VaifClient, segment: str
) -> None:
    route = respx.get(data_url("todos", "/" + segment)).mock(
        return_value=httpx.Response(200, json={"data": {"id": segment}})
    )
    operation = respx.get(f"{BASE}/projects/{segment}").mock(
        return_value=httpx.Response(200, json={"id": segment})
    )

    assert await client.from_("todos").get(segment) == {"id": segment}
    await client.operations.get_projects_by_project_id(path={"projectId": segment})

    assert route.calls.last.request.url.path == f"/v1/data/{PROJECT}/todos/{segment}"
    assert operation.call_count == 1


@respx.mock
async def test_a_percent_encoded_dot_segment_is_sent_encoded(client: VaifClient) -> None:
    # "%2e%2e" is a literal value here, not a dot segment: its percent sign is
    # encoded too, so the server receives the characters the caller passed.
    route = respx.delete(url__regex=r".*").mock(return_value=httpx.Response(204))

    await client.from_("todos").delete("%2e%2e")

    assert route.calls.last.request.url.raw_path == b"/v1/data/proj_123/todos/%252e%252e"
