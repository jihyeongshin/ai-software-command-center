"""Immutable orchestration views, never authority receipts."""

from dataclasses import dataclass
from typing import Literal

from aiscc.contracts.workflow import RuntimeMode
from aiscc.evidence.models import EvidenceCheckpointRef
from aiscc.judgment.models import JudgmentOwnerPolicy
from aiscc.next_action.models import ActionRef


@dataclass(frozen=True, slots=True, init=False)
class SelfDogfoodTaskSpec:
    project_id: str
    task_id: str
    task_contract_id: str
    task_contract_version: str
    task_contract_body_ref: str
    task_contract_body_sha256: str
    source_selection_id: str
    source_selection_version: str
    source_action_ref: ActionRef
    source_selection_fingerprint: str
    source_descriptor_fingerprint: str
    repository_id: str
    repository_root: str
    base_commit: str
    goal: str
    non_goals: tuple[str, ...]
    allowed_paths: tuple[str, ...]
    forbidden_paths: tuple[str, ...]
    evidence_requirement_set_ref: str
    evidence_requirement_set_fingerprint: str
    evidence_checkpoints: tuple[tuple[EvidenceCheckpointRef, str], ...]
    human_requirement_kind: Literal["REQUIRED", "NOT_REQUIRED"]
    judgment_owner_policy: JudgmentOwnerPolicy
    runtime_mode: RuntimeMode
    cycle_execution_mode: Literal["AISCC_SELF_DOGFOOD"]
    orchestrator_version: str
    orchestrator_commit: str

    def __init__(self) -> None:
        raise TypeError("use materialize_task_spec with a current durable receipt")
