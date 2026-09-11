from __future__ import annotations

from collections.abc import Callable
from dataclasses import asdict, replace
from datetime import UTC, datetime, timedelta
from typing import cast

from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.contracts.workflow import WorkflowState
from aiscc.evidence.models import (
    EvidenceAuthorityConflictError,
    EvidenceSetOutcome,
    canonical_hash,
)
from aiscc.evidence.repository import (
    HistoricalEvidenceProvenanceError,
    PostgresEvidenceRepository,
    verify_historical_set_attestation_provenance,
    verify_historical_set_evaluation_provenance,
)
from aiscc.human.models import (
    HumanAuthorityError,
    HumanAuthorityReason,
    HumanGateStatus,
    HumanResultKind,
)
from aiscc.human.repository import (
    _result_from_row,
    _verify_gate_consistency_in_session,
    _verify_human_result_historical_provenance_in_session,
)
from aiscc.judgment.models import (
    CommandCenterActionAuthority,
    CommandCenterPrincipal,
    Judgment,
    JudgmentAuthorityError,
    JudgmentEvidenceBasisKind,
    JudgmentGuardAttestation,
    JudgmentIdentityConflictError,
    JudgmentKind,
    JudgmentOwnerPolicy,
    JudgmentPolicy,
)
from aiscc.persistence.models import (
    CommandCenterJudgmentActionRow,
    HumanGateProjectionRow,
    HumanGateRow,
    HumanResultRow,
    JudgmentAuthorityEventRow,
    JudgmentEvaluationRow,
    JudgmentGuardAttestationRow,
    JudgmentPolicyProjectionRow,
    JudgmentPolicyRow,
    JudgmentProjectionRow,
    JudgmentRow,
    WorkRunRow,
)
from aiscc.persistence.repository import (
    acquire_judgment_transaction_lock,
    acquire_work_run_transaction_lock,
)
from aiscc.workflow.guards import TrustedGuardFact
from aiscc.workflow.models import (
    GuardId,
    GuardSemanticOwner,
    TransitionDecision,
    TransitionEvaluation,
    TransitionRequest,
    WorkRun,
)


class JudgmentPolicyAuthority:
    """Server-owned TaskContract judgment-policy issuer; callers cannot mint policy truth."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        *,
        clock: Callable[[], datetime] | None = None,
        authority_id: str = "AISCC_P1_7_JUDGMENT_POLICY_AUTHORITY_V1",
        authority_version: str = "p1-7-judgment-policy-v1",
    ) -> None:
        self._session_factory = session_factory
        self._clock = clock or (lambda: datetime.now(UTC))
        self.authority_id = authority_id
        self.authority_version = authority_version
        self._token = object()

    async def register(
        self,
        *,
        policy_id: str,
        policy_version: str,
        task_contract_id: str,
        task_contract_version: str,
        source_state: WorkflowState,
        target_state: WorkflowState,
        owner_policy: JudgmentOwnerPolicy,
        requires_human_result: bool,
        requires_post_human_evidence: bool,
        deterministic_kind: JudgmentKind | None = None,
        evidence_basis_kind: JudgmentEvidenceBasisKind | None = None,
        evidence_checkpoint_ref: str | None = None,
        evidence_requirement_set_ref: str | None = None,
    ) -> JudgmentPolicy:
        if (owner_policy is JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC) != (
            deterministic_kind is not None
        ):
            raise ValueError("deterministic Judgment policy requires exactly one fixed kind")
        if owner_policy is JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC and requires_human_result:
            raise ValueError("deterministic Judgment policy cannot depend on HumanResult")
        if owner_policy is JudgmentOwnerPolicy.HUMAN and not requires_human_result:
            raise ValueError("Human Judgment policy requires HumanResult")
        if owner_policy is JudgmentOwnerPolicy.COMMAND_CENTER and requires_human_result:
            raise ValueError("Command Center policy cannot substitute HumanResult")
        if evidence_basis_kind is None:
            if evidence_checkpoint_ref is not None or evidence_requirement_set_ref is not None:
                raise ValueError("legacy Judgment policy cannot enroll partial evidence basis")
        else:
            if not evidence_checkpoint_ref or not evidence_requirement_set_ref:
                raise ValueError("typed Judgment policy requires checkpoint and requirement set")
            if (
                evidence_basis_kind is JudgmentEvidenceBasisKind.SATISFIED_ATTESTATION
                and not requires_post_human_evidence
            ):
                raise ValueError("positive evidence basis requires admitted evidence")
            if evidence_basis_kind is JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION and (
                owner_policy is not JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC
                or deterministic_kind is not JudgmentKind.HOLD_REWORK_REQUIRED
                or target_state is not WorkflowState.REWORK_REQUIRED
                or requires_post_human_evidence
            ):
                raise ValueError("negative evidence basis requires deterministic rework policy")
        now = self._clock().astimezone(UTC)
        scope_key = _policy_scope_key(
            task_contract_id, task_contract_version, source_state, target_state
        )
        serialized_ref = f"p1-7-judgment-policy:{policy_version}:{policy_id}"
        async with self._session_factory() as session, session.begin():
            await session.execute(
                text("SELECT pg_advisory_xact_lock(hashtextextended(:key, 0))"),
                {"key": f"aiscc:p1-7:judgment-policy:{scope_key}"},
            )
            projection = await session.scalar(
                select(JudgmentPolicyProjectionRow)
                .where(JudgmentPolicyProjectionRow.policy_scope_key == scope_key)
                .with_for_update()
            )
            existing = await session.get(JudgmentPolicyRow, serialized_ref)
            revision = (
                existing.authority_revision
                if existing is not None
                else (projection.authority_revision + 1 if projection is not None else 1)
            )
            provisional = JudgmentPolicy(
                policy_id,
                policy_version,
                "",
                task_contract_id,
                task_contract_version,
                source_state,
                target_state,
                _policy_use_fingerprint(
                    task_contract_id, task_contract_version, source_state, target_state
                ),
                owner_policy,
                requires_human_result,
                requires_post_human_evidence,
                deterministic_kind,
                self.authority_id,
                self.authority_version,
                revision,
                now,
                self._token,
                evidence_basis_kind,
                evidence_checkpoint_ref,
                evidence_requirement_set_ref,
            )
            value = replace(provisional, fingerprint=_policy_fingerprint(provisional))
            if existing is not None:
                durable = _policy_from_row(existing, self._token)
                if durable.fingerprint != value.fingerprint:
                    raise JudgmentAuthorityError("JUDGMENT_POLICY_IDENTITY_CONFLICT")
                if (
                    projection is None
                    or projection.current_policy_ref != durable.serialized_ref
                    or projection.authority_revision != durable.policy_authority_revision
                ):
                    raise JudgmentAuthorityError("JUDGMENT_POLICY_STALE")
                return durable
            session.add(_policy_row(value, scope_key))
            await session.flush()
            if projection is None:
                session.add(
                    JudgmentPolicyProjectionRow(
                        policy_scope_key=scope_key,
                        current_policy_ref=value.serialized_ref,
                        authority_revision=revision,
                        updated_at=now,
                    )
                )
            else:
                projection.current_policy_ref = value.serialized_ref
                projection.authority_revision = revision
                projection.updated_at = now
            return value

    async def current_in_session(
        self,
        session: AsyncSession,
        policy: JudgmentPolicy,
        request: TransitionRequest,
    ) -> bool:
        scope_key = _policy_scope_key(
            request.task_contract_id,
            request.task_contract_version,
            cast(WorkflowState, request.observed_state),
            request.target_state,
        )
        await session.execute(
            text("SELECT pg_advisory_xact_lock(hashtextextended(:key, 0))"),
            {"key": f"aiscc:p1-7:judgment-policy:{scope_key}"},
        )
        row = await session.get(JudgmentPolicyRow, policy.serialized_ref)
        projection = await session.get(JudgmentPolicyProjectionRow, scope_key)
        if row is None or projection is None:
            return False
        durable = _policy_from_row(row, self._token)
        return bool(
            durable.fingerprint == _policy_fingerprint(durable)
            and durable == policy
            and projection.current_policy_ref == policy.serialized_ref
            and projection.authority_revision == policy.policy_authority_revision
            and policy.task_contract_id == request.task_contract_id
            and policy.task_contract_version == request.task_contract_version
            and policy.source_state is request.observed_state
            and policy.target_state is request.target_state
            and policy.target_use_fingerprint == _policy_use_for_request(request)
            and policy.policy_authority_id == self.authority_id
            and policy.policy_authority_version == self.authority_version
        )


class CommandCenterAuthority:
    """Narrow local server-owned Command Center principal/action authority."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        policy_authority: JudgmentPolicyAuthority,
        *,
        clock: Callable[[], datetime] | None = None,
        authority_id: str = "AISCC_P1_7_COMMAND_CENTER_AUTHORITY_V1",
        authority_version: str = "p1-7-command-center-v1",
    ) -> None:
        self._session_factory = session_factory
        self._policy_authority = policy_authority
        self._clock = clock or (lambda: datetime.now(UTC))
        self.authority_id = authority_id
        self.authority_version = authority_version
        self._token = object()

    def authenticate(self, *, principal_id: str, ttl_seconds: int = 300) -> CommandCenterPrincipal:
        now = self._clock().astimezone(UTC)
        if not principal_id or ttl_seconds <= 0:
            raise JudgmentAuthorityError("COMMAND_CENTER_PRINCIPAL_INVALID")
        return CommandCenterPrincipal(
            principal_id,
            self.authority_id,
            self.authority_version,
            now,
            now + timedelta(seconds=ttl_seconds),
            self._token,
        )

    async def issue_action(
        self,
        *,
        action_id: str,
        principal: CommandCenterPrincipal,
        request: TransitionRequest,
        policy: JudgmentPolicy,
        judgment_kind: JudgmentKind,
        ttl_seconds: int = 120,
    ) -> CommandCenterActionAuthority:
        if (
            principal._issuer_token is not self._token
            or ttl_seconds <= 0
            or policy.owner_policy is not JudgmentOwnerPolicy.COMMAND_CENTER
            or _guard_for_kind(judgment_kind) is not _guard_for_target(request.target_state)
        ):
            raise JudgmentAuthorityError("COMMAND_CENTER_AUTHORITY_REQUIRED")
        async with self._session_factory() as session, session.begin():
            await acquire_work_run_transaction_lock(session, request.work_run_id)
            run = await session.scalar(
                select(WorkRunRow)
                .where(WorkRunRow.work_run_id == request.work_run_id)
                .with_for_update()
            )
            if (
                run is None
                or not _request_matches_run(request, run)
                or not await self._policy_authority.current_in_session(session, policy, request)
            ):
                raise JudgmentAuthorityError("COMMAND_CENTER_AUTHORITY_REQUIRED")
            now = self._clock().astimezone(UTC)
            if now >= principal.expires_at:
                raise JudgmentAuthorityError("COMMAND_CENTER_AUTHORITY_REQUIRED")
            provisional = CommandCenterActionAuthority(
                action_id,
                "p1-7-command-center-action-v1",
                "",
                principal.principal_id,
                request.task_contract_id,
                request.task_contract_version,
                request.work_run_id,
                cast(WorkflowState, request.observed_state),
                request.observed_state_version,
                request.target_state,
                _target_fingerprint(request),
                policy.serialized_ref,
                policy.fingerprint,
                policy.policy_authority_revision,
                judgment_kind,
                now,
                min(now + timedelta(seconds=ttl_seconds), principal.expires_at),
                self.authority_id,
                self.authority_version,
                self._token,
            )
            value = replace(provisional, fingerprint=_command_center_fingerprint(provisional))
            existing = await session.get(CommandCenterJudgmentActionRow, value.serialized_ref)
            if existing is None:
                session.add(_command_center_row(value))
            elif existing.fingerprint != value.fingerprint:
                raise JudgmentAuthorityError("COMMAND_CENTER_ACTION_IDENTITY_CONFLICT")
            else:
                value = _command_center_from_row(existing, self._token)
            return value

    async def current_in_session(
        self,
        session: AsyncSession,
        action_ref: str | None,
        request: TransitionRequest,
        policy: JudgmentPolicy,
        now: datetime,
    ) -> CommandCenterActionAuthority | None:
        if action_ref is None:
            return None
        row = await session.get(CommandCenterJudgmentActionRow, action_ref)
        if row is None:
            return None
        value = _command_center_from_row(row, self._token)
        return (
            value
            if value.fingerprint == _command_center_fingerprint(value)
            and now < value.expires_at
            and value.task_contract_id == request.task_contract_id
            and value.task_contract_version == request.task_contract_version
            and value.work_run_id == request.work_run_id
            and value.source_state is request.observed_state
            and value.state_version == request.observed_state_version
            and value.target_state is request.target_state
            and value.target_use_fingerprint == _target_fingerprint(request)
            and value.policy_ref == policy.serialized_ref
            and value.policy_fingerprint == policy.fingerprint
            and value.policy_authority_revision == policy.policy_authority_revision
            else None
        )


class PostgresJudgmentAuthority:
    semantic_owner = GuardSemanticOwner.P1_7_JUDGMENT

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        evidence_repository: PostgresEvidenceRepository,
        policy_authority: JudgmentPolicyAuthority,
        *,
        command_center_authority: CommandCenterAuthority | None = None,
        clock: Callable[[], datetime] | None = None,
        authority_id: str = "AISCC_P1_7_JUDGMENT_AUTHORITY_V1",
        authority_version: str = "AISCC-P1-7-JUDGMENT-AUTHORITY-V1",
    ) -> None:
        self._session_factory = session_factory
        self._evidence_repository = evidence_repository
        self._policy_authority = policy_authority
        self._command_center_authority = command_center_authority
        self._clock = clock or (lambda: datetime.now(UTC))
        self.authority_id = authority_id
        self.authority_version = authority_version
        self._token = object()
        self._active: dict[str, str] = {}

    async def issue(
        self,
        *,
        judgment_id: str,
        judgment_version: str,
        request: TransitionRequest,
        policy: JudgmentPolicy,
        human_result_ref: str | None,
        evidence_attestation_ref: str | None,
        command_center_action_ref: str | None = None,
        reason_code: str,
        reason_vocabulary_version: str,
        supersedes_judgment_ref: str | None = None,
        evidence_basis_kind: JudgmentEvidenceBasisKind | None = None,
        evidence_evaluation_ref: str | None = None,
    ) -> Judgment:
        if evidence_basis_kind is not None and not isinstance(
            evidence_basis_kind, JudgmentEvidenceBasisKind
        ):
            raise JudgmentAuthorityError("JUDGMENT_INPUT_INCOMPLETE")
        proposal_fingerprint = _judgment_proposal_fingerprint(
            judgment_version=judgment_version,
            request=request,
            policy=policy,
            human_result_ref=human_result_ref,
            evidence_attestation_ref=evidence_attestation_ref,
            command_center_action_ref=command_center_action_ref,
            reason_code=reason_code,
            reason_vocabulary_version=reason_vocabulary_version,
            supersedes_judgment_ref=supersedes_judgment_ref,
            evidence_basis_kind=evidence_basis_kind,
            evidence_evaluation_ref=evidence_evaluation_ref,
        )
        async with self._session_factory() as session, session.begin():
            await acquire_work_run_transaction_lock(session, request.work_run_id)
            await acquire_judgment_transaction_lock(session, judgment_id)
            existing = await session.get(JudgmentRow, judgment_id)
            if existing is not None:
                durable = await _verify_judgment_historical_provenance_in_session(session, existing)
                if existing.payload.get("proposal_fingerprint") != proposal_fingerprint:
                    raise JudgmentIdentityConflictError("JUDGMENT_IDENTITY_CONFLICT")
                return durable
            run = await session.scalar(
                select(WorkRunRow)
                .where(WorkRunRow.work_run_id == request.work_run_id)
                .with_for_update()
            )
            if run is None or not _request_matches_run(request, run):
                raise JudgmentAuthorityError("JUDGMENT_STALE")
            if not await self._policy_authority.current_in_session(session, policy, request):
                raise JudgmentAuthorityError("JUDGMENT_POLICY_MISMATCH")
            current_projection = await session.get(JudgmentProjectionRow, request.work_run_id)
            current_judgment = (
                await session.get(JudgmentRow, current_projection.judgment_id)
                if current_projection is not None
                else None
            )
            if current_projection is not None:
                await _verify_judgment_consistency_in_session(session, current_projection)
            if current_projection is None and supersedes_judgment_ref is not None:
                raise JudgmentAuthorityError("JUDGMENT_SUPERSEDED")
            if current_projection is not None and (
                current_judgment is None
                or current_judgment.serialized_ref != supersedes_judgment_ref
            ):
                raise JudgmentAuthorityError("JUDGMENT_ALREADY_CURRENT")
            result_row = (
                await session.scalar(
                    select(HumanResultRow).where(HumanResultRow.serialized_ref == human_result_ref)
                )
                if human_result_ref
                else None
            )
            projection = (
                await session.get(HumanGateProjectionRow, result_row.human_gate_id)
                if result_row is not None
                else None
            )
            gate_row = (
                await session.get(HumanGateRow, result_row.human_gate_id)
                if result_row is not None
                else None
            )
            result = _result_from_row(result_row) if result_row is not None else None
            if result_row is not None and projection is not None and gate_row is not None:
                assert result is not None
                await _verify_gate_consistency_in_session(session, gate_row, projection)
            issued_at = self._clock().astimezone(UTC)
            human_current = False
            if result_row is not None and projection is not None and gate_row is not None:
                assert result is not None
                gate_expires_at = _optional_datetime(gate_row.payload.get("expires_at"))
                human_current = bool(
                    projection.status == HumanGateStatus.RESOLVED.value
                    and projection.current_result_ref == result.serialized_ref
                    and projection.authority_revision == result.gate_authority_revision + 1
                    and result.human_gate_ref == gate_row.serialized_ref
                    and result.task_contract_id == request.task_contract_id
                    and result.task_contract_version == request.task_contract_version
                    and result.work_run_id == request.work_run_id
                    and result.source_state is request.observed_state
                    and result.state_version == request.observed_state_version
                    and gate_row.task_contract_id == request.task_contract_id
                    and gate_row.task_contract_version == request.task_contract_version
                    and gate_row.work_run_id == request.work_run_id
                    and projection.bound_state
                    == (request.observed_state.value if request.observed_state else None)
                    and projection.bound_state_version == request.observed_state_version
                    and request.human_result_refs == (result.serialized_ref,)
                    and str(gate_row.payload.get("purpose_id")) == "P1_7_WORK_RESULT_REVIEW"
                    and str(gate_row.payload.get("purpose_version")) == "v1"
                    and _guard_for_kind(_judgment_kind(result.result_kind))
                    is _guard_for_target(request.target_state)
                    and (gate_expires_at is None or issued_at < gate_expires_at)
                )
            if policy.owner_policy is JudgmentOwnerPolicy.HUMAN and not human_current:
                raise JudgmentAuthorityError("JUDGMENT_INPUT_INCOMPLETE")
            if policy.owner_policy is not JudgmentOwnerPolicy.HUMAN and result_row is not None:
                raise JudgmentAuthorityError("JUDGMENT_POLICY_MISMATCH")
            if evidence_basis_kind is not policy.evidence_basis_kind:
                raise JudgmentAuthorityError("JUDGMENT_POLICY_MISMATCH")
            if policy.evidence_basis_kind is None and evidence_evaluation_ref is not None:
                raise JudgmentAuthorityError("JUDGMENT_POLICY_MISMATCH")
            if (
                policy.evidence_basis_kind
                is JudgmentEvidenceBasisKind.SATISFIED_ATTESTATION
                and (
                    evidence_attestation_ref is None
                    or evidence_evaluation_ref is not None
                    or request.evidence_refs != (evidence_attestation_ref,)
                )
            ):
                raise JudgmentAuthorityError("JUDGMENT_INPUT_INCOMPLETE")
            if (
                policy.evidence_basis_kind
                is JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION
                and (
                    evidence_evaluation_ref is None
                    or evidence_attestation_ref is not None
                    or request.evidence_refs != (evidence_evaluation_ref,)
                )
            ):
                raise JudgmentAuthorityError("JUDGMENT_INPUT_INCOMPLETE")
            evidence = (
                await self._evidence_repository.load_effective_attestation_in_session(
                    session, evidence_attestation_ref
                )
                if evidence_attestation_ref
                else None
            )
            if policy.requires_post_human_evidence and evidence is None:
                raise JudgmentAuthorityError("HUMAN_EVIDENCE_ADMISSION_REQUIRED")
            if evidence is not None and not (
                evidence.task_contract_id == request.task_contract_id
                and evidence.task_contract_version == request.task_contract_version
                and evidence.work_run_id == request.work_run_id
                and evidence.source_state is request.observed_state
                and evidence.state_version == request.observed_state_version
                and evidence.target_state is request.target_state
            ):
                raise JudgmentAuthorityError("JUDGMENT_STALE")
            if evidence is not None and policy.evidence_basis_kind is not None and (
                evidence.checkpoint_ref.serialized() != policy.evidence_checkpoint_ref
                or f"{evidence.requirement_set_id}@{evidence.requirement_set_version}"
                != policy.evidence_requirement_set_ref
            ):
                raise JudgmentAuthorityError("JUDGMENT_POLICY_MISMATCH")
            negative_evaluation = None
            if (
                policy.evidence_basis_kind
                is JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION
            ):
                assert evidence_evaluation_ref is not None
                assert policy.evidence_checkpoint_ref is not None
                assert policy.evidence_requirement_set_ref is not None
                try:
                    negative_evaluation = (
                        await self._evidence_repository.load_current_set_evaluation_in_session(
                            session,
                            evidence_evaluation_ref,
                            work_run_id=request.work_run_id,
                            source_state=cast(WorkflowState, request.observed_state),
                            state_version=request.observed_state_version,
                            checkpoint_ref=policy.evidence_checkpoint_ref,
                            requirement_set_ref=policy.evidence_requirement_set_ref,
                            expected_outcome=EvidenceSetOutcome.UNSATISFIED,
                            now=issued_at,
                        )
                    )
                except ValueError as exc:
                    raise JudgmentAuthorityError("JUDGMENT_INPUT_INCOMPLETE") from exc
                except EvidenceAuthorityConflictError as exc:
                    raise JudgmentAuthorityError("AUTHORITY_CONFLICT") from exc
                if negative_evaluation is None:
                    raise JudgmentAuthorityError("JUDGMENT_STALE")
            command_center = (
                await self._command_center_authority.current_in_session(
                    session, command_center_action_ref, request, policy, issued_at
                )
                if self._command_center_authority is not None
                else None
            )
            if policy.owner_policy is JudgmentOwnerPolicy.COMMAND_CENTER:
                if command_center is None:
                    raise JudgmentAuthorityError("COMMAND_CENTER_AUTHORITY_REQUIRED")
            elif command_center_action_ref is not None:
                raise JudgmentAuthorityError("JUDGMENT_POLICY_MISMATCH")
            if policy.owner_policy is JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC:
                kind = policy.deterministic_kind
            elif policy.owner_policy is JudgmentOwnerPolicy.HUMAN:
                kind = _judgment_kind(result.result_kind if result else None)
            else:
                kind = command_center.judgment_kind if command_center else None
            if kind is None:
                raise JudgmentAuthorityError("JUDGMENT_INPUT_INCOMPLETE")
            if _guard_for_kind(kind) is not _guard_for_target(request.target_state):
                raise JudgmentAuthorityError("JUDGMENT_POLICY_MISMATCH")
            authority_revision = (
                current_projection.authority_revision + 1 if current_projection is not None else 1
            )
            target_fingerprint = _target_fingerprint(request)
            evaluation_identity: list[object] = [
                judgment_id,
                target_fingerprint,
                human_result_ref,
                evidence_attestation_ref,
                command_center_action_ref,
                policy.fingerprint,
                reason_code,
                reason_vocabulary_version,
                supersedes_judgment_ref,
            ]
            if evidence_basis_kind is not None:
                evaluation_identity.append(
                    [evidence_basis_kind.value, evidence_evaluation_ref]
                )
            evaluation_id = "judgment-evaluation-" + canonical_hash(evaluation_identity)
            provisional = Judgment(
                judgment_id,
                judgment_version,
                "",
                self.authority_id,
                self.authority_version,
                authority_revision,
                request.task_contract_id,
                request.task_contract_version,
                request.work_run_id,
                cast(WorkflowState, request.observed_state),
                request.observed_state_version,
                request.target_state,
                target_fingerprint,
                policy.owner_policy,
                policy.policy_id,
                policy.policy_version,
                policy.fingerprint,
                policy.policy_authority_id,
                policy.policy_authority_version,
                policy.policy_authority_revision,
                command_center.serialized_ref if command_center else None,
                result.human_gate_ref if result else None,
                result.serialized_ref if result else None,
                result.result_authority_revision if result else None,
                evidence.serialized_ref if evidence else None,
                evidence.evidence_authority_revision if evidence else None,
                evidence.admitted_ref_root_hash if evidence else None,
                kind,
                reason_code,
                reason_vocabulary_version,
                evaluation_id,
                issued_at,
                supersedes_judgment_ref,
                evidence_basis_kind,
                negative_evaluation.serialized_ref if negative_evaluation else None,
                (
                    negative_evaluation.evidence_authority_revision
                    if negative_evaluation
                    else None
                ),
                policy.evidence_checkpoint_ref,
                policy.evidence_requirement_set_ref,
            )
            value = replace(provisional, fingerprint=_judgment_fingerprint(provisional))
            session.add(
                JudgmentEvaluationRow(
                    evaluation_id=evaluation_id,
                    work_run_id=request.work_run_id,
                    state_version=request.observed_state_version,
                    payload={
                        "policy": [
                            policy.policy_id,
                            policy.policy_version,
                            policy.fingerprint,
                            policy.policy_authority_revision,
                        ],
                        "human_result_ref": human_result_ref,
                        "evidence_attestation_ref": evidence_attestation_ref,
                        "command_center_action_ref": command_center_action_ref,
                        "outcome": "COMPLETE",
                    }
                    | (
                        {
                            "evidence_basis_kind": evidence_basis_kind.value,
                            "evidence_evaluation_ref": evidence_evaluation_ref,
                        }
                        if evidence_basis_kind is not None
                        else {}
                    ),
                    evaluated_at=issued_at,
                )
            )
            session.add(_judgment_row(value, proposal_fingerprint))
            await session.flush()
            if current_projection is not None and current_judgment is not None:
                session.add(
                    JudgmentAuthorityEventRow(
                        event_id="judgment-event-"
                        + canonical_hash(
                            [
                                current_judgment.serialized_ref,
                                "SUPERSEDED",
                                value.serialized_ref,
                            ]
                        ),
                        judgment_id=current_judgment.judgment_id,
                        event_kind="SUPERSEDED",
                        prior_revision=current_projection.authority_revision,
                        new_revision=authority_revision,
                        payload={"replacement_judgment_ref": value.serialized_ref},
                        created_at=issued_at,
                    )
                )
            event = JudgmentAuthorityEventRow(
                event_id="judgment-event-" + canonical_hash([value.serialized_ref, "ISSUED"]),
                judgment_id=value.judgment_id,
                event_kind="ISSUED",
                prior_revision=authority_revision - 1,
                new_revision=authority_revision,
                payload={"evaluation_ref": evaluation_id},
                created_at=issued_at,
            )
            session.add(event)
            await session.flush()
            if current_projection is None:
                session.add(
                    JudgmentProjectionRow(
                        work_run_id=request.work_run_id,
                        judgment_id=value.judgment_id,
                        authority_revision=authority_revision,
                        latest_event_sequence=event.event_sequence,
                        updated_at=issued_at,
                    )
                )
            else:
                current_projection.judgment_id = value.judgment_id
                current_projection.authority_revision = authority_revision
                current_projection.latest_event_sequence = event.event_sequence
                current_projection.updated_at = issued_at
            return value

    async def verify_consistency(self, work_run_id: str) -> Judgment | None:
        async with self._session_factory() as session, session.begin():
            await acquire_work_run_transaction_lock(session, work_run_id)
            projection = await session.get(JudgmentProjectionRow, work_run_id)
            if projection is None:
                return None
            return await _verify_judgment_consistency_in_session(session, projection)

    async def participant(
        self, request: TransitionRequest, judgment_ref: str
    ) -> JudgmentTransitionParticipant:
        async with self._session_factory() as session:
            row = await session.scalar(
                select(JudgmentRow).where(JudgmentRow.serialized_ref == judgment_ref)
            )
            if row is None:
                return JudgmentTransitionParticipant(self, request)
            judgment = _judgment_from_row(row)
            gate_row = (
                await session.scalar(
                    select(HumanGateRow).where(
                        HumanGateRow.serialized_ref == judgment.human_gate_ref
                    )
                )
                if judgment.human_gate_ref is not None
                else None
            )
            expires_at = (
                _optional_datetime(gate_row.payload.get("expires_at"))
                if gate_row is not None
                else None
            )
        guard_id = _guard_for_kind(judgment.judgment_kind)
        provisional = JudgmentGuardAttestation(
            "judgment-guard-"
            + canonical_hash(
                [request.transition_request_id, guard_id.value, judgment.serialized_ref]
            ),
            "p1-7-judgment-guard-v1",
            "",
            guard_id,
            request.task_contract_id,
            request.task_contract_version,
            request.work_run_id,
            cast(WorkflowState, request.observed_state),
            request.observed_state_version,
            request.target_state,
            _target_fingerprint(request),
            judgment.serialized_ref,
            judgment.authority_revision,
            judgment.human_gate_ref,
            judgment.human_result_ref,
            judgment.evidence_attestation_ref,
            judgment.evidence_authority_revision,
            judgment.policy_id,
            judgment.policy_version,
            judgment.policy_fingerprint,
            judgment.policy_authority_id,
            judgment.policy_authority_version,
            judgment.policy_authority_revision,
            self.authority_id,
            self.authority_version,
            self._clock().astimezone(UTC),
            expires_at,
        )
        attestation = replace(provisional, fingerprint=_guard_fingerprint(provisional))
        return JudgmentTransitionParticipant(self, request, judgment, attestation)

    def recognizes(self, fact: TrustedGuardFact, request: TransitionRequest) -> bool:
        return bool(
            fact._issuer_token is self._token
            and self._active.get(request.transition_request_id) == fact.authority_ref
        )

    def fact(self, attestation: JudgmentGuardAttestation) -> TrustedGuardFact:
        return TrustedGuardFact(
            attestation.guard_id,
            self.semantic_owner,
            True,
            "P1_7_JUDGMENT_AUTHORITY_CURRENT",
            attestation.serialized_ref,
            (attestation.judgment_ref,),
            attestation.task_contract_id,
            attestation.task_contract_version,
            attestation.work_run_id,
            attestation.state_version,
            self._token,
        )


class JudgmentTransitionParticipant:
    def __init__(
        self,
        authority: PostgresJudgmentAuthority,
        request: TransitionRequest,
        judgment: Judgment | None = None,
        attestation: JudgmentGuardAttestation | None = None,
    ) -> None:
        self._authority = authority
        self._request = request
        self._judgment = judgment
        self._attestation = attestation
        self._prepared = False

    def facts(self, request: TransitionRequest) -> tuple[TrustedGuardFact, ...]:
        return (
            (self._authority.fact(self._attestation),)
            if request == self._request and self._attestation is not None
            else ()
        )

    async def prepare(
        self, session: AsyncSession, request: TransitionRequest, current: WorkRun | None
    ) -> None:
        if self._judgment is None or self._attestation is None or current is None:
            return
        now = self._authority._clock().astimezone(UTC)
        row = await session.get(JudgmentRow, self._judgment.judgment_id)
        projection = await session.get(JudgmentProjectionRow, request.work_run_id)
        result_row = (
            await session.scalar(
                select(HumanResultRow).where(
                    HumanResultRow.serialized_ref == self._judgment.human_result_ref
                )
            )
            if self._judgment.human_result_ref
            else None
        )
        gate_projection = (
            await session.get(HumanGateProjectionRow, result_row.human_gate_id)
            if result_row is not None
            else None
        )
        gate_row = None
        if result_row is not None and gate_projection is not None:
            gate_row = await session.get(HumanGateRow, result_row.human_gate_id)
            if gate_row is None:
                raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
            await _verify_gate_consistency_in_session(session, gate_row, gate_projection)
        if projection is not None:
            await _verify_judgment_consistency_in_session(session, projection)
        evidence = (
            await self._authority._evidence_repository.load_effective_attestation_in_session(
                session, self._judgment.evidence_attestation_ref
            )
            if self._judgment.evidence_attestation_ref
            else None
        )
        policy_row = await session.get(
            JudgmentPolicyRow,
            f"p1-7-judgment-policy:{self._judgment.policy_version}:{self._judgment.policy_id}",
        )
        policy = (
            _policy_from_row(policy_row, self._authority._policy_authority._token)
            if policy_row is not None
            else None
        )
        policy_current = bool(
            policy is not None
            and await self._authority._policy_authority.current_in_session(session, policy, request)
            and policy.fingerprint == self._judgment.policy_fingerprint
            and policy.policy_authority_id == self._judgment.policy_authority_id
            and policy.policy_authority_version == self._judgment.policy_authority_version
            and policy.policy_authority_revision == self._judgment.policy_authority_revision
        )
        negative_evaluation = None
        if (
            policy is not None
            and self._judgment.evidence_basis_kind
            is JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION
            and self._judgment.evidence_evaluation_ref is not None
            and policy.evidence_checkpoint_ref is not None
            and policy.evidence_requirement_set_ref is not None
        ):
            try:
                negative_evaluation = (
                    await self._authority._evidence_repository
                    .load_current_set_evaluation_in_session(
                        session,
                        self._judgment.evidence_evaluation_ref,
                        work_run_id=request.work_run_id,
                        source_state=cast(WorkflowState, request.observed_state),
                        state_version=request.observed_state_version,
                        checkpoint_ref=policy.evidence_checkpoint_ref,
                        requirement_set_ref=policy.evidence_requirement_set_ref,
                        expected_outcome=EvidenceSetOutcome.UNSATISFIED,
                        now=now,
                    )
                )
            except ValueError:
                negative_evaluation = None
        command_center = (
            await self._authority._command_center_authority.current_in_session(
                session,
                self._judgment.command_center_action_ref,
                request,
                policy,
                now,
            )
            if self._authority._command_center_authority is not None and policy is not None
            else None
        )
        result = _result_from_row(result_row) if result_row is not None else None
        gate_expires_at = (
            _optional_datetime(gate_row.payload.get("expires_at")) if gate_row is not None else None
        )
        human_current = bool(
            self._judgment.owner_policy is not JudgmentOwnerPolicy.HUMAN
            or (
                result is not None
                and gate_row is not None
                and gate_projection is not None
                and gate_projection.current_result_ref == result.serialized_ref
                and gate_projection.status == HumanGateStatus.RESOLVED.value
                and gate_projection.authority_revision == result.gate_authority_revision + 1
                and result.human_gate_ref == gate_row.serialized_ref
                and result.task_contract_id == request.task_contract_id
                and result.task_contract_version == request.task_contract_version
                and result.work_run_id == request.work_run_id
                and result.source_state is request.observed_state
                and result.state_version == request.observed_state_version
                and request.human_result_refs == (result.serialized_ref,)
                and gate_row.task_contract_id == request.task_contract_id
                and gate_row.task_contract_version == request.task_contract_version
                and gate_row.work_run_id == request.work_run_id
                and gate_projection.bound_state
                == (request.observed_state.value if request.observed_state else None)
                and gate_projection.bound_state_version == request.observed_state_version
                and (gate_expires_at is None or now < gate_expires_at)
            )
        )
        valid = bool(
            row is not None
            and row.fingerprint == self._judgment.fingerprint
            and self._judgment.fingerprint == _judgment_fingerprint(self._judgment)
            and projection is not None
            and projection.judgment_id == self._judgment.judgment_id
            and projection.authority_revision == self._judgment.authority_revision
            and _request_matches_workrun(request, current)
            and self._judgment.target_use_fingerprint == _target_fingerprint(request)
            and self._judgment.task_contract_id == request.task_contract_id
            and self._judgment.task_contract_version == request.task_contract_version
            and self._judgment.work_run_id == request.work_run_id
            and self._judgment.source_state is request.observed_state
            and self._judgment.state_version == request.observed_state_version
            and self._judgment.target_state is request.target_state
            and request.judgment_refs == (self._judgment.serialized_ref,)
            and policy_current
            and policy is not None
            and policy.evidence_basis_kind is self._judgment.evidence_basis_kind
            and policy.evidence_checkpoint_ref == self._judgment.evidence_checkpoint_ref
            and policy.evidence_requirement_set_ref
            == self._judgment.evidence_requirement_set_ref
            and (
                self._judgment.evidence_basis_kind is None
                or request.evidence_refs
                == (
                    self._judgment.evidence_attestation_ref
                    or self._judgment.evidence_evaluation_ref,
                )
            )
            and human_current
            and (
                self._judgment.owner_policy is not JudgmentOwnerPolicy.COMMAND_CENTER
                or command_center is not None
            )
            and (
                self._judgment.evidence_attestation_ref is None
                or (
                    evidence is not None
                    and evidence.evidence_authority_revision
                    == self._judgment.evidence_authority_revision
                    and evidence.task_contract_id == request.task_contract_id
                    and evidence.task_contract_version == request.task_contract_version
                    and evidence.work_run_id == request.work_run_id
                    and evidence.source_state is request.observed_state
                    and evidence.state_version == request.observed_state_version
                    and evidence.target_state is request.target_state
                )
            )
            and (
                self._judgment.evidence_basis_kind
                is not JudgmentEvidenceBasisKind.SATISFIED_ATTESTATION
                or (
                    evidence is not None
                    and evidence.checkpoint_ref.serialized()
                    == self._judgment.evidence_checkpoint_ref
                    and f"{evidence.requirement_set_id}@{evidence.requirement_set_version}"
                    == self._judgment.evidence_requirement_set_ref
                )
            )
            and (
                self._judgment.evidence_basis_kind
                is not JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION
                or (
                    negative_evaluation is not None
                    and negative_evaluation.serialized_ref
                    == self._judgment.evidence_evaluation_ref
                    and negative_evaluation.evidence_authority_revision
                    == self._judgment.evidence_evaluation_authority_revision
                    and negative_evaluation.outcome is EvidenceSetOutcome.UNSATISFIED
                )
            )
            and self._attestation.policy_authority_id == self._judgment.policy_authority_id
            and self._attestation.policy_authority_version
            == self._judgment.policy_authority_version
            and self._attestation.policy_authority_revision
            == self._judgment.policy_authority_revision
            and (self._attestation.expires_at is None or now < self._attestation.expires_at)
        )
        if valid:
            self._prepared = True
            self._authority._active[request.transition_request_id] = (
                self._attestation.serialized_ref
            )

    def after_evaluation(self, request: TransitionRequest) -> None:
        self._authority._active.pop(request.transition_request_id, None)

    async def after_decision(
        self,
        session: AsyncSession,
        request: TransitionRequest,
        evaluation: TransitionEvaluation,
        decision: TransitionDecision,
        current: WorkRun | None,
    ) -> None:
        del request, evaluation, decision, current
        if self._attestation is None:
            return
        if not self._prepared:
            return
        existing = await session.get(JudgmentGuardAttestationRow, self._attestation.attestation_id)
        if existing is None:
            session.add(_guard_row(self._attestation))
        elif existing.fingerprint != self._attestation.fingerprint:
            raise JudgmentAuthorityError("AUTHORITY_CONFLICT")


def _judgment_kind(result: HumanResultKind | None) -> JudgmentKind:
    if result is HumanResultKind.APPROVE:
        return JudgmentKind.ACCEPTED
    if result is HumanResultKind.REJECT:
        return JudgmentKind.REJECTED
    if result is HumanResultKind.REWORK:
        return JudgmentKind.HOLD_REWORK_REQUIRED
    raise JudgmentAuthorityError("JUDGMENT_INPUT_INCOMPLETE")


def _guard_for_kind(kind: JudgmentKind) -> GuardId:
    return {
        JudgmentKind.ACCEPTED: GuardId.G_JUDGMENT_ACCEPTED,
        JudgmentKind.REJECTED: GuardId.G_JUDGMENT_REJECTED,
        JudgmentKind.HOLD_REWORK_REQUIRED: GuardId.G_JUDGMENT_REWORK,
    }[kind]


def _guard_for_target(target: WorkflowState) -> GuardId | None:
    return {
        WorkflowState.ACCEPTED: GuardId.G_JUDGMENT_ACCEPTED,
        WorkflowState.REJECTED: GuardId.G_JUDGMENT_REJECTED,
        WorkflowState.REWORK_REQUIRED: GuardId.G_JUDGMENT_REWORK,
    }.get(target)


def _request_matches_run(request: TransitionRequest, run: WorkRunRow) -> bool:
    return bool(
        run.task_contract_id == request.task_contract_id
        and run.task_contract_version == request.task_contract_version
        and run.workflow_state == (request.observed_state.value if request.observed_state else None)
        and run.state_version == request.observed_state_version
    )


def _request_matches_workrun(request: TransitionRequest, run: WorkRun) -> bool:
    return bool(
        run.task_contract_id == request.task_contract_id
        and run.task_contract_version == request.task_contract_version
        and run.state is request.observed_state
        and run.state_version == request.observed_state_version
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


def _judgment_proposal_fingerprint(
    *,
    judgment_version: str,
    request: TransitionRequest,
    policy: JudgmentPolicy,
    human_result_ref: str | None,
    evidence_attestation_ref: str | None,
    command_center_action_ref: str | None,
    reason_code: str,
    reason_vocabulary_version: str,
    supersedes_judgment_ref: str | None,
    evidence_basis_kind: JudgmentEvidenceBasisKind | None = None,
    evidence_evaluation_ref: str | None = None,
) -> str:
    payload: dict[str, object] = {
        "judgment_version": judgment_version,
        "request": [
            request.task_contract_id,
            request.task_contract_version,
            request.work_run_id,
            request.observed_state.value if request.observed_state else None,
            request.observed_state_version,
            request.target_state.value,
            _target_fingerprint(request),
        ],
        "policy": [
            policy.policy_id,
            policy.policy_version,
            policy.fingerprint,
            policy.policy_authority_id,
            policy.policy_authority_version,
            policy.policy_authority_revision,
        ],
        "inputs": [
            human_result_ref,
            evidence_attestation_ref,
            command_center_action_ref,
        ],
        "reason": [reason_code, reason_vocabulary_version],
        "supersedes": supersedes_judgment_ref,
    }
    if evidence_basis_kind is not None:
        payload["evidence_basis"] = [
            evidence_basis_kind.value,
            evidence_evaluation_ref,
        ]
    return canonical_hash(payload)


def _judgment_fingerprint(value: Judgment) -> str:
    payload = asdict(value)
    payload.pop("fingerprint")
    payload.pop("issued_at")
    payload["source_state"] = value.source_state.value
    payload["target_state"] = value.target_state.value
    payload["owner_policy"] = value.owner_policy.value
    payload["judgment_kind"] = value.judgment_kind.value
    if value.evidence_basis_kind is None:
        payload.pop("evidence_basis_kind")
        payload.pop("evidence_evaluation_ref")
        payload.pop("evidence_evaluation_authority_revision")
        payload.pop("evidence_checkpoint_ref")
        payload.pop("evidence_requirement_set_ref")
    else:
        payload["evidence_basis_kind"] = value.evidence_basis_kind.value
    return canonical_hash(payload)


def _judgment_row(value: Judgment, proposal_fingerprint: str) -> JudgmentRow:
    payload = asdict(value)
    payload["source_state"] = value.source_state.value
    payload["target_state"] = value.target_state.value
    payload["owner_policy"] = value.owner_policy.value
    payload["judgment_kind"] = value.judgment_kind.value
    if value.evidence_basis_kind is None:
        payload.pop("evidence_basis_kind")
        payload.pop("evidence_evaluation_ref")
        payload.pop("evidence_evaluation_authority_revision")
        payload.pop("evidence_checkpoint_ref")
        payload.pop("evidence_requirement_set_ref")
    else:
        payload["evidence_basis_kind"] = value.evidence_basis_kind.value
    payload["issued_at"] = value.issued_at.isoformat()
    payload["proposal_fingerprint"] = proposal_fingerprint
    return JudgmentRow(
        judgment_id=value.judgment_id,
        serialized_ref=value.serialized_ref,
        fingerprint=value.fingerprint,
        evaluation_id=value.evaluation_ref,
        work_run_id=value.work_run_id,
        state_version=value.state_version,
        judgment_kind=value.judgment_kind.value,
        authority_revision=value.authority_revision,
        payload=payload,
        issued_at=value.issued_at,
    )


def _judgment_from_row(row: JudgmentRow) -> Judgment:
    p = row.payload
    return Judgment(
        row.judgment_id,
        str(p["judgment_version"]),
        row.fingerprint,
        str(p["authority_id"]),
        str(p["authority_version"]),
        row.authority_revision,
        str(p["task_contract_id"]),
        str(p["task_contract_version"]),
        row.work_run_id,
        WorkflowState(str(p["source_state"])),
        row.state_version,
        WorkflowState(str(p["target_state"])),
        str(p["target_use_fingerprint"]),
        JudgmentOwnerPolicy(str(p["owner_policy"])),
        str(p["policy_id"]),
        str(p["policy_version"]),
        str(p["policy_fingerprint"]),
        str(p["policy_authority_id"]),
        str(p["policy_authority_version"]),
        cast(int, p["policy_authority_revision"]),
        cast(str | None, p.get("command_center_action_ref")),
        cast(str | None, p.get("human_gate_ref")),
        cast(str | None, p.get("human_result_ref")),
        cast(int | None, p.get("human_result_authority_revision")),
        cast(str | None, p.get("evidence_attestation_ref")),
        cast(int | None, p.get("evidence_authority_revision")),
        cast(str | None, p.get("evidence_root")),
        JudgmentKind(row.judgment_kind),
        str(p["reason_code"]),
        str(p["reason_vocabulary_version"]),
        row.evaluation_id,
        row.issued_at.astimezone(UTC),
        cast(str | None, p.get("supersedes_judgment_ref")),
        (
            JudgmentEvidenceBasisKind(str(p["evidence_basis_kind"]))
            if p.get("evidence_basis_kind") is not None
            else None
        ),
        cast(str | None, p.get("evidence_evaluation_ref")),
        cast(int | None, p.get("evidence_evaluation_authority_revision")),
        cast(str | None, p.get("evidence_checkpoint_ref")),
        cast(str | None, p.get("evidence_requirement_set_ref")),
    )


def _guard_fingerprint(value: JudgmentGuardAttestation) -> str:
    payload = asdict(value)
    payload.pop("fingerprint")
    payload["guard_id"] = value.guard_id.value
    payload["source_state"] = value.source_state.value
    payload["target_state"] = value.target_state.value
    payload["issued_at"] = value.issued_at.isoformat()
    payload["expires_at"] = value.expires_at.isoformat() if value.expires_at else None
    return canonical_hash(payload)


def _guard_row(value: JudgmentGuardAttestation) -> JudgmentGuardAttestationRow:
    payload = asdict(value)
    payload["guard_id"] = value.guard_id.value
    payload["source_state"] = value.source_state.value
    payload["target_state"] = value.target_state.value
    payload["issued_at"] = value.issued_at.isoformat()
    payload["expires_at"] = value.expires_at.isoformat() if value.expires_at else None
    return JudgmentGuardAttestationRow(
        attestation_id=value.attestation_id,
        serialized_ref=value.serialized_ref,
        fingerprint=value.fingerprint,
        guard_id=value.guard_id.value,
        work_run_id=value.work_run_id,
        state_version=value.state_version,
        authority_revision=value.judgment_authority_revision,
        payload=payload,
        issued_at=value.issued_at,
        expires_at=value.expires_at,
    )


async def _verify_judgment_base_issuance_provenance_in_session(
    session: AsyncSession,
    row: JudgmentRow,
) -> tuple[Judgment, JudgmentAuthorityEventRow | None]:
    """Verify one immutable Judgment issuance without traversing corrections."""
    try:
        value = _judgment_from_row(row)
    except (KeyError, TypeError, ValueError) as exc:
        raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE") from exc
    proposal_fingerprint = row.payload.get("proposal_fingerprint")
    if proposal_fingerprint is None:
        raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
    if not _is_lower_sha256(proposal_fingerprint):
        raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    if (
        row.judgment_id != value.judgment_id
        or row.serialized_ref != value.serialized_ref
        or row.fingerprint != value.fingerprint
        or row.evaluation_id != value.evaluation_ref
        or row.work_run_id != value.work_run_id
        or row.state_version != value.state_version
        or row.judgment_kind != value.judgment_kind.value
        or row.authority_revision != value.authority_revision
        or row.issued_at.astimezone(UTC) != value.issued_at
        or value.fingerprint != _judgment_fingerprint(value)
    ):
        raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    evaluation = await session.get(JudgmentEvaluationRow, value.evaluation_ref)
    if evaluation is None:
        raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
    expected_policy_input = [
        value.policy_id,
        value.policy_version,
        value.policy_fingerprint,
        value.policy_authority_revision,
    ]
    if (
        evaluation.work_run_id != value.work_run_id
        or evaluation.state_version != value.state_version
        or evaluation.payload.get("policy") != expected_policy_input
        or evaluation.payload.get("human_result_ref") != value.human_result_ref
        or evaluation.payload.get("evidence_attestation_ref") != value.evidence_attestation_ref
        or evaluation.payload.get("command_center_action_ref") != value.command_center_action_ref
        or evaluation.payload.get("evidence_basis_kind")
        != (
            value.evidence_basis_kind.value
            if value.evidence_basis_kind is not None
            else None
        )
        or evaluation.payload.get("evidence_evaluation_ref")
        != value.evidence_evaluation_ref
        or evaluation.payload.get("outcome") != "COMPLETE"
        or evaluation.evaluated_at.astimezone(UTC) != value.issued_at
    ):
        raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    events = tuple(
        await session.scalars(
            select(JudgmentAuthorityEventRow)
            .where(JudgmentAuthorityEventRow.judgment_id == row.judgment_id)
            .order_by(JudgmentAuthorityEventRow.event_sequence)
        )
    )
    issued_events = tuple(event for event in events if event.event_kind == "ISSUED")
    superseded_events = tuple(event for event in events if event.event_kind == "SUPERSEDED")
    if not issued_events:
        raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
    if len(issued_events) != 1 or len(superseded_events) > 1:
        raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    if any(event.event_kind not in {"ISSUED", "SUPERSEDED"} for event in events):
        raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    issued = issued_events[0]
    if (
        issued.prior_revision != value.authority_revision - 1
        or issued.new_revision != value.authority_revision
        or issued.payload.get("evaluation_ref") != value.evaluation_ref
        or issued.created_at.astimezone(UTC) != value.issued_at
    ):
        raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    policy_ref = f"p1-7-judgment-policy:{value.policy_version}:{value.policy_id}"
    policy_row = await session.get(JudgmentPolicyRow, policy_ref)
    if policy_row is None:
        raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
    try:
        policy = _policy_from_row(policy_row, object())
    except (KeyError, TypeError, ValueError) as exc:
        raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE") from exc
    if (
        policy_row.serialized_ref != policy.serialized_ref
        or policy_row.policy_scope_key
        != _policy_scope_key(
            value.task_contract_id,
            value.task_contract_version,
            value.source_state,
            value.target_state,
        )
        or policy_row.fingerprint != policy.fingerprint
        or policy_row.authority_revision != policy.policy_authority_revision
        or policy_row.issued_at.astimezone(UTC) != policy.issued_at
        or policy.fingerprint != _policy_fingerprint(policy)
        or policy.policy_id != value.policy_id
        or policy.policy_version != value.policy_version
        or policy.fingerprint != value.policy_fingerprint
        or policy.policy_authority_id != value.policy_authority_id
        or policy.policy_authority_version != value.policy_authority_version
        or policy.policy_authority_revision != value.policy_authority_revision
        or policy.task_contract_id != value.task_contract_id
        or policy.task_contract_version != value.task_contract_version
        or policy.source_state is not value.source_state
        or policy.target_state is not value.target_state
        or policy.target_use_fingerprint
        != _policy_use_fingerprint(
            value.task_contract_id,
            value.task_contract_version,
            value.source_state,
            value.target_state,
        )
        or policy.owner_policy is not value.owner_policy
        or policy.evidence_basis_kind is not value.evidence_basis_kind
        or policy.evidence_checkpoint_ref != value.evidence_checkpoint_ref
        or policy.evidence_requirement_set_ref != value.evidence_requirement_set_ref
    ):
        raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    if value.evidence_basis_kind is JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION:
        if (
            value.evidence_evaluation_ref is None
            or value.evidence_evaluation_authority_revision is None
            or value.evidence_attestation_ref is not None
            or value.evidence_authority_revision is not None
            or value.evidence_root is not None
        ):
            raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
        try:
            evaluation_value = await verify_historical_set_evaluation_provenance(
                session, value.evidence_evaluation_ref
            )
        except ValueError as exc:
            raise JudgmentAuthorityError("AUTHORITY_CONFLICT") from exc
        except HistoricalEvidenceProvenanceError as exc:
            reason = "PROVENANCE_INCOMPLETE" if exc.incomplete else "AUTHORITY_CONFLICT"
            raise JudgmentAuthorityError(reason) from exc
        if (
            evaluation_value.serialized_ref != value.evidence_evaluation_ref
            or evaluation_value.task_contract_id != value.task_contract_id
            or evaluation_value.task_contract_version != value.task_contract_version
            or evaluation_value.work_run_id != value.work_run_id
            or evaluation_value.source_state is not value.source_state
            or evaluation_value.state_version != value.state_version
            or evaluation_value.checkpoint_ref.serialized() != value.evidence_checkpoint_ref
            or f"{evaluation_value.requirement_set_id}@{evaluation_value.requirement_set_version}"
            != value.evidence_requirement_set_ref
            or evaluation_value.outcome is not EvidenceSetOutcome.UNSATISFIED
            or evaluation_value.evidence_authority_revision
            != value.evidence_evaluation_authority_revision
        ):
            raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    else:
        if value.evidence_evaluation_ref is not None or (
            value.evidence_evaluation_authority_revision is not None
        ):
            raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
        if value.evidence_attestation_ref is None:
            if value.evidence_authority_revision is not None or value.evidence_root is not None:
                raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
            if policy.requires_post_human_evidence:
                raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
        else:
            if value.evidence_authority_revision is None or value.evidence_root is None:
                raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
            try:
                evidence = await verify_historical_set_attestation_provenance(
                    session, value.evidence_attestation_ref
                )
            except HistoricalEvidenceProvenanceError as exc:
                reason = "PROVENANCE_INCOMPLETE" if exc.incomplete else "AUTHORITY_CONFLICT"
                raise JudgmentAuthorityError(reason) from exc
            if (
                evidence.serialized_ref != value.evidence_attestation_ref
                or evidence.task_contract_id != value.task_contract_id
                or evidence.task_contract_version != value.task_contract_version
                or evidence.work_run_id != value.work_run_id
                or evidence.source_state is not value.source_state
                or evidence.state_version != value.state_version
                or evidence.target_state is not value.target_state
                or evidence.evidence_authority_revision != value.evidence_authority_revision
                or evidence.admitted_ref_root_hash != value.evidence_root
                or (
                    value.evidence_basis_kind
                    is JudgmentEvidenceBasisKind.SATISFIED_ATTESTATION
                    and (
                        evidence.checkpoint_ref.serialized()
                        != value.evidence_checkpoint_ref
                        or f"{evidence.requirement_set_id}@{evidence.requirement_set_version}"
                        != value.evidence_requirement_set_ref
                    )
                )
            ):
                raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    if value.owner_policy is JudgmentOwnerPolicy.HUMAN:
        if (
            not policy.requires_human_result
            or value.human_result_ref is None
            or value.human_gate_ref is None
            or value.human_result_authority_revision is None
        ):
            raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
        result_row = await session.scalar(
            select(HumanResultRow).where(HumanResultRow.serialized_ref == value.human_result_ref)
        )
        if result_row is None:
            raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
        try:
            result = await _verify_human_result_historical_provenance_in_session(
                session, result_row
            )
        except HumanAuthorityError as exc:
            reason = (
                "PROVENANCE_INCOMPLETE"
                if exc.reason is HumanAuthorityReason.PROVENANCE_INCOMPLETE
                else "AUTHORITY_CONFLICT"
            )
            raise JudgmentAuthorityError(reason) from exc
        if (
            result.human_gate_ref != value.human_gate_ref
            or result.serialized_ref != value.human_result_ref
            or result.result_authority_revision != value.human_result_authority_revision
            or result.task_contract_id != value.task_contract_id
            or result.task_contract_version != value.task_contract_version
            or result.work_run_id != value.work_run_id
            or result.source_state is not value.source_state
            or result.state_version != value.state_version
            or _judgment_kind(result.result_kind) is not value.judgment_kind
        ):
            raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    elif (
        value.human_result_ref is not None
        or value.human_gate_ref is not None
        or value.human_result_authority_revision is not None
        or policy.requires_human_result
    ):
        raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    if value.owner_policy is JudgmentOwnerPolicy.COMMAND_CENTER:
        if value.command_center_action_ref is None:
            raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
        action_row = await session.get(
            CommandCenterJudgmentActionRow, value.command_center_action_ref
        )
        if action_row is None:
            raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
        try:
            action = _command_center_from_row(action_row, object())
        except (KeyError, TypeError, ValueError) as exc:
            raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE") from exc
        if (
            action_row.serialized_ref != action.serialized_ref
            or action_row.fingerprint != action.fingerprint
            or action_row.work_run_id != action.work_run_id
            or action_row.issued_at.astimezone(UTC) != action.issued_at
            or action_row.expires_at.astimezone(UTC) != action.expires_at
            or action.fingerprint != _command_center_fingerprint(action)
            or action.task_contract_id != value.task_contract_id
            or action.task_contract_version != value.task_contract_version
            or action.work_run_id != value.work_run_id
            or action.source_state is not value.source_state
            or action.state_version != value.state_version
            or action.target_state is not value.target_state
            or action.target_use_fingerprint != value.target_use_fingerprint
            or action.judgment_kind is not value.judgment_kind
            or action.policy_ref != policy.serialized_ref
            or action.policy_fingerprint != value.policy_fingerprint
            or action.policy_authority_revision != value.policy_authority_revision
        ):
            raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    elif value.command_center_action_ref is not None:
        raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    if value.owner_policy is JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC and (
        policy.deterministic_kind is not value.judgment_kind
    ):
        raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    if superseded_events and (
        superseded_events[0].event_sequence <= issued.event_sequence
        or superseded_events[0].created_at.astimezone(UTC) < value.issued_at
    ):
        raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    return value, superseded_events[0] if superseded_events else None


async def _verify_judgment_historical_provenance_in_session(
    session: AsyncSession,
    row: JudgmentRow,
) -> Judgment:
    """Verify a complete immutable Judgment correction graph without current projections."""
    cache: dict[str, tuple[Judgment, JudgmentAuthorityEventRow | None]] = {}

    async def load_ref(
        serialized_ref: str,
    ) -> tuple[Judgment, JudgmentAuthorityEventRow | None]:
        cached = cache.get(serialized_ref)
        if cached is not None:
            return cached
        candidate = await session.scalar(
            select(JudgmentRow).where(JudgmentRow.serialized_ref == serialized_ref)
        )
        if candidate is None:
            raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
        verified = await _verify_judgment_base_issuance_provenance_in_session(session, candidate)
        cache[serialized_ref] = verified
        return verified

    start = await _verify_judgment_base_issuance_provenance_in_session(session, row)
    cache[start[0].serialized_ref] = start

    predecessor_seen: set[str] = set()
    current, _ = start
    while True:
        if current.serialized_ref in predecessor_seen:
            raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
        predecessor_seen.add(current.serialized_ref)
        predecessor_ref = current.supersedes_judgment_ref
        if predecessor_ref is None:
            root = current
            break
        if predecessor_ref in predecessor_seen:
            raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
        predecessor, relation = await load_ref(predecessor_ref)
        if relation is None:
            raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
        _verify_judgment_correction_edge(predecessor, current, relation)
        current = predecessor

    forward_seen: set[str] = set()
    current = root
    while True:
        if current.serialized_ref in forward_seen:
            raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
        forward_seen.add(current.serialized_ref)
        _, relation = await load_ref(current.serialized_ref)
        if relation is None:
            break
        replacement_ref = relation.payload.get("replacement_judgment_ref")
        if not isinstance(replacement_ref, str) or not replacement_ref:
            raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
        if replacement_ref in forward_seen:
            raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
        replacement, _ = await load_ref(replacement_ref)
        _verify_judgment_correction_edge(current, replacement, relation)
        current = replacement
    if start[0].serialized_ref not in forward_seen:
        raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    return start[0]


async def verify_historical_judgment_provenance(
    session: AsyncSession, serialized_ref: str
) -> Judgment:
    """Projection-independent P1-7 read boundary for dependent authorities."""
    row = await session.scalar(
        select(JudgmentRow).where(JudgmentRow.serialized_ref == serialized_ref)
    )
    if row is None:
        raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
    return await _verify_judgment_historical_provenance_in_session(session, row)


def _verify_judgment_correction_edge(
    predecessor: Judgment,
    replacement: Judgment,
    relation: JudgmentAuthorityEventRow,
) -> None:
    if (
        relation.event_kind != "SUPERSEDED"
        or predecessor.serialized_ref == replacement.serialized_ref
        or replacement.supersedes_judgment_ref != predecessor.serialized_ref
        or predecessor.work_run_id != replacement.work_run_id
        or predecessor.task_contract_id != replacement.task_contract_id
        or predecessor.task_contract_version != replacement.task_contract_version
        or predecessor.source_state is not replacement.source_state
        or predecessor.state_version != replacement.state_version
        or predecessor.target_state is not replacement.target_state
        or predecessor.authority_revision + 1 != replacement.authority_revision
        or relation.prior_revision != predecessor.authority_revision
        or relation.new_revision != replacement.authority_revision
        or relation.payload.get("replacement_judgment_ref") != replacement.serialized_ref
        or relation.created_at.astimezone(UTC) != replacement.issued_at
    ):
        raise JudgmentAuthorityError("AUTHORITY_CONFLICT")


async def _verify_judgment_consistency_in_session(
    session: AsyncSession, projection: JudgmentProjectionRow
) -> Judgment:
    row = await session.get(JudgmentRow, projection.judgment_id)
    if row is None:
        raise JudgmentAuthorityError("PROVENANCE_INCOMPLETE")
    value = await _verify_judgment_historical_provenance_in_session(session, row)
    issued = tuple(
        await session.scalars(
            select(JudgmentAuthorityEventRow).where(
                JudgmentAuthorityEventRow.judgment_id == row.judgment_id,
                JudgmentAuthorityEventRow.event_kind == "ISSUED",
            )
        )
    )
    superseded = tuple(
        await session.scalars(
            select(JudgmentAuthorityEventRow).where(
                JudgmentAuthorityEventRow.judgment_id == row.judgment_id,
                JudgmentAuthorityEventRow.event_kind == "SUPERSEDED",
            )
        )
    )
    if (
        len(issued) != 1
        or superseded
        or value.work_run_id != projection.work_run_id
        or projection.authority_revision != value.authority_revision
        or projection.latest_event_sequence != issued[0].event_sequence
    ):
        raise JudgmentAuthorityError("AUTHORITY_CONFLICT")
    return value


def _is_lower_sha256(value: object) -> bool:
    return bool(
        isinstance(value, str)
        and len(value) == 64
        and value == value.lower()
        and all(character in "0123456789abcdef" for character in value)
    )


def _policy_scope_key(
    task_contract_id: str,
    task_contract_version: str,
    source_state: WorkflowState,
    target_state: WorkflowState,
) -> str:
    return canonical_hash(
        [task_contract_id, task_contract_version, source_state.value, target_state.value]
    )


def _policy_use_fingerprint(
    task_contract_id: str,
    task_contract_version: str,
    source_state: WorkflowState,
    target_state: WorkflowState,
) -> str:
    return canonical_hash(
        {
            "task_contract": [task_contract_id, task_contract_version],
            "source_state": source_state.value,
            "target_state": target_state.value,
            "purpose": "P1_7_JUDGMENT_TRANSITION_USE_V1",
        }
    )


def _policy_use_for_request(request: TransitionRequest) -> str:
    return _policy_use_fingerprint(
        request.task_contract_id,
        request.task_contract_version,
        cast(WorkflowState, request.observed_state),
        request.target_state,
    )


def _policy_fingerprint(value: JudgmentPolicy) -> str:
    payload: dict[str, object] = {
        "policy": [value.policy_id, value.policy_version],
        "task": [value.task_contract_id, value.task_contract_version],
        "use": [
            value.source_state.value,
            value.target_state.value,
            value.target_use_fingerprint,
        ],
        "owner": value.owner_policy.value,
        "human": value.requires_human_result,
        "evidence": value.requires_post_human_evidence,
        "deterministic_kind": (
            value.deterministic_kind.value if value.deterministic_kind is not None else None
        ),
        "authority": [
            value.policy_authority_id,
            value.policy_authority_version,
            value.policy_authority_revision,
        ],
    }
    if value.evidence_basis_kind is not None:
        payload["evidence_basis"] = [
            value.evidence_basis_kind.value,
            value.evidence_checkpoint_ref,
            value.evidence_requirement_set_ref,
        ]
    return canonical_hash(payload)


def _policy_row(value: JudgmentPolicy, scope_key: str) -> JudgmentPolicyRow:
    payload = asdict(value)
    payload.pop("_issuer_token", None)
    payload["source_state"] = value.source_state.value
    payload["target_state"] = value.target_state.value
    payload["owner_policy"] = value.owner_policy.value
    payload["deterministic_kind"] = (
        value.deterministic_kind.value if value.deterministic_kind is not None else None
    )
    if value.evidence_basis_kind is None:
        payload.pop("evidence_basis_kind")
        payload.pop("evidence_checkpoint_ref")
        payload.pop("evidence_requirement_set_ref")
    else:
        payload["evidence_basis_kind"] = value.evidence_basis_kind.value
    payload["issued_at"] = value.issued_at.isoformat()
    return JudgmentPolicyRow(
        serialized_ref=value.serialized_ref,
        policy_scope_key=scope_key,
        fingerprint=value.fingerprint,
        authority_revision=value.policy_authority_revision,
        payload=payload,
        issued_at=value.issued_at,
    )


def _policy_from_row(row: JudgmentPolicyRow, token: object) -> JudgmentPolicy:
    p = row.payload
    deterministic = p.get("deterministic_kind")
    evidence_basis = p.get("evidence_basis_kind")
    return JudgmentPolicy(
        str(p["policy_id"]),
        str(p["policy_version"]),
        row.fingerprint,
        str(p["task_contract_id"]),
        str(p["task_contract_version"]),
        WorkflowState(str(p["source_state"])),
        WorkflowState(str(p["target_state"])),
        str(p["target_use_fingerprint"]),
        JudgmentOwnerPolicy(str(p["owner_policy"])),
        cast(bool, p["requires_human_result"]),
        cast(bool, p["requires_post_human_evidence"]),
        JudgmentKind(str(deterministic)) if deterministic is not None else None,
        str(p["policy_authority_id"]),
        str(p["policy_authority_version"]),
        row.authority_revision,
        row.issued_at.astimezone(UTC),
        token,
        (
            JudgmentEvidenceBasisKind(str(evidence_basis))
            if evidence_basis is not None
            else None
        ),
        cast(str | None, p.get("evidence_checkpoint_ref")),
        cast(str | None, p.get("evidence_requirement_set_ref")),
    )


def _command_center_fingerprint(value: CommandCenterActionAuthority) -> str:
    payload = asdict(value)
    payload.pop("fingerprint")
    payload.pop("_issuer_token", None)
    payload["source_state"] = value.source_state.value
    payload["target_state"] = value.target_state.value
    payload["judgment_kind"] = value.judgment_kind.value
    payload["issued_at"] = value.issued_at.isoformat()
    payload["expires_at"] = value.expires_at.isoformat()
    return canonical_hash(payload)


def _command_center_row(
    value: CommandCenterActionAuthority,
) -> CommandCenterJudgmentActionRow:
    payload = asdict(value)
    payload.pop("_issuer_token", None)
    payload["source_state"] = value.source_state.value
    payload["target_state"] = value.target_state.value
    payload["judgment_kind"] = value.judgment_kind.value
    payload["issued_at"] = value.issued_at.isoformat()
    payload["expires_at"] = value.expires_at.isoformat()
    return CommandCenterJudgmentActionRow(
        serialized_ref=value.serialized_ref,
        fingerprint=value.fingerprint,
        work_run_id=value.work_run_id,
        payload=payload,
        issued_at=value.issued_at,
        expires_at=value.expires_at,
    )


def _command_center_from_row(
    row: CommandCenterJudgmentActionRow, token: object
) -> CommandCenterActionAuthority:
    p = row.payload
    return CommandCenterActionAuthority(
        str(p["action_id"]),
        str(p["action_version"]),
        row.fingerprint,
        str(p["principal_id"]),
        str(p["task_contract_id"]),
        str(p["task_contract_version"]),
        row.work_run_id,
        WorkflowState(str(p["source_state"])),
        cast(int, p["state_version"]),
        WorkflowState(str(p["target_state"])),
        str(p["target_use_fingerprint"]),
        str(p["policy_ref"]),
        str(p["policy_fingerprint"]),
        cast(int, p["policy_authority_revision"]),
        JudgmentKind(str(p["judgment_kind"])),
        row.issued_at.astimezone(UTC),
        row.expires_at.astimezone(UTC),
        str(p["authority_id"]),
        str(p["authority_version"]),
        token,
    )


def _optional_datetime(value: object) -> datetime | None:
    return datetime.fromisoformat(value) if isinstance(value, str) else None
