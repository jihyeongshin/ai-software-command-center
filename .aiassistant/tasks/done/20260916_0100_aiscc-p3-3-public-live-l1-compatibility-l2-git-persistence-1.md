# 작업지시서: Persist accepted Public Live L1 Compatibility + L2 implementation

## meta

- task_id: `20260916_0100_aiscc-p3-3-public-live-l1-compatibility-l2-git-persistence-1`
- created_at: `2026-09-16T01:00:00+09:00`
- work_type: `COMMAND_CENTER_RECORD_UPDATE`
- evidence_profile: `BASIC`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `a2672c7a66bfd6b3d805caf2b187dae41b6181e5`
- primary_semantic_owner: `Git/public provenance persistence`

## 현재 상태

- branch: `main`
- expected HEAD: `a2672c7a66bfd6b3d805caf2b187dae41b6181e5`
- L1→L2 compatibility substantive result: `ACCEPTED`
- L2 substantive result: `ACCEPTED`
- Git persistence: `PENDING`
- Public admission: `DISABLED`
- Public Live: `NOT_RELEASED`

현재 IDE Executor 채팅을 그대로 사용한다. 새 채팅은 필요하지 않다.

## 이번 턴 목표

1. accepted candidate bytes/diff가 2336 Executor submission과 동일한지 확인한다.
2. 아래 exact allowlist만 stage한다.
3. staged inventory/diff를 검증한다.
4. 정확히 하나의 local commit을 만든다.
5. resulting commit hash/tree/path inventory를 report/export한다.
6. push/deploy/L3/L4/L5 work는 수행하지 않는다.

## 이번 턴 비목표

- source 수정
- migration 수정
- test 수정
- PostgreSQL runtime 생성
- full-suite 재실행
- L3/L4/L5 구현
- provider call
- Public admission enable
- deployment
- Git push
- Project Source sync

## exact commit allowlist

Expected path count:

`32`

- `migrations/versions/20260916_0014_public_live_compatibility.py`
- `src/aiscc/persistence/public_live.py`
- `src/aiscc/public_live/__init__.py`
- `src/aiscc/public_live/identity.py`
- `src/aiscc/public_live/service.py`
- `tests/integration/next_action/test_genesis_bootstrap.py`
- `tests/integration/providers/test_external_ide_execution_ingress.py`
- `tests/integration/providers/test_external_ide_execution_start.py`
- `tests/integration/public_live/conftest.py`
- `tests/integration/public_live/test_compatibility.py`
- `tests/integration/public_live/test_persistence.py`
- `tests/integration/public_live/test_service.py`
- `tests/integration/self_dogfood/test_task_ready_entry.py`
- `tests/integration/task_authority/test_task_contract_durability.py`
- `tests/integration/workflow/test_postgres_kernel.py`
- `tests/unit/public_live/test_identity.py`
- `.aiassistant/records/aiscc/cycles/20260915_2325_aiscc-command-center-baseline-regression-repair-terminal-closure-l2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2325_aiscc-browser-command-center-baseline-closed-public-live-l2-entry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260915_2325_aiscc-browser-command-center-baseline-regression-repair-terminal-acceptance-l2-selection-1.md`
- `.aiassistant/tasks/done/20260915_2325_aiscc-p3-3-public-live-l2-atomic-admission-service-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260915_2340_aiscc-p3-3-l2-blocked-invalid-authority-artifact-assumption-rework-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2340_aiscc-browser-command-center-p3-3-l2-blocked-invalid-authority-artifact-assumption-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_2340_aiscc-browser-command-center-p3-3-l2-historical-design-authority-recovery-retry-handoff-1.md`
- `.aiassistant/tasks/done/20260915_2340_aiscc-p3-3-public-live-l2-historical-design-authority-recovery-and-implementation-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260915_2336_aiscc-p3-3-l2-authority-resolved-l1-api-gap-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2336_aiscc-browser-command-center-p3-3-l1-compatibility-l2-implementation-retry-handoff-1.md`
- `.aiassistant/reports/aiscc/20260915_2336_aiscc-browser-command-center-p3-3-l2-authority-resolved-l1-api-gap-judgment-1.md`
- `.aiassistant/tasks/done/20260915_2336_aiscc-p3-3-public-live-l1-compatibility-extension-and-l2-implementation-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260916_0100_aiscc-p3-3-public-live-l1-compatibility-l2-substantive-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0100_aiscc-browser-command-center-public-live-l1-compatibility-l2-substantive-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260916_0100_aiscc-browser-command-center-public-live-l2-acceptance-persistence-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260916_0100_aiscc-p3-3-public-live-l1-compatibility-l2-git-persistence-1.md`

No other path may be staged.

## allowed Git actions

Explicitly authorized:

```text
git add -- <each exact allowlisted path>
git commit -m "feat: add public live atomic admission service"
```

Only one local commit.

## forbidden Git/actions

- `git add .`
- `git add -A`
- broad wildcard staging
- amend
- rebase
- reset
- checkout/restore unrelated paths
- clean
- push
- merge
- tag
- deployment
- source edit

## must-read

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/records/aiscc/cycles/20260916_0100_aiscc-p3-3-public-live-l1-compatibility-l2-substantive-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0100_aiscc-browser-command-center-public-live-l1-compatibility-l2-substantive-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260916_0100_aiscc-browser-command-center-public-live-l2-acceptance-persistence-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260915_2336_aiscc-p3-3-public-live-l1-compatibility-extension-and-l2-implementation-retry-1.md`

## accepted source identity gate

Before staging:

1. HEAD must exactly equal `a2672c7a66bfd6b3d805caf2b187dae41b6181e5`.
2. index must be empty.
3. the 16 accepted source/test/migration paths must match the 2336 submission hashes below.
4. no accepted source may have additional modifications.
5. accepted `20260915_0013_public_live_persistence_primitives.py` must remain unchanged.
6. `tests/integration/command_center/test_postgres_read_api.py` must remain unchanged from accepted baseline.
7. unrelated dirty paths, if any, remain untouched and unstaged.
8. `git diff --check` passes for accepted source changes.

Expected accepted SHA-256:

- `migrations/versions/20260916_0014_public_live_compatibility.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `src/aiscc/persistence/public_live.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `src/aiscc/public_live/__init__.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `src/aiscc/public_live/identity.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `src/aiscc/public_live/service.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `tests/integration/next_action/test_genesis_bootstrap.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `tests/integration/providers/test_external_ide_execution_ingress.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `tests/integration/providers/test_external_ide_execution_start.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `tests/integration/public_live/conftest.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `tests/integration/public_live/test_compatibility.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `tests/integration/public_live/test_persistence.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `tests/integration/public_live/test_service.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `tests/integration/self_dogfood/test_task_ready_entry.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `tests/integration/task_authority/test_task_contract_durability.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `tests/integration/workflow/test_postgres_kernel.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export
- `tests/unit/public_live/test_identity.py`: verify against `SOURCE_INVENTORY.json` from the 2336 target bundle/export

Use the retained 2336 target/export `SOURCE_INVENTORY.json` as the exact hash authority. If it is unavailable, use the uploaded 2336 result ZIP only if the Task transport makes it locally available without inventing a path; otherwise STOP rather than guessing hashes.

## current Task lifecycle

Before commit:

`.aiassistant/tasks/active/20260916_0100_aiscc-p3-3-public-live-l1-compatibility-l2-git-persistence-1.md`

After report/export prerequisites are ready, move to:

`.aiassistant/tasks/done/20260916_0100_aiscc-p3-3-public-live-l1-compatibility-l2-git-persistence-1.md`

Stage the done path only.

## staging gate

After exact-path staging and before commit:

- `git diff --cached --name-status` path set must equal the exact 32-path allowlist;
- no extra path;
- no missing path;
- inspect cached diff;
- verify `0013` is absent;
- verify no source content changed during this persistence turn.

Mismatch => STOP before commit.

## evidence contract

executor_required:

- channel: `STATIC_SOURCE`
  scope: accepted 2336 byte/diff identity
  pass_condition: unchanged

- channel: `GIT_STAGING`
  scope: exact 32-path allowlist
  pass_condition: exact set only

- channel: `GIT_COMMIT`
  scope: one local commit
  pass_condition: commit succeeds and tree contains exact staged paths

- channel: `WORKSPACE_INTEGRITY`
  scope: post-commit status/index
  pass_condition:
    - committed accepted paths clean
    - index empty
    - unrelated pre-existing dirt unchanged
    - no push/deploy

reuse_allowed:

- 2336 full-suite:
  `1278 PASS / 3 SKIP / 0 FAIL / 0 ERROR`
  only if all accepted source bytes are unchanged.

- 2336 PostgreSQL/security evidence:
  reusable only if migration/service bytes are unchanged.

human_owned:

- Browser Command Center final commit acceptance
- L2 terminal closure
- next DAG action selection
- public release

not_required:

- PostgreSQL runtime
- targeted tests
- full-suite rerun
- browser QA
- provider
- deployment

forbidden:

- source mutation
- staging outside allowlist
- push/deploy
- L3/L4/L5 implementation
- Public admission enablement

## accept 기준

- exact starting HEAD
- accepted source hashes unchanged
- exact 32 staged paths
- one local commit
- no 0013 mutation
- post-commit index empty
- accepted paths clean
- unrelated dirt untouched
- push/deploy absent
- report/export complete

## mandatory stop

- HEAD mismatch
- accepted hash/diff mismatch
- missing allowlisted provenance
- extra staged path
- unrelated dirty collision
- source mutation required
- commit hook requires out-of-scope mutation

## export bundle

Target:

`.aiassistant/reports/target/20260916_0100_aiscc-p3-3-public-live-l1-compatibility-l2-git-persistence-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `COMMIT_METADATA.json`
- exact staged/committed inventory
- workspace before/after evidence

## final response

1. result
2. target bundle
3. starting HEAD
4. resulting commit
5. exact committed path count/list
6. accepted source byte identity
7. post-commit workspace/index
8. reused evidence
9. forbidden-not-run
10. human verification
11. unverified
