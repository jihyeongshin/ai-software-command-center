# 작업지시서: P2-4 Self-Dogfood Genesis Bootstrap Authority Implementation

## meta

- task_id: `20260914_2010_aiscc-p2-4-self-dogfood-genesis-bootstrap-authority-implementation-1`
- created_at: `2026-09-14T20:10:00+09:00`
- work_type: `HUMAN_ACCEPTED_P1_8_GENESIS_AUTHORITY_IMPLEMENTATION + TASKCONTRACT_SOURCE_EXTENSION + OPTIONAL_ADDITIVE_MIGRATION + QA + GIT_PERSISTENCE`
- evidence_profile: `CRITICAL_AUTHORITY_EXTENSION`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `e9b38c0c60e940241ec0221136a41481ddc8e1a5`
- required_parent: `6eedc50c567f552a3b9d2902c95bd71a99ca441f`
- predecessor_result_zip_sha256: `6d55681e007a4039d26747aa351a9317fd389d35efb140e824ebb2d4f1d922e1`
- predecessor_done_task_sha256: `9d8964eaa9ca5fbbb9de5e7ea013a9d36f2184bed3e216a1cc31c0e7d4fe8905`
- predecessor_result: `BLOCKED / SELF_DOGFOOD_BOOTSTRAP_AUTHORITY_MISSING`
- predecessor_disposition: `ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED`
- Human_design_decision: `HUMAN_PROVIDED / ACCEPTED`
- Human_review_sha256: `09c93a9a67ca064bd269240787b8fdd5380f05693f4394dc74bba778c9f0da8a`
- accepted_design_id: `AISCC-P1-8-SELF-DOGFOOD-GENESIS-BOOTSTRAP-V1`
- fresh_IDE_chat_required: `No`
- governance_commit_authorized: `Yes / exact 4 paths / Commit A`
- result_commit_authorized: `Yes / bounded genesis implementation allowlist / Commit B`
- optional_migration_authorized: `Yes / at most one additive 20260914_0012 after 0011, only if truthful persistence requires it`
- actual_golden_cycle_authorized: `No`
- real_AISCC_Agent_source_change_authorized: `No`
- provider_LLM_network_authorized: `No`
- Docker_authorized: `Yes / local postgres:17.6 isolated implementation proof only`
- retained_private_DB_authorized: `No`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_SELF_DOGFOOD_GENESIS_AUTHORITY_IMPLEMENTATION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. Human acceptance

Human decision:

```text
ACCEPT
```

Applies exactly to:

```text
20260914_1916_aiscc-p2-4-self-dogfood-genesis-bootstrap-authority-human-review-1.md

SHA-256:
09c93a9a67ca064bd269240787b8fdd5380f05693f4394dc74bba778c9f0da8a
```

Admit as:

```text
HUMAN_PROVIDED / ACCEPTED
```

Normative design:

```text
AISCC-P1-8-SELF-DOGFOOD-GENESIS-BOOTSTRAP-V1
```

This Task implements the genesis authority only.
It MUST NOT retry the actual golden cycle.

# 1. predecessor blocker acceptance

1916 is accepted as truthful fail-closed.

```text
Result ZIP:
6d55681e007a4039d26747aa351a9317fd389d35efb140e824ebb2d4f1d922e1

49 members
48 manifest rows
CRC PASS
48/48 manifest size/SHA exact

Governance Commit A:
e9b38c0c60e940241ec0221136a41481ddc8e1a5

parent:
6eedc50c567f552a3b9d2902c95bd71a99ca441f

Result Commit B:
NONE

operational PostgreSQL / TaskContract / WorkRun / source edit / Evidence / Judgment / runtime Cycle:
NOT CREATED
```

The exact recursion is:

```text
first cycle-derived NextAction
requires prior Cycle/current memory

prior Cycle
requires prior accepted WorkRun/evidence/Judgment

first WorkRun
requires first NextAction/TaskContract
```

# 2. accepted correction

Add exactly:

```text
source mode:
SELF_DOGFOOD_GENESIS

action:
open-self-dogfood-genesis-task-issuance
```

Steady state remains:

```text
CYCLE_DERIVED
open-cycle-derived-task-issuance
```

TaskContract V1 supported sources become exactly:

```text
SELF_DOGFOOD_GENESIS
CYCLE_DERIVED
```

and still reject:

```text
OPERATIONAL_RECOVERY
```

# 3. predecessor evidence

- `CONTRACT_REVIEW.md`: `f02ff15fb6e462bb6489493bc240ce15b89987211061341a23253961ad037216`
- `EXECUTOR_REPORT.md`: `19cd15d62da973b817e646c189ebd1b6f3bd69fc3320d940f50b990cc8ecd80b`
- `GOLDEN_RUNTIME_SOURCE_AUDIT.md`: `015b3901c0a8aa02e9679b2c012e5ecd70fa8f1e20df380f67644c411fa5d273`
- `WORKSPACE_VERIFICATION.md`: `73d3574b69ab06bd2ce98ae0fb66a5eb8035875231781c4c6f99b31fe7d4d9f6`
- `evidence/COMMIT_A.json`: `1a20030e8baf0cefd7c021313f4d52db943a2b839f1218170fe915e006bd4cb4`
- `evidence/FINAL_STATIC_CHECKS.json`: `88cb81505e2a78cdbcd2962237c616fa5ea6ff55925b4b75d6b6538471be3c9d`
- `evidence/INITIAL_HASHES.json`: `05bf76b2861ebd7f9031f8d82267e10a1d4e238d848b11b09cfd1c7f05a51aaf`
- `evidence/SOURCE_INVENTORY.json`: `d2474519dd196c0f30fb82798d9bd6b25fc161fc90e355b8b4243904cf281d5f`
- `evidence/TERMINAL_WORKSPACE.json`: `aaa7830e4cf8e73089cc929534431c02f2a04311130f227b2324b49364a34109`

After Task-first read, copy only under:

```text
.aiassistant/reports/target/20260914_2010_aiscc-p2-4-self-dogfood-genesis-bootstrap-authority-implementation-1/accepted-input/
```

Human review must also be copied there byte-exact.

# 4. exact repository preflight

Require:

```text
branch = main
HEAD = e9b38c0c60e940241ec0221136a41481ddc8e1a5
HEAD^ = 6eedc50c567f552a3b9d2902c95bd71a99ca441f
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1916_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-fresh-ide-1.md
```

Done Task SHA:

```text
9d8964eaa9ca5fbbb9de5e7ea013a9d36f2184bed3e216a1cc31c0e7d4fe8905
```

Preserve:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Canonical state hashes must remain:

```text
CURRENT_STATE_SUMMARY.md
80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48

DECISION_REGISTER.md
9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5

NEXT_ACTIONS.md
050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679
```

Migration code head initially:

```text
20260914_0011
```

Known key hashes:

- `src/aiscc/next_action/repository.py`: `65328357532182e0fdb79798829a923b158f62329577c0edd13dc300980cd666`
- `src/aiscc/next_action/models.py`: `09d5c13d73f2bb1cd4ef05433f73f40eedcb670353dcfae9cdbf480420af1ea6`
- `src/aiscc/task_authority/repository.py`: `b7bc107e4d7805605c3dbc4c96157d623824759fbb2b4012335db9d575ce8500`
- `.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md`: `7cf27b77bb961280becfc55ecf8e71c9406da9b7b91df0d2697132c2655108db`

Any mismatch -> fail closed.

# 5. fixed executables

Use only repository `.venv\Scripts\python.exe`, exact Git `C:\Program Files\Git\cmd\git.exe`,
and exact Docker `C:\Program Files\Docker\Docker\resources\bin\docker.exe` when authorized.
No PATH substitution. No Docker pull.

# 6. Governance Commit A

After Task-first read + preflight, place:

```text
20260914_2010_aiscc-p2-4-genesis-authority-human-accepted-implementation-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_2010_aiscc-p2-4-genesis-authority-design-human-acceptance-implementation-authorization-1.md
-> .aiassistant/reports/aiscc/

20260914_1916_aiscc-p2-4-self-dogfood-genesis-bootstrap-authority-human-review-1.md
-> .aiassistant/reports/aiscc/
```

Stage EXACTLY:

```text
.aiassistant/tasks/done/20260914_1916_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-fresh-ide-1.md
.aiassistant/records/aiscc/cycles/20260914_2010_aiscc-p2-4-genesis-authority-human-accepted-implementation-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_2010_aiscc-p2-4-genesis-authority-design-human-acceptance-implementation-authorization-1.md
.aiassistant/reports/aiscc/20260914_1916_aiscc-p2-4-self-dogfood-genesis-bootstrap-authority-human-review-1.md
```

Commit message:

```text
docs(aiscc): accept self dogfood genesis authority design
```

Require exact 4 paths, parent `e9b38c0c60e940241ec0221136a41481ddc8e1a5`, index empty, tracked clean.

# 7. mandatory source audit before mutation

Audit:

```text
src/aiscc/next_action/**
src/aiscc/task_authority/**
src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py

.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
```

Read cycle/memory owners only.

Create `GENESIS_SOURCE_AUTHORITY_AUDIT.md` enumerating:
- every source/selection enum exhaustive branch;
- action catalog/count assumptions;
- CYCLE_DERIVED memory/Cycle requirements;
- OPERATIONAL_RECOVERY preserved branch;
- TaskContract source gate and lock sequence;
- persistence fields that force Cycle/memory provenance;
- every exact `20260914_0011` migration-head assertion;
- every direct test assuming only existing source modes/action descriptors.

Any extra semantic owner -> `AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED`.
Any additional mutation path -> `SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED`.

# 8. genesis source and action

Add exact source mode:

```text
SELF_DOGFOOD_GENESIS
```

Add exact action:

```text
open-self-dogfood-genesis-task-issuance
```

Never alias it to CYCLE_DERIVED or OPERATIONAL_RECOVERY.
No automatic fallback into genesis.

Genesis descriptor must not fabricate `source_cycle_id`, memory refs, or CycleMemoryReference.

# 9. durable genesis authority

Implement immutable owner-issued authority equivalent to `GenesisNextActionAuthorityV1`, binding:

```text
project_id
genesis_authority_id
source_mode
action_id
repository_id
repository_root
base_commit
phase_id
runtime_mode = OWNER_SELF_DOGFOOD
cycle_execution_mode = AISCC_SELF_DOGFOOD
issuer identity/version
issued_at
canonical authority fingerprint
```

No predecessor WorkRun/Cycle identity exists.

# 10. exact eligibility/currentness

Genesis current only when ALL:

```text
no admitted operational Cycle
no CURRENT NEXT_ACTION_CONTEXT memory lineage
no prior completed genesis bootstrap
no conflicting current NextAction selection
repo/root/base exact
phase exact
runtime mode exact
```

Any real operational Cycle or current cycle-derived context -> `GENESIS_NOT_ELIGIBLE`.

First admitted real Cycle permanently supersedes genesis.

Restart must preserve current/non-current outcome.

# 11. persistence choice

If current P1-8 schema cannot represent genesis without false Cycle fields, create:

```text
migrations/versions/20260914_0012_self_dogfood_genesis_authority.py
revision = 20260914_0012
down_revision = 20260914_0011
```

Use minimal additive immutable append-only authority persistence.
No fake nullable Cycle semantics, no backfill, UPDATE/DELETE/TRUNCATE denied,
empty-only downgrade, nonempty downgrade fail-closed.

If current schema already truthfully represents genesis, do not add migration.

# 12. TaskContract V1 extension

Support exactly:

```text
SELF_DOGFOOD_GENESIS
CYCLE_DERIVED
```

Continue denying:

```text
OPERATIONAL_RECOVERY
```

Genesis issuance must verify exact current genesis authority/action/project/repo/base/phase/modes
and bind its authority identity/fingerprint without fake Cycle provenance.

# 13. lock invariant

Preserve:

```text
TaskContract issuer/revoker never acquire WorkRun locks
```

Genesis lock shape:

```text
TaskContract family lock
+
genesis authority/currentness lock
```

No predecessor WorkRun lock.

# 14. one-time genesis/idempotency

One operational project lineage -> at most one genesis TaskContract family.

Exact retry -> same durable result.
Changed body -> DENY.
Second distinct genesis authority/task family -> DENY.

After first Cycle -> all new genesis issuance/currentness DENY.

# 15. first-Cycle transition proof

Using existing P1-8 owner APIs in integration tests, prove:

```text
empty project -> genesis current
genesis TaskContract -> PASS
first real owner-admitted Cycle -> genesis permanently non-current
post-Cycle cycle-derived path remains valid
```

Do not directly insert Cycle/memory rows.
Do not import Replay/Markdown as current authority.

# 16. prohibited authority substitutions

Forbidden:

```text
Replay import as current authority
Browser/canonical Markdown -> runtime rows
operational recovery relabeled genesis
fake WorkRun/Cycle/memory refs
LLM first-action selection
generic task planner/generator
```

Genesis creates no WorkRun/Evidence/Judgment/Cycle itself.

# 17. exact mutation allowlist

Canonical rules:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
```

P1-8:

```text
src/aiscc/next_action/models.py
src/aiscc/next_action/repository.py
src/aiscc/next_action/__init__.py
src/aiscc/next_action/genesis.py
```

Last two are conditional.

TaskContract:

```text
src/aiscc/task_authority/contracts.py
src/aiscc/task_authority/repository.py
src/aiscc/task_authority/__init__.py
```

`__init__.py` conditional.

Persistence:

```text
src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py
migrations/versions/20260914_0012_self_dogfood_genesis_authority.py
```

Migration conditional.

New tests:

```text
tests/unit/next_action/test_genesis_bootstrap.py
tests/integration/next_action/test_genesis_bootstrap.py
tests/unit/task_authority/test_genesis_issuance.py
tests/integration/task_authority/test_genesis_task_contract.py
```

Existing direct-contract tests conditionally authorized only for exact source/action expectations:

```text
tests/unit/task_authority/test_task_contract_issuance.py
tests/unit/task_authority/test_task_contract_body.py
tests/integration/memory/test_postgres_project_memory_next_action.py
```

If migration 0012 is created, exact-head fixture mutations authorized only for:

- `tests/integration/workflow/test_postgres_kernel.py`
- `tests/integration/task_authority/test_task_contract_durability.py`
- `tests/integration/self_dogfood/test_task_ready_entry.py`
- `tests/integration/providers/test_external_ide_execution_ingress.py`
- `tests/integration/providers/test_external_ide_execution_start.py`

Those five may change only `0011 -> 0012` strict-head expectations and direct migration-chain coverage.

Read-only semantic owners:

```text
src/aiscc/cycle/**
src/aiscc/memory/**
src/aiscc/workflow/**
src/aiscc/providers/**
src/aiscc/evidence/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/self_dogfood/**
```

# 18. canonical rule adoption

Record exact genesis semantics in the four authorized rule docs.
Do not change CURRENT_STATE_SUMMARY / DECISION_REGISTER / NEXT_ACTIONS in this Task.

# 19. PostgreSQL proof

If 0012 exists, on isolated local postgres:17.6 prove:

```text
empty -> 0012 PASS
0011 -> 0012 PASS
strict current head 0012 PASS
immutable mutation denial PASS
empty downgrade PASS
nonempty downgrade DENY preserving schema/data/revision
```

If no migration, prove current 0011 persistence is truthful for genesis and head remains 0011.

# 20. required authority tests

Prove:

```text
empty project genesis eligibility PASS
genesis issuance/currentness PASS
restart PASS
wrong repo/base/phase/runtime/action DENY
tamper DENY
duplicate different genesis DENY
exact retry idempotent
non-empty Cycle lineage genesis DENY
current cycle-derived context genesis DENY
post-first-Cycle genesis DENY
genesis creates no fake Cycle/memory/WorkRun/Judgment/Evidence
```

TaskContract proof:

```text
genesis source PASS
cycle-derived source regression PASS
operational-recovery source DENY
stale genesis DENY
changed genesis body retry DENY
restart verification PASS
issuer/revoker no WorkRun lock PASS
```

# 21. regressions

Run at minimum:

```text
tests/unit/next_action
tests/integration/next_action
tests/integration/memory
tests/unit/task_authority
tests/integration/task_authority
tests/unit/self_dogfood
tests/integration/self_dogfood
tests/unit/workflow
tests/integration/workflow
```

Run all five strict-head tests explicitly if migration 0012 is used.

Run direct CYCLE_DERIVED and OPERATIONAL_RECOVERY regressions.
No skip/xfail substitution.

# 22. static closure

Require Ruff changed Python PASS, compile PASS, git diff --check PASS,
UTF-8/no-BOM/control/fence PASS.

# 23. Result Commit B

Only after complete PASS.

```text
feat(aiscc): add self dogfood genesis authority
```

Commit only section 17 paths actually changed.

Require parent = current Governance Commit A, index empty, tracked clean,
canonical state unchanged, legacy 1400 unchanged.

# 24. export

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
HUMAN_DESIGN_ACCEPTANCE_VERIFICATION.md
GENESIS_SOURCE_AUTHORITY_AUDIT.md
GENESIS_AUTHORITY_REVIEW.md
GENESIS_CURRENTNESS_REVIEW.md
TASKCONTRACT_GENESIS_HANDOFF_REVIEW.md
LOCK_INVARIANT_REVIEW.md
MIGRATION_REVIEW.md
POSTGRES_RUNTIME_EVIDENCE.md
TEST_RESULTS.md
STATIC_CHECKS.md
CONTRACT_REVIEW.md
```

Include changed project-relative files and current Cycle/Judgment/Human review/done Task.
No credentials/raw DB dump/private DB URL.

# 25. terminal success

```text
HEAD = Result Commit B
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_2010_aiscc-p2-4-self-dogfood-genesis-bootstrap-authority-implementation-1.md
```

No Task-owned Docker residue.

# 26. blockers

```text
BLOCKED_MISSING_ARTIFACT
DIRTY_WORKSPACE_MIXED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
MIGRATION_HEAD_TEST_SCOPE_EXPANSION_REQUIRED
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
MIGRATION_BASELINE_MISMATCH
ISOLATED_POSTGRES_IMAGE_MISSING
BLOCKED_REQUIRED_EVIDENCE
SECURITY_BOUNDARY_BLOCKED
```

# 27. success ceiling

Only:

```text
P2_4_SELF_DOGFOOD_GENESIS_AUTHORITY_IMPLEMENTATION_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do NOT retry the actual golden cycle in this Task.
