# AISCC Cycle Record

## meta

- cycle_id: `20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-hold-1`
- date: `2026-08-30T11:42:00+09:00`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT`
- affected_areas: `HumanGate / HumanResult / Judgment correction / historical provenance graph`
- work_type: `P1_7_RUNTIME_REWORK_REVIEW`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-runtime-rework-1`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `TRANSITIVE_HISTORICAL_AUTHORITY_PROVENANCE_INCOMPLETE`
- cycle_record_action: `create`
- source_mirror_sync: `not-required`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-hold-1.cycle.md`

## repository snapshot

- expected current HEAD: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- P1-7 design acceptance commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- P1-7 design terminal governance commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted design SHA-256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- predecessor runtime candidate path count: `19`
- predecessor runtime candidate aggregate SHA-256:
  `36823a442e1b4e9eaa72b270f36d3686c500dc23fdea8c0765ccd56c103ab82b`
- Stage 1 commit: `none`

## predecessor 0225 findings — review result

The 0225 rework materially closes its direct findings.

Accepted as closed:

```text
projection-independent HumanResult ADMITTED / RESOLVED provenance
→ CLOSED

projection-independent Judgment Evaluation / ISSUED / policy provenance
→ CLOSED

HUMAN Judgment dependency on historical HumanResult
→ CLOSED at the HumanResult verifier boundary

COMMAND_CENTER Judgment immutable action dependency
→ CLOSED

same-proposal historical replay/current-effectiveness separation
→ CLOSED

corrupt/missing row-level issuance provenance
→ fail closed
```

Executor evidence admitted:

```text
P1-7 focused:
4 PASS

P1-4/P1-6 direct regression:
23 PASS

unit regression:
98 PASS

ruff:
PASS

mypy src:
PASS / 67 source files

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

Export provenance independently verified:

```text
runtime paths:
19

manifest SHA:
19/19 match actual exported bytes

aggregate SHA-256:
36823a442e1b4e9eaa72b270f36d3686c500dc23fdea8c0765ccd56c103ab82b
```

---

# load-bearing finding 1 — HumanResult historical provenance does not prove the referenced HumanGate was validly System-created

`_verify_human_result_historical_provenance_in_session()` now correctly verifies:

```text
HumanResult row self-fingerprint
proposal fingerprint format
HumanGate row existence
result ↔ gate TaskContract/work_run/purpose relation
one ADMITTED result event
one matching RESOLVED gate event
revision/timestamp relation
```

However, it does not verify the immutable issuance provenance of the referenced `HumanGate` itself.

Missing historical-gate checks include exact equivalents of:

```text
HumanGateRow gate_fingerprint recomputation / immutable row integrity

HumanGateRow opened_from_state / opened_from_state_version / bound_state_version
coherence with its opening authority

exact initial OPENED or OPENED_CORRECTION event

initial event revision:
0 → 1

initial event bound state/version

for normal OPENED:
opening TransitionRequest exists
opening TransitionDecision exists
request/decision IDs match HumanGateRow payload
decision belongs to request/evaluation
decision outcome = ADMITTED
decision resulting state = HUMAN_REQUIRED
decision resulting state version = gate bound_state_version
TaskContract/work_run/source state/version match gate

for OPENED_CORRECTION:
exact supersedes_gate_ref exists
predecessor gate has coherent SUPERSEDED event pointing to replacement
correction source/target authority is exact HUMAN_REQUIRED epoch
```

Current historical HumanResult verification can therefore accept an internally self-consistent:

```text
HumanGateRow
+ RESOLVED event
+ HumanResult ADMITTED event
```

without proving that the gate ever originated from the accepted P1-4/P1-7 System gate-open authority path.

Required invariant:

```text
HumanGateRow existence
!= System-owned HumanGate issuance provenance

RESOLVED event
!= proof of valid OPENED / OPENED_CORRECTION authority
```

This is especially load-bearing because `HumanResult` authenticity depends on the gate being System-owned.

### judgment

```text
HUMAN_RESULT_HISTORICAL_PROVENANCE:
PARTIAL / REWORK_REQUIRED

HUMAN_GATE_AUTHORITY:
historical transitive provenance incomplete
```

---

# load-bearing finding 2 — Judgment correction/supersession counterpart lineage is only self-hash validated

`_verify_judgment_historical_provenance_in_session()` correctly verifies the current historical Judgment's:

```text
row fingerprint
Evaluation
ISSUED event
policy snapshot
HUMAN / COMMAND_CENTER / SYSTEM_DETERMINISTIC dependency
```

For correction relations, however:

## when current Judgment supersedes a predecessor

The verifier loads the predecessor and checks:

```text
predecessor self-fingerprint
same Task/run/state/target
revision relation
one predecessor SUPERSEDED event
replacement ref
timestamp
```

but does not prove that the predecessor itself has complete immutable issuance provenance:

```text
its Evaluation
its ISSUED event
its policy/Human/CommandCenter dependency
```

## when current historical Judgment has later been superseded

The verifier loads the replacement and checks:

```text
replacement self-fingerprint
replacement.supersedes_ref
same WorkRun
revision relation
SUPERSEDED relation/timestamp
```

but does not prove that the replacement itself was validly issued.

Therefore a self-hash-consistent but never-validly-issued predecessor/replacement can participate in a correction chain.

Required:

```text
self-hash-valid Judgment counterpart
!= valid immutable Judgment authority

SUPERSEDED relation
must connect two valid immutable issuance provenances
```

The verifier must avoid recursive cycles/infinite recursion while validating the immutable correction graph.

### judgment

```text
JUDGMENT_HISTORICAL_PROVENANCE:
PARTIAL / REWORK_REQUIRED

CORRECTION_SUPERSESSION:
historical transitive provenance incomplete
```

---

# accepted boundary to preserve

Do not regress the important separation established by 0148/0225:

```text
historical immutable provenance
!= current authority effectiveness

historical counterpart validity
does NOT mean current guard usability

current G_HUMAN_* / G_JUDGMENT_* still revalidate current authority separately
```

A superseded historical gate/result/Judgment can remain valid historical provenance while unusable as a current transition guard.

---

# command-center judgment

- result_status: `HOLD_REWORK_REQUIRED`
- P1-7 Design: `REMAINS ACCEPTED / CLOSED`
- Stage 0A/0B commits: `PRESERVE`
- 0051 findings: `CLOSED`
- 0148 findings: `CLOSED`
- 0225 direct findings: `CLOSED`
- P1-7 Runtime: `REWORK_REQUIRED / HUMAN_PENDING`
- P1-8: `NOT_STARTED`
- PUBLIC_BOUNDED_LIVE: `NOT_RELEASED`
- Stage 1 runtime commit: `none`
- required_rework:
  1. projection-independent immutable HumanGate issuance verifier;
  2. HumanResult historical verifier must consume that gate verifier;
  3. P1-4 opening TransitionRequest/Decision provenance for normal HumanGate OPENED;
  4. correction-gate predecessor/SUPERSEDED lineage for OPENED_CORRECTION;
  5. Judgment supersession counterpart must have complete immutable issuance provenance;
  6. correction graph cycle/depth protection and fail-closed corruption proof.
- terminal_decision_reason: direct row/event provenance is now verified, but historical authority still stops one edge too early and trusts referenced gate/Judgment counterparts without proving their own immutable System issuance.

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

.aiassistant/records/aiscc/cycles/
20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_0225_aiscc-p1-7-historical-replay-provenance-integrity-runtime-rework-1.md
```

## next action

```text
P1-7 narrow transitive historical-authority graph rework
→ Command Center re-review
→ Human final P1-7 runtime review only after PASS

P1-8:
NOT_STARTED
```
