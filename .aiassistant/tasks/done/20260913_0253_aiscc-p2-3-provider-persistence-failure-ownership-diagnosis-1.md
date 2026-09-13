# 작업지시서: P2-3 provider persistence failure ownership diagnosis

## meta

- task_id: `20260913_0253_aiscc-p2-3-provider-persistence-failure-ownership-diagnosis-1`
- created_at: `2026-09-13T02:53:02+09:00`
- work_type: `PROVIDER_PERSISTENCE_FAILURE_DIAGNOSIS`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- required_parent: `35cee94a92d1f12801576ef48038196922687f42`
- required_grandparent: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- source_write_authorized: `No`
- test_write_authorized: `No`
- retained_private_runtime_access_authorized: `No`
- isolated_test_postgresql_authorized: `Yes`
- accepted_predecessor_result_zip_sha256: `49531e7977e2811e322cd1403b1f1a2a64f204ff1f0264fd91c2e08cd3864f83`
- success_ceiling: `PROVIDER_PERSISTENCE_FAILURE_OWNER_IDENTIFIED / REWORK_PENDING`

# 0. purpose

Diagnose all 11 provider persistence failures from 0235 without changing any source or test.

Preserve the accepted S1 execution-start candidate exactly.

# 1. Python / transport

Use only:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Forbidden: `python`, `py`, WindowsApps alias, PATH Python discovery.

Verify the delivery ZIP/hash and exactly three flat safe members.

Place current Task first:

```text
.aiassistant/tasks/active/20260913_0253_aiscc-p2-3-provider-persistence-failure-ownership-diagnosis-1.md
```

Then place current Cycle/Judgment and verify their exact hashes:

```text
.aiassistant/records/aiscc/cycles/20260913_0253_aiscc-p2-3-provider-persistence-failure-diagnosis-entry-1.cycle.md
SHA-256 0419dbc78fb6149012653caefeab885324617307c5161e13bbf6d4df064bf69d

.aiassistant/reports/aiscc/20260913_0253_aiscc-p2-3-provider-persistence-regression-hold-diagnosis-judgment-1.md
SHA-256 169865f4095e2cd242d7b502eb5762f07d838727eb538a276e5bf0fc71c70555
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

Before delivery Git-visible untracked exactly 18:

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

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `02b7a77d3f29d7ee3878157470020ab83b377ba0343867ab81ec6e82d1a9190b`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `9ca1b1a24f3f73c2f81d3342442cf0462b58fecdba2dbccc33509b0d4039ab71`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `7315a943ad4ed82757f4398d9613f3a6f773755f3496fa1e8fa816123422ea84`

Tracked dirty exactly:

```text
src/aiscc/scenarios/stockroom_production.py
SHA-256 c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3

tests/integration/scenarios/test_stockroom_capture_runner.py
SHA-256 dca16f6ed0de608faa7f06cd4266ad377f140971536e0a82c0e92f679da73b72
```

No other tracked dirt.

After current Cycle/Judgment placement while Task is active/ignored:

```text
Git-visible untracked = 20 exact
```

# 3. strict prohibition

This Task is diagnosis only.

Do not edit:

```text
src/**
tests/**
config/**
migrations/**
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Do not access retained private S1 PostgreSQL/container/volume/password/runtime root or the 0036 WorkRun/attempt.

No private S1 recovery.

# 4. complete source reads

Read completely:

```text
src/aiscc/providers/service.py
tests/integration/providers/test_execution_persistence.py
```

Read directly required provider model/authority modules only as needed to interpret the signatures.

Record whole-file SHA-256 and HEAD blob for each production/test file used.

# 5. `_issue_capability` mechanical inventory

Using AST + `git grep`, enumerate every production definition and production call of:

```text
_issue_capability
```

For the current `AgentExecutionService` implementation record the exact signature and every keyword passed at each callsite, including whether these are required/optional:

```text
execution_attempt_id
execution_state
execution_state_version
```

Do not infer from traceback alone.

# 6. test-double override inventory

Within `tests/integration/providers/test_execution_persistence.py`, enumerate every class/function overriding or shadowing:

```text
_issue_capability
```

For each record:

```text
class
base class
exact signature
accepted positional/keyword arguments
which tests instantiate/use it
whether it matches current production caller contract
```

Also inventory directly related helper overrides used by the 11 failed tests.

# 7. candidate causality check

Mechanically determine whether the provider persistence suite imports, calls or otherwise executes either dirty candidate path:

```text
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Use AST/import/callsite evidence.

Classify candidate causality only as one of:

```text
DIRECT
INDIRECT_PROVED
NO_EXECUTION_PATH_FOUND
UNRESOLVED
```

Do not say “pre-existing baseline” unless current source/test evidence proves the failing path is outside both candidate files.

# 8. isolated PostgreSQL

Use exact locally available image:

```text
sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94
```

Create exactly one isolated container:

```text
aiscc-p2-3-provider-diagnosis-postgres-0253-v1
```

Requirements:

```text
127.0.0.1 only
Docker-assigned ephemeral host port
database aiscc_test
role aiscc_test
fresh process-only ephemeral password
tmpfs or otherwise Task-ephemeral storage only
no retained-private resource/network reuse
```

If exact container preexists: STOP.

Do not print/export the password or credential-bearing URL.

# 9. schema bootstrap

Use repository-owned Alembic bootstrap only:

```text
alembic.ini
migrations/env.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m alembic upgrade head
```

Require migration head:

```text
20260901_0008
```

# 10. provider test collection

With process-local `AISCC_TEST_DATABASE_URL`, run:

```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest --collect-only -q tests/integration/providers/test_execution_persistence.py
```

Require exact discovered count:

```text
23
```

If not 23: STOP and report.

# 11. one diagnostic execution

Run the provider persistence suite exactly once:

```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q --tb=short tests/integration/providers/test_execution_persistence.py
```

Do not rerun individual failures.

Capture enough safe traceback information to categorize all failures without credentials/private paths.

For each failed node ID record:

```text
first project-owned failing frame
exception type
normalized exception message
owning symbol/class
root-cause category
```

Do not export a credential-bearing DSN.

# 12. complete 11-failure categorization

The category counts must sum exactly to the observed failure count.

Allowed category labels are descriptive, not predetermined. Examples:

```text
STALE_TEST_DOUBLE_SIGNATURE
PRODUCTION_SERVICE_DEFECT
TEST_EXPECTATION_STALE
DATABASE_ISOLATION_ASSUMPTION
SECONDARY_CLEANUP_ERROR
OTHER_EXACT
```

Do not collapse failures merely because node names are similar.

For the known SameDomainWrongResourceService failure explicitly prove whether its override omits `execution_attempt_id` or another current keyword.

# 13. minimal rework scope

Without modifying anything, determine the smallest exact path set required to address every primary failure category.

For each path provide:

```text
path
HEAD blob
whole SHA-256
category addressed
why required
```

If failures require more than one independent correction, keep them separated.

Do not authorize any repair in this Task.

# 14. isolated DB teardown

After evidence capture, remove only:

```text
aiscc-p2-3-provider-diagnosis-postgres-0253-v1
```

Remove Task-created ephemeral storage.

No broad Docker cleanup/prune.

Verify no exact test-container/storage residue.

# 15. candidate immutability / Git

Require throughout and finally:

```text
src/aiscc/scenarios/stockroom_production.py
SHA-256 c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3

tests/integration/scenarios/test_stockroom_capture_runner.py
SHA-256 dca16f6ed0de608faa7f06cd4266ad377f140971536e0a82c0e92f679da73b72

index empty
canonical state hashes unchanged
no third tracked dirty path
```

No add/commit/push/reset/restore/checkout/stash/clean.

Before Task move Git-visible untracked = 20 exact.

Move current Task byte-identically active→done.

Final Git-visible untracked = 21 exact.

# 16. contract review

Require exactly 33 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_EXACT
PREDECESSOR_18_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
CANDIDATE_2_HASHES_EXACT
INDEX_EMPTY
ONLY_CANDIDATE_2_TRACKED_DIRTY
PYTHON_EXECUTABLE_EXACT
NO_SOURCE_TEST_STATE_MUTATION
NO_RETAINED_PRIVATE_RUNTIME_ACCESS
PROVIDER_SERVICE_COMPLETE_READ
PROVIDER_PERSISTENCE_TEST_COMPLETE_READ
ISSUE_CAPABILITY_PRODUCTION_SIGNATURE_IDENTIFIED
ISSUE_CAPABILITY_PRODUCTION_CALLS_INVENTORIED
ISSUE_CAPABILITY_TEST_OVERRIDES_INVENTORIED
STALE_OVERRIDE_SIGNATURES_IDENTIFIED
PROVIDER_23_TESTS_COLLECT_EXACT
ISOLATED_POSTGRESQL_PROVISIONED
TEST_DB_SCHEMA_HEAD_EXACT
PROVIDER_23_TESTS_EXECUTED_ONCE
ALL_11_FAILURES_CATEGORIZED
FAILURE_CATEGORY_COUNTS_SUM_11
KNOWN_SAME_DOMAIN_WRONG_RESOURCE_FAILURE_EXPLAINED
CANDIDATE_PATH_CAUSALITY_CHECKED
MINIMAL_REWORK_PATH_SET_IDENTIFIED
NO_SPECULATIVE_FIX
ISOLATED_POSTGRESQL_REMOVED
NO_TEST_DB_RESIDUE
CANDIDATE_HASHES_UNCHANGED
FINAL_INDEX_EMPTY
FINAL_DIRTY_PATHS_EXACT_2
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
EXPORT_INTEGRITY_PASS
```

Success requires `33 / 33 PASS`.

# 17. success export

Root docs exactly 11:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
PROVIDER_SERVICE_SIGNATURE_INVENTORY.md
PROVIDER_TEST_DOUBLE_INVENTORY.md
PROVIDER_FAILURE_CATEGORIZATION.md
CANDIDATE_CAUSALITY_VERIFICATION.md
ISOLATED_POSTGRESQL_VERIFICATION.md
SOURCE_TEST_SCOPE_DISCOVERY.md
CONTRACT_REVIEW.md
```

Project-relative copies exactly 5:

```text
current Cycle
current Judgment
current done Task
src/aiscc/providers/service.py
tests/integration/providers/test_execution_persistence.py
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

# 18. success ceiling

```text
S1 execution-start lifecycle candidate:
PRESERVED / DURABLE SCENARIO PASS

provider persistence failures:
OWNERSHIP_CATEGORIZED

source/test correction:
NOT PERFORMED

0036 durable S1 HOLD:
PRESERVED / UNTOUCHED

private S1 recovery:
NOT AUTHORIZED

P2-3:
IN_PROGRESS
```
