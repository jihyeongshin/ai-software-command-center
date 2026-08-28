from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path

from aiscc.contracts.security import ResourceDomain, SecurityActionClass
from aiscc.contracts.workflow import RuntimeMode


@dataclass(frozen=True, slots=True)
class PermissionProfile:
    mode: RuntimeMode
    version: str
    actions: frozenset[SecurityActionClass]
    resources: frozenset[ResourceDomain]
    fixed_scenarios: frozenset[str] = frozenset()


def load_profile_versions(config_path: Path) -> dict[str, str]:
    """Load only version metadata; executable policy remains typed source."""
    with config_path.open("rb") as stream:
        raw = tomllib.load(stream)
    profiles = raw.get("profiles")
    if not isinstance(profiles, dict):
        raise ValueError("profiles table is required")
    result: dict[str, str] = {}
    for key, value in profiles.items():
        if not isinstance(key, str) or not isinstance(value, dict):
            raise ValueError("invalid profile metadata")
        version = value.get("version")
        if not isinstance(version, str) or not version:
            raise ValueError("profile version is required")
        result[key] = version
    return result
