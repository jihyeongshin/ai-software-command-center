"""Real PostgreSQL, distinct service instances, synthetic provider evidence only."""

import asyncio
import hashlib
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy.exc import DBAPIError

from aiscc.persistence.database import create_engine, create_session_factory
from aiscc.persistence.public_live import PublicLiveRepository
from aiscc.public_live.provider_pipeline import Decision, PipelineStore, Validation
from tests.integration.public_live.test_service import harness

pytestmark = pytest.mark.postgres


def digest(value):
    return hashlib.sha256(str(value).encode()).digest()


async def setup(h):
    admitted = await h.admit()
    run = admitted.run_id
    owner = await h.running(run)
    store = PipelineStore(h.runtime, h.reconciler)
    await store.enroll(run, datetime.now(UTC))
    version = (await h.kernel.verify_consistency(owner)).state_version
    return run, store, version


async def outcome(store, run, n, kind="KNOWN_SUCCESS", closed=False, tokens=2000, cost=4400):
    await store.outcome(
        run, n, kind, closed=closed, tokens=tokens, cost=cost, proof=digest((run, n))
    )


def test_semantics_retry_concurrency_projection_and_durable_restart(l2_url):
    async def check():
        async with harness(l2_url) as h:
            run, store, version = await setup(h)
            independent_engine = create_engine(
                h.engines[0].url.render_as_string(hide_password=False)
            )
            h.engines.append(independent_engine)
            other = PipelineStore(
                PublicLiveRepository(create_session_factory(independent_engine)), h.reconciler
            )

            async def race(n):
                return await (other if n % 2 else store).authorize(run, digest(n), 8000, version)

            results = await asyncio.gather(*(race(n) for n in range(12)), return_exceptions=True)
            tickets = [r for r in results if isinstance(r, dict)]
            assert len(tickets) == 1
            assert tickets[0]["role"] == "PRIMARY" and tickets[0]["effort"] == "low"
            # Crash after authorization: a restarted instance neither resends nor
            # creates another physical request while the outcome is uncertain.
            assert len((await other.context(run))["requests"]) == 1
            with pytest.raises(DBAPIError):
                await other.authorize(run, digest("restart"), 8000, version)
            await outcome(store, run, 1, "KNOWN_FAILURE", True, 0, 0)
            retry = await other.authorize(run, digest("retry"), 8000, version)
            assert (
                retry["ordinal"],
                retry["semantic_ordinal"],
                retry["retry_of"],
                retry["role"],
                retry["effort"],
            ) == (2, 1, 1, "PRIMARY", "low")
            await outcome(store, run, 2)
            assert (
                await h.sql("SELECT state FROM public_run WHERE run_id=:r", r=run)
                == "DISPATCH_STARTED"
            )
            with pytest.raises(DBAPIError):
                await other.authorize(run, digest("no-validation"), 8000, version)
            await store.validate(run, 2, Validation(Decision.VERIFY_REQUIRED, digest("verify")))
            verify = await other.authorize(run, digest("verify-send"), 8000, version)
            assert (
                verify["ordinal"],
                verify["semantic_ordinal"],
                verify["role"],
                verify["effort"],
            ) == (3, 2, "VERIFY", "low")
            await outcome(store, run, 3)
            assert (
                await h.sql("SELECT state FROM public_run WHERE run_id=:r", r=run)
                == "DISPATCH_STARTED"
            )
            with pytest.raises(DBAPIError):
                await store.validate(run, 3, Validation(Decision.CORRECTABLE_DEFECT, digest("bad")))
            await store.validate(
                run,
                3,
                Validation(Decision.CORRECTABLE_DEFECT, digest("defect"), "SUMMARY_MISMATCH"),
            )
            boundary = await asyncio.gather(
                *(race(n + 100) for n in range(12)), return_exceptions=True
            )
            winners = [r for r in boundary if isinstance(r, dict)]
            assert len(winners) == 1
            correct = winners[0]
            assert (
                correct["ordinal"],
                correct["semantic_ordinal"],
                correct["role"],
                correct["effort"],
            ) == (4, 3, "CORRECT", "medium")
            assert correct["defect"] == "SUMMARY_MISMATCH" and correct["trigger_ref"]
            await outcome(store, run, 4)
            await store.validate(run, 4, Validation(Decision.COMPLETE, digest("complete")))
            restored = await other.context(run)
            assert restored["pipeline"]["completed"] is True
            assert len(restored["requests"]) == 4
            assert sum(q["output_tokens"] for q in restored["requests"]) == 6000
            assert sum(q["retry_of"] is not None for q in restored["requests"]) == 1
            assert (
                await h.sql("SELECT state FROM public_run WHERE run_id=:r", r=run)
                == "GOVERNANCE_PENDING"
            )
            assert (
                await h.sql("SELECT committed_max FROM public_reservation WHERE run_id=:r", r=run)
                == 17600
            )
            assert (
                await h.sql("SELECT amount FROM public_reservation WHERE run_id=:r", r=run)
                == 200000
            )
            with pytest.raises(DBAPIError):
                await other.authorize(run, digest("fifth"), 8000, version)

    asyncio.run(check())


@pytest.mark.parametrize(
    "kind,tokens,cost", [("UNKNOWN", None, None), ("KNOWN_SUCCESS", None, None)]
)
def test_unknown_missing_usage_conservative_no_blind_retry(l2_url, kind, tokens, cost):
    async def check():
        async with harness(l2_url) as h:
            run, store, version = await setup(h)
            fp = digest("initial")
            await store.authorize(run, fp, 8000, version)
            await outcome(store, run, 1, kind, False, tokens, cost)
            restarted = PipelineStore(h.runtime, h.reconciler)
            assert (await restarted.authorize(run, fp, 8000, version))["send"] is False
            with pytest.raises(DBAPIError):
                await restarted.authorize(run, digest("again"), 8000, version)
            assert (
                await h.sql("SELECT provisional_cost FROM public_dispatch WHERE run_id=:r", r=run)
                == 4400
            )
            assert (await restarted.context(run))["requests"][0]["usage_missing"]
            if kind == "UNKNOWN":
                assert await h.service.close(run, "not-closed", target=None) is False
                h.evidence.closed.add((run, "closed"))
                assert await h.service.close(run, "closed", target=None) is True
                assert (
                    await h.sql(
                        "SELECT settled_cost FROM public_reservation WHERE run_id=:r", r=run
                    )
                    == 4400
                )

    asyncio.run(check())


def test_send_claim_is_one_time_and_rechecks_deadline(l2_url):
    async def check():
        async with harness(l2_url) as h:
            run, store, version = await setup(h)
            fp = digest("send")
            ticket = await store.authorize(run, fp, 8000, version)
            starts = await asyncio.gather(
                *(store.start(run, 1, fp, version) for _ in range(8)), return_exceptions=True
            )
            assert sum(s is None for s in starts) == 1
            assert (await store.context(run))["requests"][0]["sent_at"] is not None
            await outcome(store, run, 1)
            await store.validate(
                run, 1, Validation(Decision.VERIFY_REQUIRED, digest("verify-later"))
            )
            fp2 = digest("second")
            await store.authorize(run, fp2, 8000, version)
            deadline = datetime.fromisoformat(ticket["deadline"])
            await h.clock((deadline - timedelta(seconds=34)).isoformat())
            with pytest.raises(DBAPIError, match="SEND_GATE_DENIED"):
                await store.start(run, 2, fp2, version)

    asyncio.run(check())


def test_fence_between_authorization_and_send_prevents_provider_start(l2_url):
    async def check():
        async with harness(l2_url) as h:
            run, store, version = await setup(h)
            fp = digest("fenced-send")
            await store.authorize(run, fp, 8000, version)
            assert await h.service.close(run, "unproven", target=None) is False
            with pytest.raises(DBAPIError, match="SEND_GATE_DENIED"):
                await store.start(run, 1, fp, version)
            assert (await store.context(run))["requests"][0]["sent_at"] is None

    asyncio.run(check())


def test_durable_tool_claim_drives_receipt_backed_dispatch_once(l2_url, tmp_path, monkeypatch):
    from aiscc.public_live.provider_pipeline import PublicProviderPipeline
    from tests.unit.providers.test_luna_tool import CANDIDATE, composition, success

    async def check():
        async with harness(l2_url) as h:
            run, store, version = await setup(h)
            await store.authorize(run, digest("tool-primary"), 8000, version)
            await outcome(store, run, 1)
            owner = (await store.context(run))["owner_binding"]
            broker, prepared, dispatcher, runtime, spec, policy = composition(
                tmp_path, monkeypatch, success, owner=owner, state_version=version
            )
            pipeline = PublicProviderPipeline(store, None)
            result = await pipeline.dispatch_tool(
                run,
                CANDIDATE,
                broker,
                policy=policy,
                capabilities=prepared.capabilities,
                dispatcher=dispatcher,
                dispatch_context=prepared.dispatch_context,
            )
            assert result.output["total_available"] == 13
            assert dispatcher.invocation_count == 1
            with pytest.raises(DBAPIError):
                await pipeline.dispatch_tool(
                    run,
                    CANDIDATE,
                    broker,
                    policy=policy,
                    capabilities=prepared.capabilities,
                    dispatcher=dispatcher,
                    dispatch_context=prepared.dispatch_context,
                )
            assert dispatcher.invocation_count == 1

    asyncio.run(check())


def test_upgrade_preserves_legacy_dispatch_rows(l2_url):
    import os
    import subprocess
    import sys

    def migrate(target, command="upgrade"):
        result = subprocess.run(
            [sys.executable, "-B", "-m", "alembic", command, target],
            env={**os.environ, "AISCC_DATABASE_URL": l2_url},
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr

    migrate("20260916_0016", "downgrade")

    async def check():
        async with harness(l2_url) as h:
            run = (await h.admit()).run_id
            await h.running(run)
            await h.service.authorize_dispatch(run, 1)
            h.evidence.outcomes[(run, 1, "failure")] = ("KNOWN_FAILURE", 0, digest("old-failure"))
            # Use the established reconciler's mediated outcome operation.
            async with h.reconciler.transaction() as tx:
                await tx._call(
                    "SELECT public_live_api.record_outcome(:r,1,'KNOWN_FAILURE',0,:p,:p,:o)",
                    {"r": run, "p": digest("old-failure"), "o": digest("old-observation")[:16]},
                )
            await h.service.authorize_dispatch(run, 2)
            before = await h.sql(
                "SELECT jsonb_agg(to_jsonb(d) ORDER BY ordinal) "
                "FROM public_dispatch d WHERE run_id=:r",
                r=run,
            )
            migrate("head")
            after = await h.sql(
                "SELECT jsonb_agg(to_jsonb(d) ORDER BY ordinal) "
                "FROM public_dispatch d WHERE run_id=:r",
                r=run,
            )
            assert before == after
            assert await h.sql("SELECT count(*) FROM public_provider_request") == 0
            assert await h.sql("SELECT count(*) FROM public_provider_pipeline") == 0
            with pytest.raises(DBAPIError):
                await PipelineStore(h.runtime, h.reconciler).enroll(run, datetime.now(UTC))
            assert await h.service.close(run, "unproven", target=None) is False

    asyncio.run(check())


def test_happy_primary_and_security_tool_deadline_price(l2_url):
    async def check():
        async with harness(l2_url) as h:
            run, store, version = await setup(h)
            for sql in (
                "DELETE FROM public_provider_request",
                "UPDATE public_provider_pipeline SET completed=true",
                "INSERT INTO public_provider_validation VALUES(NULL,NULL,NULL,NULL,NULL,NULL)",
                "SELECT public_live_api.pipeline_validate(:r,1,'COMPLETE',:p,NULL)",
            ):
                with pytest.raises(DBAPIError):
                    async with h.runtime.transaction() as tx:
                        await tx._call(sql, {"r": run, "p": digest("forged")})
            for invalid in (0, 8001):
                with pytest.raises(DBAPIError):
                    await store.authorize(run, digest(invalid), invalid, version)
            await store.authorize(run, digest("primary"), 8000, version)
            await outcome(store, run, 1)
            with pytest.raises(DBAPIError):
                await store.claim_tool(run, "arbitrary", version)
            claimed = await asyncio.gather(
                *(store.claim_tool(run, "stockroom_summary", version) for _ in range(8)),
                return_exceptions=True,
            )
            assert sum(v is None for v in claimed) == 1
            with pytest.raises(DBAPIError):
                async with h.runtime.transaction() as tx:
                    await tx._call(
                        "SELECT public_live_api.project_run("
                        ":r,(SELECT 1)::bigint,'GOVERNANCE_PENDING',:p)",
                        {"r": run, "p": digest((run, 1))},
                    )
            await store.validate(run, 1, Validation(Decision.COMPLETE, digest("one-done")))
            assert len((await store.context(run))["requests"]) == 1
            assert (
                await h.sql("SELECT state FROM public_run WHERE run_id=:r", r=run)
                == "GOVERNANCE_PENDING"
            )

    asyncio.run(check())


@pytest.mark.parametrize("condition", ["deadline", "price", "retry", "legacy", "above"])
def test_fail_closed_gates(l2_url, condition):
    async def check():
        async with harness(l2_url) as h:
            run, store, version = await setup(h)
            if condition == "deadline":
                deadline = await h.sql("SELECT deadline FROM public_run WHERE run_id=:r", r=run)
                await h.clock((deadline - timedelta(seconds=34)).isoformat())
            elif condition == "price":
                await h.sql(
                    "UPDATE public_provider_pipeline "
                    "SET price_verified=clock_timestamp()-interval '25 hours' WHERE run_id=:r",
                    r=run,
                )
            elif condition == "legacy":
                with pytest.raises(DBAPIError):
                    await h.service.authorize_dispatch(run, 1)
                return
            else:
                await store.authorize(run, digest("one"), 8000, version)
                if condition == "above":
                    await outcome(store, run, 1, tokens=2001, cost=4401)
                    assert await h.sql("SELECT enabled FROM public_control") is False
                    return
                await outcome(store, run, 1, "KNOWN_FAILURE", True, 0, 0)
                await store.authorize(run, digest("retry"), 8000, version)
                await outcome(store, run, 2, "KNOWN_FAILURE", True, 0, 0)
            with pytest.raises(DBAPIError):
                await store.authorize(run, digest("deny"), 8000, version)

    asyncio.run(check())


@pytest.mark.parametrize(
    "decisions",
    [
        [Decision.COMPLETE],
        [Decision.VERIFY_REQUIRED, Decision.CORRECTABLE_DEFECT, Decision.COMPLETE],
    ],
)
def test_luna_pipeline_through_p1_5_capability_and_local_sdk(l2_url, decisions):
    from dataclasses import replace

    from fake_responses_server import FakeResponsesServer, final_message, response_body
    from luna_capabilities import execution_for

    from aiscc.providers.openai_responses import OpenAIResponsesAdapter
    from aiscc.public_live.provider_pipeline import PublicProviderPipeline
    from tests.unit.providers.test_luna_profile import call

    class Validator:
        async def validate(self, run, request, result):
            decision = decisions[request["semantic_ordinal"] - 1]
            return Validation(
                decision,
                digest((run, decision)),
                "SUMMARY_MISMATCH" if decision is Decision.CORRECTABLE_DEFECT else None,
            )

    async def check(server):
        async with harness(l2_url) as h:
            run, store, version = await setup(h)
            owner = (await store.context(run))["owner_binding"]
            for n in range(len(decisions)):
                server.enqueue(response_body("completed", [final_message()]))
                request = replace(
                    call(),
                    work_run_id=owner,
                    operation_id=f"op-{n}",
                    operation_fingerprint=digest(n).hex(),
                )
                adapter = OpenAIResponsesAdapter()
                executions = []

                def prepare(prepared, ticket, adapter=adapter, executions=executions):
                    bound = execution_for(prepared, ticket, adapter)
                    executions.append(bound)
                    return bound[:3]

                pipeline = PublicProviderPipeline(
                    PipelineStore(h.runtime, h.reconciler), Validator()
                )
                result = await pipeline.step(run, request, prepare)
                assert result.output_text == "AISCC_FAKE_FINAL"
                assert executions[0][3].invocation_count == 1 and adapter.invocation_count == 1
                assert await pipeline.step(run, request, prepare) is None
                assert len(executions) == 1
            assert (await store.context(run))["pipeline"]["completed"]
            assert len(server.requests) == len(decisions)
            assert [r["reasoning"]["effort"] for r in server.requests] == (
                ["low"] if len(decisions) == 1 else ["low", "low", "medium"]
            )

    with FakeResponsesServer() as server:
        asyncio.run(check(server))


@pytest.mark.parametrize("failure", ["known-closed", "unknown", "wall"])
def test_runtime_failure_retry_and_hard_wall(l2_url, failure, monkeypatch):
    import time
    from dataclasses import replace
    from types import MappingProxyType

    from luna_capabilities import execution_for

    from aiscc.providers.models import ExecutionOperationOutcome, ProviderResult
    from aiscc.public_live.provider_pipeline import PublicProviderPipeline
    from tests.unit.providers.test_luna_profile import call

    class Adapter:
        def __init__(self):
            self.calls = 0

        def call(self, request, *, secret):
            assert secret == "synthetic-local-only"
            self.calls += 1
            if failure == "unknown":
                raise TimeoutError("synthetic transport unknown")
            if failure == "wall":
                time.sleep(0.08)
            closed = failure == "known-closed" and self.calls == 1
            return ProviderResult(
                request.operation_id,
                "failed" if closed else "completed",
                ExecutionOperationOutcome.DEFINITELY_NOT_SENT
                if closed
                else ExecutionOperationOutcome.PROVIDER_COMPLETED,
                None if closed else "local-response",
                (),
                "fixed",
                None,
                MappingProxyType(
                    {"input_tokens": 0 if closed else 1, "output_tokens": 0 if closed else 1}
                ),
                None,
                digest(request.operation_id).hex(),
            )

    class Validator:
        async def validate(self, run, request, result):
            return Validation(Decision.COMPLETE, digest("server-complete"))

    if failure == "wall":
        original = asyncio.wait_for

        async def deterministic_wall(awaitable, timeout):
            assert timeout == 35
            return await original(awaitable, timeout=0.02)

        monkeypatch.setattr("aiscc.public_live.provider_pipeline.wait_for", deterministic_wall)

    async def check():
        async with harness(l2_url) as h:
            run, store, version = await setup(h)
            owner = (await store.context(run))["owner_binding"]
            request = replace(call(), work_run_id=owner)
            adapter = Adapter()
            pipeline = PublicProviderPipeline(store, Validator())

            def prepare(prepared, ticket):
                return execution_for(prepared, ticket, adapter)[:3]

            if failure == "known-closed":
                await pipeline.step(run, request, prepare)
                second = replace(
                    request, operation_id="retry", operation_fingerprint=digest("retry").hex()
                )
                await pipeline.step(run, second, prepare)
                context = await store.context(run)
                assert context["pipeline"]["completed"]
                assert context["requests"][1]["retry_of"] == 1
                assert context["requests"][1]["effort"] == "low"
                assert adapter.calls == 2
            else:
                with pytest.raises(TimeoutError):
                    await pipeline.step(run, request, prepare)
                context = await store.context(run)
                assert context["requests"][0]["outcome"] == "UNKNOWN"
                assert context["settlement"]["committed_max"] == 4400
                with pytest.raises(DBAPIError):
                    await pipeline.step(
                        run, replace(request, operation_fingerprint=digest("retry").hex()), prepare
                    )
                assert adapter.calls == 1

    asyncio.run(check())
