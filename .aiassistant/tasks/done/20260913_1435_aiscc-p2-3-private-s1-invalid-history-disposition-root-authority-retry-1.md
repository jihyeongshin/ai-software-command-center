# 작업지시서: P2-3 private S1 invalid-history disposition root-authority retry

## meta

- task_id: `20260913_1435_aiscc-p2-3-private-s1-invalid-history-disposition-root-authority-retry-1`
- created_at: `2026-09-13T14:35:14+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PRIVATE_S1_INVALID_HISTORY_DISPOSITION_EXECUTION_RETRY`
- evidence_profile: `PRIVATE_RUNTIME_MUTATION_HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `86288febf1cbd94bbb0235cfc680bf6c6c8f7772`
- required_parent: `4341138dde5fbea487f10a8af256f78c5dcf37f3`
- required_grandparent: `5affe61f02994f219b22ca934b5e0b93bc5e6f60`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- docker_executable: `C:\Program Files\Docker\Docker\resources\bin\docker.exe`
- predecessor_1406_result_zip_sha256: `549e03fcccfac558d50de0f019ea1314606acb3ab4906d9e6f383c031f052ab2`
- accepted_persistence_result_zip_sha256: `012cc5f5abdaff9669c13f15268924f18ae13eedbec524d03c6b29dfa789862e`
- accepted_0036_result_zip_sha256: `041285052e8fad97636231be69775e0dd7003b3d1b1683b64200cdc931eb0ac5`
- accepted_1242_result_zip_sha256: `b1dc8f91d1ba01c0198953fad70ace3d3c45276fe279d35c50521f2ad02b1381`
- private_runtime_read_authorized: `Yes / exact retained resources`
- private_runtime_mutation_authorized: `Conditional / one persisted disposition`
- source_test_state_write_authorized: `No`
- new_execution_authorized: `No`
- new_run_attempt_authorized: `No`
- success_ceiling: `PRIVATE_S1_INVALID_HISTORY_DISPOSED / BROWSER_REVIEW_PENDING`

# 0. purpose

Retry the exact 1406 runtime disposition after correcting only its operator-context transport defect.

1406 performed no private runtime access and no mutation.

Exact subject remains:

```text
run_id:
aiscc-p2-3-private-s1-normal-v1-run

attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1
```

Expected initial durable authority remains:

```text
WorkRun:
RUNNING / v2

ExecutionAttempt:
NOT_STARTED / execution_version 1 / causal READY-v1

execution operations:
0

execution outputs/submission:
0

runtime evidence:
0

Judgment:
0
```

No mutation is allowed until every read-only preflight predicate passes.

# 1. transport / Python

Use only:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Docker CLI use is limited to:

```text
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

Do not discover another Docker or Python executable through PATH.

Forbidden Python aliases:

```text
python
py
WindowsApps Python alias
```

Verify delivery ZIP/hash and exactly three flat safe members.

Place current Task first:

```text
.aiassistant/tasks/active/20260913_1435_aiscc-p2-3-private-s1-invalid-history-disposition-root-authority-retry-1.md
```

Then place:

```text
.aiassistant/records/aiscc/cycles/20260913_1435_aiscc-p2-3-private-s1-root-authority-reconstructed-disposition-retry-entry-1.cycle.md
SHA-256 e944e78cddea422c1f8f586d2eb307bf4ab160c6c80862d645e5c14cebe9e5c2

.aiassistant/reports/aiscc/20260913_1435_aiscc-p2-3-private-s1-root-authority-transport-gap-retry-judgment-1.md
SHA-256 bfd93a83bd7c7b688f940e0a27f3e4c3f56bae3edb13492de9d25138a80df9c7
```

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
HEAD 86288febf1cbd94bbb0235cfc680bf6c6c8f7772
HEAD^ 4341138dde5fbea487f10a8af256f78c5dcf37f3
HEAD^^ 5affe61f02994f219b22ca934b5e0b93bc5e6f60
index empty
tracked clean
```

Before current delivery Git-visible untracked exactly three:

- `.aiassistant/tasks/done/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-1.md`  `20d611ac457a9db0a95d331a482123022629fbc80e1c9bc5f307db3ab43115d3`
- `.aiassistant/records/aiscc/cycles/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-entry-1.cycle.md`  `6acf1ab71a82dc16090c14d8b6bf5d4ad4dd46456729ab657afb26d580f86d2e`
- `.aiassistant/reports/aiscc/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-authorization-judgment-1.md`  `c10465e987246d7932a665e2c763c69de7711cba6dafb438e6239e0c02866087`

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `b551c534dcf55a3e5e20c4cb379cf1957ba8f719f1bb6d75c980ce5de7cd6283`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `551d0df4a5ad14a4fd825057f18d95d157b8fefb3a9821d26ef92fc2664ce74a`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `36687e0653375ca3c3ea4daf6393ced5a1856e1c70f5822408002322a964da24`

Persisted source/rule hashes:

- `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`  `382433d24959827fc606592e7beb78f34934209fa2f9c34aabdeda1c6e322784`
- `src/aiscc/providers/events.py`  `69b0339a12630eb552ef479a819c78596a2c0094437b4458a30eebb730c18a98`
- `src/aiscc/persistence/repository.py`  `57dac018f6505468d62588761825025776d07384947424dad37b63f9f35e5e54`
- `src/aiscc/scenarios/stockroom_production.py`  `abbe7f81840de7d9525900511f967512c72cf114104128501c681c19fbacd127`
- `src/aiscc/runtime/stockroom_workspace.py`  `1b8366b5c5a6e9054dbd65ef36cd09808074c88ccf6c7ad060a9a76a488efaab`
- `src/aiscc/bootstrap.py`  `745b58da26ec300286ed69d1a7477b21afeb7625ec43e7f422560a657bc1c115`

After current Cycle/Judgment placement while Task is active/ignored:

```text
Git-visible untracked = 5 exact

1406 Task/Cycle/Judgment
current Cycle/Judgment
```

Unexpected source/state/Git dirt:

```text
STOP before private runtime access
```

# 3. exact retained container authority

Inspect only these exact retained identities with `C:\Program Files\Docker\Docker\resources\bin\docker.exe`:

```text
container:
aiscc-p2-3-private-postgres-v1

container ID:
0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c

PostgreSQL image:
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

Require the container is running.

Do not start/recreate/repair anything on mismatch.

# 4. reconstruct exact private runtime-root authority

This section supersedes only the 1406 requirement that the absolute root already be held in chat context.

From the exact retained PostgreSQL container inspect result:

1. Select exactly one mount whose Destination is:

```text
/run/secrets/postgres_password
```

2. Require:

```text
Type = bind
RW = false
```

3. Treat its `Source` as private authority and never print/export it.

4. Require the observed Source matches exactly this Docker Desktop representation class:

```text
/run/desktop/mnt/host/<single drive letter>/<non-empty safe suffix>
```

5. Normalize only by:

```text
drive = uppercase drive letter
suffix segments = slash-separated Source suffix
native secret path = <DRIVE>:\ + exact suffix segments
```

Every suffix segment must be:

```text
non-empty
not "." or ".."
contain no ":"
contain no "\"
```

6. Reverse-map the native secret path back to Docker Desktop representation and require byte-for-byte equality with the
observed bind Source.

7. Derive exactly:

```text
private_runtime_root = native_secret_path.parent / "aiscc-p2-3-private-runtime-v1"
```

No other runtime-root candidate is permitted.

This is deterministic authority reconstruction, not filesystem search.

# 5. native private-boundary verification

For:

```text
native secret path
secret parent
derived private runtime root
```

require:

```text
absolute
exists
strict resolve == same path
no symlink/reparse point on the object or any ancestor
secret is a regular file
runtime root is a directory
```

Require the runtime root leaf name exactly:

```text
aiscc-p2-3-private-runtime-v1
```

Require no overlap with:

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

Downloads:
C:\Users\oracl\Downloads

.aiassistant/reports/target
```

Do not require the runtime root to be empty; historical materialization is expected.

# 6. ACL boundary

Using native ACL inspection only on:

```text
secret parent
secret file
derived runtime root
```

require:

```text
parent ACL inheritance protected

allowed Allow principals only:
current user SID
SYSTEM
Administrators

child/runtime Allow rights:
no broader than corresponding parent principal rights
```

Do not mutate ACLs.

Any ACL ambiguity/failure:

```text
STOP_PRESERVE
```

# 7. private-value denylist

Before reading secret bytes, add all forms of these values to an in-memory export denylist:

```text
raw Docker bind Source
native secret absolute path
derived runtime-root absolute path
JSON-escaped variants
```

After password acquisition, add:

```text
password bytes
decoded password
credential-bearing DB URL
```

None may appear in report/export.

# 8. PostgreSQL connection and migration

Read the password only from the verified native secret file.

Construct the credential URL only in memory.

Connect only to:

```text
127.0.0.1:55432
database aiscc_private_capture
role aiscc_private_capture
```

Require:

```text
current_database/current_user exact
migration head 20260901_0008
```

Never print/export password or URL.

# 9. retained Stockroom image / transient check

Read-only inspect exact image:

```text
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e
```

Require discovery tag still maps to the exact accepted image:

```text
aiscc-stockroom-runtime:p2-3-private-v1
```

Require no running container using this exact Stockroom image.

If one exists:

```text
UNEXPECTED_RUNNING_STOCKROOM_TRANSIENT
→ STOP_PRESERVE
```

Do not stop/remove it.

# 10. Phase A read-only DB preflight

Before builder or mutation, query the retained DB read-only.

Require exact:

## WorkRun

```text
work_run_id:
aiscc-p2-3-private-s1-normal-v1-run

workflow_state:
RUNNING

state_version:
2
```

## ExecutionAttempt

```text
execution_attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1

work_run_id:
aiscc-p2-3-private-s1-normal-v1-run

status:
NOT_STARTED

execution_version:
1

creation_state:
READY

creation_state_version:
1

causal_state:
READY

causal_state_version:
1

task_contract_id/version:
exactly equal WorkRun

runtime_mode:
exactly equal WorkRun
```

## downstream counts

Require:

```text
ExecutionOperation rows for attempt:
0

ExecutionOutputRef/submission rows for attempt:
0

EXECUTION_STARTED events for attempt:
0

EXECUTION_ABORTED_INVALID_HISTORY events for attempt:
0

admitted SYSTEM_RUNTIME_OBSERVATION evidence for WorkRun:
0

Judgment rows for WorkRun:
0

later/current competing execution attempt:
none
```

Any mismatch:

```text
STOP_PRESERVE
no builder
no disposition
```

# 11. Phase A workspace preflight

Using persisted:

```text
StockroomRestartSafetySettlement.inspect
```

and the exact derived private root, inspect only:

```text
aiscc-p2-3-private-s1-normal-v1-run
aiscc-p2-3-private-s1-normal-v1-attempt-1
```

Require:

```text
active attempt workspace exists
exact deterministic target under derived root
safe regular-directory identity
bounded inventory
64-hex inventory fingerprint
no symlink/reparse/hardlink/special-object violation
no multiple matching quarantine entries
```

Do not export absolute root/path or file contents.

Record only sanitized relative identity, counts, bounded byte total if safely available, and inventory fingerprint.

Absent/unsafe/ambiguous:

```text
STOP_PRESERVE
```

# 12. Phase A DB stability re-read

After workspace/Docker observations, repeat section 10 read-only.

Require all authoritative fields/counts unchanged.

Any change:

```text
CONCURRENT_PRIVATE_STATE_CHANGE
→ STOP_PRESERVE
```

# 13. builder re-entry gate

Only after all previous sections pass, construct the persisted production application exactly once using the same exact:

```text
repository root
derived private runtime root
Downloads root
accepted image provenance/ref
trusted Docker executable
retained PostgreSQL session factory
project/requester/security identities
```

Do not call:

```text
prepare_capture
runner
provider/tool execution
```

Before and after builder, compare accepted authority enrollment rows.

Require unchanged semantic rows:

```text
Evidence requirement sets/requirements/checkpoints:
4 / 4 / 4

Judgment policies/projections:
2 / 2
```

Any semantic delta:

```text
BUILDER_REENTRY_MUTATION
→ STOP before disposition
```

# 14. source-owned disposition owner

Use only:

```text
application.invalid_history_disposition_service()
```

Do not directly invoke repository abort or workflow transition for mutation.

# 15. exact provenance refs

Supply exactly this ordered tuple:

```text
aiscc-accepted-runtime-evidence:v1:0036:sha256:041285052e8fad97636231be69775e0dd7003b3d1b1683b64200cdc931eb0ac5
aiscc-accepted-disposition-contract:v1:1242:sha256:b1dc8f91d1ba01c0198953fad70ace3d3c45276fe279d35c50521f2ad02b1381
```

The source-owned service must append the exact workspace-fingerprint authority.

# 16. authorize — read-only sealing

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

Require returned request exact:

```text
run/attempt exact
state version 2
execution version 1
reason INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START
workspace identity == Phase A
workspace fingerprint == Phase A
provenance == exact supplied refs + exact source-owned workspace ref
```

Failure:

```text
STOP_PRESERVE
dispose calls 0
```

# 17. final pre-mutation recheck

Immediately before disposition, re-read:

```text
DB authority/counts
workspace inspection/fingerprint
running Stockroom transient state
```

Require exact equality with Phase A and sealed request.

Any mismatch:

```text
STOP_PRESERVE
dispose calls 0
```

# 18. single disposition invocation

Call only:

```text
result = await service.dispose(request)
```

Maximum call count:

```text
1
```

Never automatically retry after exception.

Do not directly call repository abort or manual WorkRun transition.

# 19. expected successful result

Require:

## attempt

```text
EXECUTION_FAILED
execution_version 2
causal RUNNING/v2
one EXECUTION_ABORTED_INVALID_HISTORY event
reason INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START
```

## WorkRun

```text
FAILED/v3
one admitted RUNNING/v2 → FAILED/v3 transition
authentic G_FAILURE_TERMINAL
exact invalid-history reason
```

## workspace

Because Phase A required active workspace:

```text
QUARANTINED
original active target absent
one exact quarantine target
inventory fingerprint preserved
bytes preserved
not reusable as active workspace
```

Do not delete quarantine.

# 20. post-success verification

Read-only verify:

```text
WorkRun FAILED/v3
attempt EXECUTION_FAILED/v2
attempt causal RUNNING/v2
abort event count 1
EXECUTION_STARTED event count 0
execution operations 0
execution outputs/submission 0
runtime evidence 0
Judgment 0
new WorkRuns 0
new attempts 0
authority enrollment rows unchanged
```

Require no Stockroom provider/runtime container was launched.

Retain private PostgreSQL container/volume unchanged.

# 21. exception / partial-state handling

If `dispose(request)` raises:

```text
never retry automatically
```

Re-inspect read-only only and classify:

```text
P0:
attempt NOT_STARTED/v1
WorkRun RUNNING/v2
active workspace unchanged

P1:
attempt EXECUTION_FAILED/v2
WorkRun RUNNING/v2
active workspace unchanged

P2:
attempt EXECUTION_FAILED/v2
WorkRun FAILED/v3
active workspace unchanged

P3:
attempt EXECUTION_FAILED/v2
WorkRun FAILED/v3
active target absent
one exact matching quarantine target
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

# 22. no evidence/Judgment/retry

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

# 23. export privacy

Before export scan every generated member for:

```text
raw Docker secret bind Source
native secret absolute path
absolute runtime-root path
PostgreSQL password
credential-bearing DB URL
absolute host secret-source path
```

Required matches:

```text
0
```

Use sanitized placeholders/root-relative identities only.

# 24. Git boundary

This Task must not modify tracked source/state.

Before Task move:

```text
HEAD 86288febf1cbd94bbb0235cfc680bf6c6c8f7772
index empty
tracked clean
Git-visible untracked = 5 exact
```

Move current Task byte-identically active→done.

Final Git-visible untracked:

```text
6 exact

1406 Task/Cycle/Judgment
current Task/Cycle/Judgment
```

No Git commit/push.

# 25. contract review

Require exactly 76 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_1406_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
PERSISTED_SOURCE_HASHES_EXACT
PYTHON_EXECUTABLE_EXACT
DOCKER_EXECUTABLE_EXACT
PRE_DELIVERY_UNTRACKED_3_EXACT
PRIVATE_POSTGRES_CONTAINER_IDENTITY_EXACT
PRIVATE_POSTGRES_IMAGE_EXACT
PRIVATE_POSTGRES_VOLUME_EXACT
PRIVATE_POSTGRES_ENDPOINT_EXACT
PRIVATE_SECRET_BIND_DESTINATION_RO_EXACT
SECRET_SOURCE_REPRESENTATION_EXACT
SECRET_SOURCE_SEGMENTS_SAFE
SECRET_SOURCE_NATIVE_REVERSE_MAPPING_EXACT
PRIVATE_RUNTIME_ROOT_FIXED_CHILD_DERIVATION_EXACT
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
PREFLIGHT_RUN_ATTEMPT_TASK_RUNTIME_BINDING_EXACT
PREFLIGHT_EXECUTION_OPERATIONS_ZERO
PREFLIGHT_EXECUTION_OUTPUTS_ZERO
PREFLIGHT_EXECUTION_STARTED_EVENTS_ZERO
PREFLIGHT_INVALID_HISTORY_ABORT_EVENTS_ZERO
PREFLIGHT_RUNTIME_EVIDENCE_ZERO
PREFLIGHT_JUDGMENT_ZERO
PREFLIGHT_NO_NEWER_ATTEMPT
PREFLIGHT_WORKSPACE_EXISTS_EXACT
PREFLIGHT_WORKSPACE_SAFE_INVENTORY
PREFLIGHT_WORKSPACE_FINGERPRINT_CAPTURED
PREFLIGHT_NO_EXISTING_QUARANTINE_AMBIGUITY
PREFLIGHT_DOUBLE_READ_DB_STABLE
BUILDER_SINGLE_CALL_EXACT
BUILDER_AUTHORITY_ENROLLMENTS_UNCHANGED
DISPOSITION_SERVICE_SOURCE_OWNED
PROVENANCE_REFS_EXACT
AUTHORIZE_EXPECTED_STATE_VERSION_2
AUTHORIZE_EXPECTED_EXECUTION_VERSION_1
AUTHORIZE_WORKSPACE_AUTHORITY_EXACT
FINAL_PREMUTATION_DB_RECHECK_EXACT
FINAL_PREMUTATION_WORKSPACE_RECHECK_EXACT
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
AUTHORITY_ENROLLMENTS_UNCHANGED_AFTER
NO_SOURCE_TEST_STATE_GIT_MUTATION
NO_AUTOMATIC_DISPOSE_RETRY
FAILURE_STAGE_REINSPECTION_DEFINED
PRIVATE_VALUE_EXPORT_SCAN_PASS
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
EXPORT_INTEGRITY_PASS
```

Success requires:

```text
76 / 76 PASS
```

On preflight stop or partial mutation, non-observed rows are `BLOCKED_REQUIRED_EVIDENCE`.

# 26. export

Root docs exactly 14:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
PRIVATE_RUNTIME_IDENTITY_VERIFICATION.md
PRE_DISPOSITION_DB_SNAPSHOT.md
PRE_DISPOSITION_WORKSPACE_SNAPSHOT.md
BUILDER_REENTRY_VERIFICATION.md
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
folder/archive byte equality
TASK.md == canonical done Task
```

Do not copy private runtime/source bytes into export.

# 27. success ceiling

```text
0036 exact attempt:
EXECUTION_FAILED/v2

0036 exact WorkRun:
FAILED/v3

historical active workspace:
QUARANTINED/PRESERVED

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

Git persistence/state reconciliation:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
