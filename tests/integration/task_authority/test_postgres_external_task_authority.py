from __future__ import annotations

import asyncio
import os
from collections.abc import Coroutine
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

import pytest
from sqlalchemy import func, select

from aiscc.persistence import create_engine, create_session_factory
from aiscc.persistence.models import ExternalTaskAuthorityEventRegistryRow
from aiscc.task_authority.authority import _bind_repository_once
from aiscc.task_authority.models import (
    ExternalTaskAuthorityError,
    ExternalTaskAuthorityErrorCode,
    NextActionPriorityClass,
    TaskConstraintScopeKind,
    TaskConstraintScopeV1,
)
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository


def run[T](coroutine: Coroutine[Any, Any, T]) -> T:
    return asyncio.run(coroutine)


@pytest.fixture(scope="module")
def database_url() -> str:
    value = os.environ.get("AISCC_TEST_DATABASE_URL")
    if not value:
        pytest.skip("AISCC_TEST_DATABASE_URL is required for PostgreSQL evidence")
    return value


@pytest.mark.postgres
def test_external_authority_issue_supersede_revoke_snapshot_and_restart(
    database_url: str,
) -> None:
    async def scenario() -> None:
        engine = create_engine(database_url)
        sessions = create_session_factory(engine)
        repository = PostgresExternalTaskAuthorityRepository(sessions)
        writer = _bind_repository_once(repository)
        suffix = uuid4().hex
        now = datetime.now(UTC)
        scope = TaskConstraintScopeV1(
            TaskConstraintScopeKind.TASK_CONTRACT,
            f"project-{suffix}",
            f"task-{suffix}",
            "v1",
        )
        original, issued = await writer.issue_task_constraint(
            constraint_ref_id=f"constraint-{suffix}",
            logical_constraint_id=f"logical-{suffix}",
            scope=scope,
            constraint_schema_id="TASK_CONSTRAINT_PAYLOAD_V1",
            constraint_schema_version="v1",
            constraint_payload_ref=f"constraint-payload:v1:{suffix}",
            constraint_payload_fingerprint="a" * 64,
            event_id=f"constraint-issued-{suffix}",
            issued_at=now,
        )
        snapshot_1 = await writer.certify_snapshot(
            snapshot_id=f"snapshot-1-{suffix}", issued_at=now
        )
        historical = await repository.verify_task_constraint(
            constraint_ref=original.constraint_ref,
            constraint_fingerprint=original.constraint_fingerprint,
            snapshot_ref=snapshot_1.snapshot_ref,
            snapshot_fingerprint=snapshot_1.snapshot_fingerprint,
            owner_event_high_watermark=snapshot_1.owner_event_high_watermark,
            require_current=True,
        )
        assert historical.current == original
        assert historical.consumed_event_refs == (issued.event_ref,)

        replacement, superseded = await writer.supersede_task_constraint(
            current_constraint_ref=original.constraint_ref,
            replacement_ref_id=f"constraint-replacement-{suffix}",
            constraint_schema_id="TASK_CONSTRAINT_PAYLOAD_V1",
            constraint_schema_version="v1",
            constraint_payload_ref=f"constraint-payload:v1:replacement-{suffix}",
            constraint_payload_fingerprint="b" * 64,
            event_id=f"constraint-superseded-{suffix}",
            effective_at=now,
        )
        context, context_issued = await writer.issue_next_action_context(
            context_ref_id=f"context-{suffix}",
            context_logical_local_id=f"planning-{suffix}",
            project_id=scope.project_id,
            task_contract_id=str(scope.task_contract_id),
            task_contract_version=str(scope.task_contract_version),
            context_slot_id="primary",
            priority_class=NextActionPriorityClass.ACCEPTED_CORE_CRITICAL_PATH,
            critical_path_ordinal=1,
            event_id=f"context-issued-{suffix}",
            issued_at=now,
        )
        snapshot_2 = await writer.certify_snapshot(
            snapshot_id=f"snapshot-2-{suffix}", issued_at=now
        )
        restarted = PostgresExternalTaskAuthorityRepository(sessions)
        current = await restarted.verify_task_constraint(
            constraint_ref=replacement.constraint_ref,
            constraint_fingerprint=replacement.constraint_fingerprint,
            snapshot_ref=snapshot_2.snapshot_ref,
            snapshot_fingerprint=snapshot_2.snapshot_fingerprint,
            owner_event_high_watermark=snapshot_2.owner_event_high_watermark,
            require_current=True,
        )
        assert current.current == replacement
        assert current.consumed_event_refs[-1] == superseded.event_ref
        replay = await restarted.verify_task_constraint(
            constraint_ref=original.constraint_ref,
            constraint_fingerprint=original.constraint_fingerprint,
            snapshot_ref=snapshot_1.snapshot_ref,
            snapshot_fingerprint=snapshot_1.snapshot_fingerprint,
            owner_event_high_watermark=snapshot_1.owner_event_high_watermark,
            require_current=False,
        )
        assert replay.current == original
        await restarted.verify_next_action_context(
            context_ref=context.context_ref,
            context_fingerprint=context.fingerprint,
            introduction_event_ref=context_issued.event_ref,
            introduction_event_fingerprint=context_issued.event_fingerprint,
            snapshot_ref=snapshot_2.snapshot_ref,
            snapshot_fingerprint=snapshot_2.snapshot_fingerprint,
            owner_event_high_watermark=snapshot_2.owner_event_high_watermark,
            require_current=True,
        )

        await writer.revoke_next_action_context(
            current_context_ref=context.context_ref,
            event_id=f"context-revoked-{suffix}",
            effective_at=now,
        )
        snapshot_3 = await writer.certify_snapshot(
            snapshot_id=f"snapshot-3-{suffix}", issued_at=now
        )
        with pytest.raises(ExternalTaskAuthorityError) as raised:
            await restarted.verify_next_action_context(
                context_ref=context.context_ref,
                context_fingerprint=context.fingerprint,
                introduction_event_ref=context_issued.event_ref,
                introduction_event_fingerprint=context_issued.event_fingerprint,
                snapshot_ref=snapshot_3.snapshot_ref,
                snapshot_fingerprint=snapshot_3.snapshot_fingerprint,
                owner_event_high_watermark=snapshot_3.owner_event_high_watermark,
                require_current=True,
            )
        assert raised.value.code is ExternalTaskAuthorityErrorCode.NOT_CURRENT
        await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_global_sequence_concurrency_is_contiguous_and_conflicts_are_atomic(
    database_url: str,
) -> None:
    async def scenario() -> None:
        engine = create_engine(database_url)
        sessions = create_session_factory(engine)
        repository = PostgresExternalTaskAuthorityRepository(sessions)
        writer = _bind_repository_once(repository)
        suffix = uuid4().hex
        now = datetime.now(UTC)

        async def issue(ordinal: int) -> None:
            scope = TaskConstraintScopeV1(
                TaskConstraintScopeKind.PROJECT, f"project-{suffix}-{ordinal}"
            )
            await writer.issue_task_constraint(
                constraint_ref_id=f"constraint-{suffix}-{ordinal}",
                logical_constraint_id=f"logical-{suffix}-{ordinal}",
                scope=scope,
                constraint_schema_id="TASK_CONSTRAINT_PAYLOAD_V1",
                constraint_schema_version="v1",
                constraint_payload_ref=f"constraint-payload:v1:{suffix}-{ordinal}",
                constraint_payload_fingerprint=f"{ordinal:x}" * 64,
                event_id=f"constraint-issued-{suffix}-{ordinal}",
                issued_at=now,
            )

        await asyncio.gather(issue(1), issue(2))
        snapshot = await writer.certify_snapshot(
            snapshot_id=f"snapshot-concurrent-{suffix}", issued_at=now
        )
        async with sessions() as session:
            rows = tuple(
                await session.scalars(
                    select(ExternalTaskAuthorityEventRegistryRow).order_by(
                        ExternalTaskAuthorityEventRegistryRow.event_sequence
                    )
                )
            )
            maximum = int(
                await session.scalar(
                    select(
                        func.max(ExternalTaskAuthorityEventRegistryRow.event_sequence)
                    )
                )
                or 0
            )
        assert snapshot.owner_event_high_watermark == maximum
        assert [row.event_sequence for row in rows] == list(range(1, maximum + 1))

        conflict_scope = TaskConstraintScopeV1(
            TaskConstraintScopeKind.PROJECT, f"project-conflict-{suffix}"
        )
        await writer.issue_task_constraint(
            constraint_ref_id=f"conflict-a-{suffix}",
            logical_constraint_id=f"conflict-{suffix}",
            scope=conflict_scope,
            constraint_schema_id="TASK_CONSTRAINT_PAYLOAD_V1",
            constraint_schema_version="v1",
            constraint_payload_ref=f"constraint-payload:v1:conflict-a-{suffix}",
            constraint_payload_fingerprint="a" * 64,
            event_id=f"conflict-issued-a-{suffix}",
            issued_at=now,
        )
        with pytest.raises(ExternalTaskAuthorityError):
            await writer.issue_task_constraint(
                constraint_ref_id=f"conflict-b-{suffix}",
                logical_constraint_id=f"conflict-{suffix}",
                scope=conflict_scope,
                constraint_schema_id="TASK_CONSTRAINT_PAYLOAD_V1",
                constraint_schema_version="v1",
                constraint_payload_ref=f"constraint-payload:v1:conflict-b-{suffix}",
                constraint_payload_fingerprint="b" * 64,
                event_id=f"conflict-issued-b-{suffix}",
                issued_at=now,
            )
        await engine.dispose()

    run(scenario())
