from __future__ import annotations

import json
from dataclasses import dataclass

from aiscc.contracts.security import SecurityDecision
from aiscc.security.redaction import redact_structure


@dataclass(frozen=True, slots=True)
class ProvenanceArtifact:
    event_type: str
    body: str


def decision_artifact(
    decision: SecurityDecision, *, sensitive_values: tuple[str, ...] = ()
) -> ProvenanceArtifact:
    payload: dict[str, object] = {
        "decision": decision.decision.value,
        "reason": decision.reason,
        "guards": list(decision.guards),
        "provenance": dict(decision.provenance),
    }
    safe = redact_structure(payload, sensitive_values=sensitive_values)
    return ProvenanceArtifact(
        event_type="SECURITY_ADMISSION_DECISION",
        body=json.dumps(safe, sort_keys=True, separators=(",", ":")),
    )
