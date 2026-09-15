"""Real PostgreSQL, independent pools, concurrent fixed-bucket boundaries."""

import asyncio
import hashlib
from contextlib import asynccontextmanager

import pytest
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from aiscc.persistence.database import create_engine, create_session_factory
from aiscc.persistence.public_live import PublicLiveRepository, PublicLiveTransaction
from aiscc.persistence.public_live_limits import LimitsUnavailable, PublicLiveLimits, ReadNotFound
from tests.integration.public_live.test_service import harness

pytestmark = pytest.mark.postgres


def test_shared_caps_concurrency_isolation_and_permissions(l2_url):
    async def check():
        async with harness(l2_url) as h:
            await h.clock("2026-09-16T12:00:20+00:00")
            other = create_engine(h.engines[0].url.render_as_string(hide_password=False))
            pids = set()
            ready = asyncio.Event()

            class ObservedRepository(PublicLiveRepository):
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
                PublicLiveLimits(ObservedRepository(create_session_factory(e)))
                for e in (h.engines[0], other)
            ]
            sem = asyncio.Semaphore(16)

            async def flood(i, source):
                async with sem:
                    return await services[i % 2].flood(h.campaign, "v1", source)

            async def read(i, receipt):
                async with sem:
                    return (await services[i % 2].read(receipt.run_id, receipt.read_capability))[0]

            try:
                source = hashlib.sha256(b"source-one").digest()
                results = await asyncio.gather(*(flood(i, source) for i in range(121)))
                assert len(pids) >= 2
                assert sum(r.allowed for r in results) == 120
                assert all(r.retry_after == 40 for r in results)
                assert len({r.bucket for r in results}) == 1
                assert (
                    await h.sql("SELECT attempts FROM public_live_shared_limit WHERE kind='SOURCE'")
                    == 121
                )
                assert (
                    await h.sql(
                        "SELECT attempts FROM public_live_shared_limit WHERE kind='CAMPAIGN'"
                    )
                    == 121
                )
                assert (await flood(0, hashlib.sha256(b"source-two").digest())).allowed
                assert await h.sql("SELECT count(*) FROM public_run") == 0
                assert await h.sql("SELECT held FROM public_campaign") == 0

                await h.clock("2026-09-16T12:01:00+00:00")
                assert (await flood(0, source)).allowed
                # New bucket: 1200 simultaneous attempts distributed over 12 sources,
                # plus the already allowed first request. Campaign is the binding cap.
                results = await asyncio.gather(
                    *(flood(i, hashlib.sha256(str(i % 12).encode()).digest()) for i in range(1200))
                )
                assert sum(r.allowed for r in results) == 1199
                assert all(r.retry_after == 60 for r in results)
                assert (
                    await h.sql(
                        "SELECT max(attempts) FROM public_live_shared_limit WHERE kind='CAMPAIGN'"
                    )
                    == 1201
                )

                await h.clock("2026-09-16T12:02:00+00:00")
                receipt = await h.admit()
                second = await h.admit(ip="1.1.1.1")
                results = await asyncio.gather(*(read(i, receipt) for i in range(31)))
                assert sum(r.allowed for r in results) == 30
                assert not (await read(0, receipt)).allowed
                assert (await read(1, second)).allowed
                for token in (b"", b"x" * 32, second.read_capability):
                    with pytest.raises(ReadNotFound):
                        await services[0].read(receipt.run_id, token)
                with pytest.raises(ReadNotFound):
                    await services[1].read(b"z" * 16, receipt.read_capability)
                assert (
                    await h.sql(
                        "SELECT sum(attempts) FROM public_live_shared_limit WHERE kind='READ'"
                    )
                    == 33
                )
                await h.clock("2026-09-16T12:03:00+00:00")
                assert (await read(1, receipt)).allowed
                await h.clock("2026-09-17T12:02:00+00:00")
                with pytest.raises(ReadNotFound):
                    await services[0].read(receipt.run_id, receipt.read_capability)

                for sql in (
                    "SELECT * FROM public.public_live_shared_limit",
                    "UPDATE public.public_live_shared_limit SET attempts=1",
                    "DELETE FROM public.public_live_shared_limit",
                    "INSERT INTO public.public_live_shared_limit VALUES('x','CAMPAIGN',"
                    "''::bytea,1,1)",
                    "TRUNCATE public.public_live_shared_limit",
                ):
                    async with h.engines[0].begin() as conn:
                        with pytest.raises(DBAPIError) as denied:
                            await conn.execute(text(sql))
                        assert denied.value.orig.sqlstate == "42501"
                assert await h.sql("SELECT count(*) FROM public_run") == 2
                assert await h.sql("SELECT count(*) FROM public_dispatch") == 0
            finally:
                await other.dispose()

    asyncio.run(check())


def test_campaign_isolation_atomic_pair_failure_and_clock_regression(l2_url):
    async def check():
        async with harness(l2_url) as h:
            await h.clock("2026-09-16T12:00:59.500000+00:00")
            limiter = PublicLiveLimits(h.runtime)
            source = hashlib.sha256(b"opaque-source").digest()
            first = await limiter.flood(h.campaign, "v1", source)
            assert first.allowed and first.retry_after == 1
            await h.sql(
                """INSERT INTO public_campaign
                (campaign_id,starts_at,ends_at,available,hmac_version,scenario_id,scenario_version,
                 content_digest,policy_digest)
                SELECT 'second-campaign',starts_at,ends_at,available,hmac_version,scenario_id,
                scenario_version,content_digest,policy_digest FROM public_campaign
                WHERE campaign_id=:c""",
                c=h.campaign,
            )
            assert (await limiter.flood("second-campaign", "v1", source)).allowed
            assert (
                await h.sql("SELECT count(*) FROM public_live_shared_limit WHERE kind='CAMPAIGN'")
                == 2
            )
            # Deliberately fail the second write after the first increment: entire pair rolls back.
            await h.sql(
                "UPDATE public_live_shared_limit SET attempts=9223372036854775807 "
                "WHERE campaign_id=:c AND kind='SOURCE'",
                c=h.campaign,
            )
            with pytest.raises(LimitsUnavailable):
                await limiter.flood(h.campaign, "v1", source)
            assert (
                await h.sql(
                    "SELECT attempts FROM public_live_shared_limit "
                    "WHERE campaign_id=:c AND kind='CAMPAIGN'",
                    c=h.campaign,
                )
                == 1
            )
            for campaign, version, key in (
                (h.campaign, "wrong", source),
                ("missing", "v1", source),
                (h.campaign, "v1", b"bad"),
            ):
                with pytest.raises(LimitsUnavailable):
                    await limiter.flood(campaign, version, key)
            assert await h.sql("SELECT count(*) FROM public_live_shared_limit") == 4
            await h.clock("2026-09-16T12:01:00+00:00")
            next_bucket = await limiter.flood(h.campaign, "v1", source)
            assert next_bucket.allowed and next_bucket.bucket == first.bucket + 1
            await h.clock("2026-09-16T12:00:00+00:00")
            regressed = await limiter.flood(h.campaign, "v1", source)
            assert regressed.bucket == next_bucket.bucket
            assert not await h.sql("SELECT enabled FROM public_control")
            assert await h.sql("SELECT count(*) FROM public_run") == 0

    asyncio.run(check())
