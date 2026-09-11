from __future__ import annotations

import inspect
import json
import shutil
from dataclasses import FrozenInstanceError, dataclass, replace
from pathlib import Path

import pytest

import aiscc.bootstrap as bootstrap
import aiscc.scenarios.composition as composition_module
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.evidence.service import EvidenceAdmissionService
from aiscc.human.repository import PostgresHumanAuthorityRepository
from aiscc.judgment.authority import PostgresJudgmentAuthority
from aiscc.runtime.stockroom_workspace import StockroomWorkspace
from aiscc.scenarios.composition import (
    StockroomCompositionError,
    bind_stockroom_owner_dependencies,
    build_stockroom_owner_composition,
    build_stockroom_production_composition,
)
from aiscc.scenarios.driver import (
    PreparedStockroomDriver,
    StockroomOwnerDependencies,
    build_prepared_attempt_binding,
)
from aiscc.scenarios.models import RESOURCE_REF, SCENARIO_IDS
from aiscc.security.policy import SecurityPolicy, default_profiles
from aiscc.security.stockroom_policy import StockroomOwnerRestriction
from aiscc.workflow.kernel import WorkflowKernel
from tests.unit.runtime.test_stockroom_image import synthetic_image

ROOT = Path(__file__).resolve().parents[3]
PROFILE_IDS = (
    "stockroom-owner-s1-v1",
    "stockroom-owner-s2-v1",
    "stockroom-owner-s3-v1",
    "stockroom-owner-s4-v1",
)


def test_v2_composition_fingerprint_binds_admitted_image(tmp_path, monkeypatch):
    first, *_ = synthetic_image(tmp_path, monkeypatch)
    composed = build_stockroom_production_composition(first)
    second, *_ = synthetic_image(tmp_path, monkeypatch, "b" * 64)
    other = build_stockroom_production_composition(second)
    assert composed.fingerprints.composition_sha256 != other.fingerprints.composition_sha256
    assert composed.fingerprints.tool_config_sha256 != other.fingerprints.tool_config_sha256
    assert composed.fingerprints.catalog_sha256 == other.fingerprints.catalog_sha256
    assert composed.fingerprints.security_config_sha256 == other.fingerprints.security_config_sha256
    assert composed.tool_config.registry_version == "2"
    assert build_stockroom_owner_composition().tool_config.registry_version == "1"
    with pytest.raises(ValueError):
        build_stockroom_production_composition(second.provenance)


@dataclass(frozen=True, slots=True)
class _FactoryAuthority:
    semantic_role: str
    factory_ref: str
    factory_fingerprint: str


def _factories() -> tuple[_FactoryAuthority, _FactoryAuthority]:
    return (
        _FactoryAuthority(
            "STOCKROOM_MATERIALIZER_FACTORY",
            "unit-materializer-factory",
            "1" * 64,
        ),
        _FactoryAuthority(
            "STOCKROOM_AGENT_EXECUTION_SERVICE_FACTORY",
            "unit-execution-factory",
            "2" * 64,
        ),
    )


def _owners(composition: object) -> StockroomOwnerDependencies:
    security_config = composition.security_config  # type: ignore[attr-defined]
    restriction = StockroomOwnerRestriction(security_config)
    materializer_factory, execution_factory = _factories()
    return StockroomOwnerDependencies(
        workflow_kernel=object.__new__(WorkflowKernel),
        agent_execution_service_factory=execution_factory,
        evidence_admission_service=object.__new__(EvidenceAdmissionService),
        human_gate_owner=object.__new__(PostgresHumanAuthorityRepository),
        judgment_owner=object.__new__(PostgresJudgmentAuthority),
        workspace_owner=object.__new__(StockroomWorkspace),
        materializer_factory=materializer_factory,
        security_policy=SecurityPolicy(default_profiles(), stockroom_policy=restriction),
        stockroom_owner_restriction=restriction,
    )


def _temporary_configs(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    scenario_root = tmp_path / "stockroom"
    shutil.copytree(ROOT / "config/scenarios/stockroom/v1", scenario_root)
    paths = {
        "catalog": scenario_root / "catalog.json",
        "profiles": tmp_path / "profiles.toml",
        "tool": tmp_path / "tool.toml",
        "security": tmp_path / "security.toml",
    }
    shutil.copy2(ROOT / "config/providers/stockroom-owner-profiles.v1.toml", paths["profiles"])
    shutil.copy2(ROOT / "config/providers/stockroom-tools.v1.toml", paths["tool"])
    shutil.copy2(ROOT / "config/security/stockroom-owner.v1.toml", paths["security"])
    monkeypatch.setattr(composition_module, "_SERVER_CATALOG", paths["catalog"])
    monkeypatch.setattr(composition_module, "_SERVER_PROVIDER_PROFILES", paths["profiles"])
    monkeypatch.setattr(composition_module, "_SERVER_TOOL_CONFIG", paths["tool"])
    monkeypatch.setattr(composition_module, "_SERVER_SECURITY_CONFIG", paths["security"])
    return paths


def test_canonical_owner_configuration_cross_binds_exactly() -> None:
    composed = build_stockroom_owner_composition()
    assert tuple(item.scenario_id for item in composed.catalog.scenarios) == SCENARIO_IDS
    assert tuple(composed.provider_profiles) == PROFILE_IDS
    assert composed.catalog.resource.resource_ref == RESOURCE_REF
    assert composed.owner_context.resource_ref == RESOURCE_REF
    assert composed.owner_context.mode is RuntimeMode.OWNER_SELF_DOGFOOD
    assert composed.owner_context.external_llm_executed is False

    for index, scenario_id in enumerate(SCENARIO_IDS):
        local = composed.provider_profiles[PROFILE_IDS[index]]
        policy = composed.security_config.scenarios[scenario_id]
        assert local.scenario_id == scenario_id
        assert local.profile.profile_id == PROFILE_IDS[index]
        assert local.profile.version == policy.profile_version == "1"
        assert local.profile.allowed_runtime_modes == frozenset({RuntimeMode.OWNER_SELF_DOGFOOD})
        assert local.tool_dispatch_allowed is policy.tool_allowed is (index != 2)
        assert local.profile.provider_call_maximum == policy.provider_call_limit

    tool = composed.tool_config
    security = composed.security_config
    assert (tool.registry_id, tool.registry_version) == ("aiscc-stockroom-tools", "1")
    assert (tool.tool_id, tool.action) == (
        "stockroom_summary",
        "fixed-stockroom-summary",
    )
    assert tool.network == "none"
    assert tool.operation_timeout_seconds == security.process_timeout_seconds == 5
    assert tool.cleanup_timeout_seconds == security.cleanup_timeout_seconds == 10
    assert tool.attempt_timeout_seconds == security.attempt_timeout_seconds == 30
    assert (security.provider_calls, security.tool_calls, security.process_calls) == (2, 1, 1)
    assert security.budget_units == 4


def test_configuration_fingerprints_are_deterministic_non_path_provenance() -> None:
    first = build_stockroom_owner_composition().fingerprints
    second = build_stockroom_owner_composition().fingerprints
    assert first == second
    assert all(
        len(value) == 64 and set(value) <= set("0123456789abcdef")
        for value in (
            first.catalog_sha256,
            first.provider_profiles_sha256,
            first.tool_config_sha256,
            first.security_config_sha256,
            first.composition_sha256,
        )
    )
    assert str(ROOT) not in repr(first)


def test_composition_and_requests_are_frozen_and_inert() -> None:
    composed = build_stockroom_owner_composition()
    request = composed.request(
        scenario_id=SCENARIO_IDS[0],
        run_id="run-b3-unit",
        attempt_id="attempt-1",
        expected_initial_state_version=7,
    )
    assert request.run_binding.expected_initial_state is WorkflowState.READY
    assert request.run_binding.expected_initial_state_version == 7
    assert request.configuration_fingerprints is composed.fingerprints
    assert not hasattr(composed, "execute")
    assert not hasattr(request, "execute")
    with pytest.raises(FrozenInstanceError):
        composed.tool_config = object()  # type: ignore[misc]
    with pytest.raises(TypeError):
        composed.provider_profiles["injected"] = object()  # type: ignore[index]


def test_requester_cannot_supply_server_configuration_paths() -> None:
    assert inspect.signature(build_stockroom_owner_composition).parameters == {}
    assert tuple(inspect.signature(bootstrap.build_stockroom_owner_preparation).parameters) == (
        "owners",
    )
    assert tuple(
        inspect.signature(composition_module.StockroomOwnerComposition.request).parameters
    ) == (
        "self",
        "scenario_id",
        "run_id",
        "attempt_id",
        "expected_initial_state_version",
    )


@pytest.mark.parametrize(
    "mutation",
    ("unknown", "missing", "wrong-version", "mismatch", "public-fallback"),
)
def test_altered_or_public_configuration_fails_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, mutation: str
) -> None:
    paths = _temporary_configs(tmp_path, monkeypatch)
    if mutation in {"unknown", "wrong-version"}:
        raw = json.loads(paths["catalog"].read_text(encoding="utf-8"))
        if mutation == "unknown":
            raw["unexpected"] = True
        else:
            raw["schema_version"] = "0.0.0"
        paths["catalog"].write_text(json.dumps(raw), encoding="utf-8")
    elif mutation == "missing":
        paths["catalog"].with_name("resource.json").unlink()
    else:
        current = paths["profiles"].read_text(encoding="utf-8")
        replacement = (
            'scenario_id = "stockroom-s2-missing-evidence"'
            if mutation == "mismatch"
            else 'provider_id = "public-openai"'
        )
        target = (
            'scenario_id = "stockroom-s1-normal"'
            if mutation == "mismatch"
            else 'provider_id = "aiscc-local-deterministic"'
        )
        paths["profiles"].write_text(current.replace(target, replacement, 1), encoding="utf-8")

    with pytest.raises(StockroomCompositionError) as caught:
        build_stockroom_owner_composition()
    assert str(caught.value) == "STOCKROOM_COMPOSITION_BINDING_DENIED"


@pytest.mark.parametrize("replacement", [None, object()])
def test_missing_or_duck_typed_owner_dependency_fails_closed(replacement: object) -> None:
    composed = build_stockroom_owner_composition()
    values = _owners(composed)
    with pytest.raises(ValueError, match="STOCKROOM_REAL_OWNER_DEPENDENCY_REQUIRED"):
        StockroomOwnerDependencies(
            workflow_kernel=replacement,  # type: ignore[arg-type]
            agent_execution_service_factory=values.agent_execution_service_factory,
            evidence_admission_service=values.evidence_admission_service,
            human_gate_owner=values.human_gate_owner,
            judgment_owner=values.judgment_owner,
            workspace_owner=values.workspace_owner,
            materializer_factory=values.materializer_factory,
            security_policy=values.security_policy,
            stockroom_owner_restriction=values.stockroom_owner_restriction,
        )


@pytest.mark.parametrize(
    ("field_name", "replacement"),
    [
        ("materializer_factory", object()),
        (
            "materializer_factory",
            _FactoryAuthority(
                "STOCKROOM_AGENT_EXECUTION_SERVICE_FACTORY",
                "wrong-materializer-role",
                "3" * 64,
            ),
        ),
        ("agent_execution_service_factory", object()),
        (
            "agent_execution_service_factory",
            _FactoryAuthority(
                "STOCKROOM_MATERIALIZER_FACTORY",
                "wrong-execution-role",
                "4" * 64,
            ),
        ),
    ],
)
def test_factory_authority_role_and_identity_fail_closed(
    field_name: str, replacement: object
) -> None:
    owners = _owners(build_stockroom_owner_composition())
    with pytest.raises(ValueError, match="STOCKROOM_REAL_OWNER_DEPENDENCY_REQUIRED"):
        replace(owners, **{field_name: replacement})


def test_default_bootstrap_is_unchanged_and_owner_factory_is_explicitly_inert() -> None:
    default = bootstrap.build_security_policy()
    assert type(default) is SecurityPolicy
    assert default._stockroom_policy is None
    assert set(default._profiles) == {mode.value for mode in RuntimeMode}

    composed = build_stockroom_owner_composition()
    owners = _owners(composed)
    prepared = bootstrap.build_stockroom_owner_preparation(owners=owners)
    assert prepared.owners is owners
    assert not hasattr(prepared, "execute")
    assert not hasattr(bootstrap, "build_public_stockroom")
    bound = bind_stockroom_owner_dependencies(composed, owners)
    assert bound.owners is owners

    request = bound.request(
        scenario_id=SCENARIO_IDS[0],
        run_id="run-owner-identity",
        attempt_id="attempt-owner-identity",
        expected_initial_state_version=1,
    )
    prepared_driver = bound.prepare(
        scenario_id=SCENARIO_IDS[0],
        run_id="run-owner-identity",
        attempt_id="attempt-owner-identity",
        expected_initial_state_version=1,
    )
    assert prepared_driver.owners is owners
    assert prepared_driver.request == request
    assert prepared_driver.owners.workflow_kernel is owners.workflow_kernel
    assert prepared_driver.owners.evidence_admission_service is owners.evidence_admission_service
    assert prepared_driver.owners.human_gate_owner is owners.human_gate_owner
    assert prepared_driver.owners.judgment_owner is owners.judgment_owner
    assert prepared_driver.owners.workspace_owner is owners.workspace_owner
    assert prepared_driver.owners.security_policy is owners.security_policy
    assert prepared_driver.owners.stockroom_owner_restriction is owners.stockroom_owner_restriction
    assert prepared_driver.owners.materializer_factory is owners.materializer_factory
    assert (
        prepared_driver.owners.agent_execution_service_factory
        is owners.agent_execution_service_factory
    )
    assert prepared_driver.attempt_binding.run_id == "run-owner-identity"
    assert prepared_driver.attempt_binding.attempt_id == "attempt-owner-identity"
    assert prepared_driver.attempt_binding.scenario_id == SCENARIO_IDS[0]
    assert prepared_driver.attempt_binding.request_fingerprint == request.request_fingerprint
    assert (
        prepared_driver.attempt_binding.run_binding_fingerprint
        == request.run_binding.binding_fingerprint
    )
    assert (
        prepared_driver.attempt_binding.configuration_fingerprint
        == request.configuration_fingerprints.composition_sha256
    )
    with pytest.raises(FrozenInstanceError):
        prepared_driver.attempt_binding.run_id = "foreign-run"  # type: ignore[misc]
    with pytest.raises(ValueError, match="STOCKROOM_PREPARED_ATTEMPT_BINDING_DENIED"):
        replace(
            prepared_driver,
            attempt_binding=replace(
                prepared_driver.attempt_binding,
                request_fingerprint="f" * 64,
                binding_fingerprint="e" * 64,
            ),
        )


def test_prepared_attempt_binding_rejects_foreign_request_context() -> None:
    composed = build_stockroom_owner_composition()
    owners = _owners(composed)
    local_request = composed.request(
        scenario_id=SCENARIO_IDS[0],
        run_id="run-local",
        attempt_id="attempt-local",
        expected_initial_state_version=1,
    )
    foreign_request = composed.request(
        scenario_id=SCENARIO_IDS[1],
        run_id="run-foreign",
        attempt_id="attempt-foreign",
        expected_initial_state_version=1,
    )
    foreign_binding = build_prepared_attempt_binding(foreign_request)
    with pytest.raises(ValueError, match="STOCKROOM_PREPARED_DRIVER_BINDING_DENIED"):
        PreparedStockroomDriver(local_request, owners, foreign_binding)

    altered_composition = replace(composed.fingerprints, composition_sha256="a" * 64)
    altered_request = composition_module.build_stockroom_driver_request(
        composed.enroll(SCENARIO_IDS[0]),
        run_id="run-local",
        attempt_id="attempt-local",
        expected_initial_state_version=1,
        configuration_fingerprints=altered_composition,
    )
    with pytest.raises(ValueError, match="STOCKROOM_PREPARED_DRIVER_BINDING_DENIED"):
        PreparedStockroomDriver(
            altered_request,
            owners,
            build_prepared_attempt_binding(local_request),
        )
