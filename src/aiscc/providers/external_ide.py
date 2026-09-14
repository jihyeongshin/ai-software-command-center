"""Local control-plane completion ingress; never an execution or Git write service."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
import stat
import subprocess
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from uuid import uuid4
from weakref import WeakValueDictionary

from sqlalchemy import select

from aiscc.contracts.canonical_json import canonical_json_bytes, verify_canonical_json_bytes
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.persistence.models import (
    ExternalIdeExecutionLeaseRow,
    ExternalIdeExecutionSubmissionRow,
)
from aiscc.persistence.repository import (
    acquire_work_run_transaction_lock,
    verify_historical_transition_provenance,
)
from aiscc.providers.models import ExecutionStatus, ExecutionSubmissionRef
from aiscc.task_authority.contracts import TaskContractBodyV1, plain

PRODUCER = "LOCAL_IDE_SELF_DOGFOOD_V1"
ISSUER = "AISCC_P1_5_LOCAL_IDE_SELF_DOGFOOD_V1"
VERSION = "v1"
PREFIX = "external-ide-submission:"
_VERIFIED = object()
_RECEIPTS = WeakValueDictionary()
_HEX = re.compile(r"[0-9a-f]{64}\Z")


class ExternalIdeAuthorityError(ValueError):
    """Sanitized fail-closed producer authority error."""


def _deny(message):
    raise ExternalIdeAuthorityError(message)


def _hash(data):
    return hashlib.sha256(data).hexdigest()


def _freeze(value):
    if isinstance(value, dict):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(v) for v in value)
    return value


def _path(value, *, scope=False):
    if not isinstance(value, str) or not value or "\\" in value or ":" in value:
        _deny("non-canonical governed path")
    p = PurePosixPath(value)
    if p.is_absolute() or p.as_posix() != value or any(x in (".", "..") for x in p.parts):
        _deny("path traversal or normalization")
    base = value[:-3] if scope and value.endswith("/**") else value
    if not base or any(c in base for c in "*?[]"):
        _deny("unbounded path")
    if any(x.rstrip(". ") != x or x.casefold() == ".git" for x in p.parts):
        _deny("unsafe governed path")
    if any(ord(c) < 32 for c in value):
        _deny("path control character")
    return value


def _paths(values, *, scope=False):
    if not isinstance(values, (list, tuple)):
        _deny("path array required")
    for value in values:
        _path(value, scope=scope)
    if list(values) != sorted(set(values)) or len({x.casefold() for x in values}) != len(values):
        _deny("paths must be sorted and unique")


def _matches(path, scopes):
    return any(path == x or (x.endswith("/**") and path.startswith(x[:-2])) for x in scopes)


def _timestamp(value):
    if not isinstance(value, str):
        _deny("UTC timestamp required")
    try:
        result = datetime.fromisoformat(value)
    except ValueError:
        _deny("invalid timestamp")
    if result.tzinfo is None or result.utcoffset() != timedelta(0) or result.isoformat() != value:
        _deny("canonical UTC timestamp required")
    return result


def _now(clock):
    value = clock()
    if not isinstance(value, datetime) or value.tzinfo is None:
        _deny("trusted clock unavailable")
    return value.astimezone(UTC)


@dataclass(frozen=True, init=False)
class ExternalIdeExecutionLeaseV1:
    canonical_body: bytes

    def __init__(self, value):
        fields = set(
            [
                "schema",
                "producer",
                "project_id",
                "lease_id",
                "work_run_id",
                "state",
                "state_version",
                "task_id",
                "contract_id",
                "contract_version",
                "body_ref",
                "body_sha256",
                "repository_id",
                "repository_root",
                "base_commit",
                "inner_task_sha256",
                "allowed_paths",
                "forbidden_paths",
                "scope_fingerprint",
                "issued_at",
                "expires_at",
                "capability_hash",
                "start_transition_id",
                "expected_hashes",
            ]
        )
        if not isinstance(value, dict) or set(value) != fields:
            _deny("closed lease fields differ")
        data = canonical_json_bytes(value)
        if value["schema"] != "AISCC-EXTERNAL-IDE-LEASE-V1" or value["producer"] != PRODUCER:
            _deny("unsupported external producer/schema")
        if value["state"] != "RUNNING" or type(value["state_version"]) is not int:
            _deny("RUNNING state/version required")
        if value["state_version"] < 2 or type(value["contract_version"]) is not int:
            _deny("invalid state/contract version")
        if value["contract_version"] < 1:
            _deny("invalid contract version")
        for key in (
            "project_id",
            "lease_id",
            "work_run_id",
            "task_id",
            "contract_id",
            "repository_id",
            "start_transition_id",
        ):
            if (
                not isinstance(value[key], str)
                or re.fullmatch(r"[A-Za-z0-9_.:-]{1,160}", value[key]) is None
            ):
                _deny("invalid lease identity")
        for key in ("body_sha256", "inner_task_sha256", "scope_fingerprint", "capability_hash"):
            if not isinstance(value[key], str) or not _HEX.fullmatch(value[key]):
                _deny("invalid lease hash")
        if not re.fullmatch(r"task-contract-body:v1:sha256:[0-9a-f]{64}", value["body_ref"]):
            _deny("body ref/hash differs")
        if not re.fullmatch(r"[0-9a-f]{40}", value["base_commit"]):
            _deny("invalid base commit")
        if not Path(value["repository_root"]).is_absolute():
            _deny("absolute repository binding required")
        for key in ("allowed_paths", "forbidden_paths"):
            _paths(value[key], scope=True)
        if not value["allowed_paths"]:
            _deny("bounded allowed scope required")
        for a in value["allowed_paths"]:
            for f in value["forbidden_paths"]:
                if _matches(a.removesuffix("/**"), [f]) or _matches(f.removesuffix("/**"), [a]):
                    _deny("scope overlap")
        scope = {k: value[k] for k in ("allowed_paths", "forbidden_paths")}
        if _hash(canonical_json_bytes(scope)) != value["scope_fingerprint"]:
            _deny("scope fingerprint mismatch")
        if not isinstance(value["expected_hashes"], dict):
            _deny("expected hashes required")
        _paths(list(value["expected_hashes"]))
        for p, h in value["expected_hashes"].items():
            if (
                not _matches(p, value["allowed_paths"])
                or not isinstance(h, str)
                or not _HEX.fullmatch(h)
            ):
                _deny("invalid required output hash")
        issued, expiry = (_timestamp(value[k]) for k in ("issued_at", "expires_at"))
        if not timedelta(0) < expiry - issued <= timedelta(hours=1):
            _deny("lease duration outside bounded window")
        object.__setattr__(self, "canonical_body", data)

    @property
    def value(self):
        return _freeze(json.loads(self.canonical_body))

    @property
    def fingerprint(self):
        return _hash(self.canonical_body)


@dataclass(frozen=True, init=False)
class ExternalIdeRepositoryObservationV1:
    canonical_body: bytes

    def __init__(self, value):
        if set(value) != set(
            [
                "schema",
                "head",
                "index",
                "entries",
                "files",
                "diff_check",
                "unauthorized",
                "observed_at",
            ]
        ):
            _deny("closed observation fields differ")
        data = canonical_json_bytes(value)
        if value["schema"] != "AISCC-EXTERNAL-IDE-OBSERVATION-V1":
            _deny("observation schema")
        if not re.fullmatch(r"[0-9a-f]{40}", value["head"]):
            _deny("observation HEAD")
        _timestamp(value["observed_at"])
        _paths(value["unauthorized"])
        if not isinstance(value["entries"], (list, tuple)):
            _deny("observation entries required")
        observed_paths = set()
        entry_paths = []
        index_entries = []
        for entry in value["entries"]:
            if set(entry) != {"status", "path", "original"}:
                _deny("closed observation entry differs")
            _path(entry["path"])
            if not isinstance(entry["status"], str) or len(entry["status"]) != 2:
                _deny("invalid Git status")
            if any(c not in " MADRCU?!T" for c in entry["status"]):
                _deny("unknown Git status")
            observed_paths.add(entry["path"])
            entry_paths.append(entry["path"])
            if entry["original"] is not None:
                _path(entry["original"])
                if not any(c in entry["status"] for c in "RC"):
                    _deny("rename status differs")
                observed_paths.add(entry["original"])
            if entry["status"][0] not in (" ", "?"):
                index_entries.append(entry)
        _paths(entry_paths)
        expected_index = canonical_json_bytes(index_entries).decode() if index_entries else ""
        if value["index"] != expected_index or observed_paths != set(value["files"]):
            _deny("observation path/index mismatch")
        _paths(list(value["files"]))
        for h in value["files"].values():
            if h is not None and (not isinstance(h, str) or not _HEX.fullmatch(h)):
                _deny("observation file hash")
        if type(value["diff_check"]) is not bool or not isinstance(value["index"], str):
            _deny("observation flags")
        object.__setattr__(self, "canonical_body", data)

    @property
    def value(self):
        return _freeze(json.loads(self.canonical_body))

    @property
    def root(self):
        return _hash(
            canonical_json_bytes({k: v for k, v in self.value.items() if k != "observed_at"})
        )


@dataclass(frozen=True)
class ExternalIdeExecutionSubmissionV1:
    lease: ExternalIdeExecutionLeaseV1
    observation: ExternalIdeRepositoryObservationV1
    submission_id: str
    completed_at: str

    def __post_init__(self):
        if self.submission_id != PREFIX + self.lease.value["lease_id"]:
            _deny("submission identity differs")
        when = _timestamp(self.completed_at)
        if (
            not _timestamp(self.lease.value["issued_at"])
            <= when
            < _timestamp(self.lease.value["expires_at"])
        ):
            _deny("submission time outside lease")
        _require_observation(self.lease, self.observation)

    @property
    def canonical_body(self):
        return canonical_json_bytes(
            dict(
                schema="AISCC-EXTERNAL-IDE-SUBMISSION-V1",
                producer=PRODUCER,
                lease_fingerprint=self.lease.fingerprint,
                observation=self.observation.value,
                observation_root=self.observation.root,
                submission_id=self.submission_id,
                completed_at=self.completed_at,
            )
        )

    @property
    def common_ref(self):
        v = self.lease.value
        return ExecutionSubmissionRef(
            self.submission_id,
            v["lease_id"],
            v["work_run_id"],
            v["contract_id"],
            "v" + str(v["contract_version"]),
            WorkflowState.RUNNING,
            v["state_version"],
            ExecutionStatus.EXECUTOR_COMPLETED,
            _hash(self.canonical_body),
            ISSUER,
        )


@dataclass(frozen=True)
class VerifiedExternalIdeExecutionSubmissionV1:
    submission: ExternalIdeExecutionSubmissionV1
    _owner_token: object

    @property
    def common_ref(self):
        if self._owner_token is not _VERIFIED or _RECEIPTS.get(id(self)) is not self:
            _deny("unverified external submission")
        return self.submission.common_ref


def _require_observation(lease, observation):
    v, o = lease.value, observation.value
    if o["head"] != v["base_commit"] or o["index"] or not o["diff_check"] or o["unauthorized"]:
        _deny("repository base/index/diff/scope denied")
    for p in o["files"]:
        if not _matches(p, v["allowed_paths"]) or _matches(p, v["forbidden_paths"]):
            _deny("scope violation")
    for p, h in v["expected_hashes"].items():
        if o["files"].get(p) != h:
            _deny("required output hash mismatch")


class LocalGitObserver:
    """Only fixed local read commands. Composition, not the completion caller, selects Git."""

    def __init__(self, git_executable, *, clock=lambda: datetime.now(UTC)):
        self._git = str(Path(git_executable))
        if not Path(self._git).is_absolute() or not Path(self._git).is_file():
            _deny("fixed Git executable missing")
        self._clock = clock

    def _read(self, root, args, *, check=True):
        env = {k: v for k, v in os.environ.items() if not k.upper().startswith("GIT_")}
        env.update(GIT_OPTIONAL_LOCKS="0", GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull)
        result = subprocess.run(
            [
                self._git,
                "-c",
                "core.fsmonitor=false",
                "-c",
                "core.untrackedCache=false",
                "--no-optional-locks",
                "-C",
                str(root),
                *args,
            ],
            env=env,
            capture_output=True,
            timeout=20,
            check=False,
        )
        if len(result.stdout) + len(result.stderr) > 4 * 1024 * 1024:
            _deny("Git observation size limit")
        if check and result.returncode:
            _deny("Git observation failed")
        return result

    @staticmethod
    def _safe(root, relative):
        p = root
        for part in PurePosixPath(relative).parts:
            p = p / part
            if p.exists() or p.is_symlink():
                st = p.lstat()
                if stat.S_ISLNK(st.st_mode) or getattr(st, "st_file_attributes", 0) & 0x400:
                    _deny("symlink/reparse path denied")
        return p

    def observe(self, lease):
        v = lease.value
        root = Path(v["repository_root"])
        if not root.is_dir() or str(root.resolve()) != str(root):
            _deny("repository root identity differs")
        self._safe(root.parent, root.name)
        self._safe(root, ".git")
        # Git's read commands may invoke configured clean filters. Reject executable or
        # indirectly included local configuration before any worktree observation.
        configuration = self._read(root, ["config", "--local", "--null", "--list"]).stdout
        for entry in configuration.decode("utf-8").split("\0"):
            key = entry.split("\n", 1)[0].casefold()
            if (
                key.startswith(("filter.", "include.", "includeif."))
                or key == "extensions.worktreeconfig"
            ):
                _deny("repository executable/indirect Git configuration denied")
        top = self._read(root, ["rev-parse", "--show-toplevel"]).stdout.decode().strip()
        if Path(top).resolve() != root:
            _deny("Git root differs")
        head = self._read(root, ["rev-parse", "--verify", "HEAD"]).stdout.decode().strip()
        raw = self._read(root, ["status", "--porcelain=v1", "-z", "--untracked-files=all"]).stdout
        entries, paths, index = [], set(), []
        parts = raw.decode("utf-8").split("\0")
        i = 0
        while i < len(parts) and parts[i]:
            entry = parts[i]
            i += 1
            status, path = entry[:2], entry[3:]
            _path(path)
            item = dict(status=status, path=path, original=None)
            paths.add(path)
            if "R" in status or "C" in status:
                if i >= len(parts):
                    _deny("malformed rename observation")
                original = parts[i]
                i += 1
                _path(original)
                item["original"] = original
                paths.add(original)
            entries.append(item)
            if status[0] not in (" ", "?"):
                index.append(item)
        files = {}
        for path in sorted(paths):
            p = self._safe(root, path)
            if not p.exists():
                files[path] = None
            else:
                before = p.stat()
                if not p.is_file() or before.st_size > 16 * 1024 * 1024:
                    _deny("observed file type/size denied")
                data = p.read_bytes()
                after = p.stat()
                if (before.st_ino, before.st_size, before.st_mtime_ns) != (
                    after.st_ino,
                    after.st_size,
                    after.st_mtime_ns,
                ):
                    _deny("concurrent source mutation")
                files[path] = _hash(data)
        diff = self._read(
            root, ["diff", "--no-ext-diff", "--no-textconv", "--check", "HEAD", "--"], check=False
        )
        unauthorized = sorted(
            p
            for p in paths
            if not _matches(p, v["allowed_paths"]) or _matches(p, v["forbidden_paths"])
        )
        if (
            raw
            != self._read(root, ["status", "--porcelain=v1", "-z", "--untracked-files=all"]).stdout
        ):
            _deny("concurrent repository status mutation")
        if head != self._read(root, ["rev-parse", "--verify", "HEAD"]).stdout.decode().strip():
            _deny("concurrent HEAD mutation")
        return ExternalIdeRepositoryObservationV1(
            dict(
                schema="AISCC-EXTERNAL-IDE-OBSERVATION-V1",
                head=head,
                index=canonical_json_bytes(index).decode() if index else "",
                entries=sorted(entries, key=lambda x: x["path"]),
                files=files,
                diff_check=diff.returncode == 0,
                unauthorized=unauthorized,
                observed_at=_now(self._clock).isoformat(),
            )
        )


async def verify_external_submission_in_session(session, submission_id):
    """Read-only durable P1-5 verifier shared by live/restart/historical consumers."""
    row = await session.get(ExternalIdeExecutionSubmissionRow, submission_id)
    if row is None:
        _deny("external submission missing")
    lease_row = await session.get(ExternalIdeExecutionLeaseRow, row.lease_id)
    if lease_row is None:
        _deny("AUTHORITY_CORRUPTION: lease missing")
    lease = ExternalIdeExecutionLeaseV1(
        verify_canonical_json_bytes(bytes(lease_row.canonical_body))
    )
    if lease.fingerprint != lease_row.body_sha256 or lease.value["lease_id"] != lease_row.lease_id:
        _deny("AUTHORITY_CORRUPTION: lease binding")
    from aiscc.persistence.models import TaskContractBodyRow

    body_row = await session.get(TaskContractBodyRow, lease.value["body_ref"])
    if body_row is None:
        _deny("AUTHORITY_CORRUPTION: TaskContract body missing")
    body = TaskContractBodyV1.from_bytes(bytes(body_row.canonical_body))
    if body_row.body_sha256 != body.body_sha256 or body_row.body_ref != body.body_ref:
        _deny("AUTHORITY_CORRUPTION: TaskContract body hash/ref")
    _bind_body(lease, body)
    source = await verify_historical_transition_provenance(
        session, lease.value["start_transition_id"]
    )
    _bind_run(
        lease,
        source.request,
        source.decision.resulting_state,
        source.decision.resulting_state_version,
    )
    raw = verify_canonical_json_bytes(bytes(row.canonical_body))
    submission = ExternalIdeExecutionSubmissionV1(
        lease,
        ExternalIdeRepositoryObservationV1(raw["observation"]),
        row.submission_id,
        raw["completed_at"],
    )
    if (
        submission.canonical_body != bytes(row.canonical_body)
        or _hash(submission.canonical_body) != row.body_sha256
        or row.lease_id != lease.value["lease_id"]
        or row.producer_kind != PRODUCER
        or lease_row.producer_kind != PRODUCER
        or row.work_run_id != lease.value["work_run_id"]
        or lease_row.work_run_id != row.work_run_id
    ):
        _deny("AUTHORITY_CORRUPTION: external submission binding")
    verified = VerifiedExternalIdeExecutionSubmissionV1(submission, _VERIFIED)
    _RECEIPTS[id(verified)] = verified
    return verified


def _bind_body(lease, body):
    v, t = lease.value, body.value
    expected = dict(
        project_id=t["project_id"],
        task_id=t["task_id"],
        contract_id=t["contract_id"],
        contract_version=t["contract_version"],
        body_ref=body.body_ref,
        body_sha256=body.body_sha256,
        **plain(t["repository_binding"]),
        allowed_paths=t["allowed_paths"],
        forbidden_paths=t["forbidden_paths"],
    )
    if any(v[k] != value for k, value in expected.items()):
        _deny("TaskContract lease binding differs")
    if t["execution_provenance"]["runtime_mode"] != "OWNER_SELF_DOGFOOD":
        _deny("local self-dogfood only")


def _bind_run(lease, run, state, version):
    v = lease.value
    if (
        run.work_run_id != v["work_run_id"]
        or run.project_id != v["project_id"]
        or run.task_contract_id != v["contract_id"]
        or run.task_contract_version != "v" + str(v["contract_version"])
        or run.runtime_mode is not RuntimeMode.OWNER_SELF_DOGFOOD
        or state is not WorkflowState.RUNNING
        or version != v["state_version"]
    ):
        _deny("exact RUNNING WorkRun binding denied")


class ExternalIdeExecutionRepository:
    """Completion clients hold this reader/completer, never the private lease writer."""

    def __init__(self, sessions, task_authority, observer, *, clock=lambda: datetime.now(UTC)):
        self._sessions = sessions
        self._tasks = task_authority
        self._observer = observer
        self._clock = clock
        self.__writer = None

    async def _current(self, session, lease):
        v = lease.value
        await acquire_work_run_transaction_lock(session, v["work_run_id"])
        source = await verify_historical_transition_provenance(session, v["start_transition_id"])
        _bind_run(lease, source.work_run, source.work_run.state, source.work_run.state_version)
        receipt = await self._tasks.get_task_contract(
            v["project_id"], v["contract_id"], v["contract_version"], session=session
        )
        if receipt is None:
            _deny("TaskContract missing")
        _bind_body(lease, receipt.body)
        await self._tasks.verify_task_contract(
            receipt,
            require_current=True,
            expected_repository_binding={
                k: v[k] for k in ("repository_id", "repository_root", "base_commit")
            },
            expected_next_action_ref=receipt.body.value["source_next_action"]["action_ref"],
            session=session,
        )

    async def complete(self, session, *, lease_id, capability):
        if not session.in_transaction():
            _deny("caller transaction required")
        row = await session.get(ExternalIdeExecutionLeaseRow, lease_id)
        if row is None:
            _deny("lease missing")
        lease = ExternalIdeExecutionLeaseV1(verify_canonical_json_bytes(bytes(row.canonical_body)))
        if lease.fingerprint != row.body_sha256 or row.lease_id != lease.value["lease_id"]:
            _deny("AUTHORITY_CORRUPTION: lease")
        if not isinstance(capability, str) or not hmac.compare_digest(
            _hash(capability.encode()), lease.value["capability_hash"]
        ):
            _deny("capability denied")
        await self._current(session, lease)
        now = _now(self._clock)
        if not _timestamp(lease.value["issued_at"]) <= now < _timestamp(lease.value["expires_at"]):
            _deny("lease expired/stale")
        first = self._observer.observe(lease)
        _require_observation(lease, first)
        second = self._observer.observe(lease)
        if first.root != second.root:
            _deny("concurrent source mutation")
        now = _now(self._clock)
        if not _timestamp(lease.value["issued_at"]) <= now < _timestamp(lease.value["expires_at"]):
            _deny("lease expired during observation")
        old = await session.scalar(
            select(ExternalIdeExecutionSubmissionRow).where(
                ExternalIdeExecutionSubmissionRow.lease_id == lease_id
            )
        )
        if old is not None:
            verified = await verify_external_submission_in_session(session, old.submission_id)
            if verified.submission.observation.root != first.root:
                _deny("changed completed retry")
            return verified.submission
        result = ExternalIdeExecutionSubmissionV1(lease, second, PREFIX + lease_id, now.isoformat())
        session.add(
            ExternalIdeExecutionSubmissionRow(
                submission_id=result.submission_id,
                lease_id=lease_id,
                work_run_id=lease.value["work_run_id"],
                producer_kind=PRODUCER,
                canonical_body=result.canonical_body,
                body_sha256=_hash(result.canonical_body),
            )
        )
        await session.flush()
        return result

    async def resolve(self, submission_id):
        # A separate read observes only committed authority; rollback cannot leak a trusted ref.
        async with self._sessions() as session, session.begin():
            return await verify_external_submission_in_session(session, submission_id)

    def _bind_writer(self):
        if self.__writer is not None:
            _deny("writer already bound")
        self.__writer = object()
        return _ExternalIdeLeaseWriter(self, self.__writer)

    async def _issue(
        self,
        capability,
        session,
        *,
        receipt,
        work_run_id,
        state_version,
        start_transition_id,
        inner_task_bytes,
        expected_hashes,
        ttl,
    ):
        if capability is not self.__writer or capability is None or not session.in_transaction():
            _deny("trusted writer/caller transaction required")
        t = receipt.body.value
        token = secrets.token_urlsafe(32)
        now = _now(self._clock)
        scope = {k: t[k] for k in ("allowed_paths", "forbidden_paths")}
        lease = ExternalIdeExecutionLeaseV1(
            dict(
                schema="AISCC-EXTERNAL-IDE-LEASE-V1",
                producer=PRODUCER,
                project_id=t["project_id"],
                lease_id="local-ide-" + uuid4().hex,
                work_run_id=work_run_id,
                state="RUNNING",
                state_version=state_version,
                task_id=t["task_id"],
                contract_id=t["contract_id"],
                contract_version=t["contract_version"],
                body_ref=receipt.body.body_ref,
                body_sha256=receipt.body.body_sha256,
                **plain(t["repository_binding"]),
                inner_task_sha256=_hash(inner_task_bytes),
                **scope,
                scope_fingerprint=_hash(canonical_json_bytes(scope)),
                issued_at=now.isoformat(),
                expires_at=(now + ttl).isoformat(),
                capability_hash=_hash(token.encode()),
                start_transition_id=start_transition_id,
                expected_hashes=dict(sorted(expected_hashes.items())),
            )
        )
        await self._current(session, lease)
        before = self._observer.observe(lease)
        if (
            before.value["head"] != lease.value["base_commit"]
            or before.value["entries"]
            or before.value["index"]
        ):
            _deny("lease requires clean exact base")
        session.add(
            ExternalIdeExecutionLeaseRow(
                lease_id=lease.value["lease_id"],
                work_run_id=work_run_id,
                producer_kind=PRODUCER,
                canonical_body=lease.canonical_body,
                body_sha256=lease.fingerprint,
            )
        )
        await session.flush()
        return lease, token


class _ExternalIdeLeaseWriter:
    def __init__(self, repository, capability):
        self._repository, self._capability = repository, capability

    async def issue(self, session, **kwargs):
        return await self._repository._issue(self._capability, session, **kwargs)


def _bind_external_ide_writer(repository):
    """Trusted local composition only; never expose to the IDE completion client."""
    return repository._bind_writer()


# Start authority is deliberately separate from the accepted completion domain above.
_START_OWNER = object()
_START_REFS = WeakValueDictionary()
START_PREFIX = "external-ide-start:"


@dataclass(frozen=True, init=False)
class ExternalIdeExecutionStartPermitV1:
    canonical_body: bytes

    def __init__(self, value):
        fields = set(
            [
                "schema",
                "producer",
                "project_id",
                "permit_id",
                "work_run_id",
                "state",
                "state_version",
                "task_id",
                "contract_id",
                "contract_version",
                "body_ref",
                "body_sha256",
                "repository_id",
                "repository_root",
                "base_commit",
                "inner_task_sha256",
                "allowed_paths",
                "forbidden_paths",
                "scope_fingerprint",
                "issued_at",
                "expires_at",
                "capability_hash",
                "ready_transition_id",
            ]
        )
        if type(value) is not dict or set(value) != fields:
            _deny("closed start permit fields differ")
        data = canonical_json_bytes(value)  # NFC, safe integers, no float/unknown JSON types.
        if value["schema"] != "AISCC-EXTERNAL-IDE-START-PERMIT-V1" or value["producer"] != PRODUCER:
            _deny("start producer/schema denied")
        if value["state"] != "READY":
            _deny("READY start permit required")
        for key in ("state_version", "contract_version"):
            if type(value[key]) is not int or value[key] < 1:
                _deny("positive exact start version required")
        for key in (
            "project_id",
            "permit_id",
            "work_run_id",
            "task_id",
            "contract_id",
            "repository_id",
            "ready_transition_id",
        ):
            if (
                not isinstance(value[key], str)
                or re.fullmatch(r"[A-Za-z0-9_.:-]{1,128}", value[key]) is None
            ):
                _deny("invalid start identity")
        for key in ("body_sha256", "inner_task_sha256", "scope_fingerprint", "capability_hash"):
            if not isinstance(value[key], str) or not _HEX.fullmatch(value[key]):
                _deny("invalid start fingerprint")
        if not isinstance(value["body_ref"], str) or not re.fullmatch(
            r"task-contract-body:v1:sha256:[0-9a-f]{64}", value["body_ref"]
        ):
            _deny("invalid start body ref")
        if not isinstance(value["base_commit"], str) or not re.fullmatch(
            r"[0-9a-f]{40}", value["base_commit"]
        ):
            _deny("invalid start base")
        root = value["repository_root"]
        if (
            not isinstance(root, str)
            or not Path(root).is_absolute()
            or str(Path(root)) != root
            or any(ord(c) < 32 for c in root)
        ):
            _deny("canonical absolute start root required")
        for key in ("allowed_paths", "forbidden_paths"):
            _paths(value[key], scope=True)
        if not value["allowed_paths"]:
            _deny("bounded start scope required")
        for a in value["allowed_paths"]:
            for b in value["forbidden_paths"]:
                if _matches(a.removesuffix("/**"), [b]) or _matches(b.removesuffix("/**"), [a]):
                    _deny("start scope overlap")
        if (
            _hash(canonical_json_bytes({k: value[k] for k in ("allowed_paths", "forbidden_paths")}))
            != value["scope_fingerprint"]
        ):
            _deny("start scope fingerprint differs")
        issued, expires = (_timestamp(value[k]) for k in ("issued_at", "expires_at"))
        if not timedelta(0) < expires - issued <= timedelta(hours=1):
            _deny("start expiry outside bounded window")
        object.__setattr__(self, "canonical_body", data)

    @property
    def value(self):
        return _freeze(json.loads(self.canonical_body))

    @property
    def fingerprint(self):
        return _hash(self.canonical_body)


def _start_request_hash(request):
    from dataclasses import asdict

    value = asdict(request)
    value["created_at"] = request.created_at.astimezone(UTC).isoformat()
    return _hash(canonical_json_bytes(value))


def _bind_start_request(permit, request):
    v = permit.value
    if (
        request.project_id != v["project_id"]
        or request.work_run_id != v["work_run_id"]
        or request.task_contract_id != v["contract_id"]
        or request.task_contract_version != "v" + str(v["contract_version"])
        or request.observed_state is not WorkflowState.READY
        or request.observed_state_version != v["state_version"]
        or request.target_state is not WorkflowState.RUNNING
        or request.runtime_mode is not RuntimeMode.OWNER_SELF_DOGFOOD
        or request.evidence_refs
        or request.human_result_refs
        or request.judgment_refs
        or request.blocker_claim
        or request.blocker_resolution_claim
    ):
        _deny("exact external start request denied")


@dataclass(frozen=True)
class ExternalIdeExecutionStartRef:
    permit: ExternalIdeExecutionStartPermitV1
    request_hash: str
    _owner_token: object


@dataclass(frozen=True)
class VerifiedExternalIdeExecutionStartV1:
    start_ref: ExternalIdeExecutionStartRef

    @property
    def common_ref(self):
        ref = self.start_ref
        if _START_REFS.get(id(ref)) is not ref or ref._owner_token is not _START_OWNER:
            _deny("unverified external start")
        return ref


def _start_ref(permit, request):
    ref = ExternalIdeExecutionStartRef(permit, _start_request_hash(request), _START_OWNER)
    _START_REFS[id(ref)] = ref
    return ref


def verify_external_start_ref(ref, request):
    if (
        type(ref) is not ExternalIdeExecutionStartRef
        or ref._owner_token is not _START_OWNER
        or _START_REFS.get(id(ref)) is not ref
    ):
        return False
    try:
        _bind_start_request(ref.permit, request)
        return ref.request_hash == _start_request_hash(request)
    except (ValueError, TypeError):
        return False


async def _load_start_permit(session, permit_id):
    from aiscc.persistence.models import ExternalIdeExecutionStartPermitRow

    row = await session.get(ExternalIdeExecutionStartPermitRow, permit_id)
    if row is None:
        _deny("start permit missing")
    permit = ExternalIdeExecutionStartPermitV1(
        verify_canonical_json_bytes(bytes(row.canonical_body))
    )
    if (
        row.permit_id != permit.value["permit_id"]
        or row.work_run_id != permit.value["work_run_id"]
        or row.producer_kind != PRODUCER
        or row.body_sha256 != permit.fingerprint
    ):
        _deny("AUTHORITY_CORRUPTION: start permit")
    return permit


def _start_body(permit, request, started_at):
    return canonical_json_bytes(
        dict(
            schema="AISCC-EXTERNAL-IDE-START-V1",
            started_at=started_at,
            producer=PRODUCER,
            start_id=START_PREFIX + permit.value["permit_id"],
            permit_fingerprint=permit.fingerprint,
            transition_request_id=request.transition_request_id,
            request_hash=_start_request_hash(request),
        )
    )


async def verify_external_start_in_session(session, start_id):
    """Reconstruct only committed historical start lineage; never a provider attempt."""
    from aiscc.persistence.models import ExternalIdeExecutionStartRow, TaskContractBodyRow
    from aiscc.workflow.models import GuardId

    row = await session.get(ExternalIdeExecutionStartRow, start_id)
    if row is None:
        _deny("external start missing")
    permit = await _load_start_permit(session, row.permit_id)
    v = permit.value
    body_row = await session.get(TaskContractBodyRow, v["body_ref"])
    if body_row is None:
        _deny("AUTHORITY_CORRUPTION: start TaskContract missing")
    body = TaskContractBodyV1.from_bytes(bytes(body_row.canonical_body))
    if body.body_sha256 != body_row.body_sha256 or body.body_ref != body_row.body_ref:
        _deny("AUTHORITY_CORRUPTION: start TaskContract hash")
    _bind_body(permit, body)
    ready = await verify_historical_transition_provenance(session, v["ready_transition_id"])
    _bind_ready(
        permit,
        ready.request,
        ready.decision.resulting_state,
        ready.decision.resulting_state_version,
    )
    raw = verify_canonical_json_bytes(bytes(row.canonical_body))
    started_at = raw.get("started_at")
    if not _timestamp(v["issued_at"]) <= _timestamp(started_at) < _timestamp(v["expires_at"]):
        _deny("AUTHORITY_CORRUPTION: start time outside permit")
    source = await verify_historical_transition_provenance(session, row.transition_request_id)
    _bind_start_request(permit, source.request)
    if (
        source.decision.resulting_state is not WorkflowState.RUNNING
        or source.decision.resulting_state_version != v["state_version"] + 1
        or row.start_id != START_PREFIX + v["permit_id"]
        or row.producer_kind != PRODUCER
        or row.work_run_id != v["work_run_id"]
        or bytes(row.canonical_body) != _start_body(permit, source.request, started_at)
        or row.body_sha256 != _hash(bytes(row.canonical_body))
    ):
        _deny("AUTHORITY_CORRUPTION: external start lineage")
    guards = [g for g in source.evaluation.guards if g.guard_id is GuardId.G_EXECUTION_STARTED]
    if (
        len(guards) != 1
        or not guards[0].satisfied
        or guards[0].reason != "P1_5_EXECUTION_REF_VERIFIED"
        or guards[0].authority_ref != "p1-5:ExternalIdeExecutionStartRef"
    ):
        _deny("AUTHORITY_CORRUPTION: start guard provenance")
    return VerifiedExternalIdeExecutionStartV1(_start_ref(permit, source.request))


def _bind_ready(permit, run, state, version):
    v = permit.value
    if (
        run.work_run_id != v["work_run_id"]
        or run.project_id != v["project_id"]
        or run.task_contract_id != v["contract_id"]
        or run.task_contract_version != "v" + str(v["contract_version"])
        or run.runtime_mode is not RuntimeMode.OWNER_SELF_DOGFOOD
        or state is not WorkflowState.READY
        or version != v["state_version"]
    ):
        _deny("exact READY WorkRun required")


class ExternalIdeExecutionStartRepository:
    """Trusted local start composition; start opens authority, it never edits source."""

    def __init__(
        self,
        sessions,
        task_authority,
        observer,
        *,
        system_authority,
        transition_repository,
        clock=lambda: datetime.now(UTC),
    ):
        from aiscc.persistence.repository import PostgresTransitionRepository
        from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository
        from aiscc.workflow.guards import P1_4GuardAuthority

        if (
            type(task_authority) is not PostgresExternalTaskAuthorityRepository
            or type(observer) is not LocalGitObserver
            or type(system_authority) is not P1_4GuardAuthority
            or type(transition_repository) is not PostgresTransitionRepository
        ):
            _deny("existing trusted start owners required")
        self._sessions, self._tasks, self._observer = sessions, task_authority, observer
        self._system, self._transitions, self._clock = (
            system_authority,
            transition_repository,
            clock,
        )
        self.__writer = None

    def _fresh(self, permit, capability, inner_task_bytes):
        v = permit.value
        if not isinstance(capability, str) or not hmac.compare_digest(
            _hash(capability.encode()), v["capability_hash"]
        ):
            _deny("start capability denied")
        if type(inner_task_bytes) is not bytes or _hash(inner_task_bytes) != v["inner_task_sha256"]:
            _deny("start task hash denied")
        if not _timestamp(v["issued_at"]) <= _now(self._clock) < _timestamp(v["expires_at"]):
            _deny("start permit expired/stale")

    async def _current(self, session, permit):
        v = permit.value
        await acquire_work_run_transaction_lock(session, v["work_run_id"])
        ready = await verify_historical_transition_provenance(session, v["ready_transition_id"])
        _bind_ready(permit, ready.work_run, ready.work_run.state, ready.work_run.state_version)
        _bind_ready(
            permit,
            ready.request,
            ready.decision.resulting_state,
            ready.decision.resulting_state_version,
        )
        receipt = await self._tasks.get_task_contract(
            v["project_id"], v["contract_id"], v["contract_version"], session=session
        )
        if receipt is None:
            _deny("start TaskContract missing")
        _bind_body(permit, receipt.body)
        await self._tasks.verify_task_contract(
            receipt,
            require_current=True,
            expected_repository_binding={
                k: v[k] for k in ("repository_id", "repository_root", "base_commit")
            },
            expected_next_action_ref=receipt.body.value["source_next_action"]["action_ref"],
            session=session,
        )
        first = self._observer.observe(permit)
        second = self._observer.observe(permit)
        if (
            first.root != second.root
            or second.value["head"] != v["base_commit"]
            or second.value["entries"]
            or second.value["index"]
            or not second.value["diff_check"]
        ):
            _deny("start requires clean exact repository/base")

    def _bind_writer(self):
        if self.__writer is not None:
            _deny("start writer already bound")
        self.__writer = object()
        return _ExternalIdeStartWriter(self, self.__writer)

    async def _issue(
        self,
        writer,
        session,
        *,
        receipt,
        work_run_id,
        state_version,
        ready_transition_id,
        inner_task_bytes,
        ttl,
    ):
        from aiscc.persistence.models import ExternalIdeExecutionStartPermitRow

        if writer is not self.__writer or writer is None or not session.in_transaction():
            _deny("trusted start writer/caller transaction required")
        if type(inner_task_bytes) is not bytes or not inner_task_bytes:
            _deny("exact Task bytes required")
        t = receipt.body.value
        token, now = secrets.token_urlsafe(32), _now(self._clock)
        scope = {k: t[k] for k in ("allowed_paths", "forbidden_paths")}
        permit = ExternalIdeExecutionStartPermitV1(
            dict(
                schema="AISCC-EXTERNAL-IDE-START-PERMIT-V1",
                producer=PRODUCER,
                project_id=t["project_id"],
                permit_id="local-ide-start-" + uuid4().hex,
                work_run_id=work_run_id,
                state="READY",
                state_version=state_version,
                task_id=t["task_id"],
                contract_id=t["contract_id"],
                contract_version=t["contract_version"],
                body_ref=receipt.body.body_ref,
                body_sha256=receipt.body.body_sha256,
                **plain(t["repository_binding"]),
                inner_task_sha256=_hash(inner_task_bytes),
                **scope,
                scope_fingerprint=_hash(canonical_json_bytes(scope)),
                issued_at=now.isoformat(),
                expires_at=(now + ttl).isoformat(),
                capability_hash=_hash(token.encode()),
                ready_transition_id=ready_transition_id,
            )
        )
        await self._current(session, permit)
        self._fresh(permit, token, inner_task_bytes)
        session.add(
            ExternalIdeExecutionStartPermitRow(
                permit_id=permit.value["permit_id"],
                work_run_id=work_run_id,
                producer_kind=PRODUCER,
                canonical_body=permit.canonical_body,
                body_sha256=permit.fingerprint,
            )
        )
        await session.flush()
        return permit, token

    async def start(self, *, permit_id, capability, inner_task_bytes, request):
        # Only this composition receives a transient pre-start ref. It never returns a
        # ref/fact/participant before P1-4's transaction has committed successfully.
        from aiscc.persistence.models import ExternalIdeExecutionStartRow

        async with self._sessions() as session, session.begin():
            permit = await _load_start_permit(session, permit_id)
            self._fresh(permit, capability, inner_task_bytes)
            _bind_start_request(permit, request)
            old = await session.get(ExternalIdeExecutionStartRow, START_PREFIX + permit_id)
            if old is not None:
                verified = await verify_external_start_in_session(session, old.start_id)
                if not verify_external_start_ref(verified.common_ref, request):
                    _deny("changed start retry")
            else:
                await self._current(session, permit)
        participant = _ExternalIdeStartParticipant(
            self, permit, capability, inner_task_bytes, request
        )
        try:
            return await self._transitions.decide(request, (), transaction_participant=participant)
        finally:
            participant.close()

    async def resolve(self, start_id):
        async with self._sessions() as session, session.begin():
            return await verify_external_start_in_session(session, start_id)


class _ExternalIdeStartWriter:
    def __init__(self, repository, token):
        self._repository, self._token = repository, token

    async def issue(self, session, **kwargs):
        return await self._repository._issue(self._token, session, **kwargs)


def _bind_external_ide_start_writer(repository):
    return repository._bind_writer()


class _ExternalIdeStartParticipant:
    def __init__(self, repository, permit, capability, task, request):
        self.repo, self.permit, self.capability, self.task, self.request = (
            repository,
            permit,
            capability,
            task,
            request,
        )
        self.ref = _start_ref(permit, request)

    def close(self):
        _START_REFS.pop(id(self.ref), None)
        self.capability = None

    def facts(self, request):
        from aiscc.providers.authority import ExecutionReferenceAuthority
        from aiscc.workflow.models import GuardId

        if request != self.request:
            _deny("start participant request differs")
        system = self.repo._system
        facts = tuple(
            system.issue(
                guard_id=g,
                satisfied=True,
                reason="EXTERNAL_IDE_CURRENT_TASK_VERIFIED",
                authority_ref="external-ide-start-permit:" + self.permit.fingerprint,
                request=request,
            )
            for g in (GuardId.G_CONTRACT, GuardId.G_SCOPE, GuardId.G_RUNTIME_CONTEXT)
        )
        return (
            *facts,
            system.issue_from_execution_ref(
                guard_id=GuardId.G_EXECUTION_STARTED,
                execution_ref=self.ref,
                verifier=ExecutionReferenceAuthority(),
                request=request,
            ),
        )

    async def prepare(self, session, request, current):
        from aiscc.persistence.models import ExternalIdeExecutionStartRow

        if request != self.request or current is None:
            _deny("start current request missing")
        _bind_ready(self.permit, current, current.state, current.state_version)
        permit = await _load_start_permit(session, self.permit.value["permit_id"])
        if permit.canonical_body != self.permit.canonical_body:
            _deny("start permit changed")
        if (
            await session.get(
                ExternalIdeExecutionStartRow, START_PREFIX + permit.value["permit_id"]
            )
            is not None
        ):
            _deny("start permit already consumed")
        await self.repo._current(session, permit)
        self.repo._fresh(permit, self.capability, self.task)

    def after_evaluation(self, request):
        self.close()

    async def after_decision(self, session, request, evaluation, decision, current):
        from aiscc.persistence.models import ExternalIdeExecutionStartRow
        from aiscc.workflow.models import DecisionOutcome

        if decision.outcome is not DecisionOutcome.ADMITTED:
            _deny("P1-4 start denied; rollback")
        # Recheck expiry immediately before append; owner locks are still held.
        now = _now(self.repo._clock)
        if (
            not _timestamp(self.permit.value["issued_at"])
            <= now
            < _timestamp(self.permit.value["expires_at"])
        ):
            _deny("start expired before commit")
        body = _start_body(self.permit, request, now.isoformat())
        session.add(
            ExternalIdeExecutionStartRow(
                start_id=START_PREFIX + self.permit.value["permit_id"],
                permit_id=self.permit.value["permit_id"],
                work_run_id=request.work_run_id,
                transition_request_id=request.transition_request_id,
                producer_kind=PRODUCER,
                canonical_body=body,
                body_sha256=_hash(body),
            )
        )
        await session.flush()
