from __future__ import annotations

from dataclasses import replace
from datetime import datetime

from aiscc.contracts.security import SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode, WorkflowSnapshot
from aiscc.security.cancel import CancelIntentStore, CancelRequest, PublicRunControlGrant


def _grant(snapshot: WorkflowSnapshot, expires_at: datetime) -> PublicRunControlGrant:
    return PublicRunControlGrant(
        "grant-1",
        "v1",
        "public-user-1",
        "session-1",
        snapshot.run_id,
        "request-1",
        SecurityActionClass.PUBLIC_CANCEL_CONTROL,
        RuntimeMode.PUBLIC_BOUNDED_LIVE,
        "p1-3-v2",
        "scenario-v1",
        snapshot.state_version,
        expires_at,
    )


def _request(snapshot: WorkflowSnapshot, grant: PublicRunControlGrant) -> CancelRequest:
    return CancelRequest(
        grant.principal,
        grant.session_id,
        snapshot.run_id,
        snapshot,
        grant.profile_version,
        grant.scenario_version,
        "cancel-key-1",
        grant,
    )


def test_cancel_requires_requester_session_target_binding(
    snapshot: WorkflowSnapshot, future_time: datetime
) -> None:
    grant = _grant(snapshot, future_time)
    request = _request(snapshot, grant)

    admitted = CancelIntentStore().authorize(request, snapshot)
    wrong_session = CancelIntentStore().authorize(replace(request, session_id="attacker"), snapshot)
    no_grant = CancelIntentStore().authorize(replace(request, grant=None), snapshot)

    assert admitted.admitted
    assert wrong_session.reason == "CANCEL_REQUESTER_SESSION_MISMATCH"
    assert no_grant.reason == "CANCEL_TARGET_NOT_AUTHORIZED"


def test_run_visibility_is_not_cancel_authority(
    snapshot: WorkflowSnapshot, future_time: datetime
) -> None:
    grant = _grant(snapshot, future_time)
    visible_run_request = replace(_request(snapshot, grant), principal="replay-reader")
    assert not CancelIntentStore().authorize(visible_run_request, snapshot).admitted


def test_cancel_is_idempotent(snapshot: WorkflowSnapshot, future_time: datetime) -> None:
    store = CancelIntentStore()
    request = _request(snapshot, _grant(snapshot, future_time))
    assert store.authorize(request, snapshot) == store.authorize(request, snapshot)
    assert store.control_effect_count == 1
