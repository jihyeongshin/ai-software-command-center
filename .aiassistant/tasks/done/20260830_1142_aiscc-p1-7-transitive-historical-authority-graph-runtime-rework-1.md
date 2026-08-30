# 작업지시서: P1-7 Transitive Historical Authority Graph Runtime Rework

## meta

- task_id: `20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-runtime-rework-1`
- created_at: `2026-08-30T11:42:00+09:00`
- phase: `P1-7 Human Gate and Judgment`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT`
- expected_start_head: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted_design_commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- accepted_design_terminal_commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted_design_sha256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- predecessor_runtime_path_count: `19`
- predecessor_runtime_aggregate_sha256: `36823a442e1b4e9eaa72b270f36d3686c500dc23fdea8c0765ccd56c103ab82b`
- p1_7_runtime_status: `REWORK_REQUIRED / HUMAN_PENDING`
- p1_8_status: `NOT_STARTED`
- public_bounded_live_release: `NOT_RELEASED`

---

# 1. current state

The 0225 rework successfully closed direct historical row/event provenance gaps.

Do not reopen:

```text
HumanResult same-proposal replay:
projection-independent

Judgment same-proposal replay:
projection-independent

HumanResult:
ADMITTED + RESOLVED direct lineage checked

Judgment:
Evaluation + ISSUED + policy/owner dependency checked

corrupt direct provenance:
fail closed

historical replay:
separate from current guard effectiveness
```

Preserve accepted design and Stage 0 commits:

```text
238b0b41460c2504fd3244eadb06809d8692a60f
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

Current runtime remains uncommitted.

Place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-hold-1.cycle.md
```

---

# 2. predecessor verification

Before mutation verify:

```text
HEAD ==
c87cfc75f14476e10b4a02a2ab0bd295720a85a0

accepted design SHA ==
22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549

current 19-path runtime aggregate ==
36823a442e1b4e9eaa72b270f36d3686c500dc23fdea8c0765ccd56c103ab82b
```

Mismatch:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

---

# 3. load-bearing rule

Extend the 0225 rule from direct provenance to transitive immutable dependencies:

```text
historical row self-hash
!= complete authority provenance

direct event lineage
!= complete transitive authority provenance

referenced authority
must itself be valid immutable historical authority
```

But preserve:

```text
historical validity
!= current effectiveness
```

Do not require historical objects to be current projections or usable guards.

---

# 4. FINDING-1 — projection-independent immutable HumanGate issuance verifier

Create an exact helper/service equivalent to:

```text
_verify_human_gate_historical_provenance_in_session(...)
```

It must validate a HumanGate without requiring its current `HumanGateProjectionRow`.

At minimum reconstruct/validate:

```text
HumanGateRow exists

serialized_ref / human_gate_id / human_gate_version coherent

TaskContract id/version
work_run_id
opened_from_state/version
bound_state_version
purpose id/version
authority policy id/version
principal selector
authority id/version
opened_at
expires_at
supersedes_gate_ref

gate_fingerprint is exactly recomputable from immutable gate-opening inputs
```

Because the normal gate fingerprint includes the opening target/use, and that target is recoverable from
P1-4 opening provenance, the verifier must not simply trust `gate_fingerprint`.

---

# 5. normal OPENED gate → exact P1-4 transition provenance

For a non-correction HumanGate:

```text
supersedes_gate_ref == None
```

require exactly one initial:

```text
HumanGateAuthorityEventRow
event_kind = OPENED
prior_revision = 0
new_revision = 1
```

Its immutable payload must match:

```text
HumanGateRow opening_transition_request_id
HumanGateRow opening_transition_decision_id
bound_state = HUMAN_REQUIRED
bound_state_version = HumanGateRow.bound_state_version
created_at = HumanGateRow.opened_at
```

Then load exact P1-4 durable provenance:

```text
TransitionRequestRow
TransitionEvaluationRow
TransitionDecisionRow
```

Verify at minimum:

```text
request.transition_request_id == gate payload

request.task_contract_id/version == gate
request.work_run_id == gate
request.observed_state == gate.opened_from_state
request.observed_state_version == gate.opened_from_state_version
request.target_state == HUMAN_REQUIRED

decision.transition_request_id == request
decision transition/evaluation relation complete
decision.outcome == ADMITTED
decision.resulting_state == HUMAN_REQUIRED
decision.resulting_state_version == gate.bound_state_version
decision.decided_at == gate.opened_at

gate OPENED event transition request/decision IDs == exact rows

gate fingerprint recomputed from:
gate identity/version
purpose
TaskContract
work_run
source state/version
target HUMAN_REQUIRED
authority policy
principal selector
expires_at
```

If the P1-4 repository exposes a canonical projection-independent transition provenance verifier, reuse it.

Do not duplicate P1-4 transition truth with weaker semantics.

Missing/corrupt transition provenance:

```text
→ PROVENANCE_INCOMPLETE / AUTHORITY_CONFLICT
→ historical gate invalid
```

---

# 6. OPENED_CORRECTION gate provenance

For:

```text
supersedes_gate_ref != None
```

require exactly one initial:

```text
OPENED_CORRECTION
0 → 1
```

and verify immutable row/event coherence:

```text
event.supersedes_gate_ref == row.supersedes_gate_ref

event.bound_state == HUMAN_REQUIRED

event.bound_state_version == row.bound_state_version

created_at == row.opened_at
```

Load the predecessor gate by `supersedes_gate_ref`.

Require the predecessor to have a coherent:

```text
SUPERSEDED
```

event pointing to this replacement gate with exact revision/timestamp relation.

The predecessor must itself have valid immutable historical gate issuance provenance.

Correction validation must not require the predecessor to remain current.

## cycle protection

Gate correction chains are finite historical graphs.

Implement deterministic cycle protection:

```text
visited gate refs/ids
or
bounded graph traversal with exact duplicate detection
```

Any cycle:

```text
→ AUTHORITY_CONFLICT
```

Do not rely on Python recursion without a cycle guard.

If the accepted V1 design bounds correction depth, enforce that exact bound.
Otherwise no arbitrary shallow maximum should reject legitimate history; visited-set cycle detection is preferred.

---

# 7. HumanResult historical verifier consumes immutable gate verifier

Update:

```text
_verify_human_result_historical_provenance_in_session(...)
```

so it no longer treats `HumanGateRow` existence + basic field equality as enough.

Required order equivalent:

```text
verify HumanResult row/fingerprint

→ verify referenced immutable HumanGate historical provenance

→ verify exact result ↔ gate immutable Task/run/purpose/state authority

→ verify one ADMITTED HumanResult event

→ verify exact RESOLVED HumanGate event for this result

→ return historical HumanResult
```

Additional exact checks should include:

```text
HumanGateRow.bound_state_version == HumanResult.state_version

RESOLVED event is chronologically/revision-consistent with the gate's prior immutable event history

result.gate_authority_revision == exact gate revision immediately before RESOLVED
```

Do not require current gate projection.

---

# 8. FINDING-2 — Judgment correction graph counterpart provenance

Refactor Judgment historical provenance so a correction relation connects valid historical Judgments, not
self-hash-only rows.

A clean implementation may split:

```text
_verify_judgment_base_issuance_provenance(...)
_verify_judgment_correction_graph(...)
```

## 8.1 predecessor of a corrected Judgment

If:

```text
value.supersedes_judgment_ref != None
```

require:

```text
predecessor exists

predecessor complete immutable base issuance provenance is valid:
row
Evaluation
ISSUED
policy
owner-specific immutable dependencies

predecessor SUPERSEDED relation points exactly to value

revision / work_run / TaskContract / state / target / timestamp relation exact
```

Do not accept predecessor self-hash alone.

## 8.2 replacement of a superseded historical Judgment

If the current historical Judgment has a `SUPERSEDED` event:

```text
replacement exists

replacement complete immutable base issuance provenance is valid

replacement.supersedes_judgment_ref == current ref

revision/work_run/Task/state/target/timestamp relation exact
```

The replacement need not be current projection.

## 8.3 cycle protection

Correction graph traversal must detect:

```text
A supersedes B
B supersedes A

or any longer cycle
```

and fail closed.

Avoid infinite recursion between predecessor and replacement validation.

Recommended:

```text
base issuance verification:
does not traverse correction graph

graph verifier:
walks refs with visited set
and calls base verifier per node
```

This makes the authority model reviewable.

---

# 9. corruption/fail-closed proofs

Fresh PostgreSQL proofs are mandatory.

## HUMAN_GATE_HISTORICAL_PROVENANCE

At minimum:

```text
HumanGateRow + RESOLVED event but missing OPENED
→ HumanResult historical replay fails closed

HumanGateRow gate_fingerprint mismatch
→ fail closed

OPENED event wrong request/decision ID
→ fail closed

missing opening TransitionRequest
→ fail closed

missing/wrong opening TransitionDecision
→ fail closed

decision not ADMITTED / wrong resulting state/version
→ fail closed

correction gate with missing predecessor
→ fail closed

correction gate predecessor missing SUPERSEDED relation
→ fail closed

gate correction cycle
→ fail closed
```

## JUDGMENT_CORRECTION_GRAPH

At minimum:

```text
corrected Judgment whose predecessor is self-hash-valid but missing Evaluation/ISSUED
→ replay fails closed

superseded Judgment whose replacement is self-hash-valid but missing Evaluation/ISSUED
→ replay fails closed

SUPERSEDED relation points to wrong replacement
→ fail closed

revision mismatch
→ fail closed

Judgment correction cycle
→ fail closed
```

Use:

```text
PROVENANCE_INCOMPLETE
AUTHORITY_CONFLICT
```

according to missing vs contradictory provenance.

No auto-repair.

---

# 10. positive historical proofs

Preserve:

```text
valid original gate/result
→ historical HumanResult replay works after WorkRun moved on

valid corrected gate/result chain
→ historical replay works while no current authority is implied

valid corrected Judgment
→ historical replay works

valid superseded Judgment
→ historical replay works

all valid replays:
no new row/event/evaluation/projection mutation
```

Separately:

```text
stale/superseded historical object
→ still denied as current G_HUMAN_* / G_JUDGMENT_* authority
```

---

# 11. preserve 0051 / 0148 / 0225 closures

Fresh regression must keep all previously closed behavior, including:

```text
cross-scope authority rejection

durable current gate action authority

Judgment policy / COMMAND_CENTER authority

expiry lifecycle and post-lock time authority

global HumanResult/Judgment ID serialization

HumanResult proposal idempotency

Judgment historical replay/currentness separation

direct HumanResult ADMITTED/RESOLVED verification

direct Judgment Evaluation/ISSUED/policy/Human/CommandCenter verification

P1-6 PRE_HUMAN binding

P1-4 exclusive transition ownership
```

---

# 12. implementation scope

Primary expected paths:

```text
src/aiscc/human/repository.py
src/aiscc/judgment/authority.py

tests/integration/human/test_postgres_human_gate_judgment.py
```

Narrow P1-4 persistence model/repository import/use is allowed only for reading/verifying existing durable
transition provenance:

```text
src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py
```

Do not change P1-4 transition semantics.

Migration `20260829_0004` should remain unchanged unless an actually missing durable field is proven.

The current schema already stores gate opening request/decision IDs, so prefer verification over schema expansion.

Governance/report:

```text
.aiassistant/records/aiscc/cycles/
20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-hold-1.cycle.md

.aiassistant/tasks/active/
20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-runtime-rework-1.md

.aiassistant/tasks/done/
20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-runtime-rework-1.md

.aiassistant/reports/target/
20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-runtime-rework-1/**
```

---

# 13. forbidden

Do not modify:

```text
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/
20260829_2328_aiscc-p1-7-human-gate-and-judgment-design-final-acceptance-1.cycle.md
```

No:

```text
P1-8

WorkflowState / transition matrix changes

P1-6 evidence semantics changes

real provider / external IdP / credentialed network

deployment / Public Live

git add / commit / push
```

Runtime remains uncommitted.

---

# 14. evidence contract

## executor_required

```text
STATIC_SOURCE

POSTGRESQL_INTEGRATION

HUMAN_GATE_HISTORICAL_PROVENANCE

P1_4_OPENING_TRANSITION_PROVENANCE

HUMAN_RESULT_TRANSITIVE_PROVENANCE

JUDGMENT_CORRECTION_GRAPH

CYCLE_DETECTION

CORRUPTION_FAIL_CLOSED

HISTORICAL_REPLAY

CURRENT_GUARD_ANTI_REPLAY

RESTART

SECURITY_EXPORT

0051_REGRESSION

0148_REGRESSION

0225_REGRESSION

P1_4_REGRESSION

P1_6_REGRESSION
```

## reuse_allowed

Reuse predecessor evidence only for unchanged behavior after fresh regression.

## human_owned

```text
P1-7 runtime final acceptance
→ HUMAN_PENDING
```

## forbidden

```text
P1-8
direct WorkflowState mutation
real provider/network/credential
runtime Git commit
```

---

# 15. mandatory stop

STOP on:

```text
HEAD drift

accepted design SHA drift

predecessor 19-path aggregate drift

need to change accepted P1-7 design

current durable P1-4 transition schema is insufficient to verify gate opening provenance

transitive graph cannot be validated without changing accepted authority semantics

need to weaken append-only protection

unrelated dirty collision
```

If P1-4 durable provenance is insufficient:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not replace P1-4 transition provenance with a P1-7 synthetic assertion.

---

# 16. accept criteria

All must hold:

```text
historical HumanGate provenance verifies exact immutable opening authority

normal OPENED gate binds real admitted P1-4 request/decision

correction gate binds valid predecessor + SUPERSEDED lineage

gate fingerprint is reconstructed/verified from immutable authority inputs

HumanResult replay consumes valid historical gate provenance

Judgment predecessor/replacement correction nodes have valid base issuance provenance

gate and Judgment correction cycles fail closed

missing/corrupt transitive dependency fails closed

valid historical chains replay without requiring current projections

replay causes no new authority mutation

stale historical objects remain unusable as current guards

0051/0148/0225 regressions PASS

P1-4/P1-6 regressions PASS

P1-8 remains NOT_STARTED

provider/network/credential/deployment = 0

Stage 1 Git commit = none
```

---

# 17. report requirements

Report exact:

1. task path
2. start/final HEAD
3. accepted design SHA
4. predecessor 19-path aggregate
5. 1142 HOLD Cycle placement
6. HumanGate historical verifier checks
7. normal gate P1-4 opening request/decision verification
8. correction gate predecessor/SUPERSEDED verification
9. gate fingerprint reconstruction
10. gate graph cycle detection
11. HumanResult verifier integration
12. Judgment base issuance vs correction graph split
13. predecessor complete-provenance proof
14. replacement complete-provenance proof
15. Judgment graph cycle detection
16. corrupt/missing gate OPENED proof
17. wrong/missing P1-4 transition proof
18. corrupt correction gate proof
19. corrupt predecessor/replacement Judgment proof
20. positive corrected historical replay
21. current guard rejection
22. restart
23. 0051 regression
24. 0148 regression
25. 0225 regression
26. P1-4 regression
27. P1-6 regression
28. final runtime path count / aggregate SHA
29. provider/network/credential actions
30. P1-8 = NOT_STARTED
31. Git actions = none
32. human verification = HUMAN_PENDING
33. preserved exact paths
34. next recommendation

---

# 18. export

Target:

```text
.aiassistant/reports/target/
20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-runtime-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include all changed runtime/test paths and the 1142 HOLD Cycle.

Manifest:

```text
actual copied-byte SHA
64 lowercase hex
source/copy identity PASS
runtime aggregate from actual exported runtime bytes
```

---

# 19. lifecycle / Git

Start:

```text
.aiassistant/tasks/active/
20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-runtime-rework-1.md
```

Finish:

```text
.aiassistant/tasks/done/
20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-runtime-rework-1.md
```

No Git add/commit/push.

Expected final HEAD:

```text
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

---

# 20. preserved exact paths

Must preserve:

```text
.aiassistant/rules/
AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/records/aiscc/cycles/
20260829_2328_aiscc-p1-7-human-gate-and-judgment-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_0051_aiscc-p1-7-runtime-authority-binding-policy-expiry-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_0148_aiscc-p1-7-runtime-idempotency-global-identity-and-expiry-toctou-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-runtime-rework-1.md

.aiassistant/tasks/done/
20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-runtime-rework-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

---

# 21. final state

Successful rework submission:

```text
P1-7 Design:
ACCEPTED / CLOSED

P1-7 Runtime:
REWORKED_CANDIDATE / HUMAN_PENDING

P1-8:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Next:

```text
Command Center runtime re-review
→ Human final P1-7 runtime review only after PASS
```
