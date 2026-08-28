from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot
from aiscc.runtime.contracts import ResourceRecord
from aiscc.runtime.docker import DockerRuntime
from aiscc.security.capability import Capability


@dataclass(frozen=True, slots=True)
class CleanupResult:
    clean: bool
    quarantined: bool
    residue: tuple[ResourceRecord, ...]


def cleanup_containers(
    docker: DockerRuntime,
    resources: tuple[ResourceRecord, ...],
    capabilities: Mapping[str, Capability | None],
    *,
    principal: str,
    current_mode: RuntimeMode,
    current: WorkflowSnapshot,
    profile_version: str,
) -> CleanupResult:
    residue: list[ResourceRecord] = []
    for resource in resources:
        capability = capabilities.get(resource.resource_id)
        result = (
            docker.cleanup_container(
                capability,
                principal=principal,
                current_mode=current_mode,
                current=current,
                profile_version=profile_version,
                name=resource.resource_id,
            )
            if resource.resource_type == "container" and resource.run_id == current.run_id
            else None
        )
        if result is None or result.exit_code != 0:
            residue.append(resource)
    return CleanupResult(not residue, bool(residue), tuple(residue))
