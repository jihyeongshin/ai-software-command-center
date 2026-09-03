from __future__ import annotations

from datetime import UTC, datetime
from typing import Final

PRIVATE_FIELD_NAMES: Final[frozenset[str]] = frozenset(
    {
        "authentication_session_id",
        "body",
        "canonical_body",
        "encrypted_body_ref",
        "environment",
        "human_action_authority_ref",
        "output",
        "parameters",
        "principal_authority_ref",
        "principal_id",
        "private_comment_hash",
        "private_comment_ref",
        "prompt",
        "provider_protocol",
        "rationale",
        "requester_identity",
        "secret",
        "storage_ref",
        "token",
    }
)

SAFE_COUNTER_KEYS: Final[tuple[str, ...]] = (
    "schema_version",
    "provider_calls",
    "agent_rounds",
    "tool_calls",
    "provider_retries",
    "output_bytes",
    "output_tokens",
    "budget_units",
    "started_at",
    "deadline_at",
)


def safe_string_list(value: object) -> tuple[str, ...]:
    if not isinstance(value, list):
        return ()
    return tuple(item for item in value if isinstance(item, str))


def safe_optional_string(value: object) -> str | None:
    return value if isinstance(value, str) else None


def safe_optional_int(value: object) -> int | None:
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def safe_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed.astimezone(UTC)


def safe_mapping(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        return {}
    return {str(key): item for key, item in value.items() if isinstance(key, str)}


def redacted_resource_identity(_: str) -> str:
    return "REDACTED_RESOURCE_IDENTITY"


def contains_private_field(value: object) -> bool:
    """Test/report helper for recursively detecting forbidden serialized keys."""
    if isinstance(value, dict):
        return any(
            str(key).lower() in PRIVATE_FIELD_NAMES or contains_private_field(item)
            for key, item in value.items()
        )
    if isinstance(value, (list, tuple)):
        return any(contains_private_field(item) for item in value)
    return False
