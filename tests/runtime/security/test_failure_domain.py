from __future__ import annotations

from collections.abc import Callable

import pytest

from aiscc.contracts.security import (
    AuthorityStatus,
    PermissionRequest,
    ResourceDomain,
    SecurityActionClass,
    SecurityAdmissionDecision,
)
from aiscc.contracts.workflow import RuntimeMode
from aiscc.security.policy import SecurityPolicy


@pytest.mark.runtime
def test_live_budget_failure_does_not_disable_recorded_replay(
    policy: SecurityPolicy,
    request_factory: Callable[..., PermissionRequest],
) -> None:
    live = policy.evaluate(request_factory(budget_authority=AuthorityStatus.DENIED))
    replay = policy.evaluate(
        request_factory(
            mode=RuntimeMode.PUBLIC_RECORDED_REPLAY,
            action=SecurityActionClass.REPLAY_READ_ONLY,
            resource_domain=ResourceDomain.FILESYSTEM,
            resource_id="recorded:artifact-1",
            scenario_id=None,
            budget_authority=AuthorityStatus.GRANTED,
        )
    )
    assert live.decision is SecurityAdmissionDecision.DENY
    assert replay.decision is SecurityAdmissionDecision.ALLOW
