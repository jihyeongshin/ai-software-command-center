from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest

from aiscc.contracts.security import (
    AuthorityStatus,
    PermissionRequest,
    ResourceDomain,
    ResourceScope,
    SecurityActionClass,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.providers.authority import ProviderToolResourceAuthority
from aiscc.providers.local_deterministic import STOCKROOM_SUMMARY
from aiscc.providers.models import ProviderToolSelectorRequest, ToolCallCandidate
from aiscc.providers.profiles import load_tool_registry
from aiscc.providers.stockroom_tool import (
    StockroomSummaryDispatcher,
    build_dispatch_context,
    build_stockroom_registry,
    build_stockroom_spec,
    load_stockroom_tool_config,
)
from aiscc.providers.tools import (
    KnownToolFailure,
    ToolDispatchContext,
    ToolRegistryBroker,
    UnknownToolOutcome,
)
from aiscc.runtime.docker import DockerRuntime, StockroomProcessObservation
from aiscc.security.capability import CapabilityConsumeRequest
from aiscc.security.policy import SecurityPolicy, default_profiles
from aiscc.security.stockroom_policy import (
    StockroomOwnerRestriction,
    load_stockroom_owner_policy,
)

TOOL_CONFIG = Path("config/providers/stockroom-tools.v1.toml")
POLICY_CONFIG = Path("config/security/stockroom-owner.v1.toml")
CANDIDATE = ToolCallCandidate("stockroom_summary", "{}", "call-stockroom")


def production_provider_fixture(tmp_path, monkeypatch):
    """Real execution factory/security, with only materialization/persistence inert."""
    import socket
    import subprocess
    from datetime import UTC, datetime
    from threading import Event
    from types import SimpleNamespace

    from aiscc.evidence.service import EvidenceAdmissionService
    from aiscc.human.repository import PostgresHumanAuthorityRepository
    from aiscc.judgment.authority import PostgresJudgmentAuthority
    from aiscc.providers.authority import (
        ExecutionReferenceAuthority,
        LeaseBoundSecretResolver,
        SecretResolutionLeaseAuthority,
        SecretUseAuthority,
    )
    from aiscc.providers.local_deterministic import (
        LOCAL_COMPATIBILITY_SECRET_REF,
        LOCAL_COMPATIBILITY_SENTINEL,
        LocalDeterministicProvider,
    )
    from aiscc.providers.models import ExecutionAttemptRef, ExecutionStatus, ProviderCall
    from aiscc.runtime.docker import StockroomCancellation
    from aiscc.runtime.stockroom_workspace import StockroomWorkspace
    from aiscc.scenarios.composition import build_stockroom_production_composition
    from aiscc.scenarios.driver import (
        StockroomMaterializedResultBinding,
        StockroomOwnerDependencies,
        prepare_stockroom_driver,
    )
    from aiscc.scenarios.runtime_models import MaterializedStockroom, StockroomWorkspaceLease
    from aiscc.scenarios.stockroom_production import (
        StockroomAgentExecutionServiceFactory,
        StockroomMaterializerFactory,
        _CurrentAttemptReader,
        _CurrentBinding,
    )
    from aiscc.workflow.kernel import WorkflowKernel
    from tests.unit.runtime.test_stockroom_image import synthetic_image

    def forbidden_boundary(*args, **kwargs):
        raise AssertionError("private DB/process/external network forbidden in this fixture")

    monkeypatch.setattr(subprocess, "Popen", forbidden_boundary)
    monkeypatch.setattr(socket.socket, "connect", forbidden_boundary)
    image, *_ = synthetic_image(tmp_path, monkeypatch)
    composition = build_stockroom_production_composition(image)
    profile = composition.provider_profiles["stockroom-owner-s1-v1"].profile
    restriction = StockroomOwnerRestriction(composition.security_config)
    selectors = ProviderToolResourceAuthority(
        allowed_resource_identities=frozenset({profile.provider_resource_identity}),
        allowed_profile_ids=frozenset({profile.profile_id}),
        allowed_scenarios=frozenset({"stockroom-s1-normal"}),
        allowed_modes=frozenset({RuntimeMode.OWNER_SELF_DOGFOOD}),
    )
    secrets = SecretUseAuthority(
        allowed_secret_refs=frozenset({profile.secret_ref}),
        allowed_profile_ids=frozenset({profile.profile_id}),
        allowed_scenarios=frozenset({"stockroom-s1-normal"}),
        allowed_destinations=frozenset({profile.endpoint_ref}),
        allowed_modes=frozenset({RuntimeMode.OWNER_SELF_DOGFOOD}),
    )
    policy = SecurityPolicy(default_profiles(), provider_tool_policy=selectors,
                            secret_use_policy=secrets, stockroom_policy=restriction)
    leases = SecretResolutionLeaseAuthority(policy.verify_consumption_receipt)
    reader = _CurrentAttemptReader()
    reader.current = WorkflowSnapshot("unit-s1-run", WorkflowState.RUNNING, 2)
    reader.attempt = ExecutionAttemptRef(
        "unit-s1-attempt", "unit-s1-run", "stockroom-s1-normal", "1.0.0",
        WorkflowState.RUNNING, 2, 2, ExecutionStatus.RUNNING, "unit-execution-owner",
        runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
    )
    app = SimpleNamespace(
        project_id="unit-project", requester_identity="unit-owner", composition=composition,
        repository_root=Path.cwd(), private_runtime_root=tmp_path,
        security_policy=policy, stockroom_owner_restriction=restriction,
        cancellation=StockroomCancellation("unit-s1-run", "unit-s1-attempt", Event()),
        docker_runtime=DockerRuntime(policy),
        local_provider=LocalDeterministicProvider(composition.provider_profiles),
        secret_resolver=LeaseBoundSecretResolver(
            leases, {LOCAL_COMPATIBILITY_SECRET_REF: LOCAL_COMPATIBILITY_SENTINEL}
        ),
        secret_lease_authority=leases, execution_repository=None,
        provider_tool_authority=selectors, secret_use_authority=secrets,
        execution_reference_authority=ExecutionReferenceAuthority(),
        clock=lambda: datetime.now(UTC),
    )
    materializer = StockroomMaterializerFactory(app, _CurrentBinding())
    factory = StockroomAgentExecutionServiceFactory(app, reader)
    owners = StockroomOwnerDependencies(
        object.__new__(WorkflowKernel), factory, object.__new__(EvidenceAdmissionService),
        object.__new__(PostgresHumanAuthorityRepository),
        object.__new__(PostgresJudgmentAuthority), object.__new__(StockroomWorkspace),
        materializer, policy, restriction,
    )
    request = composition.request(scenario_id="stockroom-s1-normal", run_id="unit-s1-run",
                                  attempt_id="unit-s1-attempt", expected_initial_state_version=1)
    prepared = prepare_stockroom_driver(request, owners)
    resource = composition.catalog.resource
    (tmp_path / "inert-workspace").mkdir()
    materialized = MaterializedStockroom(
        resource.resource_ref, resource.source_commit, resource.subroot, resource.git_subtree,
        (), resource.aggregate_sha256,
        StockroomWorkspaceLease("unit-lease", "unit-s1-run", "unit-s1-attempt", tmp_path,
                                tmp_path / "inert-workspace"),
        "unit-s1-run", "unit-s1-attempt", tmp_path / "inert-workspace",
    )
    bound = object.__new__(StockroomMaterializedResultBinding)
    object.__setattr__(bound, "materialized", materialized)
    object.__setattr__(bound, "provenance", SimpleNamespace(
        provenance_fingerprint="a" * 64, materialized_output_fingerprint="b" * 64,
    ))

    def fake_materialization_owner(self, *, prepared, result):
        assert self is materializer and prepared.request is request and result is bound
        return bound

    monkeypatch.setattr(StockroomMaterializerFactory, "require_issued_result",
                        fake_materialization_owner)
    inputs = factory.prepare_inputs(prepared=prepared, materialized_result=bound)
    service = factory.derive(prepared=prepared, inputs=inputs,
                             execution_reference_authority=app.execution_reference_authority).owner
    call = ProviderCall(
        "unit-provider-op", "c" * 64, "unit-s1-attempt", "unit-s1-run",
        WorkflowState.RUNNING, 2, RuntimeMode.OWNER_SELF_DOGFOOD, "unit-owner",
        "stockroom-s1-normal", 2, profile,
        ({"type": "message", "role": "user", "content": []},),
        ({"name": "stockroom_summary"},), 1,
    )
    return SimpleNamespace(app=app, service=service, call=call, current=reader.current,
                           prepared=prepared, inputs=inputs, policy=policy)


def test_production_provider_grant_uses_bound_process_identity(tmp_path, monkeypatch):
    fixture = production_provider_fixture(tmp_path, monkeypatch)
    capabilities, secret = fixture.service._provider_capabilities(
        fixture.call, fixture.current, fixture.call.operation_id
    )
    assert [x.scope.domain for x in capabilities] == [
        ResourceDomain.PROVIDER, ResourceDomain.SECRET,
    ]
    assert capabilities[0].scope.resource_id == fixture.call.profile.provider_resource_identity
    contexts = tuple(fixture.app.stockroom_owner_restriction._contexts.values())
    assert {x.process_spec_fingerprint for x in contexts} == {
        fixture.inputs.docker_spec_fingerprint
    }
    result = fixture.service.execute_provider(fixture.call, capabilities=capabilities,
                                              secret_request=secret)
    assert result.status == "completed"
    assert result.tool_call.name == "stockroom_summary"
    assert fixture.app.local_provider.invocation_count == 1


@pytest.mark.parametrize("field", [
    "provider", "tool_scope", "secret_scope", "run", "state", "version", "mode", "profile",
])
def test_production_provider_exact_grant_rejects_changed_request(field, tmp_path, monkeypatch):
    from aiscc.contracts.security import SecurityAdmissionDecision

    fixture = production_provider_fixture(tmp_path, monkeypatch)
    fixture.service._provider_capabilities(
        fixture.call, fixture.current, fixture.call.operation_id
    )
    request = next(request for _, request in fixture.policy._admissions.values()
                   if request.resource_scope.domain is ResourceDomain.PROVIDER)
    assert request.resource_grant.scope == request.resource_scope
    if field == "provider":
        changed = replace(request, resource_scope=ResourceScope(ResourceDomain.PROVIDER,
                                                               "wrong-provider-resource"))
    elif field in {"tool_scope", "secret_scope"}:
        domain = ResourceDomain.TOOL if field == "tool_scope" else ResourceDomain.SECRET
        changed = replace(request, resource_scope=ResourceScope(domain,
                                                               request.resource_scope.resource_id))
    elif field == "run":
        changed = replace(request, run_id="wrong-run")
    elif field == "state":
        changed = replace(request, observed=replace(request.observed, state=WorkflowState.READY))
    elif field == "version":
        changed = replace(request, observed=replace(request.observed, state_version=3))
    elif field == "mode":
        changed = replace(request, mode=RuntimeMode.PUBLIC_BOUNDED_LIVE)
    else:
        changed = replace(request, profile_version="wrong-profile-version")
    assert fixture.policy.evaluate(changed).decision is SecurityAdmissionDecision.DENY
    assert fixture.app.local_provider.invocation_count == 0


@pytest.mark.parametrize("field", ["attempt", "run", "version", "state", "mode", "profile"])
def test_production_provider_call_cannot_reuse_other_binding(field, tmp_path, monkeypatch):
    from aiscc.workflow.models import AuthorityConflictError

    fixture = production_provider_fixture(tmp_path, monkeypatch)
    capabilities, secret = fixture.service._provider_capabilities(
        fixture.call, fixture.current, fixture.call.operation_id
    )
    call = fixture.call
    if field == "attempt":
        call = replace(call, execution_attempt_id="wrong-attempt")
    elif field == "run":
        call = replace(call, work_run_id="wrong-run")
    elif field == "version":
        call = replace(call, state_version=3)
    elif field == "state":
        fixture.service._authority_reader.current = replace(fixture.current,
                                                           state=WorkflowState.READY)
    elif field == "mode":
        call = replace(call, runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE)
    else:
        call = replace(call, profile=replace(call.profile, model_ref="wrong-model"))
    try:
        result = fixture.service.execute_provider(call, capabilities=capabilities,
                                                  secret_request=secret)
    except (ValueError, AuthorityConflictError):
        pass
    else:
        assert result.status == "denied"
    assert fixture.app.local_provider.invocation_count == 0


def test_production_context_rejects_foreign_process_spec(tmp_path, monkeypatch):
    from aiscc.workflow.models import AuthorityConflictError

    fixture = production_provider_fixture(tmp_path, monkeypatch)
    with pytest.raises(AuthorityConflictError, match="process spec binding mismatch"):
        fixture.service._stockroom_context_factory(
            scope=ResourceScope(ResourceDomain.PROVIDER,
                                fixture.call.profile.provider_resource_identity),
            current=fixture.current, resolved_spec_fingerprint="f" * 64,
        )
    assert fixture.app.local_provider.invocation_count == 0


def test_v2_policy_has_no_runtime_image_and_rejects_mixed_schema(tmp_path):
    path = Path("config/providers/stockroom-tools.v2.toml")
    text = path.read_text(encoding="utf-8")
    config = load_stockroom_tool_config(path)
    assert config.registry_version == "2" and config.image is None
    assert load_stockroom_tool_config(TOOL_CONFIG).registry_version == "1"
    variants = [text.replace('[tool]', '[tool]\nimage = "python:latest"'),
                text.replace("TOOLS-V2", "TOOLS-V1"),
                text.replace('registry_version = "2"', 'registry_version = "1"'),
                text.replace('provenance_fingerprint_required = true',
                             'provenance_fingerprint_required = 1')]
    for altered in variants:
        temporary = tmp_path / "mixed.toml"
        temporary.write_text(altered, encoding="utf-8")
        with pytest.raises(ValueError):
            load_stockroom_tool_config(temporary)
    with pytest.raises(ValueError, match="ADMITTED_IMAGE"):
        build_stockroom_spec(config, name="test", run_id="run", workspace=tmp_path)


def _composition(tmp_path: Path, runner):
    config = load_stockroom_tool_config(TOOL_CONFIG)
    spec = build_stockroom_spec(
        config,
        name="stockroom-runner",
        run_id="run-stockroom",
        workspace=tmp_path,
    )
    registry = build_stockroom_registry(config, spec)
    broker = ToolRegistryBroker(registry)
    dispatch_context = build_dispatch_context(
        run_id="run-stockroom",
        attempt_id="attempt-stockroom",
        state_version=4,
        scenario_id="stockroom-s1-normal",
        profile_id="stockroom-owner-s1-v1",
        provider_operation_id="provider-operation",
        provider_call_id=CANDIDATE.call_id,
        spec=spec,
    )
    definition, arguments, fingerprint = broker.validate_candidate(
        CANDIDATE,
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        profile_id="stockroom-owner-s1-v1",
        scenario_id="stockroom-s1-normal",
        dispatch_context=dispatch_context,
    )
    assert arguments == {}
    identity = ":".join(
        (
            registry.registry_id,
            registry.version,
            definition.tool_id,
            definition.schema_version,
            definition.dispatcher_version,
        )
    )
    authority = ProviderToolResourceAuthority(
        allowed_resource_identities=frozenset({identity}),
        allowed_profile_ids=frozenset({"stockroom-owner-s1-v1"}),
        allowed_scenarios=frozenset({"stockroom-s1-normal"}),
        allowed_modes=frozenset({RuntimeMode.OWNER_SELF_DOGFOOD}),
    )
    restriction = StockroomOwnerRestriction(load_stockroom_owner_policy(POLICY_CONFIG))
    policy = SecurityPolicy(
        default_profiles(), provider_tool_policy=authority, stockroom_policy=restriction
    )
    snapshot = WorkflowSnapshot("run-stockroom", WorkflowState.RUNNING, 4)
    selector = ProviderToolSelectorRequest(
        ResourceDomain.TOOL.value,
        identity,
        "owner",
        snapshot.run_id,
        "attempt-stockroom",
        snapshot.state,
        snapshot.state_version,
        RuntimeMode.OWNER_SELF_DOGFOOD,
        "stockroom-owner-s1-v1",
        "1",
        "stockroom-s1-normal",
        fingerprint,
    )
    attestation = authority.attest(selector)

    def request_for(scope: ResourceScope, index: int) -> CapabilityConsumeRequest:
        selector_ref = attestation.attestation_id if scope.domain is ResourceDomain.TOOL else None
        selector_request = selector if scope.domain is ResourceDomain.TOOL else None
        owner_context = restriction.seal_context(
            context_id=f"context-{index}",
            principal="owner",
            task_action="fixed-stockroom-summary",
            mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            scenario_id="stockroom-s1-normal",
            profile_id="stockroom-owner-s1-v1",
            run_id=snapshot.run_id,
            attempt_id="attempt-stockroom",
            state=snapshot.state,
            state_version=snapshot.state_version,
            security_action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            scope=scope,
            operation_fingerprint=fingerprint,
            process_spec_fingerprint=dispatch_context.resolved_spec_fingerprint,
            remaining_provider_calls=2,
            remaining_tool_calls=1,
            remaining_process_calls=1,
            remaining_seconds=30,
            remaining_budget_units=4,
            repository_capability_ref="repository-capability",
            filesystem_capability_ref="filesystem-capability",
            process_capability_ref="process-capability",
            materialized_resource_owner_ref="materialized-owner",
            runtime_root_owner_ref="runtime-root-owner",
        )
        grant = policy.issue_resource_grant(
            mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            profile_version="p1-3-v2",
            scenario_id="stockroom-s1-normal",
            principal="owner",
            run_id=snapshot.run_id,
            action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            scope=scope,
            selector_attestation_ref=selector_ref,
            selector_request=selector_request,
            operation_fingerprint=fingerprint,
            stockroom_context=owner_context,
        )
        permission = PermissionRequest(
            "owner",
            snapshot.run_id,
            RuntimeMode.OWNER_SELF_DOGFOOD,
            snapshot,
            snapshot,
            SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            scope,
            grant,
            "p1-3-v2",
            "stockroom-s1-normal",
            *(AuthorityStatus.GRANTED for _ in range(5)),
            AuthorityStatus.NOT_APPLICABLE,
        )
        capability = policy.issue_capability(policy.evaluate(permission), permission)
        assert capability is not None
        return CapabilityConsumeRequest(
            capability,
            "owner",
            RuntimeMode.OWNER_SELF_DOGFOOD,
            snapshot,
            "p1-3-v2",
            SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            scope,
            selector_ref,
            fingerprint,
        )

    tool_scope = ResourceScope(ResourceDomain.TOOL, identity)
    requirements = (request_for(tool_scope, 1), request_for(spec.scope(), 2))
    prepared = broker.prepare_dispatch(
        CANDIDATE,
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        profile_id="stockroom-owner-s1-v1",
        scenario_id="stockroom-s1-normal",
        capabilities=requirements,
        dispatch_context=dispatch_context,
    )
    runtime = DockerRuntime(policy, stockroom_runner=runner)
    return broker, prepared, StockroomSummaryDispatcher(runtime, spec), runtime, spec


def _success(*_):
    body = json.dumps(STOCKROOM_SUMMARY, sort_keys=True, separators=(",", ":")) + "\n"
    return StockroomProcessObservation(0, body.encode("ascii"), b"")


def test_exact_config_empty_args_fingerprint_and_bounds(tmp_path: Path) -> None:
    broker, prepared, _, _, spec = _composition(tmp_path, _success)
    assert prepared.definition.tool_id == "stockroom_summary"
    assert prepared.definition.schema_version == "1"
    assert prepared.definition.dispatcher_version == "stockroom-summary-v1"
    assert len(prepared.fingerprint) == 64
    assert prepared.dispatch_context is not None
    assert len(prepared.dispatch_context.resolved_spec_fingerprint) == 64
    _, _, rebound = broker.validate_candidate(
        CANDIDATE,
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        profile_id="stockroom-owner-s1-v1",
        scenario_id="stockroom-s1-normal",
        dispatch_context=replace(prepared.dispatch_context, provider_call_id="other-call"),
    )
    assert rebound != prepared.fingerprint
    assert spec.command == ("python", "-B", "-m", "stockroom", "summary")
    assert spec.network == "none" and spec.workdir == "/workspace"
    assert (spec.stdout_limit_bytes, spec.stderr_limit_bytes) == (4096, 4096)
    assert (
        spec.operation_timeout_seconds,
        spec.cleanup_timeout_seconds,
        spec.attempt_timeout_seconds,
    ) == (5, 10, 30)
    with pytest.raises(ValueError, match="SCHEMA_DENIED"):
        broker.validate_candidate(
            replace(CANDIDATE, arguments_json='{"path":"injected"}'),
            mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            profile_id="stockroom-owner-s1-v1",
            scenario_id="stockroom-s1-normal",
            dispatch_context=prepared.dispatch_context,
        )


def test_receipts_cross_once_without_double_consumption(tmp_path: Path) -> None:
    broker, prepared, dispatcher, runtime, spec = _composition(tmp_path, _success)
    consumed = broker.consume_prepared(
        prepared, policy=runtime._policy, secret_lease_authority=None
    )
    assert len(consumed.receipts) == 2 and len(consumed.dispatch_identity) == 64
    with pytest.raises(UnknownToolOutcome):
        broker.dispatch_prepared(
            replace(consumed, receipts=()), dispatcher=dispatcher, secret_resolver=None
        )
    process_index = next(
        index
        for index, item in enumerate(prepared.capabilities)
        if item.scope.domain is ResourceDomain.PROCESS
    )
    receipt = consumed.receipts[process_index]
    requirement = prepared.capabilities[process_index]
    assert runtime._policy.verify_consumption_receipt(receipt, requirement)
    forged = replace(receipt, _issuer_token=object())
    assert not runtime.run_consumed_stockroom(
        forged,
        requirement,
        spec=spec,
        dispatch_identity=consumed.dispatch_identity,
    ).executed
    stale = replace(
        requirement,
        current=WorkflowSnapshot(requirement.current.run_id, WorkflowState.RUNNING, 5),
    )
    assert not runtime.run_consumed_stockroom(
        receipt,
        stale,
        spec=spec,
        dispatch_identity=consumed.dispatch_identity,
    ).executed
    cross_run = replace(
        requirement,
        current=WorkflowSnapshot("other-run", WorkflowState.RUNNING, 4),
    )
    assert not runtime.run_consumed_stockroom(
        receipt,
        cross_run,
        spec=spec,
        dispatch_identity=consumed.dispatch_identity,
    ).executed
    cross_state = replace(
        requirement,
        current=WorkflowSnapshot(requirement.current.run_id, WorkflowState.READY, 4),
    )
    assert not runtime.run_consumed_stockroom(
        receipt,
        cross_state,
        spec=spec,
        dispatch_identity=consumed.dispatch_identity,
    ).executed
    cross_spec = replace(spec, name="other-container")
    assert not runtime.run_consumed_stockroom(
        receipt,
        requirement,
        spec=cross_spec,
        dispatch_identity=consumed.dispatch_identity,
    ).executed

    output = broker.dispatch_prepared(consumed, dispatcher=dispatcher, secret_resolver=None)
    assert output.output == STOCKROOM_SUMMARY
    assert dispatcher.invocation_count == broker.invocation_count == 1
    with pytest.raises(KnownToolFailure):
        broker.dispatch_prepared(consumed, dispatcher=dispatcher, secret_resolver=None)
    with pytest.raises(ValueError, match="CAPABILITY_DENIED"):
        broker.consume_prepared(
            prepared, policy=runtime._policy, secret_lease_authority=None
        )


@pytest.mark.parametrize(
    ("observation", "error"),
    [
        (StockroomProcessObservation(2, b"", b"known", termination_proven=True), KnownToolFailure),
        (
            StockroomProcessObservation(
                None, b"", b"", timed_out=True, termination_proven=False, owner_reconciled=False
            ),
            UnknownToolOutcome,
        ),
    ],
)
def test_known_failure_and_unknown_outcome_are_distinct(tmp_path: Path, observation, error) -> None:
    broker, prepared, dispatcher, runtime, _ = _composition(tmp_path, lambda *_: observation)
    consumed = broker.consume_prepared(
        prepared, policy=runtime._policy, secret_lease_authority=None
    )
    with pytest.raises(error):
        broker.dispatch_prepared(consumed, dispatcher=dispatcher, secret_resolver=None)


def test_stockroom_requires_receipt_aware_path_and_legacy_remains_valid(tmp_path: Path) -> None:
    _, _, dispatcher, _, _ = _composition(tmp_path, _success)
    with pytest.raises(ValueError, match="LEGACY_DISPATCH_DENIED"):
        dispatcher.dispatch(object(), {})
    legacy = ToolRegistryBroker(load_tool_registry(Path("config/providers/tool-registry.v1.toml")))
    definition, arguments, fingerprint = legacy.validate_candidate(
        ToolCallCandidate("synthetic_lookup", '{"key":"aiscc-fixed-key"}', "legacy-call"),
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        profile_id="fake-openai-responses-v1",
        scenario_id="p1-5-fixed-synthetic",
    )
    assert definition.dispatcher_version != "stockroom-summary-v1"
    assert arguments == {"key": "aiscc-fixed-key"} and len(fingerprint) == 64
    with pytest.raises(ValueError, match="LEGACY_TOOL_DISPATCH_CONTEXT_DENIED"):
        legacy.validate_candidate(
            ToolCallCandidate("synthetic_lookup", '{"key":"aiscc-fixed-key"}', "legacy-call"),
            mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            profile_id="fake-openai-responses-v1",
            scenario_id="p1-5-fixed-synthetic",
            dispatch_context=ToolDispatchContext(
                "action", "run", "attempt", "RUNNING", 1, "OWNER_SELF_DOGFOOD",
                "p1-5-fixed-synthetic", "1.0.0", "fake-openai-responses-v1", "1",
                "resource", "provider-operation", "provider-call", "a" * 64,
            ),
        )
