"""Run the shared conformance cases through their runner and the SDK, against a fake API.

The cases and the runner are maintained with the other VAIF Studio SDKs, not in
this package. Set VAIF_CONFORMANCE_DIR to the directory that holds them (it
contains run-python.py) to run this module; it is skipped otherwise. Nothing is
loaded from any other location.

This validates SDK serialization, response decoding, errors and case execution;
it does not validate the API's authorization or storage implementation.
"""

from __future__ import annotations

import importlib.util
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

import httpx
import pytest

from tests.test_realtime import FakeSocket

if not os.environ.get("VAIF_CONFORMANCE_DIR"):
    pytest.skip(
        "Set VAIF_CONFORMANCE_DIR to the shared conformance cases to run this module",
        allow_module_level=True,
    )
CONFORMANCE = Path(os.environ["VAIF_CONFORMANCE_DIR"]).resolve()
if not (CONFORMANCE / "run-python.py").is_file():
    pytest.fail(f"VAIF_CONFORMANCE_DIR has no run-python.py: {CONFORMANCE}", pytrace=False)
sys.path.insert(0, str(CONFORMANCE))
spec = importlib.util.spec_from_file_location(
    "python_conformance_runner", CONFORMANCE / "run-python.py"
)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class FakeAPI:
    def __init__(self, *, corrupt_download: bool = False) -> None:
        self.rows: dict[str, dict] = {}
        self.upload = b""
        self.rotated = False
        self.corrupt_download = corrupt_download
        self.seen: list[str] = []
        self.installed: dict | None = None

    def __call__(self, request: httpx.Request) -> httpx.Response:
        path, method = request.url.path, request.method
        self.seen.append(method + " " + path)
        payload = json.loads(request.content) if request.content and path != "/object" else {}
        if path == "/health":
            return httpx.Response(200, json={"ok": True})
        if path == "/auth/login":
            return httpx.Response(200, json={"accessToken": "platform-token"})
        assert path != "/auth/signup", "Fixture setup must use an existing local account"
        if path == "/orgs":
            return httpx.Response(200, json=[{"id": "org"}])
        if path == "/projects":
            return httpx.Response(
                200,
                json={
                    "project": {"id": "project"},
                    "keys": {"anon": "anon", "service_role": "service"},
                },
            )
        if path == "/schema-engine/push/project":
            table = payload["sql"].split("CREATE TABLE ")[1].split(" ")[0]
            return httpx.Response(200, json={"ownerRules": {"created": [table]}})
        if path == "/realtime/install":
            # Change events come from per-table triggers, which the runner
            # installs before its realtime case.
            self.installed = payload
            return httpx.Response(200, json={"ok": True})
        if path == "/storage/buckets":
            return httpx.Response(200, json={"bucket": {"id": "bucket"}})
        if path.endswith("/settings/jwt/rotate"):
            self.rotated = True
            return httpx.Response(200, json={"ok": True})
        if path == "/projects/project/auth/signup":
            actor = payload["email"].split("-")[0]
            return httpx.Response(
                200, json={"accessToken": actor, "user": {"id": actor, "email": payload["email"]}}
            )
        if path.startswith("/v1/data/project/"):
            actor = request.headers.get("authorization", "").removeprefix("Bearer ")
            if self.rotated and actor in {"alice", "bob"}:
                return httpx.Response(401, json={"code": "TOKEN_INVALID", "message": "Rotated"})
            if method == "POST":
                row = {"id": "row", "owner_id": actor, **payload}
                self.rows["row"] = row
                return httpx.Response(201, json={"data": row})
            if path.endswith("/row"):
                if method == "PATCH":
                    self.rows["row"].update(payload)
                elif method == "DELETE":
                    del self.rows["row"]
                    return httpx.Response(204)
                return httpx.Response(200, json={"data": self.rows["row"]})
            rows = [row for row in self.rows.values() if row["owner_id"] == actor]
            return httpx.Response(200, json={"data": rows, "count": len(rows)})
        if path == "/storage/upload-url":
            assert payload["sizeBytes"] == len(b"VAIF local conformance")
            return httpx.Response(200, json={"url": "http://localhost:9147/object"})
        if path == "/object":
            assert "x-vaif-key" not in request.headers and "authorization" not in request.headers
            self.upload = request.content
            return httpx.Response(200)
        if path == "/storage/download-url":
            return httpx.Response(200, json={"url": "http://localhost:9147/download"})
        if path == "/download":
            assert "x-vaif-key" not in request.headers and "authorization" not in request.headers
            return httpx.Response(200, content=b"corrupt" if self.corrupt_download else self.upload)
        if path == "/buckets/bucket/files":
            assert request.headers["authorization"] == "Bearer platform-token"
            return httpx.Response(200, json={"files": [{"key": "conformance.txt"}]})
        if path == "/functions/hello_world/invoke":
            return httpx.Response(200, json={"message": "Hello from VAIF Functions!"})
        raise AssertionError(f"Unexpected fake API request: {method} {path}")


@pytest.mark.parametrize("corrupt_download", [False, True])
async def test_shared_conformance_cases(monkeypatch, capsys, corrupt_download: bool) -> None:
    api = FakeAPI(corrupt_download=corrupt_download)
    original_client = httpx.AsyncClient

    def http_client(**kwargs):
        return original_client(transport=httpx.MockTransport(api), **kwargs)

    async def connect(url: str, **kwargs):
        assert url == "ws://localhost:3147/realtime/ws"
        table = next(
            path.split("/")[-1]
            for path in api.seen
            if path.startswith("GET /v1/data/project/") and not path.endswith("/row")
        )
        assert api.installed == {"projectId": "project", "tables": [table]}, (
            "Realtime triggers must be installed before subscribing"
        )
        return FakeSocket(
            [
                {"type": "welcome"},
                {"type": "subscribed", "channel": "table:" + table},
                {"type": "db_change", "table": table, "op": "INSERT"},
            ]
        )

    monkeypatch.setattr(runner, "API", "http://localhost:3147")
    monkeypatch.setenv("CONFORMANCE_FUNCTION", "1")
    monkeypatch.setenv("CONFORMANCE_REALTIME", "1")
    with patch("httpx.AsyncClient", http_client), patch("vaifstudio.realtime.connect", connect):
        result = await runner.main()
    output = capsys.readouterr().out
    assert result == int(corrupt_download), output
    assert (
        "3 passed, 1 failed, 0 skipped" if corrupt_download else "4 passed, 0 failed, 0 skipped"
    ) in output, output
