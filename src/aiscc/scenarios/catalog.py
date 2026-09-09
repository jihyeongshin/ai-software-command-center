"""Explicit local-file loading only; no registration, execution or remote schema resolution."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError as SchemaValidationError
from pydantic import BaseModel, ValidationError

from aiscc.scenarios.models import (
    CatalogDocument,
    HumanOwnedClaimFixture,
    MissingEvidenceFixture,
    PolicyConflictFixture,
    PublicSelection,
    Resource,
    Scenario,
    relative_posix_path,
)

Fixture = MissingEvidenceFixture | PolicyConflictFixture | HumanOwnedClaimFixture
MAX_CONFIG_BYTES = 131072


class ContractError(ValueError):
    """Malformed, inconsistent or unavailable static configuration."""


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError("duplicate JSON field")
        result[key] = value
    return result


def _invalid_constant(value: str) -> None:
    raise ContractError("non-finite JSON number")


def _read[T: BaseModel](path: Path, model: type[T]) -> T:
    try:
        with path.open("rb") as stream:
            raw = stream.read(MAX_CONFIG_BYTES + 1)
        if len(raw) > MAX_CONFIG_BYTES:
            raise ContractError("configuration size limit exceeded")
        text = raw.decode("utf-8", errors="strict")
        value = json.loads(text, object_pairs_hook=_unique_object, parse_constant=_invalid_constant)
        # Generated local schemas contain only local $defs references; no resolver/network.
        Draft202012Validator(model.model_json_schema()).validate(value)
        return model.model_validate_json(text)
    except (OSError, ValueError, RecursionError, SchemaValidationError):
        # Never echo untrusted payloads, host paths, or Pydantic input values.
        raise ContractError("missing, malformed or inconsistent static contract") from None


def _contained_file(root: Path, relative: str) -> Path:
    try:
        relative_posix_path(relative)
        path = (root / relative).resolve(strict=True)
        if not path.is_relative_to(root) or not path.is_file():
            raise ContractError("configured file escaped its root or is not a file")
        return path
    except (OSError, ValueError, RuntimeError):
        raise ContractError("invalid or missing configured relative file") from None


@dataclass(frozen=True, slots=True)
class ScenarioCatalog:
    document: CatalogDocument
    resource: Resource
    scenarios: tuple[Scenario, ...]
    fixtures: tuple[Fixture, ...]

    def select(self, payload: object) -> Scenario:
        try:
            selection = PublicSelection.model_validate(payload)
        except ValidationError:
            raise ContractError("selection requires one allowlisted scenario_id only") from None
        for scenario in self.scenarios:
            if scenario.scenario_id == selection.scenario_id:
                return scenario
        raise ContractError("selected scenario is not configured")


def load_catalog(catalog_path: Path) -> ScenarioCatalog:
    """Load the exact configured catalog and its bounded relative references.

    The caller owns catalog_path; it is never derived from public selection input.
    Resource verification hashes manifest rows only, never source files or Git.
    """
    try:
        configured = catalog_path.resolve(strict=True)
    except (OSError, RuntimeError):
        raise ContractError("configured catalog is unavailable") from None
    root = configured.parent
    document = _read(configured, CatalogDocument)
    resource = _read(_contained_file(root, document.resource_path), Resource)
    if document.resource_ref != resource.resource_ref:
        raise ContractError("unknown catalog resource_ref")
    scenarios: list[Scenario] = []
    fixtures: list[Fixture] = []
    fixture_models: dict[str, type[Fixture]] = {
        "stockroom-s2-missing-evidence": MissingEvidenceFixture,
        "stockroom-s3-policy-conflict": PolicyConflictFixture,
        "stockroom-s4-human-owned-claim": HumanOwnedClaimFixture,
    }
    for entry in sorted(document.scenarios, key=lambda item: item.scenario_id):
        scenario = _read(_contained_file(root, entry.path), Scenario)
        if (scenario.scenario_id, scenario.scenario_version) != (
            entry.scenario_id,
            entry.scenario_version,
        ) or scenario.resource_ref != resource.resource_ref:
            raise ContractError("scenario ID/version/resource binding mismatch")
        for ref in scenario.fixture_refs:
            fixtures.append(_read(_contained_file(root, ref), fixture_models[scenario.scenario_id]))
        scenarios.append(scenario)
    return ScenarioCatalog(document, resource, tuple(scenarios), tuple(fixtures))
