from __future__ import annotations

from aiscc.contracts.security import (
    AuthorityStatus,
    PermissionRequest,
    ResourceDomain,
    ResourceScope,
    SecurityActionClass,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.providers.authority import (
    LeaseBoundSecretResolver,
    ProviderToolResourceAuthority,
    SecretResolutionLeaseAuthority,
    SecretUseAuthority,
)
from aiscc.providers.models import (
    ExecutionAttemptRef,
    ExecutionStatus,
    ProviderToolSelectorRequest,
    SecretUseSelectorRequest,
)
from aiscc.providers.service import AgentExecutionService
from aiscc.security.capability import Capability, CapabilityConsumeRequest
from aiscc.security.policy import SecurityPolicy


def _permission(
    call,
    scope_authority,
    policy: SecurityPolicy,
    scope: ResourceScope,
    ref: str,
    selector: object,
    fingerprint: str,
) -> tuple[PermissionRequest, Capability]:
    snapshot = WorkflowSnapshot(call.work_run_id, WorkflowState.RUNNING, 2)
    grant = policy.issue_resource_grant(
        mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        profile_version="p1-3-v2",
        scenario_id="stockroom-s1-normal",
        principal="owner",
        run_id=call.work_run_id,
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=scope,
        selector_attestation_ref=ref,
        selector_request=selector,
        operation_fingerprint=fingerprint,
        stockroom_context=scope_authority.context,
    )
    request = PermissionRequest(
        "owner",
        call.work_run_id,
        RuntimeMode.PUBLIC_BOUNDED_LIVE,
        snapshot,
        snapshot,
        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope,
        grant,
        "p1-3-v2",
        "stockroom-s1-normal",
        AuthorityStatus.GRANTED,
        AuthorityStatus.GRANTED,
        AuthorityStatus.GRANTED,
        AuthorityStatus.GRANTED,
        AuthorityStatus.GRANTED,
        AuthorityStatus.NOT_APPLICABLE,
    )
    capability = policy.issue_capability(policy.evaluate(request), request)
    assert capability is not None
    return request, capability


def execution_for(call, ticket, adapter, *, resolver_factory=None):
    from aiscc.public_live.provider_authority import LunaScopeAuthority, luna_permission_profiles

    scope_authority = LunaScopeAuthority(call, ticket, owner=call.work_run_id)
    fingerprint = call.operation_fingerprint
    profile = call.profile
    provider_authority = ProviderToolResourceAuthority(
        allowed_resource_identities=frozenset({profile.provider_resource_identity}),
        allowed_profile_ids=frozenset({"public-live-luna-v1"}),
        allowed_scenarios=frozenset({"stockroom-s1-normal"}),
        allowed_modes=frozenset({RuntimeMode.PUBLIC_BOUNDED_LIVE}),
    )
    secret_authority = SecretUseAuthority(
        allowed_secret_refs=frozenset({profile.secret_ref}),
        allowed_profile_ids=frozenset({"public-live-luna-v1"}),
        allowed_scenarios=frozenset({"stockroom-s1-normal"}),
        allowed_destinations=frozenset(
            {"local-fake" if resolver_factory is None else profile.endpoint_ref}
        ),
        allowed_modes=frozenset({RuntimeMode.PUBLIC_BOUNDED_LIVE}),
    )
    policy = SecurityPolicy(
        luna_permission_profiles(),
        stockroom_policy=scope_authority,
        provider_tool_policy=provider_authority,
        secret_use_policy=secret_authority,
    )
    provider_selector = ProviderToolSelectorRequest(
        "PROVIDER",
        profile.provider_resource_identity,
        "owner",
        call.work_run_id,
        call.execution_attempt_id,
        WorkflowState.RUNNING,
        2,
        RuntimeMode.PUBLIC_BOUNDED_LIVE,
        "public-live-luna-v1",
        "1",
        "stockroom-s1-normal",
        fingerprint,
    )
    secret_selector = SecretUseSelectorRequest(
        profile.secret_ref,
        "PROVIDER_API",
        "RESPONSES_CREATE",
        "local-fake" if resolver_factory is None else profile.endpoint_ref,
        profile.provider_resource_identity,
        "responses-v1",
        "owner",
        call.work_run_id,
        call.execution_attempt_id,
        call.operation_id,
        WorkflowState.RUNNING,
        2,
        RuntimeMode.PUBLIC_BOUNDED_LIVE,
        "public-live-luna-v1",
        "1",
        "stockroom-s1-normal",
        fingerprint,
    )
    provider_ref = provider_authority.attest(provider_selector).attestation_id
    secret_ref = secret_authority.attest(secret_selector).attestation_id
    provider_scope = ResourceScope(ResourceDomain.PROVIDER, profile.provider_resource_identity)
    secret_scope = ResourceScope(ResourceDomain.SECRET, profile.secret_resource_identity)
    _, provider_capability = _permission(
        call, scope_authority, policy, provider_scope, provider_ref, provider_selector, fingerprint
    )
    _, secret_capability = _permission(
        call, scope_authority, policy, secret_scope, secret_ref, secret_selector, fingerprint
    )
    snapshot = WorkflowSnapshot(call.work_run_id, WorkflowState.RUNNING, 2)
    requirements = (
        CapabilityConsumeRequest(
            provider_capability,
            "owner",
            RuntimeMode.PUBLIC_BOUNDED_LIVE,
            snapshot,
            "p1-3-v2",
            SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            provider_scope,
            provider_ref,
            fingerprint,
        ),
        CapabilityConsumeRequest(
            secret_capability,
            "owner",
            RuntimeMode.PUBLIC_BOUNDED_LIVE,
            snapshot,
            "p1-3-v2",
            SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            secret_scope,
            secret_ref,
            fingerprint,
        ),
    )

    class Reader:
        def load(self, **kwargs):
            return (
                WorkflowSnapshot(call.work_run_id, WorkflowState.RUNNING, 2),
                ExecutionAttemptRef(
                    call.execution_attempt_id,
                    call.work_run_id,
                    "task",
                    "1",
                    WorkflowState.RUNNING,
                    2,
                    2,
                    ExecutionStatus.RUNNING,
                    "test",
                ),
            )

    lease = SecretResolutionLeaseAuthority(policy.verify_consumption_receipt)
    resolver = (
        LeaseBoundSecretResolver(lease, {profile.secret_ref: "synthetic-local-only"})
        if resolver_factory is None
        else resolver_factory(lease)
    )
    service = AgentExecutionService(
        policy=policy,
        adapter=adapter,
        secret_resolver=resolver,
        authority_reader=Reader(),
        secret_lease_authority=lease,
    )
    return service, requirements, secret_selector, resolver
