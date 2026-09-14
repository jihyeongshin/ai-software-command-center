from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from aiscc.evidence.models import canonical_hash
from aiscc.task_authority.models import (
    NEXT_ACTION_CONTEXT_SOURCE_CONTRACT_FINGERPRINT,
    NextActionContextRefV1,
)

TASK_ISSUANCE_OWNER = "EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY"
NEXT_ACTION_POLICY_AUTHORITY = "P1_8_NEXT_ACTION_POLICY_AUTHORITY_V1"
ELIGIBILITY_POLICY_ID = "P1_8_NEXT_ACTION_ELIGIBILITY_POLICY"
ELIGIBILITY_POLICY_REF = (
    "p1-8-next-action-eligibility-policy:v1:P1_8_NEXT_ACTION_ELIGIBILITY_POLICY"
)
ELIGIBILITY_POLICY_FINGERPRINT = "a0425bee1c2abf26c50a63ff125795e88e0b15e6f182dfbf716fc5f0217d6d03"
SELECTION_POLICY_ID = "P1_8_NEXT_ACTION_SELECTION_POLICY"
SELECTION_POLICY_REF = "p1-8-next-action-selection-policy:v1:P1_8_NEXT_ACTION_SELECTION_POLICY"
SELECTION_POLICY_FINGERPRINT = "4f84dbae89ee1113a2f6eeb28aa5d00100fcb65db2694b8716b52925d9bb312d"
CATALOG_REF = "p1-8-policy-action-catalog:v1:P1_8_POLICY_ACTION_CATALOG"
CATALOG_FINGERPRINT = "c02290f5111608efbd3cd12edec9e066ca622133f262a1352d971fcddf02e58c"
OPERATIONAL_DESCRIPTOR_FINGERPRINT = (
    "77bf03ba2125b32daef565739274a853cbfa03faab6477e37f4f9108517af8b0"
)
CONTEXT_DESCRIPTOR_SCHEMA_FINGERPRINT = (
    "bef330ffba29c24a76910d22c2de514235224add40b2725d4ac342a25dc4a7ed"
)
CONTEXT_SOURCE_CONTRACT_REF = (
    "next-action-context-source-contract:v1:NEXT_ACTION_CONTEXT_SOURCE_CONTRACT_V1"
)


class DescriptorSourceKind(StrEnum):
    POLICY_ACTION_CATALOG = "POLICY_ACTION_CATALOG"
    CANONICAL_ROADMAP_ITEM = "CANONICAL_ROADMAP_ITEM"
    TASK_CONTRACT_FOLLOW_UP_TEMPLATE = "TASK_CONTRACT_FOLLOW_UP_TEMPLATE"
    OWNER_BLOCKER_RECOVERY_ACTION = "OWNER_BLOCKER_RECOVERY_ACTION"


class NextActionSelectionMode(StrEnum):
    OPERATIONAL_RECOVERY = "OPERATIONAL_RECOVERY"
    CYCLE_DERIVED = "CYCLE_DERIVED"
    SELF_DOGFOOD_GENESIS = "SELF_DOGFOOD_GENESIS"


class HumanInputKind(StrEnum):
    NONE = "NONE"
    BEFORE_SELECTION = "BEFORE_SELECTION"
    AFTER_TASK_ISSUANCE_P1_7 = "AFTER_TASK_ISSUANCE_P1_7"


class NextActionCurrentDisposition(StrEnum):
    RETAIN_CURRENT = "RETAIN_CURRENT"
    WITHDRAW_CURRENT = "WITHDRAW_CURRENT"


class NextActionErrorCode(StrEnum):
    NOT_ENROLLED = "NEXT_ACTION_ACTION_NOT_ENROLLED"
    NOT_SUPPORTED = "NEXT_ACTION_SOURCE_KIND_NOT_SUPPORTED"
    POLICY_NOT_CURRENT = "NEXT_ACTION_POLICY_NOT_CURRENT"
    DESCRIPTOR_NOT_CURRENT = "NEXT_ACTION_DESCRIPTOR_NOT_CURRENT"
    AUTHORITY_DENIED = "NEXT_ACTION_POLICY_AUTHORITY_ACCESS_DENIED"
    HUMAN_INPUT_REQUIRED = "HUMAN_INPUT_REQUIRED"
    HUMAN_BINDING_MISMATCH = "NEXT_ACTION_HUMAN_BINDING_MISMATCH"
    RECOVERY_AUTHORITY_REQUIRED = "NEXT_ACTION_RECOVERY_AUTHORITY_REQUIRED"
    HISTORICAL_CORRUPTION = "NEXT_ACTION_HISTORICAL_CORRUPTION"
    IDENTITY_CONFLICT = "NEXT_ACTION_IDENTITY_CONFLICT"
    NON_CURRENT_MEMORY = "NEXT_ACTION_NON_CURRENT_MEMORY"
    PRIORITY_SOURCE_NOT_ENROLLED = "NEXT_ACTION_PRIORITY_SOURCE_NOT_ENROLLED"


class NextActionError(RuntimeError):
    def __init__(self, code: NextActionErrorCode, message: str) -> None:
        super().__init__(f"{code.value}: {message}")
        self.code = code


@dataclass(frozen=True, slots=True, order=True)
class ActionRef:
    eligibility_policy_id: str
    eligibility_policy_version: str
    action_id: str
    action_version: str
    descriptor_fingerprint: str

    @property
    def serialized(self) -> str:
        return (
            f"p1-8-action:{self.eligibility_policy_id}:{self.eligibility_policy_version}:"
            f"{self.action_id}:{self.action_version}:{self.descriptor_fingerprint}"
        )

    @property
    def action_key(self) -> str:
        return self.action_id


@dataclass(frozen=True, slots=True)
class NextActionDescriptor:
    action_ref: ActionRef
    descriptor_version: str
    project_restriction: str
    scope_restrictions: dict[str, str]
    parameter_schema_id: str
    parameter_schema_version: str
    parameter_schema_fingerprint: str
    parameter_rules: dict[str, str]
    source_kind: DescriptorSourceKind
    source_authority_ref: str
    source_authority_version: str
    source_authority_fingerprint: str
    allowed_selection_modes: tuple[NextActionSelectionMode, ...]
    priority_classification_source_ref: str
    priority_classification_source_hash: str
    priority_rank: int
    dependency_ordinal: int
    critical_path_ordinal: int
    descriptor_policy_ordinal: int
    required_human_input_kind: HumanInputKind
    task_issuance_owner: str
    task_template_ref: str
    task_template_hash: str
    privacy_restrictions: tuple[str, ...]
    security_restrictions: tuple[str, ...]
    authority_revision: int
    effective_sequence: int
    supersedes_ref: str
    revocation_ref: str
    current_projection_on_invalidation: NextActionCurrentDisposition
    fingerprint: str
    _authority_seal: object | None = field(default=None, repr=False, compare=False)
    canonical_payload: dict[str, object] | None = field(default=None, repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class NextActionProposal:
    proposal_id: str
    project_id: str
    action_ref: ActionRef
    parameters: dict[str, Any]
    rationale: str
    claimed_priority: int | None = None
    claimed_security: bool | None = None
    claimed_blocker: bool | None = None

    @property
    def fingerprint(self) -> str:
        return canonical_hash(
            {
                "action_ref": self.action_ref.serialized,
                "parameters": self.parameters,
                "project_id": self.project_id,
                "proposal_id": self.proposal_id,
                "rationale": self.rationale,
            }
        )


@dataclass(frozen=True, slots=True)
class NextActionEligibilityPolicy:
    policy_id: str
    policy_version: str
    policy_ref: str
    authority_id: str
    authority_version: str
    authority_revision: int
    enrolled_action_bindings: tuple[tuple[str, str], ...]
    issued_at: datetime
    effective_sequence: int
    current_projection_on_invalidation: NextActionCurrentDisposition
    fingerprint: str
    _authority_seal: object | None = field(default=None, repr=False, compare=False)


@dataclass(frozen=True, slots=True)
class NextActionSelectionPolicy:
    policy_id: str
    policy_version: str
    policy_ref: str
    authority_id: str
    authority_version: str
    authority_revision: int
    recovery_states: tuple[str, ...]
    issued_at: datetime
    effective_sequence: int
    current_projection_on_invalidation: NextActionCurrentDisposition
    fingerprint: str
    _authority_seal: object | None = field(default=None, repr=False, compare=False)
    class_to_rank: tuple[tuple[str, int], ...] = (
        ("SECURITY_POLICY_OR_MISSING_ARTIFACT", 1),
        ("REJECTED_HOLD_FAILED_REWORK_RECOVERY", 2),
        ("BASELINE_OR_AUTHORITY_CONFLICT", 3),
        ("ACCEPTED_CORE_CRITICAL_PATH", 4),
        ("OPERATIONAL_HARDENING", 5),
        ("OPTIONAL_OPTIMIZATION", 6),
    )


@dataclass(frozen=True, slots=True)
class NextActionOwnerEvent:
    event_id: str
    subject_ref: str
    subject_kind: str
    event_kind: str
    replacement_ref: str
    disposition: NextActionCurrentDisposition
    created_at: datetime
    _authority_seal: object | None = field(default=None, repr=False, compare=False)


class P1_8NextActionPolicyAuthority:
    authority_id = NEXT_ACTION_POLICY_AUTHORITY
    authority_version = "AISCC-P1-8-NEXT-ACTION-POLICY-AUTHORITY-V1"

    def __init__(self) -> None:
        self.__seal = object()

    def issue_policy_catalog_v1(
        self,
        *,
        now: datetime,
    ) -> tuple[
        NextActionEligibilityPolicy,
        NextActionSelectionPolicy,
        tuple[NextActionDescriptor, ...],
    ]:
        descriptors = (self._fixed_operational_descriptor(),)
        bindings = tuple(
            sorted((item.action_ref.serialized, item.fingerprint) for item in descriptors)
        )
        eligibility = NextActionEligibilityPolicy(
            ELIGIBILITY_POLICY_ID,
            "v1",
            ELIGIBILITY_POLICY_REF,
            "P1_8_NEXT_ACTION_ELIGIBILITY_POLICY_AUTHORITY_V1",
            self.authority_version,
            1,
            bindings,
            now.astimezone(UTC),
            1,
            NextActionCurrentDisposition.WITHDRAW_CURRENT,
            ELIGIBILITY_POLICY_FINGERPRINT,
            self.__seal,
        )
        selection = NextActionSelectionPolicy(
            SELECTION_POLICY_ID,
            "v1",
            SELECTION_POLICY_REF,
            "P1_8_NEXT_ACTION_SELECTION_POLICY_AUTHORITY_V1",
            self.authority_version,
            1,
            ("BLOCKED", "FAILED", "REJECTED", "REWORK_REQUIRED"),
            now.astimezone(UTC),
            1,
            NextActionCurrentDisposition.WITHDRAW_CURRENT,
            SELECTION_POLICY_FINGERPRINT,
            self.__seal,
        )
        return eligibility, selection, descriptors

    def _fixed_operational_descriptor(self) -> NextActionDescriptor:
        action_ref = ActionRef(
            ELIGIBILITY_POLICY_ID,
            "v1",
            "open-operational-recovery-task-issuance",
            "v1",
            OPERATIONAL_DESCRIPTOR_FINGERPRINT,
        )
        payload: dict[str, object] = {
            "descriptor_schema": "p1-8-next-action-descriptor-v1",
            "catalog_ref": CATALOG_REF,
            "catalog_fingerprint": CATALOG_FINGERPRINT,
            "entry_identity": "open-operational-recovery-task-issuance:v1",
            "accepted_descriptor_fingerprint": OPERATIONAL_DESCRIPTOR_FINGERPRINT,
        }
        return NextActionDescriptor(
            action_ref=action_ref,
            descriptor_version="v1",
            project_restriction="*",
            scope_restrictions={},
            parameter_schema_id="P1_8_OPERATIONAL_RECOVERY_PARAMETERS_V1",
            parameter_schema_version="v1",
            parameter_schema_fingerprint=(
                "92fe98cbc7cae63ab1f72161b625eb9bbd3281592f7731f98d24f30b4dd326f1"
            ),
            parameter_rules={
                "observed_state": "string",
                "observed_state_version": "integer",
                "operational_fact_fingerprint": "string",
                "operational_fact_ref": "string",
                "operational_work_run_id": "string",
            },
            source_kind=DescriptorSourceKind.POLICY_ACTION_CATALOG,
            source_authority_ref=CATALOG_REF,
            source_authority_version="v1",
            source_authority_fingerprint=CATALOG_FINGERPRINT,
            allowed_selection_modes=(NextActionSelectionMode.OPERATIONAL_RECOVERY,),
            priority_classification_source_ref=SELECTION_POLICY_REF,
            priority_classification_source_hash=SELECTION_POLICY_FINGERPRINT,
            priority_rank=1,
            dependency_ordinal=10,
            critical_path_ordinal=0,
            descriptor_policy_ordinal=10,
            required_human_input_kind=HumanInputKind.AFTER_TASK_ISSUANCE_P1_7,
            task_issuance_owner=TASK_ISSUANCE_OWNER,
            task_template_ref="NONE",
            task_template_hash="NONE",
            privacy_restrictions=(
                "INTERNAL_ONLY",
                "NO_PRIVATE_HUMAN_ARTIFACT_EXPORT",
                "NO_RAW_MEMORY_CONTENT",
            ),
            security_restrictions=(
                "NO_CREDENTIAL_OR_SECRET_INPUT",
                "NO_PROVIDER_OR_NETWORK_ACTION",
                "NO_TASKCONTRACT_MINT",
                "NO_WORKFLOW_MUTATION",
                "REFERENCE_PARAMETERS_ONLY",
            ),
            authority_revision=1,
            effective_sequence=1,
            supersedes_ref="NONE",
            revocation_ref="NONE",
            current_projection_on_invalidation=(NextActionCurrentDisposition.WITHDRAW_CURRENT),
            fingerprint=OPERATIONAL_DESCRIPTOR_FINGERPRINT,
            _authority_seal=self.__seal,
            canonical_payload=payload,
        )

    def issue_genesis_policy_catalog(self, *, authority, now):
        from aiscc.next_action.genesis import ACTION, MODE, GenesisNextActionAuthorityV1

        if not isinstance(authority, GenesisNextActionAuthorityV1):
            raise ValueError("typed genesis authority required; persisted owner verifies selection")
        _, selection, _ = self.issue_policy_catalog_v1(now=now)
        payload = {
            "schema": "AISCC-P1-8-SELF-DOGFOOD-GENESIS-DESCRIPTOR-V1",
            "action_id": ACTION,
            "source_mode": MODE,
            "genesis_authority_ref": authority.authority_ref,
            "genesis_authority_fingerprint": authority.fingerprint,
            "context": authority.value,
            "task_issuance_owner": TASK_ISSUANCE_OWNER,
            "parameter_rules": {
                "genesis_authority_ref": "string",
                "genesis_authority_fingerprint": "string",
            },
        }
        fp = canonical_hash(payload)
        policy_id = "P1_8_SELF_DOGFOOD_GENESIS_ELIGIBILITY_POLICY"
        catalog_ref = "p1-8-genesis-catalog:v1"
        catalog_hash = canonical_hash(
            {"design": "AISCC-P1-8-SELF-DOGFOOD-GENESIS-BOOTSTRAP-V1", "action": ACTION}
        )
        descriptor = replace(
            self._fixed_operational_descriptor(),
            action_ref=ActionRef(policy_id, "v1", ACTION, "v1", fp),
            project_restriction=authority.value["project_id"],
            scope_restrictions={"phase_id": authority.value["phase_id"]},
            parameter_schema_id="P1_8_SELF_DOGFOOD_GENESIS_PARAMETERS_V1",
            parameter_schema_fingerprint=canonical_hash(payload["parameter_rules"]),
            parameter_rules=payload["parameter_rules"],
            source_authority_ref=catalog_ref,
            source_authority_fingerprint=catalog_hash,
            allowed_selection_modes=(NextActionSelectionMode.SELF_DOGFOOD_GENESIS,),
            priority_classification_source_ref=authority.authority_ref,
            priority_classification_source_hash=authority.fingerprint,
            priority_rank=0,
            dependency_ordinal=0,
            critical_path_ordinal=0,
            descriptor_policy_ordinal=0,
            required_human_input_kind=HumanInputKind.NONE,
            fingerprint=fp,
            canonical_payload=payload,
        )
        bindings = ((descriptor.action_ref.serialized, fp),)
        eligibility = NextActionEligibilityPolicy(
            policy_id,
            "v1",
            "p1-8-genesis-eligibility:v1:" + fp,
            "P1_8_NEXT_ACTION_ELIGIBILITY_POLICY_AUTHORITY_V1",
            self.authority_version,
            1,
            bindings,
            now.astimezone(UTC),
            1,
            NextActionCurrentDisposition.WITHDRAW_CURRENT,
            canonical_hash(
                {
                    "policy_id": policy_id,
                    "catalog_ref": catalog_ref,
                    "catalog_fingerprint": catalog_hash,
                    "bindings": bindings,
                }
            ),
            self.__seal,
        )
        return eligibility, selection, (descriptor,)

    def issue_context_bound_descriptor(
        self,
        *,
        context: NextActionContextRefV1,
        issuance_event_sequence: int,
    ) -> NextActionDescriptor:
        payload: dict[str, object] = {
            "descriptor_schema": "p1-8-cycle-derived-context-bound-descriptor-v1",
            "eligibility_policy_id": ELIGIBILITY_POLICY_ID,
            "eligibility_policy_version": "v1",
            "catalog_ref": CATALOG_REF,
            "catalog_fingerprint": CATALOG_FINGERPRINT,
            "action_id": "open-cycle-derived-task-issuance",
            "action_version": "v1",
            "project_id": context.project_id,
            "scope_kind": "TASK_CONTRACT",
            "task_contract_id": context.task_contract_id,
            "task_contract_version": context.task_contract_version,
            "parameter_schema_id": "P1_8_CYCLE_DERIVED_PARAMETERS_V1",
            "parameter_schema_version": "v1",
            "parameter_schema_fingerprint": (
                "3e4407fef8f429031038018d8ee8fab0cb91ad583277f28e0d75064b226ea646"
            ),
            "allowed_selection_mode": "CYCLE_DERIVED",
            "priority_classification_source_kind": "NEXT_ACTION_CONTEXT_REF_V1",
            "priority_classification_source_ref": context.context_ref,
            "priority_classification_source_hash": context.fingerprint,
            "priority_classification_source_contract_ref": CONTEXT_SOURCE_CONTRACT_REF,
            "priority_classification_source_contract_fingerprint": (
                NEXT_ACTION_CONTEXT_SOURCE_CONTRACT_FINGERPRINT
            ),
            "critical_path_ordinal": context.critical_path_ordinal,
            "descriptor_policy_ordinal": 20,
            "required_human_input": "AFTER_TASK_ISSUANCE_P1_7",
            "task_issuance_owner": TASK_ISSUANCE_OWNER,
            "privacy_restrictions": [
                "INTERNAL_ONLY",
                "NO_PRIVATE_HUMAN_ARTIFACT_EXPORT",
                "NO_RAW_MEMORY_CONTENT",
            ],
            "security_restrictions": [
                "NO_CREDENTIAL_OR_SECRET_INPUT",
                "NO_PROVIDER_OR_NETWORK_ACTION",
                "NO_TASKCONTRACT_MINT",
                "NO_WORKFLOW_MUTATION",
                "REFERENCE_PARAMETERS_ONLY",
            ],
            "issuance_event_sequence": issuance_event_sequence,
            "effective_event_sequence": context.effective_sequence,
            "current_projection_on_invalidation": "WITHDRAW_CURRENT",
        }
        fingerprint = canonical_hash(payload)
        action_ref = ActionRef(
            ELIGIBILITY_POLICY_ID,
            "v1",
            "open-cycle-derived-task-issuance",
            "v1",
            fingerprint,
        )
        return NextActionDescriptor(
            action_ref=action_ref,
            descriptor_version="v1",
            project_restriction=context.project_id,
            scope_restrictions={
                "task_contract_id": context.task_contract_id,
                "task_contract_version": context.task_contract_version,
            },
            parameter_schema_id="P1_8_CYCLE_DERIVED_PARAMETERS_V1",
            parameter_schema_version="v1",
            parameter_schema_fingerprint=(
                "3e4407fef8f429031038018d8ee8fab0cb91ad583277f28e0d75064b226ea646"
            ),
            parameter_rules={
                "source_cycle_id": "string",
                "memory_entry_refs": "array",
                "next_action_context_ref": "string",
                "next_action_context_fingerprint": "string",
                "memory_authority_event_high_watermark": "integer",
            },
            source_kind=DescriptorSourceKind.POLICY_ACTION_CATALOG,
            source_authority_ref=CATALOG_REF,
            source_authority_version="v1",
            source_authority_fingerprint=CATALOG_FINGERPRINT,
            allowed_selection_modes=(NextActionSelectionMode.CYCLE_DERIVED,),
            priority_classification_source_ref=context.context_ref,
            priority_classification_source_hash=context.fingerprint,
            priority_rank=0,
            dependency_ordinal=20,
            critical_path_ordinal=context.critical_path_ordinal,
            descriptor_policy_ordinal=20,
            required_human_input_kind=HumanInputKind.AFTER_TASK_ISSUANCE_P1_7,
            task_issuance_owner=TASK_ISSUANCE_OWNER,
            task_template_ref="NONE",
            task_template_hash="NONE",
            privacy_restrictions=(
                "INTERNAL_ONLY",
                "NO_PRIVATE_HUMAN_ARTIFACT_EXPORT",
                "NO_RAW_MEMORY_CONTENT",
            ),
            security_restrictions=(
                "NO_CREDENTIAL_OR_SECRET_INPUT",
                "NO_PROVIDER_OR_NETWORK_ACTION",
                "NO_TASKCONTRACT_MINT",
                "NO_WORKFLOW_MUTATION",
                "REFERENCE_PARAMETERS_ONLY",
            ),
            authority_revision=1,
            effective_sequence=context.effective_sequence,
            supersedes_ref="NONE",
            revocation_ref="NONE",
            current_projection_on_invalidation=(NextActionCurrentDisposition.WITHDRAW_CURRENT),
            fingerprint=fingerprint,
            _authority_seal=self.__seal,
            canonical_payload=payload,
        )

    def _issue_catalog_descriptor(
        self,
        *,
        policy_id: str,
        policy_version: str,
        catalog_id: str,
        specification: dict[str, Any],
        ordinal: int,
    ) -> NextActionDescriptor:
        source_kind = DescriptorSourceKind(
            specification.get("source_kind", DescriptorSourceKind.POLICY_ACTION_CATALOG)
        )
        if source_kind is not DescriptorSourceKind.POLICY_ACTION_CATALOG:
            raise NextActionError(
                NextActionErrorCode.NOT_SUPPORTED,
                "V1 lacks enrolled external roadmap/template owner proof",
            )
        action_id = str(specification["action_id"])
        action_version = str(specification.get("action_version", "v1"))
        parameter_rules = {
            str(key): str(value)
            for key, value in dict(specification.get("parameter_rules", {})).items()
        }
        schema_fingerprint = canonical_hash(parameter_rules)
        body = {
            "action_id": action_id,
            "action_version": action_version,
            "allowed_selection_modes": sorted(
                str(item)
                for item in specification.get(
                    "allowed_selection_modes",
                    (NextActionSelectionMode.OPERATIONAL_RECOVERY.value,),
                )
            ),
            "authority_revision": 1,
            "catalog_id": catalog_id,
            "critical_path_ordinal": int(specification.get("critical_path_ordinal", ordinal)),
            "dependency_ordinal": int(specification.get("dependency_ordinal", ordinal)),
            "descriptor_policy_ordinal": int(
                specification.get("descriptor_policy_ordinal", ordinal)
            ),
            "descriptor_version": "v1",
            "eligibility_policy_id": policy_id,
            "eligibility_policy_version": policy_version,
            "human_input_kind": str(
                specification.get("human_input_kind", HumanInputKind.NONE.value)
            ),
            "parameter_rules": parameter_rules,
            "parameter_schema_fingerprint": schema_fingerprint,
            "priority_rank": int(specification.get("priority_rank", ordinal)),
            "project_restriction": str(specification.get("project_restriction", "*")),
            "scope_restrictions": dict(specification.get("scope_restrictions", {})),
            "source_kind": source_kind.value,
        }
        source_ref = f"p1-8-policy-action-catalog:v1:{catalog_id}:{action_id}"
        source_fingerprint = canonical_hash(
            [self.authority_id, catalog_id, action_id, action_version]
        )
        priority_source_ref = f"{source_ref}#priority"
        priority_source_hash = canonical_hash(
            [catalog_id, action_id, "priority", body["priority_rank"]]
        )
        body.update(
            {
                "current_projection_on_invalidation": "WITHDRAW_CURRENT",
                "effective_sequence": 1,
                "parameter_schema_id": "P1_8_ACTION_PARAMETERS_V1",
                "parameter_schema_version": "v1",
                "priority_classification_source_hash": priority_source_hash,
                "priority_classification_source_ref": priority_source_ref,
                "privacy_restrictions": list(specification.get("privacy_restrictions", ())),
                "security_restrictions": list(specification.get("security_restrictions", ())),
                "source_authority_fingerprint": source_fingerprint,
                "source_authority_ref": source_ref,
                "source_authority_version": "v1",
                "supersedes_ref": "NONE",
                "revocation_ref": "NONE",
                "task_issuance_owner": TASK_ISSUANCE_OWNER,
                "task_template_hash": "NONE",
                "task_template_ref": "NONE",
            }
        )
        fingerprint = canonical_hash(body)
        action_ref = ActionRef(policy_id, policy_version, action_id, action_version, fingerprint)
        modes = tuple(
            NextActionSelectionMode(str(item))
            for item in specification.get(
                "allowed_selection_modes",
                (NextActionSelectionMode.OPERATIONAL_RECOVERY.value,),
            )
        )
        return NextActionDescriptor(
            action_ref,
            "v1",
            str(specification.get("project_restriction", "*")),
            {str(k): str(v) for k, v in dict(specification.get("scope_restrictions", {})).items()},
            "P1_8_ACTION_PARAMETERS_V1",
            "v1",
            schema_fingerprint,
            parameter_rules,
            source_kind,
            source_ref,
            "v1",
            source_fingerprint,
            modes,
            priority_source_ref,
            priority_source_hash,
            int(str(body["priority_rank"])),
            int(str(body["dependency_ordinal"])),
            int(str(body["critical_path_ordinal"])),
            int(str(body["descriptor_policy_ordinal"])),
            HumanInputKind(str(body["human_input_kind"])),
            TASK_ISSUANCE_OWNER,
            "NONE",
            "NONE",
            tuple(str(item) for item in specification.get("privacy_restrictions", ())),
            tuple(str(item) for item in specification.get("security_restrictions", ())),
            1,
            1,
            "NONE",
            "NONE",
            NextActionCurrentDisposition.WITHDRAW_CURRENT,
            fingerprint,
            self.__seal,
        )

    def recognizes_policy(
        self, policy: NextActionEligibilityPolicy | NextActionSelectionPolicy
    ) -> bool:
        if (
            isinstance(policy, NextActionEligibilityPolicy)
            and policy.policy_id == "P1_8_SELF_DOGFOOD_GENESIS_ELIGIBILITY_POLICY"
        ):
            from aiscc.next_action.genesis import ACTION

            bindings = policy.enrolled_action_bindings
            exact = (
                len(bindings) == 1
                and policy.policy_ref == "p1-8-genesis-eligibility:v1:" + bindings[0][1]
                and policy.authority_id == "P1_8_NEXT_ACTION_ELIGIBILITY_POLICY_AUTHORITY_V1"
                and policy.fingerprint
                == canonical_hash(
                    {
                        "policy_id": policy.policy_id,
                        "catalog_ref": "p1-8-genesis-catalog:v1",
                        "catalog_fingerprint": canonical_hash(
                            {
                                "design": "AISCC-P1-8-SELF-DOGFOOD-GENESIS-BOOTSTRAP-V1",
                                "action": ACTION,
                            }
                        ),
                        "bindings": bindings,
                    }
                )
            )
        elif isinstance(policy, NextActionEligibilityPolicy):
            exact = (
                policy.policy_id == ELIGIBILITY_POLICY_ID
                and policy.policy_ref == ELIGIBILITY_POLICY_REF
                and policy.authority_id == "P1_8_NEXT_ACTION_ELIGIBILITY_POLICY_AUTHORITY_V1"
                and policy.fingerprint == ELIGIBILITY_POLICY_FINGERPRINT
            )
        else:
            exact = (
                policy.policy_id == SELECTION_POLICY_ID
                and policy.policy_ref == SELECTION_POLICY_REF
                and policy.authority_id == "P1_8_NEXT_ACTION_SELECTION_POLICY_AUTHORITY_V1"
                and policy.fingerprint == SELECTION_POLICY_FINGERPRINT
                and policy.recovery_states == ("BLOCKED", "FAILED", "REJECTED", "REWORK_REQUIRED")
                and dict(policy.class_to_rank)
                == {
                    "SECURITY_POLICY_OR_MISSING_ARTIFACT": 1,
                    "REJECTED_HOLD_FAILED_REWORK_RECOVERY": 2,
                    "BASELINE_OR_AUTHORITY_CONFLICT": 3,
                    "ACCEPTED_CORE_CRITICAL_PATH": 4,
                    "OPERATIONAL_HARDENING": 5,
                    "OPTIONAL_OPTIMIZATION": 6,
                }
            )
        return (
            policy._authority_seal is self.__seal
            and policy.authority_version == self.authority_version
            and policy.policy_version == "v1"
            and policy.authority_revision == 1
            and policy.effective_sequence == 1
            and policy.current_projection_on_invalidation
            is NextActionCurrentDisposition.WITHDRAW_CURRENT
            and exact
        )

    def recognizes_descriptor(self, descriptor: NextActionDescriptor) -> bool:
        if descriptor.canonical_payload is None:
            return False
        if descriptor.action_ref.action_id == "open-self-dogfood-genesis-task-issuance":
            from aiscc.contracts.canonical_json import canonical_json_bytes
            from aiscc.next_action.genesis import GenesisNextActionAuthorityV1

            try:
                authority = GenesisNextActionAuthorityV1(
                    canonical_json_bytes(descriptor.canonical_payload["context"])
                )
                _, _, expected = self.issue_genesis_policy_catalog(
                    authority=authority, now=datetime.now(UTC)
                )
                return (
                    descriptor._authority_seal is self.__seal
                    and descriptor == expected[0]
                    and descriptor.canonical_payload == expected[0].canonical_payload
                )
            except (ValueError, KeyError, TypeError):
                return False
        operational = descriptor.action_ref.action_id == ("open-operational-recovery-task-issuance")
        expected = (
            OPERATIONAL_DESCRIPTOR_FINGERPRINT
            if operational
            else canonical_hash(descriptor.canonical_payload)
        )
        return (
            descriptor._authority_seal is self.__seal
            and descriptor.action_ref.descriptor_fingerprint == descriptor.fingerprint
            and descriptor.task_issuance_owner == TASK_ISSUANCE_OWNER
            and descriptor.source_kind is DescriptorSourceKind.POLICY_ACTION_CATALOG
            and descriptor.fingerprint == expected
            and descriptor.source_authority_ref == CATALOG_REF
            and descriptor.source_authority_fingerprint == CATALOG_FINGERPRINT
            and descriptor.canonical_payload.get("catalog_ref") == CATALOG_REF
            and descriptor.canonical_payload.get("catalog_fingerprint") == CATALOG_FINGERPRINT
            and descriptor.canonical_payload.get("action_id", descriptor.action_ref.action_id)
            == descriptor.action_ref.action_id
            and descriptor.canonical_payload.get(
                "critical_path_ordinal", descriptor.critical_path_ordinal
            )
            == descriptor.critical_path_ordinal
            and descriptor.dependency_ordinal == (10 if operational else 20)
            and descriptor.descriptor_policy_ordinal == (10 if operational else 20)
            and descriptor.priority_rank == (1 if operational else 0)
        )

    def invalidate(
        self,
        subject: NextActionDescriptor | NextActionEligibilityPolicy | NextActionSelectionPolicy,
        *,
        event_kind: str,
        now: datetime,
        replacement_ref: str = "NONE",
    ) -> NextActionOwnerEvent:
        if event_kind not in {"SUPERSEDED", "REVOKED"}:
            raise NextActionError(NextActionErrorCode.AUTHORITY_DENIED, "invalid event kind")
        if isinstance(subject, NextActionDescriptor):
            recognized = self.recognizes_descriptor(subject)
            subject_ref = subject.action_ref.serialized
            subject_kind = "DESCRIPTOR"
            disposition = subject.current_projection_on_invalidation
        else:
            recognized = self.recognizes_policy(subject)
            subject_ref = subject.policy_ref
            subject_kind = "POLICY"
            disposition = subject.current_projection_on_invalidation
        if not recognized:
            raise NextActionError(NextActionErrorCode.AUTHORITY_DENIED, "foreign owner object")
        return NextActionOwnerEvent(
            "next-action-owner-event-" + canonical_hash([subject_ref, event_kind, replacement_ref]),
            subject_ref,
            subject_kind,
            event_kind,
            replacement_ref,
            disposition,
            now.astimezone(UTC),
            self.__seal,
        )

    def recognizes_event(self, event: NextActionOwnerEvent) -> bool:
        return event._authority_seal is self.__seal


_DEFAULT_NEXT_ACTION_POLICY_AUTHORITY = P1_8NextActionPolicyAuthority()


def default_next_action_policy_authority() -> P1_8NextActionPolicyAuthority:
    return _DEFAULT_NEXT_ACTION_POLICY_AUTHORITY


def _descriptor_identity_payload(value: NextActionDescriptor) -> dict[str, object]:
    return {
        "action_id": value.action_ref.action_id,
        "action_version": value.action_ref.action_version,
        "allowed_selection_modes": sorted(item.value for item in value.allowed_selection_modes),
        "authority_revision": value.authority_revision,
        "catalog_id": value.source_authority_ref.split(":")[-2],
        "critical_path_ordinal": value.critical_path_ordinal,
        "current_projection_on_invalidation": (value.current_projection_on_invalidation.value),
        "dependency_ordinal": value.dependency_ordinal,
        "descriptor_policy_ordinal": value.descriptor_policy_ordinal,
        "descriptor_version": value.descriptor_version,
        "effective_sequence": value.effective_sequence,
        "eligibility_policy_id": value.action_ref.eligibility_policy_id,
        "eligibility_policy_version": value.action_ref.eligibility_policy_version,
        "human_input_kind": value.required_human_input_kind.value,
        "parameter_rules": value.parameter_rules,
        "parameter_schema_fingerprint": value.parameter_schema_fingerprint,
        "parameter_schema_id": value.parameter_schema_id,
        "parameter_schema_version": value.parameter_schema_version,
        "priority_classification_source_hash": value.priority_classification_source_hash,
        "priority_classification_source_ref": value.priority_classification_source_ref,
        "priority_rank": value.priority_rank,
        "privacy_restrictions": list(value.privacy_restrictions),
        "project_restriction": value.project_restriction,
        "scope_restrictions": value.scope_restrictions,
        "security_restrictions": list(value.security_restrictions),
        "source_authority_fingerprint": value.source_authority_fingerprint,
        "source_authority_ref": value.source_authority_ref,
        "source_authority_version": value.source_authority_version,
        "source_kind": value.source_kind.value,
        "supersedes_ref": value.supersedes_ref,
        "revocation_ref": value.revocation_ref,
        "task_issuance_owner": value.task_issuance_owner,
        "task_template_hash": value.task_template_hash,
        "task_template_ref": value.task_template_ref,
    }


def validate_parameters(descriptor: NextActionDescriptor, values: dict[str, Any]) -> None:
    if set(values) != set(descriptor.parameter_rules):
        raise NextActionError(
            NextActionErrorCode.NOT_ENROLLED, "parameters differ from descriptor schema"
        )
    types = {"string": str, "integer": int, "boolean": bool, "array": list}
    for key, kind in descriptor.parameter_rules.items():
        expected = types.get(kind)
        if expected is None or type(values[key]) is not expected:
            raise NextActionError(
                NextActionErrorCode.NOT_ENROLLED, "parameter type differs from descriptor"
            )


def ranking_key(
    proposal: NextActionProposal,
    descriptor: NextActionDescriptor,
    *,
    authoritative_priority_rank: int | None = None,
    enrolled_critical_path_ordinal: int | None = None,
) -> tuple[int, int, int, int, str, str]:
    validate_parameters(descriptor, proposal.parameters)
    return (
        (
            descriptor.priority_rank
            if authoritative_priority_rank is None
            else authoritative_priority_rank
        ),
        descriptor.dependency_ordinal,
        (
            descriptor.critical_path_ordinal
            if enrolled_critical_path_ordinal is None
            else enrolled_critical_path_ordinal
        ),
        descriptor.descriptor_policy_ordinal,
        descriptor.action_ref.serialized,
        proposal.proposal_id,
    )


@dataclass(frozen=True, slots=True)
class NextActionEvaluation:
    evaluation_id: str
    project_id: str
    project_revision: int
    mode: NextActionSelectionMode
    ranked_proposal_ids: tuple[str, ...]
    eligibility_policy_ref: str
    eligibility_policy_fingerprint: str
    selection_policy_ref: str
    selection_policy_fingerprint: str
    descriptor_enrollment_id: str
    owner_event_high_watermark: int
    authoritative_input_refs: tuple[str, ...]
    operational_work_run_id: str | None
    human_judgment_ref: str | None
    evaluated_at: datetime
    authoritative_priority_rank: int | None = None
    enrolled_critical_path_ordinal: int | None = None
    external_priority_class: str | None = None
    external_context_ref: str | None = None
    external_context_fingerprint: str | None = None
    external_context_owner_high_watermark: int | None = None
    memory_authority_event_high_watermark: int | None = None


@dataclass(frozen=True, slots=True)
class NextActionSelection:
    selection_id: str
    selection_version: str
    project_id: str
    project_revision: int
    evaluation_id: str
    proposal_id: str
    action_ref: ActionRef
    descriptor_version: str
    descriptor_fingerprint: str
    parameters: dict[str, Any]
    memory_refs: tuple[str, ...]
    selected_at: datetime
    external_context_ref: str | None = None
    external_context_fingerprint: str | None = None
    external_context_snapshot_ref: str | None = None
    external_context_snapshot_fingerprint: str | None = None
    external_context_event_high_watermark: int | None = None
    memory_authority_event_high_watermark: int | None = None

    @property
    def fingerprint(self) -> str:
        return canonical_hash(
            {
                "action_ref": self.action_ref.serialized,
                "descriptor_fingerprint": self.descriptor_fingerprint,
                "descriptor_version": self.descriptor_version,
                "evaluation_id": self.evaluation_id,
                "memory_refs": list(self.memory_refs),
                "parameters": self.parameters,
                "project_id": self.project_id,
                "project_revision": self.project_revision,
                "proposal_id": self.proposal_id,
                "selected_at": self.selected_at.astimezone(UTC).isoformat(),
                "selection_id": self.selection_id,
                "selection_version": self.selection_version,
                "external_context_ref": self.external_context_ref,
                "external_context_fingerprint": self.external_context_fingerprint,
                "external_context_snapshot_ref": self.external_context_snapshot_ref,
                "external_context_snapshot_fingerprint": (
                    self.external_context_snapshot_fingerprint
                ),
                "external_context_event_high_watermark": (
                    self.external_context_event_high_watermark
                ),
                "memory_authority_event_high_watermark": (
                    self.memory_authority_event_high_watermark
                ),
            }
        )


@dataclass(frozen=True, slots=True)
class TaskIssuanceCandidate:
    candidate_id: str
    selection_ref: str
    action_ref: ActionRef
    parameters: dict[str, Any]
    issuance_owner: str
    required_post_issuance_human_input: HumanInputKind
    created_at: datetime

    def __post_init__(self) -> None:
        if self.issuance_owner != TASK_ISSUANCE_OWNER:
            raise ValueError("Task issuance owner is external and fixed")
