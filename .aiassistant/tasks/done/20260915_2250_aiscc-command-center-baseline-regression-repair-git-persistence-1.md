# 작업지시서: Persist accepted Command Center baseline regression repair

## meta

- task_id: `20260915_2250_aiscc-command-center-baseline-regression-repair-git-persistence-1`
- created_at: `2026-09-15T22:50:00+09:00`
- work_type: `COMMAND_CENTER_RECORD_UPDATE`
- evidence_profile: `BASIC`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `3709c88fc0abd2f4219228ced931a9164f286dc4`
- primary_semantic_owner: `Git/public provenance persistence`
- ide_executor_session: `FRESH_CHAT_REQUIRED`

## 현재 상태

- branch: `main`
- expected HEAD: `3709c88fc0abd2f4219228ced931a9164f286dc4`
- substantive repair: `ACCEPTED`
- baseline: `BASELINE_GREEN_RESTORED`
- public provenance: `PENDING_GIT_PERSISTENCE`
- L2: `NOT_STARTED / ENTRY_ELIGIBLE`

## 이번 턴 목표

1. accepted test change와 exact governance provenance만 stage한다.
2. staged diff가 allowlist와 정확히 일치하는지 검증한다.
3. 단일 local Git commit으로 persistence한다.
4. commit hash와 committed path inventory를 report/export한다.
5. push/deploy/L2 implementation은 하지 않는다.

## 이번 턴 비목표

- source 수정
- test fixture 추가 수정
- test 재설계
- broader test rerun
- PostgreSQL runtime 재생성
- L2 구현
- provider/deployment
- Git push
- Project Source mirror sync

## exact commit allowlist

### accepted test source

- `tests/integration/command_center/test_postgres_read_api.py`

### predecessor governance/provenance already present in workspace

- `.aiassistant/records/aiscc/cycles/20260915_2126_aiscc-p3-3-public-live-l1-terminal-acceptance-l2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2126_aiscc-browser-command-center-p3-3-public-live-l1-complete-nextaction-selection-handoff-1.md`
- `.aiassistant/reports/aiscc/20260915_2126_aiscc-p3-3-public-live-l1-terminal-browser-acceptance-1.md`
- `.aiassistant/tasks/done/20260915_2225_aiscc-command-center-issuer-verified-executor-submission-baseline-regression-repair-1.md`
- `.aiassistant/records/aiscc/cycles/20260915_2230_aiscc-command-center-baseline-repair-blocked-environment-contract-rework-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2230_aiscc-browser-command-center-baseline-repair-blocked-environment-contract-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_2230_aiscc-browser-command-center-baseline-repair-postgresql-runtime-authorized-retry-handoff-1.md`
- `.aiassistant/tasks/done/20260915_2230_aiscc-command-center-baseline-regression-repair-postgresql-runtime-authorized-retry-1.md`

### current acceptance artifacts delivered by this package

- `.aiassistant/records/aiscc/cycles/20260915_2250_aiscc-command-center-baseline-regression-repair-substantive-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2250_aiscc-browser-command-center-baseline-regression-repair-substantive-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_2250_aiscc-browser-command-center-baseline-regression-repair-persistence-entry-handoff-1.md`

### current Task lifecycle

Before commit move:

- `.aiassistant/tasks/active/20260915_2250_aiscc-command-center-baseline-regression-repair-git-persistence-1.md`
- → `.aiassistant/tasks/done/20260915_2250_aiscc-command-center-baseline-regression-repair-git-persistence-1.md`

Commit the done path, not active path.

## allowed actions

- read Task-listed canonical paths
- `git status`
- `git diff`
- `git diff --check`
- verify exact source hash/diff matches accepted repair evidence
- move current Task active → done after report/export prerequisites are prepared
- `git add -- <exact allowlist only>`
- inspect `git diff --cached --name-status`
- inspect `git diff --cached`
- create exactly one local commit
- inspect commit hash/tree/name-status
- write report/export

## explicitly authorized Git action

This Task explicitly authorizes:

```text
git add -- <exact allowlist only>
git commit -m "test: restore command center issuer-verified submission baseline"
```

No other Git mutation is authorized.

## forbidden actions

- edit accepted source or governance contents
- stage any path outside exact allowlist
- `git add .`
- `git add -A`
- broad wildcard staging
- amend/rebase/reset/checkout restore
- clean unrelated files
- push
- merge
- tag
- deploy
- PostgreSQL/runtime start
- test rerun unless a narrow static integrity check is needed
- L2 implementation

## 읽을 문서

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/records/aiscc/cycles/20260915_2250_aiscc-command-center-baseline-regression-repair-substantive-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2250_aiscc-browser-command-center-baseline-regression-repair-substantive-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_2250_aiscc-browser-command-center-baseline-regression-repair-persistence-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260915_2230_aiscc-command-center-baseline-regression-repair-postgresql-runtime-authorized-retry-1.md`

## pre-commit mandatory checks

1. HEAD exactly equals `3709c88fc0abd2f4219228ced931a9164f286dc4`.
2. The only tracked source modification is:
   - `tests/integration/command_center/test_postgres_read_api.py`
3. Its diff still matches the accepted repair:
   - two provider imports
   - `G_EXECUTOR_SUBMISSION` branch using `ExecutionReferenceAuthority`
   - `ExecutionSubmissionRef`
   - `issue_from_execution_ref`
   - no assertion/skip/xfail changes
4. Every untracked/staged path intended for commit is in exact allowlist.
5. Any unrelated dirty path must remain untouched and unstaged.
6. `git diff --check` passes.

If any condition fails: STOP before staging/commit.

## evidence contract

executor_required:

- channel: `STATIC_SOURCE`
  scope: accepted test diff identity
  pass_condition: unchanged from accepted candidate

- channel: `GIT_STAGING`
  scope: exact allowlist
  pass_condition: cached name-status contains exact expected paths and nothing else

- channel: `GIT_COMMIT`
  scope: one local commit
  pass_condition: commit succeeds and commit tree contains exact staged paths

- channel: `WORKSPACE_INTEGRITY`
  scope: post-commit status
  pass_condition: accepted paths clean; unrelated pre-existing dirt unchanged; index empty

reuse_allowed:

- channel: `FULL_SUITE`
  predecessor: `20260915_2230 accepted repair evidence`
  applicability_condition: source bytes/diff unchanged before persistence
  result: `1220 PASS / 3 SKIP / 0 FAIL / 0 ERROR`

human_owned:

- channel: `COMMAND_CENTER_FINAL_PERSISTENCE_ACCEPTANCE`
  scope: commit review and L2-entry authorization
  expected_result_format: Browser Command Center judgment

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
- L2 implementation

## accept 기준

- exact starting HEAD
- no source mutation during this Task
- exact staged allowlist only
- `git diff --check` PASS
- one commit created
- expected source/governance paths committed
- index empty after commit
- unrelated dirt untouched
- push/deploy absent
- report/export complete

## mandatory stop

- HEAD mismatch
- accepted source diff mismatch
- extra staged path
- missing required governance artifact
- unrelated dirty collision
- commit hook requires out-of-scope mutation
- any need to edit source

## report 필수 항목

- starting HEAD
- exact read paths
- pre-commit status
- accepted source diff verification
- staged exact path list
- commit command/message
- resulting commit hash
- `git show --name-status --format=fuller <commit>` equivalent
- post-commit status/index
- unrelated dirt disposition
- forbidden-not-run
- reused test evidence
- unverified items
- next recommendation

## export bundle

Target:
`.aiassistant/reports/target/20260915_2250_aiscc-command-center-baseline-regression-repair-git-persistence-1/`

Required:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- commit metadata artifact
- staged/committed path inventory

## 최종 응답

1. result
2. target bundle
3. starting HEAD
4. resulting commit
5. committed paths
6. post-commit workspace
7. reused test evidence
8. human verification
9. unverified items
