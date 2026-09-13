# 작업지시서: P2-3 private S1 invalid-history disposition dedicated-builder execution retry

## meta

- task_id: `20260913_1707_aiscc-p2-3-private-s1-invalid-history-disposition-dedicated-builder-execution-retry-1`
- created_at: `2026-09-13T17:07:32+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PRIVATE_S1_INVALID_HISTORY_DISPOSITION_EXECUTION_RETRY`
- evidence_profile: `PRIVATE_RUNTIME_MUTATION_HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `d04f6a322f3a3ea49778314e4005b5878b20f121`
- required_parent: `7e2ea251f88ca07c6fd1bde38f73956f8885adbe`
- required_grandparent: `86288febf1cbd94bbb0235cfc680bf6c6c8f7772`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- docker_executable: `C:\Program Files\Docker\Docker\resources\bin\docker.exe`
- accepted_persistence_result_zip_sha256: `0db3994c4053f2def2dbe755315d7a7630a317b2091a13e96485a27635f6d6e1`
- accepted_candidate_result_zip_sha256: `620ffa448306c0f6486658cb8807e1887206311c2198be7d100c9f30f59ce4d1`
- private_runtime_read_authorized: `Yes / exact retained resources`
- private_runtime_mutation_authorized: `Conditional / one dedicated source-owned disposition`
- source_test_state_write_authorized: `No`
- new_execution_authorized: `No`
- new_run_attempt_authorized: `No`
- success_ceiling: `PRIVATE_S1_INVALID_HISTORY_DISPOSED / BROWSER_REVIEW_PENDING`

# 0. purpose

Execute the already persisted disposition against the exact retained 0036 S1 using only the dedicated disposition builder.

Never call the full production builder.

Exact subject:

```text
run_id:
aiscc-p2-3-private-s1-normal-v1-run

attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1

requester_identity:
aiscc-owner-operator
```

Expected initial durable state:

```text
WorkRun RUNNING/v2
ExecutionAttempt NOT_STARTED/v1
attempt causal READY/v1
execution operations 0
execution outputs/submission 0
runtime evidence 0
Judgment 0
```

No mutation before every preflight predicate passes.

# 1. transport / executables

Use only:

```text
Python:
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe

Docker:
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

Do not discover alternate Python/Docker through PATH.

Verify inbound ZIP/hash and exactly three flat safe members.

Place current Task first in canonical active, then exact Cycle/Judgment.

Bootstrap mismatch:

```text
STOP
no private runtime access
no report/export
```

# 2. repository baseline

Require:

```text
branch main
HEAD d04f6a322f3a3ea49778314e4005b5878b20f121
HEAD^ 7e2ea251f88ca07c6fd1bde38f73956f8885adbe
HEAD^^ 86288febf1cbd94bbb0235cfc680bf6c6c8f7772
index empty
tracked clean
Git-visible untracked before delivery none
```

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `05029cccdc9d20efd351fb603c681d30d5aa2b7f8a13617499f76318553ec337`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `8e5a89f622ede3d9ed16eaaa77ab8699ff9f0103c50b1a92fc528d4afb0d657c`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `6f86e6509a194e92235e14db7bdee70bae3f73c8312f868771fbf76c51f7c412`

Persisted source/rule hashes:

- `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`  `382433d24959827fc606592e7beb78f34934209fa2f9c34aabdeda1c6e322784`
- `src/aiscc/providers/events.py`  `69b0339a12630eb552ef479a819c78596a2c0094437b4458a30eebb730c18a98`
- `src/aiscc/persistence/repository.py`  `57dac018f6505468d62588761825025776d07384947424dad37b63f9f35e5e54`
- `src/aiscc/scenarios/stockroom_production.py`  `c41baca3f7cbeaaa18511dd6e94dd5dd5e65d2b282968703f2a4854d86e1b2f4`
- `src/aiscc/runtime/stockroom_workspace.py`  `1b8366b5c5a6e9054dbd65ef36cd09808074c88ccf6c7ad060a9a76a488efaab`
- `src/aiscc/bootstrap.py`  `745b58da26ec300286ed69d1a7477b21afeb7625ec43e7f422560a657bc1c115`

Require non-owned legacy active Task exact:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Preserve it untouched.

After current Cycle/Judgment placement while current Task is active/ignored:

```text
Git-visible untracked:
2 exact
```

Do not assert active-directory exclusivity.

Unexpected tracked/state/hash mismatch:

```text
STOP before private runtime access
```

# 3. exact retained PostgreSQL identity

Inspect only:

```text
container:
aiscc-p2-3-private-postgres-v1

container ID:
0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c

image ID:
sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94

volume:
aiscc-p2-3-private-postgres-data-v1

host endpoint:
127.0.0.1:55432

database:
aiscc_private_capture

role:
aiscc_private_capture
```

Require container running. Never start/recreate/repair on mismatch.

# 4. reconstruct exact private runtime root

From the exact retained PostgreSQL container inspect:

1. Find exactly one mount:
```text
Destination = /run/secrets/postgres_password
Type = bind
RW = false
```

2. Keep raw Source private.

3. Require Docker Desktop representation:
```text
/run/desktop/mnt/host/<single drive letter>/<safe non-empty suffix>
```

4. Normalize deterministically to native secret path.

5. Reject suffix segment if empty, `.`, `..`, contains `:` or backslash.

6. Reverse-map native path and require byte-for-byte equality to observed Docker Source.

7. Derive exactly:
```text
private_runtime_root = native_secret_path.parent / "aiscc-p2-3-private-runtime-v1"
```

No filesystem search or alternate root.

# 5. private boundary / ACL

For secret path, secret parent, derived runtime root require:

```text
absolute
exists
strict resolve exact
no symlink/reparse point on object/ancestors
secret regular file
runtime root directory
```

Require root leaf exactly `aiscc-p2-3-private-runtime-v1`.

Require no overlap with repository, Downloads, or `.aiassistant/reports/target`.

ACL read-only verification:

```text
secret parent inheritance protected

allowed Allow principals only:
current user SID
SYSTEM
Administrators

child/runtime rights:
no broader than parent principal rights
```

No ACL mutation.

# 6. export denylist and DB connection

Before reading password, add to in-memory export denylist:

```text
raw Docker bind Source
native secret absolute path
derived runtime-root absolute path
JSON-escaped forms
```

Then read exact secret file, add password/credential URL to denylist, and connect only:

```text
127.0.0.1:55432
aiscc_private_capture
aiscc_private_capture
```

Require DB identity exact and Alembic head:

```text
20260901_0008
```

Never print/export credential/path values.

# 7. Stockroom image / transient check

Read-only inspect exact image:

```text
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e

tag:
aiscc-stockroom-runtime:p2-3-private-v1
```

Require no running container using the exact Stockroom image.

Do not stop/remove anything on mismatch.

# 8. Phase A DB preflight

Read-only query exact subject.

Require:

## WorkRun
```text
id aiscc-p2-3-private-s1-normal-v1-run
state RUNNING
state_version 2
```

## attempt
```text
id aiscc-p2-3-private-s1-normal-v1-attempt-1
run aiscc-p2-3-private-s1-normal-v1-run
status NOT_STARTED
execution_version 1
creation READY/v1
causal READY/v1
task_contract identity/version == WorkRun
runtime_mode == WorkRun
```

Require counts:

```text
execution operations 0
execution outputs/submission 0
EXECUTION_STARTED events 0
EXECUTION_ABORTED_INVALID_HISTORY events 0
admitted SYSTEM_RUNTIME_OBSERVATION evidence 0
Judgment rows 0
later/competing attempt none
```

Mismatch → STOP_PRESERVE.

# 9. Phase A workspace preflight

Using the persisted restart-safety settlement semantics for exact run/attempt, inspect the derived root.

Require current observation:

```text
exists True
objects 20
files 14
bounded bytes 2320
inventory fingerprint 18433a8d92affe915d01e3bb1265b387a07dc6478e09c92306854908ab396068
safe regular-directory identity
no symlink/reparse/hardlink/special-object violation
no quarantine ambiguity
```

These values must be re-observed now; do not simply reuse 1435 report values.

Mismatch → STOP_PRESERVE.

# 10. Phase A stability re-read

Repeat DB authority/counts after workspace/image observations.

Require exact equality with section 8.

Any change → STOP_PRESERVE.

# 11. dedicated builder only

Import and call exactly:

```text
build_stockroom_invalid_history_disposition
```

from persisted current source.

Call exactly once:

```text
service = await build_stockroom_invalid_history_disposition(
    session_factory=factory,
    repository_root=Path(r"C:\Users\oracl\IdeaProjects\ai-software-command-center"),
    private_runtime_root=private_runtime_root,
    downloads_root=Path(r"C:\Users\oracl\Downloads"),
    requester_identity="aiscc-owner-operator",
)
```

Do not call full production builders.

Builder construction must:

```text
succeed on the nonempty retained root
perform no filesystem mutation
perform no authority enrollment/registration DB mutation
construct no Docker/provider/tool/evidence/human/Judgment stack
```

Compare DB authority-enrollment counts before/after builder and require zero delta.

# 12. source-owned provenance

Supply exactly ordered tuple:

```text
aiscc-accepted-runtime-evidence:v1:0036:sha256:041285052e8fad97636231be69775e0dd7003b3d1b1683b64200cdc931eb0ac5
aiscc-accepted-disposition-contract:v1:1242:sha256:b1dc8f91d1ba01c0198953fad70ace3d3c45276fe279d35c50521f2ad02b1381
```

The service itself must append the exact workspace-fingerprint provenance ref.

# 13. authorize

Call exactly once:

```text
request = await service.authorize(
    work_run_id="aiscc-p2-3-private-s1-normal-v1-run",
    execution_attempt_id="aiscc-p2-3-private-s1-normal-v1-attempt-1",
    expected_running_state_version=2,
    expected_execution_version=1,
    source_provenance_refs=(
        "aiscc-accepted-runtime-evidence:v1:0036:sha256:041285052e8fad97636231be69775e0dd7003b3d1b1683b64200cdc931eb0ac5",
        "aiscc-accepted-disposition-contract:v1:1242:sha256:b1dc8f91d1ba01c0198953fad70ace3d3c45276fe279d35c50521f2ad02b1381",
    ),
)
```

Require request:

```text
run/attempt exact
state version 2
execution version 1
reason INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START
workspace fingerprint 18433a8d92affe915d01e3bb1265b387a07dc6478e09c92306854908ab396068
workspace identity == current preflight
provenance == supplied two + exact source-owned workspace ref
```

Failure → STOP_PRESERVE, dispose 0.

# 14. final pre-mutation recheck

Immediately before dispose, repeat read-only:

```text
DB WorkRun/attempt/counts
workspace identity/fingerprint/counts
Stockroom running-transient check
```

Require exact equality with Phase A and sealed request.

Any mismatch → STOP_PRESERVE, dispose 0.

# 15. single disposition invocation

Only now call:

```text
result = await service.dispose(request)
```

Maximum:

```text
1 call
```

Never automatically retry after exception.

Never directly call repository abort or manual WorkRun transition.

# 16. expected success

Require:

## attempt
```text
status EXECUTION_FAILED
execution_version 2
causal RUNNING/v2
EXECUTION_ABORTED_INVALID_HISTORY count 1
reason INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START
```

## WorkRun
```text
FAILED/v3
RUNNING/v2 → FAILED/v3 admitted exactly once
authentic G_FAILURE_TERMINAL
exact invalid-history reason
```

## workspace
```text
QUARANTINED
original active target absent
one exact quarantine target
fingerprint 18433a8d92affe915d01e3bb1265b387a07dc6478e09c92306854908ab396068
bytes preserved
not reusable as active workspace
```

Do not delete quarantine.

# 17. post-success verification

Read-only verify:

```text
WorkRun FAILED/v3
attempt EXECUTION_FAILED/v2 causal RUNNING/v2
abort event 1
EXECUTION_STARTED 0
execution operations 0
execution outputs/submission 0
runtime evidence 0
Judgment 0
new WorkRuns 0
new attempts 0
authority enrollment rows unchanged from pre-builder baseline
no Stockroom container launched
```

Retain private PostgreSQL container/volume.

# 18. exception / partial state

If dispose raises, do not retry.

Read-only classify:

```text
P0:
NOT_STARTED/v1 + RUNNING/v2 + active workspace

P1:
EXECUTION_FAILED/v2 + RUNNING/v2 + active workspace

P2:
EXECUTION_FAILED/v2 + FAILED/v3 + active workspace

P3:
EXECUTION_FAILED/v2 + FAILED/v3 + active absent + one exact quarantine
```

Anything else:
```text
PARTIAL_DISPOSITION_STATE_UNEXPECTED
```

Every exception outcome:
```text
STOP_PRESERVE
no second dispose
no cleanup
no retry
no new run/attempt
```

# 19. no semantic evidence/retry

Do not create:

```text
ExecutionSubmissionRef
EvidenceCandidate
evidence satisfaction
System Judgment
HumanResult
new WorkRun
new ExecutionAttempt
```

# 20. export privacy

Scan every generated export member for:

```text
raw Docker secret bind Source
native secret absolute path
absolute runtime-root path
password
credential URL
absolute secret-source path
```

Required matches 0.

Use sanitized placeholders/root-relative identity only.

# 21. Git boundary

No tracked repository mutation.

Before Task move require:

```text
HEAD d04f6a322f3a3ea49778314e4005b5878b20f121
index empty
tracked clean
Git-visible untracked 2 exact
legacy 1400 active exact
```

Move current Task byte-identically active→done.

Final:

```text
Git-visible untracked 3 exact:
current Cycle
current Judgment
current done Task

legacy 1400 active:
present / exact / ignored / non-owned
```

No Git commit/push.

# 22. contract review

Require exactly 83 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
CURRENT_STATE_HASHES_EXACT
PERSISTED_SOURCE_HASHES_EXACT
PYTHON_EXECUTABLE_EXACT
DOCKER_EXECUTABLE_EXACT
PRE_DELIVERY_UNTRACKED_NONE
LEGACY_1400_ACTIVE_EXACT
PRIVATE_POSTGRES_CONTAINER_IDENTITY_EXACT
PRIVATE_POSTGRES_IMAGE_EXACT
PRIVATE_POSTGRES_VOLUME_EXACT
PRIVATE_POSTGRES_ENDPOINT_EXACT
PRIVATE_SECRET_BIND_DESTINATION_RO_EXACT
SECRET_SOURCE_REPRESENTATION_EXACT
SECRET_SOURCE_NATIVE_REVERSE_MAPPING_EXACT
PRIVATE_RUNTIME_ROOT_DERIVATION_EXACT
PRIVATE_RUNTIME_ROOT_EXISTS_DIRECTORY
PRIVATE_RUNTIME_ROOT_NO_REPARSE_BOUNDARY
PRIVATE_RUNTIME_ROOT_PRIVATE_ACL_EXACT
PRIVATE_RUNTIME_ROOT_NO_REPO_DOWNLOAD_OVERLAP
PRIVATE_PATH_VALUES_NOT_EXPORTED
PRIVATE_DB_MIGRATION_HEAD_EXACT
SECRET_VALUE_NOT_EXPORTED
STOCKROOM_IMAGE_ID_EXACT
NO_RUNNING_STOCKROOM_TRANSIENT
PREFLIGHT_WORKRUN_RUNNING_V2
PREFLIGHT_ATTEMPT_NOT_STARTED_V1
PREFLIGHT_ATTEMPT_CAUSAL_READY_V1
PREFLIGHT_RUN_ATTEMPT_BINDING_EXACT
PREFLIGHT_EXECUTION_OPERATIONS_ZERO
PREFLIGHT_EXECUTION_OUTPUTS_ZERO
PREFLIGHT_EXECUTION_STARTED_EVENTS_ZERO
PREFLIGHT_INVALID_HISTORY_ABORT_EVENTS_ZERO
PREFLIGHT_RUNTIME_EVIDENCE_ZERO
PREFLIGHT_JUDGMENT_ZERO
PREFLIGHT_NO_NEWER_ATTEMPT
PREFLIGHT_WORKSPACE_EXISTS_EXACT
PREFLIGHT_WORKSPACE_OBJECT_COUNT_20
PREFLIGHT_WORKSPACE_FILE_COUNT_14
PREFLIGHT_WORKSPACE_BYTES_2320
PREFLIGHT_WORKSPACE_FINGERPRINT_EXACT
PREFLIGHT_WORKSPACE_SAFE_INVENTORY
PREFLIGHT_NO_EXISTING_QUARANTINE_AMBIGUITY
PREFLIGHT_DOUBLE_READ_DB_STABLE
DEDICATED_BUILDER_SINGLE_CALL_EXACT
DEDICATED_BUILDER_REQUESTER_EXACT
DEDICATED_BUILDER_NO_REGISTRATION_DELTA
DEDICATED_BUILDER_NO_EXECUTION_STACK
DISPOSITION_SERVICE_SOURCE_OWNED
PROVENANCE_REFS_EXACT
AUTHORIZE_SINGLE_CALL_EXACT
AUTHORIZE_EXPECTED_STATE_VERSION_2
AUTHORIZE_EXPECTED_EXECUTION_VERSION_1
AUTHORIZE_WORKSPACE_AUTHORITY_EXACT
FINAL_PREMUTATION_DB_RECHECK_EXACT
FINAL_PREMUTATION_WORKSPACE_RECHECK_EXACT
FINAL_PREMUTATION_TRANSIENT_RECHECK_EXACT
DISPOSE_CALLED_ONCE_MAXIMUM
ABORT_EVENT_EXACT_ONE
ATTEMPT_EXECUTION_FAILED_V2
ATTEMPT_CAUSAL_RUNNING_V2
WORKRUN_FAILED_V3
FAILURE_TRANSITION_EXACT_ONE
G_FAILURE_TERMINAL_REASON_EXACT
WORKSPACE_QUARANTINED_EXACT
WORKSPACE_ORIGINAL_TARGET_ABSENT
QUARANTINE_FINGERPRINT_EXACT
QUARANTINE_BYTES_PRESERVED
NO_PROVIDER_OPERATION_CREATED
NO_EXECUTION_OUTPUT_SUBMISSION_CREATED
NO_RUNTIME_EVIDENCE_CREATED
NO_JUDGMENT_CREATED
NO_NEW_RUN_CREATED
NO_NEW_ATTEMPT_CREATED
NO_STOCKROOM_CONTAINER_LAUNCHED
NO_SOURCE_TEST_STATE_GIT_MUTATION
NO_AUTOMATIC_DISPOSE_RETRY
FAILURE_STAGE_REINSPECTION_DEFINED
PRIVATE_VALUE_EXPORT_SCAN_PASS
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_UNTRACKED_3_EXACT
FINAL_LEGACY_1400_ACTIVE_PRESERVED
EXPORT_INTEGRITY_PASS
```

Success:
```text
83 / 83 PASS
```

For a preflight stop/partial result, unobserved success rows are BLOCKED_REQUIRED_EVIDENCE.

# 23. export

Root docs exactly 14:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
PRIVATE_RUNTIME_IDENTITY_VERIFICATION.md
PRE_DISPOSITION_DB_SNAPSHOT.md
PRE_DISPOSITION_WORKSPACE_SNAPSHOT.md
DEDICATED_BUILDER_VERIFICATION.md
DISPOSITION_AUTHORIZATION_VERIFICATION.md
DISPOSITION_RESULT_VERIFICATION.md
POST_DISPOSITION_DB_SNAPSHOT.md
WORKSPACE_QUARANTINE_VERIFICATION.md
PRIVATE_VALUE_SCAN.md
CONTRACT_REVIEW.md
```

Project-relative copies exactly 3:

```text
current Cycle
current Judgment
current done Task
```

Success export:

```text
17 total members
16 non-self manifest rows
one top-level directory
CRC PASS
TASK.md == canonical done Task
manifest hashes exact
```

Do not copy private runtime bytes.

# 24. success ceiling

```text
0036 attempt:
EXECUTION_FAILED/v2

0036 WorkRun:
FAILED/v3

historical workspace:
QUARANTINED / PRESERVED

provider/tool execution:
NONE

runtime evidence/Judgment:
NONE

new run/attempt:
NONE

private PostgreSQL:
RETAINED

Browser runtime acceptance:
PENDING

Git/state persistence:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
