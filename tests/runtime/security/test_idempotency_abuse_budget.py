from __future__ import annotations

import pytest

from aiscc.security.limits import BudgetLedger, IdempotencyLedger, SlidingWindowThrottle


@pytest.mark.runtime
def test_duplicate_budget_and_throttle_prevent_duplicate_simulated_effect() -> None:
    idempotency = IdempotencyLedger()
    budget = BudgetLedger(1)
    throttle = SlidingWindowThrottle(1, 60)

    assert idempotency.admit("principal|run|action|key", "payload-a").allowed
    assert budget.reserve(1).allowed
    assert throttle.admit(0).allowed
    assert idempotency.admit("principal|run|action|key", "payload-a").reason == "IDEMPOTENCY_REPLAY"
    assert idempotency.operation_count == 1
    assert budget.reserve(1).reason == "BUDGET_EXHAUSTED"
    assert budget.simulated_paid_effects == 1
    assert throttle.admit(1).reason == "THROTTLE_LIMIT"
    assert SlidingWindowThrottle(None, None).admit(1).reason == "THROTTLE_POLICY_UNKNOWN"
