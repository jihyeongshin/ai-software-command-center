from __future__ import annotations

import sys
import threading
from collections.abc import Callable

import pytest
from conftest import DockerEvidenceObserver

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.runtime.contracts import RuntimeOutcomeStatus
from aiscc.runtime.docker import DockerRunSpec, DockerRuntime
from aiscc.runtime.process import BoundedProcessRunner
from aiscc.security.capability import Capability
from aiscc.security.policy import SecurityPolicy

BASE_IMAGE = (
    "python:3.12.14-slim-bookworm@"
    "sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579"
)


@pytest.mark.runtime
def test_timeout_retry_and_explicit_container_cancel_are_broker_bounded(
    policy: SecurityPolicy,
    docker: DockerRuntime,
    docker_observer: DockerEvidenceObserver,
    unique_id: Callable[[str], str],
    capability_factory: Callable[..., Capability],
) -> None:
    run_id = unique_id("run-timeout")
    current = WorkflowSnapshot(run_id, WorkflowState.RUNNING, 1)
    runner = BoundedProcessRunner(policy)
    timeout_argv = (sys.executable, "-c", "import time;time.sleep(5)")
    timeout_scope = ResourceScope(
        ResourceDomain.PROCESS, "process:owner-timeout", argv=timeout_argv
    )
    timeout = runner.run(
        capability_factory(scope=timeout_scope, current=current),
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=current,
        profile_version="p1-3-v2",
        resource_id=timeout_scope.resource_id,
        argv=timeout_argv,
        timeout_seconds=0.1,
        max_attempts=2,
    )
    failure_argv = (sys.executable, "-c", "raise SystemExit(4)")
    failure_scope = ResourceScope(ResourceDomain.PROCESS, "process:owner-retry", argv=failure_argv)
    failure = runner.run(
        capability_factory(scope=failure_scope, current=current),
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=current,
        profile_version="p1-3-v2",
        resource_id=failure_scope.resource_id,
        argv=failure_argv,
        timeout_seconds=1,
        max_attempts=2,
    )
    assert timeout.status is RuntimeOutcomeStatus.TIMEOUT and timeout.executed
    assert failure.status is RuntimeOutcomeStatus.FAILED and failure.attempts == 2

    name = unique_id("aiscc-cancel")
    docker_observer.register(name)
    spec = DockerRunSpec(
        name=name,
        run_id=run_id,
        resource_id="process:owner-cancel",
        image=BASE_IMAGE,
        command=("python", "-c", "import time;time.sleep(30)"),
        detach=True,
    )
    start = docker.run(
        capability_factory(scope=spec.scope(), current=current),
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=current,
        profile_version="p1-3-v2",
        spec=spec,
    )
    assert start.exit_code == 0
    waiter_done = threading.Event()

    def wait_for_container() -> None:
        docker_observer.wait(name, timeout_seconds=10)
        waiter_done.set()

    waiter = threading.Thread(target=wait_for_container)
    waiter.start()
    cleanup_scope = ResourceScope(ResourceDomain.PROCESS, f"container:{name}", target_name=name)
    cleanup_capability = capability_factory(
        scope=cleanup_scope,
        current=current,
        action=SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
    )
    assert (
        docker.cleanup_container(
            cleanup_capability,
            principal="owner-user-1",
            current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            current=current,
            profile_version="p1-3-v2",
            name=name,
        ).exit_code
        == 0
    )
    waiter.join(timeout=5)
    assert waiter_done.is_set() and not docker_observer.exists(name)
