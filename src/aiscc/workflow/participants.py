from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from aiscc.workflow.guards import TrustedGuardFact
from aiscc.workflow.models import (
    TransitionDecision,
    TransitionEvaluation,
    TransitionRequest,
    WorkRun,
)
from aiscc.workflow.ports import TransitionTransactionParticipant


class CompositeTransitionParticipant:
    """Deterministic composition of independent semantic-owner transaction participants."""

    def __init__(self, participants: tuple[TransitionTransactionParticipant, ...]) -> None:
        self._participants = participants

    def facts(self, request: TransitionRequest) -> tuple[TrustedGuardFact, ...]:
        return tuple(fact for item in self._participants for fact in item.facts(request))

    async def prepare(
        self, session: AsyncSession, request: TransitionRequest, current: WorkRun | None
    ) -> None:
        for item in self._participants:
            await item.prepare(session, request, current)

    def after_evaluation(self, request: TransitionRequest) -> None:
        for item in reversed(self._participants):
            item.after_evaluation(request)

    async def after_decision(
        self,
        session: AsyncSession,
        request: TransitionRequest,
        evaluation: TransitionEvaluation,
        decision: TransitionDecision,
        current: WorkRun | None,
    ) -> None:
        for item in self._participants:
            await item.after_decision(session, request, evaluation, decision, current)
