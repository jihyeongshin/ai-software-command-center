# AISCC Cycle Record

## meta

- cycle_id: `20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-hold-1`
- date: `2026-08-30T12:41:00+09:00`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT / P1-4_TRANSITION_PROVENANCE_CONSUMER`
- affected_areas: `HumanGate historical provenance / P1-4 transition root-of-trust`
- work_type: `P1_7_RUNTIME_REWORK_REVIEW`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `20260830_1142_aiscc-p1-7-transitive-historical-authority-graph-runtime-rework-1`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `P1_4_OPENING_TRANSITION_ROOT_PROVENANCE_INCOMPLETE`
- cycle_record_action: `create`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-hold-1.cycle.md`

## repository snapshot

- expected current HEAD: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- P1-7 accepted design commit: `238b0b41460c2504fd3244eadb06809d8692a60f`
- P1-7 design terminal commit: `c87cfc75f14476e10b4a02a2ab0bd295720a85a0`
- accepted design SHA-256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- reviewed predecessor runtime path count: `19`
- reviewed predecessor runtime aggregate SHA-256:
  `5211024c632934cee625529d626da097905f8270efa4727f013b7b76828bb106`
- Stage 1 runtime commit: `none`

## predecessor 1142 review result

1142 successfully closes its direct transitive graph findings.

Accepted as closed:

```text
projection-independent HumanGate base issuance verifier
→ CLOSED

normal OPENED gate:
TransitionRequest / Evaluation / Decision rows are required
→ CLOSED at local triple-link level

OPENED_CORRECTION:
valid predecessor + SUPERSEDED relation
→ CLOSED

HumanGate correction cycle detection
→ CLOSED

HumanResult consumes HumanGate historical verifier
→ CLOSED

Judgment predecessor/replacement:
complete base issuance per node
→ CLOSED

Judgment correction graph cycle detection
→ CLOSED
```

Executor evidence admitted:

```text
ruff:
PASS

mypy src:
PASS / 67 source files

unit:
98 PASS

focused PostgreSQL:
25 PASS

full unit + integration:
162 PASS

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
19

manifest SHA ↔ actual exported bytes:
19/19 MATCH

aggregate SHA-256:
5211024c632934cee625529d626da097905f8270efa4727f013b7b76828bb106
```

---

# load-bearing finding — normal HumanGate trusts a locally coherent P1-4 triple instead of canonical P1-4 admitted provenance

Current:

```text
_verify_normal_gate_transition_provenance(...)
```

loads:

```text
TransitionRequestRow
TransitionEvaluationRow
TransitionDecisionRow
```

and verifies important local relationships:

```text
request TaskContract / WorkRun / observed state/version
request target = HUMAN_REQUIRED

evaluation request relation
evaluation authoritative state/version

decision request/evaluation relation
decision outcome = ADMITTED
decision resulting state = HUMAN_REQUIRED
decision resulting version = gate bound version

opening event request/decision IDs
gate ID derivation
opening timestamp
```

This is useful but still weaker than proving that the transition is an authentic P1-4 admitted transition in the canonical WorkRun history.

## missing root provenance checks

The helper does not currently verify exact equivalents of:

```text
TransitionRequestRow.request_fingerprint
→ recomputes from the immutable request + persisted evaluation guard facts

TransitionEvaluationRow guard set
→ exact guard IDs required by the accepted P1-4 TransitionMatrix for this source/target

required guard semantic owners
→ exact accepted owner slots

for an ADMITTED decision:
all required guards satisfied
missing_guards empty / structurally coherent

G_HUMAN_REQUIRED is actually present as the accepted P1-7_HUMAN guard
for ADMISSION_PENDING → HUMAN_REQUIRED

decision admitting_owner / kernel_version
→ accepted P1-4 authority identity

this request/evaluation/decision is part of the WorkRun's canonical contiguous admitted lineage

current durable WorkRun projection
→ reconstructs consistently from all admitted P1-4 decisions
```

`PostgresWorkRunRepository._verify_consistency_in_session()` already contains canonical P1-4 logic for checking the complete admitted state/version lineage against the durable WorkRun projection.

The HumanGate verifier does not consume that authority.

## concrete corruption classes that are not rejected by the current gate verifier

A database-corrupt historical root may remain locally self-consistent while not being valid P1-4 provenance.

Examples:

```text
actual opening TransitionRequestRow.request_fingerprint
→ altered to another 64-char value

or

opening TransitionEvaluationRow.guards
→ G_HUMAN_REQUIRED removed/replaced
while decision row still says ADMITTED

or

a locally coherent request/evaluation/decision triple
→ inserted outside the canonical WorkRun admitted history
```

The current `_verify_normal_gate_transition_provenance()` can still accept such a triple if the fields it directly compares remain coherent.

Required invariant:

```text
locally coherent P1-4 rows
!= canonical admitted P1-4 transition provenance
```

A historical HumanGate is System-owned only if its opening transition is itself proven through P1-4's canonical durable authority model.

---

# required closure

Provide one canonical, projection-independent P1-4 historical transition provenance verifier, or reuse an existing exact equivalent.

Preferred ownership:

```text
P1-4 persistence/workflow owner
```

P1-7 HumanGate verification must consume it rather than implementing a weaker duplicate.

The verifier must prove at minimum:

```text
1. exact TransitionRequest immutable identity and request_fingerprint

2. exactly one Evaluation and Decision for the request

3. evaluation authoritative state/version == request observed state/version

4. exact required guard IDs for source → target from accepted P1-4 matrix

5. exact semantic owner for each required guard

6. ADMITTED:
   every required guard satisfied
   no unresolved missing required guard

7. decision:
   request/evaluation exact relation
   ADMITTED
   accepted P1-4 admitting owner/kernel authority
   resulting state/version exact

8. transition participates in the canonical contiguous admitted WorkRun history

9. complete WorkRun history reconstructs to the durable WorkRun projection
   even if this HumanGate transition is historical and the WorkRun has advanced
```

P1-7 must not reinterpret P1-4 transition truth.

Required:

```text
P1-4 historical transition verifier
!= P1-7 synthetic assertion
```

---

# command-center judgment

- result_status: `HOLD_REWORK_REQUIRED`
- P1-7 Design: `REMAINS ACCEPTED / CLOSED`
- Stage 0A/0B commits: `PRESERVE`
- 0051 findings: `CLOSED`
- 0148 findings: `CLOSED`
- 0225 findings: `CLOSED`
- 1142 direct transitive graph findings: `CLOSED`
- P1-7 Runtime: `REWORK_REQUIRED / HUMAN_PENDING`
- P1-8: `NOT_STARTED`
- PUBLIC_BOUNDED_LIVE: `NOT_RELEASED`
- Stage 1 runtime commit: `none`
- required rework:
  `canonical P1-4 opening transition root provenance only`
- terminal_decision_reason:
  `HumanGate transitive provenance now reaches the P1-4 transition rows, but it stops before proving that those rows are authentic members of P1-4's canonical admitted state-machine history.`

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

.aiassistant/records/aiscc/cycles/
20260830_1241_aiscc-p1-7-p1-4-opening-transition-root-provenance-hold-1.cycle.md
```

## next action

```text
P1-7 narrow P1-4 root-provenance rework
→ Command Center runtime re-review
→ Human final P1-7 runtime review only after PASS

P1-8:
NOT_STARTED
```
