# 작업지시서: P2-3 provider persistence complete capture + conditional fixture rework

## meta

- task_id: `20260913_1045_aiscc-p2-3-provider-persistence-complete-capture-conditional-fixture-rework-1`
- created_at: `2026-09-13T10:45:43+09:00`
- work_type: `COMPLETE_FAILURE_CAPTURE_AND_CONDITIONAL_TEST_REWORK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- required_parent: `35cee94a92d1f12801576ef48038196922687f42`
- required_grandparent: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- product_source_write_authorized: `No`
- scenario_test_write_authorized: `No`
- provider_test_write_authorized: `Conditional / exact one path`
- retained_private_runtime_access_authorized: `No`
- isolated_test_postgresql_authorized: `Yes`
- predecessor_result_zip_sha256: `899f433fd92c57f601c9076ded6721c7cc605339c7ace8dc08b8246298d3bc44`
- success_ceiling: `S1_EXECUTION_START_CANDIDATE_DURABLY_VERIFIED_WITH_PROVIDER_FIXTURE_ALIGNMENT / BROWSER_REVIEW_PENDING`

# 0. purpose

Close the 0253 capture gap without another diagnose→repair Task cycle.

Phase A:
capture and categorize all 11 provider-persistence failures completely.

Phase B:
only if Phase A proves the exact allowed two-category distribution, repair the provider test fixture in one path and
rerun the required durable regression.

No product source write and no retained private S1 access.

# 1. Python / transport

Use only:
```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Forbidden: `python`, `py`, WindowsApps alias, PATH Python discovery.

Verify delivery ZIP/hash and exactly three flat safe members.

Place current Task first:
```text
.aiassistant/tasks/active/20260913_1045_aiscc-p2-3-provider-persistence-complete-capture-conditional-fixture-rework-1.md
```

Then place:
```text
.aiassistant/records/aiscc/cycles/20260913_1045_aiscc-p2-3-provider-persistence-complete-capture-entry-1.cycle.md
SHA-256 0d670319bcb02ee23269e6bb0fa9c259fb864f506081cf23b6d82711705253bc

.aiassistant/reports/aiscc/20260913_1045_aiscc-p2-3-provider-persistence-incomplete-capture-conditional-rework-judgment-1.md
SHA-256 5d3d2dbdbd9f0a183ca6d073216f11a44a2b26aded251c06b34fb3614d4658d1
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

Before delivery Git-visible untracked exactly 21:
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

Require clean HEAD bytes:
```text
src/aiscc/providers/service.py
SHA-256 f21c3c29443446650e31fb0d4d0d30ceddb8956d51ad2e17221536102c6c5c18

tests/integration/providers/test_execution_persistence.py
SHA-256 717a40b9323d0c42560ef34a8f39634777be0929d3eeaea5b447c9e4e4de1214
```

After current Cycle/Judgment placement while current Task is active/ignored:
```text
Git-visible untracked = 23 exact
```

# 3. retained-private prohibition

Do not inspect/connect/exec/stop/restart/mutate:
```text
aiscc-p2-3-private-postgres-v1
aiscc-p2-3-private-postgres-data-v1
aiscc_private_capture
private password file
private runtime root
0036 S1 WorkRun/attempt
```

No private S1 recovery.

# 4. mandatory static reconfirmation before provisioning

Read completely:
```text
src/aiscc/providers/service.py
tests/integration/providers/test_execution_persistence.py
```

Mechanically reconfirm both current discrepancies:

## A — synthetic dispatcher fingerprint

`DurableSyntheticDispatcher.dispatch` currently computes returned `argument_hash` without:
```text
resolved_dispatch_context
```

Current canonical tool broker fingerprint includes that field even for the legacy tool where value is `None`.

Require static proof that exactly the ten non-SAME_DOMAIN currently failing nodes use `DurableSyntheticDispatcher`.

## B — wrong-resource service override

`SameDomainWrongResourceService._issue_capability` currently omits:
```text
execution_attempt_id
provider_profile_id
provider_profile_version
resolved_spec_fingerprint
```

Require current production base signature/calls prove these are valid optional keyword parameters and that
`execution_state` / `execution_state_version` are not current production parameters.

If either static finding differs:
```text
STATIC_DIAGNOSIS_BASELINE_MISMATCH
→ STOP before Docker provisioning
```

No write is permitted in sections 1–10.

# 5. isolated PostgreSQL

Use exact locally available PostgreSQL image:
```text
sha256:ef257d85f76e48da1c64832459b59fcaba1a4dac97bf5d7450c77753542eee94
```

Create exactly:
```text
aiscc-p2-3-provider-complete-capture-postgres-1045-v1
```

Requirements:
```text
127.0.0.1 only
Docker-assigned ephemeral host port
database aiscc_test
role aiscc_test
fresh ephemeral process-only password
Task-ephemeral storage only
no retained-private resource/network reuse
```

If exact container name preexists: STOP.

Never print/export password or credential-bearing URL.

# 6. schema bootstrap

Use repository-owned Alembic:
```text
alembic.ini
migrations/env.py
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m alembic upgrade head
```

Require migration head:
```text
20260901_0008
```

# 7. Phase A collection

Set `AISCC_TEST_DATABASE_URL` only in the test-process environment.

Run:
```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest --collect-only -q tests/integration/providers/test_execution_persistence.py
```

Require exactly:
```text
23 collected
```

# 8. Phase A complete diagnostic execution

Execute provider persistence suite exactly once before any edit.

Use pytest built-in JUnit XML plus complete raw stdout/stderr capture.

Equivalent required command semantics:
```text
pytest -vv --tb=long
  --junitxml=<Task-created ignored/temp path>/provider-persistence-phase-a.xml
  tests/integration/providers/test_execution_persistence.py
```

Capture stdout and stderr byte-completely to a separate Task-created ignored/temp file.

Do not parse failure boundaries by underscore decoration.

Do not delete Phase A raw/XML until all classification reports are complete.

Raw/XML are diagnostic inputs only and must not enter final export unless sanitized and explicitly required.

Require observed result:
```text
23 executed
12 passed
11 failed
```

If counts differ:
```text
PROVIDER_PHASE_A_RESULT_DRIFT
→ teardown
→ STOP_WITH_REPORT_EXPORT
```

# 9. Phase A evidence extraction

For every one of the 11 failed node IDs, derive evidence from JUnit XML and/or complete raw output:

```text
node id
failure type
failure message
complete primary traceback text or equivalent JUnit failure body
first project-owned failing frame where applicable
first deterministic source/test predicate explaining the observed failure
root-cause category
```

Every failed node must have non-empty primary evidence.

No category may be assigned from node-name similarity alone.

# 10. exact conditional classification gate

Phase B is authorized only if Phase A proves exactly:

```text
STALE_DURABLE_SYNTHETIC_DISPATCHER_FINGERPRINT:
10

STALE_SAME_DOMAIN_WRONG_RESOURCE_SIGNATURE:
1

all other categories:
0
```

For each of the ten dispatcher failures, prove:
```text
test uses DurableSyntheticDispatcher
dispatcher returned fingerprint omits resolved_dispatch_context
current canonical broker fingerprint includes resolved_dispatch_context=None for this legacy tool
observed failure outcome is causally consistent with broker mismatch / TOOL_FAILED path
no earlier independent primary cause exists in captured traceback/evidence
```

For the one wrong-resource failure, prove:
```text
SameDomainWrongResourceService selected
production call supplies a current optional keyword omitted by override
Python binding fails before override body / intended wrong-resource behavior
```

Also reconfirm:
```text
provider persistence test has NO_EXECUTION_PATH_FOUND to either current dirty candidate path
```

If any failure is unresolved, has another cause, or implicates production code:
```text
CONDITIONAL_WRITE_GATE_NOT_SATISFIED
→ no file write
→ teardown
→ STOP_WITH_REPORT_EXPORT
```

# 11. Phase B authorized file

Only after section 10 fully passes, modify exactly:
```text
tests/integration/providers/test_execution_persistence.py
```

Do not modify any production path or scenario test.

# 12. Phase B correction A — dispatcher fingerprint

In `DurableSyntheticDispatcher.dispatch`, align the synthetic returned `argument_hash` payload with the current canonical
broker payload for the existing legacy synthetic tool.

Add exactly the currently required canonical field:
```text
"resolved_dispatch_context": None
```

Preserve every other existing fingerprint field/value and test behavior.

Do not hard-code a new production fingerprint unrelated to the current broker contract.

# 13. Phase B correction B — wrong-resource override

Update only `SameDomainWrongResourceService._issue_capability` so its override accepts the current base optional keyword
contract:

```text
execution_attempt_id: str = ""
provider_profile_id: str = ""
provider_profile_version: str = ""
resolved_spec_fingerprint: str = ""
```

Preserve its intentional behavior:
```text
only FILESYSTEM workspace:server-owned-exact
→ substituted to workspace:same-domain-wrong
```

Forward every received current base parameter to `super()._issue_capability(...)`, including the four parameters above.

Do not add nonexistent:
```text
execution_state
execution_state_version
```

Do not use `**kwargs` to hide future contract drift.

# 14. post-edit exact scope

Immediately after edit require:
```text
modified tracked paths exactly 3:
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
tests/integration/providers/test_execution_persistence.py

index empty

product source SHA unchanged:
c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3

scenario test SHA unchanged:
dca16f6ed0de608faa7f06cd4266ad377f140971536e0a82c0e92f679da73b72
```

No fourth tracked path.

# 15. provider durable regression after correction

Against the same isolated test PostgreSQL, rerun:
```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/providers/test_execution_persistence.py
```

Require exactly:
```text
23 executed
23 passed
0 failed
```

No further provider-test edit if it fails.
A failure after the one authorized edit → STOP_WITH_REPORT_EXPORT.

# 16. scenario durable regression after correction

Run:
```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/scenarios/test_stockroom_capture_runner.py
```

Require exactly the current discovered scenario suite to pass with:
```text
55 passed
0 required skips
```

Specifically retain the durable S1 execution-start proof reached in 0235.

# 17. workflow handoff regression

Run:
```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/providers/test_workflow_handoff.py
```

Require zero failures.

# 18. static/unit validation

Run:
```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m py_compile
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py
  tests/integration/providers/test_execution_persistence.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -m ruff check
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py
  tests/integration/providers/test_execution_persistence.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/unit

git diff --check
```

Require zero failures.

# 19. isolated PostgreSQL teardown

After all evidence is captured, stop/remove only:
```text
aiscc-p2-3-provider-complete-capture-postgres-1045-v1
```

Remove only Task-created ephemeral storage.

No broad Docker cleanup/prune.

Verify exact container/storage residue absent.

# 20. diagnostic temporary-file handling

Before export, scan Phase A raw output/XML for:
```text
ephemeral password
credential-bearing DB URL
```

Do not export raw/XML.

Generate sanitized classification summaries only.

Delete Task-created raw/XML after their hashes/counts and sanitized evidence have been recorded and final export is verified.

# 21. Git boundary

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

Before Task move require:
```text
index empty
tracked dirty exactly 3
Git-visible untracked = 23 exact
canonical state hashes unchanged
```

Move current Task byte-identically active→done.

Final Git-visible untracked:
```text
24 exact
```

# 22. contract review

Require exactly 53 rows:
```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_EXACT
PREDECESSOR_21_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
CANDIDATE_2_HASHES_EXACT
PROVIDER_TEST_HEAD_HASH_EXACT
PROVIDER_SERVICE_HASH_EXACT
INDEX_EMPTY
ONLY_CANDIDATE_2_TRACKED_DIRTY
PYTHON_EXECUTABLE_EXACT
NO_RETAINED_PRIVATE_RUNTIME_ACCESS
NO_PRE_PHASE_A_WRITE
PROVIDER_SERVICE_COMPLETE_READ
PROVIDER_TEST_COMPLETE_READ
STATIC_TWO_DEFECTS_RECONFIRMED
ISOLATED_POSTGRESQL_PROVISIONED
TEST_DB_SCHEMA_HEAD_EXACT
PROVIDER_23_COLLECT_EXACT
PHASE_A_PYTEST_EXECUTED_ONCE
PHASE_A_RAW_OUTPUT_CAPTURED
PHASE_A_JUNIT_XML_CAPTURED
ALL_11_FAILURES_HAVE_PRIMARY_EVIDENCE
ALL_11_FAILURES_CATEGORIZED
FAILURE_CATEGORY_COUNTS_SUM_11
DISPATCHER_CATEGORY_COUNT_EXACT_10
SIGNATURE_CATEGORY_COUNT_EXACT_1
NO_OTHER_FAILURE_CATEGORY
CANDIDATE_CAUSALITY_NO_EXECUTION_PATH
CONDITIONAL_WRITE_GATE_SATISFIED
PROVIDER_TEST_ONLY_MODIFICATION
PRODUCT_SOURCE_BYTES_UNCHANGED
SCENARIO_TEST_BYTES_UNCHANGED
DISPATCHER_FINGERPRINT_CONTEXT_FIELD_ALIGNED
WRONG_RESOURCE_OVERRIDE_SIGNATURE_ALIGNED
WRONG_RESOURCE_BEHAVIOR_PRESERVED
PRODUCTION_PROVIDER_CODE_UNCHANGED
PROVIDER_23_POSTFIX_EXECUTED
PROVIDER_23_POSTFIX_PASS
SCENARIO_55_POSTFIX_EXECUTED
SCENARIO_55_POSTFIX_PASS
WORKFLOW_HANDOFF_POSTFIX_PASS
FULL_UNIT_POSTFIX_PASS
RUFF_PASS
PY_COMPILE_PASS
GIT_DIFF_CHECK_PASS
NO_SOURCE_STATE_MUTATION
NO_S1_RUNTIME_RECOVERY
ISOLATED_POSTGRESQL_REMOVED
NO_TEST_DB_RESIDUE
FINAL_INDEX_EMPTY
FINAL_DIRTY_PATHS_EXACT_3
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
EXPORT_INTEGRITY_PASS
```

Success requires:
```text
53 / 53 PASS
```

If Phase A blocks conditional correction, correction/postfix rows remain `BLOCKED_REQUIRED_EVIDENCE`.

# 23. success export

Root docs exactly 14:
```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
PHASE_A_CAPTURE_VERIFICATION.md
PROVIDER_FAILURE_CATEGORIZATION.md
STATIC_ROOT_CAUSE_VERIFICATION.md
CONDITIONAL_REWORK_DECISION.md
PROVIDER_TEST_FIXTURE_PATCH_VERIFICATION.md
ISOLATED_POSTGRESQL_VERIFICATION.md
DURABLE_PROVIDER_VERIFICATION.md
DURABLE_SCENARIO_VERIFICATION.md
TEST_VERIFICATION.md
CONTRACT_REVIEW.md
```

Project-relative copies exactly 6:
```text
current Cycle
current Judgment
current done Task
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
tests/integration/providers/test_execution_persistence.py
```

Success export:
```text
20 total members
19 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == canonical done Task
```

No credential-bearing Phase A raw output/JUnit XML in export.

# 24. success ceiling

```text
S1 execution-start lifecycle product candidate:
DURABLY_VERIFIED

scenario fixture:
CANONICAL_AUTHORITY_ALIGNED

provider persistence fixture:
CURRENT_CONTRACT_ALIGNED

provider persistence suite:
23 / 23 PASS

scenario durable suite:
55 / 55 PASS

0036 durable S1 HOLD:
PRESERVED / UNTOUCHED

private S1 recovery:
NOT AUTHORIZED

Browser source/test acceptance:
HUMAN_PENDING

Git persistence:
NOT PERFORMED

P2-3:
IN_PROGRESS
```
