# AISCC Cycle Record

## meta

- cycle_id: `20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-hold-1`
- date: `2026-08-30T02:25:00+09:00`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT`
- affected_areas: `HumanResult / Judgment / immutable replay / append-only provenance / fail-closed restart`
- work_type: `P1_7_RUNTIME_REWORK_REVIEW`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260830_0148_aiscc-p1-7-global-identity-idempotency-and-expiry-toctou-runtime-rework-1`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `HISTORICAL_PROVENANCE_NOT_REVALIDATED`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-hold-1.cycle.md`

## repository snapshot

- expected current HEAD: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- P1-7 design acceptance commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- P1-7 design terminal governance commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted design SHA-256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- predecessor runtime candidate path count: `19`
- predecessor runtime candidate aggregate SHA-256:
  `678c0981defc31c6c1351da509838a42e19e22ba2abe287bb30b7d2a7e9713fd`
- Stage 1 commit: `none`

## predecessor 0148 findings — review result

The 0148 rework materially closes all five findings that motivated it.

Accepted as closed:

```text
expiry authority time sampled only after canonical WorkRun/gate lock
→ CLOSED

global HumanResult immutable ID serialization
→ CLOSED

global Judgment immutable ID serialization
→ CLOSED

HumanResult omitted-submitted_at proposal idempotency
→ CLOSED

Judgment historical immutable replay before current-effectiveness checks
→ CLOSED for identity/current-authority separation
```

Fresh implementation properties confirmed from exported source:

```text
HumanResult lock order:
WorkRun lock
→ global HumanResult-ID advisory lock
→ existing identity
→ current rows for new authority only

Judgment lock order:
WorkRun lock
→ global Judgment-ID advisory lock
→ existing identity
→ current WorkRun/policy/Human/evidence authority for new object only

action/result expiry authority:
server clock sampled after canonical lock/current rows

HumanResult proposal identity:
caller/request immutable inputs
+ explicit null marker when submitted_at omitted
!= server admitted_at/current time

Judgment same-proposal replay:
returns historical immutable row before current policy/state effectiveness checks

current G_JUDGMENT_* use:
still revalidates current WorkRun/policy/Human/evidence/expiry authority
```

Fresh Executor evidence admitted:

```text
P1-7 focused:
4 PASS

P1-4/P1-6 direct regression:
23 PASS

full local suite:
182 PASS

ruff:
PASS

mypy src:
PASS / 67 source files

PostgreSQL:
17.6

Alembic:
20260829_0004 head

provider/network/credential/deployment:
0

P1-8:
NOT_STARTED

Git Stage 1 commit:
none
```

Export provenance independently verified by Command Center:

```text
runtime paths:
19

all manifest SHA:
actual copied bytes match

aggregate:
678c0981defc31c6c1351da509838a42e19e22ba2abe287bb30b7d2a7e9713fd
```

---

# load-bearing finding — immutable historical replay does not verify its own durable provenance lineage

Accepted P1-7 persistence semantics require:

```text
PostgreSQL
append-only provenance
deterministic restart reconstruction

corrupt/incomplete provenance
→ fail closed
→ no auto repair
```

The new immutable replay semantics correctly separate:

```text
historical immutable identity
!= current guard effectiveness
```

but the historical identity path currently validates too little durable authority provenance.

## FINDING-1 — HumanResult replay checks row fingerprint only

Current `PostgresHumanAuthorityRepository.submit_result()`:

```text
WorkRun lock
→ HumanResult-ID lock
→ existing HumanResultRow

if same proposal_fingerprint:
    reconstruct HumanResult
    verify human_result_fingerprint
    return durable
```

This path does not verify that the historical result is backed by the accepted append-only authority lineage:

```text
exact HumanResultAuthorityEventRow ADMITTED event
prior_revision = 0
new_revision = 1
event belongs to this HumanResult
event/gate binding is consistent

HumanResultRow.human_gate_id
→ existing HumanGateRow
→ result.human_gate_ref matches

durable result proposal fingerprint format/integrity
```

`_verify_gate_consistency_in_session()` verifies HumanResult event lineage when the result is the gate projection's **current** result, but an immutable replay intentionally must also work after the gate/result is no longer current.

Therefore a historical replay cannot rely on the current gate projection as its provenance verifier.

Current behavior can return an apparently valid historical `HumanResult` row even if its required ADMITTED event/gate lineage is incomplete.

Required:

```text
row fingerprint
!= complete HumanResult authority provenance
```

## FINDING-2 — Judgment replay checks row fingerprint only

Current `PostgresJudgmentAuthority.issue()` existing-object path:

```text
WorkRun lock
→ Judgment-ID lock
→ existing JudgmentRow

same proposal_fingerprint
→ reconstruct Judgment
→ verify Judgment fingerprint
→ return durable
```

It intentionally skips current WorkRun/policy/evidence effectiveness, which is correct.

However it also skips immutable historical provenance validation such as:

```text
JudgmentEvaluationRow referenced by Judgment.evaluation_ref exists
evaluation belongs to the exact WorkRun/state/version and completed issuance

exact one ISSUED JudgmentAuthorityEventRow exists
event revisions match Judgment.authority_revision
event evaluation_ref matches Judgment.evaluation_ref

policy snapshot referenced by Judgment exists and matches the immutable Judgment fields

HUMAN-owned historical Judgment:
referenced HumanResult/gate immutable identity exists and matches

COMMAND_CENTER-owned historical Judgment:
referenced Command Center action immutable identity exists and matches

supersedes_judgment_ref:
predecessor exists
and accepted correction/supersession relation is structurally complete
```

`_verify_judgment_consistency_in_session()` performs much of this for the **current projection**.

A superseded/historical Judgment is deliberately not the current projection, so the existing immutable replay path needs a projection-independent immutable provenance verifier.

Required:

```text
historical replay
→ does not require current authority

but

historical replay
→ still requires complete immutable issuance provenance
```

## consequence

Without this distinction:

```text
corrupt/incomplete historical row
+ correct self-hash
→ may be returned as System historical truth
```

That conflicts with the accepted fail-closed persistence/restart contract.

This is independent of whether the object can still satisfy `G_HUMAN_*` or `G_JUDGMENT_*`.

---

# command-center judgment

- result_status: `HOLD_REWORK_REQUIRED`
- P1-7 Design: `REMAINS ACCEPTED / CLOSED`
- Stage 0A/0B commits: `PRESERVE`
- 0051 findings: `CLOSED`
- 0148 findings: `CLOSED`
- P1-7 Runtime: `REWORK_REQUIRED / HUMAN_PENDING`
- P1-8: `NOT_STARTED`
- PUBLIC_BOUNDED_LIVE: `NOT_RELEASED`
- Stage 1 runtime commit: `none`
- required_rework:
  1. projection-independent immutable HumanResult historical provenance verification;
  2. projection-independent immutable Judgment historical provenance verification;
  3. same-proposal replay must fail closed on incomplete/corrupt immutable provenance;
  4. current-authority checks must remain separate and must not be reintroduced into historical replay.
- terminal_decision_reason: idempotent historical replay now has the correct identity semantics, but it treats a self-consistent row as sufficient historical authority even when the append-only issuance provenance required to justify that row is missing or inconsistent.

## preserved artifacts

Do not amend/revert:

```text
238b0b41460c2504fd3244eadb06809d8692a60f
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
```

Preserve:

```text
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md

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
```

## next action

```text
P1-7 narrow historical-provenance runtime rework
→ Command Center re-review
→ Human final P1-7 runtime review only after PASS

P1-8:
NOT_STARTED
```
