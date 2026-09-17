"""Fixed server-owned Public Live initialization authority.

This module can validate a start candidate and mint a short-lived, single-use
READY-context receipt.  It does not write WorkflowState or execute providers.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from aiscc.contracts.security import ResourceDomain, ResourceScope, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState

START_CONTRACT_UNAVAILABLE = "START_CONTRACT_UNAVAILABLE"
_MANIFEST_PATH = Path(__file__).parents[3] / "config" / "public_live" / "start-contract.v1.json"


def canonical_bytes(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


@dataclass(frozen=True, slots=True)
class StartContract:
    payload: dict[str, Any]
    digest: str

    @classmethod
    def load(cls, path: Path = _MANIFEST_PATH) -> StartContract:
        try:
            raw = path.read_bytes()
            payload = json.loads(raw)
        except (OSError, json.JSONDecodeError) as exc:
            raise RuntimeError(START_CONTRACT_UNAVAILABLE) from exc
        required = {
            "schema_version": "PUBLIC_LIVE_START_CONTRACT_V1",
            "task_contract_id": "aiscc-public-live-stockroom-v1",
            "task_contract_version": "1",
            "runtime_mode": RuntimeMode.PUBLIC_BOUNDED_LIVE.value,
            "scenario_id": "stockroom-s1-normal",
            "scenario_version": "1.0.0",
            "repository_identity": "repository:synthetic-stockroom",
            "provider_profile_id": "public-live-luna-v1",
            "provider_profile_version": "1",
        }
        if any(payload.get(key) != value for key, value in required.items()):
            raise RuntimeError(START_CONTRACT_UNAVAILABLE)
        digest = hashlib.sha256(canonical_bytes(payload)).hexdigest()
        return cls(payload, digest)


@dataclass(frozen=True, slots=True)
class PublicLiveStartCandidate:
    public_run_id: bytes
    campaign_id: str
    gate_version: int
    admitted_at: datetime
    deadline: datetime
    idempotency_ref: str
    admitted_payload_hash: str
    reservation_ref: str
    slot_generation: int
    requester_ref: str
    policy_digest: str
    content_digest: str
    contract_digest: str
    schema_version: str = "PUBLIC_LIVE_START_V1"

    def __post_init__(self) -> None:
        if (
            len(self.public_run_id) != 16
            or not self.campaign_id
            or self.gate_version < 1
            or self.admitted_at.tzinfo is None
            or self.deadline.tzinfo is None
            or self.deadline <= self.admitted_at
            or self.deadline - self.admitted_at > timedelta(seconds=90)
            or self.slot_generation < 1
        ):
            raise ValueError("START_CANDIDATE_INVALID")
        for digest in (
            self.admitted_payload_hash,
            self.policy_digest,
            self.content_digest,
            self.contract_digest,
        ):
            if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
                raise ValueError("START_CANDIDATE_DIGEST_INVALID")

    def payload(self, contract: StartContract) -> dict[str, object]:
        if self.contract_digest != contract.digest:
            raise RuntimeError(START_CONTRACT_UNAVAILABLE)
        return {
            "schema_version": self.schema_version,
            "public_run_id": self.public_run_id.hex(),
            "campaign_id": self.campaign_id,
            "gate_version": self.gate_version,
            "admitted_at": self.admitted_at.astimezone(UTC).isoformat(),
            "deadline": self.deadline.astimezone(UTC).isoformat(),
            "runtime_mode": RuntimeMode.PUBLIC_BOUNDED_LIVE.value,
            "scenario_id": contract.payload["scenario_id"],
            "scenario_version": contract.payload["scenario_version"],
            "repository_identity": contract.payload["repository_identity"],
            "repository_version": contract.payload["repository_version"],
            "provider_profile_id": contract.payload["provider_profile_id"],
            "provider_profile_version": contract.payload["provider_profile_version"],
            "task_contract_id": contract.payload["task_contract_id"],
            "task_contract_version": contract.payload["task_contract_version"],
            "contract_digest": self.contract_digest,
            "policy_digest": self.policy_digest,
            "content_digest": self.content_digest,
            "idempotency_ref": self.idempotency_ref,
            "admitted_payload_hash": self.admitted_payload_hash,
            "reservation_ref": self.reservation_ref,
            "slot_generation": self.slot_generation,
            "requester_ref": self.requester_ref,
            "issuer": "PUBLIC_LIVE_CHECKED_ADMISSION_V1",
        }

    def candidate_id(self, contract: StartContract) -> bytes:
        return hashlib.sha256(canonical_bytes(self.payload(contract))).digest()

    @property
    def work_run_id(self) -> str:
        return "public-live-" + self.public_run_id.hex()


@dataclass(frozen=True, slots=True)
class StartContextReceipt:
    candidate_id: bytes
    work_run_id: str
    state_version: int
    operation_fingerprint: str
    expires_at: datetime
    _token: object = field(repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class _StartResourceContext:
    current: WorkflowSnapshot
    principal: str
    scope: ResourceScope
    fingerprint: str
    candidate_id: bytes


class PublicLiveStartContextAuthority:
    """Initializer-only issuer for exact authoritative READY snapshots."""

    def __init__(self, contract: StartContract, *, principal: str) -> None:
        if principal != "aiscc-public-live-initializer":
            raise ValueError("START_PRINCIPAL_DENIED")
        self.contract = contract
        self.principal = principal
        self._token = object()
        self._consumed: set[str] = set()
        self._contexts: list[_StartResourceContext] = []

    def issue(
        self,
        candidate: PublicLiveStartCandidate,
        *,
        state: WorkflowState,
        state_version: int,
        now: datetime,
    ) -> StartContextReceipt:
        if state is not WorkflowState.READY or state_version != 1 or now >= candidate.deadline:
            raise ValueError("START_CONTEXT_DENIED")
        candidate_id = candidate.candidate_id(self.contract)
        fingerprint = hashlib.sha256(
            candidate_id + candidate.work_run_id.encode() + b"\0READY\01\0START_EXECUTION_CONTROL"
        ).hexdigest()
        return StartContextReceipt(
            candidate_id,
            candidate.work_run_id,
            state_version,
            fingerprint,
            min(candidate.deadline, now + timedelta(seconds=10)),
            self._token,
        )

    def consume(self, receipt: StartContextReceipt, *, now: datetime) -> None:
        if receipt._token is not self._token or now >= receipt.expires_at:
            raise ValueError("START_CONTEXT_STALE")
        if receipt.operation_fingerprint in self._consumed:
            raise ValueError("START_CONTEXT_ALREADY_CONSUMED")
        self._consumed.add(receipt.operation_fingerprint)

    def issue_resource_context(
        self,
        receipt: StartContextReceipt,
        *,
        current: WorkflowSnapshot,
        scope: ResourceScope,
    ) -> object:
        identities = {
            ResourceDomain.REPOSITORY: (
                f"{self.contract.payload['repository_identity']}@"
                f"{self.contract.payload['repository_version']}"
            ),
            ResourceDomain.SCENARIO: (
                f"scenario:{self.contract.payload['scenario_id']}@"
                f"{self.contract.payload['scenario_version']}"
            ),
        }
        if not (
            receipt._token is self._token
            and current
            == WorkflowSnapshot(receipt.work_run_id, WorkflowState.READY, receipt.state_version)
            and scope.domain in identities
            and scope == ResourceScope(scope.domain, identities[scope.domain])
        ):
            raise ValueError("START_RESOURCE_CONTEXT_DENIED")
        context = _StartResourceContext(
            current,
            self.principal,
            scope,
            receipt.operation_fingerprint,
            receipt.candidate_id,
        )
        self._contexts.append(context)
        return context

    def allows(
        self,
        context: object,
        *,
        mode: RuntimeMode,
        scenario_id: str | None,
        action: SecurityActionClass,
        scope: ResourceScope,
        principal: str,
        run_id: str,
        operation_fingerprint: str | None,
    ) -> bool:
        return bool(
            isinstance(context, _StartResourceContext)
            and any(context is value for value in self._contexts)
            and mode is RuntimeMode.PUBLIC_BOUNDED_LIVE
            and scenario_id == "stockroom-s1-normal"
            and action is SecurityActionClass.START_EXECUTION_CONTROL
            and principal == self.principal == context.principal
            and run_id == context.current.run_id
            and scope == context.scope
            and operation_fingerprint == context.fingerprint
        )

    def current_matches(self, context: object, current: WorkflowSnapshot) -> bool:
        return bool(
            isinstance(context, _StartResourceContext)
            and any(context is value for value in self._contexts)
            and context.current == current
        )
