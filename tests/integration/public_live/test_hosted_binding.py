"""Executable hosted L5 proof against the accepted private authority chain."""

import asyncio
import json
import os
import secrets
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from types import MappingProxyType

import pytest
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import DBAPIError

from aiscc.persistence import create_engine, create_session_factory
from aiscc.providers.models import (
    ExecutionOperationOutcome,
    ProviderCall,
    ProviderResult,
    ToolCallCandidate,
)
from aiscc.public_live.hosted_proof import (
    FaultPoint,
    QAProviderDoubleAdapter,
    run_operator_proof,
)
from aiscc.public_live.initializer import create_initializer
from aiscc.public_live.luna_profile import (
    conservative_request_liability_micro,
    hosted_luna_profile,
)
from aiscc.public_live.service import UnknownProviderReconciliationService
from aiscc.public_live.start_authority import StartContract
from aiscc.public_live.start_repository import StartRepository
from aiscc.public_live.worker import create_worker
from aiscc.public_live.worker_authority import ActiveClaim, DurableWorkerAuthority, WorkerRepository
from tests.integration.public_live.test_service import harness

pytestmark = pytest.mark.postgres


@contextmanager
def provider_double():
    receipts: dict[str, int] = {}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            return

        def do_POST(self):  # noqa: N802
            size = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(size))
            campaign = body["campaign"]
            receipts[campaign] = receipts.get(campaign, 0) + 1
            self._send({"receipt_count": receipts[campaign]})

        def do_GET(self):  # noqa: N802
            campaign = self.path.split("campaign=", 1)[-1]
            self._send({"receipt_count": receipts.get(campaign, 0)})

        def _send(self, value):
            body = json.dumps(value).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/v1"
    finally:
        server.shutdown()
        thread.join(timeout=5)
        server.server_close()


async def prepared(h, fault_point):
    h.admission.start_contract = StartContract.load()
    run = (await h.admit()).run_id
    initializer_password = secrets.token_urlsafe(24)
    worker_password = secrets.token_urlsafe(24)
    async with h.admin.begin() as connection:
        await connection.execute(
            text(f"ALTER ROLE aiscc_live_initializer_login PASSWORD '{initializer_password}'")
        )
        await connection.execute(
            text(f"ALTER ROLE aiscc_live_worker_login PASSWORD '{worker_password}'")
        )
    initializer_url = (
        make_url(h.url)
        .set(username="aiscc_live_initializer_login", password=initializer_password)
        .render_as_string(hide_password=False)
    )
    worker_url = (
        make_url(h.url)
        .set(username="aiscc_live_worker_login", password=worker_password)
        .render_as_string(hide_password=False)
    )
    with provider_double() as endpoint:
        result = await run_operator_proof(
            {
                "AISCC_PUBLIC_LIVE_START_DATABASE_URL": initializer_url,
                "AISCC_PUBLIC_LIVE_DATABASE_URL": worker_url,
                "AISCC_HOSTED_L5_PROOF_CAMPAIGN": "proof-0123456789abcdef",
                "AISCC_HOSTED_L5_PROVIDER_DOUBLE_URL": endpoint,
                "AISCC_HOSTED_L5_PROOF_LOCAL_TRANSPORT": "ENABLED",
                "AISCC_HOSTED_L5_FAKE_SECRET_CLASS": "SYNTHETIC_SENTINEL_ONLY",
                "AISCC_PUBLIC_LIVE_ADMISSION": "DISABLED",
            },
            fault_point,
        )
    assert result.run_id == run.hex()
    return run, result.observation


def test_actual_login_roles_activate_only_narrow_capabilities(l2_url) -> None:
    async def check():
        async with harness(l2_url) as h:
            async with h.admin.begin() as connection:
                await connection.execute(
                    text("ALTER ROLE aiscc_live_initializer_login PASSWORD 'role_init_only'")
                )
                await connection.execute(
                    text("ALTER ROLE aiscc_live_worker_login PASSWORD 'role_worker_only'")
                )
            base = make_url(h.url)
            init_url = base.set(
                username="aiscc_live_initializer_login", password="role_init_only"
            ).render_as_string(hide_password=False)
            worker_url = base.set(
                username="aiscc_live_worker_login", password="role_worker_only"
            ).render_as_string(hide_password=False)
            init_engine = create_engine(
                init_url,
                role="aiscc_public_live_initializer",
            )
            worker_engine = create_engine(
                worker_url,
                role="aiscc_public_live_execution",
            )
            try:
                init_repo = StartRepository(create_session_factory(init_engine))
                worker_repo = WorkerRepository(create_session_factory(worker_engine))
                await init_repo.verify_runtime_identity()
                await worker_repo.verify_runtime_identity()
                authority = DurableWorkerAuthority(worker_repo)
                await authority.register()
                assert await authority.claim_next_work() is None
                stop = asyncio.Event()
                stop.set()
                initializer = create_initializer({"AISCC_PUBLIC_LIVE_START_DATABASE_URL": init_url})
                worker = create_worker({"AISCC_PUBLIC_LIVE_DATABASE_URL": worker_url})
                try:
                    await initializer.run(stop)
                    await worker.run(stop)
                    assert callable(worker.execute_claim)
                finally:
                    await initializer.close()
                    await worker.close()
                for engine, statement in (
                    (
                        worker_engine,
                        "INSERT INTO work_runs(work_run_id,project_id,task_contract_id,"
                        "task_contract_version,workflow_state,state_version,runtime_mode,"
                        "created_at,updated_at) VALUES('denied','x','x','1','READY',1,"
                        "'PUBLIC_BOUNDED_LIVE',now(),now())",
                    ),
                    (
                        init_engine,
                        "INSERT INTO execution_operations(operation_id,execution_attempt_id,"
                        "operation_kind,operation_fingerprint,current_phase,resource_identity,"
                        "call_ordinal,latest_event_sequence,created_at,updated_at) VALUES"
                        "('denied','denied','PROVIDER',repeat('a',64),'PREPARED','x',1,0,now(),now())",
                    ),
                ):
                    with pytest.raises(DBAPIError):
                        async with engine.begin() as connection:
                            await connection.execute(text(statement))
                with pytest.raises(DBAPIError):
                    async with init_engine.begin() as connection:
                        await connection.execute(text("SET ROLE postgres"))
                with pytest.raises(DBAPIError):
                    async with h.engines[0].begin() as connection:
                        await connection.execute(
                            text("SELECT public_live_api.start_next(decode(repeat('00',16),'hex'))")
                        )
            finally:
                await init_engine.dispose()
                await worker_engine.dispose()

    asyncio.run(check())


def test_production_claim_executor_runs_primary_verify_correct(l2_url) -> None:
    async def check():
        async with harness(l2_url) as h:
            h.admission.start_contract = StartContract.load()
            run = (await h.admit()).run_id
            initializer = create_initializer({"AISCC_PUBLIC_LIVE_START_DATABASE_URL": h.url})
            decisions = {
                "PRIMARY": ("VERIFY_REQUIRED", "a" * 64, None),
                "VERIFY": ("CORRECTABLE_DEFECT", "b" * 64, "exact-defect"),
                "CORRECT": ("COMPLETE", "c" * 64, None),
            }

            def validate(role, _result):
                decision, proof, defect_ref = decisions[role]
                return MappingProxyType(
                    {"decision": decision, "proof": proof, "defect_ref": defect_ref}
                )

            worker = create_worker(
                {"AISCC_PUBLIC_LIVE_DATABASE_URL": h.url},
                semantic_validator=validate,
            )
            previous = os.environ.get("AISCC_OPENAI_API_KEY")
            try:
                assert await initializer.step()
                await worker.authority.register()
                claim = await worker.authority.claim_next_work()
                assert claim is not None
                active = ActiveClaim(claim)
                with provider_double() as endpoint:
                    adapter = QAProviderDoubleAdapter(
                        endpoint,
                        "semantic-chain-proof",
                        FaultPoint.BEFORE_DISPATCH,
                    )
                    worker.adapter = adapter
                    os.environ["AISCC_OPENAI_API_KEY"] = "synthetic-hosted-proof-only"
                    assert await worker.execute_claim(active) == "EXECUTION_TERMINAL"
                    assert adapter.observe_receipts() == 3
                    assert [call.reasoning_effort for call in adapter.calls] == [
                        "low",
                        "low",
                        "medium",
                    ]
                async with h.admin.connect() as connection:
                    links = (
                        await connection.execute(
                            text(
                                "SELECT semantic_role,request_ordinal FROM "
                                "public_provider_operation_link WHERE run_id=:r "
                                "ORDER BY request_ordinal"
                            ),
                            {"r": run},
                        )
                    ).all()
                assert links == [("PRIMARY", 1), ("VERIFY", 2), ("CORRECT", 3)]
            finally:
                if previous is None:
                    os.environ.pop("AISCC_OPENAI_API_KEY", None)
                else:
                    os.environ["AISCC_OPENAI_API_KEY"] = previous
                await initializer.close()
                await worker.close()

    asyncio.run(check())


def test_fixed_worker_starts_idle_with_exact_worker_login_without_docker(
    l2_url, monkeypatch
) -> None:
    async def check():
        async with harness(l2_url) as h:
            worker_password = secrets.token_urlsafe(24)
            async with h.admin.begin() as connection:
                await connection.execute(
                    text(f"ALTER ROLE aiscc_live_worker_login PASSWORD '{worker_password}'")
                )
            worker_url = (
                make_url(h.url)
                .set(username="aiscc_live_worker_login", password=worker_password)
                .render_as_string(hide_password=False)
            )
            worker = create_worker({"AISCC_PUBLIC_LIVE_DATABASE_URL": worker_url})

            def forbidden(*_args, **_kwargs):
                raise AssertionError("Docker lookup was reached")

            monkeypatch.setattr("shutil.which", forbidden)
            try:
                await worker.authority.repository.verify_runtime_identity()
                await worker.authority.register()
                worker.check()
                assert await worker.authority.claim_next_work() is None
                assert worker.adapter.invocation_count == 0
                assert worker.last_stockroom_dispatcher is None
            finally:
                await worker.close()

    asyncio.run(check())


def test_durable_pre_dispatch_definitely_not_sent_and_zero_receipts(l2_url) -> None:
    async def check():
        async with harness(l2_url) as h:
            run, proof = await prepared(h, FaultPoint.BEFORE_DISPATCH)
            async with h.admin.connect() as session:
                phases = tuple(
                    await session.scalars(
                        text(
                            "SELECT current_phase FROM execution_operations o "
                            "JOIN public_provider_execution e ON e.execution_attempt_id="
                            "o.execution_attempt_id WHERE e.run_id=:r"
                        ),
                        {"r": run},
                    )
                )
                pins = await session.scalar(text("SELECT count(*) FROM public_worker_dispatch_pin"))
            assert proof.provider_receipts == 0
            assert phases == ("OUTCOME_KNOWN",) and pins == 0

    asyncio.run(check())


def test_durable_post_dispatch_unknown_quarantines_without_resend(l2_url) -> None:
    async def check():
        async with harness(l2_url) as h:
            run, proof = await prepared(h, FaultPoint.AFTER_DISPATCH)
            async with h.admin.connect() as session:
                row = (
                    await session.execute(
                        text(
                            "SELECT o.current_phase,w.recovery_required,p.closed_at IS NULL,"
                            "c.claim_id,c.worker_id,c.process_generation,c.fence,c.claim_version "
                            "FROM execution_operations o JOIN public_provider_execution e "
                            "ON e.execution_attempt_id=o.execution_attempt_id "
                            "JOIN public_worker_work w USING(run_id) "
                            "JOIN public_worker_dispatch_pin p ON p.operation_id=o.operation_id "
                            "JOIN public_worker_claim c ON c.claim_id=p.claim_id WHERE e.run_id=:r"
                        ),
                        {"r": run},
                    )
                ).one()
            assert proof.provider_receipts == 1 and proof.quarantine_required
            assert row[:3] == ("OUTCOME_UNKNOWN", True, True)
            with pytest.raises(DBAPIError):
                async with h.admin.begin() as connection:
                    await connection.execute(
                        text(
                            "SELECT public_live_api.worker_release(:c,:w,:p,:f,:v,"
                            "'LIVE_UNAVAILABLE',decode(repeat('00',32),'hex'))"
                        ),
                        {"c": row[3], "w": row[4], "p": row[5], "f": row[6], "v": row[7]},
                    )

    asyncio.run(check())


def test_unknown_p1_operation_reconciles_once_without_resend(l2_url) -> None:
    async def check() -> None:
        async with harness(l2_url) as h:
            run, observation = await prepared(h, FaultPoint.AFTER_DISPATCH)
            assert observation.provider_receipts == 1
            assert observation.durable_phase == "OUTCOME_UNKNOWN"
            assert observation.retry_allowed is False
            await h.clock((datetime.now(UTC) + timedelta(minutes=3)).isoformat())
            await h.sql("UPDATE public_control SET enabled=false")
            service = UnknownProviderReconciliationService(h.reconciler)
            target = await service.select_exact_target()
            liability = conservative_request_liability_micro(hosted_luna_profile())
            assert target.run_id == run
            assert target.liability_micro == liability

            async with h.admin.connect() as connection:
                before = (
                    await connection.execute(
                        text(
                            "SELECT c.available,c.held,c.settled,d.available,d.held,d.settled "
                            "FROM public_campaign c JOIN public_day d USING(campaign_id)"
                        )
                    )
                ).one()
            result = await service.reconcile_target(target)
            assert result.reconciled and result.state == "FAILED_TIMEOUT"

            async with h.admin.connect() as connection:
                row = (
                    await connection.execute(
                        text(
                            "SELECT r.state,z.state,z.settled_cost,s.state,s.run_id IS NULL,"
                            "b.state,w.recovery_required,w.closed_at IS NOT NULL,"
                            "p.closed_at IS NOT NULL,p.outcome_event_id=e.event_id,"
                            "c.released_at IS NOT NULL,o.current_phase,o.outcome "
                            "FROM public_run r JOIN public_reservation z USING(run_id) "
                            "JOIN public_outbox b USING(run_id) "
                            "JOIN public_worker_work w USING(run_id) "
                            "JOIN public_provider_operation_link l USING(run_id) "
                            "JOIN execution_operations o USING(operation_id) "
                            "JOIN operation_events e ON e.operation_id=o.operation_id "
                            "AND e.target_phase='OUTCOME_UNKNOWN' "
                            "JOIN public_worker_dispatch_pin p ON p.operation_id=o.operation_id "
                            "JOIN public_worker_claim c ON c.claim_id=p.claim_id "
                            "CROSS JOIN public_slot s WHERE r.run_id=:r AND s.slot_id=1"
                        ),
                        {"r": run},
                    )
                ).one()
                counts = (
                    await connection.execute(
                        text(
                            "SELECT "
                            "(SELECT count(*) FROM execution_operations o "
                            "JOIN public_provider_execution x "
                            "ON x.execution_attempt_id=o.execution_attempt_id "
                            "WHERE x.run_id=:r),"
                            "(SELECT count(*) FROM execution_operations o "
                            "JOIN public_provider_execution x "
                            "ON x.execution_attempt_id=o.execution_attempt_id "
                            "WHERE x.run_id=:r AND o.operation_kind='TOOL'),"
                            "(SELECT count(*) FROM public_money_event "
                            "WHERE run_id=:r AND event_kind='SETTLE'),"
                            "(SELECT count(*) FROM public_worker_claim "
                            "WHERE run_id=:r AND released_at IS NULL),"
                            "(SELECT count(*) FROM public_worker_dispatch_pin p "
                            "JOIN public_worker_claim c USING(claim_id) "
                            "WHERE c.run_id=:r AND p.closed_at IS NULL)"
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
            assert row == (
                "FAILED_TIMEOUT",
                "SETTLED",
                liability,
                "FREE",
                True,
                "CLOSED",
                True,
                True,
                True,
                True,
                True,
                "OUTCOME_UNKNOWN",
                "TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME",
            )
            assert counts == (1, 0, 1, 0, 0)
            assert after == (
                before[0] + 200_000 - liability,
                before[1] - 200_000,
                before[2] + liability,
                before[3] + 200_000 - liability,
                before[4] - 200_000,
                before[5] + liability,
            )

            repeated = await service.reconcile_target(target)
            assert not repeated.reconciled
            async with h.admin.connect() as connection:
                unchanged = (
                    await connection.execute(
                        text(
                            "SELECT count(*),min(cost),max(cost) FROM public_money_event "
                            "WHERE run_id=:r AND event_kind='SETTLE'"
                        ),
                        {"r": run},
                    )
                ).one()
            assert unchanged == (1, liability, liability)

    asyncio.run(check())


def test_known_paths_are_not_unknown_reconciliation_candidates(l2_url) -> None:
    async def check() -> None:
        for fault in (FaultPoint.BEFORE_DISPATCH, FaultPoint.KNOWN_CLOSED_FAILURE):
            async with harness(l2_url) as h:
                await prepared(h, fault)
                await h.clock((datetime.now(UTC) + timedelta(minutes=3)).isoformat())
                async with h.reconciler.transaction() as tx:
                    assert await tx.unknown_reconciliation_candidates() == ()

    asyncio.run(check())


def test_known_closed_failure_performs_one_same_role_retry(l2_url) -> None:
    async def check():
        async with harness(l2_url) as h:
            run, proof = await prepared(h, FaultPoint.KNOWN_CLOSED_FAILURE)
            async with h.admin.connect() as session:
                links = (
                    await session.execute(
                        text(
                            "SELECT operation_id,request_ordinal,semantic_role,"
                            "retry_of_operation_id "
                            "FROM public_provider_operation_link WHERE run_id=:r "
                            "ORDER BY request_ordinal"
                        ),
                        {"r": run},
                    )
                ).all()
                outcomes = (
                    (
                        await session.execute(
                            text(
                                "SELECT o.outcome FROM execution_operations o JOIN "
                                "public_provider_operation_link l USING(operation_id) "
                                "WHERE l.run_id=:r ORDER BY l.request_ordinal"
                            ),
                            {"r": run},
                        )
                    )
                    .scalars()
                    .all()
                )
            assert proof.provider_receipts == 1 and proof.retry_allowed
            assert len(links) == 2 and links[0][2] == links[1][2] == "PRIMARY"
            assert links[1][3] == links[0][0]
            assert outcomes == ["DEFINITELY_NOT_SENT", "PROVIDER_COMPLETED"]

    asyncio.run(check())


def test_production_stockroom_tool_dispatches_once_and_continues(l2_url) -> None:
    class ToolProviderDouble:
        def __init__(self) -> None:
            self.invocation_count = 0
            self.calls: list[ProviderCall] = []

        def call(self, call: ProviderCall, *, secret: str) -> ProviderResult:
            assert secret == "synthetic-hosted-proof-only"
            self.invocation_count += 1
            self.calls.append(call)
            if self.invocation_count == 1:
                item = {
                    "type": "function_call",
                    "name": "stockroom_summary",
                    "arguments": "{}",
                    "call_id": "call-stockroom-production",
                }
                return ProviderResult(
                    call.operation_id,
                    "completed",
                    ExecutionOperationOutcome.PROVIDER_COMPLETED,
                    "provider-tool-call",
                    (item,),
                    None,
                    ToolCallCandidate("stockroom_summary", "{}", "call-stockroom-production"),
                    MappingProxyType({"input_tokens": 1, "output_tokens": 1}),
                    None,
                    "d" * 64,
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
                "e" * 64,
            )

    async def check():
        async with harness(l2_url) as h:
            h.admission.start_contract = StartContract.load()
            run = (await h.admit()).run_id
            initializer = create_initializer({"AISCC_PUBLIC_LIVE_START_DATABASE_URL": h.url})
            worker = create_worker({"AISCC_PUBLIC_LIVE_DATABASE_URL": h.url})
            adapter = ToolProviderDouble()
            worker.adapter = adapter
            previous = os.environ.get("AISCC_OPENAI_API_KEY")
            try:
                assert await initializer.step()
                await worker.authority.register()
                claim = await worker.authority.claim_next_work()
                assert claim is not None
                os.environ["AISCC_OPENAI_API_KEY"] = "synthetic-hosted-proof-only"
                assert await worker.execute_claim(ActiveClaim(claim)) == "EXECUTION_TERMINAL"
                async with h.admin.connect() as session:
                    operations = (
                        await session.execute(
                            text(
                                "SELECT operation_kind,outcome FROM execution_operations o "
                                "JOIN public_provider_execution e ON e.execution_attempt_id="
                                "o.execution_attempt_id WHERE e.run_id=:r ORDER BY call_ordinal"
                            ),
                            {"r": run},
                        )
                    ).all()
                assert worker.last_stockroom_dispatcher.invocation_count == 1
                assert {
                    domain.value
                    for domain in worker.last_stockroom_dispatcher.last_consumed_domains
                } == {"TOOL", "REPOSITORY", "SCENARIO"}
                assert adapter.invocation_count == 2
                assert any(
                    item.get("type") == "function_call_output"
                    for item in adapter.calls[1].input_items
                )
                assert operations == [
                    ("PROVIDER", "PROVIDER_COMPLETED"),
                    ("TOOL", "TOOL_COMPLETED"),
                    ("PROVIDER", "PROVIDER_COMPLETED"),
                ]
            finally:
                if previous is None:
                    os.environ.pop("AISCC_OPENAI_API_KEY", None)
                else:
                    os.environ["AISCC_OPENAI_API_KEY"] = previous
                await initializer.close()
                await worker.close()

    asyncio.run(check())


@pytest.mark.parametrize(
    ("tool_names", "expected_tool_calls", "expected_provider_calls"),
    [
        (("unknown_tool",), 0, 1),
        (("stockroom_summary", "stockroom_summary"), 1, 2),
    ],
)
def test_production_tool_scope_denies_unknown_and_second_dispatch(
    l2_url, tool_names, expected_tool_calls, expected_provider_calls
) -> None:
    class ToolSequenceAdapter:
        def __init__(self) -> None:
            self.invocation_count = 0

        def call(self, call: ProviderCall, *, secret: str) -> ProviderResult:
            assert secret == "synthetic-hosted-proof-only"
            name = tool_names[self.invocation_count]
            self.invocation_count += 1
            call_id = f"call-{self.invocation_count}"
            item = {
                "type": "function_call",
                "name": name,
                "arguments": "{}",
                "call_id": call_id,
            }
            return ProviderResult(
                call.operation_id,
                "completed",
                ExecutionOperationOutcome.PROVIDER_COMPLETED,
                f"provider-tool-{self.invocation_count}",
                (item,),
                None,
                ToolCallCandidate(name, "{}", call_id),
                MappingProxyType({"input_tokens": 1, "output_tokens": 1}),
                None,
                str(self.invocation_count) * 64,
            )

    async def check():
        async with harness(l2_url) as h:
            h.admission.start_contract = StartContract.load()
            run = (await h.admit()).run_id
            initializer = create_initializer({"AISCC_PUBLIC_LIVE_START_DATABASE_URL": h.url})
            worker = create_worker({"AISCC_PUBLIC_LIVE_DATABASE_URL": h.url})
            adapter = ToolSequenceAdapter()
            worker.adapter = adapter
            previous = os.environ.get("AISCC_OPENAI_API_KEY")
            try:
                assert await initializer.step()
                await worker.authority.register()
                claim = await worker.authority.claim_next_work()
                assert claim is not None
                os.environ["AISCC_OPENAI_API_KEY"] = "synthetic-hosted-proof-only"
                assert await worker.execute_claim(ActiveClaim(claim)) == "EXECUTION_TERMINAL"
                async with h.admin.connect() as session:
                    operations = (
                        await session.execute(
                            text(
                                "SELECT operation_kind,outcome FROM execution_operations o "
                                "JOIN public_provider_execution e ON e.execution_attempt_id="
                                "o.execution_attempt_id WHERE e.run_id=:r ORDER BY call_ordinal"
                            ),
                            {"r": run},
                        )
                    ).all()
                actual_tool_calls = (
                    worker.last_stockroom_dispatcher.invocation_count
                    if worker.last_stockroom_dispatcher is not None
                    else 0
                )
                assert actual_tool_calls == expected_tool_calls
                assert adapter.invocation_count == expected_provider_calls
                assert operations[-1] == ("TOOL", "DENIED_BEFORE_SIDE_EFFECT")
            finally:
                if previous is None:
                    os.environ.pop("AISCC_OPENAI_API_KEY", None)
                else:
                    os.environ["AISCC_OPENAI_API_KEY"] = previous
                await initializer.close()
                await worker.close()

    asyncio.run(check())


def test_sandbox_termination_executes_supervisor_and_observes_zero_receipts(l2_url) -> None:
    async def check():
        async with harness(l2_url) as h:
            h.admission.start_contract = StartContract.load()
            run = (await h.admit()).run_id
            async with h.admin.begin() as connection:
                await connection.execute(
                    text("ALTER ROLE aiscc_live_initializer_login PASSWORD 'sandbox_init_only'")
                )
                await connection.execute(
                    text("ALTER ROLE aiscc_live_worker_login PASSWORD 'sandbox_worker_only'")
                )
            base = make_url(h.url)
            with provider_double() as endpoint:
                result = await run_operator_proof(
                    {
                        "AISCC_PUBLIC_LIVE_START_DATABASE_URL": base.set(
                            username="aiscc_live_initializer_login",
                            password="sandbox_init_only",
                        ).render_as_string(hide_password=False),
                        "AISCC_PUBLIC_LIVE_DATABASE_URL": base.set(
                            username="aiscc_live_worker_login",
                            password="sandbox_worker_only",
                        ).render_as_string(hide_password=False),
                        "AISCC_HOSTED_L5_PROOF_CAMPAIGN": "proof-0123456789abcdef",
                        "AISCC_HOSTED_L5_PROVIDER_DOUBLE_URL": endpoint,
                        "AISCC_HOSTED_L5_PROOF_LOCAL_TRANSPORT": "ENABLED",
                        "AISCC_HOSTED_L5_FAKE_SECRET_CLASS": "SYNTHETIC_SENTINEL_ONLY",
                        "AISCC_PUBLIC_LIVE_ADMISSION": "DISABLED",
                    },
                    FaultPoint.SANDBOX_TERMINATION,
                )
            assert result.run_id == run.hex()
            assert result.supervisor_executed and result.observation.provider_receipts == 0
            assert not result.observation.quarantine_required

    asyncio.run(check())


@pytest.mark.parametrize("drift", ["gate", "deadline"])
def test_current_start_freshness_denies_before_first_p1_side_effect(l2_url, drift) -> None:
    async def check():
        async with harness(l2_url) as h:
            h.admission.start_contract = StartContract.load()
            run = (await h.admit()).run_id
            async with h.admin.begin() as connection:
                if drift == "gate":
                    await connection.execute(
                        text(
                            "UPDATE public_control SET enabled=false,"
                            "incident='synthetic-gate-drift'"
                        )
                    )
                else:
                    await connection.execute(
                        text(
                            "UPDATE public_run SET "
                            "admitted_at=statement_timestamp()-interval '91 seconds',"
                            "deadline=statement_timestamp()-interval '1 second',"
                            "read_expires=statement_timestamp()+interval '23 hours 58 minutes "
                            "29 seconds' WHERE run_id=:r"
                        ),
                        {"r": run},
                    )
            initializer = create_initializer({"AISCC_PUBLIC_LIVE_START_DATABASE_URL": h.url})
            try:
                assert await initializer.step() is False
            finally:
                await initializer.close()
            async with h.admin.connect() as connection:
                count = await connection.scalar(
                    text("SELECT count(*) FROM work_runs WHERE work_run_id=:w"),
                    {"w": "public-live-" + run.hex()},
                )
            assert count == 0

    asyncio.run(check())
