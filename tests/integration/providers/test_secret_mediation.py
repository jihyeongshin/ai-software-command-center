from __future__ import annotations

import os
import sys
from pathlib import Path
from types import MappingProxyType
from uuid import uuid4

from aiscc.contracts.security import (
    AuthorityStatus,
    PermissionRequest,
    ResourceDomain,
    ResourceScope,
    SecurityActionClass,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.providers.authority import (
    LeaseBoundSecretResolver,
    ProviderToolResourceAuthority,
    SecretResolutionLeaseAuthority,
    SecretUseAuthority,
)
from aiscc.providers.models import (
    ExecutionAttemptRef,
    ExecutionOperationOutcome,
    ExecutionStatus,
    ProviderCall,
    ProviderResult,
    ProviderToolSelectorRequest,
    SecretUseSelectorRequest,
    canonical_sha256,
)
from aiscc.providers.profiles import load_provider_profile
from aiscc.providers.service import AgentExecutionService
from aiscc.security.capability import Capability, CapabilityConsumeRequest
from aiscc.security.policy import SecurityPolicy, default_profiles


class LocalAdapter:
    def __init__(self, canary: str) -> None:
        self.canary = canary
        self.calls = 0

    def call(self, call: ProviderCall, *, secret: str) -> ProviderResult:
        assert secret == self.canary
        self.calls += 1
        return ProviderResult(
            call.operation_id,
            "completed",
            ExecutionOperationOutcome.PROVIDER_COMPLETED,
            "local-response",
            (),
            "SAFE_OUTPUT",
            None,
            MappingProxyType({}),
            None,
            canonical_sha256({"result": "SAFE_OUTPUT"}),
        )


class FixedAuthorityReader:
    def load(
        self, *, work_run_id: str, execution_attempt_id: str
    ) -> tuple[WorkflowSnapshot, ExecutionAttemptRef]:
        return (
            WorkflowSnapshot(work_run_id, WorkflowState.RUNNING, 2),
            ExecutionAttemptRef(
                execution_attempt_id,
                work_run_id,
                "task",
                "1",
                WorkflowState.RUNNING,
                2,
                2,
                ExecutionStatus.RUNNING,
                "issuer:p1-5:test",
            ),
        )


def _permission(
    policy: SecurityPolicy,
    scope: ResourceScope,
    ref: str,
    selector: object,
    fingerprint: str,
) -> tuple[PermissionRequest, Capability]:
    snapshot = WorkflowSnapshot("run", WorkflowState.RUNNING, 2)
    grant = policy.issue_resource_grant(
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        profile_version="p1-3-v2",
        scenario_id="p1-5-fixed-synthetic",
        principal="owner",
        run_id="run",
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=scope,
        selector_attestation_ref=ref,
        selector_request=selector,
        operation_fingerprint=fingerprint,
    )
    request = PermissionRequest(
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
    capability = policy.issue_capability(policy.evaluate(request), request)
    assert capability is not None
    return request, capability


def test_secret_is_resolved_only_after_independent_provider_and_secret_consumption() -> None:
    fingerprint = "a" * 64
    profile = load_provider_profile(
        Path("config/providers/provider-profiles.v1.toml"), "fake-openai-responses-v1"
    )
    provider_authority = ProviderToolResourceAuthority(
        allowed_resource_identities=frozenset({profile.provider_resource_identity}),
        allowed_profile_ids=frozenset({"fake-openai-responses-v1"}),
        allowed_scenarios=frozenset({"p1-5-fixed-synthetic"}),
        allowed_modes=frozenset({RuntimeMode.OWNER_SELF_DOGFOOD}),
    )
    secret_authority = SecretUseAuthority(
        allowed_secret_refs=frozenset({"secret-ref:synthetic-openai-fixture"}),
        allowed_profile_ids=frozenset({"fake-openai-responses-v1"}),
        allowed_scenarios=frozenset({"p1-5-fixed-synthetic"}),
        allowed_destinations=frozenset({"local-fake"}),
        allowed_modes=frozenset({RuntimeMode.OWNER_SELF_DOGFOOD}),
    )
    policy = SecurityPolicy(
        default_profiles(),
        provider_tool_policy=provider_authority,
        secret_use_policy=secret_authority,
    )
    provider_selector = ProviderToolSelectorRequest(
        "PROVIDER",
        profile.provider_resource_identity,
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
    secret_selector = SecretUseSelectorRequest(
        "secret-ref:synthetic-openai-fixture",
        "PROVIDER_API",
        "RESPONSES_CREATE",
        "local-fake",
        profile.provider_resource_identity,
        "responses-v1",
        "owner",
        "run",
        "attempt",
        "operation",
        WorkflowState.RUNNING,
        2,
        RuntimeMode.OWNER_SELF_DOGFOOD,
        "fake-openai-responses-v1",
        "1",
        "p1-5-fixed-synthetic",
        fingerprint,
    )
    provider_ref = provider_authority.attest(provider_selector).attestation_id
    secret_ref = secret_authority.attest(secret_selector).attestation_id
    provider_scope = ResourceScope(ResourceDomain.PROVIDER, profile.provider_resource_identity)
    secret_scope = ResourceScope(ResourceDomain.SECRET, profile.secret_resource_identity)
    _, provider_capability = _permission(
        policy, provider_scope, provider_ref, provider_selector, fingerprint
    )
    _, secret_capability = _permission(
        policy, secret_scope, secret_ref, secret_selector, fingerprint
    )
    snapshot = WorkflowSnapshot("run", WorkflowState.RUNNING, 2)
    requirements = (
        CapabilityConsumeRequest(
            provider_capability,
            "owner",
            RuntimeMode.OWNER_SELF_DOGFOOD,
            snapshot,
            "p1-3-v2",
            SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            provider_scope,
            provider_ref,
            fingerprint,
        ),
        CapabilityConsumeRequest(
            secret_capability,
            "owner",
            RuntimeMode.OWNER_SELF_DOGFOOD,
            snapshot,
            "p1-3-v2",
            SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            secret_scope,
            secret_ref,
            fingerprint,
        ),
    )
    canary = f"AISCC_{uuid4().hex}_SYNTHETIC_SECRET"
    lease_authority = SecretResolutionLeaseAuthority(policy.verify_consumption_receipt)
    resolver = LeaseBoundSecretResolver(
        lease_authority,
        {"secret-ref:synthetic-openai-fixture": canary},
    )
    adapter = LocalAdapter(canary)
    service = AgentExecutionService(
        policy=policy,
        adapter=adapter,
        secret_resolver=resolver,
        authority_reader=FixedAuthorityReader(),
        secret_lease_authority=lease_authority,
    )
    call = ProviderCall(
        "operation",
        fingerprint,
        "attempt",
        "run",
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
    result = service.execute_provider(
        call,
        capabilities=requirements,
        secret_request=secret_selector,
    )
    assert adapter.calls == 1 and resolver.invocation_count == 1
    assert canary not in repr((call, result, service.counters))
    assert canary not in repr((dict(os.environ), sys.argv))
    for path in Path(".").rglob("*"):
        if path.is_file() and ".venv" not in path.parts and "__pycache__" not in path.parts:
            assert canary.encode() not in path.read_bytes(), path
