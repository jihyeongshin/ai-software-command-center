# 작업지시서: P2-3 Phase 1B-B1 final acceptance Git persistence

## meta

- task_id: `20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-git-persistence-1`
- created_at: `2026-09-09T14:35:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / GIT_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `472bd11b76dc510562e33d056d9841b6be72c12e`
- required_base_tree: `14195b914b16d5adce7db0c4093907d2af7dcac0`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `bounded B1 implementation/rework → exact Git persistence authority`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-git-persistence-1.md

CYCLE:
20260909_1435_aiscc-p2-3-phase1b-b1-accepted-persistence-entry-1.cycle.md
SHA-256:
72036bfeb4a76e172efd11d2ee6db26db387736b29b9adcdc02900eb3f26b9b1
destination:
.aiassistant/records/aiscc/cycles/20260909_1435_aiscc-p2-3-phase1b-b1-accepted-persistence-entry-1.cycle.md

JUDGMENT:
20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-judgment-1.md
SHA-256:
31d10da0bdd0e68fa07f1e4c9a1cb65d9dfd8be564e72a97048443d80d9f9862
destination:
.aiassistant/reports/aiscc/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-git-persistence-1.md
```

Read it, then place/verify CYCLE/JUDGMENT.

Bootstrap failures follow the persisted ZIP-direct workflow.

After canonical transport, inbound cleanup refusal is non-blocking.

# 1. repository gate

After current artifact placement require:

```text
branch:
main

HEAD:
472bd11b76dc510562e33d056d9841b6be72c12e

HEAD tree:
14195b914b16d5adce7db0c4093907d2af7dcac0

index:
empty
```

Expected Git-visible set excluding current active Task:

```text
16 exact paths
```

- `.aiassistant/tasks/done/20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1300_aiscc-p2-3-phase1a-terminal-accepted-phase1b-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1300_aiscc-p2-3-phase1a-terminal-state-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1329_aiscc-p2-3-phase1b-audit-accepted-b1-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1329_aiscc-p2-3-phase1b-runtime-integration-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_1330_aiscc-p2-3-phase1b-b1-trusted-git-executable-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-judgment-1.md`
- `src/aiscc/runtime/stockroom_workspace.py`
- `src/aiscc/runtime/stockroom_materializer.py`
- `src/aiscc/scenarios/runtime_models.py`
- `tests/unit/runtime/test_stockroom_materializer.py`
- `tests/unit/runtime/test_stockroom_workspace.py`
- `.aiassistant/records/aiscc/cycles/20260909_1435_aiscc-p2-3-phase1b-b1-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup, restore, stash, reset or absorb.

# 2. accepted candidate byte identity — exact 14

Verify every accepted predecessor path before staging:

- `.aiassistant/tasks/done/20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1.md`  `61fe8fea516e79fb5c66150433bbd79d2abaf70b845f8ca72736597fac3f9f26`
- `.aiassistant/records/aiscc/cycles/20260909_1300_aiscc-p2-3-phase1a-terminal-accepted-phase1b-audit-entry-1.cycle.md`  `998d726c95165db059b697e4ce04184bead4fe50c4fa4a88c14cd5f376444c36`
- `.aiassistant/reports/aiscc/20260909_1300_aiscc-p2-3-phase1a-terminal-state-final-acceptance-judgment-1.md`  `595d283e12ee27ed7cff9484c4305ccbb8760b40b34bc25374e9800618a6ed21`
- `.aiassistant/tasks/done/20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1.md`  `68a9aa6630af1729b8c4a8aad0ff988df28e0d314bf8495b48854ca1b86d2fc3`
- `.aiassistant/records/aiscc/cycles/20260909_1329_aiscc-p2-3-phase1b-audit-accepted-b1-entry-1.cycle.md`  `e1431a3630a83a391485148117566ee63b827ba41a40745b36c11fd3974ae404`
- `.aiassistant/reports/aiscc/20260909_1329_aiscc-p2-3-phase1b-runtime-integration-audit-final-acceptance-judgment-1.md`  `fc062f0a09ff170f75c204c9bde43c0c0d061f2ed1204583bc7047e88b934169`
- `.aiassistant/tasks/done/20260909_1330_aiscc-p2-3-phase1b-b1-trusted-git-executable-rework-1.md`  `c6d0213b1a637e64349ab0cd281947f97b2fe46333f7e4cf5ddf53e08ad0ab09`
- `.aiassistant/records/aiscc/cycles/20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-rework-entry-1.cycle.md`  `74e93bfe9d38205a6e42ee60671d8d10d0540f2d7ca9535ef24e860de0cc55cf`
- `.aiassistant/reports/aiscc/20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-judgment-1.md`  `864d316a9a34adda32a99afd3f9cf6c3d22c71dcb1d8818cbcd3555e6b3335ed`
- `src/aiscc/runtime/stockroom_workspace.py`  `fd6c889e518b9fec7bef425ec4ea950b430c38c86f039a62a275949416442347`
- `src/aiscc/runtime/stockroom_materializer.py`  `e23f9f5bfd4e5836b79cab015273461d7eae40b5d42fdabe9b6d2bafc9c008d0`
- `src/aiscc/scenarios/runtime_models.py`  `2d2264ad0fcc2417febc17d8951ff66e8f3931a074d114c3382d2238e9531cef`
- `tests/unit/runtime/test_stockroom_materializer.py`  `0457f76ce48e9c357b83ca9733b5c0851f9853d472bc4d8275a3063527d18b50`
- `tests/unit/runtime/test_stockroom_workspace.py`  `ce24c649664461440d4f354d0d311624e07bed840dba4f12df99fbc49dddd1ca`

Require:

```text
14 / 14 exact
```

Any mismatch:

```text
ACCEPTED_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

Do not repair/re-edit/rerun implementation.

# 3. accepted evidence reuse

If all 14 hashes are exact, reuse:

```text
1300 Phase 1B source/integration audit:
ACCEPTED_DESIGN

1329 B1 implementation:
predecessor candidate / failed trusted-git test state

1330 bounded B1 rework:
ACCEPTED_CANDIDATE

1330 B1 suite:
116 passed / 2 platform skips / exit 0
```

The two platform skips remain disclosed and are not promoted into proof.

No test rerun is required under exact byte identity.

# 4. current issued provenance identity

Verify:

```text
.aiassistant/records/aiscc/cycles/20260909_1435_aiscc-p2-3-phase1b-b1-accepted-persistence-entry-1.cycle.md
SHA-256:
72036bfeb4a76e172efd11d2ee6db26db387736b29b9adcdc02900eb3f26b9b1

.aiassistant/reports/aiscc/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-judgment-1.md
SHA-256:
31d10da0bdd0e68fa07f1e4c9a1cb65d9dfd8be564e72a97048443d80d9f9862
```

Current TASK integrity is anchored by verified ZIP and canonical byte equality.

# 5. pre-stage integrity

Require:

```text
git diff --check:
PASS

index:
empty

Git-visible:
16 exact excluding active Task

existing tracked-file modifications:
0

Git-visible pyc/__pycache__/pytest cache:
none
```

# 6. Task lifecycle

Move:

```text
.aiassistant/tasks/active/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-git-persistence-1.md
→
.aiassistant/tasks/done/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-git-persistence-1.md
```

Do not edit bytes.

Then require:

```text
17 exact Git-visible commit candidates
```

# 7. exact final commit allowlist — 17

- `.aiassistant/tasks/done/20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1300_aiscc-p2-3-phase1a-terminal-accepted-phase1b-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1300_aiscc-p2-3-phase1a-terminal-state-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1329_aiscc-p2-3-phase1b-audit-accepted-b1-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1329_aiscc-p2-3-phase1b-runtime-integration-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_1330_aiscc-p2-3-phase1b-b1-trusted-git-executable-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-judgment-1.md`
- `src/aiscc/runtime/stockroom_workspace.py`
- `src/aiscc/runtime/stockroom_materializer.py`
- `src/aiscc/scenarios/runtime_models.py`
- `tests/unit/runtime/test_stockroom_materializer.py`
- `tests/unit/runtime/test_stockroom_workspace.py`
- `.aiassistant/records/aiscc/cycles/20260909_1435_aiscc-p2-3-phase1b-b1-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-git-persistence-1.md`

No other path may be staged.

# 8. Git persistence

Only after all gates PASS:

```text
git add -- <17 exact literal paths>
git diff --cached --check
git diff --cached --name-status
```

Require:

```text
staged:
17 exact

extra:
0

missing:
0

unstaged tracked:
0
```

Then:

```text
git commit -m "feat(runtime): persist P2-3 Phase 1B-B1 materializer"
```

Expected:

```text
parent:
472bd11b76dc510562e33d056d9841b6be72c12e

parent count:
1

message:
feat(runtime): persist P2-3 Phase 1B-B1 materializer

changed paths:
17 exact
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

1. commit hash/tree;
2. exact parent `472bd11b76dc510562e33d056d9841b6be72c12e`;
3. parent count 1;
4. exact message;
5. changed paths 17 exact;
6. accepted predecessor 14 committed bytes equal expected hashes;
7. current Cycle/Judgment/Task committed bytes equal issued bytes;
8. five B1 product/test paths present at accepted hashes;
9. index empty;
10. Git-visible worktree clean;
11. no generated cache residue;
12. push/network NOT_RUN.

# 10. semantic identity after commit

Without modifying or executing runtime scenarios, verify committed B1 still contains:

```text
accepted resource_ref binding
local fixed Git-object materializer
isolated run/attempt workspace
trusted Git executable endpoint-only hardlink exception
mutable workspace/materialized hardlink denial
cleanup/quarantine disposition
five immutable B1 files
```

Do not run B2/B3/provider/tool/scenario/DB/Replay.

# 11. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-git-persistence-1/
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

Include byte-preserving committed copies of all 17 commit paths.

After folder completion create:

```text
.aiassistant/reports/target/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-git-persistence-1.zip
```

Require:

```text
one top-level bundle directory
readable / CRC PASS
required root files present
17 committed project-relative copies present
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
- exact 16-path workspace gate
- 14-path accepted candidate identity
- exact 17-path staging/commit
- post-commit clean state
- committed semantic identity
- outbound result ZIP

reuse_allowed:

- 1300 accepted audit
- 1330 accepted B1 candidate and passing B1 unit result under exact byte identity

human_owned:

```text
new Human QA:
NOT_REQUIRED

public license:
HUMAN_PENDING / outside Task
```

forbidden:

- product/test re-edit
- B2/B3 implementation
- scenario/provider/tool execution
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
P2-3 Phase 1B-B1:
PERSISTED / READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-3 Phase 1B-B2:
NOT_STARTED

P2-3 Phase 1B-B3:
NOT_STARTED

actual scenario capture:
NOT_STARTED

Replay:
NOT_STARTED
```

Do not declare Phase 1B or P2-3 closed.
