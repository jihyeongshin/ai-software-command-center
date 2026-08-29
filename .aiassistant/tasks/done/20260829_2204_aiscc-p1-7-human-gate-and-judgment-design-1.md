# 작업지시서: P1-7 Human Gate and Judgment Design

## meta

- task_id: `20260829_2204_aiscc-p1-7-human-gate-and-judgment-design-1`
- created_at: `2026-08-29T22:04:00+09:00`
- phase: `P1-7 Human Gate and Judgment`
- work_type: `DESIGN_AUDIT / DOC_BASELINE_UPDATE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1-7_HUMAN_JUDGMENT`
- expected_start_head: `fc30aa3151494e15b132f8c48be8ca2c1bf8855d`
- predecessor_phase: `P1-6 Evidence Admission`
- predecessor_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- p1_7_runtime_status: `NOT_STARTED`
- p1_8_status: `NOT_STARTED`
- public_bounded_live_release: `NOT_RELEASED`

---

# 1. 현재 상태

P1-6 terminal provenance correction까지 완료되었다.

Expected Git lineage:

```text
P1-6 design terminal:
192e223854a02293809cf6675e3a329e099e628d

P1-6 runtime acceptance:
f36f19f5b84cef9bc1452e7cb9e9e36c4ae2873e

P1-6 terminal governance:
d80e61f65b048f3d555192ec3a13d296945feb52

P1-6 terminal provenance correction:
fc30aa3151494e15b132f8c48be8ca2c1bf8855d
```

Current phase state:

```text
P1-5 Provider / Tool Execution
→ ACCEPTED / CLOSED

P1-6 Evidence Admission Design
→ ACCEPTED / CLOSED

P1-6 Evidence Admission Runtime
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-7 Human Gate and Judgment
→ NOT_STARTED / CURRENT NEXT PHASE

P1-8 Project Memory and Cycle Admission
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

This Task starts P1-7 **design only**.

No P1-7 runtime/source implementation is allowed.

---

# 2. predecessor authority — do not weaken

P1-4 and P1-6 are frozen predecessors.

The following invariants are load-bearing:

```text
AGENT_OUTPUT != SYSTEM_STATE
AGENT_CLAIM != ADMITTED_EVIDENCE
HUMAN_OWNED_EVIDENCE != EXECUTOR_COMPLETED

ExecutionStatus != WorkflowState

EvidenceCandidate != AdmittedEvidence
AdmittedEvidence != Judgment
AdmittedEvidence != TransitionDecision
AdmittedEvidence != WorkflowState

HumanResult != Judgment

SecurityAdmissionDecision != TransitionDecision
RuntimeMode != WorkflowState
```

Terminal authority:

```text
TERMINAL_TRANSITION
→ SYSTEM_ADMISSION
→ HUMAN_GATE_WHEN_REQUIRED
```

P1-6 ownership:

```text
P1-6
→ exact G_EVIDENCE fact / EvidenceSetSatisfactionAttestation only

P1-6 MUST NOT mint:
G_HUMAN_*
G_JUDGMENT_*
TransitionDecision
WorkflowState
```

P1-7 MUST preserve:

```text
HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7

Human direct evidence != HumanGate

Human direct evidence != HumanResult

HumanResult != Judgment

Judgment != TransitionDecision

G_EVIDENCE != G_HUMAN_* != G_JUDGMENT_*
```

Do not invent a shortcut that lets HumanResult, Judgment, or an Agent directly mutate WorkflowState.

---

# 3. P1-4 frozen workflow boundary

Exact `WorkflowState` set remains frozen:

```text
READY
RUNNING
ADMISSION_PENDING
HUMAN_REQUIRED
BLOCKED
REWORK_REQUIRED
ACCEPTED
REJECTED
FAILED
```

Exact transitions relevant to P1-7 include at least:

```text
ADMISSION_PENDING → HUMAN_REQUIRED

HUMAN_REQUIRED → ACCEPTED
HUMAN_REQUIRED → REWORK_REQUIRED
HUMAN_REQUIRED → REJECTED
HUMAN_REQUIRED → BLOCKED

BLOCKED → HUMAN_REQUIRED
BLOCKED → REWORK_REQUIRED
BLOCKED → FAILED

REWORK_REQUIRED → READY
REWORK_REQUIRED → HUMAN_REQUIRED
REWORK_REQUIRED → REJECTED
```

The Task MUST read the actual accepted P1-4 orchestration contract/source and use its **exact guard IDs, guard owners, transition-purpose identities, state-version semantics, and transition request contract**.

Do not infer or rename exact P1-4 guard vocabulary from this Task.

If the accepted P1-4 source does not define enough guard ownership for P1-7:

```text
STOP
→ POLICY_BASELINE_GAP
```

and report the exact missing contract instead of inventing it.

---

# 4. 이번 턴 목표

Produce a Human-reviewable P1-7 design candidate that freezes the authority model for:

```text
HumanGate
Human principal / operator authority
HumanResult
Human-owned P1-7 evidence production
Judgment
G_HUMAN_*
G_JUDGMENT_*
P1-4 transition handoff
durable persistence / replay / concurrency / stale-result rejection
```

The design must be complete enough that a later implementation Task can be issued without silently choosing core authority semantics.

Expected canonical design candidate path:

```text
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md
```

This path becomes an accepted canonical authority only after later Human final design review.

During this Task its document status must explicitly say:

```text
DESIGN_CANDIDATE / HUMAN_REVIEW_PENDING
```

Do not mark it `ACCEPTED`.

---

# 5. 이번 턴 비목표

- P1-7 runtime implementation
- database migration
- `src/aiscc/human/**` creation
- `src/aiscc/judgment/**` creation
- P1-8 Project Memory implementation/design expansion
- WorkflowState additions/removals/renames
- transition graph changes
- P1-6 evidence semantics changes
- P1-5 provider/tool redesign
- public UI
- browser/runtime Human action execution
- actual authentication provider integration
- deployment
- PUBLIC_BOUNDED_LIVE release
- real provider calls
- credentialed external actions
- generic RBAC/enterprise IAM design unrelated to P1-7
- LLM-as-judge becoming authoritative judgment
- Agent-generated approval replacing Human result

---

# 6. design question set — must resolve

The design candidate MUST resolve the following questions explicitly.

## 6.1 HumanGate identity and authority

Define exactly:

```text
what creates/opens a HumanGate
who owns the gate
what immutable identity/version it has
what WorkflowState/state_version it binds to
what transition-purpose/checkpoint/request it binds to
what TaskContract/work_run it binds to
what required Human authority/policy it binds to
what closes/cancels/supersedes/expires it
whether one WorkRun/state_version may have multiple gates
whether multiple gates may be conjunctive/disjunctive
```

Required invariant:

```text
HumanGate
!= arbitrary caller metadata
!= chat prompt
!= boolean "human_required"
!= HumanResult
!= Judgment
```

The System must own gate identity.

If multiple-gate semantics are not needed for V1, explicitly freeze:

```text
V1 single-gate-per-transition-purpose
```

or another exact bounded rule.

Do not leave multiplicity implicit.

## 6.2 Human principal / operator authority

Define how a Human action proves identity/authority.

At minimum distinguish:

```text
authenticated Human principal identity

server-issued Human action authority / gate authority

caller-provided display name/text

Agent-provided "human approved" claim
```

Required:

```text
caller boolean/text
!= authenticated Human authority

Agent says Human approved
!= HumanResult

Human principal identity
must be server/system-authenticated
```

This design may define an abstraction/port for authentication without implementing an external identity provider.

Exact authentication technology is deferred unless already frozen elsewhere.

## 6.3 HumanResult

Define exact HumanResult domain semantics.

Must resolve:

```text
HumanResult id/version
Human principal
HumanGate ref/version
TaskContract/work_run
source WorkflowState/state_version
transition-purpose
result kind
structured reason/comment policy
created_at
idempotency fingerprint
supersession/correction rules
```

Define exact V1 result vocabulary.

The result vocabulary MUST be derived from actual P1-4 transition purposes and P1-7 authority needs.

Do not invent free-form terminal state mutation.

Required:

```text
HumanResult
!= Judgment

HumanResult
!= TransitionDecision

HumanResult
!= WorkflowState

HumanResult
!= automatically admitted Human evidence
```

## 6.4 HUMAN_P1_7 evidence producer

P1-6 already freezes two Human producer categories:

```text
HUMAN_DIRECT_EVIDENCE
HUMAN_P1_7
```

P1-7 design MUST define:

```text
what exact P1-7 object/event produces HUMAN_P1_7 evidence candidate
how producer authenticity is proven
how TaskContract/work_run/checkpoint/type/subject/resource/content are bound
how the candidate is handed to P1-6
how P1-6 admission remains authoritative
what happens when P1-6 rejects P1-7-produced Human evidence
```

Required:

```text
P1-7 HumanResult
→ may produce HUMAN_P1_7 evidence candidate

but

HumanResult
!= AdmittedEvidence

HUMAN_P1_7 producer ref
!= AdmittedEvidence

P1-6 admission
remains mandatory when TaskContract requires Human-owned evidence
```

A `HUMAN_DIRECT_EVIDENCE` item MUST NOT silently substitute for a requirement that explicitly requires `HUMAN_P1_7`.

## 6.5 Judgment

Define Judgment as a separate System-owned semantic object.

Must resolve:

```text
Judgment id/version
judgment authority version
TaskContract/work_run
source WorkflowState/state_version
HumanGate/HumanResult refs when applicable
P1-6 admitted evidence / G_EVIDENCE refs
policy/guard inputs
judgment kind
reason taxonomy
issued_at
supersession/correction
```

Required invariant:

```text
Agent review/proposal
!= Judgment

HumanResult
!= Judgment

AdmittedEvidence
!= Judgment

LLM confidence
!= Judgment

Judgment
!= TransitionDecision
```

The design must explicitly say whether Judgment is:

```text
deterministic System evaluation
```

or whether a non-authoritative Agent/LLM proposal may be an input.

If Agent/LLM proposal is allowed:

```text
proposal
→ non-authoritative input only
→ must never mint G_JUDGMENT_* directly
```

## 6.6 G_HUMAN_* owner-bound authority

Read exact P1-4 guard IDs first.

Design exact Human guard attestations/facts only for existing P1-4 owner slots.

At minimum every Human guard authority must bind:

```text
guard attestation id/version
P1-7 authority version
TaskContract id/version
work_run_id
source WorkflowState/state_version
HumanGate id/version
transition-purpose / target-use identity
Human principal/result ref
current gate/result authority revision
issued_at / expiry if applicable
```

Must reject:

```text
wrong TaskContract
wrong WorkRun
wrong state/version
wrong gate
wrong transition-purpose
wrong principal/result
stale/superseded HumanResult
closed/cancelled/expired wrong gate state
wrong P1-7 authority version
```

A Human guard fact for one gate or transition-purpose MUST NOT satisfy another.

## 6.7 G_JUDGMENT_* owner-bound authority

Read exact P1-4 guard IDs first.

Design exact Judgment attestations/facts only for existing P1-4 owner slots.

At minimum bind:

```text
judgment attestation id/version
P1-7 authority version
TaskContract id/version
work_run_id
source WorkflowState/state_version
transition-purpose / target-use identity
Judgment id/version
HumanGate/HumanResult refs when applicable
G_EVIDENCE ref/root when applicable
current authority revision
issued_at / expiry if applicable
```

Must reject:

```text
wrong TaskContract
wrong WorkRun
wrong state/version
wrong transition-purpose
stale/superseded Judgment
stale HumanResult/gate
stale G_EVIDENCE when Judgment depends on it
wrong authority version
```

Required:

```text
Judgment object
!= G_JUDGMENT_* guard fact

G_JUDGMENT_* guard fact
!= TransitionDecision
```

## 6.8 transition handoff

Define exact P1-4 integration.

Required chain must remain equivalent to:

```text
P1-7 current Human/Judgment authority
→ exact P1-4 guard facts
→ P1-4 transition request/verifier
→ TransitionDecision
→ WorkflowState mutation by System-owned transition engine/persistence
```

Forbidden:

```text
HumanResult.save()
→ directly update WorkflowState

Judgment.save()
→ directly update WorkflowState

P1-7 service
→ bypass P1-4 TransitionEngine
```

## 6.9 pre-Human / post-Human evidence non-deadlock

Preserve accepted P1-6 checkpoint semantics.

Design the sequence for a Human-required path:

```text
PRE_HUMAN checkpoint
→ applicable non-Human evidence satisfied
→ G_EVIDENCE(PRE_HUMAN)
→ P1-4 may enter HUMAN_REQUIRED

HumanGate
→ HumanResult

HumanResult / P1-7 producer
→ HUMAN_P1_7 candidate when required

P1-6 POST_HUMAN checkpoint
→ Human-owned evidence admission

Judgment
→ exact G_JUDGMENT_*

P1-4
→ terminal/rework/block transition
```

Do not create a cycle where:

```text
HumanGate cannot open until post-Human evidence exists
while
post-Human evidence cannot exist until HumanGate opens
```

If a transition does not require post-Human P1-6 evidence, say so explicitly.

## 6.10 judgment outcomes vs workflow outcomes

Design the mapping without collapsing layers.

Example principle:

```text
Judgment outcome
!= WorkflowState
```

The design must define exact V1 judgment kinds and which guard facts they can authorize.

Do not merely reuse state names unless the design explicitly proves why that does not collapse authority.

If judgment kinds resemble:

```text
ACCEPT
REWORK
REJECT
BLOCK
```

they still remain Judgment semantics, not WorkflowState values.

## 6.11 exception / override policy

Resolve whether V1 supports any Human policy exception/override.

If supported, define:

```text
what exact rule may be overridden
who can override
what cannot be overridden
how exception authority is persisted
how expiration/scope works
how Judgment consumes it
```

Load-bearing prohibition:

```text
Human override
MUST NOT bypass:
forbidden security boundary
identity/authenticity requirements
P1-4 terminal transition ownership
P1-6 evidence admission truth
```

If V1 does not need exception semantics:

```text
V1 policy exception / override:
NOT_SUPPORTED
```

Freeze that explicitly.

## 6.12 concurrency / idempotency / replay

Design must cover:

```text
duplicate gate-open request
duplicate HumanResult submit
same result id + different fingerprint
two Humans submit concurrently
gate already superseded/closed
state_version changed before result submit
Judgment concurrently evaluated
Judgment superseded after new HumanResult
old Human/Judgment guard replay
restart reconstruction
```

Required:

```text
same immutable request id + same fingerprint
→ same result

same id + different fingerprint
→ identity conflict

stale state_version
→ fail closed

old Human/Judgment guard
→ cannot satisfy new WorkRun/state_version/gate/authority version
```

The design must say what the authoritative winner rule is for concurrent Human results.

Do not leave this to ORM accident.

## 6.13 correction / supersession / revocation

Define append-only correction semantics.

At minimum:

```text
old HumanGate/Result/Judgment remains historical

correction
→ new immutable object/event

supersession/revocation
→ current authority changes
→ previously issued G_HUMAN_* / G_JUDGMENT_* becomes unusable
```

No in-place mutation of historical Human decisions.

## 6.14 persistence / restart

Expected direction:

```text
PostgreSQL
append-only provenance
deterministic restart reconstruction
```

Minimum durable concepts to evaluate/freeze:

```text
HumanGate / HumanGateRef
HumanGateAuthorityEvent

HumanResult / HumanResultRef
HumanResultAuthorityEvent

HumanP1_7EvidenceProducerRef

Judgment / JudgmentRef
JudgmentEvaluation
JudgmentAuthorityEvent

HumanGuardAttestation / exact equivalent
JudgmentGuardAttestation / exact equivalent
```

Exact names may differ, but the design must freeze semantic ownership and durable identity.

Restart must reconstruct:

```text
current gate
current HumanResult authority
current Judgment authority
which guard attestations remain effective
```

Corrupt/incomplete provenance:

```text
fail closed
no auto-repair
```

## 6.15 privacy / export

Human artifacts may contain comments/reasons.

Design sensitivity/export rules at least for:

```text
PUBLIC_SAFE
INTERNAL
PRIVATE_SENSITIVE
SECRET_FORBIDDEN
```

Required:

```text
Human comment text
!= automatically public provenance

authenticated principal internal identity
!= automatically public display identity

raw secret
→ forbidden

public Cycle/Replay
→ sanitized/minimal Human provenance only
```

P1-7 must not leak private operator identity merely to prove Human involvement.

---

# 7. exact design artifacts expected

Primary design candidate:

```text
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md
```

Document must be Korean-first and preserve code/state/guard identifiers exactly.

It must include at least:

```text
1. purpose / status
2. predecessor authority
3. non-substitution invariants
4. HumanGate model
5. Human principal authority
6. HumanResult model
7. HUMAN_P1_7 producer contract
8. Judgment model
9. G_HUMAN_* contract
10. G_JUDGMENT_* contract
11. P1-4 transition handoff
12. P1-6 post-Human evidence integration
13. outcome mapping
14. concurrency/idempotency/replay
15. correction/revocation/supersession
16. persistence/restart
17. security/privacy/export
18. rejection/failure taxonomy
19. implementation ownership
20. implementation proof matrix
21. non-goals
22. unresolved/open questions
23. Human design review questions
```

---

# 8. rejection / failure taxonomy design

The design must freeze durable sanitized reason categories for P1-7.

At minimum evaluate categories equivalent to:

```text
UNKNOWN_HUMAN_GATE
HUMAN_GATE_VERSION_MISMATCH
HUMAN_GATE_NOT_CURRENT
HUMAN_GATE_CLOSED
HUMAN_GATE_CANCELLED
HUMAN_GATE_EXPIRED

HUMAN_PRINCIPAL_NOT_AUTHORIZED
HUMAN_AUTHORITY_MISMATCH

TASK_CONTRACT_MISMATCH
WORK_RUN_MISMATCH
WORKFLOW_STATE_MISMATCH
STATE_VERSION_MISMATCH
TRANSITION_PURPOSE_MISMATCH

HUMAN_RESULT_IDENTITY_CONFLICT
HUMAN_RESULT_STALE
HUMAN_RESULT_SUPERSEDED

HUMAN_EVIDENCE_ADMISSION_REQUIRED
HUMAN_EVIDENCE_REJECTED

JUDGMENT_INPUT_INCOMPLETE
JUDGMENT_POLICY_MISMATCH
JUDGMENT_STALE
JUDGMENT_SUPERSEDED

GUARD_AUTHORITY_MISMATCH
GUARD_REPLAY_REJECTED

AUTHORITY_CONFLICT
PROVENANCE_INCOMPLETE
```

Do not blindly adopt these names if P1-4/P1-6 already own exact equivalent identifiers.

Avoid duplicate competing taxonomies.

---

# 9. design proof matrix for future implementation

The design candidate must end with a mandatory implementation proof matrix.

At minimum include:

```text
NON_SUBSTITUTION

HUMAN_GATE_AUTHORITY

HUMAN_PRINCIPAL_AUTHORITY

HUMAN_RESULT_IDEMPOTENCY

HUMAN_RESULT_STALENESS

HUMAN_P1_7_EVIDENCE_HANDOFF

POST_HUMAN_EVIDENCE_NON_DEADLOCK

JUDGMENT_AUTHORITY

G_HUMAN_BINDING

G_JUDGMENT_BINDING

P1_4_TRANSITION_HANDOFF

CONCURRENT_HUMAN_RESULT

CORRECTION_SUPERSESSION

GUARD_ANTI_REPLAY

RESTART

SECURITY_EXPORT
```

Mandatory future proof examples:

```text
Agent says "human approved"
→ no HumanResult

caller boolean `approved=true`
→ no Human authority

wrong Human principal
→ rejected

stale gate state_version
→ HumanResult rejected

same result id + same fingerprint
→ same immutable result

same result id + different fingerprint
→ identity conflict

two concurrent Human results
→ deterministic exact winner / loser behavior

HumanResult
→ not Judgment

HumanResult alone
→ not G_JUDGMENT_*

HUMAN_P1_7 producer ref
→ not AdmittedEvidence

P1-6 rejects Human evidence
→ post-Human requirement remains unsatisfied

post-Human evidence admitted
+ valid current HumanResult
+ exact policy inputs
→ Judgment may be issued

old HumanResult superseded
→ old G_HUMAN_* unusable

old Judgment superseded
→ old G_JUDGMENT_* unusable

new state_version
→ old Human/Judgment guards unusable

restart
→ current Human/Judgment authority reconstructed

HumanResult/Judgment persistence
→ no direct WorkflowState mutation
```

---

# 10. implementation ownership boundary to freeze

Expected future roots may include:

```text
src/aiscc/human/**
src/aiscc/judgment/**
```

or an equivalent bounded owner split.

The design must decide whether these are separate packages or one P1-7 package.

It must also identify narrow integration owners:

```text
src/aiscc/workflow/**
src/aiscc/evidence/**
src/aiscc/persistence/**
src/aiscc/contracts/**
```

but MUST NOT implement them in this Task.

P1-8 memory/cycle owner paths remain forbidden.

---

# 11. required source inspection

Before drafting, explicitly read:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/
20260829_1920_aiscc-p1-6-evidence-admission-runtime-final-acceptance-1.cycle.md
```

Then inspect exact current source necessary to understand:

```text
P1-4 guard IDs / owners / request-aware verifier contract
P1-4 Human-required transition guards
P1-4 WorkRun/state_version concurrency model
P1-6 HUMAN_P1_7 producer vocabulary
P1-6 checkpoint/post-Human requirement semantics
P1-6 EvidenceSetSatisfactionAttestation interface
```

Likely source roots:

```text
src/aiscc/workflow/**
src/aiscc/evidence/**
src/aiscc/persistence/**
src/aiscc/contracts/**
```

Read only exact files/symbols needed.

Do not bulk-read unrelated project source/logs.

---

# 12. design conflict rule

If actual accepted P1-4/P1-6 source contradicts this Task's assumptions:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Examples:

```text
P1-4 has no exact P1-7 guard owner slot
P1-4 guard vocabulary differs materially
P1-6 HUMAN_P1_7 semantics differ
post-Human checkpoint semantics cannot support proposed gate flow
```

Do not silently modify P1-4/P1-6 canonical rules.

Report exact conflict path/symbol and required predecessor design correction.

---

# 13. allowed paths

Primary design candidate:

```text
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md
```

Task lifecycle/report:

```text
.aiassistant/tasks/active/
20260829_2204_aiscc-p1-7-human-gate-and-judgment-design-1.md

.aiassistant/tasks/done/
20260829_2204_aiscc-p1-7-human-gate-and-judgment-design-1.md

.aiassistant/reports/target/
20260829_2204_aiscc-p1-7-human-gate-and-judgment-design-1/**
```

No other canonical file should change in this Task unless an exact design conflict requires a separate follow-up Task.

---

# 14. forbidden paths / actions

No mutation under:

```text
src/**
tests/**
migrations/**
```

Do not modify:

```text
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

in this design Task.

No:

```text
git add
git commit
git push
PR
deployment
provider call
credentialed external action
browser Human action
```

This design candidate remains uncommitted until Command Center/Human review directs persistence.

---

# 15. evidence contract

## executor_required

### STATIC_CANONICAL_INSPECTION

Scope:

```text
exact P1-4/P1-6 guard/authority/source integration points
```

Pass:

- exact identifiers recorded
- no invented guard owner
- no predecessor semantics weakened

### DESIGN_CONSISTENCY

Pass:

```text
HumanResult != Judgment
HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7
G_EVIDENCE != G_HUMAN_* != G_JUDGMENT_*
no direct WorkflowState mutation path
no pre/post-Human evidence deadlock
```

### DOCUMENT_VALIDATION

Pass:

```text
Korean-first
UTF-8
Markdown fences valid
no control-character corruption
git diff --check
no secret/private material
```

## reuse_allowed

Reuse accepted predecessor authority:

```text
P1-4 orchestration design/runtime
P1-6 evidence admission design/runtime
```

Only as read-only design inputs.

## human_owned

```text
P1-7 design final review
```

Expected after Executor completion:

```text
HUMAN_PENDING
```

## not_required

```text
unit tests
integration tests
PostgreSQL runtime
browser QA
HTTP runtime
provider call
deployment
```

## forbidden

```text
runtime implementation
Git commit
external credential/network
P1-8 work
```

## proof_non_substitution

```text
design document
!= runtime implementation

Agent design claim
!= Human design acceptance

HumanResult
!= Judgment

HumanResult
!= AdmittedEvidence

Judgment
!= TransitionDecision

P1-7 Human evidence producer
!= P1-6 admission
```

---

# 16. accept criteria — design candidate

Executor submission is reviewable only if:

```text
actual HEAD matched fc30aa3151494e15b132f8c48be8ca2c1bf8855d

P1-4 exact guard IDs/owner contracts were read from canonical/source

P1-6 HUMAN_P1_7/post-Human checkpoint semantics were read

AISCC_HUMAN_GATE_JUDGMENT.md created

document status = DESIGN_CANDIDATE / HUMAN_REVIEW_PENDING

HumanGate authority fully defined

Human principal authority fully defined

HumanResult vocabulary and idempotency/staleness defined

HUMAN_P1_7 producer handoff defined

Judgment authority defined

G_HUMAN_* exact owner-bound semantics defined

G_JUDGMENT_* exact owner-bound semantics defined

P1-4 transition handoff defined

pre/post-Human non-deadlock flow defined

concurrency/replay/correction/restart defined

privacy/export boundary defined

future proof matrix defined

no P1-7 runtime source created

no P1-8 work

no Git commit
```

---

# 17. hold/reject criteria

HOLD if any:

```text
exact P1-4 guard vocabulary unknown but design invents names

HumanResult collapses into Judgment

Judgment collapses into WorkflowState

HumanResult/Judgment directly mutates WorkflowState

Human direct evidence substitutes HUMAN_P1_7

P1-7 bypasses P1-6 evidence admission

Agent/LLM proposal can mint authoritative Judgment

Human identity is caller text/boolean

gate/result/judgment lacks TaskContract/work_run/state_version binding

old Human/Judgment guard replay not addressed

multiple-Human concurrency left implicit

post-Human evidence flow deadlocks

P1-7 design changes P1-4/P1-6 accepted semantics

P1-8 semantics mixed into P1-7

document marks itself ACCEPTED without Human review
```

---

# 18. mandatory stop

Stop on:

```text
HEAD drift
P1-4/P1-6 canonical conflict
missing required predecessor canonical/source
guard-owner baseline gap
unexpected dirty collision on design path
need for runtime evidence to decide authority semantics
```

After stop:

- gather minimal exact evidence
- produce report/export
- do not broaden into implementation

---

# 19. report requirements

`EXECUTOR_REPORT.md` must include:

1. task path
2. start HEAD
3. workspace before/after
4. exact canonical files read
5. exact P1-4 guard IDs/owners discovered
6. exact P1-4 transition-purpose bindings relevant to P1-7
7. exact P1-6 HUMAN_P1_7 semantics discovered
8. exact P1-6 pre/post-Human checkpoint semantics discovered
9. design decisions made
10. intentionally deferred decisions
11. unresolved questions
12. P1-4/P1-6 conflict result
13. product source changes: expected `none`
14. governance/provenance changes
15. repository config changes: expected `none`
16. evidence contract classifications
17. human verification: `HUMAN_PENDING`
18. UTF-8/Markdown/control-character result
19. secret/private scan
20. Git index/commit/push actions: expected `none`
21. preserved exact paths
22. next recommendation

---

# 20. export bundle

Target:

```text
.aiassistant/reports/target/
20260829_2204_aiscc-p1-7-human-gate-and-judgment-design-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md
```

Preserve repository-relative paths.

No source/test/runtime files should appear because this Task is design-only.

---

# 21. Task lifecycle

Start:

```text
.aiassistant/tasks/active/
20260829_2204_aiscc-p1-7-human-gate-and-judgment-design-1.md
```

After design/report/export is complete:

```text
.aiassistant/tasks/done/
20260829_2204_aiscc-p1-7-human-gate-and-judgment-design-1.md
```

`done` means:

```text
Executor design submission ready
```

It does NOT mean:

```text
P1-7 design ACCEPTED
P1-7 runtime started
```

---

# 22. preserved exact paths

Must survive cleanup after this Task:

```text
.aiassistant/tasks/done/
20260829_2204_aiscc-p1-7-human-gate-and-judgment-design-1.md

.aiassistant/rules/
AISCC_HUMAN_GATE_JUDGMENT.md
```

The target bundle is temporary review input and may be deleted after judgment unless later explicitly preserved.

All existing P1-6 terminal provenance remains preserved.

---

# 23. Human design review questions

The design candidate must end with a concise Human review section that asks only unresolved load-bearing decisions.

If the Executor can resolve an item directly from accepted P1-4/P1-6 authority, it MUST NOT ask the Human again.

Expected review axes include, only when not already determined:

```text
1. V1 HumanGate multiplicity
2. exact HumanResult vocabulary
3. whether V1 policy exception/override exists
4. concurrent multi-Human winner policy
5. whether Judgment may consume non-authoritative Agent proposal
6. public provenance identity/display policy
```

Do not ask broad preference questions.

---

# 24. final response format

1. result: `completed / blocked / rejected-candidate`
2. start HEAD
3. target bundle path
4. design candidate path
5. exact P1-4 guard/owner findings
6. exact P1-6 Human evidence/checkpoint findings
7. key design decisions
8. unresolved Human review questions
9. changed files
10. product source changes: expected `none`
11. Git actions: expected `none`
12. human verification: `HUMAN_PENDING`
13. preserved exact paths
14. next recommendation
