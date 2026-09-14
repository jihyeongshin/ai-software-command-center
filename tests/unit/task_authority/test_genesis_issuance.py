import pytest

from aiscc.task_authority.contracts import TaskContractBodyV1, TaskContractError
from tests.unit.task_authority.test_task_contract_body import sample_body


def genesis_body():
    value = sample_body()
    source = value["source_next_action"]
    source["action_ref"] = source["action_ref"].replace(
        "open-cycle-derived-task-issuance", "open-self-dogfood-genesis-task-issuance"
    )
    source["external_context"] = None
    source["genesis_authority"] = {
        "authority_ref": "self-dogfood-genesis:v1:genesis",
        "fingerprint": "b" * 64,
        "phase_id": "P2-4",
    }
    return value


def test_genesis_body_is_closed_and_has_no_cycle_context():
    value = genesis_body()
    body = TaskContractBodyV1(value)
    assert body.value["source_next_action"]["external_context"] is None
    assert TaskContractBodyV1(body.value).body_sha256 == body.body_sha256
    for mutate in (
        lambda v: v["source_next_action"]["genesis_authority"].update(source_cycle_id="fake"),
        lambda v: v["source_next_action"].update(
            external_context=sample_body()["source_next_action"]["external_context"]
        ),
        lambda v: v.update(contract_version=2),
        lambda v: v["source_next_action"].pop("genesis_authority"),
        lambda v: v["source_next_action"].update(
            action_ref=sample_body()["source_next_action"]["action_ref"]
        ),
    ):
        value = genesis_body()
        mutate(value)
        with pytest.raises((TaskContractError, ValueError)):
            TaskContractBodyV1(value)
