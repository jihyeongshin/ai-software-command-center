"""Server-owned, per-attempt Public Live repository/scenario authority."""

from dataclasses import dataclass

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.providers.models import ProviderProfile
from aiscc.public_live.luna_profile import hosted_luna_profile


@dataclass(frozen=True)
class _Context:
    current: WorkflowSnapshot
    attempt: str
    principal: str
    scope: ResourceScope
    fingerprint: str


class PublicLiveContextResourceAuthority:
    def __init__(
        self, *, profile: ProviderProfile, current: WorkflowSnapshot, attempt: str, principal: str
    ) -> None:
        if (
            profile != hosted_luna_profile()
            or current.state is not WorkflowState.RUNNING
            or current.state_version <= 0
            or not current.run_id
            or not attempt
            or not principal
        ):
            raise ValueError("PUBLIC_CONTEXT_BINDING_DENIED")
        self._profile = profile
        self._current = current
        self._attempt = attempt
        self._principal = principal
        self._issued: list[_Context] = []

    def issue(
        self,
        *,
        current: WorkflowSnapshot,
        mode: RuntimeMode,
        principal: str,
        scenario_id: str,
        scope: ResourceScope,
        action: SecurityActionClass,
        fingerprint: str,
        execution_attempt_id: str,
        provider_profile_id: str,
        provider_profile_version: str,
    ) -> object:
        identities = {
            ResourceDomain.REPOSITORY: self._profile.public_repository_resource_identity,
            ResourceDomain.SCENARIO: self._profile.public_scenario_resource_identity,
        }
        if not (
            current == self._current
            and mode is RuntimeMode.PUBLIC_BOUNDED_LIVE
            and action is SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT
            and principal == self._principal
            and execution_attempt_id == self._attempt
            and provider_profile_id == self._profile.profile_id
            and provider_profile_version == self._profile.version
            and scenario_id == self._profile.public_scenario_identity
            and scope.domain in identities
            and scope == ResourceScope(scope.domain, identities[scope.domain])
            and len(fingerprint) == 64
            and all(c in "0123456789abcdef" for c in fingerprint)
        ):
            raise ValueError("PUBLIC_CONTEXT_BINDING_DENIED")
        context = _Context(current, execution_attempt_id, principal, scope, fingerprint)
        self._issued.append(context)
        return context

    def allows(
        self,
        context: object,
        *,
        mode: RuntimeMode,
        scenario_id: str | None,
        action: SecurityActionClass,
        scope: ResourceScope,
        principal: str,
        run_id: str,
        operation_fingerprint: str | None,
    ) -> bool:
        return bool(
            isinstance(context, _Context)
            and any(context is item for item in self._issued)
            and mode is RuntimeMode.PUBLIC_BOUNDED_LIVE
            and action is SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT
            and scenario_id == self._profile.public_scenario_identity
            and principal == context.principal
            and run_id == context.current.run_id
            and scope == context.scope
            and operation_fingerprint == context.fingerprint
        )

    def current_matches(self, context: object, current: WorkflowSnapshot) -> bool:
        return (
            isinstance(context, _Context)
            and any(context is item for item in self._issued)
            and context.current == current
        )
