from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from threading import Event, Lock, Thread

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot
from aiscc.runtime.stockroom_image import (
    AdmittedStockroomImage,
    require_admitted_image,
    verify_image_inspect,
)
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
    image_provenance: AdmittedStockroomImage | None = None

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
    if spec.image_provenance is not None:
        admitted = require_admitted_image(spec.image_provenance)
        payload["image_provenance"] = admitted.ref.model_dump(mode="json")
        payload["required_labels"] = dict(admitted.provenance.required_labels)
    body = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(body).hexdigest()


def _validate_stockroom_spec(spec: DockerRunSpec) -> None:
    image = _STOCKROOM_IMAGE
    if type(spec) is DockerRunSpec and spec.image_provenance is not None:
        image = require_admitted_image(spec.image_provenance).provenance.image.image_id
    if (
        type(spec) is not DockerRunSpec
        or not spec.name
        or not spec.run_id
        or spec.resource_id != "process:stockroom-summary-v1"
        or spec.image != image
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


@dataclass(frozen=True, slots=True)
class StockroomCancellation:
    """Caller-owned run/attempt signal using the existing runtime Event contract."""

    run_id: str
    attempt_id: str
    event: Event

    def __post_init__(self) -> None:
        if not self.run_id or not self.attempt_id or type(self.event) is not Event:
            raise ValueError("STOCKROOM_CANCELLATION_BINDING_DENIED")


class StockroomDockerRunner:
    """One dispatch, exact ownership, bounded capture and conservative settlement."""

    def __init__(self, executable: Path, image: AdmittedStockroomImage,
                 cancellation: StockroomCancellation) -> None:
        self._image = require_admitted_image(image)
        if not executable.is_absolute() or not executable.is_file():
            raise ValueError("TRUSTED_ABSOLUTE_DOCKER_REQUIRED")
        if type(cancellation) is not StockroomCancellation:
            raise ValueError("STOCKROOM_CANCELLATION_BINDING_DENIED")
        self._executable = str(executable.resolve(strict=True))
        self._cancel = cancellation
        self._lock = Lock()
        self._dispatched = False

    def _process(self, args, timeout, stdout_limit=65536, stderr_limit=65536,
                 observe_cancel=False):
        """Drain both pipes concurrently; never retain unbounded subprocess output."""
        environment = {key: os.environ[key] for key in ("SystemRoot", "WINDIR")
                       if key in os.environ}
        process = subprocess.Popen(
            [self._executable, *args], stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, env=environment,
        )
        buffers = [bytearray(), bytearray()]
        failures = []

        def drain(stream, output, limit):
            try:
                while chunk := stream.read(4096):
                    output.extend(chunk[:max(0, limit + 1 - len(output))])
            except Exception:
                failures.append(True)
            finally:
                stream.close()

        readers = [Thread(target=drain, args=(stream, output, limit), daemon=True)
                   for stream, output, limit in (
                       (process.stdout, buffers[0], stdout_limit),
                       (process.stderr, buffers[1], stderr_limit))]
        for reader in readers:
            reader.start()
        deadline = time.monotonic() + max(0.001, timeout)
        timed_out = cancelled = False
        while process.poll() is None:
            cancelled = observe_cancel and self._cancel.event.is_set()
            timed_out = time.monotonic() >= deadline
            if cancelled or timed_out:
                process.kill()
                break
            time.sleep(0.005)
        try:
            process.wait(timeout=1)
        except subprocess.TimeoutExpired:
            failures.append(True)
        for reader in readers:
            reader.join(timeout=1)
        if failures or any(reader.is_alive() for reader in readers):
            raise ValueError("DOCKER_PIPE_SETTLEMENT_UNCERTAIN")
        return process.returncode, bytes(buffers[0]), bytes(buffers[1]), timed_out, cancelled

    def _query(self, args, deadline):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise ValueError("DOCKER_SETTLEMENT_DEADLINE")
        result = self._process(args, remaining)
        if result[3] or len(result[1]) > 65536 or len(result[2]) > 65536:
            raise ValueError("DOCKER_CONTROL_OUTPUT_UNCERTAIN")
        return result

    def _inspect(self, kind, identity, deadline):
        result = self._query([kind, "inspect", identity], deadline)
        if result[0] != 0:
            raise ValueError("DOCKER_INSPECT_UNCERTAIN")
        raw = json.loads(result[1])
        if type(raw) is not list or len(raw) != 1 or type(raw[0]) is not dict:
            raise ValueError("DOCKER_INSPECT_SHAPE_DENIED")
        return raw[0]

    @staticmethod
    def _owned(raw, identity, spec):
        labels = raw.get("Config", {}).get("Labels", {})
        if (raw.get("Id") != identity or raw.get("Name") != "/" + spec.name
                or labels.get("aiscc.run_id") != spec.run_id
                or labels.get("aiscc.owner") != "p1-3"):
            raise ValueError("DOCKER_CONTAINER_OWNER_UNCERTAIN")
        return raw

    def __call__(self, args: Sequence[str], spec: DockerRunSpec) -> StockroomProcessObservation:
        _validate_stockroom_spec(spec)
        if (spec.image_provenance is not self._image or spec.run_id != self._cancel.run_id
                or spec.name != "aiscc-" + self._cancel.attempt_id):
            raise ValueError("DOCKER_ATTEMPT_BINDING_DENIED")
        with self._lock:
            if self._dispatched:
                raise ValueError("DOCKER_REDISPATCH_DENIED")
            self._dispatched = True
        stdout = stderr = b""
        timed_out = cancelled = terminal = reconciled = captured = False
        exit_code = None
        identity = None
        try:
            operation_deadline = time.monotonic() + spec.operation_timeout_seconds
            raw = self._inspect("image", spec.image, operation_deadline)
            verify_image_inspect(raw, self._image)
            if self._cancel.event.is_set():
                return StockroomProcessObservation(None, b"", b"", cancelled=True)
            # Generate source-owned arguments; caller argv is only a consistency check.
            expected_args = DockerRuntime._secure_run_args(self, spec)
            if list(args) != expected_args:
                raise ValueError("DOCKER_ARGV_DENIED")
            created = self._query(
                ["create", "--pull=never", *expected_args[1:]], operation_deadline
            )
            candidate = created[1].decode("ascii").strip()
            if created[0] != 0 or not re.fullmatch(r"[0-9a-f]{64}", candidate):
                raise ValueError("DOCKER_CREATE_ID_UNCERTAIN")
            identity = candidate
            self._owned(self._inspect("container", identity, operation_deadline), identity, spec)
            if time.monotonic() >= operation_deadline:
                timed_out = True
                raise ValueError("DOCKER_OPERATION_DEADLINE")
            result = self._process(
                ["start", "--attach", identity], operation_deadline - time.monotonic(),
                spec.stdout_limit_bytes, spec.stderr_limit_bytes, True,
            )
            _, stdout, stderr, timed_out, cancelled = result
            captured = result[0] == 0 or timed_out or cancelled
        except Exception:
            # A failed create without an exact ID never authorizes a name-based removal.
            pass
        if identity is not None:
            try:
                deadline = time.monotonic() + spec.cleanup_timeout_seconds
                raw = self._owned(self._inspect("container", identity, deadline), identity, spec)
                state = raw.get("State", {})
                if state.get("Running") is True:
                    self._query(["stop", "--time", "1", identity], deadline)
                    raw = self._owned(
                        self._inspect("container", identity, deadline), identity, spec
                    )
                    if raw.get("State", {}).get("Running") is True:
                        self._query(["kill", identity], deadline)
                while time.monotonic() < deadline:
                    raw = self._owned(
                        self._inspect("container", identity, deadline), identity, spec
                    )
                    state = raw.get("State", {})
                    if (state.get("Running") is False and state.get("Status") in {"exited", "dead"}
                            and type(state.get("ExitCode")) is int):
                        terminal = True
                        exit_code = state["ExitCode"]
                        break
                    time.sleep(0.01)
                if terminal:
                    removed = self._query(["rm", identity], deadline)
                    if removed[0] == 0:
                        # A successful full listing distinguishes absence from
                        # inspect/daemon errors.
                        listing = self._query(["container", "ls", "--all", "--no-trunc",
                                               "--format", "{{.ID}}"], deadline)
                        ids = listing[1].decode("ascii").splitlines()
                        reconciled = (listing[0] == 0 and identity not in ids
                                      and all(re.fullmatch(r"[0-9a-f]{64}", i) for i in ids))
            except Exception:
                pass
        return StockroomProcessObservation(exit_code, stdout, stderr, timed_out, cancelled,
                                           terminal, reconciled and captured)
