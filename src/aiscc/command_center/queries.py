from __future__ import annotations

import base64
import binascii
import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol

from aiscc.command_center.read_models import (
    CycleData,
    EvidenceData,
    ExecutionData,
    HumanJudgmentData,
    NextActionData,
    OutcomesData,
    QueueData,
    ReadModel,
    TransitionsData,
    WorkRunData,
)


class CommandCenterReadError(RuntimeError):
    pass


class InvalidQueryError(CommandCenterReadError):
    pass


class ReadModelNotFoundError(CommandCenterReadError):
    pass


class AuthorityConflictReadError(CommandCenterReadError):
    pass


class NoLongerCurrentReadError(CommandCenterReadError):
    pass


class ProjectionUnavailableReadError(CommandCenterReadError):
    pass


@dataclass(frozen=True, slots=True)
class QueueFilters:
    workflow_state: str | None = None
    execution_status: str | None = None
    human_gate_status: str | None = None
    judgment_presence: str | None = None
    judgment_kind: str | None = None
    terminal: bool | None = None
    q: str | None = None


@dataclass(frozen=True, slots=True)
class QueryResult[DataT: ReadModel]:
    data: DataT
    snapshot_at: datetime
    source_revisions: dict[str, int | str]
    next_cursor: str | None = None
    poll_after_ms: int | None = 10_000


class CommandCenterQueries(Protocol):
    async def queue(
        self,
        project_id: str,
        *,
        filters: QueueFilters,
        cursor: str | None,
        limit: int,
    ) -> QueryResult[QueueData]: ...

    async def work_run(self, work_run_id: str) -> QueryResult[WorkRunData]: ...

    async def transitions(self, work_run_id: str) -> QueryResult[TransitionsData]: ...

    async def execution(self, work_run_id: str) -> QueryResult[ExecutionData]: ...

    async def evidence(self, work_run_id: str) -> QueryResult[EvidenceData]: ...

    async def human_judgment(self, work_run_id: str) -> QueryResult[HumanJudgmentData]: ...

    async def outcomes(
        self, project_id: str, *, cursor: str | None, limit: int
    ) -> QueryResult[OutcomesData]: ...

    async def cycle(self, cycle_id: str) -> QueryResult[CycleData]: ...

    async def next_action(self, project_id: str) -> QueryResult[NextActionData]: ...


class UnavailableCommandCenterQueries:
    async def _unavailable(self) -> None:
        raise ProjectionUnavailableReadError("command center read store is not configured")

    async def queue(
        self,
        project_id: str,
        *,
        filters: QueueFilters,
        cursor: str | None,
        limit: int,
    ) -> QueryResult[QueueData]:
        del project_id, filters, cursor, limit
        await self._unavailable()
        raise AssertionError("unreachable")

    async def work_run(self, work_run_id: str) -> QueryResult[WorkRunData]:
        del work_run_id
        await self._unavailable()
        raise AssertionError("unreachable")

    async def transitions(self, work_run_id: str) -> QueryResult[TransitionsData]:
        del work_run_id
        await self._unavailable()
        raise AssertionError("unreachable")

    async def execution(self, work_run_id: str) -> QueryResult[ExecutionData]:
        del work_run_id
        await self._unavailable()
        raise AssertionError("unreachable")

    async def evidence(self, work_run_id: str) -> QueryResult[EvidenceData]:
        del work_run_id
        await self._unavailable()
        raise AssertionError("unreachable")

    async def human_judgment(self, work_run_id: str) -> QueryResult[HumanJudgmentData]:
        del work_run_id
        await self._unavailable()
        raise AssertionError("unreachable")

    async def outcomes(
        self, project_id: str, *, cursor: str | None, limit: int
    ) -> QueryResult[OutcomesData]:
        del project_id, cursor, limit
        await self._unavailable()
        raise AssertionError("unreachable")

    async def cycle(self, cycle_id: str) -> QueryResult[CycleData]:
        del cycle_id
        await self._unavailable()
        raise AssertionError("unreachable")

    async def next_action(self, project_id: str) -> QueryResult[NextActionData]:
        del project_id
        await self._unavailable()
        raise AssertionError("unreachable")


def validate_limit(limit: int) -> int:
    if isinstance(limit, bool) or not 1 <= limit <= 100:
        raise InvalidQueryError("limit must be between 1 and 100")
    return limit


def encode_cursor(*, shape: dict[str, object], position: dict[str, object]) -> str:
    body = {
        "v": 1,
        "shape": _shape_hash(shape),
        "position": position,
    }
    encoded = json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(encoded).rstrip(b"=").decode("ascii")


def decode_cursor(cursor: str, *, shape: dict[str, object]) -> dict[str, object]:
    if not cursor or len(cursor) > 2048 or not cursor.isascii():
        raise InvalidQueryError("cursor is invalid")
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        raw = base64.b64decode(padded, altchars=b"-_", validate=True)
        value = json.loads(raw.decode("utf-8"))
    except (binascii.Error, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise InvalidQueryError("cursor is invalid") from exc
    if (
        not isinstance(value, dict)
        or value.get("v") != 1
        or value.get("shape") != _shape_hash(shape)
        or not isinstance(value.get("position"), dict)
    ):
        raise InvalidQueryError("cursor does not match this query")
    return {str(key): item for key, item in value["position"].items()}


def utc_snapshot(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        raise AuthorityConflictReadError("database returned a naive timestamp")
    return value.astimezone(UTC)


def _shape_hash(shape: dict[str, object]) -> str:
    canonical = json.dumps(shape, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()
