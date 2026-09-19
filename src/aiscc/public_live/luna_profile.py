"""Immutable accepted V1 policy; local-only transport until separate L5/account gates."""

from dataclasses import replace
from datetime import UTC, datetime
from types import MappingProxyType
from typing import Any
from urllib.parse import urlsplit

from aiscc.contracts.workflow import RuntimeMode
from aiscc.providers.models import (
    ProviderCall,
    ProviderInputAuthority,
    ProviderProfile,
    SideEffectClass,
    ToolDefinition,
    ToolRegistry,
    canonical_json_bytes,
)

PRICE_REFERENCE = "https://developers.openai.com/api/docs/models/gpt-5.6-luna"
POLICY_REFERENCE = "20260916_0950_aiscc-p3-3-public-live-l4-provider-profile-v1-accepted.md"
INPUT_TOKEN_MAXIMUM = 8_000
OUTPUT_TOKEN_PER_REQUEST_MAXIMUM = 2_000
INPUT_PRICE_MICRO_USD_PER_MILLION = 200_000
CACHE_WRITE_ENVELOPE_NUMERATOR = 5
CACHE_WRITE_ENVELOPE_DENOMINATOR = 4
OUTPUT_PRICE_MICRO_USD_PER_MILLION = 1_200_000
ROLE_EFFORT = MappingProxyType({"PRIMARY": "low", "VERIFY": "low", "CORRECT": "medium"})


def luna_tool_registry() -> ToolRegistry:
    """Exact Public Live registry with no process/filesystem/tool-network authority."""
    tool = ToolDefinition(
        tool_id="stockroom_summary",
        schema_version="1",
        dispatcher_version="stockroom-summary-v1",
        description="Return the fixed deterministic Stockroom summary.",
        input_schema={
            "type": "object",
            "properties": {},
            "required": [],
            "additionalProperties": False,
        },
        side_effect_classification=SideEffectClass.READ_ONLY,
        allowed_modes=frozenset({RuntimeMode.PUBLIC_BOUNDED_LIVE}),
        allowed_profiles=frozenset({"public-live-luna-v1"}),
        allowed_scenarios=frozenset({"stockroom-s1-normal"}),
        underlying_resource_requirements=(),
        secret_requirement=None,
        timeout_seconds=5.0,
        retry_maximum=1,
        idempotency_policy="READ_ONLY_NO_RETRY_AFTER_DISPATCH",
        output_byte_bound=4096,
        output_schema=_stockroom_output_schema(),
        enabled=True,
        issued_at=datetime(2026, 9, 18, tzinfo=UTC),
        revoked_at=None,
    )
    return ToolRegistry(
        "aiscc-stockroom-tools",
        "2",
        MappingProxyType({"stockroom_summary": tool}),
    )


def _stockroom_output_schema() -> dict[str, Any]:
    integer = {"type": "integer", "minimum": 0, "maximum": 1000}
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["items", "total_available"],
        "properties": {
            "items": {
                "type": "array",
                "minItems": 3,
                "maxItems": 3,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "sku",
                        "on_hand",
                        "reserved",
                        "reorder_level",
                        "available",
                        "needs_reorder",
                    ],
                    "properties": {
                        "sku": {"type": "string", "enum": ["BOX-A", "BOX-B", "BOX-C"]},
                        "on_hand": integer,
                        "reserved": integer,
                        "reorder_level": integer,
                        "available": integer,
                        "needs_reorder": {"type": "boolean"},
                    },
                },
            },
            "total_available": {"type": "integer", "const": 13},
        },
    }


def luna_profile(base_url: str = "http://127.0.0.1:18085/v1") -> ProviderProfile:
    endpoint = urlsplit(base_url)
    if (
        endpoint.scheme != "http"
        or endpoint.hostname != "127.0.0.1"
        or endpoint.username
        or endpoint.password
        or endpoint.port is None
        or endpoint.path != "/v1"
        or endpoint.query
        or endpoint.fragment
    ):
        raise ValueError("LOCAL_PROVIDER_ONLY")
    return ProviderProfile(
        profile_id="public-live-luna-v1",
        version="1",
        provider_id="openai",
        adapter_protocol_version="responses-v1",
        model_ref="gpt-5.6-luna",
        endpoint_ref="local-deterministic-fake-only",
        base_url=base_url,
        secret_ref="secret-ref:public-live-luna-synthetic-only",
        allowed_runtime_modes=frozenset({RuntimeMode.PUBLIC_BOUNDED_LIVE}),
        scenario_allowlist=frozenset({"stockroom-s1-normal"}),
        public_repository_identity="repository:synthetic-stockroom",
        public_repository_version="be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d",
        public_scenario_identity="stockroom-s1-normal",
        public_scenario_version="1.0.0",
        tool_registry_id="aiscc-stockroom-tools",
        tool_registry_version="2",
        tool_allowlist=frozenset({"stockroom_summary"}),
        provider_call_maximum=4,
        agent_round_trip_maximum=4,
        tool_call_maximum=1,
        provider_retry_maximum=1,
        connect_timeout_seconds=5,
        read_timeout_seconds=30,
        total_timeout_seconds=35,
        output_token_bound=6000,
        output_byte_bound=24000,
        input_byte_bound=8000,
        continuation_item_maximum=16,
        continuation_byte_bound=6976,
        continuation_token_estimate_bound=8000,
        budget_unit_maximum=4,
        private_protocol_retention_policy_ref="private-protocol:public-live-v1",
        budget_policy_ref=POLICY_REFERENCE,
        data_classification_policy_ref="data-classification:stockroom-synthetic-v1",
        issued_at=datetime(2026, 9, 16, tzinfo=UTC),
        revoked_at=None,
        enabled=True,
    )


def hosted_luna_profile() -> ProviderProfile:
    """Exact hosted metadata; creating a profile does not authorize a send."""
    from aiscc.providers.hosted_secret import SECRET_REF

    return replace(
        luna_profile(),
        endpoint_ref="openai-public-live-production-v1",
        base_url="https://api.openai.com/v1",
        secret_ref=SECRET_REF,
    )


def bind_call(call: ProviderCall, *, role: str) -> tuple[ProviderCall, int]:
    if (
        role not in ROLE_EFFORT
        or call.profile
        != (
            hosted_luna_profile()
            if call.profile.base_url == "https://api.openai.com/v1"
            else luna_profile(call.profile.base_url)
        )
        or call.runtime_mode is not RuntimeMode.PUBLIC_BOUNDED_LIVE
        or call.scenario_id != "stockroom-s1-normal"
    ):
        raise ValueError("LUNA_PROFILE_BINDING_DENIED")
    if len(call.input_items) > 16:
        raise ValueError("INPUT_LIMIT")
    # Initial input is server-owned text. A durable local continuation may
    # contain only the Responses protocol item classes already validated by
    # P1-5 before this binding runs.
    if call.input_authority is ProviderInputAuthority.INITIAL_SERVER:
        for item in call.input_items:
            if (
                set(item) != {"role", "content"}
                or item["role"] not in {"system", "developer", "user", "assistant"}
                or not isinstance(item["content"], str)
            ):
                raise ValueError("SERVER_TEXT_INPUT_REQUIRED")
    elif (
        call.input_authority is not ProviderInputAuthority.DURABLE_LOCAL
        or call.durable_continuation_hash is None
        or len(call.durable_continuation_hash) != 64
        or any(
            item.get("type")
            not in {"message", "function_call", "function_call_output", "reasoning"}
            for item in call.input_items
        )
    ):
        raise ValueError("DURABLE_CONTINUATION_REQUIRED")
    for tool in call.tools:
        if (
            tool.get("name") != "stockroom_summary"
            or tool.get("type") != "function"
            or tool.get("strict") is not True
            or tool.get("parameters")
            != {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            }
        ):
            raise ValueError("TOOL_SCOPE_DENIED")
    if len(call.tools) > 1:
        raise ValueError("TOOL_SCOPE_DENIED")
    inputs = (
        len(canonical_json_bytes({"input": list(call.input_items), "tools": list(call.tools)}))
        + 1024
    )
    if inputs > INPUT_TOKEN_MAXIMUM:
        raise ValueError("INPUT_LIMIT")
    return (
        replace(
            call,
            reasoning_effort=ROLE_EFFORT[role],
            output_token_maximum=OUTPUT_TOKEN_PER_REQUEST_MAXIMUM,
        ),
        inputs,
    )


def conservative_request_liability_micro(profile: ProviderProfile) -> int:
    """Return the accepted Luna V1 one-request ceiling in integer micro-USD."""
    expected = (
        hosted_luna_profile()
        if profile.base_url == "https://api.openai.com/v1"
        else luna_profile(profile.base_url)
    )
    if profile != expected:
        raise ValueError("LUNA_PROFILE_BINDING_DENIED")
    input_rate = (
        INPUT_PRICE_MICRO_USD_PER_MILLION
        * CACHE_WRITE_ENVELOPE_NUMERATOR
        // CACHE_WRITE_ENVELOPE_DENOMINATOR
    )
    numerator = (
        INPUT_TOKEN_MAXIMUM * input_rate
        + OUTPUT_TOKEN_PER_REQUEST_MAXIMUM * OUTPUT_PRICE_MICRO_USD_PER_MILLION
    )
    return (numerator + 999_999) // 1_000_000
