# 작업지시서: P2-3 private S1 invalid-history disposition runtime final acceptance Git persistence

## meta

- task_id: `20260913_1755_aiscc-p2-3-private-s1-invalid-history-disposition-runtime-final-acceptance-git-persistence-1`
- created_at: `2026-09-13T17:55:19+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `FINAL_ACCEPTANCE_PERSISTENCE / STATE_RECONCILIATION`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `d04f6a322f3a3ea49778314e4005b5878b20f121`
- required_parent: `7e2ea251f88ca07c6fd1bde38f73956f8885adbe`
- required_grandparent: `86288febf1cbd94bbb0235cfc680bf6c6c8f7772`
- accepted_result_zip_sha256: `c0590e0891a435b14b22b19ddc4206cac3441ef65f0e7559e2a8413133557783`
- source_test_write_authorized: `No`
- Docker_DB_private_runtime_authorized: `No`
- test_execution_authorized: `No`
- Git_commit_authorized: `Yes / exact two commits`
- push_authorized: `No`

# 0. purpose

Persist the Browser-accepted 1737 runtime result and reconcile canonical state.

Accepted runtime result:

```text
0036 ExecutionAttempt:
EXECUTION_FAILED/v2

0036 WorkRun:
FAILED/v3

historical workspace:
QUARANTINED / fingerprint preserved

provider/tool operations:
0

runtime evidence/Judgment:
0

new run/attempt:
0
```

This Task performs no runtime work.

# 1. Python / repository

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

If Python is needed for bounded artifact/hash work, use only:

```text
<repository-root>\.venv\Scripts\python.exe
```

Do not discover Python through PATH.

# 2. baseline

Require:

```text
branch main
HEAD d04f6a322f3a3ea49778314e4005b5878b20f121
HEAD^ 7e2ea251f88ca07c6fd1bde38f73956f8885adbe
HEAD^^ 86288febf1cbd94bbb0235cfc680bf6c6c8f7772
index empty
tracked clean
Git-visible untracked exactly 6
```

The six exact untracked predecessor artifacts are:

- `.aiassistant/records/aiscc/cycles/20260913_1707_aiscc-p2-3-private-s1-dedicated-builder-disposition-execution-entry-1.cycle.md`  `43cca097669d7a39390c2fa57b5f82e23aff70702fa2925de6182504f4f82268`
- `.aiassistant/reports/aiscc/20260913_1707_aiscc-p2-3-private-s1-dedicated-builder-disposition-execution-authorization-judgment-1.md`  `b089a17f48e40ae8ffd2b12049fe8170520d8f8242d22b7a51043ae0730c4f2e`
- `.aiassistant/tasks/done/20260913_1707_aiscc-p2-3-private-s1-invalid-history-disposition-dedicated-builder-execution-retry-1.md`  `448b56682c4509a03a8a5593089ac6b19c6469a1ec0b67f22948513c73feb3f3`
- `.aiassistant/records/aiscc/cycles/20260913_1737_aiscc-p2-3-private-s1-workspace-byte-gate-correction-retry-entry-1.cycle.md`  `fb276da72c948a2ad0d118f459c42bd4e537e7198ac58392cd040066ecc3cb98`
- `.aiassistant/reports/aiscc/20260913_1737_aiscc-p2-3-private-s1-workspace-byte-gate-command-center-defect-judgment-1.md`  `b36e6016b6ca265b9132233cf5b131c03d8a481c9ab0e3f084e3b9b7ed5ab482`
- `.aiassistant/tasks/done/20260913_1737_aiscc-p2-3-private-s1-invalid-history-disposition-workspace-byte-gate-corrected-retry-1.md`  `8588e1bf63e19e1a63d4682a024fe8ce3324defdc7889116522110879254c2a2`

Current canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `05029cccdc9d20efd351fb603c681d30d5aa2b7f8a13617499f76318553ec337`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `8e5a89f622ede3d9ed16eaaa77ab8699ff9f0103c50b1a92fc528d4afb0d657c`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `6f86e6509a194e92235e14db7bdee70bae3f73c8312f868771fbf76c51f7c412`

Preserve non-owned legacy active Task:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

The legacy Task remains ignored and is not part of Git-visible untracked inventory.

After current Cycle/Judgment placement while current Task is active/ignored:

```text
Git-visible untracked exactly 8
```

Any mismatch → STOP before staging.

# 3. absolute prohibitions

Do not:

```text
access Docker
access PostgreSQL
access private runtime root
read private secret
run tests
modify source/test/config
modify runtime state
run disposition again
create fresh S1
push
reset
restore
checkout
stash
clean
amend
move/delete legacy 1400 active Task
```

# 4. Commit A

Stage exactly 8 paths:

```text
1707 Cycle
1707 Judgment
1707 done Task
1737 Cycle
1737 Judgment
1737 done Task
current 20260913_1755 Cycle
current 20260913_1755 Judgment
```

Exact current paths:

```text
.aiassistant/records/aiscc/cycles/20260913_1755_aiscc-p2-3-private-s1-invalid-history-disposition-runtime-final-acceptance-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1755_aiscc-p2-3-private-s1-invalid-history-disposition-runtime-final-acceptance-judgment-1.md
```

Do not stage current active Task in Commit A.

Commit message exactly:

```text
docs(aiscc): persist private S1 invalid-history disposition
```

Require Commit A parent:

```text
d04f6a322f3a3ea49778314e4005b5878b20f121
```

Require Commit A changed paths exactly 8.

# 5. canonical state reconciliation

After Commit A, modify exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

## CURRENT_STATE_SUMMARY minimum semantic result

Record:

```text
P2-3:
IN_PROGRESS

invalid-history disposition runtime:
FINAL_ADMITTED / PERSISTED

0036 WorkRun:
FAILED/v3

0036 ExecutionAttempt:
EXECUTION_FAILED/v2

0036 historical workspace:
QUARANTINED / CONTENT_IDENTITY_PRESERVED

accepted result ZIP:
c0590e0891a435b14b22b19ddc4206cac3441ef65f0e7559e2a8413133557783

provider/tool execution:
NONE

runtime evidence/Judgment:
NONE

fresh S1 normal execution:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED
```

Record actual Commit A after it exists.

Do not record future Commit B before it exists.

## DECISION_REGISTER

Append/update one bounded decision:

```text
decision_id:
AISCC-P2-3-S1-INVALID-HISTORY-DISPOSITION-RUNTIME-V1

status:
FINAL_ADMITTED / PERSISTED
```

Record:

```text
accepted result SHA
actual Commit A
0036 terminal WorkRun/attempt state
quarantine/content-identity preservation
zero provider/evidence/Judgment/new-lineage facts
```

State explicitly that the stranded 0036 lineage is closed and must not be reused for normal S1.

## NEXT_ACTIONS

Immediate next action must be:

```text
phase:
P2-3

work_type:
FRESH_S1_NORMAL_PRODUCTION_PATH_EXECUTION

title:
P2-3 fresh S1 normal production-path execution

status:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED
```

Minimum entry conditions:

```text
new WorkRun and new attempt identities only
0036 lineage is terminal and forbidden for reuse
exact retained private environment revalidated before execution
source-owned normal production path only
S1 expected terminal semantic = ACCEPTED
```

Do not authorize actual fresh S1 execution in this persistence Task.

# 6. Commit B

Move current Task:

```text
.aiassistant/tasks/active/20260913_1755_aiscc-p2-3-private-s1-invalid-history-disposition-runtime-final-acceptance-git-persistence-1.md
```

to:

```text
.aiassistant/tasks/done/20260913_1755_aiscc-p2-3-private-s1-invalid-history-disposition-runtime-final-acceptance-git-persistence-1.md
```

byte-identically.

Stage exactly 4 paths:

```text
CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md
current done Task
```

Commit message exactly:

```text
docs(aiscc): reconcile private S1 disposition state
```

Require Commit B parent = actual Commit A.

Require Commit B changed paths exactly 4.

# 7. final Git state

Require graph:

```text
d04f6a322f3a3ea49778314e4005b5878b20f121
→ Commit A
→ Commit B
```

Final:

```text
branch main
HEAD = Commit B
index empty
tracked clean
Git-visible untracked none
legacy 1400 active exact / ignored / non-owned
```

No push.

# 8. contract review

Require exactly 30 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PRE_DELIVERY_UNTRACKED_6_EXACT
PREDECESSOR_1707_1737_HASHES_EXACT
CURRENT_STATE_HASHES_EXACT
LEGACY_1400_ACTIVE_EXACT
ACCEPTED_RESULT_SHA_EXACT
NO_PRIVATE_RUNTIME_ACCESS
NO_SOURCE_TEST_MODIFICATION
NO_TEST_EXECUTION
COMMIT_A_STAGE_SET_EXACT_8
COMMIT_A_PARENT_EXACT
COMMIT_A_MESSAGE_EXACT
COMMIT_A_CHANGED_PATHS_EXACT_8
STATE_SUMMARY_RECONCILED
DECISION_REGISTER_RECONCILED
NEXT_ACTIONS_RECONCILED
FRESH_S1_NEXT_ACTION_EXACT
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
COMMIT_B_STAGE_SET_EXACT_4
COMMIT_B_PARENT_COMMIT_A
COMMIT_B_MESSAGE_EXACT
COMMIT_B_CHANGED_PATHS_EXACT_4
FINAL_GRAPH_OLD_A_B_EXACT
FINAL_INDEX_EMPTY
FINAL_TRACKED_CLEAN
FINAL_UNTRACKED_NONE
FINAL_LEGACY_1400_ACTIVE_PRESERVED
NO_PUSH
EXPORT_INTEGRITY_PASS
```

Success:

```text
30 / 30 PASS
```

# 9. export

Root documents exactly 10:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
BASELINE_HASH_VERIFICATION.md
COMMIT_A_PATHS.md
STATE_RECONCILIATION_VERIFICATION.md
COMMIT_B_PATHS.md
GIT_PERSISTENCE_VERIFICATION.md
CONTRACT_REVIEW.md
```

Include project-relative byte-preserving copies of every Commit A and Commit B path.

Unique project-relative copied paths:

```text
8 Commit A paths
+ 4 Commit B paths
= 12
```

No overlap between Commit A and Commit B path sets.

Success export:

```text
22 total members
21 non-self manifest rows
one top-level
CRC PASS
TASK.md == canonical done Task
manifest SHA/size exact
```

# 10. success ceiling

```text
invalid-history disposition runtime:
FINAL_ADMITTED / PERSISTED

0036:
FAILED / QUARANTINED / CLOSED_FOR_REUSE

canonical state:
RECONCILED

fresh S1 normal execution:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

P2-3:
IN_PROGRESS
```
