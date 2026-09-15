# 작업지시서: Persist accepted Public Live limiter retention/resource bound

## meta

- task_id: `20260916_0811_aiscc-p3-3-public-live-limiter-retention-git-persistence-1`
- created_at: `2026-09-16 KST`
- work_type: `COMMAND_CENTER_RECORD_UPDATE`
- evidence_profile: `BASIC`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `bd46b40b47cede29a8865a2b78c42f4de36dc567`
- primary_semantic_owner: `Git/public provenance persistence`

## current state

- branch: `main`
- expected HEAD: `bd46b40b47cede29a8865a2b78c42f4de36dc567`
- L3: `ACCEPTED / CLOSED`
- limiter retention implementation: `SUBSTANTIVE ACCEPTED`
- release blocker: `RESOLVED_CANDIDATE`
- Git persistence: `PENDING`
- Public admission: `DISABLED`
- Public Live: `NOT_RELEASED`

Use the current IDE Executor conversation. No fresh chat is required.

## goal

1. verify accepted 0447 source bytes;
2. stage exactly the 24-path allowlist below;
3. create exactly one local commit;
4. preserve blocker state as `RESOLVED_CANDIDATE`, not final RESOLVED;
5. report commit/path/workspace integrity.

## exact commit allowlist

Expected count:

`24`

- `migrations/versions/20260916_0016_public_live_limiter_retention.py`
- `src/aiscc/persistence/public_live_limits.py`
- `tests/integration/next_action/test_genesis_bootstrap.py`
- `tests/integration/providers/test_external_ide_execution_ingress.py`
- `tests/integration/providers/test_external_ide_execution_start.py`
- `tests/integration/public_live/test_http.py`
- `tests/integration/public_live/test_persistence.py`
- `tests/integration/public_live/test_retention.py`
- `tests/integration/self_dogfood/test_task_ready_entry.py`
- `tests/integration/task_authority/test_task_contract_durability.py`
- `tests/integration/workflow/test_postgres_kernel.py`
- `.aiassistant/records/aiscc/cycles/20260916_0445_aiscc-p3-3-public-live-l3-terminal-acceptance-retention-policy-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0445_aiscc-browser-command-center-public-live-l3-complete-retention-policy-decision-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_0445_aiscc-browser-command-center-public-live-l3-terminal-acceptance-retention-policy-selection-1.md`
- `.aiassistant/reports/aiscc/20260916_0445_aiscc-p3-3-public-live-limiter-retention-resource-bound-policy-proposal-1.md`
- `.aiassistant/records/aiscc/cycles/20260916_0447_aiscc-p3-3-limiter-retention-policy-human-acceptance-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0447_aiscc-browser-command-center-limiter-retention-policy-accepted-implementation-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_0447_aiscc-browser-command-center-limiter-retention-policy-human-acceptance-implementation-entry-1.md`
- `.aiassistant/reports/aiscc/20260916_0447_aiscc-p3-3-public-live-limiter-retention-resource-bound-policy-v1-accepted.md`
- `.aiassistant/tasks/done/20260916_0447_aiscc-p3-3-public-live-limiter-retention-resource-bound-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260916_0811_aiscc-p3-3-limiter-retention-substantive-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0811_aiscc-browser-command-center-limiter-retention-substantive-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260916_0811_aiscc-browser-command-center-limiter-retention-acceptance-persistence-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260916_0811_aiscc-p3-3-public-live-limiter-retention-git-persistence-1.md`

No other path may be staged.

## accepted source hash authority

Use retained target:

`.aiassistant/reports/target/20260916_0447_aiscc-p3-3-public-live-limiter-retention-resource-bound-implementation-1/SOURCE_INVENTORY.json`

Expected source count:

`11`

Before staging:

- verify all 11 current source/test/migration bytes match the inventory;
- verify accepted `0013`, `0014`, `0015` unchanged;
- verify accepted L2/L3 protected source unchanged;
- verify repaired Command Center baseline test unchanged;
- verify index initially empty;
- leave unrelated dirt untouched.

If the retained target inventory is missing: STOP rather than guess.

## current Task lifecycle

Before commit:

`.aiassistant/tasks/active/20260916_0811_aiscc-p3-3-public-live-limiter-retention-git-persistence-1.md`

After report/export prerequisites:

`.aiassistant/tasks/done/20260916_0811_aiscc-p3-3-public-live-limiter-retention-git-persistence-1.md`

Stage only the done path.

## authorized Git actions

```text
git add -- <each exact allowlisted path>
git commit -m "fix: bound public live limiter retention"
```

Exactly one local commit.

## forbidden

- source/test/migration edits;
- `git add .`;
- `git add -A`;
- wildcard broad staging;
- amend/rebase/reset;
- cleanup of unrelated dirt;
- PostgreSQL/runtime recreation;
- test rerun except narrow byte/diff integrity;
- L4/L5 work;
- provider call;
- Public admission enablement;
- deployment;
- Git push.

## pre-commit gates

All PASS:

1. HEAD exact;
2. index empty;
3. source hashes 11/11 equal accepted target inventory;
4. 0013/0014/0015 unchanged;
5. protected L2/L3 source unchanged;
6. exact 0445/0447 governance provenance present;
7. unrelated dirt untouched;
8. `git diff --check` PASS.

## staging gate

`git diff --cached --name-status`

must equal the exact 24-path allowlist.

No extra or missing path.

Inspect cached diff before commit.

## release blocker rule

Preserve:

```text
PUBLIC_LIVE_LIMITER_RETENTION_RESOURCE_BOUND_UNRESOLVED
implementation candidate:
RESOLVED_CANDIDATE
```

Do not write final `RESOLVED` in Executor report.

Browser Command Center owns that promotion after commit review.

## evidence contract

executor_required:

- `STATIC_SOURCE`: 11/11 accepted byte identity
- `GOVERNANCE_PROVENANCE`: complete 0445/0447/current lineage
- `GIT_STAGING`: exact 24 paths
- `GIT_COMMIT`: one local commit
- `WORKSPACE_INTEGRITY`: post-commit index empty; accepted paths clean; unrelated dirt unchanged

reuse_allowed:

- focused `186 PASS`
- full `1383 PASS / 3 SKIP / 0 FAIL / 0 ERROR`
- PostgreSQL retention/cardinality/concurrency/fail-closed evidence

only if source bytes are unchanged.

human_owned:

- final commit acceptance;
- blocker final `RESOLVED`;
- L4/L5 next action;
- Public admission/release.

not_required:

- DB runtime
- HTTP runtime
- test rerun
- provider
- deployment

## accept criteria

- exact starting HEAD;
- 11 accepted source hashes unchanged;
- exact 24 committed paths;
- one local commit;
- protected prior migrations/source unchanged;
- post-commit index empty;
- committed paths clean;
- unrelated dirt untouched;
- blocker remains only `RESOLVED_CANDIDATE` in Executor output;
- no push/deploy/provider/public enablement;
- report/export complete.

## mandatory stop

- HEAD mismatch;
- source hash mismatch;
- missing provenance;
- extra/missing staged path;
- unrelated dirty collision;
- source mutation required;
- commit hook requires out-of-scope mutation.

## export bundle

Target:

`.aiassistant/reports/target/20260916_0811_aiscc-p3-3-public-live-limiter-retention-git-persistence-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `COMMIT_METADATA.json`
- exact staged/committed inventory
- accepted-source byte verification
- workspace before/after evidence

## final response

1. result
2. target bundle
3. starting HEAD
4. resulting commit
5. exact committed path count/list
6. source byte identity
7. governance provenance
8. post-commit workspace/index
9. reused evidence
10. blocker candidate status
11. forbidden-not-run
12. human verification
13. unverified
