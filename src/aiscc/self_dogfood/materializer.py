"""Current TaskContract projection and existing-owner READY composition only."""

from collections.abc import Mapping
from datetime import datetime

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.evidence.models import EvidenceCheckpointRef
from aiscc.judgment.authority import JudgmentPolicyAuthority
from aiscc.judgment.models import JudgmentOwnerPolicy
from aiscc.persistence import PostgresTransitionRepository
from aiscc.self_dogfood.models import SelfDogfoodTaskSpec
from aiscc.task_authority.contracts import (
    ID,
    IssuedTaskContractV1,
    TaskContractBodyV1,
    TaskContractError,
    action_claim,
)
from aiscc.task_authority.ready import prepare_task_contract_ready
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository
from aiscc.workflow.guards import P1_4GuardAuthority
from aiscc.workflow.models import (
    DecisionOutcome,
    RequesterType,
    TransitionDecision,
    TransitionRequest,
)


def _project_body(body: TaskContractBodyV1) -> SelfDogfoodTaskSpec:
    # Private shape conversion, called only after durable CURRENT verification.
    value = body.value
    source = value["source_next_action"]
    evidence = value["evidence_binding"]
    fields = {
        "project_id": value["project_id"],
        "task_id": value["task_id"],
        "task_contract_id": value["contract_id"],
        "task_contract_version": "v" + str(value["contract_version"]),
        "task_contract_body_ref": body.body_ref,
        "task_contract_body_sha256": body.body_sha256,
        "source_selection_id": source["selection_id"],
        "source_selection_version": source["selection_version"],
        "source_action_ref": action_claim(source["action_ref"]),
        "source_selection_fingerprint": source["selection_fingerprint"],
        "source_descriptor_fingerprint": source["descriptor_fingerprint"],
        **value["repository_binding"],
        "goal": value["goal"],
        "non_goals": tuple(value["non_goals"]),
        "allowed_paths": tuple(value["allowed_paths"]),
        "forbidden_paths": tuple(value["forbidden_paths"]),
        "evidence_requirement_set_ref": evidence["requirement_set_ref"],
        "evidence_requirement_set_fingerprint": evidence["requirement_set_fingerprint"],
        "evidence_checkpoints": tuple(
            (EvidenceCheckpointRef(*entry["ref"].rsplit("@", 1)), entry["fingerprint"])
            for entry in evidence["checkpoints"]
        ),
        "human_requirement_kind": value["human_binding"]["kind"],
        "judgment_owner_policy": JudgmentOwnerPolicy(value["judgment_binding"]["owner_policy"]),
        **value["execution_provenance"],
        "runtime_mode": RuntimeMode(value["execution_provenance"]["runtime_mode"]),
    }
    spec = object.__new__(SelfDogfoodTaskSpec)
    for name, item in fields.items():
        object.__setattr__(spec, name, item)
    return spec


async def materialize_task_spec(
    task_authority_repository: PostgresExternalTaskAuthorityRepository,
    issued_receipt: IssuedTaskContractV1,
    expected_repository_binding: Mapping[str, str],
    expected_next_action_ref: str,
) -> SelfDogfoodTaskSpec:
    if not isinstance(task_authority_repository, PostgresExternalTaskAuthorityRepository) or not (
        isinstance(issued_receipt, IssuedTaskContractV1)
    ):
        raise TaskContractError("existing durable repository and issued receipt required")
    verified = await task_authority_repository.verify_task_contract(
        issued_receipt,
        require_current=True,
        expected_repository_binding=expected_repository_binding,
        expected_next_action_ref=expected_next_action_ref,
    )
    return _project_body(verified.issued.body)


def build_ready_request(
    spec: SelfDogfoodTaskSpec,
    *,
    work_run_id: str,
    transition_request_id: str,
    requester_id: str,
    created_at: datetime,
) -> TransitionRequest:
    """Build a proposal, not an authorization; time/IDs are explicit for exact retry."""
    if not isinstance(spec, SelfDogfoodTaskSpec):
        raise TaskContractError("materialized spec required")
    for value in (work_run_id, transition_request_id, requester_id):
        if not isinstance(value, str) or ID.fullmatch(value) is None:
            raise TaskContractError("noncanonical local operation ID")
    return TransitionRequest(
        transition_request_id=transition_request_id,
        project_id=spec.project_id,
        task_contract_id=spec.task_contract_id,
        task_contract_version=spec.task_contract_version,
        work_run_id=work_run_id,
        observed_state=None,
        observed_state_version=0,
        target_state=WorkflowState.READY,
        requester_identity=requester_id,
        requester_type=RequesterType.SYSTEM,
        runtime_mode=RuntimeMode.OWNER_SELF_DOGFOOD,
        created_at=created_at,
    )


async def enter_ready(
    task_authority_repository: PostgresExternalTaskAuthorityRepository,
    issued_receipt: IssuedTaskContractV1,
    expected_repository_binding: Mapping[str, str],
    expected_next_action_ref: str,
    *,
    transition_repository: PostgresTransitionRepository,
    system_authority: P1_4GuardAuthority,
    judgment_policy_authority: JudgmentPolicyAuthority,
    work_run_id: str,
    transition_request_id: str,
    requester_id: str,
    created_at: datetime,
) -> TransitionDecision:
    """Reverify the receipt; a caller's view alone can never authorize READY."""
    if not isinstance(transition_repository, PostgresTransitionRepository):
        raise TaskContractError("existing P1-4 repository required")
    spec = await materialize_task_spec(
        task_authority_repository,
        issued_receipt,
        expected_repository_binding,
        expected_next_action_ref,
    )
    request = build_ready_request(
        spec,
        work_run_id=work_run_id,
        transition_request_id=transition_request_id,
        requester_id=requester_id,
        created_at=created_at,
    )
    participant = await prepare_task_contract_ready(
        task_authority_repository,
        issued_receipt,
        request,
        system_authority=system_authority,
        judgment_policy_authority=judgment_policy_authority,
    )
    decision = await transition_repository.decide(request, (), transaction_participant=participant)
    if (
        decision.outcome is not DecisionOutcome.ADMITTED
        or decision.resulting_state is not WorkflowState.READY
        or decision.resulting_state_version != 1
    ):
        raise TaskContractError("existing owners did not admit exact READY v1")
    return decision
