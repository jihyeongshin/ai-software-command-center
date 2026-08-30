from __future__ import annotations

from aiscc.workflow.guards import TrustedGuardFact
from aiscc.workflow.models import TransitionDecision, TransitionRequest, WorkRun
from aiscc.workflow.ports import (
    FailureInjector,
    TransitionRepository,
    TransitionTransactionParticipant,
)


class WorkflowKernel:
    """System-owned transition entrypoint; no HTTP/caller asserted-fact mutation API."""

    def __init__(
        self,
        repository: TransitionRepository,
    ) -> None:
        self._repository = repository

    async def request_transition(
        self,
        request: TransitionRequest,
        facts: tuple[TrustedGuardFact, ...],
        *,
        failure_injector: FailureInjector | None = None,
        transaction_participant: TransitionTransactionParticipant | None = None,
    ) -> TransitionDecision:
        return await self._repository.decide(
            request,
            facts,
            failure_injector=failure_injector,
            transaction_participant=transaction_participant,
        )

    async def load(self, work_run_id: str) -> WorkRun | None:
        return await self._repository.get_work_run(work_run_id)

    async def verify_consistency(self, work_run_id: str) -> WorkRun:
        return await self._repository.verify_consistency(work_run_id)
