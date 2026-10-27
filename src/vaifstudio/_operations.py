"""Runtime behind the generated ``Operations`` class (``vaifstudio._generated``).

The generated module holds one coroutine per route and nothing else; path
building, query flattening and response decoding live here so they are
written once and tested once. The generator never touches this file.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Mapping, Optional
from urllib.parse import urljoin

import httpx

from vaifstudio._http import path_segment, response_json
from vaifstudio.exceptions import VaifConsoleOnlyError

if TYPE_CHECKING:
    from vaifstudio._generated.operations import Operation

Send = Callable[..., Awaitable[httpx.Response]]
ReadSigned = Callable[[str], Awaitable[bytes]]


def build_path(template: str, params: Optional[Mapping[str, Any]], names: tuple[str, ...]) -> str:
    """Fill ``{param}`` placeholders, percent-encoding each value as one segment.

    A value of ``.`` or ``..`` raises ``ValueError``: see ``path_segment``.
    """
    values = dict(params or {})
    missing = [n for n in names if n not in values or values[n] is None]
    if missing:
        raise ValueError(f"missing path parameter(s) for {template}: {', '.join(missing)}")
    path = template
    for name in names:
        segment = path_segment(values[name], f"path parameter {name!r}")
        path = path.replace("{" + name + "}", segment)
    return path


def flatten_query(query: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
    """Flatten a query mapping the way the API reads it.

    Nested mappings become ``key[sub]=value`` (OpenAPI ``deepObject``), lists
    repeat the key, ``None`` values are dropped. Returns ``None`` when nothing
    is left so httpx sends no ``?`` at all.
    """
    if not query:
        return None
    out: dict[str, Any] = {}
    for key, value in query.items():
        if value is None:
            continue
        if isinstance(value, Mapping):
            for sub, v in value.items():
                if v is not None:
                    out[f"{key}[{sub}]"] = v
        elif isinstance(value, (list, tuple)):
            out[key] = [str(v) for v in value if v is not None]
        elif isinstance(value, bool):
            out[key] = "true" if value else "false"
        else:
            out[key] = value
    return out or None


# Platform sign-up and forgot-password: VAIF Studio accounts are created and
# reset in the console only, whose pages carry a bot check this client cannot
# pass. These operations raise VaifConsoleOnlyError before any request. Value:
# the project-scoped operation for your own app's users.
_CONSOLE_ONLY: dict[tuple[str, str], str] = {
    ("POST", "/auth/signup"): "post_projects_by_project_id_auth_signup",
    ("POST", "/auth/forgot-password"): "post_projects_by_project_id_auth_forgot_password",
}


class OperationsBase:
    """Shared request path for every generated operation method.

    ``send`` sends a request to the API as the signed-in user. ``read_signed``
    reads a signed storage link without the API key or the session token; a
    binary operation that the API answers with a redirect to such a link
    returns the link's bytes.
    """

    def __init__(self, send: Send, read_signed: Optional[ReadSigned] = None) -> None:
        self._send = send
        self._read_signed = read_signed

    async def _call(
        self,
        operation: Operation,
        *,
        path: Optional[Mapping[str, Any]],
        query: Optional[Mapping[str, Any]],
        body: Any,
        headers: Optional[Mapping[str, str]],
    ) -> Any:
        project_operation = _CONSOLE_ONLY.get((operation.method, operation.path))
        if project_operation is not None:
            raise VaifConsoleOnlyError(
                operation.name + "()",
                password_reset=operation.path == "/auth/forgot-password",
                own_app="call " + project_operation,
            )
        url_path = build_path(operation.path, path, operation.path_params)
        kwargs: dict[str, Any] = {"params": flatten_query(query), "headers": dict(headers or {})}
        if operation.body == "json":
            if body is not None:
                kwargs["json"] = body
        elif operation.body == "binary":
            kwargs["content"] = body
            kwargs["headers"].setdefault("Content-Type", "application/octet-stream")
        elif operation.body == "text":
            kwargs["content"] = body
            kwargs["headers"].setdefault("Content-Type", "text/plain")
        if operation.transport == "binary" and self._read_signed is not None:
            # The API answers a binary read, such as GET /storage/download,
            # with a redirect to a signed link. The link is read without the
            # API key or the session token, and only over https (http only
            # for loopback hosts).
            kwargs["allow_redirect"] = True
        response = await self._send(operation.method, url_path, **kwargs)
        if operation.transport == "binary":
            if response.is_redirect and self._read_signed is not None:
                link = urljoin(str(response.url), response.headers["location"])
                return await self._read_signed(link)
            return response.content
        if operation.transport == "sse":
            return response
        return response_json(response)


__all__ = ["OperationsBase", "build_path", "flatten_query"]
