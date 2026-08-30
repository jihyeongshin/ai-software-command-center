# 작업지시서: P1-7 / P1-4 Opening Transition Root Provenance Runtime Rework

## meta

- task_id: `20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-runtime-rework-1`
- created_at: `2026-08-30T12:41:00+09:00`
- phase: `P1-7 Human Gate and Judgment`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT / P1-4_TRANSITION_PROVENANCE`
- expected_start_head: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted_design_commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- accepted_design_terminal_commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted_design_sha256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- predecessor_runtime_path_count: `19`
- predecessor_runtime_aggregate_sha256: `5211024c632934cee625529d626da097905f8270efa4727f013b7b76828bb106`
- p1_7_runtime_status: `REWORK_REQUIRED / HUMAN_PENDING`
- p1_8_status: `NOT_STARTED`

---

# 1. current state

The 1142 rework closes its intended HumanGate/HumanResult/Judgment transitive graph findings.

Do not reopen:

```text
gate OPENED / OPENED_CORRECTION distinction

gate correction predecessor/SUPERSEDED lineage

gate/Judgment cycle detection

HumanResult direct ADMITTED/RESOLVED provenance

Judgment direct Evaluation/ISSUED/policy/owner provenance

Judgment predecessor/replacement base issuance provenance

historical validity != current guard effectiveness

0051 / 0148 / 0225 closures
```

The remaining gap is the root of the normal HumanGate graph:

```text
HumanGate
→ P1-4 opening TransitionRequest/Evaluation/Decision
```

Current implementation verifies this only as a locally coherent triple.

It must instead consume canonical P1-4 historical transition provenance.

Place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-hold-1.cycle.md
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
5211024c632934cee625529d626da097905f8270efa4727f013b7b76828bb106
```

Any runtime identity drift:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

---

# 3. frozen authority rule

Preserve:

```text
P1-4 owns TransitionDecision and WorkflowState mutation

P1-6 owns admitted evidence/G_EVIDENCE

P1-7 owns Human/Judgment authority

P1-7 may consume P1-4 historical transition truth
P1-7 must not recreate or weaken it
```

New exact invariant:

```text
TransitionRequestRow + TransitionEvaluationRow + TransitionDecisionRow
locally matching each other
!= canonical P1-4 admitted transition provenance
```

---

# 4. implement/reuse canonical P1-4 historical transition provenance verifier

First inspect existing P1-4 persistence/runtime source.

Current repository already has exact equivalents of:

```text
PostgresWorkRunRepository._verify_consistency_in_session(...)
_request_fingerprint(...)
accepted TransitionMatrix / TransitionEvaluator contracts
TransitionRequestRow / TransitionEvaluationRow / TransitionDecisionRow
```

Prefer extracting/reusing a P1-4-owned verifier rather than duplicating P1-4 logic under `src/aiscc/human/**`.

A clean target is an exact equivalent of:

```text
verify_historical_transition_provenance(
    session,
    transition_request_id,
) -> VerifiedHistoricalTransition
```

owned by:

```text
src/aiscc/persistence/**
or
src/aiscc/workflow/**
```

The exact API/name may differ.

No change to P1-4 transition semantics is authorized.

---

# 5. immutable TransitionRequest integrity

The verifier must load the exact request and prove its persisted immutable identity.

At minimum verify:

```text
transition_request_id
project_id
TaskContract id/version
work_run_id
observed state/version
target state
requester identity/type
runtime mode
evidence refs
human_result refs
judgment refs
parent request
created_at
```

Then recompute:

```text
TransitionRequestRow.request_fingerprint
```

using the same canonical P1-4 fingerprint semantics used at persistence time.

Because the original request fingerprint includes guard facts, reconstruct those facts from the persisted Evaluation guard entries plus exact request Task/run/state binding.

If exact recomputation is impossible from the durable schema:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not silently skip the fingerprint.

Required corruption proof:

```text
otherwise-valid opening request
+ request_fingerprint changed to another 64-char value
→ historical P1-4 transition verification fails closed
→ HumanResult historical replay fails closed
```

---

# 6. exact Evaluation / guard-matrix provenance

For the request:

```text
exactly one TransitionEvaluationRow
exactly one TransitionDecisionRow
```

Verify Evaluation:

```text
evaluation.transition_request_id == request

authoritative_state == request.observed_state
authoritative_state_version == request.observed_state_version

evaluated_at structurally coherent with decision
```

Then read the accepted P1-4 TransitionMatrix for:

```text
request.observed_state → request.target_state
```

Verify durable guard evaluation structurally matches the matrix.

For each required guard:

```text
exact GuardId present

semantic_owner == exact accepted owner

satisfied == true for ADMITTED

authority_ref structurally present when required by that guard contract

bound_refs structurally preserved
```

And:

```text
missing_guards
== exact unsatisfied required-guard set

for ADMITTED:
missing_guards == empty
every required guard satisfied
```

Do not infer extra P1-7 semantics here.

P1-4 verifies its own matrix/owner structure.

For:

```text
ADMISSION_PENDING → HUMAN_REQUIRED
```

the durable Evaluation must prove the exact accepted:

```text
G_HUMAN_REQUIRED
owner = P1_7_HUMAN
satisfied = true
```

as required by the actual P1-4 matrix.

Required corruption proofs:

```text
opening Evaluation removes G_HUMAN_REQUIRED
while Decision remains ADMITTED
→ fail closed

G_HUMAN_REQUIRED owner changed
→ fail closed

required guard marked unsatisfied
but Decision says ADMITTED
→ fail closed

missing_guards inconsistent with persisted guard evaluations
→ fail closed
```

---

# 7. exact Decision authority

Verify:

```text
decision.transition_request_id == request
decision.transition_evaluation_id == evaluation

outcome / reason are coherent

for HumanGate OPENED:
outcome = ADMITTED
reason = accepted admitted reason

resulting_state = HUMAN_REQUIRED
resulting_state_version = request.observed_state_version + 1

admitting_owner == exact accepted P1-4 owner
kernel_version == exact accepted/currently supported P1-4 kernel authority
```

Do not hardcode guessed strings if exact accepted constants exist.

Consume exact canonical identifiers.

Required corruption proof:

```text
locally coherent ADMITTED decision
but wrong admitting_owner/kernel authority
→ fail closed
```

---

# 8. canonical WorkRun admitted lineage membership

This is the core missing property.

Load durable:

```text
WorkRunRow
```

for the request's `work_run_id`.

Then prove the entire P1-4 admitted provenance reconstructs to that durable projection using the canonical
P1-4 consistency algorithm.

Prefer calling/extracting:

```text
PostgresWorkRunRepository._verify_consistency_in_session(...)
```

or an exact public/internal owner-equivalent.

The specific HumanGate-opening decision must be one contiguous admitted step of that reconstructed history:

```text
evaluated state/version
→ decision resulting state/version
```

and not an orphan/duplicate/fabricated local triple.

Historical is allowed:

```text
WorkRun may now be at a later state/version
```

The requirement is:

```text
opening transition is a valid member of the complete contiguous admitted history
```

not:

```text
opening transition is the current latest transition
```

Required corruption proof:

```text
insert/construct locally coherent request/evaluation/ADMITTED decision
that is not a member of the canonical WorkRun admitted lineage

→ P1-4 historical verifier fails closed
→ gate historical verifier fails closed
→ HumanResult historical replay fails closed
```

---

# 9. P1-7 HumanGate consumes only the P1-4 verifier

Refactor:

```text
_verify_normal_gate_transition_provenance(...)
```

so it does not maintain an independent weaker version of P1-4 transition truth.

Expected shape:

```text
verified = P1-4 historical transition verifier(...)

then P1-7 checks only gate-specific bindings:

opening event request/decision IDs
gate ID derivation
gate Task/run/source/target binding
gate opened_at vs admitted decision timestamp
gate bound version
gate fingerprint
```

Required:

```text
P1-4 verifier
→ proves transition authority

P1-7 gate verifier
→ proves this gate is bound to that verified transition
```

Avoid duplicate P1-4 matrix logic in HumanGate code.

---

# 10. fail-closed / no auto-repair

Any missing/corrupt root provenance:

```text
request fingerprint mismatch

Evaluation missing/duplicate

Decision missing/duplicate

guard matrix mismatch

owner mismatch

ADMITTED with missing/unsatisfied guards

decision owner/kernel mismatch

WorkRun projection/history mismatch

opening decision orphaned from canonical history
```

must produce accepted sanitized equivalent of:

```text
PROVENANCE_INCOMPLETE
or
AUTHORITY_CONFLICT
```

No auto repair.

No synthetic P1-7 replacement fact.

---

# 11. positive proof

Preserve successful historical behavior:

```text
valid gate opened by real P1-4 admitted transition
→ HumanResult historical replay succeeds

WorkRun later moves to HUMAN_REQUIRED/terminal/rework states
→ historical opening remains verifiable as a member of the complete P1-4 history

valid corrected gate
→ predecessor normal root still verifies through P1-4
→ corrected historical replay succeeds

no replay operation creates new transition/gate/result rows/events
```

Current guard effectiveness remains separate.

---

# 12. regression preservation

Fresh regression must preserve all previous closures:

```text
0051:
cross-scope / current gate / policy / COMMAND_CENTER / expiry

0148:
post-lock time / global IDs / proposal idempotency / historical replay separation

0225:
direct immutable HumanResult/Judgment issuance provenance

1142:
gate/Judgment transitive graph + cycle detection

P1-6:
PRE_HUMAN binding / HUMAN_P1_7 admission boundary

P1-4:
transition behavior unchanged
```

---

# 13. allowed source paths

Expected narrow changes:

```text
src/aiscc/persistence/repository.py
src/aiscc/human/repository.py

tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/workflow/test_postgres_kernel.py
```

If exact P1-4 matrix access requires:

```text
src/aiscc/workflow/**
```

a narrow verifier/helper change is allowed.

Do not modify the state graph or guard ownership.

Migration:

```text
20260829_0004
```

should remain unchanged unless the durable P1-4 schema is proven insufficient.

If durable request fingerprint cannot be recomputed from current schema:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

rather than adding ad hoc P1-7 fields.

Governance/report:

```text
.aiassistant/records/aiscc/cycles/
20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-hold-1.cycle.md

.aiassistant/tasks/active/
20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-runtime-rework-1.md

.aiassistant/tasks/done/
20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-runtime-rework-1.md

.aiassistant/reports/target/
20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-runtime-rework-1/**
```

---

# 14. forbidden

Do not modify:

```text
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

accepted P1-7 terminal Cycle
```

No:

```text
P1-8

WorkflowState additions/removals

transition graph changes

guard owner changes

P1-6 evidence semantics changes

real provider / external IdP / credentialed network

deployment / Public Live

git add / commit / push
```

Runtime remains uncommitted.

---

# 15. evidence contract

## executor_required

```text
STATIC_SOURCE

POSTGRESQL_INTEGRATION

P1_4_REQUEST_FINGERPRINT

P1_4_GUARD_MATRIX_PROVENANCE

P1_4_DECISION_AUTHORITY

P1_4_CANONICAL_HISTORY_MEMBERSHIP

HUMAN_GATE_ROOT_PROVENANCE

CORRUPTION_FAIL_CLOSED

HISTORICAL_REPLAY

0051_REGRESSION
0148_REGRESSION
0225_REGRESSION
1142_REGRESSION

P1_4_REGRESSION
P1_6_REGRESSION

SECURITY_EXPORT
```

## reuse_allowed

Predecessor evidence may be reused only for unchanged behavior after fresh regression.

## human_owned

```text
P1-7 runtime final acceptance
→ HUMAN_PENDING
```

## forbidden

```text
P1-8
direct WorkflowState mutation
runtime Git commit
real external action
```

---

# 16. mandatory stop

STOP on:

```text
HEAD drift

accepted design SHA drift

predecessor 19-path aggregate drift

need to change accepted P1-7 design

need to change P1-4 transition semantics

P1-4 durable schema cannot reconstruct exact request fingerprint / guard-matrix provenance

canonical WorkRun history cannot distinguish an orphan admitted triple

unrelated dirty collision
```

If the P1-4 baseline itself lacks enough durable data:

```text
STOP
→ POLICY_BASELINE_GAP
```

Report the exact missing fields/contracts.

Do not mask it in P1-7.

---

# 17. accept criteria

All must hold:

```text
normal HumanGate opening consumes canonical P1-4 historical transition verifier

request_fingerprint is recomputed and checked

Evaluation guard set matches exact P1-4 TransitionMatrix

ADMITTED requires every exact required guard satisfied

ADMISSION_PENDING → HUMAN_REQUIRED includes exact G_HUMAN_REQUIRED owner binding

Decision exact P1-4 admitting owner/kernel authority verified

opening decision is a member of canonical contiguous WorkRun admitted history

complete P1-4 history reconstructs to durable WorkRun projection

corrupt request fingerprint fails closed

corrupt/missing required Human guard fails closed

wrong decision owner/kernel fails closed

locally coherent but orphan P1-4 triple fails closed

valid historical gate/result replay remains successful

1142 transitive graph tests remain PASS

0051/0148/0225 regressions PASS

P1-4/P1-6 regressions PASS

P1-8 remains NOT_STARTED

provider/network/credential/deployment = 0

Stage 1 Git commit = none
```

---

# 18. report requirements

Report exact:

1. task path
2. start/final HEAD
3. accepted design SHA
4. predecessor 19-path aggregate verification
5. 1241 HOLD Cycle placement
6. exact canonical P1-4 verifier location/API
7. request fingerprint reconstruction
8. guard matrix reconstruction
9. exact ADMISSION_PENDING → HUMAN_REQUIRED required guards/owners observed
10. decision owner/kernel verification
11. full WorkRun history reconstruction
12. proof opening decision is a history member
13. corrupted request fingerprint proof
14. corrupted G_HUMAN_REQUIRED proof
15. wrong owner/kernel proof
16. orphan locally coherent triple proof
17. valid historical gate replay proof
18. corrected-gate root replay proof
19. 0051 regression
20. 0148 regression
21. 0225 regression
22. 1142 regression
23. P1-4 regression
24. P1-6 regression
25. PostgreSQL/version/test counts
26. final runtime path count / aggregate SHA
27. provider/network/credential actions
28. P1-8 = NOT_STARTED
29. Git actions = none
30. human verification = HUMAN_PENDING
31. preserved exact paths
32. next recommendation

---

# 19. export

Target:

```text
.aiassistant/reports/target/
20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-runtime-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include all changed runtime/test paths and the 1241 HOLD Cycle.

Manifest requirements:

```text
actual copied-byte SHA
64 lowercase hex
source/copy identity PASS
runtime aggregate from actual exported runtime bytes
```

---

# 20. lifecycle / Git

Start:

```text
.aiassistant/tasks/active/
20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-runtime-rework-1.md
```

Finish:

```text
.aiassistant/tasks/done/
20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-runtime-rework-1.md
```

No Git add/commit/push.

Expected final HEAD:

```text
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

---

# 21. preserved exact paths

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

.aiassistant/records/aiscc/cycles/
20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-runtime-rework-1.md

.aiassistant/tasks/done/
20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-runtime-rework-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

---

# 22. final state

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
