# AISCC Command Center Judgment

## meta

- judgment_id: `20260910_1157_aiscc-p2-3-capture-runner-nonworkflow-snapshot-binding-judgment-1`
- created_at: `2026-09-10T11:57:00+09:00`
- project: `AI Software Command Center (AISCC)`
- submitted_task: `.aiassistant/tasks/done/20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1.md`
- submitted_bundle: `20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-rework-1.zip`
- submitted_bundle_sha256: `924018e5358bf6be43056f8bb436d25e301d99ff126f27fa9fdae6356ab5ad39`
- result_status: `HOLD_REWORK_REQUIRED`
- blocker: `CANONICAL_BINDING_MISMATCH`
- root_cause: `ACCEPTED_NON_WORKFLOW_RESULT_CAN_BE_STALE_OR_CROSS_VERSION`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`

# 판정

`1142` transport/static/test evidence는 유효하지만 A1 candidate는 아직 ACCEPT하지 않는다.

Direct verification:

```text
ZIP readability / CRC:
PASS

top-level bundle:
1 exact

bundle members:
17

required root documents:
11 / 11

manifest non-self entries:
16 / 16 exact SHA-256 + size

issued 1142 TASK/CYCLE/JUDGMENT:
3 / 3 exact

compile:
3 / 3 PASS

Ruff:
3 / 3 PASS

A1 unit:
40 PASS

B3 regression:
18 PASS

reported contract review:
19 / 19 PASS
```

Submitted ZIP:

```text
SHA-256:
924018e5358bf6be43056f8bb436d25e301d99ff126f27fa9fdae6356ab5ad39
```

# what 1142 correctly fixed

The candidate now correctly enforces:

```text
operation-specific exact status domains
workflow transition result exact target
workflow transition exact version+1
non-workflow result cannot ADVANCE authoritative local state/version
```

That closes the previous global-status and authority-overwrite defects.

# remaining canonical defect

The 1142 Task intentionally tested non-workflow results such as:

```text
security ADMITTED + workflow_state=ACCEPTED/state_version=999
materializer ADMITTED + workflow_state=BLOCKED/state_version=999
evidence ADMITTED + workflow_state=REJECTED/state_version=999
Judgment ADMITTED + workflow_state=FAILED/state_version=999
```

and required the runner to ignore those snapshots and continue.

That instruction was too weak against the canonical P1-1/P1-2/P1-6 binding model.

Accepted baseline requires:

```text
security capabilities:
bound to evaluated current WorkflowState/state_version

evidence/admission:
bound to source/current state/version

Judgment applicability:
current-version bound

event/projection mismatch:
fail closed / authority conflict
```

Therefore a non-workflow owner is forbidden to ADVANCE workflow authority, but an otherwise successful non-workflow result carrying a stale/cross-state/cross-version snapshot also cannot be admitted as usable orchestration output.

Correct invariant is:

```text
non-workflow owner success status
AND
result.workflow_state == current authoritative state
AND
result.state_version == current authoritative version
```

Only then may the runner continue.

Mismatch:

```text
record result for provenance
STOP fail-closed
no later calls
no retry
authoritative local state/version unchanged
```

# why this matters

Without this check, current source can continue with:

```text
SECURITY ADMITTED at version 999
EVIDENCE ADMITTED at wrong workflow state
JUDGMENT ADMITTED at stale/cross-version state
```

while merely ignoring the mismatch.

That conflicts with exact run/state/version binding and can later allow an A2 adapter to feed stale authority into a valid-looking orchestration sequence.

# exact rework scope

```text
MODIFY:
src/aiscc/scenarios/capture_runner.py
tests/unit/scenarios/test_stockroom_capture_runner.py

FROZEN:
src/aiscc/scenarios/driver.py
```

Preserve all operation-specific status checks and workflow-only advancement from 1142.

# phase state

```text
runtime-entry audit:
ACCEPTED / COMPLETE

capture-runner core:
REWORK_REQUIRED

production owner/bootstrap integration:
NOT_STARTED

actual runtime:
NOT_RUN

actual scenario:
NOT_STARTED

Replay:
NOT_STARTED
```

# session

Same A1 implementation authority.

```text
fresh IDE Executor chat:
NOT_REQUIRED

Browser:
CONTINUE_CURRENT_BROWSER_SESSION

Handoff:
NOT_REQUIRED
```
