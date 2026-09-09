"""B1 unit materialization, synthetic authority refs, no scenario/tool execution."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
from types import SimpleNamespace

import pytest

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.runtime import stockroom_materializer as module
from aiscc.runtime.stockroom_materializer import StockroomMaterializer, operation_fingerprint
from aiscc.runtime.stockroom_workspace import StockroomWorkspace
from aiscc.scenarios.models import RESOURCE_REF, Resource
from aiscc.scenarios.runtime_models import (
    MaterializationAuthority,
    StockroomFailure,
    StockroomRunBinding,
    StockroomWorkspaceLease,
    WorkspaceOwnership,
)

REPOSITORY = Path(__file__).resolve().parents[3]
# parents: runtime -> unit -> tests -> repository
GIT = Path(shutil.which("git") or "git").resolve()


def setup_materializer(
    tmp_path: Path,
) -> tuple[
    StockroomMaterializer, StockroomWorkspace, StockroomRunBinding, MaterializationAuthority
]:
    root = tmp_path / "runtime"
    root.mkdir()
    workspace = StockroomWorkspace(
        root,
        repository_root=REPOSITORY,
        source_object_root=REPOSITORY / ".git",
        downloads_root=tmp_path / "downloads",
    )
    binding = StockroomRunBinding(
        RuntimeMode.OWNER_SELF_DOGFOOD,
        "stockroom-s1-normal",
        "1.0.0",
        RESOURCE_REF,
        "unit-run",
        "attempt-1",
        WorkflowState.RUNNING,
        2,
        "synthetic-b1-profile",
        "a" * 64,
    )
    authority = MaterializationAuthority(
        binding,
        "system:synthetic-unit",
        "synthetic:admission",
        "synthetic:repository-grant",
        "synthetic:filesystem-grant",
        operation_fingerprint(binding, REPOSITORY, root),
        REPOSITORY,
        root,
    )
    materializer = StockroomMaterializer(
        repository_root=REPOSITORY,
        git_executable=GIT,
        workspace=workspace,
        registered_authorities=(authority,),
        current_binding=lambda: binding,
    )
    return materializer, workspace, binding, authority


def resource() -> Resource:
    return Resource.model_validate_json(
        (REPOSITORY / "config/scenarios/stockroom/v1/resource.json").read_bytes()
    )


def primary_identity() -> tuple[bytes, bytes, bytes]:
    index = (REPOSITORY / ".git/index").read_bytes()
    status = subprocess.check_output(
        [str(GIT), "-C", str(REPOSITORY), "status", "--porcelain=v1", "--untracked-files=all"],
        env={**module.os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    )
    # Status alone would miss changes to already-untracked candidate bytes.
    paths = subprocess.check_output(
        [
            str(GIT),
            "-C",
            str(REPOSITORY),
            "ls-files",
            "-z",
            "--cached",
            "--others",
            "--exclude-standard",
        ],
        env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"},
    ).split(b"\0")
    digest = hashlib.sha256()
    for relative in sorted(p for p in paths if p):
        data = (REPOSITORY / relative.decode("utf-8")).read_bytes()
        digest.update(relative + b"\0" + hashlib.sha256(data).digest())
    return hashlib.sha256(index).digest(), status, digest.digest()


def test_pinned_materialization_exact_provenance(tmp_path: Path) -> None:
    materializer, workspace, binding, authority = setup_materializer(tmp_path)
    before = primary_identity()
    expected = resource()
    result = materializer.materialize(binding, authority)
    assert result.resource_ref == RESOURCE_REF
    assert result.source_commit == expected.source_commit
    assert result.subroot == expected.subroot
    assert result.git_subtree == expected.git_subtree
    assert result.aggregate_sha256 == expected.aggregate_sha256
    assert (result.run_id, result.attempt_id) == (binding.run_id, binding.attempt_id)
    assert result.resolved_source_root == result.workspace_lease.destination
    assert len(result.files) == 14
    assert tuple(f.path for f in result.files) == tuple(f.path for f in expected.files)
    for actual, item in zip(result.files, expected.files, strict=True):
        data = (result.resolved_source_root / item.path).read_bytes()
        assert actual.mode == "100644"
        assert actual.bytes == len(data) == item.bytes
        assert actual.sha256 == hashlib.sha256(data).hexdigest() == item.sha256
    with pytest.raises(FrozenInstanceError):
        result.run_id = "other"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        authority.security_admission_ref = "other"  # type: ignore[misc]
    with pytest.raises(StockroomFailure, match="^DESTINATION_ALREADY_USED$"):
        materializer.materialize(binding, authority)
    assert primary_identity() == before
    assert workspace.cleanup(result.workspace_lease).ownership is WorkspaceOwnership.CLEANED
    assert not result.workspace_lease.destination.parent.exists()
    assert primary_identity() == before


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("mode", RuntimeMode.PUBLIC_BOUNDED_LIVE),
        ("mode", RuntimeMode.PUBLIC_RECORDED_REPLAY),
        ("state", WorkflowState.READY),
        ("state", WorkflowState.ACCEPTED),
        ("state_version", 0),
        ("state_version", True),
        ("state_version", 3),
        ("resource_ref", "repository:latest"),
        ("scenario_id", "unknown"),
        ("scenario_version", "2.0.0"),
        ("profile_version", ""),
        ("config_sha256", "bad"),
        ("run_id", "../escape"),
        ("attempt_id", "C:escape"),
    ],
)
def test_binding_denied_before_allocation(tmp_path: Path, field: str, value: object) -> None:
    materializer, workspace, binding, authority = setup_materializer(tmp_path)
    changed = replace(binding, **{field: value})
    expected = (
        "UNSAFE_PATH_COMPONENT"
        if field in {"run_id", "attempt_id"}
        else "AUTHORITY_OR_CURRENT_BINDING_MISMATCH"
        if field == "state_version" and value == 3
        else "INVALID_RUN_BINDING"
    )
    with pytest.raises(StockroomFailure, match=f"^{expected}$"):
        materializer.materialize(changed, authority)
    assert not tuple(workspace.root.iterdir())


def test_registered_identity_and_live_binding_required(tmp_path: Path) -> None:
    materializer, workspace, binding, authority = setup_materializer(tmp_path)
    for forged in (replace(authority), True, None):
        with pytest.raises(StockroomFailure, match="^AUTHORITY_OR_CURRENT_BINDING_MISMATCH$"):
            materializer.materialize(binding, forged)  # type: ignore[arg-type]
    materializer._current_binding = lambda: replace(binding, state_version=3)
    with pytest.raises(StockroomFailure, match="^AUTHORITY_OR_CURRENT_BINDING_MISMATCH$"):
        materializer.materialize(binding, authority)
    assert not tuple(workspace.root.iterdir())


@pytest.mark.parametrize(
    "field",
    [
        "principal_ref",
        "security_admission_ref",
        "repository_grant_ref",
        "filesystem_grant_ref",
        "operation_fingerprint",
        "repository_root",
        "runtime_root",
    ],
)
def test_authority_exact_fields(tmp_path: Path, field: str) -> None:
    materializer, workspace, binding, authority = setup_materializer(tmp_path)
    bad = replace(authority, **{field: tmp_path if field.endswith("root") else ""})
    materializer._authorities = (bad,)
    expected = (
        "AUTHORITY_OR_CURRENT_BINDING_MISMATCH"
        if field in {"operation_fingerprint", "repository_root", "runtime_root"}
        else "EXACT_AUTHORITY_REFS_REQUIRED"
    )
    with pytest.raises(StockroomFailure, match=f"^{expected}$"):
        materializer.materialize(binding, bad)
    assert not tuple(workspace.root.iterdir())


@pytest.mark.parametrize(
    "case",
    ["commit", "subtree", "missing", "extra", "mode", "size", "sha", "aggregate", "traversal"],
)
def test_static_manifest_revalidation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, case: str
) -> None:
    materializer, workspace, binding, authority = setup_materializer(tmp_path)
    raw = json.loads((REPOSITORY / "config/scenarios/stockroom/v1/resource.json").read_bytes())
    if case == "commit":
        raw["source_commit"] = "0" * 40
    elif case == "subtree":
        raw["git_subtree"] = "0" * 40
    elif case == "missing":
        raw["files"].pop()
    elif case == "extra":
        raw["files"].append(raw["files"][0])
    elif case == "mode":
        raw["files"][0]["mode"] = "120000"
    elif case == "size":
        raw["files"][0]["bytes"] += 1
    elif case == "sha":
        raw["files"][0]["sha256"] = "0" * 64
    elif case == "aggregate":
        raw["aggregate_sha256"] = "0" * 64
    elif case == "traversal":
        raw["files"][0]["path"] = "../outside"
    fixture = tmp_path / "resource.json"
    fixture.write_text(json.dumps(raw), encoding="utf-8")
    original = module.checked_absolute

    def redirected(path: Path) -> Path:
        return fixture if path.name == "resource.json" else original(path)

    monkeypatch.setattr(module, "checked_absolute", redirected)
    with pytest.raises(StockroomFailure, match="^RESOURCE_MANIFEST_INVALID$"):
        materializer.materialize(binding, authority)
    assert not tuple(workspace.root.iterdir())


@pytest.mark.parametrize(
    "case",
    [
        "commit-type",
        "tree-type",
        "subtree",
        "missing-object",
        "mode",
        "symlink",
        "gitlink",
        "tree-file",
        "duplicate",
        "case-duplicate",
        "traversal",
        "absolute",
        "drive",
        "unc",
        "ads",
        "device",
        "trailing",
        "backslash",
        "path-set",
        "missing",
        "extra",
        "nonterminated",
        "wrong-size",
        "wrong-sha",
        "timeout",
        "nonzero",
        "ambiguous",
    ],
)
def test_bad_objects_no_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, case: str
) -> None:
    materializer, workspace, binding, authority = setup_materializer(tmp_path)
    original = materializer._read_git
    reached: list[tuple[str, ...]] = []
    reasons = {
        "commit-type": "WRONG_COMMIT_TYPE",
        "tree-type": "WRONG_TREE_TYPE",
        "subtree": "WRONG_SUBTREE",
        "missing-object": "GIT_NONZERO",
        "mode": "UNSAFE_OBJECT_MODE_OR_TYPE",
        "symlink": "UNSAFE_OBJECT_MODE_OR_TYPE",
        "gitlink": "UNSAFE_OBJECT_MODE_OR_TYPE",
        "tree-file": "UNSAFE_OBJECT_MODE_OR_TYPE",
        "duplicate": "DUPLICATE_OBJECT_PATH",
        "case-duplicate": "DUPLICATE_OBJECT_PATH",
        "traversal": "UNSAFE_PATH_COMPONENT",
        "absolute": "UNSAFE_PATH_COMPONENT",
        "drive": "UNSAFE_PATH_COMPONENT",
        "unc": "UNSAFE_PATH_COMPONENT",
        "ads": "UNSAFE_PATH_COMPONENT",
        "device": "UNSAFE_PATH_COMPONENT",
        "trailing": "UNSAFE_PATH_COMPONENT",
        "backslash": "UNSAFE_PATH_COMPONENT",
        "path-set": "MANIFEST_PATH_SET_MISMATCH",
        "missing": "TREE_FILE_COUNT",
        "extra": "TREE_FILE_COUNT",
        "nonterminated": "AMBIGUOUS_TREE_LISTING",
        "wrong-size": "SOURCE_BYTE_IDENTITY_MISMATCH",
        "wrong-sha": "SOURCE_BYTE_IDENTITY_MISMATCH",
        "timeout": "GIT_TIMEOUT",
        "nonzero": "GIT_NONZERO",
        "ambiguous": "GIT_AMBIGUOUS_OR_OVERSIZED_READ",
    }

    def faulty(args: tuple[str, ...], limit: int) -> bytes:
        reached.append(args)
        if case in {"timeout", "nonzero", "ambiguous", "missing-object"}:
            raise StockroomFailure(reasons[case])
        data = original(args, limit)
        if args[:2] == ("cat-file", "-t"):
            if case == "commit-type" and args[-1] == module._COMMIT:
                return b"blob\n"
            if case == "tree-type" and args[-1] == module._TREE:
                return b"commit\n"
        if case == "subtree" and args[0] == "rev-parse":
            return b"0" * 40 + b"\n"
        if args[0] == "ls-tree":
            rows = data[:-1].split(b"\0")
            if case in {"mode", "symlink", "gitlink", "tree-file"}:
                prefix = {
                    "mode": b"100755 blob",
                    "symlink": b"120000 blob",
                    "gitlink": b"160000 commit",
                    "tree-file": b"040000 tree",
                }[case]
                rows[0] = rows[0].replace(b"100644 blob", prefix)
            paths = {
                "traversal": b"../outside",
                "absolute": b"/outside",
                "drive": b"C:/outside",
                "unc": b"\\\\host\\share",
                "ads": b"file:stream",
                "device": b"CON.txt",
                "trailing": b"file.",
                "backslash": b"a\\b",
                "path-set": b"other",
            }
            if case in paths:
                rows[0] = rows[0].split(b"\t")[0] + b"\t" + paths[case]
            if case in {"duplicate", "case-duplicate"}:
                rows[1] = (
                    rows[0] if case == "duplicate" else rows[0].split(b"\t")[0] + b"\t.GITIGNORE"
                )
            if case == "missing":
                rows.pop()
            if case == "extra":
                rows.append(rows[0])
            return b"\0".join(rows) + (b"" if case == "nonterminated" else b"\0")
        if args[:2] == ("cat-file", "blob"):
            if case == "wrong-size":
                return data + b"x"
            if case == "wrong-sha":
                return bytes([data[0] ^ 1]) + data[1:]
        return data

    monkeypatch.setattr(materializer, "_read_git", faulty)
    with pytest.raises(StockroomFailure, match=f"^{reasons[case]}$"):
        materializer.materialize(binding, authority)
    assert reached
    if case in {"wrong-size", "wrong-sha"}:
        assert reached[-1][:2] == ("cat-file", "blob")
    elif case not in {
        "commit-type",
        "tree-type",
        "subtree",
        "timeout",
        "nonzero",
        "ambiguous",
        "missing-object",
    }:
        assert reached[-1][0] == "ls-tree"
    assert not tuple(workspace.root.iterdir())


@pytest.mark.parametrize("kind", ["write", "verify", "state-change", "unexpected-residue"])
def test_partial_failure_exact_cleanup_or_quarantine(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, kind: str
) -> None:
    materializer, workspace, binding, authority = setup_materializer(tmp_path)
    before = primary_identity()
    write = workspace.write_file
    count = 0

    def failing_write(lease: StockroomWorkspaceLease, path: str, data: bytes) -> None:
        nonlocal count
        count += 1
        if count == 3:
            if kind == "write":
                raise OSError("synthetic write failure")
            if kind == "state-change":
                materializer._current_binding = lambda: replace(binding, state_version=3)
            if kind == "unexpected-residue":
                (lease.destination / "unexpected").write_bytes(b"keep")
        assert lease.destination.is_dir()
        write(lease, path, data)

    monkeypatch.setattr(workspace, "write_file", failing_write)
    if kind == "verify":
        monkeypatch.setattr(workspace, "read_files", lambda lease: ())
    reasons = {
        "write": "DESTINATION_WRITE_OR_VERIFY_FAILED",
        "verify": "DESTINATION_MANIFEST_MISMATCH",
        "state-change": "AUTHORITY_OR_CURRENT_BINDING_MISMATCH",
        "unexpected-residue": "UNEXPECTED_RESIDUE",
    }
    with pytest.raises(StockroomFailure, match=f"^{reasons[kind]}$") as caught:
        materializer.materialize(binding, authority)
    assert count == (14 if kind == "verify" else 3)
    cleanup = caught.value.cleanup
    assert cleanup is not None
    if kind == "unexpected-residue":
        assert cleanup.ownership is WorkspaceOwnership.QUARANTINED
        assert (cleanup.destination / "unexpected").read_bytes() == b"keep"
    else:
        assert cleanup.ownership is WorkspaceOwnership.CLEANED
        assert not cleanup.destination.parent.exists()
    assert primary_identity() == before
    with pytest.raises(StockroomFailure, match="^DESTINATION_ALREADY_USED$"):
        workspace.allocate(binding.run_id, binding.attempt_id)


def test_git_reader_real_bound_and_environment(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    materializer, _, _, _ = setup_materializer(tmp_path)
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "wrong"))
    monkeypatch.setenv("GIT_OBJECT_DIRECTORY", str(tmp_path / "wrong"))
    monkeypatch.setenv("GIT_CONFIG_COUNT", "1")
    monkeypatch.setenv("GIT_CONFIG_KEY_0", "core.bare")
    monkeypatch.setenv("GIT_CONFIG_VALUE_0", "true")
    assert materializer._read_git(("cat-file", "-t", module._COMMIT), 16) == b"commit\n"
    with pytest.raises(StockroomFailure, match="GIT_AMBIGUOUS_OR_OVERSIZED_READ"):
        materializer._read_git(("cat-file", "-t", module._COMMIT), 1)
    with pytest.raises(StockroomFailure, match="GIT_NONZERO"):
        materializer._read_git(("cat-file", "-t", "0" * 40), 16)


def test_git_reader_timeout_branch(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    materializer, _, _, _ = setup_materializer(tmp_path)
    original = subprocess.Popen.wait
    first = True

    def timeout_once(self: subprocess.Popen[bytes], timeout: float | None = None) -> int:
        nonlocal first
        if first:
            first = False
            raise subprocess.TimeoutExpired("synthetic-fixed-git", timeout or 1)
        return original(self, timeout=timeout)

    monkeypatch.setattr(subprocess.Popen, "wait", timeout_once)
    with pytest.raises(StockroomFailure, match="GIT_TIMEOUT"):
        materializer._read_git(("cat-file", "-t", module._COMMIT), 16)


def test_real_configured_git_executable_identity() -> None:
    info = GIT.lstat()
    assert stat.S_ISREG(info.st_mode)
    assert not getattr(info, "st_file_attributes", 0) & 0x400
    assert info.st_nlink >= 1
    assert module._trusted_git_executable(GIT) == GIT


def test_trusted_executable_hardlink_exception_is_endpoint_only(tmp_path: Path) -> None:
    original = tmp_path / "original"
    original.write_bytes(b"Synthetic validation fixture; never execute")
    original.chmod(0o700)
    candidate = tmp_path / "git.exe"
    try:
        os.link(original, candidate)
    except OSError as exc:
        pytest.skip(f"Host cannot create executable-fixture hardlink: {type(exc).__name__}")
    assert candidate.lstat().st_nlink > 1
    assert module._trusted_git_executable(candidate) == candidate
    with pytest.raises(StockroomFailure, match="^HARDLINK_DENIED$"):
        module.checked_absolute(candidate)


@pytest.mark.parametrize(
    ("case", "reason"),
    [
        ("relative", "TRUSTED_GIT_ABSOLUTE_LOCAL_PATH_REQUIRED"),
        ("unc", "TRUSTED_GIT_ABSOLUTE_LOCAL_PATH_REQUIRED"),
        ("missing", "TRUSTED_GIT_MISSING_OR_CASE_AMBIGUOUS"),
        ("name", "TRUSTED_GIT_NAME_REQUIRED"),
        ("directory", "TRUSTED_GIT_REGULAR_FILE_REQUIRED"),
        ("case", "TRUSTED_GIT_MISSING_OR_CASE_AMBIGUOUS"),
        ("traversal", "UNSAFE_PATH_COMPONENT"),
    ],
)
def test_trusted_executable_invalid_path(tmp_path: Path, case: str, reason: str) -> None:
    candidate = tmp_path / "git.exe"
    if case == "relative":
        candidate = Path("git.exe")
    elif case == "unc":
        candidate = Path("\\\\untrusted\\share\\git.exe")
    elif case == "name":
        candidate = tmp_path / "other.exe"
    elif case == "directory":
        candidate.mkdir()
    elif case == "case":
        candidate.write_bytes(b"fixture")
        candidate = tmp_path / "GIT.exe"
    elif case == "traversal":
        candidate = tmp_path / ".." / "git.exe"
    with pytest.raises(StockroomFailure, match=f"^{reason}$"):
        module._trusted_git_executable(candidate)


@pytest.mark.parametrize("kind", ["special", "reparse", "zero-links", "no-execute", "resolution"])
def test_trusted_executable_metadata_guards(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, kind: str
) -> None:
    candidate = tmp_path / "git.exe"
    candidate.write_bytes(b"Metadata branch fixture; never execute")
    candidate.chmod(0o700)
    original_stat = Path.lstat
    original_resolve = Path.resolve
    info = candidate.lstat()

    def fake_stat(path: Path) -> object:
        if path == candidate:
            return SimpleNamespace(
                st_mode=stat.S_IFIFO if kind == "special" else info.st_mode,
                st_nlink=0 if kind == "zero-links" else info.st_nlink,
                st_file_attributes=0x400 if kind == "reparse" else 0,
            )
        return original_stat(path)

    def fake_resolve(path: Path, strict: bool = False) -> Path:
        if path == candidate and kind == "resolution":
            return tmp_path / "other.exe"
        return original_resolve(path, strict=strict)

    if kind in {"special", "reparse", "zero-links"}:
        monkeypatch.setattr(Path, "lstat", fake_stat)
    if kind == "no-execute":
        monkeypatch.setattr(module.os, "access", lambda path, mode: False)
    if kind == "resolution":
        monkeypatch.setattr(Path, "resolve", fake_resolve)
    expected = {
        "special": "TRUSTED_GIT_REGULAR_FILE_REQUIRED",
        "reparse": "TRUSTED_GIT_LINK_OR_REPARSE_DENIED",
        "zero-links": "TRUSTED_GIT_REGULAR_FILE_REQUIRED",
        "no-execute": "TRUSTED_GIT_EXECUTABLE_ACCESS_REQUIRED",
        "resolution": "TRUSTED_GIT_RESOLUTION_MISMATCH",
    }[kind]
    with pytest.raises(StockroomFailure, match=f"^{expected}$"):
        module._trusted_git_executable(candidate)


def test_trusted_executable_symlink_denied(tmp_path: Path) -> None:
    target = tmp_path / "target"
    target.write_bytes(b"Never execute")
    candidate = tmp_path / "git.exe"
    try:
        candidate.symlink_to(target)
    except OSError as exc:
        pytest.skip(f"Host cannot create executable symlink: {type(exc).__name__}")
    with pytest.raises(StockroomFailure, match="^TRUSTED_GIT_LINK_OR_REPARSE_DENIED$"):
        module._trusted_git_executable(candidate)


@pytest.mark.parametrize("overlap", ["repository", "runtime"])
def test_trusted_executable_overlap_still_denied(tmp_path: Path, overlap: str) -> None:
    repository = tmp_path / "repository"
    (repository / ".git").mkdir(parents=True)
    root = tmp_path / "runtime"
    root.mkdir()
    workspace = StockroomWorkspace(
        root,
        repository_root=repository,
        source_object_root=repository / ".git",
        downloads_root=tmp_path / "downloads",
    )
    candidate = (repository if overlap == "repository" else root) / "git.exe"
    candidate.write_bytes(b"Synthetic validation only; never execute")
    candidate.chmod(0o700)
    assert module._trusted_git_executable(candidate) == candidate
    materializer = StockroomMaterializer(
        repository_root=repository,
        git_executable=candidate,
        workspace=workspace,
        registered_authorities=(),
        current_binding=lambda: None,  # type: ignore[arg-type,return-value]
    )
    with pytest.raises(StockroomFailure, match="^UNTRUSTED_LOCAL_GIT_CONFIGURATION$"):
        materializer._configuration()
