from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Any, cast

from sqlalchemy import func, select, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.command_center.privacy import (
    redacted_resource_identity,
    safe_mapping,
    safe_optional_string,
    safe_string_list,
    safe_timestamp,
)
from aiscc.command_center.queries import (
    AuthorityConflictReadError,
    CommandCenterReadError,
    InvalidQueryError,
    ProjectionUnavailableReadError,
    QueryResult,
    QueueFilters,
    ReadModelNotFoundError,
    decode_cursor,
    encode_cursor,
    utc_snapshot,
    validate_limit,
)
from aiscc.command_center.read_models import (
    AdmittedCycleSummaryView,
    AdmittedEvidenceView,
    Availability,
    BlockerView,
    CycleData,
    DerivedStateEffect,
    DurableCountersView,
    EvidenceAdmissionDecisionView,
    EvidenceCandidateView,
    EvidenceCheckpointView,
    EvidenceContentMetadataView,
    EvidenceData,
    EvidenceRequirementSetView,
    EvidenceRequirementView,
    EvidenceSetAttestationView,
    EvidenceSetEvaluationView,
    ExecutionAttemptView,
    ExecutionData,
    ExecutionOperationView,
    ExecutionSummaryView,
    GuardView,
    HumanGateSummaryView,
    HumanGateView,
    HumanJudgmentData,
    HumanResultSummaryView,
    HumanResultView,
    JudgmentSummaryView,
    JudgmentView,
    MemorySafeSummaryView,
    NextActionData,
    NextActionProjectionView,
    NextActionSelectionView,
    NextActionSummaryView,
    OutcomeRow,
    OutcomesData,
    Presence,
    QueueData,
    QueueRow,
    RequirementSatisfactionView,
    ScopeView,
    SubmissionView,
    TaskConstraintView,
    TaskContractView,
    TaskDisplayView,
    TaskIssuanceCandidateView,
    TransitionDecisionSummaryView,
    TransitionDecisionView,
    TransitionEffectView,
    TransitionEvaluationView,
    TransitionRecord,
    TransitionRequestView,
    TransitionsData,
    WorkflowView,
    WorkRunData,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.evidence.models import (
    EvidenceAdmissionOutcome,
    EvidenceRequirementProfile,
    EvidenceSemanticOwner,
    EvidenceSetOutcome,
    RequirementObligation,
)
from aiscc.human.models import (
    HumanAuthorityError,
    HumanGateStatus,
    HumanGateSuspensionStatus,
    HumanResultKind,
)
from aiscc.judgment.authority import verify_historical_judgment_provenance
from aiscc.judgment.models import JudgmentAuthorityError, JudgmentKind, JudgmentOwnerPolicy
from aiscc.memory.models import MemoryApplicabilityState, PrivacyClassification
from aiscc.persistence.models import (
    AdmittedCycleRow,
    AdmittedEvidenceRow,
    CycleAdmissionDecisionRow,
    CycleAdmissionRequestRow,
    CycleAuthorityEventRow,
    CycleEvaluationRow,
    EvidenceAdmissionDecisionRow,
    EvidenceAdmissionRequestRow,
    EvidenceAuthorityEventRow,
    EvidenceCandidateContentBindingRow,
    EvidenceCandidateRow,
    EvidenceCheckpointRow,
    EvidenceContentObjectRow,
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
    ExternalTaskAuthorityEventRegistryRow,
    HumanGateAuthorityEventRow,
    HumanGateProjectionRow,
    HumanGateRow,
    HumanResultAuthorityEventRow,
    HumanResultRow,
    JudgmentAuthorityEventRow,
    JudgmentProjectionRow,
    JudgmentRow,
    NextActionAuthorityEventRow,
    NextActionProjectionRow,
    NextActionSelectionRow,
    P1_4BlockerProjectionRow,
    P1_4BlockerProvenanceRow,
    ProjectMemoryAuthorityEventRow,
    ProjectMemoryEntryRow,
    ProjectMemoryViewRow,
    TaskConstraintAuthorityEventRow,
    TaskConstraintCurrentRow,
    TaskConstraintOwnerSnapshotRow,
    TaskConstraintRefRow,
    TaskIssuanceCandidateRow,
    TransitionDecisionRow,
    TransitionEvaluationRow,
    TransitionRequestRow,
    WorkRunRow,
)
from aiscc.persistence.repository import (
    HistoricalTransitionProvenanceError,
    PostgresExecutionRepository,
    verify_historical_transition_provenance,
)
from aiscc.providers.models import (
    ExecutionOperationOutcome,
    ExecutionOperationPhase,
    ExecutionStatus,
    OperationKind,
)
from aiscc.task_authority.models import (
    TaskConstraintOwnerSnapshotV1,
    TaskConstraintScopeKind,
    ordered_event_prefix_root,
    task_constraint_ref_from_payload,
)
from aiscc.workflow.matrix import TERMINAL_STATES
from aiscc.workflow.models import (
    AuthorityConflictError,
    DecisionOutcome,
    DecisionReason,
    RequesterType,
)

_OUTCOME_STATES = TERMINAL_STATES | {WorkflowState.BLOCKED, WorkflowState.REWORK_REQUIRED}


class PostgresCommandCenterQueries:
    """GET-only projections assembled inside one PostgreSQL read-only snapshot."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._sessions = session_factory

    @asynccontextmanager
    async def _snapshot(self) -> AsyncIterator[tuple[AsyncSession, datetime]]:
        try:
            async with self._sessions() as session, session.begin():
                await session.execute(
                    text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
                )
                snapshot = await session.scalar(select(func.transaction_timestamp()))
                if snapshot is None:
                    raise ProjectionUnavailableReadError("snapshot timestamp is unavailable")
                yield session, utc_snapshot(snapshot)
        except CommandCenterReadError:
            raise
        except (
            AuthorityConflictError,
            HistoricalTransitionProvenanceError,
            HumanAuthorityError,
            JudgmentAuthorityError,
            KeyError,
            TypeError,
            ValueError,
        ) as exc:
            raise AuthorityConflictReadError("durable authority is inconsistent") from exc
        except SQLAlchemyError as exc:
            raise ProjectionUnavailableReadError("read projection is unavailable") from exc

    async def queue(
        self,
        project_id: str,
        *,
        filters: QueueFilters,
        cursor: str | None,
        limit: int,
    ) -> QueryResult[QueueData]:
        validate_limit(limit)
        _validate_queue_filters(filters)
        shape = _queue_shape(project_id, filters)
        position = decode_cursor(cursor, shape=shape) if cursor is not None else None
        async with self._snapshot() as (session, snapshot):
            run_rows = tuple(
                await session.scalars(
                    select(WorkRunRow)
                    .where(WorkRunRow.project_id == project_id)
                    .order_by(WorkRunRow.updated_at.desc(), WorkRunRow.work_run_id)
                )
            )
            if not run_rows:
                raise ReadModelNotFoundError("project has no authoritative WorkRun")
            rows: list[QueueRow] = []
            for run_row in run_rows:
                await self._verify_work_run(session, run_row)
                row = await self._queue_row(session, run_row)
                if _queue_matches(row, filters) and _after_queue_cursor(row, position):
                    rows.append(row)
            page = rows[:limit]
            next_cursor = None
            if len(rows) > limit and page:
                last = page[-1]
                next_cursor = encode_cursor(
                    shape=shape,
                    position={
                        "updated_at": last.workflow.updated_at.astimezone(UTC).isoformat(),
                        "work_run_id": last.work_run_id,
                    },
                )
            revisions = await self._project_revisions(session, project_id)
            return QueryResult(
                QueueData(project_id=project_id, items=tuple(page)),
                snapshot,
                revisions,
                next_cursor=next_cursor,
            )

    async def work_run(self, work_run_id: str) -> QueryResult[WorkRunData]:
        async with self._snapshot() as (session, snapshot):
            row = await self._require_work_run(session, work_run_id)
            blocker = await self._blocker(session, row.work_run_id)
            task_constraint = await self._task_constraint(session, row)
            data = WorkRunData(
                project_id=row.project_id,
                work_run_id=row.work_run_id,
                task_contract=_task_contract(row),
                runtime_mode=RuntimeMode(row.runtime_mode),
                workflow=_workflow(row, include_created=True),
                task_constraint=task_constraint,
                task_display=_reference_task_display(),
                scope=ScopeView(),
                blocker=blocker,
            )
            revisions = await self._work_run_revisions(session, row)
            return QueryResult(data, snapshot, revisions)

    async def transitions(self, work_run_id: str) -> QueryResult[TransitionsData]:
        async with self._snapshot() as (session, snapshot):
            row = await self._require_work_run(session, work_run_id)
            triples = await session.execute(
                select(TransitionRequestRow, TransitionEvaluationRow, TransitionDecisionRow)
                .join(
                    TransitionEvaluationRow,
                    TransitionEvaluationRow.transition_request_id
                    == TransitionRequestRow.transition_request_id,
                )
                .join(
                    TransitionDecisionRow,
                    TransitionDecisionRow.transition_request_id
                    == TransitionRequestRow.transition_request_id,
                )
                .where(TransitionRequestRow.work_run_id == work_run_id)
                .order_by(
                    TransitionDecisionRow.decided_at,
                    TransitionDecisionRow.transition_decision_id,
                )
            )
            records: list[TransitionRecord] = []
            maximum = 0
            for request_row, evaluation_row, decision_row in triples:
                record = await self._transition_record(
                    session, request_row, evaluation_row, decision_row
                )
                records.append(record)
                maximum = max(maximum, decision_row.event_sequence)
            revisions: dict[str, int | str] = {
                "workflow_state_version": row.state_version,
                "transition_event_high_watermark": maximum,
            }
            return QueryResult(
                TransitionsData(work_run_id=work_run_id, items=tuple(records)),
                snapshot,
                revisions,
            )

    async def execution(self, work_run_id: str) -> QueryResult[ExecutionData]:
        async with self._snapshot() as (session, snapshot):
            row = await self._require_work_run(session, work_run_id)
            attempts = tuple(
                await session.scalars(
                    select(ExecutionAttemptRow)
                    .where(ExecutionAttemptRow.work_run_id == work_run_id)
                    .order_by(
                        ExecutionAttemptRow.attempt_ordinal,
                        ExecutionAttemptRow.execution_attempt_id,
                    )
                )
            )
            views = tuple([await self._execution_attempt(session, attempt) for attempt in attempts])
            revisions: dict[str, int | str] = {"workflow_state_version": row.state_version}
            if attempts:
                revisions["execution_event_high_watermark"] = max(
                    item.latest_event_sequence for item in attempts
                )
                revisions["execution_version_max"] = max(
                    item.execution_version for item in attempts
                )
            return QueryResult(
                ExecutionData(work_run_id=work_run_id, attempts=views), snapshot, revisions
            )

    async def _require_work_run(self, session: AsyncSession, work_run_id: str) -> WorkRunRow:
        row = await session.get(WorkRunRow, work_run_id)
        if row is None:
            raise ReadModelNotFoundError("WorkRun is unavailable")
        await self._verify_work_run(session, row)
        return row

    async def _verify_work_run(self, session: AsyncSession, row: WorkRunRow) -> None:
        verified = await PostgresExecutionRepository._verify_consistency_in_session(
            session, row.work_run_id, row
        )
        if (
            verified is None
            or verified.project_id != row.project_id
            or verified.state.value != row.workflow_state
            or verified.state_version != row.state_version
        ):
            raise AuthorityConflictReadError("WorkRun projection is inconsistent")

    async def _transition_record(
        self,
        session: AsyncSession,
        request: TransitionRequestRow,
        evaluation: TransitionEvaluationRow,
        decision: TransitionDecisionRow,
    ) -> TransitionRecord:
        if (
            evaluation.transition_request_id != request.transition_request_id
            or decision.transition_request_id != request.transition_request_id
            or decision.transition_evaluation_id != evaluation.transition_evaluation_id
        ):
            raise AuthorityConflictReadError("transition provenance is incomplete")
        outcome = DecisionOutcome(decision.outcome)
        if outcome is DecisionOutcome.ADMITTED:
            verified = await verify_historical_transition_provenance(
                session, request.transition_request_id
            )
            if verified.decision.transition_decision_id != decision.transition_decision_id:
                raise AuthorityConflictReadError("transition decision identity differs")
            effect = DerivedStateEffect.CHANGED
        else:
            if (
                decision.resulting_state != evaluation.authoritative_state
                or decision.resulting_state_version != evaluation.authoritative_state_version
            ):
                raise AuthorityConflictReadError("denied transition changed authoritative state")
            effect = DerivedStateEffect.UNCHANGED
        guard_views: list[GuardView] = []
        for raw in evaluation.guards:
            item = safe_mapping(raw)
            guard_id = safe_optional_string(item.get("guard_id"))
            satisfied = item.get("satisfied")
            if guard_id is None or not isinstance(satisfied, bool):
                raise AuthorityConflictReadError("transition guard is malformed")
            guard_views.append(
                GuardView(
                    guard_id=guard_id,
                    outcome="PASS" if satisfied else "FAIL",
                    reason=safe_optional_string(item.get("reason")),
                )
            )
        request_view = TransitionRequestView(
            transition_request_id=request.transition_request_id,
            observed_state=(
                WorkflowState(request.observed_state) if request.observed_state else None
            ),
            observed_state_version=request.observed_state_version,
            target_state=WorkflowState(request.target_state),
            requester_type=RequesterType(request.requester_type),
            runtime_mode=RuntimeMode(request.runtime_mode),
            evidence_refs=safe_string_list(request.evidence_refs),
            human_result_refs=safe_string_list(request.human_result_refs),
            judgment_refs=safe_string_list(request.judgment_refs),
            parent_request_id=request.parent_request_id,
            created_at=utc_snapshot(request.created_at),
        )
        evaluation_view = TransitionEvaluationView(
            transition_evaluation_id=evaluation.transition_evaluation_id,
            authoritative_state=(
                WorkflowState(evaluation.authoritative_state)
                if evaluation.authoritative_state
                else None
            ),
            authoritative_state_version=evaluation.authoritative_state_version,
            guards=tuple(guard_views),
            missing_guards=safe_string_list(evaluation.missing_guards),
            evaluated_at=utc_snapshot(evaluation.evaluated_at),
        )
        decision_view = TransitionDecisionView(
            transition_decision_id=decision.transition_decision_id,
            outcome=outcome,
            reason=DecisionReason(decision.reason),
            resulting_state=(
                WorkflowState(decision.resulting_state) if decision.resulting_state else None
            ),
            resulting_state_version=decision.resulting_state_version,
            decided_at=utc_snapshot(decision.decided_at),
            derived_state_effect=effect,
        )
        return TransitionRecord(
            request=request_view, evaluation=evaluation_view, decision=decision_view
        )

    async def _execution_attempt(
        self, session: AsyncSession, row: ExecutionAttemptRow
    ) -> ExecutionAttemptView:
        events = tuple(
            await session.scalars(
                select(ExecutionEventRow)
                .where(ExecutionEventRow.execution_attempt_id == row.execution_attempt_id)
                .order_by(ExecutionEventRow.event_sequence)
            )
        )
        if (
            not events
            or events[-1].event_sequence != row.latest_event_sequence
            or events[-1].status_after != row.status
            or events[-1].execution_version_after != row.execution_version
        ):
            raise AuthorityConflictReadError("execution projection is inconsistent")
        operations = tuple(
            await session.scalars(
                select(ExecutionOperationRow)
                .where(ExecutionOperationRow.execution_attempt_id == row.execution_attempt_id)
                .order_by(
                    ExecutionOperationRow.call_ordinal,
                    ExecutionOperationRow.operation_id,
                )
            )
        )
        operation_views = tuple(
            ExecutionOperationView(
                operation_id=item.operation_id,
                kind=OperationKind(item.operation_kind),
                fingerprint=item.operation_fingerprint,
                phase=ExecutionOperationPhase(item.current_phase),
                outcome=(
                    ExecutionOperationOutcome(item.outcome) if item.outcome is not None else None
                ),
                call_ordinal=item.call_ordinal,
                resource=redacted_resource_identity(item.resource_identity),
                parent_operation_id=item.parent_operation_id,
                created_at=utc_snapshot(item.created_at),
                updated_at=utc_snapshot(item.updated_at),
            )
            for item in operations
        )
        outputs = tuple(
            await session.scalars(
                select(ExecutionOutputRefRow).where(
                    ExecutionOutputRefRow.execution_attempt_id == row.execution_attempt_id,
                    ExecutionOutputRefRow.ref_kind == "ExecutionSubmissionRef",
                )
            )
        )
        if len(outputs) > 1 or (row.status == ExecutionStatus.EXECUTOR_COMPLETED.value) != bool(
            outputs
        ):
            raise AuthorityConflictReadError("execution submission projection is inconsistent")
        submission = (
            SubmissionView(
                presence=Presence.PRESENT,
                submission_ref=outputs[0].output_ref_id,
                content_hash=outputs[0].content_hash,
            )
            if outputs
            else SubmissionView(presence=Presence.NONE)
        )
        counters = _counters(row.counters)
        return ExecutionAttemptView(
            execution_attempt_id=row.execution_attempt_id,
            attempt_ordinal=row.attempt_ordinal,
            parent_attempt_id=row.parent_attempt_id,
            task_contract=TaskContractView(
                id=row.task_contract_id, version=row.task_contract_version
            ),
            runtime_mode=RuntimeMode(row.runtime_mode),
            provider_profile_id=row.provider_profile_id,
            provider_profile_version=row.provider_profile_version,
            tool_registry_id=row.tool_registry_id,
            tool_registry_version=row.tool_registry_version,
            creation_state=WorkflowState(row.creation_state),
            creation_state_version=row.creation_state_version,
            causal_state=WorkflowState(row.causal_state),
            causal_state_version=row.causal_state_version,
            status=ExecutionStatus(row.status),
            execution_version=row.execution_version,
            counters=counters,
            submission=submission,
            operations=operation_views,
            created_at=utc_snapshot(row.created_at),
            updated_at=utc_snapshot(row.updated_at),
        )

    async def evidence(self, work_run_id: str) -> QueryResult[EvidenceData]:
        async with self._snapshot() as (session, snapshot):
            run = await self._require_work_run(session, work_run_id)
            requests = tuple(
                await session.scalars(
                    select(EvidenceAdmissionRequestRow)
                    .where(EvidenceAdmissionRequestRow.work_run_id == work_run_id)
                    .order_by(
                        EvidenceAdmissionRequestRow.created_at,
                        EvidenceAdmissionRequestRow.admission_request_id,
                    )
                )
            )
            request_by_id = {item.admission_request_id: item for item in requests}
            candidate_ids = tuple(dict.fromkeys(item.candidate_id for item in requests))
            candidates = (
                tuple(
                    await session.scalars(
                        select(EvidenceCandidateRow)
                        .where(EvidenceCandidateRow.candidate_id.in_(candidate_ids))
                        .order_by(
                            EvidenceCandidateRow.created_at, EvidenceCandidateRow.candidate_id
                        )
                    )
                )
                if candidate_ids
                else ()
            )
            candidate_views = tuple(
                [await self._evidence_candidate(session, candidate) for candidate in candidates]
            )
            decisions = (
                tuple(
                    await session.scalars(
                        select(EvidenceAdmissionDecisionRow)
                        .where(
                            EvidenceAdmissionDecisionRow.admission_request_id.in_(
                                tuple(request_by_id)
                            )
                        )
                        .order_by(
                            EvidenceAdmissionDecisionRow.decided_at,
                            EvidenceAdmissionDecisionRow.decision_id,
                        )
                    )
                )
                if request_by_id
                else ()
            )
            decision_views: list[EvidenceAdmissionDecisionView] = []
            for admission_decision in decisions:
                request = request_by_id.get(admission_decision.admission_request_id)
                evaluation = await session.get(
                    EvidenceEvaluationRow, admission_decision.evaluation_id
                )
                if (
                    request is None
                    or evaluation is None
                    or evaluation.admission_request_id != request.admission_request_id
                ):
                    raise AuthorityConflictReadError("evidence decision provenance is incomplete")
                decision_views.append(
                    EvidenceAdmissionDecisionView(
                        decision_id=admission_decision.decision_id,
                        candidate_id=request.candidate_id,
                        requirement_ref=request.requirement_ref,
                        checkpoint_ref=request.checkpoint_ref,
                        outcome=EvidenceAdmissionOutcome(admission_decision.outcome),
                        reason=admission_decision.reason,
                        decided_at=utc_snapshot(admission_decision.decided_at),
                    )
                )
            admitted = tuple(
                await session.scalars(
                    select(AdmittedEvidenceRow)
                    .where(AdmittedEvidenceRow.work_run_id == work_run_id)
                    .order_by(
                        AdmittedEvidenceRow.admitted_at, AdmittedEvidenceRow.admitted_evidence_id
                    )
                )
            )
            decision_by_id = {item.decision_id: item for item in decisions}
            for admitted_row in admitted:
                related_decision = decision_by_id.get(admitted_row.decision_id)
                if (
                    related_decision is None
                    or related_decision.outcome != EvidenceAdmissionOutcome.ADMITTED.value
                ):
                    raise AuthorityConflictReadError("admitted evidence lacks an admitted decision")
            admitted_views = tuple(
                AdmittedEvidenceView(
                    admitted_evidence_id=item.admitted_evidence_id,
                    decision_id=item.decision_id,
                    candidate_id=item.candidate_id,
                    requirement_ref=item.requirement_ref,
                    checkpoint_ref=item.checkpoint_ref,
                    content_hash=item.content_hash,
                    coverage=safe_string_list(item.coverage),
                    admitted_at=utc_snapshot(item.admitted_at),
                )
                for item in admitted
            )
            satisfactions = tuple(
                await session.scalars(
                    select(EvidenceRequirementSatisfactionRow)
                    .where(EvidenceRequirementSatisfactionRow.work_run_id == work_run_id)
                    .order_by(
                        EvidenceRequirementSatisfactionRow.created_at,
                        EvidenceRequirementSatisfactionRow.satisfaction_id,
                    )
                )
            )
            admitted_ids = {item.admitted_evidence_id for item in admitted}
            if any(item.admitted_evidence_id not in admitted_ids for item in satisfactions):
                raise AuthorityConflictReadError("requirement satisfaction is orphaned")
            satisfaction_views = tuple(
                RequirementSatisfactionView(
                    satisfaction_id=item.satisfaction_id,
                    admitted_evidence_id=item.admitted_evidence_id,
                    requirement_ref=item.requirement_ref,
                    checkpoint_ref=item.checkpoint_ref,
                    coverage=safe_string_list(item.coverage),
                    created_at=utc_snapshot(item.created_at),
                )
                for item in satisfactions
            )
            set_evaluations = tuple(
                await session.scalars(
                    select(EvidenceSetEvaluationRow)
                    .where(EvidenceSetEvaluationRow.work_run_id == work_run_id)
                    .order_by(
                        EvidenceSetEvaluationRow.evaluated_at,
                        EvidenceSetEvaluationRow.evaluation_id,
                    )
                )
            )
            set_evaluation_views = tuple(
                EvidenceSetEvaluationView(
                    evaluation_id=item.evaluation_id,
                    checkpoint_ref=item.checkpoint_ref,
                    requirement_set_ref=item.requirement_set_ref,
                    outcome=EvidenceSetOutcome(item.outcome),
                    evidence_authority_revision=item.evidence_authority_revision,
                    evaluated_at=utc_snapshot(item.evaluated_at),
                )
                for item in set_evaluations
            )
            attestations = tuple(
                await session.scalars(
                    select(EvidenceSetAttestationRow)
                    .where(EvidenceSetAttestationRow.work_run_id == work_run_id)
                    .order_by(
                        EvidenceSetAttestationRow.issued_at,
                        EvidenceSetAttestationRow.attestation_id,
                    )
                )
            )
            evaluation_ids = {item.evaluation_id for item in set_evaluations}
            if any(item.evidence_set_evaluation_id not in evaluation_ids for item in attestations):
                raise AuthorityConflictReadError("evidence attestation is orphaned")
            attestation_views = tuple(
                EvidenceSetAttestationView(
                    attestation_id=item.attestation_id,
                    serialized_ref=item.serialized_ref,
                    checkpoint_ref=item.checkpoint_ref,
                    state_version=item.state_version,
                    evidence_authority_revision=item.evidence_authority_revision,
                    issued_at=utc_snapshot(item.issued_at),
                    expires_at=(utc_snapshot(item.expires_at) if item.expires_at else None),
                )
                for item in attestations
            )
            checkpoint_refs = set(item.checkpoint_ref for item in requests)
            checkpoint_refs.update(item.checkpoint_ref for item in set_evaluations)
            checkpoints = (
                tuple(
                    await session.scalars(
                        select(EvidenceCheckpointRow).where(
                            EvidenceCheckpointRow.checkpoint_ref.in_(tuple(checkpoint_refs))
                        )
                    )
                )
                if checkpoint_refs
                else ()
            )
            checkpoint_by_ref = {item.checkpoint_ref: item for item in checkpoints}
            if checkpoint_refs != set(checkpoint_by_ref):
                raise AuthorityConflictReadError("evidence checkpoint provenance is incomplete")
            requirement_set_refs = set(item.requirement_set_ref for item in checkpoints)
            requirement_set_refs.update(item.requirement_set_ref for item in requests)
            sets = (
                tuple(
                    await session.scalars(
                        select(EvidenceRequirementSetRow)
                        .where(
                            EvidenceRequirementSetRow.requirement_set_ref.in_(
                                tuple(requirement_set_refs)
                            )
                        )
                        .order_by(
                            EvidenceRequirementSetRow.issued_at,
                            EvidenceRequirementSetRow.requirement_set_ref,
                        )
                    )
                )
                if requirement_set_refs
                else ()
            )
            if requirement_set_refs != {item.requirement_set_ref for item in sets}:
                raise AuthorityConflictReadError("evidence requirement set is incomplete")
            set_views: list[EvidenceRequirementSetView] = []
            requirement_order: list[str] = []
            for set_row in sets:
                payload = safe_mapping(set_row.payload)
                ordered_requirements = safe_string_list(payload.get("ordered_requirement_refs"))
                ordered_checkpoints = safe_string_list(payload.get("ordered_checkpoint_refs"))
                if len(ordered_requirements) != len(set(ordered_requirements)):
                    raise AuthorityConflictReadError("requirement set order is ambiguous")
                requirement_order.extend(ordered_requirements)
                set_views.append(
                    EvidenceRequirementSetView(
                        requirement_set_ref=set_row.requirement_set_ref,
                        ordered_requirement_refs=ordered_requirements,
                        ordered_checkpoint_refs=ordered_checkpoints,
                        semantic_owner=EvidenceSemanticOwner(str(payload["semantic_owner"])),
                        requirement_root_hash=set_row.requirement_root_hash,
                        fingerprint=set_row.fingerprint,
                    )
                )
            requirements = (
                tuple(
                    await session.scalars(
                        select(EvidenceRequirementRow).where(
                            EvidenceRequirementRow.requirement_ref.in_(tuple(requirement_order))
                        )
                    )
                )
                if requirement_order
                else ()
            )
            requirement_by_ref = {item.requirement_ref: item for item in requirements}
            if set(requirement_order) != set(requirement_by_ref):
                raise AuthorityConflictReadError("evidence requirement provenance is incomplete")
            requirement_views = tuple(
                _requirement_view(requirement_by_ref[ref]) for ref in requirement_order
            )
            checkpoint_views = tuple(
                _checkpoint_view(checkpoint_by_ref[ref]) for ref in sorted(checkpoint_by_ref)
            )
            authority_hwm = await session.scalar(
                select(func.coalesce(func.max(EvidenceAuthorityEventRow.event_sequence), 0)).where(
                    EvidenceAuthorityEventRow.work_run_id == work_run_id
                )
            )
            revisions: dict[str, int | str] = {"workflow_state_version": run.state_version}
            if decisions:
                revisions["evidence_decision_event_high_watermark"] = max(
                    item.event_sequence for item in decisions
                )
            if authority_hwm:
                revisions["evidence_authority_event_high_watermark"] = int(authority_hwm)
            if set_evaluations:
                revisions["evidence_authority_revision"] = max(
                    item.evidence_authority_revision for item in set_evaluations
                )
            data = EvidenceData(
                work_run_id=work_run_id,
                requirement_sets=tuple(set_views),
                checkpoints=checkpoint_views,
                requirements=requirement_views,
                candidates=candidate_views,
                admission_decisions=tuple(decision_views),
                admitted_evidence=admitted_views,
                satisfactions=satisfaction_views,
                set_evaluations=set_evaluation_views,
                set_attestations=attestation_views,
            )
            return QueryResult(data, snapshot, revisions)

    async def _evidence_candidate(
        self, session: AsyncSession, row: EvidenceCandidateRow
    ) -> EvidenceCandidateView:
        binding = await session.get(EvidenceCandidateContentBindingRow, row.candidate_id)
        content_view = None
        if binding is not None:
            content = await session.get(EvidenceContentObjectRow, binding.durable_content_ref)
            if (
                content is None
                or content.payload_fingerprint != binding.durable_content_payload_fingerprint
                or content.content_hash != row.content_hash
            ):
                raise AuthorityConflictReadError("durable evidence content binding differs")
            content_view = EvidenceContentMetadataView(
                content_ref=content.serialized_ref,
                content_kind=content.content_kind,
                schema_id=content.schema_id,
                schema_version=content.schema_version,
                byte_count=content.byte_count,
                content_hash=content.content_hash,
                sensitivity=content.sensitivity,
            )
        return EvidenceCandidateView(
            candidate_id=row.candidate_id,
            candidate_version=row.candidate_version,
            candidate_fingerprint=row.candidate_fingerprint,
            checkpoint_ref=row.checkpoint_ref,
            issuer_type=row.issuer_type,
            sensitivity=row.sensitivity,
            content_hash=row.content_hash,
            created_at=utc_snapshot(row.created_at),
            durable_content=content_view,
        )

    async def human_judgment(self, work_run_id: str) -> QueryResult[HumanJudgmentData]:
        async with self._snapshot() as (session, snapshot):
            run = await self._require_work_run(session, work_run_id)
            gate, result = await self._human_views(session, work_run_id)
            judgment = await self._judgment_view(session, work_run_id)
            effect = await self._transition_effect(session, work_run_id)
            revisions: dict[str, int | str] = {"workflow_state_version": run.state_version}
            if gate.authority_revision is not None:
                revisions["human_gate_authority_revision"] = gate.authority_revision
            if result.authority_revision is not None:
                revisions["human_result_authority_revision"] = result.authority_revision
            if judgment.authority_revision is not None:
                revisions["judgment_authority_revision"] = judgment.authority_revision
            data = HumanJudgmentData(
                work_run_id=work_run_id,
                human_gate=gate,
                human_result=result,
                judgment=judgment,
                transition_effect=effect,
            )
            return QueryResult(data, snapshot, revisions)

    async def outcomes(
        self, project_id: str, *, cursor: str | None, limit: int
    ) -> QueryResult[OutcomesData]:
        validate_limit(limit)
        shape: dict[str, object] = {"endpoint": "outcomes", "project_id": project_id}
        position = decode_cursor(cursor, shape=shape) if cursor is not None else None
        async with self._snapshot() as (session, snapshot):
            all_project_runs = tuple(
                await session.scalars(
                    select(WorkRunRow)
                    .where(WorkRunRow.project_id == project_id)
                    .order_by(WorkRunRow.updated_at.desc(), WorkRunRow.work_run_id)
                )
            )
            if not all_project_runs:
                raise ReadModelNotFoundError("project has no authoritative WorkRun")
            rows: list[OutcomeRow] = []
            for run in all_project_runs:
                if WorkflowState(run.workflow_state) not in _OUTCOME_STATES:
                    continue
                await self._verify_work_run(session, run)
                if not _after_outcome_cursor(run, position):
                    continue
                judgment = await self._judgment_view(session, run.work_run_id)
                cycle = await session.scalar(
                    select(AdmittedCycleRow)
                    .where(AdmittedCycleRow.work_run_id == run.work_run_id)
                    .order_by(AdmittedCycleRow.admission_sequence.desc())
                    .limit(1)
                )
                cycle_view = (
                    AdmittedCycleSummaryView(
                        presence=Presence.PRESENT,
                        cycle_id=cycle.cycle_id,
                        cycle_ref=cycle.serialized_ref,
                        admission_sequence=cycle.admission_sequence,
                        admitted_at=utc_snapshot(cycle.admitted_at),
                    )
                    if cycle is not None
                    else AdmittedCycleSummaryView(presence=Presence.NONE)
                )
                if cycle is not None and run.workflow_state != WorkflowState.ACCEPTED.value:
                    raise AuthorityConflictReadError(
                        "only an accepted WorkRun may have an admitted Cycle"
                    )
                rows.append(
                    OutcomeRow(
                        project_id=project_id,
                        work_run_id=run.work_run_id,
                        task_contract=_task_contract(run),
                        workflow=_workflow(run),
                        judgment=_judgment_summary(judgment),
                        admitted_cycle=cycle_view,
                    )
                )
            page = rows[:limit]
            next_cursor = None
            if len(rows) > limit and page:
                last = page[-1]
                next_cursor = encode_cursor(
                    shape=shape,
                    position={
                        "updated_at": last.workflow.updated_at.astimezone(UTC).isoformat(),
                        "work_run_id": last.work_run_id,
                    },
                )
            revisions = await self._project_revisions(session, project_id)
            return QueryResult(
                OutcomesData(project_id=project_id, items=tuple(page)),
                snapshot,
                revisions,
                next_cursor=next_cursor,
            )

    async def cycle(self, cycle_id: str) -> QueryResult[CycleData]:
        async with self._snapshot() as (session, snapshot):
            cycle = await session.get(AdmittedCycleRow, cycle_id)
            if cycle is None:
                raise ReadModelNotFoundError("admitted Cycle is unavailable")
            request = await session.get(CycleAdmissionDecisionRow, cycle.decision_id)
            admission_request = await session.get(CycleAdmissionRequestRow, cycle.request_id)
            if request is None or admission_request is None:
                raise AuthorityConflictReadError("Cycle admission provenance is incomplete")
            evaluation = await session.get(CycleEvaluationRow, request.evaluation_id)
            events = tuple(
                await session.scalars(
                    select(CycleAuthorityEventRow).where(
                        CycleAuthorityEventRow.cycle_id == cycle_id
                    )
                )
            )
            if (
                evaluation is None
                or evaluation.request_id != cycle.request_id
                or request.request_id != cycle.request_id
                or request.outcome != "ADMITTED"
                or evaluation.outcome != "ACCEPTED"
                or len(events) != 1
                or events[0].event_kind != "ADMITTED"
                or events[0].payload.get("decision_id") != cycle.decision_id
            ):
                raise AuthorityConflictReadError("Cycle admission provenance is inconsistent")
            run = await self._require_work_run(session, cycle.work_run_id)
            if (
                run.project_id != cycle.project_id
                or run.workflow_state != WorkflowState.ACCEPTED.value
                or run.state_version != cycle.terminal_state_version
            ):
                raise AuthorityConflictReadError("Cycle and WorkRun terminal authority differ")
            payload = safe_mapping(cycle.payload)
            transition_request_id = safe_optional_string(payload.get("transition_request_id"))
            transition_decision_id = safe_optional_string(payload.get("transition_decision_id"))
            judgment_ref = safe_optional_string(payload.get("judgment_ref"))
            evidence_attestation_ref = safe_optional_string(payload.get("evidence_attestation_ref"))
            evidence_root = safe_optional_string(payload.get("evidence_root"))
            task_contract_id = safe_optional_string(payload.get("task_contract_id"))
            task_contract_version = safe_optional_string(payload.get("task_contract_version"))
            required = (
                transition_request_id,
                transition_decision_id,
                judgment_ref,
                evidence_attestation_ref,
                evidence_root,
                task_contract_id,
                task_contract_version,
            )
            if any(item is None for item in required):
                raise AuthorityConflictReadError("Cycle payload provenance is incomplete")
            verified_transition = await verify_historical_transition_provenance(
                session, cast(str, transition_request_id)
            )
            if (
                verified_transition.decision.transition_decision_id != transition_decision_id
                or verified_transition.decision.resulting_state is not WorkflowState.ACCEPTED
                or verified_transition.decision.resulting_state_version
                != cycle.terminal_state_version
            ):
                raise AuthorityConflictReadError("Cycle transition provenance differs")
            judgment = await verify_historical_judgment_provenance(session, cast(str, judgment_ref))
            if (
                judgment.work_run_id != cycle.work_run_id
                or judgment.judgment_kind is not JudgmentKind.ACCEPTED
            ):
                raise AuthorityConflictReadError("Cycle Judgment provenance differs")
            attestation = await session.scalar(
                select(EvidenceSetAttestationRow).where(
                    EvidenceSetAttestationRow.serialized_ref == evidence_attestation_ref
                )
            )
            if attestation is None or attestation.work_run_id != cycle.work_run_id:
                raise AuthorityConflictReadError("Cycle evidence provenance differs")
            memories = await self._current_memory(session, cycle.project_id)
            task_constraint = await self._cycle_task_constraint(session, cycle, run)
            data = CycleData(
                cycle_id=cycle.cycle_id,
                cycle_version=cycle.cycle_version,
                cycle_ref=cycle.serialized_ref,
                cycle_fingerprint=cycle.cycle_fingerprint,
                project_id=cycle.project_id,
                work_run_id=cycle.work_run_id,
                task_contract=TaskContractView(
                    id=_required_text(task_contract_id),
                    version=_required_text(task_contract_version),
                ),
                terminal_state_version=cycle.terminal_state_version,
                transition_decision_id=_required_text(transition_decision_id),
                judgment_ref=_required_text(judgment_ref),
                evidence_attestation_ref=_required_text(evidence_attestation_ref),
                evidence_root=_required_text(evidence_root),
                admission_sequence=cycle.admission_sequence,
                admitted_at=utc_snapshot(cycle.admitted_at),
                task_constraint=task_constraint,
                current_memory=memories,
            )
            revisions: dict[str, int | str] = {
                "workflow_state_version": run.state_version,
                "cycle_admission_sequence": cycle.admission_sequence,
                "cycle_authority_event_sequence": events[0].event_sequence,
                "judgment_authority_revision": judgment.authority_revision,
                "evidence_authority_revision": attestation.evidence_authority_revision,
                "task_constraint_event_high_watermark": _required_positive(
                    cycle.task_constraint_event_high_watermark
                ),
            }
            return QueryResult(data, snapshot, revisions, poll_after_ms=None)

    async def next_action(self, project_id: str) -> QueryResult[NextActionData]:
        async with self._snapshot() as (session, snapshot):
            known = await self._project_exists(session, project_id)
            if not known:
                raise ReadModelNotFoundError("project is unavailable")
            projection = await session.get(NextActionProjectionRow, project_id)
            if projection is None:
                data = NextActionData(
                    project_id=project_id,
                    projection=NextActionProjectionView(presence=Presence.NONE),
                    selection=NextActionSelectionView(presence=Presence.NONE),
                    task_issuance_candidate=TaskIssuanceCandidateView(presence=Presence.NONE),
                )
                return QueryResult(data, snapshot, {})
            await self._verify_next_action_projection(session, projection)
            projection_view = NextActionProjectionView(
                presence=Presence.PRESENT,
                state=projection.state,
                reason=projection.reason,
                project_revision=projection.project_revision,
                latest_event_sequence=projection.latest_event_sequence,
                updated_at=utc_snapshot(projection.updated_at),
            )
            selection_view = NextActionSelectionView(presence=Presence.NONE)
            candidate_view = TaskIssuanceCandidateView(presence=Presence.NONE)
            if projection.selection_id is not None:
                selection = await session.get(NextActionSelectionRow, projection.selection_id)
                if (
                    selection is None
                    or selection.project_id != project_id
                    or selection.project_revision != projection.project_revision
                ):
                    raise AuthorityConflictReadError("NextAction selection differs from projection")
                candidate = await session.scalar(
                    select(TaskIssuanceCandidateRow).where(
                        TaskIssuanceCandidateRow.selection_id == selection.selection_id
                    )
                )
                if candidate is None:
                    raise AuthorityConflictReadError("NextAction issuance candidate is missing")
                candidate_payload = safe_mapping(candidate.payload)
                required_human = safe_optional_string(
                    candidate_payload.get("required_post_issuance_human_input")
                )
                if required_human is None:
                    raise AuthorityConflictReadError("NextAction candidate is malformed")
                selection_view = NextActionSelectionView(
                    presence=Presence.PRESENT,
                    selection_id=selection.selection_id,
                    selection_ref=selection.serialized_ref,
                    action_ref=selection.action_ref,
                    project_revision=selection.project_revision,
                    selected_at=utc_snapshot(selection.selected_at),
                )
                candidate_view = TaskIssuanceCandidateView(
                    presence=Presence.PRESENT,
                    candidate_id=candidate.candidate_id,
                    issuance_owner=candidate.issuance_owner,
                    required_post_issuance_human_input=required_human,
                    created_at=utc_snapshot(candidate.created_at),
                )
            data = NextActionData(
                project_id=project_id,
                projection=projection_view,
                selection=selection_view,
                task_issuance_candidate=candidate_view,
            )
            revisions: dict[str, int | str] = {
                "next_action_project_revision": projection.project_revision,
                "next_action_event_high_watermark": projection.latest_event_sequence,
            }
            return QueryResult(data, snapshot, revisions)

    async def _queue_row(self, session: AsyncSession, run: WorkRunRow) -> QueueRow:
        attempt = await session.scalar(
            select(ExecutionAttemptRow)
            .where(ExecutionAttemptRow.work_run_id == run.work_run_id)
            .order_by(
                ExecutionAttemptRow.attempt_ordinal.desc(),
                ExecutionAttemptRow.execution_attempt_id,
            )
            .limit(1)
        )
        execution = (
            ExecutionSummaryView(
                attempt_present=True,
                execution_attempt_id=attempt.execution_attempt_id,
                attempt_ordinal=attempt.attempt_ordinal,
                status=ExecutionStatus(attempt.status),
                execution_version=attempt.execution_version,
            )
            if attempt is not None
            else ExecutionSummaryView(attempt_present=False)
        )
        gate, result = await self._human_views(session, run.work_run_id)
        judgment = await self._judgment_view(session, run.work_run_id)
        latest = await self._latest_transition_summary(session, run.work_run_id)
        next_action = await self._next_action_summary(session, run.project_id)
        return QueueRow(
            project_id=run.project_id,
            work_run_id=run.work_run_id,
            task_contract=_task_contract(run),
            task_display=_reference_task_display(),
            workflow=_workflow(run),
            execution=execution,
            human_gate=HumanGateSummaryView(
                presence=gate.presence,
                human_gate_id=gate.human_gate_id,
                status=gate.status,
                suspension_status=gate.suspension_status,
                authority_revision=gate.authority_revision,
            ),
            human_result=HumanResultSummaryView(
                presence=result.presence,
                result_kind=result.result_kind,
                authority_revision=result.authority_revision,
            ),
            judgment=_judgment_summary(judgment),
            latest_transition_decision=latest,
            next_action=next_action,
            runtime_mode=RuntimeMode(run.runtime_mode),
        )

    async def _human_views(
        self, session: AsyncSession, work_run_id: str
    ) -> tuple[HumanGateView, HumanResultView]:
        projections = tuple(
            await session.scalars(
                select(HumanGateProjectionRow)
                .where(HumanGateProjectionRow.work_run_id == work_run_id)
                .order_by(
                    HumanGateProjectionRow.updated_at.desc(),
                    HumanGateProjectionRow.human_gate_id,
                )
            )
        )
        if not projections:
            return (
                HumanGateView(presence=Presence.NONE),
                HumanResultView(presence=Presence.NONE),
            )
        projection = projections[0]
        gate = await session.get(HumanGateRow, projection.human_gate_id)
        if gate is None or gate.work_run_id != work_run_id:
            raise AuthorityConflictReadError("Human gate projection is orphaned")
        await self._verify_human_gate(session, gate, projection)
        payload = safe_mapping(gate.payload)
        gate_view = HumanGateView(
            presence=Presence.PRESENT,
            human_gate_id=gate.human_gate_id,
            gate_ref=gate.serialized_ref,
            purpose_id=_payload_text(payload, "purpose_id"),
            purpose_version=_payload_text(payload, "purpose_version"),
            status=HumanGateStatus(projection.status),
            suspension_status=HumanGateSuspensionStatus(projection.suspension_status),
            bound_state=WorkflowState(projection.bound_state),
            bound_state_version=projection.bound_state_version,
            authority_revision=projection.authority_revision,
            opened_at=utc_snapshot(gate.opened_at),
            updated_at=utc_snapshot(projection.updated_at),
        )
        if projection.current_result_ref is None:
            return gate_view, HumanResultView(presence=Presence.NONE)
        result = await session.scalar(
            select(HumanResultRow).where(
                HumanResultRow.serialized_ref == projection.current_result_ref
            )
        )
        if (
            result is None
            or result.human_gate_id != gate.human_gate_id
            or result.work_run_id != work_run_id
        ):
            raise AuthorityConflictReadError("Human result projection is orphaned")
        result_events = tuple(
            await session.scalars(
                select(HumanResultAuthorityEventRow)
                .where(HumanResultAuthorityEventRow.human_result_id == result.human_result_id)
                .order_by(HumanResultAuthorityEventRow.event_sequence)
            )
        )
        _verify_revision_events(result_events, result.authority_revision)
        result_payload = safe_mapping(result.payload)
        result_view = HumanResultView(
            presence=Presence.PRESENT,
            human_result_id=result.human_result_id,
            human_result_ref=result.serialized_ref,
            result_kind=HumanResultKind(result.result_kind),
            structured_reason_code=_payload_text(result_payload, "structured_reason_code"),
            authority_revision=result.authority_revision,
            admitted_at=utc_snapshot(result.admitted_at),
        )
        return gate_view, result_view

    async def _verify_human_gate(
        self,
        session: AsyncSession,
        gate: HumanGateRow,
        projection: HumanGateProjectionRow,
    ) -> None:
        events = tuple(
            await session.scalars(
                select(HumanGateAuthorityEventRow)
                .where(HumanGateAuthorityEventRow.human_gate_id == gate.human_gate_id)
                .order_by(HumanGateAuthorityEventRow.event_sequence)
            )
        )
        _verify_revision_events(events, projection.authority_revision)
        if not events or events[-1].event_sequence != projection.latest_event_sequence:
            raise AuthorityConflictReadError("Human gate event projection differs")
        latest_payload = safe_mapping(events[-1].payload)
        bound_state = safe_optional_string(latest_payload.get("bound_state"))
        bound_version = latest_payload.get("bound_state_version")
        if (
            bound_state is not None
            and bound_state != projection.bound_state
            or isinstance(bound_version, int)
            and bound_version != projection.bound_state_version
        ):
            raise AuthorityConflictReadError("Human gate binding differs")

    async def _judgment_view(self, session: AsyncSession, work_run_id: str) -> JudgmentView:
        projection = await session.get(JudgmentProjectionRow, work_run_id)
        if projection is None:
            return JudgmentView(presence=Presence.NONE)
        row = await session.get(JudgmentRow, projection.judgment_id)
        if row is None or row.work_run_id != work_run_id:
            raise AuthorityConflictReadError("Judgment projection is orphaned")
        verified = await verify_historical_judgment_provenance(session, row.serialized_ref)
        events = tuple(
            await session.scalars(
                select(JudgmentAuthorityEventRow)
                .where(JudgmentAuthorityEventRow.judgment_id == row.judgment_id)
                .order_by(JudgmentAuthorityEventRow.event_sequence)
            )
        )
        if (
            not events
            or events[-1].event_sequence != projection.latest_event_sequence
            or projection.authority_revision != row.authority_revision
            or any(item.event_kind == "SUPERSEDED" for item in events)
            or verified.judgment_id != row.judgment_id
        ):
            raise AuthorityConflictReadError("Judgment projection differs from authority")
        payload = safe_mapping(row.payload)
        return JudgmentView(
            presence=Presence.PRESENT,
            judgment_id=row.judgment_id,
            judgment_ref=row.serialized_ref,
            kind=JudgmentKind(row.judgment_kind),
            owner_policy=JudgmentOwnerPolicy(_payload_text(payload, "owner_policy")),
            reason_code=_payload_text(payload, "reason_code"),
            state_version=row.state_version,
            authority_revision=row.authority_revision,
            issued_at=utc_snapshot(row.issued_at),
        )

    async def _transition_effect(
        self, session: AsyncSession, work_run_id: str
    ) -> TransitionEffectView:
        row = await session.scalar(
            select(TransitionDecisionRow)
            .join(
                TransitionRequestRow,
                TransitionRequestRow.transition_request_id
                == TransitionDecisionRow.transition_request_id,
            )
            .where(TransitionRequestRow.work_run_id == work_run_id)
            .order_by(
                TransitionDecisionRow.decided_at.desc(),
                TransitionDecisionRow.transition_decision_id.desc(),
            )
            .limit(1)
        )
        if row is None:
            return TransitionEffectView(presence=Presence.NONE)
        outcome = DecisionOutcome(row.outcome)
        return TransitionEffectView(
            presence=Presence.PRESENT,
            transition_decision_id=row.transition_decision_id,
            outcome=outcome,
            resulting_state=(WorkflowState(row.resulting_state) if row.resulting_state else None),
            resulting_state_version=row.resulting_state_version,
            derived_state_effect=(
                DerivedStateEffect.CHANGED
                if outcome is DecisionOutcome.ADMITTED
                else DerivedStateEffect.UNCHANGED
            ),
        )

    async def _latest_transition_summary(
        self, session: AsyncSession, work_run_id: str
    ) -> TransitionDecisionSummaryView:
        row = await session.scalar(
            select(TransitionDecisionRow)
            .join(
                TransitionRequestRow,
                TransitionRequestRow.transition_request_id
                == TransitionDecisionRow.transition_request_id,
            )
            .where(TransitionRequestRow.work_run_id == work_run_id)
            .order_by(
                TransitionDecisionRow.decided_at.desc(),
                TransitionDecisionRow.transition_decision_id.desc(),
            )
            .limit(1)
        )
        if row is None:
            return TransitionDecisionSummaryView(presence=Presence.NONE)
        return TransitionDecisionSummaryView(
            presence=Presence.PRESENT,
            decision_id=row.transition_decision_id,
            outcome=DecisionOutcome(row.outcome),
            reason=DecisionReason(row.reason),
            resulting_state=(WorkflowState(row.resulting_state) if row.resulting_state else None),
            resulting_state_version=row.resulting_state_version,
        )

    async def _next_action_summary(
        self, session: AsyncSession, project_id: str
    ) -> NextActionSummaryView:
        projection = await session.get(NextActionProjectionRow, project_id)
        if projection is None:
            return NextActionSummaryView(presence=Presence.NONE)
        await self._verify_next_action_projection(session, projection)
        if projection.selection_id is None:
            return NextActionSummaryView(presence=Presence.NONE)
        selection = await session.get(NextActionSelectionRow, projection.selection_id)
        if selection is None or selection.project_revision != projection.project_revision:
            raise AuthorityConflictReadError("NextAction selection differs from projection")
        return NextActionSummaryView(
            presence=Presence.PRESENT,
            selection_id=selection.selection_id,
            action_ref=selection.action_ref,
            project_revision=selection.project_revision,
            selected_at=utc_snapshot(selection.selected_at),
        )

    async def _blocker(self, session: AsyncSession, work_run_id: str) -> BlockerView:
        projection = await session.get(P1_4BlockerProjectionRow, work_run_id)
        if projection is None or projection.state != "ACTIVE":
            return BlockerView(presence=Presence.NONE)
        if projection.blocker_ref is None:
            raise AuthorityConflictReadError("active blocker projection has no provenance")
        blocker = await session.get(P1_4BlockerProvenanceRow, projection.blocker_ref)
        if (
            blocker is None
            or blocker.work_run_id != work_run_id
            or blocker.blocked_epoch != projection.blocked_epoch
        ):
            raise AuthorityConflictReadError("blocker projection differs from provenance")
        return BlockerView(
            presence=Presence.PRESENT,
            blocker_ref=blocker.blocker_ref,
            blocker_kind=blocker.blocker_kind,
            reason_code=blocker.reason_code,
            resumability=blocker.resumability,
            blocked_epoch=blocker.blocked_epoch,
            authority_revision=projection.authority_revision,
            updated_at=utc_snapshot(projection.updated_at),
        )

    async def _task_constraint(self, session: AsyncSession, run: WorkRunRow) -> TaskConstraintView:
        cycle = await session.scalar(
            select(AdmittedCycleRow)
            .where(AdmittedCycleRow.work_run_id == run.work_run_id)
            .order_by(AdmittedCycleRow.admission_sequence.desc())
            .limit(1)
        )
        if cycle is not None:
            return await self._cycle_task_constraint(session, cycle, run)
        rows = tuple(
            await session.scalars(
                select(TaskConstraintRefRow)
                .where(
                    TaskConstraintRefRow.project_id == run.project_id,
                    (
                        (TaskConstraintRefRow.scope_kind == "PROJECT")
                        | (
                            (TaskConstraintRefRow.scope_kind == "TASK_CONTRACT")
                            & (TaskConstraintRefRow.task_contract_id == run.task_contract_id)
                            & (
                                TaskConstraintRefRow.task_contract_version
                                == run.task_contract_version
                            )
                        )
                        | (
                            (TaskConstraintRefRow.scope_kind == "WORK_RUN")
                            & (TaskConstraintRefRow.work_run_id == run.work_run_id)
                        )
                    ),
                )
                .order_by(TaskConstraintRefRow.issuance_sequence.desc())
            )
        )
        specificity = {"PROJECT": 1, "TASK_CONTRACT": 2, "WORK_RUN": 3}
        current_rows: list[TaskConstraintRefRow] = []
        for item in rows:
            current = await session.get(TaskConstraintCurrentRow, item.logical_key)
            if current is not None and current.current_constraint_ref == item.constraint_ref:
                value = task_constraint_ref_from_payload(item.payload)
                if (
                    value.constraint_ref != item.constraint_ref
                    or value.constraint_fingerprint != item.constraint_fingerprint
                    or value.scope.project_id != run.project_id
                ):
                    raise AuthorityConflictReadError("Task constraint projection differs")
                current_rows.append(item)
        if not current_rows:
            return TaskConstraintView(presence=Presence.NONE)
        selected = max(
            current_rows,
            key=lambda item: (specificity[item.scope_kind], item.issuance_sequence),
        )
        snapshot = await session.scalar(
            select(TaskConstraintOwnerSnapshotRow)
            .order_by(TaskConstraintOwnerSnapshotRow.owner_event_high_watermark.desc())
            .limit(1)
        )
        return TaskConstraintView(
            presence=Presence.PRESENT,
            constraint_ref=selected.constraint_ref,
            constraint_fingerprint=selected.constraint_fingerprint,
            snapshot_ref=snapshot.snapshot_ref if snapshot else None,
            snapshot_fingerprint=snapshot.snapshot_fingerprint if snapshot else None,
            owner_event_high_watermark=(snapshot.owner_event_high_watermark if snapshot else None),
        )

    async def _cycle_task_constraint(
        self,
        session: AsyncSession,
        cycle: AdmittedCycleRow,
        run: WorkRunRow,
    ) -> TaskConstraintView:
        constraint_ref = _required_text(cycle.task_constraint_ref)
        constraint_fingerprint = _required_text(cycle.task_constraint_fingerprint)
        snapshot_ref = _required_text(cycle.task_constraint_snapshot_ref)
        snapshot_fingerprint = _required_text(cycle.task_constraint_snapshot_fingerprint)
        high_watermark = _required_positive(cycle.task_constraint_event_high_watermark)
        row = await session.get(TaskConstraintRefRow, constraint_ref)
        snapshot_row = await session.get(TaskConstraintOwnerSnapshotRow, snapshot_ref)
        if row is None or snapshot_row is None:
            raise AuthorityConflictReadError("Cycle Task constraint authority is incomplete")
        value = task_constraint_ref_from_payload(dict(row.payload))
        if (
            value.constraint_ref != row.constraint_ref
            or value.constraint_fingerprint != row.constraint_fingerprint
            or value.constraint_fingerprint != constraint_fingerprint
            or value.logical_key != row.logical_key
            or value.scope.project_id != cycle.project_id
        ):
            raise AuthorityConflictReadError("Cycle Task constraint identity differs")
        if value.scope.scope_kind is TaskConstraintScopeKind.TASK_CONTRACT and (
            value.scope.task_contract_id != run.task_contract_id
            or value.scope.task_contract_version != run.task_contract_version
        ):
            raise AuthorityConflictReadError("Cycle Task constraint scope differs")
        if (
            value.scope.scope_kind is TaskConstraintScopeKind.WORK_RUN
            and value.scope.work_run_id != run.work_run_id
        ):
            raise AuthorityConflictReadError("Cycle Task constraint scope differs")

        snapshot_payload = safe_mapping(snapshot_row.payload)
        issued_at = safe_timestamp(snapshot_payload.get("issued_at"))
        if issued_at is None:
            raise AuthorityConflictReadError("Cycle Task constraint snapshot is malformed")
        snapshot_value = TaskConstraintOwnerSnapshotV1(
            snapshot_ref=str(snapshot_payload["snapshot_ref"]),
            snapshot_version=str(snapshot_payload["snapshot_version"]),
            fingerprint_schema=str(snapshot_payload["fingerprint_schema"]),
            authority_ref=str(snapshot_payload["authority_ref"]),
            authority_version=str(snapshot_payload["authority_version"]),
            authority_revision=int(str(snapshot_payload["authority_revision"])),
            owner_event_high_watermark=int(str(snapshot_payload["owner_event_high_watermark"])),
            ordered_event_prefix_root=str(snapshot_payload["ordered_event_prefix_root"]),
            issued_at=issued_at,
            snapshot_fingerprint=str(snapshot_payload["snapshot_fingerprint"]),
        )
        if (
            snapshot_value.snapshot_ref != snapshot_row.snapshot_ref
            or snapshot_value.snapshot_fingerprint != snapshot_row.snapshot_fingerprint
            or snapshot_value.snapshot_fingerprint != snapshot_fingerprint
            or snapshot_value.owner_event_high_watermark != snapshot_row.owner_event_high_watermark
            or snapshot_value.owner_event_high_watermark != high_watermark
        ):
            raise AuthorityConflictReadError("Cycle Task constraint snapshot differs")
        registry = tuple(
            await session.scalars(
                select(ExternalTaskAuthorityEventRegistryRow)
                .where(ExternalTaskAuthorityEventRegistryRow.event_sequence <= high_watermark)
                .order_by(ExternalTaskAuthorityEventRegistryRow.event_sequence)
            )
        )
        if len(registry) != high_watermark or any(
            item.event_sequence != ordinal for ordinal, item in enumerate(registry, 1)
        ):
            raise AuthorityConflictReadError("Cycle Task constraint prefix is incomplete")
        prefix_pairs = tuple((item.event_ref, item.event_fingerprint) for item in registry)
        if ordered_event_prefix_root(prefix_pairs) != snapshot_value.ordered_event_prefix_root:
            raise AuthorityConflictReadError("Cycle Task constraint prefix differs")

        history = tuple(
            await session.scalars(
                select(TaskConstraintAuthorityEventRow)
                .where(
                    TaskConstraintAuthorityEventRow.logical_key == value.logical_key,
                    TaskConstraintAuthorityEventRow.event_sequence <= high_watermark,
                )
                .order_by(TaskConstraintAuthorityEventRow.effective_sequence)
            )
        )
        current_ref: str | None = None
        for ordinal, event in enumerate(history, 1):
            if event.effective_sequence != ordinal:
                raise AuthorityConflictReadError("Cycle Task constraint history has a gap")
            if event.event_kind == "ISSUED":
                if current_ref is not None:
                    raise AuthorityConflictReadError("Cycle Task constraint history differs")
                current_ref = event.constraint_ref
            elif event.event_kind == "SUPERSEDED":
                if current_ref != event.constraint_ref or event.replacement_constraint_ref is None:
                    raise AuthorityConflictReadError("Cycle Task constraint history differs")
                current_ref = event.replacement_constraint_ref
            elif event.event_kind == "REVOKED":
                if current_ref != event.constraint_ref:
                    raise AuthorityConflictReadError("Cycle Task constraint history differs")
                current_ref = None
            else:
                raise AuthorityConflictReadError("Cycle Task constraint event kind differs")
        if current_ref != constraint_ref:
            raise AuthorityConflictReadError("Cycle Task constraint was not current at snapshot")
        return TaskConstraintView(
            presence=Presence.PRESENT,
            constraint_ref=constraint_ref,
            constraint_fingerprint=constraint_fingerprint,
            snapshot_ref=snapshot_ref,
            snapshot_fingerprint=snapshot_fingerprint,
            owner_event_high_watermark=high_watermark,
        )

    async def _current_memory(
        self, session: AsyncSession, project_id: str
    ) -> tuple[MemorySafeSummaryView, ...]:
        views = tuple(
            await session.scalars(
                select(ProjectMemoryViewRow)
                .where(
                    ProjectMemoryViewRow.project_id == project_id,
                    ProjectMemoryViewRow.state == MemoryApplicabilityState.CURRENT.value,
                )
                .order_by(ProjectMemoryViewRow.memory_lineage_key)
            )
        )
        result: list[MemorySafeSummaryView] = []
        for view in views:
            if view.current_entry_id is None:
                raise AuthorityConflictReadError("current memory view has no current entry")
            entry = await session.get(ProjectMemoryEntryRow, view.current_entry_id)
            if entry is None or entry.project_id != project_id:
                raise AuthorityConflictReadError("current memory view is orphaned")
            events = tuple(
                await session.scalars(
                    select(ProjectMemoryAuthorityEventRow)
                    .where(
                        ProjectMemoryAuthorityEventRow.memory_lineage_key == view.memory_lineage_key
                    )
                    .order_by(ProjectMemoryAuthorityEventRow.event_sequence)
                )
            )
            _verify_revision_events(events, view.authority_revision)
            if not events or events[-1].event_sequence != view.latest_event_sequence:
                raise AuthorityConflictReadError("memory event projection differs")
            privacy = PrivacyClassification(entry.privacy)
            if privacy is PrivacyClassification.NON_EXPORTABLE:
                continue
            result.append(
                MemorySafeSummaryView(
                    entry_id=entry.entry_id,
                    category=entry.category,
                    privacy=privacy.value,
                    content_fingerprint=entry.content_fingerprint,
                    applicability=view.state,
                    authority_revision=view.authority_revision,
                    created_at=utc_snapshot(entry.created_at),
                )
            )
        return tuple(result)

    async def _verify_next_action_projection(
        self, session: AsyncSession, projection: NextActionProjectionRow
    ) -> None:
        events = tuple(
            await session.scalars(
                select(NextActionAuthorityEventRow)
                .where(NextActionAuthorityEventRow.project_id == projection.project_id)
                .order_by(NextActionAuthorityEventRow.event_sequence)
            )
        )
        revision = 0
        current_selection: str | None = None
        state = "WITHDRAWN"
        for event in events:
            if event.prior_revision != revision or event.new_revision != revision + 1:
                raise AuthorityConflictReadError("NextAction event revision is discontinuous")
            revision = event.new_revision
            if event.event_kind == "SELECTED":
                current_selection = event.selection_id
                state = "CURRENT"
            elif event.event_kind == "WITHDRAWN":
                current_selection = None
                state = "WITHDRAWN"
            else:
                raise AuthorityConflictReadError("NextAction event kind is unknown")
        if (
            not events
            or projection.project_revision != revision
            or projection.latest_event_sequence != events[-1].event_sequence
            or projection.selection_id != current_selection
            or projection.state != state
        ):
            raise AuthorityConflictReadError("NextAction projection differs from event lineage")

    async def _project_exists(self, session: AsyncSession, project_id: str) -> bool:
        work_run = await session.scalar(
            select(WorkRunRow.work_run_id).where(WorkRunRow.project_id == project_id).limit(1)
        )
        if work_run is not None:
            return True
        cycle = await session.scalar(
            select(AdmittedCycleRow.cycle_id)
            .where(AdmittedCycleRow.project_id == project_id)
            .limit(1)
        )
        return cycle is not None

    async def _project_revisions(
        self, session: AsyncSession, project_id: str
    ) -> dict[str, int | str]:
        values: dict[str, int | str] = {}
        workflow_version = await session.scalar(
            select(func.max(WorkRunRow.state_version)).where(WorkRunRow.project_id == project_id)
        )
        transition_hwm = await session.scalar(
            select(func.max(TransitionDecisionRow.event_sequence))
            .join(
                TransitionRequestRow,
                TransitionRequestRow.transition_request_id
                == TransitionDecisionRow.transition_request_id,
            )
            .where(TransitionRequestRow.project_id == project_id)
        )
        next_action = await session.get(NextActionProjectionRow, project_id)
        cycle_hwm = await session.scalar(
            select(func.max(AdmittedCycleRow.admission_sequence)).where(
                AdmittedCycleRow.project_id == project_id
            )
        )
        if workflow_version is not None:
            values["workflow_state_version_max"] = int(workflow_version)
        if transition_hwm is not None:
            values["transition_event_high_watermark"] = int(transition_hwm)
        if next_action is not None:
            values["next_action_project_revision"] = next_action.project_revision
        if cycle_hwm is not None:
            values["cycle_admission_sequence_max"] = int(cycle_hwm)
        return values

    async def _work_run_revisions(
        self, session: AsyncSession, run: WorkRunRow
    ) -> dict[str, int | str]:
        values: dict[str, int | str] = {"workflow_state_version": run.state_version}
        transition_hwm = await session.scalar(
            select(func.max(TransitionDecisionRow.event_sequence))
            .join(
                TransitionRequestRow,
                TransitionRequestRow.transition_request_id
                == TransitionDecisionRow.transition_request_id,
            )
            .where(TransitionRequestRow.work_run_id == run.work_run_id)
        )
        if transition_hwm is not None:
            values["transition_event_high_watermark"] = int(transition_hwm)
        return values


def _task_contract(row: WorkRunRow) -> TaskContractView:
    return TaskContractView(id=row.task_contract_id, version=row.task_contract_version)


def _workflow(row: WorkRunRow, *, include_created: bool = False) -> WorkflowView:
    return WorkflowView(
        state=WorkflowState(row.workflow_state),
        state_version=row.state_version,
        created_at=utc_snapshot(row.created_at) if include_created else None,
        updated_at=utc_snapshot(row.updated_at),
    )


def _reference_task_display() -> TaskDisplayView:
    return TaskDisplayView(
        availability=Availability.REFERENCE_ONLY,
        message="Metadata unavailable",
    )


def _counters(value: dict[str, object]) -> DurableCountersView:
    if not value:
        return DurableCountersView()
    integers: dict[str, int] = {}
    for key in (
        "provider_calls",
        "agent_rounds",
        "tool_calls",
        "provider_retries",
        "output_bytes",
        "output_tokens",
        "budget_units",
    ):
        item = value.get(key)
        if not isinstance(item, int) or isinstance(item, bool) or item < 0:
            raise AuthorityConflictReadError("execution counters are malformed")
        integers[key] = item
    schema_version = value.get("schema_version")
    if schema_version is not None and not isinstance(schema_version, str):
        raise AuthorityConflictReadError("execution counter schema is malformed")
    started = safe_timestamp(value.get("started_at"))
    deadline = safe_timestamp(value.get("deadline_at"))
    if (started is None) != (deadline is None):
        raise AuthorityConflictReadError("execution counter timestamps differ")
    return DurableCountersView(
        schema_version=schema_version,
        provider_calls=integers["provider_calls"],
        agent_rounds=integers["agent_rounds"],
        tool_calls=integers["tool_calls"],
        provider_retries=integers["provider_retries"],
        output_bytes=integers["output_bytes"],
        output_tokens=integers["output_tokens"],
        budget_units=integers["budget_units"],
        started_at=started,
        deadline_at=deadline,
    )


def _requirement_view(row: EvidenceRequirementRow) -> EvidenceRequirementView:
    payload = safe_mapping(row.payload)
    return EvidenceRequirementView(
        requirement_ref=row.requirement_ref,
        profile=EvidenceRequirementProfile(row.profile),
        obligation=RequirementObligation(row.obligation),
        semantic_owner=EvidenceSemanticOwner.P1_6_EVIDENCE,
        evidence_type_id=_payload_text(payload, "evidence_type_id"),
        evidence_type_version=_payload_text(payload, "evidence_type_version"),
        freshness_kind=_payload_text(payload, "freshness_kind"),
        applicable_checkpoint_refs=safe_string_list(payload.get("applicable_checkpoint_refs")),
        fingerprint=row.fingerprint,
    )


def _checkpoint_view(row: EvidenceCheckpointRow) -> EvidenceCheckpointView:
    return EvidenceCheckpointView(
        checkpoint_ref=row.checkpoint_ref,
        source_state=WorkflowState(row.source_state),
        target_state=WorkflowState(row.target_state) if row.target_state else None,
        transition_purpose_id=row.transition_purpose_id,
        transition_purpose_version=row.transition_purpose_version,
        requirement_set_ref=row.requirement_set_ref,
        fingerprint=row.fingerprint,
    )


def _judgment_summary(value: JudgmentView) -> JudgmentSummaryView:
    return JudgmentSummaryView(
        presence=value.presence,
        judgment_id=value.judgment_id,
        kind=value.kind,
        owner_policy=value.owner_policy,
        authority_revision=value.authority_revision,
    )


def _payload_text(payload: dict[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise AuthorityConflictReadError("durable payload is missing safe identity metadata")
    return value


def _required_text(value: str | None) -> str:
    if value is None or not value:
        raise AuthorityConflictReadError("required durable reference is absent")
    return value


def _required_positive(value: int | None) -> int:
    if value is None or value < 1:
        raise AuthorityConflictReadError("required durable revision is absent")
    return value


def _verify_revision_events(events: tuple[Any, ...], projected_revision: int) -> None:
    if not events:
        raise AuthorityConflictReadError("authority event lineage is absent")
    revision = 0
    for event in events:
        if event.prior_revision != revision or event.new_revision != revision + 1:
            raise AuthorityConflictReadError("authority event revision is discontinuous")
        revision = event.new_revision
    if revision != projected_revision:
        raise AuthorityConflictReadError("authority projection revision differs")


def _validate_queue_filters(filters: QueueFilters) -> None:
    enum_values: tuple[tuple[str | None, type[Any]], ...] = (
        (filters.workflow_state, WorkflowState),
        (filters.execution_status, ExecutionStatus),
        (filters.human_gate_status, HumanGateStatus),
        (filters.judgment_kind, JudgmentKind),
    )
    for value, enum_type in enum_values:
        if value is not None:
            try:
                enum_type(value)
            except ValueError as exc:
                raise InvalidQueryError("filter value is invalid") from exc
    if filters.judgment_presence not in {None, Presence.NONE.value, Presence.PRESENT.value}:
        raise InvalidQueryError("judgment_presence is invalid")
    if filters.q is not None and (not filters.q or len(filters.q) > 160):
        raise InvalidQueryError("q must contain a bounded stable identifier fragment")


def _queue_shape(project_id: str, filters: QueueFilters) -> dict[str, object]:
    return {
        "endpoint": "queue",
        "project_id": project_id,
        "workflow_state": filters.workflow_state,
        "execution_status": filters.execution_status,
        "human_gate_status": filters.human_gate_status,
        "judgment_presence": filters.judgment_presence,
        "judgment_kind": filters.judgment_kind,
        "terminal": filters.terminal,
        "q": filters.q,
    }


def _queue_matches(row: QueueRow, filters: QueueFilters) -> bool:
    if filters.workflow_state is not None and row.workflow.state.value != filters.workflow_state:
        return False
    if filters.execution_status is not None and (
        row.execution.status is None or row.execution.status.value != filters.execution_status
    ):
        return False
    if filters.human_gate_status is not None and (
        row.human_gate.status is None or row.human_gate.status.value != filters.human_gate_status
    ):
        return False
    if (
        filters.judgment_presence is not None
        and row.judgment.presence.value != filters.judgment_presence
    ):
        return False
    if filters.judgment_kind is not None and (
        row.judgment.kind is None or row.judgment.kind.value != filters.judgment_kind
    ):
        return False
    if filters.terminal is not None and (row.workflow.state in TERMINAL_STATES) != filters.terminal:
        return False
    if filters.q is not None:
        needle = filters.q.casefold()
        stable_ids = (
            row.work_run_id,
            row.task_contract.id,
            row.task_contract.version,
        )
        if not any(needle in value.casefold() for value in stable_ids):
            return False
    return True


def _after_queue_cursor(row: QueueRow, position: dict[str, object] | None) -> bool:
    if position is None:
        return True
    raw_timestamp = position.get("updated_at")
    raw_run_id = position.get("work_run_id")
    if not isinstance(raw_timestamp, str) or not isinstance(raw_run_id, str):
        raise InvalidQueryError("cursor position is invalid")
    timestamp = safe_timestamp(raw_timestamp)
    if timestamp is None:
        raise InvalidQueryError("cursor position is invalid")
    updated = row.workflow.updated_at.astimezone(UTC)
    return updated < timestamp or (updated == timestamp and row.work_run_id > raw_run_id)


def _after_outcome_cursor(row: WorkRunRow, position: dict[str, object] | None) -> bool:
    if position is None:
        return True
    raw_timestamp = position.get("updated_at")
    raw_run_id = position.get("work_run_id")
    if not isinstance(raw_timestamp, str) or not isinstance(raw_run_id, str):
        raise InvalidQueryError("cursor position is invalid")
    timestamp = safe_timestamp(raw_timestamp)
    if timestamp is None:
        raise InvalidQueryError("cursor position is invalid")
    updated = utc_snapshot(row.updated_at)
    return updated < timestamp or (updated == timestamp and row.work_run_id > raw_run_id)
