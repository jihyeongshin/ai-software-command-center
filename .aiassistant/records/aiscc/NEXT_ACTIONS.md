# AISCC Next Actions

이 문서는 stable roadmap이다. per-turn execution log와 terminal judgment는 Cycle Record에 둔다.

## completed phases / accepted preconditions

```text
P0-1 → ACCEPTED / CLOSED
P0-2 → ACCEPTED / CLOSED
P0-3 → HUMAN_CONFIRMED / CLOSED
P0-4 → ACCEPTED / CLOSED
P0-5 → ACCEPTED / CLOSED
P1-1 → ACCEPTED / CLOSED
P1-2 → ACCEPTED / CLOSED
P1-3 Runtime Substrate → HUMAN_PROVIDED / ACCEPTED
P1-3 Security / Runtime Safeguard Implementation and Verification → ACCEPTED / CLOSED
P1-4 Explicit State Machine Kernel Implementation → ACCEPTED / CLOSED
P1-5 Provider / Tool Execution Design → ACCEPTED / CLOSED
P1-5 Provider / Tool Execution Runtime → ACCEPTED / CLOSED
P1-6 Evidence Admission Design → HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-6 Evidence Admission Runtime → HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-7 Human Gate and Judgment Design → HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-7 Human Gate and Judgment Runtime → HUMAN_PROVIDED / ACCEPTED / CLOSED
```

## canonical queue

1. `P1-6` — Evidence Admission (`ACCEPTED / CLOSED`)
2. `P1-7 Design` — Human Gate and Judgment (`HUMAN_PROVIDED / ACCEPTED / CLOSED`)
3. `P1-7 Runtime` — Human Gate and Judgment Implementation + Verification (`HUMAN_PROVIDED / ACCEPTED / CLOSED`)
4. `P1-8` — Project Memory and Cycle Admission (`NOT_STARTED / NEXT_ACTION`)
5. `P2-1` — Command Center Web UI
6. `P2-2` — Synthetic Demo Repository
7. `P2-3` — Canonical Scenario Pack and Recorded Replay Corpus
8. `P2-4` — Self-Dogfooding Cutover
9. `P3-1` — Comparative Evaluation
10. `P3-2` — Public Repository Documentation
11. `P3-3` — Public Release and Competition Submission

## P1-5 terminal evidence

```text
final candidate:
42 paths

aggregate SHA-256:
ffeb5ba70649c564c482c2cff79ce8e2b0a462f811d8e03f2c1096f170bd39d6

unit + integration:
145 PASS

P1-5 persistence/accounting:
23 PASS

P1-5 runtime:
10 PASS

P1-3 Docker runtime regression:
10 PASS

PostgreSQL:
17.6

Alembic:
20260828_0002

real provider calls:
0

final residue:
none

Human final review:
ACCEPTED
```

## current release status

```text
P1-3 safeguard prerequisite:
SATISFIED

P1-4 authoritative workflow kernel:
SATISFIED

P1-5 bounded provider/tool runtime:
SATISFIED

P1-7 Human Gate and Judgment design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-7 Human Gate and Judgment runtime:
HUMAN_PROVIDED / ACCEPTED / CLOSED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

P1-8 and demo/release verification remain required. P1-6 and P1-7 design/runtime are
`ACCEPTED / CLOSED`.

## current next action

```text
phase:
P1-8

title:
Project Memory and Cycle Admission

status:
NOT_STARTED / NEXT_ACTION

first subtask:
issue a dedicated P1-8 design Task that preserves all accepted predecessor authority

pre-step:
use the durable P1-8 handoff and do not reinterpret P1-4/P1-6/P1-7 authority
```

## P1-6 outer authority already inherited

P1-1/P1-4/P1-5 already require:

```text
AgentOutput != SystemState
EvidenceCandidate != AdmittedEvidence
P1-5 producer ref != AdmittedEvidence
G_EVIDENCE requires P1-6 Evidence authority
P1-6 cannot mint P1-4 TransitionDecision or P1-7 Judgment
```

P1-6 therefore owns evidence requirement matching/admission, not execution truth or workflow state.

## accepted P1-6 implementation authority

The Human-accepted canonical contract is:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

SHA-256:
0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463
```

It freezes exact five-profile evidence authority, immutable RequirementSet/EvidenceCheckpoint
identity, checkpoint-specific applicability/completeness, fail-closed candidate admission,
checkpoint-bound `G_EVIDENCE`, direct/P1-7 Human producer separation, supplemental non-authority,
PostgreSQL durability/concurrency/restart, and sensitive evidence export rules.

## P1-6 runtime terminal state

```text
P1-6 Evidence Admission Runtime
HUMAN_PROVIDED / ACCEPTED / CLOSED

runtime acceptance commit:
f36f19f5b84cef9bc1452e7cb9e9e36c4ae2873e

terminal Cycle:
20260829_1920_aiscc-p1-6-evidence-admission-runtime-final-acceptance-1.cycle.md
```

## terminal P1-7 state and P1-8 handoff

P1-7 Human Gate and Judgment Design and Runtime are `HUMAN_PROVIDED / ACCEPTED / CLOSED`.
The accepted runtime is commit `b4ba49ebaeb437d885bf22d52473c7d8a79832d1`, exact
`21 paths / 1933e0451d101b142e099cc987babb426f87422d15338775d9d87bbf29fa2f90`.

P1-8 Project Memory and Cycle Admission is `NOT_STARTED / NEXT_ACTION`. Its future Task must preserve
`G_EVIDENCE`, `G_HUMAN_*`, `G_JUDGMENT_*`, `TransitionDecision`, `WorkflowState`,
`HumanResult`, `Judgment`, and `SecurityAdmissionDecision` without reinterpretation.
Public Bounded Live remains `NOT_RELEASED`.
