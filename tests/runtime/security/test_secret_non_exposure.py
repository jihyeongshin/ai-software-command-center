from __future__ import annotations

import json
import secrets
from collections.abc import Callable

import pytest
from conftest import DockerEvidenceObserver

from aiscc.contracts.security import (
    ResourceDomain,
    ResourceScope,
    SecurityActionClass,
    SecurityAdmissionDecision,
    SecurityDecision,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.runtime.docker import DockerRunSpec, DockerRuntime
from aiscc.security.capability import Capability
from aiscc.security.provenance import decision_artifact

BASE_IMAGE = (
    "python:3.12.14-slim-bookworm@"
    "sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579"
)


@pytest.mark.runtime
def test_synthetic_canary_never_enters_broker_container_or_artifacts(
    docker: DockerRuntime,
    docker_observer: DockerEvidenceObserver,
    unique_id: Callable[[str], str],
    capability_factory: Callable[..., Capability],
) -> None:
    canary = f"sk-AISCC-{secrets.token_hex(16)}"
    run_id = unique_id("run-secret")
    current = WorkflowSnapshot(run_id, WorkflowState.RUNNING, 1)
    name = unique_id("aiscc-secret")
    docker_observer.register(name)
    spec = DockerRunSpec(
        name=name,
        run_id=run_id,
        resource_id="process:owner-secret-proof",
        image=BASE_IMAGE,
        command=(
            "python",
            "-c",
            "import json,os,sys;print(json.dumps({'argv':sys.argv,'env':dict(os.environ)}))",
        ),
    )
    capability = capability_factory(scope=spec.scope(), current=current)
    result = docker.run(
        capability,
        principal="owner-user-1",
        current_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        current=current,
        profile_version="p1-3-v2",
        spec=spec,
    )
    try:
        assert result.exit_code == 0, result.stderr
        inspect = docker_observer.inspect_command_environment(name)
        public_replay_artifact = json.dumps({"run": run_id, "output": result.stdout})
        decision = SecurityDecision.create(
            SecurityAdmissionDecision.DENY,
            "SYNTHETIC_SECRET_DENIED",
            (("SG_SECRET_NON_EXPOSURE", True),),
            {"message": f"value={canary}"},
        )
        provenance = decision_artifact(decision, sensitive_values=(canary,)).body
        runtime_provenance = json.dumps(dict(result.security_provenance), sort_keys=True)
        exported = "\n".join(
            (
                result.stdout,
                result.stderr,
                inspect.stdout,
                public_replay_artifact,
                provenance,
                runtime_provenance,
            )
        )
        assert canary not in exported
        assert "[REDACTED]" in provenance
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
