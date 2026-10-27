"""File storage on the project data plane (``/storage/*``)."""

from __future__ import annotations

from typing import IO, TYPE_CHECKING, Any, Dict, Optional, Union

from vaifstudio._http import check_storage_url, path_segment, response_json
from vaifstudio.exceptions import VaifError
from vaifstudio.types import UploadResult

if TYPE_CHECKING:
    from vaifstudio.client import VaifClient

#: Largest object a single presigned PUT accepts.
MAX_UPLOAD_BYTES = 5 * 1024 * 1024 * 1024

UploadData = Union[bytes, bytearray, memoryview, IO[bytes]]


def _check_key(key: str) -> str:
    if not isinstance(key, str) or not key:
        raise ValueError("key must be a non-empty string")
    if key.startswith("/") or any(part == ".." for part in key.split("/")):
        raise ValueError("key must be relative and must not contain '..' segments")
    if any(ord(ch) < 32 for ch in key):
        raise ValueError("key must not contain control characters")
    return key


def _as_bytes(data: UploadData) -> bytes:
    if isinstance(data, (bytes, bytearray, memoryview)):
        return bytes(data)
    if hasattr(data, "read"):
        chunk = data.read()
        if not isinstance(chunk, (bytes, bytearray)):
            raise TypeError("file objects must be opened in binary mode")
        return bytes(chunk)
    raise TypeError("data must be bytes or a binary file object")


class StorageClient:
    """Upload, download and sign URLs for objects in the project's storage.

    ``bucket`` is optional everywhere; when omitted the API uses the
    project's default bucket. Keys are paths such as ``"avatars/u1.png"``.
    """

    def __init__(self, client: VaifClient) -> None:
        self._client = client

    @staticmethod
    def _target(key: str, bucket: Optional[str]) -> Dict[str, Any]:
        target: Dict[str, Any] = {"key": _check_key(key)}
        if bucket:
            target["bucket"] = bucket
        return target

    async def upload(
        self,
        key: str,
        data: UploadData,
        *,
        content_type: str = "application/octet-stream",
        bucket: Optional[str] = None,
    ) -> UploadResult:
        """Upload an object (overwrites an existing object with the same key).

        Two steps: the API mints a presigned URL
        (``POST /storage/upload-url``, which also meters the bytes), then the
        bytes go straight to the object store with an HTTP ``PUT``. The PUT is
        retried on transient failures; the mint is not, since it is metered.
        """
        body = _as_bytes(data)
        if not body:
            raise ValueError("data must not be empty")
        if len(body) > MAX_UPLOAD_BYTES:
            raise ValueError("upload() accepts at most 5 GB in a single object")
        url = await self.create_signed_upload_url(
            key, size_bytes=len(body), bucket=bucket, content_type=content_type
        )
        await self._client._transport.put_presigned(url, body, content_type)
        return UploadResult(key=key, bucket=bucket, size=len(body))

    async def download(self, key: str, *, bucket: Optional[str] = None) -> bytes:
        """Download an object's bytes. Raises ``VaifNotFoundError`` if missing.

        Two steps, like ``upload()``: the API mints a signed link
        (``POST /storage/download-url``), then the SDK reads it from the file
        host without the API key or the session token.
        """
        url = await self.create_signed_url(key, bucket=bucket)
        return await self._client._transport.get_signed(url)

    async def list(
        self,
        bucket_id: str,
        *,
        prefix: Optional[str] = None,
        limit: int = 100,
        cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """List one bucket by id. Requires a console session with bucket access.

        Returns ``files``, ``prefixes``, ``nextCursor`` and ``hasMore``.
        The API list route requires console authentication; project end-user
        sessions and API keys alone cannot authorize this operation.
        """
        if not bucket_id:
            raise ValueError("bucket_id must not be empty")
        if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 1000:
            raise ValueError("limit must be an integer from 1 to 1000")
        params: Dict[str, Any] = {"maxKeys": limit}
        if prefix is not None:
            params["prefix"] = prefix
        if cursor is not None:
            params["continuationToken"] = cursor
        response = await self._client._send(
            "GET", f"/buckets/{path_segment(bucket_id, 'bucket_id')}/files", params=params
        )
        body = response_json(response)
        if not isinstance(body, dict) or not isinstance(body.get("files"), list):
            raise VaifError("The API response did not include a file list", body=body)
        return {
            "files": body["files"],
            "prefixes": body.get("folders", []),
            "nextCursor": body.get("nextToken"),
            "hasMore": bool(body.get("isTruncated", False)),
        }

    async def delete(self, key: str, *, bucket_id: str) -> None:
        """Delete an object by bucket id. Requires a console session with bucket access."""
        if not bucket_id:
            raise ValueError("bucket_id must not be empty")
        await self._client._send(
            "DELETE",
            f"/buckets/{path_segment(bucket_id, 'bucket_id')}/files",
            params={"key": _check_key(key)},
        )

    async def create_signed_url(
        self, key: str, *, bucket: Optional[str] = None, expires_in: Optional[int] = None
    ) -> str:
        """A time-limited download URL.

        It lives ``expires_in`` seconds when given (1 to 604800, capped at the
        project's maximum), else the project's default lifetime (10 minutes
        unless the project sets another).
        """
        body = self._target(key, bucket)
        if expires_in is not None:
            if (
                isinstance(expires_in, bool)
                or not isinstance(expires_in, int)
                or not 1 <= expires_in <= 604800
            ):
                raise ValueError("expires_in must be a whole number of seconds from 1 to 604800")
            body["expiresIn"] = expires_in
        response = await self._client._send(
            "POST", "/storage/download-url", json=body, idempotent=True
        )
        return self._url(response_json(response))

    async def create_signed_upload_url(
        self,
        key: str,
        *,
        size_bytes: int,
        bucket: Optional[str] = None,
        content_type: Optional[str] = None,
    ) -> str:
        """A time-limited URL that accepts an HTTP ``PUT`` of the object's bytes.

        The URL is signed for exactly ``size_bytes`` bytes (sent as
        ``sizeBytes``) and, when ``content_type`` is given (sent as
        ``contentType``), exactly that ``Content-Type``: the ``PUT`` must send
        both as signed or the object store refuses it. The API checks the size
        against the bucket's and project's limits and the storage quota, and
        meters it. Buckets with ``allowedMimeTypes`` reject a mint without
        ``content_type``.
        """
        if (
            isinstance(size_bytes, bool)
            or not isinstance(size_bytes, int)
            or not 1 <= size_bytes <= MAX_UPLOAD_BYTES
        ):
            raise ValueError("size_bytes must be an integer from 1 to 5 GB")
        payload = self._target(key, bucket)
        payload["sizeBytes"] = size_bytes
        if content_type:
            payload["contentType"] = content_type
        response = await self._client._send("POST", "/storage/upload-url", json=payload)
        return self._url(response_json(response))

    @staticmethod
    def _url(body: Any) -> str:
        if isinstance(body, dict) and isinstance(body.get("url"), str):
            return check_storage_url(str(body["url"]))
        raise VaifError("The API response did not include a URL", body=body)
