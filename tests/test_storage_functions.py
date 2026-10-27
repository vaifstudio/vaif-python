from __future__ import annotations

import io
import json

import httpx
import pytest
import respx

from tests.conftest import BASE, auth_url
from vaifstudio import (
    VaifAuthError,
    VaifClient,
    VaifError,
    VaifNotFoundError,
    VaifServerError,
    VaifValidationError,
)

PRESIGNED = "https://objects.test/vaif/dev/proj_123/avatars/u1.png?X-Amz-Signature=abc"


@respx.mock
async def test_upload_mints_url_then_puts_bytes_without_api_credentials(client: VaifClient) -> None:
    mint = respx.post(f"{BASE}/storage/upload-url").mock(
        return_value=httpx.Response(200, json={"ok": True, "url": PRESIGNED})
    )
    put = respx.put(PRESIGNED).mock(return_value=httpx.Response(200))
    client.auth.set_session("at_user", "rt_user")

    result = await client.storage.upload(
        "avatars/u1.png", b"\x89PNG", content_type="image/png", bucket="media"
    )

    assert json.loads(mint.calls.last.request.content) == {
        "key": "avatars/u1.png",
        "bucket": "media",
        "sizeBytes": 4,
        "contentType": "image/png",
    }
    assert mint.calls.last.request.headers["authorization"] == "Bearer at_user"
    upload = put.calls.last.request
    assert upload.content == b"\x89PNG"
    assert upload.headers["content-type"] == "image/png"
    assert "x-vaif-key" not in upload.headers  # never leak the key to the object store
    assert "authorization" not in upload.headers
    assert (result.key, result.bucket, result.size) == ("avatars/u1.png", "media", 4)


@respx.mock
async def test_upload_accepts_binary_file_and_omits_default_bucket(client: VaifClient) -> None:
    mint = respx.post(f"{BASE}/storage/upload-url").mock(
        return_value=httpx.Response(200, json={"ok": True, "url": PRESIGNED})
    )
    put = respx.put(PRESIGNED).mock(return_value=httpx.Response(200))
    await client.storage.upload("docs/a.txt", io.BytesIO(b"hello"))
    assert "bucket" not in json.loads(mint.calls.last.request.content)
    assert put.calls.last.request.content == b"hello"


@respx.mock
async def test_upload_retries_the_put_but_never_the_metered_mint(client: VaifClient) -> None:
    mint = respx.post(f"{BASE}/storage/upload-url").mock(
        side_effect=[
            httpx.Response(200, json={"ok": True, "url": PRESIGNED}),
            httpx.Response(503),
        ]
    )
    put = respx.put(PRESIGNED).mock(
        side_effect=[httpx.Response(503), httpx.ReadTimeout("slow"), httpx.Response(200)]
    )
    await client.storage.upload("a.txt", b"x")
    assert put.call_count == 3
    with pytest.raises(VaifServerError):
        await client.storage.upload("a.txt", b"x")
    assert mint.call_count == 2


@respx.mock
async def test_upload_surfaces_object_store_rejection(client: VaifClient) -> None:
    respx.post(f"{BASE}/storage/upload-url").mock(
        return_value=httpx.Response(200, json={"ok": True, "url": PRESIGNED})
    )
    respx.put(PRESIGNED).mock(
        return_value=httpx.Response(403, text="<Error><Code>SignatureDoesNotMatch</Code></Error>")
    )
    with pytest.raises(VaifError) as info:
        await client.storage.upload("a.txt", b"x")
    assert info.value.status == 403


@respx.mock
async def test_an_object_store_redirect_on_upload_keeps_no_signed_query_string(
    client: VaifClient,
) -> None:
    respx.post(f"{BASE}/storage/upload-url").mock(
        return_value=httpx.Response(200, json={"ok": True, "url": PRESIGNED})
    )
    respx.put(PRESIGNED).mock(
        return_value=httpx.Response(
            307, headers={"Location": "https://objects-2.test/u1.png?X-Amz-Signature=sig_secret"}
        )
    )
    with pytest.raises(VaifError) as info:
        await client.storage.upload("avatars/u1.png", b"x")
    assert info.value.status == 307
    assert info.value.code == "STORAGE_UPLOAD_FAILED"
    assert info.value.headers["location"] == "https://objects-2.test/u1.png"
    assert "sig_secret" not in repr(info.value) + str(info.value)


async def test_rejects_unsafe_keys(client: VaifClient) -> None:
    for key in ["", "/abs", "a/../b", "bad\x00key"]:
        with pytest.raises(ValueError):
            await client.storage.upload(key, b"x")


LINK = "https://files.test/s/abc123"
OBJECT = "https://objects.test/vaif/dev/proj_123/a.txt?X-Amz-Signature=def"


@respx.mock
async def test_download_reads_the_signed_link_without_api_credentials(
    client: VaifClient,
) -> None:
    # The API's GET /storage/download only redirects to a short link, so
    # download() mints the link itself and reads it with no SDK headers.
    mint = respx.post(f"{BASE}/storage/download-url").mock(
        return_value=httpx.Response(200, json={"ok": True, "url": LINK, "expiresIn": 600})
    )
    link = respx.get(LINK).mock(return_value=httpx.Response(307, headers={"Location": OBJECT}))
    stored = respx.get(OBJECT).mock(return_value=httpx.Response(200, content=b"file-bytes"))
    client.auth.set_session("at_user")

    assert await client.storage.download("a.txt", bucket="media") == b"file-bytes"

    assert json.loads(mint.calls.last.request.content) == {"key": "a.txt", "bucket": "media"}
    assert mint.calls.last.request.headers["authorization"] == "Bearer at_user"
    for request in (link.calls.last.request, stored.calls.last.request):
        assert "x-vaif-key" not in request.headers
        assert "authorization" not in request.headers


@respx.mock
async def test_download_of_a_missing_object_is_typed(client: VaifClient) -> None:
    respx.post(f"{BASE}/storage/download-url").mock(
        return_value=httpx.Response(200, json={"ok": True, "url": LINK})
    )
    respx.get(LINK).mock(return_value=httpx.Response(404, text="Not Found"))
    with pytest.raises(VaifNotFoundError) as info:
        await client.storage.download("missing.txt")
    assert info.value.code == "STORAGE_DOWNLOAD_FAILED"


@respx.mock
async def test_download_refuses_a_redirect_to_plain_http(client: VaifClient) -> None:
    respx.post(f"{BASE}/storage/download-url").mock(
        return_value=httpx.Response(200, json={"ok": True, "url": LINK})
    )
    respx.get(LINK).mock(
        return_value=httpx.Response(307, headers={"Location": "http://objects.test/a.txt"})
    )
    downgraded = respx.get("http://objects.test/a.txt").mock(
        return_value=httpx.Response(200, content=b"cleartext")
    )
    with pytest.raises(VaifError) as info:
        await client.storage.download("a.txt")
    assert info.value.code == "INSECURE_STORAGE_URL"
    assert downgraded.call_count == 0


@respx.mock
async def test_download_follows_at_most_five_redirects(client: VaifClient) -> None:
    respx.post(f"{BASE}/storage/download-url").mock(
        return_value=httpx.Response(200, json={"ok": True, "url": LINK})
    )
    loop = respx.get(LINK).mock(return_value=httpx.Response(302, headers={"Location": LINK}))
    with pytest.raises(VaifError) as info:
        await client.storage.download("a.txt")
    assert info.value.code == "STORAGE_DOWNLOAD_FAILED"
    assert info.value.message == "The storage download was redirected more than 5 times"
    assert loop.call_count == 6


@pytest.mark.parametrize(
    "url",
    [
        "http://objects.example/put?sig",
        "HTTP://objects.example/put?sig",
        "http://localhost.example/put?sig",
        "ftp://objects.example/put",
        "/storage/object?sig",
        "objects.example/put",
    ],
)
@respx.mock
async def test_signed_urls_must_be_https_except_loopback(client: VaifClient, url: str) -> None:
    respx.post(f"{BASE}/storage/download-url").mock(
        return_value=httpx.Response(200, json={"ok": True, "url": url})
    )
    respx.post(f"{BASE}/storage/upload-url").mock(
        return_value=httpx.Response(200, json={"ok": True, "url": url})
    )
    calls = [
        client.storage.create_signed_url("a.txt"),
        client.storage.create_signed_upload_url("a.txt", size_bytes=1),
        client.storage.upload("a.txt", b"x"),
        client.storage.download("a.txt"),
    ]
    for call in calls:
        with pytest.raises(VaifError) as info:
            await call
        assert info.value.code == "INSECURE_STORAGE_URL"
        assert info.value.message == (
            "The storage URL must use https (http only for localhost, 127.0.0.1 or ::1)"
        )
    # Only the four mints were sent: nothing went to a refused URL.
    assert [c.request.method for c in respx.calls] == ["POST"] * 4


@pytest.mark.parametrize(
    "url",
    [
        "https://objects.example/put?sig",
        "HTTPS://objects.example/put?sig",
        "http://localhost:9000/put?sig",
        "http://127.0.0.1:9000/put?sig",
        "http://[::1]:9000/put?sig",
    ],
)
@respx.mock
async def test_https_and_loopback_signed_urls_are_accepted(client: VaifClient, url: str) -> None:
    respx.post(f"{BASE}/storage/upload-url").mock(
        return_value=httpx.Response(200, json={"ok": True, "url": url})
    )
    assert await client.storage.create_signed_upload_url("a.txt", size_bytes=1) == url


@respx.mock
async def test_signed_urls(client: VaifClient) -> None:
    down = respx.post(f"{BASE}/storage/download-url").mock(
        side_effect=[
            httpx.Response(503),
            httpx.Response(200, json={"ok": True, "url": "https://s3/get?sig"}),
            httpx.Response(200, json={"ok": True, "url": "https://s3/get?sig"}),
        ]
    )
    up = respx.post(f"{BASE}/storage/upload-url").mock(
        return_value=httpx.Response(200, json={"ok": True, "url": "https://s3/put?sig"})
    )
    assert await client.storage.create_signed_url("a.txt", bucket="media") == "https://s3/get?sig"
    assert down.call_count == 2  # minting a URL is replay-safe
    assert json.loads(down.calls.last.request.content) == {"key": "a.txt", "bucket": "media"}
    # The lifetime may be chosen; omitted, the project's default applies.
    await client.storage.create_signed_url("a.txt", expires_in=3600)
    assert json.loads(down.calls.last.request.content) == {"key": "a.txt", "expiresIn": 3600}
    assert (
        await client.storage.create_signed_upload_url("b.bin", size_bytes=10)
        == "https://s3/put?sig"
    )
    assert json.loads(up.calls.last.request.content) == {"key": "b.bin", "sizeBytes": 10}
    await client.storage.create_signed_upload_url(
        "c.txt", size_bytes=3, content_type="text/plain", bucket="docs"
    )
    assert json.loads(up.calls.last.request.content) == {
        "key": "c.txt",
        "bucket": "docs",
        "sizeBytes": 3,
        "contentType": "text/plain",
    }


async def test_signed_upload_url_requires_a_valid_size(client: VaifClient) -> None:
    with pytest.raises(TypeError):
        await client.storage.create_signed_upload_url("a.txt")  # type: ignore[call-arg]
    for size in [0, -1, True, 1.5, 5 * 1024**3 + 1]:
        with pytest.raises(ValueError):
            await client.storage.create_signed_upload_url("a.txt", size_bytes=size)  # type: ignore[arg-type]


@respx.mock
async def test_invoke_sends_envelope_and_parses_json(client: VaifClient) -> None:
    route = respx.post(f"{BASE}/functions/send-email/invoke").mock(
        return_value=httpx.Response(200, json={"sent": True}, headers={"x-fn": "1"})
    )
    response = await client.functions.invoke("send-email", {"to": "a@b.c", "path": "not-routing"})
    assert json.loads(route.calls.last.request.content) == {
        "method": "POST",
        "path": "/",
        "body": {"to": "a@b.c", "path": "not-routing"},
    }
    assert response.status == 200
    assert response.data == {"sent": True}
    assert response.headers["x-fn"] == "1"


@respx.mock
async def test_invoke_with_method_path_query_and_text_body(client: VaifClient) -> None:
    route = respx.post(f"{BASE}/functions/report/invoke").mock(
        return_value=httpx.Response(200, text="ok", headers={"content-type": "text/plain"})
    )
    response = await client.functions.invoke(
        "report", method="get", path="/daily", query={"day": "mon"}, headers={"X-T": "1"}
    )
    assert json.loads(route.calls.last.request.content) == {
        "method": "GET",
        "path": "/daily",
        "query": {"day": "mon"},
        "headers": {"X-T": "1"},
    }
    assert response.data == "ok"


@respx.mock
async def test_invoke_errors_carry_function_body_and_are_not_retried(client: VaifClient) -> None:
    route = respx.post(f"{BASE}/functions/f/invoke").mock(
        return_value=httpx.Response(
            400, json={"error": "ValidationError", "message": "bad input", "field": "to"}
        )
    )
    with pytest.raises(VaifValidationError) as info:
        await client.functions.invoke("f", {})
    assert info.value.body["field"] == "to"
    assert route.call_count == 1


@respx.mock
async def test_invoke_can_opt_in_to_retries(client: VaifClient) -> None:
    route = respx.post(f"{BASE}/functions/f/invoke").mock(
        side_effect=[httpx.Response(502), httpx.Response(200, json={"ok": 1})]
    )
    response = await client.functions.invoke("f", {}, idempotent=True)
    assert response.data == {"ok": 1}
    assert route.call_count == 2


@pytest.mark.parametrize("idempotent", [False, True])
@respx.mock
async def test_only_the_apis_own_401_refreshes_and_resends_an_invocation(
    client: VaifClient, idempotent: bool
) -> None:
    # The invoke route relays the function's status. A 401 that carries
    # X-Vaif-Run-Id is the function's own answer: the function ran, and the
    # session is not the problem. A 401 without it is the API refusing the
    # token before the function runs.
    refresh = respx.post(auth_url("refresh")).mock(
        return_value=httpx.Response(
            200,
            json={"accessToken": "at_2", "expiresIn": 900},
            headers={"set-cookie": "project_refresh_token=rt_2; Path=/; HttpOnly"},
        )
    )
    charge = respx.post(f"{BASE}/functions/charge/invoke").mock(
        return_value=httpx.Response(
            401, json={"error": "card_declined"}, headers={"X-Vaif-Run-Id": "run_1"}
        )
    )
    client.auth.set_session("at_1", "rt_1")

    with pytest.raises(VaifAuthError) as info:
        await client.functions.invoke("charge", {"amount": 100}, idempotent=idempotent)
    assert info.value.code == "card_declined"
    assert info.value.headers["x-vaif-run-id"] == "run_1"
    assert charge.call_count == 1
    assert refresh.call_count == 0
    assert client.auth.session is not None
    assert client.auth.session.access_token == "at_1"

    report = respx.post(f"{BASE}/functions/report/invoke").mock(
        side_effect=[
            httpx.Response(401, json={"error": "UNAUTHORIZED", "code": "TOKEN_INVALID"}),
            httpx.Response(200, json={"ok": True}, headers={"X-Vaif-Run-Id": "run_2"}),
        ]
    )
    response = await client.functions.invoke("report", {}, idempotent=idempotent)
    assert response.data == {"ok": True}
    assert refresh.call_count == 1
    assert [call.request.headers["authorization"] for call in report.calls] == [
        "Bearer at_1",
        "Bearer at_2",
    ]


async def test_invoke_validates_arguments(client: VaifClient) -> None:
    with pytest.raises(ValueError):
        await client.functions.invoke("")
    with pytest.raises(ValueError):
        await client.functions.invoke("f", method="TRACE")
    with pytest.raises(ValueError):
        await client.functions.invoke("f", path="no-slash")


@respx.mock
async def test_storage_list_uses_bucket_id_console_session_and_preserves_pagination(
    client: VaifClient,
) -> None:
    client.auth.set_session("at_console")
    route = respx.get(f"{BASE}/buckets/bucket_123/files").mock(
        return_value=httpx.Response(
            200,
            json={
                "ok": True,
                "files": [{"key": "docs/a.txt", "size": 5, "etag": "e", "custom": "kept"}],
                "folders": ["docs/"],
                "nextToken": "next",
                "isTruncated": True,
            },
        )
    )
    result = await client.storage.list("bucket_123", prefix="docs/", limit=7, cursor="previous")
    assert dict(route.calls.last.request.url.params) == {
        "prefix": "docs/",
        "maxKeys": "7",
        "continuationToken": "previous",
    }
    assert route.calls.last.request.headers["authorization"] == "Bearer at_console"
    assert result["files"][0]["custom"] == "kept"
    assert result["prefixes"] == ["docs/"]
    assert result["nextCursor"] == "next" and result["hasMore"] is True


@respx.mock
async def test_storage_list_rejects_malformed_success_body(client: VaifClient) -> None:
    respx.get(f"{BASE}/buckets/bucket_123/files").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    with pytest.raises(VaifError, match="file list"):
        await client.storage.list("bucket_123")


@respx.mock
async def test_an_undecodable_object_store_answer_raises_a_network_error(
    client: VaifClient,
) -> None:
    from vaifstudio import VaifNetworkError

    respx.post(f"{BASE}/storage/upload-url").mock(
        return_value=httpx.Response(200, json={"ok": True, "url": PRESIGNED})
    )
    respx.put(PRESIGNED).mock(
        return_value=httpx.Response(
            200,
            headers={"Content-Encoding": "gzip"},
            stream=httpx.ByteStream(b"not gzip"),
        )
    )
    with pytest.raises(VaifNetworkError) as info:
        await client.storage.upload("a.txt", b"x")
    assert info.value.message == "Network error uploading: DecodingError"
