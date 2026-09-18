from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import cast

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

from aiscc.contracts.security import ResourceDomain
from aiscc.contracts.workflow import RuntimeMode
from aiscc.providers.authority import SecretResolutionLeaseAuthority
from aiscc.providers.models import (
    SecretResolutionLease,
    SecretUseSelectorRequest,
    ToolCallCandidate,
    ToolDefinition,
    ToolOutputRef,
    ToolRegistry,
    canonical_json_bytes,
    canonical_sha256,
    parse_strict_json_object,
)
from aiscc.providers.ports import SecretResolver, ToolDispatcher
from aiscc.security.capability import (
    CapabilityConsumeRequest,
    CapabilityConsumptionReceipt,
)
from aiscc.security.policy import SecurityPolicy


class KnownToolFailure(ValueError):
    """A bounded dispatcher proved the terminal failure and effect disposition."""


class UnknownToolOutcome(RuntimeError):
    """Dispatch crossed, but termination/effect disposition is not proven."""


@dataclass(frozen=True, slots=True)
class ToolDispatchContext:
    task_action: str
    work_run_id: str
    execution_attempt_id: str
    state: str
    state_version: int
    runtime_mode: str
    scenario_id: str
    scenario_version: str
    profile_id: str
    profile_version: str
    resource_ref: str
    provider_operation_id: str
    provider_call_id: str
    resolved_spec_fingerprint: str = ""
    resolved_implementation_fingerprint: str = ""


@dataclass(frozen=True, slots=True)
class PreparedToolDispatch:
    definition: ToolDefinition
    arguments: dict[str, object]
    fingerprint: str
    capabilities: tuple[CapabilityConsumeRequest, ...]
    secret_request: SecretUseSelectorRequest | None
    dispatch_context: ToolDispatchContext | None = None


@dataclass(frozen=True, slots=True)
class ConsumedToolDispatch:
    prepared: PreparedToolDispatch
    secret_lease: SecretResolutionLease | None
    receipts: tuple[CapabilityConsumptionReceipt, ...] = ()
    dispatch_identity: str = ""


class ToolRegistryBroker:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry
        self.invocation_count = 0

    def validate_candidate(
        self,
        candidate: ToolCallCandidate,
        *,
        mode: RuntimeMode,
        profile_id: str,
        scenario_id: str,
        dispatch_context: ToolDispatchContext | None = None,
    ) -> tuple[ToolDefinition, dict[str, object], str]:
        definition = self.registry.tools.get(candidate.name)
        if definition is None:
            raise ValueError("UNKNOWN_TOOL")
        if not definition.enabled or definition.revoked_at is not None:
            raise ValueError("TOOL_DISABLED_OR_REVOKED")
        if mode not in definition.allowed_modes or profile_id not in definition.allowed_profiles:
            raise ValueError("TOOL_CONTEXT_DENIED")
        if scenario_id not in definition.allowed_scenarios:
            raise ValueError("TOOL_SCENARIO_DENIED")
        arguments = parse_strict_json_object(candidate.arguments_json)
        validator = Draft202012Validator(definition.input_schema)
        errors = sorted(validator.iter_errors(arguments), key=lambda item: list(item.path))
        if errors:
            raise ValueError("TOOL_SCHEMA_DENIED")
        resolved_binding: dict[str, str] = {}
        if definition.dispatcher_version == "stockroom-summary-v1":
            if (
                type(dispatch_context) is not ToolDispatchContext
                or dispatch_context.work_run_id == ""
                or dispatch_context.execution_attempt_id == ""
                or dispatch_context.state != "RUNNING"
                or type(dispatch_context.state_version) is not int
                or dispatch_context.state_version < 1
                or dispatch_context.runtime_mode != mode.value
                or dispatch_context.scenario_id != scenario_id
                or dispatch_context.scenario_version != "1.0.0"
                or dispatch_context.profile_id != profile_id
                or dispatch_context.profile_version != "1"
            ):
                raise ValueError("STOCKROOM_RESOLVED_DISPATCH_CONTEXT_REQUIRED")
            if mode is RuntimeMode.PUBLIC_BOUNDED_LIVE:
                if (
                    dispatch_context.resolved_spec_fingerprint != ""
                    or len(dispatch_context.resolved_implementation_fingerprint) != 64
                ):
                    raise ValueError("STOCKROOM_RESOLVED_DISPATCH_CONTEXT_REQUIRED")
                resolved_binding = {
                    "resolved_implementation_fingerprint": (
                        dispatch_context.resolved_implementation_fingerprint
                    )
                }
            else:
                if (
                    len(dispatch_context.resolved_spec_fingerprint) != 64
                    or dispatch_context.resolved_implementation_fingerprint != ""
                ):
                    raise ValueError("STOCKROOM_RESOLVED_DISPATCH_CONTEXT_REQUIRED")
                resolved_binding = {
                    "resolved_spec_fingerprint": dispatch_context.resolved_spec_fingerprint
                }
        elif dispatch_context is not None:
            raise ValueError("LEGACY_TOOL_DISPATCH_CONTEXT_DENIED")
        fingerprint = canonical_sha256(
            {
                "registry_id": self.registry.registry_id,
                "registry_version": self.registry.version,
                "tool_id": definition.tool_id,
                "schema_version": definition.schema_version,
                "dispatcher_version": definition.dispatcher_version,
                "arguments": arguments,
                "underlying_resource_requirements": [
                    {
                        "domain": requirement.scope.domain.value,
                        "resource_id": requirement.scope.resource_id,
                        "action": requirement.action.value,
                    }
                    for requirement in definition.underlying_resource_requirements
                ],
                "secret_requirement": (
                    {
                        "secret_identity": hashlib.sha256(
                            definition.secret_requirement.secret_ref.encode()
                        ).hexdigest(),
                        "secret_class": definition.secret_requirement.secret_class,
                        "purpose": definition.secret_requirement.purpose,
                        "destination": definition.secret_requirement.destination,
                        "dispatcher_identity": (definition.secret_requirement.dispatcher_identity),
                    }
                    if definition.secret_requirement is not None
                    else None
                ),
                "resolved_dispatch_context": (
                    {
                        "task_action": dispatch_context.task_action,
                        "work_run_id": dispatch_context.work_run_id,
                        "execution_attempt_id": dispatch_context.execution_attempt_id,
                        "state": dispatch_context.state,
                        "state_version": dispatch_context.state_version,
                        "runtime_mode": dispatch_context.runtime_mode,
                        "scenario_id": dispatch_context.scenario_id,
                        "scenario_version": dispatch_context.scenario_version,
                        "profile_id": dispatch_context.profile_id,
                        "profile_version": dispatch_context.profile_version,
                        "resource_ref": dispatch_context.resource_ref,
                        "provider_operation_id": dispatch_context.provider_operation_id,
                        "provider_call_id": dispatch_context.provider_call_id,
                        **resolved_binding,
                    }
                    if dispatch_context is not None
                    else None
                ),
            }
        )
        return definition, arguments, fingerprint

    def dispatch_candidate(
        self,
        candidate: ToolCallCandidate,
        *,
        mode: RuntimeMode,
        profile_id: str,
        scenario_id: str,
        policy: SecurityPolicy,
        capabilities: tuple[CapabilityConsumeRequest, ...],
        dispatcher: ToolDispatcher,
        secret_request: SecretUseSelectorRequest | None = None,
        dispatch_context: ToolDispatchContext | None = None,
        secret_lease_authority: SecretResolutionLeaseAuthority | None = None,
        secret_resolver: SecretResolver | None = None,
    ) -> ToolOutputRef:
        prepared = self.prepare_dispatch(
            candidate,
            mode=mode,
            profile_id=profile_id,
            scenario_id=scenario_id,
            capabilities=capabilities,
            secret_request=secret_request,
            dispatch_context=dispatch_context,
        )
        consumed = self.consume_prepared(
            prepared,
            policy=policy,
            secret_lease_authority=secret_lease_authority,
        )
        return self.dispatch_prepared(
            consumed,
            dispatcher=dispatcher,
            secret_resolver=secret_resolver,
        )

    def prepare_dispatch(
        self,
        candidate: ToolCallCandidate,
        *,
        mode: RuntimeMode,
        profile_id: str,
        scenario_id: str,
        capabilities: tuple[CapabilityConsumeRequest, ...],
        secret_request: SecretUseSelectorRequest | None = None,
        context_requirements: tuple[tuple[ResourceDomain, str], ...] = (),
        dispatch_context: ToolDispatchContext | None = None,
    ) -> PreparedToolDispatch:
        """Validate the exact declared authority set without consuming or dispatching."""
        definition, arguments, fingerprint = self.validate_candidate(
            candidate,
            mode=mode,
            profile_id=profile_id,
            scenario_id=scenario_id,
            dispatch_context=dispatch_context,
        )
        tool_resource_id = ":".join(
            (
                self.registry.registry_id,
                self.registry.version,
                definition.tool_id,
                definition.schema_version,
                definition.dispatcher_version,
            )
        )
        tool_requests = tuple(
            request
            for request in capabilities
            if request.scope.domain is ResourceDomain.TOOL
            and request.scope.resource_id == tool_resource_id
        )
        if len(tool_requests) != 1:
            raise ValueError("TOOL_UNDERLYING_CAPABILITY_DENIED")
        remaining = list(capabilities)
        remaining.remove(tool_requests[0])
        for requirement in definition.underlying_resource_requirements:
            matches = [
                request
                for request in remaining
                if request.scope == requirement.scope and request.action is requirement.action
            ]
            if len(matches) != 1:
                raise ValueError("TOOL_UNDERLYING_CAPABILITY_DENIED")
            remaining.remove(matches[0])
        if definition.secret_requirement is not None:
            secret_identity = hashlib.sha256(
                definition.secret_requirement.secret_ref.encode()
            ).hexdigest()
            matches = [
                request
                for request in remaining
                if request.scope.domain is ResourceDomain.SECRET
                and request.scope.resource_id
                == f"{definition.secret_requirement.secret_class}:{secret_identity}"
            ]
            if len(matches) != 1:
                raise ValueError("TOOL_SECRET_CAPABILITY_DENIED")
            remaining.remove(matches[0])
        for domain, resource_id in context_requirements:
            matches = [
                request
                for request in remaining
                if request.scope.domain is domain and request.scope.resource_id == resource_id
            ]
            if len(matches) != 1:
                raise ValueError("TOOL_CONTEXT_CAPABILITY_DENIED")
            remaining.remove(matches[0])
        if remaining:
            raise ValueError("TOOL_UNDECLARED_CAPABILITY_DENIED")
        if any(request.operation_fingerprint != fingerprint for request in capabilities):
            raise ValueError("TOOL_ARGUMENT_FINGERPRINT_DENIED")
        if definition.secret_requirement is None and secret_request is not None:
            raise ValueError("TOOL_UNDECLARED_SECRET_REQUEST_DENIED")
        if definition.secret_requirement is not None and secret_request is None:
            raise ValueError("TOOL_SECRET_LEASE_REQUIRED")
        return PreparedToolDispatch(
            definition=definition,
            arguments=arguments,
            fingerprint=fingerprint,
            capabilities=capabilities,
            secret_request=secret_request,
            dispatch_context=dispatch_context,
        )

    @staticmethod
    def consume_prepared(
        prepared: PreparedToolDispatch,
        *,
        policy: SecurityPolicy,
        secret_lease_authority: SecretResolutionLeaseAuthority | None,
    ) -> ConsumedToolDispatch:
        uses, receipts = policy.consume_capabilities_atomically_with_receipts(prepared.capabilities)
        capabilities = prepared.capabilities
        if len(uses) != len(capabilities) or not all(use.allowed for use in uses):
            raise ValueError("TOOL_CAPABILITY_DENIED")
        definition = prepared.definition
        lease: SecretResolutionLease | None = None
        if definition.secret_requirement is not None:
            if secret_lease_authority is None or prepared.secret_request is None:
                raise ValueError("TOOL_SECRET_LEASE_REQUIRED")
            secret_indexes = [
                index
                for index, requirement in enumerate(capabilities)
                if requirement.scope.domain is ResourceDomain.SECRET
            ]
            if len(secret_indexes) != 1:
                raise ValueError("TOOL_SECRET_CAPABILITY_DENIED")
            index = secret_indexes[0]
            lease = secret_lease_authority.issue(
                receipts[index], capabilities[index], prepared.secret_request
            )
        dispatch_identity = canonical_sha256(
            {
                "tool_fingerprint": prepared.fingerprint,
                "receipt_ids": [receipt.receipt_id for receipt in receipts],
            }
        )
        if definition.dispatcher_version == "stockroom-summary-v1":
            stockroom_claimed = policy.claim_consumption_receipts_atomically(
                receipts,
                capabilities,
                dispatch_identity=dispatch_identity,
            )
            if not stockroom_claimed:
                raise ValueError("STOCKROOM_RECEIPT_CLAIM_DENIED")
        return ConsumedToolDispatch(
            prepared=prepared,
            secret_lease=lease,
            receipts=receipts,
            dispatch_identity=dispatch_identity,
        )

    def dispatch_prepared(
        self,
        consumed: ConsumedToolDispatch,
        *,
        dispatcher: ToolDispatcher,
        secret_resolver: SecretResolver | None,
    ) -> ToolOutputRef:
        definition = consumed.prepared.definition
        arguments = consumed.prepared.arguments
        fingerprint = consumed.prepared.fingerprint
        if definition.dispatcher_version == "stockroom-summary-v1":
            dispatch = getattr(dispatcher, "dispatch_with_receipts", None)
            if not callable(dispatch) or consumed.secret_lease is not None:
                raise ValueError("STOCKROOM_RECEIPT_AWARE_DISPATCHER_REQUIRED")
            result = cast(
                ToolOutputRef,
                dispatch(
                    definition,
                    arguments,
                    receipts=consumed.receipts,
                    requirements=consumed.prepared.capabilities,
                    dispatch_identity=consumed.dispatch_identity,
                ),
            )
        elif consumed.secret_lease is None:
            result = dispatcher.dispatch(definition, arguments)
        else:
            if secret_resolver is None:
                raise ValueError("TOOL_SECRET_LEASE_REQUIRED")
            lease = consumed.secret_lease
            secret = secret_resolver.resolve(lease)
            try:
                result = dispatcher.dispatch(definition, arguments, secret=secret)
            finally:
                secret_resolver.close(lease)
        if result.argument_hash != fingerprint:
            raise ValueError("TOOL_DISPATCH_RESULT_BINDING_CONFLICT")
        if result.output is None:
            raise ValueError("TOOL_OUTPUT_BODY_MISSING")
        output_errors = sorted(
            Draft202012Validator(definition.output_schema).iter_errors(result.output),
            key=lambda item: list(item.path),
        )
        output_bytes = canonical_json_bytes(result.output)
        if (
            output_errors
            or len(output_bytes) > definition.output_byte_bound
            or result.result_hash != canonical_sha256(result.output)
        ):
            raise ValueError("TOOL_OUTPUT_CONTRACT_DENIED")
        self.invocation_count += 1
        return result
