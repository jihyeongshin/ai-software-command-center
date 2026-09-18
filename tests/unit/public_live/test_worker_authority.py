from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

from aiscc.public_live.worker import (
    _execute_production_claim,
    classify_worker_failure,
    stockroom_runtime_observation,
)
from aiscc.public_live.worker_authority import (
    ActiveClaim,
    ClaimRef,
    DurableWorkerAuthority,
    WorkerRef,
    _renew_claim,
)


class Repository:
    def __init__(self):
        self.registered = False
        self.sequence = []

    async def register(self, worker: WorkerRef) -> None:
        self.registered = len(worker.worker_id) == len(worker.process_generation) == 16

    async def claim(self, worker: WorkerRef, sequence: int):
        self.sequence.append(sequence)
        if sequence == 1:
            return None
        return ClaimRef(
            b"r" * 16,
            b"c" * 16,
            worker.worker_id,
            worker.process_generation,
            1,
            1,
            datetime.now(UTC) + timedelta(seconds=15),
        )


def test_authority_generates_process_identity_and_monotonic_acquisition_sequence() -> None:
    repository = Repository()
    authority = DurableWorkerAuthority(repository)  # type: ignore[arg-type]

    async def check():
        await authority.register()
        assert await authority.claim_next_work() is None
        assert (await authority.claim_next_work()).fence == 1  # type: ignore[union-attr]

    asyncio.run(check())
    assert repository.registered and repository.sequence == [1, 2]


def test_supervised_claim_renews_and_lost_renewal_closes_new_use() -> None:
    initial = ClaimRef(
        b"r" * 16,
        b"c" * 16,
        b"w" * 16,
        b"p" * 16,
        1,
        1,
        datetime.now(UTC) + timedelta(seconds=15),
    )

    class Renewals:
        calls = 0

        async def renew(self, claim):
            self.calls += 1
            if self.calls == 2:
                raise RuntimeError("lost")
            return ClaimRef(
                claim.run_id,
                claim.claim_id,
                claim.worker_id,
                claim.process_generation,
                claim.fence,
                claim.claim_version + 1,
                datetime.now(UTC) + timedelta(seconds=15),
            )

    async def check():
        repository = Renewals()
        active = ActiveClaim(initial)
        finished = asyncio.Event()
        await _renew_claim(repository, active, finished, 0.001)  # type: ignore[arg-type]
        assert repository.calls == 2 and active.renewal_failed
        assert active.ref.claim_version == 2
        try:
            active.current()
        except RuntimeError as exc:
            assert str(exc) == "WORKER_CLAIM_RENEWAL_LOST"
        else:
            raise AssertionError("lost renewal retained side-effect authority")

    asyncio.run(check())


def test_worker_loop_reports_only_allowlisted_failure_classification() -> None:
    class FailingRepository(Repository):
        async def verify_runtime_identity(self) -> None:
            return None

        async def recover_expired(self, _worker: WorkerRef) -> dict[str, int]:
            return {"recovered": 0, "quarantined": 0}

    async def check() -> None:
        repository = FailingRepository()
        authority = DurableWorkerAuthority(repository)  # type: ignore[arg-type]
        stop = asyncio.Event()
        observations = []

        async def execute(_active: ActiveClaim) -> str:
            stop.set()
            raise RuntimeError("secret-bearing-error-must-not-escape")

        from aiscc.public_live.worker_authority import run_worker_loop

        await run_worker_loop(
            authority,
            execute,
            stop,
            renewal_interval_seconds=0.001,
            observe_failure=lambda error: observations.append(classify_worker_failure(error)),
        )
        assert len(observations) == 1
        assert observations[0].stage == "CLAIM_EXECUTION"
        assert observations[0].code == "PUBLIC_WORKER_FAILURE_UNCLASSIFIED"
        assert len(observations[0].digest) == 64
        assert "secret" not in repr(observations[0])

    asyncio.run(check())


def test_fixed_runtime_and_generic_failure_are_secret_safe_codes() -> None:
    prerequisite = stockroom_runtime_observation()
    failure = classify_worker_failure(RuntimeError("PUBLIC_LIVE_STOCKROOM_DOCKER_REQUIRED"))

    assert prerequisite.stage == "RUNTIME_PREREQUISITE"
    assert prerequisite.code == "PUBLIC_LIVE_FIXED_STOCKROOM_READY"
    assert failure.stage == "CLAIM_EXECUTION"
    assert failure.code == "PUBLIC_WORKER_FAILURE_UNCLASSIFIED"
    assert prerequisite.digest != failure.digest


def test_production_claim_composes_without_docker_prerequisite(monkeypatch) -> None:
    claim = ClaimRef(
        b"r" * 16,
        b"c" * 16,
        b"w" * 16,
        b"p" * 16,
        1,
        1,
        datetime.now(UTC) + timedelta(seconds=15),
    )

    class ContextRepository:
        async def context(self, _claim: ClaimRef) -> dict[str, object]:
            return {
                "state_version": 2,
                "execution_version": 1,
                "work_run_id": "work-run-fixed",
                "execution_attempt_id": "attempt-fixed",
            }

    constructed = 0

    class ForbiddenExecutionService:
        def __init__(self, **_kwargs) -> None:
            nonlocal constructed
            constructed += 1

        async def execute(self, **_kwargs):
            return SimpleNamespace(status="EXECUTION_COMPLETED")

    worker = SimpleNamespace(
        authority=SimpleNamespace(repository=ContextRepository()),
        adapter=SimpleNamespace(invocation_count=0),
        semantic_validator=None,
        last_stockroom_dispatcher=None,
    )

    def forbidden(*_args, **_kwargs):
        raise AssertionError("Docker lookup was reached")

    monkeypatch.setattr("shutil.which", forbidden)
    monkeypatch.setattr("aiscc.public_live.worker.AgentExecutionService", ForbiddenExecutionService)

    async def check() -> None:
        assert (
            await _execute_production_claim(worker, None, ActiveClaim(claim))  # type: ignore[arg-type]
            == "EXECUTION_TERMINAL"
        )

    asyncio.run(check())
    assert constructed == 1
    assert worker.adapter.invocation_count == 0
    assert worker.last_stockroom_dispatcher is not None
    assert worker.last_stockroom_dispatcher.invocation_count == 0
