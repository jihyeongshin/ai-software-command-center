# P1-7 Runtime Accepted → P1-8 Command Center Handoff

## purpose

This durable handoff allows a future Browser Command Center or new chat to begin P1-8 without chat
memory, File Library state, or a stale Project Source mirror. It records accepted/frozen facts only.
It does not design or implement P1-8.

## exact accepted Git lineage through P1-7 runtime

```text
P1-7 accepted design commit:
238b0b41460c2504fd3244eadb06809d8692a60f

P1-7 accepted design terminal commit / Commit A parent:
c87cfc75f14476e10b4a02a2ab0bd295720a85a0

P1-7 accepted runtime Commit A:
b4ba49ebaeb437d885bf22d52473c7d8a79832d1
```

Accepted design SHA-256:
`22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`.

Accepted runtime identity:
`21 paths / 1933e0451d101b142e099cc987babb426f87422d15338775d9d87bbf29fa2f90`.

## frozen predecessor authority

### P1-4 state and transition authority

- `WorkflowState` has the accepted exact nine-state vocabulary and the exact 22 transition pairs.
- the authoritative `WorkRun` row and `state_version` are System-owned.
- `TransitionRequest`, `TransitionEvaluation`, and `TransitionDecision` remain distinct durable objects.
- only P1-4 may issue an admitted `TransitionDecision` and atomically mutate `WorkflowState/state_version`.
- guard facts and P1-7 Human/Judgment objects are inputs; none substitutes for transition authority.

### P1-6 evidence authority

- `EvidenceCandidate != AdmittedEvidence`.
- `AdmittedEvidenceRef != G_EVIDENCE`.
- `EvidenceSetSatisfactionAttestation != TransitionDecision`.
- P1-6 alone owns evidence admission and exact checkpoint/state/version/target-use/root-bound `G_EVIDENCE`.
- `HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7`.
- historical provenance validity and current effectiveness are separate: a historical chain must verify
  immutably, while current guard use still requires current unsuperseded/unexpired authority.
- P1-6 does not mint or reinterpret `HumanGate`, `HumanResult`, `Judgment`,
  `G_HUMAN_*`, or `G_JUDGMENT_*`.

### P1-7 Human Gate and Judgment authority

- `HumanGate` is System-owned; V1 has one current unsuperseded gate per current
  `HUMAN_REQUIRED` authority epoch.
- `HumanResultKind = APPROVE | REWORK | REJECT`.
- `JudgmentKind = ACCEPTED | REJECTED | HOLD_REWORK_REQUIRED`.
- concurrent HumanResult winner is `FIRST_DURABLY_ADMITTED`.
- V1 policy exception/override is `NOT_SUPPORTED`.
- Agent/LLM proposals are non-authoritative historical provenance only.
- exact current P1-6 PRE_HUMAN `EvidenceSetSatisfactionAttestation` is mandatory for
  `G_HUMAN_REQUIRED`; missing, stale, wrong, revoked, superseded, or expired authority yields no guard,
  no gate-open event, and no transition.
- HumanResult/Judgment persistence never mutates WorkRun directly.

## exact P1-4 future-owner guards implemented by P1-7

```text
P1_7_HUMAN:
G_HUMAN_REQUIRED
G_HUMAN_NOT_REQUIRED
G_NO_PENDING_HUMAN_GATE
G_HUMAN_APPROVED
G_HUMAN_REWORK
G_HUMAN_REJECTED

P1_7_JUDGMENT:
G_JUDGMENT_ACCEPTED
G_JUDGMENT_REJECTED
G_JUDGMENT_REWORK
```

These facts are owner-backed, exact-authority-bound inputs to P1-4. They are not transition decisions.

## mandatory non-substitution

```text
HumanResult != Judgment
Judgment != TransitionDecision
HumanResult/Judgment != WorkflowState
HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7
G_EVIDENCE != G_HUMAN_* != G_JUDGMENT_*
SecurityAdmissionDecision != TransitionDecision
```

## accepted P1-7 runtime evidence

```text
full unit + integration: 183 / 183 PASS
PostgreSQL-marked: 49 collected
P1-7 Human PostgreSQL: 2 / 2 PASS
P1-4 PostgreSQL regression: 18 / 18 PASS
P1-6 PostgreSQL regression: 6 / 6 PASS
PostgreSQL: 17.6
Alembic: 20260829_0004
ruff: PASS
mypy: PASS / 67 source files
real provider calls: 0
credential/network external actions: 0
deployment: 0
Public Live release: 0
```

Human final runtime review is `HUMAN_PROVIDED / ACCEPTED`; P1-7 Runtime is
`HUMAN_PROVIDED / ACCEPTED / CLOSED`.

## P1-8 phase boundary

P1-8 owns the future dedicated design and implementation work for `Project Memory and Cycle Admission`.
At this handoff it is `NOT_STARTED / NEXT_ACTION`. No P1-8 data model, admission rule, lifecycle,
transition, API, persistence scheme, or implementation decision is created here.

P1-8 must not reinterpret or take ownership of:

```text
G_EVIDENCE
G_HUMAN_*
G_JUDGMENT_*
TransitionDecision
WorkflowState
HumanResult
Judgment
SecurityAdmissionDecision
```

The next chat should issue and read a dedicated P1-8 Task before source inspection or implementation.

## release boundary

`PUBLIC_BOUNDED_LIVE` remains `NOT_RELEASED`. No deployment, push, provider call, credentialed
external action, browser QA, or Project Source mirror sync was performed by this closure.
