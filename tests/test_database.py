from __future__ import annotations

import json

import httpx
import pytest
import respx

from tests.conftest import data_url
from vaifstudio import VaifClient, VaifError, VaifNotFoundError


@respx.mock
async def test_list_serializes_filters_order_select_and_paging(client: VaifClient) -> None:
    route = respx.get(data_url("todos")).mock(
        return_value=httpx.Response(200, json={"data": [{"id": "1"}], "count": 42})
    )
    query = (
        client.from_("todos")
        .select("id", "title")
        .eq("done", False)
        .gte("priority", 2)
        .in_("tag", ["a", "b"])
        .order("created_at", desc=True)
        .order("id")
        .limit(10)
        .offset(20)
    )
    result = await query.list()
    params = route.calls.last.request.url.params
    assert json.loads(params["where"]) == {
        "AND": [
            {"field": "done", "operator": "eq", "value": False},
            {"field": "priority", "operator": "gte", "value": 2},
            {"field": "tag", "operator": "in", "value": ["a", "b"]},
        ]
    }
    assert params["select"] == "id,title"
    assert params["orderBy"] == "created_at,id"
    assert params["orderDir"] == "desc,asc"
    assert params["limit"] == "10"
    assert params["offset"] == "20"
    assert result.data == [{"id": "1"}]
    assert result.count == 42


@respx.mock
async def test_single_filter_is_sent_without_and_wrapper(client: VaifClient) -> None:
    route = respx.get(data_url("todos")).mock(
        return_value=httpx.Response(200, json={"data": [], "count": 0})
    )
    await client.from_("todos").ilike("title", "%milk%").list()
    where = json.loads(route.calls.last.request.url.params["where"])
    assert where == {"field": "title", "operator": "ilike", "value": "%milk%"}


def test_builder_is_immutable(client: VaifClient) -> None:
    base = client.from_("todos").eq("done", False)
    narrowed = base.eq("owner", "u1")
    assert base._where_param() != narrowed._where_param()


def test_rejects_unsafe_identifiers_and_bad_limits(client: VaifClient) -> None:
    with pytest.raises(ValueError):
        client.from_("todos; drop table x")
    with pytest.raises(ValueError):
        client.from_("todos").eq("a b", 1)
    with pytest.raises(ValueError):
        client.from_("todos").limit(0)
    with pytest.raises(ValueError):
        client.from_("todos").limit(1001)
    with pytest.raises(ValueError):
        client.from_("todos").in_("id", [])


@respx.mock
async def test_where_accepts_raw_or_clause(client: VaifClient) -> None:
    route = respx.get(data_url("todos")).mock(
        return_value=httpx.Response(200, json={"data": [], "count": 0})
    )
    clause = {"OR": [{"field": "a", "value": 1}, {"field": "b", "operator": "gt", "value": 2}]}
    await client.from_("todos").where(clause).list()
    assert json.loads(route.calls.last.request.url.params["where"]) == clause


@respx.mock
async def test_paginate_computes_offset_and_page_info(client: VaifClient) -> None:
    route = respx.get(data_url("todos")).mock(
        return_value=httpx.Response(200, json={"data": [{"id": 1}] * 10, "count": 25})
    )
    page = await client.from_("todos").paginate(page=2, page_size=10)
    params = route.calls.last.request.url.params
    assert params["limit"] == "10"
    assert params["offset"] == "10"
    assert (page.total, page.page_count, page.has_next, page.has_previous) == (25, 3, True, True)


@respx.mock
async def test_first_returns_none_when_empty(client: VaifClient) -> None:
    route = respx.get(data_url("todos")).mock(
        return_value=httpx.Response(200, json={"data": [], "count": 0})
    )
    assert await client.from_("todos").first() is None
    assert route.calls.last.request.url.params["limit"] == "1"


@respx.mock
async def test_crud_paths_methods_and_bodies(client: VaifClient) -> None:
    get = respx.get(data_url("todos", "/a%2Fb")).mock(
        return_value=httpx.Response(200, json={"data": {"id": "a/b"}})
    )
    create = respx.post(data_url("todos")).mock(
        return_value=httpx.Response(200, json={"data": {"id": "n1", "title": "x"}})
    )
    update = respx.patch(data_url("todos", "/n1")).mock(
        return_value=httpx.Response(200, json={"data": {"id": "n1", "title": "y"}})
    )
    delete = respx.delete(data_url("todos", "/n1")).mock(
        return_value=httpx.Response(200, json={"data": {"id": "n1"}, "deleted": True})
    )
    bulk = respx.post(data_url("todos", "/bulk")).mock(
        return_value=httpx.Response(200, json={"data": [{"id": 1}, {"id": 2}], "count": 2})
    )

    assert await client.from_("todos").get("a/b") == {"id": "a/b"}
    assert await client.from_("todos").insert({"title": "x"}) == {"id": "n1", "title": "x"}
    assert json.loads(create.calls.last.request.content) == {"title": "x"}
    assert (await client.from_("todos").update("n1", {"title": "y"}))["title"] == "y"
    assert json.loads(update.calls.last.request.content) == {"title": "y"}
    await client.from_("todos").delete("n1")
    rows = await client.from_("todos").insert_many([{"title": "a"}, {"title": "b"}])
    assert json.loads(bulk.calls.last.request.content) == [{"title": "a"}, {"title": "b"}]
    assert len(rows) == 2
    assert get.called and delete.called


@respx.mock
async def test_upsert_sends_control_fields(client: VaifClient) -> None:
    route = respx.post(data_url("profiles")).mock(
        return_value=httpx.Response(200, json={"data": {"id": 1}, "action": "updated"})
    )
    await client.from_("profiles").upsert({"email": "a@b.c", "name": "A"}, on_conflict=["email"])
    assert json.loads(route.calls.last.request.content) == {
        "email": "a@b.c",
        "name": "A",
        "_upsert": True,
        "_conflict_columns": ["email"],
    }


@respx.mock
async def test_get_missing_row_raises_not_found(client: VaifClient) -> None:
    respx.get(data_url("todos", "/nope")).mock(
        return_value=httpx.Response(404, json={"error": "NOT_FOUND", "message": "Record not found"})
    )
    with pytest.raises(VaifNotFoundError):
        await client.from_("todos").get("nope")


@respx.mock
async def test_malformed_success_body_is_an_error(client: VaifClient) -> None:
    respx.post(data_url("todos")).mock(return_value=httpx.Response(200, text="<html>"))
    with pytest.raises(VaifError):
        await client.from_("todos").insert({"title": "x"})
