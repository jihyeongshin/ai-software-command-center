from __future__ import annotations

import asyncio
import os
from uuid import uuid4

import pytest
from sqlalchemy import event, text

from aiscc.contracts.workflow import WorkflowState
from aiscc.evidence.models import EvidenceAuthorityConflictError, EvidenceRequirementProfile
from aiscc.evidence.repository import PostgresEvidenceRepository
from aiscc.persistence import create_engine, create_session_factory
from tests.integration.evidence.test_postgres_evidence_admission import (
    checkpoint,
    requirement,
    seal_snapshot,
)


def graph():
    task = "definition-" + uuid4().hex
    sid = task + "-set"
    cp = checkpoint(
        task_id=task, set_id=sid, checkpoint_id="completion", source=WorkflowState.ADMISSION_PENDING
    )
    req = requirement(
        task_id=task,
        set_id=sid,
        requirement_id="proof",
        profile=EvidenceRequirementProfile.NOT_REQUIRED,
        checkpoints=(cp.ref.serialized(),),
        issuer_types=frozenset(),
        issuer_ids=frozenset(),
        content_kinds=frozenset(),
    )
    return seal_snapshot(task_id=task, set_id=sid, requirements=(req,), checkpoints=(cp,))


def claims(values):
    _, rs, _, cps = values
    return dict(
        task_contract_id=rs.task_contract_id,
        task_contract_version="v1",
        requirement_set_ref=f"{rs.requirement_set_id}@v1",
        expected_requirement_set_fingerprint=rs.fingerprint,
        expected_checkpoints=tuple((cp.ref, cp.fingerprint) for cp in cps),
    )


@pytest.fixture
def database_url():
    value = os.environ.get("AISCC_TEST_DATABASE_URL")
    if not value:
        pytest.skip("isolated PostgreSQL required")
    return value


async def setup(database_url, values=None):
    engine = create_engine(database_url)
    sessions = create_session_factory(engine)
    repo = PostgresEvidenceRepository(sessions)
    values = values or graph()
    owner, rs, reqs, cps = values
    await repo.register_authority(
        requirement_set=rs, requirements=reqs, checkpoints=cps, authority=owner
    )
    return engine, sessions, repo, values


@pytest.mark.postgres
def test_current_restart_caller_identity_no_writes_and_claim_denials(database_url):
    async def scenario():
        engine, sessions, repo, values = await setup(database_url)
        try:
            before = await repo.counts()

            # A fresh owner instance has no in-memory sealing capability.
            def forbidden_factory():
                raise AssertionError("resolver opened its own session")

            reader = PostgresEvidenceRepository(forbidden_factory)
            sql = []

            def capture(conn, cursor, statement, parameters, context, many):
                sql.append(statement.strip().split()[0].upper())

            event.listen(engine.sync_engine, "before_cursor_execute", capture)
            async with sessions() as session:
                with pytest.raises(EvidenceAuthorityConflictError, match="caller transaction"):
                    await reader.verify_requirement_definition_graph(session, **claims(values))
                async with session.begin():
                    transaction = session.get_transaction()
                    result = await reader.verify_requirement_definition_graph(
                        session, **claims(values)
                    )
                    assert result[0].fingerprint == values[1].fingerprint
                    assert result[1][0].fingerprint == values[2][0].fingerprint
                    assert result[2][0].fingerprint == values[3][0].fingerprint
                    assert result[3] == 0
                    for change in [
                        dict(task_contract_id="wrong"),
                        dict(expected_requirement_set_fingerprint="0" * 64),
                        dict(expected_checkpoints=()),
                        dict(expected_checkpoints=((values[3][0].ref, "0" * 64),)),
                        dict(expected_checkpoints=claims(values)["expected_checkpoints"] * 2),
                    ]:
                        with pytest.raises(EvidenceAuthorityConflictError):
                            await reader.verify_requirement_definition_graph(
                                session, **(claims(values) | change)
                            )
                    assert session.get_transaction() is transaction
                    assert not session.new and not session.dirty and not session.deleted
            event.remove(engine.sync_engine, "before_cursor_execute", capture)
            assert not set(sql) & {"INSERT", "UPDATE", "DELETE", "COMMIT", "ROLLBACK"}
            assert await repo.counts() == before
            async with sessions() as session:
                assert (
                    await session.scalar(
                        text("SELECT count(*) FROM work_runs WHERE task_contract_id=:t"),
                        {"t": values[1].task_contract_id},
                    )
                    == 0
                )
        finally:
            await engine.dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize("subject", ["set", "requirement", "checkpoint"])
def test_revocation_after_verifier_wait_cannot_pass_stale_graph(database_url, subject):
    async def scenario():
        engine, sessions, repo, values = await setup(database_url)
        try:
            ref = {
                "set": claims(values)["requirement_set_ref"],
                "requirement": values[2][0].ref.serialized(),
                "checkpoint": values[3][0].ref.serialized(),
            }[subject]
            async with sessions() as holding, holding.begin():
                await holding.execute(
                    text("SELECT pg_advisory_xact_lock(hashtextextended(:k,0))"),
                    {"k": f"evidence-task:{values[1].task_contract_id}:v1"},
                )
                revoke = asyncio.create_task(
                    repo.revoke(
                        subject_ref=ref,
                        reason="test",
                        owner_id="definition-test",
                        authority_version="v1",
                    )
                )
                await asyncio.sleep(0.05)
                assert not revoke.done()
            await asyncio.wait_for(revoke, 5)
            async with sessions() as session, session.begin():
                with pytest.raises(EvidenceAuthorityConflictError):
                    await repo.verify_requirement_definition_graph(session, **claims(values))
        finally:
            await engine.dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize(
    "change",
    [
        "requirement_missing",
        "requirement_extra",
        "requirement_hash",
        "requirement_profile",
        "requirement_requiredness",
        "requirement_reuse",
        "checkpoint_hash",
        "checkpoint_source",
        "checkpoint_target",
        "checkpoint_purpose",
        "set_membership",
        "set_hash",
    ],
)
def test_corrupt_durable_graph_denied_without_resolver_mutation(database_url, change):
    async def scenario():
        from copy import deepcopy

        from aiscc.persistence.models import (
            EvidenceCheckpointRow,
            EvidenceRequirementRow,
            EvidenceRequirementSetRow,
        )

        engine, sessions, repo, values = await setup(database_url)
        try:
            async with sessions() as session:
                await session.begin()
                # Fault injection is transaction-local in the task-owned test DB.
                # Restore triggers before the resolver and roll back every injected byte.
                await session.execute(text("SET LOCAL session_replication_role = replica"))
                req = await session.get(EvidenceRequirementRow, values[2][0].ref.serialized())
                cp = await session.get(EvidenceCheckpointRow, values[3][0].ref.serialized())
                rs = await session.get(
                    EvidenceRequirementSetRow, claims(values)["requirement_set_ref"]
                )
                if change == "requirement_missing":
                    await session.delete(req)
                elif change == "requirement_extra":
                    data = {c.name: deepcopy(getattr(req, c.name)) for c in req.__table__.columns}
                    data["requirement_ref"] += "-unbound"
                    session.add(EvidenceRequirementRow(**data))
                elif change == "requirement_hash":
                    req.fingerprint = "0" * 64
                elif change == "requirement_profile":
                    req.profile = "FORBIDDEN"
                elif change == "requirement_requiredness":
                    req.obligation = "OPTIONAL"
                elif change == "requirement_reuse":
                    req.payload = req.payload | {"reuse_maximum": 27}
                elif change == "checkpoint_hash":
                    cp.fingerprint = "0" * 64
                elif change == "checkpoint_source":
                    cp.source_state = "REWORK_REQUIRED"
                elif change == "checkpoint_target":
                    cp.target_state = "REJECTED"
                elif change == "checkpoint_purpose":
                    cp.transition_purpose_id = "invented"
                elif change == "set_membership":
                    rs.payload = rs.payload | {"ordered_requirement_refs": []}
                elif change == "set_hash":
                    rs.fingerprint = "0" * 64
                await session.flush()
                await session.execute(text("SET LOCAL session_replication_role = origin"))
                sql = []

                def capture(conn, cursor, statement, parameters, context, many):
                    sql.append(statement.strip().split()[0].upper())

                event.listen(engine.sync_engine, "before_cursor_execute", capture)
                try:
                    with pytest.raises((EvidenceAuthorityConflictError, ValueError)):
                        await repo.verify_requirement_definition_graph(session, **claims(values))
                    assert not set(sql) & {"INSERT", "UPDATE", "DELETE", "COMMIT", "ROLLBACK"}
                finally:
                    event.remove(engine.sync_engine, "before_cursor_execute", capture)
                    await session.rollback()
        finally:
            await engine.dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize("kind", ["REVOKED", "SUPERSEDED", "CORRECTED"])
def test_current_reader_serializes_invalidation_and_restart_denies(database_url, kind):
    async def scenario():
        from dataclasses import replace

        from aiscc.evidence.models import EvidenceAuthorityEventKind, EvidenceRequirementRef

        owner, rs, reqs, cps = graph()
        other = replace(
            reqs[0], ref=EvidenceRequirementRef(rs.task_contract_id + ":replacement", "v1")
        )
        values = seal_snapshot(
            task_id=rs.task_contract_id,
            set_id=rs.requirement_set_id,
            requirements=(reqs[0], other),
            checkpoints=cps,
        )
        engine, sessions, repo, values = await setup(database_url, values)
        try:
            async with sessions() as session, session.begin():
                await repo.verify_requirement_definition_graph(session, **claims(values))
                invalidation = asyncio.create_task(
                    repo.revoke(
                        subject_ref=values[2][0].ref.serialized(),
                        reason="currentness-race",
                        owner_id="definition-test",
                        authority_version="v1",
                        kind=EvidenceAuthorityEventKind(kind),
                        replacement_ref=values[2][1].ref.serialized()
                        if kind != "REVOKED"
                        else None,
                    )
                )
                await asyncio.sleep(0.05)
                assert not invalidation.done(), "writer crossed held owner task lock"
                await repo.verify_requirement_definition_graph(session, **claims(values))
            await asyncio.wait_for(invalidation, 5)
            restarted = PostgresEvidenceRepository(sessions)
            async with sessions() as session, session.begin():
                with pytest.raises(EvidenceAuthorityConflictError):
                    await restarted.verify_requirement_definition_graph(session, **claims(values))
        finally:
            await engine.dispose()

    asyncio.run(scenario())
