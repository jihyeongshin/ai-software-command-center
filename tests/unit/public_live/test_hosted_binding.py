from __future__ import annotations

import asyncio
import sys
from dataclasses import dataclass
from datetime import UTC, datetime

import pytest

from aiscc.__main__ import main
from aiscc.persistence.public_live_limits import LimitResult
from aiscc.public_live.edge_identity import RailwayEdgeIdentityAuthority
from aiscc.public_live.hosted_proof import FaultPoint, HostedProofSettings, expectation
from aiscc.public_live.http import PublicLiveApp
from aiscc.public_live.ingress import IngressSettings
from aiscc.public_live.worker import WorkerSettings, create_worker
from tests.public_live_http_helpers import call


@dataclass
class Limits:
    flood_calls: int = 0

    async def flood(self, campaign, version, source):
        self.flood_calls += 1
        return LimitResult(True, 60, 1, datetime.now(UTC))

    async def read(self, run, capability):
        raise AssertionError("not used")


def edge() -> RailwayEdgeIdentityAuthority:
    return RailwayEdgeIdentityAuthority(
        "https://public-live.up.railway.app", "public-live-v1", "v1", b"k" * 32, True
    )


def edge_headers():
    return [
        ("host", "public-live.up.railway.app"),
        ("x-real-ip", "8.8.8.8"),
        ("x-forwarded-proto", "https"),
        ("x-railway-edge", "icn1"),
        ("origin", "https://aiscc-replay.pages.dev"),
        ("content-type", "application/json"),
        ("idempotency-key", "a" * 32),
    ]


def test_dedicated_route_surface_and_disabled_admission() -> None:
    limits = Limits()
    app = PublicLiveApp(edge(), limits, None)  # type: ignore[arg-type]

    async def check():
        health = await call(app, "GET", "/health", headers=[])
        assert health["status"] == 200 and limits.flood_calls == 0
        disabled = await call(app, headers=edge_headers(), scheme="http")
        assert disabled["status"] == 503
        assert disabled["json"]["error"]["code"] == "LIVE_DISABLED"
        for path in (
            "/v1/command-center/projects",
            "/command-center",
            "/v1/security/evaluate",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/admin",
            "/debug",
            "/unknown",
        ):
            result = await call(app, "GET", path, headers=[])
            assert result["status"] == 404
        nested = await call(
            app,
            "GET",
            "/v1/public-live/runs/example/cancel",
            headers=edge_headers(),
            scheme="http",
        )
        assert nested["status"] == 404
        assert (await call(app, "DELETE", headers=edge_headers(), scheme="http"))["status"] == 405

    asyncio.run(check())


def test_ingress_and_worker_database_and_secret_boundaries() -> None:
    base = {
        "AISCC_PUBLIC_LIVE_DATABASE_URL": "postgresql+asyncpg://live@db/live",
        "PUBLIC_LIVE_API_ORIGIN": "https://public-live.up.railway.app",
        "AISCC_PUBLIC_LIVE_SOURCE_HMAC_KEY": (b"k" * 32).hex(),
    }
    assert IngressSettings.from_environment(base).overwrite_proof_accepted is False
    with pytest.raises(ValueError, match="PROVIDER_SECRET_DENIED"):
        IngressSettings.from_environment(base | {"AISCC_OPENAI_API_KEY": "never-read"})
    with pytest.raises(ValueError, match="OWNER_DATABASE_DENIED"):
        IngressSettings.from_environment(base | {"AISCC_DATABASE_URL": "owner"})
    assert WorkerSettings.from_environment(base).database_url.endswith("/live")
    with pytest.raises(ValueError, match="OWNER_DATABASE_DENIED"):
        WorkerSettings.from_environment(base | {"AISCC_DATABASE_URL": "owner"})
    worker = create_worker(base | {"AISCC_OPENAI_API_KEY": "presence-only"})
    assert worker.profile.base_url == "https://api.openai.com/v1"
    assert worker.adapter.invocation_count == 0
    assert callable(worker.execute_claim)
    asyncio.run(worker.close())


def test_operator_proof_is_private_synthetic_and_fail_closed() -> None:
    env = {
        "AISCC_HOSTED_L5_PROOF_CAMPAIGN": "proof-0123456789abcdef",
        "AISCC_HOSTED_L5_PROVIDER_DOUBLE_URL": "http://provider-double.railway.internal:8080/v1",
        "AISCC_HOSTED_L5_FAKE_SECRET_CLASS": "SYNTHETIC_SENTINEL_ONLY",
        "AISCC_PUBLIC_LIVE_ADMISSION": "DISABLED",
    }
    assert HostedProofSettings.from_environment(env).admission_disabled
    assert expectation(FaultPoint.BEFORE_DISPATCH).provider_receipts == 0
    post = expectation(FaultPoint.AFTER_DISPATCH)
    assert post.quarantine_required and not post.retry_allowed and post.provider_receipts == 1
    with pytest.raises(ValueError, match="CONFIGURATION_DENIED"):
        HostedProofSettings.from_environment(
            env | {"AISCC_HOSTED_L5_PROVIDER_DOUBLE_URL": "https://api.openai.com/v1"}
        )
    with pytest.raises(ValueError, match="CONFIGURATION_DENIED"):
        HostedProofSettings.from_environment(env | {"AISCC_OPENAI_API_KEY": "presence-only"})


def test_cli_pins_no_proxy_headers_and_smokes_worker_and_proof(monkeypatch, capsys) -> None:
    observed = {}
    monkeypatch.setattr("uvicorn.run", lambda *args, **kwargs: observed.update(kwargs))
    monkeypatch.setattr(sys, "argv", ["aiscc", "serve-public-live", "--port", "9000"])
    main()
    assert observed["proxy_headers"] is False and observed["port"] == 9000

    monkeypatch.setenv("AISCC_PUBLIC_LIVE_DATABASE_URL", "postgresql+asyncpg://live@db/live")
    monkeypatch.delenv("AISCC_DATABASE_URL", raising=False)
    monkeypatch.setattr(sys, "argv", ["aiscc", "public-live-worker", "--check"])
    main()

    for key, value in {
        "AISCC_HOSTED_L5_PROOF_CAMPAIGN": "proof-0123456789abcdef",
        "AISCC_HOSTED_L5_PROVIDER_DOUBLE_URL": "http://provider-double.railway.internal:8080/v1",
        "AISCC_HOSTED_L5_FAKE_SECRET_CLASS": "SYNTHETIC_SENTINEL_ONLY",
        "AISCC_PUBLIC_LIVE_ADMISSION": "DISABLED",
    }.items():
        monkeypatch.setenv(key, value)
    monkeypatch.delenv("AISCC_OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(
        sys,
        "argv",
        ["aiscc", "hosted-l5-proof", "--check", "--fault", "after-dispatch"],
    )
    main()
    assert capsys.readouterr().out == ""


def test_trusted_owner_api_has_no_public_live_route() -> None:
    from aiscc.api.app import create_app

    paths = {route.path for route in create_app().routes if hasattr(route, "path")}
    assert not any(path.startswith("/v1/public-live") for path in paths)
