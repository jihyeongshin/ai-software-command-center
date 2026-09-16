# 작업지시서: Persist accepted L4 durable Luna provider pipeline

## meta
- task_id: `20260916_1201_aiscc-p3-3-public-live-l4-durable-luna-binding-git-persistence-1`
- created_at: `2026-09-16 KST`
- work_type: `COMMAND_CENTER_RECORD_UPDATE`
- evidence_profile: `BASIC`
- expected_orchestrator_version_or_commit: `e287117ba021411b82560df0af61901f7a8212bb`

Use the current IDE Executor conversation. No fresh chat is required.

## goal
Git persistence only.

Verify exact accepted source bytes, stage the exact 40-path allowlist, create exactly one local commit, and report workspace integrity.

## source hash authority
`.aiassistant/reports/target/20260916_1002_aiscc-p3-3-public-live-l4-durable-semantic-dispatch-compatibility-and-luna-binding-retry-1/SOURCE_INVENTORY.json`

Expected source identity: `19/19 PASS`.

If missing or mismatched: STOP.

## exact commit allowlist
Expected count: `40`

- `migrations/versions/20260916_0017_public_live_semantic_provider_requests.py`
- `src/aiscc/providers/models.py`
- `src/aiscc/providers/openai_responses.py`
- `src/aiscc/providers/service.py`
- `src/aiscc/public_live/luna_profile.py`
- `src/aiscc/public_live/provider_authority.py`
- `src/aiscc/public_live/provider_pipeline.py`
- `src/aiscc/security/policy.py`
- `tests/fixtures/providers/luna_capabilities.py`
- `tests/integration/next_action/test_genesis_bootstrap.py`
- `tests/integration/providers/test_external_ide_execution_ingress.py`
- `tests/integration/providers/test_external_ide_execution_start.py`
- `tests/integration/public_live/test_persistence.py`
- `tests/integration/public_live/test_provider_pipeline.py`
- `tests/integration/self_dogfood/test_task_ready_entry.py`
- `tests/integration/task_authority/test_task_contract_durability.py`
- `tests/integration/workflow/test_postgres_kernel.py`
- `tests/unit/providers/test_luna_profile.py`
- `tests/unit/providers/test_luna_tool.py`
- `.aiassistant/records/aiscc/cycles/20260916_0915_aiscc-p3-3-limiter-retention-terminal-closure-l4-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260916_0930_aiscc-p3-3-l4-provider-profile-human-decision-required-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260916_0950_aiscc-p3-3-l4-provider-profile-human-acceptance-implementation-entry-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260916_1002_aiscc-p3-3-l4-luna-binding-blocked-durable-dispatch-compatibility-rework-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0915_aiscc-browser-command-center-limiter-retention-terminal-closure-l4-selection-1.md`
- `.aiassistant/reports/aiscc/20260916_0915_aiscc-browser-command-center-retention-closed-l4-entry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_0930_aiscc-browser-command-center-l4-provider-profile-decision-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_0930_aiscc-browser-command-center-l4-provider-profile-human-decision-required-1.md`
- `.aiassistant/reports/aiscc/20260916_0930_aiscc-p3-3-public-live-l4-provider-profile-proposal-v1.md`
- `.aiassistant/reports/aiscc/20260916_0950_aiscc-browser-command-center-l4-provider-profile-accepted-implementation-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_0950_aiscc-browser-command-center-l4-provider-profile-human-acceptance-implementation-entry-1.md`
- `.aiassistant/reports/aiscc/20260916_0950_aiscc-p3-3-public-live-l4-provider-profile-v1-accepted.md`
- `.aiassistant/reports/aiscc/20260916_1002_aiscc-browser-command-center-l4-durable-semantic-dispatch-retry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260916_1002_aiscc-browser-command-center-l4-luna-binding-blocked-durable-dispatch-compatibility-1.md`
- `.aiassistant/tasks/done/20260916_0915_aiscc-p3-3-public-live-l4-provider-authority-and-profile-decision-preparation-1.md`
- `.aiassistant/tasks/done/20260916_0950_aiscc-p3-3-public-live-l4-provider-profile-binding-implementation-1.md`
- `.aiassistant/tasks/done/20260916_1002_aiscc-p3-3-public-live-l4-durable-semantic-dispatch-compatibility-and-luna-binding-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260916_1201_aiscc-p3-3-l4-durable-luna-binding-substantive-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_1201_aiscc-browser-command-center-l4-durable-luna-binding-substantive-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260916_1201_aiscc-browser-command-center-l4-durable-luna-binding-acceptance-persistence-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260916_1201_aiscc-p3-3-public-live-l4-durable-luna-binding-git-persistence-1.md`

No other path may be staged.

## pre-commit gates
- HEAD exact
- index empty
- accepted 0013-0016 unchanged
- 19/19 source bytes exact
- predecessor 0915/0930/0950/1002 governance provenance present
- generated `__pycache__`/runtime residue excluded
- unrelated dirt untouched
- `git diff --check` PASS

Cleanup residue is non-blocking and must not be broadly deleted.

## Task lifecycle
active:
`.aiassistant/tasks/active/20260916_1201_aiscc-p3-3-public-live-l4-durable-luna-binding-git-persistence-1.md`

done before commit:
`.aiassistant/tasks/done/20260916_1201_aiscc-p3-3-public-live-l4-durable-luna-binding-git-persistence-1.md`

Stage only the done path.

## authorized Git action
Exactly one local commit:

`feat: add durable Luna public provider pipeline`

Use explicit path staging only.

## forbidden
- source/test/migration edits
- broad git add
- test/DB rerun
- provider call
- credential/account/billing action
- L5/deployment
- Public admission enablement
- push/amend/rebase/reset

## blocker rule
Keep in Executor output:

`PUBLIC_LIVE_L4_CALL_ROLE_PERSISTENCE_SCOPE_CONFLICT = RESOLVED_CANDIDATE`

Do not claim final RESOLVED.

## L4 rule
Do not claim terminal L4 acceptance.

Account/provider evidence remains Human pending.

## reuse_allowed
If 19/19 identity passes, reuse:
- focused 400 PASS
- full 1423 PASS / 3 SKIP / 0 FAIL / 0 ERROR
- PostgreSQL/restart/concurrency/fake-provider evidence

## post-commit
- index empty
- exact committed paths clean
- unrelated/generated residue unchanged
- exactly 40 committed paths

## export
Target:
`.aiassistant/reports/target/20260916_1201_aiscc-p3-3-public-live-l4-durable-luna-binding-git-persistence-1/`

Include:
- EXPORT_MANIFEST.md
- TASK.md
- EXECUTOR_REPORT.md
- COMMIT_METADATA.json
- exact committed inventory
- source-byte verification
- workspace before/after

## final response
1. result
2. target bundle
3. starting HEAD
4. resulting commit
5. exact committed path count/list
6. 19/19 source identity
7. governance provenance
8. post-commit workspace/index
9. blocker candidate status
10. L4 account/Human pending state
11. reused evidence
12. forbidden-not-run
13. unverified
