from __future__ import annotations

from datetime import UTC, datetime
from typing import NamedTuple

from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from aiscc.evidence.models import canonical_hash
from aiscc.judgment.authority import verify_historical_judgment_provenance
from aiscc.judgment.models import JudgmentOwnerPolicy
from aiscc.next_action.models import (
    TASK_ISSUANCE_OWNER,
    ActionRef,
    HumanInputKind,
    NextActionDescriptor,
    NextActionEligibilityPolicy,
    NextActionError,
    NextActionErrorCode,
    NextActionEvaluation,
    NextActionOwnerEvent,
    NextActionProposal,
    NextActionSelection,
    NextActionSelectionMode,
    NextActionSelectionPolicy,
    P1_8NextActionPolicyAuthority,
    TaskIssuanceCandidate,
    default_next_action_policy_authority,
    ranking_key,
)
from aiscc.persistence.models import (
    CycleMemoryReferenceRow,
    NextActionAuthorityEventRow,
    NextActionDescriptorRow,
    NextActionEvaluationRow,
    NextActionOwnerEventRow,
    NextActionPolicyDescriptorEnrollmentRow,
    NextActionPolicyRow,
    NextActionProjectionRow,
    NextActionProposalRow,
    NextActionSelectionRow,
    P1_4BlockerProjectionRow,
    P1_4BlockerProvenanceRow,
    ProjectMemoryAuthorityEventRow,
    ProjectMemoryEntryRow,
    ProjectMemoryViewRow,
    TaskIssuanceCandidateRow,
    TransitionDecisionRow,
    TransitionRequestRow,
    WorkRunRow,
)
from aiscc.persistence.repository import verify_historical_transition_provenance
from aiscc.task_authority.models import ExternalTaskAuthorityError, NextActionPriorityClass
from aiscc.task_authority.ports import ExternalTaskAuthorityVerifierPort


class _ResolvedContextSelection(NamedTuple):
    context_ref: str
    context_fingerprint: str
    snapshot_ref: str
    snapshot_fingerprint: str
    owner_event_high_watermark: int
    memory_event_high_watermark: int
    priority_class: NextActionPriorityClass
    critical_path_ordinal: int


class PostgresNextActionRepository:
    """System-owned deterministic selector; it cannot issue a TaskContract."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        *,
        eligibility_policy: NextActionEligibilityPolicy,
        selection_policy: NextActionSelectionPolicy,
        descriptors: tuple[NextActionDescriptor, ...],
        policy_authority: P1_8NextActionPolicyAuthority,
        task_authority_verifier: ExternalTaskAuthorityVerifierPort,
    ) -> None:
        self._session_factory = session_factory
        self._eligibility_policy = eligibility_policy
        self._selection_policy = selection_policy
        self._descriptors = {item.action_ref.serialized: item for item in descriptors}
        self._policy_authority = policy_authority
        self._task_authority_verifier = task_authority_verifier
        if len(self._descriptors) != len(descriptors):
            raise ValueError("configured ActionRef values must be unique")
        if (
            policy_authority is not default_next_action_policy_authority()
            or not policy_authority.recognizes_policy(eligibility_policy)
            or not policy_authority.recognizes_policy(selection_policy)
            or not all(policy_authority.recognizes_descriptor(item) for item in descriptors)
        ):
            raise NextActionError(
                NextActionErrorCode.AUTHORITY_DENIED,
                "NextAction graph was not issued by bootstrap-bound P1-8 authority",
            )
        configured_bindings = {
            (item.action_ref.serialized, item.fingerprint) for item in descriptors
        }
        if not set(eligibility_policy.enrolled_action_bindings).issubset(configured_bindings):
            raise NextActionError(
                NextActionErrorCode.NOT_ENROLLED,
                "eligibility policy does not bind the exact descriptor set",
            )

    async def enroll_configured_authority(self, now: datetime | None = None) -> None:
        issued_at = (now or datetime.now(UTC)).astimezone(UTC)
        async with self._session_factory() as session, session.begin():
            await _lock(session, "p1-8-next-action-enrollment")
            for kind, policy in (
                ("ELIGIBILITY", self._eligibility_policy),
                ("SELECTION", self._selection_policy),
            ):
                row = await session.get(NextActionPolicyRow, policy.policy_ref)
                payload: dict[str, object] = _policy_payload(policy, kind)
                if row is not None:
                    if row.fingerprint != policy.fingerprint or row.payload != payload:
                        raise NextActionError(
                            NextActionErrorCode.HISTORICAL_CORRUPTION,
                            "policy immutable identity conflicts",
                        )
                else:
                    session.add(
                        NextActionPolicyRow(
                            policy_ref=policy.policy_ref,
                            policy_kind=kind,
                            fingerprint=policy.fingerprint,
                            authority_revision=policy.authority_revision,
                            payload=payload,
                            issued_at=issued_at,
                        )
                    )
                    session.add(
                        NextActionOwnerEventRow(
                            event_id="next-action-policy-issued-"
                            + canonical_hash([kind, policy.policy_ref]),
                            subject_ref=policy.policy_ref,
                            subject_kind="POLICY",
                            event_kind="ISSUED",
                            replacement_ref="NONE",
                            payload={
                                "authority_id": policy.authority_id,
                                "authority_version": policy.authority_version,
                                "authority_revision": policy.authority_revision,
                                "fingerprint": policy.fingerprint,
                            },
                            created_at=issued_at,
                        )
                    )
            for descriptor in self._descriptors.values():
                existing = await session.get(
                    NextActionDescriptorRow, descriptor.action_ref.serialized
                )
                payload = _descriptor_payload(descriptor)
                if existing is not None:
                    if (
                        existing.fingerprint != descriptor.fingerprint
                        or existing.payload != payload
                    ):
                        raise NextActionError(
                            NextActionErrorCode.HISTORICAL_CORRUPTION,
                            "descriptor immutable identity conflicts",
                        )
                else:
                    session.add(
                        NextActionDescriptorRow(
                            action_ref=descriptor.action_ref.serialized,
                            descriptor_version=descriptor.descriptor_version,
                            fingerprint=descriptor.fingerprint,
                            authority_revision=descriptor.authority_revision,
                            payload=payload,
                            enrolled_at=issued_at,
                        )
                    )
                enrollment_id = "next-action-policy-descriptor-enrollment-" + canonical_hash(
                    [
                        self._eligibility_policy.policy_ref,
                        descriptor.action_ref.serialized,
                        descriptor.fingerprint,
                    ]
                )
                enrollment = await session.get(
                    NextActionPolicyDescriptorEnrollmentRow, enrollment_id
                )
                enrollment_payload = {
                    "authority_id": self._eligibility_policy.authority_id,
                    "authority_version": self._eligibility_policy.authority_version,
                    "effective_sequence": self._eligibility_policy.effective_sequence,
                }
                if enrollment is None:
                    session.add(
                        NextActionPolicyDescriptorEnrollmentRow(
                            enrollment_id=enrollment_id,
                            eligibility_policy_ref=self._eligibility_policy.policy_ref,
                            eligibility_policy_fingerprint=self._eligibility_policy.fingerprint,
                            action_ref=descriptor.action_ref.serialized,
                            descriptor_fingerprint=descriptor.fingerprint,
                            authority_revision=self._eligibility_policy.authority_revision,
                            payload=enrollment_payload,
                            enrolled_at=issued_at,
                        )
                    )
                elif (
                    enrollment.eligibility_policy_fingerprint
                    != self._eligibility_policy.fingerprint
                    or enrollment.descriptor_fingerprint != descriptor.fingerprint
                    or enrollment.payload != enrollment_payload
                ):
                    raise NextActionError(
                        NextActionErrorCode.HISTORICAL_CORRUPTION,
                        "policy-to-descriptor enrollment identity conflicts",
                    )
                owner_event_id = "next-action-descriptor-enrolled-" + descriptor.fingerprint
                if (
                    await session.scalar(
                        select(NextActionOwnerEventRow).where(
                            NextActionOwnerEventRow.event_id == owner_event_id
                        )
                    )
                    is None
                ):
                    session.add(
                        NextActionOwnerEventRow(
                            event_id=owner_event_id,
                            subject_ref=descriptor.action_ref.serialized,
                            subject_kind="DESCRIPTOR",
                            event_kind="ENROLLED",
                            replacement_ref="NONE",
                            payload={"fingerprint": descriptor.fingerprint},
                            created_at=issued_at,
                        )
                    )

    async def select(
        self,
        *,
        selection_id: str,
        project_id: str,
        expected_project_revision: int,
        mode: NextActionSelectionMode,
        proposals: tuple[NextActionProposal, ...],
        memory_entry_ids: tuple[str, ...] = (),
        operational_work_run_id: str | None = None,
        human_judgment_ref: str | None = None,
        now: datetime | None = None,
    ) -> tuple[NextActionSelection, TaskIssuanceCandidate]:
        if not proposals:
            raise NextActionError(NextActionErrorCode.NOT_ENROLLED, "no proposal")
        if any(item.project_id != project_id for item in proposals):
            raise NextActionError(NextActionErrorCode.IDENTITY_CONFLICT, "foreign project proposal")
        selected_at = (now or datetime.now(UTC)).astimezone(UTC)
        async with self._session_factory() as session, session.begin():
            await _lock(session, f"p1-8-next-action-project:{project_id}")
            projection = await session.get(
                NextActionProjectionRow, project_id, with_for_update=True
            )
            current_revision = projection.project_revision if projection is not None else 0
            existing = await session.get(NextActionSelectionRow, selection_id)
            if existing is not None:
                pair = await self._replay_pair(session, existing)
                evaluation_row = await session.get(NextActionEvaluationRow, existing.evaluation_id)
                raw_persisted_ids = (
                    evaluation_row.payload.get("ranked_proposal_ids")
                    if evaluation_row is not None
                    else None
                )
                persisted_ids = (
                    tuple(str(item) for item in raw_persisted_ids)
                    if isinstance(raw_persisted_ids, list)
                    else ()
                )
                supplied = {item.proposal_id: item for item in proposals}
                persisted_proposals = tuple(
                    await session.scalars(
                        select(NextActionProposalRow).where(
                            NextActionProposalRow.proposal_id.in_(persisted_ids)
                        )
                    )
                )
                exact_replay = bool(
                    evaluation_row is not None
                    and existing.project_id == project_id
                    and expected_project_revision == existing.project_revision - 1
                    and evaluation_row.payload.get("mode") == mode.value
                    and set(persisted_ids) == set(supplied)
                    and tuple(sorted(memory_entry_ids)) == pair[0].memory_refs
                    and evaluation_row.payload.get("human_judgment_ref") == human_judgment_ref
                    and evaluation_row.payload.get("operational_work_run_id")
                    == operational_work_run_id
                    and all(
                        item.proposal_id in supplied
                        and item.fingerprint == supplied[item.proposal_id].fingerprint
                        for item in persisted_proposals
                    )
                    and len(persisted_proposals) == len(supplied)
                )
                if not exact_replay:
                    raise NextActionError(
                        NextActionErrorCode.IDENTITY_CONFLICT,
                        "selection ID replay differs from original proposal",
                    )
                return pair
            if expected_project_revision != current_revision:
                raise NextActionError(
                    NextActionErrorCode.IDENTITY_CONFLICT,
                    "same project revision was already consumed",
                )
            await self._require_current_policy(
                session,
                self._eligibility_policy.policy_ref,
                self._eligibility_policy.fingerprint,
                "ELIGIBILITY",
            )
            await self._require_current_policy(
                session,
                self._selection_policy.policy_ref,
                self._selection_policy.fingerprint,
                "SELECTION",
            )
            eligible: list[
                tuple[tuple[int, int, int, int, str, str], NextActionProposal, NextActionDescriptor]
            ] = []
            for proposal in proposals:
                descriptor = self._descriptors.get(proposal.action_ref.serialized)
                row = await session.get(NextActionDescriptorRow, proposal.action_ref.serialized)
                if (
                    descriptor is None
                    or row is None
                    or row.fingerprint != descriptor.fingerprint
                    or row.payload != _descriptor_payload(descriptor)
                ):
                    raise NextActionError(
                        NextActionErrorCode.NOT_ENROLLED,
                        f"{proposal.action_ref.serialized} is not enrolled",
                    )
                enrollment = await session.scalar(
                    select(NextActionPolicyDescriptorEnrollmentRow).where(
                        NextActionPolicyDescriptorEnrollmentRow.eligibility_policy_ref
                        == self._eligibility_policy.policy_ref,
                        NextActionPolicyDescriptorEnrollmentRow.action_ref
                        == proposal.action_ref.serialized,
                    )
                )
                if (
                    enrollment is None
                    or enrollment.eligibility_policy_fingerprint
                    != self._eligibility_policy.fingerprint
                    or enrollment.descriptor_fingerprint != descriptor.fingerprint
                ):
                    raise NextActionError(
                        NextActionErrorCode.NOT_ENROLLED,
                        "descriptor is not enrolled by the current eligibility policy",
                    )
                await self._require_current_subject(
                    session, proposal.action_ref.serialized, "DESCRIPTOR"
                )
                eligible.append((ranking_key(proposal, descriptor), proposal, descriptor))
            context_selection: _ResolvedContextSelection | None = None
            operational_rank = 0
            if mode is NextActionSelectionMode.CYCLE_DERIVED:
                context_selection = await self._require_current_memory(
                    session, project_id, memory_entry_ids
                )
                authoritative_input_refs = tuple(sorted(memory_entry_ids))
            elif memory_entry_ids:
                raise NextActionError(
                    NextActionErrorCode.NON_CURRENT_MEMORY,
                    "operational recovery uses source-domain facts, not memory claims",
                )
            else:
                (
                    authoritative_input_refs,
                    operational_rank,
                ) = await self._require_operational_recovery(
                    session, project_id, operational_work_run_id
                )
                context_selection = None
            if mode is NextActionSelectionMode.CYCLE_DERIVED:
                assert context_selection is not None
                authoritative_rank = dict(self._selection_policy.class_to_rank)[
                    context_selection.priority_class.value
                ]
                rebound: list[
                    tuple[
                        tuple[int, int, int, int, str, str],
                        NextActionProposal,
                        NextActionDescriptor,
                    ]
                ] = []
                for _, proposal, bound_descriptor in eligible:
                    payload = bound_descriptor.canonical_payload or {}
                    if (
                        payload.get("priority_classification_source_kind")
                        != "NEXT_ACTION_CONTEXT_REF_V1"
                        or payload.get("priority_classification_source_ref")
                        != context_selection.context_ref
                        or payload.get("priority_classification_source_hash")
                        != context_selection.context_fingerprint
                        or payload.get("priority_classification_source_contract_ref")
                        != (
                            "next-action-context-source-contract:v1:"
                            "NEXT_ACTION_CONTEXT_SOURCE_CONTRACT_V1"
                        )
                        or payload.get("priority_classification_source_contract_fingerprint")
                        != "988cdd4c71aca75e3434652044b50ffd703fb32ba4568219c56d52e498cd8698"
                        or bound_descriptor.critical_path_ordinal
                        != context_selection.critical_path_ordinal
                    ):
                        raise NextActionError(
                            NextActionErrorCode.PRIORITY_SOURCE_NOT_ENROLLED,
                            "descriptor does not enroll the exact external context source",
                        )
                    rebound.append(
                        (
                            ranking_key(
                                proposal,
                                bound_descriptor,
                                authoritative_priority_rank=authoritative_rank,
                                enrolled_critical_path_ordinal=(
                                    context_selection.critical_path_ordinal
                                ),
                            ),
                            proposal,
                            bound_descriptor,
                        )
                    )
                eligible = rebound
            else:
                eligible = [
                    (
                        ranking_key(
                            proposal,
                            bound_descriptor,
                            authoritative_priority_rank=operational_rank,
                        ),
                        proposal,
                        bound_descriptor,
                    )
                    for _, proposal, bound_descriptor in eligible
                ]
            eligible.sort(key=lambda item: item[0])
            _, winner, descriptor = eligible[0]
            if mode not in descriptor.allowed_selection_modes:
                raise NextActionError(
                    NextActionErrorCode.NOT_ENROLLED,
                    "descriptor does not authorize the requested selection mode",
                )
            if context_selection is not None and (
                winner.parameters.get("next_action_context_ref") != context_selection.context_ref
                or winner.parameters.get("next_action_context_fingerprint")
                != context_selection.context_fingerprint
                or winner.parameters.get("memory_entry_refs") != list(memory_entry_ids)
                or winner.parameters.get("memory_authority_event_high_watermark")
                != context_selection.memory_event_high_watermark
            ):
                raise NextActionError(
                    NextActionErrorCode.PRIORITY_SOURCE_NOT_ENROLLED,
                    "proposal context parameters differ from resolved selection inputs",
                )
            if (
                descriptor.project_restriction != "*"
                and descriptor.project_restriction != project_id
            ):
                raise NextActionError(
                    NextActionErrorCode.NOT_ENROLLED, "descriptor project scope differs"
                )
            if descriptor.required_human_input_kind is HumanInputKind.BEFORE_SELECTION:
                if human_judgment_ref is None:
                    raise NextActionError(
                        NextActionErrorCode.HUMAN_INPUT_REQUIRED,
                        "descriptor requires accepted P1-7 authority",
                    )
                judgment = await verify_historical_judgment_provenance(session, human_judgment_ref)
                judgment_run = await session.get(WorkRunRow, judgment.work_run_id)
                if (
                    judgment_run is None
                    or judgment_run.project_id != project_id
                    or judgment.serialized_ref != human_judgment_ref
                    or judgment.owner_policy is not JudgmentOwnerPolicy.HUMAN
                    or judgment.human_gate_ref is None
                    or judgment.human_result_ref is None
                    or (
                        descriptor.scope_restrictions.get("work_run_id")
                        and descriptor.scope_restrictions["work_run_id"] != judgment.work_run_id
                    )
                    or (
                        descriptor.scope_restrictions.get("task_contract_id")
                        and descriptor.scope_restrictions["task_contract_id"]
                        != judgment.task_contract_id
                    )
                    or (
                        descriptor.scope_restrictions.get("state_version")
                        and descriptor.scope_restrictions["state_version"]
                        != str(judgment.state_version)
                    )
                    or (
                        descriptor.scope_restrictions.get("target_state")
                        and descriptor.scope_restrictions["target_state"]
                        != judgment.target_state.value
                    )
                ):
                    raise NextActionError(
                        NextActionErrorCode.HUMAN_BINDING_MISMATCH,
                        "Human Judgment authority differs",
                    )
                authoritative_input_refs += (human_judgment_ref,)
            elif human_judgment_ref is not None:
                raise NextActionError(
                    NextActionErrorCode.HUMAN_BINDING_MISMATCH,
                    "Judgment cannot substitute for the descriptor Human input kind",
                )
            owner_high_watermark = int(
                await session.scalar(
                    select(func.coalesce(func.max(NextActionOwnerEventRow.event_sequence), 0))
                )
                or 0
            )
            enrollment = await session.scalar(
                select(NextActionPolicyDescriptorEnrollmentRow).where(
                    NextActionPolicyDescriptorEnrollmentRow.eligibility_policy_ref
                    == self._eligibility_policy.policy_ref,
                    NextActionPolicyDescriptorEnrollmentRow.action_ref
                    == descriptor.action_ref.serialized,
                )
            )
            assert enrollment is not None
            new_revision = current_revision + 1
            ranked_ids = tuple(item[1].proposal_id for item in eligible)
            evaluation = NextActionEvaluation(
                "next-action-evaluation-"
                + canonical_hash([project_id, new_revision, list(ranked_ids)]),
                project_id,
                new_revision,
                mode,
                ranked_ids,
                self._eligibility_policy.policy_ref,
                self._eligibility_policy.fingerprint,
                self._selection_policy.policy_ref,
                self._selection_policy.fingerprint,
                enrollment.enrollment_id,
                owner_high_watermark,
                tuple(sorted(authoritative_input_refs)),
                operational_work_run_id,
                human_judgment_ref,
                selected_at,
                eligible[0][0][0],
                eligible[0][0][2],
                (context_selection.priority_class.value if context_selection is not None else None),
                (context_selection.context_ref if context_selection is not None else None),
                (context_selection.context_fingerprint if context_selection is not None else None),
                (
                    context_selection.owner_event_high_watermark
                    if context_selection is not None
                    else None
                ),
                (
                    context_selection.memory_event_high_watermark
                    if context_selection is not None
                    else None
                ),
            )
            selection = NextActionSelection(
                selection_id,
                "v1",
                project_id,
                new_revision,
                evaluation.evaluation_id,
                winner.proposal_id,
                winner.action_ref,
                descriptor.descriptor_version,
                descriptor.fingerprint,
                winner.parameters,
                tuple(sorted(memory_entry_ids)),
                selected_at,
                (context_selection.context_ref if context_selection is not None else None),
                (context_selection.context_fingerprint if context_selection is not None else None),
                (context_selection.snapshot_ref if context_selection is not None else None),
                (context_selection.snapshot_fingerprint if context_selection is not None else None),
                (
                    context_selection.owner_event_high_watermark
                    if context_selection is not None
                    else None
                ),
                (
                    context_selection.memory_event_high_watermark
                    if context_selection is not None
                    else None
                ),
            )
            issuance = TaskIssuanceCandidate(
                "task-issuance-candidate-" + selection.fingerprint,
                f"p1-8-next-action-selection:v1:{selection.selection_id}",
                selection.action_ref,
                selection.parameters,
                TASK_ISSUANCE_OWNER,
                (
                    HumanInputKind.AFTER_TASK_ISSUANCE_P1_7
                    if descriptor.required_human_input_kind
                    is HumanInputKind.AFTER_TASK_ISSUANCE_P1_7
                    else HumanInputKind.NONE
                ),
                selected_at,
            )
            for proposal in proposals:
                session.add(
                    NextActionProposalRow(
                        proposal_id=proposal.proposal_id,
                        fingerprint=proposal.fingerprint,
                        project_id=project_id,
                        action_ref=proposal.action_ref.serialized,
                        payload={
                            "parameters": proposal.parameters,
                            "rationale": proposal.rationale,
                            # Claims are retained only as audit input and never ranking authority.
                            "non_authoritative_claims": {
                                "blocker": proposal.claimed_blocker,
                                "priority": proposal.claimed_priority,
                                "security": proposal.claimed_security,
                            },
                        },
                        proposed_at=selected_at,
                    )
                )
            evaluation_fingerprint = canonical_hash(_evaluation_payload(evaluation))
            session.add(
                NextActionEvaluationRow(
                    evaluation_id=evaluation.evaluation_id,
                    project_id=project_id,
                    project_revision=new_revision,
                    fingerprint=evaluation_fingerprint,
                    payload=_evaluation_payload(evaluation),
                    evaluated_at=selected_at,
                )
            )
            session.add(
                NextActionSelectionRow(
                    selection_id=selection.selection_id,
                    serialized_ref=issuance.selection_ref,
                    fingerprint=selection.fingerprint,
                    project_id=project_id,
                    project_revision=new_revision,
                    evaluation_id=evaluation.evaluation_id,
                    action_ref=selection.action_ref.serialized,
                    external_context_ref=selection.external_context_ref,
                    external_context_fingerprint=selection.external_context_fingerprint,
                    external_context_snapshot_ref=selection.external_context_snapshot_ref,
                    external_context_snapshot_fingerprint=(
                        selection.external_context_snapshot_fingerprint
                    ),
                    external_context_event_high_watermark=(
                        selection.external_context_event_high_watermark
                    ),
                    memory_authority_event_high_watermark=(
                        selection.memory_authority_event_high_watermark
                    ),
                    payload=_selection_payload(selection),
                    selected_at=selected_at,
                )
            )
            await session.flush()
            event = NextActionAuthorityEventRow(
                event_id="next-action-selected-" + selection.fingerprint,
                project_id=project_id,
                selection_id=selection.selection_id,
                event_kind="SELECTED",
                prior_revision=current_revision,
                new_revision=new_revision,
                payload={"fingerprint": selection.fingerprint},
                created_at=selected_at,
            )
            session.add(event)
            session.add(
                TaskIssuanceCandidateRow(
                    candidate_id=issuance.candidate_id,
                    selection_id=selection.selection_id,
                    issuance_owner=TASK_ISSUANCE_OWNER,
                    payload={
                        "action_ref": issuance.action_ref.serialized,
                        "parameters": issuance.parameters,
                        "selection_ref": issuance.selection_ref,
                        "required_post_issuance_human_input": (
                            issuance.required_post_issuance_human_input.value
                        ),
                    },
                    created_at=selected_at,
                )
            )
            await session.flush()
            if projection is None:
                session.add(
                    NextActionProjectionRow(
                        project_id=project_id,
                        selection_id=selection.selection_id,
                        project_revision=new_revision,
                        latest_event_sequence=event.event_sequence,
                        state="CURRENT",
                        reason="SELECTED_CURRENT",
                        updated_at=selected_at,
                    )
                )
            else:
                projection.selection_id = selection.selection_id
                projection.project_revision = new_revision
                projection.latest_event_sequence = event.event_sequence
                projection.state = "CURRENT"
                projection.reason = "SELECTED_CURRENT"
                projection.updated_at = selected_at
            return selection, issuance

    async def apply_owner_event(
        self, event: NextActionOwnerEvent, *, expected_project_revisions: dict[str, int]
    ) -> None:
        if not self._policy_authority.recognizes_event(event):
            raise NextActionError(
                NextActionErrorCode.AUTHORITY_DENIED, "foreign NextAction owner event"
            )
        async with self._session_factory() as session, session.begin():
            await _lock(session, f"p1-8-next-action-owner:{event.subject_ref}")
            await self._require_current_subject(session, event.subject_ref, event.subject_kind)
            session.add(
                NextActionOwnerEventRow(
                    event_id=event.event_id,
                    subject_ref=event.subject_ref,
                    subject_kind=event.subject_kind,
                    event_kind=event.event_kind,
                    replacement_ref=event.replacement_ref,
                    payload={"disposition": event.disposition.value},
                    created_at=event.created_at,
                )
            )
            if event.disposition.value != "WITHDRAW_CURRENT":
                return
            projections = tuple(
                await session.scalars(
                    select(NextActionProjectionRow)
                    .where(NextActionProjectionRow.state == "CURRENT")
                    .with_for_update()
                )
            )
            for projection in projections:
                if projection.selection_id is None:
                    continue
                selection = await session.get(NextActionSelectionRow, projection.selection_id)
                evaluation = (
                    await session.get(NextActionEvaluationRow, selection.evaluation_id)
                    if selection is not None
                    else None
                )
                affected = bool(
                    selection is not None
                    and (
                        event.subject_ref == selection.action_ref
                        or (
                            evaluation is not None
                            and event.subject_ref
                            in {
                                evaluation.payload.get("eligibility_policy_ref"),
                                evaluation.payload.get("selection_policy_ref"),
                            }
                        )
                    )
                )
                if not affected or selection is None:
                    continue
                if expected_project_revisions.get(projection.project_id) != (
                    projection.project_revision
                ):
                    raise NextActionError(
                        NextActionErrorCode.IDENTITY_CONFLICT,
                        "owner-event current withdrawal project revision differs",
                    )
                authority_event = NextActionAuthorityEventRow(
                    event_id="next-action-withdraw-"
                    + canonical_hash([event.event_id, selection.selection_id]),
                    project_id=projection.project_id,
                    selection_id=selection.selection_id,
                    event_kind="WITHDRAWN",
                    prior_revision=projection.project_revision,
                    new_revision=projection.project_revision + 1,
                    payload={"owner_event_id": event.event_id},
                    created_at=event.created_at,
                )
                session.add(authority_event)
                await session.flush()
                projection.selection_id = None
                projection.project_revision = authority_event.new_revision
                projection.latest_event_sequence = authority_event.event_sequence
                projection.state = "WITHDRAWN"
                projection.reason = "OWNER_AUTHORITY_CURRENT_WITHDRAWN"
                projection.updated_at = event.created_at

    async def reconcile_external_context_event(
        self,
        event_ref: str,
        *,
        expected_project_revisions: dict[str, int],
    ) -> None:
        """Append idempotent Memory/selection withdrawals from a verified owner event."""
        event = await self._task_authority_verifier.get_context_event(event_ref)
        if event is None or event.event_kind.value not in {"SUPERSEDED", "REVOKED"}:
            raise NextActionError(
                NextActionErrorCode.PRIORITY_SOURCE_NOT_ENROLLED,
                "external context invalidation event is absent or non-withdrawing",
            )
        latest = await self._task_authority_verifier.latest_snapshot()
        if event.event_sequence > latest.owner_event_high_watermark:
            raise NextActionError(
                NextActionErrorCode.PRIORITY_SOURCE_NOT_ENROLLED,
                "external invalidation is outside the latest certified owner prefix",
            )
        async with self._session_factory() as session, session.begin():
            await _lock(session, f"external-context-invalidation:{event.event_ref}")
            entries = tuple(
                await session.scalars(
                    select(ProjectMemoryEntryRow).where(
                        ProjectMemoryEntryRow.external_context_ref == event.context_ref
                    )
                )
            )
            for entry in entries:
                view = await session.get(
                    ProjectMemoryViewRow, entry.memory_lineage_key, with_for_update=True
                )
                if view is None or view.current_entry_id != entry.entry_id:
                    continue
                event_id = "memory-external-context-withdrawn-" + canonical_hash(
                    [event.event_ref, entry.entry_id]
                )
                existing = await session.scalar(
                    select(ProjectMemoryAuthorityEventRow).where(
                        ProjectMemoryAuthorityEventRow.event_id == event_id
                    )
                )
                if existing is not None:
                    continue
                memory_event = ProjectMemoryAuthorityEventRow(
                    event_id=event_id,
                    memory_lineage_key=entry.memory_lineage_key,
                    subject_entry_id=entry.entry_id,
                    replacement_entry_id="NONE",
                    event_kind="REVOKED",
                    prior_revision=view.authority_revision,
                    new_revision=view.authority_revision + 1,
                    authority_ref=event.event_ref,
                    reason="EXTERNAL_CONTEXT_CURRENT_WITHDRAWN",
                    payload={
                        "external_event_ref": event.event_ref,
                        "external_event_fingerprint": event.event_fingerprint,
                    },
                    created_at=event.effective_at,
                )
                session.add(memory_event)
                await session.flush()
                view.current_entry_id = None
                view.state = "REVOKED"
                view.reason = memory_event.reason
                view.authority_revision = memory_event.new_revision
                view.latest_event_sequence = memory_event.event_sequence
                view.updated_at = event.effective_at

            projections = tuple(
                await session.scalars(
                    select(NextActionProjectionRow)
                    .where(NextActionProjectionRow.state == "CURRENT")
                    .with_for_update()
                )
            )
            for projection in projections:
                selection = (
                    await session.get(NextActionSelectionRow, projection.selection_id)
                    if projection.selection_id is not None
                    else None
                )
                if selection is None or selection.external_context_ref != event.context_ref:
                    continue
                if expected_project_revisions.get(projection.project_id) != (
                    projection.project_revision
                ):
                    raise NextActionError(
                        NextActionErrorCode.IDENTITY_CONFLICT,
                        "external-event withdrawal project revision differs",
                    )
                event_id = "next-action-external-context-withdrawn-" + canonical_hash(
                    [event.event_ref, selection.selection_id]
                )
                existing = await session.scalar(
                    select(NextActionAuthorityEventRow).where(
                        NextActionAuthorityEventRow.event_id == event_id
                    )
                )
                if existing is not None:
                    continue
                withdrawal = NextActionAuthorityEventRow(
                    event_id=event_id,
                    project_id=projection.project_id,
                    selection_id=selection.selection_id,
                    event_kind="WITHDRAWN",
                    prior_revision=projection.project_revision,
                    new_revision=projection.project_revision + 1,
                    payload={
                        "external_event_ref": event.event_ref,
                        "external_event_fingerprint": event.event_fingerprint,
                    },
                    created_at=event.effective_at,
                )
                session.add(withdrawal)
                await session.flush()
                projection.selection_id = None
                projection.project_revision = withdrawal.new_revision
                projection.latest_event_sequence = withdrawal.event_sequence
                projection.state = "WITHDRAWN"
                projection.reason = "EXTERNAL_CONTEXT_CURRENT_WITHDRAWN"
                projection.updated_at = event.effective_at

    async def replay(self, selection_id: str) -> tuple[NextActionSelection, TaskIssuanceCandidate]:
        async with self._session_factory() as session:
            row = await session.get(NextActionSelectionRow, selection_id)
            if row is None:
                raise NextActionError(NextActionErrorCode.HISTORICAL_CORRUPTION, "selection absent")
            return await self._replay_pair(session, row)

    async def rebuild_projection(self, project_id: str) -> tuple[str | None, int]:
        async with self._session_factory() as session, session.begin():
            await _lock(session, f"p1-8-next-action-project:{project_id}")
            events = tuple(
                await session.scalars(
                    select(NextActionAuthorityEventRow)
                    .where(NextActionAuthorityEventRow.project_id == project_id)
                    .order_by(NextActionAuthorityEventRow.event_sequence)
                )
            )
            revision = 0
            selection_id: str | None = None
            state = "WITHDRAWN"
            reason = "NO_CURRENT_SELECTION"
            latest = 0
            updated_at: datetime | None = None
            for event in events:
                if event.prior_revision != revision or event.new_revision != revision + 1:
                    raise NextActionError(
                        NextActionErrorCode.HISTORICAL_CORRUPTION,
                        "NextAction authority event gap or duplicate",
                    )
                if await session.get(NextActionSelectionRow, event.selection_id) is None:
                    raise NextActionError(
                        NextActionErrorCode.HISTORICAL_CORRUPTION,
                        "NextAction event selection absent",
                    )
                revision = event.new_revision
                if event.event_kind == "SELECTED":
                    selection_id = event.selection_id
                    state = "CURRENT"
                    reason = "SELECTED_CURRENT"
                elif event.event_kind == "WITHDRAWN":
                    selection_id = None
                    state = "WITHDRAWN"
                    reason = "OWNER_AUTHORITY_CURRENT_WITHDRAWN"
                else:
                    raise NextActionError(
                        NextActionErrorCode.HISTORICAL_CORRUPTION,
                        "unknown NextAction authority event kind",
                    )
                latest = event.event_sequence
                updated_at = event.created_at
            if updated_at is None:
                raise NextActionError(
                    NextActionErrorCode.HISTORICAL_CORRUPTION, "no selection history"
                )
            projection = await session.get(NextActionProjectionRow, project_id)
            if projection is None:
                session.add(
                    NextActionProjectionRow(
                        project_id=project_id,
                        selection_id=selection_id,
                        project_revision=revision,
                        latest_event_sequence=latest,
                        state=state,
                        reason=reason,
                        updated_at=updated_at,
                    )
                )
            else:
                projection.selection_id = selection_id
                projection.project_revision = revision
                projection.latest_event_sequence = latest
                projection.state = state
                projection.reason = reason
                projection.updated_at = updated_at
            return selection_id, revision

    async def _require_current_policy(
        self, session: AsyncSession, policy_ref: str, fingerprint: str, kind: str
    ) -> None:
        row = await session.get(NextActionPolicyRow, policy_ref)
        configured = self._eligibility_policy if kind == "ELIGIBILITY" else self._selection_policy
        if (
            row is None
            or row.policy_kind != kind
            or row.fingerprint != fingerprint
            or row.payload != _policy_payload(configured, kind)
        ):
            raise NextActionError(NextActionErrorCode.POLICY_NOT_CURRENT, f"{kind} policy absent")
        await self._require_current_subject(session, policy_ref, "POLICY")

    async def _require_current_subject(
        self, session: AsyncSession, subject_ref: str, subject_kind: str
    ) -> None:
        events = tuple(
            await session.scalars(
                select(NextActionOwnerEventRow)
                .where(
                    NextActionOwnerEventRow.subject_ref == subject_ref,
                    NextActionOwnerEventRow.subject_kind == subject_kind,
                )
                .order_by(NextActionOwnerEventRow.event_sequence)
            )
        )
        issued = "ISSUED" if subject_kind == "POLICY" else "ENROLLED"
        if len(events) != 1 or events[0].event_kind != issued:
            code = (
                NextActionErrorCode.POLICY_NOT_CURRENT
                if subject_kind == "POLICY"
                else NextActionErrorCode.DESCRIPTOR_NOT_CURRENT
            )
            raise NextActionError(code, f"{subject_kind} is not current")

    async def _require_current_memory(
        self, session: AsyncSession, project_id: str, entry_ids: tuple[str, ...]
    ) -> _ResolvedContextSelection:
        if not entry_ids:
            raise NextActionError(
                NextActionErrorCode.NON_CURRENT_MEMORY, "CYCLE_DERIVED requires CURRENT memory"
            )
        contexts: list[tuple[ProjectMemoryEntryRow, CycleMemoryReferenceRow]] = []
        for entry_id in sorted(set(entry_ids)):
            entry = await session.get(ProjectMemoryEntryRow, entry_id)
            view = (
                await session.get(ProjectMemoryViewRow, entry.memory_lineage_key)
                if entry is not None
                else None
            )
            if (
                entry is None
                or entry.project_id != project_id
                or view is None
                or view.current_entry_id != entry_id
                or view.state != "CURRENT"
            ):
                raise NextActionError(
                    NextActionErrorCode.NON_CURRENT_MEMORY, "memory is not CURRENT"
                )
            if entry.category == "NEXT_ACTION_CONTEXT":
                reference = await session.scalar(
                    select(CycleMemoryReferenceRow).where(
                        CycleMemoryReferenceRow.entry_id == entry.entry_id,
                        CycleMemoryReferenceRow.cycle_id == entry.cycle_id,
                        CycleMemoryReferenceRow.declaration_ordinal == entry.declaration_ordinal,
                    )
                )
                if reference is None:
                    raise NextActionError(
                        NextActionErrorCode.NON_CURRENT_MEMORY,
                        "NEXT_ACTION_CONTEXT Cycle provenance is absent",
                    )
                contexts.append((entry, reference))
        if len(contexts) != 1:
            raise NextActionError(
                NextActionErrorCode.NON_CURRENT_MEMORY,
                "CYCLE_DERIVED requires exactly one CURRENT NEXT_ACTION_CONTEXT",
            )
        entry, reference = contexts[0]
        content = entry.payload.get("normalized_content")
        provenance = reference.provenance
        exact_content = {
            "context_ref",
            "context_fingerprint",
            "context_logical_id",
            "project_id",
            "task_contract_id",
            "task_contract_version",
            "context_slot_id",
            "priority_class",
            "critical_path_ordinal",
        }
        exact_provenance = {
            "context_ref",
            "context_fingerprint",
            "context_introduction_event_ref",
            "context_introduction_event_fingerprint",
            "context_snapshot_ref",
            "context_snapshot_fingerprint",
            "context_authority_event_high_watermark",
        }
        if (
            not isinstance(content, dict)
            or set(content) != exact_content
            or not isinstance(provenance, dict)
            or set(provenance) != exact_provenance
            or content["context_ref"] != provenance["context_ref"]
            or content["context_fingerprint"] != provenance["context_fingerprint"]
            or content["project_id"] != project_id
            or entry.external_context_ref != content["context_ref"]
        ):
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION,
                "NEXT_ACTION_CONTEXT Memory/owner locator differs",
            )
        latest = await self._task_authority_verifier.latest_snapshot()
        try:
            fold = await self._task_authority_verifier.verify_next_action_context(
                context_ref=str(content["context_ref"]),
                context_fingerprint=str(content["context_fingerprint"]),
                introduction_event_ref=str(provenance["context_introduction_event_ref"]),
                introduction_event_fingerprint=str(
                    provenance["context_introduction_event_fingerprint"]
                ),
                snapshot_ref=latest.snapshot_ref,
                snapshot_fingerprint=latest.snapshot_fingerprint,
                owner_event_high_watermark=latest.owner_event_high_watermark,
                require_current=True,
            )
        except (ExternalTaskAuthorityError, ValueError) as exc:
            raise NextActionError(
                NextActionErrorCode.PRIORITY_SOURCE_NOT_ENROLLED,
                "external context is not current at selection H",
            ) from exc
        context = fold.current
        if (
            context is None
            or context.context_ref != content["context_ref"]
            or context.fingerprint != content["context_fingerprint"]
            or context.context_logical_id != content["context_logical_id"]
            or context.project_id != content["project_id"]
            or context.task_contract_id != content["task_contract_id"]
            or context.task_contract_version != content["task_contract_version"]
            or context.context_slot_id != content["context_slot_id"]
            or context.priority_class.value != content["priority_class"]
            or context.critical_path_ordinal != content["critical_path_ordinal"]
        ):
            raise NextActionError(
                NextActionErrorCode.PRIORITY_SOURCE_NOT_ENROLLED,
                "Memory priority copies differ from independently resolved owner facts",
            )
        memory_high_watermark = int(
            await session.scalar(
                select(func.coalesce(func.max(ProjectMemoryAuthorityEventRow.event_sequence), 0))
            )
            or 0
        )
        return _ResolvedContextSelection(
            context.context_ref,
            context.fingerprint,
            latest.snapshot_ref,
            latest.snapshot_fingerprint,
            latest.owner_event_high_watermark,
            memory_high_watermark,
            context.priority_class,
            context.critical_path_ordinal,
        )

    async def _require_operational_recovery(
        self,
        session: AsyncSession,
        project_id: str,
        work_run_id: str | None,
    ) -> tuple[tuple[str, ...], int]:
        if work_run_id is None:
            raise NextActionError(
                NextActionErrorCode.RECOVERY_AUTHORITY_REQUIRED,
                "OPERATIONAL_RECOVERY requires an exact P1-4 WorkRun",
            )
        run = await session.get(WorkRunRow, work_run_id)
        if (
            run is None
            or run.project_id != project_id
            or run.workflow_state not in self._selection_policy.recovery_states
        ):
            raise NextActionError(
                NextActionErrorCode.RECOVERY_AUTHORITY_REQUIRED,
                "no current owner-backed recovery condition",
            )
        decision = await session.scalar(
            select(TransitionDecisionRow)
            .join(
                TransitionRequestRow,
                TransitionRequestRow.transition_request_id
                == TransitionDecisionRow.transition_request_id,
            )
            .where(
                TransitionRequestRow.work_run_id == work_run_id,
                TransitionDecisionRow.resulting_state == run.workflow_state,
                TransitionDecisionRow.resulting_state_version == run.state_version,
            )
            .order_by(TransitionDecisionRow.event_sequence.desc())
            .limit(1)
        )
        if decision is None:
            raise NextActionError(
                NextActionErrorCode.RECOVERY_AUTHORITY_REQUIRED,
                "current WorkRun recovery state lacks its P1-4 transition fact",
            )
        verified = await verify_historical_transition_provenance(
            session, decision.transition_request_id
        )
        if (
            verified.work_run.project_id != project_id
            or verified.work_run.work_run_id != work_run_id
            or verified.decision.transition_decision_id != decision.transition_decision_id
        ):
            raise NextActionError(
                NextActionErrorCode.RECOVERY_AUTHORITY_REQUIRED,
                "P1-4 historical recovery authority graph differs",
            )
        refs = (
            f"p1-4-work-run:{run.work_run_id}:{run.state_version}",
            f"p1-4-transition-decision:{decision.transition_decision_id}",
            f"p1-4-transition-request:{decision.transition_request_id}",
        )
        if run.workflow_state != "BLOCKED":
            return refs, 2
        blocker_projection = await session.get(P1_4BlockerProjectionRow, run.work_run_id)
        blocker = (
            await session.get(P1_4BlockerProvenanceRow, blocker_projection.blocker_ref)
            if blocker_projection is not None and blocker_projection.blocker_ref is not None
            else None
        )
        if (
            blocker_projection is None
            or blocker_projection.state != "ACTIVE"
            or blocker is None
            or blocker.blocked_epoch != run.state_version
        ):
            raise NextActionError(
                NextActionErrorCode.RECOVERY_AUTHORITY_REQUIRED,
                "BLOCKED recovery lacks exact current P1-4 blocker provenance",
            )
        if blocker.reason_code in {
            "SECURITY_BOUNDARY",
            "POLICY_CONFLICT",
            "MISSING_REQUIRED_ARTIFACT",
        }:
            rank = 1
        elif blocker.reason_code in {"BASELINE_GAP", "AUTHORITY_CONFLICT"}:
            rank = 3
        else:
            rank = 2
        return (*refs, blocker.blocker_ref), rank

    async def _verify_authoritative_inputs_as_of(
        self,
        session: AsyncSession,
        row: NextActionSelectionRow,
        evaluation: NextActionEvaluationRow,
        descriptor: NextActionDescriptorRow,
    ) -> None:
        raw_refs = evaluation.payload.get("authoritative_input_refs")
        if not isinstance(raw_refs, list):
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION,
                "authoritative input ref graph is malformed",
            )
        refs = tuple(str(item) for item in raw_refs)
        mode = evaluation.payload.get("mode")
        if mode == NextActionSelectionMode.OPERATIONAL_RECOVERY.value:
            selection_policy = await session.get(
                NextActionPolicyRow, evaluation.payload.get("selection_policy_ref")
            )
            recovery_states = (
                selection_policy.payload.get("recovery_states")
                if selection_policy is not None
                else None
            )
            if not isinstance(recovery_states, list):
                raise NextActionError(
                    NextActionErrorCode.HISTORICAL_CORRUPTION,
                    "historical selection policy recovery mapping is malformed",
                )
            prefix = "p1-4-transition-request:"
            request_refs = tuple(item[len(prefix) :] for item in refs if item.startswith(prefix))
            if len(request_refs) != 1:
                raise NextActionError(
                    NextActionErrorCode.HISTORICAL_CORRUPTION,
                    "recovery selection lacks exact P1-4 transition authority",
                )
            transition = await verify_historical_transition_provenance(session, request_refs[0])
            if (
                transition.work_run.project_id != row.project_id
                or transition.decision.resulting_state is None
                or transition.decision.resulting_state.value not in recovery_states
                or f"p1-4-transition-decision:{transition.decision.transition_decision_id}"
                not in refs
            ):
                raise NextActionError(
                    NextActionErrorCode.HISTORICAL_CORRUPTION,
                    "historical recovery authority binding differs",
                )
        elif mode == NextActionSelectionMode.CYCLE_DERIVED.value:
            raw_memory_refs = row.payload.get("memory_refs")
            if not isinstance(raw_memory_refs, list):
                raise NextActionError(
                    NextActionErrorCode.HISTORICAL_CORRUPTION,
                    "historical memory ref list is malformed",
                )
            memory_h = row.memory_authority_event_high_watermark
            context_rows: list[tuple[ProjectMemoryEntryRow, CycleMemoryReferenceRow]] = []
            if memory_h is None:
                raise NextActionError(
                    NextActionErrorCode.HISTORICAL_CORRUPTION,
                    "historical selection Memory H is absent",
                )
            for entry_id in raw_memory_refs:
                entry = await session.get(ProjectMemoryEntryRow, str(entry_id))
                if (
                    entry is None
                    or entry.project_id != row.project_id
                    or not await _memory_entry_current_at(session, entry, memory_h)
                ):
                    raise NextActionError(
                        NextActionErrorCode.HISTORICAL_CORRUPTION,
                        "historical Cycle-derived memory authority differs",
                    )
                if entry.category == "NEXT_ACTION_CONTEXT":
                    reference = await session.scalar(
                        select(CycleMemoryReferenceRow).where(
                            CycleMemoryReferenceRow.entry_id == entry.entry_id,
                            CycleMemoryReferenceRow.cycle_id == entry.cycle_id,
                            CycleMemoryReferenceRow.declaration_ordinal
                            == entry.declaration_ordinal,
                        )
                    )
                    if reference is None:
                        raise NextActionError(
                            NextActionErrorCode.HISTORICAL_CORRUPTION,
                            "historical context Cycle relation is absent",
                        )
                    context_rows.append((entry, reference))
            if len(context_rows) != 1:
                raise NextActionError(
                    NextActionErrorCode.HISTORICAL_CORRUPTION,
                    "historical selection context cardinality differs",
                )
            context_entry, context_reference = context_rows[0]
            provenance = context_reference.provenance
            if not isinstance(provenance, dict):
                raise NextActionError(
                    NextActionErrorCode.HISTORICAL_CORRUPTION,
                    "historical context provenance is malformed",
                )
            try:
                folded = await self._task_authority_verifier.verify_next_action_context(
                    context_ref=str(row.external_context_ref),
                    context_fingerprint=str(row.external_context_fingerprint),
                    introduction_event_ref=str(provenance["context_introduction_event_ref"]),
                    introduction_event_fingerprint=str(
                        provenance["context_introduction_event_fingerprint"]
                    ),
                    snapshot_ref=str(row.external_context_snapshot_ref),
                    snapshot_fingerprint=str(row.external_context_snapshot_fingerprint),
                    owner_event_high_watermark=int(row.external_context_event_high_watermark or 0),
                    require_current=False,
                )
            except (ExternalTaskAuthorityError, KeyError, TypeError, ValueError) as exc:
                raise NextActionError(
                    NextActionErrorCode.HISTORICAL_CORRUPTION,
                    "historical external context prefix differs",
                ) from exc
            normalized = context_entry.payload.get("normalized_content")
            if (
                folded.current is None
                or folded.current.context_ref != row.external_context_ref
                or folded.current.fingerprint != row.external_context_fingerprint
                or not isinstance(normalized, dict)
                or normalized.get("priority_class")
                != evaluation.payload.get("external_priority_class")
                or normalized.get("critical_path_ordinal")
                != evaluation.payload.get("enrolled_critical_path_ordinal")
                or dict(self._selection_policy.class_to_rank).get(
                    str(normalized.get("priority_class"))
                )
                != evaluation.payload.get("authoritative_priority_rank")
            ):
                raise NextActionError(
                    NextActionErrorCode.HISTORICAL_CORRUPTION,
                    "historical context/ranking equality differs",
                )
        else:
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION, "selection mode is malformed"
            )
        human_ref = evaluation.payload.get("human_judgment_ref")
        human_kind = descriptor.payload.get("required_human_input_kind")
        if human_kind == HumanInputKind.BEFORE_SELECTION.value:
            if not isinstance(human_ref, str):
                raise NextActionError(
                    NextActionErrorCode.HISTORICAL_CORRUPTION,
                    "historical BEFORE_SELECTION Judgment is absent",
                )
            judgment = await verify_historical_judgment_provenance(session, human_ref)
            judgment_run = await session.get(WorkRunRow, judgment.work_run_id)
            scope = descriptor.payload.get("scope_restrictions")
            if not isinstance(scope, dict):
                scope = {}
            if (
                judgment_run is None
                or judgment_run.project_id != row.project_id
                or judgment.owner_policy is not JudgmentOwnerPolicy.HUMAN
                or judgment.human_gate_ref is None
                or judgment.human_result_ref is None
                or (scope.get("work_run_id") and scope["work_run_id"] != judgment.work_run_id)
                or (
                    scope.get("task_contract_id")
                    and scope["task_contract_id"] != judgment.task_contract_id
                )
                or (
                    scope.get("state_version")
                    and scope["state_version"] != str(judgment.state_version)
                )
                or (
                    scope.get("target_state")
                    and scope["target_state"] != judgment.target_state.value
                )
            ):
                raise NextActionError(
                    NextActionErrorCode.HISTORICAL_CORRUPTION,
                    "historical Human authority binding differs",
                )
        elif human_ref is not None:
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION,
                "unexpected historical Judgment authority",
            )

    async def _replay_pair(
        self, session: AsyncSession, row: NextActionSelectionRow
    ) -> tuple[NextActionSelection, TaskIssuanceCandidate]:
        evaluation = await session.get(NextActionEvaluationRow, row.evaluation_id)
        proposal = await session.scalar(
            select(NextActionProposalRow).where(
                NextActionProposalRow.proposal_id == row.payload.get("proposal_id")
            )
        )
        descriptor = await session.get(NextActionDescriptorRow, row.action_ref)
        issuance = await session.scalar(
            select(TaskIssuanceCandidateRow).where(
                TaskIssuanceCandidateRow.selection_id == row.selection_id
            )
        )
        events = tuple(
            await session.scalars(
                select(NextActionAuthorityEventRow).where(
                    NextActionAuthorityEventRow.selection_id == row.selection_id
                )
            )
        )
        selected_events = tuple(item for item in events if item.event_kind == "SELECTED")
        if (
            evaluation is None
            or proposal is None
            or descriptor is None
            or issuance is None
            or len(selected_events) != 1
            or any(item.event_kind not in {"SELECTED", "WITHDRAWN"} for item in events)
        ):
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION,
                "historical selection authority graph incomplete",
            )
        if evaluation.fingerprint != canonical_hash(evaluation.payload):
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION,
                "historical ranking evaluation fingerprint differs",
            )
        proposal_fingerprint = canonical_hash(
            {
                "action_ref": proposal.action_ref,
                "parameters": proposal.payload.get("parameters"),
                "project_id": proposal.project_id,
                "proposal_id": proposal.proposal_id,
                "rationale": proposal.payload.get("rationale"),
            }
        )
        if proposal.fingerprint != proposal_fingerprint:
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION,
                "historical proposal audit fingerprint differs",
            )
        for policy_ref, fingerprint in (
            (
                str(evaluation.payload["eligibility_policy_ref"]),
                str(evaluation.payload["eligibility_policy_fingerprint"]),
            ),
            (
                str(evaluation.payload["selection_policy_ref"]),
                str(evaluation.payload["selection_policy_fingerprint"]),
            ),
        ):
            policy = await session.get(NextActionPolicyRow, policy_ref)
            owner_event = await session.scalar(
                select(NextActionOwnerEventRow).where(
                    NextActionOwnerEventRow.subject_ref == policy_ref,
                    NextActionOwnerEventRow.event_kind == "ISSUED",
                    NextActionOwnerEventRow.created_at <= row.selected_at,
                    NextActionOwnerEventRow.event_sequence
                    <= int(str(evaluation.payload.get("owner_event_high_watermark", -1))),
                )
            )
            invalid_before = await session.scalar(
                select(func.count())
                .select_from(NextActionOwnerEventRow)
                .where(
                    NextActionOwnerEventRow.subject_ref == policy_ref,
                    NextActionOwnerEventRow.event_kind.in_(("SUPERSEDED", "REVOKED")),
                    NextActionOwnerEventRow.event_sequence
                    <= int(str(evaluation.payload.get("owner_event_high_watermark", -1))),
                )
            )
            if (
                policy is None
                or policy.fingerprint != fingerprint
                or policy.payload
                != _policy_payload(
                    (
                        self._eligibility_policy
                        if policy_ref == self._eligibility_policy.policy_ref
                        else self._selection_policy
                    ),
                    (
                        "ELIGIBILITY"
                        if policy_ref == self._eligibility_policy.policy_ref
                        else "SELECTION"
                    ),
                )
                or owner_event is None
                or bool(invalid_before)
            ):
                raise NextActionError(
                    NextActionErrorCode.HISTORICAL_CORRUPTION,
                    "original selection policy validity differs",
                )
        if descriptor.fingerprint != row.payload.get("descriptor_fingerprint"):
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION, "descriptor fingerprint differs"
            )
        descriptor_enrollment = await session.scalar(
            select(NextActionOwnerEventRow).where(
                NextActionOwnerEventRow.subject_ref == row.action_ref,
                NextActionOwnerEventRow.subject_kind == "DESCRIPTOR",
                NextActionOwnerEventRow.event_kind == "ENROLLED",
                NextActionOwnerEventRow.created_at <= row.selected_at,
                NextActionOwnerEventRow.event_sequence
                <= int(str(evaluation.payload.get("owner_event_high_watermark", -1))),
            )
        )
        descriptor_invalid_before = await session.scalar(
            select(func.count())
            .select_from(NextActionOwnerEventRow)
            .where(
                NextActionOwnerEventRow.subject_ref == row.action_ref,
                NextActionOwnerEventRow.event_kind.in_(("SUPERSEDED", "REVOKED")),
                NextActionOwnerEventRow.event_sequence
                <= int(str(evaluation.payload.get("owner_event_high_watermark", -1))),
            )
        )
        if descriptor_enrollment is None or bool(descriptor_invalid_before):
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION,
                "descriptor was not valid at original issuance",
            )
        enrollment_id = evaluation.payload.get("descriptor_enrollment_id")
        enrollment = (
            await session.get(NextActionPolicyDescriptorEnrollmentRow, enrollment_id)
            if isinstance(enrollment_id, str)
            else None
        )
        if (
            enrollment is None
            or enrollment.eligibility_policy_ref != evaluation.payload.get("eligibility_policy_ref")
            or enrollment.eligibility_policy_fingerprint
            != evaluation.payload.get("eligibility_policy_fingerprint")
            or enrollment.action_ref != row.action_ref
            or enrollment.descriptor_fingerprint != descriptor.fingerprint
            or enrollment.enrolled_at > row.selected_at
        ):
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION,
                "original eligibility-policy-to-descriptor enrollment differs",
            )
        configured_descriptor = self._descriptors.get(row.action_ref)
        if configured_descriptor is not None and descriptor.payload != _descriptor_payload(
            configured_descriptor
        ):
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION,
                "descriptor immutable authority payload differs",
            )
        await self._verify_authoritative_inputs_as_of(session, row, evaluation, descriptor)
        selection = _selection_from_row(row)
        if selection.fingerprint != row.fingerprint:
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION, "selection fingerprint differs"
            )
        raw_parameters = issuance.payload["parameters"]
        if not isinstance(raw_parameters, dict):
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION,
                "issuance parameters are malformed",
            )
        candidate = TaskIssuanceCandidate(
            issuance.candidate_id,
            str(issuance.payload["selection_ref"]),
            selection.action_ref,
            {str(key): value for key, value in raw_parameters.items()},
            issuance.issuance_owner,
            HumanInputKind(
                str(
                    issuance.payload.get(
                        "required_post_issuance_human_input", HumanInputKind.NONE.value
                    )
                )
            ),
            issuance.created_at.astimezone(UTC),
        )
        return selection, candidate


async def _memory_entry_current_at(
    session: AsyncSession, entry: ProjectMemoryEntryRow, high_watermark: int
) -> bool:
    events = tuple(
        await session.scalars(
            select(ProjectMemoryAuthorityEventRow)
            .where(
                ProjectMemoryAuthorityEventRow.memory_lineage_key == entry.memory_lineage_key,
                ProjectMemoryAuthorityEventRow.event_sequence <= high_watermark,
            )
            .order_by(ProjectMemoryAuthorityEventRow.event_sequence)
        )
    )
    revision = 0
    current: str | None = None
    for event in events:
        if event.prior_revision != revision or event.new_revision != revision + 1:
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION,
                "Memory applicability history has a revision gap",
            )
        revision = event.new_revision
        if event.event_kind == "CURRENT":
            current = event.subject_entry_id
        elif event.event_kind == "SUPERSEDED":
            if current != event.subject_entry_id:
                raise NextActionError(
                    NextActionErrorCode.HISTORICAL_CORRUPTION,
                    "Memory supersession target differs",
                )
            current = event.replacement_entry_id
        elif event.event_kind in {"REVOKED", "EXPIRED"}:
            if current == event.subject_entry_id:
                current = None
        else:
            raise NextActionError(
                NextActionErrorCode.HISTORICAL_CORRUPTION,
                "Memory applicability event kind differs",
            )
    return current == entry.entry_id


async def _lock(session: AsyncSession, key: str) -> None:
    await session.execute(
        text("SELECT pg_advisory_xact_lock(hashtextextended(:key, 0))"), {"key": key}
    )


def _descriptor_payload(value: NextActionDescriptor) -> dict[str, object]:
    return {
        "action_id": value.action_ref.action_id,
        "action_version": value.action_ref.action_version,
        "allowed_selection_modes": [item.value for item in value.allowed_selection_modes],
        "authority_revision": value.authority_revision,
        "critical_path_ordinal": value.critical_path_ordinal,
        "current_projection_on_invalidation": (value.current_projection_on_invalidation.value),
        "dependency_ordinal": value.dependency_ordinal,
        "descriptor_policy_ordinal": value.descriptor_policy_ordinal,
        "effective_sequence": value.effective_sequence,
        "eligibility_policy_id": value.action_ref.eligibility_policy_id,
        "eligibility_policy_version": value.action_ref.eligibility_policy_version,
        "parameter_rules": value.parameter_rules,
        "parameter_schema_fingerprint": value.parameter_schema_fingerprint,
        "parameter_schema_id": value.parameter_schema_id,
        "parameter_schema_version": value.parameter_schema_version,
        "priority_rank": value.priority_rank,
        "priority_classification_source_hash": value.priority_classification_source_hash,
        "priority_classification_source_ref": value.priority_classification_source_ref,
        "privacy_restrictions": list(value.privacy_restrictions),
        "project_restriction": value.project_restriction,
        "required_human_input_kind": value.required_human_input_kind.value,
        "revocation_ref": value.revocation_ref,
        "scope_restrictions": value.scope_restrictions,
        "security_restrictions": list(value.security_restrictions),
        "source_authority_fingerprint": value.source_authority_fingerprint,
        "source_authority_ref": value.source_authority_ref,
        "source_authority_version": value.source_authority_version,
        "source_kind": value.source_kind.value,
        "supersedes_ref": value.supersedes_ref,
        "task_issuance_owner": value.task_issuance_owner,
        "task_template_hash": value.task_template_hash,
        "task_template_ref": value.task_template_ref,
        "canonical_payload": value.canonical_payload,
    }


def _policy_payload(
    value: NextActionEligibilityPolicy | NextActionSelectionPolicy, kind: str
) -> dict[str, object]:
    payload: dict[str, object] = {
        "authority_id": value.authority_id,
        "authority_revision": value.authority_revision,
        "authority_version": value.authority_version,
        "current_projection_on_invalidation": (value.current_projection_on_invalidation.value),
        "effective_sequence": value.effective_sequence,
        "policy_id": value.policy_id,
        "policy_kind": kind,
        "policy_version": value.policy_version,
    }
    if isinstance(value, NextActionEligibilityPolicy):
        payload["enrolled_action_bindings"] = [
            list(item) for item in value.enrolled_action_bindings
        ]
    else:
        payload["recovery_states"] = list(value.recovery_states)
        payload["class_to_rank"] = {
            priority_class: rank for priority_class, rank in value.class_to_rank
        }
    return payload


def _evaluation_payload(value: NextActionEvaluation) -> dict[str, object]:
    return {
        "eligibility_policy_fingerprint": value.eligibility_policy_fingerprint,
        "eligibility_policy_ref": value.eligibility_policy_ref,
        "human_judgment_ref": value.human_judgment_ref,
        "authoritative_input_refs": list(value.authoritative_input_refs),
        "descriptor_enrollment_id": value.descriptor_enrollment_id,
        "mode": value.mode.value,
        "operational_work_run_id": value.operational_work_run_id,
        "owner_event_high_watermark": value.owner_event_high_watermark,
        "ranked_proposal_ids": list(value.ranked_proposal_ids),
        "selection_policy_fingerprint": value.selection_policy_fingerprint,
        "selection_policy_ref": value.selection_policy_ref,
        "authoritative_priority_rank": value.authoritative_priority_rank,
        "enrolled_critical_path_ordinal": value.enrolled_critical_path_ordinal,
        "external_priority_class": value.external_priority_class,
        "external_context_ref": value.external_context_ref,
        "external_context_fingerprint": value.external_context_fingerprint,
        "external_context_owner_high_watermark": (value.external_context_owner_high_watermark),
        "memory_authority_event_high_watermark": (value.memory_authority_event_high_watermark),
    }


def _selection_payload(value: NextActionSelection) -> dict[str, object]:
    return {
        "action_id": value.action_ref.action_id,
        "action_version": value.action_ref.action_version,
        "descriptor_fingerprint": value.descriptor_fingerprint,
        "descriptor_version": value.descriptor_version,
        "memory_refs": list(value.memory_refs),
        "parameters": value.parameters,
        "proposal_id": value.proposal_id,
        "eligibility_policy_id": value.action_ref.eligibility_policy_id,
        "eligibility_policy_version": value.action_ref.eligibility_policy_version,
        "external_context_ref": value.external_context_ref,
        "external_context_fingerprint": value.external_context_fingerprint,
        "external_context_snapshot_ref": value.external_context_snapshot_ref,
        "external_context_snapshot_fingerprint": (value.external_context_snapshot_fingerprint),
        "external_context_event_high_watermark": (value.external_context_event_high_watermark),
        "memory_authority_event_high_watermark": (value.memory_authority_event_high_watermark),
    }


def _selection_from_row(row: NextActionSelectionRow) -> NextActionSelection:
    payload = row.payload
    raw_parameters = payload["parameters"]
    raw_memory_refs = payload["memory_refs"]
    if not isinstance(raw_parameters, dict) or not isinstance(raw_memory_refs, list):
        raise NextActionError(
            NextActionErrorCode.HISTORICAL_CORRUPTION,
            "selection parameters or memory refs are malformed",
        )
    return NextActionSelection(
        row.selection_id,
        row.serialized_ref.split(":", 2)[1],
        row.project_id,
        row.project_revision,
        row.evaluation_id,
        str(payload["proposal_id"]),
        ActionRef(
            str(payload["eligibility_policy_id"]),
            str(payload["eligibility_policy_version"]),
            str(payload["action_id"]),
            str(payload["action_version"]),
            str(payload["descriptor_fingerprint"]),
        ),
        str(payload["descriptor_version"]),
        str(payload["descriptor_fingerprint"]),
        {str(key): value for key, value in raw_parameters.items()},
        tuple(str(item) for item in raw_memory_refs),
        row.selected_at.astimezone(UTC),
        row.external_context_ref,
        row.external_context_fingerprint,
        row.external_context_snapshot_ref,
        row.external_context_snapshot_fingerprint,
        row.external_context_event_high_watermark,
        row.memory_authority_event_high_watermark,
    )
