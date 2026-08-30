# AISCC Cycle Record

## meta

- cycle_id: `20260830_1346_aiscc-p1-7-owner-backed-guard-and-full-workrun-history-provenance-hold-1`
- date: `2026-08-30T13:46:00+09:00`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT / P1-4_TRANSITION_PROVENANCE_CONSUMER`
- affected_areas: `G_HUMAN_REQUIRED historical authority / full WorkRun admitted history integrity`
- work_type: `P1_7_RUNTIME_REWORK_REVIEW`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-runtime-rework-1`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `OWNER_BACKED_GUARD_AND_FULL_HISTORY_PROVENANCE_INCOMPLETE`
- cycle_record_action: `create`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260830_1346_aiscc-p1-7-owner-backed-guard-and-full-workrun-history-provenance-hold-1.cycle.md`

## repository snapshot

- expected current HEAD: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- P1-7 design acceptance commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- P1-7 design terminal governance commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted design SHA-256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- reviewed predecessor runtime path count: `20`
- reviewed predecessor runtime aggregate SHA-256:
  `5007f8d9c417be39efdfcea522e910846b8e830d53d88cda2340ddb87d19ed9c`
- Stage 1 runtime commit: `none`

## predecessor 1241 review result

1241 successfully closes the direct P1-4 opening-transition root requirements that motivated it.

Accepted as closed:

```text
canonical P1-4 historical transition verifier introduced
→ CLOSED

selected TransitionRequest request_fingerprint reconstruction
→ CLOSED

selected Evaluation exact TransitionMatrix guard IDs/owners/bound refs
→ CLOSED

selected ADMITTED Decision owner/kernel/resulting state/version
→ CLOSED

selected transition membership in contiguous admitted WorkRun history
→ CLOSED

HumanGate normal opening consumes the P1-4 verifier
→ CLOSED
```

Executor evidence admitted:

```text
ruff:
PASS

mypy src:
PASS / 67 source files

focused PostgreSQL:
2 PASS

P1-4 + P1-7 PostgreSQL:
20 PASS

P1-6 PostgreSQL:
6 PASS

unit:
98 PASS

full unit + integration:
163 PASS

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
5007f8d9c417be39efdfcea522e910846b8e830d53d88cda2340ddb87d19ed9c
```

---

# load-bearing finding 1 — historical G_HUMAN_REQUIRED is structurally reconstructed but not owner-backed

Current P1-4 historical reconstruction in:

```text
src/aiscc/persistence/repository.py
_historical_evaluation_from_row(...)
```

correctly validates:

```text
exact GuardId set
exact GuardSemanticOwner
satisfied flag
reason shape
non-empty authority_ref
exact request-bound refs
```

It then reconstructs a `TrustedGuardFact` with an internal historical reconstruction token.

For:

```text
G_HUMAN_REQUIRED
owner = P1_7_HUMAN
```

the code does **not** resolve the persisted:

```text
authority_ref
```

to the exact durable:

```text
HumanGuardAttestationRow
```

and does not prove that the attestation row itself is immutable, self-consistent, and bound to the opening request.

Therefore an otherwise locally coherent durable Evaluation can contain:

```text
guard_id = G_HUMAN_REQUIRED
semantic_owner = P1_7_HUMAN
satisfied = true
authority_ref = arbitrary non-empty string
bound_refs = exact expected tuple
```

and still be reconstructed as historical trusted guard input if the request fingerprint is changed coherently.

Required invariant:

```text
correct owner name + non-empty authority_ref
!= owner-backed historical guard authority
```

For the normal HumanGate opening path, the historical `G_HUMAN_REQUIRED` must be proven by the exact persisted P1-7 Human guard attestation that was admitted in the same transition transaction.

## minimum immutable attestation checks

For the opening transition's `G_HUMAN_REQUIRED` observation:

```text
authority_ref
→ exact HumanGuardAttestationRow.serialized_ref

row exists exactly once

row.guard_id == G_HUMAN_REQUIRED
row.work_run_id == request.work_run_id
row.state_version == request.observed_state_version

row fingerprint is valid and reconstructable from row payload

payload TaskContract id/version == request
payload work_run_id == request
payload source state/version == request
payload target state == HUMAN_REQUIRED
payload target-use fingerprint == exact request target-use
payload human_gate_ref == opening HumanGate ref
payload purpose id/version == accepted HumanGate purpose
payload P1-7 authority id/version/revision == accepted values

Evaluation observation:
authority_ref == attestation.serialized_ref
semantic_owner == P1_7_HUMAN
satisfied == true
bound_refs == exact accepted bound refs
```

The historical verifier must not use process-local issuer tokens as durable proof.

---

# load-bearing finding 2 — PRE_HUMAN evidence binding inside G_HUMAN_REQUIRED must be historically immutable, not current

The accepted P1-7 design freezes:

```text
current effective PRE_HUMAN P1-6 attestation
→ mandatory owner-backed input to G_HUMAN_REQUIRED at gate-open time
```

For historical replay, current P1-6 effectiveness must not be required after the WorkRun has advanced.

But the persisted `HumanGuardAttestationRow` must prove that the `G_HUMAN_REQUIRED` attestation actually carried the exact immutable PRE_HUMAN binding admitted at gate-open time.

At minimum verify from the persisted Human guard payload:

```text
pre_human_evidence exists

attestation ref/version
checkpoint ref/version/fingerprint
TaskContract id/version
work_run_id
source state/version
target state / transition-purpose
RequirementSet id/version/full root
applicable subset root
admitted-ref root
P1-6 authority id/version/revision
satisfied = true
```

and that the referenced durable P1-6 `EvidenceSetAttestationRow` exists and its immutable row/payload fields match those exact bound values.

Required:

```text
historical P1-6 immutable issuance/binding
!= current P1-6 effectiveness
```

Do not call `load_effective_attestation()` as the historical criterion, because a valid historical opening must remain replayable after later state/version or evidence-authority changes.

A narrow projection-independent P1-6 immutable attestation validator may be added/reused if required.

Do not re-evaluate evidence requirements in P1-7.

---

# load-bearing finding 3 — complete WorkRun consistency validates state/version lineage but not every admitted request's full run identity / step integrity

Current:

```text
PostgresExecutionRepository._verify_consistency_in_session(...)
```

with an existing WorkRun projection joins:

```text
TransitionDecisionRow
TransitionEvaluationRow
TransitionRequestRow
```

but reconstructs only:

```text
authoritative state/version
resulting state/version
event order
final projection state/version
```

It does not currently validate every admitted historical request's:

```text
project_id
TaskContract id/version
runtime_mode
request fingerprint
exact matrix guard set/owners
decision owner/kernel
```

against the WorkRun identity.

The selected 1241 opening transition is validated in detail separately, but other admitted steps in the same history are not.

Therefore a corrupt prior/future admitted step can remain state/version-contiguous while carrying a foreign:

```text
project_id
TaskContract version
runtime_mode
```

or an invalid request/evaluation/decision integrity, and the whole history may still reconstruct to the projection.

Required invariant:

```text
state/version-contiguous history
!= canonical complete WorkRun authority history
```

## required closure

Refactor P1-4 historical verification so the canonical WorkRun consistency path validates every admitted step through a shared per-step immutable verifier, or an exact equivalent.

Each admitted step must prove:

```text
request work_run_id == WorkRunRow.work_run_id
request project_id == WorkRunRow.project_id
request TaskContract id/version == WorkRunRow
request runtime_mode == WorkRunRow

request fingerprint exact

exact TransitionMatrix guard set / owners / bound refs
all required guards satisfied
missing_guards empty for ADMITTED

decision request/evaluation relation exact
decision owner/kernel exact
resulting state/version exact
```

Then the contiguous state/version reconstruction is performed.

Avoid recursive verifier calls.

Recommended structure:

```text
_verify_historical_transition_step_in_session(...)
→ one immutable P1-4 step, no whole-history recursion

_verify_consistency_in_session(...)
→ iterate admitted steps
→ validate run identity + per-step integrity
→ reconstruct contiguous history
→ compare durable WorkRun projection

verify_historical_transition_provenance(...)
→ consume the canonical per-step + whole-history result
```

---

# concrete corruption classes currently needing proof

Fresh negative proof must cover:

```text
G_HUMAN_REQUIRED observation
with arbitrary authority_ref
+ coherently recomputed request fingerprint
→ fail closed

G_HUMAN_REQUIRED authority_ref
points to missing HumanGuardAttestationRow
→ fail closed

attestation row exists but fingerprint/payload Task/run/state/target/gate binding is corrupt
→ fail closed

attestation PRE_HUMAN binding points to missing/mismatched P1-6 attestation row
→ fail closed

historical P1-6 attestation is no longer current after WorkRun advances
but immutable provenance is valid
→ historical HumanGate/HumanResult replay still succeeds

another admitted step in same WorkRun
with foreign TaskContract/project/runtime identity
while state/version remains contiguous
→ complete WorkRun history fails closed

another admitted step with corrupt request fingerprint or guard matrix
while selected HumanGate opening row itself is untouched
→ complete WorkRun history fails closed
```

---

# command-center judgment

- result_status: `HOLD_REWORK_REQUIRED`
- P1-7 Design: `REMAINS ACCEPTED / CLOSED`
- Stage 0A/0B commits: `PRESERVE`
- 0051 findings: `CLOSED`
- 0148 findings: `CLOSED`
- 0225 findings: `CLOSED`
- 1142 findings: `CLOSED`
- 1241 direct findings: `CLOSED`
- P1-7 Runtime: `REWORK_REQUIRED / HUMAN_PENDING`
- P1-8: `NOT_STARTED`
- PUBLIC_BOUNDED_LIVE: `NOT_RELEASED`
- Stage 1 runtime commit: `none`
- required rework:
  1. historical G_HUMAN_REQUIRED must resolve exact durable P1-7 attestation;
  2. immutable PRE_HUMAN P1-6 binding must be verified without current-effectiveness dependence;
  3. full WorkRun admitted history must validate every step's immutable/run identity, not only state/version continuity.
- terminal_decision_reason:
  `1241 now proves the selected opening transition structurally and as a contiguous history member, but future-owner guard authority remains a string-level historical assertion and the surrounding admitted history is not yet integrity-checked step-by-step.`

## preserved artifacts

Do not amend/revert:

```text
238b0b41460c2504fd3244eadb06809d8692a60f
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

Preserve all prior P1-7 terminal/HOLD lineage plus:

```text
.aiassistant/records/aiscc/cycles/
20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_1346_aiscc-p1-7-owner-backed-guard-and-full-workrun-history-provenance-hold-1.cycle.md
```

## next action

```text
P1-7 narrow owner-backed historical guard + complete WorkRun history rework
→ Command Center runtime re-review
→ Human final P1-7 runtime review only after PASS

P1-8:
NOT_STARTED
```
