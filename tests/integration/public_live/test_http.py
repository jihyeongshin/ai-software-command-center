"""HTTPS ASGI scopes + real mediated PostgreSQL + unchanged L2 service."""

import asyncio
from dataclasses import replace
from datetime import UTC, datetime, timedelta

import pytest

from aiscc.persistence.database import create_engine, create_session_factory
from aiscc.persistence.public_live import PublicLiveRepository
from aiscc.persistence.public_live_limits import PublicLiveLimits
from aiscc.public_live.http import ORIGIN, ROOT, LocalAdmissionBinding, create_app, decode, encode
from aiscc.public_live.service import AdmissionService
from aiscc.public_live.source import DirectPeerSource
from tests.integration.public_live.test_service import C, P, harness
from tests.public_live_http_helpers import call

pytestmark = pytest.mark.postgres


def apps(h, repository=None):
    repository = repository or h.runtime
    return create_app(
        source=DirectPeerSource(h.campaign, "v1", b"s" * 32, True),
        limits=PublicLiveLimits(repository),
        admission=LocalAdmissionBinding(
            AdmissionService(repository, h.identity, policy_digest=P, content_digest=C), "10.0.0.2"
        ),
    )


def read_headers(token=None):
    return [("origin", ORIGIN)] + ([] if token is None else [("x-run-read-capability", token)])


def test_real_http_admission_replay_capability_and_shared_read(l2_url, caplog):
    async def check():
        async with harness(l2_url) as h:
            t = datetime(2026, 9, 16, 12, tzinfo=UTC)
            await h.clock(t.isoformat())
            other = create_engine(h.engines[0].url.render_as_string(hide_password=False))
            try:
                a, b = apps(h), apps(h, PublicLiveRepository(create_session_factory(other)))
                x, y = await asyncio.gather(call(a), call(b))
                assert {x["status"], y["status"]} == {201, 202}
                first, replay = (x, y) if x["status"] == 201 else (y, x)
                receipt = first["json"]
                assert set(receipt) == {
                    "run_id",
                    "state",
                    "read_capability",
                    "read_expires_at",
                    "replayed",
                }
                assert receipt["state"] == "ADMITTED" and receipt["replayed"] is False
                assert len(receipt["run_id"]) == 22 and len(receipt["read_capability"]) == 43
                assert receipt["read_expires_at"] == "2026-09-17T12:00:00Z"
                assert replay["json"] == {"run_id": receipt["run_id"], "replayed": True}
                for table in (
                    "public_run",
                    "public_idempotency",
                    "public_outbox",
                    "public_reservation",
                    "public_rate_event",
                ):
                    assert await h.sql("SELECT count(*) FROM " + table) == 1
                assert await h.sql("SELECT count(*) FROM public_dispatch") == 0
                path = ROOT + "/" + receipt["run_id"]
                token = receipt["read_capability"]
                invalid = []
                for cap in (None, "bad", encode(b"x" * 32), token + "=", token[:-1] + "!"):
                    invalid.append(await call(a, "GET", path, headers=read_headers(cap)))
                invalid.append(
                    await call(
                        b, "GET", ROOT + "/" + encode(b"z" * 16), headers=read_headers(token)
                    )
                )
                invalid.append(
                    await call(
                        a,
                        "GET",
                        path,
                        headers=read_headers(token) + [("x-run-read-capability", token)],
                    )
                )
                assert all(
                    r["status"] == 404
                    and r["json"] == {"error": {"code": "NOT_FOUND", "retryable": False}}
                    for r in invalid
                )
                assert (
                    await h.sql("SELECT count(*) FROM public_live_shared_limit WHERE kind='READ'")
                    == 0
                )
                results = await asyncio.gather(
                    *(
                        call(
                            (a, b)[i % 2],
                            "GET",
                            path,
                            headers=read_headers(token),
                            client="1.1.1.1",
                        )
                        for i in range(31)
                    )
                )
                assert sum(r["status"] == 200 for r in results) == 30
                denied = next(r for r in results if r["status"] == 429)
                assert denied["json"] == {"error": {"code": "READ_RATE_LIMIT", "retryable": True}}
                assert denied["headers"]["retry-after"] == "60"
                projection = next(r["json"] for r in results if r["status"] == 200)
                assert set(projection) == {
                    "run_id",
                    "state",
                    "reason_code",
                    "admitted_at",
                    "updated_at",
                    "deadline_at",
                    "mode",
                    "scenario_id",
                    "scenario_version",
                    "result",
                }
                assert projection["result"] is None and projection["reason_code"] is None
                assert projection["mode"] == "PUBLIC_BOUNDED_LIVE"
                assert all(len(r["raw"]) <= 16384 for r in results)
                assert await h.sql("SELECT held FROM public_campaign") == 200000
                assert await h.sql("SELECT count(*) FROM public_rate_event") == 1
                await h.clock((t + timedelta(seconds=60)).isoformat())
                assert (await call(b, "GET", path, headers=read_headers(token)))["status"] == 200
                # Different IP cannot recover replay; original token still reads after IP change.
                assert (await call(a, client="1.1.1.1"))["json"]["error"][
                    "code"
                ] == "CLIENT_BINDING_DENIED"
                await h.clock((t + timedelta(seconds=599)).isoformat())
                assert (await call(a))["status"] == 202
                await h.clock((t + timedelta(seconds=600)).isoformat())
                assert (await call(b))["status"] == 410
                await h.clock((t + timedelta(hours=24)).isoformat())
                assert (await call(b, "GET", path, headers=read_headers(token)))["raw"] == invalid[
                    0
                ]["raw"]
                assert token not in caplog.text and "8.8.8.8" not in caplog.text
            finally:
                await other.dispose()

    asyncio.run(check())


def test_real_ingress_flood_composition_and_fail_closed(l2_url):
    async def check():
        async with harness(l2_url) as h:
            await h.clock("2026-09-16T12:00:15+00:00")
            a, b = apps(h), apps(h)
            result = await call(
                a,
                "OPTIONS",
                headers=[("origin", ORIGIN), ("access-control-request-method", "POST")],
            )
            assert result["status"] == 204
            result = await call(b, body=b"not-json")
            assert result["status"] == 400
            assert await h.sql("SELECT sum(attempts) FROM public_live_shared_limit") == 4
            results = await asyncio.gather(
                *(call((a, b)[i % 2], "DELETE", ROOT + "/x/cancel") for i in range(119))
            )
            assert sum(r["status"] == 404 for r in results) == 118
            assert sum(r["status"] == 429 for r in results) == 1
            result = await call(a, headers=[], body=b"secret" * 10000)
            assert result["status"] == 429 and result["receives"] == 0
            assert result["headers"]["retry-after"] == "45"
            assert await h.sql("SELECT count(*) FROM public_run") == 0
            assert (
                await h.sql("SELECT count(*) FROM public_live_shared_limit WHERE kind='READ'") == 0
            )
            assert await h.sql("SELECT held FROM public_campaign") == 0
            assert await h.sql("SELECT count(*) FROM public_dispatch") == 0
            await h.clock("2026-09-16T12:01:00+00:00")
            await h.sql("UPDATE public_control SET enabled=false")
            assert (await call(a))["json"]["error"]["code"] == "LIVE_DISABLED"
            # Real PostgreSQL permission failure at mediated backend is safe and closed.
            await h.sql(
                "REVOKE EXECUTE ON FUNCTION "
                "public_live_api.flood_consume_retained(text,text,bytea) "
                "FROM aiscc_public_live_runtime"
            )
            result = await call(b)
            assert result["json"] == {"error": {"code": "LIVE_UNAVAILABLE", "retryable": True}}
            assert result["receives"] == 0
            assert await h.sql("SELECT count(*) FROM public_run") == 0

    asyncio.run(check())


def test_read_cross_run_and_governance_pending_safe_projection(l2_url):
    async def check():
        async with harness(l2_url) as h:
            await h.clock("2026-09-16T12:00:00+00:00")
            a = apps(h)
            first = (await call(a))["json"]
            second = (
                await call(
                    a,
                    client="1.1.1.1",
                    headers=[
                        ("origin", ORIGIN),
                        ("content-type", "application/json"),
                        ("idempotency-key", "b" * 32),
                    ],
                )
            )["json"]
            result = await call(
                a,
                "GET",
                ROOT + "/" + second["run_id"],
                headers=read_headers(first["read_capability"]),
            )
            assert result["status"] == 404
            # Test-owned committed state, no fabricated provider/Judgment authority.
            await h.sql(
                "UPDATE public_run SET state='GOVERNANCE_PENDING' WHERE run_id=:r",
                r=decode(first["run_id"], 16),
            )
            result = await call(
                a,
                "GET",
                ROOT + "/" + first["run_id"],
                headers=read_headers(first["read_capability"]),
            )
            assert result["json"]["state"] == "GOVERNANCE_PENDING"
            assert result["json"]["result"] is None and b"ACCEPTED" not in result["raw"]
            assert first["read_capability"].encode() not in result["raw"]
            assert await h.sql("SELECT count(*) FROM public_dispatch") == 0
            # Unmatched campaign/version binding never reaches accepted L2 admission.
            a.admission = LocalAdmissionBinding(
                AdmissionService(
                    h.runtime,
                    replace(h.identity, key_version="v2"),
                    policy_digest=P,
                    content_digest=C,
                ),
                "10.0.0.2",
            )
            assert (await call(a))["json"]["error"]["code"] == "IDENTITY_UNAVAILABLE"

    asyncio.run(check())
