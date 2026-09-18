"""Explicit Public Live P1-5 composition; default permission profiles stay closed.

This scope authority is constructed from a committed semantic request and the
existing server-owned ProviderProfile. It does not issue credentials or replace
the independent provider/secret selectors, receipts, or leases.
"""

from dataclasses import replace
from typing import Any

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode
from aiscc.providers.models import ProviderCall
from aiscc.providers.tools import ToolDispatchContext
from aiscc.public_live.luna_profile import bind_call
from aiscc.security.policy import default_profiles

_PUBLIC_FIXED_TOOL_RESOURCE_IDENTITY = (
    "aiscc-stockroom-tools:2:stockroom_summary:1:stockroom-summary-v1"
)


def luna_permission_profiles() -> dict[str, Any]:
    profiles = default_profiles()
    key = RuntimeMode.PUBLIC_BOUNDED_LIVE.value
    profiles[key] = replace(
        profiles[key],
        resources=profiles[key].resources
        - {
            ResourceDomain.PROCESS,
            ResourceDomain.FILESYSTEM,
            ResourceDomain.NETWORK,
        },
        fixed_scenarios=frozenset({"stockroom-s1-normal"}),
    )
    return profiles


class LunaScopeAuthority:
    """Per-request server scope, used as SecurityPolicy's Stockroom authority."""

    def __init__(self, call: ProviderCall, ticket: dict[str, Any], *, owner: str) -> None:
        bound, _ = bind_call(call, role=ticket["role"])
        if (
            owner != call.work_run_id
            or ticket["outcome"] != "STARTED"
            or ticket["model"] != call.profile.model_ref
            or ticket["effort"] != bound.reasoning_effort
        ):
            raise ValueError("DURABLE_LUNA_SCOPE_DENIED")
        self._call = bound
        self.context = object()

    def allows(self, context: object, **values: Any) -> bool:
        call = self._call
        mode = values["mode"]
        scenario_id = values["scenario_id"]
        action = values["action"]
        scope = values["scope"]
        principal = values["principal"]
        run_id = values["run_id"]
        operation_fingerprint = values["operation_fingerprint"]
        identities = {
            ResourceDomain.PROVIDER: call.profile.provider_resource_identity,
            ResourceDomain.SECRET: call.profile.secret_resource_identity,
        }
        return (
            context is self.context
            and mode is RuntimeMode.PUBLIC_BOUNDED_LIVE
            and scenario_id == "stockroom-s1-normal"
            and action is SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT
            and principal == call.principal
            and run_id == call.work_run_id
            and operation_fingerprint == call.operation_fingerprint
            and scope.domain in identities
            and scope.resource_id == identities[scope.domain]
        )


class PublicLiveFixedToolScopeAuthority:
    """One exact fixed Public Live tool binding without process or I/O authority."""

    def __init__(
        self,
        *,
        dispatch_context: ToolDispatchContext | None = None,
        implementation_fingerprint: str,
        principal: str,
        fingerprint: str | None = None,
        run_id: str | None = None,
    ) -> None:
        if (
            not principal
            or len(implementation_fingerprint) != 64
            or any(character not in "0123456789abcdef" for character in implementation_fingerprint)
            or (dispatch_context is None) == (run_id is None)
        ):
            raise ValueError("PUBLIC_STOCKROOM_SCOPE_DENIED")
        self._implementation_fingerprint = implementation_fingerprint
        expected_run_id = dispatch_context.work_run_id if dispatch_context is not None else run_id
        if expected_run_id is None:
            raise ValueError("PUBLIC_STOCKROOM_SCOPE_DENIED")
        self._expected_run_id: str = expected_run_id
        self.dispatch_context: ToolDispatchContext | None = None
        self.principal = principal
        self.fingerprint: str | None = None
        self.context = object()
        if dispatch_context is not None:
            if fingerprint is None:
                raise ValueError("PUBLIC_STOCKROOM_SCOPE_DENIED")
            self.bind(dispatch_context=dispatch_context, fingerprint=fingerprint)

    def bind(self, *, dispatch_context: ToolDispatchContext, fingerprint: str) -> object:
        if (
            dispatch_context.profile_id != "public-live-luna-v1"
            or dispatch_context.runtime_mode != RuntimeMode.PUBLIC_BOUNDED_LIVE.value
            or dispatch_context.scenario_id != "stockroom-s1-normal"
            or dispatch_context.resolved_spec_fingerprint != ""
            or dispatch_context.resolved_implementation_fingerprint
            != self._implementation_fingerprint
            or dispatch_context.work_run_id != self._expected_run_id
            or len(fingerprint) != 64
        ):
            raise ValueError("PUBLIC_STOCKROOM_SCOPE_DENIED")
        if self.dispatch_context is not None and (
            self.dispatch_context != dispatch_context or self.fingerprint != fingerprint
        ):
            raise ValueError("PUBLIC_STOCKROOM_SCOPE_ALREADY_BOUND")
        self.dispatch_context = dispatch_context
        self.fingerprint = fingerprint
        return self.context

    def owns_scope(
        self,
        *,
        scope: ResourceScope,
        principal: str,
        run_id: str,
        operation_fingerprint: str | None,
    ) -> bool:
        return (
            self.dispatch_context is not None
            and scope.domain is ResourceDomain.TOOL
            and scope.resource_id == _PUBLIC_FIXED_TOOL_RESOURCE_IDENTITY
            and principal == self.principal
            and run_id == self.dispatch_context.work_run_id
            and operation_fingerprint == self.fingerprint
        )

    def allows(self, context: object, **values: Any) -> bool:
        mode = values["mode"]
        scenario_id = values["scenario_id"]
        action = values["action"]
        scope = values["scope"]
        principal = values["principal"]
        run_id = values["run_id"]
        operation_fingerprint = values["operation_fingerprint"]
        return (
            self.dispatch_context is not None
            and context is self.context
            and mode is RuntimeMode.PUBLIC_BOUNDED_LIVE
            and scenario_id == "stockroom-s1-normal"
            and action is SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT
            and principal == self.principal
            and run_id == self.dispatch_context.work_run_id
            and operation_fingerprint == self.fingerprint
            and scope.domain is ResourceDomain.TOOL
            and scope.resource_id == _PUBLIC_FIXED_TOOL_RESOURCE_IDENTITY
        )
