"""Table queries against the data plane (``/v1/data/:projectId/:table``)."""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Sequence, Tuple

from vaifstudio._http import path_segment, response_json
from vaifstudio.exceptions import VaifError
from vaifstudio.types import ListResult, Page, Row

if TYPE_CHECKING:
    from vaifstudio.client import VaifClient

_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
#: Server-side cap on ``limit`` (larger values return ``LIMIT_TOO_HIGH``).
MAX_LIMIT = 1000


def _identifier(value: str, what: str) -> str:
    if not isinstance(value, str) or not _IDENTIFIER.match(value):
        raise ValueError(f"{what} must be a SQL identifier (letters, digits, _), got {value!r}")
    return value


class QueryBuilder:
    """Immutable, chainable query against one table.

    Every filter method returns a new builder, so a base query can be reused::

        active = vaif.from_("todos").eq("done", False)
        page = await active.order("created_at", desc=True).limit(20).list()
    """

    def __init__(
        self,
        client: VaifClient,
        table: str,
        *,
        filters: Tuple[Mapping[str, Any], ...] = (),
        order: Tuple[Tuple[str, bool], ...] = (),
        columns: Optional[Tuple[str, ...]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> None:
        self._client = client
        self._table = _identifier(table, "table")
        self._filters = filters
        self._order = order
        self._columns = columns
        self._limit = limit
        self._offset = offset

    def _copy(self, **changes: Any) -> QueryBuilder:
        state: Dict[str, Any] = {
            "filters": self._filters,
            "order": self._order,
            "columns": self._columns,
            "limit": self._limit,
            "offset": self._offset,
        }
        state.update(changes)
        return QueryBuilder(self._client, self._table, **state)

    # ------------------------------------------------------------- filters

    def _clause(self, column: str, operator: str, value: Any) -> QueryBuilder:
        clause = {"field": _identifier(column, "column"), "operator": operator, "value": value}
        return self._copy(filters=self._filters + (clause,))

    def eq(self, column: str, value: Any) -> QueryBuilder:
        return self._clause(column, "eq", value)

    def neq(self, column: str, value: Any) -> QueryBuilder:
        return self._clause(column, "neq", value)

    def gt(self, column: str, value: Any) -> QueryBuilder:
        return self._clause(column, "gt", value)

    def gte(self, column: str, value: Any) -> QueryBuilder:
        return self._clause(column, "gte", value)

    def lt(self, column: str, value: Any) -> QueryBuilder:
        return self._clause(column, "lt", value)

    def lte(self, column: str, value: Any) -> QueryBuilder:
        return self._clause(column, "lte", value)

    def like(self, column: str, pattern: str) -> QueryBuilder:
        return self._clause(column, "like", pattern)

    def ilike(self, column: str, pattern: str) -> QueryBuilder:
        return self._clause(column, "ilike", pattern)

    def in_(self, column: str, values: Sequence[Any]) -> QueryBuilder:
        values = list(values)
        if not values:
            raise ValueError("in_() needs at least one value")
        return self._clause(column, "in", values)

    def where(self, clause: Mapping[str, Any]) -> QueryBuilder:
        """Add a raw clause, e.g. ``{"OR": [{"field": "a", "value": 1}, ...]}``.

        Clauses are ANDed with the other filters on the builder.
        """
        return self._copy(filters=self._filters + (dict(clause),))

    # ----------------------------------------------------------- modifiers

    def select(self, *columns: str) -> QueryBuilder:
        """Return only these columns (default: all)."""
        return self._copy(columns=tuple(_identifier(c, "column") for c in columns) or None)

    def order(self, column: str, *, desc: bool = False) -> QueryBuilder:
        """Sort by ``column``; call again to add secondary sort keys."""
        return self._copy(order=self._order + ((_identifier(column, "column"), desc),))

    def limit(self, count: int) -> QueryBuilder:
        if count < 1 or count > MAX_LIMIT:
            raise ValueError(f"limit must be between 1 and {MAX_LIMIT}")
        return self._copy(limit=count)

    def offset(self, count: int) -> QueryBuilder:
        if count < 0:
            raise ValueError("offset must be >= 0")
        return self._copy(offset=count)

    def range(self, start: int, end: int) -> QueryBuilder:
        """Select an inclusive, zero-based range of rows (at most 1000)."""
        if (
            isinstance(start, bool)
            or not isinstance(start, int)
            or isinstance(end, bool)
            or not isinstance(end, int)
            or start < 0
            or end < start
        ):
            raise ValueError("range needs integer bounds with 0 <= start <= end")
        return self.offset(start).limit(end - start + 1)

    async def count(self) -> int:
        """Return the API's total match count, fetching at most one row."""
        return (await self._copy(limit=1, offset=0).list()).count

    # -------------------------------------------------------- serializing

    def _where_param(self) -> Optional[str]:
        if not self._filters:
            return None
        tree: Any = self._filters[0] if len(self._filters) == 1 else {"AND": list(self._filters)}
        return json.dumps(tree, separators=(",", ":"), default=str)

    def _params(
        self, *, limit: Optional[int] = None, offset: Optional[int] = None
    ) -> Dict[str, Any]:
        params: Dict[str, Any] = {}
        where = self._where_param()
        if where is not None:
            params["where"] = where
        if self._columns:
            params["select"] = ",".join(self._columns)
        if self._order:
            params["orderBy"] = ",".join(col for col, _ in self._order)
            params["orderDir"] = ",".join("desc" if desc else "asc" for _, desc in self._order)
        final_limit = limit if limit is not None else self._limit
        final_offset = offset if offset is not None else self._offset
        if final_limit is not None:
            params["limit"] = final_limit
        if final_offset is not None:
            params["offset"] = final_offset
        return params

    @property
    def _base(self) -> str:
        return f"/v1/data/{path_segment(self._client.project_id, 'project_id')}/{self._table}"

    def _row_path(self, row_id: Any) -> str:
        text = str(row_id)
        if not text:
            raise ValueError("id must not be empty")
        return f"{self._base}/{path_segment(text, 'id')}"

    # ----------------------------------------------------------- terminals

    async def list(self) -> ListResult:
        """Fetch matching rows plus the total match count."""
        response = await self._client._send("GET", self._base, params=self._params())
        body = response_json(response) or {}
        data = body.get("data") or []
        count = body.get("count")
        return ListResult(data=list(data), count=int(count) if count is not None else len(data))

    async def first(self) -> Optional[Row]:
        """The first matching row, or ``None``."""
        result = await self._copy(limit=1).list()
        return result.data[0] if result.data else None

    async def paginate(self, page: int = 1, page_size: int = 20) -> Page:
        """Offset pagination; ``page`` starts at 1."""
        if page < 1:
            raise ValueError("page must be >= 1")
        if page_size < 1 or page_size > MAX_LIMIT:
            raise ValueError(f"page_size must be between 1 and {MAX_LIMIT}")
        response = await self._client._send(
            "GET", self._base, params=self._params(limit=page_size, offset=(page - 1) * page_size)
        )
        body = response_json(response) or {}
        data = list(body.get("data") or [])
        total = body.get("count")
        return Page(
            data=data,
            total=int(total) if total is not None else len(data),
            page=page,
            page_size=page_size,
        )

    async def get(self, row_id: Any) -> Row:
        """Fetch one row by primary key. Raises ``VaifNotFoundError`` if missing."""
        params = {"select": ",".join(self._columns)} if self._columns else None
        response = await self._client._send("GET", self._row_path(row_id), params=params)
        return self._row(response_json(response))

    async def insert(self, values: Mapping[str, Any]) -> Row:
        """Insert one row and return it."""
        response = await self._client._send("POST", self._base, json=dict(values))
        return self._row(response_json(response))

    async def insert_many(self, rows: Sequence[Mapping[str, Any]]) -> List[Row]:
        """Insert rows in one request (all rows must share the same keys)."""
        if not rows:
            return []
        response = await self._client._send(
            "POST", f"{self._base}/bulk", json=[dict(r) for r in rows]
        )
        body = response_json(response) or {}
        return list(body.get("data") or [])

    async def upsert(self, values: Mapping[str, Any], *, on_conflict: Sequence[str]) -> Row:
        """Insert, or update the row that conflicts on ``on_conflict`` columns."""
        columns = [_identifier(c, "column") for c in on_conflict]
        if not columns:
            raise ValueError("upsert needs at least one on_conflict column")
        payload = dict(values)
        payload["_upsert"] = True
        payload["_conflict_columns"] = columns
        response = await self._client._send("POST", self._base, json=payload)
        return self._row(response_json(response))

    async def update(self, row_id: Any, values: Mapping[str, Any]) -> Row:
        """Update one row by primary key and return it."""
        response = await self._client._send("PATCH", self._row_path(row_id), json=dict(values))
        return self._row(response_json(response))

    async def delete(self, row_id: Any) -> None:
        """Delete one row by primary key."""
        await self._client._send("DELETE", self._row_path(row_id))

    @staticmethod
    def _row(body: Any) -> Row:
        if isinstance(body, dict) and isinstance(body.get("data"), dict):
            return dict(body["data"])
        raise VaifError("The API response did not include a row", body=body)
