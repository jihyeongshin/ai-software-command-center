from __future__ import annotations

import asyncio
import os
from collections.abc import Coroutine
from datetime import UTC, datetime, timedelta
from typing import Any
from uuid import uuid4

import pytest
from sqlalchemy import func, select, text

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.cycle.models import MemoryCategory
from aiscc.evidence.models import canonical_hash
from aiscc.memory.models import (
    MemoryApplicabilityState,
    MemoryAuthorityMode,
    PrivacyClassification,
    ProjectMemoryError,
    ProjectMemoryErrorCode,
    default_memory_policy,
    memory_content_fingerprint,
    memory_lineage_key,
)
from aiscc.memory.repository import PostgresProjectMemoryRepository
from aiscc.next_action.models import (
    TASK_ISSUANCE_OWNER,
    ActionRef,
    NextActionDescriptor,
    NextActionError,
    NextActionErrorCode,
    NextActionProposal,
    NextActionSelectionMode,
    P1_8NextActionPolicyAuthority,
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
    CycleAdmissionDecisionRow,
    CycleAdmissionRequestRow,
    CycleEvaluationRow,
    CycleMemoryReferenceRow,
    NextActionDescriptorRow,
    NextActionProjectionRow,
    NextActionSelectionRow,
    P1_4BlockerProvenanceRow,
    ProjectMemoryAuthorityEventRow,
    ProjectMemoryEntryRow,
    ProjectMemoryViewRow,
    TaskIssuanceCandidateRow,
)
from aiscc.task_authority.authority import _bind_repository_once
from aiscc.task_authority.models import NextActionPriorityClass
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository
from aiscc.workflow.evaluator import TransitionEvaluator
from aiscc.workflow.guards import P1_4GuardAuthority
from aiscc.workflow.kernel import WorkflowKernel
from aiscc.workflow.matrix import TRANSITION_MATRIX
from aiscc.workflow.models import (
    BlockerKindV1,
    BlockerReasonCodeV1,
    P1_4BlockerClaimV1,
    RequesterType,
    TransitionRequest,
)

NOW = datetime(2026, 8, 31, 8, 13, tzinfo=UTC)


def run[T](coroutine: Coroutine[Any, Any, T]) -> T:
    return asyncio.run(coroutine)


@pytest.fixture(scope="module")
def database_url() -> str:
    value = os.environ.get("AISCC_TEST_DATABASE_URL")
    if not value:
        pytest.skip("AISCC_TEST_DATABASE_URL is required for PostgreSQL P1-8 evidence")
    return value


def configured_repository(
    database_url: str, label: str
) -> tuple[
    Any,
    PostgresNextActionRepository,
    NextActionDescriptor,
    P1_8NextActionPolicyAuthority,
]:
    engine = create_engine(database_url)
    sessions = create_session_factory(engine)
    authority = default_next_action_policy_authority()
    eligibility, selection, descriptors = authority.issue_policy_catalog_v1(now=NOW)
    descriptor = descriptors[0]
    return (
        engine,
        PostgresNextActionRepository(
            sessions,
            eligibility_policy=eligibility,
            selection_policy=selection,
            descriptors=descriptors,
            policy_authority=authority,
            task_authority_verifier=PostgresExternalTaskAuthorityRepository(sessions),
        ),
        descriptor,
        authority,
    )


async def add_recovery_fact(sessions: Any, project_id: str, label: str) -> str:
    run_id = f"recovery-run-{label}"
    authority = P1_4GuardAuthority()
    kernel = WorkflowKernel(
        PostgresTransitionRepository(sessions, TransitionEvaluator(authority, ()))
    )
    steps = (
        (None, 0, WorkflowState.READY),
        (WorkflowState.READY, 1, WorkflowState.RUNNING),
        (WorkflowState.RUNNING, 2, WorkflowState.BLOCKED),
    )
    for ordinal, (source, version, target) in enumerate(steps, 1):
        request = TransitionRequest(
            transition_request_id=f"recovery-request-{label}-{ordinal}",
            project_id=project_id,
            task_contract_id=f"task-{label}",
            task_contract_version="v1",
            work_run_id=run_id,
            observed_state=source,
            observed_state_version=version,
            target_state=target,
            requester_identity="test-system",
            requester_type=RequesterType.SYSTEM,
            runtime_mode=RuntimeMode.PUBLIC_RECORDED_REPLAY,
            blocker_claim=(
                P1_4BlockerClaimV1(
                    f"blocker-recovery-{label}",
                    BlockerKindV1.EXECUTION,
                    BlockerReasonCodeV1.EXECUTION_BLOCKER,
                    "resolution-contract:v1:test",
                    "a" * 64,
                    ("source-authority:v1:test",),
                    ("c" * 64,),
                )
                if target is WorkflowState.BLOCKED
                else None
            ),
        )
        guards = TRANSITION_MATRIX[(source, target)]
        facts = tuple(
            authority.issue(
                guard_id=guard,
                satisfied=True,
                reason="P1_4_RECOVERY_TEST_AUTHORITY",
                authority_ref=f"test:p1-4:{guard.value}",
                request=request,
            )
            for guard in sorted(guards, key=str)
        )
        decision = await kernel.request_transition(request, facts)
        assert decision.resulting_state is target
    return run_id


async def operational_parameters(sessions: Any, run_id: str) -> dict[str, object]:
    async with sessions() as session:
        blocker = await session.scalar(
            select(P1_4BlockerProvenanceRow).where(
                P1_4BlockerProvenanceRow.work_run_id == run_id
            )
        )
    assert blocker is not None
    return {
        "observed_state": "BLOCKED",
        "observed_state_version": blocker.blocked_epoch,
        "operational_fact_fingerprint": blocker.blocker_fingerprint,
        "operational_fact_ref": blocker.blocker_ref,
        "operational_work_run_id": run_id,
    }


@pytest.mark.postgres
def test_next_action_enrollment_replay_staleness_and_task_boundary(
    database_url: str,
) -> None:
    async def scenario() -> None:
        label = uuid4().hex
        project_id = f"project-{label}"
        engine, repository, descriptor, authority = configured_repository(database_url, label)
        sessions = create_session_factory(engine)
        recovery_run_id = await add_recovery_fact(sessions, project_id, label)
        parameters = await operational_parameters(sessions, recovery_run_id)
        rogue_authority = P1_8NextActionPolicyAuthority()
        rogue_eligibility, rogue_selection, rogue_descriptors = (
            rogue_authority.issue_policy_catalog_v1(now=NOW)
        )
        with pytest.raises(NextActionError) as rogue_configuration:
            PostgresNextActionRepository(
                sessions,
                eligibility_policy=rogue_eligibility,
                selection_policy=rogue_selection,
                descriptors=rogue_descriptors,
                policy_authority=rogue_authority,
                task_authority_verifier=PostgresExternalTaskAuthorityRepository(sessions),
            )
        assert rogue_configuration.value.code is NextActionErrorCode.AUTHORITY_DENIED
        await repository.enroll_configured_authority(NOW)
        arbitrary = NextActionProposal(
            f"arbitrary-{label}",
            project_id,
            ActionRef(
                "rogue-policy",
                "v1",
                "novel-action",
                "v1",
                "0" * 64,
            ),
            {},
            "caller creates an action",
            claimed_priority=0,
            claimed_security=True,
            claimed_blocker=True,
        )
        with pytest.raises(NextActionError) as not_enrolled:
            await repository.select(
                selection_id=f"selection-arbitrary-{label}",
                project_id=project_id,
                expected_project_revision=0,
                mode=NextActionSelectionMode.OPERATIONAL_RECOVERY,
                proposals=(arbitrary,),
                operational_work_run_id=recovery_run_id,
                now=NOW,
            )
        assert not_enrolled.value.code is NextActionErrorCode.NOT_ENROLLED

        proposal = NextActionProposal(
            f"proposal-{label}",
            project_id,
            descriptor.action_ref,
            parameters,
            "bounded nomination",
            claimed_priority=0,
            claimed_security=True,
            claimed_blocker=True,
        )
        selection, issuance = await repository.select(
            selection_id=f"selection-{label}",
            project_id=project_id,
            expected_project_revision=0,
            mode=NextActionSelectionMode.OPERATIONAL_RECOVERY,
            proposals=(proposal,),
            operational_work_run_id=recovery_run_id,
            now=NOW,
        )
        assert selection.action_ref == descriptor.action_ref
        assert issuance.issuance_owner == TASK_ISSUANCE_OWNER
        async with sessions() as session:
            row = await session.get(TaskIssuanceCandidateRow, issuance.candidate_id)
            assert row is not None and "task_contract" not in row.payload

        restarted = configured_repository(database_url, label)[1]
        assert await restarted.replay(selection.selection_id) == (selection, issuance)
        async with sessions() as session, session.begin():
            await session.execute(text("SET LOCAL session_replication_role = replica"))
            await session.execute(
                text(
                    "UPDATE next_action_authority_events "
                    "SET prior_revision = 1, new_revision = 2 "
                    "WHERE selection_id = :selection_id"
                ),
                {"selection_id": selection.selection_id},
            )
        with pytest.raises(NextActionError) as event_gap:
            await restarted.rebuild_projection(project_id)
        assert event_gap.value.code is NextActionErrorCode.HISTORICAL_CORRUPTION
        async with sessions() as session, session.begin():
            await session.execute(text("SET LOCAL session_replication_role = replica"))
            await session.execute(
                text(
                    "UPDATE next_action_authority_events "
                    "SET prior_revision = 0, new_revision = 1 "
                    "WHERE selection_id = :selection_id"
                ),
                {"selection_id": selection.selection_id},
            )
            descriptor_row = await session.get(
                NextActionDescriptorRow, descriptor.action_ref.serialized
            )
            assert descriptor_row is not None
            descriptor_row.fingerprint = "f" * 64
        with pytest.raises(NextActionError) as corrupt_descriptor:
            await restarted.replay(selection.selection_id)
        assert corrupt_descriptor.value.code is NextActionErrorCode.HISTORICAL_CORRUPTION
        async with sessions() as session, session.begin():
            await session.execute(text("SET LOCAL session_replication_role = replica"))
            descriptor_row = await session.get(
                NextActionDescriptorRow, descriptor.action_ref.serialized
            )
            assert descriptor_row is not None
            descriptor_row.fingerprint = descriptor.fingerprint
        assert await restarted.replay(selection.selection_id) == (selection, issuance)
        await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_next_action_same_project_revision_concurrency(database_url: str) -> None:
    async def scenario() -> None:
        label = uuid4().hex
        project_id = f"concurrent-project-{label}"
        engine, repository, descriptor, _ = configured_repository(database_url, label)
        sessions = create_session_factory(engine)
        recovery_run_id = await add_recovery_fact(sessions, project_id, label)
        parameters = await operational_parameters(sessions, recovery_run_id)
        await repository.enroll_configured_authority(NOW)

        async def contender(ordinal: int) -> object:
            try:
                return await repository.select(
                    selection_id=f"concurrent-selection-{label}-{ordinal}",
                    project_id=project_id,
                    expected_project_revision=0,
                    mode=NextActionSelectionMode.OPERATIONAL_RECOVERY,
                    proposals=(
                        NextActionProposal(
                            f"concurrent-proposal-{label}-{ordinal}",
                            project_id,
                            descriptor.action_ref,
                            parameters,
                            "race",
                        ),
                    ),
                    operational_work_run_id=recovery_run_id,
                    now=NOW,
                )
            except NextActionError as exc:
                return exc

        outcomes = await asyncio.gather(contender(1), contender(2))
        assert sum(isinstance(item, tuple) for item in outcomes) == 1
        errors = [item for item in outcomes if isinstance(item, NextActionError)]
        assert len(errors) == 1
        assert errors[0].code is NextActionErrorCode.IDENTITY_CONFLICT
        async with sessions() as session:
            assert (
                await session.scalar(
                    select(func.count())
                    .select_from(NextActionSelectionRow)
                    .where(NextActionSelectionRow.project_id == project_id)
                )
                == 1
            )
        await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_descriptor_requires_exact_policy_enrollment_and_recovery_fact(
    database_url: str,
) -> None:
    async def scenario() -> None:
        label = uuid4().hex
        project_id = f"enrollment-project-{label}"
        engine, repository, descriptor, _ = configured_repository(database_url, label)
        sessions = create_session_factory(engine)
        await repository.enroll_configured_authority(NOW)
        proposal = NextActionProposal(
            f"enrollment-proposal-{label}",
            project_id,
            descriptor.action_ref,
            {
                "observed_state": "BLOCKED",
                "observed_state_version": 3,
                "operational_fact_fingerprint": "a" * 64,
                "operational_fact_ref": "p1-4-blocker:v1:absent",
                "operational_work_run_id": "absent",
            },
            "caller claims do not establish recovery",
            claimed_blocker=True,
        )
        with pytest.raises(NextActionError) as no_recovery:
            await repository.select(
                selection_id=f"no-recovery-selection-{label}",
                project_id=project_id,
                expected_project_revision=0,
                mode=NextActionSelectionMode.OPERATIONAL_RECOVERY,
                proposals=(proposal,),
                now=NOW,
            )
        assert no_recovery.value.code is NextActionErrorCode.RECOVERY_AUTHORITY_REQUIRED

        recovery_run_id = await add_recovery_fact(sessions, project_id, label)
        proposal = NextActionProposal(
            proposal.proposal_id,
            proposal.project_id,
            proposal.action_ref,
            await operational_parameters(sessions, recovery_run_id),
            proposal.rationale,
            claimed_priority=proposal.claimed_priority,
            claimed_security=proposal.claimed_security,
            claimed_blocker=proposal.claimed_blocker,
        )
        async with sessions() as session, session.begin():
            await session.execute(text("SET LOCAL session_replication_role = replica"))
            await session.execute(
                text(
                    "DELETE FROM next_action_policy_descriptor_enrollments "
                    "WHERE action_ref = :action_ref"
                ),
                {"action_ref": descriptor.action_ref.serialized},
            )
        with pytest.raises(NextActionError) as missing_enrollment:
            await repository.select(
                selection_id=f"missing-enrollment-selection-{label}",
                project_id=project_id,
                expected_project_revision=0,
                mode=NextActionSelectionMode.OPERATIONAL_RECOVERY,
                proposals=(proposal,),
                operational_work_run_id=recovery_run_id,
                now=NOW,
            )
        assert missing_enrollment.value.code is NextActionErrorCode.NOT_ENROLLED
        await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_memory_current_historical_invalidation_and_restart_rebuild(
    database_url: str,
) -> None:
    async def scenario() -> None:
        label = uuid4().hex
        project_id = f"memory-project-{label}"
        task_id = f"task-{label}"
        cycle_id = f"memory-cycle-{label}"
        request_id = f"memory-request-{label}"
        evaluation_id = f"memory-evaluation-{label}"
        decision_id = f"memory-decision-{label}"
        entry_id = canonical_hash(["entry", label])
        engine = create_engine(database_url)
        sessions = create_session_factory(engine)
        external_repository = PostgresExternalTaskAuthorityRepository(sessions)
        external_writer = _bind_repository_once(external_repository)
        context, context_introduction = await external_writer.issue_next_action_context(
            context_ref_id=f"context-{label}",
            context_logical_local_id=f"planning-{label}",
            project_id=project_id,
            task_contract_id=task_id,
            task_contract_version="v1",
            context_slot_id="primary",
            priority_class=NextActionPriorityClass.ACCEPTED_CORE_CRITICAL_PATH,
            critical_path_ordinal=3,
            event_id=f"context-issued-{label}",
            issued_at=NOW,
        )
        context_snapshot = await external_writer.certify_snapshot(
            snapshot_id=f"context-snapshot-{label}", issued_at=NOW
        )
        context_content = {
            "context_ref": context.context_ref,
            "context_fingerprint": context.fingerprint,
            "context_logical_id": context.context_logical_id,
            "project_id": context.project_id,
            "task_contract_id": context.task_contract_id,
            "task_contract_version": context.task_contract_version,
            "context_slot_id": context.context_slot_id,
            "priority_class": context.priority_class.value,
            "critical_path_ordinal": context.critical_path_ordinal,
        }
        subject_key = context.context_logical_id
        applicability_key = f"task-contract/{project_id}/{task_id}@v1"
        semantic_slot = "next-action-context/P1_8_NEXT_ACTION_CONTEXT_RESULT_V1/primary"
        policy = default_memory_policy(NOW)
        lineage = memory_lineage_key(
            project_id=project_id,
            category=MemoryCategory.NEXT_ACTION_CONTEXT,
            subject_key=subject_key,
            applicability_key=applicability_key,
            semantic_slot=semantic_slot,
        )
        content_fingerprint = memory_content_fingerprint(
            category=MemoryCategory.NEXT_ACTION_CONTEXT,
            authority_mode=MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED,
            policy_ref=policy.serialized_ref,
            normalized_derived_content=context_content,
        )
        async with sessions() as session, session.begin():
            session.add(
                CycleAdmissionRequestRow(
                    request_id=request_id,
                    request_version="v1",
                    request_fingerprint=canonical_hash(["request", label]),
                    cycle_id=cycle_id,
                    cycle_fingerprint=canonical_hash(["cycle", label]),
                    project_id=project_id,
                    work_run_id=f"run-{label}",
                    terminal_state_version=5,
                    payload={},
                    requested_at=NOW,
                )
            )
            await session.flush()
            session.add(
                CycleEvaluationRow(
                    evaluation_id=evaluation_id,
                    request_id=request_id,
                    evaluation_fingerprint=canonical_hash(["evaluation", label]),
                    outcome="ACCEPTED",
                    payload={},
                    evaluated_at=NOW,
                )
            )
            await session.flush()
            session.add(
                CycleAdmissionDecisionRow(
                    decision_id=decision_id,
                    evaluation_id=evaluation_id,
                    request_id=request_id,
                    decision_fingerprint=canonical_hash(["decision", label]),
                    outcome="ADMITTED",
                    reason="TEST_AUTHORITY_FIXTURE",
                    payload={},
                    decided_at=NOW,
                )
            )
            await session.flush()
            session.add(
                AdmittedCycleRow(
                    cycle_id=cycle_id,
                    cycle_version="v1",
                    serialized_ref=f"p1-8-cycle:v1:{cycle_id}",
                    cycle_fingerprint=canonical_hash(["cycle", label]),
                    request_id=request_id,
                    decision_id=decision_id,
                    project_id=project_id,
                    work_run_id=f"run-{label}",
                    terminal_state_version=5,
                    terminal_epoch_key=canonical_hash(["terminal-epoch", label]),
                    terminal_epoch_payload_fingerprint=canonical_hash(
                        ["terminal-payload", label]
                    ),
                    source_owner_event_high_watermark=0,
                    memory_policy_event_high_watermark=0,
                    task_constraint_ref=None,
                    task_constraint_fingerprint=None,
                    task_constraint_snapshot_ref=None,
                    task_constraint_snapshot_fingerprint=None,
                    task_constraint_event_high_watermark=None,
                    payload={},
                    admitted_at=NOW,
                )
            )
            await session.flush()
            session.add(
                ProjectMemoryEntryRow(
                    entry_id=entry_id,
                    memory_lineage_key=lineage,
                    project_id=project_id,
                    cycle_id=cycle_id,
                    declaration_ordinal=1,
                    category=MemoryCategory.NEXT_ACTION_CONTEXT.value,
                    content_fingerprint=content_fingerprint,
                    policy_ref=policy.serialized_ref,
                    policy_fingerprint=policy.fingerprint,
                    source_ref=context_introduction.event_ref,
                    external_context_ref=context.context_ref,
                    privacy=PrivacyClassification.INTERNAL.value,
                    payload={
                        "applicability_key": applicability_key,
                        "authority_mode": "STRUCTURED_RESULT_ATTESTED",
                        "normalized_content": context_content,
                        "semantic_slot": semantic_slot,
                        "subject_key": subject_key,
                    },
                    created_at=NOW,
                )
            )
            await session.flush()
            session.add(
                CycleMemoryReferenceRow(
                    reference_id=canonical_hash(["context-reference", label]),
                    cycle_id=cycle_id,
                    entry_id=entry_id,
                    declaration_ordinal=1,
                    content_fingerprint=content_fingerprint,
                    provenance={
                        "context_ref": context.context_ref,
                        "context_fingerprint": context.fingerprint,
                        "context_introduction_event_ref": context_introduction.event_ref,
                        "context_introduction_event_fingerprint": (
                            context_introduction.event_fingerprint
                        ),
                        "context_snapshot_ref": context_snapshot.snapshot_ref,
                        "context_snapshot_fingerprint": context_snapshot.snapshot_fingerprint,
                        "context_authority_event_high_watermark": (
                            context_snapshot.owner_event_high_watermark
                        ),
                    },
                    created_at=NOW,
                )
            )
            session.add(
                ProjectMemoryAuthorityEventRow(
                    event_id=f"memory-current-{label}",
                    memory_lineage_key=lineage,
                    subject_entry_id=entry_id,
                    replacement_entry_id="NONE",
                    event_kind="CURRENT",
                    prior_revision=0,
                    new_revision=1,
                    authority_ref=context.context_ref,
                    reason="ADMITTED_CURRENT",
                    payload={},
                    created_at=NOW,
                )
            )
            await session.flush()
            event = await session.scalar(
                select(ProjectMemoryAuthorityEventRow).where(
                    ProjectMemoryAuthorityEventRow.event_id == f"memory-current-{label}"
                )
            )
            assert event is not None
            session.add(
                ProjectMemoryViewRow(
                    memory_lineage_key=lineage,
                    project_id=project_id,
                    current_entry_id=entry_id,
                    state="CURRENT",
                    reason="ADMITTED_CURRENT",
                    authority_revision=1,
                    latest_event_sequence=event.event_sequence,
                    updated_at=NOW,
                )
            )
        repository = PostgresProjectMemoryRepository(sessions, policy)
        current = await repository.retrieve(project_id=project_id)
        assert len(current) == 1 and current[0].context_marker == "CURRENT_CONTEXT"
        assert (
            await repository.retrieve(
                project_id=project_id,
                privacy_clearance=PrivacyClassification.PUBLIC_SANITIZED,
            )
            == ()
        )
        assert await repository.rebuild_projection(project_id) == (entry_id,)
        async with sessions() as session, session.begin():
            await session.execute(text("SET LOCAL session_replication_role = replica"))
            memory_row = await session.get(ProjectMemoryEntryRow, entry_id)
            assert memory_row is not None
            memory_row.content_fingerprint = "f" * 64
        with pytest.raises(ProjectMemoryError) as corrupt_content:
            await repository.retrieve(project_id=project_id)
        assert corrupt_content.value.code is ProjectMemoryErrorCode.PROJECTION_CORRUPT
        async with sessions() as session, session.begin():
            await session.execute(text("SET LOCAL session_replication_role = replica"))
            memory_row = await session.get(ProjectMemoryEntryRow, entry_id)
            assert memory_row is not None
            memory_row.content_fingerprint = content_fingerprint

        action_authority = default_next_action_policy_authority()
        eligibility, selection_policy, fixed_descriptors = (
            action_authority.issue_policy_catalog_v1(now=NOW)
        )
        descriptor = action_authority.issue_context_bound_descriptor(
            context=context,
            issuance_event_sequence=context_introduction.event_sequence,
        )
        actions = PostgresNextActionRepository(
            sessions,
            eligibility_policy=eligibility,
            selection_policy=selection_policy,
            descriptors=(*fixed_descriptors, descriptor),
            policy_authority=action_authority,
            task_authority_verifier=external_repository,
        )
        await actions.enroll_configured_authority(NOW)
        async with sessions() as session:
            memory_high_watermark = int(
                await session.scalar(
                    select(func.max(ProjectMemoryAuthorityEventRow.event_sequence))
                )
                or 0
            )
        parameters = {
            "source_cycle_id": cycle_id,
            "memory_entry_refs": [entry_id],
            "next_action_context_ref": context.context_ref,
            "next_action_context_fingerprint": context.fingerprint,
            "memory_authority_event_high_watermark": memory_high_watermark,
        }
        cycle_selection, _ = await actions.select(
            selection_id=f"cycle-derived-{label}",
            project_id=project_id,
            expected_project_revision=0,
            mode=NextActionSelectionMode.CYCLE_DERIVED,
            proposals=(
                NextActionProposal(
                    f"cycle-proposal-{label}",
                    project_id,
                    descriptor.action_ref,
                    parameters,
                    "current memory context",
                ),
            ),
            memory_entry_ids=(entry_id,),
            now=NOW,
        )
        assert cycle_selection.memory_refs == (entry_id,)
        revoked = await external_writer.revoke_next_action_context(
            current_context_ref=context.context_ref,
            event_id=f"context-revoked-{label}",
            effective_at=NOW + timedelta(seconds=1),
        )
        await external_writer.certify_snapshot(
            snapshot_id=f"context-revoked-snapshot-{label}",
            issued_at=NOW + timedelta(seconds=1),
        )
        await actions.reconcile_external_context_event(
            revoked.event_ref, expected_project_revisions={project_id: 1}
        )
        await actions.reconcile_external_context_event(
            revoked.event_ref, expected_project_revisions={project_id: 2}
        )
        assert await repository.retrieve(project_id=project_id) == ()
        historical = await repository.retrieve(
            project_id=project_id,
            current_only=False,
            authorize_historical=True,
        )
        assert len(historical) == 1
        assert historical[0].state is MemoryApplicabilityState.REVOKED
        assert historical[0].context_marker == "NOT_CURRENT_CONTEXT"
        with pytest.raises(NextActionError) as not_current:
            await actions.select(
                selection_id=f"cycle-derived-stale-{label}",
                project_id=project_id,
                expected_project_revision=2,
                mode=NextActionSelectionMode.CYCLE_DERIVED,
                proposals=(
                    NextActionProposal(
                        f"cycle-proposal-stale-{label}",
                        project_id,
                        descriptor.action_ref,
                        parameters,
                        "historical memory context",
                    ),
                ),
                memory_entry_ids=(entry_id,),
                now=NOW + timedelta(seconds=2),
            )
        assert not_current.value.code is NextActionErrorCode.NON_CURRENT_MEMORY
        assert await actions.replay(cycle_selection.selection_id)
        async with sessions() as session:
            projection = await session.get(NextActionProjectionRow, project_id)
            assert projection is not None and projection.state == "WITHDRAWN"
        restarted = PostgresProjectMemoryRepository(sessions, policy)
        assert await restarted.rebuild_projection(project_id) == ()
        await engine.dispose()

    run(scenario())
