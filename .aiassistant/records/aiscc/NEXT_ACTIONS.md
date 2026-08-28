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
```

## canonical queue

1. `P1-4` — Explicit State Machine Kernel Implementation
2. `P1-5` — Agent Provider and Tool Execution
3. `P1-6` — Evidence Admission
4. `P1-7` — Human Gate and Judgment
5. `P1-8` — Project Memory and Cycle Admission
6. `P2-1` — Command Center Web UI
7. `P2-2` — Synthetic Demo Repository
8. `P2-3` — Canonical Scenario Pack and Recorded Replay Corpus
9. `P2-4` — Self-Dogfooding Cutover
10. `P3-1` — Comparative Evaluation
11. `P3-2` — Public Repository Documentation
12. `P3-3` — Public Release and Competition Submission

## P1-3 terminal evidence

```text
final candidate paths:
55

final candidate aggregate SHA-256:
4a9f49a70bbe6cc628a9bc9e6612d07b724876beaf3fd0e672b9815343018c4c

unit + integration:
26 PASS

runtime security:
10 PASS

mandatory runtime proof:
8 / 8 EXECUTED_PASS

final P1-3 Docker residue:
none

Human final review:
ACCEPTED
```

## release gate

The prerequisite:

```text
NO_PUBLIC_BOUNDED_LIVE_RELEASE
BEFORE
P1_SECURITY_RUNTIME_SAFEGUARD_IMPLEMENTATION_AND_VERIFICATION_ACCEPTED
```

is now:

```text
SATISFIED
```

This does NOT release Public Bounded Live.

```text
PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

Remaining governance/provider/demo/release verification still applies.

## current next action

```text
phase:
P1-4

title:
Explicit State Machine Kernel Implementation

status:
READY / NOT_STARTED

pre-step:
persist P1-3 terminal canonical state + exact 55-path accepted implementation candidate in one local commit

implementation owner:
authoritative WorkRun / WorkflowState / state_version
TransitionRequest / TransitionEvaluation / TransitionDecision
atomic admitted state mutation
append-only admitted/denied transition provenance
stale-request concurrency control
idempotent duplicate transition request handling
restart-durable authoritative projection
projection/event consistency fail-closed behavior
```

## P1-4 boundaries

P1-4 MUST preserve:

```text
custom explicit state machine
LangGraph core NOT_USED

AgentOutput != SystemState
Judgment != TransitionDecision
TransitionDecision != WorkflowState
SecurityAdmissionDecision != TransitionDecision
RuntimeMode != WorkflowState
```

P1-4 MUST NOT implement:

```text
P1-5 provider/tool adapters
P1-6 evidence verifier/admission
P1-7 Human identity/gate/Judgment pipeline
P1-8 Cycle memory admission
public deployment
```

P1-6/P1-7 facts may appear only as typed opaque/admitted references or trusted abstract guard inputs.
Caller-provided booleans must not be exposed as a public authoritative mutation API.
