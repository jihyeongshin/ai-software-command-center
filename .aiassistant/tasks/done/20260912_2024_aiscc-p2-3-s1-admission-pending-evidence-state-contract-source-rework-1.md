# 작업지시서: P2-3 S1 ADMISSION_PENDING evidence-state contract source rework

## meta

- task_id: `20260912_2024_aiscc-p2-3-s1-admission-pending-evidence-state-contract-source-rework-1`
- created_at: `2026-09-12T20:24:31+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_REWORK / S1_ORCHESTRATION_STATE_CONTRACT`
- evidence_profile: `STANDARD`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- required_parent: `4096913e9a117bd49bfecdb1ce5ca8de2735d661`
- required_grandparent: `6d41633210f0e556dd4292ee62a8600c6b54215f`
- fresh_ide_executor_chat: `REQUIRED`
- success_ceiling: `S1_SOURCE_DEFECT_CORRECTED_CANDIDATE / BROWSER_REVIEW_PENDING`
- private_s1_execution_authorized: `No`

# 0. purpose

Correct the source-level state-contract defect found before S1 runtime began.

Current production path:

```text
StockroomCaptureRunner.run
  → durable RUNNING_TO_ADMISSION_PENDING
  → StockroomCaptureOwnerAdapter.submit_runtime_evidence
      → _current(..., WorkflowState.RUNNING)  # stale precondition
```

Canonical intended path:

```text
RUNNING
→ ADMISSION_PENDING
→ evidence admission/evaluation
→ Judgment
→ ACCEPTED
```

The correction is **not** to reorder the runner.
The correction is to align `submit_runtime_evidence` current-state authority to `ADMISSION_PENDING`.

# 1. transport

Start this Task in a fresh IDE Executor chat.

Verify Short Prompt ZIP filename/SHA-256.
Require exactly three flat members.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_2024_aiscc-p2-3-s1-admission-pending-evidence-state-contract-source-rework-1.md
```

Require byte equality / ignored.

Then place:

```text
.aiassistant/records/aiscc/cycles/20260912_2024_aiscc-p2-3-s1-source-state-contract-defect-rework-entry-1.cycle.md
SHA-256:
8c9ca5c06d658e9e2723ee70b2b54b999801cf17494543480caf7743840e7a44

.aiassistant/reports/aiscc/20260912_2024_aiscc-p2-3-s1-source-state-contract-defect-confirmed-judgment-1.md
SHA-256:
c8a921efc6112c2bbd8532ed0869e08e9c1f1eebea4121805f0c839ad3bbf0c2
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

Before current delivery Git-visible untracked exactly these 6 predecessor artifacts:

- `.aiassistant/tasks/done/20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1.md`  `0668ed1fb71ce57f6b87dacb91c810f7505596eb6efe835841c019f3a2d51ecd`
- `.aiassistant/records/aiscc/cycles/20260912_1749_aiscc-p2-3-cut-c-persisted-private-s1-execution-entry-1.cycle.md`  `75fe2a744d010e327ff2d549aa998e2e64e0449735d50eec69a4fd6a183044ad`
- `.aiassistant/reports/aiscc/20260912_1749_aiscc-p2-3-cut-c-persistence-final-acceptance-private-s1-authorization-judgment-1.md`  `6457922c2520c2255edf9574b1c68c3ed633c3615e80be5c95c7e04f9e5961ed`
- `.aiassistant/tasks/done/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-retry-1.md`  `f3fbe8fed5d2dfcc6ac6b4586567b410e64653f648943f162219b11648ab3819`
- `.aiassistant/records/aiscc/cycles/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocked-retry-entry-1.cycle.md`  `1bb88d04b2e567a9b11ab8fb99449571696a5e039571cef6438fa62bb3fea870`
- `.aiassistant/reports/aiscc/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocker-hold-judgment-1.md`  `ee9436791b8595333090eb2a06b295ef4b3b87f620894756fea0a97176ebd25d`

After current Cycle/Judgment placement while current Task is active/ignored:

```text
Git-visible untracked:
8 exact

six predecessors
current Cycle
current Judgment
```

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `7d0c9954b87e945b8c1c3fb66bda2dd54d23d5c3319202ef9fb24aa0ac56f424`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `04ec792c5e6dd4a7c8d2d35b716d1ed1fd569e60bb557532b811bc33dd434946`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `61ae340fa06e3d87d80f3308a240dacc1e0ba132a3b241a2059757830cf6312a`

Any unexpected Git-visible path or tracked delta:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 3. exact source baseline

Before mutation require:

```text
src/aiscc/scenarios/stockroom_production.py
SHA-256:
685e2ec549473e167ed1fe4d7de1050d7a53a449d1d278dcdb3439a471478f1f

src/aiscc/scenarios/capture_runner.py
SHA-256:
600de0a4b0e718f02ab2e1907b7be62b2c4a23756559fdf99cb4cd55fb80b3d2

tests/integration/scenarios/test_stockroom_capture_runner.py
SHA-256:
373f9d5bc6f260785cdf943aa649ce99ab5826e8ae09dd2982c18db09459fbf5
```

All three must be tracked at HEAD with raw worktree bytes equal HEAD bytes.

Read exact current source around:

```text
StockroomCaptureRunner.run
StockroomCaptureOwnerAdapter.submit_runtime_evidence
StockroomCaptureOwnerAdapter._current
StockroomCaptureOwnerAdapter.transition
```

Read canonical orchestration/security/evidence rules needed to confirm the authority boundary.

# 4. mandatory static defect reproduction

Before editing, mechanically prove:

```text
runner:
RUNNING_TO_ADMISSION_PENDING transition call occurs before submit_runtime_evidence call

submit_runtime_evidence:
calls _current(prepared, WorkflowState.RUNNING)

_current:
fails closed on authoritative state mismatch
```

Require current durable transition verification confirms successful `RUNNING_TO_ADMISSION_PENDING` means the
authoritative state is `ADMISSION_PENDING`, not a local label.

If this static defect cannot be reproduced exactly:

```text
SOURCE_DEFECT_BASELINE_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 5. canonical semantic gate

Confirm from canonical baseline:

```text
RUNNING → ADMISSION_PENDING:
executor submission / G_EXECUTOR_SUBMISSION

ADMISSION_PENDING:
submission/evidence review state

ADMISSION_PENDING → ACCEPTED:
G_EVIDENCE
G_HUMAN_NOT_REQUIRED
G_JUDGMENT_ACCEPTED
```

Therefore runtime evidence admission must be compatible with authoritative `ADMISSION_PENDING`.

Do not alter canonical rules.

# 6. exact allowed tracked changes

Modify exactly two tracked paths:

```text
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Do not modify the runner or any other source/config/test/state file.

## 6.1 production correction

In `StockroomCaptureOwnerAdapter.submit_runtime_evidence`, change only the stale authoritative expected state:

```text
WorkflowState.RUNNING
→
WorkflowState.ADMISSION_PENDING
```

The exact implementation may include formatting/context necessary for the existing code style, but semantic change is
limited to this expected-state correction.

Preserve:

```text
_current implementation
AuthorityConflictError fail-closed behavior
evidence candidate validation
same-attempt/source/checkpoint binding
transition methods
Judgment handling
security checks
all other adapter methods
```

## 6.2 forbidden source workarounds

Do not:

```text
move submit_runtime_evidence before RUNNING_TO_ADMISSION_PENDING
remove or bypass _current
accept multiple states
catch-and-ignore AuthorityConflictError
forge a local state
change transition matrix
change EvidenceCheckpoint semantics
change security action eligibility
add runtime special-case for S1
modify canonical governance state
```

# 7. focused regression test

Add focused regression coverage in:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py
```

The regression must prove the actual source-owned boundary, not string matching only.

At minimum prove:

```text
1. normal runner path admits RUNNING_TO_ADMISSION_PENDING before runtime evidence submission
2. runtime-evidence owner observes authoritative ADMISSION_PENDING at submission time
3. stale RUNNING expectation would fail the same boundary
4. corrected path does not bypass _current/fail-closed authority
5. evidence submission remains same run/attempt and does not reorder normal execution stages
```

Use existing test fixtures/fakes/authorities where possible.

Do not add a product-only fake path that production does not use.

# 8. targeted validation

Use the repository `.venv` actual Python, not WindowsApps alias.

Run exactly or equivalent repository-supported forms:

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

If a named test directory is absent, do not invent a substitute silently.
Report the exact repository-supported focused scope and stop for Browser review if the requested regression scope cannot be
represented.

Do not run private S1, Docker, PostgreSQL, provider/network, or browser QA.

# 9. post-change static proof

After edits, mechanically prove:

```text
runner transition order:
unchanged

submit_runtime_evidence authoritative expected state:
ADMISSION_PENDING

_current fail-closed implementation:
byte/AST semantics unchanged except caller expected-state argument

no other production adapter behavior changed
```

Compare `git diff --` for the two exact paths.

Require no unrelated formatting sweep.

# 10. Git boundary

No staging or commit.

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

At success before Task movement require:

```text
tracked modified paths:
exactly 2

src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py

index:
empty

Git-visible untracked:
8 exact
```

Move current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_2024_aiscc-p2-3-s1-admission-pending-evidence-state-contract-source-rework-1.md
→
.aiassistant/tasks/done/20260912_2024_aiscc-p2-3-s1-admission-pending-evidence-state-contract-source-rework-1.md
```

Final Git-visible untracked:

```text
9 exact

six predecessor artifacts
current Cycle
current Judgment
current done Task
```

Tracked modified paths remain exactly two for Browser review.

# 11. contract review

Require exactly 27 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
PREDECESSOR_6_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
ADAPTER_BASELINE_HASH_EXACT
RUNNER_BASELINE_HASH_EXACT
REGRESSION_TEST_BASELINE_HASH_EXACT
SOURCE_DEFECT_REPRODUCED_STATIC
CANONICAL_ADMISSION_PENDING_SEMANTICS_CONFIRMED
MODIFIED_PATH_SET_EXACT_2
ADAPTER_EXPECTED_STATE_ADMISSION_PENDING
RUNNER_TRANSITION_ORDER_UNCHANGED
CURRENT_FAIL_CLOSED_CHECK_UNCHANGED
NO_AUTHORITY_WEAKENING
REGRESSION_TEST_ADDED
REGRESSION_PROVES_POST_TRANSITION_EVIDENCE_STATE
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

Require success:

```text
27 / 27 PASS
```

# 12. success export

Target:

```text
.aiassistant/reports/target/20260912_2024_aiscc-p2-3-s1-admission-pending-evidence-state-contract-source-rework-1/
```

Root documents exactly 11:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
SOURCE_DEFECT_VERIFICATION.md
CANONICAL_SEMANTIC_VERIFICATION.md
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
16 total members
15 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == canonical current done Task
```

Do not include predecessor result ZIPs, helper scripts, private/runtime files, Docker output or DB content.

# 13. mandatory stop

Stop with bounded report/export after:

```text
baseline mismatch
static defect no longer reproduces
canonical semantic ambiguity
unexpected modified path
test failure
lint/compile failure
attempted private/runtime access
```

Do not broaden source scope.

# 14. success ceiling

```text
S1 source defect:
CORRECTED_CANDIDATE

production adapter expected evidence state:
ADMISSION_PENDING

runner ordering:
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
