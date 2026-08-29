from __future__ import annotations

from datetime import datetime

from aiscc.contracts.workflow import WorkflowState
from aiscc.evidence.models import (
    EvidenceCheckpointRef,
    EvidenceSetEvaluation,
    EvidenceSetSatisfactionAttestation,
)
from aiscc.evidence.repository import PostgresEvidenceRepository


class EvidenceSetEvaluator:
    def __init__(
        self,
        repository: PostgresEvidenceRepository,
        *,
        authority_id: str = "AISCC_P1_6_G_EVIDENCE_AUTHORITY_V1",
        authority_version: str = "AISCC-P1-6-EVIDENCE-AUTHORITY-V1",
    ) -> None:
        self._repository = repository
        self.authority_id = authority_id
        self.authority_version = authority_version

    async def evaluate(
        self,
        *,
        work_run_id: str,
        checkpoint_ref: EvidenceCheckpointRef,
        source_state: WorkflowState,
        state_version: int,
        now: datetime | None = None,
    ) -> tuple[EvidenceSetEvaluation, EvidenceSetSatisfactionAttestation | None]:
        return await self._repository.evaluate_set(
            work_run_id=work_run_id,
            checkpoint_ref=checkpoint_ref,
            observed_state=source_state,
            observed_state_version=state_version,
            authority_id=self.authority_id,
            authority_version=self.authority_version,
            now=now,
        )
