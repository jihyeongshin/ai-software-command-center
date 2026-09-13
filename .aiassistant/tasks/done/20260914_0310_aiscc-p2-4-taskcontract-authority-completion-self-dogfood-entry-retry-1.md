# 작업지시서: P2-4 TaskContract authority completion + self-dogfood entry retry

## meta

- task_id: `20260914_0310_aiscc-p2-4-taskcontract-authority-completion-self-dogfood-entry-retry-1`
- created_at: `2026-09-14T03:10:14+09:00`
- work_type: `REWORK / P2_4_SOURCE_IMPLEMENTATION`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `b6843ee2ba412bb08d599fdadf225d91c04407b8`
- required_parent: `3050400e67470390551096b43a1947797b557151`
- predecessor_result_zip_sha256: `a506d741c0c7073d03628f37641027e92925065f0ba7d05b8a1acd462372a073`
- predecessor_done_task_sha256: `1c6a6caa1849b77506b46199a05191be618986d02b04bbda6bd0f3c7126aed75`
- governance_commit_authorized: `Yes / exact 3 paths`
- source_change_authorized: `Yes / bounded owner-completion + P2-4 retry`
- source_commit_authorized: `No`
- real_self_dogfood_golden_cycle_authorized: `No`
- DB_schema_or_migration_authorized: `No`
- private_runtime_or_DB_authorized: `No`
- Docker_authorized: `No`
- provider_or_external_network_authorized: `No`
- canonical_state_write_authorized: `No`
- public_release_authorized: `No`
- push_authorized: `No`
- fresh_IDE_chat_required: `No`
- success_ceiling: `P2_4_SELF_DOGFOOD_ENTRY_SOURCE_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. current judgment

0254 is **not** an accepted P2-4 source candidate.

Browser judgment:

```text
0254 Executor behavior:
CORRECT FAIL-CLOSED

result:
BLOCKED / P2_4_TASKCONTRACT_AUTHORITY_IMPLEMENTATION_GAP
```

Do not modify or replay P2-3 S1-S4/Recorded Replay.

P2-3 remains `ACCEPTED / CLOSED`.

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
retained/private PostgreSQL runtime
external provider/network
```

If repository `.venv\Scripts\python.exe` is absent, STOP. Do not search for another Python.

# 2. exact initial repository preflight

Require before governance placement/mutation:

```text
branch:
main

HEAD:
b6843ee2ba412bb08d599fdadf225d91c04407b8

HEAD^:
3050400e67470390551096b43a1947797b557151

index:
empty

tracked worktree:
clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0254_aiscc-p2-4-self-dogfood-orchestrator-entrypoint-task-materialization-implementation-1.md

SHA-256:
1c6a6caa1849b77506b46199a05191be618986d02b04bbda6bd0f3c7126aed75
```

Preserve ignored non-owned legacy Task byte-exact:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md

SHA-256:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Canonical state files must remain byte-exact:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48

.aiassistant/records/aiscc/DECISION_REGISTER.md
9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5

.aiassistant/records/aiscc/NEXT_ACTIONS.md
050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679
```

Any mismatch → STOP before Git/source mutation and report exact actual state.

# 3. inbound governance artifacts

The delivery package contains:

```text
20260914_0310_aiscc-p2-4-taskcontract-authority-gap-blocked-rework-entry-1.cycle.md
SHA-256 a97a84dfeb17cbb435f7ae0804481aa9aac45daf014c0d36e73b8535e8cc2662

20260914_0310_aiscc-p2-4-0254-blocked-taskcontract-authority-gap-rework-authorization-1.md
SHA-256 930fccc4bbabe70781cc3ed3d202a54afa036a3eeb6a9488b7b24dc585e5feb8

20260914_0310_aiscc-p2-4-taskcontract-authority-completion-self-dogfood-entry-retry-1.md
```

Place Task first into `.aiassistant/tasks/active/` and read it before substantive execution.

Then place:

```text
20260914_0310_aiscc-p2-4-taskcontract-authority-gap-blocked-rework-entry-1.cycle.md
→ .aiassistant/records/aiscc/cycles/

20260914_0310_aiscc-p2-4-0254-blocked-taskcontract-authority-gap-rework-authorization-1.md
→ .aiassistant/reports/aiscc/
```

After placement, before commit, Git-visible untracked must be exactly:

```text
.aiassistant/tasks/done/20260914_0254_aiscc-p2-4-self-dogfood-orchestrator-entrypoint-task-materialization-implementation-1.md
.aiassistant/records/aiscc/cycles/20260914_0310_aiscc-p2-4-taskcontract-authority-gap-blocked-rework-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_0310_aiscc-p2-4-0254-blocked-taskcontract-authority-gap-rework-authorization-1.md
```

Current Task remains ignored in `tasks/active`.

# 4. governance Commit A

Stage exactly the three untracked governance paths above.

Commit message exactly:

```text
docs(aiscc): record p2-4 taskcontract authority blocker
```

Require:

```text
Commit A parent = b6843ee2ba412bb08d599fdadf225d91c04407b8
changed paths = exact 3
index empty after commit
tracked clean after commit
Git-visible untracked = 0
```

No other commit is authorized.

If the exact stage set cannot be established, STOP before source mutation.

# 5. authoritative context / minimum reads

Read exact canonical rules:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Then inspect the current owner source, at minimum:

```text
src/aiscc/task_authority/models.py
src/aiscc/task_authority/authority.py
src/aiscc/task_authority/ports.py
src/aiscc/task_authority/repository.py
src/aiscc/next_action/**
src/aiscc/workflow/**
src/aiscc/persistence/**
src/aiscc/evidence/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/bootstrap.py
```

Read only the files/symbols necessary to establish actual ownership and integration.

If current canonical/source semantics conflict with this Task, STOP with
`POLICY_CONFLICT_INVESTIGATION_REQUIRED`.

# 6. authority invariant

Do not create a parallel TaskContract owner.

Accepted semantic boundary to preserve:

```text
TaskIssuanceCandidate != TaskContract

exact Task issuance owner:
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY

TaskContract:
immutable + versioned
Command Center-owned before issuance
issued version immutable

WorkRun:
System-owned

Judgment:
separate semantic authority

TransitionDecision:
separate System transition authority

Evidence/Human/Judgment owners:
unchanged
```

If the current repository has a superseding accepted exact authority, report it and STOP rather
than silently applying this older label.

# 7. complete the existing external Task authority

Within the existing canonical `task_authority` surface, implement or expose the minimum complete
immutable/versioned TaskContract issuance/read/verification capability needed by P2-4.

Do **not** invent a second self-dogfood TaskContract.

The issued authoritative contract (using current-repo names/types) must preserve at least:

```text
stable contract id
monotonic/exact contract version
task identity
project identity when canonical
goal
non-goals when canonical
allowed scope
forbidden scope
authority/context refs required by current architecture
evidence requirement binding/ref
Human gate requirement/policy binding
judgment owner policy
issuance provenance / source authority
immutability after issuance
```

Prefer composition/reuse of existing immutable types and refs, including existing
TaskConstraint/NextActionContext/P1-6/P1-7 refs where semantically applicable.

Agent/self_dogfood code must consume an already-authorized issuance API; it must not gain the
ability to self-authorize or expand scope.

# 8. durability boundary

The architecture requires issued TaskContract identity/version to survive restart.

Use the existing task-authority persistence/event/snapshot mechanism **only if** it can safely
persist/read/verify the complete required contract without schema change.

Forbidden:

```text
new migration
schema mutation
new database table/column
private retained PostgreSQL runtime
fake durability claim from an in-memory object
```

If complete durable authority requires a DB/schema/migration change outside current structure,
STOP with:

```text
P2_4_TASKCONTRACT_DURABILITY_SCOPE_EXPANSION_REQUIRED
```

Name exact required path/schema reason. Do not weaken the contract.

# 9. resume original P2-4 cut 1 only after authority completion

Implement immutable `SelfDogfoodTaskSpec` or semantically equivalent current-repo type.

It must explicitly bind:

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

Preserve the runtime/provenance split:

```text
product RuntimeMode:
reuse OWNER_SELF_DOGFOOD when canonical

public future Cycle execution_mode:
AISCC_SELF_DOGFOOD
```

No new WorkflowState or RuntimeMode.

# 10. deterministic NextAction → spec → TaskContract

Implement a deterministic bounded materializer for the explicitly authorized P2-4 path.

Requirements:

```text
authoritative current NextAction is input
no LLM/provider selects or rewrites NextAction
repository/base commit explicit
task/spec identity deterministic
same authoritative inputs -> same spec/fingerprint
complete TaskContract issued through existing external Task authority
Agent cannot expand scope
```

Fail closed on:

```text
wrong phase
wrong/stale NextAction ref
repository mismatch
base commit mismatch
empty/invalid task ownership
allowed/forbidden overlap
absolute/traversal paths
missing evidence binding
ambiguous Human requirement
```

# 11. WorkRun READY integration

Using the existing P1-4/System-owned creation path, prove exactly one local/fake WorkRun can be
created from the newly issued authoritative TaskContract with:

```text
WorkflowState = READY
state_version = current source-defined initial version
exact TaskContract id/version binding
RuntimeMode = existing owner/self-dogfood mode
repository/base commit provenance linked
orchestrator commit/version linked
NextAction ref linked
```

Do not manually mutate WorkRun/DB rows to simulate READY.

This is not the real golden cycle.

# 12. implementation allowlist

Allowed product paths:

```text
src/aiscc/task_authority/**
src/aiscc/self_dogfood/**
src/aiscc/bootstrap.py
```

Allowed tests:

```text
tests/unit/task_authority/**
tests/integration/task_authority/**
tests/unit/self_dogfood/**
tests/integration/self_dogfood/**
```

Existing dependency source outside these paths is read-only.

Do not modify:

```text
P1-4 transition semantics
P1-6 evidence admission semantics
P1-7 Human/Judgment semantics
P1-8 Cycle/NextAction authority
database models/migrations/schema
Stockroom scenario code
canonical state files
Replay artifacts
```

If correct integration requires any other product path, STOP with:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

and name exact path/reason.

# 13. required verification

Use repository-local Python with `-B`.

Minimum when source changes exist:

```text
in-memory compile or py_compile changed/new Python
Ruff changed/new Python
targeted unit tests for task-authority issuance/immutability/version/verification
targeted unit tests for SelfDogfoodTaskSpec validation/fingerprint
targeted unit tests for deterministic NextAction materialization
negative fail-closed tests
targeted integration: issued TaskContract -> existing WorkRun READY path
git diff --check
```

No full repository suite automatically.

No network/provider/Docker/private DB.

If targeted tests expose a broader existing-runtime regression requiring full-suite evidence,
STOP with `EVIDENCE_SCOPE_EXPANSION_REQUIRED`.

# 14. negative authority tests

At minimum prove:

```text
TaskIssuanceCandidate alone cannot satisfy TaskContract binding
self_dogfood caller cannot forge issued TaskContract
issued contract cannot be mutated in place
wrong contract version rejected
stale/wrong base rejected
wrong NextAction/phase rejected
repository mismatch rejected
allowed/forbidden overlap rejected
absolute/traversal scope path rejected
missing evidence binding rejected
ambiguous Human requirement rejected
rejected request creates no WorkRun
non-owned legacy active Task preserved
```

# 15. success semantics

A successful retry candidate must prove:

```text
canonical external Task authority:
complete immutable/versioned issuance/read/verify path present

TaskContract authority:
not duplicated

NextAction:
authoritative input

SelfDogfoodTaskSpec:
typed + immutable + deterministic

Task materialization:
deterministic

WorkRun:
existing System owner creates READY

RuntimeMode:
existing owner/self-dogfood mode

public provenance:
AISCC_SELF_DOGFOOD separate from RuntimeMode

state/evidence/Human/Judgment semantics:
unchanged

actual golden cycle:
NOT PERFORMED
```

# 16. Git terminal boundary

Governance Commit A is the only authorized commit.

Do not commit product/test source.

At terminal reporting:

- move current Task active → done byte-identically;
- index must be empty;
- tracked changes may only be allowed product/test paths;
- Git-visible governance untracked must be current done Task only;
- product untracked/modified paths must be separately reported;
- legacy 1400 ignored Task must remain byte-exact.

No push.

# 17. evidence/result classification

Report exact actuals using:

```text
EXECUTED_PASS
EXECUTED_FAIL
REUSED_ACCEPTED
HUMAN_PROVIDED
HUMAN_PENDING
NOT_REQUIRED
FORBIDDEN_NOT_RUN
BLOCKED_REQUIRED_EVIDENCE
```

Do not convert skipped implementation/tests after a mandatory STOP into PASS.

A correct fail-closed scope/durability stop is preferable to a parallel authority workaround.

# 18. export

Target:

```text
.aiassistant/reports/target/20260914_0310_aiscc-p2-4-taskcontract-authority-completion-self-dogfood-entry-retry-1/
```

Required root docs:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
SOURCE_OWNERSHIP_AUDIT.md
TASK_AUTHORITY_VERIFICATION.md
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

Generate manifest/member counts from the actual export set. Do not manually predict counts.

Require:

```text
one top-level directory
CRC PASS
manifest byte-size/SHA exact
TASK.md == canonical done Task
no private/secret values
no unrelated source copies
```

# 19. terminal ceiling

On source-candidate success:

```text
P2-3:
ACCEPTED / CLOSED

P2-4:
IMPLEMENTATION CANDIDATE / BROWSER REVIEW PENDING

actual self-dogfood golden cycle:
NOT PERFORMED

P2:
IN_PROGRESS

P3:
NOT_STARTED

Public Bounded Live:
NOT_RELEASED
```

On any named blocker, report the exact blocker and stop. Do not issue the golden cycle.
