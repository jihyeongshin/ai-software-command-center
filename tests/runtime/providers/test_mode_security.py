from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.providers.models import (
    ExecutionAttemptRef,
    ExecutionStatus,
    ProviderCall,
    ProviderResult,
    SecretResolutionLease,
    canonical_sha256,
)
from aiscc.providers.profiles import load_provider_profile
from aiscc.providers.service import AgentExecutionService
from aiscc.security.policy import SecurityPolicy, default_profiles


class Observer:
    calls = 0
    resolves = 0

    def call(self, call: ProviderCall, *, secret: str) -> ProviderResult:
        del call, secret
        self.calls += 1
        raise AssertionError("side effect reached")

    def resolve(self, lease: SecretResolutionLease) -> str:
        del lease
        self.resolves += 1
        raise AssertionError("secret reached")

    def close(self, lease: SecretResolutionLease) -> None:
        del lease


class FixedAuthorityReader:
    def __init__(self, state: WorkflowState) -> None:
        self._state = state

    def load(
        self, *, work_run_id: str, execution_attempt_id: str
    ) -> tuple[WorkflowSnapshot, ExecutionAttemptRef]:
        return (
            WorkflowSnapshot(work_run_id, self._state, 2),
            ExecutionAttemptRef(
                execution_attempt_id,
                work_run_id,
                "task",
                "1",
                self._state,
                2,
                2,
                ExecutionStatus.RUNNING,
                "issuer:p1-5:test",
            ),
        )


def _call(mode: RuntimeMode = RuntimeMode.OWNER_SELF_DOGFOOD) -> ProviderCall:
    profile = load_provider_profile(
        Path("config/providers/provider-profiles.v1.toml"), "fake-openai-responses-v1"
    )
    return ProviderCall(
        "operation",
        canonical_sha256({"fixed": 1}),
        "attempt",
        "run",
        WorkflowState.RUNNING,
        2,
        mode,
        "owner",
        "p1-5-fixed-synthetic",
        2,
        profile,
        ({"role": "user", "content": "fixed"},),
        (),
        1,
    )


@pytest.mark.runtime
@pytest.mark.parametrize(
    "state", [WorkflowState.READY, WorkflowState.BLOCKED, WorkflowState.ACCEPTED]
)
def test_wrong_state_denies_before_provider_and_secret(state: WorkflowState) -> None:
    observer = Observer()
    service = AgentExecutionService(
        policy=SecurityPolicy(default_profiles()),
        adapter=observer,
        secret_resolver=observer,
        authority_reader=FixedAuthorityReader(state),
    )
    with pytest.raises(ValueError, match="WORKFLOW_NOT_RUNNING"):
        service.execute_provider(_call(), capabilities=())
    assert observer.calls == observer.resolves == 0


@pytest.mark.runtime
def test_replay_mode_denies_before_provider_and_secret() -> None:
    observer = Observer()
    service = AgentExecutionService(
        policy=SecurityPolicy(default_profiles()),
        adapter=observer,
        secret_resolver=observer,
        authority_reader=FixedAuthorityReader(WorkflowState.RUNNING),
    )
    with pytest.raises(ValueError, match="REPLAY_ZERO_EXECUTION"):
        service.execute_provider(_call(RuntimeMode.PUBLIC_RECORDED_REPLAY), capabilities=())
    assert observer.calls == observer.resolves == 0


@pytest.mark.runtime
def test_public_live_is_fixed_profile_scenario_only_and_still_requires_capabilities() -> None:
    observer = Observer()
    service = AgentExecutionService(
        policy=SecurityPolicy(default_profiles()),
        adapter=observer,
        secret_resolver=observer,
        authority_reader=FixedAuthorityReader(WorkflowState.RUNNING),
    )
    public_call = _call(RuntimeMode.PUBLIC_BOUNDED_LIVE)
    denied = service.execute_provider(public_call, capabilities=())
    assert denied.outcome.value == "DENIED_BEFORE_SIDE_EFFECT"
    with pytest.raises(ValueError, match="PROFILE_CONTEXT_DENIED"):
        service.execute_provider(
            replace(public_call, scenario_id="caller-selected-free-form"), capabilities=()
        )
    assert observer.calls == observer.resolves == 0
