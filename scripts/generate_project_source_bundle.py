"""Generate a validated AISCC Project Source mirror from an exact Git commit.

Markdown fence validation uses this deterministic rule: an opening fence is a
line indented by at most three spaces and beginning with at least three equal
backticks or tildes; it is closed only by the same character repeated at least
as many times, followed solely by spaces or tabs.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any


EXPECTED_TARGET_PROJECT = "AI Software Command Center"
EXPECTED_PROJECT_SCOPE = "AISCC Browser Command Center canonical read-only mirror"
MANIFEST_DIRECTORY = PurePosixPath(".aiassistant/project-sources/manifests")
BUNDLE_PARENT = PurePosixPath(".aiassistant/project-sources/bundles/aiscc")
ROOT_KEYS = [
    "bundle_id",
    "target_gpt_project",
    "project_scope",
    "canonical_commit",
    "generated_by_task",
    "generated_at",
    "expected_active_count",
    "source_mirror_sync_status",
    "optional_mapping",
    "mapping",
]
MAPPING_KEYS = [
    "project_source_filename",
    "canonical_path",
    "group",
    "role",
    "canonical_sha256",
    "upload_status",
]
ALLOWED_CANONICAL_PREFIXES = (
    ".aiassistant/rules/",
    ".aiassistant/records/",
    ".aiassistant/reports/aiscc/",
)
DENIED_PATH_MARKERS = {
    "credential",
    "credentials",
    "key",
    "keys",
    "private",
    "secret",
    "secrets",
    "token",
    "tokens",
}
SECRET_PATTERNS = (
    re.compile(rb"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"),
    re.compile(rb"AKIA[0-9A-Z]{16}"),
    re.compile(rb"AIza[0-9A-Za-z_-]{35}"),
    re.compile(rb"(?:gh[pousr]|github_pat)_[0-9A-Za-z_]{20,}"),
    re.compile(rb"sk-[0-9A-Za-z]{20,}"),
)
FILENAME_PATTERN = re.compile(
    r"^[0-9]{2}_[A-Z0-9][A-Z0-9_-]*__[A-Z0-9][A-Z0-9_-]*\.md$"
)
SHA_PATTERN = re.compile(r"^[0-9a-f]{64}$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
BUNDLE_PATTERN = re.compile(r"^AISCC-PROJECT-SOURCE-MIRROR-V[1-9][0-9]*$")
TASK_PATTERN = re.compile(r"^[0-9]{8}_[0-9]{4}_[a-z0-9][a-z0-9-]*$")
TIMESTAMP_PATTERN = re.compile(
    r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}[+-][0-9]{2}:[0-9]{2}$"
)


class GenerationError(RuntimeError):
    """A fail-closed validation or generation error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise GenerationError(message)


def run_git(repository_root: Path, arguments: list[str], context: str) -> bytes:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=repository_root,
        check=False,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise GenerationError(f"Git validation failed: {context}")
    return completed.stdout


def require_exact_keys(value: dict[str, Any], expected: list[str], context: str) -> None:
    require(list(value.keys()) == expected, f"{context} keys or key order mismatch")


def require_string(value: Any, context: str) -> str:
    require(type(value) is str and bool(value), f"{context} must be a non-empty string")
    return value


def validate_timestamp(value: str) -> None:
    require(bool(TIMESTAMP_PATTERN.fullmatch(value)), "generated_at format is invalid")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise GenerationError("generated_at is not a valid timestamp") from exc
    require(parsed.utcoffset() is not None, "generated_at must include an offset")


def validate_fences(text: str, context: str) -> None:
    open_character: str | None = None
    open_length = 0
    for line_number, line in enumerate(text.splitlines(), start=1):
        if open_character is None:
            opener = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if opener is not None:
                delimiter = opener.group(1)
                open_character = delimiter[0]
                open_length = len(delimiter)
            continue
        closing = re.match(
            rf"^ {{0,3}}{re.escape(open_character)}{{{open_length},}}[ \t]*$",
            line,
        )
        if closing is not None:
            open_character = None
            open_length = 0
    require(open_character is None, f"unbalanced Markdown fence in {context}")


def validate_text_bytes(content: bytes, context: str) -> str:
    require(not content.startswith(b"\xef\xbb\xbf"), f"UTF-8 BOM rejected in {context}")
    require(b"\x00" not in content, f"NUL rejected in {context}")
    require(
        not any(byte < 0x20 and byte not in (0x09, 0x0A, 0x0D) for byte in content),
        f"prohibited C0 control byte in {context}",
    )
    try:
        text = content.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise GenerationError(f"strict UTF-8 decode failed in {context}") from exc
    require(
        re.search(r"[ \t]+(?:\r?\n|\Z)", text, flags=re.MULTILINE) is None,
        f"trailing space or tab in {context}",
    )
    validate_fences(text, context)
    return text


def validate_safe_canonical_path(value: str) -> str:
    require("\\" not in value, "canonical path contains a backslash")
    require(not value.startswith("/"), "canonical path must be repository-relative")
    raw_parts = value.split("/")
    require(all(part not in ("", ".", "..") for part in raw_parts), "canonical path is not normalized")
    normalized = PurePosixPath(value)
    require(normalized.as_posix() == value, "canonical path is not normalized")
    require(value.endswith(".md"), "canonical path must name a Markdown file")
    require(
        any(value.startswith(prefix) for prefix in ALLOWED_CANONICAL_PREFIXES),
        "canonical path is outside the allowed source roots",
    )
    marker_tokens: set[str] = set()
    for component in raw_parts:
        marker_tokens.update(token for token in re.split(r"[^a-z0-9]+", component.lower()) if token)
    require(
        marker_tokens.isdisjoint(DENIED_PATH_MARKERS),
        "canonical path contains a denied secret/private marker",
    )
    return value


def reject_secret_content(content: bytes, context: str) -> None:
    require(
        not any(pattern.search(content) for pattern in SECRET_PATTERNS),
        f"high-confidence secret pattern detected in {context}",
    )


def load_manifest(repository_root: Path, manifest_path: Path) -> dict[str, Any]:
    manifest_directory = (repository_root / Path(MANIFEST_DIRECTORY.as_posix())).resolve(strict=True)
    resolved_manifest = manifest_path.resolve(strict=True)
    require(
        resolved_manifest.parent == manifest_directory,
        "manifest must be directly under the allowed manifest directory",
    )
    content = resolved_manifest.read_bytes()
    text = validate_text_bytes(content, "manifest")
    try:
        manifest = json.loads(text)
    except json.JSONDecodeError as exc:
        raise GenerationError("manifest JSON is invalid") from exc
    require(type(manifest) is dict, "manifest root must be an object")
    require_exact_keys(manifest, ROOT_KEYS, "manifest root")
    return manifest


def validate_manifest(manifest: dict[str, Any]) -> list[dict[str, str]]:
    bundle_id = require_string(manifest["bundle_id"], "bundle_id")
    require(bool(BUNDLE_PATTERN.fullmatch(bundle_id)), "bundle_id format is invalid")
    require(
        manifest["target_gpt_project"] == EXPECTED_TARGET_PROJECT,
        "target_gpt_project mismatch",
    )
    require(manifest["project_scope"] == EXPECTED_PROJECT_SCOPE, "project_scope mismatch")

    canonical_commit = require_string(manifest["canonical_commit"], "canonical_commit")
    require(bool(COMMIT_PATTERN.fullmatch(canonical_commit)), "canonical_commit format is invalid")
    generated_by_task = require_string(manifest["generated_by_task"], "generated_by_task")
    require(bool(TASK_PATTERN.fullmatch(generated_by_task)), "generated_by_task format is invalid")
    generated_at = require_string(manifest["generated_at"], "generated_at")
    validate_timestamp(generated_at)
    require(
        type(manifest["expected_active_count"]) is int
        and manifest["expected_active_count"] > 0,
        "expected_active_count must be a positive integer",
    )
    require_string(manifest["source_mirror_sync_status"], "source_mirror_sync_status")
    require(
        type(manifest["optional_mapping"]) is list and not manifest["optional_mapping"],
        "optional_mapping must be an empty array",
    )
    require(type(manifest["mapping"]) is list, "mapping must be an array")
    require(
        len(manifest["mapping"]) == manifest["expected_active_count"],
        "mapping count does not equal expected_active_count",
    )

    validated: list[dict[str, str]] = []
    filenames: set[str] = set()
    canonical_paths: set[str] = set()
    for index, raw_mapping in enumerate(manifest["mapping"]):
        require(type(raw_mapping) is dict, f"mapping[{index}] must be an object")
        require_exact_keys(raw_mapping, MAPPING_KEYS, f"mapping[{index}]")
        mapping = {key: require_string(raw_mapping[key], f"mapping[{index}].{key}") for key in MAPPING_KEYS}
        filename = mapping["project_source_filename"]
        require(bool(FILENAME_PATTERN.fullmatch(filename)), f"invalid output filename at mapping[{index}]")
        require(filename == Path(filename).name, f"unsafe output filename at mapping[{index}]")
        filename_key = filename.casefold()
        require(filename_key not in filenames, "duplicate output filename")
        filenames.add(filename_key)

        canonical_path = validate_safe_canonical_path(mapping["canonical_path"])
        canonical_key = canonical_path.casefold()
        require(canonical_key not in canonical_paths, "duplicate canonical path")
        canonical_paths.add(canonical_key)

        require(bool(re.fullmatch(r"[A-Z][A-Z0-9_]*", mapping["group"])), f"invalid group at mapping[{index}]")
        require(bool(SHA_PATTERN.fullmatch(mapping["canonical_sha256"])), f"invalid SHA-256 at mapping[{index}]")
        require(
            mapping["upload_status"] == "REGENERATED_CANDIDATE",
            f"invalid upload_status at mapping[{index}]",
        )
        validated.append(mapping)
    return validated


def canonical_blob(
    repository_root: Path,
    canonical_commit: str,
    canonical_path: str,
) -> tuple[str, bytes]:
    object_spec = f"{canonical_commit}:{canonical_path}"
    blob_id = run_git(
        repository_root,
        ["rev-parse", "--verify", object_spec],
        f"resolve canonical blob for {canonical_path}",
    ).decode("ascii", errors="strict").strip()
    require(bool(COMMIT_PATTERN.fullmatch(blob_id)), f"invalid Git blob id for {canonical_path}")
    object_type = run_git(
        repository_root,
        ["cat-file", "-t", blob_id],
        f"read canonical object type for {canonical_path}",
    ).decode("ascii", errors="strict").strip()
    require(object_type == "blob", f"canonical object is not a blob for {canonical_path}")
    content = run_git(
        repository_root,
        ["cat-file", "blob", blob_id],
        f"read canonical blob for {canonical_path}",
    )
    return blob_id, content


def metadata_header(manifest: dict[str, Any], mapping: dict[str, str]) -> bytes:
    lines = [
        "# AISCC Project Source Mirror Metadata",
        "",
        "- mirror_type: `GPT_PROJECT_SOURCE_READ_ONLY_MIRROR`",
        f"- canonical_path: `{mapping['canonical_path']}`",
        f"- project_source_filename: `{mapping['project_source_filename']}`",
        "- canonical_owner: `AISCC repository`",
        "- mirror_owner: `AI Software Command Center Browser Project`",
        f"- mirror_generated_by_task: `{manifest['generated_by_task']}`",
        f"- mirrored_at: `{manifest['generated_at']}`",
        f"- canonical_commit: `{manifest['canonical_commit']}`",
        f"- canonical_sha256: `{mapping['canonical_sha256']}`",
        "- authority: `READ_ONLY_MIRROR`",
        "- do_not_edit_in_project_source: `true`",
        "",
        "<!-- AISCC_CANONICAL_BODY_START -->",
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")


def relative_to_repository(repository_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repository_root).as_posix()
    except ValueError as exc:
        raise GenerationError("path resolved outside repository") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", required=True)
    parser.add_argument("--manifest", required=True)
    arguments = parser.parse_args()

    repository_root = Path(arguments.repository_root).resolve(strict=True)
    require((repository_root / ".git").is_dir(), "repository root does not contain .git")
    detected_root = Path(
        run_git(repository_root, ["rev-parse", "--show-toplevel"], "resolve repository root")
        .decode("utf-8", errors="strict")
        .strip()
    ).resolve(strict=True)
    require(detected_root == repository_root, "repository-root is not the exact Git top level")

    manifest_argument = Path(arguments.manifest)
    manifest_path = (
        manifest_argument.resolve(strict=True)
        if manifest_argument.is_absolute()
        else (repository_root / manifest_argument).resolve(strict=True)
    )
    manifest = load_manifest(repository_root, manifest_path)
    mappings = validate_manifest(manifest)

    canonical_commit = manifest["canonical_commit"]
    resolved_commit = run_git(
        repository_root,
        ["rev-parse", "--verify", f"{canonical_commit}^{{commit}}"],
        "resolve canonical commit",
    ).decode("ascii", errors="strict").strip()
    require(resolved_commit == canonical_commit, "canonical_commit did not resolve exactly")

    bundle_parent = (repository_root / Path(BUNDLE_PARENT.as_posix())).resolve(strict=True)
    output_root = (bundle_parent / manifest["bundle_id"]).resolve()
    require(output_root.parent == bundle_parent, "output root escaped the bundle parent")
    require(not output_root.exists(), "output directory already exists; refusing overwrite")

    generated_content: dict[str, bytes] = {}
    canonical_content: dict[str, bytes] = {}
    for mapping in mappings:
        canonical_path = mapping["canonical_path"]
        _, body = canonical_blob(repository_root, canonical_commit, canonical_path)
        validate_text_bytes(body, f"canonical blob {canonical_path}")
        reject_secret_content(body, f"canonical blob {canonical_path}")
        body_sha256 = hashlib.sha256(body).hexdigest()
        require(
            body_sha256 == mapping["canonical_sha256"],
            f"canonical SHA-256 mismatch for {canonical_path}",
        )
        filename = mapping["project_source_filename"]
        header = metadata_header(manifest, mapping)
        generated = header + body
        validate_text_bytes(generated, f"generated candidate {filename}")
        generated_content[filename] = generated
        canonical_content[filename] = body

    output_root.mkdir()
    for filename, content in generated_content.items():
        output_path = output_root / filename
        with output_path.open("xb") as stream:
            stream.write(content)

    actual_entries = list(output_root.iterdir())
    require(all(entry.is_file() for entry in actual_entries), "output root contains a non-file entry")
    actual_filenames = {entry.name for entry in actual_entries}
    expected_filenames = set(generated_content)
    require(len(actual_entries) == manifest["expected_active_count"], "generated file count mismatch")
    require(actual_filenames == expected_filenames, "generated filename set mismatch")

    for mapping in mappings:
        filename = mapping["project_source_filename"]
        output_path = output_root / filename
        actual = output_path.read_bytes()
        expected_header = metadata_header(manifest, mapping)
        expected_body = canonical_content[filename]
        require(actual == expected_header + expected_body, f"generated bytes mismatch for {filename}")
        require(actual.startswith(expected_header), f"metadata mismatch for {filename}")
        extracted_body = actual[len(expected_header) :]
        require(extracted_body == expected_body, f"body identity mismatch for {filename}")
        require(
            hashlib.sha256(extracted_body).hexdigest() == mapping["canonical_sha256"],
            f"body SHA-256 mismatch for {filename}",
        )
        validate_text_bytes(actual, f"generated output {filename}")
        repository_relative = relative_to_repository(repository_root, output_path)
        ignored = subprocess.run(
            ["git", "check-ignore", "--quiet", "--", repository_relative],
            cwd=repository_root,
            check=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        require(ignored.returncode == 0, f"generated path is not Git-ignored: {filename}")

    output_relative = relative_to_repository(repository_root, output_root)
    generated_status = run_git(
        repository_root,
        ["status", "--porcelain=v1", "--untracked-files=all", "--", output_relative],
        "verify generated output Git visibility",
    )
    require(not generated_status, "generated output is Git-visible")

    print("GENERATED_PASS")
    print(f"bundle={manifest['bundle_id']}")
    print(f"files={len(actual_entries)}")
    print(f"canonical_commit={canonical_commit}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (GenerationError, OSError, ValueError) as error:
        print(f"GENERATION_FAILED: {error}", file=sys.stderr)
        raise SystemExit(1) from None
