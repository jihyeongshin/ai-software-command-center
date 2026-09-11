from __future__ import annotations

import asyncio
import os
from collections.abc import Coroutine
from copy import deepcopy
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import pytest
from sqlalchemy import func, select, text

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.cycle.models import (
    CycleAdmissionError,
    CycleAdmissionErrorCode,
    CycleAdmissionRequest,
    CycleCandidate,
    MemoryCategory,
    MemoryDeclaration,
    p1_8_task_binding_fingerprint,
)
from aiscc.cycle.repository import PostgresCycleAdmissionRepository
from aiscc.evidence.admission import (
    EvidenceAdmissionEvaluator,
    EvidenceContentRegistry,
    make_admission_request,
)
from aiscc.evidence.attestation import EvidenceCheckpointUseRegistry, EvidenceGuardAuthority
from aiscc.evidence.content import (
    P1_6HistoricalContentAccessAuthority,
    PrivateEvidenceContentStore,
)
from aiscc.evidence.issuers import EvidenceIssuerRegistry, P1_7HumanEvidenceIssuerAuthority
from aiscc.evidence.models import (
    EvidenceAdmissionOutcome,
    EvidenceCandidate,
    EvidenceCheckpoint,
    EvidenceCheckpointRef,
    EvidenceContentKind,
    EvidenceIssuerType,
    EvidenceOwner,
    EvidenceRequirement,
    EvidenceRequirementProfile,
    EvidenceRequirementRef,
    EvidenceRequirementSet,
    EvidenceSemanticOwner,
    EvidenceSensitivity,
    EvidenceSetEvaluationRef,
    EvidenceSetOutcome,
    FreshnessPolicy,
    FreshnessPolicyKind,
    HumanEvidenceProducerCategory,
    RequirementObligation,
    canonical_hash,
)
from aiscc.evidence.repository import PostgresEvidenceRepository
from aiscc.evidence.requirements import TaskContractEvidenceAuthority
from aiscc.evidence.service import EvidenceAdmissionService
from aiscc.human.authority import (
    HumanGateReservationAuthority,
    HumanGuardAuthority,
    HumanPrincipalAuthority,
)
from aiscc.human.models import (
    HumanAuthorityError,
    HumanGate,
    HumanGateStatus,
    HumanResult,
    HumanResultIdentityConflictError,
    HumanResultKind,
    human_guard_attestation_fingerprint,
    human_guard_attestation_payload,
)
from aiscc.human.repository import (
    PostgresHumanAuthorityRepository,
    _human_guard_attestation_from_row,
    _human_result_fingerprint,
    _human_result_proposal_fingerprint,
    _result_row,
)
from aiscc.judgment.authority import (
    CommandCenterAuthority,
    JudgmentPolicyAuthority,
    PostgresJudgmentAuthority,
    _judgment_fingerprint,
    _judgment_from_row,
    _judgment_proposal_fingerprint,
    _judgment_row,
    _policy_fingerprint,
    _policy_use_fingerprint,
    _verify_judgment_historical_provenance_in_session,
)
from aiscc.judgment.models import (
    CommandCenterPrincipal,
    Judgment,
    JudgmentAuthorityError,
    JudgmentEvidenceBasisKind,
    JudgmentIdentityConflictError,
    JudgmentKind,
    JudgmentOwnerPolicy,
    JudgmentPolicy,
)
from aiscc.memory.models import (
    MemoryAuthorityMode,
    P1_8MemoryDeclarationPolicyAuthority,
    default_memory_policy,
    default_memory_policy_authority,
    memory_content_fingerprint,
)
from aiscc.next_action.models import (
    default_next_action_policy_authority,
)
from aiscc.next_action.repository import PostgresNextActionRepository
from aiscc.persistence import PostgresTransitionRepository, create_engine, create_session_factory
from aiscc.persistence.models import (
    AdmittedCycleRow,
    EvidenceAuthorityEventRow,
    EvidenceSetAttestationRow,
    EvidenceSetEvaluationRow,
    HumanGateAuthorityEventRow,
    HumanGateProjectionRow,
    HumanGateRow,
    HumanGuardAttestationRow,
    HumanP1_7EvidenceProducerRow,
    HumanResultAuthorityEventRow,
    HumanResultRow,
    JudgmentAuthorityEventRow,
    JudgmentEvaluationRow,
    JudgmentProjectionRow,
    JudgmentRow,
    P1_4BlockerProvenanceRow,
    ProjectMemoryViewRow,
    TransitionDecisionRow,
    TransitionEvaluationRow,
    TransitionRequestRow,
)
from aiscc.persistence.repository import (
    _historical_evaluation_from_row,
    _request_fingerprint,
    _transition_request_from_row,
    acquire_work_run_transaction_lock,
)
from aiscc.task_authority.authority import _bind_repository_once
from aiscc.task_authority.models import TaskConstraintScopeKind, TaskConstraintScopeV1
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository
from aiscc.workflow.evaluator import TransitionEvaluator
from aiscc.workflow.guards import GUARD_OWNER_POLICY, P1_4GuardAuthority
from aiscc.workflow.kernel import WorkflowKernel
from aiscc.workflow.matrix import TRANSITION_MATRIX
from aiscc.workflow.models import (
    BlockerKindV1,
    BlockerReasonCodeV1,
    DecisionOutcome,
    DecisionReason,
    GuardId,
    GuardSemanticOwner,
    P1_4BlockerClaimV1,
    P1_4BlockerResolutionClaimV1,
    RequesterType,
    TransitionRequest,
)
from aiscc.workflow.participants import CompositeTransitionParticipant

NOW = datetime(2026, 8, 30, 1, 30, tzinfo=UTC)


def test_legacy_judgment_identity_remains_byte_compatible() -> None:
    use_fingerprint = _policy_use_fingerprint(
        "legacy-task",
        "v1",
        WorkflowState.ADMISSION_PENDING,
        WorkflowState.REJECTED,
    )
    assert use_fingerprint == "8c1b08dde646d91b7fee433d647b6c7439d1dd0b68df7d37af068ec8dcb37040"
    policy = JudgmentPolicy(
        "legacy-policy",
        "v1",
        "",
        "legacy-task",
        "v1",
        WorkflowState.ADMISSION_PENDING,
        WorkflowState.REJECTED,
        use_fingerprint,
        JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC,
        False,
        False,
        JudgmentKind.REJECTED,
        "AISCC_P1_7_JUDGMENT_POLICY_AUTHORITY_V1",
        "p1-7-judgment-policy-v1",
        1,
        NOW,
    )
    policy_fingerprint = _policy_fingerprint(policy)
    assert policy_fingerprint == "64478c83bfed1ca5c7050b238faf2489975aa5b7ef6918d09d2b0b1a1b98eb6f"
    assert policy.serialized_ref == "p1-7-judgment-policy:v1:legacy-policy"
    judgment = Judgment(
        "legacy-judgment",
        "v1",
        "",
        "AISCC_P1_7_JUDGMENT_AUTHORITY_V1",
        "AISCC-P1-7-JUDGMENT-AUTHORITY-V1",
        1,
        "legacy-task",
        "v1",
        "legacy-run",
        WorkflowState.ADMISSION_PENDING,
        3,
        WorkflowState.REJECTED,
        use_fingerprint,
        JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC,
        "legacy-policy",
        "v1",
        policy_fingerprint,
        "AISCC_P1_7_JUDGMENT_POLICY_AUTHORITY_V1",
        "p1-7-judgment-policy-v1",
        1,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        JudgmentKind.REJECTED,
        "LEGACY_REJECTED",
        "v1",
        "legacy-evaluation",
        NOW,
    )
    assert _judgment_fingerprint(judgment) == (
        "99aa9b1d1f3850a024b7449bb942a748c9dfb75161c0eedeb53f892aa07f511f"
    )
    assert judgment.serialized_ref == "p1-7-judgment:v1:legacy-judgment"


class TestBlockerSourceVerifier:
    async def verify_resolution_source(self, session: Any, **values: Any) -> bool:
        del session
        claim = values["claim"]
        return (
            values["resolution_source_contract_ref"] == "resolution-contract:v1:test"
            and values["resolution_source_contract_fingerprint"] == "a" * 64
            and claim.resolution_source_authority_ref == "resolution-authority:v1:test"
            and claim.resolution_source_authority_fingerprint == "b" * 64
        )


def run[T](coroutine: Coroutine[Any, Any, T]) -> T:
    return asyncio.run(coroutine)


@pytest.fixture(scope="module")
def database_url() -> str:
    value = os.environ.get("AISCC_TEST_DATABASE_URL")
    if not value:
        pytest.skip("AISCC_TEST_DATABASE_URL is required for PostgreSQL P1-7 evidence")
    return value


def request(
    task_id: str,
    run_id: str,
    source: WorkflowState | None,
    version: int,
    target: WorkflowState,
    *,
    evidence_refs: tuple[str, ...] = (),
    human_result_refs: tuple[str, ...] = (),
    judgment_refs: tuple[str, ...] = (),
    blocker_kind: BlockerKindV1 = BlockerKindV1.EXECUTION,
    blocker_resolution_claim: P1_4BlockerResolutionClaimV1 | None = None,
) -> TransitionRequest:
    transition_request_id = str(uuid4())
    reason_code = (
        BlockerReasonCodeV1.SECURITY_BOUNDARY
        if blocker_kind is BlockerKindV1.SECURITY
        else BlockerReasonCodeV1.EXECUTION_BLOCKER
    )
    blocker_claim = (
        P1_4BlockerClaimV1(
            f"blocker-{transition_request_id}",
            blocker_kind,
            reason_code,
            "resolution-contract:v1:test",
            "a" * 64,
            ("source-authority:v1:test",),
            ("c" * 64,),
        )
        if target is WorkflowState.BLOCKED
        else None
    )
    return TransitionRequest(
        transition_request_id,
        "aiscc-project",
        task_id,
        "v1",
        run_id,
        source,
        version,
        target,
        "aiscc-system",
        RequesterType.SYSTEM,
        RuntimeMode.OWNER_SELF_DOGFOOD,
        evidence_refs=evidence_refs,
        human_result_refs=human_result_refs,
        judgment_refs=judgment_refs,
        blocker_claim=blocker_claim,
        blocker_resolution_claim=blocker_resolution_claim,
        created_at=NOW,
    )


def system_facts(authority: P1_4GuardAuthority, value: TransitionRequest) -> tuple[Any, ...]:
    result = []
    for guard in TRANSITION_MATRIX[(value.observed_state, value.target_state)]:
        if GUARD_OWNER_POLICY[guard] is not GuardSemanticOwner.P1_4_SYSTEM:
            continue
        result.append(
            authority.issue(
                guard_id=guard,
                satisfied=True,
                reason="TEST_SYSTEM_AUTHORITY",
                authority_ref=f"test:{guard.value}",
                request=value,
            )
        )
    return tuple(result)


async def blocker_resolution_claim(sessions: Any, work_run_id: str) -> P1_4BlockerResolutionClaimV1:
    async with sessions() as session:
        blocker = await session.scalar(
            select(P1_4BlockerProvenanceRow).where(
                P1_4BlockerProvenanceRow.work_run_id == work_run_id
            )
        )
    assert blocker is not None
    return P1_4BlockerResolutionClaimV1(
        blocker.blocker_ref,
        blocker.blocker_fingerprint,
        "resolution-source:v1:test",
        "d" * 64,
        "resolution-authority:v1:test",
        "b" * 64,
    )


def evidence_authority_snapshot(
    task_id: str,
) -> tuple[
    TaskContractEvidenceAuthority,
    EvidenceRequirementSet,
    tuple[EvidenceRequirement, ...],
    tuple[EvidenceCheckpoint, ...],
]:
    set_id = f"human-set-{task_id}"
    owner = TaskContractEvidenceAuthority("TASK_EVIDENCE_AUTHORITY", "v1")
    pre = owner.seal_checkpoint(
        EvidenceCheckpoint(
            EvidenceCheckpointRef(f"pre-{task_id}", "v1"),
            task_id,
            "v1",
            WorkflowState.ADMISSION_PENDING,
            WorkflowState.HUMAN_REQUIRED,
            None,
            None,
            set_id,
            "v1",
            owner.authority_id,
            owner.authority_version,
            NOW,
        )
    )
    post = owner.seal_checkpoint(
        EvidenceCheckpoint(
            EvidenceCheckpointRef(f"post-{task_id}", "v1"),
            task_id,
            "v1",
            WorkflowState.HUMAN_REQUIRED,
            WorkflowState.ACCEPTED,
            None,
            None,
            set_id,
            "v1",
            owner.authority_id,
            owner.authority_version,
            NOW,
        )
    )
    negative = owner.seal_checkpoint(
        EvidenceCheckpoint(
            EvidenceCheckpointRef(f"negative-{task_id}", "v1"),
            task_id,
            "v1",
            WorkflowState.ADMISSION_PENDING,
            WorkflowState.REWORK_REQUIRED,
            None,
            None,
            set_id,
            "v1",
            owner.authority_id,
            owner.authority_version,
            NOW,
        )
    )
    human = owner.seal_requirement(
        EvidenceRequirement(
            EvidenceRequirementRef(f"human-result-{task_id}", "v1"),
            task_id,
            "v1",
            set_id,
            "v1",
            EvidenceSemanticOwner.P1_6_EVIDENCE,
            EvidenceRequirementProfile.HUMAN_OWNED,
            RequirementObligation.REQUIRED,
            (post.ref.serialized(),),
            "AISCC_HUMAN_RESULT_REVIEW",
            "v1",
            frozenset({EvidenceIssuerType.HUMAN_P1_7}),
            frozenset({"AISCC_P1_7_HUMAN_EVIDENCE_PRODUCER_V1"}),
            frozenset({HumanEvidenceProducerCategory.HUMAN_P1_7}),
            frozenset({EvidenceContentKind.HUMAN_STRUCTURED_REF}),
            "AISCC-HUMAN-RESULT",
            "v1",
            "work-result",
            "final-review",
            None,
            FreshnessPolicy(FreshnessPolicyKind.HUMAN_RESULT_SCOPED),
            frozenset({"human-review"}),
            0,
            frozenset(),
            EvidenceSensitivity.INTERNAL,
            False,
            NOW,
            "",
        )
    )
    missing = owner.seal_requirement(
        EvidenceRequirement(
            EvidenceRequirementRef(f"negative-proof-{task_id}", "v1"),
            task_id,
            "v1",
            set_id,
            "v1",
            EvidenceSemanticOwner.P1_6_EVIDENCE,
            EvidenceRequirementProfile.EXECUTOR_REQUIRED,
            RequirementObligation.REQUIRED,
            (negative.ref.serialized(),),
            "AISCC_NEGATIVE_PROOF",
            "v1",
            frozenset({EvidenceIssuerType.SYSTEM_STATIC_PROOF}),
            frozenset({"AISCC_TEST_NEGATIVE_ISSUER_V1"}),
            frozenset(),
            frozenset({EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY}),
            "AISCC-NEGATIVE-PROOF",
            "v1",
            "negative-proof",
            "judgment",
            None,
            FreshnessPolicy(FreshnessPolicyKind.WORKRUN_STATE_VERSION_SCOPED),
            frozenset({"proof"}),
            0,
            frozenset(),
            EvidenceSensitivity.INTERNAL,
            False,
            NOW,
            "",
        )
    )
    requirement_set = owner.seal_set(
        EvidenceRequirementSet(
            set_id,
            "v1",
            task_id,
            "v1",
            (human.ref.serialized(), missing.ref.serialized()),
            "",
            (pre.ref.serialized(), post.ref.serialized(), negative.ref.serialized()),
            EvidenceSemanticOwner.P1_6_EVIDENCE,
            "p1-6-authority-v1",
            NOW,
            "",
        ),
        (human, missing),
        (pre, post, negative),
    )
    return owner, requirement_set, (human, missing), (pre, post, negative)


@pytest.mark.postgres
def test_p1_7_postgres_runtime_proof(database_url: str) -> None:
    async def scenario() -> None:
        label = uuid4().hex
        task_id = f"task-p1-7-live-{label}"
        run_id = f"run-p1-7-live-{uuid4()}"
        engine = create_engine(database_url)
        sessions = create_session_factory(engine)
        external_task_repository = PostgresExternalTaskAuthorityRepository(sessions)
        external_task_writer = _bind_repository_once(external_task_repository)
        task_constraint, _ = await external_task_writer.issue_task_constraint(
            constraint_ref_id=f"task-constraint-{label}",
            logical_constraint_id=f"task-constraint-lineage-{label}",
            scope=TaskConstraintScopeV1(
                TaskConstraintScopeKind.TASK_CONTRACT,
                "aiscc-project",
                task_id,
                "v1",
            ),
            constraint_schema_id="TASK_CONSTRAINT_PAYLOAD_V1",
            constraint_schema_version="v1",
            constraint_payload_ref=f"task-constraint-payload:v1:{label}",
            constraint_payload_fingerprint="a" * 64,
            event_id=f"task-constraint-issued-{label}",
            issued_at=NOW,
        )
        task_constraint_snapshot = await external_task_writer.certify_snapshot(
            snapshot_id=f"task-constraint-snapshot-{label}", issued_at=NOW
        )
        historical_content_access = P1_6HistoricalContentAccessAuthority()
        evidence_repository = PostgresEvidenceRepository(
            sessions,
            historical_content_access_authority=historical_content_access,
        )
        evidence_owner, requirement_set, requirements, checkpoints = evidence_authority_snapshot(
            task_id
        )
        pre, post, negative_checkpoint = checkpoints
        await evidence_repository.register_authority(
            requirement_set=requirement_set,
            requirements=requirements,
            checkpoints=checkpoints,
            authority=evidence_owner,
        )
        human_repository = PostgresHumanAuthorityRepository(sessions, clock=lambda: NOW)
        reservation_authority = HumanGateReservationAuthority(
            frozenset(
                {
                    (
                        task_id,
                        "v1",
                        WorkflowState.ADMISSION_PENDING,
                        WorkflowState.HUMAN_REQUIRED,
                    )
                }
            )
        )
        checkpoint_uses = EvidenceCheckpointUseRegistry(checkpoints)
        human_guard = HumanGuardAuthority(
            sessions,
            human_repository,
            evidence_repository,
            checkpoint_uses,
            reservation_authority,
            clock=lambda: NOW,
        )
        evidence_guard = EvidenceGuardAuthority(evidence_repository, checkpoint_uses)
        judgment_policy_authority = JudgmentPolicyAuthority(sessions, clock=lambda: NOW)
        judgment_authority = PostgresJudgmentAuthority(
            sessions, evidence_repository, judgment_policy_authority, clock=lambda: NOW
        )
        system = P1_4GuardAuthority()
        repository = PostgresTransitionRepository(
            sessions,
            TransitionEvaluator(system, (evidence_guard, human_guard, judgment_authority)),
            TestBlockerSourceVerifier(),
        )
        kernel = WorkflowKernel(repository)
        for source, version, target in (
            (None, 0, WorkflowState.READY),
            (WorkflowState.READY, 1, WorkflowState.RUNNING),
            (WorkflowState.RUNNING, 2, WorkflowState.ADMISSION_PENDING),
        ):
            step = request(task_id, run_id, source, version, target)
            decision = await kernel.request_transition(step, system_facts(system, step))
            assert decision.outcome is DecisionOutcome.ADMITTED
        pre_evaluation, pre_attestation = await evidence_repository.evaluate_set(
            work_run_id=run_id,
            checkpoint_ref=pre.ref,
            observed_state=WorkflowState.ADMISSION_PENDING,
            observed_state_version=3,
            authority_id="AISCC_P1_6_EVIDENCE_AUTHORITY_V1",
            authority_version="AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
            now=NOW,
        )
        assert pre_evaluation.ordered_applicable_requirement_refs == ()
        assert pre_attestation is not None
        gate_request = request(
            task_id,
            run_id,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.HUMAN_REQUIRED,
        )
        reservation = reservation_authority.reserve(
            gate_request, designated_principal_selector_fingerprint="reviewers-v1"
        )
        missing_participant = await human_guard.gate_open_participant(
            gate_request, reservation, "p1-6-attestation:missing:missing"
        )
        missing_decision = await kernel.request_transition(
            replace(gate_request, transition_request_id=str(uuid4())),
            (),
            transaction_participant=missing_participant,
        )
        assert missing_decision.outcome is DecisionOutcome.DENIED
        assert await kernel.load(run_id) is not None
        participant = await human_guard.gate_open_participant(
            gate_request, reservation, pre_attestation.serialized_ref
        )
        open_decision = await kernel.request_transition(
            gate_request, (), transaction_participant=participant
        )
        assert open_decision.outcome is DecisionOutcome.ADMITTED
        gate = await human_repository.load_gate(
            f"p1-7-gate:{reservation.human_gate_version}:{reservation.human_gate_id}"
        )
        assert gate is not None and gate.bound_state_version == 4

        principal_authority = HumanPrincipalAuthority(human_repository, clock=lambda: NOW)
        principal = principal_authority.authenticate(
            principal_id="internal-reviewer",
            session_id="private-session",
            role_refs=("reviewer",),
        )
        rogue_principal = HumanPrincipalAuthority(human_repository, clock=lambda: NOW).authenticate(
            principal_id="caller-claimed-human",
            session_id="caller-session",
            role_refs=("reviewer",),
        )
        with pytest.raises(HumanAuthorityError):
            await principal_authority.issue_action_authority(
                rogue_principal,
                gate.serialized_ref,
                idempotency_scope="forged-authority",
            )
        action = await principal_authority.issue_action_authority(
            principal,
            gate.serialized_ref,
            idempotency_scope=f"human-result-{label}",
        )
        result = await human_repository.submit_result(
            human_result_id=f"human-result-{label}",
            human_result_version="v1",
            gate_ref=gate.serialized_ref,
            principal=principal,
            action_authority=action,
            result_kind=HumanResultKind.APPROVE,
            structured_reason_code="REVIEW_ACCEPTED",
            reason_vocabulary_version="v1",
            idempotency_key=f"human-result-{label}",
            submitted_at=NOW,
        )
        duplicate = await human_repository.submit_result(
            human_result_id=f"human-result-{label}",
            human_result_version="v1",
            gate_ref=gate.serialized_ref,
            principal=principal,
            action_authority=action,
            result_kind=HumanResultKind.APPROVE,
            structured_reason_code="REVIEW_ACCEPTED",
            reason_vocabulary_version="v1",
            idempotency_key=f"human-result-{label}",
            submitted_at=NOW,
        )
        assert duplicate == result
        with pytest.raises(HumanResultIdentityConflictError):
            await human_repository.submit_result(
                human_result_id=f"human-result-{label}",
                human_result_version="v1",
                gate_ref=gate.serialized_ref,
                principal=principal,
                action_authority=action,
                result_kind=HumanResultKind.REJECT,
                structured_reason_code="REVIEW_REJECTED",
                reason_vocabulary_version="v1",
                idempotency_key=f"human-result-{label}",
                submitted_at=NOW,
            )
        before_judgment = await kernel.load(run_id)
        assert before_judgment is not None and before_judgment.state_version == 4

        store = PrivateEvidenceContentStore("p1-7-human-content", "v1")
        content = store.put_structured(
            object_id=result.human_result_id,
            object_version="v1",
            value={"result_ref": result.serialized_ref, "kind": result.result_kind.value},
            kind=EvidenceContentKind.HUMAN_STRUCTURED_REF,
            schema_id="AISCC-HUMAN-RESULT",
            schema_version="v1",
            sensitivity=EvidenceSensitivity.INTERNAL,
        )
        producer = await human_repository.create_producer_ref(
            result_ref=result.serialized_ref,
            checkpoint_ref=post.ref.serialized(),
            evidence_type_id="AISCC_HUMAN_RESULT_REVIEW",
            evidence_type_version="v1",
            subject_id="work-result",
            scope_id="final-review",
            resource_id=None,
            content_hash=content.content_hash,
            sensitivity=EvidenceSensitivity.INTERNAL,
            export_policy="PRIVATE_AUTHORITY_ONLY",
        )
        p1_7_issuer = P1_7HumanEvidenceIssuerAuthority(human_repository)
        candidate = EvidenceCandidate(
            f"candidate-human-result-{label}",
            "v1",
            "",
            EvidenceOwner(
                EvidenceIssuerType.HUMAN_P1_7,
                p1_7_issuer.issuer_id,
                p1_7_issuer.issuer_version,
                producer.serialized_ref,
            ),
            run_id,
            None,
            None,
            task_id,
            "v1",
            post.ref,
            WorkflowState.HUMAN_REQUIRED,
            4,
            "work-result",
            "final-review",
            None,
            "AISCC_HUMAN_RESULT_REVIEW",
            "v1",
            content,
            NOW,
            NOW,
            frozenset({"human-review"}),
            producer.serialized_ref,
            HumanEvidenceProducerCategory.HUMAN_P1_7,
        )
        candidate = await p1_7_issuer.seed_candidate(candidate)
        evidence_service = EvidenceAdmissionService(
            evidence_repository,
            EvidenceAdmissionEvaluator(
                EvidenceIssuerRegistry((p1_7_issuer,)), EvidenceContentRegistry((store,))
            ),
        )
        admission_request = make_admission_request(
            admission_request_id=f"admit-human-result-{label}",
            candidate=candidate,
            requirement=requirements[0],
            requirement_set=requirement_set,
            checkpoint=post,
            work_run_id=run_id,
            observed_state=WorkflowState.HUMAN_REQUIRED,
            observed_state_version=4,
            requester_identity="aiscc-system",
            created_at=NOW,
        )
        admission, admitted = await evidence_service.submit(admission_request, candidate, now=NOW)
        assert admission.outcome is EvidenceAdmissionOutcome.ADMITTED
        assert admitted is not None
        _, post_attestation = await evidence_repository.evaluate_set(
            work_run_id=run_id,
            checkpoint_ref=post.ref,
            observed_state=WorkflowState.HUMAN_REQUIRED,
            observed_state_version=4,
            authority_id="AISCC_P1_6_EVIDENCE_AUTHORITY_V1",
            authority_version="AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
            now=NOW,
        )
        assert post_attestation is not None
        accept_request = request(
            task_id,
            run_id,
            WorkflowState.HUMAN_REQUIRED,
            4,
            WorkflowState.ACCEPTED,
            evidence_refs=(post_attestation.serialized_ref,),
            human_result_refs=(result.serialized_ref,),
        )
        policy = await judgment_policy_authority.register(
            policy_id=f"HUMAN_FINAL_REVIEW-{label}",
            policy_version="v1",
            task_contract_id=task_id,
            task_contract_version="v1",
            source_state=WorkflowState.HUMAN_REQUIRED,
            target_state=WorkflowState.ACCEPTED,
            owner_policy=JudgmentOwnerPolicy.HUMAN,
            requires_human_result=True,
            requires_post_human_evidence=True,
        )
        judgment = await judgment_authority.issue(
            judgment_id=f"judgment-{label}",
            judgment_version="v1",
            request=accept_request,
            policy=policy,
            human_result_ref=result.serialized_ref,
            evidence_attestation_ref=post_attestation.serialized_ref,
            reason_code="CURRENT_INPUTS_ACCEPTED",
            reason_vocabulary_version="v1",
        )
        corrected_judgment = await judgment_authority.issue(
            judgment_id=f"judgment-corrected-{label}",
            judgment_version="v1",
            request=accept_request,
            policy=policy,
            human_result_ref=result.serialized_ref,
            evidence_attestation_ref=post_attestation.serialized_ref,
            reason_code="CURRENT_INPUTS_ACCEPTED_CORRECTED",
            reason_vocabulary_version="v1",
            supersedes_judgment_ref=judgment.serialized_ref,
        )
        historical_judgment_counts = await _judgment_counts(sessions, run_id)
        historical_judgment_authority = PostgresJudgmentAuthority(
            sessions, evidence_repository, judgment_policy_authority
        )
        assert (
            await historical_judgment_authority.issue(
                judgment_id=f"judgment-{label}",
                judgment_version="v1",
                request=accept_request,
                policy=policy,
                human_result_ref=result.serialized_ref,
                evidence_attestation_ref=post_attestation.serialized_ref,
                reason_code="CURRENT_INPUTS_ACCEPTED",
                reason_vocabulary_version="v1",
            )
            == judgment
        )
        assert await _judgment_counts(sessions, run_id) == historical_judgment_counts

        async def replay_historical_judgment() -> None:
            with pytest.raises(JudgmentAuthorityError):
                await historical_judgment_authority.issue(
                    judgment_id=f"judgment-{label}",
                    judgment_version="v1",
                    request=accept_request,
                    policy=policy,
                    human_result_ref=result.serialized_ref,
                    evidence_attestation_ref=post_attestation.serialized_ref,
                    reason_code="CURRENT_INPUTS_ACCEPTED",
                    reason_vocabulary_version="v1",
                )

        async with sessions() as session:
            producer_row = await session.scalar(
                select(HumanP1_7EvidenceProducerRow).where(
                    HumanP1_7EvidenceProducerRow.serialized_ref == producer.serialized_ref
                )
            )
            assert producer_row is not None
            producer_original = {
                "fingerprint": producer_row.fingerprint,
                "human_result_ref": producer_row.human_result_ref,
                "work_run_id": producer_row.work_run_id,
                "payload": deepcopy(producer_row.payload),
            }

        async def corrupt_producer(field: str, value: Any) -> None:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                producer_row = await session.scalar(
                    select(HumanP1_7EvidenceProducerRow).where(
                        HumanP1_7EvidenceProducerRow.serialized_ref == producer.serialized_ref
                    )
                )
                assert producer_row is not None
                setattr(producer_row, field, value)
            await replay_historical_judgment()
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                producer_row = await session.scalar(
                    select(HumanP1_7EvidenceProducerRow).where(
                        HumanP1_7EvidenceProducerRow.serialized_ref == producer.serialized_ref
                    )
                )
                assert producer_row is not None
                for original_field, original_value in producer_original.items():
                    setattr(producer_row, original_field, deepcopy(original_value))

        def producer_payload(field: str, value: Any) -> dict[str, Any]:
            payload = deepcopy(producer_original["payload"])
            assert isinstance(payload, dict)
            payload[field] = value
            return payload

        for field, value in (
            ("fingerprint", "9" * 64),
            ("human_result_ref", f"p1-7-result:v1:missing-{uuid4()}"),
            ("work_run_id", f"foreign-run-{uuid4()}"),
            ("payload", producer_payload("task_contract_id", f"foreign-task-{uuid4()}")),
            ("payload", producer_payload("state_version", 999)),
            ("payload", producer_payload("gate_authority_revision", 999)),
            ("payload", producer_payload("result_authority_revision", 999)),
            (
                "payload",
                producer_payload("checkpoint_ref", f"foreign-checkpoint-{uuid4()}@v1"),
            ),
            ("payload", producer_payload("content_hash", "c" * 64)),
        ):
            await corrupt_producer(field, value)
        async with sessions() as session:
            transaction = await session.begin()
            try:
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                producer_row = await session.scalar(
                    select(HumanP1_7EvidenceProducerRow).where(
                        HumanP1_7EvidenceProducerRow.serialized_ref == producer.serialized_ref
                    )
                )
                assert producer_row is not None
                await session.delete(producer_row)
                await session.flush()
                judgment_row = await session.get(JudgmentRow, judgment.judgment_id)
                assert judgment_row is not None
                with pytest.raises(JudgmentAuthorityError):
                    await _verify_judgment_historical_provenance_in_session(session, judgment_row)
            finally:
                await transaction.rollback()

        async with sessions() as session:
            attestation_row = await session.scalar(
                select(EvidenceSetAttestationRow).where(
                    EvidenceSetAttestationRow.serialized_ref == post_attestation.serialized_ref
                )
            )
            assert attestation_row is not None
            attestation_payload_original = deepcopy(attestation_row.payload)
        try:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                attestation_row = await session.scalar(
                    select(EvidenceSetAttestationRow).where(
                        EvidenceSetAttestationRow.serialized_ref == post_attestation.serialized_ref
                    )
                )
                assert attestation_row is not None
                payload = deepcopy(attestation_row.payload)
                payload["admitted_ref_root_hash"] = "a" * 64
                attestation_row.payload = payload
            await replay_historical_judgment()
        finally:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                attestation_row = await session.scalar(
                    select(EvidenceSetAttestationRow).where(
                        EvidenceSetAttestationRow.serialized_ref == post_attestation.serialized_ref
                    )
                )
                assert attestation_row is not None
                attestation_row.payload = attestation_payload_original
        assert (
            await historical_judgment_authority.issue(
                judgment_id=f"judgment-{label}",
                judgment_version="v1",
                request=accept_request,
                policy=policy,
                human_result_ref=result.serialized_ref,
                evidence_attestation_ref=post_attestation.serialized_ref,
                reason_code="CURRENT_INPUTS_ACCEPTED",
                reason_vocabulary_version="v1",
            )
            == judgment
        )
        stale_judgment_request = replace(
            accept_request,
            transition_request_id=str(uuid4()),
            judgment_refs=(judgment.serialized_ref,),
        )
        stale_evidence_fact = await evidence_guard.issue_for_transition(stale_judgment_request)
        stale_human_participant = await human_guard.result_guard_participant(
            stale_judgment_request,
            next(
                guard
                for guard in TRANSITION_MATRIX[
                    (WorkflowState.HUMAN_REQUIRED, WorkflowState.ACCEPTED)
                ]
                if guard.value == "G_HUMAN_APPROVED"
            ),
        )
        stale_judgment_participant = await judgment_authority.participant(
            stale_judgment_request, judgment.serialized_ref
        )
        assert (
            await kernel.request_transition(
                stale_judgment_request,
                (stale_evidence_fact,),
                transaction_participant=CompositeTransitionParticipant(
                    (stale_human_participant, stale_judgment_participant)
                ),
            )
        ).outcome is DecisionOutcome.DENIED
        accept_request = replace(accept_request, judgment_refs=(corrected_judgment.serialized_ref,))
        post_admitted_ref = post_attestation.ordered_admitted_evidence_refs[0]
        await evidence_repository.revoke(
            subject_ref=post_admitted_ref,
            reason="CURRENT_JUDGMENT_EVIDENCE_STALE_PROOF",
            owner_id="AISCC_P1_6_EVIDENCE_AUTHORITY_V1",
            authority_version="AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
        )
        stale_current_request = replace(accept_request, transition_request_id=str(uuid4()))
        stale_current_participant = await judgment_authority.participant(
            stale_current_request, corrected_judgment.serialized_ref
        )
        current_run = await kernel.load(run_id)
        assert current_run is not None
        async with sessions() as session, session.begin():
            await stale_current_participant.prepare(session, stale_current_request, current_run)
            stale_facts = stale_current_participant.facts(stale_current_request)
            assert len(stale_facts) == 1
            assert not judgment_authority.recognizes(stale_facts[0], stale_current_request)
        async with sessions() as session, session.begin():
            await session.execute(text("SET LOCAL session_replication_role = replica"))
            invalidation = await session.scalar(
                select(EvidenceAuthorityEventRow).where(
                    EvidenceAuthorityEventRow.subject_ref == post_admitted_ref,
                    EvidenceAuthorityEventRow.reason == "CURRENT_JUDGMENT_EVIDENCE_STALE_PROOF",
                )
            )
            assert invalidation is not None
            await session.delete(invalidation)
        evidence_fact = await evidence_guard.issue_for_transition(accept_request)
        human_participant = await human_guard.result_guard_participant(
            accept_request,
            next(
                guard
                for guard in TRANSITION_MATRIX[
                    (WorkflowState.HUMAN_REQUIRED, WorkflowState.ACCEPTED)
                ]
                if guard.value == "G_HUMAN_APPROVED"
            ),
        )
        judgment_participant = await judgment_authority.participant(
            accept_request, corrected_judgment.serialized_ref
        )
        final_decision = await kernel.request_transition(
            accept_request,
            (evidence_fact,),
            transaction_participant=CompositeTransitionParticipant(
                (human_participant, judgment_participant)
            ),
        )
        assert final_decision.outcome is DecisionOutcome.ADMITTED
        final = await kernel.verify_consistency(run_id)
        assert final.state is WorkflowState.ACCEPTED and final.state_version == 5
        assert (
            await historical_judgment_authority.issue(
                judgment_id=f"judgment-{label}",
                judgment_version="v1",
                request=replace(accept_request, judgment_refs=()),
                policy=policy,
                human_result_ref=result.serialized_ref,
                evidence_attestation_ref=post_attestation.serialized_ref,
                reason_code="CURRENT_INPUTS_ACCEPTED",
                reason_vocabulary_version="v1",
            )
            == judgment
        )

        # P1-8 consumes exact P1-4/P1-6/P1-7 history. A Markdown Cycle record,
        # done Task path, or executor claim is never an input to this admission.
        memory_policy_authority = default_memory_policy_authority()
        memory_policy = default_memory_policy(NOW)
        rogue_memory_authority = P1_8MemoryDeclarationPolicyAuthority()
        with pytest.raises(CycleAdmissionError) as rogue_policy_configuration:
            PostgresCycleAdmissionRepository(
                sessions,
                evidence_repository,
                historical_content_access_grant=(
                    historical_content_access.issue_p1_8_structured_result_grant()
                ),
                memory_policy=rogue_memory_authority.issue_v1(NOW),
                memory_policy_authority=rogue_memory_authority,
                task_authority_verifier=external_task_repository,
            )
        assert (
            rogue_policy_configuration.value.code
            is CycleAdmissionErrorCode.MEMORY_POLICY_AUTHORITY_DENIED
        )
        transition_fingerprint = canonical_hash(
            {
                "admitting_owner": final_decision.admitting_owner,
                "decided_at": final_decision.decided_at.astimezone(UTC).isoformat(),
                "kernel_version": final_decision.kernel_version,
                "outcome": final_decision.outcome.value,
                "reason": final_decision.reason.value,
                "resulting_state": final_decision.resulting_state.value,
                "resulting_state_version": final_decision.resulting_state_version,
                "transition_decision_id": final_decision.transition_decision_id,
                "transition_evaluation_id": final_decision.transition_evaluation_id,
                "transition_request_id": final_decision.transition_request_id,
            }
        )
        pointer_fingerprint = memory_content_fingerprint(
            category=MemoryCategory.PROVENANCE_POINTER,
            authority_mode=MemoryAuthorityMode.DETERMINISTIC_POINTER,
            policy_ref=memory_policy.serialized_ref,
            normalized_derived_content={
                "provenance_role": "terminal-transition",
                "source_fingerprint": transition_fingerprint,
                "source_logical_id": final_decision.transition_decision_id,
                "source_object_kind": "P1_4_TRANSITION_DECISION",
                "source_ref": final_decision.transition_decision_id,
            },
        )
        cycle_candidate = CycleCandidate(
            f"cycle-{label}",
            "v1",
            "aiscc-project",
            task_id,
            "v1",
            p1_8_task_binding_fingerprint(
                project_id="aiscc-project",
                task_contract_id=task_id,
                task_contract_version="v1",
            ),
            run_id,
            5,
            accept_request.transition_request_id,
            final_decision.transition_decision_id,
            transition_fingerprint,
            corrected_judgment.serialized_ref,
            corrected_judgment.fingerprint,
            post_attestation.serialized_ref,
            post_attestation.admitted_ref_root_hash,
            (
                MemoryDeclaration(
                    MemoryCategory.PROVENANCE_POINTER,
                    final_decision.transition_decision_id,
                    "project:aiscc-project",
                    "provenance/terminal-transition/p1_4_transition_decision/"
                    + final_decision.transition_decision_id,
                    memory_policy.serialized_ref,
                    memory_policy.fingerprint,
                    pointer_fingerprint,
                    pointer_ref=final_decision.transition_decision_id,
                ),
            ),
            task_constraint.constraint_ref,
            task_constraint.constraint_fingerprint,
            task_constraint_snapshot.snapshot_ref,
            task_constraint_snapshot.snapshot_fingerprint,
            task_constraint_snapshot.owner_event_high_watermark,
        )
        cycle_request = CycleAdmissionRequest(
            f"cycle-request-{label}", "v1", cycle_candidate, "aiscc-system", NOW
        )
        cycle_repository = PostgresCycleAdmissionRepository(
            sessions,
            evidence_repository,
            historical_content_access_grant=(
                historical_content_access.issue_p1_8_structured_result_grant()
            ),
            memory_policy=memory_policy,
            memory_policy_authority=memory_policy_authority,
            task_authority_verifier=external_task_repository,
        )
        await cycle_repository.enroll_memory_policy()
        restarted_cycle_repository = PostgresCycleAdmissionRepository(
            sessions,
            evidence_repository,
            historical_content_access_grant=(
                historical_content_access.issue_p1_8_structured_result_grant()
            ),
            memory_policy=memory_policy,
            memory_policy_authority=memory_policy_authority,
            task_authority_verifier=external_task_repository,
        )
        alternate_request = replace(
            cycle_request,
            request_id=f"cycle-request-alternate-{label}",
            candidate=replace(cycle_candidate, cycle_id=f"cycle-alternate-{label}"),
        )
        concurrent_cycles = await asyncio.gather(
            cycle_repository.admit(cycle_request),
            restarted_cycle_repository.admit(alternate_request),
        )
        admitted_cycle = concurrent_cycles[0]
        assert concurrent_cycles == [admitted_cycle, admitted_cycle]
        assert admitted_cycle.cycle_id in {
            cycle_candidate.cycle_id,
            alternate_request.candidate.cycle_id,
        }
        with pytest.raises(CycleAdmissionError) as terminal_conflict:
            await cycle_repository.admit(
                replace(
                    alternate_request,
                    request_id=f"cycle-request-conflict-{label}",
                    candidate=replace(
                        alternate_request.candidate,
                        cycle_id=f"cycle-conflict-{label}",
                        memory_declarations=(
                            replace(
                                alternate_request.candidate.memory_declarations[0],
                                claimed_content_fingerprint="0" * 64,
                            ),
                        ),
                    ),
                )
            )
        assert terminal_conflict.value.code is CycleAdmissionErrorCode.TERMINAL_EPOCH_CONFLICT
        assert await restarted_cycle_repository.replay(admitted_cycle.cycle_id) == admitted_cycle
        async with sessions() as session:
            current_memory_entry_id = await session.scalar(
                select(ProjectMemoryViewRow.current_entry_id).where(
                    ProjectMemoryViewRow.project_id == "aiscc-project",
                    ProjectMemoryViewRow.state == "CURRENT",
                )
            )
        assert isinstance(current_memory_entry_id, str)
        next_action_authority = default_next_action_policy_authority()
        eligibility, selection_policy, descriptors = next_action_authority.issue_policy_catalog_v1(
            now=NOW
        )
        next_action_repository = PostgresNextActionRepository(
            sessions,
            eligibility_policy=eligibility,
            selection_policy=selection_policy,
            descriptors=descriptors,
            policy_authority=next_action_authority,
            task_authority_verifier=external_task_repository,
        )
        await next_action_repository.enroll_configured_authority(NOW)
        assert descriptors[0].action_ref.action_id == "open-operational-recovery-task-issuance"
        assert await restarted_cycle_repository.replay(admitted_cycle.cycle_id) == admitted_cycle
        async with sessions() as session, session.begin():
            await session.execute(text("SET LOCAL session_replication_role = replica"))
            cycle_row = await session.get(AdmittedCycleRow, admitted_cycle.cycle_id)
            assert cycle_row is not None
            cycle_row.cycle_fingerprint = "f" * 64
        with pytest.raises(CycleAdmissionError):
            await restarted_cycle_repository.replay(admitted_cycle.cycle_id)
        async with sessions() as session, session.begin():
            await session.execute(text("SET LOCAL session_replication_role = replica"))
            cycle_row = await session.get(AdmittedCycleRow, admitted_cycle.cycle_id)
            assert cycle_row is not None
            cycle_row.cycle_fingerprint = admitted_cycle.cycle_fingerprint

        # Restart reconstructs durable Human/producer/Judgment authority; no process cache is truth.
        restarted_human = PostgresHumanAuthorityRepository(sessions)
        assert await restarted_human.load_result(result.serialized_ref) == result
        assert await restarted_human.load_producer_ref(producer.serialized_ref) == producer
        assert len(await restarted_human.verify_consistency(run_id)) == 1
        restarted_judgment = PostgresJudgmentAuthority(
            sessions, evidence_repository, judgment_policy_authority
        )
        assert (await restarted_judgment.verify_consistency(run_id)) == corrected_judgment
        restarted_issuer = P1_7HumanEvidenceIssuerAuthority(restarted_human)
        restarted_candidate = await restarted_issuer.seed_candidate(
            replace(candidate, candidate_fingerprint="", _issuer_token=None)
        )
        assert await restarted_issuer.recognizes(restarted_candidate)
        assert human_guard.semantic_owner is GuardSemanticOwner.P1_7_HUMAN
        assert judgment_authority.semantic_owner is GuardSemanticOwner.P1_7_JUDGMENT

        # Gate-open and a competing WorkRun transition share the run advisory/row lock.
        gate_race_run_id = f"run-p1-7-gate-open-race-{uuid4()}"
        for source, version, target in (
            (None, 0, WorkflowState.READY),
            (WorkflowState.READY, 1, WorkflowState.RUNNING),
            (WorkflowState.RUNNING, 2, WorkflowState.ADMISSION_PENDING),
        ):
            step = request(task_id, gate_race_run_id, source, version, target)
            assert (
                await kernel.request_transition(step, system_facts(system, step))
            ).outcome is DecisionOutcome.ADMITTED
        _, gate_race_pre = await evidence_repository.evaluate_set(
            work_run_id=gate_race_run_id,
            checkpoint_ref=pre.ref,
            observed_state=WorkflowState.ADMISSION_PENDING,
            observed_state_version=3,
            authority_id="AISCC_P1_6_EVIDENCE_AUTHORITY_V1",
            authority_version="AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
            now=NOW,
        )
        assert gate_race_pre is not None
        gate_race_open = request(
            task_id,
            gate_race_run_id,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.HUMAN_REQUIRED,
        )
        gate_race_reservation = reservation_authority.reserve(
            gate_race_open,
            designated_principal_selector_fingerprint="reviewers-v1",
        )
        gate_race_block = request(
            task_id,
            gate_race_run_id,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.BLOCKED,
        )
        gate_race_decisions = await asyncio.gather(
            kernel.request_transition(
                gate_race_open,
                (),
                transaction_participant=await human_guard.gate_open_participant(
                    gate_race_open,
                    gate_race_reservation,
                    gate_race_pre.serialized_ref,
                ),
            ),
            kernel.request_transition(
                gate_race_block,
                system_facts(system, gate_race_block),
            ),
        )
        assert (
            sum(decision.outcome is DecisionOutcome.ADMITTED for decision in gate_race_decisions)
            == 1
        )
        assert (
            sum(decision.outcome is DecisionOutcome.DENIED for decision in gate_race_decisions) == 1
        )
        gate_race_run = await kernel.verify_consistency(gate_race_run_id)
        gate_race_gate = await human_repository.load_current_gate(gate_race_run_id)
        if gate_race_run.state is WorkflowState.HUMAN_REQUIRED:
            assert gate_race_run.state_version == 4
            assert gate_race_gate is not None and gate_race_gate.bound_state_version == 4
        else:
            assert gate_race_run.state is WorkflowState.BLOCKED
            assert gate_race_run.state_version == 4
            assert gate_race_gate is None

        # A fresh run proves FIRST_DURABLY_ADMITTED under the PostgreSQL row/run locks.
        race_run_id = f"run-p1-7-race-{uuid4()}"
        for source, version, target in (
            (None, 0, WorkflowState.READY),
            (WorkflowState.READY, 1, WorkflowState.RUNNING),
            (WorkflowState.RUNNING, 2, WorkflowState.ADMISSION_PENDING),
        ):
            step = request(task_id, race_run_id, source, version, target)
            assert (
                await kernel.request_transition(step, system_facts(system, step))
            ).outcome is DecisionOutcome.ADMITTED
        _, race_pre_attestation = await evidence_repository.evaluate_set(
            work_run_id=race_run_id,
            checkpoint_ref=pre.ref,
            observed_state=WorkflowState.ADMISSION_PENDING,
            observed_state_version=3,
            authority_id="AISCC_P1_6_EVIDENCE_AUTHORITY_V1",
            authority_version="AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
            now=NOW,
        )
        assert race_pre_attestation is not None
        race_gate_request = request(
            task_id,
            race_run_id,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.HUMAN_REQUIRED,
        )
        race_reservation = reservation_authority.reserve(
            race_gate_request, designated_principal_selector_fingerprint="reviewers-v1"
        )
        race_participant = await human_guard.gate_open_participant(
            race_gate_request, race_reservation, race_pre_attestation.serialized_ref
        )
        assert (
            await kernel.request_transition(
                race_gate_request, (), transaction_participant=race_participant
            )
        ).outcome is DecisionOutcome.ADMITTED
        race_gate = await human_repository.load_gate(
            f"p1-7-gate:{race_reservation.human_gate_version}:{race_reservation.human_gate_id}"
        )
        assert race_gate is not None
        principal_a = principal_authority.authenticate(
            principal_id="reviewer-a",
            session_id="session-a",
            role_refs=("reviewer",),
        )
        principal_b = principal_authority.authenticate(
            principal_id="reviewer-b",
            session_id="session-b",
            role_refs=("reviewer",),
        )
        action_a = await principal_authority.issue_action_authority(
            principal_a, race_gate.serialized_ref, idempotency_scope="race-a"
        )
        action_b = await principal_authority.issue_action_authority(
            principal_b, race_gate.serialized_ref, idempotency_scope="race-b"
        )

        async def submit_race(
            result_id: str,
            principal: Any,
            action: Any,
            kind: HumanResultKind,
        ) -> HumanResult:
            return await human_repository.submit_result(
                human_result_id=result_id,
                human_result_version="v1",
                gate_ref=race_gate.serialized_ref,
                principal=principal,
                action_authority=action,
                result_kind=kind,
                structured_reason_code="CONCURRENT_REVIEW",
                reason_vocabulary_version="v1",
                idempotency_key=result_id,
                submitted_at=NOW,
            )

        race_results = await asyncio.gather(
            submit_race(f"race-result-a-{label}", principal_a, action_a, HumanResultKind.APPROVE),
            submit_race(f"race-result-b-{label}", principal_b, action_b, HumanResultKind.REJECT),
            return_exceptions=True,
        )
        assert sum(isinstance(item, HumanResult) for item in race_results) == 1
        assert sum(isinstance(item, HumanAuthorityError) for item in race_results) == 1
        race_winner = next(item for item in race_results if isinstance(item, HumanResult))
        old_producer = await human_repository.create_producer_ref(
            result_ref=race_winner.serialized_ref,
            checkpoint_ref=post.ref.serialized(),
            evidence_type_id="AISCC_HUMAN_RESULT_REVIEW",
            evidence_type_version="v1",
            subject_id="work-result",
            scope_id="final-review",
            resource_id=None,
            content_hash="b" * 64,
            sensitivity=EvidenceSensitivity.INTERNAL,
            export_policy="PRIVATE_AUTHORITY_ONLY",
        )
        assert await human_repository.load_producer_ref(old_producer.serialized_ref) is not None
        corrected_gate = await human_guard.correct_gate(
            race_gate.serialized_ref,
            designated_principal_selector_fingerprint="reviewers-v2",
        )
        assert corrected_gate.supersedes_gate_ref == race_gate.serialized_ref
        assert await human_repository.load_producer_ref(old_producer.serialized_ref) is None
        winner_principal, winner_action = (
            (principal_a, action_a)
            if race_winner.human_result_id == f"race-result-a-{label}"
            else (principal_b, action_b)
        )
        historical_result_counts = (
            await _row_count(sessions, HumanResultRow),
            await _row_count(sessions, HumanResultAuthorityEventRow),
            await _row_count(sessions, HumanGateAuthorityEventRow),
        )
        historical_human_repository = PostgresHumanAuthorityRepository(sessions)
        assert (
            await historical_human_repository.submit_result(
                human_result_id=race_winner.human_result_id,
                human_result_version="v1",
                gate_ref=race_gate.serialized_ref,
                principal=winner_principal,
                action_authority=winner_action,
                result_kind=race_winner.result_kind,
                structured_reason_code="CONCURRENT_REVIEW",
                reason_vocabulary_version="v1",
                idempotency_key=race_winner.human_result_id,
                submitted_at=NOW,
            )
            == race_winner
        )
        assert (
            await _row_count(sessions, HumanResultRow),
            await _row_count(sessions, HumanResultAuthorityEventRow),
            await _row_count(sessions, HumanGateAuthorityEventRow),
        ) == historical_result_counts

        # A corrected gate stays valid historical authority only through its predecessor graph.
        corrected_action = await principal_authority.issue_action_authority(
            winner_principal,
            corrected_gate.serialized_ref,
            idempotency_scope=f"corrected-result-{label}",
        )
        corrected_result = await human_repository.submit_result(
            human_result_id=f"corrected-result-{label}",
            human_result_version="v1",
            gate_ref=corrected_gate.serialized_ref,
            principal=winner_principal,
            action_authority=corrected_action,
            result_kind=HumanResultKind.APPROVE,
            structured_reason_code="CORRECTED_REVIEW",
            reason_vocabulary_version="v1",
            idempotency_key=f"corrected-result-{label}",
            submitted_at=NOW,
        )

        async def replay_corrected_result() -> HumanResult:
            return await historical_human_repository.submit_result(
                human_result_id=corrected_result.human_result_id,
                human_result_version=corrected_result.human_result_version,
                gate_ref=corrected_result.human_gate_ref,
                principal=winner_principal,
                action_authority=corrected_action,
                result_kind=corrected_result.result_kind,
                structured_reason_code=corrected_result.structured_reason_code,
                reason_vocabulary_version=corrected_result.reason_vocabulary_version,
                idempotency_key=corrected_result.idempotency_key,
                submitted_at=corrected_result.submitted_at,
            )

        correction_counts = (
            await _row_count(sessions, HumanResultRow),
            await _row_count(sessions, HumanResultAuthorityEventRow),
            await _row_count(sessions, HumanGateAuthorityEventRow),
        )
        assert await replay_corrected_result() == corrected_result
        assert (
            await _row_count(sessions, HumanResultRow),
            await _row_count(sessions, HumanResultAuthorityEventRow),
            await _row_count(sessions, HumanGateAuthorityEventRow),
        ) == correction_counts

        async with sessions() as session:
            correction_row = await session.get(HumanGateRow, corrected_gate.human_gate_id)
            correction_opened = await session.scalar(
                select(HumanGateAuthorityEventRow).where(
                    HumanGateAuthorityEventRow.human_gate_id == corrected_gate.human_gate_id,
                    HumanGateAuthorityEventRow.event_kind == "OPENED_CORRECTION",
                )
            )
            predecessor_relation = await session.scalar(
                select(HumanGateAuthorityEventRow).where(
                    HumanGateAuthorityEventRow.human_gate_id == race_gate.human_gate_id,
                    HumanGateAuthorityEventRow.event_kind == "SUPERSEDED",
                )
            )
            assert correction_row is not None
            assert correction_opened is not None
            assert predecessor_relation is not None
            correction_payload = dict(correction_row.payload)
            correction_fingerprint = correction_row.gate_fingerprint
            correction_opened_payload = dict(correction_opened.payload)
            predecessor_relation_payload = dict(predecessor_relation.payload)

        def correction_fingerprint_for(supersedes_ref: str) -> str:
            return canonical_hash(
                {
                    "gate": [corrected_gate.human_gate_id, corrected_gate.human_gate_version],
                    "purpose": [corrected_gate.purpose_id, corrected_gate.purpose_version],
                    "task": [corrected_gate.task_contract_id, corrected_gate.task_contract_version],
                    "run": corrected_gate.work_run_id,
                    "source": [
                        WorkflowState.HUMAN_REQUIRED.value,
                        corrected_gate.bound_state_version,
                    ],
                    "target": WorkflowState.HUMAN_REQUIRED.value,
                    "policy": [
                        corrected_gate.authority_policy_ref,
                        corrected_gate.authority_policy_version,
                    ],
                    "selector": corrected_gate.designated_principal_selector_fingerprint,
                    "supersedes": supersedes_ref,
                }
            )

        async def set_correction_gate(
            supersedes_ref: str,
            *,
            opened_supersedes_ref: str | None = None,
        ) -> None:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                current_row = await session.get(HumanGateRow, corrected_gate.human_gate_id)
                current_event = await session.scalar(
                    select(HumanGateAuthorityEventRow).where(
                        HumanGateAuthorityEventRow.human_gate_id == corrected_gate.human_gate_id,
                        HumanGateAuthorityEventRow.event_kind == "OPENED_CORRECTION",
                    )
                )
                assert current_row is not None and current_event is not None
                current_row.payload = {
                    **current_row.payload,
                    "supersedes_gate_ref": supersedes_ref,
                }
                current_row.gate_fingerprint = correction_fingerprint_for(supersedes_ref)
                current_event.payload = {
                    **current_event.payload,
                    "supersedes_gate_ref": opened_supersedes_ref or supersedes_ref,
                }

        async def restore_correction_graph() -> None:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                current_row = await session.get(HumanGateRow, corrected_gate.human_gate_id)
                current_event = await session.scalar(
                    select(HumanGateAuthorityEventRow).where(
                        HumanGateAuthorityEventRow.human_gate_id == corrected_gate.human_gate_id,
                        HumanGateAuthorityEventRow.event_kind == "OPENED_CORRECTION",
                    )
                )
                relation = await session.scalar(
                    select(HumanGateAuthorityEventRow).where(
                        HumanGateAuthorityEventRow.human_gate_id == race_gate.human_gate_id,
                        HumanGateAuthorityEventRow.event_kind == "SUPERSEDED",
                    )
                )
                assert (
                    current_row is not None and current_event is not None and relation is not None
                )
                current_row.payload = correction_payload
                current_row.gate_fingerprint = correction_fingerprint
                current_event.payload = correction_opened_payload
                relation.payload = predecessor_relation_payload

        try:
            await set_correction_gate(f"p1-7-gate:p1-7-gate-v1:missing-{label}")
            with pytest.raises(HumanAuthorityError, match="PROVENANCE_INCOMPLETE"):
                await replay_corrected_result()
        finally:
            await restore_correction_graph()

        try:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                relation = await session.scalar(
                    select(HumanGateAuthorityEventRow).where(
                        HumanGateAuthorityEventRow.human_gate_id == race_gate.human_gate_id,
                        HumanGateAuthorityEventRow.event_kind == "SUPERSEDED",
                    )
                )
                assert relation is not None
                relation.payload = {"replacement_gate_ref": f"p1-7-gate:wrong:{label}"}
            with pytest.raises(HumanAuthorityError, match="PROVENANCE_INCOMPLETE"):
                await replay_corrected_result()
        finally:
            await restore_correction_graph()

        try:
            await set_correction_gate(corrected_gate.serialized_ref)
            with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                await replay_corrected_result()
        finally:
            await restore_correction_graph()

        unchanged_race_run = await kernel.load(race_run_id)
        assert unchanged_race_run is not None
        assert unchanged_race_run.state is WorkflowState.HUMAN_REQUIRED
        assert unchanged_race_run.state_version == 4
        with pytest.raises(HumanAuthorityError):
            await human_repository.submit_result(
                human_result_id=f"late-after-gate-correction-{label}",
                human_result_version="v1",
                gate_ref=race_gate.serialized_ref,
                principal=principal_a,
                action_authority=action_a,
                result_kind=HumanResultKind.APPROVE,
                structured_reason_code="LATE_REVIEW",
                reason_vocabulary_version="v1",
                idempotency_key=f"late-after-gate-correction-{label}",
                submitted_at=NOW,
            )

        old_target = (
            WorkflowState.ACCEPTED
            if race_winner.result_kind is HumanResultKind.APPROVE
            else WorkflowState.REJECTED
        )
        old_guard_request = request(
            task_id,
            race_run_id,
            WorkflowState.HUMAN_REQUIRED,
            4,
            old_target,
            human_result_refs=(race_winner.serialized_ref,),
        )
        stale_result_policy = await judgment_policy_authority.register(
            policy_id=f"HUMAN_RESULT_RACE_POLICY-{label}",
            policy_version="v1",
            task_contract_id=task_id,
            task_contract_version="v1",
            source_state=WorkflowState.HUMAN_REQUIRED,
            target_state=old_target,
            owner_policy=JudgmentOwnerPolicy.HUMAN,
            requires_human_result=True,
            requires_post_human_evidence=False,
        )
        with pytest.raises(JudgmentAuthorityError):
            await judgment_authority.issue(
                judgment_id=f"late-judgment-{label}",
                judgment_version="v1",
                request=old_guard_request,
                policy=stale_result_policy,
                human_result_ref=race_winner.serialized_ref,
                evidence_attestation_ref=None,
                reason_code="LATE_AFTER_HUMAN_SUPERSESSION",
                reason_vocabulary_version="v1",
            )
        old_guard_id = next(
            guard
            for guard in TRANSITION_MATRIX[(WorkflowState.HUMAN_REQUIRED, old_target)]
            if guard.value in {"G_HUMAN_APPROVED", "G_HUMAN_REJECTED", "G_HUMAN_REWORK"}
        )
        old_result_participant = await human_guard.result_guard_participant(
            old_guard_request, old_guard_id
        )
        assert (
            await kernel.request_transition(
                old_guard_request, (), transaction_participant=old_result_participant
            )
        ).outcome is DecisionOutcome.DENIED

        # Gate suspension/reactivation/cancellation are atomic P1-4 lifecycle participants.
        lifecycle_run_id = f"run-p1-7-lifecycle-{uuid4()}"
        for source, version, target in (
            (None, 0, WorkflowState.READY),
            (WorkflowState.READY, 1, WorkflowState.RUNNING),
            (WorkflowState.RUNNING, 2, WorkflowState.ADMISSION_PENDING),
        ):
            step = request(task_id, lifecycle_run_id, source, version, target)
            assert (
                await kernel.request_transition(step, system_facts(system, step))
            ).outcome is DecisionOutcome.ADMITTED
        _, lifecycle_pre = await evidence_repository.evaluate_set(
            work_run_id=lifecycle_run_id,
            checkpoint_ref=pre.ref,
            observed_state=WorkflowState.ADMISSION_PENDING,
            observed_state_version=3,
            authority_id="AISCC_P1_6_EVIDENCE_AUTHORITY_V1",
            authority_version="AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
            now=NOW,
        )
        assert lifecycle_pre is not None
        lifecycle_open = request(
            task_id,
            lifecycle_run_id,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.HUMAN_REQUIRED,
        )
        lifecycle_reservation = reservation_authority.reserve(
            lifecycle_open, designated_principal_selector_fingerprint="reviewers-v1"
        )
        assert (
            await kernel.request_transition(
                lifecycle_open,
                (),
                transaction_participant=await human_guard.gate_open_participant(
                    lifecycle_open,
                    lifecycle_reservation,
                    lifecycle_pre.serialized_ref,
                ),
            )
        ).outcome is DecisionOutcome.ADMITTED
        lifecycle_gate = await human_repository.load_current_gate(lifecycle_run_id)
        assert lifecycle_gate is not None
        stale_principal = principal_authority.authenticate(
            principal_id="stale-reviewer",
            session_id="stale-session",
            role_refs=("reviewer",),
        )
        stale_action = await principal_authority.issue_action_authority(
            stale_principal,
            lifecycle_gate.serialized_ref,
            idempotency_scope=f"stale-result-{label}",
        )
        block = request(
            task_id,
            lifecycle_run_id,
            WorkflowState.HUMAN_REQUIRED,
            4,
            WorkflowState.BLOCKED,
        )
        assert (
            await kernel.request_transition(
                block,
                system_facts(system, block),
                transaction_participant=human_guard.lifecycle_participant(block),
            )
        ).outcome is DecisionOutcome.ADMITTED
        suspended = await human_repository.load_current_gate(lifecycle_run_id)
        assert suspended is not None
        assert suspended.suspension_status.value == "SUSPENDED"
        assert suspended.bound_state_version == 5
        with pytest.raises(HumanAuthorityError):
            await human_repository.submit_result(
                human_result_id=f"stale-result-{label}",
                human_result_version="v1",
                gate_ref=lifecycle_gate.serialized_ref,
                principal=stale_principal,
                action_authority=stale_action,
                result_kind=HumanResultKind.APPROVE,
                structured_reason_code="STALE_REVIEW",
                reason_vocabulary_version="v1",
                idempotency_key=f"stale-result-{label}",
                submitted_at=NOW,
            )
        resume = request(
            task_id,
            lifecycle_run_id,
            WorkflowState.BLOCKED,
            5,
            WorkflowState.HUMAN_REQUIRED,
            blocker_resolution_claim=await blocker_resolution_claim(
                sessions, lifecycle_run_id
            ),
        )
        suspended_fact = await human_guard.policy_guard_participant(
            resume,
            next(
                guard
                for guard in TRANSITION_MATRIX[
                    (WorkflowState.BLOCKED, WorkflowState.HUMAN_REQUIRED)
                ]
                if guard.value == "G_SUSPENDED_HUMAN_GATE"
            ),
        )
        resumable_fact = await human_guard.policy_guard_participant(
            resume,
            next(
                guard
                for guard in TRANSITION_MATRIX[
                    (WorkflowState.BLOCKED, WorkflowState.HUMAN_REQUIRED)
                ]
                if guard.value == "G_RESUMABLE_HUMAN_GATE"
            ),
        )
        assert (
            await kernel.request_transition(
                resume,
                system_facts(system, resume),
                transaction_participant=CompositeTransitionParticipant(
                    (suspended_fact, resumable_fact)
                ),
            )
        ).outcome is DecisionOutcome.ADMITTED
        resumed = await human_repository.load_current_gate(lifecycle_run_id)
        assert resumed is not None and resumed.suspension_status.value == "ACTIVE"
        block_again = request(
            task_id,
            lifecycle_run_id,
            WorkflowState.HUMAN_REQUIRED,
            6,
            WorkflowState.BLOCKED,
            blocker_kind=BlockerKindV1.SECURITY,
        )
        assert (
            await kernel.request_transition(
                block_again,
                system_facts(system, block_again),
                transaction_participant=human_guard.lifecycle_participant(block_again),
            )
        ).outcome is DecisionOutcome.ADMITTED
        fail = request(
            task_id,
            lifecycle_run_id,
            WorkflowState.BLOCKED,
            7,
            WorkflowState.FAILED,
        )
        assert (
            await kernel.request_transition(
                fail,
                system_facts(system, fail),
                transaction_participant=human_guard.lifecycle_participant(fail),
            )
        ).outcome is DecisionOutcome.ADMITTED
        cancelled = await human_repository.load_current_gate(lifecycle_run_id)
        assert cancelled is not None and cancelled.status.value == "CANCELLED"

        no_gate_run_id = f"run-p1-7-no-gate-{uuid4()}"
        for source, version, target in (
            (None, 0, WorkflowState.READY),
            (WorkflowState.READY, 1, WorkflowState.RUNNING),
            (WorkflowState.RUNNING, 2, WorkflowState.BLOCKED),
        ):
            step = request(task_id, no_gate_run_id, source, version, target)
            assert (
                await kernel.request_transition(step, system_facts(system, step))
            ).outcome is DecisionOutcome.ADMITTED
        ready_again = request(
            task_id,
            no_gate_run_id,
            WorkflowState.BLOCKED,
            3,
            WorkflowState.READY,
            blocker_resolution_claim=await blocker_resolution_claim(sessions, no_gate_run_id),
        )
        no_pending_guard = await human_guard.policy_guard_participant(
            ready_again,
            next(
                guard
                for guard in TRANSITION_MATRIX[(WorkflowState.BLOCKED, WorkflowState.READY)]
                if guard.value == "G_NO_PENDING_HUMAN_GATE"
            ),
        )
        assert (
            await kernel.request_transition(
                ready_again,
                system_facts(system, ready_again),
                transaction_participant=no_pending_guard,
            )
        ).outcome is DecisionOutcome.ADMITTED

        negative_run_id = f"run-p1-7-negative-{uuid4()}"
        for source, version, target in (
            (None, 0, WorkflowState.READY),
            (WorkflowState.READY, 1, WorkflowState.RUNNING),
            (WorkflowState.RUNNING, 2, WorkflowState.ADMISSION_PENDING),
        ):
            step = request(task_id, negative_run_id, source, version, target)
            assert (
                await kernel.request_transition(step, system_facts(system, step))
            ).outcome is DecisionOutcome.ADMITTED
        negative_evaluation, negative_attestation = await evidence_repository.evaluate_set(
            work_run_id=negative_run_id,
            checkpoint_ref=negative_checkpoint.ref,
            observed_state=WorkflowState.ADMISSION_PENDING,
            observed_state_version=3,
            authority_id="AISCC_P1_6_EVIDENCE_AUTHORITY_V1",
            authority_version="AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
            now=NOW,
        )
        assert negative_evaluation.outcome is EvidenceSetOutcome.UNSATISFIED
        assert negative_attestation is None
        negative_request = request(
            task_id,
            negative_run_id,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.REWORK_REQUIRED,
            evidence_refs=(negative_evaluation.serialized_ref,),
        )
        with pytest.raises(
            ValueError, match="negative .*basis requires deterministic rework policy"
        ):
            await judgment_policy_authority.register(
                policy_id=f"INVALID_NEGATIVE_POLICY-{label}",
                policy_version="v2",
                task_contract_id=task_id,
                task_contract_version="v1",
                source_state=WorkflowState.ADMISSION_PENDING,
                target_state=WorkflowState.ACCEPTED,
                owner_policy=JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC,
                requires_human_result=False,
                requires_post_human_evidence=False,
                deterministic_kind=JudgmentKind.HOLD_REWORK_REQUIRED,
                evidence_basis_kind=(
                    JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION
                ),
                evidence_checkpoint_ref=negative_checkpoint.ref.serialized(),
                evidence_requirement_set_ref=(
                    f"{requirement_set.requirement_set_id}"
                    f"@{requirement_set.requirement_set_version}"
                ),
            )
        async def register_negative_policy(
            suffix: str, checkpoint_ref: str, requirement_set_ref: str
        ) -> JudgmentPolicy:
            return await judgment_policy_authority.register(
                policy_id=f"SYSTEM_REWORK_POLICY-{suffix}-{label}",
                policy_version="v2",
                task_contract_id=task_id,
                task_contract_version="v1",
                source_state=WorkflowState.ADMISSION_PENDING,
                target_state=WorkflowState.REWORK_REQUIRED,
                owner_policy=JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC,
                requires_human_result=False,
                requires_post_human_evidence=False,
                deterministic_kind=JudgmentKind.HOLD_REWORK_REQUIRED,
                evidence_basis_kind=(
                    JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION
                ),
                evidence_checkpoint_ref=checkpoint_ref,
                evidence_requirement_set_ref=requirement_set_ref,
            )

        requirement_set_ref = (
            f"{requirement_set.requirement_set_id}@{requirement_set.requirement_set_version}"
        )
        wrong_checkpoint_policy = await register_negative_policy(
            "wrong-checkpoint", "wrong-checkpoint@v1", requirement_set_ref
        )
        with pytest.raises(JudgmentAuthorityError):
            await judgment_authority.issue(
                judgment_id=f"negative-wrong-checkpoint-{label}",
                judgment_version="v2",
                request=negative_request,
                policy=wrong_checkpoint_policy,
                human_result_ref=None,
                evidence_attestation_ref=None,
                reason_code="REQUIRED_EVIDENCE_UNSATISFIED",
                reason_vocabulary_version="v2",
                evidence_basis_kind=(
                    JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION
                ),
                evidence_evaluation_ref=negative_evaluation.serialized_ref,
            )
        wrong_set_policy = await register_negative_policy(
            "wrong-set", negative_checkpoint.ref.serialized(), "wrong-set@v1"
        )
        with pytest.raises(JudgmentAuthorityError):
            await judgment_authority.issue(
                judgment_id=f"negative-wrong-set-{label}",
                judgment_version="v2",
                request=negative_request,
                policy=wrong_set_policy,
                human_result_ref=None,
                evidence_attestation_ref=None,
                reason_code="REQUIRED_EVIDENCE_UNSATISFIED",
                reason_vocabulary_version="v2",
                evidence_basis_kind=(
                    JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION
                ),
                evidence_evaluation_ref=negative_evaluation.serialized_ref,
            )
        negative_policy = await register_negative_policy(
            "current", negative_checkpoint.ref.serialized(), requirement_set_ref
        )

        async def denied_negative(
            suffix: str,
            *,
            evaluation_ref: str | None,
            attestation_ref: str | None = None,
            candidate_request: TransitionRequest = negative_request,
        ) -> None:
            with pytest.raises(JudgmentAuthorityError):
                await judgment_authority.issue(
                    judgment_id=f"negative-denied-{suffix}-{label}",
                    judgment_version="v2",
                    request=candidate_request,
                    policy=negative_policy,
                    human_result_ref=None,
                    evidence_attestation_ref=attestation_ref,
                    reason_code="REQUIRED_EVIDENCE_UNSATISFIED",
                    reason_vocabulary_version="v2",
                    evidence_basis_kind=(
                        JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION
                    ),
                    evidence_evaluation_ref=evaluation_ref,
                )

        await denied_negative("missing", evaluation_ref=None)
        await denied_negative(
            "positive-in-negative-slot",
            evaluation_ref=post_attestation.serialized_ref,
        )
        await denied_negative(
            "both",
            evaluation_ref=negative_evaluation.serialized_ref,
            attestation_ref=post_attestation.serialized_ref,
        )
        fabricated_ref = EvidenceSetEvaluationRef(
            negative_evaluation.evaluation_version,
            "evidence-set-evaluation-" + "0" * 64,
        ).serialized()
        await denied_negative("fabricated", evaluation_ref=fabricated_ref)
        await denied_negative(
            "wrong-run",
            evaluation_ref=negative_evaluation.serialized_ref,
            candidate_request=replace(negative_request, work_run_id="wrong-run"),
        )
        await denied_negative(
            "wrong-state",
            evaluation_ref=negative_evaluation.serialized_ref,
            candidate_request=replace(negative_request, observed_state=WorkflowState.RUNNING),
        )
        await denied_negative(
            "wrong-version",
            evaluation_ref=negative_evaluation.serialized_ref,
            candidate_request=replace(negative_request, observed_state_version=4),
        )

        stale_run_id = f"run-p1-7-negative-stale-{uuid4()}"
        for source, version, target in (
            (None, 0, WorkflowState.READY),
            (WorkflowState.READY, 1, WorkflowState.RUNNING),
            (WorkflowState.RUNNING, 2, WorkflowState.ADMISSION_PENDING),
        ):
            step = request(task_id, stale_run_id, source, version, target)
            assert (
                await kernel.request_transition(step, system_facts(system, step))
            ).outcome is DecisionOutcome.ADMITTED
        stale_evaluation, stale_attestation = await evidence_repository.evaluate_set(
            work_run_id=stale_run_id,
            checkpoint_ref=negative_checkpoint.ref,
            observed_state=WorkflowState.ADMISSION_PENDING,
            observed_state_version=3,
            authority_id="AISCC_P1_6_EVIDENCE_AUTHORITY_V1",
            authority_version="AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
            now=NOW,
        )
        assert stale_evaluation.outcome is EvidenceSetOutcome.UNSATISFIED
        assert stale_attestation is None
        stale_request = request(
            task_id,
            stale_run_id,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.REWORK_REQUIRED,
            evidence_refs=(stale_evaluation.serialized_ref,),
        )
        stale_judgment = await judgment_authority.issue(
            judgment_id=f"negative-stale-judgment-{label}",
            judgment_version="v2",
            request=stale_request,
            policy=negative_policy,
            human_result_ref=None,
            evidence_attestation_ref=None,
            reason_code="REQUIRED_EVIDENCE_UNSATISFIED",
            reason_vocabulary_version="v2",
            evidence_basis_kind=JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION,
            evidence_evaluation_ref=stale_evaluation.serialized_ref,
        )
        stale_request = replace(
            stale_request, judgment_refs=(stale_judgment.serialized_ref,)
        )
        stale_human = await human_guard.policy_guard_participant(
            stale_request, GuardId.G_HUMAN_NOT_REQUIRED
        )
        stale_participant = await judgment_authority.participant(
            stale_request, stale_judgment.serialized_ref
        )
        block_stale = request(
            task_id,
            stale_run_id,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.BLOCKED,
        )
        assert (
            await kernel.request_transition(
                block_stale, system_facts(system, block_stale)
            )
        ).outcome is DecisionOutcome.ADMITTED
        stale_decision = await kernel.request_transition(
            stale_request,
            (),
            transaction_participant=CompositeTransitionParticipant(
                (stale_human, stale_participant)
            ),
        )
        assert stale_decision.outcome is DecisionOutcome.DENIED
        assert stale_decision.reason is DecisionReason.STALE_REQUEST
        assert not stale_participant._prepared
        with pytest.raises(JudgmentAuthorityError, match="JUDGMENT_STALE"):
            await judgment_authority.issue(
                judgment_id=f"negative-stale-reissue-{label}",
                judgment_version="v2",
                request=replace(stale_request, judgment_refs=()),
                policy=negative_policy,
                human_result_ref=None,
                evidence_attestation_ref=None,
                reason_code="REQUIRED_EVIDENCE_UNSATISFIED",
                reason_vocabulary_version="v2",
                evidence_basis_kind=(
                    JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION
                ),
                evidence_evaluation_ref=stale_evaluation.serialized_ref,
            )

        negative_judgment = await judgment_authority.issue(
            judgment_id=f"negative-judgment-{label}",
            judgment_version="v2",
            request=negative_request,
            policy=negative_policy,
            human_result_ref=None,
            evidence_attestation_ref=None,
            reason_code="REQUIRED_EVIDENCE_UNSATISFIED",
            reason_vocabulary_version="v2",
            evidence_basis_kind=JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION,
            evidence_evaluation_ref=negative_evaluation.serialized_ref,
        )
        assert negative_judgment.evidence_attestation_ref is None
        assert negative_judgment.evidence_evaluation_ref == negative_evaluation.serialized_ref
        assert (
            negative_judgment.evidence_evaluation_authority_revision
            == negative_evaluation.evidence_authority_revision
        )
        async with sessions() as session:
            negative_row = await session.get(JudgmentRow, negative_judgment.judgment_id)
            assert negative_row is not None
            assert _judgment_from_row(negative_row) == negative_judgment
            assert (
                await _verify_judgment_historical_provenance_in_session(
                    session, negative_row
                )
                == negative_judgment
            )
        negative_request = replace(
            negative_request, judgment_refs=(negative_judgment.serialized_ref,)
        )
        negative_human = await human_guard.policy_guard_participant(
            negative_request, GuardId.G_HUMAN_NOT_REQUIRED
        )
        negative_judgment_participant = await judgment_authority.participant(
            negative_request, negative_judgment.serialized_ref
        )
        denied_negative_decision = await kernel.request_transition(
            negative_request,
            (),
            transaction_participant=CompositeTransitionParticipant(
                (negative_human, negative_judgment_participant)
            ),
        )
        assert denied_negative_decision.outcome is DecisionOutcome.DENIED
        assert denied_negative_decision.reason is DecisionReason.MISSING_GUARD
        assert denied_negative_decision.resulting_state is WorkflowState.ADMISSION_PENDING
        assert denied_negative_decision.resulting_state_version == 3
        async with sessions() as session:
            denied_negative_evaluation = await session.scalar(
                select(TransitionEvaluationRow).where(
                    TransitionEvaluationRow.transition_request_id
                    == negative_request.transition_request_id
                )
            )
            assert denied_negative_evaluation is not None
            assert denied_negative_evaluation.missing_guards == [
                GuardId.G_REWORK_SPEC.value
            ]
            denied_guards = {
                GuardId(str(item["guard_id"])): item
                for item in denied_negative_evaluation.guards
            }
            assert denied_guards[GuardId.G_CURRENT]["satisfied"] is True
            assert denied_guards[GuardId.G_HUMAN_NOT_REQUIRED]["satisfied"] is True
            assert denied_guards[GuardId.G_JUDGMENT_REWORK]["satisfied"] is True
            assert denied_guards[GuardId.G_REWORK_SPEC]["satisfied"] is False

        negative_run_after_denial = await kernel.load(negative_run_id)
        assert negative_run_after_denial is not None
        assert negative_run_after_denial.state is WorkflowState.ADMISSION_PENDING
        assert negative_run_after_denial.state_version == 3

        corrected_negative_request = replace(
            negative_request, transition_request_id=str(uuid4())
        )
        assert (
            corrected_negative_request.transition_request_id
            != negative_request.transition_request_id
        )
        corrected_negative_human = await human_guard.policy_guard_participant(
            corrected_negative_request, GuardId.G_HUMAN_NOT_REQUIRED
        )
        corrected_negative_judgment_participant = await judgment_authority.participant(
            corrected_negative_request, negative_judgment.serialized_ref
        )
        corrected_negative_decision = await kernel.request_transition(
            corrected_negative_request,
            system_facts(system, corrected_negative_request),
            transaction_participant=CompositeTransitionParticipant(
                (corrected_negative_human, corrected_negative_judgment_participant)
            ),
        )
        assert corrected_negative_decision.outcome is DecisionOutcome.ADMITTED
        assert corrected_negative_decision.resulting_state is WorkflowState.REWORK_REQUIRED
        assert corrected_negative_decision.resulting_state_version == 4
        async with sessions() as session:
            corrected_negative_evaluation = await session.scalar(
                select(TransitionEvaluationRow).where(
                    TransitionEvaluationRow.transition_request_id
                    == corrected_negative_request.transition_request_id
                )
            )
            assert corrected_negative_evaluation is not None
            assert corrected_negative_evaluation.missing_guards == []
            corrected_guards = {
                GuardId(str(item["guard_id"])): item
                for item in corrected_negative_evaluation.guards
            }
            for guard_id in (
                GuardId.G_CURRENT,
                GuardId.G_HUMAN_NOT_REQUIRED,
                GuardId.G_JUDGMENT_REWORK,
                GuardId.G_REWORK_SPEC,
            ):
                assert corrected_guards[guard_id]["satisfied"] is True

        no_human_run_id = f"run-p1-7-not-required-{uuid4()}"
        for source, version, target in (
            (None, 0, WorkflowState.READY),
            (WorkflowState.READY, 1, WorkflowState.RUNNING),
            (WorkflowState.RUNNING, 2, WorkflowState.ADMISSION_PENDING),
        ):
            step = request(task_id, no_human_run_id, source, version, target)
            assert (
                await kernel.request_transition(step, system_facts(system, step))
            ).outcome is DecisionOutcome.ADMITTED
        deterministic_request = request(
            task_id,
            no_human_run_id,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.REJECTED,
        )
        deterministic_policy = await judgment_policy_authority.register(
            policy_id=f"SYSTEM_REJECT_POLICY-{label}",
            policy_version="v1",
            task_contract_id=task_id,
            task_contract_version="v1",
            source_state=WorkflowState.ADMISSION_PENDING,
            target_state=WorkflowState.REJECTED,
            owner_policy=JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC,
            requires_human_result=False,
            requires_post_human_evidence=False,
            deterministic_kind=JudgmentKind.REJECTED,
        )
        deterministic_judgment = await judgment_authority.issue(
            judgment_id=f"deterministic-judgment-{label}",
            judgment_version="v1",
            request=deterministic_request,
            policy=deterministic_policy,
            human_result_ref=None,
            evidence_attestation_ref=None,
            reason_code="SYSTEM_POLICY_REJECTED",
            reason_vocabulary_version="v1",
        )
        deterministic_request = replace(
            deterministic_request,
            judgment_refs=(deterministic_judgment.serialized_ref,),
        )
        not_required_participant = await human_guard.policy_guard_participant(
            deterministic_request,
            next(
                guard
                for guard in TRANSITION_MATRIX[
                    (WorkflowState.ADMISSION_PENDING, WorkflowState.REJECTED)
                ]
                if guard.value == "G_HUMAN_NOT_REQUIRED"
            ),
        )
        deterministic_judgment_participant = await judgment_authority.participant(
            deterministic_request, deterministic_judgment.serialized_ref
        )
        assert (
            await kernel.request_transition(
                deterministic_request,
                (),
                transaction_participant=CompositeTransitionParticipant(
                    (not_required_participant, deterministic_judgment_participant)
                ),
            )
        ).outcome is DecisionOutcome.ADMITTED
        await evidence_repository.revoke(
            subject_ref=post_admitted_ref,
            reason="HISTORICAL_JUDGMENT_CURRENT_EFFECTIVENESS_SEPARATION",
            owner_id="AISCC_P1_6_EVIDENCE_AUTHORITY_V1",
            authority_version="AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
        )
        assert (
            await historical_judgment_authority.issue(
                judgment_id=f"judgment-{label}",
                judgment_version="v1",
                request=replace(accept_request, judgment_refs=()),
                policy=policy,
                human_result_ref=result.serialized_ref,
                evidence_attestation_ref=post_attestation.serialized_ref,
                reason_code="CURRENT_INPUTS_ACCEPTED",
                reason_vocabulary_version="v1",
            )
            == judgment
        )
        assert len(await human_repository.verify_consistency(lifecycle_run_id)) == 1
        async with sessions() as session, session.begin():
            corrupt_projection = await session.scalar(
                select(HumanGateProjectionRow).where(
                    HumanGateProjectionRow.work_run_id == lifecycle_run_id
                )
            )
            assert corrupt_projection is not None
            corrupt_projection.authority_revision += 10
        with pytest.raises(HumanAuthorityError):
            await human_repository.verify_consistency(lifecycle_run_id)
        with pytest.raises(HumanAuthorityError):
            await human_repository.verify_consistency(lifecycle_run_id)
        await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_p1_7_cross_scope_policy_idempotency_and_expiry_rework(
    database_url: str,
) -> None:
    async def scenario() -> None:
        label = uuid4().hex
        task_a = f"task-p1-7-authority-a-{label}"
        task_b = f"task-p1-7-authority-b-{label}"
        clock_value = [NOW]
        clock_calls = [0]

        def clock() -> datetime:
            clock_calls[0] += 1
            return clock_value[0]

        engine = create_engine(database_url)
        sessions = create_session_factory(engine)
        evidence_repository = PostgresEvidenceRepository(sessions)
        snapshots = {task_id: evidence_authority_snapshot(task_id) for task_id in (task_a, task_b)}
        for owner, requirement_set, requirements, checkpoints in snapshots.values():
            await evidence_repository.register_authority(
                requirement_set=requirement_set,
                requirements=requirements,
                checkpoints=checkpoints,
                authority=owner,
            )
        all_checkpoints = tuple(
            checkpoint for snapshot in snapshots.values() for checkpoint in snapshot[3]
        )
        required_uses = frozenset(
            {
                (
                    task_id,
                    "v1",
                    WorkflowState.ADMISSION_PENDING,
                    WorkflowState.HUMAN_REQUIRED,
                )
                for task_id in (task_a, task_b)
            }
        )
        human_repository = PostgresHumanAuthorityRepository(sessions, clock=clock)
        reservation_authority = HumanGateReservationAuthority(required_uses)
        checkpoint_uses = EvidenceCheckpointUseRegistry(all_checkpoints)
        human_guard = HumanGuardAuthority(
            sessions,
            human_repository,
            evidence_repository,
            checkpoint_uses,
            reservation_authority,
            clock=clock,
        )
        evidence_guard = EvidenceGuardAuthority(evidence_repository, checkpoint_uses)
        policy_authority = JudgmentPolicyAuthority(sessions, clock=clock)
        command_center = CommandCenterAuthority(sessions, policy_authority, clock=clock)
        judgment_authority = PostgresJudgmentAuthority(
            sessions,
            evidence_repository,
            policy_authority,
            command_center_authority=command_center,
            clock=clock,
        )
        system = P1_4GuardAuthority()
        repository = PostgresTransitionRepository(
            sessions,
            TransitionEvaluator(system, (evidence_guard, human_guard, judgment_authority)),
            TestBlockerSourceVerifier(),
        )
        kernel = WorkflowKernel(repository)

        async def advance_to_admission(task_id: str, run_id: str) -> None:
            for source, version, target in (
                (None, 0, WorkflowState.READY),
                (WorkflowState.READY, 1, WorkflowState.RUNNING),
                (WorkflowState.RUNNING, 2, WorkflowState.ADMISSION_PENDING),
            ):
                step = request(task_id, run_id, source, version, target)
                assert (
                    await kernel.request_transition(step, system_facts(system, step))
                ).outcome is DecisionOutcome.ADMITTED

        async def pre_human(task_id: str, run_id: str) -> Any:
            checkpoint = snapshots[task_id][3][0]
            _, attestation = await evidence_repository.evaluate_set(
                work_run_id=run_id,
                checkpoint_ref=checkpoint.ref,
                observed_state=WorkflowState.ADMISSION_PENDING,
                observed_state_version=3,
                authority_id="AISCC_P1_6_EVIDENCE_AUTHORITY_V1",
                authority_version="AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
                now=clock(),
            )
            assert attestation is not None
            return attestation

        async def open_gate(
            task_id: str,
            run_id: str,
            *,
            expires_at: datetime | None = None,
        ) -> tuple[TransitionRequest, Any, HumanGate]:
            gate_request = request(
                task_id,
                run_id,
                WorkflowState.ADMISSION_PENDING,
                3,
                WorkflowState.HUMAN_REQUIRED,
            )
            reservation = reservation_authority.reserve(
                gate_request,
                designated_principal_selector_fingerprint="reviewers-v1",
                expires_at=expires_at,
            )
            attestation = await pre_human(task_id, run_id)
            participant = await human_guard.gate_open_participant(
                gate_request, reservation, attestation.serialized_ref
            )
            assert (
                await kernel.request_transition(
                    gate_request, (), transaction_participant=participant
                )
            ).outcome is DecisionOutcome.ADMITTED
            gate = await human_repository.load_gate(
                f"p1-7-gate:{reservation.human_gate_version}:{reservation.human_gate_id}"
            )
            assert gate is not None
            return gate_request, reservation, gate

        principal_authority = HumanPrincipalAuthority(human_repository, clock=clock)
        principal = principal_authority.authenticate(
            principal_id=f"reviewer-{label}",
            session_id=f"session-{label}",
            role_refs=("reviewer",),
            ttl_seconds=3600,
        )

        # Foreign reservation A cannot consume PRE_HUMAN truth or mutate WorkRun B.
        run_a = f"run-p1-7-authority-a-{uuid4()}"
        run_b = f"run-p1-7-authority-b-{uuid4()}"
        await advance_to_admission(task_a, run_a)
        await advance_to_admission(task_a, run_b)
        request_a = request(
            task_a,
            run_a,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.HUMAN_REQUIRED,
        )
        reservation_a = reservation_authority.reserve(
            request_a, designated_principal_selector_fingerprint="reviewers-v1"
        )
        request_b = request(
            task_a,
            run_b,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.HUMAN_REQUIRED,
        )
        pre_b = await pre_human(task_a, run_b)
        foreign_reservation = await human_guard.gate_open_participant(
            request_b, reservation_a, pre_b.serialized_ref
        )
        assert (
            await kernel.request_transition(
                request_b, (), transaction_participant=foreign_reservation
            )
        ).outcome is DecisionOutcome.DENIED
        assert await human_repository.load_current_gate(run_a) is None
        assert await human_repository.load_current_gate(run_b) is None
        assert (await kernel.load(run_b)).state is WorkflowState.ADMISSION_PENDING  # type: ignore[union-attr]

        _, _, gate_a = await open_gate(task_a, run_a)
        _, _, gate_b = await open_gate(task_a, run_b)
        action_a = await principal_authority.issue_action_authority(
            principal, gate_a.serialized_ref, idempotency_scope=f"result-a-{label}"
        )
        result_a = await human_repository.submit_result(
            human_result_id=f"result-a-{label}",
            human_result_version="v1",
            gate_ref=gate_a.serialized_ref,
            principal=principal,
            action_authority=action_a,
            result_kind=HumanResultKind.APPROVE,
            structured_reason_code="APPROVED_A",
            reason_vocabulary_version="v1",
            idempotency_key=f"result-a-{label}",
        )

        # Foreign result A cannot activate a Human guard or Judgment for run B.
        accept_b_foreign = request(
            task_a,
            run_b,
            WorkflowState.HUMAN_REQUIRED,
            4,
            WorkflowState.ACCEPTED,
            human_result_refs=(result_a.serialized_ref,),
        )
        human_rows_before = await _row_count(sessions, HumanGuardAttestationRow)
        foreign_result_participant = await human_guard.result_guard_participant(
            accept_b_foreign, GuardId.G_HUMAN_APPROVED
        )
        assert (
            await kernel.request_transition(
                accept_b_foreign, (), transaction_participant=foreign_result_participant
            )
        ).outcome is DecisionOutcome.DENIED
        assert await _row_count(sessions, HumanGuardAttestationRow) == human_rows_before
        human_policy = await policy_authority.register(
            policy_id=f"HUMAN_ACCEPT-{label}",
            policy_version="v1",
            task_contract_id=task_a,
            task_contract_version="v1",
            source_state=WorkflowState.HUMAN_REQUIRED,
            target_state=WorkflowState.ACCEPTED,
            owner_policy=JudgmentOwnerPolicy.HUMAN,
            requires_human_result=True,
            requires_post_human_evidence=False,
        )
        judgment_rows_before = await _row_count(sessions, JudgmentRow)
        evaluation_rows_before = await _row_count(sessions, JudgmentEvaluationRow)
        with pytest.raises(JudgmentAuthorityError):
            await judgment_authority.issue(
                judgment_id=f"foreign-judgment-{label}",
                judgment_version="v1",
                request=accept_b_foreign,
                policy=human_policy,
                human_result_ref=result_a.serialized_ref,
                evidence_attestation_ref=None,
                reason_code="FOREIGN_RESULT",
                reason_vocabulary_version="v1",
            )
        assert await _row_count(sessions, JudgmentRow) == judgment_rows_before
        assert await _row_count(sessions, JudgmentEvaluationRow) == evaluation_rows_before

        # Action authority consumes the durable ref, never a caller-built HumanGate object.
        fake_gate = replace(gate_b, work_run_id=run_a, bound_state_version=999)
        with pytest.raises(HumanAuthorityError):
            await principal_authority.issue_action_authority(
                principal,
                fake_gate,
                idempotency_scope="fake-gate",  # type: ignore[arg-type]
            )
        with pytest.raises(HumanAuthorityError):
            await principal_authority.issue_action_authority(
                principal,
                "p1-7-gate:p1-7-gate-v1:caller-created",
                idempotency_scope="unknown-gate",
            )

        action_b = await principal_authority.issue_action_authority(
            principal, gate_b.serialized_ref, idempotency_scope=f"result-b-{label}"
        )
        result_b = await human_repository.submit_result(
            human_result_id=f"result-b-{label}",
            human_result_version="v1",
            gate_ref=gate_b.serialized_ref,
            principal=principal,
            action_authority=action_b,
            result_kind=HumanResultKind.APPROVE,
            structured_reason_code="APPROVED_B",
            reason_vocabulary_version="v1",
            idempotency_key=f"result-b-{label}",
        )
        human_judgment_request = request(
            task_a,
            run_b,
            WorkflowState.HUMAN_REQUIRED,
            4,
            WorkflowState.ACCEPTED,
            human_result_refs=(result_b.serialized_ref,),
        )
        human_judgment = await judgment_authority.issue(
            judgment_id=f"human-judgment-{label}",
            judgment_version="v1",
            request=human_judgment_request,
            policy=human_policy,
            human_result_ref=result_b.serialized_ref,
            evidence_attestation_ref=None,
            reason_code="HUMAN_APPROVED_B",
            reason_vocabulary_version="v1",
        )
        wrong_target = request(
            task_a,
            run_b,
            WorkflowState.HUMAN_REQUIRED,
            4,
            WorkflowState.REJECTED,
            human_result_refs=(result_b.serialized_ref,),
        )
        with pytest.raises(JudgmentAuthorityError):
            await judgment_authority.issue(
                judgment_id=f"wrong-target-{label}",
                judgment_version="v1",
                request=wrong_target,
                policy=human_policy,
                human_result_ref=result_b.serialized_ref,
                evidence_attestation_ref=None,
                reason_code="WRONG_TARGET",
                reason_vocabulary_version="v1",
            )

        # A real Task B WorkRun/result still cannot consume Task A policy.
        run_task_b = f"run-p1-7-task-b-{uuid4()}"
        await advance_to_admission(task_b, run_task_b)
        _, _, gate_task_b = await open_gate(task_b, run_task_b)
        action_task_b = await principal_authority.issue_action_authority(
            principal,
            gate_task_b.serialized_ref,
            idempotency_scope=f"result-task-b-{label}",
        )
        result_task_b = await human_repository.submit_result(
            human_result_id=f"result-task-b-{label}",
            human_result_version="v1",
            gate_ref=gate_task_b.serialized_ref,
            principal=principal,
            action_authority=action_task_b,
            result_kind=HumanResultKind.APPROVE,
            structured_reason_code="APPROVED_TASK_B",
            reason_vocabulary_version="v1",
            idempotency_key=f"result-task-b-{label}",
        )
        accept_task_b = request(
            task_b,
            run_task_b,
            WorkflowState.HUMAN_REQUIRED,
            4,
            WorkflowState.ACCEPTED,
            human_result_refs=(result_task_b.serialized_ref,),
        )
        task_mismatch_guard_request = replace(
            accept_task_b,
            transition_request_id=str(uuid4()),
            human_result_refs=(result_a.serialized_ref,),
        )
        task_mismatch_guard = await human_guard.result_guard_participant(
            task_mismatch_guard_request, GuardId.G_HUMAN_APPROVED
        )
        assert (
            await kernel.request_transition(
                task_mismatch_guard_request,
                (),
                transaction_participant=task_mismatch_guard,
            )
        ).outcome is DecisionOutcome.DENIED
        task_b_policy = await policy_authority.register(
            policy_id=f"HUMAN_ACCEPT_TASK_B-{label}",
            policy_version="v1",
            task_contract_id=task_b,
            task_contract_version="v1",
            source_state=WorkflowState.HUMAN_REQUIRED,
            target_state=WorkflowState.ACCEPTED,
            owner_policy=JudgmentOwnerPolicy.HUMAN,
            requires_human_result=True,
            requires_post_human_evidence=False,
        )
        with pytest.raises(JudgmentAuthorityError):
            await judgment_authority.issue(
                judgment_id=f"foreign-task-result-{label}",
                judgment_version="v1",
                request=task_mismatch_guard_request,
                policy=task_b_policy,
                human_result_ref=result_a.serialized_ref,
                evidence_attestation_ref=None,
                reason_code="FOREIGN_TASK_RESULT",
                reason_vocabulary_version="v1",
            )
        with pytest.raises(JudgmentAuthorityError):
            await judgment_authority.issue(
                judgment_id=f"wrong-task-policy-{label}",
                judgment_version="v1",
                request=accept_task_b,
                policy=human_policy,
                human_result_ref=result_task_b.serialized_ref,
                evidence_attestation_ref=None,
                reason_code="WRONG_TASK_POLICY",
                reason_vocabulary_version="v1",
            )

        # COMMAND_CENTER is a separate durable server authority, not HumanResult/text.
        cc_run = f"run-p1-7-command-center-{uuid4()}"
        await advance_to_admission(task_a, cc_run)
        cc_request = request(
            task_a,
            cc_run,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.REJECTED,
        )
        cc_policy = await policy_authority.register(
            policy_id=f"COMMAND_CENTER_REJECT-{label}",
            policy_version="v1",
            task_contract_id=task_a,
            task_contract_version="v1",
            source_state=WorkflowState.ADMISSION_PENDING,
            target_state=WorkflowState.REJECTED,
            owner_policy=JudgmentOwnerPolicy.COMMAND_CENTER,
            requires_human_result=False,
            requires_post_human_evidence=False,
        )
        with pytest.raises(JudgmentAuthorityError):
            await judgment_authority.issue(
                judgment_id=f"cc-missing-{label}",
                judgment_version="v1",
                request=cc_request,
                policy=cc_policy,
                human_result_ref=None,
                evidence_attestation_ref=None,
                reason_code="CALLER_TEXT_COMMAND_CENTER",
                reason_vocabulary_version="v1",
            )
        with pytest.raises(JudgmentAuthorityError):
            await judgment_authority.issue(
                judgment_id=f"cc-human-substitute-{label}",
                judgment_version="v1",
                request=replace(cc_request, human_result_refs=(result_a.serialized_ref,)),
                policy=cc_policy,
                human_result_ref=result_a.serialized_ref,
                evidence_attestation_ref=None,
                reason_code="HUMAN_IS_NOT_COMMAND_CENTER",
                reason_vocabulary_version="v1",
            )
        fake_cc = CommandCenterPrincipal(
            "command-center",
            command_center.authority_id,
            command_center.authority_version,
            clock(),
            clock() + timedelta(minutes=5),
            object(),
        )
        with pytest.raises(JudgmentAuthorityError):
            await command_center.issue_action(
                action_id=f"fake-cc-action-{label}",
                principal=fake_cc,
                request=cc_request,
                policy=cc_policy,
                judgment_kind=JudgmentKind.REJECTED,
            )
        cc_principal = command_center.authenticate(principal_id="local-command-center")
        cc_action = await command_center.issue_action(
            action_id=f"cc-action-{label}",
            principal=cc_principal,
            request=cc_request,
            policy=cc_policy,
            judgment_kind=JudgmentKind.REJECTED,
        )
        cc_judgment = await judgment_authority.issue(
            judgment_id=f"cc-judgment-{label}",
            judgment_version="v1",
            request=cc_request,
            policy=cc_policy,
            human_result_ref=None,
            evidence_attestation_ref=None,
            command_center_action_ref=cc_action.serialized_ref,
            reason_code="COMMAND_CENTER_REJECTED",
            reason_vocabulary_version="v1",
        )
        assert cc_judgment.owner_policy is JudgmentOwnerPolicy.COMMAND_CENTER

        # Judgment immutable ID is idempotent only for one complete proposal fingerprint.
        system_run = f"run-p1-7-system-{uuid4()}"
        await advance_to_admission(task_a, system_run)
        system_request = request(
            task_a,
            system_run,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.REJECTED,
        )
        system_policy = await policy_authority.register(
            policy_id=f"SYSTEM_REJECT-{label}",
            policy_version="v1",
            task_contract_id=task_a,
            task_contract_version="v1",
            source_state=WorkflowState.ADMISSION_PENDING,
            target_state=WorkflowState.REJECTED,
            owner_policy=JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC,
            requires_human_result=False,
            requires_post_human_evidence=False,
            deterministic_kind=JudgmentKind.REJECTED,
        )
        judgment_id = f"identity-judgment-{label}"

        async def issue_system(**changes: Any) -> Any:
            values = {
                "judgment_id": judgment_id,
                "judgment_version": "v1",
                "request": system_request,
                "policy": system_policy,
                "human_result_ref": None,
                "evidence_attestation_ref": None,
                "reason_code": "SYSTEM_REJECTED",
                "reason_vocabulary_version": "v1",
                "supersedes_judgment_ref": None,
            }
            values.update(changes)
            return await judgment_authority.issue(**values)

        identity = await issue_system()
        assert await issue_system() == identity
        identity_counts = await _judgment_counts(sessions, system_run)
        for changed in (
            {"reason_code": "DIFFERENT_REASON"},
            {"supersedes_judgment_ref": "p1-7-judgment:v1:other"},
            {"human_result_ref": result_a.serialized_ref},
        ):
            with pytest.raises(JudgmentAuthorityError, match="JUDGMENT_IDENTITY_CONFLICT"):
                await issue_system(**changed)
            assert await _judgment_counts(sessions, system_run) == identity_counts
        accepted_request = replace(system_request, target_state=WorkflowState.ACCEPTED)
        accepted_policy = await policy_authority.register(
            policy_id=f"SYSTEM_ACCEPT-{label}",
            policy_version="v1",
            task_contract_id=task_a,
            task_contract_version="v1",
            source_state=WorkflowState.ADMISSION_PENDING,
            target_state=WorkflowState.ACCEPTED,
            owner_policy=JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC,
            requires_human_result=False,
            requires_post_human_evidence=False,
            deterministic_kind=JudgmentKind.ACCEPTED,
        )
        with pytest.raises(JudgmentAuthorityError, match="JUDGMENT_IDENTITY_CONFLICT"):
            await issue_system(request=accepted_request, policy=accepted_policy)
        system_policy_v2 = await policy_authority.register(
            policy_id=f"SYSTEM_REJECT-V2-{label}",
            policy_version="v2",
            task_contract_id=task_a,
            task_contract_version="v1",
            source_state=WorkflowState.ADMISSION_PENDING,
            target_state=WorkflowState.REJECTED,
            owner_policy=JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC,
            requires_human_result=False,
            requires_post_human_evidence=False,
            deterministic_kind=JudgmentKind.REJECTED,
        )
        with pytest.raises(JudgmentAuthorityError, match="JUDGMENT_IDENTITY_CONFLICT"):
            await issue_system(policy=system_policy_v2)
        assert await _judgment_counts(sessions, system_run) == identity_counts

        # Superseded durable policy invalidates an old guard after authority restart.
        stale_transition = replace(system_request, judgment_refs=(identity.serialized_ref,))
        restarted_policy = JudgmentPolicyAuthority(sessions, clock=clock)
        restarted_judgment = PostgresJudgmentAuthority(
            sessions, evidence_repository, restarted_policy, clock=clock
        )
        restarted_repository = PostgresTransitionRepository(
            sessions,
            TransitionEvaluator(system, (evidence_guard, human_guard, restarted_judgment)),
            TestBlockerSourceVerifier(),
        )
        restarted_kernel = WorkflowKernel(restarted_repository)
        not_required = await human_guard.policy_guard_participant(
            stale_transition, GuardId.G_HUMAN_NOT_REQUIRED
        )
        stale_judgment_participant = await restarted_judgment.participant(
            stale_transition, identity.serialized_ref
        )
        assert (
            await restarted_kernel.request_transition(
                stale_transition,
                (),
                transaction_participant=CompositeTransitionParticipant(
                    (not_required, stale_judgment_participant)
                ),
            )
        ).outcome is DecisionOutcome.DENIED
        assert (await restarted_kernel.load(system_run)).state is WorkflowState.ADMISSION_PENDING  # type: ignore[union-attr]

        # Expired reservation never opens; pending expiry is additive and idempotent.
        expired_open_run = f"run-p1-7-expired-open-{uuid4()}"
        await advance_to_admission(task_a, expired_open_run)
        expired_request = request(
            task_a,
            expired_open_run,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.HUMAN_REQUIRED,
        )
        expired_reservation = reservation_authority.reserve(
            expired_request,
            designated_principal_selector_fingerprint="reviewers-v1",
            expires_at=clock(),
        )
        expired_pre = await pre_human(task_a, expired_open_run)
        expired_participant = await human_guard.gate_open_participant(
            expired_request, expired_reservation, expired_pre.serialized_ref
        )
        assert (
            await kernel.request_transition(
                expired_request, (), transaction_participant=expired_participant
            )
        ).outcome is DecisionOutcome.DENIED
        assert await human_repository.load_current_gate(expired_open_run) is None

        expiry_run = f"run-p1-7-expiry-{uuid4()}"
        await advance_to_admission(task_a, expiry_run)
        expires_at = clock() + timedelta(seconds=5)
        _, _, expiring_gate = await open_gate(task_a, expiry_run, expires_at=expires_at)
        pre_expiry_action = await principal_authority.issue_action_authority(
            principal,
            expiring_gate.serialized_ref,
            idempotency_scope=f"expiring-result-{label}",
        )
        clock_value[0] = expires_at
        expiry_results = await asyncio.gather(
            human_repository.expire_gate_if_needed(expiring_gate.serialized_ref),
            human_repository.expire_gate_if_needed(expiring_gate.serialized_ref),
        )
        assert sorted(expiry_results) == [False, True]
        assert await _expiry_event_count(sessions, expiring_gate.human_gate_id) == 1
        expired_gate = await human_repository.load_gate(expiring_gate.serialized_ref)
        assert expired_gate is not None
        assert expired_gate.status is HumanGateStatus.CANCELLED
        with pytest.raises(HumanAuthorityError):
            await principal_authority.issue_action_authority(
                principal,
                expiring_gate.serialized_ref,
                idempotency_scope="after-expiry",
            )
        with pytest.raises(HumanAuthorityError):
            await human_repository.submit_result(
                human_result_id=f"after-expiry-{label}",
                human_result_version="v1",
                gate_ref=expiring_gate.serialized_ref,
                principal=principal,
                action_authority=pre_expiry_action,
                result_kind=HumanResultKind.APPROVE,
                structured_reason_code="TOO_LATE",
                reason_vocabulary_version="v1",
                idempotency_key=f"after-expiry-{label}",
            )
        restarted_human = PostgresHumanAuthorityRepository(sessions, clock=clock)
        assert not await restarted_human.expire_gate_if_needed(expiring_gate.serialized_ref)
        assert await _expiry_event_count(sessions, expiring_gate.human_gate_id) == 1

        # A result admitted before expiry cannot mint a guard at/after gate expiry.
        guard_run = f"run-p1-7-guard-expiry-{uuid4()}"
        await advance_to_admission(task_a, guard_run)
        guard_expiry = clock() + timedelta(seconds=5)
        _, _, guard_gate = await open_gate(task_a, guard_run, expires_at=guard_expiry)
        guard_action = await principal_authority.issue_action_authority(
            principal,
            guard_gate.serialized_ref,
            idempotency_scope=f"guard-result-{label}",
        )
        guard_result = await human_repository.submit_result(
            human_result_id=f"guard-result-{label}",
            human_result_version="v1",
            gate_ref=guard_gate.serialized_ref,
            principal=principal,
            action_authority=guard_action,
            result_kind=HumanResultKind.APPROVE,
            structured_reason_code="BEFORE_EXPIRY",
            reason_vocabulary_version="v1",
            idempotency_key=f"guard-result-{label}",
        )
        clock_value[0] = guard_expiry
        guard_request = request(
            task_a,
            guard_run,
            WorkflowState.HUMAN_REQUIRED,
            4,
            WorkflowState.ACCEPTED,
            human_result_refs=(guard_result.serialized_ref,),
        )
        guard_rows_before = await _row_count(sessions, HumanGuardAttestationRow)
        expired_guard_participant = await human_guard.result_guard_participant(
            guard_request, GuardId.G_HUMAN_APPROVED
        )
        assert (
            await kernel.request_transition(
                guard_request, (), transaction_participant=expired_guard_participant
            )
        ).outcome is DecisionOutcome.DENIED
        assert await _row_count(sessions, HumanGuardAttestationRow) == guard_rows_before

        # Expiry discovery and HumanResult admission serialize to one legal outcome.
        race_run = f"run-p1-7-expiry-race-{uuid4()}"
        await advance_to_admission(task_a, race_run)
        race_expiry = clock() + timedelta(seconds=5)
        _, _, race_gate = await open_gate(task_a, race_run, expires_at=race_expiry)
        race_action = await principal_authority.issue_action_authority(
            principal,
            race_gate.serialized_ref,
            idempotency_scope=f"expiry-race-{label}",
        )
        clock_value[0] = race_expiry

        async def submit_at_expiry() -> HumanResult:
            return await human_repository.submit_result(
                human_result_id=f"expiry-race-result-{label}",
                human_result_version="v1",
                gate_ref=race_gate.serialized_ref,
                principal=principal,
                action_authority=race_action,
                result_kind=HumanResultKind.APPROVE,
                structured_reason_code="EXPIRY_RACE",
                reason_vocabulary_version="v1",
                idempotency_key=f"expiry-race-result-{label}",
            )

        race_outcomes = await asyncio.gather(
            human_repository.expire_gate_if_needed(race_gate.serialized_ref),
            submit_at_expiry(),
            return_exceptions=True,
        )
        assert sum(isinstance(item, HumanResult) for item in race_outcomes) in {0, 1}
        race_current = await human_repository.load_gate(race_gate.serialized_ref)
        assert race_current is not None
        if race_current.status is HumanGateStatus.CANCELLED:
            assert not any(isinstance(item, HumanResult) for item in race_outcomes)
            assert await _expiry_event_count(sessions, race_gate.human_gate_id) == 1
        else:
            assert race_current.status is HumanGateStatus.RESOLVED
            assert sum(isinstance(item, HumanResult) for item in race_outcomes) == 1

        # Concurrent foreign/correct reservations stay isolated by exact run locks.
        concurrent_run_a = f"run-p1-7-reservation-concurrent-a-{uuid4()}"
        concurrent_run_b = f"run-p1-7-reservation-concurrent-b-{uuid4()}"
        await advance_to_admission(task_a, concurrent_run_a)
        await advance_to_admission(task_a, concurrent_run_b)
        concurrent_request_a = request(
            task_a,
            concurrent_run_a,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.HUMAN_REQUIRED,
        )
        concurrent_request_b = request(
            task_a,
            concurrent_run_b,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.HUMAN_REQUIRED,
        )
        concurrent_reservation_a = reservation_authority.reserve(
            concurrent_request_a,
            designated_principal_selector_fingerprint="reviewers-v1",
        )
        concurrent_pre_a = await pre_human(task_a, concurrent_run_a)
        concurrent_pre_b = await pre_human(task_a, concurrent_run_b)
        correct_participant = await human_guard.gate_open_participant(
            concurrent_request_a,
            concurrent_reservation_a,
            concurrent_pre_a.serialized_ref,
        )
        cross_bound_participant = await human_guard.gate_open_participant(
            concurrent_request_b,
            concurrent_reservation_a,
            concurrent_pre_b.serialized_ref,
        )
        reservation_decisions = await asyncio.gather(
            kernel.request_transition(
                concurrent_request_a, (), transaction_participant=correct_participant
            ),
            kernel.request_transition(
                concurrent_request_b, (), transaction_participant=cross_bound_participant
            ),
        )
        assert [item.outcome for item in reservation_decisions].count(DecisionOutcome.ADMITTED) == 1
        assert [item.outcome for item in reservation_decisions].count(DecisionOutcome.DENIED) == 1
        assert await human_repository.load_current_gate(concurrent_run_a) is not None
        assert await human_repository.load_current_gate(concurrent_run_b) is None

        # PostgreSQL serializes same-ID Judgment retries and conflicting proposals.
        concurrent_policy = await policy_authority.register(
            policy_id=f"SYSTEM_CONCURRENT-{label}",
            policy_version="v3",
            task_contract_id=task_a,
            task_contract_version="v1",
            source_state=WorkflowState.ADMISSION_PENDING,
            target_state=WorkflowState.REJECTED,
            owner_policy=JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC,
            requires_human_result=False,
            requires_post_human_evidence=False,
            deterministic_kind=JudgmentKind.REJECTED,
        )
        same_run = f"run-p1-7-judgment-same-{uuid4()}"
        await advance_to_admission(task_a, same_run)
        same_request = request(
            task_a,
            same_run,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.REJECTED,
        )

        async def issue_concurrent(
            run_request: TransitionRequest, judgment_id_value: str, reason: str
        ) -> Any:
            return await judgment_authority.issue(
                judgment_id=judgment_id_value,
                judgment_version="v1",
                request=run_request,
                policy=concurrent_policy,
                human_result_ref=None,
                evidence_attestation_ref=None,
                reason_code=reason,
                reason_vocabulary_version="v1",
            )

        same_id = f"same-concurrent-{label}"
        same_outcomes = await asyncio.gather(
            issue_concurrent(same_request, same_id, "SAME"),
            issue_concurrent(same_request, same_id, "SAME"),
        )
        assert same_outcomes[0] == same_outcomes[1]
        assert (await _judgment_counts(sessions, same_run))[:2] == (1, 1)

        conflict_run = f"run-p1-7-judgment-conflict-{uuid4()}"
        await advance_to_admission(task_a, conflict_run)
        conflict_request = request(
            task_a,
            conflict_run,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.REJECTED,
        )
        conflict_id = f"different-concurrent-{label}"
        conflict_outcomes = await asyncio.gather(
            issue_concurrent(conflict_request, conflict_id, "FIRST"),
            issue_concurrent(conflict_request, conflict_id, "SECOND"),
            return_exceptions=True,
        )
        assert sum(not isinstance(item, Exception) for item in conflict_outcomes) == 1
        assert (
            sum(
                isinstance(item, JudgmentAuthorityError)
                and "JUDGMENT_IDENTITY_CONFLICT" in str(item)
                for item in conflict_outcomes
            )
            == 1
        )
        assert (await _judgment_counts(sessions, conflict_run))[:2] == (1, 1)

        # Supersession and guard use share the durable policy lock; stale use loses.
        policy_race_run = f"run-p1-7-policy-race-{uuid4()}"
        await advance_to_admission(task_a, policy_race_run)
        policy_race_request = request(
            task_a,
            policy_race_run,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.REJECTED,
        )
        policy_race_v1 = await policy_authority.register(
            policy_id=f"SYSTEM_POLICY_RACE-V1-{label}",
            policy_version="race-v1",
            task_contract_id=task_a,
            task_contract_version="v1",
            source_state=WorkflowState.ADMISSION_PENDING,
            target_state=WorkflowState.REJECTED,
            owner_policy=JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC,
            requires_human_result=False,
            requires_post_human_evidence=False,
            deterministic_kind=JudgmentKind.REJECTED,
        )
        policy_race_judgment = await judgment_authority.issue(
            judgment_id=f"policy-race-judgment-{label}",
            judgment_version="v1",
            request=policy_race_request,
            policy=policy_race_v1,
            human_result_ref=None,
            evidence_attestation_ref=None,
            reason_code="POLICY_RACE_V1",
            reason_vocabulary_version="v1",
        )
        policy_race_transition = replace(
            policy_race_request,
            judgment_refs=(policy_race_judgment.serialized_ref,),
        )
        policy_race_not_required = await human_guard.policy_guard_participant(
            policy_race_transition, GuardId.G_HUMAN_NOT_REQUIRED
        )
        policy_race_judgment_participant = await judgment_authority.participant(
            policy_race_transition, policy_race_judgment.serialized_ref
        )
        supersession_task = asyncio.create_task(
            policy_authority.register(
                policy_id=f"SYSTEM_POLICY_RACE-V2-{label}",
                policy_version="race-v2",
                task_contract_id=task_a,
                task_contract_version="v1",
                source_state=WorkflowState.ADMISSION_PENDING,
                target_state=WorkflowState.REJECTED,
                owner_policy=JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC,
                requires_human_result=False,
                requires_post_human_evidence=False,
                deterministic_kind=JudgmentKind.REJECTED,
            )
        )
        await asyncio.sleep(0)
        policy_race_decision = await kernel.request_transition(
            policy_race_transition,
            (),
            transaction_participant=CompositeTransitionParticipant(
                (policy_race_not_required, policy_race_judgment_participant)
            ),
        )
        policy_race_v2 = await supersession_task
        assert policy_race_decision.outcome is DecisionOutcome.DENIED
        assert (await kernel.load(policy_race_run)).state is WorkflowState.ADMISSION_PENDING  # type: ignore[union-attr]

        # Existing immutable Judgment identity replays before current policy effectiveness.
        historical_retry_counts = await _judgment_counts(sessions, system_run)
        historical_identity = await issue_system()
        assert historical_identity == identity
        assert await _judgment_counts(sessions, system_run) == historical_retry_counts
        with pytest.raises(JudgmentIdentityConflictError, match="JUDGMENT_IDENTITY_CONFLICT"):
            await issue_system(reason_code="CHANGED_AFTER_POLICY_SUPERSESSION")
        assert await _judgment_counts(sessions, system_run) == historical_retry_counts

        # An exact historical retry also survives the WorkRun leaving its source state, while
        # the stale Judgment cannot become current guard authority for the new state/version.
        state_replay_run = f"run-p1-7-state-replay-{uuid4()}"
        await advance_to_admission(task_b, state_replay_run)
        state_replay_request = request(
            task_b,
            state_replay_run,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.REJECTED,
        )
        state_replay_policy = await policy_authority.register(
            policy_id=f"SYSTEM_STATE_REPLAY-{label}",
            policy_version="v1",
            task_contract_id=task_b,
            task_contract_version="v1",
            source_state=WorkflowState.ADMISSION_PENDING,
            target_state=WorkflowState.REJECTED,
            owner_policy=JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC,
            requires_human_result=False,
            requires_post_human_evidence=False,
            deterministic_kind=JudgmentKind.REJECTED,
        )

        async def issue_state_replay() -> Any:
            return await judgment_authority.issue(
                judgment_id=f"state-replay-{label}",
                judgment_version="v1",
                request=state_replay_request,
                policy=state_replay_policy,
                human_result_ref=None,
                evidence_attestation_ref=None,
                reason_code="STATE_REPLAY_REJECTED",
                reason_vocabulary_version="v1",
            )

        state_replay_judgment = await issue_state_replay()
        state_replay_transition = replace(
            state_replay_request,
            judgment_refs=(state_replay_judgment.serialized_ref,),
        )
        state_replay_human = await human_guard.policy_guard_participant(
            state_replay_transition, GuardId.G_HUMAN_NOT_REQUIRED
        )
        state_replay_judgment_participant = await judgment_authority.participant(
            state_replay_transition, state_replay_judgment.serialized_ref
        )
        assert (
            await kernel.request_transition(
                state_replay_transition,
                (),
                transaction_participant=CompositeTransitionParticipant(
                    (state_replay_human, state_replay_judgment_participant)
                ),
            )
        ).outcome is DecisionOutcome.ADMITTED
        assert (await kernel.load(state_replay_run)).state is WorkflowState.REJECTED  # type: ignore[union-attr]
        state_replay_counts = await _judgment_counts(sessions, state_replay_run)
        assert await issue_state_replay() == state_replay_judgment
        assert await _judgment_counts(sessions, state_replay_run) == state_replay_counts
        stale_state_use = request(
            task_b,
            state_replay_run,
            WorkflowState.REJECTED,
            4,
            WorkflowState.FAILED,
            judgment_refs=(state_replay_judgment.serialized_ref,),
        )
        stale_state_participant = await judgment_authority.participant(
            stale_state_use, state_replay_judgment.serialized_ref
        )
        assert (
            await kernel.request_transition(
                stale_state_use, (), transaction_participant=stale_state_participant
            )
        ).outcome is DecisionOutcome.DENIED

        # PostgreSQL global Judgment-ID serialization covers different WorkRuns too.
        global_judgment_run_a = f"run-p1-7-global-judgment-a-{uuid4()}"
        global_judgment_run_b = f"run-p1-7-global-judgment-b-{uuid4()}"
        await advance_to_admission(task_a, global_judgment_run_a)
        await advance_to_admission(task_a, global_judgment_run_b)
        global_judgment_request_a = request(
            task_a,
            global_judgment_run_a,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.REJECTED,
        )
        global_judgment_request_b = request(
            task_a,
            global_judgment_run_b,
            WorkflowState.ADMISSION_PENDING,
            3,
            WorkflowState.REJECTED,
        )
        global_judgment_id = f"global-judgment-{label}"

        async def issue_global_judgment(value: TransitionRequest) -> Any:
            return await judgment_authority.issue(
                judgment_id=global_judgment_id,
                judgment_version="v1",
                request=value,
                policy=policy_race_v2,
                human_result_ref=None,
                evidence_attestation_ref=None,
                reason_code="GLOBAL_JUDGMENT",
                reason_vocabulary_version="v1",
            )

        global_judgment_outcomes = await asyncio.gather(
            issue_global_judgment(global_judgment_request_a),
            issue_global_judgment(global_judgment_request_b),
            return_exceptions=True,
        )
        assert sum(not isinstance(item, Exception) for item in global_judgment_outcomes) == 1
        assert (
            sum(
                isinstance(item, JudgmentIdentityConflictError)
                and "JUDGMENT_IDENTITY_CONFLICT" in str(item)
                for item in global_judgment_outcomes
            )
            == 1
        )
        assert await _object_id_count(sessions, JudgmentRow, "judgment_id", global_judgment_id) == 1
        global_judgment_current = (
            await judgment_authority.verify_consistency(global_judgment_run_a),
            await judgment_authority.verify_consistency(global_judgment_run_b),
        )
        assert sum(item is not None for item in global_judgment_current) == 1

        # Locked server time, not an observation made before waiting, owns gate expiry.
        t4 = NOW + timedelta(minutes=10)
        t5 = t4 + timedelta(seconds=5)
        t6 = t5 + timedelta(seconds=1)
        clock_value[0] = t4
        action_wait_run = f"run-p1-7-action-lock-time-{uuid4()}"
        await advance_to_admission(task_a, action_wait_run)
        _, _, action_wait_gate = await open_gate(task_a, action_wait_run, expires_at=t5)
        async with sessions() as lock_session, lock_session.begin():
            await acquire_work_run_transaction_lock(lock_session, action_wait_run)
            calls_before_wait = clock_calls[0]
            waiting_action = asyncio.create_task(
                principal_authority.issue_action_authority(
                    principal,
                    action_wait_gate.serialized_ref,
                    idempotency_scope=f"action-lock-time-{label}",
                )
            )
            await _wait_for_advisory_wait(sessions)
            assert clock_calls[0] == calls_before_wait
            clock_value[0] = t6
        with pytest.raises(HumanAuthorityError, match="HUMAN_GATE_EXPIRED"):
            await waiting_action
        assert await _expiry_event_count(sessions, action_wait_gate.human_gate_id) == 1

        # Acquiring the same canonical lock at T4 is a legal positive authority outcome.
        clock_value[0] = t4
        lock_win_run = f"run-p1-7-lock-time-win-{uuid4()}"
        await advance_to_admission(task_a, lock_win_run)
        _, _, lock_win_gate = await open_gate(task_a, lock_win_run, expires_at=t5)
        lock_win_action = await principal_authority.issue_action_authority(
            principal,
            lock_win_gate.serialized_ref,
            idempotency_scope=f"lock-time-win-{label}",
        )
        assert lock_win_action.issued_at == t4
        assert lock_win_action.expires_at == t5

        # Omitted submitted_at is an explicit proposal marker, never server current time.
        omitted_result_id = f"omitted-submitted-at-{label}"
        omitted_result = await human_repository.submit_result(
            human_result_id=omitted_result_id,
            human_result_version="v1",
            gate_ref=lock_win_gate.serialized_ref,
            principal=principal,
            action_authority=lock_win_action,
            result_kind=HumanResultKind.APPROVE,
            structured_reason_code="OMITTED_TIMESTAMP",
            reason_vocabulary_version="v1",
            idempotency_key=omitted_result_id,
        )
        assert omitted_result.submitted_at == t4
        clock_value[0] = t6
        calls_before_retry = clock_calls[0]
        omitted_retry = await human_repository.submit_result(
            human_result_id=omitted_result_id,
            human_result_version="v1",
            gate_ref=lock_win_gate.serialized_ref,
            principal=principal,
            action_authority=lock_win_action,
            result_kind=HumanResultKind.APPROVE,
            structured_reason_code="OMITTED_TIMESTAMP",
            reason_vocabulary_version="v1",
            idempotency_key=omitted_result_id,
        )
        assert omitted_retry == omitted_result
        assert clock_calls[0] == calls_before_retry
        with pytest.raises(HumanResultIdentityConflictError):
            await human_repository.submit_result(
                human_result_id=omitted_result_id,
                human_result_version="v1",
                gate_ref=lock_win_gate.serialized_ref,
                principal=principal,
                action_authority=lock_win_action,
                result_kind=HumanResultKind.APPROVE,
                structured_reason_code="OMITTED_TIMESTAMP",
                reason_vocabulary_version="v1",
                idempotency_key=omitted_result_id,
                submitted_at=t4,
            )

        # submit_result samples no authority time before it acquires the canonical lock.
        clock_value[0] = t4
        result_wait_run = f"run-p1-7-result-lock-time-{uuid4()}"
        await advance_to_admission(task_a, result_wait_run)
        _, _, result_wait_gate = await open_gate(task_a, result_wait_run, expires_at=t5)
        result_wait_action = await principal_authority.issue_action_authority(
            principal,
            result_wait_gate.serialized_ref,
            idempotency_scope=f"result-lock-time-{label}",
        )
        result_wait_id = f"result-lock-time-{label}"
        async with sessions() as lock_session, lock_session.begin():
            await acquire_work_run_transaction_lock(lock_session, result_wait_run)
            calls_before_wait = clock_calls[0]
            waiting_result = asyncio.create_task(
                human_repository.submit_result(
                    human_result_id=result_wait_id,
                    human_result_version="v1",
                    gate_ref=result_wait_gate.serialized_ref,
                    principal=principal,
                    action_authority=result_wait_action,
                    result_kind=HumanResultKind.APPROVE,
                    structured_reason_code="RESULT_LOCK_TIME",
                    reason_vocabulary_version="v1",
                    idempotency_key=result_wait_id,
                )
            )
            await _wait_for_advisory_wait(sessions)
            assert clock_calls[0] == calls_before_wait
            clock_value[0] = t6
        with pytest.raises(HumanAuthorityError, match="HUMAN_GATE_EXPIRED"):
            await waiting_result
        assert (
            await _object_id_count(sessions, HumanResultRow, "human_result_id", result_wait_id) == 0
        )
        assert await _expiry_event_count(sessions, result_wait_gate.human_gate_id) == 1

        # PostgreSQL global HumanResult-ID serialization covers different WorkRuns.
        clock_value[0] = NOW + timedelta(minutes=20)
        global_result_run_a = f"run-p1-7-global-result-a-{uuid4()}"
        global_result_run_b = f"run-p1-7-global-result-b-{uuid4()}"
        await advance_to_admission(task_a, global_result_run_a)
        await advance_to_admission(task_a, global_result_run_b)
        _, _, global_result_gate_a = await open_gate(task_a, global_result_run_a)
        _, _, global_result_gate_b = await open_gate(task_a, global_result_run_b)
        global_result_action_a = await principal_authority.issue_action_authority(
            principal,
            global_result_gate_a.serialized_ref,
            idempotency_scope=f"global-result-a-{label}",
        )
        global_result_action_b = await principal_authority.issue_action_authority(
            principal,
            global_result_gate_b.serialized_ref,
            idempotency_scope=f"global-result-b-{label}",
        )
        global_result_id = f"global-human-result-{label}"

        async def submit_global_result(gate: HumanGate, action: Any, suffix: str) -> HumanResult:
            return await human_repository.submit_result(
                human_result_id=global_result_id,
                human_result_version="v1",
                gate_ref=gate.serialized_ref,
                principal=principal,
                action_authority=action,
                result_kind=HumanResultKind.APPROVE,
                structured_reason_code=f"GLOBAL_RESULT_{suffix}",
                reason_vocabulary_version="v1",
                idempotency_key=f"global-result-{suffix}-{label}",
            )

        global_result_outcomes = await asyncio.gather(
            submit_global_result(global_result_gate_a, global_result_action_a, "A"),
            submit_global_result(global_result_gate_b, global_result_action_b, "B"),
            return_exceptions=True,
        )
        assert sum(isinstance(item, HumanResult) for item in global_result_outcomes) == 1
        assert (
            sum(
                isinstance(item, HumanResultIdentityConflictError)
                for item in global_result_outcomes
            )
            == 1
        )
        assert (
            await _object_id_count(sessions, HumanResultRow, "human_result_id", global_result_id)
            == 1
        )
        global_result_gates = (
            await human_repository.load_gate(global_result_gate_a.serialized_ref),
            await human_repository.load_gate(global_result_gate_b.serialized_ref),
        )
        assert (
            sum(
                item is not None and item.status is HumanGateStatus.RESOLVED
                for item in global_result_gates
            )
            == 1
        )
        assert (
            sum(
                item is not None and item.status is HumanGateStatus.PENDING
                for item in global_result_gates
            )
            == 1
        )
        await human_repository.verify_consistency(global_result_run_a)
        await human_repository.verify_consistency(global_result_run_b)

        # Existing-object replay verifies immutable lineage, not just a self-consistent row.
        def corrupt_result_fixture(
            fixture_id: str,
            *,
            gate_ref: str = result_b.human_gate_ref,
            gate_id: str = gate_b.human_gate_id,
        ) -> tuple[HumanResult, HumanResultRow]:
            provisional = replace(
                result_b,
                human_result_id=fixture_id,
                human_result_fingerprint="",
                human_gate_ref=gate_ref,
                idempotency_key=fixture_id,
            )
            value = replace(
                provisional,
                human_result_fingerprint=_human_result_fingerprint(provisional),
            )
            proposal = _human_result_proposal_fingerprint(
                human_result_id=fixture_id,
                human_result_version="v1",
                gate_ref=gate_ref,
                principal=principal,
                action_authority=action_b,
                result_kind=HumanResultKind.APPROVE,
                structured_reason_code="APPROVED_B",
                reason_vocabulary_version="v1",
                idempotency_key=fixture_id,
                private_comment_ref=None,
                private_comment_hash=None,
                sensitivity=EvidenceSensitivity.INTERNAL,
                caller_submitted_at=None,
            )
            return value, _result_row(value, gate_id, proposal)

        async def replay_corrupt_result(value: HumanResult) -> HumanResult:
            return await human_repository.submit_result(
                human_result_id=value.human_result_id,
                human_result_version=value.human_result_version,
                gate_ref=value.human_gate_ref,
                principal=principal,
                action_authority=action_b,
                result_kind=value.result_kind,
                structured_reason_code=value.structured_reason_code,
                reason_vocabulary_version=value.reason_vocabulary_version,
                idempotency_key=value.idempotency_key,
            )

        missing_result, missing_result_row = corrupt_result_fixture(
            f"missing-admitted-result-{label}"
        )
        async with sessions() as session, session.begin():
            session.add(missing_result_row)
        result_replay_counts = (
            await _row_count(sessions, HumanResultRow),
            await _row_count(sessions, HumanResultAuthorityEventRow),
            await _row_count(sessions, HumanGateAuthorityEventRow),
        )
        with pytest.raises(HumanAuthorityError, match="PROVENANCE_INCOMPLETE"):
            await replay_corrupt_result(missing_result)
        assert (
            await _row_count(sessions, HumanResultRow),
            await _row_count(sessions, HumanResultAuthorityEventRow),
            await _row_count(sessions, HumanGateAuthorityEventRow),
        ) == result_replay_counts

        wrong_event_result, wrong_event_row = corrupt_result_fixture(
            f"wrong-admitted-event-result-{label}"
        )
        async with sessions() as session, session.begin():
            session.add(wrong_event_row)
            await session.flush()
            session.add(
                HumanResultAuthorityEventRow(
                    event_id=f"wrong-result-event-{label}",
                    human_result_id=wrong_event_result.human_result_id,
                    event_kind="ADMITTED",
                    prior_revision=0,
                    new_revision=2,
                    payload={
                        "winner_rule": "FIRST_DURABLY_ADMITTED",
                        "gate_ref": gate_a.serialized_ref,
                    },
                    created_at=wrong_event_result.admitted_at,
                )
            )
        result_replay_counts = (
            await _row_count(sessions, HumanResultRow),
            await _row_count(sessions, HumanResultAuthorityEventRow),
            await _row_count(sessions, HumanGateAuthorityEventRow),
        )
        with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
            await replay_corrupt_result(wrong_event_result)
        assert (
            await _row_count(sessions, HumanResultRow),
            await _row_count(sessions, HumanResultAuthorityEventRow),
            await _row_count(sessions, HumanGateAuthorityEventRow),
        ) == result_replay_counts

        wrong_gate_result, wrong_gate_row = corrupt_result_fixture(
            f"wrong-gate-result-{label}",
            gate_ref=gate_a.serialized_ref,
            gate_id=gate_b.human_gate_id,
        )
        async with sessions() as session, session.begin():
            session.add(wrong_gate_row)
        with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
            await replay_corrupt_result(wrong_gate_result)

        # A normal gate is historical authority only with its exact admitted P1-4 opening chain.
        async def replay_result_b() -> HumanResult:
            return await human_repository.submit_result(
                human_result_id=result_b.human_result_id,
                human_result_version=result_b.human_result_version,
                gate_ref=result_b.human_gate_ref,
                principal=principal,
                action_authority=action_b,
                result_kind=result_b.result_kind,
                structured_reason_code=result_b.structured_reason_code,
                reason_vocabulary_version=result_b.reason_vocabulary_version,
                idempotency_key=result_b.idempotency_key,
            )

        async with sessions() as session:
            normal_gate_row = await session.get(HumanGateRow, gate_b.human_gate_id)
            normal_opened = await session.scalar(
                select(HumanGateAuthorityEventRow).where(
                    HumanGateAuthorityEventRow.human_gate_id == gate_b.human_gate_id,
                    HumanGateAuthorityEventRow.event_kind == "OPENED",
                )
            )
            assert normal_gate_row is not None and normal_opened is not None
            normal_gate_payload = dict(normal_gate_row.payload)
            normal_gate_fingerprint = normal_gate_row.gate_fingerprint
            normal_opened_event_id = normal_opened.event_id
            normal_opened_payload = dict(normal_opened.payload)
            opening_decision_id = str(normal_gate_payload["opening_transition_decision_id"])
            opening_request_id = str(normal_gate_payload["opening_transition_request_id"])
            opening_request = await session.get(TransitionRequestRow, opening_request_id)
            opening_evaluation = await session.scalar(
                select(TransitionEvaluationRow).where(
                    TransitionEvaluationRow.transition_request_id == opening_request_id
                )
            )
            opening_decision = await session.get(TransitionDecisionRow, opening_decision_id)
            assert opening_request is not None
            assert opening_evaluation is not None
            assert opening_decision is not None
            opening_human_guard = next(
                item
                for item in opening_evaluation.guards
                if item["guard_id"] == GuardId.G_HUMAN_REQUIRED.value
            )
            opening_human_attestation = await session.scalar(
                select(HumanGuardAttestationRow).where(
                    HumanGuardAttestationRow.serialized_ref == opening_human_guard["authority_ref"]
                )
            )
            assert opening_human_attestation is not None
            pre_human_binding = opening_human_attestation.payload["pre_human_evidence"]
            assert isinstance(pre_human_binding, dict)
            opening_evidence_attestation = await session.scalar(
                select(EvidenceSetAttestationRow).where(
                    EvidenceSetAttestationRow.serialized_ref == pre_human_binding["attestation_ref"]
                )
            )
            assert opening_evidence_attestation is not None
            opening_evidence_evaluation = await session.get(
                EvidenceSetEvaluationRow,
                opening_evidence_attestation.evidence_set_evaluation_id,
            )
            assert opening_evidence_evaluation is not None
            opening_request_fingerprint = opening_request.request_fingerprint
            opening_evaluation_guards = deepcopy(opening_evaluation.guards)
            opening_evaluation_missing = list(opening_evaluation.missing_guards)
            opening_decision_outcome = opening_decision.outcome
            opening_decision_state = opening_decision.resulting_state
            opening_decision_version = opening_decision.resulting_state_version
            opening_decision_owner = opening_decision.admitting_owner
            opening_decision_kernel = opening_decision.kernel_version
            opening_decision_sequence = opening_decision.event_sequence
            opening_human_attestation_original = {
                "fingerprint": opening_human_attestation.fingerprint,
                "work_run_id": opening_human_attestation.work_run_id,
                "state_version": opening_human_attestation.state_version,
                "authority_revision": opening_human_attestation.authority_revision,
                "payload": deepcopy(opening_human_attestation.payload),
            }
            opening_evidence_attestation_original = {
                "checkpoint_ref": opening_evidence_attestation.checkpoint_ref,
                "evidence_authority_revision": (
                    opening_evidence_attestation.evidence_authority_revision
                ),
                "payload": deepcopy(opening_evidence_attestation.payload),
            }
            opening_evidence_evaluation_original = {
                "outcome": opening_evidence_evaluation.outcome,
                "full_requirement_root_hash": (
                    opening_evidence_evaluation.full_requirement_root_hash
                ),
                "checkpoint_subset_root_hash": (
                    opening_evidence_evaluation.checkpoint_subset_root_hash
                ),
                "admitted_ref_root_hash": (opening_evidence_evaluation.admitted_ref_root_hash),
                "evidence_authority_revision": (
                    opening_evidence_evaluation.evidence_authority_revision
                ),
                "payload": deepcopy(opening_evidence_evaluation.payload),
            }

        async def restore_normal_opening() -> None:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                current_gate = await session.get(HumanGateRow, gate_b.human_gate_id)
                current_event = await session.scalar(
                    select(HumanGateAuthorityEventRow).where(
                        HumanGateAuthorityEventRow.event_id == normal_opened_event_id
                    )
                )
                current_decision = await session.get(TransitionDecisionRow, opening_decision_id)
                current_request = await session.get(TransitionRequestRow, opening_request_id)
                current_evaluation = await session.scalar(
                    select(TransitionEvaluationRow).where(
                        TransitionEvaluationRow.transition_request_id == opening_request_id
                    )
                )
                current_human_attestation = await session.scalar(
                    select(HumanGuardAttestationRow).where(
                        HumanGuardAttestationRow.serialized_ref
                        == opening_human_guard["authority_ref"]
                    )
                )
                current_evidence_attestation = await session.scalar(
                    select(EvidenceSetAttestationRow).where(
                        EvidenceSetAttestationRow.serialized_ref
                        == pre_human_binding["attestation_ref"]
                    )
                )
                current_evidence_evaluation = await session.get(
                    EvidenceSetEvaluationRow,
                    opening_evidence_attestation.evidence_set_evaluation_id,
                )
                assert current_gate is not None and current_event is not None
                assert current_request is not None and current_evaluation is not None
                assert current_decision is not None
                assert current_human_attestation is not None
                assert current_evidence_attestation is not None
                assert current_evidence_evaluation is not None
                current_gate.payload = normal_gate_payload
                current_gate.gate_fingerprint = normal_gate_fingerprint
                current_event.event_kind = "OPENED"
                current_event.payload = normal_opened_payload
                current_request.request_fingerprint = opening_request_fingerprint
                current_evaluation.guards = opening_evaluation_guards
                current_evaluation.missing_guards = opening_evaluation_missing
                current_decision.outcome = opening_decision_outcome
                current_decision.resulting_state = opening_decision_state
                current_decision.resulting_state_version = opening_decision_version
                current_decision.admitting_owner = opening_decision_owner
                current_decision.kernel_version = opening_decision_kernel
                current_decision.event_sequence = opening_decision_sequence
                current_human_attestation.fingerprint = str(
                    opening_human_attestation_original["fingerprint"]
                )
                current_human_attestation.work_run_id = str(
                    opening_human_attestation_original["work_run_id"]
                )
                current_human_attestation.state_version = int(
                    opening_human_attestation_original["state_version"]
                )
                current_human_attestation.authority_revision = int(
                    opening_human_attestation_original["authority_revision"]
                )
                current_human_attestation.payload = deepcopy(
                    opening_human_attestation_original["payload"]
                )
                current_evidence_attestation.checkpoint_ref = str(
                    opening_evidence_attestation_original["checkpoint_ref"]
                )
                current_evidence_attestation.evidence_authority_revision = int(
                    opening_evidence_attestation_original["evidence_authority_revision"]
                )
                current_evidence_attestation.payload = deepcopy(
                    opening_evidence_attestation_original["payload"]
                )
                current_evidence_evaluation.outcome = str(
                    opening_evidence_evaluation_original["outcome"]
                )
                current_evidence_evaluation.full_requirement_root_hash = str(
                    opening_evidence_evaluation_original["full_requirement_root_hash"]
                )
                current_evidence_evaluation.checkpoint_subset_root_hash = str(
                    opening_evidence_evaluation_original["checkpoint_subset_root_hash"]
                )
                current_evidence_evaluation.admitted_ref_root_hash = str(
                    opening_evidence_evaluation_original["admitted_ref_root_hash"]
                )
                current_evidence_evaluation.evidence_authority_revision = int(
                    opening_evidence_evaluation_original["evidence_authority_revision"]
                )
                current_evidence_evaluation.payload = deepcopy(
                    opening_evidence_evaluation_original["payload"]
                )

        try:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                event = await session.scalar(
                    select(HumanGateAuthorityEventRow).where(
                        HumanGateAuthorityEventRow.event_id == normal_opened_event_id
                    )
                )
                assert event is not None
                event.event_kind = "MISSING_OPENED"
            with pytest.raises(HumanAuthorityError, match="PROVENANCE_INCOMPLETE"):
                await replay_result_b()
        finally:
            await restore_normal_opening()

        try:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                current_gate = await session.get(HumanGateRow, gate_b.human_gate_id)
                assert current_gate is not None
                current_gate.gate_fingerprint = "0" * 64
            with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                await replay_result_b()
        finally:
            await restore_normal_opening()

        try:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                event = await session.scalar(
                    select(HumanGateAuthorityEventRow).where(
                        HumanGateAuthorityEventRow.event_id == normal_opened_event_id
                    )
                )
                assert event is not None
                event.payload = {
                    **event.payload,
                    "transition_request_id": f"wrong-request-{label}",
                    "transition_decision_id": f"wrong-decision-{label}",
                }
            with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                await replay_result_b()
        finally:
            await restore_normal_opening()

        try:
            missing_request_id = f"missing-opening-request-{label}"
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                current_gate = await session.get(HumanGateRow, gate_b.human_gate_id)
                event = await session.scalar(
                    select(HumanGateAuthorityEventRow).where(
                        HumanGateAuthorityEventRow.event_id == normal_opened_event_id
                    )
                )
                assert current_gate is not None and event is not None
                current_gate.payload = {
                    **current_gate.payload,
                    "opening_transition_request_id": missing_request_id,
                }
                event.payload = {
                    **event.payload,
                    "transition_request_id": missing_request_id,
                }
            with pytest.raises(HumanAuthorityError, match="PROVENANCE_INCOMPLETE"):
                await replay_result_b()
        finally:
            await restore_normal_opening()

        try:
            missing_decision_id = f"missing-opening-decision-{label}"
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                current_gate = await session.get(HumanGateRow, gate_b.human_gate_id)
                event = await session.scalar(
                    select(HumanGateAuthorityEventRow).where(
                        HumanGateAuthorityEventRow.event_id == normal_opened_event_id
                    )
                )
                assert current_gate is not None and event is not None
                current_gate.payload = {
                    **current_gate.payload,
                    "opening_transition_decision_id": missing_decision_id,
                }
                event.payload = {
                    **event.payload,
                    "transition_decision_id": missing_decision_id,
                }
            with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                await replay_result_b()
        finally:
            await restore_normal_opening()

        try:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                decision = await session.get(TransitionDecisionRow, opening_decision_id)
                assert decision is not None
                decision.outcome = "DENIED"
                decision.resulting_state = WorkflowState.REJECTED.value
                decision.resulting_state_version += 1
            with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                await replay_result_b()
        finally:
            await restore_normal_opening()

        try:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                row = await session.get(TransitionRequestRow, opening_request_id)
                assert row is not None
                row.request_fingerprint = "0" * 64
            with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                await replay_result_b()
        finally:
            await restore_normal_opening()

        for mutation in ("missing", "owner", "unsatisfied", "missing-set"):
            try:
                async with sessions() as session, session.begin():
                    await session.execute(text("SET LOCAL session_replication_role = replica"))
                    row = await session.scalar(
                        select(TransitionEvaluationRow).where(
                            TransitionEvaluationRow.transition_request_id == opening_request_id
                        )
                    )
                    assert row is not None
                    guards = [dict(item) for item in row.guards]
                    human_index = next(
                        index
                        for index, item in enumerate(guards)
                        if item["guard_id"] == GuardId.G_HUMAN_REQUIRED.value
                    )
                    if mutation == "missing":
                        guards.pop(human_index)
                    elif mutation == "owner":
                        guards[human_index]["semantic_owner"] = GuardSemanticOwner.P1_4_SYSTEM.value
                    elif mutation == "unsatisfied":
                        guards[human_index]["satisfied"] = False
                    else:
                        row.missing_guards = [GuardId.G_HUMAN_REQUIRED.value]
                    row.guards = guards
                with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                    await replay_result_b()
            finally:
                await restore_normal_opening()

        for field, corrupt_value in (
            ("admitting_owner", "UNTRUSTED_OWNER"),
            ("kernel_version", "UNTRUSTED_KERNEL"),
        ):
            try:
                async with sessions() as session, session.begin():
                    await session.execute(text("SET LOCAL session_replication_role = replica"))
                    decision_record = await session.get(TransitionDecisionRow, opening_decision_id)
                    assert decision_record is not None
                    setattr(decision_record, field, corrupt_value)
                with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                    await replay_result_b()
            finally:
                await restore_normal_opening()

        try:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                decision_record = await session.get(TransitionDecisionRow, opening_decision_id)
                assert decision_record is not None
                decision_record.event_sequence = -opening_decision_sequence
            with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                await replay_result_b()
        finally:
            await restore_normal_opening()

        async def forge_opening_guard_authority_ref(authority_ref: str) -> None:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                request_record = await session.get(TransitionRequestRow, opening_request_id)
                evaluation_record = await session.scalar(
                    select(TransitionEvaluationRow).where(
                        TransitionEvaluationRow.transition_request_id == opening_request_id
                    )
                )
                assert request_record is not None and evaluation_record is not None
                guards = deepcopy(evaluation_record.guards)
                human_index = next(
                    index
                    for index, item in enumerate(guards)
                    if item["guard_id"] == GuardId.G_HUMAN_REQUIRED.value
                )
                guards[human_index]["authority_ref"] = authority_ref
                evaluation_record.guards = guards
                reconstructed = _transition_request_from_row(request_record)
                _, facts = _historical_evaluation_from_row(evaluation_record, reconstructed)
                request_record.request_fingerprint = _request_fingerprint(reconstructed, facts)

        for forged_ref in (
            f"attacker-controlled-human-authority-{label}",
            f"p1-7-human-guard:p1-7-human-guard-v1:missing-{label}",
        ):
            try:
                await forge_opening_guard_authority_ref(forged_ref)
                with pytest.raises(HumanAuthorityError, match="PROVENANCE_INCOMPLETE"):
                    await replay_result_b()
            finally:
                await restore_normal_opening()

        try:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                attestation_row = await session.scalar(
                    select(HumanGuardAttestationRow).where(
                        HumanGuardAttestationRow.serialized_ref
                        == opening_human_guard["authority_ref"]
                    )
                )
                assert attestation_row is not None
                attestation_row.fingerprint = "0" * 64
            with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                await replay_result_b()
        finally:
            await restore_normal_opening()

        async def forge_human_attestation_binding(
            field: str,
            value: object,
            *,
            nested: bool = False,
            row_field: str | None = None,
        ) -> None:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                attestation_row = await session.scalar(
                    select(HumanGuardAttestationRow).where(
                        HumanGuardAttestationRow.serialized_ref
                        == opening_human_guard["authority_ref"]
                    )
                )
                assert attestation_row is not None
                payload = deepcopy(attestation_row.payload)
                target = payload["pre_human_evidence"] if nested else payload
                assert isinstance(target, dict)
                target[field] = value
                attestation_row.payload = payload
                provisional = replace(
                    _human_guard_attestation_from_row(attestation_row), fingerprint=""
                )
                fingerprint = human_guard_attestation_fingerprint(provisional)
                forged = replace(provisional, fingerprint=fingerprint)
                attestation_row.payload = human_guard_attestation_payload(forged)
                attestation_row.fingerprint = fingerprint
                if row_field is not None:
                    setattr(attestation_row, row_field, value)

        for field, corrupt_value, row_field in (
            ("task_contract_version", "foreign-task-version", None),
            ("work_run_id", f"foreign-run-{label}", "work_run_id"),
            ("state_version", 999, "state_version"),
            ("target_state", WorkflowState.REJECTED.value, None),
            ("human_gate_ref", f"p1-7-gate:v1:foreign-{label}", None),
            ("authority_id", f"foreign-human-authority-{label}", None),
            ("authority_version", "foreign-human-authority-version", None),
            ("authority_revision", 999, "authority_revision"),
        ):
            try:
                await forge_human_attestation_binding(field, corrupt_value, row_field=row_field)
                with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                    await replay_result_b()
            finally:
                await restore_normal_opening()

        try:
            await forge_human_attestation_binding(
                "attestation_ref",
                f"p1-6-attestation:p1-6-attestation-v1:missing-{label}",
                nested=True,
            )
            with pytest.raises(HumanAuthorityError, match="PROVENANCE_INCOMPLETE"):
                await replay_result_b()
        finally:
            await restore_normal_opening()

        for field, corrupt_value in (
            ("checkpoint_fingerprint", "f" * 64),
            ("requirement_set_root", "e" * 64),
            ("evidence_authority_revision", 999),
        ):
            try:
                await forge_human_attestation_binding(field, corrupt_value, nested=True)
                with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                    await replay_result_b()
            finally:
                await restore_normal_opening()

        try:
            forged_checkpoint_fingerprint = "9" * 64
            await forge_human_attestation_binding(
                "checkpoint_fingerprint",
                forged_checkpoint_fingerprint,
                nested=True,
            )
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                evidence_attestation_row = await session.scalar(
                    select(EvidenceSetAttestationRow).where(
                        EvidenceSetAttestationRow.serialized_ref
                        == pre_human_binding["attestation_ref"]
                    )
                )
                assert evidence_attestation_row is not None
                payload = deepcopy(evidence_attestation_row.payload)
                payload["checkpoint_fingerprint"] = forged_checkpoint_fingerprint
                evidence_attestation_row.payload = payload
            with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                await replay_result_b()
        finally:
            await restore_normal_opening()

        try:
            forged_admitted_refs = [f"p1-6-admitted:p1-6-evidence-v1:missing-{label}"]
            await forge_human_attestation_binding(
                "ordered_admitted_evidence_refs",
                forged_admitted_refs,
                nested=True,
            )
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                evidence_attestation_row = await session.scalar(
                    select(EvidenceSetAttestationRow).where(
                        EvidenceSetAttestationRow.serialized_ref
                        == pre_human_binding["attestation_ref"]
                    )
                )
                assert evidence_attestation_row is not None
                payload = deepcopy(evidence_attestation_row.payload)
                payload["ordered_admitted_evidence_refs"] = forged_admitted_refs
                evidence_attestation_row.payload = payload
            with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                await replay_result_b()
        finally:
            await restore_normal_opening()

        for field, corrupt_value in (
            ("outcome", "UNSATISFIED"),
            ("full_requirement_root_hash", "d" * 64),
        ):
            try:
                async with sessions() as session, session.begin():
                    await session.execute(text("SET LOCAL session_replication_role = replica"))
                    evaluation_row = await session.get(
                        EvidenceSetEvaluationRow,
                        opening_evidence_attestation.evidence_set_evaluation_id,
                    )
                    assert evaluation_row is not None
                    setattr(evaluation_row, field, corrupt_value)
                    payload = deepcopy(evaluation_row.payload)
                    payload[field] = corrupt_value
                    evaluation_row.payload = payload
                with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                    await replay_result_b()
            finally:
                await restore_normal_opening()

        async with sessions() as session:
            surrounding_request_row = await session.scalar(
                select(TransitionRequestRow).where(
                    TransitionRequestRow.work_run_id == run_b,
                    TransitionRequestRow.observed_state == WorkflowState.READY.value,
                    TransitionRequestRow.target_state == WorkflowState.RUNNING.value,
                )
            )
            assert surrounding_request_row is not None
            surrounding_request_id = surrounding_request_row.transition_request_id
            surrounding_request_fingerprint = surrounding_request_row.request_fingerprint
        try:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                surrounding_request_row = await session.get(
                    TransitionRequestRow, surrounding_request_id
                )
                assert surrounding_request_row is not None
                surrounding_request_row.request_fingerprint = "c" * 64
            with pytest.raises(HumanAuthorityError, match="AUTHORITY_CONFLICT"):
                await replay_result_b()
        finally:
            async with sessions() as session, session.begin():
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                surrounding_request_row = await session.get(
                    TransitionRequestRow, surrounding_request_id
                )
                assert surrounding_request_row is not None
                surrounding_request_row.request_fingerprint = surrounding_request_fingerprint

        block_request = request(
            task_a,
            run_b,
            WorkflowState.HUMAN_REQUIRED,
            4,
            WorkflowState.BLOCKED,
        )
        assert (
            await kernel.request_transition(block_request, system_facts(system, block_request))
        ).outcome is DecisionOutcome.ADMITTED
        assert (await kernel.load(run_b)).state is WorkflowState.BLOCKED  # type: ignore[union-attr]
        assert await replay_result_b() == result_b

        def corrupt_judgment_fixture(
            fixture_id: str,
            *,
            base: Any,
            fixture_request: TransitionRequest,
            fixture_policy: Any,
            human_result_ref: str | None,
            human_gate_ref: str | None,
            human_result_authority_revision: int | None,
            command_center_action_ref: str | None,
            reason_code: str,
            authority_revision: int | None = None,
            supersedes_judgment_ref: str | None = None,
        ) -> tuple[Any, JudgmentEvaluationRow, JudgmentRow, JudgmentAuthorityEventRow]:
            evaluation_id = f"corrupt-evaluation-{fixture_id}"
            provisional = replace(
                base,
                judgment_id=fixture_id,
                fingerprint="",
                evaluation_ref=evaluation_id,
                policy_id=fixture_policy.policy_id,
                policy_version=fixture_policy.policy_version,
                policy_fingerprint=fixture_policy.fingerprint,
                policy_authority_id=fixture_policy.policy_authority_id,
                policy_authority_version=fixture_policy.policy_authority_version,
                policy_authority_revision=fixture_policy.policy_authority_revision,
                owner_policy=fixture_policy.owner_policy,
                human_result_ref=human_result_ref,
                human_gate_ref=human_gate_ref,
                human_result_authority_revision=human_result_authority_revision,
                command_center_action_ref=command_center_action_ref,
                reason_code=reason_code,
                authority_revision=(
                    authority_revision
                    if authority_revision is not None
                    else base.authority_revision
                ),
                supersedes_judgment_ref=supersedes_judgment_ref,
            )
            value = replace(provisional, fingerprint=_judgment_fingerprint(provisional))
            proposal = _judgment_proposal_fingerprint(
                judgment_version=value.judgment_version,
                request=fixture_request,
                policy=fixture_policy,
                human_result_ref=human_result_ref,
                evidence_attestation_ref=value.evidence_attestation_ref,
                command_center_action_ref=command_center_action_ref,
                reason_code=reason_code,
                reason_vocabulary_version=value.reason_vocabulary_version,
                supersedes_judgment_ref=supersedes_judgment_ref,
            )
            evaluation = JudgmentEvaluationRow(
                evaluation_id=evaluation_id,
                work_run_id=value.work_run_id,
                state_version=value.state_version,
                payload={
                    "policy": [
                        value.policy_id,
                        value.policy_version,
                        value.policy_fingerprint,
                        value.policy_authority_revision,
                    ],
                    "human_result_ref": human_result_ref,
                    "evidence_attestation_ref": value.evidence_attestation_ref,
                    "command_center_action_ref": command_center_action_ref,
                    "outcome": "COMPLETE",
                },
                evaluated_at=value.issued_at,
            )
            event = JudgmentAuthorityEventRow(
                event_id=f"corrupt-judgment-event-{fixture_id}",
                judgment_id=fixture_id,
                event_kind="ISSUED",
                prior_revision=value.authority_revision - 1,
                new_revision=value.authority_revision,
                payload={"evaluation_ref": evaluation_id},
                created_at=value.issued_at,
            )
            return value, evaluation, _judgment_row(value, proposal), event

        async def replay_corrupt_judgment(
            value: Any,
            fixture_request: TransitionRequest,
            fixture_policy: Any,
        ) -> Any:
            return await judgment_authority.issue(
                judgment_id=value.judgment_id,
                judgment_version=value.judgment_version,
                request=fixture_request,
                policy=fixture_policy,
                human_result_ref=value.human_result_ref,
                evidence_attestation_ref=value.evidence_attestation_ref,
                command_center_action_ref=value.command_center_action_ref,
                reason_code=value.reason_code,
                reason_vocabulary_version=value.reason_vocabulary_version,
                supersedes_judgment_ref=value.supersedes_judgment_ref,
            )

        def corrupt_correction_pair(
            fixture_id: str,
        ) -> tuple[
            tuple[Any, JudgmentEvaluationRow, JudgmentRow, JudgmentAuthorityEventRow],
            tuple[Any, JudgmentEvaluationRow, JudgmentRow, JudgmentAuthorityEventRow],
            JudgmentAuthorityEventRow,
        ]:
            predecessor = corrupt_judgment_fixture(
                f"{fixture_id}-predecessor",
                base=identity,
                fixture_request=system_request,
                fixture_policy=system_policy,
                human_result_ref=None,
                human_gate_ref=None,
                human_result_authority_revision=None,
                command_center_action_ref=None,
                reason_code=f"{fixture_id.upper()}_PREDECESSOR",
                authority_revision=1,
            )
            replacement_ref = f"p1-7-judgment:v1:{fixture_id}-replacement"
            replacement = corrupt_judgment_fixture(
                f"{fixture_id}-replacement",
                base=identity,
                fixture_request=system_request,
                fixture_policy=system_policy,
                human_result_ref=None,
                human_gate_ref=None,
                human_result_authority_revision=None,
                command_center_action_ref=None,
                reason_code=f"{fixture_id.upper()}_REPLACEMENT",
                authority_revision=2,
                supersedes_judgment_ref=predecessor[0].serialized_ref,
            )
            relation = JudgmentAuthorityEventRow(
                event_id=f"corrupt-correction-relation-{fixture_id}",
                judgment_id=predecessor[0].judgment_id,
                event_kind="SUPERSEDED",
                prior_revision=1,
                new_revision=2,
                payload={"replacement_judgment_ref": replacement_ref},
                created_at=replacement[0].issued_at,
            )
            return predecessor, replacement, relation

        missing_predecessor_base = corrupt_correction_pair(f"missing-predecessor-base-{label}")
        async with sessions() as session, session.begin():
            await session.execute(text("SET LOCAL session_replication_role = replica"))
            predecessor, replacement, relation = missing_predecessor_base
            session.add(predecessor[2])
            await session.flush()
            session.add(predecessor[3])
            session.add_all((replacement[1], replacement[2]))
            await session.flush()
            session.add_all((replacement[3], relation))
        with pytest.raises(JudgmentAuthorityError, match="PROVENANCE_INCOMPLETE"):
            await replay_corrupt_judgment(
                missing_predecessor_base[1][0], system_request, system_policy
            )

        missing_replacement_base = corrupt_correction_pair(f"missing-replacement-base-{label}")
        async with sessions() as session, session.begin():
            predecessor, replacement, relation = missing_replacement_base
            session.add_all((predecessor[1], predecessor[2]))
            await session.flush()
            session.add(predecessor[3])
            session.add_all((replacement[1], replacement[2]))
            await session.flush()
            session.add(relation)
        with pytest.raises(JudgmentAuthorityError, match="PROVENANCE_INCOMPLETE"):
            await replay_corrupt_judgment(
                missing_replacement_base[0][0], system_request, system_policy
            )

        wrong_replacement = corrupt_correction_pair(f"wrong-replacement-{label}")
        wrong_replacement[2].payload = {
            "replacement_judgment_ref": f"p1-7-judgment:v1:wrong-{label}"
        }
        async with sessions() as session, session.begin():
            predecessor, replacement, relation = wrong_replacement
            session.add_all((predecessor[1], predecessor[2]))
            await session.flush()
            session.add(predecessor[3])
            session.add_all((replacement[1], replacement[2]))
            await session.flush()
            session.add_all((replacement[3], relation))
        with pytest.raises(JudgmentAuthorityError, match="AUTHORITY_CONFLICT"):
            await replay_corrupt_judgment(wrong_replacement[1][0], system_request, system_policy)

        wrong_revision = corrupt_correction_pair(f"wrong-revision-{label}")
        wrong_revision[2].new_revision = 3
        async with sessions() as session, session.begin():
            predecessor, replacement, relation = wrong_revision
            session.add_all((predecessor[1], predecessor[2]))
            await session.flush()
            session.add(predecessor[3])
            session.add_all((replacement[1], replacement[2]))
            await session.flush()
            session.add_all((replacement[3], relation))
        with pytest.raises(JudgmentAuthorityError, match="AUTHORITY_CONFLICT"):
            await replay_corrupt_judgment(wrong_revision[1][0], system_request, system_policy)

        cycle_a_ref = f"p1-7-judgment:v1:cycle-a-{label}"
        cycle_b_ref = f"p1-7-judgment:v1:cycle-b-{label}"
        cycle_a = corrupt_judgment_fixture(
            f"cycle-a-{label}",
            base=identity,
            fixture_request=system_request,
            fixture_policy=system_policy,
            human_result_ref=None,
            human_gate_ref=None,
            human_result_authority_revision=None,
            command_center_action_ref=None,
            reason_code="CORRECTION_CYCLE_A",
            authority_revision=2,
            supersedes_judgment_ref=cycle_b_ref,
        )
        cycle_b = corrupt_judgment_fixture(
            f"cycle-b-{label}",
            base=identity,
            fixture_request=system_request,
            fixture_policy=system_policy,
            human_result_ref=None,
            human_gate_ref=None,
            human_result_authority_revision=None,
            command_center_action_ref=None,
            reason_code="CORRECTION_CYCLE_B",
            authority_revision=1,
            supersedes_judgment_ref=cycle_a_ref,
        )
        cycle_a_relation = JudgmentAuthorityEventRow(
            event_id=f"cycle-a-relation-{label}",
            judgment_id=cycle_a[0].judgment_id,
            event_kind="SUPERSEDED",
            prior_revision=2,
            new_revision=1,
            payload={"replacement_judgment_ref": cycle_b_ref},
            created_at=cycle_b[0].issued_at,
        )
        cycle_b_relation = JudgmentAuthorityEventRow(
            event_id=f"cycle-b-relation-{label}",
            judgment_id=cycle_b[0].judgment_id,
            event_kind="SUPERSEDED",
            prior_revision=1,
            new_revision=2,
            payload={"replacement_judgment_ref": cycle_a_ref},
            created_at=cycle_a[0].issued_at,
        )
        async with sessions() as session, session.begin():
            session.add_all((cycle_a[1], cycle_a[2], cycle_b[1], cycle_b[2]))
            await session.flush()
            session.add_all(
                (
                    cycle_a[3],
                    cycle_b[3],
                    cycle_a_relation,
                    cycle_b_relation,
                )
            )
        with pytest.raises(JudgmentAuthorityError, match="AUTHORITY_CONFLICT"):
            await replay_corrupt_judgment(cycle_a[0], system_request, system_policy)

        missing_evaluation = corrupt_judgment_fixture(
            f"missing-evaluation-{label}",
            base=identity,
            fixture_request=system_request,
            fixture_policy=system_policy,
            human_result_ref=None,
            human_gate_ref=None,
            human_result_authority_revision=None,
            command_center_action_ref=None,
            reason_code="MISSING_EVALUATION",
        )
        async with sessions() as session, session.begin():
            await session.execute(text("SET LOCAL session_replication_role = replica"))
            session.add(missing_evaluation[2])
        judgment_replay_counts = await _judgment_counts(sessions, system_run)
        with pytest.raises(JudgmentAuthorityError, match="PROVENANCE_INCOMPLETE"):
            await replay_corrupt_judgment(missing_evaluation[0], system_request, system_policy)
        assert await _judgment_counts(sessions, system_run) == judgment_replay_counts

        missing_issued = corrupt_judgment_fixture(
            f"missing-issued-{label}",
            base=identity,
            fixture_request=system_request,
            fixture_policy=system_policy,
            human_result_ref=None,
            human_gate_ref=None,
            human_result_authority_revision=None,
            command_center_action_ref=None,
            reason_code="MISSING_ISSUED",
        )
        async with sessions() as session, session.begin():
            session.add_all((missing_issued[1], missing_issued[2]))
        judgment_replay_counts = await _judgment_counts(sessions, system_run)
        with pytest.raises(JudgmentAuthorityError, match="PROVENANCE_INCOMPLETE"):
            await replay_corrupt_judgment(missing_issued[0], system_request, system_policy)
        assert await _judgment_counts(sessions, system_run) == judgment_replay_counts

        wrong_issued = corrupt_judgment_fixture(
            f"wrong-issued-{label}",
            base=identity,
            fixture_request=system_request,
            fixture_policy=system_policy,
            human_result_ref=None,
            human_gate_ref=None,
            human_result_authority_revision=None,
            command_center_action_ref=None,
            reason_code="WRONG_ISSUED",
        )
        wrong_issued[3].payload = {"evaluation_ref": "wrong-evaluation-ref"}
        async with sessions() as session, session.begin():
            session.add_all((wrong_issued[1], wrong_issued[2]))
            await session.flush()
            session.add(wrong_issued[3])
        with pytest.raises(JudgmentAuthorityError, match="AUTHORITY_CONFLICT"):
            await replay_corrupt_judgment(wrong_issued[0], system_request, system_policy)

        missing_policy = replace(
            system_policy,
            policy_id=f"missing-policy-{label}",
            fingerprint="",
        )
        missing_policy = replace(missing_policy, fingerprint=_policy_fingerprint(missing_policy))
        missing_policy_judgment = corrupt_judgment_fixture(
            f"missing-policy-judgment-{label}",
            base=identity,
            fixture_request=system_request,
            fixture_policy=missing_policy,
            human_result_ref=None,
            human_gate_ref=None,
            human_result_authority_revision=None,
            command_center_action_ref=None,
            reason_code="MISSING_POLICY",
        )
        async with sessions() as session, session.begin():
            session.add_all(missing_policy_judgment[1:3])
            await session.flush()
            session.add(missing_policy_judgment[3])
        with pytest.raises(JudgmentAuthorityError, match="PROVENANCE_INCOMPLETE"):
            await replay_corrupt_judgment(
                missing_policy_judgment[0], system_request, missing_policy
            )

        corrupt_human_dependency = corrupt_judgment_fixture(
            f"corrupt-human-dependency-{label}",
            base=human_judgment,
            fixture_request=human_judgment_request,
            fixture_policy=human_policy,
            human_result_ref=missing_result.serialized_ref,
            human_gate_ref=missing_result.human_gate_ref,
            human_result_authority_revision=missing_result.result_authority_revision,
            command_center_action_ref=None,
            reason_code="CORRUPT_HUMAN_DEPENDENCY",
        )
        async with sessions() as session, session.begin():
            session.add_all(corrupt_human_dependency[1:3])
            await session.flush()
            session.add(corrupt_human_dependency[3])
        with pytest.raises(JudgmentAuthorityError, match="PROVENANCE_INCOMPLETE"):
            await replay_corrupt_judgment(
                corrupt_human_dependency[0], human_judgment_request, human_policy
            )

        missing_command_center_dependency = corrupt_judgment_fixture(
            f"missing-command-center-dependency-{label}",
            base=cc_judgment,
            fixture_request=cc_request,
            fixture_policy=cc_policy,
            human_result_ref=None,
            human_gate_ref=None,
            human_result_authority_revision=None,
            command_center_action_ref=f"p1-7-command-center-action:v1:missing-{label}",
            reason_code="MISSING_COMMAND_CENTER_DEPENDENCY",
        )
        async with sessions() as session, session.begin():
            session.add_all(missing_command_center_dependency[1:3])
            await session.flush()
            session.add(missing_command_center_dependency[3])
        with pytest.raises(JudgmentAuthorityError, match="PROVENANCE_INCOMPLETE"):
            await replay_corrupt_judgment(
                missing_command_center_dependency[0], cc_request, cc_policy
            )

        await engine.dispose()

    run(scenario())


async def _row_count(sessions: Any, row_type: Any) -> int:
    async with sessions() as session:
        value = await session.scalar(select(func.count()).select_from(row_type))
        return int(value or 0)


async def _object_id_count(sessions: Any, row_type: Any, column_name: str, object_id: str) -> int:
    async with sessions() as session:
        value = await session.scalar(
            select(func.count())
            .select_from(row_type)
            .where(getattr(row_type, column_name) == object_id)
        )
        return int(value or 0)


async def _wait_for_advisory_wait(sessions: Any) -> None:
    for _ in range(500):
        async with sessions() as session:
            waiting = await session.scalar(
                text(
                    "SELECT count(*) FROM pg_stat_activity "
                    "WHERE datname = current_database() "
                    "AND wait_event = 'advisory' "
                    "AND query LIKE '%pg_advisory_xact_lock%'"
                )
            )
        if int(waiting or 0) > 0:
            return
        await asyncio.sleep(0.01)
    raise AssertionError("operation did not reach the deterministic PostgreSQL advisory-lock wait")


async def _judgment_counts(sessions: Any, work_run_id: str) -> tuple[int, int, int, int]:
    async with sessions() as session:
        judgments = await session.scalar(
            select(func.count())
            .select_from(JudgmentRow)
            .where(JudgmentRow.work_run_id == work_run_id)
        )
        evaluations = await session.scalar(
            select(func.count())
            .select_from(JudgmentEvaluationRow)
            .where(JudgmentEvaluationRow.work_run_id == work_run_id)
        )
        events = await session.scalar(select(func.count()).select_from(JudgmentAuthorityEventRow))
        projection = await session.get(JudgmentProjectionRow, work_run_id)
        return (
            int(judgments or 0),
            int(evaluations or 0),
            int(events or 0),
            projection.authority_revision if projection is not None else 0,
        )


async def _expiry_event_count(sessions: Any, human_gate_id: str) -> int:
    async with sessions() as session:
        value = await session.scalar(
            select(func.count())
            .select_from(HumanGateAuthorityEventRow)
            .where(
                HumanGateAuthorityEventRow.human_gate_id == human_gate_id,
                HumanGateAuthorityEventRow.event_kind == "EXPIRED",
            )
        )
        return int(value or 0)
