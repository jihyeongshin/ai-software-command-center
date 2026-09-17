from __future__ import annotations

import asyncio
from dataclasses import replace
from datetime import timedelta
from hashlib import sha256
from uuid import uuid4

import pytest
from sqlalchemy import event, select, text

from aiscc.contracts.workflow import WorkflowState
from aiscc.persistence.models import (
    ExternalIdeExecutionStartPermitRow,
    ExternalIdeExecutionStartRow,
)
from aiscc.persistence.repository import HistoricalTransitionProvenanceError
from aiscc.providers.authority import ExecutionReferenceAuthority
from aiscc.providers.external_ide import (
    START_PREFIX,
    ExternalIdeExecutionRepository,
    ExternalIdeExecutionStartRepository,
    LocalGitObserver,
    _bind_external_ide_start_writer,
    _bind_external_ide_writer,
)
from aiscc.self_dogfood import build_ready_request, materialize_task_spec
from aiscc.task_authority.authority import _bind_repository_once
from aiscc.task_authority.contracts import TaskContractBodyV1, plain
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository
from aiscc.workflow.models import DecisionOutcome, GuardId
from tests.integration.self_dogfood.test_task_ready_entry import composition, enter, issue
from tests.integration.task_authority.test_task_contract_durability import (
    contract_fixture,
    successor_body,
)
from tests.integration.task_authority.test_task_contract_durability import (
    database_url as database_url,
)
from tests.unit.providers.test_external_ide_execution_ingress import GIT, NOW, git, git_fixture

TASK = b"bounded temporary repository task"


def start_repository(f, *, clock=lambda: NOW):
    return ExternalIdeExecutionStartRepository(
        f["sessions"],
        f["repo"],
        LocalGitObserver(GIT, clock=clock),
        system_authority=f["args"]["system_authority"],
        transition_repository=f["args"]["transition_repository"],
        clock=clock,
    )


async def fixture(database_url, tmp_path):
    base = git_fixture(tmp_path)
    f = await contract_fixture(database_url, tmp_path)
    f["repository_binding"]["base_commit"] = base
    f["repo"] = PostgresExternalTaskAuthorityRepository(f["sessions"])
    f["writer"] = _bind_repository_once(f["repo"])
    f["writer"].configure_task_contracts(
        project_id=f["project_id"],
        repository_binding=f["repository_binding"],
        next_action_repository=f["actions"],
        evidence_repository=f["evidence"],
    )
    f["body"] = TaskContractBodyV1(
        plain(f["body"].value) | dict(repository_binding=f["repository_binding"])
    )
    receipt = await issue(f)
    args = composition(f)
    assert (await enter(f, receipt, args)).resulting_state is WorkflowState.READY
    spec = await materialize_task_spec(
        f["repo"],
        receipt,
        f["repository_binding"],
        f["body"].value["source_next_action"]["action_ref"],
    )
    start = replace(
        build_ready_request(
            spec,
            work_run_id=args["work_run_id"],
            transition_request_id="external-start-" + uuid4().hex,
            requester_id="fixture-system",
            created_at=NOW,
        ),
        observed_state=WorkflowState.READY,
        observed_state_version=1,
        target_state=WorkflowState.RUNNING,
    )
    f.update(args=args, receipt=receipt, start=start, root=tmp_path)
    repo = start_repository(f)
    writer = _bind_external_ide_start_writer(repo)
    async with f["sessions"]() as session, session.begin():
        permit, token = await writer.issue(
            session,
            receipt=receipt,
            work_run_id=args["work_run_id"],
            state_version=1,
            ready_transition_id=args["transition_request_id"],
            inner_task_bytes=TASK,
            ttl=timedelta(minutes=10),
        )
    f.update(starts=repo, permit=permit, token=token, start_writer=writer)
    return f


async def start(f, **changes):
    return await f["starts"].start(
        **(
            dict(
                permit_id=f["permit"].value["permit_id"],
                capability=f["token"],
                inner_task_bytes=TASK,
                request=f["start"],
            )
            | changes
        )
    )


async def count_starts(f):
    async with f["sessions"]() as session:
        return len(
            (
                await session.scalars(
                    select(ExternalIdeExecutionStartRow).where(
                        ExternalIdeExecutionStartRow.work_run_id == f["args"]["work_run_id"]
                    )
                )
            ).all()
        )


async def completion_lease(f, version):
    repo = ExternalIdeExecutionRepository(
        f["sessions"], f["repo"], LocalGitObserver(GIT, clock=lambda: NOW), clock=lambda: NOW
    )
    writer = _bind_external_ide_writer(repo)
    async with f["sessions"]() as session, session.begin():
        return await writer.issue(
            session,
            receipt=f["receipt"],
            work_run_id=f["args"]["work_run_id"],
            state_version=version,
            start_transition_id=f["start"].transition_request_id,
            inner_task_bytes=TASK,
            expected_hashes={"src/file.txt": sha256(b"after\n").hexdigest()},
            ttl=timedelta(minutes=10),
        )


@pytest.mark.postgres
def test_external_ready_running_restart_and_completion_continuity(database_url, tmp_path):
    async def scenario():
        f = await fixture(database_url, tmp_path)
        try:
            with pytest.raises(HistoricalTransitionProvenanceError):
                await completion_lease(f, 2)
            decision = await start(f)
            assert decision.outcome is DecisionOutcome.ADMITTED
            assert (decision.resulting_state, decision.resulting_state_version) == (
                WorkflowState.RUNNING,
                2,
            )
            assert await count_starts(f) == 1
            assert await start(f) == decision
            rebuilt = start_repository(f)
            verified = await rebuilt.resolve(START_PREFIX + f["permit"].value["permit_id"])
            refs = ExecutionReferenceAuthority()
            assert refs.verify(verified.common_ref, f["start"], GuardId.G_EXECUTION_STARTED)
            assert not refs.verify(
                replace(verified.common_ref), f["start"], GuardId.G_EXECUTION_STARTED
            )
            assert not refs.verify(
                verified.common_ref,
                replace(f["start"], transition_request_id="other"),
                GuardId.G_EXECUTION_STARTED,
            )
            fact = f["args"]["system_authority"].issue_from_execution_ref(
                guard_id=GuardId.G_EXECUTION_STARTED,
                execution_ref=verified.common_ref,
                verifier=refs,
                request=f["start"],
            )
            assert fact.authority_ref == "p1-5:ExternalIdeExecutionStartRef"
            lease, _ = await completion_lease(f, 2)
            assert lease.value["state"] == "RUNNING"
            async with f["sessions"]() as session:
                row = await session.get(
                    ExternalIdeExecutionStartPermitRow, f["permit"].value["permit_id"]
                )
                assert f["token"].encode() not in bytes(row.canonical_body)
                assert (
                    await session.scalar(
                        text("SELECT count(*) FROM evidence_candidates WHERE task_contract_id=:c"),
                        {"c": f["body"].value["contract_id"]},
                    )
                    == 0
                )
                for table in (
                    "execution_attempts",
                    "external_ide_execution_submissions",
                    "judgments",
                    "human_gates",
                    "human_results",
                ):
                    # No producer/evidence side effects for this WorkRun.
                    assert (
                        await session.scalar(
                            text(f"SELECT count(*) FROM {table} WHERE work_run_id=:r"),
                            {"r": f["args"]["work_run_id"]},
                        )
                        == 0
                    )
            assert (tmp_path / "src/file.txt").read_bytes() == b"before\n"
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize(
    "bad",
    [
        "token",
        "task",
        "permit",
        "run",
        "version",
        "contract",
        "project",
        "target",
        "expiry",
        "base",
        "dirty",
        "revoked",
        "superseded",
    ],
)
def test_start_negative_exact_bindings_atomic(database_url, tmp_path, bad):
    async def scenario():
        f = await fixture(database_url, tmp_path)
        try:
            kw = {}
            if bad == "token":
                kw["capability"] = "wrong"
            if bad == "task":
                kw["inner_task_bytes"] = b"wrong"
            if bad == "permit":
                kw["permit_id"] = "missing"
            fields = {
                "run": dict(work_run_id="foreign"),
                "version": dict(observed_state_version=2),
                "contract": dict(task_contract_id="foreign"),
                "project": dict(project_id="foreign"),
                "target": dict(target_state=WorkflowState.FAILED),
            }
            if bad in fields:
                kw["request"] = replace(f["start"], **fields[bad])
            if bad == "expiry":
                f["starts"] = start_repository(f, clock=lambda: NOW + timedelta(hours=2))
            if bad == "base":
                git(tmp_path, "commit", "--allow-empty", "-qm", "drift")
            if bad == "dirty":
                (tmp_path / "src/file.txt").write_bytes(b"premature\n")
            if bad == "revoked":
                await f["writer"].revoke_task_contract(
                    project_id=f["project_id"],
                    contract_id=f["body"].value["contract_id"],
                    expected_version=1,
                    expected_body_sha256=f["body"].body_sha256,
                    effective_at=NOW,
                )
            if bad == "superseded":
                await f["writer"].issue_task_contract(
                    body=await successor_body(f, f["body"]),
                    expected_current_body_sha256=f["body"].body_sha256,
                    issued_at=NOW + timedelta(seconds=1),
                )
            with pytest.raises(ValueError):
                await start(f, **kw)
            assert await count_starts(f) == 0
            run = await f["args"]["transition_repository"].get_work_run(f["args"]["work_run_id"])
            assert (run.state, run.state_version) == (WorkflowState.READY, 1)
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
def test_concurrent_start_single_consumption_and_changed_retry(database_url, tmp_path):
    async def scenario():
        f = await fixture(database_url, tmp_path)
        try:
            results = await asyncio.gather(start(f), start(f), return_exceptions=True)
            passed = [r for r in results if not isinstance(r, Exception)]
            assert passed and all(r.outcome is DecisionOutcome.ADMITTED for r in passed)
            assert await count_starts(f) == 1
            with pytest.raises(ValueError):
                await start(f, request=replace(f["start"], transition_request_id="changed"))
            with pytest.raises(ValueError):
                await start(f, capability="wrong")
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize(
    "statement",
    [
        "UPDATE external_ide_execution_start_permits SET producer_kind=producer_kind",
        "DELETE FROM external_ide_execution_start_permits",
        "TRUNCATE external_ide_execution_start_permits CASCADE",
        "UPDATE external_ide_execution_starts SET producer_kind=producer_kind",
        "DELETE FROM external_ide_execution_starts",
        "TRUNCATE external_ide_execution_starts",
    ],
)
def test_start_authority_append_only(database_url, tmp_path, statement):
    async def scenario():
        f = await fixture(database_url, tmp_path)
        try:
            await start(f)
            with pytest.raises(Exception, match="append-only"):
                async with f["sessions"]() as session, session.begin():
                    await session.execute(text(statement))
            assert await count_starts(f) == 1
            await f["starts"].resolve(START_PREFIX + f["permit"].value["permit_id"])
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize("boundary", ["external_ide_execution_starts", "UPDATE work_runs"])
def test_start_rolls_back_with_owner_transaction_failure(database_url, tmp_path, boundary):
    async def scenario():
        f = await fixture(database_url, tmp_path)

        def fail(conn, cursor, statement, parameters, context, executemany):
            if boundary in statement and (
                statement.lstrip().startswith("INSERT") or statement.lstrip().startswith("UPDATE")
            ):
                raise RuntimeError("injected owner transaction failure")

        try:
            event.listen(f["engine"].sync_engine, "before_cursor_execute", fail)
            with pytest.raises(RuntimeError, match="injected"):
                await start(f)
            event.remove(f["engine"].sync_engine, "before_cursor_execute", fail)
            assert await count_starts(f) == 0
            run = await f["args"]["transition_repository"].get_work_run(f["args"]["work_run_id"])
            assert (run.state, run.state_version) == (WorkflowState.READY, 1)
            with pytest.raises(ValueError):
                await f["starts"].resolve(START_PREFIX + f["permit"].value["permit_id"])
        finally:
            if event.contains(f["engine"].sync_engine, "before_cursor_execute", fail):
                event.remove(f["engine"].sync_engine, "before_cursor_execute", fail)
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
def test_start_migration_upgrade_empty_downgrade_and_nonempty_preservation(database_url, tmp_path):
    import os
    import subprocess
    from pathlib import Path

    from sqlalchemy.engine import make_url
    from sqlalchemy.ext.asyncio import create_async_engine

    database = "start_migration_" + uuid4().hex
    url = make_url(database_url)
    isolated = url.set(database=database).render_as_string(hide_password=False)

    async def admin(sql):
        engine = create_async_engine(url.set(database="postgres"), isolation_level="AUTOCOMMIT")
        try:
            async with engine.connect() as connection:
                await connection.execute(text(sql))
        finally:
            await engine.dispose()

    def migration(*args):
        result = subprocess.run(
            [str(Path(".venv/Scripts/python.exe").resolve()), "-B", "-m", "alembic", *args],
            env=os.environ | {"AISCC_DATABASE_URL": isolated},
            capture_output=True,
        )
        return result.returncode, (result.stdout + result.stderr).decode("utf-8").replace(
            isolated, "<ISOLATED_DB>"
        )

    async def snapshot():
        engine = create_async_engine(isolated)
        try:
            async with engine.connect() as conn:
                revision = await conn.scalar(text("SELECT version_num FROM alembic_version"))
                tables = tuple(
                    (
                        await conn.execute(
                            text(
                                "SELECT tablename FROM pg_tables "
                                "WHERE schemaname='public' ORDER BY tablename"
                            )
                        )
                    ).all()
                )
                values = []
                for table in (
                    "external_ide_execution_start_permits",
                    "external_ide_execution_starts",
                ):
                    values.append(
                        tuple(
                            (
                                await conn.execute(
                                    text(
                                        f"SELECT body_sha256,canonical_body FROM {table} "
                                        "ORDER BY body_sha256"
                                    )
                                )
                            ).all()
                        )
                    )
                return revision, tables, tuple(values)
        finally:
            await engine.dispose()

    asyncio.run(admin(f'CREATE DATABASE "{database}"'))
    try:
        assert migration("upgrade", "20260914_0010")[0] == 0
        assert migration("upgrade", "head")[0] == 0
        empty = asyncio.run(snapshot())
        assert empty[0] == "20260917_0020" and empty[2] == ((), ())
        assert migration("downgrade", "20260914_0010")[0] == 0
        assert migration("upgrade", "head")[0] == 0
        assert asyncio.run(snapshot()) == empty

        async def populate():
            f = await fixture(isolated, tmp_path)
            try:
                await start(f)
            finally:
                await f["engine"].dispose()

        asyncio.run(populate())
        before = asyncio.run(snapshot())
        assert all(len(rows) == 1 for rows in before[2])
        code, output = migration("downgrade", "20260914_0010")
        assert code != 0 and "EXTERNAL_IDE_START_NONEMPTY_DOWNGRADE_FORBIDDEN" in output
        assert asyncio.run(snapshot()) == before
    finally:
        asyncio.run(admin(f'DROP DATABASE "{database}" WITH (FORCE)'))


@pytest.mark.postgres
def test_new_process_reconstructs_external_start_authenticity(database_url, tmp_path):
    import os
    import subprocess
    from pathlib import Path

    async def scenario():
        f = await fixture(database_url, tmp_path)
        try:
            await start(f)
            code = """
import asyncio, os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiscc.providers.external_ide import verify_external_start_in_session
from aiscc.providers.authority import ExecutionReferenceAuthority
from aiscc.persistence.repository import verify_historical_transition_provenance
from aiscc.workflow.models import GuardId
async def main():
    engine = create_async_engine(os.environ['AISCC_TEST_DATABASE_URL'])
    try:
        async with async_sessionmaker(engine)() as session, session.begin():
            verified = await verify_external_start_in_session(session, os.environ['START_ID'])
            source = await verify_historical_transition_provenance(
                session, os.environ['START_REQUEST'])
            assert ExecutionReferenceAuthority().verify(
                verified.common_ref, source.request, GuardId.G_EXECUTION_STARTED)
        print('NEW_PROCESS_START_AUTHORITY_PASS')
    finally:
        await engine.dispose()
asyncio.run(main())
"""
            result = await asyncio.to_thread(
                subprocess.run,
                [str(Path(".venv/Scripts/python.exe").resolve()), "-B", "-c", code],
                env=os.environ
                | {
                    "AISCC_TEST_DATABASE_URL": database_url,
                    "START_ID": START_PREFIX + f["permit"].value["permit_id"],
                    "START_REQUEST": f["start"].transition_request_id,
                },
                capture_output=True,
                timeout=30,
            )
            assert result.returncode == 0, result.stderr.decode().replace(
                database_url, "<ISOLATED_DB>"
            )
            assert result.stdout.strip() == b"NEW_PROCESS_START_AUTHORITY_PASS"
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize("bad", ["run", "version", "ready_source", "receipt"])
def test_permit_issue_requires_exact_durable_ready_and_task(database_url, tmp_path, bad):
    async def scenario():
        f = await fixture(database_url, tmp_path)
        try:
            args = dict(
                receipt=f["receipt"],
                work_run_id=f["args"]["work_run_id"],
                state_version=1,
                ready_transition_id=f["args"]["transition_request_id"],
                inner_task_bytes=TASK,
                ttl=timedelta(minutes=10),
            )
            if bad == "run":
                args["work_run_id"] = "missing-run"
            if bad == "version":
                args["state_version"] = 2
            if bad == "ready_source":
                args["ready_transition_id"] = "missing-ready"
            if bad == "receipt":
                args["receipt"] = replace(
                    f["receipt"],
                    body=TaskContractBodyV1(plain(f["body"].value) | dict(task_id="wrong-task")),
                )
            with pytest.raises((ValueError, HistoricalTransitionProvenanceError)):
                async with f["sessions"]() as session, session.begin():
                    await f["start_writer"].issue(session, **args)
            assert await count_starts(f) == 0
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())
