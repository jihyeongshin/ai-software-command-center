# 작업지시서: Persist accepted Public Live L3 HTTP + shared limiter

## meta

- task_id: `20260916_0405_aiscc-p3-3-public-live-l3-git-persistence-1`
- created_at: `2026-09-16 KST`
- work_type: `COMMAND_CENTER_RECORD_UPDATE`
- evidence_profile: `BASIC`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `968a7164cb50cfeaee5a6f83b7455ab87f6ccbd1`
- primary_semantic_owner: `Git/public provenance persistence`

## current state

- branch: `main`
- expected HEAD: `968a7164cb50cfeaee5a6f83b7455ab87f6ccbd1`
- L3 substantive result: `ACCEPTED`
- Git persistence: `PENDING`
- release blocker: `PUBLIC_LIVE_LIMITER_RETENTION_RESOURCE_BOUND_UNRESOLVED`
- Public admission: `DISABLED`
- Public Live: `NOT_RELEASED`

Use the current IDE Executor conversation. No fresh chat is required.

## goal

1. place the missing 0133 provenance documents delivered by this package;
2. verify 0135 accepted source bytes against the retained target `SOURCE_INVENTORY.json`;
3. stage exactly the allowlist below;
4. create exactly one local Git commit;
5. report commit tree/path inventory and post-commit workspace;
6. do not modify source or resolve the retention blocker in this persistence turn.

## exact commit allowlist

Expected path count:

`37`

- `migrations/versions/20260916_0015_public_live_shared_limits.py`
- `src/aiscc/persistence/public_live_limits.py`
- `src/aiscc/public_live/http.py`
- `src/aiscc/public_live/source.py`
- `tests/integration/next_action/test_genesis_bootstrap.py`
- `tests/integration/providers/test_external_ide_execution_ingress.py`
- `tests/integration/providers/test_external_ide_execution_start.py`
- `tests/integration/public_live/test_http.py`
- `tests/integration/public_live/test_persistence.py`
- `tests/integration/public_live/test_shared_limits.py`
- `tests/integration/self_dogfood/test_task_ready_entry.py`
- `tests/integration/task_authority/test_task_contract_durability.py`
- `tests/integration/workflow/test_postgres_kernel.py`
- `tests/public_live_http_helpers.py`
- `tests/unit/public_live/test_http.py`
- `tests/unit/public_live/test_source.py`
- `.aiassistant/records/aiscc/cycles/20260916_0110_aiscc-p3-3-public-live-l2-terminal-acceptance-l3-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0110_aiscc-browser-command-center-public-live-l2-complete-l3-entry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_0110_aiscc-browser-command-center-public-live-l2-terminal-acceptance-l3-selection-1.md`
- `.aiassistant/tasks/done/20260916_0110_aiscc-p3-3-public-live-l3-frozen-http-stage-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260916_0122_aiscc-p3-3-l3-blocked-missing-shared-rate-limit-authority-rework-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0122_aiscc-browser-command-center-p3-3-l3-blocked-shared-rate-limit-authority-judgment-1.md`
- `.aiassistant/reports/aiscc/20260916_0122_aiscc-browser-command-center-p3-3-shared-limit-l3-retry-handoff-1.md`
- `.aiassistant/tasks/done/20260916_0122_aiscc-p3-3-public-live-shared-limit-extension-and-l3-implementation-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260916_0133_aiscc-p3-3-l3-shared-limit-policy-ambiguity-human-decision-required-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0133_aiscc-browser-command-center-p3-3-l3-shared-limit-policy-human-decision-required-1.md`
- `.aiassistant/reports/aiscc/20260916_0133_aiscc-browser-command-center-p3-3-l3-shared-limit-policy-decision-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_0133_aiscc-p3-3-public-live-shared-limit-policy-amendment-proposal-1.md`
- `.aiassistant/records/aiscc/cycles/20260916_0135_aiscc-p3-3-shared-limit-policy-human-acceptance-l3-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0135_aiscc-browser-command-center-shared-limit-policy-accepted-l3-retry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_0135_aiscc-browser-command-center-shared-limit-policy-human-acceptance-l3-retry-1.md`
- `.aiassistant/reports/aiscc/20260916_0135_aiscc-p3-3-public-live-shared-limit-policy-amendment-v1-accepted.md`
- `.aiassistant/tasks/done/20260916_0135_aiscc-p3-3-public-live-shared-limit-and-l3-implementation-human-policy-authorized-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260916_0405_aiscc-p3-3-public-live-l3-substantive-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0405_aiscc-browser-command-center-public-live-l3-substantive-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260916_0405_aiscc-browser-command-center-public-live-l3-acceptance-persistence-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260916_0405_aiscc-p3-3-public-live-l3-git-persistence-1.md`

No other path may be staged.

## accepted byte authority

Primary source-hash authority:

`.aiassistant/reports/target/20260916_0135_aiscc-p3-3-public-live-shared-limit-and-l3-implementation-human-policy-authorized-retry-1/SOURCE_INVENTORY.json`

Expected accepted source count:

`16`

Before staging, verify all 16 current workspace source/test/migration bytes equal that inventory.

Also verify:

- `migrations/versions/20260915_0013_public_live_persistence_primitives.py` unchanged;
- `migrations/versions/20260916_0014_public_live_compatibility.py` unchanged;
- accepted L2 implementation bytes unchanged;
- repaired Command Center baseline test unchanged.

If retained target hash evidence is missing: STOP rather than guessing.

## 0133 transport rule

This ZIP contains the four 0133 provenance files that were not previously placed in the canonical Executor repository.

Place them as:

- CYCLE → `.aiassistant/records/aiscc/cycles/`
- JUDGMENT/HANDOFF/PROPOSAL → `.aiassistant/reports/aiscc/`

They must be byte-identical to the delivery package.

Do not reinterpret the 0133 proposal as accepted authority.

0135 accepted V1 remains controlling.

## current Task lifecycle

Before commit:

`.aiassistant/tasks/active/20260916_0405_aiscc-p3-3-public-live-l3-git-persistence-1.md`

After report/export prerequisites:

`.aiassistant/tasks/done/20260916_0405_aiscc-p3-3-public-live-l3-git-persistence-1.md`

Stage the done path only.

## authorized Git action

```text
git add -- <each exact allowlisted path>
git commit -m "feat: add public live HTTP shared limits"
```

Exactly one local commit.

## forbidden actions

- source/test/migration edits;
- limiter retention/GC implementation;
- test rerun except narrow static byte/diff integrity checks;
- PostgreSQL/runtime creation;
- `git add .`;
- `git add -A`;
- wildcard broad staging;
- amend/rebase/reset;
- clean unrelated files;
- push/tag/merge;
- provider call;
- L4/L5 implementation;
- deployment;
- Public admission enablement.

## pre-commit gates

All must PASS:

1. starting HEAD exact;
2. index initially empty;
3. 16 accepted source bytes exactly match SOURCE_INVENTORY;
4. exact 0133 provenance delivered and placed;
5. accepted 0013/0014 unchanged;
6. accepted L2 source unchanged;
7. unrelated dirt untouched;
8. `git diff --check` PASS.

## staging gate

Before commit:

```text
git diff --cached --name-status
```

must equal the exact 37-path allowlist.

No extra path and no missing path.

Inspect cached diff and verify no source mutation occurred in this turn.

## evidence contract

executor_required:

- `STATIC_SOURCE`
  - accepted 16-source byte identity PASS

- `GOVERNANCE_PROVENANCE`
  - 0110/0122/0133/0135 + current acceptance lineage complete

- `GIT_STAGING`
  - exact 37 paths only

- `GIT_COMMIT`
  - one local commit

- `WORKSPACE_INTEGRITY`
  - index empty after commit
  - committed accepted paths clean
  - unrelated dirt unchanged
  - no push/deploy

reuse_allowed:

- 0135 focused `178 PASS`
- 0135 full suite `1375 PASS / 3 SKIP / 0 FAIL / 0 ERROR`
- 0135 PostgreSQL/shared/concurrency/HTTP/security proof

only if all accepted source bytes are unchanged.

human_owned:

- Browser Command Center final persistence acceptance;
- L3 terminal closure;
- next DAG/release-blocker selection;
- Public admission/release.

not_required:

- PostgreSQL runtime
- HTTP runtime
- provider
- test rerun
- browser QA

forbidden:

- source mutation
- retention-policy invention
- staging outside allowlist
- push/deploy
- Public admission enablement

## release blocker preservation

Report must preserve exactly:

```text
PUBLIC_LIVE_LIMITER_RETENTION_RESOURCE_BOUND_UNRESOLVED
```

Do NOT mark it resolved.

Do NOT implement a cleanup policy.

Persistence of L3 does not authorize Public Live enablement.

## accept criteria

- starting HEAD exact;
- accepted 16-source bytes unchanged;
- exact 37 staged/committed paths;
- one local commit;
- 0013/0014/L2 unchanged;
- post-commit index empty;
- committed paths clean;
- unrelated dirt untouched;
- release blocker preserved unresolved;
- no push/deploy/provider/public enablement;
- report/export complete.

## mandatory stop

- HEAD mismatch;
- accepted source hash mismatch;
- missing 0133 provenance file;
- extra/missing staged path;
- unrelated dirty collision;
- source mutation required;
- commit hook requires out-of-scope mutation.

## export bundle

Target:

`.aiassistant/reports/target/20260916_0405_aiscc-p3-3-public-live-l3-git-persistence-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `COMMIT_METADATA.json`
- exact staged/committed path inventory
- source byte verification
- workspace before/after evidence

## final response

1. result
2. target bundle
3. starting HEAD
4. resulting commit
5. exact committed path count/list
6. accepted source byte identity
7. 0133 provenance placement
8. post-commit workspace/index
9. reused evidence
10. release blocker status
11. forbidden-not-run
12. human verification
13. unverified
