from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot
from aiscc.security.capability import Capability
from aiscc.security.policy import SecurityPolicy


def test_capability_is_bound_to_state_version_action_resource_and_use_ledger(
    policy: SecurityPolicy,
    snapshot: WorkflowSnapshot,
    capability_factory: Callable[..., Capability],
) -> None:
    scope = ResourceScope(ResourceDomain.PROCESS, "process:owner-proof", argv=("python", "-V"))
    capability = capability_factory(scope=scope)
    first = policy.consume_capability(
        capability,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=snapshot,
        profile_version="p1-3-v2",
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=scope,
    )
    assert first.allowed and first.consumed_use_count == 1
    assert first.provenance["reason"] == "CAPABILITY_CONSUMED"

    repeated = policy.consume_capability(
        capability,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=snapshot,
        profile_version="p1-3-v2",
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=scope,
    )
    assert not repeated.allowed and repeated.reason == "CAPABILITY_USE_LIMIT"

    fresh_capability = capability_factory(scope=scope)
    stale = replace(snapshot, state_version=snapshot.state_version + 1)
    stale_use = policy.consume_capability(
        fresh_capability,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=stale,
        profile_version="p1-3-v2",
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=scope,
    )
    assert not stale_use.allowed and stale_use.reason == "CAPABILITY_STALE_STATE_VERSION"


def test_wrong_action_resource_run_and_profile_never_consume(
    policy: SecurityPolicy,
    snapshot: WorkflowSnapshot,
    capability_factory: Callable[..., Capability],
) -> None:
    scope = ResourceScope(ResourceDomain.PROCESS, "process:owner-proof", argv=("python", "-V"))
    capability = capability_factory(scope=scope, max_uses=4)
    mismatches: tuple[tuple[SecurityActionClass, ResourceScope, WorkflowSnapshot, str], ...] = (
        (
            SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
            scope,
            snapshot,
            "p1-3-v2",
        ),
        (
            SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            replace(scope, resource_id="process:wrong"),
            snapshot,
            "p1-3-v2",
        ),
        (
            SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            scope,
            replace(snapshot, run_id="wrong-run"),
            "p1-3-v2",
        ),
        (
            SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            scope,
            snapshot,
            "wrong-profile",
        ),
    )
    for action, mismatched_scope, current, profile_version in mismatches:
        use = policy.consume_capability(
            capability,
            principal="owner-user-1",
            current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            current=current,
            profile_version=profile_version,
            action=action,
            scope=mismatched_scope,
        )
        assert not use.allowed

    valid = policy.consume_capability(
        capability,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=snapshot,
        profile_version="p1-3-v2",
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=scope,
    )
    assert valid.allowed and valid.consumed_use_count == 1


def test_current_runtime_mode_is_independent_from_shared_profile_version(
    policy: SecurityPolicy,
    snapshot: WorkflowSnapshot,
    capability_factory: Callable[..., Capability],
) -> None:
    scope = ResourceScope(ResourceDomain.PROCESS, "process:owner-mode", argv=("python", "-V"))
    capability = capability_factory(scope=scope)
    mismatch = policy.consume_capability(
        capability,
        principal="owner-user-1",
        current_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        current=snapshot,
        profile_version="p1-3-v2",
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=scope,
    )
    assert not mismatch.allowed
    assert mismatch.reason == "CAPABILITY_MODE_MISMATCH"
    assert mismatch.consumed_use_count == 0
