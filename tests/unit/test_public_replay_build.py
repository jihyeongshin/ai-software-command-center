"""Fault-focused checks for immutable, deterministic public Replay generation."""

import importlib.util
import json
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "public_replay_builder", ROOT / "scripts/build_public_replay.py"
)
assert SPEC and SPEC.loader
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


@pytest.fixture
def isolated(tmp_path):
    for relative in [BUILDER.CORPUS, "public/replay"]:
        shutil.copytree(ROOT / relative, tmp_path / relative)
    (tmp_path / "scripts").mkdir()
    shutil.copyfile(
        ROOT / "scripts/build_public_replay.py", tmp_path / "scripts/build_public_replay.py"
    )
    return tmp_path


def snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}


def test_deterministic_and_check_detects_output_and_asset_drift(isolated):
    BUILDER.build(isolated)
    before = snapshot(isolated / "public/replay")
    BUILDER.build(isolated)
    assert snapshot(isolated / "public/replay") == before
    BUILDER.build(isolated, check=True)
    asset = isolated / "public/replay/assets/styles.css"
    asset.write_bytes(asset.read_bytes() + b"\n/* drift */\n")
    with pytest.raises(ValueError, match="PUBLIC_REPLAY_DRIFT"):
        BUILDER.build(isolated, check=True)


@pytest.mark.parametrize("filename", [BUILDER.INDEX, *BUILDER.MEMBERS])
def test_corrupt_corpus_fails_before_any_output_write(isolated, filename):
    before = snapshot(isolated / "public/replay")
    source = isolated / BUILDER.CORPUS / filename
    source.write_bytes(source.read_bytes() + b" ")
    with pytest.raises(ValueError, match="CORPUS_IDENTITY_CONFLICT"):
        BUILDER.build(isolated)
    assert snapshot(isolated / "public/replay") == before


def test_copied_data_drift_and_unexpected_file_fail(isolated):
    copied = isolated / "public/replay/data" / BUILDER.MEMBERS[0]
    copied.write_bytes(b"{}")
    with pytest.raises(ValueError, match="PUBLIC_REPLAY_DRIFT"):
        BUILDER.build(isolated, check=True)
    BUILDER.build(isolated)
    (isolated / "public/replay/unexpected.txt").write_text("not allowed")
    with pytest.raises(ValueError, match="UNEXPECTED_PUBLIC_FILE"):
        BUILDER.build(isolated)


def test_live_release_origin_and_csp_stay_exact(isolated):
    config = json.loads((isolated / "public/replay/live-config.json").read_text("utf-8"))
    assert config == {
        "api_origin": "https://aiscc-public-live-ingress-production.up.railway.app",
        "enabled": True,
        "schema": "AISCC-PUBLIC-LIVE-FRONTEND-CONFIG-V1",
    }
    headers = (isolated / "public/replay/_headers").read_text("utf-8")
    csp = next(line.strip() for line in headers.splitlines() if "Content-Security-Policy:" in line)
    assert "connect-src 'self' https://aiscc-public-live-ingress-production.up.railway.app" in csp
    assert "*" not in csp
    assert csp.count("https://") == 1
    assert "unsafe-inline" not in csp
    assert "unsafe-eval" not in csp


def test_frontend_uses_session_storage_without_capability_debug_channels(isolated):
    app = (isolated / "public/replay/assets/app.js").read_text("utf-8")
    assert "sessionStorage" in app
    assert "localStorage" not in app
    assert "document.cookie" not in app
    assert "console." not in app
    assert "innerHTML" not in app
    assert 'credentials: "omit"' in app


def test_live_trace_frontend_requires_the_exact_safe_projection_contract(isolated):
    app = (isolated / "public/replay/assets/app.js").read_text("utf-8")
    assert "AISCC-PUBLIC-LIVE-INSPECTABLE-RESULT-V1" in app
    assert 'result.instruction.text === "Produce the bounded Stockroom summary."' in app
    assert 'result.human_boundary.state === "NOT_PERFORMED"' in app
    assert '["PRIMARY", "VERIFY", "CORRECT"]' in app
    assert '["BOX-A", 12, 2, 10, false]' in app
    assert "raw provider" not in app.lower()
    assert "private_provider" not in app
    assert 'node("h4", "Live execution trace")' in app
    assert '"Waiting for durable execution evidence."' in app


def test_authored_public_assets_are_canonical_lf_and_match_manifest(isolated):
    replay = isolated / "public/replay"
    manifest = json.loads((replay / "PUBLIC_REPLAY_BUILD_MANIFEST.json").read_text("utf-8"))
    entries = {entry["path"]: entry for entry in manifest["static_assets"]}
    for relative in BUILDER.ASSETS:
        data = (replay / relative).read_bytes()
        assert b"\r\n" not in data
        assert entries[relative] == {
            "path": relative,
            "sha256": BUILDER.sha(data),
            "bytes": len(data),
        }
    generator = (isolated / "scripts/build_public_replay.py").read_bytes()
    assert b"\r\n" not in generator
    assert manifest["generator_sha256"] == BUILDER.sha(generator)
