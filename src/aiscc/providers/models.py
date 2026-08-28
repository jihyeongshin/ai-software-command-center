from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from types import MappingProxyType
from typing import Any

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowState


class ExecutionStatus(StrEnum):
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    EXECUTOR_COMPLETED = "EXECUTOR_COMPLETED"
    EXECUTION_FAILED = "EXECUTION_FAILED"


class ExecutionOperationPhase(StrEnum):
    PREPARED = "PREPARED"
    SECURITY_ADMITTED = "SECURITY_ADMITTED"
    DISPATCH_STARTED = "DISPATCH_STARTED"
    OUTCOME_KNOWN = "OUTCOME_KNOWN"
    OUTCOME_UNKNOWN = "OUTCOME_UNKNOWN"


class ExecutionOperationOutcome(StrEnum):
    DENIED_BEFORE_SIDE_EFFECT = "DENIED_BEFORE_SIDE_EFFECT"
    DEFINITELY_NOT_SENT = "DEFINITELY_NOT_SENT"
    PROVIDER_REJECTED = "PROVIDER_REJECTED"
    PROVIDER_COMPLETED = "PROVIDER_COMPLETED"
    PROVIDER_INCOMPLETE = "PROVIDER_INCOMPLETE"
    TOOL_COMPLETED = "TOOL_COMPLETED"
    TOOL_FAILED = "TOOL_FAILED"
    TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME = "TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME"
    CANCELLED = "CANCELLED"


class ExecutionAttemptFailureClass(StrEnum):
    FATAL = "FATAL"
    CANCELLED = "CANCELLED"
    RETRY_EXHAUSTED = "RETRY_EXHAUSTED"
    UNKNOWN_OUTCOME = "UNKNOWN_OUTCOME"
    WORKFLOW_LEFT_RUNNING = "WORKFLOW_LEFT_RUNNING"
    RECOVERY_CONFLICT = "RECOVERY_CONFLICT"
    LIMIT_EXHAUSTED = "LIMIT_EXHAUSTED"


class SideEffectClass(StrEnum):
    READ_ONLY = "READ_ONLY"
    IDEMPOTENT_BY_KEY = "IDEMPOTENT_BY_KEY"
    NON_IDEMPOTENT = "NON_IDEMPOTENT"


class OperationKind(StrEnum):
    PROVIDER = "PROVIDER"
    TOOL = "TOOL"


class ProviderInputAuthority(StrEnum):
    INITIAL_SERVER = "INITIAL_SERVER"
    DURABLE_LOCAL = "DURABLE_LOCAL"


@dataclass(frozen=True, slots=True)
class ProviderCanonicalIdentity:
    profile_id: str
    profile_version: str
    provider_id: str
    model_ref_hash: str
    adapter_protocol_version: str

    def serialized(self) -> str:
        return ":".join(
            (
                self.profile_id,
                self.profile_version,
                self.provider_id,
                self.model_ref_hash,
                self.adapter_protocol_version,
            )
        )


@dataclass(frozen=True, slots=True)
class ExecutionAttemptRef:
    execution_attempt_id: str
    work_run_id: str
    task_contract_id: str
    task_contract_version: str
    state: WorkflowState
    state_version: int
    execution_version: int
    status: ExecutionStatus
    issuer_ref: str
    runtime_mode: RuntimeMode | None = None
    project_id: str | None = None
    provider_profile_id: str | None = None
    provider_profile_version: str | None = None
    tool_registry_id: str | None = None
    tool_registry_version: str | None = None


@dataclass(frozen=True, slots=True)
class ExecutionSubmissionRef:
    submission_id: str
    execution_attempt_id: str
    work_run_id: str
    task_contract_id: str
    task_contract_version: str
    state: WorkflowState
    state_version: int
    status: ExecutionStatus
    event_range_hash: str
    issuer_ref: str


@dataclass(frozen=True, slots=True)
class AgentOutputRef:
    output_id: str
    content_hash: str
    byte_count: int


@dataclass(frozen=True, slots=True)
class ToolOutputRef:
    output_id: str
    operation_id: str
    argument_hash: str
    result_hash: str
    output: dict[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class ExecutionArtifactRef:
    artifact_id: str
    content_hash: str
    classification: str


@dataclass(frozen=True, slots=True)
class ExecutionAttempt:
    execution_attempt_id: str
    work_run_id: str
    attempt_ordinal: int
    task_contract_id: str
    task_contract_version: str
    runtime_mode: RuntimeMode
    provider_profile_id: str
    provider_profile_version: str
    tool_registry_id: str
    tool_registry_version: str
    creation_state: WorkflowState
    creation_state_version: int
    status: ExecutionStatus
    execution_version: int
    created_at: datetime
    parent_attempt_id: str | None = None


@dataclass(frozen=True, slots=True)
class ExecutionOperation:
    operation_id: str
    execution_attempt_id: str
    kind: OperationKind
    fingerprint: str
    phase: ExecutionOperationPhase
    call_ordinal: int
    resource_identity: str
    outcome: ExecutionOperationOutcome | None = None
    parent_operation_id: str | None = None


@dataclass(frozen=True, slots=True)
class DurableExecutionCounters:
    schema_version: str
    provider_calls: int
    agent_rounds: int
    tool_calls: int
    provider_retries: int
    output_bytes: int
    output_tokens: int
    budget_units: int
    started_at: datetime | None
    deadline_at: datetime | None


@dataclass(frozen=True, slots=True)
class DurableBoundReservation:
    admitted: bool
    reason: str
    counters: DurableExecutionCounters
    execution_version: int


@dataclass(frozen=True, slots=True)
class ProviderProfile:
    profile_id: str
    version: str
    provider_id: str
    adapter_protocol_version: str
    model_ref: str
    endpoint_ref: str
    base_url: str
    secret_ref: str
    allowed_runtime_modes: frozenset[RuntimeMode]
    scenario_allowlist: frozenset[str]
    public_repository_identity: str
    public_repository_version: str
    public_scenario_identity: str
    public_scenario_version: str
    tool_registry_id: str
    tool_registry_version: str
    tool_allowlist: frozenset[str]
    provider_call_maximum: int
    agent_round_trip_maximum: int
    tool_call_maximum: int
    provider_retry_maximum: int
    connect_timeout_seconds: float
    read_timeout_seconds: float
    total_timeout_seconds: float
    output_token_bound: int
    output_byte_bound: int
    input_byte_bound: int
    continuation_item_maximum: int
    continuation_byte_bound: int
    continuation_token_estimate_bound: int
    budget_unit_maximum: int
    private_protocol_retention_policy_ref: str
    budget_policy_ref: str
    data_classification_policy_ref: str
    issued_at: datetime
    revoked_at: datetime | None
    enabled: bool

    @property
    def canonical_identity(self) -> ProviderCanonicalIdentity:
        model_hash = hashlib.sha256(self.model_ref.encode()).hexdigest()
        return ProviderCanonicalIdentity(
            self.profile_id,
            self.version,
            self.provider_id,
            model_hash,
            self.adapter_protocol_version,
        )

    @property
    def provider_resource_identity(self) -> str:
        return self.canonical_identity.serialized()

    @property
    def secret_resource_identity(self) -> str:
        return f"PROVIDER_API:{hashlib.sha256(self.secret_ref.encode()).hexdigest()}"

    @property
    def public_repository_resource_identity(self) -> str:
        return f"{self.public_repository_identity}@{self.public_repository_version}"

    @property
    def public_scenario_resource_identity(self) -> str:
        return f"scenario:{self.public_scenario_identity}@{self.public_scenario_version}"


@dataclass(frozen=True, slots=True)
class ProviderToolSelectorRequest:
    domain: str
    canonical_resource_identity: str
    principal: str
    work_run_id: str
    execution_attempt_id: str
    state: WorkflowState
    state_version: int
    runtime_mode: RuntimeMode
    profile_id: str
    profile_version: str
    scenario_id: str
    operation_fingerprint: str


@dataclass(frozen=True, slots=True)
class ProviderToolSelectorAttestation:
    attestation_id: str
    version: str
    request: ProviderToolSelectorRequest
    issued_at: datetime
    expires_at: datetime
    max_uses: int
    issuer_ref: str


@dataclass(frozen=True, slots=True)
class SecretUseSelectorRequest:
    secret_ref: str
    secret_class: str
    purpose: str
    destination: str
    canonical_resource_identity: str
    adapter_identity: str
    principal: str
    work_run_id: str
    execution_attempt_id: str
    operation_id: str
    state: WorkflowState
    state_version: int
    runtime_mode: RuntimeMode
    profile_id: str
    profile_version: str
    scenario_id: str
    operation_fingerprint: str


@dataclass(frozen=True, slots=True)
class SecretUseSelectorAttestation:
    attestation_id: str
    version: str
    request: SecretUseSelectorRequest
    secret_identity_hash: str
    issued_at: datetime
    expires_at: datetime
    max_uses: int
    issuer_ref: str


@dataclass(frozen=True, slots=True)
class SecretResolutionLease:
    lease_id: str
    secret_ref: str
    secret_identity_hash: str
    capability_id: str
    consumed_use_ordinal: int
    principal: str
    work_run_id: str
    execution_attempt_id: str
    operation_id: str
    state: WorkflowState
    state_version: int
    runtime_mode: RuntimeMode
    profile_id: str
    profile_version: str
    scenario_id: str
    purpose: str
    destination: str
    operation_fingerprint: str
    expires_at: datetime
    issuer_ref: str
    _issuer_token: object = field(repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class ResourceRequirement:
    scope: ResourceScope
    action: SecurityActionClass


@dataclass(frozen=True, slots=True)
class SecretRequirement:
    secret_ref: str
    secret_class: str
    purpose: str
    destination: str
    dispatcher_identity: str


@dataclass(frozen=True, slots=True)
class ToolDefinition:
    tool_id: str
    schema_version: str
    dispatcher_version: str
    description: str
    input_schema: dict[str, Any]
    side_effect_classification: SideEffectClass
    allowed_modes: frozenset[RuntimeMode]
    allowed_profiles: frozenset[str]
    allowed_scenarios: frozenset[str]
    underlying_resource_requirements: tuple[ResourceRequirement, ...]
    secret_requirement: SecretRequirement | None
    timeout_seconds: float
    retry_maximum: int
    idempotency_policy: str
    output_byte_bound: int
    output_schema: dict[str, Any]
    enabled: bool
    issued_at: datetime
    revoked_at: datetime | None

    @property
    def underlying_resource_domains(self) -> frozenset[ResourceDomain]:
        domains = {
            requirement.scope.domain for requirement in self.underlying_resource_requirements
        }
        if self.secret_requirement is not None:
            domains.add(ResourceDomain.SECRET)
        return frozenset(domains)


@dataclass(frozen=True, slots=True)
class ToolRegistry:
    registry_id: str
    version: str
    tools: MappingProxyType[str, ToolDefinition]


@dataclass(frozen=True, slots=True)
class ToolCallCandidate:
    name: str
    arguments_json: str
    call_id: str


@dataclass(frozen=True, slots=True)
class ProviderCall:
    operation_id: str
    operation_fingerprint: str
    execution_attempt_id: str
    work_run_id: str
    state: WorkflowState
    state_version: int
    runtime_mode: RuntimeMode
    principal: str
    scenario_id: str
    execution_version: int
    profile: ProviderProfile
    input_items: tuple[dict[str, Any], ...]
    tools: tuple[dict[str, Any], ...]
    call_ordinal: int
    input_authority: ProviderInputAuthority = ProviderInputAuthority.INITIAL_SERVER
    durable_continuation_hash: str | None = None
    output_token_maximum: int | None = None


@dataclass(frozen=True, slots=True)
class ProviderResult:
    operation_id: str
    status: str
    outcome: ExecutionOperationOutcome
    response_id: str | None
    output_items: tuple[dict[str, Any], ...]
    output_text: str | None
    tool_call: ToolCallCandidate | None
    usage: MappingProxyType[str, int]
    sanitized_error: str | None
    result_hash: str


def canonical_json_bytes(value: Any) -> bytes:
    _validate_json(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def parse_strict_json_object(raw: str) -> dict[str, Any]:
    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result

    value = json.loads(raw, object_pairs_hook=pairs, parse_constant=_reject_constant)
    if not isinstance(value, dict):
        raise ValueError("JSON arguments must be an object")
    _validate_json(value)
    return value


def _reject_constant(value: str) -> None:
    raise ValueError(f"invalid JSON number: {value}")


def _validate_json(value: Any) -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        raise ValueError("floating-point input is not accepted by the exact canonical subset")
    if isinstance(value, list):
        for item in value:
            _validate_json(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("JSON object keys must be strings")
            _validate_json(item)
        return
    raise ValueError("unrepresentable canonical JSON input")
