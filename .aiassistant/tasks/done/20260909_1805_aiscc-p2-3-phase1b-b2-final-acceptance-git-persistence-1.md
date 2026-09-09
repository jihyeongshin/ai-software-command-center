# 작업지시서: P2-3 Phase 1B-B2 final acceptance Git persistence

## meta

- task_id: `20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-git-persistence-1`
- created_at: `2026-09-09T18:05:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / GIT_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `0f5f19c8f8109e192275d1123f90ae50120be203`
- required_base_tree: `750ea4882f5d8688d1be20ea953b710a21c1052c`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `bounded B2 source/security rework → exact Git persistence authority`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-git-persistence-1.md

CYCLE:
20260909_1805_aiscc-p2-3-phase1b-b2-accepted-persistence-entry-1.cycle.md
SHA-256:
03ee3f7d790a77a55f1a3354963c6a6e9458a183f5bac0aebba6084a3e52cfab
destination:
.aiassistant/records/aiscc/cycles/20260909_1805_aiscc-p2-3-phase1b-b2-accepted-persistence-entry-1.cycle.md

JUDGMENT:
20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-judgment-1.md
SHA-256:
7de14abcfcfba33c5cd13a18ded9214f9b9c270e405ca106037e71861409e5c4
destination:
.aiassistant/reports/aiscc/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-git-persistence-1.md
```

Read it, then place/hash-verify CYCLE/JUDGMENT.

Bootstrap failures follow the persisted ZIP-direct workflow.

After exact canonical transport, inbound cleanup refusal is non-blocking.

# 1. repository gate

After current artifact placement require:

```text
branch:
main

HEAD:
0f5f19c8f8109e192275d1123f90ae50120be203

HEAD tree:
750ea4882f5d8688d1be20ea953b710a21c1052c

index:
empty
```

Expected Git-visible set excluding current active Task:

```text
24 exact paths
```

- `.aiassistant/tasks/done/20260909_1648_aiscc-p2-3-phase1b-b2-scenario-tool-provider-security-enrollment-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1648_aiscc-p2-3-b1-state-reconciliation-accepted-b2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1648_aiscc-p2-3-b1-state-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-contract-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1800_aiscc-p2-3-phase1b-b2-test-failure-contract-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-test-failure-judgment-1.md`
- `src/aiscc/scenarios/enrollment.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/security/stockroom_policy.py`
- `config/providers/stockroom-owner-profiles.v1.toml`
- `config/providers/stockroom-tools.v1.toml`
- `config/security/stockroom-owner.v1.toml`
- `tests/unit/scenarios/test_runtime_enrollment.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/security/test_stockroom_policy.py`
- `src/aiscc/providers/ports.py`
- `src/aiscc/providers/tools.py`
- `src/aiscc/providers/service.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/security/policy.py`
- `.aiassistant/records/aiscc/cycles/20260909_1805_aiscc-p2-3-phase1b-b2-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup, restore, stash, reset or absorb.

# 2. accepted candidate byte identity — exact 22

Verify every accepted predecessor path before staging:

- `.aiassistant/tasks/done/20260909_1648_aiscc-p2-3-phase1b-b2-scenario-tool-provider-security-enrollment-implementation-1.md`  `527cb6ac675efc935dabcbffa09f5e62f4f443b779f094c6f0463c5e192521f0`
- `.aiassistant/records/aiscc/cycles/20260909_1648_aiscc-p2-3-b1-state-reconciliation-accepted-b2-entry-1.cycle.md`  `286e75593b24bf215f5c47e1339f41c5a5e3e32bdddd2cd6745cb5279db5472c`
- `.aiassistant/reports/aiscc/20260909_1648_aiscc-p2-3-b1-state-reconciliation-final-acceptance-judgment-1.md`  `643d3dbf8f8639966d78386bc632bd5645480fd7109f71f34bd179cb1807ecd6`
- `.aiassistant/tasks/done/20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-contract-rework-1.md`  `f9b3905f81f0d437466989ef066c93e9d54a5cb02023dd305c2181fa5761874d`
- `.aiassistant/records/aiscc/cycles/20260909_1800_aiscc-p2-3-phase1b-b2-test-failure-contract-rework-entry-1.cycle.md`  `4e31117d68f02a3e3d295940610ce04991e01cfc1e48230ff4f2938bbfa6c86e`
- `.aiassistant/reports/aiscc/20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-test-failure-judgment-1.md`  `cc2461db492d9a5af1d3af7e056bde30297e50d27254b7894bd370a57c9ae7a9`
- `src/aiscc/scenarios/enrollment.py`  `2903d3f5b039a244783c5db78a847b3636bd9be30fe32716fdebd5d411c9f037`
- `src/aiscc/providers/stockroom_tool.py`  `ad02321999b2b42039007c4dc6d55d20502004c137486ca33bfc191119d7dbb7`
- `src/aiscc/providers/local_deterministic.py`  `d7fd527fec919bd3488e4a22a3e24ff357d262076de83785f75698548708399d`
- `src/aiscc/security/stockroom_policy.py`  `f2ee464eb5fff2e81e183ce5b40c9423c7d7f44e47122f0c2ca6e6e31b2128b7`
- `config/providers/stockroom-owner-profiles.v1.toml`  `82de20f5a2aa76e039e685fcacbc2da44cd04b2dd863ebb9dd8e9ff7b8e37eee`
- `config/providers/stockroom-tools.v1.toml`  `223c45f224e4aba6ae7f023ed6752b4730e9889d4878cf6d4a053eed71bd457c`
- `config/security/stockroom-owner.v1.toml`  `88b3b015b3b52ceb9338025945abf5b4e422d0efe9c2a021fe7f15e46f6dae15`
- `tests/unit/scenarios/test_runtime_enrollment.py`  `26c270f8bdd5b06f41cb97427752d90a6e8de970f7e4a0f250689fe114c8c10c`
- `tests/unit/providers/test_stockroom_tool.py`  `5d3629381b97cd0d6a449b399b0f1acce156b24e17089cf229fce4feb7641f9d`
- `tests/unit/providers/test_local_deterministic.py`  `7280db790d1d942e851b67ad0f22816ab33d0af6b34e2d51813a599f9ba38870`
- `tests/unit/security/test_stockroom_policy.py`  `d76ef98f121651820c587067295d1a59bfbae12fa02ff598020cfa519124beb0`
- `src/aiscc/providers/ports.py`  `8489359ea53c28e41bdf5e0f0d4970f567f0e763bee96f9f599cffc5a5ebfec4`
- `src/aiscc/providers/tools.py`  `0718889ccf4e98eeb18486b740e741fef005b7d580abd5cfd7c8452f2ffb9b3d`
- `src/aiscc/providers/service.py`  `f21c3c29443446650e31fb0d4d0d30ceddb8956d51ad2e17221536102c6c5c18`
- `src/aiscc/runtime/docker.py`  `196b8568e950a8d422feaceb1fd6601ab7478d4f3488d4f29ddb20c7059891c5`
- `src/aiscc/security/policy.py`  `ecb008330040966436c87d24aba0245627691cb076c4c77b6778b646b074cfe9`

Require:

```text
22 / 22 exact
```

Any mismatch:

```text
ACCEPTED_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

Do not repair, re-edit or rerun implementation.

# 3. accepted evidence reuse

If all 22 hashes are exact, reuse:

```text
1648 B2 implementation:
predecessor candidate

1800 bounded rework:
ACCEPTED_CANDIDATE

1800 first B2 suite:
51 passed / 0 skipped

1800 shared regressions:
24 passed / 0 skipped

direct Docker unit module:
NO_EXISTING_DIRECT_DOCKER_UNIT_MODULE
```

No test rerun is required under exact byte identity.

# 4. current issued provenance identity

Verify:

```text
.aiassistant/records/aiscc/cycles/20260909_1805_aiscc-p2-3-phase1b-b2-accepted-persistence-entry-1.cycle.md
SHA-256:
03ee3f7d790a77a55f1a3354963c6a6e9458a183f5bac0aebba6084a3e52cfab

.aiassistant/reports/aiscc/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-judgment-1.md
SHA-256:
7de14abcfcfba33c5cd13a18ded9214f9b9c270e405ca106037e71861409e5c4
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
24 exact excluding active Task

other product/config/test delta:
0

Git-visible pyc/__pycache__/pytest cache:
none
```

# 6. Task lifecycle

Move:

```text
.aiassistant/tasks/active/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-git-persistence-1.md
→
.aiassistant/tasks/done/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-git-persistence-1.md
```

Do not edit bytes.

Then require:

```text
25 exact Git-visible commit candidates
```

# 7. exact final commit allowlist — 25

- `.aiassistant/tasks/done/20260909_1648_aiscc-p2-3-phase1b-b2-scenario-tool-provider-security-enrollment-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1648_aiscc-p2-3-b1-state-reconciliation-accepted-b2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1648_aiscc-p2-3-b1-state-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-contract-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1800_aiscc-p2-3-phase1b-b2-test-failure-contract-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1800_aiscc-p2-3-phase1b-b2-first-suite-test-failure-judgment-1.md`
- `src/aiscc/scenarios/enrollment.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/security/stockroom_policy.py`
- `config/providers/stockroom-owner-profiles.v1.toml`
- `config/providers/stockroom-tools.v1.toml`
- `config/security/stockroom-owner.v1.toml`
- `tests/unit/scenarios/test_runtime_enrollment.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/security/test_stockroom_policy.py`
- `src/aiscc/providers/ports.py`
- `src/aiscc/providers/tools.py`
- `src/aiscc/providers/service.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/security/policy.py`
- `.aiassistant/records/aiscc/cycles/20260909_1805_aiscc-p2-3-phase1b-b2-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-git-persistence-1.md`

No other path may be staged.

# 8. Git persistence

Only after all prior gates PASS:

```text
git add -- <25 exact literal paths>
git diff --cached --check
git diff --cached --name-status
```

Require:

```text
staged:
25 exact

extra:
0

missing:
0

unstaged tracked:
0
```

Then:

```text
git commit -m "feat(runtime): persist P2-3 Phase 1B-B2 enrollment"
```

Expected:

```text
parent:
0f5f19c8f8109e192275d1123f90ae50120be203

parent count:
1

message:
feat(runtime): persist P2-3 Phase 1B-B2 enrollment

changed paths:
25 exact
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

1. result commit hash/tree;
2. exact parent `0f5f19c8f8109e192275d1123f90ae50120be203`;
3. parent count 1;
4. exact commit message;
5. changed paths 25 exact;
6. accepted predecessor 22 committed bytes equal expected hashes;
7. current Cycle/Judgment/Task committed bytes equal issued bytes;
8. all 16 B2 product/config/test paths present at accepted hashes;
9. index empty;
10. Git-visible worktree clean;
11. no generated cache residue;
12. push/network NOT_RUN.

# 10. semantic identity after commit

Without modifying or executing runtime scenarios, verify committed B2 still contains:

```text
canonical ScenarioCatalog enrollment
four exact Stockroom scenario selections
aiscc-local-deterministic / external_llm_executed=false
fixed stockroom_summary empty-argument registry
receipt-aware one-use process crossing
UnknownToolOutcome for unresolved receipt/outcome
full finite Stockroom security intersection
NETWORK denied
three strict owner-only TOML configs
```

Do not run B3, real provider/tool/Docker, DB, scenario or Replay.

# 11. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-git-persistence-1/
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

Include byte-preserving committed copies of all 25 commit paths.

After folder completion create:

```text
.aiassistant/reports/target/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-git-persistence-1.zip
```

Require:

```text
one top-level bundle directory
readable / CRC PASS
required root files present
25 committed project-relative copies present
manifest coverage
source/commit/export byte equality
folder/archive byte equality
```

Keep both folder and outbound ZIP.

# 12. inbound cleanup

After terminal outcome/outbound ZIP validation, attempt exact inbound delivery ZIP cleanup best-effort.

Failure:

```text
NON_BLOCKING_LOCAL_RESIDUE
```

No alternate deletion fallback or broad Downloads cleanup.

# 13. evidence contract

executor_required:

- inbound ZIP/artifact transport
- exact 24-path workspace gate
- 22-path accepted candidate identity
- exact 25-path staging/commit
- post-commit clean state
- committed semantic identity
- outbound result ZIP

reuse_allowed:

- 1800 accepted B2 candidate and passing unit/shared regressions under exact byte identity
- accepted 1329 Phase 1B design
- persisted B1

human_owned:

```text
new Human QA:
NOT_REQUIRED

public license:
HUMAN_PENDING / outside Task
```

forbidden:

- B2 product/config/test re-edit
- B3 implementation
- real provider/tool/Docker/scenario execution
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
P2-3 Phase 1B-B2:
PERSISTED / READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-3 Phase 1B-B3:
NOT_STARTED

actual scenario capture:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Do not declare Phase 1B or P2-3 closed.
