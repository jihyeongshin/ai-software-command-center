from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class WorkflowState(StrEnum):
    READY = "READY"
    RUNNING = "RUNNING"
    ADMISSION_PENDING = "ADMISSION_PENDING"
    HUMAN_REQUIRED = "HUMAN_REQUIRED"
    BLOCKED = "BLOCKED"
    REWORK_REQUIRED = "REWORK_REQUIRED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


class RuntimeMode(StrEnum):
    OWNER_SELF_DOGFOOD = "OWNER_SELF_DOGFOOD"
    PUBLIC_RECORDED_REPLAY = "PUBLIC_RECORDED_REPLAY"
    PUBLIC_BOUNDED_LIVE = "PUBLIC_BOUNDED_LIVE"


@dataclass(frozen=True, slots=True)
class WorkflowSnapshot:
    """Immutable security input fixture/interface, not authoritative workflow state."""

    run_id: str
    state: WorkflowState
    state_version: int

    def __post_init__(self) -> None:
        if not self.run_id or self.state_version < 1:
            raise ValueError("workflow snapshot requires run_id and positive state_version")
