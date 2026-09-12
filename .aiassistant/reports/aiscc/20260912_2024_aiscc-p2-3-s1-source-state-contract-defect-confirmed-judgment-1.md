# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_2024_aiscc-p2-3-s1-source-state-contract-defect-confirmed-judgment-1`
- created_at: `2026-09-12T20:24:31+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_task: `20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-retry-1`
- reviewed_result_zip_sha256: `12b40fd577e01d557b84fc997d101ea67399c8e75d473347c87d76888cdf3a0b`
- result_status: `HOLD_REWORK_REQUIRED / SOURCE_CONTRACT_DEFECT_CONFIRMED`
- reject_cause: `STOCKROOM_RUNTIME_EVIDENCE_EXPECTED_STATE_STALE`
- cycle_record_action: `create`
- execution_mode: `MANUAL_COMMAND_CENTER`
- source_mirror_sync: `not-required`

# Browser judgment

1954 Executor의 `POLICY_CONFLICT_INVESTIGATION_REQUIRED` STOP을 정당하게 입장한다.

Browser result verification:

```text
result ZIP:
21 members / one top-level / CRC PASS

manifest:
20 / 20 exact

TASK root == canonical done Task:
PASS

contract:
10 PASS / 28 BLOCKED_REQUIRED_EVIDENCE

Docker/private-file/ACL/DB/builder/prepare_capture/runner:
NOT_EXECUTED

WorkRun:
NOT_CREATED

Git/source/state mutation:
none
```

# confirmed source defect

Current source facts:

```text
StockroomCaptureRunner.run:
RUNNING_TO_ADMISSION_PENDING is admitted before submit_runtime_evidence()

StockroomCaptureOwnerAdapter.submit_runtime_evidence:
_current(prepared, WorkflowState.RUNNING)

_current:
reads authoritative durable WorkflowKernel state and fails closed on mismatch
```

The orchestration baseline requires:

```text
RUNNING → ADMISSION_PENDING
guard: G_EXECUTOR_SUBMISSION

then from ADMISSION_PENDING:
evidence review/admission
Judgment
G_EVIDENCE
ADMISSION_PENDING → ACCEPTED
```

Security baseline also defines `ADMISSION_PENDING` as submission/evidence-review-only and makes prior RUNNING execution
capabilities unusable there.

Therefore the stale precondition is the adapter's `RUNNING` expectation.
The runner's durable transition order must not be reversed to hide this mismatch.

# authorized correction

Narrow source correction only:

```text
StockroomCaptureOwnerAdapter.submit_runtime_evidence
authoritative current-state precondition:
RUNNING
→
ADMISSION_PENDING
```

Preserve:

```text
_current fail-closed behavior
RUNNING_TO_ADMISSION_PENDING ordering
P1-4 transition authority
P1-6 evidence authority
P1-7 Judgment separation
security action/state matrix
```

Add a focused regression proving the source-owned runner/adapter boundary.

No private S1 execution is authorized by this Judgment.
