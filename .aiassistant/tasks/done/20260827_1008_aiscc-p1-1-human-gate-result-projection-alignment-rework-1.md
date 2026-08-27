# 작업지시서: P1-1 Human Gate Result Projection Alignment Rework

## meta

- task_id: `20260827_1008_aiscc-p1-1-human-gate-result-projection-alignment-rework-1`
- created_at: `2026-08-27 10:08 KST`
- phase: `P1-1 — Core Domain / State Machine Design`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `HumanGate lifecycle / HumanResult outcome projection`
- predecessor_task: `20260827_1008_aiscc-p1-1-judgment-transition-admission-semantic-alignment-rework-1`
- predecessor_result: `HOLD_REWORK_REQUIRED`
- predecessor_cycle: `.aiassistant/records/aiscc/cycles/20260827_1008_aiscc-p1-1-human-gate-result-projection-hold-1.cycle.md`
- P1_2_status: `BLOCKED_UNTIL_P1_1_ACCEPTED`

## 현재 상태

Do NOT reopen the predecessor corrections.

The following are retained unless this Task demonstrates a direct conflict:

- exact 9-state WorkflowState set
- `Judgment != TransitionDecision`
- `HumanResult != Judgment`
- authoritative Judgment before outcome TransitionRequest
- exact Judgment guards on ACCEPT/REJECT/REWORK transition rows
- `state_version` stale/concurrency contract
- restart/recovery provenance
- RuntimeMode / WorkflowState separation
- P1 future-owner handoffs

Current remaining gap:

```text
HumanResult = APPROVE | REJECT | REWORK

HumanGateStatus =
NOT_REQUIRED | PENDING | APPROVED | REJECTED
```

`HumanResult=REWORK` has no exact gate-status projection.

## 이번 턴 목표

1. Define one exact Human gate lifecycle model.
2. Define one exact HumanResult outcome model.
3. Define the mapping between HumanResult admission and HumanGate durable projection.
4. Ensure:
   - Human gate lifecycle state is not silently equivalent to Task semantic Judgment;
   - Human approval is not automatically WorkRun acceptance;
   - Human rejection is not automatically WorkRun rejection;
   - Human rework has an exact durable representation.
5. Align both:
   - `.aiassistant/rules/AISCC_ARCHITECTURE.md`
   - `.aiassistant/rules/AISCC_ORCHESTRATION.md`
6. Update every affected transition-matrix row and prose reference.
7. Keep P1-7 implementation detail deferred.
8. Produce corrected candidate/report/export with Human review still pending.

## 비목표

- redesign the 9 WorkflowStates
- reopen Judgment/TransitionDecision ordering
- product/runtime implementation
- state-machine implementation
- P1-2/P1-3/P1-4/P1-6/P1-7 implementation
- DB/API/schema
- Git add/commit/push
- provider/network/credential/deployment
- Browser Project Source sync

## 허용 범위

allowed_paths:

```text
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/reports/target/20260827_1008_aiscc-p1-1-human-gate-result-projection-alignment-rework-1/**
.aiassistant/tasks/active/20260827_1008_aiscc-p1-1-human-gate-result-projection-alignment-rework-1.md
.aiassistant/tasks/done/20260827_1008_aiscc-p1-1-human-gate-result-projection-alignment-rework-1.md
```

allowed_actions:

- exact canonical/source read
- modify only the two P1-1 design candidates
- narrow consistency/static checks
- `git status`
- `git diff -- <two design paths>`
- `git diff --check`
- SHA-256
- target export
- active → done lifecycle after executor work completes

## 절대 금지

- application/runtime source mutation
- new WorkflowState merely to solve this gap
- P1-2/P1-3 execution
- dependency installation
- network/provider/browser/credential action
- Git add/commit/push/remote
- deployment
- Browser Project Source mutation
- Human acceptance claim

## 읽을 문서

Read exact paths:

1. `.aiassistant/rules/AISCC_AGENTS.md`
2. `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
3. `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
4. `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
5. `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md`
6. `.aiassistant/records/aiscc/DECISION_REGISTER.md`
7. `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
8. `.aiassistant/rules/AISCC_ARCHITECTURE.md`
9. `.aiassistant/rules/AISCC_ORCHESTRATION.md`
10. `.aiassistant/records/aiscc/cycles/20260827_1008_aiscc-p1-1-human-gate-result-projection-hold-1.cycle.md`
11. `.aiassistant/tasks/done/20260827_1008_aiscc-p1-1-judgment-transition-admission-semantic-alignment-rework-1.md`

Do not bulk-read unrelated historical Tasks/Cycles.

## required semantic decision

The corrected candidate MUST make this relation exact:

```text
HumanGate lifecycle
!= HumanResult semantic outcome
!= authoritative Judgment
!= TransitionDecision
!= WorkflowState
```

### Required question 1 — HumanGateStatus

Choose one canonical status set.

Examples are illustrative, not mandatory:

#### outcome-bearing

```text
NOT_REQUIRED
PENDING
APPROVED
REWORK
REJECTED
```

or

#### outcome-neutral lifecycle

```text
NOT_REQUIRED
PENDING
RESOLVED
```

A different set is allowed if exact and coherent.

### Required question 2 — HumanResult

Keep or explicitly redefine the exact HumanResult outcome set.

Current candidate:

```text
APPROVE
REWORK
REJECT
```

For every outcome specify:

- submitted by whom
- admission owner
- owner/applicability/version checks
- resulting HumanGateStatus
- whether an authoritative Judgment may now be created
- what it does NOT directly mutate

### Required question 3 — mapping table

Both candidate docs must agree on an exact mapping table equivalent to:

| HumanResult | admitted gate projection | semantic effect | does NOT imply |
|---|---|---|---|
| APPROVE | exact status | input to policy-selected Judgment | WorkRun ACCEPTED |
| REWORK | exact status | input to HOLD_REWORK_REQUIRED Judgment | automatic REWORK_REQUIRED mutation |
| REJECT | exact status | input to REJECTED Judgment | automatic WorkRun REJECTED |

No `gate resolved` free-text without a canonical status.

### Required question 4 — BLOCKED interaction

When `HUMAN_REQUIRED → BLOCKED` preserves or suspends a gate, define:

- whether `HumanGateStatus` stays `PENDING`;
- whether a separate suspension flag/status exists;
- how recovery resumes;
- whether HumanResult submitted while blocked is admissible or deferred.

Do not invent runtime/UI behavior beyond the domain semantic minimum.

### Required question 5 — transition matrix

Re-evaluate at least:

```text
HUMAN_REQUIRED → ACCEPTED
HUMAN_REQUIRED → REWORK_REQUIRED
HUMAN_REQUIRED → REJECTED
HUMAN_REQUIRED → BLOCKED
BLOCKED → READY
BLOCKED → REWORK_REQUIRED
REWORK_REQUIRED → READY
REWORK_REQUIRED → REJECTED
```

Every affected row must reference the exact gate/result projection when applicable.

## evidence contract

### executor_required — `STATIC_SOURCE`

- exact 11 paths read
- predecessor HOLD applied
- no stale/historical Browser chat authority substituted

### executor_required — `HUMAN_GATE_MODEL`

Pass when:

- exact HumanGateStatus set exists
- exact HumanResult set exists
- complete mapping exists
- no HumanResult outcome is unprojected
- lifecycle status and semantic outcome are not conflated

### executor_required — `MATRIX_ALIGNMENT`

Pass when:

- all Human-required matrix rows use the same canonical model
- no free-text-only `gate resolved`
- BLOCKED/recovery semantics do not create hidden gate outcome
- Human silence remains non-success

### executor_required — `CROSS_BASELINE_CONSISTENCY`

Preserve:

```text
HumanResult != Judgment
Judgment != TransitionDecision
Human approval != WorkRun ACCEPTED
Human rejection != WorkRun REJECTED
Human rework != automatic REWORK_REQUIRED mutation
```

### executor_required — `DOCUMENT_INTEGRITY`

- UTF-8
- fence parity
- no unintended control chars
- no unresolved placeholder
- `git diff --check` or equivalent

### reuse_allowed

- previous 9-state / Judgment / transition / concurrency / persistence candidate:
  `REUSED_CANDIDATE`
- accepted P0 baselines:
  `REUSED_ACCEPTED`

### human_owned

`HUMAN_VERIFICATION`

After corrected candidate, Human reviews the complete P1-1 design.

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

### not_required

- build/unit/integration/DB/HTTP/browser/security runtime
- provider/model/deployment
- Project Source mirror refresh

### forbidden

- implementation
- Git index/commit/push
- P1-2/P1-3
- provider/network/credential/deployment
- Human acceptance claim

## proof non-substitution

```text
HumanGateStatus=RESOLVED/APPROVED/etc
!= Task accepted

HumanResult=APPROVE
!= Judgment=ACCEPTED
!= WorkflowState=ACCEPTED

HumanResult=REWORK
!= Judgment=HOLD_REWORK_REQUIRED
!= WorkflowState=REWORK_REQUIRED

HumanResult=REJECT
!= Judgment=REJECTED
!= WorkflowState=REJECTED
```

Each arrow requires its own admitted record/decision according to the canonical ordering.

## workflow transition expectation

- initial_state: `P1_1_REWORK_READY`
- expected_terminal_candidate: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- transition_authority: `SYSTEM / COMMAND_CENTER`
- Agent may decide Human acceptance: `No`

## accept 기준

- one exact HumanGate lifecycle model
- one exact HumanResult outcome model
- total mapping for APPROVE/REWORK/REJECT or replacement exact outcomes
- BLOCKED/suspension semantics exact enough for P1-7
- matrix and prose aligned
- previous Judgment/transition correction preserved
- 9 WorkflowStates not expanded without demonstrated need
- no implementation/scope creep
- Human review pending

## hold/reject 기준

- REWORK HumanResult still has no canonical gate projection
- `APPROVED` ambiguously means Task accepted
- gate status and HumanResult are treated as interchangeable without explicit semantics
- Human result directly mutates WorkflowState
- BLOCKED silently drops/resolves Human gate
- matrix and status definitions disagree
- previous Judgment/TransitionDecision correction regresses
- implementation/P1-2 scope creep
- forbidden action

## 보고서 필수 항목

- task/repository snapshot
- exact read inventory
- previous HOLD issue mapping
- selected HumanGateStatus model and rationale
- HumanResult exact model
- total result→gate mapping
- BLOCKED/suspension semantics
- affected matrix rows before/after
- cross-document consistency table
- preserved prior P1-1 scope
- evidence classifications
- forbidden-not-run
- Human pending
- document integrity
- rollback
- preserved exact paths
- next recommendation: Human P1-1 review if candidate passes

## export bundle

Target:

```text
.aiassistant/reports/target/20260827_1008_aiscc-p1-1-human-gate-result-projection-alignment-rework-1/
```

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `.aiassistant/rules/AISCC_ARCHITECTURE.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`

## Task lifecycle

```text
.aiassistant/tasks/active/20260827_1008_aiscc-p1-1-human-gate-result-projection-alignment-rework-1.md
→
.aiassistant/tasks/done/20260827_1008_aiscc-p1-1-human-gate-result-projection-alignment-rework-1.md
```

`done` means submission ready, not accepted.

## preserved artifacts

Preserve:

- previous P1-1 done Tasks
- previous P1-1 HOLD Cycles
- this rework done Task
- eventual terminal P1-1 Cycle
- design candidates only if accepted

## next action

Corrected candidate → Command Center judgment → Human P1-1 review.

P1-2 remains blocked until P1-1 `ACCEPTED / CLOSED`.
