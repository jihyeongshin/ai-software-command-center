from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta

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
