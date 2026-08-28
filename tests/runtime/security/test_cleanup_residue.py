from __future__ import annotations

from collections.abc import Callable

import pytest
from conftest import DockerEvidenceObserver

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.runtime.cleanup import cleanup_containers
from aiscc.runtime.contracts import ResourceRecord
from aiscc.runtime.docker import DockerRunSpec, DockerRuntime
from aiscc.security.capability import Capability

BASE_IMAGE = (
    "python:3.12.14-slim-bookworm@"
    "sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579"
)


@pytest.mark.runtime
@pytest.mark.parametrize("exit_code", [0, 3])
def test_success_and_failure_resources_require_safety_capability_for_cleanup(
    docker: DockerRuntime,
    docker_observer: DockerEvidenceObserver,
    unique_id: Callable[[str], str],
    capability_factory: Callable[..., Capability],
    exit_code: int,
) -> None:
    run_id = unique_id("run-clean")
    current = WorkflowSnapshot(run_id, WorkflowState.RUNNING, 1)
    name = unique_id("aiscc-clean")
    docker_observer.register(name)
    spec = DockerRunSpec(
        name=name,
        run_id=run_id,
        resource_id="process:owner-cleanup-proof",
        image=BASE_IMAGE,
        command=("python", "-c", f"raise SystemExit({exit_code})"),
    )
    result = docker.run(
        capability_factory(scope=spec.scope(), current=current),
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=current,
        profile_version="p1-3-v2",
        spec=spec,
    )
    assert result.exit_code == exit_code
    missing_capability = cleanup_containers(
        docker,
        (ResourceRecord(run_id, "container", name),),
        {name: None},
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=current,
        profile_version="p1-3-v2",
    )
    assert not missing_capability.clean and missing_capability.quarantined
    cleanup_scope = ResourceScope(ResourceDomain.PROCESS, f"container:{name}", target_name=name)
    cleanup = cleanup_containers(
        docker,
        (ResourceRecord(run_id, "container", name),),
        {
            name: capability_factory(
                scope=cleanup_scope,
                current=current,
                action=SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
            )
        },
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=current,
        profile_version="p1-3-v2",
    )
    assert cleanup.clean and not cleanup.quarantined and not docker_observer.exists(name)


@pytest.mark.runtime
def test_wrong_ownership_becomes_quarantined_residue(
    docker: DockerRuntime,
    docker_observer: DockerEvidenceObserver,
    unique_id: Callable[[str], str],
    capability_factory: Callable[..., Capability],
) -> None:
    actual_run = unique_id("run-owner")
    current = WorkflowSnapshot(actual_run, WorkflowState.RUNNING, 1)
    name = unique_id("aiscc-residue")
    docker_observer.register(name)
    spec = DockerRunSpec(
        name=name,
        run_id=actual_run,
        resource_id="process:owner-residue-proof",
        image=BASE_IMAGE,
        command=("python", "-c", "print('controlled-residue')"),
    )
    result = docker.run(
        capability_factory(scope=spec.scope(), current=current),
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=current,
        profile_version="p1-3-v2",
        spec=spec,
    )
    assert result.exit_code == 0
    wrong_current = WorkflowSnapshot("wrong-run", WorkflowState.BLOCKED, 1)
    cleanup = cleanup_containers(
        docker,
        (ResourceRecord(actual_run, "container", name),),
        {name: None},
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=wrong_current,
        profile_version="p1-3-v2",
    )
    try:
        assert not cleanup.clean and cleanup.quarantined
        assert cleanup.residue[0].resource_id == name
        assert docker_observer.exists(name)
    finally:
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
