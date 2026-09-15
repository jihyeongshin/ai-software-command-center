"""L2 PostgreSQL evidence: real transactions/owner kernel, synthetic external ports."""

import asyncio
import hashlib
import importlib.util
from contextlib import asynccontextmanager
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import DBAPIError

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.persistence.database import create_engine, create_session_factory
from aiscc.persistence.public_live import (
    ObservationKind,
    PersistRun,
    PublicLiveRepository,
    PublicLiveTransaction,
)
from aiscc.public_live.identity import AdmissionDenied, IdentityPolicy
from aiscc.public_live.service import (
    AdmissionService,
    ProductionOwnerAdmission,
    ReconciliationService,
)
from tests.integration.workflow.test_postgres_kernel import build_kernel, facts, request

pytestmark = pytest.mark.postgres
BODY = b'{"scenario_id":"stockroom-s1-normal","scenario_version":"1.0.0"}'
P, C = b"p" * 32, b"c" * 32


class SyntheticEvidence:
    """No real provider/supervisor proof; only exact explicitly registered test facts."""

    def __init__(self):
        self.outcomes = {}
        self.closed = set()
        self.closure_proofs = {}

    async def outcome(self, run, ordinal, evidence):
        return self.outcomes[(run, ordinal, evidence)]

    async def closure(self, run, generation, evidence):
        return (
            self.closure_proofs.get((run, evidence), hashlib.sha256(b"test-closure" + run).digest())
            if (run, evidence) in self.closed
            else None
        )


class Harness:
    async def start(self, url):
        self.url = url
        self.admin = create_engine(url)
        self.kernel, self.owner_repo, self.guards, self.owner_engine = build_kernel(url)
        self.campaign = uuid4().hex
        self.roles = ["l2rt_" + uuid4().hex, "l2rc_" + uuid4().hex]
        async with self.admin.begin() as conn:
            for role, group in zip(
                self.roles,
                ["aiscc_public_live_runtime", "aiscc_public_live_reconciler"],
                strict=True,
            ):
                await conn.execute(
                    text(f"CREATE ROLE {role} LOGIN PASSWORD 'synthetic_only' INHERIT")
                )
                await conn.execute(text(f"GRANT {group} TO {role}"))
            await conn.execute(text(f"GRANT aiscc_public_live_runtime TO {self.roles[1]}"))
            await conn.execute(
                text("""INSERT INTO public_campaign
              (campaign_id,starts_at,ends_at,available,hmac_version,scenario_id,scenario_version,
               content_digest,policy_digest) VALUES(:c,'2026-09-01Z','2026-10-17T15:00:00Z',
               15000000,'v1','stockroom-s1-normal','1.0.0',:content,:policy)"""),
                {"c": self.campaign, "content": C, "policy": P},
            )
            await conn.execute(
                text("UPDATE public_control SET enabled=true,active_campaign=:c,policy_digest=:p"),
                {"c": self.campaign, "p": P},
            )
        self.engines = [
            create_engine(
                make_url(url)
                .set(username=r, password="synthetic_only")
                .render_as_string(hide_password=False)
            )
            for r in self.roles
        ]
        self.runtime, self.reconciler = [
            PublicLiveRepository(create_session_factory(e)) for e in self.engines
        ]
        self.identity = IdentityPolicy(
            ("10.0.0.0/24",), "test-edge-proof", self.campaign, "v1", b"s" * 32
        )
        self.admission = AdmissionService(
            self.runtime, self.identity, policy_digest=P, content_digest=C
        )

        async def prepare(owner_id):
            req = request(
                run_id=owner_id,
                source=None,
                version=0,
                target=WorkflowState.READY,
                request_id=owner_id + "-ready",
                runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
            )
            req = replace(req, created_at=datetime(2026, 9, 16, tzinfo=UTC))
            return req, facts(self.guards, req)

        self.owner = ProductionOwnerAdmission(self.kernel, prepare)
        self.evidence = SyntheticEvidence()
        self.service = ReconciliationService(
            self.runtime, self.reconciler, self.owner, dispatch=self, evidence=self.evidence
        )
        return self

    async def authorize(self, run, ordinal, owner_id):
        owner = await self.kernel.verify_consistency(owner_id)
        assert owner.state is WorkflowState.RUNNING
        return 68000, owner.state_version  # Synthetic approved envelope, never real pricing proof.

    async def admit(self, key=None, ip="8.8.8.8"):
        return await self.admission.admit(
            BODY, key or uuid4().hex, peer="10.0.0.2", headers=(("X-Forwarded-For", ip),)
        )

    async def running(self, run):
        owner_id = await self.service.bind(run)
        req = request(
            run_id=owner_id,
            source=WorkflowState.READY,
            version=1,
            target=WorkflowState.RUNNING,
            request_id=owner_id + "-running",
            runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        )
        await self.kernel.request_transition(req, facts(self.guards, req))
        return owner_id

    async def sql(self, query, **params):
        async with self.admin.begin() as conn:
            result = await conn.execute(text(query), params)
            return result.scalar() if result.returns_rows else None

    async def clock(self, stamp):
        # Test-only DB-clock replacement in this disposable database, never application code.
        spec = importlib.util.spec_from_file_location(
            "l1_clock",
            Path("migrations/versions/20260915_0013_public_live_persistence_primitives.py"),
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        ddl = next(
            s
            for s in module.DDL.split("-- statement")
            if "CREATE FUNCTION public_live_api.clock_lock" in s
        )
        fixed = datetime.fromisoformat(stamp).astimezone(UTC).isoformat()
        ddl = ddl.replace("CREATE FUNCTION", "CREATE OR REPLACE FUNCTION").replace(
            "now_at:=clock_timestamp();", f"now_at:='{fixed}'::timestamptz;"
        )
        await self.sql(ddl)

    async def close_zero(self, run):
        self.evidence.closed.add((run, "closed"))
        return await self.service.close(run, "closed", target="FAILED_NOT_DISPATCHED")

    async def stop(self):
        for e in self.engines + [self.owner_engine]:
            await e.dispose()
        async with self.admin.begin() as c:
            for r in self.roles:
                await c.execute(text("DROP ROLE " + r))
        await self.admin.dispose()


@asynccontextmanager
async def harness(url):
    h = await Harness().start(url)
    try:
        yield h
    finally:
        await h.stop()


def test_two_workers_one_admission_and_lost_response(l2_url):
    async def check():
        async with harness(l2_url) as h:
            ready = asyncio.Event()
            pids = set()

            class BarrierRepository:
                @asynccontextmanager
                async def transaction(self):
                    async with h.runtime._sessions() as session, session.begin():
                        pids.add(await session.scalar(text("SELECT pg_backend_pid()")))
                        if len(pids) == 2:
                            ready.set()
                        await asyncio.wait_for(ready.wait(), timeout=10)
                        now = await session.scalar(text("SELECT public_live_api.clock_lock()"))
                        tx = PublicLiveTransaction(session, now)
                        try:
                            yield tx
                        finally:
                            tx._open = False

            h.admission.repository = BarrierRepository()
            key = uuid4().hex
            a, b = await asyncio.gather(h.admit(key), h.admit(key))
            assert len(pids) == 2
            h.admission.repository = h.runtime
            assert a.run_id == b.run_id and {a.replayed, b.replayed} == {True, False}
            assert (a.read_capability is None) != (b.read_capability is None)
            for table in [
                "public_run",
                "public_idempotency",
                "public_rate_event",
                "public_reservation",
                "public_outbox",
            ]:
                assert await h.sql("SELECT count(*) FROM " + table) == 1
            assert await h.sql("SELECT held FROM public_campaign") == 200000
            await h.sql("UPDATE public_control SET enabled=false")
            assert (await h.admit(key)).replayed
            assert (await h.admit(key)).read_capability is None
            with pytest.raises(AdmissionDenied, match="CLIENT_BINDING_DENIED"):
                await h.admit(key, ip="1.1.1.1")

    asyncio.run(check())


def test_replay_expiry_clock_regression_and_pins(l2_url):
    async def check():
        async with harness(l2_url) as h:
            t = datetime(2026, 9, 16, 12, tzinfo=UTC)
            await h.clock(t.isoformat())
            key = uuid4().hex
            receipt = await h.admit(key)
            await h.clock((t + timedelta(seconds=599)).isoformat())
            assert (await h.admit(key)).replayed
            await h.clock((t + timedelta(seconds=600)).isoformat())
            with pytest.raises(AdmissionDenied, match="IDEMPOTENCY_EXPIRED"):
                await h.admit(key)
            await h.clock(t.isoformat())
            with pytest.raises(AdmissionDenied, match="LIVE_DISABLED"):
                await h.admit()
            assert not await h.sql("SELECT enabled FROM public_control")
            assert await h.sql("SELECT count(*) FROM public_idempotency") == 1
            assert receipt.read_expires_at == t + timedelta(hours=24)

    asyncio.run(check())


def test_rate_boundaries_and_nonrefundable_counts(l2_url):
    async def check():
        async with harness(l2_url) as h:
            t = datetime(2026, 9, 16, 0, tzinfo=UTC)
            await h.clock(t.isoformat())
            for i in range(10):
                if i in (3, 6, 9):
                    await h.clock((t + timedelta(hours=i // 3)).isoformat())
                r = await h.admit()
                await h.close_zero(r.run_id)
                if i == 2:
                    await h.clock((t + timedelta(seconds=3599)).isoformat())
                    with pytest.raises(AdmissionDenied, match="CLIENT_RATE_LIMIT"):
                        await h.admit()
            with pytest.raises(AdmissionDenied, match="CLIENT_RATE_LIMIT"):
                await h.admit()
            assert await h.sql("SELECT count(*) FROM public_rate_event") == 10
            assert await h.sql("SELECT held FROM public_campaign") == 0

    asyncio.run(check())


def test_global_day_limit_and_campaign_cutoff(l2_url):
    async def check():
        async with harness(l2_url) as h:
            await h.clock("2026-10-17T14:59:59+00:00")
            for i in range(20):
                r = await h.admit(ip=f"8.8.4.{i + 1}")
                await h.close_zero(r.run_id)
            with pytest.raises(AdmissionDenied, match="GLOBAL_DAY_LIMIT"):
                await h.admit(ip="1.1.1.1")
            await h.clock("2026-10-17T15:00:00+00:00")
            with pytest.raises(AdmissionDenied, match="CAMPAIGN_CLOSED"):
                await h.admit()
            assert await h.sql("SELECT count(*) FROM public_rate_event") == 20

    asyncio.run(check())


def test_two_slots_and_single_remaining_reservation_race(l2_url):
    async def check():
        async with harness(l2_url) as h:
            await h.sql("UPDATE public_campaign SET available=200000,settled=14800000")
            await h.sql(
                "INSERT INTO public_day(campaign_id,utc_date,available,settled) "
                "VALUES(:c,(clock_timestamp() AT TIME ZONE 'UTC')::date,200000,3800000)",
                c=h.campaign,
            )
            results = await asyncio.gather(h.admit(), h.admit(ip="1.1.1.1"), return_exceptions=True)
            assert sum(not isinstance(r, Exception) for r in results) == 1
            assert any(
                isinstance(r, AdmissionDenied) and str(r) == "BUDGET_UNAVAILABLE" for r in results
            )
            assert await h.sql("SELECT available FROM public_campaign") == 0
            assert await h.sql("SELECT available FROM public_day") == 0
            assert await h.sql("SELECT held FROM public_day") == 200000

    asyncio.run(check())


def test_capacity_lease_expiry_is_not_slot_release(l2_url):
    async def check():
        async with harness(l2_url) as h:
            a, b = await asyncio.gather(h.admit(), h.admit(ip="1.1.1.1"))
            async with h.runtime.transaction() as tx:
                await tx.quarantine(a.run_id, 1)
            with pytest.raises(AdmissionDenied, match="CAPACITY_UNAVAILABLE"):
                await h.admit(ip="9.9.9.9")
            assert await h.sql("SELECT count(*) FROM public_slot WHERE state<>'FREE'") == 2
            assert await h.sql("SELECT count(*) FROM public_outbox") == 2

    asyncio.run(check())


def test_real_owner_binding_markers_unknown_and_closure(l2_url):
    async def check():
        async with harness(l2_url) as h:
            r = await h.admit()
            a, b = await asyncio.gather(h.service.bind(r.run_id), h.service.bind(r.run_id))
            assert a == b and await h.sql("SELECT count(*) FROM work_runs") == 1
            assert await h.sql("SELECT count(*) FROM transition_decisions") == 1
            await h.running(r.run_id)
            ticket = await h.service.authorize_dispatch(r.run_id, 1)
            assert ticket.max_cost == 68000
            assert (
                await h.sql("SELECT count(*) FROM public_dispatch") == 1
            )  # visible from independent conn
            await h.service.recover_unknown(r.run_id)
            with pytest.raises(DBAPIError):
                await h.service.authorize_dispatch(r.run_id, 1)
            with pytest.raises(DBAPIError):
                await h.service.authorize_dispatch(r.run_id, 2)
            assert not await h.service.close(r.run_id, "not-proven", target=None)
            assert await h.sql("SELECT held FROM public_campaign") == 200000
            h.evidence.closed.add((r.run_id, "closed"))
            results = await asyncio.gather(
                h.service.close(r.run_id, "closed", target=None),
                h.service.close(r.run_id, "closed", target=None),
            )
            assert sorted(results) == [False, True]
            assert (
                await h.sql("SELECT count(*) FROM public_money_event WHERE event_kind='SETTLE'")
                == 1
            )
            assert await h.sql("SELECT settled FROM public_campaign") == 68000
            assert await h.sql("SELECT state FROM public_run") == "UNKNOWN_OUTCOME"
            h.evidence.closed.add((r.run_id, "conflicting"))
            h.evidence.closure_proofs[(r.run_id, "conflicting")] = b"x" * 32
            with pytest.raises(AdmissionDenied, match="SETTLEMENT_CONFLICT"):
                await h.service.close(r.run_id, "conflicting", target=None)
            h.evidence.outcomes[(r.run_id, 1, "late")] = (
                ObservationKind.KNOWN_SUCCESS,
                100,
                hashlib.sha256(b"late").digest(),
            )
            await h.service.record_outcome(r.run_id, 1, "late")
            assert await h.sql("SELECT settled FROM public_campaign") == 68000

    asyncio.run(check())


def test_known_failure_retry_and_original_day_settlement(l2_url):
    async def check():
        async with harness(l2_url) as h:
            await h.clock("2026-09-16T23:59:59+00:00")
            r = await h.admit()
            await h.running(r.run_id)
            for n in (1, 2):
                await h.service.authorize_dispatch(r.run_id, n)
                h.evidence.outcomes[(r.run_id, n, "failed")] = (
                    ObservationKind.KNOWN_FAILURE,
                    None,
                    hashlib.sha256(bytes([n])).digest(),
                )
                await h.service.record_outcome(r.run_id, n, "failed")
            async with h.runtime.transaction() as tx:
                ctx = await tx.run_context(r.run_id)
                assert all(d["usage_missing"] and d["cost"] == 68000 for d in ctx["dispatches"])
            with pytest.raises(AdmissionDenied):
                await h.service.authorize_dispatch(r.run_id, 3)
            await h.clock("2026-09-17T00:00:01+00:00")
            h.evidence.closed.add((r.run_id, "closed"))
            assert await h.service.close(r.run_id, "closed", target="FAILED_PROVIDER")
            assert str(await h.sql("SELECT utc_date FROM public_day")) == "2026-09-16"
            assert await h.sql("SELECT settled FROM public_day") == 136000
            await h.admit()
            assert await h.sql("SELECT count(*) FROM public_day") == 2

    asyncio.run(check())


@pytest.mark.parametrize("kind", [ObservationKind.KNOWN_SUCCESS, ObservationKind.UNKNOWN])
def test_above_bound_truth_and_default_dispatch_denial(l2_url, kind):
    async def check():
        async with harness(l2_url) as h:
            r = await h.admit()
            await h.running(r.run_id)
            unconfigured = ReconciliationService(h.runtime, h.reconciler, h.owner)
            with pytest.raises(AdmissionDenied):
                await unconfigured.authorize_dispatch(r.run_id, 1)
            await h.service.authorize_dispatch(r.run_id, 1)
            h.evidence.outcomes[(r.run_id, 1, "over")] = (
                kind,
                68001,
                hashlib.sha256(b"over").digest(),
            )
            await h.service.record_outcome(r.run_id, 1, "over")
            assert await h.sql("SELECT state FROM public_run") == "FAILED_SAFETY"
            assert not await h.sql("SELECT enabled FROM public_control")
            assert await h.sql("SELECT max(cost_micro) FROM public_observation") == 68001
            assert await h.sql("SELECT held FROM public_campaign") == 200000

    asyncio.run(check())


@pytest.mark.parametrize(
    "table,event",
    [
        ("public_run", "INSERT"),
        ("public_idempotency", "INSERT"),
        ("public_rate_event", "INSERT"),
        ("public_reservation", "INSERT"),
        ("public_money_event", "INSERT"),
        ("public_slot", "UPDATE"),
        ("public_outbox", "INSERT"),
    ],
)
def test_crash_at_each_admission_write_rolls_back(l2_url, table, event):
    async def check():
        async with harness(l2_url) as h:
            await h.sql(
                "CREATE FUNCTION public.test_crash() RETURNS trigger LANGUAGE plpgsql AS $$ "
                "BEGIN RAISE EXCEPTION 'TEST_CRASH'; END $$"
            )
            await h.sql(
                f"CREATE TRIGGER test_crash AFTER {event} ON public.{table} "
                "FOR EACH ROW EXECUTE FUNCTION public.test_crash()"
            )
            key = uuid4().hex
            with pytest.raises(DBAPIError, match="TEST_CRASH"):
                await h.admit(key)
            for name in [
                "public_run",
                "public_idempotency",
                "public_rate_event",
                "public_reservation",
                "public_money_event",
                "public_outbox",
                "public_dispatch",
            ]:
                assert await h.sql("SELECT count(*) FROM " + name) == 0
            assert await h.sql("SELECT held FROM public_campaign") == 0
            assert await h.sql("SELECT count(*) FROM public_slot WHERE state='FREE'") == 2
            await h.sql(f"DROP TRIGGER test_crash ON public.{table}")
            assert not (await h.admit(key)).replayed

    asyncio.run(check())


def test_lost_commit_acknowledgement_same_key_only(l2_url):
    class CommitUnknown(RuntimeError):
        pass

    class UncertainRepository:
        def __init__(self, repository):
            self.repository = repository
            self.once = True

        @asynccontextmanager
        async def transaction(self):
            async with self.repository.transaction() as tx:
                yield tx
            if self.once:
                self.once = False
                raise CommitUnknown("COMMIT_OUTCOME_UNKNOWN")

    async def check():
        async with harness(l2_url) as h:
            service = AdmissionService(
                UncertainRepository(h.runtime), h.identity, policy_digest=P, content_digest=C
            )
            key = uuid4().hex
            with pytest.raises(CommitUnknown):
                await service.admit(
                    BODY, key, peer="10.0.0.2", headers=(("X-Forwarded-For", "8.8.8.8"),)
                )
            retry = await h.admit(key)
            assert retry.replayed and retry.read_capability is None
            assert await h.sql("SELECT count(*) FROM public_run") == 1
            assert await h.sql("SELECT count(*) FROM public_dispatch") == 0

    asyncio.run(check())


def test_success_requires_real_governance_before_completed(l2_url):
    async def check():
        async with harness(l2_url) as h:
            r = await h.admit()
            owner_id = await h.running(r.run_id)
            await h.service.authorize_dispatch(r.run_id, 1)
            proof = hashlib.sha256(b"known-success").digest()
            h.evidence.outcomes[(r.run_id, 1, "success")] = (
                ObservationKind.KNOWN_SUCCESS,
                1000,
                proof,
            )
            await h.service.record_outcome(r.run_id, 1, "success")
            assert await h.sql("SELECT state FROM public_run") == "GOVERNANCE_PENDING"
            h.evidence.closed.add((r.run_id, "closed"))
            with pytest.raises(DBAPIError, match="PROJECTION_PREDICATE_DENIED"):
                await h.service.close(r.run_id, "closed", target="COMPLETED")
            assert await h.sql("SELECT held FROM public_campaign") == 200000
            req = request(
                run_id=owner_id,
                source=WorkflowState.RUNNING,
                version=2,
                target=WorkflowState.FAILED,
                runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
            )
            await h.kernel.request_transition(req, facts(h.guards, req))
            assert await h.service.close(r.run_id, "closed", target="COMPLETED")
            assert await h.sql("SELECT state FROM public_run") == "COMPLETED"
            assert (await h.kernel.verify_consistency(owner_id)).state is WorkflowState.FAILED
            assert not await h.service.close(r.run_id, "closed", target="COMPLETED")

    asyncio.run(check())


def test_payload_conflict_hmac_rotation_and_marker_currentness(l2_url):
    async def check():
        async with harness(l2_url) as h:
            key = uuid4().hex
            r = await h.admit(key)
            changed = AdmissionService(
                h.runtime, h.identity, policy_digest=b"q" * 32, content_digest=C
            )
            replay = await changed.admit(
                BODY, key, peer="10.0.0.2", headers=(("X-Forwarded-For", "8.8.8.8"),)
            )
            assert replay.replayed and replay.run_id == r.run_id
            async with h.runtime.transaction() as tx:
                conflict = await tx.admit_checked(
                    PersistRun(
                        r.run_id,
                        h.campaign,
                        h.identity.bucket("10.0.0.2", (("X-Forwarded-For", "8.8.8.8"),)),
                        hashlib.sha256(bytes.fromhex(key)).digest(),
                        b"r" * 32,
                        b"x" * 32,
                        1,
                    ),
                    policy_digest=P,
                    content_digest=C,
                    hmac_version="v1",
                )
                assert conflict == {"error": "IDEMPOTENCY_CONFLICT"}
            rotated = AdmissionService(
                h.runtime, replace(h.identity, key_version="v2"), policy_digest=P, content_digest=C
            )
            with pytest.raises(AdmissionDenied, match="POLICY_UNAVAILABLE"):
                await rotated.admit(
                    BODY, uuid4().hex, peer="10.0.0.2", headers=(("X-Forwarded-For", "8.8.8.8"),)
                )
            await h.running(r.run_id)
            async with h.runtime.transaction() as tx:
                with pytest.raises(DBAPIError, match="PUBLIC_OWNER_NOT_RUNNING"):
                    await tx.mark_checked(r.run_id, 1, 1, 68000, 1)
            assert await h.sql("SELECT count(*) FROM public_dispatch") == 0

    asyncio.run(check())


def test_lease_deadline_recovery_and_timeout_closure(l2_url):
    async def check():
        async with harness(l2_url) as h:
            t = datetime(2026, 9, 16, 12, tzinfo=UTC)
            await h.clock(t.isoformat())
            receipt = await h.admit()
            await h.running(receipt.run_id)
            await h.service.authorize_dispatch(receipt.run_id, 1)
            await h.clock((t + timedelta(seconds=5)).isoformat())
            await h.service.heartbeat(receipt.run_id)
            await h.clock((t + timedelta(seconds=19)).isoformat())
            assert not await h.service.recover_lease(receipt.run_id)
            await h.clock((t + timedelta(seconds=20)).isoformat())
            assert await h.service.recover_lease(receipt.run_id)
            assert await h.sql("SELECT state FROM public_slot WHERE slot_id=1") == "SUSPECT"
            assert await h.sql("SELECT state FROM public_run") == "UNKNOWN_OUTCOME"
            await h.clock((t + timedelta(seconds=90)).isoformat())
            with pytest.raises(DBAPIError):
                await h.service.authorize_dispatch(receipt.run_id, 2)
            assert not await h.service.close(receipt.run_id, "unproved", target="FAILED_TIMEOUT")
            h.evidence.closed.add((receipt.run_id, "closed"))
            assert await h.service.close(receipt.run_id, "closed", target="FAILED_TIMEOUT")
            assert await h.sql("SELECT state FROM public_run") == "FAILED_TIMEOUT"
            assert await h.sql("SELECT settled FROM public_campaign") == 68000

    asyncio.run(check())
