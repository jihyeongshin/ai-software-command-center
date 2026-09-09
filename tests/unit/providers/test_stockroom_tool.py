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
