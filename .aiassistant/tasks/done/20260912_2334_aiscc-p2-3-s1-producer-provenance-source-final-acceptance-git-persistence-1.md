# 작업지시서: P2-3 S1 producer-provenance source final acceptance Git persistence

## meta

- task_id: `20260912_2334_aiscc-p2-3-s1-producer-provenance-source-final-acceptance-git-persistence-1`
- created_at: `2026-09-12T23:34:15+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `FINAL_ACCEPTANCE_PERSISTENCE / STATE_RECONCILIATION`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- required_parent: `4096913e9a117bd49bfecdb1ce5ca8de2735d661`
- required_grandparent: `6d41633210f0e556dd4292ee62a8600c6b54215f`
- executor_session_action: `CONTINUE_CURRENT_CONTEXT`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- private_s1_execution_authorized: `No`
- success_ceiling: `SOURCE_CORRECTION_FINAL_ADMITTED_PERSISTED / PRIVATE_S1_ENTRY_READY`

# 0. execution context / Python

Continue from the existing working context and preserved six-path accepted candidate.

Do not reconstruct or reapply the source patch.

For Python use only:

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

# 1. purpose

Persist the Browser-final-accepted S1 producer-provenance source correction and reconcile canonical state.

This Task is Git/governance persistence only.

Do not execute private S1 and do not access Docker/PostgreSQL/private runtime resources.

# 2. inbound transport

Verify exact delivery ZIP filename/SHA from the Short Prompt with the exact Python executable.

Require three flat safe members.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_2334_aiscc-p2-3-s1-producer-provenance-source-final-acceptance-git-persistence-1.md
```

Require byte equality and ignored status.

Then place:

```text
.aiassistant/records/aiscc/cycles/20260912_2334_aiscc-p2-3-s1-producer-provenance-source-final-acceptance-persistence-entry-1.cycle.md
SHA-256:
a96afd22293f3fbf414b7ac8c4a56a624228c9e1213cdf0203dd6f145033d7b8

.aiassistant/reports/aiscc/20260912_2334_aiscc-p2-3-s1-producer-provenance-source-final-acceptance-judgment-1.md
SHA-256:
d298002e40896385cb2596f523bf358bcf7a1c502a325bbb2e447b29c264b4d0
```

Bootstrap mismatch:

```text
STOP
no Git write
no state mutation
no source mutation
no runtime access
no report/export
```

# 3. repository baseline

Require:

```text
branch:
main

HEAD:
ee623c995cf1c24b4a362834f2d6d1fdf71a30cd

HEAD^:
4096913e9a117bd49bfecdb1ce5ca8de2735d661

HEAD^^:
6d41633210f0e556dd4292ee62a8600c6b54215f

index:
empty
```

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `7d0c9954b87e945b8c1c3fb66bda2dd54d23d5c3319202ef9fb24aa0ac56f424`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `04ec792c5e6dd4a7c8d2d35b716d1ed1fd569e60bb557532b811bc33dd434946`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `61ae340fa06e3d87d80f3308a240dacc1e0ba132a3b241a2059757830cf6312a`

Before current delivery Git-visible untracked must be exactly these 27 paths/hashes:

- `.aiassistant/tasks/done/20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1.md`  `0668ed1fb71ce57f6b87dacb91c810f7505596eb6efe835841c019f3a2d51ecd`
- `.aiassistant/records/aiscc/cycles/20260912_1749_aiscc-p2-3-cut-c-persisted-private-s1-execution-entry-1.cycle.md`  `75fe2a744d010e327ff2d549aa998e2e64e0449735d50eec69a4fd6a183044ad`
- `.aiassistant/reports/aiscc/20260912_1749_aiscc-p2-3-cut-c-persistence-final-acceptance-private-s1-authorization-judgment-1.md`  `6457922c2520c2255edf9574b1c68c3ed633c3615e80be5c95c7e04f9e5961ed`
- `.aiassistant/tasks/done/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-retry-1.md`  `f3fbe8fed5d2dfcc6ac6b4586567b410e64653f648943f162219b11648ab3819`
- `.aiassistant/records/aiscc/cycles/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocked-retry-entry-1.cycle.md`  `1bb88d04b2e567a9b11ab8fb99449571696a5e039571cef6438fa62bb3fea870`
- `.aiassistant/reports/aiscc/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocker-hold-judgment-1.md`  `ee9436791b8595333090eb2a06b295ef4b3b87f620894756fea0a97176ebd25d`
- `.aiassistant/tasks/done/20260912_2024_aiscc-p2-3-s1-admission-pending-evidence-state-contract-source-rework-1.md`  `c61d14d7cb8fd3ac929701550a3530577eed99ad083b0bacee29f55c27d7584c`
- `.aiassistant/records/aiscc/cycles/20260912_2024_aiscc-p2-3-s1-source-state-contract-defect-rework-entry-1.cycle.md`  `8c9ca5c06d658e9e2723ee70b2b54b999801cf17494543480caf7743840e7a44`
- `.aiassistant/reports/aiscc/20260912_2024_aiscc-p2-3-s1-source-state-contract-defect-confirmed-judgment-1.md`  `c8a921efc6112c2bbd8532ed0869e08e9c1f1eebea4121805f0c839ad3bbf0c2`
- `.aiassistant/tasks/done/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-decoupling-source-rework-1.md`  `bf1c50f34cdd21ccf14d3009aeb309df3904d8903fdbeb30063b911c4a4279f3`
- `.aiassistant/records/aiscc/cycles/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-rework-entry-1.cycle.md`  `119f40188ec87d4e98d0152f9c762a90d40f1096316beaba158cc0244b19ce5f`
- `.aiassistant/reports/aiscc/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-conflict-judgment-1.md`  `cefcaa10a62e80779121bbf1014caa748195c48cb62d48c5e2406b99cc77bc37`
- `.aiassistant/tasks/done/20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-source-rework-1.md`  `51f718131e55004b8f9cb2cfa80889baf52bdac9151d37d0a5e34ec138df891a`
- `.aiassistant/records/aiscc/cycles/20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-rework-entry-1.cycle.md`  `fd7877ecab06d40dcac3a36f99a5b0ad72c94a0ffb055a1dab51d79defd4327f`
- `.aiassistant/reports/aiscc/20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-scope-expansion-judgment-1.md`  `06cb0d64c092417d1dfd4b98279a9a9b0d8df41e169ac9a2b410f130fadfc7bc`
- `.aiassistant/tasks/done/20260912_2158_aiscc-p2-3-s1-canonical-execution-bound-ref-contract-and-source-rework-1.md`  `a5108370d89424dc4b74b918be4358083d9e9b835039d92a9dc5e2720ebda9e4`
- `.aiassistant/records/aiscc/cycles/20260912_2158_aiscc-p2-3-s1-bound-ref-contract-defined-source-rework-entry-1.cycle.md`  `85194e69195c77f5e2490b586a7113ffbcb1fd426c4bba5362064bd4a379ebac`
- `.aiassistant/reports/aiscc/20260912_2158_aiscc-p2-3-s1-bound-ref-contract-definition-judgment-1.md`  `c99df7f4b9ec25c59dc7d08a931c0770e7cda9c79828f6fae8416cfb94f28247`
- `.aiassistant/tasks/done/20260912_2238_aiscc-p2-3-s1-bound-ref-candidate-completion-and-unit-policy-alignment-1.md`  `3ada0822cb951fea939aa9833ae28ba6cd10bc21d5957da3433b3b77cefca100`
- `.aiassistant/records/aiscc/cycles/20260912_2238_aiscc-p2-3-s1-bound-ref-partial-candidate-completion-entry-1.cycle.md`  `280cb063fd4ebe465a9434229085a0d03197ac5d1b2220ff5b203cb2d7434f88`
- `.aiassistant/reports/aiscc/20260912_2238_aiscc-p2-3-s1-bound-ref-partial-candidate-hold-judgment-1.md`  `add0e970d1fa9d4a5427e3ba8cb1bd54cd1756d2c889d8cac3cb1997c76670ed`
- `.aiassistant/tasks/done/20260912_2251_aiscc-p2-3-scenario-static-module-boundary-inventory-1.md`  `2059a29017a5e558cc254aad863780520dabdf6e7567bbd826e2791cddb5729c`
- `.aiassistant/records/aiscc/cycles/20260912_2251_aiscc-p2-3-scenario-static-module-boundary-inventory-entry-1.cycle.md`  `9f24995e0eb694436641fda0a8eaefa6c85ab46830f5873730739c767a420a9a`
- `.aiassistant/reports/aiscc/20260912_2251_aiscc-p2-3-unit-policy-boundary-inventory-authorization-judgment-1.md`  `32fdcda7ea36d866af86d39ea90ecf66910ed421e2c43c6a1fdd3457864ca6db`
- `.aiassistant/tasks/done/20260912_2300_aiscc-p2-3-s1-static-module-policy-and-bound-ref-candidate-finalization-1.md`  `22042a9e86d4ebc4142d035d3a86f620ad03bd6512ad3b0ca2076ad10b27838c`
- `.aiassistant/records/aiscc/cycles/20260912_2300_aiscc-p2-3-s1-static-module-policy-defined-candidate-finalization-entry-1.cycle.md`  `a7677d92239827a155adfa52d530cc9bf6bb853c253f4613d09361d5631c83a8`
- `.aiassistant/reports/aiscc/20260912_2300_aiscc-p2-3-s1-static-module-policy-definition-judgment-1.md`  `f5010fb69514816ddc3a5749c3375d0711d6d15973c717af29c620aac8a05275`

Tracked worktree must contain exactly these six accepted modifications with exact final hashes:

- `src/aiscc/workflow/guards.py`  `e7509199bca3b901c7a04b4e5a1d8c23bab217eca5b78a3b9319d10300993cab`
- `src/aiscc/persistence/repository.py`  `ab00af3dd871477da74b83275258aa48a47ba9a7081aad0154a808b6e4f1c089`
- `src/aiscc/scenarios/capture_runner.py`  `0dab27e0ce9ce2da7953188bcb26f288b637a4ba524141be2800b08302a59b18`
- `src/aiscc/scenarios/stockroom_production.py`  `1ca58848a837e1130229c7a0e085df999d04c6041c77bb61098185d342ff14a0`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `02f5835a726f22d81d9d631f120c9d7c9b3c1311cc23ed93db5d3abd9a57f41e`
- `tests/unit/scenarios/test_contracts.py`  `bd56e823f4ae15e82233d2cbd50e2d20d13176dc88c0ee00c7ddab8de752b0d7`

No seventh tracked modification is allowed.

After current Cycle/Judgment placement while current Task remains active/ignored:

```text
Git-visible untracked:
29 exact

27 predecessor artifacts
current Cycle
current Judgment

tracked dirty:
6 exact

index:
empty
```

Any mismatch:

```text
DIRTY_WORKSPACE_MIXED or BASELINE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

Do not reset/restore/checkout/stash/clean.

# 4. accepted source result — reuse only

Browser accepts result ZIP:

```text
d856d9238f78facc870d51837a64c7e446ae0c3309c021ac54f11299ea47e0cf
```

Accepted evidence:

```text
22 members / CRC PASS
manifest 21/21 exact
contract 38/38 PASS
py_compile PASS
Ruff PASS
tests/unit/scenarios/test_contracts.py 27 passed
tests/integration/scenarios/test_stockroom_capture_runner.py 41 passed / 1 skipped
tests/unit 741 passed / 2 skipped
git diff --check PASS
```

Do not rerun tests during this persistence Task.

Accepted semantic state:

```text
G_EXECUTOR_SUBMISSION:
canonical exact submission + attempt binding

CURRENT:
ADMISSION_PENDING/current exact state/version

LINK:
exact historical admitted RUNNING → ADMISSION_PENDING predecessor

PRODUCER:
issuer-verified RUNNING/original producer version
exact submission + attempt

runner order:
unchanged

static scenario contract import policy:
exact __init__.py / catalog.py / models.py only
```

This source acceptance does not substitute for private runtime execution.

# 5. Commit A — source correction + complete governance lineage

Before staging, reverify every path/hash from section 3 plus current Cycle/Judgment.

Authorize exact-path Git staging only for these 35 paths:

```text
.aiassistant/tasks/done/20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1.md
.aiassistant/records/aiscc/cycles/20260912_1749_aiscc-p2-3-cut-c-persisted-private-s1-execution-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1749_aiscc-p2-3-cut-c-persistence-final-acceptance-private-s1-authorization-judgment-1.md
.aiassistant/tasks/done/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-retry-1.md
.aiassistant/records/aiscc/cycles/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocked-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocker-hold-judgment-1.md
.aiassistant/tasks/done/20260912_2024_aiscc-p2-3-s1-admission-pending-evidence-state-contract-source-rework-1.md
.aiassistant/records/aiscc/cycles/20260912_2024_aiscc-p2-3-s1-source-state-contract-defect-rework-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_2024_aiscc-p2-3-s1-source-state-contract-defect-confirmed-judgment-1.md
.aiassistant/tasks/done/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-decoupling-source-rework-1.md
.aiassistant/records/aiscc/cycles/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-rework-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-conflict-judgment-1.md
.aiassistant/tasks/done/20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-source-rework-1.md
.aiassistant/records/aiscc/cycles/20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-rework-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-scope-expansion-judgment-1.md
.aiassistant/tasks/done/20260912_2158_aiscc-p2-3-s1-canonical-execution-bound-ref-contract-and-source-rework-1.md
.aiassistant/records/aiscc/cycles/20260912_2158_aiscc-p2-3-s1-bound-ref-contract-defined-source-rework-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_2158_aiscc-p2-3-s1-bound-ref-contract-definition-judgment-1.md
.aiassistant/tasks/done/20260912_2238_aiscc-p2-3-s1-bound-ref-candidate-completion-and-unit-policy-alignment-1.md
.aiassistant/records/aiscc/cycles/20260912_2238_aiscc-p2-3-s1-bound-ref-partial-candidate-completion-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_2238_aiscc-p2-3-s1-bound-ref-partial-candidate-hold-judgment-1.md
.aiassistant/tasks/done/20260912_2251_aiscc-p2-3-scenario-static-module-boundary-inventory-1.md
.aiassistant/records/aiscc/cycles/20260912_2251_aiscc-p2-3-scenario-static-module-boundary-inventory-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_2251_aiscc-p2-3-unit-policy-boundary-inventory-authorization-judgment-1.md
.aiassistant/tasks/done/20260912_2300_aiscc-p2-3-s1-static-module-policy-and-bound-ref-candidate-finalization-1.md
.aiassistant/records/aiscc/cycles/20260912_2300_aiscc-p2-3-s1-static-module-policy-defined-candidate-finalization-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_2300_aiscc-p2-3-s1-static-module-policy-definition-judgment-1.md
src/aiscc/workflow/guards.py
src/aiscc/persistence/repository.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
tests/unit/scenarios/test_contracts.py
.aiassistant/records/aiscc/cycles/20260912_2334_aiscc-p2-3-s1-producer-provenance-source-final-acceptance-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260912_2334_aiscc-p2-3-s1-producer-provenance-source-final-acceptance-judgment-1.md
```

Require:

```text
staged:
35 exact

source/test:
6 exact

governance/provenance:
29 exact

no extra
```

Commit message:

```text
fix(aiscc): persist S1 producer provenance correction
```

Require:

```text
Commit A parent:
ee623c995cf1c24b4a362834f2d6d1fdf71a30cd

Commit A:
created

Commit A changed paths:
35 exact
```

No amend.

# 6. canonical state reconciliation

Only after Commit A exists, modify exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

No other tracked file may change.

## 6.1 CURRENT_STATE_SUMMARY

Preserve existing Cut A/B/C accepted/persisted history.

Add/update the current P2-3 S1 source-correction authority so the current state says at minimum:

```text
P2-3:
IN_PROGRESS

Cut C:
FINAL_ADMITTED / PERSISTED

private S1 initial execution:
BLOCKED BEFORE RUNTIME by source-contract defects
historical lineage preserved

S1 producer-provenance source correction:
FINAL_ADMITTED / PERSISTED

source correction Browser review:
COMPLETED

source correction result ZIP SHA-256:
d856d9238f78facc870d51837a64c7e446ae0c3309c021ac54f11299ea47e0cf

canonical bound-ref contract:
V1 exact execution submission + execution attempt binding

CURRENT / LINK / PRODUCER:
ADMISSION_PENDING current / exact historical predecessor / RUNNING immutable producer

same-shape cross-producer substitution:
DENIED / PROVED

static scenario import-policy membership:
__init__.py / catalog.py / models.py exact

private runtime root:
CREATED / RETAINED
do not record absolute path

private DB authority enrollment:
ESTABLISHED / BOUNDED / RETAINED

private S1:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED
separate exact Browser-issued S1 Task required
```

Record actual Commit A hash after it exists.

Do not embed future Commit B hash into files contained by Commit B.

## 6.2 DECISION_REGISTER

Add exactly one bounded decision entry:

```text
decision_id:
AISCC-P2-3-PRIVATE-S1-PRODUCER-PROVENANCE-SOURCE-CORRECTION-V1

decision_status:
FINAL_ADMITTED / PERSISTED
```

Record:

```text
Browser accepted source result:
d856d9238f78facc870d51837a64c7e446ae0c3309c021ac54f11299ea47e0cf

actual Commit A:
<actual>

canonical G_EXECUTOR_SUBMISSION binding:
submission_id + execution_attempt_id using V1 canonical bound refs

producer-link invariant:
CURRENT != PRODUCER
exact admitted predecessor links them

producer state:
RUNNING/original producer version

evidence-review current state:
ADMISSION_PENDING/current version

cross-producer substitution:
DENIED

static scenario import-policy members:
__init__.py / catalog.py / models.py

accepted source/test path count:
6

private S1 runtime:
not executed by source correction

next authority:
separate private S1 execution Task
```

Do not rewrite unrelated historical decisions.

## 6.3 NEXT_ACTIONS

Set the immediate P2-3 next action to:

```text
phase:
P2-3

work_type:
PRIVATE_SCENARIO_EXECUTION

title:
P2-3 private S1 normal scenario execution/capture retry after producer-provenance correction

status:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

reason:
source correction is FINAL_ADMITTED / PERSISTED

required authorization:
separate exact Browser-issued S1 Task

scenario:
S1 normal

expected semantic terminal:
ACCEPTED

reuse:
retained Cut C private environment authority, subject to exact next-Task preflight

forbidden before authorization:
prepare_capture
new WorkRun
provider/tool execution
scenario Docker dispatch
runtime evidence admission
scenario Judgment
```

Do not mark S1 started or authorized.

# 7. current Task lifecycle + Commit B

After state reconciliation is validated, move current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_2334_aiscc-p2-3-s1-producer-provenance-source-final-acceptance-git-persistence-1.md
→
.aiassistant/tasks/done/20260912_2334_aiscc-p2-3-s1-producer-provenance-source-final-acceptance-git-persistence-1.md
```

Authorize exact-path staging only for:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/tasks/done/20260912_2334_aiscc-p2-3-s1-producer-provenance-source-final-acceptance-git-persistence-1.md
```

Require:

```text
staged:
4 exact
no extra
```

Commit message:

```text
docs(aiscc): reconcile S1 producer provenance state
```

Require:

```text
Commit B parent:
actual Commit A

Commit B:
created

graph:
ee623c995cf1c24b4a362834f2d6d1fdf71a30cd
→ Commit A
→ Commit B

final index:
empty

final tracked worktree:
clean

final Git-visible untracked:
none
```

No push.

# 8. absolute forbidden actions

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
private runtime-root filesystem access
provider/network runtime

prepare_capture
WorkRun creation
S1/S2/S3/S4
runtime evidence admission
HumanResult
scenario Judgment
Replay
deployment
```

# 9. contract review

Require exactly 31 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
BASELINE_STATE_HASHES_EXACT
PRE_DELIVERY_UNTRACKED_27_EXACT
POST_DELIVERY_UNTRACKED_29_EXACT
INDEX_EMPTY_PREWRITE
TRACKED_DIRTY6_EXACT
ACCEPTED_SOURCE_HASHES_EXACT
CURRENT_ACCEPTANCE_ARTIFACTS_EXACT
COMMIT_A_ALLOWLIST_35_EXACT
COMMIT_A_PARENT_EXACT
COMMIT_A_CREATED
COMMIT_A_PATH_SET_EXACT
COMMIT_A_SOURCE6_EXACT
COMMIT_A_GOVERNANCE29_EXACT
THREE_STATE_OWNER_RECONCILIATION_EXACT
SOURCE_CORRECTION_DECISION_RECORDED
PRIVATE_S1_ENTRY_READY_NOT_AUTHORIZED
RUNTIME_FACTS_REUSED_ONLY
NO_PRIVATE_RESOURCE_ACCESS
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
COMMIT_B_ALLOWLIST_4_EXACT
COMMIT_B_PARENT_COMMIT_A
COMMIT_B_CREATED
FINAL_GRAPH_EXACT
FINAL_INDEX_TRACKED_UNTRACKED_CLEAN
NO_SOURCE_RUNTIME_TEST_MUTATION
NO_DOCKER_DB_RUNTIME_ROOT_ACCESS
NO_S1_S4_EXECUTION
NO_PUSH
EXPORT_INTEGRITY_PASS
```

Success requires:

```text
31 / 31 PASS
```

# 10. success export

Target:

```text
.aiassistant/reports/target/20260912_2334_aiscc-p2-3-s1-producer-provenance-source-final-acceptance-git-persistence-1/
```

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

Include byte-preserving project-relative copies of all Commit A and Commit B paths.

Expected success export:

```text
49 total members
48 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == current canonical done Task
```

Do not include prior result ZIPs, private/runtime files, credentials, caches, or ignored helper artifacts.

# 11. mandatory stop

Stop with bounded report/export after:

```text
baseline mismatch
unexpected tracked/untracked path
unexpected staged path
commit failure
state edit outside exact three owners
source/test mutation
private/runtime access attempt
S1 execution attempt
```

Do not broaden scope.

# 12. success ceiling

```text
S1 producer-provenance source correction:
FINAL_ADMITTED / PERSISTED

canonical state:
RECONCILED

private S1:
ENTRY_READY / NOT_STARTED / NOT_AUTHORIZED

S1 execution:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
