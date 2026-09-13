# 작업지시서: P2-4 TaskContract durable-body authority baseline design

## meta

- task_id: `20260914_0319_aiscc-p2-4-taskcontract-durable-body-authority-baseline-design-1`
- created_at: `2026-09-14T03:19:07+09:00`
- work_type: `DESIGN_AUDIT / DOC_BASELINE_UPDATE_CANDIDATE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `04b5dda84c7bdb975cd4a4e74b7ccf3eb7f5eb6d`
- required_parent: `b6843ee2ba412bb08d599fdadf225d91c04407b8`
- predecessor_result_zip_sha256: `eeab6135d0db04e2bc942499ea58b3a857b72d5a22e2cfc063e56b936d0ff650`
- predecessor_done_task_sha256: `961107a9ca38cfeab8f4c38e22396d61d0ab7b9e06e69d084b1dde32b1f24768`
- governance_commit_authorized: `Yes / exact 3 paths`
- product_source_change_authorized: `No`
- canonical_baseline_write_authorized: `No`
- DB_schema_or_migration_authorized: `No`
- private_runtime_or_DB_authorized: `No`
- Docker_authorized: `No`
- provider_or_external_network_authorized: `No`
- source_commit_authorized: `No`
- push_authorized: `No`
- fresh_IDE_chat_required: `No`
- success_ceiling: `P2_4_TASKCONTRACT_DURABLE_BODY_BASELINE_PROPOSAL / HUMAN_REVIEW_PENDING`

# 0. current judgment

0310 Executor result is accepted as a truthful fail-closed result:

```text
BLOCKED / P2_4_TASKCONTRACT_DURABILITY_SCOPE_EXPANSION_REQUIRED
```

The P2-4 source candidate remains `NOT_CREATED`.

This is not an Executor defect and is not a contradictory Command Center contract. The 0310 Task explicitly required STOP if correct whole-TaskContract durability required schema/migration or a protected authority change.

P2-3 remains `ACCEPTED / CLOSED`. Do not rerun or modify P2-3 scenarios or Replay.

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
04b5dda84c7bdb975cd4a4e74b7ccf3eb7f5eb6d

HEAD^:
b6843ee2ba412bb08d599fdadf225d91c04407b8

index:
empty

tracked worktree:
clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0310_aiscc-p2-4-taskcontract-authority-completion-self-dogfood-entry-retry-1.md

SHA-256:
961107a9ca38cfeab8f4c38e22396d61d0ab7b9e06e69d084b1dde32b1f24768
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

Any mismatch -> STOP before Git/source mutation and report exact actual state.

# 3. inbound governance artifacts

The delivery package contains this Task plus:

```text
20260914_0319_aiscc-p2-4-taskcontract-durability-scope-blocked-design-entry-1.cycle.md
20260914_0319_aiscc-p2-4-0310-durability-scope-blocked-design-authorization-1.md
```

Place Task first into `.aiassistant/tasks/active/` and read it before substantive execution.

Then place:

```text
20260914_0319_aiscc-p2-4-taskcontract-durability-scope-blocked-design-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_0319_aiscc-p2-4-0310-durability-scope-blocked-design-authorization-1.md
-> .aiassistant/reports/aiscc/
```

After placement, before commit, Git-visible untracked must be exactly:

```text
.aiassistant/tasks/done/20260914_0310_aiscc-p2-4-taskcontract-authority-completion-self-dogfood-entry-retry-1.md
.aiassistant/records/aiscc/cycles/20260914_0319_aiscc-p2-4-taskcontract-durability-scope-blocked-design-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_0319_aiscc-p2-4-0310-durability-scope-blocked-design-authorization-1.md
```

Current Task remains ignored in `tasks/active`.

# 4. governance Commit B

Stage exactly the three untracked governance paths above.

Commit message exactly:

```text
docs(aiscc): record p2-4 taskcontract durability blocker
```

Require:

```text
Commit B parent = 04b5dda84c7bdb975cd4a4e74b7ccf3eb7f5eb6d
changed paths = exact 3
index empty after commit
tracked clean after commit
Git-visible untracked = 0
```

No other commit is authorized.

If exact stage set cannot be established, STOP before further work.

# 5. authoritative context / minimum reads

Read exact canonical rules first:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Then inspect only the source required to establish the durable owner contract, at minimum:

```text
src/aiscc/task_authority/models.py
src/aiscc/task_authority/authority.py
src/aiscc/task_authority/ports.py
src/aiscc/task_authority/repository.py
src/aiscc/persistence/models.py
migrations/versions/*
src/aiscc/next_action/*
src/aiscc/workflow/*
```

Read existing tests only when needed to establish encoded compatibility semantics.

Do not bulk-read unrelated product source.

If current canonical/source semantics conflict with this Task, STOP with `POLICY_CONFLICT_INVESTIGATION_REQUIRED`.

# 6. invariant that must not change

The proposal MUST preserve:

```text
TaskIssuanceCandidate != TaskContract
exact Task issuance owner = EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY

TaskContract:
immutable + versioned
restart-surviving identity/version/body
Command Center-owned before issuance
issued version immutable

WorkRun:
System-owned

TaskConstraintRefV1:
existing accepted reference semantics preserved
unknown_fields=DENY preserved for V1

Evidence / Human / Judgment / Transition authority:
unchanged
```

Do not solve the blocker by:

```text
adding undocumented extra fields to TaskConstraintRefV1
using permissive unknown-field deserialization
storing only an in-memory body
treating a hash/ref as if it were the full restart-surviving body
repurposing P1-6 evidence content as TaskContract truth
creating a self-dogfood-only TaskContract owner
creating a generic document store without exact authority semantics
```

# 7. this Task's only substantive goal

Produce an exact, implementation-ready **durable whole-TaskContract authority baseline proposal** under the existing external Command Center Task authority.

This Task does NOT adopt or implement the proposal.

The proposal must be derived from current canonical/source facts and must select one preferred design, not leave multiple equally-ranked alternatives.

At minimum specify:

```text
1. semantic owner
2. exact durable aggregate/record boundary
3. exact new or versioned model/type names
4. contract_id + contract_version rules
5. immutable complete body shape
6. canonical serialization/fingerprint algorithm
7. how TaskConstraintRefV1 binds to the body without changing V1 semantics
8. issuance/read/verify API boundary
9. supersession/version increment semantics
10. WorkRun binding semantics
11. NextAction/task issuance provenance binding
12. evidence requirement binding
13. Human gate/policy binding
14. judgment owner policy binding
15. restart/recovery semantics
16. concurrency/idempotency semantics
17. backward compatibility with existing durable rows/events/snapshots
18. exact migration shape if a migration is required
19. rollback/revert semantics
20. exact implementation/test path allowlist for the next Task
```

# 8. storage/migration decision requirements

The design audit must answer, from actual source:

```text
A. Can the complete immutable body be persisted with existing schema while preserving every accepted V1 semantic?
B. If NO, what exact new table/column/row model is minimally required?
C. If a new table is preferred, why is it semantically safer than extending an existing payload?
D. What is the exact foreign-key or logical binding to existing TaskConstraintRefV1 / event / owner snapshot records?
E. Which existing data requires no backfill, and why?
F. Which migration downgrade behavior is safe?
```

Do not claim "migration required" merely because it is convenient. Prove the reason from exact current schema/serialization/authority contracts.

Do not perform the migration.

# 9. baseline supersession boundary

The proposal must identify the exact accepted baseline clauses that would need Human-approved supersession/addition.

At minimum inspect whether the proposal changes:

```text
TaskContract scope
source ownership
carrier/source equality
TaskConstraintRef schema semantics
Task issuance boundary
restart-surviving truth
P1-8 prerequisite owner authority
```

Output exact old clause/reference and proposed replacement/addition.

Do not rewrite historical accepted decisions.

# 10. required output artifacts

Target:

```text
.aiassistant/reports/target/20260914_0319_aiscc-p2-4-taskcontract-durable-body-authority-baseline-design-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
SOURCE_AUTHORITY_AUDIT.md
CURRENT_SCHEMA_AUDIT.md
TASKCONTRACT_DURABLE_BODY_BASELINE_PROPOSAL.md
BASELINE_SUPERSESSION_MAP.md
MIGRATION_DESIGN.md
IMPLEMENTATION_PATH_ALLOWLIST.md
RISK_AND_ROLLBACK.md
CONTRACT_REVIEW.md
```

Include project-relative copies of:

- current Cycle;
- current Judgment;
- current done Task.

Do not include unchanged product source copies unless the Task explicitly needs a narrow `SOURCE_EVIDENCE_EXPORT`; instead report exact paths/symbols/hashes where useful.

# 11. evidence contract

executor_required:

- transport/hash/archive/current Task verification;
- exact initial Git/state/legacy preflight;
- exact governance Commit B;
- explicit read of the exact canonical P1-8 prerequisite owner-authority baseline;
- current source/schema/serialization audit;
- exact durable-body design proposal;
- baseline supersession map;
- migration design;
- implementation/test allowlist;
- UTF-8/control-character/Markdown/diff-check/export integrity.

human_owned:

- adoption of the proposed authority/baseline change;
- approval to mutate canonical baseline;
- approval to create/execute DB migration;
- P2-4 source-candidate acceptance;
- actual self-dogfood golden-cycle acceptance.

not_required:

- product implementation;
- unit/integration runtime tests;
- private DB runtime;
- Docker;
- provider/network;
- browser QA;
- P2-3 scenario/replay rerun.

forbidden:

- product/test source mutation;
- canonical baseline mutation;
- migration creation;
- DB/schema mutation;
- private runtime/Docker/provider/network;
- actual self-dogfood run;
- source commit/push/deployment.

# 12. accept criteria

Browser-review candidate is acceptable only if:

```text
one preferred design is selected
exact current-source reason is demonstrated
existing semantic owner is preserved
TaskConstraintRefV1 semantics are not silently widened
whole body is restart-surviving and immutable/versioned
complete binding fields are covered
migration need/shape is exact
backward compatibility is explicit
baseline clauses requiring Human approval are exact
next implementation path allowlist is exact
no product/canonical/schema mutation occurred
```

Success status ceiling:

```text
P2_4_TASKCONTRACT_DURABLE_BODY_BASELINE_PROPOSAL
/ HUMAN_REVIEW_PENDING
```

This is NOT source-candidate acceptance.

# 13. mandatory stop

STOP after minimal evidence/report/export if:

```text
baseline/source conflict cannot be resolved from exact current files
required canonical owner file is missing
repository baseline mismatch
proposal would require changing a different authority owner
security/private-data uncertainty
```

Do not invent missing semantics.

# 14. terminal Git boundary

Governance Commit B is the only authorized commit.

At terminal reporting:

- move current Task active -> done byte-identically;
- index empty;
- tracked clean;
- Git-visible governance untracked = current done Task only;
- no product/test/canonical-baseline/migration changes;
- legacy 1400 ignored Task byte-exact.

No push.

# 15. final state ceiling

```text
P2-3:
ACCEPTED / CLOSED

P2-4:
IN_PROGRESS
source candidate:
NOT CREATED

TaskContract durable-body authority baseline:
PROPOSAL ONLY / HUMAN_REVIEW_PENDING when successful

actual self-dogfood golden cycle:
NOT PERFORMED

P2:
IN_PROGRESS

P3:
NOT_STARTED

Public Bounded Live:
NOT_RELEASED
```
