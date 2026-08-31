from __future__ import annotations

from typing import Protocol

from aiscc.evidence.models import (
    EvidenceCandidate,
    EvidenceContentRef,
    EvidenceIssuerType,
    HistoricalContentAccessGrant,
    HumanDirectEvidenceIngress,
    VerifiedHistoricalContent,
    VerifiedHistoricalContentMetadata,
)


class EvidenceContentResolver(Protocol):
    def resolve(self, ref: EvidenceContentRef) -> bytes | None: ...


class DurableHistoricalContentResolver(Protocol):
    async def verify_historical_content_ref(
        self,
        content_ref: EvidenceContentRef,
        *,
        expected_payload_fingerprint: str | None = None,
    ) -> VerifiedHistoricalContentMetadata: ...

    async def resolve_historical_canonical_body(
        self,
        content_ref: EvidenceContentRef,
        *,
        access_grant: HistoricalContentAccessGrant,
    ) -> VerifiedHistoricalContent: ...

    async def verify_historical_admitted_evidence_with_content(
        self,
        *,
        admitted_evidence_ref: str,
        exact_terminal_attestation_ref: str,
        access_grant: HistoricalContentAccessGrant,
    ) -> VerifiedHistoricalContent: ...


class EvidenceIssuerVerifier(Protocol):
    @property
    def issuer_type(self) -> EvidenceIssuerType: ...

    async def recognizes(self, candidate: EvidenceCandidate) -> bool: ...


class P1_5ImmutableRefResolver(Protocol):
    async def verify(
        self,
        *,
        ref_id: str,
        expected_kind: str,
        work_run_id: str,
        execution_attempt_id: str,
        content_hash: str,
    ) -> bool: ...


class HumanDirectEvidenceIngressStore(Protocol):
    async def persist_human_ingress(self, value: HumanDirectEvidenceIngress) -> None: ...

    async def load_human_ingress(
        self, serialized_ref: str
    ) -> HumanDirectEvidenceIngress | None: ...
