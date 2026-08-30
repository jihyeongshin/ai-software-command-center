# 작업지시서: P1-7 Historical Replay Provenance Integrity Runtime Rework

## meta

- task_id: `20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-runtime-rework-1`
- created_at: `2026-08-30T02:25:00+09:00`
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
- predecessor_runtime_aggregate_sha256: `678c0981defc31c6c1351da509838a42e19e22ba2abe287bb30b7d2a7e9713fd`
- p1_7_runtime_status: `REWORK_REQUIRED / HUMAN_PENDING`
- p1_8_status: `NOT_STARTED`
- public_bounded_live_release: `NOT_RELEASED`

---

# 1. current state

The 0148 rework successfully closed:

```text
expiry lock-time authority
global HumanResult ID serialization
global Judgment ID serialization
HumanResult proposal idempotency
Judgment historical identity/current-effectiveness separation
```

Do not reopen those semantics.

Preserve:

```text
238b0b41460c2504fd3244eadb06809d8692a60f
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

Current runtime remains an uncommitted review candidate.

Place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-hold-1.cycle.md
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
678c0981defc31c6c1351da509838a42e19e22ba2abe287bb30b7d2a7e9713fd
```

Mismatch:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

Task/HOLD/report files are outside the 19 runtime identity.

---

# 3. load-bearing rule

Keep the 0148 separation:

```text
historical immutable replay
!= current authority effectiveness
```

Add the missing distinction:

```text
historical immutable row self-hash
!= complete historical authority provenance
```

Required V1 rule:

```text
same immutable ID + same proposal fingerprint
→ first verify complete immutable issuance provenance
→ then return the same historical object

same immutable ID + different proposal fingerprint
→ typed identity conflict

corrupt/incomplete immutable provenance
→ fail closed
→ no historical object returned as valid authority provenance
```

Do NOT require the historical object to still be current for a guard/transition.

---

# 4. FINDING-1 — projection-independent HumanResult immutable provenance verifier

Create one exact owner function/service equivalent to:

```text
_verify_human_result_historical_provenance_in_session(...)
```

It must validate the immutable historical HumanResult without requiring the gate projection to still point
to that result as current.

At minimum:

```text
HumanResultRow exists

serialized_ref / human_result_id / human_gate_id coherent

proposal_fingerprint:
- exists
- exactly 64 lowercase hex
- remains the durable proposal identity used for replay comparison

reconstructed HumanResult fingerprint
== stored human_result_fingerprint

HumanGateRow for HumanResultRow.human_gate_id exists

HumanResult.human_gate_ref
== HumanGateRow.serialized_ref

HumanResult TaskContract/work_run
== HumanGateRow immutable TaskContract/work_run

exactly one HumanResultAuthorityEventRow exists for this HumanResult

event_kind:
ADMITTED

prior_revision:
0

new_revision:
HumanResult.result_authority_revision
and accepted V1 revision value

event payload gate_ref
== HumanResult.human_gate_ref

event timestamp / admitted_at relationship is structurally valid according to accepted provenance
```

Do not require:

```text
gate projection status = RESOLVED
projection.current_result_ref = this result
current WorkRun state/version
gate not expired
```

because those are **current effectiveness**, not historical identity.

If the gate/result was corrected, superseded, expired, or its WorkRun moved on:

```text
same exact immutable proposal
→ may still return historical HumanResult
```

provided immutable issuance provenance remains complete.

---

# 5. HumanResult replay ordering

Under the already accepted lock order:

```text
WorkRun lock
→ HumanResult-ID lock
```

Existing row branch should be equivalent to:

```text
existing row found

→ verify historical immutable HumanResult provenance

→ compare existing proposal_fingerprint to proposed fingerprint

same
→ return exact historical HumanResult
→ no new event
→ no gate projection mutation
→ no clock/current authority check

different
→ HUMAN_RESULT_IDENTITY_CONFLICT
→ no mutation
```

If you choose to compare proposal fingerprint before full provenance verification for DoS/performance reasons,
the result must still fail closed on corrupted provenance and must not return the historical object.

Preferred reviewable semantics:

```text
historical integrity first
→ identity comparison second
```

because a corrupt durable row should not be treated as the authoritative basis for an identity-conflict
decision unless exact accepted error taxonomy requires otherwise.

Do not change global-ID locking or omitted-timestamp proposal semantics.

---

# 6. FINDING-2 — projection-independent Judgment immutable provenance verifier

Create one exact owner function/service equivalent to:

```text
_verify_judgment_historical_provenance_in_session(...)
```

It must validate historical Judgment issuance without requiring:

```text
JudgmentProjectionRow.work_run_id
→ currently points to this Judgment
```

At minimum validate:

```text
JudgmentRow exists

reconstructed Judgment fingerprint
== stored row fingerprint

proposal_fingerprint:
- exists
- exactly 64 lowercase hex

JudgmentEvaluationRow for Judgment.evaluation_ref exists

evaluation.work_run_id
== Judgment.work_run_id

evaluation.state_version
== Judgment.state_version

evaluation payload references the same policy/human/evidence/CommandCenter inputs
at the structural level persisted by the runtime

evaluation outcome
== accepted complete/issued state

exactly one ISSUED JudgmentAuthorityEventRow for this Judgment

ISSUED prior_revision
== Judgment.authority_revision - 1

ISSUED new_revision
== Judgment.authority_revision

ISSUED evaluation_ref
== Judgment.evaluation_ref

immutable referenced JudgmentPolicyRow exists
and matches the Judgment's:
policy id/version/fingerprint/authority id/version/revision
TaskContract/source/target/use/owner

HUMAN owner:
referenced HumanResult exists
and its own immutable historical provenance verifies
and immutable TaskContract/work_run/state/kind bindings match the Judgment

COMMAND_CENTER owner:
referenced CommandCenterJudgmentActionRow exists
and immutable fingerprint/bindings match the Judgment

SYSTEM_DETERMINISTIC owner:
policy deterministic kind matches Judgment kind
```

## 6.1 correction/supersession structural provenance

If:

```text
Judgment.supersedes_judgment_ref is not None
```

verify the predecessor exists and the predecessor has the accepted exact `SUPERSEDED` relation pointing to
this Judgment with coherent revision linkage.

If the historical Judgment itself has later been superseded:

```text
that does NOT make historical replay invalid
```

but any durable `SUPERSEDED` event on it must be structurally coherent and point to an existing replacement.

Do not require the current projection to point at the historical object.

---

# 7. Judgment replay ordering

Keep the accepted global lock order:

```text
WorkRun lock
→ Judgment-ID lock
```

Existing row branch:

```text
existing Judgment found

→ verify historical immutable Judgment provenance

→ compare durable proposal_fingerprint

same
→ return historical immutable Judgment

different
→ JUDGMENT_IDENTITY_CONFLICT
```

No current checks here:

```text
current WorkRun state/version
current policy revision
current HumanResult/gate projection
current Command Center action expiry
current P1-6 evidence effectiveness
current JudgmentProjection
```

Those remain solely in current-use paths such as:

```text
JudgmentTransitionParticipant.prepare()
```

Required:

```text
immutable provenance validation
!= current guard validation
```

---

# 8. fail-closed corruption proofs

Add fresh PostgreSQL proofs for incomplete/corrupt immutable provenance.

Do not weaken/disable append-only protections in production code.

The test fixture may create deliberately incomplete rows directly through the persistence layer or another
narrow test-only method.

At minimum:

## HUMAN_RESULT_HISTORICAL_PROVENANCE

```text
self-hash-valid HumanResultRow
+ same proposal fingerprint
+ missing ADMITTED event
→ replay fails closed

HumanResultRow
+ ADMITTED event with wrong revision/gate relation
→ replay fails closed

HumanResultRow points to missing/wrong HumanGate
→ replay fails closed
```

## JUDGMENT_HISTORICAL_PROVENANCE

```text
self-hash-valid JudgmentRow
+ same proposal fingerprint
+ missing JudgmentEvaluation
→ replay fails closed

JudgmentRow
+ missing/wrong ISSUED event
→ replay fails closed

ISSUED event points to wrong evaluation
→ replay fails closed

Judgment policy immutable snapshot missing/mismatched
→ replay fails closed

HUMAN-owned Judgment with missing/corrupt historical HumanResult provenance
→ replay fails closed

COMMAND_CENTER-owned Judgment with missing/corrupt immutable action relation
→ replay fails closed
```

Use accepted sanitized errors:

```text
PROVENANCE_INCOMPLETE
or
AUTHORITY_CONFLICT
```

according to whether data is missing vs contradictory.

Do not auto-repair.

---

# 9. positive historical replay proofs

Preserve and extend:

```text
HumanResult same proposal
after gate resolved
→ same historical object

HumanResult same proposal
after gate later expired/cancelled/superseded
→ same historical object
if immutable result provenance is complete

Judgment same proposal
after policy superseded
→ same historical object

Judgment same proposal
after WorkRun state/version changed
→ same historical object

Judgment same proposal
after Judgment itself was superseded
→ same historical object
if immutable correction lineage is complete

all above:
→ no new event/evaluation/projection mutation
```

And separately prove:

```text
those stale historical objects
→ cannot satisfy current G_HUMAN_* / G_JUDGMENT_*
```

---

# 10. preserve 0051 + 0148 closures

Fresh regression must keep:

```text
cross-scope gate/result/Judgment rejection

durable current-gate action authority

Task/use-bound Judgment policy

COMMAND_CENTER distinct authority

gate expiry lifecycle

post-lock time authority

global HumanResult/Judgment ID locks

HumanResult omitted submitted_at idempotency

typed global ID conflicts

Judgment historical identity/current-effectiveness separation

P1-6 PRE_HUMAN binding

P1-4 exclusive transition ownership
```

Do not change accepted design.

---

# 11. allowed paths

Primary expected:

```text
src/aiscc/human/repository.py
src/aiscc/judgment/authority.py

tests/integration/human/test_postgres_human_gate_judgment.py
tests/unit/human/test_human_judgment_domain.py
```

Narrow additional source only if the verifier needs a shared helper:

```text
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/persistence/**
```

Migration:

```text
20260829_0004
```

should remain unchanged unless a true durable provenance field is missing. Existing event/evaluation data should
normally be sufficient.

Governance/report:

```text
.aiassistant/records/aiscc/cycles/
20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-hold-1.cycle.md

.aiassistant/tasks/active/
20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-runtime-rework-1.md

.aiassistant/tasks/done/
20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-runtime-rework-1.md

.aiassistant/reports/target/
20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-runtime-rework-1/**
```

---

# 12. forbidden

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

# 13. evidence contract

## executor_required

```text
STATIC_SOURCE

POSTGRESQL_INTEGRATION

HUMAN_RESULT_HISTORICAL_PROVENANCE

JUDGMENT_HISTORICAL_PROVENANCE

CORRUPTION_FAIL_CLOSED

HISTORICAL_REPLAY

CURRENT_GUARD_ANTI_REPLAY

RESTART

SECURITY_EXPORT

0051_REGRESSION

0148_REGRESSION

P1_4_REGRESSION

P1_6_REGRESSION
```

## reuse_allowed

Reuse 0148 evidence only for unchanged global-ID/time/idempotency behavior after fresh regression.

## human_owned

```text
P1-7 runtime final acceptance
→ HUMAN_PENDING
```

## forbidden

```text
P1-8
direct WorkflowState mutation
real provider/network/credential action
runtime Git commit
```

---

# 14. mandatory stop

STOP on:

```text
HEAD drift

accepted design SHA drift

predecessor 19-path aggregate drift

need to change accepted P1-7 design

historical provenance cannot be verified from current durable schema

fix requires current-projection authority to validate historical identity

need to weaken append-only DB protections

unrelated dirty collision
```

If the durable schema lacks enough information to verify historical issuance provenance:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not silently treat the row self-hash as sufficient.

---

# 15. accept criteria

All must hold:

```text
HumanResult existing same-proposal replay verifies immutable ADMITTED/gate lineage

Judgment existing same-proposal replay verifies immutable evaluation/ISSUED/policy lineage

historical replay does not require current gate/Judgment projection

missing/corrupt historical event/evaluation/reference
→ fail closed

same valid historical proposal
→ exact historical object returned

different proposal
→ typed identity conflict

no new event/evaluation/projection mutation on replay

historical stale object
→ still denied as current guard authority

0148 global identity/time/idempotency proofs remain PASS

0051 cross-scope/policy/expiry proofs remain PASS

P1-4/P1-6 directly affected regression PASS

P1-8 remains NOT_STARTED

provider/network/credential/deployment = 0

Stage 1 Git commit = none
```

---

# 16. report requirements

Report exact:

1. task path
2. start/final HEAD
3. accepted design SHA
4. predecessor 19-path aggregate verification
5. 0225 HOLD Cycle placement
6. HumanResult historical verifier fields/checks
7. Judgment historical verifier fields/checks
8. replay ordering before/after
9. current-effectiveness separation
10. missing HumanResult ADMITTED-event proof
11. bad HumanResult gate-link proof
12. missing Judgment evaluation proof
13. bad/missing Judgment ISSUED-event proof
14. policy historical snapshot proof
15. HUMAN-owned Judgment historical dependency proof
16. COMMAND_CENTER-owned historical dependency proof
17. superseded Judgment positive historical replay
18. stale current guard rejection
19. restart proof
20. 0051 regression
21. 0148 regression
22. P1-4 regression
23. P1-6 regression
24. runtime path count / aggregate SHA
25. provider/network/credential actions
26. P1-8 = NOT_STARTED
27. Git actions = none
28. human verification = HUMAN_PENDING
29. preserved exact paths
30. next recommendation

---

# 17. export

Target:

```text
.aiassistant/reports/target/
20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-runtime-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include all changed runtime/test paths and the 0225 HOLD Cycle.

Manifest:

```text
actual copied-byte SHA
64 lowercase hex
source/copy identity PASS
runtime aggregate from actual exported runtime bytes
```

---

# 18. lifecycle / Git

Start:

```text
.aiassistant/tasks/active/
20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-runtime-rework-1.md
```

Finish:

```text
.aiassistant/tasks/done/
20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-runtime-rework-1.md
```

No Git add/commit/push.

Expected final HEAD:

```text
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

---

# 19. preserved exact paths

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

.aiassistant/tasks/done/
20260830_0148_aiscc-p1-7-global-identity-idempotency-and-expiry-toctou-runtime-rework-1.md

.aiassistant/tasks/done/
20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-runtime-rework-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

---

# 20. final state

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
