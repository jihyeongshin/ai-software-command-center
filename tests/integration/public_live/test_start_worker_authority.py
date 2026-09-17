from __future__ import annotations

import asyncio
import hashlib
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from sqlalchemy import text

from aiscc.persistence.database import create_engine, create_session_factory
from aiscc.public_live.initializer import create_initializer
from aiscc.public_live.start_authority import PublicLiveStartCandidate, StartContract
from aiscc.public_live.start_repository import StartRepository

pytestmark = pytest.mark.postgres


def test_start_roles_are_exact_and_no_raw_worker_initialization_dml(l2_url) -> None:
    async def check() -> None:
        engine = create_engine(l2_url)
        try:
            async with engine.connect() as connection:
                values = (
                    await connection.execute(
                        text(
                            "SELECT "
                            "has_function_privilege('aiscc_public_live_initializer',"
                            "'public_live_api.start_next(bytea)','EXECUTE'),"
                            "has_function_privilege('aiscc_public_live_execution',"
                            "'public_live_api.start_next(bytea)','EXECUTE'),"
                            "has_function_privilege('aiscc_public_live_runtime',"
                            "'public_live_api.start_register_from_admission(bytea,bytea,jsonb)',"
                            "'EXECUTE'),"
                            "has_table_privilege('aiscc_public_live_execution',"
                            "'public.work_runs','INSERT'),"
                            "has_table_privilege('aiscc_public_live_initializer',"
                            "'public.work_runs','INSERT'),"
                            "has_table_privilege('aiscc_public_live_initializer',"
                            "'public.execution_operations','INSERT')"
                        )
                    )
                ).one()
                assert values == (True, False, False, False, True, False)
                role = (
                    await connection.execute(
                        text(
                            "SELECT rolcanlogin,rolsuper,rolcreatedb,rolcreaterole,"
                            "rolinherit,rolbypassrls FROM pg_roles "
                            "WHERE rolname='aiscc_public_live_initializer'"
                        )
                    )
                ).one()
                assert role == (False, False, False, False, False, False)
        finally:
            await engine.dispose()

    asyncio.run(check())


def test_two_worker_instances_share_one_authoritative_claim(l2_url) -> None:
    async def check() -> None:
        engine = create_engine(l2_url)
        sessions = create_session_factory(engine)
        run_id = uuid4().bytes
        work_id = "public-live-" + run_id.hex()
        attempt_id = "attempt-" + uuid4().hex
        campaign = "campaign-" + uuid4().hex
        digest = hashlib.sha256(run_id).digest()
        try:
            async with sessions() as session, session.begin():
                await session.execute(
                    text(
                        "INSERT INTO public_campaign(campaign_id,starts_at,ends_at,available,"
                        "hmac_version,scenario_id,scenario_version,content_digest,policy_digest) "
                        "VALUES(:c,clock_timestamp()-interval '1 hour',"
                        "clock_timestamp()+interval '1 day',15000000,'test',"
                        "'stockroom-s1-normal','1.0.0',:d,:d)"
                    ),
                    {"c": campaign, "d": digest},
                )
                await session.execute(
                    text(
                        "INSERT INTO public_day(campaign_id,utc_date) "
                        "VALUES(:c,(clock_timestamp() at time zone 'UTC')::date)"
                    ),
                    {"c": campaign},
                )
                await session.execute(
                    text(
                        "INSERT INTO public_client VALUES(:c,:d,'test',clock_timestamp(),"
                        "clock_timestamp()+interval '1 day')"
                    ),
                    {"c": campaign, "d": digest},
                )
                await session.execute(
                    text(
                        "INSERT INTO public_run(run_id,campaign_id,utc_date,bucket_hash,"
                        "admitted_at,deadline,read_expires,state,owner_binding,read_hash,"
                        "policy_digest,payload_digest,scenario_digest) "
                        "SELECT :r,:c,(n.t at time zone 'UTC')::date,:d,n.t,"
                        "n.t+interval '90 seconds',n.t+interval '24 hours',"
                        "'ADMITTED',:w,:h,:d,:d,:d FROM (SELECT clock_timestamp() t) n"
                    ),
                    {"r": run_id, "c": campaign, "d": digest, "w": work_id, "h": uuid4().bytes * 2},
                )
                await session.execute(
                    text("INSERT INTO public_outbox VALUES(:r,'BOUND',1,:w,NULL)"),
                    {"r": run_id, "w": work_id},
                )
                await session.execute(
                    text(
                        "INSERT INTO work_runs VALUES(:w,'repository:synthetic-stockroom',"
                        "'aiscc-public-live-stockroom-v1','1','RUNNING',2,"
                        "'PUBLIC_BOUNDED_LIVE',clock_timestamp(),clock_timestamp())"
                    ),
                    {"w": work_id},
                )
                await session.execute(
                    text(
                        "INSERT INTO execution_attempts(execution_attempt_id,work_run_id,"
                        "attempt_ordinal,parent_attempt_id,task_contract_id,task_contract_version,"
                        "runtime_mode,provider_profile_id,provider_profile_version,tool_registry_id,"
                        "tool_registry_version,creation_state,creation_state_version,causal_state,"
                        "causal_state_version,status,execution_version,latest_event_sequence,counters,"
                        "created_at,updated_at) VALUES(:a,:w,1,NULL,"
                        "'aiscc-public-live-stockroom-v1','1','PUBLIC_BOUNDED_LIVE',"
                        "'public-live-luna-v1','1','aiscc-stockroom-tools','2','READY',1,"
                        "'RUNNING',2,'RUNNING',2,0,'{}',clock_timestamp(),clock_timestamp())"
                    ),
                    {"a": attempt_id, "w": work_id},
                )
                await session.execute(
                    text("SELECT public_live_api.execution_bind(:r,:w,:a,:d,:p)"),
                    {
                        "r": run_id,
                        "w": work_id,
                        "a": attempt_id,
                        "d": digest,
                        "p": hashlib.sha256(digest).digest(),
                    },
                )
                await session.execute(
                    text("SELECT public_live_api.worker_enroll(:r,:d)"),
                    {"r": run_id, "d": digest},
                )
                for marker in (b"1", b"2"):
                    await session.execute(
                        text("SELECT public_live_api.worker_register_instance(:w,:p)"),
                        {"w": marker * 16, "p": marker.upper() * 16},
                    )

            async def claim(marker: bytes):
                async with sessions() as session, session.begin():
                    return await session.scalar(
                        text("SELECT public_live_api.worker_claim_next(:w,:p,1,:h)"),
                        {
                            "w": marker * 16,
                            "p": marker.upper() * 16,
                            "h": hashlib.sha256(marker).digest(),
                        },
                    )

            first, second = await asyncio.gather(claim(b"1"), claim(b"2"))
            assert sorted(value["kind"] for value in (first, second)) == ["CLAIM", "EMPTY"]
        finally:
            await engine.dispose()

    asyncio.run(check())


def test_actual_initializer_runs_canonical_ready_start_attempt_and_binding(l2_url) -> None:
    async def check() -> None:
        engine = create_engine(l2_url)
        sessions = create_session_factory(engine)
        run_id = uuid4().bytes
        campaign = "campaign-" + uuid4().hex
        digest = hashlib.sha256(run_id).digest()
        admitted = datetime.now(UTC)
        contract = StartContract.load()
        try:
            async with sessions() as session, session.begin():
                await session.execute(
                    text(
                        "INSERT INTO public_campaign(campaign_id,starts_at,ends_at,available,"
                        "hmac_version,scenario_id,scenario_version,content_digest,policy_digest) "
                        "VALUES(:c,CAST(:n AS timestamptz)-interval '1 hour',"
                        "CAST(:n AS timestamptz)+interval '1 day',15000000,'test',"
                        "'stockroom-s1-normal','1.0.0',:d,:d)"
                    ),
                    {"c": campaign, "d": digest, "n": admitted},
                )
                await session.execute(
                    text("INSERT INTO public_day(campaign_id,utc_date) VALUES(:c,:u)"),
                    {"c": campaign, "u": admitted.date()},
                )
                await session.execute(
                    text(
                        "INSERT INTO public_client VALUES(:c,:d,'test',:n,"
                        "CAST(:n AS timestamptz)+interval '1 day')"
                    ),
                    {"c": campaign, "d": digest, "n": admitted},
                )
                await session.execute(
                    text(
                        "UPDATE public_control SET enabled=true,active_campaign=:c,"
                        "policy_digest=:d,incident=NULL WHERE id=1"
                    ),
                    {"c": campaign, "d": digest},
                )
                gate = await session.scalar(text("SELECT start_gate_version FROM public_control"))
                await session.execute(
                    text(
                        "INSERT INTO public_run(run_id,campaign_id,utc_date,bucket_hash,"
                        "admitted_at,deadline,read_expires,state,read_hash,policy_digest,"
                        "payload_digest,scenario_digest) VALUES(:r,:c,:u,:d,:n,"
                        "CAST(:n AS timestamptz)+interval '90 seconds',"
                        "CAST(:n AS timestamptz)+interval '24 hours','ADMITTED',:h,:d,:d,:d)"
                    ),
                    {
                        "r": run_id,
                        "c": campaign,
                        "u": admitted.date(),
                        "d": digest,
                        "n": admitted,
                        "h": uuid4().bytes * 2,
                    },
                )
                await session.execute(
                    text(
                        "INSERT INTO public_reservation(run_id,campaign_id,utc_date) "
                        "VALUES(:r,:c,:u)"
                    ),
                    {"r": run_id, "c": campaign, "u": admitted.date()},
                )
                await session.execute(
                    text(
                        "UPDATE public_slot SET run_id=:r,state='OCCUPIED',"
                        "heartbeat_at=statement_timestamp(),"
                        "expires_at=statement_timestamp()+interval "
                        "'15 seconds' WHERE slot_id=1"
                    ),
                    {"r": run_id},
                )
                await session.execute(
                    text("INSERT INTO public_outbox VALUES(:r,'PENDING',1,NULL,NULL)"),
                    {"r": run_id},
                )
            candidate = PublicLiveStartCandidate(
                run_id,
                campaign,
                gate,
                admitted,
                admitted + timedelta(seconds=90),
                "idempotency:" + digest.hex(),
                digest.hex(),
                "reservation:" + run_id.hex(),
                1,
                hashlib.sha256(b"opaque-requester").hexdigest(),
                digest.hex(),
                digest.hex(),
                contract.digest,
            )
            await StartRepository(sessions).register(candidate, contract)
            initializer = create_initializer({"AISCC_PUBLIC_LIVE_START_DATABASE_URL": l2_url})
            try:
                assert await initializer.step()
            finally:
                await initializer.close()
            async with sessions() as session:
                row = (
                    await session.execute(
                        text(
                            "SELECT s.phase,w.workflow_state,a.status,e.work_run_id "
                            "FROM public_start_request s JOIN work_runs w "
                            "ON w.work_run_id=s.work_run_id JOIN execution_attempts a "
                            "ON a.execution_attempt_id=s.execution_attempt_id "
                            "JOIN public_provider_execution e USING(run_id) WHERE s.run_id=:r"
                        ),
                        {"r": run_id},
                    )
                ).one()
                assert row == ("BOUND", "RUNNING", "RUNNING", "public-live-" + run_id.hex())
                assert (
                    await session.scalar(
                        text("SELECT count(*) FROM public_worker_work WHERE run_id=:r"),
                        {"r": run_id},
                    )
                    == 1
                )
        finally:
            await engine.dispose()

    asyncio.run(check())
