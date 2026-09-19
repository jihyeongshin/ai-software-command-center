"""Deterministic PostgreSQL barriers for mutable worker claim versions."""

import asyncio
import os
from collections.abc import Callable
from types import MappingProxyType

import pytest
from sqlalchemy import text

from aiscc.persistence.repository import PostgresExecutionRepository
from aiscc.providers.models import ExecutionOperationOutcome, ProviderCall, ProviderResult
from aiscc.public_live.initializer import create_initializer
from aiscc.public_live.start_authority import StartContract
from aiscc.public_live.worker import create_worker
from aiscc.public_live.worker_authority import ActiveClaim, WorkerRepository
from tests.integration.public_live.test_service import harness

pytestmark = pytest.mark.postgres


class _CompletedProvider:
    def __init__(self, guard_locked: Callable[[], bool]) -> None:
        self.invocation_count = 0
        self._guard_locked = guard_locked

    def call(self, call: ProviderCall, *, secret: str) -> ProviderResult:
        assert secret == "synthetic-hosted-proof-only"
        assert not self._guard_locked(), "claim-version guard crossed provider execution"
        self.invocation_count += 1
        item = {
            "type": "message",
            "role": "assistant",
            "content": [{"type": "output_text", "text": "complete"}],
        }
        return ProviderResult(
            call.operation_id,
            "completed",
            ExecutionOperationOutcome.PROVIDER_COMPLETED,
            "claim-version-guard-proof",
            (item,),
            "complete",
            None,
            MappingProxyType({"input_tokens": 1, "output_tokens": 1}),
            None,
            "a" * 64,
        )


@pytest.mark.parametrize("barrier", ["context", "bind", "pin"])
def test_renewal_waits_for_exact_version_authority_window(l2_url, monkeypatch, barrier) -> None:
    async def check() -> None:
        async with harness(l2_url) as h:
            h.admission.start_contract = StartContract.load()
            run = (await h.admit()).run_id
            initializer = create_initializer({"AISCC_PUBLIC_LIVE_START_DATABASE_URL": h.url})
            worker = create_worker(
                {"AISCC_PUBLIC_LIVE_DATABASE_URL": h.url},
                semantic_validator=lambda _role, _result: MappingProxyType(
                    {"decision": "COMPLETE", "proof": "b" * 64, "defect_ref": None}
                ),
            )
            entered = asyncio.Event()
            resume = asyncio.Event()

            async def pause() -> None:
                entered.set()
                await resume.wait()

            if barrier == "context":
                original = WorkerRepository.context

                async def paused_context(self, claim):
                    await pause()
                    return await original(self, claim)

                monkeypatch.setattr(WorkerRepository, "context", paused_context)
            elif barrier == "bind":
                original = WorkerRepository.link_and_bind_operation

                async def paused_bind(self, claim, **kwargs):
                    await pause()
                    return await original(self, claim, **kwargs)

                monkeypatch.setattr(WorkerRepository, "link_and_bind_operation", paused_bind)
            else:
                original = PostgresExecutionRepository.start_dispatch_if_fresh

                async def paused_pin(self, *args, **kwargs):
                    await pause()
                    return await original(self, *args, **kwargs)

                monkeypatch.setattr(
                    PostgresExecutionRepository,
                    "start_dispatch_if_fresh",
                    paused_pin,
                )

            previous = os.environ.get("AISCC_OPENAI_API_KEY")
            try:
                assert await initializer.step()
                await worker.authority.register()
                claim = await worker.authority.claim_next_work()
                assert claim is not None
                active = ActiveClaim(claim)
                worker.adapter = _CompletedProvider(active._version_guard.locked)
                os.environ["AISCC_OPENAI_API_KEY"] = "synthetic-hosted-proof-only"

                execution = asyncio.create_task(worker.execute_claim(active))
                await asyncio.wait_for(entered.wait(), timeout=5)
                initial_version = active.current().claim_version
                renewal = asyncio.create_task(active.renew(worker.authority.repository))
                await asyncio.sleep(0)
                assert not renewal.done()

                resume.set()
                assert await asyncio.wait_for(execution, timeout=10) == "EXECUTION_TERMINAL"
                await asyncio.wait_for(renewal, timeout=5)
                assert active.current().claim_version == initial_version + 1
                assert worker.adapter.invocation_count == 1

                async with h.admin.connect() as connection:
                    counts = (
                        await connection.execute(
                            text(
                                "SELECT "
                                "(SELECT count(*) FROM public_provider_operation_link "
                                "WHERE run_id=:r),"
                                "(SELECT count(*) FROM operation_events e "
                                "JOIN execution_operations o USING(operation_id) "
                                "JOIN public_provider_execution x "
                                "ON x.execution_attempt_id=o.execution_attempt_id "
                                "WHERE x.run_id=:r AND "
                                "e.target_phase='DISPATCH_STARTED')"
                            ),
                            {"r": run},
                        )
                    ).one()
                assert counts == (1, 1)
            finally:
                resume.set()
                if previous is None:
                    os.environ.pop("AISCC_OPENAI_API_KEY", None)
                else:
                    os.environ["AISCC_OPENAI_API_KEY"] = previous
                await initializer.close()
                await worker.close()

    asyncio.run(check())
