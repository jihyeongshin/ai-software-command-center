"""Mediated durable start queue adapter; no semantic-policy SQL."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.public_live.start_authority import PublicLiveStartCandidate, StartContract


@dataclass(frozen=True, slots=True)
class StartLease:
    run_id: bytes
    candidate_id: bytes
    work_run_id: str
    phase: str
    phase_version: int
    lease_generation: int
    lease_expires_at: datetime
    candidate: dict[str, Any]


class StartRepository:
    def __init__(self, sessions: async_sessionmaker[AsyncSession]) -> None:
        self._sessions = sessions

    async def verify_runtime_identity(self) -> None:
        async with self._sessions() as session:
            row = (await session.execute(text("SELECT session_user,current_user"))).one()
        if tuple(row) != ("aiscc_live_initializer_login", "aiscc_public_live_initializer"):
            raise RuntimeError("START_INITIALIZER_RUNTIME_ROLE_DENIED")

    async def register(self, candidate: PublicLiveStartCandidate, contract: StartContract) -> bytes:
        payload = candidate.payload(contract)
        candidate_id = candidate.candidate_id(contract)
        payload["candidate_id"] = candidate_id.hex()
        async with self._sessions() as session, session.begin():
            result = await session.scalar(
                text(
                    "SELECT public_live_api.start_register_from_admission(:r,:c,CAST(:p AS jsonb))"
                ),
                {"r": candidate.public_run_id, "c": candidate_id, "p": json.dumps(payload)},
            )
        if not isinstance(result, (bytes, bytearray)) or bytes(result) != candidate_id:
            raise RuntimeError("START_REGISTRATION_INVALID")
        return candidate_id

    async def next(self, process_id: bytes) -> StartLease | None:
        async with self._sessions() as session, session.begin():
            value = await session.scalar(
                text("SELECT public_live_api.start_next(:p)"), {"p": process_id}
            )
        return _lease(value)

    async def renew(self, lease: StartLease, process_id: bytes) -> StartLease:
        async with self._sessions() as session, session.begin():
            value = await session.scalar(
                text("SELECT public_live_api.start_renew(:r,:p,:g)"),
                {"r": lease.run_id, "p": process_id, "g": lease.lease_generation},
            )
        result = _lease(value)
        if result is None:
            raise RuntimeError("START_LEASE_LOST")
        return result

    async def context(self, lease: StartLease, process_id: bytes) -> dict[str, Any]:
        async with self._sessions() as session, session.begin():
            value = await session.scalar(
                text("SELECT public_live_api.start_context(:r,:p,:g)"),
                {"r": lease.run_id, "p": process_id, "g": lease.lease_generation},
            )
        if not isinstance(value, dict):
            raise RuntimeError("START_CONTEXT_INVALID")
        return value

    async def record(
        self, lease: StartLease, process_id: bytes, phase: str, source_identity: bytes
    ) -> StartLease:
        async with self._sessions() as session, session.begin():
            value = await session.scalar(
                text("SELECT public_live_api.start_record_phase(:r,:p,:g,:h,:s)"),
                {
                    "r": lease.run_id,
                    "p": process_id,
                    "g": lease.lease_generation,
                    "h": phase,
                    "s": source_identity,
                },
            )
        result = _lease(value)
        if result is None:
            raise RuntimeError("START_PHASE_INVALID")
        return result

    async def halt(
        self, lease: StartLease, process_id: bytes, reason: str, source_identity: bytes
    ) -> None:
        async with self._sessions() as session, session.begin():
            await session.execute(
                text("SELECT public_live_api.start_halt(:r,:p,:g,:h,:s)"),
                {
                    "r": lease.run_id,
                    "p": process_id,
                    "g": lease.lease_generation,
                    "h": reason,
                    "s": source_identity,
                },
            )

    async def set_attempt(
        self,
        lease: StartLease,
        process_id: bytes,
        attempt_id: str,
        source_identity: bytes,
    ) -> StartLease:
        async with self._sessions() as session, session.begin():
            value = await session.scalar(
                text("SELECT public_live_api.start_set_attempt(:r,:p,:g,:a,:s)"),
                {
                    "r": lease.run_id,
                    "p": process_id,
                    "g": lease.lease_generation,
                    "a": attempt_id,
                    "s": source_identity,
                },
            )
        result = _lease(value)
        if result is None:
            raise RuntimeError("START_ATTEMPT_INVALID")
        return result

    async def finalize(
        self,
        lease: StartLease,
        process_id: bytes,
        binding_digest: bytes,
        plan_digest: bytes,
        source_identity: bytes,
    ) -> dict[str, Any]:
        async with self._sessions() as session, session.begin():
            value = await session.scalar(
                text("SELECT public_live_api.start_finalize_binding(:r,:p,:g,:d,:q,:s)"),
                {
                    "r": lease.run_id,
                    "p": process_id,
                    "g": lease.lease_generation,
                    "d": binding_digest,
                    "q": plan_digest,
                    "s": source_identity,
                },
            )
        if not isinstance(value, dict):
            raise RuntimeError("START_BINDING_INVALID")
        return value


def _lease(value: object) -> StartLease | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise RuntimeError("START_LEASE_INVALID")
    return StartLease(
        bytes.fromhex(value["run_id"]),
        bytes.fromhex(value["candidate_id"]),
        value["work_run_id"],
        value["phase"],
        value["phase_version"],
        value["lease_generation"],
        datetime.fromisoformat(value["lease_expires_at"]),
        value["candidate"],
    )
