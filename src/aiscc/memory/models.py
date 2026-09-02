from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from aiscc.cycle.models import MemoryCategory, MemoryDeclaration
from aiscc.evidence.models import canonical_hash

MEMORY_CONTENT_FINGERPRINT_SCHEMA = "p1-8-memory-content-v1"
MEMORY_LINEAGE_KEY_SCHEMA = "p1-8-memory-lineage-v1"
MEMORY_POLICY_AUTHORITY = "P1_8_MEMORY_DECLARATION_POLICY_AUTHORITY_V1"
_ATOM = re.compile(r"[a-z0-9][a-z0-9._:/@-]{0,159}\Z")


class MemoryAuthorityMode(StrEnum):
    DETERMINISTIC_POINTER = "DETERMINISTIC_POINTER"
    STRUCTURED_RESULT_ATTESTED = "STRUCTURED_RESULT_ATTESTED"
    OWNER_ATTESTED = "OWNER_ATTESTED"
    NOT_SUPPORTED = "NOT_SUPPORTED"


class MemoryApplicabilityState(StrEnum):
    CURRENT = "CURRENT"
    SUPERSEDED = "SUPERSEDED"
    REVOKED = "REVOKED"
    EXPIRED = "EXPIRED"


class PrivacyClassification(StrEnum):
    INTERNAL = "INTERNAL"
    PUBLIC_SANITIZED = "PUBLIC_SANITIZED"
    NON_EXPORTABLE = "NON_EXPORTABLE"


class CurrentProjectionDisposition(StrEnum):
    RETAIN_CURRENT = "RETAIN_CURRENT"
    WITHDRAW_CURRENT = "WITHDRAW_CURRENT"


@dataclass(frozen=True, slots=True)
class MemoryCategorySourceContract:
    category: MemoryCategory
    authority_mode: MemoryAuthorityMode
    allowed_source_object_kinds: tuple[str, ...]
    source_schema_id: str
    source_schema_version: str
    source_selector: str
    content_derivation_schema: str
    canonicalization: str
    subject_derivation_rule: str
    applicability_derivation_rule: str
    semantic_slot_derivation_rule: str
    privacy_ceiling: PrivacyClassification
    export_ceiling: str
    policy_slot_id: str
    static_source_authority_ref: str = "NONE"
    static_source_authority_fingerprint: str = "NONE"

    def payload(self) -> dict[str, object]:
        return {
            "allowed_source_object_kinds": list(self.allowed_source_object_kinds),
            "applicability_derivation_rule": self.applicability_derivation_rule,
            "authority_mode": self.authority_mode.value,
            "canonicalization": self.canonicalization,
            "category": self.category.value,
            "content_derivation_schema": self.content_derivation_schema,
            "export_ceiling": self.export_ceiling,
            "policy_slot_id": self.policy_slot_id,
            "privacy_ceiling": self.privacy_ceiling.value,
            "semantic_slot_derivation_rule": self.semantic_slot_derivation_rule,
            "source_schema_id": self.source_schema_id,
            "source_schema_version": self.source_schema_version,
            "source_selector": self.source_selector,
            "static_source_authority_fingerprint": self.static_source_authority_fingerprint,
            "static_source_authority_ref": self.static_source_authority_ref,
            "subject_derivation_rule": self.subject_derivation_rule,
        }


CATEGORY_MODES = {
    MemoryCategory.DECISION: MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED,
    MemoryCategory.INVARIANT_POINTER: MemoryAuthorityMode.DETERMINISTIC_POINTER,
    MemoryCategory.CONSTRAINT_POINTER: MemoryAuthorityMode.DETERMINISTIC_POINTER,
    MemoryCategory.LESSON: MemoryAuthorityMode.NOT_SUPPORTED,
    MemoryCategory.BLOCKER_RESOLUTION: MemoryAuthorityMode.DETERMINISTIC_POINTER,
    MemoryCategory.PROVENANCE_POINTER: MemoryAuthorityMode.DETERMINISTIC_POINTER,
    MemoryCategory.NEXT_ACTION_CONTEXT: MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED,
}


class ProjectMemoryErrorCode(StrEnum):
    CONTENT_MISMATCH = "MEMORY_CONTENT_FINGERPRINT_MISMATCH"
    LINEAGE_ATOM_INVALID = "MEMORY_LINEAGE_ATOM_INVALID"
    DIRECT_WRITE_FORBIDDEN = "DIRECT_PROJECT_MEMORY_WRITE_FORBIDDEN"
    SUPERSESSION_AUTHORITY_REQUIRED = "MEMORY_SUPERSESSION_AUTHORITY_REQUIRED"
    MULTIPLE_CURRENT_TIPS = "MEMORY_MULTIPLE_CURRENT_TIPS"
    PROJECTION_CORRUPT = "MEMORY_PROJECTION_CORRUPT"
    PRIVACY_DENIED = "MEMORY_PRIVACY_CLEARANCE_DENIED"
    NOT_CURRENT = "MEMORY_NOT_CURRENT_CONTEXT"
    AUTHORITY_DENIED = "MEMORY_POLICY_AUTHORITY_ACCESS_DENIED"
    SOURCE_MISMATCH = "MEMORY_DECLARATION_SOURCE_MISMATCH"
    AUTHORITY_NOT_FOUND = "MEMORY_DECLARATION_AUTHORITY_NOT_FOUND"


class ProjectMemoryError(RuntimeError):
    def __init__(self, code: ProjectMemoryErrorCode, message: str) -> None:
        super().__init__(f"{code.value}: {message}")
        self.code = code


@dataclass(frozen=True, slots=True)
class MemoryDeclarationAuthorityPolicy:
    policy_id: str
    policy_version: str
    authority_id: str
    authority_version: str
    authority_revision: int
    category_modes: dict[MemoryCategory, MemoryAuthorityMode]
    structured_selectors: dict[MemoryCategory, str]
    category_priority: dict[MemoryCategory, int]
    issued_at: datetime
    category_contracts: dict[MemoryCategory, MemoryCategorySourceContract] = field(
        default_factory=dict
    )
    effective_sequence: int = 1
    supersedes_policy_ref: str = "NONE"
    supersession_disposition: CurrentProjectionDisposition = (
        CurrentProjectionDisposition.WITHDRAW_CURRENT
    )
    revocation_disposition: CurrentProjectionDisposition = (
        CurrentProjectionDisposition.WITHDRAW_CURRENT
    )
    _authority_seal: object | None = field(default=None, repr=False, compare=False)

    @property
    def serialized_ref(self) -> str:
        return f"p1-8-memory-policy:{self.policy_version}:{self.policy_id}"

    @property
    def fingerprint(self) -> str:
        return canonical_hash(
            {
                "authority_id": self.authority_id,
                "authority_revision": self.authority_revision,
                "authority_version": self.authority_version,
                "category_modes": {
                    key.value: value.value
                    for key, value in sorted(
                        self.category_modes.items(), key=lambda item: item[0].value
                    )
                },
                "category_priority": {
                    key.value: value
                    for key, value in sorted(
                        self.category_priority.items(), key=lambda item: item[0].value
                    )
                },
                "category_contracts": {
                    key.value: value.payload()
                    for key, value in sorted(
                        self.category_contracts.items(), key=lambda item: item[0].value
                    )
                },
                "effective_sequence": self.effective_sequence,
                "policy_id": self.policy_id,
                "policy_version": self.policy_version,
                "revocation_disposition": self.revocation_disposition.value,
                "structured_selectors": {
                    key.value: value
                    for key, value in sorted(
                        self.structured_selectors.items(), key=lambda item: item[0].value
                    )
                },
                "supersedes_policy_ref": self.supersedes_policy_ref,
                "supersession_disposition": self.supersession_disposition.value,
            }
        )


@dataclass(frozen=True, slots=True)
class MemoryPolicyOwnerEvent:
    event_id: str
    policy_ref: str
    event_kind: str
    replacement_ref: str
    disposition: CurrentProjectionDisposition
    created_at: datetime
    _authority_seal: object | None = field(default=None, repr=False, compare=False)


class P1_8MemoryDeclarationPolicyAuthority:
    authority_id = MEMORY_POLICY_AUTHORITY
    authority_version = "AISCC-P1-8-MEMORY-POLICY-AUTHORITY-V1"

    def __init__(self) -> None:
        self.__seal = object()

    def issue_v1(self, now: datetime) -> MemoryDeclarationAuthorityPolicy:
        contracts = _v1_category_contracts()
        return MemoryDeclarationAuthorityPolicy(
            "project-memory-v1",
            "v1",
            self.authority_id,
            self.authority_version,
            1,
            dict(CATEGORY_MODES),
            {
                MemoryCategory.DECISION: "/decision",
                MemoryCategory.NEXT_ACTION_CONTEXT: "/next_action_context",
            },
            {category: ordinal for ordinal, category in enumerate(MemoryCategory, 1)},
            now.astimezone(UTC),
            contracts,
            1,
            "NONE",
            CurrentProjectionDisposition.WITHDRAW_CURRENT,
            CurrentProjectionDisposition.WITHDRAW_CURRENT,
            self.__seal,
        )

    def recognizes(self, policy: MemoryDeclarationAuthorityPolicy) -> bool:
        return (
            policy._authority_seal is self.__seal
            and policy.authority_id == self.authority_id
            and policy.authority_version == self.authority_version
            and policy == self.issue_v1(policy.issued_at)
        )

    def invalidate(
        self,
        policy: MemoryDeclarationAuthorityPolicy,
        *,
        event_kind: str,
        replacement_ref: str = "NONE",
        now: datetime,
    ) -> MemoryPolicyOwnerEvent:
        if not self.recognizes(policy) or event_kind not in {"SUPERSEDED", "REVOKED"}:
            raise ProjectMemoryError(
                ProjectMemoryErrorCode.AUTHORITY_DENIED, "policy invalidation authority denied"
            )
        disposition = (
            policy.supersession_disposition
            if event_kind == "SUPERSEDED"
            else policy.revocation_disposition
        )
        return MemoryPolicyOwnerEvent(
            "memory-policy-" + canonical_hash([policy.serialized_ref, event_kind, replacement_ref]),
            policy.serialized_ref,
            event_kind,
            replacement_ref,
            disposition,
            now.astimezone(UTC),
            self.__seal,
        )

    def recognizes_event(self, event: MemoryPolicyOwnerEvent) -> bool:
        return event._authority_seal is self.__seal


_DEFAULT_MEMORY_POLICY_AUTHORITY = P1_8MemoryDeclarationPolicyAuthority()


def default_memory_policy_authority() -> P1_8MemoryDeclarationPolicyAuthority:
    return _DEFAULT_MEMORY_POLICY_AUTHORITY


def default_memory_policy(now: datetime) -> MemoryDeclarationAuthorityPolicy:
    return _DEFAULT_MEMORY_POLICY_AUTHORITY.issue_v1(now)


def _v1_category_contracts() -> dict[MemoryCategory, MemoryCategorySourceContract]:
    common = {
        "canonicalization": "JCS_RFC8785",
        "export_ceiling": "NO_AUTOMATIC_EXPORT",
    }
    return {
        MemoryCategory.DECISION: MemoryCategorySourceContract(
            MemoryCategory.DECISION,
            MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED,
            ("P1_6_ADMITTED_STRUCTURED_RESULT",),
            "AISCC-PROOF",
            "v1",
            "/decision",
            "P1_8_DECISION_DERIVATION_V1",
            **common,
            subject_derivation_rule="TASK_CONTRACT_ID",
            applicability_derivation_rule="PROJECT_ID",
            semantic_slot_derivation_rule="DECISION_SCHEMA_AND_POLICY_SLOT",
            privacy_ceiling=PrivacyClassification.INTERNAL,
            policy_slot_id="terminal-decision",
        ),
        MemoryCategory.NEXT_ACTION_CONTEXT: MemoryCategorySourceContract(
            MemoryCategory.NEXT_ACTION_CONTEXT,
            MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED,
            ("P1_6_ADMITTED_STRUCTURED_RESULT",),
            "AISCC-PROOF",
            "v1",
            "/next_action_context",
            "P1_8_NEXT_ACTION_CONTEXT_DERIVATION_V1",
            **common,
            subject_derivation_rule="TASK_CONTRACT_ID",
            applicability_derivation_rule="PROJECT_ID",
            semantic_slot_derivation_rule="CONTEXT_SCHEMA_AND_POLICY_SLOT",
            privacy_ceiling=PrivacyClassification.INTERNAL,
            policy_slot_id="terminal-context",
        ),
        MemoryCategory.PROVENANCE_POINTER: MemoryCategorySourceContract(
            MemoryCategory.PROVENANCE_POINTER,
            MemoryAuthorityMode.DETERMINISTIC_POINTER,
            (
                "P1_4_TRANSITION_DECISION",
                "P1_6_EVIDENCE_ATTESTATION",
                "P1_7_JUDGMENT",
            ),
            "P1_8_TERMINAL_PROVENANCE_POINTER_V1",
            "v1",
            "EXACT_TERMINAL_OBJECT",
            "P1_8_PROVENANCE_TUPLE_V1",
            **common,
            subject_derivation_rule="SOURCE_LOGICAL_ID",
            applicability_derivation_rule="PROJECT_ID",
            semantic_slot_derivation_rule="PROVENANCE_ROLE_KIND_LOGICAL_ID",
            privacy_ceiling=PrivacyClassification.INTERNAL,
            policy_slot_id="terminal-provenance",
        ),
        MemoryCategory.INVARIANT_POINTER: MemoryCategorySourceContract(
            MemoryCategory.INVARIANT_POINTER,
            MemoryAuthorityMode.DETERMINISTIC_POINTER,
            ("CANONICAL_RULE_ANCHOR",),
            "AISCC_CANONICAL_RULE_ANCHOR_V1",
            "v1",
            "EXACT_ENROLLED_ANCHOR",
            "P1_8_INVARIANT_POINTER_TUPLE_V1",
            **common,
            subject_derivation_rule="AUTHORITY_ID",
            applicability_derivation_rule="PROJECT_DOMAIN",
            semantic_slot_derivation_rule="AUTHORITY_ID_AND_ANCHOR",
            privacy_ceiling=PrivacyClassification.PUBLIC_SANITIZED,
            policy_slot_id="accepted-project-memory-rule",
            static_source_authority_ref=(
                ".aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md"
                "#project-memory-is-not-canonical-authority"
            ),
            static_source_authority_fingerprint=(
                "100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a"
            ),
        ),
    }


def normalized_atom(value: str) -> str:
    normalized = unicodedata.normalize("NFC", value)
    if normalized != value or _ATOM.fullmatch(normalized) is None:
        raise ProjectMemoryError(
            ProjectMemoryErrorCode.LINEAGE_ATOM_INVALID,
            "lineage atoms must be canonical lower-case bounded identifiers",
        )
    return normalized


def _context_atom(value: str) -> str:
    normalized = unicodedata.normalize("NFC", value)
    if (
        normalized != value
        or not value
        or len(value) > 512
        or any(
            not (character.isascii() and (character.isalnum() or character in "._:/@-"))
            for character in value
        )
    ):
        raise ProjectMemoryError(
            ProjectMemoryErrorCode.LINEAGE_ATOM_INVALID,
            "external context lineage atom is not canonical ASCII",
        )
    return normalized


def memory_lineage_key(
    *,
    project_id: str,
    category: MemoryCategory,
    subject_key: str,
    applicability_key: str,
    semantic_slot: str,
) -> str:
    atom = _context_atom if category is MemoryCategory.NEXT_ACTION_CONTEXT else normalized_atom
    payload = {
        "applicability_key": atom(applicability_key),
        "category": category.value,
        "lineage_key_schema": MEMORY_LINEAGE_KEY_SCHEMA,
        "project_id": normalized_atom(project_id),
        "semantic_slot": atom(semantic_slot),
        "subject_key": atom(subject_key),
    }
    return canonical_hash(payload)


def memory_content_fingerprint(
    *,
    category: MemoryCategory,
    authority_mode: MemoryAuthorityMode,
    policy_ref: str,
    normalized_derived_content: Any,
) -> str:
    return canonical_hash(
        {
            "authority_mode": authority_mode.value,
            "category": category.value,
            "fingerprint_schema": MEMORY_CONTENT_FINGERPRINT_SCHEMA,
            "normalized_derived_content": normalized_derived_content,
            "policy_ref": policy_ref,
        }
    )


def select_json_pointer(value: Any, pointer: str) -> Any:
    if pointer == "":
        return value
    if not pointer.startswith("/"):
        raise ProjectMemoryError(ProjectMemoryErrorCode.CONTENT_MISMATCH, "invalid selector")
    current = value
    for raw in pointer[1:].split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        if isinstance(current, dict) and token in current:
            current = current[token]
        elif isinstance(current, list) and token.isdigit() and int(token) < len(current):
            current = current[int(token)]
        else:
            raise ProjectMemoryError(ProjectMemoryErrorCode.CONTENT_MISMATCH, "selector absent")
    return current


@dataclass(frozen=True, slots=True)
class VerifiedMemorySource:
    object_kind: str
    authority_ref: str
    authority_fingerprint: str
    logical_id: str
    schema_id: str
    schema_version: str
    privacy: PrivacyClassification
    project_id: str
    task_contract_id: str
    content: Any
    provenance_role: str = "terminal"
    anchor_id: str = "NONE"


@dataclass(frozen=True, slots=True)
class DerivedMemoryDeclaration:
    authority_mode: MemoryAuthorityMode
    normalized_content: Any
    content_fingerprint: str
    subject_key: str
    applicability_key: str
    semantic_slot: str
    privacy: PrivacyClassification
    source_authority_ref: str
    source_authority_fingerprint: str


_PRIVACY_RANK = {
    PrivacyClassification.PUBLIC_SANITIZED: 0,
    PrivacyClassification.INTERNAL: 1,
    PrivacyClassification.NON_EXPORTABLE: 2,
}


def most_restrictive_privacy(
    source: PrivacyClassification, ceiling: PrivacyClassification
) -> PrivacyClassification:
    return source if _PRIVACY_RANK[source] >= _PRIVACY_RANK[ceiling] else ceiling


def derive_memory_declaration(
    declaration: MemoryDeclaration,
    policy: MemoryDeclarationAuthorityPolicy,
    *,
    source: VerifiedMemorySource,
) -> DerivedMemoryDeclaration:
    contract = policy.category_contracts.get(declaration.category)
    if contract is None:
        raise ProjectMemoryError(
            ProjectMemoryErrorCode.AUTHORITY_NOT_FOUND,
            f"no enrolled V1 source contract for {declaration.category.value}",
        )
    if (
        declaration.policy_ref != policy.serialized_ref
        or declaration.policy_fingerprint != policy.fingerprint
        or source.object_kind not in contract.allowed_source_object_kinds
        or source.schema_id != contract.source_schema_id
        or source.schema_version != contract.source_schema_version
        or (
            declaration.source_object_kind is not None
            and declaration.source_object_kind != source.object_kind
        )
        or (
            declaration.source_schema_id is not None
            and declaration.source_schema_id != source.schema_id
        )
        or (
            declaration.source_schema_version is not None
            and declaration.source_schema_version != source.schema_version
        )
    ):
        raise ProjectMemoryError(
            ProjectMemoryErrorCode.SOURCE_MISMATCH, "declaration/source/policy tuple differs"
        )
    if contract.authority_mode is MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED:
        if declaration.source_selector != contract.source_selector:
            raise ProjectMemoryError(
                ProjectMemoryErrorCode.SOURCE_MISMATCH, "structured selector differs"
            )
        content = select_json_pointer(source.content, contract.source_selector)
        if declaration.category is MemoryCategory.NEXT_ACTION_CONTEXT:
            context_fields = {
                "result_schema_id",
                "result_schema_version",
                "context_ref",
                "context_fingerprint",
                "context_logical_id",
                "context_introduction_event_ref",
                "context_introduction_event_fingerprint",
                "context_authority_event_high_watermark",
                "project_id",
                "task_contract_id",
                "task_contract_version",
                "context_slot_id",
                "priority_class",
                "critical_path_ordinal",
            }
            if not isinstance(content, dict) or set(content) != context_fields:
                raise ProjectMemoryError(
                    ProjectMemoryErrorCode.SOURCE_MISMATCH,
                    "NEXT_ACTION_CONTEXT body is not an exact object",
                )
            try:
                subject = _context_atom(str(content["context_logical_id"]))
                applicability = _context_atom(
                    "task-contract/"
                    f"{content['project_id']}/{content['task_contract_id']}@"
                    f"{content['task_contract_version']}"
                )
                slot = _context_atom(
                    "next-action-context/P1_8_NEXT_ACTION_CONTEXT_RESULT_V1/"
                    f"{content['context_slot_id']}"
                )
            except KeyError as exc:
                raise ProjectMemoryError(
                    ProjectMemoryErrorCode.SOURCE_MISMATCH,
                    "NEXT_ACTION_CONTEXT owner field is absent",
                ) from exc
            content = {
                key: content[key]
                for key in (
                    "context_ref",
                    "context_fingerprint",
                    "context_logical_id",
                    "project_id",
                    "task_contract_id",
                    "task_contract_version",
                    "context_slot_id",
                    "priority_class",
                    "critical_path_ordinal",
                )
            }
        else:
            subject = normalized_atom(f"task-contract:{source.task_contract_id}")
            applicability = normalized_atom(f"project:{source.project_id}")
            slot = normalized_atom(f"decision/{source.schema_id.lower()}/{contract.policy_slot_id}")
    elif declaration.category is MemoryCategory.PROVENANCE_POINTER:
        content = {
            "provenance_role": source.provenance_role,
            "source_fingerprint": source.authority_fingerprint,
            "source_logical_id": source.logical_id,
            "source_object_kind": source.object_kind,
            "source_ref": source.authority_ref,
        }
        subject = normalized_atom(source.logical_id)
        applicability = normalized_atom(f"project:{source.project_id}")
        slot = normalized_atom(
            f"provenance/{source.provenance_role}/{source.object_kind.lower()}/{source.logical_id}"
        )
    elif declaration.category is MemoryCategory.INVARIANT_POINTER:
        if (
            source.authority_ref != contract.static_source_authority_ref
            or source.authority_fingerprint != contract.static_source_authority_fingerprint
        ):
            raise ProjectMemoryError(
                ProjectMemoryErrorCode.SOURCE_MISMATCH, "canonical invariant authority differs"
            )
        content = {
            "anchor_id": source.anchor_id,
            "authority_fingerprint": source.authority_fingerprint,
            "authority_id": source.logical_id,
            "authority_ref": source.authority_ref,
        }
        subject = normalized_atom(source.logical_id)
        applicability = normalized_atom(f"project:{source.project_id}")
        slot = normalized_atom(f"invariant/{source.logical_id}/{source.anchor_id}")
    else:
        raise ProjectMemoryError(
            ProjectMemoryErrorCode.AUTHORITY_NOT_FOUND,
            f"{declaration.category.value} predecessor owner is not enrolled in V1",
        )
    claims = (declaration.subject_key, declaration.applicability_key, declaration.semantic_slot)
    if claims != (subject, applicability, slot):
        raise ProjectMemoryError(
            ProjectMemoryErrorCode.SOURCE_MISMATCH,
            "caller lineage claims differ from owner-derived lineage atoms",
        )
    fingerprint = memory_content_fingerprint(
        category=declaration.category,
        authority_mode=contract.authority_mode,
        policy_ref=policy.serialized_ref,
        normalized_derived_content=content,
    )
    if fingerprint != declaration.claimed_content_fingerprint:
        raise ProjectMemoryError(
            ProjectMemoryErrorCode.CONTENT_MISMATCH,
            "caller content claim differs from owner derivation",
        )
    return DerivedMemoryDeclaration(
        contract.authority_mode,
        content,
        fingerprint,
        subject,
        applicability,
        slot,
        most_restrictive_privacy(source.privacy, contract.privacy_ceiling),
        source.authority_ref,
        source.authority_fingerprint,
    )


def derive_memory_content(
    declaration: MemoryDeclaration,
    policy: MemoryDeclarationAuthorityPolicy,
    *,
    structured_source: Any | None,
    accepted_pointer_refs: frozenset[str],
) -> tuple[MemoryAuthorityMode, Any, str]:
    mode = policy.category_modes.get(declaration.category)
    if mode is None or mode is MemoryAuthorityMode.NOT_SUPPORTED:
        from aiscc.cycle.models import CycleAdmissionError, CycleAdmissionErrorCode

        raise CycleAdmissionError(
            CycleAdmissionErrorCode.UNSUPPORTED_MEMORY_CATEGORY,
            f"{declaration.category.value} is NOT_SUPPORTED in V1",
        )
    if (
        declaration.policy_ref != policy.serialized_ref
        or declaration.policy_fingerprint != policy.fingerprint
    ):
        raise ProjectMemoryError(ProjectMemoryErrorCode.CONTENT_MISMATCH, "policy binding differs")
    if mode is MemoryAuthorityMode.STRUCTURED_RESULT_ATTESTED:
        expected_selector = policy.structured_selectors.get(declaration.category)
        if (
            structured_source is None
            or declaration.source_evidence_ref is None
            or declaration.source_selector != expected_selector
        ):
            raise ProjectMemoryError(
                ProjectMemoryErrorCode.CONTENT_MISMATCH, "structured source binding differs"
            )
        derived = select_json_pointer(structured_source, expected_selector or "")
    else:
        if declaration.pointer_ref is None or declaration.pointer_ref not in accepted_pointer_refs:
            raise ProjectMemoryError(
                ProjectMemoryErrorCode.CONTENT_MISMATCH, "pointer lacks terminal authority"
            )
        derived = {"authority_ref": declaration.pointer_ref}
    fingerprint = memory_content_fingerprint(
        category=declaration.category,
        authority_mode=mode,
        policy_ref=policy.serialized_ref,
        normalized_derived_content=derived,
    )
    if fingerprint != declaration.claimed_content_fingerprint:
        raise ProjectMemoryError(
            ProjectMemoryErrorCode.CONTENT_MISMATCH, "caller claim differs from owner derivation"
        )
    return mode, derived, fingerprint


@dataclass(frozen=True, slots=True)
class ProjectMemoryEntry:
    entry_id: str
    memory_lineage_key: str
    project_id: str
    cycle_ref: str
    declaration_ordinal: int
    category: MemoryCategory
    subject_key: str
    applicability_key: str
    semantic_slot: str
    authority_mode: MemoryAuthorityMode
    policy_ref: str
    policy_fingerprint: str
    source_ref: str
    content_fingerprint: str
    normalized_content: Any
    privacy: PrivacyClassification
    created_at: datetime


def project_memory_entry_id(
    *,
    cycle_id: str,
    memory_declaration_ordinal: int,
    policy_fingerprint: str,
    memory_lineage_key_value: str,
    content_fingerprint: str,
) -> str:
    return canonical_hash(
        {
            "content_fingerprint": content_fingerprint,
            "cycle_id": cycle_id,
            "memory_declaration_ordinal": memory_declaration_ordinal,
            "memory_lineage_key": memory_lineage_key_value,
            "policy_fingerprint": policy_fingerprint,
        }
    )


@dataclass(frozen=True, slots=True)
class ProjectMemoryView:
    memory_lineage_key: str
    current_entry_id: str | None
    state: MemoryApplicabilityState
    reason: str
    authority_revision: int
    latest_event_sequence: int


@dataclass(frozen=True, slots=True)
class RetrievedMemory:
    entry: ProjectMemoryEntry
    state: MemoryApplicabilityState
    reason: str
    context_marker: str
