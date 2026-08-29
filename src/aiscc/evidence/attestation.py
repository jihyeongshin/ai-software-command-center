from __future__ import annotations

from aiscc.evidence.models import (
    EvidenceCheckpoint,
    EvidenceCheckpointRef,
    EvidenceSetSatisfactionAttestation,
)
from aiscc.evidence.repository import PostgresEvidenceRepository
from aiscc.workflow.guards import TrustedGuardFact
from aiscc.workflow.models import GuardId, GuardSemanticOwner, TransitionRequest


class EvidenceCheckpointUseRegistry:
    """System-owned exact mapping from a transition/use context to one checkpoint."""

    def __init__(self, checkpoints: tuple[EvidenceCheckpoint, ...]) -> None:
        self._uses: dict[
            tuple[str, str, object, object, str | None, str | None], EvidenceCheckpointRef
        ] = {}
        for checkpoint in checkpoints:
            key = (
                checkpoint.task_contract_id,
                checkpoint.task_contract_version,
                checkpoint.source_state,
                checkpoint.target_state,
                checkpoint.transition_purpose_id,
                checkpoint.transition_purpose_version,
            )
            if key in self._uses:
                raise ValueError("ambiguous checkpoint authority for one exact use")
            self._uses[key] = checkpoint.ref

    def resolve_transition(self, request: TransitionRequest) -> EvidenceCheckpointRef | None:
        return self._uses.get(
            (
                request.task_contract_id,
                request.task_contract_version,
                request.observed_state,
                request.target_state,
                None,
                None,
            )
        )


class EvidenceGuardAuthority:
    """P1-6-only, durable-attestation-backed G_EVIDENCE authority/verifier."""

    semantic_owner = GuardSemanticOwner.P1_6_EVIDENCE

    def __init__(
        self,
        repository: PostgresEvidenceRepository,
        checkpoint_uses: EvidenceCheckpointUseRegistry,
        *,
        authority_id: str = "AISCC_P1_6_G_EVIDENCE_AUTHORITY_V1",
        authority_version: str = "AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
    ) -> None:
        self._repository = repository
        self._checkpoint_uses = checkpoint_uses
        self.authority_id = authority_id
        self.authority_version = authority_version
        self._token = object()
        self._loaded: dict[str, EvidenceSetSatisfactionAttestation] = {}

    async def issue_for_transition(self, request: TransitionRequest) -> TrustedGuardFact:
        if len(request.evidence_refs) != 1:
            raise ValueError("G_EVIDENCE requires exactly one attestation ref")
        expected_checkpoint = self._checkpoint_uses.resolve_transition(request)
        if expected_checkpoint is None:
            raise ValueError("no System-owned evidence checkpoint for transition use")
        ref = request.evidence_refs[0]
        attestation = await self._repository.load_effective_attestation(ref)
        if not self._matches(attestation, request, expected_checkpoint):
            raise ValueError("evidence attestation does not match exact transition authority")
        assert attestation is not None
        self._loaded[ref] = attestation
        return TrustedGuardFact(
            guard_id=GuardId.G_EVIDENCE,
            semantic_owner=self.semantic_owner,
            satisfied=True,
            reason="P1_6_EVIDENCE_SET_SATISFIED",
            authority_ref=ref,
            bound_refs=request.evidence_refs,
            task_contract_id=request.task_contract_id,
            task_contract_version=request.task_contract_version,
            work_run_id=request.work_run_id,
            state_version=request.observed_state_version,
            _issuer_token=self._token,
        )

    def recognizes(self, fact: TrustedGuardFact, request: TransitionRequest) -> bool:
        attestation = self._loaded.get(fact.authority_ref)
        expected_checkpoint = self._checkpoint_uses.resolve_transition(request)
        return bool(
            fact._issuer_token is self._token
            and expected_checkpoint is not None
            and self._matches(attestation, request, expected_checkpoint)
        )

    def invalidate(self, serialized_ref: str) -> None:
        self._loaded.pop(serialized_ref, None)

    def _matches(
        self,
        attestation: EvidenceSetSatisfactionAttestation | None,
        request: TransitionRequest,
        expected_checkpoint: EvidenceCheckpointRef,
    ) -> bool:
        return bool(
            attestation
            and attestation.satisfied
            and attestation.evidence_authority_version == self.authority_version
            and attestation.issuer_version == self.authority_version
            and attestation.task_contract_id == request.task_contract_id
            and attestation.task_contract_version == request.task_contract_version
            and attestation.work_run_id == request.work_run_id
            and attestation.source_state is request.observed_state
            and attestation.state_version == request.observed_state_version
            and attestation.target_state is request.target_state
            and attestation.transition_purpose_id is None
            and attestation.transition_purpose_version is None
            and attestation.checkpoint_ref == expected_checkpoint
            and request.evidence_refs == (attestation.serialized_ref,)
        )
