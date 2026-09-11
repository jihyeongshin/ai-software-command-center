from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

import aiscc.runtime.stockroom_image as image_module
from aiscc.providers.stockroom_tool import build_stockroom_spec, load_stockroom_tool_config
from aiscc.runtime.stockroom_image import (
    BASE_REPODIGEST,
    BUILD_CONTRACT,
    PROVENANCE_PATH,
    RESOURCE_REF,
    SCHEMA_ID,
    SOURCE_AGGREGATE,
    SOURCE_COMMIT,
    SOURCE_SUBROOT,
    SOURCE_SUBTREE,
    AdmittedStockroomImage,
    StockroomImageProvenanceRef,
    canonical_fingerprint,
    image_policy,
    parse_provenance,
    provenance_payload,
    require_admitted_image,
    required_labels,
    resolve_stockroom_image,
    verify_image_inspect,
)

ROOT = Path(__file__).resolve().parents[3]


def synthetic_image(tmp_path, monkeypatch, identity="a" * 64):
    """Test-only file seam, using the real parser, resolver and build verification."""
    dockerfile_hash = hashlib.sha256(
        (ROOT / SOURCE_SUBROOT / "Dockerfile").read_bytes()
    ).hexdigest()
    labels = required_labels(dockerfile_hash)
    observation = {
        "Id": "sha256:" + identity, "Os": "linux", "Architecture": "amd64",
        "Config": {"User": "65532:65532", "WorkingDir": "/workspace", "Labels": labels},
    }
    raw = {
        "schema_id": SCHEMA_ID, "schema_version": "1.0.0",
        "provenance_id": "test-only-never-browser-issued", "provenance_version": "1",
        "issuance": {
            "accepted_cycle_ref": ".aiassistant/records/aiscc/cycles/test-only-cut-b.cycle.md",
            "accepted_judgment_ref": ".aiassistant/reports/aiscc/test-only-cut-b.md",
        },
        "image": {"identity_model": "LOCAL_IMAGE_CONFIG_ID_SHA256",
                  "image_id": "sha256:" + identity,
                  "os": "linux", "architecture": "amd64", "discovery_tag": None},
        "base_image": {"pin_model": "SOURCE_FIXED_VERIFIED_REPODIGEST",
                       "repodigest": BASE_REPODIGEST},
        "build": {"contract_version": BUILD_CONTRACT,
                  "context_model": "TASK_SCOPED_GIT_OBJECT_ASSEMBLED_EXACT_CONTEXT",
                  "dockerfile_sha256": dockerfile_hash,
                  "dockerignore_sha256": hashlib.sha256(
                      (ROOT / SOURCE_SUBROOT / ".dockerignore").read_bytes()).hexdigest()},
        "source": {"commit": SOURCE_COMMIT, "subroot": SOURCE_SUBROOT,
                   "git_subtree": SOURCE_SUBTREE,
                   "resource_ref": RESOURCE_REF, "aggregate_sha256": SOURCE_AGGREGATE,
                   "file_count": 14},
        "runtime": {"python_version": "3.12.14",
                    "argv": ["python", "-B", "-m", "stockroom", "summary"],
                    "workdir": "/workspace", "user": "65532:65532", "network": "none"},
        "required_labels": labels, "inspect_projection_sha256": canonical_fingerprint(observation),
        "issued_at": "2026-09-12T00:10:00+09:00",
    }
    path = tmp_path / "test-only-provenance.json"
    path.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    monkeypatch.setattr(image_module, "_read_canonical", path.read_bytes)
    ref = StockroomImageProvenanceRef.model_validate({
        "path": PROVENANCE_PATH, "whole_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "canonical_fingerprint": canonical_fingerprint(raw), "provenance_id": raw["provenance_id"],
        "provenance_version": "1", "issuance": raw["issuance"],
    })
    admitted = resolve_stockroom_image(ref, image_policy())
    return admitted, ref, raw, path, observation


def test_fingerprint_and_separate_transport_hash(tmp_path, monkeypatch):
    admitted, ref, raw, path, observation = synthetic_image(tmp_path, monkeypatch)
    assert (
        canonical_fingerprint(provenance_payload(admitted.provenance)) == ref.canonical_fingerprint
    )
    verify_image_inspect(observation, admitted)
    path.write_text(json.dumps(raw, separators=(",", ":")), encoding="utf-8")
    assert canonical_fingerprint(json.loads(path.read_bytes())) == ref.canonical_fingerprint
    with pytest.raises(ValueError, match="REF_BINDING"):
        require_admitted_image(admitted)


@pytest.mark.parametrize("section,key,value", [
    (None, "unknown", True), (None, "schema_version", 1),
    ("source", "commit", "0" * 40), ("source", "file_count", "14"),
    ("source", "subroot", "C:/private"), ("source", "git_subtree", "0" * 40),
    ("base_image", "repodigest", "python:latest"),
    ("build", "contract_version", "other"), ("runtime", "network", "bridge"),
    ("image", "image_id", "python:latest"), ("image", "image_id", "sha256:" + SOURCE_AGGREGATE),
    ("image", "image_id", "sha256:" + "A" * 64), ("image", "secret", "synthetic"),
    ("runtime", "argv", ["sh"]), ("runtime", "user", "root"),
])
def test_strict_schema_denies_drift(tmp_path, monkeypatch, section, key, value):
    _, _, raw, _, _ = synthetic_image(tmp_path, monkeypatch)
    (raw if section is None else raw[section])[key] = value
    with pytest.raises(ValueError):
        parse_provenance(json.dumps(raw).encode())


@pytest.mark.parametrize("field,value", [
    ("whole_file_sha256", "b" * 64), ("canonical_fingerprint", "b" * 64),
    ("provenance_id", "other"), ("provenance_version", "2"),
    ("issuance", {"accepted_cycle_ref": ".aiassistant/records/aiscc/cycles/other.cycle.md",
                  "accepted_judgment_ref": ".aiassistant/reports/aiscc/other.md"}),
])
def test_ref_binding_denies_drift(tmp_path, monkeypatch, field, value):
    _, ref, _, _, _ = synthetic_image(tmp_path, monkeypatch)
    data = ref.model_dump(mode="json")
    data[field] = value
    with pytest.raises(ValueError, match="REF_BINDING"):
        resolve_stockroom_image(StockroomImageProvenanceRef.model_validate(data), image_policy())


def test_raw_and_unresolved_objects_cannot_build_v2_spec(tmp_path, monkeypatch):
    admitted, ref, raw, _, _ = synthetic_image(tmp_path, monkeypatch)
    config = load_stockroom_tool_config(ROOT / "config/providers/stockroom-tools.v2.toml")
    for fake in (None, ref, parse_provenance(json.dumps(raw).encode()),
                 AdmittedStockroomImage(admitted.provenance, ref, object(), b""),
                 replace(
                     admitted,
                     provenance=admitted.provenance.model_copy(update={"provenance_id": "other"})
                 )):
        with pytest.raises(ValueError):
            build_stockroom_spec(config, name="aiscc-test", run_id="run", workspace=tmp_path,
                                 image_provenance=fake)


def test_missing_canonical_and_static_policy_drift(tmp_path, monkeypatch):
    admitted, ref, _, path, _ = synthetic_image(tmp_path, monkeypatch)
    policy = image_policy()
    policy["provenance_fingerprint_required"] = 1
    with pytest.raises(ValueError, match="STATIC_IMAGE_POLICY"):
        resolve_stockroom_image(ref, policy)
    path.unlink()
    with pytest.raises(FileNotFoundError):
        require_admitted_image(admitted)


def test_labels_projection_and_build_currentness(tmp_path, monkeypatch):
    admitted, ref, raw, path, observation = synthetic_image(tmp_path, monkeypatch)
    changed = copy.deepcopy(observation)
    changed["Config"]["Labels"]["io.aiscc.stockroom.python-version"] = "3.11"
    with pytest.raises(ValueError, match="LABEL_DRIFT"):
        verify_image_inspect(changed, admitted)
    changed = copy.deepcopy(observation)
    changed["Architecture"] = "arm64"
    with pytest.raises(ValueError, match="IDENTITY_DRIFT"):
        verify_image_inspect(changed, admitted)
    raw["build"]["dockerignore_sha256"] = "0" * 64
    path.write_text(json.dumps(raw), encoding="utf-8")
    ref = ref.model_copy(update={"whole_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                                 "canonical_fingerprint": canonical_fingerprint(raw)})
    with pytest.raises(ValueError, match="BUILD_FILE_CURRENTNESS"):
        resolve_stockroom_image(ref, image_policy())


def test_duplicate_json_key_denied(tmp_path, monkeypatch):
    _, _, _, path, _ = synthetic_image(tmp_path, monkeypatch)
    data = path.read_bytes().replace(b'{', b'{"schema_id":"duplicate",', 1)
    with pytest.raises(ValueError, match="DUPLICATE"):
        parse_provenance(data)
