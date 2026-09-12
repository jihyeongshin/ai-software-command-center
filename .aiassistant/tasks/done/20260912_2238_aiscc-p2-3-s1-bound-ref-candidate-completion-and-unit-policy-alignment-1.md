# 작업지시서: P2-3 S1 bound-ref candidate completion + unit-policy alignment

## meta

- task_id: `20260912_2238_aiscc-p2-3-s1-bound-ref-candidate-completion-and-unit-policy-alignment-1`
- created_at: `2026-09-12T22:38:58+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_REWORK_COMPLETION`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- required_parent: `4096913e9a117bd49bfecdb1ce5ca8de2735d661`
- required_grandparent: `6d41633210f0e556dd4292ee62a8600c6b54215f`
- fresh_ide_executor_chat: `FORBIDDEN`
- executor_session_action: `KEEP_EXISTING_2125_2158_IDE_EXECUTOR_CHAT`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- private_s1_execution_authorized: `No`
- success_ceiling: `S1_BOUND_REF_SOURCE_CANDIDATE_COMPLETE / BROWSER_REVIEW_PENDING`

# 0. session / Python

Continue the existing 2125/2158 IDE Executor chat.
Do not open a new chat.

Use only:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Forbidden:

```text
python
py
WindowsApps alias
PATH Python discovery
```

# 1. purpose

Retain the 2158 five-path partial patch and close only:

```text
A. exact same-shape unrelated ADMISSION_PENDING predecessor negative regression
B. pre-existing unit static-import policy mismatch involving collections.abc
```

Do not restart the source rework from HEAD.

# 2. transport

Verify delivery ZIP/hash using the exact Python executable.
Require three flat safe members.

Place current Task first at:

```text
.aiassistant/tasks/active/20260912_2238_aiscc-p2-3-s1-bound-ref-candidate-completion-and-unit-policy-alignment-1.md
```

Then current Cycle/Judgment with exact hashes:

```text
.aiassistant/records/aiscc/cycles/20260912_2238_aiscc-p2-3-s1-bound-ref-partial-candidate-completion-entry-1.cycle.md
280cb063fd4ebe465a9434229085a0d03197ac5d1b2220ff5b203cb2d7434f88

.aiassistant/reports/aiscc/20260912_2238_aiscc-p2-3-s1-bound-ref-partial-candidate-hold-judgment-1.md
add0e970d1fa9d4a5427e3ba8cb1bd54cd1756d2c889d8cac3cb1997c76670ed
```

# 3. repository baseline

Require:

```text
branch main
HEAD ee623c995cf1c24b4a362834f2d6d1fdf71a30cd
HEAD^ 4096913e9a117bd49bfecdb1ce5ca8de2735d661
HEAD^^ 6d41633210f0e556dd4292ee62a8600c6b54215f
index empty
```

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `7d0c9954b87e945b8c1c3fb66bda2dd54d23d5c3319202ef9fb24aa0ac56f424`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `04ec792c5e6dd4a7c8d2d35b716d1ed1fd569e60bb557532b811bc33dd434946`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `61ae340fa06e3d87d80f3308a240dacc1e0ba132a3b241a2059757830cf6312a`

Before current delivery Git-visible untracked exactly 18:

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

After current Cycle/Judgment placement while current Task is active/ignored:

```text
Git-visible untracked:
20 exact
```

Tracked worktree is intentionally dirty in exactly these five paths with exact current hashes:

- `src/aiscc/workflow/guards.py`  `e7509199bca3b901c7a04b4e5a1d8c23bab217eca5b78a3b9319d10300993cab`
- `src/aiscc/persistence/repository.py`  `ab00af3dd871477da74b83275258aa48a47ba9a7081aad0154a808b6e4f1c089`
- `src/aiscc/scenarios/capture_runner.py`  `0dab27e0ce9ce2da7953188bcb26f288b637a4ba524141be2800b08302a59b18`
- `src/aiscc/scenarios/stockroom_production.py`  `1ca58848a837e1130229c7a0e085df999d04c6041c77bb61098185d342ff14a0`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `909dda0fde3cd061a3f1c2b6ca61b334b60402f77611a5817fa5197061800539`

Any other tracked modification:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

Do not restore the retained five-path patch.

# 4. allowed tracked paths

Maximum allowed modified paths for this Task:

```text
src/aiscc/workflow/guards.py
src/aiscc/persistence/repository.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
tests/unit/scenarios/test_contracts.py
```

At start the sixth path must be clean and byte-equal to HEAD.
Record its HEAD blob and SHA before any edit.

No other path may change.

# 5. unit failure baseline proof

Read exact failing test:

```text
tests/unit/scenarios/test_contracts.py::test_static_module_has_no_execution_or_integration_imports
```

Read the required-HEAD version of:

```text
src/aiscc/scenarios/stockroom_production.py
```

Mechanically prove:

```text
collections.abc import exists at HEAD
the 2158 candidate did not introduce that import
the failure is caused by the test's existing import-policy rule
```

If any fact is false:

```text
UNIT_FAILURE_CLASSIFICATION_MISMATCH
→ STOP
```

# 6. unit-policy intent gate

Determine the exact semantic intent of the failing test from its source and neighboring assertions.

Only if the policy is intended to forbid execution/integration-layer coupling, while allowing ordinary standard-library support,
authorize a narrow correction that treats exactly the existing `collections.abc` dependency as allowed.

Preferred correction:

```text
narrow allowlist adjustment limited to the module/root required for collections.abc
```

Forbidden:

```text
allow all stdlib automatically
remove the test
skip/xfail it
broaden to arbitrary aiscc execution/provider/runtime imports
exclude stockroom_production.py wholesale unless the existing test design clearly uses an explicit module-classification list
```

If the test intent does not support a narrow safe correction:

```text
UNIT_POLICY_DESIGN_AMBIGUOUS
→ STOP before editing test policy
```

# 7. exact unrelated pending regression

The 2158 "unrelated" case used an earlier RUNNING transition and did not satisfy the required negative shape.

Add a regression that constructs:

```text
current:
ADMISSION_PENDING/vN+1

candidate predecessor:
also an admitted RUNNING/vN → ADMISSION_PENDING/vN+1 transition shape

but:
different execution submission and/or execution attempt binding from the producer under verification
```

It must be structurally capable of passing superficial state/version adjacency checks.

Require adapter result:

```text
DENIED
```

before EvidenceCandidate submission.

This test must prove the exact historical G_EXECUTOR_SUBMISSION bound refs prevent cross-producer substitution.

Do not weaken the positive path to make the negative pass.

# 8. patch preservation

Unless section 7 reveals an actual product defect, keep these four production files byte-identical to their 2158 candidate hashes:

```text
src/aiscc/workflow/guards.py
src/aiscc/persistence/repository.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py
```

If the new exact regression fails because of a real source defect, a minimal correction inside the existing five production/test candidate paths is allowed.

Any semantic production change must be described explicitly and revalidated.

# 9. validation

Use exact Python only.

Run:

```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m py_compile
  src/aiscc/workflow/guards.py
  src/aiscc/persistence/repository.py
  src/aiscc/scenarios/capture_runner.py
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py
  tests/unit/scenarios/test_contracts.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -m ruff check
  src/aiscc/workflow/guards.py
  src/aiscc/persistence/repository.py
  src/aiscc/scenarios/capture_runner.py
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py
  tests/unit/scenarios/test_contracts.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q
  tests/integration/scenarios/test_stockroom_capture_runner.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q
  tests/unit
```

Also run:

```text
git diff --check
```

No Docker/PostgreSQL/private runtime.

# 10. success conditions

Require:

```text
targeted integration:
zero failures

unit suite:
zero failures

compile:
PASS

Ruff:
PASS

git diff --check:
PASS
```

The exact same-shape unrelated predecessor regression must have executed and passed, not merely exist.

# 11. Git boundary

No add/commit/push/reset/restore/checkout/stash/clean.

At success before Task move:

```text
index:
empty

modified tracked paths:
subset of exact allowed six
must include retained 2158 five
may include tests/unit/scenarios/test_contracts.py
no others
```

Move Task byte-identically to done.

Final Git-visible untracked exactly:

```text
21

18 predecessors
current Cycle
current Judgment
current done Task
```

# 12. runtime prohibition

Do not access:

```text
Docker
PostgreSQL
private password/runtime root
provider/network runtime
prepare_capture
WorkRun runtime
S1/S2/S3/S4
Replay
```

# 13. contract review

Require exactly 34 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
PREDECESSOR_18_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
RETAINED_DIRTY5_HASHES_EXACT
INDEX_EMPTY
PYTHON_EXECUTABLE_EXACT
UNIT_FAILURE_BASELINE_IMPORT_REPRODUCED
UNIT_POLICY_INTENT_READ_EXACT
COLLECTIONS_ABC_HEAD_PREEXISTING_CONFIRMED
UNIT_POLICY_CHANGE_NARROW_ONLY
NO_EXECUTION_INTEGRATION_IMPORT_WEAKENING
SAME_SHAPE_UNRELATED_PENDING_REGRESSION_ADDED
SAME_SHAPE_UNRELATED_PENDING_REGRESSION_DENIED
POSITIVE_LINK_REGRESSION_STILL_PASS
WRONG_SUBMISSION_REGRESSION_STILL_DENIED
WRONG_ATTEMPT_REGRESSION_STILL_DENIED
WRONG_PRODUCER_VERSION_REGRESSION_STILL_DENIED
REF_ONLY_NON_SUBSTITUTION_STILL_PASS
TARGETED_SCENARIO_PYTEST_PASS
UNIT_REGRESSION_PYTEST_PASS
RUFF_PASS
PY_COMPILE_PASS
GIT_DIFF_CHECK_PASS
PRODUCTION_PATCH_SEMANTICS_PRESERVED
RUNNER_ORDER_UNCHANGED
CURRENT_LINK_PRODUCER_SPLIT_PRESERVED
NO_DOCKER_DB_PRIVATE_ACCESS
NO_S1_S4_EXECUTION
NO_CANONICAL_STATE_MUTATION
NO_GIT_COMMIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_MODIFIED_PATHS_WITHIN_ALLOWED_6
EXPORT_INTEGRITY_PASS
```

Success requires:

```text
34 / 34 PASS
```

# 14. success export

Root docs exactly 12:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
PARTIAL_PATCH_BASELINE_VERIFICATION.md
UNIT_POLICY_VERIFICATION.md
UNRELATED_PENDING_REGRESSION_VERIFICATION.md
TEST_VERIFICATION.md
PATCH_VERIFICATION.md
GIT_DIFF_VERIFICATION.md
NO_RUNTIME_EXECUTION_VERIFICATION.md
CONTRACT_REVIEW.md
```

Include project-relative copies of:

```text
current Cycle
current Judgment
current done Task
the five retained candidate paths
tests/unit/scenarios/test_contracts.py
```

Success export:

```text
21 total members
20 non-self manifest rows
one top-level
CRC PASS
folder/archive byte equality
TASK.md == canonical done Task
```

# 15. success ceiling

```text
S1 bound-ref source candidate:
COMPLETE_CANDIDATE

canonical bound-ref contract:
IMPLEMENTED

same-shape cross-producer negative:
PROVED_DENIED

unit regression:
PASS

private S1 runtime:
NOT_EXECUTED

Browser source acceptance:
HUMAN_PENDING

Git persistence:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
