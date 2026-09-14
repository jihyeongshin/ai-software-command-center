from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from aiscc.evidence.models import (
    EvidenceCandidate,
    EvidenceIssuerType,
    EvidenceOwner,
    HumanDirectEvidenceIngress,
    HumanDirectEvidenceIngressRef,
    HumanEvidenceProducerCategory,
    canonical_hash,
)
from aiscc.evidence.ports import (
    EvidenceIssuerVerifier,
    HumanDirectEvidenceIngressStore,
    P1_5ImmutableRefResolver,
)

if TYPE_CHECKING:
    from aiscc.evidence.repository import PostgresEvidenceRepository
    from aiscc.human.repository import PostgresHumanAuthorityRepository


class EvidenceIssuerRegistry:
    def __init__(self, verifiers: tuple[EvidenceIssuerVerifier, ...]) -> None:
        self._verifiers: dict[EvidenceIssuerType, EvidenceIssuerVerifier] = {}
        for verifier in verifiers:
            if verifier.issuer_type in self._verifiers:
                raise ValueError("one issuer verifier is allowed per exact issuer category")
            self._verifiers[verifier.issuer_type] = verifier

    async def recognizes(self, candidate: EvidenceCandidate) -> bool:
        verifier = self._verifiers.get(candidate.issuer.owner_type)
        return verifier is not None and await verifier.recognizes(candidate)


class TokenEvidenceIssuer:
    """Server-owned issuer for one exact System proof category."""

    def __init__(
        self, issuer_type: EvidenceIssuerType, issuer_id: str, issuer_version: str
    ) -> None:
        if issuer_type in {
            EvidenceIssuerType.HUMAN_DIRECT_EVIDENCE,
            EvidenceIssuerType.HUMAN_P1_7,
            EvidenceIssuerType.PRIOR_ADMITTED_EVIDENCE,
        } or issuer_type.value.startswith("P1_5_"):
            raise ValueError("this issuer category requires its owner-specific authority")
        self._issuer_type = issuer_type
        self.issuer_id = issuer_id
        self.issuer_version = issuer_version
        self._issuer_token = object()

    @property
    def issuer_type(self) -> EvidenceIssuerType:
        return self._issuer_type

    def issue(self, candidate: EvidenceCandidate) -> EvidenceCandidate:
        expected = EvidenceOwner(
            self.issuer_type,
            self.issuer_id,
            self.issuer_version,
            f"{self.issuer_id}@{self.issuer_version}",
        )
        if candidate.issuer != expected or candidate.human_producer_category is not None:
            raise ValueError("candidate owner does not match the System proof issuer")
        value = replace(candidate, _issuer_token=self._issuer_token)
        return replace(value, candidate_fingerprint=candidate_fingerprint(value))

    async def recognizes(self, candidate: EvidenceCandidate) -> bool:
        return (
            candidate._issuer_token is self._issuer_token
            and candidate.issuer.owner_id == self.issuer_id
            and candidate.issuer.owner_version == self.issuer_version
            and candidate.candidate_fingerprint == candidate_fingerprint(candidate)
        )


@dataclass(frozen=True, slots=True)
class AuthenticatedHumanPrincipal:
    principal_id: str
    session_id: str
    authenticated_at: datetime
    authority_id: str
    authority_version: str
    _authority_token: object


class AuthenticatedHumanPrincipalAuthority:
    def __init__(self, authority_id: str, authority_version: str) -> None:
        self.authority_id = authority_id
        self.authority_version = authority_version
        self._token = object()

    def authenticate(
        self, principal_id: str, session_id: str, authenticated_at: datetime
    ) -> AuthenticatedHumanPrincipal:
        if not principal_id or not session_id:
            raise ValueError("authenticated Human identity and session are required")
        if authenticated_at.tzinfo is None or authenticated_at.utcoffset() is None:
            raise ValueError("Human authentication time must be timezone-aware")
        return AuthenticatedHumanPrincipal(
            principal_id,
            session_id,
            authenticated_at,
            self.authority_id,
            self.authority_version,
            self._token,
        )

    def recognizes(self, principal: AuthenticatedHumanPrincipal) -> bool:
        return principal._authority_token is self._token


class HumanDirectEvidenceIngressAuthority:
    """P1-6 evidence ingress only; never issues HumanResult/Judgment/guard facts."""

    issuer_type = EvidenceIssuerType.HUMAN_DIRECT_EVIDENCE

    def __init__(
        self,
        authority_id: str,
        authority_version: str,
        principal_authority: AuthenticatedHumanPrincipalAuthority,
        ingress_store: HumanDirectEvidenceIngressStore,
    ) -> None:
        self.authority_id = authority_id
        self.authority_version = authority_version
        self._principal_authority = principal_authority
        self._ingress_store = ingress_store
        self._token = object()

    async def issue(
        self,
        candidate: EvidenceCandidate,
        principal: AuthenticatedHumanPrincipal,
        *,
        ingress_idempotency_key: str,
        ingress_record_version: str = "v1",
        provided_at: datetime | None = None,
    ) -> EvidenceCandidate:
        if not self._principal_authority.recognizes(principal):
            raise ValueError("Human principal is not authenticated by the ingress authority")
        if (
            candidate.issuer.owner_type is not self.issuer_type
            or candidate.issuer.owner_id != self.authority_id
            or candidate.issuer.owner_version != self.authority_version
            or candidate.human_producer_category
            is not HumanEvidenceProducerCategory.HUMAN_DIRECT_EVIDENCE
            or candidate.human_ingress_record_ref is not None
            or not candidate.producer_work_run_id
            or not ingress_idempotency_key
            or not ingress_record_version
        ):
            raise ValueError("Human direct candidate binding is incomplete")
        ingress_record_id = "human-ingress-" + canonical_hash(
            {
                "authority": [self.authority_id, self.authority_version],
                "idempotency_key": ingress_idempotency_key,
            }
        )
        provided = (provided_at or candidate.observed_at).astimezone(UTC)
        issued_at = datetime.now(UTC)
        provisional_ref = HumanDirectEvidenceIngressRef(
            ingress_record_id,
            ingress_record_version,
            "",
        )
        provisional = HumanDirectEvidenceIngress(
            provisional_ref,
            candidate.candidate_id,
            candidate.candidate_version,
            principal.principal_id,
            principal.session_id,
            principal.authority_id,
            principal.authority_version,
            principal.authenticated_at.astimezone(UTC),
            self.authority_id,
            self.authority_version,
            candidate.task_contract_id,
            candidate.task_contract_version,
            candidate.producer_work_run_id,
            candidate.checkpoint_ref,
            candidate.evidence_type_id,
            candidate.evidence_type_version,
            candidate.subject_id,
            candidate.scope_id,
            candidate.resource_id,
            candidate.content_ref,
            provided,
            issued_at,
            f"{self.authority_id}@{self.authority_version}",
            self._token,
        )
        ingress_ref = replace(
            provisional_ref,
            fingerprint=human_ingress_fingerprint(provisional),
        )
        record = replace(provisional, ref=ingress_ref)
        await self._ingress_store.persist_human_ingress(record)
        value = replace(
            candidate,
            human_ingress_record_ref=record.ref.serialized(),
            producer_attestation_ref=record.ref.serialized(),
            observed_at=provided,
            _issuer_token=self._token,
        )
        value = replace(value, candidate_fingerprint=candidate_fingerprint(value))
        return value

    async def recognizes(self, candidate: EvidenceCandidate) -> bool:
        if (
            candidate.issuer.owner_type is not self.issuer_type
            or candidate.issuer.owner_id != self.authority_id
            or candidate.issuer.owner_version != self.authority_version
            or candidate.human_producer_category
            is not HumanEvidenceProducerCategory.HUMAN_DIRECT_EVIDENCE
            or not candidate.human_ingress_record_ref
            or candidate.candidate_fingerprint != candidate_fingerprint(candidate)
        ):
            return False
        record = await self._ingress_store.load_human_ingress(candidate.human_ingress_record_ref)
        return bool(record and _human_ingress_matches(record, candidate, self))


def human_ingress_fingerprint(value: HumanDirectEvidenceIngress) -> str:
    return canonical_hash(
        {
            "record": [value.ref.ingress_record_id, value.ref.ingress_record_version],
            "candidate": [value.candidate_id, value.candidate_version],
            "principal": [
                value.authenticated_principal_id,
                value.authenticated_session_id,
                value.principal_authority_id,
                value.principal_authority_version,
                value.authenticated_at.isoformat(),
            ],
            "ingress_authority": [
                value.ingress_authority_id,
                value.ingress_authority_version,
                value.issuer_authenticity_ref,
            ],
            "task": [value.task_contract_id, value.task_contract_version],
            "run": value.work_run_id,
            "checkpoint": value.checkpoint_ref.serialized(),
            "type": [value.evidence_type_id, value.evidence_type_version],
            "subject": [value.subject_id, value.scope_id, value.resource_id],
            "content": [
                value.content_ref.content_kind.value,
                value.content_ref.owner_id,
                value.content_ref.owner_version,
                value.content_ref.object_id,
                value.content_ref.object_version,
                value.content_ref.content_hash,
                value.content_ref.byte_count,
                value.content_ref.sensitivity.value,
            ],
            "provided_at": value.provided_at.isoformat(),
        }
    )


def _human_ingress_matches(
    record: HumanDirectEvidenceIngress,
    candidate: EvidenceCandidate,
    authority: HumanDirectEvidenceIngressAuthority,
) -> bool:
    return bool(
        record.ref.fingerprint == human_ingress_fingerprint(record)
        and record.ingress_authority_id == authority.authority_id
        and record.ingress_authority_version == authority.authority_version
        and record.issuer_authenticity_ref
        == f"{authority.authority_id}@{authority.authority_version}"
        and record.principal_authority_id == authority._principal_authority.authority_id
        and record.principal_authority_version == authority._principal_authority.authority_version
        and record.authenticated_principal_id
        and record.authenticated_session_id
        and record.candidate_id == candidate.candidate_id
        and record.candidate_version == candidate.candidate_version
        and record.task_contract_id == candidate.task_contract_id
        and record.task_contract_version == candidate.task_contract_version
        and record.work_run_id == candidate.producer_work_run_id
        and record.checkpoint_ref == candidate.checkpoint_ref
        and record.evidence_type_id == candidate.evidence_type_id
        and record.evidence_type_version == candidate.evidence_type_version
        and record.subject_id == candidate.subject_id
        and record.scope_id == candidate.scope_id
        and record.resource_id == candidate.resource_id
        and record.content_ref == candidate.content_ref
        and record.provided_at == candidate.observed_at.astimezone(UTC)
        and candidate.producer_attestation_ref == record.ref.serialized()
    )


class P1_5EvidenceIssuerAuthority:
    """Seeds candidates from verified immutable P1-5 refs; does not admit them."""

    _KIND = {
        EvidenceIssuerType.P1_5_EXECUTION_SUBMISSION: "ExecutionSubmissionRef",
        EvidenceIssuerType.P1_5_AGENT_OUTPUT: "AgentOutputRef",
        EvidenceIssuerType.P1_5_TOOL_OUTPUT: "ToolOutputRef",
        EvidenceIssuerType.P1_5_EXECUTION_ARTIFACT: "ExecutionArtifactRef",
    }

    def __init__(
        self,
        issuer_type: EvidenceIssuerType,
        issuer_id: str,
        issuer_version: str,
        resolver: P1_5ImmutableRefResolver,
    ) -> None:
        if issuer_type not in self._KIND:
            raise ValueError("P1-5 evidence issuer requires an exact P1-5 producer category")
        self._issuer_type = issuer_type
        self.issuer_id = issuer_id
        self.issuer_version = issuer_version
        self._resolver = resolver
        self._token = object()

    @property
    def issuer_type(self) -> EvidenceIssuerType:
        return self._issuer_type

    def seed_candidate(self, candidate: EvidenceCandidate) -> EvidenceCandidate:
        from aiscc.providers.external_ide import ISSUER

        if candidate.issuer.owner_id == ISSUER:
            raise ValueError("external IDE candidate requires durable pre-verification")
        if (
            candidate.issuer.owner_type is not self.issuer_type
            or candidate.issuer.owner_id != self.issuer_id
            or candidate.issuer.owner_version != self.issuer_version
            or not candidate.producer_work_run_id
            or not candidate.execution_attempt_id
        ):
            raise ValueError("P1-5 producer candidate binding is incomplete")
        value = replace(candidate, _issuer_token=self._token)
        return replace(value, candidate_fingerprint=candidate_fingerprint(value))

    async def seed_external_candidate(self, candidate: EvidenceCandidate, repository):
        from aiscc.providers.external_ide import ExternalIdeExecutionRepository

        if (
            type(repository) is not ExternalIdeExecutionRepository
            or candidate.issuer.owner_type is not self.issuer_type
            or candidate.issuer.owner_id != self.issuer_id
            or candidate.issuer.owner_version != self.issuer_version
        ):
            raise ValueError("P1-5 durable external owner required")
        verified = await repository.resolve(candidate.producer_attestation_ref)
        if not external_candidate_matches(candidate, verified):
            raise ValueError("external candidate producer binding differs")
        value = replace(candidate, _issuer_token=self._token)
        return replace(value, candidate_fingerprint=candidate_fingerprint(value))

    async def recognizes(self, candidate: EvidenceCandidate) -> bool:
        if (
            candidate._issuer_token is not self._token
            or candidate.candidate_fingerprint != candidate_fingerprint(candidate)
            or not candidate.producer_work_run_id
            or not candidate.execution_attempt_id
        ):
            return False
        from aiscc.providers.external_ide import ISSUER, ExternalIdeExecutionRepository

        if candidate.issuer.owner_id == ISSUER:
            if type(self._resolver) is not ExternalIdeExecutionRepository:
                return False
            try:
                verified = await self._resolver.resolve(candidate.producer_attestation_ref)
                return external_candidate_matches(candidate, verified)
            except ValueError:
                return False
        return await self._resolver.verify(
            ref_id=candidate.producer_attestation_ref,
            expected_kind=self._KIND[self.issuer_type],
            work_run_id=candidate.producer_work_run_id,
            execution_attempt_id=candidate.execution_attempt_id,
            content_hash=candidate.content_ref.content_hash,
        )


def external_candidate_matches(candidate, verified):
    """Exact binding only; durable P1-5 verification must precede this comparison."""
    from aiscc.providers.external_ide import ISSUER, VERSION

    ref = verified.common_ref
    return (
        candidate.issuer.owner_type is EvidenceIssuerType.P1_5_EXECUTION_SUBMISSION
        and candidate.issuer.owner_id == ISSUER
        and candidate.issuer.owner_version == VERSION
        and candidate.issuer.authority_ref == f"{ISSUER}@{VERSION}"
        and candidate.producer_work_run_id == ref.work_run_id
        and candidate.execution_attempt_id == ref.execution_attempt_id
        and candidate.operation_id is None
        and candidate.task_contract_id == ref.task_contract_id
        and candidate.task_contract_version == ref.task_contract_version
        and candidate.observed_state is ref.state
        and candidate.observed_state_version == ref.state_version
        and candidate.producer_attestation_ref == ref.submission_id
        and candidate.content_ref.object_id == ref.submission_id
        and candidate.content_ref.content_hash == ref.event_range_hash
        and candidate.content_ref.content_kind.value == "P1_5_IMMUTABLE_PRODUCER_REF"
        and candidate.content_ref.owner_id == ISSUER
        and candidate.content_ref.owner_version == VERSION
        and candidate.content_ref.object_version == VERSION
        and candidate.content_ref.schema_id == "AISCC-EXTERNAL-IDE-SUBMISSION-V1"
        and candidate.content_ref.schema_version == VERSION
        and candidate.content_ref.canonicalization == "P1_5_IMMUTABLE_REF_EXACT_BYTES"
        and candidate.content_ref.byte_count == len(verified.submission.canonical_body)
    )


def candidate_fingerprint(value: EvidenceCandidate) -> str:
    return canonical_hash(
        {
            "candidate": [value.candidate_id, value.candidate_version],
            "issuer": [
                value.issuer.owner_type.value,
                value.issuer.owner_id,
                value.issuer.owner_version,
                value.issuer.authority_ref,
            ],
            "producer": [
                value.producer_work_run_id,
                value.execution_attempt_id,
                value.operation_id,
            ],
            "task": [value.task_contract_id, value.task_contract_version],
            "checkpoint": value.checkpoint_ref.serialized(),
            "state": [value.observed_state.value, value.observed_state_version],
            "subject": [value.subject_id, value.scope_id, value.resource_id],
            "type": [value.evidence_type_id, value.evidence_type_version],
            "content": [
                value.content_ref.content_kind.value,
                value.content_ref.owner_id,
                value.content_ref.owner_version,
                value.content_ref.object_id,
                value.content_ref.object_version,
                value.content_ref.content_hash,
                value.content_ref.byte_count,
                value.content_ref.sensitivity.value,
            ],
            "times": [value.created_at.isoformat(), value.observed_at.isoformat()],
            "coverage": sorted(value.coverage),
            "attestation": value.producer_attestation_ref,
            "human": [
                value.human_producer_category.value
                if value.human_producer_category is not None
                else None,
                value.human_ingress_record_ref,
            ],
            "prior": value.prior_admitted_evidence_ref,
            "config": value.config_version,
        }
    )


class PriorAdmittedEvidenceIssuerAuthority:
    """Creates a new reuse candidate; an old admission never becomes current authority itself."""

    issuer_type = EvidenceIssuerType.PRIOR_ADMITTED_EVIDENCE

    def __init__(
        self,
        repository: PostgresEvidenceRepository,
        issuer_id: str = "AISCC_P1_6_REUSE_AUTHORITY_V1",
        issuer_version: str = "p1-6-reuse-v1",
    ) -> None:
        self._repository = repository
        self.issuer_id = issuer_id
        self.issuer_version = issuer_version
        self._token = object()

    async def seed_candidate(self, candidate: EvidenceCandidate) -> EvidenceCandidate:
        if (
            candidate.issuer.owner_type is not self.issuer_type
            or not candidate.prior_admitted_evidence_ref
        ):
            raise ValueError("reuse candidate requires an exact prior admission ref")
        prior = await self._repository.load_admitted(candidate.prior_admitted_evidence_ref)
        if prior is None:
            raise ValueError("prior admission is unavailable or revoked")
        if (
            prior.content_ref.content_hash != candidate.content_ref.content_hash
            or prior.content_ref.object_id != candidate.content_ref.object_id
        ):
            raise ValueError("reuse candidate content differs from prior admission")
        value = replace(candidate, _issuer_token=self._token)
        return replace(value, candidate_fingerprint=candidate_fingerprint(value))

    async def recognizes(self, candidate: EvidenceCandidate) -> bool:
        if (
            candidate._issuer_token is not self._token
            or candidate.candidate_fingerprint != candidate_fingerprint(candidate)
            or not candidate.prior_admitted_evidence_ref
        ):
            return False
        return (
            await self._repository.load_admitted(candidate.prior_admitted_evidence_ref) is not None
        )


class P1_7HumanEvidenceIssuerAuthority:
    """Durable HUMAN_P1_7 producer verifier; it seeds candidates but never admits evidence."""

    issuer_type = EvidenceIssuerType.HUMAN_P1_7

    def __init__(
        self,
        repository: PostgresHumanAuthorityRepository,
        issuer_id: str = "AISCC_P1_7_HUMAN_EVIDENCE_PRODUCER_V1",
        issuer_version: str = "p1-7-producer-authority-v1",
    ) -> None:
        self._repository = repository
        self.issuer_id = issuer_id
        self.issuer_version = issuer_version
        self._token = object()

    async def seed_candidate(self, candidate: EvidenceCandidate) -> EvidenceCandidate:
        if (
            candidate.issuer.owner_type is not self.issuer_type
            or candidate.issuer.owner_id != self.issuer_id
            or candidate.issuer.owner_version != self.issuer_version
            or candidate.human_producer_category is not HumanEvidenceProducerCategory.HUMAN_P1_7
        ):
            raise ValueError("HUMAN_P1_7 candidate owner/category binding is incomplete")
        producer = await self._repository.load_producer_ref(candidate.producer_attestation_ref)
        if producer is None or not _p1_7_producer_matches(producer, candidate):
            raise ValueError("HUMAN_P1_7 producer ref is unavailable or mismatched")
        value = replace(candidate, _issuer_token=self._token)
        return replace(value, candidate_fingerprint=candidate_fingerprint(value))

    async def recognizes(self, candidate: EvidenceCandidate) -> bool:
        if (
            candidate._issuer_token is not self._token
            or candidate.candidate_fingerprint != candidate_fingerprint(candidate)
            or candidate.human_producer_category is not HumanEvidenceProducerCategory.HUMAN_P1_7
        ):
            return False
        producer = await self._repository.load_producer_ref(candidate.producer_attestation_ref)
        return producer is not None and _p1_7_producer_matches(producer, candidate)


def _p1_7_producer_matches(producer: object, candidate: EvidenceCandidate) -> bool:
    from aiscc.human.models import HumanP1_7EvidenceProducerRef

    if not isinstance(producer, HumanP1_7EvidenceProducerRef):
        return False
    return bool(
        producer.task_contract_id == candidate.task_contract_id
        and producer.task_contract_version == candidate.task_contract_version
        and producer.work_run_id == candidate.producer_work_run_id
        and producer.source_state is candidate.observed_state
        and producer.state_version == candidate.observed_state_version
        and producer.checkpoint_ref == candidate.checkpoint_ref.serialized()
        and producer.evidence_type_id == candidate.evidence_type_id
        and producer.evidence_type_version == candidate.evidence_type_version
        and producer.subject_id == candidate.subject_id
        and producer.scope_id == candidate.scope_id
        and producer.resource_id == candidate.resource_id
        and producer.content_hash == candidate.content_ref.content_hash
        and producer.sensitivity is candidate.content_ref.sensitivity
    )
