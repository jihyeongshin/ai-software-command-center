# 작업지시서: P2-4 Self-Dogfood orchestrator entrypoint and Task materialization implementation

## meta
- created_at: `2026-09-14T02:54:18+09:00`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `3050400e67470390551096b43a1947797b557151`
- required_parent: `68017ed5f3d15c0512dbf04899c798352adee710`
- required_grandparent: `23311b5283c9412e30783ae46a1925e85579247b`
- accepted_0237_result_zip_sha256: `f1490c91d65ab0c8654f3cd9a080065351403d9a624ca98b6aebc5caedd27f3d`
- governance_commit_authorized: `Yes / exact 3 paths`
- source_change_authorized: `Yes / bounded P2-4 implementation candidate`
- source_commit_authorized: `No`
- real_self_dogfood_golden_cycle_authorized: `No`
- private_runtime_or_DB_authorized: `No`
- Docker_authorized: `No`
- provider_or_external_network_authorized: `No`
- canonical_state_write_authorized: `No`
- public_release_authorized: `No`
- push_authorized: `No`
- success_ceiling: `P2_4_SELF_DOGFOOD_ENTRY_SOURCE_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. phase boundary

P2-3 is terminally closed.

This is P2-4 implementation cut 1 of the submission-path plan:

```text
1. Self-Dogfood orchestrator entrypoint + deterministic Task/WorkRun materialization
2. one actual AISCC self-dogfood golden cycle
3. final P2-4 acceptance/persistence
```

This Task implements only step 1.

Do not perform the actual golden cycle.

# 1. executables

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Use only:

```text
Python:
<repository-root>\.venv\Scripts\python.exe

Git:
C:\Program Files\Git\cmd\git.exe
```

Forbidden:

```text
python
py
WindowsApps
PATH/external Python discovery
Docker
retained private PostgreSQL/runtime
external provider/network
```

# 2. exact repository baseline

Require:

```text
branch main
HEAD 3050400e67470390551096b43a1947797b557151
HEAD^ 68017ed5f3d15c0512dbf04899c798352adee710
HEAD^^ 23311b5283c9412e30783ae46a1925e85579247b
index empty
tracked clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0237_aiscc-p2-3-replay-terminal-closure-predecessor-count-corrected-retry-1.md
SHA-256 70aaf20dde6af94a027ce061789a4b04b798f805088ca536e6a2ebeb9ca62c2a
```

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md` `80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md` `9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md` `050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679`

Require current authoritative projection:

```text
P2-3:
ACCEPTED / CLOSED

P2-4:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

P2:
IN_PROGRESS

Recorded Replay corpus root:
a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e

Public Bounded Live:
NOT_RELEASED
```

Preserve ignored non-owned legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement while current Task remains active/ignored:

```text
Git-visible untracked exactly three:
0237 done Task
current Cycle
current Judgment
```

Mismatch → STOP before Git/source mutation.

# 3. Commit A — exact P2-3 acceptance / P2-4 entry provenance

Stage exactly:

```text
.aiassistant/tasks/done/20260914_0237_aiscc-p2-3-replay-terminal-closure-predecessor-count-corrected-retry-1.md
.aiassistant/records/aiscc/cycles/20260914_0254_aiscc-p2-3-closed-p2-4-self-dogfood-implementation-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_0254_aiscc-p2-3-final-closure-acceptance-p2-4-implementation-authorization-1.md
```

Commit message exactly:

```text
docs(aiscc): persist p2-3 closure acceptance
```

Require:

```text
Commit A parent = 3050400e67470390551096b43a1947797b557151
changed paths = exact 3
index empty after commit
tracked clean
Git-visible untracked = 0
```

Current active Task remains ignored.

Any failure → STOP before source modification.

# 4. read-only architecture/source ownership audit

Before writing implementation, inspect the repository source and canonical rules for the current owners of:

```text
Project / NextAction projection
TaskContract construction/versioning
WorkRun creation / READY initial projection
RuntimeMode
P1-4 transition kernel
P1-6 evidence requirements
P1-7 Human/Judgment
P1-8 Cycle/NextAction
bootstrap/application composition
```

At minimum read:

```text
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

and the corresponding current `src/aiscc/**` types/repositories/services.

Produce:

```text
owner
existing type/API
source path
whether reused unchanged
required adapter/materializer responsibility
```

Do not implement a second state machine, TaskContract model, WorkRun repository, evidence engine, Human engine or Judgment engine.

If the current source has no safe API to create a TaskContract-bound READY WorkRun without a persistence/schema change outside the allowed scope, STOP with:

```text
P2_4_RUNTIME_INTEGRATION_SCOPE_EXPANSION_REQUIRED
```

# 5. required typed self-dogfood specification

Implement one immutable typed spec named `SelfDogfoodTaskSpec` or a semantically equivalent current-repo name.

It must explicitly carry at least:

```text
task_id
project_id
next_action_ref
repository_root
base_commit
goal
allowed_paths
forbidden_paths
evidence_requirements
human_gate_requirement
execution_mode
```

Requirements:

```text
execution_mode public provenance:
AISCC_SELF_DOGFOOD

repository_root:
exact AISCC repository identity, not arbitrary cwd

base_commit:
exact 40-char Git commit

allowed_paths / forbidden_paths:
immutable normalized project-relative paths/patterns

evidence_requirements:
explicit immutable refs/specs; not inferred from Agent prose

human_gate_requirement:
explicit; never inferred from completion text
```

If the current product already has an immutable type that semantically owns one of these fields, compose/reuse it rather than duplicate it.

# 6. runtime-mode rule

Audit current `RuntimeMode`.

If `OWNER_SELF_DOGFOOD` is the accepted product runtime context for owner/self-dogfood execution, reuse it.

Do NOT add another runtime mode solely because Command Center Cycle provenance uses:

```text
execution_mode = AISCC_SELF_DOGFOOD
```

Keep the distinction explicit:

```text
product RuntimeMode:
existing canonical owner/self-dogfood mode

public Cycle execution_mode:
AISCC_SELF_DOGFOOD
```

No workflow state is added.

# 7. deterministic NextAction → spec materialization

Implement a deterministic materializer/entrypoint.

Input must include an authoritative current NextAction projection/reference and explicit repository/base-commit context.

It must NOT call an LLM/provider to choose or rewrite the next work.

For this cut, support only the explicitly authorized P2-4 self-dogfood path.

Require fail-closed behavior for:

```text
wrong phase
wrong/stale NextAction ref
repository mismatch
base commit mismatch
invalid/empty task ownership
allowed/forbidden scope overlap
absolute or traversal scope path
missing evidence requirement binding
ambiguous Human requirement
```

Task/spec identity or fingerprint must be deterministic from its authoritative inputs.

Do not create a general planner.

# 8. TaskContract materialization

Map the typed self-dogfood spec into the existing authoritative `TaskContract` type/versioning path.

Requirements:

```text
issued TaskContract remains immutable
goal/scope/evidence/Human policy binding preserved
judgment owner policy explicitly selected by existing contract semantics
Agent cannot expand scope
execution mode/provenance attached without changing workflow-state meaning
```

Do not introduce a parallel self-dogfood-only TaskContract model.

If the existing TaskContract cannot hold required provenance directly, keep self-dogfood provenance in a typed sidecar/context object linked by exact task/contract identifiers; do not alter persistence schema in this Task.

# 9. WorkRun READY materialization

Using existing system-owned creation/repository/kernel APIs, prove the materialized contract can create exactly one new local/fake WorkRun with:

```text
initial WorkflowState:
READY

state_version:
existing source-defined initial version

TaskContract exact binding:
present

RuntimeMode:
existing owner/self-dogfood mode

repository/base commit provenance:
linked

orchestrator commit:
linked

NextAction ref:
linked
```

Do not manually mutate a WorkRun object or database row to simulate READY.

This is local deterministic integration only, not the actual AISCC golden run.

# 10. orchestrator provenance

The self-dogfood entry must expose immutable provenance sufficient for a future Cycle to record:

```text
execution_mode = AISCC_SELF_DOGFOOD
orchestrator_version
orchestrator_commit
source NextAction ref
TaskContract id/version
Task spec fingerprint
repository identity
base commit
initial state/version
```

For local tests, use explicit deterministic values.

Do not use current wall-clock time as an identity input.

# 11. Task artifact materialization boundary

If the implementation materializes a human-readable Task artifact/file, test it only inside an isolated temporary repository root.

Requirements:

```text
deterministic bytes for same spec
exact task ownership marker
project-relative canonical target
no overwrite of unrelated active Task
existing non-owned active Task preserved byte-exact
```

Do not write a new self-dogfood Task into the real repository `.aiassistant/tasks/active` during this implementation Task.

The future golden-cycle Task will own real Task issuance/materialization.

# 12. required negative tests

At minimum prove fail-closed:

```text
stale/wrong base commit → reject
wrong NextAction/phase → reject
repository mismatch → reject
allowed/forbidden overlap → reject
path traversal/absolute path → reject
missing evidence binding → reject
ambiguous Human requirement → reject
attempted non-owned active Task overwrite → reject/preserve
```

Rejected requests must not create a WorkRun.

# 13. allowed implementation scope

Preferred new source scope:

```text
src/aiscc/self_dogfood/**
```

Optional existing wiring path only if required for a public constructor/entrypoint:

```text
src/aiscc/bootstrap.py
```

Preferred tests:

```text
tests/unit/self_dogfood/**
tests/integration/self_dogfood/**
```

New files inside those exact subtrees are allowed.

Read-only dependencies may be imported from existing P1-4/P1-6/P1-7/P1-8/runtime/project modules.

Do NOT modify:
- existing P1-4 transition semantics;
- P1-6 evidence admission semantics;
- P1-7 Human/Judgment semantics;
- P1-8 Cycle/NextAction authority;
- database models/migrations;
- stockroom scenario product code;
- canonical state files.

If correct integration requires another product path, STOP with:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

and name the exact path/reason.

# 14. targeted local verification

Use repository-local Python with `-B`.

Minimum:

```text
changed/new source in-memory compile or py_compile
Ruff changed/new Python
unit tests for spec validation/fingerprint
unit tests for deterministic NextAction materialization
negative fail-closed tests
integration test using existing TaskContract + WorkRun creation path
non-owned active Task preservation test if file materialization exists
git diff --check
```

No full repository suite automatically.

No provider/LLM/network.

If the targeted suite demonstrates a broader existing-runtime regression that requires full-suite evidence, STOP with:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

# 15. success semantics

A successful implementation candidate must prove:

```text
authoritative NextAction:
input, not Agent suggestion

Task materialization:
deterministic

TaskContract:
existing canonical owner/type reused

WorkRun:
existing canonical system owner creates READY

execution mode:
explicit self-dogfood provenance

workflow state/transition authority:
unchanged

evidence/Human/Judgment semantics:
unchanged

planner:
none

actual golden cycle:
not performed
```

# 16. Git terminal boundary

Commit A is the only commit.

After Commit A:
- no source commit;
- no canonical state commit;
- no push.

Move current Task active→done byte-identically at terminal reporting.

Final governance untracked:

```text
current done Task only
```

Product working-tree changes may contain only files under the allowed source/test scope in section 13.

If new product/test files are untracked, report them separately from governance untracked. Do not conflate the sets.

Index must be empty.

Legacy 1400 remains ignored/non-owned.

# 17. contract review

Exactly 61 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
INITIAL_INDEX_EMPTY_TRACKED_CLEAN
INITIAL_UNTRACKED_0237_DONE_TASK_ONLY
PREDECESSOR_0237_RESULT_ACCEPTED
CURRENT_STATE_HASHES_EXACT
CURRENT_P2_3_ACCEPTED_CLOSED
CURRENT_P2_4_ENTRY_READY_NEXT_EXECUTABLE
REPLAY_ROOT_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
COMMIT_A_STAGE_SET_EXACT_3
COMMIT_A_PARENT_EXACT
COMMIT_A_MESSAGE_EXACT
COMMIT_A_CHANGED_PATHS_EXACT_3
POST_COMMIT_A_INDEX_EMPTY_TRACKED_CLEAN
POST_COMMIT_A_UNTRACKED_ZERO
NO_CANONICAL_STATE_MUTATION
SELF_DOGFOOD_SOURCE_OWNERSHIP_AUDIT_COMPLETE
EXISTING_NEXT_ACTION_AUTHORITY_API_IDENTIFIED
EXISTING_TASK_CONTRACT_API_IDENTIFIED
EXISTING_WORKRUN_CREATION_API_IDENTIFIED
EXISTING_RUNTIME_MODE_POLICY_IDENTIFIED
NO_DUPLICATE_STATE_MACHINE_CREATED
NO_DUPLICATE_JUDGMENT_AUTHORITY_CREATED
SELF_DOGFOOD_TASK_SPEC_TYPED_IMMUTABLE
SELF_DOGFOOD_TASK_SPEC_REQUIRED_FIELDS_PRESENT
NEXT_ACTION_BINDING_EXPLICIT
REPOSITORY_BASE_COMMIT_BINDING_EXPLICIT
ALLOWED_FORBIDDEN_SCOPE_BINDING_EXPLICIT
EVIDENCE_REQUIREMENTS_BINDING_EXPLICIT
HUMAN_GATE_REQUIREMENT_BINDING_EXPLICIT
SELF_DOGFOOD_EXECUTION_PROVENANCE_PRESENT
ORCHESTRATOR_COMMIT_PROVENANCE_PRESENT
DETERMINISTIC_TASK_ID_OR_FINGERPRINT_PRESENT
NO_LLM_NEXT_ACTION_SELECTION
NO_FREEFORM_PLANNER
TASK_MATERIALIZATION_DETERMINISTIC
NON_OWNED_ACTIVE_TASK_PRESERVED
EXISTING_TASKCONTRACT_MATERIALIZATION_PASS
EXISTING_WORKRUN_READY_CREATION_PASS
WORKRUN_RUNTIME_MODE_OWNER_SELF_DOGFOOD_OR_CANONICAL_EQUIVALENT
PUBLIC_EXECUTION_MODE_AISCC_SELF_DOGFOOD_PROJECTED
STALE_BASE_COMMIT_REJECTED
WRONG_NEXT_ACTION_REJECTED
ALLOWED_FORBIDDEN_SCOPE_OVERLAP_REJECTED
REPOSITORY_MISMATCH_REJECTED
TARGETED_UNIT_TESTS_PASS
TARGETED_INTEGRATION_TESTS_PASS
RUFF_CHANGED_PYTHON_PASS
PY_COMPILE_CHANGED_PYTHON_PASS
GIT_DIFF_CHECK_PASS
NO_EXTERNAL_PROVIDER_NETWORK
NO_REAL_SELF_DOGFOOD_GOLDEN_RUN
NO_PRIVATE_RUNTIME_DB_DOCKER_ACCESS
NO_PUBLIC_DEPLOYMENT
NO_GIT_SOURCE_COMMIT
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_GOVERNANCE_UNTRACKED_CURRENT_DONE_TASK_ONLY
FINAL_PRODUCT_CHANGES_WITHIN_ALLOWLIST
EXPORT_INTEGRITY_PASS
```

Successful source candidate:

```text
61 / 61 PASS
```

A scoped source-layout/integration stop must leave unperformed rows non-PASS.

# 18. export

Root docs:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
0237_ACCEPTANCE_VERIFICATION.md
SOURCE_OWNERSHIP_AUDIT.md
SELF_DOGFOOD_SPEC_VERIFICATION.md
NEXT_ACTION_MATERIALIZATION_VERIFICATION.md
TASKCONTRACT_WORKRUN_INTEGRATION_VERIFICATION.md
NEGATIVE_GUARD_VERIFICATION.md
SOURCE_CHANGE_SUMMARY.md
TEST_VERIFICATION.md
CONTRACT_REVIEW.md
```

Include project-relative copies of:
- current Cycle;
- current Judgment;
- current done Task;
- every changed/new product/test file.

Generate manifest/member counts from actual set.

Require:
- one top-level;
- CRC PASS;
- manifest SHA/size exact;
- TASK.md == canonical done Task;
- no private values;
- no unrelated source copies.

# 19. success ceiling

```text
P2-3:
ACCEPTED / CLOSED

P2-4:
IMPLEMENTATION CANDIDATE / BROWSER REVIEW PENDING

self-dogfood source entrypoint:
IMPLEMENTED CANDIDATE

actual AISCC self-dogfood golden cycle:
NOT_PERFORMED

P2:
IN_PROGRESS

P3:
NOT_STARTED

Public Bounded Live:
NOT_RELEASED
```
