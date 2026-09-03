from __future__ import annotations

import asyncio
import hashlib
import json
import os
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Coroutine
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

import pytest
from sqlalchemy import select, text

from aiscc.command_center.postgres_queries import PostgresCommandCenterQueries
from aiscc.command_center.queries import AuthorityConflictReadError, QueueFilters
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.evidence.repository import PostgresEvidenceRepository
from aiscc.human.models import HumanResultKind
from aiscc.judgment.authority import JudgmentPolicyAuthority, PostgresJudgmentAuthority
from aiscc.judgment.models import JudgmentKind, JudgmentOwnerPolicy
from aiscc.next_action.models import (
    NextActionProposal,
    NextActionSelectionMode,
    default_next_action_policy_authority,
)
from aiscc.next_action.repository import PostgresNextActionRepository
from aiscc.persistence import (
    PostgresTransitionRepository,
    create_engine,
    create_session_factory,
)
from aiscc.persistence.models import (
    AdmittedCycleRow,
    AdmittedEvidenceRow,
    CycleAdmissionDecisionRow,
    CycleAdmissionRequestRow,
    CycleAuthorityEventRow,
    CycleEvaluationRow,
    EvidenceAdmissionDecisionRow,
    EvidenceAdmissionRequestRow,
    EvidenceCandidateRow,
    EvidenceCheckpointRow,
    EvidenceEvaluationRow,
    EvidenceRequirementRow,
    EvidenceRequirementSatisfactionRow,
    EvidenceRequirementSetRow,
    EvidenceSetAttestationRow,
    EvidenceSetEvaluationRow,
    ExecutionAttemptRow,
    ExecutionEventRow,
    ExecutionOperationRow,
    ExecutionOutputRefRow,
    HumanGateAuthorityEventRow,
    HumanGateProjectionRow,
    HumanGateRow,
    HumanResultAuthorityEventRow,
    HumanResultRow,
    P1_4BlockerProvenanceRow,
    ProjectMemoryAuthorityEventRow,
    ProjectMemoryEntryRow,
    ProjectMemoryViewRow,
    WorkRunRow,
)
from aiscc.task_authority.authority import _bind_repository_once
from aiscc.task_authority.models import TaskConstraintScopeKind, TaskConstraintScopeV1
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository
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
    BlockerKindV1,
    BlockerReasonCodeV1,
    DecisionOutcome,
    GuardId,
    GuardSemanticOwner,
    P1_4BlockerClaimV1,
    RequesterType,
    TransitionDecision,
    TransitionRequest,
)

# Keep shared global NextAction catalog issuance aligned with the existing P1-8
# integration harness so test ordering cannot make earlier historical selections invalid.
NOW = datetime(2026, 8, 31, 8, 13, tzinfo=UTC)


def run[T](coroutine: Coroutine[Any, Any, T]) -> T:
    return asyncio.run(coroutine)


class _BlockerSourceVerifier:
    async def verify_resolution_source(self, session: Any, **values: Any) -> bool:
        del session, values
        return True


class _FutureAuthority:
    def __init__(self, semantic_owner: GuardSemanticOwner) -> None:
        self._semantic_owner = semantic_owner
        self._token = object()

    @property
    def semantic_owner(self) -> GuardSemanticOwner:
        return self._semantic_owner

    def recognizes(self, fact: TrustedGuardFact, request_value: TransitionRequest) -> bool:
        del request_value
        return fact._issuer_token is self._token

    def issue(self, guard_id: GuardId, request_value: TransitionRequest) -> TrustedGuardFact:
        return TrustedGuardFact(
            guard_id=guard_id,
            semantic_owner=self._semantic_owner,
            satisfied=True,
            reason="COMMAND_CENTER_INTEGRATION_FIXTURE_PASS",
            authority_ref=f"integration-owner:{self._semantic_owner.value}",
            bound_refs=required_bound_refs(guard_id, request_value),
            task_contract_id=request_value.task_contract_id,
            task_contract_version=request_value.task_contract_version,
            work_run_id=request_value.work_run_id,
            state_version=request_value.observed_state_version,
            _issuer_token=self._token,
        )


class _GuardAuthority:
    def __init__(self) -> None:
        self.system = P1_4GuardAuthority()
        self._future = {
            owner: _FutureAuthority(owner)
            for owner in (
                GuardSemanticOwner.P1_6_EVIDENCE,
                GuardSemanticOwner.P1_7_HUMAN,
                GuardSemanticOwner.P1_7_JUDGMENT,
            )
        }

    @property
    def future_verifiers(self) -> tuple[FutureOwnerGuardVerifier, ...]:
        return tuple(self._future.values())

    def issue(self, guard_id: GuardId, request_value: TransitionRequest) -> TrustedGuardFact:
        owner = GUARD_OWNER_POLICY[guard_id]
        if owner is GuardSemanticOwner.P1_4_SYSTEM:
            return self.system.issue(
                guard_id=guard_id,
                satisfied=True,
                reason="COMMAND_CENTER_INTEGRATION_FIXTURE_PASS",
                authority_ref=f"integration:{guard_id.value}",
                request=request_value,
            )
        return self._future[owner].issue(guard_id, request_value)


def _build_kernel(database_url: str) -> tuple[WorkflowKernel, _GuardAuthority, Any]:
    engine = create_engine(database_url)
    authority = _GuardAuthority()
    repository = PostgresTransitionRepository(
        create_session_factory(engine),
        TransitionEvaluator(authority.system, authority.future_verifiers),
        _BlockerSourceVerifier(),
    )
    return WorkflowKernel(repository), authority, engine


def _request(
    *,
    run_id: str,
    source: WorkflowState | None,
    version: int,
    target: WorkflowState,
    project_id: str,
    task_contract_id: str,
    judgment_refs: tuple[str, ...] = (),
) -> TransitionRequest:
    request_id = f"cc-transition-{uuid4().hex}"
    blocker_claim = (
        P1_4BlockerClaimV1(
            f"cc-blocker-{request_id}",
            BlockerKindV1.EXECUTION,
            BlockerReasonCodeV1.EXECUTION_BLOCKER,
            "resolution-contract:v1:test",
            "a" * 64,
            ("source-authority:v1:test",),
            ("c" * 64,),
        )
        if target is WorkflowState.BLOCKED
        else None
    )
    return TransitionRequest(
        transition_request_id=request_id,
        project_id=project_id,
        task_contract_id=task_contract_id,
        task_contract_version="v1",
        work_run_id=run_id,
        observed_state=source,
        observed_state_version=version,
        target_state=target,
        requester_identity="command-center-integration",
        requester_type=RequesterType.SYSTEM,
        runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        judgment_refs=judgment_refs,
        blocker_claim=blocker_claim,
    )


async def _admit(
    kernel: WorkflowKernel,
    authority: _GuardAuthority,
    request_value: TransitionRequest,
) -> TransitionDecision:
    required = TRANSITION_MATRIX.get(
        (request_value.observed_state, request_value.target_state), frozenset()
    )
    facts = tuple(authority.issue(guard, request_value) for guard in sorted(required, key=str))
    decision = await kernel.request_transition(request_value, facts)
    assert decision.outcome is DecisionOutcome.ADMITTED
    return decision


@pytest.fixture(scope="module")
def database_url() -> str:
    value = os.environ.get("AISCC_TEST_DATABASE_URL")
    if not value:
        pytest.skip("AISCC_TEST_DATABASE_URL is required for PostgreSQL evidence")
    return value


async def _seed(database_url: str) -> dict[str, str]:
    label = uuid4().hex
    project_id = f"cc-project-{label}"
    accepted_run_id = f"cc-accepted-{label}"
    no_attempt_run_id = f"cc-no-attempt-{label}"
    kernel, authority, engine = _build_kernel(database_url)
    sessions = create_session_factory(engine)
    task_id = f"cc-task-{label}"

    create = _request(
        run_id=accepted_run_id,
        source=None,
        version=0,
        target=WorkflowState.READY,
        project_id=project_id,
        task_contract_id=task_id,
    )
    await _admit(kernel, authority, create)
    denied = _request(
        run_id=accepted_run_id,
        source=WorkflowState.READY,
        version=1,
        target=WorkflowState.ACCEPTED,
        project_id=project_id,
        task_contract_id=task_id,
    )
    denied_decision = await kernel.request_transition(denied, ())
    assert denied_decision.outcome is DecisionOutcome.DENIED
    steps = (
        (WorkflowState.READY, 1, WorkflowState.RUNNING),
        (WorkflowState.RUNNING, 2, WorkflowState.ADMISSION_PENDING),
        (WorkflowState.ADMISSION_PENDING, 3, WorkflowState.HUMAN_REQUIRED),
    )
    for source, version, target in steps:
        await _admit(
            kernel,
            authority,
            _request(
                run_id=accepted_run_id,
                source=source,
                version=version,
                target=target,
                project_id=project_id,
                task_contract_id=task_id,
            ),
        )

    accepted_request = _request(
        run_id=accepted_run_id,
        source=WorkflowState.HUMAN_REQUIRED,
        version=4,
        target=WorkflowState.ACCEPTED,
        project_id=project_id,
        task_contract_id=task_id,
    )
    evidence_repository = PostgresEvidenceRepository(sessions)
    policy_authority = JudgmentPolicyAuthority(sessions, clock=lambda: NOW)
    policy = await policy_authority.register(
        policy_id=f"cc-policy-{label}",
        policy_version="v1",
        task_contract_id=task_id,
        task_contract_version="v1",
        source_state=WorkflowState.HUMAN_REQUIRED,
        target_state=WorkflowState.ACCEPTED,
        owner_policy=JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC,
        requires_human_result=False,
        requires_post_human_evidence=False,
        deterministic_kind=JudgmentKind.ACCEPTED,
    )
    judgment_authority = PostgresJudgmentAuthority(
        sessions,
        evidence_repository,
        policy_authority,
        clock=lambda: NOW,
    )
    judgment = await judgment_authority.issue(
        judgment_id=f"cc-judgment-{label}",
        judgment_version="v1",
        request=accepted_request,
        policy=policy,
        human_result_ref=None,
        evidence_attestation_ref=None,
        reason_code="DETERMINISTIC_ACCEPTANCE",
        reason_vocabulary_version="v1",
    )
    accepted_request = _request(
        run_id=accepted_run_id,
        source=WorkflowState.HUMAN_REQUIRED,
        version=4,
        target=WorkflowState.ACCEPTED,
        project_id=project_id,
        task_contract_id=task_id,
        judgment_refs=(judgment.serialized_ref,),
    )
    accepted_decision = await _admit(kernel, authority, accepted_request)

    await _admit(
        kernel,
        authority,
        _request(
            run_id=no_attempt_run_id,
            source=None,
            version=0,
            target=WorkflowState.READY,
            project_id=project_id,
            task_contract_id=f"cc-no-attempt-task-{label}",
        ),
    )

    external_repository = PostgresExternalTaskAuthorityRepository(sessions)
    external_writer = _bind_repository_once(external_repository)
    constraint, _ = await external_writer.issue_task_constraint(
        constraint_ref_id=f"cc-constraint-{label}",
        logical_constraint_id=f"cc-constraint-lineage-{label}",
        scope=TaskConstraintScopeV1(
            TaskConstraintScopeKind.TASK_CONTRACT,
            project_id,
            task_id,
            "v1",
        ),
        constraint_schema_id="TASK_CONSTRAINT_PAYLOAD_V1",
        constraint_schema_version="v1",
        constraint_payload_ref=f"task-constraint-payload:v1:{label}",
        constraint_payload_fingerprint="a" * 64,
        event_id=f"cc-constraint-event-{label}",
        issued_at=NOW,
    )
    constraint_snapshot = await external_writer.certify_snapshot(
        snapshot_id=f"cc-constraint-snapshot-{label}", issued_at=NOW
    )

    ids = {
        "set": f"cc-set-{label}@v1",
        "requirement": f"cc-requirement-{label}@v1",
        "checkpoint": f"cc-checkpoint-{label}@v1",
        "candidate": f"cc-candidate-{label}",
        "request": f"cc-admission-request-{label}",
        "evaluation": f"cc-evaluation-{label}",
        "decision": f"cc-evidence-decision-{label}",
        "admitted": f"cc-admitted-{label}",
        "satisfaction": f"cc-satisfaction-{label}",
        "set_evaluation": f"cc-set-evaluation-{label}",
        "attestation": f"cc-attestation-{label}",
        "attestation_ref": f"p1-6-set-attestation:v1:cc-attestation-{label}",
    }
    async with sessions() as session, session.begin():
        attempt = ExecutionAttemptRow(
            execution_attempt_id=f"cc-attempt-{label}",
            work_run_id=accepted_run_id,
            attempt_ordinal=1,
            parent_attempt_id=None,
            task_contract_id=task_id,
            task_contract_version="v1",
            runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD.value,
            provider_profile_id="provider-profile-safe",
            provider_profile_version="v1",
            tool_registry_id="tool-registry-safe",
            tool_registry_version="v1",
            creation_state=WorkflowState.READY.value,
            creation_state_version=1,
            causal_state=WorkflowState.RUNNING.value,
            causal_state_version=2,
            status="EXECUTOR_COMPLETED",
            execution_version=2,
            latest_event_sequence=0,
            counters={
                "schema_version": "AISCC-P1-5-DURABLE-COUNTERS-V1",
                "provider_calls": 1,
                "agent_rounds": 1,
                "tool_calls": 1,
                "provider_retries": 0,
                "output_bytes": 32,
                "output_tokens": 8,
                "budget_units": 2,
                "started_at": NOW.isoformat(),
                "deadline_at": NOW.replace(minute=31).isoformat(),
            },
            created_at=NOW,
            updated_at=NOW,
        )
        session.add(attempt)
        await session.flush()
        event = ExecutionEventRow(
            event_id=f"cc-execution-event-{label}",
            event_identity="b" * 64,
            execution_attempt_id=attempt.execution_attempt_id,
            event_kind="EXECUTION_COMPLETED",
            status_before="RUNNING",
            status_after="EXECUTOR_COMPLETED",
            execution_version_after=2,
            causal_state=WorkflowState.RUNNING.value,
            causal_state_version=2,
            payload_hash="c" * 64,
            refs={"private_provider_message": "DO_NOT_EXPORT"},
            created_at=NOW,
        )
        session.add(event)
        await session.flush()
        attempt.latest_event_sequence = event.event_sequence
        session.add(
            ExecutionOperationRow(
                operation_id=f"cc-operation-{label}",
                execution_attempt_id=attempt.execution_attempt_id,
                operation_kind="TOOL",
                operation_fingerprint="d" * 64,
                current_phase="OUTCOME_KNOWN",
                outcome="TOOL_COMPLETED",
                resource_identity="private://credential-bearing-resource/DO_NOT_EXPORT",
                call_ordinal=1,
                parent_operation_id=None,
                latest_event_sequence=0,
                created_at=NOW,
                updated_at=NOW,
            )
        )
        session.add(
            ExecutionOutputRefRow(
                output_ref_id=f"cc-submission-{label}",
                execution_attempt_id=attempt.execution_attempt_id,
                ref_kind="ExecutionSubmissionRef",
                content_hash="e" * 64,
                storage_ref="private://submission/DO_NOT_EXPORT",
                created_at=NOW,
            )
        )
        session.add(
            EvidenceRequirementSetRow(
                requirement_set_ref=ids["set"],
                requirement_set_id=ids["set"].split("@", 1)[0],
                requirement_set_version="v1",
                task_contract_id=task_id,
                task_contract_version="v1",
                requirement_root_hash="1" * 64,
                fingerprint="2" * 64,
                payload={
                    "ordered_requirement_refs": [ids["requirement"]],
                    "ordered_checkpoint_refs": [ids["checkpoint"]],
                    "semantic_owner": "P1_6_EVIDENCE",
                },
                issued_at=NOW,
            )
        )
        await session.flush()
        session.add(
            EvidenceRequirementRow(
                requirement_ref=ids["requirement"],
                requirement_set_ref=ids["set"],
                profile="EXECUTOR_REQUIRED",
                obligation="REQUIRED",
                fingerprint_schema="P1_6_EVIDENCE_REQUIREMENT_FINGERPRINT_V1",
                fingerprint="3" * 64,
                payload={
                    "applicable_checkpoint_refs": [ids["checkpoint"]],
                    "evidence_type_id": "STATIC_CHECK",
                    "evidence_type_version": "v1",
                    "freshness_kind": "TASK_EXECUTION_SCOPED",
                },
                issued_at=NOW,
            )
        )
        session.add(
            EvidenceCheckpointRow(
                checkpoint_ref=ids["checkpoint"],
                requirement_set_ref=ids["set"],
                task_contract_id=task_id,
                task_contract_version="v1",
                source_state=WorkflowState.HUMAN_REQUIRED.value,
                target_state=WorkflowState.ACCEPTED.value,
                transition_purpose_id=None,
                transition_purpose_version=None,
                fingerprint="4" * 64,
                payload={},
                issued_at=NOW,
            )
        )
        session.add(
            EvidenceCandidateRow(
                candidate_id=ids["candidate"],
                candidate_version="v1",
                candidate_fingerprint="5" * 64,
                task_contract_id=task_id,
                task_contract_version="v1",
                checkpoint_ref=ids["checkpoint"],
                issuer_type="SYSTEM_STATIC_PROOF",
                sensitivity="INTERNAL",
                content_hash="6" * 64,
                human_ingress_record_ref=None,
                payload={"body": "DO_NOT_EXPORT_EVIDENCE_BODY"},
                created_at=NOW,
            )
        )
        await session.flush()
        session.add(
            EvidenceAdmissionRequestRow(
                admission_request_id=ids["request"],
                request_fingerprint="7" * 64,
                candidate_id=ids["candidate"],
                requirement_ref=ids["requirement"],
                requirement_set_ref=ids["set"],
                work_run_id=accepted_run_id,
                checkpoint_ref=ids["checkpoint"],
                observed_state=WorkflowState.HUMAN_REQUIRED.value,
                observed_state_version=4,
                payload={},
                created_at=NOW,
            )
        )
        await session.flush()
        session.add(
            EvidenceEvaluationRow(
                evaluation_id=ids["evaluation"],
                admission_request_id=ids["request"],
                dimension_results=[],
                authority_version="v1",
                evaluated_at=NOW,
            )
        )
        await session.flush()
        evidence_decision = EvidenceAdmissionDecisionRow(
            decision_id=ids["decision"],
            admission_request_id=ids["request"],
            evaluation_id=ids["evaluation"],
            outcome="ADMITTED",
            reason="ADMITTED",
            secondary_reasons=[],
            admitting_authority_version="v1",
            decided_at=NOW,
        )
        session.add(evidence_decision)
        await session.flush()
        session.add(
            AdmittedEvidenceRow(
                admitted_evidence_id=ids["admitted"],
                decision_id=ids["decision"],
                candidate_id=ids["candidate"],
                requirement_ref=ids["requirement"],
                work_run_id=accepted_run_id,
                checkpoint_ref=ids["checkpoint"],
                content_hash="6" * 64,
                coverage=["static-source"],
                payload={},
                admitted_at=NOW,
            )
        )
        await session.flush()
        session.add(
            EvidenceRequirementSatisfactionRow(
                satisfaction_id=ids["satisfaction"],
                admitted_evidence_id=ids["admitted"],
                requirement_ref=ids["requirement"],
                work_run_id=accepted_run_id,
                checkpoint_ref=ids["checkpoint"],
                coverage=["static-source"],
                created_at=NOW,
            )
        )
        session.add(
            EvidenceSetEvaluationRow(
                evaluation_id=ids["set_evaluation"],
                evaluation_version="v1",
                work_run_id=accepted_run_id,
                source_state=WorkflowState.HUMAN_REQUIRED.value,
                state_version=4,
                checkpoint_ref=ids["checkpoint"],
                requirement_set_ref=ids["set"],
                outcome="SATISFIED",
                full_requirement_root_hash="1" * 64,
                checkpoint_subset_root_hash="8" * 64,
                admitted_ref_root_hash="9" * 64,
                evidence_authority_revision=1,
                payload={},
                evaluated_at=NOW,
            )
        )
        await session.flush()
        session.add(
            EvidenceSetAttestationRow(
                attestation_id=ids["attestation"],
                attestation_version="v1",
                serialized_ref=ids["attestation_ref"],
                evidence_set_evaluation_id=ids["set_evaluation"],
                work_run_id=accepted_run_id,
                checkpoint_ref=ids["checkpoint"],
                state_version=4,
                evidence_authority_revision=1,
                payload={},
                issued_at=NOW,
                expires_at=None,
            )
        )

        gate_id = f"cc-gate-{label}"
        gate_ref = f"p1-7-gate:v1:{gate_id}"
        result_id = f"cc-human-result-{label}"
        result_ref = f"p1-7-human-result:v1:{result_id}"
        session.add(
            HumanGateRow(
                human_gate_id=gate_id,
                serialized_ref=gate_ref,
                gate_fingerprint="a" * 64,
                task_contract_id=task_id,
                task_contract_version="v1",
                work_run_id=accepted_run_id,
                opened_from_state=WorkflowState.ADMISSION_PENDING.value,
                opened_from_state_version=3,
                bound_state_version=4,
                payload={
                    "purpose_id": "P1_7_WORK_RESULT_REVIEW",
                    "purpose_version": "v1",
                },
                opened_at=NOW,
            )
        )
        await session.flush()
        gate_opened = HumanGateAuthorityEventRow(
            event_id=f"cc-gate-opened-{label}",
            human_gate_id=gate_id,
            event_kind="OPENED",
            prior_revision=0,
            new_revision=1,
            payload={
                "bound_state": WorkflowState.HUMAN_REQUIRED.value,
                "bound_state_version": 4,
            },
            created_at=NOW,
        )
        session.add(gate_opened)
        await session.flush()
        gate_resolved = HumanGateAuthorityEventRow(
            event_id=f"cc-gate-resolved-{label}",
            human_gate_id=gate_id,
            event_kind="RESOLVED",
            prior_revision=1,
            new_revision=2,
            payload={
                "bound_state": WorkflowState.HUMAN_REQUIRED.value,
                "bound_state_version": 4,
            },
            created_at=NOW,
        )
        session.add(gate_resolved)
        await session.flush()
        session.add(
            HumanResultRow(
                human_result_id=result_id,
                serialized_ref=result_ref,
                human_result_fingerprint="b" * 64,
                human_gate_id=gate_id,
                work_run_id=accepted_run_id,
                result_kind="APPROVE",
                authority_revision=1,
                payload={
                    "structured_reason_code": "HUMAN_ACCEPTED",
                    "principal_id": "DO_NOT_EXPORT_HUMAN_IDENTITY",
                    "private_comment_ref": "private://DO_NOT_EXPORT_HUMAN_COMMENT",
                    "private_comment_hash": "c" * 64,
                },
                admitted_at=NOW,
            )
        )
        await session.flush()
        result_event = HumanResultAuthorityEventRow(
            event_id=f"cc-result-issued-{label}",
            human_result_id=result_id,
            event_kind="ISSUED",
            prior_revision=0,
            new_revision=1,
            payload={},
            created_at=NOW,
        )
        session.add(result_event)
        await session.flush()
        session.add(
            HumanGateProjectionRow(
                human_gate_id=gate_id,
                work_run_id=accepted_run_id,
                authority_epoch=f"cc-gate-epoch-{label}",
                status="RESOLVED",
                suspension_status="NOT_APPLICABLE",
                authority_revision=2,
                bound_state=WorkflowState.HUMAN_REQUIRED.value,
                bound_state_version=4,
                current_result_ref=result_ref,
                latest_event_sequence=gate_resolved.event_sequence,
                updated_at=NOW,
            )
        )

    cycle_id = f"cc-cycle-{label}"
    cycle_request_id = f"cc-cycle-request-{label}"
    cycle_evaluation_id = f"cc-cycle-evaluation-{label}"
    cycle_decision_id = f"cc-cycle-decision-{label}"
    async with sessions() as session, session.begin():
        session.add(
            CycleAdmissionRequestRow(
                request_id=cycle_request_id,
                request_version="v1",
                request_fingerprint="d" * 64,
                cycle_id=cycle_id,
                cycle_fingerprint="e" * 64,
                project_id=project_id,
                work_run_id=accepted_run_id,
                terminal_state_version=5,
                payload={},
                requested_at=NOW,
            )
        )
        await session.flush()
        session.add(
            CycleEvaluationRow(
                evaluation_id=cycle_evaluation_id,
                request_id=cycle_request_id,
                evaluation_fingerprint="f" * 64,
                outcome="ACCEPTED",
                payload={},
                evaluated_at=NOW,
            )
        )
        await session.flush()
        session.add(
            CycleAdmissionDecisionRow(
                decision_id=cycle_decision_id,
                evaluation_id=cycle_evaluation_id,
                request_id=cycle_request_id,
                decision_fingerprint="0" * 64,
                outcome="ADMITTED",
                reason="EXACT_ACCEPTED_TERMINAL_LINEAGE",
                payload={},
                decided_at=NOW,
            )
        )
        await session.flush()
        cycle = AdmittedCycleRow(
            cycle_id=cycle_id,
            cycle_version="v1",
            serialized_ref=f"p1-8-cycle:v1:{cycle_id}",
            cycle_fingerprint="e" * 64,
            request_id=cycle_request_id,
            decision_id=cycle_decision_id,
            project_id=project_id,
            work_run_id=accepted_run_id,
            terminal_state_version=5,
            terminal_epoch_key=None,
            terminal_epoch_payload_fingerprint=None,
            source_owner_event_high_watermark=1,
            memory_policy_event_high_watermark=1,
            task_constraint_ref=constraint.constraint_ref,
            task_constraint_fingerprint=constraint.constraint_fingerprint,
            task_constraint_snapshot_ref=constraint_snapshot.snapshot_ref,
            task_constraint_snapshot_fingerprint=constraint_snapshot.snapshot_fingerprint,
            task_constraint_event_high_watermark=(constraint_snapshot.owner_event_high_watermark),
            payload={
                "task_contract_id": task_id,
                "task_contract_version": "v1",
                "transition_request_id": accepted_request.transition_request_id,
                "transition_decision_id": accepted_decision.transition_decision_id,
                "judgment_ref": judgment.serialized_ref,
                "evidence_attestation_ref": ids["attestation_ref"],
                "evidence_root": "9" * 64,
            },
            admitted_at=NOW,
        )
        session.add(cycle)
        await session.flush()
        cycle_event = CycleAuthorityEventRow(
            event_id=f"cc-cycle-event-{label}",
            cycle_id=cycle_id,
            event_kind="ADMITTED",
            payload={"decision_id": cycle_decision_id},
            created_at=NOW,
        )
        session.add(cycle_event)
        await session.flush()
        memory_id = f"cc-memory-{label}"
        lineage = hashlib.sha256(f"cc-memory-lineage-{label}".encode()).hexdigest()
        session.add(
            ProjectMemoryEntryRow(
                entry_id=memory_id,
                memory_lineage_key=lineage,
                project_id=project_id,
                cycle_id=cycle_id,
                declaration_ordinal=1,
                category="DECISION",
                content_fingerprint="2" * 64,
                policy_ref="memory-policy:v1:test",
                policy_fingerprint="3" * 64,
                source_ref=judgment.serialized_ref,
                external_context_ref=None,
                privacy="INTERNAL",
                payload={"raw_private_memory": "DO_NOT_EXPORT_MEMORY_BODY"},
                created_at=NOW,
            )
        )
        memory_event = ProjectMemoryAuthorityEventRow(
            event_id=f"cc-memory-event-{label}",
            memory_lineage_key=lineage,
            subject_entry_id=memory_id,
            replacement_entry_id="NONE",
            event_kind="CURRENT",
            prior_revision=0,
            new_revision=1,
            authority_ref="memory-authority:v1:test",
            reason="ADMITTED_CYCLE",
            payload={},
            created_at=NOW,
        )
        session.add(memory_event)
        await session.flush()
        session.add(
            ProjectMemoryViewRow(
                memory_lineage_key=lineage,
                project_id=project_id,
                current_entry_id=memory_id,
                state="CURRENT",
                reason="ADMITTED_CYCLE",
                authority_revision=1,
                latest_event_sequence=memory_event.event_sequence,
                updated_at=NOW,
            )
        )

    blocked_run_id = f"cc-blocked-{label}"
    blocked_transitions: tuple[tuple[WorkflowState | None, int, WorkflowState], ...] = (
        (None, 0, WorkflowState.READY),
        (WorkflowState.READY, 1, WorkflowState.RUNNING),
        (WorkflowState.RUNNING, 2, WorkflowState.BLOCKED),
    )
    for blocked_source, version, target in blocked_transitions:
        await _admit(
            kernel,
            authority,
            _request(
                run_id=blocked_run_id,
                source=blocked_source,
                version=version,
                target=target,
                project_id=project_id,
                task_contract_id=f"cc-blocked-task-{label}",
            ),
        )
    async with sessions() as session:
        blocker = await session.scalar(
            select(P1_4BlockerProvenanceRow).where(
                P1_4BlockerProvenanceRow.work_run_id == blocked_run_id
            )
        )
    assert blocker is not None
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
        task_authority_verifier=external_repository,
    )
    await next_action_repository.enroll_configured_authority(NOW)
    descriptor = descriptors[0]
    proposal = NextActionProposal(
        f"cc-proposal-{label}",
        project_id,
        descriptor.action_ref,
        {
            "observed_state": "BLOCKED",
            "observed_state_version": blocker.blocked_epoch,
            "operational_fact_fingerprint": blocker.blocker_fingerprint,
            "operational_fact_ref": blocker.blocker_ref,
            "operational_work_run_id": blocked_run_id,
        },
        "DO_NOT_EXPORT_NEXT_ACTION_RATIONALE",
    )
    next_action_selection, _ = await next_action_repository.select(
        selection_id=f"cc-selection-{label}",
        project_id=project_id,
        expected_project_revision=0,
        mode=NextActionSelectionMode.OPERATIONAL_RECOVERY,
        proposals=(proposal,),
        operational_work_run_id=blocked_run_id,
        now=NOW,
    )
    await engine.dispose()
    return {
        "project_id": project_id,
        "accepted_run_id": accepted_run_id,
        "no_attempt_run_id": no_attempt_run_id,
        "cycle_id": cycle_id,
        "selection_id": next_action_selection.selection_id,
    }


async def _event_counts(database_url: str, project_id: str) -> tuple[int, ...]:
    engine = create_engine(database_url)
    try:
        async with engine.connect() as connection:
            values = []
            for statement in (
                "SELECT count(*) FROM transition_decisions d JOIN transition_requests r "
                "USING (transition_request_id) WHERE r.project_id = :project_id",
                "SELECT count(*) FROM evidence_admission_decisions d "
                "JOIN evidence_admission_requests r USING (admission_request_id) "
                "JOIN work_runs w USING (work_run_id) WHERE w.project_id = :project_id",
                "SELECT count(*) FROM human_gate_authority_events e "
                "JOIN human_gates g USING (human_gate_id) WHERE g.work_run_id IN "
                "(SELECT work_run_id FROM work_runs WHERE project_id = :project_id)",
                "SELECT count(*) FROM judgment_authority_events e JOIN judgments j "
                "USING (judgment_id) WHERE j.work_run_id IN "
                "(SELECT work_run_id FROM work_runs WHERE project_id = :project_id)",
                "SELECT count(*) FROM cycle_authority_events e JOIN admitted_cycles c "
                "USING (cycle_id) WHERE c.project_id = :project_id",
                "SELECT count(*) FROM next_action_authority_events WHERE project_id = :project_id",
            ):
                value = await connection.scalar(text(statement), {"project_id": project_id})
                values.append(int(value or 0))
            return tuple(values)
    finally:
        await engine.dispose()


async def _change_work_run_version(database_url: str, work_run_id: str, delta: int) -> None:
    engine = create_engine(database_url)
    try:
        sessions = create_session_factory(engine)
        async with sessions() as session, session.begin():
            row = await session.get(WorkRunRow, work_run_id)
            assert row is not None
            row.state_version += delta
    finally:
        await engine.dispose()


class _DefaultEntrypointServer:
    def __init__(self, database_url: str | None) -> None:
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            self.port = int(probe.getsockname()[1])
        self.database_url = database_url
        self.process: subprocess.Popen[bytes] | None = None

    def __enter__(self) -> _DefaultEntrypointServer:
        environment = os.environ.copy()
        environment.pop("AISCC_DATABASE_URL", None)
        if self.database_url is not None:
            environment["AISCC_DATABASE_URL"] = self.database_url
        repository_root = Path(__file__).resolve().parents[3]
        self.process = subprocess.Popen(
            (
                sys.executable,
                "-m",
                "aiscc",
                "serve",
                "--host",
                "127.0.0.1",
                "--port",
                str(self.port),
            ),
            cwd=repository_root,
            env=environment,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                raise AssertionError("default AISCC entrypoint exited before serving")
            try:
                with socket.create_connection(("127.0.0.1", self.port), timeout=0.2):
                    break
            except OSError:
                time.sleep(0.02)
        else:
            raise AssertionError("default AISCC entrypoint did not bind loopback")
        return self

    def __exit__(self, *_: object) -> None:
        assert self.process is not None
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=10)

    def request(
        self,
        path: str,
        *,
        method: str = "GET",
        headers: dict[str, str] | None = None,
    ) -> tuple[int, dict[str, str], bytes]:
        request_value = urllib.request.Request(
            f"http://127.0.0.1:{self.port}{path}",
            method=method,
            headers=headers or {},
        )
        try:
            response = urllib.request.urlopen(request_value, timeout=10)
        except urllib.error.HTTPError as error:
            return (
                error.code,
                {key.lower(): value for key, value in error.headers.items()},
                error.read(),
            )
        with response:
            return (
                response.status,
                {key.lower(): value for key, value in response.headers.items()},
                response.read(),
            )


@pytest.mark.postgres
def test_postgres_read_models_http_runtime_and_no_mutation(database_url: str) -> None:
    seeded = run(_seed(database_url))
    project_id = seeded["project_id"]
    run_id = seeded["accepted_run_id"]

    async def direct_checks() -> None:
        engine = create_engine(database_url)
        try:
            queries = PostgresCommandCenterQueries(create_session_factory(engine))
            queue = await queries.queue(project_id, filters=QueueFilters(), cursor=None, limit=50)
            accepted = next(item for item in queue.data.items if item.work_run_id == run_id)
            assert accepted.workflow.state is WorkflowState.ACCEPTED
            assert accepted.execution.status is not None
            assert accepted.execution.status.value == "EXECUTOR_COMPLETED"
            assert accepted.human_gate.status is not None
            assert accepted.human_gate.status.value == "RESOLVED"
            assert accepted.human_result.result_kind is HumanResultKind.APPROVE
            assert accepted.judgment.kind is JudgmentKind.ACCEPTED

            transitions = (await queries.transitions(run_id)).data.items
            effects = [item.decision.derived_state_effect.value for item in transitions]
            assert effects[1] == "UNCHANGED"
            assert transitions[1].decision.outcome is DecisionOutcome.DENIED
            no_attempt = await queries.execution(seeded["no_attempt_run_id"])
            assert no_attempt.data.attempts == ()
            completed = (await queries.execution(run_id)).data.attempts[0]
            assert completed.status.value == "EXECUTOR_COMPLETED"
            assert completed.operations[0].resource == "REDACTED_RESOURCE_IDENTITY"

            evidence = (await queries.evidence(run_id)).data
            assert len(evidence.candidates) == 1
            assert len(evidence.admission_decisions) == 1
            assert len(evidence.admitted_evidence) == 1
            assert len(evidence.satisfactions) == 1
            assert evidence.set_evaluations[0].outcome.value == "SATISFIED"
            human = (await queries.human_judgment(run_id)).data
            assert human.human_result.result_kind is HumanResultKind.APPROVE
            assert human.judgment.kind is JudgmentKind.ACCEPTED
            assert human.transition_effect.outcome is DecisionOutcome.ADMITTED
            cycle = (await queries.cycle(seeded["cycle_id"])).data
            assert cycle.work_run_id == run_id and len(cycle.current_memory) == 1
            next_action = (await queries.next_action(project_id)).data
            assert next_action.selection.selection_id == seeded["selection_id"]

            serialized = json.dumps(
                {
                    "queue": queue.data.model_dump(mode="json"),
                    "execution": completed.model_dump(mode="json"),
                    "evidence": evidence.model_dump(mode="json"),
                    "human": human.model_dump(mode="json"),
                    "cycle": cycle.model_dump(mode="json"),
                    "next_action": next_action.model_dump(mode="json"),
                }
            )
            assert "DO_NOT_EXPORT" not in serialized
            assert "private://" not in serialized
        finally:
            await engine.dispose()

    run(direct_checks())

    before = run(_event_counts(database_url, project_id))
    with _DefaultEntrypointServer(database_url) as server:
        paths = (
            f"/v1/command-center/projects/{project_id}/queue",
            f"/v1/command-center/work-runs/{run_id}",
            f"/v1/command-center/work-runs/{run_id}/transitions",
            f"/v1/command-center/work-runs/{run_id}/execution",
            f"/v1/command-center/work-runs/{run_id}/evidence",
            f"/v1/command-center/work-runs/{run_id}/human-judgment",
            f"/v1/command-center/projects/{project_id}/outcomes",
            f"/v1/command-center/cycles/{seeded['cycle_id']}",
            f"/v1/command-center/projects/{project_id}/next-action",
        )
        for path in paths:
            status, headers, body = server.request(path)
            assert status == 200
            assert json.loads(body)["meta"]["consistency"] == "VERIFIED"
            assert headers["x-aiscc-exposure"] == "LOCAL_PRIVATE_ONLY"
        queue_path = paths[0]
        status, headers, _ = server.request(queue_path)
        assert status == 200
        etag = headers["etag"]
        assert server.request(queue_path, headers={"If-None-Match": etag})[0] == 304
        status, _, first_page_body = server.request(f"{queue_path}?limit=1")
        assert status == 200
        first_page = json.loads(first_page_body)
        cursor = first_page["meta"]["next_cursor"]
        assert isinstance(cursor, str)
        status, _, second_page_body = server.request(
            f"{queue_path}?limit=1&cursor={urllib.parse.quote(cursor, safe='')}"
        )
        assert status == 200
        second_page = json.loads(second_page_body)
        assert (
            second_page["data"]["items"][0]["work_run_id"]
            != (first_page["data"]["items"][0]["work_run_id"])
        )
        head_status, _, head_body = server.request(queue_path, method="HEAD")
        assert head_status == 200 and head_body == b""
        assert server.request(queue_path, method="OPTIONS")[0] == 204
        for method in ("POST", "PUT", "PATCH", "DELETE"):
            status, _, body = server.request(queue_path, method=method)
            assert status == 405
            assert json.loads(body)["error"]["code"] == "INVALID_QUERY"
        status, _, body = server.request("/v1/command-center/work-runs/missing-safe")
        assert status == 404 and json.loads(body)["error"]["code"] == "NOT_FOUND"
        status, _, body = server.request(f"{queue_path}?limit=0")
        assert status == 400 and json.loads(body)["error"]["code"] == "INVALID_QUERY"
        run(_change_work_run_version(database_url, run_id, 1))
        try:
            status, _, body = server.request(paths[1])
            assert status == 409
            conflict = json.loads(body)["error"]
            assert conflict["code"] == "AUTHORITY_CONFLICT"
            assert "SQL" not in json.dumps(conflict)
        finally:
            run(_change_work_run_version(database_url, run_id, -1))
        server.request(queue_path)
        server.request(queue_path)
    after = run(_event_counts(database_url, project_id))
    assert after == before


@pytest.mark.postgres
def test_postgres_conflict_and_http_503_fail_closed(database_url: str) -> None:
    seeded = run(_seed(database_url))

    async def corrupt_and_verify() -> None:
        engine = create_engine(database_url)
        try:
            sessions = create_session_factory(engine)
            queries = PostgresCommandCenterQueries(sessions)
            async with sessions() as session, session.begin():
                row = await session.get(WorkRunRow, seeded["accepted_run_id"])
                assert row is not None
                row.state_version += 1
            with pytest.raises(AuthorityConflictReadError):
                await queries.work_run(seeded["accepted_run_id"])
            async with sessions() as session, session.begin():
                row = await session.get(WorkRunRow, seeded["accepted_run_id"])
                assert row is not None
                row.state_version -= 1
        finally:
            await engine.dispose()

    run(corrupt_and_verify())
    with _DefaultEntrypointServer(None) as server:
        status, _, body = server.request(
            f"/v1/command-center/projects/{seeded['project_id']}/queue"
        )
        assert status == 503
        error = json.loads(body)["error"]
        assert error["code"] == "PROJECTION_UNAVAILABLE"
        assert error["retryable"] is True
