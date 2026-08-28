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
```

## canonical queue

1. `P1-6` — Evidence Admission
2. `P1-7` — Human Gate and Judgment
3. `P1-8` — Project Memory and Cycle Admission
4. `P2-1` — Command Center Web UI
5. `P2-2` — Synthetic Demo Repository
6. `P2-3` — Canonical Scenario Pack and Recorded Replay Corpus
7. `P2-4` — Self-Dogfooding Cutover
8. `P3-1` — Comparative Evaluation
9. `P3-2` — Public Repository Documentation
10. `P3-3` — Public Release and Competition Submission

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

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

P1-6/P1-7/P1-8 and demo/release verification remain required.

## current next action

```text
phase:
P1-6

title:
Evidence Admission

status:
READY / DESIGN_FREEZE_REQUIRED

first subtask:
Evidence Admission Contract Design Freeze

pre-step:
persist final 42-path P1-5 runtime candidate + P1-5 terminal Cycle/state in one local commit
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

## why P1-6 starts with design freeze

No Human-accepted exact P1-6 contract yet freezes:

- evidence requirement identity/version;
- evidence type/classification model;
- task-scoped evidence ownership;
- executor_required / reuse_allowed / human_owned / not_required / forbidden semantics;
- candidate issuer/provenance binding;
- content/body/hash/reference authority;
- freshness/applicability/coverage rules;
- reuse and anti-replay semantics;
- evidence-set completeness;
- admission/rejection reason taxonomy;
- immutable admitted evidence refs;
- revocation/supersession/correction semantics;
- P1-4 `G_EVIDENCE` owner-bound fact issuance;
- Human-owned evidence boundary into P1-7;
- private/sensitive evidence redaction/export rules;
- persistence/concurrency/restart model.

Those decisions must not be invented inside implementation.

## after P1-6 design Human acceptance

```text
P1-6 Evidence Admission Implementation + Runtime Verification
```

Do not start P1-7 before P1-6 runtime acceptance.
