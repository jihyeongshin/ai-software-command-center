from __future__ import annotations

import asyncio
from dataclasses import replace
from datetime import timedelta
from uuid import uuid4

import pytest
from sqlalchemy import event, text

from aiscc.contracts.workflow import WorkflowState
from aiscc.evidence.models import EvidenceAuthorityConflictError
from aiscc.judgment.authority import JudgmentPolicyAuthority
from aiscc.next_action.models import NextActionError
from aiscc.persistence import PostgresTransitionRepository
from aiscc.self_dogfood import enter_ready, materialize_task_spec
from aiscc.task_authority.authority import _bind_repository_once
from aiscc.task_authority.contracts import TaskContractBodyV1, TaskContractError, plain
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository
from aiscc.workflow.evaluator import TransitionEvaluator
from aiscc.workflow.guards import P1_4GuardAuthority
from aiscc.workflow.models import DecisionOutcome, RequestIdentityConflictError
from tests.integration.task_authority.test_task_contract_durability import (
    NOW,
    contract_fixture,
    successor_body,
)
from tests.integration.task_authority.test_task_contract_durability import (
    database_url as database_url,
)
from tests.unit.self_dogfood.test_task_materializer import assert_exact_spec


def composition(f):
    system = P1_4GuardAuthority()
    return dict(
        transition_repository=PostgresTransitionRepository(
            f["sessions"], TransitionEvaluator(system)
        ),
        system_authority=system,
        judgment_policy_authority=JudgmentPolicyAuthority(f["sessions"]),
        work_run_id="self-dogfood-" + uuid4().hex,
        transition_request_id="ready-" + uuid4().hex,
        requester_id="test-system",
        created_at=NOW,
    )


async def issue(f):
    return await f["writer"].issue_task_contract(
        body=f["body"], expected_current_body_sha256=None, issued_at=NOW
    )


async def enter(f, receipt, args, expected=None, action=None):
    return await enter_ready(
        f["repo"],
        receipt,
        expected or f["repository_binding"],
        action or f["body"].value["source_next_action"]["action_ref"],
        **args,
    )


@pytest.mark.postgres
@pytest.mark.parametrize("required", [False, True])
def test_current_immutable_spec_ready_history_retry_and_restart(database_url, tmp_path, required):
    async def scenario():
        f = await contract_fixture(database_url, tmp_path, required)
        try:
            receipt = await issue(f)
            action = f["body"].value["source_next_action"]["action_ref"]
            spec = await materialize_task_spec(f["repo"], receipt, f["repository_binding"], action)
            assert_exact_spec(spec, receipt.body)
            assert spec == await materialize_task_spec(
                f["repo"], receipt, f["repository_binding"], action
            )
            args = composition(f)
            decision = await enter(f, receipt, args)
            assert decision.outcome is DecisionOutcome.ADMITTED
            assert decision.resulting_state is WorkflowState.READY
            assert decision.resulting_state_version == 1
            assert await enter(f, receipt, args) == decision
            run = await args["transition_repository"].get_work_run(args["work_run_id"])
            assert run.state is WorkflowState.READY and run.state_version == 1
            assert run.task_contract_id == spec.task_contract_id
            async with f["sessions"]() as session:
                assert await session.scalar(text("SELECT version_num FROM alembic_version")) == (
                    "20260916_0015"
                )
                for table in (
                    "transition_requests",
                    "transition_evaluations",
                    "transition_decisions",
                ):
                    assert (
                        await session.scalar(
                            text(
                                "SELECT count(*) FROM " + table + " WHERE transition_request_id=:r"
                            ),
                            {"r": args["transition_request_id"]},
                        )
                        == 1
                    )
                for table in (
                    "human_gates",
                    "human_results",
                    "judgments",
                    "human_guard_attestations",
                    "judgment_guard_attestations",
                    "evidence_set_attestations",
                    "evidence_set_evaluations",
                ):
                    assert (
                        await session.scalar(
                            text("SELECT count(*) FROM " + table + " WHERE work_run_id=:r"),
                            {"r": args["work_run_id"]},
                        )
                        == 0
                    )
            # A new owner repository configured through fixture-only private composition.
            restarted = PostgresExternalTaskAuthorityRepository(f["sessions"])
            writer = _bind_repository_once(restarted)
            writer.configure_task_contracts(
                project_id=f["project_id"],
                repository_binding=f["repository_binding"],
                next_action_repository=f["actions"],
                evidence_repository=f["evidence"],
            )
            loaded = await restarted.get_task_contract(f["project_id"], spec.task_contract_id, 1)
            assert loaded == receipt
            assert (
                await materialize_task_spec(restarted, loaded, f["repository_binding"], action)
                == spec
            )
            # Same run with a fresh identity is not another READY; transaction rolls back.
            with pytest.raises(TaskContractError):
                await enter(f, receipt, args | {"transition_request_id": "conflict-" + uuid4().hex})
            with pytest.raises(RequestIdentityConflictError):
                await enter(f, receipt, args | {"created_at": NOW + timedelta(seconds=1)})
            assert await args["transition_repository"].get_work_run(args["work_run_id"]) == run
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize(
    "bad",
    [
        "repository_id",
        "repository_root",
        "base_commit",
        "action",
        "revoked",
        "superseded",
        "p1-8-context",
        "p1-8-descriptor",
        "p1-6",
    ],
)
def test_actual_owner_denial_prevents_spec_and_ready(database_url, tmp_path, bad):
    async def scenario():
        f = await contract_fixture(database_url, tmp_path)
        try:
            receipt = await issue(f)
            expected = dict(f["repository_binding"])
            action = f["body"].value["source_next_action"]["action_ref"]
            if bad in expected:
                expected[bad] = "0" * 40 if bad == "base_commit" else "wrong"
            elif bad == "action":
                action = action.replace("open-cycle-derived", "open-operational-recovery")
            elif bad == "revoked":
                await f["writer"].revoke_task_contract(
                    project_id=f["project_id"],
                    contract_id=f["body"].value["contract_id"],
                    expected_version=1,
                    expected_body_sha256=f["body"].body_sha256,
                    effective_at=NOW,
                )
            elif bad == "superseded":
                await f["writer"].issue_task_contract(
                    body=await successor_body(f, f["body"]),
                    expected_current_body_sha256=f["body"].body_sha256,
                    issued_at=NOW,
                )
            elif bad == "p1-8-context":
                await f["writer"].revoke_next_action_context(
                    current_context_ref=f["context"].context_ref,
                    event_id="revoke-" + uuid4().hex,
                    effective_at=NOW,
                )
                await f["writer"].certify_snapshot(snapshot_id="new-" + uuid4().hex, issued_at=NOW)
            elif bad == "p1-8-descriptor":
                invalidation = f["action_authority"].invalidate(
                    f["descriptor"],
                    event_kind="SUPERSEDED",
                    replacement_ref="owner-replacement",
                    now=NOW + timedelta(seconds=1),
                )
                await f["actions"].apply_owner_event(
                    invalidation, expected_project_revisions={f["project_id"]: 1}
                )
            elif bad == "p1-6":
                await f["evidence"].revoke(
                    subject_ref=f["body"].value["evidence_binding"]["requirement_set_ref"],
                    reason="fixture revocation",
                    owner_id="test-owner",
                    authority_version="v1",
                )
            args = composition(f)
            error = (
                NextActionError
                if bad.startswith("p1-8")
                else EvidenceAuthorityConflictError
                if bad == "p1-6"
                else TaskContractError
            )
            with pytest.raises(error):
                await materialize_task_spec(f["repo"], receipt, expected, action)
            with pytest.raises(error):
                await enter(f, receipt, args, expected, action)
            assert await args["transition_repository"].get_work_run(args["work_run_id"]) is None
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
def test_fabricated_recovery_receipt_cannot_bypass_existing_owner_verifier(database_url, tmp_path):
    # V1 cannot issue recovery receipts (also covered by unchanged owner regression).
    # Relabeling a genuine receipt must not produce a spec or any durable write.
    async def scenario():
        f = await contract_fixture(database_url, tmp_path)
        try:
            receipt = await issue(f)
            value = plain(receipt.body.value)
            value["source_next_action"]["action_ref"] = value["source_next_action"][
                "action_ref"
            ].replace("open-cycle-derived-task-issuance", "open-operational-recovery-task-issuance")
            forged = replace(receipt, body=TaskContractBodyV1(value))
            writes = []

            def capture(conn, cursor, statement, parameters, context, many):
                if statement.lstrip().upper().startswith(("INSERT", "UPDATE", "DELETE")):
                    writes.append(statement)

            event.listen(f["engine"].sync_engine, "before_cursor_execute", capture)
            args = composition(f)
            with pytest.raises(TaskContractError):
                await enter(f, forged, args, action=value["source_next_action"]["action_ref"])
            assert not writes
            assert await args["transition_repository"].get_work_run(args["work_run_id"]) is None
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())
