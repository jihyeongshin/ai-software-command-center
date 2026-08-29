from __future__ import annotations

from datetime import datetime
from typing import Protocol

from aiscc.evidence.admission import EvidenceAdmissionEvaluator
from aiscc.evidence.models import (
    AdmittedEvidence,
    EvidenceAdmissionDecision,
    EvidenceAdmissionRequest,
    EvidenceAuthorityEventKind,
    EvidenceCandidate,
)
from aiscc.evidence.repository import PostgresEvidenceRepository


class AttestationInvalidator(Protocol):
    def invalidate(self, serialized_ref: str) -> None: ...


class EvidenceAdmissionService:
    """Production P1-6 entrypoint; it owns evidence authority, never workflow mutation."""

    def __init__(
        self,
        repository: PostgresEvidenceRepository,
        evaluator: EvidenceAdmissionEvaluator,
        *,
        attestation_invalidator: AttestationInvalidator | None = None,
        authority_id: str = "AISCC_P1_6_EVIDENCE_AUTHORITY_V1",
        authority_version: str = "AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
    ) -> None:
        self._repository = repository
        self._evaluator = evaluator
        self._invalidator = attestation_invalidator
        self._authority_id = authority_id
        self._authority_version = authority_version

    async def submit(
        self,
        request: EvidenceAdmissionRequest,
        candidate: EvidenceCandidate,
        *,
        now: datetime | None = None,
    ) -> tuple[EvidenceAdmissionDecision, AdmittedEvidence | None]:
        return await self._repository.admit(
            request=request,
            candidate=candidate,
            evaluator=self._evaluator,
            now=now,
        )

    async def preserve_supplemental(self, candidate: EvidenceCandidate) -> None:
        await self._repository.preserve_supplemental_candidate(candidate)

    async def invalidate_authority(
        self,
        *,
        subject_ref: str,
        reason: str,
        replacement_ref: str | None = None,
        kind: EvidenceAuthorityEventKind = EvidenceAuthorityEventKind.REVOKED,
    ) -> None:
        await self._repository.revoke(
            subject_ref=subject_ref,
            reason=reason,
            owner_id=self._authority_id,
            authority_version=self._authority_version,
            replacement_ref=replacement_ref,
            kind=kind,
        )
        if self._invalidator is not None:
            self._invalidator.invalidate(subject_ref)
