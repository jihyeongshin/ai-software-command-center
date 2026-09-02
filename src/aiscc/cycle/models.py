from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from aiscc.contracts.canonical_json import require_safe_integer
from aiscc.evidence.models import canonical_hash


class CycleAdmissionErrorCode(StrEnum):
    NOT_ACCEPTED_TERMINAL = "CYCLE_NOT_ACCEPTED_TERMINAL"
    FOREIGN_AUTHORITY = "CYCLE_FOREIGN_AUTHORITY"
    HISTORICAL_CORRUPTION = "CYCLE_HISTORICAL_CORRUPTION"
    IDENTITY_CONFLICT = "CYCLE_IDENTITY_CONFLICT"
    SOURCE_NOT_ELIGIBLE = "CYCLE_SOURCE_NOT_ELIGIBLE"
    POLICY_NOT_CURRENT = "CYCLE_POLICY_NOT_CURRENT"
    AUTHORITY_NOT_CURRENT = "CYCLE_AUTHORITY_NOT_CURRENT"
    UNSUPPORTED_MEMORY_CATEGORY = "MEMORY_CATEGORY_NOT_SUPPORTED"
    MEMORY_DECLARATION_SOURCE_MISMATCH = "MEMORY_DECLARATION_SOURCE_MISMATCH"
    MEMORY_POLICY_AUTHORITY_DENIED = "MEMORY_POLICY_AUTHORITY_ACCESS_DENIED"
    TERMINAL_EPOCH_CONFLICT = "TERMINAL_EPOCH_CONFLICT"
    TASK_BINDING_MISMATCH = "P1_8_TASK_BINDING_FINGERPRINT_MISMATCH"


class CycleAdmissionError(RuntimeError):
    def __init__(self, code: CycleAdmissionErrorCode, message: str) -> None:
        super().__init__(f"{code.value}: {message}")
        self.code = code


class MemoryCategory(StrEnum):
    DECISION = "DECISION"
    INVARIANT_POINTER = "INVARIANT_POINTER"
    CONSTRAINT_POINTER = "CONSTRAINT_POINTER"
    LESSON = "LESSON"
    BLOCKER_RESOLUTION = "BLOCKER_RESOLUTION"
    PROVENANCE_POINTER = "PROVENANCE_POINTER"
    NEXT_ACTION_CONTEXT = "NEXT_ACTION_CONTEXT"


@dataclass(frozen=True, slots=True)
class MemoryDeclaration:
    category: MemoryCategory
    subject_key: str
    applicability_key: str
    semantic_slot: str
    policy_ref: str
    policy_fingerprint: str
    claimed_content_fingerprint: str
    source_evidence_ref: str | None = None
    source_selector: str | None = None
    pointer_ref: str | None = None
    supersession_authority_ref: str | None = None
    source_object_kind: str | None = None
    source_schema_id: str | None = None
    source_schema_version: str | None = None
    source_privacy: str | None = None
    external_context_ref: str | None = None
    external_context_fingerprint: str | None = None
    external_context_introduction_event_ref: str | None = None
    external_context_introduction_event_fingerprint: str | None = None
    external_context_snapshot_ref: str | None = None
    external_context_snapshot_fingerprint: str | None = None
    external_context_event_high_watermark: int | None = None

    def __post_init__(self) -> None:
        external = (
            self.external_context_ref,
            self.external_context_fingerprint,
            self.external_context_introduction_event_ref,
            self.external_context_introduction_event_fingerprint,
            self.external_context_snapshot_ref,
            self.external_context_snapshot_fingerprint,
            self.external_context_event_high_watermark,
        )
        if self.category is MemoryCategory.NEXT_ACTION_CONTEXT:
            if any(value is None for value in external):
                raise ValueError("NEXT_ACTION_CONTEXT requires the complete external owner graph")
            require_safe_integer(
                self.external_context_event_high_watermark,
                label="external_context_event_high_watermark",
                minimum=1,
            )
        elif any(value is not None for value in external):
            raise ValueError("external context fields are non-applicable to this category")

    def payload(self) -> dict[str, Any]:
        return {
            "applicability_key": self.applicability_key,
            "category": self.category.value,
            "claimed_content_fingerprint": self.claimed_content_fingerprint,
            "pointer_ref": self.pointer_ref,
            "policy_fingerprint": self.policy_fingerprint,
            "policy_ref": self.policy_ref,
            "semantic_slot": self.semantic_slot,
            "source_evidence_ref": self.source_evidence_ref,
            "source_selector": self.source_selector,
            "subject_key": self.subject_key,
            "supersession_authority_ref": self.supersession_authority_ref,
            "source_object_kind": self.source_object_kind,
            "source_privacy": self.source_privacy,
            "source_schema_id": self.source_schema_id,
            "source_schema_version": self.source_schema_version,
            "external_context_ref": self.external_context_ref,
            "external_context_fingerprint": self.external_context_fingerprint,
            "external_context_introduction_event_ref": (
                self.external_context_introduction_event_ref
            ),
            "external_context_introduction_event_fingerprint": (
                self.external_context_introduction_event_fingerprint
            ),
            "external_context_snapshot_ref": self.external_context_snapshot_ref,
            "external_context_snapshot_fingerprint": (self.external_context_snapshot_fingerprint),
            "external_context_event_high_watermark": (self.external_context_event_high_watermark),
        }


@dataclass(frozen=True, slots=True)
class CycleCandidate:
    cycle_id: str
    cycle_version: str
    project_id: str
    task_contract_id: str
    task_contract_version: str
    task_contract_fingerprint: str
    work_run_id: str
    terminal_state_version: int
    transition_request_id: str
    transition_decision_id: str
    transition_decision_fingerprint: str
    judgment_ref: str
    judgment_fingerprint: str
    evidence_attestation_ref: str
    evidence_root: str
    memory_declarations: tuple[MemoryDeclaration, ...]
    task_constraint_ref: str
    task_constraint_fingerprint: str
    task_constraint_snapshot_ref: str
    task_constraint_snapshot_fingerprint: str
    task_constraint_event_high_watermark: int

    def __post_init__(self) -> None:
        if self.terminal_state_version < 1:
            raise ValueError("terminal state version must be positive")
        if not self.memory_declarations:
            raise ValueError("Cycle must declare at least one bounded memory item")
        if any(
            not value
            for value in (
                self.task_constraint_ref,
                self.task_constraint_fingerprint,
                self.task_constraint_snapshot_ref,
                self.task_constraint_snapshot_fingerprint,
            )
        ):
            raise ValueError("Cycle requires the complete original TaskConstraint graph")
        require_safe_integer(
            self.task_constraint_event_high_watermark,
            label="task_constraint_event_high_watermark",
            minimum=1,
        )

    @property
    def fingerprint(self) -> str:
        return canonical_hash(
            {
                "cycle_id": self.cycle_id,
                "cycle_version": self.cycle_version,
                "evidence_attestation_ref": self.evidence_attestation_ref,
                "evidence_root": self.evidence_root,
                "judgment_fingerprint": self.judgment_fingerprint,
                "judgment_ref": self.judgment_ref,
                "memory_declarations": [item.payload() for item in self.memory_declarations],
                "project_id": self.project_id,
                "p1_8_task_binding_fingerprint": self.task_contract_fingerprint,
                "task_contract_id": self.task_contract_id,
                "task_contract_version": self.task_contract_version,
                "terminal_state_version": self.terminal_state_version,
                "transition_decision_fingerprint": self.transition_decision_fingerprint,
                "transition_decision_id": self.transition_decision_id,
                "transition_request_id": self.transition_request_id,
                "work_run_id": self.work_run_id,
                "task_constraint_ref": self.task_constraint_ref,
                "task_constraint_fingerprint": self.task_constraint_fingerprint,
                "task_constraint_snapshot_ref": self.task_constraint_snapshot_ref,
                "task_constraint_snapshot_fingerprint": (self.task_constraint_snapshot_fingerprint),
                "task_constraint_event_high_watermark": (self.task_constraint_event_high_watermark),
            }
        )

    @property
    def terminal_epoch_key(self) -> str:
        return canonical_hash(
            {
                "project_id": self.project_id,
                "resulting_state_version": self.terminal_state_version,
                "task_contract_id": self.task_contract_id,
                "task_contract_version": self.task_contract_version,
                "terminal_transition_decision_ref": self.transition_decision_id,
                "terminal_epoch_schema": "P1_8_TERMINAL_EPOCH_KEY_V1",
                "work_run_id": self.work_run_id,
            }
        )

    @property
    def terminal_epoch_payload_fingerprint(self) -> str:
        """Cycle/request IDs are transport identity, not terminal epoch content."""
        return canonical_hash(
            {
                "cycle_version": self.cycle_version,
                "evidence_attestation_ref": self.evidence_attestation_ref,
                "evidence_root": self.evidence_root,
                "judgment_fingerprint": self.judgment_fingerprint,
                "judgment_ref": self.judgment_ref,
                "memory_declarations": [item.payload() for item in self.memory_declarations],
                "p1_8_task_binding_fingerprint_claim": self.task_contract_fingerprint,
                "terminal_epoch_key": self.terminal_epoch_key,
                "transition_decision_fingerprint": self.transition_decision_fingerprint,
                "transition_request_id": self.transition_request_id,
                "task_constraint_ref": self.task_constraint_ref,
                "task_constraint_fingerprint": self.task_constraint_fingerprint,
                "task_constraint_snapshot_ref": self.task_constraint_snapshot_ref,
                "task_constraint_snapshot_fingerprint": (self.task_constraint_snapshot_fingerprint),
                "task_constraint_event_high_watermark": (self.task_constraint_event_high_watermark),
            }
        )


def p1_8_task_binding_fingerprint(
    *, project_id: str, task_contract_id: str, task_contract_version: str
) -> str:
    """Non-authoritative equality binding over fields verified from P1-4/P1-6/P1-7 owners."""
    return canonical_hash(
        {
            "binding_schema": "P1_8_VERIFIED_TASK_SCOPE_BINDING_V1",
            "project_id": project_id,
            "task_contract_id": task_contract_id,
            "task_contract_version": task_contract_version,
        }
    )


@dataclass(frozen=True, slots=True)
class CycleAdmissionRequest:
    request_id: str
    request_version: str
    candidate: CycleCandidate
    requester_ref: str
    requested_at: datetime

    def __post_init__(self) -> None:
        if self.requested_at.tzinfo is None:
            raise ValueError("Cycle request timestamp must be timezone-aware")

    @property
    def fingerprint(self) -> str:
        return canonical_hash(
            {
                "candidate_fingerprint": self.candidate.fingerprint,
                "request_id": self.request_id,
                "request_version": self.request_version,
                "requested_at": self.requested_at.astimezone(UTC).isoformat(),
                "requester_ref": self.requester_ref,
            }
        )


@dataclass(frozen=True, slots=True)
class CycleEvaluation:
    evaluation_id: str
    request_id: str
    request_fingerprint: str
    terminal_provenance_fingerprint: str
    policy_fingerprints: tuple[str, ...]
    memory_content_fingerprints: tuple[str, ...]
    outcome: str
    evaluated_at: datetime

    @property
    def fingerprint(self) -> str:
        return canonical_hash(
            {
                "evaluated_at": self.evaluated_at.astimezone(UTC).isoformat(),
                "evaluation_id": self.evaluation_id,
                "memory_content_fingerprints": list(self.memory_content_fingerprints),
                "outcome": self.outcome,
                "policy_fingerprints": list(self.policy_fingerprints),
                "request_fingerprint": self.request_fingerprint,
                "request_id": self.request_id,
                "terminal_provenance_fingerprint": self.terminal_provenance_fingerprint,
            }
        )


@dataclass(frozen=True, slots=True)
class CycleAdmissionDecision:
    decision_id: str
    evaluation_id: str
    evaluation_fingerprint: str
    outcome: str
    reason: str
    authority_id: str
    authority_version: str
    decided_at: datetime

    @property
    def fingerprint(self) -> str:
        return canonical_hash(
            {
                "authority_id": self.authority_id,
                "authority_version": self.authority_version,
                "decided_at": self.decided_at.astimezone(UTC).isoformat(),
                "decision_id": self.decision_id,
                "evaluation_fingerprint": self.evaluation_fingerprint,
                "evaluation_id": self.evaluation_id,
                "outcome": self.outcome,
                "reason": self.reason,
            }
        )


@dataclass(frozen=True, slots=True)
class AdmittedCycle:
    cycle_id: str
    cycle_version: str
    cycle_fingerprint: str
    request_id: str
    decision_id: str
    project_id: str
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    terminal_state_version: int
    transition_decision_id: str
    judgment_ref: str
    evidence_attestation_ref: str
    evidence_root: str
    task_constraint_ref: str
    task_constraint_fingerprint: str
    task_constraint_snapshot_ref: str
    task_constraint_snapshot_fingerprint: str
    task_constraint_event_high_watermark: int
    admission_sequence: int
    admitted_at: datetime

    @property
    def serialized_ref(self) -> str:
        return f"p1-8-cycle:{self.cycle_version}:{self.cycle_id}"
