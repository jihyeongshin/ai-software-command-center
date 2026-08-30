# 작업지시서: P1-7 / P1-6 Historical Attestation Canonical Root Runtime Rework

## meta

- task_id: `20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-runtime-rework-1`
- created_at: `2026-08-30T14:47:00+09:00`
- phase: `P1-7 Human Gate and Judgment`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT / P1-6_EVIDENCE_PROVENANCE`
- expected_start_head: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted_design_commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- accepted_design_terminal_commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted_design_sha256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- predecessor_runtime_path_count: `20`
- predecessor_runtime_aggregate_sha256: `4bbc005bda8814653269c25502d246884578f86a13050f9ae72fa4e7f4dc5508`
- p1_7_runtime_status: `REWORK_REQUIRED / HUMAN_PENDING`
- p1_8_status: `NOT_STARTED`

---

# 1. current state

1346 closed:

```text
G_HUMAN_REQUIRED → exact HumanGuardAttestationRow
Human guard → historical P1-6 attestation/evaluation pair
full admitted WorkRun per-step integrity
```

Do not reopen those owner boundaries.

The remaining issue is narrower:

```text
verify_historical_set_attestation_provenance(...)
```

must prove the P1-6 attestation's canonical immutable checkpoint/set/subset/result/admitted-ref graph rather
than only attestation-row ↔ evaluation-row equality.

Place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-hold-1.cycle.md
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
4bbc005bda8814653269c25502d246884578f86a13050f9ae72fa4e7f4dc5508
```

Mismatch:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

---

# 3. frozen authority boundary

Preserve:

```text
P1-6 owns all evidence truth

P1-7 consumes only P1-6 immutable/current authority

historical P1-6 issuance
!= current P1-6 effectiveness
```

This Task must not:

```text
change requirement profiles
change evidence admission semantics
change freshness/reuse policy
change current load_effective_attestation semantics
let P1-7 re-evaluate evidence
```

Only strengthen the projection-independent historical verifier owned by P1-6.

---

# 4. durable checkpoint provenance

Inside:

```text
verify_historical_set_attestation_provenance(...)
```

resolve exact:

```text
EvidenceCheckpointRow
```

for `value.checkpoint_ref`.

Verify immutable row reconstruction using existing P1-6 row helpers / canonical issuer payload rules.

At minimum:

```text
checkpoint_ref exact

checkpoint row fingerprint
== recomputed immutable checkpoint fingerprint

checkpoint row fingerprint
== value.checkpoint_fingerprint

checkpoint TaskContract id/version
== attestation

checkpoint source state
== attestation source state

checkpoint target state
== attestation target state
when target-bound

checkpoint transition-purpose id/version
== attestation
when purpose-bound

checkpoint requirement_set_ref
== attestation RequirementSet id/version

task authority id/version present and immutable
```

Do NOT require:

```text
checkpoint currently unrevoked
checkpoint still current for current WorkRun state
```

A later revocation/supersession does not erase valid historical issuance.

Malformed/missing checkpoint:

```text
PROVENANCE_INCOMPLETE / AUTHORITY_CONFLICT
```

---

# 5. durable RequirementSet / Requirement canonical root

Resolve:

```text
EvidenceRequirementSetRow
```

for attestation RequirementSet.

Reconstruct and verify immutable set row:

```text
set identity/version
TaskContract id/version
semantic owner = P1_6_EVIDENCE
authority version
ordered requirement refs
ordered checkpoint refs
set fingerprint
requirement_root_hash
```

Load every requirement row in the set's durable order.

For each requirement:

```text
row requirement_ref / set_ref exact
reconstructed requirement fingerprint exact
TaskContract/set identity exact
semantic owner/profile/obligation legal
applicable checkpoint refs immutable
```

Recompute:

```text
full_requirement_root_hash =
canonical_hash(
  [(requirement_ref, requirement.fingerprint) for requirement in ordered set]
)
```

Require equality with:

```text
RequirementSetRow.requirement_root_hash
EvidenceSetEvaluation.full_requirement_root_hash
EvidenceSetSatisfactionAttestation.full_requirement_root_hash
```

Do not require current set/requirement effectiveness.

---

# 6. canonical applicable subset

Derive historical applicable requirements exactly as `evaluate_set()` did:

```text
applicable =
ordered immutable requirements
where checkpoint_ref is in requirement.applicable_checkpoint_refs
```

Require:

```text
tuple(applicable refs)
== evaluation.ordered_applicable_requirement_refs
== attestation.ordered_applicable_requirement_refs
```

Recompute:

```text
expected_subset_root =
canonical_hash(
  [(requirement_ref, requirement.fingerprint) for applicable requirement]
)
```

Require exact equality with:

```text
evaluation.checkpoint_subset_root_hash
attestation.checkpoint_subset_root_hash
HumanRequiredEvidenceBinding.applicable_subset_root
```

The Human binding equality remains verified by P1-7 as today.

Empty applicable subset:

```text
expected refs = ()
expected root = canonical_hash([])
```

No special shortcut.

---

# 7. canonical requirement-result coverage

Historical `EvidenceSetEvaluation` with outcome SATISFIED must have the exact result-bearing requirement set.

Follow the existing `evaluate_set()` V1 rules:

```text
NOT_REQUIRED:
no EvidenceRequirementSatisfaction result emitted

FORBIDDEN:
one SATISFIED result
admitted refs = ()
coverage = ()

EXECUTOR_REQUIRED / REUSE_ALLOWED / HUMAN_OWNED:
one SATISFIED result
for the exact requirement ref
```

Require:

```text
no duplicate requirement result

no foreign requirement result

no omitted result-bearing applicable requirement

result order is the canonical applicable iteration order used by evaluate_set()
```

Do not re-evaluate freshness or coverage sufficiency from current data.

This is immutable evaluation-shape validation only.

---

# 8. canonical admitted-ref root and ordered admitted refs

From the durable requirement results, recompute exactly:

```text
expected_admitted_root =
canonical_hash(
  [
    (
      result.requirement_ref,
      list(result.admitted_evidence_refs),
      list(result.coverage)
    )
    for result in canonical requirement_results
  ]
)
```

Require:

```text
expected_admitted_root
== evaluation.admitted_ref_root_hash
== attestation.admitted_ref_root_hash
```

Then compute:

```text
expected_ordered_admitted_refs =
tuple(
  sorted(
    set(
      every admitted ref across result-bearing requirement_results
    )
  )
)
```

Require:

```text
expected_ordered_admitted_refs
== attestation.ordered_admitted_evidence_refs
```

This closes the current gap where the attestation-only ordered refs can differ from the Evaluation's actual
requirement-result content.

---

# 9. minimal immutable AdmittedEvidence reference validation

For every non-empty admitted ref in the canonical historical requirement results:

Resolve exact:

```text
AdmittedEvidenceRow
```

using the accepted ref format/version.

At minimum verify:

```text
serialized ref resolves to the exact admitted_evidence_id

row.work_run_id == attestation.work_run_id

row.checkpoint_ref == attestation.checkpoint_ref

row.requirement_ref == result.requirement_ref

row admitted_at is timezone-aware / structurally valid

row payload has exact TaskContract id/version == attestation
```

If existing P1-6 row reconstruction can cheaply validate the row's immutable candidate/content identity,
reuse it.

This Task does NOT require:

```text
current evidence effectiveness
current no-invalidating-event
freshness policy replay
reuse-consumption replay
```

and does not require a new P1-6 admission decision verifier unless the accepted schema/helper already exposes
one needed for basic immutable row identity.

Missing/wrong admitted ref:

```text
PROVENANCE_INCOMPLETE / AUTHORITY_CONFLICT
```

---

# 10. deterministic evaluation/attestation identity remains required

Preserve the existing checks:

```text
evaluation ID
attestation ID
issuer/version
authority revision
issued_at
SATISFIED outcome
row/payload exact shape
```

But compute the expected identity only after canonical roots are reconstructed.

Required:

```text
canonical graph
→ roots
→ deterministic evaluation ID
→ deterministic attestation ID
```

not:

```text
stored roots
→ deterministic ID
→ assume roots are canonical
```

---

# 11. mandatory corruption proofs

Fresh PostgreSQL negative proofs:

## CHECKPOINT_ANCHOR

```text
P1-6 attestation checkpoint_fingerprint
+ Human guard binding changed coherently
while checkpoint row unchanged
→ fail closed

checkpoint target/purpose or set relation mismatch
→ fail closed
```

## REQUIREMENT_SET_ROOT

```text
attestation + evaluation full_requirement_root_hash changed coherently
while durable RequirementSet remains unchanged
→ fail closed

RequirementSet ordered requirement refs/root mismatch
→ fail closed
```

## APPLICABLE_SUBSET

```text
attestation + evaluation applicable-ref list changed coherently
while stored subset root is left unchanged
→ fail closed

forged applicable list + forged subset root
that does not match durable requirement applicability/fingerprints
→ fail closed

empty subset
→ canonical_hash([]) positive proof
```

## RESULT_AND_ADMITTED_ROOT

```text
duplicate requirement result
→ fail closed

foreign requirement result
→ fail closed

required result omitted
→ fail closed

attestation ordered_admitted_evidence_refs changed
+ Human guard binding changed coherently
while Evaluation result content unchanged
→ fail closed

admitted_ref_root altered away from canonical result hash
→ fail closed
```

## ADMITTED_REF

```text
result admitted ref points to missing AdmittedEvidenceRow
→ fail closed

row belongs to wrong WorkRun/checkpoint/requirement
→ fail closed
```

---

# 12. positive historical proof

Prove:

```text
valid PRE_HUMAN attestation
→ historical HumanResult replay succeeds

WorkRun later advances
and P1-6 attestation is no longer current/effective
→ historical replay still succeeds

later evidence authority invalidation/supersession event
→ does not rewrite whether the old attestation was validly issued
→ current guard use remains separately unusable where applicable
```

Do not accidentally turn the historical verifier into `load_effective_attestation()`.

---

# 13. preserve 0051 / 0148 / 0225 / 1142 / 1241 / 1346 closures

Fresh regression must preserve:

```text
cross-scope Human/Judgment authority

durable current gate authenticity

Judgment policy and COMMAND_CENTER authority

expiry lifecycle + post-lock time

global HumanResult/Judgment identity

historical HumanResult/Judgment provenance

gate/Judgment correction graph and cycles

canonical P1-4 opening transition root

owner-backed G_HUMAN_REQUIRED

full WorkRun admitted-step integrity
```

No accepted design or P1-6 admission semantic change.

---

# 14. expected source scope

Primary expected change:

```text
src/aiscc/evidence/repository.py
tests/integration/human/test_postgres_human_gate_judgment.py
```

Optional narrow tests:

```text
tests/integration/evidence/**
```

Only if clearer for the new P1-6 historical verifier.

No migration should be required; current P1-6 schema already stores:

```text
RequirementSet
Requirement
Checkpoint
SetEvaluation
SetAttestation
AdmittedEvidence
```

If an exact historical root cannot be reconstructed from those durable rows:

```text
STOP
→ POLICY_BASELINE_GAP
```

Do not add P1-7 shadow fields.

Governance/report:

```text
.aiassistant/records/aiscc/cycles/
20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-hold-1.cycle.md

.aiassistant/tasks/active/
20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-runtime-rework-1.md

.aiassistant/tasks/done/
20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-runtime-rework-1.md

.aiassistant/reports/target/
20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-runtime-rework-1/**
```

---

# 15. forbidden

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

WorkflowState / transition matrix changes

P1-6 evidence profile/admission/freshness/reuse semantics changes

P1-7 Human/Judgment design changes

real provider / external IdP / credentialed network

deployment / Public Live

git add / commit / push
```

Runtime remains uncommitted.

---

# 16. evidence contract

## executor_required

```text
STATIC_SOURCE

POSTGRESQL_INTEGRATION

P1_6_HISTORICAL_CHECKPOINT_PROVENANCE

P1_6_HISTORICAL_REQUIREMENT_SET_ROOT

P1_6_HISTORICAL_APPLICABLE_SUBSET_ROOT

P1_6_HISTORICAL_RESULT_ROOT

P1_6_HISTORICAL_ADMITTED_REF_INTEGRITY

CORRUPTION_FAIL_CLOSED

HISTORICAL_REPLAY

0051_REGRESSION
0148_REGRESSION
0225_REGRESSION
1142_REGRESSION
1241_REGRESSION
1346_REGRESSION

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

# 17. mandatory stop

STOP on:

```text
HEAD drift

accepted design SHA drift

predecessor `20 paths / 4bbc...` drift

need to change accepted P1-7 design

need to change P1-6 admission semantics

durable P1-6 schema cannot reconstruct canonical historical roots

unrelated dirty collision
```

---

# 18. accept criteria

All must hold:

```text
historical checkpoint fingerprint is anchored to exact immutable checkpoint row

full RequirementSet root is reconstructed from durable ordered requirement definitions

applicable refs are derived from immutable checkpoint applicability

checkpoint subset root is recomputed

SATISFIED result set exactly matches applicable result-bearing requirements

admitted root is recomputed from canonical requirement results

attestation ordered admitted refs equal exact sorted union of result refs

every admitted ref minimally resolves to matching historical AdmittedEvidenceRow

corrupt but mutually equal attestation/evaluation values cannot substitute canonical roots

historical verification does not require current P1-6 effectiveness

1346 owner-backed Human guard and full WorkRun history regressions PASS

0051/0148/0225/1142/1241 regressions PASS

P1-4/P1-6 regressions PASS

P1-8 remains NOT_STARTED

provider/network/credential/deployment = 0

Stage 1 Git commit = none
```

---

# 19. report requirements

Report exact:

1. task path
2. start/final HEAD
3. accepted design SHA
4. predecessor `20 paths / 4bbc...` verification
5. 1447 HOLD Cycle placement
6. historical checkpoint verifier checks
7. RequirementSet/Requirement immutable reconstruction
8. full requirement root recomputation
9. applicable subset derivation/root recomputation
10. exact SATISFIED requirement-result set rule
11. admitted root recomputation
12. ordered admitted ref union rule
13. admitted-row structural validation
14. coherent checkpoint-fingerprint corruption proof
15. coherent full-root corruption proof
16. coherent applicable-list/subset-root corruption proof
17. result/admitted-root corruption proof
18. missing/wrong admitted-ref proof
19. non-current-but-valid P1-6 historical replay
20. 0051 regression
21. 0148 regression
22. 0225 regression
23. 1142 regression
24. 1241 regression
25. 1346 regression
26. P1-4 regression
27. P1-6 regression
28. PostgreSQL/version/test counts
29. final runtime path count / aggregate SHA
30. provider/network/credential actions
31. P1-8 = NOT_STARTED
32. Git actions = none
33. human verification = HUMAN_PENDING
34. preserved exact paths
35. next recommendation

---

# 20. export

Target:

```text
.aiassistant/reports/target/
20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-runtime-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include all changed runtime/test paths plus the 1447 HOLD Cycle.

Manifest:

```text
actual copied-byte SHA
64 lowercase hex
source/copy identity PASS
runtime aggregate from actual exported runtime bytes
```

---

# 21. lifecycle / Git

Start:

```text
.aiassistant/tasks/active/
20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-runtime-rework-1.md
```

Finish:

```text
.aiassistant/tasks/done/
20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-runtime-rework-1.md
```

No Git add/commit/push.

Expected final HEAD:

```text
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

---

# 22. preserved exact paths

Must preserve all existing accepted/HOLD lineage and additionally:

```text
.aiassistant/records/aiscc/cycles/
20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-runtime-rework-1.md
```

Canonical state files remain preserved and unchanged.

---

# 23. final state

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
