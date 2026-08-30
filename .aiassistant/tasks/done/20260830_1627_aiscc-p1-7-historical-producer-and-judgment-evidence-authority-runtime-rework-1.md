# 작업지시서: P1-7 Historical Producer + Judgment Evidence Authority Runtime Rework

## meta

- task_id: `20260830_1627_aiscc-p1-7-historical-producer-and-judgment-evidence-authority-runtime-rework-1`
- created_at: `2026-08-30T16:27:00+09:00`
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
- predecessor_runtime_aggregate_sha256: `bf3420c989694b97edce5e398420e01cd8be0c4580760fd63c2b6068c0db5b69`
- p1_7_runtime_status: `REWORK_REQUIRED / HUMAN_PENDING`
- p1_8_status: `NOT_STARTED`

---

# 1. current state

1530 closed its exact Candidate → AdmissionRequest → Evaluation → ADMITTED Decision → AdmittedEvidence chain.

Do not reopen those direct semantics.

The remaining transitive edges are:

```text
EvidenceCandidate
→ owner-specific producer authority

Judgment
→ historical P1-6 evidence attestation authority
```

Place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260830_1627_aiscc-p1-7-historical-producer-and-judgment-evidence-authority-hold-1.cycle.md
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
bf3420c989694b97edce5e398420e01cd8be0c4580760fd63c2b6068c0db5b69
```

Mismatch:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

---

# 3. enumerate exact EvidenceIssuerType categories first

Read the current canonical P1-6 source and report every exact `EvidenceIssuerType`.

Classify each as one of:

```text
SYSTEM_TOKEN
HUMAN_DIRECT
P1_5_IMMUTABLE_REF
HUMAN_P1_7
PRIOR_ADMITTED_REUSE
OTHER_OWNER_SPECIFIC
```

For each category record:

```text
current issuer authority class
current recognizes() authority source
durable owner-specific provenance available?
historical verifier required?
```

Do not guess from this Task text.

If an owner-specific category is discovered whose current `recognizes()` requires durable authority but no
durable historical source exists:

```text
STOP
→ POLICY_BASELINE_GAP
```

---

# 4. historical Candidate issuer-policy binding

For every historical Candidate, before accepting its Evaluation's `ISSUER_AUTHORITY=PASS`, verify immutable
static relationships that can be reconstructed:

```text
candidate.issuer.owner_type
is allowed by immutable EvidenceRequirement.allowed_issuer_types

candidate.issuer.owner_id
is allowed by immutable EvidenceRequirement.allowed_issuer_ids

candidate content kind/type/version
matches the immutable requirement constraints

candidate TaskContract/checkpoint/subject/scope/resource bindings
remain those already verified by the admission request
```

Also verify the exact accepted authority-ref form for the issuer category.

This does not re-run external work.

---

# 5. P1-5 historical immutable producer ref

For every P1-5 issuer category use the exact category→ref-kind mapping from current source.

Implement/reuse an in-session projection-independent owner verifier.

At minimum:

```text
candidate.producer_attestation_ref
→ exact ExecutionOutputRefRow.output_ref_id

row exists

row.execution_attempt_id == candidate.execution_attempt_id

ExecutionAttemptRow exists

attempt.work_run_id == candidate.producer_work_run_id

row.ref_kind == exact expected immutable ref kind

row.content_hash == candidate.content_ref.content_hash

row.storage_ref satisfies accepted immutable private-ref contract

candidate issuer owner id/version/authority_ref
== exact configured P1-5 issuer authority

historical Evaluation ISSUER_AUTHORITY
== exact owner authority
```

Do not require:

```text
ExecutionAttempt currently RUNNING
WorkRun currently RUNNING
current operation state
```

If current P1-5 persistence exposes a stronger historical immutable-ref integrity verifier, consume it.

Negative proofs:

```text
missing output ref
wrong ref kind
wrong attempt
foreign WorkRun attempt
wrong content hash
invalid storage ref
wrong issuer authority id/version
→ fail closed
```

Positive proof:

```text
validly admitted P1-5 candidate
after WorkRun/execution lifecycle advances
→ historical set attestation still verifies
```

---

# 6. HUMAN_P1_7 historical producer provenance

Add a projection-independent owner verifier in the P1-7 Human owner layer.

Suggested exact equivalent:

```text
verify_historical_producer_ref_in_session(
    session,
    serialized_ref,
) -> HumanP1_7EvidenceProducerRef
```

Verify:

```text
exact HumanP1_7EvidenceProducerRow

serialized ref / producer id/version

canonical producer fingerprint

row work_run_id / issued_at / payload exact

authority id/version
== accepted P1-7 producer authority

TaskContract id/version
WorkRun
source state/version
HumanGate ref/revision
HumanResult ref/revision
private human subject ref
checkpoint ref
evidence type id/version
subject/scope/resource
content hash
sensitivity
export policy
```

Then resolve:

```text
producer.human_result_ref
→ projection-independent historical HumanResult verifier
```

Require exact result/gate bindings:

```text
TaskContract
WorkRun
state/version
HumanGate ref
HumanResult ref/revision
```

No current HumanGate projection requirement.

Then historical Candidate verification for `HUMAN_P1_7` must require:

```text
candidate.producer_attestation_ref == producer.serialized_ref

candidate Task/run/state/checkpoint/type/subject/scope/resource/content/sensitivity
== producer

candidate.human_producer_category == HUMAN_P1_7

candidate issuer id/version
== accepted P1-7 producer authority
```

Negative proofs:

```text
missing producer row
producer fingerprint corruption
foreign HumanResult
wrong gate/result revision
wrong Task/run/state/checkpoint/content
→ fail closed
```

Positive proof after gate/result/workrun becomes non-current:

```text
historical producer remains validly issued
→ historical admitted evidence remains valid
```

---

# 7. PRIOR_ADMITTED_EVIDENCE historical reuse provenance

For reuse candidates:

```text
candidate.prior_admitted_evidence_ref
```

must resolve through the projection-independent historical P1-6 admitted-evidence verifier.

Do not use `load_admitted()` as the historical criterion.

Verify immutable content relation required by the accepted reuse issuer:

```text
prior content hash == candidate content hash
prior object id == candidate content object id
```

Then require exactly one durable:

```text
EvidenceReuseConsumptionRow
```

for the current admitted evidence.

Verify:

```text
consumption.admitted_evidence_id == current admitted id

prior_admitted_evidence_ref == candidate.prior ref

requirement_ref == current request requirement

work_run_id == current request WorkRun

checkpoint_ref == current request checkpoint

policy_maximum == immutable requirement.reuse_maximum

consumption_ordinal >= 1

consumption_ordinal <= policy_maximum when maximum is bounded

consumed_at == current admitted.admitted_at
```

For the exact reuse scope:

```text
prior ref
requirement
WorkRun
checkpoint
```

verify durable ordinals follow the accepted P1-6 contiguous/unique consumption contract.

Use a visited set while traversing prior-admission chains.

Any cycle:

```text
AUTHORITY_CONFLICT
```

No current reuse availability check.

Negative proofs:

```text
missing prior admission
historically invalid prior admission
missing reuse consumption row
wrong prior/current admitted binding
wrong policy maximum
wrong ordinal / duplicate or gap according to accepted contract
reuse cycle
→ fail closed
```

Positive:

```text
prior evidence later revoked
→ current historical reuse admission still proves it was validly issued then
```

---

# 8. Human direct and System token categories

Preserve the existing Human direct ingress verifier.

Do not replace it.

For intentional System token categories:

```text
TokenEvidenceIssuer
```

do not attempt to reconstruct process-local `_issuer_token`.

Historical authority is the immutable System admission Evaluation/Decision plus the static policy bindings that
can be reconstructed from Candidate/Requirement.

But enforce exact configured issuer identity shape.

If a category is not truly System-token-owned and requires an external/durable owner verifier:

```text
do not treat it as System token
```

---

# 9. historical Judgment evidence-attestation dependency

In:

```text
_verify_judgment_base_issuance_provenance_in_session(...)
```

after immutable policy is reconstructed, validate evidence semantics.

## 9.1 required evidence

If:

```text
policy.requires_post_human_evidence == True
```

then:

```text
value.evidence_attestation_ref must be present
value.evidence_authority_revision must be present
value.evidence_root must be present
```

Missing:

```text
PROVENANCE_INCOMPLETE
```

## 9.2 present evidence

Whenever:

```text
value.evidence_attestation_ref is not None
```

call the projection-independent P1-6:

```text
verify_historical_set_attestation_provenance(
    session,
    value.evidence_attestation_ref,
)
```

Require:

```text
attestation.task_contract_id/version
== Judgment

attestation.work_run_id
== Judgment

attestation.source_state
== Judgment.source_state

attestation.state_version
== Judgment.state_version

attestation.target_state
== Judgment.target_state

attestation.evidence_authority_revision
== Judgment.evidence_authority_revision

attestation.admitted_ref_root_hash
== Judgment.evidence_root
```

Also require the JudgmentEvaluation's persisted evidence ref equals the same verified ref.

If no evidence ref is present, reject stray non-null:

```text
evidence_authority_revision
evidence_root
```

## 9.3 historical only

Do NOT call:

```text
load_effective_attestation_in_session()
```

here.

A later evidence revocation/staleness or WorkRun advance must not erase historical Judgment issuance.

Current `JudgmentTransitionParticipant.prepare()` remains responsible for current evidence effectiveness.

---

# 10. Judgment corruption proofs

Fresh PostgreSQL proofs:

```text
Judgment requires evidence but evidence ref is null
→ fail closed

evidence ref points to missing attestation
→ fail closed

attestation corrupt anywhere in the canonical historical P1-6 chain
→ Judgment historical replay fails closed

Judgment evidence authority revision differs
→ fail closed

Judgment evidence root differs
→ fail closed

Judgment Task/run/state/version/target differs from attestation
→ fail closed
```

Positive separation:

```text
valid evidence-bound Judgment

later evidence authority invalidated
→ exact historical Judgment replay still succeeds

current G_JUDGMENT_* use
→ denied if current evidence authority is no longer effective
```

---

# 11. preserve previous closures

Fresh regression must keep:

```text
1530:
Candidate/request/evaluation/ADMITTED decision/final admitted issuance

1447:
canonical checkpoint/set/subset/result/admitted roots

1346:
owner-backed G_HUMAN_REQUIRED + full WorkRun history

1241:
P1-4 opening transition root

1142:
gate/Judgment correction graph

0225:
direct historical Human/Judgment provenance

0148:
global identity/time/idempotency

0051:
cross-scope/policy/COMMAND_CENTER/expiry
```

No accepted design changes.

---

# 12. expected source scope

Likely:

```text
src/aiscc/evidence/repository.py
src/aiscc/human/repository.py
src/aiscc/judgment/authority.py

tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
```

Narrow P1-5 persistence helper use is allowed:

```text
src/aiscc/persistence/repository.py
```

only if an owner-side historical immutable-ref verifier should live there.

No migration should normally be required.

If owner-specific producer provenance is not reconstructable from current durable schema:

```text
STOP
→ POLICY_BASELINE_GAP
```

Do not add P1-7 shadow truth.

---

# 13. forbidden

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

P1-6 admission/freshness/reuse semantics changes

P1-7 Human/Judgment design changes

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

P1_6_HISTORICAL_ISSUER_CATEGORY_AUDIT

P1_5_HISTORICAL_PRODUCER_REF

HUMAN_P1_7_HISTORICAL_PRODUCER_REF

PRIOR_ADMITTED_HISTORICAL_REUSE

JUDGMENT_HISTORICAL_EVIDENCE_DEPENDENCY

CORRUPTION_FAIL_CLOSED

HISTORICAL_REPLAY

1530_REGRESSION
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

# 15. mandatory stop

STOP on:

```text
HEAD drift

accepted design SHA drift

predecessor `21 paths / bf3420...` drift

need to change accepted P1-7 design

need to change accepted P1-6 admission semantics

an accepted owner-specific EvidenceIssuerType has no durable historical provenance sufficient to prove its current recognizes() authority

reuse historical provenance cannot be reconstructed from current durable ledger

unrelated dirty collision
```

---

# 16. accept criteria

All must hold:

```text
all exact EvidenceIssuerType categories audited

P1-5 historical Candidate resolves exact immutable P1-5 producer ref

HUMAN_P1_7 historical Candidate resolves valid projection-independent producer + HumanResult provenance

PRIOR_ADMITTED historical Candidate resolves valid prior admission + durable reuse ledger

reuse cycles fail closed

intentional System token categories remain System-owned and statically policy-bound

historical Judgment with evidence consumes projection-independent P1-6 attestation provenance

Judgment evidence root/revision/Task/run/state/version/target exact

historical replay does not require current evidence/producer effectiveness

current guard use remains separately fail-closed when stale

1530/1447/1346/1241/1142/0225/0148/0051 regressions PASS

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
4. predecessor `21 paths / bf3420...` verification
5. 1627 HOLD Cycle placement
6. exact EvidenceIssuerType audit table
7. P1-5 historical producer verifier/API
8. P1-5 category→ref-kind mapping
9. HUMAN_P1_7 historical producer verifier/API
10. HUMAN_P1_7 → historical HumanResult relation
11. PRIOR_ADMITTED historical chain
12. reuse-consumption ledger proof
13. reuse cycle detection
14. System token historical boundary
15. Judgment historical evidence-attestation verification
16. missing/corrupt P1-5 producer proofs
17. missing/corrupt HUMAN_P1_7 producer proofs
18. prior/reuse-ledger corruption proofs
19. Judgment missing/corrupt evidence proofs
20. non-current-but-valid producer/evidence historical replay
21. current guard stale rejection
22. 1530 regression
23. 1447 regression
24. 1346 regression
25. 1241 regression
26. 1142 regression
27. 0225 regression
28. 0148 regression
29. 0051 regression
30. P1-4 regression
31. P1-6 regression
32. PostgreSQL/version/test counts
33. final runtime path count / aggregate SHA
34. provider/network/credential actions
35. P1-8 = NOT_STARTED
36. Git actions = none
37. human verification = HUMAN_PENDING
38. preserved exact paths
39. next recommendation

---

# 18. export

Target:

```text
.aiassistant/reports/target/
20260830_1627_aiscc-p1-7-historical-producer-and-judgment-evidence-authority-runtime-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include all changed runtime/test paths plus the 1627 HOLD Cycle.

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
20260830_1627_aiscc-p1-7-historical-producer-and-judgment-evidence-authority-runtime-rework-1.md
```

Finish:

```text
.aiassistant/tasks/done/
20260830_1627_aiscc-p1-7-historical-producer-and-judgment-evidence-authority-runtime-rework-1.md
```

No Git add/commit/push.

Expected final HEAD:

```text
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

---

# 20. preserved exact paths

Must preserve all existing accepted/HOLD lineage and additionally:

```text
.aiassistant/records/aiscc/cycles/
20260830_1627_aiscc-p1-7-historical-producer-and-judgment-evidence-authority-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_1627_aiscc-p1-7-historical-producer-and-judgment-evidence-authority-runtime-rework-1.md
```

Canonical state files remain preserved and unchanged.

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
