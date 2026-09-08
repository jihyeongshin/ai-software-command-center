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
P1-6 Durable Evidence Content Extension Design → HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-6 Durable Evidence Content Extension Runtime → HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-7 Human Gate and Judgment Design → HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-7 Human Gate and Judgment Runtime → HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-8 Project Memory and Cycle Admission Design → HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-8 NEXT_ACTION_CONTEXT Source Authority Corrected Revision → HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-8 Prerequisite Owner Authority Exact-Contract/Source-Enrollment Design → HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-8 Project Memory and Cycle Admission Runtime → HUMAN_PROVIDED / ACCEPTED / CLOSED
P1 → ACCEPTED / CLOSED
P2-1 Command Center Web UI → ACCEPTED / CLOSED / PERSISTED
```

The accepted preconditions include both the P1-6 durable-content design and runtime as
`HUMAN_PROVIDED / ACCEPTED / CLOSED`.

## canonical queue

The corrected source-authority contract, prerequisite owner-authority exact contract, and P1-8 runtime are
accepted. P1 is closed and P2 entry is ready without starting P2:

```text
P1-6 Durable Evidence Content Extension Design -> HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-6 Durable Evidence Content Extension Runtime -> HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-8 durable-content prerequisite -> SATISFIED / BLOCKER_RESOLVED
P1-8 NEXT_ACTION_CONTEXT Source Authority Corrected Revision -> HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-8 prerequisite owner-authority exact-contract/source-enrollment design -> HUMAN_PROVIDED / ACCEPTED / CLOSED
P1-8 prerequisite design blocker -> CLEARED_BY_HUMAN_ACCEPTED_JOINT_DESIGN
P1-8 Runtime -> HUMAN_PROVIDED / ACCEPTED / CLOSED
P1 -> ACCEPTED / CLOSED
P2-1 -> ACCEPTED / CLOSED / PERSISTED
P2-1 persistence commit -> 1fb9fd5e29e85481fa3c6ce78542de1fda6bf138
P2 -> IN_PROGRESS
P2-2 -> NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE
```

1. `P1-6` — Evidence Admission (`ACCEPTED / CLOSED`)
2. `P1-6 Durable Content Design` — Durable Evidence Content Extension (`HUMAN_PROVIDED / ACCEPTED / CLOSED`)
3. `P1-6 Durable Content Runtime` — Durable Evidence Content Extension Implementation (`HUMAN_PROVIDED / ACCEPTED / CLOSED`)
4. `P1-7 Design` — Human Gate and Judgment (`HUMAN_PROVIDED / ACCEPTED / CLOSED`)
5. `P1-7 Runtime` — Human Gate and Judgment Implementation + Verification (`HUMAN_PROVIDED / ACCEPTED / CLOSED`)
6. `P1-8 Design` — Project Memory and Cycle Admission (`HUMAN_PROVIDED / ACCEPTED / CLOSED`)
7. `P1-8 NEXT_ACTION_CONTEXT Source Authority Corrected Revision` (`HUMAN_PROVIDED / ACCEPTED / CLOSED`)
8. `P1-8 Prerequisite Owner Authority Exact Contract` (`HUMAN_PROVIDED / ACCEPTED / CLOSED`)
9. `P1-8 Runtime` — Project Memory and Cycle Admission Implementation (`HUMAN_PROVIDED / ACCEPTED / CLOSED`)
10. `P2-1` — Command Center Web UI (`ACCEPTED / CLOSED / PERSISTED`)
11. `P2-2` — Synthetic Demo Repository (`NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE`)
12. `P2-3` — Canonical Scenario Pack and Recorded Replay Corpus
13. `P2-4` — Self-Dogfooding Cutover
14. `P3-1` — Comparative Evaluation
15. `P3-2` — Public Repository Documentation
16. `P3-3` — Public Release and Competition Submission

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

P1-6 Durable Evidence Content Extension design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension runtime:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-7 Human Gate and Judgment design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-7 Human Gate and Judgment runtime:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 Project Memory and Cycle Admission design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 NEXT_ACTION_CONTEXT Source Authority design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 prerequisite owner-authority exact-contract design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 Project Memory and Cycle Admission runtime:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1:
ACCEPTED / CLOSED

P2-1:
ACCEPTED / CLOSED / PERSISTED

P2-1 persistence commit:
1fb9fd5e29e85481fa3c6ce78542de1fda6bf138

P2:
IN_PROGRESS

P2-2:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

The prerequisite owner-authority design blocker is `CLEARED_BY_HUMAN_ACCEPTED_JOINT_DESIGN`. P1-8 runtime, P1,
and P2-1 are closed. P2-2 implementation has not started, and later demo/release verification remains required.

## current next action

```text
phase:
P2

title:
P2-2 Synthetic Demo Repository

status:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

first subtask:
issue a separate exact P2-2 Task before any P2-2 execution

pre-step:
use the terminal P2-1 state and corrected Command Center session/artifact-delivery workflow; do not infer P2-2 started status from entry readiness
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

## P1-6 durable evidence-content extension design terminal state

```text
P1-6 Durable Evidence Content Extension Design
HUMAN_PROVIDED / ACCEPTED / CLOSED

accepted design SHA-256:
ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411

design persistence commit:
32e88234ad7a7cbaa545e12f8c7e03b5897202cb

terminal Cycle:
20260830_2357_aiscc-p1-6-durable-evidence-content-design-final-acceptance-1.cycle.md

runtime:
HUMAN_PROVIDED / ACCEPTED / CLOSED

accepted runtime commit:
8320a3c567a58bab5f728a88d5c88862392d187c

accepted runtime identity:
13 paths / 2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721
```

## terminal P1-7 state and P1-8 handoff

P1-7 Human Gate and Judgment Design and Runtime are `HUMAN_PROVIDED / ACCEPTED / CLOSED`.
The accepted runtime is commit `b4ba49ebaeb437d885bf22d52473c7d8a79832d1`, exact
`21 paths / 1933e0451d101b142e099cc987babb426f87422d15338775d9d87bbf29fa2f90`.

P1-8 Design is `HUMAN_PROVIDED / ACCEPTED / CLOSED` at exact SHA
`100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a` and commit
`c108e9c02f222cf51ce833e311465584447b3571`. Its durable-content prerequisite is `SATISFIED`. The
The historical `NEXT_ACTION_CONTEXT` source-authority acceptance at SHA
`19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1` and commit
`35901125cc5842734cf1e8eb3374d10e4ee866e3` remains preserved. Its corrected revision
`7cf27b77bb961280becfc55ecf8e71c9406da9b7b91df0d2697132c2655108db` and prerequisite rule
`8b19970629c55629df1560f2329b529992eceb86d5e4216baf0b7e78d3876960` are jointly accepted in commit
`b271f98df7d53edd3d3bc418443ff192e7aa4cfb`. P1-8 Runtime is now
`HUMAN_PROVIDED / ACCEPTED / CLOSED` under the terminal closure authority and must continue to preserve
`G_EVIDENCE`, `G_HUMAN_*`, `G_JUDGMENT_*`, `TransitionDecision`, `WorkflowState`,
`HumanResult`, `Judgment`, and `SecurityAdmissionDecision` without reinterpretation.
P1 is `ACCEPTED / CLOSED`; P2-1 is `ACCEPTED / CLOSED / PERSISTED`; P2-2 is
`NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE`. Public Bounded Live remains `NOT_RELEASED`.
