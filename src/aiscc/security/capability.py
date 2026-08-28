from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from types import MappingProxyType

from aiscc.contracts.security import ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot


@dataclass(frozen=True, slots=True)
class Capability:
    capability_id: str
    admission_id: str
    principal: str
    run_id: str
    snapshot: WorkflowSnapshot
    mode: RuntimeMode
    profile_version: str
    action: SecurityActionClass
    scope: ResourceScope
    expires_at: datetime
    max_uses: int
    _issuer_token: object = field(repr=False, compare=False)

    def validate(
        self,
        *,
        issuer_token: object,
        registered_capability: Capability | None,
        principal: str,
        current_mode: RuntimeMode,
        current: WorkflowSnapshot,
        profile_version: str,
        action: SecurityActionClass,
        scope: ResourceScope,
        current_use_count: int,
        revoked: bool,
        now: datetime | None = None,
    ) -> tuple[bool, str]:
        current_time = now or datetime.now(UTC)
        checks = (
            (self._issuer_token is issuer_token, "CAPABILITY_ISSUER_MISMATCH"),
            (registered_capability is self, "CAPABILITY_NOT_REGISTERED"),
            (not revoked, "CAPABILITY_REVOKED"),
            (current_time < self.expires_at, "CAPABILITY_EXPIRED"),
            (current_use_count < self.max_uses, "CAPABILITY_USE_LIMIT"),
            (principal == self.principal, "CAPABILITY_PRINCIPAL_MISMATCH"),
            (current_mode is self.mode, "CAPABILITY_MODE_MISMATCH"),
            (current.run_id == self.run_id == self.snapshot.run_id, "CAPABILITY_RUN_MISMATCH"),
            (current == self.snapshot, "CAPABILITY_STALE_STATE_VERSION"),
            (profile_version == self.profile_version, "CAPABILITY_PROFILE_MISMATCH"),
            (action is self.action, "CAPABILITY_ACTION_MISMATCH"),
            (scope == self.scope, "CAPABILITY_RESOURCE_SCOPE_MISMATCH"),
        )
        for passed, reason in checks:
            if not passed:
                return False, reason
        return True, "CAPABILITY_VALID"


@dataclass(frozen=True, slots=True)
class CapabilityUse:
    allowed: bool
    reason: str
    consumed_use_count: int
    provenance: Mapping[str, str]

    @classmethod
    def create(
        cls,
        *,
        allowed: bool,
        reason: str,
        consumed_use_count: int,
        provenance: dict[str, str],
    ) -> CapabilityUse:
        return cls(
            allowed,
            reason,
            consumed_use_count,
            MappingProxyType(dict(provenance)),
        )
