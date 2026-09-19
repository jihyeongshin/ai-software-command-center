"""Known-outcome P1-5 failure settlement through the exact reconciler boundary."""

import asyncio
import os
from datetime import UTC, datetime, timedelta
from types import MappingProxyType

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from aiscc.persistence.repository import PostgresExecutionRepository
from aiscc.providers.models import (
    ExecutionOperationOutcome,
    ProviderCall,
    ProviderResult,
    ToolCallCandidate,
)
from aiscc.public_live.identity import AdmissionDenied
from aiscc.public_live.initializer import create_initializer
from aiscc.public_live.luna_profile import (
    conservative_request_liability_micro,
    hosted_luna_profile,
)
from aiscc.public_live.service import KnownFailedExecutionReconciliationService
from aiscc.public_live.start_authority import StartContract
from aiscc.public_live.worker import create_worker
from aiscc.public_live.worker_authority import ActiveClaim
from tests.integration.public_live.test_service import harness

pytestmark = pytest.mark.postgres


class _ToolThenCompleteProvider:
    def __init__(self) -> None:
        self.invocation_count = 0

    def call(self, call: ProviderCall, *, secret: str) -> ProviderResult:
        assert secret == "synthetic-hosted-proof-only"
        self.invocation_count += 1
        if self.invocation_count == 1:
            item = {
                "type": "function_call",
                "name": "stockroom_summary",
                "arguments": "{}",
                "call_id": "call-stockroom",
            }
            return ProviderResult(
                call.operation_id,
                "completed",
                ExecutionOperationOutcome.PROVIDER_COMPLETED,
                "provider-tool-request",
                (item,),
                None,
                ToolCallCandidate("stockroom_summary", "{}", "call-stockroom"),
                MappingProxyType({"input_tokens": 1, "output_tokens": 1}),
                None,
                "a" * 64,
            )
        item = {
            "type": "message",
            "role": "assistant",
            "content": [{"type": "output_text", "text": "complete"}],
        }
        return ProviderResult(
            call.operation_id,
            "completed",
            ExecutionOperationOutcome.PROVIDER_COMPLETED,
            "provider-final",
            (item,),
            "complete",
            None,
            MappingProxyType({"input_tokens": 1, "output_tokens": 1}),
            None,
            "b" * 64,
        )


async def _prepare_known_failed_target(h, monkeypatch) -> bytes:
    h.admission.start_contract = StartContract.load()
    run = (await h.admit()).run_id
    initializer = create_initializer({"AISCC_PUBLIC_LIVE_START_DATABASE_URL": h.url})
    worker = create_worker({"AISCC_PUBLIC_LIVE_DATABASE_URL": h.url})
    adapter = _ToolThenCompleteProvider()
    worker.adapter = adapter
    original = PostgresExecutionRepository.start_dispatch_if_fresh
    provider_dispatches = 0
    active: ActiveClaim | None = None

    async def historical_race(self, *args, **kwargs):
        nonlocal provider_dispatches
        claim_ref = kwargs.get("claim_ref")
        if claim_ref is not None:
            provider_dispatches += 1
            if provider_dispatches == 2:
                assert active is not None
                active.ref = await worker.authority.repository.renew(claim_ref)
        return await original(self, *args, **kwargs)

    monkeypatch.setattr(
        PostgresExecutionRepository,
        "start_dispatch_if_fresh",
        historical_race,
    )
    previous = os.environ.get("AISCC_OPENAI_API_KEY")
    try:
        assert await initializer.step()
        await worker.authority.register()
        claim = await worker.authority.claim_next_work()
        assert claim is not None
        active = ActiveClaim(claim)
        os.environ["AISCC_OPENAI_API_KEY"] = "synthetic-hosted-proof-only"
        with pytest.raises(DBAPIError):
            await worker.execute_claim(active)
        assert adapter.invocation_count == 1
        await worker.authority.repository.release(active.current(), "LIVE_UNAVAILABLE")

        recovered_claim = await worker.authority.claim_next_work()
        assert recovered_claim is not None
        recovered = ActiveClaim(recovered_claim)
        assert await worker.execute_claim(recovered) == "EXECUTION_TERMINAL"
        await worker.authority.repository.release(recovered.current(), "EXECUTION_TERMINAL")
        await h.clock((datetime.now(UTC) + timedelta(minutes=3)).isoformat())
        await h.sql("UPDATE public_control SET enabled=false")
    finally:
        if previous is None:
            os.environ.pop("AISCC_OPENAI_API_KEY", None)
        else:
            os.environ["AISCC_OPENAI_API_KEY"] = previous
        await initializer.close()
        await worker.close()
    return run


def test_known_failed_execution_reconciles_once_with_conservative_liability(
    l2_url, monkeypatch
) -> None:
    async def check() -> None:
        async with harness(l2_url) as h:
            run = await _prepare_known_failed_target(h, monkeypatch)
            service = KnownFailedExecutionReconciliationService(h.reconciler)
            target = await service.select_exact_target()
            liability = conservative_request_liability_micro(hosted_luna_profile())
            assert target.run_id == run and target.liability_micro == liability == 4400

            async with h.admin.connect() as connection:
                before = (
                    await connection.execute(
                        text(
                            "SELECT c.available,c.held,c.settled,d.available,d.held,d.settled "
                            "FROM public_campaign c JOIN public_day d USING(campaign_id)"
                        )
                    )
                ).one()
                physical_before = (
                    await connection.execute(
                        text(
                            "SELECT o.operation_kind,o.current_phase,o.outcome,"
                            "(SELECT count(*) FROM operation_events e WHERE "
                            "e.operation_id=o.operation_id AND "
                            "e.target_phase='DISPATCH_STARTED') "
                            "FROM execution_operations o JOIN public_provider_execution x "
                            "ON x.execution_attempt_id=o.execution_attempt_id "
                            "WHERE x.run_id=:r ORDER BY o.call_ordinal"
                        ),
                        {"r": run},
                    )
                ).all()

            result = await service.reconcile_target(target)
            replay = await service.reconcile_target(target)
            assert result.reconciled and not replay.reconciled
            assert result.evidence_digest == replay.evidence_digest
            assert result.state == replay.state == "FAILED_SAFETY"

            async with h.admin.connect() as connection:
                final = (
                    await connection.execute(
                        text(
                            "SELECT r.state,z.state,z.settled_cost,b.state,"
                            "w.closed_at IS NOT NULL,w.close_reason,"
                            "(SELECT count(*) FROM public_slot WHERE run_id=:r),"
                            "(SELECT count(*) FROM public_money_event WHERE run_id=:r "
                            "AND event_kind='SETTLE'),"
                            "(SELECT count(*) FROM public_worker_claim WHERE run_id=:r "
                            "AND released_at IS NULL),"
                            "(SELECT count(*) FROM public_worker_dispatch_pin p "
                            "JOIN public_worker_claim c USING(claim_id) WHERE c.run_id=:r "
                            "AND p.closed_at IS NULL) "
                            "FROM public_run r JOIN public_reservation z USING(run_id) "
                            "JOIN public_outbox b USING(run_id) "
                            "JOIN public_worker_work w USING(run_id) WHERE r.run_id=:r"
                        ),
                        {"r": run},
                    )
                ).one()
                after = (
                    await connection.execute(
                        text(
                            "SELECT c.available,c.held,c.settled,d.available,d.held,d.settled "
                            "FROM public_campaign c JOIN public_day d USING(campaign_id)"
                        )
                    )
                ).one()
                physical_after = (
                    await connection.execute(
                        text(
                            "SELECT o.operation_kind,o.current_phase,o.outcome,"
                            "(SELECT count(*) FROM operation_events e WHERE "
                            "e.operation_id=o.operation_id AND "
                            "e.target_phase='DISPATCH_STARTED') "
                            "FROM execution_operations o JOIN public_provider_execution x "
                            "ON x.execution_attempt_id=o.execution_attempt_id "
                            "WHERE x.run_id=:r ORDER BY o.call_ordinal"
                        ),
                        {"r": run},
                    )
                ).all()
                candidates = await connection.scalar(
                    text(
                        "SELECT public_live_api.known_failed_execution_reconciliation_candidates()"
                    )
                )
            assert final == (
                "FAILED_SAFETY",
                "SETTLED",
                liability,
                "CLOSED",
                True,
                "KNOWN_FAILED_RECONCILED",
                0,
                1,
                0,
                0,
            )
            assert after == (
                before[0] + 200_000 - liability,
                before[1] - 200_000,
                before[2] + liability,
                before[3] + 200_000 - liability,
                before[4] - 200_000,
                before[5] + liability,
            )
            assert after[0] + after[1] + after[2] == 15_000_000
            assert after[3] + after[4] + after[5] == 4_000_000
            assert physical_after == physical_before
            assert candidates == []

    asyncio.run(check())


@pytest.mark.parametrize(
    "mutation",
    [
        "provider_unknown",
        "provider_without_dispatch",
        "two_provider_sends",
        "tool_not_completed",
        "later_provider_dispatched",
        "retry",
        "active_control",
        "open_claim_pin",
    ],
)
def test_known_failed_execution_rejects_nonexact_truth(l2_url, monkeypatch, mutation) -> None:
    async def check() -> None:
        async with harness(l2_url) as h:
            run = await _prepare_known_failed_target(h, monkeypatch)
            async with h.admin.begin() as connection:
                attempt = await connection.scalar(
                    text(
                        "SELECT execution_attempt_id FROM public_provider_execution WHERE run_id=:r"
                    ),
                    {"r": run},
                )
                op1, tool, op3 = tuple(
                    await connection.scalars(
                        text(
                            "SELECT operation_id FROM execution_operations "
                            "WHERE execution_attempt_id=:a ORDER BY call_ordinal"
                        ),
                        {"a": attempt},
                    )
                )
                if mutation in {
                    "provider_without_dispatch",
                    "two_provider_sends",
                    "later_provider_dispatched",
                }:
                    # Test-only corruption fixture in a disposable database. Production
                    # provenance remains append-only; the reconciler must still reject
                    # an impossible/mutated event graph if presented by an admin fixture.
                    await connection.execute(text("SET LOCAL session_replication_role=replica"))
                if mutation == "provider_unknown":
                    await connection.execute(
                        text(
                            "UPDATE execution_operations SET current_phase='OUTCOME_UNKNOWN',"
                            "outcome='TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME' WHERE operation_id=:o"
                        ),
                        {"o": op1},
                    )
                elif mutation == "provider_without_dispatch":
                    await connection.execute(
                        text(
                            "UPDATE operation_events SET target_phase='SECURITY_ADMITTED' "
                            "WHERE operation_id=:o AND target_phase='DISPATCH_STARTED'"
                        ),
                        {"o": op1},
                    )
                elif mutation in {"two_provider_sends", "later_provider_dispatched"}:
                    await connection.execute(
                        text(
                            "UPDATE operation_events SET target_phase='DISPATCH_STARTED' "
                            "WHERE operation_id=:o AND target_phase='SECURITY_ADMITTED'"
                        ),
                        {"o": op3},
                    )
                elif mutation == "tool_not_completed":
                    await connection.execute(
                        text(
                            "UPDATE execution_operations SET outcome='CANCELLED' "
                            "WHERE operation_id=:o"
                        ),
                        {"o": tool},
                    )
                elif mutation == "retry":
                    await connection.execute(
                        text(
                            "UPDATE public_provider_operation_link "
                            "SET retry_of_operation_id=:prior WHERE operation_id=:o"
                        ),
                        {"prior": op1, "o": op3},
                    )
                elif mutation == "active_control":
                    await connection.execute(text("UPDATE public_control SET enabled=true"))
                else:
                    await connection.execute(
                        text(
                            "UPDATE public_worker_claim SET released_at=NULL,release_reason=NULL "
                            "WHERE run_id=:r AND fence=(SELECT max(fence) FROM "
                            "public_worker_claim WHERE run_id=:r)"
                        ),
                        {"r": run},
                    )
                    await connection.execute(
                        text(
                            "UPDATE public_worker_dispatch_pin SET closed_at=NULL,"
                            "closure_evidence_digest=NULL,outcome_event_id=NULL "
                            "WHERE operation_id=:o"
                        ),
                        {"o": op1},
                    )
            service = KnownFailedExecutionReconciliationService(h.reconciler)
            with pytest.raises(AdmissionDenied, match="TARGET_AMBIGUOUS"):
                await service.select_exact_target()
            with pytest.raises(DBAPIError):
                async with h.reconciler.transaction() as tx:
                    await tx.reconcile_known_failed_execution(run)

    asyncio.run(check())


def test_known_failed_reconciler_acl_and_migration_head(l2_url) -> None:
    async def check() -> None:
        async with harness(l2_url) as h:
            async with h.admin.connect() as connection:
                head = await connection.scalar(text("SELECT version_num FROM alembic_version"))
                privileges = (
                    await connection.execute(
                        text(
                            "SELECT "
                            "has_function_privilege('aiscc_public_live_reconciler',"
                            "'public_live_api.reconcile_known_failed_execution_run(bytea)',"
                            "'EXECUTE'),"
                            "has_function_privilege('aiscc_public_live_runtime',"
                            "'public_live_api.reconcile_known_failed_execution_run(bytea)',"
                            "'EXECUTE'),"
                            "has_function_privilege('public',"
                            "'public_live_api.reconcile_known_failed_execution_run(bytea)',"
                            "'EXECUTE')"
                        )
                    )
                ).one()
            assert head == "20260919_0026"
            assert privileges == (True, False, False)

    asyncio.run(check())
