from __future__ import annotations

import subprocess
import sys
from collections.abc import Callable
from dataclasses import replace
from pathlib import Path

import pytest

from aiscc.api.routes.control import EvaluationInput, evaluate_security
from aiscc.contracts.security import (
    AuthorityStatus,
    PermissionRequest,
    ResourceDomain,
    ResourceScope,
    SecurityActionClass,
    SecurityAdmissionDecision,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.runtime.contracts import RuntimeOutcomeStatus
from aiscc.runtime.docker import DockerRunSpec, DockerRuntime
from aiscc.runtime.process import BoundedProcessRunner
from aiscc.security.capability import Capability
from aiscc.security.policy import SecurityPolicy


def test_process_broker_requires_valid_capability_and_executes_once(
    policy: SecurityPolicy,
    snapshot: WorkflowSnapshot,
    capability_factory: Callable[..., Capability],
) -> None:
    argv = (sys.executable, "-c", "print('BROKER_EXECUTED_ONCE')")
    scope = ResourceScope(ResourceDomain.PROCESS, "process:owner-broker", argv=argv)
    runner = BoundedProcessRunner(policy)

    denied = runner.run(
        None,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=snapshot,
        profile_version="p1-3-v2",
        resource_id=scope.resource_id,
        argv=argv,
        timeout_seconds=2,
        max_attempts=1,
    )
    assert not denied.executed and denied.security_reason == "CAPABILITY_REQUIRED"

    capability = capability_factory(scope=scope)
    allowed = runner.run(
        capability,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=snapshot,
        profile_version="p1-3-v2",
        resource_id=scope.resource_id,
        argv=argv,
        timeout_seconds=2,
        max_attempts=1,
    )
    assert allowed.status is RuntimeOutcomeStatus.SUCCESS
    assert allowed.executed and allowed.stdout.strip() == "BROKER_EXECUTED_ONCE"
    repeated = runner.run(
        capability,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=snapshot,
        profile_version="p1-3-v2",
        resource_id=scope.resource_id,
        argv=argv,
        timeout_seconds=2,
        max_attempts=1,
    )
    assert not repeated.executed and repeated.security_reason == "CAPABILITY_USE_LIMIT"


def test_docker_broker_and_safety_path_fail_closed_without_exact_capability(
    policy: SecurityPolicy,
    snapshot: WorkflowSnapshot,
    capability_factory: Callable[..., Capability],
) -> None:
    docker = DockerRuntime(policy, executable="must-not-be-invoked")
    spec = DockerRunSpec(
        name="must-not-exist",
        run_id=snapshot.run_id,
        resource_id="process:owner-deny-proof",
        image="not-used",
        command=("python", "-c", "print('must-not-run')"),
    )
    no_capability = docker.run(
        None,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=snapshot,
        profile_version="p1-3-v2",
        spec=spec,
    )
    assert not no_capability.executed and no_capability.exit_code is None

    cleanup_scope = ResourceScope(
        ResourceDomain.PROCESS, "container:must-not-exist", target_name="must-not-exist"
    )
    safety_capability = capability_factory(
        scope=cleanup_scope,
        action=SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
    )
    wrong_boundary = docker.run(
        safety_capability,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=snapshot,
        profile_version="p1-3-v2",
        spec=spec,
    )
    assert not wrong_boundary.executed
    cleanup_without_capability = docker.cleanup_container(
        None,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=snapshot,
        profile_version="p1-3-v2",
        name="must-not-exist",
    )
    assert not cleanup_without_capability.executed


def test_stale_and_mismatched_capabilities_never_reach_process(
    policy: SecurityPolicy,
    snapshot: WorkflowSnapshot,
    capability_factory: Callable[..., Capability],
    tmp_path: Path,
) -> None:
    marker = tmp_path / "must-not-be-created"
    argv = (
        sys.executable,
        "-c",
        f"from pathlib import Path;Path({str(marker)!r}).write_text('side-effect')",
    )
    scope = ResourceScope(ResourceDomain.PROCESS, "process:owner-no-side-effect", argv=argv)
    runner = BoundedProcessRunner(policy)
    cases: tuple[tuple[Capability, WorkflowSnapshot, str, str], ...] = (
        (
            capability_factory(scope=scope),
            replace(snapshot, state_version=snapshot.state_version + 1),
            "p1-3-v2",
            scope.resource_id,
        ),
        (capability_factory(scope=scope), snapshot, "wrong-profile", scope.resource_id),
        (capability_factory(scope=scope), snapshot, "p1-3-v2", "process:wrong-resource"),
        (
            capability_factory(
                scope=ResourceScope(
                    ResourceDomain.PROCESS,
                    "container:wrong-action",
                    target_name="wrong-action",
                ),
                action=SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
            ),
            snapshot,
            "p1-3-v2",
            scope.resource_id,
        ),
    )
    for capability, current, profile_version, resource_id in cases:
        result = runner.run(
            capability,
            principal="owner-user-1",
            current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            current=current,
            profile_version=profile_version,
            resource_id=resource_id,
            argv=argv,
            timeout_seconds=2,
            max_attempts=1,
        )
        assert not result.executed
        assert not marker.exists()


def test_mode_mismatch_and_capability_free_docker_reads_never_reach_runtime(
    policy: SecurityPolicy,
    snapshot: WorkflowSnapshot,
    capability_factory: Callable[..., Capability],
) -> None:
    argv = (sys.executable, "-c", "raise SystemExit('must-not-run')")
    scope = ResourceScope(ResourceDomain.PROCESS, "process:owner-mode-deny", argv=argv)
    result = BoundedProcessRunner(policy).run(
        capability_factory(scope=scope),
        principal="owner-user-1",
        current_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        current=snapshot,
        profile_version="p1-3-v2",
        resource_id=scope.resource_id,
        argv=argv,
        timeout_seconds=2,
        max_attempts=1,
    )
    assert not result.executed
    assert result.security_reason == "CAPABILITY_MODE_MISMATCH"

    docker = DockerRuntime(policy, executable="must-not-be-invoked")
    assert not hasattr(docker, "inspect")
    assert not hasattr(docker, "inspect_format")
    assert not hasattr(docker, "wait")
    assert not hasattr(docker, "exists")
    denied = docker.read_container_metadata(
        None,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=snapshot,
        profile_version="p1-3-v2",
        name="unrelated-container",
    )
    assert not denied.executed
    assert denied.stdout == ""
    assert denied.security_reason == "CAPABILITY_REQUIRED"


def test_public_live_capability_is_denied_in_replay_context_even_with_shared_profile(
    policy: SecurityPolicy,
    request_factory: Callable[..., PermissionRequest],
) -> None:
    request = request_factory()
    decision = policy.evaluate(request)
    capability = policy.issue_capability(decision, request)
    assert capability is not None
    use = policy.consume_capability(
        capability,
        principal=request.principal,
        current_mode=RuntimeMode.PUBLIC_RECORDED_REPLAY,
        current=request.authoritative,
        profile_version=request.profile_version,
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=request.resource_scope,
    )
    assert not use.allowed
    assert use.reason == "CAPABILITY_MODE_MISMATCH"
    assert use.consumed_use_count == 0


def test_exact_read_capability_returns_only_fixed_owned_container_metadata(
    policy: SecurityPolicy,
    snapshot: WorkflowSnapshot,
    capability_factory: Callable[..., Capability],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[list[str]] = []

    def fake_run(args: list[str], **_: object) -> subprocess.CompletedProcess[str]:
        calls.append(args)
        stdout = snapshot.run_id if "aiscc.run_id" in args[3] else '"running"'
        return subprocess.CompletedProcess(args, 0, stdout=f"{stdout}\n", stderr="")

    monkeypatch.setattr("aiscc.runtime.docker.subprocess.run", fake_run)
    name = "exact-test-owned-container"
    scope = ResourceScope(
        ResourceDomain.PROCESS,
        f"container:{name}",
        target_name=name,
    )
    assert (
        policy.issue_resource_grant(
            mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
            profile_version="p1-3-v2",
            scenario_id="p1-3-fixed-synthetic",
            principal="public-user-1",
            run_id=snapshot.run_id,
            action=SecurityActionClass.RUN_REVIEW_READ_ONLY,
            scope=scope,
        )
        is None
    )
    capability = capability_factory(
        scope=scope,
        action=SecurityActionClass.RUN_REVIEW_READ_ONLY,
    )
    result = DockerRuntime(policy).read_container_metadata(
        capability,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=snapshot,
        profile_version="p1-3-v2",
        name=name,
    )
    assert result.executed
    assert result.stdout.strip() == '"running"'
    assert len(calls) == 2
    assert calls[0][1:4] == [
        "inspect",
        "--format",
        '{{index .Config.Labels "aiscc.run_id"}}',
    ]
    assert calls[1][1:4] == ["inspect", "--format", "{{json .State.Status}}"]

    fresh_read_capability = capability_factory(
        scope=scope,
        action=SecurityActionClass.RUN_REVIEW_READ_ONLY,
    )
    execution_spec = DockerRunSpec(
        name=name,
        run_id=snapshot.run_id,
        resource_id="process:owner-read-cannot-execute",
        image="must-not-run",
        command=("python", "-c", "raise SystemExit('must-not-run')"),
    )
    denied_execution = DockerRuntime(policy).run(
        fresh_read_capability,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=snapshot,
        profile_version="p1-3-v2",
        spec=execution_spec,
    )
    assert not denied_execution.executed
    assert denied_execution.security_reason == "CAPABILITY_ACTION_MISMATCH"
    assert len(calls) == 2


def test_deny_decision_cannot_issue_capability(
    policy: SecurityPolicy,
    request_factory: Callable[..., PermissionRequest],
) -> None:
    request = request_factory(requester_authority=AuthorityStatus.UNRESOLVED)
    decision = policy.evaluate(request)
    assert decision.decision is SecurityAdmissionDecision.DENY
    assert policy.issue_capability(decision, request) is None


def test_stale_snapshot_fails_before_capability_issue(
    policy: SecurityPolicy,
    request_factory: Callable[..., PermissionRequest],
    snapshot: WorkflowSnapshot,
) -> None:
    observed = replace(snapshot, state_version=snapshot.state_version - 1)
    request = request_factory(observed=observed)
    decision = policy.evaluate(request)
    assert decision.decision is SecurityAdmissionDecision.DENY
    assert decision.reason == "STALE_REQUEST"


def test_unknown_action_fails_closed(
    policy: SecurityPolicy,
    request_factory: Callable[..., PermissionRequest],
) -> None:
    decision = policy.evaluate(request_factory(action="NEW_ACTION", resource_grant=None))
    assert decision.decision is SecurityAdmissionDecision.DENY
    assert decision.reason == "UNKNOWN_ACTION_CLASS"


def test_public_diagnostic_cannot_manufacture_authoritative_allow() -> None:
    candidate = EvaluationInput(
        principal="caller",
        run_id="caller-run",
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        state=WorkflowState.RUNNING,
        state_version=999,
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        resource_domain=ResourceDomain.PROCESS,
        resource_id="process:caller-chosen",
    )
    result = evaluate_security(candidate)
    assert result.decision == "DENY"
    assert result.reason == "NON_AUTHORITATIVE_DIAGNOSTIC_ONLY"
