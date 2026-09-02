from __future__ import annotations

import hashlib
import json
import unicodedata
from collections.abc import Mapping, Sequence
from typing import Any, TypeGuard

MAX_SAFE_INTEGER = 9_007_199_254_740_991


class CanonicalJSONError(ValueError):
    """The value is outside the AISCC JCS/safe-integer contract."""


def is_safe_integer(value: object) -> TypeGuard[int]:
    return type(value) is int and -MAX_SAFE_INTEGER <= value <= MAX_SAFE_INTEGER


def require_safe_integer(
    value: object,
    *,
    label: str,
    minimum: int = -MAX_SAFE_INTEGER,
    maximum: int = MAX_SAFE_INTEGER,
) -> int:
    if type(value) is not int:
        raise CanonicalJSONError(f"{label} must be a JSON integer (bool/float forbidden)")
    if not -MAX_SAFE_INTEGER <= value <= MAX_SAFE_INTEGER:
        raise CanonicalJSONError(f"{label} exceeds the JCS safe-integer range")
    if not minimum <= value <= maximum:
        raise CanonicalJSONError(f"{label} must be in {minimum}..{maximum}")
    return value


def require_exact_fields(
    value: Mapping[str, object],
    *,
    required: frozenset[str],
    optional: frozenset[str] = frozenset(),
    label: str,
) -> None:
    actual = frozenset(value)
    missing = required - actual
    unknown = actual - required - optional
    if missing or unknown:
        raise CanonicalJSONError(
            f"{label} fields differ (missing={sorted(missing)}, unknown={sorted(unknown)})"
        )


def canonical_json_bytes(value: object) -> bytes:
    """Return UTF-8 RFC 8785 bytes for the JSON subset used by normative AISCC payloads.

    Normative AISCC payloads reject floats and integers outside the interoperable IEEE-754
    range. Strings and object keys must already be NFC; this function never silently repairs
    authority bytes. Object ordering uses UTF-16 code units as required by RFC 8785.
    """

    return _serialize(_validated(value)).encode("utf-8")


def canonical_json_text(value: object) -> str:
    return canonical_json_bytes(value).decode("utf-8")


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def verify_canonical_json_bytes(value: bytes) -> object:
    if value.startswith(b"\xef\xbb\xbf"):
        raise CanonicalJSONError("UTF-8 BOM is forbidden")
    try:
        decoded = value.decode("utf-8")
        parsed = json.loads(
            decoded,
            parse_float=lambda _: _raise("float is forbidden"),
            parse_int=int,
            parse_constant=lambda _: _raise("NaN/Infinity are forbidden"),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CanonicalJSONError("invalid UTF-8 JSON") from exc
    canonical = canonical_json_bytes(parsed)
    if canonical != value:
        raise CanonicalJSONError("JSON bytes are not canonical JCS bytes")
    return parsed


def _raise(message: str) -> Any:
    raise CanonicalJSONError(message)


def _validated(value: object) -> object:
    if value is None or type(value) is bool:
        return value
    if type(value) is int:
        return require_safe_integer(value, label="integer")
    if isinstance(value, float):
        raise CanonicalJSONError("float/NaN/Infinity are forbidden")
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise CanonicalJSONError("strings must already be Unicode NFC")
        try:
            value.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise CanonicalJSONError("unpaired Unicode surrogate is forbidden") from exc
        return value
    if isinstance(value, Mapping):
        result: dict[str, object] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise CanonicalJSONError("JSON object keys must be strings")
            normalized_key = _validated(key)
            assert isinstance(normalized_key, str)
            result[normalized_key] = _validated(item)
        return result
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_validated(item) for item in value]
    raise CanonicalJSONError(f"unsupported JSON value: {type(value).__name__}")


def _serialize(value: object) -> str:
    if value is None:
        return "null"
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is int:
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(",", ":"))
    if isinstance(value, list):
        return "[" + ",".join(_serialize(item) for item in value) + "]"
    if isinstance(value, dict):
        ordered = sorted(value, key=lambda item: item.encode("utf-16be"))
        return (
            "{" + ",".join(f"{_serialize(key)}:{_serialize(value[key])}" for key in ordered) + "}"
        )
    raise AssertionError(f"validated JSON value has unexpected type: {type(value).__name__}")
