"""PostgreSQL-backed Stockroom production composition and A1 owner adapter."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from pathlib import Path
from types import MappingProxyType
from typing import Any, cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.contracts.security import (
    AuthorityStatus,
    PermissionRequest,
    ResourceDomain,
    ResourceGrant,
    ResourceScope,
    SecurityActionClass,
    SecurityAdmissionDecision,
    SecurityDecision,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.evidence.admission import (
    EVIDENCE_AUTHORITY_VERSION,
    EvidenceAdmissionEvaluator,
    EvidenceContentRegistry,
    make_admission_request,
)
from aiscc.evidence.attestation import EvidenceCheckpointUseRegistry, EvidenceGuardAuthority
from aiscc.evidence.content import (
    P1_6DurableContentAuthority,
    source_owner_authority_fingerprint,
)
from aiscc.evidence.issuers import (
    EvidenceIssuerRegistry,
    P1_5EvidenceIssuerAuthority,
    TokenEvidenceIssuer,
)
from aiscc.evidence.models import (
    AdmittedEvidenceRef,
    DurableContentRequirement,
    EvidenceAdmissionOutcome,
    EvidenceCandidate,
    EvidenceCheckpoint,
    EvidenceCheckpointRef,
    EvidenceContentKind,
    EvidenceContentRef,
    EvidenceIssuerType,
    EvidenceOwner,
    EvidenceRequirement,
    EvidenceRequirementProfile,
    EvidenceRequirementRef,
    EvidenceRequirementSet,
    EvidenceSemanticOwner,
    EvidenceSensitivity,
    EvidenceSetEvaluation,
    EvidenceSetOutcome,
    FreshnessPolicy,
    FreshnessPolicyKind,
    RequirementFingerprintSchema,
    RequirementObligation,
    canonical_hash,
)
from aiscc.evidence.repository import PostgresEvidenceRepository
from aiscc.evidence.requirements import TaskContractEvidenceAuthority
from aiscc.evidence.service import EvidenceAdmissionService
from aiscc.evidence.set_evaluator import EvidenceSetEvaluator
from aiscc.human.authority import HumanGateReservationAuthority, HumanGuardAuthority
from aiscc.human.repository import PostgresHumanAuthorityRepository
from aiscc.judgment.authority import (
    CommandCenterAuthority,
    JudgmentPolicyAuthority,
    PostgresJudgmentAuthority,
)
from aiscc.judgment.models import (
    JudgmentEvidenceBasisKind,
    JudgmentKind,
    JudgmentOwnerPolicy,
    JudgmentPolicy,
)
from aiscc.persistence.models import ExecutionOutputRefRow, TransitionDecisionRow
from aiscc.persistence.repository import (
    PostgresExecutionRepository,
    PostgresTransitionRepository,
    acquire_work_run_transaction_lock,
    verify_historical_transition_provenance,
)
from aiscc.providers.authority import (
    ExecutionReferenceAuthority,
    LeaseBoundSecretResolver,
    ProviderToolResourceAuthority,
    SecretResolutionLeaseAuthority,
    SecretUseAuthority,
)
from aiscc.providers.local_deterministic import (
    LOCAL_COMPATIBILITY_SECRET_REF,
    LOCAL_COMPATIBILITY_SENTINEL,
    STOCKROOM_SUMMARY,
    LocalDeterministicProvider,
)
from aiscc.providers.models import (
    ExecutionAttemptRef,
    ExecutionStatus,
    ToolRegistry,
    canonical_json_bytes,
    canonical_sha256,
)
from aiscc.providers.service import AgentExecutionService, DurableExecutionResult
from aiscc.providers.stockroom_tool import (
    StockroomSummaryDispatcher,
    build_dispatch_context,
    build_stockroom_registry,
    build_stockroom_spec,
    load_stockroom_tool_config,
)
from aiscc.runtime.docker import (
    DockerRunSpec,
    DockerRuntime,
    StockroomCancellation,
    StockroomDockerRunner,
    stockroom_spec_fingerprint,
)
from aiscc.runtime.stockroom_image import (
    StockroomImageProvenanceRef,
    resolve_stockroom_image,
)
from aiscc.runtime.stockroom_materializer import (
    StockroomMaterializer,
)
from aiscc.runtime.stockroom_materializer import (
    operation_fingerprint as materialization_operation_fingerprint,
)
from aiscc.runtime.stockroom_workspace import StockroomWorkspace
from aiscc.scenarios.capture_runner import OwnerCallResult, StockroomCaptureRunner
from aiscc.scenarios.composition import (
    StockroomOwnerComposition,
    bind_stockroom_owner_dependencies,
    build_stockroom_production_composition,
)
from aiscc.scenarios.driver import (
    PreparedStockroomDriver,
    StockroomAgentExecutionServiceDerivation,
    StockroomAgentExecutionServiceDerivationProvenance,
    StockroomMaterializedResultBinding,
    StockroomMaterializedResultProvenance,
    StockroomMaterializerDerivation,
    StockroomMaterializerDerivationProvenance,
    StockroomOwnerDependencies,
    build_prepared_attempt_binding,
    prepare_stockroom_driver,
    require_prepared_attempt_binding,
    stockroom_materialized_file_manifest_fingerprint,
    stockroom_materialized_output_fingerprint,
    stockroom_path_fingerprint,
    stockroom_workspace_lease_fingerprint,
)
from aiscc.scenarios.models import RESOURCE_REF, SCENARIO_IDS, PolicyConflictFixture
from aiscc.scenarios.runtime_models import (
    MaterializationAuthority,
    MaterializedStockroom,
    StockroomFailure,
    StockroomRunBinding,
)
from aiscc.security.capability import Capability
from aiscc.security.policy import SecurityPolicy
from aiscc.security.stockroom_policy import StockroomOwnerRestriction, StockroomSecurityContext
from aiscc.workflow.evaluator import TransitionEvaluator
from aiscc.workflow.guards import (
    GUARD_OWNER_POLICY,
    P1_4GuardAuthority,
    TrustedGuardFact,
    decode_execution_bound_refs,
)
from aiscc.workflow.kernel import WorkflowKernel
from aiscc.workflow.matrix import TRANSITION_MATRIX
from aiscc.workflow.models import (
    AuthorityConflictError,
    BlockerKindV1,
    BlockerReasonCodeV1,
    DecisionOutcome,
    GuardId,
    GuardSemanticOwner,
    P1_4BlockerClaimV1,
    RequesterType,
    TransitionDecision,
    TransitionEvaluation,
    TransitionRequest,
    WorkRun,
)
from aiscc.workflow.ports import TransitionTransactionParticipant

_EVIDENCE_CONFIG = Path("config/evidence/stockroom-capture.v1.json")
_HUMAN_CONFIG = Path("config/human/stockroom-capture.v1.json")
_JUDGMENT_CONFIG = Path("config/judgment/stockroom-capture.v2.json")
_POLICY_CONFLICT_FIXTURE = Path("config/scenarios/stockroom/v1/fixtures/policy-conflict.json")
_SECURITY_PROFILE_VERSION = "p1-3-v2"
_RUNTIME_ISSUER_ID = "AISCC_STOCKROOM_RUNTIME_OBSERVATION_ISSUER_V1"
_STATIC_ISSUER_ID = "AISCC_STOCKROOM_STATIC_POLICY_ISSUER_V1"
_AGENT_ISSUER_ID = "AISCC_STOCKROOM_P1_5_AGENT_OUTPUT_ISSUER_V1"
_SHA256 = frozenset("0123456789abcdef")


@dataclass(frozen=True, slots=True)
class StockroomEvidenceEnrollment:
    scenario_id: str
    scenario_version: str
    requirement_set: EvidenceRequirementSet
    requirement: EvidenceRequirement
    checkpoint: EvidenceCheckpoint
    issuer: TokenEvidenceIssuer


@dataclass(frozen=True, slots=True)
class StockroomHumanEnrollment:
    scenario_id: str
    scenario_version: str
    task_contract_id: str
    task_contract_version: str
    source_state: WorkflowState
    target_state: WorkflowState
    purpose_id: str
    purpose_version: str
    selector_slot: str


@dataclass(frozen=True, slots=True)
class StockroomJudgmentEnrollment:
    scenario_id: str
    scenario_version: str
    policy: JudgmentPolicy


@dataclass(frozen=True, slots=True)
class StockroomSecurityAuthorization:
    binding: StockroomRunBinding
    operation_fingerprint: str
    repository_scope: ResourceScope
    filesystem_scope: ResourceScope
    repository_context: StockroomSecurityContext
    filesystem_context: StockroomSecurityContext
    repository_grant: ResourceGrant
    filesystem_grant: ResourceGrant
    repository_decision: SecurityDecision
    filesystem_decision: SecurityDecision
    repository_capability: Capability
    filesystem_capability: Capability
    network_grant_issued: bool


@dataclass(slots=True)
class StockroomPreparedCapture:
    prepared: PreparedStockroomDriver
    adapter: StockroomCaptureOwnerAdapter
    runner: StockroomCaptureRunner
    materializer: StockroomMaterializer | None = None
    agent_execution_service: AgentExecutionService | None = None
    materializer_derivation: StockroomMaterializerDerivation | None = None
    materialized_result: StockroomMaterializedResultBinding | None = None
    execution_service_derivation: StockroomAgentExecutionServiceDerivation | None = None


@dataclass(frozen=True, slots=True)
class _SealedSecurity:
    binding: StockroomRunBinding
    operation_fingerprint: str
    repository_scope: ResourceScope
    filesystem_scope: ResourceScope
    repository_context: StockroomSecurityContext
    filesystem_context: StockroomSecurityContext


@dataclass(frozen=True, slots=True)
class _MaterializedRuntime:
    materialized: MaterializedStockroom
    materializer_derivation: StockroomMaterializerDerivation
    materialized_result: StockroomMaterializedResultBinding
    execution_inputs: _StockroomExecutionFactoryInputs
    execution_derivation: StockroomAgentExecutionServiceDerivation


class _CurrentBinding:
    def __init__(self) -> None:
        self.value: StockroomRunBinding | None = None

    def require(self) -> StockroomRunBinding:
        if self.value is None:
            raise StockroomFailure("CURRENT_BINDING_UNAVAILABLE")
        return self.value


class _CurrentAttemptReader:
    def __init__(self) -> None:
        self.current: WorkflowSnapshot | None = None
        self.attempt: ExecutionAttemptRef | None = None

    def load(self, *, work_run_id: str, execution_attempt_id: str):
        if (
            self.current is None
            or self.attempt is None
            or self.current.run_id != work_run_id
            or self.attempt.execution_attempt_id != execution_attempt_id
        ):
            raise AuthorityConflictError("attempt authority snapshot is unavailable")
        return self.current, self.attempt


class _CompositeTransitionParticipant:
    """Combines existing owner hooks without issuing or changing their facts."""

    def __init__(self, participants: Sequence[TransitionTransactionParticipant]) -> None:
        if not participants:
            raise ValueError("composite participant requires existing owner participants")
        self._participants = tuple(participants)

    def facts(self, request: TransitionRequest) -> tuple[TrustedGuardFact, ...]:
        return tuple(
            fact for participant in self._participants for fact in participant.facts(request)
        )

    async def prepare(
        self, session: AsyncSession, request: TransitionRequest, current: WorkRun | None
    ) -> None:
        for participant in self._participants:
            await participant.prepare(session, request, current)

    def after_evaluation(self, request: TransitionRequest) -> None:
        for participant in self._participants:
            participant.after_evaluation(request)

    async def after_decision(
        self,
        session: AsyncSession,
        request: TransitionRequest,
        evaluation: TransitionEvaluation,
        decision: TransitionDecision,
        current: WorkRun | None,
    ) -> None:
        for participant in self._participants:
            await participant.after_decision(session, request, evaluation, decision, current)


@dataclass(slots=True)
class StockroomProductionApplication:
    session_factory: async_sessionmaker[AsyncSession]
    repository_root: Path
    private_runtime_root: Path
    downloads_root: Path
    trusted_git_executable: Path
    project_id: str
    requester_identity: str
    human_selector_fingerprint: str
    composition: StockroomOwnerComposition
    execution_repository: PostgresExecutionRepository
    evidence_repository: PostgresEvidenceRepository
    evidence_service: EvidenceAdmissionService
    evidence_set_evaluator: EvidenceSetEvaluator
    evidence_checkpoint_uses: EvidenceCheckpointUseRegistry
    evidence_guard_authority: EvidenceGuardAuthority
    evidence_enrollments: Mapping[str, StockroomEvidenceEnrollment]
    runtime_evidence_issuer: TokenEvidenceIssuer
    static_evidence_issuer: TokenEvidenceIssuer
    agent_evidence_issuer: P1_5EvidenceIssuerAuthority
    durable_content_authority: P1_6DurableContentAuthority
    human_repository: PostgresHumanAuthorityRepository
    human_reservation_authority: HumanGateReservationAuthority
    human_guard_authority: HumanGuardAuthority
    human_enrollment: StockroomHumanEnrollment
    judgment_policy_authority: JudgmentPolicyAuthority
    command_center_authority: CommandCenterAuthority
    judgment_authority: PostgresJudgmentAuthority
    judgment_enrollments: Mapping[str, StockroomJudgmentEnrollment]
    p1_4_guard_authority: P1_4GuardAuthority
    transition_repository: PostgresTransitionRepository
    workflow_kernel: WorkflowKernel
    provider_tool_authority: ProviderToolResourceAuthority
    secret_use_authority: SecretUseAuthority
    secret_lease_authority: SecretResolutionLeaseAuthority
    secret_resolver: LeaseBoundSecretResolver
    execution_reference_authority: ExecutionReferenceAuthority
    stockroom_owner_restriction: StockroomOwnerRestriction
    security_policy: SecurityPolicy
    local_provider: LocalDeterministicProvider
    workspace: StockroomWorkspace
    docker_runtime: DockerRuntime
    static_policy_fixture: Mapping[str, object]
    clock: Callable[[], datetime]
    cancellation: StockroomCancellation

    def prepare_capture(
        self,
        *,
        scenario_id: str,
        run_id: str,
        attempt_id: str,
    ) -> StockroomPreparedCapture:
        if scenario_id not in SCENARIO_IDS:
            raise ValueError("UNKNOWN_STOCKROOM_SCENARIO")
        binding = _CurrentBinding()
        reader = _CurrentAttemptReader()
        request = self.composition.request(
            scenario_id=scenario_id,
            run_id=run_id,
            attempt_id=attempt_id,
            expected_initial_state_version=1,
        )
        attempt_binding = build_prepared_attempt_binding(request)
        materializer_factory = StockroomMaterializerFactory(self, binding)
        execution_factory = StockroomAgentExecutionServiceFactory(self, reader)
        owners = StockroomOwnerDependencies(
            workflow_kernel=self.workflow_kernel,
            agent_execution_service_factory=execution_factory,
            evidence_admission_service=self.evidence_service,
            human_gate_owner=self.human_repository,
            judgment_owner=self.judgment_authority,
            workspace_owner=self.workspace,
            materializer_factory=materializer_factory,
            security_policy=self.security_policy,
            stockroom_owner_restriction=self.stockroom_owner_restriction,
        )
        bind_stockroom_owner_dependencies(self.composition, owners)
        prepared = prepare_stockroom_driver(
            request,
            owners,
            attempt_binding=attempt_binding,
        )
        capture = StockroomPreparedCapture(
            prepared=prepared,
            adapter=cast(Any, None),
            runner=cast(Any, None),
        )
        adapter = StockroomCaptureOwnerAdapter(self, capture, binding, reader)
        capture.adapter = adapter
        capture.runner = StockroomCaptureRunner(adapter)
        return capture


@dataclass(frozen=True, slots=True, eq=False)
class StockroomMaterializerFactory:
    """Exact prepared authority for attempt-scoped materializer derivation."""

    _application: StockroomProductionApplication = field(repr=False)
    _current_binding: _CurrentBinding = field(repr=False)
    _issuer_token: object = field(default_factory=object, init=False, repr=False, compare=False)
    _issued_results: dict[str, StockroomMaterializedResultBinding] = field(
        default_factory=dict, init=False, repr=False, compare=False
    )
    factory_ref: str = field(init=False)
    factory_fingerprint: str = field(init=False)

    semantic_role = "STOCKROOM_MATERIALIZER_FACTORY"

    def __post_init__(self) -> None:
        fingerprint = _production_factory_fingerprint(self.semantic_role, self._application)
        object.__setattr__(self, "factory_fingerprint", fingerprint)
        object.__setattr__(
            self, "factory_ref", f"stockroom-materializer-factory-{fingerprint[:40]}"
        )

    def derive(
        self,
        *,
        prepared: PreparedStockroomDriver,
        authorization: StockroomSecurityAuthorization,
        authority: MaterializationAuthority,
        repository_root: Path,
        private_runtime_root: Path,
    ) -> StockroomMaterializerDerivation:
        binding = require_prepared_attempt_binding(prepared)
        application = self._application
        current = self._current_binding.require()
        if (
            prepared.owners.materializer_factory is not self
            or type(authorization) is not StockroomSecurityAuthorization
            or type(authority) is not MaterializationAuthority
            or repository_root != application.repository_root
            or private_runtime_root != application.private_runtime_root
            or current != authorization.binding
            or authority.binding != current
            or binding.run_id != current.run_id
            or binding.attempt_id != current.attempt_id
            or binding.scenario_id != current.scenario_id
            or binding.configuration_fingerprint != current.config_sha256
            or authority.principal_ref != application.requester_identity
            or authority.security_admission_ref != authorization.repository_decision.admission_id
            or authority.repository_grant_ref != authorization.repository_grant.grant_id
            or authority.filesystem_grant_ref != authorization.filesystem_grant.grant_id
            or authority.operation_fingerprint != authorization.operation_fingerprint
            or authority.repository_root != repository_root
            or authority.runtime_root != private_runtime_root
            or authorization.repository_context.run_id != binding.run_id
            or authorization.repository_context.attempt_id != binding.attempt_id
            or authorization.filesystem_context.run_id != binding.run_id
            or authorization.filesystem_context.attempt_id != binding.attempt_id
            or authorization.repository_context.operation_fingerprint
            != authority.operation_fingerprint
            or authorization.filesystem_context.operation_fingerprint
            != authority.operation_fingerprint
        ):
            raise AuthorityConflictError("prepared materializer factory binding mismatch")
        expected_operation = materialization_operation_fingerprint(
            current, repository_root, private_runtime_root
        )
        if authority.operation_fingerprint != expected_operation:
            raise AuthorityConflictError("materializer operation fingerprint mismatch")

        authority_fingerprint = _materialization_authority_fingerprint(authority)
        provenance_values = {
            "factory_ref": self.factory_ref,
            "factory_fingerprint": self.factory_fingerprint,
            "prepared_binding_fingerprint": binding.binding_fingerprint,
            "run_id": binding.run_id,
            "attempt_id": binding.attempt_id,
            "derived_owner_kind": "StockroomMaterializer",
            "materialization_authority_ref": authority.security_admission_ref,
            "materialization_authority_fingerprint": authority_fingerprint,
            "repository_root_fingerprint": _path_fingerprint(repository_root),
            "runtime_root_fingerprint": _path_fingerprint(private_runtime_root),
            "operation_fingerprint": authority.operation_fingerprint,
        }
        provenance = StockroomMaterializerDerivationProvenance(
            **provenance_values,
            provenance_fingerprint=canonical_sha256(provenance_values),
        )
        owner = StockroomMaterializer(
            repository_root=repository_root,
            git_executable=application.trusted_git_executable,
            workspace=application.workspace,
            registered_authorities=(authority,),
            current_binding=self._current_binding.require,
        )
        return StockroomMaterializerDerivation(owner, provenance)

    def materialize(
        self,
        *,
        prepared: PreparedStockroomDriver,
        authorization: StockroomSecurityAuthorization,
        authority: MaterializationAuthority,
        repository_root: Path,
        private_runtime_root: Path,
    ) -> StockroomMaterializedResultBinding:
        """Derive the exact owner, call it, and bind only its immediate return value."""
        derivation = self.derive(
            prepared=prepared,
            authorization=authorization,
            authority=authority,
            repository_root=repository_root,
            private_runtime_root=private_runtime_root,
        )
        materialized = derivation.owner.materialize(authorization.binding, authority)
        return self._issue_materialized_result(
            prepared=prepared,
            materialized=materialized,
            derivation=derivation,
        )

    def require_issued_result(
        self,
        *,
        prepared: PreparedStockroomDriver,
        result: object,
    ) -> StockroomMaterializedResultBinding:
        if type(result) is not StockroomMaterializedResultBinding:
            raise AuthorityConflictError("factory-issued materialized result required")
        typed_result = cast(StockroomMaterializedResultBinding, result)
        self._validate_materialized_result_components(
            prepared=prepared,
            materialized=typed_result.materialized,
            derivation=typed_result.materializer_derivation,
        )
        expected_provenance = self._materialized_result_provenance(
            prepared=prepared,
            materialized=typed_result.materialized,
            derivation=typed_result.materializer_derivation,
        )
        if (
            typed_result._issuer_token is not self._issuer_token
            or typed_result.materialized_identity != id(typed_result.materialized)
            or typed_result.provenance != expected_provenance
            or self._issued_results.get(expected_provenance.provenance_fingerprint)
            is not typed_result
        ):
            raise AuthorityConflictError("materialized result issuance binding mismatch")
        return typed_result

    def _issue_materialized_result(
        self,
        *,
        prepared: PreparedStockroomDriver,
        materialized: MaterializedStockroom,
        derivation: StockroomMaterializerDerivation,
    ) -> StockroomMaterializedResultBinding:
        self._validate_materialized_result_components(
            prepared=prepared,
            materialized=materialized,
            derivation=derivation,
        )
        provenance = self._materialized_result_provenance(
            prepared=prepared,
            materialized=materialized,
            derivation=derivation,
        )
        if provenance.provenance_fingerprint in self._issued_results:
            raise AuthorityConflictError("materialized result already issued")
        result = StockroomMaterializedResultBinding(
            materialized=materialized,
            materializer_derivation=derivation,
            provenance=provenance,
            materialized_identity=id(materialized),
            _issuer_token=self._issuer_token,
        )
        self._issued_results[provenance.provenance_fingerprint] = result
        return result

    def _validate_materialized_result_components(
        self,
        *,
        prepared: PreparedStockroomDriver,
        materialized: MaterializedStockroom,
        derivation: StockroomMaterializerDerivation,
    ) -> None:
        binding = require_prepared_attempt_binding(prepared)
        current = self._current_binding.require()
        resource = self._application.composition.catalog.resource
        if (
            type(materialized) is not MaterializedStockroom
            or type(derivation) is not StockroomMaterializerDerivation
        ):
            raise AuthorityConflictError("materialized result authority mismatch")
        expected_files = tuple(
            (item.path, item.mode, item.bytes, item.sha256) for item in resource.files
        )
        actual_files = tuple(
            (item.path, item.mode, item.bytes, item.sha256) for item in materialized.files
        )
        try:
            materialized.resolved_source_root.relative_to(self._application.private_runtime_root)
        except (AttributeError, ValueError):
            raise AuthorityConflictError("materialized workspace destination mismatch") from None
        provenance = derivation.provenance
        if (
            prepared.owners.materializer_factory is not self
            or provenance.factory_ref != self.factory_ref
            or provenance.factory_fingerprint != self.factory_fingerprint
            or provenance.prepared_binding_fingerprint != binding.binding_fingerprint
            or provenance.run_id != binding.run_id
            or provenance.attempt_id != binding.attempt_id
            or current.run_id != binding.run_id
            or current.attempt_id != binding.attempt_id
            or current.resource_ref != prepared.request.resource_ref
            or materialized.run_id != binding.run_id
            or materialized.attempt_id != binding.attempt_id
            or materialized.resource_ref != resource.resource_ref
            or materialized.resource_ref != prepared.request.resource_ref
            or materialized.source_commit != resource.source_commit
            or materialized.subroot != resource.subroot
            or materialized.git_subtree != resource.git_subtree
            or materialized.aggregate_sha256 != resource.aggregate_sha256
            or actual_files != expected_files
            or stockroom_materialized_file_manifest_fingerprint(materialized)
            != resource.aggregate_sha256
            or materialized.workspace_lease.run_id != binding.run_id
            or materialized.workspace_lease.attempt_id != binding.attempt_id
            or materialized.workspace_lease.runtime_root != self._application.private_runtime_root
            or materialized.workspace_lease.destination != materialized.resolved_source_root
            or materialized.workspace_lease.ownership.value != "OWNED"
        ):
            raise AuthorityConflictError("materialized result authority mismatch")

    def _materialized_result_provenance(
        self,
        *,
        prepared: PreparedStockroomDriver,
        materialized: MaterializedStockroom,
        derivation: StockroomMaterializerDerivation,
    ) -> StockroomMaterializedResultProvenance:
        binding = require_prepared_attempt_binding(prepared)
        values = {
            "factory_ref": self.factory_ref,
            "factory_fingerprint": self.factory_fingerprint,
            "prepared_binding_fingerprint": binding.binding_fingerprint,
            "materializer_derivation_provenance_fingerprint": (
                derivation.provenance.provenance_fingerprint
            ),
            "run_id": materialized.run_id,
            "attempt_id": materialized.attempt_id,
            "resource_ref": materialized.resource_ref,
            "source_commit": materialized.source_commit,
            "subroot": materialized.subroot,
            "git_subtree": materialized.git_subtree,
            "aggregate_sha256": materialized.aggregate_sha256,
            "workspace_lease_fingerprint": stockroom_workspace_lease_fingerprint(
                materialized.workspace_lease
            ),
            "resolved_source_root_fingerprint": stockroom_path_fingerprint(
                materialized.resolved_source_root
            ),
            "materialized_file_manifest_fingerprint": (
                stockroom_materialized_file_manifest_fingerprint(materialized)
            ),
            "materialized_output_fingerprint": stockroom_materialized_output_fingerprint(
                materialized
            ),
        }
        return StockroomMaterializedResultProvenance(
            **values,
            provenance_fingerprint=canonical_sha256(values),
        )


@dataclass(frozen=True, slots=True)
class _StockroomExecutionFactoryInputs:
    prepared_binding_fingerprint: str
    materialized_result: StockroomMaterializedResultBinding
    spec: DockerRunSpec
    registry: ToolRegistry
    dispatcher: StockroomSummaryDispatcher
    docker_spec_fingerprint: str
    tool_registry_fingerprint: str
    dispatcher_fingerprint: str
    spec_identity: int
    registry_identity: int
    dispatcher_identity: int
    materialized_result_identity: int
    _issuer_token: object = field(repr=False, compare=False)


@dataclass(frozen=True, slots=True, eq=False)
class StockroomAgentExecutionServiceFactory:
    """Exact prepared authority for post-materialization execution-owner derivation."""

    _application: StockroomProductionApplication = field(repr=False)
    _current_reader: _CurrentAttemptReader = field(repr=False)
    _issuer_token: object = field(default_factory=object, init=False, repr=False, compare=False)
    factory_ref: str = field(init=False)
    factory_fingerprint: str = field(init=False)

    semantic_role = "STOCKROOM_AGENT_EXECUTION_SERVICE_FACTORY"

    def __post_init__(self) -> None:
        fingerprint = _production_factory_fingerprint(self.semantic_role, self._application)
        object.__setattr__(self, "factory_fingerprint", fingerprint)
        object.__setattr__(self, "factory_ref", f"stockroom-execution-factory-{fingerprint[:40]}")

    def prepare_inputs(
        self,
        *,
        prepared: PreparedStockroomDriver,
        materialized_result: object,
    ) -> _StockroomExecutionFactoryInputs:
        binding = require_prepared_attempt_binding(prepared)
        materializer_factory = prepared.owners.materializer_factory
        if (
            prepared.owners.agent_execution_service_factory is not self
            or type(materializer_factory) is not StockroomMaterializerFactory
            or type(materialized_result) is not StockroomMaterializedResultBinding
        ):
            raise AuthorityConflictError("execution factory materialization binding mismatch")
        bound_result = materializer_factory.require_issued_result(
            prepared=prepared,
            result=materialized_result,
        )
        materialized = bound_result.materialized
        cancellation = self._application.cancellation
        if (binding.run_id, binding.attempt_id) != (cancellation.run_id, cancellation.attempt_id):
            raise ValueError("STOCKROOM_CANCELLATION_BINDING_DENIED")
        spec = build_stockroom_spec(
            self._application.composition.tool_config,
            name=f"aiscc-{binding.attempt_id}",
            run_id=binding.run_id,
            workspace=materialized.workspace_lease.destination,
            image_provenance=self._application.composition.image_provenance,
        )
        registry = build_stockroom_registry(self._application.composition.tool_config, spec)
        dispatcher = StockroomSummaryDispatcher(self._application.docker_runtime, spec)
        spec_fingerprint = stockroom_spec_fingerprint(spec)
        registry_fingerprint = _tool_registry_fingerprint(registry, spec, self._application)
        dispatcher_fingerprint = canonical_sha256(
            {
                "dispatcher": "StockroomSummaryDispatcher",
                "dispatcher_version": self._application.composition.tool_config.dispatcher_version,
                "docker_spec_fingerprint": spec_fingerprint,
            }
        )
        return _StockroomExecutionFactoryInputs(
            binding.binding_fingerprint,
            bound_result,
            spec,
            registry,
            dispatcher,
            spec_fingerprint,
            registry_fingerprint,
            dispatcher_fingerprint,
            id(spec),
            id(registry),
            id(dispatcher),
            id(bound_result),
            self._issuer_token,
        )

    def derive(
        self,
        *,
        prepared: PreparedStockroomDriver,
        inputs: _StockroomExecutionFactoryInputs,
        execution_reference_authority: ExecutionReferenceAuthority,
    ) -> StockroomAgentExecutionServiceDerivation:
        binding = require_prepared_attempt_binding(prepared)
        application = self._application
        materializer_factory = prepared.owners.materializer_factory
        if (
            prepared.owners.agent_execution_service_factory is not self
            or type(inputs) is not _StockroomExecutionFactoryInputs
            or type(materializer_factory) is not StockroomMaterializerFactory
            or inputs._issuer_token is not self._issuer_token
            or inputs.prepared_binding_fingerprint != binding.binding_fingerprint
            or inputs.materialized_result_identity != id(inputs.materialized_result)
            or inputs.spec_identity != id(inputs.spec)
            or inputs.registry_identity != id(inputs.registry)
            or inputs.dispatcher_identity != id(inputs.dispatcher)
            or inputs.docker_spec_fingerprint != stockroom_spec_fingerprint(inputs.spec)
            or inputs.tool_registry_fingerprint
            != _tool_registry_fingerprint(inputs.registry, inputs.spec, application)
            or inputs.dispatcher_fingerprint
            != _dispatcher_fingerprint(inputs.dispatcher, inputs.spec, application)
            or execution_reference_authority is not application.execution_reference_authority
        ):
            raise AuthorityConflictError("prepared execution factory binding mismatch")
        materialized_result = materializer_factory.require_issued_result(
            prepared=prepared,
            result=inputs.materialized_result,
        )
        current, attempt = self._current_reader.load(
            work_run_id=binding.run_id,
            execution_attempt_id=binding.attempt_id,
        )
        if (
            current.run_id != binding.run_id
            or current.state is not WorkflowState.RUNNING
            or current.state_version < 1
            or attempt.execution_attempt_id != binding.attempt_id
            or attempt.work_run_id != binding.run_id
        ):
            raise AuthorityConflictError("prepared execution factory binding mismatch")

        profile = application.composition.provider_profiles[
            prepared.request.provider_profile_id
        ].profile

        def context_factory(**values: object) -> StockroomSecurityContext:
            scope = cast(ResourceScope, values["scope"])
            snapshot = cast(WorkflowSnapshot, values["current"])
            return application.stockroom_owner_restriction.seal_context(
                context_id=_stable_id(
                    "stockroom-execution-context",
                    snapshot.run_id,
                    scope.domain.value,
                    str(values["operation_fingerprint"]),
                ),
                principal=cast(str, values["principal"]),
                task_action="fixed-stockroom-summary",
                mode=cast(RuntimeMode, values["mode"]),
                scenario_id=cast(str, values["scenario_id"]),
                profile_id=cast(str, values["provider_profile_id"]),
                run_id=snapshot.run_id,
                attempt_id=cast(str, values["execution_attempt_id"]),
                state=snapshot.state,
                state_version=snapshot.state_version,
                security_action=cast(SecurityActionClass, values["action"]),
                scope=scope,
                operation_fingerprint=cast(str, values["operation_fingerprint"]),
                process_spec_fingerprint=cast(str, values["resolved_spec_fingerprint"]),
                remaining_provider_calls=profile.provider_call_maximum,
                remaining_tool_calls=application.composition.security_config.tool_calls,
                remaining_process_calls=application.composition.security_config.process_calls,
                remaining_seconds=application.composition.security_config.attempt_timeout_seconds,
                remaining_budget_units=profile.budget_unit_maximum,
                repository_capability_ref="p1-3:repository-owner:v1",
                filesystem_capability_ref="p1-3:filesystem-owner:v1",
                process_capability_ref="p1-3:process-owner:v1",
                materialized_resource_owner_ref="stockroom-materialization-owner:v1",
                runtime_root_owner_ref="stockroom-runtime-root-owner:v1",
            )

        def dispatch_factory(**values: object):
            snapshot = cast(WorkflowSnapshot, values["current"])
            current_attempt = cast(ExecutionAttemptRef, values["attempt"])
            return build_dispatch_context(
                run_id=snapshot.run_id,
                attempt_id=current_attempt.execution_attempt_id,
                state_version=snapshot.state_version,
                scenario_id=cast(str, values["scenario_id"]),
                profile_id=profile.profile_id,
                provider_operation_id=cast(str, values["operation_id"]),
                provider_call_id=cast(str, values["provider_call_id"]),
                spec=inputs.spec,
            )

        owner = AgentExecutionService(
            policy=application.security_policy,
            adapter=application.local_provider,
            secret_resolver=application.secret_resolver,
            authority_reader=self._current_reader,
            secret_lease_authority=application.secret_lease_authority,
            repository=application.execution_repository,
            provider_tool_authority=application.provider_tool_authority,
            secret_use_authority=application.secret_use_authority,
            profile=profile,
            tool_registry=inputs.registry,
            tool_dispatcher=inputs.dispatcher,
            execution_ref_authority=execution_reference_authority,
            server_initial_inputs=_server_initial_inputs(prepared.request.scenario_id),
            stockroom_context_factory=context_factory,
            stockroom_dispatch_context_factory=dispatch_factory,
            security_profile_version=_SECURITY_PROFILE_VERSION,
            durable_time_source=application.clock,
        )
        materialized_result_fingerprint = materialized_result.provenance.provenance_fingerprint
        materialized_result_ref = (
            f"stockroom-materialized-result-{materialized_result_fingerprint[:40]}"
        )
        provenance_values = {
            "factory_ref": self.factory_ref,
            "factory_fingerprint": self.factory_fingerprint,
            "prepared_binding_fingerprint": binding.binding_fingerprint,
            "run_id": binding.run_id,
            "attempt_id": binding.attempt_id,
            "derived_owner_kind": "AgentExecutionService",
            "docker_spec_fingerprint": inputs.docker_spec_fingerprint,
            "tool_registry_fingerprint": inputs.tool_registry_fingerprint,
            "dispatcher_fingerprint": inputs.dispatcher_fingerprint,
            "materialized_result_provenance_ref": materialized_result_ref,
            "materialized_result_provenance_fingerprint": materialized_result_fingerprint,
            "materialized_output_fingerprint": (
                materialized_result.provenance.materialized_output_fingerprint
            ),
            "execution_reference_authority_ref": execution_reference_authority.issuer_ref,
        }
        provenance = StockroomAgentExecutionServiceDerivationProvenance(
            **provenance_values,
            provenance_fingerprint=canonical_sha256(provenance_values),
        )
        return StockroomAgentExecutionServiceDerivation(owner, provenance)


class StockroomCaptureOwnerAdapter:
    """A1 translation port that retains only refs issued by current semantic owners."""

    def __init__(
        self,
        application: StockroomProductionApplication,
        capture: StockroomPreparedCapture,
        current_binding: _CurrentBinding,
        current_reader: _CurrentAttemptReader,
    ) -> None:
        self._app = application
        self._capture = capture
        self._current_binding = current_binding
        self._current_reader = current_reader
        self._handles: dict[str, object] = {}
        self._pending_requests: dict[WorkflowState, TransitionRequest] = {}
        self._pending_participants: dict[
            WorkflowState, tuple[TransitionTransactionParticipant, ...]
        ] = {}
        self._pending_authority_refs: dict[WorkflowState, frozenset[str]] = {}

    def security_authorization(self, owner_ref: str) -> StockroomSecurityAuthorization:
        """Resolve an authorization issued by this attempt without exposing the handle map."""
        return self._require_handle(owner_ref, StockroomSecurityAuthorization)

    def _require_prepared(self, prepared: PreparedStockroomDriver) -> None:
        require_prepared_attempt_binding(prepared)
        owners = prepared.owners
        if (
            prepared is not self._capture.prepared
            or owners.workflow_kernel is not self._app.workflow_kernel
            or owners.evidence_admission_service is not self._app.evidence_service
            or owners.human_gate_owner is not self._app.human_repository
            or owners.judgment_owner is not self._app.judgment_authority
            or owners.workspace_owner is not self._app.workspace
            or owners.security_policy is not self._app.security_policy
            or owners.stockroom_owner_restriction is not self._app.stockroom_owner_restriction
            or type(owners.materializer_factory) is not StockroomMaterializerFactory
            or type(owners.agent_execution_service_factory)
            is not StockroomAgentExecutionServiceFactory
        ):
            raise AuthorityConflictError("prepared production owner identity mismatch")

    async def initial_ready(self, prepared: PreparedStockroomDriver) -> OwnerCallResult:
        request = self._request(prepared, None, 0, WorkflowState.READY)
        try:
            decision = await self._app.workflow_kernel.request_transition(
                request, self._system_facts(request)
            )
            self._handles[decision.transition_decision_id] = decision
            return await self._transition_result(decision, request)
        except (AuthorityConflictError, ValueError, RuntimeError) as exc:
            return await self._failure(prepared, "DENIED", type(exc).__name__)

    async def create_attempt(
        self, prepared: PreparedStockroomDriver, ready_ref: str
    ) -> OwnerCallResult:
        try:
            ready = self._handles.get(ready_ref)
            if (
                not isinstance(ready, TransitionDecision)
                or ready.resulting_state is not WorkflowState.READY
            ):
                raise AuthorityConflictError("READY transition ref is not current-owner issued")
            request = prepared.request
            row = await self._app.execution_repository.create_attempt(
                attempt_id=request.run_binding.attempt_id,
                work_run_id=request.run_binding.run_id,
                profile_id=request.provider_profile_id,
                profile_version=request.provider_profile_version,
                registry_id=self._app.composition.tool_config.registry_id,
                registry_version=self._app.composition.tool_config.registry_version,
            )
            ref = self._app.execution_reference_authority.register_start(
                ExecutionAttemptRef(
                    execution_attempt_id=row.execution_attempt_id,
                    work_run_id=row.work_run_id,
                    task_contract_id=row.task_contract_id,
                    task_contract_version=row.task_contract_version,
                    state=WorkflowState(row.causal_state),
                    state_version=row.causal_state_version,
                    execution_version=row.execution_version,
                    status=ExecutionStatus(row.status),
                    issuer_ref=self._app.execution_reference_authority.issuer_ref,
                    runtime_mode=RuntimeMode(row.runtime_mode),
                    project_id=self._app.project_id,
                    provider_profile_id=row.provider_profile_id,
                    provider_profile_version=row.provider_profile_version,
                    tool_registry_id=row.tool_registry_id,
                    tool_registry_version=row.tool_registry_version,
                )
            )
            self._handles[ref.execution_attempt_id] = ref
            self._current_reader.current = WorkflowSnapshot(
                row.work_run_id, WorkflowState(row.causal_state), row.causal_state_version
            )
            self._current_reader.attempt = ref
            return await self._snapshot_result(prepared, "ADMITTED", ref.execution_attempt_id)
        except (AuthorityConflictError, ValueError, RuntimeError) as exc:
            return await self._failure(prepared, "DENIED", type(exc).__name__)

    async def request_transition(
        self,
        prepared: PreparedStockroomDriver,
        *,
        target: WorkflowState,
        observed_state: WorkflowState,
        observed_version: int,
        authority_refs: tuple[str, ...],
    ) -> OwnerCallResult:
        try:
            pending = self._pending_requests.pop(target, None)
            if pending is not None:
                expected_refs = self._pending_authority_refs.pop(target, frozenset())
                if (
                    pending.observed_state is not observed_state
                    or pending.observed_state_version != observed_version
                    or frozenset(authority_refs) != expected_refs
                ):
                    raise AuthorityConflictError("pending owner transition binding mismatch")
                request = pending
            else:
                request = self._request(prepared, observed_state, observed_version, target)
            start_attempt: ExecutionAttemptRef | None = None
            if observed_state is WorkflowState.READY and target is WorkflowState.RUNNING:
                if len(authority_refs) != 1:
                    raise AuthorityConflictError("exact prepared execution attempt ref required")
                prepared_attempt = self._require_handle(authority_refs[0], ExecutionAttemptRef)
                if (
                    prepared_attempt.execution_attempt_id != prepared.request.run_binding.attempt_id
                    or prepared_attempt.work_run_id != prepared.request.run_binding.run_id
                    or prepared_attempt.status is not ExecutionStatus.NOT_STARTED
                    or prepared_attempt.state is not WorkflowState.READY
                    or prepared_attempt.state_version != observed_version
                ):
                    raise AuthorityConflictError("prepared execution start binding mismatch")
                if prepared.request.scenario_id != "stockroom-s3-policy-conflict":
                    start_attempt = prepared_attempt
            facts: list[TrustedGuardFact] = []
            participants = list(self._pending_participants.pop(target, ()))
            for guard in sorted(
                TRANSITION_MATRIX.get((observed_state, target), frozenset()), key=str
            ):
                owner = GUARD_OWNER_POLICY[guard]
                if owner is GuardSemanticOwner.P1_4_SYSTEM:
                    facts.append(self._p1_4_fact(request, guard, authority_refs))
                elif owner is GuardSemanticOwner.P1_6_EVIDENCE:
                    facts.append(
                        await self._app.evidence_guard_authority.issue_for_transition(request)
                    )
                elif owner is GuardSemanticOwner.P1_7_HUMAN and not any(
                    type(item).__module__.startswith("aiscc.human") for item in participants
                ):
                    participants.append(
                        await self._app.human_guard_authority.policy_guard_participant(
                            request, guard
                        )
                    )
            participant: TransitionTransactionParticipant | None = None
            if len(participants) == 1:
                participant = participants[0]
            elif participants:
                participant = _CompositeTransitionParticipant(participants)
            decision = await self._app.workflow_kernel.request_transition(
                request, tuple(facts), transaction_participant=participant
            )
            self._handles[decision.transition_decision_id] = decision
            return await self._transition_result(decision, request, start_attempt=start_attempt)
        except (AuthorityConflictError, ValueError, RuntimeError) as exc:
            return await self._failure(prepared, "DENIED", type(exc).__name__)

    async def seal_security_context(
        self, prepared: PreparedStockroomDriver, running_ref: str
    ) -> OwnerCallResult:
        try:
            running = self._handles.get(running_ref)
            if (
                not isinstance(running, TransitionDecision)
                or running.resulting_state is not WorkflowState.RUNNING
            ):
                raise AuthorityConflictError("RUNNING transition ref is not current-owner issued")
            current = await self._current(prepared, WorkflowState.RUNNING)
            request = prepared.request
            binding = StockroomRunBinding(
                request.runtime_mode,
                request.scenario_id,
                request.scenario_version,
                request.resource_ref,
                request.run_binding.run_id,
                request.run_binding.attempt_id,
                current.state,
                current.state_version,
                request.provider_profile_version,
                request.configuration_fingerprints.composition_sha256,
            )
            self._current_binding.value = binding
            fingerprint = materialization_operation_fingerprint(
                binding, self._app.repository_root, self._app.private_runtime_root
            )
            repository_scope = ResourceScope(ResourceDomain.REPOSITORY, RESOURCE_REF)
            filesystem_scope = ResourceScope(
                ResourceDomain.FILESYSTEM,
                f"workspace:{request.run_binding.run_id}:{request.run_binding.attempt_id}",
                workspace_path=str(self._app.private_runtime_root),
            )
            repository_context = self._seal_context(
                prepared, binding, repository_scope, fingerprint, "repository"
            )
            filesystem_context = self._seal_context(
                prepared, binding, filesystem_scope, fingerprint, "filesystem"
            )
            sealed = _SealedSecurity(
                binding,
                fingerprint,
                repository_scope,
                filesystem_scope,
                repository_context,
                filesystem_context,
            )
            ref = (
                "stockroom-security-context:"
                f"{_stable_digest(request.run_binding.run_id, fingerprint)}"
            )
            self._handles[ref] = sealed
            return await self._snapshot_result(prepared, "ADMITTED", ref)
        except (AuthorityConflictError, StockroomFailure, ValueError) as exc:
            return await self._failure(prepared, "DENIED", type(exc).__name__)

    async def authorize_runtime(
        self, prepared: PreparedStockroomDriver, security_context_ref: str
    ) -> OwnerCallResult:
        try:
            sealed = self._require_handle(security_context_ref, _SealedSecurity)
            current = await self._current(prepared, WorkflowState.RUNNING)
            repository = self._issue_capability(
                prepared,
                current,
                sealed.repository_scope,
                sealed.repository_context,
                sealed.operation_fingerprint,
            )
            filesystem = self._issue_capability(
                prepared,
                current,
                sealed.filesystem_scope,
                sealed.filesystem_context,
                sealed.operation_fingerprint,
            )
            network_scope = ResourceScope(
                ResourceDomain.NETWORK,
                "network:stockroom-denied",
                network_name="stockroom-denied",
            )
            network_grant = self._app.security_policy.issue_resource_grant(
                mode=prepared.request.runtime_mode,
                profile_version=_SECURITY_PROFILE_VERSION,
                scenario_id=prepared.request.scenario_id,
                principal=self._app.requester_identity,
                run_id=current.work_run_id,
                action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
                scope=network_scope,
                operation_fingerprint=sealed.operation_fingerprint,
                stockroom_context=None,
            )
            authorization = StockroomSecurityAuthorization(
                binding=sealed.binding,
                operation_fingerprint=sealed.operation_fingerprint,
                repository_scope=sealed.repository_scope,
                filesystem_scope=sealed.filesystem_scope,
                repository_context=sealed.repository_context,
                filesystem_context=sealed.filesystem_context,
                repository_grant=repository[0],
                filesystem_grant=filesystem[0],
                repository_decision=repository[1],
                filesystem_decision=filesystem[1],
                repository_capability=repository[2],
                filesystem_capability=filesystem[2],
                network_grant_issued=network_grant is not None,
            )
            ref = f"stockroom-security-authorization:{_stable_digest(security_context_ref)}"
            self._handles[ref] = authorization
            return await self._snapshot_result(prepared, "ADMITTED", ref)
        except (AuthorityConflictError, ValueError, RuntimeError) as exc:
            return await self._failure(prepared, "DENIED", type(exc).__name__)

    async def materialize(
        self, prepared: PreparedStockroomDriver, security_ref: str
    ) -> OwnerCallResult:
        try:
            self._require_prepared(prepared)
            authorization = self._require_handle(security_ref, StockroomSecurityAuthorization)
            materialization_authority = MaterializationAuthority(
                binding=authorization.binding,
                principal_ref=self._app.requester_identity,
                security_admission_ref=cast(str, authorization.repository_decision.admission_id),
                repository_grant_ref=authorization.repository_grant.grant_id,
                filesystem_grant_ref=authorization.filesystem_grant.grant_id,
                operation_fingerprint=authorization.operation_fingerprint,
                repository_root=self._app.repository_root,
                runtime_root=self._app.private_runtime_root,
            )
            materializer_factory = cast(
                StockroomMaterializerFactory, prepared.owners.materializer_factory
            )
            materialized_result = materializer_factory.materialize(
                prepared=prepared,
                authorization=authorization,
                authority=materialization_authority,
                repository_root=self._app.repository_root,
                private_runtime_root=self._app.private_runtime_root,
            )
            materialized = materialized_result.materialized
            materializer_derivation = materialized_result.materializer_derivation
            execution_factory = cast(
                StockroomAgentExecutionServiceFactory,
                prepared.owners.agent_execution_service_factory,
            )
            execution_inputs = execution_factory.prepare_inputs(
                prepared=prepared,
                materialized_result=materialized_result,
            )
            execution_derivation = execution_factory.derive(
                prepared=prepared,
                inputs=execution_inputs,
                execution_reference_authority=self._app.execution_reference_authority,
            )
            runtime = _MaterializedRuntime(
                materialized,
                materializer_derivation,
                materialized_result,
                execution_inputs,
                execution_derivation,
            )
            ref = f"stockroom-materialized:{materialized.workspace_lease.lease_id}"
            self._handles[ref] = runtime
            self._capture.materializer = materializer_derivation.owner
            self._capture.agent_execution_service = execution_derivation.owner
            self._capture.materializer_derivation = materializer_derivation
            self._capture.materialized_result = materialized_result
            self._capture.execution_service_derivation = execution_derivation
            return await self._snapshot_result(prepared, "ADMITTED", ref)
        except StockroomFailure as exc:
            return await self._failure(prepared, "FAILED", exc.reason)
        except (AuthorityConflictError, ValueError) as exc:
            return await self._failure(prepared, "DENIED", type(exc).__name__)

    async def execute(
        self, prepared: PreparedStockroomDriver, materialization_ref: str
    ) -> OwnerCallResult:
        try:
            self._require_prepared(prepared)
            runtime = self._require_handle(materialization_ref, _MaterializedRuntime)
            result = await runtime.execution_derivation.owner.execute(
                work_run_id=prepared.request.run_binding.run_id,
                execution_attempt_id=prepared.request.run_binding.attempt_id,
                principal=self._app.requester_identity,
                scenario_id=prepared.request.scenario_id,
            )
            if result.status != "EXECUTOR_COMPLETED" or result.submission is None:
                return await self._snapshot_result(
                    prepared, "UNKNOWN", f"execution:{result.status}", result.status
                )
            self._handles[result.submission.submission_id] = result
            return await self._snapshot_result(
                prepared, "COMPLETED", result.submission.submission_id
            )
        except (AuthorityConflictError, ValueError, RuntimeError) as exc:
            return await self._failure(prepared, "UNKNOWN", type(exc).__name__)

    async def submit_runtime_evidence(
        self, prepared: PreparedStockroomDriver, predecessor_ref: str
    ) -> OwnerCallResult:
        try:
            enrollment = self._enrollment(prepared)
            current = await self._current(prepared, WorkflowState.ADMISSION_PENDING)
            async with self._app.session_factory() as session, session.begin():
                await acquire_work_run_transaction_lock(session, current.work_run_id)
                predecessor = await session.get(TransitionDecisionRow, predecessor_ref)
                if predecessor is None:
                    raise AuthorityConflictError("exact admitted predecessor is missing")
                linked = await verify_historical_transition_provenance(
                    session, predecessor.transition_request_id
                )
                request, decision = linked.request, linked.decision
                if (
                    decision.transition_decision_id != predecessor_ref
                    or decision.outcome is not DecisionOutcome.ADMITTED
                    or request.observed_state is not WorkflowState.RUNNING
                    or request.target_state is not WorkflowState.ADMISSION_PENDING
                    or decision.resulting_state is not current.state
                    or decision.resulting_state_version != current.state_version
                    or request.observed_state_version + 1 != current.state_version
                    or request.work_run_id != prepared.request.run_binding.run_id
                    or request.work_run_id != current.work_run_id
                    or request.task_contract_id != enrollment.requirement.task_contract_id
                    or request.task_contract_version != enrollment.requirement.task_contract_version
                    or request.task_contract_id != current.task_contract_id
                    or request.task_contract_version != current.task_contract_version
                    or request.project_id != current.project_id
                    or request.runtime_mode is not current.runtime_mode
                    or linked.work_run != current
                ):
                    raise AuthorityConflictError(
                        "predecessor is not the exact current successor link"
                    )
                guards = tuple(
                    guard
                    for guard in linked.evaluation.guards
                    if guard.guard_id is GuardId.G_EXECUTOR_SUBMISSION
                )
                if len(guards) != 1 or not guards[0].satisfied:
                    raise AuthorityConflictError("exact predecessor execution guard is missing")
                submission_id, attempt_id = decode_execution_bound_refs(guards[0].bound_refs)
            execution = self._require_handle(submission_id, DurableExecutionResult)
            submission = execution.submission
            if (
                submission is None
                or submission.submission_id != submission_id
                or submission.execution_attempt_id != attempt_id
                or submission.execution_attempt_id != prepared.request.run_binding.attempt_id
                or submission.work_run_id != prepared.request.run_binding.run_id
                or submission.task_contract_id != enrollment.requirement.task_contract_id
                or submission.task_contract_version != enrollment.requirement.task_contract_version
                or submission.status is not ExecutionStatus.EXECUTOR_COMPLETED
                or not self._app.execution_reference_authority.verify(
                    submission,
                    request,
                    GuardId.G_EXECUTOR_SUBMISSION,
                )
            ):
                raise AuthorityConflictError("execution submission is absent or stale")
            observation = await self.verify_runtime_summary_source(prepared)
            if await self._current(prepared, WorkflowState.ADMISSION_PENDING) != current:
                raise AuthorityConflictError("current evidence-review authority changed")
            admitted_ref = await self._submit_durable_candidate(
                prepared,
                enrollment,
                self._app.runtime_evidence_issuer,
                value={
                    "scenario_id": prepared.request.scenario_id,
                    "execution_submission_ref": submission.submission_id,
                    "execution_submission_hash": submission.event_range_hash,
                    **observation,
                },
                producer_attestation_ref=cast(str, observation["tool_output_ref"]),
                execution_attempt_id=prepared.request.run_binding.attempt_id,
                operation_id=None,
            )
            return await self._snapshot_result(prepared, "ADMITTED", admitted_ref)
        except (AuthorityConflictError, ValueError) as exc:
            return await self._failure(prepared, "DENIED", type(exc).__name__)

    async def verify_runtime_summary_source(
        self, prepared: PreparedStockroomDriver
    ) -> dict[str, object]:
        """Verify current P1-5 output owners before deriving a runtime observation."""
        agent_output = await self._load_output(prepared, "AgentOutputRef")
        tool_output = await self._load_output(prepared, "ToolOutputRef")
        values = {
            "work_run_id": prepared.request.run_binding.run_id,
            "execution_attempt_id": prepared.request.run_binding.attempt_id,
        }
        agent_verified = await self._app.evidence_repository.verify(
            ref_id=agent_output.output_ref_id,
            expected_kind="AgentOutputRef",
            content_hash=agent_output.content_hash,
            **values,
        )
        tool_verified = await self._app.evidence_repository.verify(
            ref_id=tool_output.output_ref_id,
            expected_kind="ToolOutputRef",
            content_hash=tool_output.content_hash,
            **values,
        )
        return _derive_runtime_summary_observation(
            expected_attempt_id=prepared.request.run_binding.attempt_id,
            agent_output=agent_output,
            tool_output=tool_output,
            agent_verified=agent_verified,
            tool_verified=tool_verified,
        )

    async def submit_static_policy_evidence(
        self, prepared: PreparedStockroomDriver, running_ref: str
    ) -> OwnerCallResult:
        try:
            running = self._handles.get(running_ref)
            if not isinstance(running, TransitionDecision):
                raise AuthorityConflictError("RUNNING transition ref required")
            enrollment = self._enrollment(prepared)
            admitted_ref = await self._submit_durable_candidate(
                prepared,
                enrollment,
                self._app.static_evidence_issuer,
                value=dict(self._app.static_policy_fixture),
                producer_attestation_ref=(
                    f"server-fixture:{canonical_hash(self._app.static_policy_fixture)}"
                ),
                execution_attempt_id=None,
                operation_id=None,
            )
            return await self._snapshot_result(prepared, "ADMITTED", admitted_ref)
        except (AuthorityConflictError, ValueError) as exc:
            return await self._failure(prepared, "DENIED", type(exc).__name__)

    async def evaluate_evidence(
        self, prepared: PreparedStockroomDriver, candidate_ref: str | None
    ) -> OwnerCallResult:
        try:
            if candidate_ref is not None and candidate_ref not in self._handles:
                raise AuthorityConflictError("candidate admission ref is not retained")
            enrollment = self._enrollment(prepared)
            current = await self._current(prepared)
            evaluation, attestation = await self._app.evidence_set_evaluator.evaluate(
                work_run_id=current.work_run_id,
                checkpoint_ref=enrollment.checkpoint.ref,
                source_state=current.state,
                state_version=current.state_version,
                now=self._app.clock(),
            )
            if evaluation.outcome is EvidenceSetOutcome.SATISFIED and attestation is not None:
                self._handles[attestation.serialized_ref] = attestation
                return await self._snapshot_result(
                    prepared, "SATISFIED", attestation.serialized_ref
                )
            ref = evaluation.serialized_ref
            self._handles[ref] = evaluation
            return await self._snapshot_result(prepared, "UNSATISFIED", ref)
        except (AuthorityConflictError, ValueError) as exc:
            return await self._failure(prepared, "UNKNOWN", type(exc).__name__)

    async def submit_agent_human_claim(
        self, prepared: PreparedStockroomDriver, execution_ref: str
    ) -> OwnerCallResult:
        try:
            self._require_handle(execution_ref, DurableExecutionResult)
            enrollment = self._enrollment(prepared)
            current = await self._current(prepared, WorkflowState.ADMISSION_PENDING)
            output = await self._load_output(prepared, "AgentOutputRef")
            content_ref = EvidenceContentRef(
                EvidenceContentKind.P1_5_IMMUTABLE_PRODUCER_REF,
                "P1_5_EXECUTION",
                "v1",
                output.output_ref_id,
                "v1",
                "P1_5_OUTPUT_REF",
                "AISCC-STOCKROOM-AGENT-HUMAN-CLAIM-V1",
                "1",
                1,
                output.content_hash,
                EvidenceSensitivity.INTERNAL,
                "PRIVATE_EXECUTION_PROVENANCE",
                "PRIVATE_AUTHORITY_ONLY",
            )
            skeleton = EvidenceCandidate(
                _stable_id("stockroom-agent-claim", current.work_run_id),
                "v1",
                "",
                EvidenceOwner(
                    EvidenceIssuerType.P1_5_AGENT_OUTPUT,
                    _AGENT_ISSUER_ID,
                    "v1",
                    f"{_AGENT_ISSUER_ID}@v1",
                ),
                current.work_run_id,
                prepared.request.run_binding.attempt_id,
                None,
                enrollment.requirement.task_contract_id,
                enrollment.requirement.task_contract_version,
                enrollment.checkpoint.ref,
                current.state,
                current.state_version,
                enrollment.requirement.subject_id,
                enrollment.requirement.scope_id,
                enrollment.requirement.resource_id,
                "HUMAN_BROWSER_QA",
                "v1",
                content_ref,
                self._app.clock(),
                self._app.clock(),
                frozenset({"human-browser-qa"}),
                output.output_ref_id,
            )
            candidate = self._app.agent_evidence_issuer.seed_candidate(skeleton)
            admission = make_admission_request(
                admission_request_id=_stable_id(
                    "stockroom-agent-claim-admission", current.work_run_id
                ),
                candidate=candidate,
                requirement=enrollment.requirement,
                requirement_set=enrollment.requirement_set,
                checkpoint=enrollment.checkpoint,
                work_run_id=current.work_run_id,
                observed_state=current.state,
                observed_state_version=current.state_version,
                requester_identity=self._app.requester_identity,
                created_at=self._app.clock(),
            )
            decision, admitted = await self._app.evidence_service.submit(
                admission, candidate, now=self._app.clock()
            )
            if admitted is not None or decision.outcome is not EvidenceAdmissionOutcome.REJECTED:
                raise AuthorityConflictError("Agent Human claim was not rejected")
            self._handles[decision.decision_id] = decision
            return await self._snapshot_result(prepared, "REJECTED", decision.decision_id)
        except (AuthorityConflictError, ValueError) as exc:
            return await self._failure(prepared, "UNKNOWN", type(exc).__name__)

    async def open_human_gate(
        self, prepared: PreparedStockroomDriver, evidence_ref: str
    ) -> OwnerCallResult:
        try:
            if evidence_ref not in self._handles:
                raise AuthorityConflictError("pre-Human evidence ref is not retained")
            current = await self._current(prepared, WorkflowState.ADMISSION_PENDING)
            request = self._request(
                prepared,
                current.state,
                current.state_version,
                WorkflowState.HUMAN_REQUIRED,
            )
            reservation = self._app.human_reservation_authority.reserve(
                request,
                designated_principal_selector_fingerprint=(self._app.human_selector_fingerprint),
            )
            participant = await self._app.human_guard_authority.gate_open_participant(
                request, reservation, evidence_ref
            )
            self._pending_requests[WorkflowState.HUMAN_REQUIRED] = request
            self._pending_participants[WorkflowState.HUMAN_REQUIRED] = (participant,)
            self._pending_authority_refs[WorkflowState.HUMAN_REQUIRED] = frozenset(
                {reservation.serialized_ref}
            )
            self._handles[reservation.serialized_ref] = reservation
            return await self._snapshot_result(prepared, "PENDING", reservation.serialized_ref)
        except (AuthorityConflictError, ValueError, RuntimeError) as exc:
            return await self._failure(prepared, "DENIED", type(exc).__name__)

    async def issue_judgment(
        self,
        prepared: PreparedStockroomDriver,
        *,
        judgment_status: str,
        evidence_ref: str | None,
    ) -> OwnerCallResult:
        try:
            target = {
                "ACCEPTED": WorkflowState.ACCEPTED,
                "HOLD_REWORK_REQUIRED": WorkflowState.REWORK_REQUIRED,
            }[judgment_status]
            enrollment = self._app.judgment_enrollments.get(prepared.request.scenario_id)
            if enrollment is None or enrollment.policy.target_state is not target:
                raise AuthorityConflictError("Judgment policy is not enrolled")
            current = await self._current(prepared, WorkflowState.ADMISSION_PENDING)
            evaluation_ref: str | None = None
            reason_code = "STOCKROOM_EVIDENCE_SATISFIED"
            if target is WorkflowState.REWORK_REQUIRED:
                evaluations = tuple(
                    item
                    for item in self._handles.values()
                    if isinstance(item, EvidenceSetEvaluation)
                    and item.work_run_id == current.work_run_id
                    and item.state_version == current.state_version
                    and item.checkpoint_ref == self._enrollment(prepared).checkpoint.ref
                    and item.outcome is EvidenceSetOutcome.UNSATISFIED
                )
                if len(evaluations) != 1 or evidence_ref is not None:
                    raise AuthorityConflictError(
                        "S2 Judgment requires one authentic current UNSATISFIED evaluation"
                    )
                evaluation_ref = evaluations[0].serialized_ref
                reason_code = "STOCKROOM_REQUIRED_EVIDENCE_UNSATISFIED"
            request = self._request(
                prepared,
                current.state,
                current.state_version,
                target,
                evidence_refs=(
                    (evidence_ref,)
                    if evidence_ref is not None
                    else ((evaluation_ref,) if evaluation_ref is not None else ())
                ),
            )
            judgment = await self._app.judgment_authority.issue(
                judgment_id=_stable_id("stockroom-judgment", current.work_run_id, target.value),
                judgment_version="v2",
                request=request,
                policy=enrollment.policy,
                human_result_ref=None,
                evidence_attestation_ref=evidence_ref,
                reason_code=reason_code,
                reason_vocabulary_version="stockroom-judgment-v2",
                evidence_basis_kind=enrollment.policy.evidence_basis_kind,
                evidence_evaluation_ref=evaluation_ref,
            )
            transition_request = replace(request, judgment_refs=(judgment.serialized_ref,))
            judgment_participant = await self._app.judgment_authority.participant(
                transition_request, judgment.serialized_ref
            )
            human_participant = await self._app.human_guard_authority.policy_guard_participant(
                transition_request, GuardId.G_HUMAN_NOT_REQUIRED
            )
            self._pending_requests[target] = transition_request
            self._pending_participants[target] = (
                human_participant,
                judgment_participant,
            )
            self._pending_authority_refs[target] = frozenset({judgment.serialized_ref})
            self._handles[judgment.serialized_ref] = judgment
            return await self._snapshot_result(prepared, "ADMITTED", judgment.serialized_ref)
        except (AuthorityConflictError, KeyError, ValueError, RuntimeError) as exc:
            return await self._failure(prepared, "DENIED", type(exc).__name__)

    async def create_policy_blocker(
        self, prepared: PreparedStockroomDriver, evidence_ref: str
    ) -> OwnerCallResult:
        try:
            attestation = self._handles.get(evidence_ref)
            source_fingerprint = getattr(attestation, "admitted_ref_root_hash", None)
            if not _is_sha256(source_fingerprint):
                raise AuthorityConflictError("blocker evidence attestation is unavailable")
            current = await self._current(prepared, WorkflowState.RUNNING)
            claim = P1_4BlockerClaimV1(
                _stable_id("stockroom-policy-blocker", current.work_run_id),
                BlockerKindV1.POLICY,
                BlockerReasonCodeV1.POLICY_CONFLICT,
                "stockroom-policy-conflict-resolution@v1",
                canonical_hash({"resolution": "HUMAN_COMMAND_CENTER_POLICY_RESOLUTION"}),
                (evidence_ref,),
                (cast(str, source_fingerprint),),
            )
            request = self._request(
                prepared,
                current.state,
                current.state_version,
                WorkflowState.BLOCKED,
                blocker_claim=claim,
            )
            self._pending_requests[WorkflowState.BLOCKED] = request
            self._pending_authority_refs[WorkflowState.BLOCKED] = frozenset({claim.blocker_ref})
            self._handles[claim.blocker_ref] = claim
            return await self._snapshot_result(prepared, "ADMITTED", claim.blocker_ref)
        except (AuthorityConflictError, ValueError) as exc:
            return await self._failure(prepared, "DENIED", type(exc).__name__)

    def _request(
        self,
        prepared: PreparedStockroomDriver,
        source: WorkflowState | None,
        version: int,
        target: WorkflowState,
        *,
        evidence_refs: tuple[str, ...] = (),
        judgment_refs: tuple[str, ...] = (),
        blocker_claim: P1_4BlockerClaimV1 | None = None,
    ) -> TransitionRequest:
        enrollment = self._enrollment(prepared)
        return TransitionRequest(
            _stable_id(
                "stockroom-transition",
                prepared.request.run_binding.run_id,
                str(version),
                target.value,
            ),
            self._app.project_id,
            enrollment.requirement.task_contract_id,
            enrollment.requirement.task_contract_version,
            prepared.request.run_binding.run_id,
            source,
            version,
            target,
            self._app.requester_identity,
            RequesterType.OPERATOR,
            prepared.request.runtime_mode,
            evidence_refs=evidence_refs,
            judgment_refs=judgment_refs,
            blocker_claim=blocker_claim,
            created_at=self._app.clock(),
        )

    def _system_facts(self, request: TransitionRequest) -> tuple[TrustedGuardFact, ...]:
        return tuple(
            self._p1_4_fact(request, guard, ())
            for guard in sorted(
                TRANSITION_MATRIX.get((request.observed_state, request.target_state), frozenset()),
                key=str,
            )
            if GUARD_OWNER_POLICY[guard] is GuardSemanticOwner.P1_4_SYSTEM
        )

    def _p1_4_fact(
        self,
        request: TransitionRequest,
        guard: GuardId,
        authority_refs: tuple[str, ...],
    ) -> TrustedGuardFact:
        if guard is GuardId.G_EXECUTION_STARTED:
            if len(authority_refs) != 1:
                raise AuthorityConflictError("exact execution attempt ref required")
            ref = self._require_handle(authority_refs[0], ExecutionAttemptRef)
            return self._app.p1_4_guard_authority.issue_from_execution_ref(
                guard_id=guard,
                execution_ref=ref,
                verifier=self._app.execution_reference_authority,
                request=request,
            )
        if guard is GuardId.G_EXECUTOR_SUBMISSION:
            if len(authority_refs) != 1:
                raise AuthorityConflictError("exact execution submission ref required")
            result = self._require_handle(authority_refs[0], DurableExecutionResult)
            if result.submission is None:
                raise AuthorityConflictError("execution submission ref is absent")
            return self._app.p1_4_guard_authority.issue_from_execution_ref(
                guard_id=guard,
                execution_ref=result.submission,
                verifier=self._app.execution_reference_authority,
                request=request,
            )
        authority_ref = {
            GuardId.G_CONTRACT: "stockroom-task-contract-config:v1",
            GuardId.G_SCOPE: "stockroom-production-scope:v1",
            GuardId.G_RUNTIME_CONTEXT: "stockroom-owner-runtime-context:v1",
            GuardId.G_REWORK_SPEC: "stockroom-missing-evidence-rework:v1",
            GuardId.G_BLOCKER: (
                request.blocker_claim.blocker_ref if request.blocker_claim else "NONE"
            ),
        }.get(guard)
        if authority_ref is None:
            raise AuthorityConflictError(f"unsupported P1-4 Stockroom guard: {guard.value}")
        return self._app.p1_4_guard_authority.issue(
            guard_id=guard,
            satisfied=True,
            reason=f"STOCKROOM_{guard.value}_OWNER_VERIFIED",
            authority_ref=authority_ref,
            request=request,
        )

    def _seal_context(
        self,
        prepared: PreparedStockroomDriver,
        binding: StockroomRunBinding,
        scope: ResourceScope,
        fingerprint: str,
        label: str,
    ) -> StockroomSecurityContext:
        config = self._app.composition.security_config
        scenario = config.scenarios[prepared.request.scenario_id]
        return self._app.stockroom_owner_restriction.seal_context(
            context_id=_stable_id("stockroom-security-context", binding.run_id, label),
            principal=self._app.requester_identity,
            task_action=(
                "compare-fixed-synthetic-policies"
                if prepared.request.scenario_id == "stockroom-s3-policy-conflict"
                else "fixed-stockroom-summary"
            ),
            mode=binding.mode,
            scenario_id=binding.scenario_id,
            profile_id=prepared.request.provider_profile_id,
            run_id=binding.run_id,
            attempt_id=binding.attempt_id,
            state=binding.state,
            state_version=binding.state_version,
            security_action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            scope=scope,
            operation_fingerprint=fingerprint,
            process_spec_fingerprint=canonical_hash(
                {
                    "image": self._app.composition.tool_config.image,
                    "argv": list(self._app.composition.tool_config.argv),
                    "network": self._app.composition.tool_config.network,
                }
            ),
            remaining_provider_calls=scenario.provider_call_limit,
            remaining_tool_calls=config.tool_calls,
            remaining_process_calls=config.process_calls,
            remaining_seconds=config.attempt_timeout_seconds,
            remaining_budget_units=config.budget_units,
            repository_capability_ref="p1-3:repository-owner:v1",
            filesystem_capability_ref="p1-3:filesystem-owner:v1",
            process_capability_ref="p1-3:process-owner:v1",
            materialized_resource_owner_ref="stockroom-materialization-owner:v1",
            runtime_root_owner_ref="stockroom-runtime-root-owner:v1",
            network_requested=False,
        )

    def _issue_capability(
        self,
        prepared: PreparedStockroomDriver,
        current: WorkRun,
        scope: ResourceScope,
        context: StockroomSecurityContext,
        fingerprint: str,
    ) -> tuple[ResourceGrant, SecurityDecision, Capability]:
        snapshot = WorkflowSnapshot(current.work_run_id, current.state, current.state_version)
        grant = self._app.security_policy.issue_resource_grant(
            mode=prepared.request.runtime_mode,
            profile_version=_SECURITY_PROFILE_VERSION,
            scenario_id=prepared.request.scenario_id,
            principal=self._app.requester_identity,
            run_id=current.work_run_id,
            action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            scope=scope,
            operation_fingerprint=fingerprint,
            stockroom_context=context,
        )
        request = PermissionRequest(
            principal=self._app.requester_identity,
            run_id=current.work_run_id,
            mode=prepared.request.runtime_mode,
            observed=snapshot,
            authoritative=snapshot,
            action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            resource_scope=scope,
            resource_grant=grant,
            profile_version=_SECURITY_PROFILE_VERSION,
            scenario_id=prepared.request.scenario_id,
            requester_authority=AuthorityStatus.GRANTED,
            task_scope_authority=AuthorityStatus.GRANTED,
            limit_authority=AuthorityStatus.GRANTED,
            budget_authority=AuthorityStatus.GRANTED,
            idempotency_authority=AuthorityStatus.GRANTED,
            target_control_authority=AuthorityStatus.NOT_APPLICABLE,
        )
        decision = self._app.security_policy.evaluate(request)
        capability = self._app.security_policy.issue_capability(decision, request)
        if (
            grant is None
            or decision.decision is not SecurityAdmissionDecision.ALLOW
            or capability is None
        ):
            raise AuthorityConflictError(f"security authorization denied: {scope.domain.value}")
        return grant, decision, capability

    async def _submit_durable_candidate(
        self,
        prepared: PreparedStockroomDriver,
        enrollment: StockroomEvidenceEnrollment,
        issuer: TokenEvidenceIssuer,
        *,
        value: object,
        producer_attestation_ref: str,
        execution_attempt_id: str | None,
        operation_id: str | None,
    ) -> str:
        current = await self._current(prepared)
        placeholder = EvidenceContentRef(
            next(iter(enrollment.requirement.allowed_content_kinds)),
            issuer.issuer_id,
            issuer.issuer_version,
            _stable_id("stockroom-evidence-object", current.work_run_id, enrollment.scenario_id),
            "v1",
            "PENDING_P1_6_CANONICALIZATION",
            enrollment.requirement.schema_id,
            enrollment.requirement.schema_version,
            1,
            "0" * 64,
            enrollment.requirement.maximum_sensitivity,
            "PENDING_P1_6_RETENTION",
            "PRIVATE_AUTHORITY_ONLY",
        )
        observed_at = self._app.clock()
        skeleton = EvidenceCandidate(
            _stable_id("stockroom-evidence-candidate", current.work_run_id, enrollment.scenario_id),
            "v1",
            "",
            EvidenceOwner(
                issuer.issuer_type,
                issuer.issuer_id,
                issuer.issuer_version,
                f"{issuer.issuer_id}@{issuer.issuer_version}",
            ),
            current.work_run_id,
            execution_attempt_id,
            operation_id,
            enrollment.requirement.task_contract_id,
            enrollment.requirement.task_contract_version,
            enrollment.checkpoint.ref,
            current.state,
            current.state_version,
            enrollment.requirement.subject_id,
            enrollment.requirement.scope_id,
            enrollment.requirement.resource_id,
            enrollment.requirement.evidence_type_id,
            enrollment.requirement.evidence_type_version,
            placeholder,
            observed_at,
            observed_at,
            enrollment.requirement.required_coverage,
            producer_attestation_ref,
            config_version="stockroom-capture.v1",
        )
        prepared_content = self._app.durable_content_authority.prepare_structured(
            owner_id=issuer.issuer_id,
            owner_version=issuer.issuer_version,
            source_owner_authority_ref=skeleton.issuer.authority_ref,
            source_owner_authority_fingerprint=source_owner_authority_fingerprint(skeleton),
            object_id=placeholder.object_id,
            object_version=placeholder.object_version,
            value=value,
            kind=placeholder.content_kind,
            schema_id=placeholder.schema_id,
            schema_version=placeholder.schema_version,
            sensitivity=placeholder.sensitivity,
            created_at=observed_at,
        )
        candidate = issuer.issue(replace(skeleton, content_ref=prepared_content.content_ref))
        admission = make_admission_request(
            admission_request_id=_stable_id(
                "stockroom-evidence-admission", current.work_run_id, enrollment.scenario_id
            ),
            candidate=candidate,
            requirement=enrollment.requirement,
            requirement_set=enrollment.requirement_set,
            checkpoint=enrollment.checkpoint,
            work_run_id=current.work_run_id,
            observed_state=current.state,
            observed_state_version=current.state_version,
            requester_identity=self._app.requester_identity,
            created_at=self._app.clock(),
        )
        decision, admitted = await self._app.evidence_service.submit_durable(
            admission, candidate, prepared_content, now=observed_at
        )
        if decision.outcome is not EvidenceAdmissionOutcome.ADMITTED or admitted is None:
            raise AuthorityConflictError(f"P1-6 evidence admission denied: {decision.reason.value}")
        ref = AdmittedEvidenceRef(
            admitted.admitted_evidence_id, EVIDENCE_AUTHORITY_VERSION
        ).serialized()
        self._handles[ref] = admitted
        return ref

    async def _load_output(
        self, prepared: PreparedStockroomDriver, kind: str
    ) -> ExecutionOutputRefRow:
        async with self._app.session_factory() as session:
            rows = tuple(
                (
                    await session.scalars(
                        select(ExecutionOutputRefRow).where(
                            ExecutionOutputRefRow.execution_attempt_id
                            == prepared.request.run_binding.attempt_id,
                            ExecutionOutputRefRow.ref_kind == kind,
                        )
                    )
                ).all()
            )
        if len(rows) != 1:
            raise AuthorityConflictError(f"exactly one current {kind} ref is required")
        return rows[0]

    async def _current(
        self,
        prepared: PreparedStockroomDriver,
        expected: WorkflowState | None = None,
    ) -> WorkRun:
        current = await self._app.workflow_kernel.load(prepared.request.run_binding.run_id)
        if current is None or (expected is not None and current.state is not expected):
            raise AuthorityConflictError("authoritative WorkflowKernel snapshot mismatch")
        return current

    async def _snapshot_result(
        self,
        prepared: PreparedStockroomDriver,
        status: str,
        owner_ref: str,
        reason: str | None = None,
    ) -> OwnerCallResult:
        current = await self._current(prepared)
        return OwnerCallResult(status, owner_ref, current.state, current.state_version, reason)

    async def _transition_result(
        self,
        decision: TransitionDecision,
        request: TransitionRequest,
        *,
        start_attempt: ExecutionAttemptRef | None = None,
    ) -> OwnerCallResult:
        state = decision.resulting_state or WorkflowState.READY
        if decision.outcome is not DecisionOutcome.ADMITTED:
            return OwnerCallResult(
                "DENIED",
                decision.transition_decision_id,
                state,
                decision.resulting_state_version,
                decision.reason.value,
            )
        current = await self._app.workflow_kernel.load(request.work_run_id)
        if current is None:
            raise AuthorityConflictError("admitted transition projection is missing")
        if current.state is not state or current.state_version != decision.resulting_state_version:
            raise AuthorityConflictError("transition decision/kernel snapshot mismatch")
        if start_attempt is not None:
            if (
                current.work_run_id != start_attempt.work_run_id
                or current.state is not WorkflowState.RUNNING
                or current.state_version != start_attempt.state_version + 1
                or decision.transition_request_id != request.transition_request_id
            ):
                raise AuthorityConflictError("execution start requires exact admitted RUNNING")
            await self._app.execution_repository.transition_attempt(
                start_attempt.execution_attempt_id, "EXECUTION_STARTED"
            )
            snapshot, attempt = await self._app.execution_repository.load_authority(
                work_run_id=start_attempt.work_run_id,
                execution_attempt_id=start_attempt.execution_attempt_id,
            )
            if (
                snapshot.run_id != start_attempt.work_run_id
                or snapshot.state is not WorkflowState.RUNNING
                or snapshot.state_version != decision.resulting_state_version
                or attempt.execution_attempt_id != start_attempt.execution_attempt_id
                or attempt.work_run_id != snapshot.run_id
                or attempt.status is not ExecutionStatus.RUNNING
                or attempt.state is not snapshot.state
                or attempt.state_version != snapshot.state_version
            ):
                raise AuthorityConflictError("post-start execution authority mismatch")
            self._current_reader.attempt = attempt
        self._current_reader.current = WorkflowSnapshot(
            current.work_run_id, current.state, current.state_version
        )
        return OwnerCallResult(
            "ADMITTED", decision.transition_decision_id, state, decision.resulting_state_version
        )

    async def _failure(
        self, prepared: PreparedStockroomDriver, status: str, reason: str
    ) -> OwnerCallResult:
        current = await self._app.workflow_kernel.load(prepared.request.run_binding.run_id)
        return OwnerCallResult(
            status,
            f"stockroom-owner-failure:{_stable_digest(status, reason)}",
            current.state if current is not None else WorkflowState.READY,
            current.state_version if current is not None else 1,
            reason,
        )

    def _enrollment(self, prepared: PreparedStockroomDriver) -> StockroomEvidenceEnrollment:
        enrollment = self._app.evidence_enrollments.get(prepared.request.scenario_id)
        if enrollment is None:
            raise AuthorityConflictError("Stockroom evidence enrollment is missing")
        return enrollment

    def _require_handle(self, ref: str, kind: type[Any]):
        value = self._handles.get(ref)
        if not isinstance(value, kind):
            raise AuthorityConflictError(f"authentic {kind.__name__} handle required")
        return value


async def build_stockroom_production_application(
    *,
    session_factory: async_sessionmaker[AsyncSession],
    repository_root: Path,
    private_runtime_root: Path,
    downloads_root: Path,
    trusted_git_executable: Path,
    image_provenance_ref: StockroomImageProvenanceRef,
    trusted_docker_executable: Path,
    cancellation: StockroomCancellation,
    project_id: str,
    requester_identity: str,
    human_selector_fingerprint: str,
    secret_material_by_ref: Mapping[str, str],
    clock: Callable[[], datetime] | None = None,
) -> StockroomProductionApplication:
    if not project_id or not requester_identity or not _is_sha256(human_selector_fingerprint):
        raise ValueError("explicit project/requester/Human selector identity is required")
    if dict(secret_material_by_ref) != {
        LOCAL_COMPATIBILITY_SECRET_REF: LOCAL_COMPATIBILITY_SENTINEL
    }:
        raise ValueError("exact local non-secret compatibility material is required")
    now = clock or (lambda: datetime.now(UTC))
    root = repository_root.resolve(strict=True)
    fixed_root = Path(__file__).resolve().parents[3]
    if root != fixed_root:
        raise ValueError("PRODUCTION_REPOSITORY_ROOT_DENIED")
    tool = load_stockroom_tool_config(fixed_root / "config/providers/stockroom-tools.v2.toml")
    image = resolve_stockroom_image(image_provenance_ref, dict(tool.image_binding_policy))
    runner = StockroomDockerRunner(trusted_docker_executable, image, cancellation)
    composition = build_stockroom_production_composition(image)
    evidence_raw = load_stockroom_evidence_config(root / _EVIDENCE_CONFIG)
    human_raw = load_stockroom_human_config(root / _HUMAN_CONFIG)
    judgment_raw = load_stockroom_judgment_config(root / _JUDGMENT_CONFIG)

    durable_content_authority = P1_6DurableContentAuthority()
    evidence_repository = PostgresEvidenceRepository(
        session_factory, durable_content_authority=durable_content_authority
    )
    task_evidence_authority = TaskContractEvidenceAuthority(
        evidence_raw["authority_id"], evidence_raw["authority_version"]
    )
    runtime_issuer = TokenEvidenceIssuer(
        EvidenceIssuerType.SYSTEM_RUNTIME_OBSERVATION, _RUNTIME_ISSUER_ID, "v1"
    )
    static_issuer = TokenEvidenceIssuer(
        EvidenceIssuerType.SYSTEM_STATIC_PROOF, _STATIC_ISSUER_ID, "v1"
    )
    agent_issuer = P1_5EvidenceIssuerAuthority(
        EvidenceIssuerType.P1_5_AGENT_OUTPUT, _AGENT_ISSUER_ID, "v1", evidence_repository
    )
    evidence_enrollments: dict[str, StockroomEvidenceEnrollment] = {}
    checkpoints: list[EvidenceCheckpoint] = []
    for item in evidence_raw["enrollments"]:
        enrollment = _build_evidence_enrollment(
            item,
            task_evidence_authority,
            evidence_raw["durable_policy_fingerprint"],
            runtime_issuer,
            static_issuer,
        )
        await evidence_repository.register_authority(
            requirement_set=enrollment.requirement_set,
            requirements=(enrollment.requirement,),
            checkpoints=(enrollment.checkpoint,),
            authority=task_evidence_authority,
        )
        evidence_enrollments[enrollment.scenario_id] = enrollment
        checkpoints.append(enrollment.checkpoint)
    checkpoint_uses = EvidenceCheckpointUseRegistry(tuple(checkpoints))
    evaluator = EvidenceAdmissionEvaluator(
        EvidenceIssuerRegistry((runtime_issuer, static_issuer, agent_issuer)),
        EvidenceContentRegistry(()),
    )
    evidence_service = EvidenceAdmissionService(
        evidence_repository,
        evaluator,
        durable_content_authority=durable_content_authority,
    )
    set_evaluator = EvidenceSetEvaluator(evidence_repository)
    evidence_guard = EvidenceGuardAuthority(evidence_repository, checkpoint_uses)

    human_repository = PostgresHumanAuthorityRepository(session_factory, clock=now)
    human_enrollment = StockroomHumanEnrollment(**human_raw["required_use"])
    human_reservation = HumanGateReservationAuthority(
        frozenset(
            {
                (
                    human_enrollment.task_contract_id,
                    human_enrollment.task_contract_version,
                    human_enrollment.source_state,
                    human_enrollment.target_state,
                )
            }
        ),
        authority_policy_ref=human_raw["authority_policy_ref"],
        authority_policy_version=human_raw["authority_policy_version"],
    )
    human_guard = HumanGuardAuthority(
        session_factory,
        human_repository,
        evidence_repository,
        checkpoint_uses,
        human_reservation,
        clock=now,
    )

    def policy_clock() -> datetime:
        return cast(datetime, judgment_raw["issued_at"])

    judgment_policy_authority = JudgmentPolicyAuthority(
        session_factory,
        clock=policy_clock,
        authority_version=cast(str, judgment_raw["authority_version"]),
    )
    command_center = CommandCenterAuthority(session_factory, judgment_policy_authority, clock=now)
    judgment_authority = PostgresJudgmentAuthority(
        session_factory,
        evidence_repository,
        judgment_policy_authority,
        command_center_authority=command_center,
        clock=now,
    )
    judgment_enrollments: dict[str, StockroomJudgmentEnrollment] = {}
    for item in judgment_raw["policies"]:
        evidence_enrollment = evidence_enrollments.get(item["scenario_id"])
        if evidence_enrollment is None or (
            item["evidence_checkpoint_ref"]
            != evidence_enrollment.checkpoint.ref.serialized()
            or item["evidence_requirement_set_ref"]
            != (
                f"{evidence_enrollment.requirement_set.requirement_set_id}"
                f"@{evidence_enrollment.requirement_set.requirement_set_version}"
            )
        ):
            raise ValueError("STOCKROOM_JUDGMENT_EVIDENCE_ENROLLMENT_MISMATCH")
        policy = await judgment_policy_authority.register(
            policy_id=item["policy_id"],
            policy_version=item["policy_version"],
            task_contract_id=item["task_contract_id"],
            task_contract_version=item["task_contract_version"],
            source_state=item["source_state"],
            target_state=item["target_state"],
            owner_policy=item["owner_policy"],
            requires_human_result=item["requires_human_result"],
            requires_post_human_evidence=item["requires_post_human_evidence"],
            deterministic_kind=item["deterministic_kind"],
            evidence_basis_kind=item["evidence_basis_kind"],
            evidence_checkpoint_ref=item["evidence_checkpoint_ref"],
            evidence_requirement_set_ref=item["evidence_requirement_set_ref"],
        )
        judgment_enrollments[item["scenario_id"]] = StockroomJudgmentEnrollment(
            item["scenario_id"], item["scenario_version"], policy
        )

    p1_4 = P1_4GuardAuthority()
    transition_repository = PostgresTransitionRepository(
        session_factory,
        TransitionEvaluator(p1_4, (evidence_guard, human_guard, judgment_authority)),
    )
    workflow_kernel = WorkflowKernel(transition_repository)
    execution_repository = PostgresExecutionRepository(session_factory)

    profiles = tuple(item.profile for item in composition.provider_profiles.values())
    tool_identity = ":".join(
        (
            composition.tool_config.registry_id,
            composition.tool_config.registry_version,
            composition.tool_config.tool_id,
            composition.tool_config.schema_version,
            composition.tool_config.dispatcher_version,
        )
    )
    provider_tool_authority = ProviderToolResourceAuthority(
        allowed_resource_identities=frozenset(
            {item.provider_resource_identity for item in profiles} | {tool_identity}
        ),
        allowed_profile_ids=frozenset(item.profile_id for item in profiles),
        allowed_scenarios=frozenset(SCENARIO_IDS),
        allowed_modes=frozenset({RuntimeMode.OWNER_SELF_DOGFOOD}),
        clock=now,
    )
    secret_use_authority = SecretUseAuthority(
        allowed_secret_refs=frozenset({LOCAL_COMPATIBILITY_SECRET_REF}),
        allowed_profile_ids=frozenset(item.profile_id for item in profiles),
        allowed_scenarios=frozenset(SCENARIO_IDS),
        allowed_destinations=frozenset({"local-in-process-stockroom-v1"}),
        allowed_modes=frozenset({RuntimeMode.OWNER_SELF_DOGFOOD}),
        clock=now,
    )
    restriction = StockroomOwnerRestriction(composition.security_config)
    from aiscc.bootstrap import build_security_policy

    security_policy = build_security_policy(
        provider_tool_policy=provider_tool_authority,
        secret_use_policy=secret_use_authority,
        stockroom_policy=restriction,
    )
    secret_lease = SecretResolutionLeaseAuthority(
        security_policy.verify_consumption_receipt, clock=now
    )
    secret_resolver = LeaseBoundSecretResolver(secret_lease, dict(secret_material_by_ref))
    execution_refs = ExecutionReferenceAuthority()
    local_provider = LocalDeterministicProvider(composition.provider_profiles)
    workspace = StockroomWorkspace(
        private_runtime_root,
        repository_root=root,
        source_object_root=root / ".git",
        downloads_root=downloads_root,
    )
    docker = DockerRuntime(
        security_policy,
        executable=str(trusted_docker_executable),
        stockroom_runner=runner,
    )
    fixture = PolicyConflictFixture.model_validate_json(
        (root / _POLICY_CONFLICT_FIXTURE).read_text(encoding="utf-8")
    ).model_dump(mode="json")
    return StockroomProductionApplication(
        session_factory,
        root,
        private_runtime_root,
        downloads_root,
        trusted_git_executable,
        project_id,
        requester_identity,
        human_selector_fingerprint,
        composition,
        execution_repository,
        evidence_repository,
        evidence_service,
        set_evaluator,
        checkpoint_uses,
        evidence_guard,
        MappingProxyType(evidence_enrollments),
        runtime_issuer,
        static_issuer,
        agent_issuer,
        durable_content_authority,
        human_repository,
        human_reservation,
        human_guard,
        human_enrollment,
        judgment_policy_authority,
        command_center,
        judgment_authority,
        MappingProxyType(judgment_enrollments),
        p1_4,
        transition_repository,
        workflow_kernel,
        provider_tool_authority,
        secret_use_authority,
        secret_lease,
        secret_resolver,
        execution_refs,
        restriction,
        security_policy,
        local_provider,
        workspace,
        docker,
        MappingProxyType(fixture),
        now,
        cancellation,
    )


def load_stockroom_evidence_config(path: Path) -> dict[str, Any]:
    root = _strict_json(path)
    _exact_keys(
        root,
        {"schema_id", "schema_version", "authority", "durable_content_policy", "enrollments"},
        "evidence root",
    )
    if root["schema_id"] != "AISCC-STOCKROOM-CAPTURE-EVIDENCE-V1" or root["schema_version"] != "1":
        raise ValueError("STOCKROOM_EVIDENCE_SCHEMA_DENIED")
    authority = _table(root, "authority")
    _exact_keys(authority, {"authority_id", "authority_version"}, "evidence authority")
    policy = _table(root, "durable_content_policy")
    _exact_keys(
        policy,
        {"ref", "allowed_content_kinds", "max_bytes", "fingerprint"},
        "durable content policy",
    )
    policy_payload = {
        "ref": _text(policy, "ref"),
        "allowed_content_kinds": _string_list(policy, "allowed_content_kinds"),
        "max_bytes": _positive_int(policy, "max_bytes"),
    }
    if policy["fingerprint"] != canonical_hash(policy_payload):
        raise ValueError("STOCKROOM_DURABLE_CONTENT_POLICY_FINGERPRINT_MISMATCH")
    expected_keys = {
        "scenario_id",
        "scenario_version",
        "task_contract_id",
        "task_contract_version",
        "requirement_set_id",
        "requirement_set_version",
        "requirement_id",
        "requirement_version",
        "evidence_type_id",
        "evidence_type_version",
        "issuer_type",
        "issuer_id",
        "issuer_version",
        "content_kind",
        "content_schema_id",
        "content_schema_version",
        "subject_id",
        "scope_id",
        "resource_id",
        "required_coverage",
        "maximum_sensitivity",
        "public_export_allowed",
        "checkpoint_id",
        "checkpoint_version",
        "source_state",
        "target_state",
        "issued_at",
    }
    raw_enrollments = root.get("enrollments")
    if type(raw_enrollments) is not list:
        raise ValueError("evidence enrollments must be an array")
    enrollments: list[dict[str, Any]] = []
    for raw in raw_enrollments:
        if type(raw) is not dict:
            raise ValueError("evidence enrollment must be an object")
        _exact_keys(raw, expected_keys, "evidence enrollment")
        item = dict(raw)
        item["issuer_type"] = EvidenceIssuerType(_text(raw, "issuer_type"))
        item["content_kind"] = EvidenceContentKind(_text(raw, "content_kind"))
        item["maximum_sensitivity"] = EvidenceSensitivity(_text(raw, "maximum_sensitivity"))
        item["source_state"] = WorkflowState(_text(raw, "source_state"))
        item["target_state"] = WorkflowState(_text(raw, "target_state"))
        item["issued_at"] = _aware_datetime(raw, "issued_at")
        item["required_coverage"] = frozenset(_string_list(raw, "required_coverage"))
        if type(raw["public_export_allowed"]) is not bool:
            raise ValueError("public_export_allowed must be boolean")
        enrollments.append(item)
    if tuple(item["scenario_id"] for item in enrollments) != SCENARIO_IDS:
        raise ValueError("EXACT_STOCKROOM_EVIDENCE_ENROLLMENT_REQUIRED")
    return {
        "authority_id": _text(authority, "authority_id"),
        "authority_version": _text(authority, "authority_version"),
        "durable_policy_fingerprint": cast(str, policy["fingerprint"]),
        "enrollments": tuple(enrollments),
    }


def load_stockroom_human_config(path: Path) -> dict[str, Any]:
    root = _strict_json(path)
    _exact_keys(root, {"schema_id", "schema_version", "policy", "required_uses"}, "human root")
    if root["schema_id"] != "AISCC-STOCKROOM-CAPTURE-HUMAN-V1" or root["schema_version"] != "1":
        raise ValueError("STOCKROOM_HUMAN_SCHEMA_DENIED")
    policy = _table(root, "policy")
    _exact_keys(
        policy,
        {
            "authority_policy_ref",
            "authority_policy_version",
            "purpose_id",
            "purpose_version",
            "selector_slot",
        },
        "human policy",
    )
    uses = root.get("required_uses")
    if type(uses) is not list or len(uses) != 1 or type(uses[0]) is not dict:
        raise ValueError("EXACT_STOCKROOM_HUMAN_USE_REQUIRED")
    use = uses[0]
    _exact_keys(
        use,
        {
            "scenario_id",
            "scenario_version",
            "task_contract_id",
            "task_contract_version",
            "source_state",
            "target_state",
        },
        "human required use",
    )
    if (
        use["scenario_id"] != "stockroom-s4-human-owned-claim"
        or use["scenario_version"] != "1.0.0"
        or policy["purpose_id"] != "P1_7_WORK_RESULT_REVIEW"
        or policy["purpose_version"] != "v1"
    ):
        raise ValueError("STOCKROOM_HUMAN_USE_MISMATCH")
    return {
        "authority_policy_ref": _text(policy, "authority_policy_ref"),
        "authority_policy_version": _text(policy, "authority_policy_version"),
        "required_use": {
            "scenario_id": _text(use, "scenario_id"),
            "scenario_version": _text(use, "scenario_version"),
            "task_contract_id": _text(use, "task_contract_id"),
            "task_contract_version": _text(use, "task_contract_version"),
            "source_state": WorkflowState(_text(use, "source_state")),
            "target_state": WorkflowState(_text(use, "target_state")),
            "purpose_id": _text(policy, "purpose_id"),
            "purpose_version": _text(policy, "purpose_version"),
            "selector_slot": _text(policy, "selector_slot"),
        },
    }


def load_stockroom_judgment_config(path: Path) -> dict[str, Any]:
    root = _strict_json(path)
    _exact_keys(
        root,
        {"schema_id", "schema_version", "authority_version", "issued_at", "policies"},
        "judgment root",
    )
    schema = (_text(root, "schema_id"), _text(root, "schema_version"))
    if schema not in {
        ("AISCC-STOCKROOM-CAPTURE-JUDGMENT-V1", "1"),
        ("AISCC-STOCKROOM-CAPTURE-JUDGMENT-V2", "2"),
    }:
        raise ValueError("STOCKROOM_JUDGMENT_SCHEMA_DENIED")
    expected = {
        "scenario_id",
        "scenario_version",
        "policy_id",
        "policy_version",
        "task_contract_id",
        "task_contract_version",
        "source_state",
        "target_state",
        "owner_policy",
        "deterministic_kind",
        "requires_human_result",
        "requires_post_human_evidence",
    }
    if schema[1] == "2":
        expected |= {
            "evidence_basis_kind",
            "evidence_checkpoint_ref",
            "evidence_requirement_set_ref",
        }
    raw_policies = root.get("policies")
    if type(raw_policies) is not list or len(raw_policies) != 2:
        raise ValueError("EXACT_STOCKROOM_JUDGMENT_POLICIES_REQUIRED")
    policies: list[dict[str, Any]] = []
    for raw in raw_policies:
        if type(raw) is not dict:
            raise ValueError("judgment policy must be an object")
        _exact_keys(raw, expected, "judgment policy")
        item = dict(raw)
        item["source_state"] = WorkflowState(_text(raw, "source_state"))
        item["target_state"] = WorkflowState(_text(raw, "target_state"))
        item["owner_policy"] = JudgmentOwnerPolicy(_text(raw, "owner_policy"))
        item["deterministic_kind"] = JudgmentKind(_text(raw, "deterministic_kind"))
        if schema[1] == "2":
            item["evidence_basis_kind"] = JudgmentEvidenceBasisKind(
                _text(raw, "evidence_basis_kind")
            )
            item["evidence_checkpoint_ref"] = _text(raw, "evidence_checkpoint_ref")
            item["evidence_requirement_set_ref"] = _text(
                raw, "evidence_requirement_set_ref"
            )
        else:
            item["evidence_basis_kind"] = None
            item["evidence_checkpoint_ref"] = None
            item["evidence_requirement_set_ref"] = None
        for key in ("requires_human_result", "requires_post_human_evidence"):
            if type(raw[key]) is not bool:
                raise ValueError(f"{key} must be boolean")
        policies.append(item)
    if tuple(item["scenario_id"] for item in policies) != SCENARIO_IDS[:2]:
        raise ValueError("JUDGMENT_ONLY_S1_S2")
    if schema[1] == "2" and (
        policies[0]["evidence_basis_kind"]
        is not JudgmentEvidenceBasisKind.SATISFIED_ATTESTATION
        or policies[0]["target_state"] is not WorkflowState.ACCEPTED
        or policies[1]["evidence_basis_kind"]
        is not JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION
        or policies[1]["target_state"] is not WorkflowState.REWORK_REQUIRED
    ):
        raise ValueError("STOCKROOM_JUDGMENT_EVIDENCE_BASIS_MISMATCH")
    return {
        "authority_version": _text(root, "authority_version"),
        "issued_at": _aware_datetime(root, "issued_at"),
        "policies": tuple(policies),
    }


def _build_evidence_enrollment(
    item: dict[str, Any],
    authority: TaskContractEvidenceAuthority,
    durable_policy_fingerprint: str,
    runtime_issuer: TokenEvidenceIssuer,
    static_issuer: TokenEvidenceIssuer,
) -> StockroomEvidenceEnrollment:
    checkpoint = authority.seal_checkpoint(
        EvidenceCheckpoint(
            EvidenceCheckpointRef(item["checkpoint_id"], item["checkpoint_version"]),
            item["task_contract_id"],
            item["task_contract_version"],
            item["source_state"],
            item["target_state"],
            None,
            None,
            item["requirement_set_id"],
            item["requirement_set_version"],
            authority.authority_id,
            authority.authority_version,
            item["issued_at"],
        )
    )
    requirement = authority.seal_requirement(
        EvidenceRequirement(
            EvidenceRequirementRef(item["requirement_id"], item["requirement_version"]),
            item["task_contract_id"],
            item["task_contract_version"],
            item["requirement_set_id"],
            item["requirement_set_version"],
            EvidenceSemanticOwner.P1_6_EVIDENCE,
            EvidenceRequirementProfile.EXECUTOR_REQUIRED,
            RequirementObligation.REQUIRED,
            (checkpoint.ref.serialized(),),
            item["evidence_type_id"],
            item["evidence_type_version"],
            frozenset({item["issuer_type"]}),
            frozenset({item["issuer_id"]}),
            frozenset(),
            frozenset({item["content_kind"]}),
            item["content_schema_id"],
            item["content_schema_version"],
            item["subject_id"],
            item["scope_id"],
            item["resource_id"],
            FreshnessPolicy(FreshnessPolicyKind.WORKRUN_STATE_VERSION_SCOPED),
            item["required_coverage"],
            1,
            frozenset(),
            item["maximum_sensitivity"],
            item["public_export_allowed"],
            item["issued_at"],
            "",
            fingerprint_schema=RequirementFingerprintSchema.V2_DURABLE_CONTENT,
            durable_content_requirement=DurableContentRequirement.REQUIRED,
            durable_content_policy_ref="P1_6_STOCKROOM_CAPTURE_DURABLE_CONTENT_POLICY@v1",
            durable_content_policy_fingerprint=durable_policy_fingerprint,
        )
    )
    requirement_set = authority.seal_set(
        EvidenceRequirementSet(
            item["requirement_set_id"],
            item["requirement_set_version"],
            item["task_contract_id"],
            item["task_contract_version"],
            (requirement.ref.serialized(),),
            "",
            (checkpoint.ref.serialized(),),
            EvidenceSemanticOwner.P1_6_EVIDENCE,
            EVIDENCE_AUTHORITY_VERSION,
            item["issued_at"],
            "",
        ),
        (requirement,),
        (checkpoint,),
    )
    issuer = (
        static_issuer
        if item["issuer_type"] is EvidenceIssuerType.SYSTEM_STATIC_PROOF
        else runtime_issuer
    )
    if issuer.issuer_id != item["issuer_id"] or issuer.issuer_version != item["issuer_version"]:
        raise ValueError("evidence issuer enrollment mismatch")
    return StockroomEvidenceEnrollment(
        item["scenario_id"],
        item["scenario_version"],
        requirement_set,
        requirement,
        checkpoint,
        issuer,
    )


def scenario_id_to_profile(scenario_id: str) -> str:
    return (
        "stockroom-owner-s1-v1",
        "stockroom-owner-s2-v1",
        "stockroom-owner-s3-v1",
        "stockroom-owner-s4-v1",
    )[SCENARIO_IDS.index(scenario_id)]


def _server_initial_inputs(scenario_id: str) -> dict[str, tuple[dict[str, Any], ...]]:
    return {
        scenario_id: (
            {
                "type": "message",
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Run the fixed server-owned Stockroom scenario.",
                    }
                ],
            },
        )
    }


def _stable_digest(*parts: str) -> str:
    return hashlib.sha256("\x00".join(parts).encode("utf-8")).hexdigest()


def _path_fingerprint(path: Path) -> str:
    return canonical_sha256({"absolute_path": str(path)})


def _production_factory_fingerprint(
    semantic_role: str,
    application: StockroomProductionApplication,
) -> str:
    return canonical_sha256(
        {
            "semantic_role": semantic_role,
            "project_id": application.project_id,
            "requester_identity": application.requester_identity,
            "composition_fingerprint": application.composition.fingerprints.composition_sha256,
            "repository_root_fingerprint": _path_fingerprint(application.repository_root),
            "runtime_root_fingerprint": _path_fingerprint(application.private_runtime_root),
            "security_profile_version": _SECURITY_PROFILE_VERSION,
        }
    )


def _materialization_authority_fingerprint(authority: MaterializationAuthority) -> str:
    binding = authority.binding
    return canonical_sha256(
        {
            "binding": {
                "mode": binding.mode.value,
                "scenario_id": binding.scenario_id,
                "scenario_version": binding.scenario_version,
                "resource_ref": binding.resource_ref,
                "run_id": binding.run_id,
                "attempt_id": binding.attempt_id,
                "state": binding.state.value,
                "state_version": binding.state_version,
                "profile_version": binding.profile_version,
                "config_sha256": binding.config_sha256,
            },
            "principal_ref": authority.principal_ref,
            "security_admission_ref": authority.security_admission_ref,
            "repository_grant_ref": authority.repository_grant_ref,
            "filesystem_grant_ref": authority.filesystem_grant_ref,
            "operation_fingerprint": authority.operation_fingerprint,
            "repository_root_fingerprint": _path_fingerprint(authority.repository_root),
            "runtime_root_fingerprint": _path_fingerprint(authority.runtime_root),
        }
    )


def _tool_registry_fingerprint(
    registry: ToolRegistry,
    spec: DockerRunSpec,
    application: StockroomProductionApplication,
) -> str:
    expected = build_stockroom_registry(application.composition.tool_config, spec)
    if registry != expected:
        raise AuthorityConflictError("foreign or mismatched Stockroom ToolRegistry")
    return canonical_sha256(
        {
            "registry_id": registry.registry_id,
            "registry_version": registry.version,
            "tool_ids": list(registry.tools),
            "docker_spec_fingerprint": stockroom_spec_fingerprint(spec),
            "composition_fingerprint": application.composition.fingerprints.composition_sha256,
        }
    )


def _dispatcher_fingerprint(
    dispatcher: StockroomSummaryDispatcher,
    spec: DockerRunSpec,
    application: StockroomProductionApplication,
) -> str:
    spec_fingerprint = stockroom_spec_fingerprint(spec)
    if (
        type(dispatcher) is not StockroomSummaryDispatcher
        or dispatcher._runtime is not application.docker_runtime
        or dispatcher._spec is not spec
        or dispatcher._spec_fingerprint != spec_fingerprint
    ):
        raise AuthorityConflictError("foreign or mismatched Stockroom dispatcher")
    return canonical_sha256(
        {
            "dispatcher": "StockroomSummaryDispatcher",
            "dispatcher_version": application.composition.tool_config.dispatcher_version,
            "docker_spec_fingerprint": spec_fingerprint,
        }
    )


def _derive_runtime_summary_observation(
    *,
    expected_attempt_id: str,
    agent_output: ExecutionOutputRefRow | None,
    tool_output: ExecutionOutputRefRow | None,
    agent_verified: bool,
    tool_verified: bool,
) -> dict[str, object]:
    if (
        agent_output is None
        or agent_output.execution_attempt_id != expected_attempt_id
        or agent_output.ref_kind != "AgentOutputRef"
        or not agent_verified
    ):
        raise AuthorityConflictError("authentic same-attempt AgentOutputRef required")
    expected_tool_hash = canonical_sha256(STOCKROOM_SUMMARY)
    if (
        tool_output is None
        or tool_output.execution_attempt_id != expected_attempt_id
        or tool_output.ref_kind != "ToolOutputRef"
        or tool_output.content_hash != expected_tool_hash
        or not tool_verified
    ):
        raise AuthorityConflictError("authentic canonical Stockroom ToolOutputRef required")

    summary = json.loads(canonical_json_bytes(STOCKROOM_SUMMARY))
    if not isinstance(summary, dict) or not isinstance(summary.get("items"), list):
        raise AuthorityConflictError("canonical Stockroom summary shape is invalid")
    items = summary["items"]
    if not all(
        isinstance(item, dict)
        and type(item.get("available")) is int
        and type(item.get("reorder_level")) is int
        and type(item.get("needs_reorder")) is bool
        for item in items
    ):
        raise AuthorityConflictError("canonical Stockroom item shape is invalid")
    total_available = sum(cast(int, item["available"]) for item in items)
    if total_available != summary.get("total_available") or not all(
        cast(bool, item["needs_reorder"])
        is (cast(int, item["available"]) <= cast(int, item["reorder_level"]))
        for item in items
    ):
        raise AuthorityConflictError("canonical Stockroom summary rule is inconsistent")
    return {
        "agent_output_ref": agent_output.output_ref_id,
        "agent_output_hash": agent_output.content_hash,
        "tool_output_ref": tool_output.output_ref_id,
        "tool_output_hash": tool_output.content_hash,
        "summary": summary,
        "total_available": total_available,
        "reorder_rule": "available <= reorder_level",
    }


def _stable_id(prefix: str, *parts: str) -> str:
    return f"{prefix}-{_stable_digest(prefix, *parts)[:48]}"


def _is_sha256(value: object) -> bool:
    return type(value) is str and len(value) == 64 and set(value) <= _SHA256


def _strict_json(path: Path) -> dict[str, Any]:
    def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise ValueError(f"duplicate JSON key: {key}")
            value[key] = item
        return value

    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique)
    if type(value) is not dict:
        raise ValueError("configuration root must be an object")
    return value


def _exact_keys(value: Mapping[str, Any], expected: set[str], owner: str) -> None:
    if set(value) != expected:
        raise ValueError(f"{owner} has unknown or missing keys")


def _table(value: Mapping[str, Any], key: str) -> dict[str, Any]:
    result = value.get(key)
    if type(result) is not dict:
        raise ValueError(f"{key} must be an object")
    return result


def _text(value: Mapping[str, Any], key: str) -> str:
    result = value.get(key)
    if type(result) is not str or not result:
        raise ValueError(f"{key} must be a non-empty string")
    return result


def _string_list(value: Mapping[str, Any], key: str) -> list[str]:
    result = value.get(key)
    if (
        type(result) is not list
        or not result
        or not all(type(item) is str and item for item in result)
    ):
        raise ValueError(f"{key} must be a non-empty string array")
    if len(result) != len(set(result)):
        raise ValueError(f"{key} must not contain duplicates")
    return result


def _positive_int(value: Mapping[str, Any], key: str) -> int:
    result = value.get(key)
    if type(result) is not int or result <= 0:
        raise ValueError(f"{key} must be a positive integer")
    return result


def _aware_datetime(value: Mapping[str, Any], key: str) -> datetime:
    result = datetime.fromisoformat(_text(value, key))
    if result.tzinfo is None:
        raise ValueError(f"{key} must be timezone-aware")
    return result
