from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from sqlalchemy import func, or_, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.contracts.workflow import WorkflowState
from aiscc.evidence.admission import EvidenceAdmissionEvaluator
from aiscc.evidence.models import (
    AdmittedEvidence,
    AdmittedEvidenceRef,
    AuthoritativeWorkRunSnapshot,
    EvidenceAdmissionDecision,
    EvidenceAdmissionOutcome,
    EvidenceAdmissionRequest,
    EvidenceAuthorityConflictError,
    EvidenceAuthorityEventKind,
    EvidenceCandidate,
    EvidenceCandidateRef,
    EvidenceCheckpoint,
    EvidenceCheckpointRef,
    EvidenceContentKind,
    EvidenceContentRef,
    EvidenceEvaluation,
    EvidenceIdentityConflictError,
    EvidenceIssuerType,
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
    HumanDirectEvidenceIngress,
    HumanDirectEvidenceIngressRef,
    HumanEvidenceProducerCategory,
    RequirementObligation,
    RequirementSatisfaction,
    canonical_hash,
)
from aiscc.evidence.requirements import TaskContractEvidenceAuthority
from aiscc.persistence.models import (
    AdmittedEvidenceRow,
    EvidenceAdmissionDecisionRow,
    EvidenceAdmissionRequestRow,
    EvidenceAuthorityEventRow,
    EvidenceCandidateRow,
    EvidenceCheckpointRow,
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


class PostgresEvidenceRepository:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory

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
    ) -> tuple[EvidenceAdmissionDecision, AdmittedEvidence | None]:
        if request.candidate_ref != EvidenceCandidateRef(
            candidate.candidate_id,
            candidate.candidate_version,
            candidate.candidate_fingerprint,
        ):
            raise EvidenceIdentityConflictError("request candidate ref mismatch")
        async with self._session_factory() as session, session.begin():
            await _acquire_work_run_transaction_lock(session, request.work_run_id)
            await _lock(session, f"evidence-request:{request.admission_request_id}")
            await _lock(
                session,
                f"evidence-task:{request.task_contract_id}:{request.task_contract_version}",
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
            evaluation, decision = await evaluator.evaluate(
                request=request,
                candidate=candidate,
                requirement=requirement,
                checkpoint=checkpoint,
                requirement_set=requirement_set,
                prior_admitted=prior,
                prior_effective=prior_effective,
                authoritative_work_run=authoritative_work_run,
                reuse_consumed=reuse_consumed,
                authority_current=authority_current,
                now=now,
            )
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
        current_time = (now or datetime.now(UTC)).astimezone(UTC)
        async with self._session_factory() as session, session.begin():
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
                        EvidenceRequirementSetRow.task_contract_version
                        == run.task_contract_version,
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

            checkpoint_row = await session.get(
                EvidenceCheckpointRow, value.checkpoint_ref.serialized()
            )
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
    return EvidenceRequirementRow(
        requirement_ref=value.ref.serialized(),
        requirement_set_ref=_set_ref(value.requirement_set_id, value.requirement_set_version),
        profile=value.profile.value,
        obligation=value.obligation.value,
        fingerprint=value.fingerprint,
        payload={
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
        },
        issued_at=value.issued_at,
    )


def _requirement_from_row(row: EvidenceRequirementRow) -> EvidenceRequirement:
    requirement_id, requirement_version = row.requirement_ref.rsplit("@", 1)
    set_id, set_version = row.requirement_set_ref.rsplit("@", 1)
    payload = row.payload
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
