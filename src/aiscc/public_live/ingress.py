"""Dedicated hosted Public Live ingress composition; never imports the owner API."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.types import Receive, Scope, Send

from aiscc.persistence import create_engine, create_session_factory
from aiscc.persistence.public_live import PublicLiveRepository
from aiscc.persistence.public_live_limits import PublicLiveIngressLimits
from aiscc.public_live.edge_identity import RailwayEdgeIdentityAuthority
from aiscc.public_live.http import LocalAdmissionBinding, PublicLiveApp
from aiscc.public_live.identity import IdentityPolicy
from aiscc.public_live.luna_profile import hosted_luna_profile
from aiscc.public_live.service import AdmissionService
from aiscc.public_live.start_authority import StartContract

LIVE_DATABASE_VARIABLE = "AISCC_PUBLIC_LIVE_DATABASE_URL"
PUBLIC_ORIGIN_VARIABLE = "PUBLIC_LIVE_API_ORIGIN"
EDGE_PROOF_VARIABLE = "AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST"
SOURCE_KEY_VARIABLE = "AISCC_PUBLIC_LIVE_SOURCE_HMAC_KEY"
CAMPAIGN_ID = "public-live-v1"
HMAC_VERSION = "v1"
ADMISSION_BRIDGE_NETWORKS = ("127.0.0.1/32",)
ADMISSION_BRIDGE_PEER = "127.0.0.1"
ADMISSION_BRIDGE_PROOF = "HOSTED_RAILWAY_EDGE_TO_LOCAL_ADMISSION_V1"
INGRESS_LOGIN = "aiscc_live_ingress_login"
INGRESS_CAPABILITY = "aiscc_public_live_ingress"
FORBIDDEN_CAPABILITIES = (
    "aiscc_public_live_runtime",
    "aiscc_public_live_reconciler",
    "aiscc_public_live_execution",
    "aiscc_public_live_initializer",
)


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
                await verify_runtime_identity(self.engine)
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await self.engine.dispose()
                await send({"type": "lifespan.shutdown.complete"})
                return


async def verify_runtime_identity(engine: AsyncEngine) -> None:
    """Fail closed unless the hosted login has only the ingress capability."""
    query = text(
        "SELECT session_user,current_user,r.rolsuper,r.rolcreatedb,r.rolcreaterole,"
        "r.rolbypassrls,pg_has_role(session_user,:ingress,'USAGE'),"
        "pg_has_role(session_user,:runtime,'USAGE'),"
        "pg_has_role(session_user,:reconciler,'USAGE'),"
        "pg_has_role(session_user,:execution,'USAGE'),"
        "pg_has_role(session_user,:initializer,'USAGE') "
        "FROM pg_roles r WHERE r.rolname=session_user"
    )
    parameters = {
        "ingress": INGRESS_CAPABILITY,
        "runtime": FORBIDDEN_CAPABILITIES[0],
        "reconciler": FORBIDDEN_CAPABILITIES[1],
        "execution": FORBIDDEN_CAPABILITIES[2],
        "initializer": FORBIDDEN_CAPABILITIES[3],
    }
    try:
        async with engine.connect() as connection:
            row = (await connection.execute(query, parameters)).one_or_none()
    except Exception as exc:
        raise RuntimeError("PUBLIC_INGRESS_RUNTIME_IDENTITY_DENIED") from exc
    if row is None or tuple(row) != (
        INGRESS_LOGIN,
        INGRESS_LOGIN,
        False,
        False,
        False,
        False,
        True,
        False,
        False,
        False,
        False,
    ):
        raise RuntimeError("PUBLIC_INGRESS_RUNTIME_IDENTITY_DENIED")


def compose_admission(repository: PublicLiveRepository, source_key: bytes) -> LocalAdmissionBinding:
    """Bind accepted server-owned pins to the existing atomic admission owner."""
    contract = StartContract.load()
    profile = hosted_luna_profile()
    pins = (
        contract.payload.get("scenario_id"),
        contract.payload.get("scenario_version"),
        contract.payload.get("repository_identity"),
        contract.payload.get("repository_version"),
        contract.payload.get("provider_profile_id"),
        contract.payload.get("provider_profile_version"),
        contract.payload.get("tool_registry_id"),
        contract.payload.get("tool_registry_version"),
    )
    expected = (
        profile.public_scenario_identity,
        profile.public_scenario_version,
        profile.public_repository_identity,
        profile.public_repository_version,
        profile.profile_id,
        profile.version,
        profile.tool_registry_id,
        profile.tool_registry_version,
    )
    try:
        policy_digest = bytes.fromhex(contract.digest)
        content_digest = bytes.fromhex(profile.public_repository_version)
    except ValueError:
        raise RuntimeError("PUBLIC_INGRESS_ADMISSION_PINS_DENIED") from None
    if pins != expected or len(policy_digest) != 32 or len(content_digest) != 32:
        raise RuntimeError("PUBLIC_INGRESS_ADMISSION_PINS_DENIED")
    identity = IdentityPolicy(
        ADMISSION_BRIDGE_NETWORKS,
        ADMISSION_BRIDGE_PROOF,
        CAMPAIGN_ID,
        HMAC_VERSION,
        source_key,
    )
    service = AdmissionService(
        repository,
        identity,
        policy_digest=policy_digest,
        content_digest=content_digest,
        start_contract=contract,
    )
    return LocalAdmissionBinding(service, ADMISSION_BRIDGE_PEER)


def create_app() -> HostedPublicLiveIngress:
    settings = IngressSettings.from_environment()
    engine = create_engine(settings.database_url)
    repository = PublicLiveRepository(create_session_factory(engine))
    source = RailwayEdgeIdentityAuthority(
        public_origin=settings.public_origin,
        campaign=CAMPAIGN_ID,
        key_version=HMAC_VERSION,
        secret=settings.source_key,
        overwrite_proof_accepted=settings.overwrite_proof_accepted,
    )
    application = PublicLiveApp(
        source,
        PublicLiveIngressLimits(repository),
        compose_admission(repository, settings.source_key),
    )
    return HostedPublicLiveIngress(application, engine)
