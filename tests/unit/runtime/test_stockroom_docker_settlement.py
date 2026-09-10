from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from unittest.mock import Mock

import pytest

from aiscc.contracts.security import ResourceDomain
from aiscc.contracts.workflow import WorkflowState
from aiscc.runtime.docker import StockroomProcessObservation
from tests.unit.providers.test_stockroom_tool import CANDIDATE, _composition, _success


@pytest.fixture(autouse=True)
def forbid_process_execution(monkeypatch: pytest.MonkeyPatch):
    process = Mock(side_effect=AssertionError("Unit regression must not spawn a process"))
    monkeypatch.setattr("subprocess.Popen", process)
    yield
    process.assert_not_called()


def _consumed(tmp_path: Path, runner):
    broker, prepared, _, runtime, spec = _composition(tmp_path, runner)
    consumed = broker.consume_prepared(
        prepared, policy=runtime._policy, secret_lease_authority=None
    )
    index = next(
        index
        for index, requirement in enumerate(prepared.capabilities)
        if requirement.scope.domain is ResourceDomain.PROCESS
    )
    return runtime, spec, consumed.receipts[index], prepared.capabilities[index], consumed


@pytest.mark.parametrize("termination_proven", [False, True])
@pytest.mark.parametrize("owner_reconciled", [False, True])
@pytest.mark.parametrize("exit_code", [0, 2])
@pytest.mark.parametrize(
    "timed_out,cancelled", [(False, False), (True, False), (False, True), (True, True)]
)
@pytest.mark.parametrize(
    "stdout,stderr,invalid_capture",
    [
        (_success().stdout, b"", False),
        (b"x" * 4097, b"", True),
        (b"", b"x" * 4097, True),
        (b"\xff", b"", True),
        (b"", b"\xff", True),
    ],
    ids=["valid", "stdout-oversize", "stderr-oversize", "stdout-non-ascii", "stderr-non-ascii"],
)
def test_settlement_matrix(
    tmp_path: Path,
    termination_proven: bool,
    owner_reconciled: bool,
    exit_code: int,
    timed_out: bool,
    cancelled: bool,
    stdout: bytes,
    stderr: bytes,
    invalid_capture: bool,
) -> None:
    observation = StockroomProcessObservation(
        exit_code, stdout, stderr, timed_out, cancelled, termination_proven, owner_reconciled
    )
    runner = Mock(return_value=observation)
    runtime, spec, receipt, requirement, consumed = _consumed(tmp_path, runner)
    result = runtime.run_consumed_stockroom(
        receipt, requirement, spec=spec, dispatch_identity=consumed.dispatch_identity
    )
    if not (termination_proven and owner_reconciled):
        assert result.tool_outcome == "UNKNOWN_TOOL_OUTCOME"
        assert result.quarantine_required
    elif timed_out or cancelled or invalid_capture or exit_code != 0:
        assert result.tool_outcome == "KNOWN_TOOL_FAILURE"
        assert not result.quarantine_required
    else:
        assert result.tool_outcome == "KNOWN_TOOL_COMPLETED"
        assert not result.quarantine_required
        assert result.stdout == stdout.decode("ascii")
    assert result.executed
    assert result.security_reason == "AUTHENTIC_CONSUMED_PROCESS_RECEIPT"
    assert result.security_provenance == {"receipt_id": receipt.receipt_id}
    assert len(result.stdout) <= 4096 and len(result.stderr) <= 4096
    runner.assert_called_once_with(runtime._secure_run_args(spec), spec)
    # An unknown observation cannot authorize another crossing with the same receipt.
    repeated = runtime.run_consumed_stockroom(
        receipt, requirement, spec=spec, dispatch_identity=consumed.dispatch_identity
    )
    assert not repeated.executed
    assert repeated.security_reason == "STOCKROOM_PROCESS_RECEIPT_DENIED"
    assert runner.call_count == 1


@pytest.mark.parametrize("missing_runner", [False, True])
def test_missing_or_raising_runner_remains_unknown(tmp_path: Path, missing_runner: bool) -> None:
    runner = None if missing_runner else Mock(side_effect=RuntimeError("synthetic transport"))
    runtime, spec, receipt, requirement, consumed = _consumed(tmp_path, runner)
    result = runtime.run_consumed_stockroom(
        receipt, requirement, spec=spec, dispatch_identity=consumed.dispatch_identity
    )
    assert result.tool_outcome == "UNKNOWN_TOOL_OUTCOME"
    assert result.quarantine_required
    assert result.stdout == ""
    assert result.executed is not missing_runner


@pytest.mark.parametrize(
    "tamper",
    [
        "forged", "copy", "missing-capability", "tool-receipt", "scope", "fingerprint",
        "run", "state", "version", "dispatch",
    ],
)
def test_receipt_binding_denies_before_runner(tmp_path: Path, tamper: str) -> None:
    runner = Mock(side_effect=_success)
    runtime, spec, receipt, requirement, consumed = _consumed(tmp_path, runner)
    identity = consumed.dispatch_identity
    if tamper == "forged":
        receipt = replace(receipt, _issuer_token=object())
    elif tamper == "copy":
        receipt = replace(receipt)
    elif tamper == "missing-capability":
        requirement = replace(requirement, capability=None)
    elif tamper == "tool-receipt":
        receipt = consumed.receipts[0]
        requirement = consumed.prepared.capabilities[0]
    elif tamper == "scope":
        spec = replace(spec, name="other-container")
    elif tamper == "fingerprint":
        requirement = replace(requirement, operation_fingerprint="f" * 64)
    elif tamper == "run":
        requirement = replace(requirement, current=replace(requirement.current, run_id="other"))
    elif tamper == "state":
        requirement = replace(
            requirement, current=replace(requirement.current, state=WorkflowState.READY)
        )
    elif tamper == "version":
        requirement = replace(requirement, current=replace(requirement.current, state_version=5))
    else:
        identity = "f" * 64
    result = runtime.run_consumed_stockroom(
        receipt, requirement, spec=spec, dispatch_identity=identity
    )
    assert not result.executed
    assert result.security_reason == "STOCKROOM_PROCESS_RECEIPT_DENIED"
    runner.assert_not_called()


def test_unclaimed_authentic_receipt_is_denied(tmp_path: Path) -> None:
    runner = Mock(side_effect=_success)
    _, prepared, _, runtime, spec = _composition(tmp_path, runner)
    uses, receipts = runtime._policy.consume_capabilities_atomically_with_receipts(
        prepared.capabilities
    )
    assert all(use.allowed for use in uses)
    result = runtime.run_consumed_stockroom(
        receipts[1], prepared.capabilities[1], spec=spec, dispatch_identity="a" * 64
    )
    assert not result.executed
    runner.assert_not_called()


@pytest.mark.parametrize("field", ["execution_attempt_id", "resolved_spec_fingerprint"])
def test_attempt_and_spec_fingerprint_cannot_rebind_capabilities(
    tmp_path: Path, field: str
) -> None:
    runner = Mock(side_effect=_success)
    broker, prepared, _, _, _ = _composition(tmp_path, runner)
    assert prepared.dispatch_context is not None
    context = replace(prepared.dispatch_context, **{field: "b" * 64})
    with pytest.raises(ValueError, match="TOOL_ARGUMENT_FINGERPRINT_DENIED"):
        broker.prepare_dispatch(
            CANDIDATE,
            mode=prepared.capabilities[0].current_mode,
            profile_id="stockroom-owner-s1-v1",
            scenario_id="stockroom-s1-normal",
            capabilities=prepared.capabilities,
            dispatch_context=context,
        )
    runner.assert_not_called()
