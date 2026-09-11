"""Inert owner-only Stockroom driver preparation.

This module binds immutable enrollment metadata to explicit production owner
objects.  It deliberately exposes no execution method and performs no I/O.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Protocol, runtime_checkable

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.evidence.service import EvidenceAdmissionService
from aiscc.human.repository import PostgresHumanAuthorityRepository
from aiscc.judgment.authority import PostgresJudgmentAuthority
from aiscc.providers.models import canonical_sha256
from aiscc.providers.service import AgentExecutionService
from aiscc.runtime.stockroom_materializer import StockroomMaterializer
from aiscc.runtime.stockroom_workspace import StockroomWorkspace
from aiscc.scenarios.enrollment import StockroomEnrollment
from aiscc.scenarios.models import RESOURCE_REF, SCENARIO_IDS, ResourceFile, manifest_sha256
from aiscc.scenarios.runtime_models import MaterializedStockroom, StockroomWorkspaceLease
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
_MATERIALIZER_FACTORY_ROLE = "STOCKROOM_MATERIALIZER_FACTORY"
_EXECUTION_SERVICE_FACTORY_ROLE = "STOCKROOM_AGENT_EXECUTION_SERVICE_FACTORY"


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
            or type(self.configuration_fingerprints) is not StockroomConfigurationFingerprints
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
class PreparedStockroomAttemptBinding:
    run_id: str
    attempt_id: str
    scenario_id: str
    request_fingerprint: str
    run_binding_fingerprint: str
    configuration_fingerprint: str
    binding_fingerprint: str

    def __post_init__(self) -> None:
        if (
            _SAFE_ID.fullmatch(self.run_id) is None
            or _SAFE_ID.fullmatch(self.attempt_id) is None
            or self.scenario_id not in SCENARIO_IDS
            or any(
                _SHA256.fullmatch(value) is None
                for value in (
                    self.request_fingerprint,
                    self.run_binding_fingerprint,
                    self.configuration_fingerprint,
                    self.binding_fingerprint,
                )
            )
            or self.binding_fingerprint != canonical_sha256(_prepared_binding_payload(self))
        ):
            raise ValueError("STOCKROOM_PREPARED_ATTEMPT_BINDING_DENIED")


@runtime_checkable
class StockroomMaterializerFactoryAuthority(Protocol):
    @property
    def semantic_role(self) -> str: ...

    @property
    def factory_ref(self) -> str: ...

    @property
    def factory_fingerprint(self) -> str: ...


@runtime_checkable
class StockroomAgentExecutionServiceFactoryAuthority(Protocol):
    @property
    def semantic_role(self) -> str: ...

    @property
    def factory_ref(self) -> str: ...

    @property
    def factory_fingerprint(self) -> str: ...


@dataclass(frozen=True, slots=True)
class StockroomMaterializerDerivationProvenance:
    factory_ref: str
    factory_fingerprint: str
    prepared_binding_fingerprint: str
    run_id: str
    attempt_id: str
    derived_owner_kind: str
    materialization_authority_ref: str
    materialization_authority_fingerprint: str
    repository_root_fingerprint: str
    runtime_root_fingerprint: str
    operation_fingerprint: str
    provenance_fingerprint: str

    def __post_init__(self) -> None:
        values = {
            "factory_ref": self.factory_ref,
            "factory_fingerprint": self.factory_fingerprint,
            "prepared_binding_fingerprint": self.prepared_binding_fingerprint,
            "run_id": self.run_id,
            "attempt_id": self.attempt_id,
            "derived_owner_kind": self.derived_owner_kind,
            "materialization_authority_ref": self.materialization_authority_ref,
            "materialization_authority_fingerprint": (self.materialization_authority_fingerprint),
            "repository_root_fingerprint": self.repository_root_fingerprint,
            "runtime_root_fingerprint": self.runtime_root_fingerprint,
            "operation_fingerprint": self.operation_fingerprint,
        }
        if (
            self.derived_owner_kind != "StockroomMaterializer"
            or not self.materialization_authority_ref
            or _SAFE_ID.fullmatch(self.run_id) is None
            or _SAFE_ID.fullmatch(self.attempt_id) is None
            or any(
                _SHA256.fullmatch(value) is None
                for value in (
                    self.factory_fingerprint,
                    self.prepared_binding_fingerprint,
                    self.materialization_authority_fingerprint,
                    self.repository_root_fingerprint,
                    self.runtime_root_fingerprint,
                    self.operation_fingerprint,
                    self.provenance_fingerprint,
                )
            )
            or self.provenance_fingerprint != canonical_sha256(values)
        ):
            raise ValueError("STOCKROOM_MATERIALIZER_PROVENANCE_DENIED")


@dataclass(frozen=True, slots=True)
class StockroomMaterializerDerivation:
    owner: StockroomMaterializer
    provenance: StockroomMaterializerDerivationProvenance

    def __post_init__(self) -> None:
        if type(self.owner) is not StockroomMaterializer:
            raise ValueError("STOCKROOM_DERIVED_MATERIALIZER_REQUIRED")


@dataclass(frozen=True, slots=True)
class StockroomMaterializedResultProvenance:
    factory_ref: str
    factory_fingerprint: str
    prepared_binding_fingerprint: str
    materializer_derivation_provenance_fingerprint: str
    run_id: str
    attempt_id: str
    resource_ref: str
    source_commit: str
    subroot: str
    git_subtree: str
    aggregate_sha256: str
    workspace_lease_fingerprint: str
    resolved_source_root_fingerprint: str
    materialized_file_manifest_fingerprint: str
    materialized_output_fingerprint: str
    provenance_fingerprint: str

    def __post_init__(self) -> None:
        values = _materialized_result_provenance_payload(self)
        if (
            not self.factory_ref
            or not self.resource_ref
            or not self.subroot
            or _SAFE_ID.fullmatch(self.run_id) is None
            or _SAFE_ID.fullmatch(self.attempt_id) is None
            or re.fullmatch(r"[0-9a-f]{40}", self.source_commit) is None
            or re.fullmatch(r"[0-9a-f]{40}", self.git_subtree) is None
            or any(
                _SHA256.fullmatch(value) is None
                for value in (
                    self.factory_fingerprint,
                    self.prepared_binding_fingerprint,
                    self.materializer_derivation_provenance_fingerprint,
                    self.aggregate_sha256,
                    self.workspace_lease_fingerprint,
                    self.resolved_source_root_fingerprint,
                    self.materialized_file_manifest_fingerprint,
                    self.materialized_output_fingerprint,
                    self.provenance_fingerprint,
                )
            )
            or self.provenance_fingerprint != canonical_sha256(values)
        ):
            raise ValueError("STOCKROOM_MATERIALIZED_RESULT_PROVENANCE_DENIED")


@dataclass(frozen=True, slots=True, eq=False)
class StockroomMaterializedResultBinding:
    materialized: MaterializedStockroom
    materializer_derivation: StockroomMaterializerDerivation
    provenance: StockroomMaterializedResultProvenance
    materialized_identity: int
    _issuer_token: object = field(repr=False, compare=False)

    def __post_init__(self) -> None:
        materialized = self.materialized
        derivation = self.materializer_derivation
        provenance = self.provenance
        if (
            type(materialized) is not MaterializedStockroom
            or type(derivation) is not StockroomMaterializerDerivation
            or type(provenance) is not StockroomMaterializedResultProvenance
            or type(self.materialized_identity) is not int
            or self.materialized_identity != id(materialized)
            or materialized.run_id != provenance.run_id
            or materialized.attempt_id != provenance.attempt_id
            or materialized.resource_ref != provenance.resource_ref
            or materialized.source_commit != provenance.source_commit
            or materialized.subroot != provenance.subroot
            or materialized.git_subtree != provenance.git_subtree
            or materialized.aggregate_sha256 != provenance.aggregate_sha256
            or materialized.workspace_lease.run_id != materialized.run_id
            or materialized.workspace_lease.attempt_id != materialized.attempt_id
            or materialized.workspace_lease.destination != materialized.resolved_source_root
            or stockroom_workspace_lease_fingerprint(materialized.workspace_lease)
            != provenance.workspace_lease_fingerprint
            or stockroom_path_fingerprint(materialized.resolved_source_root)
            != provenance.resolved_source_root_fingerprint
            or stockroom_materialized_file_manifest_fingerprint(materialized)
            != provenance.materialized_file_manifest_fingerprint
            or materialized.aggregate_sha256
            != provenance.materialized_file_manifest_fingerprint
            or stockroom_materialized_output_fingerprint(materialized)
            != provenance.materialized_output_fingerprint
            or derivation.provenance.provenance_fingerprint
            != provenance.materializer_derivation_provenance_fingerprint
        ):
            raise ValueError("STOCKROOM_MATERIALIZED_RESULT_BINDING_DENIED")


@dataclass(frozen=True, slots=True)
class StockroomAgentExecutionServiceDerivationProvenance:
    factory_ref: str
    factory_fingerprint: str
    prepared_binding_fingerprint: str
    run_id: str
    attempt_id: str
    derived_owner_kind: str
    docker_spec_fingerprint: str
    tool_registry_fingerprint: str
    dispatcher_fingerprint: str
    materialized_result_provenance_ref: str
    materialized_result_provenance_fingerprint: str
    materialized_output_fingerprint: str
    execution_reference_authority_ref: str
    provenance_fingerprint: str

    def __post_init__(self) -> None:
        values = {
            "factory_ref": self.factory_ref,
            "factory_fingerprint": self.factory_fingerprint,
            "prepared_binding_fingerprint": self.prepared_binding_fingerprint,
            "run_id": self.run_id,
            "attempt_id": self.attempt_id,
            "derived_owner_kind": self.derived_owner_kind,
            "docker_spec_fingerprint": self.docker_spec_fingerprint,
            "tool_registry_fingerprint": self.tool_registry_fingerprint,
            "dispatcher_fingerprint": self.dispatcher_fingerprint,
            "materialized_result_provenance_ref": self.materialized_result_provenance_ref,
            "materialized_result_provenance_fingerprint": (
                self.materialized_result_provenance_fingerprint
            ),
            "materialized_output_fingerprint": self.materialized_output_fingerprint,
            "execution_reference_authority_ref": self.execution_reference_authority_ref,
        }
        if (
            self.derived_owner_kind != "AgentExecutionService"
            or not self.materialized_result_provenance_ref
            or not self.execution_reference_authority_ref
            or _SAFE_ID.fullmatch(self.run_id) is None
            or _SAFE_ID.fullmatch(self.attempt_id) is None
            or any(
                _SHA256.fullmatch(value) is None
                for value in (
                    self.factory_fingerprint,
                    self.prepared_binding_fingerprint,
                    self.docker_spec_fingerprint,
                    self.tool_registry_fingerprint,
                    self.dispatcher_fingerprint,
                    self.materialized_result_provenance_fingerprint,
                    self.materialized_output_fingerprint,
                    self.provenance_fingerprint,
                )
            )
            or self.provenance_fingerprint != canonical_sha256(values)
        ):
            raise ValueError("STOCKROOM_EXECUTION_SERVICE_PROVENANCE_DENIED")


@dataclass(frozen=True, slots=True)
class StockroomAgentExecutionServiceDerivation:
    owner: AgentExecutionService
    provenance: StockroomAgentExecutionServiceDerivationProvenance

    def __post_init__(self) -> None:
        if type(self.owner) is not AgentExecutionService:
            raise ValueError("STOCKROOM_DERIVED_EXECUTION_SERVICE_REQUIRED")


@dataclass(frozen=True, slots=True)
class StockroomOwnerDependencies:
    workflow_kernel: WorkflowKernel
    agent_execution_service_factory: StockroomAgentExecutionServiceFactoryAuthority
    evidence_admission_service: EvidenceAdmissionService
    human_gate_owner: PostgresHumanAuthorityRepository
    judgment_owner: PostgresJudgmentAuthority
    workspace_owner: StockroomWorkspace
    materializer_factory: StockroomMaterializerFactoryAuthority
    security_policy: SecurityPolicy
    stockroom_owner_restriction: StockroomOwnerRestriction

    def __post_init__(self) -> None:
        requirements = (
            (self.workflow_kernel, WorkflowKernel),
            (self.evidence_admission_service, EvidenceAdmissionService),
            (self.human_gate_owner, PostgresHumanAuthorityRepository),
            (self.judgment_owner, PostgresJudgmentAuthority),
            (self.workspace_owner, StockroomWorkspace),
            (self.security_policy, SecurityPolicy),
            (self.stockroom_owner_restriction, StockroomOwnerRestriction),
        )
        if (
            any(not isinstance(value, expected) for value, expected in requirements)
            or not _factory_authority_valid(
                self.materializer_factory,
                StockroomMaterializerFactoryAuthority,
                _MATERIALIZER_FACTORY_ROLE,
            )
            or not _factory_authority_valid(
                self.agent_execution_service_factory,
                StockroomAgentExecutionServiceFactoryAuthority,
                _EXECUTION_SERVICE_FACTORY_ROLE,
            )
        ):
            raise ValueError("STOCKROOM_REAL_OWNER_DEPENDENCY_REQUIRED")


@dataclass(frozen=True, slots=True)
class PreparedStockroomDriver:
    request: StockroomDriverRequest
    owners: StockroomOwnerDependencies
    attempt_binding: PreparedStockroomAttemptBinding

    def __post_init__(self) -> None:
        if (
            type(self.request) is not StockroomDriverRequest
            or type(self.owners) is not StockroomOwnerDependencies
            or type(self.attempt_binding) is not PreparedStockroomAttemptBinding
            or self.attempt_binding != build_prepared_attempt_binding(self.request)
        ):
            raise ValueError("STOCKROOM_PREPARED_DRIVER_BINDING_DENIED")


class StockroomCaptureStatus(StrEnum):
    COMPLETED = "COMPLETED"
    STOPPED = "STOPPED"


@dataclass(frozen=True, slots=True)
class StockroomCaptureProgressRef:
    owner: str
    operation: str
    owner_ref: str
    status: str
    workflow_state: WorkflowState
    state_version: int


@dataclass(frozen=True, slots=True)
class StockroomCaptureResult:
    scenario_id: str
    run_id: str
    attempt_id: str
    status: StockroomCaptureStatus
    workflow_state: WorkflowState
    state_version: int
    progress: tuple[StockroomCaptureProgressRef, ...]
    evidence_refs: tuple[str, ...] = ()
    human_gate_ref: str | None = None
    human_result_ref: None = None
    judgment_ref: str | None = None
    stop_reason: str | None = None
    retry_requires_new_attempt: bool = False


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
    *,
    attempt_binding: PreparedStockroomAttemptBinding | None = None,
) -> PreparedStockroomDriver:
    """Bind explicit existing owners without invoking any of them."""
    binding = attempt_binding or build_prepared_attempt_binding(request)
    return PreparedStockroomDriver(request=request, owners=owners, attempt_binding=binding)


def build_prepared_attempt_binding(
    request: StockroomDriverRequest,
) -> PreparedStockroomAttemptBinding:
    if type(request) is not StockroomDriverRequest:
        raise ValueError("STOCKROOM_DRIVER_REQUEST_REQUIRED")
    values = {
        "run_id": request.run_binding.run_id,
        "attempt_id": request.run_binding.attempt_id,
        "scenario_id": request.scenario_id,
        "request_fingerprint": request.request_fingerprint,
        "run_binding_fingerprint": request.run_binding.binding_fingerprint,
        "configuration_fingerprint": (request.configuration_fingerprints.composition_sha256),
    }
    return PreparedStockroomAttemptBinding(
        **values,
        binding_fingerprint=canonical_sha256(values),
    )


def require_prepared_attempt_binding(
    prepared: PreparedStockroomDriver,
) -> PreparedStockroomAttemptBinding:
    if type(prepared) is not PreparedStockroomDriver:
        raise ValueError("STOCKROOM_PREPARED_DRIVER_REQUIRED")
    expected = build_prepared_attempt_binding(prepared.request)
    if prepared.attempt_binding != expected:
        raise ValueError("STOCKROOM_PREPARED_ATTEMPT_BINDING_DENIED")
    return prepared.attempt_binding


def _prepared_binding_payload(
    binding: PreparedStockroomAttemptBinding,
) -> dict[str, str]:
    return {
        "run_id": binding.run_id,
        "attempt_id": binding.attempt_id,
        "scenario_id": binding.scenario_id,
        "request_fingerprint": binding.request_fingerprint,
        "run_binding_fingerprint": binding.run_binding_fingerprint,
        "configuration_fingerprint": binding.configuration_fingerprint,
    }


def stockroom_path_fingerprint(path: object) -> str:
    return canonical_sha256({"absolute_path": str(path)})


def stockroom_workspace_lease_fingerprint(lease: StockroomWorkspaceLease) -> str:
    if type(lease) is not StockroomWorkspaceLease:
        raise ValueError("STOCKROOM_WORKSPACE_LEASE_REQUIRED")
    return canonical_sha256(
        {
            "lease_id": lease.lease_id,
            "run_id": lease.run_id,
            "attempt_id": lease.attempt_id,
            "runtime_root_fingerprint": stockroom_path_fingerprint(lease.runtime_root),
            "destination_fingerprint": stockroom_path_fingerprint(lease.destination),
            "ownership": lease.ownership.value,
        }
    )


def stockroom_materialized_file_manifest_fingerprint(
    materialized: MaterializedStockroom,
) -> str:
    if type(materialized) is not MaterializedStockroom:
        raise ValueError("STOCKROOM_MATERIALIZED_RESULT_REQUIRED")
    files = tuple(
        ResourceFile(path=item.path, mode=item.mode, bytes=item.bytes, sha256=item.sha256)
        for item in materialized.files
    )
    return manifest_sha256(files)


def stockroom_materialized_output_fingerprint(materialized: MaterializedStockroom) -> str:
    if type(materialized) is not MaterializedStockroom:
        raise ValueError("STOCKROOM_MATERIALIZED_RESULT_REQUIRED")
    return canonical_sha256(
        {
            "resource_ref": materialized.resource_ref,
            "source_commit": materialized.source_commit,
            "subroot": materialized.subroot,
            "git_subtree": materialized.git_subtree,
            "aggregate_sha256": materialized.aggregate_sha256,
            "materialized_file_manifest_fingerprint": (
                stockroom_materialized_file_manifest_fingerprint(materialized)
            ),
            "workspace_lease_fingerprint": stockroom_workspace_lease_fingerprint(
                materialized.workspace_lease
            ),
            "run_id": materialized.run_id,
            "attempt_id": materialized.attempt_id,
            "resolved_source_root_fingerprint": stockroom_path_fingerprint(
                materialized.resolved_source_root
            ),
        }
    )


def _materialized_result_provenance_payload(
    provenance: StockroomMaterializedResultProvenance,
) -> dict[str, str]:
    return {
        "factory_ref": provenance.factory_ref,
        "factory_fingerprint": provenance.factory_fingerprint,
        "prepared_binding_fingerprint": provenance.prepared_binding_fingerprint,
        "materializer_derivation_provenance_fingerprint": (
            provenance.materializer_derivation_provenance_fingerprint
        ),
        "run_id": provenance.run_id,
        "attempt_id": provenance.attempt_id,
        "resource_ref": provenance.resource_ref,
        "source_commit": provenance.source_commit,
        "subroot": provenance.subroot,
        "git_subtree": provenance.git_subtree,
        "aggregate_sha256": provenance.aggregate_sha256,
        "workspace_lease_fingerprint": provenance.workspace_lease_fingerprint,
        "resolved_source_root_fingerprint": provenance.resolved_source_root_fingerprint,
        "materialized_file_manifest_fingerprint": (
            provenance.materialized_file_manifest_fingerprint
        ),
        "materialized_output_fingerprint": provenance.materialized_output_fingerprint,
    }


def _factory_authority_valid(
    value: object,
    authority_type: type[StockroomMaterializerFactoryAuthority]
    | type[StockroomAgentExecutionServiceFactoryAuthority],
    expected_role: str,
) -> bool:
    return bool(
        isinstance(value, authority_type)
        and value.semantic_role == expected_role
        and _SAFE_ID.fullmatch(value.factory_ref) is not None
        and _SHA256.fullmatch(value.factory_fingerprint) is not None
    )


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
