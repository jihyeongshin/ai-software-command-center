# 작업지시서: P1-2 Security Action-State and Public Cancel Authorization Alignment Rework

## meta

- task_id: `20260827_1247_aiscc-p1-2-security-action-state-and-public-cancel-authorization-alignment-rework-1`
- created_at: `2026-08-27 12:47 KST`
- phase: `P1-2 — Security / Sandbox / Runtime Boundary Design`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `security action-state eligibility / public mutable-control authorization`
- predecessor_task: `20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1`
- predecessor_result: `HOLD_REWORK_REQUIRED`
- predecessor_cycle: `.aiassistant/records/aiscc/cycles/20260827_1247_aiscc-p1-2-security-action-state-and-cancel-authorization-hold-1.cycle.md`
- predecessor_HEAD: `db81e065943970dfd19df4013de40106006fbec0`
- P1_3_status: `BLOCKED_UNTIL_P1_2_ACCEPTED`

## 현재 상태

Do NOT broadly redesign the predecessor candidate.

Retain unless directly conflicting:

- principals/trust zones;
- `SecurityAdmissionDecision = ALLOW | DENY`;
- RuntimeMode permission profiles;
- deny-by-default resource-domain rules;
- secret/opaque capability boundary;
- repository/per-run/cross-run isolation;
- timeout/retry/cancel cleanup semantics;
- idempotency/abuse/application-budget model;
- Replay/Live/provider failure-domain separation;
- P1-3 proof classes;
- P3-3 handoff;
- all accepted P1-1 semantics.

Current gaps are exactly:

1. current state/version freshness is checked, but action-class eligibility for
   each P1-1 `WorkflowState` is not defined;
2. public cancel requests are accepted as a request type, but target-run
   authorization is not bound to the requesting principal/session/run context.

## 이번 턴 목표

1. Add an exact security action-class model or equivalent.
2. Bind each side-effect/control/read/recovery class to admissible P1-1
   `WorkflowState` semantics.
3. Make unknown state/action combinations fail closed.
4. Keep state/version freshness and action/state eligibility as separate guards.
5. Define exact public cancel target authorization.
6. Make public visibility/read access non-substitutable for cancel authority.
7. Align trust crossing, permission evaluation, timeout/cancel section and
   P1-3 proof handoff with the corrected model.
8. Leave implementation details deferred.
9. Produce corrected `AISCC_SECURITY_SANDBOX.md` candidate/report/export with
   Human acceptance pending.

## 비목표

- change the P1-1 nine-state set
- change P1-1 state meanings
- change Judgment/TransitionDecision/HumanGate semantics
- security implementation
- P1-3 execution
- provider/tool adapter implementation
- DB/API/auth/token implementation
- browser/network/provider runtime proof
- Git add/commit/push
- deployment/provider credential/billing
- Browser Project Source sync

## 허용 범위

allowed_paths:

```text
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/reports/target/20260827_1247_aiscc-p1-2-security-action-state-and-public-cancel-authorization-alignment-rework-1/**
.aiassistant/tasks/active/20260827_1247_aiscc-p1-2-security-action-state-and-public-cancel-authorization-alignment-rework-1.md
.aiassistant/tasks/done/20260827_1247_aiscc-p1-2-security-action-state-and-public-cancel-authorization-alignment-rework-1.md
```

allowed_actions:

- exact canonical/source read
- modify the P1-2 candidate only
- narrow static consistency checks
- `git status`
- `git diff -- .aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- `git diff --check`
- SHA-256
- target export
- active → done lifecycle after executor-required work completes

## 절대 금지

- application/runtime/sandbox implementation
- adding or renaming P1-1 WorkflowStates
- P1-3/P3-3 execution
- dependency installation
- network/provider access
- credential/API key inspection/generation
- Git add/commit/push/remote
- deployment
- Browser Project Source mutation
- Human acceptance claim

## 읽을 문서

1. `.aiassistant/rules/AISCC_AGENTS.md`
2. `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
3. `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
4. `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
5. `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md`
6. `.aiassistant/records/aiscc/DECISION_REGISTER.md`
7. `.aiassistant/rules/AISCC_ARCHITECTURE.md`
8. `.aiassistant/rules/AISCC_ORCHESTRATION.md`
9. `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
10. `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
11. `.aiassistant/records/aiscc/cycles/20260827_1247_aiscc-p1-2-security-action-state-and-cancel-authorization-hold-1.cycle.md`
12. `.aiassistant/tasks/done/20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1.md`

This is the minimum authoritative context set.

Do not bulk-read unrelated historical Tasks/Cycles.

## required correction A — security action classes

Define one exact canonical action classification.

Names are design-owned; an acceptable model could distinguish concepts such as:

```text
RUN_EXECUTION_SIDE_EFFECT
READ_RUN_INPUT_OR_CANDIDATE
CONTROL_CANCEL_OR_TERMINATE
CLEANUP_REVOKE_QUARANTINE
RECOVERY_RECONCILIATION
REPLAY_READ_ONLY
SYSTEM_DURABLE_PROVENANCE
```

These examples are not mandatory names.

For every class define:

- requester/principal;
- whether it may create external/process/filesystem/provider side effects;
- admissible P1-1 WorkflowStates;
- required Task/profile/scenario/capability guards;
- required state/version freshness;
- failure result;
- provenance.

Do not encode provider/tool/error details as new WorkflowStates.

## required correction B — exact state/action eligibility

The security rule MUST express an exact predicate equivalent to:

```text
SECURITY_ALLOW
→ current authoritative state/version is fresh
→ action class is admissible in current WorkflowState
→ Task/profile/scenario/resource/capability/limit guards pass
```

`state_version` equality alone MUST NOT be treated as sufficient authorization.

At minimum resolve:

### normal execution side effects

Agent/tool/process/provider work that advances an execution attempt must only be
admissible when consistent with accepted P1-1 `RUNNING` semantics.

If another state is allowed for a specific action class, justify the semantic
reason explicitly.

### READY

May admit the controlled action required to start an attempt, but MUST NOT
implicitly allow arbitrary run side effects before `RUNNING` is authoritative.

### ADMISSION_PENDING / HUMAN_REQUIRED / REWORK_REQUIRED

Normal execution side effects must not continue merely because a prior
capability exists.

Any read-only review/evidence action or explicitly authorized rework-start
control must be separately classified.

### BLOCKED

Normal execution is denied.

Safety cleanup/revoke/quarantine and explicitly defined blocker-recovery checks
may remain System-admissible.

### terminal states

`ACCEPTED`, `REJECTED`, `FAILED` MUST deny new normal execution/provider/tool
side effects.

System-owned cleanup/revoke/reconciliation/provenance may still execute when
needed to safely settle resources.

## required correction C — capability lifetime versus state transition

Define what happens to previously issued capabilities when WorkflowState changes.

Minimum:

```text
STATE/VERSION CHANGE
→ previously evaluated permission is not reusable without revalidation
```

For capabilities that must not survive a transition, define revoke/expiry
semantics.

A terminal state MUST NOT leave an execution/provider capability usable merely
because its lease time has not expired.

## required correction D — public cancel authorization

Define an exact target-authorization contract.

Minimum invariant:

```text
PUBLIC_CANCEL_REQUEST
→ requester identity/session is admitted
→ target run belongs to / is controllable by that requester context
→ cancellation authority/capability is valid
→ current target run/state/version is revalidated
→ cancel intent admitted or denied
```

Required statements:

- public Replay/catalog visibility does not grant cancel authority;
- guessing/knowing a run ID does not grant cancel authority;
- another public session/principal cannot cancel a run without explicit
  delegated control authority;
- expired/mismatched/unknown authorization fails closed;
- public cancel is idempotent;
- Human/System/owner administrative cancel, if allowed, uses a separate
  versioned authorization path;
- cancel intent does not directly mutate `WorkflowState`.

Do not choose HTTP auth/session/token implementation technology in this Task.

## required correction E — trust crossing alignment

Update the public trust crossing so `cancel request` is not merely schema-valid.

It must carry or resolve an authorization reference that is checked against the
target run.

Update required provenance to include, without private/secret value:

- requester/session/principal ref;
- target run ref;
- authorization/capability ref;
- observed target state/version;
- decision/reason.

## required correction F — P1-3 proof handoff

Add/adjust P1-3 proof requirements so runtime verification includes:

1. an action allowed in the wrong WorkflowState is denied;
2. stale capability after state/version transition is denied/revoked;
3. terminal state cannot issue/use normal execution/provider side effects;
4. cleanup/revocation can still safely settle terminal/blocked runs where
   designed;
5. public session A cannot cancel session B's run;
6. public read/Replay access does not imply cancel access;
7. repeated authorized cancel is idempotent.

These runtime proofs do not need to be implemented in P1-2.

## evidence contract

### executor_required — STATIC_SOURCE

Pass:

- exact 12 required paths read;
- predecessor HOLD applied;
- no historical Browser chat used as authority.

### executor_required — ACTION_STATE_MODEL

Pass:

- exact action classes or equivalent;
- exact WorkflowState eligibility;
- freshness guard separate from semantic state eligibility;
- capability transition/revocation semantics;
- no new P1-1 state.

### executor_required — CANCEL_AUTHORIZATION_MODEL

Pass:

- exact public requester→target-run authorization;
- run visibility != cancel authority;
- cross-session cancel deny;
- current state/version revalidation;
- idempotent cancel semantics.

### executor_required — P1_1_CONFORMANCE

Pass:

- nine WorkflowStates unchanged;
- RUNNING remains admitted active execution attempt;
- terminal states remain terminal;
- cancel/security decisions do not directly mutate WorkflowState;
- Judgment/TransitionDecision/HumanGate semantics unchanged.

### executor_required — DOCUMENT_INTEGRITY

Pass:

- UTF-8;
- Markdown fence parity;
- no unintended control chars;
- no unresolved placeholder;
- `git diff --check` or equivalent.

### reuse_allowed

Predecessor P1-2 candidate:

```text
REUSED_CANDIDATE
```

for all scope not directly affected by this HOLD.

Accepted P1-1 baseline:

```text
REUSED_ACCEPTED
```

### human_owned

`HUMAN_VERIFICATION`

After corrected candidate, Human reviews the complete P1-2 baseline:

- trust zones;
- permission profiles;
- action/state model;
- cancel authorization;
- secret/isolation;
- timeout/retry/cancel;
- idempotency/abuse/budget;
- Replay fallback;
- P1-3 proof contract;
- P3-3 handoff.

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

### not_required

- build
- DB/HTTP/browser runtime
- sandbox/network/secret runtime proof
- provider access
- deployment
- mirror sync

### forbidden

- implementation/runtime proof
- Git mutation
- provider/network/credential/deployment
- P1-3/P3-3 execution
- Human acceptance claim

## proof non-substitution

```text
fresh state_version
!= action admissible in that WorkflowState

profile allows tool
!= current WorkflowState allows execution

run visibility
!= cancel authority

run_id knowledge
!= target-run authorization

cancel intent admitted
!= WorkflowState mutated

security design
!= runtime safeguard proof
```

## workflow expectation

- initial_state:
  `P1_2_REWORK_READY`
- expected_terminal_candidate:
  `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- Agent may decide Human acceptance:
  `No`

## accept 기준

- predecessor design strengths retained;
- exact state/action admission model;
- normal execution side effects cannot occur outside semantically valid state;
- stale capability cannot survive relevant state/version changes;
- terminal states cannot start/continue normal execution side effects;
- safety cleanup/recovery remains possible through explicit System action class;
- exact public cancel target authorization;
- cross-session/run cancellation denied;
- cancel remains idempotent and non-state-mutating;
- P1-3 proof handoff covers both corrections;
- no P1-1 semantic regression;
- no implementation/scope creep;
- Human review pending.

## hold/reject 기준

- state/version freshness still used without state/action eligibility;
- tool/provider capability remains usable after terminal transition;
- public run ID or read access can imply cancel authority;
- cancel target ownership remains implementation-defined;
- security decision directly mutates WorkflowState;
- P1-1 state set changed;
- previous deny/secret/isolation/budget/fallback design regresses;
- P1-3 proof contract omits the corrected risks;
- forbidden action executed.

## 보고서 필수 항목

- task/repository snapshot;
- exact read inventory;
- predecessor HOLD mapping;
- selected action-class model;
- exact action×WorkflowState eligibility table;
- capability state/version transition semantics;
- public cancel authorization model;
- trust-crossing before/after summary;
- affected P1-3 proof additions;
- preserved predecessor design scope;
- evidence classifications;
- forbidden-not-run;
- Human pending;
- document integrity;
- rollback;
- preserved exact paths;
- next recommendation: Human P1-2 review if candidate passes.

## export bundle

Target:

```text
.aiassistant/reports/target/20260827_1247_aiscc-p1-2-security-action-state-and-public-cancel-authorization-alignment-rework-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`

## Task lifecycle

```text
.aiassistant/tasks/active/20260827_1247_aiscc-p1-2-security-action-state-and-public-cancel-authorization-alignment-rework-1.md
→
.aiassistant/tasks/done/20260827_1247_aiscc-p1-2-security-action-state-and-public-cancel-authorization-alignment-rework-1.md
```

`done` means Executor submission ready, not Human accepted.

## preserved artifacts

Preserve:

- `.aiassistant/tasks/done/20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1.md`
- `.aiassistant/records/aiscc/cycles/20260827_1247_aiscc-p1-2-security-action-state-and-cancel-authorization-hold-1.cycle.md`
- this rework done Task after execution
- eventual terminal P1-2 Cycle
- `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md` only as accepted baseline after Human acceptance

## next action

Corrected candidate
→ Command Center judgment
→ Human P1-2 final review.

P1-3 remains blocked until P1-2 `ACCEPTED / CLOSED`.
