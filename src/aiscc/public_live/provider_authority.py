"""Explicit Public Live P1-5 composition; default permission profiles stay closed.

This scope authority is constructed from a committed semantic request and the
existing server-owned ProviderProfile. It does not issue credentials or replace
the independent provider/secret selectors, receipts, or leases.
"""

from dataclasses import replace

from aiscc.contracts.security import ResourceDomain, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode
from aiscc.providers.models import ProviderCall
from aiscc.public_live.luna_profile import bind_call
from aiscc.security.policy import default_profiles


def luna_permission_profiles():
    profiles = default_profiles()
    key = RuntimeMode.PUBLIC_BOUNDED_LIVE.value
    profiles[key] = replace(profiles[key], fixed_scenarios=frozenset({"stockroom-s1-normal"}))
    return profiles


class LunaScopeAuthority:
    """Per-request server scope, used as SecurityPolicy's Stockroom authority."""

    def __init__(self, call: ProviderCall, ticket: dict, *, owner: str):
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

    def allows(
        self, context, *, mode, scenario_id, action, scope, principal, run_id, operation_fingerprint
    ):
        call = self._call
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


class LunaToolScopeAuthority:
    """One exact resolved Stockroom process scope, never a public argv selector."""

    def __init__(self, *, dispatch_context, spec, principal: str, fingerprint: str):
        from aiscc.providers.stockroom_tool import stockroom_spec_fingerprint

        if (
            dispatch_context.profile_id != "public-live-luna-v1"
            or dispatch_context.runtime_mode != RuntimeMode.PUBLIC_BOUNDED_LIVE.value
            or dispatch_context.scenario_id != "stockroom-s1-normal"
            or dispatch_context.resolved_spec_fingerprint != stockroom_spec_fingerprint(spec)
            or spec.resource_id != "process:stockroom-summary-v1"
            or spec.command != ("python", "-B", "-m", "stockroom", "summary")
            or spec.network != "none"
        ):
            raise ValueError("PUBLIC_STOCKROOM_SCOPE_DENIED")
        self.process_scope = spec.scope()
        self.dispatch_context = dispatch_context
        self.principal = principal
        self.fingerprint = fingerprint
        self.context = object()

    def owns_scope(self, *, scope, principal, run_id, operation_fingerprint):
        return (
            scope == self.process_scope
            and principal == self.principal
            and run_id == self.dispatch_context.work_run_id
            and operation_fingerprint == self.fingerprint
        )

    def allows(
        self, context, *, mode, scenario_id, action, scope, principal, run_id, operation_fingerprint
    ):
        return (
            context is self.context
            and mode is RuntimeMode.PUBLIC_BOUNDED_LIVE
            and scenario_id == "stockroom-s1-normal"
            and action is SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT
            and principal == self.principal
            and run_id == self.dispatch_context.work_run_id
            and operation_fingerprint == self.fingerprint
            and (
                scope == self.process_scope
                or (
                    scope.domain is ResourceDomain.TOOL
                    and scope.resource_id
                    == "aiscc-stockroom-tools:2:stockroom_summary:1:stockroom-summary-v1"
                )
            )
        )
