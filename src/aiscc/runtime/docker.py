from __future__ import annotations

import subprocess
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot
from aiscc.security.capability import Capability
from aiscc.security.policy import SecurityPolicy


@dataclass(frozen=True, slots=True)
class DockerCommandResult:
    exit_code: int | None
    stdout: str
    stderr: str
    executed: bool
    security_reason: str
    security_provenance: Mapping[str, str]


@dataclass(frozen=True, slots=True)
class DockerRunSpec:
    name: str
    run_id: str
    resource_id: str
    image: str
    command: tuple[str, ...]
    workspace: Path | None = None
    network: str = "none"
    aliases: tuple[str, ...] = ()
    detach: bool = False

    def scope(self) -> ResourceScope:
        workspace_path = (
            str(self.workspace.resolve(strict=True)) if self.workspace is not None else None
        )
        return ResourceScope(
            domain=ResourceDomain.PROCESS,
            resource_id=self.resource_id,
            image=self.image,
            argv=self.command,
            workspace_path=workspace_path,
            network_name=self.network,
            network_aliases=self.aliases,
            target_name=self.name,
            detach=self.detach,
        )


class DockerRuntime:
    def __init__(self, policy: SecurityPolicy, executable: str = "docker") -> None:
        self._policy = policy
        self._executable = executable

    def info(self, *, timeout_seconds: float = 30) -> DockerCommandResult:
        return self._read_only_command(
            ["info", "--format", "{{.OSType}}"], timeout_seconds=timeout_seconds
        )

    def run(
        self,
        capability: Capability | None,
        *,
        principal: str,
        current_mode: RuntimeMode,
        current: WorkflowSnapshot,
        profile_version: str,
        spec: DockerRunSpec,
        timeout_seconds: float = 30,
    ) -> DockerCommandResult:
        if spec.run_id != current.run_id:
            return self._denied("DOCKER_RUN_ID_MISMATCH")
        scope = spec.scope()
        use = self._policy.consume_capability(
            capability,
            principal=principal,
            current_mode=current_mode,
            current=current,
            profile_version=profile_version,
            action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            scope=scope,
        )
        if not use.allowed:
            return self._denied(use.reason, use.provenance)
        return self._command(
            self._secure_run_args(spec),
            timeout_seconds=timeout_seconds,
            security_reason=use.reason,
            security_provenance=use.provenance,
        )

    def create_internal_network(
        self,
        capability: Capability | None,
        *,
        principal: str,
        current_mode: RuntimeMode,
        current: WorkflowSnapshot,
        profile_version: str,
        name: str,
        resource_id: str,
    ) -> DockerCommandResult:
        scope = ResourceScope(
            domain=ResourceDomain.NETWORK,
            resource_id=resource_id,
            network_name=name,
            target_name=name,
        )
        use = self._policy.consume_capability(
            capability,
            principal=principal,
            current_mode=current_mode,
            current=current,
            profile_version=profile_version,
            action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            scope=scope,
        )
        if not use.allowed:
            return self._denied(use.reason, use.provenance)
        return self._command(
            [
                "network",
                "create",
                "--internal",
                "--label",
                f"aiscc.run_id={current.run_id}",
                "--label",
                "aiscc.owner=p1-3",
                name,
            ],
            security_reason=use.reason,
            security_provenance=use.provenance,
        )

    def cleanup_container(
        self,
        capability: Capability | None,
        *,
        principal: str,
        current_mode: RuntimeMode,
        current: WorkflowSnapshot,
        profile_version: str,
        name: str,
    ) -> DockerCommandResult:
        scope = ResourceScope(
            domain=ResourceDomain.PROCESS,
            resource_id=f"container:{name}",
            target_name=name,
        )
        use = self._policy.consume_capability(
            capability,
            principal=principal,
            current_mode=current_mode,
            current=current,
            profile_version=profile_version,
            action=SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
            scope=scope,
        )
        if not use.allowed:
            return self._denied(use.reason, use.provenance)
        ownership = self._inspect_container_run_owner(name)
        if ownership.exit_code != 0 or ownership.stdout.strip() != current.run_id:
            return self._denied("RESOURCE_OWNERSHIP_MISMATCH", use.provenance)
        return self._command(
            ["rm", "--force", name],
            security_reason=use.reason,
            security_provenance=use.provenance,
        )

    def cleanup_network(
        self,
        capability: Capability | None,
        *,
        principal: str,
        current_mode: RuntimeMode,
        current: WorkflowSnapshot,
        profile_version: str,
        name: str,
    ) -> DockerCommandResult:
        scope = ResourceScope(
            domain=ResourceDomain.NETWORK,
            resource_id=f"network:{name}",
            network_name=name,
            target_name=name,
        )
        use = self._policy.consume_capability(
            capability,
            principal=principal,
            current_mode=current_mode,
            current=current,
            profile_version=profile_version,
            action=SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
            scope=scope,
        )
        if not use.allowed:
            return self._denied(use.reason, use.provenance)
        ownership = self._inspect_network_run_owner(name)
        if ownership.exit_code != 0 or ownership.stdout.strip() != current.run_id:
            return self._denied("RESOURCE_OWNERSHIP_MISMATCH", use.provenance)
        return self._command(
            ["network", "rm", name],
            security_reason=use.reason,
            security_provenance=use.provenance,
        )

    def read_container_metadata(
        self,
        capability: Capability | None,
        *,
        principal: str,
        current_mode: RuntimeMode,
        current: WorkflowSnapshot,
        profile_version: str,
        name: str,
    ) -> DockerCommandResult:
        scope = ResourceScope(
            domain=ResourceDomain.PROCESS,
            resource_id=f"container:{name}",
            target_name=name,
        )
        use = self._policy.consume_capability(
            capability,
            principal=principal,
            current_mode=current_mode,
            current=current,
            profile_version=profile_version,
            action=SecurityActionClass.RUN_REVIEW_READ_ONLY,
            scope=scope,
        )
        if not use.allowed:
            return self._denied(use.reason, use.provenance)
        ownership = self._inspect_container_run_owner(name)
        if ownership.exit_code != 0 or ownership.stdout.strip() != current.run_id:
            return self._denied("RESOURCE_OWNERSHIP_MISMATCH", use.provenance)
        return self._command(
            ["inspect", "--format", "{{json .State.Status}}", name],
            security_reason=use.reason,
            security_provenance=use.provenance,
        )

    def _inspect_container_run_owner(self, name: str) -> DockerCommandResult:
        return self._read_only_command(
            ["inspect", "--format", '{{index .Config.Labels "aiscc.run_id"}}', name]
        )

    def _inspect_network_run_owner(self, name: str) -> DockerCommandResult:
        return self._read_only_command(
            ["network", "inspect", "--format", '{{index .Labels "aiscc.run_id"}}', name]
        )

    def _secure_run_args(self, spec: DockerRunSpec) -> list[str]:
        args = [
            "run",
            "--name",
            spec.name,
            "--label",
            f"aiscc.run_id={spec.run_id}",
            "--label",
            "aiscc.owner=p1-3",
            "--read-only",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,size=16m",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges",
            "--user",
            "65532:65532",
            "--pids-limit",
            "64",
            "--memory",
            "128m",
            "--cpus",
            "0.50",
            "--network",
            spec.network,
        ]
        for alias in spec.aliases:
            args.extend(("--network-alias", alias))
        if spec.workspace is not None:
            resolved = spec.workspace.resolve(strict=True)
            args.extend(("--mount", f"type=bind,src={resolved},dst=/workspace,readonly"))
        if spec.detach:
            args.append("--detach")
        args.extend((spec.image, *spec.command))
        return args

    def _read_only_command(
        self, args: Sequence[str], *, timeout_seconds: float = 30
    ) -> DockerCommandResult:
        return self._command(
            args,
            timeout_seconds=timeout_seconds,
            security_reason="READ_ONLY_DOCKER_QUERY",
            security_provenance={},
        )

    def _command(
        self,
        args: Sequence[str],
        *,
        timeout_seconds: float = 30,
        security_reason: str,
        security_provenance: Mapping[str, str],
    ) -> DockerCommandResult:
        completed = subprocess.run(
            [self._executable, *args],
            capture_output=True,
            text=True,
            shell=False,
            timeout=timeout_seconds,
            check=False,
        )
        return DockerCommandResult(
            completed.returncode,
            completed.stdout,
            completed.stderr,
            True,
            security_reason,
            dict(security_provenance),
        )

    @staticmethod
    def _denied(reason: str, provenance: Mapping[str, str] | None = None) -> DockerCommandResult:
        return DockerCommandResult(None, "", reason, False, reason, dict(provenance or {}))
