from __future__ import annotations

import hashlib
from types import MappingProxyType
from typing import Any

from openai import APIConnectionError, APITimeoutError, OpenAI, Timeout

from aiscc.providers.models import (
    ExecutionOperationOutcome,
    ProviderCall,
    ProviderResult,
    ToolCallCandidate,
    canonical_json_bytes,
)

_SIX_STATUSES = frozenset(
    {"queued", "in_progress", "completed", "failed", "cancelled", "incomplete"}
)


class OpenAIResponsesAdapter:
    """Stateless Responses V1 adapter; the profile must point to a local acceptance endpoint."""

    def __init__(self) -> None:
        self.invocation_count = 0
        self.last_request: dict[str, Any] | None = None

    def call(self, call: ProviderCall, *, secret: str) -> ProviderResult:
        if not call.profile.base_url.startswith("http://127.0.0.1:"):
            raise ValueError("REAL_PROVIDER_ENDPOINT_FORBIDDEN")
        input_items = list(call.input_items)
        request: dict[str, Any] = {
            "model": call.profile.model_ref,
            "input": input_items,
            "tools": list(call.tools),
            "background": False,
            "stream": False,
            "store": False,
            "parallel_tool_calls": False,
            "truncation": "disabled",
            "include": ["reasoning.encrypted_content"],
            "max_output_tokens": call.output_token_maximum or call.profile.output_token_bound,
        }
        if call.profile.profile_id == "public-live-luna-v1":
            from aiscc.public_live.luna_profile import bind_call

            role = "CORRECT" if call.reasoning_effort == "medium" else "PRIMARY"
            bound, _ = bind_call(call, role=role)
            if call.reasoning_effort != bound.reasoning_effort or call.output_token_maximum != 2000:
                raise ValueError("LUNA_REQUEST_BINDING_DENIED")
            request["reasoning"] = {"effort": bound.reasoning_effort}
            request["service_tier"] = "default"
        serialized = canonical_json_bytes(request)
        if len(serialized) > call.profile.input_byte_bound:
            raise ValueError("PROVIDER_INPUT_BOUND_EXCEEDED")
        self.last_request = request
        self.invocation_count += 1
        client = OpenAI(
            api_key=secret,
            base_url=call.profile.base_url,
            timeout=Timeout(
                call.profile.total_timeout_seconds,
                connect=call.profile.connect_timeout_seconds,
                read=call.profile.read_timeout_seconds,
            ),
            max_retries=0,
        )
        try:
            raw_response = client.responses.with_raw_response.create(**request)
        except (APITimeoutError, APIConnectionError):
            return _result(
                call.operation_id,
                "unknown",
                ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME,
                None,
                (),
                sanitized_error="TRANSPORT_OUTCOME_UNKNOWN",
            )
        raw_body = raw_response.http_response.json()
        if not isinstance(raw_body, dict):
            return _result(
                call.operation_id,
                "unknown",
                ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME,
                None,
                (),
                sanitized_error="MALFORMED_RESPONSE_BODY",
            )
        body: dict[str, Any] = raw_body
        status = body.get("status")
        if status not in _SIX_STATUSES:
            return _result(
                call.operation_id,
                str(status),
                ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME,
                body.get("id"),
                (),
                sanitized_error="UNKNOWN_RESPONSE_STATUS",
            )
        output = body.get("output")
        items = (
            tuple(item for item in output if isinstance(item, dict))
            if isinstance(output, list)
            else ()
        )
        if status in {"queued", "in_progress"}:
            return _result(
                call.operation_id,
                status,
                ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME,
                body.get("id"),
                items,
                usage=_usage(body),
            )
        if status == "failed":
            return _result(
                call.operation_id,
                status,
                ExecutionOperationOutcome.PROVIDER_REJECTED,
                body.get("id"),
                items,
                usage=_usage(body),
                sanitized_error="PROVIDER_FAILED",
            )
        if status == "cancelled":
            return _result(
                call.operation_id,
                status,
                ExecutionOperationOutcome.CANCELLED,
                body.get("id"),
                items,
                usage=_usage(body),
            )
        if status == "incomplete":
            return _result(
                call.operation_id,
                status,
                ExecutionOperationOutcome.PROVIDER_INCOMPLETE,
                body.get("id"),
                items,
                usage=_usage(body),
                sanitized_error="PROVIDER_INCOMPLETE",
            )
        return self._completed(call, body, items)

    def _completed(
        self, call: ProviderCall, body: dict[str, Any], items: tuple[dict[str, Any], ...]
    ) -> ProviderResult:
        usage, usage_error = _completed_usage(
            body,
            requested_maximum=call.output_token_maximum or call.profile.output_token_bound,
        )
        hosted = any(
            item.get("type") not in {"message", "function_call", "reasoning"} for item in items
        )
        calls = [item for item in items if item.get("type") == "function_call"]
        messages = [item for item in items if item.get("type") == "message"]
        if hosted or len(calls) > 1 or (calls and messages) or (not calls and len(messages) != 1):
            return _result(
                call.operation_id,
                "completed",
                ExecutionOperationOutcome.PROVIDER_REJECTED,
                body.get("id"),
                items,
                usage=usage,
                sanitized_error="PROTOCOL_OUTPUT_REJECTED",
            )
        tool_call = None
        output_text = None
        if calls:
            item = calls[0]
            name, arguments, call_id = item.get("name"), item.get("arguments"), item.get("call_id")
            if not (
                isinstance(name, str)
                and name
                and isinstance(arguments, str)
                and arguments
                and isinstance(call_id, str)
                and call_id
            ):
                return _result(
                    call.operation_id,
                    "completed",
                    ExecutionOperationOutcome.PROVIDER_REJECTED,
                    body.get("id"),
                    items,
                    usage=usage,
                    sanitized_error="MALFORMED_FUNCTION_CALL",
                )
            tool_call = ToolCallCandidate(name, arguments, call_id)
        else:
            output_text = body.get("output_text")
            if not isinstance(output_text, str):
                output_text = _message_text(messages[0])
            if len(output_text.encode()) > call.profile.output_byte_bound:
                return _result(
                    call.operation_id,
                    "completed",
                    ExecutionOperationOutcome.PROVIDER_REJECTED,
                    body.get("id"),
                    items,
                    usage=usage,
                    sanitized_error="OUTPUT_BOUND_EXCEEDED",
                )
        return _result(
            call.operation_id,
            "completed",
            ExecutionOperationOutcome.PROVIDER_COMPLETED,
            body.get("id"),
            items,
            usage=usage,
            output_text=output_text,
            tool_call=tool_call,
            sanitized_error=usage_error,
        )


def validate_continuation(
    items: tuple[dict[str, Any], ...],
    *,
    call_id: str,
    maximum_items: int,
    maximum_bytes: int,
    maximum_token_estimate: int,
) -> None:
    if not items or len(items) > maximum_items:
        raise ValueError("CONTINUATION_ITEM_BOUND_OR_MISSING")
    encoded = canonical_json_bytes(list(items))
    if len(encoded) > maximum_bytes:
        raise ValueError("CONTINUATION_BYTE_BOUND")
    if (len(encoded) + 3) // 4 > maximum_token_estimate:
        raise ValueError("CONTINUATION_TOKEN_ESTIMATE_BOUND")
    allowed_types = {"message", "function_call", "function_call_output", "reasoning"}
    if any(item.get("type") not in allowed_types for item in items):
        raise ValueError("CONTINUATION_ITEM_TYPE_DENIED")
    reasoning = [item for item in items if item.get("type") == "reasoning"]
    if any(
        not isinstance(item.get("encrypted_content"), str) or not item.get("encrypted_content")
        for item in reasoning
    ):
        raise ValueError("CONTINUATION_REASONING_STATE_CORRUPT")
    calls = [item for item in items if item.get("type") == "function_call"]
    outputs = [item for item in items if item.get("type") == "function_call_output"]
    if not calls or len(calls) != len(outputs):
        raise ValueError("CONTINUATION_CALL_PAIR_MISSING")
    call_ids = [item.get("call_id") for item in calls]
    output_ids = [item.get("call_id") for item in outputs]
    if (
        any(not isinstance(value, str) or not value for value in (*call_ids, *output_ids))
        or len(set(call_ids)) != len(call_ids)
        or call_ids != output_ids
        or output_ids[-1] != call_id
    ):
        raise ValueError("CONTINUATION_CALL_ID_MISMATCH")
    for call, output in zip(calls, outputs, strict=True):
        if items.index(call) >= items.index(output):
            raise ValueError("CONTINUATION_CALL_ORDER_MISMATCH")


def _message_text(item: dict[str, Any]) -> str:
    content = item.get("content")
    if not isinstance(content, list):
        raise ValueError("MALFORMED_MESSAGE")
    values = [
        part.get("text")
        for part in content
        if isinstance(part, dict) and part.get("type") == "output_text"
    ]
    if len(values) != 1 or not isinstance(values[0], str):
        raise ValueError("MALFORMED_MESSAGE")
    return values[0]


def _result(
    operation_id: str,
    status: str,
    outcome: ExecutionOperationOutcome,
    response_id: object,
    items: tuple[dict[str, Any], ...],
    *,
    usage: MappingProxyType[str, int] | None = None,
    output_text: str | None = None,
    tool_call: ToolCallCandidate | None = None,
    sanitized_error: str | None = None,
) -> ProviderResult:
    payload = {"status": status, "outcome": outcome.value, "items": list(items)}
    return ProviderResult(
        operation_id,
        status,
        outcome,
        response_id if isinstance(response_id, str) else None,
        items,
        output_text,
        tool_call,
        usage or MappingProxyType({}),
        sanitized_error,
        hashlib.sha256(canonical_json_bytes(payload)).hexdigest(),
    )


def _usage(body: dict[str, Any]) -> MappingProxyType[str, int]:
    raw = body.get("usage")
    if not isinstance(raw, dict):
        return MappingProxyType({})
    values = {
        key: value
        for key, value in raw.items()
        if key in {"input_tokens", "output_tokens", "total_tokens"}
        and type(value) is int
        and value >= 0
    }
    return MappingProxyType(values)


def _completed_usage(
    body: dict[str, Any],
    *,
    requested_maximum: int,
) -> tuple[MappingProxyType[str, int], str | None]:
    raw = body.get("usage")
    if raw is None:
        return MappingProxyType({}), None
    if not isinstance(raw, dict):
        return MappingProxyType({}), "INVALID_PROVIDER_OUTPUT_TOKEN_USAGE"
    if "output_tokens" not in raw:
        return _usage(body), None
    reported = raw["output_tokens"]
    if (
        type(reported) is not int
        or reported < 0
        or type(requested_maximum) is not int
        or requested_maximum <= 0
        or reported > requested_maximum
    ):
        return MappingProxyType({}), "INVALID_PROVIDER_OUTPUT_TOKEN_USAGE"
    return _usage(body), None
