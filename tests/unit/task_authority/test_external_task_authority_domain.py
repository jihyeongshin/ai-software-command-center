from __future__ import annotations

import copy
import pickle
from datetime import UTC, datetime
from typing import Any, cast

import pytest

import aiscc.task_authority as public_api
from aiscc.task_authority.authority import _bind_repository_once
from aiscc.task_authority.models import (
    AuthorityEventKind,
    NextActionPriorityClass,
    TaskConstraintScopeKind,
    TaskConstraintScopeV1,
)
from aiscc.task_authority.repository import (
    PostgresExternalTaskAuthorityRepository,
    _new_constraint,
    _new_constraint_event,
    _new_context,
)

NOW = datetime(2026, 9, 2, 1, 2, 3, 456789, tzinfo=UTC)


@pytest.mark.parametrize(
    ("kind", "task", "version", "run"),
    [
        (TaskConstraintScopeKind.PROJECT, None, None, None),
        (TaskConstraintScopeKind.TASK_CONTRACT, "task-1", "v1", None),
        (TaskConstraintScopeKind.WORK_RUN, "task-1", "v1", "run-1"),
    ],
)
def test_three_task_constraint_scope_variants_are_closed(
    kind: TaskConstraintScopeKind,
    task: str | None,
    version: str | None,
    run: str | None,
) -> None:
    scope = TaskConstraintScopeV1(kind, "project-1", task, version, run)
    assert scope.payload()["scope_kind"] == kind.value
    constraint = _new_constraint(
        constraint_ref_id=f"constraint-{kind.value.lower()}",
        logical_constraint_id=f"logical-{kind.value.lower()}",
        scope=scope,
        constraint_schema_id="TASK_CONSTRAINT_PAYLOAD_V1",
        constraint_schema_version="v1",
        constraint_payload_ref="constraint-payload:v1:payload-1",
        constraint_payload_fingerprint="a" * 64,
        issued_at=NOW,
        issuance_sequence=1,
    )
    assert constraint.constraint_fingerprint == constraint.constraint_fingerprint.lower()


def test_scope_non_applicable_fields_and_event_variants_fail_closed() -> None:
    with pytest.raises(ValueError):
        TaskConstraintScopeV1(TaskConstraintScopeKind.PROJECT, "project-1", "task-1", "v1", None)
    scope = TaskConstraintScopeV1(
        TaskConstraintScopeKind.TASK_CONTRACT, "project-1", "task-1", "v1"
    )
    constraint = _new_constraint(
        constraint_ref_id="constraint-1",
        logical_constraint_id="logical-1",
        scope=scope,
        constraint_schema_id="TASK_CONSTRAINT_PAYLOAD_V1",
        constraint_schema_version="v1",
        constraint_payload_ref="constraint-payload:v1:payload-1",
        constraint_payload_fingerprint="a" * 64,
        issued_at=NOW,
        issuance_sequence=1,
    )
    issued = _new_constraint_event(
        event_id="constraint-issued-1",
        event_kind=AuthorityEventKind.ISSUED,
        target=constraint,
        replacement=None,
        event_sequence=1,
        effective_sequence=1,
        effective_at=NOW,
    )
    assert issued.replacement_constraint_ref is None
    with pytest.raises(ValueError):
        _new_constraint_event(
            event_id="constraint-superseded-1",
            event_kind=AuthorityEventKind.SUPERSEDED,
            target=constraint,
            replacement=None,
            event_sequence=2,
            effective_sequence=2,
            effective_at=NOW,
        )


def test_context_owner_fields_and_safe_ordinal_are_exact() -> None:
    context = _new_context(
        context_ref_id="context-1",
        context_logical_id="next-action-context-lineage:v1:planning-1",
        project_id="project-1",
        task_contract_id="task-1",
        task_contract_version="v1",
        context_slot_id="primary",
        priority_class=NextActionPriorityClass.OPERATIONAL_HARDENING,
        critical_path_ordinal=7,
        issued_at=NOW,
        issuance_sequence=1,
        effective_sequence=1,
    )
    assert context.priority_class is NextActionPriorityClass.OPERATIONAL_HARDENING
    with pytest.raises(ValueError):
        _new_context(
            context_ref_id="context-2",
            context_logical_id="next-action-context-lineage:v1:planning-2",
            project_id="project-1",
            task_contract_id="task-1",
            task_contract_version="v1",
            context_slot_id="primary",
            priority_class=NextActionPriorityClass.OPTIONAL_OPTIMIZATION,
            critical_path_ordinal=1_000_001,
            issued_at=NOW,
            issuance_sequence=2,
            effective_sequence=1,
        )


def test_live_capability_is_not_public_copyable_serializable_or_rebindable() -> None:
    assert "PostgresExternalTaskAuthorityRepository" not in public_api.__all__
    assert "_ExternalTaskAuthorityWriter" not in public_api.__all__
    repository = PostgresExternalTaskAuthorityRepository(cast(Any, object()))
    writer = _bind_repository_once(repository)
    with pytest.raises(TypeError):
        copy.copy(writer)
    with pytest.raises(TypeError):
        copy.deepcopy(writer)
    with pytest.raises(TypeError):
        pickle.dumps(writer)
    with pytest.raises(RuntimeError):
        _bind_repository_once(repository)
