from __future__ import annotations

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LimitDecision:
    allowed: bool
    reason: str


class IdempotencyLedger:
    def __init__(self) -> None:
        self._payloads: dict[str, str] = {}
        self.operation_count = 0

    def admit(self, identity: str, payload_hash: str) -> LimitDecision:
        previous = self._payloads.get(identity)
        if previous is None:
            self._payloads[identity] = payload_hash
            self.operation_count += 1
            return LimitDecision(True, "IDEMPOTENCY_NEW")
        if previous == payload_hash:
            return LimitDecision(True, "IDEMPOTENCY_REPLAY")
        return LimitDecision(False, "IDEMPOTENCY_CONFLICT")


class BudgetLedger:
    def __init__(self, limit: int) -> None:
        if limit <= 0:
            raise ValueError("budget limit must be positive")
        self.limit = limit
        self.used = 0
        self.simulated_paid_effects = 0

    def reserve(self, amount: int) -> LimitDecision:
        if amount <= 0:
            return LimitDecision(False, "BUDGET_AMOUNT_INVALID")
        if self.used + amount > self.limit:
            return LimitDecision(False, "BUDGET_EXHAUSTED")
        self.used += amount
        self.simulated_paid_effects += 1
        return LimitDecision(True, "BUDGET_RESERVED")


class SlidingWindowThrottle:
    def __init__(self, limit: int | None, window_seconds: float | None) -> None:
        self.limit = limit
        self.window_seconds = window_seconds
        self._events: deque[float] = deque()

    def admit(self, now: float) -> LimitDecision:
        if self.limit is None or self.window_seconds is None:
            return LimitDecision(False, "THROTTLE_POLICY_UNKNOWN")
        if self.limit <= 0 or self.window_seconds <= 0:
            return LimitDecision(False, "THROTTLE_POLICY_INVALID")
        while self._events and now - self._events[0] >= self.window_seconds:
            self._events.popleft()
        if len(self._events) >= self.limit:
            return LimitDecision(False, "THROTTLE_LIMIT")
        self._events.append(now)
        return LimitDecision(True, "THROTTLE_ALLOWED")
