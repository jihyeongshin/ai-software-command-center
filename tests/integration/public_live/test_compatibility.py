"""Compatibility proofs on disposable PostgreSQL; fixture activation is not release."""

from dataclasses import replace
from uuid import uuid4

import pytest
from sqlalchemy import text

from aiscc.persistence.public_live import Observation, ObservationKind
from tests.integration.public_live.test_persistence import DIGEST, denied, fixture, scenario

pytestmark = pytest.mark.postgres


def test_context_and_permission_boundary():
    async def check(s):
        tx, run = await fixture(s)
        await s.execute(text("SET LOCAL ROLE aiscc_public_live_runtime"))
        context = await tx.admission_context(run.campaign_id, run.bucket_hash)
        assert context["hour_count"] == context["client_day_count"] == 0
        assert context["day_available"] == 4000000
        result = await tx.admit_checked(
            run, policy_digest=DIGEST, content_digest=DIGEST, hmac_version="test"
        )
        assert result == {"run_id": run.run_id.hex(), "replayed": False}
        replay = await tx.admit_checked(
            replace(run, run_id=uuid4().bytes),
            policy_digest=DIGEST,
            content_digest=DIGEST,
            hmac_version="test",
        )
        assert replay == {"run_id": run.run_id.hex(), "replayed": True}
        for table in ["public_run", "public_rate_event", "public_campaign", "public_control"]:
            async with denied(s):
                await s.execute(text("SELECT * FROM " + table))
            async with denied(s):
                await s.execute(text("DELETE FROM " + table))
        async with denied(s):
            await s.execute(text("UPDATE public_run SET state='COMPLETED'"))
        assert (await tx.run_context(run.run_id))["state"] == "ADMITTED"

    scenario(check)


@pytest.mark.parametrize(
    "target", ["COMPLETED", "GOVERNANCE_PENDING", "ADMITTED", "UNKNOWN_OUTCOME"]
)
def test_unproved_state_denied(target):
    async def check(s):
        tx, run = await fixture(s)
        await tx.persist_run(run)
        await s.execute(text("SET LOCAL ROLE aiscc_public_live_runtime"))
        async with denied(s):
            await tx.project_run(run.run_id, 1, target, DIGEST)
        assert (await tx.run_context(run.run_id))["version"] == 1

    scenario(check)


def test_terminal_closure_cas_and_exact_repeat():
    async def check(s):
        tx, run = await fixture(s)
        await tx.persist_run(run)
        await tx.fence(run.run_id, 1)
        await tx.admit_closure(run.run_id, 2, 0, DIGEST, uuid4().bytes * 2)
        await tx.settle(run.run_id, 0, DIGEST)
        await s.execute(text("SET LOCAL ROLE aiscc_public_live_runtime"))
        async with denied(s):
            await tx.project_run(run.run_id, 2, "FAILED_NOT_DISPATCHED", DIGEST)
        assert await tx.project_run(run.run_id, 1, "FAILED_NOT_DISPATCHED", DIGEST) == 2
        assert await tx.project_run(run.run_id, 1, "FAILED_NOT_DISPATCHED", DIGEST) == 2
        for expected, target, proof in [
            (1, "FAILED_NOT_DISPATCHED", b"e" * 32),
            (2, "ADMITTED", DIGEST),
            (2, "COMPLETED", DIGEST),
        ]:
            async with denied(s):
                await tx.project_run(run.run_id, expected, target, proof)
        assert (
            await s.scalar(text("SELECT state FROM public_live_api.safe_status"))
            == "FAILED_NOT_DISPATCHED"
        )

    scenario(check)


def test_unknown_requires_marker_and_quarantines():
    async def check(s):
        tx, run = await fixture(s)
        await tx.persist_run(run)
        # Compatibility-only fixture; actual owner composition is tested in L2.
        await s.execute(text("UPDATE public_outbox SET state='BOUND',owner_binding='fixture'"))
        await tx.mark_dispatch(run.run_id, 1, 1, 68000)
        await s.execute(text("SET LOCAL ROLE aiscc_public_live_runtime"))
        assert await tx.project_run(run.run_id, 2, "UNKNOWN_OUTCOME", DIGEST) == 3
        async with denied(s):
            await tx.mark_dispatch(run.run_id, 1, 2, 68000)
        async with denied(s):
            await tx.settle(run.run_id, 68000, DIGEST)
        await s.execute(text("RESET ROLE"))
        assert await s.scalar(text("SELECT state FROM public_slot WHERE slot_id=1")) == "SUSPECT"
        assert await s.scalar(text("SELECT held FROM public_campaign")) == 200000

    scenario(check)


def test_safety_evidence_does_not_release_liability():
    async def check(s):
        tx, run = await fixture(s)
        await tx.persist_run(run)
        await s.execute(text("SET LOCAL ROLE aiscc_public_live_runtime"))
        await tx.observe(
            Observation(
                uuid4().bytes,
                run.run_id,
                uuid4().bytes * 2,
                ObservationKind.ABOVE_BOUND,
                DIGEST,
                cost_micro=300000,
            )
        )
        assert await tx.project_run(run.run_id, 1, "FAILED_SAFETY", DIGEST) == 2
        await s.execute(text("RESET ROLE"))
        assert not await s.scalar(text("SELECT enabled FROM public_control"))
        assert await s.scalar(text("SELECT held FROM public_campaign")) == 200000

    scenario(check)
