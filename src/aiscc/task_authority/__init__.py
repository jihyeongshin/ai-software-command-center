"""Immutable external Task-authority values and read/verifier ports.

The live writer, repository implementation, and capability binding are deliberately not
re-exported from this package boundary.
"""

from aiscc.task_authority.models import (
    AuthorityEventKind,
    CurrentProjectionDisposition,
    ExternalTaskAuthorityError,
    ExternalTaskAuthorityErrorCode,
    NextActionContextAuthorityEventV1,
    NextActionContextFoldResult,
    NextActionContextRefV1,
    NextActionPriorityClass,
    TaskConstraintAuthorityEventV1,
    TaskConstraintFoldResult,
    TaskConstraintOwnerSnapshotV1,
    TaskConstraintRefV1,
    TaskConstraintScopeKind,
    TaskConstraintScopeV1,
)
from aiscc.task_authority.ports import (
    ExternalTaskAuthorityReadPort,
    ExternalTaskAuthorityVerifierPort,
)

__all__ = [
    "AuthorityEventKind",
    "CurrentProjectionDisposition",
    "ExternalTaskAuthorityError",
    "ExternalTaskAuthorityErrorCode",
    "ExternalTaskAuthorityReadPort",
    "ExternalTaskAuthorityVerifierPort",
    "NextActionContextAuthorityEventV1",
    "NextActionContextFoldResult",
    "NextActionContextRefV1",
    "NextActionPriorityClass",
    "TaskConstraintAuthorityEventV1",
    "TaskConstraintFoldResult",
    "TaskConstraintOwnerSnapshotV1",
    "TaskConstraintRefV1",
    "TaskConstraintScopeKind",
    "TaskConstraintScopeV1",
]
