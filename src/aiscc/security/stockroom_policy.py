"""Mandatory sealed owner restriction for the four Stockroom scenarios."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.scenarios.models import RESOURCE_REF, SCENARIO_IDS

_PROFILE_IDS = (
    "stockroom-owner-s1-v1",
    "stockroom-owner-s2-v1",
    "stockroom-owner-s3-v1",
    "stockroom-owner-s4-v1",
)
_ROOT_KEYS = {
    "schema_version",
    "default_effect",
    "runtime_mode",
    "resource_ref",
    "tool_id",
    "tool_action",
    "network",
    "scenarios",
    "limits",
    "ownership",
}
_SCENARIO_KEYS = {
    "scenario_version",
    "profile_id",
    "profile_version",
    "tool_allowed",
    "provider_call_limit",
}
_LIMIT_KEYS = {
    "provider_calls",
    "tool_calls",
    "process_calls",
    "provider_timeout_seconds",
    "process_timeout_seconds",
    "cleanup_timeout_seconds",
    "attempt_timeout_seconds",
    "budget_units",
}
_OWNERSHIP_KEYS = {"runtime_root", "materialized_resource", "capability_lease"}


@dataclass(frozen=True, slots=True)
class StockroomScenarioPolicy:
    scenario_id: str
    scenario_version: str
    profile_id: str
    profile_version: str
    tool_allowed: bool
    provider_call_limit: int


@dataclass(frozen=True, slots=True)
class StockroomOwnerPolicyConfig:
    scenarios: MappingProxyType[str, StockroomScenarioPolicy]
    provider_calls: int
    tool_calls: int
    process_calls: int
    provider_timeout_seconds: int
    process_timeout_seconds: int
    cleanup_timeout_seconds: int
    attempt_timeout_seconds: int
    budget_units: int


@dataclass(frozen=True, slots=True)
class StockroomSecurityContext:
    context_id: str
    principal: str
    task_action: str
    mode: RuntimeMode
    scenario_id: str
    scenario_version: str
    profile_id: str
    profile_version: str
    run_id: str
    attempt_id: str
    state: WorkflowState
    state_version: int
    resource_ref: str
    security_action: SecurityActionClass
    scope: ResourceScope
    operation_fingerprint: str
    enrolled_tool_id: str | None
    enrolled_tool_action: str | None
    process_spec_fingerprint: str
    remaining_provider_calls: int
    remaining_tool_calls: int
    remaining_process_calls: int
    remaining_seconds: int
    remaining_budget_units: int
    repository_capability_ref: str
    filesystem_capability_ref: str
    process_capability_ref: str
    materialized_resource_owner_ref: str
    runtime_root_owner_ref: str
    network_requested: bool
    _issuer_token: object = field(repr=False, compare=False)


def load_stockroom_owner_policy(path: Path) -> StockroomOwnerPolicyConfig:
    with path.open("rb") as stream:
        raw = tomllib.load(stream)
    _exact_keys(raw, _ROOT_KEYS, "stockroom owner root")
    if (
        raw["schema_version"] != "stockroom-owner-v1"
        or raw["default_effect"] != "DENY"
        or raw["runtime_mode"] != RuntimeMode.OWNER_SELF_DOGFOOD.value
        or raw["resource_ref"] != RESOURCE_REF
        or raw["tool_id"] != "stockroom_summary"
        or raw["tool_action"] != "fixed-stockroom-summary"
        or raw["network"] != "DENY"
    ):
        raise ValueError("STOCKROOM_OWNER_SCHEMA_DENIED")
    scenario_tables = raw["scenarios"]
    if type(scenario_tables) is not dict or tuple(scenario_tables) != SCENARIO_IDS:
        raise ValueError("EXACT_STOCKROOM_SCENARIO_POLICY_SET_REQUIRED")
    scenarios: dict[str, StockroomScenarioPolicy] = {}
    for index, scenario_id in enumerate(SCENARIO_IDS):
        data = scenario_tables[scenario_id]
        if type(data) is not dict:
            raise ValueError("STOCKROOM_SCENARIO_POLICY_TABLE_REQUIRED")
        _exact_keys(data, _SCENARIO_KEYS, scenario_id)
        if (
            data["scenario_version"] != "1.0.0"
            or data["profile_id"] != _PROFILE_IDS[index]
            or data["profile_version"] != "1"
            or type(data["tool_allowed"]) is not bool
            or data["tool_allowed"] != (index != 2)
            or type(data["provider_call_limit"]) is not int
            or data["provider_call_limit"] != (1 if index == 2 else 2)
        ):
            raise ValueError("STOCKROOM_SCENARIO_POLICY_BINDING_DENIED")
        scenarios[scenario_id] = StockroomScenarioPolicy(
            scenario_id,
            "1.0.0",
            _PROFILE_IDS[index],
            "1",
            index != 2,
            1 if index == 2 else 2,
        )
    limits = raw["limits"]
    ownership = raw["ownership"]
    if type(limits) is not dict or type(ownership) is not dict:
        raise ValueError("STOCKROOM_LIMIT_AND_OWNERSHIP_TABLES_REQUIRED")
    _exact_keys(limits, _LIMIT_KEYS, "limits")
    _exact_keys(ownership, _OWNERSHIP_KEYS, "ownership")
    expected = {
        "provider_calls": 2,
        "tool_calls": 1,
        "process_calls": 1,
        "provider_timeout_seconds": 2,
        "process_timeout_seconds": 5,
        "cleanup_timeout_seconds": 10,
        "attempt_timeout_seconds": 30,
        "budget_units": 4,
    }
    if any(type(limits[key]) is not int or limits[key] != value for key, value in expected.items()):
        raise ValueError("STOCKROOM_FINITE_LIMIT_BINDING_DENIED")
    if ownership != {
        "runtime_root": "SERVER_ISSUED_ONLY",
        "materialized_resource": "SERVER_ISSUED_ONLY",
        "capability_lease": "CURRENT_REQUIRED",
    }:
        raise ValueError("STOCKROOM_OWNERSHIP_BINDING_DENIED")
    return StockroomOwnerPolicyConfig(
        MappingProxyType(scenarios),
        **{key: int(limits[key]) for key in expected},
    )


class StockroomOwnerRestriction:
    """Seals exact owner composition; it never issues a capability or ALLOW."""

    def __init__(self, config: StockroomOwnerPolicyConfig) -> None:
        self.config = config
        self._issuer_token = object()
        self._contexts: dict[str, StockroomSecurityContext] = {}

    def seal_context(
        self,
        *,
        context_id: str,
        principal: str,
        task_action: str,
        mode: RuntimeMode,
        scenario_id: str,
        profile_id: str,
        run_id: str,
        attempt_id: str,
        state: WorkflowState,
        state_version: int,
        security_action: SecurityActionClass,
        scope: ResourceScope,
        operation_fingerprint: str,
        process_spec_fingerprint: str,
        remaining_provider_calls: int,
        remaining_tool_calls: int,
        remaining_process_calls: int,
        remaining_seconds: int,
        remaining_budget_units: int,
        repository_capability_ref: str,
        filesystem_capability_ref: str,
        process_capability_ref: str,
        materialized_resource_owner_ref: str,
        runtime_root_owner_ref: str,
        network_requested: bool = False,
    ) -> StockroomSecurityContext:
        scenario = self.config.scenarios.get(scenario_id)
        tool_id = "stockroom_summary" if scenario is not None and scenario.tool_allowed else None
        tool_action = "fixed-stockroom-summary" if tool_id is not None else None
        context = StockroomSecurityContext(
            context_id=context_id,
            principal=principal,
            task_action=task_action,
            mode=mode,
            scenario_id=scenario_id,
            scenario_version="1.0.0",
            profile_id=profile_id,
            profile_version="1",
            run_id=run_id,
            attempt_id=attempt_id,
            state=state,
            state_version=state_version,
            resource_ref=RESOURCE_REF,
            security_action=security_action,
            scope=scope,
            operation_fingerprint=operation_fingerprint,
            enrolled_tool_id=tool_id,
            enrolled_tool_action=tool_action,
            process_spec_fingerprint=process_spec_fingerprint,
            remaining_provider_calls=remaining_provider_calls,
            remaining_tool_calls=remaining_tool_calls,
            remaining_process_calls=remaining_process_calls,
            remaining_seconds=remaining_seconds,
            remaining_budget_units=remaining_budget_units,
            repository_capability_ref=repository_capability_ref,
            filesystem_capability_ref=filesystem_capability_ref,
            process_capability_ref=process_capability_ref,
            materialized_resource_owner_ref=materialized_resource_owner_ref,
            runtime_root_owner_ref=runtime_root_owner_ref,
            network_requested=network_requested,
            _issuer_token=self._issuer_token,
        )
        if context_id in self._contexts:
            raise ValueError("STOCKROOM_CONTEXT_ID_ALREADY_ISSUED")
        self._contexts[context_id] = context
        return context

    def allows(
        self,
        context: object,
        *,
        mode: RuntimeMode,
        scenario_id: str | None,
        action: SecurityActionClass,
        scope: ResourceScope,
        principal: str,
        run_id: str,
        operation_fingerprint: str | None,
    ) -> bool:
        if type(context) is not StockroomSecurityContext:
            return False
        scenario = self.config.scenarios.get(context.scenario_id)
        expected_action = (
            "compare-fixed-synthetic-policies"
            if context.scenario_id == "stockroom-s3-policy-conflict"
            else "fixed-stockroom-summary"
        )
        common = bool(
            context._issuer_token is self._issuer_token
            and self._contexts.get(context.context_id) is context
            and scenario is not None
            and mode is context.mode is RuntimeMode.OWNER_SELF_DOGFOOD
            and scenario_id == context.scenario_id
            and context.scenario_version == scenario.scenario_version
            and context.profile_id == scenario.profile_id
            and context.profile_version == scenario.profile_version
            and context.principal == principal
            and context.run_id == run_id
            and context.attempt_id
            and context.state is WorkflowState.RUNNING
            and type(context.state_version) is int
            and context.state_version > 0
            and context.resource_ref == RESOURCE_REF
            and context.task_action == expected_action
            and context.security_action is action
            and context.scope == scope
            and context.operation_fingerprint == operation_fingerprint
            and _sha256(context.operation_fingerprint)
            and _sha256(context.process_spec_fingerprint)
            and context.network_requested is False
            and 0 < context.remaining_provider_calls <= scenario.provider_call_limit
            and 0 < context.remaining_tool_calls <= self.config.tool_calls
            and 0 < context.remaining_process_calls <= self.config.process_calls
            and context.remaining_seconds > 0
            and context.remaining_seconds <= self.config.attempt_timeout_seconds
            and context.remaining_budget_units > 0
            and context.remaining_budget_units <= self.config.budget_units
            and all(
                _authority_ref(value)
                for value in (
                    context.repository_capability_ref,
                    context.filesystem_capability_ref,
                    context.process_capability_ref,
                    context.materialized_resource_owner_ref,
                    context.runtime_root_owner_ref,
                )
            )
        )
        if not common or scope.domain is ResourceDomain.NETWORK:
            return False
        if scope.domain is ResourceDomain.PROVIDER:
            return 0 < context.remaining_provider_calls <= scenario.provider_call_limit
        if scope.domain is ResourceDomain.TOOL:
            return bool(
                scenario.tool_allowed
                and context.enrolled_tool_id == "stockroom_summary"
                and context.enrolled_tool_action == "fixed-stockroom-summary"
                and 0 < context.remaining_tool_calls <= self.config.tool_calls
            )
        if scope.domain is ResourceDomain.PROCESS:
            return bool(
                scenario.tool_allowed
                and context.enrolled_tool_id == "stockroom_summary"
                and 0 < context.remaining_process_calls <= self.config.process_calls
            )
        if scope.domain is ResourceDomain.SECRET:
            return context.remaining_provider_calls > 0
        return scope.domain in {
            ResourceDomain.REPOSITORY,
            ResourceDomain.FILESYSTEM,
            ResourceDomain.SCENARIO,
        }


def _exact_keys(data: dict[str, Any], expected: set[str], owner: str) -> None:
    if set(data) != expected:
        raise ValueError(f"{owner} unknown or missing key")


def _sha256(value: str | None) -> bool:
    return bool(
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _authority_ref(value: str) -> bool:
    return (
        type(value) is str
        and 1 <= len(value) <= 200
        and not any(char.isspace() for char in value)
    )
