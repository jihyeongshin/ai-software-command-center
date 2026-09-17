from __future__ import annotations

import asyncio
import os
import secrets
import subprocess
import sys
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import DBAPIError

from aiscc.persistence.database import create_engine, create_session_factory
from aiscc.persistence.public_live import PublicLiveRepository
from aiscc.persistence.public_live_limits import LimitsUnavailable, PublicLiveIngressLimits
from aiscc.public_live.http import PublicLiveApp
from aiscc.public_live.ingress import HostedPublicLiveIngress

EXPECTED_FUNCTIONS = (
    "admission_context(c text, b bytea)",
    "admit_checked_and_start(a jsonb, p jsonb)",
    "clock_lock()",
    "ingress_flood_consume_retained(c text, v text, s bytea)",
    "lock_run(r bytea)",
    "read_consume_retained(r bytea)",
    "read_key(c text, k bytea)",
    "run_context(r bytea)",
)
EXPECTED_0021_FUNCTIONS = (
    "admission_context(c text, b bytea)",
    "admit_checked_and_start(a jsonb, p jsonb)",
    "clock_lock()",
    "flood_consume(c text, v text, s bytea)",
    "lock_run(r bytea)",
    "read_consume(r bytea)",
    "read_key(c text, k bytea)",
    "run_context(r bytea)",
)


def test_upgrade_0020_to_0023() -> None:
    base = make_url(os.environ["AISCC_TEST_DATABASE_URL"])
    assert base.host == "127.0.0.1"
    name = "aiscc_ingress_upgrade_" + uuid4().hex

    async def database(sql: str) -> None:
        engine = create_engine(base.set(database="postgres").render_as_string(False))
        try:
            async with engine.connect() as connection:
                connection = await connection.execution_options(isolation_level="AUTOCOMMIT")
                await connection.execute(text(sql))
        finally:
            await engine.dispose()

    asyncio.run(database(f'CREATE DATABASE "{name}"'))
    url = base.set(database=name).render_as_string(False)
    try:
        for revision in (
            "20260917_0020",
            "20260917_0021",
            "20260918_0022",
            "20260918_0023",
        ):
            result = subprocess.run(
                [sys.executable, "-B", "-m", "alembic", "upgrade", revision],
                env=os.environ | {"AISCC_DATABASE_URL": url, "PYTHONDONTWRITEBYTECODE": "1"},
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0, result.stderr.replace(url, "<TEST_DB>")

        async def verify() -> None:
            engine = create_engine(url)
            try:
                async with engine.connect() as connection:
                    assert await connection.scalar(
                        text("SELECT version_num FROM alembic_version")
                    ) == ("20260918_0023")
                    row = (
                        await connection.execute(
                            text(
                                "SELECT rolcanlogin,rolinherit,rolsuper,rolcreatedb,"
                                "rolcreaterole,rolbypassrls FROM pg_roles "
                                "WHERE rolname='aiscc_public_live_ingress'"
                            )
                        )
                    ).one()
                    assert tuple(row) == (False, False, False, False, False, False)
            finally:
                await engine.dispose()

        asyncio.run(verify())

        restored = subprocess.run(
            [sys.executable, "-B", "-m", "alembic", "downgrade", "20260917_0021"],
            env=os.environ | {"AISCC_DATABASE_URL": url, "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True,
            text=True,
        )
        assert restored.returncode == 0, restored.stderr.replace(url, "<TEST_DB>")

        async def verify_0021_surface() -> None:
            engine = create_engine(url)
            try:
                async with engine.connect() as connection:
                    assert await connection.scalar(
                        text("SELECT version_num FROM alembic_version")
                    ) == ("20260917_0021")
                    functions = (
                        (
                            await connection.execute(
                                text(
                                    "SELECT p.proname||'('||"
                                    "pg_get_function_identity_arguments(p.oid)||')' "
                                    "FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace "
                                    "WHERE n.nspname='public_live_api' AND "
                                    "has_function_privilege("
                                    "'aiscc_public_live_ingress',p.oid,'EXECUTE') ORDER BY 1"
                                )
                            )
                        )
                        .scalars()
                        .all()
                    )
                    assert tuple(functions) == EXPECTED_0021_FUNCTIONS
            finally:
                await engine.dispose()

        asyncio.run(verify_0021_surface())
        reapplied = subprocess.run(
            [sys.executable, "-B", "-m", "alembic", "upgrade", "20260918_0023"],
            env=os.environ | {"AISCC_DATABASE_URL": url, "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True,
            text=True,
        )
        assert reapplied.returncode == 0, reapplied.stderr.replace(url, "<TEST_DB>")

        async def add_downgrade_guard_member() -> None:
            engine = create_engine(url)
            try:
                async with engine.begin() as connection:
                    await connection.execute(text("CREATE ROLE aiscc_test_ingress_member"))
                    await connection.execute(
                        text("GRANT aiscc_public_live_ingress TO aiscc_test_ingress_member")
                    )
            finally:
                await engine.dispose()

        asyncio.run(add_downgrade_guard_member())
        guarded = subprocess.run(
            [sys.executable, "-B", "-m", "alembic", "downgrade", "20260917_0020"],
            env=os.environ | {"AISCC_DATABASE_URL": url, "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True,
            text=True,
        )
        assert guarded.returncode != 0
        assert "PUBLIC_LIVE_INGRESS_ROLE_HAS_MEMBERS" in guarded.stderr

        async def remove_downgrade_guard_member() -> None:
            engine = create_engine(url)
            try:
                async with engine.begin() as connection:
                    await connection.execute(text("DROP ROLE aiscc_test_ingress_member"))
            finally:
                await engine.dispose()

        asyncio.run(remove_downgrade_guard_member())
    finally:
        asyncio.run(database(f'DROP DATABASE "{name}"'))


def test_fresh_head_ingress_authority_and_startup_identity(l2_url: str) -> None:
    password = secrets.token_urlsafe(32)
    broad_password = secrets.token_urlsafe(32)
    worker_password = secrets.token_urlsafe(32)
    initializer_password = secrets.token_urlsafe(32)

    async def check() -> None:
        admin = create_engine(l2_url)
        base = make_url(l2_url)
        ingress = None
        peer = None

        async def role_engine(role: str, role_password: str):
            return create_engine(
                base.set(username=role, password=role_password).render_as_string(False)
            )

        async def lifespan(engine, *, accepted: bool) -> None:
            app = HostedPublicLiveIngress(PublicLiveApp(None, None, None), engine)
            messages = iter(
                (
                    {"type": "lifespan.startup"},
                    {"type": "lifespan.shutdown"},
                )
            )
            sent: list[dict[str, str]] = []

            async def receive() -> dict[str, str]:
                return next(messages)

            async def send(message: dict[str, str]) -> None:
                sent.append(message)

            if accepted:
                await app({"type": "lifespan"}, receive, send)  # type: ignore[arg-type]
                assert sent == [
                    {"type": "lifespan.startup.complete"},
                    {"type": "lifespan.shutdown.complete"},
                ]
            else:
                with pytest.raises(RuntimeError, match="PUBLIC_INGRESS_RUNTIME_IDENTITY_DENIED"):
                    await app({"type": "lifespan"}, receive, send)  # type: ignore[arg-type]
                assert sent == []
                await engine.dispose()

        async def assert_denied(engine, statement: str) -> None:
            async with engine.connect() as connection:
                transaction = await connection.begin()
                try:
                    with pytest.raises(DBAPIError) as captured:
                        await connection.execute(text(statement))
                    assert getattr(captured.value.orig, "sqlstate", None) == "42501"
                finally:
                    await transaction.rollback()

        async def assert_reachable(engine, statement: str) -> None:
            async with engine.connect() as connection:
                transaction = await connection.begin()
                try:
                    try:
                        await connection.execute(text(statement))
                    except DBAPIError as exc:
                        assert getattr(exc.orig, "sqlstate", None) not in {"42501", "42883"}
                finally:
                    await transaction.rollback()

        try:
            async with admin.begin() as connection:
                assert await connection.scalar(text("SELECT version_num FROM alembic_version")) == (
                    "20260918_0023"
                )
                await connection.execute(
                    text(
                        "CREATE ROLE aiscc_live_ingress_login LOGIN INHERIT "
                        "NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS "
                        f"PASSWORD '{password}'"
                    )
                )
                await connection.execute(
                    text("GRANT aiscc_public_live_ingress TO aiscc_live_ingress_login")
                )
                await connection.execute(
                    text(
                        "CREATE ROLE aiscc_test_broad_runtime_login LOGIN INHERIT "
                        "NOSUPERUSER NOCREATEDB NOCREATEROLE NOBYPASSRLS "
                        f"PASSWORD '{broad_password}'"
                    )
                )
                await connection.execute(
                    text(
                        "GRANT aiscc_public_live_ingress,aiscc_public_live_runtime "
                        "TO aiscc_test_broad_runtime_login"
                    )
                )
                await connection.execute(
                    text(f"ALTER ROLE aiscc_live_worker_login PASSWORD '{worker_password}'")
                )
                await connection.execute(
                    text(
                        f"ALTER ROLE aiscc_live_initializer_login PASSWORD '{initializer_password}'"
                    )
                )

            ingress = await role_engine("aiscc_live_ingress_login", password)
            async with ingress.connect() as connection:
                functions = (
                    (
                        await connection.execute(
                            text(
                                "SELECT p.proname||'('||"
                                "pg_get_function_identity_arguments(p.oid)||')' "
                                "FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace "
                                "WHERE n.nspname='public_live_api' AND "
                                "has_function_privilege(current_user,p.oid,'EXECUTE') ORDER BY 1"
                            )
                        )
                    )
                    .scalars()
                    .all()
                )
                assert tuple(functions) == EXPECTED_FUNCTIONS
                raw_dml = await connection.scalar(
                    text(
                        "SELECT count(*) FROM pg_class c JOIN pg_namespace n "
                        "ON n.oid=c.relnamespace WHERE n.nspname IN ('public','public_live_api') "
                        "AND c.relkind IN ('r','p','v','m','S') AND ("
                        "has_table_privilege(current_user,c.oid,'INSERT') OR "
                        "has_table_privilege(current_user,c.oid,'UPDATE') OR "
                        "has_table_privilege(current_user,c.oid,'DELETE'))"
                    )
                )
                assert raw_dml == 0
                identity = (
                    await connection.execute(
                        text(
                            "SELECT session_user,current_user,"
                            "pg_has_role(session_user,'aiscc_public_live_ingress','USAGE'),"
                            "pg_has_role(session_user,'aiscc_public_live_runtime','USAGE'),"
                            "pg_has_role(session_user,'aiscc_public_live_reconciler','USAGE'),"
                            "pg_has_role(session_user,'aiscc_public_live_execution','USAGE'),"
                            "pg_has_role(session_user,'aiscc_public_live_initializer','USAGE')"
                        )
                    )
                ).one()
                assert tuple(identity) == (
                    "aiscc_live_ingress_login",
                    "aiscc_live_ingress_login",
                    True,
                    False,
                    False,
                    False,
                    False,
                )

            limits = PublicLiveIngressLimits(PublicLiveRepository(create_session_factory(ingress)))
            first = await limits.flood("public-live-v1", "v1", bytes(32))
            if first.retry_after <= 5:
                await asyncio.sleep(first.retry_after + 0.1)
                first = await limits.flood("public-live-v1", "v1", bytes(32))
            assert first.allowed
            peer = await role_engine("aiscc_live_ingress_login", password)
            peer_limits = PublicLiveIngressLimits(
                PublicLiveRepository(create_session_factory(peer))
            )
            async with admin.begin() as connection:
                await connection.execute(
                    text(
                        "UPDATE public_live_shared_limit SET attempts=119 "
                        "WHERE campaign_id='public-live-v1' AND kind='SOURCE' "
                        "AND identity=:source AND bucket=:bucket"
                    ),
                    {"source": bytes(32), "bucket": first.bucket},
                )
            source_boundary = await asyncio.gather(
                limits.flood("public-live-v1", "v1", bytes(32)),
                peer_limits.flood("public-live-v1", "v1", bytes(32)),
            )
            assert sorted(result.allowed for result in source_boundary) == [False, True]
            async with admin.begin() as connection:
                await connection.execute(
                    text(
                        "UPDATE public_live_shared_limit SET attempts=1199 "
                        "WHERE campaign_id='public-live-v1' AND kind='CAMPAIGN' "
                        "AND bucket=:bucket"
                    ),
                    {"bucket": first.bucket},
                )
            campaign_boundary = await asyncio.gather(
                limits.flood("public-live-v1", "v1", b"a" * 32),
                peer_limits.flood("public-live-v1", "v1", b"b" * 32),
            )
            assert sorted(result.allowed for result in campaign_boundary) == [False, True]
            with pytest.raises(LimitsUnavailable, match="LIVE_UNAVAILABLE"):
                await limits.flood("not-the-fixed-campaign", "v1", b"c" * 32)
            async with admin.connect() as connection:
                assert await connection.scalar(text("SELECT count(*) FROM public_campaign")) == 0
                counts = (
                    await connection.execute(
                        text(
                            "SELECT kind,count(*),sum(attempts) "
                            "FROM public_live_shared_limit WHERE bucket=:bucket "
                            "GROUP BY kind ORDER BY kind"
                        ),
                        {"bucket": first.bucket},
                    )
                ).all()
                assert [tuple(row) for row in counts] == [
                    ("CAMPAIGN", 1, 1201),
                    ("SOURCE", 2, 122),
                ]

            for statement in (
                "SELECT public_live_api.clock_lock()",
                "SELECT public_live_api.ingress_flood_consume_retained("
                "'public-live-v1','v1',decode(repeat('00',32),'hex'))",
                "SELECT public_live_api.read_consume_retained(decode(repeat('00',16),'hex'))",
                "SELECT public_live_api.read_key('missing',decode(repeat('00',32),'hex'))",
                "SELECT public_live_api.admission_context('missing',decode(repeat('00',32),'hex'))",
                "SELECT public_live_api.admit_checked_and_start('{}'::jsonb,'{}'::jsonb)",
                "SELECT public_live_api.run_context(decode(repeat('00',16),'hex'))",
                "SELECT (public_live_api.lock_run(decode(repeat('00',16),'hex'))).run_id",
            ):
                await assert_reachable(ingress, statement)

            for statement in (
                "INSERT INTO public.public_start_event DEFAULT VALUES",
                "UPDATE public.public_start_request SET phase=phase WHERE false",
                "DELETE FROM public.public_start_request WHERE false",
                "SELECT public_live_api.flood_consume("
                "'missing','v1',decode(repeat('00',32),'hex'))",
                "SELECT public_live_api.flood_consume_retained("
                "'missing','v1',decode(repeat('00',32),'hex'))",
                "SELECT public_live_api.read_consume(decode(repeat('00',16),'hex'))",
                "SELECT public_live_api.maintain_limiter()",
                "SELECT public_live_api.pipeline_context(decode(repeat('00',16),'hex'))",
                "SELECT public_live_api.execution_context(decode(repeat('00',16),'hex'))",
                "SELECT public_live_api.worker_claim_next("
                "decode(repeat('00',16),'hex'),decode(repeat('00',16),'hex'),1,"
                "decode(repeat('00',32),'hex'))",
                "SELECT public_live_api.start_next(decode(repeat('00',16),'hex'))",
                "SELECT public_live_api.settle("
                "decode(repeat('00',16),'hex'),0,decode(repeat('00',32),'hex'))",
            ):
                await assert_denied(ingress, statement)
            await ingress.dispose()

            await lifespan(await role_engine("aiscc_live_ingress_login", password), accepted=True)
            await lifespan(admin, accepted=False)
            admin = create_engine(l2_url)
            await lifespan(
                await role_engine("aiscc_test_broad_runtime_login", broad_password),
                accepted=False,
            )
            await lifespan(
                await role_engine("aiscc_live_worker_login", worker_password), accepted=False
            )
            await lifespan(
                await role_engine("aiscc_live_initializer_login", initializer_password),
                accepted=False,
            )

            async with admin.begin() as connection:
                await connection.execute(
                    text("GRANT aiscc_public_live_runtime TO aiscc_live_ingress_login")
                )
            await lifespan(await role_engine("aiscc_live_ingress_login", password), accepted=False)
        finally:
            if peer is not None:
                await peer.dispose()
            if ingress is not None:
                await ingress.dispose()
            await admin.dispose()
            cleanup = create_engine(l2_url)
            try:
                async with cleanup.begin() as connection:
                    await connection.execute(
                        text(
                            "DROP ROLE IF EXISTS aiscc_live_ingress_login,"
                            "aiscc_test_broad_runtime_login"
                        )
                    )
            finally:
                await cleanup.dispose()

    asyncio.run(check())
