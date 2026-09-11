from __future__ import annotations

import copy
import io
import json
from dataclasses import replace
from pathlib import Path
from threading import Event
from unittest.mock import Mock

import pytest

from aiscc.contracts.security import ResourceDomain
from aiscc.contracts.workflow import WorkflowState
from aiscc.providers.stockroom_tool import build_stockroom_spec, load_stockroom_tool_config
from aiscc.runtime.docker import (
    DockerRuntime,
    StockroomCancellation,
    StockroomDockerRunner,
    StockroomProcessObservation,
)
from tests.unit.providers.test_stockroom_tool import CANDIDATE, _composition, _success
from tests.unit.runtime.test_stockroom_image import ROOT, synthetic_image


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


def _source_runner(tmp_path, monkeypatch, fault=None):
    admitted, _, _, _, observation = synthetic_image(tmp_path, monkeypatch)
    executable = tmp_path / "test-only-docker.exe"
    executable.write_bytes(b"not executable; fake transport only")
    signal = StockroomCancellation("run", "attempt", Event())
    runner = StockroomDockerRunner(executable, admitted, signal)
    config = load_stockroom_tool_config(ROOT / "config/providers/stockroom-tools.v2.toml")
    spec = build_stockroom_spec(config, name="aiscc-attempt", run_id="run", workspace=tmp_path,
                                image_provenance=admitted)
    identity = "c" * 64
    state = {"Status": "created", "Running": False, "ExitCode": 0}
    calls = []
    image_observation = copy.deepcopy(observation)
    if fault == "labels":
        image_observation["Config"]["Labels"]["io.aiscc.stockroom.python-version"] = "3.11"
    if fault == "image-id":
        image_observation["Id"] = "sha256:" + "b" * 64

    class FakeProcess:
        def __init__(self, argv, **kwargs):
            assert argv[0] == str(executable)
            assert kwargs["shell"] is False
            assert kwargs["stdin"] == -3
            assert set(kwargs["env"]) <= {"SystemRoot", "WINDIR"}
            args = argv[1:]
            calls.append(args)
            self.returncode = 0
            output = b""
            error = b""
            if args[:2] == ["image", "inspect"]:
                assert args[2] == admitted.provenance.image.image_id
                output = json.dumps([image_observation]).encode()
            elif args[0] == "create":
                assert args[1] == "--pull=never"
                output = (identity + "\n").encode()
                if fault == "create":
                    output = b"uncertain"
            elif args[:2] == ["container", "inspect"]:
                assert args[2] == identity
                labels = {"aiscc.run_id": spec.run_id, "aiscc.owner": "p1-3"}
                if fault == "owner":
                    labels["aiscc.run_id"] = "foreign"
                output = json.dumps([{"Id": identity, "Name": "/" + spec.name,
                                      "Config": {"Labels": labels}, "State": state}]).encode()
                if fault == "inspect":
                    self.returncode = 1
            elif args[0] == "start":
                assert args == ["start", "--attach", identity]
                state.update(Status="exited", Running=False)
                output = b"x" * (100000 if fault == "overflow" else 1)
                error = b"y" * (100000 if fault == "overflow" else 0)
                if fault == "start":
                    raise OSError("synthetic uncertain start")
                if fault == "cancel":
                    state.update(Status="running", Running=True)
                    signal.event.set()
                    self.returncode = None
            elif args[0] in {"stop", "kill"}:
                assert args[-1] == identity
                if args[0] == "kill":
                    state.update(Status="exited", Running=False, ExitCode=137)
            elif args[0] == "rm":
                assert args == ["rm", identity]
                if fault == "remove":
                    self.returncode = 1
            elif args[:2] == ["container", "ls"]:
                if fault == "absence":
                    output = identity.encode()
            else:
                raise AssertionError(args)
            self.stdout = io.BytesIO(output)
            self.stderr = io.BytesIO(error)

        def poll(self):
            return self.returncode

        def kill(self):
            self.returncode = -9

        def wait(self, timeout):
            return self.returncode

    monkeypatch.setattr("subprocess.Popen", FakeProcess)
    return runner, spec, calls


@pytest.mark.parametrize("fault", [None, "overflow", "cancel", "labels", "image-id", "create",
                                   "owner", "inspect", "start", "remove", "absence"])
def test_source_runner_settlement_and_uncertainty(tmp_path, monkeypatch, fault):
    runner, spec, calls = _source_runner(tmp_path, monkeypatch, fault)
    args = DockerRuntime._secure_run_args(runner, spec)
    result = runner(args, spec)
    assert calls[0] == ["image", "inspect", spec.image]
    if fault in {None, "overflow", "cancel"}:
        assert result.termination_proven and result.owner_reconciled
        assert result.exit_code == (137 if fault == "cancel" else 0)
    else:
        assert not (result.termination_proven and result.owner_reconciled)
    if fault in {"labels", "image-id"}:
        assert len(calls) == 1
    if fault in {"owner", "inspect", "create"}:
        assert not any(c[0] in {"rm", "start"} for c in calls)
    if fault == "overflow":
        assert len(result.stdout) == len(result.stderr) == 4097
    if fault == "cancel":
        assert result.cancelled
        assert [c[0] for c in calls if c[0] in {"stop", "kill"}] == ["stop", "kill"]
    before = len(calls)
    with pytest.raises(ValueError, match="REDISPATCH"):
        runner(args, spec)
    assert len(calls) == before


def test_source_runner_operation_timeout_is_settled(tmp_path, monkeypatch):
    runner, spec, calls = _source_runner(tmp_path, monkeypatch)
    process = runner._process

    def timeout_start(args, timeout, *limits):
        if args[0] == "start":
            process(args, timeout, *limits)
            return 1, b"", b"", True, False
        return process(args, timeout, *limits)

    monkeypatch.setattr(runner, "_process", timeout_start)
    result = runner(DockerRuntime._secure_run_args(runner, spec), spec)
    assert result.timed_out and result.termination_proven and result.owner_reconciled
    assert any(c[0] == "rm" for c in calls)


def test_runner_rejects_unbound_attempt_and_raw_authority(tmp_path, monkeypatch):
    runner, spec, calls = _source_runner(tmp_path, monkeypatch)
    with pytest.raises(ValueError, match="ATTEMPT_BINDING"):
        runner([], replace(spec, run_id="foreign"))
    with pytest.raises(ValueError, match="ADMITTED_IMAGE"):
        StockroomDockerRunner(Path(runner._executable), spec.image_provenance.provenance,
                              runner._cancel)
    assert not calls
