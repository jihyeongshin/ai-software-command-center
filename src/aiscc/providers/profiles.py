from __future__ import annotations

import tomllib
from datetime import datetime
from pathlib import Path
from types import MappingProxyType
from typing import Any

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode
from aiscc.providers.models import (
    ProviderProfile,
    ResourceRequirement,
    SecretRequirement,
    SideEffectClass,
    ToolDefinition,
    ToolRegistry,
)


def load_provider_profile(path: Path, profile_id: str) -> ProviderProfile:
    raw = _load(path)
    profiles = _table(raw, "profiles")
    data = _table(profiles, profile_id)
    modes = frozenset(RuntimeMode(item) for item in _strings(data, "allowed_runtime_modes"))
    profile = ProviderProfile(
        profile_id=profile_id,
        version=_string(data, "version"),
        provider_id=_string(data, "provider_id"),
        adapter_protocol_version=_string(data, "adapter_protocol_version"),
        model_ref=_string(data, "model_ref"),
        endpoint_ref=_string(data, "endpoint_ref"),
        base_url=_string(data, "base_url"),
        secret_ref=_string(data, "secret_ref"),
        allowed_runtime_modes=modes,
        scenario_allowlist=frozenset(_strings(data, "scenario_allowlist")),
        public_repository_identity=_string(data, "public_repository_identity"),
        public_repository_version=_string(data, "public_repository_version"),
        public_scenario_identity=_string(data, "public_scenario_identity"),
        public_scenario_version=_string(data, "public_scenario_version"),
        tool_registry_id=_string(data, "tool_registry_id"),
        tool_registry_version=_string(data, "tool_registry_version"),
        tool_allowlist=frozenset(_strings(data, "tool_allowlist")),
        provider_call_maximum=_positive_int(data, "provider_call_maximum"),
        agent_round_trip_maximum=_positive_int(data, "agent_round_trip_maximum"),
        tool_call_maximum=_positive_int(data, "tool_call_maximum"),
        provider_retry_maximum=_positive_int(data, "provider_retry_maximum"),
        connect_timeout_seconds=float(_positive_int(data, "connect_timeout_seconds")),
        read_timeout_seconds=float(_positive_int(data, "read_timeout_seconds")),
        total_timeout_seconds=float(_positive_int(data, "total_timeout_seconds")),
        output_token_bound=_positive_int(data, "output_token_bound"),
        output_byte_bound=_positive_int(data, "output_byte_bound"),
        input_byte_bound=_positive_int(data, "input_byte_bound"),
        continuation_item_maximum=_positive_int(data, "continuation_item_maximum"),
        continuation_byte_bound=_positive_int(data, "continuation_byte_bound"),
        continuation_token_estimate_bound=_positive_int(data, "continuation_token_estimate_bound"),
        budget_unit_maximum=_positive_int(data, "budget_unit_maximum"),
        private_protocol_retention_policy_ref=_string(
            data, "private_protocol_retention_policy_ref"
        ),
        budget_policy_ref=_string(data, "budget_policy_ref"),
        data_classification_policy_ref=_string(data, "data_classification_policy_ref"),
        issued_at=_datetime(data, "issued_at"),
        revoked_at=_optional_datetime(data, "revoked_at"),
        enabled=_boolean(data, "enabled"),
    )
    if (
        not profile.enabled
        or not profile.base_url.startswith("http://127.0.0.1:")
        or profile.public_scenario_identity not in profile.scenario_allowlist
    ):
        raise ValueError("P1-5 acceptance profile must be enabled and local-only")
    return profile


def load_tool_registry(path: Path) -> ToolRegistry:
    raw = _load(path)
    registry_id = _string(raw, "registry_id")
    version = _string(raw, "version")
    entries = _table(raw, "tools")
    tools: dict[str, ToolDefinition] = {}
    for tool_id, untyped in entries.items():
        if not isinstance(untyped, dict):
            raise ValueError("tool definition must be a table")
        schema = _table(untyped, "input_schema")
        if schema.get("additionalProperties") is not False:
            raise ValueError("tool schema must reject additional properties")
        requirements = tuple(
            _resource_requirement(item)
            for item in _optional_tables(untyped, "underlying_resource_requirements")
        )
        secret_data = untyped.get("secret_requirement")
        secret_requirement = (
            SecretRequirement(
                secret_ref=_string(secret_data, "secret_ref"),
                secret_class=_string(secret_data, "secret_class"),
                purpose=_string(secret_data, "purpose"),
                destination=_string(secret_data, "destination"),
                dispatcher_identity=_string(secret_data, "dispatcher_identity"),
            )
            if isinstance(secret_data, dict)
            else None
        )
        tools[tool_id] = ToolDefinition(
            tool_id=tool_id,
            schema_version=_string(untyped, "schema_version"),
            dispatcher_version=_string(untyped, "dispatcher_version"),
            description=_string(untyped, "description"),
            input_schema=dict(schema),
            side_effect_classification=SideEffectClass(
                _string(untyped, "side_effect_classification")
            ),
            allowed_modes=frozenset(
                RuntimeMode(item) for item in _strings(untyped, "allowed_runtime_modes")
            ),
            allowed_profiles=frozenset(_strings(untyped, "allowed_profiles")),
            allowed_scenarios=frozenset(_strings(untyped, "allowed_scenarios")),
            underlying_resource_requirements=requirements,
            secret_requirement=secret_requirement,
            timeout_seconds=float(_positive_int(untyped, "timeout_seconds")),
            retry_maximum=_positive_int(untyped, "retry_maximum"),
            idempotency_policy=_string(untyped, "idempotency_policy"),
            output_byte_bound=_positive_int(untyped, "output_byte_bound"),
            output_schema=dict(_table(untyped, "output_schema")),
            enabled=_boolean(untyped, "enabled"),
            issued_at=_datetime(untyped, "issued_at"),
            revoked_at=_optional_datetime(untyped, "revoked_at"),
        )
    return ToolRegistry(registry_id, version, MappingProxyType(tools))


def _load(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        value = tomllib.load(stream)
    return value


def _table(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ValueError(f"{key} table is required")
    return value


def _string(data: dict[str, Any], key: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"{key} must be a non-empty string")
    return value


def _strings(data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or not value or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{key} must be a non-empty string array")
    return value


def _optional_strings(data: dict[str, Any], key: str) -> list[str]:
    value = data.get(key, [])
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{key} must be a string array")
    return value


def _optional_tables(data: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = data.get(key, [])
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        raise ValueError(f"{key} must be an array of tables")
    return value


def _resource_requirement(data: dict[str, Any]) -> ResourceRequirement:
    scope = ResourceScope(
        domain=ResourceDomain(_string(data, "domain")),
        resource_id=_string(data, "resource_id"),
        image=data.get("image") if isinstance(data.get("image"), str) else None,
        argv=tuple(_optional_strings(data, "argv")),
        workspace_path=(
            data.get("workspace_path") if isinstance(data.get("workspace_path"), str) else None
        ),
        network_name=(
            data.get("network_name") if isinstance(data.get("network_name"), str) else None
        ),
        target_name=(data.get("target_name") if isinstance(data.get("target_name"), str) else None),
    )
    return ResourceRequirement(scope, SecurityActionClass(_string(data, "action")))


def _positive_int(data: dict[str, Any], key: str) -> int:
    value = data.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(f"{key} must be a positive integer")
    return value


def _boolean(data: dict[str, Any], key: str) -> bool:
    value = data.get(key)
    if not isinstance(value, bool):
        raise ValueError(f"{key} must be boolean")
    return value


def _datetime(data: dict[str, Any], key: str) -> datetime:
    value = data.get(key)
    if not isinstance(value, str):
        raise ValueError(f"{key} must be an RFC 3339 string")
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _optional_datetime(data: dict[str, Any], key: str) -> datetime | None:
    if key not in data:
        return None
    return _datetime(data, key)
