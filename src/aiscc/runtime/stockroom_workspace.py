"""Exclusive B1 workspace owner for a private operator-provisioned directory.

No requester path, broad cleanup, recovery adoption, or shared-writer support.
The operator must keep ancestors private; these checks are not an OS sandbox.
After restart existing entries are unknown and cannot be adopted or reused.
"""

from __future__ import annotations

import hashlib
import os
import re
import stat
from pathlib import Path
from threading import RLock
from uuid import uuid4

from aiscc.scenarios.runtime_models import (
    StockroomFailure,
    StockroomWorkspaceLease,
    WorkspaceCleanupDisposition,
    WorkspaceOwnership,
)

_DEVICES = {"CON", "PRN", "AUX", "NUL", "CLOCK$", "CONIN$", "CONOUT$"} | {
    f"{prefix}{n}" for prefix in ("COM", "LPT") for n in range(1, 10)
}
_MAX_FILE_BYTES = 64 * 1024
_MAX_FILES = 14


def safe_component(value: str) -> str:
    if (
        type(value) is not str
        or not re.fullmatch(r"[A-Za-z0-9_.-]{1,100}", value)
        or value in {".", ".."}
        or value.endswith((".", " "))
        or value.split(".")[0].upper() in _DEVICES
    ):
        raise StockroomFailure("UNSAFE_PATH_COMPONENT")
    return value


def safe_relative(value: str) -> tuple[str, ...]:
    if type(value) is not str or len(value) > 240:
        raise StockroomFailure("UNSAFE_SOURCE_PATH")
    parts = tuple(safe_component(part) for part in value.split("/"))
    if any(part.casefold() == ".git" for part in parts):
        raise StockroomFailure("GIT_METADATA_PATH_DENIED")
    return parts


def _identity(path: Path) -> tuple[int, int, int]:
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
        raise StockroomFailure("LINK_OR_REPARSE_DENIED")
    if not (stat.S_ISDIR(info.st_mode) or stat.S_ISREG(info.st_mode)):
        raise StockroomFailure("SPECIAL_OBJECT_DENIED")
    if stat.S_ISREG(info.st_mode) and info.st_nlink != 1:
        raise StockroomFailure("HARDLINK_DENIED")
    return info.st_dev, info.st_ino, stat.S_IFMT(info.st_mode)


def checked_absolute(path: Path) -> Path:
    """Inspect lexical ancestors before resolution, including Windows aliases."""
    if not isinstance(path, Path) or not path.is_absolute() or str(path).startswith("\\\\"):
        raise StockroomFailure("ABSOLUTE_LOCAL_CONFIG_PATH_REQUIRED")
    current = Path(path.anchor)
    _identity(current)
    for part in path.parts[1:]:
        # Operator paths can contain interior spaces (e.g. Program Files).
        safe_component(part.replace(" ", "_"))
        if part.endswith(" "):
            raise StockroomFailure("AMBIGUOUS_CONFIG_PATH")
        matches = [p.name for p in current.iterdir() if p.name.casefold() == part.casefold()]
        if matches != [part]:
            raise StockroomFailure("MISSING_OR_CASE_AMBIGUOUS_PATH")
        current /= part
        _identity(current)
    if current.resolve(strict=True) != current:
        raise StockroomFailure("RESOLUTION_MISMATCH")
    return current


def _overlaps(left: Path, right: Path) -> bool:
    a, b = str(left).casefold(), str(right).casefold()
    return a == b or a.startswith(b + os.sep) or b.startswith(a + os.sep)


class StockroomWorkspace:
    def __init__(
        self,
        runtime_root: Path,
        *,
        repository_root: Path,
        source_object_root: Path,
        downloads_root: Path,
    ) -> None:
        self._lock = RLock()
        self.root = checked_absolute(runtime_root)
        self.repository_root = checked_absolute(repository_root)
        self.source_object_root = checked_absolute(source_object_root)
        # Downloads may not exist, but must still be an absolute unambiguous exclusion.
        if not downloads_root.is_absolute():
            raise StockroomFailure("DOWNLOADS_CONFIG_REQUIRED")
        for part in downloads_root.parts[1:]:
            safe_component(part)
        for excluded in (
            self.repository_root,
            self.repository_root / ".git",
            self.source_object_root,
            downloads_root.resolve(),
            Path.home() / "Downloads",
        ):
            if _overlaps(self.root, excluded):
                raise StockroomFailure("RUNTIME_ROOT_OVERLAP")
        if not self.root.is_dir() or tuple(self.root.iterdir()):
            raise StockroomFailure("RUNTIME_ROOT_NOT_EMPTY")
        self._root_identity = _identity(self.root)
        self._runs: dict[str, tuple[int, int, int]] = {}
        self._leases: dict[str, StockroomWorkspaceLease] = {}
        self._states: dict[str, WorkspaceOwnership] = {}
        self._objects: dict[str, dict[Path, tuple[int, int, int]]] = {}
        self._files: dict[str, dict[str, str]] = {}
        self._spent: set[tuple[str, str]] = set()

    def _check_root(self) -> None:
        if checked_absolute(self.root) != self.root or _identity(self.root) != self._root_identity:
            raise StockroomFailure("ROOT_IDENTITY_CHANGED")
        for child in self.root.iterdir():
            if child.name not in self._runs or _identity(child) != self._runs[child.name]:
                raise StockroomFailure("UNKNOWN_RUN_OBJECT")
            expected = {
                lease.attempt_id
                for lease in self._leases.values()
                if lease.run_id == child.name
                and self._states[lease.lease_id] is not WorkspaceOwnership.CLEANED
            }
            if {p.name for p in child.iterdir()} != expected:
                raise StockroomFailure("UNKNOWN_ATTEMPT_OBJECT")

    def allocate(self, run_id: str, attempt_id: str) -> StockroomWorkspaceLease:
        safe_component(run_id)
        safe_component(attempt_id)
        with self._lock:
            self._check_root()
            key = (run_id.casefold(), attempt_id.casefold())
            if key in self._spent:
                raise StockroomFailure("DESTINATION_ALREADY_USED")
            if any(name.casefold() == run_id.casefold() and name != run_id for name in self._runs):
                raise StockroomFailure("CASE_FOLD_COLLISION")
            run = self.root / run_id
            if run_id not in self._runs:
                run.mkdir(mode=0o700)
                self._runs[run_id] = _identity(run)
            attempt = run / attempt_id
            if any(p.name.casefold() == attempt_id.casefold() for p in run.iterdir()):
                raise StockroomFailure("DESTINATION_EXISTS")
            self._spent.add(key)
            lease = StockroomWorkspaceLease(
                uuid4().hex, run_id, attempt_id, self.root, attempt / "source"
            )
            self._leases[lease.lease_id] = lease
            self._states[lease.lease_id] = WorkspaceOwnership.OWNED
            self._objects[lease.lease_id] = {}
            self._files[lease.lease_id] = {}
            try:
                for path in (attempt, lease.destination):
                    path.mkdir(mode=0o700)
                    self._objects[lease.lease_id][path] = _identity(path)
            except (OSError, StockroomFailure) as exc:
                self._states[lease.lease_id] = WorkspaceOwnership.QUARANTINED
                raise StockroomFailure("ALLOCATION_QUARANTINED") from exc
            return lease

    def _verify(self, lease: StockroomWorkspaceLease) -> None:
        if (
            type(lease) is not StockroomWorkspaceLease
            or self._leases.get(lease.lease_id) is not lease
            or self._states.get(lease.lease_id) is not WorkspaceOwnership.OWNED
            or lease.destination != self.root / lease.run_id / lease.attempt_id / "source"
        ):
            raise StockroomFailure("UNKNOWN_OR_INACTIVE_LEASE")
        self._check_root()
        objects = self._objects[lease.lease_id]
        for path, identity in objects.items():
            if checked_absolute(path) != path or _identity(path) != identity:
                raise StockroomFailure("LEASE_OBJECT_CHANGED")
            if path.is_dir() and set(path.iterdir()) != {p for p in objects if p.parent == path}:
                raise StockroomFailure("UNEXPECTED_RESIDUE")

    def write_file(self, lease: StockroomWorkspaceLease, relative: str, data: bytes) -> None:
        parts = safe_relative(relative)
        if type(data) is not bytes or len(data) > _MAX_FILE_BYTES:
            raise StockroomFailure("FILE_BOUND_EXCEEDED")
        with self._lock:
            self._verify(lease)
            files = self._files[lease.lease_id]
            if len(files) >= _MAX_FILES or relative.casefold() in {p.casefold() for p in files}:
                raise StockroomFailure("FILE_COUNT_OR_COLLISION")
            objects = self._objects[lease.lease_id]
            parent = lease.destination
            for part in parts[:-1]:
                next_path = parent / part
                collisions = [p for p in parent.iterdir() if p.name.casefold() == part.casefold()]
                if collisions and (collisions != [next_path] or next_path not in objects):
                    raise StockroomFailure("CASE_FOLD_COLLISION")
                if not collisions:
                    next_path.mkdir(mode=0o700)
                    objects[next_path] = _identity(next_path)
                checked_absolute(next_path)
                parent = next_path
            target = parent / parts[-1]
            if any(p.name.casefold() == target.name.casefold() for p in parent.iterdir()):
                raise StockroomFailure("DESTINATION_FILE_EXISTS")
            with target.open("xb") as stream:
                objects[target] = _identity(target)
                stream.write(data)
            files[relative] = hashlib.sha256(data).hexdigest()

    def read_files(self, lease: StockroomWorkspaceLease) -> tuple[tuple[str, bytes], ...]:
        with self._lock:
            self._verify(lease)
            result = []
            for relative, expected in sorted(self._files[lease.lease_id].items()):
                path = lease.destination.joinpath(*safe_relative(relative))
                with path.open("rb") as stream:
                    data = stream.read(_MAX_FILE_BYTES + 1)
                if len(data) > _MAX_FILE_BYTES or hashlib.sha256(data).hexdigest() != expected:
                    raise StockroomFailure("DESTINATION_BYTES_CHANGED")
                result.append((relative, data))
            return tuple(result)

    def cleanup(self, lease: StockroomWorkspaceLease) -> WorkspaceCleanupDisposition:
        with self._lock:
            try:
                self._verify(lease)
                objects = self._objects[lease.lease_id]
                # Exact ledger entries only; never rmtree or discover-and-delete.
                for path in sorted(objects, key=lambda p: len(p.parts), reverse=True):
                    checked_absolute(path)
                    if _identity(path) != objects[path]:
                        raise StockroomFailure("CLEANUP_IDENTITY_CHANGED")
                    if path.is_dir():
                        path.rmdir()
                    else:
                        path.unlink()
                self._states[lease.lease_id] = WorkspaceOwnership.CLEANED
                return WorkspaceCleanupDisposition(
                    lease.lease_id,
                    lease.destination,
                    WorkspaceOwnership.CLEANED,
                    "EXACT_OWNED_REMOVED",
                )
            except (OSError, StockroomFailure):
                if self._leases.get(lease.lease_id) is lease:
                    self._states[lease.lease_id] = WorkspaceOwnership.QUARANTINED
                return WorkspaceCleanupDisposition(
                    lease.lease_id,
                    lease.destination,
                    WorkspaceOwnership.QUARANTINED,
                    "OWNERSHIP_OR_DELETE_UNCERTAIN_NO_REUSE",
                )
