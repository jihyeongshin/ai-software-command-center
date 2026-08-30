# AISCC Cycle Record

## meta

- cycle_id: `20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-hold-1`
- date: `2026-08-30T15:30:00+09:00`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT / P1-6_EVIDENCE_PROVENANCE_CONSUMER`
- affected_areas: `PRE_HUMAN historical P1-6 provenance / AdmittedEvidence issuance chain`
- work_type: `P1_7_RUNTIME_REWORK_REVIEW`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-runtime-rework-1`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `P1_6_HISTORICAL_ADMITTED_EVIDENCE_ISSUANCE_INCOMPLETE`
- cycle_record_action: `create`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-hold-1.cycle.md`

## repository snapshot

- expected current HEAD: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- P1-7 accepted design commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- P1-7 design terminal commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted design SHA-256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- reviewed predecessor runtime path count: `21`
- reviewed predecessor runtime aggregate SHA-256:
  `4a5d372f984145f3b0faef084bb0f13002ac2cdf384f7863ff50ee19c1068835`
- Stage 1 runtime commit: `none`

## predecessor 1447 review result

1447 successfully closes every canonical-root finding that motivated it.

Accepted as closed:

```text
historical checkpoint fingerprint
→ exact immutable EvidenceCheckpointRow
→ CLOSED

RequirementSet full root
→ durable ordered EvidenceRequirement rows
→ CLOSED

applicable refs / checkpoint subset root
→ canonical immutable applicability derivation
→ CLOSED

SATISFIED requirement result set
→ exact applicable result-bearing requirements
→ CLOSED

admitted_ref_root
→ canonical requirement-result hash
→ CLOSED

ordered_admitted_evidence_refs
→ exact sorted result-ref union
→ CLOSED

each admitted ref
→ exact matching historical AdmittedEvidenceRow
→ CLOSED at AdmittedEvidence-row structural level

historical validity
!= current P1-6 effectiveness
→ preserved
```

Executor evidence admitted:

```text
focused new PostgreSQL:
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

Export independently verified:

```text
runtime paths:
21

manifest SHA ↔ actual exported bytes:
21/21 MATCH

aggregate SHA-256:
4a5d372f984145f3b0faef084bb0f13002ac2cdf384f7863ff50ee19c1068835
```

---

# load-bearing finding — AdmittedEvidenceRow existence is not proof of a valid P1-6 ADMITTED admission

The new:

```text
_verify_historical_admitted_ref(...)
```

correctly proves that a referenced `AdmittedEvidenceRow` structurally matches:

```text
serialized admitted ref/version
work_run_id
checkpoint_ref
requirement_ref
TaskContract id/version
content hash
coverage
admitted_at
```

However, the row also contains the load-bearing provenance links:

```text
decision_id
candidate_id
candidate_version/fingerprint
```

and those are not historically verified.

Current historical verification therefore does not prove that the admitted row was produced by:

```text
EvidenceCandidate
→ EvidenceAdmissionRequest
→ EvidenceEvaluation
→ EvidenceAdmissionDecision(ADMITTED)
→ AdmittedEvidence
```

It only proves that an `AdmittedEvidenceRow` with matching surface bindings exists.

## concrete invalid state that can pass current verifier

PostgreSQL FKs prove only existence:

```text
AdmittedEvidenceRow.decision_id
→ some EvidenceAdmissionDecisionRow

AdmittedEvidenceRow.candidate_id
→ some EvidenceCandidateRow
```

They do not prove:

```text
decision.outcome == ADMITTED

decision/admission request candidate == admitted candidate

request requirement/work_run/checkpoint == admitted row

request candidate fingerprint == immutable candidate fingerprint

evaluation belongs to the exact request

decision belongs to the exact evaluation/request

evaluation represented the accepted P1-6 admission dimensions

admitted_at == valid ADMITTED decision time
```

Therefore a database-corrupt but FK-valid graph can contain:

```text
REJECTED EvidenceAdmissionDecisionRow
+
AdmittedEvidenceRow referencing that decision
```

and `_verify_historical_admitted_ref()` can still accept that row if its surface WorkRun/checkpoint/requirement
fields match the set evaluation.

Required invariant:

```text
AdmittedEvidenceRow
!= valid P1-6 admitted authority by itself
```

Historical P1-6 set provenance must reach the immutable System admission decision that created each admitted
evidence ref.

---

# required historical admission chain

Create/reuse a projection-independent P1-6 verifier equivalent to:

```text
_verify_historical_admitted_evidence_provenance_in_session(...)
```

For each historical admitted ref, prove at minimum:

## EvidenceCandidate

```text
exact EvidenceCandidateRow exists

candidate_id/version/fingerprint exact

candidate fingerprint recomputed from immutable candidate row/payload using the canonical P1-6
candidate_fingerprint() algorithm

TaskContract id/version == attestation

checkpoint_ref == attestation checkpoint

content hash == admitted row content

candidate ref stored by AdmittedEvidenceRow
== exact immutable candidate identity
```

Do not require the candidate's current effectiveness.

## EvidenceAdmissionRequest

Resolve the exact request through the admitted row's decision.

Verify:

```text
request exists exactly once

request.candidate_id == admitted candidate

request candidate version/fingerprint == exact candidate

request requirement_ref == admitted requirement

request RequirementSet == historical attestation RequirementSet

request work_run_id == admitted/attestation WorkRun

request checkpoint_ref == admitted/attestation checkpoint

request TaskContract id/version == attestation

request observed state/version == historical attestation state/version

request target / transition-purpose == historical checkpoint/use

request requirement fingerprint/root/checkpoint fingerprint
== exact immutable requirement/set/checkpoint authority already reconstructed by the historical set verifier

request_fingerprint recomputes from immutable request inputs using the canonical P1-6 request-fingerprint semantics
```

If the request fingerprint cannot be recomputed from current durable fields:

```text
STOP
→ POLICY_BASELINE_GAP
```

Do not skip it.

## EvidenceEvaluation

Verify exactly one evaluation for the request.

At minimum:

```text
evaluation.admission_request_id == request

authority_version == accepted P1-6 evaluation authority version

evaluated_at is structurally valid

dimension_results exact canonical shape

every dimension required by the accepted P1-6 admission evaluator is present exactly once

for an ADMITTED decision:
every required dimension outcome is SATISFIED/PASS according to the accepted exact vocabulary

authority_ref / authority_version fields have the exact durable shape required by the accepted dimension contract
```

Do not re-run provider/tool/Human external evidence.

This is immutable historical System-evaluation provenance verification.

If a dimension has an owner-backed durable authority ref that P1-6 already exposes a canonical historical
verifier for, consume it. Do not invent a weaker P1-7 assertion.

## EvidenceAdmissionDecision

Verify exact decision:

```text
decision_id == AdmittedEvidenceRow.decision_id

decision.admission_request_id == request

decision.evaluation_id == evaluation

outcome == ADMITTED

reason == accepted ADMITTED reason

secondary reasons exact legal empty/admitted shape

admitting_authority_version == accepted P1-6 authority version

decided_at == admitted.admitted_at
```

A REJECTED/invalid decision can never justify `AdmittedEvidence`.

## AdmittedEvidence final binding

After the admission chain is valid:

```text
AdmittedEvidenceRow.candidate_id
== request/evaluation/decision candidate

AdmittedEvidenceRow.requirement_ref
== request requirement

AdmittedEvidenceRow.work_run_id
== request WorkRun

AdmittedEvidenceRow.checkpoint_ref
== request checkpoint

AdmittedEvidenceRow content/coverage
== immutable candidate/admission output

AdmittedEvidenceRow admitted_at
== decision.decided_at
```

Only then may the historical set verifier count this ref in the canonical admitted-root graph.

---

# historical-vs-current boundary

Preserve:

```text
valid historical admission issuance
!= currently effective admitted evidence
```

Do not require:

```text
no later REVOKED/SUPERSEDED/CORRECTED event

current WorkRun state/version

current freshness

current reuse allowance

current content/config authority
```

A later invalidation may prevent current set satisfaction but does not erase the fact that the evidence was
validly admitted at the historical PRE_HUMAN checkpoint.

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
- 1346 findings: `CLOSED`
- 1447 direct findings: `CLOSED`
- P1-7 Runtime: `REWORK_REQUIRED / HUMAN_PENDING`
- P1-8: `NOT_STARTED`
- PUBLIC_BOUNDED_LIVE: `NOT_RELEASED`
- Stage 1 runtime commit: `none`
- required rework:
  `historical AdmittedEvidence → exact P1-6 candidate/request/evaluation/ADMITTED-decision issuance chain`
- terminal_decision_reason:
  `1447 now proves the canonical set/root graph down to each AdmittedEvidenceRow, but the last row can still be treated as admitted historical authority without proving the System ADMITTED decision chain that created it.`

## preserved artifacts

Do not amend/revert:

```text
238b0b41460c2504fd3244eadb06809d8692a60f
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

Preserve all existing P1-7 accepted/HOLD lineage plus:

```text
.aiassistant/records/aiscc/cycles/
20260830_1447_aiscc-p1-7-p1-6-historical-attestation-canonical-root-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-hold-1.cycle.md
```

## next action

```text
P1-7 narrow P1-6 historical AdmittedEvidence issuance-chain rework
→ Command Center runtime re-review
→ Human final P1-7 runtime review only after PASS

P1-8:
NOT_STARTED
```
