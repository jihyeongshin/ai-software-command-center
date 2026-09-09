from __future__ import annotations

from typing import Protocol

from aiscc.contracts.workflow import WorkflowSnapshot
from aiscc.providers.models import (
    ExecutionAttemptRef,
    ProviderCall,
    ProviderResult,
    ProviderToolSelectorAttestation,
    ProviderToolSelectorRequest,
    SecretResolutionLease,
    SecretUseSelectorAttestation,
    SecretUseSelectorRequest,
    ToolDefinition,
    ToolOutputRef,
)
from aiscc.security.capability import CapabilityConsumeRequest, CapabilityConsumptionReceipt


class ProviderAdapter(Protocol):
    def call(self, call: ProviderCall, *, secret: str) -> ProviderResult: ...


class ExecutionAuthorityReader(Protocol):
    def load(
        self, *, work_run_id: str, execution_attempt_id: str
    ) -> tuple[WorkflowSnapshot, ExecutionAttemptRef]: ...


class ProviderToolResourcePolicyPort(Protocol):
    def attest(self, request: ProviderToolSelectorRequest) -> ProviderToolSelectorAttestation: ...
    def verify(self, attestation_ref: str, request: ProviderToolSelectorRequest) -> bool: ...


class SecretUseAuthorityPort(Protocol):
    def attest(self, request: SecretUseSelectorRequest) -> SecretUseSelectorAttestation: ...
    def verify(self, attestation_ref: str, request: SecretUseSelectorRequest) -> bool: ...


class SecretResolver(Protocol):
    def resolve(self, lease: SecretResolutionLease) -> str: ...
    def close(self, lease: SecretResolutionLease) -> None: ...


class ToolDispatcher(Protocol):
    def dispatch(
        self,
        definition: ToolDefinition,
        arguments: dict[str, object],
        *,
        secret: str | None = None,
    ) -> ToolOutputRef: ...


class ReceiptAwareToolDispatcher(Protocol):
    def dispatch_with_receipts(
        self,
        definition: ToolDefinition,
        arguments: dict[str, object],
        *,
        receipts: tuple[CapabilityConsumptionReceipt, ...],
        requirements: tuple[CapabilityConsumeRequest, ...],
        dispatch_identity: str,
    ) -> ToolOutputRef: ...
