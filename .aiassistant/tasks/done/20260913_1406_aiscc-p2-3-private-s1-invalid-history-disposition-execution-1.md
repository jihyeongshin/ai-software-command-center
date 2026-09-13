# 작업지시서: P2-3 private S1 invalid-history disposition execution

## meta

- task_id: `20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-1`
- created_at: `2026-09-13T14:06:56+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PRIVATE_S1_INVALID_HISTORY_DISPOSITION_EXECUTION`
- evidence_profile: `PRIVATE_RUNTIME_MUTATION_HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `86288febf1cbd94bbb0235cfc680bf6c6c8f7772`
- required_parent: `4341138dde5fbea487f10a8af256f78c5dcf37f3`
- required_grandparent: `5affe61f02994f219b22ca934b5e0b93bc5e6f60`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- accepted_persistence_result_zip_sha256: `012cc5f5abdaff9669c13f15268924f18ae13eedbec524d03c6b29dfa789862e`
- private_runtime_read_authorized: `Yes / exact retained resources`
- private_runtime_mutation_authorized: `Conditional / one persisted disposition`
- source_test_state_write_authorized: `No`
- new_execution_authorized: `No`
- new_run_attempt_authorized: `No`
- success_ceiling: `PRIVATE_S1_INVALID_HISTORY_DISPOSED / BROWSER_REVIEW_PENDING`

# 0. purpose

Execute the already persisted invalid-history disposition against exactly one retained private S1 run/attempt.

Exact subject:

```text
run_id:
aiscc-p2-3-private-s1-normal-v1-run

attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1
```

Expected initial durable authority:

```text
WorkRun:
RUNNING / v2

ExecutionAttempt:
NOT_STARTED

execution_version:
1

attempt causal state:
READY / v1

execution operations:
0

execution outputs/submission:
0

runtime evidence:
0

Judgment:
0
```

Expected historical side effect:

```text
attempt-scoped materialized workspace exists and is independently inspectable
```

No mutation is allowed until every Phase A read-only predicate passes.

# 1. transport / Python

Use only:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Forbidden:

```text
python
py
WindowsApps Python alias
PATH Python discovery
```

Verify inbound ZIP/hash and exactly three flat safe members.

Place current Task first:

```text
.aiassistant/tasks/active/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-1.md
```

Then place exact Cycle/Judgment:

```text
.aiassistant/records/aiscc/cycles/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-entry-1.cycle.md
SHA-256 6acf1ab71a82dc16090c14d8b6bf5d4ad4dd46456729ab657afb26d580f86d2e

.aiassistant/reports/aiscc/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-authorization-judgment-1.md
SHA-256 c10465e987246d7932a665e2c763c69de7711cba6dafb438e6239e0c02866087
```

Transport/bootstrap mismatch:

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
Git-visible untracked before delivery none
```

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
Git-visible untracked:
2 exact

current Cycle
current Judgment
```

Unexpected source/state/Git dirt:

```text
STOP before private runtime access
```

# 3. exact retained PostgreSQL identity

Private runtime access begins here.

Inspect only the exact retained PostgreSQL container:

```text
container name:
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

secret destination:
`/run/secrets/postgres_password`

secret mount:
read-only
```

Require container running and exact identity.

Do not start, recreate or repair the container if any identity differs.

Verify migration head:

```text
20260901_0008
```

Read the password only from the exact retained secret mount/source needed for authenticated access.

Never print, log, report or export the password or credential-bearing URL.

# 4. exact private runtime root identity

Use only the exact retained private runtime root value already held by the existing 0036 private-runtime operator context.

Important:

```text
the absolute private runtime-root path is intentionally not canonical/exported
```

Therefore:

```text
do not search disks/directories to rediscover it
do not infer a new path
do not create a replacement root
```

If the exact previously used retained root value is not available to the Executor from the existing private-runtime
context:

```text
PRIVATE_RUNTIME_ROOT_IDENTITY_UNAVAILABLE
→ STOP before mutation
```

Instantiate the restart-safe workspace inspector only against that exact root and current repository/source-object/downloads
exclusions.

Do not export the absolute private root path.

# 5. retained Stockroom image / transient check

Verify locally retained Stockroom image:

```text
image ID:
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e

tag:
aiscc-stockroom-runtime:p2-3-private-v1
```

Read-only inspect only.

Require no running container using this exact Stockroom image before disposition.

If one exists:

```text
UNEXPECTED_RUNNING_STOCKROOM_TRANSIENT
→ STOP_PRESERVE
```

Do not stop/remove it in this Task.

# 6. Phase A read-only DB preflight

Before `build_stockroom_production` or any source-owned mutation, query the retained DB read-only.

Use current repository models/schema; do not hand-edit rows.

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

ExecutionOutputRef rows for attempt:
0

EXECUTION_STARTED events for attempt:
0

EXECUTION_ABORTED_INVALID_HISTORY events for attempt:
0

admitted SYSTEM_RUNTIME_OBSERVATION evidence for WorkRun:
0

Judgment rows for WorkRun:
0
```

Also require:

```text
no later/current competing execution attempt for this WorkRun
no second nonterminal attempt
```

Record non-secret row identities/counts only.

Any mismatch:

```text
STOP_PRESERVE
no builder
no disposition
```

# 7. Phase A read-only workspace preflight

Using persisted:

```text
StockroomRestartSafetySettlement.inspect
```

inspect exactly:

```text
aiscc-p2-3-private-s1-normal-v1-run
aiscc-p2-3-private-s1-normal-v1-attempt-1
```

Require:

```text
exists:
True

target:
exact deterministic attempt-scoped target under retained root

target identity:
valid regular directory identity

inventory:
within source bounds

inventory fingerprint:
64-hex exact

no symlink/reparse/hardlink/special-object violation

no multiple matching quarantine entries
```

Do not export:

```text
absolute retained root path
materialized file contents
host-private source paths
```

Record only:

```text
exists
sanitized relative identity
object/file counts
total bounded bytes if safely available
inventory fingerprint
```

If workspace is absent, already ambiguously quarantined, unsafe, or inventory-bound fails:

```text
STOP_PRESERVE
```

# 8. Phase A DB stability re-read

After Docker and workspace read-only inspection, repeat the exact DB authority query from section 6.

Require byte/semantic equality of every authoritative field/count.

Any change:

```text
CONCURRENT_PRIVATE_STATE_CHANGE
→ STOP_PRESERVE
```

# 9. builder re-entry gate

Only after Phase A passes, create the current persisted production application exactly once using the same retained
private configuration and source-owned builder pattern used for the accepted private S1 path.

Do not call:

```text
prepare_capture
runner
provider/tool execution
```

Builder call count:

```text
exactly 1
```

Before and after builder construction, compare the already accepted bounded authority-enrollment rows.

Require semantic/byte equality for the existing:

```text
Evidence requirement sets/requirements/checkpoints:
4 / 4 / 4

Judgment policies/projections:
2 / 2
```

Builder may re-register exact existing authority, but no semantic row/value delta is allowed.

Any delta:

```text
BUILDER_REENTRY_MUTATION
→ STOP before disposition
```

# 10. construct the source-owned disposition owner

Use only:

```text
application.invalid_history_disposition_service()
```

Do not directly instantiate a replacement repository/guard/workflow owner for mutation.

The service must be the persisted source implementation at current HEAD.

# 11. exact non-workspace provenance refs

Use exactly this ordered tuple:

```text
aiscc-accepted-runtime-evidence:v1:0036:sha256:041285052e8fad97636231be69775e0dd7003b3d1b1683b64200cdc931eb0ac5
aiscc-accepted-disposition-contract:v1:1242:sha256:b1dc8f91d1ba01c0198953fad70ace3d3c45276fe279d35c50521f2ad02b1381
```

Do not add arbitrary provenance refs.

The service itself must append:

```text
stockroom-invalid-history-workspace:v1:<exact current inventory fingerprint>
```

# 12. authorize — read-only sealing

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

`authorize()` is expected to remain read-only.

Require returned request exact:

```text
run/attempt IDs exact
state version 2
execution version 1
reason:
INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START

expected_workspace_identity:
matches Phase A inspection

expected_workspace_fingerprint:
matches Phase A fingerprint

provenance_refs:
exact two supplied refs + exact source-owned workspace ref
```

If authorize fails:

```text
STOP_PRESERVE
no dispose call
```

# 13. final pre-mutation recheck

Immediately before `dispose(request)`, re-read:

```text
WorkRun
ExecutionAttempt
downstream counts
workspace inspection
running Stockroom transient state
```

Require exact equality with Phase A and the sealed request.

No new running Stockroom container may appear.

Any mismatch:

```text
STOP_PRESERVE
dispose call count 0
```

# 14. single disposition invocation

Only now call:

```text
result = await service.dispose(request)
```

Call count:

```text
maximum 1
```

Do not call `dispose` again automatically if it raises.

Do not directly call `abort_invalid_history_attempt` outside the source-owned disposition service.

Do not issue a manual WorkRun transition.

# 15. expected successful durable result

Require result exact:

## attempt abort

```text
status:
EXECUTION_FAILED

execution_version:
2

causal state:
RUNNING / v2

abort event:
EXECUTION_ABORTED_INVALID_HISTORY

abort event count:
1

reason:
INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START
```

## WorkRun

```text
state:
FAILED

state_version:
3

transition:
RUNNING/v2 → FAILED/v3

decision:
ADMITTED

G_FAILURE_TERMINAL:
exactly one satisfied observation

guard reason:
INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START
```

## workspace

Because Phase A required an existing active target, success must return:

```text
QUARANTINED
```

Require:

```text
original exact attempt target absent
one exact quarantine target exists
post-move inventory fingerprint == sealed preflight fingerprint
quarantined bytes preserved
quarantine is not active/reused
```

Do not delete quarantine.

# 16. post-success DB verification

Read-only verify:

```text
WorkRun FAILED/v3

attempt EXECUTION_FAILED/v2
attempt causal RUNNING/v2

EXECUTION_ABORTED_INVALID_HISTORY events:
1

EXECUTION_STARTED events:
0

execution operations:
0

execution outputs/submission:
0

runtime evidence:
0

Judgment:
0

number of WorkRuns added:
0

number of attempts added:
0
```

Require no provider/tool operation/event rows were created.

Require the authority-enrollment rows from section 9 remain unchanged.

# 17. post-success Docker verification

Require no new/running Stockroom container was launched by disposition.

Do not stop unrelated resources.

Retain PostgreSQL container/volume exactly as-is.

# 18. no evidence / Judgment / retry

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

The technical WorkRun `FAILED` state is disposition, not a semantic scenario Judgment.

# 19. exception / partial-mutation handling

If `dispose(request)` raises, never retry automatically.

Immediately perform read-only stage classification only.

Allowed observed shapes:

## Stage P0 — no durable disposition mutation

```text
attempt NOT_STARTED/v1
WorkRun RUNNING/v2
active workspace unchanged
```

## Stage P1 — attempt aborted only

```text
attempt EXECUTION_FAILED/v2
WorkRun RUNNING/v2
active workspace unchanged
```

## Stage P2 — attempt + WorkRun terminal, workspace unsettled

```text
attempt EXECUTION_FAILED/v2
WorkRun FAILED/v3
active workspace still exact
```

## Stage P3 — durable terminal + quarantine apparently completed

```text
attempt EXECUTION_FAILED/v2
WorkRun FAILED/v3
active target absent
one exact matching quarantine target
```

Anything else:

```text
PARTIAL_DISPOSITION_STATE_UNEXPECTED
```

For every exception outcome:

```text
STOP_PRESERVE
no second dispose
no cleanup
no retry
no new attempt
export truthful partial-state evidence for Browser review
```

# 20. private-value export policy

Before export scan every generated report/export member for:

```text
PostgreSQL password
credential-bearing database URL
absolute private runtime-root path
absolute host secret-source path
```

Required matches:

```text
0
```

Use placeholders/fingerprints only:

```text
[PRIVATE_DB_URL]
[PRIVATE_RUNTIME_ROOT]
[PRIVATE_SECRET_SOURCE]
```

The quarantine absolute path must also be sanitized to a root-relative identity.

# 21. Git / source boundary

This runtime Task does not modify repository tracked source/state.

Before Task move require:

```text
HEAD 86288febf1cbd94bbb0235cfc680bf6c6c8f7772
index empty
tracked clean
Git-visible untracked = 2 exact
```

Move current Task byte-identically:

```text
.aiassistant/tasks/active/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-1.md
→
.aiassistant/tasks/done/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-1.md
```

Final Git-visible untracked:

```text
3 exact

current Cycle
current Judgment
current done Task
```

No Git commit or push.

# 22. contract review

Require exactly 67 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
CURRENT_STATE_HASHES_EXACT
PERSISTED_SOURCE_HASHES_EXACT
PYTHON_EXECUTABLE_EXACT
PRE_DELIVERY_UNTRACKED_NONE
PRIVATE_POSTGRES_CONTAINER_IDENTITY_EXACT
PRIVATE_POSTGRES_IMAGE_EXACT
PRIVATE_POSTGRES_VOLUME_EXACT
PRIVATE_POSTGRES_ENDPOINT_EXACT
PRIVATE_DB_MIGRATION_HEAD_EXACT
PRIVATE_SECRET_MOUNT_READONLY_EXACT
SECRET_VALUE_NOT_EXPORTED
PRIVATE_RUNTIME_ROOT_EXACT_PRIOR_OPERATOR_IDENTITY
NO_PRIVATE_ROOT_BROAD_DISCOVERY
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

Success:

```text
67 / 67 PASS
```

For a preflight stop or partial mutation, non-observed success rows must be `BLOCKED_REQUIRED_EVIDENCE`, not fabricated.

# 23. success export

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

Successful export:

```text
17 total members
16 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == canonical done Task
```

Do not copy private source/runtime files into the export.

For blocked/partial results, keep the same root document contract where evidence exists and truthfully mark absent sections;
do not export private bytes.

# 24. success ceiling

```text
0036 exact S1 attempt:
EXECUTION_FAILED / v2

0036 exact WorkRun:
FAILED / v3

historical active workspace:
QUARANTINED / PRESERVED

provider/tool execution:
NOT_PERFORMED

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
