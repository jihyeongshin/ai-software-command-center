# 작업지시서: P1-6 Evidence Admission Contract Design Freeze with P1-5 Terminal Commit

## meta

- task_id: `20260828_2329_aiscc-p1-6-evidence-admission-contract-design-freeze-with-p1-5-terminal-commit-1`
- created_at: `2026-08-28 23:29 KST`
- phase: `P1-6 — Evidence Admission`
- work_type: `DESIGN_BASELINE`
- evidence_profile: `HIGH_RISK_DESIGN`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `EvidenceCandidate → AdmittedEvidence authority`
- predecessor_phase: `P1-5 Provider / Tool Execution Runtime`
- predecessor_result: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- predecessor_HEAD: `15036a5ff316fccbd6d891b9ce43563de056e342`
- P1_5_final_candidate_count: `42`
- P1_5_final_candidate_aggregate_sha256: `ffeb5ba70649c564c482c2cff79ce8e2b0a462f811d8e03f2c1096f170bd39d6`
- P1_6_status_before: `READY / DESIGN_FREEZE_REQUIRED`
- P1_7_status: `NOT_STARTED`

---

# 0. sole execution contract

This Task first persists the Human-accepted P1-5 runtime implementation and terminal canonical state.

After that one local commit, the same Executor turn performs **P1-6 design only**.

Do not implement Evidence Admission runtime/source in this Task.

The design result is `HUMAN_REVIEW_PENDING`.

---

# Stage 0 — exact P1-5 terminal implementation commit

## expected repository

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
15036a5ff316fccbd6d891b9ce43563de056e342
```

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

## exact accepted P1-5 runtime candidate

Before Git index mutation verify:

```text
candidate count:
42

aggregate SHA-256:
ffeb5ba70649c564c482c2cff79ce8e2b0a462f811d8e03f2c1096f170bd39d6
```

Exact 42 paths:

- `config/providers/provider-profiles.v1.toml`
- `config/providers/tool-registry.v1.toml`
- `config/security/permission-profiles.v1.toml`
- `config/security/resource-policy.v1.toml`
- `migrations/versions/20260828_0002_p1_5_provider_tool_execution.py`
- `pyproject.toml`
- `src/aiscc/contracts/security.py`
- `src/aiscc/persistence/__init__.py`
- `src/aiscc/persistence/models.py`
- `src/aiscc/persistence/repository.py`
- `src/aiscc/providers/__init__.py`
- `src/aiscc/providers/authority.py`
- `src/aiscc/providers/events.py`
- `src/aiscc/providers/models.py`
- `src/aiscc/providers/openai_responses.py`
- `src/aiscc/providers/ports.py`
- `src/aiscc/providers/profiles.py`
- `src/aiscc/providers/service.py`
- `src/aiscc/providers/tools.py`
- `src/aiscc/security/capability.py`
- `src/aiscc/security/policy.py`
- `src/aiscc/workflow/__init__.py`
- `src/aiscc/workflow/guards.py`
- `tests/conftest.py`
- `tests/fixtures/providers/fake_responses_server.py`
- `tests/fixtures/providers/recorded_replay.json`
- `tests/integration/providers/test_execution_persistence.py`
- `tests/integration/providers/test_secret_mediation.py`
- `tests/integration/providers/test_security_resource_authority.py`
- `tests/integration/providers/test_workflow_handoff.py`
- `tests/integration/workflow/test_postgres_kernel.py`
- `tests/runtime/providers/test_ambiguous_provider_failure.py`
- `tests/runtime/providers/test_final_residue.py`
- `tests/runtime/providers/test_mode_security.py`
- `tests/runtime/providers/test_replay_zero_execution.py`
- `tests/unit/providers/test_authority.py`
- `tests/unit/providers/test_models.py`
- `tests/unit/providers/test_openai_responses.py`
- `tests/unit/providers/test_operation_protocol.py`
- `tests/unit/providers/test_service.py`
- `tests/unit/providers/test_tools.py`
- `uv.lock`

Mismatch:

```text
STOP
→ BLOCKED_P1_5_ACCEPTED_CANDIDATE_DRIFT
```

Do not repair or reinterpret P1-5 source.

## exact terminal canonical files

Human placement must provide:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
sha256:
3425165c1e925b190a296a79952662d80df7405d4a5a2dbc8565393021a17bc7

.aiassistant/records/aiscc/DECISION_REGISTER.md
sha256:
568c5614e3f547695ceed3b9598640edd69660093fa7e8a4073ada2430c107c2

.aiassistant/records/aiscc/NEXT_ACTIONS.md
sha256:
79086e7717686cde3a4660828e51397bf40b4b8e7029edb4bf105183b4db6a58

.aiassistant/records/aiscc/cycles/20260828_2329_aiscc-p1-5-provider-tool-execution-runtime-final-acceptance-1.cycle.md
sha256:
ccfb755a7c8a3a30b530ec3720e7467be949d2010be3777d0f3a6b3bd8556f17

```

Verify exact SHA-256 before staging.

Mismatch:

```text
STOP
→ BLOCKED_P1_5_RUNTIME_TERMINAL_CANONICAL_MISMATCH
```

## exact Stage-0 commit universe

Maximum exact universe:

```text
42 accepted P1-5 candidate paths

.aiassistant/tasks/done/
20260828_2215_aiscc-p1-5-missing-provider-usage-token-accounting-rework-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/
20260828_2329_aiscc-p1-5-provider-tool-execution-runtime-final-acceptance-1.cycle.md
```

Maximum:

```text
47 paths
```

Already-clean allowed members are not blockers.
Every actually staged path must belong to this universe.

The active P1-6 Task and target report MUST NOT be staged.

Before staging:

```text
git status --short
git diff --check
```

Recompute the exact 42-path aggregate immediately before staging.

Required:

```text
ffeb5ba70649c564c482c2cff79ce8e2b0a462f811d8e03f2c1096f170bd39d6
```

Exactly one local commit is authorized.

Forbidden:

```text
git add .
git add -A
git commit -a
git amend
git reset
git rebase
git stash
git clean
git fetch
git pull
git push
branch/tag/remote mutation
```

Stage explicit actual changed paths only.

Exact commit message:

```text
feat: accept P1-5 provider tool execution runtime

Persist the Human-accepted P1-5 durable provider/tool execution runtime,
including bounded PostgreSQL execution authority, security mediation,
stateless continuation, and final token-accounting verification.

Commit the exact accepted 42-path candidate before P1-6 begins.
```

Use LF-safe UTF-8 message file + `git commit -F`.

After commit:

```text
P1_6_DESIGN_BASE_COMMIT=<full new hash>
```

Verify:

- parent == `15036a5ff316fccbd6d891b9ce43563de056e342`;
- every committed path is inside the exact 47-path universe;
- committed 42-path aggregate == `ffeb5ba70649c564c482c2cff79ce8e2b0a462f811d8e03f2c1096f170bd39d6`;
- exact multiline message;
- tracked worktree clean;
- index empty;
- no remote operation.

After Stage 0:

```text
git add / commit / push
→ FORBIDDEN
```

---

# Stage 1 — canonical read / owner preflight

Read:

1. `.aiassistant/rules/AISCC_ARCHITECTURE.md`
2. `.aiassistant/rules/AISCC_ORCHESTRATION.md`
3. `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
4. `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`
5. `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`
6. `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
7. `.aiassistant/records/aiscc/DECISION_REGISTER.md`
8. `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
9. `.aiassistant/records/aiscc/cycles/20260828_2329_aiscc-p1-5-provider-tool-execution-runtime-final-acceptance-1.cycle.md`

Inspect only relevant implementation boundaries:

```text
src/aiscc/providers/**
src/aiscc/workflow/**
src/aiscc/persistence/**
src/aiscc/security/**
src/aiscc/contracts/**
```

Do not modify product source.

---

# Stage 2 — create exactly one design candidate

Create:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
```

No other canonical rule.

It must be implementation-ready and exact enough that the next P1-6 runtime Task does not invent
load-bearing evidence authority semantics.

---

# Stage 3 — core evidence domain model

Freeze exact typed concepts at minimum equivalent to:

```text
EvidenceRequirement
EvidenceRequirementSet
EvidenceCandidate
EvidenceCandidateRef
EvidenceBodyRef / EvidenceContentRef
EvidenceAdmissionRequest
EvidenceEvaluation
EvidenceAdmissionDecision
AdmittedEvidence
AdmittedEvidenceRef
EvidenceSetEvaluation
EvidenceRejectionReason
EvidenceOwner / EvidenceSemanticOwner
```

Preserve exact non-substitution:

```text
AgentOutput != EvidenceCandidate
P1-5 producer ref != EvidenceCandidate admission
EvidenceCandidate != AdmittedEvidence
AdmittedEvidence != Judgment
AdmittedEvidence != TransitionDecision
AdmittedEvidence != WorkflowState
```

A candidate object/reference is never authoritative merely because it is typed or persisted.

---

# Stage 4 — exact EvidenceRequirement contract

Freeze versioned requirement identity.

At minimum each requirement must bind:

```text
requirement_id
requirement_version
task_contract_id
task_contract_version
requirement semantic owner
evidence classification/type
producer/issuer constraints
content/reference constraints
scope/applicability
freshness rule
coverage/completeness rule
reuse policy
sensitivity/export policy
required/optional/forbidden status
```

Requirement authority is server/System-owned.

Agent/Executor/public input cannot add, weaken or remove requirements.

A later requirement version cannot silently reinterpret already-admitted evidence under an older
Task Contract.

---

# Stage 5 — exact evidence profile semantics

Freeze the project vocabulary already used by Tasks:

```text
executor_required
reuse_allowed
human_owned
not_required
forbidden
```

Define each exactly.

Required minimum semantics:

### executor_required

```text
Task cannot satisfy the requirement without a P1-6-admitted candidate
from an allowed Executor/System producer.
```

Executor report text alone is not evidence unless the requirement explicitly allows that report
artifact/type and the exact content/provenance is admitted.

### reuse_allowed

Reuse is NOT automatic.

Freeze exact compatibility gates for reused admitted evidence:

```text
same semantic requirement
compatible Task Contract/version
same scope/subject/resource
allowed producer
freshness valid
content immutable/hash-identical
no revocation/supersession
reuse count/policy valid
```

A prior `AdmittedEvidenceRef` can be a candidate for reuse but must receive a new current-task
admission decision or exact reuse-admission event.

### human_owned

Executor may not satisfy it.

Only a P1-7/Human-result-compatible Human evidence producer may later submit the required candidate.

P1-6 may validate/admit Human-owned evidence provenance, but cannot fabricate Human action/result.

Before P1-7 exists, such a requirement remains unsatisfied unless Human evidence is explicitly
supplied through a Human-owned ingress defined by the design.

### not_required

No evidence item is necessary for the current Task/requirement.

Do not synthesize an `AdmittedEvidence` row solely to represent absence.

### forbidden

Candidate admission of the forbidden evidence type/source/scope must fail closed.

Forbidden evidence cannot become admissible merely because it is useful or already exists.

---

# Stage 6 — producer / issuer authority

Freeze exact producer categories and authority boundaries.

At minimum reconcile:

```text
P1-5 ExecutionSubmissionRef
AgentOutputRef
ToolOutputRef
ExecutionArtifactRef
System runtime/static/database proof
Human-provided evidence
reused prior AdmittedEvidenceRef
```

For every candidate define exact issuer identity/version and binding.

Required:

```text
raw path/string/URL/hash
!= trusted evidence producer

Executor claim
!= producer authority

file exists
!= content admitted

test says PASS
!= test evidence admitted
```

A candidate must bind at minimum:

```text
candidate_id
issuer type/id/version
producer run/attempt when applicable
Task Contract id/version
subject/scope/resource
evidence type
content/ref identity
content hash
created/observed time
sensitivity classification
```

P1-5 issuer-backed refs may seed candidates but do not become AdmittedEvidence automatically.

---

# Stage 7 — content / body / reference authority

Freeze how P1-6 proves what evidence actually says.

Support at least:

```text
immutable inline structured evidence body
content-addressed artifact/file/blob ref
P1-5 immutable producer ref
database/runtime observation ref
Human-provided structured ref
prior AdmittedEvidenceRef reuse candidate
```

Do not accept:

```text
unverified arbitrary local path
unverified arbitrary URL
mutable latest pointer
hash string without body/ref ownership
Executor summary without exact supporting body when the requirement requires raw proof
```

Content-addressed body/ref must verify:

```text
bytes/content
→ exact canonical hash
→ expected classification/schema/type
```

Private/sensitive body may remain private while an admitted immutable metadata/hash/reference is
durable.

Define what may appear in public/review export versus private evidence storage.

---

# Stage 8 — exact admission evaluation dimensions

Every candidate evaluation must make explicit decisions for at least:

```text
REQUIREMENT_MATCH
ISSUER_AUTHORITY
TYPE
TASK_CONTRACT_BINDING
SUBJECT_SCOPE
RESOURCE_BINDING
CONTENT_INTEGRITY
SCHEMA/FORMAT
FRESHNESS
APPLICABILITY
COVERAGE
SENSITIVITY_POLICY
REUSE_POLICY
REVOCATION/SUPERSESSION
DUPLICATE/IDEMPOTENCY
```

Unknown/ambiguous dimension:

```text
→ DENY / NOT_ADMITTED
```

No score/LLM confidence may substitute for these authority dimensions.

LLM/Agent semantic classification may propose metadata only unless a future Human-accepted P1-6
contract explicitly authorizes a bounded semantic verifier.

---

# Stage 9 — admission decision / reason taxonomy

Freeze exact decision states equivalent to:

```text
ADMITTED
REJECTED
```

Do not make `PENDING` an authoritative admission decision.

Pending candidate processing may be a separate workflow/projection status.

Freeze reason codes at minimum covering:

```text
UNKNOWN_REQUIREMENT
REQUIREMENT_VERSION_MISMATCH
FORBIDDEN_EVIDENCE
ISSUER_NOT_AUTHORIZED
TASK_CONTRACT_MISMATCH
SUBJECT_SCOPE_MISMATCH
RESOURCE_MISMATCH
TYPE_MISMATCH
CONTENT_MISSING
CONTENT_HASH_MISMATCH
SCHEMA_INVALID
STALE
NOT_APPLICABLE
INSUFFICIENT_COVERAGE
REUSE_NOT_ALLOWED
REUSE_INCOMPATIBLE
REVOKED_OR_SUPERSEDED
HUMAN_OWNED_REQUIRED
DUPLICATE_IDENTITY_CONFLICT
AUTHORITY_CONFLICT
```

Names may differ; semantics may not.

Reject reason must be durable and sanitized.

---

# Stage 10 — evidence set completeness

A single admitted item is not automatically `G_EVIDENCE`.

Freeze exact set-level evaluation:

```text
Task Contract
→ EvidenceRequirementSet

AdmittedEvidence items
→ map to exact requirements

EvidenceSetEvaluation
→ each required requirement SATISFIED or UNSATISFIED
```

`G_EVIDENCE` may be issued only when the exact current requirement set is satisfied.

Required:

```text
executor_required missing
→ set UNSATISFIED

human_owned missing
→ set UNSATISFIED

forbidden candidate present but rejected
→ does not itself satisfy anything

not_required
→ no row required

reuse_allowed
→ current-task reuse admission required
```

Optional evidence may be retained but does not create requirements.

Define whether one evidence item may satisfy multiple requirements.
If allowed, require exact per-requirement admission/coverage mapping and no hidden fan-out.

---

# Stage 11 — P1-4 owner-bound `G_EVIDENCE` handoff

P1-4 currently assigns:

```text
G_EVIDENCE
→ P1_6_EVIDENCE
```

Freeze the exact trusted fact/attestation P1-6 may issue.

It must bind at minimum:

```text
evidence-set evaluation id/version
Task Contract id/version
work_run_id
authoritative WorkflowState/state_version observed
exact EvidenceRequirementSet id/version
exact admitted-evidence refs/hash root
satisfied=true
issued_at/expiry if applicable
P1-6 authority version
```

P1-6 cannot mint:

```text
G_CURRENT
G_HUMAN_*
G_JUDGMENT_*
TransitionDecision
WorkflowState
```

P1-4 validates the owner-bound P1-6 fact before using `G_EVIDENCE`.

Raw admitted evidence refs without a current P1-6 set-satisfaction attestation do not satisfy
`G_EVIDENCE`.

---

# Stage 12 — concurrency / idempotency / anti-replay

Freeze optimistic/durable authority.

Admission request binds exact:

```text
candidate identity/fingerprint
requirement id/version
Task Contract id/version
work_run_id
current evidence requirement-set version
```

Same admission request ID + same fingerprint:

```text
→ immutable same decision
```

Same ID + different fingerprint:

```text
→ identity conflict
```

Concurrent admission of the same logical candidate:

```text
→ at most one authoritative admitted identity
```

Stale requirement set/version or Task Contract:

```text
→ DENY
```

Reusing an admitted ref under a new Task cannot replay the old set-satisfaction attestation.

---

# Stage 13 — persistence / append-only provenance

Freeze PostgreSQL direction consistent with P1-3/P1-4/P1-5.

Minimum durable entities:

```text
EvidenceRequirement / RequirementSet snapshot
EvidenceCandidate metadata/ref
EvidenceAdmissionRequest
EvidenceEvaluation
EvidenceAdmissionDecision
AdmittedEvidence
EvidenceRequirementSatisfaction mapping
EvidenceSetEvaluation
EvidenceSetSatisfactionAttestation
revocation/supersession/correction event
```

Admission/evaluation/decision provenance must be append-only.

An admitted evidence body/hash/ref identity cannot be mutated in place.

Corrections:

```text
old evidence remains historical
→ new candidate/admission
→ explicit supersession/correction relation
```

If an admitted item later becomes revoked/superseded, define how current set satisfaction is
invalidated/recomputed before a new `G_EVIDENCE` fact may be issued.

Restart must reconstruct authoritative current evidence state deterministically.

---

# Stage 14 — evidence freshness / applicability

Freeze freshness as requirement-owned policy, not a global timestamp rule.

Examples of policy categories may include:

```text
IMMUTABLE_BUILD_ARTIFACT
TASK_EXECUTION_SCOPED
WORKRUN_STATE_VERSION_SCOPED
TIME_WINDOW
CONFIG_VERSION_SCOPED
HUMAN_RESULT_SCOPED
```

Exact names may differ.

Required:

```text
fresh timestamp alone
!= fresh evidence

same bytes
!= applicable evidence if scope/version changed
```

Define evidence captured before/after a state-version change.

P1-6 must not treat a stale runtime observation as current simply because content is immutable.

---

# Stage 15 — Human-owned evidence handoff

Do not implement P1-7.

Design the boundary only.

Required:

```text
human_owned requirement
→ P1-6 cannot self-satisfy

Human ingress
→ exact Human producer/result reference
→ P1-6 evidence integrity/provenance admission
→ still does not equal Judgment
```

Preserve:

```text
HumanResult != Judgment
Human evidence != HumanResult unless explicitly the same typed Human-produced artifact
Admitted Human evidence != Judgment
```

P1-7 remains Human gate/result/Judgment owner.

---

# Stage 16 — security / sensitive evidence

Freeze evidence classifications at minimum sufficient to distinguish:

```text
PUBLIC_SAFE
INTERNAL
PRIVATE_SENSITIVE
SECRET_FORBIDDEN
```

Exact names may differ.

Raw secrets must never be admitted/exported as evidence body.

A secret proof should use:

```text
non-secret canary result
redacted metadata
hash/reference
non-exposure scan result
```

not the secret itself.

Evidence export/report must respect classification.

Public Replay must not expose private evidence payload simply because the run is visible.

---

# Stage 17 — evidence requirement examples

Include concrete exact examples in the canonical design for at least:

1. static/build proof;
2. PostgreSQL migration proof;
3. Docker/runtime security proof;
4. P1-5 producer `ExecutionSubmissionRef`;
5. reusable immutable artifact;
6. Human-owned final review;
7. forbidden raw secret;
8. stale runtime proof after state_version change.

For each show:

```text
requirement
candidate
evaluation
decision
set effect
G_EVIDENCE effect
```

Examples are normative only when explicitly marked as contract examples; do not let examples create
unlisted hidden rules.

---

# Stage 18 — implementation ownership / path contract

Freeze expected next implementation owner root:

```text
src/aiscc/evidence/
```

Expected categories:

```text
evidence models / ports
requirement-set registry/snapshot
candidate ingress
issuer verifiers
content/ref integrity verifier
admission evaluator/service
evidence set evaluator
P1-4 G_EVIDENCE attestation verifier handoff
PostgreSQL repository/models/migration
tests/config
```

P1-6 may narrowly modify existing:

```text
src/aiscc/workflow/**
src/aiscc/persistence/**
src/aiscc/contracts/**
```

only for the exact P1-6 handoff.

Do not create:

```text
src/aiscc/human/
src/aiscc/memory/
```

Those remain P1-7/P1-8.

---

# Stage 19 — implementation proof matrix

Freeze the next-task executable proof matrix.

At minimum:

## NON_SUBSTITUTION

- AgentOutputRef alone → not admitted;
- ExecutionSubmissionRef alone → not admitted;
- Executor report claim alone → not admitted unless exact requirement authorizes exact report body;
- raw path/hash/string → not admitted;
- AdmittedEvidenceRef alone → does not mint `G_EVIDENCE`.

## REQUIREMENT_MATCH

- unknown/version mismatch → reject;
- forbidden evidence → reject;
- not_required creates no required row;
- human_owned cannot be executor-satisfied.

## ISSUER / CONTENT

- forged issuer → reject;
- wrong run/attempt/task contract → reject;
- missing body/ref → reject;
- hash mismatch → reject;
- schema/type mismatch → reject.

## FRESHNESS / APPLICABILITY

- valid same-version proof → admit;
- state-version scoped proof after state change → stale/reject;
- immutable reusable artifact under compatible requirement → current-task reuse admission PASS;
- incompatible reuse → reject.

## SET_COMPLETENESS

- missing one required requirement → UNSATISFIED;
- all required exact requirements satisfied → SATISFIED;
- optional item does not alter required completeness;
- rejected forbidden evidence cannot satisfy anything.

## G_EVIDENCE

- raw evidence refs → P1-4 deny;
- current owner-bound P1-6 set-satisfaction attestation → P1-4 may satisfy `G_EVIDENCE`;
- stale/wrong task/run/state/version/requirement-set attestation → deny;
- P1-6 cannot mint other owners' guards.

## CONCURRENCY / IDEMPOTENCY

- duplicate exact admission request → same decision;
- conflicting duplicate → reject;
- concurrent same candidate → one authoritative admission;
- stale requirement-set version → reject.

## REVOCATION / SUPERSESSION

- admitted evidence remains historical;
- superseding/revoking current evidence invalidates current set satisfaction;
- old `G_EVIDENCE` attestation cannot be reused.

## RESTART

- requirements/candidates/decisions/admitted refs/set evaluation reconstruct identically;
- corruption/incomplete provenance fails closed;
- no auto repair.

## SECURITY / EXPORT

- SECRET_FORBIDDEN body rejected;
- private body absent from public export;
- non-secret proof metadata remains reviewable.

No P1-7 implementation is required for P1-6 implementation acceptance; use an exact fake/Human-owned
producer fixture only for the P1-6 boundary.

---

# evidence contract for this design Task

## executor_required

- `P1_5_TERMINAL_GIT`
- `P1_6_CANONICAL_READ`
- `EVIDENCE_DOMAIN_MODEL`
- `REQUIREMENT_PROFILE_SEMANTICS`
- `PRODUCER_ISSUER_AUTHORITY`
- `CONTENT_REFERENCE_AUTHORITY`
- `ADMISSION_EVALUATION_DIMENSIONS`
- `ADMISSION_REASON_TAXONOMY`
- `EVIDENCE_SET_COMPLETENESS`
- `G_EVIDENCE_HANDOFF`
- `CONCURRENCY_IDEMPOTENCY_ANTI_REPLAY`
- `PERSISTENCE_REVOCATION_SUPERSESSION`
- `FRESHNESS_APPLICABILITY`
- `HUMAN_OWNED_HANDOFF`
- `SENSITIVE_EVIDENCE_POLICY`
- `IMPLEMENTATION_PATH_OWNERSHIP`
- `IMPLEMENTATION_PROOF_MATRIX`

## human_owned

`HUMAN_VERIFICATION`

Human decides whether:

```text
AISCC_EVIDENCE_ADMISSION.md
→ ACCEPTED
```

## not_required

- product build;
- runtime tests;
- PostgreSQL migration;
- Docker;
- P1-7 Human implementation;
- external network;
- deployment.

Reason:

This Task is P1-6 design freeze after the P1-5 terminal commit.

## forbidden

- P1-6 runtime/source implementation;
- P1-7/P1-8 implementation;
- LLM semantic verifier implementation;
- external evidence-source connector/network;
- provider call;
- credential/secret access;
- public deployment;
- second Git commit after Stage 0;
- Git push/remote mutation;
- Browser Project Source mutation.

---

# proof non-substitution

```text
design accepted
!= P1-6 runtime implemented

EvidenceCandidate
!= AdmittedEvidence

AdmittedEvidence
!= evidence-set satisfaction

evidence-set satisfaction
!= TransitionDecision

P1-6 G_EVIDENCE fact
!= P1-7 Human/Judgment fact

file/hash exists
!= content admitted

Executor claim
!= admitted evidence

prior admitted evidence
!= current-task reused evidence
```

---

# mandatory stop

Stop if:

```text
P1-6 design requires changing exact P1-1/P1-4/P1-5 authority ownership
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED

Human-owned evidence semantics require P1-7 implementation to define P1-6 admission
→ OWNER_SCOPE_CONFLICT

current canonical rules contradict each other
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not weaken non-substitution to avoid a blocker.

---

# report required fields

- Task ID/path;
- predecessor HEAD;
- exact P1-5 42-path aggregate verification;
- terminal commit path inventory;
- `P1_6_DESIGN_BASE_COMMIT`;
- post-commit clean evidence;
- exact design path;
- exact evidence domain concepts;
- exact requirement profile semantics;
- producer/issuer model;
- content/ref authority;
- admission evaluation dimensions/reasons;
- evidence-set completeness;
- exact `G_EVIDENCE` attestation;
- concurrency/idempotency/reuse model;
- persistence/revocation/supersession;
- freshness/applicability;
- Human-owned boundary;
- sensitive evidence/export policy;
- implementation path ownership;
- implementation proof matrix;
- unresolved design question if any;
- Human pending;
- forbidden-not-run;
- preserved paths;
- next recommendation.

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260828_2329_aiscc-p1-6-evidence-admission-contract-design-freeze-with-p1-5-terminal-commit-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`
- compact design review summary

No product source, evidence body containing secrets, credential or unrelated file.

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260828_2329_aiscc-p1-6-evidence-admission-contract-design-freeze-with-p1-5-terminal-commit-1.md
→
.aiassistant/tasks/done/20260828_2329_aiscc-p1-6-evidence-admission-contract-design-freeze-with-p1-5-terminal-commit-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Always preserve:

- Stage-0 `P1_6_DESIGN_BASE_COMMIT`;
- `.aiassistant/tasks/done/20260828_2215_aiscc-p1-5-missing-provider-usage-token-accounting-rework-1.md`;
- `.aiassistant/records/aiscc/cycles/20260828_2329_aiscc-p1-5-provider-tool-execution-runtime-final-acceptance-1.cycle.md`;
- all exact 42 accepted P1-5 runtime candidate paths;
- `.aiassistant/tasks/done/20260828_2329_aiscc-p1-6-evidence-admission-contract-design-freeze-with-p1-5-terminal-commit-1.md`;
- `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md` candidate until Human review.

---

# next action after Human accepts P1-6 design

```text
P1-6 Evidence Admission Implementation + Runtime Verification
```

Do not implement it in this Task.
