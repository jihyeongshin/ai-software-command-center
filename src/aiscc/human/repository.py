from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import asdict, replace
from datetime import UTC, datetime, timedelta
from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.contracts.workflow import WorkflowState
from aiscc.evidence.models import EvidenceSensitivity, canonical_hash
from aiscc.evidence.repository import (
    HistoricalEvidenceProvenanceError,
    verify_historical_set_attestation_provenance,
)
from aiscc.human.models import (
    HUMAN_AUTHORITY_VERSION,
    HUMAN_GATE_PURPOSE_ID,
    HUMAN_GATE_PURPOSE_VERSION,
    HUMAN_GUARD_ATTESTATION_VERSION,
    HUMAN_GUARD_AUTHORITY_ID,
    AuthenticatedHumanPrincipal,
    HumanActionAuthority,
    HumanAuthorityError,
    HumanAuthorityReason,
    HumanGate,
    HumanGateReservation,
    HumanGateStatus,
    HumanGateSuspensionStatus,
    HumanGuardAttestation,
    HumanP1_7EvidenceProducerRef,
    HumanRequiredEvidenceBinding,
    HumanResult,
    HumanResultIdentityConflictError,
    HumanResultKind,
    human_guard_attestation_fingerprint,
    human_guard_attestation_payload,
)
from aiscc.persistence.models import (
    HumanGateAuthorityEventRow,
    HumanGateProjectionRow,
    HumanGateRow,
    HumanGuardAttestationRow,
    HumanP1_7EvidenceProducerRow,
    HumanResultAuthorityEventRow,
    HumanResultRow,
    WorkRunRow,
)
from aiscc.persistence.repository import (
    HistoricalTransitionProvenanceError,
    acquire_human_result_transaction_lock,
    acquire_work_run_transaction_lock,
    verify_historical_transition_provenance,
)
from aiscc.workflow.guards import required_bound_refs
from aiscc.workflow.models import GuardId, GuardSemanticOwner, TransitionRequest


class PostgresHumanAuthorityRepository:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._clock = clock or (lambda: datetime.now(UTC))

    def _now(self) -> datetime:
        return self._clock().astimezone(UTC)

    async def issue_current_gate_action_authority(
        self,
        *,
        gate_ref: str,
        principal: AuthenticatedHumanPrincipal,
        issuer_token: object,
        allowed_roles_by_selector: Mapping[str, frozenset[str]],
        authority_version: str,
        idempotency_scope: str,
        ttl_seconds: int,
    ) -> HumanActionAuthority:
        """Seal Human action authority only from current durable gate authority."""
        if not isinstance(gate_ref, str) or not gate_ref or ttl_seconds <= 0:
            raise HumanAuthorityError(HumanAuthorityReason.UNKNOWN_HUMAN_GATE)
        expired = False
        value: HumanActionAuthority | None = None
        async with self._session_factory() as session, session.begin():
            initial = await session.scalar(
                select(HumanGateRow).where(HumanGateRow.serialized_ref == gate_ref)
            )
            if initial is None:
                raise HumanAuthorityError(HumanAuthorityReason.UNKNOWN_HUMAN_GATE)
            await acquire_work_run_transaction_lock(session, initial.work_run_id)
            row = await session.scalar(
                select(HumanGateRow)
                .where(HumanGateRow.serialized_ref == gate_ref)
                .with_for_update()
            )
            run = await session.scalar(
                select(WorkRunRow)
                .where(WorkRunRow.work_run_id == initial.work_run_id)
                .with_for_update()
            )
            projection = await session.scalar(
                select(HumanGateProjectionRow)
                .where(HumanGateProjectionRow.human_gate_id == initial.human_gate_id)
                .with_for_update()
            )
            if row is None or run is None or projection is None:
                raise HumanAuthorityError(HumanAuthorityReason.HUMAN_GATE_NOT_CURRENT)
            await _verify_gate_consistency_in_session(session, row, projection)
            issued_at = self._now()
            expired = await _expire_pending_gate_in_session(session, row, projection, issued_at)
            if not expired:
                gate = _gate_from_row(row, projection)
                allowed_roles = allowed_roles_by_selector.get(
                    gate.designated_principal_selector_fingerprint
                )
                if (
                    principal._issuer_token is not issuer_token
                    or issued_at >= principal.authentication_expires_at
                    or allowed_roles is None
                    or not allowed_roles.intersection(principal.internal_role_refs)
                ):
                    raise HumanAuthorityError(HumanAuthorityReason.HUMAN_PRINCIPAL_NOT_AUTHORIZED)
                if (
                    projection.status != HumanGateStatus.PENDING.value
                    or projection.suspension_status != HumanGateSuspensionStatus.ACTIVE.value
                ):
                    raise HumanAuthorityError(HumanAuthorityReason.HUMAN_GATE_CLOSED)
                if (
                    run.task_contract_id != gate.task_contract_id
                    or run.task_contract_version != gate.task_contract_version
                    or run.work_run_id != gate.work_run_id
                    or run.workflow_state != WorkflowState.HUMAN_REQUIRED.value
                    or run.state_version != gate.bound_state_version
                    or projection.bound_state != run.workflow_state
                    or projection.bound_state_version != run.state_version
                    or projection.authority_epoch != f"{run.work_run_id}:{run.state_version}"
                ):
                    raise HumanAuthorityError(HumanAuthorityReason.HUMAN_GATE_NOT_CURRENT)
                deadlines = [
                    issued_at + timedelta(seconds=ttl_seconds),
                    principal.authentication_expires_at,
                ]
                if gate.expires_at is not None:
                    deadlines.append(gate.expires_at)
                value = HumanActionAuthority(
                    "human-action-"
                    + canonical_hash(
                        [principal.principal_id, gate.serialized_ref, idempotency_scope]
                    ),
                    authority_version,
                    principal.principal_id,
                    principal.authentication_session_id,
                    gate.serialized_ref,
                    gate.gate_authority_revision,
                    gate.task_contract_id,
                    gate.task_contract_version,
                    gate.work_run_id,
                    gate.bound_state_version,
                    frozenset(HumanResultKind),
                    issued_at,
                    min(deadlines),
                    idempotency_scope,
                    issuer_token,
                )
        if expired:
            raise HumanAuthorityError(HumanAuthorityReason.HUMAN_GATE_EXPIRED)
        assert value is not None
        return value

    async def submit_result(
        self,
        *,
        human_result_id: str,
        human_result_version: str,
        gate_ref: str,
        principal: AuthenticatedHumanPrincipal,
        action_authority: HumanActionAuthority,
        result_kind: HumanResultKind,
        structured_reason_code: str,
        reason_vocabulary_version: str,
        idempotency_key: str,
        private_comment_ref: str | None = None,
        private_comment_hash: str | None = None,
        sensitivity: EvidenceSensitivity = EvidenceSensitivity.INTERNAL,
        submitted_at: datetime | None = None,
    ) -> HumanResult:
        caller_submitted_at = submitted_at.astimezone(UTC) if submitted_at is not None else None
        proposal_fingerprint = _human_result_proposal_fingerprint(
            human_result_id=human_result_id,
            human_result_version=human_result_version,
            gate_ref=gate_ref,
            principal=principal,
            action_authority=action_authority,
            result_kind=result_kind,
            structured_reason_code=structured_reason_code,
            reason_vocabulary_version=reason_vocabulary_version,
            idempotency_key=idempotency_key,
            private_comment_ref=private_comment_ref,
            private_comment_hash=private_comment_hash,
            sensitivity=sensitivity,
            caller_submitted_at=caller_submitted_at,
        )
        expired = False
        async with self._session_factory() as session, session.begin():
            await acquire_work_run_transaction_lock(session, action_authority.work_run_id)
            await acquire_human_result_transaction_lock(session, human_result_id)
            existing = await session.get(HumanResultRow, human_result_id)
            if existing is not None:
                durable = await _verify_human_result_historical_provenance_in_session(
                    session, existing
                )
                if existing.payload.get("proposal_fingerprint") != proposal_fingerprint:
                    raise HumanResultIdentityConflictError(
                        HumanAuthorityReason.HUMAN_RESULT_IDENTITY_CONFLICT
                    )
                return durable
            run = await session.scalar(
                select(WorkRunRow)
                .where(WorkRunRow.work_run_id == action_authority.work_run_id)
                .with_for_update()
            )
            gate_row = await session.scalar(
                select(HumanGateRow)
                .where(HumanGateRow.serialized_ref == gate_ref)
                .with_for_update()
            )
            projection = (
                await session.scalar(
                    select(HumanGateProjectionRow)
                    .where(HumanGateProjectionRow.human_gate_id == gate_row.human_gate_id)
                    .with_for_update()
                )
                if gate_row is not None
                else None
            )
            authoritative_now = self._now()
            if run is not None and gate_row is not None and projection is not None:
                await _verify_gate_consistency_in_session(session, gate_row, projection)
                expired = await _expire_pending_gate_in_session(
                    session, gate_row, projection, authoritative_now
                )
            if not expired:
                _validate_result_authority(
                    run,
                    gate_row,
                    projection,
                    principal,
                    action_authority,
                    result_kind,
                    authoritative_now,
                )
                assert run is not None and gate_row is not None and projection is not None
                gate = _gate_from_row(gate_row, projection)
                submitted = caller_submitted_at or authoritative_now
                provisional = HumanResult(
                    human_result_id,
                    human_result_version,
                    "",
                    gate_ref,
                    projection.authority_revision,
                    gate.purpose_id,
                    gate.purpose_version,
                    principal.principal_id,
                    f"{principal.principal_authority_id}@{principal.principal_authority_version}",
                    f"{action_authority.action_authority_id}@{action_authority.action_authority_version}",
                    gate.task_contract_id,
                    gate.task_contract_version,
                    gate.work_run_id,
                    WorkflowState.HUMAN_REQUIRED,
                    run.state_version,
                    result_kind,
                    structured_reason_code,
                    reason_vocabulary_version,
                    private_comment_ref,
                    private_comment_hash,
                    sensitivity,
                    submitted,
                    authoritative_now,
                    idempotency_key,
                    "AISCC_P1_7_HUMAN_RESULT_AUTHORITY_V1",
                    "p1-7-human-result-v1",
                    1,
                )
                result = replace(
                    provisional,
                    human_result_fingerprint=_human_result_fingerprint(provisional),
                )
                session.add(_result_row(result, gate_row.human_gate_id, proposal_fingerprint))
                await session.flush()
                event = HumanResultAuthorityEventRow(
                    event_id=(
                        f"human-result-event-{canonical_hash([result.serialized_ref, 'ADMITTED'])}"
                    ),
                    human_result_id=result.human_result_id,
                    event_kind="ADMITTED",
                    prior_revision=0,
                    new_revision=1,
                    payload={"winner_rule": "FIRST_DURABLY_ADMITTED", "gate_ref": gate_ref},
                    created_at=authoritative_now,
                )
                session.add(event)
                await session.flush()
                gate_event = HumanGateAuthorityEventRow(
                    event_id="human-gate-event-"
                    + canonical_hash([gate.serialized_ref, "RESOLVED", result.serialized_ref]),
                    human_gate_id=gate.human_gate_id,
                    event_kind="RESOLVED",
                    prior_revision=projection.authority_revision,
                    new_revision=projection.authority_revision + 1,
                    payload={
                        "human_result_ref": result.serialized_ref,
                        "bound_state": WorkflowState.HUMAN_REQUIRED.value,
                        "bound_state_version": run.state_version,
                    },
                    created_at=authoritative_now,
                )
                session.add(gate_event)
                await session.flush()
                projection.status = HumanGateStatus.RESOLVED.value
                projection.suspension_status = HumanGateSuspensionStatus.NOT_APPLICABLE.value
                projection.authority_revision += 1
                projection.current_result_ref = result.serialized_ref
                projection.latest_event_sequence = gate_event.event_sequence
                projection.updated_at = authoritative_now
                return result
        if expired:
            raise HumanAuthorityError(HumanAuthorityReason.HUMAN_GATE_EXPIRED)
        raise AssertionError("HumanResult admission ended without an authority outcome")

    async def expire_gate_if_needed(self, gate_ref: str) -> bool:
        async with self._session_factory() as session, session.begin():
            row = await session.scalar(
                select(HumanGateRow).where(HumanGateRow.serialized_ref == gate_ref)
            )
            if row is None:
                return False
            await acquire_work_run_transaction_lock(session, row.work_run_id)
            row = await session.scalar(
                select(HumanGateRow)
                .where(HumanGateRow.serialized_ref == gate_ref)
                .with_for_update()
            )
            projection = (
                await session.scalar(
                    select(HumanGateProjectionRow)
                    .where(HumanGateProjectionRow.human_gate_id == row.human_gate_id)
                    .with_for_update()
                )
                if row is not None
                else None
            )
            if row is None or projection is None:
                return False
            await _verify_gate_consistency_in_session(session, row, projection)
            now = self._now()
            return await _expire_pending_gate_in_session(session, row, projection, now)

    async def load_gate(self, serialized_ref: str) -> HumanGate | None:
        async with self._session_factory() as session:
            row = await session.scalar(
                select(HumanGateRow).where(HumanGateRow.serialized_ref == serialized_ref)
            )
            if row is None:
                return None
            projection = await session.get(HumanGateProjectionRow, row.human_gate_id)
            return _gate_from_row(row, projection) if projection is not None else None

    async def load_result(self, serialized_ref: str) -> HumanResult | None:
        async with self._session_factory() as session:
            row = await session.scalar(
                select(HumanResultRow).where(HumanResultRow.serialized_ref == serialized_ref)
            )
            return _result_from_row(row) if row is not None else None

    async def load_current_gate(self, work_run_id: str) -> HumanGate | None:
        async with self._session_factory() as session:
            run = await session.get(WorkRunRow, work_run_id)
            if run is None:
                return None
            projection = await session.scalar(
                select(HumanGateProjectionRow).where(
                    HumanGateProjectionRow.work_run_id == work_run_id,
                    HumanGateProjectionRow.authority_epoch == f"{work_run_id}:{run.state_version}",
                )
            )
            if projection is None:
                return None
            row = await session.get(HumanGateRow, projection.human_gate_id)
            if row is None:
                return None
            await _verify_gate_consistency_in_session(session, row, projection)
            return _gate_from_row(row, projection)

    async def verify_consistency(self, work_run_id: str) -> tuple[HumanGate, ...]:
        async with self._session_factory() as session, session.begin():
            await acquire_work_run_transaction_lock(session, work_run_id)
            rows = tuple(
                await session.scalars(
                    select(HumanGateRow)
                    .where(HumanGateRow.work_run_id == work_run_id)
                    .order_by(HumanGateRow.opened_at, HumanGateRow.human_gate_id)
                )
            )
            values: list[HumanGate] = []
            for row in rows:
                projection = await session.get(HumanGateProjectionRow, row.human_gate_id)
                if projection is None:
                    raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
                await _verify_gate_consistency_in_session(session, row, projection)
                values.append(_gate_from_row(row, projection))
            return tuple(values)

    async def supersede_gate(
        self,
        current: HumanGate,
        reservation: HumanGateReservation,
        *,
        authority_id: str,
        authority_version: str,
    ) -> HumanGate:
        changed_at = self._now()
        async with self._session_factory() as session, session.begin():
            await acquire_work_run_transaction_lock(session, current.work_run_id)
            run = await session.scalar(
                select(WorkRunRow)
                .where(WorkRunRow.work_run_id == current.work_run_id)
                .with_for_update()
            )
            old_row = await session.get(HumanGateRow, current.human_gate_id)
            old_projection = await session.scalar(
                select(HumanGateProjectionRow)
                .where(HumanGateProjectionRow.human_gate_id == current.human_gate_id)
                .with_for_update()
            )
            if (
                run is None
                or old_row is None
                or old_projection is None
                or run.workflow_state != WorkflowState.HUMAN_REQUIRED.value
                or run.state_version != current.bound_state_version
                or old_projection.status != HumanGateStatus.RESOLVED.value
                or old_projection.authority_revision != current.gate_authority_revision
                or reservation.work_run_id != current.work_run_id
                or reservation.opened_from_state_version != run.state_version
            ):
                raise HumanAuthorityError(HumanAuthorityReason.HUMAN_GATE_NOT_CURRENT)
            await _verify_gate_consistency_in_session(session, old_row, old_projection)
            old_revision = old_projection.authority_revision
            superseded_event = HumanGateAuthorityEventRow(
                event_id="human-gate-event-"
                + canonical_hash(
                    [current.serialized_ref, "SUPERSEDED", old_revision, reservation.human_gate_id]
                ),
                human_gate_id=current.human_gate_id,
                event_kind="SUPERSEDED",
                prior_revision=old_revision,
                new_revision=old_revision + 1,
                payload={
                    "replacement_gate_ref": (
                        f"p1-7-gate:{reservation.human_gate_version}:{reservation.human_gate_id}"
                    )
                },
                created_at=changed_at,
            )
            session.add(superseded_event)
            await session.flush()
            old_projection.status = HumanGateStatus.CANCELLED.value
            old_projection.suspension_status = HumanGateSuspensionStatus.NOT_APPLICABLE.value
            old_projection.authority_revision = old_revision + 1
            old_projection.authority_epoch = (
                f"{old_projection.authority_epoch}:superseded:{old_revision + 1}"
            )
            old_projection.latest_event_sequence = superseded_event.event_sequence
            old_projection.updated_at = changed_at
            serialized_ref = (
                f"p1-7-gate:{reservation.human_gate_version}:{reservation.human_gate_id}"
            )
            new_row = HumanGateRow(
                human_gate_id=reservation.human_gate_id,
                serialized_ref=serialized_ref,
                gate_fingerprint=reservation.gate_fingerprint,
                task_contract_id=reservation.task_contract_id,
                task_contract_version=reservation.task_contract_version,
                work_run_id=reservation.work_run_id,
                opened_from_state=WorkflowState.HUMAN_REQUIRED.value,
                opened_from_state_version=run.state_version,
                bound_state_version=run.state_version,
                payload={
                    "human_gate_version": reservation.human_gate_version,
                    "purpose_id": reservation.purpose_id,
                    "purpose_version": reservation.purpose_version,
                    "opening_transition_request_id": "P1_7_AUTHORITY_CORRECTION",
                    "opening_transition_decision_id": "P1_7_AUTHORITY_CORRECTION",
                    "authority_policy_ref": reservation.authority_policy_ref,
                    "authority_policy_version": reservation.authority_policy_version,
                    "designated_principal_selector_fingerprint": (
                        reservation.designated_principal_selector_fingerprint
                    ),
                    "gate_authority_id": authority_id,
                    "gate_authority_version": authority_version,
                    "expires_at": (
                        reservation.expires_at.isoformat() if reservation.expires_at else None
                    ),
                    "supersedes_gate_ref": current.serialized_ref,
                },
                opened_at=changed_at,
            )
            session.add(new_row)
            await session.flush()
            opened_event = HumanGateAuthorityEventRow(
                event_id="human-gate-event-"
                + canonical_hash([serialized_ref, "OPENED_CORRECTION"]),
                human_gate_id=reservation.human_gate_id,
                event_kind="OPENED_CORRECTION",
                prior_revision=0,
                new_revision=1,
                payload={
                    "supersedes_gate_ref": current.serialized_ref,
                    "bound_state": WorkflowState.HUMAN_REQUIRED.value,
                    "bound_state_version": run.state_version,
                },
                created_at=changed_at,
            )
            session.add(opened_event)
            await session.flush()
            new_projection = HumanGateProjectionRow(
                human_gate_id=reservation.human_gate_id,
                work_run_id=reservation.work_run_id,
                authority_epoch=f"{reservation.work_run_id}:{run.state_version}",
                status=HumanGateStatus.PENDING.value,
                suspension_status=HumanGateSuspensionStatus.ACTIVE.value,
                authority_revision=1,
                bound_state=WorkflowState.HUMAN_REQUIRED.value,
                bound_state_version=run.state_version,
                current_result_ref=None,
                latest_event_sequence=opened_event.event_sequence,
                updated_at=changed_at,
            )
            session.add(new_projection)
            await session.flush()
            return _gate_from_row(new_row, new_projection)

    async def create_producer_ref(
        self,
        *,
        result_ref: str,
        checkpoint_ref: str,
        evidence_type_id: str,
        evidence_type_version: str,
        subject_id: str,
        scope_id: str,
        resource_id: str | None,
        content_hash: str,
        sensitivity: EvidenceSensitivity,
        export_policy: str,
    ) -> HumanP1_7EvidenceProducerRef:
        issued_at = self._now()
        async with self._session_factory() as session, session.begin():
            result_row = await session.scalar(
                select(HumanResultRow).where(HumanResultRow.serialized_ref == result_ref)
            )
            if result_row is None:
                raise HumanAuthorityError(HumanAuthorityReason.HUMAN_RESULT_STALE)
            await acquire_work_run_transaction_lock(session, result_row.work_run_id)
            gate_row = await session.get(HumanGateRow, result_row.human_gate_id)
            projection = await session.get(HumanGateProjectionRow, result_row.human_gate_id)
            run = await session.get(WorkRunRow, result_row.work_run_id)
            if (
                gate_row is None
                or projection is None
                or run is None
                or projection.current_result_ref != result_ref
                or projection.status != HumanGateStatus.RESOLVED.value
            ):
                raise HumanAuthorityError(HumanAuthorityReason.HUMAN_RESULT_STALE)
            result = _result_from_row(result_row)
            producer_id = "human-producer-" + canonical_hash(
                [result_ref, checkpoint_ref, evidence_type_id, content_hash]
            )
            provisional = HumanP1_7EvidenceProducerRef(
                producer_id,
                "p1-7-producer-v1",
                "",
                result.task_contract_id,
                result.task_contract_version,
                result.work_run_id,
                WorkflowState(run.workflow_state),
                run.state_version,
                result.human_gate_ref,
                projection.authority_revision,
                result.serialized_ref,
                result.result_authority_revision,
                f"private-human-subject:{canonical_hash(result.principal_id)[:24]}",
                checkpoint_ref,
                evidence_type_id,
                evidence_type_version,
                subject_id,
                scope_id,
                resource_id,
                content_hash,
                sensitivity,
                export_policy,
                "AISCC_P1_7_HUMAN_EVIDENCE_PRODUCER_V1",
                "p1-7-producer-authority-v1",
                issued_at,
                None,
            )
            value = replace(provisional, fingerprint=_producer_fingerprint(provisional))
            existing = await session.get(HumanP1_7EvidenceProducerRow, producer_id)
            if existing is None:
                session.add(_producer_row(value))
            elif existing.fingerprint != value.fingerprint:
                raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
            return value

    async def load_producer_ref(self, serialized_ref: str) -> HumanP1_7EvidenceProducerRef | None:
        async with self._session_factory() as session:
            row = await session.scalar(
                select(HumanP1_7EvidenceProducerRow).where(
                    HumanP1_7EvidenceProducerRow.serialized_ref == serialized_ref
                )
            )
            if row is None:
                return None
            value = _producer_from_row(row)
            result = await session.scalar(
                select(HumanResultRow).where(
                    HumanResultRow.serialized_ref == value.human_result_ref
                )
            )
            projection = (
                await session.get(HumanGateProjectionRow, result.human_gate_id)
                if result is not None
                else None
            )
            if (
                value.fingerprint != _producer_fingerprint(value)
                or result is None
                or projection is None
                or projection.current_result_ref != value.human_result_ref
                or projection.authority_revision != value.gate_authority_revision
            ):
                return None
            return value


async def verify_historical_producer_ref_in_session(
    session: AsyncSession,
    serialized_ref: str,
) -> HumanP1_7EvidenceProducerRef:
    """Verify immutable HUMAN_P1_7 producer issuance without current projections."""
    rows = tuple(
        await session.scalars(
            select(HumanP1_7EvidenceProducerRow).where(
                HumanP1_7EvidenceProducerRow.serialized_ref == serialized_ref
            )
        )
    )
    if not rows:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    if len(rows) != 1:
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    row = rows[0]
    try:
        value = _producer_from_row(row)
    except (KeyError, TypeError, ValueError) as exc:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE) from exc
    expected = _producer_row(value)
    if (
        row.producer_ref_id != value.producer_ref_id
        or row.serialized_ref != value.serialized_ref
        or row.serialized_ref != serialized_ref
        or row.fingerprint != value.fingerprint
        or row.fingerprint != _producer_fingerprint(value)
        or row.human_result_ref != value.human_result_ref
        or row.work_run_id != value.work_run_id
        or row.payload != expected.payload
        or row.issued_at.astimezone(UTC) != value.issued_at
        or value.producer_ref_version != "p1-7-producer-v1"
        or value.authority_id != "AISCC_P1_7_HUMAN_EVIDENCE_PRODUCER_V1"
        or value.authority_version != "p1-7-producer-authority-v1"
    ):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    result_rows = tuple(
        await session.scalars(
            select(HumanResultRow).where(
                HumanResultRow.serialized_ref == value.human_result_ref
            )
        )
    )
    if not result_rows:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    if len(result_rows) != 1:
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    result = await _verify_human_result_historical_provenance_in_session(
        session, result_rows[0]
    )
    if (
        value.human_result_ref != result.serialized_ref
        or value.result_authority_revision != result.result_authority_revision
        or value.human_gate_ref != result.human_gate_ref
        or value.gate_authority_revision != result.gate_authority_revision + 1
        or value.task_contract_id != result.task_contract_id
        or value.task_contract_version != result.task_contract_version
        or value.work_run_id != result.work_run_id
        or value.source_state is not result.source_state
        or value.state_version != result.state_version
        or value.principal_subject_ref
        != f"private-human-subject:{canonical_hash(result.principal_id)[:24]}"
    ):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    return value


async def _expire_pending_gate_in_session(
    session: AsyncSession,
    row: HumanGateRow,
    projection: HumanGateProjectionRow,
    now: datetime,
) -> bool:
    expires_at = _dt(row.payload.get("expires_at"))
    if projection.status != HumanGateStatus.PENDING.value or expires_at is None or now < expires_at:
        return False
    prior_revision = projection.authority_revision
    event = HumanGateAuthorityEventRow(
        event_id="human-gate-event-"
        + canonical_hash([row.serialized_ref, "EXPIRED", prior_revision]),
        human_gate_id=row.human_gate_id,
        event_kind="EXPIRED",
        prior_revision=prior_revision,
        new_revision=prior_revision + 1,
        payload={
            "reason": HumanAuthorityReason.HUMAN_GATE_EXPIRED.value,
            "bound_state": projection.bound_state,
            "bound_state_version": projection.bound_state_version,
        },
        created_at=now,
    )
    session.add(event)
    await session.flush()
    projection.status = HumanGateStatus.CANCELLED.value
    projection.suspension_status = HumanGateSuspensionStatus.NOT_APPLICABLE.value
    projection.authority_revision = prior_revision + 1
    projection.latest_event_sequence = event.event_sequence
    projection.updated_at = now
    return True


def _validate_result_authority(
    run: WorkRunRow | None,
    gate_row: HumanGateRow | None,
    projection: HumanGateProjectionRow | None,
    principal: AuthenticatedHumanPrincipal,
    action: HumanActionAuthority,
    result_kind: HumanResultKind,
    now: datetime,
) -> None:
    if run is None or gate_row is None or projection is None:
        raise HumanAuthorityError(HumanAuthorityReason.UNKNOWN_HUMAN_GATE)
    if run.workflow_state != WorkflowState.HUMAN_REQUIRED.value:
        raise HumanAuthorityError(HumanAuthorityReason.WORKFLOW_STATE_MISMATCH)
    if (
        run.state_version != action.state_version
        or projection.bound_state_version != run.state_version
    ):
        raise HumanAuthorityError(HumanAuthorityReason.STATE_VERSION_MISMATCH)
    if projection.status != HumanGateStatus.PENDING.value:
        raise HumanAuthorityError(HumanAuthorityReason.HUMAN_GATE_CLOSED)
    if projection.suspension_status != HumanGateSuspensionStatus.ACTIVE.value:
        raise HumanAuthorityError(HumanAuthorityReason.HUMAN_GATE_NOT_CURRENT)
    if (
        principal._issuer_token is not action._issuer_token
        or principal.principal_id != action.principal_id
        or principal.authentication_session_id != action.authentication_session_id
        or action.human_gate_ref != gate_row.serialized_ref
        or action.task_contract_id != gate_row.task_contract_id
        or action.task_contract_version != gate_row.task_contract_version
        or action.work_run_id != gate_row.work_run_id
        or action.gate_authority_revision != projection.authority_revision
        or result_kind not in action.allowed_result_kinds
        or now >= action.expires_at
        or now >= principal.authentication_expires_at
    ):
        raise HumanAuthorityError(HumanAuthorityReason.HUMAN_AUTHORITY_MISMATCH)


def _gate_from_row(row: HumanGateRow, projection: HumanGateProjectionRow) -> HumanGate:
    payload = row.payload
    return HumanGate(
        row.human_gate_id,
        str(payload["human_gate_version"]),
        row.gate_fingerprint,
        str(payload["purpose_id"]),
        str(payload["purpose_version"]),
        row.task_contract_id,
        row.task_contract_version,
        row.work_run_id,
        WorkflowState(row.opened_from_state),
        row.opened_from_state_version,
        WorkflowState(projection.bound_state),
        projection.bound_state_version,
        str(payload["opening_transition_request_id"]),
        str(payload["opening_transition_decision_id"]),
        str(payload["authority_policy_ref"]),
        str(payload["authority_policy_version"]),
        str(payload["designated_principal_selector_fingerprint"]),
        str(payload["gate_authority_id"]),
        str(payload["gate_authority_version"]),
        projection.authority_revision,
        HumanGateStatus(projection.status),
        HumanGateSuspensionStatus(projection.suspension_status),
        row.opened_at.astimezone(UTC),
        _dt(payload.get("expires_at")),
        cast(str | None, payload.get("supersedes_gate_ref")),
    )


def _human_result_proposal_fingerprint(
    *,
    human_result_id: str,
    human_result_version: str,
    gate_ref: str,
    principal: AuthenticatedHumanPrincipal,
    action_authority: HumanActionAuthority,
    result_kind: HumanResultKind,
    structured_reason_code: str,
    reason_vocabulary_version: str,
    idempotency_key: str,
    private_comment_ref: str | None,
    private_comment_hash: str | None,
    sensitivity: EvidenceSensitivity,
    caller_submitted_at: datetime | None,
) -> str:
    return canonical_hash(
        {
            "result": [human_result_id, human_result_version, result_kind.value],
            "gate": [
                gate_ref,
                action_authority.human_gate_ref,
                action_authority.gate_authority_revision,
            ],
            "principal": [
                principal.principal_id,
                principal.principal_authority_id,
                principal.principal_authority_version,
                principal.authentication_session_id,
                principal.authenticated_at.isoformat(),
                principal.authentication_expires_at.isoformat(),
            ],
            "action": [
                action_authority.action_authority_id,
                action_authority.action_authority_version,
                action_authority.task_contract_id,
                action_authority.task_contract_version,
                action_authority.work_run_id,
                action_authority.state_version,
                action_authority.issued_at.isoformat(),
                action_authority.expires_at.isoformat(),
                action_authority.idempotency_scope,
            ],
            "reason": [structured_reason_code, reason_vocabulary_version],
            "private": [private_comment_ref, private_comment_hash, sensitivity.value],
            "caller_submitted_at": (
                caller_submitted_at.isoformat() if caller_submitted_at is not None else None
            ),
            "idempotency": idempotency_key,
        }
    )


def _human_result_fingerprint(value: HumanResult) -> str:
    payload = asdict(value)
    payload.pop("human_result_fingerprint")
    payload["source_state"] = value.source_state.value
    payload["result_kind"] = value.result_kind.value
    payload["sensitivity"] = value.sensitivity.value
    payload["submitted_at"] = value.submitted_at.isoformat()
    payload["admitted_at"] = value.admitted_at.isoformat()
    return canonical_hash(payload)


def _result_row(
    value: HumanResult, human_gate_id: str, proposal_fingerprint: str
) -> HumanResultRow:
    payload = asdict(value)
    payload["source_state"] = value.source_state.value
    payload["result_kind"] = value.result_kind.value
    payload["sensitivity"] = value.sensitivity.value
    payload["submitted_at"] = value.submitted_at.isoformat()
    payload["admitted_at"] = value.admitted_at.isoformat()
    payload["proposal_fingerprint"] = proposal_fingerprint
    return HumanResultRow(
        human_result_id=value.human_result_id,
        serialized_ref=value.serialized_ref,
        human_result_fingerprint=value.human_result_fingerprint,
        human_gate_id=human_gate_id,
        work_run_id=value.work_run_id,
        result_kind=value.result_kind.value,
        authority_revision=value.result_authority_revision,
        payload=payload,
        admitted_at=value.admitted_at,
    )


def _result_from_row(row: HumanResultRow) -> HumanResult:
    p = row.payload
    return HumanResult(
        row.human_result_id,
        str(p["human_result_version"]),
        row.human_result_fingerprint,
        str(p["human_gate_ref"]),
        cast(int, p["gate_authority_revision"]),
        str(p["purpose_id"]),
        str(p["purpose_version"]),
        str(p["principal_id"]),
        str(p["principal_authority_ref"]),
        str(p["human_action_authority_ref"]),
        str(p["task_contract_id"]),
        str(p["task_contract_version"]),
        row.work_run_id,
        WorkflowState(str(p["source_state"])),
        cast(int, p["state_version"]),
        HumanResultKind(row.result_kind),
        str(p["structured_reason_code"]),
        str(p["reason_vocabulary_version"]),
        cast(str | None, p.get("private_comment_ref")),
        cast(str | None, p.get("private_comment_hash")),
        EvidenceSensitivity(str(p["sensitivity"])),
        datetime.fromisoformat(str(p["submitted_at"])),
        row.admitted_at.astimezone(UTC),
        str(p["idempotency_key"]),
        str(p["result_authority_id"]),
        str(p["result_authority_version"]),
        row.authority_revision,
        cast(str | None, p.get("supersedes_human_result_ref")),
    )


def _strict_text(payload: dict[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    return value


def _strict_optional_text(payload: dict[str, object], key: str) -> str | None:
    value = payload.get(key)
    if value is not None and not isinstance(value, str):
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    return value


def _strict_int(payload: dict[str, object], key: str) -> int:
    value = payload.get(key)
    if type(value) is not int:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    return value


def _strict_optional_int(payload: dict[str, object], key: str) -> int | None:
    value = payload.get(key)
    if value is not None and type(value) is not int:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    return value


def _strict_datetime(payload: dict[str, object], key: str) -> datetime:
    raw = _strict_text(payload, key)
    try:
        value = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE) from exc
    if value.tzinfo is None or value.utcoffset() is None:
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    return value.astimezone(UTC)


def _strict_optional_datetime(payload: dict[str, object], key: str) -> datetime | None:
    raw = _strict_optional_text(payload, key)
    if raw is None:
        return None
    try:
        value = datetime.fromisoformat(raw)
    except ValueError as exc:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE) from exc
    if value.tzinfo is None or value.utcoffset() is None:
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    return value.astimezone(UTC)


def _strict_text_tuple(payload: dict[str, object], key: str) -> tuple[str, ...]:
    raw = payload.get(key)
    if not isinstance(raw, list) or any(not isinstance(item, str) for item in raw):
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    return tuple(raw)


def _human_required_binding_from_payload(
    payload: dict[str, object],
) -> HumanRequiredEvidenceBinding:
    exact_keys = {
        "attestation_ref",
        "attestation_version",
        "checkpoint_ref",
        "checkpoint_fingerprint",
        "task_contract_id",
        "task_contract_version",
        "work_run_id",
        "source_state",
        "state_version",
        "target_state",
        "transition_purpose_id",
        "transition_purpose_version",
        "requirement_set_id",
        "requirement_set_version",
        "requirement_set_root",
        "ordered_applicable_requirement_refs",
        "applicable_subset_root",
        "ordered_admitted_evidence_refs",
        "admitted_ref_root",
        "evidence_authority_version",
        "evidence_authority_revision",
        "issued_at",
        "expires_at",
        "p1_6_authority_id",
        "p1_6_authority_version",
    }
    if set(payload) != exact_keys:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    target_raw = _strict_optional_text(payload, "target_state")
    try:
        source_state = WorkflowState(_strict_text(payload, "source_state"))
        target_state = WorkflowState(target_raw) if target_raw is not None else None
    except ValueError as exc:
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT) from exc
    return HumanRequiredEvidenceBinding(
        _strict_text(payload, "attestation_ref"),
        _strict_text(payload, "attestation_version"),
        _strict_text(payload, "checkpoint_ref"),
        _strict_text(payload, "checkpoint_fingerprint"),
        _strict_text(payload, "task_contract_id"),
        _strict_text(payload, "task_contract_version"),
        _strict_text(payload, "work_run_id"),
        source_state,
        _strict_int(payload, "state_version"),
        target_state,
        _strict_optional_text(payload, "transition_purpose_id"),
        _strict_optional_text(payload, "transition_purpose_version"),
        _strict_text(payload, "requirement_set_id"),
        _strict_text(payload, "requirement_set_version"),
        _strict_text(payload, "requirement_set_root"),
        _strict_text_tuple(payload, "ordered_applicable_requirement_refs"),
        _strict_text(payload, "applicable_subset_root"),
        _strict_text_tuple(payload, "ordered_admitted_evidence_refs"),
        _strict_text(payload, "admitted_ref_root"),
        _strict_text(payload, "evidence_authority_version"),
        _strict_int(payload, "evidence_authority_revision"),
        _strict_datetime(payload, "issued_at"),
        _strict_optional_datetime(payload, "expires_at"),
        _strict_text(payload, "p1_6_authority_id"),
        _strict_text(payload, "p1_6_authority_version"),
    )


def _human_guard_attestation_from_row(
    row: HumanGuardAttestationRow,
) -> HumanGuardAttestation:
    payload = row.payload
    exact_keys = {
        "attestation_id",
        "attestation_version",
        "fingerprint",
        "guard_id",
        "task_contract_id",
        "task_contract_version",
        "work_run_id",
        "source_state",
        "state_version",
        "target_state",
        "target_use_fingerprint",
        "human_gate_ref",
        "gate_authority_revision",
        "purpose_id",
        "purpose_version",
        "human_result_ref",
        "result_authority_revision",
        "authority_id",
        "authority_version",
        "authority_revision",
        "issued_at",
        "expires_at",
        "pre_human_evidence",
    }
    if not isinstance(payload, dict) or set(payload) != exact_keys:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    raw_binding = payload.get("pre_human_evidence")
    if not isinstance(raw_binding, dict):
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    try:
        guard_id = GuardId(_strict_text(payload, "guard_id"))
        source_state = WorkflowState(_strict_text(payload, "source_state"))
        target_state = WorkflowState(_strict_text(payload, "target_state"))
    except ValueError as exc:
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT) from exc
    return HumanGuardAttestation(
        _strict_text(payload, "attestation_id"),
        _strict_text(payload, "attestation_version"),
        _strict_text(payload, "fingerprint"),
        guard_id,
        _strict_text(payload, "task_contract_id"),
        _strict_text(payload, "task_contract_version"),
        _strict_text(payload, "work_run_id"),
        source_state,
        _strict_int(payload, "state_version"),
        target_state,
        _strict_text(payload, "target_use_fingerprint"),
        _strict_text(payload, "human_gate_ref"),
        _strict_int(payload, "gate_authority_revision"),
        _strict_text(payload, "purpose_id"),
        _strict_text(payload, "purpose_version"),
        _strict_optional_text(payload, "human_result_ref"),
        _strict_optional_int(payload, "result_authority_revision"),
        _strict_text(payload, "authority_id"),
        _strict_text(payload, "authority_version"),
        _strict_int(payload, "authority_revision"),
        _strict_datetime(payload, "issued_at"),
        _strict_optional_datetime(payload, "expires_at"),
        _human_required_binding_from_payload(raw_binding),
    )


async def _verify_human_guard_attestation_historical_provenance_in_session(
    session: AsyncSession,
    *,
    serialized_ref: str,
    request: TransitionRequest,
    gate_row: HumanGateRow,
    opening_revision: int,
) -> HumanGuardAttestation:
    rows = tuple(
        await session.scalars(
            select(HumanGuardAttestationRow).where(
                HumanGuardAttestationRow.serialized_ref == serialized_ref
            )
        )
    )
    if not rows:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    if len(rows) != 1:
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    row = rows[0]
    value = _human_guard_attestation_from_row(row)
    expected_target_use = canonical_hash(
        [
            request.task_contract_id,
            request.task_contract_version,
            request.work_run_id,
            request.observed_state.value if request.observed_state else None,
            request.observed_state_version,
            request.target_state.value,
        ]
    )
    if (
        row.attestation_id != value.attestation_id
        or row.serialized_ref != value.serialized_ref
        or row.fingerprint != value.fingerprint
        or row.guard_id != value.guard_id.value
        or row.work_run_id != value.work_run_id
        or row.state_version != value.state_version
        or row.authority_revision != value.authority_revision
        or row.issued_at.astimezone(UTC) != value.issued_at
        or (row.expires_at.astimezone(UTC) if row.expires_at else None) != value.expires_at
        or row.payload != human_guard_attestation_payload(value)
        or value.fingerprint != human_guard_attestation_fingerprint(value)
        or value.attestation_version != HUMAN_GUARD_ATTESTATION_VERSION
        or value.guard_id is not GuardId.G_HUMAN_REQUIRED
        or value.task_contract_id != request.task_contract_id
        or value.task_contract_version != request.task_contract_version
        or value.work_run_id != request.work_run_id
        or value.source_state is not request.observed_state
        or value.state_version != request.observed_state_version
        or value.target_state is not WorkflowState.HUMAN_REQUIRED
        or value.target_state is not request.target_state
        or value.target_use_fingerprint != expected_target_use
        or value.human_gate_ref != gate_row.serialized_ref
        or value.gate_authority_revision != opening_revision
        or value.purpose_id != HUMAN_GATE_PURPOSE_ID
        or value.purpose_version != HUMAN_GATE_PURPOSE_VERSION
        or value.human_result_ref is not None
        or value.result_authority_revision is not None
        or value.authority_id != HUMAN_GUARD_AUTHORITY_ID
        or value.authority_version != HUMAN_AUTHORITY_VERSION
        or value.authority_revision != opening_revision
        or gate_row.payload.get("gate_authority_id") != value.authority_id
        or gate_row.payload.get("gate_authority_version") != value.authority_version
        or gate_row.payload.get("purpose_id") != value.purpose_id
        or gate_row.payload.get("purpose_version") != value.purpose_version
        or _dt(gate_row.payload.get("expires_at")) != value.expires_at
    ):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)

    binding = value.pre_human_evidence
    assert binding is not None
    try:
        evidence = await verify_historical_set_attestation_provenance(
            session, binding.attestation_ref
        )
    except HistoricalEvidenceProvenanceError as exc:
        reason = (
            HumanAuthorityReason.PROVENANCE_INCOMPLETE
            if exc.incomplete
            else HumanAuthorityReason.AUTHORITY_CONFLICT
        )
        raise HumanAuthorityError(reason) from exc
    if (
        binding.attestation_ref != evidence.serialized_ref
        or binding.attestation_version != evidence.attestation_version
        or binding.checkpoint_ref != evidence.checkpoint_ref.serialized()
        or binding.checkpoint_fingerprint != evidence.checkpoint_fingerprint
        or binding.task_contract_id != evidence.task_contract_id
        or binding.task_contract_version != evidence.task_contract_version
        or binding.work_run_id != evidence.work_run_id
        or binding.source_state is not evidence.source_state
        or binding.state_version != evidence.state_version
        or binding.target_state is not evidence.target_state
        or binding.transition_purpose_id != evidence.transition_purpose_id
        or binding.transition_purpose_version != evidence.transition_purpose_version
        or binding.requirement_set_id != evidence.requirement_set_id
        or binding.requirement_set_version != evidence.requirement_set_version
        or binding.requirement_set_root != evidence.full_requirement_root_hash
        or binding.ordered_applicable_requirement_refs
        != evidence.ordered_applicable_requirement_refs
        or binding.applicable_subset_root != evidence.checkpoint_subset_root_hash
        or binding.ordered_admitted_evidence_refs != evidence.ordered_admitted_evidence_refs
        or binding.admitted_ref_root != evidence.admitted_ref_root_hash
        or not evidence.satisfied
        or binding.evidence_authority_version != evidence.evidence_authority_version
        or binding.evidence_authority_revision != evidence.evidence_authority_revision
        or binding.issued_at != evidence.issued_at
        or binding.expires_at != evidence.expires_at
        or binding.p1_6_authority_id != evidence.issuer_id
        or binding.p1_6_authority_version != evidence.issuer_version
    ):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    return value


async def _verify_human_result_historical_provenance_in_session(
    session: AsyncSession,
    row: HumanResultRow,
) -> HumanResult:
    """Verify immutable HumanResult issuance without consulting a current projection."""
    try:
        value = _result_from_row(row)
    except (KeyError, TypeError, ValueError) as exc:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE) from exc
    proposal_fingerprint = row.payload.get("proposal_fingerprint")
    if proposal_fingerprint is None:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    if not _is_lower_sha256(proposal_fingerprint):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    if (
        row.human_result_id != value.human_result_id
        or row.serialized_ref != value.serialized_ref
        or row.human_result_fingerprint != value.human_result_fingerprint
        or row.work_run_id != value.work_run_id
        or row.result_kind != value.result_kind.value
        or row.authority_revision != value.result_authority_revision
        or row.admitted_at.astimezone(UTC) != value.admitted_at
        or value.result_authority_revision != 1
        or value.human_result_fingerprint != _human_result_fingerprint(value)
    ):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    gate = await session.get(HumanGateRow, row.human_gate_id)
    if gate is None:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    gate_events = await _verify_human_gate_historical_provenance_in_session(session, gate)
    if (
        value.human_gate_ref != gate.serialized_ref
        or value.task_contract_id != gate.task_contract_id
        or value.task_contract_version != gate.task_contract_version
        or value.work_run_id != gate.work_run_id
        or value.purpose_id != gate.payload.get("purpose_id")
        or value.purpose_version != gate.payload.get("purpose_version")
        or value.source_state is not WorkflowState.HUMAN_REQUIRED
        or gate.bound_state_version != value.state_version
    ):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    result_events = tuple(
        await session.scalars(
            select(HumanResultAuthorityEventRow).where(
                HumanResultAuthorityEventRow.human_result_id == row.human_result_id
            )
        )
    )
    if not result_events:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    if len(result_events) != 1:
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    admitted = result_events[0]
    if (
        admitted.event_kind != "ADMITTED"
        or admitted.prior_revision != 0
        or admitted.new_revision != value.result_authority_revision
        or admitted.payload.get("winner_rule") != "FIRST_DURABLY_ADMITTED"
        or admitted.payload.get("gate_ref") != value.human_gate_ref
        or admitted.created_at.astimezone(UTC) != value.admitted_at
    ):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    matching_resolutions = tuple(
        event
        for event in gate_events
        if event.event_kind == "RESOLVED"
        if event.payload.get("human_result_ref") == value.serialized_ref
    )
    if not matching_resolutions:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    if len(matching_resolutions) != 1:
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    resolved = matching_resolutions[0]
    if (
        resolved.prior_revision != value.gate_authority_revision
        or resolved.new_revision != value.gate_authority_revision + 1
        or resolved.payload.get("bound_state") != value.source_state.value
        or resolved.payload.get("bound_state_version") != value.state_version
        or resolved.created_at.astimezone(UTC) != value.admitted_at
    ):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    resolved_index = gate_events.index(resolved)
    if resolved_index == 0 or gate_events[resolved_index - 1].new_revision != (
        value.gate_authority_revision
    ):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    return value


async def _verify_human_gate_historical_provenance_in_session(
    session: AsyncSession,
    row: HumanGateRow,
) -> tuple[HumanGateAuthorityEventRow, ...]:
    """Verify immutable gate issuance and its complete correction ancestry."""
    verified: dict[str, tuple[HumanGateAuthorityEventRow, ...]] = {}
    visiting: set[str] = set()

    async def verify_node(
        current: HumanGateRow,
    ) -> tuple[HumanGateAuthorityEventRow, ...]:
        if current.serialized_ref in visiting:
            raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
        cached = verified.get(current.serialized_ref)
        if cached is not None:
            return cached
        visiting.add(current.serialized_ref)
        try:
            events = await _verify_human_gate_base_issuance_in_session(session, current)
            supersedes_ref = current.payload.get("supersedes_gate_ref")
            if supersedes_ref is not None:
                predecessor = await session.scalar(
                    select(HumanGateRow).where(HumanGateRow.serialized_ref == supersedes_ref)
                )
                if predecessor is None:
                    raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
                predecessor_events = await verify_node(predecessor)
                relations = tuple(
                    event
                    for event in predecessor_events
                    if event.event_kind == "SUPERSEDED"
                    and event.payload.get("replacement_gate_ref") == current.serialized_ref
                )
                if not relations:
                    raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
                if len(relations) != 1:
                    raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
                relation = relations[0]
                if (
                    predecessor.task_contract_id != current.task_contract_id
                    or predecessor.task_contract_version != current.task_contract_version
                    or predecessor.work_run_id != current.work_run_id
                    or predecessor.bound_state_version != current.bound_state_version
                    or predecessor.payload.get("purpose_id") != current.payload.get("purpose_id")
                    or predecessor.payload.get("purpose_version")
                    != current.payload.get("purpose_version")
                    or predecessor.payload.get("expires_at") != current.payload.get("expires_at")
                    or current.human_gate_id
                    != "human-gate-"
                    + canonical_hash(
                        [predecessor.serialized_ref, relation.prior_revision, "CORRECTION"]
                    )
                    or relation.new_revision != relation.prior_revision + 1
                    or relation.created_at.astimezone(UTC) != current.opened_at.astimezone(UTC)
                ):
                    raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
            verified[current.serialized_ref] = events
            return events
        finally:
            visiting.remove(current.serialized_ref)

    return await verify_node(row)


async def _verify_human_gate_base_issuance_in_session(
    session: AsyncSession,
    row: HumanGateRow,
) -> tuple[HumanGateAuthorityEventRow, ...]:
    try:
        version = str(row.payload["human_gate_version"])
        purpose_id = str(row.payload["purpose_id"])
        purpose_version = str(row.payload["purpose_version"])
        opening_request_id = str(row.payload["opening_transition_request_id"])
        opening_decision_id = str(row.payload["opening_transition_decision_id"])
        policy_ref = str(row.payload["authority_policy_ref"])
        policy_version = str(row.payload["authority_policy_version"])
        selector = str(row.payload["designated_principal_selector_fingerprint"])
        authority_id = str(row.payload["gate_authority_id"])
        authority_version = str(row.payload["gate_authority_version"])
        expires_raw = row.payload.get("expires_at")
        expires_at = _dt(expires_raw)
        supersedes_ref = cast(str | None, row.payload.get("supersedes_gate_ref"))
        opened_from = WorkflowState(row.opened_from_state)
        opened_at = row.opened_at.astimezone(UTC)
    except (KeyError, TypeError, ValueError) as exc:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE) from exc
    if (
        not version
        or not purpose_id
        or not purpose_version
        or not policy_ref
        or not policy_version
        or not selector
        or not authority_id
        or not authority_version
        or row.serialized_ref != f"p1-7-gate:{version}:{row.human_gate_id}"
        or row.opened_from_state != opened_from.value
        or row.opened_from_state_version < 1
        or row.bound_state_version < 1
        or (expires_raw is not None and expires_at is None)
    ):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)

    events = tuple(
        await session.scalars(
            select(HumanGateAuthorityEventRow)
            .where(HumanGateAuthorityEventRow.human_gate_id == row.human_gate_id)
            .order_by(HumanGateAuthorityEventRow.event_sequence)
        )
    )
    if not events:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    initial_events = tuple(
        event for event in events if event.event_kind in {"OPENED", "OPENED_CORRECTION"}
    )
    if not initial_events:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    if len(initial_events) != 1:
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    initial = initial_events[0]
    if (
        events[0] is not initial
        or initial.prior_revision != 0
        or initial.new_revision != 1
        or initial.created_at.astimezone(UTC) != opened_at
        or initial.payload.get("bound_state") != WorkflowState.HUMAN_REQUIRED.value
        or initial.payload.get("bound_state_version") != row.bound_state_version
    ):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    previous_revision = 0
    for event in events:
        if (
            event.event_kind
            not in {
                "OPENED",
                "OPENED_CORRECTION",
                "RESOLVED",
                "SUSPENDED",
                "REACTIVATED",
                "CANCELLED",
                "SUPERSEDED",
                "EXPIRED",
            }
            or event.prior_revision != previous_revision
            or event.new_revision != previous_revision + 1
        ):
            raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
        previous_revision = event.new_revision

    if supersedes_ref is None:
        if initial.event_kind != "OPENED":
            raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
        await _verify_normal_gate_transition_provenance(
            session,
            row,
            initial,
            opening_request_id,
            opening_decision_id,
        )
        expected_fingerprint = canonical_hash(
            {
                "gate": [row.human_gate_id, version],
                "purpose": [purpose_id, purpose_version],
                "task": [row.task_contract_id, row.task_contract_version],
                "run": row.work_run_id,
                "source": [opened_from.value, row.opened_from_state_version],
                "target": WorkflowState.HUMAN_REQUIRED.value,
                "policy": [policy_ref, policy_version],
                "selector": selector,
                "expires_at": expires_raw,
            }
        )
    else:
        if (
            not isinstance(supersedes_ref, str)
            or not supersedes_ref
            or initial.event_kind != "OPENED_CORRECTION"
            or opened_from is not WorkflowState.HUMAN_REQUIRED
            or row.opened_from_state_version != row.bound_state_version
            or opening_request_id != "P1_7_AUTHORITY_CORRECTION"
            or opening_decision_id != "P1_7_AUTHORITY_CORRECTION"
            or initial.payload.get("supersedes_gate_ref") != supersedes_ref
        ):
            raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
        expected_fingerprint = canonical_hash(
            {
                "gate": [row.human_gate_id, version],
                "purpose": [purpose_id, purpose_version],
                "task": [row.task_contract_id, row.task_contract_version],
                "run": row.work_run_id,
                "source": [WorkflowState.HUMAN_REQUIRED.value, row.bound_state_version],
                "target": WorkflowState.HUMAN_REQUIRED.value,
                "policy": [policy_ref, policy_version],
                "selector": selector,
                "supersedes": supersedes_ref,
            }
        )
    if row.gate_fingerprint != expected_fingerprint:
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    return events


async def _verify_normal_gate_transition_provenance(
    session: AsyncSession,
    row: HumanGateRow,
    initial: HumanGateAuthorityEventRow,
    request_id: str,
    decision_id: str,
) -> None:
    try:
        verified = await verify_historical_transition_provenance(session, request_id)
    except HistoricalTransitionProvenanceError as exc:
        reason = (
            HumanAuthorityReason.PROVENANCE_INCOMPLETE
            if exc.incomplete
            else HumanAuthorityReason.AUTHORITY_CONFLICT
        )
        raise HumanAuthorityError(reason) from exc
    request = verified.request
    evaluation = verified.evaluation
    decision = verified.decision
    human_required_guards = tuple(
        guard for guard in evaluation.guards if guard.guard_id is GuardId.G_HUMAN_REQUIRED
    )
    if not human_required_guards:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    if len(human_required_guards) != 1:
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    human_required_guard = human_required_guards[0]
    if (
        human_required_guard.semantic_owner is not GuardSemanticOwner.P1_7_HUMAN
        or not human_required_guard.satisfied
        or human_required_guard.reason != "P1_7_HUMAN_AUTHORITY_CURRENT"
        or not human_required_guard.authority_ref
        or human_required_guard.bound_refs != required_bound_refs(GuardId.G_HUMAN_REQUIRED, request)
    ):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    await _verify_human_guard_attestation_historical_provenance_in_session(
        session,
        serialized_ref=human_required_guard.authority_ref,
        request=request,
        gate_row=row,
        opening_revision=initial.new_revision,
    )
    if (
        initial.payload.get("transition_request_id") != request_id
        or initial.payload.get("transition_decision_id") != decision_id
        or request.transition_request_id != request_id
        or row.human_gate_id
        != "human-gate-"
        + canonical_hash([row.work_run_id, row.opened_from_state_version, request_id])
        or request.task_contract_id != row.task_contract_id
        or request.task_contract_version != row.task_contract_version
        or request.work_run_id != row.work_run_id
        or request.observed_state is not WorkflowState(row.opened_from_state)
        or request.observed_state_version != row.opened_from_state_version
        or request.target_state is not WorkflowState.HUMAN_REQUIRED
        or decision.transition_decision_id != decision_id
        or decision.resulting_state is not WorkflowState.HUMAN_REQUIRED
        or decision.resulting_state_version != row.bound_state_version
        or row.bound_state_version != row.opened_from_state_version + 1
        or decision.decided_at.astimezone(UTC) != row.opened_at.astimezone(UTC)
    ):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)


def _is_lower_sha256(value: object) -> bool:
    return bool(
        isinstance(value, str)
        and len(value) == 64
        and value == value.lower()
        and all(character in "0123456789abcdef" for character in value)
    )


def _producer_fingerprint(value: HumanP1_7EvidenceProducerRef) -> str:
    return canonical_hash(
        {
            "producer": [value.producer_ref_id, value.producer_ref_version],
            "task": [value.task_contract_id, value.task_contract_version, value.work_run_id],
            "state": [value.source_state.value, value.state_version],
            "human": [
                value.human_gate_ref,
                value.gate_authority_revision,
                value.human_result_ref,
                value.result_authority_revision,
            ],
            "checkpoint": value.checkpoint_ref,
            "type": [value.evidence_type_id, value.evidence_type_version],
            "scope": [value.subject_id, value.scope_id, value.resource_id],
            "content": [value.content_hash, value.sensitivity.value, value.export_policy],
            "authority": [value.authority_id, value.authority_version],
            "issued_at": value.issued_at.isoformat(),
        }
    )


def _producer_row(value: HumanP1_7EvidenceProducerRef) -> HumanP1_7EvidenceProducerRow:
    payload = asdict(value)
    payload["source_state"] = value.source_state.value
    payload["sensitivity"] = value.sensitivity.value
    payload["issued_at"] = value.issued_at.isoformat()
    payload["expires_at"] = value.expires_at.isoformat() if value.expires_at else None
    return HumanP1_7EvidenceProducerRow(
        producer_ref_id=value.producer_ref_id,
        serialized_ref=value.serialized_ref,
        fingerprint=value.fingerprint,
        human_result_ref=value.human_result_ref,
        work_run_id=value.work_run_id,
        payload=payload,
        issued_at=value.issued_at,
    )


def _producer_from_row(row: HumanP1_7EvidenceProducerRow) -> HumanP1_7EvidenceProducerRef:
    p = row.payload
    return HumanP1_7EvidenceProducerRef(
        row.producer_ref_id,
        str(p["producer_ref_version"]),
        row.fingerprint,
        str(p["task_contract_id"]),
        str(p["task_contract_version"]),
        row.work_run_id,
        WorkflowState(str(p["source_state"])),
        cast(int, p["state_version"]),
        str(p["human_gate_ref"]),
        cast(int, p["gate_authority_revision"]),
        row.human_result_ref,
        cast(int, p["result_authority_revision"]),
        str(p["principal_subject_ref"]),
        str(p["checkpoint_ref"]),
        str(p["evidence_type_id"]),
        str(p["evidence_type_version"]),
        str(p["subject_id"]),
        str(p["scope_id"]),
        cast(str | None, p.get("resource_id")),
        str(p["content_hash"]),
        EvidenceSensitivity(str(p["sensitivity"])),
        str(p["export_policy"]),
        str(p["authority_id"]),
        str(p["authority_version"]),
        row.issued_at.astimezone(UTC),
        _dt(p.get("expires_at")),
    )


def _dt(value: object) -> datetime | None:
    return datetime.fromisoformat(value) if isinstance(value, str) else None


async def _verify_gate_consistency_in_session(
    session: AsyncSession,
    row: HumanGateRow,
    projection: HumanGateProjectionRow,
) -> None:
    events = tuple(
        await session.scalars(
            select(HumanGateAuthorityEventRow)
            .where(HumanGateAuthorityEventRow.human_gate_id == row.human_gate_id)
            .order_by(HumanGateAuthorityEventRow.event_sequence)
        )
    )
    if not events:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    revision = 0
    status: HumanGateStatus | None = None
    suspension: HumanGateSuspensionStatus | None = None
    bound_state: str | None = None
    bound_version: int | None = None
    latest_sequence = 0
    for event in events:
        if event.prior_revision != revision or event.new_revision != revision + 1:
            raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
        revision = event.new_revision
        latest_sequence = event.event_sequence
        payload_state = event.payload.get("bound_state")
        payload_version = event.payload.get("bound_state_version")
        if isinstance(payload_state, str):
            bound_state = payload_state
        if isinstance(payload_version, int):
            bound_version = payload_version
        if event.event_kind in {"OPENED", "OPENED_CORRECTION"}:
            status = HumanGateStatus.PENDING
            suspension = HumanGateSuspensionStatus.ACTIVE
        elif event.event_kind == "RESOLVED":
            status = HumanGateStatus.RESOLVED
            suspension = HumanGateSuspensionStatus.NOT_APPLICABLE
        elif event.event_kind == "SUSPENDED":
            status = HumanGateStatus.PENDING
            suspension = HumanGateSuspensionStatus.SUSPENDED
        elif event.event_kind == "REACTIVATED":
            status = HumanGateStatus.PENDING
            suspension = HumanGateSuspensionStatus.ACTIVE
        elif event.event_kind in {"CANCELLED", "SUPERSEDED", "EXPIRED"}:
            status = HumanGateStatus.CANCELLED
            suspension = HumanGateSuspensionStatus.NOT_APPLICABLE
        else:
            raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    if (
        status is None
        or suspension is None
        or bound_state is None
        or bound_version is None
        or projection.authority_revision != revision
        or projection.latest_event_sequence != latest_sequence
        or projection.status != status.value
        or projection.suspension_status != suspension.value
        or projection.bound_state != bound_state
        or projection.bound_state_version != bound_version
    ):
        raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
    if projection.current_result_ref is not None:
        result = await session.scalar(
            select(HumanResultRow).where(
                HumanResultRow.serialized_ref == projection.current_result_ref
            )
        )
        if result is None or result.human_gate_id != row.human_gate_id:
            raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
        await _verify_human_result_historical_provenance_in_session(session, result)
