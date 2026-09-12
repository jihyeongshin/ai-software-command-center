# 작업지시서: P2-3 S1 static-module policy + bound-ref candidate finalization

## meta

- task_id: `20260912_2300_aiscc-p2-3-s1-static-module-policy-and-bound-ref-candidate-finalization-1`
- created_at: `2026-09-12T23:00:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_CANDIDATE_FINALIZATION`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- required_parent: `4096913e9a117bd49bfecdb1ce5ca8de2735d661`
- required_grandparent: `6d41633210f0e556dd4292ee62a8600c6b54215f`
- fresh_ide_executor_chat: `FORBIDDEN`
- executor_session_action: `KEEP_EXISTING_IDE_EXECUTOR_CHAT`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- private_s1_execution_authorized: `No`
- success_ceiling: `S1_BOUND_REF_SOURCE_CANDIDATE_COMPLETE / BROWSER_REVIEW_PENDING`

# 0. session / Python

Continue the current IDE Executor chat.
Do not open a new chat.

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

# 1. purpose

Retain the existing 2158 five-path partial source candidate and close the two remaining gaps:

```text
1. replace the stale all-scenario glob unit policy with the exact frozen static-module set
2. add and execute the exact same-shape cross-producer negative regression
```

# 2. transport

Verify this delivery ZIP/hash with the exact Python executable.
Require exactly three flat safe members.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_2300_aiscc-p2-3-s1-static-module-policy-and-bound-ref-candidate-finalization-1.md
```

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_2300_aiscc-p2-3-s1-static-module-policy-defined-candidate-finalization-entry-1.cycle.md
SHA-256:
a7677d92239827a155adfa52d530cc9bf6bb853c253f4613d09361d5631c83a8

.aiassistant/reports/aiscc/20260912_2300_aiscc-p2-3-s1-static-module-policy-definition-judgment-1.md
SHA-256:
f5010fb69514816ddc3a5749c3375d0711d6d15973c717af29c620aac8a05275
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

Before current delivery Git-visible untracked exactly 24:

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

After current Cycle/Judgment placement while current Task remains active/ignored:

```text
Git-visible untracked:
26 exact
```

Tracked dirty paths at start must be exactly these five, with exact hashes:

- `src/aiscc/workflow/guards.py`  `e7509199bca3b901c7a04b4e5a1d8c23bab217eca5b78a3b9319d10300993cab`
- `src/aiscc/persistence/repository.py`  `ab00af3dd871477da74b83275258aa48a47ba9a7081aad0154a808b6e4f1c089`
- `src/aiscc/scenarios/capture_runner.py`  `0dab27e0ce9ce2da7953188bcb26f288b637a4ba524141be2800b08302a59b18`
- `src/aiscc/scenarios/stockroom_production.py`  `1ca58848a837e1130229c7a0e085df999d04c6041c77bb61098185d342ff14a0`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `909dda0fde3cd061a3f1c2b6ca61b334b60402f77611a5817fa5197061800539`

The unit-policy test must be clean at HEAD:

```text
tests/unit/scenarios/test_contracts.py
SHA-256:
d72b4f2acccefb8b0dd5069005b49d21f90a12424adf79e8e5de4906171b2784
```

Any other tracked modification:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 4. allowed modified paths

Maximum allowed tracked modified paths:

```text
src/aiscc/workflow/guards.py
src/aiscc/persistence/repository.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
tests/unit/scenarios/test_contracts.py
```

No other path may change.

# 5. frozen static-module policy

Modify only the membership selection of:

```text
test_static_module_has_no_execution_or_integration_imports
```

The exact static module set is:

```text
src/aiscc/scenarios/__init__.py
src/aiscc/scenarios/catalog.py
src/aiscc/scenarios/models.py
```

The test must scan exactly these three files.

Do not use:

```text
glob("*.py")
```

for this static policy.

Prefer an explicit immutable tuple/list of exact paths or basenames.

The existing allowed import-root set remains unchanged:

```text
__future__
aiscc.scenarios
dataclasses
hashlib
json
jsonschema
pathlib
pydantic
re
typing
```

Do not add `collections`, `collections.abc`, `aiscc.workflow`, `aiscc.providers`, `aiscc.evidence`,
`aiscc.persistence`, `sqlalchemy`, or broad stdlib/runtime exceptions.

Do not delete, skip or xfail the test.

# 6. policy boundary regression

The unit test must mechanically prove membership is exactly three.

At minimum ensure a future accidental `glob("*.py")` broadening cannot silently return.

The following current modules are explicitly not members of this static import-policy test:

```text
capture_runner.py
composition.py
driver.py
enrollment.py
runtime_models.py
stockroom_production.py
```

This does not grant them unrestricted imports; it only means this specific static-contract test does not own them.

# 7. exact same-shape cross-producer regression

Extend:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py
```

with a regression where:

```text
current:
ADMISSION_PENDING/vN+1

historical candidate predecessor:
ADMITTED RUNNING/vN → ADMISSION_PENDING/vN+1

shape:
same run/state/version/target form required by the positive path

but G_EXECUTOR_SUBMISSION bound refs:
different submission_id and/or execution_attempt_id from the producer ref being verified
```

The case must be capable of passing superficial state/version adjacency checks.

Required result:

```text
DENIED
```

before runtime EvidenceCandidate submission.

The denial must be caused by exact producer-link mismatch, not by unrelated invalid setup.

# 8. retained production patch

Unless section 7 exposes a real product defect, these four production paths must remain byte-identical to their 2158 candidate hashes:

```text
src/aiscc/workflow/guards.py
src/aiscc/persistence/repository.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py
```

If the exact regression exposes a real defect, a minimal fix inside the six allowed paths is authorized.
Report any production-byte change explicitly.

Preserve:

```text
CURRENT = ADMISSION_PENDING/current version
PRODUCER = RUNNING/original producer version
LINK = exact historical G_EXECUTOR_SUBMISSION submission+attempt binding
ExecutionSubmissionRef != EvidenceCandidate != AdmittedEvidence != G_EVIDENCE
runner transition order unchanged
```

# 9. validation

Use only the exact Python executable.

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
  tests/unit/scenarios/test_contracts.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q
  tests/integration/scenarios/test_stockroom_capture_runner.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q
  tests/unit

git diff --check
```

No Docker/PostgreSQL/private runtime.

# 10. required test outcomes

Success requires zero failures for all executed pytest commands.

The same-shape cross-producer negative must be observed executing and passing.

Do not substitute test existence for execution evidence.

# 11. Git boundary

No:

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
index:
empty

modified tracked paths:
subset of exact allowed six
must include the retained five
must include tests/unit/scenarios/test_contracts.py
no others
```

Move current Task byte-identically to done.

Final Git-visible untracked:

```text
27 exact

24 predecessors
current Cycle
current Judgment
current done Task
```

# 12. runtime prohibition

Do not access:

```text
Docker
PostgreSQL
private password file
private runtime root
provider/network runtime
prepare_capture
WorkRun runtime creation
S1/S2/S3/S4
Replay
```

# 13. contract review

Require exactly 38 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
PREDECESSOR_24_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
RETAINED_DIRTY5_HASHES_EXACT
UNIT_POLICY_HEAD_HASH_EXACT
INDEX_EMPTY
PYTHON_EXECUTABLE_EXACT
STATIC_MODULE_SET_EXACT_3
STATIC_IMPORT_ROOT_ALLOWLIST_UNCHANGED
STATIC_POLICY_NO_GLOB_ALL_SCENARIOS
STATIC_POLICY_SCANS_INIT
STATIC_POLICY_SCANS_CATALOG
STATIC_POLICY_SCANS_MODELS
STATIC_POLICY_EXCLUDES_RUNTIME_COMPOSITION_MODULES
SAME_SHAPE_CROSS_PRODUCER_REGRESSION_ADDED
SAME_SHAPE_CROSS_PRODUCER_REGRESSION_DENIED
POSITIVE_LINK_REGRESSION_PASS
WRONG_SUBMISSION_REGRESSION_DENIED
WRONG_ATTEMPT_REGRESSION_DENIED
WRONG_PRODUCER_VERSION_REGRESSION_DENIED
REF_ONLY_NON_SUBSTITUTION_PASS
TARGETED_CONTRACT_TEST_PASS
TARGETED_SCENARIO_PYTEST_PASS
FULL_UNIT_PYTEST_PASS
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

Success:

```text
38 / 38 PASS
```

# 14. success export

Root docs exactly 13:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
STATIC_MODULE_POLICY_VERIFICATION.md
BOUND_REF_CONTRACT_VERIFICATION.md
HISTORICAL_PROVENANCE_VERIFICATION.md
CURRENT_PRODUCER_LINK_VERIFICATION.md
CROSS_PRODUCER_REGRESSION_VERIFICATION.md
TEST_VERIFICATION.md
PATCH_VERIFICATION.md
GIT_DIFF_VERIFICATION.md
CONTRACT_REVIEW.md
```

Project-relative copies exactly 9:

```text
current Cycle
current Judgment
current done Task
src/aiscc/workflow/guards.py
src/aiscc/persistence/repository.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
tests/unit/scenarios/test_contracts.py
```

Success export:

```text
22 total members
21 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == canonical done Task
```

# 15. success ceiling

```text
static scenario module policy:
DEFINED / EXACT_3

bound-ref source candidate:
COMPLETE_CANDIDATE

same-shape cross-producer negative:
PROVED_DENIED

unit suite:
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
