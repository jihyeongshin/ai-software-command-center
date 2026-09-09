from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from aiscc.scenarios import ContractError, load_catalog, manifest_sha256
from aiscc.scenarios.models import ResourceFile

CONFIG = Path(__file__).resolve().parents[3] / "config/scenarios/stockroom/v1"
EXPECTED = "be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d"


def test_accepted_manifest_identity_without_runtime_source_reads() -> None:
    resource = load_catalog(CONFIG / "catalog.json").resource
    assert resource.file_count == len(resource.files) == 14
    assert tuple(f.path for f in resource.files) == (
        ".gitignore",
        ".python-version",
        "PROVENANCE.md",
        "README.md",
        "stockroom/__init__.py",
        "stockroom/__main__.py",
        "stockroom/cli.py",
        "stockroom/data/catalog.json",
        "stockroom/inventory.py",
        "stockroom/model.py",
        "tests/test_cli.py",
        "tests/test_contract.py",
        "tests/test_inventory.py",
        "tools/build.py",
    )
    assert resource.source_commit == "05185c57a6265a4002050ce25cdfde3dc87e9779"
    assert resource.git_subtree == "f3d9203321ae3535abf8e92a7285da1067f6c55e"
    assert resource.aggregate_sha256 == resource.resource_version == EXPECTED
    assert manifest_sha256(resource.files) == EXPECTED
    assert all(f.mode == "100644" for f in resource.files)


def test_aggregate_has_exact_tabs_decimal_count_and_final_lf() -> None:
    file = ResourceFile(path="a.txt", mode="100644", bytes=12, sha256="a" * 64)
    expected = hashlib.sha256(b"100644\ta.txt\t12\t" + b"a" * 64 + b"\n").hexdigest()
    assert manifest_sha256((file,)) == expected
    with pytest.raises(ValueError):
        manifest_sha256((file, file))
    later = ResourceFile(path="z.txt", mode="100644", bytes=0, sha256="b" * 64)
    with pytest.raises(ValueError):
        manifest_sha256((later, file))


@pytest.mark.parametrize(
    "change",
    [
        lambda d: d.update(aggregate_sha256="0" * 64),
        lambda d: d.update(resource_version="latest"),
        lambda d: d.update(resource_version="1.0.0"),
        lambda d: d.update(resource_ref="repository:synthetic-stockroom@latest"),
        lambda d: d.update(file_count=13),
        lambda d: d.update(file_count="14"),
        lambda d: d.update(source_commit="0" * 40),
        lambda d: d.update(git_subtree="0" * 40),
        lambda d: d.update(subroot="../"),
        lambda d: d.update(extra="unknown"),
        lambda d: d["files"][0].update(sha256="A" * 64),
        lambda d: d["files"][0].update(sha256="a" * 63),
        lambda d: d["files"][0].update(sha256="0" * 64),
        lambda d: d["files"][0].update(mode="100755"),
        lambda d: d["files"][0].update(bytes=-1),
        lambda d: d["files"][0].update(bytes=True),
        lambda d: d["files"][0].update(bytes=1.0),
        lambda d: d["files"][0].update(extra=True),
        lambda d: d["files"][0].update(path="/absolute"),
        lambda d: d["files"][0].update(path="../escape"),
        lambda d: d["files"][0].update(path="a/../escape"),
        lambda d: d["files"].reverse(),
        lambda d: d["files"].__setitem__(1, d["files"][0]),
        lambda d: d["files"].pop(),
    ],
)
def test_inconsistent_resource_is_rejected(tmp_path: Path, change) -> None:
    pack = tmp_path / "pack"
    shutil.copytree(CONFIG, pack)
    path = pack / "resource.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    change(raw)
    path.write_text(json.dumps(raw), encoding="utf-8")
    with pytest.raises(ContractError):
        load_catalog(pack / "catalog.json")
