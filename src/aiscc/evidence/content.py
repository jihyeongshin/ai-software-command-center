from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from typing import Any

from aiscc.evidence.models import (
    EvidenceContentKind,
    EvidenceContentRef,
    EvidenceSensitivity,
    canonical_json_bytes,
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
