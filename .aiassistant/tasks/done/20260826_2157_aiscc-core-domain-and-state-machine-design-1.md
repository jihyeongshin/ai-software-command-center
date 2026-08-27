# 작업지시서: P1-1 Core Domain / State Machine Design

## meta

- task_id: `20260826_2157_aiscc-core-domain-and-state-machine-design-1`
- created_at: `2026-08-26 21:57 KST`
- phase: `P1-1 — Core Domain / State Machine Design`
- work_type: `DESIGN_AUDIT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `core domain model / explicit workflow state machine / transition authority semantics`
- predecessor_phase: `P0-5 First Project Source Mirror v1`
- predecessor_result: `ACCEPTED / CLOSED`
- predecessor_cycle: `.aiassistant/records/aiscc/cycles/20260826_2157_aiscc-p0-5-first-project-source-mirror-v1-terminal-closure-1.cycle.md`
- product_runtime_status_before: `NOT_IMPLEMENTED`
- architecture_owner_before: `NOT_YET_CREATED`
- orchestration_owner_before: `NOT_YET_CREATED`

## 현재 상태

Accepted baseline:

```text
AISCC
= Software Engineering Governance Control Plane
!= Coding Agent
```

Bootstrap status:

```text
P0-1 ACCEPTED / CLOSED
P0-2 ACCEPTED / CLOSED
P0-3 HUMAN_CONFIRMED / CLOSED
P0-4 ACCEPTED / CLOSED
P0-5 ACCEPTED / CLOSED
```

Current Browser Project Source:

```text
AI Software Command Center
AISCC-PROJECT-SOURCE-MIRROR-V1
active mirror files: 18
active Bootstrap Seed files: 0
mirror snapshot canonical commit:
0dc4e19a6da31c22e08d144eaba24209a4476b4d
```

Important snapshot rule:

The active Browser Project Source files were generated from the pre-sync canonical snapshot and may contain P0-5 pending text. The P0-5 terminal Cycle and current repository canonical state supersede that stale lifecycle snapshot. Do not reopen P0-5 merely because an uploaded mirror file contains pre-sync status.

Accepted orchestration decision:

```text
AISCC orchestration core
→ custom explicit state machine

LangGraph as orchestration core
→ NOT USED
```

Accepted authority invariants:

```text
AGENT_OUTPUT
!= SYSTEM_STATE

AGENT_CLAIM
!= ADMITTED_EVIDENCE

HUMAN_OWNED_EVIDENCE
!= EXECUTOR_COMPLETED

TERMINAL_TRANSITION
→ SYSTEM_ADMISSION
→ HUMAN_GATE_WHEN_REQUIRED
```

## 이번 턴 목표

P1-1은 implementation 전에 AISCC Core Domain과 explicit state machine의 semantic contract를 canonical baseline으로 만든다.

1. AISCC workflow의 **core domain concepts와 ownership boundary**를 exact하게 정의한다.
2. workflow state와 status taxonomy를 exact하게 정의한다.
3. state transition을 요청하는 actor와 transition을 admission하는 owner를 분리한다.
4. transition request / guard evaluation / admission / denial / human-required semantics를 정의한다.
5. terminal / non-terminal / blocked / failed / rework / human-required 의미를 서로 겹치지 않게 정의한다.
6. Agent output, evidence candidate, admitted evidence, judgment, Cycle, Next Action과 workflow state의 관계를 정의한다.
7. stale/concurrent transition request와 retry/rework의 domain-level semantics를 정의한다.
8. restart/recovery가 state truth를 잃지 않도록 **persistence semantics requirement**를 정의한다.
9. `OWNER_SELF_DOGFOOD`, `PUBLIC_RECORDED_REPLAY`, `PUBLIC_BOUNDED_LIVE` runtime mode와 workflow state를 동일 dimension으로 섞지 않는 모델을 정의한다.
10. future P1-2/P1-3/P1-4/P1-6/P1-7/P1-8 owner boundary를 명확히 handoff한다.
11. 아래 두 canonical baseline candidate를 생성한다.

```text
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
```

## 이번 턴 비목표

- product/runtime source implementation
- state-machine code implementation
- persistence/database implementation
- API/controller/schema implementation
- frontend/UI implementation
- Agent provider/model selection
- tool execution adapter implementation
- detailed evidence admission implementation
- Human Gate UI/implementation
- Cycle persistence implementation
- security/sandbox safeguard design detail owned by P1-2
- security/runtime safeguard implementation owned by P1-3
- public deployment/provider configuration
- Cloudflare/Railway/OpenAI resource creation
- API key/credential/billing/spend-limit
- P2 scenario/replay implementation
- P3 release/submission
- prior-art audit reopening
- new novelty/uniqueness claim

## 허용 범위

### allowed_paths

Create or modify only:

```text
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/reports/target/20260826_2157_aiscc-core-domain-and-state-machine-design-1/**
.aiassistant/tasks/active/20260826_2157_aiscc-core-domain-and-state-machine-design-1.md
.aiassistant/tasks/done/20260826_2157_aiscc-core-domain-and-state-machine-design-1.md
```

The Task may read, but MUST NOT silently modify:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md
.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md
.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md
```

Command Center will own terminal Cycle and accepted-state record updates after Human review.

### allowed_actions

- exact canonical Markdown read
- local repository file inventory limited to Task-relevant `.aiassistant` paths
- create/update the two design baseline candidates
- Markdown/static integrity check
- `git status`
- `git diff -- <allowed design paths>`
- `git diff --check`
- local SHA-256
- target export generation
- move this Task active → done when executor-required work/report/export is complete

## 절대 금지

### forbidden_paths

- application/runtime source directories not explicitly created by this Task
- `.git/`
- `.idea/`
- `.aiassistant/project-sources/bundles/**`
- credential/private data path
- unrelated previous target bundles

### forbidden_actions

- `git add`
- `git commit`
- `git push`
- remote Git operation
- dependency installation
- network/provider calls
- browser runtime
- DB/runtime harness
- product code generation
- security sandbox implementation
- deployment
- credential/API key creation/read/print
- billing configuration
- Browser Project Source upload/replacement
- P1-2/P1-3 implementation
- Agent deciding a terminal project judgment

## 읽을 문서

Read these exact repository canonical paths before design work:

1. `.aiassistant/rules/AISCC_AGENTS.md`
2. `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
3. `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
4. `.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md`
5. `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
6. `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md`
7. `.aiassistant/records/command-center/NEXT_ACTION_SELECTION_RUBRIC.md`
8. `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
9. `.aiassistant/records/aiscc/DECISION_REGISTER.md`
10. `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
11. `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
12. `.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md`
13. `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
14. `.aiassistant/records/aiscc/cycles/20260826_2157_aiscc-p0-5-first-project-source-mirror-v1-terminal-closure-1.cycle.md`

This is the minimum authoritative context set.

Do not bulk-read all `tasks/done`, all Cycles, generated mirror bundles, or unrelated files.

## agent instruction transport / authority

- repository-root `AGENTS.md` is thin transport bootstrap, not policy authority.
- current Task File owns task-specific scope/evidence but cannot silently supersede accepted canonical decisions.
- repository canonical path is authority; Browser Project Source is a read-only mirror snapshot.
- P0-5 terminal Cycle/current repository canonical state overrides stale lifecycle wording embedded in the pre-sync mirror snapshot.
- auto-discovered instruction, Task, canonical rule, current file, accepted evidence conflict → STOP and report exact conflict.
- human-owned design acceptance cannot be claimed by Executor.

## design deliverable A — `AISCC_ARCHITECTURE.md`

Must define at minimum:

### 1. architecture scope

- AISCC product boundary
- governance control plane vs Coding Agent separation
- initial single-system/MVP architecture assumption
- what P1-1 owns vs future Tasks

### 2. core domain glossary

Define exact semantics and owner for at least:

- `Project`
- `TaskContract`
- `WorkRun` or selected canonical execution aggregate name
- `WorkflowState`
- `TransitionRequest`
- `TransitionAdmission` / `TransitionDecision`
- `EvidenceRequirementRef`
- `EvidenceCandidateRef`
- `AdmittedEvidenceRef`
- `HumanGate`
- `Judgment`
- `CycleRecord`
- `NextAction`

You may choose better canonical names, but each concept must have one semantic owner and aliases must not become competing terms.

### 3. aggregate / ownership boundaries

For each aggregate or authoritative record, state:

- semantic owner
- mutable by whom
- immutable/history semantics
- relation to system state
- relation to Agent output
- relation to Human decision
- future persistence owner

### 4. mode separation

Model these as runtime/execution context dimensions, not accidental workflow states:

```text
OWNER_SELF_DOGFOOD
PUBLIC_RECORDED_REPLAY
PUBLIC_BOUNDED_LIVE
```

Explain how mode affects permissions/runtime policy without letting it redefine workflow truth.

### 5. persistence semantics requirement

P1-1 MUST decide semantic requirements, not DB technology.

At minimum answer:

- what state must survive process restart;
- whether transition admission needs monotonic/versioned state;
- how stale concurrent transition requests are rejected;
- what history is append-only vs current projection;
- what identifiers are stable;
- what minimum provenance is required to reconstruct a transition.

Do not select PostgreSQL tables/schema in P1-1 unless absolutely needed to express a semantic invariant.

### 6. future owner handoff

Map:

- P1-2 Security/Sandbox/Runtime Boundary Design
- P1-3 safeguard implementation/verification
- P1-4 state machine kernel implementation
- P1-5 provider/tool execution
- P1-6 evidence admission
- P1-7 human gate/judgment
- P1-8 memory/cycle admission

## design deliverable B — `AISCC_ORCHESTRATION.md`

Must define at minimum:

### 1. state model

Propose one exact canonical state set.

For every state define:

- meaning
- terminal vs non-terminal
- who/what may request entry
- admissible predecessor states
- required abstract predicates
- allowed outgoing transitions
- whether Human input is required
- retry/rework meaning
- recovery meaning

Avoid state explosion.

Do not encode every evidence type, provider error, UI state, or deployment condition as a workflow state.

### 2. transition table

Provide an exact transition matrix/table containing at least:

- source state
- requested target state
- requester
- admission owner
- abstract guard
- admitted result
- denied result
- Human gate behavior when applicable
- provenance emitted

### 3. authority contract

Must preserve:

```text
Agent
→ MAY propose action / target / evidence candidate

Agent
→ MUST NOT directly mutate authoritative workflow state

System
→ owns transition admission and authoritative state mutation

Human
→ owns designated policy/business/verification gates

Terminal state
→ cannot be established from Agent prose alone
```

### 4. request vs admission

Model separately:

```text
TransitionRequest
TransitionEvaluation
TransitionAdmission / Denial
AuthoritativeStateMutation
```

An Agent saying “done” is not a transition admission event.

### 5. evidence interface boundary

P1-1 defines only the state machine’s dependency on evidence admission.

It MUST NOT pre-implement P1-6.

Specify:

- what abstract evidence predicate/result the transition engine consumes;
- what data must be provenance-linked;
- what `HUMAN_PENDING`, wrong-owner, wrong-proof-type, stale evidence imply for transition admission;
- evidence detail remains owned by P1-6.

### 6. Human gate boundary

Specify how:

- a transition becomes `human-required`;
- system waits without falsely completing;
- Human result is admitted;
- rejection/rework resumes;
- Human silence/absence is not success.

Detailed Human Gate implementation remains P1-7.

### 7. failure / blocked / rework semantics

Explicitly distinguish at least:

- execution failure
- missing required evidence
- policy/authority conflict
- Human required
- rejected judgment
- rework requested
- terminal accepted/completed outcome if such a state exists

The design may choose different canonical names, but semantic distinctions must remain observable.

### 8. concurrency / stale request contract

Define the domain rule for concurrent transition requests.

Required invariant:

```text
TRANSITION_REQUEST
MUST BE EVALUATED AGAINST
THE AUTHORITATIVE CURRENT STATE/VERSION

STALE_REQUEST
→ DENIED / RETRY-REQUIRED
→ MUST NOT SILENTLY OVERWRITE CURRENT STATE
```

Do not choose a database lock implementation yet.

### 9. deterministic/replayable transition trace

Define the minimum transition event fields needed to reconstruct why a state changed or was denied.

At minimum consider:

- run/task identifier
- source state
- requested target
- requester type
- authoritative state/version observed
- evaluated guard identifiers/results
- evidence/human refs
- admission/denial reason
- admitting owner
- timestamp
- resulting state/version

### 10. terminal semantics

If multiple terminal states exist, define them exactly.

A terminal state MUST NOT ambiguously combine:

- executor completion
- evidence sufficiency
- Human acceptance
- project-level closure

If the design uses separate `execution status`, `workflow state`, `judgment status`, or similar dimensions, define the reason and authoritative owner for each.

## required design questions

The report must answer explicitly:

1. What is the smallest state set that preserves AISCC authority/evidence semantics?
2. Is `HUMAN_REQUIRED` a workflow state, a gate state, or another dimension? Why?
3. Is `BLOCKED` terminal? Under what condition can it resume?
4. How are `FAILED`, `REJECTED`, and `REWORK_REQUIRED` distinguished?
5. What exactly constitutes “executor work completed” vs “system admitted terminal result”?
6. Where is the version/concurrency boundary?
7. What must be durable before P1-4 implementation starts?
8. Which decisions are intentionally deferred to P1-2/P1-6/P1-7/P1-8?
9. Which state-machine semantics are required for Self-Dogfooding later?
10. Which semantics are required so Recorded Replay can truthfully reconstruct a prior run?

## workflow transition expectation

- initial_state: `P1_1_DESIGN_READY`
- expected_non_terminal_state_when_human_pending: `HUMAN_REQUIRED`
- expected_terminal_candidate: `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING`
- transition_authority: `SYSTEM / COMMAND_CENTER`
- Agent can directly decide terminal accepted state: `No`

## evidence contract

### executor_required

#### channel: `STATIC_SOURCE`

scope:

- exact 14 canonical paths listed above

pass condition:

- read inventory recorded
- P0-5 terminal Cycle is read
- stale pre-sync snapshot wording is not mistaken for current project state
- accepted P0-2/P0 queue invariants preserved

#### channel: `CORE_DOMAIN_DESIGN`

scope:

- `AISCC_ARCHITECTURE.md`

pass condition:

- one semantic owner per core concept
- runtime mode vs workflow state separated
- authoritative mutable state vs immutable provenance differentiated
- persistence/concurrency semantics specified without premature infrastructure lock-in
- future owner boundaries explicit

#### channel: `STATE_MACHINE_DESIGN`

scope:

- `AISCC_ORCHESTRATION.md`

pass condition:

- exact finite state set
- exact transition matrix
- terminal/non-terminal semantics
- request/admission separation
- system-owned authoritative mutation
- Human gate semantics
- stale transition semantics
- failure/blocked/rework semantics
- minimum deterministic transition trace

#### channel: `CROSS_BASELINE_CONSISTENCY`

scope:

- Product Thesis
- Decision Register
- Competition Public Runtime Boundary
- P1 safeguard-before-release invariant

pass condition:

- no LangGraph core
- Agent never owns terminal state
- public/private runtime mode separation preserved
- P1-2/P1-3 security ownership not absorbed
- P1-6 evidence admission not prematurely implemented
- P1-7 Human Gate implementation not prematurely implemented

#### channel: `CLAIM_BOUNDARY`

scope:

- architecture/orchestration wording

pass condition:

- no world-first/unique/invention claim
- no prior-art primitive claimed as AISCC invention
- design target vs implemented capability clearly separated

#### channel: `DOCUMENT_INTEGRITY`

scope:

- two baseline candidates
- Task/report/export

pass condition:

- UTF-8
- Markdown fence parity
- no unintended control chars
- no broken placeholder
- `git diff --check` or equivalent passes

### reuse_allowed

- P0-2 Product Thesis and runtime/prior-art baselines:
  `REUSED_ACCEPTED`
- P0-4 canonical authority/Git rules:
  `REUSED_ACCEPTED`
- P0-5 terminal source mirror closure:
  `REUSED_ACCEPTED`

Applicability condition:

- only accepted semantic boundary/provenance may be reused;
- no historical Browser-chat judgment is authority by itself.

### human_owned

#### channel: `HUMAN_VERIFICATION`

scope:

Human must review:

- exact domain names/ownership
- exact state set
- terminal vs non-terminal definitions
- `HUMAN_REQUIRED` modeling
- blocked/failure/rework semantics
- transition table
- concurrency/stale-request semantics
- persistence/recovery semantic contract
- future owner handoff

expected result:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

### not_required

- build
- unit test
- integration test
- database runtime
- HTTP runtime
- browser runtime
- security sandbox runtime
- provider/model execution
- deployment
- Project Source mirror refresh

Reason:

P1-1 is a design baseline Task and implements no runtime.

### forbidden

- runtime/product implementation
- security safeguard implementation
- provider/network/credential action
- Git index/commit/push
- Browser Project Source mutation
- P1-2/P1-3 execution

## proof non-substitution

```text
state diagram
!= implemented state machine

transition table
!= runtime transition proof

design review
!= security sandbox proof

Agent proposal
!= authoritative state

Agent "done"
!= terminal admission

evidence candidate
!= admitted evidence

HUMAN_PENDING
!= HUMAN_PROVIDED

P1-1 persistence semantics
!= database implementation

P1-1 security handoff
!= P1-2 design
!= P1-3 implementation/verification
```

## conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant:
  - `AISCC-ORCHESTRATION-CORE-V1`
  - `AISCC-PRODUCT-THESIS-V1`
  - `AISCC-COMPETITION-PUBLIC-RUNTIME-V1`
  - `AISCC-P1-SAFEGUARD-BEFORE-RELEASE-V1`
- required_actual_owner:
  `P1-1 design baseline`
- planned_vs_actual_scope:
  report exact deviations
- rollback_or_failure_semantics:
  candidate docs can be reverted without product/runtime rollback because implementation is forbidden

## project context impact

architecture:
- `UPDATE_REQUIRED`
- target owner: `.aiassistant/rules/AISCC_ARCHITECTURE.md`

orchestration_contract:
- `UPDATE_REQUIRED`
- target owner: `.aiassistant/rules/AISCC_ORCHESTRATION.md`

security_sandbox:
- `NONE / HANDOFF_TO_P1_2`
- P1-1 may identify required interface constraints but must not design the full safeguard implementation

public_provenance:
- `TASK_AND_CYCLE_ONLY + CANONICAL_BASELINE_CANDIDATES`

## mandatory stop 조건

Stop design/mutation after minimal evidence if:

- P0-5 terminal Cycle is missing
- repository canonical says P0-5 is not closed and no newer terminal Cycle exists
- Product Thesis / Decision Register / Current State conflict materially
- a state/transition authority decision requires Human policy choice before a coherent design is possible
- design would need P1-2 security details to proceed
- design would need runtime implementation or DB experiment
- unrelated dirty canonical collision
- private/company source or secret is encountered
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`

After named blocker:

- do not implement around the gap;
- report exact conflicting paths/statements;
- create minimal target report/export;
- stop safely.

## accept 기준

Command Center candidate may be accepted only if:

- two canonical design candidates exist
- state set is exact and finite
- each state has unambiguous semantics
- transition table is complete for intended MVP workflow
- Agent cannot mutate authoritative state
- terminal admission is System-owned
- Human-required result cannot auto-pass
- evidence candidate/admission/state remain separate
- blocked/failed/rework/rejected semantics are distinguishable
- stale concurrent transition requests cannot silently overwrite current state
- restart/recovery semantic requirements are explicit
- runtime mode and workflow state are separate
- P1-2/P1-3/P1-6/P1-7/P1-8 handoffs are explicit
- no premature implementation/infrastructure decision
- no forbidden action occurred
- Human review remains pending until actually provided

## hold/reject 기준

- vague prose without exact state/transition matrix
- Agent-owned next/terminal state
- `done` text directly becoming system state
- `HUMAN_REQUIRED` silently treated as success
- evidence validity embedded ad hoc into Agent prose instead of abstract admission boundary
- security design swallowed into P1-1
- no stale/concurrency semantics
- in-memory-only semantics accepted without recovery discussion
- state explosion mapping every tool/error/UI detail into core workflow state
- framework-first design that makes LangGraph/core framework the source of truth
- novelty/uniqueness overclaim
- implementation/source changes outside allowed paths
- Git/remote/provider/deployment action
- Human acceptance falsely claimed

## 보고서 필수 항목

- task/work type/task path
- repository HEAD/worktree before and after
- read canonical paths
- stale mirror snapshot vs current terminal Cycle handling
- created/modified design files
- core domain concept inventory
- aggregate/ownership table
- exact state inventory
- exact transition matrix
- terminal/non-terminal rationale
- Human-required design
- blocked/failed/rework/rejected rationale
- concurrency/stale request semantics
- persistence/recovery semantics
- runtime mode separation
- P1-2/P1-3/P1-4/P1-6/P1-7/P1-8 handoff
- design questions 1~10 answers
- evidence contract actual classifications
- forbidden-not-run
- mandatory stop/scope expansion
- document integrity
- unverified/open Human choices
- rollback/revert guide
- preserved exact paths
- next recommendation: P1-2 only after P1-1 Human acceptance

## export bundle 요구

Target:

```text
.aiassistant/reports/target/20260826_2157_aiscc-core-domain-and-state-machine-design-1/
```

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `.aiassistant/rules/AISCC_ARCHITECTURE.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`

No unchanged source export.

No generated Project Source bundle.

## Task lifecycle

When executor-required design/report/export is complete:

```text
.aiassistant/tasks/active/20260826_2157_aiscc-core-domain-and-state-machine-design-1.md
→
.aiassistant/tasks/done/20260826_2157_aiscc-core-domain-and-state-machine-design-1.md
```

`done` means executor submission ready, not Human accepted.

## 사람 검증 요구

Human review is mandatory before P1-1 terminal acceptance.

Review focus:

1. exact core domain names and semantic ownership
2. exact workflow state set
3. exact transition matrix
4. terminal semantics
5. Human gate semantics
6. stale/concurrency contract
7. persistence/recovery semantic requirement
8. owner handoff to later P1 stages

## preserved artifacts after acceptance

Expected preserve:

- `.aiassistant/tasks/done/20260826_2157_aiscc-core-domain-and-state-machine-design-1.md`
- `.aiassistant/records/aiscc/cycles/<P1-1-terminal-cycle>.cycle.md`
- `.aiassistant/rules/AISCC_ARCHITECTURE.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`

Temporary target bundle may be deleted after Command Center judgment unless explicitly preserved.

## next action after acceptance

```text
P1-2 Security / Sandbox / Runtime Boundary Design
```

Do not execute P1-2 in the same turn.
