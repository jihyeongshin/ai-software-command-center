from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

import pytest
from conftest import DockerEvidenceObserver

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.runtime.docker import DockerRunSpec, DockerRuntime
from aiscc.security.capability import Capability

BASE_IMAGE = (
    "python:3.12.14-slim-bookworm@"
    "sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579"
)
FIXTURES = Path(__file__).parents[2] / "fixtures"


@pytest.mark.runtime
def test_read_only_workspace_host_isolation_and_cleanup_through_broker(
    docker: DockerRuntime,
    docker_observer: DockerEvidenceObserver,
    unique_id: Callable[[str], str],
    capability_factory: Callable[..., Capability],
) -> None:
    run_id = unique_id("run-isolation")
    current = WorkflowSnapshot(run_id, WorkflowState.RUNNING, 1)
    name = unique_id("aiscc-isolation")
    docker_observer.register(name)
    command = (
        "import json,os,pathlib;"
        "p=pathlib.Path('/workspace/input.txt');"
        "print(json.dumps({'uid':os.getuid(),'gid':os.getgid(),"
        "'input':p.read_text().strip(),'workspace_writable':os.access('/workspace',os.W_OK),"
        "'host_git_visible':pathlib.Path('/workspace/../.git').exists(),"
        "'host_root_visible':pathlib.Path('/host').exists()}))"
    )
    spec = DockerRunSpec(
        name=name,
        run_id=run_id,
        resource_id="process:owner-isolation-proof",
        image=BASE_IMAGE,
        command=("python", "-c", command),
        workspace=FIXTURES / "sandbox" / "allowed",
    )
    capability = capability_factory(scope=spec.scope(), current=current)
    other_run_id = unique_id("run-isolation-other")
    other_current = WorkflowSnapshot(other_run_id, WorkflowState.RUNNING, 1)
    other_name = unique_id("aiscc-isolation-other")
    docker_observer.register(other_name)
    other_spec = DockerRunSpec(
        name=other_name,
        run_id=other_run_id,
        resource_id="process:owner-cross-run-read-target",
        image=BASE_IMAGE,
        command=("python", "-c", "print('cross-run-target')"),
    )
    result = docker.run(
        capability,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=current,
        profile_version="p1-3-v2",
        spec=spec,
        timeout_seconds=20,
    )
    try:
        assert result.exit_code == 0, result.stderr
        assert result.executed and result.security_reason == "CAPABILITY_CONSUMED"
        payload = json.loads(result.stdout)
        assert payload == {
            "uid": 65532,
            "gid": 65532,
            "input": "AISCC_P1_3_ALLOWED_INPUT",
            "workspace_writable": False,
            "host_git_visible": False,
            "host_root_visible": False,
        }
        inspect = docker_observer.inspect_hardening(name)
        assert inspect.returncode == 0
        metadata = json.loads(inspect.stdout)[0]
        config = metadata["Config"]
        host_config = metadata["HostConfig"]
        assert config["Labels"]["aiscc.run_id"] == run_id
        assert config["Labels"]["aiscc.owner"] == "p1-3"
        assert config["User"] == "65532:65532"
        assert host_config["ReadonlyRootfs"] is True
        assert "ALL" in host_config["CapDrop"]
        assert any(option.startswith("no-new-privileges") for option in host_config["SecurityOpt"])
        assert host_config["PidsLimit"] == 64
        assert host_config["Memory"] == 134217728
        assert host_config["NanoCpus"] == 500000000
        assert host_config["NetworkMode"] == "none"

        tmpfs_options = set(host_config["Tmpfs"]["/tmp"].split(","))
        assert {"rw", "noexec", "nosuid"} <= tmpfs_options
        assert tmpfs_options & {"size=16m", "size=16777216"}

        mounts = metadata["Mounts"]
        assert len(mounts) == 1
        workspace_mount = mounts[0]
        assert workspace_mount["Type"] == "bind"
        assert workspace_mount["Destination"] == "/workspace"
        assert workspace_mount["RW"] is False
        expected_source = str((FIXTURES / "sandbox" / "allowed").resolve()).replace("\\", "/")
        observed_source = str(workspace_mount["Source"]).replace("\\", "/")
        assert (
            observed_source.casefold() == expected_source.casefold()
            or observed_source.casefold().endswith(expected_source[2:].casefold())
        )
        forbidden_mount_fragments = ("/.git", "/.ssh", "/docker.sock", "/workspace-sibling")
        assert not any(
            fragment in observed_source.casefold() for fragment in forbidden_mount_fragments
        )

        other_result = docker.run(
            capability_factory(scope=other_spec.scope(), current=other_current),
            principal="owner-user-1",
            current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            current=other_current,
            profile_version="p1-3-v2",
            spec=other_spec,
        )
        assert other_result.exit_code == 0
        assert docker_observer.exists(other_name)
        other_owner = json.loads(docker_observer.inspect_hardening(other_name).stdout)[0]
        assert other_owner["Config"]["Labels"]["aiscc.run_id"] == other_run_id

        cross_run_scope = ResourceScope(
            ResourceDomain.PROCESS,
            f"container:{other_name}",
            target_name=other_name,
        )
        cross_run_read = docker.read_container_metadata(
            capability_factory(
                scope=cross_run_scope,
                current=current,
                action=SecurityActionClass.RUN_REVIEW_READ_ONLY,
            ),
            principal="owner-user-1",
            current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            current=current,
            profile_version="p1-3-v2",
            name=other_name,
        )
        assert not cross_run_read.executed
        assert cross_run_read.stdout == ""
        assert cross_run_read.security_reason == "RESOURCE_OWNERSHIP_MISMATCH"
    finally:
        if docker_observer.exists(other_name):
            other_cleanup_scope = ResourceScope(
                ResourceDomain.PROCESS,
                f"container:{other_name}",
                target_name=other_name,
            )
            assert (
                docker.cleanup_container(
                    capability_factory(
                        scope=other_cleanup_scope,
                        current=other_current,
                        action=SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
                    ),
                    principal="owner-user-1",
                    current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
                    current=other_current,
                    profile_version="p1-3-v2",
                    name=other_name,
                ).exit_code
                == 0
            )
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
    assert not docker_observer.exists(name)
