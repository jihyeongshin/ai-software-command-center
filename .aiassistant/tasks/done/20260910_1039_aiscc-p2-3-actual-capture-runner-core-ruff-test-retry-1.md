# 작업지시서: P2-3 actual-capture runner core Ruff/test retry

## meta

- task_id: `20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1`
- created_at: `2026-09-10T10:39:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_FORMAT_REWORK / UNIT_REGRESSION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-3 owner-only capture runner core retry`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf`
- required_base_tree: `992a15a33e8b34cc3da35f44bd846ceddccb2526`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

The 1040 A1 candidate stopped at the mandatory static gate on one runner-only Ruff E501.

This Task does not authorize a runner redesign or test modification.

It authorizes one AST-equivalent line-wrap correction and completion of the previously blocked static/test evidence.

# 1. inbound ZIP bootstrap

The Browser Short Prompt ZIP SHA-256 is the transport integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md

CYCLE:
20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-retry-entry-1.cycle.md
SHA-256:
56de671d96c839d91d8457ed3c131f152627211ed825489a0222399041b844b6
destination:
.aiassistant/records/aiscc/cycles/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-retry-entry-1.cycle.md

JUDGMENT:
20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-judgment-1.md
SHA-256:
5a97033467671e9cbeddc66f8d3010cc8e45bab32d11be1307d8415e8b999983
destination:
.aiassistant/reports/aiscc/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md
```

Read it, then place/hash-verify current Cycle/Judgment.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
```

After exact canonical transport, inbound cleanup refusal is non-blocking.

# 2. repository gate — exact dirty baseline

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

Expected Git-visible set excluding current active Task is exact 11 paths:

- `.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md`
- `src/aiscc/scenarios/capture_runner.py`
- `src/aiscc/scenarios/driver.py`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`
- `.aiassistant/records/aiscc/cycles/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1039_aiscc-p2-3-capture-runner-core-static-failure-judgment-1.md`

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

Require exact starting A1 candidate:

- `src/aiscc/scenarios/capture_runner.py`  `415b75d5be21b1c6538da55d765f081b66127c5a04626e6bd96f1243434036d8`
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
src/aiscc/scenarios/capture_runner.py
```

may change.

Frozen exact bytes:

```text
src/aiscc/scenarios/driver.py
SHA-256:
9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6

tests/unit/scenarios/test_stockroom_capture_runner.py
SHA-256:
6f8f39c48775244c15aa49990090d4dffd132c18d41d14b6cc39061305b14e7b
```

No other source/config/test path may change.

If another path requires modification:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 5. exact authorized runner edit

Before editing:

1. parse `src/aiscc/scenarios/capture_runner.py` with `ast.parse`;
2. retain `ast.dump(tree, include_attributes=False)` or structurally equivalent dump.

Correct only Ruff E501 at the final S1/S2 target assignment around original line 262:

```text
target = WorkflowState.REWORK_REQUIRED if request.scenario_id == S2 else WorkflowState.ACCEPTED
```

Use a normal multi-line expression consistent with repository style.

Do not change:

```text
condition
target values
branch order
owner call order
state/version handling
authority_refs
failure behavior
```

After editing parse again and require:

```text
RUNNER_AST_BEFORE == RUNNER_AST_AFTER
```

If false:

```text
RUNNER_SEMANTICS_CHANGED
→ STOP
```

Do not run an autoformatter/auto-fix.

# 6. frozen-path verification

Immediately after the edit verify:

```text
src/aiscc/scenarios/driver.py
SHA-256:
9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6

tests/unit/scenarios/test_stockroom_capture_runner.py
SHA-256:
6f8f39c48775244c15aa49990090d4dffd132c18d41d14b6cc39061305b14e7b
```

Any mismatch:

```text
UNEXPECTED_FROZEN_PATH_DELTA
→ STOP
```

# 7. mandatory static gate

Run non-mutating checks on all three A1 paths:

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

If any fail:

```text
STATIC_CHECK_FAILURE
→ STOP
```

No same-turn second repair.

# 8. mandatory A1 unit

Only after static PASS, run exactly:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider tests/unit/scenarios/test_stockroom_capture_runner.py -ra
```

Require:

```text
exit 0
failed 0
errors 0
```

Report exact passed/skipped count.

If nonzero:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair.

# 9. mandatory B3 regression

Only after A1 unit PASS, run exactly:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_owner_composition.py   tests/integration/scenarios/test_stockroom_binding.py -ra
```

Require exit 0.

If nonzero:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair.

# 10. bounded direct driver regression discovery

Search only:

```text
tests/unit/scenarios/**
tests/integration/scenarios/**
```

for direct imports/calls of:

```text
PreparedStockroomDriver
StockroomOwnerDependencies
StockroomDriverRequest
```

The 1040 result reported no additional direct driver regression beyond the mandatory B3 modules.

Confirm from current source.

If none:

```text
NO_ADDITIONAL_DIRECT_DRIVER_REGRESSION
```

If clear additional zero-side-effect direct modules exist, run only that bounded set.

If ambiguous or runtime-bearing:

```text
TEST_SCOPE_AMBIGUOUS
→ STOP
```

# 11. executed scenario-sequence proof

From the passing A1 unit evidence require executed coverage for:

```text
S1:
READY → RUNNING → ADMISSION_PENDING → ACCEPTED

S2:
READY → RUNNING → ADMISSION_PENDING → REWORK_REQUIRED
required evidence candidate omitted
no substitution
no automatic retry

S3:
READY → RUNNING → BLOCKED
no materialization
no provider/tool/Docker path
no Judgment

S4:
READY → RUNNING → ADMISSION_PENDING → HUMAN_REQUIRED
Human gate reached
HumanResult absent
Judgment absent
automatic continuation absent
```

All authoritative outputs must originate from recording owner fakes matching existing owner contracts.

# 12. authority non-substitution proof

Require executed tests establish:

```text
TransitionDecision:
not fabricated by runner

AdmittedEvidenceRef:
not fabricated by runner

HumanResult:
not fabricated

Judgment:
not fabricated

Agent claim:
not converted to HumanResult/HUMAN_OWNED evidence

tool/runtime output:
not treated as admitted evidence

Judgment ref:
not treated as transition authority without owner transition call
```

# 13. failure / unknown proof

Require executed cases for at least:

```text
transition denied
security/grant denied
materializer failure
provider/tool unknown outcome
quarantine-required outcome
evidence admission rejected
Human gate denial
Judgment denial
```

For each:

```text
no later owner calls
no auto retry
no substitute artifact
```

Unknown/quarantine path must not execute a second provider/tool/process attempt.

# 14. final source contract review

After tests, report PASS/FAIL for:

```text
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
12 / 12 PASS
```

# 15. strict no-runtime ceiling

This retry must perform:

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

Unit/fake-owner calls are not runtime evidence.

# 16. final candidate identity/scope

Require:

```text
capture_runner.py:
changed only by AST-equivalent formatting

driver.py:
exact frozen hash

test_stockroom_capture_runner.py:
exact frozen hash

A1 path set:
3 exact

other source/config/test delta:
0

index:
empty

git diff --check:
PASS
```

# 17. Task lifecycle / final workspace

Before current Task lifecycle:

```text
1008 governance:
3

1040 governance:
3

A1 candidate:
3

current Cycle/Judgment:
2

total excluding active Task:
11 exact
```

Then move:

```text
.aiassistant/tasks/active/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md
→
.aiassistant/tasks/done/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md
```

Final:

```text
12 exact Git-visible paths
index empty
```

No other path.

# 18. evidence contract

executor_required:

- inbound transport
- exact 11-path workspace gate
- exact predecessor/candidate identity
- AST-equivalent runner formatting edit
- frozen driver/test identity
- static checks PASS
- A1 unit PASS
- B3 regression PASS
- bounded driver regression result
- executed scenario sequence proof
- authority non-substitution proof
- failure/unknown proof
- 12/12 source contract review
- strict no-runtime proof
- exact final workspace
- outbound ZIP

reuse_allowed:

- 1040 source candidate
- accepted 1008 runtime-entry audit
- persisted B1/B2/B3/settlement evidence

human_owned:

```text
S4 HumanResult:
HUMAN_PENDING / outside A1

public distribution/license:
HUMAN_PENDING
```

forbidden:

- runner semantic redesign
- driver mutation
- test mutation
- production bootstrap/config/shared-owner mutation
- DB/Docker/provider/tool/materializer real execution
- actual scenario
- Git add/commit/push
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
RUNNER_SEMANTICS_CHANGED
UNEXPECTED_FROZEN_PATH_DELTA
STATIC_CHECK_FAILURE
TEST_SCOPE_AMBIGUOUS
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

No same-turn repair after mandatory static/test failure.

Inbound cleanup refusal after canonical transport remains non-blocking.

# 20. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
RUNNER_FORMAT_EQUIVALENCE.md
RUNNER_CONTRACT_VERIFICATION.md
SCENARIO_SEQUENCE_VERIFICATION.md
AUTHORITY_NON_SUBSTITUTION_VERIFICATION.md
TEST_VERIFICATION.md
```

Include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
all three final A1 source/test paths
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

# 21. final ceiling

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

Do not start A2 or runtime work in this Task.
