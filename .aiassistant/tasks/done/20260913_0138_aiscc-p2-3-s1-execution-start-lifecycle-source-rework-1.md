# 작업지시서: P2-3 S1 execution-start lifecycle source rework

## meta

- task_id: `20260913_0138_aiscc-p2-3-s1-execution-start-lifecycle-source-rework-1`
- created_at: `2026-09-13T01:38:20+09:00`
- work_type: `SOURCE_REWORK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- required_parent: `35cee94a92d1f12801576ef48038196922687f42`
- required_grandparent: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- source_write_authorized: `Yes / exact 2 paths`
- private_runtime_access_authorized: `No`
- runtime_recovery_authorized: `No`
- accepted_diagnosis_result_zip_sha256: `14007a21c9adeefc33459eb4d8fd7a2bb274e97e4578ceb59c56bd4523db9838`
- success_ceiling: `EXECUTION_START_LIFECYCLE_SOURCE_CORRECTED_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. purpose

Correct only the missing Stockroom integration bridge:

```text
WorkRun READY→RUNNING admitted
ExecutionAttempt remains NOT_STARTED
AgentExecutionService.execute returns NOT_STARTED before any operation
```

Do not access or mutate the retained 0036 S1 durable state.

# 1. Python and transport

Use only:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Forbidden: `python`, `py`, WindowsApps alias, PATH Python discovery.

Verify the inbound delivery ZIP/hash and exactly three flat safe members.

Place this Task first at:

```text
.aiassistant/tasks/active/20260913_0138_aiscc-p2-3-s1-execution-start-lifecycle-source-rework-1.md
```

Then place current Cycle/Judgment and verify:

```text
.aiassistant/records/aiscc/cycles/20260913_0138_aiscc-p2-3-s1-execution-start-lifecycle-source-rework-entry-1.cycle.md
SHA-256 5c7bfc64071e4e9feaf7a397c3377a6611986d190e7bcd74627ef8b5fdcb29db

.aiassistant/reports/aiscc/20260913_0138_aiscc-p2-3-s1-execution-lifecycle-owner-confirmed-rework-judgment-1.md
SHA-256 94b8347a340c12b7ecce6f71b3b7017f46a2dddf7cbcd36d577ad27cb8c39d73
```

# 2. repository baseline

Require branch `main`, HEAD `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`, HEAD^ `35cee94a92d1f12801576ef48038196922687f42`, HEAD^^ `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`, index empty, tracked clean.

Before delivery Git-visible untracked exactly 9:

- `.aiassistant/tasks/done/20260913_0012_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-retry-1.md`  `310bcfab97f13c7606bb09fc773ec6c659102e63b6ba1d33fa38b18c7cfeb034`
- `.aiassistant/records/aiscc/cycles/20260913_0012_aiscc-p2-3-private-s1-source-correction-persisted-execution-entry-1.cycle.md`  `ff0ca7f1752fd3a49306b660b1823b57b194a60b1d58c2341867e9c9b75dc702`
- `.aiassistant/reports/aiscc/20260913_0012_aiscc-p2-3-private-s1-source-correction-persisted-execution-authorization-judgment-1.md`  `568268a48fcda0145b549f9b26a5baf4287b8fb7f4937c3bfd9b2db60b5836a8`
- `.aiassistant/tasks/done/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-semantic-datetime-retry-1.md`  `0226353dba304ac01e9add745053502618001f6eecd833a92e9fd2b45d844f4b`
- `.aiassistant/records/aiscc/cycles/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-harness-corrected-retry-entry-1.cycle.md`  `8619cd9bfc9c3476129199c1213366a1bd26127c2f64d2156bddada7a3d97bfa`
- `.aiassistant/reports/aiscc/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-harness-error-retry-judgment-1.md`  `82550b3a3ed60678b1b252fe483f48003757870427ae8c1ecbefd4c35d1f0011`
- `.aiassistant/tasks/done/20260913_0115_aiscc-p2-3-s1-execution-lifecycle-desync-source-ownership-diagnosis-1.md`  `2b1443f6d760a63cc6a43b6fde4bdd26e9dc957f882216ca7a5a685068e2f00a`
- `.aiassistant/records/aiscc/cycles/20260913_0115_aiscc-p2-3-s1-execution-lifecycle-desync-diagnosis-entry-1.cycle.md`  `8b9f180f0e9a0d4ccf505ac2c3de920a5be3c9a088f163ae80066c1d6145b428`
- `.aiassistant/reports/aiscc/20260913_0115_aiscc-p2-3-s1-execution-not-started-runtime-hold-judgment-1.md`  `f462080446ad883fea933b48677a7b871dfcd054b8c344c410950db02af3772d`

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `02b7a77d3f29d7ee3878157470020ab83b377ba0343867ab81ec6e82d1a9190b`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `9ca1b1a24f3f73c2f81d3342442cf0462b58fecdba2dbccc33509b0d4039ab71`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `7315a943ad4ed82757f4398d9613f3a6f773755f3496fa1e8fa816123422ea84`

After current Cycle/Judgment placement while Task is active/ignored: Git-visible untracked exactly 11.

# 3. exact source scope

Before source write require:

```text
src/aiscc/scenarios/stockroom_production.py
HEAD blob 8ce77a62fb11a0d1675f9fba1b77289706539d04
SHA-256 1ca58848a837e1130229c7a0e085df999d04c6041c77bb61098185d342ff14a0

tests/integration/scenarios/test_stockroom_capture_runner.py
HEAD blob edd7db03789ca51838dc6ed3b8cb0eb8d9cec793
SHA-256 02f5835a726f22d81d9d631f120c9d7c9b3c1311cc23ed93db5d3abd9a57f41e
```

These are the only modifiable tracked paths.

Verification-only baselines:

```text
src/aiscc/providers/service.py
f21c3c29443446650e31fb0d4d0d30ceddb8956d51ad2e17221536102c6c5c18

src/aiscc/persistence/repository.py
ab00af3dd871477da74b83275258aa48a47ba9a7081aad0154a808b6e4f1c089

src/aiscc/scenarios/capture_runner.py
0dab27e0ce9ce2da7953188bcb26f288b637a4ba524141be2800b08302a59b18

tests/integration/providers/test_execution_persistence.py
717a40b9323d0c42560ef34a8f39634777be0929d3eeaea5b447c9e4e4de1214

tests/integration/providers/test_workflow_handoff.py
a76c021bd2ae4f55335c50d1b4dffd24256c732986e00cbb1ef709b06e601b70

tests/unit/scenarios/test_stockroom_capture_runner.py
a137021608ac9cb5b4c328b6bb88fd0c22cb0d9afd9b1a22054ec5bdd32f68ff
```

No model/schema/migration/config/state path is authorized.

# 4. mandatory static reproduction

Before write mechanically prove current HEAD still does all of:

```text
create_attempt → NOT_STARTED / READY
G_EXECUTION_STARTED uses that exact prepared ref
READY→RUNNING is admitted
_transition_result refreshes only WorkRun snapshot
stockroom_production.py has no durable EXECUTION_STARTED call
AgentExecutionService.execute returns immediately when attempt.status != RUNNING
```

Mismatch → `SOURCE_BASELINE_DIAGNOSIS_MISMATCH` and STOP before write.

# 5. ownership

Keep ownership where diagnosed.

Do not move the missing start into:

```text
AgentExecutionService.execute
PostgresExecutionRepository
StockroomCaptureRunner
P1-4 guard authority
ExecutionReferenceAuthority.register_start
```

`register_start` remains prepared NOT_STARTED authority.
`G_EXECUTION_STARTED` remains authorization for READY→RUNNING, not proof the durable start event already occurred.

# 6. required exact order

For the normal READY→RUNNING path:

```text
A exact prepared NOT_STARTED attempt exists
B G_EXECUTION_STARTED verifies that exact ref
C WorkflowKernel admits READY→RUNNING
D authoritative WorkRun RUNNING/resulting version is verified
E execution_repository.transition_attempt(exact attempt_id, "EXECUTION_STARTED", existing convention) exactly once
F authoritative WorkRun + attempt are reloaded
G WorkRun == RUNNING at decision.resulting_state_version
H attempt == RUNNING
I attempt.causal_state == RUNNING
J attempt.causal_state_version == WorkRun state_version
K exact run/attempt identity unchanged
L adapter current attempt view is refreshed from authoritative post-start values
M only then READY→RUNNING owner result may return ADMITTED
```

Never start the execution attempt before WorkRun RUNNING admission.

# 7. exact prepared binding

The durable start must use the same attempt that backed `G_EXECUTION_STARTED`.

Require before start:

```text
authority ref count = 1
handle type = ExecutionAttemptRef
attempt_id = prepared request attempt_id
work_run_id = prepared request run_id
status = NOT_STARTED
state = READY
state_version = exact observed READY version
```

No caller-created replacement ref.

# 8. event refs

Do not invent new `refs` keys or a new provenance schema.

Inspect the existing canonical `EXECUTION_STARTED` test/contract convention.

- If existing start uses no refs: preserve no-refs.
- If one canonical refs contract exists: use it exactly.
- If ambiguous: `EXECUTION_START_REF_CONTRACT_AMBIGUOUS` → STOP before source write.

# 9. post-start authority

Reload using the existing durable authority path.

Require exact RUNNING WorkRun and RUNNING attempt with the same causal state/version.

Refresh `_CurrentAttemptReader.attempt` from the authoritative post-start attempt; do not mutate/fake the old NOT_STARTED ref.

# 10. fail closed

Workflow transition denied:

```text
EXECUTION_STARTED calls = 0
```

WorkRun admitted but start mutation or post-start verification fails:

```text
no seal_security_context
no authorize_runtime
no materialize
no AgentExecutionService.execute
no provider/tool dispatch
```

Do not rollback WorkRun, create replacement attempt, or fabricate RUNNING in memory.

# 11. static branch

Preserve S3/static branch: no execution start, security, materialization or provider/tool execution.

Do not edit `capture_runner.py`.

# 12. required integration regressions

Modify only `tests/integration/scenarios/test_stockroom_capture_runner.py`.

Prove:

1. Positive actual Stockroom owner path:
   NOT_STARTED/READY → admitted RUNNING → one durable EXECUTION_STARTED → RUNNING causal exact → downstream service no longer sees NOT_STARTED.

2. Workflow denial:
   no EXECUTION_STARTED and no downstream side effect.

3. Durable start failure:
   WorkRun admitted RUNNING but no security/materialization/execution.

4. Post-start authority mismatch:
   NOT_STARTED/wrong causal version/wrong identity is denied before downstream side effects.

5. S3/static:
   no EXECUTION_STARTED.

Use the actual Stockroom production owner path, not only a RecordingOwners fake.

# 13. validation

Run only with the exact Python executable:

```text
"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m py_compile src/aiscc/scenarios/stockroom_production.py tests/integration/scenarios/test_stockroom_capture_runner.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -m ruff check src/aiscc/scenarios/stockroom_production.py tests/integration/scenarios/test_stockroom_capture_runner.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/scenarios/test_stockroom_capture_runner.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/providers/test_execution_persistence.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/integration/providers/test_workflow_handoff.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/unit/scenarios/test_stockroom_capture_runner.py

"C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe" -B -m pytest -q tests/unit

git diff --check
```

These tests must not access the retained private S1 DB/container/runtime root.

# 14. forbidden scope

Do not modify verification-only files, provider models/events/authority, workflow source, schema/migrations, or canonical state.

Do not access retained private PostgreSQL, Docker, secret file, private runtime root, or the 0036 WorkRun/attempt.

No runtime recovery.

# 15. Git boundary

No add/commit/push/reset/restore/checkout/stash/clean.

Before Task move:

```text
modified tracked paths = exact two authorized paths
index empty
Git-visible untracked = 11 exact
```

Move current Task byte-identically active→done.

Final Git-visible untracked = 12 exact:
0012/0036/0115/current Task+Cycle+Judgment.

# 16. contract review

Require exactly 48 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_9_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
MODIFIABLE_2_BASELINES_EXACT
VERIFICATION_ONLY_BASELINES_EXACT
PYTHON_EXECUTABLE_EXACT
NO_PRIVATE_RUNTIME_ACCESS
NO_DB_DOCKER_ACCESS
DEFECT_B_REPRODUCED_STATIC
EXACT_PREPARED_ATTEMPT_REUSED
WORKFLOW_RUNNING_ADMISSION_PRECEDES_EXECUTION_START
DURABLE_EXECUTION_STARTED_CALLED_ONCE
EXECUTION_START_USES_EXISTING_REPOSITORY_API
NO_NEW_EVENT_REF_SCHEMA_INVENTED
POST_START_AUTHORITY_RELOADED
POST_START_WORKRUN_RUNNING_EXACT
POST_START_ATTEMPT_RUNNING_EXACT
POST_START_CAUSAL_VERSION_EXACT
CURRENT_ATTEMPT_VIEW_REFRESHED
ADMITTED_RETURN_ONLY_AFTER_EXECUTION_START
START_FAILURE_STOPS_BEFORE_SECURITY
START_FAILURE_STOPS_BEFORE_MATERIALIZATION
START_FAILURE_STOPS_BEFORE_EXECUTION
WORKFLOW_DENIAL_DOES_NOT_START_ATTEMPT
S3_STATIC_BRANCH_DOES_NOT_START_ATTEMPT
NO_SECOND_ATTEMPT_OR_ID_SUBSTITUTION
PROVIDER_SERVICE_NOT_WEAKENED
EXECUTION_REPOSITORY_NOT_WEAKENED
CAPTURE_RUNNER_ORDER_UNCHANGED
POSITIVE_STOCKROOM_LIFECYCLE_REGRESSION_PASS
START_FAILURE_NEGATIVE_REGRESSION_PASS
MISMATCHED_POST_START_AUTHORITY_DENIED
WORKFLOW_DENIED_NO_START_REGRESSION_PASS
STATIC_BRANCH_NO_START_REGRESSION_PASS
PROVIDER_PERSISTENCE_REGRESSION_PASS
WORKFLOW_HANDOFF_REGRESSION_PASS
RUNNER_UNIT_REGRESSION_PASS
TARGETED_SCENARIO_INTEGRATION_PASS
FULL_UNIT_REGRESSION_PASS
RUFF_PASS
PY_COMPILE_PASS
GIT_DIFF_CHECK_PASS
MODIFIED_PATHS_EXACT_SUBSET_2
NO_CANONICAL_STATE_MUTATION
NO_GIT_COMMIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
EXPORT_INTEGRITY_PASS
```

Success requires `48 / 48 PASS`.

# 17. success export

Root docs exactly 12:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
DIAGNOSIS_BASELINE_VERIFICATION.md
EXECUTION_START_PATCH_VERIFICATION.md
POST_START_AUTHORITY_VERIFICATION.md
NEGATIVE_REGRESSION_VERIFICATION.md
TEST_VERIFICATION.md
GIT_DIFF_VERIFICATION.md
NO_RUNTIME_ACCESS_VERIFICATION.md
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

Success export: 17 members total, 16 non-self manifest rows, one top-level directory, CRC PASS, folder/archive byte equality, TASK.md == canonical done Task.

# 18. success ceiling

```text
execution-start lifecycle defect:
CORRECTED_CANDIDATE

0036 durable S1 HOLD:
PRESERVED / UNTOUCHED

runtime recovery:
NOT AUTHORIZED

private S1 rerun:
NOT AUTHORIZED

Browser source acceptance:
HUMAN_PENDING

Git persistence:
NOT PERFORMED

P2-3:
IN_PROGRESS
```
