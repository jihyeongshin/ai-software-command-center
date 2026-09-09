from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from time import monotonic
from types import MappingProxyType
from typing import Any

from aiscc.contracts.security import (
    AuthorityStatus,
    PermissionRequest,
    ResourceDomain,
    ResourceScope,
    SecurityActionClass,
    SecurityAdmissionDecision,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.persistence.repository import PostgresExecutionRepository
from aiscc.providers.authority import (
    ExecutionReferenceAuthority,
    SecretResolutionLeaseAuthority,
)
from aiscc.providers.models import (
    ExecutionAttemptRef,
    ExecutionOperationOutcome,
    ExecutionOperationPhase,
    ExecutionStatus,
    ExecutionSubmissionRef,
    OperationKind,
    ProviderCall,
    ProviderInputAuthority,
    ProviderProfile,
    ProviderResult,
    ProviderToolSelectorRequest,
    SecretUseSelectorRequest,
    ToolCallCandidate,
    ToolRegistry,
    canonical_json_bytes,
    canonical_sha256,
)
from aiscc.providers.openai_responses import validate_continuation
from aiscc.providers.ports import (
    ExecutionAuthorityReader,
    ProviderAdapter,
    ProviderToolResourcePolicyPort,
    SecretResolver,
    SecretUseAuthorityPort,
    ToolDispatcher,
)
from aiscc.providers.tools import ToolDispatchContext, ToolRegistryBroker, UnknownToolOutcome
from aiscc.security.capability import CapabilityConsumeRequest
from aiscc.security.policy import SecurityPolicy
from aiscc.workflow.models import AuthorityConflictError


@dataclass(slots=True)
class ExecutionCounters:
    provider_calls: int = 0
    rounds: int = 0
    tool_calls: int = 0
    retries: int = 0
    output_tokens: int = 0
    output_bytes: int = 0
    budget_units: int = 0


@dataclass(frozen=True, slots=True)
class DurableExecutionResult:
    status: str
    submission: ExecutionSubmissionRef | None = None


class AgentExecutionService:
    def __init__(
        self,
        *,
        policy: SecurityPolicy,
        adapter: ProviderAdapter,
        secret_resolver: SecretResolver,
        authority_reader: ExecutionAuthorityReader,
        secret_lease_authority: SecretResolutionLeaseAuthority | None = None,
        repository: PostgresExecutionRepository | None = None,
        provider_tool_authority: ProviderToolResourcePolicyPort | None = None,
        secret_use_authority: SecretUseAuthorityPort | None = None,
        profile: ProviderProfile | None = None,
        tool_registry: ToolRegistry | None = None,
        tool_dispatcher: ToolDispatcher | None = None,
        execution_ref_authority: ExecutionReferenceAuthority | None = None,
        server_initial_inputs: dict[str, tuple[dict[str, Any], ...]] | None = None,
        stockroom_context_factory: Callable[..., object] | None = None,
        stockroom_dispatch_context_factory: Callable[..., ToolDispatchContext] | None = None,
        security_profile_version: str = "p1-3-v2",
        time_source: Callable[[], float] = monotonic,
        durable_time_source: Callable[[], datetime] = lambda: datetime.now(UTC),
    ) -> None:
        self._policy = policy
        self._adapter = adapter
        self._secret_resolver = secret_resolver
        self._authority_reader = authority_reader
        self._secret_lease_authority = secret_lease_authority
        self._repository = repository
        self._provider_tool_authority = provider_tool_authority
        self._secret_use_authority = secret_use_authority
        self._profile = profile
        self._tool_broker = ToolRegistryBroker(tool_registry) if tool_registry is not None else None
        self._tool_dispatcher = tool_dispatcher
        self._execution_ref_authority = execution_ref_authority
        self._server_initial_inputs = dict(server_initial_inputs or {})
        self._stockroom_context_factory = stockroom_context_factory
        self._stockroom_dispatch_context_factory = stockroom_dispatch_context_factory
        self._security_profile_version = security_profile_version
        self._time_source = time_source
        self._durable_time_source = durable_time_source
        self._started_at = time_source()
        self._closed = False
        self.failure_events: list[str] = []
        self.counters = ExecutionCounters()

    def execute_provider(
        self,
        call: ProviderCall,
        *,
        capabilities: tuple[CapabilityConsumeRequest, ...],
        secret_request: SecretUseSelectorRequest | None = None,
    ) -> ProviderResult:
        if self._closed:
            raise ValueError("EXECUTION_ATTEMPT_CLOSED")
        current, attempt = self._authority_reader.load(
            work_run_id=call.work_run_id,
            execution_attempt_id=call.execution_attempt_id,
        )
        if call.runtime_mode is RuntimeMode.PUBLIC_RECORDED_REPLAY:
            raise ValueError("REPLAY_ZERO_EXECUTION")
        if current.state is not WorkflowState.RUNNING:
            raise ValueError("WORKFLOW_NOT_RUNNING")
        if current.run_id != call.work_run_id or current.state_version != call.state_version:
            raise ValueError("STALE_PROVIDER_CALL")
        if (
            attempt.execution_attempt_id != call.execution_attempt_id
            or attempt.work_run_id != call.work_run_id
            or attempt.state is not WorkflowState.RUNNING
            or attempt.state_version != call.state_version
            or attempt.execution_version != call.execution_version
            or attempt.status is not ExecutionStatus.RUNNING
        ):
            raise ValueError("STALE_EXECUTION_ATTEMPT")
        if (
            call.runtime_mode not in call.profile.allowed_runtime_modes
            or call.scenario_id not in call.profile.scenario_allowlist
            or not call.profile.enabled
        ):
            raise ValueError("PROVIDER_PROFILE_CONTEXT_DENIED")
        item_types = {item.get("type") for item in call.input_items}
        continuation_types = {"function_call", "function_call_output", "reasoning"}
        if call.input_authority is ProviderInputAuthority.INITIAL_SERVER:
            if item_types & continuation_types:
                raise ValueError("CALLER_CONTINUATION_AUTHORITY_DENIED")
        elif (
            call.durable_continuation_hash is None
            or call.durable_continuation_hash
            != hashlib.sha256(canonical_json_bytes(list(call.input_items))).hexdigest()
        ):
            raise ValueError("DURABLE_CONTINUATION_AUTHORITY_DENIED")
        self._check_bounds(call)
        required_domains = {ResourceDomain.PROVIDER, ResourceDomain.SECRET}
        supplied_domains = {
            request.scope.domain for request in capabilities if request.capability is not None
        }
        if not required_domains.issubset(supplied_domains):
            return self._security_denial(call)
        provider_requirements = tuple(
            request for request in capabilities if request.scope.domain is ResourceDomain.PROVIDER
        )
        secret_requirements = tuple(
            request for request in capabilities if request.scope.domain is ResourceDomain.SECRET
        )
        expected_scopes = {
            ResourceDomain.PROVIDER: call.profile.provider_resource_identity,
            ResourceDomain.SECRET: call.profile.secret_resource_identity,
        }
        if len(provider_requirements) != 1 or len(secret_requirements) != 1:
            return self._security_denial(call)
        for requirement in (*provider_requirements, *secret_requirements):
            if (
                requirement.principal != call.principal
                or requirement.current != current
                or requirement.current_mode is not call.runtime_mode
                or requirement.scope.resource_id != expected_scopes[requirement.scope.domain]
                or requirement.operation_fingerprint != call.operation_fingerprint
                or requirement.selector_attestation_ref is None
            ):
                return self._security_denial(call)
        uses, receipts = self._policy.consume_capabilities_atomically_with_receipts(capabilities)
        if (
            len(capabilities) < 2
            or len(uses) != len(capabilities)
            or not all(use.allowed for use in uses)
        ):
            return self._security_denial(call)
        secret_index = next(
            (
                index
                for index, requirement in enumerate(capabilities)
                if requirement.scope.domain is ResourceDomain.SECRET
            ),
            None,
        )
        if secret_index is None or len(receipts) != len(capabilities):
            return self._security_denial(call)
        if self._secret_lease_authority is None or secret_request is None:
            return self._security_denial(call)
        lease = self._secret_lease_authority.issue(
            receipts[secret_index], capabilities[secret_index], secret_request
        )
        secret = self._secret_resolver.resolve(lease)
        try:
            result = self._adapter.call(call, secret=secret)
        finally:
            self._secret_resolver.close(lease)
        self.counters.provider_calls += 1
        self.counters.rounds += 1
        self.counters.budget_units += 1
        output_tokens = result.usage.get("output_tokens", 0)
        output_bytes = len(result.output_text.encode()) if result.output_text is not None else 0
        self.admit_output(call, output_bytes=output_bytes, output_tokens=output_tokens)
        return result

    async def execute(
        self,
        *,
        work_run_id: str,
        execution_attempt_id: str,
        principal: str,
        scenario_id: str,
        max_provider_rounds: int | None = None,
    ) -> DurableExecutionResult:
        """Run or resume the sole durable P1-5 provider/tool causal path."""
        repository = self._require_durable_dependencies()
        profile = self._profile
        broker = self._tool_broker
        lease_authority = self._secret_lease_authority
        if profile is None or broker is None or lease_authority is None:
            raise RuntimeError("durable provider configuration is missing")
        initial_inputs = self._server_initial_inputs.get(scenario_id)
        allowed_rounds = max_provider_rounds or profile.agent_round_trip_maximum
        if allowed_rounds <= 0 or allowed_rounds > profile.agent_round_trip_maximum:
            raise ValueError("PROVIDER_ROUND_BOUND_DENIED")
        for _ in range(allowed_rounds):
            current, attempt = await repository.load_authority(
                work_run_id=work_run_id,
                execution_attempt_id=execution_attempt_id,
            )
            if attempt.status is not ExecutionStatus.RUNNING:
                return DurableExecutionResult(attempt.status.value)
            if (
                current.state is not WorkflowState.RUNNING
                or attempt.state is not current.state
                or attempt.state_version != current.state_version
            ):
                await repository.close_workflow_left_running(
                    execution_attempt_id,
                    reason="EXECUTE_ENTRY_FRESHNESS_DENIED",
                )
                return DurableExecutionResult("EXECUTION_FAILED")
            recovered = await self._recover_nonterminal_operation(repository, execution_attempt_id)
            if recovered:
                return DurableExecutionResult("EXECUTION_FAILED")
            history = await repository.load_private_protocol_items(execution_attempt_id)
            final_text = _latest_final_text(history)
            if final_text is not None:
                submission = await self._complete_durable_attempt(
                    repository, current, attempt, final_text
                )
                return DurableExecutionResult("EXECUTOR_COMPLETED", submission)
            pending_tool = _pending_tool_call(history)
            if pending_tool is not None:
                tool_admitted = await self._execute_durable_tool(
                    repository=repository,
                    work_run_id=work_run_id,
                    execution_attempt_id=execution_attempt_id,
                    principal=principal,
                    scenario_id=scenario_id,
                    candidate=pending_tool,
                )
                if not tool_admitted:
                    return DurableExecutionResult("EXECUTION_FAILED")
                history = await repository.load_private_protocol_items(execution_attempt_id)
            call_id = _continuation_call_id(history)
            if history:
                if call_id is None:
                    raise AuthorityConflictError("durable continuation call_id is missing")
                validate_continuation(
                    history,
                    call_id=call_id,
                    maximum_items=profile.continuation_item_maximum,
                    maximum_bytes=profile.continuation_byte_bound,
                    maximum_token_estimate=profile.continuation_token_estimate_bound,
                )
                input_items = history
                input_authority = ProviderInputAuthority.DURABLE_LOCAL
                continuation_hash = hashlib.sha256(canonical_json_bytes(list(history))).hexdigest()
            else:
                input_items = initial_inputs or ()
                input_authority = ProviderInputAuthority.INITIAL_SERVER
                continuation_hash = None
            operations = await repository.load_operations(execution_attempt_id)
            ordinal = len(operations) + 1
            operation_id = _stable_id(
                "provider", execution_attempt_id, str(ordinal), profile.provider_resource_identity
            )
            fingerprint = canonical_sha256(
                {
                    "schema_version": "p1-5-operation-v1",
                    "kind": "PROVIDER",
                    "work_run_id": work_run_id,
                    "execution_attempt_id": execution_attempt_id,
                    "state": current.state.value,
                    "state_version": current.state_version,
                    "runtime_mode": (
                        attempt.runtime_mode.value
                        if attempt.runtime_mode is not None
                        else "MISSING"
                    ),
                    "scenario_id": scenario_id,
                    "profile_id": profile.profile_id,
                    "profile_version": profile.version,
                    "resource_identity": profile.provider_resource_identity,
                    "input_hash": hashlib.sha256(
                        canonical_json_bytes(list(input_items))
                    ).hexdigest(),
                    "call_ordinal": ordinal,
                }
            )
            if attempt.runtime_mode is None:
                raise AuthorityConflictError("execution attempt RuntimeMode is missing")
            runtime_mode = attempt.runtime_mode
            await repository.create_operation(
                operation_id=operation_id,
                attempt_id=execution_attempt_id,
                kind=OperationKind.PROVIDER,
                fingerprint=fingerprint,
                resource_identity=profile.provider_resource_identity,
                call_ordinal=ordinal,
            )
            try:
                self._require_running_context(current, attempt, profile, scenario_id)
                if initial_inputs is None:
                    raise ValueError("SERVER_INITIAL_INPUT_MISSING")
                if not history:
                    await self._store_protocol_items(
                        repository,
                        execution_attempt_id,
                        operation_id,
                        input_items,
                    )
                call = ProviderCall(
                    operation_id=operation_id,
                    operation_fingerprint=fingerprint,
                    execution_attempt_id=execution_attempt_id,
                    work_run_id=work_run_id,
                    state=current.state,
                    state_version=current.state_version,
                    runtime_mode=runtime_mode,
                    principal=principal,
                    scenario_id=scenario_id,
                    execution_version=attempt.execution_version,
                    profile=profile,
                    input_items=input_items,
                    tools=self._provider_tools(profile, broker),
                    call_ordinal=ordinal,
                    input_authority=input_authority,
                    durable_continuation_hash=continuation_hash,
                )
                capabilities, secret_request = self._provider_capabilities(
                    call, current, operation_id
                )
                await repository.advance_operation(
                    operation_id,
                    ExecutionOperationPhase.SECURITY_ADMITTED,
                    refs={
                        "capability_ids": [
                            requirement.capability.capability_id
                            for requirement in capabilities
                            if requirement.capability is not None
                        ]
                    },
                )
                input_size = len(canonical_json_bytes(list(input_items)))
                continuation_size = len(canonical_json_bytes(list(history))) if history else 0
                reservation = await repository.reserve_execution_bounds(
                    operation_id=operation_id,
                    profile=profile,
                    expected_state_version=current.state_version,
                    expected_execution_version=attempt.execution_version,
                    provider_calls=1,
                    agent_rounds=1,
                    budget_units=1,
                    input_bytes=input_size,
                    continuation_items=len(history),
                    continuation_bytes=continuation_size,
                    continuation_token_estimate=(continuation_size + 3) // 4,
                    now=self._durable_time_source(),
                )
                if not reservation.admitted:
                    return DurableExecutionResult("EXECUTION_FAILED")
                call = replace(
                    call,
                    execution_version=reservation.execution_version,
                    output_token_maximum=(
                        profile.output_token_bound - reservation.counters.output_tokens
                    ),
                )
                uses, receipts = self._policy.consume_capabilities_atomically_with_receipts(
                    capabilities
                )
                if len(uses) != len(capabilities) or not all(use.allowed for use in uses):
                    raise ValueError("CAPABILITY_ATOMIC_CONSUME_DENIED")
                secret_indexes = [
                    index
                    for index, requirement in enumerate(capabilities)
                    if requirement.scope.domain is ResourceDomain.SECRET
                ]
                if len(secret_indexes) != 1 or len(receipts) != len(capabilities):
                    raise ValueError("PROVIDER_SECRET_CAPABILITY_DENIED")
                secret_index = secret_indexes[0]
                lease = lease_authority.issue(
                    receipts[secret_index], capabilities[secret_index], secret_request
                )
                fresh = await repository.start_dispatch_if_fresh(
                    operation_id=operation_id,
                    expected_state_version=current.state_version,
                    expected_execution_version=reservation.execution_version,
                    refs={"secret_lease_id": lease.lease_id},
                )
                if not fresh:
                    self._secret_resolver.close(lease)
                    return DurableExecutionResult("EXECUTION_FAILED")
            except (AuthorityConflictError, ValueError) as exc:
                await repository.fail_operation_before_side_effect(
                    operation_id=operation_id,
                    reason=str(exc),
                    failure_class="SECURITY_DENIAL",
                )
                return DurableExecutionResult("EXECUTION_FAILED")
            secret = self._secret_resolver.resolve(lease)
            try:
                result = self._adapter.call(call, secret=secret)
            except Exception as exc:
                await repository.advance_operation(
                    operation_id,
                    ExecutionOperationPhase.OUTCOME_UNKNOWN,
                    ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME,
                    refs={"sanitized_error": type(exc).__name__},
                )
                failed_current, failed_attempt = await repository.load_authority(
                    work_run_id=work_run_id,
                    execution_attempt_id=execution_attempt_id,
                )
                if (
                    failed_current.state is not WorkflowState.RUNNING
                    or failed_attempt.state is not failed_current.state
                    or failed_attempt.state_version != failed_current.state_version
                ):
                    await repository.close_workflow_left_running(
                        execution_attempt_id,
                        reason="WORKFLOW_LEFT_RUNNING_AFTER_PROVIDER_EXCEPTION",
                    )
                else:
                    await repository.transition_attempt(
                        execution_attempt_id,
                        "EXECUTION_FAILED",
                        refs={"failure_class": "UNKNOWN_OUTCOME", "blind_retry": False},
                    )
                return DurableExecutionResult("EXECUTION_FAILED")
            finally:
                self._secret_resolver.close(lease)
            target_phase = (
                ExecutionOperationPhase.OUTCOME_UNKNOWN
                if result.outcome is ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
                else ExecutionOperationPhase.OUTCOME_KNOWN
            )
            await repository.advance_operation(
                operation_id,
                target_phase,
                result.outcome,
                refs={"result_hash": result.result_hash, "provider_status": result.status},
            )
            refreshed, refreshed_attempt = await repository.load_authority(
                work_run_id=work_run_id,
                execution_attempt_id=execution_attempt_id,
            )
            if (
                refreshed.state is not WorkflowState.RUNNING
                or refreshed_attempt.state is not refreshed.state
                or refreshed_attempt.state_version != refreshed.state_version
            ):
                await repository.close_workflow_left_running(
                    execution_attempt_id,
                    reason="WORKFLOW_LEFT_RUNNING_AFTER_PROVIDER_DISPATCH",
                )
                return DurableExecutionResult("EXECUTION_FAILED")
            if result.outcome is ExecutionOperationOutcome.PROVIDER_COMPLETED:
                output_bytes = len(canonical_json_bytes(list(result.output_items)))
                try:
                    output_tokens = _durable_provider_output_token_charge(
                        result,
                        requested_maximum=call.output_token_maximum,
                    )
                except ValueError as exc:
                    await repository.transition_attempt(
                        execution_attempt_id,
                        "EXECUTION_FAILED",
                        refs={
                            "failure_class": "PROVIDER_PROTOCOL_ACCOUNTING",
                            "reason": str(exc),
                            "blind_retry": False,
                        },
                    )
                    return DurableExecutionResult("EXECUTION_FAILED")
                settlement = await repository.settle_execution_output(
                    operation_id=operation_id,
                    profile=profile,
                    output_bytes=output_bytes,
                    output_tokens=output_tokens,
                    now=self._durable_time_source(),
                )
                if not settlement.admitted:
                    return DurableExecutionResult("EXECUTION_FAILED")
            if result.output_items:
                await self._store_protocol_items(
                    repository,
                    execution_attempt_id,
                    operation_id,
                    result.output_items,
                )
            self.counters.provider_calls += 1
            self.counters.rounds += 1
            self.counters.budget_units += 1
            if target_phase is ExecutionOperationPhase.OUTCOME_UNKNOWN or result.outcome not in {
                ExecutionOperationOutcome.PROVIDER_COMPLETED
            }:
                await repository.transition_attempt(
                    execution_attempt_id,
                    "EXECUTION_FAILED",
                    refs={
                        "failure_class": (
                            "UNKNOWN_OUTCOME"
                            if target_phase is ExecutionOperationPhase.OUTCOME_UNKNOWN
                            else "FATAL"
                        ),
                        "blind_retry": False,
                    },
                )
                return DurableExecutionResult("EXECUTION_FAILED")
            if result.tool_call is not None:
                tool_admitted = await self._execute_durable_tool(
                    repository=repository,
                    work_run_id=work_run_id,
                    execution_attempt_id=execution_attempt_id,
                    principal=principal,
                    scenario_id=scenario_id,
                    candidate=result.tool_call,
                )
                if not tool_admitted:
                    return DurableExecutionResult("EXECUTION_FAILED")
                continue
            if result.output_text is None:
                raise AuthorityConflictError("provider completed without final output or tool call")
            refreshed, refreshed_attempt = await repository.load_authority(
                work_run_id=work_run_id,
                execution_attempt_id=execution_attempt_id,
            )
            submission = await self._complete_durable_attempt(
                repository, refreshed, refreshed_attempt, result.output_text
            )
            return DurableExecutionResult("EXECUTOR_COMPLETED", submission)
        return DurableExecutionResult("CONTINUATION_REQUIRED")

    def _require_durable_dependencies(self) -> PostgresExecutionRepository:
        if (
            self._repository is None
            or self._provider_tool_authority is None
            or self._secret_use_authority is None
            or self._profile is None
            or self._tool_broker is None
            or self._tool_dispatcher is None
            or self._execution_ref_authority is None
            or self._secret_lease_authority is None
        ):
            raise RuntimeError("durable AgentExecutionService dependencies are incomplete")
        return self._repository

    @staticmethod
    def _require_running_context(
        current: WorkflowSnapshot,
        attempt: ExecutionAttemptRef,
        profile: ProviderProfile,
        scenario_id: str,
    ) -> None:
        if (
            current.state is not WorkflowState.RUNNING
            or attempt.status is not ExecutionStatus.RUNNING
            or attempt.state is not WorkflowState.RUNNING
            or attempt.state_version != current.state_version
            or attempt.work_run_id != current.run_id
            or attempt.runtime_mode is None
            or attempt.runtime_mode not in profile.allowed_runtime_modes
            or attempt.provider_profile_id != profile.profile_id
            or attempt.provider_profile_version != profile.version
            or attempt.tool_registry_id != profile.tool_registry_id
            or attempt.tool_registry_version != profile.tool_registry_version
            or scenario_id not in profile.scenario_allowlist
            or not profile.enabled
            or profile.revoked_at is not None
            or (
                attempt.runtime_mode is RuntimeMode.PUBLIC_BOUNDED_LIVE
                and (
                    attempt.project_id != profile.public_repository_resource_identity
                    or scenario_id != profile.public_scenario_identity
                )
            )
        ):
            raise AuthorityConflictError("durable execution context is not current and admissible")

    @staticmethod
    def _provider_tools(
        profile: ProviderProfile, broker: ToolRegistryBroker
    ) -> tuple[dict[str, Any], ...]:
        definitions: list[dict[str, Any]] = []
        for tool_id in sorted(profile.tool_allowlist):
            definition = broker.registry.tools.get(tool_id)
            if definition is None or not definition.enabled or definition.revoked_at is not None:
                raise AuthorityConflictError("profile tool allowlist is unresolved")
            definitions.append(
                {
                    "type": "function",
                    "name": definition.tool_id,
                    "description": definition.description,
                    "parameters": definition.input_schema,
                    "strict": True,
                }
            )
        return tuple(definitions)

    def _provider_capabilities(
        self,
        call: ProviderCall,
        current: WorkflowSnapshot,
        operation_id: str,
    ) -> tuple[tuple[CapabilityConsumeRequest, ...], SecretUseSelectorRequest]:
        authority = self._provider_tool_authority
        secret_authority = self._secret_use_authority
        if authority is None or secret_authority is None:
            raise RuntimeError("P1-5 selector authorities are missing")
        provider_selector = ProviderToolSelectorRequest(
            domain=ResourceDomain.PROVIDER.value,
            canonical_resource_identity=call.profile.provider_resource_identity,
            principal=call.principal,
            work_run_id=call.work_run_id,
            execution_attempt_id=call.execution_attempt_id,
            state=call.state,
            state_version=call.state_version,
            runtime_mode=call.runtime_mode,
            profile_id=call.profile.profile_id,
            profile_version=call.profile.version,
            scenario_id=call.scenario_id,
            operation_fingerprint=call.operation_fingerprint,
        )
        provider_attestation = authority.attest(provider_selector)
        secret_selector = SecretUseSelectorRequest(
            secret_ref=call.profile.secret_ref,
            secret_class="PROVIDER_API",
            purpose="RESPONSES_CREATE",
            destination=call.profile.endpoint_ref,
            canonical_resource_identity=call.profile.provider_resource_identity,
            adapter_identity=call.profile.adapter_protocol_version,
            principal=call.principal,
            work_run_id=call.work_run_id,
            execution_attempt_id=call.execution_attempt_id,
            operation_id=operation_id,
            state=call.state,
            state_version=call.state_version,
            runtime_mode=call.runtime_mode,
            profile_id=call.profile.profile_id,
            profile_version=call.profile.version,
            scenario_id=call.scenario_id,
            operation_fingerprint=call.operation_fingerprint,
        )
        secret_attestation = secret_authority.attest(secret_selector)
        capabilities = [
            self._issue_capability(
                current=current,
                mode=call.runtime_mode,
                principal=call.principal,
                scenario_id=call.scenario_id,
                scope=ResourceScope(
                    ResourceDomain.PROVIDER, call.profile.provider_resource_identity
                ),
                selector_ref=provider_attestation.attestation_id,
                selector_request=provider_selector,
                fingerprint=call.operation_fingerprint,
                execution_attempt_id=call.execution_attempt_id,
                provider_profile_id=call.profile.profile_id,
                provider_profile_version=call.profile.version,
            ),
            self._issue_capability(
                current=current,
                mode=call.runtime_mode,
                principal=call.principal,
                scenario_id=call.scenario_id,
                scope=ResourceScope(ResourceDomain.SECRET, call.profile.secret_resource_identity),
                selector_ref=secret_attestation.attestation_id,
                selector_request=secret_selector,
                fingerprint=call.operation_fingerprint,
                execution_attempt_id=call.execution_attempt_id,
                provider_profile_id=call.profile.profile_id,
                provider_profile_version=call.profile.version,
            ),
        ]
        if call.runtime_mode is RuntimeMode.PUBLIC_BOUNDED_LIVE:
            capabilities.extend(
                (
                    self._issue_capability(
                        current=current,
                        mode=call.runtime_mode,
                        principal=call.principal,
                        scenario_id=call.scenario_id,
                        scope=ResourceScope(
                            ResourceDomain.REPOSITORY,
                            call.profile.public_repository_resource_identity,
                        ),
                        selector_ref=None,
                        selector_request=None,
                        fingerprint=call.operation_fingerprint,
                    ),
                    self._issue_capability(
                        current=current,
                        mode=call.runtime_mode,
                        principal=call.principal,
                        scenario_id=call.scenario_id,
                        scope=ResourceScope(
                            ResourceDomain.SCENARIO,
                            call.profile.public_scenario_resource_identity,
                        ),
                        selector_ref=None,
                        selector_request=None,
                        fingerprint=call.operation_fingerprint,
                    ),
                )
            )
        return tuple(capabilities), secret_selector

    def _issue_capability(
        self,
        *,
        current: WorkflowSnapshot,
        mode: RuntimeMode,
        principal: str,
        scenario_id: str,
        scope: ResourceScope,
        selector_ref: str | None,
        selector_request: object | None,
        fingerprint: str,
        action: SecurityActionClass = SecurityActionClass.RUN_EXECUTION_SIDE_EFFECT,
        execution_attempt_id: str = "",
        provider_profile_id: str = "",
        provider_profile_version: str = "",
        resolved_spec_fingerprint: str = "",
    ) -> CapabilityConsumeRequest:
        stockroom_context = None
        if self._stockroom_context_factory is not None:
            stockroom_context = self._stockroom_context_factory(
                current=current,
                mode=mode,
                principal=principal,
                scenario_id=scenario_id,
                scope=scope,
                action=action,
                operation_fingerprint=fingerprint,
                execution_attempt_id=execution_attempt_id,
                provider_profile_id=provider_profile_id,
                provider_profile_version=provider_profile_version,
                resolved_spec_fingerprint=resolved_spec_fingerprint,
            )
        grant = self._policy.issue_resource_grant(
            mode=mode,
            profile_version=self._security_profile_version,
            scenario_id=scenario_id,
            principal=principal,
            run_id=current.run_id,
            action=action,
            scope=scope,
            selector_attestation_ref=selector_ref,
            selector_request=selector_request,
            operation_fingerprint=fingerprint,
            stockroom_context=stockroom_context,
        )
        request = PermissionRequest(
            principal=principal,
            run_id=current.run_id,
            mode=mode,
            observed=current,
            authoritative=current,
            action=action,
            resource_scope=scope,
            resource_grant=grant,
            profile_version=self._security_profile_version,
            scenario_id=scenario_id,
            requester_authority=AuthorityStatus.GRANTED,
            task_scope_authority=AuthorityStatus.GRANTED,
            limit_authority=AuthorityStatus.GRANTED,
            budget_authority=AuthorityStatus.GRANTED,
            idempotency_authority=AuthorityStatus.GRANTED,
            target_control_authority=AuthorityStatus.NOT_APPLICABLE,
        )
        decision = self._policy.evaluate(request)
        if decision.decision is not SecurityAdmissionDecision.ALLOW:
            raise ValueError(f"P1_3_SECURITY_DENIED:{scope.domain.value}:{decision.reason}")
        capability = self._policy.issue_capability(decision, request)
        if capability is None:
            raise ValueError("P1_3_CAPABILITY_ISSUANCE_DENIED")
        return CapabilityConsumeRequest(
            capability=capability,
            principal=principal,
            current_mode=mode,
            current=current,
            profile_version=self._security_profile_version,
            action=action,
            scope=scope,
            selector_attestation_ref=selector_ref,
            operation_fingerprint=fingerprint,
        )

    async def _execute_durable_tool(
        self,
        *,
        repository: PostgresExecutionRepository,
        work_run_id: str,
        execution_attempt_id: str,
        principal: str,
        scenario_id: str,
        candidate: ToolCallCandidate,
    ) -> bool:
        profile = self._profile
        broker = self._tool_broker
        authority = self._provider_tool_authority
        dispatcher = self._tool_dispatcher
        if profile is None or broker is None or authority is None or dispatcher is None:
            raise RuntimeError("durable tool dependencies are missing")
        current, attempt = await repository.load_authority(
            work_run_id=work_run_id,
            execution_attempt_id=execution_attempt_id,
        )
        if (
            attempt.status is not ExecutionStatus.RUNNING
            or current.state is not WorkflowState.RUNNING
            or attempt.state is not current.state
            or attempt.state_version != current.state_version
        ):
            if attempt.status is ExecutionStatus.RUNNING:
                await repository.close_workflow_left_running(
                    execution_attempt_id,
                    reason="TOOL_ENTRY_FRESHNESS_DENIED",
                )
            return False
        if attempt.runtime_mode is None:
            raise AuthorityConflictError("durable tool RuntimeMode is missing")
        operations = await repository.load_operations(execution_attempt_id)
        ordinal = len(operations) + 1
        operation_id = _stable_id("tool", execution_attempt_id, str(ordinal), candidate.call_id)
        dispatch_context = (
            self._stockroom_dispatch_context_factory(
                current=current,
                attempt=attempt,
                profile=profile,
                scenario_id=scenario_id,
                operation_id=operation_id,
                provider_call_id=candidate.call_id,
            )
            if self._stockroom_dispatch_context_factory is not None
            else None
        )
        try:
            definition, arguments, fingerprint = broker.validate_candidate(
                candidate,
                mode=attempt.runtime_mode,
                profile_id=profile.profile_id,
                scenario_id=scenario_id,
                dispatch_context=dispatch_context,
            )
            resource_identity = ":".join(
                (
                    broker.registry.registry_id,
                    broker.registry.version,
                    definition.tool_id,
                    definition.schema_version,
                    definition.dispatcher_version,
                )
            )
        except ValueError as exc:
            fingerprint = canonical_sha256(
                {
                    "kind": "UNRESOLVED_TOOL",
                    "name": candidate.name,
                    "arguments_json": candidate.arguments_json,
                    "call_id": candidate.call_id,
                }
            )
            resource_identity = f"UNRESOLVED_TOOL:{candidate.name}"
            await repository.create_operation(
                operation_id=operation_id,
                attempt_id=execution_attempt_id,
                kind=OperationKind.TOOL,
                fingerprint=fingerprint,
                resource_identity=resource_identity,
                call_ordinal=ordinal,
            )
            await repository.fail_operation_before_side_effect(
                operation_id=operation_id,
                reason=str(exc),
                failure_class="SECURITY_DENIAL",
            )
            return False
        await repository.create_operation(
            operation_id=operation_id,
            attempt_id=execution_attempt_id,
            kind=OperationKind.TOOL,
            fingerprint=fingerprint,
            resource_identity=resource_identity,
            call_ordinal=ordinal,
        )
        try:
            self._require_running_context(current, attempt, profile, scenario_id)
            if definition.tool_id not in profile.tool_allowlist:
                raise ValueError("TOOL_NOT_IN_PROVIDER_PROFILE")
            selector = ProviderToolSelectorRequest(
                domain=ResourceDomain.TOOL.value,
                canonical_resource_identity=resource_identity,
                principal=principal,
                work_run_id=current.run_id,
                execution_attempt_id=execution_attempt_id,
                state=current.state,
                state_version=current.state_version,
                runtime_mode=attempt.runtime_mode,
                profile_id=profile.profile_id,
                profile_version=profile.version,
                scenario_id=scenario_id,
                operation_fingerprint=fingerprint,
            )
            attestation = authority.attest(selector)
            capabilities = [
                self._issue_capability(
                    current=current,
                    mode=attempt.runtime_mode,
                    principal=principal,
                    scenario_id=scenario_id,
                    scope=ResourceScope(ResourceDomain.TOOL, resource_identity),
                    selector_ref=attestation.attestation_id,
                    selector_request=selector,
                    fingerprint=fingerprint,
                    execution_attempt_id=execution_attempt_id,
                    provider_profile_id=profile.profile_id,
                    provider_profile_version=profile.version,
                    resolved_spec_fingerprint=(
                        dispatch_context.resolved_spec_fingerprint
                        if dispatch_context is not None
                        else ""
                    ),
                )
            ]
            for requirement in definition.underlying_resource_requirements:
                capabilities.append(
                    self._issue_capability(
                        current=current,
                        mode=attempt.runtime_mode,
                        principal=principal,
                        scenario_id=scenario_id,
                        scope=requirement.scope,
                        selector_ref=None,
                        selector_request=None,
                        fingerprint=fingerprint,
                        action=requirement.action,
                        execution_attempt_id=execution_attempt_id,
                        provider_profile_id=profile.profile_id,
                        provider_profile_version=profile.version,
                        resolved_spec_fingerprint=(
                            dispatch_context.resolved_spec_fingerprint
                            if dispatch_context is not None
                            else ""
                        ),
                    )
                )
            context_requirements: tuple[tuple[ResourceDomain, str], ...] = ()
            if attempt.runtime_mode is RuntimeMode.PUBLIC_BOUNDED_LIVE:
                context_requirements = (
                    (
                        ResourceDomain.REPOSITORY,
                        profile.public_repository_resource_identity,
                    ),
                    (ResourceDomain.SCENARIO, profile.public_scenario_resource_identity),
                )
                for domain, resource_id in context_requirements:
                    capabilities.append(
                        self._issue_capability(
                            current=current,
                            mode=attempt.runtime_mode,
                            principal=principal,
                            scenario_id=scenario_id,
                            scope=ResourceScope(domain, resource_id),
                            selector_ref=None,
                            selector_request=None,
                            fingerprint=fingerprint,
                        )
                    )
            tool_secret_selector: SecretUseSelectorRequest | None = None
            if definition.secret_requirement is not None:
                secret_authority = self._secret_use_authority
                if secret_authority is None:
                    raise AuthorityConflictError("tool SecretUse authority is missing")
                secret_requirement = definition.secret_requirement
                tool_secret_selector = SecretUseSelectorRequest(
                    secret_ref=secret_requirement.secret_ref,
                    secret_class=secret_requirement.secret_class,
                    purpose=secret_requirement.purpose,
                    destination=secret_requirement.destination,
                    canonical_resource_identity=resource_identity,
                    adapter_identity=secret_requirement.dispatcher_identity,
                    principal=principal,
                    work_run_id=current.run_id,
                    execution_attempt_id=execution_attempt_id,
                    operation_id=operation_id,
                    state=current.state,
                    state_version=current.state_version,
                    runtime_mode=attempt.runtime_mode,
                    profile_id=profile.profile_id,
                    profile_version=profile.version,
                    scenario_id=scenario_id,
                    operation_fingerprint=fingerprint,
                )
                secret_attestation = secret_authority.attest(tool_secret_selector)
                secret_identity = hashlib.sha256(secret_requirement.secret_ref.encode()).hexdigest()
                capabilities.append(
                    self._issue_capability(
                        current=current,
                        mode=attempt.runtime_mode,
                        principal=principal,
                        scenario_id=scenario_id,
                        scope=ResourceScope(
                            ResourceDomain.SECRET,
                            f"{secret_requirement.secret_class}:{secret_identity}",
                        ),
                        selector_ref=secret_attestation.attestation_id,
                        selector_request=tool_secret_selector,
                        fingerprint=fingerprint,
                    )
                )
            capability_tuple = tuple(capabilities)
            prepared = broker.prepare_dispatch(
                candidate,
                mode=attempt.runtime_mode,
                profile_id=profile.profile_id,
                scenario_id=scenario_id,
                capabilities=capability_tuple,
                secret_request=tool_secret_selector,
                context_requirements=context_requirements,
                dispatch_context=dispatch_context,
            )
            await repository.advance_operation(
                operation_id,
                ExecutionOperationPhase.SECURITY_ADMITTED,
                refs={
                    "capability_ids": [
                        item.capability.capability_id
                        for item in capability_tuple
                        if item.capability is not None
                    ]
                },
            )
            reservation = await repository.reserve_execution_bounds(
                operation_id=operation_id,
                profile=profile,
                expected_state_version=current.state_version,
                expected_execution_version=attempt.execution_version,
                tool_calls=1,
                budget_units=1,
                now=self._durable_time_source(),
            )
            if not reservation.admitted:
                return False
            consumed = broker.consume_prepared(
                prepared,
                policy=self._policy,
                secret_lease_authority=self._secret_lease_authority,
            )
            dispatch_refs: dict[str, object] = (
                {"secret_lease_id": consumed.secret_lease.lease_id}
                if consumed.secret_lease is not None
                else {}
            )
            fresh = await repository.start_dispatch_if_fresh(
                operation_id=operation_id,
                expected_state_version=current.state_version,
                expected_execution_version=reservation.execution_version,
                refs=dispatch_refs,
            )
            if not fresh:
                if consumed.secret_lease is not None:
                    self._secret_resolver.close(consumed.secret_lease)
                return False
        except (AuthorityConflictError, ValueError) as exc:
            await repository.fail_operation_before_side_effect(
                operation_id=operation_id,
                reason=str(exc),
                failure_class="SECURITY_DENIAL",
            )
            return False
        try:
            output = broker.dispatch_prepared(
                consumed,
                dispatcher=dispatcher,
                secret_resolver=self._secret_resolver,
            )
        except UnknownToolOutcome as exc:
            await repository.advance_operation(
                operation_id,
                ExecutionOperationPhase.OUTCOME_UNKNOWN,
                ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME,
                refs={"sanitized_error": type(exc).__name__, "blind_retry": False},
            )
            await repository.transition_attempt(
                execution_attempt_id,
                "EXECUTION_FAILED",
                refs={
                    "failure_class": "UNKNOWN_OUTCOME",
                    "reason": "TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME",
                    "blind_retry": False,
                },
            )
            return False
        except (AuthorityConflictError, ValueError) as exc:
            await repository.advance_operation(
                operation_id,
                ExecutionOperationPhase.OUTCOME_KNOWN,
                ExecutionOperationOutcome.TOOL_FAILED,
                refs={"sanitized_error": type(exc).__name__},
            )
            failed_current, failed_attempt = await repository.load_authority(
                work_run_id=work_run_id,
                execution_attempt_id=execution_attempt_id,
            )
            if (
                failed_current.state is not WorkflowState.RUNNING
                or failed_attempt.state is not failed_current.state
                or failed_attempt.state_version != failed_current.state_version
            ):
                await repository.close_workflow_left_running(
                    execution_attempt_id,
                    reason="WORKFLOW_LEFT_RUNNING_AFTER_TOOL_EXCEPTION",
                )
            else:
                await repository.transition_attempt(
                    execution_attempt_id,
                    "EXECUTION_FAILED",
                    refs={"failure_class": "FATAL", "reason": "TOOL_FAILED"},
                )
            return False
        durable_output_id = _stable_id(
            "tool-output",
            execution_attempt_id,
            operation_id,
            candidate.call_id,
            output.result_hash,
        )
        await repository.advance_operation(
            operation_id,
            ExecutionOperationPhase.OUTCOME_KNOWN,
            ExecutionOperationOutcome.TOOL_COMPLETED,
            refs={"tool_output_ref": durable_output_id, "result_hash": output.result_hash},
        )
        completed_current, completed_attempt = await repository.load_authority(
            work_run_id=work_run_id,
            execution_attempt_id=execution_attempt_id,
        )
        if (
            completed_current.state is not WorkflowState.RUNNING
            or completed_attempt.state is not completed_current.state
            or completed_attempt.state_version != completed_current.state_version
        ):
            await repository.close_workflow_left_running(
                execution_attempt_id,
                reason="WORKFLOW_LEFT_RUNNING_AFTER_TOOL_DISPATCH",
            )
            return False
        await repository.store_output_ref(
            ref_id=durable_output_id,
            attempt_id=execution_attempt_id,
            kind="ToolOutputRef",
            content_hash=output.result_hash,
            storage_ref=f"private://tool-output/{durable_output_id}",
        )
        if output.output is None:
            raise AuthorityConflictError("durable tool output body is missing")
        tool_item: dict[str, Any] = {
            "type": "function_call_output",
            "call_id": candidate.call_id,
            "output": canonical_json_bytes(output.output).decode("utf-8"),
        }
        await self._store_protocol_items(
            repository,
            execution_attempt_id,
            operation_id,
            (tool_item,),
        )
        self.counters.tool_calls += 1
        self.counters.budget_units += 1
        return True

    async def _store_protocol_items(
        self,
        repository: PostgresExecutionRepository,
        attempt_id: str,
        operation_id: str,
        items: tuple[dict[str, Any], ...],
    ) -> None:
        existing = await repository.load_private_protocol_items(attempt_id)
        ordinal = len(existing)
        for item in items:
            item_type = item.get("type")
            if not isinstance(item_type, str) or not item_type:
                raise AuthorityConflictError("provider protocol item type is missing")
            body = canonical_json_bytes(item)
            ordinal += 1
            call_id = item.get("call_id")
            if call_id is not None and not isinstance(call_id, str):
                raise AuthorityConflictError("provider protocol call_id is malformed")
            item_hash = hashlib.sha256(body).hexdigest()
            state_id = _stable_id(attempt_id, operation_id, str(ordinal), item_hash)
            await repository.store_private_protocol_item(
                state_id=state_id,
                attempt_id=attempt_id,
                operation_id=operation_id,
                ordinal=ordinal,
                item_type=item_type,
                item_hash=item_hash,
                call_id=call_id,
                encrypted_body_ref=f"private://provider-protocol/{state_id}",
                body_bytes=body,
                classification="PRIVATE_PROVIDER_PROTOCOL",
                byte_count=len(body),
            )

    async def _complete_durable_attempt(
        self,
        repository: PostgresExecutionRepository,
        current: WorkflowSnapshot,
        attempt: ExecutionAttemptRef,
        output_text: str,
    ) -> ExecutionSubmissionRef:
        output_hash = hashlib.sha256(output_text.encode()).hexdigest()
        output_id = _stable_id("agent-output", attempt.execution_attempt_id, output_hash)
        await repository.store_output_ref(
            ref_id=output_id,
            attempt_id=attempt.execution_attempt_id,
            kind="AgentOutputRef",
            content_hash=output_hash,
            storage_ref=f"private://agent-output/{output_id}",
        )
        submission_hash = canonical_sha256(
            {
                "execution_attempt_id": attempt.execution_attempt_id,
                "work_run_id": attempt.work_run_id,
                "state": current.state.value,
                "state_version": current.state_version,
                "agent_output_hash": output_hash,
            }
        )
        submission_id = _stable_id(
            "execution-submission", attempt.execution_attempt_id, submission_hash
        )
        status = await repository.transition_attempt(
            attempt.execution_attempt_id,
            "EXECUTION_COMPLETED",
            refs={
                "agent_output_ref": output_id,
                "execution_submission_ref": submission_id,
                "execution_submission_hash": submission_hash,
                "execution_submission_storage_ref": (
                    f"private://execution-submission/{submission_id}"
                ),
            },
        )
        if status is not ExecutionStatus.EXECUTOR_COMPLETED:
            raise AuthorityConflictError("execution completion projection mismatch")
        ref = ExecutionSubmissionRef(
            submission_id=submission_id,
            execution_attempt_id=attempt.execution_attempt_id,
            work_run_id=attempt.work_run_id,
            task_contract_id=attempt.task_contract_id,
            task_contract_version=attempt.task_contract_version,
            state=current.state,
            state_version=current.state_version,
            status=status,
            event_range_hash=submission_hash,
            issuer_ref="AISCC_P1_5_EXECUTION_REF_AUTHORITY_V1",
        )
        authority = self._execution_ref_authority
        if authority is None:
            raise RuntimeError("execution reference authority is missing")
        return authority.register_submission(ref)

    @staticmethod
    async def _recover_nonterminal_operation(
        repository: PostgresExecutionRepository, attempt_id: str
    ) -> bool:
        operations = await repository.load_operations(attempt_id)
        pending = next(
            (
                operation
                for operation in reversed(operations)
                if operation.phase
                in {
                    ExecutionOperationPhase.PREPARED,
                    ExecutionOperationPhase.SECURITY_ADMITTED,
                    ExecutionOperationPhase.DISPATCH_STARTED,
                }
            ),
            None,
        )
        if pending is None:
            return False
        if pending.phase is ExecutionOperationPhase.PREPARED:
            target = ExecutionOperationPhase.OUTCOME_KNOWN
            outcome = ExecutionOperationOutcome.DENIED_BEFORE_SIDE_EFFECT
        elif pending.phase is ExecutionOperationPhase.SECURITY_ADMITTED:
            target = ExecutionOperationPhase.OUTCOME_KNOWN
            outcome = ExecutionOperationOutcome.CANCELLED
        else:
            target = ExecutionOperationPhase.OUTCOME_UNKNOWN
            outcome = ExecutionOperationOutcome.TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
        await repository.advance_operation(
            pending.operation_id,
            target,
            outcome,
            refs={"recovery": "NO_DUPLICATE_SIDE_EFFECT"},
        )
        await repository.transition_attempt(
            attempt_id,
            "EXECUTION_FAILED",
            refs={
                "failure_class": (
                    "UNKNOWN_OUTCOME"
                    if target is ExecutionOperationPhase.OUTCOME_UNKNOWN
                    else "RECOVERY_CONFLICT"
                )
            },
        )
        return True

    def admit_output(self, call: ProviderCall, *, output_bytes: int, output_tokens: int) -> None:
        self._check_open_and_time(call)
        if (
            output_bytes < 0
            or output_tokens < 0
            or self.counters.output_bytes + output_bytes > call.profile.output_byte_bound
            or self.counters.output_tokens + output_tokens > call.profile.output_token_bound
        ):
            self._fail_once("OUTPUT_LIMIT_EXHAUSTED")
            raise ValueError("EXECUTION_LIMIT_EXHAUSTED:OUTPUT")
        self.counters.output_bytes += output_bytes
        self.counters.output_tokens += output_tokens

    def admit_tool_side_effect(self, call: ProviderCall) -> None:
        self._check_open_and_time(call)
        if self.counters.tool_calls >= call.profile.tool_call_maximum:
            self._fail_once("TOOL_CALL_LIMIT_EXHAUSTED")
            raise ValueError("EXECUTION_LIMIT_EXHAUSTED:TOOL_CALLS")
        if self.counters.budget_units >= call.profile.budget_unit_maximum:
            self._fail_once("BUDGET_LIMIT_EXHAUSTED")
            raise ValueError("EXECUTION_LIMIT_EXHAUSTED:BUDGET")
        self.counters.tool_calls += 1
        self.counters.budget_units += 1

    def admit_provider_retry(
        self,
        call: ProviderCall,
        *,
        previous_outcome: ExecutionOperationOutcome,
        known_retryable_rejection: bool = False,
    ) -> None:
        self._check_open_and_time(call)
        if previous_outcome is not ExecutionOperationOutcome.DEFINITELY_NOT_SENT and not (
            previous_outcome is ExecutionOperationOutcome.PROVIDER_REJECTED
            and known_retryable_rejection
        ):
            self._fail_once("PROVIDER_RETRY_OUTCOME_DENIED")
            raise ValueError("PROVIDER_RETRY_OUTCOME_DENIED")
        if self.counters.retries >= call.profile.provider_retry_maximum:
            self._fail_once("PROVIDER_RETRY_LIMIT_EXHAUSTED")
            raise ValueError("EXECUTION_LIMIT_EXHAUSTED:RETRIES")
        self.counters.retries += 1

    def _security_denial(self, call: ProviderCall) -> ProviderResult:
        return ProviderResult(
            call.operation_id,
            "denied",
            ExecutionOperationOutcome.DENIED_BEFORE_SIDE_EFFECT,
            None,
            (),
            None,
            None,
            MappingProxyType({}),
            "SECURITY_CAPABILITY_DENIED",
            call.operation_fingerprint,
        )

    def _check_bounds(self, call: ProviderCall) -> None:
        self._check_open_and_time(call)
        if len(canonical_json_bytes(list(call.input_items))) > call.profile.input_byte_bound:
            self._fail_once("INPUT_LIMIT_EXHAUSTED")
            raise ValueError("EXECUTION_LIMIT_EXHAUSTED:INPUT")
        bounds = (
            (
                self.counters.provider_calls,
                call.profile.provider_call_maximum,
                "PROVIDER_CALL_LIMIT_EXHAUSTED",
            ),
            (
                self.counters.rounds,
                call.profile.agent_round_trip_maximum,
                "AGENT_ROUND_LIMIT_EXHAUSTED",
            ),
            (
                self.counters.budget_units,
                call.profile.budget_unit_maximum,
                "BUDGET_LIMIT_EXHAUSTED",
            ),
        )
        for current, maximum, reason in bounds:
            if current >= maximum:
                self._fail_once(reason)
                raise ValueError(f"EXECUTION_LIMIT_EXHAUSTED:{reason}")

    def _check_open_and_time(self, call: ProviderCall) -> None:
        if self._closed:
            raise ValueError("EXECUTION_ATTEMPT_CLOSED")
        if self._time_source() - self._started_at >= call.profile.total_timeout_seconds:
            self._fail_once("WALL_TIME_LIMIT_EXHAUSTED")
            raise ValueError("EXECUTION_LIMIT_EXHAUSTED:WALL_TIME")

    def _fail_once(self, reason: str) -> None:
        if not self.failure_events:
            self.failure_events.append(reason)
        self._closed = True


class ReplayExecutionService:
    def __init__(self, recorded: dict[str, object]) -> None:
        self._recorded = recorded
        self.invocation_counts = {
            name: 0 for name in ("provider", "tool", "process", "network", "secret")
        }

    def replay(self, replay_id: str) -> object:
        if replay_id not in self._recorded:
            raise ValueError("REPLAY_MISSING_NO_LIVE_FALLBACK")
        record = self._recorded[replay_id]
        if not isinstance(record, dict):
            raise ValueError("REPLAY_CORRUPT_NO_LIVE_FALLBACK")
        status, output, content_hash = (
            record.get("status"),
            record.get("output"),
            record.get("content_hash"),
        )
        if (
            status != ExecutionStatus.EXECUTOR_COMPLETED.value
            or not isinstance(output, str)
            or not isinstance(content_hash, str)
            or hashlib.sha256(output.encode()).hexdigest() != content_hash
        ):
            raise ValueError("REPLAY_CORRUPT_NO_LIVE_FALLBACK")
        return dict(record)


def _stable_id(*parts: str) -> str:
    prefix = parts[0].replace("_", "-")[:28]
    digest = hashlib.sha256("\x00".join(parts).encode()).hexdigest()[:48]
    return f"{prefix}-{digest}"


def _durable_provider_output_token_charge(
    result: ProviderResult,
    *,
    requested_maximum: int | None,
) -> int:
    """Use reported usage exactly, or charge the full server-owned request ceiling."""
    if type(requested_maximum) is not int or requested_maximum <= 0:
        raise ValueError("REQUESTED_MAX_OUTPUT_TOKENS_INVALID")
    if result.sanitized_error == "INVALID_PROVIDER_OUTPUT_TOKEN_USAGE":
        raise ValueError("INVALID_PROVIDER_OUTPUT_TOKEN_USAGE")
    if "output_tokens" not in result.usage:
        return requested_maximum
    reported = result.usage["output_tokens"]
    if type(reported) is not int or reported < 0 or reported > requested_maximum:
        raise ValueError("INVALID_PROVIDER_OUTPUT_TOKEN_USAGE")
    return reported


def _pending_tool_call(items: tuple[dict[str, object], ...]) -> ToolCallCandidate | None:
    completed = {
        item.get("call_id")
        for item in items
        if item.get("type") == "function_call_output" and isinstance(item.get("call_id"), str)
    }
    for item in reversed(items):
        if item.get("type") != "function_call" or item.get("call_id") in completed:
            continue
        name, arguments, call_id = item.get("name"), item.get("arguments"), item.get("call_id")
        if not all(isinstance(value, str) and value for value in (name, arguments, call_id)):
            raise AuthorityConflictError("durable function call is malformed")
        return ToolCallCandidate(str(name), str(arguments), str(call_id))
    return None


def _continuation_call_id(items: tuple[dict[str, object], ...]) -> str | None:
    outputs = [item.get("call_id") for item in items if item.get("type") == "function_call_output"]
    if not outputs:
        return None
    value = outputs[-1]
    return value if isinstance(value, str) and value else None


def _latest_final_text(items: tuple[dict[str, object], ...]) -> str | None:
    for item in reversed(items):
        if item.get("type") != "message" or item.get("role") != "assistant":
            continue
        content = item.get("content")
        if not isinstance(content, list):
            raise AuthorityConflictError("durable assistant message content is malformed")
        values = [
            part.get("text")
            for part in content
            if isinstance(part, dict) and part.get("type") == "output_text"
        ]
        if len(values) != 1 or not isinstance(values[0], str):
            raise AuthorityConflictError("durable assistant output is malformed")
        return values[0]
    return None
