# 작업지시서: P1-7 Design Terminal Persistence + Runtime Implementation / Verification

## meta

- task_id: `20260829_2328_aiscc-p1-7-design-terminal-persistence-and-runtime-implementation-1`
- created_at: `2026-08-29T23:28:00+09:00`
- phase: `P1-7 Human Gate and Judgment`
- work_type: `HUMAN_GATE_JUDGMENT_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT`
- expected_start_head: `fc30aa3151494e15b132f8c48be8ca2c1bf8855d`
- accepted_design_path: `.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md`
- accepted_design_sha256: `22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549`
- human_final_design_result: `HUMAN_PROVIDED / ACCEPTED`
- p1_6_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- p1_7_runtime_status: `NOT_STARTED`
- p1_8_status: `NOT_STARTED`
- public_bounded_live_release: `NOT_RELEASED`

---

# 1. Human terminal design decision

The following Human final result is authoritative for the exact accepted design candidate:

```text
Human P1-7 design final review
판정: ACCEPTED
```

Accepted design:

```text
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md
```

Accepted SHA-256:

```text
22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549
```

This acceptance applies only to that exact design byte identity.

Required:

```text
Human accepted design
!= Human accepted later modified design
```

Any design hash drift:

```text
STOP
→ REVIEWED_DESIGN_DRIFT
```

---

# 2. predecessor state

Expected repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Expected branch:

```text
main
```

Expected start HEAD:

```text
fc30aa3151494e15b132f8c48be8ca2c1bf8855d
```

Expected prior phase:

```text
P1-6 Evidence Admission Design
→ ACCEPTED / CLOSED

P1-6 Evidence Admission Runtime
→ ACCEPTED / CLOSED

P1-6 terminal provenance
→ COMPLETE
```

P1-7 design artifacts expected in the working tree / done lifecycle:

```text
.aiassistant/tasks/done/
20260829_2204_aiscc-p1-7-human-gate-and-judgment-design-1.md

.aiassistant/tasks/done/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-design-rework-1.md

.aiassistant/records/aiscc/cycles/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-hold-1.cycle.md

.aiassistant/rules/
AISCC_HUMAN_GATE_JUDGMENT.md
```

If actual predecessor provenance materially differs:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

---

# 3. load-bearing frozen invariants

Do not weaken:

```text
AGENT_OUTPUT != SYSTEM_STATE
AGENT_CLAIM != ADMITTED_EVIDENCE

EvidenceCandidate != AdmittedEvidence
AdmittedEvidence != Judgment
AdmittedEvidence != TransitionDecision
AdmittedEvidence != WorkflowState

HumanResult != Judgment
HumanResult != TransitionDecision
HumanResult != WorkflowState

Judgment != TransitionDecision
Judgment != WorkflowState

HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7

G_EVIDENCE != G_HUMAN_* != G_JUDGMENT_*

P1-6 owns:
exact EvidenceSetSatisfactionAttestation / G_EVIDENCE only

P1-7 owns:
exact Human/Judgment authority facts only

P1-4 owns:
TransitionDecision + WorkflowState mutation
```

Required transition chain:

```text
P1-6/P1-7 owner-bound authority
→ P1-4 guard verifier
→ P1-4 TransitionDecision
→ P1-4/System WorkflowState mutation
```

Forbidden:

```text
HumanResult.save()
→ WorkflowState update

Judgment.save()
→ WorkflowState update

P1-7 direct transition bypass
```

---

# 4. frozen accepted P1-7 design decisions

The implementation MUST read the accepted design and implement its exact identifiers.

At minimum the accepted design freezes these semantic decisions:

```text
HumanGate:
System-owned

V1 HumanGate multiplicity:
one current gate per HUMAN_REQUIRED authority epoch

HumanResultKind:
APPROVE
REWORK
REJECT

JudgmentKind:
ACCEPTED
REJECTED
HOLD_REWORK_REQUIRED

concurrent HumanResult winner:
FIRST_DURABLY_ADMITTED

policy exception / override:
NOT_SUPPORTED

Agent / LLM proposal:
non-authoritative provenance only

HUMAN_DIRECT_EVIDENCE:
cannot substitute HUMAN_P1_7

Human principal:
authenticated/server-owned authority

public Human identity:
sanitized projection only

PRE_HUMAN P1-6 evidence:
mandatory owner-backed input to G_HUMAN_REQUIRED

empty PRE_HUMAN applicable subset:
uses the same exact P1-6 SATISFIED attestation path

P1-4:
exclusive transition owner
```

Do not reconstruct exact guard IDs from this Task text.

The exact accepted design/canonical P1-4 source is authoritative for:

```text
G_HUMAN_* exact IDs
G_JUDGMENT_* exact IDs
guard owner slots
transition-purpose identities
target bindings
state/version semantics
```

If actual accepted identifiers conflict with implementation assumptions:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

---

# 5. overall Task structure

This Task has three stages.

```text
Stage 0A:
exact accepted P1-7 design persistence commit

Stage 0B:
P1-7 design terminal governance commit
+ terminal Cycle
+ canonical state

Stage 1:
P1-7 runtime implementation + verification
→ uncommitted review candidate
```

No Stage 1 source mutation before Stage 0A and Stage 0B both succeed.

---

# 6. Stage 0A — exact design persistence

## 6.1 preflight

Verify:

```text
HEAD ==
fc30aa3151494e15b132f8c48be8ca2c1bf8855d
```

Verify accepted design SHA:

```text
22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549
```

Verify exact design lineage artifacts exist.

Inventory unrelated dirty files.

Do not reset/clean unrelated files.

Forbidden:

```text
git add .
git add -A
```

## 6.2 Commit A allowlist

Commit only the exact accepted design and design-review lineage that is currently uncommitted:

```text
.aiassistant/rules/
AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/tasks/done/
20260829_2204_aiscc-p1-7-human-gate-and-judgment-design-1.md

.aiassistant/tasks/done/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-design-rework-1.md

.aiassistant/records/aiscc/cycles/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-hold-1.cycle.md
```

If any of these are already tracked at HEAD with exact accepted bytes, do not manufacture a diff.

No runtime source belongs in Commit A.

## 6.3 Commit A message

Recommended:

```text
docs(governance): persist accepted P1-7 human judgment design

Persist the Human-accepted P1-7 Human Gate and Judgment authority contract,
including the PRE_HUMAN evidence binding rework and its design-review provenance,
before any P1-7 runtime implementation begins.
```

Record exact hash:

```text
P1_7_DESIGN_ACCEPTANCE_COMMIT
```

---

# 7. Stage 0B — terminal design governance

After Commit A succeeds, create the terminal design Cycle.

Canonical path:

```text
.aiassistant/records/aiscc/cycles/
20260829_2328_aiscc-p1-7-human-gate-and-judgment-design-final-acceptance-1.cycle.md
```

The Cycle MUST bind:

```text
phase:
P1-7 Human Gate and Judgment Design

Human result:
HUMAN_PROVIDED / ACCEPTED

accepted design path:
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md

accepted design SHA-256:
22851cd0a6476fe613a3cc7a86a4096ace7236b4bafdd3c7c5a25e701a3b1549

design acceptance commit:
<exact Commit A hash>

predecessor HOLD:
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-hold-1.cycle.md

judgment:
P1-7 Design
→ ACCEPTED / CLOSED

P1-7 Runtime:
NOT_STARTED at terminal design judgment time

P1-8:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED

next action:
P1-7 Human Gate and Judgment Runtime Implementation + Verification
```

Do not put a placeholder in the terminal Cycle.

The Cycle is created only after Commit A hash exists.

---

# 8. Stage 0B canonical state updates

Update exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Required state after Stage 0B:

```text
P1-6 Evidence Admission
→ ACCEPTED / CLOSED

P1-7 Human Gate and Judgment Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-7 Human Gate and Judgment Runtime
→ NOT_STARTED

P1-8 Project Memory and Cycle Admission
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED

current next action:
P1-7 Runtime Implementation + Verification
```

The state files must not claim runtime capability already exists.

---

# 9. Stage 0B Git commit

Allowed paths:

```text
.aiassistant/records/aiscc/cycles/
20260829_2328_aiscc-p1-7-human-gate-and-judgment-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

No runtime/product source.

Recommended commit message:

```text
chore(governance): close P1-7 design and open runtime phase

Record the Human final acceptance of the P1-7 Human Gate and Judgment design,
bind the accepted design commit into terminal Cycle provenance, and advance the
canonical next action to P1-7 runtime implementation without starting P1-8.
```

Record exact hash:

```text
P1_7_DESIGN_TERMINAL_COMMIT
```

After Stage 0B succeeds, Stage 1 may begin.

---

# 10. Stage 1 — implementation scope

Implement the accepted P1-7 design exactly.

Expected primary ownership:

```text
src/aiscc/human/**
src/aiscc/judgment/**
```

or the exact package split frozen by the accepted design.

Narrow integration may touch:

```text
src/aiscc/workflow/**
src/aiscc/evidence/**
src/aiscc/persistence/**
src/aiscc/contracts/**
existing Alembic migration directory
```

Do not create P1-8 memory/cycle runtime ownership.

If actual accepted design freezes one combined P1-7 package rather than two packages, follow the accepted design.

Do not introduce a parallel duplicate architecture.

---

# 11. HumanGate runtime requirements

Implement exact System-owned gate identity/version/authority.

Must enforce:

```text
TaskContract id/version
work_run_id
source WorkflowState/state_version
transition-purpose / target-use
gate authority id/version/revision
gate status/lifecycle
current gate uniqueness rule
```

V1 multiplicity:

```text
one current gate per HUMAN_REQUIRED authority epoch
```

Opening a gate must require the accepted `G_HUMAN_REQUIRED` path.

Gate identity cannot come from:

```text
caller text
caller boolean
Agent claim
```

Gate lifecycle must be append-only or exact equivalent to accepted design.

---

# 12. PRE_HUMAN evidence → G_HUMAN_REQUIRED

This is load-bearing.

The future runtime must implement the accepted binding exactly.

Before `G_HUMAN_REQUIRED` may be effective:

```text
current P1-6 PRE_HUMAN checkpoint
current effective EvidenceSetSatisfactionAttestation
TaskContract/work_run/state/state_version exact match
transition-purpose/target-use exact match
RequirementSet root exact match
applicable-subset root exact match
evidence authority revision exact/current
P1-6 authority version exact/current
attestation not expired/revoked/superseded
```

Missing/stale/wrong:

```text
→ no G_HUMAN_REQUIRED
→ no gate open
→ no HUMAN_REQUIRED transition
```

Empty applicable subset:

```text
→ still exact P1-6 SATISFIED attestation required
→ no P1-7 no-evidence shortcut
```

Do not replicate P1-6 evidence evaluation in P1-7.

---

# 13. shared transition transaction boundary

Read the exact P1-4 and P1-6 current runtime implementation first.

For gate-open transition, preserve the accepted shared WorkRun authority boundary equivalent to:

```text
run:{work_run_id} advisory transaction lock
+ WorkRunRow FOR UPDATE
```

Required ordering:

```text
lock current WorkRun authority

→ verify current WorkRun TaskContract/state/state_version

→ resolve current P1-6 PRE_HUMAN authority

→ verify current G_HUMAN_REQUIRED input

→ P1-4 evaluate transition

→ if ADMITTED:
   gate-open durable event
   + WorkflowState HUMAN_REQUIRED / state_version increment
   atomically under accepted owner transaction
```

P1-7 MUST NOT perform the WorkflowState mutation independently.

If existing P1-4 API cannot atomically coordinate gate-open side effects without bypassing transition ownership:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

---

# 14. authenticated Human principal / action authority

Implement the accepted abstraction.

Must distinguish:

```text
authenticated Human principal

server-issued Human action authority

public/sanitized reviewer projection

caller-provided display text

Agent-provided "Human approved"
```

Forbidden:

```text
approved=true
human_name="..."
Agent says approved
```

as authentication.

Actual external identity provider integration is not required unless the accepted design explicitly requires it.

Local/system-owned test authentication authority is allowed for runtime verification.

---

# 15. HumanResult runtime

Implement immutable/durable HumanResult.

Exact accepted result vocabulary:

```text
APPROVE
REWORK
REJECT
```

Bind at minimum the exact accepted design fields:

```text
HumanResult id/version
HumanGate ref/version
authenticated Human principal/action authority
TaskContract id/version
work_run_id
source WorkflowState/state_version
transition-purpose
result kind
reason/comment according to policy
created_at
idempotency fingerprint
authority revision
supersession/correction relation
```

Required:

```text
HumanResult != Judgment
HumanResult != TransitionDecision
HumanResult != WorkflowState
```

Stale gate/state/version:

```text
→ reject
```

---

# 16. concurrent HumanResult rule

Implement exact V1 winner rule:

```text
FIRST_DURABLY_ADMITTED
```

Must prove:

```text
same result ID + same fingerprint
→ same immutable result

same ID + different fingerprint
→ identity conflict

two different Humans submit concurrently
→ exactly one current authoritative result wins
→ loser gets deterministic stale/conflict result
```

Do not rely on ORM accident.

Use PostgreSQL uniqueness/locking consistent with current WorkRun/gate authority.

---

# 17. HUMAN_P1_7 evidence handoff

Accepted chain:

```text
HumanResult / P1-7 producer authority
→ HUMAN_P1_7 EvidenceCandidate
→ P1-6 admission
→ AdmittedEvidence
```

Required:

```text
HumanResult
!= AdmittedEvidence

HUMAN_P1_7 producer ref
!= AdmittedEvidence

P1-7 cannot mark its own Human evidence admitted
```

If P1-6 rejects the candidate:

```text
post-Human requirement remains unsatisfied
Judgment path requiring that evidence cannot proceed
```

`HUMAN_DIRECT_EVIDENCE` cannot substitute an exact `HUMAN_P1_7` requirement.

---

# 18. Judgment runtime

Implement System-owned Judgment as separate authority.

Exact accepted vocabulary:

```text
ACCEPTED
REJECTED
HOLD_REWORK_REQUIRED
```

At minimum bind exact accepted semantics equivalent to:

```text
Judgment id/version
judgment authority version
TaskContract id/version
work_run_id
source WorkflowState/state_version
HumanGate ref
HumanResult ref
P1-6 post-Human evidence/G_EVIDENCE refs when required
policy/guard inputs
judgment kind
reason taxonomy
issued_at
authority revision
supersession/correction
```

Required:

```text
HumanResult != Judgment

Agent/LLM proposal != Judgment

Judgment != TransitionDecision

Judgment != WorkflowState
```

Agent/LLM proposal may be persisted only as non-authoritative provenance if accepted design allows it.

It must not mint Judgment or G_JUDGMENT_*.

---

# 19. post-Human P1-6 evidence integration

Preserve non-deadlock flow:

```text
PRE_HUMAN
→ G_EVIDENCE(PRE_HUMAN)
→ HumanGate open
→ HUMAN_REQUIRED

HumanResult
→ HUMAN_P1_7 evidence candidate when required

P1-6 POST_HUMAN checkpoint
→ Human-owned evidence admitted

Judgment
→ current exact G_JUDGMENT_*

P1-4
→ ACCEPTED / REWORK_REQUIRED / REJECTED / BLOCKED as exact guard contract allows
```

P1-7 must use P1-6 owner-backed current evidence authority.

Do not infer post-Human evidence truth from HumanResult alone.

---

# 20. G_HUMAN_* implementation

Read accepted design and P1-4 exact IDs.

Implement only existing exact guard slots owned by P1-7.

Every Human guard fact/attestation must bind at minimum:

```text
guard id/version
P1-7 authority version
TaskContract id/version
work_run_id
source WorkflowState/state_version
HumanGate id/version
transition-purpose / target-use
Human principal / HumanResult ref where applicable
current gate/result authority revision
issued_at / expiry if used
```

`G_HUMAN_REQUIRED` additionally binds exact PRE_HUMAN P1-6 evidence authority.

Wrong/stale/replayed authority:

```text
→ P1-4 guard verification reject
```

---

# 21. G_JUDGMENT_* implementation

Implement only exact accepted P1-4 judgment guard slots.

Bind at minimum:

```text
guard id/version
P1-7 authority version
TaskContract id/version
work_run_id
source WorkflowState/state_version
transition-purpose / target-use
Judgment id/version
current judgment authority revision
HumanGate/HumanResult refs when applicable
current P1-6 evidence/G_EVIDENCE authority when judgment depends on it
issued_at / expiry if used
```

Required:

```text
Judgment
!= G_JUDGMENT_*

G_JUDGMENT_*
!= TransitionDecision
```

Old/superseded Judgment or HumanResult:

```text
→ old guard unusable
```

---

# 22. correction / supersession / revocation

Use append-only provenance.

No in-place historical rewrite.

Required:

```text
old HumanGate remains historical
old HumanResult remains historical
old Judgment remains historical

correction
→ new immutable authority object/event
→ explicit relation

supersession/revocation
→ current authority revision advances
→ old G_HUMAN_* / G_JUDGMENT_* unusable
```

Restart must reconstruct current authority deterministically.

---

# 23. persistence

Expected:

```text
PostgreSQL
append-only
restart-durable
```

Implement exact durable concepts frozen by accepted design.

Likely equivalents:

```text
HumanGate
HumanGateAuthorityEvent

HumanResult
HumanResultAuthorityEvent

HumanP1_7EvidenceProducerRef

Judgment
JudgmentEvaluation
JudgmentAuthorityEvent

HumanGuardAttestation
JudgmentGuardAttestation
```

Do not introduce a second persistence framework.

Use existing SQLAlchemy/Alembic conventions.

Corrupt/incomplete provenance:

```text
fail closed
no auto repair
```

---

# 24. security / privacy / export

Implement accepted sensitivity/export rules.

At minimum:

```text
PUBLIC_SAFE
INTERNAL
PRIVATE_SENSITIVE
SECRET_FORBIDDEN
```

Required:

```text
raw secret
→ never Human/Judgment body

authenticated internal principal identity
→ not automatically public

Human comment/reason
→ not automatically public

public provenance
→ sanitized HUMAN_REVIEWER projection only
```

Do not leak session IDs, internal user IDs, auth tokens, private comments, or secrets through public Replay/Cycle/export.

---

# 25. V1 policy override

Accepted:

```text
policy exception / override:
NOT_SUPPORTED
```

Do not implement:

```text
force approve
admin override
manual evidence bypass
security override
judgment override
```

Human review does not override forbidden security/evidence/transition authority.

---

# 26. mandatory runtime proof matrix

Implement and verify at least:

```text
NON_SUBSTITUTION

HUMAN_GATE_AUTHORITY

PRE_HUMAN_EVIDENCE_GATE_BINDING

HUMAN_PRINCIPAL_AUTHORITY

HUMAN_RESULT_IDEMPOTENCY

HUMAN_RESULT_STALENESS

CONCURRENT_HUMAN_RESULT

HUMAN_P1_7_EVIDENCE_HANDOFF

POST_HUMAN_EVIDENCE_NON_DEADLOCK

JUDGMENT_AUTHORITY

G_HUMAN_BINDING

G_JUDGMENT_BINDING

P1_4_TRANSITION_HANDOFF

CORRECTION_SUPERSESSION

GUARD_ANTI_REPLAY

RESTART

SECURITY_EXPORT
```

---

# 27. mandatory proof examples

At minimum:

```text
Agent says "human approved"
→ no HumanResult

caller approved=true
→ no Human authority

wrong Human principal
→ rejected

missing PRE_HUMAN attestation
→ no G_HUMAN_REQUIRED
→ no gate
→ no HUMAN_REQUIRED transition

wrong/stale PRE_HUMAN checkpoint/root/revision/state/version
→ rejected

empty PRE_HUMAN applicable subset
→ valid exact P1-6 SATISFIED attestation still required

current exact PRE_HUMAN attestation
+ current gate reservation/policy
→ G_HUMAN_REQUIRED may be effective

stale gate state_version
→ HumanResult rejected

same HumanResult ID + same fingerprint
→ same immutable result

same HumanResult ID + different fingerprint
→ identity conflict

two Humans concurrent
→ FIRST_DURABLY_ADMITTED exact winner

HumanResult
→ not Judgment

HumanResult alone
→ not G_JUDGMENT_*

HUMAN_P1_7 producer ref
→ not AdmittedEvidence

P1-6 rejects HUMAN_P1_7 candidate
→ post-Human evidence remains unsatisfied

valid HumanResult
+ required post-Human evidence admitted
+ policy complete
→ Judgment may be issued

Agent/LLM proposal only
→ no authoritative Judgment

old HumanResult superseded
→ old G_HUMAN_* unusable

old Judgment superseded
→ old G_JUDGMENT_* unusable

new WorkRun state_version
→ old Human/Judgment guards unusable

restart
→ current gate/result/judgment/guard authority reconstructed

HumanResult/Judgment persistence
→ no direct WorkflowState mutation
```

---

# 28. transition race proofs

Use real PostgreSQL where load-bearing.

At minimum prove races equivalent to:

```text
gate-open vs WorkRun transition/state_version change

HumanResult submit vs gate supersession/closure

two concurrent HumanResult submissions

Judgment issue vs HumanResult supersession

P1-4 terminal/rework transition vs stale G_JUDGMENT_* reuse
```

Correctness must not depend on process-local locks.

Use shared accepted WorkRun/gate authority transaction ordering.

---

# 29. regression

After P1-7-specific proof:

Run directly affected accepted predecessor regression only.

Must cover:

```text
P1-4 workflow / guard / transition engine

P1-6 evidence admission
PRE_HUMAN / POST_HUMAN checkpoint authority
HUMAN_P1_7 admission boundary
WorkRun shared concurrency boundary

P1-5 only if shared persistence/runtime code is materially touched
```

Do not inflate pass counts with unrelated broad suites.

---

# 30. forbidden implementation scope

Do not create P1-8 ownership:

```text
src/aiscc/memory/**
project-memory authority
cycle-admission runtime
next-action memory runtime
```

Do not change:

```text
WorkflowState set
P1-4 transition graph
P1-6 evidence profile vocabulary
P1-6 accepted admission semantics
P1-5 provider execution semantics
```

No public UI/deployment/release.

---

# 31. Stage 1 Git policy

Runtime implementation remains a Command Center review candidate.

This Task authorizes:

```text
Stage 0A commit
Stage 0B commit
```

This Task does **not** authorize:

```text
Stage 1 runtime Git commit
git push
PR merge
tag/release
deployment
```

At executor completion:

```text
P1-7 runtime
→ HUMAN_PENDING
```

---

# 32. evidence contract

## executor_required

```text
STATIC_SOURCE

UNIT_TEST

POSTGRESQL_INTEGRATION

HUMAN_GATE_AUTHORITY

PRE_HUMAN_EVIDENCE_GATE_BINDING

HUMAN_PRINCIPAL_AUTHORITY

HUMAN_RESULT_IDEMPOTENCY

CONCURRENT_HUMAN_RESULT

HUMAN_P1_7_EVIDENCE_HANDOFF

POST_HUMAN_EVIDENCE_NON_DEADLOCK

JUDGMENT_AUTHORITY

G_HUMAN_BINDING

G_JUDGMENT_BINDING

P1_4_TRANSITION_HANDOFF

CONCURRENCY

RESTART

SECURITY_EXPORT

DIRECTLY_AFFECTED_REGRESSION
```

## reuse_allowed

Accepted predecessor proof may be reused only for unchanged behavior:

```text
P1-4 accepted workflow kernel/runtime
P1-6 accepted evidence runtime
P1-5 accepted runtime when untouched
```

No predecessor proof substitutes new P1-7 authority proof.

## human_owned

```text
P1-7 runtime final acceptance
```

Expected at Task end:

```text
HUMAN_PENDING
```

## not_required

```text
browser QA
frontend
real external IdP
real provider API
deployment
PUBLIC_BOUNDED_LIVE
production/test server
```

## forbidden

```text
P1-8 implementation
policy override
direct WorkflowState mutation
real provider call
credentialed external action
public Live enable
Stage 1 runtime commit
git push
deployment
```

---

# 33. allowed paths

## Stage 0A

```text
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/tasks/done/
20260829_2204_aiscc-p1-7-human-gate-and-judgment-design-1.md

.aiassistant/tasks/done/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-design-rework-1.md

.aiassistant/records/aiscc/cycles/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-hold-1.cycle.md
```

## Stage 0B

```text
.aiassistant/records/aiscc/cycles/
20260829_2328_aiscc-p1-7-human-gate-and-judgment-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

## Stage 1

Per accepted design:

```text
src/aiscc/human/**
src/aiscc/judgment/**
```

Narrow integration:

```text
src/aiscc/workflow/**
src/aiscc/evidence/**
src/aiscc/persistence/**
src/aiscc/contracts/**

existing migration directory

tests/unit/human/**
tests/unit/judgment/**
tests/integration/human/**
tests/integration/judgment/**

directly affected existing workflow/evidence tests
```

If accepted package names differ, use exact accepted design names.

---

# 34. mandatory stop conditions

Stop on:

```text
BLOCKED_PREDECESSOR_HEAD_DRIFT

REVIEWED_DESIGN_DRIFT

missing predecessor P1-7 design/rework artifact

P1-4/P1-6 canonical conflict

guard owner/ID mismatch

shared transaction boundary cannot preserve P1-4 transition ownership

P1-6 cannot provide exact PRE_HUMAN authority required by accepted design

external identity/provider credential required

P1-8 authority needed to proceed

unexpected unrelated dirty collision

secret/private material would enter public provenance
```

After stop:

- collect minimum blocker evidence
- do not broaden implementation
- do not create Stage 1 commit

---

# 35. report requirements

`EXECUTOR_REPORT.md` must include:

1. task path
2. start HEAD
3. accepted design SHA expected/actual
4. predecessor design/rework artifact verification
5. Stage 0A exact staged paths
6. Stage 0A commit hash
7. Stage 0A committed exact paths
8. terminal design Cycle path/content summary
9. Stage 0B canonical state changes
10. Stage 0B exact staged paths
11. Stage 0B commit hash
12. Stage 0B committed exact paths
13. exact P1-4 Human/Judgment guard IDs/owners implemented
14. exact HumanGate model/lifecycle
15. PRE_HUMAN evidence binding implementation
16. Human principal/action authority
17. HumanResult implementation
18. concurrent winner rule implementation
19. HUMAN_P1_7 evidence handoff
20. post-Human evidence flow
21. Judgment implementation
22. G_HUMAN_* implementation
23. G_JUDGMENT_* implementation
24. P1-4 transition handoff
25. persistence/migration changes
26. correction/supersession/revocation
27. security/privacy/export
28. mandatory proof matrix item-by-item
29. PostgreSQL version/runtime
30. concurrency proof
31. restart proof
32. regression commands/counts
33. real provider/network/credential actions
34. P1-8 source creation: expected `none`
35. Stage 1 Git commit: expected `none`
36. workspace after
37. human verification: `HUMAN_PENDING`
38. preserved exact paths
39. next recommendation

---

# 36. target bundle

Create:

```text
.aiassistant/reports/target/
20260829_2328_aiscc-p1-7-design-terminal-persistence-and-runtime-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include:

- Stage 0 changed governance/provenance files
- Stage 1 changed source/test/migration files
- preserve repository-relative paths
- `REMOVED_FILES.md` only if deletion exists

Do not include secrets/private auth material.

---

# 37. Task lifecycle

Start:

```text
.aiassistant/tasks/active/
20260829_2328_aiscc-p1-7-design-terminal-persistence-and-runtime-implementation-1.md
```

At executor turn completion:

```text
.aiassistant/tasks/done/
20260829_2328_aiscc-p1-7-design-terminal-persistence-and-runtime-implementation-1.md
```

The current Task done file is **not** included in Stage 0A/B commits.

It remains part of the uncommitted Stage 1 review provenance unless a later terminal runtime acceptance Task explicitly commits it.

`done` means:

```text
Executor submission ready
```

not:

```text
P1-7 Runtime ACCEPTED
```

---

# 38. final state after successful Executor turn

If Stage 0 and Stage 1 implementation/proof complete:

```text
P1-7 Design
→ ACCEPTED / CLOSED

P1-7 Runtime
→ IMPLEMENTED_CANDIDATE / HUMAN_PENDING

P1-8
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

Human/Command Center must review the runtime candidate before any runtime commit.

---

# 39. preserved exact paths

Must survive cleanup:

```text
.aiassistant/rules/
AISCC_HUMAN_GATE_JUDGMENT.md

.aiassistant/tasks/done/
20260829_2204_aiscc-p1-7-human-gate-and-judgment-design-1.md

.aiassistant/tasks/done/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-design-rework-1.md

.aiassistant/tasks/done/
20260829_2328_aiscc-p1-7-design-terminal-persistence-and-runtime-implementation-1.md

.aiassistant/records/aiscc/cycles/
20260829_2204_aiscc-p1-7-pre-human-evidence-gate-binding-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260829_2328_aiscc-p1-7-human-gate-and-judgment-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Existing P1-6 terminal artifacts remain preserved.

---

# 40. final response format

1. result
2. start HEAD
3. accepted design SHA
4. Stage 0A design commit
5. Stage 0B terminal governance commit
6. target bundle
7. Stage 1 changed files
8. exact P1-4 guard IDs/owners used
9. mandatory proof matrix summary
10. PostgreSQL/concurrency/restart summary
11. regression summary
12. provider/network/credential actions
13. P1-8 status
14. Stage 1 Git commit status = `none`
15. human verification = `HUMAN_PENDING`
16. preserved exact paths
17. next recommendation
