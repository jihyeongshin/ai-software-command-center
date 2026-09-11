"""Fixed Stockroom image authority; Cut A never issues production provenance."""

from __future__ import annotations

import hashlib
import json
import tomllib
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SCHEMA_ID = "AISCC-STOCKROOM-IMAGE-PROVENANCE-V1"
SCHEMA_VERSION = "1.0.0"
BUILD_CONTRACT = "AISCC-STOCKROOM-RUNTIME-BUILD-V1"
PROVENANCE_PATH = ".aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json"
BASE_REPODIGEST = (
    "python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579"
)
SOURCE_COMMIT = "05185c57a6265a4002050ce25cdfde3dc87e9779"
SOURCE_SUBROOT = "examples/synthetic-stockroom/"
SOURCE_SUBTREE = "f3d9203321ae3535abf8e92a7285da1067f6c55e"
SOURCE_AGGREGATE = "be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d"
RESOURCE_REF = "repository:synthetic-stockroom@" + SOURCE_AGGREGATE
BUILD_FILES = ("Dockerfile", ".dockerignore", "IMAGE_PROVENANCE.md")
_ROOT = Path(__file__).resolve().parents[3]
_ISSUER = object()


def canonical_fingerprint(value: object) -> str:
    return hashlib.sha256(json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False,
    ).encode("utf-8")).hexdigest()


class _Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


class Issuance(_Strict):
    accepted_cycle_ref: str = Field(
        pattern=r"^\.aiassistant/records/aiscc/cycles/[a-z0-9_-]+\.cycle\.md$"
    )
    accepted_judgment_ref: str = Field(pattern=r"^\.aiassistant/reports/aiscc/[a-z0-9_-]+\.md$")


class ImageIdentity(_Strict):
    identity_model: Literal["LOCAL_IMAGE_CONFIG_ID_SHA256"]
    image_id: str = Field(pattern=r"^sha256:[0-9a-f]{64}$")
    os: Literal["linux"]
    architecture: Literal["amd64"]
    discovery_tag: str | None = Field(
        default=None, pattern=r"^[a-z0-9][a-z0-9._/-]*:[a-zA-Z0-9_.-]+$"
    )

    @model_validator(mode="after")
    def no_pseudo_image(self) -> ImageIdentity:
        if self.image_id == "sha256:" + SOURCE_AGGREGATE:
            raise ValueError("SOURCE_AGGREGATE_NOT_IMAGE_ID")
        return self


class BaseImage(_Strict):
    pin_model: Literal["SOURCE_FIXED_VERIFIED_REPODIGEST"]
    repodigest: str

    @model_validator(mode="after")
    def fixed_pin(self) -> BaseImage:
        if self.repodigest != BASE_REPODIGEST:
            raise ValueError("BASE_REPODIGEST_MISMATCH")
        return self


class BuildIdentity(_Strict):
    contract_version: Literal["AISCC-STOCKROOM-RUNTIME-BUILD-V1"]
    context_model: Literal["TASK_SCOPED_GIT_OBJECT_ASSEMBLED_EXACT_CONTEXT"]
    dockerfile_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    dockerignore_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")


class SourceIdentity(_Strict):
    commit: str
    subroot: str
    git_subtree: str
    resource_ref: str
    aggregate_sha256: str
    file_count: Literal[14]

    @model_validator(mode="after")
    def fixed_source(self) -> SourceIdentity:
        if (self.commit, self.subroot, self.git_subtree, self.resource_ref,
                self.aggregate_sha256) != (
                SOURCE_COMMIT, SOURCE_SUBROOT, SOURCE_SUBTREE, RESOURCE_REF, SOURCE_AGGREGATE):
            raise ValueError("SOURCE_IDENTITY_MISMATCH")
        return self


class RuntimeIdentity(_Strict):
    python_version: Literal["3.12.14"]
    argv: tuple[
        Literal["python"], Literal["-B"], Literal["-m"], Literal["stockroom"], Literal["summary"]
    ]
    workdir: Literal["/workspace"]
    user: Literal["65532:65532"]
    network: Literal["none"]


def required_labels(dockerfile_sha256: str) -> dict[str, str]:
    values = {
        "build-contract": BUILD_CONTRACT,
        "source-commit": SOURCE_COMMIT,
        "source-subroot": SOURCE_SUBROOT,
        "git-subtree": SOURCE_SUBTREE,
        "resource-ref": RESOURCE_REF,
        "source-aggregate": SOURCE_AGGREGATE,
        "source-file-count": "14",
        "python-version": "3.12.14",
        "dockerfile-sha256": dockerfile_sha256,
        "base-repodigest": BASE_REPODIGEST,
    }
    return {"io.aiscc.stockroom." + key: value for key, value in values.items()}


class StockroomImageProvenance(_Strict):
    schema_id: Literal["AISCC-STOCKROOM-IMAGE-PROVENANCE-V1"]
    schema_version: Literal["1.0.0"]
    provenance_id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,127}$")
    provenance_version: str = Field(pattern=r"^[1-9][0-9]*$")
    issuance: Issuance
    image: ImageIdentity
    base_image: BaseImage
    build: BuildIdentity
    source: SourceIdentity
    runtime: RuntimeIdentity
    required_labels: tuple[tuple[str, str], ...]
    inspect_projection_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    issued_at: str

    @model_validator(mode="after")
    def verify_labels_and_date(self) -> StockroomImageProvenance:
        if self.required_labels != tuple(
            sorted(required_labels(self.build.dockerfile_sha256).items())
        ):
            raise ValueError("REQUIRED_IMAGE_LABELS_MISMATCH")
        if datetime.fromisoformat(self.issued_at).tzinfo is None:
            raise ValueError("ISSUED_AT_TIMEZONE_REQUIRED")
        return self


def parse_provenance(data: bytes) -> StockroomImageProvenance:
    """Parse the exact JSON schema without admitting the resulting object."""
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("DUPLICATE_PROVENANCE_KEY")
            result[key] = value
        return result

    raw = json.loads(data.decode("utf-8"), object_pairs_hook=unique)
    if type(raw) is not dict or type(raw.get("required_labels")) is not dict:
        raise ValueError("PROVENANCE_OBJECT_REQUIRED")
    labels = raw["required_labels"]
    if any(type(k) is not str or type(v) is not str for k, v in labels.items()):
        raise ValueError("LABEL_TYPE_DENIED")
    raw["required_labels"] = tuple(sorted(labels.items()))
    if type(raw.get("source")) is not dict or type(raw["source"].get("file_count")) is not int:
        raise ValueError("SOURCE_COUNT_TYPE_DENIED")
    if type(raw.get("runtime")) is not dict or type(raw["runtime"].get("argv")) is not list:
        raise ValueError("RUNTIME_ARGV_REQUIRED")
    raw["runtime"]["argv"] = tuple(raw["runtime"]["argv"])
    return StockroomImageProvenance.model_validate(raw)


def provenance_payload(value: StockroomImageProvenance) -> dict:
    raw = value.model_dump(mode="json")
    raw["required_labels"] = dict(value.required_labels)
    return raw


class StockroomImageProvenanceRef(_Strict):
    path: Literal[".aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json"]
    whole_file_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    canonical_fingerprint: str = Field(pattern=r"^[0-9a-f]{64}$")
    provenance_id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{0,127}$")
    provenance_version: str = Field(pattern=r"^[1-9][0-9]*$")
    issuance: Issuance


@dataclass(frozen=True, slots=True)
class AdmittedStockroomImage:
    provenance: StockroomImageProvenance
    ref: StockroomImageProvenanceRef
    _issuer: object = field(repr=False, compare=False)
    _bytes: bytes = field(repr=False, compare=False)


def image_policy() -> dict[str, str | bool]:
    return {
        "binding_model": "IMAGE_IDENTITY_POLICY_AND_PROVENANCE_REF",
        "runtime_identity_model": "LOCAL_IMAGE_CONFIG_ID_SHA256",
        "provenance_schema_id": SCHEMA_ID,
        "provenance_schema_version": SCHEMA_VERSION,
        "provenance_ref": PROVENANCE_PATH,
        "provenance_fingerprint_required": True,
        "base_image_pin_model": "SOURCE_FIXED_VERIFIED_REPODIGEST",
        "base_image_ref": BASE_REPODIGEST,
        "build_contract_version": BUILD_CONTRACT,
        "source_resource_ref": RESOURCE_REF,
    }


def require_image_policy(policy: object) -> None:
    expected = image_policy()
    if type(policy) is not dict or policy.keys() != expected.keys() or any(
        type(policy[key]) is not type(value) or policy[key] != value
        for key, value in expected.items()
    ):
        raise ValueError("STATIC_IMAGE_POLICY_DENIED")


def _read_canonical() -> bytes:
    path = _ROOT / PROVENANCE_PATH
    if path.is_symlink() or path.resolve(strict=True) != path.absolute():
        raise ValueError("PROVENANCE_PATH_DENIED")
    return path.read_bytes()


def _verify_build(value: StockroomImageProvenance) -> None:
    with (_ROOT / "config/providers/stockroom-tools.v2.toml").open("rb") as stream:
        static = tomllib.load(stream)
    if static.get("registry_version") != "2":
        raise ValueError("STATIC_POLICY_CURRENTNESS_DENIED")
    require_image_policy(static.get("tool", {}).get("image_binding_policy"))
    for name, expected in (
        ("Dockerfile", value.build.dockerfile_sha256),
        (".dockerignore", value.build.dockerignore_sha256),
    ):
        if hashlib.sha256((_ROOT / SOURCE_SUBROOT / name).read_bytes()).hexdigest() != expected:
            raise ValueError("BUILD_FILE_CURRENTNESS_DENIED")
    resource = json.loads((_ROOT / "config/scenarios/stockroom/v1/resource.json").read_bytes())
    if (resource["source_commit"], resource["subroot"], resource["git_subtree"],
        resource["resource_ref"], resource["aggregate_sha256"], resource["file_count"]) != (
        SOURCE_COMMIT, SOURCE_SUBROOT, SOURCE_SUBTREE, RESOURCE_REF, SOURCE_AGGREGATE, 14
    ):
        raise ValueError("RESOURCE_CURRENTNESS_DENIED")


def resolve_stockroom_image(
    ref: StockroomImageProvenanceRef, policy: object
) -> AdmittedStockroomImage:
    if type(ref) is not StockroomImageProvenanceRef:
        raise ValueError("TYPED_PROVENANCE_REF_REQUIRED")
    require_image_policy(policy)
    data = _read_canonical()
    value = parse_provenance(data)
    if (hashlib.sha256(data).hexdigest(), canonical_fingerprint(provenance_payload(value)),
        value.provenance_id, value.provenance_version, value.issuance) != (
        ref.whole_file_sha256, ref.canonical_fingerprint, ref.provenance_id,
        ref.provenance_version, ref.issuance
    ):
        raise ValueError("PROVENANCE_REF_BINDING_DENIED")
    _verify_build(value)
    return AdmittedStockroomImage(value, ref, _ISSUER, data)


def require_admitted_image(value: object) -> AdmittedStockroomImage:
    if type(value) is not AdmittedStockroomImage or value._issuer is not _ISSUER:
        raise ValueError("ADMITTED_IMAGE_REQUIRED")
    current = resolve_stockroom_image(value.ref, image_policy())
    if current._bytes != value._bytes or current.provenance != value.provenance:
        raise ValueError("PROVENANCE_CURRENTNESS_DENIED")
    return value


def inspect_projection(observation: object, value: StockroomImageProvenance) -> dict:
    if type(observation) is not dict or type(observation.get("Config")) is not dict:
        raise ValueError("IMAGE_INSPECT_DENIED")
    config = observation["Config"]
    labels = config.get("Labels")
    expected = dict(value.required_labels)
    if type(labels) is not dict or any(labels.get(k) != v for k, v in expected.items()):
        raise ValueError("IMAGE_LABEL_DRIFT")
    result = {
        "Id": observation.get("Id"), "Os": observation.get("Os"),
        "Architecture": observation.get("Architecture"),
        "Config": {"User": config.get("User"), "WorkingDir": config.get("WorkingDir"),
                   "Labels": {k: labels[k] for k in expected}},
    }
    if (result["Id"], result["Os"], result["Architecture"], config.get("User"),
        config.get("WorkingDir")) != (value.image.image_id, "linux", "amd64", "65532:65532",
                                     "/workspace"):
        raise ValueError("IMAGE_INSPECT_IDENTITY_DRIFT")
    return result


def verify_image_inspect(observation: object, admitted: AdmittedStockroomImage) -> None:
    value = require_admitted_image(admitted).provenance
    if (
        canonical_fingerprint(inspect_projection(observation, value))
        != value.inspect_projection_sha256
    ):
        raise ValueError("IMAGE_INSPECT_PROJECTION_DRIFT")
