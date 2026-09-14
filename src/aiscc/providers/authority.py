from __future__ import annotations

import hashlib
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from aiscc.contracts.security import ResourceDomain
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.providers.models import (
    ExecutionAttemptRef,
    ExecutionStatus,
    ExecutionSubmissionRef,
    ProviderToolSelectorAttestation,
    ProviderToolSelectorRequest,
    SecretResolutionLease,
    SecretUseSelectorAttestation,
    SecretUseSelectorRequest,
)
from aiscc.security.capability import CapabilityConsumeRequest, CapabilityConsumptionReceipt
from aiscc.workflow.models import GuardId, TransitionRequest


class ProviderToolResourceAuthority:
    def __init__(
        self,
        issuer_ref: str = "AISCC_P1_5_RESOURCE_AUTHORITY_V1",
        *,
        allowed_resource_identities: frozenset[str],
        allowed_profile_ids: frozenset[str],
        allowed_scenarios: frozenset[str],
        allowed_modes: frozenset[RuntimeMode],
        ttl_seconds: int = 20,
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
    ) -> None:
        self.issuer_ref = issuer_ref
        if ttl_seconds <= 0:
            raise ValueError("authority TTL must be positive")
        self._ttl = timedelta(seconds=ttl_seconds)
        self._clock = clock
        self._allowed_resource_identities = allowed_resource_identities
        self._allowed_profile_ids = allowed_profile_ids
        self._allowed_scenarios = allowed_scenarios
        self._allowed_modes = allowed_modes
        self._sequence = 0
        self._attestations: dict[str, ProviderToolSelectorAttestation] = {}
        self._revoked: set[str] = set()
        self._uses: dict[str, int] = {}

    def attest(self, request: ProviderToolSelectorRequest) -> ProviderToolSelectorAttestation:
        _validate_request(request.operation_fingerprint, request.work_run_id)
        if (
            request.domain not in {"PROVIDER", "TOOL"}
            or request.canonical_resource_identity not in self._allowed_resource_identities
            or request.profile_id not in self._allowed_profile_ids
            or request.scenario_id not in self._allowed_scenarios
            or request.runtime_mode not in self._allowed_modes
        ):
            raise ValueError("provider/tool request is outside server-owned authority")
        self._sequence += 1
        now = self._clock()
        value = ProviderToolSelectorAttestation(
            f"provider-tool-attestation-{self._sequence}",
            "p1-5-v1",
            request,
            now,
            now + self._ttl,
            1,
            self.issuer_ref,
        )
        self._attestations[value.attestation_id] = value
        return value

    def verify(self, attestation_ref: str, request: ProviderToolSelectorRequest) -> bool:
        value = self._attestations.get(attestation_ref)
        if not (
            value
            and value.request == request
            and value.expires_at > self._clock()
            and attestation_ref not in self._revoked
            and self._uses.get(attestation_ref, 0) < value.max_uses
        ):
            return False
        self._uses[attestation_ref] = self._uses.get(attestation_ref, 0) + 1
        return True

    def revoke(self, attestation_ref: str) -> None:
        self._revoked.add(attestation_ref)


class SecretUseAuthority:
    def __init__(
        self,
        issuer_ref: str = "AISCC_P1_5_SECRET_USE_AUTHORITY_V1",
        *,
        allowed_secret_refs: frozenset[str],
        allowed_profile_ids: frozenset[str],
        allowed_scenarios: frozenset[str],
        allowed_destinations: frozenset[str],
        allowed_modes: frozenset[RuntimeMode],
        ttl_seconds: int = 20,
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
    ) -> None:
        self.issuer_ref = issuer_ref
        if ttl_seconds <= 0:
            raise ValueError("authority TTL must be positive")
        self._ttl = timedelta(seconds=ttl_seconds)
        self._clock = clock
        self._allowed_secret_refs = allowed_secret_refs
        self._allowed_profile_ids = allowed_profile_ids
        self._allowed_scenarios = allowed_scenarios
        self._allowed_destinations = allowed_destinations
        self._allowed_modes = allowed_modes
        self._sequence = 0
        self._attestations: dict[str, SecretUseSelectorAttestation] = {}
        self._revoked: set[str] = set()
        self._uses: dict[str, int] = {}

    def attest(self, request: SecretUseSelectorRequest) -> SecretUseSelectorAttestation:
        _validate_request(request.operation_fingerprint, request.secret_ref)
        if (
            request.secret_ref not in self._allowed_secret_refs
            or request.profile_id not in self._allowed_profile_ids
            or request.scenario_id not in self._allowed_scenarios
            or request.destination not in self._allowed_destinations
            or request.runtime_mode not in self._allowed_modes
        ):
            raise ValueError("secret use request is outside server-owned authority")
        self._sequence += 1
        now = self._clock()
        value = SecretUseSelectorAttestation(
            f"secret-use-attestation-{self._sequence}",
            "p1-5-v1",
            request,
            hashlib.sha256(request.secret_ref.encode()).hexdigest(),
            now,
            now + self._ttl,
            1,
            self.issuer_ref,
        )
        self._attestations[value.attestation_id] = value
        return value

    def verify(self, attestation_ref: str, request: SecretUseSelectorRequest) -> bool:
        value = self._attestations.get(attestation_ref)
        if not (
            value
            and value.request == request
            and value.expires_at > self._clock()
            and attestation_ref not in self._revoked
            and self._uses.get(attestation_ref, 0) < value.max_uses
        ):
            return False
        self._uses[attestation_ref] = self._uses.get(attestation_ref, 0) + 1
        return True

    def revoke(self, attestation_ref: str) -> None:
        self._revoked.add(attestation_ref)


class SecretResolutionLeaseAuthority:
    """Issues resolver-only leases from P1-3 issuer-backed consumption receipts."""

    def __init__(
        self,
        receipt_verifier: Callable[[CapabilityConsumptionReceipt, CapabilityConsumeRequest], bool],
        *,
        issuer_ref: str = "AISCC_P1_5_SECRET_LEASE_AUTHORITY_V1",
        ttl_seconds: int = 10,
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
    ) -> None:
        if ttl_seconds <= 0 or ttl_seconds > 30:
            raise ValueError("secret lease TTL must be positive and bounded")
        self.issuer_ref = issuer_ref
        self._receipt_verifier = receipt_verifier
        self._ttl = timedelta(seconds=ttl_seconds)
        self._clock = clock
        self._issuer_token = object()
        self._sequence = 0
        self._leases: dict[str, SecretResolutionLease] = {}
        self._resolved: set[str] = set()
        self._closed: set[str] = set()
        self._revoked: set[str] = set()

    def issue(
        self,
        receipt: CapabilityConsumptionReceipt,
        requirement: CapabilityConsumeRequest,
        secret_request: SecretUseSelectorRequest,
    ) -> SecretResolutionLease:
        capability = requirement.capability
        secret_identity_hash = hashlib.sha256(secret_request.secret_ref.encode()).hexdigest()
        if not (
            capability is not None
            and requirement.scope.domain is ResourceDomain.SECRET
            and self._receipt_verifier(receipt, requirement)
            and receipt.capability_id == capability.capability_id
            and requirement.selector_attestation_ref is not None
            and requirement.scope.resource_id
            == f"{secret_request.secret_class}:{secret_identity_hash}"
            and requirement.principal == secret_request.principal
            and requirement.current.run_id == secret_request.work_run_id
            and requirement.current.state is secret_request.state
            and requirement.current.state_version == secret_request.state_version
            and requirement.current_mode is secret_request.runtime_mode
            and requirement.operation_fingerprint == secret_request.operation_fingerprint
        ):
            raise ValueError("SECRET_CONSUMPTION_RECEIPT_DENIED")
        self._sequence += 1
        now = self._clock()
        lease = SecretResolutionLease(
            lease_id=f"secret-resolution-lease-{self._sequence}",
            secret_ref=secret_request.secret_ref,
            secret_identity_hash=secret_identity_hash,
            capability_id=receipt.capability_id,
            consumed_use_ordinal=receipt.consumed_use_ordinal,
            principal=secret_request.principal,
            work_run_id=secret_request.work_run_id,
            execution_attempt_id=secret_request.execution_attempt_id,
            operation_id=secret_request.operation_id,
            state=secret_request.state,
            state_version=secret_request.state_version,
            runtime_mode=secret_request.runtime_mode,
            profile_id=secret_request.profile_id,
            profile_version=secret_request.profile_version,
            scenario_id=secret_request.scenario_id,
            purpose=secret_request.purpose,
            destination=secret_request.destination,
            operation_fingerprint=secret_request.operation_fingerprint,
            expires_at=now + self._ttl,
            issuer_ref=self.issuer_ref,
            _issuer_token=self._issuer_token,
        )
        self._leases[lease.lease_id] = lease
        return lease

    def consume_for_resolution(self, lease: SecretResolutionLease) -> bool:
        valid = bool(
            lease._issuer_token is self._issuer_token
            and self._leases.get(lease.lease_id) is lease
            and lease.expires_at > self._clock()
            and lease.lease_id not in self._resolved
            and lease.lease_id not in self._closed
            and lease.lease_id not in self._revoked
        )
        if valid:
            self._resolved.add(lease.lease_id)
        return valid

    def close(self, lease: SecretResolutionLease) -> None:
        if self._leases.get(lease.lease_id) is not lease:
            raise ValueError("SECRET_LEASE_FORGED")
        self._closed.add(lease.lease_id)

    def revoke(self, lease: SecretResolutionLease) -> None:
        if self._leases.get(lease.lease_id) is not lease:
            raise ValueError("SECRET_LEASE_FORGED")
        self._revoked.add(lease.lease_id)


class LeaseBoundSecretResolver:
    """Private resolver: a raw secret_ref is never an accepted input."""

    def __init__(
        self,
        authority: SecretResolutionLeaseAuthority,
        material_by_ref: dict[str, str],
    ) -> None:
        self._authority = authority
        self._material_by_ref = dict(material_by_ref)
        self.invocation_count = 0

    def resolve(self, lease: SecretResolutionLease) -> str:
        if not isinstance(
            lease, SecretResolutionLease
        ) or not self._authority.consume_for_resolution(lease):
            raise ValueError("SECRET_LEASE_DENIED")
        material = self._material_by_ref.get(lease.secret_ref)
        if material is None:
            raise ValueError("SECRET_REFERENCE_UNRESOLVED")
        self.invocation_count += 1
        return material

    def close(self, lease: SecretResolutionLease) -> None:
        self._authority.close(lease)


def _validate_request(fingerprint: str, identity: str) -> None:
    if len(fingerprint) != 64 or any(char not in "0123456789abcdef" for char in fingerprint):
        raise ValueError("operation fingerprint must be lowercase SHA-256")
    if not identity:
        raise ValueError("authority request identity is required")


class ExecutionReferenceAuthority:
    """Issuer-backed P1-5 refs; it has no P1-4 guard issuer handle."""

    def __init__(self, issuer_ref: str = "AISCC_P1_5_EXECUTION_REF_AUTHORITY_V1") -> None:
        self.issuer_ref = issuer_ref
        self._refs: dict[str, object] = {}

    def register_start(self, ref: ExecutionAttemptRef) -> ExecutionAttemptRef:
        if (
            ref.status is not ExecutionStatus.NOT_STARTED
            or ref.state is not WorkflowState.READY
            or ref.execution_version != 1
            or ref.issuer_ref != self.issuer_ref
        ):
            raise ValueError("start ref requires NOT_STARTED attempt")
        self._refs[ref.execution_attempt_id] = ref
        return ref

    def register_submission(self, ref: ExecutionSubmissionRef) -> ExecutionSubmissionRef:
        if ref.issuer_ref == "AISCC_P1_5_LOCAL_IDE_SELF_DOGFOOD_V1" or ref.submission_id.startswith(
            "external-ide-submission:"
        ):
            raise ValueError("external IDE authority requires durable owner verification")
        if (
            ref.status is not ExecutionStatus.EXECUTOR_COMPLETED
            or ref.state is not WorkflowState.RUNNING
            or ref.issuer_ref != self.issuer_ref
            or len(ref.event_range_hash) != 64
            or any(character not in "0123456789abcdef" for character in ref.event_range_hash)
        ):
            raise ValueError("submission ref requires EXECUTOR_COMPLETED attempt")
        self._refs[ref.submission_id] = ref
        return ref

    def resolve_external_submission(self, verified) -> ExecutionSubmissionRef:
        """Enroll only a committed, durable-owner verified external producer receipt."""
        from aiscc.providers.external_ide import VerifiedExternalIdeExecutionSubmissionV1

        if type(verified) is not VerifiedExternalIdeExecutionSubmissionV1:
            raise ValueError("durable external owner receipt required")
        ref = verified.common_ref
        self._refs[ref.submission_id] = ref
        return ref

    def verify(self, ref: object, request: TransitionRequest, guard_id: GuardId) -> bool:
        if guard_id is GuardId.G_EXECUTION_STARTED and isinstance(ref, ExecutionAttemptRef):
            return bool(
                self._refs.get(ref.execution_attempt_id) is ref
                and ref.work_run_id == request.work_run_id
                and ref.task_contract_id == request.task_contract_id
                and ref.task_contract_version == request.task_contract_version
                and ref.state is request.observed_state
                and ref.state_version == request.observed_state_version
                and ref.status is ExecutionStatus.NOT_STARTED
            )
        if guard_id is GuardId.G_EXECUTOR_SUBMISSION and isinstance(ref, ExecutionSubmissionRef):
            return bool(
                self._refs.get(ref.submission_id) is ref
                and ref.work_run_id == request.work_run_id
                and ref.task_contract_id == request.task_contract_id
                and ref.task_contract_version == request.task_contract_version
                and ref.state is request.observed_state
                and ref.state_version == request.observed_state_version
                and ref.status is ExecutionStatus.EXECUTOR_COMPLETED
            )
        return False
