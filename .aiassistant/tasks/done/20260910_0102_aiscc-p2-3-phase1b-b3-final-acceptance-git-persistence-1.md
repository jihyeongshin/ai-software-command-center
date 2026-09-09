# 작업지시서: P2-3 Phase 1B-B3 final acceptance Git persistence

## meta

- task_id: `20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-git-persistence-1`
- created_at: `2026-09-10T01:02:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / GIT_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `40804edfa2dfce244965c59ec94a89c62bf83df5`
- required_base_tree: `1988fc71fc2dce05317eb62879b99c8a5f9dfb53`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `bounded B3 source rework/testing → exact Git persistence authority`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-git-persistence-1.md

CYCLE:
20260910_0102_aiscc-p2-3-phase1b-b3-accepted-persistence-entry-1.cycle.md
SHA-256:
a57cda2d8e296bf53db5aad3e2ba1db0b6f1b68877c0b0515e7651d7b6c4c313
destination:
.aiassistant/records/aiscc/cycles/20260910_0102_aiscc-p2-3-phase1b-b3-accepted-persistence-entry-1.cycle.md

JUDGMENT:
20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-judgment-1.md
SHA-256:
118ff53e3da4ce39d6ca78e3b17bb45b479c40f044474f6f1e5ea697e17957c6
destination:
.aiassistant/reports/aiscc/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-judgment-1.md

HANDOFF:
none
```

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-git-persistence-1.md
```

Read it, then place/hash-verify CYCLE/JUDGMENT.

Bootstrap failures follow the persisted ZIP-direct workflow.

After canonical transport, inbound cleanup refusal is non-blocking.

# 1. repository gate

After current artifact placement require:

```text
branch:
main

HEAD:
40804edfa2dfce244965c59ec94a89c62bf83df5

HEAD tree:
1988fc71fc2dce05317eb62879b99c8a5f9dfb53

index:
empty
```

Expected Git-visible set excluding current active Task:

```text
19 exact paths
```

- `.aiassistant/tasks/done/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_2136_aiscc-p2-3-b2-state-reconciliation-accepted-b3-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_2136_aiscc-p2-3-b2-state-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-candidate-adoption-qa-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_2330_aiscc-p2-3-phase1b-b3-dirty-candidate-adoption-qa-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-dirty-candidate-judgment-1.md`
- `.aiassistant/tasks/done/20260910_0020_aiscc-p2-3-phase1b-b3-candidate-fingerprint-zero-side-effect-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failed-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260910_0100_aiscc-p2-3-phase1b-b3-tool-fingerprint-json-subset-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0100_aiscc-p2-3-phase1b-b3-second-test-failure-tool-fingerprint-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0100_aiscc-p2-3-phase1b-b3-second-test-failure-judgment-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/driver.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `.aiassistant/records/aiscc/cycles/20260910_0102_aiscc-p2-3-phase1b-b3-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup, restore, stash, reset, overwrite or absorb.

# 2. accepted pending/candidate identity — exact 17

Verify every accepted path before staging:

- `.aiassistant/tasks/done/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.md`  `1d261d6a7546768f24e14d48678ae344a5d5aa9be77009cc6566dc8805f9af70`
- `.aiassistant/records/aiscc/cycles/20260909_2136_aiscc-p2-3-b2-state-reconciliation-accepted-b3-implementation-entry-1.cycle.md`  `c50a03a48ff75de627b6f94ea93c67886cbdda2815ccfe56d3a21746fb5e156d`
- `.aiassistant/reports/aiscc/20260909_2136_aiscc-p2-3-b2-state-reconciliation-final-acceptance-judgment-1.md`  `bf4375c2e0b7661abaa502a9b3d21fa2bdb38e2dab5cbd6f58f9881e63b22461`
- `.aiassistant/tasks/done/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-candidate-adoption-qa-1.md`  `7a4bcd03c69e309ec08d680c2f889564805ad501de0c943f68f98f9240814dac`
- `.aiassistant/records/aiscc/cycles/20260909_2330_aiscc-p2-3-phase1b-b3-dirty-candidate-adoption-qa-entry-1.cycle.md`  `570d8267404e5e23dd5512e377570a5b81bcca6e514385a3742cb9e2e560a8da`
- `.aiassistant/reports/aiscc/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-dirty-candidate-judgment-1.md`  `6c85c7c533ffebab14ce1f580cd29a915aa40bd0b52b57d725e29b9a0562c059`
- `.aiassistant/tasks/done/20260910_0020_aiscc-p2-3-phase1b-b3-candidate-fingerprint-zero-side-effect-rework-1.md`  `5a7b1eabc00e0ca2cf36b92d0708bded98e51c4acc63ce8923d1106b9b33e16b`
- `.aiassistant/records/aiscc/cycles/20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failed-rework-entry-1.cycle.md`  `459f70b2e13f87fca6ba0e6b9c8e30e1d96ad613fc5f72db896f5bd1227dbb91`
- `.aiassistant/reports/aiscc/20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failure-judgment-1.md`  `93b61e981d9190bceaa31b39b9687b4446b24d82d4663330e874e420901285f3`
- `.aiassistant/tasks/done/20260910_0100_aiscc-p2-3-phase1b-b3-tool-fingerprint-json-subset-rework-1.md`  `2c1757bb3369740d56360e213271b633ff686ee7c976c61094030f8e48e518fb`
- `.aiassistant/records/aiscc/cycles/20260910_0100_aiscc-p2-3-phase1b-b3-second-test-failure-tool-fingerprint-rework-entry-1.cycle.md`  `b931f3b7de6df604d986cb96c66fc09312a1f769bc5adb0108c38c8dbcdca2fe`
- `.aiassistant/reports/aiscc/20260910_0100_aiscc-p2-3-phase1b-b3-second-test-failure-judgment-1.md`  `4ed40a08fc831a65b145a7cd3cfaa6ff2873f428f6c608092c7eddee1c5237c7`
- `src/aiscc/bootstrap.py`  `f23912571b1510ff86d0ad45117ef974e8bb7a84329c8fb08757433cf44d616f`
- `src/aiscc/scenarios/composition.py`  `051f89bdceadeb1d08176e9ce0e2ed0ac3d9d14bddb6cd33657420853e50857c`
- `src/aiscc/scenarios/driver.py`  `7740b0a228d37e1034d1938141a903a9c883683b83e90451fa7b82f3381765c4`
- `tests/unit/scenarios/test_owner_composition.py`  `2ccf94c635ecd530d784531dda8d47120a226c12aaab5da5319d9249baa8b024`
- `tests/integration/scenarios/test_stockroom_binding.py`  `f1a4fb8b2239dc70982fe4d16701340c14f420c136ae87abee6def331cf9f7bb`

Require:

```text
17 / 17 exact
```

Any mismatch:

```text
ACCEPTED_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

Do not repair, re-edit or rerun implementation.

Candidate authorship remains:

```text
UNKNOWN
```

Do not rewrite provenance as Executor authorship.

# 3. accepted evidence reuse

If all 17 hashes are exact, reuse:

```text
0100 B3 candidate:
ACCEPTED_CANDIDATE

B3 mandatory tests:
18 passed / 0 skipped

B2 targeted regressions:
51 passed / 0 skipped

B3 source contract review:
10 / 10 PASS

zero-side-effect milestones:
7 / 7 reached

zero-side-effect counters:
40 / 40 zero

bootstrap direct regression discovery:
NO_EXISTING_DIRECT_BOOTSTRAP_UNIT_MODULE
```

No test rerun is required under exact byte identity.

# 4. current issued provenance identity

Verify:

```text
.aiassistant/records/aiscc/cycles/20260910_0102_aiscc-p2-3-phase1b-b3-accepted-persistence-entry-1.cycle.md
SHA-256:
a57cda2d8e296bf53db5aad3e2ba1db0b6f1b68877c0b0515e7651d7b6c4c313

.aiassistant/reports/aiscc/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-judgment-1.md
SHA-256:
118ff53e3da4ce39d6ca78e3b17bb45b479c40f044474f6f1e5ea697e17957c6
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
19 exact excluding active Task

other product/config/test delta:
0

Git-visible pyc/__pycache__/pytest cache:
none
```

# 6. Task lifecycle

Move:

```text
.aiassistant/tasks/active/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-git-persistence-1.md
→
.aiassistant/tasks/done/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-git-persistence-1.md
```

Do not edit bytes.

Then require:

```text
20 exact Git-visible commit candidates
```

# 7. exact final commit allowlist — 20

- `.aiassistant/tasks/done/20260909_2136_aiscc-p2-3-phase1b-b3-driver-composition-bootstrap-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_2136_aiscc-p2-3-b2-state-reconciliation-accepted-b3-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_2136_aiscc-p2-3-b2-state-reconciliation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-candidate-adoption-qa-1.md`
- `.aiassistant/records/aiscc/cycles/20260909_2330_aiscc-p2-3-phase1b-b3-dirty-candidate-adoption-qa-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260909_2330_aiscc-p2-3-phase1b-b3-preexisting-dirty-candidate-judgment-1.md`
- `.aiassistant/tasks/done/20260910_0020_aiscc-p2-3-phase1b-b3-candidate-fingerprint-zero-side-effect-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failed-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0020_aiscc-p2-3-phase1b-b3-adoption-qa-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260910_0100_aiscc-p2-3-phase1b-b3-tool-fingerprint-json-subset-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_0100_aiscc-p2-3-phase1b-b3-second-test-failure-tool-fingerprint-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0100_aiscc-p2-3-phase1b-b3-second-test-failure-judgment-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/driver.py`
- `tests/unit/scenarios/test_owner_composition.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `.aiassistant/records/aiscc/cycles/20260910_0102_aiscc-p2-3-phase1b-b3-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-git-persistence-1.md`

No other path may be staged.

# 8. Git persistence

Only after all prior gates PASS:

```text
git add -- <20 exact literal paths>
git diff --cached --check
git diff --cached --name-status
```

Require:

```text
staged:
20 exact

extra:
0

missing:
0

unstaged tracked:
0
```

Then:

```text
git commit -m "feat(runtime): persist P2-3 Phase 1B-B3 composition"
```

Expected:

```text
parent:
40804edfa2dfce244965c59ec94a89c62bf83df5

parent count:
1

message:
feat(runtime): persist P2-3 Phase 1B-B3 composition

changed paths:
20 exact
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
2. exact parent `40804edfa2dfce244965c59ec94a89c62bf83df5`;
3. parent count 1;
4. exact commit message;
5. changed paths 20 exact;
6. accepted predecessor/candidate 17 committed bytes equal expected hashes;
7. current Cycle/Judgment/Task committed bytes equal issued bytes;
8. all five B3 product/test paths present at accepted hashes;
9. candidate authorship remains recorded as UNKNOWN;
10. index empty;
11. Git-visible worktree clean;
12. no generated cache residue;
13. push/network NOT_RUN.

# 10. committed semantic identity

Without executing runtime scenarios, verify committed B3 still contains:

```text
inert Stockroom driver request
explicit real-owner dependency binding
strict server-owned owner composition
cross-config identity validation
strict canonical configuration fingerprints
explicit owner-only bootstrap preparation factory
unchanged default bootstrap semantics
PUBLIC_BOUNDED_LIVE not enrolled
zero automatic runtime execution path
no capture algorithm
```

Also verify the final tool fingerprint uses explicit strict-JSON payload with:

```text
argv:
list

provider total_timeout_seconds:
validated integral integer representation at canonical boundary
```

Do not execute B3 runtime, scenario, provider/tool/Docker, DB or Replay.

# 11. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-git-persistence-1/
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

Include byte-preserving committed copies of all 20 commit paths.

After folder completion create:

```text
.aiassistant/reports/target/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-git-persistence-1.zip
```

Require:

```text
one top-level bundle directory
readable / CRC PASS
required root files present
20 committed project-relative copies present
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
- exact 19-path workspace gate
- 17-path accepted identity
- exact 20-path staging/commit
- post-commit clean state
- committed B3 semantic identity
- outbound result ZIP

reuse_allowed:

- 0100 accepted B3 candidate and passing proof under exact byte identity
- persisted B1/B2
- prior B3 blocked/rework provenance

human_owned:

```text
new Human QA:
NOT_REQUIRED

candidate authorship:
UNKNOWN

public license:
HUMAN_PENDING / outside Task
```

forbidden:

- B3 source/test re-edit
- B1/B2/config/shared-owner mutation
- actual scenario/provider/tool/Docker execution
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

Inbound cleanup refusal after canonical transport remains non-blocking.

# 15. final ceiling

Success:

```text
P2-3 Phase 1B-B3:
PERSISTED / READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-3 Phase 1B:
NOT_CLOSED_YET

actual scenario capture:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Do not declare Phase 1B closed and do not start runtime/capture work.
