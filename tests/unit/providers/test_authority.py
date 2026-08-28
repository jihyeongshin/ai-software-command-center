from __future__ import annotations

import hashlib
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from typing import Any

import pytest

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
    ProviderToolSelectorRequest,
    SecretResolutionLease,
    SecretUseSelectorRequest,
)
from aiscc.security.capability import CapabilityConsumeRequest
from aiscc.security.policy import SecurityPolicy, default_profiles


def _provider_request(fingerprint: str = "a" * 64) -> ProviderToolSelectorRequest:
    return ProviderToolSelectorRequest(
        "PROVIDER",
        "profile:1:openai:model:responses-v1",
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


def _secret_request(fingerprint: str = "a" * 64) -> SecretUseSelectorRequest:
    return SecretUseSelectorRequest(
        "secret-ref:synthetic-openai-fixture",
        "PROVIDER_API",
        "RESPONSES_CREATE",
        "local-fake",
        "profile:1:openai:model:responses-v1",
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


def _provider_authority(**kwargs: Any) -> ProviderToolResourceAuthority:
    return ProviderToolResourceAuthority(
        allowed_resource_identities=frozenset({_provider_request().canonical_resource_identity}),
        allowed_profile_ids=frozenset({_provider_request().profile_id}),
        allowed_scenarios=frozenset({_provider_request().scenario_id}),
        allowed_modes=frozenset({_provider_request().runtime_mode}),
        **kwargs,
    )


def _secret_authority(**kwargs: Any) -> SecretUseAuthority:
    return SecretUseAuthority(
        allowed_secret_refs=frozenset({_secret_request().secret_ref}),
        allowed_profile_ids=frozenset({_secret_request().profile_id}),
        allowed_scenarios=frozenset({_secret_request().scenario_id}),
        allowed_destinations=frozenset({_secret_request().destination}),
        allowed_modes=frozenset({_secret_request().runtime_mode}),
        **kwargs,
    )


def _permission(
    policy: SecurityPolicy,
    scope: ResourceScope,
    selector_ref: str,
    selector_request: object,
    fingerprint: str = "a" * 64,
) -> PermissionRequest:
    snapshot = WorkflowSnapshot("run", WorkflowState.RUNNING, 2)
    grant = policy.issue_resource_grant(
        mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        profile_version="p1-3-v2",
        scenario_id="p1-5-fixed-synthetic",
        principal="owner",
        run_id="run",
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=scope,
        selector_attestation_ref=selector_ref,
        selector_request=selector_request,
        operation_fingerprint=fingerprint,
    )
    return PermissionRequest(
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


def test_missing_authority_and_forged_selector_fail_closed() -> None:
    scope = ResourceScope(ResourceDomain.PROVIDER, "profile:1:openai:model:responses-v1")
    request = _provider_request()
    policy = SecurityPolicy(default_profiles())
    assert (
        policy.issue_resource_grant(
            mode=RuntimeMode.OWNER_SELF_DOGFOOD,
            profile_version="p1-3-v2",
            scenario_id="p1-5-fixed-synthetic",
            principal="owner",
            run_id="run",
            action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            scope=scope,
            selector_attestation_ref="forged",
            selector_request=request,
            operation_fingerprint="a" * 64,
        )
        is None
    )


def test_provider_and_secret_are_independent_and_atomically_consumed() -> None:
    provider_authority = _provider_authority()
    secret_authority = _secret_authority()
    policy = SecurityPolicy(
        default_profiles(),
        provider_tool_policy=provider_authority,
        secret_use_policy=secret_authority,
    )
    provider_request = _provider_request()
    secret_request = _secret_request()
    provider_attestation = provider_authority.attest(provider_request)
    secret_attestation = secret_authority.attest(secret_request)
    provider_scope = ResourceScope(
        ResourceDomain.PROVIDER, provider_request.canonical_resource_identity
    )
    secret_scope = ResourceScope(
        ResourceDomain.SECRET,
        "PROVIDER_API:61c27eb152caf4004eb7a36ad6c12dcdbba04903fdff8307da5b5414b69b5076",
    )
    provider_permission = _permission(
        policy, provider_scope, provider_attestation.attestation_id, provider_request
    )
    secret_permission = _permission(
        policy, secret_scope, secret_attestation.attestation_id, secret_request
    )
    assert provider_permission.resource_grant is not None
    assert secret_permission.resource_grant is not None
    provider_decision = policy.evaluate(provider_permission)
    secret_decision = policy.evaluate(secret_permission)
    provider_capability = policy.issue_capability(provider_decision, provider_permission)
    secret_capability = policy.issue_capability(secret_decision, secret_permission)
    assert provider_capability is not None and secret_capability is not None
    current = WorkflowSnapshot("run", WorkflowState.RUNNING, 2)
    wrong_secret = CapabilityConsumeRequest(
        secret_capability,
        "owner",
        RuntimeMode.OWNER_SELF_DOGFOOD,
        current,
        "p1-3-v2",
        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        secret_scope,
        "wrong",
        "a" * 64,
    )
    provider_use = CapabilityConsumeRequest(
        provider_capability,
        "owner",
        RuntimeMode.OWNER_SELF_DOGFOOD,
        current,
        "p1-3-v2",
        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        provider_scope,
        provider_attestation.attestation_id,
        "a" * 64,
    )
    denied = policy.consume_capabilities_atomically((provider_use, wrong_secret))
    assert not denied[0].allowed
    secret_use = CapabilityConsumeRequest(
        secret_capability,
        "owner",
        RuntimeMode.OWNER_SELF_DOGFOOD,
        current,
        "p1-3-v2",
        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        secret_scope,
        secret_attestation.attestation_id,
        "a" * 64,
    )
    admitted = policy.consume_capabilities_atomically((provider_use, secret_use))
    assert [item.consumed_use_count for item in admitted] == [1, 1]


def test_selector_attestations_are_unknown_safe_single_use_revocable_and_expiring() -> None:
    current = [datetime(2026, 8, 28, tzinfo=UTC)]
    authority = _provider_authority(ttl_seconds=2, clock=lambda: current[0])
    request = _provider_request()
    assert not authority.verify("unknown", request)
    single_use = authority.attest(request)
    assert authority.verify(single_use.attestation_id, request)
    assert not authority.verify(single_use.attestation_id, request)
    revoked = authority.attest(request)
    authority.revoke(revoked.attestation_id)
    assert not authority.verify(revoked.attestation_id, request)
    expired = authority.attest(request)
    current[0] += timedelta(seconds=2)
    assert not authority.verify(expired.attestation_id, request)

    secret = _secret_authority(ttl_seconds=2, clock=lambda: current[0])
    secret_attestation = secret.attest(_secret_request())
    secret.revoke(secret_attestation.attestation_id)
    assert not secret.verify(secret_attestation.attestation_id, _secret_request())


def test_server_owned_authority_rejects_arbitrary_provider_tool_and_secret_selection() -> None:
    provider = _provider_authority()
    with pytest.raises(ValueError, match="server-owned"):
        provider.attest(
            replace(
                _provider_request(),
                canonical_resource_identity="arbitrary-provider:model",
            )
        )
    with pytest.raises(ValueError, match="server-owned"):
        provider.attest(replace(_provider_request(), profile_id="arbitrary-profile"))
    secret = _secret_authority()
    with pytest.raises(ValueError, match="server-owned"):
        secret.attest(replace(_secret_request(), secret_ref="secret-ref:caller-selected"))
    with pytest.raises(ValueError, match="server-owned"):
        secret.attest(replace(_secret_request(), destination="https://external.example"))


def test_secret_resolution_requires_unforgeable_consumed_secret_lease() -> None:
    now = [datetime(2026, 8, 28, tzinfo=UTC)]
    provider_authority = _provider_authority()
    secret_authority = _secret_authority()
    policy = SecurityPolicy(
        default_profiles(),
        provider_tool_policy=provider_authority,
        secret_use_policy=secret_authority,
    )
    secret_request = _secret_request()
    secret_attestation = secret_authority.attest(secret_request)
    identity_hash = hashlib.sha256(secret_request.secret_ref.encode()).hexdigest()
    secret_scope = ResourceScope(
        ResourceDomain.SECRET,
        f"{secret_request.secret_class}:{identity_hash}",
    )
    secret_permission = _permission(
        policy,
        secret_scope,
        secret_attestation.attestation_id,
        secret_request,
    )
    secret_capability = policy.issue_capability(
        policy.evaluate(secret_permission), secret_permission
    )
    assert secret_capability is not None
    consume_request = CapabilityConsumeRequest(
        secret_capability,
        "owner",
        RuntimeMode.OWNER_SELF_DOGFOOD,
        WorkflowSnapshot("run", WorkflowState.RUNNING, 2),
        "p1-3-v2",
        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        secret_scope,
        secret_attestation.attestation_id,
        "a" * 64,
    )
    uses, receipts = policy.consume_capabilities_atomically_with_receipts((consume_request,))
    assert uses[0].allowed and len(receipts) == 1
    lease_authority = SecretResolutionLeaseAuthority(
        policy.verify_consumption_receipt,
        ttl_seconds=2,
        clock=lambda: now[0],
    )
    resolver = LeaseBoundSecretResolver(
        lease_authority,
        {secret_request.secret_ref: "SYNTHETIC_CANARY"},
    )
    lease = lease_authority.issue(receipts[0], consume_request, secret_request)
    with pytest.raises(ValueError, match="LEASE_DENIED"):
        resolver.resolve(secret_request.secret_ref)  # type: ignore[arg-type]
    forged = replace(lease, lease_id="forged-lease")
    with pytest.raises(ValueError, match="LEASE_DENIED"):
        resolver.resolve(forged)
    assert resolver.resolve(lease) == "SYNTHETIC_CANARY"
    with pytest.raises(ValueError, match="LEASE_DENIED"):
        resolver.resolve(lease)
    resolver.close(lease)
    assert resolver.invocation_count == 1

    provider_request = replace(_provider_request(), operation_fingerprint="b" * 64)
    provider_attestation = provider_authority.attest(provider_request)
    provider_scope = ResourceScope(
        ResourceDomain.PROVIDER,
        provider_request.canonical_resource_identity,
    )
    provider_permission = _permission(
        policy,
        provider_scope,
        provider_attestation.attestation_id,
        provider_request,
        "b" * 64,
    )
    provider_capability = policy.issue_capability(
        policy.evaluate(provider_permission), provider_permission
    )
    assert provider_capability is not None
    provider_consume = CapabilityConsumeRequest(
        provider_capability,
        "owner",
        RuntimeMode.OWNER_SELF_DOGFOOD,
        WorkflowSnapshot("run", WorkflowState.RUNNING, 2),
        "p1-3-v2",
        SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        provider_scope,
        provider_attestation.attestation_id,
        "b" * 64,
    )
    _, provider_receipts = policy.consume_capabilities_atomically_with_receipts((provider_consume,))
    with pytest.raises(ValueError, match="SECRET_CONSUMPTION_RECEIPT_DENIED"):
        lease_authority.issue(provider_receipts[0], provider_consume, secret_request)
    assert resolver.invocation_count == 1

    def fresh_secret_lease(fingerprint: str) -> SecretResolutionLease:
        request = replace(
            _secret_request(fingerprint),
            operation_id=f"operation-{fingerprint[0]}",
        )
        attestation = secret_authority.attest(request)
        permission = _permission(
            policy,
            secret_scope,
            attestation.attestation_id,
            request,
            fingerprint,
        )
        capability = policy.issue_capability(policy.evaluate(permission), permission)
        assert capability is not None
        consume = CapabilityConsumeRequest(
            capability,
            "owner",
            RuntimeMode.OWNER_SELF_DOGFOOD,
            WorkflowSnapshot("run", WorkflowState.RUNNING, 2),
            "p1-3-v2",
            SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
            secret_scope,
            attestation.attestation_id,
            fingerprint,
        )
        _, new_receipts = policy.consume_capabilities_atomically_with_receipts((consume,))
        return lease_authority.issue(new_receipts[0], consume, request)

    expired = fresh_secret_lease("c" * 64)
    now[0] += timedelta(seconds=2)
    with pytest.raises(ValueError, match="LEASE_DENIED"):
        resolver.resolve(expired)
    revoked = fresh_secret_lease("d" * 64)
    lease_authority.revoke(revoked)
    with pytest.raises(ValueError, match="LEASE_DENIED"):
        resolver.resolve(revoked)
    closed = fresh_secret_lease("e" * 64)
    lease_authority.close(closed)
    with pytest.raises(ValueError, match="LEASE_DENIED"):
        resolver.resolve(closed)
