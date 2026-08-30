# AISCC Cycle Record

## meta

- cycle_id: `20260830_1627_aiscc-p1-7-historical-producer-and-judgment-evidence-authority-hold-1`
- date: `2026-08-30T16:27:00+09:00`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT / P1-6_EVIDENCE_PROVENANCE_CONSUMER`
- affected_areas: `historical EvidenceCandidate producer authority / Judgment historical evidence dependency`
- work_type: `P1_7_RUNTIME_REWORK_REVIEW`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-runtime-rework-1`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `TRANSITIVE_PRODUCER_AND_JUDGMENT_EVIDENCE_PROVENANCE_INCOMPLETE`
- cycle_record_action: `create`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260830_1627_aiscc-p1-7-historical-producer-and-judgment-evidence-authority-hold-1.cycle.md`

## repository snapshot

- expected current HEAD: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- P1-7 accepted design commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- P1-7 design terminal commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted design SHA-256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- reviewed predecessor runtime path count: `21`
- reviewed predecessor runtime aggregate SHA-256:
  `bf3420c989694b97edce5e398420e01cd8be0c4580760fd63c2b6068c0db5b69`
- Stage 1 runtime commit: `none`

## predecessor 1530 review result

1530 successfully closes its direct issuance-chain findings.

Accepted as closed:

```text
historical AdmittedEvidence
→ exact EvidenceCandidateRow
→ canonical candidate fingerprint
→ CLOSED

historical AdmissionRequest
→ exact candidate/requirement/set/checkpoint/run/state/use
→ canonical make_admission_request() fingerprint
→ CLOSED

historical EvidenceEvaluation
→ exact dimension set / accepted positive vocabulary / authority-ref shape
→ CLOSED

historical EvidenceAdmissionDecision
→ exact request/evaluation
→ ADMITTED
→ accepted P1-6 authority
→ CLOSED

final AdmittedEvidence
→ candidate/request/decision/content/coverage/time
→ CLOSED

REJECTED-decision-backed admitted row
→ fail closed
→ CLOSED
```

Executor evidence admitted:

```text
focused issuance:
1 PASS

targeted P1-4/P1-6/P1-7:
26 PASS

full unit + integration:
163 PASS

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
21

manifest SHA ↔ actual exported bytes:
21/21 MATCH

aggregate SHA-256:
bf3420c989694b97edce5e398420e01cd8be0c4580760fd63c2b6068c0db5b69
```

---

# finding 1 — owner-specific historical EvidenceCandidate producer authority still stops at the Candidate row

`_historical_candidate_from_row()` now correctly verifies the complete immutable Candidate row and canonical
candidate fingerprint.

For `HUMAN_DIRECT_EVIDENCE`, it also verifies the durable Human direct ingress record.

For the other accepted owner-specific producer categories, historical verification currently does not follow
`producer_attestation_ref` / `prior_admitted_evidence_ref` to the durable producer authority that the current
P1-6 admission path requires.

Current owner-specific issuers include exact equivalents of:

```text
P1_5_EXECUTION_SUBMISSION
P1_5_AGENT_OUTPUT
P1_5_TOOL_OUTPUT
P1_5_EXECUTION_ARTIFACT

HUMAN_P1_7

PRIOR_ADMITTED_EVIDENCE
```

Current admission does not accept those categories from a bare Candidate:

```text
P1_5EvidenceIssuerAuthority.recognizes()
→ resolves exact immutable P1-5 output ref

P1_7HumanEvidenceIssuerAuthority.recognizes()
→ resolves exact durable HumanP1_7EvidenceProducerRef

PriorAdmittedEvidenceIssuerAuthority.recognizes()
→ resolves exact prior admitted evidence
```

Historical admission provenance should not weaken that owner boundary.

Required invariant:

```text
durable Candidate self-fingerprint
+ persisted ISSUER_AUTHORITY = PASS
!= owner-specific producer authority provenance
```

A raw `producer_attestation_ref` string must not become trusted historical producer authority merely because
the Candidate and Evaluation rows agree.

---

# finding 1A — P1-5 immutable producer refs

`PostgresEvidenceRepository.verify()` already defines the current P1-5 immutable-ref boundary using:

```text
ExecutionOutputRefRow
ExecutionAttemptRow

ref_id
expected ref kind
execution_attempt_id
WorkRun
content_hash
private:// storage ref
```

Historical verification should consume an in-session / projection-independent equivalent.

For a P1-5 candidate require:

```text
producer_attestation_ref
→ exact ExecutionOutputRefRow.output_ref_id

row.execution_attempt_id == candidate.execution_attempt_id

ExecutionAttemptRow exists
attempt.work_run_id == candidate.producer_work_run_id

row.ref_kind == exact issuer-category kind:
ExecutionSubmissionRef
AgentOutputRef
ToolOutputRef
ExecutionArtifactRef

row.content_hash == candidate.content_ref.content_hash

row.storage_ref satisfies accepted immutable private-ref contract

candidate issuer id/version/authority_ref match the exact accepted P1-5 issuer authority

historical Evaluation ISSUER_AUTHORITY dimension
→ points to that exact accepted issuer authority
```

Do not require the execution attempt or WorkRun to remain current now.

If current P1-5 owner exposes a stronger canonical immutable-ref verifier, reuse it rather than duplicating a
weaker check in P1-7.

---

# finding 1B — HUMAN_P1_7 producer ref needs a historical verifier

Current `PostgresHumanAuthorityRepository.load_producer_ref()` is a current-effectiveness loader. It requires
the HumanGate projection still to point at the same HumanResult/revision.

That is correct for current admission, but it cannot be the criterion for historical replay after the gate,
result, or WorkRun has advanced.

Create/reuse a projection-independent verifier equivalent to:

```text
_verify_human_p1_7_producer_historical_provenance_in_session(...)
```

Verify at minimum:

```text
HumanP1_7EvidenceProducerRow exists by serialized ref

row fingerprint
== canonical _producer_fingerprint(reconstructed producer)

row.work_run_id / issued_at / payload exact

producer authority id/version
== accepted P1-7 Human evidence producer authority

producer TaskContract id/version
producer WorkRun
source state/version
HumanGate ref/revision
HumanResult ref/revision
checkpoint ref
evidence type id/version
subject/scope/resource
content hash
sensitivity
export policy
```

Then resolve the referenced historical HumanResult through the already accepted:

```text
_verify_human_result_historical_provenance_in_session(...)
```

and require exact immutable producer ↔ result/gate bindings.

Do NOT require:

```text
current HumanGate projection
current result
current WorkRun state/version
current gate expiry
```

Historical producer issuance remains valid even if current authority later changed.

---

# finding 1C — PRIOR_ADMITTED_EVIDENCE requires historical reuse provenance

For a historical candidate with:

```text
issuer.owner_type = PRIOR_ADMITTED_EVIDENCE
prior_admitted_evidence_ref != None
```

prove:

```text
prior ref is a valid historical AdmittedEvidence issuance
```

using the same P1-6 historical admitted-evidence verifier.

Do not use current `load_admitted()` because later revocation/supersession must not erase valid historical
issuance.

Also verify the current admitted evidence's durable reuse ledger:

```text
exact one EvidenceReuseConsumptionRow
for current admitted_evidence_id

prior_admitted_evidence_ref == candidate.prior ref

requirement_ref / work_run_id / checkpoint_ref
== current admission request

policy_maximum
== immutable EvidenceRequirement.reuse_maximum

consumption_ordinal > 0
and within the accepted maximum

consumed_at == current admitted.admitted_at
```

For all ledger rows in the exact reuse scope, verify ordinal uniqueness/contiguity according to the accepted
P1-6 durable reuse-consumption contract.

Historical reuse chains must have cycle detection:

```text
A prior→B
B prior→A
or longer cycle
→ AUTHORITY_CONFLICT
```

Do not re-evaluate current reuse availability.

---

# finding 1D — generic/System issuer categories

Do not invent durable producer objects where the accepted P1-6 issuer is intentionally a System-owned
`TokenEvidenceIssuer` with no separate durable producer row.

For such categories the historical System admission Evaluation/Decision remains the durable System statement,
but the verifier must still enforce static immutable policy relationships that are reconstructable:

```text
candidate issuer type/id
is allowed by the exact immutable EvidenceRequirement

candidate issuer authority_ref
has the exact accepted issuer-id/version form

candidate content kind/type/sensitivity/subject/resource bindings
remain consistent with immutable requirement/candidate/request data
```

If any accepted System issuer category actually requires a durable owner-specific producer ref that is not
represented in the current historical verifier:

```text
STOP
→ POLICY_BASELINE_GAP
```

Do not silently downgrade it to token/string authority.

---

# finding 2 — historical Judgment provenance does not verify `evidence_attestation_ref`

Current Judgment issuance correctly does:

```text
load_effective_attestation_in_session(...)
```

when `evidence_attestation_ref` is supplied and enforces exact TaskContract/WorkRun/state/version/target
bindings.

Current transition-time `G_JUDGMENT_*` use also revalidates current evidence authority.

However `_verify_judgment_base_issuance_provenance_in_session()` currently verifies only:

```text
Judgment.evidence_attestation_ref
== JudgmentEvaluation.payload.evidence_attestation_ref
```

It does not prove that the historical evidence attestation itself existed and was validly issued by P1-6.

Therefore a self-consistent historical Judgment row/evaluation can retain an arbitrary or corrupted
`evidence_attestation_ref` without the historical Judgment verifier consuming the P1-6 provenance graph.

Required:

```text
historical Judgment evidence ref string
!= historical P1-6 evidence authority
```

---

# finding 2A — projection-independent historical Judgment evidence dependency

Inside Judgment base issuance verification:

If:

```text
value.evidence_attestation_ref is not None
```

consume:

```text
verify_historical_set_attestation_provenance(
    session,
    value.evidence_attestation_ref,
)
```

and require exact immutable match:

```text
TaskContract id/version
work_run_id
source state/version
target state
evidence authority revision
admitted_ref_root_hash
```

against the Judgment fields:

```text
value.evidence_authority_revision
value.evidence_root
```

and the Judgment request/use represented by the Judgment.

If policy:

```text
requires_post_human_evidence == true
```

then historical Judgment issuance requires the evidence attestation.

If evidence is present even when optional under the policy, it still must be historically valid.

Do NOT require the attestation to be current/effective now.

---

# finding 2B — historical-vs-current Judgment separation remains

Required behavior:

```text
valid Judgment issued with valid P1-6 evidence attestation

later:
P1-6 attestation/evidence becomes stale/revoked/superseded
or WorkRun advances

same immutable Judgment proposal replay
→ historical Judgment still verifies and returns

but

current G_JUDGMENT_* use
→ still denied when current evidence/policy/state authority is stale
```

Do not call `load_effective_attestation_in_session()` from the historical Judgment verifier.

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
- 1447 findings: `CLOSED`
- 1530 direct findings: `CLOSED`
- P1-7 Runtime: `REWORK_REQUIRED / HUMAN_PENDING`
- P1-8: `NOT_STARTED`
- PUBLIC_BOUNDED_LIVE: `NOT_RELEASED`
- Stage 1 runtime commit: `none`
- required rework:
  1. owner-specific historical EvidenceCandidate producer authority;
  2. P1-5 immutable producer refs;
  3. projection-independent HUMAN_P1_7 producer provenance;
  4. PRIOR_ADMITTED_EVIDENCE historical reuse chain/ledger;
  5. historical Judgment → P1-6 evidence-attestation dependency.
- terminal_decision_reason:
  `1530 proves the System admission chain to each Candidate and AdmittedEvidence, but owner-specific producer refs are still trusted as Candidate fields, and historical Judgment replay does not consume the P1-6 evidence authority it records.`

## preservation

Do not amend/revert:

```text
238b0b41460c2504fd3244eadb06809d8692a60f
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

Preserve all accepted/HOLD lineage plus:

```text
.aiassistant/records/aiscc/cycles/
20260830_1530_aiscc-p1-7-p1-6-historical-admitted-evidence-issuance-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_1627_aiscc-p1-7-historical-producer-and-judgment-evidence-authority-hold-1.cycle.md
```

## next action

```text
P1-7 narrow historical producer/Judgment-evidence authority rework
→ Command Center runtime re-review
→ Human final P1-7 runtime review only after PASS

P1-8:
NOT_STARTED
```
