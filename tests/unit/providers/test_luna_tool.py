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
from aiscc.providers.stockroom_tool import (
    StockroomSummaryDispatcher,
    build_dispatch_context,
    build_stockroom_spec,
    load_stockroom_tool_config,
)
from aiscc.providers.tools import (
    ToolRegistryBroker,
)
from aiscc.runtime.docker import DockerRuntime, StockroomProcessObservation
from aiscc.security.capability import CapabilityConsumeRequest
from aiscc.security.policy import SecurityPolicy


def composition(tmp_path: Path, monkeypatch, runner, owner="run-stockroom", state_version=4):
    from aiscc.public_live.luna_profile import luna_tool_registry
    from aiscc.public_live.provider_authority import (
        LunaToolScopeAuthority,
        luna_permission_profiles,
    )
    from tests.unit.runtime.test_stockroom_image import synthetic_image

    image, *_ = synthetic_image(tmp_path, monkeypatch)
    config = load_stockroom_tool_config(Path("config/providers/stockroom-tools.v2.toml"))
    spec = build_stockroom_spec(
        config,
        name="stockroom-runner",
        run_id=owner,
        workspace=tmp_path,
        image_provenance=image,
    )
    registry = luna_tool_registry(config, spec)
    broker = ToolRegistryBroker(registry)
    dispatch_context = build_dispatch_context(
        run_id=owner,
        attempt_id="attempt-stockroom",
        state_version=state_version,
        scenario_id="stockroom-s1-normal",
        profile_id="public-live-luna-v1",
        provider_operation_id="provider-operation",
        provider_call_id=CANDIDATE.call_id,
        spec=spec,
    )
    dispatch_context = replace(dispatch_context, runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE.value)
    definition, arguments, fingerprint = broker.validate_candidate(
        CANDIDATE,
        mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        profile_id="public-live-luna-v1",
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
        allowed_profile_ids=frozenset({"public-live-luna-v1"}),
        allowed_scenarios=frozenset({"stockroom-s1-normal"}),
        allowed_modes=frozenset({RuntimeMode.PUBLIC_BOUNDED_LIVE}),
    )
    restriction = LunaToolScopeAuthority(
        dispatch_context=dispatch_context, spec=spec, principal="owner", fingerprint=fingerprint
    )
    policy = SecurityPolicy(
        luna_permission_profiles(), provider_tool_policy=authority, stockroom_policy=restriction
    )
    snapshot = WorkflowSnapshot(owner, WorkflowState.RUNNING, state_version)
    selector = ProviderToolSelectorRequest(
        ResourceDomain.TOOL.value,
        identity,
        "owner",
        snapshot.run_id,
        "attempt-stockroom",
        snapshot.state,
        snapshot.state_version,
        RuntimeMode.PUBLIC_BOUNDED_LIVE,
        "public-live-luna-v1",
        "1",
        "stockroom-s1-normal",
        fingerprint,
    )
    attestation = authority.attest(selector)

    def request_for(scope: ResourceScope, index: int) -> CapabilityConsumeRequest:
        selector_ref = attestation.attestation_id if scope.domain is ResourceDomain.TOOL else None
        selector_request = selector if scope.domain is ResourceDomain.TOOL else None
        owner_context = restriction.context
        grant = policy.issue_resource_grant(
            mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
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
            RuntimeMode.PUBLIC_BOUNDED_LIVE,
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
            RuntimeMode.PUBLIC_BOUNDED_LIVE,
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
        mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        profile_id="public-live-luna-v1",
        scenario_id="stockroom-s1-normal",
        capabilities=requirements,
        dispatch_context=dispatch_context,
    )
    runtime = DockerRuntime(policy, stockroom_runner=runner)
    return broker, prepared, StockroomSummaryDispatcher(runtime, spec), runtime, spec, policy


CANDIDATE = ToolCallCandidate("stockroom_summary", "{}", "call-stockroom")


def success(*_):
    body = json.dumps(STOCKROOM_SUMMARY, sort_keys=True, separators=(",", ":")) + "\n"
    return StockroomProcessObservation(0, body.encode("ascii"), b"")


def test_luna_uses_existing_receipt_backed_stockroom_dispatch(tmp_path, monkeypatch):
    broker, prepared, dispatcher, runtime, spec, policy = composition(
        tmp_path, monkeypatch, success
    )
    consumed = broker.consume_prepared(prepared, policy=policy, secret_lease_authority=None)
    result = broker.dispatch_prepared(consumed, dispatcher=dispatcher, secret_resolver=None)
    assert result.output == STOCKROOM_SUMMARY
    assert dispatcher.invocation_count == 1
    with pytest.raises(ValueError):
        broker.dispatch_prepared(consumed, dispatcher=dispatcher, secret_resolver=None)
    assert dispatcher.invocation_count == 1


@pytest.mark.parametrize("change", ["scope", "context", "fingerprint", "scenario"])
def test_public_stockroom_scope_cannot_expand(tmp_path, monkeypatch, change):
    broker, prepared, dispatcher, runtime, spec, policy = composition(
        tmp_path, monkeypatch, success
    )
    restriction = policy._stockroom_policy
    grant = policy.issue_resource_grant(
        mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        profile_version="p1-3-v2",
        scenario_id="other" if change == "scenario" else "stockroom-s1-normal",
        principal="owner",
        run_id=prepared.dispatch_context.work_run_id,
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=replace(spec.scope(), argv=("sh",)) if change == "scope" else spec.scope(),
        operation_fingerprint="0" * 64 if change == "fingerprint" else prepared.fingerprint,
        stockroom_context=object() if change == "context" else restriction.context,
    )
    assert grant is None
