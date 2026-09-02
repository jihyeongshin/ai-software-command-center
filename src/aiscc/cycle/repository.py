from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.contracts.workflow import WorkflowState
from aiscc.cycle.models import (
    AdmittedCycle,
    CycleAdmissionDecision,
    CycleAdmissionError,
    CycleAdmissionErrorCode,
    CycleAdmissionRequest,
    CycleEvaluation,
    MemoryCategory,
    p1_8_task_binding_fingerprint,
)
from aiscc.evidence.models import (
    DurableContentError,
    EvidenceSensitivity,
    HistoricalContentAccessGrant,
    canonical_hash,
)
from aiscc.evidence.repository import (
    PostgresEvidenceRepository,
    verify_historical_set_attestation_provenance,
)
from aiscc.judgment.authority import verify_historical_judgment_provenance
from aiscc.memory.models import (
    DerivedMemoryDeclaration,
    MemoryApplicabilityState,
    MemoryAuthorityMode,
    MemoryDeclarationAuthorityPolicy,
    MemoryPolicyOwnerEvent,
    P1_8MemoryDeclarationPolicyAuthority,
    PrivacyClassification,
    ProjectMemoryError,
    ProjectMemoryErrorCode,
    VerifiedMemorySource,
    default_memory_policy_authority,
    derive_memory_declaration,
    memory_content_fingerprint,
    memory_lineage_key,
    project_memory_entry_id,
)
from aiscc.persistence.models import (
    AdmittedCycleRow,
    CycleAdmissionDecisionRow,
    CycleAdmissionRequestRow,
    CycleAuthorityEventRow,
    CycleEvaluationRow,
    CycleMemoryReferenceRow,
    EvidenceAuthorityEventRow,
    MemoryDeclarationPolicyRow,
    MemoryPolicyAuthorityEventRow,
    ProjectMemoryAuthorityEventRow,
    ProjectMemoryEntryRow,
    ProjectMemoryViewRow,
    WorkRunRow,
)
from aiscc.persistence.repository import verify_historical_transition_provenance
from aiscc.task_authority.models import (
    ExternalTaskAuthorityError,
    ExternalTaskAuthorityErrorCode,
    NextActionContextRefV1,
    TaskConstraintScopeKind,
)
from aiscc.task_authority.ports import ExternalTaskAuthorityVerifierPort
from aiscc.workflow.models import DecisionOutcome


class PostgresCycleAdmissionRepository:
    """P1-8 owner; consumes predecessor history and never mints predecessor authority."""

    authority_id = "AISCC_P1_8_CYCLE_ADMISSION_AUTHORITY_V1"
    authority_version = "AISCC-P1-8-CYCLE-ADMISSION-AUTHORITY-V1"

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        evidence_repository: PostgresEvidenceRepository,
        *,
        historical_content_access_grant: HistoricalContentAccessGrant,
        memory_policy: MemoryDeclarationAuthorityPolicy,
        memory_policy_authority: P1_8MemoryDeclarationPolicyAuthority,
        task_authority_verifier: ExternalTaskAuthorityVerifierPort,
    ) -> None:
        self._session_factory = session_factory
        self._evidence_repository = evidence_repository
        # Opaque capability is injected by bootstrap. This class exposes no mint/write path.
        self._historical_content_access_grant = historical_content_access_grant
        self._memory_policy = memory_policy
        self._memory_policy_authority = memory_policy_authority
        self._task_authority_verifier = task_authority_verifier
        if (
            memory_policy_authority is not default_memory_policy_authority()
            or not memory_policy_authority.recognizes(memory_policy)
        ):
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.MEMORY_POLICY_AUTHORITY_DENIED,
                "memory policy was not issued by the bootstrap-bound P1-8 authority",
            )

    async def enroll_memory_policy(self) -> None:
        policy = self._memory_policy
        if not self._memory_policy_authority.recognizes(policy):
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.MEMORY_POLICY_AUTHORITY_DENIED,
                "rogue memory policy authority",
            )
        payload = _memory_policy_payload(policy)
        async with self._session_factory() as session, session.begin():
            await _advisory_locks(session, (f"p1-8-memory-policy:{policy.serialized_ref}",))
            existing = await session.get(MemoryDeclarationPolicyRow, policy.serialized_ref)
            if existing is not None:
                if existing.fingerprint != policy.fingerprint or existing.payload != payload:
                    raise CycleAdmissionError(
                        CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                        "memory policy immutable identity conflicts",
                    )
                return
            session.add(
                MemoryDeclarationPolicyRow(
                    serialized_ref=policy.serialized_ref,
                    fingerprint=policy.fingerprint,
                    authority_revision=policy.authority_revision,
                    payload=payload,
                    issued_at=policy.issued_at,
                )
            )
            session.add(
                MemoryPolicyAuthorityEventRow(
                    event_id="memory-policy-issued-" + policy.fingerprint,
                    policy_ref=policy.serialized_ref,
                    event_kind="ISSUED",
                    replacement_ref="NONE",
                    payload={
                        "fingerprint": policy.fingerprint,
                        "authority_id": policy.authority_id,
                        "authority_version": policy.authority_version,
                        "authority_revision": policy.authority_revision,
                        "disposition": policy.revocation_disposition.value,
                    },
                    created_at=policy.issued_at,
                )
            )

    async def admit(self, request: CycleAdmissionRequest) -> AdmittedCycle:
        derived: list[DerivedMemoryDeclaration] = []
        candidate = request.candidate
        attested = await self._resolve_structured_declarations(request)
        await self._verify_task_constraint(request)
        context_current = await self._verify_external_contexts(request, attested)

        async with self._session_factory() as session, session.begin():
            run = await session.scalar(
                select(WorkRunRow)
                .where(WorkRunRow.work_run_id == candidate.work_run_id)
                .with_for_update()
            )
            if run is None:
                raise CycleAdmissionError(
                    CycleAdmissionErrorCode.FOREIGN_AUTHORITY, "WorkRun absent"
                )
            await _advisory_locks(
                session,
                tuple(
                    sorted(
                        {
                            f"p1-8-cycle-request:{request.request_id}",
                            f"p1-8-cycle:{candidate.cycle_id}",
                        }
                    )
                ),
            )
            await _advisory_locks(
                session,
                (f"p1-8-memory-policy:{self._memory_policy.serialized_ref}",),
            )
            await _advisory_locks(
                session,
                (
                    f"p1-8-terminal:{candidate.work_run_id}:{candidate.terminal_state_version}",
                    f"p1-8-memory-project:{candidate.project_id}",
                ),
            )
            source_refs = tuple(
                sorted(
                    {
                        item.source_evidence_ref
                        for item in candidate.memory_declarations
                        if item.source_evidence_ref is not None
                    }
                )
            )
            await _advisory_locks(
                session, tuple(f"evidence-authority-event:{ref}" for ref in source_refs)
            )
            lineage_keys = tuple(
                sorted(
                    memory_lineage_key(
                        project_id=candidate.project_id,
                        category=item.category,
                        subject_key=item.subject_key,
                        applicability_key=item.applicability_key,
                        semantic_slot=item.semantic_slot,
                    )
                    for item in candidate.memory_declarations
                )
            )
            await _advisory_locks(
                session, tuple(f"p1-8-memory-lineage:{key}" for key in lineage_keys)
            )
            existing = await session.get(AdmittedCycleRow, candidate.cycle_id)
            if existing is not None:
                if existing.cycle_fingerprint != candidate.fingerprint:
                    raise CycleAdmissionError(
                        CycleAdmissionErrorCode.IDENTITY_CONFLICT,
                        "Cycle ID already binds another candidate",
                    )
                return await self._verify_cycle_in_session(session, existing)
            existing_epoch = await session.scalar(
                select(AdmittedCycleRow).where(
                    AdmittedCycleRow.terminal_epoch_key == candidate.terminal_epoch_key
                )
            )
            if existing_epoch is not None:
                if (
                    existing_epoch.terminal_epoch_payload_fingerprint
                    != candidate.terminal_epoch_payload_fingerprint
                ):
                    raise CycleAdmissionError(
                        CycleAdmissionErrorCode.TERMINAL_EPOCH_CONFLICT,
                        "terminal epoch already binds a different immutable admitted payload",
                    )
                return await self._verify_cycle_in_session(session, existing_epoch)
            existing_request = await session.get(CycleAdmissionRequestRow, request.request_id)
            if existing_request is not None:
                raise CycleAdmissionError(
                    CycleAdmissionErrorCode.IDENTITY_CONFLICT,
                    "request ID already binds another admission",
                )
            await self._verify_current_policy(session)
            transition = await verify_historical_transition_provenance(
                session, candidate.transition_request_id
            )
            judgment = await verify_historical_judgment_provenance(session, candidate.judgment_ref)
            attestation = await verify_historical_set_attestation_provenance(
                session, candidate.evidence_attestation_ref
            )
            terminal_at = transition.decision.decided_at.astimezone(UTC)
            self._verify_terminal_bindings(request, transition, judgment, attestation)
            for ordinal, declaration in enumerate(candidate.memory_declarations, 1):
                try:
                    source = _verified_memory_source(
                        candidate,
                        declaration,
                        attested.get(ordinal),
                        transition,
                        judgment,
                        attestation,
                        self._memory_policy,
                    )
                    derived.append(
                        derive_memory_declaration(
                            declaration,
                            self._memory_policy,
                            source=source,
                        )
                    )
                except ProjectMemoryError as exc:
                    raise CycleAdmissionError(
                        CycleAdmissionErrorCode.MEMORY_DECLARATION_SOURCE_MISMATCH,
                        str(exc),
                    ) from exc
            if await _invalid_at(session, candidate.evidence_attestation_ref, terminal_at):
                raise CycleAdmissionError(
                    CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                    "terminal evidence authority was invalid at the consumed epoch",
                )
            source_current: dict[str, bool] = {}
            for declaration in candidate.memory_declarations:
                if declaration.source_evidence_ref:
                    if await _invalid_at(session, declaration.source_evidence_ref, terminal_at):
                        raise CycleAdmissionError(
                            CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                            "structured source was invalid at terminal epoch",
                        )
                    source_current[declaration.source_evidence_ref] = not await _invalid_at(
                        session, declaration.source_evidence_ref, datetime.max.replace(tzinfo=UTC)
                    )
            source_high_watermark = int(
                await session.scalar(
                    select(func.coalesce(func.max(EvidenceAuthorityEventRow.event_sequence), 0))
                )
                or 0
            )
            policy_high_watermark = int(
                await session.scalar(
                    select(func.coalesce(func.max(MemoryPolicyAuthorityEventRow.event_sequence), 0))
                )
                or 0
            )
            now = datetime.now(UTC)
            evaluation = CycleEvaluation(
                "cycle-evaluation-" + request.fingerprint,
                request.request_id,
                request.fingerprint,
                canonical_hash(
                    {
                        "attestation_ref": attestation.serialized_ref,
                        "evidence_root": attestation.admitted_ref_root_hash,
                        "judgment_ref": judgment.serialized_ref,
                        "transition_decision_id": transition.decision.transition_decision_id,
                    }
                ),
                tuple(item.policy_fingerprint for item in candidate.memory_declarations),
                tuple(item.content_fingerprint for item in derived),
                "ACCEPTED",
                now,
            )
            decision = CycleAdmissionDecision(
                "cycle-decision-" + evaluation.fingerprint,
                evaluation.evaluation_id,
                evaluation.fingerprint,
                "ADMITTED",
                "EXACT_ACCEPTED_TERMINAL_LINEAGE",
                self.authority_id,
                self.authority_version,
                now,
            )
            session.add(_request_row(request))
            await session.flush()
            session.add(_evaluation_row(evaluation))
            await session.flush()
            session.add(_decision_row(decision, request.request_id))
            await session.flush()
            cycle_row = AdmittedCycleRow(
                cycle_id=candidate.cycle_id,
                cycle_version=candidate.cycle_version,
                serialized_ref=f"p1-8-cycle:{candidate.cycle_version}:{candidate.cycle_id}",
                cycle_fingerprint=candidate.fingerprint,
                request_id=request.request_id,
                decision_id=decision.decision_id,
                project_id=candidate.project_id,
                work_run_id=candidate.work_run_id,
                terminal_state_version=candidate.terminal_state_version,
                terminal_epoch_key=candidate.terminal_epoch_key,
                terminal_epoch_payload_fingerprint=candidate.terminal_epoch_payload_fingerprint,
                source_owner_event_high_watermark=source_high_watermark,
                memory_policy_event_high_watermark=policy_high_watermark,
                task_constraint_ref=candidate.task_constraint_ref,
                task_constraint_fingerprint=candidate.task_constraint_fingerprint,
                task_constraint_snapshot_ref=candidate.task_constraint_snapshot_ref,
                task_constraint_snapshot_fingerprint=(
                    candidate.task_constraint_snapshot_fingerprint
                ),
                task_constraint_event_high_watermark=(
                    candidate.task_constraint_event_high_watermark
                ),
                payload=_cycle_payload(candidate),
                admitted_at=now,
            )
            session.add(cycle_row)
            await session.flush()
            session.add(
                CycleAuthorityEventRow(
                    event_id="cycle-admitted-" + candidate.fingerprint,
                    cycle_id=candidate.cycle_id,
                    event_kind="ADMITTED",
                    payload={"decision_id": decision.decision_id},
                    created_at=now,
                )
            )
            await self._persist_memory(
                session,
                request,
                cycle_row,
                derived,
                source_current,
                source_high_watermark,
                policy_high_watermark,
                context_current,
                now,
            )
            return _cycle_from_row(cycle_row)

    async def apply_memory_policy_event(self, event: MemoryPolicyOwnerEvent) -> None:
        if not self._memory_policy_authority.recognizes_event(event):
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.MEMORY_POLICY_AUTHORITY_DENIED,
                "foreign memory policy event authority",
            )
        async with self._session_factory() as session, session.begin():
            await _advisory_locks(session, (f"p1-8-memory-policy:{event.policy_ref}",))
            await self._verify_current_policy(session)
            session.add(
                MemoryPolicyAuthorityEventRow(
                    event_id=event.event_id,
                    policy_ref=event.policy_ref,
                    event_kind=event.event_kind,
                    replacement_ref=event.replacement_ref,
                    payload={"disposition": event.disposition.value},
                    created_at=event.created_at,
                )
            )
            if event.disposition.value != "WITHDRAW_CURRENT":
                return
            entries = tuple(
                await session.scalars(
                    select(ProjectMemoryEntryRow).where(
                        ProjectMemoryEntryRow.policy_ref == event.policy_ref
                    )
                )
            )
            for entry in entries:
                view = await session.get(
                    ProjectMemoryViewRow, entry.memory_lineage_key, with_for_update=True
                )
                if view is None or view.current_entry_id != entry.entry_id:
                    continue
                current_event = ProjectMemoryAuthorityEventRow(
                    event_id="memory-policy-withdraw-"
                    + canonical_hash([event.event_id, entry.entry_id]),
                    memory_lineage_key=entry.memory_lineage_key,
                    subject_entry_id=entry.entry_id,
                    replacement_entry_id="NONE",
                    event_kind=MemoryApplicabilityState.REVOKED.value,
                    prior_revision=view.authority_revision,
                    new_revision=view.authority_revision + 1,
                    authority_ref=event.event_id,
                    reason="MEMORY_POLICY_CURRENT_WITHDRAWN",
                    payload={"policy_event_id": event.event_id},
                    created_at=event.created_at,
                )
                session.add(current_event)
                await session.flush()
                view.current_entry_id = None
                view.state = MemoryApplicabilityState.REVOKED.value
                view.reason = current_event.reason
                view.authority_revision = current_event.new_revision
                view.latest_event_sequence = current_event.event_sequence
                view.updated_at = event.created_at

    async def replay(self, cycle_id: str) -> AdmittedCycle:
        async with self._session_factory() as session:
            row = await session.get(AdmittedCycleRow, cycle_id)
            if row is None:
                raise CycleAdmissionError(CycleAdmissionErrorCode.FOREIGN_AUTHORITY, "Cycle absent")
            return await self._verify_cycle_in_session(session, row)

    async def _verify_task_constraint(self, request: CycleAdmissionRequest) -> None:
        candidate = request.candidate
        try:
            folded = await self._task_authority_verifier.verify_task_constraint(
                constraint_ref=candidate.task_constraint_ref,
                constraint_fingerprint=candidate.task_constraint_fingerprint,
                snapshot_ref=candidate.task_constraint_snapshot_ref,
                snapshot_fingerprint=candidate.task_constraint_snapshot_fingerprint,
                owner_event_high_watermark=candidate.task_constraint_event_high_watermark,
                require_current=True,
            )
        except (ExternalTaskAuthorityError, ValueError) as exc:
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.TASK_BINDING_MISMATCH,
                "external TaskConstraint authority graph is not current and valid",
            ) from exc
        constraint = folded.current
        if constraint is None:
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.TASK_BINDING_MISMATCH,
                "TaskConstraint fold has no current ref",
            )
        scope = constraint.scope
        if (
            scope.project_id != candidate.project_id
            or scope.scope_kind
            not in {TaskConstraintScopeKind.TASK_CONTRACT, TaskConstraintScopeKind.WORK_RUN}
            or scope.task_contract_id != candidate.task_contract_id
            or scope.task_contract_version != candidate.task_contract_version
            or (
                scope.scope_kind is TaskConstraintScopeKind.WORK_RUN
                and scope.work_run_id != candidate.work_run_id
            )
        ):
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.TASK_BINDING_MISMATCH,
                "TaskConstraint scope differs from the Cycle lineage",
            )

    async def _verify_external_contexts(
        self,
        request: CycleAdmissionRequest,
        attested: dict[int, Any],
    ) -> dict[int, bool]:
        result: dict[int, bool] = {}
        for ordinal, declaration in enumerate(request.candidate.memory_declarations, 1):
            if declaration.category is not MemoryCategory.NEXT_ACTION_CONTEXT:
                continue
            structured = attested.get(ordinal)
            if structured is None:
                raise CycleAdmissionError(
                    CycleAdmissionErrorCode.MEMORY_DECLARATION_SOURCE_MISMATCH,
                    "NEXT_ACTION_CONTEXT durable structured source is absent",
                )
            _, body = structured
            try:
                raw = body["next_action_context"]
            except (KeyError, TypeError) as exc:
                raise CycleAdmissionError(
                    CycleAdmissionErrorCode.MEMORY_DECLARATION_SOURCE_MISMATCH,
                    "NEXT_ACTION_CONTEXT result shape differs",
                ) from exc
            context = await self._verify_context_declaration(declaration, raw)
            latest = await self._task_authority_verifier.latest_snapshot()
            try:
                await self._task_authority_verifier.verify_next_action_context(
                    context_ref=context.context_ref,
                    context_fingerprint=context.fingerprint,
                    introduction_event_ref=str(declaration.external_context_introduction_event_ref),
                    introduction_event_fingerprint=str(
                        declaration.external_context_introduction_event_fingerprint
                    ),
                    snapshot_ref=latest.snapshot_ref,
                    snapshot_fingerprint=latest.snapshot_fingerprint,
                    owner_event_high_watermark=latest.owner_event_high_watermark,
                    require_current=True,
                )
                result[ordinal] = True
            except ExternalTaskAuthorityError as exc:
                if exc.code is not ExternalTaskAuthorityErrorCode.NOT_CURRENT:
                    raise CycleAdmissionError(
                        CycleAdmissionErrorCode.MEMORY_DECLARATION_SOURCE_MISMATCH,
                        "external context latest graph differs",
                    ) from exc
                result[ordinal] = False
        return result

    async def _verify_context_declaration(
        self, declaration: Any, raw: Any
    ) -> NextActionContextRefV1:
        exact = {
            "result_schema_id",
            "result_schema_version",
            "context_ref",
            "context_fingerprint",
            "context_logical_id",
            "context_introduction_event_ref",
            "context_introduction_event_fingerprint",
            "context_authority_event_high_watermark",
            "project_id",
            "task_contract_id",
            "task_contract_version",
            "context_slot_id",
            "priority_class",
            "critical_path_ordinal",
        }
        if not isinstance(raw, dict) or set(raw) != exact:
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.MEMORY_DECLARATION_SOURCE_MISMATCH,
                "NEXT_ACTION_CONTEXT exact result fields differ",
            )
        if (
            raw["result_schema_id"] != "P1_8_NEXT_ACTION_CONTEXT_RESULT_V1"
            or raw["result_schema_version"] != "v1"
            or raw["context_ref"] != declaration.external_context_ref
            or raw["context_fingerprint"] != declaration.external_context_fingerprint
            or raw["context_introduction_event_ref"]
            != declaration.external_context_introduction_event_ref
            or raw["context_introduction_event_fingerprint"]
            != declaration.external_context_introduction_event_fingerprint
            or raw["context_authority_event_high_watermark"]
            != declaration.external_context_event_high_watermark
        ):
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.MEMORY_DECLARATION_SOURCE_MISMATCH,
                "NEXT_ACTION_CONTEXT declaration/body equality differs",
            )
        try:
            await self._task_authority_verifier.verify_next_action_context(
                context_ref=str(declaration.external_context_ref),
                context_fingerprint=str(declaration.external_context_fingerprint),
                introduction_event_ref=str(declaration.external_context_introduction_event_ref),
                introduction_event_fingerprint=str(
                    declaration.external_context_introduction_event_fingerprint
                ),
                snapshot_ref=str(declaration.external_context_snapshot_ref),
                snapshot_fingerprint=str(declaration.external_context_snapshot_fingerprint),
                owner_event_high_watermark=int(declaration.external_context_event_high_watermark),
                require_current=False,
            )
        except (ExternalTaskAuthorityError, ValueError) as exc:
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.MEMORY_DECLARATION_SOURCE_MISMATCH,
                "NEXT_ACTION_CONTEXT original owner prefix differs",
            ) from exc
        context = await self._task_authority_verifier.get_next_action_context(
            str(declaration.external_context_ref)
        )
        equality = (
            context is not None
            and context.context_ref == raw["context_ref"]
            and context.fingerprint == raw["context_fingerprint"]
            and context.context_logical_id == raw["context_logical_id"]
            and context.project_id == raw["project_id"]
            and context.task_contract_id == raw["task_contract_id"]
            and context.task_contract_version == raw["task_contract_version"]
            and context.context_slot_id == raw["context_slot_id"]
            and context.priority_class.value == raw["priority_class"]
            and context.critical_path_ordinal == raw["critical_path_ordinal"]
        )
        if not equality or context is None:
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.MEMORY_DECLARATION_SOURCE_MISMATCH,
                "NEXT_ACTION_CONTEXT body/owner equality differs",
            )
        return context

    async def _resolve_structured_declarations(
        self, request: CycleAdmissionRequest
    ) -> dict[int, Any]:
        result: dict[int, Any] = {}
        for ordinal, declaration in enumerate(request.candidate.memory_declarations, 1):
            mode = self._memory_policy.category_modes.get(declaration.category)
            if mode is not MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED:
                continue
            if declaration.source_evidence_ref is None:
                raise CycleAdmissionError(
                    CycleAdmissionErrorCode.SOURCE_NOT_ELIGIBLE, "structured source ref absent"
                )
            try:
                resolver = (
                    self._evidence_repository.verify_historical_admitted_evidence_with_content
                )
                verified = await resolver(
                    admitted_evidence_ref=declaration.source_evidence_ref,
                    exact_terminal_attestation_ref=request.candidate.evidence_attestation_ref,
                    access_grant=self._historical_content_access_grant,
                )
            except DurableContentError as exc:
                raise CycleAdmissionError(
                    CycleAdmissionErrorCode.SOURCE_NOT_ELIGIBLE, str(exc)
                ) from exc
            try:
                body = json.loads(verified.canonical_body_bytes)
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise CycleAdmissionError(
                    CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                    "owner-backed structured body is not canonical JSON",
                ) from exc
            result[ordinal] = (verified, body)
        return result

    def _verify_terminal_bindings(
        self, request: CycleAdmissionRequest, transition: Any, judgment: Any, attestation: Any
    ) -> None:
        candidate = request.candidate
        decision = transition.decision
        work_run = transition.work_run
        computed_decision_fingerprint = canonical_hash(
            {
                "admitting_owner": decision.admitting_owner,
                "decided_at": decision.decided_at.astimezone(UTC).isoformat(),
                "kernel_version": decision.kernel_version,
                "outcome": decision.outcome.value,
                "reason": decision.reason.value,
                "resulting_state": decision.resulting_state.value
                if decision.resulting_state
                else None,
                "resulting_state_version": decision.resulting_state_version,
                "transition_decision_id": decision.transition_decision_id,
                "transition_evaluation_id": decision.transition_evaluation_id,
                "transition_request_id": decision.transition_request_id,
            }
        )
        exact = (
            work_run.state is WorkflowState.ACCEPTED
            and decision.outcome is DecisionOutcome.ADMITTED
            and decision.resulting_state is WorkflowState.ACCEPTED
            and work_run.state_version == candidate.terminal_state_version
            and decision.resulting_state_version == candidate.terminal_state_version
            and decision.transition_decision_id == candidate.transition_decision_id
            and computed_decision_fingerprint == candidate.transition_decision_fingerprint
            and work_run.project_id == candidate.project_id
            and work_run.task_contract_id == candidate.task_contract_id
            and work_run.task_contract_version == candidate.task_contract_version
            and candidate.task_contract_fingerprint
            == p1_8_task_binding_fingerprint(
                project_id=work_run.project_id,
                task_contract_id=work_run.task_contract_id,
                task_contract_version=work_run.task_contract_version,
            )
            and judgment.fingerprint == candidate.judgment_fingerprint
            and judgment.serialized_ref in transition.request.judgment_refs
            and judgment.work_run_id == candidate.work_run_id
            and judgment.task_contract_id == candidate.task_contract_id
            and judgment.task_contract_version == candidate.task_contract_version
            and judgment.target_state is WorkflowState.ACCEPTED
            and judgment.evidence_attestation_ref == candidate.evidence_attestation_ref
            and judgment.evidence_root == candidate.evidence_root
            and attestation.serialized_ref == candidate.evidence_attestation_ref
            and attestation.admitted_ref_root_hash == candidate.evidence_root
            and attestation.work_run_id == candidate.work_run_id
            and attestation.task_contract_id == candidate.task_contract_id
            and attestation.task_contract_version == candidate.task_contract_version
            and attestation.satisfied
        )
        if not exact:
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.NOT_ACCEPTED_TERMINAL,
                "candidate does not bind the exact accepted terminal authority graph",
            )

    async def _verify_current_policy(self, session: AsyncSession) -> None:
        row = await session.get(MemoryDeclarationPolicyRow, self._memory_policy.serialized_ref)
        if (
            row is None
            or row.fingerprint != self._memory_policy.fingerprint
            or row.payload != _memory_policy_payload(self._memory_policy)
        ):
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.POLICY_NOT_CURRENT, "memory policy not enrolled"
            )
        events = tuple(
            await session.scalars(
                select(MemoryPolicyAuthorityEventRow)
                .where(MemoryPolicyAuthorityEventRow.policy_ref == row.serialized_ref)
                .order_by(MemoryPolicyAuthorityEventRow.event_sequence)
            )
        )
        if len(events) != 1 or events[0].event_kind != "ISSUED":
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.POLICY_NOT_CURRENT, "memory policy not current"
            )

    async def _persist_memory(
        self,
        session: AsyncSession,
        request: CycleAdmissionRequest,
        cycle_row: AdmittedCycleRow,
        derived: list[DerivedMemoryDeclaration],
        source_current: dict[str, bool],
        source_high_watermark: int,
        policy_high_watermark: int,
        context_current: dict[int, bool],
        now: datetime,
    ) -> None:
        for ordinal, (declaration, item) in enumerate(
            zip(request.candidate.memory_declarations, derived, strict=True), 1
        ):
            mode = item.authority_mode
            content = item.normalized_content
            content_fingerprint = item.content_fingerprint
            lineage = memory_lineage_key(
                project_id=request.candidate.project_id,
                category=declaration.category,
                subject_key=item.subject_key,
                applicability_key=item.applicability_key,
                semantic_slot=item.semantic_slot,
            )
            view = await session.get(ProjectMemoryViewRow, lineage, with_for_update=True)
            current_entry = (
                await session.get(ProjectMemoryEntryRow, view.current_entry_id)
                if view is not None and view.current_entry_id is not None
                else None
            )
            if (
                current_entry is not None
                and current_entry.content_fingerprint == content_fingerprint
            ):
                session.add(
                    CycleMemoryReferenceRow(
                        reference_id=canonical_hash(
                            {
                                "cycle_id": cycle_row.cycle_id,
                                "declaration_ordinal": ordinal,
                                "entry_id": current_entry.entry_id,
                            }
                        ),
                        cycle_id=cycle_row.cycle_id,
                        entry_id=current_entry.entry_id,
                        declaration_ordinal=ordinal,
                        content_fingerprint=content_fingerprint,
                        provenance=_external_context_provenance(declaration),
                        created_at=now,
                    )
                )
                continue
            if current_entry is not None and not await _supersession_authorized(
                session, declaration.supersession_authority_ref, current_entry
            ):
                raise CycleAdmissionError(
                    CycleAdmissionErrorCode.AUTHORITY_NOT_CURRENT,
                    "different-content replacement requires source-owner authority",
                )
            entry_id = project_memory_entry_id(
                cycle_id=cycle_row.cycle_id,
                memory_declaration_ordinal=ordinal,
                policy_fingerprint=declaration.policy_fingerprint,
                memory_lineage_key_value=lineage,
                content_fingerprint=content_fingerprint,
            )
            source_ref = item.source_authority_ref
            entry = ProjectMemoryEntryRow(
                entry_id=entry_id,
                memory_lineage_key=lineage,
                project_id=request.candidate.project_id,
                cycle_id=cycle_row.cycle_id,
                declaration_ordinal=ordinal,
                category=declaration.category.value,
                content_fingerprint=content_fingerprint,
                policy_ref=declaration.policy_ref,
                policy_fingerprint=declaration.policy_fingerprint,
                source_ref=source_ref,
                external_context_ref=declaration.external_context_ref,
                privacy=item.privacy.value,
                payload={
                    "applicability_key": item.applicability_key,
                    "authority_mode": mode.value,
                    "normalized_content": content,
                    "policy_event_high_watermark": policy_high_watermark,
                    "policy_privacy_authority_ref": declaration.policy_ref,
                    "source_authority_fingerprint": item.source_authority_fingerprint,
                    "source_event_high_watermark": source_high_watermark,
                    "source_privacy_authority_ref": source_ref,
                    "semantic_slot": item.semantic_slot,
                    "subject_key": item.subject_key,
                },
                created_at=now,
            )
            session.add(entry)
            await session.flush()
            session.add(
                CycleMemoryReferenceRow(
                    reference_id=canonical_hash(
                        {
                            "cycle_id": cycle_row.cycle_id,
                            "declaration_ordinal": ordinal,
                            "entry_id": entry_id,
                        }
                    ),
                    cycle_id=cycle_row.cycle_id,
                    entry_id=entry_id,
                    declaration_ordinal=ordinal,
                    content_fingerprint=content_fingerprint,
                    provenance=_external_context_provenance(declaration),
                    created_at=now,
                )
            )
            await session.flush()
            revision = view.authority_revision if view is not None else 0
            if current_entry is not None:
                superseded = ProjectMemoryAuthorityEventRow(
                    event_id="memory-superseded-"
                    + canonical_hash([current_entry.entry_id, entry_id]),
                    memory_lineage_key=lineage,
                    subject_entry_id=current_entry.entry_id,
                    replacement_entry_id=entry_id,
                    event_kind=MemoryApplicabilityState.SUPERSEDED.value,
                    prior_revision=revision,
                    new_revision=revision + 1,
                    authority_ref=declaration.supersession_authority_ref or "NONE",
                    reason="EXPLICIT_SUPERSESSION_ONLY",
                    payload={},
                    created_at=now,
                )
                session.add(superseded)
                await session.flush()
                revision += 1
            is_current = source_current.get(source_ref, True) and context_current.get(ordinal, True)
            state = (
                MemoryApplicabilityState.CURRENT if is_current else MemoryApplicabilityState.REVOKED
            )
            event = ProjectMemoryAuthorityEventRow(
                event_id="memory-applicability-" + canonical_hash([entry_id, state.value]),
                memory_lineage_key=lineage,
                subject_entry_id=entry_id,
                replacement_entry_id="NONE",
                event_kind=state.value,
                prior_revision=revision,
                new_revision=revision + 1,
                authority_ref=source_ref,
                reason="ADMITTED_CURRENT" if is_current else "SOURCE_NOT_CURRENT_AT_ADMISSION",
                payload={
                    "observed_current": is_current,
                    "policy_event_high_watermark": policy_high_watermark,
                    "source_event_high_watermark": source_high_watermark,
                },
                created_at=now,
            )
            session.add(event)
            await session.flush()
            if view is None:
                session.add(
                    ProjectMemoryViewRow(
                        memory_lineage_key=lineage,
                        project_id=request.candidate.project_id,
                        current_entry_id=entry_id if is_current else None,
                        state=state.value,
                        reason=event.reason,
                        authority_revision=revision + 1,
                        latest_event_sequence=event.event_sequence,
                        updated_at=now,
                    )
                )
            else:
                view.current_entry_id = entry_id if is_current else None
                view.state = state.value
                view.reason = event.reason
                view.authority_revision = revision + 1
                view.latest_event_sequence = event.event_sequence
                view.updated_at = now

    async def _verify_cycle_in_session(
        self, session: AsyncSession, row: AdmittedCycleRow
    ) -> AdmittedCycle:
        request = await session.get(CycleAdmissionRequestRow, row.request_id)
        decision = await session.get(CycleAdmissionDecisionRow, row.decision_id)
        evaluation = (
            await session.get(CycleEvaluationRow, decision.evaluation_id)
            if decision is not None
            else None
        )
        events = tuple(
            await session.scalars(
                select(CycleAuthorityEventRow).where(
                    CycleAuthorityEventRow.cycle_id == row.cycle_id
                )
            )
        )
        candidate_payload = dict(row.payload)
        computed_cycle_fingerprint = canonical_hash(
            {
                "cycle_id": row.cycle_id,
                "cycle_version": row.cycle_version,
                "evidence_attestation_ref": candidate_payload.get("evidence_attestation_ref"),
                "evidence_root": candidate_payload.get("evidence_root"),
                "judgment_fingerprint": candidate_payload.get("judgment_fingerprint"),
                "judgment_ref": candidate_payload.get("judgment_ref"),
                "memory_declarations": candidate_payload.get("memory_declarations"),
                "project_id": row.project_id,
                "p1_8_task_binding_fingerprint": candidate_payload.get(
                    "p1_8_task_binding_fingerprint"
                ),
                "task_contract_id": candidate_payload.get("task_contract_id"),
                "task_contract_version": candidate_payload.get("task_contract_version"),
                "terminal_state_version": row.terminal_state_version,
                "transition_decision_fingerprint": candidate_payload.get(
                    "transition_decision_fingerprint"
                ),
                "transition_decision_id": candidate_payload.get("transition_decision_id"),
                "transition_request_id": candidate_payload.get("transition_request_id"),
                "work_run_id": row.work_run_id,
                "task_constraint_ref": candidate_payload.get("task_constraint_ref"),
                "task_constraint_fingerprint": candidate_payload.get("task_constraint_fingerprint"),
                "task_constraint_snapshot_ref": candidate_payload.get(
                    "task_constraint_snapshot_ref"
                ),
                "task_constraint_snapshot_fingerprint": candidate_payload.get(
                    "task_constraint_snapshot_fingerprint"
                ),
                "task_constraint_event_high_watermark": candidate_payload.get(
                    "task_constraint_event_high_watermark"
                ),
            }
        )
        computed_request_fingerprint = (
            canonical_hash(
                {
                    "candidate_fingerprint": request.cycle_fingerprint,
                    "request_id": request.request_id,
                    "request_version": request.request_version,
                    "requested_at": request.requested_at.astimezone(UTC).isoformat(),
                    "requester_ref": request.payload.get("requester_ref"),
                }
            )
            if request is not None
            else ""
        )
        computed_evaluation_fingerprint = (
            canonical_hash(
                {
                    "evaluated_at": evaluation.evaluated_at.astimezone(UTC).isoformat(),
                    "evaluation_id": evaluation.evaluation_id,
                    "memory_content_fingerprints": evaluation.payload.get(
                        "memory_content_fingerprints"
                    ),
                    "outcome": evaluation.outcome,
                    "policy_fingerprints": evaluation.payload.get("policy_fingerprints"),
                    "request_fingerprint": evaluation.payload.get("request_fingerprint"),
                    "request_id": evaluation.request_id,
                    "terminal_provenance_fingerprint": evaluation.payload.get(
                        "terminal_provenance_fingerprint"
                    ),
                }
            )
            if evaluation is not None
            else ""
        )
        computed_decision_fingerprint = (
            canonical_hash(
                {
                    "authority_id": decision.payload.get("authority_id"),
                    "authority_version": decision.payload.get("authority_version"),
                    "decided_at": decision.decided_at.astimezone(UTC).isoformat(),
                    "decision_id": decision.decision_id,
                    "evaluation_fingerprint": decision.payload.get("evaluation_fingerprint"),
                    "evaluation_id": decision.evaluation_id,
                    "outcome": decision.outcome,
                    "reason": decision.reason,
                }
            )
            if decision is not None
            else ""
        )
        if (
            request is None
            or decision is None
            or evaluation is None
            or len(events) != 1
            or events[0].event_kind != "ADMITTED"
            or request.cycle_fingerprint != row.cycle_fingerprint
            or computed_cycle_fingerprint != row.cycle_fingerprint
            or request.request_fingerprint != computed_request_fingerprint
            or evaluation.evaluation_fingerprint != computed_evaluation_fingerprint
            or decision.decision_fingerprint != computed_decision_fingerprint
            or decision.request_id != request.request_id
            or evaluation.request_id != request.request_id
            or decision.outcome != "ADMITTED"
            or evaluation.outcome != "ACCEPTED"
            or events[0].payload.get("decision_id") != decision.decision_id
            or row.terminal_epoch_key
            != canonical_hash(
                {
                    "project_id": row.project_id,
                    "resulting_state_version": row.terminal_state_version,
                    "task_contract_id": candidate_payload.get("task_contract_id"),
                    "task_contract_version": candidate_payload.get("task_contract_version"),
                    "terminal_transition_decision_ref": candidate_payload.get(
                        "transition_decision_id"
                    ),
                    "terminal_epoch_schema": "P1_8_TERMINAL_EPOCH_KEY_V1",
                    "work_run_id": row.work_run_id,
                }
            )
            or row.terminal_epoch_payload_fingerprint
            != canonical_hash(
                {
                    "cycle_version": row.cycle_version,
                    "evidence_attestation_ref": candidate_payload.get("evidence_attestation_ref"),
                    "evidence_root": candidate_payload.get("evidence_root"),
                    "judgment_fingerprint": candidate_payload.get("judgment_fingerprint"),
                    "judgment_ref": candidate_payload.get("judgment_ref"),
                    "memory_declarations": candidate_payload.get("memory_declarations"),
                    "p1_8_task_binding_fingerprint_claim": candidate_payload.get(
                        "p1_8_task_binding_fingerprint"
                    ),
                    "terminal_epoch_key": row.terminal_epoch_key,
                    "transition_decision_fingerprint": candidate_payload.get(
                        "transition_decision_fingerprint"
                    ),
                    "transition_request_id": candidate_payload.get("transition_request_id"),
                    "task_constraint_ref": candidate_payload.get("task_constraint_ref"),
                    "task_constraint_fingerprint": candidate_payload.get(
                        "task_constraint_fingerprint"
                    ),
                    "task_constraint_snapshot_ref": candidate_payload.get(
                        "task_constraint_snapshot_ref"
                    ),
                    "task_constraint_snapshot_fingerprint": candidate_payload.get(
                        "task_constraint_snapshot_fingerprint"
                    ),
                    "task_constraint_event_high_watermark": candidate_payload.get(
                        "task_constraint_event_high_watermark"
                    ),
                }
            )
            or candidate_payload.get("p1_8_task_binding_fingerprint")
            != p1_8_task_binding_fingerprint(
                project_id=row.project_id,
                task_contract_id=str(candidate_payload.get("task_contract_id")),
                task_contract_version=str(candidate_payload.get("task_contract_version")),
            )
        ):
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.HISTORICAL_CORRUPTION, "Cycle authority graph differs"
            )
        try:
            await self._task_authority_verifier.verify_task_constraint(
                constraint_ref=str(row.task_constraint_ref),
                constraint_fingerprint=str(row.task_constraint_fingerprint),
                snapshot_ref=str(row.task_constraint_snapshot_ref),
                snapshot_fingerprint=str(row.task_constraint_snapshot_fingerprint),
                owner_event_high_watermark=int(row.task_constraint_event_high_watermark or 0),
                require_current=False,
            )
        except (ExternalTaskAuthorityError, ValueError) as exc:
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                "historical TaskConstraint authority graph differs",
            ) from exc
        transition = await verify_historical_transition_provenance(
            session, str(row.payload.get("transition_request_id"))
        )
        judgment = await verify_historical_judgment_provenance(
            session, str(row.payload.get("judgment_ref"))
        )
        attestation = await verify_historical_set_attestation_provenance(
            session, str(row.payload.get("evidence_attestation_ref"))
        )
        if (
            transition.decision.transition_decision_id != row.payload.get("transition_decision_id")
            or transition.decision.resulting_state is not WorkflowState.ACCEPTED
            or transition.decision.resulting_state_version != row.terminal_state_version
            or judgment.fingerprint != row.payload.get("judgment_fingerprint")
            or judgment.serialized_ref not in transition.request.judgment_refs
            or judgment.evidence_attestation_ref != attestation.serialized_ref
            or judgment.evidence_root != attestation.admitted_ref_root_hash
            or attestation.admitted_ref_root_hash != row.payload.get("evidence_root")
        ):
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                "historical predecessor authority differs from Cycle binding",
            )
        declarations = row.payload.get("memory_declarations")
        if not isinstance(declarations, list):
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                "memory declaration list is malformed",
            )
        entry_rows = tuple(
            await session.scalars(
                select(ProjectMemoryEntryRow).where(ProjectMemoryEntryRow.cycle_id == row.cycle_id)
            )
        )
        reference_rows = tuple(
            await session.scalars(
                select(CycleMemoryReferenceRow).where(
                    CycleMemoryReferenceRow.cycle_id == row.cycle_id
                )
            )
        )
        if len(reference_rows) != len(declarations):
            raise CycleAdmissionError(
                CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                "Cycle memory issuance cardinality differs",
            )
        by_ordinal = {item.declaration_ordinal: item for item in entry_rows}
        ref_by_ordinal = {item.declaration_ordinal: item for item in reference_rows}
        for ordinal, raw in enumerate(declarations, 1):
            if not isinstance(raw, dict):
                raise CycleAdmissionError(
                    CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                    "memory declaration payload is malformed",
                )
            policy_ref = raw.get("policy_ref")
            policy_fingerprint = raw.get("policy_fingerprint")
            policy = await session.get(MemoryDeclarationPolicyRow, policy_ref)
            policy_issuance = await session.scalar(
                select(MemoryPolicyAuthorityEventRow).where(
                    MemoryPolicyAuthorityEventRow.policy_ref == policy_ref,
                    MemoryPolicyAuthorityEventRow.event_kind == "ISSUED",
                    MemoryPolicyAuthorityEventRow.created_at <= row.admitted_at,
                    MemoryPolicyAuthorityEventRow.event_sequence
                    <= row.memory_policy_event_high_watermark,
                )
            )
            invalid_policy_at_admission = await session.scalar(
                select(func.count())
                .select_from(MemoryPolicyAuthorityEventRow)
                .where(
                    MemoryPolicyAuthorityEventRow.policy_ref == policy_ref,
                    MemoryPolicyAuthorityEventRow.event_kind.in_(("SUPERSEDED", "REVOKED")),
                    MemoryPolicyAuthorityEventRow.event_sequence
                    <= row.memory_policy_event_high_watermark,
                )
            )
            if (
                policy is None
                or policy.fingerprint != policy_fingerprint
                or canonical_hash(policy.payload) != policy.fingerprint
                or policy_issuance is None
                or policy_issuance.payload.get("fingerprint") != policy.fingerprint
                or policy_issuance.payload.get("authority_id") != policy.payload.get("authority_id")
                or policy_issuance.payload.get("authority_version")
                != policy.payload.get("authority_version")
                or bool(invalid_policy_at_admission)
            ):
                raise CycleAdmissionError(
                    CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                    "original memory policy validity differs",
                )
            entry = by_ordinal.get(ordinal)
            reference = ref_by_ordinal.get(ordinal)
            if entry is not None:
                try:
                    category = MemoryCategory(str(raw["category"]))
                    mode = MemoryAuthorityMode(str(entry.payload["authority_mode"]))
                    expected_lineage = memory_lineage_key(
                        project_id=row.project_id,
                        category=category,
                        subject_key=str(raw["subject_key"]),
                        applicability_key=str(raw["applicability_key"]),
                        semantic_slot=str(raw["semantic_slot"]),
                    )
                    expected_content = memory_content_fingerprint(
                        category=category,
                        authority_mode=mode,
                        policy_ref=str(policy_ref),
                        normalized_derived_content=entry.payload["normalized_content"],
                    )
                except (KeyError, ValueError, ProjectMemoryError) as exc:
                    raise CycleAdmissionError(
                        CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                        "memory entry immutable payload is malformed",
                    ) from exc
                if (
                    entry.memory_lineage_key != expected_lineage
                    or entry.content_fingerprint != expected_content
                    or entry.content_fingerprint != raw.get("claimed_content_fingerprint")
                    or entry.payload.get("source_event_high_watermark")
                    != row.source_owner_event_high_watermark
                    or entry.payload.get("policy_event_high_watermark")
                    != row.memory_policy_event_high_watermark
                ):
                    raise CycleAdmissionError(
                        CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                        "memory entry lineage/content fingerprint differs",
                    )
            elif reference is None or reference.content_fingerprint != raw.get(
                "claimed_content_fingerprint"
            ):
                raise CycleAdmissionError(
                    CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                    "CycleMemoryReference content binding differs",
                )
            source_ref = raw.get("source_evidence_ref")
            if isinstance(source_ref, str):
                if await _invalid_at(
                    session, source_ref, transition.decision.decided_at.astimezone(UTC)
                ):
                    raise CycleAdmissionError(
                        CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                        "structured source was invalid at terminal epoch",
                    )
                try:
                    await (
                        self._evidence_repository.verify_historical_admitted_evidence_with_content(
                            admitted_evidence_ref=source_ref,
                            exact_terminal_attestation_ref=attestation.serialized_ref,
                            access_grant=self._historical_content_access_grant,
                        )
                    )
                except DurableContentError as exc:
                    raise CycleAdmissionError(
                        CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                        "historical structured source integrity differs",
                    ) from exc
            if raw.get("category") == MemoryCategory.NEXT_ACTION_CONTEXT.value:
                target_entry = entry
                target_reference = reference
                provenance = (
                    target_reference.provenance
                    if target_reference is not None
                    else _external_context_provenance_from_raw(raw)
                )
                if (
                    provenance is None
                    or target_entry is not None
                    and target_entry.external_context_ref != raw.get("external_context_ref")
                    or provenance != _external_context_provenance_from_raw(raw)
                ):
                    raise CycleAdmissionError(
                        CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                        "historical external context provenance differs",
                    )
                try:
                    await self._task_authority_verifier.verify_next_action_context(
                        context_ref=str(raw["external_context_ref"]),
                        context_fingerprint=str(raw["external_context_fingerprint"]),
                        introduction_event_ref=str(raw["external_context_introduction_event_ref"]),
                        introduction_event_fingerprint=str(
                            raw["external_context_introduction_event_fingerprint"]
                        ),
                        snapshot_ref=str(raw["external_context_snapshot_ref"]),
                        snapshot_fingerprint=str(raw["external_context_snapshot_fingerprint"]),
                        owner_event_high_watermark=int(
                            raw["external_context_event_high_watermark"]
                        ),
                        require_current=False,
                    )
                except (ExternalTaskAuthorityError, KeyError, TypeError, ValueError) as exc:
                    raise CycleAdmissionError(
                        CycleAdmissionErrorCode.HISTORICAL_CORRUPTION,
                        "historical external context owner graph differs",
                    ) from exc
        return _cycle_from_row(row)


def _verified_memory_source(
    candidate: Any,
    declaration: Any,
    structured: Any,
    transition: Any,
    judgment: Any,
    attestation: Any,
    policy: MemoryDeclarationAuthorityPolicy,
) -> VerifiedMemorySource:
    contract = policy.category_contracts.get(declaration.category)
    if contract is None:
        raise ProjectMemoryError(
            ProjectMemoryErrorCode.AUTHORITY_NOT_FOUND,
            "category has no enrolled predecessor source authority",
        )
    if contract.authority_mode is MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED:
        if structured is None or declaration.source_evidence_ref is None:
            raise ProjectMemoryError(
                ProjectMemoryErrorCode.AUTHORITY_NOT_FOUND,
                "structured historical content authority absent",
            )
        verified, body = structured
        content = verified.metadata.content
        privacy = {
            EvidenceSensitivity.PUBLIC_SAFE: PrivacyClassification.PUBLIC_SANITIZED,
            EvidenceSensitivity.INTERNAL: PrivacyClassification.INTERNAL,
            EvidenceSensitivity.PRIVATE_SENSITIVE: PrivacyClassification.NON_EXPORTABLE,
        }.get(content.sensitivity)
        if privacy is None:
            raise ProjectMemoryError(
                ProjectMemoryErrorCode.SOURCE_MISMATCH,
                "source sensitivity is forbidden for ProjectMemory",
            )
        return VerifiedMemorySource(
            "P1_6_ADMITTED_STRUCTURED_RESULT",
            declaration.source_evidence_ref,
            content.payload_fingerprint,
            content.object_id,
            content.schema_id,
            content.schema_version,
            privacy,
            candidate.project_id,
            candidate.task_contract_id,
            body,
        )
    if declaration.category is MemoryCategory.INVARIANT_POINTER:
        return VerifiedMemorySource(
            "CANONICAL_RULE_ANCHOR",
            str(declaration.pointer_ref),
            contract.static_source_authority_fingerprint,
            "p1-8-project-memory-cycle-admission",
            contract.source_schema_id,
            contract.source_schema_version,
            PrivacyClassification.PUBLIC_SANITIZED,
            candidate.project_id,
            candidate.task_contract_id,
            {},
            anchor_id="project-memory-is-not-canonical-authority",
        )
    pointer = declaration.pointer_ref
    if pointer == candidate.transition_decision_id:
        return VerifiedMemorySource(
            "P1_4_TRANSITION_DECISION",
            pointer,
            candidate.transition_decision_fingerprint,
            candidate.transition_decision_id,
            contract.source_schema_id,
            contract.source_schema_version,
            PrivacyClassification.INTERNAL,
            candidate.project_id,
            candidate.task_contract_id,
            {},
            provenance_role="terminal-transition",
        )
    if pointer == candidate.judgment_ref:
        return VerifiedMemorySource(
            "P1_7_JUDGMENT",
            pointer,
            judgment.fingerprint,
            judgment.judgment_id,
            contract.source_schema_id,
            contract.source_schema_version,
            PrivacyClassification.INTERNAL,
            candidate.project_id,
            candidate.task_contract_id,
            {},
            provenance_role="terminal-judgment",
        )
    if pointer == candidate.evidence_attestation_ref:
        return VerifiedMemorySource(
            "P1_6_EVIDENCE_ATTESTATION",
            pointer,
            canonical_hash(
                {
                    "admitted_ref_root_hash": attestation.admitted_ref_root_hash,
                    "attestation_ref": attestation.serialized_ref,
                    "full_requirement_root_hash": attestation.full_requirement_root_hash,
                }
            ),
            attestation.attestation_id,
            contract.source_schema_id,
            contract.source_schema_version,
            PrivacyClassification.INTERNAL,
            candidate.project_id,
            candidate.task_contract_id,
            {},
            provenance_role="terminal-evidence",
        )
    raise ProjectMemoryError(
        ProjectMemoryErrorCode.AUTHORITY_NOT_FOUND,
        "pointer is not an enrolled exact predecessor object",
    )


async def _advisory_locks(session: AsyncSession, keys: tuple[str, ...]) -> None:
    for key in keys:
        await session.execute(
            text("SELECT pg_advisory_xact_lock(hashtextextended(:key, 0))"), {"key": key}
        )


async def _invalid_at(session: AsyncSession, subject_ref: str, at: datetime) -> bool:
    return bool(
        await session.scalar(
            select(func.count())
            .select_from(EvidenceAuthorityEventRow)
            .where(
                EvidenceAuthorityEventRow.subject_ref == subject_ref,
                EvidenceAuthorityEventRow.event_kind.in_(("REVOKED", "SUPERSEDED", "EXPIRED")),
                EvidenceAuthorityEventRow.created_at <= at,
            )
        )
    )


async def _supersession_authorized(
    session: AsyncSession, authority_ref: str | None, current: ProjectMemoryEntryRow
) -> bool:
    if authority_ref is None:
        return False
    event = await session.scalar(
        select(EvidenceAuthorityEventRow).where(
            EvidenceAuthorityEventRow.event_id == authority_ref,
            EvidenceAuthorityEventRow.subject_ref == current.source_ref,
            EvidenceAuthorityEventRow.event_kind.in_(("REVOKED", "SUPERSEDED")),
        )
    )
    return event is not None


def _memory_policy_payload(policy: MemoryDeclarationAuthorityPolicy) -> dict[str, object]:
    return {
        "authority_id": policy.authority_id,
        "authority_revision": policy.authority_revision,
        "authority_version": policy.authority_version,
        "category_contracts": {
            key.value: value.payload() for key, value in policy.category_contracts.items()
        },
        "category_modes": {key.value: value.value for key, value in policy.category_modes.items()},
        "category_priority": {key.value: value for key, value in policy.category_priority.items()},
        "policy_id": policy.policy_id,
        "policy_version": policy.policy_version,
        "effective_sequence": policy.effective_sequence,
        "revocation_disposition": policy.revocation_disposition.value,
        "structured_selectors": {
            key.value: value for key, value in policy.structured_selectors.items()
        },
        "supersedes_policy_ref": policy.supersedes_policy_ref,
        "supersession_disposition": policy.supersession_disposition.value,
    }


def _request_row(value: CycleAdmissionRequest) -> CycleAdmissionRequestRow:
    return CycleAdmissionRequestRow(
        request_id=value.request_id,
        request_version=value.request_version,
        request_fingerprint=value.fingerprint,
        cycle_id=value.candidate.cycle_id,
        cycle_fingerprint=value.candidate.fingerprint,
        project_id=value.candidate.project_id,
        work_run_id=value.candidate.work_run_id,
        terminal_state_version=value.candidate.terminal_state_version,
        payload={
            "candidate": _cycle_payload(value.candidate),
            "requester_ref": value.requester_ref,
        },
        requested_at=value.requested_at,
    )


def _evaluation_row(value: CycleEvaluation) -> CycleEvaluationRow:
    return CycleEvaluationRow(
        evaluation_id=value.evaluation_id,
        request_id=value.request_id,
        evaluation_fingerprint=value.fingerprint,
        outcome=value.outcome,
        payload={
            "memory_content_fingerprints": list(value.memory_content_fingerprints),
            "policy_fingerprints": list(value.policy_fingerprints),
            "request_fingerprint": value.request_fingerprint,
            "terminal_provenance_fingerprint": value.terminal_provenance_fingerprint,
        },
        evaluated_at=value.evaluated_at,
    )


def _decision_row(value: CycleAdmissionDecision, request_id: str) -> CycleAdmissionDecisionRow:
    return CycleAdmissionDecisionRow(
        decision_id=value.decision_id,
        evaluation_id=value.evaluation_id,
        request_id=request_id,
        decision_fingerprint=value.fingerprint,
        outcome=value.outcome,
        reason=value.reason,
        payload={
            "authority_id": value.authority_id,
            "authority_version": value.authority_version,
            "evaluation_fingerprint": value.evaluation_fingerprint,
        },
        decided_at=value.decided_at,
    )


def _cycle_payload(value: Any) -> dict[str, object]:
    return {
        "evidence_attestation_ref": value.evidence_attestation_ref,
        "evidence_root": value.evidence_root,
        "judgment_fingerprint": value.judgment_fingerprint,
        "judgment_ref": value.judgment_ref,
        "memory_declarations": [item.payload() for item in value.memory_declarations],
        "p1_8_task_binding_fingerprint": value.task_contract_fingerprint,
        "task_contract_id": value.task_contract_id,
        "task_contract_version": value.task_contract_version,
        "transition_decision_fingerprint": value.transition_decision_fingerprint,
        "transition_decision_id": value.transition_decision_id,
        "transition_request_id": value.transition_request_id,
        "task_constraint_ref": value.task_constraint_ref,
        "task_constraint_fingerprint": value.task_constraint_fingerprint,
        "task_constraint_snapshot_ref": value.task_constraint_snapshot_ref,
        "task_constraint_snapshot_fingerprint": value.task_constraint_snapshot_fingerprint,
        "task_constraint_event_high_watermark": (value.task_constraint_event_high_watermark),
    }


def _external_context_provenance(value: Any) -> dict[str, object] | None:
    if value.category is not MemoryCategory.NEXT_ACTION_CONTEXT:
        return None
    return {
        "context_ref": value.external_context_ref,
        "context_fingerprint": value.external_context_fingerprint,
        "context_introduction_event_ref": value.external_context_introduction_event_ref,
        "context_introduction_event_fingerprint": (
            value.external_context_introduction_event_fingerprint
        ),
        "context_snapshot_ref": value.external_context_snapshot_ref,
        "context_snapshot_fingerprint": value.external_context_snapshot_fingerprint,
        "context_authority_event_high_watermark": (value.external_context_event_high_watermark),
    }


def _external_context_provenance_from_raw(value: dict[str, object]) -> dict[str, object]:
    return {
        "context_ref": value.get("external_context_ref"),
        "context_fingerprint": value.get("external_context_fingerprint"),
        "context_introduction_event_ref": value.get("external_context_introduction_event_ref"),
        "context_introduction_event_fingerprint": value.get(
            "external_context_introduction_event_fingerprint"
        ),
        "context_snapshot_ref": value.get("external_context_snapshot_ref"),
        "context_snapshot_fingerprint": value.get("external_context_snapshot_fingerprint"),
        "context_authority_event_high_watermark": value.get(
            "external_context_event_high_watermark"
        ),
    }


def _cycle_from_row(row: AdmittedCycleRow) -> AdmittedCycle:
    payload = row.payload
    return AdmittedCycle(
        row.cycle_id,
        row.cycle_version,
        row.cycle_fingerprint,
        row.request_id,
        row.decision_id,
        row.project_id,
        str(payload["task_contract_id"]),
        str(payload["task_contract_version"]),
        row.work_run_id,
        row.terminal_state_version,
        str(payload["transition_decision_id"]),
        str(payload["judgment_ref"]),
        str(payload["evidence_attestation_ref"]),
        str(payload["evidence_root"]),
        str(row.task_constraint_ref),
        str(row.task_constraint_fingerprint),
        str(row.task_constraint_snapshot_ref),
        str(row.task_constraint_snapshot_fingerprint),
        int(row.task_constraint_event_high_watermark or 0),
        row.admission_sequence,
        row.admitted_at.astimezone(UTC),
    )
