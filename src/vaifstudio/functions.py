"""Invoke deployed functions (``POST /functions/:name/invoke``)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional

from vaifstudio._http import path_segment
from vaifstudio.types import FunctionResponse

if TYPE_CHECKING:
    from vaifstudio.client import VaifClient

_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}


class FunctionsClient:
    """Call the project's functions by name or id."""

    def __init__(self, client: VaifClient) -> None:
        self._client = client

    async def invoke(
        self,
        name: str,
        body: Any = None,
        *,
        method: str = "POST",
        path: str = "/",
        query: Optional[Mapping[str, str]] = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Optional[float] = None,
        idempotent: bool = False,
    ) -> FunctionResponse:
        """Invoke a function and return its HTTP response.

        ``method``, ``path``, ``query`` and ``headers`` are what the function
        itself sees. Non-2xx responses raise the matching ``VaifError``
        subclass with the function's body in ``error.body`` and its headers in
        ``error.headers``. A request that may have reached the function is
        not sent again unless ``idempotent=True``. When the API refuses the
        session token with HTTP 401, which it does before the function runs,
        the session is refreshed and the invocation is sent once more. A 401
        from the function itself is raised as it is.
        """
        if not name:
            raise ValueError("name must not be empty")
        verb = method.upper()
        if verb not in _METHODS:
            raise ValueError(f"method must be one of {sorted(_METHODS)}")
        if not path.startswith("/"):
            raise ValueError("path must start with '/'")
        # Always send the envelope form: a raw body that happened to contain a
        # "method" or "path" key would otherwise be misread as an envelope.
        envelope: Dict[str, Any] = {"method": verb, "path": path}
        if query:
            envelope["query"] = {str(k): str(v) for k, v in query.items()}
        if headers:
            envelope["headers"] = {str(k): str(v) for k, v in headers.items()}
        if body is not None:
            envelope["body"] = body
        response = await self._client._send(
            "POST",
            f"/functions/{path_segment(name, 'name')}/invoke",
            json=envelope,
            timeout=timeout,
            idempotent=idempotent,
        )
        content_type = response.headers.get("content-type", "")
        data: Any
        if not response.content:
            data = None
        elif "json" in content_type:
            try:
                data = response.json()
            except ValueError:
                data = response.text
        elif content_type.startswith("text/"):
            data = response.text
        else:
            data = response.content
        return FunctionResponse(
            status=response.status_code, headers=dict(response.headers), data=data
        )
