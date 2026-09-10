# AISCC Command Center Judgment

## meta

- judgment_id: `20260910_1142_aiscc-p2-3-capture-runner-owner-status-state-authority-judgment-1`
- created_at: `2026-09-10T11:42:00+09:00`
- project: `AI Software Command Center (AISCC)`
- submitted_task: `.aiassistant/tasks/done/20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.md`
- submitted_bundle: `20260910_1039_aiscc-p2-3-actual-capture-runner-core-ruff-test-retry-1.zip`
- submitted_bundle_sha256: `81d2ee2237bf3d3864839c3893dfb5934eb84614706d49cc64035309c51d8c81`
- result_status: `HOLD_REWORK_REQUIRED`
- blocker: `CONTRACT_MISMATCH`
- root_cause: `OWNER_STATUS_AND_WORKFLOW_STATE_AUTHORITY_FAIL_OPEN`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`

# 판정

`1039` bundle transport/static/test evidence itself is valid, but A1 candidate is not accepted.

Direct bundle verification:

```text
ZIP readability / CRC:
PASS

top-level bundle:
1 exact

bundle members:
15

manifest non-self inventory:
14 / 14 SHA-256 + byte-size PASS

issued 1039 TASK/CYCLE/JUDGMENT:
3 / 3 exact

1039 runner formatting:
AST-equivalent to 1040 candidate

driver:
byte-frozen exact

test:
byte-frozen exact
```

Submitted ZIP:

```text
SHA-256:
81d2ee2237bf3d3864839c3893dfb5934eb84614706d49cc64035309c51d8c81
```

Reported tests:

```text
compile:
3 / 3 PASS

Ruff:
3 / 3 PASS

A1 unit:
14 PASS

B3 regression:
18 PASS

source-contract report:
12 / 12 PASS
```

These tests are admitted as executed evidence, but they do not close the Browser source-review defect below.

# Browser source-review blocker

Current runner helper:

```python
if result.status not in {"ADMITTED", "COMPLETED", "SATISFIED", "PENDING", "REJECTED"}:
    return False
state, version = result.workflow_state, result.state_version
return True
```

This is shared by every owner operation.

Two authority defects follow.

## 1. status domain is globally fail-open

Scenario-specific statuses are accepted as success for unrelated owners.

Examples current source can accept:

```text
INITIAL_READY -> PENDING
SECURITY/AUTHORIZE_RUNTIME -> REJECTED
MATERIALIZE -> SATISFIED
SUBMIT_RUNTIME_EVIDENCE -> REJECTED
JUDGMENT -> PENDING
```

Because `OwnerCallResult.status` is an unrestricted string and the shared helper uses a union of all positive/special statuses, an operation can continue on a status that is not valid for that operation.

This violates the A1 requirement:

```text
unexpected/denied/rejected owner result
→ stop fail-closed
→ no later owner calls
```

and the canonical security rule that unknown/invalid permission/authority outcomes cannot fail open.

## 2. non-workflow owners can overwrite workflow state/version

The same helper executes:

```python
state, version = result.workflow_state, result.state_version
```

after successful calls from:

```text
EXECUTION
SECURITY
RUNTIME
EVIDENCE
HUMAN
JUDGMENT
```

Therefore a non-workflow owner result can influence the `observed_state` / `observed_version` supplied to the next transition.

That crosses the accepted authority boundary:

```text
Judgment != TransitionDecision
Evidence != TransitionDecision
security/runtime result != TransitionDecision
```

The runner may record non-workflow owner projections for provenance, but only the workflow transition owner may advance the runner's authoritative workflow state/version.

# required correction

Rework only:

```text
MODIFY:
src/aiscc/scenarios/capture_runner.py
tests/unit/scenarios/test_stockroom_capture_runner.py

FROZEN:
src/aiscc/scenarios/driver.py
```

Required behavior:

```text
operation-specific accepted status
+
workflow state/version advancement only from workflow-authoritative operations
+
exact transition target/version validation
+
fail-closed on cross-domain or malformed owner status/state
```

The existing scenario sequencing and A1 architecture remain otherwise valid.

# phase state

```text
actual-capture runtime-entry audit:
ACCEPTED / COMPLETE

capture-runner core:
REWORK_REQUIRED

production owner/bootstrap integration:
NOT_STARTED

actual scenario:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

# session

This stays within the same A1 source/test implementation authority.

```text
fresh IDE Executor chat:
NOT_REQUIRED

Browser:
CONTINUE_CURRENT_BROWSER_SESSION

Handoff:
NOT_REQUIRED
```
