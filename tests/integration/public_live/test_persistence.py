"""Real PostgreSQL L1 proofs. All campaign activation here is test-only."""

from __future__ import annotations

import asyncio
import hashlib
import os
import subprocess
from contextlib import asynccontextmanager
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import DBAPIError

from aiscc.persistence.database import create_engine, create_session_factory
from aiscc.persistence.public_live import (
    Observation,
    ObservationKind,
    PersistRun,
    PublicLiveRepository,
    PublicLiveTransaction,
)

pytestmark = pytest.mark.postgres
DIGEST = b"d" * 32


@asynccontextmanager
async def denied(session):
    with pytest.raises(DBAPIError):
        async with session.begin_nested():
            yield


async def fixture(session):
    campaign = uuid4().hex
    await session.execute(
        text("""INSERT INTO public_campaign
        (campaign_id,starts_at,ends_at,available,hmac_version,scenario_id,scenario_version,
         content_digest,policy_digest) VALUES(:c,clock_timestamp()-interval '1 hour',
         clock_timestamp()+interval '1 day',15000000,'test','stockroom-s1-normal','1.0.0',:d,:d)
        """),
        {"c": campaign, "d": DIGEST},
    )
    await session.execute(
        text("""UPDATE public_control SET enabled=true,incident=NULL,
        last_clock=NULL,active_campaign=:c,policy_digest=:d WHERE id=1"""),
        {"c": campaign, "d": DIGEST},
    )
    now = await session.scalar(text("SELECT public_live_api.clock_lock()"))
    tx = PublicLiveTransaction(session, now)
    run = PersistRun(
        uuid4().bytes,
        campaign,
        DIGEST,
        uuid4().bytes * 2,
        hashlib.sha256(uuid4().bytes).digest(),
        DIGEST,
        1,
    )
    return tx, run


def scenario(action):
    async def run():
        engine = create_engine(os.environ["AISCC_TEST_DATABASE_URL"])
        try:
            async with create_session_factory(engine)() as session:
                transaction = await session.begin()
                try:
                    await action(session)
                finally:
                    await transaction.rollback()
        finally:
            await engine.dispose()

    asyncio.run(run())


def test_initialization():
    async def check(s):
        assert (
            await s.execute(text("SELECT enabled,active_campaign FROM public_control"))
        ).one() == (False, None)
        assert (
            await s.execute(text("SELECT slot_id,state,run_id FROM public_slot ORDER BY slot_id"))
        ).all() == [(1, "FREE", None), (2, "FREE", None)]
        assert await s.scalar(text("SELECT count(*) FROM public_campaign")) == 0
        names = set(
            (
                await s.execute(
                    text(
                        "SELECT tablename FROM pg_tables WHERE schemaname='public' "
                        "AND tablename LIKE 'public_%'"
                    )
                )
            ).scalars()
        )
        assert "public_live_shared_limit" in names
        assert "public_live_limiter_maintenance" in names
        assert len(names) == 15

    scenario(check)


@pytest.mark.parametrize("kind", ["key", "read", "run", "slot", "third"])
def test_identity_and_slot_uniqueness(kind):
    async def check(s):
        tx, run = await fixture(s)
        await tx.persist_run(run)
        other = replace(
            run,
            run_id=uuid4().bytes,
            key_hash=uuid4().bytes * 2,
            read_hash=uuid4().bytes * 2,
            slot_id=2,
        )
        if kind == "key":
            other = replace(other, key_hash=run.key_hash)
        if kind == "read":
            other = replace(other, read_hash=run.read_hash)
        if kind == "run":
            other = replace(other, run_id=run.run_id)
        if kind == "slot":
            other = replace(other, slot_id=1)
        async with denied(s):
            if kind == "third":
                await s.execute(text("INSERT INTO public_slot(slot_id) VALUES(3)"))
            else:
                await tx.persist_run(other)
        assert await s.scalar(text("SELECT count(*) FROM public_run")) == 1
        assert (
            await s.scalar(
                text("SELECT held FROM public_campaign WHERE campaign_id=:c"),
                {"c": run.campaign_id},
            )
            == 200000
        )

    scenario(check)


@pytest.mark.parametrize(
    "sql",
    [
        "UPDATE public_campaign SET available=-1,held=15000001 WHERE campaign_id=:c",
        "UPDATE public_day SET held=-1,available=4000001 WHERE campaign_id=:c",
        "UPDATE public_reservation SET committed_max=200001 WHERE run_id=:r",
        "UPDATE public_reservation SET settled_cost=1,state='SETTLED' WHERE run_id=:r",
        "UPDATE public_reservation SET provisional=-1 WHERE run_id=:r",
        "INSERT INTO public_money_event SELECT * FROM public_money_event WHERE run_id=:r",
        "DELETE FROM public_money_event WHERE run_id=:r",
        "DELETE FROM public_slot WHERE slot_id=2",
        "UPDATE public_campaign SET hmac_version='changed' WHERE campaign_id=:c",
    ],
)
def test_money_append_only_and_fixed_slots(sql):
    async def check(s):
        tx, run = await fixture(s)
        await tx.persist_run(run)
        async with denied(s):
            await s.execute(text(sql), {"r": run.run_id, "c": run.campaign_id})

    scenario(check)


def test_disabled_gate_and_transaction_rollback():
    async def check(s):
        tx, run = await fixture(s)
        await s.execute(text("UPDATE public_control SET enabled=false"))
        async with denied(s):
            await tx.persist_run(run)
        assert await s.scalar(text("SELECT count(*) FROM public_run")) == 0
        await s.execute(text("UPDATE public_control SET enabled=true"))
        nested = await s.begin_nested()
        await tx.persist_run(run)
        await nested.rollback()
        for name in [
            "public_run",
            "public_idempotency",
            "public_rate_event",
            "public_reservation",
            "public_outbox",
            "public_money_event",
        ]:
            assert await s.scalar(text("SELECT count(*) FROM " + name)) == 0
        assert (
            await s.scalar(
                text("SELECT held FROM public_campaign WHERE campaign_id=:c"),
                {"c": run.campaign_id},
            )
            == 0
        )

    scenario(check)


def test_clock_regression_utc_and_safe_replay_clock():
    async def check(s):
        tx, run = await fixture(s)
        await tx.persist_run(run)
        admitted, deadline, expires = (
            await s.execute(
                text("SELECT admitted_at,deadline,read_expires FROM public_run WHERE run_id=:r"),
                {"r": run.run_id},
            )
        ).one()
        assert admitted.utcoffset() == timedelta(0)
        assert deadline - admitted == timedelta(seconds=90)
        assert expires - admitted == timedelta(hours=24)
        future = datetime.now(UTC) + timedelta(days=1)
        await s.execute(text("UPDATE public_control SET last_clock=:f"), {"f": future})
        assert await s.scalar(text("SELECT public_live_api.clock_lock()")) == future
        assert (
            await s.execute(text("SELECT enabled,incident,last_clock FROM public_control"))
        ).one() == (False, "CLOCK_REGRESSION", future)
        binding = await tx.read_idempotency(run.campaign_id, run.key_hash)
        assert binding is not None
        async with denied(s):
            await tx.persist_run(
                replace(
                    run,
                    run_id=uuid4().bytes,
                    key_hash=uuid4().bytes * 2,
                    read_hash=uuid4().bytes * 2,
                    slot_id=2,
                )
            )

    scenario(check)


def test_dispatch_constraints_and_generation():
    async def check(s):
        tx, run = await fixture(s)
        await tx.persist_run(run)
        async with denied(s):
            await tx.mark_dispatch(run.run_id, 1, 1, 60000)
        # Test-only trusted owner composition; L2 must provide real owner binding.
        await s.execute(
            text(
                "UPDATE public_outbox SET state='BOUND',owner_binding='test-owner' WHERE run_id=:r"
            ),
            {"r": run.run_id},
        )
        for ordinal, generation in [(3, 1), (1, 2), (2, 1)]:
            async with denied(s):
                await tx.mark_dispatch(run.run_id, generation, ordinal, 60000)
        await tx.mark_dispatch(run.run_id, 1, 1, 60000)
        async with denied(s):
            await tx.mark_dispatch(run.run_id, 1, 1, 60000)
        await s.execute(
            text("UPDATE public_dispatch SET state='KNOWN_FAILURE' WHERE run_id=:r"),
            {"r": run.run_id},
        )
        async with denied(s):
            await tx.mark_dispatch(run.run_id, 1, 2, 150000)
        await tx.mark_dispatch(run.run_id, 1, 2, 60000)
        assert (
            await s.scalar(
                text("SELECT committed_max FROM public_reservation WHERE run_id=:r"),
                {"r": run.run_id},
            )
            == 120000
        )

    scenario(check)


def test_observation_identity_settlement_and_quarantine():
    async def check(s):
        tx, run = await fixture(s)
        await tx.persist_run(run)
        await tx.heartbeat(run.run_id, 1)
        await tx.quarantine(run.run_id, 1)
        async with denied(s):
            await tx.heartbeat(run.run_id, 1)
        o = Observation(uuid4().bytes, run.run_id, DIGEST, ObservationKind.UNKNOWN, DIGEST)
        await tx.observe(o)
        async with denied(s):
            await tx.observe(replace(o, observation_id=uuid4().bytes))
        async with denied(s):
            await tx.settle(run.run_id, 0, DIGEST)
        async with denied(s):
            await tx.observe(replace(o, classification=ObservationKind.CLOSURE))
        assert (await tx.read_outbox(run.run_id)).state == "PENDING"
        await tx.fence(run.run_id, 1)
        # Privileged fixture stands for a separately admitted closure, not real runtime proof.
        await tx.admit_closure(run.run_id, 2, 0, DIGEST, uuid4().bytes * 2)
        assert await tx.settle(run.run_id, 0, DIGEST)
        assert not await tx.settle(run.run_id, 0, DIGEST)
        async with denied(s):
            await tx.settle(run.run_id, 1, DIGEST)
        assert (
            await s.scalar(
                text("SELECT count(*) FROM public_money_event WHERE event_kind='SETTLE'")
            )
            == 1
        )
        assert (
            await s.scalar(
                text("SELECT available FROM public_campaign WHERE campaign_id=:c"),
                {"c": run.campaign_id},
            )
            == 15000000
        )
        assert await s.scalar(text("SELECT state FROM public_slot WHERE slot_id=1")) == "FREE"
        await tx.observe(
            replace(
                o,
                observation_id=uuid4().bytes,
                source_identity=uuid4().bytes * 2,
                classification=ObservationKind.LATE_USAGE,
            )
        )
        assert (
            await s.scalar(
                text("SELECT count(*) FROM public_money_event WHERE event_kind='SETTLE'")
            )
            == 1
        )

    scenario(check)


def test_runtime_permissions_and_above_bound_incident():
    async def check(s):
        tx, run = await fixture(s)
        await s.execute(text("SET LOCAL ROLE aiscc_public_live_runtime"))
        await tx.persist_run(run)
        for sql in [
            "UPDATE public_control SET enabled=true",
            "DELETE FROM public_money_event",
            "INSERT INTO public_slot(slot_id) VALUES(3)",
            "SELECT * FROM work_runs",
        ]:
            async with denied(s):
                await s.execute(text(sql))
        await tx.observe(
            Observation(
                uuid4().bytes, run.run_id, uuid4().bytes * 2, ObservationKind.ABOVE_BOUND, DIGEST
            )
        )
        await s.execute(text("RESET ROLE"))
        assert await s.scalar(text("SELECT incident FROM public_control")) == "ABOVE_BOUND_USAGE"
        assert await s.scalar(text("SELECT state FROM public_slot WHERE slot_id=1")) == "SUSPECT"

    scenario(check)


def test_two_connection_control_lock_serialization():
    async def check():
        engine = create_engine(os.environ["AISCC_TEST_DATABASE_URL"])
        sessions = create_session_factory(engine)
        repo = PublicLiveRepository(sessions)
        attempted = asyncio.Event()
        acquired = asyncio.Event()

        async def second():
            attempted.set()
            async with repo.transaction():
                acquired.set()

        try:
            async with repo.transaction():
                task = asyncio.create_task(second())
                await attempted.wait()
                # PostgreSQL reports the second transaction actually waiting on a lock.
                async with engine.connect() as c:
                    for _ in range(100):
                        waiting = await c.scalar(
                            text(
                                "SELECT count(*) FROM pg_stat_activity "
                                "WHERE datname=current_database() AND wait_event_type='Lock'"
                            )
                        )
                        if waiting:
                            break
                        await asyncio.sleep(0.01)
                    assert waiting and not acquired.is_set()
            await asyncio.wait_for(task, 5)
            assert acquired.is_set()
        finally:
            await engine.dispose()

    asyncio.run(check())


def test_trusted_reconciliation_known_cost_and_denials():
    async def check(s):
        tx, run = await fixture(s)
        await tx.persist_run(run)
        async with denied(s):
            await tx.bind_owner(run.run_id, 1, "nonexistent-owner")
        async with denied(s):
            await s.execute(
                text(
                    "UPDATE public_slot SET run_id=:r,state='OCCUPIED',"
                    "heartbeat_at=transaction_timestamp(),"
                    "expires_at=transaction_timestamp()+interval '15 seconds' WHERE slot_id=2"
                ),
                {"r": run.run_id},
            )
        await s.execute(
            text("UPDATE public_outbox SET state='BOUND',owner_binding='fixture' WHERE run_id=:r"),
            {"r": run.run_id},
        )
        await tx.mark_dispatch(run.run_id, 1, 1, 60000)
        await s.execute(text("SET LOCAL ROLE aiscc_public_live_runtime"))
        async with denied(s):
            await tx.admit_closure(run.run_id, 1, 0, DIGEST, uuid4().bytes * 2)
        async with denied(s):
            await tx.record_outcome(
                run.run_id, 1, ObservationKind.KNOWN_SUCCESS, 10000, DIGEST, uuid4().bytes * 2
            )
        await s.execute(text("RESET ROLE"))
        await s.execute(text("SET LOCAL ROLE aiscc_public_live_reconciler"))
        await tx.record_outcome(
            run.run_id, 1, ObservationKind.KNOWN_SUCCESS, 10000, DIGEST, uuid4().bytes * 2
        )
        async with denied(s):
            await tx.admit_closure(run.run_id, 1, 10000, DIGEST, uuid4().bytes * 2)
        await tx.fence(run.run_id, 1)
        async with denied(s):
            await tx.admit_closure(run.run_id, 2, 0, DIGEST, uuid4().bytes * 2)
        await tx.admit_closure(run.run_id, 2, 10000, DIGEST, uuid4().bytes * 2)
        assert await tx.settle(run.run_id, 10000, DIGEST)
        await s.execute(text("RESET ROLE"))
        assert (
            await s.execute(
                text("SELECT available,held,settled FROM public_campaign WHERE campaign_id=:c"),
                {"c": run.campaign_id},
            )
        ).one() == (14990000, 0, 10000)

    scenario(check)


def test_migration_paths_and_owner_preservation():
    base = os.environ["AISCC_TEST_DATABASE_URL"]
    parsed = make_url(base)
    assert parsed.host == "127.0.0.1"

    def migrate(url, revision):
        result = subprocess.run(
            [
                str(Path.cwd() / ".venv/Scripts/python.exe"),
                "-B",
                "-m",
                "alembic",
                "upgrade",
                revision,
            ],
            env=os.environ | {"AISCC_DATABASE_URL": url, "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr.replace(url, "<TEST_DB>")

    async def admin(command):
        engine = create_engine(base)
        try:
            async with engine.connect() as conn:
                conn = await conn.execution_options(isolation_level="AUTOCOMMIT")
                await conn.execute(text(command))
        finally:
            await engine.dispose()

    async def snapshot(url, seed=False):
        engine = create_engine(url)
        try:
            async with engine.begin() as conn:
                if seed:
                    await conn.execute(
                        text(
                            "INSERT INTO work_runs VALUES('l1-owner-history',"
                            "'p','t','1','READY',1,'OWNER_SELF_DOGFOOD',"
                            "'2026-09-01T00:00:00Z','2026-09-01T00:00:00Z')"
                        )
                    )
                owner = (
                    (
                        await conn.execute(
                            text("SELECT to_jsonb(w) FROM work_runs w ORDER BY work_run_id")
                        )
                    )
                    .scalars()
                    .all()
                )
                rev = await conn.scalar(text("SELECT version_num FROM alembic_version"))
                if rev == "20260916_0016":
                    assert (
                        await conn.execute(
                            text("SELECT enabled,active_campaign FROM public_control")
                        )
                    ).one() == (False, None)
                    assert (
                        await conn.execute(
                            text("SELECT slot_id,state,run_id FROM public_slot ORDER BY slot_id")
                        )
                    ).all() == [(1, "FREE", None), (2, "FREE", None)]
                    assert await conn.scalar(text("SELECT count(*) FROM public_campaign")) == 0
                return owner, rev
        finally:
            await engine.dispose()

    for upgrade in [False, True]:
        name = "aiscc_l1_migration_" + uuid4().hex
        url = parsed.set(database=name).render_as_string(hide_password=False)
        asyncio.run(admin('CREATE DATABASE "' + name + '"'))
        try:
            before = []
            if upgrade:
                migrate(url, "20260914_0012")
                before, rev = asyncio.run(snapshot(url, seed=True))
                assert rev == "20260914_0012"
            migrate(url, "head")
            after, rev = asyncio.run(snapshot(url))
            assert rev == "20260916_0016" and after == before
        finally:
            asyncio.run(admin('DROP DATABASE "' + name + '"'))
