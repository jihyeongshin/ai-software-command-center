from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.contracts.workflow import WorkflowState
from aiscc.evidence.attestation import EvidenceCheckpointUseRegistry
from aiscc.evidence.models import (
    EvidenceAuthorityConflictError,
    EvidenceSetSatisfactionAttestation,
    canonical_hash,
)
from aiscc.evidence.repository import PostgresEvidenceRepository
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
    HumanRequiredEvidenceBinding,
    HumanResultKind,
    human_guard_attestation_fingerprint,
    human_guard_attestation_payload,
)
from aiscc.human.repository import (
    PostgresHumanAuthorityRepository,
    _dt,
    _expire_pending_gate_in_session,
    _result_from_row,
    _verify_gate_consistency_in_session,
)
from aiscc.persistence.models import (
    HumanGateAuthorityEventRow,
    HumanGateProjectionRow,
    HumanGateRow,
    HumanGuardAttestationRow,
    HumanResultRow,
    WorkRunRow,
)
from aiscc.workflow.guards import TrustedGuardFact
from aiscc.workflow.models import (
    DecisionOutcome,
    GuardId,
    GuardSemanticOwner,
    TransitionDecision,
    TransitionEvaluation,
    TransitionRequest,
    WorkRun,
)


class HumanPrincipalAuthority:
    def __init__(
        self,
        repository: PostgresHumanAuthorityRepository | None = None,
        *,
        allowed_roles_by_selector: Mapping[str, frozenset[str]] | None = None,
        clock: Callable[[], datetime] | None = None,
        authority_id: str = "AISCC_P1_7_HUMAN_PRINCIPAL_AUTHORITY_V1",
        authority_version: str = "p1-7-human-principal-v1",
    ) -> None:
        self._repository = repository
        self._allowed_roles_by_selector = allowed_roles_by_selector or {
            "reviewers-v1": frozenset({"reviewer"}),
            "reviewers-v2": frozenset({"reviewer"}),
        }
        self._clock = clock or (lambda: datetime.now(UTC))
        self.authority_id = authority_id
        self.authority_version = authority_version
        self._token = object()

    def authenticate(
        self,
        *,
        principal_id: str,
        session_id: str,
        role_refs: tuple[str, ...],
        ttl_seconds: int = 300,
    ) -> AuthenticatedHumanPrincipal:
        issued = self._clock().astimezone(UTC)
        if not principal_id or not session_id or ttl_seconds <= 0:
            raise ValueError("authenticated Human principal binding is incomplete")
        return AuthenticatedHumanPrincipal(
            principal_id,
            self.authority_id,
            self.authority_version,
            session_id,
            issued,
            issued + timedelta(seconds=ttl_seconds),
            "AISCC_HUMAN_AUTHENTICATION_POLICY_V1",
            role_refs,
            self._token,
        )

    async def issue_action_authority(
        self,
        principal: AuthenticatedHumanPrincipal,
        gate_ref: str,
        *,
        ttl_seconds: int = 120,
        idempotency_scope: str,
    ) -> HumanActionAuthority:
        if self._repository is None or not isinstance(gate_ref, str):
            raise HumanAuthorityError(HumanAuthorityReason.UNKNOWN_HUMAN_GATE)
        if principal._issuer_token is not self._token:
            raise HumanAuthorityError(HumanAuthorityReason.HUMAN_PRINCIPAL_NOT_AUTHORIZED)
        return await self._repository.issue_current_gate_action_authority(
            gate_ref=gate_ref,
            principal=principal,
            issuer_token=self._token,
            allowed_roles_by_selector=self._allowed_roles_by_selector,
            authority_version="p1-7-human-action-v1",
            idempotency_scope=idempotency_scope,
            ttl_seconds=ttl_seconds,
        )


class HumanGateReservationAuthority:
    def __init__(
        self,
        required_uses: frozenset[tuple[str, str, WorkflowState, WorkflowState]],
        *,
        authority_policy_ref: str = "AISCC_HUMAN_GATE_POLICY_V1",
        authority_policy_version: str = "v1",
    ) -> None:
        self._required_uses = required_uses
        self.authority_policy_ref = authority_policy_ref
        self.authority_policy_version = authority_policy_version
        self._token = object()

    def reserve(
        self,
        request: TransitionRequest,
        *,
        designated_principal_selector_fingerprint: str,
        expires_at: datetime | None = None,
    ) -> HumanGateReservation:
        key = (
            request.task_contract_id,
            request.task_contract_version,
            cast(WorkflowState, request.observed_state),
            request.target_state,
        )
        if request.observed_state is None or key not in self._required_uses:
            raise HumanAuthorityError(HumanAuthorityReason.TRANSITION_PURPOSE_MISMATCH)
        gate_id = "human-gate-" + canonical_hash(
            [request.work_run_id, request.observed_state_version, request.transition_request_id]
        )
        fingerprint = canonical_hash(
            {
                "gate": [gate_id, "p1-7-gate-v1"],
                "purpose": [HUMAN_GATE_PURPOSE_ID, HUMAN_GATE_PURPOSE_VERSION],
                "task": [request.task_contract_id, request.task_contract_version],
                "run": request.work_run_id,
                "source": [request.observed_state.value, request.observed_state_version],
                "target": request.target_state.value,
                "policy": [self.authority_policy_ref, self.authority_policy_version],
                "selector": designated_principal_selector_fingerprint,
                "expires_at": expires_at.isoformat() if expires_at else None,
            }
        )
        return HumanGateReservation(
            gate_id,
            "p1-7-gate-v1",
            fingerprint,
            HUMAN_GATE_PURPOSE_ID,
            HUMAN_GATE_PURPOSE_VERSION,
            request.task_contract_id,
            request.task_contract_version,
            request.work_run_id,
            request.observed_state,
            request.observed_state_version,
            request.target_state,
            self.authority_policy_ref,
            self.authority_policy_version,
            designated_principal_selector_fingerprint,
            expires_at,
            self._token,
        )

    def recognizes(self, reservation: HumanGateReservation) -> bool:
        return bool(
            reservation._issuer_token is self._token
            and reservation.authority_policy_ref == self.authority_policy_ref
            and reservation.authority_policy_version == self.authority_policy_version
            and reservation.purpose_id == HUMAN_GATE_PURPOSE_ID
            and reservation.purpose_version == HUMAN_GATE_PURPOSE_VERSION
            and reservation.gate_fingerprint == _reservation_fingerprint(reservation)
        )

    def matches_request(
        self, reservation: HumanGateReservation, request: TransitionRequest
    ) -> bool:
        return bool(
            self.recognizes(reservation)
            and request.observed_state is not None
            and reservation.task_contract_id == request.task_contract_id
            and reservation.task_contract_version == request.task_contract_version
            and reservation.work_run_id == request.work_run_id
            and reservation.opened_from_state is request.observed_state
            and reservation.opened_from_state_version == request.observed_state_version
            and reservation.target_state is request.target_state
            and self.requires_human(request)
        )

    def requires_human(self, request: TransitionRequest) -> bool:
        if request.observed_state is None:
            return False
        return (
            request.task_contract_id,
            request.task_contract_version,
            request.observed_state,
            request.target_state,
        ) in self._required_uses

    def reserve_correction(
        self,
        gate: HumanGate,
        *,
        designated_principal_selector_fingerprint: str,
    ) -> HumanGateReservation:
        gate_id = "human-gate-" + canonical_hash(
            [gate.serialized_ref, gate.gate_authority_revision, "CORRECTION"]
        )
        fingerprint = canonical_hash(
            {
                "gate": [gate_id, "p1-7-gate-v1"],
                "purpose": [gate.purpose_id, gate.purpose_version],
                "task": [gate.task_contract_id, gate.task_contract_version],
                "run": gate.work_run_id,
                "source": [WorkflowState.HUMAN_REQUIRED.value, gate.bound_state_version],
                "target": WorkflowState.HUMAN_REQUIRED.value,
                "policy": [self.authority_policy_ref, self.authority_policy_version],
                "selector": designated_principal_selector_fingerprint,
                "supersedes": gate.serialized_ref,
            }
        )
        return HumanGateReservation(
            gate_id,
            "p1-7-gate-v1",
            fingerprint,
            gate.purpose_id,
            gate.purpose_version,
            gate.task_contract_id,
            gate.task_contract_version,
            gate.work_run_id,
            WorkflowState.HUMAN_REQUIRED,
            gate.bound_state_version,
            WorkflowState.HUMAN_REQUIRED,
            self.authority_policy_ref,
            self.authority_policy_version,
            designated_principal_selector_fingerprint,
            gate.expires_at,
            self._token,
        )


class HumanGuardAuthority:
    semantic_owner = GuardSemanticOwner.P1_7_HUMAN

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        human_repository: PostgresHumanAuthorityRepository,
        evidence_repository: PostgresEvidenceRepository,
        checkpoint_uses: EvidenceCheckpointUseRegistry,
        reservation_authority: HumanGateReservationAuthority,
        *,
        clock: Callable[[], datetime] | None = None,
        authority_id: str = HUMAN_GUARD_AUTHORITY_ID,
        authority_version: str = HUMAN_AUTHORITY_VERSION,
    ) -> None:
        self._session_factory = session_factory
        self._human_repository = human_repository
        self._evidence_repository = evidence_repository
        self._checkpoint_uses = checkpoint_uses
        self._reservation_authority = reservation_authority
        self._clock = clock or (lambda: datetime.now(UTC))
        self.authority_id = authority_id
        self.authority_version = authority_version
        self._token = object()
        self._active: dict[str, set[str]] = {}

    async def gate_open_participant(
        self,
        request: TransitionRequest,
        reservation: HumanGateReservation,
        pre_human_attestation_ref: str,
    ) -> HumanTransitionParticipant:
        if not self._reservation_authority.recognizes(reservation):
            raise HumanAuthorityError(HumanAuthorityReason.HUMAN_AUTHORITY_MISMATCH)
        if not self._reservation_authority.matches_request(reservation, request):
            return HumanTransitionParticipant(self, request, reservation=reservation)
        proposed = await self._evidence_repository.load_effective_attestation(
            pre_human_attestation_ref
        )
        attestation = (
            self._human_required_attestation(request, reservation, proposed)
            if proposed is not None
            else None
        )
        return HumanTransitionParticipant(
            self,
            request,
            reservation=reservation,
            attestation=attestation,
            proposed_evidence=proposed,
        )

    async def result_guard_participant(
        self, request: TransitionRequest, guard_id: GuardId
    ) -> HumanTransitionParticipant:
        expected = {
            GuardId.G_HUMAN_APPROVED: HumanResultKind.APPROVE,
            GuardId.G_HUMAN_REWORK: HumanResultKind.REWORK,
            GuardId.G_HUMAN_REJECTED: HumanResultKind.REJECT,
        }.get(guard_id)
        if expected is None or len(request.human_result_refs) != 1:
            raise ValueError("result guard requires one exact current HumanResult ref")
        result = await self._human_repository.load_result(request.human_result_refs[0])
        gate = await self._human_repository.load_gate(result.human_gate_ref) if result else None
        if result is None or gate is None or result.result_kind is not expected:
            return HumanTransitionParticipant(self, request)
        attestation = self._result_attestation(request, gate, result, guard_id)
        return HumanTransitionParticipant(self, request, attestation=attestation)

    async def policy_guard_participant(
        self, request: TransitionRequest, guard_id: GuardId
    ) -> HumanTransitionParticipant:
        if guard_id not in {
            GuardId.G_HUMAN_NOT_REQUIRED,
            GuardId.G_NO_PENDING_HUMAN_GATE,
            GuardId.G_SUSPENDED_HUMAN_GATE,
            GuardId.G_RESUMABLE_HUMAN_GATE,
        }:
            raise ValueError("unsupported P1-7 Human policy guard")
        gate = await self._human_repository.load_current_gate(request.work_run_id)
        if gate is None and guard_id in {
            GuardId.G_SUSPENDED_HUMAN_GATE,
            GuardId.G_RESUMABLE_HUMAN_GATE,
        }:
            return HumanTransitionParticipant(self, request)
        gate_ref = gate.serialized_ref if gate is not None else "NONE"
        revision = gate.gate_authority_revision if gate is not None else 0
        provisional = HumanGuardAttestation(
            "human-guard-"
            + canonical_hash([request.transition_request_id, guard_id.value, gate_ref, revision]),
            HUMAN_GUARD_ATTESTATION_VERSION,
            "",
            guard_id,
            request.task_contract_id,
            request.task_contract_version,
            request.work_run_id,
            cast(WorkflowState, request.observed_state),
            request.observed_state_version,
            request.target_state,
            _target_fingerprint(request),
            gate_ref,
            revision,
            HUMAN_GATE_PURPOSE_ID,
            HUMAN_GATE_PURPOSE_VERSION,
            None,
            None,
            self.authority_id,
            self.authority_version,
            revision,
            self._clock().astimezone(UTC),
            gate.expires_at if gate is not None else None,
        )
        attestation = replace(
            provisional, fingerprint=human_guard_attestation_fingerprint(provisional)
        )
        lifecycle = guard_id is GuardId.G_RESUMABLE_HUMAN_GATE
        return HumanTransitionParticipant(
            self, request, attestation=attestation, lifecycle=lifecycle
        )

    def lifecycle_participant(self, request: TransitionRequest) -> HumanTransitionParticipant:
        return HumanTransitionParticipant(self, request, lifecycle=True)

    async def correct_gate(
        self,
        gate_ref: str,
        *,
        designated_principal_selector_fingerprint: str,
    ) -> HumanGate:
        current = await self._human_repository.load_gate(gate_ref)
        if current is None:
            raise HumanAuthorityError(HumanAuthorityReason.UNKNOWN_HUMAN_GATE)
        reservation = self._reservation_authority.reserve_correction(
            current,
            designated_principal_selector_fingerprint=(designated_principal_selector_fingerprint),
        )
        return await self._human_repository.supersede_gate(
            current,
            reservation,
            authority_id=self.authority_id,
            authority_version=self.authority_version,
        )

    def recognizes(self, fact: TrustedGuardFact, request: TransitionRequest) -> bool:
        return bool(
            fact._issuer_token is self._token
            and fact.authority_ref in self._active.get(request.transition_request_id, set())
        )

    def activate(self, request: TransitionRequest, attestation: HumanGuardAttestation) -> None:
        self._active.setdefault(request.transition_request_id, set()).add(
            attestation.serialized_ref
        )

    def deactivate(self, request: TransitionRequest) -> None:
        self._active.pop(request.transition_request_id, None)

    def fact(self, attestation: HumanGuardAttestation) -> TrustedGuardFact:
        bound_refs = (
            (attestation.human_result_ref,)
            if attestation.guard_id
            in {GuardId.G_HUMAN_APPROVED, GuardId.G_HUMAN_REWORK, GuardId.G_HUMAN_REJECTED}
            and attestation.human_result_ref is not None
            else ()
        )
        return TrustedGuardFact(
            attestation.guard_id,
            self.semantic_owner,
            True,
            "P1_7_HUMAN_AUTHORITY_CURRENT",
            attestation.serialized_ref,
            bound_refs,
            attestation.task_contract_id,
            attestation.task_contract_version,
            attestation.work_run_id,
            attestation.state_version,
            self._token,
        )

    def _human_required_attestation(
        self,
        request: TransitionRequest,
        reservation: HumanGateReservation,
        evidence: EvidenceSetSatisfactionAttestation,
    ) -> HumanGuardAttestation:
        binding = _evidence_binding(evidence)
        provisional = HumanGuardAttestation(
            "human-guard-"
            + canonical_hash(
                [
                    request.transition_request_id,
                    GuardId.G_HUMAN_REQUIRED.value,
                    evidence.serialized_ref,
                ]
            ),
            HUMAN_GUARD_ATTESTATION_VERSION,
            "",
            GuardId.G_HUMAN_REQUIRED,
            request.task_contract_id,
            request.task_contract_version,
            request.work_run_id,
            cast(WorkflowState, request.observed_state),
            request.observed_state_version,
            request.target_state,
            _target_fingerprint(request),
            f"p1-7-gate:{reservation.human_gate_version}:{reservation.human_gate_id}",
            1,
            reservation.purpose_id,
            reservation.purpose_version,
            None,
            None,
            self.authority_id,
            self.authority_version,
            1,
            self._clock().astimezone(UTC),
            reservation.expires_at,
            binding,
        )
        return replace(provisional, fingerprint=human_guard_attestation_fingerprint(provisional))

    def _result_attestation(
        self,
        request: TransitionRequest,
        gate: HumanGate,
        result: object,
        guard_id: GuardId,
    ) -> HumanGuardAttestation:
        from aiscc.human.models import HumanResult

        assert isinstance(result, HumanResult)
        provisional = HumanGuardAttestation(
            "human-guard-"
            + canonical_hash(
                [request.transition_request_id, guard_id.value, result.serialized_ref]
            ),
            HUMAN_GUARD_ATTESTATION_VERSION,
            "",
            guard_id,
            request.task_contract_id,
            request.task_contract_version,
            request.work_run_id,
            cast(WorkflowState, request.observed_state),
            request.observed_state_version,
            request.target_state,
            _target_fingerprint(request),
            gate.serialized_ref,
            gate.gate_authority_revision,
            gate.purpose_id,
            gate.purpose_version,
            result.serialized_ref,
            result.result_authority_revision,
            self.authority_id,
            self.authority_version,
            gate.gate_authority_revision,
            self._clock().astimezone(UTC),
            gate.expires_at,
        )
        return replace(provisional, fingerprint=human_guard_attestation_fingerprint(provisional))


class HumanTransitionParticipant:
    def __init__(
        self,
        authority: HumanGuardAuthority,
        request: TransitionRequest,
        *,
        reservation: HumanGateReservation | None = None,
        attestation: HumanGuardAttestation | None = None,
        proposed_evidence: EvidenceSetSatisfactionAttestation | None = None,
        lifecycle: bool = False,
    ) -> None:
        self._authority = authority
        self._request = request
        self._reservation = reservation
        self._attestation = attestation
        self._proposed_evidence = proposed_evidence
        self._lifecycle = lifecycle
        self._prepared = False

    def facts(self, request: TransitionRequest) -> tuple[TrustedGuardFact, ...]:
        if request != self._request or self._attestation is None:
            return ()
        return (self._authority.fact(self._attestation),)

    async def prepare(
        self, session: AsyncSession, request: TransitionRequest, current: WorkRun | None
    ) -> None:
        if self._attestation is None or current is None:
            return
        now = self._authority._clock().astimezone(UTC)
        valid = False
        if self._attestation.guard_id is GuardId.G_HUMAN_REQUIRED:
            try:
                loader = self._authority._evidence_repository
                current_evidence = await loader.load_effective_attestation_in_session(
                    session,
                    cast(
                        HumanRequiredEvidenceBinding, self._attestation.pre_human_evidence
                    ).attestation_ref,
                )
            except EvidenceAuthorityConflictError:
                current_evidence = None
            expected_checkpoint = self._authority._checkpoint_uses.resolve_transition(request)
            valid = bool(
                self._reservation is not None
                and self._authority._reservation_authority.matches_request(
                    self._reservation, request
                )
                and (self._reservation.expires_at is None or now < self._reservation.expires_at)
                and _gate_attestation_matches_reservation(
                    self._attestation, self._reservation, request
                )
                and current_evidence == self._proposed_evidence
                and current_evidence is not None
                and expected_checkpoint == current_evidence.checkpoint_ref
                and _request_matches_current(request, current)
                and _pre_human_matches(request, current_evidence)
            )
        elif self._attestation.guard_id in {
            GuardId.G_HUMAN_APPROVED,
            GuardId.G_HUMAN_REWORK,
            GuardId.G_HUMAN_REJECTED,
        }:
            valid = await _result_guard_current(session, request, self._attestation, now)
        else:
            valid = await _policy_guard_current(
                session,
                request,
                self._attestation,
                self._authority._reservation_authority,
                now,
            )
        if valid:
            self._prepared = True
            self._authority.activate(request, self._attestation)

    def after_evaluation(self, request: TransitionRequest) -> None:
        self._authority.deactivate(request)

    async def after_decision(
        self,
        session: AsyncSession,
        request: TransitionRequest,
        evaluation: TransitionEvaluation,
        decision: TransitionDecision,
        current: WorkRun | None,
    ) -> None:
        del evaluation, current
        if self._attestation is None:
            if decision.outcome is DecisionOutcome.ADMITTED and self._lifecycle:
                await _apply_gate_lifecycle(
                    session, request, decision, self._authority._clock().astimezone(UTC)
                )
            return
        if self._prepared:
            existing = await session.get(HumanGuardAttestationRow, self._attestation.attestation_id)
            if existing is None:
                session.add(_human_attestation_row(self._attestation))
                await session.flush()
            elif existing.fingerprint != self._attestation.fingerprint:
                raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
        if (
            decision.outcome is DecisionOutcome.ADMITTED
            and self._attestation.guard_id is GuardId.G_HUMAN_REQUIRED
        ):
            assert self._reservation is not None
            await _open_gate(
                session,
                request,
                decision,
                self._reservation,
                self._authority,
                self._authority._clock().astimezone(UTC),
            )
        elif decision.outcome is DecisionOutcome.ADMITTED and self._lifecycle:
            await _apply_gate_lifecycle(
                session, request, decision, self._authority._clock().astimezone(UTC)
            )


async def _open_gate(
    session: AsyncSession,
    request: TransitionRequest,
    decision: TransitionDecision,
    reservation: HumanGateReservation,
    authority: HumanGuardAuthority,
    now: datetime,
) -> None:
    if (
        not authority._reservation_authority.matches_request(reservation, request)
        or (reservation.expires_at is not None and now >= reservation.expires_at)
        or decision.resulting_state is not WorkflowState.HUMAN_REQUIRED
        or decision.resulting_state_version != request.observed_state_version + 1
    ):
        raise HumanAuthorityError(HumanAuthorityReason.HUMAN_AUTHORITY_MISMATCH)
    serialized_ref = f"p1-7-gate:{reservation.human_gate_version}:{reservation.human_gate_id}"
    existing = await session.get(HumanGateRow, reservation.human_gate_id)
    if existing is not None:
        if existing.gate_fingerprint != reservation.gate_fingerprint:
            raise HumanAuthorityError(HumanAuthorityReason.AUTHORITY_CONFLICT)
        return
    opened_at = decision.decided_at
    gate = HumanGateRow(
        human_gate_id=reservation.human_gate_id,
        serialized_ref=serialized_ref,
        gate_fingerprint=reservation.gate_fingerprint,
        task_contract_id=reservation.task_contract_id,
        task_contract_version=reservation.task_contract_version,
        work_run_id=reservation.work_run_id,
        opened_from_state=reservation.opened_from_state.value,
        opened_from_state_version=reservation.opened_from_state_version,
        bound_state_version=decision.resulting_state_version,
        payload={
            "human_gate_version": reservation.human_gate_version,
            "purpose_id": reservation.purpose_id,
            "purpose_version": reservation.purpose_version,
            "opening_transition_request_id": request.transition_request_id,
            "opening_transition_decision_id": decision.transition_decision_id,
            "authority_policy_ref": reservation.authority_policy_ref,
            "authority_policy_version": reservation.authority_policy_version,
            "designated_principal_selector_fingerprint": (
                reservation.designated_principal_selector_fingerprint
            ),
            "gate_authority_id": authority.authority_id,
            "gate_authority_version": authority.authority_version,
            "expires_at": reservation.expires_at.isoformat() if reservation.expires_at else None,
            "supersedes_gate_ref": None,
        },
        opened_at=opened_at,
    )
    session.add(gate)
    await session.flush()
    event = HumanGateAuthorityEventRow(
        event_id=f"human-gate-event-{canonical_hash([serialized_ref, 'OPENED'])}",
        human_gate_id=reservation.human_gate_id,
        event_kind="OPENED",
        prior_revision=0,
        new_revision=1,
        payload={
            "transition_request_id": request.transition_request_id,
            "transition_decision_id": decision.transition_decision_id,
            "bound_state": WorkflowState.HUMAN_REQUIRED.value,
            "bound_state_version": decision.resulting_state_version,
        },
        created_at=opened_at,
    )
    session.add(event)
    await session.flush()
    session.add(
        HumanGateProjectionRow(
            human_gate_id=reservation.human_gate_id,
            work_run_id=reservation.work_run_id,
            authority_epoch=f"{reservation.work_run_id}:{decision.resulting_state_version}",
            status=HumanGateStatus.PENDING.value,
            suspension_status=HumanGateSuspensionStatus.ACTIVE.value,
            authority_revision=1,
            bound_state=WorkflowState.HUMAN_REQUIRED.value,
            bound_state_version=decision.resulting_state_version,
            current_result_ref=None,
            latest_event_sequence=event.event_sequence,
            updated_at=opened_at,
        )
    )


async def _result_guard_current(
    session: AsyncSession,
    request: TransitionRequest,
    attestation: HumanGuardAttestation,
    now: datetime,
) -> bool:
    result_row = await session.scalar(
        select(HumanResultRow).where(HumanResultRow.serialized_ref == attestation.human_result_ref)
    )
    gate_row = await session.scalar(
        select(HumanGateRow).where(HumanGateRow.serialized_ref == attestation.human_gate_ref)
    )
    projection = (
        await session.get(HumanGateProjectionRow, gate_row.human_gate_id)
        if gate_row is not None
        else None
    )
    run = await session.get(WorkRunRow, request.work_run_id)
    if result_row is None or gate_row is None or projection is None or run is None:
        return False
    await _verify_gate_consistency_in_session(session, gate_row, projection)
    await _expire_pending_gate_in_session(session, gate_row, projection, now)
    result = _result_from_row(result_row)
    gate = HumanGateStatus(projection.status)
    expected_kind = {
        GuardId.G_HUMAN_APPROVED: HumanResultKind.APPROVE,
        GuardId.G_HUMAN_REWORK: HumanResultKind.REWORK,
        GuardId.G_HUMAN_REJECTED: HumanResultKind.REJECT,
    }[attestation.guard_id]
    return bool(
        gate is HumanGateStatus.RESOLVED
        and projection.current_result_ref == result.serialized_ref
        and projection.authority_revision == attestation.gate_authority_revision
        and result.gate_authority_revision + 1 == projection.authority_revision
        and result.result_kind is expected_kind
        and request.human_result_refs == (result.serialized_ref,)
        and result.task_contract_id == request.task_contract_id
        and result.task_contract_version == request.task_contract_version
        and result.work_run_id == request.work_run_id
        and result.source_state is request.observed_state
        and result.state_version == request.observed_state_version
        and gate_row.task_contract_id == request.task_contract_id
        and gate_row.task_contract_version == request.task_contract_version
        and gate_row.work_run_id == request.work_run_id
        and projection.bound_state == request.observed_state.value
        and projection.bound_state_version == request.observed_state_version
        and result.human_gate_ref == gate_row.serialized_ref
        and attestation.human_gate_ref == gate_row.serialized_ref
        and attestation.human_result_ref == result.serialized_ref
        and attestation.expires_at == _dt(gate_row.payload.get("expires_at"))
        and (attestation.expires_at is None or now < attestation.expires_at)
        and str(gate_row.payload.get("purpose_id")) == HUMAN_GATE_PURPOSE_ID
        and str(gate_row.payload.get("purpose_version")) == HUMAN_GATE_PURPOSE_VERSION
        and _guard_target_matches_result(request.target_state, expected_kind)
        and _request_row_matches(request, run)
        and attestation.target_use_fingerprint == _target_fingerprint(request)
    )


async def _policy_guard_current(
    session: AsyncSession,
    request: TransitionRequest,
    attestation: HumanGuardAttestation,
    policy: HumanGateReservationAuthority,
    now: datetime,
) -> bool:
    pending = tuple(
        await session.scalars(
            select(HumanGateProjectionRow).where(
                HumanGateProjectionRow.work_run_id == request.work_run_id,
                HumanGateProjectionRow.status == HumanGateStatus.PENDING.value,
            )
        )
    )
    run = await session.get(WorkRunRow, request.work_run_id)
    if run is None or not _request_row_matches(request, run):
        return False
    current_pending: list[HumanGateProjectionRow] = []
    for projection in pending:
        gate_row = await session.get(HumanGateRow, projection.human_gate_id)
        if gate_row is None:
            raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
        await _verify_gate_consistency_in_session(session, gate_row, projection)
        if not await _expire_pending_gate_in_session(session, gate_row, projection, now):
            current_pending.append(projection)
    pending = tuple(current_pending)
    if attestation.guard_id is GuardId.G_HUMAN_NOT_REQUIRED:
        return not pending and not policy.requires_human(request)
    if attestation.guard_id is GuardId.G_NO_PENDING_HUMAN_GATE:
        return not pending
    if len(pending) != 1:
        return False
    projection = pending[0]
    gate_row = await session.get(HumanGateRow, projection.human_gate_id)
    if gate_row is None:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    await _verify_gate_consistency_in_session(session, gate_row, projection)
    return bool(
        projection.human_gate_id == attestation.human_gate_ref.rsplit(":", 1)[-1]
        and projection.authority_revision == attestation.gate_authority_revision
        and projection.bound_state == WorkflowState.BLOCKED.value
        and projection.bound_state_version == request.observed_state_version
        and projection.suspension_status == HumanGateSuspensionStatus.SUSPENDED.value
        and attestation.guard_id in {GuardId.G_SUSPENDED_HUMAN_GATE, GuardId.G_RESUMABLE_HUMAN_GATE}
        and attestation.target_use_fingerprint == _target_fingerprint(request)
        and (attestation.expires_at is None or now < attestation.expires_at)
    )


async def _apply_gate_lifecycle(
    session: AsyncSession,
    request: TransitionRequest,
    decision: TransitionDecision,
    now: datetime,
) -> None:
    projection = await session.scalar(
        select(HumanGateProjectionRow)
        .where(
            HumanGateProjectionRow.work_run_id == request.work_run_id,
            HumanGateProjectionRow.status == HumanGateStatus.PENDING.value,
        )
        .with_for_update()
    )
    if projection is None:
        return
    gate_row = await session.get(HumanGateRow, projection.human_gate_id)
    if gate_row is None:
        raise HumanAuthorityError(HumanAuthorityReason.PROVENANCE_INCOMPLETE)
    await _verify_gate_consistency_in_session(session, gate_row, projection)
    if await _expire_pending_gate_in_session(session, gate_row, projection, now):
        return
    source = cast(WorkflowState, request.observed_state)
    if (
        projection.bound_state != source.value
        or projection.bound_state_version != request.observed_state_version
    ):
        raise HumanAuthorityError(HumanAuthorityReason.HUMAN_GATE_NOT_CURRENT)
    target = request.target_state
    if (source, target) == (WorkflowState.HUMAN_REQUIRED, WorkflowState.BLOCKED):
        event_kind = "SUSPENDED"
        status = HumanGateStatus.PENDING
        suspension = HumanGateSuspensionStatus.SUSPENDED
    elif (source, target) == (WorkflowState.BLOCKED, WorkflowState.HUMAN_REQUIRED):
        event_kind = "REACTIVATED"
        status = HumanGateStatus.PENDING
        suspension = HumanGateSuspensionStatus.ACTIVE
    elif (source, target) == (WorkflowState.BLOCKED, WorkflowState.FAILED):
        event_kind = "CANCELLED"
        status = HumanGateStatus.CANCELLED
        suspension = HumanGateSuspensionStatus.NOT_APPLICABLE
    else:
        return
    prior_revision = projection.authority_revision
    event = HumanGateAuthorityEventRow(
        event_id="human-gate-event-"
        + canonical_hash(
            [
                projection.human_gate_id,
                event_kind,
                prior_revision,
                decision.transition_decision_id,
            ]
        ),
        human_gate_id=projection.human_gate_id,
        event_kind=event_kind,
        prior_revision=prior_revision,
        new_revision=prior_revision + 1,
        payload={
            "transition_request_id": request.transition_request_id,
            "transition_decision_id": decision.transition_decision_id,
            "bound_state": target.value,
            "bound_state_version": decision.resulting_state_version,
        },
        created_at=decision.decided_at,
    )
    session.add(event)
    await session.flush()
    projection.status = status.value
    projection.suspension_status = suspension.value
    projection.authority_revision = prior_revision + 1
    projection.bound_state = target.value
    projection.bound_state_version = decision.resulting_state_version
    projection.authority_epoch = f"{request.work_run_id}:{decision.resulting_state_version}"
    projection.latest_event_sequence = event.event_sequence
    projection.updated_at = decision.decided_at


def _request_matches_current(request: TransitionRequest, current: WorkRun) -> bool:
    return bool(
        request.task_contract_id == current.task_contract_id
        and request.task_contract_version == current.task_contract_version
        and request.work_run_id == current.work_run_id
        and request.observed_state is current.state
        and request.observed_state_version == current.state_version
    )


def _request_row_matches(request: TransitionRequest, run: WorkRunRow) -> bool:
    return bool(
        request.task_contract_id == run.task_contract_id
        and request.task_contract_version == run.task_contract_version
        and request.work_run_id == run.work_run_id
        and request.observed_state is WorkflowState(run.workflow_state)
        and request.observed_state_version == run.state_version
    )


def _pre_human_matches(
    request: TransitionRequest, evidence: EvidenceSetSatisfactionAttestation
) -> bool:
    return bool(
        evidence.satisfied
        and evidence.task_contract_id == request.task_contract_id
        and evidence.task_contract_version == request.task_contract_version
        and evidence.work_run_id == request.work_run_id
        and evidence.source_state is request.observed_state
        and evidence.state_version == request.observed_state_version
        and evidence.target_state is request.target_state
        and evidence.transition_purpose_id is None
        and evidence.transition_purpose_version is None
    )


def _evidence_binding(value: EvidenceSetSatisfactionAttestation) -> HumanRequiredEvidenceBinding:
    return HumanRequiredEvidenceBinding(
        value.serialized_ref,
        value.attestation_version,
        value.checkpoint_ref.serialized(),
        value.checkpoint_fingerprint,
        value.task_contract_id,
        value.task_contract_version,
        value.work_run_id,
        value.source_state,
        value.state_version,
        value.target_state,
        value.transition_purpose_id,
        value.transition_purpose_version,
        value.requirement_set_id,
        value.requirement_set_version,
        value.full_requirement_root_hash,
        value.ordered_applicable_requirement_refs,
        value.checkpoint_subset_root_hash,
        value.ordered_admitted_evidence_refs,
        value.admitted_ref_root_hash,
        value.evidence_authority_version,
        value.evidence_authority_revision,
        value.issued_at,
        value.expires_at,
        value.issuer_id,
        value.issuer_version,
    )


def _target_fingerprint(request: TransitionRequest) -> str:
    return canonical_hash(
        [
            request.task_contract_id,
            request.task_contract_version,
            request.work_run_id,
            request.observed_state.value if request.observed_state else None,
            request.observed_state_version,
            request.target_state.value,
        ]
    )


def _reservation_fingerprint(reservation: HumanGateReservation) -> str:
    return canonical_hash(
        {
            "gate": [reservation.human_gate_id, reservation.human_gate_version],
            "purpose": [reservation.purpose_id, reservation.purpose_version],
            "task": [reservation.task_contract_id, reservation.task_contract_version],
            "run": reservation.work_run_id,
            "source": [
                reservation.opened_from_state.value,
                reservation.opened_from_state_version,
            ],
            "target": reservation.target_state.value,
            "policy": [
                reservation.authority_policy_ref,
                reservation.authority_policy_version,
            ],
            "selector": reservation.designated_principal_selector_fingerprint,
            "expires_at": (reservation.expires_at.isoformat() if reservation.expires_at else None),
        }
    )


def _gate_attestation_matches_reservation(
    attestation: HumanGuardAttestation,
    reservation: HumanGateReservation,
    request: TransitionRequest,
) -> bool:
    return bool(
        attestation.task_contract_id == reservation.task_contract_id
        and attestation.task_contract_version == reservation.task_contract_version
        and attestation.work_run_id == reservation.work_run_id
        and attestation.source_state is reservation.opened_from_state
        and attestation.state_version == reservation.opened_from_state_version
        and attestation.target_state is reservation.target_state
        and attestation.target_use_fingerprint == _target_fingerprint(request)
        and attestation.human_gate_ref
        == f"p1-7-gate:{reservation.human_gate_version}:{reservation.human_gate_id}"
        and attestation.purpose_id == reservation.purpose_id
        and attestation.purpose_version == reservation.purpose_version
        and attestation.expires_at == reservation.expires_at
    )


def _guard_target_matches_result(target: WorkflowState, result_kind: HumanResultKind) -> bool:
    return {
        HumanResultKind.APPROVE: WorkflowState.ACCEPTED,
        HumanResultKind.REWORK: WorkflowState.REWORK_REQUIRED,
        HumanResultKind.REJECT: WorkflowState.REJECTED,
    }[result_kind] is target


def _human_attestation_row(value: HumanGuardAttestation) -> HumanGuardAttestationRow:
    payload = human_guard_attestation_payload(value)
    return HumanGuardAttestationRow(
        attestation_id=value.attestation_id,
        serialized_ref=value.serialized_ref,
        fingerprint=value.fingerprint,
        guard_id=value.guard_id.value,
        work_run_id=value.work_run_id,
        state_version=value.state_version,
        authority_revision=value.authority_revision,
        payload=payload,
        issued_at=value.issued_at,
        expires_at=value.expires_at,
    )


def public_human_projection(
    gate: HumanGate, result_kind: HumanResultKind | None
) -> dict[str, object]:
    return {
        "human_review": "performed" if gate.status is HumanGateStatus.RESOLVED else "pending",
        "principal_display": "HUMAN_REVIEWER",
        "result_kind": result_kind.value if result_kind is not None else None,
    }
