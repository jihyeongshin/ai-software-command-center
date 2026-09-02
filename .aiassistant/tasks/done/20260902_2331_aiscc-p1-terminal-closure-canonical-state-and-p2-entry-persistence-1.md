# 작업지시서: P1 terminal closure canonical state and P2 entry persistence

## meta

- task_id: `20260902_2331_aiscc-p1-terminal-closure-canonical-state-and-p2-entry-persistence-1`
- created_at: `2026-09-02T23:31:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P1 terminal closure`
- work_type: `GIT_TERMINAL_PERSISTENCE / CANONICAL_CLOSURE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_commit_a: `0f702cb95253a7ed13b46accabe9ac9e969da7a5`
- predecessor_commit_b: `c9004e89ae9ed961d7cabe6e3eca1100ef4a13cc`
- predecessor_commit_b_tree: `7ca0ab78781f7c5a8ae2fd1ec1a1707e7973e86f`
- predecessor_judgment_cycle: `.aiassistant/records/aiscc/cycles/20260902_2329_aiscc-p1-8-governance-commit-b-substantive-acceptance-and-terminal-closure-authority-1.cycle.md`
- target_bundle: `.aiassistant/reports/target/20260902_2331_aiscc-p1-terminal-closure-canonical-state-and-p2-entry-persistence-1/`
- fresh_chat_policy: `NO_NEW_CHAT_REQUIRED / SAME_FRESH_SESSION_ALLOWED`
- success_boundary: `TERMINAL_CLOSURE_PERSISTENCE_COMMIT_CREATED / COMMAND_CENTER_REVIEW_REQUIRED`

## 0. authority

Browser Command Center has substantively accepted:

```text
Runtime Commit A:
0f702cb95253a7ed13b46accabe9ac9e969da7a5

Governance Commit B:
c9004e89ae9ed961d7cabe6e3eca1100ef4a13cc
```

The exact 2329 Cycle authorizes P1 terminal closure state, subject to exact persistence.

This Task implements that already-authorized governance state. It does not create new product/runtime acceptance.

## 1. exact goal

1. transport the exact current Task and exact 2329 Cycle;
2. verify repository is exactly on accepted Commit B with empty index/worktree;
3. verify the exact pre-mutation identities of the three canonical files;
4. modify only those three canonical files according to the exact semantic contract in Section 8;
5. create exactly one phase handoff file according to Section 9;
6. perform current Task active→matching done lifecycle;
7. stage exactly six paths;
8. create exactly one governance-only terminal-closure persistence commit;
9. prove exact parent/message/path/blob/tree and no runtime/rule/config changes;
10. export evidence and stop for Browser review.

## 2. non-goals / forbidden

Do not:

- modify `src/**`, `tests/**`, `migrations/**`;
- modify `.aiassistant/rules/**`;
- modify repository config;
- modify any prior Task/Cycle/Handoff;
- create more than the one authorized phase handoff;
- start implementation of P2-1;
- mark P2 as started;
- generate or sync Project Source mirror;
- push/network/deploy/release;
- amend/rebase/merge/revert;
- use broad staging/cleanup.

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

Exactly two files:

```text
C:\Users\oracl\Downloads\20260902_2331_aiscc-p1-terminal-closure-canonical-state-and-p2-entry-persistence-1.md
C:\Users\oracl\Downloads\20260902_2329_aiscc-p1-8-governance-commit-b-substantive-acceptance-and-terminal-closure-authority-1.cycle.md
```

Destinations:

```text
.aiassistant/tasks/active/20260902_2331_aiscc-p1-terminal-closure-canonical-state-and-p2-entry-persistence-1.md
.aiassistant/records/aiscc/cycles/20260902_2329_aiscc-p1-8-governance-commit-b-substantive-acceptance-and-terminal-closure-authority-1.cycle.md
```

2329 Cycle expected SHA-256:

```text
a324d83de5dc011ff3e4361d19395b0c44f8935d88cc17b8ab225e7413f1e123
```

Before moving either:

1. both exact Downloads sources exist;
2. both exact destinations do not exist;
3. Cycle SHA-256 exact match.

Any failure:

```text
move neither
do not search alternate path
do not overwrite/delete
STOP: TRANSPORT_PRECONDITION_FAILED
```

All PASS:

- Move exactly both files, not Copy;
- verify destination byte identity and source absence.

## 4. session

Reuse current IDE Executor session.

No new chat is required.

If repository or session evidence shows out-of-Task mutation after accepted Commit B, do not repair/reset it.
Stop before content mutation and report exact drift.

## 5. minimum authoritative context

Read exact:

Core:

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`

Current authority:

- `.aiassistant/tasks/active/20260902_2331_aiscc-p1-terminal-closure-canonical-state-and-p2-entry-persistence-1.md`
- `.aiassistant/records/aiscc/cycles/20260902_2329_aiscc-p1-8-governance-commit-b-substantive-acceptance-and-terminal-closure-authority-1.cycle.md`

Accepted terminal lineage:

- `.aiassistant/records/aiscc/cycles/20260902_2159_aiscc-p1-8-runtime-commit-a-substantive-acceptance-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260902_2200_aiscc-p1-8-terminal-governance-audit-acceptance-and-commit-b-sequencing-freeze-1.cycle.md`
- `.aiassistant/tasks/done/20260902_2202_aiscc-p1-8-terminal-governance-provenance-checkpoint-commit-b-persistence-1.md`

Canonical mutation targets:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`

Do not bulk-read unrelated source/logs.

## 6. repository preflight

Before canonical content mutation require:

```text
repository == ai-software-command-center
branch == main
HEAD == c9004e89ae9ed961d7cabe6e3eca1100ef4a13cc
HEAD tree == 7ca0ab78781f7c5a8ae2fd1ec1a1707e7973e86f
HEAD parent == 0f702cb95253a7ed13b46accabe9ac9e969da7a5
index change count == 0
Git-visible worktree dirt before 2329 Cycle transport == 0
runtime/source/test/migration dirt == 0
```

After 2329 Cycle transport while current Task is active/ignored:

```text
Git-visible dirt == exact 1 path
.aiassistant/records/aiscc/cycles/20260902_2329_aiscc-p1-8-governance-commit-b-substantive-acceptance-and-terminal-closure-authority-1.cycle.md
```

No allowlist expansion.

## 7. exact pre-mutation canonical identity

Before content edit require:

```text
CURRENT_STATE_SUMMARY.md
bytes: 24957
SHA-256: b20d0928896123e12d4337ba93068a41497982d42cc24e000e3d0a4f998e1b09
Git blob: b934841568919544bc20b55843ac7efac5c5ce58

DECISION_REGISTER.md
bytes: 57228
SHA-256: f6fd9e32cd11dd720cfdd375f1f6eb3b9f3d2a1a10e864dbcdab853a4c10e302
Git blob: 9c7509269c211497949605fef44d57ff10bed471

NEXT_ACTIONS.md
bytes: 8814
SHA-256: 00b36388c22809b04ee5f3c4b699a0b8a551939621e533df8609b3a88863b6b9
Git blob: 7fc1593e4af997e645857c690fc731a8d185c0a3
```

Also require each path to be clean against Commit B before edit.

Any mismatch:

```text
CANONICAL_BASELINE_IDENTITY_MISMATCH
```

STOP before modifying content.

## 8. exact canonical semantic mutation contract

Modify no other existing file.

### 8.1 CURRENT_STATE_SUMMARY.md

Preserve historical sections. Make the current terminal status unambiguous.

Required current facts after edit:

```text
P1-8 Project Memory and Cycle Admission Runtime:
HUMAN_PROVIDED / ACCEPTED / CLOSED

Runtime Commit A:
0f702cb95253a7ed13b46accabe9ac9e969da7a5
ACCEPTED

Governance Commit B:
c9004e89ae9ed961d7cabe6e3eca1100ef4a13cc
ACCEPTED

RESTORE_SIX_TO_EXACT_HEAD:
COMPLETED

P1:
ACCEPTED / CLOSED

P2:
NOT_STARTED / ENTRY_READY

next executable:
P2-1 Command Center Web UI

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Replace the stale P1-8 runtime phase-table value rather than leaving contradictory current status elsewhere.

### 8.2 DECISION_REGISTER.md

Do not alter unrelated entries.

Append exactly one new durable decision section:

```text
## AISCC-P1-TERMINAL-CLOSURE-V1
```

Required fields/facts:

```text
decision:
P1-8 runtime and P1 are ACCEPTED / CLOSED; P2 remains NOT_STARTED / ENTRY_READY.

decision_status:
ACCEPTED_PROJECT_DECISION / TERMINAL

Human runtime acceptance:
Human P1-8 runtime final review — ACCEPTED

Runtime Commit A:
0f702cb95253a7ed13b46accabe9ac9e969da7a5 / ACCEPTED

Governance Commit B:
c9004e89ae9ed961d7cabe6e3eca1100ef4a13cc / ACCEPTED

closure authority Cycle:
.aiassistant/records/aiscc/cycles/20260902_2329_aiscc-p1-8-governance-commit-b-substantive-acceptance-and-terminal-closure-authority-1.cycle.md

next owner:
P2-1 Command Center Web UI

public release:
NOT_RELEASED
```

### 8.3 NEXT_ACTIONS.md

Preserve roadmap order.

Required current queue/status:

```text
P1-8 Runtime:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1:
ACCEPTED / CLOSED

P2:
NOT_STARTED / ENTRY_READY

next executable:
P2-1 Command Center Web UI
```

Remove or supersede stale `NOT_ACCEPTED / SEPARATE_REWORK_RESUME_AUTHORIZED` current-state language so it cannot
remain authoritative beside the new terminal state.

Keep:

```text
P2-2 Synthetic Demo Repository
P2-3 Canonical Scenario Pack and Recorded Replay Corpus
P2-4 Self-Dogfooding Cutover
P3-1 Comparative Evaluation
P3-2 Public Repository Documentation
P3-3 Public Release and Competition Submission
```

Do not mark any P2 item complete or started.

## 9. phase handoff creation

Create exactly:

```text
.aiassistant/reports/aiscc/20260902_2331_aiscc-p1-completion-p2-entry-handoff-1.md
```

Required title:

```text
AISCC P1 Completion → P2 Entry Handoff
```

Required content:

- project thesis in one concise paragraph;
- P1 completion statement;
- Human P1-8 runtime acceptance;
- accepted Runtime Commit A `0f702cb95253a7ed13b46accabe9ac9e969da7a5`;
- accepted governance Commit B `c9004e89ae9ed961d7cabe6e3eca1100ef4a13cc`;
- exact-six restoration complete;
- closure authority Cycle `20260902_2329_aiscc-p1-8-governance-commit-b-substantive-acceptance-and-terminal-closure-authority-1.cycle.md`;
- `P1-8 ACCEPTED / CLOSED`;
- `P1 ACCEPTED / CLOSED`;
- `P2 NOT_STARTED / ENTRY_READY`;
- first owner `P2-1 Command Center Web UI`;
- remaining P2/P3 roadmap;
- `PUBLIC_BOUNDED_LIVE: NOT_RELEASED`;
- Project Source mirror is stale relative to terminal canonical and requires a later explicit replacement/sync step;
- this file is a phase handoff and does not require Browser-session migration.

Do not include a guessed future closure-persistence commit hash.

## 10. validate edited bytes before lifecycle/staging

Required:

- all four content targets UTF-8 without BOM;
- Markdown readable;
- no prohibited control characters;
- no secret material introduced;
- `git diff --check` PASS for only the three canonical edits + one handoff;
- `git diff --name-only` content mutation set exact:
  - three canonical paths
  - one handoff path
- runtime/source/test/migration diff paths `0`;
- rules/config diff paths `0`.

If `git diff --check` fails because of bytes introduced in this Task, fix only within the four authorized content
targets and revalidate.

Do not edit predecessor provenance to fix historical whitespace.

## 11. current Task lifecycle

After content validation and before staging:

```text
.aiassistant/tasks/active/20260902_2331_aiscc-p1-terminal-closure-canonical-state-and-p2-entry-persistence-1.md
→
.aiassistant/tasks/done/20260902_2331_aiscc-p1-terminal-closure-canonical-state-and-p2-entry-persistence-1.md
```

Requirements:

- active exists;
- matching done absent;
- Move not Copy;
- bytes unchanged.

After lifecycle expected Git-visible changed/untracked set is exactly six paths:

```text
1. .aiassistant/records/aiscc/cycles/20260902_2329_aiscc-p1-8-governance-commit-b-substantive-acceptance-and-terminal-closure-authority-1.cycle.md
2. .aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
3. .aiassistant/records/aiscc/DECISION_REGISTER.md
4. .aiassistant/records/aiscc/NEXT_ACTIONS.md
5. .aiassistant/reports/aiscc/20260902_2331_aiscc-p1-completion-p2-entry-handoff-1.md
6. .aiassistant/tasks/done/20260902_2331_aiscc-p1-terminal-closure-canonical-state-and-p2-entry-persistence-1.md
```

No seventh path permitted.

## 12. staging

Stage exactly the six paths above with explicit pathspecs.

Do not broad-stage.

Require:

```text
staged path count == 6
staged set == exact six
unstaged Git-visible dirt == 0
runtime staged == 0
rules/config staged == 0
target/mirror staged == 0
```

## 13. terminal closure persistence commit

Authorized message:

```text
docs(governance): close P1 and persist P2 entry state
```

Create exactly one commit.

Required:

```text
parent == c9004e89ae9ed961d7cabe6e3eca1100ef4a13cc
parent count == 1
merge parent count == 0
changed path count == 6
changed path set == exact Section 11 six
runtime/source/test/migration changed == 0
rules/config changed == 0
```

No amend or repair second commit.

If Git author identity is unavailable, stop without changing Git config.

## 14. post-commit proof

Prove:

- branch `main`;
- HEAD is new terminal-closure persistence commit candidate;
- parent exact accepted Commit B;
- accepted Commit A and B objects unchanged;
- exact six changed paths;
- exact per-path commit-tree blob and SHA-256;
- index empty;
- Git-visible worktree dirt `0`;
- runtime dirt `0`;
- rules/config dirt `0`;
- no mirror/target path committed.

Executor must not claim its own commit accepted.

## 15. required export

Target:

```text
.aiassistant/reports/target/20260902_2331_aiscc-p1-terminal-closure-canonical-state-and-p2-entry-persistence-1/
```

Required root Markdown:

```text
TASK.md
EXECUTOR_REPORT.md
GIT_OBJECT_EVIDENCE.md
CANONICAL_STATE_EVIDENCE.md
EXPORT_MANIFEST.md
```

Export exact commit-tree copies preserving repository-relative paths for all six changed paths.

`CANONICAL_STATE_EVIDENCE.md` must show:

- before/after SHA-256 for canonical three;
- exact required current facts found after edit;
- handoff path/hash;
- no contradictory current P1-8 runtime status remains in canonical current-status sections;
- P2 remains not started.

Manifest binds every payload except itself.

## 16. evidence contract

### executor_required

- transport;
- accepted Commit B preflight;
- canonical baseline identities;
- exact scoped canonical edits;
- exact phase handoff creation;
- diff/UTF-8 validation;
- Task lifecycle;
- exact six staging;
- commit object/tree/path/blob proof;
- exact six commit-tree export.

### reuse_allowed

- Human exact runtime acceptance;
- accepted Runtime Commit A;
- accepted governance Commit B;
- 2329 closure authority Cycle.

### human_owned

- no new Human gate before execution;
- later Project Source replacement confirmation if performed;
- release/deployment decisions.

### forbidden

- runtime/rule/config mutation;
- P2 implementation;
- mirror sync;
- network/push/deployment;
- broad staging/cleanup.

## 17. success / stop

Success candidate:

```text
TERMINAL_CLOSURE_PERSISTENCE_COMMIT_CREATED
/ COMMAND_CENTER_REVIEW_REQUIRED
```

Do not declare:

```text
P2_STARTED
PUBLIC_RELEASED
SOURCE_MIRROR_SYNCED
```

The authoritative closure decision comes from the 2329 Cycle; this Task only persists it.

Any path/identity/scope mismatch before commit is mandatory STOP without auto-expansion.

Any post-commit discrepancy is reported without repair second commit.

## 18. preserved artifacts

Preserve:

- accepted Commit A `0f702cb95253a7ed13b46accabe9ac9e969da7a5`;
- accepted Commit B `c9004e89ae9ed961d7cabe6e3eca1100ef4a13cc`;
- `.aiassistant/records/aiscc/cycles/20260902_2329_aiscc-p1-8-governance-commit-b-substantive-acceptance-and-terminal-closure-authority-1.cycle.md`;
- `.aiassistant/tasks/done/20260902_2331_aiscc-p1-terminal-closure-canonical-state-and-p2-entry-persistence-1.md`;
- `.aiassistant/reports/aiscc/20260902_2331_aiscc-p1-completion-p2-entry-handoff-1.md`;
- the three canonical state files after exact authorized mutation.

Target bundle remains temporary through Browser substantive review.
