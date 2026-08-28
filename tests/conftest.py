from __future__ import annotations

import subprocess
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

import pytest

from aiscc.contracts.security import (
    AuthorityStatus,
    PermissionRequest,
    ResourceDomain,
    ResourceScope,
    SecurityActionClass,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.runtime.docker import DockerRuntime
from aiscc.security.capability import Capability
from aiscc.security.policy import SecurityPolicy, default_profiles

BASE_IMAGE = (
    "python:3.12.14-slim-bookworm@"
    "sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579"
)
FIXTURES = Path(__file__).parent / "fixtures"


class DockerEvidenceObserver:
    """Test-only observer for exact resources created by the runtime evidence suite."""

    def __init__(self, executable: str = "docker") -> None:
        self._executable = executable
        self._registered_names: set[str] = set()
        self._registered_network_names: set[str] = set()

    def register(self, name: str) -> None:
        if not name or name.startswith("-"):
            raise ValueError("observer resource name must be exact")
        self._registered_names.add(name)

    def register_network(self, name: str) -> None:
        if not name or name.startswith("-"):
            raise ValueError("observer network name must be exact")
        self._registered_network_names.add(name)

    def inspect_hardening(self, name: str) -> subprocess.CompletedProcess[str]:
        self._require_registered(name)
        return self._command(("inspect", name))

    def inspect_command_environment(self, name: str) -> subprocess.CompletedProcess[str]:
        self._require_registered(name)
        return self._command(
            ("inspect", "--format", "{{json .Config.Env}} {{json .Config.Cmd}}", name)
        )

    def wait(self, name: str, *, timeout_seconds: float) -> subprocess.CompletedProcess[str]:
        self._require_registered(name)
        return self._command(("wait", name), timeout_seconds=timeout_seconds)

    def exists(self, name: str) -> bool:
        self._require_registered(name)
        return self._command(("inspect", name)).returncode == 0

    def network_exists(self, name: str) -> bool:
        if name not in self._registered_network_names:
            raise ValueError("observer may inspect only an exact test-owned network")
        return self._command(("network", "inspect", name)).returncode == 0

    def _require_registered(self, name: str) -> None:
        if name not in self._registered_names:
            raise ValueError("observer may inspect only an exact test-owned resource")

    def _command(
        self, args: tuple[str, ...], *, timeout_seconds: float = 30
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [self._executable, *args],
            capture_output=True,
            text=True,
            shell=False,
            timeout=timeout_seconds,
            check=False,
        )


@pytest.fixture
def policy() -> SecurityPolicy:
    return SecurityPolicy(default_profiles())


@pytest.fixture
def docker(policy: SecurityPolicy) -> DockerRuntime:
    runtime = DockerRuntime(policy)
    assert runtime.info(timeout_seconds=10).stdout.strip() == "linux"
    return runtime


@pytest.fixture
def docker_observer() -> DockerEvidenceObserver:
    return DockerEvidenceObserver()


@pytest.fixture
def unique_id() -> Callable[[str], str]:
    return lambda prefix: f"{prefix}-{uuid4().hex[:12]}"


@pytest.fixture
def snapshot() -> WorkflowSnapshot:
    return WorkflowSnapshot("run-p1-3", WorkflowState.RUNNING, 7)


@pytest.fixture
def request_factory(
    policy: SecurityPolicy, snapshot: WorkflowSnapshot
) -> Callable[..., PermissionRequest]:
    def create(**overrides: object) -> PermissionRequest:
        mode = overrides.pop("mode", RuntimeMode.PUBLIC_BOUNDED_LIVE)
        action = overrides.pop("action", SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT)
        profile_version = overrides.pop("profile_version", "p1-3-v2")
        scenario_id = overrides.pop("scenario_id", "p1-3-fixed-synthetic")
        principal = overrides.pop("principal", "public-user-1")
        run_id = overrides.pop("run_id", snapshot.run_id)
        authoritative = overrides.pop("authoritative", snapshot)
        observed = overrides.pop("observed", snapshot)
        resource_scope = overrides.pop("resource_scope", None)
        assert isinstance(mode, RuntimeMode)
        assert isinstance(action, (SecurityActionClass, str))
        assert isinstance(profile_version, str)
        assert isinstance(principal, str)
        assert isinstance(run_id, str)
        assert isinstance(authoritative, WorkflowSnapshot)
        assert isinstance(observed, WorkflowSnapshot)
        if resource_scope is None:
            domain = overrides.pop("resource_domain", ResourceDomain.PROCESS)
            resource_id = overrides.pop("resource_id", "process:p1-3-synthetic-probe")
            assert isinstance(domain, ResourceDomain)
            resource_scope = (
                ResourceScope(
                    ResourceDomain.PROCESS,
                    "process:p1-3-synthetic-probe",
                    argv=("python", "-c", "print('AISCC_PUBLIC_LIVE_SYNTHETIC_OK')"),
                )
                if mode is RuntimeMode.PUBLIC_BOUNDED_LIVE
                and domain is ResourceDomain.PROCESS
                and resource_id == "process:p1-3-synthetic-probe"
                else ResourceScope(domain, str(resource_id))
            )
        assert isinstance(resource_scope, ResourceScope)
        grant_override = overrides.pop("resource_grant", "ISSUE")
        grant = (
            policy.issue_resource_grant(
                mode=mode,
                profile_version=profile_version,
                scenario_id=scenario_id if isinstance(scenario_id, str) else None,
                principal=principal,
                run_id=run_id,
                action=action,
                scope=resource_scope,
            )
            if grant_override == "ISSUE" and isinstance(action, SecurityActionClass)
            else grant_override
        )
        values: dict[str, object] = {
            "principal": principal,
            "run_id": run_id,
            "mode": mode,
            "observed": observed,
            "authoritative": authoritative,
            "action": action,
            "resource_scope": resource_scope,
            "resource_grant": grant,
            "profile_version": profile_version,
            "scenario_id": scenario_id,
            "requester_authority": AuthorityStatus.GRANTED,
            "task_scope_authority": AuthorityStatus.GRANTED,
            "limit_authority": AuthorityStatus.GRANTED,
            "budget_authority": AuthorityStatus.GRANTED,
            "idempotency_authority": AuthorityStatus.GRANTED,
            "target_control_authority": AuthorityStatus.NOT_APPLICABLE,
        }
        values.update(overrides)
        return PermissionRequest(**values)  # type: ignore[arg-type]

    return create


@pytest.fixture
def capability_factory(
    policy: SecurityPolicy, snapshot: WorkflowSnapshot
) -> Callable[..., Capability]:
    def create(
        *,
        scope: ResourceScope,
        current: WorkflowSnapshot | None = None,
        action: SecurityActionClass = SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        mode: RuntimeMode = RuntimeMode.OWNER_SELF_DOGFOOD,
        principal: str = "owner-user-1",
        profile_version: str = "p1-3-v2",
        scenario_id: str | None = None,
        max_uses: int = 1,
    ) -> Capability:
        authoritative = current or snapshot
        grant = policy.issue_resource_grant(
            mode=mode,
            profile_version=profile_version,
            scenario_id=scenario_id,
            principal=principal,
            run_id=authoritative.run_id,
            action=action,
            scope=scope,
        )
        assert grant is not None
        request = PermissionRequest(
            principal=principal,
            run_id=authoritative.run_id,
            mode=mode,
            observed=authoritative,
            authoritative=authoritative,
            action=action,
            resource_scope=scope,
            resource_grant=grant,
            profile_version=profile_version,
            scenario_id=scenario_id,
            requester_authority=AuthorityStatus.GRANTED,
            task_scope_authority=AuthorityStatus.GRANTED,
            limit_authority=AuthorityStatus.GRANTED,
            budget_authority=AuthorityStatus.GRANTED,
            idempotency_authority=AuthorityStatus.GRANTED,
            target_control_authority=(
                AuthorityStatus.GRANTED
                if action
                in {
                    SecurityActionClass.PUBLIC_CANCEL_CONTROL,
                    SecurityActionClass.ADMINISTRATIVE_TERMINATE_CONTROL,
                    SecurityActionClass.SAFETY_CLEANUP_REVOKE_QUARANTINE,
                }
                else AuthorityStatus.NOT_APPLICABLE
            ),
        )
        decision = policy.evaluate(request)
        capability = policy.issue_capability(decision, request, ttl_seconds=15, max_uses=max_uses)
        assert capability is not None
        return capability

    return create


@pytest.fixture
def future_time() -> datetime:
    return datetime.now(UTC) + timedelta(minutes=5)
