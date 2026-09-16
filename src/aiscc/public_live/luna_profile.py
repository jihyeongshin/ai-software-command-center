"""Immutable accepted V1 policy; local-only transport until separate L5/account gates."""

from dataclasses import replace
from datetime import UTC, datetime
from types import MappingProxyType
from urllib.parse import urlsplit

from aiscc.contracts.workflow import RuntimeMode
from aiscc.providers.models import ProviderCall, ProviderProfile, canonical_json_bytes

PRICE_REFERENCE = "https://developers.openai.com/api/docs/models/gpt-5.6-luna"
POLICY_REFERENCE = "20260916_0950_aiscc-p3-3-public-live-l4-provider-profile-v1-accepted.md"
ROLE_EFFORT = MappingProxyType({"PRIMARY": "low", "VERIFY": "low", "CORRECT": "medium"})


def luna_tool_registry(config, spec):
    """Reuse Stockroom's exact process/resource requirements and sandbox spec."""
    from aiscc.providers.models import ToolRegistry
    from aiscc.providers.stockroom_tool import build_stockroom_registry

    if config.registry_version != "2":
        raise ValueError("LUNA_TOOL_REGISTRY_VERSION_DENIED")
    baseline = build_stockroom_registry(config, spec)
    tool = baseline.tools["stockroom_summary"]
    return ToolRegistry(
        baseline.registry_id,
        baseline.version,
        MappingProxyType(
            {
                "stockroom_summary": replace(
                    tool,
                    allowed_modes=frozenset({RuntimeMode.PUBLIC_BOUNDED_LIVE}),
                    allowed_profiles=frozenset({"public-live-luna-v1"}),
                    allowed_scenarios=frozenset({"stockroom-s1-normal"}),
                )
            }
        ),
    )


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


def bind_call(call: ProviderCall, *, role: str) -> tuple[ProviderCall, int]:
    if (
        role not in ROLE_EFFORT
        or call.profile != luna_profile(call.profile.base_url)
        or call.runtime_mode is not RuntimeMode.PUBLIC_BOUNDED_LIVE
        or call.scenario_id != "stockroom-s1-normal"
    ):
        raise ValueError("LUNA_PROFILE_BINDING_DENIED")
    if len(call.input_items) > 16:
        raise ValueError("INPUT_LIMIT")
    # Text-only server payload. Byte upper bound, plus 1024 reserved framing
    # tokens, is intentionally stricter than a chars/4 token estimate.
    for item in call.input_items:
        if (
            set(item) != {"role", "content"}
            or item["role"] not in {"system", "developer", "user", "assistant"}
            or not isinstance(item["content"], str)
        ):
            raise ValueError("SERVER_TEXT_INPUT_REQUIRED")
    for tool in call.tools:
        if (
            tool.get("name") != "stockroom_summary"
            or tool.get("type") != "function"
            or tool.get("strict") is not True
            or tool.get("parameters")
            not in (
                {"type": "object", "properties": {}, "required": [], "additionalProperties": False},
                {"type": "object", "required": [], "additionalProperties": False},
            )
        ):
            raise ValueError("TOOL_SCOPE_DENIED")
    if len(call.tools) > 1:
        raise ValueError("TOOL_SCOPE_DENIED")
    inputs = (
        len(canonical_json_bytes({"input": list(call.input_items), "tools": list(call.tools)}))
        + 1024
    )
    if inputs > 8000:
        raise ValueError("INPUT_LIMIT")
    return replace(call, reasoning_effort=ROLE_EFFORT[role], output_token_maximum=2000), inputs
