from __future__ import annotations

import asyncio
import os
from dataclasses import replace
from uuid import uuid4

import pytest
from sqlalchemy import event, text

from aiscc.contracts.workflow import WorkflowState
from aiscc.evidence.models import EvidenceRequirementProfile
from aiscc.evidence.repository import PostgresEvidenceRepository
from aiscc.task_authority.authority import _bind_repository_once
from aiscc.task_authority.contracts import (
    TaskContractBodyV1,
    TaskContractError,
    candidate_fingerprint,
    plain,
)
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository
from tests.integration.evidence.test_postgres_evidence_admission import (
    checkpoint,
    requirement,
    seal_snapshot,
)
from tests.integration.memory.test_postgres_project_memory_next_action import (
    NOW,
    cycle_selection_fixture,
)


@pytest.fixture
def database_url():
    value = os.environ.get("AISCC_TEST_DATABASE_URL")
    if not value:
        pytest.skip("isolated PostgreSQL required")
    return value


async def contract_fixture(database_url, tmp_path, required=False, maximum_ids=False):
    f = await cycle_selection_fixture(
        database_url, ("p" * 64 + uuid4().hex) if maximum_ids else None
    )
    repo = f["external_repository"]
    writer = f["external_writer"]
    evidence = PostgresEvidenceRepository(f["sessions"])
    cid = ("c" * 64 if maximum_ids else "contract-") + uuid4().hex
    cp = checkpoint(
        task_id=cid,
        set_id=cid + "-set",
        checkpoint_id="completion",
        source=WorkflowState.HUMAN_REQUIRED if required else WorkflowState.ADMISSION_PENDING,
    )
    req = requirement(
        task_id=cid,
        set_id=cid + "-set",
        requirement_id="proof",
        profile=EvidenceRequirementProfile.NOT_REQUIRED,
        checkpoints=(cp.ref.serialized(),),
        issuer_types=frozenset(),
        issuer_ids=frozenset(),
        content_kinds=frozenset(),
    )
    owner, rs, reqs, cps = seal_snapshot(
        task_id=cid, set_id=cid + "-set", requirements=(req,), checkpoints=(cp,)
    )
    await evidence.register_authority(
        requirement_set=rs, requirements=reqs, checkpoints=cps, authority=owner
    )
    repository_binding = dict(
        repository_id="fixture-repository",
        repository_root=str(tmp_path.resolve()),
        base_commit="1" * 40,
    )
    writer.configure_task_contracts(
        project_id=f["project_id"],
        repository_binding=repository_binding,
        next_action_repository=f["actions"],
        evidence_repository=evidence,
    )
    selected = f["selected"]
    intro = f["context_introduction"]
    uses = []
    if required:
        uses = [
            dict(source_state=a, target_state=b)
            for a, b in sorted(
                [
                    ("RUNNING", "REWORK_REQUIRED"),
                    ("ADMISSION_PENDING", "REWORK_REQUIRED"),
                    ("ADMISSION_PENDING", "ACCEPTED"),
                    ("ADMISSION_PENDING", "REJECTED"),
                    ("BLOCKED", "REWORK_REQUIRED"),
                    ("REWORK_REQUIRED", "REJECTED"),
                    ("ADMISSION_PENDING", "HUMAN_REQUIRED"),
                ]
            )
        ]
    body = TaskContractBodyV1(
        dict(
            schema_id="AISCC-TASKCONTRACT-BODY-V1",
            owner="EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY",
            project_id=f["project_id"],
            contract_id=cid,
            task_id=cid,
            contract_version=1,
            goal="Implement bounded local change",
            non_goals=["No network"],
            allowed_paths=["src/**"],
            forbidden_paths=["secrets/**"],
            authority_refs=[],
            evidence_binding=dict(
                requirement_set_ref=rs.requirement_set_id + "@v1",
                requirement_set_fingerprint=rs.fingerprint,
                checkpoints=[dict(ref=x.ref.serialized(), fingerprint=x.fingerprint) for x in cps],
            ),
            human_binding=dict(
                kind="REQUIRED" if required else "NOT_REQUIRED",
                authority_policy_ref="body-human-policy",
                authority_policy_version="v1",
                required_uses=uses,
                purpose_id="P1_7_WORK_RESULT_REVIEW" if required else None,
                purpose_version="v1" if required else None,
                owner_selector_fingerprint="reviewers-v1" if required else None,
            ),
            judgment_binding=dict(
                owner_policy="HUMAN" if required else "SYSTEM_DETERMINISTIC",
                policies=[
                    dict(
                        policy_id="policy-" + cid[-32:] + "-accepted",
                        policy_version="v1",
                        source_state=cp.source_state.value,
                        target_state="ACCEPTED",
                        requires_human_result=required,
                        requires_post_human_evidence=True,
                        deterministic_kind=None if required else "ACCEPTED",
                        evidence_basis_kind="SATISFIED_ATTESTATION",
                        evidence_checkpoint_ref=cp.ref.serialized(),
                        evidence_requirement_set_ref=rs.requirement_set_id + "@v1",
                    )
                ],
            ),
            source_next_action=dict(
                selection_id=selected.selection_id,
                selection_version=selected.selection_version,
                selection_fingerprint=selected.fingerprint,
                project_revision=selected.project_revision,
                action_ref=selected.action_ref.serialized,
                descriptor_fingerprint=selected.descriptor_fingerprint,
                issuance_candidate_id=f["candidate"].candidate_id,
                issuance_candidate_fingerprint=candidate_fingerprint(f["candidate"]),
                external_context=dict(
                    context_ref=selected.external_context_ref,
                    context_fingerprint=selected.external_context_fingerprint,
                    introduction_event_ref=intro.event_ref,
                    introduction_event_fingerprint=intro.event_fingerprint,
                    snapshot_ref=selected.external_context_snapshot_ref,
                    snapshot_fingerprint=selected.external_context_snapshot_fingerprint,
                    owner_event_high_watermark=selected.external_context_event_high_watermark,
                ),
            ),
            repository_binding=repository_binding,
            execution_provenance=dict(
                runtime_mode="OWNER_SELF_DOGFOOD",
                cycle_execution_mode="AISCC_SELF_DOGFOOD",
                orchestrator_version="v1",
                orchestrator_commit="1" * 40,
            ),
            predecessor=None,
        )
    )
    f.update(
        repo=repo,
        writer=writer,
        evidence=evidence,
        body=body,
        repository_binding=repository_binding,
        evidence_values=(owner, rs, reqs, cps),
    )
    return f


async def verify(f, receipt, repo=None, session=None, current=True):
    return await (repo or f["repo"]).verify_task_contract(
        receipt,
        require_current=current,
        expected_repository_binding=f["repository_binding"],
        expected_next_action_ref=f["body"].value["source_next_action"]["action_ref"],
        session=session,
    )


@pytest.mark.postgres
@pytest.mark.parametrize("maximum_ids", [False, True])
def test_body_issue_retry_restart_current_revoke_and_no_source_run_lock(
    database_url, tmp_path, maximum_ids
):
    async def scenario():
        f = await contract_fixture(database_url, tmp_path, maximum_ids=maximum_ids)
        try:
            if maximum_ids:
                assert len(f["project_id"]) == len(f["body"].value["contract_id"]) == 96
            locks = []

            def capture(conn, cursor, statement, parameters, context, many):
                if "pg_advisory" in statement:
                    locks.extend(str(x) for x in parameters)

            event.listen(f["engine"].sync_engine, "before_cursor_execute", capture)
            receipt = await f["writer"].issue_task_contract(
                body=f["body"], expected_current_body_sha256=None, issued_at=NOW
            )
            replay = await f["writer"].issue_task_contract(
                body=f["body"], expected_current_body_sha256=None, issued_at=NOW
            )
            assert receipt == replay and len(receipt.body.body_ref) == 93
            assert not any(x.startswith("run:") for x in locks)
            assert (await verify(f, receipt)).current
            restarted = PostgresExternalTaskAuthorityRepository(f["sessions"])
            restarted_writer = _bind_repository_once(restarted)
            restarted_writer.configure_task_contracts(
                project_id=f["project_id"],
                repository_binding=f["repository_binding"],
                next_action_repository=f["actions"],
                evidence_repository=f["evidence"],
            )
            loaded = await restarted.get_task_contract(
                f["project_id"], f["body"].value["contract_id"], 1
            )
            assert loaded == receipt and (await verify(f, loaded, restarted)).current
            changed = TaskContractBodyV1(plain(f["body"].value) | dict(goal="different"))
            with pytest.raises(TaskContractError):
                await f["writer"].issue_task_contract(
                    body=changed, expected_current_body_sha256=None, issued_at=NOW
                )
            revoked = await f["writer"].revoke_task_contract(
                project_id=f["project_id"],
                contract_id=f["body"].value["contract_id"],
                expected_version=1,
                expected_body_sha256=f["body"].body_sha256,
                effective_at=NOW,
            )
            assert revoked == await f["writer"].revoke_task_contract(
                project_id=f["project_id"],
                contract_id=f["body"].value["contract_id"],
                expected_version=1,
                expected_body_sha256=f["body"].body_sha256,
                effective_at=NOW,
            )
            with pytest.raises(TaskContractError):
                await verify(f, receipt)
            assert not (await verify(f, receipt, current=False)).current
            assert not any(x.startswith("run:") for x in locks)
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


async def successor_body(f, original):
    from aiscc.evidence.models import EvidenceCheckpointRef, EvidenceRequirementRef

    owner, rs, reqs, cps = f["evidence_values"]
    n = original.value["contract_version"] + 1
    version = "v" + str(n)
    cp = replace(
        cps[0],
        ref=EvidenceCheckpointRef(cps[0].ref.checkpoint_id, version),
        task_contract_version=version,
        requirement_set_version=version,
    )
    cp = owner.seal_checkpoint(cp)
    req = owner.seal_requirement(
        replace(
            reqs[0],
            ref=EvidenceRequirementRef(reqs[0].ref.requirement_id, version),
            task_contract_version=version,
            requirement_set_version=version,
            applicable_checkpoint_refs=(cp.ref.serialized(),),
        )
    )
    newset = owner.seal_set(
        replace(
            rs,
            requirement_set_version=version,
            task_contract_version=version,
            ordered_requirement_refs=(req.ref.serialized(),),
            ordered_checkpoint_refs=(cp.ref.serialized(),),
            requirement_root_hash="",
        ),
        (req,),
        (cp,),
    )
    await f["evidence"].register_authority(
        requirement_set=newset, requirements=(req,), checkpoints=(cp,), authority=owner
    )
    value = plain(original.value)
    value["contract_version"] = n
    value["predecessor"] = {"contract_version": n - 1, "body_sha256": original.body_sha256}
    value["evidence_binding"] = {
        "requirement_set_ref": rs.requirement_set_id + "@" + version,
        "requirement_set_fingerprint": newset.fingerprint,
        "checkpoints": [{"ref": cp.ref.serialized(), "fingerprint": cp.fingerprint}],
    }
    policy = value["judgment_binding"]["policies"][0]
    policy.update(
        policy_version=version,
        evidence_checkpoint_ref=cp.ref.serialized(),
        evidence_requirement_set_ref=rs.requirement_set_id + "@" + version,
    )
    return TaskContractBodyV1(value)


@pytest.mark.postgres
def test_exact_concurrent_issuance_version_lineage_and_revoked_family(database_url, tmp_path):
    async def scenario():
        f = await contract_fixture(database_url, tmp_path)
        try:

            async def issue(body, previous=None):
                return await f["writer"].issue_task_contract(
                    body=body, expected_current_body_sha256=previous, issued_at=NOW
                )

            first = await asyncio.gather(issue(f["body"]), issue(f["body"]))
            assert first[0] == first[1]
            body2 = await successor_body(f, f["body"])
            second = await asyncio.gather(
                issue(body2, f["body"].body_sha256), issue(body2, f["body"].body_sha256)
            )
            assert second[0] == second[1]
            assert await issue(f["body"]) == first[0]
            with pytest.raises(TaskContractError):
                await verify(f, first[0])
            assert (await verify(f, second[0])).current
            await f["writer"].revoke_task_contract(
                project_id=f["project_id"],
                contract_id=body2.value["contract_id"],
                expected_version=2,
                expected_body_sha256=body2.body_sha256,
                effective_at=NOW,
            )
            body3 = await successor_body(f, body2)
            with pytest.raises(TaskContractError):
                await issue(body3, body2.body_sha256)
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize(
    "boundary",
    [
        "task_constraint_refs",
        "task_constraint_authority_events",
        "task_contract_bodies",
        "task_constraint_owner_snapshots",
    ],
)
def test_issuance_failure_rolls_back_all_body_ref_event_writes(database_url, tmp_path, boundary):
    async def scenario():
        f = await contract_fixture(database_url, tmp_path)
        try:

            async def counts():
                async with f["sessions"]() as session:
                    return tuple(
                        [
                            await session.scalar(text("SELECT count(*) FROM " + table))
                            for table in (
                                "task_contract_bodies",
                                "task_constraint_refs",
                                "task_constraint_authority_events",
                                "external_task_authority_event_registry",
                                "task_constraint_owner_snapshots",
                            )
                        ]
                    )

            before = await counts()

            def fail(conn, cursor, statement, parameters, context, many):
                if statement.lower().startswith("insert into " + boundary + " "):
                    raise RuntimeError("injected boundary failure")

            event.listen(f["engine"].sync_engine, "before_cursor_execute", fail)
            try:
                with pytest.raises(RuntimeError, match="injected boundary"):
                    await f["writer"].issue_task_contract(
                        body=f["body"], expected_current_body_sha256=None, issued_at=NOW
                    )
            finally:
                event.remove(f["engine"].sync_engine, "before_cursor_execute", fail)
            assert await counts() == before
            receipt = await f["writer"].issue_task_contract(
                body=f["body"], expected_current_body_sha256=None, issued_at=NOW
            )
            assert (await verify(f, receipt)).current
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize(
    "statement",
    [
        "UPDATE task_contract_bodies SET task_id='tampered'",
        "DELETE FROM task_contract_bodies",
        "TRUNCATE task_contract_bodies",
    ],
)
def test_append_only_body_denies_update_delete_truncate(database_url, tmp_path, statement):
    from sqlalchemy.exc import DBAPIError

    async def scenario():
        f = await contract_fixture(database_url, tmp_path)
        try:
            receipt = await f["writer"].issue_task_contract(
                body=f["body"], expected_current_body_sha256=None, issued_at=NOW
            )
            async with f["sessions"]() as session:
                with pytest.raises(DBAPIError, match="append-only"):
                    await session.execute(text(statement))
                await session.rollback()
            assert (
                await f["repo"].get_task_contract(
                    f["project_id"], f["body"].value["contract_id"], 1
                )
                == receipt
            )
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
def test_operational_source_v1_denial_precedes_work_run_lock_and_writes(database_url, tmp_path):
    from aiscc.next_action.models import NextActionProposal, NextActionSelectionMode
    from tests.integration.memory.test_postgres_project_memory_next_action import (
        add_recovery_fact,
        operational_parameters,
    )

    async def scenario():
        f = await contract_fixture(database_url, tmp_path)
        try:
            label = uuid4().hex
            source_run = await add_recovery_fact(f["sessions"], f["project_id"], label)
            descriptor = f["action_authority"].issue_policy_catalog_v1(now=NOW)[2][0]
            selected, candidate = await f["actions"].select(
                selection_id="recovery-" + label,
                project_id=f["project_id"],
                expected_project_revision=1,
                mode=NextActionSelectionMode.OPERATIONAL_RECOVERY,
                proposals=(
                    NextActionProposal(
                        "proposal-" + label,
                        f["project_id"],
                        descriptor.action_ref,
                        await operational_parameters(f["sessions"], source_run),
                        "recovery proof",
                    ),
                ),
                operational_work_run_id=source_run,
                now=NOW,
            )
            value = plain(f["body"].value)
            value["source_next_action"].update(
                selection_id=selected.selection_id,
                selection_version=selected.selection_version,
                selection_fingerprint=selected.fingerprint,
                project_revision=selected.project_revision,
                action_ref=selected.action_ref.serialized,
                descriptor_fingerprint=descriptor.fingerprint,
                issuance_candidate_id=candidate.candidate_id,
                issuance_candidate_fingerprint=candidate_fingerprint(candidate),
                external_context=None,
            )
            body = TaskContractBodyV1(value)
            locks = []
            writes = []

            def capture(conn, cursor, statement, parameters, context, many):
                if "pg_advisory" in statement:
                    locks.extend(str(x) for x in parameters)
                if statement.lstrip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                    writes.append(statement)

            event.listen(f["engine"].sync_engine, "before_cursor_execute", capture)
            try:
                with pytest.raises(
                    TaskContractError, match="TASKCONTRACT_V1_UNSUPPORTED_NEXT_ACTION_SOURCE"
                ):
                    await f["writer"].issue_task_contract(
                        body=body, expected_current_body_sha256=None, issued_at=NOW
                    )
                assert not writes and not any(x.startswith("run:") for x in locks)
            finally:
                event.remove(f["engine"].sync_engine, "before_cursor_execute", capture)
            async with f["sessions"]() as session, session.begin():
                assert await f["actions"].verify_current_selection(
                    session,
                    selection_id=selected.selection_id,
                    expected_project_id=f["project_id"],
                    expected_project_revision=selected.project_revision,
                    expected_selection_fingerprint=selected.fingerprint,
                    expected_candidate=candidate,
                    expected_action_ref=descriptor.action_ref,
                    expected_descriptor_fingerprint=descriptor.fingerprint,
                )
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize("bad", ["hash", "bytes", "event", "reference", "snapshot", "predecessor"])
def test_tampered_durable_authority_denies_without_repair(database_url, tmp_path, bad):
    from aiscc.persistence.models import TaskConstraintOwnerSnapshotRow, TaskContractBodyRow

    async def scenario():
        f = await contract_fixture(database_url, tmp_path)
        try:
            receipt = await f["writer"].issue_task_contract(
                body=f["body"], expected_current_body_sha256=None, issued_at=NOW
            )
            async with f["sessions"]() as session:
                await session.begin()
                await session.execute(text("SET LOCAL session_replication_role=replica"))
                row = await session.get(TaskContractBodyRow, receipt.body.body_ref)
                if bad == "hash":
                    row.body_sha256 = "0" * 64
                if bad == "bytes":
                    row.canonical_body = b"{}"
                if bad == "event":
                    row.issuance_event_ref = "missing-event"
                if bad == "reference":
                    row.constraint_ref = "missing-ref"
                if bad == "predecessor":
                    row.task_id = "wrong-task"
                if bad == "snapshot":
                    snap = await session.get(TaskConstraintOwnerSnapshotRow, receipt.snapshot_ref)
                    snap.payload = snap.payload | {"snapshot_fingerprint": "0" * 64}
                await session.flush()
                await session.execute(text("SET LOCAL session_replication_role=origin"))
                with pytest.raises((TaskContractError, ValueError, RuntimeError)):
                    await verify(f, receipt, session=session)
                await session.rollback()
            assert (await verify(f, receipt)).current
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize("owner", ["P1_6", "P1_8"])
def test_invalidating_owner_waits_through_issuance_then_currentness_denies(
    database_url, tmp_path, owner
):
    async def scenario():
        f = await contract_fixture(database_url, tmp_path)
        writer_task = None
        try:
            # Interpose at the first body insert, after both public owner verifiers have locked.
            # The production owner invalidation starts concurrently and cannot commit first.
            started = asyncio.Event()

            def boundary(conn, cursor, statement, parameters, context, many):
                if statement.lower().startswith("insert into task_contract_bodies "):
                    started.set()

            event.listen(f["engine"].sync_engine, "before_cursor_execute", boundary)

            async def invalidate():
                await started.wait()
                if owner == "P1_6":
                    await f["evidence"].revoke(
                        subject_ref=f["body"].value["evidence_binding"]["requirement_set_ref"],
                        reason="concurrent",
                        owner_id="test-owner",
                        authority_version="v1",
                    )
                else:
                    await f["writer"].revoke_next_action_context(
                        current_context_ref=f["context"].context_ref,
                        event_id="source-revoke-" + uuid4().hex,
                        effective_at=NOW,
                    )
                    await f["writer"].certify_snapshot(
                        snapshot_id="source-after-" + uuid4().hex, issued_at=NOW
                    )

            writer_task = asyncio.create_task(invalidate())
            receipt = await f["writer"].issue_task_contract(
                body=f["body"], expected_current_body_sha256=None, issued_at=NOW
            )
            await asyncio.wait_for(writer_task, 5)
            with pytest.raises((TaskContractError, ValueError, RuntimeError)):
                await verify(f, receipt)
            assert (
                await f["repo"].get_task_contract(
                    f["project_id"], f["body"].value["contract_id"], 1
                )
                == receipt
            )
        finally:
            if writer_task is not None and not writer_task.done():
                writer_task.cancel()
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize("owner", ["P1_6", "P1_8"])
def test_owner_invalidation_committed_first_denies_issuance_without_partial_rows(
    database_url, tmp_path, owner
):
    async def scenario():
        f = await contract_fixture(database_url, tmp_path)
        try:
            if owner == "P1_6":
                await f["evidence"].revoke(
                    subject_ref=f["body"].value["evidence_binding"]["requirement_set_ref"],
                    reason="before issuance",
                    owner_id="test-owner",
                    authority_version="v1",
                )
            else:
                await f["writer"].revoke_next_action_context(
                    current_context_ref=f["context"].context_ref,
                    event_id="before-" + uuid4().hex,
                    effective_at=NOW,
                )
                await f["writer"].certify_snapshot(
                    snapshot_id="before-" + uuid4().hex, issued_at=NOW
                )
            writes = []

            def capture(conn, cursor, statement, parameters, context, many):
                if statement.lstrip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                    writes.append(statement)

            event.listen(f["engine"].sync_engine, "before_cursor_execute", capture)
            with pytest.raises((TaskContractError, ValueError, RuntimeError)):
                await f["writer"].issue_task_contract(
                    body=f["body"], expected_current_body_sha256=None, issued_at=NOW
                )
            assert not writes
            assert (
                await f["repo"].get_task_contract(
                    f["project_id"], f["body"].value["contract_id"], 1
                )
                is None
            )
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize(
    "bad",
    [
        "project",
        "repository",
        "base",
        "selection",
        "candidate",
        "descriptor",
        "context",
        "extra_authority",
    ],
)
def test_mismatched_authorization_claims_deny_before_body_writes(database_url, tmp_path, bad):
    async def scenario():
        f = await contract_fixture(database_url, tmp_path)
        try:
            value = plain(f["body"].value)
            if bad == "project":
                value["project_id"] = "wrong"
            elif bad == "repository":
                value["repository_binding"]["repository_id"] = "wrong"
            elif bad == "base":
                value["repository_binding"]["base_commit"] = "2" * 40
            elif bad == "selection":
                value["source_next_action"]["selection_id"] = "missing"
            elif bad == "candidate":
                value["source_next_action"]["issuance_candidate_fingerprint"] = "0" * 64
            elif bad == "descriptor":
                value["source_next_action"]["descriptor_fingerprint"] = "0" * 64
            elif bad == "context":
                value["source_next_action"]["external_context"]["context_fingerprint"] = "0" * 64
            else:
                value["authority_refs"] = [
                    {"ref": "task-constraint:v1:missing", "fingerprint": "0" * 64}
                ]
            with pytest.raises((TaskContractError, ValueError, RuntimeError)):
                await f["writer"].issue_task_contract(
                    body=TaskContractBodyV1(value), expected_current_body_sha256=None, issued_at=NOW
                )
            assert (
                await f["repo"].get_task_contract(
                    f["project_id"], f["body"].value["contract_id"], 1
                )
                is None
            )
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
def test_migration_empty_upgrade_downgrade_and_nonempty_preservation(database_url, tmp_path):
    import subprocess
    from pathlib import Path

    from sqlalchemy.engine import make_url
    from sqlalchemy.ext.asyncio import create_async_engine

    parsed = make_url(database_url)
    # Test-owned database in the supplied isolated PostgreSQL only. No discovery or external access.
    assert parsed.host in {"127.0.0.1", "localhost"}
    dbname = "aiscc_1302_migration_" + uuid4().hex
    isolated = parsed.set(database=dbname).render_as_string(hide_password=False)
    executable = Path.cwd() / ".venv" / "Scripts" / "python.exe"
    assert executable.is_file()

    async def admin(statement):
        engine = create_async_engine(database_url, isolation_level="AUTOCOMMIT")
        try:
            async with engine.connect() as connection:
                await connection.execute(text(statement))
        finally:
            await engine.dispose()

    def migration(*args):
        result = subprocess.run(
            [str(executable), "-B", "-m", "alembic", *args],
            env=os.environ | {"AISCC_DATABASE_URL": isolated},
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        output = (result.stdout + result.stderr).replace(isolated, "<TASK_DB_URL>")
        return result.returncode, output

    async def snapshot():
        engine = create_async_engine(isolated)
        try:
            async with engine.connect() as connection:
                return (
                    await connection.scalar(text("SELECT version_num FROM alembic_version")),
                    await connection.scalar(text("SELECT count(*) FROM task_contract_bodies")),
                    tuple(
                        (
                            await connection.execute(
                                text(
                                    "SELECT body_ref, body_sha256, canonical_body "
                                    "FROM task_contract_bodies ORDER BY body_ref"
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
                )
        finally:
            await engine.dispose()

    asyncio.run(admin(f'CREATE DATABASE "{dbname}"'))
    try:
        assert migration("upgrade", "head")[0] == 0
        assert asyncio.run(snapshot())[:2] == ("20260916_0016", 0)
        assert migration("downgrade", "20260901_0008")[0] == 0
        assert migration("upgrade", "head")[0] == 0

        async def issue():
            f = await contract_fixture(isolated, tmp_path)
            try:
                await f["writer"].issue_task_contract(
                    body=f["body"], expected_current_body_sha256=None, issued_at=NOW
                )
            finally:
                await f["engine"].dispose()

        asyncio.run(issue())
        before = asyncio.run(snapshot())
        code, output = migration("downgrade", "20260901_0008")
        assert code != 0 and "TASKCONTRACT_NONEMPTY_DOWNGRADE_FORBIDDEN" in output
        assert asyncio.run(snapshot()) == before
    finally:
        asyncio.run(admin(f'DROP DATABASE "{dbname}"'))
