from __future__ import annotations

import subprocess
import time
from collections.abc import Mapping, Sequence
from threading import Event

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot
from aiscc.runtime.contracts import RuntimeOutcome, RuntimeOutcomeStatus
from aiscc.security.capability import Capability
from aiscc.security.policy import SecurityPolicy


class BoundedProcessRunner:
    def __init__(self, policy: SecurityPolicy) -> None:
        self._policy = policy

    def run(
        self,
        capability: Capability | None,
        *,
        principal: str,
        current_mode: RuntimeMode,
        current: WorkflowSnapshot,
        profile_version: str,
        resource_id: str,
        argv: Sequence[str],
        timeout_seconds: float,
        max_attempts: int,
        cancel: Event | None = None,
    ) -> RuntimeOutcome:
        if not argv or timeout_seconds <= 0 or max_attempts <= 0:
            return RuntimeOutcome(
                RuntimeOutcomeStatus.FAILED,
                None,
                0,
                "",
                "invalid finite limits",
                True,
                False,
                "INVALID_RUNTIME_LIMITS",
                {},
            )
        scope = ResourceScope(
            domain=ResourceDomain.PROCESS,
            resource_id=resource_id,
            argv=tuple(argv),
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
            return RuntimeOutcome(
                RuntimeOutcomeStatus.FAILED,
                None,
                0,
                "",
                use.reason,
                True,
                False,
                use.reason,
                use.provenance,
            )
        return self._run_unchecked(
            argv,
            timeout_seconds=timeout_seconds,
            max_attempts=max_attempts,
            cancel=cancel,
            security_reason=use.reason,
            security_provenance=use.provenance,
        )

    @staticmethod
    def _run_unchecked(
        argv: Sequence[str],
        *,
        timeout_seconds: float,
        max_attempts: int,
        cancel: Event | None,
        security_reason: str,
        security_provenance: Mapping[str, str],
    ) -> RuntimeOutcome:
        provenance = dict(security_provenance)
        last_stdout = ""
        last_stderr = ""
        for attempt in range(1, max_attempts + 1):
            process = subprocess.Popen(
                list(argv),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=False,
            )
            deadline = time.monotonic() + timeout_seconds
            while process.poll() is None:
                if cancel is not None and cancel.is_set():
                    process.terminate()
                    stdout, stderr = process.communicate(timeout=5)
                    return RuntimeOutcome(
                        RuntimeOutcomeStatus.CANCELLED,
                        process.returncode,
                        attempt,
                        stdout,
                        stderr,
                        True,
                        True,
                        security_reason,
                        provenance,
                    )
                if time.monotonic() >= deadline:
                    process.kill()
                    stdout, stderr = process.communicate(timeout=5)
                    return RuntimeOutcome(
                        RuntimeOutcomeStatus.TIMEOUT,
                        process.returncode,
                        attempt,
                        stdout,
                        stderr,
                        True,
                        True,
                        security_reason,
                        provenance,
                    )
                time.sleep(0.01)
            last_stdout, last_stderr = process.communicate()
            if process.returncode == 0:
                return RuntimeOutcome(
                    RuntimeOutcomeStatus.SUCCESS,
                    0,
                    attempt,
                    last_stdout,
                    last_stderr,
                    True,
                    True,
                    security_reason,
                    provenance,
                )
        return RuntimeOutcome(
            RuntimeOutcomeStatus.FAILED,
            process.returncode,
            max_attempts,
            last_stdout,
            last_stderr,
            True,
            True,
            security_reason,
            provenance,
        )
