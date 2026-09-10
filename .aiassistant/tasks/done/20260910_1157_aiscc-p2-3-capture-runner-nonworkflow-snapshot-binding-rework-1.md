# 작업지시서: P2-3 capture-runner non-workflow snapshot binding rework

## meta

- task_id: `20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-1`
- created_at: `2026-09-10T11:57:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `ORCHESTRATION_BINDING_REWORK / UNIT_REGRESSION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf`
- required_base_tree: `992a15a33e8b34cc3da35f44bd846ceddccb2526`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Preserve the 1142 status-domain and workflow-authority fixes.

Add the missing canonical rule:

```text
accepted non-workflow owner result
must be bound to the runner's current authoritative workflow state/version.
```

Non-workflow owners still cannot advance workflow authority.

# 1. inbound ZIP bootstrap

Verify the Browser delivery ZIP by exact filename/SHA-256, validate archive safety, place TASK first at:

```text
.aiassistant/tasks/active/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-1.md
```

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-entry-1.cycle.md
SHA-256:
dd4d4bf3a8cbfcf35fbdd849fcf22609fa19a6474c05eefdff959f475de094bf

.aiassistant/reports/aiscc/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-judgment-1.md
SHA-256:
091813d26152595a0c12bf82fd16827dcc105b31bbff6cc3c144bf0a0d8231f9
```

Bootstrap failure before TASK placement:

```text
STOP
no report/export
no substantive mutation
```

# 2. repository gate

Require:

```text
branch:
main

HEAD:
04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf

HEAD tree:
992a15a33e8b34cc3da35f44bd846ceddccb2526

index:
empty
```

Expected Git-visible set excluding active Task is exact 17 paths:

- `.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1142_aiscc-p2-3-capture-runner-owner-status-authority-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-judgment-1.md`
- `src/aiscc/scenarios/capture_runner.py`
- `src/aiscc/scenarios/driver.py`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`
- `.aiassistant/records/aiscc/cycles/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

No cleanup/reset/stash/restore.

# 3. exact predecessor/candidate identity

Require exact governance/source hashes:

- `.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md`  `11db99ba9b22ed8e6dddab96d49d1a9207b928b846c93e53bcd88e48a8d10f52`
- `.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md`  `3cc310ccfe052307a906fe2524db6176f7af0d38ba53616096df6ece0ff581a0`
- `.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md`  `6cb059aa4206ac5e1f00789e8adbc955f574bf84c71b2e551c4f23a414e51ff0`
- `.aiassistant/tasks/done/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md`  `0109756f710d26b625b42ec90c98f0dd585cad36445473e9fb9e4e20e964d3d2`
- `.aiassistant/records/aiscc/cycles/20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md`  `6a6195c8c430a9d292c765f6a044992970b945518c25a12e506737873999bbbb`
- `.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md`  `48e84d88626bcd5804ff4f3f9c580c7f9d4efa28ea974adb5f69498afa8555c3`
- `.aiassistant/tasks/done/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md`  `ed429af33012ecc73613badd4fc743181b5570accccd931be91e24f0bcf81dbf`
- `.aiassistant/records/aiscc/cycles/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-retry-entry-1.cycle.md`  `56de671d96c839d91d8457ed3c131f152627211ed825489a0222399041b844b6`
- `.aiassistant/reports/aiscc/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-judgment-1.md`  `5a97033467671e9cbeddc66f8d3010cc8e45bab32d11be1307d8415e8b999983`
- `.aiassistant/tasks/done/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1.md`  `1c663fa72c263d5176db907e418f33811aa7f4174bc6db764d4ddb74c17f6648`
- `.aiassistant/records/aiscc/cycles/20260910_1142_aiscc-p2-3-capture-runner-owner-status-authority-rework-entry-1.cycle.md`  `d23c0d5108aa26d7b66b02dcbb0dc047eedd871ba5f208fb7b675758d71d2b63`
- `.aiassistant/reports/aiscc/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-judgment-1.md`  `079d0593ef198b4f3adebd01bb2e74aebbed645e0550563e90b5b92aea1c5f5c`
- `src/aiscc/scenarios/capture_runner.py`  `5f7765b3eae7078002adc27ca2536b3fc8e55fe264f1837c2e7c5350ed79cd2b`
- `src/aiscc/scenarios/driver.py`  `9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`  `badf838be2f1000346ed42cbaa8defcc2d15ab569cb88da5e03ffd64e60dac5c`

Mismatch:

```text
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

# 4. mutation allowlist

Only:

```text
MODIFY:
src/aiscc/scenarios/capture_runner.py
tests/unit/scenarios/test_stockroom_capture_runner.py
```

Frozen:

```text
src/aiscc/scenarios/driver.py
SHA-256:
9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6
```

No other source/config/test mutation.

# 5. preserve 1142 operation-status contract

Do not weaken these exact operation statuses:

```text
initial_ready:
ADMITTED

create_attempt:
ADMITTED

request_transition:
ADMITTED

seal_security_context:
ADMITTED

authorize_runtime:
ADMITTED

materialize:
ADMITTED

execute:
COMPLETED

submit_runtime_evidence:
ADMITTED

submit_static_policy_evidence:
ADMITTED

evaluate_evidence S1/S3/S4:
SATISFIED

evaluate_evidence S2:
UNSATISFIED

submit_agent_human_claim:
REJECTED

open_human_gate:
PENDING

issue_judgment:
ADMITTED

create_policy_blocker:
ADMITTED
```

Unexpected status remains:

```text
record
STOP
no later calls
no retry
```

# 6. preserve workflow-only authority advancement

Authoritative local workflow state/version may be established/advanced only by:

```text
initial_ready exact ADMITTED/READY/expected-version

request_transition exact:
ADMITTED
requested target
observed_version + 1
```

No other owner may advance it.

# 7. new non-workflow current-snapshot binding rule

For every non-workflow operation that returns its expected operation status, require additionally:

```text
result.workflow_state is current authoritative state
result.state_version == current authoritative version
```

This applies to:

```text
create_attempt
seal_security_context
authorize_runtime
materialize
execute
submit_runtime_evidence
submit_static_policy_evidence
evaluate_evidence
submit_agent_human_claim
open_human_gate
issue_judgment
create_policy_blocker
```

If expected status matches but state or version differs:

```text
record returned result in progress
return STOPPED
do not mutate local authoritative state/version
do not make later owner calls
do not retry
```

The stop reason must be stable and distinguish snapshot/binding mismatch from ordinary status denial.

Use repository-style stable code such as:

```text
OWNER_RESULT_STATE_VERSION_MISMATCH
```

or an existing exact equivalent if already defined.

# 8. accepted result provenance

Recording an accepted non-workflow result does not itself admit workflow mutation.

Progress may retain the returned owner snapshot.

The top-level stopped result must retain the last valid workflow-authoritative:

```text
workflow_state
state_version
```

not the mismatched returned values.

# 9. replace 1142 forged-snapshot expectation

The 1142 unit currently demonstrates that forged non-workflow state/version is ignored and execution continues.

Change those tests to the canonical fail-closed expectation.

At minimum execute:

```text
create_attempt:
ADMITTED + wrong state/version
→ STOP before READY->RUNNING

security context:
ADMITTED + wrong state/version
→ STOP before authorize_runtime

runtime grant:
ADMITTED + wrong state/version
→ STOP before materialize

materialize:
ADMITTED + wrong state/version
→ STOP before execute

execute:
COMPLETED + wrong state/version
→ STOP before ADMISSION_PENDING

runtime evidence:
ADMITTED + wrong state/version
→ STOP before evaluate

static S3 evidence:
ADMITTED + wrong state/version
→ STOP before evaluate/blocker

evidence evaluation:
expected SATISFIED/UNSATISFIED + wrong state/version
→ STOP

Agent claim:
REJECTED + wrong state/version
→ STOP before Human gate

Human gate:
PENDING + wrong state/version
→ STOP before HUMAN_REQUIRED transition

Judgment:
ADMITTED + wrong state/version
→ STOP before terminal/rework transition

policy blocker:
ADMITTED + wrong state/version
→ STOP before BLOCKED transition
```

Each case must prove:

```text
failing call exactly once
mismatched result recorded
no later owner call
no automatic retry
top-level result retains last valid authoritative state/version
```

# 10. preserve workflow-result tampering tests

Keep PASS coverage for:

```text
initial_ready wrong state
initial_ready wrong version
transition wrong target
transition same/skipped/wrong version
unexpected cross-domain status
```

All remain fail-closed.

# 11. scenario success regressions

After the new binding rule, successful recording owners must return snapshots exactly matching the runner's current authoritative state/version.

Preserve successful S1-S4 sequences:

```text
S1:
READY -> RUNNING -> ADMISSION_PENDING -> ACCEPTED

S2:
READY -> RUNNING -> ADMISSION_PENDING -> REWORK_REQUIRED

S3:
READY -> RUNNING -> BLOCKED

S4:
READY -> RUNNING -> ADMISSION_PENDING -> HUMAN_REQUIRED
```

No proof substitution or automatic retry.

# 12. static gate

Run:

```text
Python compile:
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/driver.py
tests/unit/scenarios/test_stockroom_capture_runner.py

Ruff:
same 3

git diff --check
```

Require all PASS and index empty.

Failure:

```text
STATIC_CHECK_FAILURE
→ STOP
```

No same-turn repair.

# 13. mandatory A1 unit

After static PASS:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider tests/unit/scenarios/test_stockroom_capture_runner.py -ra
```

Require exit 0.

Failure:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair.

# 14. mandatory B3 regression

After A1 unit PASS:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_owner_composition.py   tests/integration/scenarios/test_stockroom_binding.py -ra
```

Require exit 0.

# 15. final contract review

Require PASS for at least:

```text
OPERATION_SPECIFIC_STATUS_DOMAIN
UNEXPECTED_STATUS_FAIL_CLOSED
WORKFLOW_STATE_AUTHORITY_ONLY
NON_WORKFLOW_CANNOT_ADVANCE_WORKFLOW
NON_WORKFLOW_RESULT_BOUND_TO_CURRENT_STATE
NON_WORKFLOW_RESULT_BOUND_TO_CURRENT_VERSION
NON_WORKFLOW_MISMATCH_RECORDED
NON_WORKFLOW_MISMATCH_FAIL_CLOSED
INITIAL_READY_EXACT_STATE_VERSION
TRANSITION_EXACT_TARGET_NEXT_VERSION
S1_ACCEPT_PATH
S2_CONTROLLED_EVIDENCE_OMISSION
S3_NO_TOOL_BLOCKED_PATH
S4_HUMAN_PENDING_PATH
NO_PROOF_SUBSTITUTION
NO_AUTOMATIC_RETRY
UNKNOWN_FAIL_CLOSED
PREPARED_DRIVER_REMAINS_INERT
NO_PRODUCTION_OWNER_CONSTRUCTION
NO_PUBLIC_MODE
```

Success:

```text
20 / 20 PASS
```

# 16. strict no-runtime ceiling

Must remain:

```text
DB NOT_RUN
Docker NOT_RUN
real Stockroom process NOT_RUN
real materialization NOT_RUN
real provider/tool NOT_RUN
network NOT_RUN
HumanResult NOT_CREATED
real Judgment NOT_CREATED
actual scenario NOT_RUN
Git add/commit/push NOT_RUN
```

# 17. final workspace

Before Task lifecycle:

```text
prior governance:
12

A1 candidate:
3

current Cycle/Judgment:
2

total excluding active Task:
17 exact

index:
empty
```

Then move active Task to done.

Final:

```text
18 exact Git-visible paths
index empty
```

No other path.

# 18. evidence contract

executor_required:

- exact transport/repository gate
- exact predecessor/candidate identity
- two-path rework only
- frozen driver
- non-workflow current-state/version binding tests
- preserved operation-status tests
- preserved workflow tamper tests
- static PASS
- A1 unit PASS
- B3 regression PASS
- 20/20 contract review
- no-runtime proof
- exact final workspace
- outbound ZIP

forbidden:

- driver mutation
- bootstrap/config/shared-owner mutation
- DB/Docker/provider/tool/materializer real execution
- actual scenario
- Git staging/commit/push
- A2/P2-4/P3

# 19. mandatory stop

```text
DOWNLOAD_ZIP_MISSING
DOWNLOAD_ZIP_HASH_MISMATCH
DOWNLOAD_ZIP_CORRUPT
DOWNLOAD_TASK_MEMBER_MISSING
DOWNLOAD_TASK_PLACEMENT_FAILED
TRANSPORT_FAILURE
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
SCOPE_EXPANSION_REQUIRED
UNEXPECTED_FROZEN_PATH_DELTA
STATIC_CHECK_FAILURE
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

No same-turn repair after mandatory static/test failure.

# 20. export

Bundle folder:

```text
.aiassistant/reports/target/20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
NONWORKFLOW_SNAPSHOT_BINDING_VERIFICATION.md
STATUS_DOMAIN_VERIFICATION.md
WORKFLOW_STATE_AUTHORITY_VERIFICATION.md
SCENARIO_SEQUENCE_VERIFICATION.md
RUNNER_CONTRACT_VERIFICATION.md
TEST_VERIFICATION.md
```

Include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/driver.py
tests/unit/scenarios/test_stockroom_capture_runner.py
```

Create adjacent verified ZIP.

# 21. final ceiling

Success:

```text
capture-runner core:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

production owner/bootstrap integration:
NOT_STARTED

runtime prerequisites:
NOT_VERIFIED

actual scenario:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```
