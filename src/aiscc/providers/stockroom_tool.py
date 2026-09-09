"""Strict Stockroom tool registry and receipt-aware fixed summary dispatcher."""

from __future__ import annotations

import hashlib
import tomllib
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from types import MappingProxyType
from typing import Any

from aiscc.contracts.security import ResourceDomain, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode
from aiscc.providers.local_deterministic import STOCKROOM_SUMMARY
from aiscc.providers.models import (
    ResourceRequirement,
    SideEffectClass,
    ToolDefinition,
    ToolOutputRef,
    ToolRegistry,
    canonical_sha256,
    parse_strict_json_object,
)
from aiscc.providers.tools import KnownToolFailure, ToolDispatchContext, UnknownToolOutcome
from aiscc.runtime.docker import DockerRunSpec, DockerRuntime, stockroom_spec_fingerprint
from aiscc.scenarios.models import RESOURCE_REF
from aiscc.security.capability import CapabilityConsumeRequest, CapabilityConsumptionReceipt

_ROOT_KEYS = {
    "schema_version",
    "default_effect",
    "registry_id",
    "registry_version",
    "tool",
}
_TOOL_KEYS = {
    "tool_id",
    "schema_version",
    "action",
    "dispatcher_version",
    "side_effect_classification",
    "allowed_scenarios",
    "allowed_profiles",
    "process_resource_id",
    "image",
    "argv",
    "workdir",
    "network",
    "stdout_limit_bytes",
    "stderr_limit_bytes",
    "operation_timeout_seconds",
    "cleanup_timeout_seconds",
    "attempt_timeout_seconds",
    "retry_maximum",
    "idempotency_policy",
    "output_byte_bound",
}
_SCENARIOS = (
    "stockroom-s1-normal",
    "stockroom-s2-missing-evidence",
    "stockroom-s4-human-owned-claim",
)
_PROFILES = (
    "stockroom-owner-s1-v1",
    "stockroom-owner-s2-v1",
    "stockroom-owner-s4-v1",
)
_IMAGE = (
    "aiscc-stockroom-runtime@sha256:"
    "be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d"
)


@dataclass(frozen=True, slots=True)
class StockroomToolConfig:
    registry_id: str
    registry_version: str
    tool_id: str
    schema_version: str
    action: str
    dispatcher_version: str
    process_resource_id: str
    image: str
    argv: tuple[str, ...]
    workdir: str
    network: str
    stdout_limit_bytes: int
    stderr_limit_bytes: int
    operation_timeout_seconds: int
    cleanup_timeout_seconds: int
    attempt_timeout_seconds: int
    retry_maximum: int
    output_byte_bound: int


def load_stockroom_tool_config(path: Path) -> StockroomToolConfig:
    with path.open("rb") as stream:
        raw = tomllib.load(stream)
    _exact_keys(raw, _ROOT_KEYS, "stockroom tool root")
    data = raw["tool"]
    if type(data) is not dict:
        raise ValueError("STOCKROOM_TOOL_TABLE_REQUIRED")
    _exact_keys(data, _TOOL_KEYS, "stockroom tool")
    integers = {
        key: _positive_int(data, key)
        for key in (
            "stdout_limit_bytes",
            "stderr_limit_bytes",
            "operation_timeout_seconds",
            "cleanup_timeout_seconds",
            "attempt_timeout_seconds",
            "retry_maximum",
            "output_byte_bound",
        )
    }
    if (
        raw["schema_version"] != "AISCC-STOCKROOM-TOOLS-V1"
        or raw["default_effect"] != "DENY"
        or raw["registry_id"] != "aiscc-stockroom-tools"
        or raw["registry_version"] != "1"
        or data["tool_id"] != "stockroom_summary"
        or data["schema_version"] != "1"
        or data["action"] != "fixed-stockroom-summary"
        or data["dispatcher_version"] != "stockroom-summary-v1"
        or data["side_effect_classification"] != "READ_ONLY"
        or tuple(data["allowed_scenarios"]) != _SCENARIOS
        or tuple(data["allowed_profiles"]) != _PROFILES
        or data["process_resource_id"] != "process:stockroom-summary-v1"
        or data["image"] != _IMAGE
        or data["argv"] != ["python", "-B", "-m", "stockroom", "summary"]
        or data["workdir"] != "/workspace"
        or data["network"] != "none"
        or integers != {
            "stdout_limit_bytes": 4096,
            "stderr_limit_bytes": 4096,
            "operation_timeout_seconds": 5,
            "cleanup_timeout_seconds": 10,
            "attempt_timeout_seconds": 30,
            "retry_maximum": 1,
            "output_byte_bound": 4096,
        }
        or data["idempotency_policy"] != "READ_ONLY_NO_RETRY_AFTER_DISPATCH"
    ):
        raise ValueError("STOCKROOM_TOOL_CONFIG_DENIED")
    return StockroomToolConfig(
        str(raw["registry_id"]),
        str(raw["registry_version"]),
        str(data["tool_id"]),
        str(data["schema_version"]),
        str(data["action"]),
        str(data["dispatcher_version"]),
        str(data["process_resource_id"]),
        str(data["image"]),
        tuple(str(item) for item in data["argv"]),
        str(data["workdir"]),
        str(data["network"]),
        integers["stdout_limit_bytes"],
        integers["stderr_limit_bytes"],
        integers["operation_timeout_seconds"],
        integers["cleanup_timeout_seconds"],
        integers["attempt_timeout_seconds"],
        integers["retry_maximum"],
        integers["output_byte_bound"],
    )


def build_stockroom_spec(
    config: StockroomToolConfig,
    *,
    name: str,
    run_id: str,
    workspace: Path,
) -> DockerRunSpec:
    return DockerRunSpec(
        name=name,
        run_id=run_id,
        resource_id=config.process_resource_id,
        image=config.image,
        command=config.argv,
        workspace=workspace,
        network=config.network,
        workdir=config.workdir,
        stdout_limit_bytes=config.stdout_limit_bytes,
        stderr_limit_bytes=config.stderr_limit_bytes,
        operation_timeout_seconds=config.operation_timeout_seconds,
        cleanup_timeout_seconds=config.cleanup_timeout_seconds,
        attempt_timeout_seconds=config.attempt_timeout_seconds,
    )


def build_stockroom_registry(config: StockroomToolConfig, spec: DockerRunSpec) -> ToolRegistry:
    stockroom_spec_fingerprint(spec)
    definition = ToolDefinition(
        tool_id=config.tool_id,
        schema_version=config.schema_version,
        dispatcher_version=config.dispatcher_version,
        description="Return the fixed deterministic Stockroom summary.",
        input_schema={"type": "object", "additionalProperties": False, "required": []},
        side_effect_classification=SideEffectClass.READ_ONLY,
        allowed_modes=frozenset({RuntimeMode.OWNER_SELF_DOGFOOD}),
        allowed_profiles=frozenset(_PROFILES),
        allowed_scenarios=frozenset(_SCENARIOS),
        underlying_resource_requirements=(
            ResourceRequirement(spec.scope(), SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT),
        ),
        secret_requirement=None,
        timeout_seconds=float(config.operation_timeout_seconds),
        retry_maximum=config.retry_maximum,
        idempotency_policy="READ_ONLY_NO_RETRY_AFTER_DISPATCH",
        output_byte_bound=config.output_byte_bound,
        output_schema=_output_schema(),
        enabled=True,
        issued_at=datetime(2026, 9, 9, tzinfo=UTC),
        revoked_at=None,
    )
    return ToolRegistry(
        config.registry_id,
        config.registry_version,
        MappingProxyType({config.tool_id: definition}),
    )


def build_dispatch_context(
    *,
    run_id: str,
    attempt_id: str,
    state_version: int,
    scenario_id: str,
    profile_id: str,
    provider_operation_id: str,
    provider_call_id: str,
    spec: DockerRunSpec,
) -> ToolDispatchContext:
    return ToolDispatchContext(
        task_action="fixed-stockroom-summary",
        work_run_id=run_id,
        execution_attempt_id=attempt_id,
        state="RUNNING",
        state_version=state_version,
        runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD.value,
        scenario_id=scenario_id,
        scenario_version="1.0.0",
        profile_id=profile_id,
        profile_version="1",
        resource_ref=RESOURCE_REF,
        provider_operation_id=provider_operation_id,
        provider_call_id=provider_call_id,
        resolved_spec_fingerprint=stockroom_spec_fingerprint(spec),
    )


class StockroomSummaryDispatcher:
    def __init__(self, runtime: DockerRuntime, spec: DockerRunSpec) -> None:
        self._runtime = runtime
        self._spec = spec
        self._spec_fingerprint = stockroom_spec_fingerprint(spec)
        self.invocation_count = 0

    def dispatch(self, *args: object, **kwargs: object) -> ToolOutputRef:
        del args, kwargs
        raise ValueError("STOCKROOM_LEGACY_DISPATCH_DENIED")

    def dispatch_with_receipts(
        self,
        definition: ToolDefinition,
        arguments: dict[str, object],
        *,
        receipts: tuple[CapabilityConsumptionReceipt, ...],
        requirements: tuple[CapabilityConsumeRequest, ...],
        dispatch_identity: str,
    ) -> ToolOutputRef:
        if arguments != {} or definition.dispatcher_version != "stockroom-summary-v1":
            raise KnownToolFailure("STOCKROOM_ARGUMENT_OR_DISPATCHER_DENIED")
        if len(receipts) != len(requirements):
            raise UnknownToolOutcome("STOCKROOM_PROCESS_RECEIPT_UNRESOLVED")
        pairs = [
            (receipt, requirement)
            for receipt, requirement in zip(receipts, requirements, strict=True)
            if requirement.scope.domain is ResourceDomain.PROCESS
        ]
        if len(pairs) != 1 or len(dispatch_identity) != 64:
            raise UnknownToolOutcome("STOCKROOM_PROCESS_RECEIPT_UNRESOLVED")
        receipt, requirement = pairs[0]
        result = self._runtime.run_consumed_stockroom(
            receipt,
            requirement,
            spec=self._spec,
            dispatch_identity=dispatch_identity,
        )
        if result.tool_outcome == "UNKNOWN_TOOL_OUTCOME":
            raise UnknownToolOutcome("STOCKROOM_PROCESS_OUTCOME_UNKNOWN")
        if result.tool_outcome != "KNOWN_TOOL_COMPLETED" or result.exit_code != 0:
            raise KnownToolFailure("STOCKROOM_PROCESS_KNOWN_FAILURE")
        if (
            result.stderr != ""
            or not result.stdout.endswith("\n")
            or result.stdout.count("\n") != 1
        ):
            raise KnownToolFailure("STOCKROOM_OUTPUT_STREAM_CONTRACT_DENIED")
        try:
            output = parse_strict_json_object(result.stdout[:-1])
        except (UnicodeError, ValueError) as exc:
            raise KnownToolFailure("STOCKROOM_OUTPUT_JSON_DENIED") from exc
        if output != STOCKROOM_SUMMARY:
            raise KnownToolFailure("STOCKROOM_OUTPUT_VALUE_DENIED")
        self.invocation_count += 1
        return ToolOutputRef(
            output_id=f"stockroom-output-{hashlib.sha256(dispatch_identity.encode()).hexdigest()[:24]}",
            operation_id=dispatch_identity,
            argument_hash=requirement.operation_fingerprint or "",
            result_hash=canonical_sha256(output),
            output=output,
        )


def _output_schema() -> dict[str, Any]:
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


def _exact_keys(data: dict[str, Any], expected: set[str], owner: str) -> None:
    if set(data) != expected:
        raise ValueError(f"{owner} unknown or missing key")


def _positive_int(data: dict[str, Any], key: str) -> int:
    value = data.get(key)
    if type(value) is not int or value <= 0:
        raise ValueError(f"{key} must be a positive integer")
    return value
