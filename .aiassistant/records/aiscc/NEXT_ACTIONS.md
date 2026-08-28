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
P1-5 Provider / Tool Execution Contract Design Freeze → ACCEPTED / CLOSED
```

## canonical queue

1. `P1-5` — Provider / Tool Execution Implementation + Runtime Verification
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

## P1-5 accepted design

```text
canonical:
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md

SHA-256:
12070677aa1cfa74b7eea9a52db24f78aacd2bf23d655f125a7689797d172443

Human final review:
ACCEPTED
```

Accepted runtime implementation contract includes:

```text
ExecutionStatus exact four values
provider/tool selector authority + P1-3 ALLOW separation
scoped SECRET mediation
server-owned ProviderProfile / ToolRegistry
bounded provider/tool loop
append-only execution attempts/operations/events
OpenAI Responses V1 store=false local-history continuation
unknown-outcome no-blind-retry
P1-6 output/submission ref handoff
Replay zero execution
```

## release gate

P1-3 safeguard prerequisite:

```text
SATISFIED
```

P1-4 authoritative state-machine prerequisite:

```text
SATISFIED
```

P1-5 design prerequisite:

```text
SATISFIED
```

Public Bounded Live remains:

```text
NOT_RELEASED
```

P1-5 runtime, P1-6/P1-7/P1-8, demo and release evidence remain required.

## current next action

```text
phase:
P1-5

title:
Provider / Tool Execution Implementation + Runtime Verification

status:
READY / NOT_STARTED

pre-step:
persist accepted AISCC_PROVIDER_TOOL_EXECUTION.md + P1-5 design terminal Cycle/state in one local commit

implementation:
provider/tool models + authority + profiles
P1-3 PROVIDER/TOOL/SECRET extension integration
OpenAI Responses V1 stateless adapter
ToolRegistry / dispatcher
bounded AgentExecutionService
ExecutionAttempt/Operation/Event PostgreSQL durability
P1-4 execution-start/submission ref validation
fake/local provider transport runtime proof
```

## implementation acceptance boundary

Required:

```text
real provider call:
NOT REQUIRED

real API key:
FORBIDDEN / NOT REQUIRED

real billing/spend configuration:
NOT REQUIRED

public deployment:
FORBIDDEN
```

Acceptance uses deterministic fake/local provider transport plus actual P1-3 security and isolated
PostgreSQL runtime proof.

Exact current provider SDK/API compatibility may be verified from official public documentation and
package metadata, but no external provider side effect is required.

## next after P1-5 runtime Human acceptance

```text
P1-6 Evidence Admission
```

Do not implement P1-6 in P1-5.
