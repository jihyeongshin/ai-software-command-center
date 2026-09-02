# 작업지시서: Terminal Project Source mirror v2 activation persistence and closure

## meta

- task_id: `20260903_0330_aiscc-terminal-project-source-mirror-v2-activation-persistence-and-closure-1`
- created_at: `2026-09-03T03:30:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P1 terminal maintenance / P2 entry operational pre-step closure`
- work_type: `COMMAND_CENTER_RECORD_UPDATE / PROJECT_SOURCE_MIRROR_SYNC_PERSISTENCE`
- evidence_profile: `GOVERNANCE_HIGH`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_candidate_commit: `2b156d8b2a43d1b908bca6aaf740eba4061fd4a1`
- predecessor_terminal_canonical_commit: `b9ed57feb595b3a670b644a213c184f958956924`
- human_sync_cycle: `.aiassistant/records/aiscc/cycles/20260903_0328_aiscc-terminal-project-source-mirror-v2-human-sync-confirmation-1.cycle.md`
- predecessor_candidate_cycle: `.aiassistant/records/aiscc/cycles/20260903_0310_aiscc-terminal-project-source-mirror-v2-candidate-substantive-acceptance-human-replacement-gate-1.cycle.md`
- target_bundle: `.aiassistant/reports/target/20260903_0330_aiscc-terminal-project-source-mirror-v2-activation-persistence-and-closure-1/`
- fresh_chat_policy: `NO_NEW_CHAT_REQUIRED / SAME_SESSION_ALLOWED`
- success_boundary: `MIRROR_V2_ACTIVATION_PERSISTENCE_COMMIT_CREATED / COMMAND_CENTER_REVIEW_REQUIRED`

## 0. Human-provided authority

Human has completed Browser Project Source replacement and reported:

```text
Mirror Sync 완료
22개 업로드 완료
```

Command Center admits:

```text
AISCC-PROJECT-SOURCE-MIRROR-V2:
HUMAN_SYNC_CONFIRMED / 22

Browser active authority:
V2

V1:
RETIRED / HISTORICAL
```

Exact candidate:

```text
candidate commit:
2b156d8b2a43d1b908bca6aaf740eba4061fd4a1

bundle:
AISCC-PROJECT-SOURCE-MIRROR-V2

snapshot canonical commit:
b9ed57feb595b3a670b644a213c184f958956924
```

This Task persists that already-provided Human result. It does not re-run or simulate Browser upload.

## 1. exact goal

1. transport current Task, exact 0310 predecessor candidate-acceptance Cycle, and exact 0328 Human-sync Cycle;
2. verify repository baseline is exact candidate commit with clean index/runtime;
3. verify candidate registry/v2 manifest/current canonical state identities before mutation;
4. modify exactly four existing tracked governance files to record v2 Human activation;
5. perform current Task active→matching done lifecycle;
6. stage exactly seven governance/provenance paths;
7. create exactly one governance-only activation-persistence commit;
8. verify exact object/path/blob/tree contract;
9. export evidence and stop for Browser Command Center review.

## 2. non-goals / forbidden

Do not:

- regenerate v2 bundle;
- modify any generated Browser mirror file;
- upload/remove Browser Project Source;
- modify runtime/source/tests/migrations;
- modify `.aiassistant/rules/**`;
- modify P1→P2 handoff body;
- modify `NEXT_ACTIONS.md`;
- start P2/P2-1;
- push/network/deploy;
- amend/rebase/merge/revert;
- broad-stage or broad-clean.

Forbidden:

```text
git add .
git add -A
git restore .
git checkout .
git reset --hard
git clean
git stash
git commit --amend
git rebase
git merge
git revert
```

## 3. Downloads transport

Exactly three transport inputs are required.

Current Task:

```text
source:
C:\Users\oracl\Downloads\20260903_0330_aiscc-terminal-project-source-mirror-v2-activation-persistence-and-closure-1.md

destination:
.aiassistant/tasks/active/20260903_0330_aiscc-terminal-project-source-mirror-v2-activation-persistence-and-closure-1.md
```

Human-sync Cycle:

```text
source:
C:\Users\oracl\Downloads\20260903_0328_aiscc-terminal-project-source-mirror-v2-human-sync-confirmation-1.cycle.md

destination:
.aiassistant/records/aiscc/cycles/20260903_0328_aiscc-terminal-project-source-mirror-v2-human-sync-confirmation-1.cycle.md

expected SHA-256:
1d7a1d1780d1a02c2d53c2513accdca8677ab31be5a650b253c29b6ebfee31ab
```

Predecessor candidate-acceptance Cycle:

```text
source:
C:\Users\oracl\Downloads\20260903_0310_aiscc-terminal-project-source-mirror-v2-candidate-substantive-acceptance-human-replacement-gate-1.cycle.md

destination:
.aiassistant/records/aiscc/cycles/20260903_0310_aiscc-terminal-project-source-mirror-v2-candidate-substantive-acceptance-human-replacement-gate-1.cycle.md

expected SHA-256:
32a877571c0b205e2f0ef658179b28527aa2c80fb19dbecb21e1bbcd0edc7799
```

### 3.1 precheck

Require:

- current Task source exists and active destination absent;
- Human-sync Cycle source exists and destination absent;
- Human-sync Cycle SHA exact;
- 0310 Cycle:
  - if canonical destination absent, exact Downloads source must exist and SHA match;
  - if canonical destination already exists, its SHA must match exactly and no second transport is performed;
  - mismatch is STOP.

Do not search alternate Downloads paths.

If a required absent-destination transport precondition fails, do not partially move the current Task or 0328 Cycle.

### 3.2 execution

After full precheck:

- Move current Task to active;
- Move 0328 Cycle to canonical cycles;
- Move 0310 Cycle only when destination was absent;
- verify byte identity and moved-source absence.

## 4. repository baseline

Before content mutation require:

```text
repository == ai-software-command-center
branch == main
HEAD == 2b156d8b2a43d1b908bca6aaf740eba4061fd4a1
index == empty
runtime/source/test/migration dirt == 0
```

Existing expected governance dirt before current transport:

```text
0310 Cycle:
absent or exact already-canonical only
```

After transport, Git-visible dirt must be only exact transported Cycle paths not already committed.

Do not auto-expand unexpected dirt.

## 5. minimum authoritative context

Read exact:

```text
.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v2.json

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260903_0310_aiscc-terminal-project-source-mirror-v2-candidate-substantive-acceptance-human-replacement-gate-1.cycle.md
.aiassistant/records/aiscc/cycles/20260903_0328_aiscc-terminal-project-source-mirror-v2-human-sync-confirmation-1.cycle.md
.aiassistant/tasks/active/20260903_0330_aiscc-terminal-project-source-mirror-v2-activation-persistence-and-closure-1.md
```

Do not bulk-read unrelated history/source.

## 6. exact mutation scope

Modify exactly:

```text
1. .aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
2. .aiassistant/project-sources/manifests/aiscc-project-source-mirror-v2.json
3. .aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
4. .aiassistant/records/aiscc/DECISION_REGISTER.md
```

Do not modify any fifth existing file.

## 7. registry semantic contract

Preserve history.

Required current facts:

```text
AISCC-PROJECT-SOURCE-MIRROR-V1:
RETIRED / HISTORICAL / previous active count 18

AISCC-PROJECT-SOURCE-MIRROR-V2:
ACTIVE / HUMAN_SYNC_CONFIRMED / 22

v2 Browser sync:
HUMAN_PROVIDED / CONFIRMED

v2 candidate commit:
2b156d8b2a43d1b908bca6aaf740eba4061fd4a1

v2 snapshot canonical commit:
b9ed57feb595b3a670b644a213c184f958956924

current Browser authority:
AISCC-PROJECT-SOURCE-MIRROR-V2

active Browser source count:
22
```

Do not claim exact subscription plan ceiling.

## 8. v2 manifest semantic contract

Modify only mirror-sync status metadata; do not change the accepted 22 mapping rows, canonical paths, hashes,
bundle ID, target project, canonical commit, generated task or generated timestamp.

Required:

```text
bundle_id:
AISCC-PROJECT-SOURCE-MIRROR-V2

canonical_commit:
b9ed57feb595b3a670b644a213c184f958956924

expected_active_count:
22

source_mirror_sync_status:
HUMAN_PROVIDED_CONFIRMED
```

All 22 mapping rows must remain byte-semantically identical in values and order.

Do not regenerate Browser files merely because this tracked manifest status changes after Human upload.

## 9. CURRENT_STATE_SUMMARY semantic contract

Preserve terminal P1/P2 state.

Update only source-mirror current authority/provenance statements so current facts are unambiguous:

```text
current Browser mirror:
AISCC-PROJECT-SOURCE-MIRROR-V2

active mirror file count:
22

mirror snapshot canonical commit:
b9ed57feb595b3a670b644a213c184f958956924

mirror candidate/persistence commit:
2b156d8b2a43d1b908bca6aaf740eba4061fd4a1

source_mirror_sync:
HUMAN_PROVIDED / CONFIRMED

v1:
RETIRED / HISTORICAL
```

Keep:

```text
P1 = ACCEPTED / CLOSED
P2 = NOT_STARTED / ENTRY_READY
next executable = P2-1 Command Center Web UI
PUBLIC_BOUNDED_LIVE = NOT_RELEASED
```

Do not rewrite unrelated historical sections for style.

## 10. DECISION_REGISTER semantic contract

Preserve existing decisions.

Update current mirror-authority entry so it no longer says v1 is active.

Add exactly one durable decision section:

```text
## AISCC-PROJECT-SOURCE-MIRROR-V2-ACTIVATION
```

Required facts:

```text
decision:
AI Software Command Center Browser Project active source is AISCC-PROJECT-SOURCE-MIRROR-V2 22/22 complete replacement.

decision_status:
HUMAN_PROVIDED / ACCEPTED / CLOSED

candidate commit:
2b156d8b2a43d1b908bca6aaf740eba4061fd4a1

snapshot canonical commit:
b9ed57feb595b3a670b644a213c184f958956924

Human result:
Mirror Sync 완료 / 22개 업로드 완료

v1:
RETIRED / HISTORICAL

authority:
repository canonical remains editable owner; Browser Project Source is read-only mirror v2.

P2:
NOT_STARTED / ENTRY_READY
```

Do not alter unrelated decision semantics.

## 11. validation before lifecycle

Require:

- exact four content mutation paths only;
- `NEXT_ACTIONS.md` clean;
- P1→P2 handoff clean;
- v1 manifest and generator clean;
- Python generator clean;
- runtime/source/test/migrations clean;
- rules clean;
- generated v2 bundle ignored/unmodified;
- UTF-8/no-BOM;
- no prohibited controls;
- no secret material introduced;
- `git diff --check` PASS.

## 12. current Task lifecycle

After content validation:

```text
.aiassistant/tasks/active/20260903_0330_aiscc-terminal-project-source-mirror-v2-activation-persistence-and-closure-1.md
→
.aiassistant/tasks/done/20260903_0330_aiscc-terminal-project-source-mirror-v2-activation-persistence-and-closure-1.md
```

Move, not Copy.

Matching done destination must be absent.

## 13. exact staging set

Stage exactly:

```text
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v2.json
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/cycles/20260903_0328_aiscc-terminal-project-source-mirror-v2-human-sync-confirmation-1.cycle.md
.aiassistant/records/aiscc/cycles/20260903_0310_aiscc-terminal-project-source-mirror-v2-candidate-substantive-acceptance-human-replacement-gate-1.cycle.md
.aiassistant/tasks/done/20260903_0330_aiscc-terminal-project-source-mirror-v2-activation-persistence-and-closure-1.md
```

Expected changed/staged count:

```text
7
```

If the 0310 Cycle was already tracked in HEAD, then this exact baseline assumption is false: STOP before staging
and report `PREDECESSOR_CYCLE_ALREADY_TRACKED_BASELINE_RECONCILIATION_REQUIRED`; do not silently reduce count.

No broad staging.

## 14. activation persistence commit

Authorized message:

```text
docs(governance): activate Project Source mirror v2
```

Create exactly one commit.

Require:

```text
parent == 2b156d8b2a43d1b908bca6aaf740eba4061fd4a1
parent count == 1
merge parent count == 0
changed paths == exact seven
runtime/source/test/migration changed == 0
rules changed == 0
NEXT_ACTIONS changed == 0
P1-to-P2 handoff changed == 0
generated bundle committed == 0
```

No amend or second repair commit.

## 15. post-commit proof

Prove:

- branch `main`;
- HEAD is new activation-persistence candidate;
- parent exact candidate commit;
- index empty;
- Git-visible worktree clean;
- v2 registry/manifest/current-state/decision facts exact;
- P1 remains CLOSED;
- P2 remains NOT_STARTED / ENTRY_READY;
- generated 22-file Browser bundle not tracked/changed;
- no Browser action was simulated by Executor.

## 16. required export

Target:

```text
.aiassistant/reports/target/20260903_0330_aiscc-terminal-project-source-mirror-v2-activation-persistence-and-closure-1/
```

Required root:

```text
TASK.md
EXECUTOR_REPORT.md
GIT_OBJECT_EVIDENCE.md
MIRROR_ACTIVATION_EVIDENCE.md
EXPORT_MANIFEST.md
```

Export exact commit-tree copies of all seven changed paths.

`MIRROR_ACTIVATION_EVIDENCE.md` must state:

- Human-provided result;
- v2 active 22;
- v1 retired;
- snapshot canonical commit;
- candidate commit;
- registry/manifest/current-state/decision after values;
- P2 remains not started;
- exact project file ceiling remains unverified; capacity only proven sufficient for 22.

Manifest binds every payload except itself.

## 17. success / stop

Success candidate:

```text
MIRROR_V2_ACTIVATION_PERSISTENCE_COMMIT_CREATED
/ COMMAND_CENTER_REVIEW_REQUIRED
```

Do not declare:

```text
P2_STARTED
P2-1_STARTED
PUBLIC_RELEASED
```

After Browser Command Center accepts the persistence commit, Project Source refresh operational pre-step is closed
and the next executable Task is `P2-1 Command Center Web UI`.

## 18. preserved artifacts

Preserve:

- candidate commit `2b156d8b2a43d1b908bca6aaf740eba4061fd4a1`;
- `.aiassistant/records/aiscc/cycles/20260903_0310_aiscc-terminal-project-source-mirror-v2-candidate-substantive-acceptance-human-replacement-gate-1.cycle.md`;
- `.aiassistant/records/aiscc/cycles/20260903_0328_aiscc-terminal-project-source-mirror-v2-human-sync-confirmation-1.cycle.md`;
- `.aiassistant/tasks/done/20260903_0330_aiscc-terminal-project-source-mirror-v2-activation-persistence-and-closure-1.md`;
- v2 registry/manifest;
- updated canonical current state and decision register.

Target bundle is temporary through Browser substantive review.
