from __future__ import annotations

import asyncio
import os
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

import pytest
from fake_responses_server import FakeResponsesServer, final_message, response_body
from sqlalchemy import select, text

from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.persistence import PostgresExecutionRepository, create_engine, create_session_factory
from aiscc.persistence.models import ExecutionAttemptRow, ExecutionOperationRow, WorkRunRow
from aiscc.providers.models import (
    ExecutionAttemptRef,
    ExecutionOperationOutcome,
    ExecutionOperationPhase,
    ExecutionStatus,
    OperationKind,
    ProviderCall,
    ProviderResult,
    SecretResolutionLease,
    canonical_sha256,
)
from aiscc.providers.openai_responses import OpenAIResponsesAdapter
from aiscc.providers.profiles import load_provider_profile
from aiscc.providers.service import AgentExecutionService
from aiscc.security.policy import SecurityPolicy, default_profiles


class NotReachedAdapter:
    def call(self, call: ProviderCall, *, secret: str) -> ProviderResult:
        del call, secret
        raise AssertionError("provider adapter must not be reached by retry admission")


class NotReachedResolver:
    def resolve(self, lease: SecretResolutionLease) -> str:
        del lease
        raise AssertionError("secret resolver must not be reached by retry admission")

    def close(self, lease: SecretResolutionLease) -> None:
        del lease


class NotReachedAuthorityReader:
    def load(
        self, *, work_run_id: str, execution_attempt_id: str
    ) -> tuple[WorkflowSnapshot, ExecutionAttemptRef]:
        del work_run_id, execution_attempt_id
        raise AssertionError("authority reader must not be reached by retry admission")


@pytest.mark.runtime
def test_local_transport_unknown_is_durable_classification_and_not_blindly_retried() -> None:
    profile = load_provider_profile(
        Path("config/providers/provider-profiles.v1.toml"), "fake-openai-responses-v1"
    )
    unique = uuid4().hex
    run_id, attempt_id, operation_id = (
        f"runtime-run-{unique}",
        f"runtime-attempt-{unique}",
        f"runtime-operation-{unique}",
    )
    call = ProviderCall(
        operation_id,
        canonical_sha256({"unknown": 1}),
        attempt_id,
        run_id,
        WorkflowState.RUNNING,
        2,
        RuntimeMode.OWNER_SELF_DOGFOOD,
        "owner",
        "p1-5-fixed-synthetic",
        2,
        profile,
        ({"role": "user", "content": "fixed"},),
        (),
        1,
    )
    database_url = os.environ["AISCC_TEST_DATABASE_URL"]
    engine = create_engine(database_url)
    factory = create_session_factory(engine)
    adapter = OpenAIResponsesAdapter()

    async def scenario() -> None:
        now = datetime.now(UTC)
        async with factory() as session, session.begin():
            session.add(
                WorkRunRow(
                    work_run_id=run_id,
                    project_id=f"runtime-{unique}",
                    task_contract_id="task",
                    task_contract_version="1",
                    workflow_state="READY",
                    state_version=1,
                    runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD.value,
                    created_at=now,
                    updated_at=now,
                )
            )
        repository = PostgresExecutionRepository(factory)
        await repository.create_attempt(
            attempt_id=attempt_id,
            work_run_id=run_id,
            profile_id=profile.profile_id,
            profile_version=profile.version,
            registry_id=profile.tool_registry_id,
            registry_version=profile.tool_registry_version,
        )
        async with factory() as session, session.begin():
            await session.execute(
                text(
                    "UPDATE work_runs SET workflow_state='RUNNING', state_version=2 "
                    "WHERE work_run_id=:id"
                ),
                {"id": run_id},
            )
        await repository.transition_attempt(attempt_id, "EXECUTION_STARTED")
        await repository.create_operation(
            operation_id=operation_id,
            attempt_id=attempt_id,
            kind=OperationKind.PROVIDER,
            fingerprint=call.operation_fingerprint,
            resource_identity=profile.canonical_identity.serialized(),
            call_ordinal=1,
        )
        await repository.advance_operation(operation_id, ExecutionOperationPhase.SECURITY_ADMITTED)
        await repository.advance_operation(operation_id, ExecutionOperationPhase.DISPATCH_STARTED)
        result = adapter.call(call, secret="synthetic-local-only")
        assert result.outcome is ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
        await repository.advance_operation(
            operation_id,
            ExecutionOperationPhase.OUTCOME_UNKNOWN,
            result.outcome,
            refs={"budget": "conservatively-retained", "retry": "forbidden"},
        )
        await repository.transition_attempt(
            attempt_id,
            "EXECUTION_FAILED",
            refs={"failure_class": "UNKNOWN_OUTCOME", "blind_retry": False},
        )
        async with factory() as session:
            attempt = await session.scalar(
                select(ExecutionAttemptRow).where(
                    ExecutionAttemptRow.execution_attempt_id == attempt_id
                )
            )
            operation = await session.get(ExecutionOperationRow, operation_id)
            work_run = await session.get(WorkRunRow, run_id)
            assert attempt is not None and attempt.status == ExecutionStatus.EXECUTION_FAILED.value
            assert operation is not None and operation.current_phase == "OUTCOME_UNKNOWN"
            assert operation.outcome == result.outcome.value
            assert work_run is not None and work_run.workflow_state == "RUNNING"
            assert work_run.state_version == 2
        assert adapter.invocation_count == 1

    try:
        asyncio.run(scenario())
    finally:
        asyncio.run(engine.dispose())


@pytest.mark.runtime
def test_definitely_not_sent_retry_is_separately_bounded_without_dispatch() -> None:
    profile = load_provider_profile(
        Path("config/providers/provider-profiles.v1.toml"), "fake-openai-responses-v1"
    )
    call = ProviderCall(
        "retry-operation",
        canonical_sha256({"retry": "definitely-not-sent"}),
        "retry-attempt",
        "retry-run",
        WorkflowState.RUNNING,
        2,
        RuntimeMode.OWNER_SELF_DOGFOOD,
        "owner",
        "p1-5-fixed-synthetic",
        2,
        profile,
        ({"role": "user", "content": "fixed"},),
        (),
        1,
    )
    service = AgentExecutionService(
        policy=SecurityPolicy(default_profiles()),
        adapter=NotReachedAdapter(),
        secret_resolver=NotReachedResolver(),
        authority_reader=NotReachedAuthorityReader(),
    )
    for _ in range(profile.provider_retry_maximum):
        service.admit_provider_retry(
            call, previous_outcome=ExecutionOperationOutcome.DEFINITELY_NOT_SENT
        )
    with pytest.raises(ValueError, match="RETRIES"):
        service.admit_provider_retry(
            call, previous_outcome=ExecutionOperationOutcome.DEFINITELY_NOT_SENT
        )
    assert service.counters.retries == profile.provider_retry_maximum


@pytest.mark.runtime
def test_official_sdk_runtime_call_is_local_stateless_and_provider_hosted_tools_are_absent() -> (
    None
):
    profile = load_provider_profile(
        Path("config/providers/provider-profiles.v1.toml"), "fake-openai-responses-v1"
    )
    call = ProviderCall(
        "local-runtime-operation",
        canonical_sha256({"runtime": "local-fake"}),
        "local-runtime-attempt",
        "local-runtime-run",
        WorkflowState.RUNNING,
        2,
        RuntimeMode.OWNER_SELF_DOGFOOD,
        "owner",
        "p1-5-fixed-synthetic",
        2,
        profile,
        ({"role": "user", "content": "fixed synthetic runtime"},),
        (),
        1,
    )
    with FakeResponsesServer() as server:
        server.enqueue(response_body("completed", [final_message()]))
        adapter = OpenAIResponsesAdapter()
        result = adapter.call(call, secret="synthetic-local-only")
    assert result.outcome is ExecutionOperationOutcome.PROVIDER_COMPLETED
    request = server.requests[0]
    assert request["store"] is False and request["background"] is False
    assert "conversation" not in request and "previous_response_id" not in request
    assert request["tools"] == []
