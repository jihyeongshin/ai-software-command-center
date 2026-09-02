# 작업지시서: P1-8 terminal governance inventory and Commit B allowlist reconciliation audit

## meta

- task_id: `20260902_2159_aiscc-p1-8-terminal-governance-inventory-and-commit-b-allowlist-reconciliation-audit-1`
- created_at: `2026-09-02T21:59:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P1-8 — Project Memory and Cycle Admission`
- work_type: `READ_ONLY_AUDIT / TERMINAL_GOVERNANCE_RECONCILIATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `terminal governance inventory / future Commit B exact allowlist`
- predecessor_commit_a: `0f702cb95253a7ed13b46accabe9ac9e969da7a5`
- predecessor_commit_a_tree: `ca3ace6d7879073fa2cb2b940c702e24960b275f`
- predecessor_commit_a_parent: `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
- predecessor_task: `.aiassistant/tasks/done/20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1.md`
- predecessor_judgment_cycle: `.aiassistant/records/aiscc/cycles/20260902_2159_aiscc-p1-8-runtime-commit-a-substantive-acceptance-1.cycle.md`
- target_bundle: `.aiassistant/reports/target/20260902_2159_aiscc-p1-8-terminal-governance-inventory-and-commit-b-allowlist-reconciliation-audit-1/`
- fresh_chat_policy: `NO_NEW_CHAT_REQUIRED / READ_ONLY_AUDIT`
- browser_session_continuation: `HUMAN_PROVIDED — same Browser Command Center continuation is authorized`

## 0. current accepted authority

Browser Command Center has substantively accepted Runtime Commit A persistence:

```text
Commit A:
0f702cb95253a7ed13b46accabe9ac9e969da7a5

tree:
ca3ace6d7879073fa2cb2b940c702e24960b275f

parent:
1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a

message:
feat(runtime): complete P1-8 project memory and cycle admission

changed path count:
36

accepted aggregate:
a82d94c1d607bc379c12d0768ff54d0cd481467eb731e0884f63176bd1207f3c
```

Human runtime acceptance remains:

```text
Human P1-8 runtime final review:
ACCEPTED
```

Exact-six disposition has been executed and accepted:

```text
RESTORE_SIX_TO_EXACT_HEAD
→ six clean against predecessor HEAD
→ six absent from Commit A
```

Current semantic state:

```text
P1-8_RUNTIME_HUMAN_ACCEPTED
/ SIX_RESTORED
/ RUNTIME_COMMIT_A_ACCEPTED
/ TERMINAL_GOVERNANCE_PENDING
```

This Task does not authorize P1-8 closure.

## 1. purpose

The 2025 Executor reports final Git-visible governance/provenance dirt count `23`.

Repeated blocked/rework turns added durable Task/Cycle provenance after the older terminal-persistence Commit-B
allowlist was designed.

The purpose of this Task is to enumerate and classify the **actual local-canonical governance dirt** after accepted
Commit A so the Browser Command Center can issue a later exact governance-only Commit B Task without auto-expanding
a stale allowlist.

This Task is audit-only.

## 2. non-goals / forbidden actions

Do not:

- edit runtime/source/test/migration bytes;
- edit governance/canonical records;
- restore/reset/checkout/clean/stash any worktree path;
- stage any path;
- create/amend/revert/rebase/merge any commit;
- change Git configuration;
- delete/rename cleanup candidates;
- update CURRENT_STATE_SUMMARY / DECISION_REGISTER / NEXT_ACTIONS;
- create final P1-8 closure Cycle/Handoff;
- create Commit B;
- start P2;
- push, fetch, pull, query remote, create PR/release/deploy;
- generate Project Source mirror.

Explicitly forbidden:

```text
git add
git add .
git add -A
git reset
git reset --hard
git restore
git checkout
git clean
git stash
git commit
git commit --amend
git revert
git rebase
git merge
```

Task active→done provenance lifecycle is the only repository file move authorized by this Task after report/export.

## 3. Downloads transport

Transport exactly two files.

Sources:

```text
C:\Users\oracl\Downloads\20260902_2159_aiscc-p1-8-terminal-governance-inventory-and-commit-b-allowlist-reconciliation-audit-1.md
C:\Users\oracl\Downloads\20260902_2159_aiscc-p1-8-runtime-commit-a-substantive-acceptance-1.cycle.md
```

Destinations:

```text
.aiassistant/tasks/active/20260902_2159_aiscc-p1-8-terminal-governance-inventory-and-commit-b-allowlist-reconciliation-audit-1.md
.aiassistant/records/aiscc/cycles/20260902_2159_aiscc-p1-8-runtime-commit-a-substantive-acceptance-1.cycle.md
```

Expected judgment Cycle SHA-256:

```text
19605928d4593dd7f96038e46463d509915f8bdd5921a78535ba34a7fa38cf63
```

Before moving either file, atomically verify:

1. both exact Downloads sources exist;
2. both exact destinations do not exist;
3. Cycle source SHA-256 equals the expected value above.

If any check fails:

```text
move neither file
do not search another path
do not overwrite/delete a destination
STOP: TRANSPORT_PRECONDITION_FAILED
```

If all pass, Move exactly those two files, not Copy, and verify destination identity plus Downloads-source absence.

## 4. session authority

No new IDE chat is required.

This Task reduces authority from destructive Commit-A persistence to read-only terminal-governance audit.

Reuse of the current fresh IDE session is allowed.

If there is evidence of an out-of-Task runtime/index/commit mutation after 2025, report it and continue only in
read-only reconciliation mode. Never force the repository back to this Task's expected baseline.

## 5. minimum authoritative context

After transport, read exact canonical paths:

Core rules:

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`

Current:

- `.aiassistant/tasks/active/20260902_2159_aiscc-p1-8-terminal-governance-inventory-and-commit-b-allowlist-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260902_2159_aiscc-p1-8-runtime-commit-a-substantive-acceptance-1.cycle.md`

Accepted Commit A lineage:

- `.aiassistant/tasks/done/20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260902_2023_aiscc-p1-8-runtime-commit-a-task-lifecycle-destination-conflict-rework-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260902_1934_aiscc-p1-8-runtime-commit-a-six-semantic-equivalence-contract-rework-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260902_1355_aiscc-p1-8-terminal-dirty-baseline-audit-acceptance-human-disposition-gate-1.cycle.md`
- `.aiassistant/reports/aiscc/20260902_1621_aiscc-browser-command-center-session-handoff-p1-8-runtime-commit-a-fresh-chat-resume-1.md`

Earlier terminal persistence design:

- `.aiassistant/tasks/done/20260902_1222_aiscc-p1-8-runtime-final-acceptance-terminal-persistence-1.md`

Canonical state:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`

Do not bulk-read unrelated rules/records/source/logs.

## 6. repository/Commit A read-only preflight

Record exact current:

```text
repository
branch
HEAD
HEAD tree
HEAD parent(s)
index entry count
runtime/source/test/migration Git-visible dirt
governance/provenance Git-visible dirt
```

Expected no-drift baseline from 2025:

```text
repository: ai-software-command-center
branch: main
HEAD: 0f702cb95253a7ed13b46accabe9ac9e969da7a5
HEAD tree: ca3ace6d7879073fa2cb2b940c702e24960b275f
HEAD parent: 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
index: empty
runtime/source/test/migration dirty: 0
Git-visible governance/provenance before this new Cycle placement: 23
```

After transporting the current judgment Cycle and active Task, expected no-drift governance count:

```text
24
```

because the Cycle is Git-visible and the active Task directory is expected to be ignored.

Do not treat mismatch as authority to restore/reset. Record exact drift.

## 7. re-prove accepted Commit A identity locally

Using local Git objects only, verify:

```text
HEAD == 0f702cb95253a7ed13b46accabe9ac9e969da7a5
tree == ca3ace6d7879073fa2cb2b940c702e24960b275f
parent count == 1
parent == 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
merge parent count == 0
message == feat(runtime): complete P1-8 project memory and cycle admission
changed path count == 36
```

Read the accepted 36 path/hash set from the exact 2025 done Task Section 12.

For each Commit-A path, recompute SHA-256 from:

```text
0f702cb95253a7ed13b46accabe9ac9e969da7a5:<path>
```

Require:

```text
36/36 exact
aggregate == a82d94c1d607bc379c12d0768ff54d0cd481467eb731e0884f63176bd1207f3c
```

Also prove:

```text
six restore paths in Commit A diff == 0
.aiassistant/** paths in Commit A diff == 0
repository configuration paths in Commit A diff == 0
```

This is read-only verification. If Commit A identity differs, do not repair it.

## 8. exact governance/provenance inventory

Enumerate every Git-visible path outside:

```text
src/**
tests/**
migrations/**
```

that differs from HEAD or is untracked.

For each entry record:

- porcelain/status code;
- exact case-sensitive repository-relative path;
- tracked/untracked;
- current byte size if regular file;
- current SHA-256 if regular file;
- current `git hash-object --no-filters` blob identity if regular file;
- HEAD blob identity if path exists in HEAD;
- rename old/new path if Git reports rename;
- whether the path is currently under tasks/active, tasks/done, cycles, canonical state, reports/aiscc, rules, or another category.

Do not collapse rename pairs or infer that two paths are equivalent.

Record the exact ordinal-sorted inventory and its count.

For no-drift baseline after current Cycle transport, expected count is `24`.

## 9. classification buckets

Classify each exact inventory row without mutating it into one of:

```text
A. durable accepted/review provenance
   - Task done
   - judgment/HOLD/acceptance Cycle
   - required durable Handoff/report

B. canonical state candidate
   - CURRENT_STATE_SUMMARY.md
   - DECISION_REGISTER.md
   - NEXT_ACTIONS.md

C. current terminal-governance Task provenance
   - current audit Task active/done lifecycle

D. superseded/non-canonical candidate
   - Browser Handoff or artifact explicitly declared superseded/non-canonical

E. unexpected governance/configuration path
   - no existing authority/classification basis
```

Classification is evidence preparation only. Executor does not decide which category Human/Command Center ultimately
commits or deletes.

## 10. compare against older Commit-B design

Read the exact 1222 terminal-persistence Task's intended Commit-B contract.

Report:

1. every old allowlisted path that is currently present;
2. every old allowlisted path that is currently absent/clean/already committed;
3. every currently dirty path not in that old allowlist;
4. whether active→done lifecycle history creates old/new-path ambiguity;
5. whether the old Commit-B count can still be used exactly.

Expected conclusion must be evidence-driven.

Do not auto-expand the legacy allowlist.

## 11. canonical state semantic audit

Read-only inspect:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Determine whether each currently records or omits:

- actual Runtime Commit A SHA `0f702cb95253a7ed13b46accabe9ac9e969da7a5`;
- Runtime Commit A accepted status;
- six-restored state;
- `TERMINAL_GOVERNANCE_PENDING`;
- P1-8 not yet closed;
- Commit B not yet created;
- P1 not yet closed;
- P2 not yet started.

Report exact relevant headings/keys and current values.

Do not edit the files.

## 12. future Commit B candidate analysis

Produce a **candidate**, not authority.

Candidate must specify separately:

```text
existing dirty provenance paths proposed for Commit B
canonical state files that require mutation before Commit B
new final acceptance/closure Cycle that would need to be created
new durable handoff/next-action report, if required
future terminal-persistence Task done path
paths explicitly excluded
```

A future Commit B must, at minimum, be evaluated against:

```text
parent == accepted Commit A 0f702cb95253a7ed13b46accabe9ac9e969da7a5
runtime tree unchanged from Commit A
src/tests/migrations changed by Commit B == 0
only exact Command-Center-authorized governance allowlist
index empty after commit
no target bundle / Project Source mirror / repository config
no push/network/deployment
```

Do not stage the candidate.

## 13. required export

Target:

```text
.aiassistant/reports/target/20260902_2159_aiscc-p1-8-terminal-governance-inventory-and-commit-b-allowlist-reconciliation-audit-1/
```

Required root Markdown:

```text
TASK.md
EXECUTOR_REPORT.md
GOVERNANCE_INVENTORY.md
COMMIT_A_OBJECT_EVIDENCE.md
COMMIT_B_ALLOWLIST_ANALYSIS.md
EXPORT_MANIFEST.md
```

Also export byte-exact copies, preserving repository-relative paths, of:

- every Git-visible governance/provenance inventory regular file;
- the three canonical state files even if currently clean;
- the exact 1222 terminal-persistence Task;
- the exact 2025 done Task;
- the current 2159 acceptance Cycle.

Do not export credentials/private data. If a file contains suspected secret material, record only path/classification
and omit content while explaining the omission without printing the secret.

Manifest must bind every exported payload except itself with byte count and SHA-256.

## 14. current Task lifecycle

After read-only audit/report/export completion, Move only:

```text
.aiassistant/tasks/active/20260902_2159_aiscc-p1-8-terminal-governance-inventory-and-commit-b-allowlist-reconciliation-audit-1.md
→
.aiassistant/tasks/done/20260902_2159_aiscc-p1-8-terminal-governance-inventory-and-commit-b-allowlist-reconciliation-audit-1.md
```

Do not stage or commit it.

After this lifecycle, expected no-drift governance count becomes:

```text
25
```

because current Task done becomes Git-visible.

`tasks/done != accepted`.

## 15. evidence contract

### executor_required

- exact Downloads transport proof;
- read-only repository/Commit-A object proof;
- accepted-36 Commit-A tree recomputation;
- exact governance inventory with per-path identities;
- legacy Commit-B allowlist comparison;
- canonical state semantic audit;
- future Commit-B candidate analysis;
- target export and manifest integrity;
- current Task lifecycle proof.

### reuse_allowed

- Human accepted exact-36 result;
- accepted Runtime Commit A judgment Cycle;
- earlier 1222 terminal Commit-B design only as historical design input, not as current allowlist authority.

### human_owned

- any new Human policy/acceptance decision if later required;
- Project Source replacement;
- push/release/deployment.

### not_required

- runtime tests;
- DB/container;
- browser/provider/network evidence;
- new IDE chat.

### forbidden

- runtime/governance edits;
- staging;
- commit;
- cleanup/reset/restore;
- network/remote;
- P1/P2 state mutation.

## 16. mandatory stop / drift semantics

Because this Task is read-only, repository drift does not authorize repair.

If expected baseline differs:

```text
READ_ONLY_RECONCILIATION_REQUIRED
```

Continue only far enough to report exact current state when safe.

Stop entirely if:

- Task/Cycle transport identity fails;
- repository path cannot be identified;
- evidence collection would require mutation;
- a requested file cannot be read without secret exposure and no safe metadata-only alternative exists.

## 17. success result

Successful Executor result:

```text
TERMINAL_GOVERNANCE_INVENTORY_AUDITED
/ COMMIT_B_ALLOWLIST_COMMAND_CENTER_REVIEW_REQUIRED
/ NO_MUTATION
```

Executor must not declare:

```text
COMMIT_B_READY
P1-8 CLOSED
P1 CLOSED
P2 STARTED
```

## 18. preserved artifacts

Preserve:

- `.aiassistant/records/aiscc/cycles/20260902_2159_aiscc-p1-8-runtime-commit-a-substantive-acceptance-1.cycle.md`
- `.aiassistant/tasks/done/20260902_2159_aiscc-p1-8-terminal-governance-inventory-and-commit-b-allowlist-reconciliation-audit-1.md`
- `.aiassistant/tasks/done/20260902_2025_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-task-lifecycle-rework-1.md`
- Runtime Commit A `0f702cb95253a7ed13b46accabe9ac9e969da7a5`
- all accepted predecessor P1-8 Tasks/Cycles/Handoffs already required by canonical lineage.

Target bundle is temporary until Browser Command Center substantive review.
