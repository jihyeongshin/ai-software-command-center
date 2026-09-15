from __future__ import annotations

import asyncio
from dataclasses import replace
from datetime import timedelta
from hashlib import sha256
from uuid import uuid4

import pytest
from sqlalchemy import select, text

from aiscc.contracts.workflow import WorkflowState
from aiscc.persistence import PostgresExecutionRepository
from aiscc.persistence.models import ExternalIdeExecutionSubmissionRow
from aiscc.providers.authority import ExecutionReferenceAuthority
from aiscc.providers.external_ide import (
    ExternalIdeExecutionRepository,
    LocalGitObserver,
    _bind_external_ide_writer,
)
from aiscc.self_dogfood import build_ready_request, materialize_task_spec
from aiscc.task_authority.authority import _bind_repository_once
from aiscc.task_authority.contracts import TaskContractBodyV1, plain
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository
from aiscc.workflow.matrix import TRANSITION_MATRIX
from aiscc.workflow.models import DecisionOutcome, GuardId
from tests.integration.self_dogfood.test_task_ready_entry import composition, enter, issue
from tests.integration.task_authority.test_task_contract_durability import (
    contract_fixture,
)
from tests.integration.task_authority.test_task_contract_durability import (
    database_url as database_url,
)
from tests.unit.providers.test_external_ide_execution_ingress import GIT, NOW, git_fixture


async def fixture(database_url, tmp_path):
    base = git_fixture(tmp_path)
    f = await contract_fixture(database_url, tmp_path)
    # A fresh trusted fixture composition binds the genuine temporary repository commit.
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
    ready = build_ready_request(
        spec,
        work_run_id=args["work_run_id"],
        transition_request_id="start-" + uuid4().hex,
        requester_id="fixture-system",
        created_at=NOW,
    )
    start = replace(
        ready,
        observed_state=WorkflowState.READY,
        observed_state_version=1,
        target_state=WorkflowState.RUNNING,
    )
    execution = PostgresExecutionRepository(f["sessions"])
    attempt = "provider-fixture-" + uuid4().hex
    await execution.create_attempt(
        attempt_id=attempt,
        work_run_id=args["work_run_id"],
        profile_id="fake-openai-responses-v1",
        profile_version="1",
        registry_id="aiscc-p1-5-tools",
        registry_version="1",
    )
    _, actual = await execution.load_authority(
        work_run_id=args["work_run_id"], execution_attempt_id=attempt
    )
    refs = ExecutionReferenceAuthority()
    start_ref = refs.register_start(actual)
    system = args["system_authority"]
    facts = [
        system.issue(
            guard_id=g,
            satisfied=True,
            reason="LEGITIMATE_EXISTING_START_FIXTURE",
            authority_ref="fixture:" + g.value,
            request=start,
        )
        for g in TRANSITION_MATRIX[(WorkflowState.READY, WorkflowState.RUNNING)]
        if g is not GuardId.G_EXECUTION_STARTED
    ]
    facts.append(
        system.issue_from_execution_ref(
            guard_id=GuardId.G_EXECUTION_STARTED,
            execution_ref=start_ref,
            verifier=refs,
            request=start,
        )
    )
    assert (
        await args["transition_repository"].decide(start, tuple(facts))
    ).outcome is DecisionOutcome.ADMITTED
    await execution.transition_attempt(attempt, "EXECUTION_STARTED")
    repo = ExternalIdeExecutionRepository(
        f["sessions"], f["repo"], LocalGitObserver(GIT, clock=lambda: NOW), clock=lambda: NOW
    )
    writer = _bind_external_ide_writer(repo)
    expected = {"src/file.txt": sha256(b"after\n").hexdigest()}
    async with f["sessions"]() as session, session.begin():
        lease, token = await writer.issue(
            session,
            receipt=receipt,
            work_run_id=args["work_run_id"],
            state_version=2,
            start_transition_id=start.transition_request_id,
            inner_task_bytes=b"bounded fixture instruction",
            expected_hashes=expected,
            ttl=timedelta(minutes=10),
        )
    f.update(
        external=repo,
        lease=lease,
        token=token,
        args=args,
        start=start,
        receipt=receipt,
        root=tmp_path,
        external_writer=writer,
    )
    return f


async def complete(f, token=None):
    async with f["sessions"]() as session, session.begin():
        return await f["external"].complete(
            session,
            lease_id=f["lease"].value["lease_id"],
            capability=token if token is not None else f["token"],
        )


@pytest.mark.postgres
def test_actual_ingress_restart_common_guard_single_use_no_provider_output(database_url, tmp_path):
    async def scenario():
        f = await fixture(database_url, tmp_path)
        try:
            (tmp_path / "src/file.txt").write_bytes(b"after\n")
            result = await complete(f)
            assert result == await complete(f)
            refs = ExecutionReferenceAuthority()
            with pytest.raises(ValueError):
                refs.register_submission(result.common_ref)
            restarted = ExternalIdeExecutionRepository(
                f["sessions"], f["repo"], LocalGitObserver(GIT)
            )
            verified = await restarted.resolve(result.submission_id)
            ref = refs.resolve_external_submission(verified)
            request = replace(
                f["start"],
                transition_request_id="admission-" + uuid4().hex,
                observed_state=WorkflowState.RUNNING,
                observed_state_version=2,
                target_state=WorkflowState.ADMISSION_PENDING,
            )
            fact = f["args"]["system_authority"].issue_from_execution_ref(
                guard_id=GuardId.G_EXECUTOR_SUBMISSION,
                execution_ref=ref,
                verifier=refs,
                request=request,
            )
            assert fact.satisfied
            with pytest.raises(ValueError):
                refs.resolve_external_submission(
                    replace(
                        verified,
                        submission=replace(
                            result, completed_at=(NOW + timedelta(seconds=1)).isoformat()
                        ),
                    )
                )
            async with f["sessions"]() as session:
                assert (
                    len(
                        tuple(
                            await session.scalars(
                                select(ExternalIdeExecutionSubmissionRow).where(
                                    ExternalIdeExecutionSubmissionRow.lease_id
                                    == f["lease"].value["lease_id"]
                                )
                            )
                        )
                    )
                    == 1
                )
                for table in (
                    "execution_output_refs",
                    "evidence_candidates",
                    "judgments",
                    "human_results",
                ):
                    # Producer IDs are disjoint from provider attempt IDs; no fabricated rows.
                    if table == "execution_output_refs":
                        assert (
                            await session.scalar(
                                text(
                                    "SELECT count(*) FROM execution_output_refs "
                                    "WHERE output_ref_id=:id"
                                ),
                                {"id": ref.submission_id},
                            )
                            == 0
                        )
            assert f["token"].encode() not in f["lease"].canonical_body
            (tmp_path / "src/file.txt").write_bytes(b"changed retry\n")
            with pytest.raises(ValueError):
                await complete(f)
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize(
    "bad", ["token", "hash", "scope", "base", "expired", "revoked", "state", "wrong-run", "race"]
)
def test_failed_completion_is_atomic(database_url, tmp_path, bad):
    async def scenario():
        f = await fixture(database_url, tmp_path)
        try:
            (tmp_path / "src/file.txt").write_bytes(b"after\n")
            if bad == "hash":
                (tmp_path / "src/file.txt").write_bytes(b"wrong\n")
            if bad == "scope":
                (tmp_path / "outside.txt").write_bytes(b"outside\n")
            if bad == "base":
                from tests.unit.providers.test_external_ide_execution_ingress import git

                git(tmp_path, "add", "src/file.txt")
                git(tmp_path, "commit", "-qm", "unexpected")
            if bad == "expired":
                f["external"]._clock = lambda: NOW + timedelta(hours=1)
            if bad == "revoked":
                await f["writer"].revoke_task_contract(
                    project_id=f["project_id"],
                    contract_id=f["body"].value["contract_id"],
                    expected_version=1,
                    expected_body_sha256=f["body"].body_sha256,
                    effective_at=NOW,
                )
            if bad in ("state", "wrong-run"):
                # Legitimate currentness loss is exercised through an existing owner transition.
                request = replace(f["start"], transition_request_id="repeat-" + uuid4().hex)
                assert (
                    await f["args"]["transition_repository"].decide(request, ())
                ).outcome is DecisionOutcome.DENIED
                # A wrong lease/run binding is rejected by the owner before issuing a second lease.
                async with f["sessions"]() as session, session.begin():
                    with pytest.raises(ValueError):
                        await f["external_writer"].issue(
                            session,
                            receipt=f["receipt"],
                            work_run_id=f["args"]["work_run_id"]
                            + ("-wrong" if bad == "wrong-run" else ""),
                            state_version=3 if bad == "state" else 2,
                            start_transition_id=f["start"].transition_request_id,
                            inner_task_bytes=b"fixture",
                            expected_hashes={},
                            ttl=timedelta(minutes=1),
                        )
                return
            if bad == "race":

                class ChangingObserver(LocalGitObserver):
                    def observe(self, lease):
                        observed = super().observe(lease)
                        (tmp_path / "src/file.txt").write_bytes(b"raced\n")
                        return observed

                f["external"]._observer = ChangingObserver(GIT, clock=lambda: NOW)
            with pytest.raises(ValueError):
                await complete(f, "incorrect" if bad == "token" else None)
            async with f["sessions"]() as session:
                assert (
                    await session.scalar(
                        select(ExternalIdeExecutionSubmissionRow).where(
                            ExternalIdeExecutionSubmissionRow.lease_id
                            == f["lease"].value["lease_id"]
                        )
                    )
                    is None
                )
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
def test_concurrent_completion_rollback_immutability_and_tamper(database_url, tmp_path):
    async def scenario():
        f = await fixture(database_url, tmp_path)
        try:
            (tmp_path / "src/file.txt").write_bytes(b"after\n")
            async with f["sessions"]() as session:
                await session.begin()
                uncommitted = await f["external"].complete(
                    session, lease_id=f["lease"].value["lease_id"], capability=f["token"]
                )
                await session.rollback()
            with pytest.raises(ValueError):
                await f["external"].resolve(uncommitted.submission_id)
            a, b = await asyncio.gather(complete(f), complete(f))
            assert a == b
            for table, column, identity in [
                ("external_ide_execution_leases", "lease_id", f["lease"].value["lease_id"]),
                ("external_ide_execution_submissions", "submission_id", a.submission_id),
            ]:
                for command in [
                    f"UPDATE {table} SET body_sha256=body_sha256 WHERE {column}=:i",
                    f"DELETE FROM {table} WHERE {column}=:i",
                    f"TRUNCATE {table} CASCADE",
                ]:
                    async with f["sessions"]() as session:
                        with pytest.raises(Exception, match="append-only"):
                            await session.execute(text(command), {"i": identity})
                        await session.rollback()
                assert (await f["external"].resolve(a.submission_id)).submission == a
            # Deliberate corruption in a rollback-only isolated test transaction; no real runtime.
            from aiscc.providers.external_ide import verify_external_submission_in_session

            async with f["sessions"]() as session:
                await session.begin()
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                await session.execute(
                    text(
                        "UPDATE external_ide_execution_submissions "
                        "SET body_sha256=:h WHERE submission_id=:i"
                    ),
                    {"h": "0" * 64, "i": a.submission_id},
                )
                with pytest.raises(ValueError):
                    await verify_external_submission_in_session(session, a.submission_id)
                await session.rollback()
            assert (await f["external"].resolve(a.submission_id)).submission == a
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
def test_additive_migration_empty_and_nonempty_downgrade(database_url, tmp_path):
    import os
    import subprocess
    from pathlib import Path

    from sqlalchemy.engine import make_url
    from sqlalchemy.ext.asyncio import create_async_engine

    database = "external_ide_migration_" + uuid4().hex
    isolated = make_url(database_url).set(database=database).render_as_string(hide_password=False)

    async def admin(sql):
        engine = create_async_engine(database_url, isolation_level="AUTOCOMMIT")
        try:
            async with engine.connect() as conn:
                await conn.execute(text(sql))
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
                return (
                    await conn.scalar(text("SELECT version_num FROM alembic_version")),
                    tuple(
                        (
                            await conn.execute(
                                text(
                                    "SELECT lease_id,body_sha256,canonical_body "
                                    "FROM external_ide_execution_leases ORDER BY lease_id"
                                )
                            )
                        ).all()
                    ),
                    tuple(
                        (
                            await conn.execute(
                                text(
                                    "SELECT submission_id,body_sha256,canonical_body "
                                    "FROM external_ide_execution_submissions ORDER BY submission_id"
                                )
                            )
                        ).all()
                    ),
                    tuple(
                        (
                            await conn.execute(
                                text(
                                    "SELECT tablename FROM pg_tables "
                                    "WHERE schemaname='public' ORDER BY tablename"
                                )
                            )
                        ).all()
                    ),
                )
        finally:
            await engine.dispose()

    asyncio.run(admin(f'CREATE DATABASE "{database}"'))
    try:
        assert migration("upgrade", "head")[0] == 0
        assert asyncio.run(snapshot())[:3] == ("20260915_0013", (), ())
        assert migration("downgrade", "20260914_0009")[0] == 0
        assert migration("upgrade", "head")[0] == 0

        async def populate():
            f = await fixture(isolated, tmp_path)
            try:
                (tmp_path / "src/file.txt").write_bytes(b"after\n")
                await complete(f)
            finally:
                await f["engine"].dispose()

        asyncio.run(populate())
        before = asyncio.run(snapshot())
        code, output = migration("downgrade", "20260914_0009")
        assert code != 0 and "EXTERNAL_IDE_NONEMPTY_DOWNGRADE_FORBIDDEN" in output
        assert asyncio.run(snapshot()) == before
    finally:
        asyncio.run(admin(f'DROP DATABASE "{database}" WITH (FORCE)'))
