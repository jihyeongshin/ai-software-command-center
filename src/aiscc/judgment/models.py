from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum

from aiscc.contracts.workflow import WorkflowState
from aiscc.workflow.models import GuardId


class JudgmentKind(StrEnum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    HOLD_REWORK_REQUIRED = "HOLD_REWORK_REQUIRED"


class JudgmentOwnerPolicy(StrEnum):
    SYSTEM_DETERMINISTIC = "SYSTEM_DETERMINISTIC"
    HUMAN = "HUMAN"
    COMMAND_CENTER = "COMMAND_CENTER"


class JudgmentEvidenceBasisKind(StrEnum):
    SATISFIED_ATTESTATION = "SATISFIED_ATTESTATION"
    UNSATISFIED_SET_EVALUATION = "UNSATISFIED_SET_EVALUATION"


class JudgmentAuthorityError(RuntimeError):
    pass


class JudgmentIdentityConflictError(JudgmentAuthorityError):
    pass


@dataclass(frozen=True, slots=True)
class JudgmentPolicy:
    policy_id: str
    policy_version: str
    fingerprint: str
    task_contract_id: str
    task_contract_version: str
    source_state: WorkflowState
    target_state: WorkflowState
    target_use_fingerprint: str
    owner_policy: JudgmentOwnerPolicy
    requires_human_result: bool
    requires_post_human_evidence: bool
    deterministic_kind: JudgmentKind | None
    policy_authority_id: str
    policy_authority_version: str
    policy_authority_revision: int
    issued_at: datetime
    _issuer_token: object = field(default=None, repr=False, compare=False)
    evidence_basis_kind: JudgmentEvidenceBasisKind | None = None
    evidence_checkpoint_ref: str | None = None
    evidence_requirement_set_ref: str | None = None

    def __post_init__(self) -> None:
        if self.evidence_basis_kind is None:
            if self.evidence_checkpoint_ref is not None or (
                self.evidence_requirement_set_ref is not None
            ):
                raise ValueError("legacy Judgment policy cannot carry partial evidence basis")
            return
        if not isinstance(self.evidence_basis_kind, JudgmentEvidenceBasisKind):
            raise ValueError("unknown Judgment evidence basis kind")
        if not self.evidence_checkpoint_ref or not self.evidence_requirement_set_ref:
            raise ValueError("typed Judgment policy requires checkpoint and requirement set")
        if (
            self.evidence_basis_kind is JudgmentEvidenceBasisKind.SATISFIED_ATTESTATION
            and not self.requires_post_human_evidence
        ):
            raise ValueError("positive Judgment policy requires admitted evidence")
        if self.evidence_basis_kind is JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION and (
            self.owner_policy is not JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC
            or self.deterministic_kind is not JudgmentKind.HOLD_REWORK_REQUIRED
            or self.target_state is not WorkflowState.REWORK_REQUIRED
            or self.requires_post_human_evidence
        ):
            raise ValueError("negative Judgment basis requires deterministic rework policy")

    @property
    def serialized_ref(self) -> str:
        return f"p1-7-judgment-policy:{self.policy_version}:{self.policy_id}"


@dataclass(frozen=True, slots=True)
class CommandCenterPrincipal:
    principal_id: str
    authority_id: str
    authority_version: str
    authenticated_at: datetime
    expires_at: datetime
    _issuer_token: object = field(repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class CommandCenterActionAuthority:
    action_id: str
    action_version: str
    fingerprint: str
    principal_id: str
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    source_state: WorkflowState
    state_version: int
    target_state: WorkflowState
    target_use_fingerprint: str
    policy_ref: str
    policy_fingerprint: str
    policy_authority_revision: int
    judgment_kind: JudgmentKind
    issued_at: datetime
    expires_at: datetime
    authority_id: str
    authority_version: str
    _issuer_token: object = field(default=None, repr=False, compare=False)

    @property
    def serialized_ref(self) -> str:
        return f"p1-7-command-center-action:{self.action_version}:{self.action_id}"


@dataclass(frozen=True, slots=True)
class Judgment:
    judgment_id: str
    judgment_version: str
    fingerprint: str
    authority_id: str
    authority_version: str
    authority_revision: int
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    source_state: WorkflowState
    state_version: int
    target_state: WorkflowState
    target_use_fingerprint: str
    owner_policy: JudgmentOwnerPolicy
    policy_id: str
    policy_version: str
    policy_fingerprint: str
    policy_authority_id: str
    policy_authority_version: str
    policy_authority_revision: int
    command_center_action_ref: str | None
    human_gate_ref: str | None
    human_result_ref: str | None
    human_result_authority_revision: int | None
    evidence_attestation_ref: str | None
    evidence_authority_revision: int | None
    evidence_root: str | None
    judgment_kind: JudgmentKind
    reason_code: str
    reason_vocabulary_version: str
    evaluation_ref: str
    issued_at: datetime
    supersedes_judgment_ref: str | None = None
    evidence_basis_kind: JudgmentEvidenceBasisKind | None = None
    evidence_evaluation_ref: str | None = None
    evidence_evaluation_authority_revision: int | None = None
    evidence_checkpoint_ref: str | None = None
    evidence_requirement_set_ref: str | None = None

    def __post_init__(self) -> None:
        if self.evidence_basis_kind is None:
            if any(
                value is not None
                for value in (
                    self.evidence_evaluation_ref,
                    self.evidence_evaluation_authority_revision,
                    self.evidence_checkpoint_ref,
                    self.evidence_requirement_set_ref,
                )
            ):
                raise ValueError("legacy Judgment cannot carry typed evidence basis metadata")
            return
        if not isinstance(self.evidence_basis_kind, JudgmentEvidenceBasisKind):
            raise ValueError("unknown Judgment evidence basis kind")
        if not self.evidence_checkpoint_ref or not self.evidence_requirement_set_ref:
            raise ValueError(
                "typed Judgment evidence basis requires checkpoint and requirement set"
            )
        if self.evidence_basis_kind is JudgmentEvidenceBasisKind.SATISFIED_ATTESTATION:
            if (
                self.evidence_attestation_ref is None
                or self.evidence_authority_revision is None
                or self.evidence_root is None
                or any(
                    value is not None
                    for value in (
                        self.evidence_evaluation_ref,
                        self.evidence_evaluation_authority_revision,
                    )
                )
            ):
                raise ValueError("positive Judgment basis requires only an attestation ref")
        elif (
            self.evidence_basis_kind
            is JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION
            and (
                self.evidence_evaluation_ref is None
                or self.evidence_evaluation_authority_revision is None
                or self.evidence_attestation_ref is not None
                or self.evidence_authority_revision is not None
                or self.evidence_root is not None
                or self.target_state is not WorkflowState.REWORK_REQUIRED
                or self.judgment_kind is not JudgmentKind.HOLD_REWORK_REQUIRED
            )
        ):
            raise ValueError("negative Judgment basis requires only an evaluation ref")

    @property
    def serialized_ref(self) -> str:
        return f"p1-7-judgment:{self.judgment_version}:{self.judgment_id}"


@dataclass(frozen=True, slots=True)
class JudgmentGuardAttestation:
    attestation_id: str
    attestation_version: str
    fingerprint: str
    guard_id: GuardId
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    source_state: WorkflowState
    state_version: int
    target_state: WorkflowState
    target_use_fingerprint: str
    judgment_ref: str
    judgment_authority_revision: int
    human_gate_ref: str | None
    human_result_ref: str | None
    evidence_attestation_ref: str | None
    evidence_authority_revision: int | None
    policy_id: str
    policy_version: str
    policy_fingerprint: str
    policy_authority_id: str
    policy_authority_version: str
    policy_authority_revision: int
    authority_id: str
    authority_version: str
    issued_at: datetime
    expires_at: datetime | None

    @property
    def serialized_ref(self) -> str:
        return f"p1-7-judgment-guard:{self.attestation_version}:{self.attestation_id}"
