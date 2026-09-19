from __future__ import annotations

import asyncio
from dataclasses import dataclass

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from aiscc.persistence import create_session_factory
from aiscc.public_live.initializer import create_initializer
from aiscc.public_live.start_authority import StartContract
from aiscc.public_live.worker_authority import DurableWorkerAuthority, WorkerRepository
from tests.integration.public_live.test_service import harness

pytestmark = pytest.mark.postgres


def test_rejected_claim_does_not_skip_sequence_after_external_release(l2_url: str) -> None:
    async def check() -> None:
        async with harness(l2_url) as h:
            h.admission.start_contract = StartContract.load()
            run_id = (await h.admit()).run_id
            initializer = create_initializer({"AISCC_PUBLIC_LIVE_START_DATABASE_URL": h.url})
            try:
                assert await initializer.step()
            finally:
                await initializer.close()

            repository = WorkerRepository(create_session_factory(h.admin))
            authority = DurableWorkerAuthority(repository)
            await authority.register()
            claim = await authority.claim_next_work()
            assert claim is not None and claim.run_id == run_id
            assert authority.sequence == 1

            for _ in range(3):
                with pytest.raises(DBAPIError, match="CLAIM_SEQUENCE_DENIED"):
                    await authority.claim_next_work()
                assert authority.sequence == 1

            await repository.release(claim, "LIVE_UNAVAILABLE")
            recovered = await authority.claim_next_work()
            assert recovered is not None and recovered.run_id == run_id
            assert recovered.fence == claim.fence + 1
            assert authority.sequence == 2

            async with h.admin.connect() as connection:
                instance = (
                    await connection.execute(
                        text(
                            "SELECT last_acquire_seq,last_result_kind "
                            "FROM public_worker_instance WHERE worker_id=:worker"
                        ),
                        {"worker": authority.worker.worker_id},
                    )
                ).one()
                assert tuple(instance) == (2, "CLAIM")
                assert (
                    await connection.scalar(text("SELECT count(*) FROM execution_operations")) == 0
                )
                assert (
                    await connection.scalar(
                        text("SELECT count(*) FROM public_worker_claim_event WHERE kind='ACQUIRED'")
                    )
                    == 2
                )
            await repository.release(recovered, "LIVE_UNAVAILABLE")

    asyncio.run(check())


def test_lost_response_replays_same_sequence_without_duplicate_claim(l2_url: str) -> None:
    @dataclass
    class LostResponseRepository:
        repository: WorkerRepository
        lose_once: bool = True

        async def register(self, worker):
            await self.repository.register(worker)

        async def recover_expired(self, worker):
            return await self.repository.recover_expired(worker)

        async def claim(self, worker, sequence):
            result = await self.repository.claim(worker, sequence)
            if self.lose_once:
                self.lose_once = False
                raise RuntimeError("SIMULATED_RESPONSE_LOSS_AFTER_COMMIT")
            return result

    async def check() -> None:
        async with harness(l2_url) as h:
            h.admission.start_contract = StartContract.load()
            run_id = (await h.admit()).run_id
            initializer = create_initializer({"AISCC_PUBLIC_LIVE_START_DATABASE_URL": h.url})
            try:
                assert await initializer.step()
            finally:
                await initializer.close()

            base = WorkerRepository(create_session_factory(h.admin))
            authority = DurableWorkerAuthority(LostResponseRepository(base))  # type: ignore[arg-type]
            await authority.register()
            with pytest.raises(RuntimeError, match="SIMULATED_RESPONSE_LOSS_AFTER_COMMIT"):
                await authority.claim_next_work()
            assert authority.sequence == 0

            claim = await authority.claim_next_work()
            assert claim is not None and claim.run_id == run_id
            assert authority.sequence == 1
            async with h.admin.connect() as connection:
                row = (
                    await connection.execute(
                        text(
                            "SELECT count(*),min(fence),max(fence),min(acquisition_seq),"
                            "max(acquisition_seq) FROM public_worker_claim WHERE run_id=:run"
                        ),
                        {"run": run_id},
                    )
                ).one()
                assert tuple(row) == (1, 1, 1, 1, 1)
                assert (
                    await connection.scalar(
                        text(
                            "SELECT count(*) FROM public_worker_claim_event "
                            "WHERE run_id=:run AND kind='ACQUIRED'"
                        ),
                        {"run": run_id},
                    )
                    == 1
                )
                assert (
                    await connection.scalar(text("SELECT count(*) FROM execution_operations")) == 0
                )
            await base.release(claim, "LIVE_UNAVAILABLE")

    asyncio.run(check())


def test_empty_acquisitions_and_fresh_worker_sequences_are_independent(l2_url: str) -> None:
    async def check() -> None:
        async with harness(l2_url) as h:
            repository = WorkerRepository(create_session_factory(h.admin))
            first = DurableWorkerAuthority(repository)
            second = DurableWorkerAuthority(repository)
            await first.register()
            await second.register()

            for expected in range(1, 4):
                assert await first.claim_next_work() is None
                assert first.sequence == expected
            assert await second.claim_next_work() is None
            assert second.sequence == 1

            async with h.admin.connect() as connection:
                rows = (
                    await connection.execute(
                        text(
                            "SELECT worker_id,last_acquire_seq,last_result_kind "
                            "FROM public_worker_instance "
                            "WHERE worker_id IN (:first,:second) ORDER BY worker_id"
                        ),
                        {"first": first.worker.worker_id, "second": second.worker.worker_id},
                    )
                ).all()
                by_worker = {
                    bytes(row.worker_id): (row.last_acquire_seq, row.last_result_kind)
                    for row in rows
                }
                assert by_worker[first.worker.worker_id] == (3, "EMPTY")
                assert by_worker[second.worker.worker_id] == (1, "EMPTY")
                assert (
                    await connection.scalar(text("SELECT count(*) FROM public_worker_claim")) == 0
                )
                assert (
                    await connection.scalar(text("SELECT count(*) FROM execution_operations")) == 0
                )

    asyncio.run(check())
