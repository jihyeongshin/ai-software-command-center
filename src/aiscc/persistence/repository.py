from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from datetime import UTC, datetime, timedelta
from typing import Any, cast

from sqlalchemy import Select, func, select, text, update
from sqlalchemy.engine import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.persistence.models import (
    ExecutionAttemptRow,
    ExecutionEventRow,
    ExecutionOperationRow,
    ExecutionOutputRefRow,
    OperationEventRow,
    PrivateProviderProtocolStateRow,
    TransitionDecisionRow,
    TransitionEvaluationRow,
    TransitionRequestRow,
    WorkRunRow,
)
from aiscc.providers.events import lifecycle_result, require_legal_operation_edge
from aiscc.providers.models import (
    DurableBoundReservation,
    DurableExecutionCounters,
    ExecutionAttemptRef,
    ExecutionOperation,
    ExecutionOperationOutcome,
    ExecutionOperationPhase,
    ExecutionStatus,
    OperationKind,
    ProviderProfile,
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

_COUNTER_SCHEMA_VERSION = "AISCC-P1-5-DURABLE-COUNTERS-V1"


class PostgresExecutionRepository:
    """P1-5 projection/event authority; never mutates WorkRun state/version."""

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._evaluator: TransitionEvaluator | None = None

    async def create_attempt(
        self,
        *,
        attempt_id: str,
        work_run_id: str,
        profile_id: str,
        profile_version: str,
        registry_id: str,
        registry_version: str,
        parent_attempt_id: str | None = None,
    ) -> ExecutionAttemptRow:
        async with self._session_factory() as session, session.begin():
            await _advisory_lock(session, f"execution-run:{work_run_id}")
            existing = await session.get(ExecutionAttemptRow, attempt_id)
            if existing is not None:
                if (
                    existing.work_run_id != work_run_id
                    or existing.provider_profile_id != profile_id
                    or existing.provider_profile_version != profile_version
                    or existing.tool_registry_id != registry_id
                    or existing.tool_registry_version != registry_version
                    or existing.parent_attempt_id != parent_attempt_id
                ):
                    raise AuthorityConflictError("execution attempt identity conflict")
                return existing
            run = await session.scalar(
                select(WorkRunRow).where(WorkRunRow.work_run_id == work_run_id).with_for_update()
            )
            if run is None or run.workflow_state != WorkflowState.READY.value:
                raise AuthorityConflictError(
                    "attempt creation requires authoritative READY WorkRun"
                )
            active = await session.scalar(
                select(func.count())
                .select_from(ExecutionAttemptRow)
                .where(
                    ExecutionAttemptRow.work_run_id == work_run_id,
                    ExecutionAttemptRow.status.in_(
                        (ExecutionStatus.NOT_STARTED.value, ExecutionStatus.RUNNING.value)
                    ),
                )
            )
            if active:
                raise AuthorityConflictError("a nonterminal execution attempt already exists")
            ordinal = (
                int(
                    await session.scalar(
                        select(
                            func.coalesce(func.max(ExecutionAttemptRow.attempt_ordinal), 0)
                        ).where(ExecutionAttemptRow.work_run_id == work_run_id)
                    )
                    or 0
                )
                + 1
            )
            if ordinal == 1 and parent_attempt_id is not None:
                raise AuthorityConflictError("first execution attempt cannot name a parent")
            if ordinal > 1:
                previous = await session.scalar(
                    select(ExecutionAttemptRow)
                    .where(ExecutionAttemptRow.work_run_id == work_run_id)
                    .order_by(ExecutionAttemptRow.attempt_ordinal.desc())
                    .limit(1)
                )
                if (
                    previous is None
                    or parent_attempt_id != previous.execution_attempt_id
                    or previous.status
                    not in (
                        ExecutionStatus.EXECUTOR_COMPLETED.value,
                        ExecutionStatus.EXECUTION_FAILED.value,
                    )
                ):
                    raise AuthorityConflictError(
                        "new execution attempt requires the exact terminal parent lineage"
                    )
            now = datetime.now().astimezone()
            row = ExecutionAttemptRow(
                execution_attempt_id=attempt_id,
                work_run_id=work_run_id,
                attempt_ordinal=ordinal,
                parent_attempt_id=parent_attempt_id,
                task_contract_id=run.task_contract_id,
                task_contract_version=run.task_contract_version,
                runtime_mode=run.runtime_mode,
                provider_profile_id=profile_id,
                provider_profile_version=profile_version,
                tool_registry_id=registry_id,
                tool_registry_version=registry_version,
                creation_state=run.workflow_state,
                creation_state_version=run.state_version,
                causal_state=run.workflow_state,
                causal_state_version=run.state_version,
                status=ExecutionStatus.NOT_STARTED.value,
                execution_version=1,
                latest_event_sequence=0,
                counters={},
                created_at=now,
                updated_at=now,
            )
            session.add(row)
            await session.flush()
            event = _execution_event(
                attempt_id,
                "EXECUTION_ATTEMPT_CREATED",
                None,
                ExecutionStatus.NOT_STARTED,
                1,
                run,
                {"profile": profile_id},
                now,
            )
            session.add(event)
            await session.flush()
            row.latest_event_sequence = event.event_sequence
            await session.flush()
            return row

    async def transition_attempt(
        self,
        attempt_id: str,
        event_kind: str,
        *,
        refs: dict[str, object] | None = None,
    ) -> ExecutionStatus:
        async with self._session_factory() as session, session.begin():
            await _advisory_lock(session, f"execution-attempt:{attempt_id}")
            row = await session.scalar(
                select(ExecutionAttemptRow)
                .where(ExecutionAttemptRow.execution_attempt_id == attempt_id)
                .with_for_update()
            )
            if row is None:
                raise AuthorityConflictError("execution attempt is missing")
            await self._verify_attempt(session, row)
            await self._verify_private_protocol_integrity(session, row.execution_attempt_id)
            run = await session.get(WorkRunRow, row.work_run_id)
            workflow_left_failure = bool(
                run is not None
                and event_kind == "EXECUTION_FAILED"
                and row.status == ExecutionStatus.RUNNING.value
                and (refs or {}).get("failure_class") == "WORKFLOW_LEFT_RUNNING"
                and (
                    run.workflow_state != WorkflowState.RUNNING.value
                    or row.causal_state != run.workflow_state
                    or row.causal_state_version != run.state_version
                )
            )
            if run is None or (
                run.workflow_state != WorkflowState.RUNNING.value and not workflow_left_failure
            ):
                raise AuthorityConflictError(
                    "execution lifecycle mutation requires RUNNING WorkRun"
                )
            identity = _event_identity(attempt_id, event_kind, run.state_version, refs or {})
            existing = await session.scalar(
                select(ExecutionEventRow).where(
                    ExecutionEventRow.execution_attempt_id == attempt_id,
                    ExecutionEventRow.event_identity == identity,
                )
            )
            if existing is not None:
                return ExecutionStatus(existing.status_after)
            if (
                row.status == ExecutionStatus.RUNNING.value
                and not workflow_left_failure
                and (
                    row.causal_state != run.workflow_state
                    or row.causal_state_version != run.state_version
                )
            ):
                raise AuthorityConflictError("execution attempt is stale against current WorkRun")
            after = ExecutionStatus(lifecycle_result(row.status, event_kind))
            if event_kind == "EXECUTION_COMPLETED":
                await self._require_completion_integrity(session, row)
                completion_refs = refs or {}
                submission_id = completion_refs.get("execution_submission_ref")
                submission_hash = completion_refs.get("execution_submission_hash")
                submission_storage_ref = completion_refs.get("execution_submission_storage_ref")
                if (
                    not isinstance(submission_id, str)
                    or not isinstance(submission_hash, str)
                    or len(submission_hash) != 64
                    or any(character not in "0123456789abcdef" for character in submission_hash)
                    or not isinstance(submission_storage_ref, str)
                    or not submission_storage_ref.startswith("private://")
                ):
                    raise AuthorityConflictError(
                        "execution completion requires exact immutable submission reference fields"
                    )
                session.add(
                    ExecutionOutputRefRow(
                        output_ref_id=submission_id,
                        execution_attempt_id=attempt_id,
                        ref_kind="ExecutionSubmissionRef",
                        content_hash=submission_hash,
                        storage_ref=submission_storage_ref,
                        created_at=datetime.now().astimezone(),
                    )
                )
                await session.flush()
            now = datetime.now().astimezone()
            event = _execution_event(
                attempt_id,
                event_kind,
                ExecutionStatus(row.status),
                after,
                row.execution_version + 1,
                run,
                refs or {},
                now,
            )
            session.add(event)
            await session.flush()
            old_version = row.execution_version
            result = cast(
                CursorResult[Any],
                await session.execute(
                    update(ExecutionAttemptRow)
                    .where(
                        ExecutionAttemptRow.execution_attempt_id == attempt_id,
                        ExecutionAttemptRow.execution_version == old_version,
                    )
                    .values(
                        status=after.value,
                        execution_version=old_version + 1,
                        latest_event_sequence=event.event_sequence,
                        causal_state=run.workflow_state,
                        causal_state_version=run.state_version,
                        updated_at=now,
                    )
                ),
            )
            if result.rowcount != 1:
                raise AuthorityConflictError("execution projection CAS failed")
            return after

    async def create_operation(
        self,
        *,
        operation_id: str,
        attempt_id: str,
        kind: OperationKind,
        fingerprint: str,
        resource_identity: str,
        call_ordinal: int,
    ) -> None:
        async with self._session_factory() as session, session.begin():
            await _advisory_lock(session, f"execution-attempt:{attempt_id}")
            attempt = await session.get(ExecutionAttemptRow, attempt_id)
            if attempt is None or attempt.status != ExecutionStatus.RUNNING.value:
                raise AuthorityConflictError("operation requires RUNNING execution attempt")
            await self._verify_attempt(session, attempt)
            await self._verify_private_protocol_integrity(session, attempt.execution_attempt_id)
            run = await session.get(WorkRunRow, attempt.work_run_id)
            if run is None or run.workflow_state != WorkflowState.RUNNING.value:
                raise AuthorityConflictError("operation requires authoritative RUNNING WorkRun")
            if (
                attempt.causal_state != run.workflow_state
                or attempt.causal_state_version != run.state_version
            ):
                raise AuthorityConflictError("operation attempt binding is stale")
            existing = await session.get(ExecutionOperationRow, operation_id)
            if existing is not None:
                if (
                    existing.execution_attempt_id != attempt_id
                    or existing.operation_kind != kind.value
                    or existing.operation_fingerprint != fingerprint
                    or existing.resource_identity != resource_identity
                    or existing.call_ordinal != call_ordinal
                ):
                    raise AuthorityConflictError("operation identity fingerprint conflict")
                return
            now = datetime.now().astimezone()
            row = ExecutionOperationRow(
                operation_id=operation_id,
                execution_attempt_id=attempt_id,
                operation_kind=kind.value,
                operation_fingerprint=fingerprint,
                current_phase=ExecutionOperationPhase.PREPARED.value,
                outcome=None,
                resource_identity=resource_identity,
                call_ordinal=call_ordinal,
                parent_operation_id=None,
                latest_event_sequence=0,
                created_at=now,
                updated_at=now,
            )
            session.add(row)
            await session.flush()
            event = _operation_event(
                operation_id, None, ExecutionOperationPhase.PREPARED, None, {}, now
            )
            session.add(event)
            await session.flush()
            row.latest_event_sequence = event.event_sequence

    async def advance_operation(
        self,
        operation_id: str,
        target: ExecutionOperationPhase,
        outcome: ExecutionOperationOutcome | None = None,
        *,
        refs: dict[str, object] | None = None,
    ) -> None:
        async with self._session_factory() as session, session.begin():
            await _advisory_lock(session, f"operation:{operation_id}")
            row = await session.scalar(
                select(ExecutionOperationRow)
                .where(ExecutionOperationRow.operation_id == operation_id)
                .with_for_update()
            )
            if row is None:
                raise AuthorityConflictError("operation is missing")
            await self._verify_operation(session, row)
            attempt = await session.get(ExecutionAttemptRow, row.execution_attempt_id)
            if attempt is None or attempt.status != ExecutionStatus.RUNNING.value:
                raise AuthorityConflictError("operation attempt is not RUNNING")
            await self._verify_attempt(session, attempt)
            await self._verify_private_protocol_integrity(session, attempt.execution_attempt_id)
            run = await session.get(WorkRunRow, attempt.work_run_id)
            source = ExecutionOperationPhase(row.current_phase)
            workflow_left_terminal = bool(
                run is not None
                and attempt.status == ExecutionStatus.RUNNING.value
                and (
                    run.workflow_state != WorkflowState.RUNNING.value
                    or attempt.causal_state != run.workflow_state
                    or attempt.causal_state_version != run.state_version
                )
                and (
                    (
                        source is ExecutionOperationPhase.PREPARED
                        and target is ExecutionOperationPhase.OUTCOME_KNOWN
                        and outcome is ExecutionOperationOutcome.DENIED_BEFORE_SIDE_EFFECT
                    )
                    or (
                        source is ExecutionOperationPhase.SECURITY_ADMITTED
                        and target is ExecutionOperationPhase.OUTCOME_KNOWN
                        and outcome is ExecutionOperationOutcome.CANCELLED
                    )
                    or (
                        source is ExecutionOperationPhase.DISPATCH_STARTED
                        and target
                        in {
                            ExecutionOperationPhase.OUTCOME_KNOWN,
                            ExecutionOperationPhase.OUTCOME_UNKNOWN,
                        }
                    )
                )
            )
            if run is None or (
                (
                    run.workflow_state != WorkflowState.RUNNING.value
                    or attempt.causal_state != run.workflow_state
                    or attempt.causal_state_version != run.state_version
                )
                and not workflow_left_terminal
            ):
                raise AuthorityConflictError("operation authority is stale against current WorkRun")
            require_legal_operation_edge(source, target, outcome)
            now = datetime.now().astimezone()
            event = _operation_event(operation_id, source, target, outcome, refs or {}, now)
            session.add(event)
            await session.flush()
            row.current_phase = target.value
            row.outcome = outcome.value if outcome else None
            row.latest_event_sequence = event.event_sequence
            row.updated_at = now

    async def store_private_protocol_item(
        self,
        *,
        state_id: str,
        attempt_id: str,
        operation_id: str,
        ordinal: int,
        item_type: str,
        item_hash: str,
        call_id: str | None,
        encrypted_body_ref: str,
        body_bytes: bytes,
        classification: str,
        byte_count: int,
    ) -> None:
        async with self._session_factory() as session, session.begin():
            attempt = await session.get(ExecutionAttemptRow, attempt_id)
            if attempt is None:
                raise AuthorityConflictError("private protocol attempt is missing")
            await _advisory_lock(session, f"run:{attempt.work_run_id}")
            await _advisory_lock(session, f"execution-attempt:{attempt_id}")
            await _advisory_lock(session, f"operation:{operation_id}")
            attempt = await session.get(ExecutionAttemptRow, attempt_id)
            operation = await session.get(ExecutionOperationRow, operation_id)
            run = (
                await session.get(WorkRunRow, attempt.work_run_id) if attempt is not None else None
            )
            if (
                attempt is None
                or operation is None
                or run is None
                or operation.execution_attempt_id != attempt_id
                or attempt.status != ExecutionStatus.RUNNING.value
                or run.workflow_state != WorkflowState.RUNNING.value
                or attempt.causal_state != run.workflow_state
                or attempt.causal_state_version != run.state_version
            ):
                raise AuthorityConflictError("private protocol item authority is invalid")
            await self._verify_attempt(session, attempt)
            await self._verify_operation(session, operation)
            await self._verify_private_protocol_integrity(session, attempt_id)
            if (
                ordinal < 1
                or len(item_hash) != 64
                or any(character not in "0123456789abcdef" for character in item_hash)
                or not encrypted_body_ref.startswith("private://")
                or byte_count != len(body_bytes)
                or hashlib.sha256(body_bytes).hexdigest() != item_hash
                or not classification
            ):
                raise AuthorityConflictError("private protocol item is not canonically bounded")
            existing = await session.get(PrivateProviderProtocolStateRow, state_id)
            if existing is not None:
                if not (
                    existing.execution_attempt_id == attempt_id
                    and existing.operation_id == operation_id
                    and existing.item_ordinal == ordinal
                    and existing.item_type == item_type
                    and existing.item_hash == item_hash
                    and existing.call_id == call_id
                    and existing.encrypted_body_ref == encrypted_body_ref
                    and existing.body_bytes == body_bytes
                    and existing.classification == classification
                    and existing.byte_count == byte_count
                ):
                    raise AuthorityConflictError("private protocol item identity conflict")
                return
            session.add(
                PrivateProviderProtocolStateRow(
                    protocol_state_id=state_id,
                    execution_attempt_id=attempt_id,
                    operation_id=operation_id,
                    item_ordinal=ordinal,
                    item_type=item_type,
                    item_hash=item_hash,
                    call_id=call_id,
                    encrypted_body_ref=encrypted_body_ref,
                    body_bytes=body_bytes,
                    classification=classification,
                    byte_count=byte_count,
                    created_at=datetime.now().astimezone(),
                )
            )

    async def load_authority(
        self, *, work_run_id: str, execution_attempt_id: str
    ) -> tuple[WorkflowSnapshot, ExecutionAttemptRef]:
        async with self._session_factory() as session:
            run = await session.get(WorkRunRow, work_run_id)
            attempt = await session.get(ExecutionAttemptRow, execution_attempt_id)
            if run is None or attempt is None or attempt.work_run_id != work_run_id:
                raise AuthorityConflictError("execution authority is missing")
            await self._verify_attempt(session, attempt)
            await self._verify_private_protocol_integrity(session, execution_attempt_id)
            snapshot = WorkflowSnapshot(
                run_id=run.work_run_id,
                state=WorkflowState(run.workflow_state),
                state_version=run.state_version,
            )
            ref = ExecutionAttemptRef(
                execution_attempt_id=attempt.execution_attempt_id,
                work_run_id=attempt.work_run_id,
                task_contract_id=attempt.task_contract_id,
                task_contract_version=attempt.task_contract_version,
                state=WorkflowState(attempt.causal_state),
                state_version=attempt.causal_state_version,
                execution_version=attempt.execution_version,
                status=ExecutionStatus(attempt.status),
                issuer_ref="AISCC_P1_5_EXECUTION_REF_AUTHORITY_V1",
                runtime_mode=RuntimeMode(attempt.runtime_mode),
                project_id=run.project_id,
                provider_profile_id=attempt.provider_profile_id,
                provider_profile_version=attempt.provider_profile_version,
                tool_registry_id=attempt.tool_registry_id,
                tool_registry_version=attempt.tool_registry_version,
            )
            return snapshot, ref

    async def reserve_execution_bounds(
        self,
        *,
        operation_id: str,
        profile: ProviderProfile,
        expected_state_version: int,
        expected_execution_version: int,
        provider_calls: int = 0,
        agent_rounds: int = 0,
        tool_calls: int = 0,
        provider_retries: int = 0,
        budget_units: int = 0,
        input_bytes: int = 0,
        continuation_items: int = 0,
        continuation_bytes: int = 0,
        continuation_token_estimate: int = 0,
        now: datetime | None = None,
    ) -> DurableBoundReservation:
        deltas = {
            "provider_calls": provider_calls,
            "agent_rounds": agent_rounds,
            "tool_calls": tool_calls,
            "provider_retries": provider_retries,
            "budget_units": budget_units,
        }
        if (
            any(value < 0 for value in deltas.values())
            or min(
                input_bytes,
                continuation_items,
                continuation_bytes,
                continuation_token_estimate,
            )
            < 0
        ):
            raise AuthorityConflictError("durable bound reservation delta is invalid")
        current_time = (now or datetime.now(UTC)).astimezone(UTC)
        async with self._session_factory() as session, session.begin():
            operation = await session.get(ExecutionOperationRow, operation_id)
            if operation is None:
                raise AuthorityConflictError("bound reservation operation is missing")
            attempt = await session.get(ExecutionAttemptRow, operation.execution_attempt_id)
            if attempt is None:
                raise AuthorityConflictError("bound reservation attempt is missing")
            await _advisory_lock(session, f"run:{attempt.work_run_id}")
            await _advisory_lock(session, f"execution-attempt:{attempt.execution_attempt_id}")
            await _advisory_lock(session, f"operation:{operation_id}")
            run = await session.scalar(
                select(WorkRunRow)
                .where(WorkRunRow.work_run_id == attempt.work_run_id)
                .with_for_update()
            )
            attempt = await session.scalar(
                select(ExecutionAttemptRow)
                .where(ExecutionAttemptRow.execution_attempt_id == attempt.execution_attempt_id)
                .with_for_update()
            )
            operation = await session.scalar(
                select(ExecutionOperationRow)
                .where(ExecutionOperationRow.operation_id == operation_id)
                .with_for_update()
            )
            if attempt is None or operation is None or run is None:
                raise AuthorityConflictError("bound reservation authority disappeared")
            await self._verify_attempt(session, attempt)
            await self._verify_operation(session, operation)
            await self._verify_private_protocol_integrity(session, attempt.execution_attempt_id)
            counters = _durable_counters(attempt.counters)
            if (
                attempt.status != ExecutionStatus.RUNNING.value
                or operation.current_phase != ExecutionOperationPhase.SECURITY_ADMITTED.value
                or attempt.provider_profile_id != profile.profile_id
                or attempt.provider_profile_version != profile.version
            ):
                raise AuthorityConflictError("durable bound reservation authority is invalid")
            if (
                run.workflow_state != WorkflowState.RUNNING.value
                or run.state_version != expected_state_version
                or attempt.causal_state != run.workflow_state
                or attempt.causal_state_version != run.state_version
                or attempt.execution_version != expected_execution_version
            ):
                await _terminalize_operation(
                    session,
                    operation,
                    ExecutionOperationOutcome.CANCELLED,
                    {"reason": "WORKFLOW_LEFT_RUNNING"},
                    current_time,
                )
                await _fail_attempt(
                    session,
                    attempt,
                    run,
                    "WORKFLOW_LEFT_RUNNING",
                    "BOUND_RESERVATION_FRESHNESS_DENIED",
                    current_time,
                )
                return DurableBoundReservation(
                    False, "WORKFLOW_LEFT_RUNNING", counters, attempt.execution_version
                )
            if counters.started_at is None or counters.deadline_at is None:
                counters = DurableExecutionCounters(
                    schema_version=_COUNTER_SCHEMA_VERSION,
                    provider_calls=counters.provider_calls,
                    agent_rounds=counters.agent_rounds,
                    tool_calls=counters.tool_calls,
                    provider_retries=counters.provider_retries,
                    output_bytes=counters.output_bytes,
                    output_tokens=counters.output_tokens,
                    budget_units=counters.budget_units,
                    started_at=current_time,
                    deadline_at=current_time + timedelta(seconds=profile.total_timeout_seconds),
                )
            reason = _bound_denial_reason(
                counters,
                profile,
                deltas,
                input_bytes=input_bytes,
                continuation_items=continuation_items,
                continuation_bytes=continuation_bytes,
                continuation_token_estimate=continuation_token_estimate,
                now=current_time,
            )
            if reason is not None:
                await _terminalize_operation(
                    session,
                    operation,
                    ExecutionOperationOutcome.CANCELLED,
                    {"reason": reason},
                    current_time,
                )
                await _fail_attempt(
                    session,
                    attempt,
                    run,
                    "LIMIT_EXHAUSTED",
                    reason,
                    current_time,
                )
                return DurableBoundReservation(
                    False, reason, _durable_counters(attempt.counters), attempt.execution_version
                )
            updated = DurableExecutionCounters(
                schema_version=_COUNTER_SCHEMA_VERSION,
                provider_calls=counters.provider_calls + provider_calls,
                agent_rounds=counters.agent_rounds + agent_rounds,
                tool_calls=counters.tool_calls + tool_calls,
                provider_retries=counters.provider_retries + provider_retries,
                output_bytes=counters.output_bytes,
                output_tokens=counters.output_tokens,
                budget_units=counters.budget_units + budget_units,
                started_at=counters.started_at,
                deadline_at=counters.deadline_at,
            )
            version = await _record_counter_projection(
                session,
                attempt,
                run,
                event_kind="EXECUTION_BOUNDS_RESERVED",
                refs={"deltas": deltas, "operation_id": operation_id},
                counters=updated,
                now=current_time,
            )
            return DurableBoundReservation(True, "BOUND_RESERVED", updated, version)

    async def settle_execution_output(
        self,
        *,
        operation_id: str,
        profile: ProviderProfile,
        output_bytes: int,
        output_tokens: int,
        now: datetime | None = None,
    ) -> DurableBoundReservation:
        if output_bytes < 0 or output_tokens < 0:
            raise AuthorityConflictError("output settlement cannot be negative")
        current_time = (now or datetime.now(UTC)).astimezone(UTC)
        async with self._session_factory() as session, session.begin():
            operation = await session.get(ExecutionOperationRow, operation_id)
            if operation is None:
                raise AuthorityConflictError("output settlement operation is missing")
            attempt = await session.get(ExecutionAttemptRow, operation.execution_attempt_id)
            if attempt is None:
                raise AuthorityConflictError("output settlement attempt is missing")
            await _advisory_lock(session, f"run:{attempt.work_run_id}")
            await _advisory_lock(session, f"execution-attempt:{attempt.execution_attempt_id}")
            run = await session.scalar(
                select(WorkRunRow)
                .where(WorkRunRow.work_run_id == attempt.work_run_id)
                .with_for_update()
            )
            attempt = await session.scalar(
                select(ExecutionAttemptRow)
                .where(ExecutionAttemptRow.execution_attempt_id == attempt.execution_attempt_id)
                .with_for_update()
            )
            operation = await session.get(ExecutionOperationRow, operation_id)
            if attempt is None or operation is None or run is None:
                raise AuthorityConflictError("output settlement authority disappeared")
            await self._verify_attempt(session, attempt)
            await self._verify_operation(session, operation)
            await self._verify_private_protocol_integrity(session, attempt.execution_attempt_id)
            counters = _durable_counters(attempt.counters)
            if (
                attempt.status != ExecutionStatus.RUNNING.value
                or operation.current_phase != ExecutionOperationPhase.OUTCOME_KNOWN.value
                or operation.outcome != ExecutionOperationOutcome.PROVIDER_COMPLETED.value
            ):
                raise AuthorityConflictError("output settlement requires known provider completion")
            if (
                run.workflow_state != WorkflowState.RUNNING.value
                or attempt.causal_state != run.workflow_state
                or attempt.causal_state_version != run.state_version
            ):
                await _fail_attempt(
                    session,
                    attempt,
                    run,
                    "WORKFLOW_LEFT_RUNNING",
                    "OUTPUT_SETTLEMENT_FRESHNESS_DENIED",
                    current_time,
                )
                return DurableBoundReservation(
                    False, "WORKFLOW_LEFT_RUNNING", counters, attempt.execution_version
                )
            if (
                counters.output_bytes + output_bytes > profile.output_byte_bound
                or counters.output_tokens + output_tokens > profile.output_token_bound
            ):
                reason = (
                    "OUTPUT_BYTE_LIMIT"
                    if counters.output_bytes + output_bytes > profile.output_byte_bound
                    else "OUTPUT_TOKEN_LIMIT"
                )
                await _fail_attempt(
                    session,
                    attempt,
                    run,
                    "LIMIT_EXHAUSTED",
                    reason,
                    current_time,
                )
                return DurableBoundReservation(False, reason, counters, attempt.execution_version)
            updated = DurableExecutionCounters(
                schema_version=_COUNTER_SCHEMA_VERSION,
                provider_calls=counters.provider_calls,
                agent_rounds=counters.agent_rounds,
                tool_calls=counters.tool_calls,
                provider_retries=counters.provider_retries,
                output_bytes=counters.output_bytes + output_bytes,
                output_tokens=counters.output_tokens + output_tokens,
                budget_units=counters.budget_units,
                started_at=counters.started_at,
                deadline_at=counters.deadline_at,
            )
            version = await _record_counter_projection(
                session,
                attempt,
                run,
                event_kind="EXECUTION_OUTPUT_SETTLED",
                refs={
                    "operation_id": operation_id,
                    "output_bytes": output_bytes,
                    "output_tokens": output_tokens,
                },
                counters=updated,
                now=current_time,
            )
            return DurableBoundReservation(True, "OUTPUT_SETTLED", updated, version)

    async def start_dispatch_if_fresh(
        self,
        *,
        operation_id: str,
        expected_state_version: int,
        expected_execution_version: int,
        refs: dict[str, object] | None = None,
    ) -> bool:
        async with self._session_factory() as session, session.begin():
            operation = await session.get(ExecutionOperationRow, operation_id)
            if operation is None:
                raise AuthorityConflictError("dispatch operation is missing")
            attempt = await session.get(ExecutionAttemptRow, operation.execution_attempt_id)
            if attempt is None:
                raise AuthorityConflictError("dispatch attempt is missing")
            await _advisory_lock(session, f"run:{attempt.work_run_id}")
            await _advisory_lock(session, f"execution-attempt:{attempt.execution_attempt_id}")
            await _advisory_lock(session, f"operation:{operation_id}")
            run = await session.scalar(
                select(WorkRunRow)
                .where(WorkRunRow.work_run_id == attempt.work_run_id)
                .with_for_update()
            )
            attempt = await session.scalar(
                select(ExecutionAttemptRow)
                .where(ExecutionAttemptRow.execution_attempt_id == attempt.execution_attempt_id)
                .with_for_update()
            )
            operation = await session.scalar(
                select(ExecutionOperationRow)
                .where(ExecutionOperationRow.operation_id == operation_id)
                .with_for_update()
            )
            if attempt is None or operation is None or run is None:
                raise AuthorityConflictError("dispatch authority disappeared")
            await self._verify_attempt(session, attempt)
            await self._verify_operation(session, operation)
            await self._verify_private_protocol_integrity(session, attempt.execution_attempt_id)
            if operation.current_phase != ExecutionOperationPhase.SECURITY_ADMITTED.value:
                raise AuthorityConflictError("dispatch requires SECURITY_ADMITTED operation")
            fresh = bool(
                attempt.status == ExecutionStatus.RUNNING.value
                and run.workflow_state == WorkflowState.RUNNING.value
                and run.state_version == expected_state_version
                and attempt.causal_state == run.workflow_state
                and attempt.causal_state_version == run.state_version
                and attempt.execution_version == expected_execution_version
            )
            if not fresh:
                now = datetime.now(UTC)
                await _terminalize_operation(
                    session,
                    operation,
                    ExecutionOperationOutcome.CANCELLED,
                    {"reason": "FINAL_FRESHNESS_DENIED"},
                    now,
                )
                failure_class = (
                    "WORKFLOW_LEFT_RUNNING"
                    if run.workflow_state != WorkflowState.RUNNING.value
                    or run.state_version != expected_state_version
                    else "RECOVERY_CONFLICT"
                )
                await _fail_attempt(
                    session,
                    attempt,
                    run,
                    failure_class,
                    "FINAL_FRESHNESS_DENIED",
                    now,
                )
                return False
            await _terminalize_operation(
                session,
                operation,
                None,
                refs or {},
                datetime.now(UTC),
                target=ExecutionOperationPhase.DISPATCH_STARTED,
            )
            return True

    async def fail_operation_before_side_effect(
        self,
        *,
        operation_id: str,
        reason: str,
        failure_class: str = "FATAL",
    ) -> None:
        async with self._session_factory() as session, session.begin():
            operation = await session.get(ExecutionOperationRow, operation_id)
            if operation is None:
                raise AuthorityConflictError("denied operation is missing")
            attempt = await session.get(ExecutionAttemptRow, operation.execution_attempt_id)
            if attempt is None:
                raise AuthorityConflictError("denied operation attempt is missing")
            await _advisory_lock(session, f"run:{attempt.work_run_id}")
            await _advisory_lock(session, f"execution-attempt:{attempt.execution_attempt_id}")
            await _advisory_lock(session, f"operation:{operation_id}")
            run = await session.get(WorkRunRow, attempt.work_run_id)
            operation = await session.get(ExecutionOperationRow, operation_id)
            attempt = await session.get(ExecutionAttemptRow, attempt.execution_attempt_id)
            if run is None or operation is None or attempt is None:
                raise AuthorityConflictError("denial authority disappeared")
            await self._verify_attempt(session, attempt)
            await self._verify_operation(session, operation)
            now = datetime.now(UTC)
            source = ExecutionOperationPhase(operation.current_phase)
            if source is ExecutionOperationPhase.PREPARED:
                outcome = ExecutionOperationOutcome.DENIED_BEFORE_SIDE_EFFECT
            elif source is ExecutionOperationPhase.SECURITY_ADMITTED:
                outcome = ExecutionOperationOutcome.CANCELLED
            else:
                raise AuthorityConflictError("operation crossed dispatch before denial")
            await _terminalize_operation(session, operation, outcome, {"reason": reason}, now)
            exact_failure = (
                "WORKFLOW_LEFT_RUNNING"
                if run.workflow_state != WorkflowState.RUNNING.value
                or attempt.causal_state != run.workflow_state
                or attempt.causal_state_version != run.state_version
                else failure_class
            )
            await _fail_attempt(session, attempt, run, exact_failure, reason, now)

    async def close_workflow_left_running(self, attempt_id: str, *, reason: str) -> None:
        async with self._session_factory() as session, session.begin():
            attempt = await session.get(ExecutionAttemptRow, attempt_id)
            if attempt is None:
                raise AuthorityConflictError("workflow-left-running attempt is missing")
            await _advisory_lock(session, f"run:{attempt.work_run_id}")
            await _advisory_lock(session, f"execution-attempt:{attempt_id}")
            run = await session.get(WorkRunRow, attempt.work_run_id)
            attempt = await session.get(ExecutionAttemptRow, attempt_id)
            if run is None or attempt is None:
                raise AuthorityConflictError("workflow-left-running authority disappeared")
            await self._verify_attempt(session, attempt)
            if attempt.status != ExecutionStatus.RUNNING.value:
                return
            if (
                run.workflow_state == WorkflowState.RUNNING.value
                and attempt.causal_state == run.workflow_state
                and attempt.causal_state_version == run.state_version
            ):
                raise AuthorityConflictError("WorkRun has not left the attempt binding")
            operations = tuple(
                await session.scalars(
                    select(ExecutionOperationRow)
                    .where(ExecutionOperationRow.execution_attempt_id == attempt_id)
                    .order_by(ExecutionOperationRow.call_ordinal)
                    .with_for_update()
                )
            )
            now = datetime.now(UTC)
            for operation in operations:
                phase = ExecutionOperationPhase(operation.current_phase)
                if phase is ExecutionOperationPhase.PREPARED:
                    outcome = ExecutionOperationOutcome.DENIED_BEFORE_SIDE_EFFECT
                elif phase is ExecutionOperationPhase.SECURITY_ADMITTED:
                    outcome = ExecutionOperationOutcome.CANCELLED
                elif phase is ExecutionOperationPhase.DISPATCH_STARTED:
                    await _terminalize_operation(
                        session,
                        operation,
                        ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME,
                        {"reason": reason},
                        now,
                        target=ExecutionOperationPhase.OUTCOME_UNKNOWN,
                    )
                    continue
                else:
                    continue
                await _terminalize_operation(session, operation, outcome, {"reason": reason}, now)
            await _fail_attempt(
                session,
                attempt,
                run,
                "WORKFLOW_LEFT_RUNNING",
                reason,
                now,
            )

    async def load_durable_counters(self, attempt_id: str) -> DurableExecutionCounters:
        async with self._session_factory() as session:
            attempt = await session.get(ExecutionAttemptRow, attempt_id)
            if attempt is None:
                raise AuthorityConflictError("durable counters attempt is missing")
            await self._verify_attempt(session, attempt)
            await self._verify_private_protocol_integrity(session, attempt_id)
            return _durable_counters(attempt.counters)

    async def load_operations(self, attempt_id: str) -> tuple[ExecutionOperation, ...]:
        async with self._session_factory() as session:
            rows = tuple(
                await session.scalars(
                    select(ExecutionOperationRow)
                    .where(ExecutionOperationRow.execution_attempt_id == attempt_id)
                    .order_by(ExecutionOperationRow.call_ordinal)
                )
            )
            for row in rows:
                await self._verify_operation(session, row)
            return tuple(
                ExecutionOperation(
                    operation_id=row.operation_id,
                    execution_attempt_id=row.execution_attempt_id,
                    kind=OperationKind(row.operation_kind),
                    fingerprint=row.operation_fingerprint,
                    phase=ExecutionOperationPhase(row.current_phase),
                    call_ordinal=row.call_ordinal,
                    resource_identity=row.resource_identity,
                    outcome=(
                        ExecutionOperationOutcome(row.outcome) if row.outcome is not None else None
                    ),
                    parent_operation_id=row.parent_operation_id,
                )
                for row in rows
            )

    async def load_private_protocol_items(self, attempt_id: str) -> tuple[dict[str, object], ...]:
        async with self._session_factory() as session:
            await self._verify_private_protocol_integrity(session, attempt_id)
            rows = tuple(
                await session.scalars(
                    select(PrivateProviderProtocolStateRow)
                    .where(PrivateProviderProtocolStateRow.execution_attempt_id == attempt_id)
                    .order_by(PrivateProviderProtocolStateRow.item_ordinal)
                )
            )
            values: list[dict[str, object]] = []
            for row in rows:
                try:
                    value = json.loads(row.body_bytes.decode("utf-8"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise AuthorityConflictError(
                        "private provider protocol-state body is corrupt"
                    ) from exc
                if not isinstance(value, dict):
                    raise AuthorityConflictError(
                        "private provider protocol-state body is not an item"
                    )
                values.append(value)
            return tuple(values)

    async def store_output_ref(
        self,
        *,
        ref_id: str,
        attempt_id: str,
        kind: str,
        content_hash: str,
        storage_ref: str,
    ) -> None:
        async with self._session_factory() as session, session.begin():
            attempt = await session.get(ExecutionAttemptRow, attempt_id)
            if attempt is None:
                raise AuthorityConflictError("output reference attempt is missing")
            await _advisory_lock(session, f"run:{attempt.work_run_id}")
            await _advisory_lock(session, f"execution-attempt:{attempt_id}")
            attempt = await session.get(ExecutionAttemptRow, attempt_id)
            run = (
                await session.get(WorkRunRow, attempt.work_run_id) if attempt is not None else None
            )
            if (
                attempt is None
                or run is None
                or attempt.status != ExecutionStatus.RUNNING.value
                or run.workflow_state != WorkflowState.RUNNING.value
                or attempt.causal_state != run.workflow_state
                or attempt.causal_state_version != run.state_version
            ):
                raise AuthorityConflictError("output reference requires RUNNING execution attempt")
            await self._verify_attempt(session, attempt)
            await self._verify_private_protocol_integrity(session, attempt.execution_attempt_id)
            if kind == "ExecutionSubmissionRef":
                raise AuthorityConflictError(
                    "ExecutionSubmissionRef is created only by atomic EXECUTION_COMPLETED"
                )
            if (
                len(content_hash) != 64
                or any(character not in "0123456789abcdef" for character in content_hash)
                or not storage_ref.startswith("private://")
            ):
                raise AuthorityConflictError("output reference is not canonically bounded")
            existing = await session.get(ExecutionOutputRefRow, ref_id)
            if existing is not None:
                if not (
                    existing.execution_attempt_id == attempt_id
                    and existing.ref_kind == kind
                    and existing.content_hash == content_hash
                    and existing.storage_ref == storage_ref
                ):
                    raise AuthorityConflictError("output reference identity conflict")
                return
            session.add(
                ExecutionOutputRefRow(
                    output_ref_id=ref_id,
                    execution_attempt_id=attempt_id,
                    ref_kind=kind,
                    content_hash=content_hash,
                    storage_ref=storage_ref,
                    created_at=datetime.now().astimezone(),
                )
            )

    @staticmethod
    async def _verify_attempt(session: AsyncSession, row: ExecutionAttemptRow) -> None:
        events = tuple(
            await session.scalars(
                select(ExecutionEventRow)
                .where(ExecutionEventRow.execution_attempt_id == row.execution_attempt_id)
                .order_by(ExecutionEventRow.event_sequence)
            )
        )
        if not events or events[-1].status_after != row.status:
            raise AuthorityConflictError("execution projection/event mismatch")
        if events[-1].execution_version_after != row.execution_version:
            raise AuthorityConflictError("execution version/event mismatch")
        if events[-1].event_sequence != row.latest_event_sequence:
            raise AuthorityConflictError("execution latest sequence mismatch")
        projected: dict[str, object] = {}
        for event in events:
            counter_projection = event.refs.get("counter_projection")
            if counter_projection is not None:
                if not isinstance(counter_projection, dict):
                    raise AuthorityConflictError("execution counter event is malformed")
                projected = counter_projection
        if row.counters != projected:
            raise AuthorityConflictError("execution counter projection/event mismatch")

    @staticmethod
    async def _verify_operation(session: AsyncSession, row: ExecutionOperationRow) -> None:
        events = tuple(
            await session.scalars(
                select(OperationEventRow)
                .where(OperationEventRow.operation_id == row.operation_id)
                .order_by(OperationEventRow.event_sequence)
            )
        )
        if not events or events[-1].target_phase != row.current_phase:
            raise AuthorityConflictError("operation projection/event mismatch")
        if (
            events[-1].outcome != row.outcome
            or events[-1].event_sequence != row.latest_event_sequence
        ):
            raise AuthorityConflictError("operation outcome/sequence mismatch")

    @staticmethod
    async def _require_completion_integrity(
        session: AsyncSession, row: ExecutionAttemptRow
    ) -> None:
        operations = tuple(
            await session.scalars(
                select(ExecutionOperationRow).where(
                    ExecutionOperationRow.execution_attempt_id == row.execution_attempt_id
                )
            )
        )
        for operation in operations:
            await PostgresExecutionRepository._verify_operation(session, operation)
            if operation.current_phase != ExecutionOperationPhase.OUTCOME_KNOWN.value:
                raise AuthorityConflictError(
                    "execution completion requires every operation to have a known outcome"
                )
        ref_kinds = set(
            await session.scalars(
                select(ExecutionOutputRefRow.ref_kind).where(
                    ExecutionOutputRefRow.execution_attempt_id == row.execution_attempt_id
                )
            )
        )
        if "AgentOutputRef" not in ref_kinds:
            raise AuthorityConflictError(
                "execution completion requires an immutable AgentOutputRef"
            )

    @staticmethod
    async def _verify_private_protocol_integrity(session: AsyncSession, attempt_id: str) -> None:
        items = tuple(
            await session.scalars(
                select(PrivateProviderProtocolStateRow)
                .where(PrivateProviderProtocolStateRow.execution_attempt_id == attempt_id)
                .order_by(PrivateProviderProtocolStateRow.item_ordinal)
            )
        )
        for expected_ordinal, item in enumerate(items, start=1):
            operation = await session.get(ExecutionOperationRow, item.operation_id)
            if (
                item.item_ordinal != expected_ordinal
                or operation is None
                or operation.execution_attempt_id != attempt_id
                or len(item.item_hash) != 64
                or any(character not in "0123456789abcdef" for character in item.item_hash)
                or not item.encrypted_body_ref.startswith("private://")
                or item.byte_count != len(item.body_bytes)
                or hashlib.sha256(item.body_bytes).hexdigest() != item.item_hash
                or not item.classification
            ):
                raise AuthorityConflictError("private provider protocol-state integrity mismatch")
            try:
                body = json.loads(item.body_bytes.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise AuthorityConflictError(
                    "private provider protocol-state body is corrupt"
                ) from exc
            if (
                not isinstance(body, dict)
                or body.get("type") != item.item_type
                or body.get("call_id") != item.call_id
            ):
                raise AuthorityConflictError(
                    "private provider protocol-state item binding mismatch"
                )
        outputs = tuple(
            await session.scalars(
                select(ExecutionOutputRefRow).where(
                    ExecutionOutputRefRow.execution_attempt_id == attempt_id
                )
            )
        )
        for output in outputs:
            if (
                len(output.content_hash) != 64
                or any(character not in "0123456789abcdef" for character in output.content_hash)
                or not output.storage_ref.startswith("private://")
            ):
                raise AuthorityConflictError("execution output reference integrity mismatch")

    async def decide(
        self,
        request: TransitionRequest,
        facts: tuple[TrustedGuardFact, ...],
        *,
        failure_injector: FailureInjector | None = None,
    ) -> TransitionDecision:
        if self._evaluator is None:
            raise AuthorityConflictError("transition evaluator is not configured")
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


class PostgresTransitionRepository(PostgresExecutionRepository):
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        evaluator: TransitionEvaluator,
    ) -> None:
        super().__init__(session_factory)
        self._evaluator = evaluator


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


def _durable_counters(value: dict[str, object]) -> DurableExecutionCounters:
    if not value:
        return DurableExecutionCounters(
            schema_version=_COUNTER_SCHEMA_VERSION,
            provider_calls=0,
            agent_rounds=0,
            tool_calls=0,
            provider_retries=0,
            output_bytes=0,
            output_tokens=0,
            budget_units=0,
            started_at=None,
            deadline_at=None,
        )
    exact_keys = {
        "schema_version",
        "provider_calls",
        "agent_rounds",
        "tool_calls",
        "provider_retries",
        "output_bytes",
        "output_tokens",
        "budget_units",
        "started_at",
        "deadline_at",
    }
    if set(value) != exact_keys or value.get("schema_version") != _COUNTER_SCHEMA_VERSION:
        raise AuthorityConflictError("durable execution counter schema is invalid")
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
        raw = value.get(key)
        if type(raw) is not int or raw < 0:
            raise AuthorityConflictError("durable execution counter value is invalid")
        integers[key] = raw

    def timestamp(key: str) -> datetime | None:
        raw = value.get(key)
        if raw is None:
            return None
        if not isinstance(raw, str):
            raise AuthorityConflictError("durable execution timestamp is invalid")
        try:
            parsed = datetime.fromisoformat(raw)
        except ValueError as exc:
            raise AuthorityConflictError("durable execution timestamp is invalid") from exc
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            raise AuthorityConflictError("durable execution timestamp is not timezone-aware")
        return parsed.astimezone(UTC)

    started_at = timestamp("started_at")
    deadline_at = timestamp("deadline_at")
    if (started_at is None) != (deadline_at is None):
        raise AuthorityConflictError("durable execution deadline pair is incomplete")
    if started_at is not None and deadline_at is not None and deadline_at <= started_at:
        raise AuthorityConflictError("durable execution deadline is invalid")
    return DurableExecutionCounters(
        schema_version=_COUNTER_SCHEMA_VERSION,
        provider_calls=integers["provider_calls"],
        agent_rounds=integers["agent_rounds"],
        tool_calls=integers["tool_calls"],
        provider_retries=integers["provider_retries"],
        output_bytes=integers["output_bytes"],
        output_tokens=integers["output_tokens"],
        budget_units=integers["budget_units"],
        started_at=started_at,
        deadline_at=deadline_at,
    )


def _counter_projection(counters: DurableExecutionCounters) -> dict[str, object]:
    return {
        "schema_version": counters.schema_version,
        "provider_calls": counters.provider_calls,
        "agent_rounds": counters.agent_rounds,
        "tool_calls": counters.tool_calls,
        "provider_retries": counters.provider_retries,
        "output_bytes": counters.output_bytes,
        "output_tokens": counters.output_tokens,
        "budget_units": counters.budget_units,
        "started_at": counters.started_at.astimezone(UTC).isoformat()
        if counters.started_at is not None
        else None,
        "deadline_at": counters.deadline_at.astimezone(UTC).isoformat()
        if counters.deadline_at is not None
        else None,
    }


def _bound_denial_reason(
    counters: DurableExecutionCounters,
    profile: ProviderProfile,
    deltas: dict[str, int],
    *,
    input_bytes: int,
    continuation_items: int,
    continuation_bytes: int,
    continuation_token_estimate: int,
    now: datetime,
) -> str | None:
    if counters.deadline_at is not None and now >= counters.deadline_at:
        return "WALL_TIME_LIMIT"
    if input_bytes > profile.input_byte_bound:
        return "INPUT_BYTE_LIMIT"
    if continuation_items > profile.continuation_item_maximum:
        return "CONTINUATION_ITEM_LIMIT"
    if continuation_bytes > profile.continuation_byte_bound:
        return "CONTINUATION_BYTE_LIMIT"
    if continuation_token_estimate > profile.continuation_token_estimate_bound:
        return "CONTINUATION_TOKEN_LIMIT"
    limits = (
        ("provider_calls", profile.provider_call_maximum, "PROVIDER_CALL_LIMIT"),
        ("agent_rounds", profile.agent_round_trip_maximum, "AGENT_ROUND_LIMIT"),
        ("tool_calls", profile.tool_call_maximum, "TOOL_CALL_LIMIT"),
        ("provider_retries", profile.provider_retry_maximum, "PROVIDER_RETRY_LIMIT"),
        ("budget_units", profile.budget_unit_maximum, "BUDGET_LIMIT"),
    )
    for name, maximum, reason in limits:
        if getattr(counters, name) + deltas[name] > maximum:
            return reason
    if deltas["provider_calls"] and counters.output_bytes >= profile.output_byte_bound:
        return "OUTPUT_BYTE_LIMIT"
    if deltas["provider_calls"] and counters.output_tokens >= profile.output_token_bound:
        return "OUTPUT_TOKEN_LIMIT"
    return None


async def _record_counter_projection(
    session: AsyncSession,
    attempt: ExecutionAttemptRow,
    run: WorkRunRow,
    *,
    event_kind: str,
    refs: dict[str, object],
    counters: DurableExecutionCounters,
    now: datetime,
) -> int:
    projection = _counter_projection(counters)
    event_refs = {**refs, "counter_projection": projection}
    version = attempt.execution_version + 1
    event = _execution_event(
        attempt.execution_attempt_id,
        event_kind,
        ExecutionStatus.RUNNING,
        ExecutionStatus.RUNNING,
        version,
        run,
        event_refs,
        now,
    )
    session.add(event)
    await session.flush()
    attempt.counters = projection
    attempt.execution_version = version
    attempt.latest_event_sequence = event.event_sequence
    attempt.causal_state = run.workflow_state
    attempt.causal_state_version = run.state_version
    attempt.updated_at = now
    await session.flush()
    return version


async def _terminalize_operation(
    session: AsyncSession,
    operation: ExecutionOperationRow,
    outcome: ExecutionOperationOutcome | None,
    refs: dict[str, object],
    now: datetime,
    *,
    target: ExecutionOperationPhase = ExecutionOperationPhase.OUTCOME_KNOWN,
) -> None:
    source = ExecutionOperationPhase(operation.current_phase)
    require_legal_operation_edge(source, target, outcome)
    event = _operation_event(operation.operation_id, source, target, outcome, refs, now)
    session.add(event)
    await session.flush()
    operation.current_phase = target.value
    operation.outcome = outcome.value if outcome is not None else None
    operation.latest_event_sequence = event.event_sequence
    operation.updated_at = now
    await session.flush()


async def _fail_attempt(
    session: AsyncSession,
    attempt: ExecutionAttemptRow,
    run: WorkRunRow,
    failure_class: str,
    reason: str,
    now: datetime,
) -> int:
    if attempt.status != ExecutionStatus.RUNNING.value:
        raise AuthorityConflictError("only a RUNNING attempt can be terminalized as failed")
    projection = _counter_projection(_durable_counters(attempt.counters))
    refs: dict[str, object] = {
        "failure_class": failure_class,
        "reason": reason,
        "counter_projection": projection,
    }
    version = attempt.execution_version + 1
    event = _execution_event(
        attempt.execution_attempt_id,
        "EXECUTION_FAILED",
        ExecutionStatus.RUNNING,
        ExecutionStatus.EXECUTION_FAILED,
        version,
        run,
        refs,
        now,
    )
    session.add(event)
    await session.flush()
    attempt.status = ExecutionStatus.EXECUTION_FAILED.value
    attempt.execution_version = version
    attempt.latest_event_sequence = event.event_sequence
    attempt.counters = projection
    attempt.causal_state = run.workflow_state
    attempt.causal_state_version = run.state_version
    attempt.updated_at = now
    await session.flush()
    return version


def _event_identity(
    owner_id: str, event_kind: str, state_version: int, refs: dict[str, object]
) -> str:
    body = json.dumps(
        {
            "owner_id": owner_id,
            "event_kind": event_kind,
            "state_version": state_version,
            "refs": refs,
        },
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(body).hexdigest()


def _execution_event(
    attempt_id: str,
    event_kind: str,
    before: ExecutionStatus | None,
    after: ExecutionStatus,
    version: int,
    run: WorkRunRow,
    refs: dict[str, object],
    now: datetime,
) -> ExecutionEventRow:
    identity = _event_identity(attempt_id, event_kind, run.state_version, refs)
    return ExecutionEventRow(
        event_id=f"execution-event-{identity}",
        event_identity=identity,
        execution_attempt_id=attempt_id,
        event_kind=event_kind,
        status_before=before.value if before else None,
        status_after=after.value,
        execution_version_after=version,
        causal_state=run.workflow_state,
        causal_state_version=run.state_version,
        payload_hash=hashlib.sha256(
            json.dumps(refs, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest(),
        refs=refs,
        created_at=now,
    )


def _operation_event(
    operation_id: str,
    source: ExecutionOperationPhase | None,
    target: ExecutionOperationPhase,
    outcome: ExecutionOperationOutcome | None,
    refs: dict[str, object],
    now: datetime,
) -> OperationEventRow:
    identity = _event_identity(
        operation_id,
        ":".join(
            (
                source.value if source else "NONE",
                target.value,
                outcome.value if outcome else "NONE",
            )
        ),
        0,
        refs,
    )
    return OperationEventRow(
        event_id=f"operation-event-{identity}",
        event_identity=identity,
        operation_id=operation_id,
        source_phase=source.value if source else None,
        target_phase=target.value,
        outcome=outcome.value if outcome else None,
        refs=refs,
        created_at=now,
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
