from __future__ import annotations

import asyncio
import inspect
from datetime import UTC, datetime
from typing import Any, cast

import pytest
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncEngine

import aiscc.api.app as app_module
from aiscc.api.app import create_app
from aiscc.api.routes import command_center as command_center_routes
from aiscc.command_center import postgres_queries
from aiscc.command_center.postgres_queries import PostgresCommandCenterQueries
from aiscc.command_center.privacy import PRIVATE_FIELD_NAMES, contains_private_field
from aiscc.command_center.queries import (
    InvalidQueryError,
    UnavailableCommandCenterQueries,
    decode_cursor,
    encode_cursor,
    validate_limit,
)
from aiscc.command_center.read_models import (
    Availability,
    CycleData,
    DerivedStateEffect,
    ErrorCode,
    ErrorDetail,
    ErrorEnvelope,
    ExecutionSummaryView,
    HumanGateSummaryView,
    HumanGateView,
    HumanJudgmentData,
    HumanResultSummaryView,
    HumanResultView,
    JudgmentSummaryView,
    JudgmentView,
    NextActionSummaryView,
    Presence,
    QueueRow,
    ScopeView,
    TaskContractView,
    TaskDisplayView,
    TransitionDecisionSummaryView,
    TransitionEffectView,
    WorkflowView,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.human.models import HumanResultKind
from aiscc.judgment.models import JudgmentKind, JudgmentOwnerPolicy
from aiscc.providers.models import ExecutionStatus
from aiscc.workflow.models import DecisionOutcome, DecisionReason

NOW = datetime(2026, 9, 3, 1, 0, tzinfo=UTC)


def _queue_row() -> QueueRow:
    return QueueRow(
        project_id="project-1",
        work_run_id="run-1",
        task_contract=TaskContractView(id="task-1", version="v1"),
        task_display=TaskDisplayView(),
        workflow=WorkflowView(
            state=WorkflowState.RUNNING,
            state_version=3,
            updated_at=NOW,
        ),
        execution=ExecutionSummaryView(
            attempt_present=True,
            execution_attempt_id="attempt-1",
            attempt_ordinal=1,
            status=ExecutionStatus.EXECUTOR_COMPLETED,
            execution_version=4,
        ),
        human_gate=HumanGateSummaryView(presence=Presence.NONE),
        human_result=HumanResultSummaryView(presence=Presence.NONE),
        judgment=JudgmentSummaryView(presence=Presence.NONE),
        latest_transition_decision=TransitionDecisionSummaryView(presence=Presence.NONE),
        next_action=NextActionSummaryView(presence=Presence.NONE),
        runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
    )


def test_workflow_and_execution_status_are_independent_exact_enums() -> None:
    payload = _queue_row().model_dump(mode="json")
    assert payload["workflow"]["state"] == "RUNNING"
    assert payload["execution"]["status"] == "EXECUTOR_COMPLETED"
    assert payload["workflow"]["state"] != "ACCEPTED"


def test_executor_completed_cannot_populate_workflow_state() -> None:
    with pytest.raises(ValidationError):
        WorkflowView(
            state=ExecutionStatus.EXECUTOR_COMPLETED,  # type: ignore[arg-type]
            state_version=3,
            updated_at=NOW,
        )


def test_human_result_does_not_populate_judgment() -> None:
    data = HumanJudgmentData(
        work_run_id="run-1",
        human_gate=HumanGateView(presence=Presence.NONE),
        human_result=HumanResultView(
            presence=Presence.PRESENT,
            human_result_id="human-result-1",
            result_kind=HumanResultKind.APPROVE,
            authority_revision=1,
        ),
        judgment=JudgmentView(presence=Presence.NONE),
        transition_effect=TransitionEffectView(presence=Presence.NONE),
    ).model_dump(mode="json")
    assert data["human_result"]["result_kind"] == "APPROVE"
    assert data["judgment"]["presence"] == "NONE"
    assert data["judgment"]["kind"] is None


def test_judgment_does_not_populate_transition_decision() -> None:
    data = HumanJudgmentData(
        work_run_id="run-1",
        human_gate=HumanGateView(presence=Presence.NONE),
        human_result=HumanResultView(presence=Presence.NONE),
        judgment=JudgmentView(
            presence=Presence.PRESENT,
            judgment_id="judgment-1",
            kind=JudgmentKind.ACCEPTED,
            owner_policy=JudgmentOwnerPolicy.HUMAN,
            authority_revision=1,
        ),
        transition_effect=TransitionEffectView(presence=Presence.NONE),
    )
    assert data.judgment.kind is JudgmentKind.ACCEPTED
    assert data.transition_effect.presence is Presence.NONE
    assert data.transition_effect.transition_decision_id is None


def test_denied_transition_is_explicitly_unchanged() -> None:
    effect = TransitionEffectView(
        presence=Presence.PRESENT,
        transition_decision_id="decision-denied",
        outcome=DecisionOutcome.DENIED,
        resulting_state=WorkflowState.RUNNING,
        resulting_state_version=3,
        derived_state_effect=DerivedStateEffect.UNCHANGED,
    )
    assert effect.outcome is DecisionOutcome.DENIED
    assert effect.derived_state_effect is DerivedStateEffect.UNCHANGED


def test_absent_judgment_uses_presence_and_null_kind() -> None:
    payload = JudgmentSummaryView(presence=Presence.NONE).model_dump(mode="json")
    assert payload == {
        "presence": "NONE",
        "judgment_id": None,
        "kind": None,
        "owner_policy": None,
        "authority_revision": None,
    }
    assert "status" not in payload


def test_untrusted_task_metadata_and_scope_are_reference_only() -> None:
    task = TaskDisplayView()
    scope = ScopeView()
    assert task.availability is Availability.REFERENCE_ONLY
    assert task.message == "Metadata unavailable"
    assert task.title is None and task.type is None and task.source_ref is None
    assert scope.availability is Availability.REFERENCE_ONLY
    assert scope.message == "Metadata unavailable"
    assert scope.allowed is None and scope.forbidden is None


def test_privacy_denylist_rejects_owner_and_body_fields() -> None:
    private = {
        "principal_id": "human-1",
        "private_comment_ref": "private://comment",
        "provider_protocol": {"body": "secret"},
        "parameters": {"credential": "secret"},
    }
    assert contains_private_field(private)
    assert {
        "principal_id",
        "private_comment_ref",
        "private_comment_hash",
        "canonical_body",
        "output",
        "parameters",
        "rationale",
        "storage_ref",
    } <= PRIVATE_FIELD_NAMES
    assert not contains_private_field(_queue_row().model_dump(mode="json"))


def test_cursor_is_opaque_shape_bound_and_limit_fails_closed() -> None:
    shape: dict[str, object] = {
        "endpoint": "queue",
        "project_id": "project-1",
        "q": None,
    }
    cursor = encode_cursor(
        shape=shape,
        position={"updated_at": NOW.isoformat(), "work_run_id": "run-1"},
    )
    assert "run-1" not in cursor
    assert decode_cursor(cursor, shape=shape)["work_run_id"] == "run-1"
    with pytest.raises(InvalidQueryError):
        decode_cursor(cursor, shape={**shape, "q": "different"})
    for invalid in (0, 101):
        with pytest.raises(InvalidQueryError):
            validate_limit(invalid)


def test_next_action_read_adapter_has_no_mutation_repository_calls() -> None:
    source = inspect.getsource(postgres_queries.PostgresCommandCenterQueries.next_action)
    assert "PostgresNextActionRepository" not in source
    assert "rebuild_projection" not in source
    assert ".issue(" not in source
    assert ".select(" not in source


def test_runtime_cycle_dto_has_no_repository_governance_record() -> None:
    assert "governance_record" not in CycleData.model_fields
    assert "command_center_cycle_record" not in {name.casefold() for name in CycleData.model_fields}


def test_error_envelope_is_safe_and_extra_details_are_forbidden() -> None:
    error = ErrorEnvelope(
        error=ErrorDetail(
            code=ErrorCode.AUTHORITY_CONFLICT,
            message="The authoritative read model is inconsistent.",
            retryable=False,
            correlation_id="cc-safe",
        )
    ).model_dump(mode="json")
    serialized = str(error).lower()
    assert "select *" not in serialized
    assert "traceback" not in serialized
    assert "private://" not in serialized
    with pytest.raises(ValidationError):
        ErrorEnvelope.model_validate({"error": error["error"], "stack": "private"})


def test_exact_command_center_route_set_has_read_only_methods() -> None:
    create_app()
    routes = {
        str(getattr(route, "path", "")): set(getattr(route, "methods", set()) or set())
        for route in command_center_routes.router.routes
        if str(getattr(route, "path", "")).startswith("/v1/command-center")
    }
    assert set(routes) == {
        "/v1/command-center/projects/{project_id}/queue",
        "/v1/command-center/work-runs/{work_run_id}",
        "/v1/command-center/work-runs/{work_run_id}/transitions",
        "/v1/command-center/work-runs/{work_run_id}/execution",
        "/v1/command-center/work-runs/{work_run_id}/evidence",
        "/v1/command-center/work-runs/{work_run_id}/human-judgment",
        "/v1/command-center/projects/{project_id}/outcomes",
        "/v1/command-center/cycles/{cycle_id}",
        "/v1/command-center/projects/{project_id}/next-action",
    }
    assert all(methods == {"GET", "HEAD", "OPTIONS"} for methods in routes.values())


def test_default_composition_uses_postgres_and_disposes_owned_engine(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class DisposableEngine:
        dispose_calls = 0

        async def dispose(self) -> None:
            self.dispose_calls += 1

    engine = DisposableEngine()
    monkeypatch.setenv("AISCC_DATABASE_URL", "postgresql+asyncpg://configured/runtime")
    monkeypatch.setattr(
        app_module,
        "create_engine",
        lambda _: cast(AsyncEngine, cast(Any, engine)),
    )
    monkeypatch.setattr(app_module, "create_session_factory", lambda _: cast(Any, object()))

    application = create_app()
    assert isinstance(application.state.command_center_queries, PostgresCommandCenterQueries)

    async def exercise_lifespan() -> None:
        async with application.router.lifespan_context(application):
            assert engine.dispose_calls == 0

    asyncio.run(exercise_lifespan())
    assert engine.dispose_calls == 1


def test_default_composition_without_safe_database_config_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("AISCC_DATABASE_URL", raising=False)
    unavailable = create_app()
    assert isinstance(unavailable.state.command_center_queries, UnavailableCommandCenterQueries)

    monkeypatch.setenv("AISCC_DATABASE_URL", "sqlite:///not-authoritative.db")
    invalid = create_app()
    assert isinstance(invalid.state.command_center_queries, UnavailableCommandCenterQueries)


def test_decision_reason_remains_distinct_from_judgment_kind() -> None:
    decision = TransitionDecisionSummaryView(
        presence=Presence.PRESENT,
        decision_id="decision-1",
        outcome=DecisionOutcome.ADMITTED,
        reason=DecisionReason.ADMITTED,
        resulting_state=WorkflowState.ACCEPTED,
        resulting_state_version=4,
    )
    judgment = JudgmentSummaryView(
        presence=Presence.PRESENT,
        judgment_id="judgment-1",
        kind=JudgmentKind.ACCEPTED,
        owner_policy=JudgmentOwnerPolicy.HUMAN,
        authority_revision=1,
    )
    assert decision.reason is DecisionReason.ADMITTED
    assert judgment.kind is JudgmentKind.ACCEPTED
