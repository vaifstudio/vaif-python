"""Verament's plan card from the Python SDK: what each call sends, and what a refusal raises.

A build request is answered with its plan card; a server confirms or cancels it
on the non-streaming routes (POST /ai/copilot/chat, or POST /ai/copilot/job for
a background build), with the plan's session and the message it was made for,
or skips it for automation with autoConfirm.
"""

from __future__ import annotations

import json
from typing import Dict, List, Optional, get_type_hints

import httpx
import pytest
import respx

from tests.conftest import BASE
from vaifstudio import CopilotClient, VaifClient, VaifConflictError, VaifError, VaifNotFoundError
from vaifstudio.copilot import (
    BUILD_TIMEOUT_SECONDS,
    DocsChoice,
    PlanAssumption,
    PlanCard,
    PlanDocs,
    PlanDocsKind,
    PlanEngine,
    blueprint_engine_offer,
    pending_plan_of,
)

PLAN_ID = "11111111-1111-4111-8111-111111111111"
SESSION = "22222222-2222-4222-8222-222222222222"
PROJECT = "33333333-3333-4333-8333-333333333333"
MESSAGE = "tables for a todo list"
TOKEN = "account_token"


def sent(route: respx.Route) -> dict:
    return json.loads(route.calls.last.request.content)


@respx.mock
async def test_chat_sends_auto_confirm_with_the_account_token(client: VaifClient) -> None:
    route = respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(
            200,
            json={
                "ok": True,
                "sessionId": SESSION,
                "preflightRequired": {"kind": "plan", "plan": {"planId": PLAN_ID}},
            },
        )
    )
    result = await client.copilot(TOKEN).chat(
        PROJECT, MESSAGE, generation_types=["schema"], auto_confirm_max_credits=25
    )
    assert sent(route) == {
        "projectId": PROJECT,
        "message": MESSAGE,
        "generationTypes": ["schema"],
        "autoConfirm": {"maxCredits": 25},
    }
    assert route.calls.last.request.headers["authorization"] == f"Bearer {TOKEN}"
    assert result["preflightRequired"]["plan"]["planId"] == PLAN_ID


@respx.mock
async def test_chat_waits_as_long_as_a_build_only_with_auto_confirm(client: VaifClient) -> None:
    route = respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(200, json={"ok": True, "sessionId": SESSION})
    )
    copilot = client.copilot(TOKEN)
    await copilot.chat(PROJECT, MESSAGE, auto_confirm_max_credits=25)
    # The build may run in an auto-confirmed call.
    assert route.calls.last.request.extensions["timeout"]["read"] == BUILD_TIMEOUT_SECONDS
    await copilot.chat(PROJECT, MESSAGE)
    assert route.calls.last.request.extensions["timeout"]["read"] == 120.0
    await copilot.chat(PROJECT, MESSAGE, auto_confirm_max_credits=25, timeout=30.0)
    assert route.calls.last.request.extensions["timeout"]["read"] == 30.0


async def test_chat_refuses_a_ceiling_that_is_not_a_positive_whole_number(
    client: VaifClient,
) -> None:
    for bad in (0, -5, 2.5):
        with pytest.raises(ValueError):
            await client.copilot(TOKEN).chat(PROJECT, MESSAGE, auto_confirm_max_credits=bad)  # type: ignore[arg-type]


@respx.mock
async def test_confirm_plan_posts_the_plan_id_in_its_session_with_its_message(
    client: VaifClient,
) -> None:
    route = respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(
            200,
            json={
                "ok": True,
                "sessionId": SESSION,
                "planId": PLAN_ID,
                "manifestId": "m1",
                "response": {
                    "type": "generation",
                    "content": "",
                    "artifacts": {"files": [{"path": "a.sql", "content": "x"}]},
                },
                "context": {"creditsCharged": 12, "tokensUsed": 900},
                "build": {
                    "status": "completed",
                    "totalFiles": 1,
                    "totalBatches": 1,
                    "durationSeconds": 2,
                    "warnings": [],
                },
            },
        )
    )
    built = await client.copilot(TOKEN).confirm_plan(
        PROJECT, SESSION, PLAN_ID, MESSAGE, generation_types=["schema"]
    )
    assert sent(route) == {
        "projectId": PROJECT,
        "sessionId": SESSION,
        "message": MESSAGE,
        "generationTypes": ["schema"],
        "preflight": {"confirmPlanId": PLAN_ID},
    }
    assert built["response"]["artifacts"]["files"][0]["path"] == "a.sql"
    assert route.call_count == 1


@respx.mock
async def test_confirm_plan_with_a_credit_choice_sends_it_with_the_confirm(
    client: VaifClient,
) -> None:
    route = respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    await client.copilot(TOKEN).confirm_plan(
        PROJECT, SESSION, PLAN_ID, MESSAGE, credit_choice="until_zero"
    )
    assert sent(route)["preflight"] == {"confirmPlanId": PLAN_ID, "creditChoice": "until_zero"}
    with pytest.raises(ValueError):
        await client.copilot(TOKEN).confirm_plan(
            PROJECT, SESSION, PLAN_ID, MESSAGE, credit_choice="stop"
        )  # type: ignore[arg-type]


def envelope(status: int, code: str, **extra: object) -> dict:
    """The copilot error envelope the API answers a refused confirm with."""
    text = f"server copy for {code}"
    return {
        "error": {"code": code, "message": text, "statusCode": status, "retryable": False},
        "message": text,
        **extra,
    }


@pytest.mark.parametrize(
    ("status", "code", "error_type"),
    [
        (404, "PLAN_NOT_FOUND", VaifNotFoundError),
        (409, "PLAN_ALREADY_CONFIRMED", VaifConflictError),
        (409, "PLAN_STALE", VaifConflictError),
        (410, "PLAN_EXPIRED", VaifError),
    ],
)
@respx.mock
async def test_a_refused_confirm_raises_with_its_code_and_is_sent_once(
    client: VaifClient, status: int, code: str, error_type: type
) -> None:
    route = respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(status, json=envelope(status, code))
    )
    with pytest.raises(error_type) as raised:
        await client.copilot(TOKEN).confirm_plan(PROJECT, SESSION, PLAN_ID, MESSAGE)
    assert raised.value.status == status
    assert raised.value.code == code
    assert str(raised.value) == f"server copy for {code}"
    assert route.call_count == 1


@respx.mock
async def test_a_confirm_envelope_without_a_top_level_message_keeps_the_nested_one(
    client: VaifClient,
) -> None:
    respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(
            410,
            json={
                "error": {
                    "code": "PLAN_EXPIRED",
                    "message": "This plan expired.",
                    "statusCode": 410,
                }
            },
        )
    )
    with pytest.raises(VaifError) as raised:
        await client.copilot(TOKEN).confirm_plan(PROJECT, SESSION, PLAN_ID, MESSAGE)
    assert (raised.value.code, str(raised.value)) == ("PLAN_EXPIRED", "This plan expired.")


@respx.mock
async def test_a_confirm_is_never_replayed_even_on_a_503(client: VaifClient) -> None:
    route = respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(503, json=envelope(503, "AI_AT_CAPACITY"))
    )
    with pytest.raises(VaifError) as raised:
        await client.copilot(TOKEN).confirm_plan(PROJECT, SESSION, PLAN_ID, MESSAGE)
    assert raised.value.code == "AI_AT_CAPACITY"
    assert route.call_count == 1


@respx.mock
async def test_a_failed_build_keeps_its_files_and_resume_token_on_the_error(
    client: VaifClient,
) -> None:
    files = [{"path": "src/schema/todos.sql", "content": "CREATE TABLE todos ();"}]
    respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(
            502,
            json=envelope(
                502,
                "AI_PROVIDER_ERROR",
                files=files,
                checkpoint={"id": "c1", "resumeToken": "resume-1"},
            ),
        )
    )
    with pytest.raises(VaifError) as raised:
        await client.copilot(TOKEN).confirm_plan(PROJECT, SESSION, PLAN_ID, MESSAGE)
    assert raised.value.code == "AI_PROVIDER_ERROR"
    assert raised.value.body["files"] == files
    assert raised.value.body["checkpoint"]["resumeToken"] == "resume-1"


@respx.mock
async def test_cancel_plan_posts_cancel_plan_id(client: VaifClient) -> None:
    route = respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(
            200,
            json={
                "ok": True,
                "sessionId": SESSION,
                "planId": PLAN_ID,
                "stopped": True,
                "creditsCharged": 0,
            },
        )
    )
    result = await client.copilot(TOKEN).cancel_plan(PROJECT, SESSION, PLAN_ID, MESSAGE)
    assert sent(route) == {
        "projectId": PROJECT,
        "sessionId": SESSION,
        "message": MESSAGE,
        "preflight": {"cancelPlanId": PLAN_ID},
    }
    assert result["stopped"] is True


@respx.mock
async def test_queue_confirm_plan_and_get_job(client: VaifClient) -> None:
    queue = respx.post(f"{BASE}/ai/copilot/job").mock(
        return_value=httpx.Response(200, json={"ok": True, "jobId": "j1", "status": "queued"})
    )
    status = respx.get(f"{BASE}/ai/copilot/job/j1").mock(
        return_value=httpx.Response(
            200,
            json={
                "jobId": "j1",
                "status": "completed",
                "result": {"status": "completed", "planId": PLAN_ID, "files": []},
            },
        )
    )
    copilot = client.copilot(TOKEN)
    job = await copilot.queue_confirm_plan(PROJECT, SESSION, PLAN_ID, MESSAGE)
    assert sent(queue)["preflight"] == {"confirmPlanId": PLAN_ID}
    assert job["jobId"] == "j1"
    done = await copilot.get_job("j1")
    assert done["result"]["planId"] == PLAN_ID
    assert status.calls.last.request.headers["authorization"] == f"Bearer {TOKEN}"


@respx.mock
async def test_get_session_returns_the_waiting_card(client: VaifClient) -> None:
    respx.get(f"{BASE}/ai/copilot/session/{SESSION}").mock(
        return_value=httpx.Response(
            200,
            json={
                "session": {"id": SESSION},
                "messages": [],
                "pendingPlan": {
                    "kind": "plan",
                    "plan": {"planId": PLAN_ID},
                    "messageId": "m1",
                    "prompt": MESSAGE,
                },
            },
        )
    )
    session = await client.copilot(TOKEN).get_session(SESSION)
    pending = pending_plan_of(session)
    assert (
        pending is not None
        and pending["plan"]["planId"] == PLAN_ID
        and pending["prompt"] == MESSAGE
    )
    assert pending_plan_of({"pendingPlan": None}) is None


def test_copilot_needs_an_account_token(client: VaifClient) -> None:
    with pytest.raises(ValueError):
        CopilotClient(client, "")


# Verament engines and effort: a request names a tier and an effort by id, the
# plan card names the engine its confirm builds, and a tier or effort above the
# plan is a 403 offer. Values hand-typed from the spec.


@respx.mock
async def test_chat_sends_tier_and_effort_by_id_and_omits_them_when_unset(
    client: VaifClient,
) -> None:
    route = respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(200, json={"ok": True, "sessionId": SESSION})
    )
    copilot = client.copilot(TOKEN)
    await copilot.chat(PROJECT, MESSAGE, tier="max", effort="deep")
    assert sent(route) == {
        "projectId": PROJECT,
        "message": MESSAGE,
        "tier": "max",
        "effort": "deep",
    }
    await copilot.chat(PROJECT, MESSAGE)
    assert sent(route) == {"projectId": PROJECT, "message": MESSAGE}


@respx.mock
async def test_a_confirm_sends_no_tier_or_effort_so_the_plans_own_is_built(
    client: VaifClient,
) -> None:
    chat = respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(200, json={"ok": True, "sessionId": SESSION})
    )
    job = respx.post(f"{BASE}/ai/copilot/job").mock(
        return_value=httpx.Response(200, json={"ok": True, "jobId": "j1"})
    )
    copilot = client.copilot(TOKEN)
    await copilot.confirm_plan(PROJECT, SESSION, PLAN_ID, MESSAGE)
    await copilot.queue_confirm_plan(PROJECT, SESSION, PLAN_ID, MESSAGE)
    for route in (chat, job):
        assert sorted(sent(route)) == ["message", "preflight", "projectId", "sessionId"]


def test_the_plan_card_names_its_engine() -> None:
    assert get_type_hints(PlanCard)["engine"] == Optional[PlanEngine]
    assert sorted(get_type_hints(PlanEngine)) == ["effort", "effortLabel", "tier", "tierLabel"]


OFFER = {
    "error": "UpgradeRequired",
    "code": "BLUEPRINT_TIER_NOT_IN_PLAN",
    "suggestedPlan": "studio_plus",
    "message": "Verament Max 1.0 is not included in your Pro plan, which includes Verament Lite 1.0 and Verament Standard 1.0 at Quick, Balanced or Deep effort. Studio+ includes it.",
    "allowed": {"tiers": ["lite", "standard"], "efforts": ["quick", "balanced", "deep"]},
    "retryWith": {"tier": "standard", "effort": "deep"},
}


@respx.mock
async def test_blueprint_engine_offer_reads_a_tier_or_effort_refusal(client: VaifClient) -> None:
    route = respx.post(f"{BASE}/ai/copilot/chat").mock(return_value=httpx.Response(403, json=OFFER))
    with pytest.raises(VaifError) as raised:
        await client.copilot(TOKEN).chat(PROJECT, MESSAGE, tier="max")
    assert blueprint_engine_offer(raised.value) == {
        "code": "BLUEPRINT_TIER_NOT_IN_PLAN",
        "message": OFFER["message"],
        "suggestedPlan": "studio_plus",
        "allowed": {"tiers": ["lite", "standard"], "efforts": ["quick", "balanced", "deep"]},
        "retryWith": {"tier": "standard", "effort": "deep"},
    }

    route.mock(
        return_value=httpx.Response(403, json={**OFFER, "code": "BLUEPRINT_EFFORT_NOT_IN_PLAN"})
    )
    with pytest.raises(VaifError) as effort:
        await client.copilot(TOKEN).chat(PROJECT, MESSAGE, effort="extended")
    offer = blueprint_engine_offer(effort.value)
    assert offer is not None and offer["code"] == "BLUEPRINT_EFFORT_NOT_IN_PLAN"

    # The offer's message is the body's, whatever the error wrapping it says.
    wrapped = VaifError("wrapped", status=403, code="BLUEPRINT_TIER_NOT_IN_PLAN", body=OFFER)
    wrapped_offer = blueprint_engine_offer(wrapped)
    assert wrapped_offer is not None and wrapped_offer["message"] == OFFER["message"]


def test_blueprint_engine_offer_is_none_for_any_other_error() -> None:
    no_retry_effort = {**OFFER, "retryWith": {"tier": "standard"}}
    other_code = {**OFFER, "code": "PLAN_UPGRADE_REQUIRED"}
    for error in (
        VaifError(
            "x",
            status=403,
            code="PLAN_UPGRADE_REQUIRED",
            body={"error": "UpgradeRequired", "code": "PLAN_UPGRADE_REQUIRED"},
        ),
        VaifError("x", status=403, code="BLUEPRINT_TIER_NOT_IN_PLAN", body=no_retry_effort),
        VaifError("x", status=403, code="PLAN_UPGRADE_REQUIRED", body=other_code),
        VaifError("x", status=403, code="BLUEPRINT_TIER_NOT_IN_PLAN", body=None),
        ValueError("x"),
        None,
    ):
        assert blueprint_engine_offer(error) is None


def test_the_plan_card_carries_its_assumptions_and_provided_files() -> None:
    hints = get_type_hints(PlanCard)
    assert hints["assumptions"] == List[PlanAssumption]
    assert hints["provided"] == List[Dict[str, str]]
    assert sorted(get_type_hints(PlanAssumption)) == ["choice", "id", "options", "text", "topic"]


@respx.mock
async def test_a_confirm_sends_the_cards_changed_choices(client: VaifClient) -> None:
    chat = respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    job = respx.post(f"{BASE}/ai/copilot/job").mock(
        return_value=httpx.Response(200, json={"jobId": "j1"})
    )
    copilot = client.copilot(TOKEN)
    await copilot.confirm_plan(
        PROJECT, SESSION, PLAN_ID, MESSAGE, assumption_choices={"a1": "assets"}
    )
    assert sent(chat)["preflight"] == {
        "confirmPlanId": PLAN_ID,
        "assumptionChoices": {"a1": "assets"},
    }
    await copilot.queue_confirm_plan(
        PROJECT, SESSION, PLAN_ID, MESSAGE, assumption_choices={"a1": "assets"}
    )
    assert sent(job)["preflight"] == {
        "confirmPlanId": PLAN_ID,
        "assumptionChoices": {"a1": "assets"},
    }


@respx.mock
async def test_replan_plans_the_same_message_again_with_choices_that_change_files(
    client: VaifClient,
) -> None:
    route = respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    await client.copilot(TOKEN).replan(PROJECT, SESSION, MESSAGE, {"a1": "create:media"})
    assert sent(route) == {
        "projectId": PROJECT,
        "sessionId": SESSION,
        "message": MESSAGE,
        "preflight": {"assumptionChoices": {"a1": "create:media"}},
    }
    with pytest.raises(ValueError):
        await client.copilot(TOKEN).replan(PROJECT, SESSION, MESSAGE, {})


@respx.mock
async def test_plan_with_defaults_resends_the_question_message_to_plan_without_asking(
    client: VaifClient,
) -> None:
    route = respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    await client.copilot(TOKEN).plan_with_defaults(PROJECT, SESSION, MESSAGE)
    assert sent(route) == {
        "projectId": PROJECT,
        "sessionId": SESSION,
        "message": MESSAGE,
        "preflight": {"planWithDefaults": True},
    }


# The plan card's docs choice: the README is written for free; a card's docs
# row offers more, each priced into the maximum, and a confirm sends the kinds
# chosen. Values hand-typed from the API's card.


def test_the_plan_card_carries_its_docs_row() -> None:
    assert get_type_hints(PlanCard)["docs"] == Optional[PlanDocs]
    assert sorted(get_type_hints(PlanDocs)) == [
        "defaultChoice",
        "kinds",
        "maximumCredits",
        "noteMax",
        "selections",
    ]
    assert get_type_hints(PlanDocs)["maximumCredits"] == Optional[Dict[str, int]]
    assert get_type_hints(PlanDocs)["selections"] == List[str]
    assert sorted(get_type_hints(PlanDocsKind)) == ["id", "label", "suggested"]
    assert sorted(get_type_hints(DocsChoice)) == ["kinds", "note"]


@respx.mock
async def test_a_confirm_sends_the_cards_docs_choice(client: VaifClient) -> None:
    chat = respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    job = respx.post(f"{BASE}/ai/copilot/job").mock(
        return_value=httpx.Response(200, json={"jobId": "j1"})
    )
    copilot = client.copilot(TOKEN)
    await copilot.confirm_plan(
        PROJECT,
        SESSION,
        PLAN_ID,
        MESSAGE,
        docs={"kinds": ["api", "custom"], "note": "a deploy checklist"},
    )
    assert sent(chat)["preflight"] == {
        "confirmPlanId": PLAN_ID,
        "docs": {"kinds": ["api", "custom"], "note": "a deploy checklist"},
    }
    await copilot.queue_confirm_plan(
        PROJECT, SESSION, PLAN_ID, MESSAGE, credit_choice="smaller", docs={"kinds": ["guide"]}
    )
    assert sent(job)["preflight"] == {
        "confirmPlanId": PLAN_ID,
        "creditChoice": "smaller",
        "docs": {"kinds": ["guide"]},
    }
    await copilot.confirm_plan(PROJECT, SESSION, PLAN_ID, MESSAGE)
    assert sent(chat)["preflight"] == {"confirmPlanId": PLAN_ID}


@respx.mock
async def test_a_docs_choice_without_kinds_is_refused_before_anything_is_sent(
    client: VaifClient,
) -> None:
    chat = respx.post(f"{BASE}/ai/copilot/chat").mock(
        return_value=httpx.Response(200, json={"ok": True})
    )
    with pytest.raises(ValueError):
        await client.copilot(TOKEN).confirm_plan(
            PROJECT, SESSION, PLAN_ID, MESSAGE, docs={"kinds": []}
        )
    assert not chat.called
