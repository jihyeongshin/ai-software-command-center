# 작업지시서: Retry L4 durable Luna Git persistence with exact historical provenance whitespace exception

## meta

- task_id: `20260916_1240_aiscc-p3-3-public-live-l4-durable-luna-binding-git-persistence-whitespace-exception-retry-1`
- created_at: `2026-09-16 KST`
- work_type: `COMMAND_CENTER_RECORD_UPDATE`
- evidence_profile: `BASIC`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `e287117ba021411b82560df0af61901f7a8212bb`
- predecessor_task: `20260916_1201_aiscc-p3-3-public-live-l4-durable-luna-binding-git-persistence-1`

Use the current IDE Executor conversation. No fresh chat is required.

## starting state is intentionally staged

Unlike the predecessor Task, the expected starting index is NOT empty.

Require:

```text
HEAD:
e287117ba021411b82560df0af61901f7a8212bb

staged path count:
40

staged path set:
exactly the predecessor 1201 ALLOWLIST.json set

commit from predecessor:
NONE
```

If the index is empty, has fewer/more than 40 paths, or differs from predecessor `ALLOWLIST.json`: STOP.

Do NOT reset, unstage or recreate the existing 40-path staging.

## accepted source gate

Use retained authority:

`.aiassistant/reports/target/20260916_1002_aiscc-p3-3-public-live-l4-durable-semantic-dispatch-compatibility-and-luna-binding-retry-1/SOURCE_INVENTORY.json`

Require:

`19/19 PASS`

Also require accepted migrations `0013-0016` unchanged.

No source/test/migration edit is authorized.

## exact historical provenance exception

Path:

`.aiassistant/reports/aiscc/20260916_0930_aiscc-p3-3-public-live-l4-provider-profile-proposal-v1.md`

Required SHA-256:

`2d1f17edb3b1fbe1284fb75d1018ccdbcbc94edf05055f3bc8a40c43ebd8096e`

Preserve this file byte-identically.

Do NOT normalize, rewrite, re-encode or remove its trailing blank line.

The exact allowed `git diff --cached --check` warning is:

```text
.aiassistant/reports/aiscc/20260916_0930_aiscc-p3-3-public-live-l4-provider-profile-proposal-v1.md:93: new blank line at EOF.
```

No other warning is allowed.

### equivalent whitespace gate

After final staging:

1. verify the historical file SHA exact;
2. run full `git diff --cached --check`;
3. normalize only command-output path separator if necessary for comparison;
4. require the warning set/count to equal exactly the single authorized warning above;
5. separately verify all accepted 19 source/test/migration files still match SOURCE_INVENTORY.

If output is empty, that is acceptable only if Git/platform normalization still left the historical file byte hash exact and no content changed.

If any other whitespace warning exists: STOP.

This explicit exception supersedes the predecessor zero-warning gate only for the exact path/hash above.

## inbound governance placement

Place/read this package canonically:

Cycle:
`.aiassistant/records/aiscc/cycles/20260916_1240_aiscc-p3-3-l4-git-persistence-blocked-exact-provenance-whitespace-exception-retry-1.cycle.md`

Judgment:
`.aiassistant/reports/aiscc/20260916_1240_aiscc-browser-command-center-l4-git-persistence-provenance-whitespace-exception-1.md`

Handoff:
`.aiassistant/reports/aiscc/20260916_1240_aiscc-browser-command-center-l4-git-persistence-whitespace-exception-retry-handoff-1.md`

Task active:
`.aiassistant/tasks/active/20260916_1240_aiscc-p3-3-public-live-l4-durable-luna-binding-git-persistence-whitespace-exception-retry-1.md`

Move Task to done before commit:

`.aiassistant/tasks/done/20260916_1240_aiscc-p3-3-public-live-l4-durable-luna-binding-git-persistence-whitespace-exception-retry-1.md`

## final staging

Add only the four successor governance paths:

- `.aiassistant/records/aiscc/cycles/20260916_1240_aiscc-p3-3-l4-git-persistence-blocked-exact-provenance-whitespace-exception-retry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_1240_aiscc-browser-command-center-l4-git-persistence-provenance-whitespace-exception-1.md`
- `.aiassistant/reports/aiscc/20260916_1240_aiscc-browser-command-center-l4-git-persistence-whitespace-exception-retry-handoff-1.md`
- `.aiassistant/tasks/done/20260916_1240_aiscc-p3-3-public-live-l4-durable-luna-binding-git-persistence-whitespace-exception-retry-1.md`

Expected final staged count:

`44`

Expected staged set:

```text
predecessor exact 40
+ successor exact 4
```

No other path may be staged.

## authorized Git action

Create exactly one local commit:

`feat: add durable Luna public provider pipeline`

No amend/rebase/reset.

## blocker/L4 status

Executor must preserve:

```text
PUBLIC_LIVE_L4_CALL_ROLE_PERSISTENCE_SCOPE_CONFLICT:
RESOLVED_CANDIDATE

L4 terminal:
OPEN

account/provider evidence:
HUMAN_PENDING
```

Do not claim final blocker RESOLVED or terminal L4 acceptance.

## forbidden

- source/test/migration edits;
- historical provenance normalization;
- broad git add;
- test rerun;
- PostgreSQL rerun;
- provider call;
- credential/account/billing action;
- L5/deployment;
- Public admission enablement;
- push.

## post-commit gates

Require:

- exactly one new commit;
- parent exactly `e287117ba021411b82560df0af61901f7a8212bb`;
- exact commit message;
- exact 44 committed paths;
- 19/19 accepted source identity;
- historical 0930 provenance hash unchanged;
- accepted migrations unchanged;
- index empty;
- committed tracked paths clean;
- unrelated 61 residue hashes unchanged.

## reuse_allowed

Reuse predecessor accepted evidence:

- focused `400 PASS`;
- full `1423 PASS / 3 existing SKIP / 0 FAIL / 0 ERROR`;
- PostgreSQL/restart/concurrency/fake-provider evidence.

No rerun.

## export

Target:

`.aiassistant/reports/target/20260916_1240_aiscc-p3-3-public-live-l4-durable-luna-binding-git-persistence-whitespace-exception-retry-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `COMMIT_METADATA.json`
- predecessor staged-set verification
- final 44-path inventory
- source-byte verification
- exact whitespace-exception verification
- workspace before/after

## final response

1. result
2. target bundle
3. starting HEAD
4. predecessor staged 40 verification
5. exact provenance exception verification
6. resulting commit
7. exact 44 committed paths
8. 19/19 source identity
9. post-commit index/worktree
10. blocker candidate status
11. L4 Human/account pending state
12. reused evidence
13. forbidden-not-run
