from __future__ import annotations

import ast
import asyncio
from dataclasses import FrozenInstanceError, fields
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import AsyncMock

import pytest

import aiscc.self_dogfood as public
from aiscc.contracts.workflow import RuntimeMode, WorkflowState
from aiscc.judgment.models import JudgmentOwnerPolicy
from aiscc.self_dogfood.materializer import _project_body
from aiscc.task_authority.contracts import (
    IssuedTaskContractV1,
    TaskContractBodyV1,
    TaskContractError,
    VerifiedTaskContractBindingV1,
)
from aiscc.task_authority.repository import PostgresExternalTaskAuthorityRepository
from aiscc.workflow.models import RequesterType
from tests.unit.task_authority.test_task_contract_body import sample_body


def assert_exact_spec(spec, body):
    v = body.value
    source, ev = v["source_next_action"], v["evidence_binding"]
    expected = {
        "project_id": v["project_id"],
        "task_id": v["task_id"],
        "task_contract_id": v["contract_id"],
        "task_contract_version": "v" + str(v["contract_version"]),
        "task_contract_body_ref": body.body_ref,
        "task_contract_body_sha256": body.body_sha256,
        "source_selection_id": source["selection_id"],
        "source_selection_version": source["selection_version"],
        "source_action_ref": source["action_ref"],
        "source_selection_fingerprint": source["selection_fingerprint"],
        "source_descriptor_fingerprint": source["descriptor_fingerprint"],
        **v["repository_binding"],
        "goal": v["goal"],
        "non_goals": tuple(v["non_goals"]),
        "allowed_paths": tuple(v["allowed_paths"]),
        "forbidden_paths": tuple(v["forbidden_paths"]),
        "evidence_requirement_set_ref": ev["requirement_set_ref"],
        "evidence_requirement_set_fingerprint": ev["requirement_set_fingerprint"],
        "evidence_checkpoints": tuple((x["ref"], x["fingerprint"]) for x in ev["checkpoints"]),
        "human_requirement_kind": v["human_binding"]["kind"],
        "judgment_owner_policy": v["judgment_binding"]["owner_policy"],
        **v["execution_provenance"],
    }
    actual = {f.name: getattr(spec, f.name) for f in fields(spec)}
    actual["source_action_ref"] = spec.source_action_ref.serialized
    actual["evidence_checkpoints"] = tuple(
        (ref.serialized(), sha) for ref, sha in spec.evidence_checkpoints
    )
    assert actual == expected
    assert type(spec.runtime_mode) is RuntimeMode
    assert type(spec.judgment_owner_policy) is JudgmentOwnerPolicy


def test_private_shape_conversion_is_deterministic_and_recursively_immutable():
    # Pure shape coverage is NOT evidence of durable verification; integration uses real owners.
    value = sample_body()
    body = TaskContractBodyV1(value)
    spec = _project_body(body)
    assert_exact_spec(spec, body)
    assert spec == _project_body(TaskContractBodyV1.from_bytes(body.canonical_body))
    assert hash(spec) == hash(_project_body(body))
    value["non_goals"].append("changed")
    value["evidence_binding"]["checkpoints"][0]["fingerprint"] = "0" * 64
    assert_exact_spec(spec, body)
    with pytest.raises(FrozenInstanceError):
        spec.goal = "changed"
    with pytest.raises(TypeError):
        spec.allowed_paths[0] = "changed"
    with pytest.raises(FrozenInstanceError):
        spec.evidence_checkpoints[0][0].checkpoint_id = "changed"
    with pytest.raises(TypeError):
        public.SelfDogfoodTaskSpec()


@pytest.mark.parametrize("value", [{}, True, VerifiedTaskContractBindingV1(None, True)])
def test_caller_currentness_claim_cannot_materialize(value):
    repo = PostgresExternalTaskAuthorityRepository(None)
    with pytest.raises(TaskContractError, match="issued receipt"):
        asyncio.run(public.materialize_task_spec(repo, value, {}, "wrong"))


@pytest.mark.parametrize(
    "reason",
    [
        "repository mismatch",
        "base mismatch",
        "wrong NextAction",
        "revoked",
        "non-current",
        "TASKCONTRACT_V1_UNSUPPORTED_NEXT_ACTION_SOURCE",
    ],
)
def test_verifier_denial_propagates_without_projection(monkeypatch, reason):
    repo = PostgresExternalTaskAuthorityRepository(None)
    body = TaskContractBodyV1(sample_body())
    receipt = IssuedTaskContractV1(body, "ref", "hash", "event", "snapshot", "hash", 1)
    denial = AsyncMock(side_effect=TaskContractError(reason))
    monkeypatch.setattr(repo, "verify_task_contract", denial)
    expected = {"repository_id": "expected"}
    with pytest.raises(TaskContractError, match=reason):
        asyncio.run(public.materialize_task_spec(repo, receipt, expected, "expected-action"))
    denial.assert_awaited_once_with(
        receipt,
        require_current=True,
        expected_repository_binding=expected,
        expected_next_action_ref="expected-action",
    )


def test_exact_ready_adapter_and_explicit_time():
    spec = _project_body(TaskContractBodyV1(sample_body()))
    args = dict(
        work_run_id="run-1",
        transition_request_id="request-1",
        requester_id="system",
        created_at=datetime(2026, 9, 14, tzinfo=UTC),
    )
    request = public.build_ready_request(spec, **args)
    assert public.build_ready_request(spec, **args) == request
    assert (request.project_id, request.task_contract_id, request.task_contract_version) == (
        spec.project_id,
        spec.task_contract_id,
        spec.task_contract_version,
    )
    assert (request.observed_state, request.observed_state_version) == (None, 0)
    assert request.target_state is WorkflowState.READY
    assert request.runtime_mode is RuntimeMode.OWNER_SELF_DOGFOOD
    assert request.requester_type is RequesterType.SYSTEM
    assert not request.evidence_refs and not request.human_result_refs and not request.judgment_refs
    assert request.created_at == args["created_at"]
    with pytest.raises(TypeError):
        public.build_ready_request(spec, **{k: v for k, v in args.items() if k != "created_at"})
    with pytest.raises(ValueError):
        public.build_ready_request(spec, **(args | {"created_at": datetime(2026, 9, 14)}))


@pytest.mark.parametrize("field", ["work_run_id", "transition_request_id", "requester_id"])
@pytest.mark.parametrize("value", ["", " ", "../run", "run\n", "r" * 97, "é", None])
def test_invalid_operation_identity_denied(field, value):
    args = dict(
        work_run_id="run",
        transition_request_id="request",
        requester_id="system",
        created_at=datetime(2026, 9, 14, tzinfo=UTC),
    )
    with pytest.raises(TaskContractError, match="noncanonical"):
        public.build_ready_request(
            _project_body(TaskContractBodyV1(sample_body())), **(args | {field: value})
        )


def test_public_surface_has_no_writer_duplicate_enums_or_side_effect_capability():
    assert set(public.__all__) == {
        "SelfDogfoodTaskSpec",
        "materialize_task_spec",
        "build_ready_request",
        "enter_ready",
    }
    for path in Path(public.__file__).parent.glob("*.py"):
        content = path.read_text(encoding="utf-8")
        assert "_ExternalTaskAuthorityWriter" not in content
        tree = ast.parse(content)
        assert not any(
            isinstance(x, ast.ClassDef)
            and x.name
            in {
                "WorkflowState",
                "RuntimeMode",
                "JudgmentOwnerPolicy",
                "TransitionDecision",
                "WorkRun",
            }
            for x in ast.walk(tree)
        )
        assert not any(
            isinstance(x, ast.Attribute)
            and x.attr
            in {
                "issue_task_contract",
                "revoke_task_contract",
                "execute",
                "issue",
                "write_text",
                "write_bytes",
                "mkdir",
                "connect",
                "create_task",
            }
            for x in ast.walk(tree)
        )
