from __future__ import annotations

from collections.abc import Callable

from aiscc.contracts.security import PermissionRequest
from aiscc.security.policy import SecurityPolicy
from aiscc.security.provenance import decision_artifact


def test_decision_provenance_is_deterministic_and_redacts_canary(
    policy: SecurityPolicy,
    request_factory: Callable[..., PermissionRequest],
) -> None:
    canary = "sk-AISCC0123456789-canary"
    decision = policy.evaluate(request_factory(resource_id=f"synthetic:{canary}"))
    artifact = decision_artifact(decision, sensitive_values=(canary,))

    assert artifact.event_type == "SECURITY_ADMISSION_DECISION"
    assert canary not in artifact.body
    assert "[REDACTED]" in artifact.body
    assert artifact.body == decision_artifact(decision, sensitive_values=(canary,)).body
