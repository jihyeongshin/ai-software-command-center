from __future__ import annotations

import ast
import json
from dataclasses import replace
from pathlib import Path

import pytest

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.providers.local_deterministic import (
    LOCAL_COMPATIBILITY_SECRET_REF,
    LOCAL_COMPATIBILITY_SENTINEL,
    STOCKROOM_SUMMARY,
    LocalDeterministicProvider,
    load_stockroom_owner_profiles,
)
from aiscc.providers.models import ProviderCall, ProviderInputAuthority
from aiscc.scenarios.models import SCENARIO_IDS

CONFIG = Path("config/providers/stockroom-owner-profiles.v1.toml")
INITIAL = ({"type": "message", "role": "user", "content": "fixed server task"},)
TOOLS = ({"name": "stockroom_summary"},)


def _call(local_profile, *, items=INITIAL, tools=TOOLS, ordinal=1) -> ProviderCall:
    profile = local_profile.profile
    return ProviderCall(
        operation_id=f"provider-operation-{ordinal}",
        operation_fingerprint="a" * 64,
        execution_attempt_id="attempt-local",
        work_run_id="run-local",
        state=WorkflowState.RUNNING,
        state_version=3,
        runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        principal="owner",
        scenario_id=local_profile.scenario_id,
        execution_version=ordinal,
        profile=profile,
        input_items=items,
        tools=tools,
        call_ordinal=ordinal,
        input_authority=(
            ProviderInputAuthority.INITIAL_SERVER
            if ordinal == 1
            else ProviderInputAuthority.DURABLE_LOCAL
        ),
    )


def test_four_exact_owner_profiles_and_finite_bounds() -> None:
    profiles = load_stockroom_owner_profiles(CONFIG)
    assert tuple(profiles) == tuple(f"stockroom-owner-s{i}-v1" for i in range(1, 5))
    assert tuple(item.scenario_id for item in profiles.values()) == SCENARIO_IDS
    for index, item in enumerate(profiles.values()):
        profile = item.profile
        assert profile.version == "1"
        assert profile.provider_id == "aiscc-local-deterministic"
        assert profile.adapter_protocol_version == "stockroom-local-responses-v1"
        assert profile.endpoint_ref == "local-in-process-stockroom-v1"
        assert profile.base_url == "http://127.0.0.1:1/v1"
        assert profile.secret_ref == LOCAL_COMPATIBILITY_SECRET_REF
        assert profile.allowed_runtime_modes == {RuntimeMode.OWNER_SELF_DOGFOOD}
        assert profile.provider_call_maximum == (1 if index == 2 else 2)
        assert profile.agent_round_trip_maximum == (1 if index == 2 else 2)
        assert profile.tool_call_maximum == 1
        assert profile.input_byte_bound <= 16384
        assert profile.output_byte_bound <= 8192
        assert profile.continuation_item_maximum <= 16
        assert profile.total_timeout_seconds <= 30
        assert profile.read_timeout_seconds <= 2
        assert profile.budget_unit_maximum <= 4
        assert item.tool_dispatch_allowed is (index != 2)


@pytest.mark.parametrize(
    "profile_id",
    (
        "stockroom-owner-s1-v1",
        "stockroom-owner-s2-v1",
        "stockroom-owner-s4-v1",
    ),
)
def test_tool_scenarios_emit_one_call_then_truthful_final(profile_id: str) -> None:
    profiles = load_stockroom_owner_profiles(CONFIG)
    local = profiles[profile_id]
    adapter = LocalDeterministicProvider(profiles)
    first = adapter.call(_call(local), secret=LOCAL_COMPATIBILITY_SENTINEL)
    assert first.tool_call is not None
    assert first.tool_call.name == "stockroom_summary"
    assert first.tool_call.arguments_json == "{}"
    assert len(first.output_items) == 1
    output = {
        "type": "function_call_output",
        "call_id": first.tool_call.call_id,
        "output": json.dumps(STOCKROOM_SUMMARY, sort_keys=True, separators=(",", ":")),
    }
    second = adapter.call(
        _call(local, items=INITIAL + first.output_items + (output,), ordinal=2),
        secret=LOCAL_COMPATIBILITY_SENTINEL,
    )
    assert second.tool_call is None
    disclosure = json.loads(second.output_text or "")
    assert disclosure["execution_backend_kind"] == "LOCAL_DETERMINISTIC_PROVIDER"
    assert disclosure["external_llm_executed"] is False
    assert disclosure["summary"] == STOCKROOM_SUMMARY


def test_s3_has_no_tool_and_discloses_fixed_policy_conflict() -> None:
    profiles = load_stockroom_owner_profiles(CONFIG)
    local = profiles["stockroom-owner-s3-v1"]
    result = LocalDeterministicProvider(profiles).call(
        _call(local, tools=()), secret=LOCAL_COMPATIBILITY_SENTINEL
    )
    assert result.tool_call is None
    assert json.loads(result.output_text or "") == {
        "baseline": "available <= reorder_level",
        "external_llm_executed": False,
        "outcome": "POLICY_CONFLICT",
        "requested_replacement": "available < reorder_level",
        "scenario_id": "stockroom-s3-policy-conflict",
    }


def test_wrong_profile_secret_order_call_and_result_are_denied() -> None:
    profiles = load_stockroom_owner_profiles(CONFIG)
    s1 = profiles["stockroom-owner-s1-v1"]
    s2 = profiles["stockroom-owner-s2-v1"]
    adapter = LocalDeterministicProvider(profiles)
    first = adapter.call(_call(s1), secret=LOCAL_COMPATIBILITY_SENTINEL)
    assert first.tool_call is not None
    valid_output = {
        "type": "function_call_output",
        "call_id": first.tool_call.call_id,
        "output": json.dumps(STOCKROOM_SUMMARY),
    }
    invalid_calls = (
        (_call(s1), "credential"),
        (replace(_call(s1), profile=s2.profile), LOCAL_COMPATIBILITY_SENTINEL),
        (
            _call(s1, items=INITIAL + (valid_output,) + first.output_items, ordinal=2),
            LOCAL_COMPATIBILITY_SENTINEL,
        ),
        (
            _call(
                s1,
                items=INITIAL
                + first.output_items
                + ({**valid_output, "call_id": "wrong-call"},),
                ordinal=2,
            ),
            LOCAL_COMPATIBILITY_SENTINEL,
        ),
        (
            _call(
                s1,
                items=INITIAL
                + first.output_items
                + ({**valid_output, "output": "{}"},),
                ordinal=2,
            ),
            LOCAL_COMPATIBILITY_SENTINEL,
        ),
    )
    for call, secret in invalid_calls:
        with pytest.raises(ValueError):
            adapter.call(call, secret=secret)


def test_local_adapter_has_no_transport_or_client_imports() -> None:
    source = Path("src/aiscc/providers/local_deterministic.py").read_text(encoding="utf-8")
    imports = {
        alias.name.split(".", 1)[0]
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Import)
        for alias in node.names
    } | {
        (node.module or "").split(".", 1)[0]
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.ImportFrom)
    }
    assert imports.isdisjoint({"socket", "httpx", "requests", "urllib", "openai"})
    assert "external_llm_executed" in source


def test_strict_profile_loader_rejects_unknown_key(tmp_path: Path) -> None:
    changed = tmp_path / "profiles.toml"
    changed.write_text(CONFIG.read_text(encoding="utf-8") + "\nunknown = true\n", encoding="utf-8")
    with pytest.raises(ValueError):
        load_stockroom_owner_profiles(changed)
