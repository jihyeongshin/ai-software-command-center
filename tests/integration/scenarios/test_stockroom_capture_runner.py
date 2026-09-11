from __future__ import annotations

import asyncio
import json
import os
from collections.abc import Coroutine
from dataclasses import FrozenInstanceError, replace
from datetime import UTC, datetime
from pathlib import Path
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
                item["evidence_basis_kind"] is None
                for item in legacy_judgment_config["policies"]
            )
            assert tuple(
                item["evidence_basis_kind"] for item in judgment_config["policies"]
            ) == (
                JudgmentEvidenceBasisKind.SATISFIED_ATTESTATION,
                JudgmentEvidenceBasisKind.UNSATISFIED_SET_EVALUATION,
            )
            malformed_judgment = json.loads(
                (
                    repository_root / "config/judgment/stockroom-capture.v2.json"
                ).read_text(encoding="utf-8")
            )
            malformed_judgment["policies"][1].pop("evidence_checkpoint_ref")
            malformed_path = tmp_path / "malformed-judgment-v2.json"
            malformed_path.write_text(
                json.dumps(malformed_judgment), encoding="utf-8"
            )
            with pytest.raises(ValueError, match="judgment policy has unknown or missing keys"):
                load_stockroom_judgment_config(malformed_path)
            malformed_path.unlink()

            application = await build_stockroom_production(
                session_factory=sessions,
                repository_root=repository_root,
                private_runtime_root=tmp_path,
                downloads_root=Path.home() / "Downloads",
                trusted_git_executable=tmp_path / "git.exe",
                docker_process_runner=docker_runner,
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
                request = s2_capture.adapter._request(
                    s2_capture.prepared, source, version, target
                )
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
                decision = await application.workflow_kernel.request_transition(
                    request, facts
                )
                assert decision.outcome is DecisionOutcome.ADMITTED
            s2_evaluation = await s2_capture.adapter.evaluate_evidence(
                s2_capture.prepared, None
            )
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
                assert (
                    s2_judgment_row.payload["evidence_evaluation_ref"]
                    == s2_evaluation.owner_ref
                )
                assert s2_judgment_row.payload["evidence_attestation_ref"] is None
                assert s2_judgment_row.payload["reason_code"] == (
                    "STOCKROOM_REQUIRED_EVIDENCE_UNSATISFIED"
                )
                assert (
                    s2_evaluation.owner_ref
                    not in str(s2_judgment_row.payload["reason_code"])
                )
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
                        select(JudgmentRow).where(
                            JudgmentRow.work_run_id.in_(no_judgment_runs)
                        )
                    )
                )

            run_id = f"stockroom-production-{uuid4()}"
            attempt_id = f"stockroom-attempt-{uuid4()}"
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
            materialized_destination = tmp_path
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
                    runtime_root=tmp_path,
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
            assert tuple(tmp_path.iterdir()) == ()
        finally:
            await engine.dispose()

    run(scenario())
