"""Isolated implementation proofs; never operational golden-cycle evidence."""

import asyncio
import os
import subprocess
from dataclasses import replace
from pathlib import Path
from uuid import uuid4

import pytest
from sqlalchemy import func, select, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import create_async_engine

from aiscc.next_action.genesis import GenesisAuthorityRepository, GenesisContextV1
from aiscc.next_action.models import (
    NextActionProposal,
    NextActionSelectionMode,
    default_next_action_policy_authority,
)
from aiscc.next_action.repository import PostgresNextActionRepository
from aiscc.persistence import create_engine, create_session_factory
from aiscc.persistence.models import (
    AdmittedCycleRow,
    GenesisAuthorityRow,
    ProjectMemoryEntryRow,
    WorkRunRow,
)
from aiscc.task_authority.authority import _bind_repository_once
from aiscc.task_authority.contracts import TaskContractError
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository
from tests.unit.next_action.test_genesis_bootstrap import NOW


@pytest.fixture
def database_url():
    # Missing infrastructure is a failed required proof, never a skip.
    return os.environ["AISCC_TEST_DATABASE_URL"]


async def genesis_fixture(database_url, tmp_path):
    label = uuid4().hex
    engine = create_engine(database_url)
    sessions = create_session_factory(engine)
    context = GenesisContextV1(
        "genesis-project-" + label, "repository", str(tmp_path.resolve()), "1" * 40, "P2-4"
    )
    genesis = GenesisAuthorityRepository(sessions, context=context)
    genesis_writer = genesis._bind_writer_once()
    authority = await genesis_writer.issue(authority_id="genesis-" + label, issued_at=NOW)
    policy_owner = default_next_action_policy_authority()
    eligibility, selection, descriptors = policy_owner.issue_genesis_policy_catalog(
        authority=authority, now=NOW
    )
    repo = PostgresExternalTaskAuthorityRepository(sessions)
    writer = _bind_repository_once(repo)
    actions = PostgresNextActionRepository(
        sessions,
        eligibility_policy=eligibility,
        selection_policy=selection,
        descriptors=descriptors,
        policy_authority=policy_owner,
        task_authority_verifier=repo,
        genesis_repository=genesis,
    )
    await actions.enroll_configured_authority(NOW)
    parameters = {
        "genesis_authority_ref": authority.authority_ref,
        "genesis_authority_fingerprint": authority.fingerprint,
    }
    selected, candidate = await actions.select(
        selection_id="genesis-selection-" + label,
        project_id=context.project_id,
        expected_project_revision=0,
        mode=NextActionSelectionMode.SELF_DOGFOOD_GENESIS,
        proposals=(
            NextActionProposal(
                "proposal-" + label,
                context.project_id,
                descriptors[0].action_ref,
                parameters,
                "Explicit one-time Genesis",
            ),
        ),
        now=NOW,
    )
    return dict(
        engine=engine,
        sessions=sessions,
        context=context,
        genesis=genesis,
        genesis_writer=genesis_writer,
        authority=authority,
        actions=actions,
        selected=selected,
        candidate=candidate,
        descriptor=descriptors[0],
        repo=repo,
        writer=writer,
        project_id=context.project_id,
    )


async def current(f, reader=None):
    async with f["sessions"]() as session, session.begin():
        return await (reader or f["genesis"]).verify_current(
            session,
            f["authority"].authority_ref,
            f["authority"].fingerprint,
            selection_id=f["selected"].selection_id,
        )


@pytest.mark.postgres
def test_empty_genesis_retry_restart_context_mismatch_and_immutable_storage(database_url, tmp_path):
    async def scenario():
        f = await genesis_fixture(database_url, tmp_path)
        try:
            assert await current(f) == f["authority"]
            restarted = GenesisAuthorityRepository(f["sessions"], context=f["context"])
            assert await current(f, restarted) == f["authority"]
            assert (
                await restarted._bind_writer_once().issue(
                    authority_id=f["authority"].value["genesis_authority_id"], issued_at=NOW
                )
                == f["authority"]
            )
            with pytest.raises(TaskContractError, match="different genesis authority"):
                await f["genesis_writer"].issue(authority_id="different", issued_at=NOW)
            for changes in [
                dict(repository_id="other"),
                dict(repository_root=str(tmp_path / "other")),
                dict(base_commit="2" * 40),
                dict(phase_id="P3"),
                dict(project_id="other"),
            ]:
                with pytest.raises(TaskContractError, match="GENESIS_NOT_ELIGIBLE"):
                    await current(
                        f,
                        GenesisAuthorityRepository(
                            f["sessions"], context=replace(f["context"], **changes)
                        ),
                    )
            async with f["sessions"]() as session:
                for model in (AdmittedCycleRow, ProjectMemoryEntryRow, WorkRunRow):
                    assert (
                        await session.scalar(
                            select(func.count())
                            .select_from(model)
                            .where(model.project_id == f["project_id"])
                        )
                        == 0
                    )
                assert (
                    await session.scalar(
                        select(func.count())
                        .select_from(GenesisAuthorityRow)
                        .where(GenesisAuthorityRow.project_id == f["project_id"])
                    )
                    == 1
                )
            for sql in (
                "UPDATE self_dogfood_genesis_authority SET fingerprint=fingerprint "
                "WHERE record_id=:ref",
                "DELETE FROM self_dogfood_genesis_authority WHERE record_id=:ref",
                "TRUNCATE self_dogfood_genesis_authority",
            ):
                with pytest.raises(DBAPIError, match="append-only"):
                    async with f["sessions"]() as session, session.begin():
                        await session.execute(text(sql), {"ref": f["authority"].authority_ref})
            # Deliberate corruption is rolled back; it can never become authority.
            async with f["sessions"]() as session:
                tx = await session.begin()
                try:
                    await session.execute(text("SET LOCAL session_replication_role=replica"))
                    await session.execute(
                        text(
                            "UPDATE self_dogfood_genesis_authority SET fingerprint=:fp "
                            "WHERE record_id=:ref"
                        ),
                        {"fp": "0" * 64, "ref": f["authority"].authority_ref},
                    )
                    with pytest.raises(TaskContractError, match="AUTHORITY_CORRUPTION"):
                        await f["genesis"].read(
                            session, f["authority"].authority_ref, f["authority"].fingerprint
                        )
                finally:
                    await tx.rollback()
            assert await current(f) == f["authority"]
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
def test_genesis_additive_migration_empty_and_nonempty_preservation(database_url, tmp_path):
    parsed = make_url(database_url)
    assert parsed.host in {"127.0.0.1", "localhost"}
    name = "aiscc_genesis_migration_" + uuid4().hex
    isolated = parsed.set(database=name).render_as_string(hide_password=False)

    async def admin(sql):
        engine = create_async_engine(database_url, isolation_level="AUTOCOMMIT")
        try:
            async with engine.connect() as connection:
                await connection.execute(text(sql))
        finally:
            await engine.dispose()

    def migrate(*args):
        result = subprocess.run(
            [str(Path.cwd() / ".venv/Scripts/python.exe"), "-B", "-m", "alembic", *args],
            env=os.environ | {"AISCC_DATABASE_URL": isolated},
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        return result.returncode, (result.stdout + result.stderr).replace(isolated, "<TEST_DB_URL>")

    async def snapshot():
        engine = create_async_engine(isolated)
        try:
            async with engine.connect() as connection:
                return (
                    await connection.scalar(text("SELECT version_num FROM alembic_version")),
                    tuple(
                        (
                            await connection.execute(
                                text(
                                    "SELECT record_id,project_id,record_kind,canonical_body,"
                                "fingerprint,issued_at "
                                    "FROM self_dogfood_genesis_authority ORDER BY record_id"
                                )
                            )
                        ).all()
                    ),
                    tuple(
                        (
                            await connection.execute(
                                text(
                                    "SELECT tablename FROM pg_tables "
                                "WHERE schemaname='public' ORDER BY tablename"
                                )
                            )
                        ).all()
                    ),
                    tuple(
                        (
                            await connection.execute(
                                text(
                                    "SELECT tgname,pg_get_triggerdef(oid) FROM pg_trigger "
                                    "WHERE tgrelid='self_dogfood_genesis_authority'::regclass "
                                "ORDER BY tgname"
                                )
                            )
                        ).all()
                    ),
                )
        finally:
            await engine.dispose()

    asyncio.run(admin(f'CREATE DATABASE "{name}"'))
    try:
        assert migrate("upgrade", "head")[0] == 0
        assert asyncio.run(snapshot())[:2] == ("20260916_0016", ())
        assert migrate("downgrade", "20260914_0011")[0] == 0
        assert migrate("upgrade", "head")[0] == 0

        async def enroll():
            f = await genesis_fixture(isolated, tmp_path)
            await f["engine"].dispose()

        asyncio.run(enroll())
        before = asyncio.run(snapshot())
        assert len(before[1]) == 1
        code, output = migrate("downgrade", "20260914_0011")
        assert code != 0 and "GENESIS_NONEMPTY_DOWNGRADE_FORBIDDEN" in output
        assert asyncio.run(snapshot()) == before
    finally:
        asyncio.run(admin(f'DROP DATABASE "{name}"'))


@pytest.mark.postgres
def test_existing_owner_work_run_denies_initial_genesis(database_url, tmp_path):
    from tests.integration.evidence import test_postgres_evidence_admission as e

    async def scenario():
        engine = create_engine(database_url)
        sessions = create_session_factory(engine)
        label = uuid4().hex
        project = "nonempty-" + label
        authorities = e.WorkflowAuthorities()
        kernel = e.WorkflowKernel(
            e.PostgresTransitionRepository(
                sessions, e.TransitionEvaluator(authorities.system, authorities.future)
            )
        )
        try:
            request = replace(
                e.transition_request(
                    run_id="owner-run-" + label,
                    task_id="owner-task-" + label,
                    source=None,
                    version=0,
                    target=e.WorkflowState.READY,
                ),
                project_id=project,
            )
            assert (
                await kernel.request_transition(request, authorities.facts(request))
            ).outcome is e.DecisionOutcome.ADMITTED
            genesis = GenesisAuthorityRepository(
                sessions,
                context=GenesisContextV1(project, "repository", str(tmp_path), "1" * 40, "P2-4"),
            )
            with pytest.raises(TaskContractError, match="pre-existing operational WorkRun"):
                await genesis._bind_writer_once().issue(
                    authority_id="genesis-" + label, issued_at=NOW
                )
            async with sessions() as session:
                assert (
                    await session.scalar(
                        select(func.count())
                        .select_from(GenesisAuthorityRow)
                        .where(GenesisAuthorityRow.project_id == project)
                    )
                    == 0
                )
        finally:
            await engine.dispose()

    asyncio.run(scenario())
