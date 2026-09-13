# 작업지시서: P2-3 disposition-only composition final acceptance Git persistence

## meta

- task_id: `20260913_1633_aiscc-p2-3-disposition-only-composition-final-acceptance-git-persistence-1`
- created_at: `2026-09-13T16:33:20+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `FINAL_ACCEPTANCE_PERSISTENCE / STATE_RECONCILIATION`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `86288febf1cbd94bbb0235cfc680bf6c6c8f7772`
- required_parent: `4341138dde5fbea487f10a8af256f78c5dcf37f3`
- required_grandparent: `5affe61f02994f219b22ca934b5e0b93bc5e6f60`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- accepted_result_zip_sha256: `620ffa448306c0f6486658cb8807e1887206311c2198be7d100c9f30f59ce4d1`
- private_runtime_access_authorized: `No`
- runtime_disposition_authorized: `No`
- success_ceiling: `DISPOSITION_ONLY_COMPOSITION_FINAL_ADMITTED_PERSISTED / PRIVATE_DISPOSITION_RETRY_ENTRY_READY`

# 0. purpose

Persist the final-accepted disposition-only composition source candidate and complete 1406→1608 governance lineage.

Then reconcile canonical state.

This is Git/governance persistence only.

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

Place current Task first, then current Cycle/Judgment.

Bootstrap mismatch:

```text
STOP
no Git/state/source/runtime mutation
```

# 2. repository baseline

Require:

```text
branch main
HEAD 86288febf1cbd94bbb0235cfc680bf6c6c8f7772
HEAD^ 4341138dde5fbea487f10a8af256f78c5dcf37f3
HEAD^^ 5affe61f02994f219b22ca934b5e0b93bc5e6f60
index empty
```

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `b551c534dcf55a3e5e20c4cb379cf1957ba8f719f1bb6d75c980ce5de7cd6283`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `551d0df4a5ad14a4fd825057f18d95d157b8fefb3a9821d26ef92fc2664ce74a`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `36687e0653375ca3c3ea4daf6393ced5a1856e1c70f5822408002322a964da24`

Tracked dirty exactly two accepted candidate paths:

- `src/aiscc/scenarios/stockroom_production.py`  `c41baca3f7cbeaaa18511dd6e94dd5dd5e65d2b282968703f2a4854d86e1b2f4`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `d46ec32658be849a6aea659d52e675636f6e78263e5ef6d0c65a6f2855a279bd`

Before current delivery Git-visible untracked exactly 18:

- `.aiassistant/tasks/done/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-1.md`  `20d611ac457a9db0a95d331a482123022629fbc80e1c9bc5f307db3ab43115d3`
- `.aiassistant/records/aiscc/cycles/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-entry-1.cycle.md`  `6acf1ab71a82dc16090c14d8b6bf5d4ad4dd46456729ab657afb26d580f86d2e`
- `.aiassistant/reports/aiscc/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-authorization-judgment-1.md`  `c10465e987246d7932a665e2c763c69de7711cba6dafb438e6239e0c02866087`
- `.aiassistant/tasks/done/20260913_1435_aiscc-p2-3-private-s1-invalid-history-disposition-root-authority-retry-1.md`  `291549aa7fb05199ac78d5adb7f8ff610d7d6311e5a4f1c24cd6bfc01d486ac7`
- `.aiassistant/records/aiscc/cycles/20260913_1435_aiscc-p2-3-private-s1-root-authority-reconstructed-disposition-retry-entry-1.cycle.md`  `e944e78cddea422c1f8f586d2eb307bf4ab160c6c80862d645e5c14cebe9e5c2`
- `.aiassistant/reports/aiscc/20260913_1435_aiscc-p2-3-private-s1-root-authority-transport-gap-retry-judgment-1.md`  `bfd93a83bd7c7b688f940e0a27f3e4c3f56bae3edb13492de9d25138a80df9c7`
- `.aiassistant/tasks/done/20260913_1511_aiscc-p2-3-disposition-only-composition-entrypoint-source-rework-1.md`  `241f6c9cad0190457455cdfd1d42083045a07499957c1d6c2456a8b92c997535`
- `.aiassistant/records/aiscc/cycles/20260913_1511_aiscc-p2-3-disposition-builder-conflict-source-rework-entry-1.cycle.md`  `a7ed737a6739e812f7266f08a30c9d06f787fb70d6385f1dad3b703447c95cba`
- `.aiassistant/reports/aiscc/20260913_1511_aiscc-p2-3-full-builder-retained-root-conflict-rework-judgment-1.md`  `284775b7e4aa18fc6d1eac8ecf58ae166a61b55209b92f64fe008f55cf9eb854`
- `.aiassistant/tasks/done/20260913_1520_aiscc-p2-3-disposition-only-composition-entrypoint-transport-corrected-retry-1.md`  `1a282d0b9df9be3122dd12c461d50c6b189f69bf1ba276a448e269785397ea82`
- `.aiassistant/records/aiscc/cycles/20260913_1520_aiscc-p2-3-disposition-composition-transport-baseline-corrected-entry-1.cycle.md`  `acdcef07b9bd8bfdd79438b2a35e27488cef2b32415dfda671558130bc790260`
- `.aiassistant/reports/aiscc/20260913_1520_aiscc-p2-3-1511-transport-baseline-mismatch-retry-judgment-1.md`  `26c95d5758c58f8576534e642bdc6c2a9f0595de02903a29181b995e80301c5e`
- `.aiassistant/tasks/done/20260913_1531_aiscc-p2-3-disposition-only-composition-active-legacy-corrected-retry-1.md`  `e2fb91569aa164f23fe7664d4d5a78402ee6f5e56d563244a1c06053010185ed`
- `.aiassistant/records/aiscc/cycles/20260913_1531_aiscc-p2-3-disposition-composition-active-legacy-corrected-entry-1.cycle.md`  `ebc31620dfdd530930ba6c939b53840a1c08f67fcf660b888d88c745d97f1eae`
- `.aiassistant/reports/aiscc/20260913_1531_aiscc-p2-3-1520-active-legacy-baseline-mismatch-retry-judgment-1.md`  `85786b83189f5fc6c8173a61500fa12692a68a9bfef3287d8884d7666013ad73`
- `.aiassistant/tasks/done/20260913_1608_aiscc-p2-3-disposition-only-composition-export-contract-correction-1.md`  `8c80b8344a7b03dbe759438c757d236c9aed5e6e6ea190706e86756ded346231`
- `.aiassistant/records/aiscc/cycles/20260913_1608_aiscc-p2-3-disposition-only-composition-export-correction-entry-1.cycle.md`  `b30b3669c8e4923e6c81577168036c951b0aa60181d8d483fc2a6529df483073`
- `.aiassistant/reports/aiscc/20260913_1608_aiscc-p2-3-1531-export-contract-rework-judgment-1.md`  `6834884bed9e75a36a5801364b488b40774faf4dded372bedd72c85b9a0cb13d`

Require non-owned legacy active Task:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Do not move, stage, delete, rewrite, or complete it.

After current Cycle/Judgment placement while current persistence Task is active/ignored:

```text
Git-visible untracked:
20 exact
```

Any mismatch → STOP_WITH_REPORT_EXPORT.

# 3. accepted result authority

Browser accepts:

```text
620ffa448306c0f6486658cb8807e1887206311c2198be7d100c9f30f59ce4d1
```

Accepted evidence:

```text
19 members
18/18 manifest exact
40/40 contract PASS
scenario 57 passed
provider persistence 24 passed
workflow handoff 3 passed
unit 745 passed / 3 skipped
Ruff / py_compile / git diff --check PASS
private runtime untouched
```

Do not rerun tests.

# 4. Commit A

Stage only these exact 22 paths:

```text
.aiassistant/tasks/done/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-1.md
.aiassistant/records/aiscc/cycles/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1406_aiscc-p2-3-private-s1-invalid-history-disposition-execution-authorization-judgment-1.md
.aiassistant/tasks/done/20260913_1435_aiscc-p2-3-private-s1-invalid-history-disposition-root-authority-retry-1.md
.aiassistant/records/aiscc/cycles/20260913_1435_aiscc-p2-3-private-s1-root-authority-reconstructed-disposition-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1435_aiscc-p2-3-private-s1-root-authority-transport-gap-retry-judgment-1.md
.aiassistant/tasks/done/20260913_1511_aiscc-p2-3-disposition-only-composition-entrypoint-source-rework-1.md
.aiassistant/records/aiscc/cycles/20260913_1511_aiscc-p2-3-disposition-builder-conflict-source-rework-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1511_aiscc-p2-3-full-builder-retained-root-conflict-rework-judgment-1.md
.aiassistant/tasks/done/20260913_1520_aiscc-p2-3-disposition-only-composition-entrypoint-transport-corrected-retry-1.md
.aiassistant/records/aiscc/cycles/20260913_1520_aiscc-p2-3-disposition-composition-transport-baseline-corrected-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1520_aiscc-p2-3-1511-transport-baseline-mismatch-retry-judgment-1.md
.aiassistant/tasks/done/20260913_1531_aiscc-p2-3-disposition-only-composition-active-legacy-corrected-retry-1.md
.aiassistant/records/aiscc/cycles/20260913_1531_aiscc-p2-3-disposition-composition-active-legacy-corrected-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1531_aiscc-p2-3-1520-active-legacy-baseline-mismatch-retry-judgment-1.md
.aiassistant/tasks/done/20260913_1608_aiscc-p2-3-disposition-only-composition-export-contract-correction-1.md
.aiassistant/records/aiscc/cycles/20260913_1608_aiscc-p2-3-disposition-only-composition-export-correction-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1608_aiscc-p2-3-1531-export-contract-rework-judgment-1.md
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
.aiassistant/records/aiscc/cycles/20260913_1633_aiscc-p2-3-disposition-only-composition-final-acceptance-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260913_1633_aiscc-p2-3-disposition-only-composition-final-acceptance-judgment-1.md
```

Require:

```text
candidate source/test:
2 exact

governance/provenance:
20 exact

total:
22 exact
```

Commit message:

```text
fix(aiscc): persist disposition-only composition builder
```

Require:

```text
Commit A parent = 86288febf1cbd94bbb0235cfc680bf6c6c8f7772
changed paths = 22 exact
no amend
```

# 5. canonical state reconciliation

Only after Commit A exists, modify exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

No other tracked path may change.

## CURRENT_STATE_SUMMARY

Preserve all prior accepted history.

Record at minimum:

```text
P2-3:
IN_PROGRESS

invalid-history abort contract:
FINAL_ADMITTED / PERSISTED

source-owned invalid-history disposition:
FINAL_ADMITTED / PERSISTED

disposition-only composition entrypoint:
FINAL_ADMITTED / PERSISTED

entrypoint:
build_stockroom_invalid_history_disposition

accepted result ZIP:
620ffa448306c0f6486658cb8807e1887206311c2198be7d100c9f30f59ce4d1

scenario:
57 / 57 PASS

provider persistence:
24 / 24 PASS

workflow handoff:
3 / 3 PASS

unit:
745 passed / 3 skipped

0036 durable S1:
HOLD / PRESERVED / NOT YET DISPOSED

private disposition execution retry:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

legacy 1400 active Task:
NON_OWNED / PRESERVED
```

Record actual Commit A.

Do not embed future Commit B hash.

## DECISION_REGISTER

Add one bounded decision:

```text
decision_id:
AISCC-P2-3-S1-DISPOSITION-ONLY-COMPOSITION-V1

status:
FINAL_ADMITTED / PERSISTED
```

Record:

```text
accepted result ZIP:
620ffa448306c0f6486658cb8807e1887206311c2198be7d100c9f30f59ce4d1

actual Commit A:
<actual>

dedicated public builder:
build_stockroom_invalid_history_disposition

full production builder:
UNCHANGED

StockroomWorkspace empty-root invariant:
PRESERVED

private runtime disposition:
NOT EXECUTED

next:
separate exact private-runtime disposition retry
```

Do not rewrite unrelated decisions.

## NEXT_ACTIONS

Set immediate action:

```text
phase:
P2-3

work_type:
PRIVATE_S1_INVALID_HISTORY_DISPOSITION_EXECUTION_RETRY

title:
P2-3 stranded S1 disposition execution via dedicated builder

status:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

subject:
exact retained 0036 run/attempt only

required builder:
build_stockroom_invalid_history_disposition

required preflight:
reconstruct exact private root authority
verify WorkRun RUNNING/v2
verify attempt NOT_STARTED/v1 causal READY-v1
verify zero operations/outputs/evidence/Judgment
verify active historical workspace/fingerprint
verify no running Stockroom transient

forbidden before later Browser authorization:
full production builder
new run/attempt
provider/tool execution
delayed EXECUTION_STARTED
READY→RUNNING replay
DB-direct repair
broad cleanup
evidence/Judgment
```

Do not mark runtime disposition started/authorized.

# 6. Commit B

Move current Task byte-identically active→done.

Stage only:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/tasks/done/20260913_1633_aiscc-p2-3-disposition-only-composition-final-acceptance-git-persistence-1.md
```

Commit message:

```text
docs(aiscc): reconcile disposition-only composition state
```

Require:

```text
Commit B parent = actual Commit A

graph:
86288febf1cbd94bbb0235cfc680bf6c6c8f7772
→ Commit A
→ Commit B

final index:
empty

final tracked:
clean

final Git-visible untracked:
none

legacy 1400 active:
still present / exact / ignored / non-owned
```

No push.

# 7. forbidden

Do not:

```text
modify source/test
rerun tests
access Docker/PostgreSQL/private runtime
perform real disposition
stage or move legacy 1400 active
git push/reset/restore/checkout/stash/clean/amend
```

# 8. contract review

Require exactly 35 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
BASELINE_STATE_HASHES_EXACT
PRE_DELIVERY_UNTRACKED_18_EXACT
LEGACY_1400_ACTIVE_EXACT
POST_DELIVERY_UNTRACKED_20_EXACT
INDEX_EMPTY_PREWRITE
TRACKED_DIRTY2_EXACT
ACCEPTED_CANDIDATE_HASHES_EXACT
CURRENT_ACCEPTANCE_ARTIFACTS_EXACT
COMMIT_A_ALLOWLIST_22_EXACT
COMMIT_A_PARENT_EXACT
COMMIT_A_CREATED
COMMIT_A_PATH_SET_EXACT
COMMIT_A_CANDIDATE2_EXACT
COMMIT_A_GOVERNANCE20_EXACT
THREE_STATE_OWNER_RECONCILIATION_EXACT
DISPOSITION_ONLY_COMPOSITION_ACCEPTANCE_RECORDED
LEGACY_1400_ACTIVE_NONOWNED_RECORDED
STRANDED_S1_HOLD_RECORDED
NEXT_ACTION_PRIVATE_DISPOSITION_EXECUTION_RETRY_ENTRY_ONLY
NO_PRIVATE_RUNTIME_ACCESS
NO_RUNTIME_DISPOSITION
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
COMMIT_B_ALLOWLIST_4_EXACT
COMMIT_B_PARENT_COMMIT_A
COMMIT_B_CREATED
FINAL_GRAPH_EXACT
FINAL_INDEX_TRACKED_UNTRACKED_CLEAN
FINAL_LEGACY_1400_ACTIVE_PRESERVED
NO_SOURCE_TEST_MUTATION_DURING_PERSISTENCE
NO_TEST_RERUN
NO_DOCKER_DB_ACCESS
NO_PUSH
EXPORT_INTEGRITY_PASS
```

Success:

```text
35 / 35 PASS
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

Include byte-preserving project-relative copies of every Commit A and Commit B path.

Expected:

```text
36 total members
35 non-self manifest rows
one top-level directory
CRC PASS
TASK.md == canonical done Task
manifest hashes exact
```

Do not include the non-owned legacy 1400 active Task in export or commits.

# 10. success ceiling

```text
disposition-only composition:
FINAL_ADMITTED / PERSISTED

canonical state:
RECONCILED

0036 S1:
HOLD / PRESERVED / NOT YET DISPOSED

legacy 1400 active:
PRESERVED / NON-OWNED

private disposition retry:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

P2-3:
IN_PROGRESS
```
