"""The spec-generated operation surface (``client.operations``).

``vaifstudio/_generated/`` is written by the SDK generator and never edited by
hand; these tests pin the hand-written runtime underneath it
(``vaifstudio._operations``) and the contract between the two: every table entry
has a method, every method hits the route its table entry names, through the
client's own transport (API key, session, error mapping).
"""

from __future__ import annotations

import inspect
import json
import re
from pathlib import Path

import httpx
import pytest
import respx

from tests.conftest import BASE
from vaifstudio import VaifAuthError, VaifClient, VaifError, VaifNetworkError, VaifNotFoundError
from vaifstudio._generated import OPERATIONS, UNGENERATED_OPERATIONS, Operations
from vaifstudio._operations import build_path, flatten_query


def test_build_path_encodes_each_segment_and_rejects_missing_params() -> None:
    assert (
        build_path(
            "/projects/{projectId}/tables/{table}",
            {"projectId": "p 1", "table": "a/b"},
            ("projectId", "table"),
        )
        == "/projects/p%201/tables/a%2Fb"
    )
    with pytest.raises(ValueError, match="missing path parameter.*projectId"):
        build_path("/projects/{projectId}", {}, ("projectId",))


def test_flatten_query_matches_the_api_parser() -> None:
    assert flatten_query(
        {
            "limit": 10,
            "archived": False,
            "tags": ["a", None, "b"],
            "filter": {"status": "open", "gone": None},
            "skip": None,
        }
    ) == {"limit": 10, "archived": "false", "tags": ["a", "b"], "filter[status]": "open"}
    assert flatten_query(None) is None
    assert flatten_query({"skip": None}) is None


def test_every_table_entry_has_a_method_and_vice_versa() -> None:
    methods = {
        name
        for name, member in inspect.getmembers(Operations, inspect.isfunction)
        if not name.startswith("_")
    }
    assert methods == set(OPERATIONS)
    # 943 operations in the API's OpenAPI description: 775 generated, 168 not.
    assert len(OPERATIONS) == 775
    assert len(UNGENERATED_OPERATIONS) == 168
    # The skipped routes are listed as (method, path, reason), never silently dropped.
    assert all(len(entry) == 3 and entry[2] for entry in UNGENERATED_OPERATIONS)
    generated_routes = {(op.method, op.path) for op in OPERATIONS.values()}
    assert not generated_routes & {(m, p) for m, p, _ in UNGENERATED_OPERATIONS}


def test_table_entries_are_consistent_with_their_path_templates() -> None:
    for name, op in OPERATIONS.items():
        placeholders = tuple(
            seg[1:-1] for seg in op.path.split("/") if seg.startswith("{") and seg.endswith("}")
        )
        assert placeholders == op.path_params, name
        assert op.method in {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}, name
        assert op.transport in {"json", "sse", "binary"}, name


@respx.mock
async def test_operation_sends_through_the_client_transport(client: VaifClient) -> None:
    route = respx.get(f"{BASE}/projects/proj_123/api-keys").mock(
        return_value=httpx.Response(200, json={"ok": True, "keys": []})
    )
    client.auth.set_session("at_user", "rt_user")

    result = await client.operations.get_projects_by_project_id_api_keys(
        path={"projectId": "proj_123"}
    )

    assert result == {"ok": True, "keys": []}
    request = route.calls.last.request
    assert request.headers["authorization"] == "Bearer at_user"
    assert request.headers["x-vaif-key"]


@respx.mock
async def test_caller_authorization_is_not_replaced_by_the_session(client: VaifClient) -> None:
    """A platform token must survive an end-user session.

    Signed in, then calling a console operation with an explicit
    Authorization header used to send the session bearer instead, so the
    API answered 401 TOKEN_INVALID. The caller's header wins, and a 401
    on it does not refresh the session and retry.
    """
    route = respx.get(f"{BASE}/projects/proj_123/api-keys").mock(
        return_value=httpx.Response(
            401, json={"error": "TOKEN_INVALID", "message": "Invalid or expired token"}
        )
    )
    refresh = respx.post(f"{BASE}/projects/proj_123/auth/refresh").mock(
        return_value=httpx.Response(200, json={"accessToken": "at_fresh", "expiresIn": 3600})
    )
    client.auth.set_session("at_user", "rt_user")

    with pytest.raises(VaifAuthError):
        await client.operations.get_projects_by_project_id_api_keys(
            path={"projectId": "proj_123"},
            headers={"Authorization": "Bearer platform-token"},
        )

    assert route.call_count == 1
    assert route.calls.last.request.headers["authorization"] == "Bearer platform-token"
    assert refresh.call_count == 0


@respx.mock
async def test_operation_encodes_query_and_json_body(client: VaifClient) -> None:
    route = respx.post(f"{BASE}/projects").mock(
        return_value=httpx.Response(201, json={"ok": True, "project": {"id": "p"}})
    )

    await client.operations.post_projects(body={"name": "demo", "region": "eu-west"})

    request = route.calls.last.request
    assert json.loads(request.content) == {"name": "demo", "region": "eu-west"}
    assert request.headers["content-type"].startswith("application/json")

    listing = respx.get(f"{BASE}/logs/project/p").mock(
        return_value=httpx.Response(200, json={"ok": True, "logs": []})
    )
    await client.operations.get_logs_project_by_project_id(
        path={"projectId": "p"}, query={"limit": 5, "archived": False}
    )
    assert dict(listing.calls.last.request.url.params) == {"limit": "5", "archived": "false"}


@respx.mock
async def test_operation_errors_map_like_the_hand_written_modules(client: VaifClient) -> None:
    respx.get(f"{BASE}/projects/missing").mock(
        return_value=httpx.Response(
            404, json={"ok": False, "error": {"code": "NOT_FOUND", "message": "no such project"}}
        )
    )
    with pytest.raises(VaifNotFoundError):
        await client.operations.get_projects_by_project_id(path={"projectId": "missing"})


class _BrokenStream(httpx.AsyncByteStream):
    """An event stream whose connection drops after the first event."""

    async def __aiter__(self):
        yield b'data: {"type":"token","text":"Hel"}\n\n'
        raise httpx.ReadError("connection reset")


@respx.mock
async def test_an_event_stream_that_fails_midway_raises_a_vaif_error(client: VaifClient) -> None:
    respx.post(f"{BASE}/ai/copilot/chat/stream").mock(
        return_value=httpx.Response(
            200, headers={"Content-Type": "text/event-stream"}, stream=_BrokenStream()
        )
    )
    with pytest.raises(VaifNetworkError) as info:
        await client.operations.post_ai_copilot_chat_stream()
    assert info.value.message == "Network error: ReadError"
    assert isinstance(info.value.__cause__, httpx.ReadError)


SIGNED_LINK = "https://files.test/vaif/proj_123/a.txt?X-Amz-Signature=sig_1"


@respx.mock
async def test_the_generated_download_reads_the_signed_link_without_api_credentials(
    client: VaifClient,
) -> None:
    # GET /storage/download answers with a 307 to a signed link. The SDK reads
    # the link itself, without the API key or the session token.
    api = respx.get(f"{BASE}/storage/download").mock(
        return_value=httpx.Response(307, headers={"Location": SIGNED_LINK})
    )
    link = respx.get(SIGNED_LINK).mock(return_value=httpx.Response(200, content=b"file-bytes"))
    client.auth.set_session("at_user")

    data = await client.operations.get_storage_download(query={"key": "a.txt", "bucket": "media"})

    assert data == b"file-bytes"
    sent = api.calls.last.request
    assert sent.url.params["key"] == "a.txt"
    assert sent.url.params["bucket"] == "media"
    assert sent.headers["authorization"] == "Bearer at_user"
    assert sent.headers["x-vaif-key"] == "vk_pub_test"
    read = link.calls.last.request
    assert "x-vaif-key" not in read.headers
    assert "authorization" not in read.headers


@respx.mock
async def test_the_generated_download_refuses_a_plain_http_signed_link(
    client: VaifClient,
) -> None:
    respx.get(f"{BASE}/storage/download").mock(
        return_value=httpx.Response(307, headers={"Location": "http://files.test/a.txt?sig=1"})
    )
    cleartext = respx.get("http://files.test/a.txt").mock(
        return_value=httpx.Response(200, content=b"cleartext")
    )
    with pytest.raises(VaifError) as info:
        await client.operations.get_storage_download(query={"key": "a.txt"})
    assert info.value.code == "INSECURE_STORAGE_URL"
    assert cleartext.call_count == 0


def test_the_generated_modules_name_nothing_outside_this_package() -> None:
    # These files ship in the wheel and in the public repository, where the
    # generator's own source tree, paths and commands do not exist.
    folder = Path(inspect.getfile(Operations)).parent
    stamp = re.compile(
        r"# Source: the VAIF Studio API's OpenAPI description, sha256:[0-9a-f]{16}; "
        r"775 operations generated, 168 not generated \(listed in "
        r"UNGENERATED_OPERATIONS with the reason\)\."
    )
    names = sorted(path.name for path in folder.glob("*.py"))
    assert names == ["__init__.py", "client.py", "operations.py"]
    for name in names:
        lines = (folder / name).read_text(encoding="utf-8").splitlines()
        assert lines[0] == "# GENERATED FILE — do not edit by hand.", name
        assert stamp.fullmatch(lines[1]), (name, lines[1])
        assert lines[2] == (
            "# Changes are made in the generator, not in this file; see CONTRIBUTING.md."
        ), name
        comments = "\n".join(line for line in lines if line.startswith("#"))
        for outside in (
            "apps/",
            "scripts/",
            "pnpm",
            "openapi-sdk.json",
            "generate.ts",
            "generator's header",
        ):
            assert outside not in comments, (name, outside)


_STAFF_ONLY_PATH = re.compile(r"^/(?:admin|auth/impersonate)(?:/|$)")

# The platform-staff operations outside /admin and /auth/impersonate. The API
# answers each only for VAIF platform staff, so the package has no method for them.
_STAFF_ONLY_OUTSIDE_ADMIN = frozenset(
    {
        ("DELETE", "/docs/api-endpoints/{id}"),
        ("DELETE", "/docs/changelog/{id}"),
        ("DELETE", "/docs/examples/{id}"),
        ("DELETE", "/docs/sdk-examples/{id}"),
        ("DELETE", "/docs/sdks/{id}"),
        ("DELETE", "/docs/v2/pages/{id}"),
        ("DELETE", "/flags/{key}"),
        ("GET", "/ai/copilot/stats"),
        ("GET", "/flags"),
        ("PATCH", "/docs/api-endpoints/{id}"),
        ("PATCH", "/docs/changelog/{id}"),
        ("PATCH", "/docs/examples/{id}"),
        ("PATCH", "/docs/sdks/{id}"),
        ("PATCH", "/docs/v2/pages/{id}"),
        ("POST", "/docs/api-endpoints"),
        ("POST", "/docs/changelog"),
        ("POST", "/docs/examples"),
        ("POST", "/docs/sdk-examples"),
        ("POST", "/docs/sdks"),
        ("POST", "/docs/v2/pages"),
        ("POST", "/enterprise/contracts"),
        ("POST", "/enterprise/contracts/{contractId}/invoice"),
        ("POST", "/enterprise/invoices/{invoiceId}/paid"),
        ("POST", "/enterprise/invoices/{invoiceId}/send"),
        ("POST", "/flags"),
        ("PUT", "/flags/{key}"),
    }
)


def _is_staff_only(method: str, path: str) -> bool:
    return bool(_STAFF_ONLY_PATH.match(path)) or (method, path) in _STAFF_ONLY_OUTSIDE_ADMIN


def test_no_operation_method_calls_a_platform_staff_route() -> None:
    assert len(_STAFF_ONLY_OUTSIDE_ADMIN) == 26
    for name, op in OPERATIONS.items():
        assert not _is_staff_only(op.method, op.path), (name, op.method, op.path)
    staff = [entry for entry in UNGENERATED_OPERATIONS if entry[2] == "platform staff only"]
    assert len(staff) == 134
    for method, path, reason in UNGENERATED_OPERATIONS:
        assert _is_staff_only(method, path) == (reason == "platform staff only"), (
            method,
            path,
            reason,
        )
    assert ("POST", "/auth/impersonate/token", "platform staff only") in staff
    assert ("POST", "/admin/admins", "platform staff only") in staff

    # No module of the package names a staff route except in the list of
    # operations without a generated method. /auth/me/admin is a route of its own.
    named = re.compile(r"[\"'\s]/(?:admin|auth/impersonate)(?:[/\"'{.\s]|$)")
    listed = re.compile(r'^    \("[A-Z]+", "[^"]+", "platform staff only"\),$')
    package = Path(inspect.getfile(VaifClient)).parent
    modules = sorted(package.rglob("*.py"))
    assert len(modules) > 10
    for module in modules:
        for number, line in enumerate(module.read_text(encoding="utf-8").splitlines(), 1):
            assert not named.search(line) or listed.match(line), (module.name, number, line)


def test_the_staff_only_operations_outside_admin_have_no_method() -> None:
    assert "post_flags" not in OPERATIONS
    assert "post_enterprise_invoices_by_invoice_id_paid" not in OPERATIONS
    assert not hasattr(Operations, "post_flags")
    assert not hasattr(Operations, "post_enterprise_invoices_by_invoice_id_paid")
    assert ("POST", "/flags", "platform staff only") in UNGENERATED_OPERATIONS
    assert (
        "POST",
        "/enterprise/invoices/{invoiceId}/paid",
        "platform staff only",
    ) in UNGENERATED_OPERATIONS


def test_the_generated_docstring_states_what_an_event_stream_operation_returns() -> None:
    doc = inspect.getdoc(Operations)
    assert doc is not None
    assert doc.splitlines()[-3:] == [
        "``bytes`` (a redirect to a signed link is read without the project key",
        "or the session token), and ``sse`` operations return the",
        "``httpx.Response`` after the stream has ended, with the whole body read.",
    ]
