from __future__ import annotations

from datetime import UTC, datetime, timedelta

from aiscc.contracts.security import (
    AuthorityStatus,
    PermissionRequest,
    ResourceDomain,
    ResourceGrant,
    ResourceScope,
    SecurityActionClass,
    SecurityAdmissionDecision,
    SecurityDecision,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot
from aiscc.security.action_state import is_action_state_eligible
from aiscc.security.capability import Capability, CapabilityUse
from aiscc.security.models import PermissionProfile

_MUTABLE_TARGET_ACTIONS = frozenset(
    {
        SecurityActionClass.PUBLIC_CANCEL_CONTROL,
        SecurityActionClass.ADMINISTRATIVE_TERMINATE_CONTROL,
        SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
    }
)
_P1_5_OWNED_DOMAINS = frozenset({ResourceDomain.PROVIDER, ResourceDomain.TOOL})
_PUBLIC_LIVE_PROCESS_SCOPE = ResourceScope(
    domain=ResourceDomain.PROCESS,
    resource_id="process:p1-3-synthetic-probe",
    argv=("python", "-c", "print('AISCC_PUBLIC_LIVE_SYNTHETIC_OK')"),
)


def default_profiles() -> dict[str, PermissionProfile]:
    all_actions = frozenset(SecurityActionClass)
    all_resources = frozenset(ResourceDomain)
    replay_actions = frozenset(
        {SecurityActionClass.RUN_REVIEW_READ_ONLY, SecurityActionClass.REPLAY_READ_ONLY}
    )
    live_actions = frozenset(
        {
            SecurityActionClass.START_EXECUTION_CONTROL,
            SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            SecurityActionClass.RUN_REVIEW_READ_ONLY,
            SecurityActionClass.PUBLIC_CANCEL_CONTROL,
            SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
            SecurityActionClass.RECOVERY_RECONCILIATION,
            SecurityActionClass.SYSTEM_DURABLE_PROVENANCE,
            SecurityActionClass.REPLAY_READ_ONLY,
        }
    )
    return {
        RuntimeMode.OWNER_SELF_DOGFOOD.value: PermissionProfile(
            RuntimeMode.OWNER_SELF_DOGFOOD, "p1-3-v2", all_actions, all_resources
        ),
        RuntimeMode.PUBLIC_RECORDED_REPLAY.value: PermissionProfile(
            RuntimeMode.PUBLIC_RECORDED_REPLAY,
            "p1-3-v2",
            replay_actions,
            frozenset({ResourceDomain.FILESYSTEM, ResourceDomain.SCENARIO}),
        ),
        RuntimeMode.PUBLIC_BOUNDED_LIVE.value: PermissionProfile(
            RuntimeMode.PUBLIC_BOUNDED_LIVE,
            "p1-3-v2",
            live_actions,
            frozenset(
                {
                    ResourceDomain.FILESYSTEM,
                    ResourceDomain.PROCESS,
                    ResourceDomain.NETWORK,
                    ResourceDomain.REPOSITORY,
                    ResourceDomain.SCENARIO,
                }
            ),
            frozenset({"p1-3-fixed-synthetic"}),
        ),
    }


class SecurityPolicy:
    def __init__(self, profiles: dict[str, PermissionProfile]) -> None:
        self._profiles = dict(profiles)
        self._resource_issuer_token = object()
        self._capability_issuer_token = object()
        self._grant_sequence = 0
        self._admission_sequence = 0
        self._capability_sequence = 0
        self._admissions: dict[str, tuple[SecurityDecision, PermissionRequest]] = {}
        self._capabilities: dict[str, Capability] = {}
        self._capability_uses: dict[str, int] = {}
        self._revoked_capabilities: set[str] = set()

    def issue_resource_grant(
        self,
        *,
        mode: RuntimeMode,
        profile_version: str,
        scenario_id: str | None,
        principal: str,
        run_id: str,
        action: SecurityActionClass,
        scope: ResourceScope,
        ttl_seconds: int = 30,
        now: datetime | None = None,
    ) -> ResourceGrant | None:
        current_time = now or datetime.now(UTC)
        if ttl_seconds <= 0 or ttl_seconds > 60:
            return None
        profile = self._profiles.get(mode.value)
        if (
            profile is None
            or profile.version != profile_version
            or action not in profile.actions
            or scope.domain not in profile.resources
            or not self._scope_is_policy_owned(mode, scenario_id, action, scope)
        ):
            return None
        self._grant_sequence += 1
        return ResourceGrant(
            grant_id=f"resource-grant-{self._grant_sequence}",
            version="resource-grant-v1",
            mode=mode,
            profile_version=profile_version,
            scenario_id=scenario_id,
            principal=principal,
            run_id=run_id,
            action=action,
            scope=scope,
            expires_at=current_time + timedelta(seconds=ttl_seconds),
            revoked=False,
            _issuer_token=self._resource_issuer_token,
        )

    def evaluate(self, request: PermissionRequest) -> SecurityDecision:
        provenance = {
            "principal": request.principal,
            "run_id": request.run_id,
            "mode": request.mode.value,
            "observed_state": request.observed.state.value,
            "observed_version": str(request.observed.state_version),
            "current_state": request.authoritative.state.value,
            "current_version": str(request.authoritative.state_version),
            "resource_domain": request.resource_scope.domain.value,
            "resource_id": request.resource_scope.resource_id,
            "resource_grant_id": (
                request.resource_grant.grant_id if request.resource_grant is not None else "none"
            ),
        }
        if not isinstance(request.action, SecurityActionClass):
            return SecurityDecision.create(
                SecurityAdmissionDecision.DENY,
                "UNKNOWN_ACTION_CLASS",
                (("SG_KNOWN_ACTION_CLASS", False),),
                provenance,
            )
        action = request.action
        provenance["action"] = action.value
        profile = self._profiles.get(request.mode.value)
        profile_valid = profile is not None and profile.version == request.profile_version
        fresh = (
            request.run_id == request.observed.run_id == request.authoritative.run_id
            and request.observed == request.authoritative
        )
        eligible = is_action_state_eligible(request.authoritative.state, action)
        profile_action = profile_valid and profile is not None and action in profile.actions
        resource_valid = self._resource_grant_is_valid(request, action)
        target_control = (
            request.target_control_authority is AuthorityStatus.GRANTED
            if action in _MUTABLE_TARGET_ACTIONS
            else request.target_control_authority is AuthorityStatus.NOT_APPLICABLE
        )
        guards = (
            ("SG_FRESH_STATE_VERSION", fresh),
            ("SG_ACTION_STATE_ELIGIBLE", eligible),
            (
                "SG_REQUESTER_AUTHORIZED",
                request.requester_authority is AuthorityStatus.GRANTED,
            ),
            (
                "SG_TASK_PROFILE_SCOPE",
                request.task_scope_authority is AuthorityStatus.GRANTED and profile_action,
            ),
            ("SG_EXACT_RESOURCE_GRANT", resource_valid),
            ("SG_LIMIT", request.limit_authority is AuthorityStatus.GRANTED),
            ("SG_BUDGET", request.budget_authority is AuthorityStatus.GRANTED),
            ("SG_IDEMPOTENCY", request.idempotency_authority is AuthorityStatus.GRANTED),
            ("SG_TARGET_CONTROL_AUTHORIZATION_WHEN_MUTABLE_CONTROL", target_control),
        )
        for guard, passed in guards:
            if not passed:
                reason = (
                    "STALE_REQUEST"
                    if guard == "SG_FRESH_STATE_VERSION"
                    else "ACTION_STATE_NOT_ADMISSIBLE"
                    if guard == "SG_ACTION_STATE_ELIGIBLE"
                    else guard.removeprefix("SG_") + "_DENIED"
                )
                return SecurityDecision.create(
                    SecurityAdmissionDecision.DENY, reason, guards, provenance
                )
        self._admission_sequence += 1
        admission_id = f"security-admission-{self._admission_sequence}"
        provenance["admission_id"] = admission_id
        decision = SecurityDecision.create(
            SecurityAdmissionDecision.ALLOW,
            "ALL_SECURITY_GUARDS_PASSED",
            guards,
            provenance,
            admission_id,
        )
        self._admissions[admission_id] = (decision, request)
        return decision

    def issue_capability(
        self,
        decision: SecurityDecision,
        request: PermissionRequest,
        *,
        ttl_seconds: int = 15,
        max_uses: int = 1,
        now: datetime | None = None,
    ) -> Capability | None:
        current_time = now or datetime.now(UTC)
        if (
            decision.decision is not SecurityAdmissionDecision.ALLOW
            or decision.admission_id is None
            or ttl_seconds <= 0
            or ttl_seconds > 30
            or max_uses <= 0
            or max_uses > 16
            or not isinstance(request.action, SecurityActionClass)
            or not self._resource_grant_is_valid(request, request.action, current_time)
        ):
            return None
        admitted = self._admissions.get(decision.admission_id)
        if admitted is None or admitted[0] is not decision or admitted[1] != request:
            return None
        self._capability_sequence += 1
        capability = Capability(
            capability_id=f"capability-{self._capability_sequence}",
            admission_id=decision.admission_id,
            principal=request.principal,
            run_id=request.run_id,
            snapshot=request.authoritative,
            mode=request.mode,
            profile_version=request.profile_version,
            action=request.action,
            scope=request.resource_scope,
            expires_at=current_time + timedelta(seconds=ttl_seconds),
            max_uses=max_uses,
            _issuer_token=self._capability_issuer_token,
        )
        self._capabilities[capability.capability_id] = capability
        self._capability_uses[capability.capability_id] = 0
        return capability

    def consume_capability(
        self,
        capability: Capability | None,
        *,
        principal: str,
        current_mode: RuntimeMode,
        current: WorkflowSnapshot,
        profile_version: str,
        action: SecurityActionClass,
        scope: ResourceScope,
        now: datetime | None = None,
    ) -> CapabilityUse:
        capability_id = capability.capability_id if capability is not None else "none"
        current_use_count = self._capability_uses.get(capability_id, 0)
        provenance = {
            "capability_id": capability_id,
            "principal": principal,
            "current_mode": current_mode.value,
            "run_id": current.run_id,
            "state": current.state.value,
            "state_version": str(current.state_version),
            "profile_version": profile_version,
            "action": action.value,
            "resource_domain": scope.domain.value,
            "resource_id": scope.resource_id,
            "consumed_use_count": str(current_use_count),
        }
        if capability is None:
            return CapabilityUse.create(
                allowed=False,
                reason="CAPABILITY_REQUIRED",
                consumed_use_count=0,
                provenance=provenance,
            )
        valid, reason = capability.validate(
            issuer_token=self._capability_issuer_token,
            registered_capability=self._capabilities.get(capability.capability_id),
            principal=principal,
            current_mode=current_mode,
            current=current,
            profile_version=profile_version,
            action=action,
            scope=scope,
            current_use_count=current_use_count,
            revoked=capability.capability_id in self._revoked_capabilities,
            now=now,
        )
        if valid and not is_action_state_eligible(current.state, action):
            valid, reason = False, "ACTION_STATE_NOT_ADMISSIBLE"
        if not valid:
            provenance["reason"] = reason
            return CapabilityUse.create(
                allowed=False,
                reason=reason,
                consumed_use_count=current_use_count,
                provenance=provenance,
            )
        consumed = current_use_count + 1
        self._capability_uses[capability.capability_id] = consumed
        provenance["reason"] = "CAPABILITY_CONSUMED"
        provenance["consumed_use_count"] = str(consumed)
        return CapabilityUse.create(
            allowed=True,
            reason="CAPABILITY_CONSUMED",
            consumed_use_count=consumed,
            provenance=provenance,
        )

    def revoke_capability(self, capability: Capability) -> bool:
        if self._capabilities.get(capability.capability_id) is not capability:
            return False
        self._revoked_capabilities.add(capability.capability_id)
        return True

    def _resource_grant_is_valid(
        self,
        request: PermissionRequest,
        action: SecurityActionClass,
        now: datetime | None = None,
    ) -> bool:
        current_time = now or datetime.now(UTC)
        grant = request.resource_grant
        return bool(
            grant is not None
            and grant._issuer_token is self._resource_issuer_token
            and grant.version == "resource-grant-v1"
            and not grant.revoked
            and current_time < grant.expires_at
            and grant.mode is request.mode
            and grant.profile_version == request.profile_version
            and grant.scenario_id == request.scenario_id
            and grant.principal == request.principal
            and grant.run_id == request.run_id
            and grant.action is action
            and grant.scope == request.resource_scope
        )

    @staticmethod
    def _scope_is_policy_owned(
        mode: RuntimeMode,
        scenario_id: str | None,
        action: SecurityActionClass,
        scope: ResourceScope,
    ) -> bool:
        if scope.domain in _P1_5_OWNED_DOMAINS or scope.domain is ResourceDomain.SECRET:
            return False
        if action is SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE:
            return (
                scope.domain in {ResourceDomain.PROCESS, ResourceDomain.NETWORK}
                and scope.resource_id.startswith(("container:", "network:"))
                and scope.image is None
                and not scope.argv
                and scope.workspace_path is None
            )
        if action is SecurityActionClass.RUN_REVIEW_READ_ONLY:
            return (
                mode is RuntimeMode.OWNER_SELF_DOGFOOD
                and scope.domain in {ResourceDomain.PROCESS, ResourceDomain.NETWORK}
                and scope.resource_id.startswith(("container:", "network:"))
                and scope.target_name is not None
                and scope.resource_id.endswith(scope.target_name)
                and scope.image is None
                and not scope.argv
                and scope.workspace_path is None
                and not scope.network_aliases
                and not scope.detach
            )
        if mode is RuntimeMode.OWNER_SELF_DOGFOOD:
            if scope.domain is ResourceDomain.PROCESS:
                return bool(scope.argv)
            if scope.domain is ResourceDomain.NETWORK:
                return scope.network_name is not None
            return True
        if mode is RuntimeMode.PUBLIC_RECORDED_REPLAY:
            return (
                action
                in {
                    SecurityActionClass.RUN_REVIEW_READ_ONLY,
                    SecurityActionClass.REPLAY_READ_ONLY,
                }
                and scope.domain in {ResourceDomain.FILESYSTEM, ResourceDomain.SCENARIO}
                and scope.resource_id in {"recorded:artifact-1", "scenario:p1-3-fixed-synthetic"}
                and scope.image is None
                and not scope.argv
                and scope.workspace_path is None
                and scope.network_name is None
            )
        if scenario_id != "p1-3-fixed-synthetic":
            return False
        if scope.domain is ResourceDomain.PROCESS:
            return scope == _PUBLIC_LIVE_PROCESS_SCOPE
        if scope.domain is ResourceDomain.FILESYSTEM:
            return scope == ResourceScope(
                ResourceDomain.FILESYSTEM,
                "workspace:p1-3-synthetic",
                workspace_path="synthetic://p1-3-workspace",
            )
        if scope.domain is ResourceDomain.NETWORK:
            return scope == ResourceScope(
                ResourceDomain.NETWORK,
                "network:p1-3-internal-fixture",
                network_name="aiscc-p1-3-internal",
            )
        if scope.domain is ResourceDomain.REPOSITORY:
            return scope == ResourceScope(ResourceDomain.REPOSITORY, "repository:p1-3-synthetic")
        if scope.domain is ResourceDomain.SCENARIO:
            return scope == ResourceScope(ResourceDomain.SCENARIO, "scenario:p1-3-fixed-synthetic")
        return False
