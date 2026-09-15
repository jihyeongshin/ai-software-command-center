"""L1 transaction primitives; callers supply separately admitted authority.

No HTTP admission service, provider transport, activation, or owner workflow
mutation lives here. Use a separate public database login with membership only
in aiscc_public_live_runtime. Never pass the owner database credential.
"""

from __future__ import annotations

import json
import secrets
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class ObservationKind(StrEnum):
    KNOWN_SUCCESS = "KNOWN_SUCCESS"
    KNOWN_FAILURE = "KNOWN_FAILURE"
    UNKNOWN = "UNKNOWN"
    USAGE = "USAGE"
    ABOVE_BOUND = "ABOVE_BOUND"
    CLOSURE = "CLOSURE"
    LATE_USAGE = "LATE_USAGE"


class OutboxState(StrEnum):
    PENDING = "PENDING"
    BOUND = "BOUND"
    CLOSED = "CLOSED"


@dataclass(frozen=True)
class IdempotencyBinding:
    run_id: bytes
    bucket_hash: bytes
    payload_hash: bytes
    admitted_at: datetime
    replay_until: datetime
    retention_until: datetime


@dataclass(frozen=True)
class OutboxIdentity:
    run_id: bytes
    state: OutboxState
    generation: int
    owner_binding: str | None
    fenced_at: datetime | None


@dataclass(frozen=True)
class RunIdentity:
    run_id: bytes
    read_capability: bytes

    @classmethod
    def generate(cls) -> RunIdentity:
        return cls(secrets.token_bytes(16), secrets.token_bytes(32))


@dataclass(frozen=True)
class PersistRun:
    run_id: bytes
    campaign_id: str
    bucket_hash: bytes
    key_hash: bytes
    read_hash: bytes
    payload_digest: bytes
    slot_id: int


@dataclass(frozen=True)
class Observation:
    observation_id: bytes
    run_id: bytes
    source_identity: bytes
    classification: ObservationKind
    evidence_digest: bytes
    ordinal: int | None = None
    cost_micro: int | None = None


class PublicLiveTransaction:
    """Valid only within PublicLiveRepository.transaction().

    Every SQL writer obtains the singleton control lock. The repository also
    acquires it on entry, before DB-clock observation. Return values are not
    dispatch authority until the outer context has committed successfully.
    """

    def __init__(self, session: AsyncSession, now: datetime) -> None:
        self._session = session
        self.now = now
        self._open = True

    async def _call(self, sql: str, params: dict[str, Any]) -> Any:
        if not self._open:
            raise RuntimeError("PUBLIC_TRANSACTION_CLOSED")
        return await self._session.scalar(text(sql), params)

    async def read_idempotency(self, campaign: str, key_hash: bytes) -> IdempotencyBinding | None:
        result = await self._call(
            "SELECT public_live_api.read_key(:c,:k)", {"c": campaign, "k": key_hash}
        )
        if result is not None and not isinstance(result, dict):
            raise RuntimeError("PUBLIC_IDEMPOTENCY_PROJECTION_INVALID")
        if result is None:
            return None
        return IdempotencyBinding(
            bytes.fromhex(result["run_id"][2:]),
            bytes.fromhex(result["bucket_hash"][2:]),
            bytes.fromhex(result["payload_hash"][2:]),
            datetime.fromisoformat(result["admitted_at"]),
            datetime.fromisoformat(result["replay_until"]),
            datetime.fromisoformat(result["retention_until"]),
        )

    async def admission_context(self, campaign: str, bucket: bytes) -> dict[str, Any] | None:
        result = await self._call(
            "SELECT public_live_api.admission_context(:c,:b)",
            {"c": campaign, "b": bucket},
        )
        if result is not None and not isinstance(result, dict):
            raise RuntimeError("PUBLIC_ADMISSION_CONTEXT_INVALID")
        return result

    async def admit_checked(
        self, value: PersistRun, *, policy_digest: bytes, content_digest: bytes, hmac_version: str
    ) -> dict[str, Any]:
        """DB-mediated rate/pin/admission check; return only after outer commit."""
        result = await self._call(
            "SELECT public_live_api.admit_checked(CAST(:p AS jsonb))",
            {
                "p": json.dumps(
                    {
                        "run_id": value.run_id.hex(),
                        "campaign_id": value.campaign_id,
                        "bucket_hash": value.bucket_hash.hex(),
                        "key_hash": value.key_hash.hex(),
                        "read_hash": value.read_hash.hex(),
                        "payload_digest": value.payload_digest.hex(),
                        "policy_digest": policy_digest.hex(),
                        "content_digest": content_digest.hex(),
                        "hmac_version": hmac_version,
                    }
                )
            },
        )
        if not isinstance(result, dict):
            raise RuntimeError("PUBLIC_ADMISSION_RESULT_INVALID")
        return result

    async def run_context(self, run_id: bytes) -> dict[str, Any]:
        result = await self._call("SELECT public_live_api.run_context(:r)", {"r": run_id})
        if not isinstance(result, dict):
            raise RuntimeError("PUBLIC_RUN_CONTEXT_INVALID")
        return result

    async def project_run(
        self, run_id: bytes, expected_version: int, target: str, proof: bytes
    ) -> int:
        result = await self._call(
            "SELECT public_live_api.project_run(:r,:v,:t,:p)",
            {"r": run_id, "v": expected_version, "t": target, "p": proof},
        )
        if type(result) is not int:
            raise RuntimeError("PUBLIC_PROJECTION_VERSION_INVALID")
        return result

    async def mark_checked(
        self, run_id: bytes, generation: int, ordinal: int, max_cost: int, owner_version: int
    ) -> None:
        if type(max_cost) is not int or type(owner_version) is not int:
            raise TypeError("exact integer bound and owner version required")
        await self._call(
            "SELECT public_live_api.mark_checked(:r,:g,:n,:b,:v)",
            {"r": run_id, "g": generation, "n": ordinal, "b": max_cost, "v": owner_version},
        )

    async def lock_context(self, campaign: str, days: tuple[date, ...], bucket: bytes) -> None:
        await self._call(
            "SELECT public_live_api.lock_context(:c,:d,:b)",
            {"c": campaign, "d": sorted(set(days)), "b": bucket},
        )

    async def persist_run(self, value: PersistRun) -> None:
        """Atomic identity/reservation/slot write; no HTTP/rate admission decision."""
        await self._call(
            "SELECT public_live_api.persist_run(CAST(:p AS jsonb))",
            {
                "p": json.dumps(
                    {
                        "run_id": value.run_id.hex(),
                        "campaign_id": value.campaign_id,
                        "bucket_hash": value.bucket_hash.hex(),
                        "key_hash": value.key_hash.hex(),
                        "read_hash": value.read_hash.hex(),
                        "payload_digest": value.payload_digest.hex(),
                        "slot_id": value.slot_id,
                    }
                )
            },
        )

    async def heartbeat(self, run_id: bytes, generation: int) -> None:
        await self._call(
            "SELECT public_live_api.slot_update(:r,:g,false)", {"r": run_id, "g": generation}
        )

    async def quarantine(self, run_id: bytes, generation: int) -> None:
        await self._call(
            "SELECT public_live_api.slot_update(:r,:g,true)", {"r": run_id, "g": generation}
        )

    async def read_outbox(self, run_id: bytes) -> OutboxIdentity | None:
        result = await self._call("SELECT public_live_api.read_outbox(:r)", {"r": run_id})
        if result is not None and not isinstance(result, dict):
            raise RuntimeError("PUBLIC_OUTBOX_PROJECTION_INVALID")
        if result is None:
            return None
        return OutboxIdentity(
            bytes.fromhex(result["run_id"][2:]),
            OutboxState(result["state"]),
            result["generation"],
            result["owner_binding"],
            datetime.fromisoformat(result["fenced_at"]) if result["fenced_at"] else None,
        )

    async def fence(self, run_id: bytes, generation: int) -> None:
        """Close future markers; this does not prove an already authorized send ended."""
        await self._call("SELECT public_live_api.fence_run(:r,:g)", {"r": run_id, "g": generation})

    async def mark_dispatch(
        self, run_id: bytes, generation: int, ordinal: int, max_cost: int
    ) -> None:
        if type(max_cost) is not int:
            raise TypeError("micro-USD must be an integer")
        await self._call(
            "SELECT public_live_api.mark_dispatch(:r,:g,:n,:b)",
            {"r": run_id, "g": generation, "n": ordinal, "b": max_cost},
        )

    async def observe(self, value: Observation) -> None:
        if value.cost_micro is not None and type(value.cost_micro) is not int:
            raise TypeError("micro-USD must be an integer")
        await self._call(
            "SELECT public_live_api.observe(CAST(:p AS jsonb))",
            {
                "p": json.dumps(
                    {
                        "observation_id": value.observation_id.hex(),
                        "run_id": value.run_id.hex(),
                        "ordinal": value.ordinal,
                        "source_identity": value.source_identity.hex(),
                        "classification": value.classification.value,
                        "evidence_digest": value.evidence_digest.hex(),
                        "cost_micro": value.cost_micro,
                    }
                )
            },
        )

    async def bind_owner(self, run_id: bytes, generation: int, owner_id: str) -> None:
        """Requires the separate trusted reconciler role and actual owner lineage."""
        await self._call(
            "SELECT public_live_api.bind_owner(:r,:g,:o)",
            {"r": run_id, "g": generation, "o": owner_id},
        )

    async def record_outcome(
        self,
        run_id: bytes,
        ordinal: int,
        kind: ObservationKind,
        cost: int,
        proof: bytes,
        identity: bytes,
    ) -> None:
        """Persist an already verified outcome; no provider call or verification."""
        if type(cost) is not int:
            raise TypeError("micro-USD must be an integer")
        await self._call(
            "SELECT public_live_api.record_outcome(:r,:n,:k,:c,:p,:i,:o)",
            {
                "r": run_id,
                "n": ordinal,
                "k": kind.value,
                "c": cost,
                "p": proof,
                "i": identity,
                "o": secrets.token_bytes(16),
            },
        )

    async def admit_closure(
        self, run_id: bytes, fenced_generation: int, cost: int, proof: bytes, identity: bytes
    ) -> None:
        """Trusted reconciler only, AFTER real closure proof and DB fencing.

        External termination evidence is a later-layer responsibility. Runtime
        role cannot turn an arbitrary observation into settlement authority.
        """
        if type(cost) is not int:
            raise TypeError("micro-USD must be an integer")
        await self._call(
            "SELECT public_live_api.admit_closure(:r,:g,:c,:p,:i,:o)",
            {
                "r": run_id,
                "g": fenced_generation,
                "c": cost,
                "p": proof,
                "i": identity,
                "o": secrets.token_bytes(16),
            },
        )

    async def settle(self, run_id: bytes, cost: int, closure_digest: bytes) -> bool:
        if type(cost) is not int:
            raise TypeError("micro-USD must be an integer")
        return bool(
            await self._call(
                "SELECT public_live_api.settle(:r,:c,:p)",
                {"r": run_id, "c": cost, "p": closure_digest},
            )
        )


class PublicLiveRepository:
    def __init__(self, sessions: async_sessionmaker[AsyncSession]) -> None:
        self._sessions = sessions

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[PublicLiveTransaction]:
        async with self._sessions() as session, session.begin():
            now = await session.scalar(text("SELECT public_live_api.clock_lock()"))
            if not isinstance(now, datetime):
                raise RuntimeError("PUBLIC_CLOCK_UNAVAILABLE")
            tx = PublicLiveTransaction(session, now)
            try:
                yield tx
            finally:
                tx._open = False
