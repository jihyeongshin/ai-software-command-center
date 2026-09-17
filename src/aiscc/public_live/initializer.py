"""Foreground private initializer for the accepted Public Live start saga."""

from __future__ import annotations

import asyncio
import hashlib
import os
import secrets
from collections.abc import Awaitable, Callable, Mapping
from contextlib import suppress
from dataclasses import dataclass, replace

from sqlalchemy.ext.asyncio import AsyncEngine

from aiscc.persistence import create_engine, create_session_factory
from aiscc.public_live.start_authority import PublicLiveStartContextAuthority, StartContract
from aiscc.public_live.start_repository import StartLease, StartRepository


@dataclass(frozen=True, slots=True)
class InitializerSettings:
    database_url: str

    @classmethod
    def from_environment(cls, environ: Mapping[str, str] = os.environ) -> InitializerSettings:
        forbidden = (
            "AISCC_DATABASE_URL",
            "AISCC_OPENAI_API_KEY",
            "OPENAI_API_KEY",
            "AISCC_PUBLIC_LIVE_DATABASE_URL",
        )
        if any(name in environ for name in forbidden):
            raise ValueError("START_INITIALIZER_FORBIDDEN_AUTHORITY_PRESENT")
        value = environ.get("AISCC_PUBLIC_LIVE_START_DATABASE_URL", "")
        if not value:
            raise ValueError("START_INITIALIZER_DATABASE_REQUIRED")
        return cls(value)


@dataclass(frozen=True, slots=True)
class StartOwners:
    """Registered semantic owners; callbacks perform canonical P1 operations."""

    create_ready: Callable[[StartLease], Awaitable[str]]
    admit_start: Callable[[StartLease], Awaitable[None]]
    prepare_attempt: Callable[[StartLease], Awaitable[str]]
    start_workflow: Callable[[StartLease, str], Awaitable[None]]
    start_execution: Callable[[StartLease, str], Awaitable[None]]


@dataclass(slots=True)
class PublicLiveInitializer:
    engine: AsyncEngine
    repository: StartRepository
    contract: StartContract
    process_id: bytes
    owners: StartOwners | None = None

    def check(self) -> None:
        if len(self.process_id) != 16 or self.owners is None:
            raise RuntimeError("START_OWNER_COMPOSITION_UNAVAILABLE")

    def check_configuration(self) -> None:
        if len(self.process_id) != 16 or self.contract.payload.get("runtime_mode") != (
            "PUBLIC_BOUNDED_LIVE"
        ):
            raise RuntimeError("START_INITIALIZER_CONFIGURATION_INVALID")

    async def step(self) -> bool:
        self.check()
        lease = await self.repository.next(self.process_id)
        if lease is None:
            return False
        try:
            assert self.owners is not None
            if lease.phase == "REGISTERED":
                lease = await self._fresh(lease)
                work_run_id = await self.owners.create_ready(lease)
                if work_run_id != lease.work_run_id:
                    raise RuntimeError("START_WORK_IDENTITY_CONFLICT")
                lease = await self.repository.record(
                    lease, self.process_id, "READY_CREATED", _source(lease, "GENESIS")
                )
            if lease.phase == "READY_CREATED":
                lease = await self._fresh(lease)
                await self.owners.admit_start(lease)
                lease = await self._fresh(lease)
                attempt_id = await self.owners.prepare_attempt(lease)
                lease = await self.repository.set_attempt(
                    lease, self.process_id, attempt_id, _source(lease, "ATTEMPT_PREPARED")
                )
            attempt_id = _attempt(lease)
            if lease.phase == "ATTEMPT_PREPARED":
                lease = await self._fresh(lease)
                await self.owners.start_workflow(lease, attempt_id)
                lease = await self.repository.record(
                    lease, self.process_id, "WORKFLOW_RUNNING", _source(lease, "WORKFLOW_RUNNING")
                )
            if lease.phase == "WORKFLOW_RUNNING":
                lease = await self._fresh(lease)
                await self.owners.start_execution(lease, attempt_id)
                lease = await self.repository.record(
                    lease,
                    self.process_id,
                    "EXECUTION_RUNNING",
                    _source(lease, "EXECUTION_RUNNING"),
                )
            if lease.phase == "EXECUTION_RUNNING":
                lease = await self._fresh(lease)
                binding = hashlib.sha256(
                    lease.run_id + lease.work_run_id.encode() + attempt_id.encode()
                ).digest()
                plan = hashlib.sha256(binding + self.contract.digest.encode()).digest()
                await self.repository.finalize(
                    lease, self.process_id, binding, plan, _source(lease, "BOUND")
                )
            return True
        except Exception:
            # If the canonical owner committed and the ACK was lost, halting would
            # lie.  Leave the lease to expire; the next owner rehydrates P1 truth.
            raise

    async def _fresh(self, lease: StartLease) -> StartLease:
        context = await self.repository.context(lease, self.process_id)
        authority_now = context.get("authority_now")
        control_gate = context.get("control_gate")
        if not isinstance(authority_now, str) or control_gate != lease.candidate.get(
            "gate_version"
        ):
            raise RuntimeError("START_FRESHNESS_DENIED")
        return replace(
            lease,
            candidate={**lease.candidate, "authority_now": authority_now},
        )

    async def run(self, stop: asyncio.Event) -> None:
        await self.repository.verify_runtime_identity()
        empty_delay = 1
        db_delay = 1
        while not stop.is_set():
            try:
                worked = await self.step()
                db_delay = 1
                empty_delay = 1 if worked else min(empty_delay * 2, 5)
                if not worked:
                    await _wait(stop, empty_delay)
            except Exception:
                await _wait(stop, db_delay)
                db_delay = min(db_delay * 2, 10)

    async def close(self) -> None:
        await self.engine.dispose()


def create_initializer(
    environ: Mapping[str, str] = os.environ, *, owners: StartOwners | None = None
) -> PublicLiveInitializer:
    settings = InitializerSettings.from_environment(environ)
    engine = create_engine(settings.database_url, role="aiscc_public_live_initializer")
    sessions = create_session_factory(engine)
    repository = StartRepository(sessions)
    contract = StartContract.load()
    if owners is None:
        from aiscc.persistence.repository import PostgresTransitionRepository
        from aiscc.providers.authority import ExecutionReferenceAuthority
        from aiscc.public_live.start_owners import CanonicalStartOwners
        from aiscc.security.policy import SecurityPolicy, default_profiles
        from aiscc.workflow.evaluator import TransitionEvaluator
        from aiscc.workflow.guards import P1_4GuardAuthority
        from aiscc.workflow.kernel import WorkflowKernel

        guard_authority = P1_4GuardAuthority()
        execution_refs = ExecutionReferenceAuthority()
        context_authority = PublicLiveStartContextAuthority(
            contract, principal="aiscc-public-live-initializer"
        )
        security = SecurityPolicy(default_profiles(), public_context_policy=context_authority)
        p1 = PostgresTransitionRepository(sessions, TransitionEvaluator(guard_authority))
        owners = CanonicalStartOwners(
            contract=contract,
            kernel=WorkflowKernel(p1),
            repository=p1,
            guard_authority=guard_authority,
            execution_refs=execution_refs,
            context_authority=context_authority,
            security_policy=security,
        ).ports()
    return PublicLiveInitializer(engine, repository, contract, secrets.token_bytes(16), owners)


def _attempt(lease: StartLease) -> str:
    value = lease.candidate.get("execution_attempt_id")
    if not isinstance(value, str) or not value:
        # The mediated context may omit it from immutable candidate data.  The
        # accepted deterministic identity is safe to reconstruct.
        value = (
            "pl-start-attempt-"
            + hashlib.sha256(
                lease.candidate_id + lease.work_run_id.encode() + b"\0READY\01\0ordinal-1"
            ).hexdigest()
        )
    return value[:128]


def _source(lease: StartLease, phase: str) -> bytes:
    return hashlib.sha256(
        lease.candidate_id + phase.encode() + lease.phase_version.to_bytes(8, "big")
    ).digest()


async def _wait(stop: asyncio.Event, seconds: int) -> None:
    with suppress(TimeoutError):
        await asyncio.wait_for(stop.wait(), timeout=seconds)
