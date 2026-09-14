import asyncio
from dataclasses import replace
from datetime import timedelta

import pytest
from sqlalchemy import text

from aiscc.contracts.workflow import WorkflowState
from aiscc.providers.external_ide import (
    START_PREFIX,
    ExternalIdeExecutionStartRepository,
    LocalGitObserver,
)
from aiscc.workflow.guards import P1_4GuardAuthority
from aiscc.workflow.models import DecisionOutcome
from tests.integration.providers.test_external_ide_execution_start import (
    TASK,
    count_starts,
    fixture,
    start,
)
from tests.integration.task_authority.test_task_contract_durability import (
    database_url as database_url,
)
from tests.unit.providers.test_external_ide_execution_ingress import GIT, NOW


@pytest.mark.postgres
def test_denied_p1_4_owner_evaluation_rolls_back_start_authority(database_url, tmp_path):
    async def scenario():
        f = await fixture(database_url, tmp_path)
        try:
            # A different P1-4 issuer is genuinely unrecognized by this evaluator.
            # No monkeypatch, fake transition result or direct WorkRun write.
            f["starts"] = ExternalIdeExecutionStartRepository(
                f["sessions"],
                f["repo"],
                LocalGitObserver(GIT, clock=lambda: NOW),
                system_authority=P1_4GuardAuthority(),
                transition_repository=f["args"]["transition_repository"],
                clock=lambda: NOW,
            )
            with pytest.raises(ValueError, match="P1-4 start denied"):
                await start(f)
            assert await count_starts(f) == 0
            run = await f["args"]["transition_repository"].get_work_run(f["args"]["work_run_id"])
            assert (run.state, run.state_version) == (WorkflowState.READY, 1)
            assert (
                await f["args"]["transition_repository"].get_decision(
                    f["start"].transition_request_id
                )
                is None
            )
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
def test_competing_exact_state_version_starts_admit_only_one(database_url, tmp_path):
    async def scenario():
        f = await fixture(database_url, tmp_path)
        try:
            second = replace(f["start"], transition_request_id="competing-start")
            results = await asyncio.gather(
                start(f), start(f, request=second), return_exceptions=True
            )
            admitted = [r for r in results if not isinstance(r, Exception)]
            assert len(admitted) == 1 and admitted[0].outcome is DecisionOutcome.ADMITTED
            assert await count_starts(f) == 1
            async with f["sessions"]() as session, session.begin():
                with pytest.raises(ValueError, match="READY"):
                    await f["start_writer"].issue(
                        session,
                        receipt=f["receipt"],
                        work_run_id=f["args"]["work_run_id"],
                        state_version=1,
                        ready_transition_id=f["args"]["transition_request_id"],
                        inner_task_bytes=TASK,
                        ttl=timedelta(minutes=10),
                    )
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize("corruption", ["permit_hash", "start_hash", "start_missing"])
def test_restart_corruption_denies_without_repair(database_url, tmp_path, corruption):
    async def scenario():
        f = await fixture(database_url, tmp_path)
        try:
            await start(f)
            # Transaction-local tamper simulation, always rolled back. No durable repair.
            async with f["sessions"]() as session:
                tx = await session.begin()
                try:
                    await session.execute(text("SET LOCAL session_replication_role = replica"))
                    if corruption == "permit_hash":
                        await session.execute(
                            text(
                                "UPDATE external_ide_execution_start_permits "
                                "SET body_sha256=:h WHERE permit_id=:p"
                            ),
                            {"h": "0" * 64, "p": f["permit"].value["permit_id"]},
                        )
                    elif corruption == "start_hash":
                        await session.execute(
                            text(
                                "UPDATE external_ide_execution_starts "
                                "SET body_sha256=:h WHERE permit_id=:p"
                            ),
                            {"h": "0" * 64, "p": f["permit"].value["permit_id"]},
                        )
                    else:
                        await session.execute(
                            text("DELETE FROM external_ide_execution_starts WHERE permit_id=:p"),
                            {"p": f["permit"].value["permit_id"]},
                        )
                    from aiscc.providers.external_ide import verify_external_start_in_session

                    with pytest.raises(ValueError):
                        await verify_external_start_in_session(
                            session, START_PREFIX + f["permit"].value["permit_id"]
                        )
                finally:
                    await tx.rollback()
            await f["starts"].resolve(START_PREFIX + f["permit"].value["permit_id"])
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())
