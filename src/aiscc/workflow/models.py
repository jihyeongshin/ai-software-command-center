from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from aiscc.contracts.canonical_json import canonical_sha256
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


class BlockerKindV1(StrEnum):
    SECURITY = "SECURITY"
    POLICY = "POLICY"
    ARTIFACT = "ARTIFACT"
    BASELINE = "BASELINE"
    AUTHORITY = "AUTHORITY"
    EXTERNAL_DEPENDENCY = "EXTERNAL_DEPENDENCY"
    EXECUTION = "EXECUTION"


class BlockerReasonCodeV1(StrEnum):
    SECURITY_BOUNDARY = "SECURITY_BOUNDARY"
    POLICY_CONFLICT = "POLICY_CONFLICT"
    MISSING_REQUIRED_ARTIFACT = "MISSING_REQUIRED_ARTIFACT"
    BASELINE_GAP = "BASELINE_GAP"
    AUTHORITY_CONFLICT = "AUTHORITY_CONFLICT"
    EXTERNAL_DEPENDENCY = "EXTERNAL_DEPENDENCY"
    EXECUTION_BLOCKER = "EXECUTION_BLOCKER"


class BlockerResumabilityV1(StrEnum):
    RESUMABLE = "RESUMABLE"
    NON_RESUMABLE = "NON_RESUMABLE"


BLOCKER_TAXONOMY_V1 = {
    (
        BlockerKindV1.SECURITY,
        BlockerReasonCodeV1.SECURITY_BOUNDARY,
    ): BlockerResumabilityV1.NON_RESUMABLE,
    (BlockerKindV1.POLICY, BlockerReasonCodeV1.POLICY_CONFLICT): BlockerResumabilityV1.RESUMABLE,
    (
        BlockerKindV1.ARTIFACT,
        BlockerReasonCodeV1.MISSING_REQUIRED_ARTIFACT,
    ): BlockerResumabilityV1.RESUMABLE,
    (BlockerKindV1.BASELINE, BlockerReasonCodeV1.BASELINE_GAP): BlockerResumabilityV1.RESUMABLE,
    (
        BlockerKindV1.AUTHORITY,
        BlockerReasonCodeV1.AUTHORITY_CONFLICT,
    ): BlockerResumabilityV1.RESUMABLE,
    (
        BlockerKindV1.EXTERNAL_DEPENDENCY,
        BlockerReasonCodeV1.EXTERNAL_DEPENDENCY,
    ): BlockerResumabilityV1.RESUMABLE,
    (
        BlockerKindV1.EXECUTION,
        BlockerReasonCodeV1.EXECUTION_BLOCKER,
    ): BlockerResumabilityV1.RESUMABLE,
}

P1_4_BLOCKER_OWNER = "P1_4_SYSTEM_TRANSITION_AUTHORITY"
P1_4_BLOCKER_AUTHORITY_REF = "p1-4-system-transition-authority:blocker-provenance:v1"
P1_4_BLOCKER_AUTHORITY_VERSION = "AISCC-P1-4-BLOCKER-PROVENANCE-AUTHORITY-V1"
P1_4_BLOCKER_TAXONOMY_FINGERPRINT = (
    "ec170cd257b04e77410951abe8c7f196a88bf8f35d9e6deaec8d8889bb0e9d0c"
)


def _require_text(value: str, label: str) -> None:
    if not value:
        raise ValueError(f"{label} must be non-empty")


def _require_fingerprint(value: str, label: str) -> None:
    if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
        raise ValueError(f"{label} must be 64 lowercase hex characters")


@dataclass(frozen=True, slots=True)
class P1_4BlockerClaimV1:
    blocker_id: str
    blocker_kind: BlockerKindV1
    reason_code: BlockerReasonCodeV1
    resolution_source_contract_ref: str
    resolution_source_contract_fingerprint: str
    ordered_source_authority_refs: tuple[str, ...]
    ordered_source_authority_fingerprints: tuple[str, ...]

    def __post_init__(self) -> None:
        for value, label in (
            (self.blocker_id, "blocker_id"),
            (self.resolution_source_contract_ref, "resolution_source_contract_ref"),
        ):
            _require_text(value, label)
        _require_fingerprint(
            self.resolution_source_contract_fingerprint,
            "resolution_source_contract_fingerprint",
        )
        if (self.blocker_kind, self.reason_code) not in BLOCKER_TAXONOMY_V1:
            raise ValueError("blocker kind/reason pair is outside P1_4_BLOCKER_TAXONOMY_V1")
        if not self.ordered_source_authority_refs or len(self.ordered_source_authority_refs) != len(
            self.ordered_source_authority_fingerprints
        ):
            raise ValueError("ordered source authority refs/fingerprints must be paired")
        for ref in self.ordered_source_authority_refs:
            _require_text(ref, "ordered_source_authority_ref")
        for fingerprint in self.ordered_source_authority_fingerprints:
            _require_fingerprint(fingerprint, "ordered_source_authority_fingerprint")

    @property
    def blocker_ref(self) -> str:
        return f"p1-4-blocker:v1:{self.blocker_id}"

    @property
    def resumability(self) -> BlockerResumabilityV1:
        return BLOCKER_TAXONOMY_V1[(self.blocker_kind, self.reason_code)]

    def payload(self) -> dict[str, object]:
        return {
            "blocker_id": self.blocker_id,
            "blocker_kind": self.blocker_kind.value,
            "reason_code": self.reason_code.value,
            "resolution_source_contract_ref": self.resolution_source_contract_ref,
            "resolution_source_contract_fingerprint": (self.resolution_source_contract_fingerprint),
            "ordered_source_authority_refs": list(self.ordered_source_authority_refs),
            "ordered_source_authority_fingerprints": list(
                self.ordered_source_authority_fingerprints
            ),
        }


@dataclass(frozen=True, slots=True)
class P1_4BlockerResolutionClaimV1:
    blocker_ref: str
    blocker_fingerprint: str
    resolution_source_ref: str
    resolution_source_fingerprint: str
    resolution_source_authority_ref: str
    resolution_source_authority_fingerprint: str

    def __post_init__(self) -> None:
        for value, label in (
            (self.blocker_ref, "blocker_ref"),
            (self.resolution_source_ref, "resolution_source_ref"),
            (self.resolution_source_authority_ref, "resolution_source_authority_ref"),
        ):
            _require_text(value, label)
        for value, label in (
            (self.blocker_fingerprint, "blocker_fingerprint"),
            (self.resolution_source_fingerprint, "resolution_source_fingerprint"),
            (
                self.resolution_source_authority_fingerprint,
                "resolution_source_authority_fingerprint",
            ),
        ):
            _require_fingerprint(value, label)

    def payload(self) -> dict[str, str]:
        return {
            "blocker_ref": self.blocker_ref,
            "blocker_fingerprint": self.blocker_fingerprint,
            "resolution_source_ref": self.resolution_source_ref,
            "resolution_source_fingerprint": self.resolution_source_fingerprint,
            "resolution_source_authority_ref": self.resolution_source_authority_ref,
            "resolution_source_authority_fingerprint": (
                self.resolution_source_authority_fingerprint
            ),
        }


@dataclass(frozen=True, slots=True)
class P1_4BlockerProvenanceV1:
    payload_without_fingerprint: dict[str, object]
    blocker_fingerprint: str

    def __post_init__(self) -> None:
        _require_fingerprint(self.blocker_fingerprint, "blocker_fingerprint")
        if canonical_sha256(self.payload_without_fingerprint) != self.blocker_fingerprint:
            raise ValueError("blocker provenance fingerprint mismatch")

    @property
    def blocker_ref(self) -> str:
        return str(self.payload_without_fingerprint["blocker_ref"])

    def payload(self) -> dict[str, object]:
        return {**self.payload_without_fingerprint, "blocker_fingerprint": self.blocker_fingerprint}


@dataclass(frozen=True, slots=True)
class P1_4BlockerResolvedAttestationV1:
    payload_without_fingerprint: dict[str, object]
    attestation_fingerprint: str

    def __post_init__(self) -> None:
        _require_fingerprint(self.attestation_fingerprint, "attestation_fingerprint")
        if canonical_sha256(self.payload_without_fingerprint) != self.attestation_fingerprint:
            raise ValueError("blocker resolution attestation fingerprint mismatch")

    @property
    def attestation_ref(self) -> str:
        return str(self.payload_without_fingerprint["attestation_ref"])

    def payload(self) -> dict[str, object]:
        return {
            **self.payload_without_fingerprint,
            "attestation_fingerprint": self.attestation_fingerprint,
        }


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
    blocker_claim: P1_4BlockerClaimV1 | None = None
    blocker_resolution_claim: P1_4BlockerResolutionClaimV1 | None = None
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
        if self.blocker_claim is not None and self.blocker_resolution_claim is not None:
            raise ValueError("a request cannot both create and resolve a blocker")


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
