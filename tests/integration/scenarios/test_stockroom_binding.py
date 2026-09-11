from __future__ import annotations

import socket
import subprocess
from dataclasses import FrozenInstanceError, dataclass, replace
from types import MappingProxyType

import pytest

import aiscc.scenarios.composition as composition_module
from aiscc import bootstrap
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.evidence.service import EvidenceAdmissionService
from aiscc.human.repository import PostgresHumanAuthorityRepository
from aiscc.judgment.authority import PostgresJudgmentAuthority
from aiscc.persistence.repository import PostgresExecutionRepository
from aiscc.providers.local_deterministic import LocalDeterministicProvider
from aiscc.providers.openai_responses import OpenAIResponsesAdapter
from aiscc.providers.service import AgentExecutionService
from aiscc.providers.stockroom_tool import StockroomSummaryDispatcher
from aiscc.runtime.docker import DockerRuntime
from aiscc.runtime.stockroom_materializer import StockroomMaterializer
from aiscc.runtime.stockroom_workspace import StockroomWorkspace
from aiscc.scenarios.composition import build_stockroom_owner_composition
from aiscc.scenarios.driver import StockroomOwnerDependencies
from aiscc.scenarios.models import RESOURCE_REF, SCENARIO_IDS
from aiscc.security.policy import SecurityPolicy, default_profiles
from aiscc.security.stockroom_policy import StockroomOwnerRestriction
from aiscc.workflow.kernel import WorkflowKernel


@dataclass(frozen=True, slots=True)
class _FactoryAuthority:
    semantic_role: str
    factory_ref: str
    factory_fingerprint: str


def _owners() -> StockroomOwnerDependencies:
    config = build_stockroom_owner_composition().security_config
    restriction = StockroomOwnerRestriction(config)
    materializer_factory = _FactoryAuthority(
        "STOCKROOM_MATERIALIZER_FACTORY", "binding-materializer-factory", "1" * 64
    )
    execution_factory = _FactoryAuthority(
        "STOCKROOM_AGENT_EXECUTION_SERVICE_FACTORY",
        "binding-execution-factory",
        "2" * 64,
    )
    return StockroomOwnerDependencies(
        workflow_kernel=object.__new__(WorkflowKernel),
        agent_execution_service_factory=execution_factory,
        evidence_admission_service=object.__new__(EvidenceAdmissionService),
        human_gate_owner=object.__new__(PostgresHumanAuthorityRepository),
        judgment_owner=object.__new__(PostgresJudgmentAuthority),
        workspace_owner=object.__new__(StockroomWorkspace),
        materializer_factory=materializer_factory,
        security_policy=SecurityPolicy(default_profiles(), stockroom_policy=restriction),
        stockroom_owner_restriction=restriction,
    )


def test_four_owner_bindings_prepare_without_runtime_side_effects(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: dict[str, int] = {}
    reached: list[str] = []

    def forbid(name: str):
        def forbidden(*args: object, **kwargs: object) -> None:
            del args, kwargs
            calls[name] = calls.get(name, 0) + 1
            raise AssertionError(f"runtime boundary called: {name}")

        return forbidden

    boundaries = (
        (WorkflowKernel, "request_transition"),
        (AgentExecutionService, "execute_provider"),
        (AgentExecutionService, "execute"),
        (PostgresExecutionRepository, "create_attempt"),
        (PostgresExecutionRepository, "transition_attempt"),
        (PostgresExecutionRepository, "create_operation"),
        (PostgresExecutionRepository, "advance_operation"),
        (PostgresExecutionRepository, "store_private_protocol_item"),
        (PostgresExecutionRepository, "reserve_execution_bounds"),
        (PostgresExecutionRepository, "settle_execution_output"),
        (PostgresExecutionRepository, "start_dispatch_if_fresh"),
        (PostgresExecutionRepository, "fail_operation_before_side_effect"),
        (PostgresExecutionRepository, "close_workflow_left_running"),
        (PostgresExecutionRepository, "store_output_ref"),
        (EvidenceAdmissionService, "submit"),
        (EvidenceAdmissionService, "submit_durable"),
        (EvidenceAdmissionService, "preserve_supplemental"),
        (EvidenceAdmissionService, "invalidate_authority"),
        (PostgresHumanAuthorityRepository, "submit_result"),
        (
            PostgresHumanAuthorityRepository,
            "issue_current_gate_action_authority",
        ),
        (PostgresHumanAuthorityRepository, "expire_gate_if_needed"),
        (PostgresHumanAuthorityRepository, "supersede_gate"),
        (PostgresHumanAuthorityRepository, "create_producer_ref"),
        (PostgresJudgmentAuthority, "issue"),
        (StockroomWorkspace, "allocate"),
        (StockroomWorkspace, "write_file"),
        (StockroomMaterializer, "materialize"),
        (SecurityPolicy, "issue_resource_grant"),
        (SecurityPolicy, "evaluate"),
        (SecurityPolicy, "issue_capability"),
        (StockroomOwnerRestriction, "seal_context"),
        (StockroomOwnerRestriction, "allows"),
        (LocalDeterministicProvider, "call"),
        (StockroomSummaryDispatcher, "dispatch"),
        (StockroomSummaryDispatcher, "dispatch_with_receipts"),
        (DockerRuntime, "run"),
        (DockerRuntime, "run_consumed_stockroom"),
        (OpenAIResponsesAdapter, "__init__"),
    )
    for owner, method in boundaries:
        name = f"{owner.__name__}.{method}"
        calls[name] = 0
        monkeypatch.setattr(owner, method, forbid(name))
    for owner, method in ((subprocess, "Popen"), (socket, "socket")):
        name = f"{owner.__name__}.{method}"
        calls[name] = 0
        monkeypatch.setattr(owner, method, forbid(name))

    owners = _owners()
    reached.append("owner_dependency_construction")
    prepared_root = bootstrap.build_stockroom_owner_preparation(owners=owners)
    reached.extend(("owner_composition_creation", "bootstrap_owner_preparation"))

    prepared_drivers = []
    for index, scenario_id in enumerate(SCENARIO_IDS):
        prepared_drivers.append(
            prepared_root.prepare(
                scenario_id=scenario_id,
                run_id=f"run-b3-{index + 1}",
                attempt_id="attempt-1",
                expected_initial_state_version=1,
            )
        )
        reached.append(f"S{index + 1}_request_preparation")
    prepared_drivers = tuple(prepared_drivers)
    requests = tuple(item.request for item in prepared_drivers)

    assert tuple(item.scenario_id for item in requests) == SCENARIO_IDS
    assert all(item.scenario_version == "1.0.0" for item in requests)
    assert all(item.resource_ref == RESOURCE_REF for item in requests)
    assert all(item.runtime_mode is RuntimeMode.OWNER_SELF_DOGFOOD for item in requests)
    assert all(item.enrollment.external_llm_executed is False for item in requests)
    assert all(item.run_binding.expected_initial_state is WorkflowState.READY for item in requests)
    assert all(item.run_binding.expected_initial_state_version == 1 for item in requests)
    assert len({item.configuration_fingerprints.composition_sha256 for item in requests}) == 1
    assert all(len(item.request_fingerprint) == 64 for item in requests)
    assert all(item.owners is owners for item in prepared_drivers)
    assert all(
        item.owners.materializer_factory is owners.materializer_factory
        and item.owners.agent_execution_service_factory is owners.agent_execution_service_factory
        for item in prepared_drivers
    )
    assert all(
        item.attempt_binding.request_fingerprint == item.request.request_fingerprint
        and item.attempt_binding.run_binding_fingerprint
        == item.request.run_binding.binding_fingerprint
        and item.attempt_binding.configuration_fingerprint
        == item.request.configuration_fingerprints.composition_sha256
        for item in prepared_drivers
    )
    with pytest.raises(FrozenInstanceError):
        prepared_drivers[0].attempt_binding.attempt_id = "foreign"  # type: ignore[misc]

    s1, s2, s3, s4 = requests
    assert (s1.tool_id, s1.tool_action) == (
        "stockroom_summary",
        "fixed-stockroom-summary",
    )
    assert s2.tool_id == "stockroom_summary"
    assert s2.enrollment.suppress_summary_evidence_candidate is True
    assert s2.enrollment.same_run_automatic_retry is False
    assert {item.requirement_id for item in s2.evidence_descriptors} == {"summary-runtime"}
    assert s3.tool_id is None and s3.tool_action is None
    assert {item.proof_type for item in s3.evidence_descriptors} == {"STATIC_SOURCE"}
    assert s4.tool_id == "stockroom_summary"
    assert s4.human_descriptor is not None
    assert (
        s4.human_descriptor.ownership,
        s4.human_descriptor.producer,
        s4.human_descriptor.status,
    ) == ("HUMAN_OWNED", "HUMAN_P1_7", "HUMAN_PENDING")
    assert s4.enrollment.human_result is None
    assert all(item.enrollment.admitted_evidence == () for item in requests)
    assert all(item.enrollment.judgment is None for item in requests)
    assert reached == [
        "owner_dependency_construction",
        "owner_composition_creation",
        "bootstrap_owner_preparation",
        "S1_request_preparation",
        "S2_request_preparation",
        "S3_request_preparation",
        "S4_request_preparation",
    ]
    assert calls and all(count == 0 for count in calls.values())


def _profiles_with_timeout(value: float | int) -> MappingProxyType:
    composed = build_stockroom_owner_composition()
    return MappingProxyType(
        {
            profile_id: replace(
                local,
                profile=replace(local.profile, total_timeout_seconds=value),
            )
            for profile_id, local in composed.provider_profiles.items()
        }
    )


def test_provider_timeout_fingerprint_uses_exact_integer_seconds() -> None:
    composed = build_stockroom_owner_composition()
    whole_float = composition_module._fingerprints(
        composed.catalog,
        _profiles_with_timeout(30.0),
        composed.tool_config,
        composed.security_config,
    )
    whole_integer = composition_module._fingerprints(
        composed.catalog,
        _profiles_with_timeout(30),
        composed.tool_config,
        composed.security_config,
    )

    assert whole_float == whole_integer == composed.fingerprints
    assert all(
        len(value) == 64 and value == value.lower() and set(value) <= set("0123456789abcdef")
        for value in (
            whole_float.provider_profiles_sha256,
            whole_float.composition_sha256,
        )
    )


@pytest.mark.parametrize("value", [29.5, float("nan"), float("inf"), float("-inf")])
def test_provider_timeout_fingerprint_denies_non_integral_or_non_finite(
    value: float,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    composed = build_stockroom_owner_composition()
    profiles = _profiles_with_timeout(value)
    with pytest.raises(
        composition_module.StockroomCompositionError,
        match="STOCKROOM_COMPOSITION_BINDING_DENIED",
    ):
        composition_module._fingerprints(
            composed.catalog,
            profiles,
            composed.tool_config,
            composed.security_config,
        )

    monkeypatch.setattr(
        composition_module,
        "load_stockroom_owner_profiles",
        lambda path: profiles,
    )
    with pytest.raises(
        composition_module.StockroomCompositionError,
        match="STOCKROOM_COMPOSITION_BINDING_DENIED",
    ):
        build_stockroom_owner_composition()
