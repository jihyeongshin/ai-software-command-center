"""Owner API integration in a disposable test database, not an actual golden run."""

import asyncio
import os
from dataclasses import replace
from datetime import timedelta
from uuid import uuid4

import pytest
from sqlalchemy import event, func, select

from aiscc.next_action.genesis import GenesisAuthorityRepository
from aiscc.persistence.models import AdmittedCycleRow, ProjectMemoryEntryRow, WorkRunRow
from aiscc.task_authority.authority import _bind_repository_once
from aiscc.task_authority.contracts import (
    TaskContractBodyV1,
    TaskContractError,
    candidate_fingerprint,
    plain,
)
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository
from tests.integration.evidence import test_postgres_evidence_admission as e
from tests.integration.memory import test_postgres_project_memory_next_action as m
from tests.integration.next_action.test_genesis_bootstrap import (
    current,
    genesis_fixture,
)
from tests.integration.task_authority.test_task_contract_durability import verify
from tests.unit.next_action.test_genesis_bootstrap import NOW
from tests.unit.task_authority.test_genesis_issuance import genesis_body


@pytest.fixture
def database_url():
    return os.environ["AISCC_TEST_DATABASE_URL"]


async def contract_fixture(database_url, tmp_path, *, durable=False, existing=None):
    f = dict(existing) if existing else await genesis_fixture(database_url, tmp_path)
    if existing:
        f["repo"] = PostgresExternalTaskAuthorityRepository(f["sessions"])
        f["writer"] = _bind_repository_once(f["repo"])
    cid = "contract-" + uuid4().hex
    cp = e.checkpoint(
        task_id=cid,
        set_id=cid + "-set",
        checkpoint_id="completion",
        source=e.WorkflowState.ADMISSION_PENDING,
    )
    req = e.requirement(
        task_id=cid,
        set_id=cid + "-set",
        requirement_id="proof",
        profile=e.EvidenceRequirementProfile.EXECUTOR_REQUIRED
        if durable
        else e.EvidenceRequirementProfile.NOT_REQUIRED,
        checkpoints=(cp.ref.serialized(),),
        issuer_types=frozenset({e.EvidenceIssuerType.SYSTEM_STATIC_PROOF})
        if durable
        else frozenset(),
        issuer_ids=frozenset({"STATIC_ISSUER"}) if durable else frozenset(),
        content_kinds=frozenset({e.EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY})
        if durable
        else frozenset(),
    )
    if durable:
        req = replace(
            req,
            ref=e.EvidenceRequirementRef(cid + ":proof", "v2"),
            fingerprint_schema=e.RequirementFingerprintSchema.V2_DURABLE_CONTENT,
            durable_content_requirement=e.DurableContentRequirement.REQUIRED,
            durable_content_policy_ref="P1_6_DURABLE_CONTENT_POLICY@v1",
            durable_content_policy_fingerprint=e.canonical_hash(
                {
                    "policy": "P1_6_DURABLE_CONTENT_POLICY_V1",
                    "kind": e.EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY.value,
                    "schema": ["AISCC-PROOF", "v1"],
                    "limit": 65536,
                }
            ),
        )
    owner, rs, reqs, cps = e.seal_snapshot(
        task_id=cid, set_id=cid + "-set", requirements=(req,), checkpoints=(cp,)
    )
    content_owner = e.P1_6DurableContentAuthority()
    access_owner = e.P1_6HistoricalContentAccessAuthority()
    evidence = e.PostgresEvidenceRepository(
        f["sessions"],
        durable_content_authority=content_owner,
        historical_content_access_authority=access_owner,
    )
    await evidence.register_authority(
        requirement_set=rs, requirements=reqs, checkpoints=cps, authority=owner
    )
    binding = {
        k: getattr(f["context"], k) for k in ("repository_id", "repository_root", "base_commit")
    }
    f["writer"].configure_task_contracts(
        project_id=f["project_id"],
        repository_binding=binding,
        next_action_repository=f["actions"],
        evidence_repository=evidence,
    )
    await f["writer"].certify_snapshot(snapshot_id="empty-prefix-" + cid, issued_at=NOW)
    value = genesis_body()
    value.update(
        project_id=f["project_id"], contract_id=cid, task_id=cid, repository_binding=binding
    )
    value["evidence_binding"] = dict(
        requirement_set_ref=rs.requirement_set_id + "@v1",
        requirement_set_fingerprint=rs.fingerprint,
        checkpoints=[dict(ref=cps[0].ref.serialized(), fingerprint=cps[0].fingerprint)],
    )
    policy = value["judgment_binding"]["policies"][0]
    policy.update(
        policy_id="accept-" + cid,
        evidence_checkpoint_ref=cps[0].ref.serialized(),
        evidence_requirement_set_ref=rs.requirement_set_id + "@v1",
    )
    s, c = f["selected"], f["candidate"]
    value["source_next_action"] = dict(
        selection_id=s.selection_id,
        selection_version=s.selection_version,
        selection_fingerprint=s.fingerprint,
        project_revision=s.project_revision,
        action_ref=s.action_ref.serialized,
        descriptor_fingerprint=s.descriptor_fingerprint,
        issuance_candidate_id=c.candidate_id,
        issuance_candidate_fingerprint=candidate_fingerprint(c),
        external_context=None,
        genesis_authority=dict(
            authority_ref=f["authority"].authority_ref,
            fingerprint=f["authority"].fingerprint,
            phase_id=f["context"].phase_id,
        ),
    )
    f.update(
        body=TaskContractBodyV1(value),
        evidence=evidence,
        repository_binding=binding,
        evidence_values=(owner, rs, reqs, cps),
        content_owner=content_owner,
        access_owner=access_owner,
    )
    return f


@pytest.mark.postgres
def test_genesis_contract_retry_restart_revoke_no_run_locks(database_url, tmp_path):
    async def scenario():
        f = await contract_fixture(database_url, tmp_path)
        locks = []

        def capture(conn, cursor, statement, parameters, context, many):
            if "pg_advisory" in statement:
                locks.extend(str(v) for v in parameters)

        event.listen(f["engine"].sync_engine, "before_cursor_execute", capture)
        try:
            receipt = await f["writer"].issue_task_contract(
                body=f["body"], expected_current_body_sha256=None, issued_at=NOW
            )
            assert receipt == await f["writer"].issue_task_contract(
                body=f["body"], expected_current_body_sha256=None, issued_at=NOW
            )
            assert (await verify(f, receipt)).current
            restarted = PostgresExternalTaskAuthorityRepository(f["sessions"])
            writer = _bind_repository_once(restarted)
            writer.configure_task_contracts(
                project_id=f["project_id"],
                repository_binding=f["repository_binding"],
                next_action_repository=f["actions"],
                evidence_repository=f["evidence"],
            )
            assert (
                await restarted.get_task_contract(
                    f["project_id"], f["body"].value["contract_id"], 1
                )
                == receipt
            )
            assert (await verify(f, receipt, restarted)).current
            for changes in [dict(goal="changed")]:
                with pytest.raises(TaskContractError):
                    await writer.issue_task_contract(
                        body=TaskContractBodyV1(plain(f["body"].value) | changes),
                        expected_current_body_sha256=None,
                        issued_at=NOW,
                    )
            other = await contract_fixture(database_url, tmp_path, existing=f)
            with pytest.raises(TaskContractError, match="different TaskContract family/body"):
                await other["writer"].issue_task_contract(
                    body=other["body"], expected_current_body_sha256=None, issued_at=NOW
                )
            for key, value in [
                ("phase_id", "P3"),
                ("fingerprint", "0" * 64),
                ("authority_ref", "self-dogfood-genesis:v1:missing"),
            ]:
                altered = plain(f["body"].value)
                altered["source_next_action"]["genesis_authority"][key] = value
                with pytest.raises(TaskContractError):
                    await writer.issue_task_contract(
                        body=TaskContractBodyV1(altered),
                        expected_current_body_sha256=None,
                        issued_at=NOW,
                    )
            async with f["sessions"]() as session:
                for model in (WorkRunRow, AdmittedCycleRow, ProjectMemoryEntryRow):
                    assert (
                        await session.scalar(
                            select(func.count())
                            .select_from(model)
                            .where(model.project_id == f["project_id"])
                        )
                        == 0
                    )
            await writer.revoke_task_contract(
                project_id=f["project_id"],
                contract_id=f["body"].value["contract_id"],
                expected_version=1,
                expected_body_sha256=f["body"].body_sha256,
                effective_at=NOW,
            )
            with pytest.raises(TaskContractError):
                await writer.issue_task_contract(
                    body=f["body"], expected_current_body_sha256=None, issued_at=NOW
                )
            assert not (await verify(f, receipt, current=False)).current
            assert any("task-contract-family:" in k for k in locks)
            assert any("p1-8-memory-project:" in k for k in locks)
            assert not any(k.startswith("run:") for k in locks)
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
def test_competing_genesis_families_admit_exactly_one(database_url, tmp_path):
    async def scenario():
        first = await contract_fixture(database_url, tmp_path)
        try:
            second = await contract_fixture(database_url, tmp_path, existing=first)
            results = await asyncio.gather(
                *(
                    f["writer"].issue_task_contract(
                        body=f["body"], expected_current_body_sha256=None, issued_at=NOW
                    )
                    for f in (first, second)
                ),
                return_exceptions=True,
            )
            assert sum(isinstance(x, TaskContractError) for x in results) == 1
            winner = next(x for x in results if not isinstance(x, Exception))
            assert winner.body.body_sha256 in {
                first["body"].body_sha256,
                second["body"].body_sha256,
            }
        finally:
            await first["engine"].dispose()

    asyncio.run(scenario())


@pytest.mark.postgres
def test_first_owner_admitted_cycle_permanently_ends_genesis_and_enables_cycle_source(
    database_url, tmp_path
):
    async def scenario():
        f = await contract_fixture(database_url, tmp_path, durable=True)
        try:
            receipt = await f["writer"].issue_task_contract(
                body=f["body"], expected_current_body_sha256=None, issued_at=NOW
            )
            cid, project, sessions = f["body"].value["contract_id"], f["project_id"], f["sessions"]
            run_id = "test-owner-run-" + uuid4().hex
            authorities = e.WorkflowAuthorities()
            kernel = e.WorkflowKernel(
                e.PostgresTransitionRepository(
                    sessions, e.TransitionEvaluator(authorities.system, authorities.future)
                )
            )
            # Test-only P1-4/P1-5 guard capabilities; all WorkRun rows are admitted by
            # the real transition repository. This is not external-IDE execution proof.
            for source, version, target in [
                (None, 0, e.WorkflowState.READY),
                (e.WorkflowState.READY, 1, e.WorkflowState.RUNNING),
                (e.WorkflowState.RUNNING, 2, e.WorkflowState.ADMISSION_PENDING),
            ]:
                request = replace(
                    e.transition_request(
                        run_id=run_id, task_id=cid, source=source, version=version, target=target
                    ),
                    project_id=project,
                )
                decision = await kernel.request_transition(request, authorities.facts(request))
                assert decision.outcome is e.DecisionOutcome.ADMITTED
            assert await current(f) == f["authority"]
            context, intro = await f["writer"].issue_next_action_context(
                context_ref_id="context-" + cid,
                context_logical_local_id="planning-" + cid,
                project_id=project,
                task_contract_id=cid,
                task_contract_version="v1",
                context_slot_id="primary",
                priority_class=m.NextActionPriorityClass.ACCEPTED_CORE_CRITICAL_PATH,
                critical_path_ordinal=1,
                event_id="context-issued-" + cid,
                issued_at=NOW,
            )
            snapshot = await f["writer"].certify_snapshot(
                snapshot_id="context-snapshot-" + cid, issued_at=NOW
            )
            normalized = dict(
                context_ref=context.context_ref,
                context_fingerprint=context.fingerprint,
                context_logical_id=context.context_logical_id,
                project_id=project,
                task_contract_id=cid,
                task_contract_version="v1",
                context_slot_id="primary",
                priority_class=context.priority_class.value,
                critical_path_ordinal=1,
            )
            raw_context = dict(
                **normalized,
                result_schema_id="P1_8_NEXT_ACTION_CONTEXT_RESULT_V1",
                result_schema_version="v1",
                context_introduction_event_ref=intro.event_ref,
                context_introduction_event_fingerprint=intro.event_fingerprint,
                context_authority_event_high_watermark=snapshot.owner_event_high_watermark,
            )
            _, rs, reqs, cps = f["evidence_values"]
            cp, req = cps[0], reqs[0]
            issuer = e.TokenEvidenceIssuer(
                e.EvidenceIssuerType.SYSTEM_STATIC_PROOF, "STATIC_ISSUER", "v1"
            )
            placeholder = e.EvidenceContentRef(
                e.EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY,
                "durable-owner",
                "v1",
                "object-" + cid,
                "v1",
                "PENDING_P1_6_CANONICALIZATION",
                "AISCC-PROOF",
                "v1",
                1,
                "0" * 64,
                e.EvidenceSensitivity.INTERNAL,
                "PENDING_P1_6_RETENTION",
                "PRIVATE_AUTHORITY_ONLY",
            )
            skeleton = e.EvidenceCandidate(
                "candidate-" + cid,
                "v1",
                "",
                e.EvidenceOwner(
                    e.EvidenceIssuerType.SYSTEM_STATIC_PROOF,
                    "STATIC_ISSUER",
                    "v1",
                    "STATIC_ISSUER@v1",
                ),
                run_id,
                None,
                None,
                cid,
                "v1",
                cp.ref,
                e.WorkflowState.ADMISSION_PENDING,
                3,
                "aiscc-source",
                "repository",
                "repo@commit",
                "AISCC_PROOF",
                "v1",
                placeholder,
                NOW,
                NOW,
                frozenset({"result"}),
                "system-proof-attestation",
            )
            prepared = f["content_owner"].prepare_structured(
                owner_id="durable-owner",
                owner_version="v1",
                source_owner_authority_ref=skeleton.issuer.authority_ref,
                source_owner_authority_fingerprint=e.source_owner_authority_fingerprint(skeleton),
                object_id="object-" + cid,
                object_version="v1",
                value={"next_action_context": raw_context},
                kind=e.EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY,
                schema_id="AISCC-PROOF",
                schema_version="v1",
                sensitivity=e.EvidenceSensitivity.INTERNAL,
                created_at=NOW,
            )
            candidate = issuer.issue(replace(skeleton, content_ref=prepared.content_ref))
            service = e.EvidenceAdmissionService(
                f["evidence"],
                e.EvidenceAdmissionEvaluator(
                    e.EvidenceIssuerRegistry((issuer,)), e.EvidenceContentRegistry(())
                ),
                durable_content_authority=f["content_owner"],
            )
            evidence_request = e.admission_request(
                request_id="evidence-request-" + cid,
                candidate=candidate,
                requirement=req,
                requirement_set=rs,
                checkpoint=cp,
                run_id=run_id,
                state_version=3,
            )
            evidence_decision, admitted = await service.submit_durable(
                evidence_request, candidate, prepared, now=NOW
            )
            assert evidence_decision.outcome is e.EvidenceAdmissionOutcome.ADMITTED, (
                evidence_decision
            )
            evidence_ref = e.AdmittedEvidenceRef(
                admitted.admitted_evidence_id, e.EVIDENCE_AUTHORITY_VERSION
            ).serialized()
            evaluation, attestation = await e.EvidenceSetEvaluator(f["evidence"]).evaluate(
                work_run_id=run_id,
                checkpoint_ref=cp.ref,
                source_state=e.WorkflowState.ADMISSION_PENDING,
                state_version=3,
                now=NOW,
            )
            assert evaluation.outcome is e.EvidenceSetOutcome.SATISFIED and attestation is not None
            accept = replace(
                e.transition_request(
                    run_id=run_id,
                    task_id=cid,
                    source=e.WorkflowState.ADMISSION_PENDING,
                    version=3,
                    target=e.WorkflowState.ACCEPTED,
                    evidence_refs=(attestation.serialized_ref,),
                ),
                project_id=project,
            )
            policies = e.JudgmentPolicyAuthority(sessions, clock=lambda: NOW)
            judgments = e.PostgresJudgmentAuthority(
                sessions, f["evidence"], policies, clock=lambda: NOW
            )
            policy = await policies.register(
                policy_id="accept-" + cid,
                policy_version="v1",
                task_contract_id=cid,
                task_contract_version="v1",
                source_state=e.WorkflowState.ADMISSION_PENDING,
                target_state=e.WorkflowState.ACCEPTED,
                owner_policy=e.JudgmentOwnerPolicy.SYSTEM_DETERMINISTIC,
                requires_human_result=False,
                requires_post_human_evidence=True,
                deterministic_kind=e.JudgmentKind.ACCEPTED,
            )
            judgment = await judgments.issue(
                judgment_id="judgment-" + cid,
                judgment_version="v1",
                request=accept,
                policy=policy,
                human_result_ref=None,
                evidence_attestation_ref=attestation.serialized_ref,
                reason_code="GENESIS_IMPLEMENTATION_PROOF",
                reason_vocabulary_version="v1",
            )
            accept = replace(accept, judgment_refs=(judgment.serialized_ref,))
            evidence_guard = e.EvidenceGuardAuthority(
                f["evidence"], e.EvidenceCheckpointUseRegistry(cps)
            )
            accepting = e.WorkflowKernel(
                e.PostgresTransitionRepository(
                    sessions,
                    e.TransitionEvaluator(
                        authorities.system, (authorities.human, evidence_guard, judgments)
                    ),
                )
            )
            facts = [await evidence_guard.issue_for_transition(accept)]
            for guard in e.TRANSITION_MATRIX[
                (e.WorkflowState.ADMISSION_PENDING, e.WorkflowState.ACCEPTED)
            ]:
                owner = e.GUARD_OWNER_POLICY[guard]
                if owner is e.GuardSemanticOwner.P1_4_SYSTEM:
                    facts.append(
                        authorities.system.issue(
                            guard_id=guard,
                            satisfied=True,
                            reason="ISOLATED_OWNER_TEST",
                            authority_ref="test:" + guard.value,
                            request=accept,
                        )
                    )
                elif owner is e.GuardSemanticOwner.P1_7_HUMAN:
                    facts.append(authorities.human.issue(guard, accept))
            final = await accepting.request_transition(
                accept,
                tuple(facts),
                transaction_participant=await judgments.participant(
                    accept, judgment.serialized_ref
                ),
            )
            assert final.resulting_state is e.WorkflowState.ACCEPTED
            transition_fp = e.canonical_hash(
                dict(
                    admitting_owner=final.admitting_owner,
                    decided_at=final.decided_at.astimezone(e.UTC).isoformat(),
                    kernel_version=final.kernel_version,
                    outcome=final.outcome.value,
                    reason=final.reason.value,
                    resulting_state=final.resulting_state.value,
                    resulting_state_version=final.resulting_state_version,
                    transition_decision_id=final.transition_decision_id,
                    transition_evaluation_id=final.transition_evaluation_id,
                    transition_request_id=final.transition_request_id,
                )
            )
            memory_policy = e.default_memory_policy(NOW)
            declaration = e.MemoryDeclaration(
                e.MemoryCategory.NEXT_ACTION_CONTEXT,
                context.context_logical_id,
                f"task-contract/{project}/{cid}@v1",
                "next-action-context/P1_8_NEXT_ACTION_CONTEXT_RESULT_V1/primary",
                memory_policy.serialized_ref,
                memory_policy.fingerprint,
                e.memory_content_fingerprint(
                    category=e.MemoryCategory.NEXT_ACTION_CONTEXT,
                    authority_mode=e.MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED,
                    policy_ref=memory_policy.serialized_ref,
                    normalized_derived_content=normalized,
                ),
                source_evidence_ref=evidence_ref,
                source_selector="/next_action_context",
                source_object_kind="P1_6_ADMITTED_STRUCTURED_RESULT",
                source_schema_id="AISCC-PROOF",
                source_schema_version="v1",
                external_context_ref=context.context_ref,
                external_context_fingerprint=context.fingerprint,
                external_context_introduction_event_ref=intro.event_ref,
                external_context_introduction_event_fingerprint=intro.event_fingerprint,
                external_context_snapshot_ref=snapshot.snapshot_ref,
                external_context_snapshot_fingerprint=snapshot.snapshot_fingerprint,
                external_context_event_high_watermark=snapshot.owner_event_high_watermark,
            )
            cycle_candidate = e.CycleCandidate(
                "cycle-" + cid,
                "v1",
                project,
                cid,
                "v1",
                e.p1_8_task_binding_fingerprint(
                    project_id=project, task_contract_id=cid, task_contract_version="v1"
                ),
                run_id,
                4,
                accept.transition_request_id,
                final.transition_decision_id,
                transition_fp,
                judgment.serialized_ref,
                judgment.fingerprint,
                attestation.serialized_ref,
                attestation.admitted_ref_root_hash,
                (declaration,),
                receipt.constraint_ref,
                receipt.constraint_fingerprint,
                snapshot.snapshot_ref,
                snapshot.snapshot_fingerprint,
                snapshot.owner_event_high_watermark,
            )
            cycles = e.PostgresCycleAdmissionRepository(
                sessions,
                f["evidence"],
                historical_content_access_grant=f[
                    "access_owner"
                ].issue_p1_8_structured_result_grant(),
                memory_policy=memory_policy,
                memory_policy_authority=e.default_memory_policy_authority(),
                task_authority_verifier=f["repo"],
            )
            await cycles.enroll_memory_policy()
            cycle = await cycles.admit(
                e.CycleAdmissionRequest(
                    "cycle-request-" + cid, "v1", cycle_candidate, "aiscc-system", NOW
                )
            )
            assert cycle.work_run_id == run_id
            for reader in (
                f["genesis"],
                GenesisAuthorityRepository(sessions, context=f["context"]),
            ):
                with pytest.raises(TaskContractError, match="GENESIS_NOT_ELIGIBLE"):
                    await current(f, reader)
            with pytest.raises(TaskContractError, match="GENESIS_NOT_ELIGIBLE"):
                await f["writer"].issue_task_contract(
                    body=f["body"], expected_current_body_sha256=None, issued_at=NOW
                )
            with pytest.raises(TaskContractError, match="GENESIS_NOT_ELIGIBLE"):
                await f["genesis_writer"].issue(
                    authority_id=f["authority"].value["genesis_authority_id"], issued_at=NOW
                )
            assert (await verify(f, receipt, current=False)).issued == receipt
            # Post-Cycle selection consumes the actual owner-admitted context relation.
            action_owner = m.default_next_action_policy_authority()
            eligibility, selection_policy, fixed = action_owner.issue_policy_catalog_v1(now=NOW)
            descriptor = action_owner.issue_context_bound_descriptor(
                context=context, issuance_event_sequence=intro.event_sequence
            )
            actions = m.PostgresNextActionRepository(
                sessions,
                eligibility_policy=eligibility,
                selection_policy=selection_policy,
                descriptors=(*fixed, descriptor),
                policy_authority=action_owner,
                task_authority_verifier=f["repo"],
            )
            await actions.enroll_configured_authority(NOW)
            async with sessions() as session:
                entry_id = await session.scalar(
                    select(ProjectMemoryEntryRow.entry_id).where(
                        ProjectMemoryEntryRow.project_id == project
                    )
                )
                watermark = await session.scalar(
                    select(func.max(m.ProjectMemoryAuthorityEventRow.event_sequence))
                )
            parameters = dict(
                source_cycle_id=cycle.cycle_id,
                memory_entry_refs=[entry_id],
                next_action_context_ref=context.context_ref,
                next_action_context_fingerprint=context.fingerprint,
                memory_authority_event_high_watermark=watermark,
            )
            selected, candidate = await actions.select(
                selection_id="after-cycle-" + cid,
                project_id=project,
                expected_project_revision=f["selected"].project_revision,
                mode=m.NextActionSelectionMode.CYCLE_DERIVED,
                proposals=(
                    m.NextActionProposal(
                        "cycle-proposal-" + cid,
                        project,
                        descriptor.action_ref,
                        parameters,
                        "First owner-admitted context",
                    ),
                ),
                memory_entry_ids=(entry_id,),
                now=NOW,
            )
            async with sessions() as session, session.begin():
                verified = await actions.verify_current_selection(
                    session,
                    selection_id=selected.selection_id,
                    expected_project_id=project,
                    expected_project_revision=selected.project_revision,
                    expected_selection_fingerprint=selected.fingerprint,
                    expected_candidate=candidate,
                    expected_action_ref=descriptor.action_ref,
                    expected_descriptor_fingerprint=descriptor.fingerprint,
                )
                assert verified[0] == selected
            revoked = await f["writer"].revoke_next_action_context(
                current_context_ref=context.context_ref,
                event_id="context-revoked-" + cid,
                effective_at=NOW + timedelta(seconds=1),
            )
            await f["writer"].certify_snapshot(
                snapshot_id="revoked-snapshot-" + cid,
                issued_at=NOW + timedelta(seconds=1),
            )
            await actions.reconcile_external_context_event(
                revoked.event_ref,
                expected_project_revisions={project: selected.project_revision},
            )
            assert (await actions.rebuild_projection(project))[0] is None
            assert await f["actions"].replay(f["selected"].selection_id) == (
                f["selected"],
                f["candidate"],
            )
            with pytest.raises(TaskContractError, match="GENESIS_NOT_ELIGIBLE"):
                await current(f, GenesisAuthorityRepository(sessions, context=f["context"]))
        finally:
            await f["engine"].dispose()

    asyncio.run(scenario())
