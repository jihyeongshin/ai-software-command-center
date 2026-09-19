# ruff: noqa: E501
"""Successful P1-5 execution closes only the Public Live projection."""

import asyncio
import os
import secrets
from types import MappingProxyType

import pytest
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import DBAPIError

from aiscc.providers.models import (
    ExecutionOperationOutcome,
    ProviderCall,
    ProviderResult,
    ToolCallCandidate,
)
from aiscc.public_live.initializer import create_initializer
from aiscc.public_live.service import SuccessfulExecutionReconciliationService
from aiscc.public_live.start_authority import StartContract
from aiscc.public_live.worker import create_worker
from aiscc.public_live.worker_authority import ActiveClaim
from tests.integration.public_live.test_service import harness

pytestmark = pytest.mark.postgres


async def worker_url(h) -> str:
    password = secrets.token_urlsafe(24)
    async with h.admin.begin() as connection:
        await connection.execute(text(f"ALTER ROLE aiscc_live_worker_login PASSWORD '{password}'"))
    return (
        make_url(h.url)
        .set(username="aiscc_live_worker_login", password=password)
        .render_as_string(hide_password=False)
    )


class ToolThenCompleteProvider:
    def __init__(self) -> None:
        self.invocation_count = 0

    def call(self, call: ProviderCall, *, secret: str) -> ProviderResult:
        assert secret == "synthetic-hosted-proof-only"
        self.invocation_count += 1
        if self.invocation_count == 1:
            return ProviderResult(
                call.operation_id,
                "completed",
                ExecutionOperationOutcome.PROVIDER_COMPLETED,
                "provider-tool-request",
                (
                    {
                        "type": "function_call",
                        "name": "stockroom_summary",
                        "arguments": "{}",
                        "call_id": "call-stockroom",
                    },
                ),
                None,
                ToolCallCandidate("stockroom_summary", "{}", "call-stockroom"),
                MappingProxyType({"input_tokens": 1, "output_tokens": 1}),
                None,
                "a" * 64,
            )
        return ProviderResult(
            call.operation_id,
            "completed",
            ExecutionOperationOutcome.PROVIDER_COMPLETED,
            "provider-final",
            (
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": "complete"}],
                },
            ),
            "complete",
            None,
            MappingProxyType({"input_tokens": 1, "output_tokens": 1}),
            None,
            "b" * 64,
        )


class ImmediateCompleteProvider:
    def __init__(self) -> None:
        self.invocation_count = 0

    def call(self, call: ProviderCall, *, secret: str) -> ProviderResult:
        assert secret == "synthetic-hosted-proof-only"
        self.invocation_count += 1
        return ProviderResult(
            call.operation_id,
            "completed",
            ExecutionOperationOutcome.PROVIDER_COMPLETED,
            "provider-final",
            (
                {
                    "type": "message",
                    "role": "assistant",
                    "content": [{"type": "output_text", "text": "complete"}],
                },
            ),
            "complete",
            None,
            MappingProxyType({"input_tokens": 1, "output_tokens": 1}),
            None,
            "c" * 64,
        )


def test_manual_success_reproduces_gap_then_finalizer_closes_idempotently(l2_url: str) -> None:
    async def check() -> None:
        async with harness(l2_url) as h:
            h.admission.start_contract = StartContract.load()
            run = (await h.admit()).run_id
            initializer = create_initializer({"AISCC_PUBLIC_LIVE_START_DATABASE_URL": h.url})
            worker = create_worker({"AISCC_PUBLIC_LIVE_DATABASE_URL": await worker_url(h)})
            worker.adapter = ToolThenCompleteProvider()
            previous = os.environ.get("AISCC_OPENAI_API_KEY")
            try:
                assert await initializer.step()
                await worker.authority.register()
                claim = await worker.authority.claim_next_work()
                assert claim is not None
                os.environ["AISCC_OPENAI_API_KEY"] = "synthetic-hosted-proof-only"
                active = ActiveClaim(claim)
                assert await worker.execute_claim(active) == "EXECUTION_TERMINAL"
                await worker.authority.repository.release(active.current(), "EXECUTION_TERMINAL")
                async with h.admin.connect() as connection:
                    row = (
                        await connection.execute(
                            text(
                                "SELECT r.state,z.state,q.state,b.state,"
                                "w.closed_at IS NULL,a.status,wr.workflow_state,"
                                "(SELECT count(*) FROM public_worker_claim c WHERE c.run_id=r.run_id AND c.released_at IS NULL),"
                                "(SELECT count(*) FROM public_worker_dispatch_pin p JOIN public_worker_claim c USING(claim_id) WHERE c.run_id=r.run_id AND p.closed_at IS NULL) "
                                "FROM public_run r JOIN public_reservation z USING(run_id) "
                                "JOIN public_slot q USING(run_id) JOIN public_outbox b USING(run_id) "
                                "JOIN public_worker_work w USING(run_id) JOIN public_provider_execution x USING(run_id) "
                                "JOIN execution_attempts a ON a.execution_attempt_id=x.execution_attempt_id "
                                "JOIN work_runs wr ON wr.work_run_id=x.work_run_id WHERE r.run_id=:r"
                            ),
                            {"r": run},
                        )
                    ).one()
                assert row == (
                    "ADMITTED",
                    "HELD",
                    "OCCUPIED",
                    "BOUND",
                    True,
                    "EXECUTOR_COMPLETED",
                    "RUNNING",
                    0,
                    0,
                )
                service = SuccessfulExecutionReconciliationService(h.reconciler)
                target = await service.select_exact_target()
                assert target.run_id == run
                assert target.provider_request_count == target.physical_provider_send_count == 2
                assert target.tool_operation_count == 1
                assert target.liability_micro == 8800
                result = await service.reconcile_target(target)
                replay = await service.reconcile_target(target)
                assert result.reconciled and not replay.reconciled
                assert result.evidence_digest == replay.evidence_digest
                async with h.admin.connect() as connection:
                    final = (
                        await connection.execute(
                            text(
                                "SELECT r.state,z.state,z.settled_cost,b.state,"
                                "w.closed_at IS NOT NULL,w.close_reason,a.status,wr.workflow_state,"
                                "(SELECT count(*) FROM public_slot q WHERE q.run_id=r.run_id) "
                                "FROM public_run r JOIN public_reservation z USING(run_id) "
                                "JOIN public_outbox b USING(run_id) JOIN public_worker_work w USING(run_id) "
                                "JOIN public_provider_execution x USING(run_id) "
                                "JOIN execution_attempts a ON a.execution_attempt_id=x.execution_attempt_id "
                                "JOIN work_runs wr ON wr.work_run_id=x.work_run_id WHERE r.run_id=:r"
                            ),
                            {"r": run},
                        )
                    ).one()
                assert final == (
                    "COMPLETED",
                    "SETTLED",
                    8800,
                    "CLOSED",
                    True,
                    "SUCCESS_RECONCILED",
                    "EXECUTOR_COMPLETED",
                    "RUNNING",
                    0,
                )
            finally:
                if previous is None:
                    os.environ.pop("AISCC_OPENAI_API_KEY", None)
                else:
                    os.environ["AISCC_OPENAI_API_KEY"] = previous
                await initializer.close()
                await worker.close()

    asyncio.run(check())


def test_worker_loop_automatically_closes_provider_only_success(l2_url: str) -> None:
    async def check() -> None:
        async with harness(l2_url) as h:
            h.admission.start_contract = StartContract.load()
            run = (await h.admit()).run_id
            initializer = create_initializer({"AISCC_PUBLIC_LIVE_START_DATABASE_URL": h.url})
            worker = create_worker({"AISCC_PUBLIC_LIVE_DATABASE_URL": await worker_url(h)})
            adapter = ImmediateCompleteProvider()
            worker.adapter = adapter
            stop = asyncio.Event()
            execute = worker.execute_claim

            async def execute_once(active: ActiveClaim) -> str:
                result = await execute(active)
                stop.set()
                return result

            worker.execute_claim = execute_once
            previous = os.environ.get("AISCC_OPENAI_API_KEY")
            try:
                assert await initializer.step()
                os.environ["AISCC_OPENAI_API_KEY"] = "synthetic-hosted-proof-only"
                await asyncio.wait_for(worker.run(stop), timeout=8)
                assert adapter.invocation_count == 1
                async with h.admin.connect() as connection:
                    row = (
                        await connection.execute(
                            text(
                                "SELECT r.state,z.state,z.settled_cost,b.state,"
                                "w.close_reason,a.status,wr.workflow_state,"
                                "(SELECT count(*) FROM public_slot q WHERE q.run_id=r.run_id) "
                                "FROM public_run r JOIN public_reservation z USING(run_id) "
                                "JOIN public_outbox b USING(run_id) JOIN public_worker_work w USING(run_id) "
                                "JOIN public_provider_execution x USING(run_id) "
                                "JOIN execution_attempts a ON a.execution_attempt_id=x.execution_attempt_id "
                                "JOIN work_runs wr ON wr.work_run_id=x.work_run_id WHERE r.run_id=:r"
                            ),
                            {"r": run},
                        )
                    ).one()
                assert row == (
                    "COMPLETED",
                    "SETTLED",
                    4400,
                    "CLOSED",
                    "SUCCESS_RECONCILED",
                    "EXECUTOR_COMPLETED",
                    "RUNNING",
                    0,
                )
            finally:
                if previous is None:
                    os.environ.pop("AISCC_OPENAI_API_KEY", None)
                else:
                    os.environ["AISCC_OPENAI_API_KEY"] = previous
                await initializer.close()
                await worker.close()

    asyncio.run(check())


def test_finalizer_retry_is_db_only_and_never_resends_provider(l2_url: str) -> None:
    async def check() -> None:
        async with harness(l2_url) as h:
            h.admission.start_contract = StartContract.load()
            run = (await h.admit()).run_id
            initializer = create_initializer({"AISCC_PUBLIC_LIVE_START_DATABASE_URL": h.url})
            worker = create_worker({"AISCC_PUBLIC_LIVE_DATABASE_URL": await worker_url(h)})
            adapter = ToolThenCompleteProvider()
            worker.adapter = adapter
            stop = asyncio.Event()
            attempts = 0
            original = worker.success_finalizer.reconcile_run

            async def fail_once(run_id: bytes):
                nonlocal attempts
                attempts += 1
                if attempts == 1:
                    raise RuntimeError("synthetic finalizer transaction outage")
                result = await original(run_id)
                stop.set()
                return result

            worker.success_finalizer.reconcile_run = fail_once  # type: ignore[method-assign]
            previous = os.environ.get("AISCC_OPENAI_API_KEY")
            try:
                assert await initializer.step()
                os.environ["AISCC_OPENAI_API_KEY"] = "synthetic-hosted-proof-only"
                await asyncio.wait_for(worker.run(stop), timeout=8)
                assert attempts == 2
                assert adapter.invocation_count == 2
                async with h.admin.connect() as connection:
                    state = await connection.scalar(
                        text("SELECT state FROM public_run WHERE run_id=:r"), {"r": run}
                    )
                    provider_operations = await connection.scalar(
                        text(
                            "SELECT count(*) FROM execution_operations o "
                            "JOIN public_provider_execution x USING(execution_attempt_id) "
                            "WHERE x.run_id=:r AND o.operation_kind='PROVIDER'"
                        ),
                        {"r": run},
                    )
                assert state == "COMPLETED"
                assert provider_operations == 2
            finally:
                if previous is None:
                    os.environ.pop("AISCC_OPENAI_API_KEY", None)
                else:
                    os.environ["AISCC_OPENAI_API_KEY"] = previous
                await initializer.close()
                await worker.close()

    asyncio.run(check())


def test_success_finalizer_acl_and_migration_head_are_exact(l2_url: str) -> None:
    async def check() -> None:
        async with harness(l2_url) as h, h.admin.connect() as connection:
            head = await connection.scalar(text("SELECT version_num FROM alembic_version"))
            assert head == "20260919_0027"
            for signature in (
                "public_live_api.successful_execution_reconciliation_candidates()",
                "public_live_api.complete_successful_execution_run(bytea)",
            ):
                privileges = {}
                for role in (
                    "aiscc_public_live_execution",
                    "aiscc_public_live_reconciler",
                    "aiscc_public_live_runtime",
                    "aiscc_public_live_ingress",
                    "aiscc_public_live_initializer",
                ):
                    privileges[role] = await connection.scalar(
                        text("SELECT has_function_privilege(:r,:f,'EXECUTE')"),
                        {"r": role, "f": signature},
                    )
                assert privileges == {
                    "aiscc_public_live_execution": True,
                    "aiscc_public_live_reconciler": True,
                    "aiscc_public_live_runtime": False,
                    "aiscc_public_live_ingress": False,
                    "aiscc_public_live_initializer": False,
                }
                assert not await connection.scalar(
                    text(
                        "SELECT EXISTS(SELECT 1 FROM pg_proc p WHERE "
                        "p.oid=to_regprocedure(:f) AND EXISTS(SELECT 1 FROM "
                        "aclexplode(coalesce(p.proacl,acldefault('f',p.proowner))) a "
                        "WHERE a.grantee=0 AND a.privilege_type='EXECUTE'))"
                    ),
                    {"f": signature},
                )
            for role in ("aiscc_public_live_execution", "aiscc_public_live_reconciler"):
                for table in (
                    "public_run",
                    "public_reservation",
                    "public_slot",
                    "public_outbox",
                    "public_worker_work",
                    "public_money_event",
                ):
                    assert not await connection.scalar(
                        text("SELECT has_table_privilege(:r,:t,'INSERT,UPDATE,DELETE')"),
                        {"r": role, "t": "public." + table},
                    )

    asyncio.run(check())


@pytest.mark.parametrize(
    "mutation",
    [
        "provider_unknown",
        "provider_incomplete",
        "attempt_failed",
        "tool_incomplete",
        "open_claim",
        "prior_settle",
    ],
)
def test_success_finalizer_rejects_nonexact_durable_truth(l2_url: str, mutation: str) -> None:
    async def check() -> None:
        async with harness(l2_url) as h:
            h.admission.start_contract = StartContract.load()
            run = (await h.admit()).run_id
            initializer = create_initializer({"AISCC_PUBLIC_LIVE_START_DATABASE_URL": h.url})
            worker = create_worker({"AISCC_PUBLIC_LIVE_DATABASE_URL": h.url})
            worker.adapter = ToolThenCompleteProvider()
            previous = os.environ.get("AISCC_OPENAI_API_KEY")
            try:
                assert await initializer.step()
                await worker.authority.register()
                claim = await worker.authority.claim_next_work()
                assert claim is not None
                active = ActiveClaim(claim)
                os.environ["AISCC_OPENAI_API_KEY"] = "synthetic-hosted-proof-only"
                assert await worker.execute_claim(active) == "EXECUTION_TERMINAL"
                await worker.authority.repository.release(active.current(), "EXECUTION_TERMINAL")
                async with h.admin.begin() as connection:
                    if mutation == "provider_unknown":
                        await connection.execute(
                            text(
                                "UPDATE execution_operations SET current_phase='OUTCOME_UNKNOWN',"
                                "outcome='TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME' WHERE operation_id=("
                                "SELECT o.operation_id FROM execution_operations o "
                                "JOIN public_provider_execution x USING(execution_attempt_id) "
                                "WHERE x.run_id=:r AND o.operation_kind='PROVIDER' "
                                "ORDER BY o.call_ordinal DESC LIMIT 1)"
                            ),
                            {"r": run},
                        )
                    elif mutation == "provider_incomplete":
                        await connection.execute(
                            text(
                                "UPDATE execution_operations SET current_phase='DISPATCH_STARTED',"
                                "outcome=NULL WHERE operation_id=(SELECT o.operation_id FROM "
                                "execution_operations o JOIN public_provider_execution x "
                                "USING(execution_attempt_id) WHERE x.run_id=:r AND "
                                "o.operation_kind='PROVIDER' ORDER BY o.call_ordinal DESC LIMIT 1)"
                            ),
                            {"r": run},
                        )
                    elif mutation == "attempt_failed":
                        await connection.execute(
                            text(
                                "UPDATE execution_attempts SET status='EXECUTION_FAILED' WHERE "
                                "execution_attempt_id=(SELECT execution_attempt_id FROM "
                                "public_provider_execution WHERE run_id=:r)"
                            ),
                            {"r": run},
                        )
                    elif mutation == "tool_incomplete":
                        await connection.execute(
                            text(
                                "UPDATE execution_operations SET current_phase='DISPATCH_STARTED',"
                                "outcome=NULL WHERE operation_id=(SELECT o.operation_id FROM "
                                "execution_operations o JOIN public_provider_execution x "
                                "USING(execution_attempt_id) WHERE x.run_id=:r AND "
                                "o.operation_kind='TOOL' LIMIT 1)"
                            ),
                            {"r": run},
                        )
                    elif mutation == "open_claim":
                        await connection.execute(
                            text(
                                "UPDATE public_worker_claim SET released_at=NULL,release_reason=NULL,"
                                "heartbeat_at=public_live_api.clock_lock(),"
                                "lease_expires_at=public_live_api.clock_lock()+interval '14 seconds' "
                                "WHERE run_id=:r"
                            ),
                            {"r": run},
                        )
                    else:
                        await connection.execute(
                            text(
                                "INSERT INTO public_money_event(run_id,event_kind,amount,cost,"
                                "release,campaign_id,utc_date,evidence_digest,created_at) "
                                "SELECT run_id,'SETTLE',200000,8800,191200,campaign_id,utc_date,"
                                "decode(repeat('ab',32),'hex'),public_live_api.clock_lock() "
                                "FROM public_run WHERE run_id=:r"
                            ),
                            {"r": run},
                        )
                service = SuccessfulExecutionReconciliationService(h.reconciler)
                assert await service.candidates() == ()
                with pytest.raises(DBAPIError):
                    await service.reconcile_run(run)
            finally:
                if previous is None:
                    os.environ.pop("AISCC_OPENAI_API_KEY", None)
                else:
                    os.environ["AISCC_OPENAI_API_KEY"] = previous
                await initializer.close()
                await worker.close()

    asyncio.run(check())
