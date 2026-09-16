import json

import pytest

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.runtime.docker import DockerRunSpec


@pytest.mark.runtime
def test_actual_container_excludes_hosted_secrets(
    docker, capability_factory, unique_id, monkeypatch
):
    monkeypatch.setenv("AISCC_OPENAI_API_KEY", "SYNTHETIC_CONTAINER_SENTINEL_A")
    monkeypatch.setenv("OPENAI_API_KEY", "SYNTHETIC_CONTAINER_SENTINEL_B")
    name = unique_id("aiscc-l5-secret")
    current = WorkflowSnapshot(unique_id("run-secret"), WorkflowState.RUNNING, 1)
    spec = DockerRunSpec(
        name=name,
        run_id=current.run_id,
        resource_id="process:owner-secret-proof",
        image="python:3.12.14-slim-bookworm@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579",
        command=(
            "python",
            "-B",
            "-c",
            "import os,json; print(json.dumps({k:k in os.environ for k in "
            "['AISCC_OPENAI_API_KEY','OPENAI_API_KEY']}))",
        ),
    )
    try:
        result = docker.run(
            capability_factory(scope=spec.scope(), current=current),
            principal="owner-user-1",
            current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            current=current,
            profile_version="p1-3-v2",
            spec=spec,
        )
        assert result.exit_code == 0, result.stderr
        assert json.loads(result.stdout) == {"AISCC_OPENAI_API_KEY": False, "OPENAI_API_KEY": False}
        assert "SYNTHETIC_CONTAINER_SENTINEL" not in result.stdout + result.stderr
    finally:
        scope = ResourceScope(ResourceDomain.PROCESS, f"container:{name}", target_name=name)
        cleanup = docker.cleanup_container(
            capability_factory(
                scope=scope,
                current=current,
                action=SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
            ),
            principal="owner-user-1",
            current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            current=current,
            profile_version="p1-3-v2",
            name=name,
        )
        assert cleanup.exit_code == 0
