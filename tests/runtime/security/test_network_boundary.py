from __future__ import annotations

import time
from collections.abc import Callable
from pathlib import Path

import pytest
from conftest import DockerEvidenceObserver

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.runtime.docker import DockerCommandResult, DockerRunSpec, DockerRuntime
from aiscc.runtime.network import InternalNetwork
from aiscc.security.capability import Capability

BASE_IMAGE = (
    "python:3.12.14-slim-bookworm@"
    "sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579"
)
FIXTURES = Path(__file__).parents[2] / "fixtures"


@pytest.mark.runtime
def test_broker_default_deny_exact_internal_allow_and_unlisted_deny(
    docker: DockerRuntime,
    docker_observer: DockerEvidenceObserver,
    unique_id: Callable[[str], str],
    capability_factory: Callable[..., Capability],
) -> None:
    run_id = unique_id("run-network")
    current = WorkflowSnapshot(run_id, WorkflowState.RUNNING, 1)

    no_capability_name = unique_id("aiscc-network-no-cap")
    docker_observer.register_network(no_capability_name)
    no_capability = docker.create_internal_network(
        None,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=current,
        profile_version="p1-3-v2",
        name=no_capability_name,
        resource_id=f"network:{no_capability_name}",
    )
    assert not no_capability.executed
    assert no_capability.security_reason == "CAPABILITY_REQUIRED"
    assert not docker_observer.network_exists(no_capability_name)

    wrong_mode_name = unique_id("aiscc-network-wrong-mode")
    docker_observer.register_network(wrong_mode_name)
    wrong_mode_scope = ResourceScope(
        ResourceDomain.NETWORK,
        f"network:{wrong_mode_name}",
        network_name=wrong_mode_name,
        target_name=wrong_mode_name,
    )
    wrong_mode = docker.create_internal_network(
        capability_factory(scope=wrong_mode_scope, current=current),
        principal="owner-user-1",
        current_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        current=current,
        profile_version="p1-3-v2",
        name=wrong_mode_name,
        resource_id=f"network:{wrong_mode_name}",
    )
    assert not wrong_mode.executed
    assert wrong_mode.security_reason == "CAPABILITY_MODE_MISMATCH"
    assert not docker_observer.network_exists(wrong_mode_name)

    wrong_run_name = unique_id("aiscc-network-wrong-run")
    docker_observer.register_network(wrong_run_name)
    wrong_run_scope = ResourceScope(
        ResourceDomain.NETWORK,
        f"network:{wrong_run_name}",
        network_name=wrong_run_name,
        target_name=wrong_run_name,
    )
    wrong_run = docker.create_internal_network(
        capability_factory(scope=wrong_run_scope, current=current),
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=WorkflowSnapshot(unique_id("run-network-wrong"), WorkflowState.RUNNING, 1),
        profile_version="p1-3-v2",
        name=wrong_run_name,
        resource_id=f"network:{wrong_run_name}",
    )
    assert not wrong_run.executed
    assert wrong_run.security_reason == "CAPABILITY_RUN_MISMATCH"
    assert not docker_observer.network_exists(wrong_run_name)

    capability_name = unique_id("aiscc-network-capability-a")
    requested_name = unique_id("aiscc-network-resource-b")
    docker_observer.register_network(requested_name)
    capability_scope = ResourceScope(
        ResourceDomain.NETWORK,
        f"network:{capability_name}",
        network_name=capability_name,
        target_name=capability_name,
    )
    wrong_resource = docker.create_internal_network(
        capability_factory(scope=capability_scope, current=current),
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=current,
        profile_version="p1-3-v2",
        name=requested_name,
        resource_id=f"network:{requested_name}",
    )
    assert not wrong_resource.executed
    assert wrong_resource.security_reason == "CAPABILITY_RESOURCE_SCOPE_MISMATCH"
    assert not docker_observer.network_exists(requested_name)

    network_name = unique_id("aiscc-internal")
    docker_observer.register_network(network_name)
    network_resource = f"network:{network_name}"
    server_name = unique_id("aiscc-fixture")
    docker_observer.register(server_name)
    client_names: list[str] = []
    network = InternalNetwork(docker, network_name, network_resource)
    network_scope = ResourceScope(
        ResourceDomain.NETWORK,
        network_resource,
        network_name=network_name,
        target_name=network_name,
    )
    assert (
        network.create(
            capability_factory(scope=network_scope, current=current),
            principal="owner-user-1",
            current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            current=current,
            profile_version="p1-3-v2",
        ).exit_code
        == 0
    )
    server_spec = DockerRunSpec(
        name=server_name,
        run_id=run_id,
        resource_id="process:owner-network-fixture",
        image=BASE_IMAGE,
        command=("python", "/workspace/fixture_server.py"),
        workspace=FIXTURES / "network",
        network=network_name,
        aliases=("fixture",),
        detach=True,
    )
    assert (
        docker.run(
            capability_factory(scope=server_spec.scope(), current=current),
            principal="owner-user-1",
            current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            current=current,
            profile_version="p1-3-v2",
            spec=server_spec,
        ).exit_code
        == 0
    )
    try:
        allowed: DockerCommandResult | None = None
        for _ in range(20):
            client_name = unique_id("aiscc-client")
            client_names.append(client_name)
            docker_observer.register(client_name)
            spec = DockerRunSpec(
                name=client_name,
                run_id=run_id,
                resource_id="process:owner-network-client",
                image=BASE_IMAGE,
                command=(
                    "python",
                    "-c",
                    "import urllib.request;print(urllib.request.urlopen('http://fixture:8080',timeout=1).read().decode())",
                ),
                network=network_name,
            )
            allowed = docker.run(
                capability_factory(scope=spec.scope(), current=current),
                principal="owner-user-1",
                current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
                current=current,
                profile_version="p1-3-v2",
                spec=spec,
                timeout_seconds=10,
            )
            if allowed.exit_code == 0:
                break
            time.sleep(0.1)
        assert allowed is not None and allowed.exit_code == 0
        assert allowed.stdout.strip() == "AISCC_INTERNAL_FIXTURE_OK"

        unlisted_name = unique_id("aiscc-unlisted")
        client_names.append(unlisted_name)
        docker_observer.register(unlisted_name)
        unlisted_spec = DockerRunSpec(
            name=unlisted_name,
            run_id=run_id,
            resource_id="process:owner-network-unlisted",
            image=BASE_IMAGE,
            command=(
                "python",
                "-c",
                "import socket;socket.create_connection(('unlisted.invalid',8080),1)",
            ),
            network=network_name,
        )
        unlisted = docker.run(
            capability_factory(scope=unlisted_spec.scope(), current=current),
            principal="owner-user-1",
            current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            current=current,
            profile_version="p1-3-v2",
            spec=unlisted_spec,
        )
        assert unlisted.exit_code != 0

        none_name = unique_id("aiscc-none")
        client_names.append(none_name)
        docker_observer.register(none_name)
        none_spec = DockerRunSpec(
            name=none_name,
            run_id=run_id,
            resource_id="process:owner-network-none",
            image=BASE_IMAGE,
            command=(
                "python",
                "-c",
                "import socket;socket.create_connection(('fixture',8080),1)",
            ),
        )
        default_deny = docker.run(
            capability_factory(scope=none_spec.scope(), current=current),
            principal="owner-user-1",
            current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            current=current,
            profile_version="p1-3-v2",
            spec=none_spec,
        )
        assert default_deny.exit_code != 0
    finally:
        for name in client_names + [server_name]:
            if docker_observer.exists(name):
                cleanup_scope = ResourceScope(
                    ResourceDomain.PROCESS, f"container:{name}", target_name=name
                )
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
        network_cleanup_scope = ResourceScope(
            ResourceDomain.NETWORK,
            f"network:{network_name}",
            network_name=network_name,
            target_name=network_name,
        )
        assert (
            network.remove(
                capability_factory(
                    scope=network_cleanup_scope,
                    current=current,
                    action=SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
                ),
                principal="owner-user-1",
                current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
                current=current,
                profile_version="p1-3-v2",
            ).exit_code
            == 0
        )
        assert not docker_observer.network_exists(network_name)
