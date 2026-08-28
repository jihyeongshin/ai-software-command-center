from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from datetime import datetime
from typing import Any, cast

from sqlalchemy import Select, select, text, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.persistence.models import (
    TransitionDecisionRow,
    TransitionEvaluationRow,
    TransitionRequestRow,
    WorkRunRow,
)
from aiscc.workflow.evaluator import TransitionEvaluator
from aiscc.workflow.guards import TrustedGuardFact
from aiscc.workflow.models import (
    AuthorityConflictError,
    DecisionOutcome,
    DecisionReason,
    RequestIdentityConflictError,
    TransitionDecision,
    TransitionEvaluation,
    TransitionRequest,
    WorkRun,
)
from aiscc.workflow.ports import FailureInjector, FailurePoint


class PostgresTransitionRepository:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        evaluator: TransitionEvaluator,
    ) -> None:
        self._session_factory = session_factory
        self._evaluator = evaluator

    async def decide(
        self,
        request: TransitionRequest,
        facts: tuple[TrustedGuardFact, ...],
        *,
        failure_injector: FailureInjector | None = None,
    ) -> TransitionDecision:
        fingerprint = _request_fingerprint(request, facts)
        async with self._session_factory() as session, session.begin():
            await _advisory_lock(session, f"run:{request.work_run_id}")
            await _advisory_lock(session, f"request:{request.transition_request_id}")
            existing_request = await session.get(
                TransitionRequestRow, request.transition_request_id
            )
            if existing_request is not None:
                if existing_request.request_fingerprint != fingerprint:
                    raise RequestIdentityConflictError(
                        "transition_request_id is already bound to different immutable content"
                    )
                existing_decision = await self._decision_for_request(
                    session, request.transition_request_id
                )
                if existing_decision is None:
                    raise AuthorityConflictError("request exists without immutable decision")
                return existing_decision

            current_row = await session.scalar(
                select(WorkRunRow)
                .where(WorkRunRow.work_run_id == request.work_run_id)
                .with_for_update()
            )
            current = await self._verify_consistency_in_session(
                session,
                request.work_run_id,
                current_row,
                incoming_request=request,
            )
            evaluation, decision = self._evaluator.evaluate(
                request=request,
                current=current,
                facts=facts,
            )
            session.add(_request_row(request, fingerprint))
            await session.flush()
            session.add(_evaluation_row(evaluation))
            await session.flush()
            session.add(_decision_row(decision))
            await session.flush()
            _inject(failure_injector, FailurePoint.AFTER_PROVENANCE_BEFORE_PROJECTION)

            if decision.outcome is DecisionOutcome.ADMITTED:
                if current_row is None:
                    session.add(
                        WorkRunRow(
                            work_run_id=request.work_run_id,
                            project_id=request.project_id,
                            task_contract_id=request.task_contract_id,
                            task_contract_version=request.task_contract_version,
                            workflow_state=request.target_state.value,
                            state_version=decision.resulting_state_version,
                            runtime_mode=request.runtime_mode.value,
                            created_at=decision.decided_at,
                            updated_at=decision.decided_at,
                        )
                    )
                else:
                    result = cast(
                        CursorResult[Any],
                        await session.execute(
                            update(WorkRunRow)
                            .where(
                                WorkRunRow.work_run_id == request.work_run_id,
                                WorkRunRow.state_version == current_row.state_version,
                                WorkRunRow.workflow_state == current_row.workflow_state,
                            )
                            .values(
                                workflow_state=request.target_state.value,
                                state_version=decision.resulting_state_version,
                                updated_at=decision.decided_at,
                            )
                        ),
                    )
                    if result.rowcount != 1:
                        raise AuthorityConflictError("atomic projection compare-and-swap failed")
                await session.flush()
                _inject(failure_injector, FailurePoint.AFTER_PROJECTION_BEFORE_COMMIT)
            return decision

    async def get_work_run(self, work_run_id: str) -> WorkRun | None:
        async with self._session_factory() as session:
            row = await session.get(WorkRunRow, work_run_id)
            return _work_run_from_row(row) if row is not None else None

    async def get_decision(self, transition_request_id: str) -> TransitionDecision | None:
        async with self._session_factory() as session:
            return await self._decision_for_request(session, transition_request_id)

    async def history(self, work_run_id: str) -> tuple[TransitionDecision, ...]:
        async with self._session_factory() as session:
            rows = await session.scalars(_history_query(work_run_id))
            return tuple(_decision_from_row(row) for row in rows)

    async def verify_consistency(self, work_run_id: str) -> WorkRun:
        async with self._session_factory() as session, session.begin():
            await _advisory_lock(session, f"run:{work_run_id}")
            projection_row = await session.scalar(
                select(WorkRunRow).where(WorkRunRow.work_run_id == work_run_id).with_for_update()
            )
            current = await self._verify_consistency_in_session(
                session,
                work_run_id,
                projection_row,
            )
            if current is None:
                raise AuthorityConflictError("authoritative WorkRun projection is missing")
            return current

    @staticmethod
    async def _verify_consistency_in_session(
        session: AsyncSession,
        work_run_id: str,
        projection_row: WorkRunRow | None,
        *,
        incoming_request: TransitionRequest | None = None,
    ) -> WorkRun | None:
        if projection_row is None:
            requests = tuple(
                await session.scalars(
                    select(TransitionRequestRow)
                    .where(TransitionRequestRow.work_run_id == work_run_id)
                    .order_by(
                        TransitionRequestRow.created_at,
                        TransitionRequestRow.transition_request_id,
                    )
                )
            )
            for historical_request in requests:
                evaluations = tuple(
                    await session.scalars(
                        select(TransitionEvaluationRow).where(
                            TransitionEvaluationRow.transition_request_id
                            == historical_request.transition_request_id
                        )
                    )
                )
                decisions = tuple(
                    await session.scalars(
                        select(TransitionDecisionRow).where(
                            TransitionDecisionRow.transition_request_id
                            == historical_request.transition_request_id
                        )
                    )
                )
                if len(evaluations) != 1 or len(decisions) != 1:
                    raise AuthorityConflictError(
                        "projection-free transition provenance is partial or orphaned"
                    )
                evaluation = evaluations[0]
                decision = decisions[0]
                if (
                    decision.transition_evaluation_id != evaluation.transition_evaluation_id
                    or evaluation.authoritative_state is not None
                    or evaluation.authoritative_state_version != 0
                    or decision.outcome != DecisionOutcome.DENIED.value
                    or decision.resulting_state is not None
                    or decision.resulting_state_version != 0
                ):
                    raise AuthorityConflictError(
                        "authoritative WorkRun projection is missing and provenance is not "
                        "denied-only NONE/v0"
                    )
                if incoming_request is not None and not _same_run_identity(
                    historical_request, incoming_request
                ):
                    raise AuthorityConflictError(
                        "denied precreation provenance has a different run identity"
                    )
            return None

        joined = await session.execute(
            select(TransitionDecisionRow, TransitionEvaluationRow)
            .join(
                TransitionRequestRow,
                TransitionRequestRow.transition_request_id
                == TransitionDecisionRow.transition_request_id,
            )
            .join(
                TransitionEvaluationRow,
                TransitionEvaluationRow.transition_evaluation_id
                == TransitionDecisionRow.transition_evaluation_id,
            )
            .where(TransitionRequestRow.work_run_id == work_run_id)
            .order_by(TransitionDecisionRow.event_sequence)
        )
        reconstructed_state: WorkflowState | None = None
        reconstructed_version = 0
        admitted_count = 0
        for decision_row, evaluation_row in joined:
            if decision_row.outcome != DecisionOutcome.ADMITTED.value:
                continue
            evaluated_state = (
                WorkflowState(evaluation_row.authoritative_state)
                if evaluation_row.authoritative_state is not None
                else None
            )
            if (
                evaluated_state is not reconstructed_state
                or evaluation_row.authoritative_state_version != reconstructed_version
                or decision_row.resulting_state_version != reconstructed_version + 1
                or decision_row.resulting_state is None
            ):
                raise AuthorityConflictError(
                    "admitted provenance is not a contiguous state/version lineage"
                )
            reconstructed_state = WorkflowState(decision_row.resulting_state)
            reconstructed_version = decision_row.resulting_state_version
            admitted_count += 1
        if admitted_count == 0:
            raise AuthorityConflictError("projection has no admitted provenance")
        if (
            reconstructed_state is None
            or reconstructed_state.value != projection_row.workflow_state
            or reconstructed_version != projection_row.state_version
        ):
            raise AuthorityConflictError("projection and append-only admitted provenance disagree")
        return _work_run_from_row(projection_row)

    @staticmethod
    async def _decision_for_request(
        session: AsyncSession, transition_request_id: str
    ) -> TransitionDecision | None:
        row = await session.scalar(
            select(TransitionDecisionRow).where(
                TransitionDecisionRow.transition_request_id == transition_request_id
            )
        )
        return _decision_from_row(row) if row is not None else None


def _history_query(work_run_id: str) -> Select[tuple[TransitionDecisionRow]]:
    return (
        select(TransitionDecisionRow)
        .join(
            TransitionRequestRow,
            TransitionRequestRow.transition_request_id
            == TransitionDecisionRow.transition_request_id,
        )
        .where(TransitionRequestRow.work_run_id == work_run_id)
        .order_by(TransitionDecisionRow.event_sequence)
    )


def _same_run_identity(
    historical: TransitionRequestRow,
    incoming: TransitionRequest,
) -> bool:
    return (
        historical.project_id == incoming.project_id
        and historical.task_contract_id == incoming.task_contract_id
        and historical.task_contract_version == incoming.task_contract_version
        and historical.work_run_id == incoming.work_run_id
        and historical.runtime_mode == incoming.runtime_mode.value
    )


async def _advisory_lock(session: AsyncSession, key: str) -> None:
    await session.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:lock_key, 0))"),
        {"lock_key": key},
    )


def _inject(injector: FailureInjector | None, point: FailurePoint) -> None:
    if injector is not None:
        injector(point)


def _request_fingerprint(request: TransitionRequest, facts: Sequence[TrustedGuardFact]) -> str:
    payload = {
        "request": {
            "transition_request_id": request.transition_request_id,
            "project_id": request.project_id,
            "task_contract_id": request.task_contract_id,
            "task_contract_version": request.task_contract_version,
            "work_run_id": request.work_run_id,
            "observed_state": request.observed_state.value if request.observed_state else None,
            "observed_state_version": request.observed_state_version,
            "target_state": request.target_state.value,
            "requester_identity": request.requester_identity,
            "requester_type": request.requester_type.value,
            "runtime_mode": request.runtime_mode.value,
            "evidence_refs": list(request.evidence_refs),
            "human_result_refs": list(request.human_result_refs),
            "judgment_refs": list(request.judgment_refs),
            "parent_request_id": request.parent_request_id,
            "created_at": request.created_at.isoformat(),
        },
        "facts": [
            {
                "guard_id": fact.guard_id.value,
                "semantic_owner": fact.semantic_owner.value,
                "satisfied": fact.satisfied,
                "reason": fact.reason,
                "authority_ref": fact.authority_ref,
                "bound_refs": list(fact.bound_refs),
                "task_contract_id": fact.task_contract_id,
                "task_contract_version": fact.task_contract_version,
                "work_run_id": fact.work_run_id,
                "state_version": fact.state_version,
            }
            for fact in sorted(facts, key=lambda item: item.guard_id.value)
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


def _request_row(request: TransitionRequest, fingerprint: str) -> TransitionRequestRow:
    return TransitionRequestRow(
        transition_request_id=request.transition_request_id,
        request_fingerprint=fingerprint,
        project_id=request.project_id,
        task_contract_id=request.task_contract_id,
        task_contract_version=request.task_contract_version,
        work_run_id=request.work_run_id,
        observed_state=request.observed_state.value if request.observed_state else None,
        observed_state_version=request.observed_state_version,
        target_state=request.target_state.value,
        requester_identity=request.requester_identity,
        requester_type=request.requester_type.value,
        runtime_mode=request.runtime_mode.value,
        evidence_refs=list(request.evidence_refs),
        human_result_refs=list(request.human_result_refs),
        judgment_refs=list(request.judgment_refs),
        parent_request_id=request.parent_request_id,
        created_at=request.created_at,
    )


def _evaluation_row(evaluation: TransitionEvaluation) -> TransitionEvaluationRow:
    return TransitionEvaluationRow(
        transition_evaluation_id=evaluation.transition_evaluation_id,
        transition_request_id=evaluation.transition_request_id,
        authoritative_state=(
            evaluation.authoritative_state.value
            if evaluation.authoritative_state is not None
            else None
        ),
        authoritative_state_version=evaluation.authoritative_state_version,
        guards=[
            {
                "guard_id": guard.guard_id.value,
                "semantic_owner": guard.semantic_owner.value,
                "satisfied": guard.satisfied,
                "reason": guard.reason,
                "authority_ref": guard.authority_ref,
                "bound_refs": list(guard.bound_refs),
            }
            for guard in evaluation.guards
        ],
        missing_guards=[guard.value for guard in evaluation.missing_guards],
        evaluated_at=evaluation.evaluated_at,
    )


def _decision_row(decision: TransitionDecision) -> TransitionDecisionRow:
    return TransitionDecisionRow(
        transition_decision_id=decision.transition_decision_id,
        transition_evaluation_id=decision.transition_evaluation_id,
        transition_request_id=decision.transition_request_id,
        outcome=decision.outcome.value,
        reason=decision.reason.value,
        resulting_state=(
            decision.resulting_state.value if decision.resulting_state is not None else None
        ),
        resulting_state_version=decision.resulting_state_version,
        admitting_owner=decision.admitting_owner,
        kernel_version=decision.kernel_version,
        decided_at=decision.decided_at,
    )


def _work_run_from_row(row: WorkRunRow) -> WorkRun:
    return WorkRun(
        project_id=row.project_id,
        task_contract_id=row.task_contract_id,
        task_contract_version=row.task_contract_version,
        work_run_id=row.work_run_id,
        state=WorkflowState(row.workflow_state),
        state_version=row.state_version,
        runtime_mode=RuntimeMode(row.runtime_mode),
        created_at=_aware(row.created_at),
        updated_at=_aware(row.updated_at),
    )


def _decision_from_row(row: TransitionDecisionRow) -> TransitionDecision:
    return TransitionDecision(
        transition_decision_id=row.transition_decision_id,
        transition_evaluation_id=row.transition_evaluation_id,
        transition_request_id=row.transition_request_id,
        outcome=DecisionOutcome(row.outcome),
        reason=DecisionReason(row.reason),
        resulting_state=(WorkflowState(row.resulting_state) if row.resulting_state else None),
        resulting_state_version=row.resulting_state_version,
        admitting_owner=row.admitting_owner,
        kernel_version=row.kernel_version,
        decided_at=_aware(row.decided_at),
    )


def _aware(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise AuthorityConflictError("database returned a naive authority timestamp")
    return value
