# 작업지시서: P1-8 terminal governance provenance checkpoint Commit B persistence

## meta

- task_id: `20260902_2202_aiscc-p1-8-terminal-governance-provenance-checkpoint-commit-b-persistence-1`
- created_at: `2026-09-02T22:02:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P1-8 — terminal governance persistence`
- work_type: `GIT_TERMINAL_PERSISTENCE / GOVERNANCE_ONLY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `accepted P1-8 governance/provenance persistence checkpoint`
- predecessor_commit_a: `0f702cb95253a7ed13b46accabe9ac9e969da7a5`
- predecessor_commit_a_tree: `ca3ace6d7879073fa2cb2b940c702e24960b275f`
- predecessor_judgment_cycle: `.aiassistant/records/aiscc/cycles/20260902_2200_aiscc-p1-8-terminal-governance-audit-acceptance-and-commit-b-sequencing-freeze-1.cycle.md`
- predecessor_audit_task: `.aiassistant/tasks/done/20260902_2159_aiscc-p1-8-terminal-governance-inventory-and-commit-b-allowlist-reconciliation-audit-1.md`
- target_bundle: `.aiassistant/reports/target/20260902_2202_aiscc-p1-8-terminal-governance-provenance-checkpoint-commit-b-persistence-1/`
- fresh_chat_policy: `NO_NEW_CHAT_REQUIRED / SAME_FRESH_SESSION_ALLOWED`
- browser_session_continuation: `HUMAN_PROVIDED — same Browser Command Center continuation is authorized`

## 0. authority

Accepted Runtime Commit A:

```text
0f702cb95253a7ed13b46accabe9ac9e969da7a5
```

2200 Command Center judgment authorizes one governance-only **Commit B provenance checkpoint**.

This Task does not authorize canonical closure.

State entering Task:

```text
P1-8_RUNTIME_HUMAN_ACCEPTED
/ RUNTIME_COMMIT_A_ACCEPTED
/ TERMINAL_GOVERNANCE_INVENTORY_ACCEPTED
/ COMMIT_B_PROVENANCE_CHECKPOINT_AUTHORIZED
```

## 1. exact goal

1. transport the exact 2202 Task and exact 2200 Cycle;
2. revalidate the accepted Commit A baseline and exact governance inventory;
3. make no content edits;
4. move this Task active→matching done before staging;
5. stage exactly the 25 accepted existing provenance files + exact 2200 Cycle + exact 2202 Task done;
6. create exactly one governance-only Commit B;
7. prove its parent/message/path/blob/tree contract;
8. export exact Commit-B-tree copies and evidence;
9. stop at `COMMIT_B_CREATED / COMMAND_CENTER_REVIEW_REQUIRED`.

Expected staged/changed path count:

```text
27
```

## 2. non-goals / forbidden

Do not edit any file contents.

Explicitly forbidden:

- runtime/source/test/migration mutation;
- canonical-state mutation;
- Handoff creation;
- rule/config mutation;
- cleanup/delete/rename of provenance;
- broad staging;
- amend/rebase/merge/revert;
- push/network/deployment/mirror generation;
- P1-8/P1 closure;
- P2 start.

Canonical files are read-only and must remain byte-identical to Commit A:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Forbidden commands/patterns:

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

Exactly two Downloads sources:

```text
C:\Users\oracl\Downloads\20260902_2202_aiscc-p1-8-terminal-governance-provenance-checkpoint-commit-b-persistence-1.md
C:\Users\oracl\Downloads\20260902_2200_aiscc-p1-8-terminal-governance-audit-acceptance-and-commit-b-sequencing-freeze-1.cycle.md
```

Exact destinations:

```text
.aiassistant/tasks/active/20260902_2202_aiscc-p1-8-terminal-governance-provenance-checkpoint-commit-b-persistence-1.md
.aiassistant/records/aiscc/cycles/20260902_2200_aiscc-p1-8-terminal-governance-audit-acceptance-and-commit-b-sequencing-freeze-1.cycle.md
```

2200 Cycle expected SHA-256:

```text
86f21a4762717bc7cf0efe2f95d0107c5332d5b32928bcba752b43c39cb542ab
```

Before either Move:

1. both exact sources exist;
2. both exact destinations do not exist;
3. Cycle SHA-256 matches.

Any failure:

```text
move neither
do not search alternate path
do not overwrite/delete
STOP: TRANSPORT_PRECONDITION_FAILED
```

All PASS:

- Move exactly both files, not Copy;
- verify destination identity and source absence.

## 4. session

Reuse of the current fresh IDE Executor session is allowed.

No new chat is required because authority is narrower than the already-executed Commit A task and runtime mutation
is forbidden.

If out-of-Task mutation is detected, do not repair/reset it. Stop before Git mutation and report exact drift.

## 5. minimum authoritative context

Read exact:

Core rules:

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`

Current:

- `.aiassistant/tasks/active/20260902_2202_aiscc-p1-8-terminal-governance-provenance-checkpoint-commit-b-persistence-1.md`
- `.aiassistant/records/aiscc/cycles/20260902_2200_aiscc-p1-8-terminal-governance-audit-acceptance-and-commit-b-sequencing-freeze-1.cycle.md`

Accepted lineage:

- `.aiassistant/records/aiscc/cycles/20260902_2159_aiscc-p1-8-runtime-commit-a-substantive-acceptance-1.cycle.md`
- `.aiassistant/tasks/done/20260902_2159_aiscc-p1-8-terminal-governance-inventory-and-commit-b-allowlist-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1.md`

Canonical state read-only identity:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`

Do not bulk-read unrelated source/logs.

## 6. repository preflight

Required before any Task lifecycle/staging:

```text
repository == ai-software-command-center
branch == main
HEAD == 0f702cb95253a7ed13b46accabe9ac9e969da7a5
HEAD tree == ca3ace6d7879073fa2cb2b940c702e24960b275f
HEAD parent == 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
index change count == 0
runtime/source/test/migration dirt == 0
```

After 2200 Cycle transport and while current Task remains active/ignored:

```text
Git-visible governance/provenance dirt count == 26
```

The exact set must equal:

- the 25 baseline rows in Section 7;
- plus the exact 2200 Cycle;
- no other path.

Any mismatch is a mandatory stop. Never auto-expand.

## 7. exact accepted 25-path baseline

Each row is:

```text
<path> <expected-sha256> <expected-no-filter-blob>
```

```text
.aiassistant/records/aiscc/cycles/20260902_1100_aiscc-p1-8-runtime-expanded-path-implementation-hold-1.cycle.md 69f2d28f09180f2fe0d02eecafc48940d1db6de44c68994dca6887f4c9ceb383 18d01364e3b9d960de258ef4f5b2c3d202386eeb
.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md f9bfb792e80b83d571066e3a72e18ba825bcf6a515e17606380492137993d77e ad73238f527eee0ba9f5c455cdd09b27a1e439f6
.aiassistant/records/aiscc/cycles/20260902_1300_aiscc-p1-8-terminal-persistence-precondition-blocked-1.cycle.md 2c3808a6510ea947146965f97455659c8edba78ebe926fb00d14e9da2735582b 1d822593063017a57170d37a8794f06c41d427a6
.aiassistant/records/aiscc/cycles/20260902_1355_aiscc-p1-8-terminal-dirty-baseline-audit-acceptance-human-disposition-gate-1.cycle.md a7ae3c92d3feba97e835a8962c6da0dd6cd66dea72732ae018cae056830e7116 6fd7330798b47e8f0f4c1da225e02e1a292f8fee
.aiassistant/records/aiscc/cycles/20260902_1621_aiscc-p1-8-runtime-commit-a-fresh-chat-precondition-blocked-1.cycle.md 0c3f2b98ed7deb96956cf2ef4e93e747870c94d20f4adf9b20fbc07228f80952 744f9a8fbe69b8971a3c1be8e677cdfd2d18a009
.aiassistant/records/aiscc/cycles/20260902_1759_aiscc-p1-8-runtime-commit-a-human-fresh-chat-precondition-blocked-1.cycle.md e0f0356506d743859f6bfef61bf91c7e1488321cc43139213fdd1e193902244f 0c5d22df1904823742000f96d8d6b2f7b047c3c8
.aiassistant/records/aiscc/cycles/20260902_1934_aiscc-p1-8-runtime-commit-a-six-semantic-equivalence-contract-rework-1.cycle.md e10b67526f142fb2ae2de6ef16318c7a6c03f5bd87da1a9176e2805e29b96366 a46c4455b5f6d281a7945475276bd68eb95f40d0
.aiassistant/records/aiscc/cycles/20260902_1940_aiscc-p1-8-runtime-commit-a-transport-authority-label-conflict-rework-1.cycle.md 328a6ca2da22f6b4d2b6aab3e1fb9449d56d3d5dec4f8f7bf70bec31e4b8d027 7b2824c98d3fe0c3d63adfc926421a8babda57b1
.aiassistant/records/aiscc/cycles/20260902_2023_aiscc-p1-8-runtime-commit-a-task-lifecycle-destination-conflict-rework-1.cycle.md 353c3dba610320b08979130f0aa17b6e5f39666ba51c3cdebd56a846dd4a8cbf 269ec87b9805b1be20ca6eb760d06f58bbae3681
.aiassistant/records/aiscc/cycles/20260902_2159_aiscc-p1-8-runtime-commit-a-substantive-acceptance-1.cycle.md 19605928d4593dd7f96038e46463d509915f8bdd5921a78535ba34a7fa38cf63 158316260ea3c153638f9afbddd73402d2e02d3a
.aiassistant/reports/aiscc/20260902_1621_aiscc-browser-command-center-session-handoff-p1-8-runtime-commit-a-fresh-chat-resume-1.md 0346ee9e121adc779bd3d04592948ab73f6579d6b9a5c0f75d358c4e92eba134 87ec57dc7d86336536d328fb58f6dcb179526b6c
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md 0795bd24b5d1b9531840424dbd7ba6c788fa08df3d19a21564e82250734fc1e7 a4c834bf01f8a9b7d3675a6bccb93558c6251e02
.aiassistant/tasks/done/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md ca616a7193a69aabd8d12f9e265152187e83806828edc7568f428669093a73b6 a307cda9fcf8e04672ed6b62d7a07af8b700ea1c
.aiassistant/tasks/done/20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1.md 73b5beb16a882d391e174d2b29d8bebb36ebcf76cd95075d3313af8085bf171a b8beb88c9f84a9ff76b567b5719a9b30641e97ee
.aiassistant/tasks/done/20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1.md 24caae66b547fe2e7cab58522e224dd77f666e7492f0ddf2c2e9c9156e5c3a00 6ce0dfd94c62c282c9b060fe4c3a08578477690d
.aiassistant/tasks/done/20260902_1100_aiscc-p1-8-runtime-provider-regression-and-metadata-parity-rework-1.md 4a423a5614e90c882d26ea2c8a47c776670f5f241bcbc3ff92583ef416e787f0 fcd33e07ef51644c248389bb8560a03b97abe7ce
.aiassistant/tasks/done/20260902_1222_aiscc-p1-8-runtime-final-acceptance-terminal-persistence-1.md f0ba64ef2a1b72e77a3a36bfdfd8fa7834bef8ef4619637a694f46a7fec02e3b f413b035ed6b8e1959c7f6d0339af03510e39b87
.aiassistant/tasks/done/20260902_1300_aiscc-p1-8-terminal-dirty-baseline-provenance-reconciliation-audit-1.md e034d2c1d7092ded19b78ebbafd39384e0b9abfdb56bd48d38a842eab84be385 7d700cd3929ebe78282864db904d1115980365a0
.aiassistant/tasks/done/20260902_1400_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-1.md b19b51eed1935cf0144038eb7c6b68c9ec0b71eff82d01c7a0c083dd02d18c76 42212338435abda2928e7c26e0cffd0f088ce3e2
.aiassistant/tasks/done/20260902_1708_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-fresh-ide-session-retry-1.md e72510c2d514f9d7bfdaf9bf4d081b996533c0b3ba51be0926bc91c8b4d49641 52f8ff31b905e860daeffc6c59f79045bc4b5725
.aiassistant/tasks/done/20260902_1849_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-fresh-ide-session-retry-2.md a271f69eb8788197990c4e7e244edb53bcbb66446a577ef3205b6043e150563c 3652c2cb1827bceb55e9f00d2e927a59f8fc8d2c
.aiassistant/tasks/done/20260902_1936_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-semantic-gate-rework-1.md 6028fd63eb50e8a59de14a348edc8cc31ca417427a2d8a8e0cd0b961dfc69e3a d68dde344ba9bf3642cc501c91505a73e6e65d20
.aiassistant/tasks/done/20260902_1942_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-transport-label-rework-1.md 95ca0d505509ef3ea60f4e2fc71af73eb09b662c92272c4b5c0a11f1c5f5e279 5a20eaa937617fbe8e3cf82a6a50c6492eb7ddac
.aiassistant/tasks/done/20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1.md 0925ba5dccbfb8c41d08f11ef7512d4fb165d5ac0c825306a10ed5fa21f71928 1229769d90a8b46f7c0be88a55912e6fe0055915
.aiassistant/tasks/done/20260902_2159_aiscc-p1-8-terminal-governance-inventory-and-commit-b-allowlist-reconciliation-audit-1.md d0de32d42441ee0fa919847283c5d254625fc3febe31ccd3f98a74b7018fd85b c9e681ad309910e851e197cc0ff7e6c8f5181ef1
```

All 25 must:

- exist as regular files;
- be Git-visible untracked against Commit A;
- have exact SHA-256 and no-filter blob shown above;
- have no HEAD blob.

## 8. exact 2200 Cycle identity

```text
path:
.aiassistant/records/aiscc/cycles/20260902_2200_aiscc-p1-8-terminal-governance-audit-acceptance-and-commit-b-sequencing-freeze-1.cycle.md

SHA-256:
86f21a4762717bc7cf0efe2f95d0107c5332d5b32928bcba752b43c39cb542ab

HEAD blob:
ABSENT
```

Compute and record its no-filter blob locally.

## 9. canonical state immutability gate

Before Task lifecycle and again before commit, prove:

```text
CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md
```

are clean against Commit A.

Do not edit them in this Task.

If any is dirty, STOP before staging:

```text
CANONICAL_STATE_UNEXPECTED_MUTATION
```

## 10. current Task lifecycle before staging

After all read-only gates PASS, Move only:

```text
.aiassistant/tasks/active/20260902_2202_aiscc-p1-8-terminal-governance-provenance-checkpoint-commit-b-persistence-1.md
→
.aiassistant/tasks/done/20260902_2202_aiscc-p1-8-terminal-governance-provenance-checkpoint-commit-b-persistence-1.md
```

Requirements before Move:

- active source exists;
- matching done destination absent.

Verify byte identity unchanged after Move.

After lifecycle, expected exact Git-visible governance dirt:

```text
27
```

It must equal:

```text
25 baseline paths
+ exact 2200 Cycle
+ exact 2202 Task done
```

No other dirty path is allowed.

`tasks/done != accepted`.

## 11. staging

Stage exactly the 27 case-sensitive paths with explicit pathspecs.

Do not use broad staging.

Verify:

```text
staged path count == 27
unstaged governance dirt == 0
runtime staged paths == 0
src/tests/migrations staged paths == 0
canonical-state staged paths == 0
rules/config staged paths == 0
target/mirror staged paths == 0
```

For the 25 baseline rows, staged blob must equal Section 7 expected no-filter blob.

For 2200 Cycle and current 2202 Task done, record staged blob and verify staged content SHA-256 against worktree bytes.

## 12. Commit B

Authorized message:

```text
docs(governance): persist P1-8 terminal provenance checkpoint
```

Create exactly one commit.

Requirements:

```text
parent == 0f702cb95253a7ed13b46accabe9ac9e969da7a5
parent count == 1
merge parent count == 0
changed path count == 27
changed path set == exact Section 10 set
runtime/source/test/migration changed paths == 0
canonical-state changed paths == 0
rules/config changed paths == 0
```

No amend and no second repair commit.

If Git author identity is unavailable, stop without changing local/global Git config.

## 13. post-commit proof

Prove:

- branch remains `main`;
- HEAD is newly created Commit B;
- Commit B parent exact accepted Commit A;
- Commit A remains unchanged;
- index empty;
- runtime/source/test/migration worktree dirt `0`;
- governance/provenance worktree dirt `0`;
- canonical three clean and byte-identical to Commit A;
- exact 27 commit paths/blobs;
- no six restored path in Commit B;
- no `.aiassistant/rules/**`;
- no repository configuration;
- no Project Source mirror/target bundle.

Do not claim Commit B accepted.

## 14. required export

Target:

```text
.aiassistant/reports/target/20260902_2202_aiscc-p1-8-terminal-governance-provenance-checkpoint-commit-b-persistence-1/
```

Required root Markdown:

```text
TASK.md
EXECUTOR_REPORT.md
GIT_OBJECT_EVIDENCE.md
GOVERNANCE_PATH_EVIDENCE.md
EXPORT_MANIFEST.md
```

Export byte-exact Commit-B-tree copies preserving repository-relative paths for all exact 27 changed paths.

Manifest binds every exported payload except itself with byte count and SHA-256.

Required report fields:

- transport proof;
- preflight;
- exact 26 pre-lifecycle inventory;
- exact 27 post-lifecycle inventory;
- canonical immutability;
- staged path/blob proof;
- Commit B hash/tree/parent/message;
- exact 27 commit-tree path/blob/SHA-256 identities;
- post-commit index/worktree;
- forbidden-not-run;
- Task lifecycle;
- sensitive-data scan without printing secret values.

## 15. evidence contract

### executor_required

- transport;
- local Git preflight;
- exact 25 baseline identity;
- 2200 Cycle identity;
- canonical-state clean proof;
- current Task lifecycle;
- exact 27 staging;
- Commit-B Git object/tree proof;
- exact 27 commit-tree export;
- manifest integrity.

### reuse_allowed

- accepted Runtime Commit A object and 2159 acceptance judgment;
- 2159 governance audit only while exact path identities remain unchanged.

### human_owned

- no Human gate before this execution;
- future Browser/Command Center substantive Commit B review;
- any later Project Source replacement or release.

### forbidden

- content mutation;
- canonical closure;
- Handoff creation;
- runtime mutation;
- broad staging/cleanup;
- network/push/deployment.

## 16. success/stop

Success:

```text
COMMIT_B_CREATED / COMMAND_CENTER_REVIEW_REQUIRED
```

Executor must not declare:

```text
COMMIT_B_ACCEPTED
P1-8 CLOSED
P1 CLOSED
P2 STARTED
```

Mandatory pre-commit stop on any identity/path/count/index/canonical mismatch.

If a post-commit object discrepancy is discovered, do not create a repair commit. Export exact evidence for Browser
Command Center review.

## 17. preserved artifacts

Preserve:

- accepted Commit A `0f702cb95253a7ed13b46accabe9ac9e969da7a5`;
- newly created Commit B candidate if successful;
- `.aiassistant/records/aiscc/cycles/20260902_2200_aiscc-p1-8-terminal-governance-audit-acceptance-and-commit-b-sequencing-freeze-1.cycle.md`;
- `.aiassistant/tasks/done/20260902_2202_aiscc-p1-8-terminal-governance-provenance-checkpoint-commit-b-persistence-1.md`;
- all exact 25 baseline provenance paths.

Target bundle is temporary until Browser substantive review.
