"""Deterministic, standard-library-only public Replay build. No runtime or network."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

BASELINE = "17fcd337a8bc1410e230a7c18195ac3d3006b417"
CORPUS_ROOT = "a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e"
INDEX_SHA = "c92fb81c43cef9b1c379c2df8dac967aa55f4ddae73780d31f5d51c617aa38e0"
CORPUS = ".aiassistant/reports/aiscc/replay/stockroom/v1"
INDEX = "REPLAY_CORPUS_INDEX.json"
MEMBERS = (
    "stockroom-s1-normal.json",
    "stockroom-s2-missing-evidence.json",
    "stockroom-s3-policy-conflict.json",
    "stockroom-s4-human-owned-claim.json",
)
ASSETS = ("index.html", "404.html", "assets/app.js", "assets/styles.css", "_headers")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def encoded(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode()


def read_regular(root: Path, relative: str) -> bytes:
    path = root / relative
    if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"UNSAFE_PATH: {relative}")
    return path.read_bytes()


def build(root: Path, *, check: bool = False) -> dict[str, object]:
    source = root / CORPUS
    output = root / "public/replay"
    index_bytes = read_regular(source, INDEX)
    if sha(index_bytes) != INDEX_SHA or len(index_bytes) != 4084:
        raise ValueError("CORPUS_IDENTITY_CONFLICT: index")
    index = json.loads(index_bytes)
    rows = index["members"]
    if {m["member_relative_path"] for m in rows} != set(MEMBERS) or len(rows) != 4:
        raise ValueError("CORPUS_IDENTITY_CONFLICT: member set")
    tuples = sorted([[m["scenario_id"], m["member_sha256"], m["member_bytes"]] for m in rows])
    root_hash = sha(json.dumps(tuples, ensure_ascii=False, separators=(",", ":")).encode())
    if root_hash != CORPUS_ROOT or index["corpus_integrity_root_sha256"] != CORPUS_ROOT:
        raise ValueError("CORPUS_IDENTITY_CONFLICT: root")
    planned = {"data/" + INDEX: index_bytes}
    source_members = []
    for m in rows:
        name = m["member_relative_path"]
        data = read_regular(source, name)
        if sha(data) != m["member_sha256"] or len(data) != m["member_bytes"]:
            raise ValueError(f"CORPUS_IDENTITY_CONFLICT: {name}")
        planned["data/" + name] = data
        source_members.append(
            {"path": CORPUS + "/" + name, "sha256": sha(data), "bytes": len(data)}
        )
    # Authored shells are build inputs. Their exact bytes are frozen in the output manifest.
    assets = {name: read_regular(output, name) for name in ASSETS}
    for name, data in assets.items():
        data.decode("utf-8")
        if b"\x00" in data:
            raise ValueError(f"INVALID_STATIC_ASSET: {name}")
    health = {
        "status": "ok",
        "mode": "RECORDED_RUN_REPLAY",
        "live": False,
        "corpus_root_sha256": CORPUS_ROOT,
        "scenario_count": 4,
        "owner_database": False,
        "provider_inference": False,
    }
    planned["health.json"] = encoded(health)
    manifest = {
        "schema": "AISCC-PUBLIC-REPLAY-BUILD-V1",
        "version": 1,
        "mode": "RECORDED_RUN_REPLAY",
        "live": False,
        "source_commit": BASELINE,
        "source_commit_note": (
            "Pre-implementation baseline; final persistence/deployment commit must be verified "
            "by the later deployment Task. This manifest does not self-reference a future commit."
        ),
        "canonical_corpus_root_sha256": CORPUS_ROOT,
        "source_index": {
            "path": CORPUS + "/" + INDEX,
            "sha256": INDEX_SHA,
            "bytes": len(index_bytes),
        },
        "source_members": source_members,
        "public_copies": [
            {"path": name, "sha256": sha(data), "bytes": len(data)}
            for name, data in sorted(planned.items())
            if name.startswith("data/")
        ],
        "static_assets": [
            {"path": name, "sha256": sha(data), "bytes": len(data)}
            for name, data in sorted(assets.items())
        ],
        "health": {
            "path": "health.json",
            "sha256": sha(planned["health.json"]),
            "bytes": len(planned["health.json"]),
        },
        "generator_sha256": sha(read_regular(root, "scripts/build_public_replay.py")),
        "owner_db_dependency": False,
        "provider_dependency": False,
        "secret_dependency": False,
        "deployment_target_direction": "Cloudflare Pages",
        "deployment_status": "NOT_DEPLOYED",
    }
    planned["PUBLIC_REPLAY_BUILD_MANIFEST.json"] = encoded(manifest)
    expected = set(ASSETS) | set(planned)
    existing = {p.relative_to(output).as_posix() for p in output.rglob("*") if p.is_file()}
    if existing - expected:
        raise ValueError("UNEXPECTED_PUBLIC_FILE: " + ", ".join(sorted(existing - expected)))
    for name in expected:
        path = output / name
        if path.is_symlink() or not path.resolve().is_relative_to(output.resolve()):
            raise ValueError(f"UNSAFE_OUTPUT_PATH: {name}")
    drift = [
        name
        for name, data in planned.items()
        if not (output / name).exists() or (output / name).read_bytes() != data
    ]
    if check and drift:
        raise ValueError("PUBLIC_REPLAY_DRIFT: " + ", ".join(drift))
    if not check:
        for name, data in planned.items():
            path = output / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    return {
        "status": "PASS",
        "check": check,
        "scenario_count": 4,
        "file_count": len(expected),
        "corpus_root_sha256": CORPUS_ROOT,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Verify without writing; fail on drift"
    )
    args = parser.parse_args()
    try:
        result = build(Path(__file__).resolve().parents[1], check=args.check)
    except (ValueError, KeyError, OSError) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
