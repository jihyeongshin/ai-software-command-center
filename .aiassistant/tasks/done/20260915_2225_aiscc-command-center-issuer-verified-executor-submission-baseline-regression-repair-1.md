# 작업지시서: Command Center issuer-verified executor-submission baseline regression repair

## meta

- task_id: `20260915_2225_aiscc-command-center-issuer-verified-executor-submission-baseline-regression-repair-1`
- created_at: `2026-09-15T22:25:00+09:00`
- work_type: `REWORK`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `3709c88fc0abd2f4219228ced931a9164f286dc4`
- primary_semantic_owner: `Command Center integration test baseline / current G_EXECUTOR_SUBMISSION authority contract`
- ide_executor_session: `FRESH_CHAT_REQUIRED`

## 현재 상태

- branch: `main`
- expected HEAD before work: `3709c88fc0abd2f4219228ced931a9164f286dc4`
- predecessor commit parent: `209e7534f66e9b07ce9d33742e6993370a70f4fb`
- predecessor phase result: `P3-3 PUBLIC LIVE L1 IMPLEMENTED / ACCEPTED / CLOSED`
- Public Live: `NOT_RELEASED`
- Public admission: `DISABLED`
- L2: `NOT_STARTED / ENTRY_ELIGIBLE`
- open blocker/debt: broader baseline has exactly three known Command Center integration failures.
- predecessor broader-suite result:
  - `1197 PASS`
  - `3 FAIL`
  - `3 SKIP`
  - `0 ERROR`
- shared failure:
  - `ValueError: G_EXECUTOR_SUBMISSION requires an issuer-verified execution ref`
- predecessor disposition:
  - `PREEXISTING_NOT_L1_CAUSED`
  - `DEFERRED_SEPARATE_TASK`

Exact known failures:

1. `tests/integration/command_center/test_postgres_read_api.py::test_postgres_read_models_http_runtime_and_no_mutation`
2. `tests/integration/command_center/test_postgres_read_api.py::test_postgres_conflict_and_http_503_fail_closed`
3. `tests/integration/command_center/test_web_ui.py::test_default_entrypoint_ui_queue_etag_and_event_no_mutation`

## 이번 턴 목표

1. 위 세 Command Center integration test/fixture가 현재 `G_EXECUTOR_SUBMISSION` issuer-verification authority contract에 맞는 execution ref를 생성하도록 교정한다.
2. stronger current guard를 그대로 유지하고 old fixture만 current contract에 정렬한다.
3. exact three failures를 통과시킨 뒤 기존 full-suite environment에서 broader baseline을 다시 실행하여 green baseline을 복구한다.
4. 변경이 test-only인지 검증하고, L2 구현에 들어가기 전에 회귀 attribution 가능한 clean baseline을 복원한다.

## 이번 턴 비목표

- Public Live L2 구현
- Public Live L4 provider profile 작업
- Public Live L5 Railway ingress/sandbox/deployment proof
- `G_EXECUTOR_SUBMISSION` guard/authority 완화
- product runtime behavior 변경
- 새로운 WorkflowState, Evidence rule, Judgment rule 설계
- 새 DB/runtime harness 구축
- provider paid call
- deployment
- Git commit/push
- unrelated failing test 정리

## 허용 범위

allowed_paths:
- `tests/integration/command_center/test_postgres_read_api.py`
- `tests/integration/command_center/test_web_ui.py`
- 위 exact tests가 직접 사용하는 기존 shared test fixture/helper가 별도 파일에 있을 경우 그 파일 1개 이상을 최소 범위로 추가할 수 있다. 단, 각 추가 path와 필요성을 report에 명시한다.
- test-only support path 외 product/runtime source 수정은 허용하지 않는다.
- `.aiassistant/tasks/active/**`
- `.aiassistant/tasks/done/**`
- `.aiassistant/reports/target/**`

allowed_actions:
- expected HEAD / workspace 상태 확인
- 아래 must-read exact path 읽기
- exact error text와 `G_EXECUTOR_SUBMISSION` current implementation/fixture producer를 좁게 추적
- current issuer-verified execution ref를 생성하는 accepted test helper 또는 canonical construction path 재사용
- 허용 test/fixture만 수정
- exact three targeted integration tests 실행
- 현재 repository의 기존 full-suite command/environment 재사용
- `git diff --check` 또는 동등한 changed-path validation
- report/export 작성
- executor-required 작업 완료 후 Task를 `tasks/done`으로 이동

## 절대 금지

forbidden_paths:
- production/application/runtime source
- canonical governance baseline 수정
- migration/schema 변경
- deployment/resource configuration
- provider credential/budget configuration
- unrelated tests

forbidden_actions:
- `G_EXECUTOR_SUBMISSION`의 issuer-verification 조건 삭제/완화/bypass
- stale/unsigned/unverified execution ref를 current authority처럼 허용
- 세 failing test를 skip/xfail/delete/조건부 무시
- assertion을 약화해 failure를 숨김
- predecessor debt를 L1 regression으로 재분류 without new evidence
- unrelated failing test를 함께 고침
- 새 DB/runtime/browser/network/credential 환경 구성
- provider paid call
- deployment
- Git index / commit / push
- root `.gitignore` 또는 Git policy 변경
- unrelated dirty file reset/cleanup

## 읽을 문서

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`
- `.aiassistant/records/aiscc/cycles/20260915_2126_aiscc-p3-3-public-live-l1-terminal-acceptance-l2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2126_aiscc-p3-3-public-live-l1-terminal-browser-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260915_2126_aiscc-browser-command-center-p3-3-public-live-l1-complete-nextaction-selection-handoff-1.md`

## agent instruction transport / authority

- repository-root instruction entrypoint는 thin transport bootstrap이며 policy authority가 아니다.
- Task File의 위 목록은 minimum authoritative context set이다.
- unrelated rules/records/source/logs를 bulk-read하지 않는다.
- current source에서 `G_EXECUTOR_SUBMISSION` issuer-verification contract의 canonical owner가 추가로 확인되면 그 exact owner path만 읽고 report에 추가한다.
- active Task, canonical rule, current source, accepted predecessor evidence가 충돌하면 mutation을 중단하고 `POLICY_CONFLICT_INVESTIGATION_REQUIRED`로 보고한다.
- predecessor Handoff의 핵심 경계는 current guard 유지 + fixture repair이다.

## 조사할 source

반드시 좁게 확인:

1. exact error string:
   - `G_EXECUTOR_SUBMISSION requires an issuer-verified execution ref`
2. `G_EXECUTOR_SUBMISSION` guard/evaluation code path
3. issuer verification을 만족하는 execution ref의 current construction/admission path
4. 위 세 failing tests가 사용하는 stale fixture/factory/helper
5. 이미 green인 nearby tests 중 current issuer-verified ref 생성 예제가 있는지

우선 current accepted helper를 재사용하고, 불필요한 새 fixture abstraction을 만들지 않는다.

## 구현/문서/감사 범위

- 이 작업은 test baseline repair다.
- expected product source changes: `none`
- expected governance/provenance source changes: `Task lifecycle only`
- expected repository configuration changes: `none`
- expected test changes:
  - exact three failing tests가 current issuer-verified execution ref를 사용하도록 fixture/factory 정렬
  - 필요 시 직접 공유하는 최소 test helper 수정
- test가 current contract를 잘못 가정했음을 드러내는 최소 주석은 허용하지만 장문 설명은 금지한다.

## workflow transition expectation

- initial_state: `L1 CLOSED / baseline debt open / L2 ENTRY_ELIGIBLE`
- expected_non_terminal_state_when_human_pending: `NOT_APPLICABLE`
- expected_terminal_candidate: `BASELINE_GREEN_RESTORED / L2 still NOT_STARTED`
- transition_authority: `NOT_APPLICABLE`
- Agent가 직접 P3-3/Public Live terminal/release state를 결정할 수 있는가: `No`

## evidence contract

executor_required:

- channel: `STATIC_SOURCE`
  scope: `G_EXECUTOR_SUBMISSION current guard와 issuer-verification requirement가 변경되지 않았음을 diff/source로 확인`
  allowed_command_or_environment: `repository-local read/diff only`
  pass_condition: `production/runtime source와 authority guard 변경 0`

- channel: `INTEGRATION_TEST`
  scope: `위 exact three known failing tests`
  allowed_command_or_environment: `현재 repository가 이미 사용하는 existing local test environment`
  pass_condition: `3/3 PASS, 0 FAIL, 0 ERROR`

- channel: `FULL_SUITE`
  scope: `predecessor broader suite와 동일한 repository full-suite command/environment`
  allowed_command_or_environment: `existing local environment only; 새 harness/service provisioning 금지`
  pass_condition: `0 FAIL / 0 ERROR; predecessor의 legitimate skip를 인위적으로 늘리지 않음. 동일 suite count라면 expected projection은 1200 PASS / 3 SKIP.`

- channel: `WORKSPACE_INTEGRITY`
  scope: `before/after HEAD, tracked worktree, untracked, changed-path inventory, diff check`
  allowed_command_or_environment: `local Git read-only status/diff commands`
  pass_condition: `task-related test changes만 존재하고 unrelated dirt를 수정하지 않음`

reuse_allowed:
- channel: `PREDECESSOR_CLASSIFICATION`
  predecessor: `20260915_2126 L1 terminal acceptance`
  provenance_condition: `accepted predecessor Cycle/Judgment/Handoff exact files`
  applicability_condition: `세 failure가 작업 시작 시 동일 test node와 동일 shared error로 재현/확인될 때만 PREEXISTING_NOT_L1_CAUSED classification을 유지`

human_owned:
- channel: `COMMAND_CENTER_ACCEPTANCE`
  scope: `repair candidate의 최종 acceptance, persistence/commit 여부, L2 진입 승인`
  expected_result_format: `Browser Command Center judgment`

not_required:
- channel: `BROWSER_RUNTIME`
  reason: `test baseline repair이며 browser QA가 acceptance proof가 아님`
- channel: `PUBLIC_LIVE_PROVIDER`
  reason: `L4/L6/L7 범위이며 이 Task에서 paid provider action 금지`
- channel: `DEPLOYMENT`
  reason: `L5 이후 별도 release/deployment 범위`
- channel: `DATABASE_MIGRATION`
  reason: `schema/migration 변경 금지`

forbidden:
- action_or_channel: `guard weakening / skip / xfail / assertion dilution`
  reason: `proof type과 current authority를 fixture에 맞춰 낮추는 것은 repair가 아님`
- action_or_channel: `Git commit/push/deployment/provider paid call`
  reason: `별도 authorization 필요`

proof_non_substitution:
- `targeted 3 PASS != full-suite green`
- `full-suite green != Browser/Human acceptance`
- `fixture changed != guard correctness unless production diff confirms guard unchanged`
- `predecessor classification != current reproduction unless exact applicability confirmed`

## conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant:
  - `G_EXECUTOR_SUBMISSION requires an issuer-verified execution ref`
  - `Agent claim != admitted evidence`
  - `accepted predecessor proof != current changed-path proof`
- required_actual_owner:
  - authority guard: current System/canonical runtime owner
  - fixture construction: test code
- planned_vs_actual_scope:
  - expected test-only
- rollback_or_failure_semantics:
  - test repair이 production mutation을 요구하면 변경하지 말고 STOP
  - exact three가 current shared error가 아니면 predecessor applicability를 재분류하고 STOP
  - full suite에 새로운 unrelated failure가 나타나면 숨기거나 확대 수정하지 말고 exact failure inventory와 함께 candidate를 `HOLD_REWORK_REQUIRED`로 제출

## project context impact

architecture:
- `NONE`

orchestration_contract:
- `NONE`

security_sandbox:
- `NONE`

public_provenance:
- `TASK_AND_CYCLE_ONLY`

## accept 기준

모두 충족해야 한다.

- expected HEAD `3709c88fc0abd2f4219228ced931a9164f286dc4`에서 시작했거나, 다른 HEAD라면 substantive mutation 전에 STOP하고 보고
- 세 known failing tests가 current issuer-verified execution ref contract를 만족하도록 test fixture가 정렬됨
- `G_EXECUTOR_SUBMISSION` production guard/authority source 변경 없음
- skip/xfail/delete/assertion weakening 없음
- exact three targeted tests `PASS`
- full suite `0 FAIL / 0 ERROR`
- predecessor의 legitimate skip를 repair 수단으로 증가시키지 않음
- product/runtime source change 없음
- unrelated dirty source 수정 없음
- report/export 완성

## hold/reject 기준

- `G_EXECUTOR_SUBMISSION` guard를 완화해야만 tests가 통과함
- issuer verification을 우회하는 fake/stale ref를 도입함
- skip/xfail/assertion dilution이 포함됨
- product/runtime source change가 필요함
- exact three의 failure identity가 predecessor와 달라 attribution이 불명확함
- full suite에 1개 이상 FAIL/ERROR가 남음
- unrelated dirty workspace와 current repair diff가 충돌하여 attribution 불가

## mandatory stop 조건

- expected HEAD mismatch
- policy baseline conflict
- missing required predecessor artifact
- exact three failure identity mismatch
- allowed test path 외 product/runtime mutation 필요
- dirty workspace collision with target tests/shared fixture
- forbidden action/tool request
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`
- human decision required before further mutation

named blocker 이후에는 blocker를 입증하는 최소 evidence, workspace inventory, report/export와 안전한 종료만 수행한다.

## 보고서 필수 항목

- 작업명 / work type / task path
- starting branch/HEAD
- read canonical paths
- exact three reproduction/result
- `G_EXECUTOR_SUBMISSION` current guard source owner와 unchanged 여부
- stale fixture가 무엇이었는지
- reused current issuer-verified ref construction path
- source inventory
- product source changes
- governance/provenance changes
- repository configuration changes
- test changes
- before/after workspace
- evidence contract와 실제 result classification
- full-suite actual counts
- skipped test actual count/list 변화 여부
- Agent claim vs admitted evidence
- forbidden-not-run
- mandatory stop/scope expansion
- planned-vs-actual conformance
- unverified items
- rollback/revert guide
- preserved artifact exact paths
- next turn recommendation

## export bundle 요구

Target:
`.aiassistant/reports/target/20260915_2225_aiscc-command-center-issuer-verified-executor-submission-baseline-regression-repair-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- changed test files preserving project-relative paths
- `REMOVED_FILES.md` only when deletion exists

Task lifecycle:
- executor-required work/report/export 완료 후
- `.aiassistant/tasks/active/20260915_2225_aiscc-command-center-issuer-verified-executor-submission-baseline-regression-repair-1.md`
- → `.aiassistant/tasks/done/20260915_2225_aiscc-command-center-issuer-verified-executor-submission-baseline-regression-repair-1.md`

## 사람 검증 요구

- 이번 Executor Task 자체에는 별도 browser/manual QA가 필요하지 않다.
- Browser Command Center가 target bundle을 판정한 뒤:
  - baseline repair acceptance
  - Git persistence/commit authorization
  - L2 진입 여부
  를 별도 결정한다.

## 최종 응답 형식

1. result: completed / blocked / rejected-candidate
2. target bundle path
3. changed files
4. removed files
5. exact three result
6. full-suite result
7. guard unchanged result
8. human verification
9. unverified items
10. preserved exact paths
