from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

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
from aiscc.providers.models import ProviderToolSelectorRequest, ToolCallCandidate, canonical_sha256
from aiscc.providers.tools import ConsumedToolDispatch, ToolRegistryBroker, UnknownToolOutcome
from aiscc.public_live.luna_profile import luna_profile
from aiscc.public_live.provider_authority import luna_permission_profiles
from aiscc.public_live.stockroom_runtime import compose_public_stockroom
from aiscc.security.capability import CapabilityConsumeRequest
from aiscc.security.policy import SecurityPolicy

CANDIDATE = ToolCallCandidate("stockroom_summary", "{}", "call-stockroom")


def composition(owner: str = "run-stockroom", state_version: int = 4):
    profile = luna_profile()
    public = compose_public_stockroom(
        run_id=owner,
        attempt_id="attempt-stockroom",
        principal="owner",
        profile=profile,
    )
    broker = ToolRegistryBroker(public.registry)
    snapshot = WorkflowSnapshot(owner, WorkflowState.RUNNING, state_version)
    context = public.scope_authority.build_dispatch_context(
        current=snapshot,
        attempt=SimpleNamespace(execution_attempt_id="attempt-stockroom"),
        profile=profile,
        scenario_id="stockroom-s1-normal",
        operation_id="tool-operation",
        provider_call_id=CANDIDATE.call_id,
    )
    definition, arguments, fingerprint = broker.validate_candidate(
        CANDIDATE,
        mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        profile_id=profile.profile_id,
        scenario_id="stockroom-s1-normal",
        dispatch_context=context,
    )
    assert arguments == {}
    identity = ":".join(
        (
            public.registry.registry_id,
            public.registry.version,
            definition.tool_id,
            definition.schema_version,
            definition.dispatcher_version,
        )
    )
    provider_authority = ProviderToolResourceAuthority(
        allowed_resource_identities=frozenset({identity}),
        allowed_profile_ids=frozenset({profile.profile_id}),
        allowed_scenarios=frozenset({"stockroom-s1-normal"}),
        allowed_modes=frozenset({RuntimeMode.PUBLIC_BOUNDED_LIVE}),
    )
    policy = SecurityPolicy(
        luna_permission_profiles(),
        provider_tool_policy=provider_authority,
        stockroom_policy=public.scope_authority,
    )
    selector = ProviderToolSelectorRequest(
        ResourceDomain.TOOL.value,
        identity,
        "owner",
        snapshot.run_id,
        "attempt-stockroom",
        snapshot.state,
        snapshot.state_version,
        RuntimeMode.PUBLIC_BOUNDED_LIVE,
        profile.profile_id,
        profile.version,
        "stockroom-s1-normal",
        fingerprint,
    )
    attestation = provider_authority.attest(selector)
    tool_scope = ResourceScope(ResourceDomain.TOOL, identity)
    stockroom_context = public.scope_authority.issue_context(
        scope=tool_scope,
        operation_fingerprint=fingerprint,
    )
    grant = policy.issue_resource_grant(
        mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        profile_version="p1-3-v2",
        scenario_id="stockroom-s1-normal",
        principal="owner",
        run_id=snapshot.run_id,
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=tool_scope,
        selector_attestation_ref=attestation.attestation_id,
        selector_request=selector,
        operation_fingerprint=fingerprint,
        stockroom_context=stockroom_context,
    )
    permission = PermissionRequest(
        "owner",
        snapshot.run_id,
        RuntimeMode.PUBLIC_BOUNDED_LIVE,
        snapshot,
        snapshot,
        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        tool_scope,
        grant,
        "p1-3-v2",
        "stockroom-s1-normal",
        *(AuthorityStatus.GRANTED for _ in range(5)),
        AuthorityStatus.NOT_APPLICABLE,
    )
    capability = policy.issue_capability(policy.evaluate(permission), permission)
    assert capability is not None
    requirement = CapabilityConsumeRequest(
        capability,
        "owner",
        RuntimeMode.PUBLIC_BOUNDED_LIVE,
        snapshot,
        "p1-3-v2",
        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        tool_scope,
        attestation.attestation_id,
        fingerprint,
    )
    prepared = broker.prepare_dispatch(
        CANDIDATE,
        mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        profile_id=profile.profile_id,
        scenario_id="stockroom-s1-normal",
        capabilities=(requirement,),
        dispatch_context=context,
    )
    return public, broker, prepared, public.dispatcher(policy), policy


def test_public_luna_uses_fixed_receipt_backed_dispatch_without_ambient_io(monkeypatch):
    public, broker, prepared, dispatcher, policy = composition()
    consumed = broker.consume_prepared(prepared, policy=policy, secret_lease_authority=None)

    def forbidden(*_args, **_kwargs):
        raise AssertionError("ambient I/O path was reached")

    monkeypatch.setattr("shutil.which", forbidden)
    monkeypatch.setattr("subprocess.run", forbidden)
    monkeypatch.setattr("subprocess.Popen", forbidden)
    monkeypatch.setattr("socket.socket", forbidden)
    monkeypatch.setattr("socket.create_connection", forbidden)
    result = broker.dispatch_prepared(consumed, dispatcher=dispatcher, secret_resolver=None)

    assert result.output == STOCKROOM_SUMMARY
    assert result.output is not STOCKROOM_SUMMARY
    assert result.result_hash == canonical_sha256(STOCKROOM_SUMMARY)
    assert dispatcher.invocation_count == 1
    assert dispatcher.last_consumed_domains == (ResourceDomain.TOOL,)
    assert public.registry.tools["stockroom_summary"].underlying_resource_requirements == ()
    assert public.registry.tools["stockroom_summary"].secret_requirement is None
    with pytest.raises(UnknownToolOutcome, match="PUBLIC_STOCKROOM_TOOL_RECEIPT_DENIED"):
        broker.dispatch_prepared(consumed, dispatcher=dispatcher, secret_resolver=None)
    assert dispatcher.invocation_count == 1


def test_public_fixed_dispatch_rejects_forged_receipt():
    _, broker, prepared, dispatcher, policy = composition()
    consumed = broker.consume_prepared(prepared, policy=policy, secret_lease_authority=None)
    forged = replace(consumed.receipts[0], receipt_id="forged-receipt")
    tampered = ConsumedToolDispatch(
        consumed.prepared,
        consumed.secret_lease,
        (forged,),
        consumed.dispatch_identity,
    )
    with pytest.raises(UnknownToolOutcome, match="PUBLIC_STOCKROOM_TOOL_RECEIPT_DENIED"):
        broker.dispatch_prepared(tampered, dispatcher=dispatcher, secret_resolver=None)
    assert dispatcher.invocation_count == 0


@pytest.mark.parametrize(
    ("candidate", "mode", "profile_id", "scenario_id", "reason"),
    [
        (
            ToolCallCandidate("stockroom_summary", '{"path":"/tmp"}', "call-extra"),
            RuntimeMode.PUBLIC_BOUNDED_LIVE,
            "public-live-luna-v1",
            "stockroom-s1-normal",
            "TOOL_SCHEMA_DENIED",
        ),
        (
            CANDIDATE,
            RuntimeMode.OWNER_SELF_DOGFOOD,
            "public-live-luna-v1",
            "stockroom-s1-normal",
            "TOOL_CONTEXT_DENIED",
        ),
        (
            CANDIDATE,
            RuntimeMode.PUBLIC_BOUNDED_LIVE,
            "foreign-profile",
            "stockroom-s1-normal",
            "TOOL_CONTEXT_DENIED",
        ),
        (
            CANDIDATE,
            RuntimeMode.PUBLIC_BOUNDED_LIVE,
            "public-live-luna-v1",
            "foreign-scenario",
            "TOOL_SCENARIO_DENIED",
        ),
    ],
)
def test_public_fixed_tool_denies_non_exact_contract(
    candidate, mode, profile_id, scenario_id, reason
):
    public, broker, prepared, _, _ = composition()
    with pytest.raises(ValueError, match=reason):
        broker.validate_candidate(
            candidate,
            mode=mode,
            profile_id=profile_id,
            scenario_id=scenario_id,
            dispatch_context=prepared.dispatch_context,
        )
    assert public.registry.tools["stockroom_summary"].underlying_resource_domains == frozenset()


@pytest.mark.parametrize(
    "domain",
    [ResourceDomain.PROCESS, ResourceDomain.FILESYSTEM, ResourceDomain.NETWORK],
)
def test_public_stockroom_cannot_issue_ambient_resource_grant(domain):
    public, _, prepared, _, policy = composition()
    scope = ResourceScope(domain, f"denied:{domain.value.lower()}")
    grant = policy.issue_resource_grant(
        mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        profile_version="p1-3-v2",
        scenario_id="stockroom-s1-normal",
        principal="owner",
        run_id=prepared.dispatch_context.work_run_id,
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=scope,
        operation_fingerprint=prepared.fingerprint,
        stockroom_context=public.scope_authority.context,
    )
    assert grant is None
