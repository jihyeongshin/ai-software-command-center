from __future__ import annotations

from collections.abc import Callable
from enum import StrEnum
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from aiscc.workflow.guards import TrustedGuardFact
from aiscc.workflow.models import (
    TransitionDecision,
    TransitionEvaluation,
    TransitionRequest,
    WorkRun,
)


class FailurePoint(StrEnum):
    AFTER_PROVENANCE_BEFORE_PROJECTION = "AFTER_PROVENANCE_BEFORE_PROJECTION"
    AFTER_PROJECTION_BEFORE_COMMIT = "AFTER_PROJECTION_BEFORE_COMMIT"


FailureInjector = Callable[[FailurePoint], None]


class TransitionTransactionParticipant(Protocol):
    """Owner hook executed inside P1-4's canonical run transaction."""

    def facts(self, request: TransitionRequest) -> tuple[TrustedGuardFact, ...]: ...

    async def prepare(
        self,
        session: AsyncSession,
        request: TransitionRequest,
        current: WorkRun | None,
    ) -> None: ...

    def after_evaluation(self, request: TransitionRequest) -> None: ...

    async def after_decision(
        self,
        session: AsyncSession,
        request: TransitionRequest,
        evaluation: TransitionEvaluation,
        decision: TransitionDecision,
        current: WorkRun | None,
    ) -> None: ...


class TransitionRepository(Protocol):
    async def decide(
        self,
        request: TransitionRequest,
        facts: tuple[TrustedGuardFact, ...],
        *,
        failure_injector: FailureInjector | None = None,
        transaction_participant: TransitionTransactionParticipant | None = None,
    ) -> TransitionDecision: ...

    async def get_work_run(self, work_run_id: str) -> WorkRun | None: ...

    async def get_decision(self, transition_request_id: str) -> TransitionDecision | None: ...

    async def verify_consistency(self, work_run_id: str) -> WorkRun: ...
