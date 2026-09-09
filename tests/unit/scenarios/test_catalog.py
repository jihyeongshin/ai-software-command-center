from __future__ import annotations

import json
import shutil
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from pydantic import ValidationError

from aiscc.scenarios import ContractError, load_catalog

CONFIG = Path(__file__).resolve().parents[3] / "config/scenarios/stockroom/v1"
IDS = (
    "stockroom-s1-normal",
    "stockroom-s2-missing-evidence",
    "stockroom-s3-policy-conflict",
    "stockroom-s4-human-owned-claim",
)
REF = (
    "repository:synthetic-stockroom@"
    "be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d"
)


@pytest.fixture
def pack(tmp_path: Path) -> Path:
    target = tmp_path / "pack"
    shutil.copytree(CONFIG, target)
    return target


def edit(pack: Path, filename: str, change) -> None:
    path = pack / filename
    value = json.loads(path.read_text(encoding="utf-8"))
    change(value)
    path.write_text(json.dumps(value), encoding="utf-8")


def test_four_exact_scenarios_and_selection() -> None:
    catalog = load_catalog(CONFIG / "catalog.json")
    assert tuple(item.scenario_id for item in catalog.scenarios) == IDS
    assert len(catalog.fixtures) == 3
    assert {item.scenario_version for item in catalog.scenarios} == {"1.0.0"}
    assert {item.resource_ref for item in catalog.scenarios} == {REF}
    schema = catalog.document.public_selection_schema.model_dump(mode="json")
    assert schema == {
        "type": "object",
        "additionalProperties": False,
        "required": ["scenario_id"],
        "properties": {"scenario_id": {"type": "string", "enum": list(IDS)}},
    }
    for sid in IDS:
        assert Draft202012Validator(schema).is_valid({"scenario_id": sid})
        assert catalog.select({"scenario_id": sid}).scenario_id == sid


def test_shuffled_catalog_has_deterministic_loaded_order(pack: Path) -> None:
    edit(pack, "catalog.json", lambda d: d["scenarios"].reverse())
    assert (
        load_catalog(pack / "catalog.json").scenarios
        == load_catalog(CONFIG / "catalog.json").scenarios
    )


def test_loaded_contract_is_deeply_frozen() -> None:
    catalog = load_catalog(CONFIG / "catalog.json")
    with pytest.raises(FrozenInstanceError):
        catalog.scenarios = ()
    with pytest.raises(ValidationError):
        catalog.scenarios[0].task_contract.goal = "replace"
    with pytest.raises(ValidationError):
        catalog.resource.files[0].sha256 = "0" * 64
    with pytest.raises(TypeError):
        catalog.scenarios[0].evidence_contract.executor_required[0] = None


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"scenario_id": "unknown"},
        {"scenario_id": 1},
        {"scenario_id": True},
        {"scenario_id": "stockroom-s1-normal@1.0.0"},
        [],
        None,
    ]
    + [
        {"scenario_id": IDS[0], key: "injected"}
        for key in (
            "task",
            "path",
            "repo",
            "url",
            "command",
            "provider",
            "model",
            "parameters",
            "credential",
        )
    ],
)
def test_selector_rejects_every_other_surface(payload: object) -> None:
    catalog = load_catalog(CONFIG / "catalog.json")
    with pytest.raises(ContractError):
        catalog.select(payload)
    schema = catalog.document.public_selection_schema.model_dump(mode="json")
    assert not Draft202012Validator(schema).is_valid(payload)


@pytest.mark.parametrize(
    ("filename", "change"),
    [
        ("catalog.json", lambda d: d.update(extra=True)),
        ("catalog.json", lambda d: d["scenarios"].__setitem__(1, d["scenarios"][0])),
        ("catalog.json", lambda d: d["scenarios"][0].update(scenario_version="latest")),
        ("catalog.json", lambda d: d["scenarios"][0].update(scenario_id="unknown")),
        ("catalog.json", lambda d: d["scenarios"][0].update(path="s2-missing-evidence.json")),
        ("catalog.json", lambda d: d.update(resource_ref="repository:unknown@1")),
        ("catalog.json", lambda d: d["public_selection_schema"].update(additionalProperties=True)),
        ("catalog.json", lambda d: d["public_selection_schema"]["required"].clear()),
        (
            "catalog.json",
            lambda d: d["public_selection_schema"]["properties"]["scenario_id"]["enum"].pop(),
        ),
        ("s1-normal.json", lambda d: d.update(extra=True)),
        ("s1-normal.json", lambda d: d["task_contract"].update(command="injected")),
        ("s1-normal.json", lambda d: d.update(scenario_id="stockroom-unknown")),
        ("s1-normal.json", lambda d: d.update(scenario_version="2.0.0")),
        (
            "s1-normal.json",
            lambda d: d.update(resource_ref="repository:synthetic-stockroom@latest"),
        ),
        ("s1-normal.json", lambda d: d.update(user_parameters={"task": "injected"})),
        ("s1-normal.json", lambda d: d.update(user_parameters=["injected"])),
        ("s2-missing-evidence.json", lambda d: d["fixture_refs"].append(d["fixture_refs"][0])),
    ],
)
def test_bad_catalog_and_scenario_contracts_fail_closed(pack: Path, filename, change) -> None:
    edit(pack, filename, change)
    with pytest.raises(ContractError):
        load_catalog(pack / "catalog.json")


@pytest.mark.parametrize(
    "ref",
    [
        "/tmp/fixture.json",
        "../fixture.json",
        "fixtures/../../fixture.json",
        "C:/fixture.json",
        "C:\\fixture.json",
        "\\\\server\\fixture.json",
        "fixtures//missing-evidence.json",
        "fixtures/./missing-evidence.json",
        "fixtures/missing-evidence.json:stream",
        "fixtures/%2e%2e/fixture.json",
        "https://invalid.test/fixture.json",
    ],
)
def test_fixture_path_injection(pack: Path, ref: str) -> None:
    edit(pack, "s2-missing-evidence.json", lambda d: d.update(fixture_refs=[ref]))
    with pytest.raises(ContractError):
        load_catalog(pack / "catalog.json")


def test_scenario_file_cannot_be_swapped_under_catalog_identity(pack: Path) -> None:
    (pack / "s1-normal.json").write_bytes((pack / "s2-missing-evidence.json").read_bytes())
    with pytest.raises(ContractError):
        load_catalog(pack / "catalog.json")


@pytest.mark.parametrize(
    "filename",
    [
        "catalog.json",
        "resource.json",
        "s1-normal.json",
        "fixtures/policy-conflict.json",
    ],
)
def test_missing_file(pack: Path, filename: str) -> None:
    (pack / filename).unlink()
    with pytest.raises(ContractError):
        load_catalog(pack / "catalog.json")


@pytest.mark.parametrize(
    "payload",
    [
        b'{"schema_id": "x", "schema_id": "y"}',
        b'{"x": NaN}',
        b'{"x": Infinity}',
        b'{"schema_id":',
        b"\xff",
        b"[]",
        b"null",
        b" " * 131073,
    ],
    ids=(
        "duplicate-key",
        "nan",
        "infinity",
        "truncated-json",
        "invalid-utf8",
        "array-root",
        "null-root",
        "oversize",
    ),
)
def test_malformed_json_and_duplicate_keys(pack: Path, payload: bytes) -> None:
    (pack / "catalog.json").write_bytes(payload)
    with pytest.raises(ContractError, match="static contract|size limit"):
        load_catalog(pack / "catalog.json")


def test_resolved_fixture_escape_denied_without_reading_outside(pack: Path, monkeypatch) -> None:
    original = Path.resolve
    fixture = pack / "fixtures/missing-evidence.json"
    outside = pack.parent / "outside.json"

    def resolve(path: Path, strict: bool = False) -> Path:
        return outside if path == fixture else original(path, strict=strict)

    monkeypatch.setattr(Path, "resolve", resolve)
    with pytest.raises(ContractError):
        load_catalog(pack / "catalog.json")
