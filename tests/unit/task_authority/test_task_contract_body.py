from __future__ import annotations

import json

import pytest

from aiscc.task_authority.contracts import TaskContractBodyV1, TaskContractError, plain


def sample_body():
    return dict(
        schema_id="AISCC-TASKCONTRACT-BODY-V1",
        owner="EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY",
        project_id="project",
        contract_id="contract",
        task_id="task",
        contract_version=1,
        goal="Bounded implementation",
        non_goals=["No external access"],
        allowed_paths=["src/**"],
        forbidden_paths=["secret/**"],
        authority_refs=[],
        evidence_binding=dict(
            requirement_set_ref="set@v1",
            requirement_set_fingerprint="1" * 64,
            checkpoints=[dict(ref="checkpoint@v1", fingerprint="2" * 64)],
        ),
        human_binding=dict(
            kind="NOT_REQUIRED",
            authority_policy_ref="human-policy",
            authority_policy_version="v1",
            required_uses=[],
            purpose_id=None,
            purpose_version=None,
            owner_selector_fingerprint=None,
        ),
        judgment_binding=dict(
            owner_policy="SYSTEM_DETERMINISTIC",
            policies=[
                dict(
                    policy_id="accepted-policy",
                    policy_version="v1",
                    source_state="ADMISSION_PENDING",
                    target_state="ACCEPTED",
                    requires_human_result=False,
                    requires_post_human_evidence=True,
                    deterministic_kind="ACCEPTED",
                    evidence_basis_kind="SATISFIED_ATTESTATION",
                    evidence_checkpoint_ref="checkpoint@v1",
                    evidence_requirement_set_ref="set@v1",
                )
            ],
        ),
        source_next_action=dict(
            selection_id="selected",
            selection_version="v1",
            selection_fingerprint="3" * 64,
            project_revision=1,
            action_ref="p1-8-action:eligibility:v1:open-cycle-derived-task-issuance:v1:" + "4" * 64,
            descriptor_fingerprint="4" * 64,
            issuance_candidate_id="candidate",
            issuance_candidate_fingerprint="5" * 64,
            external_context=dict(
                context_ref="context",
                context_fingerprint="6" * 64,
                introduction_event_ref="event",
                introduction_event_fingerprint="7" * 64,
                snapshot_ref="snapshot",
                snapshot_fingerprint="8" * 64,
                owner_event_high_watermark=1,
            ),
        ),
        repository_binding=dict(
            repository_id="repo", repository_root="C:/task-repository", base_commit="9" * 40
        ),
        execution_provenance=dict(
            runtime_mode="OWNER_SELF_DOGFOOD",
            cycle_execution_mode="AISCC_SELF_DOGFOOD",
            orchestrator_version="v1",
            orchestrator_commit="a" * 40,
        ),
        predecessor=None,
    )


def test_canonical_body_roundtrip_immutable_and_96_id_ref():
    value = sample_body()
    value.update(project_id="p" * 96, contract_id="c" * 96)
    body = TaskContractBodyV1(value)
    assert len(body.body_ref) == 93 and body.body_ref.isascii()
    assert body == TaskContractBodyV1.from_bytes(body.canonical_body)
    assert not body.canonical_body.endswith(b"\n")
    value["goal"] = "mutated caller"
    assert body.value["goal"] != "mutated caller"
    with pytest.raises(TypeError):
        body.value["evidence_binding"]["checkpoints"][0]["ref"] = "forged"
    changed = TaskContractBodyV1(plain(body.value) | dict(goal="different goal"))
    assert changed.body_ref == body.body_ref and changed.body_sha256 != body.body_sha256


@pytest.mark.parametrize(
    "path",
    [
        "../escape",
        "C:/escape",
        "/absolute",
        "x\\y",
        "src/../../x",
        "src//x",
        "src/NUL.txt",
        "src/trailing.",
        "src/%2e%2e/x",
        "src/*",
        "src/./x",
    ],
)
def test_scope_path_escape_denied(path):
    value = sample_body()
    value["allowed_paths"] = [path]
    with pytest.raises(ValueError):
        TaskContractBodyV1(value)


@pytest.mark.parametrize(
    "change",
    [
        {"contract_version": True},
        {"contract_version": 1.0},
        {"contract_version": 9007199254740992},
        {"project_id": "p" * 97},
        {"goal": "e\u0301"},
        {"goal": ""},
        {"goal": "x" * 16385},
        {"extra": "unknown"},
        {"predecessor": {"contract_version": 0, "body_sha256": "0" * 64}},
        {"allowed_paths": ["src/**"], "forbidden_paths": ["SRC/private/**"]},
        {"allowed_paths": ["src/A.py", "src/a.py"]},
    ],
)
def test_closed_schema_domains_fail_closed(change):
    with pytest.raises(ValueError):
        TaskContractBodyV1(sample_body() | change)


@pytest.mark.parametrize("variant", ["whitespace", "duplicate", "unknown", "bom"])
def test_noncanonical_encoded_bodies_denied(variant):
    body = TaskContractBodyV1(sample_body())
    encoded = body.canonical_body
    if variant == "whitespace":
        encoded += b"\n"
    elif variant == "duplicate":
        encoded = b'{"goal":"duplicate",' + encoded[1:]
    elif variant == "unknown":
        encoded = json.dumps(sample_body() | {"unexpected": 1}).encode()
    else:
        encoded = b"\xef\xbb\xbf" + encoded
    with pytest.raises(ValueError):
        TaskContractBodyV1.from_bytes(encoded)


def test_one_mib_limit_and_legacy_policy_shape_rejected():
    value = sample_body()
    value["non_goals"] = [str(i) + "x" * 4090 for i in range(260)]
    with pytest.raises(TaskContractError, match="byte limit"):
        TaskContractBodyV1(value)
    value = sample_body()
    value["human_binding"]["policy_fingerprint"] = "0" * 64
    with pytest.raises(ValueError):
        TaskContractBodyV1(value)
