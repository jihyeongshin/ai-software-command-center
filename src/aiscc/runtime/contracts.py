from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum


class RuntimeOutcomeStatus(StrEnum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"
    QUARANTINED = "QUARANTINED"


@dataclass(frozen=True, slots=True)
class RuntimeOutcome:
    status: RuntimeOutcomeStatus
    exit_code: int | None
    attempts: int
    stdout: str
    stderr: str
    cleanup_complete: bool
    executed: bool
    security_reason: str
    security_provenance: Mapping[str, str]


@dataclass(frozen=True, slots=True)
class ResourceRecord:
    run_id: str
    resource_type: str
    resource_id: str
