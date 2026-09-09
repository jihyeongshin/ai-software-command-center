# 작업지시서: P2-3 Phase 1A final acceptance Git persistence

## meta

- task_id: `20260909_0115_aiscc-p2-3-phase1a-final-acceptance-git-persistence-1`
- created_at: `2026-09-09T01:15:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / GIT_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `4cadcb45b44d5bb2a260d7fa9350626ce28ea875`
- required_base_tree: `7d98df6f74eba74427d1be3b0abe9a78ef91a29f`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `QA-only rework → exact Git staging/commit persistence authority`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260909_0115_aiscc-p2-3-phase1a-final-acceptance-git-persistence-1.md

CYCLE:
20260909_0115_aiscc-p2-3-phase1a-static-contract-accepted-persistence-entry-1.cycle.md
SHA-256:
aece031d6a9984542e7ed4f9982627a90608d91d18d3ba9af48ff32a692a8139
destination:
.aiassistant/records/aiscc/cycles/20260909_0115_aiscc-p2-3-phase1a-static-contract-accepted-persistence-entry-1.cycle.md

JUDGMENT:
20260909_0115_aiscc-p2-3-phase1a-static-contract-final-acceptance-judgment-1.md
SHA-256:
f7b953fb4600709c99fe0401d4bce9b298a76dc56f00f8a3c183dd37edd12fb4
destination:
.aiassistant/reports/aiscc/20260909_0115_aiscc-p2-3-phase1a-static-contract-final-acceptance-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260909_0115_aiscc-p2-3-phase1a-final-acceptance-git-persistence-1.md
```

Read it, then place/verify current CYCLE/JUDGMENT.

Bootstrap failures follow the persisted ZIP-direct workflow.

After canonical transport, inbound cleanup refusal is non-blocking.

# 1. repository gate

After current artifact placement require:

```text
branch:
main

HEAD:
4cadcb45b44d5bb2a260d7fa9350626ce28ea875

HEAD tree:
7d98df6f74eba74427d1be3b0abe9a78ef91a29f

index:
empty
```

Expected Git-visible set excluding current active Task:

```text
28 exact
```

Exact paths:

- `.aiassistant/tasks/done/20260908_2330_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-2.md`
- `.aiassistant/records/aiscc/cycles/20260908_2330_aiscc-p2-3-decision-register-reconciliation-accepted-source-audit-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_2330_aiscc-p2-3-decision-register-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_0008_aiscc-p2-3-phase1a-static-scenario-resource-contract-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_0008_aiscc-p2-3-source-contract-audit-accepted-phase1a-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_0008_aiscc-p2-3-source-contract-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_0110_aiscc-p2-3-phase1a-windows-pytest-parameter-id-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_0110_aiscc-p2-3-phase1a-test-failure-parameter-id-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_0110_aiscc-p2-3-phase1a-test-failure-parameter-id-judgment-1.md`
- `config/scenarios/schemas/resource-v1.schema.json`
- `config/scenarios/schemas/scenario-v1.schema.json`
- `config/scenarios/stockroom/v1/catalog.json`
- `config/scenarios/stockroom/v1/resource.json`
- `config/scenarios/stockroom/v1/s1-normal.json`
- `config/scenarios/stockroom/v1/s2-missing-evidence.json`
- `config/scenarios/stockroom/v1/s3-policy-conflict.json`
- `config/scenarios/stockroom/v1/s4-human-owned-claim.json`
- `config/scenarios/stockroom/v1/fixtures/missing-evidence.json`
- `config/scenarios/stockroom/v1/fixtures/policy-conflict.json`
- `config/scenarios/stockroom/v1/fixtures/human-owned-claim.json`
- `src/aiscc/scenarios/__init__.py`
- `src/aiscc/scenarios/models.py`
- `src/aiscc/scenarios/catalog.py`
- `tests/unit/scenarios/test_catalog.py`
- `tests/unit/scenarios/test_resource_identity.py`
- `tests/unit/scenarios/test_contracts.py`
- `.aiassistant/records/aiscc/cycles/20260909_0115_aiscc-p2-3-phase1a-static-contract-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_0115_aiscc-p2-3-phase1a-static-contract-final-acceptance-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup, restore, absorb, stash or reset.

# 2. accepted predecessor byte identity — exact 26

Verify every accepted predecessor path before staging:

- `.aiassistant/tasks/done/20260908_2330_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-2.md`  `1b55a92948cbad4fb86e1d48f5925f38faee8d9662a9da71d320cef1d88bb284`
- `.aiassistant/records/aiscc/cycles/20260908_2330_aiscc-p2-3-decision-register-reconciliation-accepted-source-audit-retry-entry-1.cycle.md`  `016afc405faa85dd0725445ceb8c559130f1d4c58b3fdaf05827d806dc567f61`
- `.aiassistant/reports/aiscc/20260908_2330_aiscc-p2-3-decision-register-reconciliation-final-acceptance-judgment-1.md`  `e93888c32e371d95961286ebe626344a3251c121aadb780c27888bff510872d0`
- `.aiassistant/tasks/done/20260909_0008_aiscc-p2-3-phase1a-static-scenario-resource-contract-implementation-1.md`  `739297691177f9bf6338eec3cdd03279b067847da3f07ce3ad31064710c7e4ca`
- `.aiassistant/records/aiscc/cycles/20260909_0008_aiscc-p2-3-source-contract-audit-accepted-phase1a-entry-1.cycle.md`  `23c0b64e09ecfdf7c4bb27a1842c2be30eb6e341ffc9d25dc4835d39970e979a`
- `.aiassistant/reports/aiscc/20260909_0008_aiscc-p2-3-source-contract-audit-final-acceptance-judgment-1.md`  `ccba59565758e52c3ee89c5daf0bcda0dd6baefe767754497ea2afa14da381a3`
- `.aiassistant/tasks/done/20260909_0110_aiscc-p2-3-phase1a-windows-pytest-parameter-id-rework-1.md`  `5932ecd52de5907a4a958b9ad815c5899965d63490547c1e39cff753aab0c3af`
- `.aiassistant/records/aiscc/cycles/20260909_0110_aiscc-p2-3-phase1a-test-failure-parameter-id-rework-entry-1.cycle.md`  `f9fc4e87ef383b97516dc3bd900d48775b187e2c50f6da473ac1e7609888b6f2`
- `.aiassistant/reports/aiscc/20260909_0110_aiscc-p2-3-phase1a-test-failure-parameter-id-judgment-1.md`  `c8bcb571191cbf647cd54fa8d65b1b99837e757d76423e5a1d2cd46aa553f607`
- `config/scenarios/schemas/resource-v1.schema.json`  `bc4d25c0f898e6c78d6df0b4b359ee0b990094bf590666124dbe5c2fa60e8cb5`
- `config/scenarios/schemas/scenario-v1.schema.json`  `8ed61bb2dbb6c2391ad3dc0440f855cf47d3c7947c3d4e2beda700fce7949823`
- `config/scenarios/stockroom/v1/catalog.json`  `bbc94776d53c06b472ab8879971a0d52f7901f600e3e88f4dadd1abc0d37cd17`
- `config/scenarios/stockroom/v1/resource.json`  `a5b8c8a5bd7165073f37647eb791df0bc59aa7b73033d59dd5f3967bbff28a99`
- `config/scenarios/stockroom/v1/s1-normal.json`  `fcca50e5876c4b276cc0f3ab865abc1eae8376e3e4dd68f7d675878a1b1cccc8`
- `config/scenarios/stockroom/v1/s2-missing-evidence.json`  `7473b8ec6b808866f16184edf4267ce7b2757e32c7205feb646c25041f938f51`
- `config/scenarios/stockroom/v1/s3-policy-conflict.json`  `73704589a51f59228bb72e770532f9153d35183cf3c1708e5db5ab80f6220cbe`
- `config/scenarios/stockroom/v1/s4-human-owned-claim.json`  `f364408f8874967b693b80c05144d23e382a40fe5d368e330908548af3938d29`
- `config/scenarios/stockroom/v1/fixtures/missing-evidence.json`  `c9a430ae61452b841e6deb06220cf59b748d57e698aa6108ca8966f522a04d1c`
- `config/scenarios/stockroom/v1/fixtures/policy-conflict.json`  `f01d061b5625d3c5f1e0f154f2f8eca97e3b64a6bd5e77551231b836be31bb91`
- `config/scenarios/stockroom/v1/fixtures/human-owned-claim.json`  `1a4ab952c40e43680e5d352928d2e076e8957d71acdc9dfa4cbf4793e3a7d5d4`
- `src/aiscc/scenarios/__init__.py`  `18a0f227f6c9633de56b03dcf746edc59f315e368692446a18040a8c92d1323c`
- `src/aiscc/scenarios/models.py`  `09936eaa8c59dfcca7afd4fef9fdad31c7b5e97e576abf396854a826daf4190a`
- `src/aiscc/scenarios/catalog.py`  `597a0788700d3302808b72771230636a5e5959ad68fea08183f457c9379e5a2d`
- `tests/unit/scenarios/test_catalog.py`  `3e86e9981903dafbeba92957e091e0c6276ab150244bfd075f844c32d0a4121a`
- `tests/unit/scenarios/test_resource_identity.py`  `d5a0e2b125bc355f37c6e25e701c0281a42b1d97dfc52236409e004f6e3013fd`
- `tests/unit/scenarios/test_contracts.py`  `d72b4f2acccefb8b0dd5069005b49d21f90a12424adf79e8e5de4906171b2784`

Require:

```text
26 / 26 exact
```

Any mismatch:

```text
ACCEPTED_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

Do not repair or rerun implementation.

# 3. accepted evidence reuse

If all 26 hashes are exact, reuse:

```text
2330 source/contract design:
ACCEPTED

0008 Phase 1A implementation candidate:
accepted except prior test-environment blocker

0110 bounded rework:
ACCEPTED

0110 exact Windows suite:
113 / 113 PASS
```

Do not rerun tests unless byte identity cannot be established.

Do not edit any product/config/test/governance file.

# 4. current provenance identity

Verify current issued:

```text
.aiassistant/records/aiscc/cycles/20260909_0115_aiscc-p2-3-phase1a-static-contract-accepted-persistence-entry-1.cycle.md
SHA-256:
aece031d6a9984542e7ed4f9982627a90608d91d18d3ba9af48ff32a692a8139

.aiassistant/reports/aiscc/20260909_0115_aiscc-p2-3-phase1a-static-contract-final-acceptance-judgment-1.md
SHA-256:
f7b953fb4600709c99fe0401d4bce9b298a76dc56f00f8a3c183dd37edd12fb4
```

Current TASK integrity is anchored by the verified delivery ZIP and canonical byte equality.

# 5. pre-stage integrity

Require:

```text
git diff --check:
PASS

index:
empty

Git-visible:
28 exact excluding active Task

existing tracked-file modifications:
0
```

No generated cache/pyc/pytest residue may be Git-visible.

# 6. Task lifecycle

Move exact current Task:

```text
.aiassistant/tasks/active/20260909_0115_aiscc-p2-3-phase1a-final-acceptance-git-persistence-1.md
→
.aiassistant/tasks/done/20260909_0115_aiscc-p2-3-phase1a-final-acceptance-git-persistence-1.md
```

Do not edit its bytes.

Then require final Git-visible commit candidate:

```text
29 exact paths
```

# 7. exact final commit allowlist — 29

- `.aiassistant/tasks/done/20260908_2330_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-2.md`
- `.aiassistant/records/aiscc/cycles/20260908_2330_aiscc-p2-3-decision-register-reconciliation-accepted-source-audit-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_2330_aiscc-p2-3-decision-register-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_0008_aiscc-p2-3-phase1a-static-scenario-resource-contract-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_0008_aiscc-p2-3-source-contract-audit-accepted-phase1a-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_0008_aiscc-p2-3-source-contract-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_0110_aiscc-p2-3-phase1a-windows-pytest-parameter-id-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_0110_aiscc-p2-3-phase1a-test-failure-parameter-id-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_0110_aiscc-p2-3-phase1a-test-failure-parameter-id-judgment-1.md`
- `config/scenarios/schemas/resource-v1.schema.json`
- `config/scenarios/schemas/scenario-v1.schema.json`
- `config/scenarios/stockroom/v1/catalog.json`
- `config/scenarios/stockroom/v1/resource.json`
- `config/scenarios/stockroom/v1/s1-normal.json`
- `config/scenarios/stockroom/v1/s2-missing-evidence.json`
- `config/scenarios/stockroom/v1/s3-policy-conflict.json`
- `config/scenarios/stockroom/v1/s4-human-owned-claim.json`
- `config/scenarios/stockroom/v1/fixtures/missing-evidence.json`
- `config/scenarios/stockroom/v1/fixtures/policy-conflict.json`
- `config/scenarios/stockroom/v1/fixtures/human-owned-claim.json`
- `src/aiscc/scenarios/__init__.py`
- `src/aiscc/scenarios/models.py`
- `src/aiscc/scenarios/catalog.py`
- `tests/unit/scenarios/test_catalog.py`
- `tests/unit/scenarios/test_resource_identity.py`
- `tests/unit/scenarios/test_contracts.py`
- `.aiassistant/records/aiscc/cycles/20260909_0115_aiscc-p2-3-phase1a-static-contract-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_0115_aiscc-p2-3-phase1a-static-contract-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_0115_aiscc-p2-3-phase1a-final-acceptance-git-persistence-1.md`

No other path may be staged.

# 8. exact Git persistence

Only after all prior gates PASS:

```text
git add -- <29 exact literal paths>
git diff --cached --check
git diff --cached --name-status
```

Require:

```text
staged:
29 exact

extra:
0

missing:
0

unstaged tracked changes:
0
```

Then:

```text
git commit -m "feat(scenarios): persist P2-3 Phase 1A static contracts"
```

Expected:

```text
parent:
4cadcb45b44d5bb2a260d7fa9350626ce28ea875

parent count:
1

message:
feat(scenarios): persist P2-3 Phase 1A static contracts

changed paths:
29 exact
```

Forbidden:

```text
git add -A
git add .
git reset
git restore
git checkout
git stash
git clean
git push
git pull
git fetch
git merge
git rebase
git cherry-pick
```

# 9. post-commit verification

Verify:

1. commit hash/tree
2. exact parent `4cadcb45b44d5bb2a260d7fa9350626ce28ea875`
3. parent count 1
4. exact commit message
5. changed paths 29 exact
6. accepted predecessor 26 committed bytes equal expected hashes
7. current Cycle/Judgment/Task committed bytes equal issued bytes
8. index empty
9. Git-visible worktree clean
10. no generated cache/pyc/pytest residue
11. push/network NOT_RUN

# 10. source/test semantic checks after commit

Without modifying files, verify committed Phase 1A still contains:

```text
4 exact scenario IDs
scenario version 1.0.0
exact Synthetic Stockroom resource_ref
11 config JSON files
five-way evidence contract
test_catalog explicit short IDs including oversize
```

Do not execute runtime scenarios/provider/DB/Replay.

No test rerun is required because exact accepted hashes are the persistence proof.

# 11. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260909_0115_aiscc-p2-3-phase1a-final-acceptance-git-persistence-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
CANDIDATE_IDENTITY_VERIFICATION.md
GIT_PERSISTENCE_VERIFICATION.md
```

Include byte-preserving committed copies of all 29 commit paths.

After folder completion create adjacent:

```text
.aiassistant/reports/target/20260909_0115_aiscc-p2-3-phase1a-final-acceptance-git-persistence-1.zip
```

Require:

```text
one top-level bundle directory
readable/CRC PASS
required root files present
29 committed project-relative copies present
manifest coverage
source/commit/export byte equality
folder/archive byte equality
```

Keep both folder and outbound ZIP.

# 12. inbound cleanup

After terminal result/outbound ZIP validation, attempt exact inbound delivery ZIP cleanup best-effort.

Failure:

```text
NON_BLOCKING_LOCAL_RESIDUE
```

No alternate deletion fallback or broad Downloads cleanup.

# 13. evidence contract

executor_required:

- inbound ZIP/artifact transport
- exact 28-path workspace gate
- 26-path accepted candidate identity
- exact 29-path staging
- exact Git commit persistence
- post-commit clean state
- committed semantic identity
- outbound result ZIP

reuse_allowed:

- 2330 accepted design
- 0110 accepted candidate and 113/113 Windows unit result under exact byte identity

human_owned:

```text
new Human QA:
NOT_REQUIRED

public license:
HUMAN_PENDING / outside Task
```

forbidden:

- source/config/test re-edit
- runtime enrollment/materialization
- scenario execution
- DB
- Replay
- public admission
- Git network/push
- P2-4/P3

# 14. mandatory stop

```text
DOWNLOAD_ZIP_MISSING
DOWNLOAD_ZIP_HASH_MISMATCH
DOWNLOAD_ZIP_CORRUPT
DOWNLOAD_TASK_MEMBER_MISSING
DOWNLOAD_TASK_PLACEMENT_FAILED
TRANSPORT_FAILURE
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
ACCEPTED_CANDIDATE_IDENTITY_MISMATCH
GIT_STAGE_ALLOWLIST_MISMATCH
GIT_COMMIT_VERIFICATION_FAILED
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

Inbound cleanup refusal after canonical transport is non-blocking.

# 15. final ceiling

Success:

```text
P2-3 Phase 1A static scenario/resource contract:
PERSISTED / READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-3 Phase 1B runtime materialization/enrollment:
NOT_STARTED

P2-3 actual run capture:
NOT_STARTED

P2-3 Replay:
NOT_STARTED
```

Do not declare P2-3 closed.
