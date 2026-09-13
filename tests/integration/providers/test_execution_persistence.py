from __future__ import annotations

import asyncio
import hashlib
import os
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from types import MappingProxyType
from typing import Any
from uuid import uuid4

import pytest
from fake_responses_server import (
    FakeResponsesServer,
    final_message,
    response_body,
)
from sqlalchemy import func, select, text
from sqlalchemy.exc import DBAPIError

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.persistence import (
    PostgresExecutionRepository,
    PostgresTransitionRepository,
    create_engine,
    create_session_factory,
)
from aiscc.persistence.models import (
    ExecutionAttemptRow,
    ExecutionEventRow,
    ExecutionOperationRow,
    OperationEventRow,
    P1_4BlockerProjectionRow,
    P1_4BlockerProvenanceRow,
    PrivateProviderProtocolStateRow,
    WorkRunRow,
)
from aiscc.providers.authority import (
    ExecutionReferenceAuthority,
    LeaseBoundSecretResolver,
    ProviderToolResourceAuthority,
    SecretResolutionLeaseAuthority,
    SecretUseAuthority,
)
from aiscc.providers.models import (
    ExecutionAttemptRef,
    ExecutionOperationOutcome,
    ExecutionOperationPhase,
    ExecutionStatus,
    OperationKind,
    ProviderProfile,
    ResourceRequirement,
    ToolDefinition,
    ToolOutputRef,
    ToolRegistry,
    canonical_json_bytes,
    canonical_sha256,
)
from aiscc.providers.openai_responses import OpenAIResponsesAdapter
from aiscc.providers.profiles import load_provider_profile, load_tool_registry
from aiscc.providers.service import AgentExecutionService
from aiscc.security.capability import (
    CapabilityConsumeRequest,
    CapabilityConsumptionReceipt,
    CapabilityUse,
)
from aiscc.security.policy import SecurityPolicy, default_profiles
from aiscc.workflow.evaluator import TransitionEvaluator
from aiscc.workflow.guards import P1_4GuardAuthority, TrustedGuardFact
from aiscc.workflow.kernel import WorkflowKernel
from aiscc.workflow.matrix import TRANSITION_MATRIX
from aiscc.workflow.models import (
    AuthorityConflictError,
    BlockerKindV1,
    BlockerReasonCodeV1,
    DecisionOutcome,
    GuardId,
    P1_4BlockerClaimV1,
    RequesterType,
    TransitionRequest,
)


def run(coroutine: Any) -> Any:
    return asyncio.run(coroutine)


class DurableSyntheticDispatcher:
    def __init__(self) -> None:
        self.calls = 0

    def dispatch(
        self,
        definition: ToolDefinition,
        arguments: dict[str, object],
        *,
        secret: str | None = None,
    ) -> ToolOutputRef:
        assert definition.tool_id == "synthetic_lookup"
        assert arguments == {"key": "aiscc-fixed-key"}
        assert secret is None
        self.calls += 1
        output = {"value": "AISCC_DURABLE_TOOL_OK"}
        fingerprint = canonical_sha256(
            {
                "registry_id": "aiscc-p1-5-tools",
                "registry_version": "1",
                "tool_id": definition.tool_id,
                "schema_version": definition.schema_version,
                "dispatcher_version": definition.dispatcher_version,
                "arguments": arguments,
                "underlying_resource_requirements": [],
                "secret_requirement": None,
                "resolved_dispatch_context": None,
            }
        )
        return ToolOutputRef(
            output_id=f"durable-tool-output-{self.calls}",
            operation_id=f"durable-tool-operation-{self.calls}",
            argument_hash=fingerprint,
            result_hash=canonical_sha256(output),
            output=output,
        )


class UnusedSyncAuthorityReader:
    def load(
        self, *, work_run_id: str, execution_attempt_id: str
    ) -> tuple[WorkflowSnapshot, ExecutionAttemptRef]:
        del work_run_id, execution_attempt_id
        raise AssertionError("durable service must use PostgresExecutionRepository")


class DenySecondAtomicBatchPolicy(SecurityPolicy):
    atomic_batches = 0

    def consume_capabilities_atomically_with_receipts(
        self,
        requirements: tuple[CapabilityConsumeRequest, ...],
        *,
        now: datetime | None = None,
    ) -> tuple[tuple[CapabilityUse, ...], tuple[CapabilityConsumptionReceipt, ...]]:
        self.atomic_batches += 1
        if self.atomic_batches == 2:
            return (
                (
                    CapabilityUse.create(
                        allowed=False,
                        reason="TEST_ATOMIC_BATCH_DENIED",
                        consumed_use_count=0,
                        provenance={"proof": "TOOL_ATOMIC_BATCH"},
                    ),
                ),
                (),
            )
        return super().consume_capabilities_atomically_with_receipts(
            requirements,
            now=now,
        )


class SameDomainWrongResourceService(AgentExecutionService):
    def _issue_capability(
        self,
        *,
        current: WorkflowSnapshot,
        mode: RuntimeMode,
        principal: str,
        scenario_id: str,
        scope: ResourceScope,
        selector_ref: str | None,
        selector_request: object | None,
        fingerprint: str,
        action: SecurityActionClass = SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        execution_attempt_id: str = "",
        provider_profile_id: str = "",
        provider_profile_version: str = "",
        resolved_spec_fingerprint: str = "",
    ) -> CapabilityConsumeRequest:
        if scope == ResourceScope(ResourceDomain.FILESYSTEM, "workspace:server-owned-exact"):
            scope = ResourceScope(ResourceDomain.FILESYSTEM, "workspace:same-domain-wrong")
        return super()._issue_capability(
            current=current,
            mode=mode,
            principal=principal,
            scenario_id=scenario_id,
            scope=scope,
            selector_ref=selector_ref,
            selector_request=selector_request,
            fingerprint=fingerprint,
            action=action,
            execution_attempt_id=execution_attempt_id,
            provider_profile_id=provider_profile_id,
            provider_profile_version=provider_profile_version,
            resolved_spec_fingerprint=resolved_spec_fingerprint,
        )


@pytest.mark.postgres
def test_execution_lifecycle_operation_restart_consistency_and_state_version_separation() -> None:
    database_url = os.environ["AISCC_TEST_DATABASE_URL"]
    engine = create_engine(database_url)
    factory = create_session_factory(engine)
    run_id, attempt_id, operation_id = (f"p15-{uuid4().hex}" for _ in range(3))

    async def scenario() -> None:
        now = datetime.now(UTC)
        async with factory() as session, session.begin():
            session.add(
                WorkRunRow(
                    work_run_id=run_id,
                    project_id="project",
                    task_contract_id="task",
                    task_contract_version="1",
                    workflow_state="READY",
                    state_version=1,
                    runtime_mode="OWNER_SELF_DOGFOOD",
                    created_at=now,
                    updated_at=now,
                )
            )
        repository = PostgresExecutionRepository(factory)
        await repository.create_attempt(
            attempt_id=attempt_id,
            work_run_id=run_id,
            profile_id="fake-openai-responses-v1",
            profile_version="1",
            registry_id="aiscc-p1-5-tools",
            registry_version="1",
        )
        async with factory() as session, session.begin():
            await session.execute(
                text(
                    "UPDATE work_runs SET workflow_state='RUNNING', state_version=2 "
                    "WHERE work_run_id=:id"
                ),
                {"id": run_id},
            )
        assert (
            await repository.transition_attempt(attempt_id, "EXECUTION_STARTED")
            is ExecutionStatus.RUNNING
        )
        await repository.create_operation(
            operation_id=operation_id,
            attempt_id=attempt_id,
            kind=OperationKind.PROVIDER,
            fingerprint="a" * 64,
            resource_identity="provider:fake",
            call_ordinal=1,
        )
        await repository.advance_operation(operation_id, ExecutionOperationPhase.SECURITY_ADMITTED)
        await repository.advance_operation(operation_id, ExecutionOperationPhase.DISPATCH_STARTED)
        await repository.advance_operation(
            operation_id,
            ExecutionOperationPhase.OUTCOME_KNOWN,
            ExecutionOperationOutcome.PROVIDER_COMPLETED,
        )
        protocol_body = b'{"type":"message"}'
        await repository.store_private_protocol_item(
            state_id=f"state-{operation_id}",
            attempt_id=attempt_id,
            operation_id=operation_id,
            ordinal=1,
            item_type="message",
            item_hash=hashlib.sha256(protocol_body).hexdigest(),
            call_id=None,
            encrypted_body_ref="private://opaque",
            body_bytes=protocol_body,
            classification="PRIVATE_PROVIDER_PROTOCOL",
            byte_count=len(protocol_body),
        )
        await repository.store_output_ref(
            ref_id=f"output-{attempt_id}",
            attempt_id=attempt_id,
            kind="AgentOutputRef",
            content_hash="c" * 64,
            storage_ref="private://output",
        )
        completed = await asyncio.gather(
            repository.transition_attempt(
                attempt_id,
                "EXECUTION_COMPLETED",
                refs={
                    "execution_submission_ref": f"submission-{attempt_id}",
                    "execution_submission_hash": "d" * 64,
                    "execution_submission_storage_ref": "private://submission",
                },
            ),
            repository.transition_attempt(
                attempt_id,
                "EXECUTION_COMPLETED",
                refs={
                    "execution_submission_ref": f"submission-{attempt_id}",
                    "execution_submission_hash": "d" * 64,
                    "execution_submission_storage_ref": "private://submission",
                },
            ),
        )
        assert tuple(completed) == (ExecutionStatus.EXECUTOR_COMPLETED,) * 2
        restarted = PostgresExecutionRepository(factory)
        async with factory() as session:
            attempt = await session.scalar(
                select(ExecutionAttemptRow).where(
                    ExecutionAttemptRow.execution_attempt_id == attempt_id
                )
            )
            work_run = await session.get(WorkRunRow, run_id)
            assert attempt is not None and attempt.status == "EXECUTOR_COMPLETED"
            assert work_run is not None and work_run.state_version == 2
        async with factory() as session, session.begin():
            await session.execute(
                text(
                    "UPDATE execution_attempts SET execution_version=99 "
                    "WHERE execution_attempt_id=:id"
                ),
                {"id": attempt_id},
            )
        with pytest.raises(AuthorityConflictError):
            await restarted.transition_attempt(attempt_id, "EXECUTION_FAILED")

    try:
        run(scenario())
    finally:
        run(engine.dispose())


@pytest.mark.postgres
def test_concurrent_idempotency_unknown_outcome_and_append_only_fail_closed() -> None:
    database_url = os.environ["AISCC_TEST_DATABASE_URL"]
    engine = create_engine(database_url)
    factory = create_session_factory(engine)
    run_id, attempt_id, operation_id = (f"p15-{uuid4().hex}" for _ in range(3))

    async def scenario() -> None:
        now = datetime.now(UTC)
        async with factory() as session, session.begin():
            session.add(
                WorkRunRow(
                    work_run_id=run_id,
                    project_id="project",
                    task_contract_id="task",
                    task_contract_version="1",
                    workflow_state="READY",
                    state_version=1,
                    runtime_mode="OWNER_SELF_DOGFOOD",
                    created_at=now,
                    updated_at=now,
                )
            )
        repository = PostgresExecutionRepository(factory)
        created = await asyncio.gather(
            repository.create_attempt(
                attempt_id=attempt_id,
                work_run_id=run_id,
                profile_id="fake-openai-responses-v1",
                profile_version="1",
                registry_id="aiscc-p1-5-tools",
                registry_version="1",
            ),
            repository.create_attempt(
                attempt_id=attempt_id,
                work_run_id=run_id,
                profile_id="fake-openai-responses-v1",
                profile_version="1",
                registry_id="aiscc-p1-5-tools",
                registry_version="1",
            ),
        )
        assert [row.execution_attempt_id for row in created] == [attempt_id, attempt_id]
        with pytest.raises(AuthorityConflictError, match="identity conflict"):
            await repository.create_attempt(
                attempt_id=attempt_id,
                work_run_id=run_id,
                profile_id="different-profile",
                profile_version="1",
                registry_id="aiscc-p1-5-tools",
                registry_version="1",
            )
        async with factory() as session, session.begin():
            await session.execute(
                text(
                    "UPDATE work_runs SET workflow_state='RUNNING', state_version=2 "
                    "WHERE work_run_id=:id"
                ),
                {"id": run_id},
            )
        started = await asyncio.gather(
            repository.transition_attempt(attempt_id, "EXECUTION_STARTED"),
            repository.transition_attempt(attempt_id, "EXECUTION_STARTED"),
        )
        assert tuple(started) == (ExecutionStatus.RUNNING, ExecutionStatus.RUNNING)
        async with factory() as session:
            start_events = await session.scalar(
                select(func.count())
                .select_from(ExecutionEventRow)
                .where(
                    ExecutionEventRow.execution_attempt_id == attempt_id,
                    ExecutionEventRow.event_kind == "EXECUTION_STARTED",
                )
            )
            assert start_events == 1
        await repository.create_operation(
            operation_id=operation_id,
            attempt_id=attempt_id,
            kind=OperationKind.PROVIDER,
            fingerprint="a" * 64,
            resource_identity="provider:fake",
            call_ordinal=1,
        )
        with pytest.raises(AuthorityConflictError, match="identity fingerprint conflict"):
            await repository.create_operation(
                operation_id=operation_id,
                attempt_id=attempt_id,
                kind=OperationKind.PROVIDER,
                fingerprint="b" * 64,
                resource_identity="provider:fake",
                call_ordinal=1,
            )
        await repository.advance_operation(operation_id, ExecutionOperationPhase.SECURITY_ADMITTED)
        await repository.advance_operation(operation_id, ExecutionOperationPhase.DISPATCH_STARTED)
        await repository.advance_operation(
            operation_id,
            ExecutionOperationPhase.OUTCOME_UNKNOWN,
            ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME,
            refs={"budget": "conservatively-retained", "blind_retry": False},
        )
        await repository.store_output_ref(
            ref_id=f"output-{attempt_id}",
            attempt_id=attempt_id,
            kind="AgentOutputRef",
            content_hash="c" * 64,
            storage_ref="private://output",
        )
        completion_refs: dict[str, object] = {
            "execution_submission_ref": f"submission-{attempt_id}",
            "execution_submission_hash": "d" * 64,
            "execution_submission_storage_ref": "private://submission",
        }
        with pytest.raises(AuthorityConflictError, match="known outcome"):
            await repository.transition_attempt(
                attempt_id, "EXECUTION_COMPLETED", refs=completion_refs
            )
        failed = await asyncio.gather(
            repository.transition_attempt(
                attempt_id,
                "EXECUTION_FAILED",
                refs={"failure_class": "UNKNOWN_OUTCOME", "blind_retry": False},
            ),
            repository.transition_attempt(
                attempt_id,
                "EXECUTION_FAILED",
                refs={"failure_class": "UNKNOWN_OUTCOME", "blind_retry": False},
            ),
        )
        assert tuple(failed) == (ExecutionStatus.EXECUTION_FAILED,) * 2
        async with factory() as session:
            work_run = await session.get(WorkRunRow, run_id)
            operation = await session.get(ExecutionOperationRow, operation_id)
            assert work_run is not None and work_run.state_version == 2
            assert operation is not None and operation.current_phase == "OUTCOME_UNKNOWN"
        with pytest.raises(DBAPIError):
            async with factory() as session, session.begin():
                await session.execute(
                    text(
                        "UPDATE execution_events SET event_kind='MUTATED' "
                        "WHERE execution_attempt_id=:id"
                    ),
                    {"id": attempt_id},
                )

    try:
        run(scenario())
    finally:
        run(engine.dispose())


@pytest.mark.postgres
def test_restart_recovery_phase_semantics_and_private_state_integrity_gate() -> None:
    database_url = os.environ["AISCC_TEST_DATABASE_URL"]
    engine = create_engine(database_url)
    factory = create_session_factory(engine)
    unique = uuid4().hex
    run_id, attempt_id = f"recovery-run-{unique}", f"recovery-attempt-{unique}"
    operation_ids = tuple(f"recovery-operation-{index}-{unique}" for index in range(1, 5))

    async def scenario() -> None:
        now = datetime.now(UTC)
        async with factory() as session, session.begin():
            session.add(
                WorkRunRow(
                    work_run_id=run_id,
                    project_id="project",
                    task_contract_id="task",
                    task_contract_version="1",
                    workflow_state="READY",
                    state_version=1,
                    runtime_mode="OWNER_SELF_DOGFOOD",
                    created_at=now,
                    updated_at=now,
                )
            )
        repository = PostgresExecutionRepository(factory)
        await repository.create_attempt(
            attempt_id=attempt_id,
            work_run_id=run_id,
            profile_id="fake-openai-responses-v1",
            profile_version="1",
            registry_id="aiscc-p1-5-tools",
            registry_version="1",
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
        for ordinal, operation_id in enumerate(operation_ids, start=1):
            await repository.create_operation(
                operation_id=operation_id,
                attempt_id=attempt_id,
                kind=OperationKind.PROVIDER,
                fingerprint=f"{ordinal:x}" * 64,
                resource_identity="provider:fake",
                call_ordinal=ordinal,
            )
        await repository.advance_operation(
            operation_ids[1], ExecutionOperationPhase.SECURITY_ADMITTED
        )
        await repository.advance_operation(
            operation_ids[2], ExecutionOperationPhase.SECURITY_ADMITTED
        )
        await repository.advance_operation(
            operation_ids[2], ExecutionOperationPhase.DISPATCH_STARTED
        )

        restarted = PostgresExecutionRepository(factory)
        await restarted.advance_operation(
            operation_ids[0],
            ExecutionOperationPhase.OUTCOME_KNOWN,
            ExecutionOperationOutcome.DENIED_BEFORE_SIDE_EFFECT,
        )
        await restarted.advance_operation(
            operation_ids[1],
            ExecutionOperationPhase.OUTCOME_KNOWN,
            ExecutionOperationOutcome.CANCELLED,
        )
        await restarted.advance_operation(
            operation_ids[2],
            ExecutionOperationPhase.OUTCOME_UNKNOWN,
            ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME,
        )
        async with factory() as session, session.begin():
            await session.execute(
                text(
                    "INSERT INTO private_provider_protocol_states "
                    "(protocol_state_id, execution_attempt_id, operation_id, item_ordinal, "
                    "item_type, item_hash, call_id, encrypted_body_ref, body_bytes, "
                    "classification, byte_count, created_at) "
                    "VALUES (:state_id, :attempt_id, :operation_id, 1, 'reasoning', "
                    "'corrupt', NULL, 'private://corrupt', :body_bytes, "
                    "'PRIVATE_PROVIDER_PROTOCOL', 7, :created_at)"
                ),
                {
                    "state_id": f"corrupt-{unique}",
                    "attempt_id": attempt_id,
                    "operation_id": operation_ids[3],
                    "body_bytes": b'{"type":"reasoning"}',
                    "created_at": now,
                },
            )
        with pytest.raises(AuthorityConflictError, match="protocol-state integrity"):
            await restarted.advance_operation(
                operation_ids[3], ExecutionOperationPhase.SECURITY_ADMITTED
            )
        async with factory() as session:
            phases = tuple(
                await session.scalars(
                    select(ExecutionOperationRow.current_phase)
                    .where(ExecutionOperationRow.operation_id.in_(operation_ids))
                    .order_by(ExecutionOperationRow.call_ordinal)
                )
            )
            assert phases == (
                "OUTCOME_KNOWN",
                "OUTCOME_KNOWN",
                "OUTCOME_UNKNOWN",
                "PREPARED",
            )

    try:
        run(scenario())
    finally:
        run(engine.dispose())


@pytest.mark.postgres
def test_production_output_token_accounting_is_conservative_exact_and_restart_durable() -> None:
    database_url = os.environ["AISCC_TEST_DATABASE_URL"]
    engine = create_engine(database_url)
    factory = create_session_factory(engine)
    unique = uuid4().hex

    async def scenario() -> None:
        base_profile = load_provider_profile(
            Path("config/providers/provider-profiles.v1.toml"),
            "fake-openai-responses-v1",
        )
        profile = replace(base_profile, output_token_bound=256)
        registry = load_tool_registry(Path("config/providers/tool-registry.v1.toml"))
        definition = registry.tools["synthetic_lookup"]
        tool_identity = ":".join(
            (
                registry.registry_id,
                registry.version,
                definition.tool_id,
                definition.schema_version,
                definition.dispatcher_version,
            )
        )
        modes = frozenset({RuntimeMode.OWNER_SELF_DOGFOOD})
        provider_tool_authority = ProviderToolResourceAuthority(
            allowed_resource_identities=frozenset(
                {profile.provider_resource_identity, tool_identity}
            ),
            allowed_profile_ids=frozenset({profile.profile_id}),
            allowed_scenarios=frozenset({profile.public_scenario_identity}),
            allowed_modes=modes,
        )
        secret_use_authority = SecretUseAuthority(
            allowed_secret_refs=frozenset({profile.secret_ref}),
            allowed_profile_ids=frozenset({profile.profile_id}),
            allowed_scenarios=frozenset({profile.public_scenario_identity}),
            allowed_destinations=frozenset({profile.endpoint_ref}),
            allowed_modes=modes,
        )
        policy = SecurityPolicy(
            default_profiles(),
            provider_tool_policy=provider_tool_authority,
            secret_use_policy=secret_use_authority,
        )
        lease_authority = SecretResolutionLeaseAuthority(policy.verify_consumption_receipt)
        resolver = LeaseBoundSecretResolver(
            lease_authority,
            {profile.secret_ref: "AISCC_SYNTHETIC_LOCAL_ONLY"},
        )
        adapter = OpenAIResponsesAdapter()
        dispatcher = DurableSyntheticDispatcher()
        execution_refs = ExecutionReferenceAuthority()
        initial_inputs: dict[str, tuple[dict[str, Any], ...]] = {
            profile.public_scenario_identity: (
                {
                    "type": "message",
                    "role": "user",
                    "content": [{"type": "input_text", "text": "token accounting"}],
                },
            )
        }

        async def start_attempt(label: str) -> tuple[str, str, PostgresExecutionRepository]:
            run_id = f"token-accounting-run-{label}-{unique}"
            attempt_id = f"token-accounting-attempt-{label}-{unique}"
            now = datetime.now(UTC)
            async with factory() as session, session.begin():
                session.add(
                    WorkRunRow(
                        work_run_id=run_id,
                        project_id="project-p1-5-token-accounting",
                        task_contract_id="task-p1-5-token-accounting",
                        task_contract_version="1",
                        workflow_state=WorkflowState.READY.value,
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
                registry_id=registry.registry_id,
                registry_version=registry.version,
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
            return run_id, attempt_id, repository

        def build_service(repository: PostgresExecutionRepository) -> AgentExecutionService:
            return AgentExecutionService(
                policy=policy,
                adapter=adapter,
                secret_resolver=resolver,
                authority_reader=UnusedSyncAuthorityReader(),
                secret_lease_authority=lease_authority,
                repository=repository,
                provider_tool_authority=provider_tool_authority,
                secret_use_authority=secret_use_authority,
                profile=profile,
                tool_registry=registry,
                tool_dispatcher=dispatcher,
                execution_ref_authority=execution_refs,
                server_initial_inputs=initial_inputs,
            )

        def function_call(label: str) -> dict[str, Any]:
            return {
                "id": f"fc_token_{label}_{unique}",
                "type": "function_call",
                "status": "completed",
                "name": "synthetic_lookup",
                "call_id": f"call_token_{label}_{unique}",
                "arguments": '{"key":"aiscc-fixed-key"}',
            }

        with FakeResponsesServer() as server:
            missing_run, missing_attempt, missing_repository = await start_attempt("missing-full")
            missing_full = response_body("completed", [function_call("missing-full")])
            missing_full.pop("usage")
            missing_full_bytes = len(canonical_json_bytes(missing_full["output"]))
            assert (missing_full_bytes + 3) // 4 < 256
            server.enqueue(missing_full)
            missing_request_index = len(server.requests)
            missing_result = await build_service(missing_repository).execute(
                work_run_id=missing_run,
                execution_attempt_id=missing_attempt,
                principal="owner",
                scenario_id=profile.public_scenario_identity,
                max_provider_rounds=1,
            )
            assert missing_result.status == "CONTINUATION_REQUIRED"
            assert server.requests[missing_request_index]["max_output_tokens"] == 256
            missing_restart = PostgresExecutionRepository(factory)
            assert (
                await missing_restart.load_durable_counters(missing_attempt)
            ).output_tokens == 256
            before_missing_exhausted = len(server.requests)
            missing_exhausted = await build_service(missing_restart).execute(
                work_run_id=missing_run,
                execution_attempt_id=missing_attempt,
                principal="owner",
                scenario_id=profile.public_scenario_identity,
                max_provider_rounds=1,
            )
            assert missing_exhausted.status == "EXECUTION_FAILED"
            assert len(server.requests) == before_missing_exhausted

            run_id, attempt_id, repository = await start_attempt("cumulative")
            reported = response_body("completed", [function_call("reported")])
            reported["usage"]["output_tokens"] = 4
            reported["usage"]["total_tokens"] = 5
            server.enqueue(reported)
            cumulative_request_index = len(server.requests)
            first = await build_service(repository).execute(
                work_run_id=run_id,
                execution_attempt_id=attempt_id,
                principal="owner",
                scenario_id=profile.public_scenario_identity,
                max_provider_rounds=1,
            )
            assert first.status == "CONTINUATION_REQUIRED"
            assert server.requests[cumulative_request_index]["max_output_tokens"] == 256
            after_reported = await PostgresExecutionRepository(factory).load_durable_counters(
                attempt_id
            )
            assert after_reported.output_tokens == 4

            missing = response_body("completed", [function_call("missing")])
            missing.pop("usage")
            missing_output_bytes = len(canonical_json_bytes(missing["output"]))
            assert (missing_output_bytes + 3) // 4 < 252
            server.enqueue(missing)
            restarted_repository = PostgresExecutionRepository(factory)
            second = await build_service(restarted_repository).execute(
                work_run_id=run_id,
                execution_attempt_id=attempt_id,
                principal="owner",
                scenario_id=profile.public_scenario_identity,
                max_provider_rounds=1,
            )
            assert second.status == "CONTINUATION_REQUIRED"
            assert server.requests[cumulative_request_index + 1]["max_output_tokens"] == 252
            after_missing = await PostgresExecutionRepository(factory).load_durable_counters(
                attempt_id
            )
            assert after_missing.output_tokens == 256

            request_count = len(server.requests)
            exhausted = await build_service(PostgresExecutionRepository(factory)).execute(
                work_run_id=run_id,
                execution_attempt_id=attempt_id,
                principal="owner",
                scenario_id=profile.public_scenario_identity,
                max_provider_rounds=1,
            )
            assert exhausted.status == "EXECUTION_FAILED"
            assert len(server.requests) == request_count
            assert (
                await PostgresExecutionRepository(factory).load_durable_counters(attempt_id)
            ).output_tokens == 256

            malformed_values: tuple[tuple[str, object], ...] = (
                ("negative", -1),
                ("over-request-maximum", 257),
                ("non-integer", True),
            )
            for label, malformed_value in malformed_values:
                malformed_run, malformed_attempt, malformed_repository = await start_attempt(label)
                body = response_body("completed", [final_message(f"INVALID_USAGE_{label}")])
                body["usage"]["output_tokens"] = malformed_value
                server.enqueue(body)
                failed = await build_service(malformed_repository).execute(
                    work_run_id=malformed_run,
                    execution_attempt_id=malformed_attempt,
                    principal="owner",
                    scenario_id=profile.public_scenario_identity,
                    max_provider_rounds=1,
                )
                assert failed.status == "EXECUTION_FAILED"
                counters = await PostgresExecutionRepository(factory).load_durable_counters(
                    malformed_attempt
                )
                assert counters.output_tokens == 0
                async with factory() as session:
                    attempt = await session.get(ExecutionAttemptRow, malformed_attempt)
                    operation = await session.scalar(
                        select(ExecutionOperationRow).where(
                            ExecutionOperationRow.execution_attempt_id == malformed_attempt
                        )
                    )
                    failure = await session.scalar(
                        select(ExecutionEventRow).where(
                            ExecutionEventRow.execution_attempt_id == malformed_attempt,
                            ExecutionEventRow.event_kind == "EXECUTION_FAILED",
                        )
                    )
                    assert attempt is not None and attempt.status == "EXECUTION_FAILED"
                    assert operation is not None
                    assert operation.current_phase == ExecutionOperationPhase.OUTCOME_KNOWN.value
                    assert operation.outcome == ExecutionOperationOutcome.PROVIDER_COMPLETED.value
                    assert failure is not None
                    assert failure.refs["failure_class"] == "PROVIDER_PROTOCOL_ACCOUNTING"
                    assert failure.refs["reason"] == "INVALID_PROVIDER_OUTPUT_TOKEN_USAGE"

    try:
        run(scenario())
    finally:
        run(engine.dispose())


@pytest.mark.postgres
@pytest.mark.parametrize(
    "runtime_mode",
    [RuntimeMode.OWNER_SELF_DOGFOOD, RuntimeMode.PUBLIC_BOUNDED_LIVE],
)
def test_durable_agent_service_two_round_restart_and_public_live_positive_execution(
    runtime_mode: RuntimeMode,
) -> None:
    database_url = os.environ["AISCC_TEST_DATABASE_URL"]
    engine = create_engine(database_url)
    factory = create_session_factory(engine)
    unique = uuid4().hex
    run_id = f"durable-agent-run-{unique}"
    attempt_id = f"durable-agent-attempt-{unique}"

    async def scenario() -> None:
        system_authority = P1_4GuardAuthority()
        transition_repository = PostgresTransitionRepository(
            factory,
            TransitionEvaluator(system_authority),
        )
        kernel = WorkflowKernel(transition_repository)

        def transition_request(
            source: WorkflowState | None,
            version: int,
            target: WorkflowState,
        ) -> TransitionRequest:
            return TransitionRequest(
                transition_request_id=f"request-{target.value}-{uuid4().hex}",
                project_id=(
                    "repository:p1-5-synthetic@1"
                    if runtime_mode is RuntimeMode.PUBLIC_BOUNDED_LIVE
                    else "project-p1-5-durable"
                ),
                task_contract_id="task-p1-5-durable",
                task_contract_version="1",
                work_run_id=run_id,
                observed_state=source,
                observed_state_version=version,
                target_state=target,
                requester_identity="aiscc-system",
                requester_type=RequesterType.SYSTEM,
                runtime_mode=runtime_mode,
            )

        def system_facts(request: TransitionRequest) -> list[TrustedGuardFact]:
            required = TRANSITION_MATRIX[(request.observed_state, request.target_state)]
            return [
                system_authority.issue(
                    guard_id=guard,
                    satisfied=True,
                    reason="P1_5_DURABLE_INTEGRATION_PRECONDITION",
                    authority_ref=f"integration:{guard.value}",
                    request=request,
                )
                for guard in sorted(required, key=str)
                if guard is not GuardId.G_EXECUTION_STARTED
            ]

        create = transition_request(None, 0, WorkflowState.READY)
        ready = await kernel.request_transition(create, tuple(system_facts(create)))
        assert ready.outcome is DecisionOutcome.ADMITTED

        execution_repository = PostgresExecutionRepository(factory)
        await execution_repository.create_attempt(
            attempt_id=attempt_id,
            work_run_id=run_id,
            profile_id="fake-openai-responses-v1",
            profile_version="1",
            registry_id="aiscc-p1-5-tools",
            registry_version="1",
        )
        execution_refs = ExecutionReferenceAuthority()
        start_ref = execution_refs.register_start(
            ExecutionAttemptRef(
                execution_attempt_id=attempt_id,
                work_run_id=run_id,
                task_contract_id="task-p1-5-durable",
                task_contract_version="1",
                state=WorkflowState.READY,
                state_version=1,
                execution_version=1,
                status=ExecutionStatus.NOT_STARTED,
                issuer_ref=execution_refs.issuer_ref,
                runtime_mode=runtime_mode,
            )
        )
        start = transition_request(WorkflowState.READY, 1, WorkflowState.RUNNING)
        start_facts = system_facts(start)
        start_facts.append(
            system_authority.issue_from_execution_ref(
                guard_id=GuardId.G_EXECUTION_STARTED,
                execution_ref=start_ref,
                verifier=execution_refs,
                request=start,
            )
        )
        running = await kernel.request_transition(start, tuple(start_facts))
        assert running.outcome is DecisionOutcome.ADMITTED
        assert (
            await execution_repository.transition_attempt(attempt_id, "EXECUTION_STARTED")
            is ExecutionStatus.RUNNING
        )

        profile = load_provider_profile(
            Path("config/providers/provider-profiles.v1.toml"),
            "fake-openai-responses-v1",
        )
        registry = load_tool_registry(Path("config/providers/tool-registry.v1.toml"))
        definition = registry.tools["synthetic_lookup"]
        tool_identity = ":".join(
            (
                registry.registry_id,
                registry.version,
                definition.tool_id,
                definition.schema_version,
                definition.dispatcher_version,
            )
        )
        modes = frozenset({RuntimeMode.OWNER_SELF_DOGFOOD, RuntimeMode.PUBLIC_BOUNDED_LIVE})
        provider_tool_authority = ProviderToolResourceAuthority(
            allowed_resource_identities=frozenset(
                {profile.provider_resource_identity, tool_identity}
            ),
            allowed_profile_ids=frozenset({profile.profile_id}),
            allowed_scenarios=frozenset({"p1-5-fixed-synthetic"}),
            allowed_modes=modes,
        )
        secret_use_authority = SecretUseAuthority(
            allowed_secret_refs=frozenset({profile.secret_ref}),
            allowed_profile_ids=frozenset({profile.profile_id}),
            allowed_scenarios=frozenset({"p1-5-fixed-synthetic"}),
            allowed_destinations=frozenset({profile.endpoint_ref}),
            allowed_modes=modes,
        )
        policy = SecurityPolicy(
            default_profiles(),
            provider_tool_policy=provider_tool_authority,
            secret_use_policy=secret_use_authority,
        )
        lease_authority = SecretResolutionLeaseAuthority(policy.verify_consumption_receipt)
        resolver = LeaseBoundSecretResolver(
            lease_authority,
            {profile.secret_ref: "AISCC_SYNTHETIC_LOCAL_ONLY"},
        )
        adapter = OpenAIResponsesAdapter()
        dispatcher = DurableSyntheticDispatcher()
        initial_inputs: dict[str, tuple[dict[str, Any], ...]] = {
            "p1-5-fixed-synthetic": (
                {
                    "type": "message",
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": "Execute the fixed synthetic lookup.",
                        }
                    ],
                },
            )
        }

        def build_service(repository: PostgresExecutionRepository) -> AgentExecutionService:
            return AgentExecutionService(
                policy=policy,
                adapter=adapter,
                secret_resolver=resolver,
                authority_reader=UnusedSyncAuthorityReader(),
                secret_lease_authority=lease_authority,
                repository=repository,
                provider_tool_authority=provider_tool_authority,
                secret_use_authority=secret_use_authority,
                profile=profile,
                tool_registry=registry,
                tool_dispatcher=dispatcher,
                execution_ref_authority=execution_refs,
                server_initial_inputs=initial_inputs,
            )

        function_call = {
            "id": "fc_durable",
            "type": "function_call",
            "status": "completed",
            "name": "synthetic_lookup",
            "call_id": "call_durable_exact",
            "arguments": '{"key":"aiscc-fixed-key"}',
        }
        with FakeResponsesServer() as server:
            server.enqueue(response_body("completed", [function_call]))
            server.enqueue(response_body("completed", [final_message("AISCC_DURABLE_FINAL")]))
            first = await build_service(execution_repository).execute(
                work_run_id=run_id,
                execution_attempt_id=attempt_id,
                principal=(
                    "public-user" if runtime_mode is RuntimeMode.PUBLIC_BOUNDED_LIVE else "owner"
                ),
                scenario_id="p1-5-fixed-synthetic",
                max_provider_rounds=1,
            )
            assert first.status == "CONTINUATION_REQUIRED"
            async with factory() as session:
                stored_rows = tuple(
                    await session.scalars(
                        select(PrivateProviderProtocolStateRow)
                        .where(PrivateProviderProtocolStateRow.execution_attempt_id == attempt_id)
                        .order_by(PrivateProviderProtocolStateRow.item_ordinal)
                    )
                )
            original = stored_rows[1]
            original_values = {
                "protocol_state_id": original.protocol_state_id,
                "execution_attempt_id": original.execution_attempt_id,
                "operation_id": original.operation_id,
                "item_ordinal": original.item_ordinal,
                "item_type": original.item_type,
                "item_hash": original.item_hash,
                "call_id": original.call_id,
                "encrypted_body_ref": original.encrypted_body_ref,
                "body_bytes": original.body_bytes,
                "classification": original.classification,
                "byte_count": original.byte_count,
                "created_at": original.created_at,
            }

            async def corrupt_private_state(kind: str) -> None:
                async with factory() as session, session.begin():
                    await session.execute(
                        text(
                            "ALTER TABLE private_provider_protocol_states "
                            "DISABLE TRIGGER private_provider_protocol_states_append_only"
                        )
                    )
                    if kind == "missing":
                        await session.execute(
                            text(
                                "DELETE FROM private_provider_protocol_states "
                                "WHERE protocol_state_id=:id"
                            ),
                            {"id": original.protocol_state_id},
                        )
                    elif kind == "body":
                        await session.execute(
                            text(
                                "UPDATE private_provider_protocol_states SET body_bytes=:value "
                                "WHERE protocol_state_id=:id"
                            ),
                            {"id": original.protocol_state_id, "value": b"{}"},
                        )
                    elif kind == "order":
                        await session.execute(
                            text(
                                "UPDATE private_provider_protocol_states SET item_ordinal=99 "
                                "WHERE protocol_state_id=:id"
                            ),
                            {"id": original.protocol_state_id},
                        )
                    else:
                        await session.execute(
                            text(
                                "UPDATE private_provider_protocol_states SET call_id='wrong' "
                                "WHERE protocol_state_id=:id"
                            ),
                            {"id": original.protocol_state_id},
                        )
                    await session.execute(
                        text(
                            "ALTER TABLE private_provider_protocol_states "
                            "ENABLE TRIGGER private_provider_protocol_states_append_only"
                        )
                    )

            async def restore_private_state() -> None:
                async with factory() as session, session.begin():
                    await session.execute(
                        text(
                            "ALTER TABLE private_provider_protocol_states "
                            "DISABLE TRIGGER private_provider_protocol_states_append_only"
                        )
                    )
                    await session.execute(
                        text(
                            "DELETE FROM private_provider_protocol_states "
                            "WHERE protocol_state_id=:id"
                        ),
                        {"id": original.protocol_state_id},
                    )
                    await session.execute(
                        text(
                            "INSERT INTO private_provider_protocol_states "
                            "(protocol_state_id, execution_attempt_id, operation_id, "
                            "item_ordinal, item_type, item_hash, call_id, encrypted_body_ref, "
                            "body_bytes, classification, byte_count, created_at) VALUES "
                            "(:protocol_state_id, :execution_attempt_id, :operation_id, "
                            ":item_ordinal, :item_type, :item_hash, :call_id, "
                            ":encrypted_body_ref, :body_bytes, :classification, :byte_count, "
                            ":created_at)"
                        ),
                        original_values,
                    )
                    await session.execute(
                        text(
                            "ALTER TABLE private_provider_protocol_states "
                            "ENABLE TRIGGER private_provider_protocol_states_append_only"
                        )
                    )

            for corruption in ("missing", "body", "order", "call_id"):
                await corrupt_private_state(corruption)
                before = adapter.invocation_count
                with pytest.raises(AuthorityConflictError):
                    await build_service(PostgresExecutionRepository(factory)).execute(
                        work_run_id=run_id,
                        execution_attempt_id=attempt_id,
                        principal=(
                            "public-user"
                            if runtime_mode is RuntimeMode.PUBLIC_BOUNDED_LIVE
                            else "owner"
                        ),
                        scenario_id="p1-5-fixed-synthetic",
                    )
                assert adapter.invocation_count == before
                await restore_private_state()
            restarted_repository = PostgresExecutionRepository(factory)
            second = await build_service(restarted_repository).execute(
                work_run_id=run_id,
                execution_attempt_id=attempt_id,
                principal=(
                    "public-user" if runtime_mode is RuntimeMode.PUBLIC_BOUNDED_LIVE else "owner"
                ),
                scenario_id="p1-5-fixed-synthetic",
            )
            assert second.status == "EXECUTOR_COMPLETED"
            assert second.submission is not None
            assert len(server.requests) == 2
            assert "previous_response_id" not in server.requests[1]
            continuation = server.requests[1]["input"]
            assert any(item.get("type") == "function_call" for item in continuation)
            assert any(item.get("type") == "function_call_output" for item in continuation)

        assert adapter.invocation_count == 2
        assert dispatcher.calls == 1
        assert resolver.invocation_count == 2
        counters = await execution_repository.load_durable_counters(attempt_id)
        assert (
            counters.provider_calls,
            counters.agent_rounds,
            counters.tool_calls,
            counters.provider_retries,
            counters.output_tokens,
            counters.budget_units,
        ) == (2, 2, 1, 0, 2, 3)
        assert counters.output_bytes > 0
        assert counters.started_at is not None and counters.deadline_at is not None
        assert (
            await PostgresExecutionRepository(factory).load_durable_counters(attempt_id) == counters
        )
        operations = await execution_repository.load_operations(attempt_id)
        assert tuple(operation.kind for operation in operations) == (
            OperationKind.PROVIDER,
            OperationKind.TOOL,
            OperationKind.PROVIDER,
        )
        assert all(
            operation.phase is ExecutionOperationPhase.OUTCOME_KNOWN for operation in operations
        )
        private_items = await execution_repository.load_private_protocol_items(attempt_id)
        assert [item["type"] for item in private_items] == [
            "message",
            "function_call",
            "function_call_output",
            "message",
        ]
        async with factory() as session:
            work_run = await session.get(WorkRunRow, run_id)
            attempt = await session.get(ExecutionAttemptRow, attempt_id)
            assert work_run is not None
            assert work_run.workflow_state == "RUNNING" and work_run.state_version == 2
            assert attempt is not None and attempt.status == "EXECUTOR_COMPLETED"

    try:
        run(scenario())
    finally:
        run(engine.dispose())


@pytest.mark.postgres
@pytest.mark.parametrize(
    "bound",
    [
        "PROVIDER_CALL_LIMIT",
        "AGENT_ROUND_LIMIT",
        "TOOL_CALL_LIMIT",
        "BUDGET_LIMIT",
        "OUTPUT_BYTE_LIMIT",
        "OUTPUT_TOKEN_LIMIT",
        "WALL_TIME_LIMIT",
    ],
)
def test_production_execute_bounds_are_restart_durable_and_fail_before_next_side_effect(
    bound: str,
) -> None:
    database_url = os.environ["AISCC_TEST_DATABASE_URL"]
    engine = create_engine(database_url)
    factory = create_session_factory(engine)
    unique = uuid4().hex
    run_id = f"durable-bound-run-{unique}"
    attempt_id = f"durable-bound-attempt-{unique}"
    first_call = {
        "id": f"fc_bound_1_{unique}",
        "type": "function_call",
        "status": "completed",
        "caller": None,
        "name": "synthetic_lookup",
        "namespace": None,
        "call_id": f"call_bound_1_{unique}",
        "arguments": '{"key":"aiscc-fixed-key"}',
    }
    second_call = {
        "id": f"fc_bound_2_{unique}",
        "type": "function_call",
        "status": "completed",
        "caller": None,
        "name": "synthetic_lookup",
        "namespace": None,
        "call_id": f"call_bound_2_{unique}",
        "arguments": '{"key":"aiscc-fixed-key"}',
    }
    first_output_bytes = len(canonical_json_bytes([first_call]))

    async def scenario() -> None:
        now = datetime.now(UTC)
        async with factory() as session, session.begin():
            session.add(
                WorkRunRow(
                    work_run_id=run_id,
                    project_id="project-p1-5-durable-bounds",
                    task_contract_id="task-p1-5-durable-bounds",
                    task_contract_version="1",
                    workflow_state=WorkflowState.READY.value,
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
            profile_id="fake-openai-responses-v1",
            profile_version="1",
            registry_id="aiscc-p1-5-tools",
            registry_version="1",
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

        base_profile = load_provider_profile(
            Path("config/providers/provider-profiles.v1.toml"),
            "fake-openai-responses-v1",
        )
        profile: ProviderProfile
        if bound == "PROVIDER_CALL_LIMIT":
            profile = replace(base_profile, provider_call_maximum=1)
        elif bound == "AGENT_ROUND_LIMIT":
            profile = replace(base_profile, agent_round_trip_maximum=1)
        elif bound == "TOOL_CALL_LIMIT":
            profile = replace(base_profile, tool_call_maximum=1)
        elif bound == "BUDGET_LIMIT":
            profile = replace(base_profile, budget_unit_maximum=2)
        elif bound == "OUTPUT_BYTE_LIMIT":
            profile = replace(base_profile, output_byte_bound=first_output_bytes)
        elif bound == "OUTPUT_TOKEN_LIMIT":
            profile = replace(base_profile, output_token_bound=1)
        elif bound == "WALL_TIME_LIMIT":
            profile = replace(base_profile, total_timeout_seconds=1)
        else:
            raise AssertionError(f"unhandled bound: {bound}")
        registry = load_tool_registry(Path("config/providers/tool-registry.v1.toml"))
        definition = registry.tools["synthetic_lookup"]
        tool_identity = ":".join(
            (
                registry.registry_id,
                registry.version,
                definition.tool_id,
                definition.schema_version,
                definition.dispatcher_version,
            )
        )
        modes = frozenset({RuntimeMode.OWNER_SELF_DOGFOOD})
        provider_tool_authority = ProviderToolResourceAuthority(
            allowed_resource_identities=frozenset(
                {profile.provider_resource_identity, tool_identity}
            ),
            allowed_profile_ids=frozenset({profile.profile_id}),
            allowed_scenarios=frozenset({"p1-5-fixed-synthetic"}),
            allowed_modes=modes,
        )
        secret_use_authority = SecretUseAuthority(
            allowed_secret_refs=frozenset({profile.secret_ref}),
            allowed_profile_ids=frozenset({profile.profile_id}),
            allowed_scenarios=frozenset({"p1-5-fixed-synthetic"}),
            allowed_destinations=frozenset({profile.endpoint_ref}),
            allowed_modes=modes,
        )
        policy = SecurityPolicy(
            default_profiles(),
            provider_tool_policy=provider_tool_authority,
            secret_use_policy=secret_use_authority,
        )
        lease_authority = SecretResolutionLeaseAuthority(policy.verify_consumption_receipt)
        resolver = LeaseBoundSecretResolver(
            lease_authority,
            {profile.secret_ref: "AISCC_SYNTHETIC_LOCAL_ONLY"},
        )
        adapter = OpenAIResponsesAdapter()
        dispatcher = DurableSyntheticDispatcher()
        execution_refs = ExecutionReferenceAuthority()
        initial_inputs: dict[str, tuple[dict[str, Any], ...]] = {
            "p1-5-fixed-synthetic": (
                {
                    "type": "message",
                    "role": "user",
                    "content": [{"type": "input_text", "text": "bounded loop"}],
                },
            )
        }

        def build_service(
            execution_repository: PostgresExecutionRepository,
            clock: datetime,
        ) -> AgentExecutionService:
            return AgentExecutionService(
                policy=policy,
                adapter=adapter,
                secret_resolver=resolver,
                authority_reader=UnusedSyncAuthorityReader(),
                secret_lease_authority=lease_authority,
                repository=execution_repository,
                provider_tool_authority=provider_tool_authority,
                secret_use_authority=secret_use_authority,
                profile=profile,
                tool_registry=registry,
                tool_dispatcher=dispatcher,
                execution_ref_authority=execution_refs,
                server_initial_inputs=initial_inputs,
                durable_time_source=lambda: clock,
            )

        with FakeResponsesServer() as server:
            server.enqueue(response_body("completed", [first_call]))
            first = await build_service(repository, now).execute(
                work_run_id=run_id,
                execution_attempt_id=attempt_id,
                principal="owner",
                scenario_id="p1-5-fixed-synthetic",
                max_provider_rounds=1,
            )
            assert first.status == "CONTINUATION_REQUIRED"
            at_maximum = await repository.load_durable_counters(attempt_id)
            restarted_repository = PostgresExecutionRepository(factory)
            assert await restarted_repository.load_durable_counters(attempt_id) == at_maximum
            before = (
                adapter.invocation_count,
                resolver.invocation_count,
                dispatcher.calls,
                len(server.requests),
            )
            if bound == "TOOL_CALL_LIMIT":
                server.enqueue(response_body("completed", [second_call]))
            advanced_clock = now + timedelta(seconds=2) if bound == "WALL_TIME_LIMIT" else now
            failed = await build_service(restarted_repository, advanced_clock).execute(
                work_run_id=run_id,
                execution_attempt_id=attempt_id,
                principal="owner",
                scenario_id="p1-5-fixed-synthetic",
                max_provider_rounds=1,
            )
            assert failed.status == "EXECUTION_FAILED"
            after = (
                adapter.invocation_count,
                resolver.invocation_count,
                dispatcher.calls,
                len(server.requests),
            )
        if bound == "TOOL_CALL_LIMIT":
            assert after == (before[0] + 1, before[1] + 1, before[2], before[3] + 1)
        else:
            assert after == before
        durable = await restarted_repository.load_durable_counters(attempt_id)
        if bound == "TOOL_CALL_LIMIT":
            assert durable.tool_calls == 1
            assert durable.provider_calls == 2
        else:
            assert durable == at_maximum
        async with factory() as session:
            attempt = await session.get(ExecutionAttemptRow, attempt_id)
            failure_events = tuple(
                await session.scalars(
                    select(ExecutionEventRow).where(
                        ExecutionEventRow.execution_attempt_id == attempt_id,
                        ExecutionEventRow.event_kind == "EXECUTION_FAILED",
                    )
                )
            )
            assert attempt is not None and attempt.status == "EXECUTION_FAILED"
            assert len(failure_events) == 1
            assert failure_events[0].refs["failure_class"] == "LIMIT_EXHAUSTED"
            assert failure_events[0].refs["reason"] == bound

    try:
        run(scenario())
    finally:
        run(engine.dispose())


@pytest.mark.postgres
@pytest.mark.parametrize(
    "denial_case",
    [
        "WRONG_REPOSITORY_IDENTITY",
        "WRONG_REPOSITORY_VERSION",
        "WRONG_SCENARIO_VERSION",
        "WRONG_PROFILE_VERSION",
        "WRONG_MODEL",
        "WRONG_SECRET",
        "WRONG_STATE_VERSION",
    ],
)
def test_public_fixed_context_and_authority_denials_have_zero_side_effect(
    denial_case: str,
) -> None:
    database_url = os.environ["AISCC_TEST_DATABASE_URL"]
    engine = create_engine(database_url)
    factory = create_session_factory(engine)
    unique = uuid4().hex
    run_id = f"public-context-run-{unique}"
    attempt_id = f"public-context-attempt-{unique}"

    async def scenario() -> None:
        base_profile = load_provider_profile(
            Path("config/providers/provider-profiles.v1.toml"),
            "fake-openai-responses-v1",
        )
        profile = base_profile
        project_id = base_profile.public_repository_resource_identity
        scenario_id = base_profile.public_scenario_identity
        attempt_profile_version = base_profile.version
        if denial_case == "WRONG_REPOSITORY_IDENTITY":
            project_id = "repository:caller-selected@1"
        elif denial_case == "WRONG_REPOSITORY_VERSION":
            project_id = "repository:p1-5-synthetic@2"
        elif denial_case == "WRONG_SCENARIO_VERSION":
            scenario_id = "p1-5-fixed-synthetic@2"
        elif denial_case == "WRONG_PROFILE_VERSION":
            profile = replace(base_profile, version="2")
        elif denial_case == "WRONG_MODEL":
            profile = replace(base_profile, model_ref="caller-selected-model")
        elif denial_case == "WRONG_SECRET":
            profile = replace(base_profile, secret_ref="secret-ref:caller-selected")

        now = datetime.now(UTC)
        async with factory() as session, session.begin():
            session.add(
                WorkRunRow(
                    work_run_id=run_id,
                    project_id=project_id,
                    task_contract_id="task-p1-5-public-context",
                    task_contract_version="1",
                    workflow_state=WorkflowState.READY.value,
                    state_version=1,
                    runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE.value,
                    created_at=now,
                    updated_at=now,
                )
            )
        repository = PostgresExecutionRepository(factory)
        await repository.create_attempt(
            attempt_id=attempt_id,
            work_run_id=run_id,
            profile_id=base_profile.profile_id,
            profile_version=attempt_profile_version,
            registry_id="aiscc-p1-5-tools",
            registry_version="1",
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
        if denial_case == "WRONG_STATE_VERSION":
            async with factory() as session, session.begin():
                await session.execute(
                    text(
                        "UPDATE work_runs SET workflow_state='BLOCKED', state_version=3 "
                        "WHERE work_run_id=:id"
                    ),
                    {"id": run_id},
                )

        registry = load_tool_registry(Path("config/providers/tool-registry.v1.toml"))
        definition = registry.tools["synthetic_lookup"]
        tool_identity = ":".join(
            (
                registry.registry_id,
                registry.version,
                definition.tool_id,
                definition.schema_version,
                definition.dispatcher_version,
            )
        )
        modes = frozenset({RuntimeMode.PUBLIC_BOUNDED_LIVE})
        provider_tool_authority = ProviderToolResourceAuthority(
            allowed_resource_identities=frozenset(
                {base_profile.provider_resource_identity, tool_identity}
            ),
            allowed_profile_ids=frozenset({base_profile.profile_id}),
            allowed_scenarios=frozenset({base_profile.public_scenario_identity}),
            allowed_modes=modes,
        )
        secret_use_authority = SecretUseAuthority(
            allowed_secret_refs=frozenset({base_profile.secret_ref}),
            allowed_profile_ids=frozenset({base_profile.profile_id}),
            allowed_scenarios=frozenset({base_profile.public_scenario_identity}),
            allowed_destinations=frozenset({base_profile.endpoint_ref}),
            allowed_modes=modes,
        )
        policy = SecurityPolicy(
            default_profiles(),
            provider_tool_policy=provider_tool_authority,
            secret_use_policy=secret_use_authority,
        )
        lease_authority = SecretResolutionLeaseAuthority(policy.verify_consumption_receipt)
        resolver = LeaseBoundSecretResolver(
            lease_authority,
            {base_profile.secret_ref: "AISCC_SYNTHETIC_LOCAL_ONLY"},
        )
        adapter = OpenAIResponsesAdapter()
        dispatcher = DurableSyntheticDispatcher()
        service = AgentExecutionService(
            policy=policy,
            adapter=adapter,
            secret_resolver=resolver,
            authority_reader=UnusedSyncAuthorityReader(),
            secret_lease_authority=lease_authority,
            repository=repository,
            provider_tool_authority=provider_tool_authority,
            secret_use_authority=secret_use_authority,
            profile=profile,
            tool_registry=registry,
            tool_dispatcher=dispatcher,
            execution_ref_authority=ExecutionReferenceAuthority(),
            server_initial_inputs={
                base_profile.public_scenario_identity: (
                    {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": "fixed context"}],
                    },
                )
            },
        )
        result = await service.execute(
            work_run_id=run_id,
            execution_attempt_id=attempt_id,
            principal="public-user",
            scenario_id=scenario_id,
            max_provider_rounds=1,
        )
        assert result.status == "EXECUTION_FAILED"
        assert (adapter.invocation_count, resolver.invocation_count, dispatcher.calls) == (0, 0, 0)
        async with factory() as session:
            attempt = await session.get(ExecutionAttemptRow, attempt_id)
            dispatch_events = await session.scalar(
                select(func.count())
                .select_from(OperationEventRow)
                .join(ExecutionOperationRow)
                .where(
                    ExecutionOperationRow.execution_attempt_id == attempt_id,
                    OperationEventRow.target_phase
                    == ExecutionOperationPhase.DISPATCH_STARTED.value,
                )
            )
            assert attempt is not None and attempt.status == "EXECUTION_FAILED"
            assert dispatch_events == 0

    try:
        run(scenario())
    finally:
        run(engine.dispose())


@pytest.mark.postgres
def test_provider_returned_tool_is_denied_when_accepted_transition_leaves_running() -> None:
    database_url = os.environ["AISCC_TEST_DATABASE_URL"]
    engine = create_engine(database_url)
    factory = create_session_factory(engine)
    unique = uuid4().hex
    run_id = f"workflow-left-running-run-{unique}"
    attempt_id = f"workflow-left-running-attempt-{unique}"
    project_id = "project-p1-5-workflow-left-running"

    async def scenario() -> None:
        guard_authority = P1_4GuardAuthority()
        kernel = WorkflowKernel(
            PostgresTransitionRepository(factory, TransitionEvaluator(guard_authority))
        )

        def request(
            source: WorkflowState | None,
            version: int,
            target: WorkflowState,
            *,
            blocker_claim: P1_4BlockerClaimV1 | None = None,
        ) -> TransitionRequest:
            return TransitionRequest(
                transition_request_id=f"workflow-left-{target.value}-{uuid4().hex}",
                project_id=project_id,
                task_contract_id="task-p1-5-workflow-left-running",
                task_contract_version="1",
                work_run_id=run_id,
                observed_state=source,
                observed_state_version=version,
                target_state=target,
                requester_identity="aiscc-system",
                requester_type=RequesterType.SYSTEM,
                runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
                blocker_claim=blocker_claim,
            )

        def facts(
            authority: P1_4GuardAuthority,
            transition: TransitionRequest,
            *,
            skip_execution_started: bool = False,
        ) -> list[TrustedGuardFact]:
            return [
                authority.issue(
                    guard_id=guard,
                    satisfied=True,
                    reason="P1_5_WORKFLOW_FRESHNESS_CONCURRENCY_PROOF",
                    authority_ref=f"integration:{guard.value}",
                    request=transition,
                )
                for guard in sorted(
                    TRANSITION_MATRIX[(transition.observed_state, transition.target_state)],
                    key=str,
                )
                if not (skip_execution_started and guard is GuardId.G_EXECUTION_STARTED)
            ]

        create = request(None, 0, WorkflowState.READY)
        assert (
            await kernel.request_transition(create, tuple(facts(guard_authority, create)))
        ).outcome is DecisionOutcome.ADMITTED
        repository = PostgresExecutionRepository(factory)
        await repository.create_attempt(
            attempt_id=attempt_id,
            work_run_id=run_id,
            profile_id="fake-openai-responses-v1",
            profile_version="1",
            registry_id="aiscc-p1-5-tools",
            registry_version="1",
        )
        execution_refs = ExecutionReferenceAuthority()
        start_ref = execution_refs.register_start(
            ExecutionAttemptRef(
                execution_attempt_id=attempt_id,
                work_run_id=run_id,
                task_contract_id="task-p1-5-workflow-left-running",
                task_contract_version="1",
                state=WorkflowState.READY,
                state_version=1,
                execution_version=1,
                status=ExecutionStatus.NOT_STARTED,
                issuer_ref=execution_refs.issuer_ref,
                runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            )
        )
        start = request(WorkflowState.READY, 1, WorkflowState.RUNNING)
        start_facts = facts(guard_authority, start, skip_execution_started=True)
        start_facts.append(
            guard_authority.issue_from_execution_ref(
                guard_id=GuardId.G_EXECUTION_STARTED,
                execution_ref=start_ref,
                verifier=execution_refs,
                request=start,
            )
        )
        assert (
            await kernel.request_transition(start, tuple(start_facts))
        ).outcome is DecisionOutcome.ADMITTED
        await repository.transition_attempt(attempt_id, "EXECUTION_STARTED")
        assert execution_refs.verify(start_ref, start, GuardId.G_EXECUTION_STARTED)

        denial_class = "WORKFLOW_LEFT_RUNNING"
        denial_reason = "WORKFLOW_LEFT_RUNNING_AFTER_PROVIDER_DISPATCH"
        blocker_source_contract_ref = (
            "p1-5-execution-source-contract:v1:workflow-currentness-denial"
        )
        blocker_source_contract_fingerprint = canonical_sha256(
            {
                "blocker_kind": BlockerKindV1.EXECUTION.value,
                "denial_class": denial_class,
                "denial_reason": denial_reason,
                "reason_code": BlockerReasonCodeV1.EXECUTION_BLOCKER.value,
                "source_authority": execution_refs.issuer_ref,
                "verification": "ExecutionReferenceAuthority.verify",
            }
        )
        blocker_source_ref = f"p1-5-execution-start-ref:v1:{attempt_id}"
        blocker_source_fingerprint = canonical_sha256(
            {
                "execution_attempt_id": start_ref.execution_attempt_id,
                "execution_version": start_ref.execution_version,
                "issuer_ref": start_ref.issuer_ref,
                "state": start_ref.state.value,
                "state_version": start_ref.state_version,
                "status": start_ref.status.value,
                "task_contract_id": start_ref.task_contract_id,
                "task_contract_version": start_ref.task_contract_version,
                "work_run_id": start_ref.work_run_id,
            }
        )

        profile = load_provider_profile(
            Path("config/providers/provider-profiles.v1.toml"),
            "fake-openai-responses-v1",
        )
        registry = load_tool_registry(Path("config/providers/tool-registry.v1.toml"))
        definition = registry.tools["synthetic_lookup"]
        tool_identity = ":".join(
            (
                registry.registry_id,
                registry.version,
                definition.tool_id,
                definition.schema_version,
                definition.dispatcher_version,
            )
        )
        modes = frozenset({RuntimeMode.OWNER_SELF_DOGFOOD})
        provider_tool_authority = ProviderToolResourceAuthority(
            allowed_resource_identities=frozenset(
                {profile.provider_resource_identity, tool_identity}
            ),
            allowed_profile_ids=frozenset({profile.profile_id}),
            allowed_scenarios=frozenset({profile.public_scenario_identity}),
            allowed_modes=modes,
        )
        secret_use_authority = SecretUseAuthority(
            allowed_secret_refs=frozenset({profile.secret_ref}),
            allowed_profile_ids=frozenset({profile.profile_id}),
            allowed_scenarios=frozenset({profile.public_scenario_identity}),
            allowed_destinations=frozenset({profile.endpoint_ref}),
            allowed_modes=modes,
        )
        policy = SecurityPolicy(
            default_profiles(),
            provider_tool_policy=provider_tool_authority,
            secret_use_policy=secret_use_authority,
        )
        lease_authority = SecretResolutionLeaseAuthority(policy.verify_consumption_receipt)
        resolver = LeaseBoundSecretResolver(
            lease_authority,
            {profile.secret_ref: "AISCC_SYNTHETIC_LOCAL_ONLY"},
        )
        adapter = OpenAIResponsesAdapter()
        dispatcher = DurableSyntheticDispatcher()
        callback_errors: list[BaseException] = []

        def leave_running() -> None:
            async def transition() -> None:
                callback_engine = create_engine(database_url)
                callback_factory = create_session_factory(callback_engine)
                callback_authority = P1_4GuardAuthority()
                callback_kernel = WorkflowKernel(
                    PostgresTransitionRepository(
                        callback_factory,
                        TransitionEvaluator(callback_authority),
                    )
                )
                blocked = request(
                    WorkflowState.RUNNING,
                    2,
                    WorkflowState.BLOCKED,
                    blocker_claim=P1_4BlockerClaimV1(
                        blocker_id=f"workflow-left-running-{attempt_id}",
                        blocker_kind=BlockerKindV1.EXECUTION,
                        reason_code=BlockerReasonCodeV1.EXECUTION_BLOCKER,
                        resolution_source_contract_ref=blocker_source_contract_ref,
                        resolution_source_contract_fingerprint=(
                            blocker_source_contract_fingerprint
                        ),
                        ordered_source_authority_refs=(blocker_source_ref,),
                        ordered_source_authority_fingerprints=(
                            blocker_source_fingerprint,
                        ),
                    ),
                )
                decision = await callback_kernel.request_transition(
                    blocked,
                    tuple(facts(callback_authority, blocked)),
                )
                assert decision.outcome is DecisionOutcome.ADMITTED
                await callback_engine.dispose()

            try:
                asyncio.run(transition())
            except BaseException as exc:  # pragma: no cover - asserted below
                callback_errors.append(exc)

        function_call = {
            "id": f"fc_workflow_left_{unique}",
            "type": "function_call",
            "status": "completed",
            "name": "synthetic_lookup",
            "call_id": f"call_workflow_left_{unique}",
            "arguments": '{"key":"aiscc-fixed-key"}',
        }
        service = AgentExecutionService(
            policy=policy,
            adapter=adapter,
            secret_resolver=resolver,
            authority_reader=UnusedSyncAuthorityReader(),
            secret_lease_authority=lease_authority,
            repository=repository,
            provider_tool_authority=provider_tool_authority,
            secret_use_authority=secret_use_authority,
            profile=profile,
            tool_registry=registry,
            tool_dispatcher=dispatcher,
            execution_ref_authority=execution_refs,
            server_initial_inputs={
                profile.public_scenario_identity: (
                    {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": "leave running"}],
                    },
                )
            },
        )
        with FakeResponsesServer() as server:
            server.enqueue(
                response_body("completed", [function_call]),
                before_response=leave_running,
            )
            result = await service.execute(
                work_run_id=run_id,
                execution_attempt_id=attempt_id,
                principal="owner",
                scenario_id=profile.public_scenario_identity,
                max_provider_rounds=1,
            )
            assert len(server.requests) == 1
        assert not callback_errors
        assert result.status == "EXECUTION_FAILED"
        assert adapter.invocation_count == 1
        assert resolver.invocation_count == 1
        assert dispatcher.calls == 0
        async with factory() as session:
            work_run = await session.get(WorkRunRow, run_id)
            attempt = await session.get(ExecutionAttemptRow, attempt_id)
            failure = await session.scalar(
                select(ExecutionEventRow)
                .where(
                    ExecutionEventRow.execution_attempt_id == attempt_id,
                    ExecutionEventRow.event_kind == "EXECUTION_FAILED",
                )
                .order_by(ExecutionEventRow.event_sequence.desc())
            )
            tool_operations = await session.scalar(
                select(func.count())
                .select_from(ExecutionOperationRow)
                .where(
                    ExecutionOperationRow.execution_attempt_id == attempt_id,
                    ExecutionOperationRow.operation_kind == OperationKind.TOOL.value,
                )
            )
            assert work_run is not None
            assert (work_run.workflow_state, work_run.state_version) == ("BLOCKED", 3)
            blocker = await session.scalar(
                select(P1_4BlockerProvenanceRow).where(
                    P1_4BlockerProvenanceRow.work_run_id == run_id,
                    P1_4BlockerProvenanceRow.blocked_epoch == 3,
                )
            )
            blocker_projection = await session.get(P1_4BlockerProjectionRow, run_id)
            assert blocker is not None
            assert (
                blocker.blocker_kind,
                blocker.reason_code,
                blocker.resumability,
            ) == ("EXECUTION", "EXECUTION_BLOCKER", "RESUMABLE")
            assert blocker.payload["resolution_source_contract_ref"] == (
                blocker_source_contract_ref
            )
            assert blocker.payload["resolution_source_contract_fingerprint"] == (
                blocker_source_contract_fingerprint
            )
            assert blocker.payload["ordered_source_authority_refs"] == [blocker_source_ref]
            assert blocker.payload["ordered_source_authority_fingerprints"] == [
                blocker_source_fingerprint
            ]
            assert blocker_projection is not None
            assert (
                blocker_projection.blocker_ref,
                blocker_projection.state,
                blocker_projection.blocked_epoch,
            ) == (blocker.blocker_ref, "ACTIVE", 3)
            assert attempt is not None and attempt.status == "EXECUTION_FAILED"
            assert failure is not None
            assert failure.refs["failure_class"] == denial_class
            assert failure.refs["reason"] == denial_reason
            assert tool_operations == 0

    try:
        run(scenario())
    finally:
        run(engine.dispose())


@pytest.mark.postgres
@pytest.mark.parametrize(
    ("denial_case", "expected_outcome"),
    [
        (
            "SAME_DOMAIN_WRONG_RESOURCE",
            ExecutionOperationOutcome.DENIED_BEFORE_SIDE_EFFECT,
        ),
        ("ATOMIC_CONSUME_FAILURE", ExecutionOperationOutcome.CANCELLED),
    ],
)
def test_production_tool_admission_denials_never_cross_dispatch_started(
    denial_case: str,
    expected_outcome: ExecutionOperationOutcome,
) -> None:
    database_url = os.environ["AISCC_TEST_DATABASE_URL"]
    engine = create_engine(database_url)
    factory = create_session_factory(engine)
    unique = uuid4().hex
    run_id = f"tool-admission-run-{unique}"
    attempt_id = f"tool-admission-attempt-{unique}"

    async def scenario() -> None:
        now = datetime.now(UTC)
        async with factory() as session, session.begin():
            session.add(
                WorkRunRow(
                    work_run_id=run_id,
                    project_id="project-p1-5-tool-admission",
                    task_contract_id="task-p1-5-tool-admission",
                    task_contract_version="1",
                    workflow_state=WorkflowState.READY.value,
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
            profile_id="fake-openai-responses-v1",
            profile_version="1",
            registry_id="aiscc-p1-5-tools",
            registry_version="1",
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

        profile = load_provider_profile(
            Path("config/providers/provider-profiles.v1.toml"),
            "fake-openai-responses-v1",
        )
        loaded_registry = load_tool_registry(Path("config/providers/tool-registry.v1.toml"))
        definition = loaded_registry.tools["synthetic_lookup"]
        service_type: type[AgentExecutionService] = AgentExecutionService
        if denial_case == "SAME_DOMAIN_WRONG_RESOURCE":
            definition = replace(
                definition,
                underlying_resource_requirements=(
                    ResourceRequirement(
                        ResourceScope(
                            ResourceDomain.FILESYSTEM,
                            "workspace:server-owned-exact",
                        ),
                        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
                    ),
                ),
            )
            service_type = SameDomainWrongResourceService
        registry = ToolRegistry(
            loaded_registry.registry_id,
            loaded_registry.version,
            MappingProxyType({definition.tool_id: definition}),
        )
        tool_identity = ":".join(
            (
                registry.registry_id,
                registry.version,
                definition.tool_id,
                definition.schema_version,
                definition.dispatcher_version,
            )
        )
        modes = frozenset({RuntimeMode.OWNER_SELF_DOGFOOD})
        provider_tool_authority = ProviderToolResourceAuthority(
            allowed_resource_identities=frozenset(
                {profile.provider_resource_identity, tool_identity}
            ),
            allowed_profile_ids=frozenset({profile.profile_id}),
            allowed_scenarios=frozenset({profile.public_scenario_identity}),
            allowed_modes=modes,
        )
        secret_use_authority = SecretUseAuthority(
            allowed_secret_refs=frozenset({profile.secret_ref}),
            allowed_profile_ids=frozenset({profile.profile_id}),
            allowed_scenarios=frozenset({profile.public_scenario_identity}),
            allowed_destinations=frozenset({profile.endpoint_ref}),
            allowed_modes=modes,
        )
        policy_type: type[SecurityPolicy] = (
            DenySecondAtomicBatchPolicy
            if denial_case == "ATOMIC_CONSUME_FAILURE"
            else SecurityPolicy
        )
        policy = policy_type(
            default_profiles(),
            provider_tool_policy=provider_tool_authority,
            secret_use_policy=secret_use_authority,
        )
        if isinstance(policy, DenySecondAtomicBatchPolicy):
            policy.atomic_batches = 0
        lease_authority = SecretResolutionLeaseAuthority(policy.verify_consumption_receipt)
        resolver = LeaseBoundSecretResolver(
            lease_authority,
            {profile.secret_ref: "AISCC_SYNTHETIC_LOCAL_ONLY"},
        )
        adapter = OpenAIResponsesAdapter()
        dispatcher = DurableSyntheticDispatcher()
        service = service_type(
            policy=policy,
            adapter=adapter,
            secret_resolver=resolver,
            authority_reader=UnusedSyncAuthorityReader(),
            secret_lease_authority=lease_authority,
            repository=repository,
            provider_tool_authority=provider_tool_authority,
            secret_use_authority=secret_use_authority,
            profile=profile,
            tool_registry=registry,
            tool_dispatcher=dispatcher,
            execution_ref_authority=ExecutionReferenceAuthority(),
            server_initial_inputs={
                profile.public_scenario_identity: (
                    {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": "tool admission"}],
                    },
                )
            },
        )
        function_call = {
            "id": f"fc_tool_admission_{unique}",
            "type": "function_call",
            "status": "completed",
            "name": "synthetic_lookup",
            "call_id": f"call_tool_admission_{unique}",
            "arguments": '{"key":"aiscc-fixed-key"}',
        }
        with FakeResponsesServer() as server:
            server.enqueue(response_body("completed", [function_call]))
            result = await service.execute(
                work_run_id=run_id,
                execution_attempt_id=attempt_id,
                principal="owner",
                scenario_id=profile.public_scenario_identity,
                max_provider_rounds=1,
            )
            assert len(server.requests) == 1
        assert result.status == "EXECUTION_FAILED"
        assert adapter.invocation_count == 1
        assert resolver.invocation_count == 1
        assert dispatcher.calls == 0
        async with factory() as session:
            tool_operation = await session.scalar(
                select(ExecutionOperationRow).where(
                    ExecutionOperationRow.execution_attempt_id == attempt_id,
                    ExecutionOperationRow.operation_kind == OperationKind.TOOL.value,
                )
            )
            assert tool_operation is not None
            assert tool_operation.current_phase == ExecutionOperationPhase.OUTCOME_KNOWN.value
            assert tool_operation.outcome == expected_outcome.value
            dispatch_events = await session.scalar(
                select(func.count())
                .select_from(OperationEventRow)
                .where(
                    OperationEventRow.operation_id == tool_operation.operation_id,
                    OperationEventRow.target_phase
                    == ExecutionOperationPhase.DISPATCH_STARTED.value,
                )
            )
            assert dispatch_events == 0

    try:
        run(scenario())
    finally:
        run(engine.dispose())
