# 작업지시서: P2-3 private S1 invalid-history disposition workspace-byte-gate corrected retry

## meta

- task_id: `20260913_1737_aiscc-p2-3-private-s1-invalid-history-disposition-workspace-byte-gate-corrected-retry-1`
- created_at: `2026-09-13T17:37:44+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PRIVATE_S1_INVALID_HISTORY_DISPOSITION_EXECUTION_RETRY`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `d04f6a322f3a3ea49778314e4005b5878b20f121`
- required_parent: `7e2ea251f88ca07c6fd1bde38f73956f8885adbe`
- required_grandparent: `86288febf1cbd94bbb0235cfc680bf6c6c8f7772`
- predecessor_result_zip_sha256: `b43bc0f17eb60e9c7321af5c8f1e23cf1dd65d57f5ba18cb777957d5e6fd8d0d`
- private_runtime_read_authorized: `Yes / exact retained resources`
- private_runtime_mutation_authorized: `Conditional / one corrected dedicated disposition`
- source_test_state_write_authorized: `No`
- new_execution_authorized: `No`
- new_run_attempt_authorized: `No`
- success_ceiling: `PRIVATE_S1_INVALID_HISTORY_DISPOSED / BROWSER_REVIEW_PENDING`

# 0. Browser correction authority

1707 stopped correctly before mutation because the issued Task required:

```text
workspace total bytes == 2320
```

That exact-byte predicate was a Command Center defect.

Persisted `StockroomRestartSafetySettlement` computes the authoritative restart fingerprint from an inventory containing, for every file:

```text
relative path
filesystem identity
kind
bytes
sha256
```

Therefore exact fingerprint equality is a stronger source-owned content-identity check.

Historical/current accepted fingerprint:

```text
18433a8d92affe915d01e3bb1265b387a07dc6478e09c92306854908ab396068
```

Do **not** require:

```text
total workspace bytes == 2320
```

Do **not** replace it with:

```text
total workspace bytes == 26727
```

The aggregate byte total may be reported for diagnostics only. It is not a mutation gate in this retry.

# 1. exact subject

```text
run_id:
aiscc-p2-3-private-s1-normal-v1-run

attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1

requester_identity:
aiscc-owner-operator
```

Expected durable state before mutation:

```text
WorkRun RUNNING/v2
ExecutionAttempt NOT_STARTED/v1
attempt causal READY/v1
execution operations 0
execution outputs/submission 0
EXECUTION_STARTED 0
EXECUTION_ABORTED_INVALID_HISTORY 0
runtime evidence 0
Judgment 0
```

# 2. transport and Python

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Python is not an independently authored absolute path.

Use exactly:

```text
<repository-root>\.venv\Scripts\python.exe
```

where `<repository-root>` is the exact repository above.

Require that exact file exists.

Forbidden:

```text
python
py
WindowsApps alias
PATH Python discovery
repository-external Python/venv discovery
```

If the repository-local fixed relative executable does not exist, STOP before private runtime access.

Docker executable:

```text
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

No Docker PATH discovery.

# 3. repository bootstrap

Before delivery require:

```text
branch main
HEAD d04f6a322f3a3ea49778314e4005b5878b20f121
HEAD^ 7e2ea251f88ca07c6fd1bde38f73956f8885adbe
HEAD^^ 86288febf1cbd94bbb0235cfc680bf6c6c8f7772
index empty
tracked clean
Git-visible untracked exactly 3
```

Those three are the 1707 predecessor Cycle/Judgment/done Task:

```text
.aiassistant/records/aiscc/cycles/20260913_1707_aiscc-p2-3-private-s1-dedicated-builder-disposition-execution-entry-1.cycle.md
SHA-256 43cca097669d7a39390c2fa57b5f82e23aff70702fa2925de6182504f4f82268

.aiassistant/reports/aiscc/20260913_1707_aiscc-p2-3-private-s1-dedicated-builder-disposition-execution-authorization-judgment-1.md
SHA-256 b089a17f48e40ae8ffd2b12049fe8170520d8f8242d22b7a51043ae0730c4f2e

.aiassistant/tasks/done/20260913_1707_aiscc-p2-3-private-s1-invalid-history-disposition-dedicated-builder-execution-retry-1.md
SHA-256 448b56682c4509a03a8a5593089ac6b19c6469a1ec0b67f22948513c73feb3f3
```

Current state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `05029cccdc9d20efd351fb603c681d30d5aa2b7f8a13617499f76318553ec337`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `8e5a89f622ede3d9ed16eaaa77ab8699ff9f0103c50b1a92fc528d4afb0d657c`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `6f86e6509a194e92235e14db7bdee70bae3f73c8312f868771fbf76c51f7c412`

Persisted source hashes:

- `src/aiscc/runtime/stockroom_workspace.py`  `1b8366b5c5a6e9054dbd65ef36cd09808074c88ccf6c7ad060a9a76a488efaab`
- `src/aiscc/scenarios/stockroom_production.py`  `c41baca3f7cbeaaa18511dd6e94dd5dd5e65d2b282968703f2a4854d86e1b2f4`
- `src/aiscc/persistence/repository.py`  `57dac018f6505468d62588761825025776d07384947424dad37b63f9f35e5e54`

Preserve non-owned legacy active Task:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Do not require active-directory exclusivity.

After current Cycle/Judgment placement while current Task is active/ignored:

```text
Git-visible untracked exactly 5
```

# 4. retained environment authority

Reconstruct the private runtime root only from exact retained PostgreSQL container inspect:

```text
container:
aiscc-p2-3-private-postgres-v1

container ID:
0b50ac47a79e05ac9b88a8f679d04ddc39f729bf1a8e099d149c4c5570b5999c

PostgreSQL image:
sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94

volume:
aiscc-p2-3-private-postgres-data-v1

endpoint:
127.0.0.1:55432

database / role:
aiscc_private_capture
```

Secret mount must be exactly one:

```text
Destination = /run/secrets/postgres_password
Type = bind
RW = false
```

Use the previously accepted deterministic Docker Desktop Source → native-path reverse mapping and fixed child:

```text
aiscc-p2-3-private-runtime-v1
```

No path search.

Require private boundary no-reparse, protected ACL, allowed-principal boundary, and no repository/Downloads/report-target overlap.

Never export private absolute paths or secret values.

# 5. DB / image preflight

Connect using the exact retained secret only after private-value denylist setup.

Require:

```text
migration head:
20260901_0008
```

Require Stockroom image:

```text
sha256:c51ad05852b58a3b4fd275ee88d183551e745d79ac8239e3da3b98372fe0bb9e
```

Require no running Stockroom transient.

# 6. Phase A durable-state preflight

Require exact subject:

```text
WorkRun:
RUNNING/v2

attempt:
NOT_STARTED/v1

creation/causal:
READY/v1
```

Require exact run/attempt/task-contract/runtime-mode binding.

Require:

```text
execution operations 0
execution outputs/submission 0
EXECUTION_STARTED events 0
EXECUTION_ABORTED_INVALID_HISTORY events 0
SYSTEM_RUNTIME_OBSERVATION evidence 0
Judgments 0
later/competing attempt none
```

Mismatch → STOP_PRESERVE.

# 7. corrected workspace authority

Construct the persisted `StockroomRestartSafetySettlement` against the exact derived private runtime root and call its source-owned `inspect(run_id, attempt_id)`.

Require:

```text
exists:
true

objects:
20

files:
14

inventory fingerprint:
18433a8d92affe915d01e3bb1265b387a07dc6478e09c92306854908ab396068

safe regular directory:
PASS

symlink/reparse/hardlink/special-object violation:
none

matching quarantine entries:
0
```

Important:

```text
NO exact aggregate byte-total equality predicate exists in this Task.
```

It is permitted to report an observed aggregate byte total as diagnostic evidence only.

The mutation authority is the exact source-owned `RestartWorkspaceInspection` identity plus the exact fingerprint above, not an independently invented aggregate byte metric.

Mismatch → STOP_PRESERVE.

# 8. stability read

Repeat DB authority/counts after workspace inspection.

Require exact equality with section 6.

# 9. dedicated builder

Call exactly once:

```text
service = await build_stockroom_invalid_history_disposition(
    session_factory=factory,
    repository_root=repository_root,
    private_runtime_root=private_runtime_root,
    downloads_root=downloads_root,
    requester_identity="aiscc-owner-operator",
)
```

Full production builder is forbidden.

Require constructor:

```text
no workspace mutation
no provider/tool stack
no evidence/Judgment stack
no authority-registration delta
```

# 10. authorize

Supply exactly:

```text
aiscc-accepted-runtime-evidence:v1:0036:sha256:041285052e8fad97636231be69775e0dd7003b3d1b1683b64200cdc931eb0ac5
aiscc-accepted-disposition-contract:v1:1242:sha256:b1dc8f91d1ba01c0198953fad70ace3d3c45276fe279d35c50521f2ad02b1381
```

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

Require the sealed request to bind the exact source-owned workspace inspection fingerprint:

```text
18433a8d92affe915d01e3bb1265b387a07dc6478e09c92306854908ab396068
```

Failure → STOP_PRESERVE, dispose 0.

# 11. final pre-mutation recheck

Immediately before `dispose` re-read:

```text
DB state/counts
source-owned workspace inspection
Stockroom running-transient state
```

Require exact equality with the authorized request/current Phase A state.

# 12. disposition

Only then call:

```text
await service.dispose(request)
```

Maximum one call.

No automatic retry after exception.

Never call repository abort or transition APIs directly.

# 13. expected terminal state

Require:

```text
ExecutionAttempt:
EXECUTION_FAILED/v2

attempt causal:
RUNNING/v2

EXECUTION_ABORTED_INVALID_HISTORY:
exactly 1

reason:
INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START
```

WorkRun:

```text
FAILED/v3
```

with authentic:

```text
RUNNING/v2 → FAILED/v3
G_FAILURE_TERMINAL
```

Workspace:

```text
original active target absent
one exact quarantine target
fingerprint 18433a8d92affe915d01e3bb1265b387a07dc6478e09c92306854908ab396068
source-owned post-move fingerprint equality PASS
```

The quarantine fingerprint equality is the byte/content-preservation proof. Do not add an unrelated aggregate-total-byte hard gate.

# 14. post verification

Require zero:

```text
EXECUTION_STARTED
execution operations
execution outputs/submission
runtime evidence
Judgment
new WorkRuns
new attempts
Stockroom container launches
```

Retain PostgreSQL and quarantine.

# 15. exception semantics

If `dispose` raises:

```text
no second dispose
no cleanup
no retry
```

Read-only classify P0/P1/P2/P3 and STOP_PRESERVE.

# 16. Git boundary

No tracked file mutation.

Before Task move:

```text
HEAD d04f6a322f3a3ea49778314e4005b5878b20f121
index empty
tracked clean
Git-visible untracked exactly 5
legacy 1400 exact/preserved
```

Move current Task active→done byte-identically.

Final:

```text
Git-visible untracked exactly 6:
1707 Cycle
1707 Judgment
1707 done Task
current Cycle
current Judgment
current done Task
```

Legacy 1400 remains ignored/non-owned and does not count as Git-visible untracked.

No commit/push.

# 17. contract review

Require exactly 78 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
CURRENT_STATE_HASHES_EXACT
PERSISTED_SOURCE_HASHES_EXACT
PREDECESSOR_1707_TRIPLE_EXACT
PREDECESSOR_1707_RESULT_SHA_EXACT
PYTHON_REPOSITORY_VENV_EXACT
DOCKER_EXECUTABLE_EXACT
PRE_DELIVERY_UNTRACKED_3_EXACT
LEGACY_1400_ACTIVE_EXACT
PRIVATE_POSTGRES_CONTAINER_IDENTITY_EXACT
PRIVATE_POSTGRES_IMAGE_EXACT
PRIVATE_POSTGRES_VOLUME_EXACT
PRIVATE_POSTGRES_ENDPOINT_EXACT
PRIVATE_SECRET_BIND_DESTINATION_RO_EXACT
PRIVATE_RUNTIME_ROOT_DERIVATION_EXACT
PRIVATE_RUNTIME_ROOT_NO_REPARSE_BOUNDARY
PRIVATE_RUNTIME_ROOT_PRIVATE_ACL_EXACT
PRIVATE_RUNTIME_ROOT_NO_REPO_DOWNLOAD_OVERLAP
PRIVATE_DB_MIGRATION_HEAD_EXACT
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
PREFLIGHT_WORKSPACE_FINGERPRINT_EXACT
PREFLIGHT_WORKSPACE_SAFE_INVENTORY
PREFLIGHT_NO_EXISTING_QUARANTINE_AMBIGUITY
NO_EXACT_WORKSPACE_TOTAL_BYTE_GATE
PREFLIGHT_DOUBLE_READ_DB_STABLE
DEDICATED_BUILDER_SINGLE_CALL_EXACT
DEDICATED_BUILDER_REQUESTER_EXACT
DEDICATED_BUILDER_NO_REGISTRATION_DELTA
DEDICATED_BUILDER_NO_EXECUTION_STACK
PROVENANCE_REFS_EXACT
AUTHORIZE_SINGLE_CALL_EXACT
AUTHORIZE_EXPECTED_STATE_VERSION_2
AUTHORIZE_EXPECTED_EXECUTION_VERSION_1
AUTHORIZE_WORKSPACE_FINGERPRINT_EXACT
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
QUARANTINE_CONTENT_IDENTITY_PRESERVED
NO_PROVIDER_OPERATION_CREATED
NO_EXECUTION_OUTPUT_SUBMISSION_CREATED
NO_RUNTIME_EVIDENCE_CREATED
NO_JUDGMENT_CREATED
NO_NEW_RUN_CREATED
NO_NEW_ATTEMPT_CREATED
NO_STOCKROOM_CONTAINER_LAUNCHED
NO_SOURCE_TEST_STATE_GIT_MUTATION
NO_AUTOMATIC_DISPOSE_RETRY
PRIVATE_VALUE_EXPORT_SCAN_PASS
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_UNTRACKED_6_EXACT
FINAL_LEGACY_1400_ACTIVE_PRESERVED
EXPORT_INTEGRITY_PASS
```

Successful disposition:

```text
78 / 78 PASS
```

Blocked result must not relabel unobserved postconditions as PASS.

# 18. export

Root documents exactly 14:

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
one top-level
CRC PASS
TASK.md == current done Task
```

Do not export predecessor 1707 artifacts again.

# 19. success ceiling

```text
0036 attempt:
EXECUTION_FAILED/v2

0036 WorkRun:
FAILED/v3

historical workspace:
QUARANTINED / content identity preserved

provider/tool execution:
NONE

runtime evidence/Judgment:
NONE

new run/attempt:
NONE

P2-3:
IN_PROGRESS

Browser runtime acceptance:
PENDING
```
