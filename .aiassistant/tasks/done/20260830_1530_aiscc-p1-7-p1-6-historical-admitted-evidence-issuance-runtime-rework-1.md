# 작업지시서: P1-7 / P1-6 Historical AdmittedEvidence Issuance Runtime Rework

## meta

- task_id: `20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-runtime-rework-1`
- created_at: `2026-08-30T15:30:00+09:00`
- phase: `P1-7 Human Gate and Judgment`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT / P1-6_EVIDENCE_PROVENANCE`
- expected_start_head: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted_design_commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- accepted_design_terminal_commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted_design_sha256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- predecessor_runtime_path_count: `21`
- predecessor_runtime_aggregate_sha256: `4a5d372f984145f3b0faef084bb0f13002ac2cdf384f7863ff50ee19c1068835`
- p1_7_runtime_status: `REWORK_REQUIRED / HUMAN_PENDING`
- p1_8_status: `NOT_STARTED`

---

# 1. current state

1447 closed its intended canonical checkpoint/set/subset/result/admitted-ref root findings.

Do not reopen:

```text
checkpoint immutable anchor

RequirementSet / Requirement canonical root

applicable subset derivation/root

SATISFIED result set

admitted-ref root

ordered admitted-ref union

historical-vs-current P1-6 separation

owner-backed G_HUMAN_REQUIRED

full P1-4 WorkRun admitted history

all earlier P1-7 corrections
```

Remaining issue:

```text
historical set attestation
→ canonical admitted ref
→ AdmittedEvidenceRow
```

stops before proving:

```text
EvidenceCandidate
→ AdmissionRequest
→ Evaluation
→ ADMITTED Decision
→ AdmittedEvidence
```

Place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-hold-1.cycle.md
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
21 paths /
4a5d372f984145f3b0faef084bb0f13002ac2cdf384f7863ff50ee19c1068835
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
EvidenceCandidate != AdmittedEvidence

P1-6 admission decision
→ owns whether evidence became admitted

P1-7 historical Human authority
→ may consume valid immutable P1-6 admitted provenance
→ must not mint or reinterpret admission truth
```

New exact rule:

```text
AdmittedEvidenceRow existence / FK integrity
!= historical ADMITTED authority
```

---

# 4. implement projection-independent historical AdmittedEvidence provenance verifier

Strengthen:

```text
_verify_historical_admitted_ref(...)
```

or create one exact owner helper equivalent to:

```text
_verify_historical_admitted_evidence_provenance_in_session(...)
```

Return/reuse immutable `AdmittedEvidence` only after the full P1-6 issuance chain is proven.

---

# 5. immutable EvidenceCandidate provenance

Resolve:

```text
EvidenceCandidateRow
```

by `AdmittedEvidenceRow.candidate_id`.

Reconstruct an `EvidenceCandidate` from the row using the same immutable row/payload semantics as persistence.

Verify exact payload shape and at minimum:

```text
candidate_id
candidate_version
candidate_fingerprint
TaskContract id/version
checkpoint_ref
issuer owner type/id/version/authority_ref
producer WorkRun / execution attempt / operation
observed state/version
subject/scope/resource
evidence type id/version
content ref
observed_at / created_at
coverage
producer_attestation_ref
human producer category / ingress ref
prior admitted ref
config version
```

Recompute:

```text
candidate_fingerprint(value)
```

using the canonical function from:

```text
src/aiscc/evidence/issuers.py
```

Require exact equality with the durable row.

Also require:

```text
AdmittedEvidenceRow candidate_id == candidate

AdmittedEvidenceRow content_hash == candidate.content_ref.content_hash

AdmittedEvidenceRow payload candidate_version/fingerprint == exact candidate
```

Do not require current issuer effectiveness.

If HUMAN_DIRECT_EVIDENCE candidate has an ingress ref, preserve existing accepted issuer/ingress structural
rules; do not broaden into P1-7 HumanGate semantics.

---

# 6. immutable EvidenceAdmissionRequest provenance

Resolve the request through the exact:

```text
EvidenceAdmissionDecisionRow
→ admission_request_id
```

Require one request/evaluation/decision chain.

Reconstruct the exact request immutable body.

Verify:

```text
request.candidate_id == candidate.candidate_id

payload candidate_version/fingerprint == candidate

request.requirement_ref == historical admitted requirement

request.requirement_set_ref == historical set

request.work_run_id == historical attestation WorkRun

request.checkpoint_ref == historical checkpoint

request.observed_state/version == historical attestation state/version

payload TaskContract id/version == historical attestation

payload requirement_fingerprint
== immutable historical EvidenceRequirement fingerprint

payload requirement_root_hash
== immutable historical RequirementSet full root

payload checkpoint_fingerprint
== immutable historical checkpoint fingerprint

payload target_state
== historical checkpoint target

payload transition purpose id/version
== historical checkpoint purpose

requester identity exact non-empty accepted System requester shape
```

## request fingerprint

Recompute the request fingerprint using the exact canonical P1-6 `make_admission_request`/request-fingerprint
algorithm.

Do not create a second subtly different fingerprint function.

If no reusable canonical function currently exists, extract one from the accepted request constructor and use it
for both current request creation and historical verification without changing semantic inputs.

Required:

```text
durable request.request_fingerprint == recomputed canonical fingerprint
```

If current durable schema lacks any input required to recompute it:

```text
STOP
→ POLICY_BASELINE_GAP
```

---

# 7. immutable EvidenceEvaluation provenance

Resolve exactly one:

```text
EvidenceEvaluationRow
```

for the request.

Verify:

```text
evaluation_id relation
admission_request_id relation
authority_version
evaluated_at
dimension_results exact canonical payload shape
```

Read exact accepted P1-6 dimension vocabulary from the current admission evaluator.

For an ADMITTED decision, prove:

```text
the exact required dimension set is present exactly once

no unknown/duplicate dimension

each required dimension has the accepted positive/satisfied outcome

authority_ref / authority_version shape is valid for that dimension
```

Do NOT re-run external provider/tool/Human work.

Do NOT ask whether those authorities are current now.

This is immutable historical System-evaluation provenance.

If an exact dimension has an owner-backed durable authority that the accepted P1-6 runtime already requires
for admission and a projection-independent verifier exists, consume it. Otherwise verify the exact durable
evaluation record that the P1-6 evaluator persisted; do not invent new future-owner semantics.

---

# 8. immutable EvidenceAdmissionDecision provenance

Resolve exactly one:

```text
EvidenceAdmissionDecisionRow
```

and verify:

```text
decision_id == AdmittedEvidenceRow.decision_id

admission_request_id == request

evaluation_id == evaluation

outcome == ADMITTED

reason == exact accepted ADMITTED reason

secondary_reasons == exact legal ADMITTED shape

admitting_authority_version == exact accepted P1-6 authority version

decided_at timezone-aware
```

Require:

```text
AdmittedEvidenceRow.admitted_at == decision.decided_at
```

A decision with:

```text
REJECTED
wrong evaluation
wrong request
wrong admitting authority
```

must fail closed.

---

# 9. final AdmittedEvidence binding

After candidate/request/evaluation/decision provenance verifies, reconstruct the admitted object.

Require exact:

```text
admitted_evidence_id / serialized ref

decision_id

candidate ref

requirement ref

TaskContract id/version

work_run_id

checkpoint ref

content ref

coverage

admitted_at
```

against all immutable upstream authority.

At minimum:

```text
admitted content == candidate content

admitted coverage == sorted candidate coverage as accepted admission output

admitted requirement/run/checkpoint == request

admitted TaskContract == request/candidate

admitted_at == ADMITTED decision time
```

Only then count this admitted ref when reconstructing the historical set evaluation roots.

---

# 10. historical-vs-current separation

Do not query current invalidation as the historical criterion.

Historical verification must continue to pass after later:

```text
EvidenceAuthorityEvent REVOKED
SUPERSEDED
CORRECTED

WorkRun state/version advance

freshness expiry

reuse consumption
```

provided the old evidence was validly admitted at the historical checkpoint.

Current `load_effective_attestation()` / set evaluation remains responsible for current effectiveness.

---

# 11. mandatory corruption proofs

Fresh PostgreSQL negative proofs:

## CANDIDATE

```text
candidate fingerprint changed
→ fail closed

candidate immutable payload changed + stored fingerprint not matching
→ fail closed

admitted row candidate payload fingerprint/version differs from CandidateRow
→ fail closed
```

## REQUEST

```text
request candidate differs from admitted candidate
→ fail closed

request requirement/set/checkpoint/run differs
→ fail closed

request requirement/checkpoint/root fingerprint changed coherently in request payload only
→ fail closed

request_fingerprint changed
→ fail closed
```

## EVALUATION

```text
evaluation missing/duplicate
→ fail closed

required dimension omitted
→ fail closed

dimension duplicate/unknown
→ fail closed

required dimension non-positive
while Decision remains ADMITTED
→ fail closed
```

## DECISION

```text
AdmittedEvidenceRow points to REJECTED decision
→ fail closed

decision request/evaluation mismatch
→ fail closed

wrong admitting authority version
→ fail closed

decision time differs from admitted_at
→ fail closed
```

## FINAL BINDING

```text
admitted content hash differs from candidate
→ fail closed

admitted coverage differs from canonical candidate coverage
→ fail closed
```

Use accepted sanitized:

```text
PROVENANCE_INCOMPLETE
AUTHORITY_CONFLICT
```

No auto-repair.

---

# 12. positive proof

Prove:

```text
valid historical admitted evidence chain
→ historical PRE_HUMAN attestation verifies
→ historical HumanResult replay succeeds

later admitted-evidence invalidation/current ineffectiveness
→ historical chain still verifies

current set/evidence authority
→ separately refuses stale/revoked evidence where accepted behavior requires
```

---

# 13. preserve all earlier closures

Fresh regression must preserve:

```text
1447 canonical checkpoint/set/subset/result roots

1346 owner-backed Human guard + full WorkRun history

1241 P1-4 opening transition root

1142 transitive gate/Judgment graph

0225 direct historical Human/Judgment provenance

0148 global identity/time/idempotency

0051 cross-scope/policy/COMMAND_CENTER/expiry

P1-6 current admission/freshness/reuse semantics

P1-4 transition ownership
```

---

# 14. expected source scope

Likely narrow changes:

```text
src/aiscc/evidence/repository.py
src/aiscc/evidence/issuers.py
```

Only if a canonical request-fingerprint helper needs extraction.

Tests:

```text
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
```

No migration should be required because the current durable schema already stores:

```text
EvidenceCandidate
EvidenceAdmissionRequest
EvidenceEvaluation
EvidenceAdmissionDecision
AdmittedEvidence
```

If exact request/evaluation historical identity cannot be reconstructed from current schema:

```text
STOP
→ POLICY_BASELINE_GAP
```

Do not add P1-7 shadow authority.

Governance/report:

```text
.aiassistant/records/aiscc/cycles/
20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-hold-1.cycle.md

.aiassistant/tasks/active/
20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-runtime-rework-1.md

.aiassistant/tasks/done/
20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-runtime-rework-1.md

.aiassistant/reports/target/
20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-runtime-rework-1/**
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

P1-6 admission dimension semantics changes

P1-6 freshness/reuse/current-effectiveness changes

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

P1_6_HISTORICAL_CANDIDATE_INTEGRITY

P1_6_HISTORICAL_REQUEST_INTEGRITY

P1_6_HISTORICAL_EVALUATION_INTEGRITY

P1_6_HISTORICAL_ADMISSION_DECISION

P1_6_HISTORICAL_ADMITTED_EVIDENCE

CORRUPTION_FAIL_CLOSED

HISTORICAL_REPLAY

1447_REGRESSION
1346_REGRESSION
1241_REGRESSION
1142_REGRESSION
0225_REGRESSION
0148_REGRESSION
0051_REGRESSION

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

predecessor `21 paths / 4a5d...` drift

need to change accepted P1-7 design

need to change P1-6 admission semantics

durable P1-6 schema cannot reconstruct exact candidate/request/evaluation/decision issuance provenance

unrelated dirty collision
```

---

# 18. accept criteria

All must hold:

```text
every historical admitted ref proves exact immutable CandidateRow

candidate fingerprint recomputed

exact AdmissionRequest relation and request fingerprint verified

exact Evaluation relation/dimension shape verified

ADMITTED Decision required

decision authority/version/time verified

AdmittedEvidence row binds exactly to candidate/request/decision output

REJECTED decision can never back an admitted historical ref

historical verifier does not require current evidence effectiveness

1447 canonical-root proofs remain PASS

1346/1241/1142/0225/0148/0051 regressions PASS

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
4. predecessor `21 paths / 4a5d...` verification
5. 1530 HOLD Cycle placement
6. historical Candidate verifier
7. canonical candidate fingerprint
8. historical AdmissionRequest verifier
9. canonical request fingerprint source/helper
10. historical Evaluation dimension verifier
11. exact positive dimension vocabulary
12. historical ADMITTED Decision verifier
13. final AdmittedEvidence binding
14. candidate corruption proof
15. request corruption/fingerprint proof
16. evaluation missing/duplicate/dimension proof
17. REJECTED-decision-backed admitted-row proof
18. decision authority/time mismatch proof
19. final content/coverage mismatch proof
20. non-current-but-valid historical replay
21. 1447 regression
22. 1346 regression
23. 1241 regression
24. 1142 regression
25. 0225 regression
26. 0148 regression
27. 0051 regression
28. P1-4 regression
29. P1-6 regression
30. PostgreSQL/version/test counts
31. final runtime path count / aggregate SHA
32. provider/network/credential actions
33. P1-8 = NOT_STARTED
34. Git actions = none
35. human verification = HUMAN_PENDING
36. preserved exact paths
37. next recommendation

---

# 20. export

Target:

```text
.aiassistant/reports/target/
20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-runtime-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include all changed runtime/test paths plus the 1530 HOLD Cycle.

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
20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-runtime-rework-1.md
```

Finish:

```text
.aiassistant/tasks/done/
20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-runtime-rework-1.md
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
20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-runtime-rework-1.md
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
