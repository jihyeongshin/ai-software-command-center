"""One-time external Command Center authority for an empty self-dogfood project."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import select, text

from aiscc.contracts.canonical_json import canonical_json_bytes, canonical_sha256
from aiscc.persistence.models import (
    AdmittedCycleRow,
    GenesisAuthorityRow,
    NextActionProjectionRow,
    NextActionSelectionRow,
    ProjectMemoryEntryRow,
    ProjectMemoryViewRow,
    TaskContractBodyRow,
    WorkRunRow,
)
from aiscc.task_authority.contracts import TaskContractError, fingerprint, string

MODE = "SELF_DOGFOOD_GENESIS"
ACTION = "open-self-dogfood-genesis-task-issuance"
OWNER = "EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY"
ISSUER_VERSION = "SELF_DOGFOOD_GENESIS_AUTHORITY_V1"


@dataclass(frozen=True)
class GenesisContextV1:
    project_id: str
    repository_id: str
    repository_root: str
    base_commit: str
    phase_id: str
    runtime_mode: str = "OWNER_SELF_DOGFOOD"
    cycle_execution_mode: str = "AISCC_SELF_DOGFOOD"

    def __post_init__(self):
        for value in (self.project_id, self.repository_id, self.phase_id):
            string(value, 96)
        string(self.repository_root, 4096)
        if (
            not Path(self.repository_root).is_absolute()
            or re.fullmatch(r"[0-9a-f]{40}", self.base_commit) is None
            or self.runtime_mode != "OWNER_SELF_DOGFOOD"
            or self.cycle_execution_mode != "AISCC_SELF_DOGFOOD"
        ):
            raise TaskContractError("GENESIS_NOT_ELIGIBLE: repository/runtime context")

    def payload(self):
        return {name: getattr(self, name) for name in self.__dataclass_fields__}


@dataclass(frozen=True)
class GenesisNextActionAuthorityV1:
    canonical_body: bytes

    def __post_init__(self):
        value = json.loads(self.canonical_body)
        context_fields = set(GenesisContextV1.__dataclass_fields__)
        if set(value) != context_fields | {
            "genesis_authority_id",
            "source_mode",
            "action_id",
            "issuer",
            "issuer_version",
            "issued_at",
        }:
            raise TaskContractError("AUTHORITY_CORRUPTION: genesis fields")
        GenesisContextV1(**{k: value[k] for k in context_fields})
        string(value["genesis_authority_id"], 96)
        if (
            value["source_mode"] != MODE
            or value["action_id"] != ACTION
            or value["issuer"] != OWNER
            or value["issuer_version"] != ISSUER_VERSION
            or canonical_json_bytes(value) != self.canonical_body
        ):
            raise TaskContractError("AUTHORITY_CORRUPTION: genesis canonical identity")
        stamp = datetime.fromisoformat(value["issued_at"])
        if (
            stamp.tzinfo is None
            or stamp.astimezone(UTC).isoformat(timespec="microseconds") != value["issued_at"]
        ):
            raise TaskContractError("AUTHORITY_CORRUPTION: genesis timestamp")

    @property
    def value(self):
        return json.loads(self.canonical_body)

    @property
    def fingerprint(self):
        return canonical_sha256(self.value)

    @property
    def authority_ref(self):
        return "self-dogfood-genesis:v1:" + self.value["genesis_authority_id"]


async def lock_genesis_project(session, project_id):
    # This is the existing Cycle owner's project lock, never a WorkRun lock.
    await session.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:key, 0))"),
        {"key": f"p1-8-memory-project:{project_id}"},
    )


class GenesisAuthorityRepository:
    def __init__(self, sessions, *, context: GenesisContextV1):
        self._sessions = sessions
        self.__context = context
        self.__capability = None

    @property
    def context(self):
        return self.__context

    async def read(self, session, authority_ref, expected_fingerprint):
        fingerprint(expected_fingerprint)
        row = await session.get(GenesisAuthorityRow, authority_ref)
        if row is None or row.record_kind != "ISSUED":
            raise TaskContractError("AUTHORITY_CORRUPTION: genesis absent")
        authority = GenesisNextActionAuthorityV1(bytes(row.canonical_body))
        if (
            authority.authority_ref != row.record_id
            or authority.fingerprint != row.fingerprint
            or authority.fingerprint != expected_fingerprint
            or authority.value["project_id"] != row.project_id
            or row.issued_at.astimezone(UTC).isoformat(timespec="microseconds")
            != authority.value["issued_at"]
        ):
            raise TaskContractError("AUTHORITY_CORRUPTION: genesis projection")
        return authority

    async def verify_current(
        self, session, authority_ref, expected_fingerprint, *, selection_id=None
    ):
        await self._lock_currentness(session)
        authority = await self.read(session, authority_ref, expected_fingerprint)
        if any(authority.value[k] != v for k, v in self.context.payload().items()):
            raise TaskContractError("GENESIS_NOT_ELIGIBLE: enrolled context differs")
        await self._eligible(session, selection_id=selection_id, allow_bound_runs=True)
        return authority

    async def _lock_currentness(self, session):
        await session.execute(
            text("SELECT pg_advisory_xact_lock(hashtextextended(:key, 0))"),
            {"key": f"p1-8-next-action-project:{self.context.project_id}"},
        )
        await lock_genesis_project(session, self.context.project_id)

    async def _eligible(self, session, *, selection_id=None, allow_bound_runs=False):
        project = self.context.project_id
        cycle = await session.scalar(
            select(AdmittedCycleRow.cycle_id).where(AdmittedCycleRow.project_id == project).limit(1)
        )
        memory = await session.scalar(
            select(ProjectMemoryEntryRow.entry_id)
            .join(
                ProjectMemoryViewRow,
                ProjectMemoryViewRow.current_entry_id == ProjectMemoryEntryRow.entry_id,
            )
            .where(
                ProjectMemoryEntryRow.project_id == project,
                ProjectMemoryEntryRow.category == "NEXT_ACTION_CONTEXT",
                ProjectMemoryViewRow.state == "CURRENT",
            )
            .limit(1)
        )
        if cycle is not None or memory is not None:
            raise TaskContractError("GENESIS_NOT_ELIGIBLE: operational Cycle/current context")
        projection = await session.get(NextActionProjectionRow, project, populate_existing=True)
        if (
            projection is not None
            and projection.state == "CURRENT"
            and projection.selection_id != selection_id
        ):
            raise TaskContractError("GENESIS_NOT_ELIGIBLE: conflicting current selection")
        if projection is not None and projection.state == "CURRENT":
            selected = await session.get(NextActionSelectionRow, projection.selection_id)
            issued = await session.scalar(
                select(GenesisAuthorityRow).where(
                    GenesisAuthorityRow.project_id == project,
                    GenesisAuthorityRow.record_kind == "ISSUED",
                )
            )
            if (
                selected is None
                or issued is None
                or selected.payload.get("parameters")
                != {
                    "genesis_authority_ref": issued.record_id,
                    "genesis_authority_fingerprint": issued.fingerprint,
                }
            ):
                raise TaskContractError("GENESIS_NOT_ELIGIBLE: conflicting selection source")
        binding = await session.scalar(
            select(GenesisAuthorityRow).where(
                GenesisAuthorityRow.project_id == project,
                GenesisAuthorityRow.record_kind == "TASK_BOUND",
            )
        )
        bound = self._binding_value(binding) if binding is not None else None
        bodies = tuple(
            await session.scalars(
                select(TaskContractBodyRow).where(TaskContractBodyRow.project_id == project)
            )
        )
        genesis_bodies = [
            b
            for b in bodies
            if json.loads(bytes(b.canonical_body))
            .get("source_next_action", {})
            .get("genesis_authority")
            is not None
        ]
        if bound is None and genesis_bodies:
            raise TaskContractError("AUTHORITY_CORRUPTION: missing genesis family binding")
        if bound is not None and (
            len(genesis_bodies) != 1
            or genesis_bodies[0].body_ref != bound["body_ref"]
            or genesis_bodies[0].body_sha256 != bound["body_sha256"]
        ):
            raise TaskContractError("AUTHORITY_CORRUPTION: partial genesis body/family")
        runs = tuple(
            await session.scalars(select(WorkRunRow).where(WorkRunRow.project_id == project))
        )
        for run in runs:
            if (
                not allow_bound_runs
                or bound is None
                or (run.task_contract_id, run.task_contract_version) != (bound["contract_id"], "v1")
            ):
                raise TaskContractError("GENESIS_NOT_ELIGIBLE: pre-existing operational WorkRun")

    @staticmethod
    def _binding_value(row):
        value = json.loads(bytes(row.canonical_body))
        if (
            set(value)
            != {
                "project_id",
                "authority_ref",
                "authority_fingerprint",
                "contract_id",
                "task_id",
                "body_ref",
                "body_sha256",
                "issued_at",
            }
            or canonical_json_bytes(value) != bytes(row.canonical_body)
            or canonical_sha256(value) != row.fingerprint
            or value["project_id"] != row.project_id
            or row.record_id != "self-dogfood-genesis-task:v1:" + row.project_id
            or row.issued_at.astimezone(UTC).isoformat(timespec="microseconds")
            != value["issued_at"]
        ):
            raise TaskContractError("AUTHORITY_CORRUPTION: genesis family binding")
        return value

    async def _bind_task(self, session, body, authority, issued_at):
        v = body.value
        if v["contract_version"] != 1:
            raise TaskContractError("GENESIS_NOT_ELIGIBLE: one exact contract version")
        record_id = "self-dogfood-genesis-task:v1:" + self.context.project_id
        value = {
            "project_id": v["project_id"],
            "authority_ref": authority.authority_ref,
            "authority_fingerprint": authority.fingerprint,
            "contract_id": v["contract_id"],
            "task_id": v["task_id"],
            "body_ref": body.body_ref,
            "body_sha256": body.body_sha256,
            "issued_at": issued_at.astimezone(UTC).isoformat(timespec="microseconds"),
        }
        existing = await session.get(GenesisAuthorityRow, record_id)
        if existing is not None:
            prior = self._binding_value(existing)
            if {k: v for k, v in prior.items() if k != "issued_at"} != {
                k: v for k, v in value.items() if k != "issued_at"
            }:
                raise TaskContractError("GENESIS_NOT_ELIGIBLE: different TaskContract family/body")
            return
        session.add(
            GenesisAuthorityRow(
                record_id=record_id,
                project_id=v["project_id"],
                record_kind="TASK_BOUND",
                canonical_body=canonical_json_bytes(value),
                fingerprint=canonical_sha256(value),
                issued_at=issued_at,
            )
        )

    async def _issue(self, capability, authority_id, issued_at):
        if capability is None or capability is not self.__capability:
            raise TaskContractError("GENESIS_AUTHORITY_ACCESS_DENIED")
        if issued_at.tzinfo is None:
            raise TaskContractError("genesis requires aware issuance time")
        value = {
            **self.context.payload(),
            "genesis_authority_id": authority_id,
            "source_mode": MODE,
            "action_id": ACTION,
            "issuer": OWNER,
            "issuer_version": ISSUER_VERSION,
            "issued_at": issued_at.astimezone(UTC).isoformat(timespec="microseconds"),
        }
        proposed = GenesisNextActionAuthorityV1(canonical_json_bytes(value))
        async with self._sessions() as session, session.begin():
            await self._lock_currentness(session)
            existing = await session.scalar(
                select(GenesisAuthorityRow).where(
                    GenesisAuthorityRow.project_id == self.context.project_id,
                    GenesisAuthorityRow.record_kind == "ISSUED",
                )
            )
            if existing is not None:
                authority = await self.read(session, existing.record_id, existing.fingerprint)
                if {k: v for k, v in authority.value.items() if k != "issued_at"} != {
                    k: v for k, v in proposed.value.items() if k != "issued_at"
                }:
                    raise TaskContractError("GENESIS_NOT_ELIGIBLE: different genesis authority")
                projection = await session.get(NextActionProjectionRow, self.context.project_id)
                own_selection = None
                if projection is not None and projection.selection_id is not None:
                    selected = await session.get(NextActionSelectionRow, projection.selection_id)
                    if selected is not None and selected.payload.get("parameters") == {
                        "genesis_authority_ref": authority.authority_ref,
                        "genesis_authority_fingerprint": authority.fingerprint,
                    }:
                        own_selection = selected.selection_id
                await self._eligible(session, selection_id=own_selection, allow_bound_runs=True)
                return authority
            await self._eligible(session)
            session.add(
                GenesisAuthorityRow(
                    record_id=proposed.authority_ref,
                    project_id=self.context.project_id,
                    record_kind="ISSUED",
                    canonical_body=proposed.canonical_body,
                    fingerprint=proposed.fingerprint,
                    issued_at=issued_at,
                )
            )
            return proposed

    def _bind_writer_once(self):
        if self.__capability is not None:
            raise TaskContractError("genesis writer already bound")
        self.__capability = object()
        return _GenesisWriter(self, self.__capability)


class _GenesisWriter:
    def __init__(self, repository, capability):
        self.__repository, self.__capability = repository, capability

    async def issue(self, *, authority_id, issued_at):
        return await self.__repository._issue(self.__capability, authority_id, issued_at)

    def __reduce__(self):
        raise TypeError("genesis writer cannot be serialized")

    def __copy__(self):
        raise TypeError("genesis writer cannot be copied")

    def __deepcopy__(self, memo):
        raise TypeError("genesis writer cannot be copied")


async def verify_genesis_task_binding(session, body):
    """Historical reciprocity check; never makes the source current again."""
    v = body.value
    claim = v["source_next_action"]["genesis_authority"]
    row = await session.get(GenesisAuthorityRow, "self-dogfood-genesis-task:v1:" + v["project_id"])
    if row is None or row.record_kind != "TASK_BOUND":
        raise TaskContractError("AUTHORITY_CORRUPTION: genesis task binding absent")
    bound = GenesisAuthorityRepository._binding_value(row)
    expected = {
        "project_id": v["project_id"],
        "authority_ref": claim["authority_ref"],
        "authority_fingerprint": claim["fingerprint"],
        "contract_id": v["contract_id"],
        "task_id": v["task_id"],
        "body_ref": body.body_ref,
        "body_sha256": body.body_sha256,
    }
    if {k: x for k, x in bound.items() if k != "issued_at"} != expected:
        raise TaskContractError("AUTHORITY_CORRUPTION: genesis task binding differs")
    context = GenesisContextV1(
        project_id=v["project_id"], **v["repository_binding"], phase_id=claim["phase_id"]
    )
    reader = GenesisAuthorityRepository(None, context=context)
    authority = await reader.read(session, claim["authority_ref"], claim["fingerprint"])
    if any(authority.value[k] != x for k, x in context.payload().items()):
        raise TaskContractError("AUTHORITY_CORRUPTION: genesis Task context differs")
