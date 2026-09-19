from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import httpx2 as httpx
import pytest
from fake_responses_server import (
    FakeResponsesServer,
    final_message,
    response_body,
)
from openai import APIConnectionError, APITimeoutError, BadRequestError

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.providers.models import (
    ExecutionOperationOutcome,
    ProviderCall,
    canonical_sha256,
)
from aiscc.providers.openai_responses import OpenAIResponsesAdapter, validate_continuation
from aiscc.providers.profiles import load_provider_profile, load_tool_registry


def _call() -> ProviderCall:
    profile = load_provider_profile(
        Path("config/providers/provider-profiles.v1.toml"), "fake-openai-responses-v1"
    )
    registry = load_tool_registry(Path("config/providers/tool-registry.v1.toml"))
    definition = registry.tools["synthetic_lookup"]
    tools = (
        {
            "type": "function",
            "name": definition.tool_id,
            "description": definition.description,
            "parameters": definition.input_schema,
            "strict": True,
        },
    )
    fingerprint = canonical_sha256({"operation": "provider", "ordinal": 1})
    return ProviderCall(
        "operation-1",
        fingerprint,
        "attempt",
        "run",
        WorkflowState.RUNNING,
        2,
        RuntimeMode.OWNER_SELF_DOGFOOD,
        "owner",
        "p1-5-fixed-synthetic",
        2,
        profile,
        ({"role": "user", "content": "fixed synthetic request"},),
        tools,
        1,
    )


def test_official_sdk_serializes_exact_stateless_v1_flags_against_local_fake() -> None:
    with FakeResponsesServer() as server:
        server.enqueue(response_body("completed", [final_message()]))
        adapter = OpenAIResponsesAdapter()
        result = adapter.call(_call(), secret="synthetic-local-only")
    assert result.outcome is ExecutionOperationOutcome.PROVIDER_COMPLETED
    assert result.output_text == "AISCC_FAKE_FINAL"
    request = server.requests[0]
    assert {
        key: request[key]
        for key in ("background", "stream", "store", "parallel_tool_calls", "truncation")
    } == {
        "background": False,
        "stream": False,
        "store": False,
        "parallel_tool_calls": False,
        "truncation": "disabled",
    }
    assert "conversation" not in request and "previous_response_id" not in request
    assert all(tool["type"] == "function" and tool["strict"] for tool in request["tools"])


def test_proxy_environment_cannot_retarget_fixed_transport(monkeypatch) -> None:
    monkeypatch.setenv("HTTP_PROXY", "http://127.0.0.1:1")
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:1")
    monkeypatch.setenv("ALL_PROXY", "http://127.0.0.1:1")
    with FakeResponsesServer() as server:
        server.enqueue(response_body("completed", [final_message()]))
        result = OpenAIResponsesAdapter().call(_call(), secret="synthetic-local-only")
    assert result.outcome is ExecutionOperationOutcome.PROVIDER_COMPLETED
    assert len(server.requests) == 1


@pytest.mark.parametrize(
    ("status", "outcome"),
    [
        ("queued", ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME),
        ("in_progress", ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME),
        ("failed", ExecutionOperationOutcome.PROVIDER_REJECTED),
        ("cancelled", ExecutionOperationOutcome.CANCELLED),
        ("incomplete", ExecutionOperationOutcome.PROVIDER_INCOMPLETE),
    ],
)
def test_exact_response_status_mapping(status: str, outcome: ExecutionOperationOutcome) -> None:
    with FakeResponsesServer() as server:
        server.enqueue(response_body(status))
        result = OpenAIResponsesAdapter().call(_call(), secret="synthetic-local-only")
    assert result.outcome is outcome
    if status in {"queued", "in_progress"}:
        assert result.sanitized_error == "PROVIDER_NONTERMINAL_STATUS"


def test_unknown_response_and_malformed_body_have_fixed_safe_diagnostics() -> None:
    unknown = response_body("future-provider-status")
    with FakeResponsesServer() as server:
        server.enqueue(unknown)
        unknown_result = OpenAIResponsesAdapter().call(_call(), secret="synthetic-local-only")
    assert unknown_result.outcome is ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
    assert unknown_result.sanitized_error == "UNKNOWN_RESPONSE_STATUS"

    with FakeResponsesServer() as server:
        server.enqueue([])  # type: ignore[arg-type]
        malformed = OpenAIResponsesAdapter().call(_call(), secret="synthetic-local-only")
    assert malformed.outcome is ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
    assert malformed.sanitized_error == "MALFORMED_RESPONSE_BODY"


@pytest.mark.parametrize("kind", ["timeout", "connection", "bad_request"])
def test_sdk_failures_have_fixed_safe_diagnostics(monkeypatch, kind: str) -> None:
    request = httpx.Request("POST", "http://127.0.0.1:18085/v1/responses")
    if kind == "timeout":
        failure = APITimeoutError(request)
        expected = "TRANSPORT_OUTCOME_UNKNOWN"
    elif kind == "connection":
        failure = APIConnectionError(request=request)
        expected = "TRANSPORT_OUTCOME_UNKNOWN"
    else:
        failure = BadRequestError(
            "synthetic safe bad request",
            response=httpx.Response(400, request=request),
            body=None,
        )
        expected = "PROVIDER_HTTP_ERROR_RESPONSE"

    def sdk(**_kwargs):
        def create(**_request):
            raise failure

        return SimpleNamespace(
            responses=SimpleNamespace(with_raw_response=SimpleNamespace(create=create))
        )

    monkeypatch.setattr("aiscc.providers.openai_responses.OpenAI", sdk)
    result = OpenAIResponsesAdapter().call(_call(), secret="synthetic-local-only")
    assert result.outcome is ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
    assert result.sanitized_error == expected


def test_function_call_and_private_continuation_call_id_binding() -> None:
    function_call = {
        "id": "fc_fake",
        "type": "function_call",
        "status": "completed",
        "name": "synthetic_lookup",
        "call_id": "call_exact",
        "arguments": '{"key":"aiscc-fixed-key"}',
    }
    with FakeResponsesServer() as server:
        server.enqueue(response_body("completed", [function_call]))
        result = OpenAIResponsesAdapter().call(_call(), secret="synthetic-local-only")
    assert result.tool_call is not None and result.tool_call.call_id == "call_exact"
    continuation = (
        {"type": "reasoning", "encrypted_content": "opaque-ciphertext-only"},
        function_call,
        {"type": "function_call_output", "call_id": "call_exact", "output": "fixed"},
    )
    validate_continuation(
        continuation,
        call_id="call_exact",
        maximum_items=4,
        maximum_bytes=4096,
        maximum_token_estimate=2048,
    )
    with pytest.raises(ValueError, match="CALL_ID"):
        validate_continuation(
            continuation,
            call_id="wrong",
            maximum_items=4,
            maximum_bytes=4096,
            maximum_token_estimate=2048,
        )
    with pytest.raises(ValueError, match="TOKEN_ESTIMATE"):
        validate_continuation(
            continuation,
            call_id="call_exact",
            maximum_items=4,
            maximum_bytes=4096,
            maximum_token_estimate=1,
        )


def test_hosted_tool_and_over_bound_output_fail_closed() -> None:
    with FakeResponsesServer() as server:
        server.enqueue(response_body("completed", [{"id": "hosted", "type": "web_search_call"}]))
        hosted = OpenAIResponsesAdapter().call(_call(), secret="synthetic-local-only")
    assert hosted.outcome is ExecutionOperationOutcome.PROVIDER_REJECTED
    assert hosted.sanitized_error == "PROTOCOL_OUTPUT_REJECTED"

    oversized = final_message()
    oversized["content"][0]["text"] = "x" * (_call().profile.output_byte_bound + 1)
    with FakeResponsesServer() as server:
        server.enqueue(response_body("completed", [oversized]))
        bounded = OpenAIResponsesAdapter().call(_call(), secret="synthetic-local-only")
    assert bounded.outcome is ExecutionOperationOutcome.PROVIDER_REJECTED
    assert bounded.sanitized_error == "OUTPUT_BOUND_EXCEEDED"
