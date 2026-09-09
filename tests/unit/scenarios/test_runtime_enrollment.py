from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from aiscc.contracts.workflow import RuntimeMode
from aiscc.scenarios import load_catalog
from aiscc.scenarios.enrollment import (
    build_stockroom_owner_context,
    compile_stockroom_selection,
)
from aiscc.scenarios.models import RESOURCE_REF, SCENARIO_IDS

CONFIG = Path("config/scenarios/stockroom/v1/catalog.json")


def _compiled():
    catalog = load_catalog(CONFIG)
    context = build_stockroom_owner_context(catalog.scenarios)
    return catalog, context, tuple(
        compile_stockroom_selection(
            {"scenario_id": scenario_id}, catalog=catalog, owner_context=context
        )
        for scenario_id in SCENARIO_IDS
    )


def test_four_exact_inert_owner_enrollments_are_frozen() -> None:
    _, _, enrollments = _compiled()
    assert tuple(item.scenario_id for item in enrollments) == SCENARIO_IDS
    assert {item.scenario_version for item in enrollments} == {"1.0.0"}
    assert {item.resource_ref for item in enrollments} == {RESOURCE_REF}
    assert {item.mode for item in enrollments} == {RuntimeMode.OWNER_SELF_DOGFOOD}
    assert {item.execution_backend_kind for item in enrollments} == {
        "LOCAL_DETERMINISTIC_PROVIDER"
    }
    assert all(item.external_llm_executed is False for item in enrollments)
    assert all(item.admitted_evidence == () and item.human_result is None for item in enrollments)
    with pytest.raises(FrozenInstanceError):
        enrollments[0].scenario_id = "replaced"  # type: ignore[misc]


def test_scenario_semantics_remain_distinct() -> None:
    _, _, (s1, s2, s3, s4) = _compiled()
    assert (s1.tool_id, s1.expected_states[-1]) == ("stockroom_summary", "ACCEPTED")
    assert s2.tool_id == "stockroom_summary"
    assert s2.suppress_summary_evidence_candidate is True
    assert s2.expected_states[-1] == "REWORK_REQUIRED"
    assert s2.same_run_automatic_retry is False
    assert s3.tool_id is None and s3.tool_action is None
    assert s3.expected_states[-1] == "BLOCKED"
    assert s3.judgment_descriptor.authoritative_at_capture_boundary is False
    assert s4.human_descriptor is not None
    assert s4.human_descriptor.ownership == "HUMAN_OWNED"
    assert s4.human_descriptor.producer == "HUMAN_P1_7"
    assert s4.human_descriptor.status == "HUMAN_PENDING"
    assert s4.human_descriptor.pre_human_readiness_required is True
    assert {d.proof_type for d in s1.evidence_descriptors} == {"TOOL_RUNTIME"}
    assert {d.proof_type for d in s3.evidence_descriptors} == {"STATIC_SOURCE"}


@pytest.mark.parametrize(
    "selection",
    [
        {},
        {"scenario_id": "unknown"},
        {"scenario_id": SCENARIO_IDS[0], "task": "injected"},
        {"scenario_id": SCENARIO_IDS[0], "provider": "injected"},
        {"scenario_id": SCENARIO_IDS[0], "command": "injected"},
        [SCENARIO_IDS[0]],
    ],
)
def test_requester_surface_is_scenario_id_only(selection: object) -> None:
    catalog = load_catalog(CONFIG)
    context = build_stockroom_owner_context(catalog.scenarios)
    with pytest.raises(ValueError):
        compile_stockroom_selection(selection, catalog=catalog, owner_context=context)


def test_compile_performs_no_io_or_runtime_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    catalog = load_catalog(CONFIG)
    context = build_stockroom_owner_context(catalog.scenarios)

    def forbidden(*args: object, **kwargs: object) -> None:
        del args, kwargs
        raise AssertionError("side effect boundary called")

    monkeypatch.setattr(Path, "open", forbidden)
    enrollment = compile_stockroom_selection(
        {"scenario_id": SCENARIO_IDS[0]}, catalog=catalog, owner_context=context
    )
    assert enrollment.scenario_id == SCENARIO_IDS[0]
