"""Canonical P1-3/P1-4/P1-5 owners used by the private initializer."""

from __future__ import annotations

import hashlib
from datetime import datetime

from aiscc.contracts.security import (
    AuthorityStatus,
    PermissionRequest,
    ResourceDomain,
    ResourceScope,
    SecurityActionClass,
    SecurityAdmissionDecision,
)
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState
from aiscc.persistence.repository import PostgresTransitionRepository
from aiscc.providers.authority import ExecutionReferenceAuthority
from aiscc.public_live.initializer import StartOwners
from aiscc.public_live.start_authority import (
    PublicLiveStartCandidate,
    PublicLiveStartContextAuthority,
    StartContextReceipt,
    StartContract,
)
from aiscc.public_live.start_repository import StartLease
from aiscc.security.capability import CapabilityConsumeRequest
from aiscc.security.policy import SecurityPolicy
from aiscc.workflow.guards import P1_4GuardAuthority, TrustedGuardFact
from aiscc.workflow.kernel import WorkflowKernel
from aiscc.workflow.models import GuardId, RequesterType, TransitionRequest


class CanonicalStartOwners:
    def __init__(
        self,
        *,
        contract: StartContract,
        kernel: WorkflowKernel,
        repository: PostgresTransitionRepository,
        guard_authority: P1_4GuardAuthority,
        execution_refs: ExecutionReferenceAuthority,
        context_authority: PublicLiveStartContextAuthority,
        security_policy: SecurityPolicy,
    ) -> None:
        self.contract = contract
        self.kernel = kernel
        self.repository = repository
        self.guards = guard_authority
        self.execution_refs = execution_refs
        self.contexts = context_authority
        self.security = security_policy
        self._admitted: dict[bytes, StartContextReceipt] = {}

    def ports(self) -> StartOwners:
        return StartOwners(
            self.create_ready,
            self.admit_start,
            self.prepare_attempt,
            self.start_workflow,
            self.start_execution,
        )

    async def create_ready(self, lease: StartLease) -> str:
        request = self._request(lease, None, 0, WorkflowState.READY, "genesis")
        decision = await self.kernel.request_transition(request, self._base_facts(request))
        if decision.resulting_state is not WorkflowState.READY:
            raise RuntimeError("START_GENESIS_DENIED")
        run = await self.kernel.verify_consistency(lease.work_run_id)
        if run.state is not WorkflowState.READY or run.state_version != 1:
            raise RuntimeError("START_GENESIS_INVALID")
        return run.work_run_id

    async def admit_start(self, lease: StartLease) -> None:
        run = await self.kernel.verify_consistency(lease.work_run_id)
        if run.state is not WorkflowState.READY or run.state_version != 1:
            raise RuntimeError("START_READY_REQUIRED")
        candidate = self._candidate(lease)
        now = datetime.fromisoformat(lease.candidate["authority_now"])
        receipt = self.contexts.issue(
            candidate, state=run.state, state_version=run.state_version, now=now
        )
        current = WorkflowSnapshot(run.work_run_id, run.state, run.state_version)
        consumes = []
        for scope in self._start_scopes():
            context = self.contexts.issue_resource_context(receipt, current=current, scope=scope)
            grant = self.security.issue_resource_grant(
                mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
                profile_version="p1-3-v2",
                scenario_id="stockroom-s1-normal",
                principal="aiscc-public-live-initializer",
                run_id=run.work_run_id,
                action=SecurityActionClass.START_EXECUTION_CONTROL,
                scope=scope,
                ttl_seconds=10,
                selector_request=context,
                operation_fingerprint=receipt.operation_fingerprint,
                stockroom_context=context,
                now=now,
            )
            request = PermissionRequest(
                principal="aiscc-public-live-initializer",
                run_id=run.work_run_id,
                mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
                observed=current,
                authoritative=current,
                action=SecurityActionClass.START_EXECUTION_CONTROL,
                resource_scope=scope,
                resource_grant=grant,
                profile_version="p1-3-v2",
                scenario_id="stockroom-s1-normal",
                requester_authority=AuthorityStatus.GRANTED,
                task_scope_authority=AuthorityStatus.GRANTED,
                limit_authority=AuthorityStatus.GRANTED,
                budget_authority=AuthorityStatus.GRANTED,
                idempotency_authority=AuthorityStatus.GRANTED,
                target_control_authority=AuthorityStatus.NOT_APPLICABLE,
            )
            decision = self.security.evaluate(request)
            if decision.decision is not SecurityAdmissionDecision.ALLOW:
                raise RuntimeError("START_EXECUTION_CONTROL_DENIED")
            capability = self.security.issue_capability(
                decision, request, ttl_seconds=10, max_uses=1, now=now
            )
            consumes.append(
                CapabilityConsumeRequest(
                    capability=capability,
                    principal=request.principal,
                    current_mode=request.mode,
                    current=current,
                    profile_version=request.profile_version,
                    action=SecurityActionClass.START_EXECUTION_CONTROL,
                    scope=scope,
                    operation_fingerprint=receipt.operation_fingerprint,
                )
            )
        uses, _ = self.security.consume_capabilities_atomically_with_receipts(
            tuple(consumes), now=now
        )
        if len(uses) != 2 or not all(use.allowed for use in uses):
            raise RuntimeError("START_CAPABILITY_CONSUME_DENIED")
        self.contexts.consume(receipt, now=now)
        self._admitted[lease.run_id] = receipt

    async def prepare_attempt(self, lease: StartLease) -> str:
        if lease.run_id not in self._admitted:
            raise RuntimeError("START_ADMISSION_REQUIRED")
        attempt_id = self._attempt_id(lease)
        row = await self.repository.create_attempt(
            attempt_id=attempt_id,
            work_run_id=lease.work_run_id,
            profile_id="public-live-luna-v1",
            profile_version="1",
            registry_id="aiscc-stockroom-tools",
            registry_version="2",
        )
        return row.execution_attempt_id

    async def start_workflow(self, lease: StartLease, attempt_id: str) -> None:
        receipt = self._admitted.get(lease.run_id)
        if receipt is None:
            raise RuntimeError("START_ADMISSION_REQUIRED")
        current, ref = await self.repository.load_authority(
            work_run_id=lease.work_run_id, execution_attempt_id=attempt_id
        )
        if current.state is not WorkflowState.READY:
            raise RuntimeError("START_READY_REQUIRED")
        registered = self.execution_refs.register_start(ref)
        request = self._request(lease, WorkflowState.READY, 1, WorkflowState.RUNNING, "running")
        facts = (
            *self._base_facts(request),
            self.guards.issue_from_execution_ref(
                guard_id=GuardId.G_EXECUTION_STARTED,
                execution_ref=registered,
                verifier=self.execution_refs,
                request=request,
            ),
        )
        decision = await self.kernel.request_transition(request, facts)
        if decision.resulting_state is not WorkflowState.RUNNING:
            raise RuntimeError("START_WORKFLOW_DENIED")

    async def start_execution(self, lease: StartLease, attempt_id: str) -> None:
        status = await self.repository.transition_attempt(
            attempt_id,
            "EXECUTION_STARTED",
            refs={
                "start_candidate": lease.candidate_id.hex(),
                "start_admission": self._admitted[lease.run_id].operation_fingerprint,
            },
        )
        if status.value != "RUNNING":
            raise RuntimeError("START_EXECUTION_DENIED")

    def _request(
        self,
        lease: StartLease,
        observed: WorkflowState | None,
        version: int,
        target: WorkflowState,
        phase: str,
    ) -> TransitionRequest:
        digest = hashlib.sha256(
            lease.candidate_id + phase.encode() + version.to_bytes(8, "big")
        ).hexdigest()
        return TransitionRequest(
            transition_request_id=f"pl-start-{phase}-{digest}"[:128],
            project_id=(
                f"{self.contract.payload['repository_identity']}@"
                f"{self.contract.payload['repository_version']}"
            ),
            task_contract_id="aiscc-public-live-stockroom-v1",
            task_contract_version="1",
            work_run_id=lease.work_run_id,
            observed_state=observed,
            observed_state_version=version,
            target_state=target,
            requester_identity="aiscc-public-live-initializer",
            requester_type=RequesterType.SYSTEM,
            runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        )

    def _base_facts(self, request: TransitionRequest) -> tuple[TrustedGuardFact, ...]:
        return tuple(
            self.guards.issue(
                guard_id=guard,
                satisfied=True,
                reason="PUBLIC_LIVE_FIXED_START_CONTRACT_VERIFIED",
                authority_ref=f"public-live-start-v1:{guard.value}",
                request=request,
            )
            for guard in (GuardId.G_CONTRACT, GuardId.G_SCOPE, GuardId.G_RUNTIME_CONTEXT)
        )

    def _candidate(self, lease: StartLease) -> PublicLiveStartCandidate:
        value = lease.candidate
        return PublicLiveStartCandidate(
            lease.run_id,
            value["campaign_id"],
            int(value["gate_version"]),
            datetime.fromisoformat(value["admitted_at"]),
            datetime.fromisoformat(value["deadline"]),
            value["idempotency_ref"],
            value["admitted_payload_hash"],
            value["reservation_ref"],
            int(value["slot_generation"]),
            value["requester_ref"],
            value["policy_digest"],
            value["content_digest"],
            value["contract_digest"],
        )

    def _attempt_id(self, lease: StartLease) -> str:
        return (
            "pl-start-attempt-"
            + hashlib.sha256(
                lease.candidate_id + lease.work_run_id.encode() + b"\0READY\01\0ordinal-1"
            ).hexdigest()
        )[:128]

    def _start_scopes(self) -> tuple[ResourceScope, ResourceScope]:
        return (
            ResourceScope(
                ResourceDomain.REPOSITORY,
                f"{self.contract.payload['repository_identity']}@"
                f"{self.contract.payload['repository_version']}",
            ),
            ResourceScope(
                ResourceDomain.SCENARIO,
                f"scenario:{self.contract.payload['scenario_id']}@"
                f"{self.contract.payload['scenario_version']}",
            ),
        )
