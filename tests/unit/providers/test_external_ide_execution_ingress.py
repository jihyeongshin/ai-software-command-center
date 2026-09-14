import subprocess
from dataclasses import FrozenInstanceError
from datetime import UTC, datetime, timedelta
from hashlib import sha256

import pytest

from aiscc.contracts.canonical_json import canonical_json_bytes
from aiscc.providers.external_ide import (
    ExternalIdeAuthorityError,
    ExternalIdeExecutionLeaseV1,
    ExternalIdeExecutionSubmissionV1,
    LocalGitObserver,
    VerifiedExternalIdeExecutionSubmissionV1,
)

GIT = r"C:\Program Files\Git\cmd\git.exe"
NOW = datetime(2026, 9, 14, 9, tzinfo=UTC)


def git(root, *args):
    return subprocess.check_output([GIT, "-C", str(root), *args]).decode().strip()


def git_fixture(root):
    root.mkdir(exist_ok=True)
    git(root, "init", "-q")
    git(root, "config", "user.email", "isolated@example.invalid")
    git(root, "config", "user.name", "Isolated Fixture")
    (root / "src").mkdir()
    (root / "src/file.txt").write_bytes(b"before\n")
    git(root, "add", "--", "src/file.txt")
    git(root, "commit", "-qm", "fixture base")
    return git(root, "rev-parse", "HEAD")


def sample(root, base="1" * 40):
    scope = dict(allowed_paths=["src/**"], forbidden_paths=["private/**"])
    return dict(
        schema="AISCC-EXTERNAL-IDE-LEASE-V1",
        producer="LOCAL_IDE_SELF_DOGFOOD_V1",
        project_id="project",
        lease_id="lease",
        work_run_id="run",
        state="RUNNING",
        state_version=2,
        task_id="task",
        contract_id="contract",
        contract_version=1,
        body_ref="task-contract-body:v1:sha256:" + "a" * 64,
        body_sha256="a" * 64,
        repository_id="repository",
        repository_root=str(root.resolve()),
        base_commit=base,
        inner_task_sha256="b" * 64,
        **scope,
        scope_fingerprint=sha256(canonical_json_bytes(scope)).hexdigest(),
        issued_at=NOW.isoformat(),
        expires_at=(NOW + timedelta(minutes=10)).isoformat(),
        capability_hash="c" * 64,
        start_transition_id="start",
        expected_hashes={},
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("producer", "GENERIC_EXTERNAL_EXECUTOR"),
        ("unexpected", "field"),
        ("state", "READY"),
        ("state_version", True),
        ("state_version", 2**54),
        ("body_sha256", "A" * 64),
        ("project_id", "e\u0301"),
        ("allowed_paths", ["../file"]),
        ("allowed_paths", ["/root"]),
        ("allowed_paths", ["src/**", "src/**"]),
        ("allowed_paths", ["**"]),
        ("forbidden_paths", ["src/file.txt"]),
        ("expires_at", NOW.isoformat()),
        ("expected_hashes", {"other/file": "d" * 64}),
    ],
)
def test_closed_immutable_lease_validation(tmp_path, field, value):
    with pytest.raises(ValueError):
        ExternalIdeExecutionLeaseV1(sample(tmp_path) | {field: value})


def test_immutable_models_and_caller_receipt_cannot_create_authority(tmp_path):
    base = git_fixture(tmp_path)
    lease = ExternalIdeExecutionLeaseV1(sample(tmp_path, base))
    with pytest.raises(TypeError):
        lease.value["project_id"] = "forged"
    with pytest.raises(FrozenInstanceError):
        lease.canonical_body = b"{}"
    (tmp_path / "src/file.txt").write_bytes(b"after\n")
    observation = LocalGitObserver(GIT, clock=lambda: NOW).observe(lease)
    submission = ExternalIdeExecutionSubmissionV1(
        lease, observation, "external-ide-submission:lease", NOW.isoformat()
    )
    with pytest.raises(ExternalIdeAuthorityError):
        _ = VerifiedExternalIdeExecutionSubmissionV1(submission, object()).common_ref
    with pytest.raises(FrozenInstanceError):
        submission.submission_id = "forged"


def test_real_git_observation_hash_scope_deletion_rename_and_no_index_write(tmp_path):
    base = git_fixture(tmp_path)
    lease = ExternalIdeExecutionLeaseV1(sample(tmp_path, base))
    observer = LocalGitObserver(GIT, clock=lambda: NOW)
    index = (tmp_path / ".git/index").read_bytes()
    (tmp_path / "src/file.txt").write_bytes(b"changed\n")
    (tmp_path / "src/new.txt").write_bytes(b"new\n")
    (tmp_path / "outside.txt").write_bytes(b"unauthorized\n")
    first = observer.observe(lease)
    assert first.root == observer.observe(lease).root
    assert first.value["files"]["src/new.txt"] == sha256(b"new\n").hexdigest()
    assert first.value["unauthorized"] == ("outside.txt",)
    assert (tmp_path / ".git/index").read_bytes() == index
    (tmp_path / "src/file.txt").unlink()
    assert observer.observe(lease).value["files"]["src/file.txt"] is None
    # Fixture mutation is outside the observer; staged rename must be observed and denied.
    git(tmp_path, "reset", "--hard", "HEAD")
    git(tmp_path, "mv", "src/file.txt", "src/renamed.txt")
    rename = observer.observe(lease)
    assert rename.value["index"]
    assert any(x["original"] == "src/file.txt" for x in rename.value["entries"])
    assert git(tmp_path, "rev-parse", "HEAD") == base


def test_no_arbitrary_command_or_producer_registration_api():
    from aiscc.providers.external_ide import ExternalIdeExecutionRepository

    assert not hasattr(LocalGitObserver, "run")
    assert not hasattr(ExternalIdeExecutionRepository, "register_submission")
    assert not hasattr(ExternalIdeExecutionRepository, "issue")


@pytest.mark.parametrize("key", ["filter.untrusted.clean", "include.path"])
def test_observer_denies_executable_or_indirect_local_git_configuration(tmp_path, key):
    base = git_fixture(tmp_path)
    lease = ExternalIdeExecutionLeaseV1(sample(tmp_path, base))
    git(tmp_path, "config", key, "untrusted-fixture-value")
    with pytest.raises(ExternalIdeAuthorityError, match="configuration denied"):
        LocalGitObserver(GIT).observe(lease)
