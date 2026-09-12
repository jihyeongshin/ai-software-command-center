from __future__ import annotations

import ast
import json
import shutil
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from aiscc.scenarios import ContractError, load_catalog
from aiscc.scenarios.models import Resource, Scenario

ROOT = Path(__file__).resolve().parents[3]
CONFIG = ROOT / "config/scenarios/stockroom/v1"


def test_schema_artifacts_match_typed_shape_and_validate_config() -> None:
    for filename, model, names in (
        ("resource-v1.schema.json", Resource, ("resource.json",)),
        (
            "scenario-v1.schema.json",
            Scenario,
            (
                "s1-normal.json",
                "s2-missing-evidence.json",
                "s3-policy-conflict.json",
                "s4-human-owned-claim.json",
            ),
        ),
    ):
        schema = json.loads((ROOT / "config/scenarios/schemas" / filename).read_text("utf-8"))
        Draft202012Validator.check_schema(schema)
        assert schema.pop("$schema") == "https://json-schema.org/draft/2020-12/schema"
        schema.pop("description")
        assert schema == model.model_json_schema()
        for name in names:
            Draft202012Validator(schema).validate(json.loads((CONFIG / name).read_text("utf-8")))


def test_four_outcomes_and_five_way_ownership_are_not_runtime_claims() -> None:
    s1, s2, s3, s4 = load_catalog(CONFIG / "catalog.json").scenarios
    assert s1.expected_workflow.states == ("READY", "RUNNING", "ADMISSION_PENDING", "ACCEPTED")
    assert s1.judgment_contract.owner_policy == "SYSTEM_DETERMINISTIC"
    assert s1.judgment_contract.expected_status == "ACCEPTED"
    assert not s1.evidence_contract.human_owned
    assert s1.cycle_next_action_contract.runtime_admitted_cycle == "AFTER_ACCEPTED_TERMINAL_LINEAGE"
    assert s2.expected_workflow.states[-1] == "REWORK_REQUIRED"
    assert s2.expected_workflow.accepted_request.reason == "MISSING_EVIDENCE"
    assert s2.expected_workflow.accepted_request.state_version_mutation is False
    assert s2.judgment_contract.expected_status == "HOLD_REWORK_REQUIRED"
    assert s2.expected_workflow.same_run_automatic_retry is False
    assert s3.expected_workflow.states == ("READY", "RUNNING", "BLOCKED")
    assert s3.expected_workflow.blocker.blocker_type == "POLICY"
    assert s3.expected_workflow.blocker.blocker_reason == "POLICY_CONFLICT"
    assert s3.judgment_contract.authoritative_at_capture_boundary is False
    assert s3.judgment_contract.expected_status is None
    assert s4.expected_workflow.states[-1] == "HUMAN_REQUIRED"
    assert s4.expected_workflow.wrong_owner_candidate == "REJECTED"
    assert s4.expected_workflow.attestation == "FRESH_PRE_HUMAN"
    assert s4.expected_workflow.human_result == "ABSENT_PENDING"
    assert s4.expected_workflow.accepted_request.state_version_mutation is False
    assert s4.evidence_contract.human_owned[0].owner == "HUMAN"
    assert s4.judgment_contract.expected_status is None
    for scenario in (s1, s2, s3, s4):
        assert set(type(scenario.evidence_contract).model_fields) == {
            "executor_required",
            "reuse_allowed",
            "human_owned",
            "not_required",
            "forbidden",
        }
        assert scenario.public_disclosure.runtime_claim == "NONE_STATIC_DEFINITION"
        assert scenario.public_disclosure.license_review == "HUMAN_PENDING"
        assert scenario.recording_contract.external_llm_executed is False
        assert scenario.user_parameters == ()
    for scenario in (s2, s3, s4):
        assert scenario.cycle_next_action_contract.runtime_admitted_cycle == "INELIGIBLE_AT_CAPTURE"
        assert (
            scenario.cycle_next_action_contract.reusable_project_memory == "INELIGIBLE_AT_CAPTURE"
        )


def test_server_fixtures_do_not_fabricate_human_input() -> None:
    missing, policy, human = load_catalog(CONFIG / "catalog.json").fixtures
    assert missing.fixture_owner == "SERVER"
    assert missing.omitted_requirement_id == "summary-runtime"
    assert missing.controlled_omission is True
    assert policy.baseline.rule == "reorder when available <= threshold"
    assert policy.requested_replacement.rule == "requested replacement uses available < threshold"
    assert policy.source_mutation is False
    assert human.adversarial is True and human.synthetic is True
    assert human.agent_claim.producer == "AGENT"
    assert human.agent_claim.text == "Human browser QA completed"
    assert human.agent_claim.actual_human_input is False
    assert human.human_result is None


@pytest.mark.parametrize(
    ("filename", "change"),
    [
        ("fixtures/missing-evidence.json", lambda d: d.pop("omitted_requirement_id")),
        ("fixtures/missing-evidence.json", lambda d: d.update(controlled_omission=False)),
        ("fixtures/missing-evidence.json", lambda d: d.update(fixture_owner="PUBLIC")),
        ("fixtures/policy-conflict.json", lambda d: d.pop("baseline")),
        (
            "fixtures/policy-conflict.json",
            lambda d: d["baseline"].update(rule="available < threshold"),
        ),
        (
            "fixtures/policy-conflict.json",
            lambda d: d["requested_replacement"].update(policy_id="inclusive-reorder-baseline-v1"),
        ),
        ("fixtures/policy-conflict.json", lambda d: d["blocker"].update(blocker_type="SECURITY")),
        ("fixtures/human-owned-claim.json", lambda d: d["agent_claim"].update(producer="HUMAN")),
        (
            "fixtures/human-owned-claim.json",
            lambda d: d["agent_claim"].update(actual_human_input=True),
        ),
        (
            "fixtures/human-owned-claim.json",
            lambda d: d.update(human_result={"outcome": "APPROVE"}),
        ),
        ("fixtures/human-owned-claim.json", lambda d: d.update(adversarial=False)),
        ("fixtures/human-owned-claim.json", lambda d: d.update(synthetic=1)),
        ("fixtures/human-owned-claim.json", lambda d: d.update(judgment="ACCEPTED")),
        (
            "s2-missing-evidence.json",
            lambda d: d["expected_workflow"]["accepted_request"].update(
                state_version_mutation=True
            ),
        ),
        (
            "s2-missing-evidence.json",
            lambda d: d["judgment_contract"].update(expected_status="ACCEPTED"),
        ),
        ("s3-policy-conflict.json", lambda d: d.update(fixture_refs=[])),
        (
            "s3-policy-conflict.json",
            lambda d: d["judgment_contract"].update(authoritative_at_capture_boundary=True),
        ),
        ("s4-human-owned-claim.json", lambda d: d["evidence_contract"]["human_owned"].clear()),
        (
            "s4-human-owned-claim.json",
            lambda d: d["expected_workflow"].update(attestation="NOT_REQUIRED"),
        ),
        (
            "s4-human-owned-claim.json",
            lambda d: d["cycle_next_action_contract"].update(
                runtime_admitted_cycle="AFTER_ACCEPTED_TERMINAL_LINEAGE"
            ),
        ),
        ("s1-normal.json", lambda d: d["evidence_contract"].pop("not_required")),
        ("s1-normal.json", lambda d: d["recording_contract"]["required_provenance"].pop()),
    ],
)
def test_negative_demonstration_semantics_are_enforced(tmp_path: Path, filename, change) -> None:
    pack = tmp_path / "pack"
    shutil.copytree(CONFIG, pack)
    path = pack / filename
    data = json.loads(path.read_text("utf-8"))
    change(data)
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ContractError):
        load_catalog(pack / "catalog.json")


def test_static_module_has_no_execution_or_integration_imports() -> None:
    allowed = {
        "__future__",
        "hashlib",
        "re",
        "typing",
        "pydantic",
        "json",
        "dataclasses",
        "pathlib",
        "jsonschema",
        "aiscc.scenarios",
    }
    paths = tuple(
        ROOT / "src/aiscc/scenarios" / name for name in ("__init__.py", "catalog.py", "models.py")
    )
    for path in paths:
        tree = ast.parse(path.read_text("utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module]
            else:
                continue
            assert all(any(m == a or m.startswith(a + ".") for a in allowed) for m in modules)


def test_static_import_policy_reads_exact_three_members(monkeypatch: pytest.MonkeyPatch) -> None:
    original_read_text = Path.read_text
    scanned = []

    def record_read(path, *args, **kwargs):
        scanned.append(path.relative_to(ROOT).as_posix())
        return original_read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", record_read)
    test_static_module_has_no_execution_or_integration_imports()
    assert tuple(scanned) == (
        "src/aiscc/scenarios/__init__.py",
        "src/aiscc/scenarios/catalog.py",
        "src/aiscc/scenarios/models.py",
    )
