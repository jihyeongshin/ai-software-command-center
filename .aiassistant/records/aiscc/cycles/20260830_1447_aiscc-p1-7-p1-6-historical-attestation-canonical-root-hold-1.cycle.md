# AISCC Cycle Record

## meta

- cycle_id: `20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-hold-1`
- date: `2026-08-30T14:47:00+09:00`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT / P1-6_EVIDENCE_PROVENANCE_CONSUMER`
- affected_areas: `G_HUMAN_REQUIRED / PRE_HUMAN historical P1-6 provenance`
- work_type: `P1_7_RUNTIME_REWORK_REVIEW`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260830_1346_aiscc-p1-7-owner-backed-guard-and-full-workrun-history-provenance-runtime-rework-1`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `P1_6_HISTORICAL_ATTESTATION_CANONICAL_ROOT_INCOMPLETE`
- cycle_record_action: `create`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-hold-1.cycle.md`

## repository snapshot

- expected current HEAD: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- P1-7 accepted design commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- P1-7 design terminal commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted design SHA-256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- reviewed predecessor runtime path count: `20`
- reviewed predecessor runtime aggregate SHA-256:
  `4bbc005bda8814653269c25502d246884578f86a13050f9ae72fa4e7f4dc5508`
- Stage 1 runtime commit: `none`

## predecessor 1346 review result

1346 successfully closes the three findings that motivated it.

Accepted as closed:

```text
historical G_HUMAN_REQUIRED
→ exact durable HumanGuardAttestationRow resolution
→ CLOSED

HumanGuardAttestation PRE_HUMAN binding
→ projection-independent P1-6 attestation/evaluation resolution
→ CLOSED at row/pair level

complete admitted WorkRun history
→ every admitted step validates WorkRun identity, request fingerprint,
  matrix guards, decision owner/kernel, contiguous state/version
→ CLOSED
```

Executor evidence admitted:

```text
focused new PostgreSQL proofs:
2 PASS

targeted P1-4/P1-6/P1-7 PostgreSQL:
26 PASS

full unit + integration:
163 PASS

P1-4 regression:
18 PASS

P1-6 regression:
6 PASS

ruff:
PASS

mypy:
67 source files / PASS

PostgreSQL:
17.6

Alembic:
20260829_0004

provider/network/credential/deployment:
0

P1-8:
NOT_STARTED

Stage 1 Git commit:
none
```

Export independently verified by Command Center:

```text
runtime paths:
20

manifest SHA ↔ actual exported bytes:
20/20 MATCH

aggregate SHA-256:
4bbc005bda8814653269c25502d246884578f86a13050f9ae72fa4e7f4dc5508
```

---

# load-bearing finding — the new historical P1-6 verifier validates the attestation/evaluation pair but does not reconstruct its canonical evidence roots

1346 added:

```text
src/aiscc/evidence/repository.py
verify_historical_set_attestation_provenance(...)
```

This is the correct owner boundary and must be preserved.

It currently verifies:

```text
EvidenceSetAttestationRow exact payload shape
row ↔ EvidenceSetSatisfactionAttestation reconstruction
referenced EvidenceSetEvaluationRow existence
evaluation exact payload shape
SATISFIED requirement-result shape
deterministic evaluation/attestation IDs
attestation ↔ evaluation field equality
issuer/version/revision equality
```

However, several values that represent P1-6 evidence truth are only compared between the attestation and
evaluation rows. They are not recomputed from the durable P1-6 authority objects from which `evaluate_set()`
originally derived them.

Required invariant:

```text
attestation value == evaluation value
!= canonical P1-6 root provenance
```

## FINDING-1 — checkpoint fingerprint is not anchored to the durable checkpoint

The historical verifier does not load:

```text
EvidenceCheckpointRow
```

and therefore does not prove:

```text
attestation.checkpoint_ref
→ exact checkpoint row

checkpoint row fingerprint
== attestation.checkpoint_fingerprint

checkpoint TaskContract/source state/target or transition-purpose
== attestation/evaluation

checkpoint requirement_set_ref
== attestation RequirementSet
```

A coherently modified:

```text
EvidenceSetAttestationRow.checkpoint_fingerprint
+
HumanRequiredEvidenceBinding.checkpoint_fingerprint
```

can remain acceptable because the referenced Evaluation stores checkpoint ref but not checkpoint fingerprint.

Required:

```text
historical checkpoint fingerprint
→ exact immutable System/TaskContract-owned checkpoint row
```

Current checkpoint effectiveness/revocation is NOT required for historical replay.

---

# FINDING-2 — full RequirementSet root is not anchored to the durable RequirementSet definition

The historical verifier does not load/reconstruct:

```text
EvidenceRequirementSetRow
```

and therefore does not prove:

```text
set TaskContract id/version
set identity/version
ordered requirement refs
ordered checkpoint refs
set fingerprint
requirement_root_hash
```

against the attestation/evaluation.

`full_requirement_root_hash` is not part of the current evaluation identity hash, so an attestation and
evaluation can be changed coherently to another full root while retaining the same evaluation/attestation ID
if the subset/admitted roots are left unchanged.

Required:

```text
historical full_requirement_root_hash
== immutable RequirementSetRow.requirement_root_hash
== canonical root of the set's durable ordered requirement definitions
```

---

# FINDING-3 — applicable-ref list is not proven to produce checkpoint_subset_root_hash

`evaluate_set()` originally computes:

```text
applicable =
requirements whose applicable_checkpoint_refs contain checkpoint_ref

subset_root =
canonical_hash(
  [(requirement_ref, requirement.fingerprint) for requirement in applicable]
)
```

The historical verifier currently checks only:

```text
evaluation_payload.ordered_applicable_requirement_refs
== attestation.ordered_applicable_requirement_refs

evaluation.checkpoint_subset_root_hash
== attestation.checkpoint_subset_root_hash
```

It does not verify the relation between the list and the root.

Therefore a coherently changed applicable-ref list can coexist with the old root.

Required:

```text
exact applicable refs
→ derived from immutable RequirementSet/Requirement rows + checkpoint ref

checkpoint_subset_root_hash
→ recomputed from those exact refs/fingerprints
```

Empty applicable subset must still verify as:

```text
canonical_hash([])
```

---

# FINDING-4 — requirement_results, ordered admitted refs, and admitted_ref_root are not tied together

`evaluate_set()` originally computes:

```text
requirement_results
→ exact per-applicable-requirement SATISFIED results

ordered_admitted_evidence_refs
→ sorted unique union of result admitted refs

admitted_ref_root_hash
→ canonical_hash(
    [(requirement_ref, admitted refs, coverage) for result in requirement_results]
  )
```

The new historical verifier currently validates that requirement result entries have a legal shape and
`SATISFIED` outcome, but it does not verify:

```text
requirement_results exactly cover the applicable result-bearing requirements

no duplicate/foreign requirement result

ordered_admitted_evidence_refs
== exact sorted unique union from requirement_results

admitted_ref_root_hash
== canonical hash of requirement_results
```

In particular, `ordered_admitted_evidence_refs` exists only on the attestation side, so it can be changed
coherently with the Human guard binding while the Evaluation/result root remains unchanged.

Required:

```text
historical admitted refs/root
→ canonical reconstruction from immutable SATISFIED evaluation result content
```

---

# FINDING-5 — admitted refs are not minimally resolved as immutable P1-6 admitted evidence rows

For each non-empty admitted ref represented by a historical SATISFIED result, the historical verifier should
at minimum prove the durable referenced:

```text
AdmittedEvidenceRow
```

exists and structurally matches:

```text
serialized admitted ref/version
work_run_id
checkpoint_ref
requirement_ref
```

and the exact ref used by the result.

Do not require that the evidence remains current/unrevoked at historical replay time.

This Task does not require re-evaluating freshness, coverage policy, or current evidence admission truth.

Required separation:

```text
immutable admitted-evidence issuance/reference integrity
!= current evidence effectiveness
```

---

# why this blocks P1-7 final runtime acceptance

`G_HUMAN_REQUIRED` historical provenance now correctly resolves:

```text
Evaluation
→ HumanGuardAttestationRow
→ HumanRequiredEvidenceBinding
→ P1-6 EvidenceSetSatisfactionAttestation
```

but the last object is currently accepted if its attestation/evaluation pair is internally equal even when
its canonical checkpoint/RequirementSet/applicable/admitted root relationships are inconsistent.

Therefore:

```text
owner-backed Human guard
→ yes

canonical owner-backed PRE_HUMAN evidence provenance
→ not yet fully proven
```

The gap is inside the new historical verifier, not in accepted P1-6 admission semantics.

---

# command-center judgment

- result_status: `HOLD_REWORK_REQUIRED`
- P1-7 Design: `REMAINS ACCEPTED / CLOSED`
- Stage 0A/0B commits: `PRESERVE`
- 0051 findings: `CLOSED`
- 0148 findings: `CLOSED`
- 0225 findings: `CLOSED`
- 1142 findings: `CLOSED`
- 1241 findings: `CLOSED`
- 1346 direct findings: `CLOSED`
- P1-7 Runtime: `REWORK_REQUIRED / HUMAN_PENDING`
- P1-8: `NOT_STARTED`
- PUBLIC_BOUNDED_LIVE: `NOT_RELEASED`
- Stage 1 runtime commit: `none`
- required rework:
  1. anchor historical checkpoint identity/fingerprint to `EvidenceCheckpointRow`;
  2. anchor RequirementSet root/identity to durable set + requirement definitions;
  3. recompute applicable subset/root;
  4. recompute result coverage/admitted-ref root and ordered admitted refs;
  5. minimally resolve admitted refs to matching historical `AdmittedEvidenceRow`;
  6. preserve historical-vs-current P1-6 authority separation.
- terminal_decision_reason:
  `P1-7 now reaches the durable P1-6 attestation, but that historical verifier still trusts several roots/lists because two P1-6 rows agree rather than proving those values from the immutable P1-6 authority graph that originally produced them.`

## preserved artifacts

Do not amend/revert:

```text
238b0b41460c2504fd3244eadb06809d8692a60f
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

Preserve all existing P1-7 accepted/HOLD lineage plus:

```text
.aiassistant/records/aiscc/cycles/
20260830_1346_aiscc-p1-7-owner-backed-guard-and-full-workrun-history-provenance-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-hold-1.cycle.md
```

## next action

```text
P1-7 narrow P1-6 historical-attestation canonical-root rework
→ Command Center runtime re-review
→ Human final P1-7 runtime review only after PASS

P1-8:
NOT_STARTED
```
