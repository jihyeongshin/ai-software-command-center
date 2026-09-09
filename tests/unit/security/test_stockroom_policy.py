from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from aiscc.contracts.security import (
    AuthorityStatus,
    PermissionRequest,
    ResourceDomain,
    ResourceScope,
    SecurityActionClass,
    SecurityAdmissionDecision,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.providers.stockroom_tool import build_stockroom_spec, load_stockroom_tool_config
from aiscc.security.capability import CapabilityConsumeRequest
from aiscc.security.policy import SecurityPolicy, default_profiles
from aiscc.security.stockroom_policy import (
    StockroomOwnerRestriction,
    load_stockroom_owner_policy,
)

POLICY_CONFIG = Path("config/security/stockroom-owner.v1.toml")
TOOL_CONFIG = Path("config/providers/stockroom-tools.v1.toml")
FINGERPRINT = "a" * 64
SPEC_FINGERPRINT = "b" * 64


def _restriction() -> StockroomOwnerRestriction:
    return StockroomOwnerRestriction(load_stockroom_owner_policy(POLICY_CONFIG))


def _scope(tmp_path: Path, *, run_id: str = "run-stockroom") -> ResourceScope:
    spec = build_stockroom_spec(
        load_stockroom_tool_config(TOOL_CONFIG),
        name="stockroom-test",
        run_id=run_id,
        workspace=tmp_path,
    )
    return spec.scope()


def _context(restriction: StockroomOwnerRestriction, scope: ResourceScope, **overrides):
    values = {
        "context_id": f"context-{id(overrides)}-{len(restriction._contexts)}",
        "principal": "owner",
        "task_action": "fixed-stockroom-summary",
        "mode": RuntimeMode.OWNER_SELF_DOGFOOD,
        "scenario_id": "stockroom-s1-normal",
        "profile_id": "stockroom-owner-s1-v1",
        "run_id": "run-stockroom",
        "attempt_id": "attempt-stockroom",
        "state": WorkflowState.RUNNING,
        "state_version": 1,
        "security_action": SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        "scope": scope,
        "operation_fingerprint": FINGERPRINT,
        "process_spec_fingerprint": SPEC_FINGERPRINT,
        "remaining_provider_calls": 2,
        "remaining_tool_calls": 1,
        "remaining_process_calls": 1,
        "remaining_seconds": 30,
        "remaining_budget_units": 4,
        "repository_capability_ref": "repository-capability",
        "filesystem_capability_ref": "filesystem-capability",
        "process_capability_ref": "process-capability",
        "materialized_resource_owner_ref": "materialized-owner",
        "runtime_root_owner_ref": "runtime-root-owner",
        "network_requested": False,
    }
    values.update(overrides)
    return restriction.seal_context(**values)


def _allows(restriction, context, scope, **overrides) -> bool:
    values = {
        "mode": RuntimeMode.OWNER_SELF_DOGFOOD,
        "scenario_id": "stockroom-s1-normal",
        "action": SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        "scope": scope,
        "principal": "owner",
        "run_id": "run-stockroom",
        "operation_fingerprint": FINGERPRINT,
    }
    values.update(overrides)
    return restriction.allows(context, **values)


def test_strict_owner_policy_and_exact_context_are_eligible(tmp_path: Path) -> None:
    restriction = _restriction()
    scope = _scope(tmp_path)
    context = _context(restriction, scope)
    assert _allows(restriction, context, scope)
    network_scope = ResourceScope(
        ResourceDomain.NETWORK, "network:forbidden", network_name="net"
    )
    assert not _allows(restriction, context, network_scope)


@pytest.mark.parametrize(
    "overrides",
    [
        {"mode": RuntimeMode.PUBLIC_BOUNDED_LIVE},
        {"scenario_id": "unknown"},
        {"profile_id": "wrong-profile"},
        {"run_id": "wrong-run"},
        {"attempt_id": ""},
        {"state": WorkflowState.READY},
        {"state_version": 0},
        {"task_action": "wrong-action"},
        {"process_spec_fingerprint": "c" * 63},
        {"remaining_provider_calls": 0},
        {"remaining_tool_calls": 0},
        {"remaining_process_calls": 0},
        {"remaining_seconds": 0},
        {"remaining_budget_units": 0},
        {"network_requested": True},
        {"materialized_resource_owner_ref": ""},
        {"runtime_root_owner_ref": "unknown owner"},
    ],
)
def test_each_unresolved_sealed_dimension_denies(tmp_path: Path, overrides: dict) -> None:
    restriction = _restriction()
    scope = _scope(tmp_path, run_id=str(overrides.get("run_id", "run-stockroom")))
    context = _context(restriction, scope, **overrides)
    assert not _allows(restriction, context, scope)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("scenario_version", "2.0.0"),
        ("profile_version", "2"),
        ("resource_ref", "repository:wrong@" + "0" * 64),
        ("enrolled_tool_id", "wrong-tool"),
        ("enrolled_tool_action", "wrong-action"),
        ("operation_fingerprint", "d" * 64),
        ("repository_capability_ref", ""),
        ("filesystem_capability_ref", ""),
        ("process_capability_ref", ""),
    ],
)
def test_forged_context_dimensions_deny(tmp_path: Path, field: str, value: object) -> None:
    restriction = _restriction()
    scope = _scope(tmp_path)
    context = replace(_context(restriction, scope), **{field: value})
    assert not _allows(restriction, context, scope)


def test_context_is_mandatory_and_does_not_grant_by_itself(tmp_path: Path) -> None:
    restriction = _restriction()
    policy = SecurityPolicy(default_profiles(), stockroom_policy=restriction)
    scope = _scope(tmp_path)
    snapshot = WorkflowSnapshot("run-stockroom", WorkflowState.RUNNING, 1)
    grant_without_context = policy.issue_resource_grant(
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        profile_version="p1-3-v2",
        principal="owner",
        run_id=snapshot.run_id,
        scope=scope,
        operation_fingerprint=FINGERPRINT,
        **SCENARIO_ACTION,
    )
    assert grant_without_context is None
    permission = PermissionRequest(
        "owner",
        snapshot.run_id,
        RuntimeMode.OWNER_SELF_DOGFOOD,
        snapshot,
        snapshot,
        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope,
        None,
        "p1-3-v2",
        "stockroom-s1-normal",
        AuthorityStatus.GRANTED,
        AuthorityStatus.GRANTED,
        AuthorityStatus.GRANTED,
        AuthorityStatus.GRANTED,
        AuthorityStatus.GRANTED,
        AuthorityStatus.NOT_APPLICABLE,
    )
    assert policy.evaluate(permission).decision is SecurityAdmissionDecision.DENY

    context = _context(restriction, scope)
    valid_grant = policy.issue_resource_grant(
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        profile_version="p1-3-v2",
        principal="owner",
        run_id=snapshot.run_id,
        scope=scope,
        operation_fingerprint=FINGERPRINT,
        stockroom_context=context,
        **SCENARIO_ACTION,
    )
    assert valid_grant is not None
    assert (
        policy.issue_resource_grant(
            mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            profile_version="wrong-base-profile",
            principal="owner",
            run_id=snapshot.run_id,
            scope=scope,
            operation_fingerprint=FINGERPRINT,
            stockroom_context=context,
            **SCENARIO_ACTION,
        )
        is None
    )


def test_receipt_forgery_staleness_and_exhaustion_deny(tmp_path: Path) -> None:
    restriction = _restriction()
    policy = SecurityPolicy(default_profiles(), stockroom_policy=restriction)
    scope = _scope(tmp_path)
    snapshot = WorkflowSnapshot("run-stockroom", WorkflowState.RUNNING, 1)
    context = _context(restriction, scope)
    grant = policy.issue_resource_grant(
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        profile_version="p1-3-v2",
        scenario_id="stockroom-s1-normal",
        principal="owner",
        run_id=snapshot.run_id,
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=scope,
        operation_fingerprint=FINGERPRINT,
        stockroom_context=context,
    )
    permission = PermissionRequest(
        "owner",
        snapshot.run_id,
        RuntimeMode.OWNER_SELF_DOGFOOD,
        snapshot,
        snapshot,
        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope,
        grant,
        "p1-3-v2",
        "stockroom-s1-normal",
        *(AuthorityStatus.GRANTED for _ in range(5)),
        AuthorityStatus.NOT_APPLICABLE,
    )
    capability = policy.issue_capability(policy.evaluate(permission), permission)
    assert capability is not None
    request = CapabilityConsumeRequest(
        capability,
        "owner",
        RuntimeMode.OWNER_SELF_DOGFOOD,
        snapshot,
        "p1-3-v2",
        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope,
        None,
        FINGERPRINT,
    )
    uses, receipts = policy.consume_capabilities_atomically_with_receipts((request,))
    assert uses[0].allowed and len(receipts) == 1
    receipt = receipts[0]
    assert policy.verify_consumption_receipt(receipt, request)
    assert not policy.verify_consumption_receipt(
        replace(receipt, _issuer_token=object()), request
    )
    stale = replace(request, current=WorkflowSnapshot(snapshot.run_id, snapshot.state, 2))
    assert not policy.verify_consumption_receipt(receipt, stale)
    denied, no_receipts = policy.consume_capabilities_atomically_with_receipts((request,))
    assert not denied[0].allowed and no_receipts == ()


SCENARIO_ACTION = {
    "scenario_id": "stockroom-s1-normal",
    "action": SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
}
