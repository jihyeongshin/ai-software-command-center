# 작업지시서: P1-2 Security / Sandbox / Runtime Boundary Design

## meta

- task_id: `20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1`
- created_at: `2026-08-27 11:15 KST`
- phase: `P1-2 — Security / Sandbox / Runtime Boundary Design`
- work_type: `DESIGN_AUDIT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `security trust boundary / sandbox / tool-network-secret permission model / runtime failure and budget policy`
- predecessor_phase: `P1-1 Core Domain / State Machine Design`
- predecessor_result: `ACCEPTED / CLOSED`
- predecessor_cycle: `.aiassistant/records/aiscc/cycles/20260827_1115_aiscc-p1-1-core-domain-state-machine-design-final-acceptance-1.cycle.md`
- implementation_status_before: `NOT_IMPLEMENTED`
- P1_3_status: `BLOCKED_UNTIL_P1_2_ACCEPTED`

## execution prerequisite

Before executing this Task, Human MUST complete the canonical closure Git persistence containing:

- accumulated P0-5 pending/terminal Cycle provenance still in the working tree;
- P1-1 Task/Cycle lineage;
- accepted `.aiassistant/rules/AISCC_ARCHITECTURE.md`;
- accepted `.aiassistant/rules/AISCC_ORCHESTRATION.md`;
- P1-1 terminal Cycle;
- current state / decision / next-action updates.

If the working tree still contains the pre-P1-2 closure set as uncommitted canonical changes, STOP:

```text
BLOCKED_REPOSITORY_PRECONDITION_DRIFT
```

Do not absorb those changes into P1-2.

## accepted inputs

P1-1 canonical invariants:

```text
AgentOutput != SystemState
EvidenceCandidate != AdmittedEvidence

HumanGateStatus != HumanResult
HumanResult != Judgment
Judgment != TransitionDecision
TransitionDecision != WorkflowState

RuntimeMode != WorkflowState
```

Accepted public runtime:

```text
PUBLIC_REPLAY_WITH_BOUNDED_LIVE
PUBLIC_RECORDED_REPLAY = default
PUBLIC_PAGE_VIEW_OR_REPLAY → NO_LLM_INFERENCE
```

Accepted release invariant:

```text
P1-2 security/runtime design
→ P1-3 safeguard implementation + verification
→ later P3 release/reverification
```

## 이번 턴 목표

Create the canonical design candidate:

```text
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
```

Define exact design semantics for:

1. principals and trust zones;
2. permission profile per RuntimeMode;
3. owner/private vs public execution isolation;
4. repository/worktree/synthetic-repository boundary;
5. filesystem/process/command/tool/network deny-by-default policy;
6. allowlist semantics;
7. credential/secret handling and non-exposure boundary;
8. mutable run isolation and cross-run leakage prevention;
9. timeout/retry/cancel/failure semantics;
10. idempotency and duplicate paid-run prevention;
11. abuse/throttling admission;
12. application budget guard semantics;
13. provider spend/hard-limit defense-in-depth when supported;
14. provider/budget failure → Recorded Replay fallback;
15. cleanup/residue/recovery requirements;
16. future security evidence required by P1-3;
17. exact P1-3 implementation/verification handoff;
18. exact P3-3 current-provider/release reverification handoff.

## 이번 턴 비목표

- sandbox/container/worktree implementation
- security runtime proof
- P1-3 implementation
- state-machine kernel implementation
- evidence-admission implementation
- Human-gate implementation
- provider/tool adapter implementation
- synthetic repository creation
- Cloudflare/Railway/OpenAI resource creation
- provider login
- API key/token/credential action
- current pricing/region/feature verification
- billing/spend-limit configuration
- deployment/public URL
- penetration test/benchmark
- Browser Project Source mutation

## 허용 범위

allowed_paths:

```text
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/reports/target/20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1/**
.aiassistant/tasks/active/20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1.md
.aiassistant/tasks/done/20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1.md
```

Read-only accepted owners:

```text
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

If coherent security design requires changing accepted P1-1 semantics, STOP with:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

## 절대 금지

- product/runtime/source implementation
- sandbox runtime experiment
- network/provider access
- credential/API-key inspection or generation
- secret value printing
- dependency installation
- Git add/commit/push/remote operation
- deployment
- Browser Project Source mutation
- P1-3 execution
- P3-3 execution
- changing accepted WorkflowState/transition authority in this Task

## 읽을 문서

1. `.aiassistant/rules/AISCC_AGENTS.md`
2. `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
3. `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
4. `.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md`
5. `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
6. `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md`
7. `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
8. `.aiassistant/records/aiscc/DECISION_REGISTER.md`
9. `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
10. `.aiassistant/rules/AISCC_ARCHITECTURE.md`
11. `.aiassistant/rules/AISCC_ORCHESTRATION.md`
12. `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
13. `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
14. `.aiassistant/records/aiscc/cycles/20260827_1115_aiscc-p1-1-core-domain-state-machine-design-final-acceptance-1.cycle.md`

Do not bulk-read unrelated historical Tasks/Cycles.

## required design A — principals / trust zones

Define at least:

- Human owner/operator
- AISCC System
- Agent/provider
- owner workspace/repository
- fixed synthetic public repository
- public anonymous/user request surface
- external provider
- persistence/event/evidence store
- secret/credential store if applicable conceptually

For every trust crossing specify:

- allowed information/action
- denied information/action
- enforcing owner
- failure behavior
- provenance/evidence requirement

## required design B — RuntimeMode permission profiles

Define separate permission profiles for:

### OWNER_SELF_DOGFOOD

May be broader, but must remain explicitly authorized and bounded.

### PUBLIC_RECORDED_REPLAY

```text
LLM inference: forbidden
source mutation: forbidden
shell/network/tool execution: forbidden
```

### PUBLIC_BOUNDED_LIVE

Must preserve:

```text
fixed synthetic repository only
allowlisted scenario only
server-fixed provider/model
bounded calls/retries/time/budget
no free-form task
no external repository/upload
no arbitrary shell/network
no owner/private workspace access
```

## required design C — deny-by-default

Specify fail-closed semantics for:

- filesystem
- process/shell
- tool
- outbound network
- credential/secret
- repository/worktree
- provider call
- unknown permission
- unknown scenario/action

No implicit allow from Agent prose.

## required design D — secret boundary

Define:

- secret material never enters public Task/Cycle/Replay;
- Agent receives only minimum required capability/handle when explicitly permitted;
- secret values are not logged/replayed;
- public runtime cannot select or submit credentials;
- secret detection stops public provenance admission without printing value.

Do not choose a concrete secret manager unless necessary.

## required design E — isolation / cleanup

Define domain requirements for:

- per-run mutable workspace
- cross-run read/write isolation
- owner/public separation
- cleanup on success/failure/cancel/timeout
- residue detection
- recovery after process failure
- what may be persisted vs destroyed

P1-2 defines semantics, not container implementation.

## required design F — timeout/retry/cancel

Define:

- finite wall-clock bound
- finite retry bound
- cancellation semantics
- timeout result
- provider/tool partial failure
- no silent success
- no unbounded retry loop
- workflow state interaction without redefining P1-1 state meanings

## required design G — idempotency / abuse / budget

Define:

```text
PUBLIC LIVE REQUEST
→ scenario allowlist
→ identity/session/abuse gate
→ idempotency
→ application budget admission
→ provider availability/capability gate
→ isolated run admission
```

Specify:

- duplicate click/refresh/retry does not automatically create a new paid run;
- finite per-run/application/global budget semantics;
- application guard is authoritative for admission;
- provider spend/hard limit is defense-in-depth when supported;
- exact provider feature/config remains deferred;
- budget/provider failure cannot disable Stored Replay.

## required design H — failure-domain separation

Preserve:

```text
LIVE_UNAVAILABLE_OR_BUDGET_EXHAUSTED
→ RECORDED_REPLAY_REMAINS_AVAILABLE
```

Define failure separation between:

- static/public page
- recorded replay data path
- live orchestration path
- external provider path

Do not claim deployment implementation exists.

## required design I — P1-3 security evidence contract

P1-2 MUST specify which safeguards P1-3 must implement and what proof classes are not substitutable.

At minimum P1-3 future proof must distinguish:

- static/source test
- unit/integration test
- actual sandbox/process/filesystem isolation proof
- actual network deny/allow proof
- secret non-exposure proof
- timeout/retry/cancel runtime proof
- idempotency/abuse/budget runtime proof
- cleanup/residue proof

Security unit tests MUST NOT be treated as complete sandbox-runtime proof.

## required design J — P3-3 boundary

P3-3 owns later:

- current provider capability verification
- actual provider/resource configuration
- current pricing/region verification
- exact model/call/token/time/run/currency caps
- provider spend/hard-limit configuration evidence
- deployed URL/accessibility
- release recovery
- competition submission

P3-3 MUST NOT become the first implementation stage for P1-2 safeguards.

## evidence contract

### executor_required — STATIC_SOURCE

- exact 14 read paths
- accepted P1-1 baseline read directly
- no stale Browser mirror substituted for repository canonical

### executor_required — SECURITY_BOUNDARY_DESIGN

Pass when:

- explicit trust-zone/principal map
- explicit RuntimeMode permission profiles
- deny-by-default policy
- secret boundary
- run isolation/cleanup/recovery
- timeout/retry/cancel
- idempotency/abuse/budget
- failure-domain separation
- P1-3 evidence handoff
- P3-3 handoff

### executor_required — P1_1_CONFORMANCE

Pass when security design does not redefine:

- WorkflowState
- Judgment/TransitionDecision order
- Human gate semantics
- state_version concurrency contract
- RuntimeMode != WorkflowState

### executor_required — DOCUMENT_INTEGRITY

- UTF-8
- Markdown fence parity
- no unintended control chars
- no unresolved placeholder
- `git diff --check` or equivalent

### human_owned — HUMAN_VERIFICATION

Human must review:

- trust zones
- permission profiles
- public/private isolation
- deny-by-default boundary
- secret handling
- isolation/cleanup/recovery
- budget/abuse policy
- P1-3 proof requirements
- P3-3 handoff

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

### not_required

- build
- DB runtime
- HTTP/browser runtime
- sandbox runtime
- provider access
- deployment

### forbidden

- implementation/runtime proof
- Git mutation
- provider/network/credential/deployment
- P1-3/P3-3 execution

## proof non-substitution

```text
security design
!= implemented safeguard

unit test
!= sandbox runtime proof

mock network deny
!= actual process/network isolation proof

secret scan
!= complete secret isolation proof

application budget design
!= provider spend cap configured

provider capability document
!= deployed configuration

Replay availability design
!= public deployment availability
```

## workflow expectation

- initial_state: `P1_2_DESIGN_READY`
- expected_terminal_candidate: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- Agent may decide terminal acceptance: `No`

## accept 기준

- one coherent `AISCC_SECURITY_SANDBOX.md`
- explicit fail-closed boundaries
- public/private permission profiles separated
- public mode cannot reach owner workspace/secrets/arbitrary shell/network
- Replay path remains available on Live/provider/budget failure by design
- implementation details deferred without leaving semantic holes
- P1-3 owns first safeguard implementation + verification
- P3-3 owns release-time provider/config verification only
- accepted P1-1 state semantics preserved
- no forbidden action
- Human review pending

## hold/reject 기준

- public Live permission profile is general-purpose coding-agent access
- free-form/external repo/upload/arbitrary shell/network permitted
- unknown permission fails open
- Human/Agent claim overrides security gate
- no cleanup/residue/recovery contract
- no stale/idempotency/budget boundary
- Replay depends on paid Live path for availability
- P1-3 proof contract is vague or substitutes unit tests for sandbox runtime evidence
- provider/deployment details are falsely claimed as implemented
- P1-1 workflow semantics redefined
- forbidden action executed

## export bundle

Target:

```text
.aiassistant/reports/target/20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`

## Task lifecycle

```text
.aiassistant/tasks/active/20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1.md
→
.aiassistant/tasks/done/20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1.md
```

`done` means Executor submission ready, not Human accepted.

## preserved artifacts after acceptance

Expected:

- `.aiassistant/tasks/done/20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1.md`
- `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- `.aiassistant/records/aiscc/cycles/<P1-2-terminal-cycle>.cycle.md`

## next action after acceptance

```text
P1-3 Security / Runtime Safeguard Implementation and Verification
```

Do not execute P1-3 in the same turn.
