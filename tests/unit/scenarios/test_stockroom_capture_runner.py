from __future__ import annotations

import asyncio

import pytest

from aiscc.contracts.workflow import WorkflowState
from aiscc.scenarios.capture_runner import OwnerCallResult, StockroomCaptureRunner
from aiscc.scenarios.driver import StockroomCaptureStatus


class RecordingOwners:
    def __init__(
        self,
        *,
        fail_at: str | None = None,
        fail_status: str = "DENIED",
        overrides: dict[str, tuple[str, WorkflowState, int]] | None = None,
    ) -> None:
        self.calls: list[tuple[str, object]] = []
        self.transition_requests: list[tuple[WorkflowState, WorkflowState, int]] = []
        self.fail_at = fail_at
        self.fail_status = fail_status
        self.overrides = overrides or {}
        self.version = 1

    def _result(self, name: str, state: WorkflowState, status: str = "ADMITTED"):
        self.calls.append((name, state))
        if self.fail_at == name:
            status = self.fail_status
        if name.startswith("transition:") and status == "ADMITTED":
            self.version += 1
            state = WorkflowState(name.split(":", 1)[1])
        result_version = self.version
        if name in self.overrides:
            status, state, result_version = self.overrides[name]
        return OwnerCallResult(status, f"owner:{name}", state, result_version, status)

    async def initial_ready(self, prepared):
        return self._result("initial_ready", WorkflowState.READY)

    async def create_attempt(self, prepared, ready_ref):
        return self._result("create_attempt", WorkflowState.READY)

    async def request_transition(
        self,
        prepared,
        *,
        target,
        observed_state,
        observed_version,
        authority_refs,
    ):
        self.transition_requests.append((target, observed_state, observed_version))
        assert observed_version == self.version
        assert authority_refs and all(ref.startswith("owner:") for ref in authority_refs)
        return self._result(f"transition:{target.value}", observed_state)

    async def seal_security_context(self, prepared, running_ref):
        return self._result("security", WorkflowState.RUNNING)

    async def authorize_runtime(self, prepared, security_context_ref):
        return self._result("grant", WorkflowState.RUNNING)

    async def materialize(self, prepared, security_ref):
        return self._result("materialize", WorkflowState.RUNNING)

    async def execute(self, prepared, materialization_ref):
        return self._result("execute", WorkflowState.RUNNING, "COMPLETED")

    async def submit_runtime_evidence(self, prepared, execution_ref):
        return self._result("submit_runtime", WorkflowState.ADMISSION_PENDING)

    async def submit_static_policy_evidence(self, prepared, running_ref):
        return self._result("submit_static", WorkflowState.RUNNING)

    async def evaluate_evidence(self, prepared, candidate_ref):
        missing = prepared.request.scenario_id.endswith("missing-evidence")
        state = (
            WorkflowState.RUNNING
            if prepared.request.scenario_id.endswith("policy-conflict")
            else WorkflowState.ADMISSION_PENDING
        )
        status = "UNSATISFIED" if missing else "SATISFIED"
        return self._result("evaluate", state, status)

    async def submit_agent_human_claim(self, prepared, execution_ref):
        return self._result("agent_claim", WorkflowState.ADMISSION_PENDING, "REJECTED")

    async def open_human_gate(self, prepared, evidence_ref):
        return self._result("human_gate", WorkflowState.ADMISSION_PENDING, "PENDING")

    async def issue_judgment(self, prepared, *, judgment_status, evidence_ref):
        return self._result(f"judgment:{judgment_status}", WorkflowState.ADMISSION_PENDING)

    async def create_policy_blocker(self, prepared, evidence_ref):
        return self._result("blocker:POLICY:POLICY_CONFLICT", WorkflowState.RUNNING)


def prepared_driver(scenario_id: str):
    from aiscc.contracts.workflow import RuntimeMode
    from aiscc.scenarios import driver
    from aiscc.scenarios.enrollment import StockroomEnrollment

    enrollment = object.__new__(StockroomEnrollment)
    object.__setattr__(enrollment, "mode", RuntimeMode.OWNER_SELF_DOGFOOD)
    object.__setattr__(enrollment, "scenario_id", scenario_id)
    object.__setattr__(enrollment, "scenario_version", "1.0.0")
    binding = object.__new__(driver.StockroomRunPreparationBinding)
    object.__setattr__(binding, "run_id", "run-1")
    object.__setattr__(binding, "attempt_id", "attempt-1")
    object.__setattr__(binding, "expected_initial_state", WorkflowState.READY)
    object.__setattr__(binding, "expected_initial_state_version", 1)
    object.__setattr__(binding, "binding_fingerprint", "0" * 64)
    request = object.__new__(driver.StockroomDriverRequest)
    object.__setattr__(request, "enrollment", enrollment)
    object.__setattr__(request, "run_binding", binding)
    object.__setattr__(request, "configuration_fingerprints", object())
    object.__setattr__(request, "request_fingerprint", "0" * 64)
    prepared = object.__new__(driver.PreparedStockroomDriver)
    object.__setattr__(prepared, "request", request)
    object.__setattr__(prepared, "owners", object())
    return prepared


@pytest.mark.parametrize(
    ("scenario", "target", "expected"),
    [
        (
            "stockroom-s1-normal",
            WorkflowState.ACCEPTED,
            [
                "initial_ready",
                "create_attempt",
                "transition:RUNNING",
                "security",
                "grant",
                "materialize",
                "execute",
                "transition:ADMISSION_PENDING",
                "submit_runtime",
                "evaluate",
                "judgment:ACCEPTED",
                "transition:ACCEPTED",
            ],
        ),
        (
            "stockroom-s2-missing-evidence",
            WorkflowState.REWORK_REQUIRED,
            [
                "initial_ready",
                "create_attempt",
                "transition:RUNNING",
                "security",
                "grant",
                "materialize",
                "execute",
                "transition:ADMISSION_PENDING",
                "evaluate",
                "judgment:HOLD_REWORK_REQUIRED",
                "transition:REWORK_REQUIRED",
            ],
        ),
        (
            "stockroom-s3-policy-conflict",
            WorkflowState.BLOCKED,
            [
                "initial_ready",
                "create_attempt",
                "transition:RUNNING",
                "submit_static",
                "evaluate",
                "blocker:POLICY:POLICY_CONFLICT",
                "transition:BLOCKED",
            ],
        ),
        (
            "stockroom-s4-human-owned-claim",
            WorkflowState.HUMAN_REQUIRED,
            [
                "initial_ready",
                "create_attempt",
                "transition:RUNNING",
                "security",
                "grant",
                "materialize",
                "execute",
                "transition:ADMISSION_PENDING",
                "submit_runtime",
                "evaluate",
                "agent_claim",
                "human_gate",
                "transition:HUMAN_REQUIRED",
            ],
        ),
    ],
)
def test_scenario_owner_order(scenario, target, expected):
    owners = RecordingOwners()
    result = asyncio.run(StockroomCaptureRunner(owners).run(prepared_driver(scenario)))
    names = [name for name, _ in owners.calls]
    assert result.status is StockroomCaptureStatus.COMPLETED
    assert result.workflow_state is target
    assert names == expected
    assert result.human_result_ref is None
    if scenario.endswith("missing-evidence"):
        assert result.retry_requires_new_attempt is True
        assert names.count("execute") == 1
    if scenario.endswith("human-owned-claim"):
        assert result.human_gate_ref == "owner:human_gate"
        assert result.judgment_ref is None


@pytest.mark.parametrize(
    ("fail_at", "status"),
    [
        ("transition:RUNNING", "DENIED"),
        ("security", "DENIED"),
        ("grant", "DENIED"),
        ("materialize", "FAILED"),
        ("execute", "UNKNOWN"),
        ("execute", "QUARANTINE_REQUIRED"),
        ("evaluate", "REJECTED"),
        ("human_gate", "DENIED"),
        ("judgment:ACCEPTED", "DENIED"),
    ],
)
def test_failure_stops_without_retry(fail_at, status):
    scenario = (
        "stockroom-s4-human-owned-claim"
        if fail_at == "human_gate"
        else "stockroom-s1-normal"
    )
    owners = RecordingOwners(fail_at=fail_at, fail_status=status)
    result = asyncio.run(StockroomCaptureRunner(owners).run(prepared_driver(scenario)))
    names = [name for name, _ in owners.calls]
    assert result.status is StockroomCaptureStatus.STOPPED
    assert names.count(fail_at) == 1
    assert names[-1] == fail_at
    assert result.retry_requires_new_attempt is True


def test_runner_carries_owner_refs_without_substitution():
    owners = RecordingOwners()
    result = asyncio.run(
        StockroomCaptureRunner(owners).run(prepared_driver("stockroom-s1-normal"))
    )
    assert result.judgment_ref == "owner:judgment:ACCEPTED"
    assert result.evidence_refs == ("owner:evaluate",)
    assert all(item.owner_ref.startswith("owner:") for item in result.progress)
    assert "owner:judgment:ACCEPTED" != "owner:transition:ACCEPTED"


@pytest.mark.parametrize(
    ("scenario", "fail_at", "status", "expected_state", "expected_version"),
    [
        ("stockroom-s1-normal", "initial_ready", "PENDING", WorkflowState.READY, 1),
        ("stockroom-s1-normal", "create_attempt", "PENDING", WorkflowState.READY, 1),
        ("stockroom-s1-normal", "transition:RUNNING", "PENDING", WorkflowState.READY, 1),
        ("stockroom-s1-normal", "security", "REJECTED", WorkflowState.RUNNING, 2),
        ("stockroom-s1-normal", "grant", "REJECTED", WorkflowState.RUNNING, 2),
        ("stockroom-s1-normal", "materialize", "SATISFIED", WorkflowState.RUNNING, 2),
        ("stockroom-s1-normal", "materialize", "PENDING", WorkflowState.RUNNING, 2),
        ("stockroom-s1-normal", "execute", "ADMITTED", WorkflowState.RUNNING, 2),
        (
            "stockroom-s1-normal",
            "submit_runtime",
            "REJECTED",
            WorkflowState.ADMISSION_PENDING,
            3,
        ),
        (
            "stockroom-s3-policy-conflict",
            "submit_static",
            "REJECTED",
            WorkflowState.RUNNING,
            2,
        ),
        (
            "stockroom-s4-human-owned-claim",
            "agent_claim",
            "ADMITTED",
            WorkflowState.ADMISSION_PENDING,
            3,
        ),
        (
            "stockroom-s4-human-owned-claim",
            "human_gate",
            "ADMITTED",
            WorkflowState.ADMISSION_PENDING,
            3,
        ),
        (
            "stockroom-s1-normal",
            "judgment:ACCEPTED",
            "PENDING",
            WorkflowState.ADMISSION_PENDING,
            3,
        ),
        (
            "stockroom-s1-normal",
            "judgment:ACCEPTED",
            "REJECTED",
            WorkflowState.ADMISSION_PENDING,
            3,
        ),
        (
            "stockroom-s3-policy-conflict",
            "blocker:POLICY:POLICY_CONFLICT",
            "SATISFIED",
            WorkflowState.RUNNING,
            2,
        ),
        (
            "stockroom-s3-policy-conflict",
            "blocker:POLICY:POLICY_CONFLICT",
            "REJECTED",
            WorkflowState.RUNNING,
            2,
        ),
    ],
)
def test_operation_specific_statuses_fail_closed(
    scenario, fail_at, status, expected_state, expected_version
):
    owners = RecordingOwners(fail_at=fail_at, fail_status=status)
    result = asyncio.run(StockroomCaptureRunner(owners).run(prepared_driver(scenario)))
    names = [name for name, _ in owners.calls]
    assert result.status is StockroomCaptureStatus.STOPPED
    assert names.count(fail_at) == 1
    assert names[-1] == fail_at
    assert result.workflow_state is expected_state
    assert result.state_version == expected_version
    assert result.progress[-1].status == status
    assert result.retry_requires_new_attempt is True


@pytest.mark.parametrize(
    (
        "scenario",
        "tamper_at",
        "status",
        "forged_state",
        "forged_version",
        "authoritative_state",
        "authoritative_version",
    ),
    [
        (
            "stockroom-s1-normal",
            "create_attempt",
            "ADMITTED",
            WorkflowState.ACCEPTED,
            999,
            WorkflowState.READY,
            1,
        ),
        (
            "stockroom-s1-normal",
            "create_attempt",
            "ADMITTED",
            WorkflowState.ACCEPTED,
            1,
            WorkflowState.READY,
            1,
        ),
        (
            "stockroom-s1-normal",
            "create_attempt",
            "ADMITTED",
            WorkflowState.READY,
            999,
            WorkflowState.READY,
            1,
        ),
        (
            "stockroom-s1-normal",
            "security",
            "ADMITTED",
            WorkflowState.ACCEPTED,
            999,
            WorkflowState.RUNNING,
            2,
        ),
        (
            "stockroom-s1-normal",
            "grant",
            "ADMITTED",
            WorkflowState.ACCEPTED,
            999,
            WorkflowState.RUNNING,
            2,
        ),
        (
            "stockroom-s1-normal",
            "materialize",
            "ADMITTED",
            WorkflowState.BLOCKED,
            999,
            WorkflowState.RUNNING,
            2,
        ),
        (
            "stockroom-s1-normal",
            "execute",
            "COMPLETED",
            WorkflowState.FAILED,
            999,
            WorkflowState.RUNNING,
            2,
        ),
        (
            "stockroom-s1-normal",
            "submit_runtime",
            "ADMITTED",
            WorkflowState.REJECTED,
            999,
            WorkflowState.ADMISSION_PENDING,
            3,
        ),
        (
            "stockroom-s3-policy-conflict",
            "submit_static",
            "ADMITTED",
            WorkflowState.REJECTED,
            999,
            WorkflowState.RUNNING,
            2,
        ),
        (
            "stockroom-s1-normal",
            "evaluate",
            "SATISFIED",
            WorkflowState.REJECTED,
            999,
            WorkflowState.ADMISSION_PENDING,
            3,
        ),
        (
            "stockroom-s2-missing-evidence",
            "evaluate",
            "UNSATISFIED",
            WorkflowState.REJECTED,
            999,
            WorkflowState.ADMISSION_PENDING,
            3,
        ),
        (
            "stockroom-s4-human-owned-claim",
            "agent_claim",
            "REJECTED",
            WorkflowState.REJECTED,
            999,
            WorkflowState.ADMISSION_PENDING,
            3,
        ),
        (
            "stockroom-s4-human-owned-claim",
            "human_gate",
            "PENDING",
            WorkflowState.REJECTED,
            999,
            WorkflowState.ADMISSION_PENDING,
            3,
        ),
        (
            "stockroom-s1-normal",
            "judgment:ACCEPTED",
            "ADMITTED",
            WorkflowState.FAILED,
            999,
            WorkflowState.ADMISSION_PENDING,
            3,
        ),
        (
            "stockroom-s3-policy-conflict",
            "blocker:POLICY:POLICY_CONFLICT",
            "ADMITTED",
            WorkflowState.FAILED,
            999,
            WorkflowState.RUNNING,
            2,
        ),
    ],
)
def test_non_workflow_snapshot_mismatch_stops_fail_closed(
    scenario,
    tamper_at,
    status,
    forged_state,
    forged_version,
    authoritative_state,
    authoritative_version,
):
    owners = RecordingOwners(
        overrides={tamper_at: (status, forged_state, forged_version)}
    )
    result = asyncio.run(StockroomCaptureRunner(owners).run(prepared_driver(scenario)))
    names = [name for name, _ in owners.calls]
    assert result.status is StockroomCaptureStatus.STOPPED
    assert names[-1] == tamper_at
    assert names.count(tamper_at) == 1
    assert result.workflow_state is authoritative_state
    assert result.state_version == authoritative_version
    assert result.stop_reason == "OWNER_RESULT_STATE_VERSION_MISMATCH"
    assert result.retry_requires_new_attempt is True
    assert result.progress[-1].workflow_state is forged_state
    assert result.progress[-1].state_version == forged_version


@pytest.mark.parametrize(
    ("state", "version"),
    [
        (WorkflowState.RUNNING, 1),
        (WorkflowState.READY, 2),
    ],
)
def test_initial_ready_requires_exact_state_and_version(state, version):
    owners = RecordingOwners(overrides={"initial_ready": ("ADMITTED", state, version)})
    result = asyncio.run(
        StockroomCaptureRunner(owners).run(prepared_driver("stockroom-s1-normal"))
    )
    assert result.status is StockroomCaptureStatus.STOPPED
    assert [name for name, _ in owners.calls] == ["initial_ready"]
    assert result.workflow_state is WorkflowState.READY
    assert result.state_version == 1
    assert result.progress[-1].workflow_state is state
    assert result.progress[-1].state_version == version


@pytest.mark.parametrize(
    ("state", "version"),
    [
        (WorkflowState.ACCEPTED, 2),
        (WorkflowState.RUNNING, 1),
        (WorkflowState.RUNNING, 3),
        (WorkflowState.RUNNING, 999),
    ],
)
def test_transition_requires_exact_target_and_next_version(state, version):
    name = "transition:RUNNING"
    owners = RecordingOwners(overrides={name: ("ADMITTED", state, version)})
    result = asyncio.run(
        StockroomCaptureRunner(owners).run(prepared_driver("stockroom-s1-normal"))
    )
    assert result.status is StockroomCaptureStatus.STOPPED
    assert [call for call, _ in owners.calls][-1] == name
    assert [call for call, _ in owners.calls].count(name) == 1
    assert result.workflow_state is WorkflowState.READY
    assert result.state_version == 1
    assert result.progress[-1].workflow_state is state
    assert result.progress[-1].state_version == version


@pytest.fixture(autouse=True)
def no_real_boundaries(monkeypatch):
    def forbidden(*args, **kwargs):
        raise AssertionError("REAL_BOUNDARY_REACHED")

    monkeypatch.setattr("subprocess.run", forbidden)
    monkeypatch.setattr("socket.create_connection", forbidden)
    monkeypatch.setattr(
        "aiscc.runtime.docker.DockerRuntime.run_consumed_stockroom", forbidden
    )
    monkeypatch.setattr(
        "aiscc.runtime.stockroom_materializer.StockroomMaterializer.materialize",
        forbidden,
    )
    monkeypatch.setattr(
        "aiscc.providers.local_deterministic.LocalDeterministicProvider.call", forbidden
    )
    monkeypatch.setattr(
        "aiscc.providers.stockroom_tool.StockroomSummaryDispatcher.dispatch_with_receipts",
        forbidden,
    )
    monkeypatch.setattr(
        "aiscc.persistence.repository.PostgresExecutionRepository.__init__", forbidden
    )
    monkeypatch.setattr("aiscc.workflow.models.TransitionDecision", forbidden)
    monkeypatch.setattr("aiscc.evidence.models.AdmittedEvidence", forbidden)
    monkeypatch.setattr("aiscc.human.models.HumanResult", forbidden)
    monkeypatch.setattr("aiscc.judgment.models.Judgment", forbidden)
