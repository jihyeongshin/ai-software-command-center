from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from aiscc.contracts.workflow import RuntimeMode, WorkflowState


class GuardId(StrEnum):
    G_CURRENT = "G_CURRENT"
    G_CONTRACT = "G_CONTRACT"
    G_SCOPE = "G_SCOPE"
    G_RUNTIME_CONTEXT = "G_RUNTIME_CONTEXT"
    G_EXECUTION_STARTED = "G_EXECUTION_STARTED"
    G_EXECUTOR_SUBMISSION = "G_EXECUTOR_SUBMISSION"
    G_EVIDENCE = "G_EVIDENCE"
    G_HUMAN_REQUIRED = "G_HUMAN_REQUIRED"
    G_HUMAN_NOT_REQUIRED = "G_HUMAN_NOT_REQUIRED"
    G_NO_PENDING_HUMAN_GATE = "G_NO_PENDING_HUMAN_GATE"
    G_SUSPENDED_HUMAN_GATE = "G_SUSPENDED_HUMAN_GATE"
    G_RESUMABLE_HUMAN_GATE = "G_RESUMABLE_HUMAN_GATE"
    G_HUMAN_APPROVED = "G_HUMAN_APPROVED"
    G_HUMAN_REWORK = "G_HUMAN_REWORK"
    G_HUMAN_REJECTED = "G_HUMAN_REJECTED"
    G_JUDGMENT_ACCEPTED = "G_JUDGMENT_ACCEPTED"
    G_JUDGMENT_REJECTED = "G_JUDGMENT_REJECTED"
    G_JUDGMENT_REWORK = "G_JUDGMENT_REWORK"
    G_BLOCKER = "G_BLOCKER"
    G_BLOCKER_RESOLVED = "G_BLOCKER_RESOLVED"
    G_REWORK_SPEC = "G_REWORK_SPEC"
    G_FAILURE_TERMINAL = "G_FAILURE_TERMINAL"


class GuardSemanticOwner(StrEnum):
    P1_4_SYSTEM = "P1_4_SYSTEM"
    P1_6_EVIDENCE = "P1_6_EVIDENCE"
    P1_7_HUMAN = "P1_7_HUMAN"
    P1_7_JUDGMENT = "P1_7_JUDGMENT"


class RequesterType(StrEnum):
    SYSTEM = "SYSTEM"
    AGENT = "AGENT"
    EXECUTOR = "EXECUTOR"
    HUMAN = "HUMAN"
    COMMAND_CENTER = "COMMAND_CENTER"
    OPERATOR = "OPERATOR"


class DecisionOutcome(StrEnum):
    ADMITTED = "ADMITTED"
    DENIED = "DENIED"


class DecisionReason(StrEnum):
    ADMITTED = "ADMITTED"
    STALE_REQUEST = "STALE_REQUEST"
    INVALID_TRANSITION = "INVALID_TRANSITION"
    MISSING_GUARD = "MISSING_GUARD"
    GUARD_FAILED = "GUARD_FAILED"
    CONTRACT_MISMATCH = "CONTRACT_MISMATCH"
    RUNTIME_MODE_MISMATCH = "RUNTIME_MODE_MISMATCH"


class RequestIdentityConflictError(RuntimeError):
    """A request ID was reused with different immutable request/fact content."""


class AuthorityConflictError(RuntimeError):
    """The durable projection cannot be reconstructed from admitted provenance."""


@dataclass(frozen=True, slots=True)
class WorkRun:
    project_id: str
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    state: WorkflowState
    state_version: int
    runtime_mode: RuntimeMode
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class TransitionRequest:
    transition_request_id: str
    project_id: str
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    observed_state: WorkflowState | None
    observed_state_version: int
    target_state: WorkflowState
    requester_identity: str
    requester_type: RequesterType
    runtime_mode: RuntimeMode
    evidence_refs: tuple[str, ...] = ()
    human_result_refs: tuple[str, ...] = ()
    judgment_refs: tuple[str, ...] = ()
    parent_request_id: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def __post_init__(self) -> None:
        required = (
            self.transition_request_id,
            self.project_id,
            self.task_contract_id,
            self.task_contract_version,
            self.work_run_id,
            self.requester_identity,
        )
        if any(not value for value in required):
            raise ValueError("transition request identifiers must be non-empty")
        if self.observed_state is None and self.observed_state_version != 0:
            raise ValueError("NONE observation requires state_version 0")
        if self.observed_state is not None and self.observed_state_version < 1:
            raise ValueError("existing state observation requires a positive state_version")
        if self.created_at.tzinfo is None:
            raise ValueError("transition request timestamp must be timezone-aware")


@dataclass(frozen=True, slots=True)
class GuardObservation:
    guard_id: GuardId
    semantic_owner: GuardSemanticOwner
    satisfied: bool
    reason: str
    authority_ref: str
    bound_refs: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class TransitionEvaluation:
    transition_evaluation_id: str
    transition_request_id: str
    authoritative_state: WorkflowState | None
    authoritative_state_version: int
    guards: tuple[GuardObservation, ...]
    missing_guards: tuple[GuardId, ...]
    evaluated_at: datetime


@dataclass(frozen=True, slots=True)
class TransitionDecision:
    transition_decision_id: str
    transition_evaluation_id: str
    transition_request_id: str
    outcome: DecisionOutcome
    reason: DecisionReason
    resulting_state: WorkflowState | None
    resulting_state_version: int
    admitting_owner: str
    kernel_version: str
    decided_at: datetime
