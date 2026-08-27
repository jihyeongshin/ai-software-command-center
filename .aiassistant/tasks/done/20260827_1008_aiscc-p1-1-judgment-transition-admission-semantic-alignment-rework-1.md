# 작업지시서: P1-1 Judgment / Transition Admission Semantic Alignment Rework

## meta

- task_id: `20260827_1008_aiscc-p1-1-judgment-transition-admission-semantic-alignment-rework-1`
- created_at: `2026-08-27 10:08 KST`
- phase: `P1-1 — Core Domain / State Machine Design`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `Judgment / TransitionDecision / terminal admission semantic alignment`
- predecessor_task: `20260826_2157_aiscc-core-domain-and-state-machine-design-1`
- predecessor_result: `HOLD_REWORK_REQUIRED`
- predecessor_cycle: `.aiassistant/records/aiscc/cycles/20260827_1008_aiscc-p1-1-core-domain-state-machine-design-hold-1.cycle.md`
- product_runtime_status_before: `NOT_IMPLEMENTED`
- P1_2_status: `BLOCKED_UNTIL_P1_1_ACCEPTED`

## 현재 상태

The predecessor candidate established a strong partial baseline:

- `WorkRun` as System-owned authoritative aggregate
- exact 9-state candidate
- separate `ExecutionStatus`, `HumanGateStatus`, `JudgmentStatus`, `RuntimeMode`
- request/evaluation/decision/mutation separation
- `state_version` stale/concurrency guard
- append-only transition provenance and recovery semantics
- runtime mode vs workflow state separation
- future owner handoffs

Command Center did NOT reopen those decisions generally.

The current blocker is an exact semantic inconsistency:

```text
AISCC_ORCHESTRATION section 4.3:
Judgment ref is required before ACCEPTED / REJECTED / REWORK_REQUIRED admission

BUT

transition matrix ACCEPTED rows:
no Judgment guard

AND

AISCC_ARCHITECTURE information flow:
state mutation precedes Judgment
```

This rework must resolve that contradiction before Human design review.

## 이번 턴 목표

1. Define one authoritative semantic relationship among:
   - `Judgment`
   - `JudgmentStatus`
   - `TransitionRequest`
   - `TransitionEvaluation`
   - `TransitionDecision`
   - authoritative state mutation
2. Make `AISCC_ARCHITECTURE.md` and `AISCC_ORCHESTRATION.md` express the same ordering.
3. Ensure terminal/rework state admission cannot silently collapse:
   - evidence sufficiency
   - Human result
   - semantic Judgment
   - mechanical transition admission
4. Update the exact transition matrix guards/provenance accordingly.
5. Resolve the `RUNNING → REWORK_REQUIRED` vs current `REWORK_REQUIRED` wording mismatch.
6. Preserve the predecessor's accepted partial design scope unless a correction is necessary to achieve consistency.
7. Produce corrected P1-1 design candidate and Executor report/export.
8. Leave Human acceptance pending.

## 비목표

- reopen product thesis
- reopen prior-art boundary
- redesign the entire 9-state set without demonstrated necessity
- add new workflow states merely to fix wording
- state-machine implementation
- persistence/database implementation
- P1-2 security design
- P1-3 safeguard implementation
- P1-4 kernel implementation
- P1-6 evidence implementation
- P1-7 Human Gate implementation
- product source
- Git commit/push
- deployment/provider/network/credential action
- Browser Project Source sync

## 허용 범위

allowed_paths:

```text
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/reports/target/20260827_1008_aiscc-p1-1-judgment-transition-admission-semantic-alignment-rework-1/**
.aiassistant/tasks/active/20260827_1008_aiscc-p1-1-judgment-transition-admission-semantic-alignment-rework-1.md
.aiassistant/tasks/done/20260827_1008_aiscc-p1-1-judgment-transition-admission-semantic-alignment-rework-1.md
```

Do not modify current state/decision/queue records in the Executor turn.
Command Center owns terminal Cycle and accepted-state persistence after Human review.

allowed_actions:

- exact canonical/source read
- update the two P1-1 candidate docs
- narrow static consistency checks
- `git status`
- `git diff -- <two candidate paths>`
- `git diff --check`
- SHA-256
- target export generation
- active → done Task lifecycle after executor-required work is complete

## 절대 금지

- product/runtime source implementation
- state-machine code
- DB/schema/API
- security/sandbox implementation
- P1-2/P1-3 execution
- dependency install
- network/provider call
- credential/API key/billing action
- browser runtime
- Browser Project Source mutation
- Git add/commit/push/remote operation
- Human acceptance claim

## 읽을 문서

Read exact paths:

1. `.aiassistant/rules/AISCC_AGENTS.md`
2. `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
3. `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
4. `.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md`
5. `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
6. `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md`
7. `.aiassistant/records/aiscc/DECISION_REGISTER.md`
8. `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
9. `.aiassistant/rules/AISCC_ARCHITECTURE.md`
10. `.aiassistant/rules/AISCC_ORCHESTRATION.md`
11. `.aiassistant/records/aiscc/cycles/20260827_1008_aiscc-p1-1-core-domain-state-machine-design-hold-1.cycle.md`
12. `.aiassistant/tasks/done/20260826_2157_aiscc-core-domain-and-state-machine-design-1.md`

This is the minimum authoritative context set.

Do not bulk-read unrelated historical Tasks/Cycles or generated mirror bundles.

## required semantic decision A — Judgment vs TransitionDecision

The corrected design MUST define these as separate concepts.

Minimum invariant:

```text
JUDGMENT
!= TRANSITION_DECISION
```

Required distinction:

### `Judgment`

Semantic task outcome decision.

It must answer what the current work outcome means under the Task/evidence/Human policy, for example:

```text
ACCEPT
REJECT
REWORK
```

The exact canonical values/names may remain aligned with `JudgmentStatus`.

The design MUST specify:

- authoritative judgment owner policy
- when a Human result is an input rather than the Judgment itself
- when/if System may produce deterministic judgment
- how Agent reviewer output remains only proposal/candidate
- immutable/supersession provenance

### `TransitionDecision`

Mechanical System decision:

```text
given authoritative current state/version
+ requested target
+ applicable guards
+ admitted semantic refs
→ ADMITTED or DENIED
```

It MUST NOT itself substitute for the semantic Judgment.

Likewise:

```text
Judgment exists
!= state automatically mutated
```

System transition admission must still verify current state/version and target-specific guards.

## required semantic decision B — exact ordering

Choose one exact canonical flow and apply it in BOTH design documents.

The expected default correction is:

```text
Executor/Agent output
→ Evidence Candidate
→ Evidence Admission
→ Review/Judgment Candidate
→ Human Gate when required
→ authoritative Judgment admitted
→ TransitionRequest
→ TransitionEvaluation
→ TransitionDecision
→ atomic authoritative state mutation
→ Cycle admission
→ NextAction
```

A materially different ordering is allowed only if it preserves all accepted P0-2 authority/proof boundaries and is explicitly justified.

Do not put authoritative Judgment both before and after terminal transition.

## required semantic decision C — terminal / rework guards

The exact transition matrix MUST align with the chosen Judgment semantics.

At minimum re-evaluate these rows:

```text
ADMISSION_PENDING → ACCEPTED
HUMAN_REQUIRED → ACCEPTED
ADMISSION_PENDING → REJECTED
HUMAN_REQUIRED → REJECTED
ADMISSION_PENDING → REWORK_REQUIRED
HUMAN_REQUIRED → REWORK_REQUIRED
REWORK_REQUIRED → REJECTED
RUNNING → REWORK_REQUIRED
```

If authoritative Judgment is required for semantic terminal/rework routing, introduce exact abstract guards such as:

```text
G_JUDGMENT_ACCEPTED
G_JUDGMENT_REJECTED
G_JUDGMENT_REWORK
```

or an equally explicit canonical equivalent.

Do not hide Judgment requirement in prose while omitting it from the matrix.

Every affected matrix row must state:

- judgment requirement
- Human result requirement when applicable
- denied result
- resulting state/version
- provenance emitted

## required semantic decision D — Human result relationship

Explicitly define:

```text
HumanResult
!= Judgment
```

unless Human is explicitly the designated authoritative Judgment owner for that Task.

If the design allows both Human-owned and deterministic System-owned Judgment,
define the selection policy in the TaskContract/policy reference.

Human silence/absence remains non-success.

Wrong owner/stale/wrong-proof Human result remains non-admitted.

## required semantic decision E — REWORK semantics

Resolve:

```text
REWORK_REQUIRED meaning:
"current submission cannot be accepted..."
```

vs allowed:

```text
RUNNING → REWORK_REQUIRED
```

Either:

- broaden state semantics to a correctable current attempt/submission outcome and define the judgment/reason required for RUNNING rework, or
- remove that transition and use an existing coherent path.

Do not add a new state solely for this.

## required cross-document consistency table

Add to one candidate doc or Executor report a compact table:

| semantic fact | AISCC_ARCHITECTURE | AISCC_ORCHESTRATION | result |
|---|---|---|---|
| Judgment owner | exact | exact | MATCHED |
| Judgment timing | exact | exact | MATCHED |
| HumanResult relation | exact | exact | MATCHED |
| TransitionDecision role | exact | exact | MATCHED |
| ACCEPT guard | exact | exact | MATCHED |
| REJECT guard | exact | exact | MATCHED |
| REWORK guard | exact | exact | MATCHED |
| Cycle timing | exact | exact | MATCHED |

No row may remain `AMBIGUOUS`.

## evidence contract

### executor_required

#### `STATIC_SOURCE`

pass:

- exact 12 required paths read
- predecessor HOLD Cycle applied
- no historical Browser-chat authority substituted

#### `SEMANTIC_ALIGNMENT`

pass:

- `Judgment != TransitionDecision`
- `HumanResult` relation exact
- one authoritative ordering
- both candidate docs match

#### `TRANSITION_MATRIX_ALIGNMENT`

pass:

- all affected transitions contain exact Judgment/Human guards
- no prose-only hidden guard
- state definitions and predecessors/outgoing matrix agree
- denied paths do not silently mutate alternate state

#### `CROSS_BASELINE_CONSISTENCY`

pass:

- Agent output != system state
- Agent claim != admitted evidence
- Human-owned evidence != executor-completed
- terminal transition remains System-admitted
- Human gate applied when required
- `WorkRun ACCEPTED != project CLOSED`
- P1-2/P1-3/P1-6/P1-7/P1-8 ownership not absorbed

#### `DOCUMENT_INTEGRITY`

pass:

- UTF-8
- fence parity
- no unintended control characters
- no broken placeholder
- `git diff --check` or equivalent

### reuse_allowed

- predecessor 9-state model and concurrency/persistence design:
  `REUSED_CANDIDATE`, not independently accepted canonical yet
- P0-2/P0-4/P0-5 accepted baselines:
  `REUSED_ACCEPTED`

### human_owned

`HUMAN_VERIFICATION`

After corrected candidate:

- exact core domain names
- 9-state set
- corrected Judgment/transition relationship
- exact transition matrix
- terminal/Human/rework semantics
- concurrency/persistence contract
- future owner handoff

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

### not_required

- build/unit/integration/DB/HTTP/browser/security runtime
- provider/model
- deployment
- mirror sync

### forbidden

- implementation
- Git index/commit/push
- provider/network/credential/deployment
- Human acceptance claim

## proof non-substitution

```text
EvidenceSatisfied
!= JudgmentAccepted

HumanApproved
!= state mutation

JudgmentAccepted
!= TransitionDecision admitted

TransitionDecision
!= Judgment

Agent review
!= authoritative Judgment

Executor completed
!= WorkRun ACCEPTED

WorkRun ACCEPTED
!= Project CLOSED
```

## workflow transition expectation

- initial_state: `P1_1_REWORK_READY`
- expected_terminal_candidate: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- transition_authority: `SYSTEM / COMMAND_CENTER`
- Agent may decide Human acceptance: `No`

## accept 기준

- predecessor strong candidate scope retained unless exact reason given
- Judgment/TransitionDecision semantic contradiction removed
- Architecture and Orchestration ordering identical
- exact transition matrix expresses judgment guards
- Human result relationship exact
- REWORK definition/matrix coherent
- state set remains finite and non-exploded
- concurrency/persistence/runtime-mode boundaries preserved
- no implementation
- no forbidden action
- Human review remains pending

## hold/reject 기준

- Judgment still appears both before and after state mutation
- ACCEPTED transition can occur from evidence sufficiency alone despite separate Judgment contract
- Human approval silently substitutes for semantic Judgment without an explicit owner rule
- TransitionDecision treated as Judgment or vice versa
- matrix and prose disagree
- `RUNNING → REWORK_REQUIRED` remains semantically incompatible
- state set is unnecessarily expanded to avoid the contradiction
- security/evidence/Human implementation scope creep
- forbidden Git/provider/deployment action
- false Human acceptance claim

## 보고서 필수 항목

- task path
- repository HEAD/worktree before/after
- exact read inventory
- predecessor HOLD issue mapping
- changed files
- exact Judgment owner/status semantics
- HumanResult relation
- corrected authoritative ordering
- affected transition rows before/after summary
- cross-document consistency table
- REWORK semantic resolution
- retained predecessor candidate scope
- evidence classification
- forbidden-not-run
- document integrity
- Human pending
- rollback
- preserved exact paths
- next recommendation: Human P1-1 review, NOT P1-2 execution yet

## export bundle

Target:

```text
.aiassistant/reports/target/20260827_1008_aiscc-p1-1-judgment-transition-admission-semantic-alignment-rework-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `.aiassistant/rules/AISCC_ARCHITECTURE.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`

## Task lifecycle

```text
.aiassistant/tasks/active/20260827_1008_aiscc-p1-1-judgment-transition-admission-semantic-alignment-rework-1.md
→
.aiassistant/tasks/done/20260827_1008_aiscc-p1-1-judgment-transition-admission-semantic-alignment-rework-1.md
```

`done` means Executor submission ready, not Human acceptance.

## preserved artifacts

Preserve after this rework turn:

- predecessor done Task
- predecessor HOLD Cycle
- this rework done Task
- eventual terminal P1-1 Cycle
- two design candidates only if accepted; otherwise next rework supersedes them

## next action

Corrected candidate submission → Command Center judgment → Human review.

P1-2 remains blocked until P1-1 `ACCEPTED / CLOSED`.
