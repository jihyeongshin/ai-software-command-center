from __future__ import annotations

import inspect
import json
import shutil
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

import aiscc.bootstrap as bootstrap
import aiscc.scenarios.composition as composition_module
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.evidence.service import EvidenceAdmissionService
from aiscc.human.repository import PostgresHumanAuthorityRepository
from aiscc.judgment.authority import PostgresJudgmentAuthority
from aiscc.providers.service import AgentExecutionService
from aiscc.runtime.stockroom_materializer import StockroomMaterializer
from aiscc.runtime.stockroom_workspace import StockroomWorkspace
from aiscc.scenarios.composition import (
    StockroomCompositionError,
    bind_stockroom_owner_dependencies,
    build_stockroom_owner_composition,
)
from aiscc.scenarios.driver import StockroomOwnerDependencies
from aiscc.scenarios.models import RESOURCE_REF, SCENARIO_IDS
from aiscc.security.policy import SecurityPolicy, default_profiles
from aiscc.security.stockroom_policy import StockroomOwnerRestriction
from aiscc.workflow.kernel import WorkflowKernel

ROOT = Path(__file__).resolve().parents[3]
PROFILE_IDS = (
    "stockroom-owner-s1-v1",
    "stockroom-owner-s2-v1",
    "stockroom-owner-s3-v1",
    "stockroom-owner-s4-v1",
)


def _owners(composition: object) -> StockroomOwnerDependencies:
    security_config = composition.security_config  # type: ignore[attr-defined]
    restriction = StockroomOwnerRestriction(security_config)
    return StockroomOwnerDependencies(
        workflow_kernel=object.__new__(WorkflowKernel),
        agent_execution_service=object.__new__(AgentExecutionService),
        evidence_admission_service=object.__new__(EvidenceAdmissionService),
        human_gate_owner=object.__new__(PostgresHumanAuthorityRepository),
        judgment_owner=object.__new__(PostgresJudgmentAuthority),
        workspace_owner=object.__new__(StockroomWorkspace),
        materializer=object.__new__(StockroomMaterializer),
        security_policy=SecurityPolicy(
            default_profiles(), stockroom_policy=restriction
        ),
        stockroom_owner_restriction=restriction,
    )


def _temporary_configs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> dict[str, Path]:
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
        assert local.profile.allowed_runtime_modes == frozenset(
            {RuntimeMode.OWNER_SELF_DOGFOOD}
        )
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
        paths["profiles"].write_text(
            current.replace(target, replacement, 1), encoding="utf-8"
        )

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
            agent_execution_service=values.agent_execution_service,
            evidence_admission_service=values.evidence_admission_service,
            human_gate_owner=values.human_gate_owner,
            judgment_owner=values.judgment_owner,
            workspace_owner=values.workspace_owner,
            materializer=values.materializer,
            security_policy=values.security_policy,
            stockroom_owner_restriction=values.stockroom_owner_restriction,
        )


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
