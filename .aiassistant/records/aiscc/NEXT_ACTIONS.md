# AISCC Next Actions

이 문서는 stable roadmap이다. per-turn execution log와 terminal judgment는 Cycle Record에 둔다.

## completed phases

```text
P0-1 → ACCEPTED / CLOSED
P0-2 → ACCEPTED / CLOSED
P0-3 → HUMAN_CONFIRMED / CLOSED
P0-4 → ACCEPTED / CLOSED
P0-5 → ACCEPTED / CLOSED
P1-1 → ACCEPTED / CLOSED
```

## canonical queue

1. `P1-2` — Security / Sandbox / Runtime Boundary Design
2. `P1-3` — Security / Runtime Safeguard Implementation and Verification
3. `P1-4` — Explicit State Machine Kernel Implementation
4. `P1-5` — Agent Provider and Tool Execution
5. `P1-6` — Evidence Admission
6. `P1-7` — Human Gate and Judgment
7. `P1-8` — Project Memory and Cycle Admission
8. `P2-1` — Command Center Web UI
9. `P2-2` — Synthetic Demo Repository
10. `P2-3` — Canonical Scenario Pack and Recorded Replay Corpus
11. `P2-4` — Self-Dogfooding Cutover
12. `P3-1` — Comparative Evaluation
13. `P3-2` — Public Repository Documentation
14. `P3-3` — Public Release and Competition Submission

## required ordering

```text
P1-2 Security / Sandbox / Runtime Boundary Design
→ P1-3 Security / Runtime Safeguard Implementation and Verification
→ remaining Governance Kernel implementation
→ P2 Demonstration / Self-Dogfooding
→ P3 Proof / public release / submission
```

## release gate invariant

```text
NO_PUBLIC_BOUNDED_LIVE_RELEASE
BEFORE
P1_SECURITY_RUNTIME_SAFEGUARD_IMPLEMENTATION_AND_VERIFICATION_ACCEPTED
```

`P3-3` MUST NOT be the first safeguard implementation stage.

## current next action

```text
phase: P1-2
current_action: Security / Sandbox / Runtime Boundary Design
status: READY / TASK_CONTRACT_ISSUED / NOT_EXECUTED
predecessor: P1-1 ACCEPTED / CLOSED
execution_gate: complete current canonical closure Git persistence first
```

## accepted P1-1 handoff

P1-2 MUST preserve:

- System-owned authoritative workflow state
- Agent cannot mutate state directly
- Human-owned verification cannot be forged by Agent/Executor
- `RuntimeMode != WorkflowState`
- `OWNER_SELF_DOGFOOD` and `PUBLIC_BOUNDED_LIVE` may use different permission profiles
- security failure cannot be silently relabeled as successful workflow outcome

## deployment handoff

`AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1` remains accepted direction but `NOT_EXECUTED`.

Provider resources, current provider capability/pricing, API keys, billing controls, deployment and public URL remain future-task evidence.
