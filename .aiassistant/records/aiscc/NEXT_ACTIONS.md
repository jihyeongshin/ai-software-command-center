# AISCC Next Actions

이 문서는 stable roadmap이다. per-turn 실행 log와 terminal judgment는 Cycle Record에 둔다.

## canonical queue

1. `P0-5` — First Project Source Mirror v1
2. `P1-1` — Core Domain / State Machine Design
3. `P1-2` — Security / Sandbox / Runtime Boundary Design
4. `P1-3` — Security / Runtime Safeguard Implementation and Verification
5. `P1-4` — Explicit State Machine Kernel Implementation
6. `P1-5` — Agent Provider and Tool Execution
7. `P1-6` — Evidence Admission
8. `P1-7` — Human Gate and Judgment
9. `P1-8` — Project Memory and Cycle Admission
10. `P2-1` — Command Center Web UI
11. `P2-2` — Synthetic Demo Repository
12. `P2-3` — Canonical Scenario Pack and Recorded Replay Corpus
13. `P2-4` — Self-Dogfooding Cutover
14. `P3-1` — Comparative Evaluation
15. `P3-2` — Public Repository Documentation
16. `P3-3` — Public Release and Competition Submission

Required ordering:

```text
P0-5 First Project Source Mirror v1
→ P1-1 Core Domain / State Machine Design
→ P1-2 Security / Sandbox / Runtime Boundary Design
→ P1-3 Security / Runtime Safeguard Implementation and Verification
→ remaining Governance Kernel implementation tasks
→ P2 Demonstration / scenario / Self-Dogfooding
→ P3 Proof / public release / submission
```

## release gate invariant

```text
NO_PUBLIC_BOUNDED_LIVE_RELEASE
BEFORE
P1_SECURITY_RUNTIME_SAFEGUARD_IMPLEMENTATION_AND_VERIFICATION_ACCEPTED
```

`P1-3`은 다음 safeguard를 처음 구현하고 applicable evidence로 검증하는 dedicated stage다.

- public/private permission-profile isolation
- synthetic repository isolation
- command/network deny-by-default
- secret/credential boundary
- timeout/retry/cancel failure semantics
- idempotency/abuse/throttling guard
- application budget guard
- provider spend-guard capability/configuration when supported
- Replay fallback under Live/provider/budget failure

`P3-3`은 이미 설계·구현·검증된 safeguard를 current provider와 release environment에서 재검증하고 구성한다. `P3-3`은 위 safeguard의 first implementation stage가 아니다.

## current next action

```text
task_id: P0-5
title: First Project Source Mirror v1
status: READY_AFTER_P0_4_HUMAN_ACCEPTANCE
owner: future P0-5 Task Contract
```

P0-5는 tracked manifest, ignored generated mirror bundle, canonical/body hash mapping, Human complete Browser Project Source replacement를 소유한다. P0-4는 이를 실행하지 않았다.

## deployment decision handoff

`AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1`은 accepted direction이지만 `NOT_EXECUTED`다. Provider resource, region/plan capability, pricing, budget control, API key, deployment, public URL은 해당 future Task에서 current official source와 actual configuration evidence로 검증해야 한다.
