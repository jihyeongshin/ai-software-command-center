# 작업지시서: P1-7 Owner-Backed Guard + Full WorkRun History Provenance Runtime Rework

## meta

- task_id: `20260830_1346_aiscc-p1-7-owner-backed-guard-and-full-workrun-history-provenance-runtime-rework-1`
- created_at: `2026-08-30T13:46:00+09:00`
- phase: `P1-7 Human Gate and Judgment`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT / P1-4_TRANSITION_PROVENANCE`
- expected_start_head: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted_design_commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- accepted_design_terminal_commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted_design_sha256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- predecessor_runtime_path_count: `20`
- predecessor_runtime_aggregate_sha256: `5007f8d9c417be39efdfcea522e910846b8e830d53d88cda2340ddb87d19ed9c`
- p1_7_runtime_status: `REWORK_REQUIRED / HUMAN_PENDING`
- p1_8_status: `NOT_STARTED`
- public_bounded_live_release: `NOT_RELEASED`

---

# 1. current state

1241 closed its direct root-provenance finding.

Do not reopen:

```text
selected opening request fingerprint reconstruction

selected exact P1-4 matrix guard set/owners/bound refs

selected ADMITTED decision owner/kernel/result state/version

selected transition contiguous-history membership

normal HumanGate consuming canonical P1-4 verifier

1142 transitive gate/Judgment graph

0225 direct historical issuance provenance

0148 global identity/time/idempotency

0051 cross-scope/policy/COMMAND_CENTER/expiry
```

Remaining gaps are:

```text
A. historical G_HUMAN_REQUIRED is not resolved to its durable P1-7 attestation

B. that Human guard's PRE_HUMAN P1-6 immutable binding is not historically verified

C. whole WorkRun admitted history validates state/version continuity but not every step's full immutable/run identity
```

Place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260830_1346_aiscc-p1-7-owner-backed-guard-and-full-workrun-history-provenance-hold-1.cycle.md
```

---

# 2. predecessor verification

Before mutation verify:

```text
HEAD ==
c87cfc75f14476e10b4a02a2ab0bd295720a85a0

accepted design SHA ==
22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549

current runtime candidate ==
20 paths /
5007f8d9c417be39efdfcea522e910846b8e830d53d88cda2340ddb87d19ed9c
```

Mismatch:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

---

# 3. frozen ownership boundary

Preserve:

```text
P1-4:
TransitionDecision / WorkflowState owner

P1-6:
Evidence admission / EvidenceSetSatisfactionAttestation / G_EVIDENCE owner

P1-7:
HumanGate / HumanResult / Judgment / G_HUMAN_* / G_JUDGMENT_* owner
```

Historical verification may cross owner boundaries only by consuming the owner's durable immutable provenance.

Forbidden:

```text
P1-4 invents P1-7 Human truth

P1-7 invents P1-6 evidence truth

process-local issuer token
→ durable historical proof
```

---

# 4. historical G_HUMAN_REQUIRED owner-backed verifier

For the selected normal HumanGate opening, after P1-4 canonical structural transition verification returns the exact Evaluation:

Locate:

```text
GuardId.G_HUMAN_REQUIRED
```

and verify its persisted `authority_ref`.

Required:

```text
authority_ref
→ exactly one HumanGuardAttestationRow.serialized_ref
```

No match:

```text
PROVENANCE_INCOMPLETE
```

Ambiguous/mismatched:

```text
AUTHORITY_CONFLICT
```

## 4.1 reconstruct immutable HumanGuardAttestation

Create/reuse an exact projection-independent helper equivalent to:

```text
_verify_human_guard_attestation_historical_provenance_in_session(...)
```

It must reconstruct the `HumanGuardAttestation` from the durable row/payload and verify:

```text
attestation_id / version / serialized_ref coherence

fingerprint exactly recomputed

row.guard_id == payload.guard_id == G_HUMAN_REQUIRED

row.work_run_id == payload.work_run_id == request.work_run_id

row.state_version == payload.state_version == request.observed_state_version

payload TaskContract id/version == request

payload source state/version == request

payload target state == HUMAN_REQUIRED

payload target_use_fingerprint == exact request target-use fingerprint

payload human_gate_ref == exact historical gate serialized ref

payload gate authority revision == accepted opening revision

payload purpose id/version == accepted HumanGate purpose

payload human_result_ref == None

payload P1-7 authority id/version/revision == exact accepted runtime authority constants

issued_at / expires_at row ↔ payload coherent
```

The Evaluation observation must exactly match:

```text
guard_id
semantic_owner = P1_7_HUMAN
satisfied = true
authority_ref = attestation.serialized_ref
bound_refs = exact required_bound_refs(G_HUMAN_REQUIRED, request)
```

Do not use `_HISTORICAL_RECONSTRUCTION_TOKEN` as proof of P1-7 authority.

---

# 5. immutable PRE_HUMAN P1-6 binding

The historical Human guard attestation for `G_HUMAN_REQUIRED` must contain its accepted typed PRE_HUMAN evidence binding.

Verify exact immutable values:

```text
pre_human_evidence attestation ref/version

checkpoint ref/version/fingerprint

TaskContract id/version
work_run_id
source state/version
target state
transition-purpose id/version

RequirementSet id/version
full requirement root
ordered applicable requirement refs if persisted
applicable subset root

ordered admitted evidence refs if persisted
admitted-ref root

satisfied = true

P1-6 evidence authority id/version/revision

issued_at / expires_at
```

## 5.1 referenced P1-6 attestation row

Resolve the exact durable:

```text
EvidenceSetAttestationRow
```

by serialized ref.

Verify immutable row/payload equivalence with the Human guard's PRE_HUMAN binding.

At minimum:

```text
same attestation id/version/ref

same evaluation id/version

same TaskContract/work_run/state/version

same checkpoint ref/fingerprint

same target / transition-purpose

same RequirementSet identity/full root/applicable subset root

same admitted-ref root

same satisfied=true

same P1-6 authority version/revision

same issuer identity/version

row state_version / authority revision / issued_at / expires_at coherent
```

If the P1-6 attestation row references an Evaluation row, verify the immutable Evaluation identity/root/outcome fields required to prove that the attestation was genuinely issued as `SATISFIED`.

Do not require:

```text
current WorkRun state/version
current evidence authority revision
current RequirementSet projection
current unexpired status at replay time
```

Those are current effectiveness, not historical issuance.

Required:

```text
valid historical PRE_HUMAN attestation
may be no longer current
→ historical gate/result replay still valid
```

If current P1-6 durable schema cannot verify immutable issuance without current projection:

```text
STOP
→ POLICY_BASELINE_GAP
```

Do not re-evaluate requirements inside P1-7.

---

# 6. complete WorkRun history must validate every admitted step

Refactor P1-4 verification to avoid:

```text
selected step = strong
surrounding admitted steps = state/version only
```

Create one non-recursive per-step verifier equivalent to:

```text
_verify_historical_transition_step_in_session(...)
```

It should verify for every admitted transition:

```text
request immutable row → TransitionRequest reconstruction

request fingerprint exact

exact matrix transition exists

Evaluation exact shape / guard set / owner / bound refs

all required guards satisfied for ADMITTED

missing_guards empty

Decision exact relation
outcome = ADMITTED
reason = ADMITTED
admitting_owner / kernel_version exact
resulting state/version exact
```

## 6.1 WorkRun identity for every admitted step

For every admitted request:

```text
request.work_run_id == WorkRunRow.work_run_id

request.project_id == WorkRunRow.project_id

request.task_contract_id == WorkRunRow.task_contract_id

request.task_contract_version == WorkRunRow.task_contract_version

request.runtime_mode == WorkRunRow.runtime_mode
```

Any mismatch:

```text
AUTHORITY_CONFLICT
```

## 6.2 whole-history reconstruction

Then reconstruct:

```text
NONE/v0
→ each admitted evaluated state/version
→ each resulting state/version
→ final durable WorkRun projection
```

Event order remains authoritative through the existing durable sequence.

The selected opening decision must be one verified step in that exact sequence.

Avoid calling the whole-history verifier recursively from the per-step verifier.

---

# 7. historical future-owner guard scope

For this Task, full owner-backed resolution is mandatory for:

```text
selected HumanGate-opening G_HUMAN_REQUIRED
```

because P1-7 owns and can verify it.

For other historical future-owner guards in surrounding steps:

- P1-4 must still verify exact owner / shape / bound refs / request fingerprint.
- Do not invent P1-6/P1-7/Judgment semantics inside P1-4.
- If complete whole-history authenticity requires owner-backed validation for another future-owner guard and no owner verifier exists, report the exact case.

Do not broaden this Task into P1-8.

If a generic dependency-inversion interface is needed, it may be a narrow historical guard provenance resolver keyed by semantic owner, but do not redesign runtime transition evaluation.

---

# 8. mandatory corruption proofs

Fresh PostgreSQL negative proofs:

## OWNER_BACKED_G_HUMAN_REQUIRED

```text
Evaluation G_HUMAN_REQUIRED authority_ref changed to arbitrary non-empty string
and request fingerprint coherently recomputed
→ fail closed

authority_ref points to missing HumanGuardAttestationRow
→ fail closed

attestation row fingerprint corrupted
→ fail closed

attestation TaskContract/work_run/state/target/gate binding corrupted
→ fail closed

attestation authority id/version/revision corrupted
→ fail closed
```

## PRE_HUMAN_IMMUTABLE_BINDING

```text
Human guard PRE_HUMAN attestation ref points to missing P1-6 row
→ fail closed

P1-6 row checkpoint/root/revision differs from Human guard binding
→ fail closed

P1-6 attestation immutable Evaluation outcome/root mismatched
→ fail closed

valid historical P1-6 attestation becomes non-current after WorkRun advances
→ historical HumanResult replay still succeeds
```

## FULL_WORKRUN_STEP_INTEGRITY

Create/corrupt a different admitted transition in the same WorkRun while keeping state/version contiguous:

```text
foreign TaskContract version
→ fail closed

foreign project_id
→ fail closed

foreign runtime_mode
→ fail closed

request_fingerprint changed
→ fail closed

required guard owner/shape corrupted
→ fail closed

decision owner/kernel corrupted
→ fail closed
```

The selected HumanGate opening rows themselves should remain unchanged in at least one of these proofs, proving that full-history validation catches corruption elsewhere.

---

# 9. preserve all earlier closures

Fresh regression must preserve:

```text
0051:
cross-scope / current gate / Judgment policy / COMMAND_CENTER / expiry

0148:
post-lock time / global IDs / HumanResult proposal idempotency / Judgment historical replay

0225:
direct HumanResult/Judgment immutable issuance provenance

1142:
gate/Judgment transitive correction graph + cycles

1241:
selected P1-4 opening request fingerprint / matrix / decision / history membership

P1-6:
PRE_HUMAN / HUMAN_P1_7 admission behavior

P1-4:
9 states / accepted transition matrix / transition ownership unchanged
```

---

# 10. expected source scope

Likely narrow changes:

```text
src/aiscc/persistence/repository.py
src/aiscc/human/authority.py
src/aiscc/human/repository.py
src/aiscc/evidence/repository.py

tests/integration/workflow/test_postgres_kernel.py
tests/integration/human/test_postgres_human_gate_judgment.py
```

Only add a P1-6 projection-independent immutable verifier if current repository helpers cannot safely expose one.

No accepted evidence semantics change.

Migration should remain unchanged unless immutable P1-6 attestation provenance is not reconstructable from existing durable rows.

If schema is insufficient:

```text
STOP
→ POLICY_BASELINE_GAP
```

Do not add ad hoc P1-7 shadow provenance.

---

# 11. forbidden

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

WorkflowState changes

transition matrix / guard owner changes

P1-6 admission truth changes

real provider / external IdP / credentialed network

deployment / Public Live

git add / commit / push
```

Runtime remains uncommitted.

---

# 12. evidence contract

## executor_required

```text
STATIC_SOURCE

POSTGRESQL_INTEGRATION

OWNER_BACKED_G_HUMAN_REQUIRED

HUMAN_GUARD_HISTORICAL_ATTESTATION

PRE_HUMAN_IMMUTABLE_P1_6_BINDING

FULL_WORKRUN_STEP_INTEGRITY

P1_4_REQUEST_FINGERPRINT

P1_4_GUARD_MATRIX_PROVENANCE

P1_4_CANONICAL_HISTORY

CORRUPTION_FAIL_CLOSED

HISTORICAL_REPLAY

0051_REGRESSION
0148_REGRESSION
0225_REGRESSION
1142_REGRESSION
1241_REGRESSION

P1_4_REGRESSION
P1_6_REGRESSION

SECURITY_EXPORT
```

## human_owned

```text
P1-7 runtime final acceptance
→ HUMAN_PENDING
```

---

# 13. mandatory stop

STOP on:

```text
HEAD drift

accepted design SHA drift

predecessor 20-path aggregate drift

need to modify accepted P1-7 design

P1-6 durable schema cannot prove immutable historical PRE_HUMAN attestation issuance

full-history validation requires changing P1-4 transition semantics

unrelated dirty collision
```

---

# 14. accept criteria

All must hold:

```text
historical G_HUMAN_REQUIRED resolves exact HumanGuardAttestationRow

Human guard attestation fingerprint and immutable request/gate bindings verified

historical Human guard PRE_HUMAN binding resolves exact immutable P1-6 attestation provenance

historical replay does not require current P1-6 effectiveness

every admitted WorkRun step validates project/TaskContract/runtime identity

every admitted step validates request fingerprint / matrix guards / decision owner/kernel

whole admitted history reconstructs durable WorkRun projection

corruption in a different admitted step invalidates historical gate/result replay

owner-string-only forged G_HUMAN_REQUIRED fails closed

all 0051/0148/0225/1142/1241 regressions PASS

P1-4/P1-6 regressions PASS

P1-8 remains NOT_STARTED

provider/network/credential/deployment = 0

Stage 1 Git commit = none
```

---

# 15. report requirements

Report exact:

1. task path
2. start/final HEAD
3. accepted design SHA
4. predecessor `20 paths / 5007...` verification
5. 1346 HOLD Cycle placement
6. HumanGuardAttestation historical verifier API
7. exact G_HUMAN_REQUIRED durable row checks
8. PRE_HUMAN P1-6 immutable attestation verifier/API
9. current-vs-historical P1-6 separation
10. P1-4 per-step historical verifier
11. full WorkRun identity validation
12. arbitrary authority_ref + recomputed fingerprint corruption proof
13. missing/corrupt Human guard attestation proof
14. missing/corrupt PRE_HUMAN P1-6 provenance proof
15. non-current-but-valid PRE_HUMAN historical replay proof
16. foreign TaskContract/project/runtime step proof
17. corrupt other-step fingerprint/guard/decision proof
18. 0051 regression
19. 0148 regression
20. 0225 regression
21. 1142 regression
22. 1241 regression
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

# 16. export

Target:

```text
.aiassistant/reports/target/
20260830_1346_aiscc-p1-7-owner-backed-guard-and-full-workrun-history-provenance-runtime-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include all changed runtime/test paths plus the 1346 HOLD Cycle.

Manifest:

```text
actual copied-byte SHA
64 lowercase hex
source/copy identity PASS
runtime aggregate from actual exported runtime bytes
```

---

# 17. lifecycle / Git

Start:

```text
.aiassistant/tasks/active/
20260830_1346_aiscc-p1-7-owner-backed-guard-and-full-workrun-history-provenance-runtime-rework-1.md
```

Finish:

```text
.aiassistant/tasks/done/
20260830_1346_aiscc-p1-7-owner-backed-guard-and-full-workrun-history-provenance-runtime-rework-1.md
```

No Git add/commit/push.

Expected final HEAD:

```text
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

---

# 18. preserved exact paths

Must preserve all existing P1-7 accepted/HOLD lineage and additionally:

```text
.aiassistant/records/aiscc/cycles/
20260830_1346_aiscc-p1-7-owner-backed-guard-and-full-workrun-history-provenance-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_1346_aiscc-p1-7-owner-backed-guard-and-full-workrun-history-provenance-runtime-rework-1.md
```

Canonical state files remain preserved and unchanged.

---

# 19. final state

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
