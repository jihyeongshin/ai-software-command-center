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
```

## canonical queue

1. `P1-5` — Agent Provider and Tool Execution
2. `P1-6` — Evidence Admission
3. `P1-7` — Human Gate and Judgment
4. `P1-8` — Project Memory and Cycle Admission
5. `P2-1` — Command Center Web UI
6. `P2-2` — Synthetic Demo Repository
7. `P2-3` — Canonical Scenario Pack and Recorded Replay Corpus
8. `P2-4` — Self-Dogfooding Cutover
9. `P3-1` — Comparative Evaluation
10. `P3-2` — Public Repository Documentation
11. `P3-3` — Public Release and Competition Submission

## P1-4 terminal evidence

```text
final candidate paths:
19

final candidate aggregate SHA-256:
1316fd14faf6a2ad85f43ae9e9a2bab45c1736e4f28bea40d35865f53dee4cb5

targeted PostgreSQL integration:
17 PASS

full unit + integration:
74 PASS

PostgreSQL:
17.6

Alembic head:
20260828_0001

Human final review:
ACCEPTED
```

## release gate

P1-3 security safeguard prerequisite remains:

```text
SATISFIED
```

P1-4 authoritative workflow kernel prerequisite is now:

```text
SATISFIED
```

This still does NOT release Public Bounded Live.

```text
PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

P1-5/P1-6/P1-7/P1-8 and later demo/release verification remain required.

## current next action

```text
phase:
P1-5

title:
Agent Provider and Tool Execution

status:
READY / DESIGN_FREEZE_REQUIRED

first subtask:
Provider / Tool Execution Contract Design Freeze

pre-step:
persist P1-4 terminal canonical state + exact accepted 19-path implementation candidate in one local commit
```

## why P1-5 starts with a design freeze

P1-1/P1-2 already freeze the outer ownership/security boundary:

```text
P1-5
→ provider/tool execution adapter + execution events

AGENT_PROVIDER
→ proposal/output/tool/evidence candidates only
→ no permission expansion
→ no authoritative WorkflowState mutation

PUBLIC_RECORDED_REPLAY
→ provider inference 0
→ tool execution 0

PUBLIC_BOUNDED_LIVE
→ fixed synthetic repository
→ allowlisted scenario
→ server-fixed provider/model
→ bounded calls/retry/time/budget
```

But no Human-accepted exact P1-5 contract yet defines:

- provider/tool `ResourceDomain` authority integration with P1-3;
- exact provider/model/tool profile/selector identity;
- capability binding to exact provider/tool operation;
- exact `ExecutionStatus` durable projection/event semantics;
- provider/tool call idempotency;
- ambiguous timeout/unknown provider outcome handling;
- retry/cancel policy at the provider/tool layer;
- provider output/tool output durable candidate/reference boundary;
- provider adapter transport/API selection;
- tool registry/schema/argument binding;
- P1-6 evidence handoff.

Those decisions are load-bearing and must not be silently invented inside implementation.

## P1-5 design-freeze boundaries

The design MUST preserve:

```text
ExecutionStatus != WorkflowState

EXECUTOR_COMPLETED != ACCEPTED

AgentOutput != SystemState

provider/tool output
!= AdmittedEvidence

SecurityAdmissionDecision
!= provider result
!= TransitionDecision
```

It must also preserve P1-3 fail-closed behavior:

```text
no P1-5 provider/tool authority
→ PROVIDER / TOOL side effects DENY
```

P1-5 design does NOT implement:

```text
P1-6 evidence admission
P1-7 Human/Judgment
P1-8 Cycle memory
public deployment
real provider credentials/billing
```

## after P1-5 design Human acceptance

```text
P1-5 Provider / Tool Execution Implementation + Runtime Verification
```

Do not start implementation before that acceptance.
