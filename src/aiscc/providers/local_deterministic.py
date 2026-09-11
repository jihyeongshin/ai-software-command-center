"""Owner-only deterministic Stockroom provider with no transport imports."""

from __future__ import annotations

import json
import tomllib
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from types import MappingProxyType
from typing import Any

from aiscc.contracts.workflow import RuntimeMode
from aiscc.providers.models import (
    ExecutionOperationOutcome,
    ProviderCall,
    ProviderProfile,
    ProviderResult,
    ToolCallCandidate,
    canonical_json_bytes,
    canonical_sha256,
    parse_strict_json_object,
)
from aiscc.scenarios.models import RESOURCE_REF, SCENARIO_IDS

LOCAL_COMPATIBILITY_SECRET_REF = "secret-ref:stockroom-local-non-secret-compat-v1"
LOCAL_COMPATIBILITY_SENTINEL = "aiscc-local-non-secret-sentinel-v1"

STOCKROOM_SUMMARY: dict[str, object] = {
    "items": [
        {
            "sku": "BOX-A",
            "on_hand": 12,
            "reserved": 2,
            "reorder_level": 3,
            "available": 10,
            "needs_reorder": False,
        },
        {
            "sku": "BOX-B",
            "on_hand": 5,
            "reserved": 5,
            "reorder_level": 2,
            "available": 0,
            "needs_reorder": True,
        },
        {
            "sku": "BOX-C",
            "on_hand": 4,
            "reserved": 1,
            "reorder_level": 3,
            "available": 3,
            "needs_reorder": True,
        },
    ],
    "total_available": 13,
}

_PROFILE_IDS = (
    "stockroom-owner-s1-v1",
    "stockroom-owner-s2-v1",
    "stockroom-owner-s3-v1",
    "stockroom-owner-s4-v1",
)
_ROOT_KEYS = {"schema_version", "default_effect", "profiles"}
_PROFILE_KEYS = {
    "version",
    "scenario_id",
    "provider_id",
    "adapter_protocol_version",
    "model_ref",
    "endpoint_ref",
    "base_url",
    "secret_ref",
    "tool_registry_id",
    "tool_registry_version",
    "tool_allowlist",
    "tool_dispatch_allowed",
    "provider_call_maximum",
    "agent_round_trip_maximum",
    "tool_call_maximum",
    "provider_retry_maximum",
    "connect_timeout_seconds",
    "read_timeout_seconds",
    "total_timeout_seconds",
    "output_token_bound",
    "output_byte_bound",
    "input_byte_bound",
    "continuation_item_maximum",
    "continuation_byte_bound",
    "continuation_token_estimate_bound",
    "budget_unit_maximum",
}


@dataclass(frozen=True, slots=True)
class LocalStockroomProfile:
    profile: ProviderProfile
    scenario_id: str
    tool_dispatch_allowed: bool


def load_stockroom_owner_profiles(path: Path) -> MappingProxyType[str, LocalStockroomProfile]:
    with path.open("rb") as stream:
        raw = tomllib.load(stream)
    _exact_keys(raw, _ROOT_KEYS, "profile root")
    version = {"AISCC-STOCKROOM-OWNER-PROFILES-V1": "1",
               "AISCC-STOCKROOM-OWNER-PROFILES-V2": "2"}.get(raw["schema_version"])
    if (
        version is None
        or raw["default_effect"] != "DENY"
    ):
        raise ValueError("STOCKROOM_PROFILE_SCHEMA_DENIED")
    tables = raw["profiles"]
    if type(tables) is not dict or tuple(tables) != _PROFILE_IDS:
        raise ValueError("EXACT_STOCKROOM_PROFILE_SET_REQUIRED")
    loaded: dict[str, LocalStockroomProfile] = {}
    issued_at = datetime(2026, 9, 9, tzinfo=UTC)
    for index, profile_id in enumerate(_PROFILE_IDS):
        data = tables[profile_id]
        if type(data) is not dict:
            raise ValueError("STOCKROOM_PROFILE_TABLE_REQUIRED")
        _exact_keys(data, _PROFILE_KEYS, profile_id)
        scenario_id = _string(data, "scenario_id")
        tool_allowed = _bool(data, "tool_dispatch_allowed")
        tools = _strings(data, "tool_allowlist", allow_empty=True)
        expected_tools = () if index == 2 else ("stockroom_summary",)
        maxima = {
            key: _positive_int(data, key)
            for key in _PROFILE_KEYS
            if key.endswith(("_maximum", "_bound")) or key.endswith("_seconds")
        }
        if (
            scenario_id != SCENARIO_IDS[index]
            or _string(data, "version") != "1"
            or _string(data, "provider_id") != "aiscc-local-deterministic"
            or _string(data, "adapter_protocol_version") != "stockroom-local-responses-v1"
            or _string(data, "endpoint_ref") != "local-in-process-stockroom-v1"
            or _string(data, "base_url") != "http://127.0.0.1:1/v1"
            or _string(data, "secret_ref") != LOCAL_COMPATIBILITY_SECRET_REF
            or _string(data, "tool_registry_id") != "aiscc-stockroom-tools"
            or _string(data, "tool_registry_version") != version
            or tools != expected_tools
            or tool_allowed != (index != 2)
            or maxima["provider_call_maximum"] != (1 if index == 2 else 2)
            or maxima["agent_round_trip_maximum"] != (1 if index == 2 else 2)
            or maxima["tool_call_maximum"] != 1
            or maxima["read_timeout_seconds"] > 2
            or maxima["total_timeout_seconds"] > 30
            or maxima["budget_unit_maximum"] > 4
            or maxima["continuation_item_maximum"] > 16
            or maxima["continuation_byte_bound"] > 16384
            or maxima["input_byte_bound"] > 16384
            or maxima["output_byte_bound"] > 8192
        ):
            raise ValueError("STOCKROOM_PROFILE_BINDING_DENIED")
        profile = ProviderProfile(
            profile_id=profile_id,
            version="1",
            provider_id="aiscc-local-deterministic",
            adapter_protocol_version="stockroom-local-responses-v1",
            model_ref=_string(data, "model_ref"),
            endpoint_ref="local-in-process-stockroom-v1",
            base_url="http://127.0.0.1:1/v1",
            secret_ref=LOCAL_COMPATIBILITY_SECRET_REF,
            allowed_runtime_modes=frozenset({RuntimeMode.OWNER_SELF_DOGFOOD}),
            scenario_allowlist=frozenset({scenario_id}),
            public_repository_identity=RESOURCE_REF.split("@", 1)[0],
            public_repository_version=RESOURCE_REF.split("@", 1)[1],
            public_scenario_identity=scenario_id,
            public_scenario_version="1.0.0",
            tool_registry_id="aiscc-stockroom-tools",
            tool_registry_version=version,
            tool_allowlist=frozenset(tools),
            provider_call_maximum=maxima["provider_call_maximum"],
            agent_round_trip_maximum=maxima["agent_round_trip_maximum"],
            tool_call_maximum=maxima["tool_call_maximum"],
            provider_retry_maximum=maxima["provider_retry_maximum"],
            connect_timeout_seconds=float(maxima["connect_timeout_seconds"]),
            read_timeout_seconds=float(maxima["read_timeout_seconds"]),
            total_timeout_seconds=float(maxima["total_timeout_seconds"]),
            output_token_bound=maxima["output_token_bound"],
            output_byte_bound=maxima["output_byte_bound"],
            input_byte_bound=maxima["input_byte_bound"],
            continuation_item_maximum=maxima["continuation_item_maximum"],
            continuation_byte_bound=maxima["continuation_byte_bound"],
            continuation_token_estimate_bound=maxima["continuation_token_estimate_bound"],
            budget_unit_maximum=maxima["budget_unit_maximum"],
            private_protocol_retention_policy_ref="private-protocol:stockroom-owner-v1",
            budget_policy_ref="application-budget:stockroom-owner-v1",
            data_classification_policy_ref="data-classification:stockroom-synthetic-v1",
            issued_at=issued_at,
            revoked_at=None,
            enabled=True,
        )
        loaded[profile_id] = LocalStockroomProfile(profile, scenario_id, tool_allowed)
    return MappingProxyType(loaded)


class LocalDeterministicProvider:
    def __init__(self, profiles: MappingProxyType[str, LocalStockroomProfile]) -> None:
        self._profiles = profiles
        self.invocation_count = 0

    def call(self, call: ProviderCall, *, secret: str) -> ProviderResult:
        local = self._profiles.get(call.profile.profile_id)
        if (
            local is None
            or call.profile != local.profile
            or call.runtime_mode is not RuntimeMode.OWNER_SELF_DOGFOOD
            or call.scenario_id != local.scenario_id
            or secret != LOCAL_COMPATIBILITY_SENTINEL
            or call.profile.secret_ref != LOCAL_COMPATIBILITY_SECRET_REF
            or call.profile.provider_id != "aiscc-local-deterministic"
            or call.profile.endpoint_ref != "local-in-process-stockroom-v1"
            or call.profile.adapter_protocol_version != "stockroom-local-responses-v1"
        ):
            raise ValueError("LOCAL_STOCKROOM_PROFILE_OR_SECRET_DENIED")
        input_bytes = canonical_json_bytes(list(call.input_items))
        if (
            len(call.input_items) > call.profile.continuation_item_maximum
            or len(input_bytes) > min(
                call.profile.input_byte_bound,
                call.profile.continuation_byte_bound,
                16384,
            )
        ):
            raise ValueError("LOCAL_STOCKROOM_INPUT_BOUND_DENIED")
        self.invocation_count += 1
        if call.scenario_id == "stockroom-s3-policy-conflict":
            if local.tool_dispatch_allowed or call.tools or _continuation_items(call.input_items):
                raise ValueError("S3_TOOL_OR_CONTINUATION_DENIED")
            return _final_result(
                call,
                {
                    "scenario_id": call.scenario_id,
                    "outcome": "POLICY_CONFLICT",
                    "baseline": "available <= reorder_level",
                    "requested_replacement": "available < reorder_level",
                    "external_llm_executed": False,
                },
            )

        expected_call_id = _call_id(call.execution_attempt_id, call.scenario_id)
        continuations = _continuation_items(call.input_items)
        if not continuations:
            tool_names = tuple(tool.get("name") for tool in call.tools)
            if not local.tool_dispatch_allowed or tool_names != ("stockroom_summary",):
                raise ValueError("STOCKROOM_TOOL_DEFINITION_REQUIRED")
            item = {
                "type": "function_call",
                "id": f"local-{expected_call_id}",
                "call_id": expected_call_id,
                "name": "stockroom_summary",
                "arguments": "{}",
            }
            return ProviderResult(
                call.operation_id,
                "completed",
                ExecutionOperationOutcome.PROVIDER_COMPLETED,
                None,
                (item,),
                None,
                ToolCallCandidate("stockroom_summary", "{}", expected_call_id),
                MappingProxyType({"output_tokens": 0}),
                None,
                canonical_sha256(item),
            )
        if len(continuations) != 2:
            raise ValueError("LOCAL_STOCKROOM_CONTINUATION_ORDER_DENIED")
        function_call, function_output = continuations
        if (
            function_call.get("type") != "function_call"
            or function_call.get("call_id") != expected_call_id
            or function_call.get("name") != "stockroom_summary"
            or function_call.get("arguments") != "{}"
            or function_output.get("type") != "function_call_output"
            or function_output.get("call_id") != expected_call_id
            or type(function_output.get("output")) is not str
            or parse_strict_json_object(str(function_output["output"])) != STOCKROOM_SUMMARY
        ):
            raise ValueError("LOCAL_STOCKROOM_CONTINUATION_BINDING_DENIED")
        return _final_result(
            call,
            {
                "scenario_id": call.scenario_id,
                "execution_backend_kind": "LOCAL_DETERMINISTIC_PROVIDER",
                "external_llm_executed": False,
                "summary": STOCKROOM_SUMMARY,
            },
        )


def _final_result(call: ProviderCall, disclosure: dict[str, object]) -> ProviderResult:
    text = json.dumps(disclosure, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    body = text.encode("ascii")
    if len(body) > min(call.profile.output_byte_bound, 8192):
        raise ValueError("LOCAL_STOCKROOM_OUTPUT_BOUND_DENIED")
    item: dict[str, Any] = {
        "type": "message",
        "role": "assistant",
        "content": [{"type": "output_text", "text": text}],
    }
    return ProviderResult(
        call.operation_id,
        "completed",
        ExecutionOperationOutcome.PROVIDER_COMPLETED,
        None,
        (item,),
        text,
        None,
        MappingProxyType({"output_tokens": (len(body) + 3) // 4}),
        None,
        canonical_sha256(item),
    )


def _continuation_items(items: tuple[dict[str, Any], ...]) -> tuple[dict[str, Any], ...]:
    allowed_initial = {"message", "input_text"}
    result: list[dict[str, Any]] = []
    started = False
    for item in items:
        item_type = item.get("type")
        if item_type in {"function_call", "function_call_output"}:
            started = True
            result.append(item)
        elif started or item_type not in allowed_initial:
            raise ValueError("LOCAL_STOCKROOM_UNEXPECTED_CONTINUATION_ITEM")
    return tuple(result)


def _call_id(attempt_id: str, scenario_id: str) -> str:
    return f"stockroom-{canonical_sha256({'attempt': attempt_id, 'scenario': scenario_id})[:24]}"


def _exact_keys(data: dict[str, Any], expected: set[str], owner: str) -> None:
    if set(data) != expected:
        raise ValueError(f"{owner} has unknown or missing keys")


def _string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if type(value) is not str or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _strings(data: dict[str, Any], key: str, *, allow_empty: bool) -> tuple[str, ...]:
    value = data.get(key)
    if (
        type(value) is not list
        or (not value and not allow_empty)
        or not all(type(item) is str for item in value)
    ):
        raise ValueError(f"{key} must be an exact string array")
    return tuple(value)


def _positive_int(data: dict[str, Any], key: str) -> int:
    value = data.get(key)
    if type(value) is not int or value <= 0:
        raise ValueError(f"{key} must be a positive integer")
    return value


def _bool(data: dict[str, Any], key: str) -> bool:
    value = data.get(key)
    if type(value) is not bool:
        raise ValueError(f"{key} must be boolean")
    return value
