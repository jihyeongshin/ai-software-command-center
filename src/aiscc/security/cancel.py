from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from aiscc.contracts.security import SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot, WorkflowState


@dataclass(frozen=True, slots=True)
class PublicRunControlGrant:
    grant_id: str
    version: str
    principal: str
    session_id: str
    target_run_id: str
    originating_request_id: str
    action: SecurityActionClass
    mode: RuntimeMode
    profile_version: str
    scenario_version: str
    issued_state_version: int
    expires_at: datetime
    revoked: bool = False
    delegate_principal: str | None = None
    delegate_session_id: str | None = None


@dataclass(frozen=True, slots=True)
class CancelRequest:
    principal: str
    session_id: str
    target_run_id: str
    observed: WorkflowSnapshot
    profile_version: str
    scenario_version: str
    idempotency_key: str
    grant: PublicRunControlGrant | None


@dataclass(frozen=True, slots=True)
class CancelIntent:
    intent_id: str
    target_run_id: str
    idempotency_identity: str
    admitted: bool
    reason: str


class CancelIntentStore:
    """P1-3 in-memory proof store; not production durability or workflow state."""

    def __init__(self) -> None:
        self._intents: dict[str, CancelIntent] = {}
        self.control_effect_count = 0

    def authorize(
        self,
        request: CancelRequest,
        current: WorkflowSnapshot,
        now: datetime | None = None,
    ) -> CancelIntent:
        current_time = now or datetime.now(UTC)
        grant = request.grant
        identity = "|".join(
            (
                request.principal,
                request.session_id,
                grant.grant_id if grant is not None else "no-grant",
                request.target_run_id,
                request.idempotency_key,
            )
        )
        existing = self._intents.get(identity)
        if existing is not None:
            return existing
        reason = self._deny_reason(request, current, current_time)
        admitted = reason is None
        intent = CancelIntent(
            intent_id=f"cancel-{len(self._intents) + 1}",
            target_run_id=request.target_run_id,
            idempotency_identity=identity,
            admitted=admitted,
            reason="CANCEL_INTENT_ADMITTED" if admitted else str(reason),
        )
        self._intents[identity] = intent
        if admitted:
            self.control_effect_count += 1
        return intent

    @staticmethod
    def _deny_reason(
        request: CancelRequest, current: WorkflowSnapshot, now: datetime
    ) -> str | None:
        grant = request.grant
        if grant is None:
            return "CANCEL_TARGET_NOT_AUTHORIZED"
        direct = request.principal == grant.principal and request.session_id == grant.session_id
        delegated = (
            request.principal == grant.delegate_principal
            and request.session_id == grant.delegate_session_id
            and grant.delegate_principal is not None
        )
        checks = (
            (direct or delegated, "CANCEL_REQUESTER_SESSION_MISMATCH"),
            (request.target_run_id == grant.target_run_id, "CANCEL_TARGET_MISMATCH"),
            (grant.action is SecurityActionClass.PUBLIC_CANCEL_CONTROL, "CANCEL_ACTION_MISMATCH"),
            (grant.mode is RuntimeMode.PUBLIC_BOUNDED_LIVE, "CANCEL_MODE_MISMATCH"),
            (request.profile_version == grant.profile_version, "CANCEL_PROFILE_MISMATCH"),
            (request.scenario_version == grant.scenario_version, "CANCEL_SCENARIO_MISMATCH"),
            (not grant.revoked, "CANCEL_GRANT_REVOKED"),
            (now < grant.expires_at, "CANCEL_GRANT_EXPIRED"),
            (request.observed == current, "CANCEL_TARGET_STALE"),
            (current.run_id == grant.target_run_id, "CANCEL_CURRENT_RUN_MISMATCH"),
            (current.state is WorkflowState.RUNNING, "ACTION_STATE_NOT_ADMISSIBLE"),
            (current.state_version >= grant.issued_state_version, "CANCEL_GRANT_VERSION_INVALID"),
        )
        for passed, reason in checks:
            if not passed:
                return reason
        return None
