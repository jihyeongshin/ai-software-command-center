# 작업지시서: P1-3 Security / Runtime Safeguard Implementation with P1-2 Closure Repair Commit

## meta

- task_id: `20260827_1421_aiscc-p1-3-security-runtime-safeguard-implementation-with-closure-repair-commit-1`
- created_at: `2026-08-27 14:21 KST`
- phase: `P1-3 — Security / Runtime Safeguard Implementation and Verification`
- work_type: `SECURITY_SANDBOX_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1-2 terminal closure repair/persistence → first executable security safeguard implementation + runtime proof`
- predecessor_phase: `P1-2 Security / Sandbox / Runtime Boundary Design`
- predecessor_result: `ACCEPTED / CLOSED`
- predecessor_HEAD_before_closure_commit: `db81e065943970dfd19df4013de40106006fbec0`
- predecessor_terminal_cycle: `.aiassistant/records/aiscc/cycles/20260827_1342_aiscc-p1-2-security-sandbox-runtime-boundary-final-acceptance-1.cycle.md`
- previous_p1_3_attempt:
  `20260827_1357_aiscc-security-runtime-safeguard-implementation-and-verification-with-closure-commit-1`
- previous_p1_3_result:
  `BLOCKED_P1_2_CLOSURE_SET_MISMATCH`
- previous_attempt_scope:
  `Stage 0 only; no Git index mutation, no commit, no substrate inspection, no implementation`
- implementation_status_before: `NOT_IMPLEMENTED`
- public_live_release_status: `BLOCKED_UNTIL_P1_3_ACCEPTED`

---

# 0. supersession and blocker admission

The previous P1-3 Task:

```text
20260827_1357_aiscc-security-runtime-safeguard-implementation-and-verification-with-closure-commit-1
```

completed safely with:

```text
BLOCKED_P1_2_CLOSURE_SET_MISMATCH
```

Admit that result as predecessor provenance.

Reported Stage 0 evidence:

```text
repository root: PASS
branch main: PASS
HEAD db81e065...: PASS
closure SHA-256: 4/8 PASS, 4/8 FAIL
expected dirty set: 8
actual dirty set: 5
Git index mutation: none
closure commit: not created
P1_3_BASE_COMMIT: not created
substrate inspection: not started
P1-3 implementation: not started
```

Reported mismatched canonical files:

```text
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

This Task supersedes the previous Task for execution.

Do NOT reopen the previous blocker as an unexplained error.
The blocker established that the old exact-count/hash precondition did not match the actual
repository working tree.

This reissued Task intentionally removes the brittle rule:

```text
"exactly 8 dirty files MUST already exist"
```

and replaces it with:

```text
actual tracked dirty subset
MUST be contained in an explicit allowed provenance set

+
four terminal canonical files may be repaired by this Task
```

The previous blocked Task is already a submitted/done provenance artifact and MUST be preserved.

---

# 1. Human preparation

Human performs only:

1. place this Task at:

```text
.aiassistant/tasks/active/20260827_1421_aiscc-p1-3-security-runtime-safeguard-implementation-with-closure-repair-commit-1.md
```

2. start a fresh Executor chat.

Human does NOT need to reapply the prior Browser-produced closure ZIP.

Human does NOT create the closure commit.

The Executor owns:

```text
P1-2 terminal canonical repair
→ exact local provenance/closure commit
→ new P1_3_BASE_COMMIT verification
→ same Task continuation into runtime-substrate preflight
→ P1-3 implementation only if substrate preflight passes
```

---

# Stage 0 — repository and predecessor verification

## expected repository identity

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

expected HEAD before repair/closure commit:
db81e065943970dfd19df4013de40106006fbec0
```

Before any source edit or Git index mutation:

1. verify repository root;
2. verify branch `main`;
3. verify HEAD exactly;
4. verify no remote/network operation is needed;
5. read `git status --short`;
6. inventory tracked dirty paths;
7. confirm current active Task is this Task;
8. confirm previous blocked P1-3 Task exists under `tasks/done` or otherwise has durable submitted provenance;
9. run `git diff --check`;
10. confirm no secret/private material is present in the allowed closure/provenance set.

If HEAD is no longer `db81e065943970dfd19df4013de40106006fbec0`:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

Do not reinterpret a later commit as equivalent.

---

# Stage 0A — allowed pre-commit provenance universe

The pre-commit tracked dirty set does NOT need to contain every path below.

It MUST be a subset of the following explicit set, plus the exact terminal-repair edits performed
by this Task on paths already in the same set.

```text
.aiassistant/tasks/done/20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1.md

.aiassistant/tasks/done/20260827_1247_aiscc-p1-2-security-action-state-and-public-cancel-authorization-alignment-rework-1.md

.aiassistant/records/aiscc/cycles/20260827_1247_aiscc-p1-2-security-action-state-and-cancel-authorization-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/20260827_1342_aiscc-p1-2-security-sandbox-runtime-boundary-final-acceptance-1.cycle.md

.aiassistant/rules/AISCC_SECURITY_SANDBOX.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/tasks/done/20260827_1357_aiscc-security-runtime-safeguard-implementation-and-verification-with-closure-commit-1.md
```

Call this set:

```text
P1_2_CLOSURE_AND_P1_3_BLOCKER_ALLOWLIST
```

Rules:

```text
actual tracked dirty path outside allowlist
→ STOP
→ BLOCKED_P1_2_CLOSURE_SET_MISMATCH

allowlisted path absent from dirty set
→ NOT A BLOCKER by itself

allowlisted clean path
→ do not force-edit solely to make it dirty
```

Ignored:

```text
.aiassistant/tasks/active/**
.aiassistant/reports/target/**
.aiassistant/project-sources/bundles/**
```

do not count as tracked dirty closure paths.

Do not use `git clean`, `git reset`, `git stash` or destructive workspace normalization.

---

# Stage 0B — immutable predecessor evidence checks

The following accepted/submitted predecessor artifacts MUST be read directly and preserved.

Expected hashes:

```text
.aiassistant/tasks/done/20260827_1115_aiscc-security-sandbox-runtime-boundary-design-1.md
sha256:
c8201fa1de3392f10747ea446a5ae36e9b83a36f774e3e73490e5e01e39bd3e3

.aiassistant/tasks/done/20260827_1247_aiscc-p1-2-security-action-state-and-public-cancel-authorization-alignment-rework-1.md
sha256:
8ff58c3322685bb49607102b36f6c4e02ad0dd52b273629c266dc5319a2d4382

.aiassistant/records/aiscc/cycles/20260827_1247_aiscc-p1-2-security-action-state-and-cancel-authorization-hold-1.cycle.md
sha256:
3f3df261a5091d706176175957a2468fc0fda6c4eb103c2bf116c2357cf38b21

.aiassistant/records/aiscc/cycles/20260827_1342_aiscc-p1-2-security-sandbox-runtime-boundary-final-acceptance-1.cycle.md
sha256:
434331f1cef46cd786b7a179f4093de079280828f90dd5ef845cc92928251a80
```

If one of these four hashes differs:

```text
STOP
→ BLOCKED_IMMUTABLE_P1_2_PROVENANCE_MISMATCH
```

Do not rewrite accepted/submitted predecessor Task/Cycle content.

For the previous blocked P1-3 done Task:

```text
.aiassistant/tasks/done/20260827_1357_aiscc-security-runtime-safeguard-implementation-and-verification-with-closure-commit-1.md
```

verify:

- exact `task_id`;
- it records the prior execution contract;
- it was submitted/done;
- no successful closure commit or implementation is falsely recorded.

A hash match is not required because task-lifecycle/export metadata may have been added by the
Executor according to workflow rules.

Do not rewrite it.

---

# Stage 0C — repair the four terminal canonical files

The previous blocker explicitly established that these four files were not yet at the accepted
P1-2 terminal canonical state:

```text
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

This Task explicitly authorizes narrow canonical repair of these four files.

The repair authority is:

```text
Human P1-2 final review: ACCEPTED
+
P1-2 terminal Cycle
+
accepted P1-2 candidate semantics
+
current accepted P1-1 baseline
```

Do NOT use Browser chat text as canonical source.

## C1. AISCC_SECURITY_SANDBOX.md repair

Preserve the accepted substantive security design.

Do NOT redesign:

- principals/trust zones;
- RuntimeMode profiles;
- deny-by-default;
- action-class × WorkflowState model;
- state/version capability invalidation;
- public cancel target authorization;
- secret/isolation;
- timeout/retry/cancel;
- idempotency/abuse/budget;
- Replay fallback;
- P1-3 proof contract;
- P3-3 handoff.

Repair only terminal canonical metadata/provenance required to represent:

```text
document:
AISCC-P1-2-SECURITY-SANDBOX-V1

result:
ACCEPTED / CLOSED

human acceptance:
2026-08-27 Human P1-2 final review → ACCEPTED

terminal cycle:
.aiassistant/records/aiscc/cycles/20260827_1342_aiscc-p1-2-security-sandbox-runtime-boundary-final-acceptance-1.cycle.md

implementation status:
NOT_IMPLEMENTED

runtime security proof:
NOT_EXECUTED
```

Required semantic statement:

```text
This file is the repository canonical accepted P1-2 security/runtime design baseline.
It is NOT runtime safeguard proof.
```

After repair, compute SHA-256 and report it.

A particular Browser-generated hash is NOT required in this reissued Task.
Semantic terminal correctness + diff review is authoritative.

## C2. CURRENT_STATE_SUMMARY.md repair

Preserve all accepted prior phase history.

Ensure exact current phase statuses include:

```text
P1-1 Core Domain / State Machine Design
→ ACCEPTED / CLOSED

P1-2 Security / Sandbox / Runtime Boundary Design
→ ACCEPTED / CLOSED

P1-3 Security / Runtime Safeguard Implementation and Verification
→ READY / NOT_EXECUTED
```

Ensure:

```text
P1-2 implementation/runtime proof
→ NOT_EXECUTED

public bounded Live release
→ BLOCKED until P1-3 safeguard implementation + applicable verification is accepted
```

Reference terminal Cycle:

```text
.aiassistant/records/aiscc/cycles/20260827_1342_aiscc-p1-2-security-sandbox-runtime-boundary-final-acceptance-1.cycle.md
```

Current next action must be the reissued P1-3 track, not the superseded Task as an executable
authority.

## C3. DECISION_REGISTER.md repair

Ensure one active accepted decision exists:

```text
decision_id:
AISCC-P1-2-SECURITY-SANDBOX-RUNTIME-BOUNDARY-V1

decision_status:
HUMAN_PROVIDED / ACCEPTED / CLOSED

implementation_status:
NOT_IMPLEMENTED

verification_status:
semantic design + Human acceptance complete;
safeguard runtime evidence deferred to P1-3
```

It MUST preserve:

```text
SecurityAdmissionDecision = ALLOW | DENY

fresh state_version
!= action admissible in current WorkflowState

public run/replay visibility
!= cancel authority

run ID knowledge
!= target-run authorization

LIVE_UNAVAILABLE_OR_BUDGET_EXHAUSTED
→ RECORDED_REPLAY_REMAINS_AVAILABLE

P1-3
→ first safeguard implementation + runtime proof

P3-3
→ release-time provider/config reverification
```

Do not create a competing second active P1-2 security decision.

If a candidate/stale P1-2 decision exists, normalize/supersede it explicitly rather than leaving
two simultaneously-current decisions.

## C4. NEXT_ACTIONS.md repair

Stable queue must be:

```text
P1-3 — Security / Runtime Safeguard Implementation and Verification
P1-4 — Explicit State Machine Kernel Implementation
P1-5 — Agent Provider and Tool Execution
P1-6 — Evidence Admission
P1-7 — Human Gate and Judgment
P1-8 — Project Memory and Cycle Admission
P2-1 — Command Center Web UI
P2-2 — Synthetic Demo Repository
P2-3 — Canonical Scenario Pack and Recorded Replay Corpus
P2-4 — Self-Dogfooding Cutover
P3-1 — Comparative Evaluation
P3-2 — Public Repository Documentation
P3-3 — Public Release and Competition Submission
```

Completed phases must include:

```text
P1-1 → ACCEPTED / CLOSED
P1-2 → ACCEPTED / CLOSED
```

Current action:

```text
phase: P1-3
status: READY / TASK_CONTRACT_ISSUED / NOT_EXECUTED
```

Record:

```text
previous P1-3 preflight attempt
→ BLOCKED_P1_2_CLOSURE_SET_MISMATCH
→ no implementation occurred

current execution authority
→ 20260827_1421_aiscc-p1-3-security-runtime-safeguard-implementation-with-closure-repair-commit-1
```

Do not alter the release gate:

```text
NO_PUBLIC_BOUNDED_LIVE_RELEASE
BEFORE
P1_SECURITY_RUNTIME_SAFEGUARD_IMPLEMENTATION_AND_VERIFICATION_ACCEPTED
```

---

# Stage 0D — closure repair validation

After the four-file repair:

1. run `git diff --check`;
2. inspect exact diffs for the four repaired files;
3. verify terminal Cycle still matches expected hash;
4. verify no accepted P1-1 semantics changed;
5. verify no P1-2 substantive security policy weakened;
6. verify no product/runtime implementation exists yet;
7. verify no credential/provider/deployment claim was introduced;
8. compute SHA-256 for each repaired canonical file;
9. inventory current tracked dirty subset.

The resulting tracked dirty subset MUST still be contained in:

```text
P1_2_CLOSURE_AND_P1_3_BLOCKER_ALLOWLIST
```

No exact dirty-file count is required.

---

# Stage 0E — authorized local closure/provenance commit

This Task authorizes exactly one local commit before P1-3 substrate preflight.

## staging rule

Stage ONLY currently changed paths from:

```text
P1_2_CLOSURE_AND_P1_3_BLOCKER_ALLOWLIST
```

Use explicit path staging.

Allowed pattern:

```text
git add -- <explicit changed allowlisted path 1> <path 2> ...
```

Forbidden:

```text
git add .
git add -A
git commit -a
```

Before commit:

```text
git diff --cached --check
git diff --cached --name-status
```

Verify:

```text
staged paths
⊆ P1_2_CLOSURE_AND_P1_3_BLOCKER_ALLOWLIST

and

every tracked dirty allowlisted path intended as durable provenance
is either staged or explicitly justified as unchanged/non-durable
```

The prior blocked P1-3 done Task is durable provenance and, if tracked dirty, MUST be staged.

## commit message

Use exactly:

```text
docs: close P1-2 and record P1-3 preflight blocker

Persist the Human-accepted P1-2 security baseline and terminal provenance.

Record the superseded P1-3 closure-set preflight blocker, advance the
canonical queue to the reissued P1-3 task, and keep safeguard
implementation and runtime proof explicitly unexecuted.
```

## allowed Git operations

```text
git add -- <explicit allowlisted paths>
git diff --cached --check
git diff --cached --name-status
git status --short
git commit
git rev-parse HEAD
git show --name-status --stat <new-head>
```

Forbidden:

```text
git reset
git stash
git clean
git amend
git fetch
git pull
git push
branch switch/create
tag
remote mutation
```

If Git identity is missing:

```text
STOP
→ HUMAN_GIT_IDENTITY_REQUIRED
```

Do not invent/configure identity.

## Stage 0 commit acceptance gate

After commit:

1. record full commit hash as:

```text
P1_3_BASE_COMMIT
```

2. verify commit contains no path outside:

```text
P1_2_CLOSURE_AND_P1_3_BLOCKER_ALLOWLIST
```

3. verify:

```text
git diff db81e065943970dfd19df4013de40106006fbec0..<P1_3_BASE_COMMIT> --check
```

4. verify tracked working tree is clean;
5. ignored current active Task/target artifacts may remain;
6. verify no remote operation occurred.

If fail:

```text
STOP
→ BLOCKED_P1_2_CLOSURE_COMMIT_INVALID
```

If pass:

```text
P1-2 terminal Git persistence
→ COMPLETED

previous P1-3 blocker provenance
→ PERSISTED

P1_3_BASE_COMMIT
→ <full new commit hash>
```

Git commit authorization is now exhausted.

For the remainder of this Task:

```text
git add
git commit
git push
→ FORBIDDEN
```

P1-3 implementation remains uncommitted review candidate.

---

# Stage 1 — runtime substrate preflight

After the Stage 0 commit only.

P1-3 MUST NOT silently select a language/framework/build system.

Inspect the now-clean repository to determine whether a canonical/unambiguous executable AISCC
runtime substrate already exists.

Acceptable evidence:

- accepted canonical architecture/runtime baseline naming language/build; or
- one unambiguous tracked product runtime with build manifest + source root; or
- Human-accepted repository decision defining implementation substrate.

Not sufficient alone:

- Project Source mirror generator;
- one-off Python script;
- bootstrap helper;
- IDE/editor metadata;
- target/export artifact.

If unresolved:

```text
STOP
→ BLOCKED_RUNTIME_SUBSTRATE_DECISION_REQUIRED
```

Then:

- do not install dependencies;
- do not create a top-level runtime;
- do not choose Python/Node/Java/etc. from convenience;
- do not start P1-4/P1-5;
- produce substrate evidence + Executor report/export only.

If resolved, record:

```text
P1_3_BASE_COMMIT:
runtime_language:
runtime_framework:
build_manifest:
runtime_source_root:
test_root:
resolution_evidence:
```

and continue Stage 2 in the same Task.

---

# accepted design inputs

P1-1:

```text
AgentOutput != SystemState
EvidenceCandidate != AdmittedEvidence

HumanGateStatus != HumanResult
HumanResult != Judgment
Judgment != TransitionDecision
TransitionDecision != WorkflowState

RuntimeMode != WorkflowState
```

P1-2:

```text
SecurityAdmissionDecision = ALLOW | DENY
unknown / ambiguous permission → DENY

fresh state_version
!= action admissible

PUBLIC_RUN_OR_REPLAY_VISIBILITY
!= PUBLIC_CANCEL_AUTHORITY

RUN_ID_KNOWLEDGE
!= TARGET_RUN_CONTROL_AUTHORIZATION

LIVE_UNAVAILABLE_OR_BUDGET_EXHAUSTED
→ RECORDED_REPLAY_REMAINS_AVAILABLE
```

---

# Stage 2 — P1-3 implementation and verification

Execute only if Stage 1 resolves an accepted/unambiguous runtime substrate.

## implementation goals

Implement the FIRST executable security safeguard slice covering at minimum:

1. versioned RuntimeMode permission profiles;
2. exact `SecurityActionClass`;
3. action-class × WorkflowState eligibility;
4. authoritative state/version freshness validation;
5. prior capability invalidation/revocation after state/version change;
6. deny-by-default resource-domain admission;
7. public requester/session/principal → exact target-run cancel authorization;
8. idempotent public cancel intent admission;
9. secret-safe opaque capability/reference handling;
10. applicable per-run isolation boundary in the selected substrate;
11. bounded timeout/retry/cancel primitive;
12. application idempotency/abuse/budget admission;
13. cleanup/residue/quarantine behavior;
14. secret-safe ALLOW/DENY provenance;
15. required tests/runtime probes.

This Task is NOT the full workflow kernel.

## P1-4 boundary

Allowed:

```text
SecurityPolicy / SecurityAdmission
→ consumes authoritative WorkflowState + state_version snapshot/ref
→ returns ALLOW / DENY + reason/provenance
```

A test state fixture is allowed.

```text
security test state fixture
!= P1-4 workflow kernel
```

Do not implement a competing authoritative state machine.

## non-goals

- P1-4 full state machine kernel
- P1-5 provider/tool orchestration
- P1-6 evidence engine
- P1-7 Human Gate/Judgment
- P1-8 Cycle memory
- frontend/UI
- public deployment
- Cloudflare/Railway/OpenAI resource creation
- real API key/credential inspection/generation
- provider billing/configuration
- current provider pricing/region verification
- production penetration testing
- P3-3 release/submission
- Browser Project Source sync
- second Git commit

---

# canonical read set

Read exactly as needed:

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
12. `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
13. `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
14. `.aiassistant/records/aiscc/cycles/20260827_1342_aiscc-p1-2-security-sandbox-runtime-boundary-final-acceptance-1.cycle.md`
15. `.aiassistant/tasks/done/20260827_1357_aiscc-security-runtime-safeguard-implementation-and-verification-with-closure-commit-1.md`

Do not bulk-read unrelated historical Tasks/Cycles.

---

# required executable safeguards

## A. RuntimeMode profiles

Implement:

```text
OWNER_SELF_DOGFOOD
PUBLIC_RECORDED_REPLAY
PUBLIC_BOUNDED_LIVE
```

Public Replay:

```text
NO inference
NO source mutation
NO shell/network/tool execution
```

Public Live hard prohibitions must be executable policy, not prompt convention.

## B. action/state admission

Minimum:

```text
RUN_EXECUTION_SIDE_EFFECT
→ RUNNING only

wrong action/state
→ DENY(ACTION_STATE_NOT_ADMISSIBLE)
```

Unknown combination fails closed.

## C. freshness / capability lifetime

```text
state/version change
→ prior permission/capability cannot be reused without revalidation
```

Terminal state cannot leave normal execution/provider capability active solely because lease time
remains.

## D. deny-by-default resource boundary

Applicable domains:

- filesystem
- process/shell
- tool
- outbound network
- secret/credential
- repository/worktree
- provider
- scenario/action

Unknown → `DENY`.

Policy object alone must not be claimed as host/container isolation.

## E. public cancel authorization

Required deny cases:

```text
run/replay visible only → DENY
run_id known only → DENY
session/principal mismatch → DENY
expired/revoked/wrong-target grant → DENY
```

Repeated authorized cancel is idempotent.

Cancel admission does NOT mutate authoritative WorkflowState directly.

## F. secret-safe capability

No raw secret in policy/provenance/log.

Use opaque capability/reference where applicable.

Do not fabricate production secret-manager proof.

## G. timeout/retry/cancel

- finite timeout
- finite retry
- explicit cancellation
- no silent success
- no unbounded retry

## H. idempotency / abuse / budget

Prove at application boundary:

- duplicate identity does not duplicate operation;
- exhausted budget/limit denies before simulated paid action;
- finite limits;
- provider hard-spend config not falsely claimed.

## I. cleanup / residue / quarantine

Deterministic cleanup hooks for applicable:

- success
- failure
- cancel
- timeout

Unresolved residue:

```text
quarantine/failure signal
!= clean success
```

---

# evidence contract

## executor_required — CLOSURE_REPAIR_AND_GIT_PROVENANCE

Pass:

- old HEAD exact;
- actual dirty subset within allowlist;
- immutable predecessor hashes pass;
- four canonical files repaired;
- no substantive P1-2 policy regression;
- exact staged paths recorded;
- one local commit created;
- new full `P1_3_BASE_COMMIT`;
- no unauthorized path in commit;
- tracked tree clean after commit;
- no remote operation.

## executor_required — REPOSITORY_PREFLIGHT

Pass if runtime substrate resolved.

Valid blocker:

```text
BLOCKED_RUNTIME_SUBSTRATE_DECISION_REQUIRED
```

## executor_required — STATIC_SOURCE

- accepted canonical sources read;
- implementation paths exact;
- no P1-1/P1-2 semantic drift;
- no prompt-only hard prohibition.

## executor_required — TARGETED_TEST

Deterministic automated coverage for changed safeguard logic.

Does NOT substitute for runtime isolation/network/cleanup proof.

## executor_required — ACTION_STATE_CANCEL_AUTHORIZATION_RUNTIME

Prove:

1. wrong WorkflowState action → DENY;
2. prior capability after state/version transition → stale/revoked DENY;
3. terminal state normal execution/provider side effect → DENY;
4. designed blocked/terminal safety cleanup can settle existing resources without opening normal execution;
5. public session A cannot cancel session B's run;
6. Replay/read/run-ID visibility alone cannot cancel;
7. repeated authorized cancel is idempotent.

## executor_required — FILESYSTEM_PROCESS_ISOLATION_RUNTIME

Required only if implementation slice creates subprocess/filesystem run resources.

If implementation is expected to enforce it but runtime proof requires broader infrastructure:

```text
BLOCKED_REQUIRED_EVIDENCE
```

Do not substitute unit/source proof.

## executor_required — NETWORK_RUNTIME

Required only if implementation slice exposes outbound network capability.

If runtime evidence requires broad external infrastructure/credentials:

```text
BLOCKED_REQUIRED_EVIDENCE
```

Do not use real provider credentials.

## executor_required — SECRET_NON_EXPOSURE

- opaque refs only in decision/provenance/log;
- raw secret absent;
- public profile cannot request/select credential.

Do not insert a real secret.

## executor_required — TIMEOUT_RETRY_CANCEL_RUNTIME

- bounded timeout;
- bounded retry;
- cancellation settles applicable resource;
- failure not relabeled success.

## executor_required — IDEMPOTENCY_ABUSE_BUDGET_RUNTIME

- duplicate identity no duplicate operation;
- exceeded budget/limit denies before simulated paid action;
- tested abuse/throttle fails closed.

## executor_required — CLEANUP_RESIDUE_RUNTIME

- applicable cleanup paths executed;
- residue detection;
- unresolved residue → quarantine/failure.

## human_owned — HUMAN_VERIFICATION

Human reviews:

- Stage 0 repair/commit correctness;
- `P1_3_BASE_COMMIT`;
- runtime substrate;
- implementation scope;
- runtime proof;
- any blocked proof;
- cleanup/residue;
- whether P1-3 can be accepted before P1-4.

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

---

# proof non-substitution

```text
terminal metadata repair
!= security implementation

closure commit
!= P1-3 acceptance

fresh state_version
!= action admissible

policy source
!= runtime enforcement

unit test
!= filesystem/process/network sandbox proof

run visibility
!= cancel authority

opaque secret test
!= production secret manager proof

application budget enforcement
!= provider spend limit configured

security test fixture
!= P1-4 workflow kernel
```

---

# mandatory stop

Stop after minimal report/export if:

- old HEAD differs;
- dirty path exists outside allowlist;
- immutable P1-2 Task/Cycle hash differs;
- accepted P1-2 semantics cannot be reconstructed without ambiguity;
- closure commit cannot be created safely;
- Git identity missing;
- substrate undefined;
- new runtime language/framework must be invented;
- P1-1/P1-2 conflict appears;
- real credential/provider access is required;
- required runtime proof requires broad new infrastructure;
- unrelated workspace changes collide;
- private/secret material is encountered;
- scope expansion is required.

Do not broaden into P1-4/P1-5.

---

# Git policy after Stage 0

After the one authorized closure/provenance commit:

```text
git add
git commit
git push
remote operation
→ FORBIDDEN
```

P1-3 implementation remains uncommitted for Command Center review.

---

# accept 기준

P1-3 may become `ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING` only when:

- Stage 0 repair + commit pass;
- runtime substrate resolves;
- executable safeguard implementation exists;
- fail-closed profile/action/state/cancel/secret/idempotency/budget rules enforced;
- applicable runtime proof passes;
- no required proof substitution;
- accepted P1-1/P1-2 semantics unchanged;
- no provider/deployment/credential action;
- no second Git commit;
- Human verification remains pending.

If runtime substrate is undefined:

```text
BLOCKED_RUNTIME_SUBSTRATE_DECISION_REQUIRED
```

is the correct successful blocker outcome.

---

# report required fields

- Task path/id
- previous blocked P1-3 Task/result
- repository root/branch/old HEAD
- initial tracked dirty inventory
- allowlist subset judgment
- immutable predecessor hashes
- exact four-file repair summary
- repaired file SHA-256
- pre-commit diff/integrity
- exact staged paths
- commit message
- new full `P1_3_BASE_COMMIT`
- commit inventory
- post-commit tracked clean evidence
- no remote operation evidence
- runtime substrate resolution
- implementation/test paths
- changed product/security source
- targeted tests
- each runtime evidence classification
- Agent claim vs admitted evidence
- Human pending
- forbidden-not-run
- mandatory stop/scope expansion
- rollback/revert guide
- preserved exact paths
- next recommendation

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260827_1421_aiscc-p1-3-security-runtime-safeguard-implementation-with-closure-repair-commit-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- changed P1-3 implementation/test/config files preserving relative paths
- `REMOVED_FILES.md` only if deletion actually occurred

If blocked at Stage 1 before implementation, export only Task/report/manifest and minimal
non-sensitive blocker evidence; do not invent changed implementation files.

---

# Task lifecycle

When Executor-required work/report/export completes or a named blocker is safely established:

```text
.aiassistant/tasks/active/20260827_1421_aiscc-p1-3-security-runtime-safeguard-implementation-with-closure-repair-commit-1.md
→
.aiassistant/tasks/done/20260827_1421_aiscc-p1-3-security-runtime-safeguard-implementation-with-closure-repair-commit-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Always preserve after this turn:

- `.aiassistant/tasks/done/20260827_1357_aiscc-security-runtime-safeguard-implementation-and-verification-with-closure-commit-1.md`
- `.aiassistant/tasks/done/20260827_1421_aiscc-p1-3-security-runtime-safeguard-implementation-with-closure-repair-commit-1.md`
- the single Stage 0 local closure/provenance commit
- accepted P1-2 canonical files/provenance contained in that commit

If P1-3 implementation proceeds:

- changed runtime/security source/tests remain uncommitted for review
- eventual terminal P1-3 Cycle is created by Command Center after judgment

Temporary target/runtime logs are not durable canonical unless later judgment explicitly preserves
them.

---

# next action after P1-3 acceptance

```text
P1-4 Explicit State Machine Kernel Implementation
```

Do not execute P1-4 in this Task.
