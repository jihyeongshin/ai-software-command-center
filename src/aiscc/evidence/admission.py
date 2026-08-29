from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from uuid import uuid4

from aiscc.evidence.checkpoints import requirement_applies
from aiscc.evidence.issuers import EvidenceIssuerRegistry
from aiscc.evidence.models import (
    AdmittedEvidence,
    AuthoritativeWorkRunSnapshot,
    EvidenceAdmissionDecision,
    EvidenceAdmissionDimension,
    EvidenceAdmissionOutcome,
    EvidenceAdmissionRequest,
    EvidenceCandidate,
    EvidenceCandidateRef,
    EvidenceCheckpoint,
    EvidenceContentKind,
    EvidenceDimensionOutcome,
    EvidenceDimensionResult,
    EvidenceEvaluation,
    EvidenceIssuerType,
    EvidenceRejectionReason,
    EvidenceRequirement,
    EvidenceRequirementProfile,
    EvidenceRequirementSet,
    EvidenceSensitivity,
    FreshnessPolicyKind,
    HumanEvidenceProducerCategory,
    canonical_hash,
)
from aiscc.evidence.ports import EvidenceContentResolver

EVIDENCE_AUTHORITY_VERSION = "AISCC-P1-6-EVIDENCE-AUTHORITY-V1"

_SENSITIVITY_ORDER = {
    EvidenceSensitivity.PUBLIC_SAFE: 0,
    EvidenceSensitivity.INTERNAL: 1,
    EvidenceSensitivity.PRIVATE_SENSITIVE: 2,
    EvidenceSensitivity.SECRET_FORBIDDEN: 3,
}


class EvidenceContentRegistry:
    def __init__(self, resolvers: tuple[EvidenceContentResolver, ...]) -> None:
        self._resolvers = resolvers

    def resolve(self, candidate: EvidenceCandidate) -> bytes | None:
        matches = [item.resolve(candidate.content_ref) for item in self._resolvers]
        bodies = [item for item in matches if item is not None]
        if len(bodies) != 1:
            return None
        return bodies[0]


class EvidenceAdmissionEvaluator:
    def __init__(
        self,
        issuer_registry: EvidenceIssuerRegistry,
        content_registry: EvidenceContentRegistry,
        *,
        authority_version: str = EVIDENCE_AUTHORITY_VERSION,
    ) -> None:
        self._issuers = issuer_registry
        self._content = content_registry
        self.authority_version = authority_version

    async def evaluate(
        self,
        *,
        request: EvidenceAdmissionRequest,
        candidate: EvidenceCandidate,
        requirement: EvidenceRequirement | None,
        checkpoint: EvidenceCheckpoint | None,
        requirement_set: EvidenceRequirementSet | None,
        prior_admitted: AdmittedEvidence | None,
        prior_effective: bool,
        authoritative_work_run: AuthoritativeWorkRunSnapshot | None,
        reuse_consumed: int = 0,
        authority_current: bool = True,
        now: datetime | None = None,
    ) -> tuple[EvidenceEvaluation, EvidenceAdmissionDecision]:
        evaluated_at = (now or datetime.now(UTC)).astimezone(UTC)
        results: dict[EvidenceAdmissionDimension, EvidenceDimensionResult] = {}

        work_run_authority_ref = (
            authoritative_work_run.authority_ref
            if authoritative_work_run is not None
            else f"AISCC_SYSTEM_WORKRUN_MISSING:{request.work_run_id}"
        )
        work_run_authority_version = (
            authoritative_work_run.authority_version
            if authoritative_work_run is not None
            else "MISSING"
        )

        def record(
            dimension: EvidenceAdmissionDimension,
            passed: bool | None,
            reason: str,
            authority_ref: str = "AISCC_P1_6_POLICY",
            authority_version: str | None = None,
        ) -> None:
            outcome = (
                EvidenceDimensionOutcome.NOT_APPLICABLE
                if passed is None
                else EvidenceDimensionOutcome.PASS
                if passed
                else EvidenceDimensionOutcome.FAIL
            )
            results[dimension] = EvidenceDimensionResult(
                dimension,
                outcome,
                authority_ref,
                authority_version or self.authority_version,
                reason,
            )

        known = requirement is not None and requirement_set is not None
        requirement_matches = False
        if requirement is not None and requirement_set is not None:
            requirement_matches = bool(
                request.requirement_ref == requirement.ref
                and request.requirement_fingerprint == requirement.fingerprint
                and request.requirement_set_id == requirement.requirement_set_id
                and request.requirement_set_version == requirement.requirement_set_version
                and request.requirement_root_hash == requirement_set.requirement_root_hash
            )
        record(
            EvidenceAdmissionDimension.REQUIREMENT_MATCH,
            requirement_matches,
            "EXACT_REQUIREMENT_MATCH" if known else "UNKNOWN_REQUIREMENT",
        )
        issuer_valid = await self._issuers.recognizes(candidate)
        record(
            EvidenceAdmissionDimension.ISSUER_AUTHORITY,
            issuer_valid
            and requirement is not None
            and candidate.issuer.owner_type in requirement.allowed_issuer_types
            and (
                not requirement.allowed_issuer_ids
                or candidate.issuer.owner_id in requirement.allowed_issuer_ids
            ),
            "ISSUER_VERIFIED" if issuer_valid else "ISSUER_NOT_AUTHORIZED",
            candidate.issuer.authority_ref,
        )
        type_matches = bool(
            requirement
            and candidate.evidence_type_id == requirement.evidence_type_id
            and candidate.evidence_type_version == requirement.evidence_type_version
            and candidate.content_ref.content_kind in requirement.allowed_content_kinds
        )
        record(EvidenceAdmissionDimension.TYPE, type_matches, "EXACT_TYPE_AND_CONTENT_KIND")
        task_matches = bool(
            requirement
            and requirement_set
            and authoritative_work_run
            and candidate.task_contract_id
            == request.task_contract_id
            == requirement.task_contract_id
            == requirement_set.task_contract_id
            == authoritative_work_run.task_contract_id
            and candidate.task_contract_version
            == request.task_contract_version
            == requirement.task_contract_version
            == requirement_set.task_contract_version
            == authoritative_work_run.task_contract_version
            and request.work_run_id == authoritative_work_run.work_run_id
        )
        record(
            EvidenceAdmissionDimension.TASK_CONTRACT_BINDING,
            task_matches,
            "EXACT_AUTHORITATIVE_WORKRUN_TASK_CONTRACT_BINDING"
            if task_matches
            else "AUTHORITATIVE_WORKRUN_MISSING_OR_TASK_CONTRACT_MISMATCH",
            work_run_authority_ref,
            work_run_authority_version,
        )
        checkpoint_matches = bool(
            checkpoint
            and authoritative_work_run
            and candidate.checkpoint_ref == request.checkpoint_ref == checkpoint.ref
            and request.checkpoint_fingerprint == checkpoint.fingerprint
            and request.observed_state is checkpoint.source_state
            and authoritative_work_run.workflow_state is request.observed_state
            and authoritative_work_run.workflow_state is checkpoint.source_state
            and request.target_state is checkpoint.target_state
            and request.transition_purpose_id == checkpoint.transition_purpose_id
            and request.transition_purpose_version == checkpoint.transition_purpose_version
        )
        record(
            EvidenceAdmissionDimension.CHECKPOINT_BINDING,
            checkpoint_matches,
            "EXACT_CHECKPOINT_USE_AND_AUTHORITATIVE_SOURCE_STATE_BINDING"
            if checkpoint_matches
            else "CHECKPOINT_OR_AUTHORITATIVE_SOURCE_STATE_MISMATCH",
            work_run_authority_ref,
            work_run_authority_version,
        )
        human_result = _human_category(requirement, candidate)
        record(
            EvidenceAdmissionDimension.HUMAN_PRODUCER_CATEGORY,
            human_result,
            "EXACT_HUMAN_PRODUCER_CATEGORY"
            if human_result is not False
            else "HUMAN_PRODUCER_CATEGORY_MISMATCH",
        )
        subject_matches = bool(
            requirement
            and candidate.subject_id == requirement.subject_id
            and candidate.scope_id == requirement.scope_id
        )
        record(
            EvidenceAdmissionDimension.SUBJECT_SCOPE,
            subject_matches,
            "EXACT_SUBJECT_SCOPE",
        )
        resource_matches = bool(
            requirement
            and (
                requirement.resource_id is None or candidate.resource_id == requirement.resource_id
            )
        )
        record(
            EvidenceAdmissionDimension.RESOURCE_BINDING,
            resource_matches,
            "EXACT_RESOURCE_BINDING"
            if requirement and requirement.resource_id
            else "NO_RESOURCE_REQUIRED",
        )

        body = self._content.resolve(candidate)
        content_valid = bool(
            body is not None
            and len(body) == candidate.content_ref.byte_count
            and hashlib.sha256(body).hexdigest() == candidate.content_ref.content_hash
        )
        record(
            EvidenceAdmissionDimension.CONTENT_INTEGRITY,
            content_valid,
            "OWNER_BACKED_CONTENT_HASH_VERIFIED"
            if content_valid
            else "CONTENT_MISSING_OR_HASH_MISMATCH",
            f"{candidate.content_ref.owner_id}@{candidate.content_ref.owner_version}",
        )
        schema_valid = _schema_valid(candidate, body, requirement)
        record(
            EvidenceAdmissionDimension.SCHEMA_FORMAT,
            schema_valid,
            "EXACT_SCHEMA_FORMAT" if schema_valid else "SCHEMA_INVALID",
        )
        fresh = _fresh(
            requirement,
            candidate,
            request,
            authoritative_work_run,
            evaluated_at,
        )
        record(
            EvidenceAdmissionDimension.FRESHNESS,
            fresh,
            "REQUIREMENT_OWNED_CURRENT_WORKRUN_FRESHNESS"
            if fresh
            else "STALE_OR_MISSING_AUTHORITATIVE_WORKRUN",
            work_run_authority_ref,
            work_run_authority_version,
        )
        applies = bool(requirement and checkpoint and requirement_applies(requirement, checkpoint))
        record(
            EvidenceAdmissionDimension.APPLICABILITY,
            applies,
            "CHECKPOINT_APPLICABLE" if applies else "NOT_APPLICABLE",
        )
        coverage = bool(requirement and requirement.required_coverage <= candidate.coverage)
        record(
            EvidenceAdmissionDimension.COVERAGE,
            coverage,
            "EXACT_COVERAGE" if coverage else "INSUFFICIENT_COVERAGE",
        )
        sensitivity = bool(
            requirement
            and candidate.content_ref.sensitivity is not EvidenceSensitivity.SECRET_FORBIDDEN
            and _SENSITIVITY_ORDER[candidate.content_ref.sensitivity]
            <= _SENSITIVITY_ORDER[requirement.maximum_sensitivity]
        )
        record(
            EvidenceAdmissionDimension.SENSITIVITY_POLICY,
            sensitivity,
            "SENSITIVITY_POLICY_PASS" if sensitivity else "SENSITIVITY_POLICY_DENY",
        )
        reuse = _reuse_valid(
            requirement,
            candidate,
            prior_admitted,
            prior_effective,
            reuse_consumed,
        )
        record(
            EvidenceAdmissionDimension.REUSE_POLICY,
            reuse,
            "REUSE_POLICY_PASS" if reuse is not False else "REUSE_INCOMPATIBLE",
        )
        effective = authority_current and (
            prior_effective if candidate.prior_admitted_evidence_ref else True
        )
        record(
            EvidenceAdmissionDimension.REVOCATION_SUPERSESSION,
            effective,
            "NO_REVOCATION_OR_SUPERSESSION" if effective else "REVOKED_OR_SUPERSEDED",
        )
        record(
            EvidenceAdmissionDimension.DUPLICATE_IDEMPOTENCY,
            True,
            "SERIALIZED_IMMUTABLE_REQUEST",
        )

        profile_rejection = _profile_rejection(requirement)
        failures = [
            item.dimension
            for item in results.values()
            if item.outcome is EvidenceDimensionOutcome.FAIL
        ]
        authority_rejection = (
            EvidenceRejectionReason.AUTHORITY_CONFLICT if authoritative_work_run is None else None
        )
        reason = (
            profile_rejection
            or authority_rejection
            or _primary_reason(failures, requirement, candidate, body, prior_effective)
        )
        outcome = (
            EvidenceAdmissionOutcome.ADMITTED
            if reason is EvidenceRejectionReason.ADMITTED
            else EvidenceAdmissionOutcome.REJECTED
        )
        evaluation_id = str(uuid4())
        evaluation = EvidenceEvaluation(
            evaluation_id,
            request.admission_request_id,
            tuple(results[item] for item in EvidenceAdmissionDimension),
            evaluated_at,
            self.authority_version,
        )
        secondary = tuple(
            dict.fromkeys(
                _dimension_reason(item, requirement, candidate, body, prior_effective)
                for item in failures
                if _dimension_reason(item, requirement, candidate, body, prior_effective)
                is not reason
            )
        )
        decision = EvidenceAdmissionDecision(
            str(uuid4()),
            request.admission_request_id,
            evaluation_id,
            candidate.candidate_id,
            request.requirement_ref.serialized(),
            f"{request.requirement_set_id}@{request.requirement_set_version}",
            outcome,
            reason,
            secondary,
            self.authority_version,
            evaluated_at,
        )
        return evaluation, decision


def make_admission_request(
    *,
    admission_request_id: str,
    candidate: EvidenceCandidate,
    requirement: EvidenceRequirement,
    requirement_set: EvidenceRequirementSet,
    checkpoint: EvidenceCheckpoint,
    work_run_id: str,
    observed_state: object,
    observed_state_version: int,
    requester_identity: str,
    created_at: datetime,
) -> EvidenceAdmissionRequest:
    if observed_state is not checkpoint.source_state:
        raise ValueError("admission request source must match the System checkpoint")
    payload = {
        "admission_request_id": admission_request_id,
        "candidate": [
            candidate.candidate_id,
            candidate.candidate_version,
            candidate.candidate_fingerprint,
        ],
        "requirement": [requirement.ref.serialized(), requirement.fingerprint],
        "set": [
            requirement_set.requirement_set_id,
            requirement_set.requirement_set_version,
            requirement_set.requirement_root_hash,
        ],
        "task": [requirement.task_contract_id, requirement.task_contract_version],
        "work_run_id": work_run_id,
        "checkpoint": [checkpoint.ref.serialized(), checkpoint.fingerprint],
        "state": [checkpoint.source_state.value, observed_state_version],
        "target": checkpoint.target_state.value if checkpoint.target_state else None,
        "purpose": [
            checkpoint.transition_purpose_id,
            checkpoint.transition_purpose_version,
        ],
        "requester_identity": requester_identity,
        "created_at": created_at.isoformat(),
    }
    return EvidenceAdmissionRequest(
        admission_request_id,
        EvidenceCandidateRef(
            candidate.candidate_id,
            candidate.candidate_version,
            candidate.candidate_fingerprint,
        ),
        requirement.ref,
        requirement.fingerprint,
        requirement_set.requirement_set_id,
        requirement_set.requirement_set_version,
        requirement_set.requirement_root_hash,
        requirement.task_contract_id,
        requirement.task_contract_version,
        work_run_id,
        checkpoint.ref,
        checkpoint.fingerprint,
        checkpoint.source_state,
        observed_state_version,
        checkpoint.target_state,
        checkpoint.transition_purpose_id,
        checkpoint.transition_purpose_version,
        requester_identity,
        created_at,
        canonical_hash(payload),
    )


def _human_category(
    requirement: EvidenceRequirement | None,
    candidate: EvidenceCandidate,
) -> bool | None:
    if requirement is None:
        return False
    if requirement.profile is not EvidenceRequirementProfile.HUMAN_OWNED:
        return None if candidate.human_producer_category is None else False
    if candidate.human_producer_category is None:
        return False
    return candidate.human_producer_category in requirement.allowed_human_categories


def _schema_valid(
    candidate: EvidenceCandidate,
    body: bytes | None,
    requirement: EvidenceRequirement | None,
) -> bool:
    if requirement is None or body is None:
        return False
    if (
        candidate.content_ref.schema_id != requirement.schema_id
        or candidate.content_ref.schema_version != requirement.schema_version
    ):
        return False
    if candidate.content_ref.content_kind in {
        EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY,
        EvidenceContentKind.DATABASE_OBSERVATION_REF,
        EvidenceContentKind.RUNTIME_OBSERVATION_REF,
        EvidenceContentKind.HUMAN_STRUCTURED_REF,
    }:
        try:
            return isinstance(json.loads(body), (dict, list))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return False
    return True


def _fresh(
    requirement: EvidenceRequirement | None,
    candidate: EvidenceCandidate,
    request: EvidenceAdmissionRequest,
    authoritative_work_run: AuthoritativeWorkRunSnapshot | None,
    now: datetime,
) -> bool:
    if (
        requirement is None
        or authoritative_work_run is None
        or authoritative_work_run.work_run_id != request.work_run_id
        or authoritative_work_run.task_contract_id != request.task_contract_id
        or authoritative_work_run.task_contract_version != request.task_contract_version
        or authoritative_work_run.workflow_state is not request.observed_state
        or authoritative_work_run.state_version != request.observed_state_version
    ):
        return False
    policy = requirement.freshness_policy
    if policy.kind is FreshnessPolicyKind.IMMUTABLE_BUILD_ARTIFACT:
        return True
    if policy.kind is FreshnessPolicyKind.TASK_EXECUTION_SCOPED:
        return candidate.producer_work_run_id == authoritative_work_run.work_run_id
    if policy.kind is FreshnessPolicyKind.WORKRUN_STATE_VERSION_SCOPED:
        return (
            candidate.producer_work_run_id == authoritative_work_run.work_run_id
            and candidate.observed_state is authoritative_work_run.workflow_state
            and candidate.observed_state_version == authoritative_work_run.state_version
        )
    if policy.kind is FreshnessPolicyKind.TIME_WINDOW:
        return bool(
            policy.max_age_seconds is not None
            and 0
            <= (now - candidate.observed_at.astimezone(UTC)).total_seconds()
            <= policy.max_age_seconds
        )
    if policy.kind is FreshnessPolicyKind.CONFIG_VERSION_SCOPED:
        return bool(policy.config_version and candidate.config_version == policy.config_version)
    return (
        candidate.human_producer_category is HumanEvidenceProducerCategory.HUMAN_P1_7
        and candidate.producer_work_run_id == authoritative_work_run.work_run_id
        and candidate.observed_state_version == authoritative_work_run.state_version
    )


def _reuse_valid(
    requirement: EvidenceRequirement | None,
    candidate: EvidenceCandidate,
    prior: AdmittedEvidence | None,
    prior_effective: bool,
    reuse_consumed: int,
) -> bool | None:
    if requirement is None:
        return False
    if requirement.profile is not EvidenceRequirementProfile.REUSE_ALLOWED:
        return None if candidate.prior_admitted_evidence_ref is None else False
    if (
        candidate.issuer.owner_type is not EvidenceIssuerType.PRIOR_ADMITTED_EVIDENCE
        or prior is None
        or not prior_effective
        or requirement.reuse_maximum < 1
        or reuse_consumed >= requirement.reuse_maximum
    ):
        return False
    return bool(
        prior.requirement_ref.serialized() in requirement.compatible_requirement_refs
        and prior.content_ref.content_hash == candidate.content_ref.content_hash
        and prior.content_ref.object_id == candidate.content_ref.object_id
        and prior.coverage == tuple(sorted(candidate.coverage))
    )


def _profile_rejection(
    requirement: EvidenceRequirement | None,
) -> EvidenceRejectionReason | None:
    if requirement is None:
        return None
    if requirement.profile is EvidenceRequirementProfile.FORBIDDEN:
        return EvidenceRejectionReason.FORBIDDEN_EVIDENCE
    if requirement.profile is EvidenceRequirementProfile.NOT_REQUIRED:
        return EvidenceRejectionReason.NOT_APPLICABLE
    return None


def _primary_reason(
    failures: list[EvidenceAdmissionDimension],
    requirement: EvidenceRequirement | None,
    candidate: EvidenceCandidate,
    body: bytes | None,
    prior_effective: bool,
) -> EvidenceRejectionReason:
    if not failures:
        return EvidenceRejectionReason.ADMITTED
    return _dimension_reason(failures[0], requirement, candidate, body, prior_effective)


def _dimension_reason(
    dimension: EvidenceAdmissionDimension,
    requirement: EvidenceRequirement | None,
    candidate: EvidenceCandidate,
    body: bytes | None,
    prior_effective: bool,
) -> EvidenceRejectionReason:
    mapping = {
        EvidenceAdmissionDimension.REQUIREMENT_MATCH: EvidenceRejectionReason.UNKNOWN_REQUIREMENT
        if requirement is None
        else EvidenceRejectionReason.REQUIREMENT_VERSION_MISMATCH,
        EvidenceAdmissionDimension.ISSUER_AUTHORITY: EvidenceRejectionReason.ISSUER_NOT_AUTHORIZED,
        EvidenceAdmissionDimension.TYPE: EvidenceRejectionReason.TYPE_MISMATCH,
        EvidenceAdmissionDimension.TASK_CONTRACT_BINDING: (
            EvidenceRejectionReason.TASK_CONTRACT_MISMATCH
        ),
        EvidenceAdmissionDimension.CHECKPOINT_BINDING: EvidenceRejectionReason.CHECKPOINT_MISMATCH,
        EvidenceAdmissionDimension.HUMAN_PRODUCER_CATEGORY: (
            EvidenceRejectionReason.HUMAN_PRODUCER_CATEGORY_MISMATCH
            if candidate.human_producer_category is not None
            else EvidenceRejectionReason.HUMAN_OWNED_REQUIRED
        ),
        EvidenceAdmissionDimension.SUBJECT_SCOPE: EvidenceRejectionReason.SUBJECT_SCOPE_MISMATCH,
        EvidenceAdmissionDimension.RESOURCE_BINDING: EvidenceRejectionReason.RESOURCE_MISMATCH,
        EvidenceAdmissionDimension.CONTENT_INTEGRITY: EvidenceRejectionReason.CONTENT_MISSING
        if body is None
        else EvidenceRejectionReason.CONTENT_HASH_MISMATCH,
        EvidenceAdmissionDimension.SCHEMA_FORMAT: EvidenceRejectionReason.SCHEMA_INVALID,
        EvidenceAdmissionDimension.FRESHNESS: EvidenceRejectionReason.STALE,
        EvidenceAdmissionDimension.APPLICABILITY: EvidenceRejectionReason.NOT_APPLICABLE,
        EvidenceAdmissionDimension.COVERAGE: EvidenceRejectionReason.INSUFFICIENT_COVERAGE,
        EvidenceAdmissionDimension.SENSITIVITY_POLICY: EvidenceRejectionReason.FORBIDDEN_EVIDENCE,
        EvidenceAdmissionDimension.REUSE_POLICY: EvidenceRejectionReason.REUSE_INCOMPATIBLE,
        EvidenceAdmissionDimension.REVOCATION_SUPERSESSION: (
            EvidenceRejectionReason.REVOKED_OR_SUPERSEDED
        ),
        EvidenceAdmissionDimension.DUPLICATE_IDEMPOTENCY: (
            EvidenceRejectionReason.DUPLICATE_IDENTITY_CONFLICT
        ),
    }
    return mapping[dimension]
