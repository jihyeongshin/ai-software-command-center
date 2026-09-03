# 작업지시서: P2-1B shell/queue Git persistence

## meta

- task_id: `20260903_1716_aiscc-p2-1b-shell-queue-git-persistence-1`
- created_at: `2026-09-03T17:16:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P2-1B — persistence checkpoint`
- work_type: `GIT_PERSISTENCE / P2_1B_CHECKPOINT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_head: `4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e`
- predecessor_task: `.aiassistant/tasks/done/20260903_1602_aiscc-p2-1b-responsive-queue-layout-and-human-qa-usability-rework-1.md`
- predecessor_source_runtime_cycle: `.aiassistant/records/aiscc/cycles/20260903_1604_aiscc-p2-1b-responsive-queue-rework-source-runtime-acceptance-pending-human-reqa-1.cycle.md`
- predecessor_human_acceptance_cycle: `.aiassistant/records/aiscc/cycles/20260903_1714_aiscc-p2-1b-responsive-queue-human-reqa-final-acceptance-1.cycle.md`
- accepted_product_aggregate_sha256: `fe68734a4b12b3e3038d8c38dbd93b40e26481c2d8541fd88e8d95717e9454fd`
- target_bundle: `.aiassistant/reports/target/20260903_1716_aiscc-p2-1b-shell-queue-git-persistence-1/`
- fresh_chat_policy: `REUSE_CURRENT_P2_1B_IMPLEMENTATION_CHAT_ALLOWED / GIT_PERSISTENCE_ONLY`
- success_boundary: `P2_1B_PERSISTENCE_COMMIT_CREATED / COMMAND_CENTER_REVIEW_REQUIRED`

## 0. authority

P2-1B source/runtime and focused Human re-QA are accepted.

Human result:

```text
R1-R8:
ALL PASS
```

This Task may persist only:

```text
exact five accepted P2-1B product/test bytes
+
exact accumulated P2-1B governance provenance
```

No product/test content mutation is authorized.

## 1. Downloads transport

Transport exactly three new files.

### current Task

```text
C:\Users\oracl\Downloads\20260903_1716_aiscc-p2-1b-shell-queue-git-persistence-1.md
→
.aiassistant/tasks/active/20260903_1716_aiscc-p2-1b-shell-queue-git-persistence-1.md
```

### 1604 source/runtime acceptance Cycle

```text
C:\Users\oracl\Downloads\20260903_1604_aiscc-p2-1b-responsive-queue-rework-source-runtime-acceptance-pending-human-reqa-1.cycle.md
→
.aiassistant/records/aiscc/cycles/20260903_1604_aiscc-p2-1b-responsive-queue-rework-source-runtime-acceptance-pending-human-reqa-1.cycle.md

expected SHA-256:
aea5f056f1fc0993a3f1c1ec40d50f9a87ad9b279bd2b2547e4352d3357a8837
```

### 1714 Human acceptance Cycle

```text
C:\Users\oracl\Downloads\20260903_1714_aiscc-p2-1b-responsive-queue-human-reqa-final-acceptance-1.cycle.md
→
.aiassistant/records/aiscc/cycles/20260903_1714_aiscc-p2-1b-responsive-queue-human-reqa-final-acceptance-1.cycle.md

expected SHA-256:
1d95f6344d19464982ceb78c1f2186f18651b635f113c88fe9bab0addcf199f5
```

Before moving any newly absent-destination file:

- exact Task source exists;
- current Task active destination absent;
- each Cycle:
  - if destination absent, exact Downloads source exists and SHA matches;
  - if destination exists, destination SHA must match exactly and no duplicate Move occurs.

Do not search alternate Downloads paths.

Any conflict:

```text
TRANSPORT_PRECONDITION_FAILED
```

Move, not Copy.

## 2. session authority

Reuse current P2-1B implementation/rework chat.

Allowed lineage:

```text
1325 implementation
→ 1329 Korean-first rework
→ 1602 responsive/Human-QA rework
→ 1716 persistence
```

This Task is persistence-only.

No source redesign or further UI density optimization is authorized.

## 3. repository preflight

Require:

```text
repository == ai-software-command-center
branch == main
HEAD == 4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e
index == empty
```

Product/test dirt MUST be exactly the five accepted paths in Section 4.

Before 1604/1714 transport, expected Git-visible accumulated P2-1B governance/provenance dirt is exactly eight paths:

```text
.aiassistant/records/aiscc/cycles/20260903_1323_aiscc-p2-1a-read-api-foundation-persistence-final-acceptance-1.cycle.md
.aiassistant/tasks/done/20260903_1325_aiscc-p2-1b-command-center-shell-and-project-task-queue-implementation-1.md
.aiassistant/records/aiscc/cycles/20260903_1327_aiscc-p2-1b-shell-queue-partial-acceptance-korean-first-ui-copy-rework-1.cycle.md
.aiassistant/tasks/done/20260903_1329_aiscc-p2-1b-korean-first-visible-copy-and-document-language-rework-1.md
.aiassistant/records/aiscc/cycles/20260903_1431_aiscc-p2-1b-shell-queue-rework-acceptance-pending-human-browser-qa-1.cycle.md
.aiassistant/records/aiscc/cycles/20260903_1436_aiscc-p2-1b-human-browser-qa-gate-execution-guidance-correction-1.cycle.md
.aiassistant/records/aiscc/cycles/20260903_1600_aiscc-p2-1b-human-browser-qa-rework-responsive-queue-and-visual-hierarchy-1.cycle.md
.aiassistant/tasks/done/20260903_1602_aiscc-p2-1b-responsive-queue-layout-and-human-qa-usability-rework-1.md
```

After 1604 and 1714 Cycle transport:

```text
governance/provenance dirt:
10
```

No unrelated path is allowed.

Do not clean, restore, or absorb it.

## 4. exact accepted five product/test identities

- `src/aiscc/api/app.py` — `34b9216342dc256fd319ab5c594799b9aa6784c35bc13a8b01595d4204d572f0`
- `src/aiscc/api/routes/command_center_ui.py` — `05ac1ba9ce029d9b45b8aa93ee805976b97cc8b4e338af3747c14577e08122e2`
- `src/aiscc/command_center/web.py` — `06a281504a3e880dca9d96dfb92fcf8b209f39d4a62a306155e8139cae201b8e`
- `tests/integration/command_center/test_web_ui.py` — `9eaaf6e5018b811a1a536ec2448baad234d9753944ee6efad4080f33f5499134`
- `tests/unit/command_center/test_web_shell.py` — `bfbbdd0f71efdccb28bb0a5dd033d9f88d7f2cd19bbfebcce88011def265a410`

Require:

```text
path count == 5
per-path SHA-256 == exact above
aggregate == fe68734a4b12b3e3038d8c38dbd93b40e26481c2d8541fd88e8d95717e9454fd
```

No byte change.

## 5. validation before lifecycle/staging

Run:

```text
git diff --check
```

Do not rerun product tests merely for persistence while exact accepted bytes are unchanged.

1602 source/runtime and Human R1-R8 evidence may be reused.

If any source/test hash differs:

```text
ACCEPTED_SOURCE_IDENTITY_MISMATCH
```

STOP without restore.

## 6. current Task lifecycle

After preflight:

```text
.aiassistant/tasks/active/20260903_1716_aiscc-p2-1b-shell-queue-git-persistence-1.md
→
.aiassistant/tasks/done/20260903_1716_aiscc-p2-1b-shell-queue-git-persistence-1.md
```

Move, not Copy.

Verify Task bytes unchanged.

After lifecycle exact Git-visible set MUST be:

```text
5 accepted product/test
+ 10 predecessor/acceptance governance paths
+ current 1716 Task done
= 16 paths
```

No seventeenth path.

## 7. exact staging

Stage exactly the 16 paths with explicit pathspecs.

Do not use:

```text
git add .
git add -A
```

Require:

```text
staged count == 16
unstaged Git-visible dirt == 0

product/test:
5

governance/provenance:
11

rules:
0

config:
0

migrations:
0

Project Source:
0

P2-1A product files outside the exact accepted P2-1B five:
0
```

For each accepted product/test path, staged content SHA-256 must equal Section 4.

## 8. persistence commit

Authorized message:

```text
feat(command-center): complete P2-1B shell and project queue
```

Create exactly one non-merge commit.

Require:

```text
parent:
4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e

parent count:
1

merge parent count:
0

changed path count:
16

changed path set:
exact Section 6 set
```

Do not amend/rebase/merge/revert or create a second repair commit.

If Git author identity is unavailable:

```text
STOP
```

Do not change Git config.

## 9. post-commit proof

Prove:

- branch `main`;
- HEAD = single new persistence commit;
- parent exact;
- message exact;
- path count exact 16;
- product/test five commit-tree SHA-256 exact;
- aggregate `fe68734a4b12b3e3038d8c38dbd93b40e26481c2d8541fd88e8d95717e9454fd`;
- governance path set exact;
- index empty;
- Git-visible worktree clean;
- no Project Source bundle/manifest change;
- no tests/network/deploy/push rerun unnecessarily.

Do not declare P2-1C started.

## 10. export

Target:

```text
.aiassistant/reports/target/20260903_1716_aiscc-p2-1b-shell-queue-git-persistence-1/
```

Required root:

```text
TASK.md
EXECUTOR_REPORT.md
GIT_OBJECT_EVIDENCE.md
ACCEPTED_SOURCE_IDENTITY.md
EXPORT_MANIFEST.md
```

Export exact commit-tree copies of all 16 changed paths preserving repository-relative paths.

`ACCEPTED_SOURCE_IDENTITY.md` must list:

```text
five product/test path SHA-256
aggregate
Human R1-R8 acceptance reference
```

Manifest binds every payload except itself.

## 11. evidence contract

### executor_required

- Downloads transport;
- baseline/index/dirty inventory;
- exact five source identities;
- exact governance identities;
- exact explicit staging;
- commit object/tree/path proof;
- post-commit clean state;
- export manifest.

### reuse_allowed

- 1602 source/runtime regression evidence;
- Human R1-R8 re-QA acceptance;
- only while the exact five accepted bytes remain identical.

### human_owned

No further Human verification before persistence.

### forbidden

- source/test mutation;
- 3-column-at-1080 density experiment;
- product path expansion;
- canonical state rewrite;
- Project Source refresh;
- broad staging/cleanup;
- P2-1C implementation;
- network/push/deploy.

## 12. success

Successful candidate:

```text
P2_1B_PERSISTENCE_COMMIT_CREATED
/ COMMAND_CENTER_REVIEW_REQUIRED
```

Do not declare:

```text
P2-1C STARTED
P2-1 ACCEPTED
P2-1 CLOSED
P2-2 STARTED
```

## 13. preserved artifacts

Preserve:

- new P2-1B persistence commit candidate;
- `.aiassistant/records/aiscc/cycles/20260903_1604_aiscc-p2-1b-responsive-queue-rework-source-runtime-acceptance-pending-human-reqa-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260903_1714_aiscc-p2-1b-responsive-queue-human-reqa-final-acceptance-1.cycle.md`
- `.aiassistant/tasks/done/20260903_1716_aiscc-p2-1b-shell-queue-git-persistence-1.md`
- exact accumulated P2-1B governance lineage.

Target bundle remains temporary through Browser persistence review.
