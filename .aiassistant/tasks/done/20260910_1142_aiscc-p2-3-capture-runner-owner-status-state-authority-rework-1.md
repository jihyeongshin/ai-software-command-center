# 작업지시서: P2-3 capture-runner owner status/state authority rework

## meta

- task_id: `20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1`
- created_at: `2026-09-10T11:42:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `ORCHESTRATION_AUTHORITY_REWORK / UNIT_REGRESSION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-3 owner-only capture runner status/workflow-state authority`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf`
- required_base_tree: `992a15a33e8b34cc3da35f44bd846ceddccb2526`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

The 1039 A1 tests passed, but Browser source review found two fail-open authority defects in the generic result helper:

```text
1. operation-specific status domains are collapsed into one global accepted set
2. non-workflow owners can overwrite authoritative workflow state/version
```

Fix only these defects and add direct regression proof.

Do not begin A2 or production/runtime work.

# 1. inbound ZIP bootstrap

The Browser Short Prompt ZIP SHA-256 is the transport integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1.md

CYCLE:
20260910_1142_aiscc-p2-3-capture-runner-owner-status-authority-rework-entry-1.cycle.md
SHA-256:
d23c0d5108aa26d7b66b02dcbb0dc047eedd871ba5f208fb7b675758d71d2b63
destination:
.aiassistant/records/aiscc/cycles/20260910_1142_aiscc-p2-3-capture-runner-owner-status-authority-rework-entry-1.cycle.md

JUDGMENT:
20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-judgment-1.md
SHA-256:
079d0593ef198b4f3adebd01bb2e74aebbed645e0550563e90b5b92aea1c5f5c
destination:
.aiassistant/reports/aiscc/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1.md
```

Read it, then place/hash-verify current Cycle/Judgment.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
```

After exact canonical transport, inbound cleanup refusal is non-blocking.

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

Expected Git-visible set excluding current active Task is exact 14 paths:

- `.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-judgment-1.md`
- `src/aiscc/scenarios/capture_runner.py`
- `src/aiscc/scenarios/driver.py`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`
- `.aiassistant/records/aiscc/cycles/20260910_1142_aiscc-p2-3-capture-runner-owner-status-authority-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/stash/reset/overwrite.

# 3. exact predecessor/candidate identity

Require exact 1008 governance:

- `.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md`  `11db99ba9b22ed8e6dddab96d49d1a9207b928b846c93e53bcd88e48a8d10f52`
- `.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md`  `3cc310ccfe052307a906fe2524db6176f7af0d38ba53616096df6ece0ff581a0`
- `.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md`  `6cb059aa4206ac5e1f00789e8adbc955f574bf84c71b2e551c4f23a414e51ff0`

Require exact 1040 governance:

- `.aiassistant/tasks/done/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md`  `0109756f710d26b625b42ec90c98f0dd585cad36445473e9fb9e4e20e964d3d2`
- `.aiassistant/records/aiscc/cycles/20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md`  `6a6195c8c430a9d292c765f6a044992970b945518c25a12e506737873999bbbb`
- `.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md`  `48e84d88626bcd5804ff4f3f9c580c7f9d4efa28ea974adb5f69498afa8555c3`

Require exact 1039 governance:

- `.aiassistant/tasks/done/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md`  `ed429af33012ecc73613badd4fc743181b5570accccd931be91e24f0bcf81dbf`
- `.aiassistant/records/aiscc/cycles/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-retry-entry-1.cycle.md`  `56de671d96c839d91d8457ed3c131f152627211ed825489a0222399041b844b6`
- `.aiassistant/reports/aiscc/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-judgment-1.md`  `5a97033467671e9cbeddc66f8d3010cc8e45bab32d11be1307d8415e8b999983`

Require exact starting A1 candidate:

- `src/aiscc/scenarios/capture_runner.py`  `21417673f6831c46694c785e6879142e1cc69dff503210fa22dfb75eef122a09`
- `src/aiscc/scenarios/driver.py`  `9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`  `6f8f39c48775244c15aa49990090d4dffd132c18d41d14b6cc39061305b14e7b`

Any mismatch:

```text
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

# 4. exact mutation authority

Only:

```text
MODIFY:
src/aiscc/scenarios/capture_runner.py
tests/unit/scenarios/test_stockroom_capture_runner.py
```

Frozen exact path:

```text
src/aiscc/scenarios/driver.py
SHA-256:
9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6
```

No other source/config/test path may change.

If another path is required:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 5. operation-specific result acceptance

Remove the global semantic rule equivalent to:

```text
ADMITTED | COMPLETED | SATISFIED | PENDING | REJECTED
accepted for every operation
```

Each owner call must accept only its own expected status.

For the current A1 contract, preserve these exact success/special statuses unless direct current source proves a narrower equivalent:

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

Any other status at that operation:

```text
record returned owner result as progress
do not treat it as success
do not advance workflow state/version
STOP
no later owner calls
no retry
```

Do not normalize an unexpected status into a valid one.

# 6. workflow state/version authority

The runner may record the `workflow_state` and `state_version` fields returned by any owner for provenance.

But authoritative local `state/version` used for later TransitionRequest observation may advance only from workflow-authoritative results.

Required:

```text
initial_ready:
validate exact READY + expected initial version
then establish authoritative state/version

request_transition:
validate exact requested target
validate exact next monotonic version
then advance authoritative state/version
```

Non-workflow owner calls must NOT overwrite local authoritative `state/version`, including:

```text
create_attempt
security context
security grant
materialization
execution
evidence submission/evaluation
agent-claim rejection
Human gate
Judgment
policy blocker
```

Those results may carry state/version snapshots, but they are non-authoritative for workflow advancement.

# 7. exact transition admission validation

For every `request_transition` call require all:

```text
status == ADMITTED
result.workflow_state == requested target
result.state_version == observed_version + 1
```

If any condition fails:

```text
TRANSITION_RESULT_MISMATCH
→ runner STOPPED result
→ no later calls
```

Do not fabricate a corrected TransitionDecision.

For `initial_ready`, require:

```text
status == ADMITTED
workflow_state == READY
state_version == request.run_binding.expected_initial_state_version
```

Mismatch must stop before attempt creation.

# 8. progress recording on rejected/malformed result

A rejected/unexpected owner result should remain visible in:

```text
StockroomCaptureProgressRef
```

for diagnostics/provenance.

But recording it must not imply:

```text
admission
workflow mutation
authority substitution
```

The stopped result must report the last workflow-authoritative state/version, not the rejected non-workflow owner's claimed state/version.

# 9. preserve existing S1-S4 semantics

After the authority fix, retain:

```text
S1:
READY → RUNNING → ADMISSION_PENDING → ACCEPTED

S2:
READY → RUNNING → ADMISSION_PENDING → REWORK_REQUIRED
runtime evidence candidate omitted
no substitution
no auto retry

S3:
READY → RUNNING → BLOCKED
no materializer/provider/tool/Docker/Judgment

S4:
READY → RUNNING → ADMISSION_PENDING → HUMAN_REQUIRED
agent claim rejected
HumanResult absent
Judgment absent
```

Do not redesign scenario ordering outside what is necessary for sections 5-8.

# 10. required unit regression expansion

Modify:

```text
tests/unit/scenarios/test_stockroom_capture_runner.py
```

Preserve existing passing cases and add direct tests for status-domain fail-closed behavior.

At minimum execute cases equivalent to:

```text
initial_ready returns PENDING
→ STOP before create_attempt

security/grant returns REJECTED
→ STOP

materialize returns SATISFIED or PENDING
→ STOP

execute returns ADMITTED instead of COMPLETED
→ STOP

submit_runtime_evidence returns REJECTED
→ STOP before evaluate

submit_static_policy_evidence returns REJECTED
→ STOP before evaluate/blocker

Human gate returns ADMITTED instead of PENDING
→ STOP

Judgment returns PENDING/REJECTED
→ STOP before final transition

policy blocker returns SATISFIED/REJECTED
→ STOP before BLOCKED transition
```

For each:

```text
failing call occurs exactly once
no later calls
no retry
stopped result retains previous workflow-authoritative state/version
```

# 11. non-workflow state/version tampering regression

Extend the recording fake so individual owner results can return a forged state/version while keeping an otherwise accepted operation status.

Required executed cases:

```text
security accepted status + forged ACCEPTED/state_version=999
materializer accepted status + forged BLOCKED/state_version=999
evidence accepted status + forged REJECTED/state_version=999
Judgment accepted status + forged FAILED/state_version=999
```

The next workflow transition must still receive the last true workflow-authoritative:

```text
observed_state
observed_version
```

from the preceding admitted workflow transition.

No non-workflow owner may move it.

# 12. workflow-result tampering regression

Required executed cases:

```text
initial_ready:
ADMITTED but wrong workflow_state
→ STOP

initial_ready:
ADMITTED but wrong version
→ STOP

transition:
ADMITTED but wrong target state
→ STOP

transition:
ADMITTED but same/skipped/wrong version
→ STOP
```

No later owner calls.

# 13. existing failure coverage

Preserve existing executed failure/unknown cases:

```text
transition denied
security/grant denied
materializer failure
provider/tool unknown
quarantine required
evidence evaluation rejected
Human gate denied
Judgment denied
```

No auto retry/no later calls.

# 14. static gate

After mutation run:

```text
Python compile:
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/driver.py
tests/unit/scenarios/test_stockroom_capture_runner.py

Ruff:
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/driver.py
tests/unit/scenarios/test_stockroom_capture_runner.py

git diff --check
```

Require:

```text
compile:
3 / 3 PASS

Ruff:
3 / 3 PASS

git diff --check:
PASS

index:
empty
```

If any fails:

```text
STATIC_CHECK_FAILURE
→ STOP
```

No same-turn repair after mandatory static failure.

# 15. mandatory A1 unit

Only after static PASS:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider tests/unit/scenarios/test_stockroom_capture_runner.py -ra
```

Require exit 0.

Report exact count.

If nonzero:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair.

# 16. mandatory B3 regression

Only after A1 unit PASS:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_owner_composition.py   tests/integration/scenarios/test_stockroom_binding.py -ra
```

Require exit 0.

If nonzero:

```text
TEST_FAILURE
→ STOP
```

# 17. final contract review

Require PASS for:

```text
OPERATION_SPECIFIC_STATUS_DOMAIN
UNEXPECTED_STATUS_FAIL_CLOSED
WORKFLOW_STATE_AUTHORITY_ONLY
NON_WORKFLOW_STATE_VERSION_IGNORED_FOR_AUTHORITY
INITIAL_READY_EXACT_STATE_VERSION
TRANSITION_EXACT_TARGET_NEXT_VERSION
FAILED_RESULT_RECORDED_NOT_ADMITTED
RUNNER_ORCHESTRATION_ONLY
EXISTING_OWNER_AUTHORITY_PRESERVED
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

Success requires:

```text
19 / 19 PASS
```

# 18. strict no-runtime ceiling

This Task must perform:

```text
DB:
NOT_RUN

Docker CLI/daemon/image:
NOT_RUN

real Stockroom process:
NOT_RUN

real materialization:
NOT_RUN

real provider/tool:
NOT_RUN

network:
NOT_RUN

HumanResult:
NOT_CREATED

real Judgment:
NOT_CREATED

actual scenario:
NOT_RUN

Git add/commit/push:
NOT_RUN
```

Only unit/fake boundaries are allowed.

# 19. final workspace

Before current Task lifecycle require:

```text
1008 governance:
3

1040 governance:
3

1039 governance:
3

A1 source/test:
3

current Cycle/Judgment:
2

total excluding active Task:
14 exact

index:
empty
```

Then move:

```text
.aiassistant/tasks/active/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1.md
→
.aiassistant/tasks/done/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1.md
```

Final:

```text
15 exact Git-visible paths
index empty
```

No other path.

# 20. evidence contract

executor_required:

- inbound transport
- exact 14-path workspace gate
- exact predecessor/candidate identity
- exact two-path rework
- frozen driver identity
- operation-specific status tests
- non-workflow state/version authority tests
- transition-result tamper tests
- existing failure regression
- static PASS
- A1 unit PASS
- B3 regression PASS
- 19/19 contract review
- strict no-runtime proof
- exact final workspace
- outbound ZIP

reuse_allowed:

- 1039 successful scenario/failure evidence where exact unchanged behavior remains
- accepted 1008 audit
- persisted Phase 1B/settlement evidence

human_owned:

```text
S4 HumanResult:
HUMAN_PENDING

public distribution/license:
HUMAN_PENDING
```

forbidden:

- driver mutation
- production bootstrap/config/shared-owner mutation
- DB/Docker/provider/tool/materializer real execution
- actual scenario
- Git add/commit/push
- A2/P2-4/P3

# 21. mandatory stop

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

Inbound cleanup refusal after canonical transport remains non-blocking.

# 22. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
STATUS_DOMAIN_VERIFICATION.md
WORKFLOW_STATE_AUTHORITY_VERIFICATION.md
SCENARIO_SEQUENCE_VERIFICATION.md
AUTHORITY_NON_SUBSTITUTION_VERIFICATION.md
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

Create adjacent outbound ZIP.

Use Windows extended-length path handling if needed.

Require:

```text
one top-level directory
readable / CRC PASS
required roots present
manifest coverage
folder/archive byte equality
```

# 23. final ceiling

Success:

```text
P2-3 actual-capture runner core:
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

Do not start A2/runtime work in this Task.
