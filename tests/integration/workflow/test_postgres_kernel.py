from __future__ import annotations

import asyncio
import hashlib
import os
from collections.abc import Coroutine
from typing import Any
from uuid import uuid4

import pytest
from sqlalchemy import func, select, text

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.persistence import PostgresTransitionRepository, create_engine, create_session_factory
from aiscc.persistence.models import (
    P1_4BlockerProvenanceRow,
    TransitionDecisionRow,
    TransitionEvaluationRow,
    TransitionRequestRow,
)
from aiscc.persistence.repository import (
    HistoricalTransitionProvenanceError,
    _historical_evaluation_from_row,
    _request_fingerprint,
    _transition_request_from_row,
    acquire_work_run_transaction_lock,
    verify_historical_transition_provenance,
)
from aiscc.providers.authority import ExecutionReferenceAuthority
from aiscc.providers.models import ExecutionStatus, ExecutionSubmissionRef
from aiscc.workflow.evaluator import TransitionEvaluator
from aiscc.workflow.guards import (
    GUARD_OWNER_POLICY,
    FutureOwnerGuardVerifier,
    P1_4GuardAuthority,
    TrustedGuardFact,
    required_bound_refs,
)
from aiscc.workflow.kernel import WorkflowKernel
from aiscc.workflow.matrix import TRANSITION_MATRIX
from aiscc.workflow.models import (
    AuthorityConflictError,
    BlockerKindV1,
    BlockerReasonCodeV1,
    DecisionOutcome,
    DecisionReason,
    GuardId,
    GuardSemanticOwner,
    P1_4BlockerClaimV1,
    P1_4BlockerResolutionClaimV1,
    RequesterType,
    TransitionDecision,
    TransitionRequest,
)
from aiscc.workflow.ports import FailurePoint


class TestBlockerSourceVerifier:
    async def verify_resolution_source(self, session: Any, **values: Any) -> bool:
        del session
        claim = values["claim"]
        return (
            values["resolution_source_contract_ref"] == "resolution-contract:v1:test"
            and values["resolution_source_contract_fingerprint"] == "a" * 64
            and claim.resolution_source_authority_ref == "resolution-authority:v1:test"
            and claim.resolution_source_authority_fingerprint == "b" * 64
        )


def run[T](coroutine: Coroutine[Any, Any, T]) -> T:
    return asyncio.run(coroutine)


@pytest.fixture(scope="module")
def database_url() -> str:
    value = os.environ.get("AISCC_TEST_DATABASE_URL")
    if not value:
        pytest.skip("AISCC_TEST_DATABASE_URL is required for PostgreSQL evidence")
    return value


def build_kernel(
    database_url: str,
) -> tuple[
    WorkflowKernel,
    PostgresTransitionRepository,
    TestGuardAuthority,
    Any,
]:
    engine = create_engine(database_url)
    authority = TestGuardAuthority()
    repository = PostgresTransitionRepository(
        create_session_factory(engine),
        TransitionEvaluator(authority.system, authority.future_verifiers),
        TestBlockerSourceVerifier(),
    )
    return WorkflowKernel(repository), repository, authority, engine


def request(
    *,
    run_id: str,
    source: WorkflowState | None,
    version: int,
    target: WorkflowState,
    request_id: str | None = None,
    evidence_refs: tuple[str, ...] = (),
    human_result_refs: tuple[str, ...] = (),
    judgment_refs: tuple[str, ...] = (),
    project_id: str = "project-p1-4",
    task_contract_id: str = "task-contract-p1-4",
    task_contract_version: str = "v1",
    runtime_mode: RuntimeMode = RuntimeMode.OWNER_SELF_DOGFOOD,
    blocker_resolution_claim: P1_4BlockerResolutionClaimV1 | None = None,
) -> TransitionRequest:
    transition_id = request_id or f"request-{uuid4()}"
    blocker_claim = (
        P1_4BlockerClaimV1(
            f"blocker-{transition_id}",
            BlockerKindV1.EXECUTION,
            BlockerReasonCodeV1.EXECUTION_BLOCKER,
            "resolution-contract:v1:test",
            "a" * 64,
            ("source-authority:v1:test",),
            ("c" * 64,),
        )
        if target is WorkflowState.BLOCKED
        else None
    )
    return TransitionRequest(
        transition_request_id=transition_id,
        project_id=project_id,
        task_contract_id=task_contract_id,
        task_contract_version=task_contract_version,
        work_run_id=run_id,
        observed_state=source,
        observed_state_version=version,
        target_state=target,
        requester_identity="aiscc-system",
        requester_type=RequesterType.SYSTEM,
        runtime_mode=runtime_mode,
        evidence_refs=evidence_refs,
        human_result_refs=human_result_refs,
        judgment_refs=judgment_refs,
        blocker_claim=blocker_claim,
        blocker_resolution_claim=blocker_resolution_claim,
    )


class TestFutureOwnerAuthority:
    __test__ = False

    def __init__(self, semantic_owner: GuardSemanticOwner) -> None:
        self._semantic_owner = semantic_owner
        self._issuer_token = object()

    @property
    def semantic_owner(self) -> GuardSemanticOwner:
        return self._semantic_owner

    def recognizes(self, fact: TrustedGuardFact, request: TransitionRequest) -> bool:
        del request
        return fact._issuer_token is self._issuer_token

    def issue(
        self,
        guard_id: GuardId,
        transition_request: TransitionRequest,
    ) -> TrustedGuardFact:
        return TrustedGuardFact(
            guard_id=guard_id,
            semantic_owner=self.semantic_owner,
            satisfied=True,
            reason="TRUSTED_INTEGRATION_FIXTURE_PASS",
            authority_ref=f"integration-owner:{self.semantic_owner.value}",
            bound_refs=required_bound_refs(guard_id, transition_request),
            task_contract_id=transition_request.task_contract_id,
            task_contract_version=transition_request.task_contract_version,
            work_run_id=transition_request.work_run_id,
            state_version=transition_request.observed_state_version,
            _issuer_token=self._issuer_token,
        )


def execution_submission_fact(
    authority: P1_4GuardAuthority, request: TransitionRequest
) -> TrustedGuardFact:
    # Synthetic producer-owned ref; the real P1-5 verifier and P1-4 issuer perform the handoff.
    producer = ExecutionReferenceAuthority()
    identity = hashlib.sha256(request.transition_request_id.encode("utf-8")).hexdigest()
    submission = producer.register_submission(
        ExecutionSubmissionRef(
            submission_id="fixture-submission-" + identity,
            execution_attempt_id="fixture-attempt-" + identity,
            work_run_id=request.work_run_id,
            task_contract_id=request.task_contract_id,
            task_contract_version=request.task_contract_version,
            state=request.observed_state,
            state_version=request.observed_state_version,
            status=ExecutionStatus.EXECUTOR_COMPLETED,
            event_range_hash=identity,
            issuer_ref=producer.issuer_ref,
        )
    )
    return authority.issue_from_execution_ref(
        guard_id=GuardId.G_EXECUTOR_SUBMISSION,
        execution_ref=submission,
        verifier=producer,
        request=request,
    )


class TestGuardAuthority:
    __test__ = False

    def __init__(self) -> None:
        self.system = P1_4GuardAuthority()
        self._future = {
            owner: TestFutureOwnerAuthority(owner)
            for owner in (
                GuardSemanticOwner.P1_6_EVIDENCE,
                GuardSemanticOwner.P1_7_HUMAN,
                GuardSemanticOwner.P1_7_JUDGMENT,
            )
        }

    @property
    def future_verifiers(self) -> tuple[FutureOwnerGuardVerifier, ...]:
        return tuple(self._future.values())

    def issue(self, guard_id: GuardId, transition_request: TransitionRequest) -> TrustedGuardFact:
        if guard_id is GuardId.G_EXECUTOR_SUBMISSION:
            return execution_submission_fact(self.system, transition_request)
        owner = GUARD_OWNER_POLICY[guard_id]
        if owner is GuardSemanticOwner.P1_4_SYSTEM:
            return self.system.issue(
                guard_id=guard_id,
                satisfied=True,
                reason="TRUSTED_INTEGRATION_FIXTURE_PASS",
                authority_ref=f"integration:{guard_id.value}",
                request=transition_request,
            )
        return self._future[owner].issue(guard_id, transition_request)


def facts(
    authority: TestGuardAuthority,
    transition_request: TransitionRequest,
) -> tuple[TrustedGuardFact, ...]:
    required = TRANSITION_MATRIX.get(
        (transition_request.observed_state, transition_request.target_state), frozenset()
    )
    return tuple(authority.issue(guard, transition_request) for guard in sorted(required, key=str))


async def admit(
    kernel: WorkflowKernel,
    authority: TestGuardAuthority,
    transition_request: TransitionRequest,
) -> TransitionDecision:
    decision = await kernel.request_transition(
        transition_request, facts(authority, transition_request)
    )
    assert decision.outcome is DecisionOutcome.ADMITTED
    return decision


async def provenance_counts(engine: Any, run_id: str) -> tuple[int, int, int]:
    async with engine.connect() as connection:
        request_count = await connection.scalar(
            text("SELECT count(*) FROM transition_requests WHERE work_run_id = :run_id"),
            {"run_id": run_id},
        )
        evaluation_count = await connection.scalar(
            text(
                "SELECT count(*) FROM transition_evaluations e "
                "JOIN transition_requests r USING (transition_request_id) "
                "WHERE r.work_run_id = :run_id"
            ),
            {"run_id": run_id},
        )
        decision_count = await connection.scalar(
            text(
                "SELECT count(*) FROM transition_decisions d "
                "JOIN transition_requests r USING (transition_request_id) "
                "WHERE r.work_run_id = :run_id"
            ),
            {"run_id": run_id},
        )
    return int(request_count or 0), int(evaluation_count or 0), int(decision_count or 0)


@pytest.mark.postgres
def test_migration_is_at_exact_head(database_url: str) -> None:
    async def scenario() -> None:
        engine = create_engine(database_url)
        try:
            async with engine.connect() as connection:
                revision = await connection.scalar(text("SELECT version_num FROM alembic_version"))
            assert revision == "20260916_0017"
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_authoritative_mutation_restart_durability_and_consistency(database_url: str) -> None:
    async def scenario() -> None:
        run_id = f"run-durable-{uuid4()}"
        kernel, repository, authority, engine = build_kernel(database_url)
        create = request(run_id=run_id, source=None, version=0, target=WorkflowState.READY)
        ready = await admit(kernel, authority, create)
        assert ready.resulting_state_version == 1
        start = request(
            run_id=run_id,
            source=WorkflowState.READY,
            version=1,
            target=WorkflowState.RUNNING,
        )
        running = await admit(kernel, authority, start)
        assert running.resulting_state_version == 2
        submit = request(
            run_id=run_id,
            source=WorkflowState.RUNNING,
            version=2,
            target=WorkflowState.ADMISSION_PENDING,
        )
        pending = await admit(kernel, authority, submit)
        assert pending.resulting_state_version == 3
        assert len(await repository.history(run_id)) == 3
        await engine.dispose()

        restarted, restarted_repository, _, restarted_engine = build_kernel(database_url)
        try:
            projection = await restarted.load(run_id)
            assert projection is not None
            assert projection.state is WorkflowState.ADMISSION_PENDING
            assert projection.state_version == 3
            assert len(await restarted_repository.history(run_id)) == 3
            verified = await restarted.verify_consistency(run_id)
            assert verified == projection
        finally:
            await restarted_engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_canonical_historical_transition_provenance_is_rooted_in_workrun_history(
    database_url: str,
) -> None:
    async def scenario() -> None:
        run_id = f"run-historical-root-{uuid4()}"
        kernel, _, authority, engine = build_kernel(database_url)
        sessions = create_session_factory(engine)
        try:
            steps = (
                request(run_id=run_id, source=None, version=0, target=WorkflowState.READY),
                request(
                    run_id=run_id,
                    source=WorkflowState.READY,
                    version=1,
                    target=WorkflowState.RUNNING,
                ),
                request(
                    run_id=run_id,
                    source=WorkflowState.RUNNING,
                    version=2,
                    target=WorkflowState.ADMISSION_PENDING,
                ),
                request(
                    run_id=run_id,
                    source=WorkflowState.ADMISSION_PENDING,
                    version=3,
                    target=WorkflowState.HUMAN_REQUIRED,
                ),
                request(
                    run_id=run_id,
                    source=WorkflowState.HUMAN_REQUIRED,
                    version=4,
                    target=WorkflowState.BLOCKED,
                ),
            )
            decisions = [await admit(kernel, authority, step) for step in steps]
            opening = steps[3]
            opening_decision = decisions[3]

            async def verify() -> Any:
                async with sessions() as session, session.begin():
                    await acquire_work_run_transaction_lock(session, run_id)
                    return await verify_historical_transition_provenance(
                        session, opening.transition_request_id
                    )

            verified = await verify()
            assert verified.request == opening
            assert verified.decision == opening_decision
            assert verified.work_run.state is WorkflowState.BLOCKED
            assert verified.work_run.state_version == 5
            assert {item.guard_id for item in verified.evaluation.guards} == {
                GuardId.G_CURRENT,
                GuardId.G_HUMAN_REQUIRED,
            }
            human_guard = next(
                item
                for item in verified.evaluation.guards
                if item.guard_id is GuardId.G_HUMAN_REQUIRED
            )
            assert human_guard.semantic_owner is GuardSemanticOwner.P1_7_HUMAN
            assert human_guard.satisfied is True

            async with sessions() as session:
                request_row = await session.get(TransitionRequestRow, opening.transition_request_id)
                evaluation_row = await session.scalar(
                    select(TransitionEvaluationRow).where(
                        TransitionEvaluationRow.transition_request_id
                        == opening.transition_request_id
                    )
                )
                decision_row = await session.get(
                    TransitionDecisionRow, opening_decision.transition_decision_id
                )
                assert request_row is not None
                assert evaluation_row is not None
                assert decision_row is not None
                original_fingerprint = request_row.request_fingerprint
                original_guards = list(evaluation_row.guards)
                original_missing = list(evaluation_row.missing_guards)
                original_owner = decision_row.admitting_owner
                original_kernel = decision_row.kernel_version
                original_sequence = decision_row.event_sequence

            async def restore() -> None:
                async with sessions() as session, session.begin():
                    await session.execute(text("SET LOCAL session_replication_role = replica"))
                    request_row = await session.get(
                        TransitionRequestRow, opening.transition_request_id
                    )
                    evaluation_row = await session.scalar(
                        select(TransitionEvaluationRow).where(
                            TransitionEvaluationRow.transition_request_id
                            == opening.transition_request_id
                        )
                    )
                    decision_row = await session.get(
                        TransitionDecisionRow, opening_decision.transition_decision_id
                    )
                    assert request_row is not None
                    assert evaluation_row is not None
                    assert decision_row is not None
                    request_row.request_fingerprint = original_fingerprint
                    evaluation_row.guards = original_guards
                    evaluation_row.missing_guards = original_missing
                    decision_row.admitting_owner = original_owner
                    decision_row.kernel_version = original_kernel
                    decision_row.event_sequence = original_sequence

            try:
                async with sessions() as session, session.begin():
                    await session.execute(text("SET LOCAL session_replication_role = replica"))
                    row = await session.get(TransitionRequestRow, opening.transition_request_id)
                    assert row is not None
                    row.request_fingerprint = "0" * 64
                with pytest.raises(HistoricalTransitionProvenanceError, match="fingerprint"):
                    await verify()
            finally:
                await restore()

            for mutation in ("missing", "owner", "unsatisfied", "missing-set"):
                try:
                    async with sessions() as session, session.begin():
                        await session.execute(text("SET LOCAL session_replication_role = replica"))
                        row = await session.scalar(
                            select(TransitionEvaluationRow).where(
                                TransitionEvaluationRow.transition_request_id
                                == opening.transition_request_id
                            )
                        )
                        assert row is not None
                        guards = [dict(item) for item in row.guards]
                        human_index = next(
                            index
                            for index, item in enumerate(guards)
                            if item["guard_id"] == GuardId.G_HUMAN_REQUIRED.value
                        )
                        if mutation == "missing":
                            guards.pop(human_index)
                        elif mutation == "owner":
                            guards[human_index]["semantic_owner"] = (
                                GuardSemanticOwner.P1_4_SYSTEM.value
                            )
                        elif mutation == "unsatisfied":
                            guards[human_index]["satisfied"] = False
                        else:
                            row.missing_guards = [GuardId.G_HUMAN_REQUIRED.value]
                        row.guards = guards
                    with pytest.raises(HistoricalTransitionProvenanceError):
                        await verify()
                finally:
                    await restore()

            for field, corrupt_value in (
                ("admitting_owner", "UNTRUSTED_OWNER"),
                ("kernel_version", "UNTRUSTED_KERNEL"),
            ):
                try:
                    async with sessions() as session, session.begin():
                        await session.execute(text("SET LOCAL session_replication_role = replica"))
                        decision_record = await session.get(
                            TransitionDecisionRow, opening_decision.transition_decision_id
                        )
                        assert decision_record is not None
                        setattr(decision_record, field, corrupt_value)
                    with pytest.raises(HistoricalTransitionProvenanceError, match="admitted"):
                        await verify()
                finally:
                    await restore()

            try:
                async with sessions() as session, session.begin():
                    await session.execute(text("SET LOCAL session_replication_role = replica"))
                    decision_record = await session.get(
                        TransitionDecisionRow, opening_decision.transition_decision_id
                    )
                    assert decision_record is not None
                    decision_record.event_sequence = original_sequence + 1_000_000_000
                with pytest.raises(HistoricalTransitionProvenanceError, match="history"):
                    await verify()
            finally:
                await restore()

            surrounding = steps[1]
            surrounding_decision = decisions[1]
            async with sessions() as session:
                surrounding_request_row = await session.get(
                    TransitionRequestRow, surrounding.transition_request_id
                )
                surrounding_evaluation_row = await session.scalar(
                    select(TransitionEvaluationRow).where(
                        TransitionEvaluationRow.transition_request_id
                        == surrounding.transition_request_id
                    )
                )
                surrounding_decision_row = await session.get(
                    TransitionDecisionRow, surrounding_decision.transition_decision_id
                )
                assert surrounding_request_row is not None
                assert surrounding_evaluation_row is not None
                assert surrounding_decision_row is not None
                surrounding_original = {
                    "project_id": surrounding_request_row.project_id,
                    "task_contract_version": surrounding_request_row.task_contract_version,
                    "runtime_mode": surrounding_request_row.runtime_mode,
                    "request_fingerprint": surrounding_request_row.request_fingerprint,
                    "guards": list(surrounding_evaluation_row.guards),
                    "admitting_owner": surrounding_decision_row.admitting_owner,
                    "kernel_version": surrounding_decision_row.kernel_version,
                }

            async def restore_surrounding() -> None:
                async with sessions() as session, session.begin():
                    await session.execute(text("SET LOCAL session_replication_role = replica"))
                    request_record = await session.get(
                        TransitionRequestRow, surrounding.transition_request_id
                    )
                    evaluation_record = await session.scalar(
                        select(TransitionEvaluationRow).where(
                            TransitionEvaluationRow.transition_request_id
                            == surrounding.transition_request_id
                        )
                    )
                    decision_record = await session.get(
                        TransitionDecisionRow, surrounding_decision.transition_decision_id
                    )
                    assert request_record is not None
                    assert evaluation_record is not None
                    assert decision_record is not None
                    request_record.project_id = str(surrounding_original["project_id"])
                    request_record.task_contract_version = str(
                        surrounding_original["task_contract_version"]
                    )
                    request_record.runtime_mode = str(surrounding_original["runtime_mode"])
                    request_record.request_fingerprint = str(
                        surrounding_original["request_fingerprint"]
                    )
                    evaluation_record.guards = list(surrounding_original["guards"])
                    decision_record.admitting_owner = str(surrounding_original["admitting_owner"])
                    decision_record.kernel_version = str(surrounding_original["kernel_version"])

            async def corrupt_identity(field: str, value: str) -> None:
                async with sessions() as session, session.begin():
                    await session.execute(text("SET LOCAL session_replication_role = replica"))
                    request_record = await session.get(
                        TransitionRequestRow, surrounding.transition_request_id
                    )
                    evaluation_record = await session.scalar(
                        select(TransitionEvaluationRow).where(
                            TransitionEvaluationRow.transition_request_id
                            == surrounding.transition_request_id
                        )
                    )
                    assert request_record is not None
                    assert evaluation_record is not None
                    setattr(request_record, field, value)
                    reconstructed = _transition_request_from_row(request_record)
                    _, facts = _historical_evaluation_from_row(evaluation_record, reconstructed)
                    request_record.request_fingerprint = _request_fingerprint(reconstructed, facts)

            for field, corrupt_value in (
                ("task_contract_version", "foreign-task-version"),
                ("project_id", "foreign-project"),
                ("runtime_mode", RuntimeMode.PUBLIC_RECORDED_REPLAY.value),
            ):
                try:
                    await corrupt_identity(field, corrupt_value)
                    with pytest.raises(HistoricalTransitionProvenanceError, match="history"):
                        await verify()
                finally:
                    await restore_surrounding()

            try:
                async with sessions() as session, session.begin():
                    await session.execute(text("SET LOCAL session_replication_role = replica"))
                    request_record = await session.get(
                        TransitionRequestRow, surrounding.transition_request_id
                    )
                    assert request_record is not None
                    request_record.request_fingerprint = "1" * 64
                with pytest.raises(HistoricalTransitionProvenanceError, match="history"):
                    await verify()
            finally:
                await restore_surrounding()

            try:
                async with sessions() as session, session.begin():
                    await session.execute(text("SET LOCAL session_replication_role = replica"))
                    evaluation_record = await session.scalar(
                        select(TransitionEvaluationRow).where(
                            TransitionEvaluationRow.transition_request_id
                            == surrounding.transition_request_id
                        )
                    )
                    assert evaluation_record is not None
                    guards = [dict(item) for item in evaluation_record.guards]
                    non_current_index = next(
                        index
                        for index, item in enumerate(guards)
                        if item["guard_id"] != GuardId.G_CURRENT.value
                    )
                    guards[non_current_index]["semantic_owner"] = (
                        GuardSemanticOwner.P1_7_HUMAN.value
                    )
                    evaluation_record.guards = guards
                with pytest.raises(HistoricalTransitionProvenanceError, match="history"):
                    await verify()
            finally:
                await restore_surrounding()

            for field, corrupt_value in (
                ("admitting_owner", "FOREIGN_TRANSITION_OWNER"),
                ("kernel_version", "FOREIGN_KERNEL"),
            ):
                try:
                    async with sessions() as session, session.begin():
                        await session.execute(text("SET LOCAL session_replication_role = replica"))
                        decision_record = await session.get(
                            TransitionDecisionRow,
                            surrounding_decision.transition_decision_id,
                        )
                        assert decision_record is not None
                        setattr(decision_record, field, corrupt_value)
                    with pytest.raises(HistoricalTransitionProvenanceError, match="history"):
                        await verify()
                finally:
                    await restore_surrounding()
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_representative_blocked_rework_human_and_outcome_paths(database_url: str) -> None:
    async def scenario() -> None:
        kernel, _, authority, engine = build_kernel(database_url)
        try:
            blocked_run = f"run-blocked-{uuid4()}"
            await admit(
                kernel,
                authority,
                request(
                    run_id=blocked_run,
                    source=None,
                    version=0,
                    target=WorkflowState.READY,
                ),
            )
            await admit(
                kernel,
                authority,
                request(
                    run_id=blocked_run,
                    source=WorkflowState.READY,
                    version=1,
                    target=WorkflowState.RUNNING,
                ),
            )
            await admit(
                kernel,
                authority,
                request(
                    run_id=blocked_run,
                    source=WorkflowState.RUNNING,
                    version=2,
                    target=WorkflowState.BLOCKED,
                ),
            )
            sessions = create_session_factory(engine)
            async with sessions() as session:
                blocker = await session.scalar(
                    select(P1_4BlockerProvenanceRow).where(
                        P1_4BlockerProvenanceRow.work_run_id == blocked_run,
                        P1_4BlockerProvenanceRow.blocked_epoch == 3,
                    )
                )
            assert blocker is not None
            await admit(
                kernel,
                authority,
                request(
                    run_id=blocked_run,
                    source=WorkflowState.BLOCKED,
                    version=3,
                    target=WorkflowState.READY,
                    blocker_resolution_claim=P1_4BlockerResolutionClaimV1(
                        blocker.blocker_ref,
                        blocker.blocker_fingerprint,
                        "resolution-source:v1:test",
                        "d" * 64,
                        "resolution-authority:v1:test",
                        "b" * 64,
                    ),
                ),
            )

            human_run = f"run-human-{uuid4()}"
            await admit(
                kernel,
                authority,
                request(
                    run_id=human_run,
                    source=None,
                    version=0,
                    target=WorkflowState.READY,
                ),
            )
            await admit(
                kernel,
                authority,
                request(
                    run_id=human_run,
                    source=WorkflowState.READY,
                    version=1,
                    target=WorkflowState.RUNNING,
                ),
            )
            await admit(
                kernel,
                authority,
                request(
                    run_id=human_run,
                    source=WorkflowState.RUNNING,
                    version=2,
                    target=WorkflowState.ADMISSION_PENDING,
                ),
            )
            await admit(
                kernel,
                authority,
                request(
                    run_id=human_run,
                    source=WorkflowState.ADMISSION_PENDING,
                    version=3,
                    target=WorkflowState.HUMAN_REQUIRED,
                ),
            )
            accepted_request = request(
                run_id=human_run,
                source=WorkflowState.HUMAN_REQUIRED,
                version=4,
                target=WorkflowState.ACCEPTED,
                evidence_refs=("admitted-evidence:synthetic",),
                human_result_refs=("human-result:approve",),
                judgment_refs=("judgment:accepted",),
            )
            accepted = await admit(kernel, authority, accepted_request)
            assert accepted.resulting_state is WorkflowState.ACCEPTED
            assert accepted.resulting_state_version == 5

            rework_run = f"run-rework-{uuid4()}"
            await admit(
                kernel,
                authority,
                request(
                    run_id=rework_run,
                    source=None,
                    version=0,
                    target=WorkflowState.READY,
                ),
            )
            await admit(
                kernel,
                authority,
                request(
                    run_id=rework_run,
                    source=WorkflowState.READY,
                    version=1,
                    target=WorkflowState.RUNNING,
                ),
            )
            rework_request = request(
                run_id=rework_run,
                source=WorkflowState.RUNNING,
                version=2,
                target=WorkflowState.REWORK_REQUIRED,
                judgment_refs=("judgment:hold-rework",),
            )
            rework = await admit(kernel, authority, rework_request)
            assert rework.resulting_state is WorkflowState.REWORK_REQUIRED
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize("failure_point", tuple(FailurePoint))
def test_blocker_provenance_projection_and_workrun_rollback_together(
    database_url: str, failure_point: FailurePoint
) -> None:
    async def scenario() -> None:
        run_id = f"run-blocker-rollback-{failure_point.value}-{uuid4()}"
        kernel, _, authority, engine = build_kernel(database_url)
        sessions = create_session_factory(engine)
        try:
            await admit(
                kernel,
                authority,
                request(run_id=run_id, source=None, version=0, target=WorkflowState.READY),
            )
            await admit(
                kernel,
                authority,
                request(
                    run_id=run_id,
                    source=WorkflowState.READY,
                    version=1,
                    target=WorkflowState.RUNNING,
                ),
            )
            block = request(
                run_id=run_id,
                source=WorkflowState.RUNNING,
                version=2,
                target=WorkflowState.BLOCKED,
            )

            def fail(point: FailurePoint) -> None:
                if point is failure_point:
                    raise RuntimeError("injected blocker transaction cut")

            with pytest.raises(RuntimeError, match="injected blocker"):
                await kernel.request_transition(
                    block,
                    facts(authority, block),
                    failure_injector=fail,
                    transaction_participant=None,
                )
            async with sessions() as session:
                blocker_count = int(
                    await session.scalar(
                        select(func.count())
                        .select_from(P1_4BlockerProvenanceRow)
                        .where(P1_4BlockerProvenanceRow.work_run_id == run_id)
                    )
                    or 0
                )
                request_row = await session.get(
                    TransitionRequestRow, block.transition_request_id
                )
            projection = await kernel.load(run_id)
            assert blocker_count == 0
            assert request_row is None
            assert projection is not None
            assert projection.state is WorkflowState.RUNNING
            assert projection.state_version == 2
            admitted = await admit(kernel, authority, block)
            assert admitted.resulting_state is WorkflowState.BLOCKED
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_same_version_concurrency_admits_one_and_denies_one_stale(database_url: str) -> None:
    async def scenario() -> None:
        kernel, repository, authority, engine = build_kernel(database_url)
        try:
            for _ in range(3):
                run_id = f"run-concurrent-{uuid4()}"
                await admit(
                    kernel,
                    authority,
                    request(
                        run_id=run_id,
                        source=None,
                        version=0,
                        target=WorkflowState.READY,
                    ),
                )
                first = request(
                    run_id=run_id,
                    source=WorkflowState.READY,
                    version=1,
                    target=WorkflowState.RUNNING,
                )
                second = request(
                    run_id=run_id,
                    source=WorkflowState.READY,
                    version=1,
                    target=WorkflowState.RUNNING,
                )
                decisions = await asyncio.gather(
                    kernel.request_transition(first, facts(authority, first)),
                    kernel.request_transition(second, facts(authority, second)),
                )
                assert [item.outcome for item in decisions].count(DecisionOutcome.ADMITTED) == 1
                assert [item.reason for item in decisions].count(DecisionReason.STALE_REQUEST) == 1
                projection = await kernel.load(run_id)
                assert projection is not None
                assert projection.state is WorkflowState.RUNNING
                assert projection.state_version == 2
                history = await repository.history(run_id)
                assert len(history) == 3
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_duplicate_request_id_is_one_decision_one_mutation(database_url: str) -> None:
    async def scenario() -> None:
        run_id = f"run-duplicate-{uuid4()}"
        kernel, repository, authority, engine = build_kernel(database_url)
        try:
            await admit(
                kernel,
                authority,
                request(
                    run_id=run_id,
                    source=None,
                    version=0,
                    target=WorkflowState.READY,
                ),
            )
            duplicate = request(
                run_id=run_id,
                source=WorkflowState.READY,
                version=1,
                target=WorkflowState.RUNNING,
                request_id=f"request-duplicate-{uuid4()}",
            )
            trusted = facts(authority, duplicate)
            first, second = await asyncio.gather(
                kernel.request_transition(duplicate, trusted),
                kernel.request_transition(duplicate, trusted),
            )
            assert first.transition_decision_id == second.transition_decision_id
            assert first.outcome is DecisionOutcome.ADMITTED
            projection = await kernel.load(run_id)
            assert projection is not None and projection.state_version == 2
            history = await repository.history(run_id)
            assert len(history) == 2
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_atomic_failure_rolls_back_provenance_and_projection(database_url: str) -> None:
    async def scenario() -> None:
        kernel, repository, authority, engine = build_kernel(database_url)
        try:
            for selected_point in FailurePoint:
                run_id = f"run-atomic-{uuid4()}"
                request_id = f"request-atomic-{uuid4()}"
                transition_request = request(
                    run_id=run_id,
                    source=None,
                    version=0,
                    target=WorkflowState.READY,
                    request_id=request_id,
                )

                def fail(point: FailurePoint, expected: FailurePoint = selected_point) -> None:
                    if point is expected:
                        raise RuntimeError("controlled atomicity failure")

                with pytest.raises(RuntimeError, match="controlled atomicity failure"):
                    await kernel.request_transition(
                        transition_request,
                        facts(authority, transition_request),
                        failure_injector=fail,
                    )
                assert await kernel.load(run_id) is None
                assert await repository.get_decision(request_id) is None
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_denied_provenance_is_append_only_and_projection_unchanged(database_url: str) -> None:
    async def scenario() -> None:
        run_id = f"run-denied-{uuid4()}"
        kernel, repository, authority, engine = build_kernel(database_url)
        try:
            await admit(
                kernel,
                authority,
                request(
                    run_id=run_id,
                    source=None,
                    version=0,
                    target=WorkflowState.READY,
                ),
            )
            invalid = request(
                run_id=run_id,
                source=WorkflowState.READY,
                version=1,
                target=WorkflowState.ACCEPTED,
            )
            invalid_decision = await kernel.request_transition(invalid, ())
            assert invalid_decision.reason is DecisionReason.INVALID_TRANSITION
            missing = request(
                run_id=run_id,
                source=WorkflowState.READY,
                version=1,
                target=WorkflowState.RUNNING,
            )
            missing_decision = await kernel.request_transition(missing, ())
            assert missing_decision.reason is DecisionReason.MISSING_GUARD
            projection = await kernel.load(run_id)
            assert projection is not None
            assert projection.state is WorkflowState.READY
            assert projection.state_version == 1
            history = await repository.history(run_id)
            assert len(history) == 3
            assert [item.outcome for item in history].count(DecisionOutcome.DENIED) == 2

            async with engine.begin() as connection:
                with pytest.raises(Exception, match="append-only"):
                    await connection.execute(
                        text(
                            "UPDATE transition_decisions SET reason = 'ADMITTED' "
                            "WHERE transition_decision_id = :decision_id"
                        ),
                        {"decision_id": invalid_decision.transition_decision_id},
                    )
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_projection_event_mismatch_gates_fresh_mutation_without_provenance(
    database_url: str,
) -> None:
    async def scenario() -> None:
        run_id = f"run-conflict-{uuid4()}"
        kernel, _, authority, engine = build_kernel(database_url)
        try:
            await admit(
                kernel,
                authority,
                request(
                    run_id=run_id,
                    source=None,
                    version=0,
                    target=WorkflowState.READY,
                ),
            )
            async with engine.begin() as connection:
                await connection.execute(
                    text(
                        "UPDATE work_runs SET state_version = state_version + 7 "
                        "WHERE work_run_id = :run_id"
                    ),
                    {"run_id": run_id},
                )
            before_counts = await provenance_counts(engine, run_id)
            fresh = request(
                run_id=run_id,
                source=WorkflowState.READY,
                version=8,
                target=WorkflowState.RUNNING,
            )
            with pytest.raises(AuthorityConflictError, match="projection"):
                await kernel.request_transition(fresh, facts(authority, fresh))
            assert await provenance_counts(engine, run_id) == before_counts
            projection = await kernel.load(run_id)
            assert projection is not None and projection.state_version == 8
            assert projection.state is WorkflowState.READY
            with pytest.raises(AuthorityConflictError, match="projection"):
                await kernel.verify_consistency(run_id)
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_missing_projection_with_history_gates_fresh_mutation_without_recreation(
    database_url: str,
) -> None:
    async def scenario() -> None:
        run_id = f"run-missing-projection-{uuid4()}"
        kernel, _, authority, engine = build_kernel(database_url)
        try:
            await admit(
                kernel,
                authority,
                request(
                    run_id=run_id,
                    source=None,
                    version=0,
                    target=WorkflowState.READY,
                ),
            )
            async with engine.begin() as connection:
                await connection.execute(
                    text("DELETE FROM work_runs WHERE work_run_id = :run_id"),
                    {"run_id": run_id},
                )
            before_counts = await provenance_counts(engine, run_id)
            fresh = request(
                run_id=run_id,
                source=None,
                version=0,
                target=WorkflowState.READY,
            )
            with pytest.raises(AuthorityConflictError, match="projection is missing"):
                await kernel.request_transition(fresh, facts(authority, fresh))
            assert await provenance_counts(engine, run_id) == before_counts
            assert await kernel.load(run_id) is None
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_denied_precreation_missing_guard_allows_fresh_retry_to_ready(
    database_url: str,
) -> None:
    async def scenario() -> None:
        run_id = f"run-denied-retry-{uuid4()}"
        kernel, repository, authority, engine = build_kernel(database_url)
        try:
            denied_request = request(
                run_id=run_id,
                source=None,
                version=0,
                target=WorkflowState.READY,
            )
            denied = await kernel.request_transition(denied_request, ())
            assert denied.outcome is DecisionOutcome.DENIED
            assert denied.reason is DecisionReason.MISSING_GUARD
            assert denied.resulting_state is None
            assert denied.resulting_state_version == 0
            assert await kernel.load(run_id) is None
            assert await provenance_counts(engine, run_id) == (1, 1, 1)

            fresh = request(
                run_id=run_id,
                source=None,
                version=0,
                target=WorkflowState.READY,
            )
            admitted = await admit(kernel, authority, fresh)
            assert admitted.resulting_state is WorkflowState.READY
            assert admitted.resulting_state_version == 1
            projection = await kernel.load(run_id)
            assert projection is not None
            assert projection.state is WorkflowState.READY
            assert projection.state_version == 1
            assert await kernel.verify_consistency(run_id) == projection
            history = await repository.history(run_id)
            assert [item.outcome for item in history] == [
                DecisionOutcome.DENIED,
                DecisionOutcome.ADMITTED,
            ]
            assert await provenance_counts(engine, run_id) == (2, 2, 2)
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_denied_precreation_invalid_transition_allows_fresh_retry(
    database_url: str,
) -> None:
    async def scenario() -> None:
        run_id = f"run-invalid-retry-{uuid4()}"
        kernel, repository, authority, engine = build_kernel(database_url)
        try:
            invalid = request(
                run_id=run_id,
                source=None,
                version=0,
                target=WorkflowState.RUNNING,
            )
            denied = await kernel.request_transition(invalid, ())
            assert denied.reason is DecisionReason.INVALID_TRANSITION
            assert await kernel.load(run_id) is None

            fresh = request(
                run_id=run_id,
                source=None,
                version=0,
                target=WorkflowState.READY,
            )
            admitted = await admit(kernel, authority, fresh)
            assert admitted.resulting_state_version == 1
            assert [item.outcome for item in await repository.history(run_id)] == [
                DecisionOutcome.DENIED,
                DecisionOutcome.ADMITTED,
            ]
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_multiple_denied_precreation_attempts_allow_fresh_retry(
    database_url: str,
) -> None:
    async def scenario() -> None:
        run_id = f"run-multiple-denied-retry-{uuid4()}"
        kernel, repository, authority, engine = build_kernel(database_url)
        try:
            missing = request(
                run_id=run_id,
                source=None,
                version=0,
                target=WorkflowState.READY,
            )
            invalid = request(
                run_id=run_id,
                source=None,
                version=0,
                target=WorkflowState.RUNNING,
            )
            assert (
                await kernel.request_transition(missing, ())
            ).reason is DecisionReason.MISSING_GUARD
            assert (
                await kernel.request_transition(invalid, ())
            ).reason is DecisionReason.INVALID_TRANSITION
            assert await kernel.load(run_id) is None

            fresh = request(
                run_id=run_id,
                source=None,
                version=0,
                target=WorkflowState.READY,
            )
            admitted = await admit(kernel, authority, fresh)
            assert admitted.resulting_state_version == 1
            assert [item.outcome for item in await repository.history(run_id)] == [
                DecisionOutcome.DENIED,
                DecisionOutcome.DENIED,
                DecisionOutcome.ADMITTED,
            ]
            assert await provenance_counts(engine, run_id) == (3, 3, 3)
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.postgres
@pytest.mark.parametrize(
    ("identity_field", "replacement"),
    (
        ("project_id", "project-other"),
        ("task_contract_id", "task-contract-other"),
        ("task_contract_version", "v2"),
        ("runtime_mode", RuntimeMode.PUBLIC_RECORDED_REPLAY),
    ),
)
def test_denied_precreation_identity_mismatch_remains_authority_conflict(
    database_url: str,
    identity_field: str,
    replacement: str | RuntimeMode,
) -> None:
    async def scenario() -> None:
        run_id = f"run-identity-conflict-{uuid4()}"
        kernel, _, authority, engine = build_kernel(database_url)
        try:
            denied_request = request(
                run_id=run_id,
                source=None,
                version=0,
                target=WorkflowState.READY,
            )
            denied = await kernel.request_transition(denied_request, ())
            assert denied.reason is DecisionReason.MISSING_GUARD
            before_counts = await provenance_counts(engine, run_id)

            fresh = request(
                run_id=run_id,
                source=None,
                version=0,
                target=WorkflowState.READY,
                project_id=(
                    replacement
                    if identity_field == "project_id" and isinstance(replacement, str)
                    else "project-p1-4"
                ),
                task_contract_id=(
                    replacement
                    if identity_field == "task_contract_id" and isinstance(replacement, str)
                    else "task-contract-p1-4"
                ),
                task_contract_version=(
                    replacement
                    if identity_field == "task_contract_version" and isinstance(replacement, str)
                    else "v1"
                ),
                runtime_mode=(
                    replacement
                    if identity_field == "runtime_mode" and isinstance(replacement, RuntimeMode)
                    else RuntimeMode.OWNER_SELF_DOGFOOD
                ),
            )
            with pytest.raises(AuthorityConflictError, match="different run identity"):
                await kernel.request_transition(fresh, facts(authority, fresh))
            assert await provenance_counts(engine, run_id) == before_counts
            assert await kernel.load(run_id) is None
        finally:
            await engine.dispose()

    run(scenario())


@pytest.mark.postgres
def test_partial_precreation_provenance_remains_authority_conflict(
    database_url: str,
) -> None:
    async def scenario() -> None:
        run_id = f"run-partial-provenance-{uuid4()}"
        kernel, _, authority, engine = build_kernel(database_url)
        try:
            partial = request(
                run_id=run_id,
                source=None,
                version=0,
                target=WorkflowState.READY,
            )
            async with engine.begin() as connection:
                await connection.execute(
                    text(
                        "INSERT INTO transition_requests ("
                        "transition_request_id, request_fingerprint, project_id, "
                        "task_contract_id, task_contract_version, work_run_id, "
                        "observed_state, observed_state_version, target_state, "
                        "requester_identity, requester_type, runtime_mode, evidence_refs, "
                        "human_result_refs, judgment_refs, parent_request_id, created_at"
                        ") VALUES ("
                        ":request_id, :fingerprint, :project_id, :task_contract_id, "
                        ":task_contract_version, :run_id, NULL, 0, :target_state, "
                        ":requester_identity, :requester_type, :runtime_mode, "
                        "'[]'::jsonb, '[]'::jsonb, '[]'::jsonb, NULL, :created_at"
                        ")"
                    ),
                    {
                        "request_id": partial.transition_request_id,
                        "fingerprint": "0" * 64,
                        "project_id": partial.project_id,
                        "task_contract_id": partial.task_contract_id,
                        "task_contract_version": partial.task_contract_version,
                        "run_id": partial.work_run_id,
                        "target_state": partial.target_state.value,
                        "requester_identity": partial.requester_identity,
                        "requester_type": partial.requester_type.value,
                        "runtime_mode": partial.runtime_mode.value,
                        "created_at": partial.created_at,
                    },
                )
            before_counts = await provenance_counts(engine, run_id)
            assert before_counts == (1, 0, 0)
            fresh = request(
                run_id=run_id,
                source=None,
                version=0,
                target=WorkflowState.READY,
            )
            with pytest.raises(AuthorityConflictError, match="partial or orphaned"):
                await kernel.request_transition(fresh, facts(authority, fresh))
            assert await provenance_counts(engine, run_id) == before_counts
            assert await kernel.load(run_id) is None
        finally:
            await engine.dispose()

    run(scenario())
