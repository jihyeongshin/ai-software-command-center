from __future__ import annotations

import re
from collections.abc import Mapping, Sequence

type JsonScalar = str | int | float | bool | None
type JsonValue = JsonScalar | list[JsonValue] | dict[str, JsonValue]

_SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


def redact_text(value: str, *, sensitive_values: tuple[str, ...] = ()) -> str:
    result = value
    for secret in sensitive_values:
        if secret:
            result = result.replace(secret, "[REDACTED]")
    for pattern in _SECRET_PATTERNS:
        result = pattern.sub("[REDACTED]", result)
    return result


def redact_structure(value: object, *, sensitive_values: tuple[str, ...] = ()) -> JsonValue:
    if value is None or isinstance(value, (int, float, bool)):
        return value
    if isinstance(value, str):
        return redact_text(value, sensitive_values=sensitive_values)
    if isinstance(value, Mapping):
        return {
            str(key): redact_structure(item, sensitive_values=sensitive_values)
            for key, item in value.items()
            if str(key).lower() not in {"secret", "token", "password", "credential"}
        }
    if isinstance(value, Sequence) and not isinstance(value, (bytes, bytearray)):
        return [redact_structure(item, sensitive_values=sensitive_values) for item in value]
    return redact_text(str(value), sensitive_values=sensitive_values)
