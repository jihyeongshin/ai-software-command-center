"""Operator-only one-request proof for the sealed hosted Luna credential path."""

from __future__ import annotations

import hashlib
import os
from collections.abc import Mapping
from types import MappingProxyType
from typing import Any

from aiscc.contracts.security import (
    AuthorityStatus,
    PermissionRequest,
    ResourceDomain,
    ResourceScope,
    SecurityActionClass,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.providers.authority import (
    ProviderToolResourceAuthority,
    SecretResolutionLeaseAuthority,
    SecretUseAuthority,
)
from aiscc.providers.hosted_secret import (
    SECRET_VARIABLE,
    HostedOpenAISecretResolver,
)
from aiscc.providers.models import (
    ExecutionAttemptRef,
    ExecutionOperationOutcome,
    ExecutionStatus,
    ProviderCall,
    ProviderToolSelectorRequest,
    SecretResolutionLease,
    SecretUseSelectorRequest,
    canonical_sha256,
)
from aiscc.providers.openai_responses import OpenAIResponsesAdapter
from aiscc.providers.service import AgentExecutionService
from aiscc.public_live.luna_profile import bind_call, hosted_luna_profile
from aiscc.public_live.provider_authority import LunaScopeAuthority, luna_permission_profiles
from aiscc.security.capability import Capability, CapabilityConsumeRequest
from aiscc.security.policy import SecurityPolicy

_SERVICE = "aiscc-public-live-worker"
_ENVIRONMENT = "production"
_PRINCIPAL = "aiscc-public-live-worker-canary"
_RUN_ID = "public-live-real-luna-canary-v1"
_ATTEMPT_ID = "public-live-real-luna-canary-attempt-v1"
_OPERATION_ID = "public-live-real-luna-canary-operation-v1"
_SCENARIO = "stockroom-s1-normal"
_PROFILE_VERSION = "p1-3-v2"
_INPUT = (
    {
        "role": "system",
        "content": "This is a fixed synthetic Stockroom provider-readiness canary.",
    },
    {
        "role": "user",
        "content": "Reply with the single word READY. Do not call a tool.",
    },
)


class _Reader:
    def __init__(self, current: WorkflowSnapshot, attempt: ExecutionAttemptRef) -> None:
        self._current = current
        self._attempt = attempt

    def load(self, **_kwargs: Any) -> tuple[WorkflowSnapshot, ExecutionAttemptRef]:
        return self._current, self._attempt


class _ObservedResolver(HostedOpenAISecretResolver):
    def __init__(self, authority: SecretResolutionLeaseAuthority) -> None:
        super().__init__(authority)
        self.resolve_calls = 0
        self.resolved_lease: SecretResolutionLease | None = None

    def resolve(self, lease: SecretResolutionLease) -> str:
        self.resolve_calls += 1
        self.resolved_lease = lease
        return super().resolve(lease)


def _permission(
    *,
    policy: SecurityPolicy,
    scope_authority: LunaScopeAuthority,
    current: WorkflowSnapshot,
    scope: ResourceScope,
    selector_ref: str,
    selector: object,
    fingerprint: str,
) -> CapabilityConsumeRequest:
    grant = policy.issue_resource_grant(
        mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        profile_version=_PROFILE_VERSION,
        scenario_id=_SCENARIO,
        principal=_PRINCIPAL,
        run_id=_RUN_ID,
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=scope,
        selector_attestation_ref=selector_ref,
        selector_request=selector,
        operation_fingerprint=fingerprint,
        stockroom_context=scope_authority.context,
    )
    request = PermissionRequest(
        principal=_PRINCIPAL,
        run_id=_RUN_ID,
        mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        observed=current,
        authoritative=current,
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        resource_scope=scope,
        resource_grant=grant,
        profile_version=_PROFILE_VERSION,
        scenario_id=_SCENARIO,
        requester_authority=AuthorityStatus.GRANTED,
        task_scope_authority=AuthorityStatus.GRANTED,
        limit_authority=AuthorityStatus.GRANTED,
        budget_authority=AuthorityStatus.GRANTED,
        idempotency_authority=AuthorityStatus.GRANTED,
        target_control_authority=AuthorityStatus.NOT_APPLICABLE,
    )
    capability: Capability | None = policy.issue_capability(policy.evaluate(request), request)
    if capability is None:
        raise RuntimeError("CANARY_CAPABILITY_DENIED")
    return CapabilityConsumeRequest(
        capability=capability,
        principal=_PRINCIPAL,
        current_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        current=current,
        profile_version=_PROFILE_VERSION,
        action=SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        scope=scope,
        selector_attestation_ref=selector_ref,
        operation_fingerprint=fingerprint,
    )


def _compose() -> tuple[
    AgentExecutionService,
    ProviderCall,
    tuple[CapabilityConsumeRequest, ...],
    SecretUseSelectorRequest,
    OpenAIResponsesAdapter,
    _ObservedResolver,
    SecretResolutionLeaseAuthority,
]:
    profile = hosted_luna_profile()
    current = WorkflowSnapshot(_RUN_ID, WorkflowState.RUNNING, 2)
    attempt = ExecutionAttemptRef(
        execution_attempt_id=_ATTEMPT_ID,
        work_run_id=_RUN_ID,
        task_contract_id="public-live-real-luna-canary-v1",
        task_contract_version="1",
        state=WorkflowState.RUNNING,
        state_version=2,
        execution_version=1,
        status=ExecutionStatus.RUNNING,
        issuer_ref="AISCC_L8_REAL_LUNA_CANARY_V1",
        runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        project_id=profile.public_repository_resource_identity,
        provider_profile_id=profile.profile_id,
        provider_profile_version=profile.version,
        tool_registry_id=profile.tool_registry_id,
        tool_registry_version=profile.tool_registry_version,
    )
    fingerprint = canonical_sha256(
        {
            "kind": "PROVIDER_CANARY",
            "operation_id": _OPERATION_ID,
            "profile": [profile.profile_id, profile.version, profile.model_ref],
            "runtime_mode": RuntimeMode.PUBLIC_BOUNDED_LIVE.value,
            "scenario": _SCENARIO,
            "input": list(_INPUT),
        }
    )
    call = bind_call(
        ProviderCall(
            operation_id=_OPERATION_ID,
            operation_fingerprint=fingerprint,
            execution_attempt_id=_ATTEMPT_ID,
            work_run_id=_RUN_ID,
            state=WorkflowState.RUNNING,
            state_version=2,
            runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
            principal=_PRINCIPAL,
            scenario_id=_SCENARIO,
            execution_version=1,
            profile=profile,
            input_items=_INPUT,
            tools=(),
            call_ordinal=1,
        ),
        role="PRIMARY",
    )[0]
    scope_authority = LunaScopeAuthority(
        call,
        {"role": "PRIMARY", "outcome": "STARTED", "model": profile.model_ref, "effort": "low"},
        owner=_RUN_ID,
    )
    provider_authority = ProviderToolResourceAuthority(
        allowed_resource_identities=frozenset({profile.provider_resource_identity}),
        allowed_profile_ids=frozenset({profile.profile_id}),
        allowed_scenarios=frozenset({_SCENARIO}),
        allowed_modes=frozenset({RuntimeMode.PUBLIC_BOUNDED_LIVE}),
    )
    secret_authority = SecretUseAuthority(
        allowed_secret_refs=frozenset({profile.secret_ref}),
        allowed_profile_ids=frozenset({profile.profile_id}),
        allowed_scenarios=frozenset({_SCENARIO}),
        allowed_destinations=frozenset({profile.endpoint_ref}),
        allowed_modes=frozenset({RuntimeMode.PUBLIC_BOUNDED_LIVE}),
    )
    policy = SecurityPolicy(
        luna_permission_profiles(),
        stockroom_policy=scope_authority,
        provider_tool_policy=provider_authority,
        secret_use_policy=secret_authority,
    )
    provider_selector = ProviderToolSelectorRequest(
        domain="PROVIDER",
        canonical_resource_identity=profile.provider_resource_identity,
        principal=_PRINCIPAL,
        work_run_id=_RUN_ID,
        execution_attempt_id=_ATTEMPT_ID,
        state=WorkflowState.RUNNING,
        state_version=2,
        runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        profile_id=profile.profile_id,
        profile_version=profile.version,
        scenario_id=_SCENARIO,
        operation_fingerprint=fingerprint,
    )
    secret_selector = SecretUseSelectorRequest(
        secret_ref=profile.secret_ref,
        secret_class="PROVIDER_API",
        purpose="RESPONSES_CREATE",
        destination=profile.endpoint_ref,
        canonical_resource_identity=profile.provider_resource_identity,
        adapter_identity=profile.adapter_protocol_version,
        principal=_PRINCIPAL,
        work_run_id=_RUN_ID,
        execution_attempt_id=_ATTEMPT_ID,
        operation_id=_OPERATION_ID,
        state=WorkflowState.RUNNING,
        state_version=2,
        runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        profile_id=profile.profile_id,
        profile_version=profile.version,
        scenario_id=_SCENARIO,
        operation_fingerprint=fingerprint,
    )
    provider_ref = provider_authority.attest(provider_selector).attestation_id
    secret_ref = secret_authority.attest(secret_selector).attestation_id
    requirements = (
        _permission(
            policy=policy,
            scope_authority=scope_authority,
            current=current,
            scope=ResourceScope(ResourceDomain.PROVIDER, profile.provider_resource_identity),
            selector_ref=provider_ref,
            selector=provider_selector,
            fingerprint=fingerprint,
        ),
        _permission(
            policy=policy,
            scope_authority=scope_authority,
            current=current,
            scope=ResourceScope(ResourceDomain.SECRET, profile.secret_resource_identity),
            selector_ref=secret_ref,
            selector=secret_selector,
            fingerprint=fingerprint,
        ),
    )
    lease_authority = SecretResolutionLeaseAuthority(policy.verify_consumption_receipt)
    resolver = _ObservedResolver(lease_authority)
    adapter = OpenAIResponsesAdapter(hosted=True)
    service = AgentExecutionService(
        policy=policy,
        adapter=adapter,
        secret_resolver=resolver,
        authority_reader=_Reader(current, attempt),
        secret_lease_authority=lease_authority,
    )
    return (
        service,
        call,
        requirements,
        secret_selector,
        adapter,
        resolver,
        lease_authority,
    )


def _request_evidence(request: dict[str, Any] | None) -> dict[str, Any]:
    if request is None:
        return {}
    return {
        "model": request.get("model"),
        "service_tier": request.get("service_tier"),
        "reasoning_effort": (request.get("reasoning") or {}).get("effort"),
        "store": request.get("store"),
        "stream": request.get("stream"),
        "background": request.get("background"),
        "parallel_tool_calls": request.get("parallel_tool_calls"),
        "truncation": request.get("truncation"),
        "max_output_tokens": request.get("max_output_tokens"),
        "tool_count": len(request.get("tools", ())),
    }


def run_real_luna_canary(environ: Mapping[str, str] = os.environ) -> MappingProxyType[str, Any]:
    """Make the sole physical request and return secret-safe evidence."""
    if (
        environ.get("RAILWAY_SERVICE_NAME") != _SERVICE
        or environ.get("RAILWAY_ENVIRONMENT_NAME") != _ENVIRONMENT
        or SECRET_VARIABLE not in environ
        or "OPENAI_API_KEY" in environ
    ):
        raise RuntimeError("REAL_LUNA_CANARY_WORKER_ENVIRONMENT_DENIED")

    service, call, requirements, selector, adapter, resolver, lease_authority = _compose()
    if adapter.invocation_count != 0:
        raise RuntimeError("REAL_LUNA_CANARY_INVOCATION_NOT_ZERO")
    result = service.execute_provider(
        call,
        capabilities=requirements,
        secret_request=selector,
    )
    lease = resolver.resolved_lease
    if (
        adapter.invocation_count != 1
        or service.counters.provider_calls != 1
        or resolver.resolve_calls != 1
        or lease is None
    ):
        raise RuntimeError("REAL_LUNA_CANARY_ONE_SEND_PROOF_FAILED")
    lease_reusable = lease_authority.consume_for_resolution(lease)
    if lease_reusable:
        raise RuntimeError("REAL_LUNA_CANARY_LEASE_REUSE_ALLOWED")

    if result.outcome is ExecutionOperationOutcome.PROVIDER_COMPLETED:
        classification = "REAL_LUNA_CANARY_PASS_CANDIDATE"
    elif result.outcome is ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME:
        classification = "REAL_LUNA_CANARY_UNKNOWN_NO_RETRY"
    else:
        classification = "REAL_LUNA_CANARY_PROVIDER_REJECTED"
    response_hash = (
        hashlib.sha256(result.response_id.encode()).hexdigest()
        if result.response_id is not None
        else None
    )
    return MappingProxyType(
        {
            "schema_version": "aiscc-real-luna-canary-result-v1",
            "classification": classification,
            "service": _SERVICE,
            "environment": _ENVIRONMENT,
            "profile_id": call.profile.profile_id,
            "profile_version": call.profile.version,
            "model": call.profile.model_ref,
            "runtime_mode": call.runtime_mode.value,
            "scenario": call.scenario_id,
            "adapter": "OpenAIResponsesAdapter(hosted=True)",
            "sdk_max_retries": 0,
            "invocation_count_before": 0,
            "invocation_count_after": adapter.invocation_count,
            "provider_call_count": service.counters.provider_calls,
            "resolver_call_count": resolver.resolve_calls,
            "lease_issuer": lease.issuer_ref,
            "lease_consumed_use_ordinal": lease.consumed_use_ordinal,
            "lease_reusable": lease_reusable,
            "provider_status": result.status,
            "provider_outcome": result.outcome.value,
            "response_id_present": result.response_id is not None,
            "response_id_sha256": response_hash,
            "usage": dict(result.usage),
            "sanitized_error": result.sanitized_error,
            "result_hash": result.result_hash,
            "output_exported": False,
            "request": _request_evidence(adapter.last_request),
        }
    )


def blocked_result(error: BaseException) -> MappingProxyType[str, Any]:
    """Return a message-only-safe classification; never serialize an exception value."""
    return MappingProxyType(
        {
            "schema_version": "aiscc-real-luna-canary-result-v1",
            "classification": "REAL_LUNA_CANARY_TRUST_PATH_BLOCKED",
            "exception_type": type(error).__name__,
            "raw_exception_exported": False,
        }
    )
