# AISCC Command Center Judgment

## meta

- judgment_id: `20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failure-judgment-1`
- created_at: `2026-09-10T00:20:00+09:00`
- project: `AI Software Command Center (AISCC)`
- submitted_task: `.aiassistant/tasks/done/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-candidate-adoption-qa-1.md`
- submitted_bundle: `20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-candidate-adoption-qa-1.zip`
- submitted_bundle_sha256: `30f276b212c8e7427fdbde96b4c30bf46c7fcce67bc54aef41e3a36a0672e63d`
- result_status: `HOLD_REWORK_REQUIRED`
- blocker: `TEST_FAILURE / CANDIDATE_REWORK_REQUIRED`
- root_cause: `B3_FINGERPRINT_CANONICALIZATION_AND_PROOF_HARNESS_DEFECTS`
- reject_cause: `none`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`

# 판정

`2330` adoption QA의 mandatory STOP은 적합하다.

Browser Command Center direct verification:

```text
ZIP readability / CRC:
PASS

top-level bundle:
1 exact

bundle members:
34

submitted ZIP SHA-256:
30f276b212c8e7427fdbde96b4c30bf46c7fcce67bc54aef41e3a36a0672e63d

issued 2330 TASK/CYCLE/JUDGMENT:
3 / 3 exact

frozen B3 candidate:
5 / 5 exact before/after QA

product/config/test mutation during QA:
none

Git add/commit/push:
NOT_RUN
```

# mandatory B3 result

Static:

```text
Python compile:
5 / 5 PASS

Ruff:
FAIL
I001 unsorted import block
tests/integration/scenarios/test_stockroom_binding.py:1

git diff --check:
PASS

index:
empty
```

Mandatory B3 tests:

```text
7 failed
6 passed
0 errors
exit 1
```

Per Task contract the Executor correctly stopped; targeted B2 regressions and bootstrap regression discovery were not run.

# defect 1 — canonical fingerprint numeric representation

All seven B3 test failures originate while constructing the canonical owner composition.

Current code:

```text
src/aiscc/scenarios/composition.py:_fingerprints
provider limits.total_seconds
= LocalStockroomProfile.profile.total_timeout_seconds
= float

canonical_sha256(...)
rejects floating-point values by contract
```

Observed failing line:

```text
composition.py:314
```

This is a B3 product defect.

B2's strict Stockroom profile contract uses whole-second finite limits for this field. B3 must encode that accepted semantic value into the repository canonical JSON subset without admitting arbitrary float representation.

Required resolution:

```text
validate total_timeout_seconds is finite, positive and exactly integral;
encode the canonical fingerprint value as an integer number of seconds;
reject a fractional/non-finite value fail-closed.
```

Do not change the canonical JSON/hash utility and do not stringify arbitrary floating-point values.

Tool/security fingerprint fields already use integer seconds and remain unchanged.

# defect 2 — integration proof observation window

The zero-side-effect integration test currently performs:

```text
owners = _owners()
prepared_root = bootstrap.build_stockroom_owner_preparation(...)

before installing runtime boundary spies
```

Therefore the required observation interval does not include owner/composition/bootstrap construction.

The test must install all spies before `_owners()` and before `build_stockroom_owner_preparation(...)`.

# defect 3 — incomplete zero-call boundary map

The 2330 QA identified omitted current mutation/dispatch boundaries.

At minimum the integration proof must include available current callables for:

```text
StockroomSummaryDispatcher.dispatch

PostgresExecutionRepository:
create_operation
advance_operation
store_private_protocol_item
reserve_execution_bounds
settle_execution_output
start_dispatch_if_fresh
fail_operation_before_side_effect
close_workflow_left_running
store_output_ref

PostgresHumanAuthorityRepository:
issue_current_gate_action_authority
expire_gate_if_needed
supersede_gate
create_producer_ref

EvidenceAdmissionService:
preserve_supplemental
invalidate_authority
```

and retain all already-mapped boundaries from the candidate.

If an exact named callable is absent at current HEAD, map the real current equivalent or report:

```text
NOT_APPLICABLE_CURRENT_OWNER_INTERFACE
```

Do not silently omit it.

# defect 4 — Ruff import order

The integration test has one deterministic lint defect:

```text
tests/integration/scenarios/test_stockroom_binding.py
I001 unsorted import block
```

Fix import ordering only as required by repository Ruff rules; do not use auto-fix.

# bounded rework authority

Only these two candidate paths may change:

```text
src/aiscc/scenarios/composition.py
tests/integration/scenarios/test_stockroom_binding.py
```

The following three candidate paths remain byte-frozen:

```text
src/aiscc/bootstrap.py
src/aiscc/scenarios/driver.py
tests/unit/scenarios/test_owner_composition.py
```

No B1/B2/config/shared-owner mutation is authorized.

# authorship

Candidate authorship remains:

```text
UNKNOWN
```

This is irrelevant to correctness admission once exact bytes are tested under Command Center authority, but it must not be rewritten as Executor authorship.

# phase state

```text
P2-3 Phase 1B-B3:
PREEXISTING_CANDIDATE / REWORK_REQUIRED

B3 accepted:
NO

B3 persisted:
NO

actual scenario capture:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

# session

The successor remains inside the same B3 candidate/rework authority.

```text
fresh IDE Executor chat:
NOT_REQUIRED

Browser:
CONTINUE_CURRENT_BROWSER_SESSION

Handoff:
NOT_REQUIRED
```
