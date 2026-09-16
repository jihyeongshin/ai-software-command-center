from __future__ import annotations

import asyncio
import os
from types import MappingProxyType, SimpleNamespace
from uuid import uuid4

import pytest
from sqlalchemy import text

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.persistence import (
    PostgresExecutionRepository,
    PostgresTransitionRepository,
    create_engine,
    create_session_factory,
)
from aiscc.providers.authority import (
    ExecutionReferenceAuthority,
    ProviderToolResourceAuthority,
    SecretResolutionLeaseAuthority,
    SecretUseAuthority,
)
from aiscc.providers.hosted_secret import SECRET_VARIABLE, HostedOpenAISecretResolver
from aiscc.providers.models import (
    ExecutionAttemptRef,
    ExecutionStatus,
    ToolRegistry,
)
from aiscc.providers.openai_responses import OpenAIResponsesAdapter
from aiscc.providers.service import AgentExecutionService
from aiscc.public_live.luna_profile import hosted_luna_profile
from aiscc.public_live.provider_authority import luna_permission_profiles
from aiscc.security.policy import SecurityPolicy
from aiscc.workflow.evaluator import TransitionEvaluator
from aiscc.workflow.guards import P1_4GuardAuthority, TrustedGuardFact
from aiscc.workflow.kernel import WorkflowKernel
from aiscc.workflow.matrix import TRANSITION_MATRIX
from aiscc.workflow.models import DecisionOutcome, GuardId, RequesterType, TransitionRequest
from tests.integration.providers.test_execution_persistence import (
    DurableSyntheticDispatcher,
    UnusedSyncAuthorityReader,
)


@pytest.mark.postgres
@pytest.mark.parametrize(
    "case", ["missing", "blank", "positive", "crash", "freshness", "uncertain"]
)
def test_hosted_durable_boundary(case, monkeypatch, capsys):
    engine = create_engine(os.environ["AISCC_TEST_DATABASE_URL"])
    factory = create_session_factory(engine)
    unique = uuid4().hex
    run_id, attempt_id = "hosted-run-" + unique, "hosted-attempt-" + unique
    runtime_mode = RuntimeMode.PUBLIC_BOUNDED_LIVE
    profile = hosted_luna_profile()
    sentinel = "SYNTHETIC_HOSTED_SENTINEL_" + unique
    monkeypatch.delenv(SECRET_VARIABLE, raising=False)
    if case != "missing":
        monkeypatch.setenv(SECRET_VARIABLE, "   " if case == "blank" else sentinel)
    sdk_calls = []
    leases = []

    def sdk(**kwargs):
        assert kwargs["api_key"] == sentinel

        def create(**request):
            sdk_calls.append(request)
            if case == "uncertain":
                raise RuntimeError("synthetic transport uncertainty")
            return SimpleNamespace(
                http_response=SimpleNamespace(
                    json=lambda: {
                        "id": "fake",
                        "status": "completed",
                        "output": [
                            {
                                "type": "message",
                                "role": "assistant",
                                "content": [{"type": "output_text", "text": "SAFE"}],
                            }
                        ],
                        "usage": {"input_tokens": 2, "output_tokens": 1},
                    }
                )
            )

        return SimpleNamespace(
            responses=SimpleNamespace(with_raw_response=SimpleNamespace(create=create))
        )

    monkeypatch.setattr("aiscc.providers.openai_responses.OpenAI", sdk)

    async def scenario():
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
                    profile.public_repository_resource_identity
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
            profile_id=profile.profile_id,
            profile_version="1",
            registry_id=profile.tool_registry_id,
            registry_version=profile.tool_registry_version,
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

        from dataclasses import replace
        from pathlib import Path

        from aiscc.providers.profiles import load_tool_registry

        fixture_tool = load_tool_registry(Path("config/providers/tool-registry.v1.toml")).tools[
            "synthetic_lookup"
        ]
        registry = ToolRegistry(
            profile.tool_registry_id,
            profile.tool_registry_version,
            MappingProxyType(
                {
                    "stockroom_summary": replace(
                        fixture_tool,
                        tool_id="stockroom_summary",
                        input_schema={
                            "type": "object",
                            "properties": {},
                            "required": [],
                            "additionalProperties": False,
                        },
                    )
                }
            ),
        )
        provider_authority = ProviderToolResourceAuthority(
            allowed_resource_identities=frozenset({profile.provider_resource_identity}),
            allowed_profile_ids=frozenset({profile.profile_id}),
            allowed_scenarios=frozenset({"stockroom-s1-normal"}),
            allowed_modes=frozenset({runtime_mode}),
        )
        secret_authority = SecretUseAuthority(
            allowed_secret_refs=frozenset({profile.secret_ref}),
            allowed_profile_ids=frozenset({profile.profile_id}),
            allowed_scenarios=frozenset({"stockroom-s1-normal"}),
            allowed_destinations=frozenset({profile.endpoint_ref}),
            allowed_modes=frozenset({runtime_mode}),
        )

        class FixedScope:
            context = object()

            def allows(self, context, **kw):
                return (
                    context is self.context
                    and kw["run_id"] == run_id
                    and kw["mode"] is runtime_mode
                    and kw["scenario_id"] == "stockroom-s1-normal"
                    and kw["scope"].resource_id
                    in {
                        profile.provider_resource_identity,
                        profile.secret_resource_identity,
                        profile.public_repository_resource_identity,
                        profile.public_scenario_resource_identity,
                    }
                )

        scope = FixedScope()
        from aiscc.contracts.workflow import WorkflowSnapshot
        from aiscc.public_live.context_authority import PublicLiveContextResourceAuthority

        context_owner = PublicLiveContextResourceAuthority(
            profile=profile,
            current=WorkflowSnapshot(run_id, WorkflowState.RUNNING, 2),
            attempt=attempt_id,
            principal="owner",
        )
        policy = SecurityPolicy(
            luna_permission_profiles(),
            stockroom_policy=scope,
            public_context_policy=context_owner,
            provider_tool_policy=provider_authority,
            secret_use_policy=secret_authority,
        )
        lease_authority = SecretResolutionLeaseAuthority(policy.verify_consumption_receipt)

        class Resolver(HostedOpenAISecretResolver):
            def resolve(self, lease):
                leases.append(lease)
                material = super().resolve(lease)
                if case == "crash":
                    raise KeyboardInterrupt("synthetic process death before reservation")
                return material

        resolver = Resolver(lease_authority)
        adapter = OpenAIResponsesAdapter(hosted=True)
        if case == "freshness":
            original = execution_repository.start_dispatch_if_fresh

            async def stale(**kw):
                kw["expected_state_version"] += 1
                return await original(**kw)

            execution_repository.start_dispatch_if_fresh = stale

        def service(repository):
            return AgentExecutionService(
                policy=policy,
                adapter=adapter,
                secret_resolver=resolver,
                authority_reader=UnusedSyncAuthorityReader(),
                secret_lease_authority=lease_authority,
                repository=repository,
                provider_tool_authority=provider_authority,
                secret_use_authority=secret_authority,
                profile=profile,
                tool_registry=registry,
                tool_dispatcher=DurableSyntheticDispatcher(),
                execution_ref_authority=execution_refs,
                stockroom_context_factory=lambda **kw: scope.context,
                public_context_authority=context_owner,
                server_initial_inputs={
                    "stockroom-s1-normal": ({"role": "user", "content": "Fixed synthetic input."},)
                },
            )

        executor = service(execution_repository)
        args = dict(
            work_run_id=run_id,
            execution_attempt_id=attempt_id,
            principal="owner",
            scenario_id="stockroom-s1-normal",
        )
        if case == "crash":
            with pytest.raises(KeyboardInterrupt):
                await executor.execute(**args)
            result = await service(PostgresExecutionRepository(factory)).execute(**args)
        else:
            result = await executor.execute(**args)
        operations = await execution_repository.load_operations(attempt_id)
        assert len(operations) == 1
        async with factory() as session:
            rows = (
                await session.execute(
                    text(
                        "SELECT current_phase,outcome FROM execution_operations "
                        "WHERE execution_attempt_id=:a"
                    ),
                    {"a": attempt_id},
                )
            ).all()
        phase, outcome = rows[0]
        async with factory() as session:
            events = (
                await session.execute(
                    text(
                        "SELECT e.target_phase,e.refs FROM operation_events e "
                        "JOIN execution_operations o ON o.operation_id=e.operation_id "
                        "WHERE o.execution_attempt_id=:a"
                    ),
                    {"a": attempt_id},
                )
            ).all()
        if case in {"missing", "blank"}:
            assert any(refs.get("reason") == "LIVE_UNAVAILABLE" for _, refs in events)
            assert all(
                target not in {"DISPATCH_STARTED", "OUTCOME_UNKNOWN"} for target, _ in events
            )
        counters = await execution_repository.load_durable_counters(attempt_id)
        if case in {"missing", "blank", "crash"}:
            assert (phase, outcome) == ("OUTCOME_KNOWN", "CANCELLED")
            assert counters.provider_calls == counters.agent_rounds == counters.budget_units == 0
            assert counters.output_tokens == 0 and not sdk_calls
            assert result.status == "EXECUTION_FAILED"
        elif case == "freshness":
            assert phase == "OUTCOME_KNOWN" and outcome == "CANCELLED"
            assert counters.provider_calls == 1 and not sdk_calls
        elif case == "uncertain":
            assert (phase, outcome) == ("OUTCOME_UNKNOWN", "TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME")
            assert counters.provider_calls == 1 and len(sdk_calls) == 1
        else:
            assert phase == "OUTCOME_KNOWN" and outcome == "PROVIDER_COMPLETED"
            assert result.status == "EXECUTOR_COMPLETED" and len(sdk_calls) == 1
            request = sdk_calls[0]
            assert request["model"] == "gpt-5.6-luna" and request["reasoning"] == {"effort": "low"}
            assert all(
                request[k] is False
                for k in ["stream", "store", "background", "parallel_tool_calls"]
            )
            assert request["truncation"] == "disabled" and request["max_output_tokens"] == 2000
        # Restart does not resend terminal/unknown attempts.
        count = len(sdk_calls)
        await service(PostgresExecutionRepository(factory)).execute(**args)
        assert len(sdk_calls) == count
        for lease in tuple(leases):
            with pytest.raises(ValueError, match="SECRET_LEASE_DENIED"):
                resolver.resolve(lease)
        # All application text/JSON/bytea columns, without dumping their contents.
        inspected = []
        async with factory() as session:
            columns = (
                await session.execute(
                    text(
                        "SELECT table_schema,table_name,column_name,data_type "
                        "FROM information_schema.columns "
                        "WHERE table_schema IN ('public','public_live') AND data_type IN "
                        "('text','character varying','json','jsonb','bytea')"
                    )
                )
            ).all()
            for schema, table, column, kind in columns:
                ident = '"' + column.replace('"', '""') + '"'
                expr = f"encode({ident}, 'escape')" if kind == "bytea" else f"{ident}::text"
                query = f'SELECT count(*) FROM "{schema}"."{table}" WHERE strpos({expr}, :needle)>0'
                assert (await session.execute(text(query), {"needle": sentinel})).scalar_one() == 0
                inspected.append(f"{schema}.{table}.{column}")
        assert inspected
        evidence_dir = os.environ.get("AISCC_L5_EVIDENCE_DIR")
        if evidence_dir:
            import json
            from pathlib import Path

            (Path(evidence_dir) / ("DURABLE_" + case + ".json")).write_text(
                json.dumps(
                    {
                        "case": case,
                        "phase": phase,
                        "outcome": outcome,
                        "sdk_requests": len(sdk_calls),
                        "provider_reservations": counters.provider_calls,
                        "round_reservations": counters.agent_rounds,
                        "budget_reservations": counters.budget_units,
                        "scanned_columns": inspected,
                        "sentinel_occurrences": 0,
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
        assert sentinel not in repr((result, operations, counters))
        await engine.dispose()

    asyncio.run(scenario())
    assert sentinel not in str(capsys.readouterr())
