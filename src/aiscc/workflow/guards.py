from __future__ import annotations

import base64
import binascii
import re
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Protocol

from aiscc.contracts.workflow import WorkflowState
from aiscc.providers.models import ExecutionSubmissionRef
from aiscc.workflow.models import GuardId, GuardSemanticOwner, TransitionRequest

_EXECUTION_BOUND_PREFIXES = (
    "aiscc-bound-ref:v1:execution-submission:",
    "aiscc-bound-ref:v1:execution-attempt:",
)


def encode_execution_bound_refs(submission_id: str, execution_attempt_id: str) -> tuple[str, ...]:
    """Canonical V1 identity encoding; encoding alone confers no authority."""
    result = []
    for prefix, identifier in zip(
        _EXECUTION_BOUND_PREFIXES, (submission_id, execution_attempt_id), strict=True
    ):
        if not isinstance(identifier, str) or not identifier:
            raise ValueError("NON_CANONICAL_BOUND_REF")
        payload = base64.urlsafe_b64encode(identifier.encode("utf-8", errors="strict"))
        result.append(prefix + payload.rstrip(b"=").decode("ascii"))
    return tuple(result)


def decode_execution_bound_refs(bound_refs: tuple[str, ...]) -> tuple[str, str]:
    if not isinstance(bound_refs, tuple) or len(bound_refs) != 2:
        raise ValueError("NON_CANONICAL_BOUND_REF")
    identifiers = []
    for prefix, ref in zip(_EXECUTION_BOUND_PREFIXES, bound_refs, strict=True):
        if not isinstance(ref, str) or not ref.startswith(prefix):
            raise ValueError("NON_CANONICAL_BOUND_REF")
        payload = ref[len(prefix) :]
        if re.fullmatch(r"[A-Za-z0-9_-]+", payload) is None:
            raise ValueError("NON_CANONICAL_BOUND_REF")
        try:
            raw = base64.b64decode(
                payload + "=" * (-len(payload) % 4), altchars=b"-_", validate=True
            )
            identifier = raw.decode("utf-8", errors="strict")
        except (binascii.Error, UnicodeError) as exc:
            raise ValueError("NON_CANONICAL_BOUND_REF") from exc
        if not identifier or base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii") != payload:
            raise ValueError("NON_CANONICAL_BOUND_REF")
        identifiers.append(identifier)
    return identifiers[0], identifiers[1]


GUARD_OWNER_POLICY = MappingProxyType(
    {
        GuardId.G_CURRENT: GuardSemanticOwner.P1_4_SYSTEM,
        GuardId.G_CONTRACT: GuardSemanticOwner.P1_4_SYSTEM,
        GuardId.G_SCOPE: GuardSemanticOwner.P1_4_SYSTEM,
        GuardId.G_RUNTIME_CONTEXT: GuardSemanticOwner.P1_4_SYSTEM,
        GuardId.G_EXECUTION_STARTED: GuardSemanticOwner.P1_4_SYSTEM,
        GuardId.G_EXECUTOR_SUBMISSION: GuardSemanticOwner.P1_4_SYSTEM,
        GuardId.G_EVIDENCE: GuardSemanticOwner.P1_6_EVIDENCE,
        GuardId.G_HUMAN_REQUIRED: GuardSemanticOwner.P1_7_HUMAN,
        GuardId.G_HUMAN_NOT_REQUIRED: GuardSemanticOwner.P1_7_HUMAN,
        GuardId.G_NO_PENDING_HUMAN_GATE: GuardSemanticOwner.P1_7_HUMAN,
        GuardId.G_SUSPENDED_HUMAN_GATE: GuardSemanticOwner.P1_7_HUMAN,
        GuardId.G_RESUMABLE_HUMAN_GATE: GuardSemanticOwner.P1_7_HUMAN,
        GuardId.G_HUMAN_APPROVED: GuardSemanticOwner.P1_7_HUMAN,
        GuardId.G_HUMAN_REWORK: GuardSemanticOwner.P1_7_HUMAN,
        GuardId.G_HUMAN_REJECTED: GuardSemanticOwner.P1_7_HUMAN,
        GuardId.G_JUDGMENT_ACCEPTED: GuardSemanticOwner.P1_7_JUDGMENT,
        GuardId.G_JUDGMENT_REJECTED: GuardSemanticOwner.P1_7_JUDGMENT,
        GuardId.G_JUDGMENT_REWORK: GuardSemanticOwner.P1_7_JUDGMENT,
        GuardId.G_BLOCKER: GuardSemanticOwner.P1_4_SYSTEM,
        GuardId.G_BLOCKER_RESOLVED: GuardSemanticOwner.P1_4_SYSTEM,
        GuardId.G_REWORK_SPEC: GuardSemanticOwner.P1_4_SYSTEM,
        GuardId.G_FAILURE_TERMINAL: GuardSemanticOwner.P1_4_SYSTEM,
    }
)

_HUMAN_RESULT_GUARDS = frozenset(
    {GuardId.G_HUMAN_APPROVED, GuardId.G_HUMAN_REWORK, GuardId.G_HUMAN_REJECTED}
)
_JUDGMENT_GUARDS = frozenset(
    {
        GuardId.G_JUDGMENT_ACCEPTED,
        GuardId.G_JUDGMENT_REJECTED,
        GuardId.G_JUDGMENT_REWORK,
    }
)


@dataclass(frozen=True, slots=True)
class TrustedGuardFact:
    guard_id: GuardId
    semantic_owner: GuardSemanticOwner
    satisfied: bool
    reason: str
    authority_ref: str
    bound_refs: tuple[str, ...]
    task_contract_id: str
    task_contract_version: str
    work_run_id: str
    state_version: int
    _issuer_token: object = field(repr=False, compare=False)


class FutureOwnerGuardVerifier(Protocol):
    """Owner-specific authenticity port implemented by a future semantic owner."""

    @property
    def semantic_owner(self) -> GuardSemanticOwner: ...

    def recognizes(self, fact: TrustedGuardFact, request: TransitionRequest) -> bool: ...


class ExecutionRefVerifier(Protocol):
    def verify(self, ref: object, request: TransitionRequest, guard_id: GuardId) -> bool: ...


class P1_4GuardAuthority:
    """Issues only P1-4-owned facts; future-owner guards are never mintable here."""

    semantic_owner = GuardSemanticOwner.P1_4_SYSTEM

    def __init__(self, authority_id: str = "AISCC_P1_4_SYSTEM_GUARD_AUTHORITY_V1") -> None:
        if not authority_id:
            raise ValueError("guard authority ID must be non-empty")
        self.authority_id = authority_id
        self._issuer_token = object()
        self._execution_facts: dict[int, TrustedGuardFact] = {}

    def issue(
        self,
        *,
        guard_id: GuardId,
        satisfied: bool,
        reason: str,
        authority_ref: str,
        request: TransitionRequest,
    ) -> TrustedGuardFact:
        if guard_id is GuardId.G_CURRENT:
            raise ValueError("G_CURRENT is produced only by the transition authority")
        if guard_id is GuardId.G_EXECUTOR_SUBMISSION:
            raise ValueError("G_EXECUTOR_SUBMISSION requires an issuer-verified execution ref")
        if GUARD_OWNER_POLICY[guard_id] is not self.semantic_owner:
            raise ValueError(f"{guard_id.value} is not owned by P1-4")
        if not reason or not authority_ref:
            raise ValueError("trusted guard facts require reason and authority provenance")
        return TrustedGuardFact(
            guard_id=guard_id,
            semantic_owner=self.semantic_owner,
            satisfied=satisfied,
            reason=reason,
            authority_ref=authority_ref,
            bound_refs=required_bound_refs(guard_id, request),
            task_contract_id=request.task_contract_id,
            task_contract_version=request.task_contract_version,
            work_run_id=request.work_run_id,
            state_version=request.observed_state_version,
            _issuer_token=self._issuer_token,
        )

    def recognizes(self, fact: TrustedGuardFact) -> bool:
        return fact._issuer_token is self._issuer_token and (
            fact.guard_id is not GuardId.G_EXECUTOR_SUBMISSION
            or self._execution_facts.get(id(fact)) is fact
        )

    def issue_from_execution_ref(
        self,
        *,
        guard_id: GuardId,
        execution_ref: object,
        verifier: ExecutionRefVerifier,
        request: TransitionRequest,
    ) -> TrustedGuardFact:
        if guard_id not in {GuardId.G_EXECUTION_STARTED, GuardId.G_EXECUTOR_SUBMISSION}:
            raise ValueError("only P1-5 execution refs use this validation path")
        if not verifier.verify(execution_ref, request, guard_id):
            raise ValueError("unrecognized or mismatched P1-5 execution ref")
        if guard_id is GuardId.G_EXECUTOR_SUBMISSION:
            if not isinstance(execution_ref, ExecutionSubmissionRef):
                raise ValueError("G_EXECUTOR_SUBMISSION requires ExecutionSubmissionRef")
            bound_refs = encode_execution_bound_refs(
                execution_ref.submission_id, execution_ref.execution_attempt_id
            )
            required_bound_refs(guard_id, request, execution_bound_refs=bound_refs)
            fact = TrustedGuardFact(
                guard_id=guard_id,
                semantic_owner=self.semantic_owner,
                satisfied=True,
                reason="P1_5_EXECUTION_REF_VERIFIED",
                authority_ref="p1-5:ExecutionSubmissionRef",
                bound_refs=bound_refs,
                task_contract_id=request.task_contract_id,
                task_contract_version=request.task_contract_version,
                work_run_id=request.work_run_id,
                state_version=request.observed_state_version,
                _issuer_token=self._issuer_token,
            )
            self._execution_facts[id(fact)] = fact
            return fact
        return self.issue(
            guard_id=guard_id,
            satisfied=True,
            reason="P1_5_EXECUTION_REF_VERIFIED",
            authority_ref=f"p1-5:{type(execution_ref).__name__}",
            request=request,
        )


def required_bound_refs(
    guard_id: GuardId,
    request: TransitionRequest,
    *,
    execution_bound_refs: tuple[str, ...] = (),
) -> tuple[str, ...]:
    if guard_id is GuardId.G_EXECUTOR_SUBMISSION:
        decode_execution_bound_refs(execution_bound_refs)
        if (
            request.observed_state is not WorkflowState.RUNNING
            or request.target_state is not WorkflowState.ADMISSION_PENDING
        ):
            raise ValueError("execution submission binding requires RUNNING to ADMISSION_PENDING")
        return execution_bound_refs
    if guard_id is GuardId.G_EVIDENCE:
        return request.evidence_refs
    if guard_id in _HUMAN_RESULT_GUARDS:
        return request.human_result_refs
    if guard_id in _JUDGMENT_GUARDS:
        return request.judgment_refs
    if guard_id is GuardId.G_BLOCKER and request.blocker_claim is not None:
        return (request.blocker_claim.blocker_ref,)
    if guard_id is GuardId.G_BLOCKER_RESOLVED and request.blocker_resolution_claim is not None:
        claim = request.blocker_resolution_claim
        return (claim.blocker_ref, claim.resolution_source_ref)
    return ()


def fact_matches_request(fact: TrustedGuardFact, request: TransitionRequest) -> bool:
    try:
        expected_refs = required_bound_refs(
            fact.guard_id, request, execution_bound_refs=fact.bound_refs
        )
    except ValueError:
        return False
    return (
        fact.semantic_owner is GUARD_OWNER_POLICY[fact.guard_id]
        and fact.bound_refs == expected_refs
        and fact.task_contract_id == request.task_contract_id
        and fact.task_contract_version == request.task_contract_version
        and fact.work_run_id == request.work_run_id
        and fact.state_version == request.observed_state_version
    )


def verifier_matches_fact(
    verifier: FutureOwnerGuardVerifier,
    fact: TrustedGuardFact,
    request: TransitionRequest,
) -> bool:
    return (
        verifier.semantic_owner is fact.semantic_owner
        and fact.semantic_owner is not GuardSemanticOwner.P1_4_SYSTEM
        and fact_matches_request(fact, request)
        and verifier.recognizes(fact, request)
    )


def p1_4_authority_matches_fact(
    authority: P1_4GuardAuthority,
    fact: TrustedGuardFact,
    request: TransitionRequest,
) -> bool:
    return (
        fact.semantic_owner is GuardSemanticOwner.P1_4_SYSTEM
        and fact_matches_request(fact, request)
        and authority.recognizes(fact)
    )
