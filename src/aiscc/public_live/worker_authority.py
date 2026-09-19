"""Opaque mediated durable-worker authority and foreground scheduler."""

from __future__ import annotations

import asyncio
import hashlib
import secrets
from collections.abc import Awaitable, Callable
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


@dataclass(frozen=True, slots=True)
class WorkerRef:
    worker_id: bytes
    process_generation: bytes


@dataclass(frozen=True, slots=True)
class ClaimRef:
    run_id: bytes
    claim_id: bytes
    worker_id: bytes
    process_generation: bytes
    fence: int
    claim_version: int
    lease_expires_at: datetime


@dataclass(slots=True)
class ActiveClaim:
    """Supervised live claim reference; renewal failure closes new-use authority."""

    ref: ClaimRef
    renewal_failed: bool = False
    dispatch_started: bool = False

    def current(self) -> ClaimRef:
        if self.renewal_failed:
            raise RuntimeError("WORKER_CLAIM_RENEWAL_LOST")
        return self.ref


class WorkerRepository:
    def __init__(self, sessions: async_sessionmaker[AsyncSession]) -> None:
        self._sessions = sessions

    async def verify_runtime_identity(self) -> None:
        async with self._sessions() as session:
            row = (await session.execute(text("SELECT session_user,current_user"))).one()
        if tuple(row) != ("aiscc_live_worker_login", "aiscc_public_live_execution"):
            raise RuntimeError("PUBLIC_WORKER_RUNTIME_ROLE_DENIED")

    async def register(self, worker: WorkerRef) -> None:
        async with self._sessions() as session, session.begin():
            value = await session.scalar(
                text("SELECT public_live_api.worker_register_instance(:w,:p)"),
                {"w": worker.worker_id, "p": worker.process_generation},
            )
        if not isinstance(value, dict) or value.get("draining") is not False:
            raise RuntimeError("WORKER_REGISTRATION_DENIED")

    async def claim(self, worker: WorkerRef, sequence: int) -> ClaimRef | None:
        request_hash = hashlib.sha256(
            worker.worker_id + worker.process_generation + sequence.to_bytes(8, "big")
        ).digest()
        async with self._sessions() as session, session.begin():
            value = await session.scalar(
                text("SELECT public_live_api.worker_claim_next(:w,:p,:q,:h)"),
                {
                    "w": worker.worker_id,
                    "p": worker.process_generation,
                    "q": sequence,
                    "h": request_hash,
                },
            )
        if not isinstance(value, dict):
            raise RuntimeError("WORKER_CLAIM_INVALID")
        if value.get("kind") == "EMPTY":
            return None
        if value.get("kind") != "CLAIM":
            raise RuntimeError("WORKER_CLAIM_INVALID")
        return ClaimRef(
            bytes.fromhex(value["run_id"]),
            bytes.fromhex(value["claim_id"]),
            worker.worker_id,
            worker.process_generation,
            value["fence"],
            value["claim_version"],
            datetime.fromisoformat(value["lease_expires_at"]),
        )

    async def recover_expired(self, worker: WorkerRef) -> dict[str, int]:
        async with self._sessions() as session, session.begin():
            value = await session.scalar(
                text("SELECT public_live_api.worker_recover_expired(:w,:p)"),
                {"w": worker.worker_id, "p": worker.process_generation},
            )
        if not isinstance(value, dict):
            raise RuntimeError("WORKER_RECOVERY_INVALID")
        return {"recovered": int(value["recovered"]), "quarantined": int(value["quarantined"])}

    async def renew(self, claim: ClaimRef) -> ClaimRef:
        async with self._sessions() as session, session.begin():
            value = await session.scalar(
                text("SELECT public_live_api.worker_renew(:c,:w,:p,:f,:v)"),
                {
                    "c": claim.claim_id,
                    "w": claim.worker_id,
                    "p": claim.process_generation,
                    "f": claim.fence,
                    "v": claim.claim_version,
                },
            )
        if not isinstance(value, dict):
            raise RuntimeError("WORKER_CLAIM_STALE")
        return ClaimRef(
            claim.run_id,
            claim.claim_id,
            claim.worker_id,
            claim.process_generation,
            claim.fence,
            value["claim_version"],
            datetime.fromisoformat(value["lease_expires_at"]),
        )

    async def context(self, claim: ClaimRef) -> dict[str, object]:
        async with self._sessions() as session, session.begin():
            value = await session.scalar(
                text("SELECT public_live_api.worker_claim_context(:c,:w,:p,:f,:v)"),
                {
                    "c": claim.claim_id,
                    "w": claim.worker_id,
                    "p": claim.process_generation,
                    "f": claim.fence,
                    "v": claim.claim_version,
                },
            )
        if not isinstance(value, dict) or value.get("run_id") != claim.run_id.hex():
            raise RuntimeError("WORKER_CLAIM_CONTEXT_DENIED")
        return value

    async def link_and_bind_operation(
        self,
        claim: ClaimRef,
        *,
        ordinal: int,
        operation_id: str,
        role: str,
        retry_of: str | None,
    ) -> None:
        async with self._sessions() as session, session.begin():
            await session.execute(
                text("SELECT public_live_api.execution_link_operation(:r,:o,:i,:s,:q)"),
                {"r": claim.run_id, "o": ordinal, "i": operation_id, "s": role, "q": retry_of},
            )
            value = await session.scalar(
                text("SELECT public_live_api.worker_bind_operation(:c,:w,:p,:f,:v,:i)"),
                {
                    "c": claim.claim_id,
                    "w": claim.worker_id,
                    "p": claim.process_generation,
                    "f": claim.fence,
                    "v": claim.claim_version,
                    "i": operation_id,
                },
            )
        if not isinstance(value, dict) or value.get("operation_id") != operation_id:
            raise RuntimeError("WORKER_OPERATION_BIND_DENIED")

    async def semantic_history(self, run_id: bytes) -> tuple[dict[str, object], ...]:
        async with self._sessions() as session:
            value = await session.scalar(
                text("SELECT public_live_api.execution_semantic_history(:r)"), {"r": run_id}
            )
        if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
            raise RuntimeError("PUBLIC_SEMANTIC_HISTORY_INVALID")
        return tuple(value)

    async def record_validation(
        self,
        operation_id: str,
        *,
        decision: str,
        proof: str,
        defect_ref: str | None,
    ) -> None:
        if len(proof) != 64:
            raise ValueError("SEMANTIC_VALIDATION_PROOF_INVALID")
        async with self._sessions() as session, session.begin():
            value = await session.scalar(
                text("SELECT public_live_api.execution_record_validation(:o,:d,:p,:f)"),
                {
                    "o": operation_id,
                    "d": decision,
                    "p": bytes.fromhex(proof),
                    "f": defect_ref,
                },
            )
        if not isinstance(value, dict) or value.get("operation_id") != operation_id:
            raise RuntimeError("SEMANTIC_VALIDATION_RECORD_DENIED")

    async def release(self, claim: ClaimRef, reason: str) -> None:
        source = hashlib.sha256(
            claim.claim_id + claim.fence.to_bytes(8, "big") + reason.encode()
        ).digest()
        async with self._sessions() as session, session.begin():
            await session.execute(
                text("SELECT public_live_api.worker_release(:c,:w,:p,:f,:v,:r,:s)"),
                {
                    "c": claim.claim_id,
                    "w": claim.worker_id,
                    "p": claim.process_generation,
                    "f": claim.fence,
                    "v": claim.claim_version,
                    "r": reason,
                    "s": source,
                },
            )


class DurableWorkerAuthority:
    """One opaque claim at a time; claims never create P1 or secret authority."""

    def __init__(self, repository: WorkerRepository) -> None:
        self.repository = repository
        self.worker = WorkerRef(secrets.token_bytes(16), secrets.token_bytes(16))
        self.sequence = 0

    async def register(self) -> None:
        await self.repository.register(self.worker)

    async def claim_next_work(self) -> ClaimRef | None:
        recover = getattr(self.repository, "recover_expired", None)
        if recover is not None:
            await recover(self.worker)
        candidate = self.sequence + 1
        claim = await self.repository.claim(self.worker, candidate)
        self.sequence = candidate
        return claim


async def run_worker_loop(
    authority: DurableWorkerAuthority,
    execute: Callable[[ActiveClaim], Awaitable[str]],
    stop: asyncio.Event,
    *,
    renewal_interval_seconds: float = 5.0,
    observe_failure: Callable[[BaseException], None] | None = None,
) -> None:
    await authority.repository.verify_runtime_identity()
    await authority.register()
    empty_delay, db_delay = 1, 1
    while not stop.is_set():
        try:
            claim = await authority.claim_next_work()
            db_delay = 1
            if claim is None:
                await _wait(stop, empty_delay)
                empty_delay = min(empty_delay * 2, 5)
                continue
            empty_delay = 1
            active = ActiveClaim(claim)
            finished = asyncio.Event()
            renewal = asyncio.create_task(
                _renew_claim(
                    authority.repository,
                    active,
                    finished,
                    renewal_interval_seconds,
                )
            )
            try:
                result = await execute(active)
            finally:
                finished.set()
                await renewal
            claim = active.ref
            reason = (
                result
                if result in {"KNOWN_STEP_CLOSED", "EXECUTION_TERMINAL"}
                else "LIVE_UNAVAILABLE"
            )
            await authority.repository.release(claim, reason)
        except Exception as error:
            if observe_failure is not None:
                with suppress(Exception):
                    observe_failure(error)
            await _wait(stop, db_delay)
            db_delay = min(db_delay * 2, 10)


async def _wait(stop: asyncio.Event, seconds: int) -> None:
    with suppress(TimeoutError):
        await asyncio.wait_for(stop.wait(), timeout=seconds)


async def _renew_claim(
    repository: WorkerRepository,
    active: ActiveClaim,
    finished: asyncio.Event,
    interval_seconds: float = 5.0,
) -> None:
    while not finished.is_set():
        with suppress(TimeoutError):
            await asyncio.wait_for(finished.wait(), timeout=interval_seconds)
        if finished.is_set():
            return
        try:
            active.ref = await repository.renew(active.ref)
        except Exception:
            active.renewal_failed = True
            return
