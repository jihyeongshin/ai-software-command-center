# 작업지시서: Command Center baseline regression repair — PostgreSQL runtime authorized retry

## meta

- task_id: `20260915_2230_aiscc-command-center-baseline-regression-repair-postgresql-runtime-authorized-retry-1`
- created_at: `2026-09-15T22:30:00+09:00`
- work_type: `REWORK`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `3709c88fc0abd2f4219228ced931a9164f286dc4`
- primary_semantic_owner: `Command Center integration test baseline / current G_EXECUTOR_SUBMISSION authority contract`
- predecessor_blocked_task: `20260915_2225_aiscc-command-center-issuer-verified-executor-submission-baseline-regression-repair-1`
- predecessor_blocker: `EVIDENCE_SCOPE_EXPANSION_REQUIRED`
- ide_executor_session: `FRESH_CHAT_REQUIRED`

## 현재 상태

- branch: `main`
- expected HEAD before work: `3709c88fc0abd2f4219228ced931a9164f286dc4`
- predecessor L1 result: `P3-3 PUBLIC LIVE L1 IMPLEMENTED / ACCEPTED / CLOSED`
- Public Live: `NOT_RELEASED`
- Public admission: `DISABLED`
- L2: `NOT_STARTED / ENTRY_ELIGIBLE`
- broader baseline debt:
  - `1197 PASS`
  - `3 FAIL`
  - `3 SKIP`
  - `0 ERROR`
- exact shared failure:
  - `ValueError: G_EXECUTOR_SUBMISSION requires an issuer-verified execution ref`
- accepted historical attribution:
  - `PREEXISTING_NOT_L1_CAUSED`
  - `DEFERRED_SEPARATE_TASK`

Previous retry result:

```text
BLOCKED / EVIDENCE_SCOPE_EXPANSION_REQUIRED
HEAD unchanged
test/product source changes: none
```

The previous Task incorrectly required reuse of an existing predecessor PostgreSQL environment while also forbidding recreation. The predecessor task had correctly cleaned up its task-owned PostgreSQL container/volume, so absence of that runtime is expected and MUST NOT be treated as a product blocker.

Exact known failures:

1. `tests/integration/command_center/test_postgres_read_api.py::test_postgres_read_models_http_runtime_and_no_mutation`
2. `tests/integration/command_center/test_postgres_read_api.py::test_postgres_conflict_and_http_503_fail_closed`
3. `tests/integration/command_center/test_web_ui.py::test_default_entrypoint_ui_queue_etag_and_event_no_mutation`

## 이번 턴 목표

1. task-owned isolated PostgreSQL 17.6 test runtime을 로컬에서 재생성한다.
2. exact three failures를 **수정 전 먼저 재현**하여 predecessor failure identity/applicability를 확인한다.
3. stronger current `G_EXECUTOR_SUBMISSION` issuer-verification guard는 그대로 유지하고 stale Command Center test fixture만 current contract에 정렬한다.
4. exact three targeted tests를 PASS시킨다.
5. 같은 task-owned PostgreSQL runtime에서 broader full suite를 실행하여 green baseline을 복구한다.
6. L2 구현 전 clean regression baseline을 확립한다.

## 이번 턴 비목표

- Public Live L2 구현
- Public Live L4 provider profile 작업
- Public Live L5 Railway ingress/sandbox/deployment proof
- `G_EXECUTOR_SUBMISSION` guard/authority 완화
- production/application/runtime source 변경
- 새로운 WorkflowState/Evidence/Judgment 정책 설계
- external PostgreSQL 사용
- private/pre-existing PostgreSQL container 재사용
- network image pull
- dependency 설치
- provider paid call
- deployment
- Git commit/push
- unrelated failing test 정리

## 허용 범위

allowed_paths:
- `tests/integration/command_center/test_postgres_read_api.py`
- `tests/integration/command_center/test_web_ui.py`
- 위 exact tests가 직접 사용하는 기존 shared test fixture/helper가 별도 test 파일에 있을 경우 최소 범위로 추가 가능
- `.aiassistant/tasks/active/**`
- `.aiassistant/tasks/done/**`
- `.aiassistant/reports/target/**`

production/application/runtime source:
- read-only inspection only
- modification forbidden

allowed_actions:
- expected HEAD / workspace 확인
- Task-listed canonical source 읽기
- current `G_EXECUTOR_SUBMISSION` implementation과 issuer-verification construction path 좁게 조사
- local Docker image inventory read
- cached `postgres:17.6` image 사용
- task-owned PostgreSQL 17.6 container/ephemeral volume 생성·기동·health 확인
- loopback `127.0.0.1:55432`만 host bind
- task-local test database/user/password 사용
- `AISCC_TEST_DATABASE_URL`을 task-owned local DB로 설정
- `LOCAL_POSTGRES_RUNTIME.json` 생성
- exact three tests 수정 전 reproduction
- 허용 test fixture 수정
- exact three targeted integration tests 재실행
- same isolated PostgreSQL runtime을 사용한 repository full suite 실행
- `git diff --check`
- report/export
- 종료 시 task-owned container/volume best-effort cleanup
- executor-required work/report/export 완료 후 Task를 `tasks/done`으로 이동

## PostgreSQL runtime prerequisite — EXPLICITLY AUTHORIZED

이 section은 previous Task의 환경 금지를 명시적으로 supersede한다.

### required runtime shape

```text
engine:
PostgreSQL 17.6

image:
postgres:17.6

image acquisition:
LOCAL CACHE ONLY

network image pull:
FORBIDDEN

container ownership:
CURRENT TASK ONLY

host bind:
127.0.0.1:55432

container port:
5432

database purpose:
AISCC isolated integration-test runtime only

external/private DB reuse:
FORBIDDEN
```

### preflight

1. `docker image inspect postgres:17.6` 또는 동등한 read-only 확인으로 cached image 존재 여부를 확인한다.
2. cached image가 없으면 pull하지 말고 `BLOCKED_MISSING_ARTIFACT` 또는 명확한 runtime prerequisite blocker로 STOP한다.
3. `127.0.0.1:55432`가 unrelated process/container에 의해 사용 중이면 그 owner를 변경/종료하지 말고 collision으로 STOP한다.
4. existing `aiscc-p2-3-private-postgres-v1` 또는 다른 prior/private PostgreSQL runtime을 시작·재사용·reset·credential-inspect하지 않는다.

### task-owned creation

- container name은 task-specific name을 사용한다. 권장:
  - `aiscc-command-center-baseline-repair-postgres-17-6`
- storage는 task-owned ephemeral volume만 사용한다.
- test credential은 task-local synthetic value만 사용한다.
- host exposure는 `127.0.0.1:55432` 외 금지한다.
- public/external network endpoint를 사용하지 않는다.
- repository에서 이미 accepted된 local PostgreSQL test bootstrap convention이 있으면 그 shape를 재사용하되 private credential/source를 읽지 않는다.

### runtime evidence

테스트 전에 target bundle 아래에 `LOCAL_POSTGRES_RUNTIME.json`을 생성하고 최소 다음을 기록한다.

```text
postgres_version
image_tag
image_id_or_digest_when_available
image_source = local-cache
network_pull = false
container_name
container_id
host_bind = 127.0.0.1
host_port = 55432
container_port = 5432
health_status
database_url_present = true
database_url_value = REDACTED
private_db_reused = false
ready_for_tests = true|false
```

PASS 조건:

```text
postgres_version == 17.6
network_pull == false
host_bind == 127.0.0.1
host_port == 55432
private_db_reused == false
health_status == healthy/ready
ready_for_tests == true
```

raw password/credential/database URL 전체값을 report/export에 기록하지 않는다.

### lifecycle / cleanup

- exact-three reproduction → fixture repair → targeted rerun → full suite가 끝날 때까지 같은 task-owned runtime을 유지한다.
- source/result evidence를 먼저 기록한다.
- 이후 current task가 생성한 container/ephemeral volume만 best-effort cleanup한다.
- unrelated container/volume/image는 삭제하지 않는다.
- cleanup 실패는 **substantive test result를 무효화하지 않는다**.
- cleanup 실패 시 `NON_BLOCKING_LOCAL_RESIDUE`로 exact task-owned resource name만 보고한다.
- cached `postgres:17.6` image 자체는 삭제하지 않는다.

## 절대 금지

forbidden_paths:
- production/application/runtime source modification
- canonical governance baseline modification
- migration/schema source modification
- deployment/resource configuration
- provider credential/budget configuration
- unrelated tests

forbidden_actions:
- `G_EXECUTOR_SUBMISSION` issuer-verification 조건 삭제/완화/bypass
- stale/unsigned/unverified execution ref를 current authority처럼 허용
- failing tests skip/xfail/delete
- assertion weakening
- reproduction 없이 바로 fixture mutation
- predecessor debt를 L1 regression으로 재분류 without new evidence
- unrelated failure를 함께 수정
- cached image가 없을 때 docker pull
- external/private PostgreSQL 사용
- `aiscc-p2-3-private-postgres-v1` 등 unrelated DB start/reset/reuse/credential inspection
- host bind `0.0.0.0`
- external network service provisioning
- dependency/toolchain install
- provider call
- deployment
- Git index/commit/push
- root `.gitignore` 변경
- unrelated dirty file cleanup/reset

## 읽을 문서

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- `.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md`
- `.aiassistant/records/aiscc/cycles/20260915_2126_aiscc-p3-3-public-live-l1-terminal-acceptance-l2-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2126_aiscc-p3-3-public-live-l1-terminal-browser-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260915_2126_aiscc-browser-command-center-p3-3-public-live-l1-complete-nextaction-selection-handoff-1.md`
- `.aiassistant/tasks/done/20260915_2225_aiscc-command-center-issuer-verified-executor-submission-baseline-regression-repair-1.md`
- `.aiassistant/records/aiscc/cycles/20260915_2230_aiscc-command-center-baseline-repair-blocked-environment-contract-rework-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_2230_aiscc-browser-command-center-baseline-repair-blocked-environment-contract-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_2230_aiscc-browser-command-center-baseline-repair-postgresql-runtime-authorized-retry-handoff-1.md`

## agent instruction transport / authority

- repository-root instruction entrypoint는 thin transport bootstrap이며 policy authority가 아니다.
- 위 exact list는 minimum authoritative context set이다.
- unrelated rules/records/source/logs를 bulk-read하지 않는다.
- current `G_EXECUTOR_SUBMISSION`의 canonical owner가 좁은 source inspection 중 추가로 확인되면 그 exact owner path만 읽고 report한다.
- current source와 canonical authority가 충돌하면 mutation을 중단하고 `POLICY_CONFLICT_INVESTIGATION_REQUIRED`.
- previous Task의 `new DB/runtime provisioning forbidden` 문구는 이 retry에 적용하지 않는다.
- 이 Task의 PostgreSQL runtime section이 current retry의 exact environment authority다.

## 조사할 source

반드시 좁게 확인:

1. exact error:
   - `G_EXECUTOR_SUBMISSION requires an issuer-verified execution ref`
2. `G_EXECUTOR_SUBMISSION` guard/evaluation code path
3. `issue_from_execution_ref` 또는 current equivalent verified construction path
4. `ExecutionReferenceAuthority` / producer verifier current path
5. stale `_GuardAuthority.issue` shared fixture path
6. nearby green workflow integration test의 issuer-verified execution submission construction example
7. exact three tests가 공유하는 `_seed` / helper lineage

Current blocked predecessor already identified this likely direction, but it is **Agent finding**, not accepted repair proof. Reproduce first.

## 구현 범위

Expected repair:
- stale Command Center shared fixture/factory가 `G_EXECUTOR_SUBMISSION`에 generic `issue`를 쓰지 않고 current issuer-verified execution ref construction/admission path를 사용하도록 test-only 정렬.

Expected product source changes:
- none

Expected migration changes:
- none

Expected runtime/config source changes:
- none

If production/runtime source mutation becomes necessary:
- DO NOT mutate.
- STOP and report `POLICY_CONFLICT_INVESTIGATION_REQUIRED` or required scope expansion.

## workflow transition expectation

- initial_state: `L1 CLOSED / baseline debt open / L2 ENTRY_ELIGIBLE`
- expected_terminal_candidate: `BASELINE_GREEN_RESTORED / L2 still NOT_STARTED`
- Agent가 P3-3/Public Live release 또는 L2 start를 직접 결정할 수 있는가: `No`

## evidence contract

executor_required:

- channel: `DATABASE_RUNTIME`
  scope: `task-owned isolated PostgreSQL 17.6 recreation`
  pass_condition:
    - cached `postgres:17.6`
    - no image pull
    - `127.0.0.1:55432`
    - task-owned container/volume only
    - `LOCAL_POSTGRES_RUNTIME.json` PASS
    - no private DB reuse

- channel: `INTEGRATION_TEST_REPRODUCTION`
  scope: `exact three known failing nodes before any test source mutation`
  pass_condition: `all three reproduce the accepted shared issuer-verification failure, or exact actual divergence is reported and mutation stops`

- channel: `STATIC_SOURCE`
  scope: `guard unchanged + fixture repair path`
  pass_condition: `production/runtime tracked diff empty; no guard weakening`

- channel: `INTEGRATION_TEST_TARGETED`
  scope: `exact three nodes after repair`
  pass_condition: `3 PASS / 0 FAIL / 0 ERROR`

- channel: `FULL_SUITE`
  scope: `repository broader test suite using same task-owned PostgreSQL runtime`
  pass_condition: `0 FAIL / 0 ERROR; legitimate skips not increased as repair mechanism`

- channel: `WORKSPACE_INTEGRITY`
  scope: `before/after HEAD, tracked diff, untracked, changed-path inventory`
  pass_condition: `test-only source changes + Task/report temporary artifacts; unrelated dirt unchanged`

reuse_allowed:

- channel: `PREDECESSOR_L1_ACCEPTANCE`
  predecessor: `20260915_2126 L1 terminal acceptance`
  applicability_condition: `L1 source/commit remains unchanged`

- channel: `PREDECESSOR_BLOCKED_INVESTIGATION`
  predecessor: `20260915_2225 blocked executor report`
  allowed_use: `source navigation hypothesis only`
  not_allowed_as: `current reproduction or repair proof`

human_owned:
- channel: `COMMAND_CENTER_ACCEPTANCE`
  scope: `repair acceptance, Git persistence, L2 entry`
  expected_result_format: `Browser Command Center judgment`

not_required:
- `BROWSER_RUNTIME`
- `PUBLIC_LIVE_PROVIDER`
- `DEPLOYMENT`
- `DATABASE_MIGRATION`

forbidden:
- guard weakening
- proof substitution
- private DB reuse
- network pull
- Git persistence actions

proof_non_substitution:
- `historical 3 FAIL != fresh reproduction`
- `fresh reproduction != repaired PASS`
- `3 targeted PASS != full-suite green`
- `full-suite green != Human/Command Center acceptance`
- `task-owned local PostgreSQL != production/deployment proof`
- `fixture update != guard correctness unless guard diff remains unchanged`

## accept 기준

모두 충족:

- start HEAD exact match `3709c88fc0abd2f4219228ced931a9164f286dc4`
- isolated PostgreSQL 17.6 runtime recreation PASS
- no network pull
- no private/pre-existing DB reuse
- `LOCAL_POSTGRES_RUNTIME.json` PASS
- exact three pre-mutation reproduction confirms same shared failure
- fixture/test-only repair
- `G_EXECUTOR_SUBMISSION` production guard unchanged
- no skip/xfail/assertion dilution
- exact three post-repair `3 PASS`
- broader full suite `0 FAIL / 0 ERROR`
- legitimate skips not increased to hide failures
- product/runtime/migration/config source changes none
- unrelated dirty source unchanged
- report/export complete

## hold/reject 기준

- cached `postgres:17.6` unavailable
- port 55432 collision with unrelated owner
- reproduction differs materially from accepted three-failure identity
- production/runtime mutation required
- guard weakening/bypass required
- private DB reuse required
- exact three remain failing
- full suite has any FAIL/ERROR
- unrelated dirty workspace collision prevents attribution

## mandatory stop 조건

- expected HEAD mismatch
- cached image missing
- loopback port collision
- missing required predecessor artifact
- policy conflict
- exact-three reproduction identity mismatch
- product/runtime mutation required
- dirty workspace collision
- forbidden action request
- human decision required before further mutation

named blocker 이후에는 최소 evidence, workspace inventory, report/export, safe cleanup만 수행한다.

## 보고서 필수 항목

- task/work type/path
- starting branch/HEAD
- PostgreSQL recreation evidence
- image cache / no-pull evidence
- container/volume ownership
- `LOCAL_POSTGRES_RUNTIME.json`
- exact three pre-mutation reproduction
- stale fixture root cause
- current issuer-verified construction path
- changed test files
- guard unchanged evidence
- exact three post-repair result
- full-suite counts
- skip count/list comparison
- product/governance/config changes
- workspace before/after
- evidence classification
- forbidden-not-run
- cleanup result and any non-blocking task-owned residue
- unverified items
- rollback
- preserved exact paths
- next-turn recommendation

## export bundle 요구

Target:
`.aiassistant/reports/target/20260915_2230_aiscc-command-center-baseline-regression-repair-postgresql-runtime-authorized-retry-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `LOCAL_POSTGRES_RUNTIME.json`
- changed test files preserving project-relative paths
- `REMOVED_FILES.md` only when product/test deletion exists

Task lifecycle:
- active:
  `.aiassistant/tasks/active/20260915_2230_aiscc-command-center-baseline-regression-repair-postgresql-runtime-authorized-retry-1.md`
- done after executor-required work/report/export:
  `.aiassistant/tasks/done/20260915_2230_aiscc-command-center-baseline-regression-repair-postgresql-runtime-authorized-retry-1.md`

## 사람 검증 요구

별도 browser/visual QA는 필요하지 않다.

Browser Command Center가 결과 bundle 제출 후:
1. baseline repair acceptance
2. Git persistence authorization
3. L2 entry authorization
을 판정한다.

## 최종 응답 형식

1. result
2. target bundle path
3. PostgreSQL runtime result
4. pre-mutation reproduction result
5. changed files
6. exact-three post-repair result
7. full-suite result
8. guard unchanged result
9. cleanup/residue
10. human verification
11. unverified items
12. preserved exact paths
