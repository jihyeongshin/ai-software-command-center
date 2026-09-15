"""Real DB retention/cardinality proofs; clocks and fault injection are test-owned."""

import asyncio
import hashlib
from contextlib import asynccontextmanager
from datetime import datetime

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from aiscc.persistence.database import create_engine, create_session_factory
from aiscc.persistence.public_live import PublicLiveRepository, PublicLiveTransaction
from aiscc.persistence.public_live_limits import LimitsUnavailable, PublicLiveLimits, ReadNotFound
from tests.integration.public_live.test_http import apps
from tests.integration.public_live.test_service import harness
from tests.public_live_http_helpers import call

pytestmark = pytest.mark.postgres
STAMP = "2026-09-16T12:00:20+00:00"
BUCKET = int(datetime.fromisoformat(STAMP).timestamp()) // 60
SOURCE = hashlib.sha256(b"test-owned-source").digest()


def test_ten_buckets_current_quota_and_once_per_bucket(l2_url):
    async def check():
        async with harness(l2_url) as h:
            await h.clock(STAMP)
            run = await h.admit()
            # Privileged fixture seeds expired history for all kinds; no row identities exported.
            for kind, identity in (("SOURCE", SOURCE), ("CAMPAIGN", b""), ("READ", run.run_id)):
                await h.sql(
                    """INSERT INTO public_live_shared_limit
                    SELECT :c,:k,:i,b,1
                    FROM generate_series(CAST(:old AS bigint),CAST(:current AS bigint)) AS b""",
                    c=h.campaign,
                    k=kind,
                    i=identity,
                    old=BUCKET - 12,
                    current=BUCKET,
                )
            limiter = PublicLiveLimits(h.runtime)
            result, _ = await limiter.read(run.run_id, run.read_capability)
            assert result.bucket == BUCKET and result.allowed
            assert await h.sql("SELECT count(*) FROM public_live_shared_limit") == 30
            assert await h.sql("SELECT count(DISTINCT bucket) FROM public_live_shared_limit") == 10
            assert await h.sql("SELECT min(bucket) FROM public_live_shared_limit") == BUCKET - 9
            assert await h.sql("SELECT max(bucket) FROM public_live_shared_limit") == BUCKET
            assert await h.sql("SELECT last_bucket FROM public_live_limiter_maintenance") == BUCKET
            before = await h.sql("SELECT xmin::text FROM public_live_limiter_maintenance")
            await h.sql(
                "UPDATE public_live_shared_limit SET attempts=30 WHERE kind='READ' AND bucket=:b",
                b=BUCKET,
            )
            assert not (await limiter.read(run.run_id, run.read_capability))[0].allowed
            await h.sql(
                "UPDATE public_live_shared_limit SET attempts=120 "
                "WHERE kind='SOURCE' AND bucket=:b",
                b=BUCKET,
            )
            assert not (await limiter.flood(h.campaign, "v1", SOURCE)).allowed
            assert await h.sql("SELECT xmin::text FROM public_live_limiter_maintenance") == before
            assert (
                await h.sql(
                    "SELECT attempts FROM public_live_shared_limit WHERE kind='READ' AND bucket=:b",
                    b=BUCKET,
                )
                == 31
            )
            assert (
                await h.sql(
                    "SELECT attempts FROM public_live_shared_limit "
                    "WHERE kind='SOURCE' AND bucket=:b",
                    b=BUCKET,
                )
                == 121
            )
            with pytest.raises(ReadNotFound):
                await limiter.read(run.run_id, b"wrong")
            assert (
                await h.sql("SELECT count(*) FROM public_live_shared_limit WHERE kind='READ'") == 10
            )
            await h.clock("2026-09-16T12:01:00+00:00")
            assert (await limiter.flood(h.campaign, "v1", SOURCE)).allowed
            assert await h.sql("SELECT min(bucket) FROM public_live_shared_limit") == BUCKET - 8
            assert await h.sql("SELECT count(DISTINCT bucket) FROM public_live_shared_limit") == 10
            assert await h.sql("SELECT count(*) FROM public_live_limiter_maintenance") == 1
            assert await h.sql("SELECT xmin::text FROM public_live_limiter_maintenance") != before

    asyncio.run(check())


def test_concurrent_cleanup_and_public_ingress_cardinality(l2_url):
    async def check():
        async with harness(l2_url) as h:
            await h.clock(STAMP)
            await h.sql(
                """INSERT INTO public_live_shared_limit VALUES(:c,'SOURCE',:s,:b,1)""",
                c=h.campaign,
                s=SOURCE,
                b=BUCKET - 10,
            )
            other = create_engine(h.engines[0].url.render_as_string(hide_password=False))
            pids, states = set(), set()
            ready = asyncio.Event()

            class Observed(PublicLiveRepository):
                @asynccontextmanager
                async def transaction(self):
                    async with self._sessions() as session, session.begin():
                        pids.add(await session.scalar(text("SELECT pg_backend_pid()")))
                        if len(pids) >= 2:
                            ready.set()
                        await asyncio.wait_for(ready.wait(), 20)
                        now = await session.scalar(text("SELECT public_live_api.clock_lock()"))
                        tx = PublicLiveTransaction(session, now)
                        try:
                            yield tx
                        finally:
                            tx._open = False

            services = [
                PublicLiveLimits(Observed(create_session_factory(e))) for e in (h.engines[0], other)
            ]
            semaphore = asyncio.Semaphore(16)

            async def consume(i):
                async with semaphore:
                    result = await services[i % 2].flood(
                        h.campaign, "v1", hashlib.sha256(str(i).encode()).digest()
                    )
                    states.add(
                        await h.sql("SELECT xmin::text FROM public_live_limiter_maintenance")
                    )
                    return result

            try:
                results = await asyncio.gather(*(consume(i) for i in range(1220)))
                assert len(pids) >= 2 and len(states) == 1
                assert sum(result.allowed for result in results) == 1200
                assert (
                    await h.sql("SELECT count(*) FROM public_live_shared_limit WHERE kind='SOURCE'")
                    == 1200
                )
                assert (
                    await h.sql(
                        "SELECT sum(attempts) FROM public_live_shared_limit WHERE kind='SOURCE'"
                    )
                    == 1200
                )
                assert (
                    await h.sql(
                        "SELECT attempts FROM public_live_shared_limit WHERE kind='CAMPAIGN'"
                    )
                    == 1220
                )
                assert await h.sql("SELECT min(bucket) FROM public_live_shared_limit") == BUCKET
                # No increment even for a previously materialized identity after global exhaustion.
                assert not (
                    await services[0].flood(h.campaign, "v1", hashlib.sha256(b"0").digest())
                ).allowed
                assert (
                    await h.sql(
                        "SELECT sum(attempts) FROM public_live_shared_limit WHERE kind='SOURCE'"
                    )
                    == 1200
                )
                assert await h.sql("SELECT count(*) FROM public_run") == 0
                assert await h.sql("SELECT held FROM public_campaign") == 0
            finally:
                await other.dispose()

    asyncio.run(check())


@pytest.mark.parametrize("fault", ["missing", "future", "prune_error"])
def test_maintenance_failure_http_no_side_effects(l2_url, fault, caplog):
    async def check():
        async with harness(l2_url) as h:
            await h.clock(STAMP)
            if fault == "missing":
                await h.sql("DELETE FROM public_live_limiter_maintenance")
            elif fault == "future":
                await h.sql(
                    "UPDATE public_live_limiter_maintenance SET last_bucket=:b", b=BUCKET + 1
                )
            else:
                await h.sql(
                    "INSERT INTO public_live_shared_limit VALUES(:c,'SOURCE',:s,:b,1)",
                    c=h.campaign,
                    s=SOURCE,
                    b=BUCKET - 10,
                )
                await h.sql("""CREATE FUNCTION public.test_prune_fault() RETURNS trigger
                    LANGUAGE plpgsql AS $$ BEGIN
                    RAISE EXCEPTION 'synthetic maintenance fault'; END $$""")
                await h.sql("""CREATE TRIGGER test_prune_fault
                    BEFORE DELETE ON public_live_shared_limit
                    FOR EACH ROW EXECUTE FUNCTION public.test_prune_fault()""")
            app = apps(h)

            class ForbiddenAdmission:
                async def admit(self, *args):
                    raise AssertionError("L2 must not be reached")

            app.admission = ForbiddenAdmission()
            result = await call(app)
            assert result["status"] == 503 and result["receives"] == 0
            assert result["json"] == {"error": {"code": "LIVE_UNAVAILABLE", "retryable": True}}
            for table in (
                "public_run",
                "public_outbox",
                "public_reservation",
                "public_rate_event",
                "public_dispatch",
            ):
                assert await h.sql("SELECT count(*) FROM " + table) == 0
            assert await h.sql("SELECT held FROM public_campaign") == 0
            assert (
                await h.sql("SELECT count(*) FROM public_live_shared_limit WHERE kind='CAMPAIGN'")
                == 0
            )
            # The authenticated READ path is also gated, independently of HTTP flood.
            run = await h.admit()
            with pytest.raises(LimitsUnavailable):
                await PublicLiveLimits(h.runtime).read(run.run_id, run.read_capability)
            assert (
                await h.sql("SELECT count(*) FROM public_live_shared_limit WHERE kind='READ'") == 0
            )
            assert "synthetic maintenance fault" not in caplog.text

    asyncio.run(check())


def test_raw_maintenance_and_unguarded_consumers_are_not_runtime_authority(l2_url):
    async def check():
        async with harness(l2_url) as h:
            for query in (
                "SELECT * FROM public_live_limiter_maintenance",
                "DELETE FROM public_live_limiter_maintenance",
                "UPDATE public_live_limiter_maintenance SET last_bucket=0",
                "INSERT INTO public_live_limiter_maintenance VALUES(1,0)",
                "TRUNCATE public_live_limiter_maintenance",
                "DELETE FROM public_live_shared_limit",
                "SELECT public_live_api.maintain_limiter()",
                "SELECT public_live_api.flood_consume('c','v',decode(repeat('00',32),'hex'))",
                "SELECT public_live_api.read_consume(decode(repeat('00',16),'hex'))",
            ):
                async with h.engines[0].begin() as conn:
                    with pytest.raises(DBAPIError) as failure:
                        await conn.execute(text(query))
                    assert failure.value.orig.sqlstate == "42501"

    asyncio.run(check())


@pytest.mark.parametrize("kind,transition_call", [("flood", 3), ("read", 5)])
def test_db_minute_rollover_inside_consume_refreshes_maintenance(l2_url, kind, transition_call):
    async def check():
        async with harness(l2_url) as h:
            await h.clock(STAMP)
            run = await h.admit()
            await h.sql(
                "INSERT INTO public_live_shared_limit VALUES(:c,'SOURCE',:s,:b,1)",
                c=h.campaign,
                s=SOURCE,
                b=BUCKET - 9,
            )
            await h.sql("CREATE TABLE public.test_clock_steps(step integer NOT NULL)")
            await h.sql("INSERT INTO public.test_clock_steps VALUES(0)")
            definition = await h.sql(
                "SELECT pg_get_functiondef('public_live_api.clock_lock()'::regprocedure)"
            )
            old = "now_at:='2026-09-16T12:00:20+00:00'::timestamptz;"
            assert old in definition
            replacement = (
                "UPDATE public.test_clock_steps SET step=step+1; "
                f"SELECT CASE WHEN step>={transition_call} "
                "THEN '2026-09-16T12:01:00Z'::timestamptz "
                "ELSE '2026-09-16T12:00:20Z'::timestamptz END "
                "INTO now_at FROM public.test_clock_steps;"
            )
            await h.sql(definition.replace(old, replacement))
            limiter = PublicLiveLimits(h.runtime)
            if kind == "flood":
                result = await limiter.flood(h.campaign, "v1", SOURCE)
            else:
                result, _ = await limiter.read(run.run_id, run.read_capability)
            assert result.allowed and result.bucket == BUCKET + 1
            assert (
                await h.sql("SELECT last_bucket FROM public_live_limiter_maintenance") == BUCKET + 1
            )
            assert await h.sql("SELECT min(bucket) FROM public_live_shared_limit") == BUCKET + 1
            assert await h.sql("SELECT step FROM public.test_clock_steps") > transition_call

    asyncio.run(check())
