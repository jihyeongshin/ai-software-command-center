from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any

from aiscc.contracts.canonical_json import canonical_json_bytes
from aiscc.contracts.workflow import WorkflowState
from aiscc.workflow.matrix import TRANSITION_MATRIX

SCHEMA = "AISCC-TASKCONTRACT-BODY-V1"
OWNER = "EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY"
HEX = re.compile(r"[0-9a-f]{64}\Z")
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,95}\Z")
FIELDS = frozenset(
    [
        "schema_id",
        "owner",
        "project_id",
        "contract_id",
        "task_id",
        "contract_version",
        "goal",
        "non_goals",
        "allowed_paths",
        "forbidden_paths",
        "authority_refs",
        "evidence_binding",
        "human_binding",
        "judgment_binding",
        "source_next_action",
        "repository_binding",
        "execution_provenance",
        "predecessor",
    ]
)


class TaskContractError(ValueError):
    """Fail-closed whole-contract validation or durable authority failure."""


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def closed(value: Any, fields: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value) != set(fields.split()):
        raise TaskContractError("closed object fields differ")
    return value


def string(value: Any, maximum: int = 1024) -> str:
    if (
        not isinstance(value, str)
        or not value.strip()
        or len(value.encode()) > maximum
        or unicodedata.normalize("NFC", value) != value
        or any(ord(c) < 32 for c in value)
    ):
        raise TaskContractError("invalid NFC string")
    return value


def fingerprint(value: Any) -> str:
    if not isinstance(value, str) or HEX.fullmatch(value) is None:
        raise TaskContractError("invalid SHA-256")
    return value


def sequence(value: Any, *, nonempty: bool = True) -> list[Any]:
    if not isinstance(value, (list, tuple)) or (nonempty and not value):
        raise TaskContractError("invalid array")
    return list(value)


def immutable(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({k: immutable(v) for k, v in value.items()})
    if isinstance(value, list):
        return tuple(immutable(v) for v in value)
    return value


def plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {k: plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    return value


def _paths(value: Any) -> list[str]:
    paths = sequence(value)
    if paths != sorted(set(paths)) or len({p.casefold() for p in paths}) != len(paths):
        raise TaskContractError("scope ordering/collision")
    for path in paths:
        string(path)
        base = path[:-3] if path.endswith("/**") else path
        for part in base.split("/"):
            if (
                not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", part)
                or part.endswith(".")
                or part.split(".")[0].upper()
                in {
                    "CON",
                    "PRN",
                    "AUX",
                    "NUL",
                    *(f"COM{i}" for i in range(1, 10)),
                    *(f"LPT{i}" for i in range(1, 10)),
                }
            ):
                raise TaskContractError("unsafe scope selector")
    return paths


def _overlap(a: str, b: str) -> bool:
    ar, br = a.endswith("/**"), b.endswith("/**")
    x, y = (a[:-3] if ar else a).casefold(), (b[:-3] if br else b).casefold()
    return x == y or (ar and y.startswith(x + "/")) or (br and x.startswith(y + "/"))


def _refs(value: Any, nonempty: bool) -> None:
    refs = sequence(value, nonempty=nonempty)
    for ref in refs:
        closed(ref, "ref fingerprint")
        string(ref["ref"])
        fingerprint(ref["fingerprint"])
    keys = [r["ref"] for r in refs]
    if keys != sorted(set(keys)):
        raise TaskContractError("reference ordering/duplicate")


def _policies(body: Mapping[str, Any]) -> None:
    human = closed(
        body["human_binding"],
        "kind authority_policy_ref authority_policy_version required_uses purpose_id "
        "purpose_version owner_selector_fingerprint",
    )
    string(human["authority_policy_ref"], 160)
    string(human["authority_policy_version"], 64)
    uses = sequence(human["required_uses"], nonempty=False)
    pairs = []
    for use in uses:
        closed(use, "source_state target_state")
        pair = (WorkflowState(use["source_state"]), WorkflowState(use["target_state"]))
        if pair not in TRANSITION_MATRIX:
            raise TaskContractError("unknown Human transition use")
        pairs.append(tuple(x.value for x in pair))
    if pairs != sorted(set(pairs)):
        raise TaskContractError("Human use ordering")
    required = human["kind"] == "REQUIRED"
    if human["kind"] not in {"REQUIRED", "NOT_REQUIRED"}:
        raise TaskContractError("Human kind missing")
    bypass = {
        ("RUNNING", "REWORK_REQUIRED"),
        ("ADMISSION_PENDING", "REWORK_REQUIRED"),
        ("ADMISSION_PENDING", "ACCEPTED"),
        ("ADMISSION_PENDING", "REJECTED"),
        ("BLOCKED", "REWORK_REQUIRED"),
        ("REWORK_REQUIRED", "REJECTED"),
    }
    opens = {("ADMISSION_PENDING", "HUMAN_REQUIRED"), ("REWORK_REQUIRED", "HUMAN_REQUIRED")}
    if required:
        if human["purpose_id"] != "P1_7_WORK_RESULT_REVIEW" or human["purpose_version"] != "v1":
            raise TaskContractError("Human purpose differs")
        string(human["owner_selector_fingerprint"], 160)
        if not set(pairs) & opens or not bypass <= set(pairs) or not set(pairs) <= bypass | opens:
            raise TaskContractError("Human bypass coverage incomplete")
    elif pairs or any(
        human[k] is not None
        for k in ("purpose_id", "purpose_version", "owner_selector_fingerprint")
    ):
        raise TaskContractError("NOT_REQUIRED configuration differs")
    judgment = closed(body["judgment_binding"], "owner_policy policies")
    owner = judgment["owner_policy"]
    if (
        owner not in {"HUMAN", "COMMAND_CENTER", "SYSTEM_DETERMINISTIC"}
        or (owner == "HUMAN") != required
    ):
        raise TaskContractError("Human/Judgment owner conflict")
    keys, ids, transitions = [], set(), set()
    for policy in sequence(judgment["policies"]):
        closed(
            policy,
            "policy_id policy_version source_state target_state requires_human_result "
            "requires_post_human_evidence deterministic_kind evidence_basis_kind "
            "evidence_checkpoint_ref evidence_requirement_set_ref",
        )
        if (
            ID.fullmatch(string(policy["policy_id"], 96)) is None
            or re.fullmatch(
                r"[A-Za-z0-9][A-Za-z0-9_.-]{0,63}", string(policy["policy_version"], 64)
            )
            is None
        ):
            raise TaskContractError("Judgment policy identity")
        source, target = (
            WorkflowState(policy["source_state"]),
            WorkflowState(policy["target_state"]),
        )
        guards = TRANSITION_MATRIX.get((source, target), ())
        human_result_use = any(
            getattr(g, "value", g) in {"G_HUMAN_APPROVED", "G_HUMAN_REWORK", "G_HUMAN_REJECTED"}
            for g in guards
        )
        if human_result_use != required:
            raise TaskContractError("Judgment Human transition use differs")
        if not any(str(getattr(g, "value", g)).startswith("G_JUDGMENT_") for g in guards):
            raise TaskContractError("not a Judgment transition use")
        if (
            type(policy["requires_human_result"]) is not bool
            or type(policy["requires_post_human_evidence"]) is not bool
            or policy["requires_human_result"] != required
        ):
            raise TaskContractError("Judgment Human flag conflict")
        kind = policy["deterministic_kind"]
        if (kind is not None) != (owner == "SYSTEM_DETERMINISTIC") or (
            kind is not None
            and {
                "ACCEPTED": "ACCEPTED",
                "REJECTED": "REJECTED",
                "HOLD_REWORK_REQUIRED": "REWORK_REQUIRED",
            }.get(kind)
            != target.value
        ):
            raise TaskContractError("deterministic Judgment target conflict")
        basis = policy["evidence_basis_kind"]
        refs = [policy["evidence_checkpoint_ref"], policy["evidence_requirement_set_ref"]]
        if basis is None:
            if refs != [None, None]:
                raise TaskContractError("partial evidence basis")
        else:
            if basis not in {"SATISFIED_ATTESTATION", "UNSATISFIED_SET_EVALUATION"}:
                raise TaskContractError("unknown evidence basis")
            for ref in refs:
                string(ref)
            if (
                refs[0] not in {c["ref"] for c in body["evidence_binding"]["checkpoints"]}
                or refs[1] != body["evidence_binding"]["requirement_set_ref"]
            ):
                raise TaskContractError("evidence binding mismatch")
            if basis == "SATISFIED_ATTESTATION" and not policy["requires_post_human_evidence"]:
                raise TaskContractError("satisfied evidence flag")
            if basis == "UNSATISFIED_SET_EVALUATION" and (
                owner != "SYSTEM_DETERMINISTIC"
                or kind != "HOLD_REWORK_REQUIRED"
                or policy["requires_post_human_evidence"]
            ):
                raise TaskContractError("unsatisfied evidence conflict")
        identity = (policy["policy_id"], policy["policy_version"])
        if identity in ids or (source, target) in transitions:
            raise TaskContractError("duplicate Judgment identity/use")
        ids.add(identity)
        transitions.add((source, target))
        keys.append((source.value, target.value, *identity))
    if keys != sorted(keys):
        raise TaskContractError("Judgment ordering")


@dataclass(frozen=True, init=False)
class TaskContractBodyV1:
    canonical_body: bytes

    def __init__(self, value: Mapping[str, Any]) -> None:
        body = plain(value)
        if (
            not isinstance(body, dict)
            or set(body) != FIELDS
            or body["schema_id"] != SCHEMA
            or body["owner"] != OWNER
        ):
            raise TaskContractError("body schema/owner/fields differ")
        for k in ("project_id", "contract_id", "task_id"):
            if ID.fullmatch(string(body[k], 96)) is None:
                raise TaskContractError("invalid local ID")
        version = body["contract_version"]
        if type(version) is not int or not 1 <= version <= 9007199254740991:
            raise TaskContractError("invalid contract version")
        string(body["goal"], 16384)
        ng = sequence(body["non_goals"])
        for value in ng:
            string(value, 4096)
        if len(set(ng)) != len(ng):
            raise TaskContractError("duplicate non-goals")
        allowed, forbidden = _paths(body["allowed_paths"]), _paths(body["forbidden_paths"])
        if any(_overlap(a, b) for a in allowed for b in forbidden):
            raise TaskContractError("scope intersection")
        _refs(body["authority_refs"], False)
        evidence = closed(
            body["evidence_binding"], "requirement_set_ref requirement_set_fingerprint checkpoints"
        )
        string(evidence["requirement_set_ref"])
        fingerprint(evidence["requirement_set_fingerprint"])
        _refs(evidence["checkpoints"], True)
        repo = closed(body["repository_binding"], "repository_id repository_root base_commit")
        string(repo["repository_id"])
        string(repo["repository_root"], 4096)
        if re.fullmatch(r"[0-9a-f]{40}", string(repo["base_commit"])) is None:
            raise TaskContractError("invalid base commit")
        provenance = closed(
            body["execution_provenance"],
            "runtime_mode cycle_execution_mode orchestrator_version orchestrator_commit",
        )
        if (
            provenance["runtime_mode"] != "OWNER_SELF_DOGFOOD"
            or provenance["cycle_execution_mode"] != "AISCC_SELF_DOGFOOD"
        ):
            raise TaskContractError("invalid execution provenance")
        string(provenance["orchestrator_version"], 160)
        if re.fullmatch(r"[0-9a-f]{40}", string(provenance["orchestrator_commit"])) is None:
            raise TaskContractError("invalid orchestrator commit")
        src = closed(
            body["source_next_action"],
            "selection_id selection_version selection_fingerprint project_revision "
            "action_ref descriptor_fingerprint issuance_candidate_id "
            "issuance_candidate_fingerprint external_context",
        )
        for k in ("selection_id", "selection_version", "action_ref", "issuance_candidate_id"):
            string(src[k])
        for k in (
            "selection_fingerprint",
            "descriptor_fingerprint",
            "issuance_candidate_fingerprint",
        ):
            fingerprint(src[k])
        if (
            type(src["project_revision"]) is not int
            or not 1 <= src["project_revision"] <= 9007199254740991
        ):
            raise TaskContractError("invalid selection revision")
        if src["external_context"] is not None:
            ctx = closed(
                src["external_context"],
                "context_ref context_fingerprint introduction_event_ref "
                "introduction_event_fingerprint snapshot_ref snapshot_fingerprint "
                "owner_event_high_watermark",
            )
            for k in ("context_ref", "introduction_event_ref", "snapshot_ref"):
                string(ctx[k])
            for k in (
                "context_fingerprint",
                "introduction_event_fingerprint",
                "snapshot_fingerprint",
            ):
                fingerprint(ctx[k])
            if (
                type(ctx["owner_event_high_watermark"]) is not int
                or not 0 <= ctx["owner_event_high_watermark"] <= 9007199254740991
            ):
                raise TaskContractError("invalid context H")
        predecessor = body["predecessor"]
        if version == 1:
            if predecessor is not None:
                raise TaskContractError("v1 predecessor")
        else:
            pred = closed(predecessor, "contract_version body_sha256")
            if type(pred["contract_version"]) is not int or pred["contract_version"] != version - 1:
                raise TaskContractError("version gap")
            fingerprint(pred["body_sha256"])
        _policies(body)
        encoded = canonical_json_bytes(body)
        if not 1 <= len(encoded) <= 1048576:
            raise TaskContractError("body byte limit")
        object.__setattr__(self, "canonical_body", encoded)

    @property
    def value(self) -> Mapping[str, Any]:
        return immutable(json.loads(self.canonical_body))

    @property
    def body_sha256(self) -> str:
        return digest(self.canonical_body)

    @property
    def body_ref(self) -> str:
        v = self.value
        return "task-contract-body:v1:sha256:" + digest(
            canonical_json_bytes(
                {k: v[k] for k in ("project_id", "contract_id", "contract_version")}
            )
        )

    @classmethod
    def from_bytes(cls, encoded: bytes) -> TaskContractBodyV1:
        if not isinstance(encoded, bytes) or not 1 <= len(encoded) <= 1048576:
            raise TaskContractError("body byte limit/type")

        def unique(items: list[tuple[str, Any]]) -> dict[str, Any]:
            if len(dict(items)) != len(items):
                raise TaskContractError("duplicate JSON key")
            return dict(items)

        body = cls(json.loads(encoded, object_pairs_hook=unique))
        if body.canonical_body != encoded:
            raise TaskContractError("noncanonical body bytes")
        return body


@dataclass(frozen=True)
class IssuedTaskContractV1:
    body: TaskContractBodyV1
    constraint_ref: str
    constraint_fingerprint: str
    issuance_event_ref: str
    snapshot_ref: str
    snapshot_fingerprint: str
    owner_event_high_watermark: int


@dataclass(frozen=True)
class VerifiedTaskContractBindingV1:
    issued: IssuedTaskContractV1
    current: bool


SUPPORTED_ACTION_ID = "open-cycle-derived-task-issuance"
UNSUPPORTED_SOURCE = "TASKCONTRACT_V1_UNSUPPORTED_NEXT_ACTION_SOURCE"


def candidate_fingerprint(candidate: Any) -> str:
    from datetime import UTC

    return digest(
        canonical_json_bytes(
            {
                "candidate_id": candidate.candidate_id,
                "selection_ref": candidate.selection_ref,
                "action_ref": candidate.action_ref.serialized,
                "parameters": candidate.parameters,
                "issuance_owner": candidate.issuance_owner,
                "required_post_issuance_human_input": (
                    candidate.required_post_issuance_human_input.value
                ),
                "created_at": candidate.created_at.astimezone(UTC).isoformat(
                    timespec="microseconds"
                ),
            }
        )
    )


def action_claim(serialized: str):
    from aiscc.next_action.models import ActionRef

    pieces = serialized.split(":")
    if len(pieces) != 6 or pieces[0] != "p1-8-action":
        raise TaskContractError("invalid action identity")
    result = ActionRef(*pieces[1:])
    if result.serialized != serialized:
        raise TaskContractError("noncanonical action identity")
    return result
