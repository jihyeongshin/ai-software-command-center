"""B1 server-composition DTOs; no security issuer or public input boundary.

An authority ref set must be registered by trusted composition, then matched by
object identity and live binding. Its presence is not runtime capability proof.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from aiscc.contracts.workflow import RuntimeMode, WorkflowState


@dataclass(frozen=True, slots=True)
class StockroomRunBinding:
    mode: RuntimeMode
    scenario_id: str
    scenario_version: str
    resource_ref: str
    run_id: str
    attempt_id: str
    state: WorkflowState
    state_version: int
    profile_version: str
    config_sha256: str


@dataclass(frozen=True, slots=True)
class MaterializationAuthority:
    binding: StockroomRunBinding
    principal_ref: str
    security_admission_ref: str
    repository_grant_ref: str
    filesystem_grant_ref: str
    operation_fingerprint: str
    repository_root: Path
    runtime_root: Path


class WorkspaceOwnership(StrEnum):
    OWNED = "OWNED"
    CLEANED = "CLEANED"
    QUARANTINED = "QUARANTINED"


@dataclass(frozen=True, slots=True)
class StockroomWorkspaceLease:
    lease_id: str
    run_id: str
    attempt_id: str
    runtime_root: Path
    destination: Path
    ownership: WorkspaceOwnership = WorkspaceOwnership.OWNED


@dataclass(frozen=True, slots=True)
class WorkspaceCleanupDisposition:
    lease_id: str
    destination: Path
    ownership: WorkspaceOwnership
    reason: str


@dataclass(frozen=True, slots=True)
class MaterializedFile:
    path: str
    mode: str
    bytes: int
    sha256: str


@dataclass(frozen=True, slots=True)
class MaterializedStockroom:
    resource_ref: str
    source_commit: str
    subroot: str
    git_subtree: str
    files: tuple[MaterializedFile, ...]
    aggregate_sha256: str
    workspace_lease: StockroomWorkspaceLease
    run_id: str
    attempt_id: str
    resolved_source_root: Path


class StockroomFailure(RuntimeError):
    """Stable classification, without raw Git stderr or imported file content."""

    def __init__(self, reason: str, cleanup: WorkspaceCleanupDisposition | None = None) -> None:
        super().__init__(reason)
        self.reason = reason
        self.cleanup = cleanup
