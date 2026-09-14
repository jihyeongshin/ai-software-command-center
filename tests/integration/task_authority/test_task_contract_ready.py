from __future__ import annotations

import asyncio
from uuid import uuid4

import pytest
from sqlalchemy import event, text

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.judgment.authority import JudgmentPolicyAuthority
from aiscc.persistence import PostgresTransitionRepository
from aiscc.task_authority.contracts import TaskContractError
from aiscc.task_authority.ready import prepare_task_contract_ready
from aiscc.workflow.evaluator import TransitionEvaluator
from aiscc.workflow.guards import P1_4GuardAuthority
from aiscc.workflow.models import DecisionOutcome, RequesterType, TransitionRequest
from tests.integration.task_authority.test_task_contract_durability import (
    NOW,
    contract_fixture,
)
from tests.integration.task_authority.test_task_contract_durability import (
    database_url as database_url,
)


def request_for(f):
    return TransitionRequest(
        "ready-" + uuid4().hex,
        f["project_id"],
        f["body"].value["contract_id"],
        "v1",
        "run-" + uuid4().hex,
        None,
        0,
        WorkflowState.READY,
        "system",
        RequesterType.SYSTEM,
        RuntimeMode.OWNER_SELF_DOGFOOD,
        created_at=NOW,
    )


@pytest.mark.postgres
@pytest.mark.parametrize("required", [False, True])
def test_existing_p1_4_ready_and_p1_7_configuration_without_future_facts(
    database_url, tmp_path, required
):
    async def scenario():
        f = await contract_fixture(database_url, tmp_path, required)
        try:
            receipt = await f["writer"].issue_task_contract(
                body=f["body"], expected_current_body_sha256=None, issued_at=NOW
            )
            system = P1_4GuardAuthority()
            policies = JudgmentPolicyAuthority(f["sessions"])
            request = request_for(f)
            participant = await prepare_task_contract_ready(
                f["repo"],
                receipt,
                request,
                system_authority=system,
                judgment_policy_authority=policies,
            )
            reloaded = await prepare_task_contract_ready(
                f["repo"],
                receipt,
                request,
                system_authority=system,
                judgment_policy_authority=JudgmentPolicyAuthority(f["sessions"]),
            )
            assert participant.judgment_policies == reloaded.judgment_policies
            assert {x.guard_id.value for x in participant.facts(request)} == {
                "G_CONTRACT",
                "G_SCOPE",
                "G_RUNTIME_CONTEXT",
            }
            locks = []

            def capture(conn, cursor, statement, parameters, context, many):
                if "pg_advisory" in statement:
                    locks.extend(str(x) for x in parameters)

            event.listen(f["engine"].sync_engine, "before_cursor_execute", capture)
            workflow = PostgresTransitionRepository(f["sessions"], TransitionEvaluator(system))
            decision = await workflow.decide(request, (), transaction_participant=participant)
            assert decision.outcome is DecisionOutcome.ADMITTED
            assert (
                decision.resulting_state is WorkflowState.READY
                and decision.resulting_state_version == 1
            )
            assert locks[0] == "run:" + request.work_run_id
            assert [x for x in locks if x.startswith("run:")] == ["run:" + request.work_run_id]
            assert next(i for i, x in enumerate(locks) if x.startswith("task-contract-family:")) > 0
            async with f["sessions"]() as session:
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
                            {"r": request.work_run_id},
                        )
                        == 0
                    )
            assert (
                await workflow.decide(request, (), transaction_participant=participant) == decision
            )
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
def test_stale_prepared_ready_denied_after_body_revocation(database_url, tmp_path):
    async def scenario():
        f = await contract_fixture(database_url, tmp_path)
        try:
            receipt = await f["writer"].issue_task_contract(
                body=f["body"], expected_current_body_sha256=None, issued_at=NOW
            )
            request = request_for(f)
            system = P1_4GuardAuthority()
            participant = await prepare_task_contract_ready(
                f["repo"],
                receipt,
                request,
                system_authority=system,
                judgment_policy_authority=JudgmentPolicyAuthority(f["sessions"]),
            )
            await f["writer"].revoke_task_contract(
                project_id=f["project_id"],
                contract_id=f["body"].value["contract_id"],
                expected_version=1,
                expected_body_sha256=f["body"].body_sha256,
                effective_at=NOW,
            )
            workflow = PostgresTransitionRepository(f["sessions"], TransitionEvaluator(system))
            with pytest.raises(TaskContractError):
                await workflow.decide(request, (), transaction_participant=participant)
            assert await workflow.get_work_run(request.work_run_id) is None
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())
