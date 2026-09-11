"""Strict server-owned Stockroom composition with no execution behavior."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from pathlib import Path
from types import MappingProxyType

from aiscc.contracts.workflow import RuntimeMode
from aiscc.providers.local_deterministic import (
    LocalStockroomProfile,
    load_stockroom_owner_profiles,
)
from aiscc.providers.models import canonical_sha256
from aiscc.providers.stockroom_tool import StockroomToolConfig, load_stockroom_tool_config
from aiscc.scenarios.catalog import ScenarioCatalog, load_catalog
from aiscc.scenarios.driver import (
    PreparedStockroomDriver,
    StockroomConfigurationFingerprints,
    StockroomDriverRequest,
    StockroomOwnerDependencies,
    build_prepared_attempt_binding,
    build_stockroom_driver_request,
    prepare_stockroom_driver,
)
from aiscc.scenarios.enrollment import (
    StockroomEnrollment,
    StockroomOwnerContext,
    build_stockroom_owner_context,
    compile_stockroom_selection,
)
from aiscc.scenarios.models import RESOURCE_REF, SCENARIO_IDS
from aiscc.security.stockroom_policy import (
    StockroomOwnerPolicyConfig,
    load_stockroom_owner_policy,
)

_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_SERVER_CATALOG = _PROJECT_ROOT / "config/scenarios/stockroom/v1/catalog.json"
_SERVER_PROVIDER_PROFILES = _PROJECT_ROOT / "config/providers/stockroom-owner-profiles.v1.toml"
_SERVER_TOOL_CONFIG = _PROJECT_ROOT / "config/providers/stockroom-tools.v1.toml"
_SERVER_SECURITY_CONFIG = _PROJECT_ROOT / "config/security/stockroom-owner.v1.toml"
_PROFILE_IDS = (
    "stockroom-owner-s1-v1",
    "stockroom-owner-s2-v1",
    "stockroom-owner-s3-v1",
    "stockroom-owner-s4-v1",
)
_TOOL_SCENARIOS = (SCENARIO_IDS[0], SCENARIO_IDS[1], SCENARIO_IDS[3])
_TOOL_PROFILES = (_PROFILE_IDS[0], _PROFILE_IDS[1], _PROFILE_IDS[3])
_TOOL_IMAGE = (
    "aiscc-stockroom-runtime@sha256:"
    "be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d"
)
_PROFILE_TOTAL_TIMEOUT_MAX_SECONDS = 30


class StockroomCompositionError(ValueError):
    """Stable fail-closed configuration/composition denial."""

    code = "STOCKROOM_COMPOSITION_BINDING_DENIED"

    def __init__(self) -> None:
        super().__init__(self.code)


@dataclass(frozen=True, slots=True)
class StockroomOwnerComposition:
    catalog: ScenarioCatalog
    owner_context: StockroomOwnerContext
    provider_profiles: MappingProxyType[str, LocalStockroomProfile]
    tool_config: StockroomToolConfig
    security_config: StockroomOwnerPolicyConfig
    fingerprints: StockroomConfigurationFingerprints

    def enroll(self, scenario_id: str) -> StockroomEnrollment:
        return compile_stockroom_selection(
            {"scenario_id": scenario_id},
            catalog=self.catalog,
            owner_context=self.owner_context,
        )

    def request(
        self,
        *,
        scenario_id: str,
        run_id: str,
        attempt_id: str,
        expected_initial_state_version: int,
    ) -> StockroomDriverRequest:
        return build_stockroom_driver_request(
            self.enroll(scenario_id),
            run_id=run_id,
            attempt_id=attempt_id,
            expected_initial_state_version=expected_initial_state_version,
            configuration_fingerprints=self.fingerprints,
        )


@dataclass(frozen=True, slots=True)
class StockroomOwnerPreparation:
    composition: StockroomOwnerComposition
    owners: StockroomOwnerDependencies

    def request(
        self,
        *,
        scenario_id: str,
        run_id: str,
        attempt_id: str,
        expected_initial_state_version: int,
    ) -> StockroomDriverRequest:
        return self.composition.request(
            scenario_id=scenario_id,
            run_id=run_id,
            attempt_id=attempt_id,
            expected_initial_state_version=expected_initial_state_version,
        )

    def prepare(
        self,
        *,
        scenario_id: str,
        run_id: str,
        attempt_id: str,
        expected_initial_state_version: int,
    ) -> PreparedStockroomDriver:
        request = self.request(
            scenario_id=scenario_id,
            run_id=run_id,
            attempt_id=attempt_id,
            expected_initial_state_version=expected_initial_state_version,
        )
        attempt_binding = build_prepared_attempt_binding(request)
        return prepare_stockroom_driver(
            request,
            self.owners,
            attempt_binding=attempt_binding,
        )


def build_stockroom_owner_composition() -> StockroomOwnerComposition:
    """Load only the four fixed server configuration paths and cross-bind them."""
    try:
        catalog = load_catalog(_SERVER_CATALOG)
        profiles = load_stockroom_owner_profiles(_SERVER_PROVIDER_PROFILES)
        tool = load_stockroom_tool_config(_SERVER_TOOL_CONFIG)
        security = load_stockroom_owner_policy(_SERVER_SECURITY_CONFIG)
        context = build_stockroom_owner_context(catalog.scenarios)
        return _cross_bind(catalog, context, profiles, tool, security)
    except (OSError, TypeError, ValueError):
        raise StockroomCompositionError() from None


def bind_stockroom_owner_dependencies(
    composition: StockroomOwnerComposition,
    owners: StockroomOwnerDependencies,
) -> StockroomOwnerPreparation:
    if (
        type(composition) is not StockroomOwnerComposition
        or type(owners) is not StockroomOwnerDependencies
        or owners.stockroom_owner_restriction.config != composition.security_config
    ):
        raise ValueError("STOCKROOM_OWNER_DEPENDENCY_BINDING_DENIED")
    return StockroomOwnerPreparation(composition=composition, owners=owners)


def _cross_bind(
    catalog: ScenarioCatalog,
    context: StockroomOwnerContext,
    profiles: MappingProxyType[str, LocalStockroomProfile],
    tool: StockroomToolConfig,
    security: StockroomOwnerPolicyConfig,
) -> StockroomOwnerComposition:
    catalog_ids = tuple(item.scenario_id for item in catalog.scenarios)
    document_ids = tuple(item.scenario_id for item in catalog.document.scenarios)
    if (
        type(catalog) is not ScenarioCatalog
        or type(context) is not StockroomOwnerContext
        or type(profiles) is not MappingProxyType
        or type(tool) is not StockroomToolConfig
        or type(security) is not StockroomOwnerPolicyConfig
        or catalog_ids != SCENARIO_IDS
        or document_ids != SCENARIO_IDS
        or any(item.scenario_version != "1.0.0" for item in catalog.scenarios)
        or catalog.document.schema_version != "1.0.0"
        or catalog.document.resource_ref != RESOURCE_REF
        or catalog.resource.resource_ref != RESOURCE_REF
        or context.mode is not RuntimeMode.OWNER_SELF_DOGFOOD
        or context.resource_ref != RESOURCE_REF
        or context.provider_id != "aiscc-local-deterministic"
        or context.adapter_protocol_version != "stockroom-local-responses-v1"
        or context.execution_backend_kind != "LOCAL_DETERMINISTIC_PROVIDER"
        or context.external_llm_executed is not False
        or tuple(profiles) != _PROFILE_IDS
        or tuple(security.scenarios) != SCENARIO_IDS
    ):
        raise StockroomCompositionError()

    for index, scenario_id in enumerate(SCENARIO_IDS):
        binding = context.bindings[index]
        local = profiles[_PROFILE_IDS[index]]
        policy = security.scenarios[scenario_id]
        profile = local.profile
        expected_tool = index != 2
        if (
            binding.scenario is not catalog.scenarios[index]
            or binding.provider_profile_id != _PROFILE_IDS[index]
            or binding.provider_profile_version != "1"
            or (binding.tool_id is not None) != expected_tool
            or (binding.tool_action is not None) != expected_tool
            or local.scenario_id != scenario_id
            or local.tool_dispatch_allowed is not expected_tool
            or profile.profile_id != _PROFILE_IDS[index]
            or profile.version != "1"
            or profile.provider_id != "aiscc-local-deterministic"
            or profile.adapter_protocol_version != "stockroom-local-responses-v1"
            or profile.allowed_runtime_modes != frozenset({RuntimeMode.OWNER_SELF_DOGFOOD})
            or profile.scenario_allowlist != frozenset({scenario_id})
            or profile.tool_allowlist
            != (frozenset({"stockroom_summary"}) if expected_tool else frozenset())
            or profile.provider_call_maximum != policy.provider_call_limit
            or profile.agent_round_trip_maximum != policy.provider_call_limit
            or profile.tool_call_maximum != security.tool_calls
            or profile.read_timeout_seconds != security.provider_timeout_seconds
            or profile.total_timeout_seconds != security.attempt_timeout_seconds
            or profile.budget_unit_maximum != security.budget_units
            or policy.profile_id != _PROFILE_IDS[index]
            or policy.profile_version != "1"
            or policy.scenario_version != "1.0.0"
            or policy.tool_allowed is not expected_tool
        ):
            raise StockroomCompositionError()

    if (
        tool.registry_id != "aiscc-stockroom-tools"
        or tool.registry_version != "1"
        or tool.tool_id != "stockroom_summary"
        or tool.schema_version != "1"
        or tool.action != "fixed-stockroom-summary"
        or tool.dispatcher_version != "stockroom-summary-v1"
        or tool.process_resource_id != "process:stockroom-summary-v1"
        or tool.image != _TOOL_IMAGE
        or tool.network != "none"
        or tool.argv != ("python", "-B", "-m", "stockroom", "summary")
        or tool.workdir != "/workspace"
        or tool.stdout_limit_bytes != 4096
        or tool.stderr_limit_bytes != 4096
        or tool.output_byte_bound != 4096
        or tool.operation_timeout_seconds != security.process_timeout_seconds
        or tool.cleanup_timeout_seconds != security.cleanup_timeout_seconds
        or tool.attempt_timeout_seconds != security.attempt_timeout_seconds
        or tool.retry_maximum != 1
        or security.process_calls != 1
        or security.tool_calls != 1
        or security.provider_calls != 2
        or tuple(
            scenario_id
            for scenario_id in SCENARIO_IDS
            if security.scenarios[scenario_id].tool_allowed
        )
        != _TOOL_SCENARIOS
        or tuple(
            profile_id for profile_id in _PROFILE_IDS if profiles[profile_id].tool_dispatch_allowed
        )
        != _TOOL_PROFILES
    ):
        raise StockroomCompositionError()

    fingerprints = _fingerprints(catalog, profiles, tool, security)
    return StockroomOwnerComposition(
        catalog=catalog,
        owner_context=context,
        provider_profiles=profiles,
        tool_config=tool,
        security_config=security,
        fingerprints=fingerprints,
    )


def _fingerprints(
    catalog: ScenarioCatalog,
    profiles: MappingProxyType[str, LocalStockroomProfile],
    tool: StockroomToolConfig,
    security: StockroomOwnerPolicyConfig,
) -> StockroomConfigurationFingerprints:
    catalog_hash = canonical_sha256(
        {
            "schema": [catalog.document.schema_id, catalog.document.schema_version],
            "resource_ref": catalog.resource.resource_ref,
            "resource_manifest": catalog.resource.aggregate_sha256,
            "scenarios": [[item.scenario_id, item.scenario_version] for item in catalog.scenarios],
        }
    )
    provider_hash = canonical_sha256(
        {
            "runtime_mode": RuntimeMode.OWNER_SELF_DOGFOOD.value,
            "execution_backend_kind": "LOCAL_DETERMINISTIC_PROVIDER",
            "external_llm_executed": False,
            "profiles": [
                {
                    "profile_id": local.profile.profile_id,
                    "version": local.profile.version,
                    "scenario_id": local.scenario_id,
                    "provider_id": local.profile.provider_id,
                    "adapter_protocol_version": local.profile.adapter_protocol_version,
                    "model_ref": local.profile.model_ref,
                    "tool_registry": [
                        local.profile.tool_registry_id,
                        local.profile.tool_registry_version,
                    ],
                    "tool_allowlist": sorted(local.profile.tool_allowlist),
                    "limits": {
                        "provider_calls": local.profile.provider_call_maximum,
                        "rounds": local.profile.agent_round_trip_maximum,
                        "tool_calls": local.profile.tool_call_maximum,
                        "total_seconds": _canonical_profile_timeout_seconds(
                            local.profile.total_timeout_seconds
                        ),
                        "budget_units": local.profile.budget_unit_maximum,
                    },
                }
                for local in profiles.values()
            ],
        }
    )
    tool_hash = canonical_sha256(
        {
            "registry_id": tool.registry_id,
            "registry_version": tool.registry_version,
            "tool_id": tool.tool_id,
            "schema_version": tool.schema_version,
            "action": tool.action,
            "dispatcher_version": tool.dispatcher_version,
            "process_resource_id": tool.process_resource_id,
            "image": tool.image,
            "argv": list(tool.argv),
            "workdir": tool.workdir,
            "network": tool.network,
            "stdout_limit_bytes": tool.stdout_limit_bytes,
            "stderr_limit_bytes": tool.stderr_limit_bytes,
            "operation_timeout_seconds": tool.operation_timeout_seconds,
            "cleanup_timeout_seconds": tool.cleanup_timeout_seconds,
            "attempt_timeout_seconds": tool.attempt_timeout_seconds,
            "retry_maximum": tool.retry_maximum,
            "output_byte_bound": tool.output_byte_bound,
            "allowed_scenarios": list(_TOOL_SCENARIOS),
            "allowed_profiles": list(_TOOL_PROFILES),
            "model_visible_arguments": {},
        }
    )
    security_hash = canonical_sha256(
        {
            "schema_version": "stockroom-owner-v1",
            "default_effect": "DENY",
            "runtime_mode": RuntimeMode.OWNER_SELF_DOGFOOD.value,
            "resource_ref": RESOURCE_REF,
            "network": "DENY",
            "scenarios": [asdict(security.scenarios[item]) for item in SCENARIO_IDS],
            "limits": {
                "provider_calls": security.provider_calls,
                "tool_calls": security.tool_calls,
                "process_calls": security.process_calls,
                "provider_timeout_seconds": security.provider_timeout_seconds,
                "process_timeout_seconds": security.process_timeout_seconds,
                "cleanup_timeout_seconds": security.cleanup_timeout_seconds,
                "attempt_timeout_seconds": security.attempt_timeout_seconds,
                "budget_units": security.budget_units,
            },
        }
    )
    composition_hash = canonical_sha256(
        {
            "contract": "AISCC-STOCKROOM-OWNER-COMPOSITION-V1",
            "runtime_mode": RuntimeMode.OWNER_SELF_DOGFOOD.value,
            "resource_ref": RESOURCE_REF,
            "external_llm_executed": False,
            "components": [catalog_hash, provider_hash, tool_hash, security_hash],
        }
    )
    return StockroomConfigurationFingerprints(
        catalog_hash,
        provider_hash,
        tool_hash,
        security_hash,
        composition_hash,
    )


def _canonical_profile_timeout_seconds(value: float | int) -> int:
    if (
        type(value) not in (float, int)
        or value <= 0
        or value > _PROFILE_TOTAL_TIMEOUT_MAX_SECONDS
        or not math.isfinite(value)
        or (type(value) is float and not value.is_integer())
    ):
        raise StockroomCompositionError()
    return int(value)
