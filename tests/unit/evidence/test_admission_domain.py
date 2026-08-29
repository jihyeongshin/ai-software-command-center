from __future__ import annotations

import asyncio
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from aiscc.contracts.workflow import WorkflowState
from aiscc.evidence.admission import (
    EvidenceAdmissionEvaluator,
    EvidenceContentRegistry,
    make_admission_request,
)
from aiscc.evidence.content import PrivateEvidenceContentStore
from aiscc.evidence.issuers import (
    AuthenticatedHumanPrincipalAuthority,
    EvidenceIssuerRegistry,
    HumanDirectEvidenceIngressAuthority,
    TokenEvidenceIssuer,
)
from aiscc.evidence.models import (
    AdmittedEvidence,
    AuthoritativeWorkRunSnapshot,
    EvidenceAdmissionDimension,
    EvidenceAdmissionOutcome,
    EvidenceCandidate,
    EvidenceCandidateRef,
    EvidenceCheckpoint,
    EvidenceCheckpointRef,
    EvidenceContentKind,
    EvidenceContentRef,
    EvidenceDimensionOutcome,
    EvidenceIdentityConflictError,
    EvidenceIssuerType,
    EvidenceOwner,
    EvidenceRejectionReason,
    EvidenceRequirement,
    EvidenceRequirementProfile,
    EvidenceRequirementRef,
    EvidenceRequirementSet,
    EvidenceSemanticOwner,
    EvidenceSensitivity,
    FreshnessPolicy,
    FreshnessPolicyKind,
    HumanDirectEvidenceIngress,
    HumanEvidenceProducerCategory,
    RequirementObligation,
)
from aiscc.evidence.requirements import TaskContractEvidenceAuthority

NOW = datetime(2026, 8, 29, 4, 0, tzinfo=UTC)
TASK_ID = "task-p1-6"
TASK_VERSION = "v1"
RUN_ID = "run-p1-6"
SET_ID = "evidence-set-p1-6"
SET_VERSION = "v1"
PRE = EvidenceCheckpointRef("pre-human-evidence", "v1")
POST = EvidenceCheckpointRef("post-human-evidence", "v1")
DEFAULT_FRESHNESS = FreshnessPolicy(FreshnessPolicyKind.WORKRUN_STATE_VERSION_SCOPED)


class InMemoryHumanIngressStore:
    def __init__(self) -> None:
        self.values: dict[str, HumanDirectEvidenceIngress] = {}

    async def persist_human_ingress(self, value: HumanDirectEvidenceIngress) -> None:
        existing = self.values.get(value.ref.ingress_record_id)
        if existing is not None and existing.ref.fingerprint != value.ref.fingerprint:
            raise EvidenceIdentityConflictError("Human ingress identity conflict")
        self.values.setdefault(value.ref.ingress_record_id, value)

    async def load_human_ingress(self, serialized_ref: str) -> HumanDirectEvidenceIngress | None:
        return next(
            (item for item in self.values.values() if item.ref.serialized() == serialized_ref),
            None,
        )


def checkpoint(ref: EvidenceCheckpointRef, source: WorkflowState) -> EvidenceCheckpoint:
    return EvidenceCheckpoint(
        ref,
        TASK_ID,
        TASK_VERSION,
        source,
        WorkflowState.ACCEPTED,
        None,
        None,
        SET_ID,
        SET_VERSION,
        "TASK_AUTHORITY",
        "v1",
        NOW,
    )


def requirement(
    requirement_id: str,
    *,
    profile: EvidenceRequirementProfile = EvidenceRequirementProfile.EXECUTOR_REQUIRED,
    checkpoints: tuple[str, ...] = ("pre-human-evidence@v1",),
    issuer_types: frozenset[EvidenceIssuerType] = frozenset(
        {EvidenceIssuerType.SYSTEM_STATIC_PROOF}
    ),
    issuer_ids: frozenset[str] = frozenset({"STATIC_ISSUER"}),
    human_categories: frozenset[HumanEvidenceProducerCategory] = frozenset(),
    content_kinds: frozenset[EvidenceContentKind] = frozenset(
        {EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY}
    ),
    freshness: FreshnessPolicy = DEFAULT_FRESHNESS,
    reuse_compatible: frozenset[str] = frozenset(),
    reuse_maximum: int = 1,
) -> EvidenceRequirement:
    obligation = {
        EvidenceRequirementProfile.EXECUTOR_REQUIRED: RequirementObligation.REQUIRED,
        EvidenceRequirementProfile.REUSE_ALLOWED: RequirementObligation.REQUIRED,
        EvidenceRequirementProfile.HUMAN_OWNED: RequirementObligation.REQUIRED,
        EvidenceRequirementProfile.NOT_REQUIRED: RequirementObligation.NOT_REQUIRED,
        EvidenceRequirementProfile.FORBIDDEN: RequirementObligation.FORBIDDEN,
    }[profile]
    return EvidenceRequirement(
        EvidenceRequirementRef(requirement_id, "v1"),
        TASK_ID,
        TASK_VERSION,
        SET_ID,
        SET_VERSION,
        EvidenceSemanticOwner.P1_6_EVIDENCE,
        profile,
        obligation,
        checkpoints,
        "STATIC_PROOF",
        "v1",
        issuer_types,
        issuer_ids,
        human_categories,
        content_kinds,
        "AISCC-PROOF",
        "v1",
        "aiscc-source",
        "repository",
        "repo@commit",
        freshness,
        frozenset({"source", "result"}),
        reuse_maximum,
        reuse_compatible,
        EvidenceSensitivity.INTERNAL,
        False,
        NOW,
        "",
    )


def snapshot(
    requirements: tuple[EvidenceRequirement, ...],
    checkpoints: tuple[EvidenceCheckpoint, ...],
) -> tuple[
    TaskContractEvidenceAuthority,
    EvidenceRequirementSet,
    tuple[EvidenceRequirement, ...],
    tuple[EvidenceCheckpoint, ...],
]:
    authority = TaskContractEvidenceAuthority("TASK_AUTHORITY", "v1")
    sealed_requirements = tuple(authority.seal_requirement(item) for item in requirements)
    sealed_checkpoints = tuple(authority.seal_checkpoint(item) for item in checkpoints)
    requirement_set = authority.seal_set(
        EvidenceRequirementSet(
            SET_ID,
            SET_VERSION,
            TASK_ID,
            TASK_VERSION,
            tuple(item.ref.serialized() for item in sealed_requirements),
            "",
            tuple(item.ref.serialized() for item in sealed_checkpoints),
            EvidenceSemanticOwner.P1_6_EVIDENCE,
            "AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
            NOW,
            "",
        ),
        sealed_requirements,
        sealed_checkpoints,
    )
    return authority, requirement_set, sealed_requirements, sealed_checkpoints


def static_candidate(
    store: PrivateEvidenceContentStore,
    issuer: TokenEvidenceIssuer,
    cp: EvidenceCheckpoint,
    *,
    candidate_id: str = "candidate-static",
    state_version: int = 3,
    content_ref: EvidenceContentRef | None = None,
    observed_at: datetime = NOW,
) -> EvidenceCandidate:
    ref = content_ref or store.put_structured(
        object_id=f"body-{candidate_id}",
        object_version="v1",
        value={"result": "PASS", "source": "ruff"},
        kind=EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY,
        schema_id="AISCC-PROOF",
        schema_version="v1",
        sensitivity=EvidenceSensitivity.INTERNAL,
    )
    return issuer.issue(
        EvidenceCandidate(
            candidate_id,
            "v1",
            "",
            EvidenceOwner(
                EvidenceIssuerType.SYSTEM_STATIC_PROOF,
                "STATIC_ISSUER",
                "v1",
                "STATIC_ISSUER@v1",
            ),
            RUN_ID,
            None,
            None,
            TASK_ID,
            TASK_VERSION,
            cp.ref,
            cp.source_state,
            state_version,
            "aiscc-source",
            "repository",
            "repo@commit",
            "STATIC_PROOF",
            "v1",
            ref,
            NOW,
            observed_at,
            frozenset({"source", "result"}),
            "system-proof-attestation",
        )
    )


def authoritative_work_run(
    cp: EvidenceCheckpoint,
    *,
    state_version: int = 3,
    task_contract_id: str = TASK_ID,
    task_contract_version: str = TASK_VERSION,
) -> AuthoritativeWorkRunSnapshot:
    return AuthoritativeWorkRunSnapshot(
        RUN_ID,
        task_contract_id,
        task_contract_version,
        cp.source_state,
        state_version,
        f"AISCC_SYSTEM_WORKRUN:{RUN_ID}",
        f"state-version:{state_version}",
    )


async def decide(
    candidate: EvidenceCandidate,
    req: EvidenceRequirement,
    req_set: EvidenceRequirementSet,
    cp: EvidenceCheckpoint,
    evaluator: EvidenceAdmissionEvaluator,
    *,
    request_id: str = "request-1",
    prior: AdmittedEvidence | None = None,
    prior_effective: bool = False,
    reuse_consumed: int = 0,
) -> tuple[EvidenceAdmissionOutcome, EvidenceRejectionReason]:
    request = make_admission_request(
        admission_request_id=request_id,
        candidate=candidate,
        requirement=req,
        requirement_set=req_set,
        checkpoint=cp,
        work_run_id=RUN_ID,
        observed_state=cp.source_state,
        observed_state_version=3,
        requester_identity="system:test",
        created_at=NOW,
    )
    _, decision = await evaluator.evaluate(
        request=request,
        candidate=candidate,
        requirement=req,
        checkpoint=cp,
        requirement_set=req_set,
        prior_admitted=prior,
        prior_effective=prior_effective,
        authoritative_work_run=authoritative_work_run(cp),
        reuse_consumed=reuse_consumed,
        now=NOW,
    )
    return decision.outcome, decision.reason


def test_exact_profiles_and_positive_admission_are_non_substituting() -> None:
    assert tuple(EvidenceRequirementProfile) == (
        EvidenceRequirementProfile.EXECUTOR_REQUIRED,
        EvidenceRequirementProfile.REUSE_ALLOWED,
        EvidenceRequirementProfile.HUMAN_OWNED,
        EvidenceRequirementProfile.NOT_REQUIRED,
        EvidenceRequirementProfile.FORBIDDEN,
    )
    cp = checkpoint(PRE, WorkflowState.ADMISSION_PENDING)
    _, req_set, requirements, checkpoints = snapshot((requirement("static"),), (cp,))
    req = requirements[0]
    cp = checkpoints[0]
    store = PrivateEvidenceContentStore("PRIVATE_STORE", "v1")
    issuer = TokenEvidenceIssuer(EvidenceIssuerType.SYSTEM_STATIC_PROOF, "STATIC_ISSUER", "v1")
    candidate = static_candidate(store, issuer, cp)
    evaluator = EvidenceAdmissionEvaluator(
        EvidenceIssuerRegistry((issuer,)), EvidenceContentRegistry((store,))
    )
    outcome, reason = asyncio.run(decide(candidate, req, req_set, cp, evaluator))
    assert (outcome, reason) == (
        EvidenceAdmissionOutcome.ADMITTED,
        EvidenceRejectionReason.ADMITTED,
    )
    assert type(candidate) is EvidenceCandidate


def test_raw_ref_forged_issuer_hash_mismatch_and_stale_are_rejected() -> None:
    cp = checkpoint(PRE, WorkflowState.ADMISSION_PENDING)
    _, req_set, requirements, checkpoints = snapshot((requirement("static"),), (cp,))
    req, cp = requirements[0], checkpoints[0]
    store = PrivateEvidenceContentStore("PRIVATE_STORE", "v1")
    issuer = TokenEvidenceIssuer(EvidenceIssuerType.SYSTEM_STATIC_PROOF, "STATIC_ISSUER", "v1")
    evaluator = EvidenceAdmissionEvaluator(
        EvidenceIssuerRegistry((issuer,)), EvidenceContentRegistry((store,))
    )
    good = static_candidate(store, issuer, cp)

    raw_ref = replace(good.content_ref, _owner_token=None, object_id="C:/untrusted/path")
    raw = static_candidate(store, issuer, cp, candidate_id="raw", content_ref=raw_ref)
    assert asyncio.run(decide(raw, req, req_set, cp, evaluator, request_id="raw"))[1] is (
        EvidenceRejectionReason.CONTENT_MISSING
    )

    forged = replace(good, candidate_id="forged", _issuer_token=object())
    assert asyncio.run(decide(forged, req, req_set, cp, evaluator, request_id="forged"))[1] is (
        EvidenceRejectionReason.ISSUER_NOT_AUTHORIZED
    )

    tampered_ref = store.tampered_ref(good.content_ref, content_hash="0" * 64)
    tampered = static_candidate(
        store, issuer, cp, candidate_id="tampered", content_ref=tampered_ref
    )
    assert asyncio.run(decide(tampered, req, req_set, cp, evaluator, request_id="tampered"))[1] is (
        EvidenceRejectionReason.CONTENT_HASH_MISMATCH
    )

    stale = static_candidate(store, issuer, cp, candidate_id="stale", state_version=2)
    assert asyncio.run(decide(stale, req, req_set, cp, evaluator, request_id="stale"))[1] is (
        EvidenceRejectionReason.STALE
    )


def test_authoritative_workrun_overrides_request_candidate_self_consistency() -> None:
    cp = checkpoint(PRE, WorkflowState.ADMISSION_PENDING)
    _, req_set, requirements, checkpoints = snapshot((requirement("static"),), (cp,))
    req, cp = requirements[0], checkpoints[0]
    store = PrivateEvidenceContentStore("AUTHORITATIVE_WORKRUN_STORE", "v1")
    issuer = TokenEvidenceIssuer(EvidenceIssuerType.SYSTEM_STATIC_PROOF, "STATIC_ISSUER", "v1")
    evaluator = EvidenceAdmissionEvaluator(
        EvidenceIssuerRegistry((issuer,)), EvidenceContentRegistry((store,))
    )
    candidate = static_candidate(store, issuer, cp, candidate_id="self-consistent-v3")
    request = make_admission_request(
        admission_request_id="self-consistent-v3",
        candidate=candidate,
        requirement=req,
        requirement_set=req_set,
        checkpoint=cp,
        work_run_id=RUN_ID,
        observed_state=cp.source_state,
        observed_state_version=3,
        requester_identity="system:test",
        created_at=NOW,
    )
    evaluation, stale = asyncio.run(
        evaluator.evaluate(
            request=request,
            candidate=candidate,
            requirement=req,
            checkpoint=cp,
            requirement_set=req_set,
            prior_admitted=None,
            prior_effective=False,
            authoritative_work_run=authoritative_work_run(cp, state_version=4),
            now=NOW,
        )
    )
    freshness = next(
        item
        for item in evaluation.dimension_results
        if item.dimension is EvidenceAdmissionDimension.FRESHNESS
    )
    assert stale.reason is EvidenceRejectionReason.STALE
    assert freshness.outcome is EvidenceDimensionOutcome.FAIL
    assert freshness.authority_version == "state-version:4"

    _, missing = asyncio.run(
        evaluator.evaluate(
            request=replace(request, admission_request_id="missing-workrun"),
            candidate=candidate,
            requirement=req,
            checkpoint=cp,
            requirement_set=req_set,
            prior_admitted=None,
            prior_effective=False,
            authoritative_work_run=None,
            now=NOW,
        )
    )
    assert missing.reason is EvidenceRejectionReason.AUTHORITY_CONFLICT


def test_checkpoint_and_human_direct_category_are_exact() -> None:
    pre = checkpoint(PRE, WorkflowState.ADMISSION_PENDING)
    post = checkpoint(POST, WorkflowState.HUMAN_REQUIRED)
    human_req = requirement(
        "human-final",
        profile=EvidenceRequirementProfile.HUMAN_OWNED,
        checkpoints=(POST.serialized(),),
        issuer_types=frozenset({EvidenceIssuerType.HUMAN_DIRECT_EVIDENCE}),
        issuer_ids=frozenset({"HUMAN_INGRESS"}),
        human_categories=frozenset({HumanEvidenceProducerCategory.HUMAN_P1_7}),
        content_kinds=frozenset({EvidenceContentKind.HUMAN_STRUCTURED_REF}),
    )
    _, req_set, requirements, checkpoints = snapshot((human_req,), (pre, post))
    req, pre, post = requirements[0], checkpoints[0], checkpoints[1]
    store = PrivateEvidenceContentStore("HUMAN_STORE", "v1")
    content = store.put_structured(
        object_id="human-record",
        object_version="v1",
        value={"review": "APPROVED"},
        kind=EvidenceContentKind.HUMAN_STRUCTURED_REF,
        schema_id="AISCC-PROOF",
        schema_version="v1",
        sensitivity=EvidenceSensitivity.INTERNAL,
    )
    principal_authority = AuthenticatedHumanPrincipalAuthority("HUMAN_AUTHN", "v1")
    ingress_store = InMemoryHumanIngressStore()
    ingress = HumanDirectEvidenceIngressAuthority(
        "HUMAN_INGRESS", "v1", principal_authority, ingress_store
    )
    principal = principal_authority.authenticate("human:operator", "session-1", NOW)
    unissued = EvidenceCandidate(
        "human-direct",
        "v1",
        "",
        EvidenceOwner(
            EvidenceIssuerType.HUMAN_DIRECT_EVIDENCE,
            "HUMAN_INGRESS",
            "v1",
            "HUMAN_INGRESS@v1",
        ),
        RUN_ID,
        None,
        None,
        TASK_ID,
        TASK_VERSION,
        post.ref,
        post.source_state,
        3,
        "aiscc-source",
        "repository",
        "repo@commit",
        "STATIC_PROOF",
        "v1",
        content,
        NOW,
        NOW,
        frozenset({"source", "result"}),
        "",
        HumanEvidenceProducerCategory.HUMAN_DIRECT_EVIDENCE,
    )
    direct = asyncio.run(
        ingress.issue(
            unissued,
            principal,
            ingress_idempotency_key="human-ingress-record-1",
        )
    )
    evaluator = EvidenceAdmissionEvaluator(
        EvidenceIssuerRegistry((ingress,)), EvidenceContentRegistry((store,))
    )
    _, reason = asyncio.run(decide(direct, req, req_set, post, evaluator))
    assert reason is EvidenceRejectionReason.HUMAN_PRODUCER_CATEGORY_MISMATCH

    wrong_checkpoint = replace(direct, checkpoint_ref=pre.ref)
    request = make_admission_request(
        admission_request_id="wrong-checkpoint",
        candidate=wrong_checkpoint,
        requirement=req,
        requirement_set=req_set,
        checkpoint=post,
        work_run_id=RUN_ID,
        observed_state=post.source_state,
        observed_state_version=3,
        requester_identity="system:test",
        created_at=NOW,
    )
    _, decision = asyncio.run(
        evaluator.evaluate(
            request=request,
            candidate=wrong_checkpoint,
            requirement=req,
            checkpoint=post,
            requirement_set=req_set,
            prior_admitted=None,
            prior_effective=False,
            authoritative_work_run=authoritative_work_run(post),
            now=NOW,
        )
    )
    assert EvidenceRejectionReason.CHECKPOINT_MISMATCH in (
        decision.reason,
        *decision.secondary_reasons,
    )
    conflicting = replace(unissued, candidate_id="human-direct-conflict")
    with pytest.raises(EvidenceIdentityConflictError):
        asyncio.run(
            ingress.issue(
                conflicting,
                principal,
                ingress_idempotency_key="human-ingress-record-1",
            )
        )


def test_private_export_and_secret_body_fail_closed() -> None:
    store = PrivateEvidenceContentStore("PRIVATE_STORE", "v1")
    private = store.put_structured(
        object_id="private",
        object_version="v1",
        value={"redacted": True},
        kind=EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY,
        schema_id="AISCC-PROOF",
        schema_version="v1",
        sensitivity=EvidenceSensitivity.PRIVATE_SENSITIVE,
    )
    assert store.public_export(private) is None
    with pytest.raises(ValueError, match="raw secret"):
        store.put_bytes(
            object_id="secret",
            object_version="v1",
            body=b"credential-material",
            sensitivity=EvidenceSensitivity.SECRET_FORBIDDEN,
        )


def test_unknown_not_required_forbidden_and_all_dimensions_fail_closed() -> None:
    cp = checkpoint(PRE, WorkflowState.ADMISSION_PENDING)
    base = requirement("base")
    _, req_set, requirements, checkpoints = snapshot((base,), (cp,))
    req, cp = requirements[0], checkpoints[0]
    store = PrivateEvidenceContentStore("PROFILE_STORE", "v1")
    issuer = TokenEvidenceIssuer(EvidenceIssuerType.SYSTEM_STATIC_PROOF, "STATIC_ISSUER", "v1")
    candidate = static_candidate(store, issuer, cp)
    evaluator = EvidenceAdmissionEvaluator(
        EvidenceIssuerRegistry((issuer,)), EvidenceContentRegistry((store,))
    )
    request = make_admission_request(
        admission_request_id="profile-request",
        candidate=candidate,
        requirement=req,
        requirement_set=req_set,
        checkpoint=cp,
        work_run_id=RUN_ID,
        observed_state=cp.source_state,
        observed_state_version=3,
        requester_identity="system:test",
        created_at=NOW,
    )
    evaluation, positive = asyncio.run(
        evaluator.evaluate(
            request=request,
            candidate=candidate,
            requirement=req,
            checkpoint=cp,
            requirement_set=req_set,
            prior_admitted=None,
            prior_effective=False,
            authoritative_work_run=authoritative_work_run(cp),
            now=NOW,
        )
    )
    assert positive.outcome is EvidenceAdmissionOutcome.ADMITTED
    assert tuple(item.dimension for item in evaluation.dimension_results) == tuple(
        EvidenceAdmissionDimension
    )

    _, unknown = asyncio.run(
        evaluator.evaluate(
            request=replace(
                request,
                requirement_ref=EvidenceRequirementRef("unknown", "v9"),
            ),
            candidate=candidate,
            requirement=None,
            checkpoint=cp,
            requirement_set=req_set,
            prior_admitted=None,
            prior_effective=False,
            authoritative_work_run=authoritative_work_run(cp),
            now=NOW,
        )
    )
    assert unknown.reason is EvidenceRejectionReason.UNKNOWN_REQUIREMENT

    for profile, expected in (
        (EvidenceRequirementProfile.NOT_REQUIRED, EvidenceRejectionReason.NOT_APPLICABLE),
        (EvidenceRequirementProfile.FORBIDDEN, EvidenceRejectionReason.FORBIDDEN_EVIDENCE),
    ):
        profile_requirement = requirement(f"profile-{profile.value}", profile=profile)
        _, profile_set, profile_requirements, profile_checkpoints = snapshot(
            (profile_requirement,), (checkpoint(PRE, WorkflowState.ADMISSION_PENDING),)
        )
        sealed_requirement = profile_requirements[0]
        sealed_checkpoint = profile_checkpoints[0]
        profile_request = make_admission_request(
            admission_request_id=f"request-{profile.value}",
            candidate=candidate,
            requirement=sealed_requirement,
            requirement_set=profile_set,
            checkpoint=sealed_checkpoint,
            work_run_id=RUN_ID,
            observed_state=sealed_checkpoint.source_state,
            observed_state_version=3,
            requester_identity="system:test",
            created_at=NOW,
        )
        _, decision = asyncio.run(
            evaluator.evaluate(
                request=profile_request,
                candidate=candidate,
                requirement=sealed_requirement,
                checkpoint=sealed_checkpoint,
                requirement_set=profile_set,
                prior_admitted=None,
                prior_effective=False,
                authoritative_work_run=authoritative_work_run(sealed_checkpoint),
                now=NOW,
            )
        )
        assert decision.reason is expected


def test_reuse_requires_new_compatible_current_admission() -> None:
    cp = checkpoint(PRE, WorkflowState.ADMISSION_PENDING)
    prior_ref = EvidenceRequirementRef("prior-static", "v1")
    reuse_req = requirement(
        "reuse-static",
        profile=EvidenceRequirementProfile.REUSE_ALLOWED,
        issuer_types=frozenset({EvidenceIssuerType.PRIOR_ADMITTED_EVIDENCE}),
        issuer_ids=frozenset({"AISCC_P1_6_REUSE_AUTHORITY_V1"}),
        reuse_compatible=frozenset({prior_ref.serialized()}),
    )
    _, req_set, requirements, checkpoints = snapshot((reuse_req,), (cp,))
    req, cp = requirements[0], checkpoints[0]
    store = PrivateEvidenceContentStore("PRIVATE_STORE", "v1")
    content = store.put_structured(
        object_id="reusable",
        object_version="v1",
        value={"result": "PASS", "source": "build"},
        kind=EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY,
        schema_id="AISCC-PROOF",
        schema_version="v1",
        sensitivity=EvidenceSensitivity.INTERNAL,
    )
    candidate = EvidenceCandidate(
        "reuse-candidate",
        "v1",
        "reuse-fingerprint",
        EvidenceOwner(
            EvidenceIssuerType.PRIOR_ADMITTED_EVIDENCE,
            "AISCC_P1_6_REUSE_AUTHORITY_V1",
            "p1-6-reuse-v1",
            "reuse-authority",
        ),
        RUN_ID,
        None,
        None,
        TASK_ID,
        TASK_VERSION,
        cp.ref,
        cp.source_state,
        3,
        "aiscc-source",
        "repository",
        "repo@commit",
        "STATIC_PROOF",
        "v1",
        content,
        NOW,
        NOW,
        frozenset({"source", "result"}),
        "prior-admission-attestation",
        prior_admitted_evidence_ref="p1-6-admitted:v1:prior-admitted",
    )

    class ReuseVerifier:
        issuer_type = EvidenceIssuerType.PRIOR_ADMITTED_EVIDENCE

        async def recognizes(self, value: EvidenceCandidate) -> bool:
            return value is candidate

    prior = AdmittedEvidence(
        "prior-admitted",
        "prior-decision",
        EvidenceCandidateRef("prior-candidate", "v1", "prior-fingerprint"),
        prior_ref,
        "prior-task",
        "v1",
        "prior-run",
        cp.ref,
        content,
        ("result", "source"),
        NOW - timedelta(days=1),
    )
    evaluator = EvidenceAdmissionEvaluator(
        EvidenceIssuerRegistry((ReuseVerifier(),)), EvidenceContentRegistry((store,))
    )
    outcome, reason = asyncio.run(
        decide(
            candidate,
            req,
            req_set,
            cp,
            evaluator,
            prior=prior,
            prior_effective=True,
        )
    )
    assert (outcome, reason) == (
        EvidenceAdmissionOutcome.ADMITTED,
        EvidenceRejectionReason.ADMITTED,
    )
    _, revoked_reason = asyncio.run(
        decide(
            candidate,
            req,
            req_set,
            cp,
            evaluator,
            request_id="revoked-reuse",
            prior=prior,
            prior_effective=False,
        )
    )
    assert revoked_reason is EvidenceRejectionReason.REUSE_INCOMPATIBLE

    _, exhausted_reason = asyncio.run(
        decide(
            candidate,
            req,
            req_set,
            cp,
            evaluator,
            request_id="exhausted-reuse",
            prior=prior,
            prior_effective=True,
            reuse_consumed=1,
        )
    )
    assert exhausted_reason is EvidenceRejectionReason.REUSE_INCOMPATIBLE

    zero_requirement = requirement(
        "reuse-zero",
        profile=EvidenceRequirementProfile.REUSE_ALLOWED,
        issuer_types=frozenset({EvidenceIssuerType.PRIOR_ADMITTED_EVIDENCE}),
        issuer_ids=frozenset({"AISCC_P1_6_REUSE_AUTHORITY_V1"}),
        reuse_compatible=frozenset({prior_ref.serialized()}),
        reuse_maximum=0,
    )
    _, zero_set, zero_requirements, zero_checkpoints = snapshot(
        (zero_requirement,), (checkpoint(PRE, WorkflowState.ADMISSION_PENDING),)
    )
    _, zero_reason = asyncio.run(
        decide(
            candidate,
            zero_requirements[0],
            zero_set,
            zero_checkpoints[0],
            evaluator,
            request_id="zero-reuse",
            prior=prior,
            prior_effective=True,
        )
    )
    assert zero_reason is EvidenceRejectionReason.REUSE_INCOMPATIBLE
