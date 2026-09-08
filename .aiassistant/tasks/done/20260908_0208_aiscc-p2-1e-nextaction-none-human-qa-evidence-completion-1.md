# 작업지시서: P2-1E NextAction NONE Human-QA evidence completion

## meta

- task_id: `20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1`
- created_at: `2026-09-08T02:08:00+09:00`
- work_type: `QA_ONLY / EVIDENCE_GAP_CLOSURE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `P2-1E NextAction NONE/empty truthful-state Human Browser evidence preparation`

## 현재 상태

- current canonical baseline:
  - P2-1D: `HUMAN_PROVIDED / ACCEPTED / PERSISTED`
  - P2-1E source/runtime: `ACCEPTED_CANDIDATE`
  - P2-1E Human QA: `HUMAN_PROVIDED / PARTIAL_ACCEPTED`
- predecessor cycle:
  - `.aiassistant/records/aiscc/cycles/20260908_0158_aiscc-p2-1e-human-browser-qa-partial-accepted-nextaction-none-fixture-gap-1.cycle.md`
- predecessor handoff:
  - `.aiassistant/reports/aiscc/20260908_0158_aiscc-browser-command-center-p2-1e-human-qa-partial-evidence-completion-entry-handoff-1.md`
- accepted Human correction:
  - `Operation 17 visible polling resume: PASS`
- remaining open Human evidence:
  - `Operation 8 NextAction empty/NONE truthful state: BLOCKED_FIXTURE_GAP`
- known dirty workspace:
  - P2-1E accepted candidate lineage의 existing working-tree mutation을 보존한다.
  - 이 Task는 기존 dirt를 normalize하거나 정리하지 않는다.
- open blocker:
  - safe deterministic NONE/empty NextAction fixture의 가용성 미확인

## 이번 턴 목표

1. repository가 이미 제공하는 deterministic fixture/setup authority 안에서 `NextAction = NONE/empty`를 진실하게 만들 수 있는 supported path가 있는지 확인한다.
2. supported path가 있으면 product source를 수정하지 않고 narrow local PostgreSQL/AISCC QA runtime을 준비한다.
3. Human이 Operation 8만 재실행할 수 있도록 exact runtime identity와 Project URL/ID를 보고한다.
4. supported path가 없으면 arbitrary SQL/ad-hoc authority mutation 없이 `EVIDENCE_SCOPE_EXPANSION_REQUIRED`로 중단한다.

## 이번 턴 비목표

- P2-1E product behavior rework
- Operations 1-7, 9-22 전체 Browser QA 재실행
- 이미 Human `PASS`로 정정된 Operation 17 재검증
- P2-1E persistence/commit
- P2-1 closure
- P2-2 start
- public deployment/release
- 새로운 general-purpose fixture framework 설계/구현
- production/domain authority 변경

## 허용 범위

allowed_paths:
- existing repository-provided fixture/setup/runtime source의 read-only inspection
- existing QA/runtime scripts/configuration의 read-only inspection
- Task-owned ignored temporary runtime artifacts
- `.aiassistant/tasks/active/20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1.md`
- `.aiassistant/tasks/done/20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1.md`
- `.aiassistant/reports/target/20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1/**`

allowed_actions:
- exact Task-listed canonical source read
- existing deterministic fixture/setup path discovery
- existing supported fixture/setup invocation
- local-only PostgreSQL 17.6 disposable QA runtime preparation
- existing Alembic migration path 실행
- repository `.venv` 사용
- normal AISCC local entrypoint 실행
- loopback-only HTTP runtime
- Task-owned disposable DB/container cleanup
- exact runtime identity 수집
- narrow source/static inspection required to establish fixture provenance
- `git status` / `git diff --check` 등 non-mutating workspace inspection

## 절대 금지

forbidden_paths:
- unrelated product/runtime source mutation
- unrelated tests/configuration/governance mutation
- production/private repository/data

forbidden_actions:
- arbitrary SQL로 Project/NextAction authoritative rows 제조 또는 수정
- ad-hoc DB authority mutation
- production/domain authority mutation
- new migration
- new dependency
- Docker image pull
- external provider/network
- remote DB
- deployment/public release
- P2-2 start
- broad Browser QA replay
- Git index / commit / push
- `git reset`
- `git restore`
- `git checkout`
- `git stash`
- `git clean`
- unrelated dirty-file cleanup
- Human Browser proof를 Executor proof로 대체

## 읽을 문서

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md`
- `.aiassistant/tasks/done/20260907_2328_aiscc-p2-1e-authorized-postgresql-runtime-implementation-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0020_aiscc-p2-1e-implementation-runtime-candidate-accepted-human-qa-pending-1.cycle.md`
- `.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0158_aiscc-p2-1e-human-browser-qa-partial-accepted-nextaction-none-fixture-gap-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_0158_aiscc-browser-command-center-p2-1e-human-qa-partial-evidence-completion-entry-handoff-1.md`

## agent instruction transport / authority

- repository-root instruction entrypoint는 thin transport bootstrap이며 project policy authority가 아니다.
- Project Rules UI 또는 automatic retrieval만으로 canonical body가 Agent에 전달됐다고 가정하지 않는다.
- 위 목록은 minimum authoritative context set이다.
- unrelated rules/records/source/logs를 bulk-read하지 않는다.
- active Task File, canonical rule, current source, accepted evidence가 충돌하면 구현/fixture mutation을 중단하고 conflict investigation으로 보고한다.
- Human-owned Browser evidence를 executor-completed로 주장하지 않는다.
- 이번 Human correction은 exact `Operation 17: PASS`로 취급한다. `PAS`는 더 이상 open gap이 아니다.

## 조사할 source

FIRST:
- repository에서 P2-1E QA용 deterministic fixture/setup authority를 식별한다.
- `NextAction NONE/empty`가 자연스럽고 지원되는 상태로 생성되는 기존 path가 있는지 확인한다.
- fixture가 만드는 Project/Task/Cycle/NextAction 의미가 실제 product authority와 정합하는지 확인한다.

검색 우선순위:
1. existing test/QA fixture factories
2. seed/setup commands or scripts
3. repository-owned deterministic scenario builders
4. existing runtime bootstrap helpers

임의 SQL row fabrication은 조사 결과의 대안이 아니다.

## 구현/문서/감사 범위

### Branch A — existing supported fixture 있음

- product source 수정: `NONE`
- existing fixture/setup path만 사용
- local PostgreSQL/AISCC runtime 준비
- 다음 exact identity를 보고:
  - server URL + actual port
  - project_id
  - cycle_id if applicable
  - primary_work_run_id
  - terminal_work_run_id
- Human Operation 8 재실행용 exact Project URL 제공
- Operation 8에 기대되는 truthful NONE/empty state가 왜 fixture 의미상 정상인지 source provenance를 짧게 보고
- Human Browser 검증 직전 stop

### Branch B — existing supported fixture 없음

- product source 수정: `NONE`
- arbitrary DB authority mutation: `FORBIDDEN_NOT_RUN`
- 새 fixture 구현: `FORBIDDEN_NOT_RUN`
- result:
  - `EVIDENCE_SCOPE_EXPANSION_REQUIRED`
- separately authorized narrow fixture-provisioning Task가 필요하다고 보고
- Human Browser QA를 실행 가능한 것으로 가장하지 않는다.

## runtime boundary

기존 accepted local-only pattern을 유지한다.

```text
PostgreSQL 17.6
postgres:17.6-alpine
--pull=never
loopback only
Task-owned disposable DB
tmpfs DB storage
existing Alembic migration path
repository .venv
normal AISCC entrypoint
```

Docker image가 local에 없으면 pull하지 말고 blocker로 보고한다.

## workflow transition expectation

- initial_state: `P2-1E HUMAN_QA PARTIAL_ACCEPTED`
- expected_non_terminal_state_when_human_pending: `P2-1E HUMAN_QA EVIDENCE GAP CLOSURE / HUMAN_PENDING`
- expected_terminal_candidate: `NOT_APPLICABLE_IN_EXECUTOR_TURN`
- transition_authority: `NOT_APPLICABLE`
- Agent가 직접 P2-1E terminal acceptance를 결정할 수 있는가: `No`

## evidence contract

executor_required:
- channel: `STATIC_SOURCE`
  scope: existing deterministic fixture/setup authority discovery
  allowed_command_or_environment: read-only repository inspection
  pass_condition: supported NONE/empty NextAction path가 존재하는지 provenance와 함께 확정
- channel: `DATABASE_RUNTIME`
  scope: Branch A일 때만 existing supported fixture/setup으로 local PostgreSQL runtime 준비
  allowed_command_or_environment: accepted local PostgreSQL 17.6 pattern
  pass_condition: fixture-created Project/runtime identity가 exact하게 기록되고 authoritative state가 정상 조회됨
- channel: `HTTP_RUNTIME`
  scope: Branch A일 때만 Human Operation 8 진입에 필요한 Project page/API가 loopback에서 접근 가능
  allowed_command_or_environment: normal AISCC local entrypoint
  pass_condition: exact server/Project URL과 required identifiers 보고

reuse_allowed:
- channel: `STATIC_SOURCE / UNIT_TEST / INTEGRATION_TEST / DATABASE_RUNTIME / HTTP_RUNTIME / FRONTEND_SOURCE_TEST`
  predecessor: `20260908_0020_aiscc-p2-1e-implementation-runtime-candidate-accepted-human-qa-pending-1.cycle.md`
  provenance_condition: P2-1E product source identity unchanged
  applicability_condition: evidence-completion Task가 해당 behavior를 수정하지 않음
- channel: `BROWSER_RUNTIME / VISUAL / USABILITY / RESPONSIVE`
  predecessor: `20260908_0158_aiscc-p2-1e-human-browser-qa-partial-accepted-nextaction-none-fixture-gap-1.cycle.md`
  provenance_condition: Human reported accepted operations remain unchanged
  applicability_condition: this Task does not mutate covered behavior

human_owned:
- channel: `BROWSER_RUNTIME`
  scope: `Operation 8 NextAction empty/NONE truthful state` only
  expected_result_format:
    - `Operation 8: PASS`
    - or `Operation 8: FAIL` with actual visible wording/behavior
- channel: `HUMAN_VERIFICATION`
  scope: Browser observation ownership
  expected_result_format: exact Human result only

not_required:
- channel: `BROWSER_RUNTIME`
  reason: Operations 1-7, 9-22 are not rerun when source identity/covered behavior remain unchanged
- channel: `PUBLIC_PROVENANCE`
  reason: persistence/release is outside this Task
- channel: `SECURITY_SANDBOX`
  reason: no security boundary change is authorized

forbidden:
- action_or_channel: arbitrary DB authority mutation
  reason: prior QA guide explicitly prohibits manufacturing NONE/empty state through ad-hoc mutation
- action_or_channel: Human proof substitution
  reason: Executor runtime/source proof cannot establish Operation 8 Browser acceptance
- action_or_channel: product source mutation
  reason: no source defect has been established
- action_or_channel: Git persistence/deployment
  reason: separately authorized terminal persistence Task is required

proof_non_substitution:
- `STATIC_SOURCE != HUMAN_BROWSER_PROOF`
- `DATABASE_RUNTIME != HUMAN_BROWSER_PROOF`
- `HTTP_RUNTIME != HUMAN_BROWSER_PROOF`
- `Executor observation != Human Operation 8 result`
- `Operation 17 PASS != Operation 8 PASS`

## conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant:
  - proof type non-substitution
  - Human-owned evidence ownership
  - no ad-hoc authority mutation
  - current accepted candidate lineage preservation
- required_actual_owner:
  - fixture/runtime preparation: Executor
  - Operation 8 Browser judgment: Human
- planned_vs_actual_scope:
  - Branch A 또는 Branch B 중 실제 branch를 명시
- rollback_or_failure_semantics:
  - Task-owned disposable runtime만 정리
  - product source/authority는 수정하지 않음

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

Executor turn `completed` 조건:

```text
existing supported deterministic fixture/setup path = FOUND
AND product source changes = none
AND arbitrary DB authority mutation = absent
AND narrow local runtime = prepared
AND exact continuation runtime identity = recorded
AND exact Project URL/ID for Human Operation 8 = provided
AND Human Browser proof remains HUMAN_PENDING
```

Executor turn `blocked` 조건:

```text
existing supported deterministic fixture/setup path = NOT_FOUND
AND no prohibited fixture fabrication/mutation performed
AND result = EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

두 경우 모두 P2-1E terminal acceptance를 주장하지 않는다.

## hold/reject 기준

- product/source behavior defect가 실제로 발견됨
- existing fixture path가 truthfully NONE/empty를 만들지 않는데 강제로 사용함
- arbitrary SQL/ad-hoc authority mutation 실행
- unrelated source mutation
- Human proof false-claim
- forbidden Git/deployment action
- current candidate lineage/source identity를 불명확하게 변경

## mandatory stop 조건

- policy baseline conflict
- missing required canonical artifact
- dirty workspace collision affecting this Task
- forbidden action/tool request
- security boundary uncertainty
- existing fixture 없음 → `EVIDENCE_SCOPE_EXPANSION_REQUIRED`
- source defect 발견 → `HOLD_REWORK_REQUIRED`
- Human decision required before further mutation

named blocker 이후에는 최소 source evidence, workspace inventory, report/export와 안전한 종료만 수행한다.

## 보고서 필수 항목

- 작업명 / work type / task path
- read canonical paths
- source inventory
- fixture/setup authority discovery result
- selected Branch A / Branch B
- product source changes: expected `none`
- governance/provenance changes
- repository configuration changes
- workspace before/after
- exact runtime identity when Branch A
- exact Human Operation 8 URL/project_id when Branch A
- Task evidence contract와 실제 result classification
- reused predecessor evidence applicability
- `Operation 17: HUMAN_PROVIDED / PASS` correction recorded
- Human Operation 8: `HUMAN_PENDING`
- arbitrary DB authority mutation: `FORBIDDEN_NOT_RUN`
- Git persistence/deployment: `FORBIDDEN_NOT_RUN`
- mandatory stop/scope expansion
- unverified items
- rollback/runtime cleanup guide
- preserved artifact exact paths
- next turn recommendation

## export bundle 요구

Target:
`.aiassistant/reports/target/20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- changed files preserving project-relative paths
- `REMOVED_FILES.md` only when deletion exists

Expected product changed files:
- none

## 사람 검증 요구

Branch A에서 Executor가 runtime 준비를 완료한 뒤 Human은 **Operation 8만** 실행한다.

Human 제출 형식:

```text
P2-1E Operation 8 continuation QA

server:
<actual URL including port>

project_id:
<actual>

cycle_id:
<actual or N/A if fixture truthfully has none>

primary_work_run_id:
<actual or N/A if not applicable>

terminal_work_run_id:
<actual or N/A if not applicable>

Operation 8 NextAction empty/NONE truthful state:
PASS
```

실제 defect가 보이면:

```text
Operation 8 NextAction empty/NONE truthful state:
FAIL

actual:
<visible wording / behavior>
```

Operation 17은 이미 Human correction으로 다음과 같이 정규화되었다.

```text
Operation 17 visible polling resume:
PASS
```

따라서 Operation 17 재실행은 요구하지 않는다.

## 최종 응답 형식

1. result: `completed` / `blocked` / `rejected-candidate`
2. selected branch: `A_EXISTING_FIXTURE` / `B_SCOPE_EXPANSION_REQUIRED`
3. target bundle path
4. changed files
5. removed files
6. fixture/setup authority result
7. exact runtime identity if applicable
8. Human verification: `Operation 8 HUMAN_PENDING`
9. unverified items
10. preserved exact paths
