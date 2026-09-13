# 작업지시서: P2-3 S1 execution-start durable PostgreSQL verification

## meta

- task_id: `20260913_0206_aiscc-p2-3-s1-execution-start-durable-postgresql-verification-1`
- created_at: `2026-09-13T02:06:56+09:00`
- work_type: `DURABLE_INTEGRATION_VERIFICATION`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- required_parent: `35cee94a92d1f12801576ef48038196922687f42`
- required_grandparent: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- source_write_authorized: `No`
- retained_private_runtime_access_authorized: `No`
- isolated_test_postgresql_authorized: `Yes`
- runtime_recovery_authorized: `No`
- accepted_predecessor_result_zip_sha256: `e9dcc6cb688a3a75b39e59d47b951c37664c9b557fabe991c39a603fe6d32395`
- success_ceiling: `EXECUTION_START_SOURCE_CANDIDATE_DURABLY_VERIFIED / BROWSER_REVIEW_PENDING`

# 0. purpose

Preserve the exact 0138 two-path candidate and close only its missing PostgreSQL-backed regression evidence.

Do not modify source/tests.
Do not access the retained private S1 runtime.

# 1. Python / transport

Use only:
```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Forbidden: `python`, `py`, WindowsApps alias, PATH Python discovery.

Verify delivery ZIP/hash and exactly three flat safe members.

Place current Task first:
```text
.aiassistant/tasks/active/20260913_0206_aiscc-p2-3-s1-execution-start-durable-postgresql-verification-1.md
```

Then place:
```text
.aiassistant/records/aiscc/cycles/20260913_0206_aiscc-p2-3-s1-execution-start-durable-verification-entry-1.cycle.md
SHA-256 fafebcfa2f981f00af4d40d0b99c0eab0030e372f9c559ea0aac9ca285aec488

.aiassistant/reports/aiscc/20260913_0206_aiscc-p2-3-s1-execution-start-source-candidate-durable-proof-required-judgment-1.md
SHA-256 3c3f4d5031ced700a2ac679cdf2380384522884b2c1cf5bef10f01bea3773126
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

Before delivery Git-visible untracked exactly 12:
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

Canonical state hashes:
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `02b7a77d3f29d7ee3878157470020ab83b377ba0343867ab81ec6e82d1a9190b`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `9ca1b1a24f3f73c2f81d3342442cf0462b58fecdba2dbccc33509b0d4039ab71`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `7315a943ad4ed82757f4398d9613f3a6f773755f3496fa1e8fa816123422ea84`

Tracked dirty exactly:
- `src/aiscc/scenarios/stockroom_production.py`  `c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `f2bb84980c89f3dcdcd54bdfe6c283343bc43b978261c50aad8e20f09fb95616`

After current Cycle/Judgment placement while Task is active/ignored:
```text
Git-visible untracked = 14 exact
```

# 3. retained-private boundary

Do not inspect/connect/exec/stop/restart/mutate:
```text
aiscc-p2-3-private-postgres-v1
aiscc-p2-3-private-postgres-data-v1
aiscc_private_capture
private password file
private runtime root
0036 exact S1 WorkRun/attempt
```

Do not reuse the retained private PostgreSQL host port.

# 4. identify canonical test-DB bootstrap

Read current tracked test/migration configuration and identify one unambiguous repository-owned mechanism that prepares the PostgreSQL schema used by `AISCC_TEST_DATABASE_URL` tests.

Required migration head:
```text
20260901_0008
```

Do not invent DDL or substitute `metadata.create_all()` unless that is explicitly the repository's existing test contract.

If ambiguous:
```text
TEST_DB_BOOTSTRAP_CONTRACT_AMBIGUOUS
→ STOP before Docker provisioning
```

# 5. isolated PostgreSQL

Use exact locally available image:
```text
sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94
```

Create exactly one isolated test container:
```text
aiscc-p2-3-source-verification-postgres-0138-v1
```

Require:
```text
publish 127.0.0.1 only
Docker-assigned ephemeral host port
database aiscc_test
role aiscc_test
fresh random ephemeral password
no persistent named volume
no retained-private network/resource reuse
```

If that exact verification container already exists before provisioning:
```text
TEST_DB_RESIDUE_PREEXISTS
→ STOP
```

The ephemeral password must not be written to repo/governance/report/export.

# 6. readiness and schema

Wait for only the isolated container to become ready.

Resolve its own ephemeral localhost port.

Construct `AISCC_TEST_DATABASE_URL` only in process/environment for test commands; do not print it.

Apply the exact repository-owned bootstrap from section 4 and verify migration head `20260901_0008`.

# 7. scenario durable regression

Run:
```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/scenarios/test_stockroom_capture_runner.py
```

Require zero failures and:
```text
test_production_owner_graph_and_bounded_running_prefix = EXECUTED / PASS
no required PostgreSQL-backed skip
```

Durable proof must cover:
```text
prepared NOT_STARTED
READY→RUNNING admitted
one durable EXECUTION_STARTED
attempt RUNNING with exact causal RUNNING state/version
authoritative attempt reader refreshed
test sentinel stops before provider/tool runtime
```

# 8. provider persistence regression

Run:
```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/providers/test_execution_persistence.py
```

Require:
```text
23 executed
23 passed
0 failed
0 AISCC_TEST_DATABASE_URL lookup failures
```

If current discovery count is not 23, report exact count and STOP rather than changing tests.

# 9. workflow handoff regression

Run:
```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/providers/test_workflow_handoff.py
```

Require zero failures.

# 10. candidate immutability

After every command require candidate bytes unchanged:
- `src/aiscc/scenarios/stockroom_production.py`  `c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `f2bb84980c89f3dcdcd54bdfe6c283343bc43b978261c50aad8e20f09fb95616`

Also require:
```text
no other tracked modification
index empty
canonical state hashes unchanged
```

# 11. teardown

Stop/remove only:
```text
aiscc-p2-3-source-verification-postgres-0138-v1
```

Remove its Task-created anonymous storage.

No broad Docker cleanup/prune.

Verify:
```text
test container absent
no named verification volume
no Task-created anonymous volume residue
```

Do not inspect/alter retained private resources during teardown proof.

# 12. failure behavior

If a durable test fails:
```text
preserve candidate unchanged
capture safe failure evidence
remove isolated test container/storage
STOP_WITH_REPORT_EXPORT
```

No source/test edit and no private S1 recovery.

# 13. Git boundary

No add/commit/push/reset/restore/checkout/stash/clean.

Before Task movement:
```text
modified tracked = exact candidate two
index empty
Git-visible untracked = 14 exact
```

Move current Task byte-identically active→done.

Final Git-visible untracked:
```text
15 exact
```

# 14. contract review

Require exactly 34 rows:
```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_EXACT
PREDECESSOR_12_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
CANDIDATE_2_HASHES_EXACT
INDEX_EMPTY
ONLY_CANDIDATE_2_TRACKED_DIRTY
PYTHON_EXECUTABLE_EXACT
RETAINED_PRIVATE_RESOURCES_NOT_ACCESSED
TEST_DB_PROVISIONING_CONTRACT_IDENTIFIED
ISOLATED_POSTGRES_IMAGE_EXACT
ISOLATED_POSTGRES_CONTAINER_NAME_EXACT
ISOLATED_POSTGRES_LOCALHOST_ONLY
ISOLATED_POSTGRES_EPHEMERAL_CREDENTIAL
ISOLATED_POSTGRES_NO_RETAINED_VOLUME
ISOLATED_POSTGRES_READY
TEST_DB_SCHEMA_HEAD_EXACT
AISCC_TEST_DATABASE_URL_PROCESS_LOCAL_ONLY
SCENARIO_DURABLE_REGRESSION_EXECUTED
SCENARIO_DURABLE_REGRESSION_PASS
SCENARIO_SUITE_ZERO_REQUIRED_SKIPS
PROVIDER_PERSISTENCE_23_EXECUTED
PROVIDER_PERSISTENCE_23_PASS
WORKFLOW_HANDOFF_REGRESSION_PASS
CANDIDATE_HASHES_UNCHANGED_AFTER_TESTS
NO_SOURCE_TEST_STATE_MUTATION
NO_S1_RUNTIME_RECOVERY
ISOLATED_POSTGRES_STOPPED_REMOVED
ISOLATED_POSTGRES_STORAGE_REMOVED
NO_ISOLATED_TEST_RESIDUE
FINAL_INDEX_EMPTY
FINAL_TRACKED_DIRTY_EXACT_CANDIDATE_2
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
EXPORT_INTEGRITY_PASS
```

Success requires `34 / 34 PASS`.

# 15. success export

Root docs exactly 11:
```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
CANDIDATE_BASELINE_VERIFICATION.md
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
16 total members
15 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == canonical done Task
```

Never export the ephemeral DB password or credential-bearing URL.

# 16. success ceiling

```text
execution-start lifecycle source candidate:
DURABLY_VERIFIED

candidate bytes:
UNCHANGED

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
