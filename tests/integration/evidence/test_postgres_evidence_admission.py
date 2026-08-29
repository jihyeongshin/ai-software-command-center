from __future__ import annotations

import asyncio
import hashlib
import os
from collections.abc import Coroutine
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

import aiscc.evidence.repository as evidence_repository_module
import aiscc.persistence.repository as workflow_repository_module
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.evidence.admission import (
    EVIDENCE_AUTHORITY_VERSION,
    EvidenceAdmissionEvaluator,
    EvidenceContentRegistry,
    make_admission_request,
)
from aiscc.evidence.attestation import EvidenceCheckpointUseRegistry, EvidenceGuardAuthority
from aiscc.evidence.content import PrivateEvidenceContentStore
from aiscc.evidence.issuers import (
    AuthenticatedHumanPrincipal,
    AuthenticatedHumanPrincipalAuthority,
    EvidenceIssuerRegistry,
    HumanDirectEvidenceIngressAuthority,
    P1_5EvidenceIssuerAuthority,
    PriorAdmittedEvidenceIssuerAuthority,
    TokenEvidenceIssuer,
)
from aiscc.evidence.models import (
    AdmittedEvidenceRef,
    EvidenceAdmissionOutcome,
    EvidenceAuthorityConflictError,
    EvidenceAuthorityEventKind,
    EvidenceCandidate,
    EvidenceCheckpoint,
    EvidenceCheckpointRef,
    EvidenceContentKind,
    EvidenceIdentityConflictError,
    EvidenceIssuerType,
    EvidenceOwner,
    EvidenceRejectionReason,
    EvidenceRequirement,
    EvidenceRequirementProfile,
    EvidenceRequirementRef,
    EvidenceRequirementSet,
    EvidenceSemanticOwner,
    EvidenceSensitivity,
    EvidenceSetOutcome,
    FreshnessPolicy,
    FreshnessPolicyKind,
    HumanEvidenceProducerCategory,
    RequirementObligation,
)
from aiscc.evidence.repository import PostgresEvidenceRepository
from aiscc.evidence.requirements import TaskContractEvidenceAuthority
from aiscc.evidence.service import EvidenceAdmissionService
from aiscc.evidence.set_evaluator import EvidenceSetEvaluator
from aiscc.persistence import (
    PostgresExecutionRepository,
    PostgresTransitionRepository,
    create_engine,
    create_session_factory,
)
from aiscc.persistence.models import WorkRunRow
from aiscc.workflow.evaluator import TransitionEvaluator
from aiscc.workflow.guards import (
    GUARD_OWNER_POLICY,
    FutureOwnerGuardVerifier,
    P1_4GuardAuthority,
    TrustedGuardFact,
    required_bound_refs,
)
from aiscc.workflow.kernel import WorkflowKernel
from aiscc.workflow.matrix import TRANSITION_MATRIX
from aiscc.workflow.models import (
    DecisionOutcome,
    GuardId,
    GuardSemanticOwner,
    RequesterType,
    TransitionRequest,
)

NOW = datetime(2026, 8, 29, 5, 0, tzinfo=UTC)
DEFAULT_FRESHNESS = FreshnessPolicy(FreshnessPolicyKind.WORKRUN_STATE_VERSION_SCOPED)


def run[T](coroutine: Coroutine[Any, Any, T]) -> T:
    return asyncio.run(coroutine)


@pytest.fixture(scope="module")
def database_url() -> str:
    value = os.environ.get("AISCC_TEST_DATABASE_URL")
    if not value:
        pytest.skip("AISCC_TEST_DATABASE_URL is required for PostgreSQL evidence")
    return value


class FutureAuthority:
    def __init__(self, owner: GuardSemanticOwner) -> None:
        self._owner = owner
        self._token = object()

    @property
    def semantic_owner(self) -> GuardSemanticOwner:
        return self._owner

    def recognizes(self, fact: TrustedGuardFact, request: TransitionRequest) -> bool:
        del request
        return fact._issuer_token is self._token

    def issue(self, guard_id: GuardId, request: TransitionRequest) -> TrustedGuardFact:
        return TrustedGuardFact(
            guard_id,
            self.semantic_owner,
            True,
            "TEST_OWNER_AUTHORITY",
            f"test:{self.semantic_owner.value}",
            required_bound_refs(guard_id, request),
            request.task_contract_id,
            request.task_contract_version,
            request.work_run_id,
            request.observed_state_version,
            self._token,
        )


class WorkflowAuthorities:
    def __init__(self) -> None:
        self.system = P1_4GuardAuthority()
        self.human = FutureAuthority(GuardSemanticOwner.P1_7_HUMAN)
        self.judgment = FutureAuthority(GuardSemanticOwner.P1_7_JUDGMENT)

    @property
    def future(self) -> tuple[FutureOwnerGuardVerifier, ...]:
        return self.human, self.judgment

    def facts(self, request: TransitionRequest) -> tuple[TrustedGuardFact, ...]:
        required = TRANSITION_MATRIX[(request.observed_state, request.target_state)]
        result: list[TrustedGuardFact] = []
        for guard in sorted(required, key=str):
            owner = GUARD_OWNER_POLICY[guard]
            if owner is GuardSemanticOwner.P1_4_SYSTEM:
                result.append(
                    self.system.issue(
                        guard_id=guard,
                        satisfied=True,
                        reason="TEST_SYSTEM_AUTHORITY",
                        authority_ref=f"test:{guard.value}",
                        request=request,
                    )
                )
            elif owner is GuardSemanticOwner.P1_7_HUMAN:
                result.append(self.human.issue(guard, request))
            elif owner is GuardSemanticOwner.P1_7_JUDGMENT:
                result.append(self.judgment.issue(guard, request))
            else:
                raise AssertionError("test lifecycle does not mint P1-6 evidence")
        return tuple(result)


def transition_request(
    *,
    run_id: str,
    task_id: str,
    source: WorkflowState | None,
    version: int,
    target: WorkflowState,
    evidence_refs: tuple[str, ...] = (),
) -> TransitionRequest:
    return TransitionRequest(
        str(uuid4()),
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
    )


async def move_to(
    kernel: WorkflowKernel,
    authorities: WorkflowAuthorities,
    *,
    run_id: str,
    task_id: str,
    target: WorkflowState,
) -> None:
    steps = [
        (None, 0, WorkflowState.READY),
        (WorkflowState.READY, 1, WorkflowState.RUNNING),
        (WorkflowState.RUNNING, 2, WorkflowState.ADMISSION_PENDING),
    ]
    if target is WorkflowState.HUMAN_REQUIRED:
        steps.append((WorkflowState.ADMISSION_PENDING, 3, WorkflowState.HUMAN_REQUIRED))
    for source, version, next_state in steps:
        request = transition_request(
            run_id=run_id,
            task_id=task_id,
            source=source,
            version=version,
            target=next_state,
        )
        decision = await kernel.request_transition(request, authorities.facts(request))
        assert decision.outcome is DecisionOutcome.ADMITTED
        if next_state is target:
            break


def requirement(
    *,
    task_id: str,
    set_id: str,
    requirement_id: str,
    profile: EvidenceRequirementProfile,
    checkpoints: tuple[str, ...],
    issuer_types: frozenset[EvidenceIssuerType],
    issuer_ids: frozenset[str],
    content_kinds: frozenset[EvidenceContentKind],
    human_categories: frozenset[HumanEvidenceProducerCategory] = frozenset(),
    freshness: FreshnessPolicy = DEFAULT_FRESHNESS,
    reuse_maximum: int = 1,
    reuse_compatible: frozenset[str] = frozenset(),
) -> EvidenceRequirement:
    obligation = {
        EvidenceRequirementProfile.EXECUTOR_REQUIRED: RequirementObligation.REQUIRED,
        EvidenceRequirementProfile.REUSE_ALLOWED: RequirementObligation.REQUIRED,
        EvidenceRequirementProfile.HUMAN_OWNED: RequirementObligation.REQUIRED,
        EvidenceRequirementProfile.NOT_REQUIRED: RequirementObligation.NOT_REQUIRED,
        EvidenceRequirementProfile.FORBIDDEN: RequirementObligation.FORBIDDEN,
    }[profile]
    return EvidenceRequirement(
        EvidenceRequirementRef(f"{task_id}:{requirement_id}", "v1"),
        task_id,
        "v1",
        set_id,
        "v1",
        EvidenceSemanticOwner.P1_6_EVIDENCE,
        profile,
        obligation,
        checkpoints,
        "AISCC_PROOF",
        "v1",
        issuer_types,
        issuer_ids,
        human_categories,
        content_kinds,
        "AISCC-PROOF",
        "v1",
        "aiscc-source",
        "repository",
        "repo@commit",
        freshness,
        frozenset({"result"}),
        reuse_maximum,
        reuse_compatible,
        EvidenceSensitivity.INTERNAL,
        False,
        NOW,
        "",
    )


def seal_snapshot(
    *,
    task_id: str,
    set_id: str,
    requirements: tuple[EvidenceRequirement, ...],
    checkpoints: tuple[EvidenceCheckpoint, ...],
) -> tuple[
    TaskContractEvidenceAuthority,
    EvidenceRequirementSet,
    tuple[EvidenceRequirement, ...],
    tuple[EvidenceCheckpoint, ...],
]:
    authority = TaskContractEvidenceAuthority(f"{task_id}-authority", "v1")
    sealed_requirements = tuple(authority.seal_requirement(item) for item in requirements)
    sealed_checkpoints = tuple(authority.seal_checkpoint(item) for item in checkpoints)
    requirement_set = authority.seal_set(
        EvidenceRequirementSet(
            set_id,
            "v1",
            task_id,
            "v1",
            tuple(item.ref.serialized() for item in sealed_requirements),
            "",
            tuple(item.ref.serialized() for item in sealed_checkpoints),
            EvidenceSemanticOwner.P1_6_EVIDENCE,
            EVIDENCE_AUTHORITY_VERSION,
            NOW,
            "",
        ),
        sealed_requirements,
        sealed_checkpoints,
    )
    return authority, requirement_set, sealed_requirements, sealed_checkpoints


def checkpoint(
    *,
    task_id: str,
    set_id: str,
    checkpoint_id: str,
    source: WorkflowState,
    target: WorkflowState | None = WorkflowState.ACCEPTED,
    purpose: str | None = None,
) -> EvidenceCheckpoint:
    return EvidenceCheckpoint(
        EvidenceCheckpointRef(f"{task_id}:{checkpoint_id}", "v1"),
        task_id,
        "v1",
        source,
        target,
        purpose,
        "v1" if purpose else None,
        set_id,
        "v1",
        f"{task_id}-authority",
        "v1",
        NOW,
    )


def system_candidate(
    *,
    candidate_id: str,
    run_id: str,
    checkpoint: EvidenceCheckpoint,
    state_version: int,
    store: PrivateEvidenceContentStore,
    issuer: TokenEvidenceIssuer,
) -> EvidenceCandidate:
    content = store.put_structured(
        object_id=f"body-{candidate_id}",
        object_version="v1",
        value={"result": "PASS"},
        kind=EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY,
        schema_id="AISCC-PROOF",
        schema_version="v1",
        sensitivity=EvidenceSensitivity.INTERNAL,
    )
    return issuer.issue(
        EvidenceCandidate(
            candidate_id,
            "v1",
            "",
            EvidenceOwner(
                EvidenceIssuerType.SYSTEM_STATIC_PROOF,
                "STATIC_ISSUER",
                "v1",
                "STATIC_ISSUER@v1",
            ),
            run_id,
            None,
            None,
            checkpoint.task_contract_id,
            "v1",
            checkpoint.ref,
            checkpoint.source_state,
            state_version,
            "aiscc-source",
            "repository",
            "repo@commit",
            "AISCC_PROOF",
            "v1",
            content,
            NOW,
            NOW,
            frozenset({"result"}),
            "system-proof-attestation",
        )
    )


def admission_request(
    *,
    request_id: str,
    candidate: EvidenceCandidate,
    requirement: EvidenceRequirement,
    requirement_set: EvidenceRequirementSet,
    checkpoint: EvidenceCheckpoint,
    run_id: str,
    state_version: int,
) -> Any:
    return make_admission_request(
        admission_request_id=request_id,
        candidate=candidate,
        requirement=requirement,
        requirement_set=requirement_set,
        checkpoint=checkpoint,
        work_run_id=run_id,
        observed_state=checkpoint.source_state,
        observed_state_version=state_version,
        requester_identity="aiscc-system",
        created_at=NOW,
    )


@pytest.mark.postgres
def test_durable_admission_concurrency_checkpoint_revocation_and_p1_4_handoff(
    database_url: str,
) -> None:
    async def scenario() -> None:
        task_id = f"task-evidence-{uuid4()}"
        set_id = f"set-evidence-{uuid4()}"
        run_id = f"run-evidence-{uuid4()}"
        engine = create_engine(database_url)
        sessions = create_session_factory(engine)
        workflow_authorities = WorkflowAuthorities()
        workflow_repository = PostgresTransitionRepository(
            sessions,
            TransitionEvaluator(workflow_authorities.system, workflow_authorities.future),
        )
        kernel = WorkflowKernel(workflow_repository)
        await move_to(
            kernel,
            workflow_authorities,
            run_id=run_id,
            task_id=task_id,
            target=WorkflowState.ADMISSION_PENDING,
        )
        pre = checkpoint(
            task_id=task_id,
            set_id=set_id,
            checkpoint_id="pre-human",
            source=WorkflowState.ADMISSION_PENDING,
        )
        same_state_other_use = checkpoint(
            task_id=task_id,
            set_id=set_id,
            checkpoint_id="same-state-other-use",
            source=WorkflowState.ADMISSION_PENDING,
            target=None,
            purpose="AUDIT_ONLY",
        )
        post = checkpoint(
            task_id=task_id,
            set_id=set_id,
            checkpoint_id="post-human",
            source=WorkflowState.HUMAN_REQUIRED,
        )
        static = requirement(
            task_id=task_id,
            set_id=set_id,
            requirement_id="static-proof",
            profile=EvidenceRequirementProfile.EXECUTOR_REQUIRED,
            checkpoints=(pre.ref.serialized(), same_state_other_use.ref.serialized()),
            issuer_types=frozenset({EvidenceIssuerType.SYSTEM_STATIC_PROOF}),
            issuer_ids=frozenset({"STATIC_ISSUER"}),
            content_kinds=frozenset({EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY}),
        )
        human = requirement(
            task_id=task_id,
            set_id=set_id,
            requirement_id="human-final",
            profile=EvidenceRequirementProfile.HUMAN_OWNED,
            checkpoints=(post.ref.serialized(),),
            issuer_types=frozenset({EvidenceIssuerType.HUMAN_DIRECT_EVIDENCE}),
            issuer_ids=frozenset({"HUMAN_INGRESS"}),
            content_kinds=frozenset({EvidenceContentKind.HUMAN_STRUCTURED_REF}),
            human_categories=frozenset({HumanEvidenceProducerCategory.HUMAN_DIRECT_EVIDENCE}),
        )
        not_required = requirement(
            task_id=task_id,
            set_id=set_id,
            requirement_id="supplemental",
            profile=EvidenceRequirementProfile.NOT_REQUIRED,
            checkpoints=(pre.ref.serialized(),),
            issuer_types=frozenset({EvidenceIssuerType.SYSTEM_STATIC_PROOF}),
            issuer_ids=frozenset({"STATIC_ISSUER"}),
            content_kinds=frozenset({EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY}),
        )
        forbidden = requirement(
            task_id=task_id,
            set_id=set_id,
            requirement_id="secret-forbidden",
            profile=EvidenceRequirementProfile.FORBIDDEN,
            checkpoints=(pre.ref.serialized(), post.ref.serialized()),
            issuer_types=frozenset({EvidenceIssuerType.SYSTEM_STATIC_PROOF}),
            issuer_ids=frozenset({"STATIC_ISSUER"}),
            content_kinds=frozenset({EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY}),
        )
        authority, requirement_set, requirements, checkpoints = seal_snapshot(
            task_id=task_id,
            set_id=set_id,
            requirements=(static, human, not_required, forbidden),
            checkpoints=(pre, same_state_other_use, post),
        )
        static, _, _, _ = requirements
        pre, same_state_other_use, _ = checkpoints
        repository = PostgresEvidenceRepository(sessions)
        await repository.register_authority(
            requirement_set=requirement_set,
            requirements=requirements,
            checkpoints=checkpoints,
            authority=authority,
        )
        shadow_set_id = f"shadow-{set_id}"
        shadow_checkpoint = checkpoint(
            task_id=task_id,
            set_id=shadow_set_id,
            checkpoint_id="shadow-use",
            source=WorkflowState.ADMISSION_PENDING,
            target=None,
            purpose="SHADOW_ONLY",
        )
        shadow_requirement = requirement(
            task_id=task_id,
            set_id=shadow_set_id,
            requirement_id="shadow-proof",
            profile=EvidenceRequirementProfile.EXECUTOR_REQUIRED,
            checkpoints=(shadow_checkpoint.ref.serialized(),),
            issuer_types=frozenset({EvidenceIssuerType.SYSTEM_STATIC_PROOF}),
            issuer_ids=frozenset({"STATIC_ISSUER"}),
            content_kinds=frozenset({EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY}),
        )
        shadow_authority, shadow_set, shadow_requirements, shadow_checkpoints = seal_snapshot(
            task_id=task_id,
            set_id=shadow_set_id,
            requirements=(shadow_requirement,),
            checkpoints=(shadow_checkpoint,),
        )
        with pytest.raises(EvidenceAuthorityConflictError, match="explicitly supersede"):
            await repository.register_authority(
                requirement_set=shadow_set,
                requirements=shadow_requirements,
                checkpoints=shadow_checkpoints,
                authority=shadow_authority,
            )
        baseline_admitted = (await repository.counts())["admitted"]
        store = PrivateEvidenceContentStore(f"private-store-{run_id}", "v1")
        issuer = TokenEvidenceIssuer(EvidenceIssuerType.SYSTEM_STATIC_PROOF, "STATIC_ISSUER", "v1")
        evaluator = EvidenceAdmissionEvaluator(
            EvidenceIssuerRegistry((issuer,)), EvidenceContentRegistry((store,))
        )
        service = EvidenceAdmissionService(repository, evaluator)
        candidate = system_candidate(
            candidate_id=f"candidate-{uuid4()}",
            run_id=run_id,
            checkpoint=pre,
            state_version=3,
            store=store,
            issuer=issuer,
        )
        first_request = admission_request(
            request_id=f"admission-{uuid4()}",
            candidate=candidate,
            requirement=static,
            requirement_set=requirement_set,
            checkpoint=pre,
            run_id=run_id,
            state_version=3,
        )
        first_decision, first_admitted = await service.submit(first_request, candidate, now=NOW)
        assert first_decision.outcome is EvidenceAdmissionOutcome.ADMITTED
        assert first_admitted is not None
        with pytest.raises(DBAPIError, match="append-only"):
            async with engine.begin() as connection:
                await connection.execute(
                    text(
                        "UPDATE evidence_candidates SET content_hash = :hash "
                        "WHERE candidate_id = :candidate_id"
                    ),
                    {"hash": "0" * 64, "candidate_id": candidate.candidate_id},
                )
        same_decision, same_admitted = await EvidenceAdmissionService(
            PostgresEvidenceRepository(sessions), evaluator
        ).submit(first_request, candidate, now=NOW)
        assert same_decision == first_decision
        assert same_admitted == first_admitted
        conflict = replace(first_request, request_fingerprint="0" * 64)
        with pytest.raises(EvidenceIdentityConflictError):
            await service.submit(conflict, candidate, now=NOW)

        concurrent_requests = tuple(
            admission_request(
                request_id=f"admission-concurrent-{uuid4()}",
                candidate=candidate,
                requirement=static,
                requirement_set=requirement_set,
                checkpoint=pre,
                run_id=run_id,
                state_version=3,
            )
            for _ in range(4)
        )
        concurrent_results = await asyncio.gather(
            *(service.submit(item, candidate, now=NOW) for item in concurrent_requests)
        )
        assert all(
            item[0].outcome is EvidenceAdmissionOutcome.ADMITTED for item in concurrent_results
        )
        assert {item[1].admitted_evidence_id for item in concurrent_results if item[1]} == {
            first_admitted.admitted_evidence_id
        }
        assert (await repository.counts())["admitted"] == baseline_admitted + 1

        set_evaluator = EvidenceSetEvaluator(repository)
        wrong_evaluation, wrong_attestation = await set_evaluator.evaluate(
            work_run_id=run_id,
            checkpoint_ref=same_state_other_use.ref,
            source_state=WorkflowState.ADMISSION_PENDING,
            state_version=3,
            now=NOW,
        )
        assert wrong_evaluation.outcome is EvidenceSetOutcome.UNSATISFIED
        assert wrong_attestation is None
        other_use_candidate = system_candidate(
            candidate_id=f"other-use-{uuid4()}",
            run_id=run_id,
            checkpoint=same_state_other_use,
            state_version=3,
            store=store,
            issuer=issuer,
        )
        other_use_request = admission_request(
            request_id=f"other-use-admission-{uuid4()}",
            candidate=other_use_candidate,
            requirement=static,
            requirement_set=requirement_set,
            checkpoint=same_state_other_use,
            run_id=run_id,
            state_version=3,
        )
        other_decision, other_admitted = await service.submit(
            other_use_request, other_use_candidate, now=NOW
        )
        assert other_decision.outcome is EvidenceAdmissionOutcome.ADMITTED
        assert other_admitted is not None
        other_evaluation, other_attestation = await set_evaluator.evaluate(
            work_run_id=run_id,
            checkpoint_ref=same_state_other_use.ref,
            source_state=WorkflowState.ADMISSION_PENDING,
            state_version=3,
            now=NOW,
        )
        assert other_evaluation.outcome is EvidenceSetOutcome.SATISFIED
        assert other_attestation is not None
        wrong_transition_use = transition_request(
            run_id=run_id,
            task_id=task_id,
            source=WorkflowState.ADMISSION_PENDING,
            version=3,
            target=WorkflowState.ACCEPTED,
            evidence_refs=(other_attestation.serialized_ref,),
        )
        with pytest.raises(ValueError, match="exact transition authority"):
            await EvidenceGuardAuthority(
                repository, EvidenceCheckpointUseRegistry(checkpoints)
            ).issue_for_transition(wrong_transition_use)
        evaluation, attestation = await set_evaluator.evaluate(
            work_run_id=run_id,
            checkpoint_ref=pre.ref,
            source_state=WorkflowState.ADMISSION_PENDING,
            state_version=3,
            now=NOW,
        )
        assert evaluation.outcome is EvidenceSetOutcome.SATISFIED
        assert attestation is not None

        supplemental = system_candidate(
            candidate_id=f"supplemental-{uuid4()}",
            run_id=run_id,
            checkpoint=pre,
            state_version=3,
            store=store,
            issuer=issuer,
        )
        before = await repository.counts()
        await service.preserve_supplemental(supplemental)
        after = await repository.counts()
        assert after["candidates"] == before["candidates"] + 1
        assert after["admitted"] == before["admitted"]
        unchanged, unchanged_attestation = await set_evaluator.evaluate(
            work_run_id=run_id,
            checkpoint_ref=pre.ref,
            source_state=WorkflowState.ADMISSION_PENDING,
            state_version=3,
            now=NOW,
        )
        assert unchanged.admitted_ref_root_hash == evaluation.admitted_ref_root_hash
        assert unchanged_attestation is not None
        assert unchanged_attestation.attestation_id == attestation.attestation_id

        first_ref = AdmittedEvidenceRef(
            first_admitted.admitted_evidence_id, EVIDENCE_AUTHORITY_VERSION
        ).serialized()
        corrected = system_candidate(
            candidate_id=f"corrected-{uuid4()}",
            run_id=run_id,
            checkpoint=pre,
            state_version=3,
            store=store,
            issuer=issuer,
        )
        corrected_request = admission_request(
            request_id=f"corrected-admission-{uuid4()}",
            candidate=corrected,
            requirement=static,
            requirement_set=requirement_set,
            checkpoint=pre,
            run_id=run_id,
            state_version=3,
        )
        corrected_decision, corrected_admitted = await service.submit(
            corrected_request, corrected, now=NOW
        )
        assert corrected_decision.outcome is EvidenceAdmissionOutcome.ADMITTED
        assert corrected_admitted is not None
        corrected_ref = AdmittedEvidenceRef(
            corrected_admitted.admitted_evidence_id, EVIDENCE_AUTHORITY_VERSION
        ).serialized()
        await service.invalidate_authority(
            subject_ref=first_ref,
            reason="TEST_CORRECTION",
            replacement_ref=corrected_ref,
            kind=EvidenceAuthorityEventKind.CORRECTED,
        )
        async with engine.connect() as connection:
            event = (
                (
                    await connection.execute(
                        text(
                            "SELECT event_kind, owner_id, task_contract_id, work_run_id, "
                            "affected_refs, affected_mappings "
                            "FROM evidence_authority_events WHERE subject_ref = :subject_ref"
                        ),
                        {"subject_ref": first_ref},
                    )
                )
                .mappings()
                .one()
            )
        assert event["event_kind"] == EvidenceAuthorityEventKind.CORRECTED.value
        assert event["owner_id"] == "AISCC_P1_6_EVIDENCE_AUTHORITY_V1"
        assert event["task_contract_id"] == task_id
        assert event["work_run_id"] == run_id
        assert event["affected_refs"] == [first_ref, corrected_ref]
        assert event["affected_mappings"]
        fresh_repository = PostgresEvidenceRepository(sessions)
        assert await fresh_repository.load_effective_attestation(attestation.serialized_ref) is None
        assert await fresh_repository.load_admitted(first_ref) is None
        assert await fresh_repository.load_admitted(corrected_ref) is not None
        corrected_eval, corrected_attestation = await EvidenceSetEvaluator(
            fresh_repository
        ).evaluate(
            work_run_id=run_id,
            checkpoint_ref=pre.ref,
            source_state=WorkflowState.ADMISSION_PENDING,
            state_version=3,
            now=NOW,
        )
        assert corrected_eval.outcome is EvidenceSetOutcome.SATISFIED
        assert corrected_attestation is not None
        assert (
            corrected_attestation.evidence_authority_revision
            > attestation.evidence_authority_revision
        )

        evidence_guard = EvidenceGuardAuthority(
            fresh_repository, EvidenceCheckpointUseRegistry(checkpoints)
        )
        accept_request = transition_request(
            run_id=run_id,
            task_id=task_id,
            source=WorkflowState.ADMISSION_PENDING,
            version=3,
            target=WorkflowState.ACCEPTED,
            evidence_refs=(corrected_attestation.serialized_ref,),
        )
        evidence_fact = await evidence_guard.issue_for_transition(accept_request)
        human_fact = workflow_authorities.human.issue(GuardId.G_HUMAN_NOT_REQUIRED, accept_request)
        judgment_fact = workflow_authorities.judgment.issue(
            GuardId.G_JUDGMENT_ACCEPTED, accept_request
        )
        final_kernel = WorkflowKernel(
            PostgresTransitionRepository(
                sessions,
                TransitionEvaluator(
                    workflow_authorities.system,
                    (evidence_guard, *workflow_authorities.future),
                ),
            )
        )
        final_decision = await final_kernel.request_transition(
            accept_request, (evidence_fact, human_fact, judgment_fact)
        )
        assert final_decision.outcome is DecisionOutcome.ADMITTED
        await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_human_checkpoint_non_deadlock_and_authenticated_direct_ingress(
    database_url: str,
) -> None:
    async def scenario() -> None:
        task_id = f"task-human-evidence-{uuid4()}"
        set_id = f"set-human-evidence-{uuid4()}"
        run_id = f"run-human-evidence-{uuid4()}"
        engine = create_engine(database_url)
        sessions = create_session_factory(engine)
        workflow_authorities = WorkflowAuthorities()
        kernel = WorkflowKernel(
            PostgresTransitionRepository(
                sessions,
                TransitionEvaluator(workflow_authorities.system, workflow_authorities.future),
            )
        )
        await move_to(
            kernel,
            workflow_authorities,
            run_id=run_id,
            task_id=task_id,
            target=WorkflowState.HUMAN_REQUIRED,
        )
        post = checkpoint(
            task_id=task_id,
            set_id=set_id,
            checkpoint_id="post-human",
            source=WorkflowState.HUMAN_REQUIRED,
        )
        p1_7_only_checkpoint = checkpoint(
            task_id=task_id,
            set_id=set_id,
            checkpoint_id="p1-7-only",
            source=WorkflowState.HUMAN_REQUIRED,
            target=None,
            purpose="P1_7_ONLY_TEST",
        )
        static = requirement(
            task_id=task_id,
            set_id=set_id,
            requirement_id="static-proof",
            profile=EvidenceRequirementProfile.EXECUTOR_REQUIRED,
            checkpoints=(post.ref.serialized(),),
            issuer_types=frozenset({EvidenceIssuerType.SYSTEM_STATIC_PROOF}),
            issuer_ids=frozenset({"STATIC_ISSUER"}),
            content_kinds=frozenset({EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY}),
        )
        human = requirement(
            task_id=task_id,
            set_id=set_id,
            requirement_id="human-final",
            profile=EvidenceRequirementProfile.HUMAN_OWNED,
            checkpoints=(post.ref.serialized(),),
            issuer_types=frozenset({EvidenceIssuerType.HUMAN_DIRECT_EVIDENCE}),
            issuer_ids=frozenset({"HUMAN_INGRESS"}),
            content_kinds=frozenset({EvidenceContentKind.HUMAN_STRUCTURED_REF}),
            human_categories=frozenset({HumanEvidenceProducerCategory.HUMAN_DIRECT_EVIDENCE}),
        )
        p1_7_only = requirement(
            task_id=task_id,
            set_id=set_id,
            requirement_id="human-p1-7-only",
            profile=EvidenceRequirementProfile.HUMAN_OWNED,
            checkpoints=(p1_7_only_checkpoint.ref.serialized(),),
            issuer_types=frozenset({EvidenceIssuerType.HUMAN_DIRECT_EVIDENCE}),
            issuer_ids=frozenset({"HUMAN_INGRESS"}),
            content_kinds=frozenset({EvidenceContentKind.HUMAN_STRUCTURED_REF}),
            human_categories=frozenset({HumanEvidenceProducerCategory.HUMAN_P1_7}),
        )
        authority, requirement_set, requirements, checkpoints = seal_snapshot(
            task_id=task_id,
            set_id=set_id,
            requirements=(static, human, p1_7_only),
            checkpoints=(post, p1_7_only_checkpoint),
        )
        static, human, p1_7_only = requirements
        post, p1_7_only_checkpoint = checkpoints
        repository = PostgresEvidenceRepository(sessions)
        await repository.register_authority(
            requirement_set=requirement_set,
            requirements=requirements,
            checkpoints=checkpoints,
            authority=authority,
        )
        store = PrivateEvidenceContentStore(f"human-store-{run_id}", "v1")
        static_issuer = TokenEvidenceIssuer(
            EvidenceIssuerType.SYSTEM_STATIC_PROOF, "STATIC_ISSUER", "v1"
        )
        principal_authority = AuthenticatedHumanPrincipalAuthority("HUMAN_AUTHN", "v1")
        ingress = HumanDirectEvidenceIngressAuthority(
            "HUMAN_INGRESS", "v1", principal_authority, repository
        )
        evaluator = EvidenceAdmissionEvaluator(
            EvidenceIssuerRegistry((static_issuer, ingress)),
            EvidenceContentRegistry((store,)),
        )
        service = EvidenceAdmissionService(repository, evaluator)
        static_candidate_value = system_candidate(
            candidate_id=f"human-run-static-{uuid4()}",
            run_id=run_id,
            checkpoint=post,
            state_version=4,
            store=store,
            issuer=static_issuer,
        )
        static_request = admission_request(
            request_id=f"human-run-static-request-{uuid4()}",
            candidate=static_candidate_value,
            requirement=static,
            requirement_set=requirement_set,
            checkpoint=post,
            run_id=run_id,
            state_version=4,
        )
        static_decision, _ = await service.submit(static_request, static_candidate_value, now=NOW)
        assert static_decision.outcome is EvidenceAdmissionOutcome.ADMITTED
        incomplete, no_attestation = await EvidenceSetEvaluator(repository).evaluate(
            work_run_id=run_id,
            checkpoint_ref=post.ref,
            source_state=WorkflowState.HUMAN_REQUIRED,
            state_version=4,
            now=NOW,
        )
        assert incomplete.outcome is EvidenceSetOutcome.UNSATISFIED
        assert no_attestation is None

        human_content = store.put_structured(
            object_id=f"human-body-{uuid4()}",
            object_version="v1",
            value={"result": "HUMAN_PROVIDED"},
            kind=EvidenceContentKind.HUMAN_STRUCTURED_REF,
            schema_id="AISCC-PROOF",
            schema_version="v1",
            sensitivity=EvidenceSensitivity.INTERNAL,
        )
        unissued = EvidenceCandidate(
            f"human-direct-{uuid4()}",
            "v1",
            "",
            EvidenceOwner(
                EvidenceIssuerType.HUMAN_DIRECT_EVIDENCE,
                "HUMAN_INGRESS",
                "v1",
                "HUMAN_INGRESS@v1",
            ),
            run_id,
            None,
            None,
            task_id,
            "v1",
            post.ref,
            WorkflowState.HUMAN_REQUIRED,
            4,
            "aiscc-source",
            "repository",
            "repo@commit",
            "AISCC_PROOF",
            "v1",
            human_content,
            NOW,
            NOW,
            frozenset({"result"}),
            "",
            HumanEvidenceProducerCategory.HUMAN_DIRECT_EVIDENCE,
        )
        forged = AuthenticatedHumanPrincipal(
            "human:forged",
            "session",
            NOW,
            "HUMAN_AUTHN",
            "v1",
            object(),
        )
        with pytest.raises(ValueError, match="not authenticated"):
            await ingress.issue(
                unissued,
                forged,
                ingress_idempotency_key="human-ingress-record-forged",
            )
        principal = principal_authority.authenticate("human:operator", "session-1", NOW)
        ingress_idempotency_key = f"human-ingress-record-{uuid4()}"
        human_candidate = await ingress.issue(
            unissued,
            principal,
            ingress_idempotency_key=ingress_idempotency_key,
        )
        same_candidate = await ingress.issue(
            unissued,
            principal,
            ingress_idempotency_key=ingress_idempotency_key,
        )
        assert same_candidate == human_candidate
        with pytest.raises(EvidenceIdentityConflictError, match="Human ingress identity conflict"):
            await ingress.issue(
                replace(unissued, candidate_id=f"conflicting-human-{uuid4()}"),
                principal,
                ingress_idempotency_key=ingress_idempotency_key,
            )
        forged_ref_candidate = replace(
            unissued,
            human_ingress_record_ref=("p1-6-human-ingress:v1:caller-crafted:" + "0" * 64),
        )
        assert not await ingress.recognizes(forged_ref_candidate)
        human_request = admission_request(
            request_id=f"human-direct-request-{uuid4()}",
            candidate=human_candidate,
            requirement=human,
            requirement_set=requirement_set,
            checkpoint=post,
            run_id=run_id,
            state_version=4,
        )
        human_decision, human_admitted = await service.submit(
            human_request, human_candidate, now=NOW
        )
        assert human_decision.outcome is EvidenceAdmissionOutcome.ADMITTED
        assert human_admitted is not None
        fresh_ingress = HumanDirectEvidenceIngressAuthority(
            "HUMAN_INGRESS",
            "v1",
            AuthenticatedHumanPrincipalAuthority("HUMAN_AUTHN", "v1"),
            PostgresEvidenceRepository(sessions),
        )
        assert await fresh_ingress.recognizes(human_candidate)
        assert human_candidate.human_ingress_record_ref is not None
        durable_ingress = await PostgresEvidenceRepository(sessions).load_human_ingress(
            human_candidate.human_ingress_record_ref
        )
        assert durable_ingress is not None
        assert durable_ingress.authenticated_principal_id == "human:operator"
        with pytest.raises(DBAPIError, match="append-only"):
            async with engine.begin() as connection:
                await connection.execute(
                    text(
                        "UPDATE human_direct_evidence_ingress "
                        "SET authenticated_principal_id = 'forged' "
                        "WHERE ingress_record_id = :record_id"
                    ),
                    {"record_id": durable_ingress.ref.ingress_record_id},
                )
        p1_7_unissued = replace(
            unissued,
            candidate_id=f"human-direct-against-p1-7-{uuid4()}",
            checkpoint_ref=p1_7_only_checkpoint.ref,
            producer_attestation_ref="",
            human_ingress_record_ref=None,
        )
        p1_7_candidate = await ingress.issue(
            p1_7_unissued,
            principal,
            ingress_idempotency_key=f"human-p1-7-mismatch-{uuid4()}",
        )
        p1_7_request = admission_request(
            request_id=f"human-p1-7-mismatch-request-{uuid4()}",
            candidate=p1_7_candidate,
            requirement=p1_7_only,
            requirement_set=requirement_set,
            checkpoint=p1_7_only_checkpoint,
            run_id=run_id,
            state_version=4,
        )
        p1_7_decision, p1_7_admitted = await service.submit(p1_7_request, p1_7_candidate, now=NOW)
        assert p1_7_decision.outcome is EvidenceAdmissionOutcome.REJECTED
        assert EvidenceRejectionReason.HUMAN_PRODUCER_CATEGORY_MISMATCH in (
            p1_7_decision.reason,
            *p1_7_decision.secondary_reasons,
        )
        assert p1_7_admitted is None
        complete, attestation = await EvidenceSetEvaluator(
            PostgresEvidenceRepository(sessions)
        ).evaluate(
            work_run_id=run_id,
            checkpoint_ref=post.ref,
            source_state=WorkflowState.HUMAN_REQUIRED,
            state_version=4,
            now=NOW,
        )
        assert complete.outcome is EvidenceSetOutcome.SATISFIED
        assert attestation is not None
        await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_authority_revision_invalidates_every_contributing_authority_after_restart(
    database_url: str,
) -> None:
    async def scenario() -> None:
        engine = create_engine(database_url)
        sessions = create_session_factory(engine)

        async def prepare(label: str) -> dict[str, Any]:
            task_id = f"task-authority-{label}-{uuid4()}"
            set_id = f"set-authority-{label}-{uuid4()}"
            run_id = f"run-authority-{label}-{uuid4()}"
            workflow_authorities = WorkflowAuthorities()
            kernel = WorkflowKernel(
                PostgresTransitionRepository(
                    sessions,
                    TransitionEvaluator(workflow_authorities.system, workflow_authorities.future),
                )
            )
            await move_to(
                kernel,
                workflow_authorities,
                run_id=run_id,
                task_id=task_id,
                target=WorkflowState.ADMISSION_PENDING,
            )
            current_checkpoint = checkpoint(
                task_id=task_id,
                set_id=set_id,
                checkpoint_id="pre-human",
                source=WorkflowState.ADMISSION_PENDING,
            )
            current_requirement = requirement(
                task_id=task_id,
                set_id=set_id,
                requirement_id="static-proof",
                profile=EvidenceRequirementProfile.EXECUTOR_REQUIRED,
                checkpoints=(current_checkpoint.ref.serialized(),),
                issuer_types=frozenset({EvidenceIssuerType.SYSTEM_STATIC_PROOF}),
                issuer_ids=frozenset({"STATIC_ISSUER"}),
                content_kinds=frozenset({EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY}),
            )
            authority, current_set, requirements, checkpoints = seal_snapshot(
                task_id=task_id,
                set_id=set_id,
                requirements=(current_requirement,),
                checkpoints=(current_checkpoint,),
            )
            current_requirement = requirements[0]
            current_checkpoint = checkpoints[0]
            repository = PostgresEvidenceRepository(sessions)
            await repository.register_authority(
                requirement_set=current_set,
                requirements=requirements,
                checkpoints=checkpoints,
                authority=authority,
            )
            store = PrivateEvidenceContentStore(f"authority-store-{run_id}", "v1")
            issuer = TokenEvidenceIssuer(
                EvidenceIssuerType.SYSTEM_STATIC_PROOF, "STATIC_ISSUER", "v1"
            )
            evaluator = EvidenceAdmissionEvaluator(
                EvidenceIssuerRegistry((issuer,)), EvidenceContentRegistry((store,))
            )
            service = EvidenceAdmissionService(repository, evaluator)
            candidate = system_candidate(
                candidate_id=f"authority-candidate-{uuid4()}",
                run_id=run_id,
                checkpoint=current_checkpoint,
                state_version=3,
                store=store,
                issuer=issuer,
            )
            request = admission_request(
                request_id=f"authority-request-{uuid4()}",
                candidate=candidate,
                requirement=current_requirement,
                requirement_set=current_set,
                checkpoint=current_checkpoint,
                run_id=run_id,
                state_version=3,
            )
            decision, admitted = await service.submit(request, candidate, now=NOW)
            assert decision.outcome is EvidenceAdmissionOutcome.ADMITTED
            assert admitted is not None
            evaluation, attestation = await EvidenceSetEvaluator(repository).evaluate(
                work_run_id=run_id,
                checkpoint_ref=current_checkpoint.ref,
                source_state=WorkflowState.ADMISSION_PENDING,
                state_version=3,
                now=NOW,
            )
            assert evaluation.outcome is EvidenceSetOutcome.SATISFIED
            assert attestation is not None
            return {
                "task_id": task_id,
                "set": current_set,
                "requirement": current_requirement,
                "checkpoint": current_checkpoint,
                "run_id": run_id,
                "repository": repository,
                "service": service,
                "store": store,
                "issuer": issuer,
                "admitted": admitted,
                "attestation": attestation,
            }

        for subject_kind in ("admitted", "requirement", "checkpoint"):
            context = await prepare(subject_kind)
            admitted = context["admitted"]
            requirement_value = context["requirement"]
            checkpoint_value = context["checkpoint"]
            attestation = context["attestation"]
            if subject_kind == "admitted":
                subject_ref = AdmittedEvidenceRef(
                    admitted.admitted_evidence_id, EVIDENCE_AUTHORITY_VERSION
                ).serialized()
            elif subject_kind == "requirement":
                subject_ref = requirement_value.ref.serialized()
            else:
                subject_ref = checkpoint_value.ref.serialized()
            await context["service"].invalidate_authority(
                subject_ref=subject_ref,
                reason=f"TEST_{subject_kind.upper()}_REVOKED",
            )
            fresh_repository = PostgresEvidenceRepository(sessions)
            assert (
                await fresh_repository.load_effective_attestation(attestation.serialized_ref)
                is None
            )
            old_request = transition_request(
                run_id=context["run_id"],
                task_id=context["task_id"],
                source=WorkflowState.ADMISSION_PENDING,
                version=3,
                target=WorkflowState.ACCEPTED,
                evidence_refs=(attestation.serialized_ref,),
            )
            with pytest.raises(ValueError, match="exact transition authority"):
                await EvidenceGuardAuthority(
                    fresh_repository,
                    EvidenceCheckpointUseRegistry((checkpoint_value,)),
                ).issue_for_transition(old_request)

        context = await prepare("requirement-set")
        old_set = context["set"]
        old_attestation = context["attestation"]
        task_id = context["task_id"]
        run_id = context["run_id"]
        new_set_id = f"set-authority-replacement-{uuid4()}"
        new_checkpoint = checkpoint(
            task_id=task_id,
            set_id=new_set_id,
            checkpoint_id="pre-human-replacement",
            source=WorkflowState.ADMISSION_PENDING,
        )
        new_requirement = requirement(
            task_id=task_id,
            set_id=new_set_id,
            requirement_id="static-proof-replacement",
            profile=EvidenceRequirementProfile.EXECUTOR_REQUIRED,
            checkpoints=(new_checkpoint.ref.serialized(),),
            issuer_types=frozenset({EvidenceIssuerType.SYSTEM_STATIC_PROOF}),
            issuer_ids=frozenset({"STATIC_ISSUER"}),
            content_kinds=frozenset({EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY}),
        )
        replacement_authority = TaskContractEvidenceAuthority(f"{task_id}-authority", "v1")
        replacement_requirements = (replacement_authority.seal_requirement(new_requirement),)
        replacement_checkpoints = (replacement_authority.seal_checkpoint(new_checkpoint),)
        replacement_set = replacement_authority.seal_set(
            EvidenceRequirementSet(
                new_set_id,
                "v1",
                task_id,
                "v1",
                tuple(item.ref.serialized() for item in replacement_requirements),
                "",
                tuple(item.ref.serialized() for item in replacement_checkpoints),
                EvidenceSemanticOwner.P1_6_EVIDENCE,
                EVIDENCE_AUTHORITY_VERSION,
                NOW + timedelta(seconds=1),
                "",
                supersedes_set_ref=(
                    f"{old_set.requirement_set_id}@{old_set.requirement_set_version}"
                ),
            ),
            replacement_requirements,
            replacement_checkpoints,
        )
        await context["repository"].register_authority(
            requirement_set=replacement_set,
            requirements=replacement_requirements,
            checkpoints=replacement_checkpoints,
            authority=replacement_authority,
        )
        fresh_repository = PostgresEvidenceRepository(sessions)
        assert (
            await fresh_repository.load_effective_attestation(old_attestation.serialized_ref)
            is None
        )
        replacement_evaluation, replacement_attestation = await EvidenceSetEvaluator(
            fresh_repository
        ).evaluate(
            work_run_id=run_id,
            checkpoint_ref=replacement_checkpoints[0].ref,
            source_state=WorkflowState.ADMISSION_PENDING,
            state_version=3,
            now=NOW + timedelta(seconds=1),
        )
        assert replacement_evaluation.outcome is EvidenceSetOutcome.UNSATISFIED
        assert replacement_attestation is None
        replacement_candidate = system_candidate(
            candidate_id=f"replacement-candidate-{uuid4()}",
            run_id=run_id,
            checkpoint=replacement_checkpoints[0],
            state_version=3,
            store=context["store"],
            issuer=context["issuer"],
        )
        replacement_request = admission_request(
            request_id=f"replacement-request-{uuid4()}",
            candidate=replacement_candidate,
            requirement=replacement_requirements[0],
            requirement_set=replacement_set,
            checkpoint=replacement_checkpoints[0],
            run_id=run_id,
            state_version=3,
        )
        replacement_decision, replacement_admitted = await EvidenceAdmissionService(
            fresh_repository,
            EvidenceAdmissionEvaluator(
                EvidenceIssuerRegistry((context["issuer"],)),
                EvidenceContentRegistry((context["store"],)),
            ),
        ).submit(replacement_request, replacement_candidate, now=NOW + timedelta(seconds=1))
        assert replacement_decision.outcome is EvidenceAdmissionOutcome.ADMITTED
        assert replacement_admitted is not None
        satisfied, new_attestation = await EvidenceSetEvaluator(fresh_repository).evaluate(
            work_run_id=run_id,
            checkpoint_ref=replacement_checkpoints[0].ref,
            source_state=WorkflowState.ADMISSION_PENDING,
            state_version=3,
            now=NOW + timedelta(seconds=1),
        )
        assert satisfied.outcome is EvidenceSetOutcome.SATISFIED
        assert new_attestation is not None
        assert (
            new_attestation.evidence_authority_revision
            > old_attestation.evidence_authority_revision
        )
        await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_finite_reuse_maximum_is_durable_concurrent_and_restart_safe(
    database_url: str,
) -> None:
    async def scenario() -> None:
        task_id = f"task-reuse-limit-{uuid4()}"
        set_id = f"set-reuse-limit-{uuid4()}"
        run_id = f"run-reuse-limit-{uuid4()}"
        engine = create_engine(database_url)
        sessions = create_session_factory(engine)
        workflow_authorities = WorkflowAuthorities()
        kernel = WorkflowKernel(
            PostgresTransitionRepository(
                sessions,
                TransitionEvaluator(workflow_authorities.system, workflow_authorities.future),
            )
        )
        await move_to(
            kernel,
            workflow_authorities,
            run_id=run_id,
            task_id=task_id,
            target=WorkflowState.ADMISSION_PENDING,
        )
        pre = checkpoint(
            task_id=task_id,
            set_id=set_id,
            checkpoint_id="pre-human",
            source=WorkflowState.ADMISSION_PENDING,
        )
        prior_requirement = requirement(
            task_id=task_id,
            set_id=set_id,
            requirement_id="prior-static",
            profile=EvidenceRequirementProfile.EXECUTOR_REQUIRED,
            checkpoints=(pre.ref.serialized(),),
            issuer_types=frozenset({EvidenceIssuerType.SYSTEM_STATIC_PROOF}),
            issuer_ids=frozenset({"STATIC_ISSUER"}),
            content_kinds=frozenset({EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY}),
        )
        prior_requirement_ref = prior_requirement.ref.serialized()

        def reuse_requirement(name: str, maximum: int) -> EvidenceRequirement:
            return requirement(
                task_id=task_id,
                set_id=set_id,
                requirement_id=name,
                profile=EvidenceRequirementProfile.REUSE_ALLOWED,
                checkpoints=(pre.ref.serialized(),),
                issuer_types=frozenset({EvidenceIssuerType.PRIOR_ADMITTED_EVIDENCE}),
                issuer_ids=frozenset({"AISCC_P1_6_REUSE_AUTHORITY_V1"}),
                content_kinds=frozenset({EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY}),
                reuse_maximum=maximum,
                reuse_compatible=frozenset({prior_requirement_ref}),
            )

        zero = reuse_requirement("reuse-zero", 0)
        one = reuse_requirement("reuse-one", 1)
        two = reuse_requirement("reuse-two", 2)
        authority, requirement_set, requirements, checkpoints = seal_snapshot(
            task_id=task_id,
            set_id=set_id,
            requirements=(prior_requirement, zero, one, two),
            checkpoints=(pre,),
        )
        prior_requirement, zero, one, two = requirements
        pre = checkpoints[0]
        repository = PostgresEvidenceRepository(sessions)
        await repository.register_authority(
            requirement_set=requirement_set,
            requirements=requirements,
            checkpoints=checkpoints,
            authority=authority,
        )
        baseline_reuse_consumptions = (await repository.counts())["reuse_consumptions"]
        store = PrivateEvidenceContentStore(f"reuse-store-{run_id}", "v1")
        static_issuer = TokenEvidenceIssuer(
            EvidenceIssuerType.SYSTEM_STATIC_PROOF, "STATIC_ISSUER", "v1"
        )
        static_evaluator = EvidenceAdmissionEvaluator(
            EvidenceIssuerRegistry((static_issuer,)), EvidenceContentRegistry((store,))
        )
        prior_candidate = system_candidate(
            candidate_id=f"prior-candidate-{uuid4()}",
            run_id=run_id,
            checkpoint=pre,
            state_version=3,
            store=store,
            issuer=static_issuer,
        )
        prior_request = admission_request(
            request_id=f"prior-request-{uuid4()}",
            candidate=prior_candidate,
            requirement=prior_requirement,
            requirement_set=requirement_set,
            checkpoint=pre,
            run_id=run_id,
            state_version=3,
        )
        prior_decision, prior_admitted = await EvidenceAdmissionService(
            repository, static_evaluator
        ).submit(prior_request, prior_candidate, now=NOW)
        assert prior_decision.outcome is EvidenceAdmissionOutcome.ADMITTED
        assert prior_admitted is not None
        prior_ref = AdmittedEvidenceRef(
            prior_admitted.admitted_evidence_id, EVIDENCE_AUTHORITY_VERSION
        ).serialized()

        reuse_issuer = PriorAdmittedEvidenceIssuerAuthority(repository)

        async def reusable_candidate(candidate_id: str) -> EvidenceCandidate:
            return await reuse_issuer.seed_candidate(
                EvidenceCandidate(
                    candidate_id,
                    "v1",
                    "",
                    EvidenceOwner(
                        EvidenceIssuerType.PRIOR_ADMITTED_EVIDENCE,
                        reuse_issuer.issuer_id,
                        reuse_issuer.issuer_version,
                        f"{reuse_issuer.issuer_id}@{reuse_issuer.issuer_version}",
                    ),
                    run_id,
                    None,
                    None,
                    task_id,
                    "v1",
                    pre.ref,
                    WorkflowState.ADMISSION_PENDING,
                    3,
                    "aiscc-source",
                    "repository",
                    "repo@commit",
                    "AISCC_PROOF",
                    "v1",
                    prior_admitted.content_ref,
                    NOW,
                    NOW,
                    frozenset({"result"}),
                    prior_ref,
                    prior_admitted_evidence_ref=prior_ref,
                )
            )

        reuse_evaluator = EvidenceAdmissionEvaluator(
            EvidenceIssuerRegistry((reuse_issuer,)), EvidenceContentRegistry((store,))
        )
        reuse_service = EvidenceAdmissionService(repository, reuse_evaluator)

        async def submit_reuse(
            candidate: EvidenceCandidate,
            governed_requirement: EvidenceRequirement,
            request_id: str,
        ) -> tuple[Any, Any]:
            request = admission_request(
                request_id=request_id,
                candidate=candidate,
                requirement=governed_requirement,
                requirement_set=requirement_set,
                checkpoint=pre,
                run_id=run_id,
                state_version=3,
            )
            return await reuse_service.submit(request, candidate, now=NOW)

        zero_candidate = await reusable_candidate(f"reuse-zero-{uuid4()}")
        zero_decision, zero_admitted = await submit_reuse(
            zero_candidate, zero, f"reuse-zero-request-{uuid4()}"
        )
        assert zero_decision.outcome is EvidenceAdmissionOutcome.REJECTED
        assert zero_admitted is None
        assert (await repository.counts())["reuse_consumptions"] == baseline_reuse_consumptions

        one_candidate = await reusable_candidate(f"reuse-one-first-{uuid4()}")
        one_request_id = f"reuse-one-request-{uuid4()}"
        one_decision, one_admitted = await submit_reuse(one_candidate, one, one_request_id)
        assert one_decision.outcome is EvidenceAdmissionOutcome.ADMITTED
        assert one_admitted is not None
        with pytest.raises(DBAPIError, match="append-only"):
            async with engine.begin() as connection:
                await connection.execute(
                    text(
                        "UPDATE evidence_reuse_consumptions SET policy_maximum = 99 "
                        "WHERE admitted_evidence_id = :admitted_id"
                    ),
                    {"admitted_id": one_admitted.admitted_evidence_id},
                )
        retry_decision, retry_admitted = await submit_reuse(one_candidate, one, one_request_id)
        assert retry_decision == one_decision
        assert retry_admitted == one_admitted
        second_one = await reusable_candidate(f"reuse-one-second-{uuid4()}")
        second_one_decision, second_one_admitted = await submit_reuse(
            second_one, one, f"reuse-one-second-request-{uuid4()}"
        )
        assert second_one_decision.outcome is EvidenceAdmissionOutcome.REJECTED
        assert second_one_admitted is None
        assert (await repository.counts())["reuse_consumptions"] == baseline_reuse_consumptions + 1

        first_two = await reusable_candidate(f"reuse-two-first-{uuid4()}")
        first_two_decision, first_two_admitted = await submit_reuse(
            first_two, two, f"reuse-two-first-request-{uuid4()}"
        )
        assert first_two_decision.outcome is EvidenceAdmissionOutcome.ADMITTED
        assert first_two_admitted is not None
        concurrent_candidates = (
            await reusable_candidate(f"reuse-two-concurrent-a-{uuid4()}"),
            await reusable_candidate(f"reuse-two-concurrent-b-{uuid4()}"),
        )
        concurrent_results = await asyncio.gather(
            *(
                submit_reuse(
                    candidate,
                    two,
                    f"reuse-two-concurrent-request-{uuid4()}",
                )
                for candidate in concurrent_candidates
            )
        )
        assert (
            sum(
                result[0].outcome is EvidenceAdmissionOutcome.ADMITTED
                for result in concurrent_results
            )
            == 1
        )
        assert sum(result[1] is not None for result in concurrent_results) == 1
        assert (await repository.counts())["reuse_consumptions"] == baseline_reuse_consumptions + 3

        fresh_repository = PostgresEvidenceRepository(sessions)
        fresh_reuse_issuer = PriorAdmittedEvidenceIssuerAuthority(fresh_repository)
        restart_candidate = await fresh_reuse_issuer.seed_candidate(
            replace(
                await reusable_candidate(f"reuse-two-restart-{uuid4()}"),
                _issuer_token=None,
            )
        )
        restart_evaluator = EvidenceAdmissionEvaluator(
            EvidenceIssuerRegistry((fresh_reuse_issuer,)),
            EvidenceContentRegistry((store,)),
        )
        restart_request = admission_request(
            request_id=f"reuse-two-restart-request-{uuid4()}",
            candidate=restart_candidate,
            requirement=two,
            requirement_set=requirement_set,
            checkpoint=pre,
            run_id=run_id,
            state_version=3,
        )
        restart_decision, restart_admitted = await EvidenceAdmissionService(
            fresh_repository, restart_evaluator
        ).submit(restart_request, restart_candidate, now=NOW)
        assert restart_decision.outcome is EvidenceAdmissionOutcome.REJECTED
        assert restart_admitted is None
        assert (await fresh_repository.counts())[
            "reuse_consumptions"
        ] == baseline_reuse_consumptions + 3

        incompatible_content = store.put_structured(
            object_id=f"incompatible-{uuid4()}",
            object_version="v1",
            value={"result": "DIFFERENT"},
            kind=EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY,
            schema_id="AISCC-PROOF",
            schema_version="v1",
            sensitivity=EvidenceSensitivity.INTERNAL,
        )
        with pytest.raises(ValueError, match="content differs"):
            await fresh_reuse_issuer.seed_candidate(
                replace(
                    restart_candidate,
                    candidate_id=f"incompatible-reuse-{uuid4()}",
                    content_ref=incompatible_content,
                    _issuer_token=None,
                )
            )
        assert (await fresh_repository.counts())[
            "reuse_consumptions"
        ] == baseline_reuse_consumptions + 3

        await EvidenceAdmissionService(fresh_repository, restart_evaluator).invalidate_authority(
            subject_ref=prior_ref,
            reason="TEST_PRIOR_REVOKED_AFTER_REUSE",
        )
        with pytest.raises(ValueError, match="unavailable or revoked"):
            await PriorAdmittedEvidenceIssuerAuthority(
                PostgresEvidenceRepository(sessions)
            ).seed_candidate(
                replace(
                    restart_candidate,
                    candidate_id=f"revoked-reuse-{uuid4()}",
                    _issuer_token=None,
                )
            )
        assert (await fresh_repository.counts())[
            "reuse_consumptions"
        ] == baseline_reuse_consumptions + 3
        await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_authoritative_workrun_freshness_missing_mismatch_race_and_restart(
    database_url: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    async def scenario() -> None:
        task_id = f"task-workrun-freshness-{uuid4()}"
        set_id = f"set-workrun-freshness-{uuid4()}"
        engine = create_engine(database_url)
        sessions = create_session_factory(engine)
        workflow_authorities = WorkflowAuthorities()
        workflow_repository = PostgresTransitionRepository(
            sessions,
            TransitionEvaluator(workflow_authorities.system, workflow_authorities.future),
        )
        kernel = WorkflowKernel(workflow_repository)
        pre = checkpoint(
            task_id=task_id,
            set_id=set_id,
            checkpoint_id="pre-human",
            source=WorkflowState.ADMISSION_PENDING,
        )
        static = requirement(
            task_id=task_id,
            set_id=set_id,
            requirement_id="static-proof",
            profile=EvidenceRequirementProfile.EXECUTOR_REQUIRED,
            checkpoints=(pre.ref.serialized(),),
            issuer_types=frozenset({EvidenceIssuerType.SYSTEM_STATIC_PROOF}),
            issuer_ids=frozenset({"STATIC_ISSUER"}),
            content_kinds=frozenset({EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY}),
        )
        authority, requirement_set, requirements, checkpoints = seal_snapshot(
            task_id=task_id,
            set_id=set_id,
            requirements=(static,),
            checkpoints=(pre,),
        )
        static = requirements[0]
        pre = checkpoints[0]
        repository = PostgresEvidenceRepository(sessions)
        await repository.register_authority(
            requirement_set=requirement_set,
            requirements=requirements,
            checkpoints=checkpoints,
            authority=authority,
        )
        store = PrivateEvidenceContentStore(f"workrun-store-{uuid4()}", "v1")
        issuer = TokenEvidenceIssuer(EvidenceIssuerType.SYSTEM_STATIC_PROOF, "STATIC_ISSUER", "v1")
        evaluator = EvidenceAdmissionEvaluator(
            EvidenceIssuerRegistry((issuer,)), EvidenceContentRegistry((store,))
        )
        service = EvidenceAdmissionService(repository, evaluator)

        async def seed_work_run(
            run_id: str,
            *,
            bound_task_id: str = task_id,
            bound_task_version: str = "v1",
            state: WorkflowState = WorkflowState.ADMISSION_PENDING,
            state_version: int = 3,
        ) -> None:
            async with sessions() as session, session.begin():
                session.add(
                    WorkRunRow(
                        work_run_id=run_id,
                        project_id="aiscc-project",
                        task_contract_id=bound_task_id,
                        task_contract_version=bound_task_version,
                        workflow_state=state.value,
                        state_version=state_version,
                        runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD.value,
                        created_at=NOW,
                        updated_at=NOW,
                    )
                )

        async def submit(
            label: str,
            run_id: str,
            *,
            state_version: int,
            current_service: EvidenceAdmissionService = service,
            current_store: PrivateEvidenceContentStore = store,
            current_issuer: TokenEvidenceIssuer = issuer,
        ) -> tuple[Any, Any, EvidenceCandidate]:
            candidate = system_candidate(
                candidate_id=f"candidate-{label}-{uuid4()}",
                run_id=run_id,
                checkpoint=pre,
                state_version=state_version,
                store=current_store,
                issuer=current_issuer,
            )
            request = admission_request(
                request_id=f"request-{label}-{uuid4()}",
                candidate=candidate,
                requirement=static,
                requirement_set=requirement_set,
                checkpoint=pre,
                run_id=run_id,
                state_version=state_version,
            )
            decision, admitted = await current_service.submit(request, candidate, now=NOW)
            return decision, admitted, candidate

        async def assert_no_authority_rows(candidate_id: str) -> None:
            async with sessions() as session:
                admitted_count = int(
                    await session.scalar(
                        text(
                            "SELECT count(*) FROM admitted_evidence "
                            "WHERE candidate_id = :candidate_id"
                        ),
                        {"candidate_id": candidate_id},
                    )
                    or 0
                )
                satisfaction_count = int(
                    await session.scalar(
                        text(
                            "SELECT count(*) FROM evidence_requirement_satisfactions s "
                            "JOIN admitted_evidence a ON "
                            "a.admitted_evidence_id = s.admitted_evidence_id "
                            "WHERE a.candidate_id = :candidate_id"
                        ),
                        {"candidate_id": candidate_id},
                    )
                    or 0
                )
                reuse_count = int(
                    await session.scalar(
                        text(
                            "SELECT count(*) FROM evidence_reuse_consumptions c "
                            "JOIN admitted_evidence a ON "
                            "a.admitted_evidence_id = c.admitted_evidence_id "
                            "WHERE a.candidate_id = :candidate_id"
                        ),
                        {"candidate_id": candidate_id},
                    )
                    or 0
                )
            assert (admitted_count, satisfaction_count, reuse_count) == (0, 0, 0)

        stale_run = f"run-stale-{uuid4()}"
        await seed_work_run(stale_run, state_version=4)
        stale, stale_admitted, stale_candidate = await submit(
            "self-consistent-v3-current-v4", stale_run, state_version=3
        )
        assert stale.outcome is EvidenceAdmissionOutcome.REJECTED
        assert stale.reason is EvidenceRejectionReason.STALE
        assert stale_admitted is None
        await assert_no_authority_rows(stale_candidate.candidate_id)
        async with sessions() as session:
            dimensions = await session.scalar(
                text(
                    "SELECT e.dimension_results FROM evidence_evaluations e "
                    "WHERE e.evaluation_id = :evaluation_id"
                ),
                {"evaluation_id": stale.evaluation_id},
            )
        assert isinstance(dimensions, list)
        freshness = next(item for item in dimensions if item["dimension"] == "FRESHNESS")
        assert freshness["outcome"] == "FAIL"
        assert freshness["authority_ref"] == f"AISCC_SYSTEM_WORKRUN:{stale_run}"
        assert freshness["authority_version"] == "state-version:4"

        current_run = f"run-current-{uuid4()}"
        await seed_work_run(current_run, state_version=4)
        current, current_admitted, _ = await submit(
            "self-consistent-v4-current-v4", current_run, state_version=4
        )
        assert current.outcome is EvidenceAdmissionOutcome.ADMITTED
        assert current_admitted is not None

        missing_run = f"run-missing-{uuid4()}"
        missing, missing_admitted, missing_candidate = await submit(
            "missing-workrun", missing_run, state_version=3
        )
        assert missing.outcome is EvidenceAdmissionOutcome.REJECTED
        assert missing.reason is EvidenceRejectionReason.AUTHORITY_CONFLICT
        assert missing_admitted is None
        await assert_no_authority_rows(missing_candidate.candidate_id)

        wrong_task_run = f"run-wrong-task-{uuid4()}"
        await seed_work_run(wrong_task_run, bound_task_id=f"other-{task_id}")
        wrong_task, no_wrong_task_admission, wrong_task_candidate = await submit(
            "wrong-task-id", wrong_task_run, state_version=3
        )
        assert wrong_task.reason is EvidenceRejectionReason.TASK_CONTRACT_MISMATCH
        assert no_wrong_task_admission is None
        await assert_no_authority_rows(wrong_task_candidate.candidate_id)

        wrong_version_run = f"run-wrong-version-{uuid4()}"
        await seed_work_run(wrong_version_run, bound_task_version="v2")
        wrong_version, no_wrong_version_admission, wrong_version_candidate = await submit(
            "wrong-task-version", wrong_version_run, state_version=3
        )
        assert wrong_version.reason is EvidenceRejectionReason.TASK_CONTRACT_MISMATCH
        assert no_wrong_version_admission is None
        await assert_no_authority_rows(wrong_version_candidate.candidate_id)

        wrong_state_run = f"run-wrong-state-{uuid4()}"
        await seed_work_run(wrong_state_run, state=WorkflowState.HUMAN_REQUIRED)
        wrong_state, no_wrong_state_admission, wrong_state_candidate = await submit(
            "wrong-state", wrong_state_run, state_version=3
        )
        assert wrong_state.reason is EvidenceRejectionReason.CHECKPOINT_MISMATCH
        assert no_wrong_state_admission is None
        await assert_no_authority_rows(wrong_state_candidate.candidate_id)

        restart_store = PrivateEvidenceContentStore(f"restart-store-{uuid4()}", "v1")
        restart_issuer = TokenEvidenceIssuer(
            EvidenceIssuerType.SYSTEM_STATIC_PROOF, "STATIC_ISSUER", "v1"
        )
        restart_service = EvidenceAdmissionService(
            PostgresEvidenceRepository(sessions),
            EvidenceAdmissionEvaluator(
                EvidenceIssuerRegistry((restart_issuer,)),
                EvidenceContentRegistry((restart_store,)),
            ),
        )
        restarted, no_restart_admission, restart_candidate = await submit(
            "restart-stale-v3-current-v4",
            stale_run,
            state_version=3,
            current_service=restart_service,
            current_store=restart_store,
            current_issuer=restart_issuer,
        )
        assert restarted.reason is EvidenceRejectionReason.STALE
        assert no_restart_admission is None
        await assert_no_authority_rows(restart_candidate.candidate_id)

        race_run = f"run-race-{uuid4()}"
        await move_to(
            kernel,
            workflow_authorities,
            run_id=race_run,
            task_id=task_id,
            target=WorkflowState.ADMISSION_PENDING,
        )
        race_candidate = system_candidate(
            candidate_id=f"candidate-race-{uuid4()}",
            run_id=race_run,
            checkpoint=pre,
            state_version=3,
            store=store,
            issuer=issuer,
        )
        race_request = admission_request(
            request_id=f"request-race-{uuid4()}",
            candidate=race_candidate,
            requirement=static,
            requirement_set=requirement_set,
            checkpoint=pre,
            run_id=race_run,
            state_version=3,
        )
        transition = transition_request(
            run_id=race_run,
            task_id=task_id,
            source=WorkflowState.ADMISSION_PENDING,
            version=3,
            target=WorkflowState.HUMAN_REQUIRED,
        )
        original_transition_lock = workflow_repository_module.acquire_work_run_transaction_lock
        original_admission_lock = evidence_repository_module._acquire_work_run_transaction_lock
        transition_has_lock = asyncio.Event()
        release_transition = asyncio.Event()
        admission_attempted_lock = asyncio.Event()

        async def hold_transition_lock(session: Any, work_run_id: str) -> None:
            await original_transition_lock(session, work_run_id)
            if work_run_id == race_run:
                transition_has_lock.set()
                await release_transition.wait()

        async def observe_admission_lock(session: Any, work_run_id: str) -> None:
            if work_run_id == race_run:
                admission_attempted_lock.set()
            await original_admission_lock(session, work_run_id)

        monkeypatch.setattr(
            workflow_repository_module,
            "acquire_work_run_transaction_lock",
            hold_transition_lock,
        )
        monkeypatch.setattr(
            evidence_repository_module,
            "_acquire_work_run_transaction_lock",
            observe_admission_lock,
        )
        transition_task = asyncio.create_task(
            kernel.request_transition(transition, workflow_authorities.facts(transition))
        )
        await asyncio.wait_for(transition_has_lock.wait(), timeout=5)
        admission_task = asyncio.create_task(service.submit(race_request, race_candidate, now=NOW))
        await asyncio.wait_for(admission_attempted_lock.wait(), timeout=5)
        release_transition.set()
        transition_result, admission_result = await asyncio.gather(transition_task, admission_task)
        race_decision, race_admitted = admission_result
        assert transition_result.outcome is DecisionOutcome.ADMITTED
        assert race_decision.outcome is EvidenceAdmissionOutcome.REJECTED
        assert race_decision.reason in {
            EvidenceRejectionReason.CHECKPOINT_MISMATCH,
            EvidenceRejectionReason.STALE,
        }
        assert race_admitted is None
        await assert_no_authority_rows(race_candidate.candidate_id)
        final_run = await kernel.load(race_run)
        assert final_run is not None
        assert (final_run.state, final_run.state_version) == (
            WorkflowState.HUMAN_REQUIRED,
            4,
        )

        async with sessions() as session:
            admitted_fk_count = int(
                await session.scalar(
                    text(
                        "SELECT count(*) FROM pg_constraint "
                        "WHERE conrelid = 'admitted_evidence'::regclass "
                        "AND confrelid = 'work_runs'::regclass "
                        "AND contype = 'f'"
                    )
                )
                or 0
            )
        assert admitted_fk_count >= 1
        await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_p1_5_immutable_ref_is_verified_candidate_input_not_admission(
    database_url: str,
) -> None:
    async def scenario() -> None:
        task_id = f"task-p1-5-ref-{uuid4()}"
        set_id = f"set-p1-5-ref-{uuid4()}"
        run_id = f"run-p1-5-ref-{uuid4()}"
        attempt_id = f"attempt-p1-5-ref-{uuid4()}"
        output_ref_id = f"agent-output-{uuid4()}"
        engine = create_engine(database_url)
        sessions = create_session_factory(engine)
        workflow_authorities = WorkflowAuthorities()
        workflow_repository = PostgresTransitionRepository(
            sessions,
            TransitionEvaluator(workflow_authorities.system, workflow_authorities.future),
        )
        kernel = WorkflowKernel(workflow_repository)
        ready_request = transition_request(
            run_id=run_id,
            task_id=task_id,
            source=None,
            version=0,
            target=WorkflowState.READY,
        )
        assert (
            await kernel.request_transition(
                ready_request, workflow_authorities.facts(ready_request)
            )
        ).outcome is DecisionOutcome.ADMITTED
        execution_repository = PostgresExecutionRepository(sessions)
        await execution_repository.create_attempt(
            attempt_id=attempt_id,
            work_run_id=run_id,
            profile_id="profile-local-fake",
            profile_version="v1",
            registry_id="registry-local-fake",
            registry_version="v1",
        )
        running_request = transition_request(
            run_id=run_id,
            task_id=task_id,
            source=WorkflowState.READY,
            version=1,
            target=WorkflowState.RUNNING,
        )
        assert (
            await kernel.request_transition(
                running_request, workflow_authorities.facts(running_request)
            )
        ).outcome is DecisionOutcome.ADMITTED
        await execution_repository.transition_attempt(attempt_id, "EXECUTION_STARTED")
        body = b'{"result":"P1_5_LOCAL_FAKE_OUTPUT"}'
        body_hash = hashlib.sha256(body).hexdigest()
        await execution_repository.store_output_ref(
            ref_id=output_ref_id,
            attempt_id=attempt_id,
            kind="AgentOutputRef",
            content_hash=body_hash,
            storage_ref=f"private://p1-5/{output_ref_id}",
        )
        admission_pending_request = transition_request(
            run_id=run_id,
            task_id=task_id,
            source=WorkflowState.RUNNING,
            version=2,
            target=WorkflowState.ADMISSION_PENDING,
        )
        assert (
            await kernel.request_transition(
                admission_pending_request,
                workflow_authorities.facts(admission_pending_request),
            )
        ).outcome is DecisionOutcome.ADMITTED

        pre = checkpoint(
            task_id=task_id,
            set_id=set_id,
            checkpoint_id="pre-human",
            source=WorkflowState.ADMISSION_PENDING,
        )
        producer_requirement = requirement(
            task_id=task_id,
            set_id=set_id,
            requirement_id="agent-output-proof",
            profile=EvidenceRequirementProfile.EXECUTOR_REQUIRED,
            checkpoints=(pre.ref.serialized(),),
            issuer_types=frozenset({EvidenceIssuerType.P1_5_AGENT_OUTPUT}),
            issuer_ids=frozenset({"P1_5_OUTPUT_AUTHORITY"}),
            content_kinds=frozenset({EvidenceContentKind.P1_5_IMMUTABLE_PRODUCER_REF}),
            freshness=FreshnessPolicy(FreshnessPolicyKind.TASK_EXECUTION_SCOPED),
        )
        authority, requirement_set, requirements, checkpoints = seal_snapshot(
            task_id=task_id,
            set_id=set_id,
            requirements=(producer_requirement,),
            checkpoints=(pre,),
        )
        producer_requirement = requirements[0]
        pre = checkpoints[0]
        repository = PostgresEvidenceRepository(sessions)
        await repository.register_authority(
            requirement_set=requirement_set,
            requirements=requirements,
            checkpoints=checkpoints,
            authority=authority,
        )
        baseline_admitted = (await repository.counts())["admitted"]
        store = PrivateEvidenceContentStore(f"p1-5-store-{run_id}", "v1")
        content = store.put_p1_5_producer_bytes(
            object_id=output_ref_id,
            object_version="v1",
            body=body,
            schema_id="AISCC-PROOF",
            schema_version="v1",
        )
        p1_5_issuer = P1_5EvidenceIssuerAuthority(
            EvidenceIssuerType.P1_5_AGENT_OUTPUT,
            "P1_5_OUTPUT_AUTHORITY",
            "v1",
            repository,
        )
        raw_candidate = EvidenceCandidate(
            f"p1-5-candidate-{uuid4()}",
            "v1",
            "",
            EvidenceOwner(
                EvidenceIssuerType.P1_5_AGENT_OUTPUT,
                "P1_5_OUTPUT_AUTHORITY",
                "v1",
                "P1_5_OUTPUT_AUTHORITY@v1",
            ),
            run_id,
            attempt_id,
            None,
            task_id,
            "v1",
            pre.ref,
            WorkflowState.RUNNING,
            2,
            "aiscc-source",
            "repository",
            "repo@commit",
            "AISCC_PROOF",
            "v1",
            content,
            NOW,
            NOW,
            frozenset({"result"}),
            output_ref_id,
        )
        evaluator = EvidenceAdmissionEvaluator(
            EvidenceIssuerRegistry((p1_5_issuer,)), EvidenceContentRegistry((store,))
        )
        service = EvidenceAdmissionService(repository, evaluator)
        raw_request = admission_request(
            request_id=f"raw-p1-5-request-{uuid4()}",
            candidate=raw_candidate,
            requirement=producer_requirement,
            requirement_set=requirement_set,
            checkpoint=pre,
            run_id=run_id,
            state_version=3,
        )
        raw_decision, raw_admitted = await service.submit(raw_request, raw_candidate, now=NOW)
        assert raw_decision.outcome is EvidenceAdmissionOutcome.REJECTED
        assert raw_admitted is None
        assert (await repository.counts())["admitted"] == baseline_admitted

        candidate = p1_5_issuer.seed_candidate(
            replace(raw_candidate, candidate_id=f"seeded-p1-5-candidate-{uuid4()}")
        )
        request = admission_request(
            request_id=f"seeded-p1-5-request-{uuid4()}",
            candidate=candidate,
            requirement=producer_requirement,
            requirement_set=requirement_set,
            checkpoint=pre,
            run_id=run_id,
            state_version=3,
        )
        decision, admitted = await service.submit(request, candidate, now=NOW)
        assert decision.outcome is EvidenceAdmissionOutcome.ADMITTED
        assert admitted is not None
        assert (await repository.counts())["admitted"] == baseline_admitted + 1
        await engine.dispose()

    run(scenario())
