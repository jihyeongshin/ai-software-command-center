# 작업지시서: P2-4 first actual self-dogfood golden cycle — Executor driver fix retry

## meta

- task_id: `20260914_2301_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-driver-fix-retry-1`
- created_at: `2026-09-14T23:01:21+09:00`
- work_type: `ACTUAL_SELF_DOGFOOD_GOLDEN_CYCLE_RETRY + FRESH_RUNTIME_IDENTITY + SINGLE_FILE_AGENT_CHANGE + GIT_PERSISTENCE`
- evidence_profile: `CRITICAL_GOLDEN`
- execution_mode: `MANUAL_COMMAND_CENTER_OUTER / AISCC_SELF_DOGFOOD_INNER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `609d3063ee9e707dae8b2cc7834647b617c2f5a1`
- required_parent: `621c1a374fe6ad42731c6249c68a39421eeda395`
- predecessor_result_zip_sha256: `07161104c425c5d701c0985159333954590022bbc290b1d45e71cc1f12f11788`
- failed_outer_task_sha256: `08efe3cb3d73923f0b4f843e001232ff974621409fb93316c0b38ba38f0ea508`
- failed_inner_task_sha256: `93600cafcade7e51495f6cea4f4797e6677b4e835231f19cced8d934ec5e8574`
- predecessor_disposition: `ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED`
- predecessor_classification: `EXECUTOR_OPERATIONAL_DRIVER_COMPOSITION_DEFECT`
- migration_head: `20260914_0012`
- fresh_IDE_chat_required: `No`
- governance_commit_authorized: `Yes / exact 4 paths / Commit A`
- real_self_dogfood_Task_authorized: `Yes / exact supplied inner Task`
- real_local_PostgreSQL_runtime_authorized: `Yes / one fresh Task-owned postgres:17.6`
- real_TaskContract_WorkRun_authorized: `Yes / one fresh golden lineage`
- real_repository_Agent_change_authorized: `Yes / exact one file`
- real_evidence_judgment_cycle_nextaction_authorized: `Yes / exact golden lineage`
- result_commit_authorized: `Yes / exact one governed source file / Commit B`
- product_runtime_source_mutation_authorized: `No`
- test_rule_migration_canonical_state_mutation_authorized: `No`
- provider_LLM_external_network_authorized: `No`
- retained_private_DB_authorized: `No`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_FIRST_SELF_DOGFOOD_GOLDEN_CYCLE_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. Browser judgment of 2216

2216 is NOT a golden success.

Browser disposition:

```text
ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED
```

Classification:

```text
EXECUTOR_OPERATIONAL_DRIVER_COMPOSITION_DEFECT
```

Verified successful operational boundary:

```text
Genesis current
→ TaskContract
→ READY/v1
→ external start
→ RUNNING/v2
→ clean completion lease before edit
```

Failure:

```text
FileNotFoundError
because docs/ parent did not exist
```

No product/runtime semantic defect is established.

# 1. predecessor evidence

- `CONTRACT_REVIEW.md`: `0ccedad4bfc6f842196b529f060c932aea07f91a9807239247570f490cf07071`
- `EXECUTOR_REPORT.md`: `b3448c61b68bbf9dfd4a0c36c8214bbf459175aeb2c54388e02ca63c025a22c1`
- `GOLDEN_BOOTSTRAP_REVIEW.md`: `86ede31afaca9ca83c6245ab03e6ebad4f83cdeb1308a97de8bdcbc9027ae52d`
- `GOLDEN_EXTERNAL_START.json`: `855c81f5986bb2c45efc99ab8b9675ce5f61a100ee185fe9420ffff2792066da`
- `GOLDEN_GENESIS.json`: `dcdb042b3a6f5b16258f5c541ede42164af299964953fae2b3ef0cb3fda52d84`
- `GOLDEN_PROVENANCE.json`: `af7b27ec72ea7c0bd72b39de87fdc3e176657ecc563e97bd706205e9efe7d576`
- `GOLDEN_RUNTIME_SOURCE_AUDIT.md`: `b988df61b0001d6656cbdbf1df057aec334ca92c8e5b556e6fe2c6216b4ec867`
- `GOLDEN_SPEC.json`: `f6dc4537b36f4b282e6540255d6ebec6cb24cb364620bc1d4a58575eaeeae521`
- `GOLDEN_TASKCONTRACT.json`: `6be49feb948e767afc573427b98fbc92cae69bda88354e25cbbff4d9ea567898`
- `GOLDEN_TRANSITIONS.json`: `b1bb31f84bc66c45bbd2eeecee3ab1a0af9f971a47ee9a4c19ba1f8d9a6460bf`
- `GOLDEN_WORKRUN.json`: `a7f70bc897187e37279ea8ce53b4d8adbcd87de4eb045e679ae0ae8f8cfd1ad0`
- `evidence/COMMIT_A.json`: `08184f78a70c96c352dc3fbb99b005ee30c94910d999034a6e5f3af6a5e3dbbe`
- `evidence/COMPLETION_LEASE.json`: `d3afee55e3b5f716d8c0a898f8b31121c70772d1cca1adacb4db4b8138775405`
- `evidence/READONLY_TERMINAL_RUNTIME.json`: `df614777be9ea59a2679e4850e90d559118f2ee1658bc00a4d131d97b60df348`
- `evidence/RUNTIME_STOP.json`: `e1bcc9fb103c0899ab517bfa1570af2d8b5db34a7f75cf2bded065bca1fbb6dc`
- `evidence/TERMINAL_WORKSPACE.json`: `b66eae169d72f73ed33186520a670937704625cdbed44e8e5b9933a633d5e0ec`

After Task-first read, copy only to:

```text
.aiassistant/reports/target/20260914_2301_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-driver-fix-retry-1/accepted-input/
```

Mismatch -> `BLOCKED_MISSING_ARTIFACT`.

# 2. exact new inner Task

Package member:

```text
20260914_2301_aiscc-p2-4-golden-agent-single-file-proof-change-3.md
```

Expected SHA-256:

```text
0b3ae3ab85fc0bf3a9d121865735c41f595756e2bc4a185848ab893dfa22c912
```

Governed target:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

Expected target SHA-256:

```text
7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
```

# 3. exact repository preflight

Require before new Governance Commit A:

```text
branch = main
HEAD = 609d3063ee9e707dae8b2cc7834647b617c2f5a1
HEAD^ = 621c1a374fe6ad42731c6249c68a39421eeda395
index empty
tracked clean
Git-visible untracked = 0
```

Require failed Tasks still active byte-exact:

```text
.aiassistant/tasks/active/20260914_2216_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-genesis-enabled-retry-1.md
SHA = 08efe3cb3d73923f0b4f843e001232ff974621409fb93316c0b38ba38f0ea508

.aiassistant/tasks/active/20260914_2216_aiscc-p2-4-golden-agent-single-file-proof-change-2.md
SHA = 93600cafcade7e51495f6cea4f4797e6677b4e835231f19cced8d934ec5e8574
```

Require target absent:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

Preserve legacy 1400:

```text
SHA = 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Canonical state hashes remain exactly:

```text
CURRENT_STATE_SUMMARY.md
80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48

DECISION_REGISTER.md
9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5

NEXT_ACTIONS.md
050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679
```

Migration head:

```text
20260914_0012
```

# 4. Governance Commit A — close failed 2216 lineage + enter retry

Task-first transport order applies.

Move failed Tasks byte-exact:

```text
.aiassistant/tasks/active/20260914_2216_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-genesis-enabled-retry-1.md
→ .aiassistant/tasks/done/20260914_2216_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-genesis-enabled-retry-1.md

.aiassistant/tasks/active/20260914_2216_aiscc-p2-4-golden-agent-single-file-proof-change-2.md
→ .aiassistant/tasks/done/20260914_2216_aiscc-p2-4-golden-agent-single-file-proof-change-2.md
```

Place:

```text
20260914_2301_aiscc-p2-4-2216-golden-driver-failure-retry-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_2301_aiscc-p2-4-2216-golden-driver-composition-failure-retry-authorization-1.md
-> .aiassistant/reports/aiscc/
```

Stage EXACTLY the four resulting project paths:

```text
.aiassistant/tasks/done/20260914_2216_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-genesis-enabled-retry-1.md
.aiassistant/tasks/done/20260914_2216_aiscc-p2-4-golden-agent-single-file-proof-change-2.md
.aiassistant/records/aiscc/cycles/20260914_2301_aiscc-p2-4-2216-golden-driver-failure-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_2301_aiscc-p2-4-2216-golden-driver-composition-failure-retry-authorization-1.md
```

Commit message exactly:

```text
docs(aiscc): record failed golden driver attempt and retry
```

Require Commit A parent = `609d3063ee9e707dae8b2cc7834647b617c2f5a1`, exact four paths, clean index/worktree.

Commit A becomes the fresh golden repository base.

# 5. fresh runtime identity

Do NOT reuse the failed 2216 operational lineage.

Use:

```text
project_id:
aiscc-self-dogfood-p2-4-golden-2

genesis_authority_id:
aiscc-golden-genesis-2

genesis_selection_id:
aiscc-golden-genesis-selection-2

contract_id:
aiscc-p2-4-golden-cycle-2

contract_version:
1

work_run_id:
aiscc-p2-4-golden-workrun-2

READY transition request:
aiscc-golden-ready-2

RUNNING transition request:
aiscc-golden-running-2
```

Other durable IDs may be owner-generated but must be new.

Do not import the deleted prior operational database or fabricate recovery.

# 6. actual operational boundary

This is actual runtime, not pytest.

Forbidden:

```text
tests.* imports
pytest fixtures
monkeypatch
direct owner-table writes
fake owner rows
Replay/Markdown current authority substitution
manual register_start/register_submission as authenticity
```

One Task-owned `postgres:17.6`, `--pull=never`, loopback-only, empty DB upgraded to 0012.

# 7. repeat accepted owner chain

Repeat the accepted truthful flow using the fresh identity:

```text
P1-6/P1-7 owner configuration
→ SELF_DOGFOOD_GENESIS authority
→ genesis current selection
→ genesis-backed TaskContract
→ materialized SelfDogfoodTaskSpec
→ READY/v1
→ external IDE start
→ RUNNING/v2
→ clean completion lease before edit
```

All prior 2216 owner/API restrictions still apply.

# 8. mandatory driver correction at governed edit boundary

The 2216 failure must be corrected ONLY in the Task-owned operational driver.

Immediately before opening the target file:

```python
target = ROOT / TARGET
target.parent.mkdir(parents=True, exist_ok=True)
with target.open("xb") as file:
    file.write(EXACT_TARGET_BYTES)
```

Equivalent exact safe code is allowed.

Requirements:

```text
parent directory creation happens only after RUNNING and clean completion lease
target file itself did not exist before this point
mkdir creates no governed second file
no product source/config/test/rule/migration modification
```

Do not commit the driver.

# 9. governed Agent edit

Create exactly:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

with exact package bytes.

Require:

```text
SHA = 7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
git diff --check PASS
changed file path = exact one
unauthorized source diff = 0
```

No other governed file.

# 10. trusted completion

Complete through the accepted durable external IDE completion flow.

Require trusted LocalGitObserver proves:

```text
HEAD = retry Governance Commit A
target path exact
target SHA exact
index expected
diff-check PASS
unauthorized path count = 0
stable observation
```

Persist immutable external submission and owner-verified common ExecutionSubmissionRef.

# 11. P1-6 evidence

Admit owner-authenticated execution evidence for:

```text
WorkRun/TaskContract
external submission
inner Task SHA
target path
target SHA
diff-check PASS
unauthorized count 0
```

Restart/recompose and verify historical external producer.

# 12. structured NEXT_ACTION_CONTEXT evidence

Use the production/source-owned System observation/durable P1-6 path identified in 2216 source audit.

No tests.* issuer and no direct row write.

Admit the exact structured `next_action_context` needed by P1-8 Cycle admission.

If only fabricated/test-only path is available:

```text
GOLDEN_NEXT_ACTION_CONTEXT_EVIDENCE_GAP
```

STOP.

# 13. Judgment and terminal ACCEPTED

Evaluate satisfied P1-6 requirement set/checkpoint.

Use existing:

```text
SYSTEM_DETERMINISTIC
human = NOT_REQUIRED
```

Judgment authority.

Drive source-owned P1-4 transition sequence to terminal:

```text
Judgment = ACCEPTED
WorkRun = ACCEPTED
```

No HumanResult.

# 14. first real Cycle

Admit exactly one real P1-8 Cycle through owner APIs.

Bind Genesis NextAction, Task, TaskContract, WorkRun/transitions, external start/submission,
Evidence/satisfaction, Judgment, structured NEXT_ACTION_CONTEXT and `AISCC_SELF_DOGFOOD`.

Then require:

```text
Genesis currentness = permanently DENY
historical Genesis selection = replayable
normal P1-8 current memory exists
```

# 15. Result Commit B

Only after real Cycle admission.

Stage EXACTLY:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

Commit message exactly:

```text
docs(aiscc): prove first self dogfood golden cycle
```

Require parent = retry Governance Commit A, exact one changed path, target hash exact.

# 16. resulting NextAction

After Commit B select using real first Cycle/current memory.

Required source mode:

```text
CYCLE_DERIVED
```

Expected supported action:

```text
open-cycle-derived-task-issuance
```

Owner currentness verifier must PASS.

Otherwise STOP `GOLDEN_NEXT_ACTION_UNAVAILABLE`.

# 17. success Task lifecycle

After full success only:

```text
new outer Task active -> done byte-exact
new inner Task active -> done byte-exact
```

Do not include them in Commit B.

Terminal Git-visible untracked exactly the two new done Tasks.

# 18. export

Export full golden owner-read provenance:

```text
GOLDEN_GENESIS.json
GOLDEN_TASKCONTRACT.json
GOLDEN_SPEC.json
GOLDEN_WORKRUN.json
GOLDEN_TRANSITIONS.json
GOLDEN_EXTERNAL_START.json
GOLDEN_EXTERNAL_SUBMISSION.json
GOLDEN_EVIDENCE.json
GOLDEN_JUDGMENT.json
GOLDEN_CYCLE.json
GOLDEN_NEXT_ACTION.json
GOLDEN_PROVENANCE.json
GOLDEN_PROVENANCE_ROOT.md
```

Also export runtime driver and explicitly prove its parent-directory fix.

No raw capabilities/credentials/private DB URL.

# 19. cleanup and terminal

After exports/hashes:

```text
remove exact Task-owned PostgreSQL container/volume
no prune
```

Require:

```text
migration head 0012
canonical state unchanged
legacy 1400 unchanged
Docker residue 0
index empty
tracked clean
```

# 20. prohibited

No product runtime/test/rule/migration/canonical-state change.
No provider/LLM/external network.
No push/deploy.
No recovery/bypass of the failed 2216 lease.
No second edit path.
No fabricated authority.

# 21. blockers

```text
BLOCKED_MISSING_ARTIFACT
DIRTY_WORKSPACE_MIXED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
GOLDEN_AUTHORITY_GAP
GOLDEN_EVIDENCE_INGRESS_UNAVAILABLE
GOLDEN_NEXT_ACTION_CONTEXT_EVIDENCE_GAP
GOLDEN_JUDGMENT_POLICY_UNAVAILABLE
GOLDEN_NEXT_ACTION_UNAVAILABLE
ISOLATED_POSTGRES_IMAGE_MISSING
BLOCKED_REQUIRED_EVIDENCE
SECURITY_BOUNDARY_BLOCKED
```

# 22. success ceiling

Only:

```text
P2_4_FIRST_SELF_DOGFOOD_GOLDEN_CYCLE_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do not claim P2-4 CLOSED or state reconciliation.
