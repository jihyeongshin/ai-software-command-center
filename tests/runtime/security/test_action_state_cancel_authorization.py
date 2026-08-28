from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from datetime import datetime

import pytest
from conftest import DockerEvidenceObserver

from aiscc.contracts.security import (
    PermissionRequest,
    ResourceDomain,
    ResourceScope,
    SecurityActionClass,
    SecurityAdmissionDecision,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.runtime.docker import DockerRunSpec, DockerRuntime
from aiscc.security.cancel import CancelIntentStore, CancelRequest, PublicRunControlGrant
from aiscc.security.capability import Capability
from aiscc.security.policy import SecurityPolicy

BASE_IMAGE = (
    "python:3.12.14-slim-bookworm@"
    "sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579"
)


def _grant(snapshot: WorkflowSnapshot, expires_at: datetime) -> PublicRunControlGrant:
    return PublicRunControlGrant(
        "grant-runtime",
        "v1",
        "session-a-user",
        "session-a",
        snapshot.run_id,
        "request-runtime",
        SecurityActionClass.PUBLIC_CANCEL_CONTROL,
        RuntimeMode.PUBLIC_BOUNDED_LIVE,
        "p1-3-v2",
        "scenario-v1",
        snapshot.state_version,
        expires_at,
    )


@pytest.mark.runtime
def test_exact_action_state_capability_cleanup_and_cancel_contract(
    policy: SecurityPolicy,
    docker: DockerRuntime,
    docker_observer: DockerEvidenceObserver,
    unique_id: Callable[[str], str],
    request_factory: Callable[..., PermissionRequest],
    capability_factory: Callable[..., Capability],
    snapshot: WorkflowSnapshot,
    future_time: datetime,
) -> None:
    blocked = replace(snapshot, state=WorkflowState.BLOCKED, state_version=8)
    wrong_state = policy.evaluate(request_factory(observed=blocked, authoritative=blocked))
    assert wrong_state.reason == "ACTION_STATE_NOT_ADMISSIBLE"

    mode_name = unique_id("aiscc-mode-denied")
    mode_spec = DockerRunSpec(
        name=mode_name,
        run_id=snapshot.run_id,
        resource_id="process:owner-runtime-mode-proof",
        image=BASE_IMAGE,
        command=("python", "-c", "print('must-not-run')"),
    )
    docker_observer.register(mode_name)
    mode_result = docker.run(
        capability_factory(scope=mode_spec.scope(), current=snapshot),
        principal="owner-user-1",
        current_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        current=snapshot,
        profile_version="p1-3-v2",
        spec=mode_spec,
    )
    assert not mode_result.executed
    assert mode_result.security_reason == "CAPABILITY_MODE_MISMATCH"
    assert not docker_observer.exists(mode_name)

    stale_spec = DockerRunSpec(
        name=unique_id("aiscc-stale-denied"),
        run_id=snapshot.run_id,
        resource_id="process:owner-stale-proof",
        image=BASE_IMAGE,
        command=("python", "-c", "print('must-not-run')"),
    )
    docker_observer.register(stale_spec.name)
    stale_capability = capability_factory(scope=stale_spec.scope(), current=snapshot)
    stale_result = docker.run(
        stale_capability,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=blocked,
        profile_version="p1-3-v2",
        spec=stale_spec,
    )
    assert not stale_result.executed
    assert stale_result.security_reason == "CAPABILITY_STALE_STATE_VERSION"
    assert not docker_observer.exists(stale_spec.name)

    terminal = replace(snapshot, state=WorkflowState.ACCEPTED, state_version=9)
    terminal_result = docker.run(
        stale_capability,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=terminal,
        profile_version="p1-3-v2",
        spec=stale_spec,
    )
    assert not terminal_result.executed and not docker_observer.exists(stale_spec.name)

    cleanup_run = unique_id("run-safety")
    running = WorkflowSnapshot(cleanup_run, WorkflowState.RUNNING, 1)
    container = unique_id("aiscc-safety")
    docker_observer.register(container)
    create_spec = DockerRunSpec(
        name=container,
        run_id=cleanup_run,
        resource_id="process:owner-existing-resource",
        image=BASE_IMAGE,
        command=("python", "-c", "print('existing-resource')"),
    )
    created = docker.run(
        capability_factory(scope=create_spec.scope(), current=running),
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=running,
        profile_version="p1-3-v2",
        spec=create_spec,
    )
    assert created.exit_code == 0
    blocked_cleanup = WorkflowSnapshot(cleanup_run, WorkflowState.BLOCKED, 2)
    cleanup_scope = ResourceScope(
        ResourceDomain.PROCESS, f"container:{container}", target_name=container
    )
    cleanup_capability = capability_factory(
        scope=cleanup_scope,
        current=blocked_cleanup,
        action=SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
    )
    assert (
        docker.cleanup_container(
            cleanup_capability,
            principal="owner-user-1",
            current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            current=blocked_cleanup,
            profile_version="p1-3-v2",
            name=container,
        ).exit_code
        == 0
    )
    assert not docker_observer.exists(container)

    grant = _grant(snapshot, future_time)
    base_cancel = CancelRequest(
        grant.principal,
        grant.session_id,
        snapshot.run_id,
        snapshot,
        grant.profile_version,
        grant.scenario_version,
        "cancel-runtime-key",
        grant,
    )
    assert (
        not CancelIntentStore()
        .authorize(replace(base_cancel, session_id="session-b"), snapshot)
        .admitted
    )
    assert (
        not CancelIntentStore()
        .authorize(replace(base_cancel, principal="replay-reader", grant=None), snapshot)
        .admitted
    )
    store = CancelIntentStore()
    first = store.authorize(base_cancel, snapshot)
    second = store.authorize(base_cancel, snapshot)
    assert first.admitted and first == second and store.control_effect_count == 1

    terminal_decision = policy.evaluate(request_factory(observed=terminal, authoritative=terminal))
    assert terminal_decision.decision is SecurityAdmissionDecision.DENY
