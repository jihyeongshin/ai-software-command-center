"""Immutable static contracts. These values grant no runtime authority."""

from __future__ import annotations

import hashlib
import re
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

RESOURCE_VERSION = "be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d"
RESOURCE_REF = f"repository:synthetic-stockroom@{RESOURCE_VERSION}"
SCENARIO_IDS = (
    "stockroom-s1-normal",
    "stockroom-s2-missing-evidence",
    "stockroom-s3-policy-conflict",
    "stockroom-s4-human-owned-claim",
)
ScenarioId = Literal[
    "stockroom-s1-normal",
    "stockroom-s2-missing-evidence",
    "stockroom-s3-policy-conflict",
    "stockroom-s4-human-owned-claim",
]
Text = Annotated[str, Field(min_length=1, max_length=4096)]
Sha256 = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]
State = Literal[
    "READY",
    "RUNNING",
    "ADMISSION_PENDING",
    "ACCEPTED",
    "REWORK_REQUIRED",
    "BLOCKED",
    "HUMAN_REQUIRED",
]


class Contract(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)


def relative_posix_path(value: str) -> str:
    """Reject ambiguous paths before any filesystem resolution or read."""
    if not re.fullmatch(r"[A-Za-z0-9_./-]+", value):
        raise ValueError("path must be relative ASCII POSIX")
    if any(part in ("", ".", "..") or part.endswith(".") for part in value.split("/")):
        raise ValueError("path must have only unambiguous relative segments")
    return value


class ResourceFile(Contract):
    path: Text
    mode: Literal["100644"]
    bytes: Annotated[int, Field(ge=0)]
    sha256: Sha256

    _path = field_validator("path")(relative_posix_path)


def manifest_sha256(files: tuple[ResourceFile, ...]) -> str:
    """AISCC-SOURCE-MANIFEST-SHA256-V1; pure, no source reads or extraction."""
    paths = tuple(item.path for item in files)
    if paths != tuple(sorted(set(paths))):
        raise ValueError("manifest paths must be sorted and unique")
    rows = "".join(f"{item.mode}\t{item.path}\t{item.bytes}\t{item.sha256}\n" for item in files)
    return hashlib.sha256(rows.encode("ascii")).hexdigest()


class Resource(Contract):
    schema_id: Literal["AISCC-SYNTHETIC-RESOURCE-V1"]
    schema_version: Literal["1.0.0"]
    resource_id: Literal["repository:synthetic-stockroom"]
    resource_version: Sha256
    resource_ref: Text
    source_commit: Literal["05185c57a6265a4002050ce25cdfde3dc87e9779"]
    subroot: Literal["examples/synthetic-stockroom/"]
    git_subtree: Literal["f3d9203321ae3535abf8e92a7285da1067f6c55e"]
    file_count: Annotated[int, Field(ge=14, le=14)]
    aggregate_algorithm: Literal["AISCC-SOURCE-MANIFEST-SHA256-V1"]
    aggregate_sha256: Sha256
    files: Annotated[tuple[ResourceFile, ...], Field(min_length=14, max_length=14)]

    @model_validator(mode="after")
    def identity(self) -> Self:
        if self.file_count != len(self.files):
            raise ValueError("file_count mismatch")
        if not (
            self.resource_ref == f"{self.resource_id}@{self.resource_version}" == RESOURCE_REF
            and self.resource_version == self.aggregate_sha256 == RESOURCE_VERSION
            and manifest_sha256(self.files) == self.aggregate_sha256
        ):
            raise ValueError("resource identity or manifest aggregate mismatch")
        return self


class TaskContract(Contract):
    goal: Text
    non_goals: Annotated[tuple[Text, ...], Field(min_length=1)]


class EvidenceRequirement(Contract):
    requirement_id: Literal["summary-runtime", "policy-conflict-static", "human-browser-qa"]
    proof_type: Literal["TOOL_RUNTIME", "STATIC_SOURCE", "HUMAN_VERIFICATION"]
    owner: Literal["EXECUTOR", "HUMAN"]

    @model_validator(mode="after")
    def owner_and_type(self) -> Self:
        expected = {
            "summary-runtime": ("TOOL_RUNTIME", "EXECUTOR"),
            "policy-conflict-static": ("STATIC_SOURCE", "EXECUTOR"),
            "human-browser-qa": ("HUMAN_VERIFICATION", "HUMAN"),
        }
        if (self.proof_type, self.owner) != expected[self.requirement_id]:
            raise ValueError("wrong evidence owner or proof type")
        return self


class EvidenceContract(Contract):
    executor_required: tuple[EvidenceRequirement, ...]
    reuse_allowed: tuple[Literal["accepted-resource-manifest-identity"], ...]
    human_owned: tuple[EvidenceRequirement, ...]
    not_required: tuple[Literal["external-llm", "public-live", "browser-qa"], ...]
    forbidden: tuple[Literal["agent-claim-as-human-result", "static-proof-as-runtime-proof"], ...]


class DeniedAcceptance(Contract):
    requested_target: Literal["ACCEPTED"]
    decision: Literal["DENIED"]
    state_version_mutation: Literal[False]
    reason: Literal["MISSING_EVIDENCE", "HUMAN_RESULT_ABSENT"]


class PolicyBlocker(Contract):
    blocker_type: Literal["POLICY"]
    blocker_reason: Literal["POLICY_CONFLICT"]


class ExpectedWorkflow(Contract):
    states: tuple[State, ...]
    accepted_request: DeniedAcceptance | None
    blocker: PolicyBlocker | None
    wrong_owner_candidate: Literal["NOT_APPLICABLE", "REJECTED"]
    attestation: Literal["NOT_REQUIRED", "FRESH_PRE_HUMAN"]
    human_result: Literal["NOT_REQUIRED", "ABSENT_PENDING"]
    same_run_automatic_retry: Literal[False]
    source_mutation: Literal[False]


class JudgmentContract(Contract):
    owner_policy: Literal["SYSTEM_DETERMINISTIC", "HUMAN"]
    expected_status: Literal["ACCEPTED", "HOLD_REWORK_REQUIRED"] | None
    authoritative_at_capture_boundary: bool
    admitted_human_result_required: bool
    separate_transition_admission_required: Literal[True]
    rule_version: Literal["stockroom-judgment-v1"]


class CycleNextActionContract(Contract):
    runtime_admitted_cycle: Literal["AFTER_ACCEPTED_TERMINAL_LINEAGE", "INELIGIBLE_AT_CAPTURE"]
    reusable_project_memory: Literal["AFTER_ACCEPTED_TERMINAL_LINEAGE", "INELIGIBLE_AT_CAPTURE"]
    next_action: Literal[
        "SEPARATE_SUCCESSOR_TASK",
        "EXPLICIT_REWORK_REVISION",
        "HUMAN_COMMAND_CENTER_POLICY_RESOLUTION",
        "WAIT_FOR_DESIGNATED_HUMAN",
    ]
    fabricate_cycle_or_memory: Literal[False]


class RecordingContract(Contract):
    contract_kind: Literal["STATIC_CAPTURE_REQUIREMENTS_NOT_RUN_DATA"]
    runtime_mode: Literal["OWNER_SELF_DOGFOOD"]
    execution_backend_kind: Literal["LOCAL_DETERMINISTIC_PROVIDER"]
    external_llm_executed: Literal[False]
    actual_execution_required_before_recorded_replay: Literal[True]
    required_provenance: tuple[
        Literal[
            "task-contract",
            "scenario-version",
            "resource-ref",
            "orchestrator-version",
            "transition-decisions",
            "state-versions",
            "evidence-admission",
            "agent-claims",
            "human-gate-and-result",
            "judgment",
            "cycle-next-action",
            "capture-timestamp",
        ],
        ...,
    ]


class PublicDisclosure(Contract):
    content: Literal["SYNTHETIC_ONLY"]
    runtime_claim: Literal["NONE_STATIC_DEFINITION"]
    future_replay_label: Literal["Recorded Run Replay"]
    license_review: Literal["HUMAN_PENDING"]
    public_replay: Literal["NOT_ADMITTED"]
    public_live: Literal["NOT_RELEASED"]
    replay_requires_sanitization_and_license_admission: Literal[True]
    external_llm_reasoning_claim: Literal[False]


class Scenario(Contract):
    schema_id: Literal["AISCC-SCENARIO-V1"]
    schema_version: Literal["1.0.0"]
    scenario_id: ScenarioId
    scenario_version: Literal["1.0.0"]
    purpose: Text
    resource_ref: Text
    task_contract: TaskContract
    allowed_actions: tuple[
        Literal[
            "fixed-stockroom-summary",
            "compare-fixed-synthetic-policies",
            "submit-evidence-candidates",
            "submit-synthetic-agent-claim",
        ],
        ...,
    ]
    forbidden_actions: tuple[
        Literal[
            "source-mutation",
            "arbitrary-parameters",
            "arbitrary-shell-network",
            "external-provider",
            "fabricate-human-result-judgment-cycle",
        ],
        ...,
    ]
    user_parameters: tuple[()]
    expected_workflow: ExpectedWorkflow
    evidence_contract: EvidenceContract
    judgment_contract: JudgmentContract
    cycle_next_action_contract: CycleNextActionContract
    recording_contract: RecordingContract
    public_disclosure: PublicDisclosure
    fixture_refs: tuple[str, ...]

    @field_validator("fixture_refs")
    @classmethod
    def fixture_paths(cls, values: tuple[str, ...]) -> tuple[str, ...]:
        if len(values) != len(set(values)):
            raise ValueError("duplicate fixture ref")
        for value in values:
            relative_posix_path(value)
            if not value.startswith("fixtures/") or not value.endswith(".json"):
                raise ValueError("fixture must be beneath fixtures and have JSON suffix")
        return values

    @model_validator(mode="after")
    def scenario_semantics(self) -> Self:
        number = SCENARIO_IDS.index(self.scenario_id)
        if self.resource_ref != RESOURCE_REF:
            raise ValueError("unknown resource_ref")
        states = (
            ("READY", "RUNNING", "ADMISSION_PENDING", "ACCEPTED"),
            ("READY", "RUNNING", "ADMISSION_PENDING", "REWORK_REQUIRED"),
            ("READY", "RUNNING", "BLOCKED"),
            ("READY", "RUNNING", "ADMISSION_PENDING", "HUMAN_REQUIRED"),
        )
        fixtures = (
            (),
            ("fixtures/missing-evidence.json",),
            ("fixtures/policy-conflict.json",),
            ("fixtures/human-owned-claim.json",),
        )
        workflow = self.expected_workflow
        denial = workflow.accepted_request
        if workflow.states != states[number] or self.fixture_refs != fixtures[number]:
            raise ValueError("scenario workflow or fixture binding mismatch")
        if number in (1, 3):
            reason = "MISSING_EVIDENCE" if number == 1 else "HUMAN_RESULT_ABSENT"
            if denial is None or denial.reason != reason:
                raise ValueError("explicit unchanged-version ACCEPTED denial required")
        elif denial is not None:
            raise ValueError("unexpected acceptance denial")
        if (workflow.blocker is not None) != (number == 2):
            raise ValueError("policy blocker binding mismatch")
        if (
            workflow.wrong_owner_candidate != ("REJECTED" if number == 3 else "NOT_APPLICABLE")
            or workflow.attestation != ("FRESH_PRE_HUMAN" if number == 3 else "NOT_REQUIRED")
            or workflow.human_result != ("ABSENT_PENDING" if number == 3 else "NOT_REQUIRED")
        ):
            raise ValueError("Human ownership or PRE_HUMAN boundary mismatch")
        evidence = self.evidence_contract
        required = "policy-conflict-static" if number == 2 else "summary-runtime"
        if tuple(r.requirement_id for r in evidence.executor_required) != (required,):
            raise ValueError("executor requirement mismatch")
        expected_human = ("human-browser-qa",) if number == 3 else ()
        if tuple(r.requirement_id for r in evidence.human_owned) != expected_human:
            raise ValueError("Human requirement must remain explicit")
        if evidence.reuse_allowed != ("accepted-resource-manifest-identity",):
            raise ValueError("reuse boundary mismatch")
        not_required = ("external-llm", "public-live") + (() if number == 3 else ("browser-qa",))
        if evidence.not_required != not_required or evidence.forbidden != (
            "agent-claim-as-human-result",
            "static-proof-as-runtime-proof",
        ):
            raise ValueError("evidence non-substitution boundary mismatch")
        judgment = self.judgment_contract
        if (
            judgment.owner_policy != ("HUMAN" if number == 3 else "SYSTEM_DETERMINISTIC")
            or judgment.expected_status != ("ACCEPTED", "HOLD_REWORK_REQUIRED", None, None)[number]
            or judgment.authoritative_at_capture_boundary != (number < 2)
            or judgment.admitted_human_result_required != (number == 3)
        ):
            raise ValueError("judgment capture boundary mismatch")
        cycle = self.cycle_next_action_contract
        eligibility = "AFTER_ACCEPTED_TERMINAL_LINEAGE" if number == 0 else "INELIGIBLE_AT_CAPTURE"
        next_action = (
            "SEPARATE_SUCCESSOR_TASK",
            "EXPLICIT_REWORK_REVISION",
            "HUMAN_COMMAND_CENTER_POLICY_RESOLUTION",
            "WAIT_FOR_DESIGNATED_HUMAN",
        )[number]
        if (
            cycle.runtime_admitted_cycle != eligibility
            or cycle.reusable_project_memory != eligibility
            or cycle.next_action != next_action
        ):
            raise ValueError("cycle/next action capture boundary mismatch")
        actions = (
            ("compare-fixed-synthetic-policies",)
            if number == 2
            else (
                "fixed-stockroom-summary",
                "submit-evidence-candidates",
            )
            + (("submit-synthetic-agent-claim",) if number == 3 else ())
        )
        if self.allowed_actions != actions or self.forbidden_actions != (
            "source-mutation",
            "arbitrary-parameters",
            "arbitrary-shell-network",
            "external-provider",
            "fabricate-human-result-judgment-cycle",
        ):
            raise ValueError("action boundary mismatch")
        provenance = self.recording_contract.required_provenance
        if len(provenance) != 12 or len(set(provenance)) != 12:
            raise ValueError("complete unique recording provenance required")
        return self


class MissingEvidenceFixture(Contract):
    schema_id: Literal["AISCC-MISSING-EVIDENCE-FIXTURE-V1"]
    schema_version: Literal["1.0.0"]
    scenario_id: Literal["stockroom-s2-missing-evidence"]
    fixture_owner: Literal["SERVER"]
    synthetic: Literal[True]
    operation: Literal["OMIT_REQUIRED_EVIDENCE_CANDIDATE"]
    omitted_requirement_id: Literal["summary-runtime"]
    controlled_omission: Literal[True]


class InclusivePolicy(Contract):
    policy_id: Literal["inclusive-reorder-baseline-v1"]
    rule: Literal["reorder when available <= threshold"]


class StrictPolicy(Contract):
    policy_id: Literal["strict-reorder-request-v1"]
    rule: Literal["requested replacement uses available < threshold"]


class PolicyConflictFixture(Contract):
    schema_id: Literal["AISCC-POLICY-CONFLICT-FIXTURE-V1"]
    schema_version: Literal["1.0.0"]
    scenario_id: Literal["stockroom-s3-policy-conflict"]
    fixture_owner: Literal["SERVER"]
    synthetic: Literal[True]
    baseline: InclusivePolicy
    requested_replacement: StrictPolicy
    blocker: PolicyBlocker
    source_mutation: Literal[False]
    authoritative_judgment_at_capture: Literal[False]


class SyntheticAgentClaim(Contract):
    producer: Literal["AGENT"]
    text: Literal["Human browser QA completed"]
    claimed_requirement_id: Literal["human-browser-qa"]
    classification: Literal["SYNTHETIC_ADVERSARIAL_AGENT_CLAIM"]
    actual_human_input: Literal[False]


class HumanOwnedClaimFixture(Contract):
    schema_id: Literal["AISCC-HUMAN-OWNED-CLAIM-FIXTURE-V1"]
    schema_version: Literal["1.0.0"]
    scenario_id: Literal["stockroom-s4-human-owned-claim"]
    fixture_owner: Literal["SERVER"]
    synthetic: Literal[True]
    adversarial: Literal[True]
    agent_claim: SyntheticAgentClaim
    expected_candidate_decision: Literal["REJECTED_WRONG_OWNER"]
    human_result: None


class SelectorEnum(Contract):
    type: Literal["string"]
    enum: tuple[ScenarioId, ...]

    @field_validator("enum")
    @classmethod
    def exact_ids(cls, ids: tuple[ScenarioId, ...]) -> tuple[ScenarioId, ...]:
        if ids != SCENARIO_IDS:
            raise ValueError("selector must expose exactly the four ordered scenario IDs")
        return ids


class SelectorProperties(Contract):
    scenario_id: SelectorEnum


class SelectorSchema(Contract):
    type: Literal["object"]
    additionalProperties: Literal[False]
    required: tuple[Literal["scenario_id"], ...]
    properties: SelectorProperties

    @field_validator("required")
    @classmethod
    def exact_required(cls, required: tuple[str, ...]) -> tuple[str, ...]:
        if required != ("scenario_id",):
            raise ValueError("selector requires scenario_id only")
        return required


class PublicSelection(Contract):
    scenario_id: ScenarioId


class CatalogEntry(Contract):
    scenario_id: ScenarioId
    scenario_version: Literal["1.0.0"]
    path: Text

    _path = field_validator("path")(relative_posix_path)


class CatalogDocument(Contract):
    schema_id: Literal["AISCC-SCENARIO-CATALOG-V1"]
    schema_version: Literal["1.0.0"]
    resource_path: Literal["resource.json"]
    resource_ref: Text
    public_selection_schema: SelectorSchema
    scenarios: Annotated[tuple[CatalogEntry, ...], Field(min_length=4, max_length=4)]

    @model_validator(mode="after")
    def exact_catalog(self) -> Self:
        ids = tuple(entry.scenario_id for entry in self.scenarios)
        if len(set(ids)) != len(ids):
            raise ValueError("duplicate scenario ID/version")
        if set(ids) != set(SCENARIO_IDS) or self.resource_ref != RESOURCE_REF:
            raise ValueError("catalog identity mismatch")
        paths = (
            "s1-normal.json",
            "s2-missing-evidence.json",
            "s3-policy-conflict.json",
            "s4-human-owned-claim.json",
        )
        for entry in self.scenarios:
            if entry.path != paths[SCENARIO_IDS.index(entry.scenario_id)]:
                raise ValueError("catalog scenario ID/version/path binding mismatch")
        return self
