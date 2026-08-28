from __future__ import annotations

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.providers.authority import ProviderToolResourceAuthority
from aiscc.providers.models import ProviderToolSelectorRequest
from aiscc.security.policy import SecurityPolicy, default_profiles


def test_wrong_profile_model_tool_mode_scenario_or_fingerprint_denies_before_grant() -> None:
    request = ProviderToolSelectorRequest(
        "TOOL",
        "registry:1:synthetic_lookup:1:synthetic-v1",
        "owner",
        "run",
        "attempt",
        WorkflowState.RUNNING,
        2,
        RuntimeMode.OWNER_SELF_DOGFOOD,
        "fake-openai-responses-v1",
        "1",
        "p1-5-fixed-synthetic",
        "a" * 64,
    )
    authority = ProviderToolResourceAuthority(
        allowed_resource_identities=frozenset({request.canonical_resource_identity}),
        allowed_profile_ids=frozenset({request.profile_id}),
        allowed_scenarios=frozenset({request.scenario_id}),
        allowed_modes=frozenset({request.runtime_mode}),
    )
    attestation = authority.attest(request)
    policy = SecurityPolicy(default_profiles(), provider_tool_policy=authority)
    scope = ResourceScope(ResourceDomain.TOOL, request.canonical_resource_identity)
    wrong = ProviderToolSelectorRequest(
        request.domain,
        request.canonical_resource_identity,
        request.principal,
        request.work_run_id,
        request.execution_attempt_id,
        request.state,
        request.state_version,
        request.runtime_mode,
        request.profile_id,
        request.profile_version,
        "wrong-scenario",
        request.operation_fingerprint,
    )
    assert (
        policy.issue_resource_grant(
            mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            profile_version="p1-3-v2",
            scenario_id="p1-5-fixed-synthetic",
            principal="owner",
            run_id="run",
            action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            scope=scope,
            selector_attestation_ref=attestation.attestation_id,
            selector_request=wrong,
            operation_fingerprint="a" * 64,
        )
        is None
    )
