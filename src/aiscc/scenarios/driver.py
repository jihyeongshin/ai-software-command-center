"""Inert owner-only Stockroom driver preparation.

This module binds immutable enrollment metadata to explicit production owner
objects.  It deliberately exposes no execution method and performs no I/O.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.evidence.service import EvidenceAdmissionService
from aiscc.human.repository import PostgresHumanAuthorityRepository
from aiscc.judgment.authority import PostgresJudgmentAuthority
from aiscc.providers.models import canonical_sha256
from aiscc.providers.service import AgentExecutionService
from aiscc.runtime.stockroom_materializer import StockroomMaterializer
from aiscc.runtime.stockroom_workspace import StockroomWorkspace
from aiscc.scenarios.enrollment import StockroomEnrollment
from aiscc.scenarios.models import RESOURCE_REF, SCENARIO_IDS
from aiscc.security.policy import SecurityPolicy
from aiscc.security.stockroom_policy import StockroomOwnerRestriction
from aiscc.workflow.kernel import WorkflowKernel

_PROFILE_IDS = (
    "stockroom-owner-s1-v1",
    "stockroom-owner-s2-v1",
    "stockroom-owner-s3-v1",
    "stockroom-owner-s4-v1",
)
_SAFE_ID = re.compile(r"[A-Za-z0-9_.-]{1,100}")
_SHA256 = re.compile(r"[0-9a-f]{64}")


@dataclass(frozen=True, slots=True)
class StockroomConfigurationFingerprints:
    catalog_sha256: str
    provider_profiles_sha256: str
    tool_config_sha256: str
    security_config_sha256: str
    composition_sha256: str

    def __post_init__(self) -> None:
        if any(
            _SHA256.fullmatch(value) is None
            for value in (
                self.catalog_sha256,
                self.provider_profiles_sha256,
                self.tool_config_sha256,
                self.security_config_sha256,
                self.composition_sha256,
            )
        ):
            raise ValueError("STOCKROOM_CONFIGURATION_FINGERPRINT_REQUIRED")


@dataclass(frozen=True, slots=True)
class StockroomRunPreparationBinding:
    run_id: str
    attempt_id: str
    expected_initial_state: WorkflowState
    expected_initial_state_version: int
    binding_fingerprint: str

    def __post_init__(self) -> None:
        if (
            type(self.run_id) is not str
            or _SAFE_ID.fullmatch(self.run_id) is None
            or type(self.attempt_id) is not str
            or _SAFE_ID.fullmatch(self.attempt_id) is None
            or self.expected_initial_state is not WorkflowState.READY
            or type(self.expected_initial_state_version) is not int
            or self.expected_initial_state_version < 1
            or _SHA256.fullmatch(self.binding_fingerprint) is None
        ):
            raise ValueError("STOCKROOM_RUN_PREPARATION_BINDING_DENIED")


@dataclass(frozen=True, slots=True)
class StockroomDriverRequest:
    enrollment: StockroomEnrollment
    run_binding: StockroomRunPreparationBinding
    configuration_fingerprints: StockroomConfigurationFingerprints
    request_fingerprint: str

    def __post_init__(self) -> None:
        enrollment = self.enrollment
        if (
            type(enrollment) is not StockroomEnrollment
            or enrollment.mode is not RuntimeMode.OWNER_SELF_DOGFOOD
            or enrollment.scenario_id not in SCENARIO_IDS
            or enrollment.scenario_version != "1.0.0"
            or enrollment.resource_ref != RESOURCE_REF
            or enrollment.provider_id != "aiscc-local-deterministic"
            or enrollment.provider_profile_id
            != _PROFILE_IDS[SCENARIO_IDS.index(enrollment.scenario_id)]
            or enrollment.provider_profile_version != "1"
            or enrollment.adapter_protocol_version != "stockroom-local-responses-v1"
            or enrollment.execution_backend_kind != "LOCAL_DETERMINISTIC_PROVIDER"
            or enrollment.external_llm_executed is not False
            or (enrollment.tool_id is None) != (enrollment.scenario_id == SCENARIO_IDS[2])
            or (enrollment.tool_action is None) != (enrollment.scenario_id == SCENARIO_IDS[2])
            or type(self.run_binding) is not StockroomRunPreparationBinding
            or type(self.configuration_fingerprints)
            is not StockroomConfigurationFingerprints
            or _SHA256.fullmatch(self.request_fingerprint) is None
            or self.request_fingerprint != canonical_sha256(_request_payload(self))
        ):
            raise ValueError("STOCKROOM_DRIVER_REQUEST_BINDING_DENIED")

    @property
    def scenario_id(self) -> str:
        return self.enrollment.scenario_id

    @property
    def scenario_version(self) -> str:
        return self.enrollment.scenario_version

    @property
    def resource_ref(self) -> str:
        return self.enrollment.resource_ref

    @property
    def runtime_mode(self) -> RuntimeMode:
        return self.enrollment.mode

    @property
    def provider_profile_id(self) -> str:
        return self.enrollment.provider_profile_id

    @property
    def provider_profile_version(self) -> str:
        return self.enrollment.provider_profile_version

    @property
    def tool_id(self) -> str | None:
        return self.enrollment.tool_id

    @property
    def tool_action(self) -> str | None:
        return self.enrollment.tool_action

    @property
    def evidence_descriptors(self) -> tuple[object, ...]:
        return self.enrollment.evidence_descriptors

    @property
    def human_descriptor(self) -> object | None:
        return self.enrollment.human_descriptor

    @property
    def judgment_descriptor(self) -> object:
        return self.enrollment.judgment_descriptor


@dataclass(frozen=True, slots=True)
class StockroomOwnerDependencies:
    workflow_kernel: WorkflowKernel
    agent_execution_service: AgentExecutionService
    evidence_admission_service: EvidenceAdmissionService
    human_gate_owner: PostgresHumanAuthorityRepository
    judgment_owner: PostgresJudgmentAuthority
    workspace_owner: StockroomWorkspace
    materializer: StockroomMaterializer
    security_policy: SecurityPolicy
    stockroom_owner_restriction: StockroomOwnerRestriction

    def __post_init__(self) -> None:
        requirements = (
            (self.workflow_kernel, WorkflowKernel),
            (self.agent_execution_service, AgentExecutionService),
            (self.evidence_admission_service, EvidenceAdmissionService),
            (self.human_gate_owner, PostgresHumanAuthorityRepository),
            (self.judgment_owner, PostgresJudgmentAuthority),
            (self.workspace_owner, StockroomWorkspace),
            (self.materializer, StockroomMaterializer),
            (self.security_policy, SecurityPolicy),
            (self.stockroom_owner_restriction, StockroomOwnerRestriction),
        )
        if any(not isinstance(value, expected) for value, expected in requirements):
            raise ValueError("STOCKROOM_REAL_OWNER_DEPENDENCY_REQUIRED")


@dataclass(frozen=True, slots=True)
class PreparedStockroomDriver:
    request: StockroomDriverRequest
    owners: StockroomOwnerDependencies

    def __post_init__(self) -> None:
        if (
            type(self.request) is not StockroomDriverRequest
            or type(self.owners) is not StockroomOwnerDependencies
        ):
            raise ValueError("STOCKROOM_PREPARED_DRIVER_BINDING_DENIED")


def build_stockroom_driver_request(
    enrollment: StockroomEnrollment,
    *,
    run_id: str,
    attempt_id: str,
    expected_initial_state_version: int,
    configuration_fingerprints: StockroomConfigurationFingerprints,
) -> StockroomDriverRequest:
    """Create one immutable request; this function has no runtime side effects."""
    if (
        type(enrollment) is not StockroomEnrollment
        or type(configuration_fingerprints) is not StockroomConfigurationFingerprints
    ):
        raise ValueError("STOCKROOM_DRIVER_REQUEST_INPUT_DENIED")
    binding_payload = {
        "run_id": run_id,
        "attempt_id": attempt_id,
        "expected_initial_state": WorkflowState.READY.value,
        "expected_initial_state_version": expected_initial_state_version,
        "composition_sha256": configuration_fingerprints.composition_sha256,
    }
    binding = StockroomRunPreparationBinding(
        run_id=run_id,
        attempt_id=attempt_id,
        expected_initial_state=WorkflowState.READY,
        expected_initial_state_version=expected_initial_state_version,
        binding_fingerprint=canonical_sha256(binding_payload),
    )
    return StockroomDriverRequest(
        enrollment=enrollment,
        run_binding=binding,
        configuration_fingerprints=configuration_fingerprints,
        request_fingerprint=canonical_sha256(
            _request_payload_values(enrollment, binding, configuration_fingerprints)
        ),
    )


def prepare_stockroom_driver(
    request: StockroomDriverRequest,
    owners: StockroomOwnerDependencies,
) -> PreparedStockroomDriver:
    """Bind explicit existing owners without invoking any of them."""
    return PreparedStockroomDriver(request=request, owners=owners)


def _request_payload(request: StockroomDriverRequest) -> dict[str, object]:
    return _request_payload_values(
        request.enrollment,
        request.run_binding,
        request.configuration_fingerprints,
    )


def _request_payload_values(
    enrollment: StockroomEnrollment,
    run_binding: StockroomRunPreparationBinding,
    configuration_fingerprints: StockroomConfigurationFingerprints,
) -> dict[str, object]:
    return {
        "scenario_id": enrollment.scenario_id,
        "scenario_version": enrollment.scenario_version,
        "resource_ref": enrollment.resource_ref,
        "runtime_mode": enrollment.mode.value,
        "provider": {
            "provider_id": enrollment.provider_id,
            "profile_id": enrollment.provider_profile_id,
            "profile_version": enrollment.provider_profile_version,
            "adapter_protocol_version": enrollment.adapter_protocol_version,
            "execution_backend_kind": enrollment.execution_backend_kind,
            "external_llm_executed": enrollment.external_llm_executed,
        },
        "tool": {"tool_id": enrollment.tool_id, "tool_action": enrollment.tool_action},
        "run_binding": {
            "run_id": run_binding.run_id,
            "attempt_id": run_binding.attempt_id,
            "expected_initial_state": run_binding.expected_initial_state.value,
            "expected_initial_state_version": run_binding.expected_initial_state_version,
            "binding_fingerprint": run_binding.binding_fingerprint,
        },
        "evidence": [asdict(item) for item in enrollment.evidence_descriptors],
        "human": asdict(enrollment.human_descriptor) if enrollment.human_descriptor else None,
        "judgment": asdict(enrollment.judgment_descriptor),
        "same_run_automatic_retry": enrollment.same_run_automatic_retry,
        "configuration_fingerprints": asdict(configuration_fingerprints),
    }
