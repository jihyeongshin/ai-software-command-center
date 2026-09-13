# 작업지시서: P2-3 S1 execution-start candidate final acceptance Git persistence

## meta

- task_id: `20260913_1102_aiscc-p2-3-s1-execution-start-candidate-final-acceptance-git-persistence-1`
- created_at: `2026-09-13T11:02:29+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `FINAL_ACCEPTANCE_PERSISTENCE / STATE_RECONCILIATION`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- required_parent: `35cee94a92d1f12801576ef48038196922687f42`
- required_grandparent: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- runtime_recovery_authorized: `No`
- private_runtime_access_authorized: `No`
- success_ceiling: `EXECUTION_START_CORRECTION_FINAL_ADMITTED_PERSISTED / RECOVERY_DESIGN_ENTRY_READY`

# 0. purpose

Persist the Browser-final-accepted execution-start lifecycle correction and its complete 0012→1045 governance lineage.

Then reconcile canonical state.

This Task is Git/governance persistence only.

Do not access or mutate the retained private S1 runtime.

# 1. Python / transport

Use only:
```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Forbidden: `python`, `py`, WindowsApps alias, PATH Python discovery.

Verify inbound ZIP/hash and exactly three flat safe members.

Place current Task first:
```text
.aiassistant/tasks/active/20260913_1102_aiscc-p2-3-s1-execution-start-candidate-final-acceptance-git-persistence-1.md
```

Then place:
```text
.aiassistant/records/aiscc/cycles/20260913_1102_aiscc-p2-3-s1-execution-start-candidate-final-acceptance-persistence-entry-1.cycle.md
SHA-256 5575c67fc818d5f8637cd99c357aca3f19742b6a38bad7b37817152c31f45e41

.aiassistant/reports/aiscc/20260913_1102_aiscc-p2-3-s1-execution-start-candidate-final-acceptance-judgment-1.md
SHA-256 65de3221e3d852b1892aa0587308d812eca7b62b4ef9dcd65f4448bf6e2650ac
```

Bootstrap mismatch:
```text
STOP
no Git write
no state mutation
no source mutation
no runtime access
```

# 2. repository baseline

Require:
```text
branch main
HEAD 6cc4f988f56f5cbf32e57f4b5e9a52a180044c36
HEAD^ 35cee94a92d1f12801576ef48038196922687f42
HEAD^^ ee623c995cf1c24b4a362834f2d6d1fdf71a30cd
index empty
```

Canonical state hashes:
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `02b7a77d3f29d7ee3878157470020ab83b377ba0343867ab81ec6e82d1a9190b`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `9ca1b1a24f3f73c2f81d3342442cf0462b58fecdba2dbccc33509b0d4039ab71`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `7315a943ad4ed82757f4398d9613f3a6f773755f3496fa1e8fa816123422ea84`

Before current delivery Git-visible untracked exactly 24:
- `.aiassistant/tasks/done/20260913_0012_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-retry-1.md`  `310bcfab97f13c7606bb09fc773ec6c659102e63b6ba1d33fa38b18c7cfeb034`
- `.aiassistant/records/aiscc/cycles/20260913_0012_aiscc-p2-3-private-s1-source-correction-persisted-execution-entry-1.cycle.md`  `ff0ca7f1752fd3a49306b660b1823b57b194a60b1d58c2341867e9c9b75dc702`
- `.aiassistant/reports/aiscc/20260913_0012_aiscc-p2-3-private-s1-source-correction-persisted-execution-authorization-judgment-1.md`  `568268a48fcda0145b549f9b26a5baf4287b8fb7f4937c3bfd9b2db60b5836a8`
- `.aiassistant/tasks/done/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-semantic-datetime-retry-1.md`  `0226353dba304ac01e9add745053502618001f6eecd833a92e9fd2b45d844f4b`
- `.aiassistant/records/aiscc/cycles/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-harness-corrected-retry-entry-1.cycle.md`  `8619cd9bfc9c3476129199c1213366a1bd26127c2f64d2156bddada7a3d97bfa`
- `.aiassistant/reports/aiscc/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-harness-error-retry-judgment-1.md`  `82550b3a3ed60678b1b252fe483f48003757870427ae8c1ecbefd4c35d1f0011`
- `.aiassistant/tasks/done/20260913_0115_aiscc-p2-3-s1-execution-lifecycle-desync-source-ownership-diagnosis-1.md`  `2b1443f6d760a63cc6a43b6fde4bdd26e9dc957f882216ca7a5a685068e2f00a`
- `.aiassistant/records/aiscc/cycles/20260913_0115_aiscc-p2-3-s1-execution-lifecycle-desync-diagnosis-entry-1.cycle.md`  `8b9f180f0e9a0d4ccf505ac2c3de920a5be3c9a088f163ae80066c1d6145b428`
- `.aiassistant/reports/aiscc/20260913_0115_aiscc-p2-3-s1-execution-not-started-runtime-hold-judgment-1.md`  `f462080446ad883fea933b48677a7b871dfcd054b8c344c410950db02af3772d`
- `.aiassistant/tasks/done/20260913_0138_aiscc-p2-3-s1-execution-start-lifecycle-source-rework-1.md`  `17be2065f75e4262cfdf2c7678d2e5463e18f69fe38a4762d737f41667a27fb7`
- `.aiassistant/records/aiscc/cycles/20260913_0138_aiscc-p2-3-s1-execution-start-lifecycle-source-rework-entry-1.cycle.md`  `5c7bfc64071e4e9feaf7a397c3377a6611986d190e7bcd74627ef8b5fdcb29db`
- `.aiassistant/reports/aiscc/20260913_0138_aiscc-p2-3-s1-execution-lifecycle-owner-confirmed-rework-judgment-1.md`  `94b8347a340c12b7ecce6f71b3b7017f46a2dddf7cbcd36d577ad27cb8c39d73`
- `.aiassistant/tasks/done/20260913_0206_aiscc-p2-3-s1-execution-start-durable-postgresql-verification-1.md`  `0468cc058c46f8a8c8d3c45b6f1290513e7c8ca37bdbde4201af685dba98d689`
- `.aiassistant/records/aiscc/cycles/20260913_0206_aiscc-p2-3-s1-execution-start-durable-verification-entry-1.cycle.md`  `fafebcfa2f981f00af4d40d0b99c0eab0030e372f9c559ea0aac9ca285aec488`
- `.aiassistant/reports/aiscc/20260913_0206_aiscc-p2-3-s1-execution-start-source-candidate-durable-proof-required-judgment-1.md`  `3c3f4d5031ced700a2ac679cdf2380384522884b2c1cf5bef10f01bea3773126`
- `.aiassistant/tasks/done/20260913_0235_aiscc-p2-3-s1-durable-scenario-fixture-authority-correction-and-verification-1.md`  `0a5096812127cd1a043fb83870b422f050190ac285d69ae6d80424078a1964e0`
- `.aiassistant/records/aiscc/cycles/20260913_0235_aiscc-p2-3-s1-durable-scenario-fixture-correction-verification-entry-1.cycle.md`  `ad3e00ea8c5da679441e141c393f6cf4b07378ffebd4dcd2698ed32e0bc54587`
- `.aiassistant/reports/aiscc/20260913_0235_aiscc-p2-3-s1-durable-scenario-fixture-authority-defect-judgment-1.md`  `061a414f56b80bd0b005f65c3c31e972d96f9f494355c53de6f2540cde541807`
- `.aiassistant/tasks/done/20260913_0253_aiscc-p2-3-provider-persistence-failure-ownership-diagnosis-1.md`  `34aaabce811d6d5a6f6baf37351dc5323919c2ec26d954ad26cbb05cef8435c9`
- `.aiassistant/records/aiscc/cycles/20260913_0253_aiscc-p2-3-provider-persistence-failure-diagnosis-entry-1.cycle.md`  `0419dbc78fb6149012653caefeab885324617307c5161e13bbf6d4df064bf69d`
- `.aiassistant/reports/aiscc/20260913_0253_aiscc-p2-3-provider-persistence-regression-hold-diagnosis-judgment-1.md`  `169865f4095e2cd242d7b502eb5762f07d838727eb538a276e5bf0fc71c70555`
- `.aiassistant/tasks/done/20260913_1045_aiscc-p2-3-provider-persistence-complete-capture-conditional-fixture-rework-1.md`  `21496bee7ace5e2cdeb4cf79c4d09dc1605c26bb225ce80d251deaeaec98b7e2`
- `.aiassistant/records/aiscc/cycles/20260913_1045_aiscc-p2-3-provider-persistence-complete-capture-entry-1.cycle.md`  `0d670319bcb02ee23269e6bb0fa9c259fb864f506081cf23b6d82711705253bc`
- `.aiassistant/reports/aiscc/20260913_1045_aiscc-p2-3-provider-persistence-incomplete-capture-conditional-rework-judgment-1.md`  `5d3d2dbdbd9f0a183ca6d073216f11a44a2b26aded251c06b34fb3614d4658d1`

Tracked dirty exactly:
- `src/aiscc/scenarios/stockroom_production.py`  `c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `dca16f6ed0de608faa7f06cd4266ad377f140971536e0a82c0e92f679da73b72`
- `tests/integration/providers/test_execution_persistence.py`  `4f0bbcadf3f0cb38f6406becbb9343cda7c2787e9e2cbef3fff60be363c9c74a`

After current Cycle/Judgment placement while Task remains active/ignored:
```text
Git-visible untracked = 26 exact
tracked dirty = 3 exact
index empty
```

Any mismatch → STOP_WITH_REPORT_EXPORT.

# 3. accepted result authority

Browser accepts result ZIP:
```text
50dce7aa4ad298021848a9ac96adf32c5ffacd0fc403a3ae5a7f54273283500e
```

Accepted evidence:
```text
20 members / CRC PASS
manifest 19/19 exact
contract 53/53 PASS
Phase A categories 10 + 1 = 11 exact
provider persistence 23/23 PASS
scenario durable 55/55 PASS
workflow handoff 3/3 PASS
unit 741 passed / 2 skipped / 0 failed
Ruff PASS
py_compile PASS
git diff --check PASS
isolated PostgreSQL removed
retained private S1 untouched
```

Do not rerun tests in this persistence Task.

# 4. Commit A

Authorize exact-path staging only for these 29 paths:

```text
.aiassistant/tasks/done/20260913_0012_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-retry-1.md
.aiassistant/records/aiscc/cycles/20260913_0012_aiscc-p2-3-private-s1-source-correction-persisted-execution-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_0012_aiscc-p2-3-private-s1-source-correction-persisted-execution-authorization-judgment-1.md
.aiassistant/tasks/done/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-semantic-datetime-retry-1.md
.aiassistant/records/aiscc/cycles/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-harness-corrected-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-harness-error-retry-judgment-1.md
.aiassistant/tasks/done/20260913_0115_aiscc-p2-3-s1-execution-lifecycle-desync-source-ownership-diagnosis-1.md
.aiassistant/records/aiscc/cycles/20260913_0115_aiscc-p2-3-s1-execution-lifecycle-desync-diagnosis-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_0115_aiscc-p2-3-s1-execution-not-started-runtime-hold-judgment-1.md
.aiassistant/tasks/done/20260913_0138_aiscc-p2-3-s1-execution-start-lifecycle-source-rework-1.md
.aiassistant/records/aiscc/cycles/20260913_0138_aiscc-p2-3-s1-execution-start-lifecycle-source-rework-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_0138_aiscc-p2-3-s1-execution-lifecycle-owner-confirmed-rework-judgment-1.md
.aiassistant/tasks/done/20260913_0206_aiscc-p2-3-s1-execution-start-durable-postgresql-verification-1.md
.aiassistant/records/aiscc/cycles/20260913_0206_aiscc-p2-3-s1-execution-start-durable-verification-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_0206_aiscc-p2-3-s1-execution-start-source-candidate-durable-proof-required-judgment-1.md
.aiassistant/tasks/done/20260913_0235_aiscc-p2-3-s1-durable-scenario-fixture-authority-correction-and-verification-1.md
.aiassistant/records/aiscc/cycles/20260913_0235_aiscc-p2-3-s1-durable-scenario-fixture-correction-verification-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_0235_aiscc-p2-3-s1-durable-scenario-fixture-authority-defect-judgment-1.md
.aiassistant/tasks/done/20260913_0253_aiscc-p2-3-provider-persistence-failure-ownership-diagnosis-1.md
.aiassistant/records/aiscc/cycles/20260913_0253_aiscc-p2-3-provider-persistence-failure-diagnosis-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_0253_aiscc-p2-3-provider-persistence-regression-hold-diagnosis-judgment-1.md
.aiassistant/tasks/done/20260913_1045_aiscc-p2-3-provider-persistence-complete-capture-conditional-fixture-rework-1.md
.aiassistant/records/aiscc/cycles/20260913_1045_aiscc-p2-3-provider-persistence-complete-capture-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1045_aiscc-p2-3-provider-persistence-incomplete-capture-conditional-rework-judgment-1.md
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
tests/integration/providers/test_execution_persistence.py
.aiassistant/records/aiscc/cycles/20260913_1102_aiscc-p2-3-s1-execution-start-candidate-final-acceptance-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1102_aiscc-p2-3-s1-execution-start-candidate-final-acceptance-judgment-1.md
```

Require:
```text
staged = 29 exact
candidate source/test = 3 exact
governance/provenance = 26 exact
no extra
```

Commit message:
```text
fix(aiscc): persist S1 execution-start lifecycle correction
```

Require:
```text
Commit A parent = 6cc4f988f56f5cbf32e57f4b5e9a52a180044c36
Commit A created
Commit A changed paths = 29 exact
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

Preserve all prior accepted/persisted history.

Add/update current P2-3 authority to state at minimum:

```text
P2-3:
IN_PROGRESS

S1 producer-provenance source correction:
FINAL_ADMITTED / PERSISTED

S1 execution-start lifecycle correction:
FINAL_ADMITTED / PERSISTED

accepted result ZIP:
50dce7aa4ad298021848a9ac96adf32c5ffacd0fc403a3ae5a7f54273283500e

durable scenario verification:
55 / 55 PASS

provider persistence:
23 / 23 PASS

provider fixture alignment:
FINAL_ADMITTED / PERSISTED

0036 durable S1:
HOLD / PRESERVED

0036 WorkRun:
RUNNING / v2

0036 ExecutionAttempt:
NOT_STARTED

0036 execution operations:
0

0036 runtime evidence:
none

0036 Judgment:
none

runtime recovery:
NOT_AUTHORIZED

next governance state:
RECOVERY_DESIGN_ENTRY_READY
```

Record actual Commit A hash.

Do not embed future Commit B hash into files committed by Commit B.

## 5.2 DECISION_REGISTER

Add exactly one bounded decision entry:

```text
decision_id:
AISCC-P2-3-S1-EXECUTION-START-LIFECYCLE-CORRECTION-V1

decision_status:
FINAL_ADMITTED / PERSISTED
```

Record:
```text
Browser accepted result ZIP:
50dce7aa4ad298021848a9ac96adf32c5ffacd0fc403a3ae5a7f54273283500e

actual Commit A:
<actual>

production correction:
Stockroom READY→RUNNING admitted
→ durable EXECUTION_STARTED on exact prepared attempt
→ authoritative RUNNING/casual-version verification before downstream execution

durable scenario:
55/55 PASS

provider persistence:
23/23 PASS

provider fixture alignment:
resolved_dispatch_context fingerprint + current _issue_capability optional keyword contract

0036 stranded runtime:
preserved, not recovered

next authority:
separate recovery-design/authorization Task
```

Do not rewrite unrelated decisions.

## 5.3 NEXT_ACTIONS

Set immediate P2-3 next action:

```text
phase:
P2-3

work_type:
PRIVATE_S1_RECOVERY_DESIGN

title:
P2-3 stranded S1 RUNNING/NOT_STARTED in-place recovery boundary design

status:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

subject:
existing exact 0036 durable state only

known state:
WorkRun RUNNING/v2
ExecutionAttempt NOT_STARTED
execution_operations 0
runtime evidence none
Judgment none

goal:
determine whether in-place continuation is valid under current contracts and, if valid, define exact safe transition/authorization sequence

forbidden before later authorization:
rerun prepare_capture
new run/attempt ID
delete/reset/repair DB
manual provider/tool execution
runtime-root cleanup
scenario Judgment
```

Do not mark recovery started or authorized.

# 6. current Task lifecycle + Commit B

After state reconciliation, move current Task byte-identically:
```text
.aiassistant/tasks/active/20260913_1102_aiscc-p2-3-s1-execution-start-candidate-final-acceptance-git-persistence-1.md
→
.aiassistant/tasks/done/20260913_1102_aiscc-p2-3-s1-execution-start-candidate-final-acceptance-git-persistence-1.md
```

Authorize exact-path staging only for:
```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/tasks/done/20260913_1102_aiscc-p2-3-s1-execution-start-candidate-final-acceptance-git-persistence-1.md
```

Require:
```text
staged = 4 exact
```

Commit message:
```text
docs(aiscc): reconcile S1 execution-start correction state
```

Require:
```text
Commit B parent = actual Commit A
Commit B created

graph:
6cc4f988f56f5cbf32e57f4b5e9a52a180044c36
→ Commit A
→ Commit B

final index empty
final tracked clean
final Git-visible untracked none
```

No push.

# 7. absolute forbidden actions

```text
git push
git reset
git restore
git checkout
git stash
git clean
git commit --amend

source/test/config edits
test reruns

Docker CLI/API
PostgreSQL connection/query
private password file
private runtime root

prepare_capture
new WorkRun/attempt
existing S1 continuation
provider/tool execution
runtime evidence admission
scenario Judgment
```

# 8. contract review

Require exactly 33 rows:
```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
BASELINE_STATE_HASHES_EXACT
PRE_DELIVERY_UNTRACKED_24_EXACT
POST_DELIVERY_UNTRACKED_26_EXACT
INDEX_EMPTY_PREWRITE
TRACKED_DIRTY3_EXACT
ACCEPTED_CANDIDATE_HASHES_EXACT
CURRENT_ACCEPTANCE_ARTIFACTS_EXACT
COMMIT_A_ALLOWLIST_29_EXACT
COMMIT_A_PARENT_EXACT
COMMIT_A_CREATED
COMMIT_A_PATH_SET_EXACT
COMMIT_A_CANDIDATE3_EXACT
COMMIT_A_GOVERNANCE26_EXACT
THREE_STATE_OWNER_RECONCILIATION_EXACT
EXECUTION_START_ACCEPTANCE_RECORDED
PROVIDER_FIXTURE_ACCEPTANCE_RECORDED
STRANDED_S1_HOLD_RECORDED
NEXT_ACTION_RECOVERY_DESIGN_ONLY
NO_RUNTIME_RECOVERY
NO_PRIVATE_RUNTIME_ACCESS
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
COMMIT_B_ALLOWLIST_4_EXACT
COMMIT_B_PARENT_COMMIT_A
COMMIT_B_CREATED
FINAL_GRAPH_EXACT
FINAL_INDEX_TRACKED_UNTRACKED_CLEAN
NO_SOURCE_TEST_MUTATION
NO_DOCKER_DB_ACCESS
NO_S1_EXECUTION
NO_PUSH
EXPORT_INTEGRITY_PASS
```

Success requires:
```text
33 / 33 PASS
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
43 total members
42 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == canonical done Task
```

# 10. success ceiling

```text
S1 execution-start lifecycle correction:
FINAL_ADMITTED / PERSISTED

provider fixture alignment:
FINAL_ADMITTED / PERSISTED

canonical state:
RECONCILED

0036 durable S1:
HOLD / PRESERVED

runtime recovery:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

S1 execution/recovery:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
