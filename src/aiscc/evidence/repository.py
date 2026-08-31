from __future__ import annotations

import hashlib
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import uuid4

from sqlalchemy import func, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.contracts.workflow import WorkflowState
from aiscc.evidence.admission import (
    EVIDENCE_AUTHORITY_VERSION,
    EvidenceAdmissionEvaluator,
    make_admission_request,
)
from aiscc.evidence.content import (
    CANONICALIZATION_V1,
    DURABLE_CONTENT_AUTHORITY_ID,
    DURABLE_CONTENT_AUTHORITY_REVISION,
    DURABLE_CONTENT_AUTHORITY_VERSION,
    DURABLE_CONTENT_IDENTITY_SCHEMA,
    DURABLE_CONTENT_KINDS,
    DURABLE_CONTENT_PAYLOAD_SCHEMA,
    DURABLE_CONTENT_RETENTION_POLICY,
    MAX_DURABLE_CONTENT_BYTES,
    P1_6DurableContentAuthority,
    P1_6HistoricalContentAccessAuthority,
    PreparedDurableEvidenceContent,
    canonicalize_structured_json,
    source_owner_authority_fingerprint,
)
from aiscc.evidence.issuers import candidate_fingerprint, human_ingress_fingerprint
from aiscc.evidence.models import (
    AdmittedEvidence,
    AdmittedEvidenceRef,
    AuthoritativeWorkRunSnapshot,
    DurableContentError,
    DurableContentErrorCode,
    DurableContentRequirement,
    DurableEvidenceContentObject,
    EvidenceAdmissionDecision,
    EvidenceAdmissionDimension,
    EvidenceAdmissionOutcome,
    EvidenceAdmissionRequest,
    EvidenceAuthorityConflictError,
    EvidenceAuthorityEventKind,
    EvidenceCandidate,
    EvidenceCandidateDurableContentBinding,
    EvidenceCandidateRef,
    EvidenceCheckpoint,
    EvidenceCheckpointRef,
    EvidenceContentKind,
    EvidenceContentRef,
    EvidenceDimensionOutcome,
    EvidenceDimensionResult,
    EvidenceEvaluation,
    EvidenceIdentityConflictError,
    EvidenceIssuerType,
    EvidenceOwner,
    EvidenceRejectionReason,
    EvidenceRequirement,
    EvidenceRequirementProfile,
    EvidenceRequirementRef,
    EvidenceRequirementSatisfaction,
    EvidenceRequirementSet,
    EvidenceSemanticOwner,
    EvidenceSensitivity,
    EvidenceSetEvaluation,
    EvidenceSetOutcome,
    EvidenceSetSatisfactionAttestation,
    FreshnessPolicy,
    FreshnessPolicyKind,
    HistoricalContentAccessGrant,
    HumanDirectEvidenceIngress,
    HumanDirectEvidenceIngressRef,
    HumanEvidenceProducerCategory,
    RequirementFingerprintSchema,
    RequirementObligation,
    RequirementSatisfaction,
    VerifiedHistoricalContent,
    VerifiedHistoricalContentMetadata,
    canonical_hash,
)
from aiscc.evidence.requirements import (
    TaskContractEvidenceAuthority,
    _checkpoint_payload,
    _requirement_payload,
    _set_payload,
)
from aiscc.persistence.models import (
    AdmittedEvidenceRow,
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
    EvidenceReuseConsumptionRow,
    EvidenceSetAttestationRow,
    EvidenceSetEvaluationRow,
    ExecutionAttemptRow,
    ExecutionOutputRefRow,
    HumanDirectEvidenceIngressRow,
    WorkRunRow,
)
from aiscc.persistence.repository import acquire_work_run_transaction_lock


class HistoricalEvidenceProvenanceError(EvidenceAuthorityConflictError):
    """Projection-independent immutable P1-6 issuance failure."""

    def __init__(self, message: str, *, incomplete: bool = False) -> None:
        super().__init__(message)
        self.incomplete = incomplete


class PostgresEvidenceRepository:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        *,
        durable_content_authority: P1_6DurableContentAuthority | None = None,
        historical_content_access_authority: (
            P1_6HistoricalContentAccessAuthority | None
        ) = None,
    ) -> None:
        self._session_factory = session_factory
        self._durable_content_authority = durable_content_authority
        self._historical_content_access_authority = historical_content_access_authority

    def is_configured_durable_content_authority(
        self, authority: P1_6DurableContentAuthority | None
    ) -> bool:
        """Construction-time identity check; authority IDs/versions are not capabilities."""
        return authority is self._durable_content_authority

    async def register_authority(
        self,
        *,
        requirement_set: EvidenceRequirementSet,
        requirements: tuple[EvidenceRequirement, ...],
        checkpoints: tuple[EvidenceCheckpoint, ...],
        authority: TaskContractEvidenceAuthority,
    ) -> None:
        if not authority.recognizes(requirement_set) or any(
            not authority.recognizes(item) for item in (*requirements, *checkpoints)
        ):
            raise EvidenceAuthorityConflictError("unrecognized TaskContract evidence authority")
        set_ref = _set_ref(
            requirement_set.requirement_set_id, requirement_set.requirement_set_version
        )
        if requirement_set.ordered_requirement_refs != tuple(
            item.ref.serialized() for item in requirements
        ) or requirement_set.ordered_checkpoint_refs != tuple(
            item.ref.serialized() for item in checkpoints
        ):
            raise EvidenceAuthorityConflictError("authority snapshot ordering mismatch")
        async with self._session_factory() as session, session.begin():
            await _lock(
                session,
                f"evidence-task:{requirement_set.task_contract_id}:"
                f"{requirement_set.task_contract_version}",
            )
            await _lock(session, f"evidence-set:{set_ref}")
            existing = await session.get(EvidenceRequirementSetRow, set_ref)
            if existing is not None:
                if existing.fingerprint != requirement_set.fingerprint:
                    raise EvidenceIdentityConflictError("RequirementSet identity conflict")
                return
            same_task_sets = tuple(
                await session.scalars(
                    select(EvidenceRequirementSetRow).where(
                        EvidenceRequirementSetRow.task_contract_id
                        == requirement_set.task_contract_id,
                        EvidenceRequirementSetRow.task_contract_version
                        == requirement_set.task_contract_version,
                    )
                )
            )
            current_set_values: list[EvidenceRequirementSetRow] = []
            for item in same_task_sets:
                if item.payload.get("revoked_at") is None and not await _has_invalidating_event(
                    session, item.requirement_set_ref
                ):
                    current_set_values.append(item)
            current_sets = tuple(current_set_values)
            if len(current_sets) > 1:
                raise EvidenceAuthorityConflictError(
                    "TaskContract has ambiguous current RequirementSet authority"
                )
            if current_sets:
                current_ref = current_sets[0].requirement_set_ref
                if requirement_set.supersedes_set_ref != current_ref:
                    raise EvidenceAuthorityConflictError(
                        "new RequirementSet must explicitly supersede the exact current set"
                    )
            session.add(_set_row(requirement_set))
            await session.flush()
            session.add_all(_requirement_row(item) for item in requirements)
            session.add_all(_checkpoint_row(item) for item in checkpoints)
            if current_sets:
                session.add(
                    EvidenceAuthorityEventRow(
                        event_id=str(uuid4()),
                        subject_ref=current_sets[0].requirement_set_ref,
                        event_kind=EvidenceAuthorityEventKind.SUPERSEDED.value,
                        replacement_ref=set_ref,
                        reason="REQUIREMENT_SET_SUPERSEDED",
                        owner_id=authority.authority_id,
                        authority_version=requirement_set.authority_version,
                        task_contract_id=requirement_set.task_contract_id,
                        task_contract_version=requirement_set.task_contract_version,
                        work_run_id=None,
                        affected_refs=[current_sets[0].requirement_set_ref, set_ref],
                        affected_mappings=[],
                        created_at=requirement_set.issued_at,
                    )
                )

    async def persist_human_ingress(self, value: HumanDirectEvidenceIngress) -> None:
        async with self._session_factory() as session, session.begin():
            await _lock(session, f"evidence-human-ingress:{value.ref.ingress_record_id}")
            existing = await session.get(HumanDirectEvidenceIngressRow, value.ref.ingress_record_id)
            if existing is not None:
                if (
                    existing.fingerprint != value.ref.fingerprint
                    or existing.serialized_ref != value.ref.serialized()
                ):
                    raise EvidenceIdentityConflictError("Human ingress identity conflict")
                return
            duplicate_ref = await session.scalar(
                select(HumanDirectEvidenceIngressRow).where(
                    HumanDirectEvidenceIngressRow.serialized_ref == value.ref.serialized()
                )
            )
            if duplicate_ref is not None:
                raise EvidenceIdentityConflictError("Human ingress ref identity conflict")
            session.add(_human_ingress_row(value))

    async def load_human_ingress(self, serialized_ref: str) -> HumanDirectEvidenceIngress | None:
        async with self._session_factory() as session:
            row = await session.scalar(
                select(HumanDirectEvidenceIngressRow).where(
                    HumanDirectEvidenceIngressRow.serialized_ref == serialized_ref
                )
            )
            return _human_ingress_from_row(row) if row is not None else None

    async def preserve_supplemental_candidate(self, candidate: EvidenceCandidate) -> None:
        """Append-only provenance only: no requirement, admission, set, or guard authority."""
        async with self._session_factory() as session, session.begin():
            await _lock(session, f"evidence-candidate:{candidate.candidate_id}")
            await _persist_candidate(session, candidate)

    async def admit(
        self,
        *,
        request: EvidenceAdmissionRequest,
        candidate: EvidenceCandidate,
        evaluator: EvidenceAdmissionEvaluator,
        now: datetime | None = None,
        prepared_durable_content: PreparedDurableEvidenceContent | None = None,
    ) -> tuple[EvidenceAdmissionDecision, AdmittedEvidence | None]:
        if request.candidate_ref != EvidenceCandidateRef(
            candidate.candidate_id,
            candidate.candidate_version,
            candidate.candidate_fingerprint,
        ):
            raise EvidenceIdentityConflictError("request candidate ref mismatch")
        if prepared_durable_content is not None and (
            self._durable_content_authority is None
            or not self._durable_content_authority.recognizes(prepared_durable_content)
        ):
            raise DurableContentError(
                DurableContentErrorCode.ACCESS_DENIED,
                "durable write requires the configured P1-6 writer capability",
            )
        async with self._session_factory() as session, session.begin():
            await _acquire_work_run_transaction_lock(session, request.work_run_id)
            await _lock(session, f"evidence-request:{request.admission_request_id}")
            await _lock(
                session,
                f"evidence-task:{request.task_contract_id}:{request.task_contract_version}",
            )
            if prepared_durable_content is not None:
                await _lock(
                    session,
                    "evidence-content:"
                    + prepared_durable_content.content.content_identity_key,
                )
            await _lock(
                session,
                ":".join(
                    (
                        "evidence-logical",
                        request.work_run_id,
                        request.checkpoint_ref.serialized(),
                        request.requirement_ref.serialized(),
                        candidate.content_ref.content_hash,
                    )
                ),
            )
            existing_request = await session.get(
                EvidenceAdmissionRequestRow, request.admission_request_id
            )
            if existing_request is not None:
                if existing_request.request_fingerprint != request.request_fingerprint:
                    raise EvidenceIdentityConflictError(
                        "admission request ID has different immutable content"
                    )
                return await _load_request_result(session, request.admission_request_id)

            work_run_row = await session.scalar(
                select(WorkRunRow)
                .where(WorkRunRow.work_run_id == request.work_run_id)
                .with_for_update()
            )
            authoritative_work_run = (
                _authoritative_work_run_snapshot(work_run_row) if work_run_row is not None else None
            )

            reuse_consumed = 0
            if candidate.prior_admitted_evidence_ref:
                reuse_scope = _reuse_scope_key(request, candidate.prior_admitted_evidence_ref)
                await _lock(session, f"evidence-reuse:{reuse_scope}")
                reuse_consumed = int(
                    await session.scalar(
                        select(func.count())
                        .select_from(EvidenceReuseConsumptionRow)
                        .where(
                            EvidenceReuseConsumptionRow.prior_admitted_evidence_ref
                            == candidate.prior_admitted_evidence_ref,
                            EvidenceReuseConsumptionRow.requirement_ref
                            == request.requirement_ref.serialized(),
                            EvidenceReuseConsumptionRow.work_run_id == request.work_run_id,
                            EvidenceReuseConsumptionRow.checkpoint_ref
                            == request.checkpoint_ref.serialized(),
                        )
                    )
                    or 0
                )

            await _persist_candidate(session, candidate)
            set_ref = _set_ref(request.requirement_set_id, request.requirement_set_version)
            set_row = await session.get(EvidenceRequirementSetRow, set_ref)
            checkpoint_row = await session.get(
                EvidenceCheckpointRow, request.checkpoint_ref.serialized()
            )
            requirement_row = await session.get(
                EvidenceRequirementRow, request.requirement_ref.serialized()
            )
            requirement_set = _set_from_row(set_row) if set_row is not None else None
            checkpoint = (
                _checkpoint_from_row(checkpoint_row) if checkpoint_row is not None else None
            )
            requirement = (
                _requirement_from_row(requirement_row) if requirement_row is not None else None
            )
            durable_required = bool(
                requirement is not None
                and requirement.fingerprint_schema
                is RequirementFingerprintSchema.V2_DURABLE_CONTENT
                and requirement.durable_content_requirement
                is DurableContentRequirement.REQUIRED
            )
            if prepared_durable_content is not None and not durable_required:
                raise DurableContentError(
                    DurableContentErrorCode.REQUIREMENT_LEGACY_IDENTITY_CONFLICT,
                    "durable content cannot be attached to a non-V2 Requirement",
                )
            if durable_required and prepared_durable_content is not None:
                if requirement is None or requirement_set is None:
                    raise DurableContentError(
                        DurableContentErrorCode.REQUIRED,
                        "durable content lacks Requirement authority",
                    )
                await _persist_durable_content_and_binding(
                    session,
                    prepared=prepared_durable_content,
                    candidate=candidate,
                    request=request,
                    requirement=requirement,
                    requirement_set=requirement_set,
                    bound_at=(now or datetime.now(UTC)).astimezone(UTC),
                )
            authority_current = bool(
                set_row
                and checkpoint_row
                and requirement_row
                and set_row.payload.get("revoked_at") is None
                and checkpoint_row.payload.get("revoked_at") is None
                and requirement_row.payload.get("revoked_at") is None
                and not await _has_invalidating_event(session, set_ref)
                and not await _has_invalidating_event(session, request.checkpoint_ref.serialized())
                and not await _has_invalidating_event(session, request.requirement_ref.serialized())
            )
            prior = None
            prior_effective = False
            if candidate.prior_admitted_evidence_ref:
                prior_row = await _admitted_by_ref(session, candidate.prior_admitted_evidence_ref)
                if prior_row is not None:
                    prior = _admitted_from_row(prior_row)
                    prior_effective = not await _has_invalidating_event(
                        session, candidate.prior_admitted_evidence_ref
                    )
            evaluator_arguments: dict[str, Any] = {
                "request": request,
                "candidate": candidate,
                "requirement": requirement,
                "checkpoint": checkpoint,
                "requirement_set": requirement_set,
                "prior_admitted": prior,
                "prior_effective": prior_effective,
                "authoritative_work_run": authoritative_work_run,
                "reuse_consumed": reuse_consumed,
                "authority_current": authority_current,
                "now": now,
            }
            if durable_required:
                evaluator_arguments["authoritative_content_body"] = (
                    prepared_durable_content.content.canonical_body_bytes
                    if prepared_durable_content is not None
                    else None
                )
            evaluation, decision = await evaluator.evaluate(**evaluator_arguments)
            session.add(_request_row(request))
            await session.flush()
            session.add(_evaluation_row(evaluation))
            await session.flush()
            session.add(_decision_row(decision))
            await session.flush()
            admitted = None
            if decision.outcome is EvidenceAdmissionOutcome.ADMITTED:
                duplicate = await session.scalar(
                    select(AdmittedEvidenceRow)
                    .join(
                        EvidenceCandidateRow,
                        EvidenceCandidateRow.candidate_id == AdmittedEvidenceRow.candidate_id,
                    )
                    .where(
                        AdmittedEvidenceRow.requirement_ref == request.requirement_ref.serialized(),
                        AdmittedEvidenceRow.work_run_id == request.work_run_id,
                        AdmittedEvidenceRow.checkpoint_ref == request.checkpoint_ref.serialized(),
                        EvidenceCandidateRow.candidate_fingerprint
                        == candidate.candidate_fingerprint,
                    )
                    .limit(1)
                )
                if duplicate is not None:
                    admitted = _admitted_from_row(duplicate)
                else:
                    admitted = _make_admitted(request, candidate, decision)
                    session.add(_admitted_row(admitted))
                    await session.flush()
                    session.add(
                        EvidenceRequirementSatisfactionRow(
                            satisfaction_id=f"satisfaction-{admitted.admitted_evidence_id}",
                            admitted_evidence_id=admitted.admitted_evidence_id,
                            requirement_ref=admitted.requirement_ref.serialized(),
                            work_run_id=admitted.work_run_id,
                            checkpoint_ref=admitted.checkpoint_ref.serialized(),
                            coverage=list(admitted.coverage),
                            created_at=admitted.admitted_at,
                        )
                    )
                    if candidate.prior_admitted_evidence_ref:
                        if requirement is None:
                            raise EvidenceAuthorityConflictError(
                                "reuse admission lacks current requirement authority"
                            )
                        session.add(
                            EvidenceReuseConsumptionRow(
                                consumption_id=f"reuse-{admitted.admitted_evidence_id}",
                                prior_admitted_evidence_ref=(candidate.prior_admitted_evidence_ref),
                                admitted_evidence_id=admitted.admitted_evidence_id,
                                requirement_ref=request.requirement_ref.serialized(),
                                work_run_id=request.work_run_id,
                                checkpoint_ref=request.checkpoint_ref.serialized(),
                                policy_maximum=requirement.reuse_maximum,
                                consumption_ordinal=reuse_consumed + 1,
                                consumed_at=admitted.admitted_at,
                            )
                        )
            return decision, admitted

    async def revoke(
        self,
        *,
        subject_ref: str,
        reason: str,
        owner_id: str,
        authority_version: str,
        replacement_ref: str | None = None,
        kind: EvidenceAuthorityEventKind = EvidenceAuthorityEventKind.REVOKED,
    ) -> None:
        if not subject_ref or not reason or not owner_id or not authority_version:
            raise ValueError("authority event requires subject, owner, version, and reason")
        if (
            kind
            in {
                EvidenceAuthorityEventKind.SUPERSEDED,
                EvidenceAuthorityEventKind.CORRECTED,
            }
            and not replacement_ref
        ):
            raise ValueError("supersession/correction requires an exact replacement ref")
        replacement = replacement_ref or "NONE"
        async with self._session_factory() as session, session.begin():
            initial_scope = await _authority_subject_scope(session, subject_ref)
            if initial_scope is None:
                raise EvidenceAuthorityConflictError("authority event subject is unknown")
            subject_kind, task_id, task_version, work_run_id, affected_mappings = initial_scope
            await _lock(session, f"evidence-task:{task_id}:{task_version}")
            await _lock(session, f"evidence-authority-event:{subject_ref}")
            current_scope = await _authority_subject_scope(session, subject_ref)
            if current_scope != initial_scope:
                raise EvidenceAuthorityConflictError("authority event subject scope changed")
            if replacement_ref:
                replacement_scope = await _authority_subject_scope(session, replacement_ref)
                if replacement_scope is None or replacement_scope[0] != subject_kind:
                    raise EvidenceAuthorityConflictError(
                        "authority event replacement has a different or unknown authority kind"
                    )
                if replacement_scope[1:4] != initial_scope[1:4]:
                    raise EvidenceAuthorityConflictError(
                        "authority event replacement has a different Task/run scope"
                    )
            exists = await session.scalar(
                select(EvidenceAuthorityEventRow).where(
                    EvidenceAuthorityEventRow.subject_ref == subject_ref,
                    EvidenceAuthorityEventRow.event_kind == kind.value,
                    EvidenceAuthorityEventRow.replacement_ref == replacement,
                )
            )
            if exists is not None:
                if (
                    exists.reason != reason[:128]
                    or exists.owner_id != owner_id
                    or exists.authority_version != authority_version
                    or exists.task_contract_id != task_id
                    or exists.task_contract_version != task_version
                    or exists.work_run_id != work_run_id
                ):
                    raise EvidenceIdentityConflictError("authority event identity conflict")
                return
            session.add(
                EvidenceAuthorityEventRow(
                    event_id=str(uuid4()),
                    subject_ref=subject_ref,
                    event_kind=kind.value,
                    replacement_ref=replacement,
                    reason=reason[:128],
                    owner_id=owner_id,
                    authority_version=authority_version,
                    task_contract_id=task_id,
                    task_contract_version=task_version,
                    work_run_id=work_run_id,
                    affected_refs=[subject_ref]
                    + ([replacement_ref] if replacement_ref is not None else []),
                    affected_mappings=list(affected_mappings),
                    created_at=datetime.now(UTC),
                )
            )

    async def verify(
        self,
        *,
        ref_id: str,
        expected_kind: str,
        work_run_id: str,
        execution_attempt_id: str,
        content_hash: str,
    ) -> bool:
        """P1-5 immutable output-ref owner verification; never evidence admission."""
        async with self._session_factory() as session:
            row = await session.get(ExecutionOutputRefRow, ref_id)
            attempt = await session.get(ExecutionAttemptRow, execution_attempt_id)
            return bool(
                row
                and attempt
                and row.execution_attempt_id == execution_attempt_id
                and attempt.work_run_id == work_run_id
                and row.ref_kind == expected_kind
                and row.content_hash == content_hash
                and row.storage_ref.startswith("private://")
            )

    async def load_admitted(self, serialized_ref: str) -> AdmittedEvidence | None:
        async with self._session_factory() as session:
            row = await _admitted_by_ref(session, serialized_ref)
            if row is None or await _has_invalidating_event(session, serialized_ref):
                return None
            return _admitted_from_row(row)

    async def counts(self) -> dict[str, int]:
        async with self._session_factory() as session:
            result: dict[str, int] = {}
            for name, model in (
                ("human_ingress", HumanDirectEvidenceIngressRow),
                ("candidates", EvidenceCandidateRow),
                ("durable_content_objects", EvidenceContentObjectRow),
                ("durable_content_bindings", EvidenceCandidateContentBindingRow),
                ("requests", EvidenceAdmissionRequestRow),
                ("decisions", EvidenceAdmissionDecisionRow),
                ("admitted", AdmittedEvidenceRow),
                ("reuse_consumptions", EvidenceReuseConsumptionRow),
                ("set_evaluations", EvidenceSetEvaluationRow),
                ("attestations", EvidenceSetAttestationRow),
                ("authority_events", EvidenceAuthorityEventRow),
            ):
                result[name] = int(
                    await session.scalar(select(func.count()).select_from(model)) or 0
                )
            return result

    async def verify_historical_content_ref(
        self,
        content_ref: EvidenceContentRef,
        *,
        expected_payload_fingerprint: str | None = None,
    ) -> VerifiedHistoricalContentMetadata:
        """Verify immutable PostgreSQL content without consulting current effectiveness."""
        async with self._session_factory() as session:
            return await _verify_historical_content_in_session(
                session,
                content_ref,
                expected_payload_fingerprint=expected_payload_fingerprint,
            )

    async def resolve_historical_canonical_body(
        self,
        content_ref: EvidenceContentRef,
        *,
        access_grant: HistoricalContentAccessGrant,
    ) -> VerifiedHistoricalContent:
        """Opt-in exact-body resolution; caller bytes are never an input."""
        metadata = await self.verify_historical_content_ref(content_ref)
        content = metadata.content
        if not _historical_content_access_allowed(
            content, access_grant, self._historical_content_access_authority
        ):
            raise DurableContentError(
                DurableContentErrorCode.ACCESS_DENIED,
                "consumer grant does not authorize exact historical bytes",
            )
        return VerifiedHistoricalContent(metadata, bytes(content.canonical_body_bytes))

    async def verify_historical_admitted_evidence_with_content(
        self,
        *,
        admitted_evidence_ref: str,
        exact_terminal_attestation_ref: str,
        access_grant: HistoricalContentAccessGrant,
    ) -> VerifiedHistoricalContent:
        """Verify terminal-consumed P1-6 admission plus its original V2 content binding."""
        async with self._session_factory() as session:
            attestation = await verify_historical_set_attestation_provenance(
                session, exact_terminal_attestation_ref
            )
            terminal_refs = set(attestation.ordered_admitted_evidence_refs)
            if admitted_evidence_ref not in terminal_refs:
                raise DurableContentError(
                    DurableContentErrorCode.INTEGRITY_MISMATCH,
                    "admitted evidence is not a member of the exact terminal attestation",
                )
            admitted = await _verify_historical_admitted_ref(
                session,
                serialized_ref=admitted_evidence_ref,
                value=attestation,
            )
            admitted_row = await _admitted_by_ref(session, admitted_evidence_ref)
            if admitted_row is None:
                raise DurableContentError(
                    DurableContentErrorCode.MISSING,
                    "terminal admitted evidence row is absent",
                )
            binding_row = await session.get(
                EvidenceCandidateContentBindingRow, admitted_row.candidate_id
            )
            if binding_row is None:
                raise DurableContentError(
                    DurableContentErrorCode.P1_8_SOURCE_NOT_DURABLE,
                    "historical admission lacks an original V2 durable binding",
                )
            binding = await _verify_durable_binding_in_session(session, binding_row)
            if (
                binding.requirement_ref != admitted.requirement_ref.serialized()
                or binding.requirement_root_hash != attestation.full_requirement_root_hash
            ):
                raise DurableContentError(
                    DurableContentErrorCode.INTEGRITY_MISMATCH,
                    "durable binding differs from terminal-consumed Requirement authority",
                )
            metadata = await _verify_historical_content_in_session(
                session,
                admitted.content_ref,
                expected_payload_fingerprint=(
                    binding.durable_content_payload_fingerprint
                ),
            )
            if not _historical_content_access_allowed(
                metadata.content,
                access_grant,
                self._historical_content_access_authority,
            ):
                raise DurableContentError(
                    DurableContentErrorCode.ACCESS_DENIED,
                    "consumer grant does not authorize exact historical bytes",
                )
            return VerifiedHistoricalContent(
                metadata, bytes(metadata.content.canonical_body_bytes)
            )

    async def require_p1_8_structured_source_binding(
        self, candidate_id: str
    ) -> EvidenceCandidateDurableContentBinding:
        """Read-only eligibility cut: legacy metadata-only candidates fail closed."""
        async with self._session_factory() as session:
            row = await session.get(EvidenceCandidateContentBindingRow, candidate_id)
            if row is None:
                raise DurableContentError(
                    DurableContentErrorCode.P1_8_SOURCE_NOT_DURABLE,
                    "candidate lacks original V2 REQUIRED durable binding",
                )
            return await _verify_durable_binding_in_session(session, row)

    async def evaluate_set(
        self,
        *,
        work_run_id: str,
        checkpoint_ref: EvidenceCheckpointRef,
        observed_state: WorkflowState,
        observed_state_version: int,
        authority_id: str,
        authority_version: str,
        now: datetime | None = None,
    ) -> tuple[EvidenceSetEvaluation, EvidenceSetSatisfactionAttestation | None]:
        evaluated_at = (now or datetime.now(UTC)).astimezone(UTC)
        async with self._session_factory() as session, session.begin():
            await _lock(session, f"evidence-set-eval:{work_run_id}")
            run = await session.scalar(
                select(WorkRunRow).where(WorkRunRow.work_run_id == work_run_id).with_for_update()
            )
            checkpoint_row = await session.get(EvidenceCheckpointRow, checkpoint_ref.serialized())
            if (
                run is None
                or run.workflow_state != observed_state.value
                or run.state_version != observed_state_version
                or checkpoint_row is None
                or checkpoint_row.source_state != observed_state.value
            ):
                raise EvidenceAuthorityConflictError(
                    "set evaluation requires fresh WorkRun/checkpoint authority"
                )
            await _lock(
                session,
                f"evidence-task:{run.task_contract_id}:{run.task_contract_version}",
            )
            if checkpoint_row.payload.get(
                "revoked_at"
            ) is not None or await _has_invalidating_event(session, checkpoint_ref.serialized()):
                raise EvidenceAuthorityConflictError(
                    "set evaluation requires current checkpoint authority"
                )
            checkpoint = _checkpoint_from_row(checkpoint_row)
            set_row = await session.get(
                EvidenceRequirementSetRow, checkpoint_row.requirement_set_ref
            )
            if set_row is None:
                raise EvidenceAuthorityConflictError("checkpoint RequirementSet is missing")
            requirement_set = _set_from_row(set_row)
            if (
                set_row.task_contract_id != run.task_contract_id
                or set_row.task_contract_version != run.task_contract_version
                or set_row.payload.get("revoked_at") is not None
                or await _has_invalidating_event(session, set_row.requirement_set_ref)
            ):
                raise EvidenceAuthorityConflictError("RequirementSet is stale or revoked")
            requirement_rows = {
                row.requirement_ref: row
                for row in await session.scalars(
                    select(EvidenceRequirementRow).where(
                        EvidenceRequirementRow.requirement_set_ref
                        == checkpoint_row.requirement_set_ref
                    )
                )
            }
            if set(requirement_rows) != set(requirement_set.ordered_requirement_refs):
                raise EvidenceAuthorityConflictError(
                    "RequirementSet definition/projection is incomplete"
                )
            requirements = tuple(
                _requirement_from_row(requirement_rows[ref])
                for ref in requirement_set.ordered_requirement_refs
            )
            for item in requirements:
                definition_row = requirement_rows[item.ref.serialized()]
                if definition_row.payload.get(
                    "revoked_at"
                ) is not None or await _has_invalidating_event(session, item.ref.serialized()):
                    raise EvidenceAuthorityConflictError(
                        "RequirementSet contains revoked or superseded requirement authority"
                    )
            authority_revision = await _current_authority_revision(
                session,
                task_contract_id=run.task_contract_id,
                task_contract_version=run.task_contract_version,
                work_run_id=work_run_id,
            )
            applicable = tuple(
                item
                for item in requirements
                if checkpoint_ref.serialized() in item.applicable_checkpoint_refs
            )
            subset_root = canonical_hash(
                [(item.ref.serialized(), item.fingerprint) for item in applicable]
            )
            admitted_rows = tuple(
                await session.scalars(
                    select(AdmittedEvidenceRow).where(
                        AdmittedEvidenceRow.work_run_id == work_run_id,
                        AdmittedEvidenceRow.checkpoint_ref == checkpoint_ref.serialized(),
                    )
                )
            )
            effective_rows: list[AdmittedEvidenceRow] = []
            for admitted_row in admitted_rows:
                serialized = AdmittedEvidenceRef(
                    admitted_row.admitted_evidence_id, authority_version
                ).serialized()
                if not await _has_invalidating_event(session, serialized):
                    effective_rows.append(admitted_row)
            results: list[EvidenceRequirementSatisfaction] = []
            all_satisfied = True
            admitted_refs: list[str] = []
            expiry_candidates: list[datetime] = []
            for requirement in applicable:
                matching = [
                    row
                    for row in effective_rows
                    if row.requirement_ref == requirement.ref.serialized()
                    and await _admitted_current_for_set(
                        session, row, requirement, run, evaluated_at
                    )
                ]
                if requirement.profile is EvidenceRequirementProfile.NOT_REQUIRED:
                    continue
                if requirement.profile is EvidenceRequirementProfile.FORBIDDEN:
                    satisfied = not matching
                    result_refs: tuple[str, ...] = ()
                    coverage: tuple[str, ...] = ()
                else:
                    coverage_set = {
                        coverage_item
                        for admitted_item in matching
                        for coverage_item in admitted_item.coverage
                    }
                    satisfied = requirement.required_coverage <= coverage_set and bool(matching)
                    result_refs = tuple(
                        AdmittedEvidenceRef(
                            admitted_item.admitted_evidence_id, authority_version
                        ).serialized()
                        for admitted_item in sorted(
                            matching, key=lambda item: item.admitted_evidence_id
                        )
                    )
                    coverage = tuple(sorted(coverage_set))
                    admitted_refs.extend(result_refs)
                    if requirement.freshness_policy.kind is FreshnessPolicyKind.TIME_WINDOW:
                        for admitted_item in matching:
                            candidate_row = await session.get(
                                EvidenceCandidateRow, admitted_item.candidate_id
                            )
                            if (
                                candidate_row is not None
                                and requirement.freshness_policy.max_age_seconds is not None
                            ):
                                observed = datetime.fromisoformat(
                                    str(candidate_row.payload["observed_at"])
                                ).astimezone(UTC)
                                expiry_candidates.append(
                                    observed
                                    + timedelta(
                                        seconds=requirement.freshness_policy.max_age_seconds
                                    )
                                )
                all_satisfied = all_satisfied and satisfied
                results.append(
                    EvidenceRequirementSatisfaction(
                        requirement.ref.serialized(),
                        RequirementSatisfaction.SATISFIED
                        if satisfied
                        else RequirementSatisfaction.UNSATISFIED,
                        result_refs,
                        coverage,
                    )
                )
            ordered_admitted = tuple(sorted(set(admitted_refs)))
            admitted_root = canonical_hash(
                [
                    (item.requirement_ref, list(item.admitted_evidence_refs), list(item.coverage))
                    for item in results
                ]
            )
            identity = canonical_hash(
                {
                    "run": work_run_id,
                    "state": [observed_state.value, observed_state_version],
                    "checkpoint": checkpoint_ref.serialized(),
                    "set": checkpoint_row.requirement_set_ref,
                    "subset_root": subset_root,
                    "admitted_root": admitted_root,
                    "authority_revision": authority_revision,
                    "outcome": "SATISFIED" if all_satisfied else "UNSATISFIED",
                }
            )
            evaluation = EvidenceSetEvaluation(
                f"evidence-set-evaluation-{identity}",
                "p1-6-set-evaluation-v1",
                run.task_contract_id,
                run.task_contract_version,
                work_run_id,
                observed_state,
                observed_state_version,
                checkpoint_ref,
                requirement_set.requirement_set_id,
                requirement_set.requirement_set_version,
                requirement_set.requirement_root_hash,
                tuple(item.ref.serialized() for item in applicable),
                subset_root,
                tuple(results),
                admitted_root,
                authority_revision,
                EvidenceSetOutcome.SATISFIED if all_satisfied else EvidenceSetOutcome.UNSATISFIED,
                evaluated_at,
            )
            existing_eval = await session.get(EvidenceSetEvaluationRow, evaluation.evaluation_id)
            if existing_eval is None:
                session.add(_set_evaluation_row(evaluation))
                await session.flush()
            elif existing_eval.payload != _set_evaluation_payload(evaluation):
                raise EvidenceAuthorityConflictError("set evaluation identity conflict")
            if not all_satisfied:
                return evaluation, None
            attestation = EvidenceSetSatisfactionAttestation(
                f"evidence-set-attestation-{identity}",
                "p1-6-attestation-v1",
                evaluation.evaluation_id,
                evaluation.evaluation_version,
                run.task_contract_id,
                run.task_contract_version,
                work_run_id,
                observed_state,
                observed_state_version,
                checkpoint_ref,
                checkpoint.fingerprint,
                checkpoint.target_state,
                checkpoint.transition_purpose_id,
                checkpoint.transition_purpose_version,
                requirement_set.requirement_set_id,
                requirement_set.requirement_set_version,
                requirement_set.requirement_root_hash,
                evaluation.ordered_applicable_requirement_refs,
                subset_root,
                ordered_admitted,
                admitted_root,
                True,
                authority_version,
                authority_revision,
                evaluated_at,
                min(expiry_candidates) if expiry_candidates else None,
                authority_id,
                authority_version,
            )
            existing_attestation = await session.scalar(
                select(EvidenceSetAttestationRow).where(
                    EvidenceSetAttestationRow.serialized_ref == attestation.serialized_ref
                )
            )
            if existing_attestation is None:
                session.add(_attestation_row(attestation))
            elif existing_attestation.payload != _attestation_payload(attestation):
                raise EvidenceAuthorityConflictError("attestation identity conflict")
            return evaluation, attestation

    async def load_effective_attestation(
        self, serialized_ref: str, *, now: datetime | None = None
    ) -> EvidenceSetSatisfactionAttestation | None:
        async with self._session_factory() as session, session.begin():
            return await self.load_effective_attestation_in_session(
                session, serialized_ref, now=now
            )

    async def load_effective_attestation_in_session(
        self,
        session: AsyncSession,
        serialized_ref: str,
        *,
        now: datetime | None = None,
    ) -> EvidenceSetSatisfactionAttestation | None:
        """Reload current P1-6 truth inside a caller-owned shared run transaction."""
        current_time = (now or datetime.now(UTC)).astimezone(UTC)
        row = await session.scalar(
            select(EvidenceSetAttestationRow).where(
                EvidenceSetAttestationRow.serialized_ref == serialized_ref
            )
        )
        if row is None or await _has_invalidating_event(session, serialized_ref):
            return None
        value = _attestation_from_row(row)
        if value.expires_at is not None and value.expires_at <= current_time:
            return None
        evaluation_row = await session.get(
            EvidenceSetEvaluationRow, value.evidence_set_evaluation_id
        )
        run = await session.get(WorkRunRow, value.work_run_id)
        if (
            evaluation_row is None
            or evaluation_row.outcome != EvidenceSetOutcome.SATISFIED.value
            or run is None
            or run.workflow_state != value.source_state.value
            or run.state_version != value.state_version
            or row.evidence_authority_revision != value.evidence_authority_revision
            or evaluation_row.evidence_authority_revision != value.evidence_authority_revision
            or evaluation_row.full_requirement_root_hash != value.full_requirement_root_hash
            or evaluation_row.checkpoint_subset_root_hash != value.checkpoint_subset_root_hash
            or evaluation_row.admitted_ref_root_hash != value.admitted_ref_root_hash
        ):
            raise EvidenceAuthorityConflictError(
                "attestation projection/provenance is inconsistent"
            )
        await _lock(
            session,
            f"evidence-task:{run.task_contract_id}:{run.task_contract_version}",
        )
        current_revision = await _current_authority_revision(
            session,
            task_contract_id=run.task_contract_id,
            task_contract_version=run.task_contract_version,
            work_run_id=run.work_run_id,
        )
        if current_revision != value.evidence_authority_revision:
            return None
        task_sets = tuple(
            await session.scalars(
                select(EvidenceRequirementSetRow).where(
                    EvidenceRequirementSetRow.task_contract_id == run.task_contract_id,
                    EvidenceRequirementSetRow.task_contract_version == run.task_contract_version,
                )
            )
        )
        current_sets: list[EvidenceRequirementSetRow] = []
        for set_row in task_sets:
            if set_row.payload.get("revoked_at") is None and not await _has_invalidating_event(
                session, set_row.requirement_set_ref
            ):
                current_sets.append(set_row)
        if len(current_sets) != 1:
            raise EvidenceAuthorityConflictError(
                "attestation current RequirementSet authority is missing or ambiguous"
            )
        current_set = current_sets[0]
        expected_set_ref = _set_ref(value.requirement_set_id, value.requirement_set_version)
        if current_set.requirement_set_ref != expected_set_ref:
            return None
        if current_set.requirement_root_hash != value.full_requirement_root_hash:
            raise EvidenceAuthorityConflictError("attestation RequirementSet root mismatch")
        checkpoint_row = await session.get(EvidenceCheckpointRow, value.checkpoint_ref.serialized())
        if checkpoint_row is None:
            raise EvidenceAuthorityConflictError("attestation checkpoint is missing")
        if (
            checkpoint_row.requirement_set_ref != expected_set_ref
            or checkpoint_row.fingerprint != value.checkpoint_fingerprint
            or checkpoint_row.payload.get("revoked_at") is not None
            or await _has_invalidating_event(session, checkpoint_row.checkpoint_ref)
        ):
            return None
        applicable_rows: list[EvidenceRequirementRow] = []
        for requirement_ref in value.ordered_applicable_requirement_refs:
            requirement_row = await session.get(EvidenceRequirementRow, requirement_ref)
            if requirement_row is None:
                raise EvidenceAuthorityConflictError(
                    "attestation applicable requirement is missing"
                )
            if (
                requirement_row.requirement_set_ref != expected_set_ref
                or requirement_row.payload.get("revoked_at") is not None
                or await _has_invalidating_event(session, requirement_ref)
            ):
                return None
            applicable_rows.append(requirement_row)
        current_subset_root = canonical_hash(
            [(item.requirement_ref, item.fingerprint) for item in applicable_rows]
        )
        if current_subset_root != value.checkpoint_subset_root_hash:
            raise EvidenceAuthorityConflictError(
                "attestation current requirement subset root mismatch"
            )
        for admitted_ref in value.ordered_admitted_evidence_refs:
            if await _has_invalidating_event(session, admitted_ref):
                return None
            if await _admitted_by_ref(session, admitted_ref) is None:
                raise EvidenceAuthorityConflictError(
                    "attestation references missing admitted evidence"
                )
        return value


async def verify_historical_set_attestation_provenance(
    session: AsyncSession,
    serialized_ref: str,
) -> EvidenceSetSatisfactionAttestation:
    """Verify immutable P1-6 set-attestation issuance, not current effectiveness."""
    rows = tuple(
        await session.scalars(
            select(EvidenceSetAttestationRow).where(
                EvidenceSetAttestationRow.serialized_ref == serialized_ref
            )
        )
    )
    if not rows:
        raise HistoricalEvidenceProvenanceError(
            "evidence set attestation provenance is missing", incomplete=True
        )
    if len(rows) != 1:
        raise HistoricalEvidenceProvenanceError("evidence set attestation provenance is ambiguous")
    row = rows[0]
    payload = row.payload
    exact_attestation_keys = {
        "attestation_version",
        "evidence_set_evaluation_id",
        "evaluation_version",
        "task_contract_id",
        "task_contract_version",
        "work_run_id",
        "source_state",
        "state_version",
        "checkpoint_ref",
        "checkpoint_fingerprint",
        "target_state",
        "transition_purpose_id",
        "transition_purpose_version",
        "requirement_set_id",
        "requirement_set_version",
        "full_requirement_root_hash",
        "ordered_applicable_requirement_refs",
        "checkpoint_subset_root_hash",
        "ordered_admitted_evidence_refs",
        "admitted_ref_root_hash",
        "satisfied",
        "evidence_authority_version",
        "evidence_authority_revision",
        "issuer_id",
        "issuer_version",
    }
    if (
        not isinstance(payload, dict)
        or set(payload) != exact_attestation_keys
        or type(payload.get("state_version")) is not int
        or type(payload.get("evidence_authority_revision")) is not int
        or type(payload.get("satisfied")) is not bool
        or payload.get("satisfied") is not True
        or not isinstance(payload.get("ordered_applicable_requirement_refs"), list)
        or not isinstance(payload.get("ordered_admitted_evidence_refs"), list)
    ):
        raise HistoricalEvidenceProvenanceError("evidence set attestation payload is non-canonical")
    try:
        value = _attestation_from_row(row)
    except (EvidenceAuthorityConflictError, KeyError, TypeError, ValueError) as exc:
        raise HistoricalEvidenceProvenanceError(
            "evidence set attestation contains malformed immutable values"
        ) from exc
    if (
        row.attestation_id != value.attestation_id
        or row.attestation_version != value.attestation_version
        or row.serialized_ref != value.serialized_ref
        or row.evidence_set_evaluation_id != value.evidence_set_evaluation_id
        or row.work_run_id != value.work_run_id
        or row.checkpoint_ref != value.checkpoint_ref.serialized()
        or row.state_version != value.state_version
        or row.evidence_authority_revision != value.evidence_authority_revision
        or _aware(row.issued_at) != value.issued_at
        or (_aware(row.expires_at) if row.expires_at else None) != value.expires_at
        or payload != _attestation_payload(value)
        or not value.issuer_id
        or not value.issuer_version
        or value.evidence_authority_version != value.issuer_version
    ):
        raise HistoricalEvidenceProvenanceError(
            "evidence set attestation row and immutable payload disagree"
        )

    checkpoint, requirement_set, requirements = await _historical_authority_graph(session, value)
    applicable = tuple(
        item
        for item in requirements
        if value.checkpoint_ref.serialized() in item.applicable_checkpoint_refs
    )
    expected_full_root = canonical_hash(
        [(item.ref.serialized(), item.fingerprint) for item in requirements]
    )
    expected_subset_root = canonical_hash(
        [(item.ref.serialized(), item.fingerprint) for item in applicable]
    )
    expected_applicable_refs = tuple(item.ref.serialized() for item in applicable)
    if (
        checkpoint.fingerprint != value.checkpoint_fingerprint
        or requirement_set.requirement_root_hash != expected_full_root
        or value.full_requirement_root_hash != expected_full_root
        or value.ordered_applicable_requirement_refs != expected_applicable_refs
        or value.checkpoint_subset_root_hash != expected_subset_root
    ):
        raise HistoricalEvidenceProvenanceError(
            "evidence set attestation canonical checkpoint/set roots disagree"
        )

    evaluation_rows = tuple(
        await session.scalars(
            select(EvidenceSetEvaluationRow).where(
                EvidenceSetEvaluationRow.evaluation_id == value.evidence_set_evaluation_id
            )
        )
    )
    if not evaluation_rows:
        raise HistoricalEvidenceProvenanceError(
            "evidence set evaluation provenance is missing", incomplete=True
        )
    if len(evaluation_rows) != 1:
        raise HistoricalEvidenceProvenanceError("evidence set evaluation provenance is ambiguous")
    evaluation = evaluation_rows[0]
    evaluation_payload = evaluation.payload
    exact_evaluation_keys = {
        "evaluation_version",
        "task_contract_id",
        "task_contract_version",
        "work_run_id",
        "source_state",
        "state_version",
        "checkpoint_ref",
        "requirement_set_id",
        "requirement_set_version",
        "full_requirement_root_hash",
        "ordered_applicable_requirement_refs",
        "checkpoint_subset_root_hash",
        "requirement_results",
        "admitted_ref_root_hash",
        "evidence_authority_revision",
        "outcome",
    }
    if (
        not isinstance(evaluation_payload, dict)
        or set(evaluation_payload) != exact_evaluation_keys
        or type(evaluation_payload.get("state_version")) is not int
        or type(evaluation_payload.get("evidence_authority_revision")) is not int
        or not isinstance(evaluation_payload.get("ordered_applicable_requirement_refs"), list)
        or not isinstance(evaluation_payload.get("requirement_results"), list)
    ):
        raise HistoricalEvidenceProvenanceError("evidence set evaluation payload is non-canonical")
    requirement_results = _items(evaluation_payload["requirement_results"])
    if any(
        not isinstance(item, dict)
        or set(item) != {"requirement_ref", "outcome", "admitted_evidence_refs", "coverage"}
        or item.get("outcome") != RequirementSatisfaction.SATISFIED.value
        or not isinstance(item.get("requirement_ref"), str)
        or not isinstance(item.get("admitted_evidence_refs"), list)
        or not isinstance(item.get("coverage"), list)
        for item in requirement_results
    ):
        raise HistoricalEvidenceProvenanceError(
            "satisfied evidence set evaluation contains an invalid requirement result"
        )
    if (
        evaluation.evaluation_version != value.evaluation_version
        or evaluation.work_run_id != value.work_run_id
        or evaluation.source_state != value.source_state.value
        or evaluation.state_version != value.state_version
        or evaluation.checkpoint_ref != value.checkpoint_ref.serialized()
        or evaluation.requirement_set_ref
        != _set_ref(value.requirement_set_id, value.requirement_set_version)
        or evaluation.outcome != EvidenceSetOutcome.SATISFIED.value
        or evaluation.full_requirement_root_hash != value.full_requirement_root_hash
        or evaluation.checkpoint_subset_root_hash != value.checkpoint_subset_root_hash
        or evaluation.admitted_ref_root_hash != value.admitted_ref_root_hash
        or evaluation.evidence_authority_revision != value.evidence_authority_revision
        or _aware(evaluation.evaluated_at) != value.issued_at
        or evaluation_payload.get("evaluation_version") != evaluation.evaluation_version
        or evaluation_payload.get("task_contract_id") != value.task_contract_id
        or evaluation_payload.get("task_contract_version") != value.task_contract_version
        or evaluation_payload.get("work_run_id") != evaluation.work_run_id
        or evaluation_payload.get("source_state") != evaluation.source_state
        or evaluation_payload.get("state_version") != evaluation.state_version
        or evaluation_payload.get("checkpoint_ref") != evaluation.checkpoint_ref
        or evaluation_payload.get("requirement_set_id") != value.requirement_set_id
        or evaluation_payload.get("requirement_set_version") != value.requirement_set_version
        or evaluation_payload.get("full_requirement_root_hash")
        != evaluation.full_requirement_root_hash
        or evaluation_payload.get("ordered_applicable_requirement_refs")
        != list(value.ordered_applicable_requirement_refs)
        or evaluation_payload.get("checkpoint_subset_root_hash")
        != evaluation.checkpoint_subset_root_hash
        or evaluation_payload.get("admitted_ref_root_hash") != evaluation.admitted_ref_root_hash
        or evaluation_payload.get("evidence_authority_revision")
        != evaluation.evidence_authority_revision
        or evaluation_payload.get("outcome") != EvidenceSetOutcome.SATISFIED.value
    ):
        raise HistoricalEvidenceProvenanceError(
            "evidence set attestation and immutable SATISFIED evaluation disagree"
        )

    canonical_results = await _historical_requirement_results(
        session,
        value=value,
        checkpoint=checkpoint,
        requirement_set=requirement_set,
        applicable=applicable,
        raw_results=requirement_results,
    )
    expected_admitted_root = canonical_hash(
        [
            (
                item.requirement_ref,
                list(item.admitted_evidence_refs),
                list(item.coverage),
            )
            for item in canonical_results
        ]
    )
    expected_ordered_admitted_refs = tuple(
        sorted(
            {
                admitted_ref
                for item in canonical_results
                for admitted_ref in item.admitted_evidence_refs
            }
        )
    )
    if (
        evaluation.full_requirement_root_hash != expected_full_root
        or evaluation_payload["full_requirement_root_hash"] != expected_full_root
        or tuple(
            str(item) for item in _items(evaluation_payload["ordered_applicable_requirement_refs"])
        )
        != expected_applicable_refs
        or evaluation.checkpoint_subset_root_hash != expected_subset_root
        or evaluation_payload["checkpoint_subset_root_hash"] != expected_subset_root
        or evaluation.admitted_ref_root_hash != expected_admitted_root
        or evaluation_payload["admitted_ref_root_hash"] != expected_admitted_root
        or value.admitted_ref_root_hash != expected_admitted_root
        or value.ordered_admitted_evidence_refs != expected_ordered_admitted_refs
    ):
        raise HistoricalEvidenceProvenanceError(
            "evidence set evaluation canonical result/admitted roots disagree"
        )

    expected_identity = canonical_hash(
        {
            "run": evaluation.work_run_id,
            "state": [evaluation.source_state, evaluation.state_version],
            "checkpoint": evaluation.checkpoint_ref,
            "set": evaluation.requirement_set_ref,
            "subset_root": expected_subset_root,
            "admitted_root": expected_admitted_root,
            "authority_revision": evaluation.evidence_authority_revision,
            "outcome": EvidenceSetOutcome.SATISFIED.value,
        }
    )
    if (
        evaluation.evaluation_id != f"evidence-set-evaluation-{expected_identity}"
        or value.attestation_id != f"evidence-set-attestation-{expected_identity}"
    ):
        raise HistoricalEvidenceProvenanceError(
            "evidence set evaluation/attestation deterministic identity is invalid"
        )
    return value


async def _historical_authority_graph(
    session: AsyncSession,
    value: EvidenceSetSatisfactionAttestation,
) -> tuple[EvidenceCheckpoint, EvidenceRequirementSet, tuple[EvidenceRequirement, ...]]:
    checkpoint_ref = value.checkpoint_ref.serialized()
    checkpoint_row = await session.get(EvidenceCheckpointRow, checkpoint_ref)
    if checkpoint_row is None:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence checkpoint is missing", incomplete=True
        )
    checkpoint_payload = checkpoint_row.payload
    if (
        not isinstance(checkpoint_payload, dict)
        or set(checkpoint_payload)
        != {
            "task_authority_id",
            "task_authority_version",
            "revoked_at",
            "supersedes_checkpoint_ref",
        }
        or not isinstance(checkpoint_payload.get("task_authority_id"), str)
        or not checkpoint_payload.get("task_authority_id")
        or not isinstance(checkpoint_payload.get("task_authority_version"), str)
        or not checkpoint_payload.get("task_authority_version")
        or not _is_optional_string(checkpoint_payload.get("revoked_at"))
        or not _is_optional_string(checkpoint_payload.get("supersedes_checkpoint_ref"))
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical evidence checkpoint payload is non-canonical"
        )
    try:
        checkpoint = _checkpoint_from_row(checkpoint_row)
    except (EvidenceAuthorityConflictError, KeyError, TypeError, ValueError) as exc:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence checkpoint contains malformed immutable values"
        ) from exc
    if (
        checkpoint.ref.serialized() != checkpoint_row.checkpoint_ref
        or checkpoint.ref.serialized() != checkpoint_ref
        or checkpoint.task_contract_id != value.task_contract_id
        or checkpoint.task_contract_version != value.task_contract_version
        or checkpoint.source_state is not value.source_state
        or checkpoint.target_state is not value.target_state
        or checkpoint.transition_purpose_id != value.transition_purpose_id
        or checkpoint.transition_purpose_version != value.transition_purpose_version
        or checkpoint.fingerprint != checkpoint_row.fingerprint
        or checkpoint.fingerprint != canonical_hash(_checkpoint_payload(checkpoint))
        or _aware(checkpoint_row.issued_at) != checkpoint.issued_at
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical evidence checkpoint immutable authority disagrees"
        )

    expected_set_ref = _set_ref(value.requirement_set_id, value.requirement_set_version)
    if (
        checkpoint_row.requirement_set_ref != expected_set_ref
        or _set_ref(checkpoint.requirement_set_id, checkpoint.requirement_set_version)
        != expected_set_ref
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical checkpoint RequirementSet relation disagrees"
        )
    set_row = await session.get(EvidenceRequirementSetRow, expected_set_ref)
    if set_row is None:
        raise HistoricalEvidenceProvenanceError(
            "historical RequirementSet is missing", incomplete=True
        )
    set_payload = set_row.payload
    if (
        not isinstance(set_payload, dict)
        or set(set_payload)
        != {
            "ordered_requirement_refs",
            "ordered_checkpoint_refs",
            "semantic_owner",
            "authority_version",
            "revoked_at",
            "supersedes_set_ref",
        }
        or not _is_string_list(set_payload.get("ordered_requirement_refs"))
        or not _is_string_list(set_payload.get("ordered_checkpoint_refs"))
        or set_payload.get("semantic_owner") != EvidenceSemanticOwner.P1_6_EVIDENCE.value
        or not isinstance(set_payload.get("authority_version"), str)
        or not set_payload.get("authority_version")
        or not _is_optional_string(set_payload.get("revoked_at"))
        or not _is_optional_string(set_payload.get("supersedes_set_ref"))
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical RequirementSet payload is non-canonical"
        )
    try:
        requirement_set = _set_from_row(set_row)
    except (EvidenceAuthorityConflictError, KeyError, TypeError, ValueError) as exc:
        raise HistoricalEvidenceProvenanceError(
            "historical RequirementSet contains malformed immutable values"
        ) from exc
    if (
        set_row.requirement_set_ref != expected_set_ref
        or _set_ref(
            requirement_set.requirement_set_id,
            requirement_set.requirement_set_version,
        )
        != expected_set_ref
        or requirement_set.task_contract_id != value.task_contract_id
        or requirement_set.task_contract_version != value.task_contract_version
        or requirement_set.semantic_owner is not EvidenceSemanticOwner.P1_6_EVIDENCE
        or checkpoint_ref not in requirement_set.ordered_checkpoint_refs
        or len(requirement_set.ordered_requirement_refs)
        != len(set(requirement_set.ordered_requirement_refs))
        or len(requirement_set.ordered_checkpoint_refs)
        != len(set(requirement_set.ordered_checkpoint_refs))
        or set_row.fingerprint != requirement_set.fingerprint
        or set_row.fingerprint != canonical_hash(_set_payload(requirement_set))
        or _aware(set_row.issued_at) != requirement_set.issued_at
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical RequirementSet immutable authority disagrees"
        )

    requirement_rows = tuple(
        await session.scalars(
            select(EvidenceRequirementRow).where(
                EvidenceRequirementRow.requirement_set_ref == expected_set_ref
            )
        )
    )
    rows_by_ref = {item.requirement_ref: item for item in requirement_rows}
    if len(rows_by_ref) != len(requirement_rows) or set(rows_by_ref) != set(
        requirement_set.ordered_requirement_refs
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical RequirementSet definitions are incomplete or ambiguous",
            incomplete=True,
        )
    requirements: list[EvidenceRequirement] = []
    expected_obligations = {
        EvidenceRequirementProfile.EXECUTOR_REQUIRED: RequirementObligation.REQUIRED,
        EvidenceRequirementProfile.REUSE_ALLOWED: RequirementObligation.REQUIRED,
        EvidenceRequirementProfile.HUMAN_OWNED: RequirementObligation.REQUIRED,
        EvidenceRequirementProfile.NOT_REQUIRED: RequirementObligation.NOT_REQUIRED,
        EvidenceRequirementProfile.FORBIDDEN: RequirementObligation.FORBIDDEN,
    }
    for requirement_ref in requirement_set.ordered_requirement_refs:
        requirement_row = rows_by_ref[requirement_ref]
        payload = requirement_row.payload
        if (
            not isinstance(payload, dict)
            or not _historical_requirement_payload_shape_valid(requirement_row)
            or any(
                not _is_string_list(payload.get(key))
                for key in (
                    "applicable_checkpoint_refs",
                    "allowed_issuer_types",
                    "allowed_issuer_ids",
                    "allowed_human_categories",
                    "allowed_content_kinds",
                    "required_coverage",
                    "compatible_requirement_refs",
                )
            )
            or type(payload.get("reuse_maximum")) is not int
            or type(payload.get("public_export_allowed")) is not bool
            or any(
                not isinstance(payload.get(key), str) or not payload.get(key)
                for key in (
                    "task_contract_id",
                    "task_contract_version",
                    "evidence_type_id",
                    "evidence_type_version",
                    "schema_id",
                    "schema_version",
                    "subject_id",
                    "scope_id",
                    "freshness_kind",
                    "maximum_sensitivity",
                )
            )
            or not _is_optional_string(payload.get("resource_id"))
            or not _is_optional_int(payload.get("freshness_max_age_seconds"))
            or not _is_optional_string(payload.get("freshness_config_version"))
            or not _is_optional_string(payload.get("revoked_at"))
            or not _is_optional_string(payload.get("supersedes_requirement_ref"))
        ):
            raise HistoricalEvidenceProvenanceError(
                "historical EvidenceRequirement payload is non-canonical"
            )
        try:
            requirement = _requirement_from_row(requirement_row)
        except (EvidenceAuthorityConflictError, KeyError, TypeError, ValueError) as exc:
            raise HistoricalEvidenceProvenanceError(
                "historical EvidenceRequirement contains malformed immutable values"
            ) from exc
        if (
            requirement.ref.serialized() != requirement_ref
            or requirement_row.requirement_set_ref != expected_set_ref
            or requirement.task_contract_id != value.task_contract_id
            or requirement.task_contract_version != value.task_contract_version
            or requirement.requirement_set_id != value.requirement_set_id
            or requirement.requirement_set_version != value.requirement_set_version
            or requirement.semantic_owner is not EvidenceSemanticOwner.P1_6_EVIDENCE
            or requirement.obligation is not expected_obligations[requirement.profile]
            or requirement_row.profile != requirement.profile.value
            or requirement_row.obligation != requirement.obligation.value
            or requirement_row.fingerprint != requirement.fingerprint
            or requirement_row.fingerprint != canonical_hash(_requirement_payload(requirement))
            or _aware(requirement_row.issued_at) != requirement.issued_at
        ):
            raise HistoricalEvidenceProvenanceError(
                "historical EvidenceRequirement immutable authority disagrees"
            )
        requirements.append(requirement)

    requirement_values = tuple(requirements)
    expected_full_root = canonical_hash(
        [(item.ref.serialized(), item.fingerprint) for item in requirement_values]
    )
    if (
        set_row.requirement_root_hash != requirement_set.requirement_root_hash
        or set_row.requirement_root_hash != expected_full_root
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical RequirementSet canonical requirement root disagrees"
        )
    return checkpoint, requirement_set, requirement_values


async def _historical_requirement_results(
    session: AsyncSession,
    *,
    value: EvidenceSetSatisfactionAttestation,
    checkpoint: EvidenceCheckpoint,
    requirement_set: EvidenceRequirementSet,
    applicable: tuple[EvidenceRequirement, ...],
    raw_results: tuple[object, ...],
) -> tuple[EvidenceRequirementSatisfaction, ...]:
    result_requirements = tuple(
        item for item in applicable if item.profile is not EvidenceRequirementProfile.NOT_REQUIRED
    )
    expected_refs = tuple(item.ref.serialized() for item in result_requirements)
    actual_refs = tuple(
        str(item["requirement_ref"]) for item in raw_results if isinstance(item, dict)
    )
    if actual_refs != expected_refs:
        raise HistoricalEvidenceProvenanceError(
            "historical SATISFIED result requirement set/order disagrees"
        )

    canonical_results: list[EvidenceRequirementSatisfaction] = []
    for requirement, raw in zip(result_requirements, raw_results, strict=True):
        if not isinstance(raw, dict):
            raise HistoricalEvidenceProvenanceError(
                "historical requirement result payload is non-canonical"
            )
        admitted_raw = raw["admitted_evidence_refs"]
        coverage_raw = raw["coverage"]
        if not _is_string_list(admitted_raw) or not _is_string_list(coverage_raw):
            raise HistoricalEvidenceProvenanceError(
                "historical requirement result list is non-canonical"
            )
        admitted_refs = tuple(admitted_raw)
        coverage = tuple(coverage_raw)
        if admitted_refs != tuple(sorted(set(admitted_refs))) or coverage != tuple(
            sorted(set(coverage))
        ):
            raise HistoricalEvidenceProvenanceError(
                "historical requirement result ordering/uniqueness is non-canonical"
            )
        if requirement.profile is EvidenceRequirementProfile.FORBIDDEN:
            if admitted_refs or coverage:
                raise HistoricalEvidenceProvenanceError(
                    "historical FORBIDDEN result contains admitted authority"
                )
        elif not admitted_refs:
            raise HistoricalEvidenceProvenanceError(
                "historical required SATISFIED result lacks admitted evidence"
            )
        for admitted_ref in admitted_refs:
            await _verify_historical_admitted_ref(
                session,
                serialized_ref=admitted_ref,
                value=value,
                checkpoint=checkpoint,
                requirement_set=requirement_set,
                requirement=requirement,
            )
        canonical_results.append(
            EvidenceRequirementSatisfaction(
                requirement.ref.serialized(),
                RequirementSatisfaction.SATISFIED,
                admitted_refs,
                coverage,
            )
        )
    return tuple(canonical_results)


async def _verify_historical_admitted_ref(
    session: AsyncSession,
    *,
    serialized_ref: str,
    value: EvidenceSetSatisfactionAttestation | None = None,
    checkpoint: EvidenceCheckpoint | None = None,
    requirement_set: EvidenceRequirementSet | None = None,
    requirement: EvidenceRequirement | None = None,
    visited_admitted_refs: frozenset[str] = frozenset(),
) -> AdmittedEvidence:
    if serialized_ref in visited_admitted_refs:
        raise HistoricalEvidenceProvenanceError(
            "historical prior-admission authority graph contains a cycle"
        )
    visited = visited_admitted_refs | {serialized_ref}
    authority_version = (
        value.evidence_authority_version if value is not None else EVIDENCE_AUTHORITY_VERSION
    )
    parts = serialized_ref.split(":", 2)
    if (
        len(parts) != 3
        or parts[0] != "p1-6-admitted"
        or parts[1] != authority_version
        or not parts[2]
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical admitted evidence ref format/version is invalid"
        )
    row = await session.get(AdmittedEvidenceRow, parts[2])
    if row is None:
        raise HistoricalEvidenceProvenanceError(
            "historical admitted evidence is missing", incomplete=True
        )
    decision_row = await session.get(EvidenceAdmissionDecisionRow, row.decision_id)
    if decision_row is None:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence admission decision is missing", incomplete=True
        )
    request_row = await session.get(EvidenceAdmissionRequestRow, decision_row.admission_request_id)
    if request_row is None:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence admission request is missing", incomplete=True
        )
    (
        derived_checkpoint,
        derived_set,
        derived_requirement,
    ) = await _historical_request_authority_graph(session, request_row)
    if checkpoint is None:
        checkpoint = derived_checkpoint
    if requirement_set is None:
        requirement_set = derived_set
    if requirement is None:
        requirement = derived_requirement
    if (
        checkpoint.ref != derived_checkpoint.ref
        or requirement_set.requirement_set_id != derived_set.requirement_set_id
        or requirement_set.requirement_set_version != derived_set.requirement_set_version
        or requirement.ref != derived_requirement.ref
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical admitted evidence authority graph context disagrees"
        )
    try:
        admitted = _admitted_from_row(row)
    except (EvidenceAuthorityConflictError, KeyError, TypeError, ValueError) as exc:
        raise HistoricalEvidenceProvenanceError(
            "historical admitted evidence contains malformed immutable values"
        ) from exc
    if (
        AdmittedEvidenceRef(admitted.admitted_evidence_id, authority_version).serialized()
        != serialized_ref
        or admitted.admitted_evidence_id != row.admitted_evidence_id
        or (value is not None and admitted.work_run_id != value.work_run_id)
        or (
            value is not None
            and admitted.checkpoint_ref.serialized() != value.checkpoint_ref.serialized()
        )
        or admitted.requirement_ref != requirement.ref
        or (value is not None and admitted.task_contract_id != value.task_contract_id)
        or (value is not None and admitted.task_contract_version != value.task_contract_version)
        or admitted.work_run_id != row.work_run_id
        or admitted.checkpoint_ref.serialized() != row.checkpoint_ref
        or row.content_hash != admitted.content_ref.content_hash
        or row.coverage != list(admitted.coverage)
        or row.payload != _admitted_row(admitted).payload
        or _aware(row.admitted_at) != admitted.admitted_at
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical admitted evidence immutable binding disagrees"
        )
    candidate = await _historical_candidate_from_row(session, row.candidate_id)
    request, evaluation, decision = await _historical_admission_chain(
        session,
        admitted_row=row,
        candidate=candidate,
        requirement=requirement,
        requirement_set=requirement_set,
        checkpoint=checkpoint,
    )
    if (
        (value is not None and request.observed_state is not value.source_state)
        or (value is not None and request.observed_state_version != value.state_version)
        or admitted.decision_id != decision.decision_id
        or admitted.candidate_ref
        != EvidenceCandidateRef(
            candidate.candidate_id,
            candidate.candidate_version,
            candidate.candidate_fingerprint,
        )
        or admitted.requirement_ref != request.requirement_ref
        or admitted.task_contract_id != request.task_contract_id
        or admitted.task_contract_version != request.task_contract_version
        or admitted.work_run_id != request.work_run_id
        or admitted.checkpoint_ref != request.checkpoint_ref
        or admitted.content_ref != candidate.content_ref
        or admitted.coverage != tuple(sorted(candidate.coverage))
        or admitted.admitted_at != decision.decided_at
        or evaluation.evaluated_at != decision.decided_at
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical admitted evidence issuance output disagrees"
        )
    await _verify_historical_candidate_producer(
        session,
        candidate=candidate,
        requirement=requirement,
        admitted=admitted,
        visited_admitted_refs=visited,
    )
    return admitted


async def _historical_candidate_from_row(
    session: AsyncSession, candidate_id: str
) -> EvidenceCandidate:
    row = await session.get(EvidenceCandidateRow, candidate_id)
    if row is None:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence candidate is missing", incomplete=True
        )
    payload = row.payload
    exact_keys = {
        "issuer",
        "producer_work_run_id",
        "execution_attempt_id",
        "operation_id",
        "observed_state",
        "observed_state_version",
        "subject_id",
        "scope_id",
        "resource_id",
        "evidence_type_id",
        "evidence_type_version",
        "content_ref",
        "observed_at",
        "coverage",
        "producer_attestation_ref",
        "human_producer_category",
        "human_ingress_record_ref",
        "prior_admitted_evidence_ref",
        "config_version",
    }
    if not isinstance(payload, dict) or set(payload) != exact_keys:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence candidate payload is non-canonical"
        )
    issuer_payload = payload["issuer"]
    content_payload = payload["content_ref"]
    coverage_payload = payload["coverage"]
    if (
        not isinstance(issuer_payload, dict)
        or set(issuer_payload) != {"owner_type", "owner_id", "owner_version", "authority_ref"}
        or not all(isinstance(item, str) and item for item in issuer_payload.values())
        or not isinstance(content_payload, dict)
        or not _is_string_list(coverage_payload)
        or type(payload["observed_state_version"]) is not int
        or not isinstance(payload["observed_at"], str)
        or not _is_optional_string(payload["producer_work_run_id"])
        or not _is_optional_string(payload["execution_attempt_id"])
        or not _is_optional_string(payload["operation_id"])
        or not _is_optional_string(payload["resource_id"])
        or not _is_optional_string(payload["human_producer_category"])
        or not _is_optional_string(payload["human_ingress_record_ref"])
        or not _is_optional_string(payload["prior_admitted_evidence_ref"])
        or not _is_optional_string(payload["config_version"])
        or not all(
            isinstance(payload[key], str) and payload[key]
            for key in (
                "observed_state",
                "subject_id",
                "scope_id",
                "evidence_type_id",
                "evidence_type_version",
                "producer_attestation_ref",
            )
        )
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical evidence candidate payload contains malformed values"
        )
    issuer_values = cast(dict[str, str], issuer_payload)
    coverage_values = cast(list[str], coverage_payload)
    if coverage_values != sorted(set(coverage_values)):
        raise HistoricalEvidenceProvenanceError(
            "historical evidence candidate coverage is non-canonical"
        )
    try:
        checkpoint_id, checkpoint_version = row.checkpoint_ref.rsplit("@", 1)
        content = _content_from_payload(content_payload)
        observed_at = _historical_datetime(payload["observed_at"])
        human_category = (
            HumanEvidenceProducerCategory(cast(str, payload["human_producer_category"]))
            if payload["human_producer_category"] is not None
            else None
        )
        candidate = EvidenceCandidate(
            row.candidate_id,
            row.candidate_version,
            row.candidate_fingerprint,
            EvidenceOwner(
                EvidenceIssuerType(issuer_values["owner_type"]),
                issuer_values["owner_id"],
                issuer_values["owner_version"],
                issuer_values["authority_ref"],
            ),
            cast(str | None, payload["producer_work_run_id"]),
            cast(str | None, payload["execution_attempt_id"]),
            cast(str | None, payload["operation_id"]),
            row.task_contract_id,
            row.task_contract_version,
            EvidenceCheckpointRef(checkpoint_id, checkpoint_version),
            WorkflowState(cast(str, payload["observed_state"])),
            payload["observed_state_version"],
            cast(str, payload["subject_id"]),
            cast(str, payload["scope_id"]),
            cast(str | None, payload["resource_id"]),
            cast(str, payload["evidence_type_id"]),
            cast(str, payload["evidence_type_version"]),
            content,
            _aware(row.created_at),
            observed_at,
            frozenset(coverage_values),
            cast(str, payload["producer_attestation_ref"]),
            human_category,
            cast(str | None, payload["human_ingress_record_ref"]),
            cast(str | None, payload["prior_admitted_evidence_ref"]),
            cast(str | None, payload["config_version"]),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence candidate contains malformed immutable values"
        ) from exc
    expected_row = _candidate_row(candidate)
    if (
        row.candidate_id != candidate_id
        or row.candidate_fingerprint != candidate_fingerprint(candidate)
        or row.candidate_version != expected_row.candidate_version
        or row.task_contract_id != expected_row.task_contract_id
        or row.task_contract_version != expected_row.task_contract_version
        or row.checkpoint_ref != expected_row.checkpoint_ref
        or row.issuer_type != expected_row.issuer_type
        or row.sensitivity != expected_row.sensitivity
        or row.content_hash != expected_row.content_hash
        or row.human_ingress_record_ref != expected_row.human_ingress_record_ref
        or row.payload != expected_row.payload
        or _aware(row.created_at) != _aware(expected_row.created_at)
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical evidence candidate immutable authority disagrees"
        )
    if candidate.issuer.owner_type is EvidenceIssuerType.HUMAN_DIRECT_EVIDENCE:
        await _verify_historical_human_ingress(session, candidate)
    return candidate


async def _verify_historical_human_ingress(
    session: AsyncSession, candidate: EvidenceCandidate
) -> None:
    serialized_ref = candidate.human_ingress_record_ref
    if not serialized_ref:
        raise HistoricalEvidenceProvenanceError(
            "historical Human direct candidate lacks ingress provenance", incomplete=True
        )
    rows = tuple(
        await session.scalars(
            select(HumanDirectEvidenceIngressRow).where(
                HumanDirectEvidenceIngressRow.serialized_ref == serialized_ref
            )
        )
    )
    if not rows:
        raise HistoricalEvidenceProvenanceError(
            "historical Human direct ingress is missing", incomplete=True
        )
    if len(rows) != 1:
        raise HistoricalEvidenceProvenanceError("historical Human direct ingress is ambiguous")
    row = rows[0]
    if not isinstance(row.payload, dict) or set(row.payload) != {
        "candidate_id",
        "candidate_version",
        "principal_authority_id",
        "principal_authority_version",
        "authenticated_at",
        "subject_id",
        "scope_id",
        "resource_id",
        "content_ref",
        "issuer_authenticity_ref",
    }:
        raise HistoricalEvidenceProvenanceError(
            "historical Human direct ingress payload is non-canonical"
        )
    try:
        ingress = _human_ingress_from_row(row)
    except (EvidenceAuthorityConflictError, KeyError, TypeError, ValueError) as exc:
        raise HistoricalEvidenceProvenanceError(
            "historical Human direct ingress contains malformed immutable values"
        ) from exc
    expected_row = _human_ingress_row(ingress)
    if (
        ingress.ref.serialized() != serialized_ref
        or ingress.ref.fingerprint != human_ingress_fingerprint(ingress)
        or row.fingerprint != ingress.ref.fingerprint
        or row.ingress_record_id != expected_row.ingress_record_id
        or row.ingress_record_version != expected_row.ingress_record_version
        or row.ingress_authority_id != expected_row.ingress_authority_id
        or row.ingress_authority_version != expected_row.ingress_authority_version
        or row.authenticated_principal_id != expected_row.authenticated_principal_id
        or row.authenticated_session_id != expected_row.authenticated_session_id
        or row.task_contract_id != expected_row.task_contract_id
        or row.task_contract_version != expected_row.task_contract_version
        or row.work_run_id != expected_row.work_run_id
        or row.checkpoint_ref != expected_row.checkpoint_ref
        or row.evidence_type_id != expected_row.evidence_type_id
        or row.evidence_type_version != expected_row.evidence_type_version
        or row.content_hash != expected_row.content_hash
        or row.payload != expected_row.payload
        or _aware(row.provided_at) != _aware(expected_row.provided_at)
        or _aware(row.issued_at) != _aware(expected_row.issued_at)
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical Human direct ingress immutable authority disagrees"
        )
    if (
        ingress.candidate_id != candidate.candidate_id
        or ingress.candidate_version != candidate.candidate_version
        or ingress.task_contract_id != candidate.task_contract_id
        or ingress.task_contract_version != candidate.task_contract_version
        or ingress.work_run_id != candidate.producer_work_run_id
        or ingress.checkpoint_ref != candidate.checkpoint_ref
        or ingress.evidence_type_id != candidate.evidence_type_id
        or ingress.evidence_type_version != candidate.evidence_type_version
        or ingress.subject_id != candidate.subject_id
        or ingress.scope_id != candidate.scope_id
        or ingress.resource_id != candidate.resource_id
        or ingress.content_ref != candidate.content_ref
        or ingress.provided_at != candidate.observed_at
        or candidate.producer_attestation_ref != serialized_ref
        or not ingress.authenticated_principal_id
        or not ingress.authenticated_session_id
        or ingress.issuer_authenticity_ref
        != f"{ingress.ingress_authority_id}@{ingress.ingress_authority_version}"
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical Human direct ingress candidate binding disagrees"
        )


async def _historical_request_authority_graph(
    session: AsyncSession,
    request_row: EvidenceAdmissionRequestRow,
) -> tuple[EvidenceCheckpoint, EvidenceRequirementSet, EvidenceRequirement]:
    """Resolve the immutable P1-6 authority roots used by one admission request."""
    set_row = await session.get(EvidenceRequirementSetRow, request_row.requirement_set_ref)
    requirement_row = await session.get(EvidenceRequirementRow, request_row.requirement_ref)
    checkpoint_row = await session.get(EvidenceCheckpointRow, request_row.checkpoint_ref)
    if set_row is None or requirement_row is None or checkpoint_row is None:
        raise HistoricalEvidenceProvenanceError(
            "historical admission authority root is missing", incomplete=True
        )
    try:
        requirement_set = _set_from_row(set_row)
        requirement = _requirement_from_row(requirement_row)
        checkpoint = _checkpoint_from_row(checkpoint_row)
    except (EvidenceAuthorityConflictError, KeyError, TypeError, ValueError) as exc:
        raise HistoricalEvidenceProvenanceError(
            "historical admission authority root contains malformed values"
        ) from exc
    requirement_rows = tuple(
        await session.scalars(
            select(EvidenceRequirementRow).where(
                EvidenceRequirementRow.requirement_set_ref == request_row.requirement_set_ref
            )
        )
    )
    by_ref = {item.requirement_ref: item for item in requirement_rows}
    if len(by_ref) != len(requirement_rows) or set(by_ref) != set(
        requirement_set.ordered_requirement_refs
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical admission RequirementSet is incomplete or ambiguous",
            incomplete=True,
        )
    ordered_requirements: list[EvidenceRequirement] = []
    try:
        for requirement_ref in requirement_set.ordered_requirement_refs:
            item = _requirement_from_row(by_ref[requirement_ref])
            if (
                item.fingerprint != by_ref[requirement_ref].fingerprint
                or item.fingerprint != canonical_hash(_requirement_payload(item))
                or _aware(by_ref[requirement_ref].issued_at) != item.issued_at
                or item.requirement_set_id != requirement_set.requirement_set_id
                or item.requirement_set_version != requirement_set.requirement_set_version
                or item.task_contract_id != requirement_set.task_contract_id
                or item.task_contract_version != requirement_set.task_contract_version
            ):
                raise HistoricalEvidenceProvenanceError(
                    "historical admission requirement immutable authority disagrees"
                )
            ordered_requirements.append(item)
    except (EvidenceAuthorityConflictError, KeyError, TypeError, ValueError) as exc:
        raise HistoricalEvidenceProvenanceError(
            "historical admission requirement contains malformed values"
        ) from exc
    expected_root = canonical_hash(
        [(item.ref.serialized(), item.fingerprint) for item in ordered_requirements]
    )
    if (
        set_row.fingerprint != requirement_set.fingerprint
        or set_row.fingerprint != canonical_hash(_set_payload(requirement_set))
        or set_row.requirement_root_hash != expected_root
        or requirement_set.requirement_root_hash != expected_root
        or requirement_row.requirement_set_ref != request_row.requirement_set_ref
        or requirement.ref.serialized() != request_row.requirement_ref
        or requirement.fingerprint != requirement_row.fingerprint
        or checkpoint_row.requirement_set_ref != request_row.requirement_set_ref
        or checkpoint.ref.serialized() != request_row.checkpoint_ref
        or checkpoint.fingerprint != checkpoint_row.fingerprint
        or checkpoint.fingerprint != canonical_hash(_checkpoint_payload(checkpoint))
        or checkpoint.task_contract_id != requirement_set.task_contract_id
        or checkpoint.task_contract_version != requirement_set.task_contract_version
        or checkpoint.requirement_set_id != requirement_set.requirement_set_id
        or checkpoint.requirement_set_version != requirement_set.requirement_set_version
        or checkpoint.ref.serialized() not in requirement_set.ordered_checkpoint_refs
        or _aware(set_row.issued_at) != requirement_set.issued_at
        or _aware(checkpoint_row.issued_at) != checkpoint.issued_at
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical admission canonical authority root disagrees"
        )
    return checkpoint, requirement_set, requirement


async def _verify_historical_candidate_producer(
    session: AsyncSession,
    *,
    candidate: EvidenceCandidate,
    requirement: EvidenceRequirement,
    admitted: AdmittedEvidence,
    visited_admitted_refs: frozenset[str],
) -> None:
    """Verify owner-specific immutable producer authority without process tokens."""
    if (
        candidate.issuer.owner_type not in requirement.allowed_issuer_types
        or candidate.issuer.owner_id not in requirement.allowed_issuer_ids
        or candidate.evidence_type_id != requirement.evidence_type_id
        or candidate.evidence_type_version != requirement.evidence_type_version
        or candidate.content_ref.content_kind not in requirement.allowed_content_kinds
        or candidate.content_ref.schema_id != requirement.schema_id
        or candidate.content_ref.schema_version != requirement.schema_version
        or candidate.subject_id != requirement.subject_id
        or candidate.scope_id != requirement.scope_id
        or candidate.resource_id != requirement.resource_id
        or not requirement.required_coverage.issubset(candidate.coverage)
        or candidate.checkpoint_ref.serialized() not in requirement.applicable_checkpoint_refs
        or requirement.profile
        in {
            EvidenceRequirementProfile.NOT_REQUIRED,
            EvidenceRequirementProfile.FORBIDDEN,
        }
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical candidate and requirement issuer/content authority disagree"
        )
    owner_type = candidate.issuer.owner_type
    if owner_type is EvidenceIssuerType.HUMAN_P1_7:
        if (
            requirement.profile is not EvidenceRequirementProfile.HUMAN_OWNED
            or candidate.human_producer_category not in requirement.allowed_human_categories
        ):
            raise HistoricalEvidenceProvenanceError(
                "historical HUMAN_P1_7 producer category is not allowed"
            )
        await _verify_historical_p1_7_producer(session, candidate)
        return
    expected_authority_ref = f"{candidate.issuer.owner_id}@{candidate.issuer.owner_version}"
    if candidate.issuer.authority_ref != expected_authority_ref:
        raise HistoricalEvidenceProvenanceError(
            "historical candidate issuer authority ref is non-canonical"
        )
    if owner_type.value.startswith("P1_5_"):
        if requirement.profile is not EvidenceRequirementProfile.EXECUTOR_REQUIRED:
            raise HistoricalEvidenceProvenanceError(
                "historical P1-5 candidate has an invalid requirement profile"
            )
        await _verify_historical_p1_5_producer(session, candidate)
    elif owner_type is EvidenceIssuerType.PRIOR_ADMITTED_EVIDENCE:
        if requirement.profile is not EvidenceRequirementProfile.REUSE_ALLOWED:
            raise HistoricalEvidenceProvenanceError(
                "historical reuse candidate has an invalid requirement profile"
            )
        await _verify_historical_prior_admission(
            session,
            candidate=candidate,
            requirement=requirement,
            admitted=admitted,
            visited_admitted_refs=visited_admitted_refs,
        )
    elif owner_type is EvidenceIssuerType.HUMAN_DIRECT_EVIDENCE:
        if (
            requirement.profile is not EvidenceRequirementProfile.HUMAN_OWNED
            or candidate.human_producer_category
            is not HumanEvidenceProducerCategory.HUMAN_DIRECT_EVIDENCE
            or candidate.human_producer_category not in requirement.allowed_human_categories
        ):
            raise HistoricalEvidenceProvenanceError(
                "historical Human direct producer category disagrees"
            )
        # The durable ingress graph was already verified while reconstructing the candidate.
    elif owner_type in {
        EvidenceIssuerType.SYSTEM_STATIC_PROOF,
        EvidenceIssuerType.SYSTEM_BUILD_PROOF,
        EvidenceIssuerType.SYSTEM_DATABASE_OBSERVATION,
        EvidenceIssuerType.SYSTEM_RUNTIME_OBSERVATION,
    }:
        if candidate.human_producer_category is not None:
            raise HistoricalEvidenceProvenanceError(
                "historical System producer unexpectedly carries a Human category"
            )
        # Intentional System token issuers have no durable token object. The immutable
        # candidate, accepted ISSUER_AUTHORITY result, and exact requirement binding are
        # their historical issuance proof.
    else:
        raise HistoricalEvidenceProvenanceError(
            "historical candidate issuer category has no canonical verifier"
        )


async def _verify_historical_p1_5_producer(
    session: AsyncSession, candidate: EvidenceCandidate
) -> None:
    expected_kinds = {
        EvidenceIssuerType.P1_5_EXECUTION_SUBMISSION: "ExecutionSubmissionRef",
        EvidenceIssuerType.P1_5_AGENT_OUTPUT: "AgentOutputRef",
        EvidenceIssuerType.P1_5_TOOL_OUTPUT: "ToolOutputRef",
        EvidenceIssuerType.P1_5_EXECUTION_ARTIFACT: "ExecutionArtifactRef",
    }
    if (
        not candidate.producer_work_run_id
        or not candidate.execution_attempt_id
        or not candidate.producer_attestation_ref
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical P1-5 candidate lacks immutable producer binding",
            incomplete=True,
        )
    output = await session.get(ExecutionOutputRefRow, candidate.producer_attestation_ref)
    attempt = await session.get(ExecutionAttemptRow, candidate.execution_attempt_id)
    if output is None or attempt is None:
        raise HistoricalEvidenceProvenanceError(
            "historical P1-5 producer ref or attempt is missing", incomplete=True
        )
    if (
        output.output_ref_id != candidate.producer_attestation_ref
        or output.output_ref_id != candidate.content_ref.object_id
        or output.execution_attempt_id != candidate.execution_attempt_id
        or output.ref_kind != expected_kinds[candidate.issuer.owner_type]
        or output.content_hash != candidate.content_ref.content_hash
        or not output.storage_ref.startswith("private://")
        or attempt.execution_attempt_id != candidate.execution_attempt_id
        or attempt.work_run_id != candidate.producer_work_run_id
        or attempt.task_contract_id != candidate.task_contract_id
        or attempt.task_contract_version != candidate.task_contract_version
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical P1-5 immutable producer authority disagrees"
        )


async def _verify_historical_p1_7_producer(
    session: AsyncSession, candidate: EvidenceCandidate
) -> None:
    from aiscc.human.models import HumanAuthorityError, HumanAuthorityReason
    from aiscc.human.repository import verify_historical_producer_ref_in_session

    if candidate.human_producer_category is not HumanEvidenceProducerCategory.HUMAN_P1_7:
        raise HistoricalEvidenceProvenanceError("historical HUMAN_P1_7 producer category disagrees")
    try:
        producer = await verify_historical_producer_ref_in_session(
            session, candidate.producer_attestation_ref
        )
    except HumanAuthorityError as exc:
        raise HistoricalEvidenceProvenanceError(
            "historical HUMAN_P1_7 producer provenance is invalid",
            incomplete=exc.reason is HumanAuthorityReason.PROVENANCE_INCOMPLETE,
        ) from exc
    if (
        candidate.issuer.authority_ref != producer.serialized_ref
        or candidate.issuer.owner_id != producer.authority_id
        or candidate.issuer.owner_version != producer.authority_version
        or candidate.producer_work_run_id != producer.work_run_id
        or candidate.task_contract_id != producer.task_contract_id
        or candidate.task_contract_version != producer.task_contract_version
        or candidate.observed_state is not producer.source_state
        or candidate.observed_state_version != producer.state_version
        or candidate.checkpoint_ref.serialized() != producer.checkpoint_ref
        or candidate.evidence_type_id != producer.evidence_type_id
        or candidate.evidence_type_version != producer.evidence_type_version
        or candidate.subject_id != producer.subject_id
        or candidate.scope_id != producer.scope_id
        or candidate.resource_id != producer.resource_id
        or candidate.content_ref.content_hash != producer.content_hash
        or candidate.content_ref.sensitivity is not producer.sensitivity
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical HUMAN_P1_7 candidate and producer ref disagree"
        )


async def _verify_historical_prior_admission(
    session: AsyncSession,
    *,
    candidate: EvidenceCandidate,
    requirement: EvidenceRequirement,
    admitted: AdmittedEvidence,
    visited_admitted_refs: frozenset[str],
) -> None:
    prior_ref = candidate.prior_admitted_evidence_ref
    if not prior_ref or candidate.producer_attestation_ref != prior_ref:
        raise HistoricalEvidenceProvenanceError(
            "historical reuse candidate lacks exact prior admission authority",
            incomplete=True,
        )
    if (
        candidate.issuer.owner_id != "AISCC_P1_6_REUSE_AUTHORITY_V1"
        or candidate.issuer.owner_version != "p1-6-reuse-v1"
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical reuse candidate owner authority disagrees"
        )
    ledger_rows = tuple(
        await session.scalars(
            select(EvidenceReuseConsumptionRow).where(
                EvidenceReuseConsumptionRow.admitted_evidence_id == admitted.admitted_evidence_id
            )
        )
    )
    if not ledger_rows:
        raise HistoricalEvidenceProvenanceError(
            "historical reuse consumption ledger is missing", incomplete=True
        )
    if len(ledger_rows) != 1:
        raise HistoricalEvidenceProvenanceError("historical reuse consumption ledger is ambiguous")
    ledger = ledger_rows[0]
    scoped_rows = tuple(
        await session.scalars(
            select(EvidenceReuseConsumptionRow)
            .where(
                EvidenceReuseConsumptionRow.prior_admitted_evidence_ref == prior_ref,
                EvidenceReuseConsumptionRow.requirement_ref == requirement.ref.serialized(),
                EvidenceReuseConsumptionRow.work_run_id == admitted.work_run_id,
                EvidenceReuseConsumptionRow.checkpoint_ref == admitted.checkpoint_ref.serialized(),
            )
            .order_by(EvidenceReuseConsumptionRow.consumption_ordinal)
        )
    )
    if (
        ledger.consumption_id != f"reuse-{admitted.admitted_evidence_id}"
        or ledger.prior_admitted_evidence_ref != prior_ref
        or ledger.requirement_ref != requirement.ref.serialized()
        or ledger.work_run_id != admitted.work_run_id
        or ledger.checkpoint_ref != admitted.checkpoint_ref.serialized()
        or ledger.policy_maximum != requirement.reuse_maximum
        or ledger.consumption_ordinal < 1
        or ledger.consumption_ordinal > requirement.reuse_maximum
        or _aware(ledger.consumed_at) != admitted.admitted_at
        or tuple(item.consumption_ordinal for item in scoped_rows)
        != tuple(range(1, len(scoped_rows) + 1))
        or len(scoped_rows) > requirement.reuse_maximum
        or any(item.policy_maximum != requirement.reuse_maximum for item in scoped_rows)
    ):
        raise HistoricalEvidenceProvenanceError("historical reuse consumption authority disagrees")
    prior = await _verify_historical_admitted_ref(
        session,
        serialized_ref=prior_ref,
        visited_admitted_refs=visited_admitted_refs,
    )
    if (
        prior.content_ref.content_hash != candidate.content_ref.content_hash
        or prior.content_ref.object_id != candidate.content_ref.object_id
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical reuse candidate content differs from prior admission"
        )


async def _historical_admission_chain(
    session: AsyncSession,
    *,
    admitted_row: AdmittedEvidenceRow,
    candidate: EvidenceCandidate,
    requirement: EvidenceRequirement,
    requirement_set: EvidenceRequirementSet,
    checkpoint: EvidenceCheckpoint,
) -> tuple[EvidenceAdmissionRequest, EvidenceEvaluation, EvidenceAdmissionDecision]:
    decision_row = await session.get(EvidenceAdmissionDecisionRow, admitted_row.decision_id)
    if decision_row is None:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence admission decision is missing", incomplete=True
        )
    request_row = await session.get(EvidenceAdmissionRequestRow, decision_row.admission_request_id)
    if request_row is None:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence admission request is missing", incomplete=True
        )
    request = _verify_historical_admission_request(
        request_row,
        candidate=candidate,
        requirement=requirement,
        requirement_set=requirement_set,
        checkpoint=checkpoint,
        expected_work_run_id=admitted_row.work_run_id,
    )
    evaluation_rows = tuple(
        await session.scalars(
            select(EvidenceEvaluationRow).where(
                EvidenceEvaluationRow.admission_request_id == request.admission_request_id
            )
        )
    )
    if not evaluation_rows:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence evaluation is missing", incomplete=True
        )
    if len(evaluation_rows) != 1:
        raise HistoricalEvidenceProvenanceError("historical evidence evaluation is ambiguous")
    evaluation = _verify_historical_evaluation(
        evaluation_rows[0], request=request, candidate=candidate, requirement=requirement
    )
    decision_rows = tuple(
        await session.scalars(
            select(EvidenceAdmissionDecisionRow).where(
                EvidenceAdmissionDecisionRow.admission_request_id == request.admission_request_id
            )
        )
    )
    if not decision_rows:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence admission decision is missing", incomplete=True
        )
    if len(decision_rows) != 1 or decision_rows[0].decision_id != admitted_row.decision_id:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence admission decision is ambiguous"
        )
    row = decision_rows[0]
    try:
        decision = _decision_from_row(row, request_row)
    except (KeyError, TypeError, ValueError) as exc:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence admission decision contains malformed values"
        ) from exc
    if (
        row.evaluation_id != evaluation.evaluation_id
        or decision.admission_request_id != request.admission_request_id
        or decision.evaluation_id != evaluation.evaluation_id
        or decision.candidate_id != candidate.candidate_id
        or decision.requirement_ref != requirement.ref.serialized()
        or decision.requirement_set_ref
        != _set_ref(
            requirement_set.requirement_set_id,
            requirement_set.requirement_set_version,
        )
        or decision.outcome is not EvidenceAdmissionOutcome.ADMITTED
        or decision.reason is not EvidenceRejectionReason.ADMITTED
        or decision.secondary_reasons
        or decision.admitting_authority_version != EVIDENCE_AUTHORITY_VERSION
        or decision.decided_at != _aware(admitted_row.admitted_at)
        or decision.decided_at != evaluation.evaluated_at
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical evidence ADMITTED decision authority disagrees"
        )
    return request, evaluation, decision


def _verify_historical_admission_request(
    row: EvidenceAdmissionRequestRow,
    *,
    candidate: EvidenceCandidate,
    requirement: EvidenceRequirement,
    requirement_set: EvidenceRequirementSet,
    checkpoint: EvidenceCheckpoint,
    expected_work_run_id: str,
) -> EvidenceAdmissionRequest:
    payload = row.payload
    exact_keys = {
        "candidate_version",
        "candidate_fingerprint",
        "requirement_fingerprint",
        "requirement_root_hash",
        "task_contract_id",
        "task_contract_version",
        "checkpoint_fingerprint",
        "target_state",
        "transition_purpose_id",
        "transition_purpose_version",
        "requester_identity",
    }
    if (
        not isinstance(payload, dict)
        or set(payload) != exact_keys
        or not all(
            isinstance(payload[key], str) and payload[key]
            for key in (
                "candidate_version",
                "candidate_fingerprint",
                "requirement_fingerprint",
                "requirement_root_hash",
                "task_contract_id",
                "task_contract_version",
                "checkpoint_fingerprint",
                "requester_identity",
            )
        )
        or not _is_optional_string(payload["target_state"])
        or not _is_optional_string(payload["transition_purpose_id"])
        or not _is_optional_string(payload["transition_purpose_version"])
        or cast(str, payload["requester_identity"]).strip() != payload["requester_identity"]
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical evidence admission request payload is non-canonical"
        )
    try:
        observed_state = WorkflowState(row.observed_state)
        request = make_admission_request(
            admission_request_id=row.admission_request_id,
            candidate=candidate,
            requirement=requirement,
            requirement_set=requirement_set,
            checkpoint=checkpoint,
            work_run_id=row.work_run_id,
            observed_state=observed_state,
            observed_state_version=row.observed_state_version,
            requester_identity=payload["requester_identity"],
            created_at=_aware(row.created_at),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence admission request contains malformed values"
        ) from exc
    expected_row = _request_row(request)
    if (
        row.request_fingerprint != request.request_fingerprint
        or row.candidate_id != candidate.candidate_id
        or row.requirement_ref != requirement.ref.serialized()
        or row.requirement_set_ref
        != _set_ref(
            requirement_set.requirement_set_id,
            requirement_set.requirement_set_version,
        )
        or row.work_run_id != expected_work_run_id
        or row.checkpoint_ref != checkpoint.ref.serialized()
        or row.observed_state != checkpoint.source_state.value
        or row.payload != expected_row.payload
        or row.request_fingerprint != expected_row.request_fingerprint
        or request.candidate_ref.candidate_version != candidate.candidate_version
        or request.candidate_ref.candidate_fingerprint != candidate.candidate_fingerprint
        or request.requirement_fingerprint != requirement.fingerprint
        or request.requirement_root_hash != requirement_set.requirement_root_hash
        or request.checkpoint_fingerprint != checkpoint.fingerprint
        or request.task_contract_id != candidate.task_contract_id
        or request.task_contract_version != candidate.task_contract_version
        or request.target_state is not checkpoint.target_state
        or request.transition_purpose_id != checkpoint.transition_purpose_id
        or request.transition_purpose_version != checkpoint.transition_purpose_version
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical evidence admission request immutable authority disagrees"
        )
    return request


def _verify_historical_evaluation(
    row: EvidenceEvaluationRow,
    *,
    request: EvidenceAdmissionRequest,
    candidate: EvidenceCandidate,
    requirement: EvidenceRequirement,
) -> EvidenceEvaluation:
    raw_results = row.dimension_results
    if not isinstance(raw_results, list) or len(raw_results) != len(EvidenceAdmissionDimension):
        raise HistoricalEvidenceProvenanceError(
            "historical evidence evaluation dimension set is incomplete"
        )
    results: list[EvidenceDimensionResult] = []
    for raw in raw_results:
        if (
            not isinstance(raw, dict)
            or set(raw) != {"dimension", "outcome", "authority_ref", "authority_version", "reason"}
            or not all(isinstance(raw[key], str) and raw[key] for key in raw)
        ):
            raise HistoricalEvidenceProvenanceError(
                "historical evidence evaluation dimension payload is non-canonical"
            )
        try:
            results.append(
                EvidenceDimensionResult(
                    EvidenceAdmissionDimension(cast(str, raw["dimension"])),
                    EvidenceDimensionOutcome(cast(str, raw["outcome"])),
                    cast(str, raw["authority_ref"]),
                    cast(str, raw["authority_version"]),
                    cast(str, raw["reason"]),
                )
            )
        except ValueError as exc:
            raise HistoricalEvidenceProvenanceError(
                "historical evidence evaluation dimension vocabulary is invalid"
            ) from exc
    expected_dimensions = tuple(EvidenceAdmissionDimension)
    if tuple(item.dimension for item in results) != expected_dimensions:
        raise HistoricalEvidenceProvenanceError(
            "historical evidence evaluation dimensions are missing, duplicate, or unordered"
        )
    expected_outcomes = {item: EvidenceDimensionOutcome.PASS for item in EvidenceAdmissionDimension}
    if candidate.human_producer_category is None:
        expected_outcomes[EvidenceAdmissionDimension.HUMAN_PRODUCER_CATEGORY] = (
            EvidenceDimensionOutcome.NOT_APPLICABLE
        )
    if candidate.prior_admitted_evidence_ref is None:
        expected_outcomes[EvidenceAdmissionDimension.REUSE_POLICY] = (
            EvidenceDimensionOutcome.NOT_APPLICABLE
        )
    work_run_authority_ref = f"AISCC_SYSTEM_WORKRUN:{request.work_run_id}"
    work_run_authority_version = f"state-version:{request.observed_state_version}"
    expected_authorities = {
        item: ("AISCC_P1_6_POLICY", EVIDENCE_AUTHORITY_VERSION)
        for item in EvidenceAdmissionDimension
    }
    expected_authorities[EvidenceAdmissionDimension.ISSUER_AUTHORITY] = (
        candidate.issuer.authority_ref,
        EVIDENCE_AUTHORITY_VERSION,
    )
    expected_authorities[EvidenceAdmissionDimension.CONTENT_INTEGRITY] = (
        f"{candidate.content_ref.owner_id}@{candidate.content_ref.owner_version}",
        EVIDENCE_AUTHORITY_VERSION,
    )
    for dimension in (
        EvidenceAdmissionDimension.TASK_CONTRACT_BINDING,
        EvidenceAdmissionDimension.CHECKPOINT_BINDING,
        EvidenceAdmissionDimension.FRESHNESS,
    ):
        expected_authorities[dimension] = (
            work_run_authority_ref,
            work_run_authority_version,
        )
    if any(
        item.outcome is not expected_outcomes[item.dimension]
        or (item.authority_ref, item.authority_version) != expected_authorities[item.dimension]
        for item in results
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical evidence evaluation positive dimension authority disagrees"
        )
    evaluation = EvidenceEvaluation(
        row.evaluation_id,
        row.admission_request_id,
        tuple(results),
        _aware(row.evaluated_at),
        row.authority_version,
    )
    if (
        evaluation.admission_request_id != request.admission_request_id
        or evaluation.authority_version != EVIDENCE_AUTHORITY_VERSION
        or row.dimension_results != _evaluation_row(evaluation).dimension_results
    ):
        raise HistoricalEvidenceProvenanceError(
            "historical evidence evaluation immutable authority disagrees"
        )
    return evaluation


def _historical_datetime(value: object) -> datetime:
    if not isinstance(value, str):
        raise ValueError("historical authority timestamp must be a string")
    return _aware(datetime.fromisoformat(value))


_V1_REQUIREMENT_ROW_PAYLOAD_KEYS = {
    "task_contract_id",
    "task_contract_version",
    "applicable_checkpoint_refs",
    "evidence_type_id",
    "evidence_type_version",
    "allowed_issuer_types",
    "allowed_issuer_ids",
    "allowed_human_categories",
    "allowed_content_kinds",
    "schema_id",
    "schema_version",
    "subject_id",
    "scope_id",
    "resource_id",
    "freshness_kind",
    "freshness_max_age_seconds",
    "freshness_config_version",
    "required_coverage",
    "reuse_maximum",
    "compatible_requirement_refs",
    "maximum_sensitivity",
    "public_export_allowed",
    "revoked_at",
    "supersedes_requirement_ref",
}
_V2_REQUIREMENT_ROW_PAYLOAD_KEYS = _V1_REQUIREMENT_ROW_PAYLOAD_KEYS | {
    "fingerprint_schema",
    "durable_content_requirement",
    "durable_content_policy_ref",
    "durable_content_policy_fingerprint",
}


def _historical_requirement_payload_shape_valid(row: EvidenceRequirementRow) -> bool:
    payload = row.payload
    if row.fingerprint_schema == RequirementFingerprintSchema.V1.value:
        return set(payload) == _V1_REQUIREMENT_ROW_PAYLOAD_KEYS
    if row.fingerprint_schema == RequirementFingerprintSchema.V2_DURABLE_CONTENT.value:
        policy_ref = payload.get("durable_content_policy_ref")
        policy_hash = payload.get("durable_content_policy_fingerprint")
        return bool(
            set(payload) == _V2_REQUIREMENT_ROW_PAYLOAD_KEYS
            and payload.get("fingerprint_schema") == row.fingerprint_schema
            and payload.get("durable_content_requirement")
            == DurableContentRequirement.REQUIRED.value
            and isinstance(policy_ref, str)
            and policy_ref
            and isinstance(policy_hash, str)
            and len(policy_hash) == 64
            and policy_hash.lower() == policy_hash
            and all(character in "0123456789abcdef" for character in policy_hash)
        )
    return False


def _is_string_list(value: object) -> bool:
    return isinstance(value, list) and all(isinstance(item, str) for item in value)


def _is_optional_string(value: object) -> bool:
    return value is None or isinstance(value, str)


def _is_optional_int(value: object) -> bool:
    return value is None or type(value) is int


async def _lock(session: AsyncSession, key: str) -> None:
    await session.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:lock_key, 0))"),
        {"lock_key": key},
    )


async def _acquire_work_run_transaction_lock(session: AsyncSession, work_run_id: str) -> None:
    await acquire_work_run_transaction_lock(session, work_run_id)


def _authoritative_work_run_snapshot(row: WorkRunRow) -> AuthoritativeWorkRunSnapshot:
    try:
        workflow_state = WorkflowState(row.workflow_state)
    except ValueError as exc:
        raise EvidenceAuthorityConflictError(
            "authoritative WorkRun has an unknown workflow state"
        ) from exc
    return AuthoritativeWorkRunSnapshot(
        work_run_id=row.work_run_id,
        task_contract_id=row.task_contract_id,
        task_contract_version=row.task_contract_version,
        workflow_state=workflow_state,
        state_version=row.state_version,
        authority_ref=f"AISCC_SYSTEM_WORKRUN:{row.work_run_id}",
        authority_version=f"state-version:{row.state_version}",
    )


async def _persist_durable_content_and_binding(
    session: AsyncSession,
    *,
    prepared: PreparedDurableEvidenceContent,
    candidate: EvidenceCandidate,
    request: EvidenceAdmissionRequest,
    requirement: EvidenceRequirement,
    requirement_set: EvidenceRequirementSet,
    bound_at: datetime,
) -> None:
    content = prepared.content
    if candidate.content_ref != prepared.content_ref:
        raise DurableContentError(
            DurableContentErrorCode.INTEGRITY_MISMATCH,
            "candidate EvidenceContentRef differs from the prepared durable object",
        )
    if (
        requirement.fingerprint_schema
        is not RequirementFingerprintSchema.V2_DURABLE_CONTENT
        or requirement.durable_content_requirement is not DurableContentRequirement.REQUIRED
        or requirement.durable_content_policy_ref is None
        or requirement.durable_content_policy_fingerprint is None
    ):
        raise DurableContentError(
            DurableContentErrorCode.REQUIRED,
            "Requirement lacks original REQUIRED durable enrollment",
        )
    sensitivity_allowed = bool(
        content.sensitivity is EvidenceSensitivity.PUBLIC_SAFE
        or (
            content.sensitivity is EvidenceSensitivity.INTERNAL
            and requirement.maximum_sensitivity is EvidenceSensitivity.INTERNAL
        )
    )
    if (
        content.source_owner_authority_ref != candidate.issuer.authority_ref
        or content.source_owner_authority_fingerprint
        != source_owner_authority_fingerprint(candidate)
        or content.content_kind not in DURABLE_CONTENT_KINDS
        or content.content_kind not in requirement.allowed_content_kinds
        or content.canonicalization != CANONICALIZATION_V1
        or content.schema_id != requirement.schema_id
        or content.schema_version != requirement.schema_version
        or not sensitivity_allowed
        or content.retention_policy != DURABLE_CONTENT_RETENTION_POLICY
    ):
        raise DurableContentError(
            DurableContentErrorCode.SCHEMA_MISMATCH,
            "durable object differs from Requirement-enrolled owner/content policy",
        )
    _verify_durable_object_value(content, candidate.content_ref)

    existing = await session.get(EvidenceContentObjectRow, content.serialized_ref)
    if existing is None:
        conflicting_identity = await session.scalar(
            select(EvidenceContentObjectRow).where(
                EvidenceContentObjectRow.owner_id == content.owner_id,
                EvidenceContentObjectRow.owner_version == content.owner_version,
                EvidenceContentObjectRow.object_id == content.object_id,
                EvidenceContentObjectRow.object_version == content.object_version,
            )
        )
        if conflicting_identity is not None:
            raise DurableContentError(
                DurableContentErrorCode.IDENTITY_CONFLICT,
                "owner/object identity already has different immutable content",
            )
        session.add(_durable_content_row(content))
        await session.flush()
    elif _durable_content_from_row(existing) != content:
        raise DurableContentError(
            DurableContentErrorCode.IDENTITY_CONFLICT,
            "durable content identity replay differs from stored immutable payload",
        )

    content_ref_fingerprint = canonical_hash(_content_payload(candidate.content_ref))
    binding = EvidenceCandidateDurableContentBinding(
        candidate_id=candidate.candidate_id,
        candidate_version=candidate.candidate_version,
        candidate_fingerprint=candidate.candidate_fingerprint,
        durable_content_ref=content.serialized_ref,
        durable_content_payload_fingerprint=content.payload_fingerprint,
        content_ref_metadata_fingerprint=content_ref_fingerprint,
        requirement_ref=request.requirement_ref.serialized(),
        requirement_fingerprint_schema=requirement.fingerprint_schema,
        requirement_fingerprint=requirement.fingerprint,
        requirement_set_ref=(
            f"{requirement_set.requirement_set_id}@{requirement_set.requirement_set_version}"
        ),
        requirement_root_hash=requirement_set.requirement_root_hash,
        durable_content_policy_ref=requirement.durable_content_policy_ref,
        durable_content_policy_fingerprint=requirement.durable_content_policy_fingerprint,
        bound_at=bound_at,
        binding_fingerprint="",
    )
    binding = replace(
        binding, binding_fingerprint=canonical_hash(_durable_binding_payload(binding))
    )
    existing_binding = await session.get(
        EvidenceCandidateContentBindingRow, candidate.candidate_id
    )
    if existing_binding is None:
        session.add(_durable_binding_row(binding))
        await session.flush()
    elif _durable_binding_from_row(existing_binding) != binding:
        raise DurableContentError(
            DurableContentErrorCode.IDENTITY_CONFLICT,
            "candidate durable-content binding identity conflict",
        )


async def _verify_historical_content_in_session(
    session: AsyncSession,
    content_ref: EvidenceContentRef,
    *,
    expected_payload_fingerprint: str | None = None,
) -> VerifiedHistoricalContentMetadata:
    identity_key = canonical_hash(
        {
            "identity_schema": DURABLE_CONTENT_IDENTITY_SCHEMA,
            "owner_id": content_ref.owner_id,
            "owner_version": content_ref.owner_version,
            "object_id": content_ref.object_id,
            "object_version": content_ref.object_version,
        }
    )
    serialized_ref = f"p1-6-durable-content:v1:{identity_key}"
    row = await session.get(EvidenceContentObjectRow, serialized_ref)
    if row is None:
        raise DurableContentError(
            DurableContentErrorCode.MISSING,
            "durable content row is absent",
        )
    try:
        content = _durable_content_from_row(row)
        _verify_durable_object_value(content, content_ref)
    except DurableContentError:
        raise
    except (KeyError, TypeError, ValueError) as exc:
        raise DurableContentError(
            DurableContentErrorCode.INTEGRITY_MISMATCH,
            "durable content row contains malformed immutable values",
        ) from exc
    if (
        expected_payload_fingerprint is not None
        and content.payload_fingerprint != expected_payload_fingerprint
    ):
        raise DurableContentError(
            DurableContentErrorCode.INTEGRITY_MISMATCH,
            "durable content payload fingerprint differs from expected binding",
        )
    return VerifiedHistoricalContentMetadata(content)


def _historical_content_access_allowed(
    content: DurableEvidenceContentObject,
    access_grant: HistoricalContentAccessGrant,
    authority: P1_6HistoricalContentAccessAuthority | None,
) -> bool:
    return bool(authority is not None and authority.allows_historical_read(access_grant, content))


async def _verify_durable_binding_in_session(
    session: AsyncSession, row: EvidenceCandidateContentBindingRow
) -> EvidenceCandidateDurableContentBinding:
    try:
        binding = _durable_binding_from_row(row)
    except (KeyError, TypeError, ValueError) as exc:
        raise DurableContentError(
            DurableContentErrorCode.INTEGRITY_MISMATCH,
            "durable candidate binding contains malformed immutable values",
        ) from exc
    if binding.binding_fingerprint != canonical_hash(_durable_binding_payload(binding)):
        raise DurableContentError(
            DurableContentErrorCode.INTEGRITY_MISMATCH,
            "durable candidate binding fingerprint disagrees",
        )
    candidate = await _historical_candidate_from_row(session, binding.candidate_id)
    requirement_row = await session.get(EvidenceRequirementRow, binding.requirement_ref)
    set_row = await session.get(EvidenceRequirementSetRow, binding.requirement_set_ref)
    content_row = await session.get(EvidenceContentObjectRow, binding.durable_content_ref)
    if requirement_row is None or set_row is None or content_row is None:
        raise DurableContentError(
            DurableContentErrorCode.MISSING,
            "durable binding authority graph is incomplete",
        )
    if not _historical_requirement_payload_shape_valid(requirement_row):
        raise DurableContentError(
            DurableContentErrorCode.REQUIREMENT_SCHEMA_UNKNOWN,
            "persisted Requirement schema/row shape is unknown",
        )
    try:
        requirement = _requirement_from_row(requirement_row)
    except (KeyError, TypeError, ValueError) as exc:
        raise DurableContentError(
            DurableContentErrorCode.REQUIREMENT_SCHEMA_UNKNOWN,
            "persisted Requirement cannot be reconstructed by its schema",
        ) from exc
    if requirement_row.fingerprint != canonical_hash(_requirement_payload(requirement)):
        raise DurableContentError(
            DurableContentErrorCode.REQUIREMENT_FINGERPRINT_MISMATCH,
            "persisted Requirement differs from schema-selected canonical bytes",
        )
    try:
        requirement_set = _set_from_row(set_row)
        member_rows = {
            member.requirement_ref: member
            for member in await session.scalars(
                select(EvidenceRequirementRow).where(
                    EvidenceRequirementRow.requirement_set_ref
                    == binding.requirement_set_ref
                )
            )
        }
        members = tuple(
            _requirement_from_row(member_rows[member_ref])
            for member_ref in requirement_set.ordered_requirement_refs
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise DurableContentError(
            DurableContentErrorCode.INTEGRITY_MISMATCH,
            "durable binding RequirementSet graph is malformed",
        ) from exc
    expected_root = canonical_hash(
        [(member.ref.serialized(), member.fingerprint) for member in members]
    )
    if (
        any(
            not _historical_requirement_payload_shape_valid(
                member_rows[member.ref.serialized()]
            )
            or member.fingerprint != canonical_hash(_requirement_payload(member))
            for member in members
        )
        or
        expected_root != requirement_set.requirement_root_hash
        or set_row.fingerprint != canonical_hash(_set_payload(requirement_set))
    ):
        raise DurableContentError(
            DurableContentErrorCode.INTEGRITY_MISMATCH,
            "durable binding RequirementSet root/fingerprint disagrees",
        )
    content = _durable_content_from_row(content_row)
    await _verify_historical_content_in_session(
        session,
        candidate.content_ref,
        expected_payload_fingerprint=binding.durable_content_payload_fingerprint,
    )
    if (
        requirement.fingerprint_schema
        is not RequirementFingerprintSchema.V2_DURABLE_CONTENT
        or requirement.durable_content_requirement is not DurableContentRequirement.REQUIRED
        or requirement.ref.serialized() != binding.requirement_ref
        or requirement.fingerprint != binding.requirement_fingerprint
        or requirement.fingerprint_schema != binding.requirement_fingerprint_schema
        or requirement.durable_content_policy_ref != binding.durable_content_policy_ref
        or requirement.durable_content_policy_fingerprint
        != binding.durable_content_policy_fingerprint
        or set_row.requirement_root_hash != binding.requirement_root_hash
        or candidate.candidate_version != binding.candidate_version
        or candidate.candidate_fingerprint != binding.candidate_fingerprint
        or canonical_hash(_content_payload(candidate.content_ref))
        != binding.content_ref_metadata_fingerprint
        or content.payload_fingerprint != binding.durable_content_payload_fingerprint
    ):
        raise DurableContentError(
            DurableContentErrorCode.INTEGRITY_MISMATCH,
            "durable candidate binding differs from immutable authority graph",
        )
    return binding


async def _persist_candidate(session: AsyncSession, candidate: EvidenceCandidate) -> None:
    existing = await session.get(EvidenceCandidateRow, candidate.candidate_id)
    if existing is not None:
        if existing.candidate_fingerprint != candidate.candidate_fingerprint:
            raise EvidenceIdentityConflictError("candidate identity conflict")
        return
    session.add(_candidate_row(candidate))
    await session.flush()


async def _load_request_result(
    session: AsyncSession, request_id: str
) -> tuple[EvidenceAdmissionDecision, AdmittedEvidence | None]:
    evaluations = tuple(
        await session.scalars(
            select(EvidenceEvaluationRow).where(
                EvidenceEvaluationRow.admission_request_id == request_id
            )
        )
    )
    decisions = tuple(
        await session.scalars(
            select(EvidenceAdmissionDecisionRow).where(
                EvidenceAdmissionDecisionRow.admission_request_id == request_id
            )
        )
    )
    if len(evaluations) != 1 or len(decisions) != 1:
        raise EvidenceAuthorityConflictError("admission provenance is partial or ambiguous")
    request_row = await session.get(EvidenceAdmissionRequestRow, request_id)
    if request_row is None:
        raise EvidenceAuthorityConflictError("admission request projection is missing")
    decision = _decision_from_row(decisions[0], request_row)
    admitted_row = await session.scalar(
        select(AdmittedEvidenceRow).where(AdmittedEvidenceRow.decision_id == decision.decision_id)
    )
    return decision, _admitted_from_row(admitted_row) if admitted_row is not None else None


async def _admitted_by_ref(
    session: AsyncSession, serialized_ref: str
) -> AdmittedEvidenceRow | None:
    parts = serialized_ref.split(":", 2)
    if len(parts) != 3 or parts[0] != "p1-6-admitted":
        return None
    return await session.get(AdmittedEvidenceRow, parts[2])


async def _has_invalidating_event(session: AsyncSession, subject_ref: str) -> bool:
    return bool(
        await session.scalar(
            select(func.count())
            .select_from(EvidenceAuthorityEventRow)
            .where(
                EvidenceAuthorityEventRow.subject_ref == subject_ref,
                EvidenceAuthorityEventRow.event_kind.in_(
                    (
                        EvidenceAuthorityEventKind.REVOKED.value,
                        EvidenceAuthorityEventKind.SUPERSEDED.value,
                        EvidenceAuthorityEventKind.CORRECTED.value,
                    )
                ),
            )
        )
    )


async def _current_authority_revision(
    session: AsyncSession,
    *,
    task_contract_id: str,
    task_contract_version: str,
    work_run_id: str,
) -> int:
    return int(
        await session.scalar(
            select(func.max(EvidenceAuthorityEventRow.event_sequence)).where(
                EvidenceAuthorityEventRow.task_contract_id == task_contract_id,
                EvidenceAuthorityEventRow.task_contract_version == task_contract_version,
                or_(
                    EvidenceAuthorityEventRow.work_run_id.is_(None),
                    EvidenceAuthorityEventRow.work_run_id == work_run_id,
                ),
            )
        )
        or 0
    )


async def _authority_subject_scope(
    session: AsyncSession, subject_ref: str
) -> tuple[str, str, str, str | None, tuple[str, ...]] | None:
    if subject_ref.startswith("p1-6-admitted:"):
        admitted = await _admitted_by_ref(session, subject_ref)
        if admitted is None:
            return None
        mappings = tuple(
            await session.scalars(
                select(EvidenceRequirementSatisfactionRow.satisfaction_id).where(
                    EvidenceRequirementSatisfactionRow.admitted_evidence_id
                    == admitted.admitted_evidence_id
                )
            )
        )
        return (
            "ADMITTED_EVIDENCE",
            str(admitted.payload["task_contract_id"]),
            str(admitted.payload["task_contract_version"]),
            admitted.work_run_id,
            mappings,
        )

    matches: list[tuple[str, str, str, str | None, tuple[str, ...]]] = []
    requirement_set = await session.get(EvidenceRequirementSetRow, subject_ref)
    if requirement_set is not None:
        matches.append(
            (
                "REQUIREMENT_SET",
                requirement_set.task_contract_id,
                requirement_set.task_contract_version,
                None,
                (),
            )
        )
    requirement = await session.get(EvidenceRequirementRow, subject_ref)
    if requirement is not None:
        parent = await session.get(EvidenceRequirementSetRow, requirement.requirement_set_ref)
        if parent is None:
            raise EvidenceAuthorityConflictError("requirement parent set is missing")
        matches.append(
            (
                "REQUIREMENT",
                parent.task_contract_id,
                parent.task_contract_version,
                None,
                (),
            )
        )
    checkpoint = await session.get(EvidenceCheckpointRow, subject_ref)
    if checkpoint is not None:
        matches.append(
            (
                "CHECKPOINT",
                checkpoint.task_contract_id,
                checkpoint.task_contract_version,
                None,
                (),
            )
        )
    if not matches:
        return None
    if len(matches) != 1:
        raise EvidenceAuthorityConflictError("authority subject kind is ambiguous")
    return matches[0]


def _reuse_scope_key(request: EvidenceAdmissionRequest, prior_ref: str) -> str:
    return canonical_hash(
        {
            "prior": prior_ref,
            "requirement": request.requirement_ref.serialized(),
            "run": request.work_run_id,
            "checkpoint": request.checkpoint_ref.serialized(),
        }
    )


def _set_ref(set_id: str, version: str) -> str:
    return f"{set_id}@{version}"


def _set_row(value: EvidenceRequirementSet) -> EvidenceRequirementSetRow:
    return EvidenceRequirementSetRow(
        requirement_set_ref=_set_ref(value.requirement_set_id, value.requirement_set_version),
        requirement_set_id=value.requirement_set_id,
        requirement_set_version=value.requirement_set_version,
        task_contract_id=value.task_contract_id,
        task_contract_version=value.task_contract_version,
        requirement_root_hash=value.requirement_root_hash,
        fingerprint=value.fingerprint,
        payload={
            "ordered_requirement_refs": list(value.ordered_requirement_refs),
            "ordered_checkpoint_refs": list(value.ordered_checkpoint_refs),
            "semantic_owner": value.semantic_owner.value,
            "authority_version": value.authority_version,
            "revoked_at": value.revoked_at.isoformat() if value.revoked_at else None,
            "supersedes_set_ref": value.supersedes_set_ref,
        },
        issued_at=value.issued_at,
    )


def _set_from_row(row: EvidenceRequirementSetRow) -> EvidenceRequirementSet:
    return EvidenceRequirementSet(
        row.requirement_set_id,
        row.requirement_set_version,
        row.task_contract_id,
        row.task_contract_version,
        tuple(str(item) for item in _items(row.payload["ordered_requirement_refs"])),
        row.requirement_root_hash,
        tuple(str(item) for item in _items(row.payload["ordered_checkpoint_refs"])),
        EvidenceSemanticOwner(str(row.payload["semantic_owner"])),
        str(row.payload["authority_version"]),
        _aware(row.issued_at),
        row.fingerprint,
        _optional_datetime(row.payload.get("revoked_at")),
        _optional_str(row.payload.get("supersedes_set_ref")),
    )


def _requirement_row(value: EvidenceRequirement) -> EvidenceRequirementRow:
    payload: dict[str, object] = {
        "task_contract_id": value.task_contract_id,
        "task_contract_version": value.task_contract_version,
        "applicable_checkpoint_refs": list(value.applicable_checkpoint_refs),
        "evidence_type_id": value.evidence_type_id,
        "evidence_type_version": value.evidence_type_version,
        "allowed_issuer_types": sorted(item.value for item in value.allowed_issuer_types),
        "allowed_issuer_ids": sorted(value.allowed_issuer_ids),
        "allowed_human_categories": sorted(
            item.value for item in value.allowed_human_categories
        ),
        "allowed_content_kinds": sorted(item.value for item in value.allowed_content_kinds),
        "schema_id": value.schema_id,
        "schema_version": value.schema_version,
        "subject_id": value.subject_id,
        "scope_id": value.scope_id,
        "resource_id": value.resource_id,
        "freshness_kind": value.freshness_policy.kind.value,
        "freshness_max_age_seconds": value.freshness_policy.max_age_seconds,
        "freshness_config_version": value.freshness_policy.config_version,
        "required_coverage": sorted(value.required_coverage),
        "reuse_maximum": value.reuse_maximum,
        "compatible_requirement_refs": sorted(value.compatible_requirement_refs),
        "maximum_sensitivity": value.maximum_sensitivity.value,
        "public_export_allowed": value.public_export_allowed,
        "revoked_at": value.revoked_at.isoformat() if value.revoked_at else None,
        "supersedes_requirement_ref": value.supersedes_requirement_ref,
    }
    if value.fingerprint_schema is RequirementFingerprintSchema.V2_DURABLE_CONTENT:
        payload.update(
            {
                "fingerprint_schema": value.fingerprint_schema.value,
                "durable_content_requirement": value.durable_content_requirement.value,
                "durable_content_policy_ref": value.durable_content_policy_ref,
                "durable_content_policy_fingerprint": (
                    value.durable_content_policy_fingerprint
                ),
            }
        )
    return EvidenceRequirementRow(
        requirement_ref=value.ref.serialized(),
        requirement_set_ref=_set_ref(value.requirement_set_id, value.requirement_set_version),
        profile=value.profile.value,
        obligation=value.obligation.value,
        fingerprint_schema=value.fingerprint_schema.value,
        fingerprint=value.fingerprint,
        payload=payload,
        issued_at=value.issued_at,
    )


def _requirement_from_row(row: EvidenceRequirementRow) -> EvidenceRequirement:
    requirement_id, requirement_version = row.requirement_ref.rsplit("@", 1)
    set_id, set_version = row.requirement_set_ref.rsplit("@", 1)
    payload = row.payload
    schema = RequirementFingerprintSchema(row.fingerprint_schema)
    return EvidenceRequirement(
        EvidenceRequirementRef(requirement_id, requirement_version),
        str(payload["task_contract_id"]),
        str(payload["task_contract_version"]),
        set_id,
        set_version,
        EvidenceSemanticOwner.P1_6_EVIDENCE,
        EvidenceRequirementProfile(row.profile),
        RequirementObligation(row.obligation),
        tuple(str(item) for item in _items(payload["applicable_checkpoint_refs"])),
        str(payload["evidence_type_id"]),
        str(payload["evidence_type_version"]),
        frozenset(
            EvidenceIssuerType(str(item)) for item in _items(payload["allowed_issuer_types"])
        ),
        frozenset(str(item) for item in _items(payload["allowed_issuer_ids"])),
        frozenset(
            HumanEvidenceProducerCategory(str(item))
            for item in _items(payload["allowed_human_categories"])
        ),
        frozenset(
            EvidenceContentKind(str(item)) for item in _items(payload["allowed_content_kinds"])
        ),
        str(payload["schema_id"]),
        str(payload["schema_version"]),
        str(payload["subject_id"]),
        str(payload["scope_id"]),
        _optional_str(payload.get("resource_id")),
        FreshnessPolicy(
            FreshnessPolicyKind(str(payload["freshness_kind"])),
            _optional_int(payload.get("freshness_max_age_seconds")),
            _optional_str(payload.get("freshness_config_version")),
        ),
        frozenset(str(item) for item in _items(payload["required_coverage"])),
        _required_int(payload["reuse_maximum"]),
        frozenset(str(item) for item in _items(payload["compatible_requirement_refs"])),
        EvidenceSensitivity(str(payload["maximum_sensitivity"])),
        bool(payload["public_export_allowed"]),
        _aware(row.issued_at),
        row.fingerprint,
        _optional_datetime(payload.get("revoked_at")),
        _optional_str(payload.get("supersedes_requirement_ref")),
        fingerprint_schema=schema,
        durable_content_requirement=(
            DurableContentRequirement(str(payload["durable_content_requirement"]))
            if schema is RequirementFingerprintSchema.V2_DURABLE_CONTENT
            else DurableContentRequirement.NOT_APPLICABLE
        ),
        durable_content_policy_ref=(
            _optional_str(payload.get("durable_content_policy_ref"))
            if schema is RequirementFingerprintSchema.V2_DURABLE_CONTENT
            else None
        ),
        durable_content_policy_fingerprint=(
            _optional_str(payload.get("durable_content_policy_fingerprint"))
            if schema is RequirementFingerprintSchema.V2_DURABLE_CONTENT
            else None
        ),
    )


def _checkpoint_row(value: EvidenceCheckpoint) -> EvidenceCheckpointRow:
    return EvidenceCheckpointRow(
        checkpoint_ref=value.ref.serialized(),
        requirement_set_ref=_set_ref(value.requirement_set_id, value.requirement_set_version),
        task_contract_id=value.task_contract_id,
        task_contract_version=value.task_contract_version,
        source_state=value.source_state.value,
        target_state=value.target_state.value if value.target_state else None,
        transition_purpose_id=value.transition_purpose_id,
        transition_purpose_version=value.transition_purpose_version,
        fingerprint=value.fingerprint,
        payload={
            "task_authority_id": value.task_authority_id,
            "task_authority_version": value.task_authority_version,
            "revoked_at": value.revoked_at.isoformat() if value.revoked_at else None,
            "supersedes_checkpoint_ref": value.supersedes_checkpoint_ref,
        },
        issued_at=value.issued_at,
    )


def _checkpoint_from_row(row: EvidenceCheckpointRow) -> EvidenceCheckpoint:
    checkpoint_id, checkpoint_version = row.checkpoint_ref.rsplit("@", 1)
    set_id, set_version = row.requirement_set_ref.rsplit("@", 1)
    return EvidenceCheckpoint(
        EvidenceCheckpointRef(checkpoint_id, checkpoint_version),
        row.task_contract_id,
        row.task_contract_version,
        WorkflowState(row.source_state),
        WorkflowState(row.target_state) if row.target_state else None,
        row.transition_purpose_id,
        row.transition_purpose_version,
        set_id,
        set_version,
        str(row.payload["task_authority_id"]),
        str(row.payload["task_authority_version"]),
        _aware(row.issued_at),
        _optional_datetime(row.payload.get("revoked_at")),
        _optional_str(row.payload.get("supersedes_checkpoint_ref")),
        row.fingerprint,
    )


def _content_payload(value: EvidenceContentRef) -> dict[str, object]:
    return {
        "content_kind": value.content_kind.value,
        "owner_id": value.owner_id,
        "owner_version": value.owner_version,
        "object_id": value.object_id,
        "object_version": value.object_version,
        "canonicalization": value.canonicalization,
        "schema_id": value.schema_id,
        "schema_version": value.schema_version,
        "byte_count": value.byte_count,
        "content_hash": value.content_hash,
        "sensitivity": value.sensitivity.value,
        "retention_policy": value.retention_policy,
        "access_policy": value.access_policy,
    }


def _content_from_payload(payload: dict[str, object]) -> EvidenceContentRef:
    return EvidenceContentRef(
        EvidenceContentKind(str(payload["content_kind"])),
        str(payload["owner_id"]),
        str(payload["owner_version"]),
        str(payload["object_id"]),
        str(payload["object_version"]),
        str(payload["canonicalization"]),
        str(payload["schema_id"]),
        str(payload["schema_version"]),
        _required_int(payload["byte_count"]),
        str(payload["content_hash"]),
        EvidenceSensitivity(str(payload["sensitivity"])),
        str(payload["retention_policy"]),
        str(payload["access_policy"]),
    )


def _durable_content_metadata(value: DurableEvidenceContentObject) -> dict[str, object]:
    return {
        "serialized_ref": value.serialized_ref,
        "content_identity_key": value.content_identity_key,
        "owner_id": value.owner_id,
        "owner_version": value.owner_version,
        "source_owner_authority_ref": value.source_owner_authority_ref,
        "source_owner_authority_fingerprint": value.source_owner_authority_fingerprint,
        "object_id": value.object_id,
        "object_version": value.object_version,
        "content_kind": value.content_kind.value,
        "canonicalization": value.canonicalization,
        "schema_id": value.schema_id,
        "schema_version": value.schema_version,
        "byte_count": value.byte_count,
        "content_hash_algorithm": value.content_hash_algorithm,
        "content_hash": value.content_hash,
        "sensitivity": value.sensitivity.value,
        "retention_policy": value.retention_policy,
        "access_policy": value.access_policy,
        "created_at": value.created_at.isoformat(),
        "content_authority_id": value.content_authority_id,
        "content_authority_version": value.content_authority_version,
        "content_authority_revision": value.content_authority_revision,
        "payload_fingerprint_schema": value.payload_fingerprint_schema,
    }


def _verify_durable_object_value(
    value: DurableEvidenceContentObject, content_ref: EvidenceContentRef
) -> None:
    expected_identity_key = canonical_hash(
        {
            "identity_schema": DURABLE_CONTENT_IDENTITY_SCHEMA,
            "owner_id": value.owner_id,
            "owner_version": value.owner_version,
            "object_id": value.object_id,
            "object_version": value.object_version,
        }
    )
    expected_ref = f"p1-6-durable-content:v1:{expected_identity_key}"
    body = bytes(value.canonical_body_bytes)
    expected_content_ref = EvidenceContentRef(
        value.content_kind,
        value.owner_id,
        value.owner_version,
        value.object_id,
        value.object_version,
        value.canonicalization,
        value.schema_id,
        value.schema_version,
        value.byte_count,
        value.content_hash,
        value.sensitivity,
        value.retention_policy,
        value.access_policy,
    )
    actual_content_ref = EvidenceContentRef(
        content_ref.content_kind,
        content_ref.owner_id,
        content_ref.owner_version,
        content_ref.object_id,
        content_ref.object_version,
        content_ref.canonicalization,
        content_ref.schema_id,
        content_ref.schema_version,
        content_ref.byte_count,
        content_ref.content_hash,
        content_ref.sensitivity,
        content_ref.retention_policy,
        content_ref.access_policy,
    )
    if (
        value.content_identity_key != expected_identity_key
        or value.serialized_ref != expected_ref
        or value.content_kind not in DURABLE_CONTENT_KINDS
        or value.canonicalization != CANONICALIZATION_V1
        or value.content_hash_algorithm != "SHA-256"
        or value.content_authority_id != DURABLE_CONTENT_AUTHORITY_ID
        or value.content_authority_version != DURABLE_CONTENT_AUTHORITY_VERSION
        or value.content_authority_revision != DURABLE_CONTENT_AUTHORITY_REVISION
        or value.payload_fingerprint_schema != DURABLE_CONTENT_PAYLOAD_SCHEMA
        or value.retention_policy != DURABLE_CONTENT_RETENTION_POLICY
        or not 1 <= len(body) <= MAX_DURABLE_CONTENT_BYTES
        or value.byte_count != len(body)
        or value.content_hash != hashlib.sha256(body).hexdigest()
        or value.payload_fingerprint != canonical_hash(_durable_content_metadata(value))
        or canonicalize_structured_json(body) != body
        or expected_content_ref != actual_content_ref
    ):
        raise DurableContentError(
            DurableContentErrorCode.INTEGRITY_MISMATCH,
            "durable content identity, metadata, or canonical bytes disagree",
        )


def _durable_content_row(value: DurableEvidenceContentObject) -> EvidenceContentObjectRow:
    return EvidenceContentObjectRow(
        serialized_ref=value.serialized_ref,
        content_identity_key=value.content_identity_key,
        owner_id=value.owner_id,
        owner_version=value.owner_version,
        source_owner_authority_ref=value.source_owner_authority_ref,
        source_owner_authority_fingerprint=value.source_owner_authority_fingerprint,
        object_id=value.object_id,
        object_version=value.object_version,
        content_kind=value.content_kind.value,
        canonicalization=value.canonicalization,
        schema_id=value.schema_id,
        schema_version=value.schema_version,
        byte_count=value.byte_count,
        content_hash_algorithm=value.content_hash_algorithm,
        content_hash=value.content_hash,
        sensitivity=value.sensitivity.value,
        retention_policy=value.retention_policy,
        access_policy=value.access_policy,
        canonical_body=value.canonical_body_bytes,
        created_at=value.created_at,
        content_authority_id=value.content_authority_id,
        content_authority_version=value.content_authority_version,
        content_authority_revision=value.content_authority_revision,
        payload_fingerprint_schema=value.payload_fingerprint_schema,
        payload_fingerprint=value.payload_fingerprint,
    )


def _durable_content_from_row(row: EvidenceContentObjectRow) -> DurableEvidenceContentObject:
    return DurableEvidenceContentObject(
        serialized_ref=row.serialized_ref,
        content_identity_key=row.content_identity_key,
        owner_id=row.owner_id,
        owner_version=row.owner_version,
        source_owner_authority_ref=row.source_owner_authority_ref,
        source_owner_authority_fingerprint=row.source_owner_authority_fingerprint,
        object_id=row.object_id,
        object_version=row.object_version,
        content_kind=EvidenceContentKind(row.content_kind),
        canonicalization=row.canonicalization,
        schema_id=row.schema_id,
        schema_version=row.schema_version,
        byte_count=row.byte_count,
        content_hash_algorithm=row.content_hash_algorithm,
        content_hash=row.content_hash,
        sensitivity=EvidenceSensitivity(row.sensitivity),
        retention_policy=row.retention_policy,
        access_policy=row.access_policy,
        canonical_body_bytes=bytes(row.canonical_body),
        created_at=_aware(row.created_at),
        content_authority_id=row.content_authority_id,
        content_authority_version=row.content_authority_version,
        content_authority_revision=row.content_authority_revision,
        payload_fingerprint_schema=row.payload_fingerprint_schema,
        payload_fingerprint=row.payload_fingerprint,
    )


def _durable_binding_row(
    value: EvidenceCandidateDurableContentBinding,
) -> EvidenceCandidateContentBindingRow:
    return EvidenceCandidateContentBindingRow(
        candidate_id=value.candidate_id,
        candidate_version=value.candidate_version,
        candidate_fingerprint=value.candidate_fingerprint,
        durable_content_ref=value.durable_content_ref,
        durable_content_payload_fingerprint=value.durable_content_payload_fingerprint,
        content_ref_metadata_fingerprint=value.content_ref_metadata_fingerprint,
        requirement_ref=value.requirement_ref,
        requirement_fingerprint_schema=value.requirement_fingerprint_schema.value,
        requirement_fingerprint=value.requirement_fingerprint,
        requirement_set_ref=value.requirement_set_ref,
        requirement_root_hash=value.requirement_root_hash,
        durable_content_policy_ref=value.durable_content_policy_ref,
        durable_content_policy_fingerprint=value.durable_content_policy_fingerprint,
        binding_fingerprint=value.binding_fingerprint,
        bound_at=value.bound_at,
    )


def _durable_binding_payload(
    value: EvidenceCandidateDurableContentBinding,
) -> dict[str, object]:
    return {
        "candidate": [
            value.candidate_id,
            value.candidate_version,
            value.candidate_fingerprint,
        ],
        "durable_content": [
            value.durable_content_ref,
            value.durable_content_payload_fingerprint,
        ],
        "content_ref_metadata_fingerprint": value.content_ref_metadata_fingerprint,
        "requirement": [
            value.requirement_ref,
            value.requirement_fingerprint_schema.value,
            value.requirement_fingerprint,
        ],
        "requirement_set": [value.requirement_set_ref, value.requirement_root_hash],
        "policy": [
            value.durable_content_policy_ref,
            value.durable_content_policy_fingerprint,
        ],
        "bound_at": value.bound_at.isoformat(),
    }


def _durable_binding_from_row(
    row: EvidenceCandidateContentBindingRow,
) -> EvidenceCandidateDurableContentBinding:
    return EvidenceCandidateDurableContentBinding(
        candidate_id=row.candidate_id,
        candidate_version=row.candidate_version,
        candidate_fingerprint=row.candidate_fingerprint,
        durable_content_ref=row.durable_content_ref,
        durable_content_payload_fingerprint=row.durable_content_payload_fingerprint,
        content_ref_metadata_fingerprint=row.content_ref_metadata_fingerprint,
        requirement_ref=row.requirement_ref,
        requirement_fingerprint_schema=RequirementFingerprintSchema(
            row.requirement_fingerprint_schema
        ),
        requirement_fingerprint=row.requirement_fingerprint,
        requirement_set_ref=row.requirement_set_ref,
        requirement_root_hash=row.requirement_root_hash,
        durable_content_policy_ref=row.durable_content_policy_ref,
        durable_content_policy_fingerprint=row.durable_content_policy_fingerprint,
        bound_at=_aware(row.bound_at),
        binding_fingerprint=row.binding_fingerprint,
    )


def _human_ingress_row(value: HumanDirectEvidenceIngress) -> HumanDirectEvidenceIngressRow:
    return HumanDirectEvidenceIngressRow(
        ingress_record_id=value.ref.ingress_record_id,
        ingress_record_version=value.ref.ingress_record_version,
        serialized_ref=value.ref.serialized(),
        fingerprint=value.ref.fingerprint,
        ingress_authority_id=value.ingress_authority_id,
        ingress_authority_version=value.ingress_authority_version,
        authenticated_principal_id=value.authenticated_principal_id,
        authenticated_session_id=value.authenticated_session_id,
        task_contract_id=value.task_contract_id,
        task_contract_version=value.task_contract_version,
        work_run_id=value.work_run_id,
        checkpoint_ref=value.checkpoint_ref.serialized(),
        evidence_type_id=value.evidence_type_id,
        evidence_type_version=value.evidence_type_version,
        content_hash=value.content_ref.content_hash,
        payload={
            "candidate_id": value.candidate_id,
            "candidate_version": value.candidate_version,
            "principal_authority_id": value.principal_authority_id,
            "principal_authority_version": value.principal_authority_version,
            "authenticated_at": value.authenticated_at.isoformat(),
            "subject_id": value.subject_id,
            "scope_id": value.scope_id,
            "resource_id": value.resource_id,
            "content_ref": _content_payload(value.content_ref),
            "issuer_authenticity_ref": value.issuer_authenticity_ref,
        },
        provided_at=value.provided_at,
        issued_at=value.issued_at,
    )


def _human_ingress_from_row(
    row: HumanDirectEvidenceIngressRow,
) -> HumanDirectEvidenceIngress:
    checkpoint_id, checkpoint_version = row.checkpoint_ref.rsplit("@", 1)
    return HumanDirectEvidenceIngress(
        HumanDirectEvidenceIngressRef(
            row.ingress_record_id,
            row.ingress_record_version,
            row.fingerprint,
        ),
        str(row.payload["candidate_id"]),
        str(row.payload["candidate_version"]),
        row.authenticated_principal_id,
        row.authenticated_session_id,
        str(row.payload["principal_authority_id"]),
        str(row.payload["principal_authority_version"]),
        _optional_datetime(row.payload.get("authenticated_at")) or _aware(row.provided_at),
        row.ingress_authority_id,
        row.ingress_authority_version,
        row.task_contract_id,
        row.task_contract_version,
        row.work_run_id,
        EvidenceCheckpointRef(checkpoint_id, checkpoint_version),
        row.evidence_type_id,
        row.evidence_type_version,
        str(row.payload["subject_id"]),
        str(row.payload["scope_id"]),
        _optional_str(row.payload.get("resource_id")),
        _content_from_payload(row.payload["content_ref"]),  # type: ignore[arg-type]
        _aware(row.provided_at),
        _aware(row.issued_at),
        str(row.payload["issuer_authenticity_ref"]),
    )


def _candidate_row(value: EvidenceCandidate) -> EvidenceCandidateRow:
    return EvidenceCandidateRow(
        candidate_id=value.candidate_id,
        candidate_version=value.candidate_version,
        candidate_fingerprint=value.candidate_fingerprint,
        task_contract_id=value.task_contract_id,
        task_contract_version=value.task_contract_version,
        checkpoint_ref=value.checkpoint_ref.serialized(),
        issuer_type=value.issuer.owner_type.value,
        sensitivity=value.content_ref.sensitivity.value,
        content_hash=value.content_ref.content_hash,
        human_ingress_record_ref=value.human_ingress_record_ref,
        payload={
            "issuer": {
                "owner_type": value.issuer.owner_type.value,
                "owner_id": value.issuer.owner_id,
                "owner_version": value.issuer.owner_version,
                "authority_ref": value.issuer.authority_ref,
            },
            "producer_work_run_id": value.producer_work_run_id,
            "execution_attempt_id": value.execution_attempt_id,
            "operation_id": value.operation_id,
            "observed_state": value.observed_state.value,
            "observed_state_version": value.observed_state_version,
            "subject_id": value.subject_id,
            "scope_id": value.scope_id,
            "resource_id": value.resource_id,
            "evidence_type_id": value.evidence_type_id,
            "evidence_type_version": value.evidence_type_version,
            "content_ref": _content_payload(value.content_ref),
            "observed_at": value.observed_at.isoformat(),
            "coverage": sorted(value.coverage),
            "producer_attestation_ref": value.producer_attestation_ref,
            "human_producer_category": value.human_producer_category.value
            if value.human_producer_category
            else None,
            "human_ingress_record_ref": value.human_ingress_record_ref,
            "prior_admitted_evidence_ref": value.prior_admitted_evidence_ref,
            "config_version": value.config_version,
        },
        created_at=value.created_at,
    )


def _request_row(value: EvidenceAdmissionRequest) -> EvidenceAdmissionRequestRow:
    return EvidenceAdmissionRequestRow(
        admission_request_id=value.admission_request_id,
        request_fingerprint=value.request_fingerprint,
        candidate_id=value.candidate_ref.candidate_id,
        requirement_ref=value.requirement_ref.serialized(),
        requirement_set_ref=_set_ref(value.requirement_set_id, value.requirement_set_version),
        work_run_id=value.work_run_id,
        checkpoint_ref=value.checkpoint_ref.serialized(),
        observed_state=value.observed_state.value,
        observed_state_version=value.observed_state_version,
        payload={
            "candidate_version": value.candidate_ref.candidate_version,
            "candidate_fingerprint": value.candidate_ref.candidate_fingerprint,
            "requirement_fingerprint": value.requirement_fingerprint,
            "requirement_root_hash": value.requirement_root_hash,
            "task_contract_id": value.task_contract_id,
            "task_contract_version": value.task_contract_version,
            "checkpoint_fingerprint": value.checkpoint_fingerprint,
            "target_state": value.target_state.value if value.target_state else None,
            "transition_purpose_id": value.transition_purpose_id,
            "transition_purpose_version": value.transition_purpose_version,
            "requester_identity": value.requester_identity,
        },
        created_at=value.created_at,
    )


def _evaluation_row(value: EvidenceEvaluation) -> EvidenceEvaluationRow:
    return EvidenceEvaluationRow(
        evaluation_id=value.evaluation_id,
        admission_request_id=value.admission_request_id,
        dimension_results=[
            {
                "dimension": item.dimension.value,
                "outcome": item.outcome.value,
                "authority_ref": item.authority_ref,
                "authority_version": item.authority_version,
                "reason": item.reason,
            }
            for item in value.dimension_results
        ],
        authority_version=value.authority_version,
        evaluated_at=value.evaluated_at,
    )


def _decision_row(value: EvidenceAdmissionDecision) -> EvidenceAdmissionDecisionRow:
    return EvidenceAdmissionDecisionRow(
        decision_id=value.decision_id,
        admission_request_id=value.admission_request_id,
        evaluation_id=value.evaluation_id,
        outcome=value.outcome.value,
        reason=value.reason.value,
        secondary_reasons=[item.value for item in value.secondary_reasons],
        admitting_authority_version=value.admitting_authority_version,
        decided_at=value.decided_at,
    )


def _decision_from_row(
    row: EvidenceAdmissionDecisionRow,
    request: EvidenceAdmissionRequestRow,
) -> EvidenceAdmissionDecision:
    return EvidenceAdmissionDecision(
        row.decision_id,
        row.admission_request_id,
        row.evaluation_id,
        request.candidate_id,
        request.requirement_ref,
        request.requirement_set_ref,
        EvidenceAdmissionOutcome(row.outcome),
        EvidenceRejectionReason(row.reason),
        tuple(EvidenceRejectionReason(item) for item in row.secondary_reasons),
        row.admitting_authority_version,
        _aware(row.decided_at),
    )


def _make_admitted(
    request: EvidenceAdmissionRequest,
    candidate: EvidenceCandidate,
    decision: EvidenceAdmissionDecision,
) -> AdmittedEvidence:
    return AdmittedEvidence(
        str(uuid4()),
        decision.decision_id,
        request.candidate_ref,
        request.requirement_ref,
        request.task_contract_id,
        request.task_contract_version,
        request.work_run_id,
        request.checkpoint_ref,
        candidate.content_ref,
        tuple(sorted(candidate.coverage)),
        decision.decided_at,
    )


def _admitted_row(value: AdmittedEvidence) -> AdmittedEvidenceRow:
    return AdmittedEvidenceRow(
        admitted_evidence_id=value.admitted_evidence_id,
        decision_id=value.decision_id,
        candidate_id=value.candidate_ref.candidate_id,
        requirement_ref=value.requirement_ref.serialized(),
        work_run_id=value.work_run_id,
        checkpoint_ref=value.checkpoint_ref.serialized(),
        content_hash=value.content_ref.content_hash,
        coverage=list(value.coverage),
        payload={
            "candidate_version": value.candidate_ref.candidate_version,
            "candidate_fingerprint": value.candidate_ref.candidate_fingerprint,
            "task_contract_id": value.task_contract_id,
            "task_contract_version": value.task_contract_version,
            "content_ref": _content_payload(value.content_ref),
        },
        admitted_at=value.admitted_at,
    )


def _admitted_from_row(row: AdmittedEvidenceRow) -> AdmittedEvidence:
    requirement_id, requirement_version = row.requirement_ref.rsplit("@", 1)
    checkpoint_id, checkpoint_version = row.checkpoint_ref.rsplit("@", 1)
    return AdmittedEvidence(
        row.admitted_evidence_id,
        row.decision_id,
        EvidenceCandidateRef(
            row.candidate_id,
            str(row.payload["candidate_version"]),
            str(row.payload["candidate_fingerprint"]),
        ),
        EvidenceRequirementRef(requirement_id, requirement_version),
        str(row.payload["task_contract_id"]),
        str(row.payload["task_contract_version"]),
        row.work_run_id,
        EvidenceCheckpointRef(checkpoint_id, checkpoint_version),
        _content_from_payload(row.payload["content_ref"]),  # type: ignore[arg-type]
        tuple(str(item) for item in row.coverage),
        _aware(row.admitted_at),
    )


def _aware(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise EvidenceAuthorityConflictError("database returned naive evidence authority time")
    return value.astimezone(UTC)


def _optional_datetime(value: object) -> datetime | None:
    if value is None:
        return None
    parsed = datetime.fromisoformat(str(value))
    return _aware(parsed)


def _optional_str(value: object) -> str | None:
    return str(value) if value is not None else None


def _optional_int(value: object) -> int | None:
    return _required_int(value) if value is not None else None


def _required_int(value: object) -> int:
    if type(value) is not int:
        raise EvidenceAuthorityConflictError("durable evidence integer field is invalid")
    return value


def _items(value: object) -> tuple[object, ...]:
    if not isinstance(value, list):
        raise EvidenceAuthorityConflictError("durable evidence list field is invalid")
    return tuple(value)


async def _admitted_current_for_set(
    session: AsyncSession,
    admitted: AdmittedEvidenceRow,
    requirement: EvidenceRequirement,
    run: WorkRunRow,
    now: datetime,
) -> bool:
    candidate = await session.get(EvidenceCandidateRow, admitted.candidate_id)
    if candidate is None:
        raise EvidenceAuthorityConflictError("admitted evidence candidate is missing")
    observed_state = str(candidate.payload["observed_state"])
    observed_version = _required_int(candidate.payload["observed_state_version"])
    producer_run = candidate.payload.get("producer_work_run_id")
    policy = requirement.freshness_policy
    if policy.kind is FreshnessPolicyKind.IMMUTABLE_BUILD_ARTIFACT:
        return True
    if policy.kind is FreshnessPolicyKind.TASK_EXECUTION_SCOPED:
        return producer_run == run.work_run_id
    if policy.kind in {
        FreshnessPolicyKind.WORKRUN_STATE_VERSION_SCOPED,
        FreshnessPolicyKind.HUMAN_RESULT_SCOPED,
    }:
        return bool(
            producer_run == run.work_run_id
            and observed_state == run.workflow_state
            and observed_version == run.state_version
        )
    if policy.kind is FreshnessPolicyKind.CONFIG_VERSION_SCOPED:
        return bool(
            policy.config_version
            and candidate.payload.get("config_version") == policy.config_version
        )
    if policy.max_age_seconds is None:
        return False
    observed_at = datetime.fromisoformat(str(candidate.payload["observed_at"])).astimezone(UTC)
    return 0 <= (now - observed_at).total_seconds() <= policy.max_age_seconds


def _set_evaluation_payload(value: EvidenceSetEvaluation) -> dict[str, object]:
    return {
        "evaluation_version": value.evaluation_version,
        "task_contract_id": value.task_contract_id,
        "task_contract_version": value.task_contract_version,
        "work_run_id": value.work_run_id,
        "source_state": value.source_state.value,
        "state_version": value.state_version,
        "checkpoint_ref": value.checkpoint_ref.serialized(),
        "requirement_set_id": value.requirement_set_id,
        "requirement_set_version": value.requirement_set_version,
        "full_requirement_root_hash": value.full_requirement_root_hash,
        "ordered_applicable_requirement_refs": list(value.ordered_applicable_requirement_refs),
        "checkpoint_subset_root_hash": value.checkpoint_subset_root_hash,
        "requirement_results": [
            {
                "requirement_ref": item.requirement_ref,
                "outcome": item.outcome.value,
                "admitted_evidence_refs": list(item.admitted_evidence_refs),
                "coverage": list(item.coverage),
            }
            for item in value.requirement_results
        ],
        "admitted_ref_root_hash": value.admitted_ref_root_hash,
        "evidence_authority_revision": value.evidence_authority_revision,
        "outcome": value.outcome.value,
    }


def _set_evaluation_row(value: EvidenceSetEvaluation) -> EvidenceSetEvaluationRow:
    return EvidenceSetEvaluationRow(
        evaluation_id=value.evaluation_id,
        evaluation_version=value.evaluation_version,
        work_run_id=value.work_run_id,
        source_state=value.source_state.value,
        state_version=value.state_version,
        checkpoint_ref=value.checkpoint_ref.serialized(),
        requirement_set_ref=_set_ref(value.requirement_set_id, value.requirement_set_version),
        outcome=value.outcome.value,
        full_requirement_root_hash=value.full_requirement_root_hash,
        checkpoint_subset_root_hash=value.checkpoint_subset_root_hash,
        admitted_ref_root_hash=value.admitted_ref_root_hash,
        evidence_authority_revision=value.evidence_authority_revision,
        payload=_set_evaluation_payload(value),
        evaluated_at=value.evaluated_at,
    )


def _attestation_payload(
    value: EvidenceSetSatisfactionAttestation,
) -> dict[str, object]:
    return {
        "attestation_version": value.attestation_version,
        "evidence_set_evaluation_id": value.evidence_set_evaluation_id,
        "evaluation_version": value.evaluation_version,
        "task_contract_id": value.task_contract_id,
        "task_contract_version": value.task_contract_version,
        "work_run_id": value.work_run_id,
        "source_state": value.source_state.value,
        "state_version": value.state_version,
        "checkpoint_ref": value.checkpoint_ref.serialized(),
        "checkpoint_fingerprint": value.checkpoint_fingerprint,
        "target_state": value.target_state.value if value.target_state else None,
        "transition_purpose_id": value.transition_purpose_id,
        "transition_purpose_version": value.transition_purpose_version,
        "requirement_set_id": value.requirement_set_id,
        "requirement_set_version": value.requirement_set_version,
        "full_requirement_root_hash": value.full_requirement_root_hash,
        "ordered_applicable_requirement_refs": list(value.ordered_applicable_requirement_refs),
        "checkpoint_subset_root_hash": value.checkpoint_subset_root_hash,
        "ordered_admitted_evidence_refs": list(value.ordered_admitted_evidence_refs),
        "admitted_ref_root_hash": value.admitted_ref_root_hash,
        "satisfied": value.satisfied,
        "evidence_authority_version": value.evidence_authority_version,
        "evidence_authority_revision": value.evidence_authority_revision,
        "issuer_id": value.issuer_id,
        "issuer_version": value.issuer_version,
    }


def _attestation_row(
    value: EvidenceSetSatisfactionAttestation,
) -> EvidenceSetAttestationRow:
    return EvidenceSetAttestationRow(
        attestation_id=value.attestation_id,
        attestation_version=value.attestation_version,
        serialized_ref=value.serialized_ref,
        evidence_set_evaluation_id=value.evidence_set_evaluation_id,
        work_run_id=value.work_run_id,
        checkpoint_ref=value.checkpoint_ref.serialized(),
        state_version=value.state_version,
        evidence_authority_revision=value.evidence_authority_revision,
        payload=_attestation_payload(value),
        issued_at=value.issued_at,
        expires_at=value.expires_at,
    )


def _attestation_from_row(
    row: EvidenceSetAttestationRow,
) -> EvidenceSetSatisfactionAttestation:
    payload = row.payload
    checkpoint_id, checkpoint_version = str(payload["checkpoint_ref"]).rsplit("@", 1)
    return EvidenceSetSatisfactionAttestation(
        row.attestation_id,
        row.attestation_version,
        str(payload["evidence_set_evaluation_id"]),
        str(payload["evaluation_version"]),
        str(payload["task_contract_id"]),
        str(payload["task_contract_version"]),
        row.work_run_id,
        WorkflowState(str(payload["source_state"])),
        row.state_version,
        EvidenceCheckpointRef(checkpoint_id, checkpoint_version),
        str(payload["checkpoint_fingerprint"]),
        WorkflowState(str(payload["target_state"])) if payload.get("target_state") else None,
        _optional_str(payload.get("transition_purpose_id")),
        _optional_str(payload.get("transition_purpose_version")),
        str(payload["requirement_set_id"]),
        str(payload["requirement_set_version"]),
        str(payload["full_requirement_root_hash"]),
        tuple(str(item) for item in _items(payload["ordered_applicable_requirement_refs"])),
        str(payload["checkpoint_subset_root_hash"]),
        tuple(str(item) for item in _items(payload["ordered_admitted_evidence_refs"])),
        str(payload["admitted_ref_root_hash"]),
        bool(payload["satisfied"]),
        str(payload["evidence_authority_version"]),
        _required_int(payload["evidence_authority_revision"]),
        _aware(row.issued_at),
        _aware(row.expires_at) if row.expires_at else None,
        str(payload["issuer_id"]),
        str(payload["issuer_version"]),
    )
