# 작업지시서: Retry P2-1E NextAction NONE Human QA evidence completion

## meta

- task_id: `20260908_0303_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-retry-1`
- created_at: `2026-09-08T03:03:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `QA_ONLY / EVIDENCE_GAP_CLOSURE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `P2-1E NextAction NONE Human Browser evidence completion`

## 현재 상태

- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- current P2-1E implementation state: `ACCEPTED_CANDIDATE`
- current PostgreSQL-backed runtime evidence: `EXECUTED_PASS`
- current Human QA state: `HUMAN_PROVIDED / PARTIAL_ACCEPTED`
- `Operation 17 visible polling resume`: `HUMAN_PROVIDED / PASS`
- `Operation 8 NextAction empty/NONE truthful state`: `HUMAN_PENDING`
- 0051 canonical QA guide: `RESTORED / BROWSER_COMMAND_CENTER_ACCEPTED`
- supported deterministic NONE fixture availability: `UNKNOWN`
- P2-1: `ACTIVE / NOT_CLOSED`
- P2-2: `NOT_STARTED`
- PUBLIC_BOUNDED_LIVE: `NOT_RELEASED`

Current accepted restoration prerequisite:

```text
.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md

accepted size:
25366 bytes

accepted SHA-256:
17d09506a7b5c18ff96646e88193ba2c7aa134bcaaeb58864732491cd461681e
```

The predecessor missing-artifact blocker is resolved.

This Task does **not** reopen the 0051 restoration judgment.

## predecessor authority

- `.aiassistant/records/aiscc/cycles/20260908_0158_aiscc-p2-1e-human-browser-qa-partial-accepted-nextaction-none-fixture-gap-1.cycle.md`
- `.aiassistant/tasks/done/20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0222_aiscc-p2-1e-evidence-gap-closure-blocked-missing-canonical-qa-guide-1.cycle.md`
- `.aiassistant/tasks/done/20260908_0227_aiscc-p2-1e-0051-human-qa-guide-canonical-artifact-restoration-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0259_aiscc-p2-1e-0051-canonical-qa-guide-restoration-accepted-evidence-gap-retry-entry-1.cycle.md`

The old `0208` Task is provenance only.
Do not reuse it as an active Task.

## 이번 턴 목표

1. Restored canonical 0051 QA guide와 predecessor evidence contract를 읽는다.
2. **existing repository-provided deterministic fixture/setup authority**만 조사하여 NextAction empty/NONE state를 만들 수 있는 supported fixture가 실제로 존재하는지 판정한다.
3. supported fixture가 존재할 때만 그 fixture contract를 그대로 사용해 narrow local PostgreSQL/AISCC runtime을 준비한다.
4. Human이 **Operation 8 only**를 수행할 수 있도록 exact runtime identity를 출력하고 중단한다.
5. supported fixture가 존재하지 않는 것으로 authority audit가 충분히 확정되면 fixture를 새로 만들거나 DB를 임의 조작하지 말고 `EVIDENCE_SCOPE_EXPANSION_REQUIRED`로 종료한다.

## 이번 턴 비목표

- 0051 guide restoration 재검증/재복원
- Operations 1-7 재실행
- Operations 9-22 재실행
- Operation 17 재실행
- product source 수정
- test source 수정
- migration 작성
- 새로운 durable fixture authority 추가
- arbitrary/ad-hoc SQL로 NONE 상태 생성
- unrelated PostgreSQL fixture 생성
- Git persistence
- deployment
- P2-1E terminal acceptance 판정
- P2-1 closure
- P2-2 시작
- PUBLIC_BOUNDED_LIVE release

## 허용 범위

### allowed_paths

Read-only discovery는 현재 Task 목적에 필요한 repository-local source/test/fixture/setup 경로에 한정한다.

반드시 먼저 exact canonical 문서를 읽고, 그 이후 fixture/setup authority를 찾기 위한 좁은 source discovery만 수행한다.

Mutation이 허용되는 repository tracked source path:

```text
NONE
```

Temporary runtime/report lifecycle에 필요한 ignored path는 기존 canonical rule 범위에서만 허용한다.

### allowed_actions

- exact must-read canonical document read
- current repository status/inventory read
- deterministic fixture/setup authority를 찾기 위한 targeted filename/text/symbol search
- 발견한 fixture/setup contract의 source read
- supported fixture가 존재하는 경우에 한해:
  - Task-scoped local PostgreSQL runtime 준비
  - canonical migration/runtime bootstrap
  - repository가 이미 제공하는 fixture/setup mechanism 실행
  - normal AISCC local server 시작
  - fixture identity와 runtime identity 확인
  - Human Operation 8 진입에 필요한 exact Project/runtime identifiers 출력
- report/export 작성
- Task lifecycle `active → done`

## 절대 금지

### forbidden_paths / mutations

- product source 변경
- test source 변경
- migration 변경/추가
- canonical baseline/rule 변경
- existing fixture source 수정
- 새로운 fixture 파일 추가
- `.gitignore` 변경
- unrelated governance file 수정

### forbidden_actions

- arbitrary SQL / ad-hoc INSERT/UPDATE/DELETE로 NextAction NONE 상태 제조
- fixture 존재를 source evidence 없이 추론
- 한 군데 검색 실패를 전체 fixture 부재로 단정
- unsupported/manual DB mutation을 fixture처럼 취급
- Operations 1-7 또는 9-22 Browser 재실행
- Operation 17 Browser 재실행
- browser automation으로 Human-owned Operation 8을 executor-completed라고 주장
- product/test refactor
- full-suite 또는 unrelated module verification
- external network/credentialed environment
- Git index / commit / push
- `git reset`
- `git restore`
- `git checkout`
- `git stash`
- `git clean`
- deployment
- P2-2 start

## 읽을 문서

Minimum authoritative context set:

1. `.aiassistant/rules/AISCC_AGENTS.md`
2. `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
3. `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
4. `.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md`
5. `.aiassistant/tasks/done/20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1.md`
6. `.aiassistant/records/aiscc/cycles/20260908_0158_aiscc-p2-1e-human-browser-qa-partial-accepted-nextaction-none-fixture-gap-1.cycle.md`
7. `.aiassistant/records/aiscc/cycles/20260908_0222_aiscc-p2-1e-evidence-gap-closure-blocked-missing-canonical-qa-guide-1.cycle.md`
8. `.aiassistant/tasks/done/20260908_0227_aiscc-p2-1e-0051-human-qa-guide-canonical-artifact-restoration-1.md`
9. `.aiassistant/records/aiscc/cycles/20260908_0259_aiscc-p2-1e-0051-canonical-qa-guide-restoration-accepted-evidence-gap-retry-entry-1.cycle.md`

Do not bulk-read unrelated rules/records/source/logs.

## agent instruction transport / authority

- repository-root instruction entrypoint는 thin transport bootstrap이며 project policy authority가 아니다.
- Project Rules UI 또는 automatic retrieval만으로 canonical rule body가 Agent context에 전달됐다고 가정하지 않는다.
- 위 `읽을 문서` 목록은 minimum authoritative context set이다.
- exact path를 직접 읽는다.
- unrelated rules/records/source/logs를 bulk-read하지 않는다.
- active Task File, canonical rule, current source, accepted evidence가 충돌하면 mutation/runtime 준비를 중단하고 conflict investigation으로 보고한다.
- human-owned evidence를 executor-completed로 주장하지 않는다.
- repository-local canonical이 Browser Project Source mirror보다 우선한다.

## 조사할 source

### FIRST — fixture/setup authority discovery

다음 의미를 만족하는 **existing repository-provided deterministic authority**를 찾는다.

```text
P2-1E integrated Project UI를 실제 PostgreSQL-backed runtime에서 열었을 때
NextAction이 empty/NONE truthful state가 되도록
repository에 이미 정의된 deterministic fixture/setup mechanism
```

Search는 targeted discovery로 수행한다.

후보 예시 범주는 다음과 같으나, exact 이름을 가정하지 않는다.

```text
fixture
seed
scenario
demo data
test data
runtime bootstrap
PostgreSQL setup
project/workrun/cycle/next-action setup
NONE / empty NextAction state
```

반드시 다음을 구분한다.

```text
fixture candidate found
!= supported fixture authority established

obvious candidate not found
!= supported fixture does not exist
```

Supported fixture로 인정하려면 최소한:

1. repository source에 실제 존재하고,
2. 현재 P2-1E runtime/QA를 위한 사용 경로가 source 또는 accepted Task/guide와 정합하며,
3. arbitrary row mutation이 아니라 repeatable setup mechanism이고,
4. Operation 8의 semantic state를 deterministic하게 만들 수 있으며,
5. 현재 source identity를 수정하지 않고 실행 가능해야 한다.

### IF supported fixture exists

다음 순서만 수행한다.

```text
supported fixture authority established
→ exact fixture/setup identity 기록
→ narrow local PostgreSQL 준비
→ repository-provided setup mechanism 실행
→ normal AISCC server 준비
→ exact QA runtime identity 확인
→ STOP FOR HUMAN OPERATION 8
```

Human에게 최소 다음 runtime identity를 제공한다.

```text
server:
http://127.0.0.1:<actual-port>

project_id:
<actual NONE/empty fixture project id>

cycle_id:
<actual if applicable>

primary_work_run_id:
<actual if applicable>

terminal_work_run_id:
<actual if applicable>

fixture/setup authority:
<exact repository path / command / identifier>
```

0051 guide가 Operation 8 진입에 더 적은/다른 exact identity를 요구하면 guide를 따른다.

### IF supported fixture does not exist

부재 판정은 authority audit가 충분할 때만 허용한다.

그 경우:

```text
result:
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

그리고 정확히 보고한다.

```text
supported deterministic NONE fixture:
NOT_ESTABLISHED / NO_SUPPORTED_EXISTING_AUTHORITY_FOUND

new fixture or ad-hoc DB mutation required:
YES

Operation 8:
HUMAN_PENDING

product/test mutation:
NOT_PERFORMED
```

새 fixture를 작성하지 않는다.
임의 SQL로 상태를 만들지 않는다.

## workflow transition expectation

- initial_state: `P2-1E HUMAN QA PARTIAL_ACCEPTED / Operation 8 HUMAN_PENDING`
- expected_non_terminal_state_when_fixture_exists: `COMMAND_PREREQUISITE_REACHED / HUMAN_PENDING`
- expected_terminal_candidate: `NOT_APPLICABLE_THIS_EXECUTOR_TURN`
- transition_authority: `NOT_APPLICABLE`
- Agent가 P2-1E terminal state를 직접 결정할 수 있는가: `No`

## evidence contract

### executor_required

#### 1. fixture authority discovery

- channel: `STATIC_SOURCE / FIXTURE_SETUP_AUTHORITY`
- scope: existing repository-provided deterministic NONE/empty fixture/setup authority
- allowed_command_or_environment:
  - targeted repository read/search only
- pass_condition:
  - supported existing authority established with exact provenance
  - OR sufficient audit establishes no supported existing authority and returns `EVIDENCE_SCOPE_EXPANSION_REQUIRED`

#### 2. workspace scope verification

- channel: `WORKSPACE_STATIC`
- scope: pre/post workspace identity and current Task mutation boundary
- pass_condition:
  - no product/test/config source mutation
  - no unrelated cleanup/reset/index action
  - current Task changes limited to permitted Task/report lifecycle artifacts

#### 3. PostgreSQL/runtime preparation — CONDITIONAL

- channel: `DATABASE_RUNTIME`
- applicability: `ONLY_IF_SUPPORTED_FIXTURE_EXISTS`
- scope: narrow local PostgreSQL required by supported fixture
- pass_condition:
  - canonical migrations/runtime bootstrap succeeds
  - existing supported fixture/setup mechanism succeeds
  - exact target Project/state identity can be emitted

#### 4. AISCC server preparation — CONDITIONAL

- channel: `HTTP_RUNTIME`
- applicability: `ONLY_IF_SUPPORTED_FIXTURE_EXISTS`
- scope: normal local AISCC server required for Human Operation 8
- pass_condition:
  - server is reachable at emitted local URL
  - exact Project/runtime identity is available
  - no unrelated Browser operation is executed by Executor

### reuse_allowed

#### P2-1E implementation/runtime predecessor proof

- channel: `STATIC_SOURCE / POSTGRESQL_BACKED_RUNTIME`
- predecessor:
  - accepted P2-1E source/runtime evidence already recorded by predecessor Cycles
- provenance_condition:
  - current source identity relevant to those proofs has not been mutated by this Task
- applicability_condition:
  - reuse is background confidence only; it does not substitute for the specific NONE fixture runtime needed for Operation 8

#### Operation 17

- channel: `HUMAN_VERIFICATION`
- predecessor:
  - `Operation 17 visible polling resume: HUMAN_PROVIDED / PASS`
- applicability_condition:
  - no source mutation invalidates the result
- result:
  - preserve without rerun

### human_owned

#### Operation 8

- channel: `BROWSER_RUNTIME / HUMAN_VERIFICATION`
- scope:
  - `Operation 8 NextAction empty/NONE truthful state`
- expected_result_format:

```text
Operation 8 NextAction empty/NONE truthful state:
PASS
```

or:

```text
Operation 8 NextAction empty/NONE truthful state:
FAIL
<actual visible behavior / wording>
```

Executor success ceiling before Human result:

```text
Operation 8:
HUMAN_PENDING
```

### not_required

- Operations 1-7: previously admitted; not rerun
- Operations 9-22: previously admitted; not rerun
- Operation 17: already `HUMAN_PROVIDED / PASS`
- UNIT_TEST: no source mutation; not required for this evidence-gap closure
- INTEGRATION_TEST: no source mutation; not required unless canonical fixture mechanism itself explicitly requires a narrow setup command already within its contract
- deployment: not required
- public release: not required

### forbidden

- arbitrary SQL / DB row fabrication
- new fixture creation
- product/test source mutation
- unrelated browser QA
- Git persistence
- deployment
- P2-2

### proof_non_substitution

```text
fixture source presence
!= supported fixture authority

supported fixture authority
!= Operation 8 Browser PASS

runtime preparation
!= Human Browser verification

Executor report
!= Human Operation 8 result

Operation 17 PASS
!= Operation 8 PASS

0051 guide restoration
!= Operation 8 Browser proof
```

## conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant:
  - existing authority first
  - proof type non-substitution
  - human-owned Browser evidence
  - no ad-hoc fixture fabrication
  - no task scope expansion
- required_actual_owner:
  - fixture/setup authority: repository current source
  - Operation 8 result: Human
- planned_vs_actual_scope:
  - report exact fixture search scope
  - report runtime actions only if fixture is established
- rollback_or_failure_semantics:
  - Task-owned local runtime/container/process may be safely stopped if the Task reaches a blocker before Human handoff
  - if runtime is intentionally left active for immediate Human Operation 8, report exact active runtime and cleanup ownership
  - never modify tracked source merely to make cleanup easier

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

### Executor prerequisite success candidate

All:

1. restored 0051 canonical guide was read successfully.
2. existing supported deterministic NONE/empty fixture authority was established.
3. no product/test source mutation occurred.
4. no arbitrary SQL/ad-hoc row mutation occurred.
5. narrow PostgreSQL/AISCC runtime was prepared using only supported authority.
6. exact Human QA runtime identity was emitted.
7. Executor stopped before performing Human-owned Operation 8.
8. report/export is complete.

Maximum result wording:

```text
COMMAND_PREREQUISITE_REACHED
Operation 8: HUMAN_PENDING
```

This is not P2-1E acceptance.

## hold/block 기준

### `BLOCKED_MISSING_ARTIFACT`

Use only if a newly required exact canonical artifact is actually missing.

### `POLICY_CONFLICT_INVESTIGATION_REQUIRED`

Use if current canonical guide/Task/source authority conflict materially changes the allowed fixture/runtime path.

### `EVIDENCE_SCOPE_EXPANSION_REQUIRED`

Use when:

```text
Operation 8 deterministic NONE state cannot be produced from an existing supported repository fixture/setup authority
AND
new product/test fixture or ad-hoc DB mutation would be required
```

Do not create that fixture in this Task.

## mandatory stop 조건

Immediately stop further scope expansion after any of:

- policy baseline conflict
- missing required artifact
- dirty workspace collision affecting safe execution
- forbidden action/tool requirement
- security boundary uncertainty
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`
- Human Operation 8 prerequisite reached

After a named blocker or Human prerequisite is reached, perform only:

```text
minimal blocker/prerequisite evidence
workspace inventory
report/export
safe runtime state reporting
Task lifecycle completion
```

Do not continue into unrelated verification.

## 보고서 필수 항목

- 작업명 / work type / task path
- repository / branch / HEAD
- read canonical paths
- restored 0051 guide identity observed
- fixture authority search scope
- candidate fixtures considered
- supported fixture admission reasoning
- exact fixture/setup path/command/identifier if established
- workspace before/after
- product source changes
- governance/provenance changes
- repository configuration changes
- Task evidence contract
- actual evidence result classification
- PostgreSQL runtime result if applicable
- AISCC server/runtime identity if applicable
- Agent claim vs admitted evidence
- `Operation 17: HUMAN_PROVIDED / PASS` preserved
- `Operation 8: HUMAN_PENDING`
- forbidden-not-run
- mandatory stop/scope expansion result
- unverified items
- active runtime / cleanup ownership
- rollback/revert guide
- preserved artifact exact paths
- next turn recommendation

## export bundle 요구

Target:

```text
.aiassistant/reports/target/20260908_0303_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-retry-1/
```

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`

Changed repository product/test files:

```text
NONE EXPECTED
```

If no deletion exists, do not create `REMOVED_FILES.md`.

## 사람 검증 요구

If Executor reports:

```text
COMMAND_PREREQUISITE_REACHED
```

Human performs **only Operation 8** from:

```text
.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md
```

Do not rerun Operations 1-7 or 9-22.

Human returns PASS or FAIL with actual visible behavior/wording.

If Executor returns:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

there is no Human Browser QA to perform yet.
Return the Executor target bundle to Browser Command Center for judgment.

## 최종 응답 형식

1. result: `COMMAND_PREREQUISITE_REACHED` / `EVIDENCE_SCOPE_EXPANSION_REQUIRED` / `BLOCKED_*`
2. target bundle path
3. supported deterministic NONE fixture:
   - `ESTABLISHED` + exact authority
   - or `NOT_ESTABLISHED / NO_SUPPORTED_EXISTING_AUTHORITY_FOUND`
4. changed files
5. removed files
6. active runtime identity / cleanup state
7. human verification:
   - `Operation 17: HUMAN_PROVIDED / PASS`
   - `Operation 8: HUMAN_PENDING`
8. unverified items
9. preserved exact paths
