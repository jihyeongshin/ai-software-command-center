from __future__ import annotations

from collections.abc import Callable

from aiscc.contracts.security import (
    AuthorityStatus,
    PermissionRequest,
    ResourceDomain,
    ResourceScope,
    SecurityActionClass,
    SecurityAdmissionDecision,
)
from aiscc.security.policy import SecurityPolicy


def test_all_independent_guards_allow_valid_request(
    policy: SecurityPolicy,
    request_factory: Callable[..., PermissionRequest],
) -> None:
    decision = policy.evaluate(request_factory())

    assert decision.decision is SecurityAdmissionDecision.ALLOW
    assert decision.admission_id is not None
    assert all(passed for _, passed in decision.guards)


def test_each_missing_or_unresolved_guard_denies(
    policy: SecurityPolicy,
    request_factory: Callable[..., PermissionRequest],
) -> None:
    authority_fields = (
        "requester_authority",
        "task_scope_authority",
        "limit_authority",
        "budget_authority",
        "idempotency_authority",
    )
    for field in authority_fields:
        for unresolved in (None, AuthorityStatus.UNRESOLVED):
            decision = policy.evaluate(request_factory(**{field: unresolved}))
            assert decision.decision is SecurityAdmissionDecision.DENY, (field, unresolved)

    missing_resource = policy.evaluate(request_factory(resource_grant=None))
    assert missing_resource.reason == "EXACT_RESOURCE_GRANT_DENIED"


def test_mutable_target_control_unresolved_denies(
    policy: SecurityPolicy,
    request_factory: Callable[..., PermissionRequest],
) -> None:
    scope = ResourceScope(ResourceDomain.PROCESS, "container:run-p1-3-target")
    for unresolved in (None, AuthorityStatus.UNRESOLVED):
        decision = policy.evaluate(
            request_factory(
                action=SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
                resource_scope=scope,
                target_control_authority=unresolved,
            )
        )
        assert decision.decision is SecurityAdmissionDecision.DENY


def test_public_live_arbitrary_and_p1_5_owned_resources_deny(
    policy: SecurityPolicy,
    request_factory: Callable[..., PermissionRequest],
) -> None:
    scopes = (
        ResourceScope(ResourceDomain.PROCESS, "process:arbitrary", argv=("python", "-V")),
        ResourceScope(ResourceDomain.REPOSITORY, "repository:owner-private"),
        ResourceScope(ResourceDomain.NETWORK, "network:external", network_name="bridge"),
        ResourceScope(ResourceDomain.PROVIDER, "provider:future-model"),
        ResourceScope(ResourceDomain.TOOL, "tool:future-adapter"),
    )
    for scope in scopes:
        decision = policy.evaluate(request_factory(resource_scope=scope))
        assert decision.decision is SecurityAdmissionDecision.DENY, scope
        assert decision.reason == "EXACT_RESOURCE_GRANT_DENIED"
