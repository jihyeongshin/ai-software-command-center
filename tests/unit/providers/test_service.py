from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from types import MappingProxyType

import pytest

from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.providers.models import (
    ExecutionAttemptRef,
    ExecutionOperationOutcome,
    ExecutionStatus,
    ProviderCall,
    ProviderResult,
    SecretResolutionLease,
    canonical_sha256,
)
from aiscc.providers.profiles import load_provider_profile
from aiscc.providers.service import (
    AgentExecutionService,
    ReplayExecutionService,
    _durable_provider_output_token_charge,
)
from aiscc.security.policy import SecurityPolicy, default_profiles


class NeverAdapter:
    def __init__(self) -> None:
        self.calls = 0

    def call(self, call: ProviderCall, *, secret: str) -> ProviderResult:
        del call, secret
        self.calls += 1
        raise AssertionError("adapter must not be reached")


class NeverResolver:
    def __init__(self) -> None:
        self.resolves = 0

    def resolve(self, lease: SecretResolutionLease) -> str:
        del lease
        self.resolves += 1
        raise AssertionError("resolver must not be reached")

    def close(self, lease: SecretResolutionLease) -> None:
        del lease


class FixedAuthorityReader:
    def load(
        self, *, work_run_id: str, execution_attempt_id: str
    ) -> tuple[WorkflowSnapshot, ExecutionAttemptRef]:
        return (
            WorkflowSnapshot(work_run_id, WorkflowState.RUNNING, 2),
            ExecutionAttemptRef(
                execution_attempt_id,
                work_run_id,
                "task",
                "1",
                WorkflowState.RUNNING,
                2,
                2,
                ExecutionStatus.RUNNING,
                "issuer:p1-5:test",
            ),
        )


def _call() -> ProviderCall:
    profile = load_provider_profile(
        Path("config/providers/provider-profiles.v1.toml"), "fake-openai-responses-v1"
    )
    return ProviderCall(
        "operation",
        canonical_sha256({"operation": 1}),
        "attempt",
        "run",
        WorkflowState.RUNNING,
        2,
        RuntimeMode.OWNER_SELF_DOGFOOD,
        "owner",
        "p1-5-fixed-synthetic",
        2,
        profile,
        ({"role": "user", "content": "fixed"},),
        (),
        1,
    )


def test_security_denial_prevents_secret_resolution_and_provider_side_effect() -> None:
    adapter, resolver = NeverAdapter(), NeverResolver()
    service = AgentExecutionService(
        policy=SecurityPolicy(default_profiles()),
        adapter=adapter,
        secret_resolver=resolver,
        authority_reader=FixedAuthorityReader(),
    )
    result = service.execute_provider(_call(), capabilities=())
    assert result.status == "denied"
    assert adapter.calls == resolver.resolves == 0


def test_replay_has_zero_execution_and_no_live_fallback() -> None:
    replay = ReplayExecutionService(
        {
            "fixed": {
                "status": "EXECUTOR_COMPLETED",
                "output": "recorded",
                "content_hash": "3d96a458120e68868ccca6bad66be3fc8df4627a6b7372d69b98d3ba7688774d",
            },
            "corrupt": {
                "status": "EXECUTOR_COMPLETED",
                "output": "tampered",
                "content_hash": "0" * 64,
            },
        }
    )
    assert replay.replay("fixed") == {
        "status": "EXECUTOR_COMPLETED",
        "output": "recorded",
        "content_hash": "3d96a458120e68868ccca6bad66be3fc8df4627a6b7372d69b98d3ba7688774d",
    }
    with pytest.raises(ValueError, match="NO_LIVE_FALLBACK"):
        replay.replay("missing")
    with pytest.raises(ValueError, match="CORRUPT_NO_LIVE_FALLBACK"):
        replay.replay("corrupt")
    assert replay.invocation_counts == {
        "provider": 0,
        "tool": 0,
        "process": 0,
        "network": 0,
        "secret": 0,
    }


def test_each_bound_closes_new_provider_work() -> None:
    service = AgentExecutionService(
        policy=SecurityPolicy(default_profiles()),
        adapter=NeverAdapter(),
        secret_resolver=NeverResolver(),
        authority_reader=FixedAuthorityReader(),
    )
    service.counters.provider_calls = _call().profile.provider_call_maximum
    with pytest.raises(ValueError, match="LIMIT_EXHAUSTED"):
        service.execute_provider(_call(), capabilities=())


@pytest.mark.parametrize(
    "bound",
    ["provider", "round", "budget", "tool", "retry", "input", "output", "output_token"],
)
def test_each_independent_bound_emits_one_failure_and_closes(bound: str) -> None:
    service = AgentExecutionService(
        policy=SecurityPolicy(default_profiles()),
        adapter=NeverAdapter(),
        secret_resolver=NeverResolver(),
        authority_reader=FixedAuthorityReader(),
    )
    call = _call()
    if bound == "provider":
        service.counters.provider_calls = call.profile.provider_call_maximum
    elif bound == "round":
        service.counters.rounds = call.profile.agent_round_trip_maximum
    elif bound == "budget":
        service.counters.budget_units = call.profile.budget_unit_maximum
    elif bound == "tool":
        service.counters.tool_calls = call.profile.tool_call_maximum
    elif bound == "retry":
        service.counters.retries = call.profile.provider_retry_maximum
    elif bound == "output":
        service.counters.output_bytes = call.profile.output_byte_bound
    elif bound == "output_token":
        service.counters.output_tokens = call.profile.output_token_bound
    else:
        call = replace(call, profile=replace(call.profile, input_byte_bound=1))

    def action() -> object:
        if bound == "tool":
            service.admit_tool_side_effect(call)
            return None
        if bound == "retry":
            service.admit_provider_retry(
                call, previous_outcome=ExecutionOperationOutcome.DEFINITELY_NOT_SENT
            )
            return None
        if bound == "output":
            service.admit_output(call, output_bytes=1, output_tokens=0)
            return None
        if bound == "output_token":
            service.admit_output(call, output_bytes=0, output_tokens=1)
            return None
        return service.execute_provider(call, capabilities=())

    with pytest.raises(ValueError, match="EXECUTION_LIMIT_EXHAUSTED"):
        action()
    assert len(service.failure_events) == 1
    with pytest.raises(ValueError, match="EXECUTION_ATTEMPT_CLOSED"):
        action()
    assert len(service.failure_events) == 1


def test_wall_time_bound_is_independent_and_fail_closed() -> None:
    clock = [0.0]
    service = AgentExecutionService(
        policy=SecurityPolicy(default_profiles()),
        adapter=NeverAdapter(),
        secret_resolver=NeverResolver(),
        authority_reader=FixedAuthorityReader(),
        time_source=lambda: clock[0],
    )
    clock[0] = _call().profile.total_timeout_seconds
    with pytest.raises(ValueError, match="WALL_TIME"):
        service.execute_provider(_call(), capabilities=())
    assert service.failure_events == ["WALL_TIME_LIMIT_EXHAUSTED"]


def test_unknown_outcome_retry_is_forbidden_and_definitely_not_sent_is_bounded() -> None:
    denied = AgentExecutionService(
        policy=SecurityPolicy(default_profiles()),
        adapter=NeverAdapter(),
        secret_resolver=NeverResolver(),
        authority_reader=FixedAuthorityReader(),
    )
    with pytest.raises(ValueError, match="RETRY_OUTCOME_DENIED"):
        denied.admit_provider_retry(
            _call(),
            previous_outcome=ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME,
        )
    assert denied.counters.retries == 0

    bounded = AgentExecutionService(
        policy=SecurityPolicy(default_profiles()),
        adapter=NeverAdapter(),
        secret_resolver=NeverResolver(),
        authority_reader=FixedAuthorityReader(),
    )
    bounded.admit_provider_retry(
        _call(), previous_outcome=ExecutionOperationOutcome.DEFINITELY_NOT_SENT
    )
    assert bounded.counters.retries == 1


def test_durable_output_token_charge_requires_exact_request_and_reported_integers() -> None:
    def result(
        usage: dict[str, object],
        *,
        sanitized_error: str | None = None,
    ) -> ProviderResult:
        return ProviderResult(
            operation_id="operation",
            status="completed",
            outcome=ExecutionOperationOutcome.PROVIDER_COMPLETED,
            response_id="response",
            output_items=(),
            output_text="fixed",
            tool_call=None,
            usage=MappingProxyType(usage),  # type: ignore[arg-type]
            sanitized_error=sanitized_error,
            result_hash="0" * 64,
        )

    missing = result({})
    assert _durable_provider_output_token_charge(missing, requested_maximum=8) == 8
    assert (
        _durable_provider_output_token_charge(result({"output_tokens": 3}), requested_maximum=8)
        == 3
    )
    assert (
        _durable_provider_output_token_charge(result({"output_tokens": 0}), requested_maximum=8)
        == 0
    )

    for invalid_maximum in (None, 0, -1, True):
        with pytest.raises(ValueError, match="REQUESTED_MAX_OUTPUT_TOKENS_INVALID"):
            _durable_provider_output_token_charge(
                missing,
                requested_maximum=invalid_maximum,
            )
    for invalid_usage in (-1, 9, True, 1.0, "1"):
        with pytest.raises(ValueError, match="INVALID_PROVIDER_OUTPUT_TOKEN_USAGE"):
            _durable_provider_output_token_charge(
                result({"output_tokens": invalid_usage}),
                requested_maximum=8,
            )
    with pytest.raises(ValueError, match="INVALID_PROVIDER_OUTPUT_TOKEN_USAGE"):
        _durable_provider_output_token_charge(
            result({}, sanitized_error="INVALID_PROVIDER_OUTPUT_TOKEN_USAGE"),
            requested_maximum=8,
        )
