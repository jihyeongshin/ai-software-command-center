"""Production ingress composition against mediated PostgreSQL admission/start."""

import asyncio
import secrets

import pytest
from sqlalchemy import text
from sqlalchemy.engine import make_url

from aiscc.persistence import create_engine
from aiscc.public_live.http import ORIGIN
from aiscc.public_live.ingress import (
    CAMPAIGN_ID,
    HMAC_VERSION,
    create_app,
    verify_runtime_identity,
)
from aiscc.public_live.start_authority import StartContract
from aiscc.scenarios.models import RESOURCE_VERSION
from tests.public_live_http_helpers import call

pytestmark = pytest.mark.postgres

LOGIN = "aiscc_live_ingress_login"
EDGE_TRUST = "HOSTED_OVERWRITE_PROOF_ACCEPTED_V1"


def edge_headers(key: str = "a" * 32) -> list[tuple[str, str]]:
    return [
        ("host", "public-live.up.railway.app"),
        ("x-real-ip", "8.8.8.8"),
        ("x-forwarded-proto", "https"),
        ("x-railway-edge", "icn1"),
        ("origin", ORIGIN),
        ("content-type", "application/json"),
        ("idempotency-key", key),
    ]


def test_production_ingress_disabled_gate_and_atomic_start(l2_url: str, monkeypatch) -> None:
    async def check() -> None:
        password = secrets.token_urlsafe(24)
        source_key = b"k" * 32
        admin = create_engine(l2_url)
        base = make_url(l2_url)
        hosted = None
        try:
            async with admin.begin() as connection:
                await connection.execute(
                    text(
                        f"CREATE ROLE {LOGIN} LOGIN INHERIT NOSUPERUSER "
                        "NOCREATEDB NOCREATEROLE NOBYPASSRLS "
                        f"PASSWORD '{password}'"
                    )
                )
                await connection.execute(text(f"GRANT aiscc_public_live_ingress TO {LOGIN}"))
            ingress_url = base.set(username=LOGIN, password=password).render_as_string(
                hide_password=False
            )
            monkeypatch.setenv("AISCC_PUBLIC_LIVE_DATABASE_URL", ingress_url)
            monkeypatch.setenv("PUBLIC_LIVE_API_ORIGIN", "https://public-live.up.railway.app")
            monkeypatch.setenv("AISCC_PUBLIC_LIVE_SOURCE_HMAC_KEY", source_key.hex())
            monkeypatch.setenv("AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST", EDGE_TRUST)
            monkeypatch.delenv("AISCC_OPENAI_API_KEY", raising=False)
            monkeypatch.delenv("OPENAI_API_KEY", raising=False)
            monkeypatch.delenv("AISCC_DATABASE_URL", raising=False)

            hosted = create_app()
            await verify_runtime_identity(hosted.engine)
            admission = hosted.application.admission
            assert admission is not None
            contract = StartContract.load()
            assert admission.service.policy_digest == bytes.fromhex(contract.digest)
            assert admission.service.content_digest == bytes.fromhex(RESOURCE_VERSION)
            assert admission.service.start_contract == contract

            # A configured campaign with the singleton control still disabled
            # is the accepted preactivation DB state.
            async with admin.begin() as connection:
                await connection.execute(
                    text(
                        "INSERT INTO public_campaign("
                        "campaign_id,starts_at,ends_at,available,hmac_version,"
                        "scenario_id,scenario_version,content_digest,policy_digest"
                        ") VALUES(:campaign,clock_timestamp()-interval '1 hour',"
                        "'2026-10-17T15:00:00Z',15000000,:version,"
                        "'stockroom-s1-normal','1.0.0',:content,:policy)"
                    ),
                    {
                        "campaign": CAMPAIGN_ID,
                        "version": HMAC_VERSION,
                        "content": admission.service.content_digest,
                        "policy": admission.service.policy_digest,
                    },
                )
                await connection.execute(
                    text(
                        "UPDATE public_control SET active_campaign=:campaign,"
                        "policy_digest=:policy WHERE id=1"
                    ),
                    {
                        "campaign": CAMPAIGN_ID,
                        "policy": admission.service.policy_digest,
                    },
                )

            disabled = await call(
                hosted,
                headers=edge_headers(),
                scheme="http",
            )
            assert disabled["status"] == 503
            assert disabled["json"] == {"error": {"code": "LIVE_DISABLED", "retryable": False}}
            async with admin.connect() as connection:
                counts = (
                    await connection.execute(
                        text(
                            "SELECT "
                            "(SELECT count(*) FROM public_run),"
                            "(SELECT count(*) FROM public_reservation),"
                            "(SELECT count(*) FROM public_outbox),"
                            "(SELECT count(*) FROM public_start_request),"
                            "(SELECT count(*) FROM public_start_event),"
                            "(SELECT count(*) FROM public_provider_execution),"
                            "(SELECT count(*) FROM public_provider_request),"
                            "(SELECT count(*) FROM public_worker_claim),"
                            "(SELECT count(*) FROM execution_operations),"
                            "(SELECT count(*) FROM work_runs)"
                        )
                    )
                ).one()
            assert tuple(counts) == (0,) * 10

            async with admin.begin() as connection:
                await connection.execute(
                    text("UPDATE public_control SET enabled=true,incident=NULL WHERE id=1"),
                )

            accepted = await call(hosted, headers=edge_headers(), scheme="http")
            replayed = await call(hosted, headers=edge_headers(), scheme="http")
            assert accepted["status"] == 201
            assert accepted["json"]["state"] == "ADMITTED"
            assert accepted["json"]["replayed"] is False
            assert replayed["status"] == 202
            assert replayed["json"] == {
                "run_id": accepted["json"]["run_id"],
                "replayed": True,
            }

            async with admin.connect() as connection:
                counts = (
                    await connection.execute(
                        text(
                            "SELECT "
                            "(SELECT count(*) FROM public_run),"
                            "(SELECT count(*) FROM public_reservation),"
                            "(SELECT count(*) FROM public_outbox),"
                            "(SELECT count(*) FROM public_start_request),"
                            "(SELECT count(*) FROM public_start_event),"
                            "(SELECT count(*) FROM public_idempotency),"
                            "(SELECT count(*) FROM public_provider_execution),"
                            "(SELECT count(*) FROM public_provider_request),"
                            "(SELECT count(*) FROM public_worker_claim),"
                            "(SELECT count(*) FROM execution_operations),"
                            "(SELECT count(*) FROM work_runs)"
                        )
                    )
                ).one()
                candidate = await connection.scalar(
                    text("SELECT candidate_body FROM public_start_request")
                )
                run_pins = (
                    await connection.execute(
                        text(
                            "SELECT encode(policy_digest,'hex'),"
                            "encode(scenario_digest,'hex') FROM public_run"
                        )
                    )
                ).one()
            assert tuple(counts) == (1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0)
            assert candidate["campaign_id"] == CAMPAIGN_ID
            assert candidate["scenario_id"] == "stockroom-s1-normal"
            assert candidate["scenario_version"] == "1.0.0"
            assert candidate["contract_digest"] == contract.digest
            assert candidate["policy_digest"] == admission.service.policy_digest.hex()
            assert candidate["content_digest"] == RESOURCE_VERSION
            assert tuple(run_pins) == (contract.digest, RESOURCE_VERSION)
        finally:
            if hosted is not None:
                await hosted.engine.dispose()
            try:
                async with admin.begin() as connection:
                    await connection.execute(text(f"REVOKE aiscc_public_live_ingress FROM {LOGIN}"))
                    await connection.execute(text(f"DROP ROLE {LOGIN}"))
            finally:
                await admin.dispose()

    asyncio.run(check())
