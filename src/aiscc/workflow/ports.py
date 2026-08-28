from __future__ import annotations

from collections.abc import Callable
from enum import StrEnum
from typing import Protocol

from aiscc.workflow.guards import TrustedGuardFact
from aiscc.workflow.models import TransitionDecision, TransitionRequest, WorkRun


class FailurePoint(StrEnum):
    AFTER_PROVENANCE_BEFORE_PROJECTION = "AFTER_PROVENANCE_BEFORE_PROJECTION"
    AFTER_PROJECTION_BEFORE_COMMIT = "AFTER_PROJECTION_BEFORE_COMMIT"


FailureInjector = Callable[[FailurePoint], None]


class TransitionRepository(Protocol):
    async def decide(
        self,
        request: TransitionRequest,
        facts: tuple[TrustedGuardFact, ...],
        *,
        failure_injector: FailureInjector | None = None,
    ) -> TransitionDecision: ...

    async def get_work_run(self, work_run_id: str) -> WorkRun | None: ...

    async def get_decision(self, transition_request_id: str) -> TransitionDecision | None: ...

    async def verify_consistency(self, work_run_id: str) -> WorkRun: ...
