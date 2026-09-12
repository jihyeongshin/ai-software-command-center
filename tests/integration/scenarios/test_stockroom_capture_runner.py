from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Coroutine
from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime
from pathlib import Path
from threading import Event
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest
from sqlalchemy import select

from aiscc.bootstrap import build_stockroom_production
from aiscc.contracts.security import ResourceDomain, SecurityAdmissionDecision
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.evidence.models import EvidenceSetEvaluationRef
from aiscc.judgment.models import JudgmentEvidenceBasisKind
from aiscc.persistence import create_engine, create_session_factory
from aiscc.persistence.models import (
    EvidenceCheckpointRow,
    EvidenceRequirementRow,
    EvidenceRequirementSetRow,
    ExecutionAttemptRow,
    ExecutionOutputRefRow,
    JudgmentPolicyRow,
    JudgmentRow,
)
from aiscc.providers.authority import ExecutionReferenceAuthority
from aiscc.providers.local_deterministic import (
    LOCAL_COMPATIBILITY_SECRET_REF,
    LOCAL_COMPATIBILITY_SENTINEL,
    STOCKROOM_SUMMARY,
    LocalDeterministicProvider,
)
from aiscc.providers.models import canonical_sha256
from aiscc.providers.service import AgentExecutionService
from aiscc.providers.stockroom_tool import StockroomSummaryDispatcher
from aiscc.runtime.docker import StockroomCancellation, StockroomDockerRunner
from aiscc.runtime.stockroom_materializer import StockroomMaterializer
from aiscc.scenarios.capture_runner import StockroomCaptureRunner
from aiscc.scenarios.driver import StockroomMaterializedResultBinding
from aiscc.scenarios.models import RESOURCE_REF, SCENARIO_IDS
from aiscc.scenarios.runtime_models import (
    MaterializationAuthority,
    MaterializedFile,
    MaterializedStockroom,
    StockroomRunBinding,
    StockroomWorkspaceLease,
)
from aiscc.scenarios.stockroom_production import (
    StockroomAgentExecutionServiceFactory,
    StockroomMaterializerFactory,
    StockroomSecurityAuthorization,
    _derive_runtime_summary_observation,
    load_stockroom_evidence_config,
    load_stockroom_human_config,
    load_stockroom_judgment_config,
)
from aiscc.workflow.guards import GUARD_OWNER_POLICY
from aiscc.workflow.matrix import TRANSITION_MATRIX
from aiscc.workflow.models import (
    AuthorityConflictError,
    DecisionOutcome,
    GuardSemanticOwner,
    RequesterType,
    TransitionRequest,
)
from tests.unit.runtime.test_stockroom_image import synthetic_image
from tests.unit.scenarios.test_stockroom_capture_runner import RecordingOwners, prepared_driver


def run[T](coroutine: Coroutine[Any, Any, T]) -> T:
    return asyncio.run(coroutine)


@pytest.fixture(scope="module")
def database_url() -> str:
    value = os.environ.get("AISCC_TEST_DATABASE_URL")
    if not value:
        pytest.skip("AISCC_TEST_DATABASE_URL is required for PostgreSQL evidence")
    return value


def _transition_request(
    *,
    scenario_id: str,
    source: WorkflowState,
    target: WorkflowState,
) -> TransitionRequest:
    return TransitionRequest(
        transition_request_id=f"stockroom-config-lookup-{scenario_id}-{target.value}",
        project_id="aiscc-stockroom-integration",
        task_contract_id=scenario_id,
        task_contract_version="1.0.0",
        work_run_id=f"stockroom-config-lookup-{scenario_id}",
        observed_state=source,
        observed_state_version=3,
        target_state=target,
        requester_identity="aiscc-stockroom-integration",
        requester_type=RequesterType.OPERATOR,
        runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        created_at=datetime(2026, 9, 10, 9, 24, tzinfo=UTC),
    )


def _output_ref(
    *, ref_id: str, attempt_id: str, kind: str, content_hash: str
) -> ExecutionOutputRefRow:
    return ExecutionOutputRefRow(
        output_ref_id=ref_id,
        execution_attempt_id=attempt_id,
        ref_kind=kind,
        content_hash=content_hash,
        storage_ref=f"private://test/{ref_id}",
        created_at=datetime(2026, 9, 10, 9, 24, tzinfo=UTC),
    )


def test_runtime_summary_derivation_requires_verified_same_attempt_tool_provenance() -> None:
    attempt_id = "stockroom-runtime-evidence-attempt"
    agent = _output_ref(
        ref_id="agent-output-current",
        attempt_id=attempt_id,
        kind="AgentOutputRef",
        content_hash="a" * 64,
    )
    tool = _output_ref(
        ref_id="tool-output-current",
        attempt_id=attempt_id,
        kind="ToolOutputRef",
        content_hash=canonical_sha256(STOCKROOM_SUMMARY),
    )

    observation = _derive_runtime_summary_observation(
        expected_attempt_id=attempt_id,
        agent_output=agent,
        tool_output=tool,
        agent_verified=True,
        tool_verified=True,
    )
    assert observation["summary"] == STOCKROOM_SUMMARY
    assert observation["total_available"] == sum(
        item["available"] for item in STOCKROOM_SUMMARY["items"]
    )
    assert observation["tool_output_ref"] == tool.output_ref_id
    assert observation["tool_output_hash"] == tool.content_hash

    denied_sources = (
        {"agent_output": None, "tool_output": None},
        {"agent_output": agent, "tool_output": None},
        {
            "agent_output": agent,
            "tool_output": _output_ref(
                ref_id="tool-output-wrong-hash",
                attempt_id=attempt_id,
                kind="ToolOutputRef",
                content_hash="0" * 64,
            ),
        },
        {
            "agent_output": agent,
            "tool_output": _output_ref(
                ref_id="tool-output-wrong-attempt",
                attempt_id="another-attempt",
                kind="ToolOutputRef",
                content_hash=canonical_sha256(STOCKROOM_SUMMARY),
            ),
        },
        {
            "agent_output": agent,
            "tool_output": _output_ref(
                ref_id="tool-output-wrong-kind",
                attempt_id=attempt_id,
                kind="AgentOutputRef",
                content_hash=canonical_sha256(STOCKROOM_SUMMARY),
            ),
        },
    )
    for source in denied_sources:
        with pytest.raises(AuthorityConflictError):
            _derive_runtime_summary_observation(
                expected_attempt_id=attempt_id,
                agent_output=source["agent_output"],
                tool_output=source["tool_output"],
                agent_verified=True,
                tool_verified=True,
            )

    with pytest.raises(AuthorityConflictError):
        _derive_runtime_summary_observation(
            expected_attempt_id=attempt_id,
            agent_output=agent,
            tool_output=tool,
            agent_verified=True,
            tool_verified=False,
        )


@pytest.mark.postgres
def test_production_owner_graph_and_bounded_running_prefix(
    database_url: str, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository_root = Path(__file__).resolve().parents[3]
    counters = {
        "docker": 0,
        "materialize": 0,
        "provider": 0,
        "dispatcher": 0,
        "execution": 0,
    }
    bounded_returns: dict[tuple[str, str], MaterializedStockroom] = {}
    _, image_ref, _, _, _ = synthetic_image(tmp_path, monkeypatch)
    docker_executable = tmp_path / "test-only-docker.exe"
    docker_executable.write_bytes(b"fake executable; subprocess forbidden")
    private_runtime_root = tmp_path / "private-runtime"
    private_runtime_root.mkdir()
    assert tuple(private_runtime_root.iterdir()) == ()
    run_id = f"stockroom-production-{uuid4()}"
    attempt_id = f"stockroom-attempt-{uuid4()}"

    def fail_sync(name: str):
        def fail(*args: object, **kwargs: object) -> Any:
            del args, kwargs
            counters[name] += 1
            raise AssertionError(f"forbidden runtime edge called: {name}")

        return fail

    def fail_async(name: str):
        async def fail(*args: object, **kwargs: object) -> Any:
            del args, kwargs
            counters[name] += 1
            raise AssertionError(f"forbidden runtime edge called: {name}")

        return fail

    def bounded_materialize(
        owner: StockroomMaterializer,
        binding: StockroomRunBinding,
        authority: MaterializationAuthority,
    ) -> MaterializedStockroom:
        counters["materialize"] += 1
        assert type(owner) is StockroomMaterializer
        assert len(owner._authorities) == 1
        assert owner._authorities[0] is authority
        assert binding is authority.binding
        key = (binding.run_id, binding.attempt_id)
        return bounded_returns[key]

    monkeypatch.setattr(StockroomMaterializer, "materialize", bounded_materialize)
    monkeypatch.setattr(LocalDeterministicProvider, "call", fail_sync("provider"))
    monkeypatch.setattr(
        StockroomSummaryDispatcher, "dispatch_with_receipts", fail_sync("dispatcher")
    )
    monkeypatch.setattr(AgentExecutionService, "execute", fail_async("execution"))

    def docker_runner(*args: object, **kwargs: object) -> Any:
        del args, kwargs
        counters["docker"] += 1
        raise AssertionError("forbidden runtime edge called: docker")

    monkeypatch.setattr(StockroomDockerRunner, "_process", docker_runner)

    async def scenario() -> None:
        engine = create_engine(database_url)
        sessions = create_session_factory(engine)
        try:
            evidence_config = load_stockroom_evidence_config(
                repository_root / "config/evidence/stockroom-capture.v1.json"
            )
            human_config = load_stockroom_human_config(
                repository_root / "config/human/stockroom-capture.v1.json"
            )
            legacy_judgment_config = load_stockroom_judgment_config(
                repository_root / "config/judgment/stockroom-capture.v1.json"
            )
            judgment_config = load_stockroom_judgment_config(
                repository_root / "config/judgment/stockroom-capture.v2.json"
            )
            assert tuple(item["scenario_id"] for item in evidence_config["enrollments"]) == (
                SCENARIO_IDS
            )
            assert human_config["required_use"]["scenario_id"] == SCENARIO_IDS[3]
            assert (
                tuple(item["scenario_id"] for item in judgment_config["policies"])
                == (SCENARIO_IDS[:2])
            )
            assert all(
                item["evidence_basis_kind"] is None for item in legacy_judgment_config["policies"]
            )
            assert tuple(item["evidence_basis_kind"] for item in judgment_config["policies"]) == (
                JudgmentEvidenceBasisKind.SATISFIED_ATTESTATION,
                JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION,
            )
            malformed_judgment = json.loads(
                (repository_root / "config/judgment/stockroom-capture.v2.json").read_text(
                    encoding="utf-8"
                )
            )
            malformed_judgment["policies"][1].pop("evidence_checkpoint_ref")
            malformed_path = tmp_path / "malformed-judgment-v2.json"
            malformed_path.write_text(json.dumps(malformed_judgment), encoding="utf-8")
            with pytest.raises(ValueError, match="judgment policy has unknown or missing keys"):
                load_stockroom_judgment_config(malformed_path)
            malformed_path.unlink()

            application = await build_stockroom_production(
                session_factory=sessions,
                repository_root=repository_root,
                private_runtime_root=private_runtime_root,
                downloads_root=Path.home() / "Downloads",
                trusted_git_executable=tmp_path / "git.exe",
                image_provenance_ref=image_ref,
                trusted_docker_executable=docker_executable,
                cancellation=StockroomCancellation(run_id, attempt_id, Event()),
                project_id="aiscc-stockroom-integration",
                requester_identity="aiscc-stockroom-integration",
                human_selector_fingerprint="a" * 64,
                secret_material_by_ref={
                    LOCAL_COMPATIBILITY_SECRET_REF: LOCAL_COMPATIBILITY_SENTINEL
                },
                clock=lambda: datetime(2026, 9, 10, 9, 24, tzinfo=UTC),
            )

            assert application.execution_repository._session_factory is sessions
            assert application.evidence_repository._session_factory is sessions
            assert application.human_repository._session_factory is sessions
            assert application.judgment_policy_authority._session_factory is sessions
            assert application.transition_repository._session_factory is sessions

            async with sessions() as session:
                for enrollment in application.evidence_enrollments.values():
                    set_ref = (
                        f"{enrollment.requirement_set.requirement_set_id}"
                        f"@{enrollment.requirement_set.requirement_set_version}"
                    )
                    requirement_ref = enrollment.requirement.ref.serialized()
                    checkpoint_ref = enrollment.checkpoint.ref.serialized()
                    requirement_set = await session.get(EvidenceRequirementSetRow, set_ref)
                    requirement = await session.get(EvidenceRequirementRow, requirement_ref)
                    checkpoint = await session.get(EvidenceCheckpointRow, checkpoint_ref)
                    assert requirement_set is not None
                    assert requirement is not None
                    assert checkpoint is not None
                    assert requirement_set.task_contract_id == enrollment.scenario_id
                    assert checkpoint.task_contract_id == enrollment.scenario_id

                    request = _transition_request(
                        scenario_id=enrollment.scenario_id,
                        source=enrollment.checkpoint.source_state,
                        target=enrollment.checkpoint.target_state,
                    )
                    resolved = application.evidence_checkpoint_uses.resolve_transition(request)
                    assert resolved == enrollment.checkpoint.ref

                for enrollment in application.judgment_enrollments.values():
                    policy = await session.get(JudgmentPolicyRow, enrollment.policy.serialized_ref)
                    assert policy is not None
                    assert policy.fingerprint == enrollment.policy.fingerprint

            human_request = _transition_request(
                scenario_id=SCENARIO_IDS[3],
                source=WorkflowState.ADMISSION_PENDING,
                target=WorkflowState.HUMAN_REQUIRED,
            )
            assert application.human_reservation_authority.requires_human(human_request)
            assert set(application.judgment_enrollments) == set(SCENARIO_IDS[:2])
            assert (
                application.judgment_enrollments[SCENARIO_IDS[0]].policy.evidence_basis_kind
                is JudgmentEvidenceBasisKind.SATISFIED_ATTESTATION
            )
            assert (
                application.judgment_enrollments[SCENARIO_IDS[1]].policy.evidence_basis_kind
                is JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION
            )

            s2_run_id = f"stockroom-production-s2-{uuid4()}"
            s2_capture = application.prepare_capture(
                scenario_id=SCENARIO_IDS[1],
                run_id=s2_run_id,
                attempt_id=f"stockroom-s2-attempt-{uuid4()}",
            )
            for source, version, target in (
                (None, 0, WorkflowState.READY),
                (WorkflowState.READY, 1, WorkflowState.RUNNING),
                (WorkflowState.RUNNING, 2, WorkflowState.ADMISSION_PENDING),
            ):
                request = s2_capture.adapter._request(s2_capture.prepared, source, version, target)
                facts = tuple(
                    application.p1_4_guard_authority.issue(
                        guard_id=guard,
                        satisfied=True,
                        reason="BOUNDED_SCENARIO_TEST_AUTHORITY",
                        authority_ref=f"bounded-test:{guard.value}",
                        request=request,
                    )
                    for guard in TRANSITION_MATRIX[(source, target)]
                    if GUARD_OWNER_POLICY[guard] is GuardSemanticOwner.P1_4_SYSTEM
                )
                decision = await application.workflow_kernel.request_transition(request, facts)
                assert decision.outcome is DecisionOutcome.ADMITTED
            s2_evaluation = await s2_capture.adapter.evaluate_evidence(s2_capture.prepared, None)
            assert s2_evaluation.status == "UNSATISFIED"
            assert (
                EvidenceSetEvaluationRef.parse(s2_evaluation.owner_ref).serialized()
                == s2_evaluation.owner_ref
            )
            authentic_evaluation = s2_capture.adapter._handles.pop(s2_evaluation.owner_ref)
            s2_capture.adapter._handles[s2_evaluation.owner_ref] = s2_evaluation.owner_ref
            denied_text_basis = await s2_capture.adapter.issue_judgment(
                s2_capture.prepared,
                judgment_status="HOLD_REWORK_REQUIRED",
                evidence_ref=None,
            )
            assert denied_text_basis.status == "DENIED"
            s2_capture.adapter._handles[s2_evaluation.owner_ref] = authentic_evaluation
            s2_judgment_call = await s2_capture.adapter.issue_judgment(
                s2_capture.prepared,
                judgment_status="HOLD_REWORK_REQUIRED",
                evidence_ref=None,
            )
            assert s2_judgment_call.status == "ADMITTED"
            async with sessions() as session:
                s2_judgment_row = await session.scalar(
                    select(JudgmentRow).where(JudgmentRow.work_run_id == s2_run_id)
                )
                assert s2_judgment_row is not None
                assert s2_judgment_row.payload["evidence_basis_kind"] == (
                    JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION.value
                )
                assert s2_judgment_row.payload["evidence_evaluation_ref"] == s2_evaluation.owner_ref
                assert s2_judgment_row.payload["evidence_attestation_ref"] is None
                assert s2_judgment_row.payload["reason_code"] == (
                    "STOCKROOM_REQUIRED_EVIDENCE_UNSATISFIED"
                )
                assert s2_evaluation.owner_ref not in str(s2_judgment_row.payload["reason_code"])
            s2_transition = await s2_capture.adapter.request_transition(
                s2_capture.prepared,
                target=WorkflowState.REWORK_REQUIRED,
                observed_state=WorkflowState.ADMISSION_PENDING,
                observed_version=3,
                authority_refs=(s2_judgment_call.owner_ref,),
            )
            assert (s2_transition.status, s2_transition.workflow_state) == (
                "ADMITTED",
                WorkflowState.REWORK_REQUIRED,
            )
            no_judgment_runs = (
                f"stockroom-production-s3-{uuid4()}",
                f"stockroom-production-s4-{uuid4()}",
            )
            for scenario_id, untouched_run_id in zip(
                SCENARIO_IDS[2:], no_judgment_runs, strict=True
            ):
                application.prepare_capture(
                    scenario_id=scenario_id,
                    run_id=untouched_run_id,
                    attempt_id=f"untouched-attempt-{uuid4()}",
                )
            async with sessions() as session:
                assert not tuple(
                    await session.scalars(
                        select(JudgmentRow).where(JudgmentRow.work_run_id.in_(no_judgment_runs))
                    )
                )

            capture = application.prepare_capture(
                scenario_id=SCENARIO_IDS[0], run_id=run_id, attempt_id=attempt_id
            )
            assert isinstance(capture.runner, StockroomCaptureRunner)
            owners = capture.prepared.owners
            assert owners.workflow_kernel is application.workflow_kernel
            assert owners.evidence_admission_service is application.evidence_service
            assert owners.human_gate_owner is application.human_repository
            assert owners.judgment_owner is application.judgment_authority
            assert owners.workspace_owner is application.workspace
            assert owners.security_policy is application.security_policy
            assert owners.stockroom_owner_restriction is application.stockroom_owner_restriction
            assert type(owners.materializer_factory) is StockroomMaterializerFactory
            assert (
                type(owners.agent_execution_service_factory)
                is StockroomAgentExecutionServiceFactory
            )
            materializer_factory = owners.materializer_factory
            execution_factory = owners.agent_execution_service_factory
            assert capture.materializer is None
            assert capture.agent_execution_service is None
            assert capture.prepared.attempt_binding.run_id == run_id
            assert capture.prepared.attempt_binding.attempt_id == attempt_id
            assert capture.prepared.attempt_binding.scenario_id == SCENARIO_IDS[0]
            assert (
                capture.prepared.attempt_binding.request_fingerprint
                == capture.prepared.request.request_fingerprint
            )
            assert (
                capture.prepared.attempt_binding.run_binding_fingerprint
                == capture.prepared.request.run_binding.binding_fingerprint
            )
            assert (
                capture.prepared.attempt_binding.configuration_fingerprint
                == application.composition.fingerprints.composition_sha256
            )

            ready = await capture.adapter.initial_ready(capture.prepared)
            assert (ready.status, ready.workflow_state, ready.state_version) == (
                "ADMITTED",
                WorkflowState.READY,
                1,
            )
            attempt = await capture.adapter.create_attempt(capture.prepared, ready.owner_ref)
            assert (attempt.status, attempt.workflow_state, attempt.state_version) == (
                "ADMITTED",
                WorkflowState.READY,
                1,
            )
            running = await capture.adapter.request_transition(
                capture.prepared,
                target=WorkflowState.RUNNING,
                observed_state=WorkflowState.READY,
                observed_version=1,
                authority_refs=(attempt.owner_ref,),
            )
            assert (running.status, running.workflow_state, running.state_version) == (
                "ADMITTED",
                WorkflowState.RUNNING,
                2,
            )
            current = await application.workflow_kernel.load(run_id)
            assert current is not None
            assert (current.state, current.state_version) == (WorkflowState.RUNNING, 2)

            snapshot, authentic_attempt = await application.execution_repository.load_authority(
                work_run_id=run_id, execution_attempt_id=attempt_id
            )
            assert (snapshot.state, snapshot.state_version) == (WorkflowState.RUNNING, 2)
            assert authentic_attempt.execution_attempt_id == attempt.owner_ref == attempt_id
            async with sessions() as session:
                persisted_attempt = await session.get(ExecutionAttemptRow, attempt_id)
                assert persisted_attempt is not None
                assert persisted_attempt.work_run_id == run_id

            sealed = await capture.adapter.seal_security_context(
                capture.prepared, running.owner_ref
            )
            assert (sealed.status, sealed.workflow_state, sealed.state_version) == (
                "ADMITTED",
                WorkflowState.RUNNING,
                2,
            )
            authorized = await capture.adapter.authorize_runtime(capture.prepared, sealed.owner_ref)
            assert (authorized.status, authorized.workflow_state, authorized.state_version) == (
                "ADMITTED",
                WorkflowState.RUNNING,
                2,
            )
            authority = capture.adapter.security_authorization(authorized.owner_ref)
            assert isinstance(authority, StockroomSecurityAuthorization)
            assert authority.repository_scope.domain is ResourceDomain.REPOSITORY
            assert authority.filesystem_scope.domain is ResourceDomain.FILESYSTEM
            assert authority.repository_decision.decision is SecurityAdmissionDecision.ALLOW
            assert authority.filesystem_decision.decision is SecurityAdmissionDecision.ALLOW
            assert authority.repository_capability.snapshot.state is WorkflowState.RUNNING
            assert authority.repository_capability.snapshot.state_version == 2
            assert authority.filesystem_capability.snapshot.state_version == 2
            assert authority.network_grant_issued is False

            foreign_capture = application.prepare_capture(
                scenario_id=SCENARIO_IDS[0],
                run_id=f"{run_id}-foreign",
                attempt_id=f"{attempt_id}-foreign",
            )
            rejected_foreign_prepared = await capture.adapter.materialize(
                foreign_capture.prepared,
                authorized.owner_ref,
            )
            assert rejected_foreign_prepared.status == "DENIED"
            assert counters["materialize"] == 0

            resource = application.composition.catalog.resource
            materialized_destination = private_runtime_root
            bounded_owner_return = MaterializedStockroom(
                resource_ref=resource.resource_ref,
                source_commit=resource.source_commit,
                subroot=resource.subroot,
                git_subtree=resource.git_subtree,
                files=tuple(
                    MaterializedFile(item.path, item.mode, item.bytes, item.sha256)
                    for item in resource.files
                ),
                aggregate_sha256=resource.aggregate_sha256,
                workspace_lease=StockroomWorkspaceLease(
                    lease_id="bounded-owner-return",
                    run_id=run_id,
                    attempt_id=attempt_id,
                    runtime_root=private_runtime_root,
                    destination=materialized_destination,
                ),
                run_id=run_id,
                attempt_id=attempt_id,
                resolved_source_root=materialized_destination,
            )
            bounded_returns[(run_id, attempt_id)] = bounded_owner_return

            materialized_call = await capture.adapter.materialize(
                capture.prepared,
                authorized.owner_ref,
            )
            assert (
                materialized_call.status,
                materialized_call.workflow_state,
                materialized_call.state_version,
            ) == ("ADMITTED", WorkflowState.RUNNING, 2)
            assert counters["materialize"] == 1
            assert capture.materialized_result is not None
            assert type(capture.materialized_result) is StockroomMaterializedResultBinding
            materialized_result = capture.materialized_result
            assert materialized_result.materialized is bounded_owner_return
            materializer_derivation = materialized_result.materializer_derivation
            assert type(materializer_derivation.owner) is StockroomMaterializer
            assert len(materializer_derivation.owner._authorities) == 1
            materialization_authority = materializer_derivation.owner._authorities[0]
            assert (
                materializer_derivation.provenance.factory_ref == materializer_factory.factory_ref
            )
            assert (
                materializer_derivation.provenance.factory_fingerprint
                == materializer_factory.factory_fingerprint
            )
            assert (
                materializer_derivation.provenance.prepared_binding_fingerprint
                == capture.prepared.attempt_binding.binding_fingerprint
            )
            assert materializer_derivation.provenance.run_id == run_id
            assert materializer_derivation.provenance.attempt_id == attempt_id
            result_provenance = materialized_result.provenance
            assert result_provenance.factory_ref == materializer_factory.factory_ref
            assert result_provenance.factory_fingerprint == materializer_factory.factory_fingerprint
            assert (
                result_provenance.prepared_binding_fingerprint
                == capture.prepared.attempt_binding.binding_fingerprint
            )
            assert (
                result_provenance.materializer_derivation_provenance_fingerprint
                == materializer_derivation.provenance.provenance_fingerprint
            )
            assert (result_provenance.run_id, result_provenance.attempt_id) == (
                run_id,
                attempt_id,
            )
            assert result_provenance.resource_ref == resource.resource_ref == RESOURCE_REF
            assert result_provenance.source_commit == resource.source_commit
            assert result_provenance.subroot == resource.subroot
            assert result_provenance.git_subtree == resource.git_subtree
            assert result_provenance.aggregate_sha256 == resource.aggregate_sha256
            assert (
                result_provenance.materialized_file_manifest_fingerprint
                == resource.aggregate_sha256
            )
            assert len(result_provenance.workspace_lease_fingerprint) == 64
            assert len(result_provenance.resolved_source_root_fingerprint) == 64
            assert len(result_provenance.materialized_output_fingerprint) == 64
            with pytest.raises(FrozenInstanceError):
                materialized_result.materialized_identity = 0  # type: ignore[misc]

            runtime = capture.adapter._handles[materialized_call.owner_ref]
            execution_inputs = runtime.execution_inputs
            execution_derivation = runtime.execution_derivation
            assert type(execution_derivation.owner) is AgentExecutionService
            assert execution_derivation.owner._tool_dispatcher is execution_inputs.dispatcher
            assert execution_derivation.provenance.factory_ref == execution_factory.factory_ref
            assert (
                execution_derivation.provenance.prepared_binding_fingerprint
                == capture.prepared.attempt_binding.binding_fingerprint
            )
            assert execution_derivation.provenance.run_id == run_id
            assert execution_derivation.provenance.attempt_id == attempt_id
            assert (
                execution_derivation.provenance.materialized_result_provenance_fingerprint
                == result_provenance.provenance_fingerprint
            )
            assert (
                execution_derivation.provenance.materialized_output_fingerprint
                == result_provenance.materialized_output_fingerprint
            )

            raw_materialized = replace(bounded_owner_return)
            with pytest.raises(AuthorityConflictError):
                execution_factory.prepare_inputs(
                    prepared=capture.prepared,
                    materialized_result=raw_materialized,
                )
            with pytest.raises(AuthorityConflictError):
                execution_factory.prepare_inputs(
                    prepared=capture.prepared,
                    materialized_result=replace(materialized_result),
                )
            with pytest.raises(AuthorityConflictError):
                execution_factory.prepare_inputs(
                    prepared=foreign_capture.prepared,
                    materialized_result=materialized_result,
                )

            tampered_outputs = (
                replace(bounded_owner_return, run_id="foreign-run"),
                replace(bounded_owner_return, attempt_id="foreign-attempt"),
                replace(bounded_owner_return, resource_ref="repository:foreign@invalid"),
                replace(bounded_owner_return, source_commit="0" * 40),
                replace(bounded_owner_return, subroot="examples/foreign-stockroom/"),
                replace(bounded_owner_return, git_subtree="0" * 40),
                replace(bounded_owner_return, aggregate_sha256="0" * 64),
                replace(
                    bounded_owner_return,
                    files=(
                        replace(bounded_owner_return.files[0], sha256="0" * 64),
                        *bounded_owner_return.files[1:],
                    ),
                ),
                replace(
                    bounded_owner_return,
                    workspace_lease=replace(
                        bounded_owner_return.workspace_lease,
                        lease_id="foreign-lease",
                    ),
                ),
                replace(
                    bounded_owner_return,
                    workspace_lease=replace(
                        bounded_owner_return.workspace_lease,
                        run_id="foreign-run",
                    ),
                ),
                replace(
                    bounded_owner_return,
                    workspace_lease=replace(
                        bounded_owner_return.workspace_lease,
                        attempt_id="foreign-attempt",
                    ),
                ),
                replace(
                    bounded_owner_return,
                    workspace_lease=replace(
                        bounded_owner_return.workspace_lease,
                        runtime_root=tmp_path / "foreign-runtime",
                    ),
                ),
                replace(
                    bounded_owner_return,
                    workspace_lease=replace(
                        bounded_owner_return.workspace_lease,
                        destination=tmp_path / "foreign-destination",
                    ),
                ),
                replace(
                    bounded_owner_return,
                    resolved_source_root=tmp_path / "foreign-source-root",
                ),
            )
            for tampered_output in tampered_outputs:
                with pytest.raises(ValueError):
                    replace(
                        materialized_result,
                        materialized=tampered_output,
                        materialized_identity=id(tampered_output),
                    )
            with pytest.raises(ValueError):
                replace(result_provenance, provenance_fingerprint="0" * 64)

            foreign_materializer_factory = replace(materializer_factory)
            foreign_materializer_owners = replace(
                capture.prepared.owners,
                materializer_factory=foreign_materializer_factory,
            )
            foreign_materializer_prepared = replace(
                capture.prepared,
                owners=foreign_materializer_owners,
            )
            foreign_materialized_result = foreign_materializer_factory.materialize(
                prepared=foreign_materializer_prepared,
                authorization=authority,
                authority=materialization_authority,
                repository_root=application.repository_root,
                private_runtime_root=application.private_runtime_root,
            )
            assert foreign_materialized_result.materialized is bounded_owner_return
            with pytest.raises(AuthorityConflictError):
                execution_factory.prepare_inputs(
                    prepared=capture.prepared,
                    materialized_result=foreign_materialized_result,
                )

            foreign_execution_factory = replace(execution_factory)
            foreign_execution_owners = replace(
                capture.prepared.owners,
                agent_execution_service_factory=foreign_execution_factory,
            )
            foreign_execution_prepared = replace(
                capture.prepared,
                owners=foreign_execution_owners,
            )
            with pytest.raises(AuthorityConflictError):
                execution_factory.prepare_inputs(
                    prepared=foreign_execution_prepared,
                    materialized_result=materialized_result,
                )
            with pytest.raises(AuthorityConflictError):
                foreign_execution_factory.prepare_inputs(
                    prepared=capture.prepared,
                    materialized_result=materialized_result,
                )

            with pytest.raises(AuthorityConflictError):
                replace(materializer_factory).derive(
                    prepared=capture.prepared,
                    authorization=authority,
                    authority=materialization_authority,
                    repository_root=application.repository_root,
                    private_runtime_root=application.private_runtime_root,
                )
            with pytest.raises(AuthorityConflictError):
                materializer_factory.derive(
                    prepared=capture.prepared,
                    authorization=authority,
                    authority=replace(
                        materialization_authority,
                        principal_ref="foreign-principal",
                    ),
                    repository_root=application.repository_root,
                    private_runtime_root=application.private_runtime_root,
                )
            with pytest.raises(AuthorityConflictError):
                materializer_factory.derive(
                    prepared=capture.prepared,
                    authorization=authority,
                    authority=materialization_authority,
                    repository_root=tmp_path,
                    private_runtime_root=application.private_runtime_root,
                )
            with pytest.raises(AuthorityConflictError):
                replace(execution_factory).derive(
                    prepared=capture.prepared,
                    inputs=execution_inputs,
                    execution_reference_authority=application.execution_reference_authority,
                )
            with pytest.raises(AuthorityConflictError):
                execution_factory.derive(
                    prepared=capture.prepared,
                    inputs=replace(
                        execution_inputs,
                        spec=replace(execution_inputs.spec, run_id="foreign-run"),
                    ),
                    execution_reference_authority=application.execution_reference_authority,
                )
            with pytest.raises(AuthorityConflictError):
                execution_factory.derive(
                    prepared=capture.prepared,
                    inputs=replace(
                        execution_inputs,
                        registry=replace(execution_inputs.registry),
                    ),
                    execution_reference_authority=application.execution_reference_authority,
                )
            with pytest.raises(AuthorityConflictError):
                execution_factory.derive(
                    prepared=capture.prepared,
                    inputs=replace(
                        execution_inputs,
                        dispatcher=StockroomSummaryDispatcher(
                            application.docker_runtime, execution_inputs.spec
                        ),
                    ),
                    execution_reference_authority=application.execution_reference_authority,
                )
            with pytest.raises(AuthorityConflictError):
                execution_factory.derive(
                    prepared=capture.prepared,
                    inputs=execution_inputs,
                    execution_reference_authority=ExecutionReferenceAuthority(),
                )

            assert counters == {
                "docker": 0,
                "materialize": 2,
                "provider": 0,
                "dispatcher": 0,
                "execution": 0,
            }
            assert tuple(private_runtime_root.iterdir()) == ()
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.parametrize("identifiers", [("s", "a"), ("??:??", "attempt/?"), ("e\u0301", "?")])
def test_execution_bound_ref_canonical_roundtrip(identifiers) -> None:
    from aiscc.workflow.guards import decode_execution_bound_refs, encode_execution_bound_refs

    refs = encode_execution_bound_refs(*identifiers)
    assert decode_execution_bound_refs(refs) == identifiers
    assert "=" not in "".join(refs)
    assert encode_execution_bound_refs(*decode_execution_bound_refs(refs)) == refs


@pytest.mark.parametrize("identifiers", [("", "a"), ("s", ""), (None, "a"), ("\ud800", "a")])
def test_execution_bound_ref_empty_or_invalid_identifier_denied(identifiers) -> None:
    from aiscc.workflow.guards import encode_execution_bound_refs

    with pytest.raises(ValueError):
        encode_execution_bound_refs(*identifiers)


@pytest.mark.parametrize(
    "mutation",
    [
        "empty",
        "one",
        "extra",
        "order",
        "duplicate",
        "prefix",
        "version",
        "type",
        "padding",
        "alphabet",
        "length",
        "noncanonical",
        "utf8",
        "empty_payload",
    ],
)
def test_execution_bound_ref_decoder_denies_noncanonical(mutation) -> None:
    from aiscc.workflow.guards import decode_execution_bound_refs, encode_execution_bound_refs

    refs = encode_execution_bound_refs("s", "a")
    prefix = "aiscc-bound-ref:v1:execution-submission:"
    cases = {
        "empty": (),
        "one": refs[:1],
        "extra": (*refs, refs[0]),
        "order": refs[::-1],
        "duplicate": (refs[0], refs[0]),
        "prefix": (refs[0].replace("aiscc-", "other-"), refs[1]),
        "version": (refs[0].replace(":v1:", ":v2:"), refs[1]),
        "type": (refs[0].replace("execution-submission", "evidence"), refs[1]),
        "padding": (prefix + "cw==", refs[1]),
        "alphabet": (prefix + "+w", refs[1]),
        "length": (prefix + "c", refs[1]),
        "noncanonical": (prefix + "cx", refs[1]),
        "utf8": (prefix + "_w", refs[1]),
        "empty_payload": (prefix, refs[1]),
    }
    with pytest.raises(ValueError, match="NON_CANONICAL_BOUND_REF"):
        decode_execution_bound_refs(cases[mutation])


def _execution_link_fixture():
    """Synthetic rows only: exercise real issuers/evaluator/history code without a database."""
    from aiscc.persistence import repository
    from aiscc.persistence.models import (
        TransitionDecisionRow,
        TransitionEvaluationRow,
        TransitionRequestRow,
        WorkRunRow,
    )
    from aiscc.providers.models import ExecutionStatus, ExecutionSubmissionRef
    from aiscc.workflow.evaluator import TransitionEvaluator
    from aiscc.workflow.guards import P1_4GuardAuthority
    from aiscc.workflow.models import GuardId, WorkRun

    authority = P1_4GuardAuthority()
    producer = ExecutionReferenceAuthority()
    now = datetime(2026, 9, 12, 12, 58, tzinfo=UTC)
    submission = producer.register_submission(
        ExecutionSubmissionRef(
            "submission-1",
            "attempt-1",
            "run-1",
            "task-1",
            "1",
            WorkflowState.RUNNING,
            2,
            ExecutionStatus.EXECUTOR_COMPLETED,
            "a" * 64,
            producer.issuer_ref,
        )
    )
    current = None
    steps = []
    for version, target in enumerate(
        (WorkflowState.READY, WorkflowState.RUNNING, WorkflowState.ADMISSION_PENDING)
    ):
        request = TransitionRequest(
            f"request-{version}",
            "project-1",
            "task-1",
            "1",
            "run-1",
            current.state if current else None,
            version,
            target,
            "system",
            RequesterType.SYSTEM,
            RuntimeMode.OWNER_SELF_DOGFOOD,
            created_at=now,
        )
        facts = []
        for guard in sorted(TRANSITION_MATRIX[(request.observed_state, target)], key=str):
            if guard is GuardId.G_EXECUTOR_SUBMISSION:
                fact = authority.issue_from_execution_ref(
                    guard_id=guard, execution_ref=submission, verifier=producer, request=request
                )
            else:
                fact = authority.issue(
                    guard_id=guard,
                    satisfied=True,
                    reason="SYNTHETIC_STATIC_FIXTURE",
                    authority_ref="test-owner",
                    request=request,
                )
            facts.append(fact)
        evaluation, decision = TransitionEvaluator(authority).evaluate(
            request=request, current=current, facts=tuple(facts), now=now
        )
        assert decision.outcome is DecisionOutcome.ADMITTED
        current = WorkRun(
            "project-1",
            "task-1",
            "1",
            "run-1",
            target,
            version + 1,
            RuntimeMode.OWNER_SELF_DOGFOOD,
            now,
            now,
        )
        steps.append(
            (
                repository._request_row(
                    request, repository._request_fingerprint(request, tuple(facts))
                ),
                repository._evaluation_row(evaluation),
                repository._decision_row(decision),
            )
        )
    projection = WorkRunRow(
        project_id=current.project_id,
        task_contract_id=current.task_contract_id,
        task_contract_version=current.task_contract_version,
        work_run_id=current.work_run_id,
        workflow_state=current.state.value,
        state_version=current.state_version,
        runtime_mode=current.runtime_mode.value,
        created_at=now,
        updated_at=now,
    )

    class RowSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return False

        def begin(self):
            return self

        async def get(self, model, identity):
            if model is WorkRunRow:
                return projection if identity == projection.work_run_id else None
            index, field = {
                TransitionRequestRow: (0, "transition_request_id"),
                TransitionEvaluationRow: (1, "transition_evaluation_id"),
                TransitionDecisionRow: (2, "transition_decision_id"),
            }[model]
            return next((s[index] for s in steps if getattr(s[index], field) == identity), None)

        async def scalars(self, query):
            description = query.column_descriptions[0]
            if description["name"] == "transition_decision_id":
                return [s[2].transition_decision_id for s in steps]
            model = description["entity"]
            request_id = next(iter(query.compile().params.values()))
            index = 1 if model is TransitionEvaluationRow else 2
            return [s[index] for s in steps if s[0].transition_request_id == request_id]

        async def execute(self, query, *args):
            if str(query).startswith("SELECT pg_advisory_xact_lock"):
                return None
            return [(s[2], s[1], s[0]) for s in steps]

    return SimpleNamespace(
        authority=authority,
        producer=producer,
        submission=submission,
        current=current,
        steps=steps,
        projection=projection,
        session=RowSession(),
    )


def test_verified_execution_guard_and_historical_link_roundtrip() -> None:
    from aiscc.persistence import repository
    from aiscc.workflow.guards import decode_execution_bound_refs
    from aiscc.workflow.models import GuardId

    fixture = _execution_link_fixture()
    verified = run(
        repository.verify_historical_transition_provenance(
            fixture.session, fixture.steps[-1][0].transition_request_id
        )
    )
    guard = next(
        g for g in verified.evaluation.guards if g.guard_id is GuardId.G_EXECUTOR_SUBMISSION
    )
    assert decode_execution_bound_refs(guard.bound_refs) == ("submission-1", "attempt-1")
    assert verified.request.observed_state is WorkflowState.RUNNING
    assert verified.request.observed_state_version == 2
    assert verified.work_run == fixture.current
    assert verified.decision.resulting_state_version == 3


@pytest.mark.parametrize(
    "mutation", ["missing_submission", "missing_attempt", "bad", "order", "extra"]
)
def test_historical_execution_binding_fails_closed(mutation) -> None:
    from aiscc.persistence import repository

    fixture = _execution_link_fixture()
    guard = next(g for g in fixture.steps[-1][1].guards if g["guard_id"] == "G_EXECUTOR_SUBMISSION")
    refs = guard["bound_refs"]
    guard["bound_refs"] = {
        "missing_submission": refs[1:],
        "missing_attempt": refs[:1],
        "bad": ["wrong-prefix", refs[1]],
        "order": refs[::-1],
        "extra": [*refs, refs[0]],
    }[mutation]
    with pytest.raises(repository.HistoricalTransitionProvenanceError):
        run(
            repository.verify_historical_transition_provenance(
                fixture.session, fixture.steps[-1][0].transition_request_id
            )
        )


def test_execution_guard_requires_authentic_ref_and_cannot_substitute_evidence() -> None:
    from aiscc.persistence import repository
    from aiscc.workflow.evaluator import TransitionEvaluator
    from aiscc.workflow.guards import encode_execution_bound_refs
    from aiscc.workflow.models import GuardId

    fixture = _execution_link_fixture()
    request = repository._transition_request_from_row(fixture.steps[-1][0])
    with pytest.raises(ValueError):
        fixture.authority.issue(
            guard_id=GuardId.G_EXECUTOR_SUBMISSION,
            satisfied=True,
            reason="claim",
            authority_ref="caller",
            request=request,
        )
    with pytest.raises(ValueError):
        fixture.authority.issue_from_execution_ref(
            guard_id=GuardId.G_EXECUTOR_SUBMISSION,
            execution_ref=replace(fixture.submission),
            verifier=fixture.producer,
            request=request,
        )
    fact = fixture.authority.issue_from_execution_ref(
        guard_id=GuardId.G_EXECUTOR_SUBMISSION,
        execution_ref=fixture.submission,
        verifier=fixture.producer,
        request=request,
    )
    assert fixture.authority.recognizes(fact)
    assert not fixture.authority.recognizes(
        replace(fact, bound_refs=encode_execution_bound_refs("foreign", "attempt-1"))
    )
    acceptance = replace(
        request,
        observed_state=WorkflowState.ADMISSION_PENDING,
        observed_state_version=3,
        target_state=WorkflowState.ACCEPTED,
        evidence_refs=(fixture.submission.submission_id,),
    )
    evaluation, decision = TransitionEvaluator(fixture.authority).evaluate(
        request=acceptance,
        current=fixture.current,
        facts=(fact,),
    )
    assert decision.outcome is DecisionOutcome.DENIED
    assert GuardId.G_EVIDENCE in evaluation.missing_guards
    assert not any(g.guard_id is GuardId.G_EVIDENCE and g.satisfied for g in evaluation.guards)


@pytest.mark.parametrize(
    "mutation",
    [
        "positive",
        "wrong_submission",
        "wrong_attempt",
        "wrong_version",
        "unrelated",
        "missing_predecessor",
        "ref_only",
        "wrong_current",
        "unregistered",
        "stale_current",
    ],
)
def test_runtime_evidence_requires_current_exact_link_and_verified_producer(mutation) -> None:
    from aiscc.providers.service import DurableExecutionResult
    from aiscc.scenarios.stockroom_production import StockroomCaptureOwnerAdapter

    fixture = _execution_link_fixture()
    current = fixture.current
    if mutation == "wrong_current":
        current = replace(current, state=WorkflowState.RUNNING)
    calls = []

    async def load(run_id):
        assert run_id == "run-1"
        return current

    async def observe(prepared):
        nonlocal current
        if mutation == "stale_current":
            current = replace(current, state_version=4)
        return {"tool_output_ref": "verified-tool"}

    async def submit(*args, **kwargs):
        calls.append(kwargs)
        return "normal-evidence-admission-path"

    producer_ref = fixture.submission
    if mutation == "wrong_submission":
        producer_ref = fixture.producer.register_submission(
            replace(producer_ref, submission_id="other")
        )
    elif mutation == "wrong_attempt":
        producer_ref = fixture.producer.register_submission(
            replace(producer_ref, execution_attempt_id="other")
        )
    elif mutation == "wrong_version":
        producer_ref = fixture.producer.register_submission(replace(producer_ref, state_version=1))
    elif mutation == "unregistered":
        producer_ref = replace(producer_ref)
    adapter = object.__new__(StockroomCaptureOwnerAdapter)
    prepared = prepared_driver("stockroom-s1-normal")
    requirement = SimpleNamespace(task_contract_id="task-1", task_contract_version="1")
    adapter._app = SimpleNamespace(
        session_factory=lambda: fixture.session,
        workflow_kernel=SimpleNamespace(load=load),
        execution_reference_authority=fixture.producer,
        evidence_enrollments={
            prepared.request.scenario_id: SimpleNamespace(requirement=requirement)
        },
        runtime_evidence_issuer=object(),
    )
    adapter._handles = {"submission-1": DurableExecutionResult("COMPLETED", producer_ref)}
    adapter.verify_runtime_summary_source = observe
    adapter._submit_durable_candidate = submit
    predecessor_id = fixture.steps[-1][2].transition_decision_id
    if mutation == "unrelated":
        predecessor_id = fixture.steps[-2][2].transition_decision_id
    elif mutation == "missing_predecessor":
        predecessor_id = "missing"
    elif mutation == "ref_only":
        predecessor_id = fixture.submission.submission_id
    result = run(adapter.submit_runtime_evidence(prepared, predecessor_id))
    if mutation == "positive":
        assert result.status == "ADMITTED"
        assert len(calls) == 1
        assert calls[0]["value"]["execution_submission_ref"] == fixture.submission.submission_id
        assert result.workflow_state is WorkflowState.ADMISSION_PENDING
        assert fixture.submission.state is WorkflowState.RUNNING
        assert fixture.submission.state_version == 2
    else:
        assert result.status == "DENIED"
        assert calls == []


def test_runner_passes_admitted_predecessor_identity_in_existing_order() -> None:
    class LinkedOwners(RecordingOwners):
        async def submit_runtime_evidence(self, prepared, predecessor_ref):
            assert predecessor_ref == "owner:transition:ADMISSION_PENDING"
            assert [name for name, _ in self.calls][-2:] == [
                "execute",
                "transition:ADMISSION_PENDING",
            ]
            return await super().submit_runtime_evidence(prepared, predecessor_ref)

    owners = LinkedOwners()
    run(StockroomCaptureRunner(owners).run(prepared_driver("stockroom-s1-normal")))
    assert any(name == "submit_runtime" for name, _ in owners.calls)


def test_same_shape_admitted_pending_predecessor_denies_cross_producer_substitution() -> None:
    from aiscc.persistence import repository
    from aiscc.providers.service import DurableExecutionResult
    from aiscc.scenarios.stockroom_production import StockroomCaptureOwnerAdapter
    from aiscc.workflow.evaluator import TransitionEvaluator
    from aiscc.workflow.guards import decode_execution_bound_refs
    from aiscc.workflow.models import GuardId

    fixture = _execution_link_fixture()
    original = fixture.submission
    linked_producer = fixture.producer.register_submission(
        replace(original, submission_id="different-authentic-submission")
    )
    request = repository._transition_request_from_row(fixture.steps[-1][0])
    # Both producers are authentic for the same run, attempt and original RUNNING/v2.
    assert fixture.producer.verify(original, request, GuardId.G_EXECUTOR_SUBMISSION)
    assert fixture.producer.verify(linked_producer, request, GuardId.G_EXECUTOR_SUBMISSION)
    execution_fact = fixture.authority.issue_from_execution_ref(
        guard_id=GuardId.G_EXECUTOR_SUBMISSION,
        execution_ref=linked_producer,
        verifier=fixture.producer,
        request=request,
    )
    scope_fact = fixture.authority.issue(
        guard_id=GuardId.G_SCOPE,
        satisfied=True,
        reason="SYNTHETIC_STATIC_FIXTURE",
        authority_ref="test-owner",
        request=request,
    )
    facts = (execution_fact, scope_fact)
    running = replace(fixture.current, state=WorkflowState.RUNNING, state_version=2)
    evaluation, decision = TransitionEvaluator(fixture.authority).evaluate(
        request=request, current=running, facts=facts, now=fixture.current.updated_at
    )
    assert decision.outcome is DecisionOutcome.ADMITTED
    fixture.steps[-1] = (
        repository._request_row(request, repository._request_fingerprint(request, facts)),
        repository._evaluation_row(evaluation),
        repository._decision_row(decision),
    )
    # Verify the complete historical lineage; denial must not come from malformed rows.
    historical = run(
        repository.verify_historical_transition_provenance(
            fixture.session, request.transition_request_id
        )
    )
    assert historical.work_run == fixture.current
    assert historical.request.work_run_id == original.work_run_id
    assert historical.request.observed_state is WorkflowState.RUNNING
    assert historical.request.observed_state_version == original.state_version == 2
    assert historical.request.target_state is WorkflowState.ADMISSION_PENDING
    assert historical.decision.resulting_state is fixture.current.state
    assert historical.decision.resulting_state_version == fixture.current.state_version == 3
    guard = next(
        g for g in historical.evaluation.guards if g.guard_id is GuardId.G_EXECUTOR_SUBMISSION
    )
    assert decode_execution_bound_refs(guard.bound_refs) == (
        linked_producer.submission_id,
        original.execution_attempt_id,
    )
    assert linked_producer.submission_id != original.submission_id
    calls = []
    resolved = []

    async def load(run_id):
        assert run_id == fixture.current.work_run_id
        return fixture.current

    async def observe(prepared):
        calls.append("observation")
        return {"tool_output_ref": "verified-tool"}

    async def submit(*args, **kwargs):
        calls.append("candidate-submission")
        return "normal-evidence-admission-path"

    adapter = object.__new__(StockroomCaptureOwnerAdapter)
    prepared = prepared_driver("stockroom-s1-normal")
    requirement = SimpleNamespace(task_contract_id="task-1", task_contract_version="1")
    adapter._app = SimpleNamespace(
        session_factory=lambda: fixture.session,
        workflow_kernel=SimpleNamespace(load=load),
        execution_reference_authority=fixture.producer,
        evidence_enrollments={
            prepared.request.scenario_id: SimpleNamespace(requirement=requirement)
        },
        runtime_evidence_issuer=object(),
    )
    # Deliberately substitute the other authentic producer at the linked handle boundary.
    substituted = DurableExecutionResult("COMPLETED", original)
    adapter._handles = {linked_producer.submission_id: substituted}
    original_require_handle = adapter._require_handle

    def record_handle(ref, kind):
        result = original_require_handle(ref, kind)
        resolved.append(result)
        return result

    adapter._require_handle = record_handle
    adapter.verify_runtime_summary_source = observe
    adapter._submit_durable_candidate = submit
    denied = run(adapter.submit_runtime_evidence(prepared, decision.transition_decision_id))
    assert resolved == [substituted]  # not missing/invalid handle setup
    assert denied.status == "DENIED"
    assert calls == []  # before observation and EvidenceCandidate submission
    # Same history/current state with the exact linked producer reaches normal admission.
    adapter._handles[linked_producer.submission_id] = DurableExecutionResult(
        "COMPLETED", linked_producer
    )
    admitted = run(adapter.submit_runtime_evidence(prepared, decision.transition_decision_id))
    assert admitted.status == "ADMITTED"
    assert calls == ["observation", "candidate-submission"]
