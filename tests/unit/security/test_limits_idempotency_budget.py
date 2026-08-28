from __future__ import annotations

from aiscc.security.limits import BudgetLedger, IdempotencyLedger, SlidingWindowThrottle


def test_idempotency_replays_once_and_rejects_conflict() -> None:
    ledger = IdempotencyLedger()
    assert ledger.admit("identity-1", "hash-a").allowed
    assert ledger.admit("identity-1", "hash-a").reason == "IDEMPOTENCY_REPLAY"
    assert ledger.admit("identity-1", "hash-b").reason == "IDEMPOTENCY_CONFLICT"
    assert ledger.operation_count == 1


def test_budget_and_unknown_throttle_fail_closed() -> None:
    budget = BudgetLedger(2)
    assert budget.reserve(2).allowed
    assert budget.reserve(1).reason == "BUDGET_EXHAUSTED"
    assert budget.simulated_paid_effects == 1
    assert SlidingWindowThrottle(None, None).admit(0).reason == "THROTTLE_POLICY_UNKNOWN"
