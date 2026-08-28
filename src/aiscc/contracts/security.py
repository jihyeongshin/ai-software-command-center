from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from types import MappingProxyType

from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot


class SecurityAdmissionDecision(StrEnum):
    ALLOW = "ALLOW"
    DENY = "DENY"


class AuthorityStatus(StrEnum):
    GRANTED = "GRANTED"
    DENIED = "DENIED"
    UNRESOLVED = "UNRESOLVED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class SecurityActionClass(StrEnum):
    START_EXECUTION_CONTROL = "START_EXECUTION_CONTROL"
    RUN_EXECUTION_SIDE_EFFECT = "RUN_EXECUTION_SIDE_EFFECT"
    RUN_REVIEW_READ_ONLY = "RUN_REVIEW_READ_ONLY"
    PUBLIC_CANCEL_CONTROL = "PUBLIC_CANCEL_CONTROL"
    ADMINISTRATIVE_TERMINATE_CONTROL = "ADMINISTRATIVE_TERMINATE_CONTROL"
    REWORK_START_CONTROL = "REWORK_START_CONTROL"
    BLOCKER_RECOVERY_CHECK = "BLOCKER_RECOVERY_CHECK"
    SAFETY_CLEANUP_REVOKE_QUARANTINE = "SAFETY_CLEANUP_REVOKE_QUARANTINE"
    RECOVERY_RECONCILIATION = "RECOVERY_RECONCILIATION"
    SYSTEM_DURABLE_PROVENANCE = "SYSTEM_DURABLE_PROVENANCE"
    REPLAY_READ_ONLY = "REPLAY_READ_ONLY"


class ResourceDomain(StrEnum):
    FILESYSTEM = "FILESYSTEM"
    PROCESS = "PROCESS"
    TOOL = "TOOL"
    NETWORK = "NETWORK"
    SECRET = "SECRET"
    REPOSITORY = "REPOSITORY"
    PROVIDER = "PROVIDER"
    SCENARIO = "SCENARIO"


@dataclass(frozen=True, slots=True)
class ResourceScope:
    domain: ResourceDomain
    resource_id: str
    image: str | None = None
    argv: tuple[str, ...] = ()
    workspace_path: str | None = None
    network_name: str | None = None
    network_aliases: tuple[str, ...] = ()
    target_name: str | None = None
    detach: bool = False

    def __post_init__(self) -> None:
        if not self.resource_id:
            raise ValueError("resource scope requires an exact resource_id")


@dataclass(frozen=True, slots=True)
class ResourceGrant:
    grant_id: str
    version: str
    mode: RuntimeMode
    profile_version: str
    scenario_id: str | None
    principal: str
    run_id: str
    action: SecurityActionClass
    scope: ResourceScope
    expires_at: datetime
    revoked: bool
    _issuer_token: object = field(repr=False, compare=False)
    selector_attestation_ref: str | None = None
    selector_request: object | None = field(default=None, repr=False, compare=True)
    operation_fingerprint: str | None = None


@dataclass(frozen=True, slots=True)
class PermissionRequest:
    principal: str
    run_id: str
    mode: RuntimeMode
    observed: WorkflowSnapshot
    authoritative: WorkflowSnapshot
    action: object
    resource_scope: ResourceScope
    resource_grant: ResourceGrant | None
    profile_version: str
    scenario_id: str | None
    requester_authority: AuthorityStatus | None
    task_scope_authority: AuthorityStatus | None
    limit_authority: AuthorityStatus | None
    budget_authority: AuthorityStatus | None
    idempotency_authority: AuthorityStatus | None
    target_control_authority: AuthorityStatus | None


@dataclass(frozen=True, slots=True)
class SecurityDecision:
    decision: SecurityAdmissionDecision
    reason: str
    guards: tuple[tuple[str, bool], ...]
    provenance: Mapping[str, str]
    admission_id: str | None = None

    @classmethod
    def create(
        cls,
        decision: SecurityAdmissionDecision,
        reason: str,
        guards: tuple[tuple[str, bool], ...],
        provenance: dict[str, str],
        admission_id: str | None = None,
    ) -> SecurityDecision:
        return cls(
            decision,
            reason,
            guards,
            MappingProxyType(dict(provenance)),
            admission_id,
        )
