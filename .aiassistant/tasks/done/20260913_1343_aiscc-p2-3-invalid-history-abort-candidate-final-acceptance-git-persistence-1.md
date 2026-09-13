# 작업지시서: P2-3 invalid-history abort candidate final acceptance Git persistence

## meta

- task_id: `20260913_1343_aiscc-p2-3-invalid-history-abort-candidate-final-acceptance-git-persistence-1`
- created_at: `2026-09-13T13:43:21+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `FINAL_ACCEPTANCE_PERSISTENCE / STATE_RECONCILIATION`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `5affe61f02994f219b22ca934b5e0b93bc5e6f60`
- required_parent: `a4eb36611dca8d504610d9e3091950b0f32c20e7`
- required_grandparent: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- accepted_result_zip_sha256: `b1dc8f91d1ba01c0198953fad70ace3d3c45276fe279d35c50521f2ad02b1381`
- private_runtime_access_authorized: `No`
- runtime_disposition_authorized: `No`
- success_ceiling: `INVALID_HISTORY_ABORT_FINAL_ADMITTED_PERSISTED / PRIVATE_DISPOSITION_ENTRY_READY`

# 0. purpose

Persist the Browser-final-accepted invalid-history abort/disposition candidate and its complete 1129→1242 governance lineage.

Then reconcile canonical state.

This Task is Git/governance persistence only.

Do not access or mutate retained private S1 runtime.

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
.aiassistant/tasks/active/20260913_1343_aiscc-p2-3-invalid-history-abort-candidate-final-acceptance-git-persistence-1.md
```

Then place:
```text
.aiassistant/records/aiscc/cycles/20260913_1343_aiscc-p2-3-invalid-history-abort-final-acceptance-persistence-entry-1.cycle.md
SHA-256 738393029df08fe23f14e4df368a021385757fcdd536579f435cd992342acd15

.aiassistant/reports/aiscc/20260913_1343_aiscc-p2-3-invalid-history-abort-candidate-final-acceptance-judgment-1.md
SHA-256 f8c44e10b4cbf4cc90f8b34bf39a74cc53b390d9859260a1464a50c7db625ef5
```

Bootstrap mismatch:
```text
STOP
no Git write
no state mutation
no source/rule/test mutation
no runtime access
```

# 2. repository baseline

Require:
```text
branch main
HEAD 5affe61f02994f219b22ca934b5e0b93bc5e6f60
HEAD^ a4eb36611dca8d504610d9e3091950b0f32c20e7
HEAD^^ 6cc4f988f56f5cbf32e57f4b5e9a52a180044c36
index empty
```

Canonical state hashes:
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `550b7b3ec6659c5ad86558c84902a5319457334432db452405e31a2eb1153164`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `c9496a814cb94a834f53c4dee46032836dfaa4f8490d433a5909c0e46d2e3c3f`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `a6130f00deb41a1cae8c42cb62e7eb57d3457e40775794c6efb725fb604c832e`

Before current delivery Git-visible untracked exactly 12:
- `.aiassistant/tasks/done/20260913_1129_aiscc-p2-3-stranded-s1-in-place-recovery-boundary-design-1.md`  `d01fbfa993c0e37f06a9066f9def2ca1c4af590d372eaa122a6c53dee4e29e36`
- `.aiassistant/records/aiscc/cycles/20260913_1129_aiscc-p2-3-stranded-s1-recovery-design-entry-1.cycle.md`  `02356ec126b9381248ab491b013ad8a74f90abfd8d69a50349ad9f2718dd0b50`
- `.aiassistant/reports/aiscc/20260913_1129_aiscc-p2-3-stranded-s1-recovery-design-authorization-judgment-1.md`  `4ab5b734e9802c975e51a761bd4281b7a9359df7bd140711d7e8cb3e49dd214a`
- `.aiassistant/tasks/done/20260913_1208_aiscc-p2-3-stranded-s1-recovery-boundary-corrected-design-retry-1.md`  `899c1c650acd90fec2b2e99cf4e49ed5c5804539e57713b00fbb3462d2024e4c`
- `.aiassistant/records/aiscc/cycles/20260913_1208_aiscc-p2-3-stranded-s1-recovery-baseline-conflict-corrected-entry-1.cycle.md`  `f87221fb252c6db21f5731f09c58c2393ff4eaf4002d11bba4d8053d8132b9e5`
- `.aiassistant/reports/aiscc/20260913_1208_aiscc-p2-3-stranded-s1-recovery-baseline-conflict-correction-judgment-1.md`  `03c66a81c212c075f5e425accd2001106bc9709ee86c9f2833d3d1f32ef1b075`
- `.aiassistant/tasks/done/20260913_1224_aiscc-p2-3-stranded-s1-invalid-history-disposition-design-1.md`  `3c05de4c825ee3e3b3c6906add1f2d2f95148f2b286c0f98b5d17fef5059b5dc`
- `.aiassistant/records/aiscc/cycles/20260913_1224_aiscc-p2-3-stranded-s1-invalid-history-disposition-entry-1.cycle.md`  `a0d2658398c834550bd89e10d2cc2283422a6a60cdc424fd0fe6808c941e06d3`
- `.aiassistant/reports/aiscc/20260913_1224_aiscc-p2-3-stranded-s1-in-place-continuation-forbidden-judgment-1.md`  `9587af829556be5327a4dabe63a1d46bce638f956689c551f7126d4ac0577717`
- `.aiassistant/tasks/done/20260913_1242_aiscc-p2-3-invalid-history-abort-contract-and-disposition-source-rework-1.md`  `4b36b76aa60e0803d86bd5e375e031839adc2cc3fedf282b8a4edc5f65e6b745`
- `.aiassistant/records/aiscc/cycles/20260913_1242_aiscc-p2-3-invalid-history-abort-contract-rework-entry-1.cycle.md`  `f796bdcda330aa6133e2424951e02b82cbd7399400bd87e0d1e9ffd417455980`
- `.aiassistant/reports/aiscc/20260913_1242_aiscc-p2-3-disposition-forbidden-contract-rework-authorization-judgment-1.md`  `63efbe1860bba000a2b90b9778dcd4c721d61c75e68e61ed9439129841efa59c`

Tracked dirty exactly nine accepted paths:
- `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`  `382433d24959827fc606592e7beb78f34934209fa2f9c34aabdeda1c6e322784`
- `src/aiscc/providers/events.py`  `69b0339a12630eb552ef479a819c78596a2c0094437b4458a30eebb730c18a98`
- `src/aiscc/persistence/repository.py`  `57dac018f6505468d62588761825025776d07384947424dad37b63f9f35e5e54`
- `src/aiscc/scenarios/stockroom_production.py`  `abbe7f81840de7d9525900511f967512c72cf114104128501c681c19fbacd127`
- `src/aiscc/runtime/stockroom_workspace.py`  `1b8366b5c5a6e9054dbd65ef36cd09808074c88ccf6c7ad060a9a76a488efaab`
- `tests/unit/providers/test_operation_protocol.py`  `7160869c0342691574b8c3fb8bb3d8e741afd85ddefed08e8d96af826a263602`
- `tests/integration/providers/test_execution_persistence.py`  `ba0f0a424dc0170c1400755804481e5e584643cac77cd8f539075f18f9ac6c9d`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `0f6c21edec2b70695a3727148e47143559aa2dc65b07058c6a8d59a18ee22fb6`
- `tests/unit/runtime/test_stockroom_workspace.py`  `0dcd21e8f73ae84feb5eceb0a4a9addd7d6c8598455acda46b9559c029b0d706`

After current Cycle/Judgment placement while Task remains active/ignored:
```text
Git-visible untracked = 14 exact
tracked dirty = 9 exact
index empty
```

Any mismatch → STOP_WITH_REPORT_EXPORT.

# 3. accepted result authority

Browser accepts result ZIP:
```text
b1dc8f91d1ba01c0198953fad70ace3d3c45276fe279d35c50521f2ad02b1381
```

Accepted evidence:
```text
26 members / CRC PASS
manifest 25/25 exact
contract 60/60 PASS
provider persistence 24/24 PASS
Stockroom scenario/disposition 56/56 PASS
workflow handoff 3/3 PASS
unit 745 passed / 3 host-conditional skipped
Ruff PASS
py_compile PASS
git diff --check PASS
retained private S1 untouched
```

Do not rerun tests in this persistence Task.

# 4. Commit A

Authorize exact-path staging only for these 23 paths:

```text
.aiassistant/tasks/done/20260913_1129_aiscc-p2-3-stranded-s1-in-place-recovery-boundary-design-1.md
.aiassistant/records/aiscc/cycles/20260913_1129_aiscc-p2-3-stranded-s1-recovery-design-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1129_aiscc-p2-3-stranded-s1-recovery-design-authorization-judgment-1.md
.aiassistant/tasks/done/20260913_1208_aiscc-p2-3-stranded-s1-recovery-boundary-corrected-design-retry-1.md
.aiassistant/records/aiscc/cycles/20260913_1208_aiscc-p2-3-stranded-s1-recovery-baseline-conflict-corrected-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1208_aiscc-p2-3-stranded-s1-recovery-baseline-conflict-correction-judgment-1.md
.aiassistant/tasks/done/20260913_1224_aiscc-p2-3-stranded-s1-invalid-history-disposition-design-1.md
.aiassistant/records/aiscc/cycles/20260913_1224_aiscc-p2-3-stranded-s1-invalid-history-disposition-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1224_aiscc-p2-3-stranded-s1-in-place-continuation-forbidden-judgment-1.md
.aiassistant/tasks/done/20260913_1242_aiscc-p2-3-invalid-history-abort-contract-and-disposition-source-rework-1.md
.aiassistant/records/aiscc/cycles/20260913_1242_aiscc-p2-3-invalid-history-abort-contract-rework-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1242_aiscc-p2-3-disposition-forbidden-contract-rework-authorization-judgment-1.md
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
src/aiscc/providers/events.py
src/aiscc/persistence/repository.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/runtime/stockroom_workspace.py
tests/unit/providers/test_operation_protocol.py
tests/integration/providers/test_execution_persistence.py
tests/integration/scenarios/test_stockroom_capture_runner.py
tests/unit/runtime/test_stockroom_workspace.py
.aiassistant/records/aiscc/cycles/20260913_1343_aiscc-p2-3-invalid-history-abort-final-acceptance-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1343_aiscc-p2-3-invalid-history-abort-candidate-final-acceptance-judgment-1.md
```

Require:
```text
staged = 23 exact
accepted candidate = 9 exact
governance/provenance = 14 exact
no extra
```

Commit message:
```text
fix(aiscc): persist invalid-history disposition contract
```

Require:
```text
Commit A parent = 5affe61f02994f219b22ca934b5e0b93bc5e6f60
Commit A created
Commit A changed paths = 23 exact
```

No amend.

# 5. canonical state reconciliation

Only after Commit A exists, modify exactly:
```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

No other tracked file may change.

## 5.1 CURRENT_STATE_SUMMARY

Preserve prior accepted/persisted history.

Record at minimum:

```text
P2-3:
IN_PROGRESS

S1 execution-start lifecycle correction:
FINAL_ADMITTED / PERSISTED

invalid-history disposition classification:
IN_PLACE_CONTINUATION_FORBIDDEN_BY_CURRENT_CONTRACT

invalid-history abort contract:
FINAL_ADMITTED / PERSISTED

event:
EXECUTION_ABORTED_INVALID_HISTORY

reason:
INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START

source-owned disposition:
FINAL_ADMITTED / PERSISTED

restart-safe workspace quarantine:
FINAL_ADMITTED / PERSISTED

accepted result ZIP:
b1dc8f91d1ba01c0198953fad70ace3d3c45276fe279d35c50521f2ad02b1381

provider persistence:
24 / 24 PASS

Stockroom scenario/disposition:
56 / 56 PASS

0036 durable S1:
HOLD / PRESERVED / NOT YET DISPOSED

private runtime disposition:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED
```

Record actual Commit A hash.

Do not embed future Commit B hash into Commit-B-owned files.

## 5.2 DECISION_REGISTER

Add exactly one bounded decision entry:

```text
decision_id:
AISCC-P2-3-S1-INVALID-HISTORY-ABORT-DISPOSITION-V1

decision_status:
FINAL_ADMITTED / PERSISTED
```

Record:
```text
Browser accepted result ZIP:
b1dc8f91d1ba01c0198953fad70ace3d3c45276fe279d35c50521f2ad02b1381

actual Commit A:
<actual>

in-place continuation:
FORBIDDEN_BY_CURRENT_CONTRACT

new dedicated lifecycle event:
EXECUTION_ABORTED_INVALID_HISTORY

edge:
NOT_STARTED → EXECUTION_FAILED

reason:
INVALID_HISTORY_SIDE_EFFECT_BEFORE_EXECUTION_START

source-owned order:
attempt abort
→ authentic G_FAILURE_TERMINAL
→ WorkRun RUNNING→FAILED
→ restart-safe quarantine

no evidence/Judgment created

post-disposition retry:
new WorkRun lineage only; not authorized here
```

Do not rewrite unrelated decisions.

## 5.3 NEXT_ACTIONS

Set immediate P2-3 next action:

```text
phase:
P2-3

work_type:
PRIVATE_S1_INVALID_HISTORY_DISPOSITION_EXECUTION

title:
P2-3 stranded S1 invalid-history disposition execution

status:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

subject:
existing exact 0036 run/attempt only

expected preflight:
WorkRun RUNNING/v2
ExecutionAttempt NOT_STARTED
execution_operations 0
runtime evidence absent
Judgment absent
exact materialized workspace independently inspectable
no running transient
no later state change

authorized later sequence:
read-only preflight first
→ exact invalid-history disposition only if all preconditions match
→ attempt EXECUTION_FAILED
→ WorkRun FAILED
→ exact workspace quarantine/ABSENT verdict

forbidden before later Browser authorization:
new run/attempt
provider/tool execution
delayed EXECUTION_STARTED
READY→RUNNING replay
DB-direct repair
broad cleanup
evidence/Judgment
```

Do not mark runtime disposition started or authorized.

# 6. current Task + Commit B

After state reconciliation, move current Task byte-identically:
```text
.aiassistant/tasks/active/20260913_1343_aiscc-p2-3-invalid-history-abort-candidate-final-acceptance-git-persistence-1.md
→
.aiassistant/tasks/done/20260913_1343_aiscc-p2-3-invalid-history-abort-candidate-final-acceptance-git-persistence-1.md
```

Authorize exact-path staging only for:
```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/tasks/done/20260913_1343_aiscc-p2-3-invalid-history-abort-candidate-final-acceptance-git-persistence-1.md
```

Require:
```text
staged = 4 exact
```

Commit message:
```text
docs(aiscc): reconcile invalid-history disposition state
```

Require:
```text
Commit B parent = actual Commit A
Commit B created

graph:
5affe61f02994f219b22ca934b5e0b93bc5e6f60
→ Commit A
→ Commit B

final index empty
final tracked clean
final Git-visible untracked none
```

No push.

# 7. forbidden

```text
git push
git reset
git restore
git checkout
git stash
git clean
git commit --amend

source/rule/test/config edits
test reruns

Docker CLI/API
PostgreSQL connection/query
private password file
private runtime root
materialized workspace inspection

attempt abort
WorkRun transition
workspace quarantine
new WorkRun/attempt
provider/tool execution
runtime evidence
Judgment
```

# 8. contract review

Require exactly 34 rows:
```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
BASELINE_STATE_HASHES_EXACT
PRE_DELIVERY_UNTRACKED_12_EXACT
POST_DELIVERY_UNTRACKED_14_EXACT
INDEX_EMPTY_PREWRITE
TRACKED_DIRTY9_EXACT
ACCEPTED_CANDIDATE_HASHES_EXACT
CURRENT_ACCEPTANCE_ARTIFACTS_EXACT
COMMIT_A_ALLOWLIST_23_EXACT
COMMIT_A_PARENT_EXACT
COMMIT_A_CREATED
COMMIT_A_PATH_SET_EXACT
COMMIT_A_CANDIDATE9_EXACT
COMMIT_A_GOVERNANCE14_EXACT
THREE_STATE_OWNER_RECONCILIATION_EXACT
INVALID_HISTORY_ABORT_ACCEPTANCE_RECORDED
DISPOSITION_SOURCE_ACCEPTANCE_RECORDED
QUARANTINE_SETTLEMENT_ACCEPTANCE_RECORDED
STRANDED_S1_HOLD_RECORDED
NEXT_ACTION_PRIVATE_DISPOSITION_EXECUTION_ENTRY_ONLY
NO_PRIVATE_RUNTIME_ACCESS
NO_RUNTIME_DISPOSITION
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
COMMIT_B_ALLOWLIST_4_EXACT
COMMIT_B_PARENT_COMMIT_A
COMMIT_B_CREATED
FINAL_GRAPH_EXACT
FINAL_INDEX_TRACKED_UNTRACKED_CLEAN
NO_SOURCE_TEST_RULE_MUTATION_DURING_PERSISTENCE
NO_DOCKER_DB_ACCESS
NO_S1_MUTATION
NO_PUSH
EXPORT_INTEGRITY_PASS
```

Success requires:
```text
34 / 34 PASS
```

# 9. success export

Root docs exactly 10:
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

Include byte-preserving project-relative copies of all Commit A and Commit B paths.

Expected success export:
```text
37 total members
36 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == canonical done Task
```

# 10. success ceiling

```text
invalid-history abort contract:
FINAL_ADMITTED / PERSISTED

source-owned disposition:
FINAL_ADMITTED / PERSISTED

restart-safe quarantine:
FINAL_ADMITTED / PERSISTED

canonical state:
RECONCILED

0036 durable S1:
HOLD / PRESERVED / NOT YET DISPOSED

private runtime disposition:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

P2-3:
IN_PROGRESS
```
