from __future__ import annotations

import json
from pathlib import Path

from aiscc.providers.service import ReplayExecutionService


def test_recorded_replay_and_failure_invoke_nothing() -> None:
    recorded = json.loads(Path("tests/fixtures/providers/recorded_replay.json").read_text())
    service = ReplayExecutionService(recorded)
    assert service.replay("replay-p1-5-fixed")
    try:
        service.replay("missing")
    except ValueError:
        pass
    else:
        raise AssertionError("missing Replay must fail")
    corrupted = dict(recorded)
    corrupted["corrupt"] = {
        "status": "EXECUTOR_COMPLETED",
        "output": "tampered",
        "content_hash": "0" * 64,
    }
    corrupt_service = ReplayExecutionService(corrupted)
    try:
        corrupt_service.replay("corrupt")
    except ValueError:
        pass
    else:
        raise AssertionError("corrupt Replay must fail")
    assert tuple(service.invocation_counts.values()) == (0, 0, 0, 0, 0)
    assert tuple(corrupt_service.invocation_counts.values()) == (0, 0, 0, 0, 0)
