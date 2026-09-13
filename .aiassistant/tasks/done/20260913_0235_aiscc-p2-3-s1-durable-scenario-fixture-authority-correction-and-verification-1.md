# 작업지시서: P2-3 S1 durable scenario fixture authority correction and verification

## meta

- task_id: `20260913_0235_aiscc-p2-3-s1-durable-scenario-fixture-authority-correction-and-verification-1`
- created_at: `2026-09-13T02:35:57+09:00`
- work_type: `TEST_FIXTURE_REWORK_AND_DURABLE_VERIFICATION`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- required_parent: `35cee94a92d1f12801576ef48038196922687f42`
- required_grandparent: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- source_write_authorized: `No`
- test_write_authorized: `Yes / exact one path`
- retained_private_runtime_access_authorized: `No`
- isolated_test_postgresql_authorized: `Yes`
- accepted_predecessor_result_zip_sha256: `9a60f9d9ab0849eb1b7cb1acdab815272934acc80bdb003f5c5cbae75da7fda1`
- success_ceiling: `EXECUTION_START_SOURCE_CANDIDATE_DURABLY_VERIFIED / BROWSER_REVIEW_PENDING`

# 0. purpose

Preserve the 0138 product source candidate exactly.

Correct only the stale S2 test fixture that attempts generic issuance of `G_EXECUTOR_SUBMISSION`, then rerun the missing durable PostgreSQL verification.

# 1. Python / transport

Use only:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Forbidden: `python`, `py`, WindowsApps alias, PATH Python discovery.

Verify delivery ZIP/hash and exactly three flat safe members.

Place current Task first:

```text
.aiassistant/tasks/active/20260913_0235_aiscc-p2-3-s1-durable-scenario-fixture-authority-correction-and-verification-1.md
```

Then place:

```text
.aiassistant/records/aiscc/cycles/20260913_0235_aiscc-p2-3-s1-durable-scenario-fixture-correction-verification-entry-1.cycle.md
SHA-256 ad3e00ea8c5da679441e141c393f6cf4b07378ffebd4dcd2698ed32e0bc54587

.aiassistant/reports/aiscc/20260913_0235_aiscc-p2-3-s1-durable-scenario-fixture-authority-defect-judgment-1.md
SHA-256 061a414f56b80bd0b005f65c3c31e972d96f9f494355c53de6f2540cde541807
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

Before delivery Git-visible untracked exactly 15:

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

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `02b7a77d3f29d7ee3878157470020ab83b377ba0343867ab81ec6e82d1a9190b`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `9ca1b1a24f3f73c2f81d3342442cf0462b58fecdba2dbccc33509b0d4039ab71`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `7315a943ad4ed82757f4398d9613f3a6f773755f3496fa1e8fa816123422ea84`

Require exact current dirty candidate:

```text
src/aiscc/scenarios/stockroom_production.py
SHA-256 c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3

tests/integration/scenarios/test_stockroom_capture_runner.py
SHA-256 f2bb84980c89f3dcdcd54bdfe6c283343bc43b978261c50aad8e20f09fb95616
```

No other tracked dirt.

After current Cycle/Judgment placement while Task is active/ignored:

```text
Git-visible untracked = 17 exact
```

# 3. strict retained-private boundary

Do not inspect/connect/exec/stop/restart/mutate retained private S1 PostgreSQL, volume, password file, runtime root, or 0036 WorkRun/attempt.

Only a new isolated test PostgreSQL instance is authorized.

# 4. mandatory stale-fixture reproduction

Before test write, mechanically prove the 0206 failure still exists in the current test candidate:

```text
S2 setup manually advances:
NONE→READY
READY→RUNNING
RUNNING→ADMISSION_PENDING

guard loop uses generic:
application.p1_4_guard_authority.issue(...)

for every P1_4_SYSTEM guard

RUNNING→ADMISSION_PENDING includes:
G_EXECUTOR_SUBMISSION

generic issue(G_EXECUTOR_SUBMISSION):
rejected by current P1_4GuardAuthority contract
```

If this does not reproduce:

```text
TEST_FIXTURE_BASELINE_MISMATCH
→ STOP before edit
```

# 5. exact test-only correction

Modify only:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Do not modify product source.

For the S2 `RUNNING→ADMISSION_PENDING` setup only, construct a test-only authentic `ExecutionSubmissionRef` that is:

```text
submission_id:
unique bounded test ID

execution_attempt_id:
the exact S2 capture attempt_id

work_run_id:
the exact S2 run_id

task_contract_id/version:
exact values from the S2 enrollment/request

state:
RUNNING

state_version:
2

status:
EXECUTOR_COMPLETED

event_range_hash:
valid deterministic SHA-256 test value

issuer_ref:
the exact application.execution_reference_authority issuer
```

Register/authenticate it through the existing `application.execution_reference_authority` API.

Then issue `G_EXECUTOR_SUBMISSION` only through:

```text
application.p1_4_guard_authority.issue_from_execution_ref(
    guard_id=G_EXECUTOR_SUBMISSION,
    execution_ref=<authentic registered submission>,
    verifier=application.execution_reference_authority,
    request=<exact S2 transition request>,
)
```

All other S2 guards keep their existing semantics.

Do not:

```text
call generic issue() for G_EXECUTOR_SUBMISSION
weaken P1_4GuardAuthority
fake TrustedGuardFact directly
copy arbitrary bound_refs
reuse the S1 producer
change production source
run provider/tool execution merely to prepare S2 fixture
```

The fixture may use the existing test-only authority registration API; it must remain internally authentic under current guard semantics.

# 6. source immutability

Throughout the Task require:

```text
src/aiscc/scenarios/stockroom_production.py
SHA-256 c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3
```

Any product source byte change:

```text
UNAUTHORIZED_SOURCE_MUTATION
→ STOP
```

# 7. isolated PostgreSQL provisioning

Use exact locally available PostgreSQL image:

```text
sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94
```

Create exactly one new isolated container:

```text
aiscc-p2-3-source-verification-postgres-0235-v1
```

Require:

```text
127.0.0.1 only
Docker-assigned ephemeral port
database aiscc_test
role aiscc_test
fresh ephemeral password
no named persistent volume
no retained-private resource/network reuse
```

If exact container name preexists: STOP.

Password/credential URL must not enter reports/export.

# 8. schema bootstrap

Use the already verified repository-owned Alembic path from 0206:

```text
alembic.ini
migrations/env.py
python -m alembic upgrade head
```

with the exact Python executable.

Require current migration head:

```text
20260901_0008
```

No custom DDL or `metadata.create_all()` substitute.

# 9. durable scenario verification

Set `AISCC_TEST_DATABASE_URL` process-locally and run:

```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/scenarios/test_stockroom_capture_runner.py
```

Require:

```text
zero failures
zero required DB skips
```

The production-owner test must reach and PASS the S1 lifecycle block proving:

```text
prepared attempt NOT_STARTED
READY→RUNNING admitted
durable EXECUTION_STARTED exactly once
attempt RUNNING
causal state RUNNING
causal version exact
authoritative current attempt refreshed
downstream service no longer observes NOT_STARTED
```

Also require the corrected S2 setup reaches its evidence/judgment assertions under authentic `G_EXECUTOR_SUBMISSION`.

# 10. provider persistence

Run:

```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/providers/test_execution_persistence.py
```

Require exactly:

```text
23 executed
23 passed
```

If discovery count differs from 23, STOP and report exact count.

# 11. workflow handoff

Run:

```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/providers/test_workflow_handoff.py
```

Require zero failures.

# 12. source/unit validation

Run:

```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m py_compile
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -m ruff check
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/unit

git diff --check
```

# 13. failure behavior

If any durable regression fails:

```text
do not edit product source
do not perform a second speculative test correction
capture safe failure evidence
remove only the isolated test container/storage
STOP_WITH_REPORT_EXPORT
```

A second test-only edit is not authorized without Browser review.

# 14. isolated DB teardown

Stop/remove only:

```text
aiscc-p2-3-source-verification-postgres-0235-v1
```

Remove Task-created anonymous/tmp storage.

No broad Docker cleanup/prune.

Verify exact test container/storage residue is absent.

# 15. final workspace

Require:

```text
HEAD unchanged
index empty
canonical state hashes unchanged

tracked dirty:
exactly two paths

src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

The product source hash remains `c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3`.
Record the new test-file SHA after correction.

Before Task move Git-visible untracked = 17 exact.

Move current Task byte-identically active→done.

Final Git-visible untracked = 18 exact.

# 16. contract review

Require exactly 40 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_EXACT
PREDECESSOR_15_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
PRODUCT_SOURCE_CANDIDATE_HASH_EXACT
TEST_CANDIDATE_BASELINE_HASH_EXACT
INDEX_EMPTY
ONLY_CANDIDATE_2_TRACKED_DIRTY
PYTHON_EXECUTABLE_EXACT
RETAINED_PRIVATE_RESOURCES_NOT_ACCESSED
S2_STALE_GENERIC_G_EXECUTOR_SUBMISSION_REPRODUCED
TEST_ONLY_MODIFICATION_EXACT
G_EXECUTOR_SUBMISSION_GENERIC_ISSUE_REMOVED_FROM_S2_SETUP
S2_VERIFIED_EXECUTION_SUBMISSION_REF_CREATED
S2_EXECUTION_REF_ISSUER_EXACT
S2_G_EXECUTOR_SUBMISSION_ISSUED_FROM_VERIFIED_REF
S2_OTHER_GUARD_SEMANTICS_UNCHANGED
PRODUCTION_GUARD_AUTHORITY_NOT_WEAKENED
PRODUCT_SOURCE_BYTES_UNCHANGED
ISOLATED_POSTGRESQL_PROVISIONED_EXACT
TEST_DB_SCHEMA_HEAD_EXACT
SCENARIO_DURABLE_REGRESSION_EXECUTED
SCENARIO_DURABLE_REGRESSION_PASS
SCENARIO_S1_LIFECYCLE_ASSERTIONS_REACHED
SCENARIO_SUITE_ZERO_REQUIRED_SKIPS
PROVIDER_PERSISTENCE_23_EXECUTED
PROVIDER_PERSISTENCE_23_PASS
WORKFLOW_HANDOFF_REGRESSION_PASS
FULL_UNIT_REGRESSION_PASS
RUFF_PASS
PY_COMPILE_PASS
GIT_DIFF_CHECK_PASS
NO_SOURCE_STATE_MUTATION
NO_S1_RUNTIME_RECOVERY
ISOLATED_POSTGRESQL_REMOVED
NO_TEST_DB_RESIDUE
FINAL_INDEX_EMPTY
FINAL_DIRTY_PATHS_EXACT_2
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
EXPORT_INTEGRITY_PASS
```

Success requires `40 / 40 PASS`.

# 17. success export

Root docs exactly 12:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
TEST_FIXTURE_CORRECTION_VERIFICATION.md
PRODUCT_SOURCE_IMMUTABILITY.md
ISOLATED_POSTGRESQL_VERIFICATION.md
TEST_DB_SCHEMA_VERIFICATION.md
DURABLE_SCENARIO_TEST_VERIFICATION.md
PROVIDER_PERSISTENCE_VERIFICATION.md
TEST_DB_TEARDOWN_VERIFICATION.md
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
TASK.md == canonical done Task
```

# 18. success ceiling

```text
execution-start lifecycle product source candidate:
DURABLY_VERIFIED

test fixture:
CANONICAL_AUTHORITY_ALIGNED

0036 durable S1 HOLD:
PRESERVED / UNTOUCHED

private S1 recovery:
NOT AUTHORIZED

Browser source acceptance:
HUMAN_PENDING

Git persistence:
NOT PERFORMED

P2-3:
IN_PROGRESS
```
