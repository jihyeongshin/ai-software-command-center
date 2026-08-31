from __future__ import annotations

import hashlib
import json
import unicodedata
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from typing import Any

from aiscc.evidence.models import (
    DurableContentError,
    DurableContentErrorCode,
    DurableEvidenceContentObject,
    EvidenceCandidate,
    EvidenceContentKind,
    EvidenceContentRef,
    EvidenceSensitivity,
    HistoricalContentAccessGrant,
    canonical_hash,
    canonical_json_bytes,
)

CANONICALIZATION_V1 = "AISCC_CANONICAL_STRUCTURED_JSON_V1"
DURABLE_CONTENT_AUTHORITY_ID = "AISCC_P1_6_DURABLE_CONTENT_AUTHORITY_V1"
DURABLE_CONTENT_AUTHORITY_VERSION = "1"
DURABLE_CONTENT_AUTHORITY_REVISION = 1
DURABLE_CONTENT_PAYLOAD_SCHEMA = "p1-6-durable-content-payload-v1"
DURABLE_CONTENT_IDENTITY_SCHEMA = "p1-6-durable-content-identity-v1"
DURABLE_CONTENT_RETENTION_POLICY = "P1_8_HISTORICAL_RECONSTRUCTION_RETAIN_V1"
MAX_DURABLE_CONTENT_BYTES = 65_536
MAX_DURABLE_CONTENT_DEPTH = 32
MAX_DURABLE_CONTENT_NODES = 4_096
P1_8_STRUCTURED_RESULT_CONSUMER = "P1_8"
P1_8_STRUCTURED_RESULT_PURPOSE = "P1_8_STRUCTURED_RESULT_V1"

DURABLE_CONTENT_KINDS = frozenset(
    {
        EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY,
        EvidenceContentKind.DATABASE_OBSERVATION_REF,
        EvidenceContentKind.RUNTIME_OBSERVATION_REF,
    }
)
DURABLE_CONTENT_SENSITIVITIES = frozenset(
    {EvidenceSensitivity.PUBLIC_SAFE, EvidenceSensitivity.INTERNAL}
)


@dataclass(frozen=True, slots=True)
class PreparedDurableEvidenceContent:
    content: DurableEvidenceContentObject
    content_ref: EvidenceContentRef
    _writer_token: object


class P1_6DurableContentAuthority:
    """The sole application authority that can prepare PostgreSQL durable content writes."""

    def __init__(self) -> None:
        self._writer_token = object()

    def prepare_structured(
        self,
        *,
        owner_id: str,
        owner_version: str,
        source_owner_authority_ref: str,
        source_owner_authority_fingerprint: str,
        object_id: str,
        object_version: str,
        value: Any,
        kind: EvidenceContentKind,
        schema_id: str,
        schema_version: str,
        sensitivity: EvidenceSensitivity,
        access_policy: str = "PRIVATE_AUTHORITY_ONLY",
        created_at: datetime | None = None,
    ) -> PreparedDurableEvidenceContent:
        if kind not in DURABLE_CONTENT_KINDS:
            raise DurableContentError(
                DurableContentErrorCode.KIND_NOT_SUPPORTED,
                f"{kind.value} is not in the V1 durable allowlist",
            )
        if sensitivity not in DURABLE_CONTENT_SENSITIVITIES:
            raise DurableContentError(
                DurableContentErrorCode.SENSITIVITY_DENIED,
                f"{sensitivity.value} cannot be stored as durable structured content",
            )
        if not all(
            (
                owner_id,
                owner_version,
                source_owner_authority_ref,
                object_id,
                object_version,
                schema_id,
                schema_version,
            )
        ):
            raise DurableContentError(
                DurableContentErrorCode.SCHEMA_MISMATCH,
                "durable owner/object/schema identity is required",
            )
        _require_sha256(source_owner_authority_fingerprint, "source owner authority")
        if access_policy not in {"PRIVATE_AUTHORITY_ONLY", "PUBLIC_SAFE_EXPORT"}:
            raise DurableContentError(
                DurableContentErrorCode.ACCESS_DENIED,
                "unsupported durable content access policy",
            )
        if (
            access_policy == "PUBLIC_SAFE_EXPORT"
            and sensitivity is not EvidenceSensitivity.PUBLIC_SAFE
        ):
            raise DurableContentError(
                DurableContentErrorCode.ACCESS_DENIED,
                "public body export requires PUBLIC_SAFE sensitivity",
            )
        canonical_body = canonicalize_structured_json(value)
        issued_at = (created_at or datetime.now(UTC)).astimezone(UTC)
        identity = {
            "identity_schema": DURABLE_CONTENT_IDENTITY_SCHEMA,
            "owner_id": owner_id,
            "owner_version": owner_version,
            "object_id": object_id,
            "object_version": object_version,
        }
        identity_key = canonical_hash(identity)
        serialized_ref = f"p1-6-durable-content:v1:{identity_key}"
        content_hash = hashlib.sha256(canonical_body).hexdigest()
        metadata: dict[str, object] = {
            "serialized_ref": serialized_ref,
            "content_identity_key": identity_key,
            "owner_id": owner_id,
            "owner_version": owner_version,
            "source_owner_authority_ref": source_owner_authority_ref,
            "source_owner_authority_fingerprint": source_owner_authority_fingerprint,
            "object_id": object_id,
            "object_version": object_version,
            "content_kind": kind.value,
            "canonicalization": CANONICALIZATION_V1,
            "schema_id": schema_id,
            "schema_version": schema_version,
            "byte_count": len(canonical_body),
            "content_hash_algorithm": "SHA-256",
            "content_hash": content_hash,
            "sensitivity": sensitivity.value,
            "retention_policy": DURABLE_CONTENT_RETENTION_POLICY,
            "access_policy": access_policy,
            "created_at": issued_at.isoformat(),
            "content_authority_id": DURABLE_CONTENT_AUTHORITY_ID,
            "content_authority_version": DURABLE_CONTENT_AUTHORITY_VERSION,
            "content_authority_revision": DURABLE_CONTENT_AUTHORITY_REVISION,
            "payload_fingerprint_schema": DURABLE_CONTENT_PAYLOAD_SCHEMA,
        }
        payload_fingerprint = canonical_hash(metadata)
        content = DurableEvidenceContentObject(
            serialized_ref=serialized_ref,
            content_identity_key=identity_key,
            owner_id=owner_id,
            owner_version=owner_version,
            source_owner_authority_ref=source_owner_authority_ref,
            source_owner_authority_fingerprint=source_owner_authority_fingerprint,
            object_id=object_id,
            object_version=object_version,
            content_kind=kind,
            canonicalization=CANONICALIZATION_V1,
            schema_id=schema_id,
            schema_version=schema_version,
            byte_count=len(canonical_body),
            content_hash_algorithm="SHA-256",
            content_hash=content_hash,
            sensitivity=sensitivity,
            retention_policy=DURABLE_CONTENT_RETENTION_POLICY,
            access_policy=access_policy,
            canonical_body_bytes=canonical_body,
            created_at=issued_at,
            content_authority_id=DURABLE_CONTENT_AUTHORITY_ID,
            content_authority_version=DURABLE_CONTENT_AUTHORITY_VERSION,
            content_authority_revision=DURABLE_CONTENT_AUTHORITY_REVISION,
            payload_fingerprint_schema=DURABLE_CONTENT_PAYLOAD_SCHEMA,
            payload_fingerprint=payload_fingerprint,
        )
        content_ref = EvidenceContentRef(
            content_kind=kind,
            owner_id=owner_id,
            owner_version=owner_version,
            object_id=object_id,
            object_version=object_version,
            canonicalization=CANONICALIZATION_V1,
            schema_id=schema_id,
            schema_version=schema_version,
            byte_count=len(canonical_body),
            content_hash=content_hash,
            sensitivity=sensitivity,
            retention_policy=DURABLE_CONTENT_RETENTION_POLICY,
            access_policy=access_policy,
            _owner_token=self._writer_token,
        )
        return PreparedDurableEvidenceContent(content, content_ref, self._writer_token)

    def recognizes(self, prepared: PreparedDurableEvidenceContent) -> bool:
        return prepared._writer_token is self._writer_token


class P1_6HistoricalContentAccessAuthority:
    """P1-6 owner of current, purpose-bounded historical body read capability."""

    _P1_8_SENSITIVITY_CEILING = frozenset(
        {EvidenceSensitivity.PUBLIC_SAFE, EvidenceSensitivity.INTERNAL}
    )
    _INTERNAL_READ_ACCESS_POLICIES = frozenset(
        {"PRIVATE_AUTHORITY_ONLY", "PUBLIC_SAFE_EXPORT"}
    )

    def __init__(self) -> None:
        self._read_token = object()

    def issue_p1_8_structured_result_grant(self) -> HistoricalContentAccessGrant:
        return HistoricalContentAccessGrant(
            consumer=P1_8_STRUCTURED_RESULT_CONSUMER,
            purpose=P1_8_STRUCTURED_RESULT_PURPOSE,
            _capability_token=self._read_token,
        )

    def recognizes(self, grant: HistoricalContentAccessGrant) -> bool:
        return bool(
            grant._capability_token is self._read_token
            and grant.consumer == P1_8_STRUCTURED_RESULT_CONSUMER
            and grant.purpose == P1_8_STRUCTURED_RESULT_PURPOSE
        )

    def allows_historical_read(
        self,
        grant: HistoricalContentAccessGrant,
        content: DurableEvidenceContentObject,
    ) -> bool:
        return bool(
            self.recognizes(grant)
            and content.sensitivity in self._P1_8_SENSITIVITY_CEILING
            and content.access_policy in self._INTERNAL_READ_ACCESS_POLICIES
        )


def canonicalize_structured_json(value: Any) -> bytes:
    parsed = _parse_json_bytes(value) if isinstance(value, bytes) else value
    counter = [0]
    normalized = _normalize_json(parsed, depth=1, counter=counter)
    try:
        body = json.dumps(
            normalized,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise DurableContentError(
            DurableContentErrorCode.SCHEMA_MISMATCH,
            "structured content cannot be serialized canonically",
        ) from exc
    if not 1 <= len(body) <= MAX_DURABLE_CONTENT_BYTES:
        raise DurableContentError(
            DurableContentErrorCode.TOO_LARGE,
            "canonical structured body is outside 1..65,536 bytes",
        )
    return body


def source_owner_authority_fingerprint(candidate: EvidenceCandidate) -> str:
    """Fingerprint the already registered producer authority; never caller-authored content."""
    return canonical_hash(
        {
            "issuer": [
                candidate.issuer.owner_type.value,
                candidate.issuer.owner_id,
                candidate.issuer.owner_version,
                candidate.issuer.authority_ref,
            ],
            "producer_attestation_ref": candidate.producer_attestation_ref,
        }
    )


def _parse_json_bytes(value: bytes) -> Any:
    if not 1 <= len(value) <= MAX_DURABLE_CONTENT_BYTES:
        raise DurableContentError(
            DurableContentErrorCode.TOO_LARGE,
            "raw structured body is outside 1..65,536 bytes",
        )
    if value.startswith(b"\xef\xbb\xbf"):
        raise DurableContentError(
            DurableContentErrorCode.SCHEMA_MISMATCH,
            "UTF-8 BOM is forbidden",
        )

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        normalized_keys: set[str] = set()
        for key, item in items:
            if key in result:
                raise DurableContentError(
                    DurableContentErrorCode.SCHEMA_MISMATCH,
                    "duplicate object key",
                )
            normalized_key = unicodedata.normalize("NFC", key)
            if normalized_key in normalized_keys:
                raise DurableContentError(
                    DurableContentErrorCode.SCHEMA_MISMATCH,
                    "object keys collide after NFC normalization",
                )
            result[key] = item
            normalized_keys.add(normalized_key)
        return result

    def reject_number(_: str) -> Any:
        raise DurableContentError(
            DurableContentErrorCode.SCHEMA_MISMATCH,
            "floating-point, NaN, and Infinity are forbidden",
        )

    try:
        return json.loads(
            value.decode("utf-8"),
            object_pairs_hook=pairs,
            parse_float=reject_number,
            parse_constant=reject_number,
        )
    except DurableContentError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise DurableContentError(
            DurableContentErrorCode.SCHEMA_MISMATCH,
            "structured content is not strict UTF-8 JSON",
        ) from exc


def _normalize_json(value: Any, *, depth: int, counter: list[int]) -> Any:
    if type(value) in {list, dict} and depth > MAX_DURABLE_CONTENT_DEPTH:
        raise DurableContentError(
            DurableContentErrorCode.TOO_LARGE,
            "structured content exceeds maximum nesting depth 32",
        )
    counter[0] += 1
    if counter[0] > MAX_DURABLE_CONTENT_NODES:
        raise DurableContentError(
            DurableContentErrorCode.TOO_LARGE,
            "structured content exceeds maximum 4,096 value/key nodes",
        )
    if value is None or type(value) is bool:
        return value
    if type(value) is int:
        if not -(2**63) <= value <= 2**63 - 1:
            raise DurableContentError(
                DurableContentErrorCode.SCHEMA_MISMATCH,
                "integer is outside signed 64-bit range",
            )
        return value
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if type(value) is list:
        return [
            _normalize_json(item, depth=depth + 1, counter=counter) for item in value
        ]
    if type(value) is dict:
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise DurableContentError(
                    DurableContentErrorCode.SCHEMA_MISMATCH,
                    "object keys must be strings",
                )
            counter[0] += 1
            if counter[0] > MAX_DURABLE_CONTENT_NODES:
                raise DurableContentError(
                    DurableContentErrorCode.TOO_LARGE,
                    "structured content exceeds maximum 4,096 value/key nodes",
                )
            normalized_key = unicodedata.normalize("NFC", key)
            if normalized_key in normalized:
                raise DurableContentError(
                    DurableContentErrorCode.SCHEMA_MISMATCH,
                    "object keys collide after NFC normalization",
                )
            normalized[normalized_key] = _normalize_json(
                item, depth=depth + 1, counter=counter
            )
        return normalized
    raise DurableContentError(
        DurableContentErrorCode.SCHEMA_MISMATCH,
        "only null, boolean, signed integer, string, array, and object are supported",
    )


def _require_sha256(value: str, label: str) -> None:
    if (
        len(value) != 64
        or value.lower() != value
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise DurableContentError(
            DurableContentErrorCode.SCHEMA_MISMATCH,
            f"{label} fingerprint must be lowercase SHA-256",
        )


class PrivateEvidenceContentStore:
    """Owner-backed immutable bytes; arbitrary paths and URLs are never resolution inputs."""

    def __init__(self, owner_id: str, owner_version: str) -> None:
        if not owner_id or not owner_version:
            raise ValueError("content owner identity is required")
        self.owner_id = owner_id
        self.owner_version = owner_version
        self._owner_token = object()
        self._objects: dict[tuple[str, str], bytes] = {}

    def put_structured(
        self,
        *,
        object_id: str,
        object_version: str,
        value: Any,
        kind: EvidenceContentKind,
        schema_id: str,
        schema_version: str,
        sensitivity: EvidenceSensitivity,
        retention_policy: str = "TASK_AUTHORITY_RETENTION_V1",
        access_policy: str = "PRIVATE_AUTHORITY_ONLY",
    ) -> EvidenceContentRef:
        if kind not in {
            EvidenceContentKind.INLINE_CANONICAL_STRUCTURED_BODY,
            EvidenceContentKind.DATABASE_OBSERVATION_REF,
            EvidenceContentKind.RUNTIME_OBSERVATION_REF,
            EvidenceContentKind.HUMAN_STRUCTURED_REF,
        }:
            raise ValueError("structured content kind is not owner-backed structured evidence")
        try:
            body = canonical_json_bytes(value)
            json.loads(body)
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            raise ValueError("structured evidence is not canonical JSON") from exc
        return self._put(
            object_id=object_id,
            object_version=object_version,
            body=body,
            kind=kind,
            canonicalization="RFC8785_SUBSET_SORTED_JSON_V1",
            schema_id=schema_id,
            schema_version=schema_version,
            sensitivity=sensitivity,
            retention_policy=retention_policy,
            access_policy=access_policy,
        )

    def put_bytes(
        self,
        *,
        object_id: str,
        object_version: str,
        body: bytes,
        kind: EvidenceContentKind = EvidenceContentKind.CONTENT_ADDRESSED_ARTIFACT_REF,
        schema_id: str = "AISCC-RAW-BYTES",
        schema_version: str = "1",
        sensitivity: EvidenceSensitivity = EvidenceSensitivity.INTERNAL,
        retention_policy: str = "TASK_AUTHORITY_RETENTION_V1",
        access_policy: str = "PRIVATE_AUTHORITY_ONLY",
    ) -> EvidenceContentRef:
        if kind is not EvidenceContentKind.CONTENT_ADDRESSED_ARTIFACT_REF:
            raise ValueError("raw bytes require CONTENT_ADDRESSED_ARTIFACT_REF")
        return self._put(
            object_id=object_id,
            object_version=object_version,
            body=body,
            kind=kind,
            canonicalization="EXACT_RAW_BYTES",
            schema_id=schema_id,
            schema_version=schema_version,
            sensitivity=sensitivity,
            retention_policy=retention_policy,
            access_policy=access_policy,
        )

    def put_p1_5_producer_bytes(
        self,
        *,
        object_id: str,
        object_version: str,
        body: bytes,
        schema_id: str,
        schema_version: str,
        sensitivity: EvidenceSensitivity = EvidenceSensitivity.INTERNAL,
    ) -> EvidenceContentRef:
        return self._put(
            object_id=object_id,
            object_version=object_version,
            body=body,
            kind=EvidenceContentKind.P1_5_IMMUTABLE_PRODUCER_REF,
            canonicalization="P1_5_IMMUTABLE_REF_EXACT_BYTES",
            schema_id=schema_id,
            schema_version=schema_version,
            sensitivity=sensitivity,
            retention_policy="P1_5_PRIVATE_REF_RETENTION_V1",
            access_policy="PRIVATE_AUTHORITY_ONLY",
        )

    def _put(
        self,
        *,
        object_id: str,
        object_version: str,
        body: bytes,
        kind: EvidenceContentKind,
        canonicalization: str,
        schema_id: str,
        schema_version: str,
        sensitivity: EvidenceSensitivity,
        retention_policy: str,
        access_policy: str,
    ) -> EvidenceContentRef:
        if sensitivity is EvidenceSensitivity.SECRET_FORBIDDEN:
            raise ValueError("raw secret material cannot enter the evidence content store")
        if not object_id or not object_version or not body:
            raise ValueError("immutable evidence content identity/body is required")
        key = (object_id, object_version)
        existing = self._objects.get(key)
        if existing is not None and existing != body:
            raise ValueError("immutable evidence content identity conflict")
        self._objects[key] = bytes(body)
        return EvidenceContentRef(
            content_kind=kind,
            owner_id=self.owner_id,
            owner_version=self.owner_version,
            object_id=object_id,
            object_version=object_version,
            canonicalization=canonicalization,
            schema_id=schema_id,
            schema_version=schema_version,
            byte_count=len(body),
            content_hash=hashlib.sha256(body).hexdigest(),
            sensitivity=sensitivity,
            retention_policy=retention_policy,
            access_policy=access_policy,
            _owner_token=self._owner_token,
        )

    def resolve(self, ref: EvidenceContentRef) -> bytes | None:
        if (
            ref.owner_id != self.owner_id
            or ref.owner_version != self.owner_version
            or ref._owner_token is not self._owner_token
        ):
            return None
        body = self._objects.get((ref.object_id, ref.object_version))
        return bytes(body) if body is not None else None

    def public_export(self, ref: EvidenceContentRef) -> bytes | None:
        if (
            ref.sensitivity is not EvidenceSensitivity.PUBLIC_SAFE
            or ref.access_policy != "PUBLIC_SAFE_EXPORT"
        ):
            return None
        return self.resolve(ref)

    def tampered_ref(self, ref: EvidenceContentRef, *, content_hash: str) -> EvidenceContentRef:
        """Test/support constructor; resolution remains owner-token bound."""
        return replace(ref, content_hash=content_hash)
