# 작업지시서: P2-3 S1 current-state / producer-provenance decoupling source rework

## meta

- task_id: `20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-decoupling-source-rework-1`
- created_at: `2026-09-12T20:52:11+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_REWORK / AUTHORITY_DECOUPLING`
- evidence_profile: `STANDARD`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- required_parent: `4096913e9a117bd49bfecdb1ce5ca8de2735d661`
- required_grandparent: `6d41633210f0e556dd4292ee62a8600c6b54215f`
- fresh_ide_executor_chat: `REQUIRED`
- success_ceiling: `S1_SOURCE_AUTHORITY_COUPLING_CORRECTED_CANDIDATE / BROWSER_REVIEW_PENDING`
- private_s1_execution_authorized: `No`

# 0. purpose

Correct the source-level authority coupling found by the 2024 static review.

The system must preserve two different state facts simultaneously:

```text
A. current workflow state at evidence review:
ADMISSION_PENDING / current state_version

B. immutable execution producer provenance:
RUNNING / producer state_version
```

`ExecutionSubmissionRef` is producer authority, not current WorkflowState authority and not AdmittedEvidence.

The implementation must not force A and B to be the same state/version.

# 1. transport

Start in a fresh IDE Executor chat.

Verify Short Prompt ZIP filename/SHA-256.
Require exactly three flat members.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-decoupling-source-rework-1.md
```

Require byte equality and ignored status.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-rework-entry-1.cycle.md
SHA-256:
119f40188ec87d4e98d0152f9c762a90d40f1096316beaba158cc0244b19ce5f

.aiassistant/reports/aiscc/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-conflict-judgment-1.md
SHA-256:
cefcaa10a62e80779121bbf1014caa748195c48cb62d48c5e2406b99cc77bc37
```

Bootstrap mismatch:

```text
STOP
no source write
no test execution
no report/export
```

# 2. repository baseline

Require:

```text
branch main
HEAD ee623c995cf1c24b4a362834f2d6d1fdf71a30cd
HEAD^ 4096913e9a117bd49bfecdb1ce5ca8de2735d661
HEAD^^ 6d41633210f0e556dd4292ee62a8600c6b54215f
index empty
tracked worktree clean
```

Before current delivery Git-visible untracked exactly these 9 predecessor artifacts:

- `.aiassistant/tasks/done/20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1.md`  `0668ed1fb71ce57f6b87dacb91c810f7505596eb6efe835841c019f3a2d51ecd`
- `.aiassistant/records/aiscc/cycles/20260912_1749_aiscc-p2-3-cut-c-persisted-private-s1-execution-entry-1.cycle.md`  `75fe2a744d010e327ff2d549aa998e2e64e0449735d50eec69a4fd6a183044ad`
- `.aiassistant/reports/aiscc/20260912_1749_aiscc-p2-3-cut-c-persistence-final-acceptance-private-s1-authorization-judgment-1.md`  `6457922c2520c2255edf9574b1c68c3ed633c3615e80be5c95c7e04f9e5961ed`
- `.aiassistant/tasks/done/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-retry-1.md`  `f3fbe8fed5d2dfcc6ac6b4586567b410e64653f648943f162219b11648ab3819`
- `.aiassistant/records/aiscc/cycles/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocked-retry-entry-1.cycle.md`  `1bb88d04b2e567a9b11ab8fb99449571696a5e039571cef6438fa62bb3fea870`
- `.aiassistant/reports/aiscc/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocker-hold-judgment-1.md`  `ee9436791b8595333090eb2a06b295ef4b3b87f620894756fea0a97176ebd25d`
- `.aiassistant/tasks/done/20260912_2024_aiscc-p2-3-s1-admission-pending-evidence-state-contract-source-rework-1.md`  `c61d14d7cb8fd3ac929701550a3530577eed99ad083b0bacee29f55c27d7584c`
- `.aiassistant/records/aiscc/cycles/20260912_2024_aiscc-p2-3-s1-source-state-contract-defect-rework-entry-1.cycle.md`  `8c9ca5c06d658e9e2723ee70b2b54b999801cf17494543480caf7743840e7a44`
- `.aiassistant/reports/aiscc/20260912_2024_aiscc-p2-3-s1-source-state-contract-defect-confirmed-judgment-1.md`  `c8a921efc6112c2bbd8532ed0869e08e9c1f1eebea4121805f0c839ad3bbf0c2`

After current Cycle/Judgment placement while current Task is active/ignored:

```text
Git-visible untracked:
11 exact

nine predecessor artifacts
current Cycle
current Judgment
```

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `7d0c9954b87e945b8c1c3fb66bda2dd54d23d5c3319202ef9fb24aa0ac56f424`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `04ec792c5e6dd4a7c8d2d35b716d1ed1fd569e60bb557532b811bc33dd434946`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `61ae340fa06e3d87d80f3308a240dacc1e0ba132a3b241a2059757830cf6312a`

Unexpected path/delta:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 3. exact source baseline

Before mutation require exact whole-file hashes:

```text
src/aiscc/scenarios/stockroom_production.py
685e2ec549473e167ed1fe4d7de1050d7a53a449d1d278dcdb3439a471478f1f

src/aiscc/scenarios/capture_runner.py
600de0a4b0e718f02ab2e1907b7be62b2c4a23756559fdf99cb4cd55fb80b3d2

tests/integration/scenarios/test_stockroom_capture_runner.py
373f9d5bc6f260785cdf943aa649ce99ab5826e8ae09dd2982c18db09459fbf5
```

All must equal HEAD bytes.

Read exact current implementations needed to understand:

```text
StockroomCaptureRunner.run
StockroomCaptureOwnerAdapter.submit_runtime_evidence
StockroomCaptureOwnerAdapter._current
StockroomCaptureOwnerAdapter._request or equivalent request constructor
StockroomCaptureOwnerAdapter.transition / transition result handling
ExecutionSubmissionRef model
ExecutionReferenceAuthority.register_submission
ExecutionReferenceAuthority.verify
provider execution completion/submission issuance
WorkflowKernel load/transition
durable transition decision/projection APIs used by this adapter
```

Read canonical orchestration, provider/tool, evidence and security authority needed for the split.

# 4. mandatory source-coupling reproduction

Before editing mechanically prove:

```text
1. source-owned runner admits RUNNING_TO_ADMISSION_PENDING before submit_runtime_evidence
2. authoritative current state after that admitted transition is ADMISSION_PENDING/vN+1
3. submit_runtime_evidence currently expects current RUNNING
4. ExecutionSubmissionRef was issuer-bound to execution producer RUNNING/vN
5. current verification path currently derives producer verification request from the same current snapshot/request context
6. changing only current expected state to ADMISSION_PENDING would make producer verification compare incompatible state/version or otherwise weaken provenance
```

If any of these six facts is false:

```text
SOURCE_DIAGNOSIS_BASELINE_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 5. canonical semantics

Confirm:

```text
RUNNING → ADMISSION_PENDING:
G_EXECUTOR_SUBMISSION / executor completion provenance

ADMISSION_PENDING:
submission/evidence review state

ADMISSION_PENDING → ACCEPTED:
G_EVIDENCE + G_HUMAN_NOT_REQUIRED + G_JUDGMENT_ACCEPTED
```

Also confirm:

```text
ExecutionSubmissionRef:
immutable P1-5 producer authority

ExecutionSubmissionRef:
!= EvidenceCandidate admission
!= AdmittedEvidence
!= current WorkflowState

state/version change:
must not silently rewrite old producer provenance
```

# 6. predecessor linkage requirement

A valid correction must independently establish all three:

```text
CURRENT:
authoritative current WorkRun is ADMISSION_PENDING/current_version

PRODUCER:
ExecutionSubmissionRef is authentic and remains bound to RUNNING/producer_version

LINK:
the current ADMISSION_PENDING/current_version is the exact admitted immediate successor of
that producer RUNNING/producer_version for the same run/attempt and the expected
RUNNING_TO_ADMISSION_PENDING transition
```

The LINK must come from existing issuer/workflow durable authority already present in current source.

Forbidden proof:

```text
producer ref says RUNNING/vN
therefore assume current must be ADMISSION_PENDING/vN+1
```

without independent durable transition/current-state verification.

If existing source APIs cannot establish LINK without modifying another production source file:

```text
SOURCE_SCOPE_INSUFFICIENT
→ STOP before source write
→ report the exact additional owner/API/path required
```

Do not broaden scope yourself.

# 7. allowed tracked changes

Modify exactly:

```text
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

The runner must remain byte-identical.

The production correction may restructure `submit_runtime_evidence` locally as needed to separate
current-state and producer-provenance checks, but may not weaken either.

Required final semantics:

```text
current-state guard:
ADMISSION_PENDING exact

producer-ref expected provenance:
RUNNING exact
original producer state_version exact

same run/attempt:
exact

predecessor linkage:
durably verified

ExecutionReferenceAuthority.verify:
still used with issuer-backed expected producer context

_current / AuthorityConflictError:
still fail closed
```

# 8. forbidden implementation shortcuts

Do not:

```text
change runner transition order
submit evidence while current RUNNING
rebind ExecutionSubmissionRef to ADMISSION_PENDING
change producer state_version to current state_version
construct expected producer context solely by copying unverified fields from the ref
accept current RUNNING or ADMISSION_PENDING union
disable state/version comparison in ExecutionReferenceAuthority.verify
bypass issuer registry
bypass _current
catch-and-ignore AuthorityConflictError
change P1-4 transition matrix
change P1-5 provider authority globally
change P1-6 evidence model globally
```

# 9. focused regression

Add source-level/integration regression in:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Use current production adapter/runner authorities, not a replacement orchestration.

Required cases:

```text
POSITIVE:
RUNNING/vN execution submission ref
+ admitted RUNNING/vN → ADMISSION_PENDING/vN+1
+ current ADMISSION_PENDING/vN+1
→ runtime evidence producer verification proceeds

NEGATIVE_CURRENT:
current state still RUNNING
→ evidence-review current-state gate denies

NEGATIVE_PRODUCER_VERSION:
authentic-looking submission with wrong producer state_version
→ producer verification denies

NEGATIVE_LINK:
current ADMISSION_PENDING exists but is not the exact successor linkage for the submitted producer ref
→ deny

NON_SUBSTITUTION:
ExecutionSubmissionRef alone never creates admitted evidence or G_EVIDENCE
```

Also assert:

```text
runner RUNNING_TO_ADMISSION_PENDING call remains before submit_runtime_evidence
runner file byte-identical to baseline
_current remains fail closed
```

# 10. validation

Use repository `.venv` actual Python.

Run:

```text
.venv\Scripts\python.exe -B -m py_compile
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py

.venv\Scripts\python.exe -m ruff check
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py

.venv\Scripts\python.exe -B -m pytest -q
  tests/integration/scenarios/test_stockroom_capture_runner.py

.venv\Scripts\python.exe -B -m pytest -q
  tests/unit/scenarios
  tests/integration/scenarios
```

If the exact regression requires an existing provider/evidence unit file outside the allowed two paths,
do not edit it. Existing tests may be run read-only.

No Docker, PostgreSQL, private runtime, provider/network or S1 execution.

# 11. post-change proof

After edits mechanically prove:

```text
runner bytes unchanged
current evidence-review state = ADMISSION_PENDING
producer ref remains RUNNING/original version
predecessor LINK independently verified
ExecutionReferenceAuthority.verify semantics unchanged
_current fail-closed semantics unchanged
no evidence admission occurs merely because producer ref exists
```

Inspect exact `git diff --` for the two allowed paths.

No unrelated formatting.

# 12. Git boundary

No staging/commit/push.

Forbidden:

```text
git add
git commit
git push
git reset
git restore
git checkout
git stash
git clean
```

Before Task movement require:

```text
tracked modified paths:
exactly 2

src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py

index:
empty

Git-visible untracked:
11 exact
```

Move current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-decoupling-source-rework-1.md
→
.aiassistant/tasks/done/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-decoupling-source-rework-1.md
```

Final Git-visible untracked:

```text
12 exact

nine predecessor artifacts
current Cycle
current Judgment
current done Task
```

# 13. contract review

Require exactly 34 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
PREDECESSOR_9_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
ADAPTER_BASELINE_HASH_EXACT
RUNNER_BASELINE_HASH_EXACT
REGRESSION_TEST_BASELINE_HASH_EXACT
CURRENT_SOURCE_COUPLING_DEFECT_REPRODUCED
CANONICAL_CURRENT_STATE_ADMISSION_PENDING_CONFIRMED
CANONICAL_PRODUCER_STATE_RUNNING_CONFIRMED
PRODUCER_REF_NON_SUBSTITUTION_CONFIRMED
PREDECESSOR_LINKAGE_MECHANISM_EXACT
MODIFIED_PATH_SET_EXACT_2
CURRENT_STATE_GUARD_ADMISSION_PENDING
PRODUCER_PROVENANCE_REMAINS_RUNNING
PRODUCER_STATE_VERSION_NOT_REBOUND
EXECUTION_REFERENCE_VERIFY_NOT_WEAKENED
RUNNER_TRANSITION_ORDER_UNCHANGED
CURRENT_FAIL_CLOSED_CHECK_PRESERVED
REGRESSION_CURRENT_STATE_PASS
REGRESSION_PRODUCER_PROVENANCE_PASS
REGRESSION_WRONG_PRODUCER_VERSION_DENIED
REGRESSION_UNRELATED_PENDING_STATE_DENIED
TARGETED_PYTEST_PASS
SCENARIO_REGRESSION_PYTEST_PASS
RUFF_PASS
PY_COMPILE_PASS
NO_DOCKER_DB_PRIVATE_ACCESS
NO_S1_S4_EXECUTION
NO_CANONICAL_STATE_MUTATION
NO_GIT_COMMIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_DIFF_PATH_SET_EXACT_2
EXPORT_INTEGRITY_PASS
```

Success:

```text
34 / 34 PASS
```

Blocked rows remain `BLOCKED_REQUIRED_EVIDENCE`.

# 14. success export

Root documents exactly 12:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
SOURCE_COUPLING_VERIFICATION.md
CANONICAL_AUTHORITY_VERIFICATION.md
PRODUCER_PROVENANCE_VERIFICATION.md
PATCH_VERIFICATION.md
TEST_VERIFICATION.md
GIT_DIFF_VERIFICATION.md
NO_RUNTIME_EXECUTION_VERIFICATION.md
CONTRACT_REVIEW.md
```

Project-relative copies exactly 5:

```text
current Cycle
current Judgment
current done Task
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Success export:

```text
17 total members
16 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == canonical current done Task
```

Blocked export may omit unchanged source copies that were never modified, but must not fabricate a success patch.

# 15. mandatory stop

Stop with bounded report/export on:

```text
baseline mismatch
diagnosis mismatch
no durable predecessor LINK API within allowed scope
unexpected modified path
test/lint/compile failure
runtime/private access attempt
```

# 16. success ceiling

```text
S1 source authority coupling:
CORRECTED_CANDIDATE

current evidence state:
ADMISSION_PENDING

producer provenance:
RUNNING / original producer version / immutable

predecessor linkage:
VERIFIED

runner:
UNCHANGED

private S1 runtime:
NOT_EXECUTED

Browser source acceptance:
HUMAN_PENDING

Git persistence:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
