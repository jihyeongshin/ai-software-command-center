from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from types import MappingProxyType

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
from aiscc.providers.models import (
    ProviderToolSelectorRequest,
    ResourceRequirement,
    ToolCallCandidate,
    ToolDefinition,
    ToolOutputRef,
    ToolRegistry,
    canonical_sha256,
)
from aiscc.providers.profiles import load_tool_registry
from aiscc.providers.tools import ToolRegistryBroker
from aiscc.security.capability import CapabilityConsumeRequest
from aiscc.security.policy import SecurityPolicy, default_profiles


class RecordingDispatcher:
    def __init__(self, fingerprint: str) -> None:
        self.calls = 0
        self._fingerprint = fingerprint

    def dispatch(
        self,
        definition: ToolDefinition,
        arguments: dict[str, object],
        *,
        secret: str | None = None,
    ) -> ToolOutputRef:
        assert secret is None
        self.calls += 1
        assert definition.tool_id == "synthetic_lookup"
        assert arguments == {"key": "aiscc-fixed-key"}
        output = {"value": "fixed"}
        return ToolOutputRef(
            "tool-output",
            "operation",
            self._fingerprint,
            canonical_sha256(output),
            output,
        )


def test_exact_tool_registry_and_argument_fingerprint() -> None:
    broker = ToolRegistryBroker(load_tool_registry(Path("config/providers/tool-registry.v1.toml")))
    definition, arguments, fingerprint = broker.validate_candidate(
        ToolCallCandidate("synthetic_lookup", '{"key":"aiscc-fixed-key"}', "call-1"),
        mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        profile_id="fake-openai-responses-v1",
        scenario_id="p1-5-fixed-synthetic",
    )
    assert definition.tool_id == "synthetic_lookup"
    assert arguments == {"key": "aiscc-fixed-key"}
    assert len(fingerprint) == 64


@pytest.mark.parametrize(
    "candidate",
    [
        ToolCallCandidate("unknown", "{}", "call-1"),
        ToolCallCandidate("synthetic_lookup", '{"key":"wrong"}', "call-1"),
        ToolCallCandidate(
            "synthetic_lookup", '{"key":"aiscc-fixed-key","url":"https://bad"}', "call-1"
        ),
    ],
)
def test_unknown_schema_invalid_and_injection_arguments_deny(candidate: ToolCallCandidate) -> None:
    broker = ToolRegistryBroker(load_tool_registry(Path("config/providers/tool-registry.v1.toml")))
    with pytest.raises(ValueError):
        broker.validate_candidate(
            candidate,
            mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
            profile_id="fake-openai-responses-v1",
            scenario_id="p1-5-fixed-synthetic",
        )


def test_tool_dispatch_requires_exact_tool_capability_and_argument_fingerprint() -> None:
    broker = ToolRegistryBroker(load_tool_registry(Path("config/providers/tool-registry.v1.toml")))
    candidate = ToolCallCandidate("synthetic_lookup", '{"key":"aiscc-fixed-key"}', "call-1")
    definition, _, fingerprint = broker.validate_candidate(
        candidate,
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        profile_id="fake-openai-responses-v1",
        scenario_id="p1-5-fixed-synthetic",
    )
    dispatcher = RecordingDispatcher(fingerprint)
    policy = SecurityPolicy(default_profiles())
    with pytest.raises(ValueError, match="UNDERLYING_CAPABILITY_DENIED"):
        broker.dispatch_candidate(
            candidate,
            mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            profile_id="fake-openai-responses-v1",
            scenario_id="p1-5-fixed-synthetic",
            policy=policy,
            capabilities=(),
            dispatcher=dispatcher,
        )
    assert dispatcher.calls == broker.invocation_count == 0

    resource_identity = (
        f"{broker.registry.registry_id}:{broker.registry.version}:{definition.tool_id}:"
        f"{definition.schema_version}:{definition.dispatcher_version}"
    )
    authority = ProviderToolResourceAuthority(
        allowed_resource_identities=frozenset({resource_identity}),
        allowed_profile_ids=frozenset({"fake-openai-responses-v1"}),
        allowed_scenarios=frozenset({"p1-5-fixed-synthetic"}),
        allowed_modes=frozenset({RuntimeMode.OWNER_SELF_DOGFOOD}),
    )
    policy = SecurityPolicy(default_profiles(), provider_tool_policy=authority)
    selector = ProviderToolSelectorRequest(
        "TOOL",
        resource_identity,
        "owner",
        "run",
        "attempt",
        WorkflowState.RUNNING,
        2,
        RuntimeMode.OWNER_SELF_DOGFOOD,
        "fake-openai-responses-v1",
        "1",
        "p1-5-fixed-synthetic",
        fingerprint,
    )
    attestation = authority.attest(selector)
    scope = ResourceScope(ResourceDomain.TOOL, resource_identity)
    snapshot = WorkflowSnapshot("run", WorkflowState.RUNNING, 2)
    grant = policy.issue_resource_grant(
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        profile_version="p1-3-v2",
        scenario_id="p1-5-fixed-synthetic",
        principal="owner",
        run_id="run",
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=scope,
        selector_attestation_ref=attestation.attestation_id,
        selector_request=selector,
        operation_fingerprint=fingerprint,
    )
    permission = PermissionRequest(
        "owner",
        "run",
        RuntimeMode.OWNER_SELF_DOGFOOD,
        snapshot,
        snapshot,
        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope,
        grant,
        "p1-3-v2",
        "p1-5-fixed-synthetic",
        AuthorityStatus.GRANTED,
        AuthorityStatus.GRANTED,
        AuthorityStatus.GRANTED,
        AuthorityStatus.GRANTED,
        AuthorityStatus.GRANTED,
        AuthorityStatus.NOT_APPLICABLE,
    )
    capability = policy.issue_capability(policy.evaluate(permission), permission)
    assert capability is not None
    result = broker.dispatch_candidate(
        candidate,
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        profile_id="fake-openai-responses-v1",
        scenario_id="p1-5-fixed-synthetic",
        policy=policy,
        capabilities=(
            CapabilityConsumeRequest(
                capability,
                "owner",
                RuntimeMode.OWNER_SELF_DOGFOOD,
                snapshot,
                "p1-3-v2",
                SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
                scope,
                attestation.attestation_id,
                fingerprint,
            ),
        ),
        dispatcher=dispatcher,
    )
    assert result.argument_hash == fingerprint
    assert dispatcher.calls == broker.invocation_count == 1


def test_same_domain_wrong_underlying_resource_is_denied_before_dispatch() -> None:
    loaded = load_tool_registry(Path("config/providers/tool-registry.v1.toml"))
    base = loaded.tools["synthetic_lookup"]
    exact_scope = ResourceScope(ResourceDomain.FILESYSTEM, "workspace:server-owned-exact")
    wrong_scope = ResourceScope(ResourceDomain.FILESYSTEM, "workspace:confused-deputy")
    definition = replace(
        base,
        underlying_resource_requirements=(
            ResourceRequirement(
                exact_scope,
                SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            ),
        ),
    )
    registry = ToolRegistry(
        loaded.registry_id,
        loaded.version,
        MappingProxyType({definition.tool_id: definition}),
    )
    broker = ToolRegistryBroker(registry)
    candidate = ToolCallCandidate(
        "synthetic_lookup", '{"key":"aiscc-fixed-key"}', "call-confused-deputy"
    )
    _, _, fingerprint = broker.validate_candidate(
        candidate,
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        profile_id="fake-openai-responses-v1",
        scenario_id="p1-5-fixed-synthetic",
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
    authority = ProviderToolResourceAuthority(
        allowed_resource_identities=frozenset({tool_identity}),
        allowed_profile_ids=frozenset({"fake-openai-responses-v1"}),
        allowed_scenarios=frozenset({"p1-5-fixed-synthetic"}),
        allowed_modes=frozenset({RuntimeMode.OWNER_SELF_DOGFOOD}),
    )
    policy = SecurityPolicy(default_profiles(), provider_tool_policy=authority)
    snapshot = WorkflowSnapshot("run-confused", WorkflowState.RUNNING, 2)
    selector = ProviderToolSelectorRequest(
        "TOOL",
        tool_identity,
        "owner",
        snapshot.run_id,
        "attempt",
        snapshot.state,
        snapshot.state_version,
        RuntimeMode.OWNER_SELF_DOGFOOD,
        "fake-openai-responses-v1",
        "1",
        "p1-5-fixed-synthetic",
        fingerprint,
    )
    attestation = authority.attest(selector)

    def capability_for(
        scope: ResourceScope,
        selector_ref: str | None,
        selector_request: object | None,
    ) -> CapabilityConsumeRequest:
        grant = policy.issue_resource_grant(
            mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            profile_version="p1-3-v2",
            scenario_id="p1-5-fixed-synthetic",
            principal="owner",
            run_id=snapshot.run_id,
            action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            scope=scope,
            selector_attestation_ref=selector_ref,
            selector_request=selector_request,
            operation_fingerprint=fingerprint,
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
            "p1-5-fixed-synthetic",
            AuthorityStatus.GRANTED,
            AuthorityStatus.GRANTED,
            AuthorityStatus.GRANTED,
            AuthorityStatus.GRANTED,
            AuthorityStatus.GRANTED,
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

    tool_requirement = capability_for(
        ResourceScope(ResourceDomain.TOOL, tool_identity),
        attestation.attestation_id,
        selector,
    )
    wrong_requirement = capability_for(wrong_scope, None, None)
    dispatcher = RecordingDispatcher(fingerprint)
    with pytest.raises(ValueError, match="UNDERLYING_CAPABILITY_DENIED"):
        broker.dispatch_candidate(
            candidate,
            mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            profile_id="fake-openai-responses-v1",
            scenario_id="p1-5-fixed-synthetic",
            policy=policy,
            capabilities=(tool_requirement, wrong_requirement),
            dispatcher=dispatcher,
        )
    assert dispatcher.calls == 0
    assert tool_requirement.capability is not None
    still_available = policy.consume_capability(
        tool_requirement.capability,
        principal=tool_requirement.principal,
        current_mode=tool_requirement.current_mode,
        current=tool_requirement.current,
        profile_version=tool_requirement.profile_version,
        action=tool_requirement.action,
        scope=tool_requirement.scope,
        selector_attestation_ref=tool_requirement.selector_attestation_ref,
        operation_fingerprint=tool_requirement.operation_fingerprint,
    )
    assert still_available.allowed
