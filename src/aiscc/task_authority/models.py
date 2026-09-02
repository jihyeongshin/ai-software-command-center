from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from aiscc.contracts.canonical_json import (
    MAX_SAFE_INTEGER,
    canonical_sha256,
    require_safe_integer,
)

EXTERNAL_TASK_AUTHORITY_OWNER = "EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY"
TASK_CONSTRAINT_AUTHORITY_REF = "external-command-center-task-authority:task-constraint:v1"
TASK_CONSTRAINT_AUTHORITY_VERSION = "AISCC-EXTERNAL-COMMAND-CENTER-TASK-CONSTRAINT-AUTHORITY-V1"
NEXT_ACTION_CONTEXT_AUTHORITY_REF = (
    "external-command-center-task-authority:next-action-context-source:v1"
)
NEXT_ACTION_CONTEXT_AUTHORITY_VERSION = (
    "AISCC-EXTERNAL-COMMAND-CENTER-NEXT-ACTION-CONTEXT-AUTHORITY-V1"
)
AUTHORITY_REVISION = 1

TASK_CONSTRAINT_REF_SCHEMA_FINGERPRINT = (
    "c3bba5050a43a37c2563518d862a4b7fc1c3ee344cd763ab66da19d15a7126cc"
)
TASK_CONSTRAINT_EVENT_SCHEMA_FINGERPRINT = (
    "2b4bd41b7dbf7f002f2b48aabcf816ac386d860c12c20e947843bee5390c9b00"
)
TASK_CONSTRAINT_SNAPSHOT_SCHEMA_FINGERPRINT = (
    "41330e2502ae9c337a3a1e8dfc693b2fb9307bec9eb5b5138e33ad7cdd35c1aa"
)
NEXT_ACTION_CONTEXT_SOURCE_CONTRACT_FINGERPRINT = (
    "988cdd4c71aca75e3434652044b50ffd703fb32ba4568219c56d52e498cd8698"
)
NEXT_ACTION_CONTEXT_PRIORITY_ENROLLMENT_FINGERPRINT = (
    "f2b090057ae3f5f00ed4ef878a41664e2322988190969458e6a6544f76932f6b"
)
NEXT_ACTION_CONTEXT_REF_SCHEMA_FINGERPRINT = (
    "842ac2619a3069a0b844cbaf89d36ceb252bfe1f1ec149097727f224a6cdc307"
)
NEXT_ACTION_CONTEXT_EVENT_SCHEMA_FINGERPRINT = (
    "59e695623329908fdabce214a1d80be4249b4767c86844749de93094aeb7fce4"
)
NEXT_ACTION_CONTEXT_RESULT_SCHEMA_FINGERPRINT = (
    "db08fb7cbe1b55b7c686df28ffccbaf8462dd27dea7416e9b4478ae40e6cd67f"
)
NEXT_ACTION_CONTEXT_MEMORY_DERIVATION_FINGERPRINT = (
    "6de3e66a0d16a1dc0038838eb58b9ca0ca6c2d790ab3a5cdcab3802b5093b508"
)

_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:/@-]{0,159}\Z", re.ASCII)
_VERSION = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,63}\Z", re.ASCII)
_LOCAL_ID = re.compile(r"[a-z0-9][a-z0-9._:@-]{0,159}\Z", re.ASCII)
_SLOT_ID = re.compile(r"[a-z0-9][a-z0-9._-]{0,63}\Z", re.ASCII)
_FINGERPRINT = re.compile(r"[0-9a-f]{64}\Z", re.ASCII)


class ExternalTaskAuthorityErrorCode(StrEnum):
    IDENTITY_CONFLICT = "EXTERNAL_TASK_AUTHORITY_IDENTITY_CONFLICT"
    AUTHORITY_CONFLICT = "EXTERNAL_TASK_AUTHORITY_CONFLICT"
    HISTORY_CORRUPT = "EXTERNAL_TASK_AUTHORITY_EVENT_HISTORY_CORRUPT"
    CAPABILITY_DENIED = "EXTERNAL_TASK_AUTHORITY_CAPABILITY_DENIED"
    NOT_CURRENT = "EXTERNAL_TASK_AUTHORITY_NOT_CURRENT"
    SCOPE_MISMATCH = "EXTERNAL_TASK_AUTHORITY_SCOPE_MISMATCH"


class ExternalTaskAuthorityError(RuntimeError):
    def __init__(self, code: ExternalTaskAuthorityErrorCode, message: str) -> None:
        super().__init__(f"{code.value}: {message}")
        self.code = code


class TaskConstraintScopeKind(StrEnum):
    PROJECT = "PROJECT"
    TASK_CONTRACT = "TASK_CONTRACT"
    WORK_RUN = "WORK_RUN"


class AuthorityEventKind(StrEnum):
    ISSUED = "ISSUED"
    SUPERSEDED = "SUPERSEDED"
    REVOKED = "REVOKED"


class CurrentProjectionDisposition(StrEnum):
    RETAIN_CURRENT = "RETAIN_CURRENT"
    WITHDRAW_CURRENT = "WITHDRAW_CURRENT"


class NextActionPriorityClass(StrEnum):
    ACCEPTED_CORE_CRITICAL_PATH = "ACCEPTED_CORE_CRITICAL_PATH"
    OPERATIONAL_HARDENING = "OPERATIONAL_HARDENING"
    OPTIONAL_OPTIMIZATION = "OPTIONAL_OPTIMIZATION"


@dataclass(frozen=True, slots=True)
class TaskConstraintScopeV1:
    scope_kind: TaskConstraintScopeKind
    project_id: str
    task_contract_id: str | None = None
    task_contract_version: str | None = None
    work_run_id: str | None = None

    def __post_init__(self) -> None:
        _require_id(self.project_id, "project_id")
        if self.scope_kind is TaskConstraintScopeKind.PROJECT:
            if any(
                item is not None
                for item in (
                    self.task_contract_id,
                    self.task_contract_version,
                    self.work_run_id,
                )
            ):
                raise ValueError("PROJECT forbids TaskContract and WorkRun fields")
        elif self.scope_kind is TaskConstraintScopeKind.TASK_CONTRACT:
            _require_id(self.task_contract_id, "task_contract_id")
            _require_version(self.task_contract_version, "task_contract_version")
            if self.work_run_id is not None:
                raise ValueError("TASK_CONTRACT forbids work_run_id")
        else:
            _require_id(self.task_contract_id, "task_contract_id")
            _require_version(self.task_contract_version, "task_contract_version")
            _require_id(self.work_run_id, "work_run_id")

    def payload(self) -> dict[str, str]:
        result = {"scope_kind": self.scope_kind.value, "project_id": self.project_id}
        if self.task_contract_id is not None:
            result["task_contract_id"] = self.task_contract_id
        if self.task_contract_version is not None:
            result["task_contract_version"] = self.task_contract_version
        if self.work_run_id is not None:
            result["work_run_id"] = self.work_run_id
        return result

    @property
    def logical_key_fragment(self) -> str:
        return canonical_sha256(self.payload())


@dataclass(frozen=True, slots=True)
class TaskConstraintRefV1:
    constraint_ref: str
    constraint_ref_id: str
    constraint_ref_version: str
    fingerprint_schema: str
    constraint_owner: str
    authority_ref: str
    authority_version: str
    authority_revision: int
    logical_constraint_id: str
    scope: TaskConstraintScopeV1
    constraint_schema_id: str
    constraint_schema_version: str
    constraint_payload_ref: str
    constraint_payload_fingerprint: str
    issued_at: datetime
    issuance_sequence: int
    constraint_fingerprint: str

    def __post_init__(self) -> None:
        _require_local_id(self.constraint_ref_id, "constraint_ref_id")
        _require_local_id(self.logical_constraint_id, "logical_constraint_id")
        _require_id(self.constraint_schema_id, "constraint_schema_id")
        _require_version(self.constraint_schema_version, "constraint_schema_version")
        _require_id(self.constraint_payload_ref, "constraint_payload_ref")
        _require_fingerprint(self.constraint_payload_fingerprint, "constraint payload")
        _require_fingerprint(self.constraint_fingerprint, "constraint")
        _require_sequence(self.issuance_sequence, "issuance_sequence")
        _require_timestamp(self.issued_at)
        if (
            self.constraint_ref != f"task-constraint:v1:{self.constraint_ref_id}"
            or self.constraint_ref_version != "v1"
            or self.fingerprint_schema != "task-constraint-ref-v1"
            or self.constraint_owner != EXTERNAL_TASK_AUTHORITY_OWNER
            or self.authority_ref != TASK_CONSTRAINT_AUTHORITY_REF
            or self.authority_version != TASK_CONSTRAINT_AUTHORITY_VERSION
            or self.authority_revision != AUTHORITY_REVISION
            or canonical_sha256(self.fingerprint_payload()) != self.constraint_fingerprint
        ):
            raise ValueError("TaskConstraintRefV1 immutable identity differs")

    def fingerprint_payload(self) -> dict[str, object]:
        return {
            "constraint_ref": self.constraint_ref,
            "constraint_ref_id": self.constraint_ref_id,
            "constraint_ref_version": self.constraint_ref_version,
            "fingerprint_schema": self.fingerprint_schema,
            "constraint_owner": self.constraint_owner,
            "authority_ref": self.authority_ref,
            "authority_version": self.authority_version,
            "authority_revision": self.authority_revision,
            "logical_constraint_id": self.logical_constraint_id,
            "scope": self.scope.payload(),
            "constraint_schema_id": self.constraint_schema_id,
            "constraint_schema_version": self.constraint_schema_version,
            "constraint_payload_ref": self.constraint_payload_ref,
            "constraint_payload_fingerprint": self.constraint_payload_fingerprint,
            "issued_at": _timestamp(self.issued_at),
            "issuance_sequence": self.issuance_sequence,
        }

    @property
    def logical_key(self) -> str:
        return canonical_sha256(
            {
                "logical_constraint_id": self.logical_constraint_id,
                "scope": self.scope.payload(),
            }
        )


@dataclass(frozen=True, slots=True)
class TaskConstraintAuthorityEventV1:
    event_ref: str
    event_id: str
    event_version: str
    fingerprint_schema: str
    event_kind: AuthorityEventKind
    constraint_ref: str
    constraint_fingerprint: str
    replacement_constraint_ref: str | None
    replacement_constraint_fingerprint: str | None
    logical_constraint_id: str
    scope: TaskConstraintScopeV1
    authority_ref: str
    authority_version: str
    authority_revision: int
    event_sequence: int
    effective_sequence: int
    effective_at: datetime
    current_projection_disposition: CurrentProjectionDisposition
    event_fingerprint: str

    def __post_init__(self) -> None:
        _require_local_id(self.event_id, "event_id")
        _require_local_id(self.logical_constraint_id, "logical_constraint_id")
        _require_fingerprint(self.constraint_fingerprint, "constraint")
        _require_fingerprint(self.event_fingerprint, "event")
        _require_sequence(self.event_sequence, "event_sequence")
        _require_sequence(self.effective_sequence, "effective_sequence")
        _require_timestamp(self.effective_at)
        replacement_required = self.event_kind is AuthorityEventKind.SUPERSEDED
        if replacement_required:
            _require_id(self.replacement_constraint_ref, "replacement_constraint_ref")
            _require_fingerprint(self.replacement_constraint_fingerprint, "replacement constraint")
        elif (
            self.replacement_constraint_ref is not None
            or self.replacement_constraint_fingerprint is not None
        ):
            raise ValueError("ISSUED/REVOKED replacement fields must be JSON null")
        expected_disposition = (
            CurrentProjectionDisposition.RETAIN_CURRENT
            if self.event_kind is AuthorityEventKind.ISSUED
            else CurrentProjectionDisposition.WITHDRAW_CURRENT
        )
        if (
            self.event_ref != f"task-constraint-event:v1:{self.event_id}"
            or self.event_version != "v1"
            or self.fingerprint_schema != "task-constraint-authority-event-v1"
            or self.authority_ref != TASK_CONSTRAINT_AUTHORITY_REF
            or self.authority_version != TASK_CONSTRAINT_AUTHORITY_VERSION
            or self.authority_revision != AUTHORITY_REVISION
            or self.current_projection_disposition is not expected_disposition
            or canonical_sha256(self.fingerprint_payload()) != self.event_fingerprint
        ):
            raise ValueError("TaskConstraintAuthorityEventV1 immutable identity differs")

    def fingerprint_payload(self) -> dict[str, object]:
        return {
            "event_ref": self.event_ref,
            "event_id": self.event_id,
            "event_version": self.event_version,
            "fingerprint_schema": self.fingerprint_schema,
            "event_kind": self.event_kind.value,
            "constraint_ref": self.constraint_ref,
            "constraint_fingerprint": self.constraint_fingerprint,
            "replacement_constraint_ref": self.replacement_constraint_ref,
            "replacement_constraint_fingerprint": self.replacement_constraint_fingerprint,
            "logical_constraint_id": self.logical_constraint_id,
            "scope": self.scope.payload(),
            "authority_ref": self.authority_ref,
            "authority_version": self.authority_version,
            "authority_revision": self.authority_revision,
            "event_sequence": self.event_sequence,
            "effective_sequence": self.effective_sequence,
            "effective_at": _timestamp(self.effective_at),
            "current_projection_disposition": self.current_projection_disposition.value,
        }


@dataclass(frozen=True, slots=True)
class TaskConstraintOwnerSnapshotV1:
    snapshot_ref: str
    snapshot_version: str
    fingerprint_schema: str
    authority_ref: str
    authority_version: str
    authority_revision: int
    owner_event_high_watermark: int
    ordered_event_prefix_root: str
    issued_at: datetime
    snapshot_fingerprint: str

    def __post_init__(self) -> None:
        _require_fingerprint(self.ordered_event_prefix_root, "ordered prefix root")
        _require_fingerprint(self.snapshot_fingerprint, "snapshot")
        require_safe_integer(
            self.owner_event_high_watermark,
            label="owner_event_high_watermark",
            minimum=0,
        )
        _require_timestamp(self.issued_at)
        if (
            not self.snapshot_ref.startswith("task-constraint-owner-snapshot:v1:")
            or self.snapshot_version != "v1"
            or self.fingerprint_schema != "task-constraint-owner-snapshot-v1"
            or self.authority_ref != TASK_CONSTRAINT_AUTHORITY_REF
            or self.authority_version != TASK_CONSTRAINT_AUTHORITY_VERSION
            or self.authority_revision != AUTHORITY_REVISION
            or canonical_sha256(self.fingerprint_payload()) != self.snapshot_fingerprint
        ):
            raise ValueError("TaskConstraintOwnerSnapshotV1 immutable identity differs")

    def fingerprint_payload(self) -> dict[str, object]:
        return {
            "snapshot_ref": self.snapshot_ref,
            "snapshot_version": self.snapshot_version,
            "fingerprint_schema": self.fingerprint_schema,
            "authority_ref": self.authority_ref,
            "authority_version": self.authority_version,
            "authority_revision": self.authority_revision,
            "owner_event_high_watermark": self.owner_event_high_watermark,
            "ordered_event_prefix_root": self.ordered_event_prefix_root,
            "issued_at": _timestamp(self.issued_at),
        }


@dataclass(frozen=True, slots=True)
class NextActionContextRefV1:
    context_ref: str
    context_ref_id: str
    context_ref_version: str
    fingerprint_schema: str
    context_owner: str
    authority_ref: str
    authority_version: str
    authority_revision: int
    context_logical_id: str
    project_id: str
    scope_kind: str
    task_contract_id: str
    task_contract_version: str
    context_slot_id: str
    priority_class: NextActionPriorityClass
    critical_path_ordinal: int
    context_payload_schema_id: str
    context_payload_schema_version: str
    context_payload_schema_fingerprint: str
    privacy_class: str
    security_class: str
    issued_at: datetime
    issuance_sequence: int
    effective_sequence: int
    fingerprint: str

    def __post_init__(self) -> None:
        _require_local_id(self.context_ref_id, "context_ref_id")
        if not self.context_logical_id.startswith("next-action-context-lineage:v1:"):
            raise ValueError("context_logical_id grammar differs")
        _require_local_id(self.context_logical_id.rsplit(":", 1)[-1], "context logical local ID")
        _require_id(self.project_id, "project_id")
        _require_id(self.task_contract_id, "task_contract_id")
        _require_version(self.task_contract_version, "task_contract_version")
        if _SLOT_ID.fullmatch(self.context_slot_id) is None:
            raise ValueError("context_slot_id grammar differs")
        require_safe_integer(
            self.critical_path_ordinal,
            label="critical_path_ordinal",
            minimum=1,
            maximum=1_000_000,
        )
        _require_sequence(self.issuance_sequence, "issuance_sequence")
        _require_sequence(self.effective_sequence, "effective_sequence")
        _require_fingerprint(self.context_payload_schema_fingerprint, "context result schema")
        _require_fingerprint(self.fingerprint, "context")
        _require_timestamp(self.issued_at)
        fixed = (
            self.context_ref == f"next-action-context:v1:{self.context_ref_id}"
            and self.context_ref_version == "v1"
            and self.fingerprint_schema == "next-action-context-ref-v1"
            and self.context_owner == EXTERNAL_TASK_AUTHORITY_OWNER
            and self.authority_ref == NEXT_ACTION_CONTEXT_AUTHORITY_REF
            and self.authority_version == NEXT_ACTION_CONTEXT_AUTHORITY_VERSION
            and self.authority_revision == AUTHORITY_REVISION
            and self.scope_kind == "TASK_CONTRACT"
            and self.context_payload_schema_id == "P1_8_NEXT_ACTION_CONTEXT_RESULT_V1"
            and self.context_payload_schema_version == "v1"
            and self.context_payload_schema_fingerprint
            == NEXT_ACTION_CONTEXT_RESULT_SCHEMA_FINGERPRINT
            and self.privacy_class == "PRIVATE_INTERNAL"
            and self.security_class == "INTERNAL_REFERENCE_ONLY"
        )
        if not fixed or canonical_sha256(self.fingerprint_payload()) != self.fingerprint:
            raise ValueError("NextActionContextRefV1 immutable identity differs")

    def fingerprint_payload(self) -> dict[str, object]:
        return {
            "context_ref": self.context_ref,
            "context_ref_id": self.context_ref_id,
            "context_ref_version": self.context_ref_version,
            "fingerprint_schema": self.fingerprint_schema,
            "context_owner": self.context_owner,
            "authority_ref": self.authority_ref,
            "authority_version": self.authority_version,
            "authority_revision": self.authority_revision,
            "context_logical_id": self.context_logical_id,
            "project_id": self.project_id,
            "scope_kind": self.scope_kind,
            "task_contract_id": self.task_contract_id,
            "task_contract_version": self.task_contract_version,
            "context_slot_id": self.context_slot_id,
            "priority_class": self.priority_class.value,
            "critical_path_ordinal": self.critical_path_ordinal,
            "context_payload_schema_id": self.context_payload_schema_id,
            "context_payload_schema_version": self.context_payload_schema_version,
            "context_payload_schema_fingerprint": self.context_payload_schema_fingerprint,
            "privacy_class": self.privacy_class,
            "security_class": self.security_class,
            "issued_at": _timestamp(self.issued_at),
            "issuance_sequence": self.issuance_sequence,
            "effective_sequence": self.effective_sequence,
        }

    @property
    def logical_key(self) -> str:
        return canonical_sha256(
            {
                "project_id": self.project_id,
                "task_contract_id": self.task_contract_id,
                "task_contract_version": self.task_contract_version,
                "context_logical_id": self.context_logical_id,
                "context_slot_id": self.context_slot_id,
            }
        )


@dataclass(frozen=True, slots=True)
class NextActionContextAuthorityEventV1:
    event_ref: str
    event_id: str
    event_version: str
    fingerprint_schema: str
    event_kind: AuthorityEventKind
    context_ref: str
    context_fingerprint: str
    replacement_context_ref: str | None
    replacement_context_fingerprint: str | None
    project_id: str
    task_contract_id: str
    task_contract_version: str
    context_logical_id: str
    context_slot_id: str
    authority_ref: str
    authority_version: str
    authority_revision: int
    event_sequence: int
    effective_sequence: int
    effective_at: datetime
    current_projection_disposition: CurrentProjectionDisposition
    event_fingerprint: str

    def __post_init__(self) -> None:
        _require_local_id(self.event_id, "event_id")
        _require_fingerprint(self.context_fingerprint, "context")
        _require_fingerprint(self.event_fingerprint, "context event")
        _require_sequence(self.event_sequence, "event_sequence")
        _require_sequence(self.effective_sequence, "effective_sequence")
        _require_timestamp(self.effective_at)
        if self.event_kind is AuthorityEventKind.SUPERSEDED:
            _require_id(self.replacement_context_ref, "replacement_context_ref")
            _require_fingerprint(self.replacement_context_fingerprint, "replacement context")
        elif (
            self.replacement_context_ref is not None
            or self.replacement_context_fingerprint is not None
        ):
            raise ValueError("ISSUED/REVOKED replacement fields must be JSON null")
        expected_disposition = (
            CurrentProjectionDisposition.RETAIN_CURRENT
            if self.event_kind is AuthorityEventKind.ISSUED
            else CurrentProjectionDisposition.WITHDRAW_CURRENT
        )
        if (
            self.event_ref != f"next-action-context-event:v1:{self.event_id}"
            or self.event_version != "v1"
            or self.fingerprint_schema != "next-action-context-authority-event-v1"
            or self.authority_ref != NEXT_ACTION_CONTEXT_AUTHORITY_REF
            or self.authority_version != NEXT_ACTION_CONTEXT_AUTHORITY_VERSION
            or self.authority_revision != AUTHORITY_REVISION
            or self.current_projection_disposition is not expected_disposition
            or canonical_sha256(self.fingerprint_payload()) != self.event_fingerprint
        ):
            raise ValueError("NextActionContextAuthorityEventV1 immutable identity differs")

    def fingerprint_payload(self) -> dict[str, object]:
        return {
            "event_ref": self.event_ref,
            "event_id": self.event_id,
            "event_version": self.event_version,
            "fingerprint_schema": self.fingerprint_schema,
            "event_kind": self.event_kind.value,
            "context_ref": self.context_ref,
            "context_fingerprint": self.context_fingerprint,
            "replacement_context_ref": self.replacement_context_ref,
            "replacement_context_fingerprint": self.replacement_context_fingerprint,
            "project_id": self.project_id,
            "task_contract_id": self.task_contract_id,
            "task_contract_version": self.task_contract_version,
            "context_logical_id": self.context_logical_id,
            "context_slot_id": self.context_slot_id,
            "authority_ref": self.authority_ref,
            "authority_version": self.authority_version,
            "authority_revision": self.authority_revision,
            "event_sequence": self.event_sequence,
            "effective_sequence": self.effective_sequence,
            "effective_at": _timestamp(self.effective_at),
            "current_projection_disposition": self.current_projection_disposition.value,
        }


@dataclass(frozen=True, slots=True)
class TaskConstraintFoldResult:
    current: TaskConstraintRefV1 | None
    consumed_event_refs: tuple[str, ...]
    snapshot_ref: str
    snapshot_fingerprint: str
    owner_event_high_watermark: int


@dataclass(frozen=True, slots=True)
class NextActionContextFoldResult:
    current: NextActionContextRefV1 | None
    consumed_event_refs: tuple[str, ...]
    snapshot_ref: str
    snapshot_fingerprint: str
    owner_event_high_watermark: int


def ordered_event_prefix_root(pairs: tuple[tuple[str, str], ...]) -> str:
    return canonical_sha256([[event_ref, fingerprint] for event_ref, fingerprint in pairs])


def task_constraint_ref_from_payload(payload: dict[str, Any]) -> TaskConstraintRefV1:
    raw_scope = payload["scope"]
    if not isinstance(raw_scope, dict):
        raise ValueError("TaskConstraint scope payload is malformed")
    scope = TaskConstraintScopeV1(
        TaskConstraintScopeKind(str(raw_scope["scope_kind"])),
        str(raw_scope["project_id"]),
        _optional_str(raw_scope.get("task_contract_id")),
        _optional_str(raw_scope.get("task_contract_version")),
        _optional_str(raw_scope.get("work_run_id")),
    )
    return TaskConstraintRefV1(
        constraint_ref=str(payload["constraint_ref"]),
        constraint_ref_id=str(payload["constraint_ref_id"]),
        constraint_ref_version=str(payload["constraint_ref_version"]),
        fingerprint_schema=str(payload["fingerprint_schema"]),
        constraint_owner=str(payload["constraint_owner"]),
        authority_ref=str(payload["authority_ref"]),
        authority_version=str(payload["authority_version"]),
        authority_revision=int(payload["authority_revision"]),
        logical_constraint_id=str(payload["logical_constraint_id"]),
        scope=scope,
        constraint_schema_id=str(payload["constraint_schema_id"]),
        constraint_schema_version=str(payload["constraint_schema_version"]),
        constraint_payload_ref=str(payload["constraint_payload_ref"]),
        constraint_payload_fingerprint=str(payload["constraint_payload_fingerprint"]),
        issued_at=_parse_timestamp(str(payload["issued_at"])),
        issuance_sequence=int(payload["issuance_sequence"]),
        constraint_fingerprint=str(payload["constraint_fingerprint"]),
    )


def next_action_context_ref_from_payload(payload: dict[str, Any]) -> NextActionContextRefV1:
    return NextActionContextRefV1(
        context_ref=str(payload["context_ref"]),
        context_ref_id=str(payload["context_ref_id"]),
        context_ref_version=str(payload["context_ref_version"]),
        fingerprint_schema=str(payload["fingerprint_schema"]),
        context_owner=str(payload["context_owner"]),
        authority_ref=str(payload["authority_ref"]),
        authority_version=str(payload["authority_version"]),
        authority_revision=int(payload["authority_revision"]),
        context_logical_id=str(payload["context_logical_id"]),
        project_id=str(payload["project_id"]),
        scope_kind=str(payload["scope_kind"]),
        task_contract_id=str(payload["task_contract_id"]),
        task_contract_version=str(payload["task_contract_version"]),
        context_slot_id=str(payload["context_slot_id"]),
        priority_class=NextActionPriorityClass(str(payload["priority_class"])),
        critical_path_ordinal=int(payload["critical_path_ordinal"]),
        context_payload_schema_id=str(payload["context_payload_schema_id"]),
        context_payload_schema_version=str(payload["context_payload_schema_version"]),
        context_payload_schema_fingerprint=str(payload["context_payload_schema_fingerprint"]),
        privacy_class=str(payload["privacy_class"]),
        security_class=str(payload["security_class"]),
        issued_at=_parse_timestamp(str(payload["issued_at"])),
        issuance_sequence=int(payload["issuance_sequence"]),
        effective_sequence=int(payload["effective_sequence"]),
        fingerprint=str(payload["fingerprint"]),
    )


def _timestamp(value: datetime) -> str:
    return value.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _parse_timestamp(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=UTC)


def _require_timestamp(value: datetime) -> None:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("authority timestamp must be timezone-aware")


def _require_id(value: object, label: str) -> None:
    if not isinstance(value, str) or _ID.fullmatch(value) is None:
        raise ValueError(f"{label} grammar differs")


def _require_version(value: object, label: str) -> None:
    if not isinstance(value, str) or _VERSION.fullmatch(value) is None:
        raise ValueError(f"{label} grammar differs")


def _require_local_id(value: object, label: str) -> None:
    if not isinstance(value, str) or _LOCAL_ID.fullmatch(value) is None:
        raise ValueError(f"{label} grammar differs")


def _require_fingerprint(value: object, label: str) -> None:
    if not isinstance(value, str) or _FINGERPRINT.fullmatch(value) is None:
        raise ValueError(f"{label} fingerprint grammar differs")


def _require_sequence(value: object, label: str) -> None:
    require_safe_integer(value, label=label, minimum=1, maximum=MAX_SAFE_INTEGER)


def _optional_str(value: object) -> str | None:
    return None if value is None else str(value)
