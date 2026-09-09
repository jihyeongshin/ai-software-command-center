"""B1 filesystem unit proof on pytest-owned paths; no sandbox admission claim."""

from __future__ import annotations

import os
import subprocess
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from aiscc.runtime.stockroom_workspace import StockroomWorkspace, checked_absolute, safe_component
from aiscc.scenarios.runtime_models import StockroomFailure, WorkspaceOwnership


def owner(tmp_path: Path) -> StockroomWorkspace:
    for name in ("runtime", "repository", "downloads"):
        (tmp_path / name).mkdir()
    (tmp_path / "repository/.git").mkdir()
    return StockroomWorkspace(
        tmp_path / "runtime",
        repository_root=tmp_path / "repository",
        source_object_root=tmp_path / "repository/.git",
        downloads_root=tmp_path / "downloads",
    )


def test_exclusive_exact_destination_and_immutable_lease(tmp_path: Path) -> None:
    workspace = owner(tmp_path)
    lease = workspace.allocate("run-1", "attempt-1")
    assert lease.destination == tmp_path / "runtime/run-1/attempt-1/source"
    assert lease.ownership is WorkspaceOwnership.OWNED
    with pytest.raises(FrozenInstanceError):
        lease.run_id = "other"  # type: ignore[misc]
    with pytest.raises(StockroomFailure):
        workspace.allocate("run-1", "attempt-1")
    next_lease = workspace.allocate("run-1", "attempt-2")
    other = workspace.allocate("run-2", "attempt-1")
    assert len({lease.destination, next_lease.destination, other.destination}) == 3


@pytest.mark.parametrize(
    "value",
    [
        "..",
        ".",
        "",
        "a/../b",
        "/tmp",
        "C:\\x",
        "C:x",
        "\\\\host\\share",
        "x:y",
        "CON",
        "nul.txt",
        "COM1.log",
        "lpt9",
        "aux",
        "a.",
        "a ",
        "a\\b",
        "a/b",
        "a\x00b",
        "-" * 101,
        "COM¹",
    ],
)
def test_unsafe_components(value: str) -> None:
    with pytest.raises(StockroomFailure):
        safe_component(value)


@pytest.mark.parametrize("target", ["repository", "repository/.git", "downloads"])
def test_excluded_roots(tmp_path: Path, target: str) -> None:
    owner(tmp_path)
    with pytest.raises(StockroomFailure, match="RUNTIME_ROOT_OVERLAP"):
        StockroomWorkspace(
            tmp_path / target,
            repository_root=tmp_path / "repository",
            source_object_root=tmp_path / "repository/.git",
            downloads_root=tmp_path / "downloads",
        )


def test_distinct_object_store_overlap(tmp_path: Path) -> None:
    workspace = owner(tmp_path)
    with pytest.raises(StockroomFailure, match="RUNTIME_ROOT_OVERLAP"):
        StockroomWorkspace(
            workspace.root,
            repository_root=tmp_path / "repository",
            source_object_root=workspace.root,
            downloads_root=tmp_path / "downloads",
        )


def test_case_collision_and_unexpected_sibling(tmp_path: Path) -> None:
    workspace = owner(tmp_path)
    lease = workspace.allocate("run", "attempt")
    with pytest.raises(StockroomFailure):
        workspace.allocate("RUN", "other")
    with pytest.raises(StockroomFailure):
        workspace.allocate("run", "ATTEMPT")
    workspace.write_file(lease, "dir/file", b"ok")
    with pytest.raises(StockroomFailure):
        workspace.write_file(lease, "DIR/other", b"bad")
    (workspace.root / "unexpected").mkdir()
    with pytest.raises(StockroomFailure):
        workspace.allocate("next", "attempt")
    assert workspace.cleanup(lease).ownership is WorkspaceOwnership.QUARANTINED


def test_existing_attempt_object_denied(tmp_path: Path) -> None:
    workspace = owner(tmp_path)
    workspace.allocate("run", "attempt")
    (workspace.root / "run/unknown").mkdir()
    with pytest.raises(StockroomFailure):
        workspace.allocate("run", "unknown")


def test_unknown_existing_root_denied(tmp_path: Path) -> None:
    workspace = owner(tmp_path)
    (workspace.root / "unknown").write_text("untouched", encoding="utf-8")
    with pytest.raises(StockroomFailure):
        StockroomWorkspace(
            workspace.root,
            repository_root=tmp_path / "repository",
            source_object_root=tmp_path / "repository/.git",
            downloads_root=tmp_path / "downloads",
        )


def test_exact_cleanup_and_no_reuse(tmp_path: Path) -> None:
    workspace = owner(tmp_path)
    lease = workspace.allocate("run", "attempt")
    sibling = workspace.allocate("other", "attempt")
    workspace.write_file(lease, "a/b.txt", b"verified")
    workspace.write_file(sibling, "keep.txt", b"keep")
    assert workspace.read_files(lease) == (("a/b.txt", b"verified"),)
    assert workspace.cleanup(lease).ownership is WorkspaceOwnership.CLEANED
    assert not lease.destination.parent.exists()
    assert (sibling.destination / "keep.txt").read_bytes() == b"keep"
    with pytest.raises(StockroomFailure):
        workspace.allocate("run", "attempt")


def test_forged_and_cross_run_lease_refused(tmp_path: Path) -> None:
    workspace = owner(tmp_path)
    lease = workspace.allocate("run", "attempt")
    sibling = workspace.allocate("other", "attempt")
    for forged in (
        replace(lease),
        replace(lease, destination=sibling.destination),
        replace(lease, run_id="other"),
    ):
        assert workspace.cleanup(forged).ownership is WorkspaceOwnership.QUARANTINED
        with pytest.raises(StockroomFailure):
            workspace.write_file(forged, "x", b"bad")
    assert lease.destination.exists() and sibling.destination.exists()
    assert workspace.cleanup(lease).ownership is WorkspaceOwnership.CLEANED


def test_unknown_residue_quarantines_without_deleting(tmp_path: Path) -> None:
    workspace = owner(tmp_path)
    lease = workspace.allocate("run", "attempt")
    unknown = lease.destination / "unknown"
    unknown.write_bytes(b"keep")
    assert workspace.cleanup(lease).ownership is WorkspaceOwnership.QUARANTINED
    assert unknown.read_bytes() == b"keep"
    with pytest.raises(StockroomFailure):
        workspace.write_file(lease, "x", b"bad")


def test_delete_failure_quarantines(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    workspace = owner(tmp_path)
    lease = workspace.allocate("run", "attempt")
    workspace.write_file(lease, "file", b"keep")

    def fail(*args: object, **kwargs: object) -> None:
        raise PermissionError("synthetic deletion failure")

    monkeypatch.setattr(Path, "unlink", fail)
    assert workspace.cleanup(lease).ownership is WorkspaceOwnership.QUARANTINED
    assert (lease.destination / "file").exists()


def test_symlink_escape_refused(tmp_path: Path) -> None:
    workspace = owner(tmp_path)
    lease = workspace.allocate("run", "attempt")
    link = lease.destination / "link"
    try:
        link.symlink_to(tmp_path / "downloads", target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"Host cannot create directory symlinks: {type(exc).__name__}")
    with pytest.raises(StockroomFailure):
        workspace.write_file(lease, "link/escape", b"bad")
    assert workspace.cleanup(lease).ownership is WorkspaceOwnership.QUARANTINED
    assert not (tmp_path / "downloads/escape").exists()


@pytest.mark.skipif(os.name != "nt", reason="Windows junction primitive required")
def test_windows_junction_ancestor_denied(tmp_path: Path) -> None:
    workspace = owner(tmp_path)
    junction = tmp_path / "junction"
    result = subprocess.run(
        [os.environ["COMSPEC"], "/d", "/c", "mklink", "/J", str(junction), str(workspace.root)],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        pytest.skip("Host denied creation of pytest-owned junction")
    try:
        with pytest.raises(StockroomFailure, match="LINK_OR_REPARSE_DENIED"):
            checked_absolute(junction)
    finally:
        junction.rmdir()


def test_destination_tamper_and_hardlink_denied(tmp_path: Path) -> None:
    workspace = owner(tmp_path)
    lease = workspace.allocate("run", "attempt")
    workspace.write_file(lease, "file", b"original")
    (lease.destination / "file").write_bytes(b"changed")
    with pytest.raises(StockroomFailure, match="DESTINATION_BYTES_CHANGED"):
        workspace.read_files(lease)
    try:
        os.link(lease.destination / "file", tmp_path / "hardlink")
    except OSError as exc:
        pytest.skip(f"Host cannot create hardlinks: {type(exc).__name__}")
    assert workspace.cleanup(lease).ownership is WorkspaceOwnership.QUARANTINED
