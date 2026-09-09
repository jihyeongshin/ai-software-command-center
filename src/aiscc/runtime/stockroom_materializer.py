"""Pinned local-object B1 copying; never executes imported Stockroom code.

Trusted composition registers exact authority objects and supplies live binding.
B2 must supply security-issued refs; B1 does not issue or admit capabilities.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import stat
import subprocess
from collections.abc import Callable
from dataclasses import asdict
from pathlib import Path
from threading import Thread

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.runtime.stockroom_workspace import (
    StockroomWorkspace,
    checked_absolute,
    safe_component,
    safe_relative,
)
from aiscc.scenarios.models import (
    RESOURCE_REF,
    SCENARIO_IDS,
    Resource,
    ResourceFile,
    manifest_sha256,
)
from aiscc.scenarios.runtime_models import (
    MaterializationAuthority,
    MaterializedFile,
    MaterializedStockroom,
    StockroomFailure,
    StockroomRunBinding,
)

_COMMIT = "05185c57a6265a4002050ce25cdfde3dc87e9779"
_TREE = "f3d9203321ae3535abf8e92a7285da1067f6c55e"
_SUBROOT = "examples/synthetic-stockroom/"
_FILE_LIMIT = 64 * 1024
_TOTAL_LIMIT = 512 * 1024
_TREE_LIMIT = 16 * 1024
_TIMEOUT_SECONDS = 10


def _trusted_git_executable(path: Path) -> Path:
    """Validate only the operator-configured, read-only executable endpoint.

    Ancestors retain the workspace helper's strict path checks. A final regular
    Git executable may have multiple hardlinks; mutable objects never use this
    validator. This function neither selects an executable nor searches PATH.
    """
    if not isinstance(path, Path) or not path.is_absolute() or str(path).startswith("\\\\"):
        raise StockroomFailure("TRUSTED_GIT_ABSOLUTE_LOCAL_PATH_REQUIRED")
    if path.name.casefold() not in {"git", "git.exe"}:
        raise StockroomFailure("TRUSTED_GIT_NAME_REQUIRED")
    try:
        parent = checked_absolute(path.parent)
        names = [p.name for p in parent.iterdir() if p.name.casefold() == path.name.casefold()]
        if names != [path.name]:
            raise StockroomFailure("TRUSTED_GIT_MISSING_OR_CASE_AMBIGUOUS")
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise StockroomFailure("TRUSTED_GIT_LINK_OR_REPARSE_DENIED")
        if not stat.S_ISREG(info.st_mode) or info.st_nlink < 1:
            raise StockroomFailure("TRUSTED_GIT_REGULAR_FILE_REQUIRED")
        if str(path.resolve(strict=True)) != str(path):
            raise StockroomFailure("TRUSTED_GIT_RESOLUTION_MISMATCH")
        if not os.access(path, os.X_OK):
            raise StockroomFailure("TRUSTED_GIT_EXECUTABLE_ACCESS_REQUIRED")
        return path
    except OSError as exc:
        raise StockroomFailure("TRUSTED_GIT_PATH_UNAVAILABLE") from exc


def operation_fingerprint(binding: StockroomRunBinding, repository: Path, root: Path) -> str:
    payload = {
        "operation": "stockroom-materialize-v1",
        "binding": asdict(binding),
        "repository": str(repository),
        "runtime_root": str(root),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def _binding_valid(binding: StockroomRunBinding) -> None:
    if type(binding) is not StockroomRunBinding:
        raise StockroomFailure("SERVER_BINDING_REQUIRED")
    if (
        binding.mode is not RuntimeMode.OWNER_SELF_DOGFOOD
        or binding.state is not WorkflowState.RUNNING
        or binding.scenario_id not in SCENARIO_IDS
        or binding.scenario_version != "1.0.0"
        or binding.resource_ref != RESOURCE_REF
        or type(binding.state_version) is not int
        or binding.state_version < 1
        or not re.fullmatch(r"[a-zA-Z0-9_.-]{1,100}", binding.profile_version)
        or not re.fullmatch(r"[0-9a-f]{64}", binding.config_sha256)
    ):
        raise StockroomFailure("INVALID_RUN_BINDING")
    safe_component(binding.run_id)
    safe_component(binding.attempt_id)


class StockroomMaterializer:
    def __init__(
        self,
        *,
        repository_root: Path,
        git_executable: Path,
        workspace: StockroomWorkspace,
        registered_authorities: tuple[MaterializationAuthority, ...],
        current_binding: Callable[[], StockroomRunBinding],
    ) -> None:
        self._repository = repository_root
        self._git = git_executable
        self._workspace = workspace
        # No issuer is provided. Only the server composition constructor can register refs.
        self._authorities = tuple(registered_authorities)
        self._current_binding = current_binding

    def _authorize(self, binding: StockroomRunBinding, authority: MaterializationAuthority) -> None:
        _binding_valid(binding)
        if (
            type(authority) is not MaterializationAuthority
            or not any(authority is registered for registered in self._authorities)
            or authority.binding != binding
            or self._current_binding() != binding
            or authority.repository_root != self._repository
            or authority.runtime_root != self._workspace.root
            or authority.operation_fingerprint
            != operation_fingerprint(binding, self._repository, self._workspace.root)
        ):
            raise StockroomFailure("AUTHORITY_OR_CURRENT_BINDING_MISMATCH")
        for ref in (
            authority.principal_ref,
            authority.security_admission_ref,
            authority.repository_grant_ref,
            authority.filesystem_grant_ref,
        ):
            if type(ref) is not str or not re.fullmatch(r"[A-Za-z0-9:_.-]{1,200}", ref):
                raise StockroomFailure("EXACT_AUTHORITY_REFS_REQUIRED")

    def _configuration(self) -> None:
        repository = checked_absolute(self._repository)
        git = _trusted_git_executable(self._git)
        git_dir = checked_absolute(repository / ".git")
        if (
            not repository.is_dir()
            or not git.is_file()
            or git.name.casefold() not in {"git", "git.exe"}
            or not os.access(git, os.X_OK)
            or not git_dir.is_dir()
            or repository != self._workspace.repository_root
            or git_dir != self._workspace.source_object_root
            or git.is_relative_to(repository)
            or git.is_relative_to(self._workspace.root)
        ):
            raise StockroomFailure("UNTRUSTED_LOCAL_GIT_CONFIGURATION")
        # Deliberately fail closed for linked worktrees, alternate object stores,
        # shallow histories, and partial clones instead of expanding B1 scope.
        for relative in ("objects/info/alternates", "objects/info/http-alternates", "shallow"):
            if (git_dir / relative).exists():
                raise StockroomFailure("UNSUPPORTED_OBJECT_STORE")
        objects = checked_absolute(git_dir / "objects")
        pack = checked_absolute(objects / "pack")
        for ordinal, path in enumerate(pack.iterdir()):
            if ordinal >= 256:
                raise StockroomFailure("PACK_INVENTORY_BOUND")
            checked_absolute(path)
            if path.suffix == ".promisor":
                raise StockroomFailure("PARTIAL_CLONE_DENIED")

    def _read_git(self, args: tuple[str, ...], limit: int) -> bytes:
        for argument in args:
            oid = argument.split(":", 1)[0]
            if re.fullmatch(r"[0-9a-f]{40}", oid):
                loose = self._repository / ".git/objects" / oid[:2] / oid[2:]
                if loose.exists() or loose.is_symlink():
                    checked_absolute(loose)
        env = {
            key: value
            for key, value in os.environ.items()
            if key.upper() in {"SYSTEMROOT", "WINDIR"}
        }
        env.update(
            {
                "PATH": str(self._git.parent),
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_NO_REPLACE_OBJECTS": "1",
                "GIT_NO_LAZY_FETCH": "1",
                "GIT_TERMINAL_PROMPT": "0",
                "GIT_OPTIONAL_LOCKS": "0",
                "GIT_ALLOW_PROTOCOL": "",
                "GIT_CONFIG_SYSTEM": os.devnull,
            }
        )
        argv = [
            str(self._git),
            "--no-replace-objects",
            "--git-dir",
            str(self._repository / ".git"),
            "-c",
            "protocol.allow=never",
            "-c",
            "core.useReplaceRefs=false",
            *args,
        ]
        output: list[bytes] = []
        errors: list[Exception] = []
        try:
            with subprocess.Popen(
                argv,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                env=env,
                shell=False,
            ) as process:
                assert process.stdout is not None
                stream = process.stdout

                def read_bounded() -> None:
                    try:
                        data = stream.read(limit + 1)
                        output.append(data)
                        if len(data) > limit:
                            process.kill()
                    except OSError as exc:
                        errors.append(exc)

                reader = Thread(target=read_bounded, daemon=True)
                reader.start()
                try:
                    code = process.wait(timeout=_TIMEOUT_SECONDS)
                except subprocess.TimeoutExpired as exc:
                    process.kill()
                    process.wait(timeout=_TIMEOUT_SECONDS)
                    reader.join(timeout=_TIMEOUT_SECONDS)
                    raise StockroomFailure("GIT_TIMEOUT") from exc
                reader.join(timeout=_TIMEOUT_SECONDS)
                if reader.is_alive() or errors or len(output) != 1 or len(output[0]) > limit:
                    raise StockroomFailure("GIT_AMBIGUOUS_OR_OVERSIZED_READ")
                if code != 0:
                    raise StockroomFailure("GIT_NONZERO")
                return output[0]
        except OSError as exc:
            raise StockroomFailure("GIT_UNAVAILABLE") from exc

    def _resource(self) -> Resource:
        path = checked_absolute(self._repository / "config/scenarios/stockroom/v1/resource.json")
        try:
            with path.open("rb") as stream:
                data = stream.read(_TREE_LIMIT + 1)
            if len(data) > _TREE_LIMIT:
                raise StockroomFailure("MANIFEST_SIZE_BOUND")
            resource = Resource.model_validate_json(data)
            for item in resource.files:
                safe_relative(item.path)
            folded = tuple(item.path.casefold() for item in resource.files)
            if len(set(folded)) != 14 or any(item.bytes > _FILE_LIMIT for item in resource.files):
                raise StockroomFailure("MANIFEST_BOUNDS_OR_COLLISION")
            if sum(item.bytes for item in resource.files) > _TOTAL_LIMIT:
                raise StockroomFailure("MANIFEST_TOTAL_BOUND")
            return resource
        except ValueError as exc:
            raise StockroomFailure("RESOURCE_MANIFEST_INVALID") from exc

    def _source_bytes(self, resource: Resource) -> tuple[tuple[ResourceFile, bytes], ...]:
        if self._read_git(("cat-file", "-t", _COMMIT), 16) != b"commit\n":
            raise StockroomFailure("WRONG_COMMIT_TYPE")
        if (
            self._read_git(("rev-parse", f"{_COMMIT}:{_SUBROOT.rstrip('/')}"), 64)
            != (_TREE + "\n").encode()
        ):
            raise StockroomFailure("WRONG_SUBTREE")
        if self._read_git(("cat-file", "-t", _TREE), 16) != b"tree\n":
            raise StockroomFailure("WRONG_TREE_TYPE")
        listing = self._read_git(("ls-tree", "-z", "-r", _TREE), _TREE_LIMIT)
        if not listing.endswith(b"\0"):
            raise StockroomFailure("AMBIGUOUS_TREE_LISTING")
        rows = listing[:-1].split(b"\0")
        if len(rows) != 14:
            raise StockroomFailure("TREE_FILE_COUNT")
        inventory: dict[str, str] = {}
        folded: set[str] = set()
        for row in rows:
            match = re.fullmatch(rb"100644 blob ([0-9a-f]{40})\t([^\x00]+)", row)
            if match is None:
                raise StockroomFailure("UNSAFE_OBJECT_MODE_OR_TYPE")
            try:
                path = match[2].decode("ascii")
                safe_relative(path)
            except (ValueError, UnicodeError) as exc:
                raise StockroomFailure("UNSAFE_OBJECT_PATH") from exc
            if path.casefold() in folded:
                raise StockroomFailure("DUPLICATE_OBJECT_PATH")
            folded.add(path.casefold())
            inventory[path] = match[1].decode("ascii")
        if tuple(sorted(inventory)) != tuple(item.path for item in resource.files):
            raise StockroomFailure("MANIFEST_PATH_SET_MISMATCH")
        verified = []
        for item in resource.files:
            data = self._read_git(("cat-file", "blob", inventory[item.path]), item.bytes)
            if len(data) != item.bytes or hashlib.sha256(data).hexdigest() != item.sha256:
                raise StockroomFailure("SOURCE_BYTE_IDENTITY_MISMATCH")
            verified.append((item, data))
        return tuple(verified)

    def materialize(
        self, binding: StockroomRunBinding, authority: MaterializationAuthority
    ) -> MaterializedStockroom:
        self._authorize(binding, authority)
        self._configuration()
        resource = self._resource()
        verified = self._source_bytes(resource)
        self._authorize(binding, authority)
        lease = self._workspace.allocate(binding.run_id, binding.attempt_id)
        try:
            for item, data in verified:
                self._authorize(binding, authority)
                self._workspace.write_file(lease, item.path, data)
            actual = self._workspace.read_files(lease)
            files = tuple(
                ResourceFile(
                    path=path,
                    mode="100644",
                    bytes=len(data),
                    sha256=hashlib.sha256(data).hexdigest(),
                )
                for path, data in actual
            )
            if files != resource.files or manifest_sha256(files) != resource.aggregate_sha256:
                raise StockroomFailure("DESTINATION_MANIFEST_MISMATCH")
            self._authorize(binding, authority)
            return MaterializedStockroom(
                resource.resource_ref,
                resource.source_commit,
                resource.subroot,
                resource.git_subtree,
                tuple(
                    MaterializedFile(item.path, item.mode, item.bytes, item.sha256)
                    for item in files
                ),
                resource.aggregate_sha256,
                lease,
                binding.run_id,
                binding.attempt_id,
                lease.destination,
            )
        except (OSError, ValueError, StockroomFailure) as exc:
            disposition = self._workspace.cleanup(lease)
            reason = (
                exc.reason
                if isinstance(exc, StockroomFailure)
                else "DESTINATION_WRITE_OR_VERIFY_FAILED"
            )
            raise StockroomFailure(reason, disposition) from exc
