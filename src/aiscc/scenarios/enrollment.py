"""Pure Stockroom scenario enrollment for the owner-only Phase 1B runtime.

The compiler accepts the one-field requester selection and already-loaded,
server-owned contracts.  It performs no I/O and creates no runtime authority,
evidence, Human result, Judgment, or workflow mutation.
"""

from __future__ import annotations

from dataclasses import dataclass

from aiscc.contracts.workflow import RuntimeMode
from aiscc.scenarios.catalog import ScenarioCatalog
from aiscc.scenarios.models import (
    RESOURCE_REF,
    SCENARIO_IDS,
    Scenario,
)

_PROFILE_IDS = (
    "stockroom-owner-s1-v1",
    "stockroom-owner-s2-v1",
    "stockroom-owner-s3-v1",
    "stockroom-owner-s4-v1",
)


@dataclass(frozen=True, slots=True)
class FrozenEvidenceDescriptor:
    requirement_id: str
    profile: str
    proof_type: str
    evidence_type_version: str
    producer: str
    ownership: str
    tool_output_ref_required: bool
    checkpoint: str


@dataclass(frozen=True, slots=True)
class FrozenHumanDescriptor:
    requirement_id: str
    ownership: str
    proof_type: str
    producer: str
    status: str
    pre_human_readiness_required: bool


@dataclass(frozen=True, slots=True)
class FrozenJudgmentDescriptor:
    owner_policy: str
    expected_status: str | None
    authoritative_at_capture_boundary: bool
    rule_version: str


@dataclass(frozen=True, slots=True)
class StockroomScenarioBinding:
    scenario: Scenario
    provider_profile_id: str
    provider_profile_version: str
    tool_id: str | None
    tool_action: str | None
    suppress_summary_evidence_candidate: bool


@dataclass(frozen=True, slots=True)
class StockroomOwnerContext:
    mode: RuntimeMode
    resource_ref: str
    provider_id: str
    adapter_protocol_version: str
    execution_backend_kind: str
    external_llm_executed: bool
    bindings: tuple[StockroomScenarioBinding, ...]


@dataclass(frozen=True, slots=True)
class StockroomEnrollment:
    mode: RuntimeMode
    scenario_id: str
    scenario_version: str
    resource_ref: str
    task_contract: object
    allowed_actions: tuple[str, ...]
    provider_id: str
    provider_profile_id: str
    provider_profile_version: str
    adapter_protocol_version: str
    execution_backend_kind: str
    external_llm_executed: bool
    tool_id: str | None
    tool_action: str | None
    evidence_descriptors: tuple[FrozenEvidenceDescriptor, ...]
    human_descriptor: FrozenHumanDescriptor | None
    judgment_descriptor: FrozenJudgmentDescriptor
    expected_states: tuple[str, ...]
    suppress_summary_evidence_candidate: bool
    same_run_automatic_retry: bool
    admitted_evidence: tuple[()] = ()
    human_result: None = None
    judgment: None = None


def build_stockroom_owner_context(scenarios: tuple[Scenario, ...]) -> StockroomOwnerContext:
    """Build the inert private context from four already-validated contracts."""
    scenario_ids = tuple(item.scenario_id for item in scenarios)
    if type(scenarios) is not tuple or scenario_ids != SCENARIO_IDS:
        raise ValueError("EXACT_FOUR_STOCKROOM_SCENARIOS_REQUIRED")
    bindings = tuple(
        StockroomScenarioBinding(
            scenario=scenario,
            provider_profile_id=_PROFILE_IDS[index],
            provider_profile_version="1",
            tool_id=None if index == 2 else "stockroom_summary",
            tool_action=None if index == 2 else "fixed-stockroom-summary",
            suppress_summary_evidence_candidate=index == 1,
        )
        for index, scenario in enumerate(scenarios)
    )
    return StockroomOwnerContext(
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        resource_ref=RESOURCE_REF,
        provider_id="aiscc-local-deterministic",
        adapter_protocol_version="stockroom-local-responses-v1",
        execution_backend_kind="LOCAL_DETERMINISTIC_PROVIDER",
        external_llm_executed=False,
        bindings=bindings,
    )


def compile_stockroom_selection(
    selection: object,
    *,
    catalog: ScenarioCatalog,
    owner_context: StockroomOwnerContext,
) -> StockroomEnrollment:
    """Compile one exact selection without touching any runtime boundary."""
    if type(selection) is not dict or set(selection) != {"scenario_id"}:
        raise ValueError("SCENARIO_ID_ONLY_SELECTION_REQUIRED")
    scenario_id = selection.get("scenario_id")
    if type(scenario_id) is not str or scenario_id not in SCENARIO_IDS:
        raise ValueError("UNKNOWN_STOCKROOM_SCENARIO")
    if type(catalog) is not ScenarioCatalog or type(owner_context) is not StockroomOwnerContext:
        raise ValueError("SERVER_OWNED_CATALOG_AND_CONTEXT_REQUIRED")
    if (
        owner_context.mode is not RuntimeMode.OWNER_SELF_DOGFOOD
        or owner_context.resource_ref != RESOURCE_REF
        or owner_context.provider_id != "aiscc-local-deterministic"
        or owner_context.adapter_protocol_version != "stockroom-local-responses-v1"
        or owner_context.execution_backend_kind != "LOCAL_DETERMINISTIC_PROVIDER"
        or owner_context.external_llm_executed is not False
        or catalog.resource.resource_ref != RESOURCE_REF
        or catalog.document.resource_ref != RESOURCE_REF
        or tuple(item.scenario_id for item in catalog.scenarios) != SCENARIO_IDS
    ):
        raise ValueError("STOCKROOM_OWNER_CONTEXT_MISMATCH")
    matches = tuple(
        binding
        for binding in owner_context.bindings
        if binding.scenario.scenario_id == scenario_id
    )
    if len(matches) != 1:
        raise ValueError("STOCKROOM_SCENARIO_BINDING_MISMATCH")
    binding = matches[0]
    scenario = binding.scenario
    catalog_matches = tuple(
        item for item in catalog.scenarios if item.scenario_id == scenario_id
    )
    if (
        len(catalog_matches) != 1
        or scenario is not catalog_matches[0]
        or scenario.scenario_version != "1.0.0"
        or scenario.resource_ref != RESOURCE_REF
    ):
        raise ValueError("STOCKROOM_SCENARIO_IDENTITY_MISMATCH")

    evidence = tuple(
        _evidence_descriptor(item.requirement_id)
        for item in scenario.evidence_contract.executor_required
    )
    human = (
        FrozenHumanDescriptor(
            requirement_id="human-browser-qa",
            ownership="HUMAN_OWNED",
            proof_type="HUMAN_VERIFICATION",
            producer="HUMAN_P1_7",
            status="HUMAN_PENDING",
            pre_human_readiness_required=True,
        )
        if scenario_id == "stockroom-s4-human-owned-claim"
        else None
    )
    judgment = scenario.judgment_contract
    return StockroomEnrollment(
        mode=owner_context.mode,
        scenario_id=scenario.scenario_id,
        scenario_version=scenario.scenario_version,
        resource_ref=scenario.resource_ref,
        task_contract=scenario.task_contract,
        allowed_actions=scenario.allowed_actions,
        provider_id=owner_context.provider_id,
        provider_profile_id=binding.provider_profile_id,
        provider_profile_version=binding.provider_profile_version,
        adapter_protocol_version=owner_context.adapter_protocol_version,
        execution_backend_kind=owner_context.execution_backend_kind,
        external_llm_executed=owner_context.external_llm_executed,
        tool_id=binding.tool_id,
        tool_action=binding.tool_action,
        evidence_descriptors=evidence,
        human_descriptor=human,
        judgment_descriptor=FrozenJudgmentDescriptor(
            owner_policy=judgment.owner_policy,
            expected_status=judgment.expected_status,
            authoritative_at_capture_boundary=judgment.authoritative_at_capture_boundary,
            rule_version=judgment.rule_version,
        ),
        expected_states=scenario.expected_workflow.states,
        suppress_summary_evidence_candidate=binding.suppress_summary_evidence_candidate,
        same_run_automatic_retry=scenario.expected_workflow.same_run_automatic_retry,
    )


def _evidence_descriptor(requirement_id: str) -> FrozenEvidenceDescriptor:
    if requirement_id == "summary-runtime":
        return FrozenEvidenceDescriptor(
            requirement_id,
            "EXECUTOR_REQUIRED",
            "TOOL_RUNTIME",
            "1",
            "SYSTEM_RUNTIME_OBSERVATION",
            "EXECUTOR",
            True,
            "PRE_HUMAN_EVIDENCE",
        )
    if requirement_id == "policy-conflict-static":
        return FrozenEvidenceDescriptor(
            requirement_id,
            "EXECUTOR_REQUIRED",
            "STATIC_SOURCE",
            "1",
            "SYSTEM_STATIC_PROOF",
            "EXECUTOR",
            False,
            "PRE_HUMAN_EVIDENCE",
        )
    raise ValueError("UNKNOWN_STOCKROOM_EVIDENCE_REQUIREMENT")
