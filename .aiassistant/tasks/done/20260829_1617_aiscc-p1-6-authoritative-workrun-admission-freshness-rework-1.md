# 작업지시서: P1-6 Authoritative WorkRun Admission Freshness Rework

## meta

- task_id: `20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-rework-1`
- created_at: `2026-08-29T16:17:00+09:00`
- phase: `P1-6 Evidence Admission`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1-6_EVIDENCE`
- accepted_design_commit: `192e223854a02293809cf6675e3a329e099e628d`
- accepted_design_path: `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`
- accepted_design_sha256: `0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463`
- predecessor_rework_task: `20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1`
- predecessor_judgment: `HOLD_REWORK_REQUIRED`
- p1_7_status: `NOT_STARTED`
- p1_8_status: `NOT_STARTED`
- public_bounded_live_release: `NOT_RELEASED`

---

# 1. 현재 상태

Accepted design terminal provenance is frozen:

```text
HEAD:
192e223854a02293809cf6675e3a329e099e628d
```

The current P1-6 runtime candidate remains uncommitted.

The previous rework successfully closed:

```text
durable HUMAN_DIRECT_EVIDENCE ingress
authority-revision attestation invalidation
finite reuse_maximum
CORRECTED vocabulary
```

Do not reopen or redesign those areas unless directly required by this narrow fix.

New Command Center HOLD Cycle:

```text
.aiassistant/records/aiscc/cycles/
20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-hold-1.cycle.md
```

New finding:

```text
Evidence admission currently validates stale state/version
against request/candidate self-consistency,
not against authoritative current WorkRunRow.
```

---

# 2. load-bearing invariant

Accepted P1-6 contract requires:

```text
EvidenceCandidate != AdmittedEvidence

WORKRUN_STATE_VERSION_SCOPED freshness
→ current WorkRun authority

state-version scoped stale proof
→ REJECTED

stale / missing / mismatched TaskContract/checkpoint authority
→ REJECTED
```

The following substitution is forbidden:

```text
candidate.observed_state/version
==
request.observed_state/version

!=

authoritative current WorkRun state/version
```

A later `EvidenceSetEvaluation` rejecting stale admitted evidence does not repair an invalid admission.

---

# 3. exact current gap

Current `PostgresEvidenceRepository.admit()` does not load authoritative `WorkRunRow` before persisting an `ADMITTED` decision.

Current `_fresh()` for:

```text
WORKRUN_STATE_VERSION_SCOPED
```

checks only:

```text
candidate.producer_work_run_id == request.work_run_id
candidate.observed_state == request.observed_state
candidate.observed_state_version == request.observed_state_version
```

Therefore this can currently pass:

```text
candidate:
work_run = R
state = ADMISSION_PENDING
state_version = 3

request:
work_run = R
state = ADMISSION_PENDING
state_version = 3

durable WorkRun R:
state = ADMISSION_PENDING
state_version = 4

current result:
candidate/request freshness may PASS

required result:
REJECTED / STALE
no AdmittedEvidence
```

Likewise, a missing or TaskContract-mismatched WorkRun must not produce admitted evidence.

---

# 4. 이번 턴 목표

1. Place/preserve the new HOLD Cycle.
2. Bind every admission request to authoritative durable WorkRun identity.
3. Verify exact current WorkRun TaskContract/state/state_version before `AdmittedEvidence` may be created.
4. Eliminate TOCTOU between WorkRun verification and admission persistence using the existing P1-4 persistence concurrency convention.
5. Make the admission evaluation dimensions/report reflect the real System authority result.
6. Add fresh PostgreSQL stale/missing/mismatch/concurrency tests.
7. Re-run directly affected P1-6/P1-4/P1-5 regressions.
8. Keep runtime candidate uncommitted.

---

# 5. authoritative WorkRun checks

Before an admission can be `ADMITTED`, the System-owned durable WorkRun must prove at minimum:

```text
WorkRun exists

WorkRun.work_run_id
== request.work_run_id

WorkRun.task_contract_id
== request.task_contract_id

WorkRun.task_contract_version
== request.task_contract_version

WorkRun.workflow_state
== request.observed_state

WorkRun.workflow_state
== checkpoint.source_state

WorkRun.state_version
== request.observed_state_version
```

Candidate-specific freshness then additionally follows the exact requirement-owned freshness policy.

For `WORKRUN_STATE_VERSION_SCOPED`:

```text
candidate.producer_work_run_id
== authoritative WorkRun.work_run_id

candidate.observed_state
== authoritative WorkRun.workflow_state

candidate.observed_state_version
== authoritative WorkRun.state_version
```

Do not merely compare candidate to request.

---

# 6. missing / mismatched WorkRun semantics

Unknown or mismatched authority must fail closed and produce a durable `REJECTED` admission result when the request can be safely evaluated.

At minimum prove:

```text
missing WorkRun
→ no AdmittedEvidence

WorkRun TaskContract id mismatch
→ no AdmittedEvidence

WorkRun TaskContract version mismatch
→ no AdmittedEvidence

WorkRun state mismatch
→ no AdmittedEvidence

WorkRun state_version mismatch
→ no AdmittedEvidence
```

Use the accepted rejection taxonomy/dimensions.

Do not add a new public rejection code unless the accepted design cannot represent the case.

Preferred semantic mapping should remain truthful across:

```text
TASK_CONTRACT_BINDING
CHECKPOINT_BINDING
FRESHNESS
AUTHORITY_CONFLICT / STALE
```

Exact implementation is owned by this Task but must not mislabel stale System authority as revocation.

---

# 7. TOCTOU / concurrency requirement

The following race must not be possible:

```text
T1:
admission reads WorkRun state_version = 3

T2:
workflow transition advances WorkRun to state_version = 4

T1:
persists ADMITTED evidence for state_version = 3
```

Before implementing a new lock, inspect the exact accepted P1-4 PostgreSQL transition persistence owner and reuse its WorkRun concurrency convention.

Required:

```text
admission WorkRun authority read
+ admission decision/admitted persistence
```

must be protected so a concurrent P1-4 state transition cannot invalidate the checked current state before the admission transaction commits.

Acceptable exact mechanism depends on existing P1-4 implementation:

```text
same WorkRun row lock
or
same canonical WorkRun advisory lock
or
other already accepted equivalent
```

Do NOT create an unrelated parallel lock namespace if it does not serialize with P1-4.

If current P1-4 transition persistence cannot provide a compatible synchronization boundary:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not guess.

---

# 8. authority/evaluator architecture

Do not solve the problem only with a repository-side exception that bypasses the normal admission decision provenance unless corruption/ambiguity truly prevents a safe evaluation.

The accepted model requires every candidate evaluation to explicitly decide authority dimensions.

The evaluation path must have access to the System-owned WorkRun result, for example through a narrow immutable authority snapshot or equivalent.

Required semantic outcome:

```text
request/candidate self-consistent
+ current WorkRun stale/missing/mismatched
→ REJECTED
```

and the durable evaluation must show why.

Do not let:

```text
REVOCATION_SUPERSESSION = FAIL
```

stand in for a WorkRun freshness mismatch unless that is actually the correct accepted dimension.

---

# 9. persistence integrity

The admission authority must not depend on an unverified string-only `work_run_id`.

Where compatible with the existing schema/conventions, add or preserve database-level referential integrity from P1-6 rows to `work_runs`.

However:

```text
FK existence
!= freshness proof
```

Even with an FK, current workflow state/version must still be checked transactionally.

Do not broaden migration scope beyond the minimum required P1-6 durability/integrity fix.

---

# 10. mandatory fresh proof matrix

## A. STALE_SYSTEM_STATE

Seed:

```text
WorkRun:
ADMISSION_PENDING / state_version 4

candidate:
ADMISSION_PENDING / state_version 3

request:
ADMISSION_PENDING / state_version 3
```

Expected:

```text
decision = REJECTED
primary or exact accepted reason = STALE / authority mismatch as canonical mapping requires
AdmittedEvidence = none
satisfaction row = none
reuse consumption = none if reuse candidate
```

This is the load-bearing test missing from the predecessor candidate.

## B. CURRENT_SYSTEM_STATE

Seed:

```text
WorkRun:
ADMISSION_PENDING / state_version 4

candidate:
ADMISSION_PENDING / state_version 4

request:
ADMISSION_PENDING / state_version 4
```

Expected:

```text
other exact authority requirements satisfied
→ normal admission may succeed
```

## C. MISSING_WORKRUN

```text
request/candidate use internally consistent unknown work_run_id
→ REJECTED
→ no AdmittedEvidence
```

## D. TASK_CONTRACT_MISMATCH

Prove separately:

```text
WorkRun task_contract_id mismatch
WorkRun task_contract_version mismatch
→ REJECTED
→ no AdmittedEvidence
```

## E. STATE_MISMATCH

```text
request/candidate claim ADMISSION_PENDING
current WorkRun = HUMAN_REQUIRED
same or different version
→ REJECTED
```

## F. TRANSITION / ADMISSION RACE

Use the real P1-4 persistence/concurrency mechanism.

Create a deterministic concurrency test proving:

```text
either admission wins while state/version is still current
or transition wins and admission rejects

never:
transition to new state/version committed
AND stale old-state admission committed as ADMITTED
```

The test must exercise PostgreSQL, not only a mocked lock.

## G. RESTART

Fresh repository/service objects:

```text
stale request after restart
→ still REJECTED from durable WorkRun authority
```

No process-local freshness cache.

---

# 11. regression required

After the new tests pass, run directly affected suites:

```text
P1-6 evidence unit/integration
P1-4 workflow unit/integration
P1-5 provider/tool unit/integration if shared persistence paths changed
```

Do not substitute predecessor pass counts for the new stale-System-state proof.

No broad unrelated full-suite expansion.

---

# 12. allowed paths

Primary:

```text
src/aiscc/evidence/admission.py
src/aiscc/evidence/repository.py
src/aiscc/evidence/models.py
src/aiscc/evidence/ports.py
src/aiscc/evidence/service.py
tests/unit/evidence/**
tests/integration/evidence/**
```

Narrow P1-4 integration/concurrency owner only if required after reading exact current source:

```text
src/aiscc/workflow/**
src/aiscc/persistence/**
tests/unit/workflow/**
tests/integration/workflow/**
```

Migration only if referential-integrity or exact schema adjustment is required:

```text
migrations/versions/20260829_0003_p1_6_evidence_admission.py
```

Governance/report lifecycle:

```text
.aiassistant/records/aiscc/cycles/20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-hold-1.cycle.md
.aiassistant/tasks/active/<this-task>
.aiassistant/tasks/done/<this-task>
.aiassistant/reports/target/20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-rework-1/**
```

Do not reopen unrelated corrected files simply to reformat them.

---

# 13. must-read source

Before implementation, read:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

.aiassistant/records/aiscc/cycles/
20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-hold-1.cycle.md

.aiassistant/tasks/done/
20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1.md
```

Then resolve and explicitly read the exact current P1-4 persistence implementation that owns:

```text
WorkRunRow current state/version read
transition transaction
row/advisory lock ordering
state_version increment
```

Do not infer concurrency behavior from tests or model definitions alone.

---

# 14. non-goals / forbidden

- no P1-7 implementation
- no P1-8 implementation
- no WorkflowState/transition graph changes
- no P1-5 provider redesign
- no new Human gate
- no public Live/deployment
- no real provider call
- no external credential/network
- no accepted design rewrite
- no accepted commit amend/revert
- no runtime candidate commit
- no Git push
- no unrelated refactor

---

# 15. evidence contract

executor_required:

```text
STATIC_SOURCE
UNIT_TEST
POSTGRESQL_INTEGRATION
WORKRUN_FRESHNESS
CONCURRENCY
RESTART
P1_4_REGRESSION
P1_5_REGRESSION when persistence integration touched
SECURITY_EXPORT
```

reuse_allowed:

```text
the four predecessor HOLD findings may be reused as closed
only if this rework does not alter their behavior

their fresh predecessor tests do not substitute for new WorkRun freshness proof
```

human_owned:

```text
P1-6 runtime final acceptance
```

not_required:

```text
browser
frontend
real provider
external HTTP
deployment
production/test infrastructure
```

forbidden:

```text
P1-7/P1-8 source
real provider call
credentialed external action
public Live
Git commit/push
accepted design rewrite
```

proof_non_substitution:

```text
candidate/request state agreement
!= System WorkRun freshness

foreign key
!= current state/version proof

later set-evaluation rejection
!= admission-time stale rejection

unit stale mismatch
!= PostgreSQL current-WorkRun stale proof
```

---

# 16. accept 기준

Rework candidate is reviewable only if all are true:

```text
admission reads authoritative current WorkRun

WorkRun TaskContract id/version are exact

WorkRun source state/state_version are exact at admission

request/candidate old-but-self-consistent state/version is REJECTED

missing WorkRun is REJECTED / no admission

TaskContract mismatch is REJECTED / no admission

state mismatch is REJECTED / no admission

P1-4 concurrent transition cannot race stale ADMITTED persistence

fresh PostgreSQL race test PASS

restart stale proof PASS

previous four corrected findings remain PASS

P1-4 regression PASS

P1-5 regression PASS when applicable

real provider/network/credential actions = 0

P1-7/P1-8 remain NOT_STARTED

Git HEAD remains
192e223854a02293809cf6675e3a329e099e628d

runtime candidate remains uncommitted
```

---

# 17. mandatory stop

STOP on:

```text
accepted design conflict
HEAD drift
unrelated dirty collision
need to modify WorkflowState graph
P1-4 concurrency convention cannot be safely shared
need for P1-7 authority
external runtime/credential/network requirement
```

After stop, perform only minimum blocker evidence/report/export.

---

# 18. report required

Executor report must include:

```text
start/final HEAD
accepted design SHA
new HOLD Cycle placement
exact P1-4 WorkRun concurrency owner/path read
pre-rework admission gap confirmation
changed authority path
how WorkRun is loaded/locked
how TOCTOU is prevented against actual P1-4 transition
evaluation dimension/rejection mapping
missing WorkRun result
TaskContract mismatch result
state mismatch result
stale System state/version result
current System state/version positive result
PostgreSQL concurrency race result
restart result
previous four findings regression
P1-4/P1-5 regression counts
migration/FK changes if any
provider/network/credential actions
Git HEAD/index/status
human verification = HUMAN_PENDING
preserved exact paths
```

---

# 19. export bundle

Target:

```text
.aiassistant/reports/target/
20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
all changed candidate files preserving repository-relative paths
new HOLD Cycle
REMOVED_FILES.md only if deletion exists
```

---

# 20. lifecycle / Git

Task starts:

```text
.aiassistant/tasks/active/
20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-rework-1.md
```

Executor turn complete:

```text
.aiassistant/tasks/done/
20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-rework-1.md
```

No Git add/commit/push is authorized.

Expected final HEAD remains:

```text
192e223854a02293809cf6675e3a329e099e628d
```

---

# 21. preserved artifacts

Must preserve:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

.aiassistant/records/aiscc/cycles/
20260829_1241_aiscc-p1-6-evidence-admission-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260829_1513_aiscc-p1-6-evidence-admission-runtime-authority-gap-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-hold-1.cycle.md

.aiassistant/tasks/done/
20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1.md

.aiassistant/tasks/done/
20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1.md

.aiassistant/tasks/done/
20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-rework-1.md
```

Do not remove:

```text
.aiassistant/reports/aiscc/20260829_1227_aiscc-p1-6-design-accepted-command-center-handoff-1.md
```

---

# 22. final response

1. result
2. start/final HEAD
3. HOLD Cycle placement
4. exact P1-4 WorkRun concurrency authority read
5. stale admission gap closed/not closed
6. changed files
7. fresh PostgreSQL proof
8. transition/admission race proof
9. restart proof
10. predecessor finding regression
11. target bundle
12. provider/network/credential actions
13. human verification = `HUMAN_PENDING`
14. Git index/status
15. preserved exact paths
16. next recommendation
