from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from aiscc.contracts.canonical_json import (
    MAX_SAFE_INTEGER,
    CanonicalJSONError,
    canonical_json_bytes,
    canonical_sha256,
    require_exact_fields,
    require_safe_integer,
    verify_canonical_json_bytes,
)

EXPECTED_SCHEMA_FINGERPRINTS = {
    "988cdd4c71aca75e3434652044b50ffd703fb32ba4568219c56d52e498cd8698",
    "f2b090057ae3f5f00ed4ef878a41664e2322988190969458e6a6544f76932f6b",
    "842ac2619a3069a0b844cbaf89d36ceb252bfe1f1ec149097727f224a6cdc307",
    "59e695623329908fdabce214a1d80be4249b4767c86844749de93094aeb7fce4",
    "db08fb7cbe1b55b7c686df28ffccbaf8462dd27dea7416e9b4478ae40e6cd67f",
    "6de3e66a0d16a1dc0038838eb58b9ca0ca6c2d790ab3a5cdcab3802b5093b508",
    "c3bba5050a43a37c2563518d862a4b7fc1c3ee344cd763ab66da19d15a7126cc",
    "2b4bd41b7dbf7f002f2b48aabcf816ac386d860c12c20e947843bee5390c9b00",
    "41330e2502ae9c337a3a1e8dfc693b2fb9307bec9eb5b5138e33ad7cdd35c1aa",
    "ec170cd257b04e77410951abe8c7f196a88bf8f35d9e6deaec8d8889bb0e9d0c",
    "b984abd21d657015d3b3febbe55588762ee481ea93fcfff868114b09b5943329",
    "0d92603174460dfd59be4b5bcb7a577014e8b51dad98fe992f08c3f638c43dbd",
    "bef330ffba29c24a76910d22c2de514235224add40b2725d4ac342a25dc4a7ed",
    "d173e426e651497abbf45ba4abb6f38bdc9e9d54e4b3a63e76c33aa9e7edb2a2",
    "4f84dbae89ee1113a2f6eeb28aa5d00100fcb65db2694b8716b52925d9bb312d",
    "92fe98cbc7cae63ab1f72161b625eb9bbd3281592f7731f98d24f30b4dd326f1",
    "3e4407fef8f429031038018d8ee8fab0cb91ad583277f28e0d75064b226ea646",
    "c02290f5111608efbd3cd12edec9e066ca622133f262a1352d971fcddf02e58c",
    "a0425bee1c2abf26c50a63ff125795e88e0b15e6f182dfbf716fc5f0217d6d03",
}


def _accepted_json_vectors() -> dict[str, object]:
    root = Path(__file__).parents[3]
    paths = (
        root / ".aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md",
        root / ".aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md",
    )
    result: dict[str, object] = {}
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for raw in re.findall(r"```json\s*\n([^`]+?)\n```", text):
            value = json.loads(raw)
            fingerprint = canonical_sha256(value)
            if fingerprint in EXPECTED_SCHEMA_FINGERPRINTS:
                result[fingerprint] = value
    return result


def test_all_22_accepted_payload_fingerprints_reproduce_exactly() -> None:
    vectors = _accepted_json_vectors()
    assert set(vectors) == EXPECTED_SCHEMA_FINGERPRINTS
    catalog = vectors["c02290f5111608efbd3cd12edec9e066ca622133f262a1352d971fcddf02e58c"]
    assert isinstance(catalog, dict)
    entries = catalog["entries"]
    assert isinstance(entries, list) and len(entries) == 2
    common = {
        "catalog_ref": "p1-8-policy-action-catalog:v1:P1_8_POLICY_ACTION_CATALOG",
        "catalog_fingerprint": ("c02290f5111608efbd3cd12edec9e066ca622133f262a1352d971fcddf02e58c"),
    }
    operational = {
        "descriptor_schema": "p1-8-next-action-descriptor-v1",
        **common,
        "entry": entries[0],
    }
    action_ref = {
        "eligibility_policy_id": "P1_8_NEXT_ACTION_ELIGIBILITY_POLICY",
        "eligibility_policy_version": "v1",
        "action_id": "open-operational-recovery-task-issuance",
        "action_version": "v1",
        "descriptor_fingerprint": canonical_sha256(operational),
    }
    template = {
        "descriptor_schema": "p1-8-next-action-descriptor-template-v1",
        **common,
        "entry": entries[1],
    }
    assert canonical_sha256(operational) == (
        "77bf03ba2125b32daef565739274a853cbfa03faab6477e37f4f9108517af8b0"
    )
    assert canonical_sha256(action_ref) == (
        "a6a272fc7757439b7cc0877ace775d091539c25a4c3be8c0cd973cf2b746f157"
    )
    assert canonical_sha256(template) == (
        "7b766d3d3f3062381ebc1792cb4e4bc4768bf7be8963d8adff5b7e5a1bf29ddf"
    )
    assert len(vectors) + 3 == 22


def test_safe_integer_bool_float_nfc_and_canonical_bytes_fail_closed() -> None:
    assert require_safe_integer(MAX_SAFE_INTEGER, label="sequence", minimum=1) == (MAX_SAFE_INTEGER)
    for value in (MAX_SAFE_INTEGER + 1, True, 1.0):
        with pytest.raises(CanonicalJSONError):
            require_safe_integer(value, label="sequence", minimum=1)
    with pytest.raises(CanonicalJSONError):
        canonical_json_bytes({"value": 1.0})
    with pytest.raises(CanonicalJSONError):
        canonical_json_bytes({"value": "e\u0301"})
    with pytest.raises(CanonicalJSONError):
        verify_canonical_json_bytes(b'{"b":1,"a":2}')
    assert verify_canonical_json_bytes(b'{"a":2,"b":1}') == {"a": 2, "b": 1}


def test_exact_schema_validator_denies_unknown_fields() -> None:
    with pytest.raises(CanonicalJSONError):
        require_exact_fields(
            {"required": "ok", "unknown": "denied"},
            required=frozenset({"required"}),
            label="test payload",
        )
