from __future__ import annotations

from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.human.authority import HumanGateReservationAuthority, HumanPrincipalAuthority
from aiscc.judgment.authority import JudgmentPolicyAuthority
from aiscc.judgment.models import JudgmentEvidenceBasisKind, JudgmentKind, JudgmentOwnerPolicy
from aiscc.task_authority.contracts import IssuedTaskContractV1, TaskContractError, plain
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository
from aiscc.workflow.guards import P1_4GuardAuthority
from aiscc.workflow.models import GuardId

_FACTORY = object()


def _policy_arguments(body, entry):
    args = plain(entry)
    for field in ("source_state", "target_state"):
        args[field] = WorkflowState(args[field])
    args["owner_policy"] = JudgmentOwnerPolicy(body.value["judgment_binding"]["owner_policy"])
    for field, kind in (
        ("deterministic_kind", JudgmentKind),
        ("evidence_basis_kind", JudgmentEvidenceBasisKind),
    ):
        if args[field] is not None:
            args[field] = kind(args[field])
    args.update(
        task_contract_id=body.value["contract_id"],
        task_contract_version="v" + str(body.value["contract_version"]),
    )
    return args


def _request_matches(body, request):
    v = body.value
    return (
        request.project_id == v["project_id"]
        and request.task_contract_id == v["contract_id"]
        and request.task_contract_version == "v" + str(v["contract_version"])
        and request.runtime_mode is RuntimeMode.OWNER_SELF_DOGFOOD
        and request.observed_state is None
        and request.observed_state_version == 0
        and request.target_state is WorkflowState.READY
    )


class TaskContractReadyParticipant:
    """Task adapter; P1-4 owns facts and the only READY mutation."""

    def __init__(
        self, token, repository, receipt, request, facts, reservation, principal, policies
    ):
        if token is not _FACTORY:
            raise TaskContractError("use verified TaskContract READY composition")
        self._repository, self._receipt, self._request, self._facts = (
            repository,
            receipt,
            request,
            facts,
        )
        self.reservation_authority = reservation
        self.human_principal_authority = principal
        self.judgment_policies = tuple(policies)

    def facts(self, request):
        if request != self._request:
            raise TaskContractError("READY request differs")
        return self._facts

    async def prepare(self, session, request, current):
        if (
            current is not None
            or request != self._request
            or not _request_matches(self._receipt.body, request)
        ):
            raise TaskContractError("new READY request binding differs")
        body = self._receipt.body
        await self._repository.verify_task_contract(
            self._receipt,
            require_current=True,
            expected_repository_binding=body.value["repository_binding"],
            expected_next_action_ref=body.value["source_next_action"]["action_ref"],
            session=session,
        )
        entries = body.value["judgment_binding"]["policies"]
        if len(entries) != len(self.judgment_policies):
            raise TaskContractError("prepared Judgment configuration differs")
        for entry, policy in zip(entries, self.judgment_policies, strict=True):
            if any(getattr(policy, k) != v for k, v in _policy_arguments(body, entry).items()):
                raise TaskContractError("prepared Judgment configuration differs")
        # No future transition request, Human authentication, gate or Judgment fact.

    def after_evaluation(self, request):
        if request != self._request:
            raise TaskContractError("READY evaluation request differs")

    async def after_decision(self, session, request, evaluation, decision, current):
        del session, request, evaluation, decision, current


async def prepare_task_contract_ready(
    repository, receipt, request, *, system_authority, judgment_policy_authority
):
    if not isinstance(system_authority, P1_4GuardAuthority) or not isinstance(
        judgment_policy_authority, JudgmentPolicyAuthority
    ):
        raise TaskContractError("existing owner composition required")
    if not isinstance(repository, PostgresExternalTaskAuthorityRepository) or not isinstance(
        receipt, IssuedTaskContractV1
    ):
        raise TaskContractError("existing verified Task authority repository and receipt required")
    body = receipt.body
    if not _request_matches(body, request):
        raise TaskContractError("only exact fresh READY is supported")
    await repository.verify_task_contract(
        receipt,
        require_current=True,
        expected_repository_binding=body.value["repository_binding"],
        expected_next_action_ref=body.value["source_next_action"]["action_ref"],
    )
    # Existing owner registration is outside READY's run transaction and idempotent.
    policies = []
    for entry in body.value["judgment_binding"]["policies"]:
        policies.append(await judgment_policy_authority.register(**_policy_arguments(body, entry)))
    human = body.value["human_binding"]
    uses = frozenset(
        (
            body.value["contract_id"],
            "v" + str(body.value["contract_version"]),
            WorkflowState(x["source_state"]),
            WorkflowState(x["target_state"]),
        )
        for x in human["required_uses"]
    )
    reservation = HumanGateReservationAuthority(
        uses,
        authority_policy_ref=human["authority_policy_ref"],
        authority_policy_version=human["authority_policy_version"],
    )
    roles = repository._contract_composition()[5]
    principal = HumanPrincipalAuthority(allowed_roles_by_selector=roles)
    locator = "task-contract-admission:v1:" + body.body_sha256 + ":" + receipt.snapshot_ref
    facts = tuple(
        system_authority.issue(
            guard_id=g,
            satisfied=True,
            reason="TASKCONTRACT_BODY_VERIFIED",
            authority_ref=locator,
            request=request,
        )
        for g in (GuardId.G_CONTRACT, GuardId.G_SCOPE, GuardId.G_RUNTIME_CONTEXT)
    )
    return TaskContractReadyParticipant(
        _FACTORY, repository, receipt, request, facts, reservation, principal, policies
    )
