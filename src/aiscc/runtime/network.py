from __future__ import annotations

from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot
from aiscc.runtime.docker import DockerCommandResult, DockerRuntime
from aiscc.security.capability import Capability


class InternalNetwork:
    def __init__(self, docker: DockerRuntime, name: str, resource_id: str) -> None:
        self._docker = docker
        self.name = name
        self.resource_id = resource_id

    def create(
        self,
        capability: Capability | None,
        *,
        principal: str,
        current_mode: RuntimeMode,
        current: WorkflowSnapshot,
        profile_version: str,
    ) -> DockerCommandResult:
        return self._docker.create_internal_network(
            capability,
            principal=principal,
            current_mode=current_mode,
            current=current,
            profile_version=profile_version,
            name=self.name,
            resource_id=self.resource_id,
        )

    def remove(
        self,
        capability: Capability | None,
        *,
        principal: str,
        current_mode: RuntimeMode,
        current: WorkflowSnapshot,
        profile_version: str,
    ) -> DockerCommandResult:
        return self._docker.cleanup_network(
            capability,
            principal=principal,
            current_mode=current_mode,
            current=current,
            profile_version=profile_version,
            name=self.name,
        )
