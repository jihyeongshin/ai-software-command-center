from __future__ import annotations

import hashlib
import json
import subprocess
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot
from aiscc.security.capability import (
    Capability,
    CapabilityConsumeRequest,
    CapabilityConsumptionReceipt,
)
from aiscc.security.policy import SecurityPolicy

_STOCKROOM_IMAGE = (
    "aiscc-stockroom-runtime@sha256:"
    "be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d"
)


@dataclass(frozen=True, slots=True)
class DockerCommandResult:
    exit_code: int | None
    stdout: str
    stderr: str
    executed: bool
    security_reason: str
    security_provenance: Mapping[str, str]
    tool_outcome: str = "NOT_APPLICABLE"
    quarantine_required: bool = False


@dataclass(frozen=True, slots=True)
class StockroomProcessObservation:
    exit_code: int | None
    stdout: bytes
    stderr: bytes
    timed_out: bool = False
    cancelled: bool = False
    termination_proven: bool = True
    owner_reconciled: bool = True


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
    workdir: str | None = None
    stdout_limit_bytes: int = 65536
    stderr_limit_bytes: int = 65536
    operation_timeout_seconds: int = 30
    cleanup_timeout_seconds: int = 30
    attempt_timeout_seconds: int = 30

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
    def __init__(
        self,
        policy: SecurityPolicy,
        executable: str = "docker",
        *,
        stockroom_runner: Callable[
            [Sequence[str], DockerRunSpec], StockroomProcessObservation
        ]
        | None = None,
    ) -> None:
        self._policy = policy
        self._executable = executable
        self._stockroom_runner = stockroom_runner

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

    def run_consumed_stockroom(
        self,
        receipt: CapabilityConsumptionReceipt,
        requirement: CapabilityConsumeRequest,
        *,
        spec: DockerRunSpec,
        dispatch_identity: str,
    ) -> DockerCommandResult:
        """Enter the fixed Stockroom process path from an authentic consumed receipt."""
        try:
            _validate_stockroom_spec(spec)
        except ValueError as exc:
            return self._denied(str(exc))
        if (
            requirement.current.run_id != spec.run_id
            or requirement.action is not SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT
            or requirement.scope != spec.scope()
            or not self._policy.enter_claimed_dispatch(
                receipt,
                requirement,
                dispatch_identity=dispatch_identity,
            )
        ):
            return self._denied("STOCKROOM_PROCESS_RECEIPT_DENIED")
        if self._stockroom_runner is None:
            return DockerCommandResult(
                None,
                "",
                "STOCKROOM_PROCESS_BOUNDARY_NOT_INJECTED",
                False,
                "AUTHENTIC_CONSUMED_PROCESS_RECEIPT",
                {"receipt_id": receipt.receipt_id},
                "UNKNOWN_TOOL_OUTCOME",
                True,
            )
        try:
            observation = self._stockroom_runner(self._secure_run_args(spec), spec)
        except Exception:
            return DockerCommandResult(
                None,
                "",
                "STOCKROOM_PROCESS_TRANSPORT_UNCERTAIN",
                True,
                "AUTHENTIC_CONSUMED_PROCESS_RECEIPT",
                {"receipt_id": receipt.receipt_id},
                "UNKNOWN_TOOL_OUTCOME",
                True,
            )
        bounded = (
            len(observation.stdout) <= spec.stdout_limit_bytes
            and len(observation.stderr) <= spec.stderr_limit_bytes
        )
        settled = observation.termination_proven and observation.owner_reconciled
        if not settled:
            outcome = "UNKNOWN_TOOL_OUTCOME"
            quarantine = True
        elif (
            observation.timed_out
            or observation.cancelled
            or not bounded
            or observation.exit_code != 0
        ):
            outcome = "KNOWN_TOOL_FAILURE"
            quarantine = False
        else:
            outcome = "KNOWN_TOOL_COMPLETED"
            quarantine = False
        try:
            stdout = observation.stdout[: spec.stdout_limit_bytes].decode(
                "ascii", errors="strict"
            )
            stderr = observation.stderr[: spec.stderr_limit_bytes].decode(
                "ascii", errors="strict"
            )
        except UnicodeDecodeError:
            return DockerCommandResult(
                observation.exit_code,
                "",
                "STOCKROOM_NON_ASCII_OUTPUT",
                True,
                "AUTHENTIC_CONSUMED_PROCESS_RECEIPT",
                {"receipt_id": receipt.receipt_id},
                "KNOWN_TOOL_FAILURE" if settled else "UNKNOWN_TOOL_OUTCOME",
                not settled,
            )
        return DockerCommandResult(
            observation.exit_code,
            stdout,
            stderr,
            True,
            "AUTHENTIC_CONSUMED_PROCESS_RECEIPT",
            {"receipt_id": receipt.receipt_id},
            outcome,
            quarantine,
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
        if spec.workdir is not None:
            args.extend(("--workdir", spec.workdir))
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


def stockroom_spec_fingerprint(spec: DockerRunSpec) -> str:
    _validate_stockroom_spec(spec)
    payload = {
        "name": spec.name,
        "run_id": spec.run_id,
        "resource_id": spec.resource_id,
        "image": spec.image,
        "command": list(spec.command),
        "workspace": str(spec.workspace.resolve(strict=True)) if spec.workspace else None,
        "network": spec.network,
        "aliases": list(spec.aliases),
        "detach": spec.detach,
        "workdir": spec.workdir,
        "stdout_limit_bytes": spec.stdout_limit_bytes,
        "stderr_limit_bytes": spec.stderr_limit_bytes,
        "operation_timeout_seconds": spec.operation_timeout_seconds,
        "cleanup_timeout_seconds": spec.cleanup_timeout_seconds,
        "attempt_timeout_seconds": spec.attempt_timeout_seconds,
    }
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(body).hexdigest()


def _validate_stockroom_spec(spec: DockerRunSpec) -> None:
    if (
        type(spec) is not DockerRunSpec
        or not spec.name
        or not spec.run_id
        or spec.resource_id != "process:stockroom-summary-v1"
        or spec.image != _STOCKROOM_IMAGE
        or spec.command != ("python", "-B", "-m", "stockroom", "summary")
        or spec.workspace is None
        or not spec.workspace.is_absolute()
        or not spec.workspace.is_dir()
        or spec.network != "none"
        or spec.aliases
        or spec.detach
        or spec.workdir != "/workspace"
        or spec.stdout_limit_bytes != 4096
        or spec.stderr_limit_bytes != 4096
        or spec.operation_timeout_seconds != 5
        or spec.cleanup_timeout_seconds != 10
        or spec.attempt_timeout_seconds != 30
    ):
        raise ValueError("STOCKROOM_DOCKER_SPEC_DENIED")
