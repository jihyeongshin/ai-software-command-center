"""Dedicated hosted Public Live ingress composition; never imports the owner API."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.types import Receive, Scope, Send

from aiscc.persistence import create_engine, create_session_factory
from aiscc.persistence.public_live import PublicLiveRepository
from aiscc.persistence.public_live_limits import PublicLiveLimits
from aiscc.public_live.edge_identity import RailwayEdgeIdentityAuthority
from aiscc.public_live.http import PublicLiveApp

LIVE_DATABASE_VARIABLE = "AISCC_PUBLIC_LIVE_DATABASE_URL"
PUBLIC_ORIGIN_VARIABLE = "PUBLIC_LIVE_API_ORIGIN"
EDGE_PROOF_VARIABLE = "AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST"
SOURCE_KEY_VARIABLE = "AISCC_PUBLIC_LIVE_SOURCE_HMAC_KEY"


@dataclass(frozen=True)
class IngressSettings:
    database_url: str
    public_origin: str
    source_key: bytes
    overwrite_proof_accepted: bool

    @classmethod
    def from_environment(cls, environ: Mapping[str, str] = os.environ) -> IngressSettings:
        # Presence is checked without reading provider material.
        if "AISCC_OPENAI_API_KEY" in environ or "OPENAI_API_KEY" in environ:
            raise ValueError("PUBLIC_INGRESS_PROVIDER_SECRET_DENIED")
        if "AISCC_DATABASE_URL" in environ:
            raise ValueError("PUBLIC_INGRESS_OWNER_DATABASE_DENIED")
        database_url = environ.get(LIVE_DATABASE_VARIABLE, "")
        origin = environ.get(PUBLIC_ORIGIN_VARIABLE, "")
        try:
            source_key = bytes.fromhex(environ.get(SOURCE_KEY_VARIABLE, ""))
        except ValueError:
            raise ValueError("PUBLIC_INGRESS_SOURCE_KEY_DENIED") from None
        if not database_url or len(source_key) < 32:
            raise ValueError("PUBLIC_INGRESS_CONFIGURATION_DENIED")
        return cls(
            database_url,
            origin,
            source_key,
            environ.get(EDGE_PROOF_VARIABLE) == "HOSTED_OVERWRITE_PROOF_ACCEPTED_V1",
        )


class HostedPublicLiveIngress:
    """Owns only the Public Live ASGI app and its distinct Live DB engine."""

    def __init__(self, application: PublicLiveApp, engine: AsyncEngine) -> None:
        self.application = application
        self.engine = engine

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "lifespan":
            await self.application(scope, receive, send)
            return
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await self.engine.dispose()
                await send({"type": "lifespan.shutdown.complete"})
                return


def create_app() -> HostedPublicLiveIngress:
    settings = IngressSettings.from_environment()
    engine = create_engine(settings.database_url)
    repository = PublicLiveRepository(create_session_factory(engine))
    source = RailwayEdgeIdentityAuthority(
        public_origin=settings.public_origin,
        campaign="public-live-v1",
        key_version="v1",
        secret=settings.source_key,
        overwrite_proof_accepted=settings.overwrite_proof_accepted,
    )
    # admission=None is intentional and release-safe. A later release task must
    # explicitly bind admission after hosted edge proof and L6 acceptance.
    application = PublicLiveApp(source, PublicLiveLimits(repository), None)
    return HostedPublicLiveIngress(application, engine)
