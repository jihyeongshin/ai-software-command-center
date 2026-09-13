# 작업지시서: P2-3 stranded S1 invalid-history disposition design

## meta

- task_id: `20260913_1224_aiscc-p2-3-stranded-s1-invalid-history-disposition-design-1`
- created_at: `2026-09-13T12:24:29+09:00`
- work_type: `PRIVATE_S1_INVALID_HISTORY_DISPOSITION_DESIGN`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `5affe61f02994f219b22ca934b5e0b93bc5e6f60`
- required_parent: `a4eb36611dca8d504610d9e3091950b0f32c20e7`
- required_grandparent: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- accepted_1208_result_zip_sha256: `76908e7d7505a49ea08e5708f56251be35d8c5a06175d24bc0e054eb675fa6f0`
- source_write_authorized: `No`
- test_write_authorized: `No`
- private_runtime_access_authorized: `No`
- runtime_disposition_authorized: `No`
- success_ceiling: `STRANDED_S1_DISPOSITION_BOUNDARY_DEFINED / EXECUTION_NOT_AUTHORIZED`

# 0. purpose

Do not retry in-place continuation.

Command Center has resolved:

```text
IN_PLACE_CONTINUATION_FORBIDDEN_BY_CURRENT_CONTRACT
```

Accepted exact stranded state:

```text
run_id: aiscc-p2-3-private-s1-normal-v1-run
attempt_id: aiscc-p2-3-private-s1-normal-v1-attempt-1
WorkRun: RUNNING/v2
ExecutionAttempt: NOT_STARTED
historical security seal: ADMITTED
historical runtime authorization: ADMITTED
historical materialization: ADMITTED
execution_operations: 0
runtime evidence: none
Judgment: none
```

Design only the contract-valid disposition of this invalid-history state.

# 1. transport and Python

Use only:
```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Forbidden: `python`, `py`, WindowsApps alias, PATH Python discovery.

Verify exact delivery ZIP/hash and three flat safe members.
Place current Task first at:
```text
.aiassistant/tasks/active/20260913_1224_aiscc-p2-3-stranded-s1-invalid-history-disposition-design-1.md
```
Then place current Cycle/Judgment and verify:
```text
.aiassistant/records/aiscc/cycles/20260913_1224_aiscc-p2-3-stranded-s1-invalid-history-disposition-entry-1.cycle.md
a0d2658398c834550bd89e10d2cc2283422a6a60cdc424fd0fe6808c941e06d3

.aiassistant/reports/aiscc/20260913_1224_aiscc-p2-3-stranded-s1-in-place-continuation-forbidden-judgment-1.md
9587af829556be5327a4dabe63a1d46bce638f956689c551f7126d4ac0577717
```

Bootstrap mismatch → STOP with no write/access/report/export.

# 2. repository baseline

Require:
```text
branch main
HEAD 5affe61f02994f219b22ca934b5e0b93bc5e6f60
HEAD^ a4eb36611dca8d504610d9e3091950b0f32c20e7
HEAD^^ 6cc4f988f56f5cbf32e57f4b5e9a52a180044c36
index empty
tracked clean
```

Before current delivery Git-visible untracked exactly six:
- `.aiassistant/tasks/done/20260913_1129_aiscc-p2-3-stranded-s1-in-place-recovery-boundary-design-1.md`  `d01fbfa993c0e37f06a9066f9def2ca1c4af590d372eaa122a6c53dee4e29e36`
- `.aiassistant/records/aiscc/cycles/20260913_1129_aiscc-p2-3-stranded-s1-recovery-design-entry-1.cycle.md`  `02356ec126b9381248ab491b013ad8a74f90abfd8d69a50349ad9f2718dd0b50`
- `.aiassistant/reports/aiscc/20260913_1129_aiscc-p2-3-stranded-s1-recovery-design-authorization-judgment-1.md`  `4ab5b734e9802c975e51a761bd4281b7a9359df7bd140711d7e8cb3e49dd214a`
- `.aiassistant/tasks/done/20260913_1208_aiscc-p2-3-stranded-s1-recovery-boundary-corrected-design-retry-1.md`  `899c1c650acd90fec2b2e99cf4e49ed5c5804539e57713b00fbb3462d2024e4c`
- `.aiassistant/records/aiscc/cycles/20260913_1208_aiscc-p2-3-stranded-s1-recovery-baseline-conflict-corrected-entry-1.cycle.md`  `f87221fb252c6db21f5731f09c58c2393ff4eaf4002d11bba4d8053d8132b9e5`
- `.aiassistant/reports/aiscc/20260913_1208_aiscc-p2-3-stranded-s1-recovery-baseline-conflict-correction-judgment-1.md`  `03c66a81c212c075f5e425accd2001106bc9709ee86c9f2833d3d1f32ef1b075`

Canonical state hashes:
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `550b7b3ec6659c5ad86558c84902a5319457334432db452405e31a2eb1153164`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `c9496a814cb94a834f53c4dee46032836dfaa4f8490d433a5909c0e46d2e3c3f`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `a6130f00deb41a1cae8c42cb62e7eb57d3457e40775794c6efb725fb604c832e`

Known source baselines:
- `src/aiscc/scenarios/stockroom_production.py`  `c070e194b5d3e0ca18d952202f71860175ab36f3a51b327c7799fe5ef36bffb3`
- `src/aiscc/scenarios/capture_runner.py`  `0dab27e0ce9ce2da7953188bcb26f288b637a4ba524141be2800b08302a59b18`
- `src/aiscc/providers/service.py`  `f21c3c29443446650e31fb0d4d0d30ceddb8956d51ad2e17221536102c6c5c18`
- `src/aiscc/persistence/repository.py`  `ab00af3dd871477da74b83275258aa48a47ba9a7081aad0154a808b6e4f1c089`

After current Cycle/Judgment placement while Task is active/ignored:
```text
Git-visible untracked = 8 exact
```

# 3. resolved authority

Do not reopen the delayed-start question.

For this exact history:
```text
delayed EXECUTION_STARTED = FORBIDDEN
in-place continuation = FORBIDDEN
```

No analysis may narrow filesystem materialization out of execution-side-effect scope.

# 4. runtime prohibition

Do not access Docker, retained PostgreSQL, password file, private runtime root, materialized files, security runtime, or
0036 rows. Do not execute transitions, cleanup, provider/tool calls, evidence or Judgment.

# 5. complete governance reads

Read current canonical rules for:
```text
ExecutionStatus transitions and terminal states
NOT_STARTED failure/abort semantics
Workflow RUNNING exit transitions
retry / return-to-READY
same-WorkRun next-attempt prerequisites
new WorkRun prerequisites
unknown outcome handling
security authority invalidation/revocation
materialization settlement/cleanup
artifact retention
evidence/Judgment prerequisites
audit preservation
```

Complete at minimum:
```text
AISCC_ORCHESTRATION
AISCC_PROVIDER_TOOL_EXECUTION
AISCC_SECURITY_SANDBOX
AISCC_EVIDENCE_ADMISSION
AISCC_HUMAN_GATE_JUDGMENT
```

Record exact paths and SHA-256.

# 6. complete source reads

Read completely:
```text
src/aiscc/scenarios/stockroom_production.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/providers/service.py
src/aiscc/persistence/repository.py
```

Discover/read directly required production modules owning execution terminalization, workflow transitions, retry, security
settlement/revocation, Stockroom workspace cleanup and materialized artifact settlement.

Record path/blob/SHA/symbols.

# 7. attempt disposition

Determine whether a durable attempt in:
```text
NOT_STARTED
causal READY/v1
while WorkRun RUNNING/v2
after prior execution-side-effect
```
has a contract-valid transition to a terminal/disposed status without `EXECUTION_STARTED`.

Inventory actual events/statuses only. For each classify:
```text
LEGAL
FORBIDDEN
REQUIRES_BOUNDED_SOURCE_SUPPORT
UNRESOLVED
```

# 8. WorkRun disposition

After any legal attempt disposition, determine exact allowed transitions out of RUNNING/v2.

Explicitly inspect whether current source/contract supports RUNNING→READY, a terminal failure/block state, or another
transition, with exact guards.

# 9. retry eligibility

Determine prerequisites for:
```text
same WorkRun + new attempt ID
new WorkRun
```

State whether current nonterminal NOT_STARTED attempt blocks either. Do not authorize a new attempt/run.

# 10. materialization cleanup

Trace source-owned cleanup/settlement.

Determine:
```text
cleanup owner
required durable disposition before cleanup
spent-key/lease preservation
audit/provenance retention requirements
whether successful materialization can be removed
whether partial/colliding workspace changes disposition
```

No actual cleanup.

# 11. security authority disposition

Determine how already-admitted seal/runtime authorization is handled when the attempt cannot continue:
```text
revocation
expiry
settlement
scope invalidation
natural process-local loss
```

Do not invent APIs absent source.

# 12. evidence/Judgment

Determine whether disposition should create evidence/Judgment or whether both must remain absent because provider
execution never reached a qualifying completion/failure boundary.

# 13. disposition classification

Inventory existing public production APIs that can express the needed disposition.

Conclude exactly one:
```text
DISPOSITION_VALID_WITH_EXISTING_PUBLIC_SOURCE
DISPOSITION_REQUIRES_BOUNDED_SOURCE_SUPPORT
DISPOSITION_FORBIDDEN_BY_CURRENT_CONTRACT
DISPOSITION_CONTRACT_UNRESOLVED
```

# 14. bounded support if required

Do not edit.

Identify minimal exact source/test paths for a source-owned disposition entrypoint.

It must:
```text
target exact existing run/attempt only
verify expected invalid-history shape before mutation
never emit delayed EXECUTION_STARTED
never replay READY→RUNNING
never invoke provider/tool execution
preserve historical audit rows
perform only contract-valid attempt/workflow disposition
order cleanup/revocation after correct durable boundary
reload authority after each mutation
fail closed on mismatch
```

# 15. future runtime preflight

Define exact later observations before mutation:
```text
WorkRun RUNNING/v2
attempt NOT_STARTED
execution_operations 0
runtime evidence absent
Judgment absent
materialized workspace identity/presence/completeness
no running transient
security/runtime authorization state if inspectable
no later state change
```

# 16. mandatory STOP conditions

Define STOP_PRESERVE/HUMAN_REVIEW for:
```text
WorkRun changed
attempt changed
operation exists
evidence/Judgment exists
materialization identity ambiguous
unexpected transient
cleanup target ambiguous
security authority incompatible
attempt disposition rejected
workflow disposition rejected
post-transition authority mismatch
```

No rollback/delete/reset.

# 17. post-disposition retry boundary

Without authorizing retry, define the exact durable state that would make a future retry/new attempt eligible:
```text
old attempt terminal/disposed state
required WorkRun state
security/materialization settlement
same WorkRun retained or not
fresh G_EXECUTION_STARTED requirement
```

# 18. Git lifecycle

Before Task move:
```text
HEAD unchanged
index empty
tracked clean
Git-visible untracked = 8 exact
```

Move current Task byte-identically active→done.

Final:
```text
Git-visible untracked = 9 exact
1129 Task/Cycle/Judgment
1208 Task/Cycle/Judgment
current Task/Cycle/Judgment
```

# 19. contract review

Require exactly 34 rows:
```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_6_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
KNOWN_SOURCE_BASELINES_EXACT
PYTHON_EXECUTABLE_EXACT
NO_PRIVATE_RUNTIME_ACCESS
NO_DB_DOCKER_ACCESS
NO_SOURCE_TEST_STATE_MUTATION
NO_GIT_WRITE
IN_PLACE_CONTINUATION_FORBIDDEN_ACCEPTED
DELAYED_EXECUTION_START_NOT_AUTHORIZED
READY_RUNNING_REPLAY_NOT_AUTHORIZED
ALTERNATE_ATTEMPT_ESCAPE_NOT_AUTHORIZED
EXECUTION_ATTEMPT_TERMINALIZATION_CONTRACT_READ
WORKRUN_DISPOSITION_TRANSITIONS_INVENTORIED
NOT_STARTED_FAILURE_ABORT_PATH_INVENTORIED
RETRY_ELIGIBILITY_CONTRACT_READ
NEW_ATTEMPT_PREREQUISITES_IDENTIFIED
MATERIALIZATION_CLEANUP_OWNER_IDENTIFIED
CLEANUP_ORDERING_CONTRACT_IDENTIFIED
SECURITY_AUTHORITY_DISPOSITION_IDENTIFIED
INVALID_HISTORY_AUDIT_PRESERVATION_DEFINED
EVIDENCE_JUDGMENT_NONCREATION_PRESERVED
EXISTING_PUBLIC_DISPOSITION_API_INVENTORIED
DISPOSITION_CLASSIFICATION_EXACT
MINIMAL_SOURCE_SCOPE_IF_REQUIRED_IDENTIFIED
DISPOSITION_PREFLIGHT_REQUIREMENTS_DEFINED
DISPOSITION_STOP_CONDITIONS_DEFINED
POST_DISPOSITION_RETRY_BOUNDARY_DEFINED
NO_EXECUTABLE_DISPOSITION_PERFORMED
NO_RUNTIME_CLEANUP_PERFORMED
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
EXPORT_INTEGRITY_PASS
```

Success requires `34 / 34 PASS`.

# 20. success export

Root docs exactly 11:
```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
DISPOSITION_CONTRACT_INVENTORY.md
ATTEMPT_DISPOSITION_ANALYSIS.md
WORKRUN_DISPOSITION_ANALYSIS.md
MATERIALIZATION_SECURITY_SETTLEMENT.md
DISPOSITION_CLASSIFICATION.md
DISPOSITION_SCOPE_AND_STOP_CONDITIONS.md
CONTRACT_REVIEW.md
```

Project-relative copies exactly 7:
```text
current Cycle
current Judgment
current done Task
src/aiscc/scenarios/stockroom_production.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/providers/service.py
src/aiscc/persistence/repository.py
```

Success export:
```text
18 total members
17 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == current done Task
```

# 21. success ceiling

```text
1208 accepted blocked result
in-place continuation FORBIDDEN_BY_CURRENT_CONTRACT
0036 S1 HOLD/PRESERVED
disposition contract DEFINED
source changes NONE
runtime access NONE
runtime disposition NOT_EXECUTED / NOT_AUTHORIZED
P2-3 IN_PROGRESS
```
