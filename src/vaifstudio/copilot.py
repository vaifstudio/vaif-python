"""VAIF Verament from a server: the plan card, confirmed or canceled without a stream.

A build request is answered with its PLAN CARD: the planning call ran and is
charged (the card shows it); nothing is built, and the build is not charged,
until the plan is confirmed. A server-side caller has no browser for the
streaming route, so it answers the card here:

- :meth:`CopilotClient.confirm_plan` builds the plan and returns once the
  build is over (files under ``response.artifacts.files``);
- :meth:`CopilotClient.queue_confirm_plan` builds it in the background; poll
  :meth:`CopilotClient.get_job` for the result;
- :meth:`CopilotClient.cancel_plan` drops it (nothing more is charged).

For automation, ``chat(..., auto_confirm_max_credits=N)`` builds in the same
call when the whole run costs at most N credits, and otherwise returns the card
marked refused. A plan can be confirmed once, for 30 minutes, in its session,
with the message it was made for.

ENGINES AND EFFORT. VAIF Verament runs on three engines: Verament Lite 1.0
(VAIF's AI engine for quick builds and edits), Verament Standard 1.0 (VAIF's
AI engine for full backend generation) and Verament Max 1.0 (VAIF's AI engine
at full strength, for the hardest runs), each at Quick, Balanced, Deep or
Extended effort. ``chat(..., tier="standard", effort="deep")`` names them;
omitted, the plan's defaults apply. The card's ``engine`` is what its confirm
builds, and a confirm names none. A tier or effort the plan does not include is
refused with a 403 before any model call: :func:`blueprint_engine_offer` reads
what the plan allows and what to retry with. A deeper effort uses more tokens,
so more credits, at the same rate per token.

Verament acts for your VAIF account, not a project end user: pass the
account's access token. The project key is sent as on every other call.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, TypedDict, Union, cast

from vaifstudio._http import path_segment, response_json

if TYPE_CHECKING:
    from vaifstudio.client import VaifClient

#: How long :meth:`CopilotClient.confirm_plan` waits: the whole build runs before the answer.
BUILD_TIMEOUT_SECONDS = 15 * 60.0

CreditChoiceAnswer = Literal["smaller", "until_zero"]

#: A Verament engine, by id: Verament Lite 1.0, Standard 1.0 or Max 1.0.
BlueprintTier = Literal["lite", "standard", "max"]

#: A Verament effort level, by id: Quick, Balanced, Deep or Extended.
BlueprintEffort = Literal["quick", "balanced", "deep", "extended"]

_ENGINE_OFFER_CODES = ("BLUEPRINT_TIER_NOT_IN_PLAN", "BLUEPRINT_EFFORT_NOT_IN_PLAN")


class PlanEngine(TypedDict):
    """The engine a plan card's confirm builds, with its names ("Verament Standard 1.0", "Deep").

    The card's ``maximumCredits`` includes that effort's larger token allowance."""

    tier: BlueprintTier
    tierLabel: str
    effort: BlueprintEffort
    effortLabel: str


class EngineOffer(TypedDict):
    """A tier or effort above the org's plan. Nothing was charged.

    ``allowed`` is what the plan includes, ``retryWith`` the closest engine it
    includes (send the request again with it), and ``suggestedPlan`` the plan
    that includes what was asked."""

    code: str
    message: str
    suggestedPlan: str
    allowed: Dict[str, List[str]]
    retryWith: Dict[str, str]


class CreditChoice(TypedDict, total=False):
    """The balance is below the run's maximum: answer a confirm with a ``credit_choice``."""

    scope: Literal["planning", "run"]
    maximumCredits: int
    remainingCredits: int
    upgradePlan: Optional[Dict[str, str]]
    smallerRun: Optional[Dict[str, int]]
    untilZero: Optional[Dict[str, int]]


class PlanAssumption(TypedDict):
    """An open choice a plan made instead of asking, with the options the server offers.

    Changing to an option with ``affects: "code"`` is free at confirm
    (``confirm_plan(..., assumption_choices=...)``); one with ``affects: "files"``
    makes a new plan (:meth:`CopilotClient.replan`), and planning is charged again.
    """

    id: str
    #: "storage", "realtime", "auth", "events", "data", "access" or "other".
    topic: str
    text: str
    #: The option value the plan uses.
    choice: str
    options: List[Dict[str, str]]


#: A docs kind a plan card offers: API reference, user guide, architecture
#: notes, or something else described by a note ("custom").
DocsKind = Literal["api", "guide", "architecture", "custom"]


class PlanDocsKind(TypedDict):
    """One kind on the card's docs row.

    ``suggested`` marks a kind the plan itself asked for; it is not selected."""

    id: DocsKind
    label: str
    suggested: bool


class PlanDocs(TypedDict):
    """The plan card's docs row.

    The workspace writes README.md itself, free; "Docs: README only" is the
    default (``defaultChoice``). Each kind offered is one more file, written
    after the code and priced into the maximum: ``maximumCredits`` is the whole
    run's maximum per selection, keyed by its kind ids sorted and joined with
    ``+`` (``"api+guide"``); None when not metered. README only is the card's
    own ``maximumCredits``. ``noteMax`` is the longest note "custom" takes.
    ``selections`` lists the selections a confirm can send, keyed the same
    way, metered or not: near the plan's batch limit not every combination of
    the kinds fits the build, and any other is refused (PLAN_DOCS_UNKNOWN).
    """

    defaultChoice: Literal["readme"]
    kinds: List[PlanDocsKind]
    noteMax: int
    maximumCredits: Optional[Dict[str, int]]
    selections: List[str]


class _DocsChoiceKinds(TypedDict):
    kinds: List[DocsKind]


class DocsChoice(_DocsChoiceKinds, total=False):
    """A confirm's docs choice: kinds the card's docs row offers, and the note
    that goes with ``"custom"`` (required with it, refused without it)."""

    note: str


class PlanCard(TypedDict, total=False):
    """The plan a build waits on."""

    planId: str
    expiresAt: str
    scope: Optional[Dict[str, Any]]
    files: List[Dict[str, str]]
    fileCount: int
    batchCount: int
    planningCredits: int
    maximumCredits: Optional[int]
    remainingCredits: Optional[int]
    credits: Optional[CreditChoice]
    autoConfirm: Dict[str, Any]
    scopeDecisionId: str
    unmetered: bool
    #: The tier and effort the confirm builds; None on a plan made before engines were named.
    engine: Optional[PlanEngine]
    #: The plan's open choices (absent on a plan made before them).
    assumptions: List[PlanAssumption]
    #: Files the workspace provides, taken out of the plan: ``{"path", "reason"}``.
    provided: List[Dict[str, str]]
    #: The docs row (README only, or docs added at confirm); None when the plan offers none.
    docs: Optional[PlanDocs]


class PreflightRequired(TypedDict, total=False):
    """What a request stopped at.

    ``kind`` is ``"plan"`` (the card) or ``"credits"`` (a confirm's credit choice).
    """

    kind: Literal["plan", "credits"]
    plan: PlanCard
    credits: CreditChoice
    planId: str


class PendingPlan(TypedDict, total=False):
    """The plan card a session waits on (the session's ``pendingPlan``)."""

    kind: Literal["plan"]
    plan: PlanCard
    messageId: Optional[str]
    prompt: str


class CopilotClient:
    """Verament calls for one VAIF account (``client.copilot(account_token)``)."""

    def __init__(self, client: VaifClient, account_token: str) -> None:
        if not account_token:
            raise ValueError("account_token must not be empty")
        self._client = client
        self._headers = {"Authorization": f"Bearer {account_token}"}

    async def _post(
        self, path: str, body: Dict[str, Any], *, timeout: Optional[float] = None
    ) -> Any:
        # Not retried: a confirm is single use, so a replay would only be refused.
        response = await self._client._send(
            "POST", path, json=body, headers=self._headers, timeout=timeout, idempotent=False
        )
        return response_json(response)

    async def _get(self, path: str) -> Any:
        response = await self._client._send("GET", path, headers=self._headers)
        return response_json(response)

    async def chat(
        self,
        project_id: str,
        message: str,
        *,
        session_id: Optional[str] = None,
        generation_types: Optional[List[str]] = None,
        generation_options: Optional[Dict[str, Any]] = None,
        auto_confirm_max_credits: Optional[int] = None,
        tier: Optional[BlueprintTier] = None,
        effort: Optional[BlueprintEffort] = None,
        timeout: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Send a message. A build request returns ``preflightRequired`` (the plan card) unless
        ``auto_confirm_max_credits`` covers the build, which then runs in this call.

        ``tier`` ("lite", "standard" or "max": Verament Lite 1.0, Standard 1.0, Max 1.0)
        and ``effort`` ("quick", "balanced", "deep" or "extended") name the engine;
        omitted, the plan's defaults apply (on Enterprise, the org's). One the plan does not
        include raises a 403 :class:`VaifAuthError`; see :func:`blueprint_engine_offer`.

        ``timeout`` defaults to 120 seconds, or to ``BUILD_TIMEOUT_SECONDS`` with
        ``auto_confirm_max_credits``, since the build may run in this call."""
        if auto_confirm_max_credits is not None and (
            not isinstance(auto_confirm_max_credits, int) or auto_confirm_max_credits <= 0
        ):
            raise ValueError("auto_confirm_max_credits must be a positive whole number")
        body: Dict[str, Any] = {"projectId": project_id, "message": message}
        if session_id:
            body["sessionId"] = session_id
        if generation_types:
            body["generationTypes"] = list(generation_types)
        if generation_options:
            body["generationOptions"] = dict(generation_options)
        if auto_confirm_max_credits is not None:
            body["autoConfirm"] = {"maxCredits": auto_confirm_max_credits}
        if tier:
            body["tier"] = tier
        if effort:
            body["effort"] = effort
        if timeout is None:
            timeout = BUILD_TIMEOUT_SECONDS if auto_confirm_max_credits is not None else 120.0
        result: Dict[str, Any] = await self._post("/ai/copilot/chat", body, timeout=timeout)
        return result

    @staticmethod
    def _plan_request(
        project_id: str,
        session_id: str,
        message: str,
        generation_types: Optional[List[str]],
        preflight: Dict[str, Any],
    ) -> Dict[str, Any]:
        if not project_id or not session_id or not message:
            raise ValueError("project_id, session_id and message are required")
        body: Dict[str, Any] = {
            "projectId": project_id,
            "sessionId": session_id,
            "message": message,
            "preflight": preflight,
        }
        if generation_types:
            body["generationTypes"] = list(generation_types)
        return body

    @staticmethod
    def _confirm(
        plan_id: str,
        credit_choice: Optional[CreditChoiceAnswer],
        assumption_choices: Optional[Dict[str, str]] = None,
        docs: Optional[DocsChoice] = None,
    ) -> Dict[str, Any]:
        if not plan_id:
            raise ValueError("plan_id must not be empty")
        if credit_choice is not None and credit_choice not in ("smaller", "until_zero"):
            raise ValueError("credit_choice must be 'smaller' or 'until_zero'")
        preflight: Dict[str, Any] = {"confirmPlanId": plan_id}
        if credit_choice:
            preflight["creditChoice"] = credit_choice
        if assumption_choices:
            preflight["assumptionChoices"] = dict(assumption_choices)
        if docs is not None:
            if not docs.get("kinds"):
                raise ValueError("docs needs at least one kind")
            choice: Dict[str, Any] = {"kinds": list(docs["kinds"])}
            if "note" in docs:
                choice["note"] = docs["note"]
            preflight["docs"] = choice
        return preflight

    async def confirm_plan(
        self,
        project_id: str,
        session_id: str,
        plan_id: str,
        message: str,
        *,
        credit_choice: Optional[CreditChoiceAnswer] = None,
        assumption_choices: Optional[Dict[str, str]] = None,
        docs: Optional[DocsChoice] = None,
        generation_types: Optional[List[str]] = None,
        timeout: float = BUILD_TIMEOUT_SECONDS,
    ) -> Dict[str, Any]:
        """Confirm the plan and build it; returns once the build is over.

        ``assumption_choices`` (id to option value) changes the card's assumptions
        to options that change only code; one that changes files raises a 409
        (PLAN_REPLAN_REQUIRED): use :meth:`replan`.

        ``docs`` (``{"kinds": [...], "note": ...}``) adds the card's docs kinds,
        written after the code and priced into the maximum; omitted, the README
        only. A kind the card did not offer raises a 400 (PLAN_DOCS_UNKNOWN)
        before anything runs.

        The answer carries the files under ``response.artifacts.files``, the charge under
        ``context.creditsCharged`` and ``build.status``. A balance below the maximum returns
        ``preflightRequired`` (the credit choice): confirm again with ``credit_choice``.
        A refused confirm raises: 404 not found, 409 already confirmed, canceled,
        superseded, another prompt or PLAN_STALE, 410 expired.
        """
        body = self._plan_request(
            project_id,
            session_id,
            message,
            generation_types,
            self._confirm(plan_id, credit_choice, assumption_choices, docs),
        )
        result: Dict[str, Any] = await self._post("/ai/copilot/chat", body, timeout=timeout)
        return result

    async def cancel_plan(
        self,
        project_id: str,
        session_id: str,
        plan_id: str,
        message: str,
    ) -> Dict[str, Any]:
        """Drop the plan for good. Nothing runs, and nothing more is charged."""
        if not plan_id:
            raise ValueError("plan_id must not be empty")
        body = self._plan_request(project_id, session_id, message, None, {"cancelPlanId": plan_id})
        result: Dict[str, Any] = await self._post("/ai/copilot/chat", body)
        return result

    async def queue_confirm_plan(
        self,
        project_id: str,
        session_id: str,
        plan_id: str,
        message: str,
        *,
        credit_choice: Optional[CreditChoiceAnswer] = None,
        assumption_choices: Optional[Dict[str, str]] = None,
        docs: Optional[DocsChoice] = None,
        generation_types: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Confirm the plan and build it in the background. Returns ``{"jobId": ...}``;
        a refused confirm raises at once, as :meth:`confirm_plan` does."""
        body = self._plan_request(
            project_id,
            session_id,
            message,
            generation_types,
            self._confirm(plan_id, credit_choice, assumption_choices, docs),
        )
        result: Dict[str, Any] = await self._post("/ai/copilot/job", body)
        return result

    async def replan(
        self,
        project_id: str,
        session_id: str,
        message: str,
        assumption_choices: Dict[str, str],
        *,
        generation_types: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Plan the same message again with the card's changed assumptions, when a
        changed option affects files (``confirm_plan`` raised PLAN_REPLAN_REQUIRED).
        Returns the new plan card under ``preflightRequired``; planning is charged again."""
        if not assumption_choices:
            raise ValueError("assumption_choices must not be empty")
        body = self._plan_request(
            project_id,
            session_id,
            message,
            generation_types,
            {"assumptionChoices": dict(assumption_choices)},
        )
        result: Dict[str, Any] = await self._post("/ai/copilot/chat", body, timeout=120.0)
        return result

    async def plan_with_defaults(
        self,
        project_id: str,
        session_id: str,
        message: str,
        *,
        generation_types: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """After a reply that asked a question (``planWithDefaults`` on the answer, with
        what the question cost): plan the same message without asking. Planning is
        charged as usual."""
        body = self._plan_request(
            project_id, session_id, message, generation_types, {"planWithDefaults": True}
        )
        result: Dict[str, Any] = await self._post("/ai/copilot/chat", body, timeout=120.0)
        return result

    async def get_job(self, job_id: str) -> Dict[str, Any]:
        """A queued job's state and, once finished, its ``result`` (files, ``status``)."""
        if not job_id:
            raise ValueError("job_id must not be empty")
        path = f"/ai/copilot/job/{path_segment(job_id, 'job_id')}"
        result: Dict[str, Any] = await self._get(path)
        return result

    async def get_session(self, session_id: str) -> Dict[str, Any]:
        """A session, its messages, and ``pendingPlan``: the card it waits on, or None."""
        if not session_id:
            raise ValueError("session_id must not be empty")
        path = f"/ai/copilot/session/{path_segment(session_id, 'session_id')}"
        result: Dict[str, Any] = await self._get(path)
        return result


def pending_plan_of(session: Dict[str, Any]) -> Union[PendingPlan, None]:
    """The plan card a session (from :meth:`CopilotClient.get_session`) waits on, or None."""
    pending = session.get("pendingPlan")
    if isinstance(pending, dict) and pending.get("kind") == "plan":
        return cast(PendingPlan, pending)
    return None


def blueprint_engine_offer(error: object) -> Optional[EngineOffer]:
    """The engine offer in an error raised by :meth:`CopilotClient.chat`, ``confirm_plan`` or
    ``queue_confirm_plan`` (a tier or effort above the plan), or None for any other error.

    ::

        try:
            await copilot.chat(project_id, message, tier="max")
        except VaifError as err:
            offer = blueprint_engine_offer(err)
            if offer:
                await copilot.chat(project_id, message, **offer["retryWith"])
    """
    code = getattr(error, "code", None)
    body = getattr(error, "body", None)
    if code not in _ENGINE_OFFER_CODES or not isinstance(body, dict):
        return None
    retry, allowed = body.get("retryWith"), body.get("allowed")
    if not isinstance(retry, dict) or not isinstance(allowed, dict):
        return None
    if not isinstance(retry.get("tier"), str) or not isinstance(retry.get("effort"), str):
        return None
    tiers, efforts = allowed.get("tiers"), allowed.get("efforts")
    if not isinstance(tiers, list) or not isinstance(efforts, list):
        return None
    message = body.get("message")
    suggested = body.get("suggestedPlan")
    return {
        "code": cast(str, code),
        "message": message if isinstance(message, str) else str(getattr(error, "message", "")),
        "suggestedPlan": suggested if isinstance(suggested, str) else "",
        "allowed": {"tiers": [str(t) for t in tiers], "efforts": [str(e) for e in efforts]},
        "retryWith": {"tier": retry["tier"], "effort": retry["effort"]},
    }
