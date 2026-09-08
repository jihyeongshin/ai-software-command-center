# 작업지시서: P2-1E 0051 Human QA guide canonical artifact restoration

## meta

- task_id: `20260908_0227_aiscc-p2-1e-0051-human-qa-guide-canonical-artifact-restoration-1`
- created_at: `2026-09-08T02:27:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `COMMAND_CENTER_RECORD_UPDATE / MISSING_CANONICAL_ARTIFACT_RESTORATION`
- evidence_profile: `BASIC`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `P2-1E canonical Human QA guide provenance restoration`

## 현재 상태

- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- current P2-1E implementation/runtime: `ACCEPTED_CANDIDATE / POSTGRESQL_BACKED_RUNTIME EXECUTED_PASS`
- current P2-1E Human QA: `HUMAN_PROVIDED / PARTIAL_ACCEPTED`
- Operation 17: `HUMAN_PROVIDED / PASS`
- Operation 8: `HUMAN_PENDING`
- supported deterministic NextAction NONE fixture availability: `UNKNOWN`
- P2-1: `ACTIVE / NOT_CLOSED`
- P2-2: `NOT_STARTED`
- predecessor task:
  `.aiassistant/tasks/done/20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1.md`
- predecessor cycle:
  `.aiassistant/records/aiscc/cycles/20260908_0222_aiscc-p2-1e-evidence-gap-closure-blocked-missing-canonical-qa-guide-1.cycle.md`
- predecessor handoff:
  `.aiassistant/reports/aiscc/20260908_0222_aiscc-browser-command-center-p2-1e-missing-qa-guide-restoration-entry-handoff-1.md`
- open blocker:
  exact canonical prerequisite missing:
  `.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md`

## 이번 턴 목표

1. Human/Downloads에 이미 공급된 `0051` Human QA guide의 **trusted original candidate**를 좁게 식별한다.
2. candidate의 source path, byte size, SHA-256 및 provenance/identity 근거를 기록한다.
3. trusted original임이 성립할 때만 candidate를 byte-preserving 방식으로 아래 exact canonical destination에 복구한다.
4. destination SHA-256가 source SHA-256와 exact match하는지 검증한다.
5. 이번 변경을 `governance/provenance restoration`으로만 분류하고 report/export를 완료한 뒤 중단한다.

Exact destination:

```text
.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md
```

## 이번 턴 비목표

- supported deterministic NextAction NONE/empty fixture 조사
- PostgreSQL 시작/변경
- AISCC server 시작/변경
- Operation 8 실행 또는 Human Browser QA
- Operation 17 재검증
- product source/test/runtime 수정
- P2-1E terminal acceptance/closure
- P2-1 closure
- P2-2 시작
- Git persistence
- deployment/public release

## 허용 범위

### allowed_paths

읽기:

- repository root와 아래 `must_read` exact paths
- `C:\Users\oracl\Downloads\` 아래에서 **0051 guide candidate를 찾기 위한 exact-name 중심의 좁은 탐색**
- repository 안에서 exact basename 또는 exact canonical path를 참조하는 provenance 기록만 좁게 검색
- 현재 worktree status/diff를 분류하기 위한 Git read-only 명령

쓰기:

- `.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md`
- current Task lifecycle에 필요한:
  - `.aiassistant/tasks/active/20260908_0227_aiscc-p2-1e-0051-human-qa-guide-canonical-artifact-restoration-1.md`
  - `.aiassistant/tasks/done/20260908_0227_aiscc-p2-1e-0051-human-qa-guide-canonical-artifact-restoration-1.md`
  - `.aiassistant/reports/target/20260908_0227_aiscc-p2-1e-0051-human-qa-guide-canonical-artifact-restoration-1/**`

### candidate filename handling

우선 exact basename을 찾는다.

```text
20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md
```

Windows/browser download collision로 `(1)`, `(2)` 같은 suffix가 붙은 candidate가 있을 수 있으므로, 동일 base artifact의 download-copy 후보로 식별 가능한 경우에 한해 후보 목록에 포함할 수 있다.

단, filename 유사성만으로 trusted original을 확정하지 않는다.

### allowed_actions

- exact must-read 문서 읽기
- Downloads의 0051 candidate 후보 존재 여부/metadata 확인
- candidate 전체 내용 읽기
- SHA-256, byte size 계산
- repository 내 exact basename/path reference를 좁게 검색하여 provenance 보강
- source/destination 존재 여부와 hash 비교
- trusted original이 성립하면 byte-preserving copy 1회
- destination 재해시 및 byte equality 검증
- `git status --short`, `git diff -- <exact allowed path>` 등 read-only Git inspection
- report/export 작성
- Task active → done 이동

## trusted original admission 기준

candidate를 canonical destination에 복구하려면 다음을 모두 만족해야 한다.

1. candidate가 Human/Downloads에 존재하는 실제 file이어야 한다.
2. file 내용이 `P2-1E Human Integrated Browser QA`의 operation guide임을 직접 식별할 수 있어야 한다.
3. candidate가 `20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1` artifact와 연결된다는 provenance가 filename, document identity/content, predecessor reference 중 둘 이상의 독립 신호로 성립해야 한다.
4. current repository/canonical record와 내용 충돌이 없어야 한다.
5. reconstruction, paraphrase, regeneration이 아니라 기존 bytes를 그대로 복사할 수 있어야 한다.

가능하면 다음 provenance를 report한다.

```text
candidate source path
candidate filename
candidate first heading/document identity
candidate task_id or guide identity if present
candidate byte size
candidate SHA-256
repository references to exact 0051 artifact
destination pre-state
destination post-state
destination SHA-256
source == destination byte equality
```

## 절대 금지

### forbidden_paths

- product source 전역
- tests/runtime implementation 전역
- DB migration/config
- unrelated `.aiassistant` canonical/rules/records
- root `.gitignore`
- unrelated Downloads 파일

### forbidden_actions

- missing guide를 chat memory/Handoff/Cycle paraphrase로 재작성
- 비슷한 내용의 새 guide 저작
- arbitrary SQL/ad-hoc DB mutation
- fixture discovery
- PostgreSQL/AISCC runtime start
- Browser QA
- external provider/network
- dependency/install
- Git index/commit/push
- deployment
- broad cleanup
- unrelated dirty file mutation

아래 명령은 명시적으로 금지한다.

```text
git add
git commit
git push
git reset
git restore
git checkout
git stash
git clean
```

## 읽을 문서

Minimum authoritative context set:

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md`
- `.aiassistant/tasks/done/20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0222_aiscc-p2-1e-evidence-gap-closure-blocked-missing-canonical-qa-guide-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_0222_aiscc-browser-command-center-p2-1e-missing-qa-guide-restoration-entry-handoff-1.md`

현재 missing target인 아래 path는 **must-read prerequisite로 요구하지 않는다**. 존재 여부 및 restoration destination으로만 취급한다.

```text
.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md
```

## agent instruction transport / authority

- repository-root instruction entrypoint는 thin transport bootstrap이며 project policy authority가 아니다.
- Project Rules UI 또는 automatic retrieval만으로 canonical rule body가 Agent context에 전달됐다고 가정하지 않는다.
- 위 `읽을 문서` 목록은 이번 Task의 minimum authoritative context set이다.
- unrelated rules/records/source/logs를 bulk-read하지 않는다.
- active Task, canonical rules, predecessor Cycle/Handoff, current source가 충돌하면 mutation을 중단하고 conflict를 보고한다.
- Downloads candidate는 provenance 검증 전까지 canonical authority가 아니다.
- candidate가 trusted original로 admit된 뒤에도 **복구 source**일 뿐 Browser/Downloads 자체가 current canonical owner가 되지 않는다.

## source 조사 범위

Exact objective:

```text
0051 trusted original candidate
→ provenance/identity verification
→ exact canonical destination restoration
→ byte/hash verification
→ STOP
```

다음 semantic objective로 넘어가지 않는다.

```text
NONE fixture discovery
Operation 8 runtime preparation
Human Browser QA
```

## 구현/문서/감사 범위

Product implementation:

```text
NOT_APPLICABLE
```

Governance/provenance change:

```text
ONLY:
.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md
```

Temporary artifacts:

```text
current Task active/done lifecycle
current target bundle
```

Repository configuration:

```text
NONE
```

## workflow transition expectation

- initial_state: `BLOCKED_MISSING_ARTIFACT`
- expected_non_terminal_state_when_human_pending: `NOT_APPLICABLE`
- expected_terminal_candidate:
  - `RESTORATION_COMPLETED_CANDIDATE`, or
  - `BLOCKED_MISSING_ARTIFACT`, or
  - `POLICY_CONFLICT_INVESTIGATION_REQUIRED`
- transition_authority: `NOT_APPLICABLE / Browser Command Center judges result`
- Agent가 P2-1E terminal state를 결정할 수 있는가: `No`

## evidence contract

### executor_required

- channel: `CANONICAL_PREREQUISITE_CHECK`
  - scope: exact canonical 0051 destination pre-state
  - allowed_command_or_environment: local filesystem read
  - pass_condition: existence/non-existence와 type을 직접 확인

- channel: `SOURCE_PROVENANCE`
  - scope: Downloads candidate identity/provenance
  - allowed_command_or_environment: narrow local file inspection/hash and exact-reference search
  - pass_condition: trusted original admission 기준을 충족하거나, 충족 불가를 정직하게 보고

- channel: `BYTE_INTEGRITY`
  - scope: restoration 수행 시 source/destination hash 및 byte equality
  - allowed_command_or_environment: local filesystem/hash
  - pass_condition: source SHA-256 == destination SHA-256 and bytes equal

- channel: `WORKSPACE_STATIC`
  - scope: task 전후 allowed-path change 분류
  - allowed_command_or_environment: read-only Git status/diff
  - pass_condition: product/repository configuration mutation 없음, restoration scope 밖 current-task mutation 없음

### reuse_allowed

- channel: `PREDECESSOR_JUDGMENT`
  - predecessor:
    `.aiassistant/records/aiscc/cycles/20260908_0222_aiscc-p2-1e-evidence-gap-closure-blocked-missing-canonical-qa-guide-1.cycle.md`
  - provenance_condition: exact canonical cycle
  - applicability_condition: blocker identity와 restoration destination이 unchanged

- channel: `HUMAN_QA`
  - predecessor: admitted P2-1E Human QA lineage
  - provenance_condition: Operation 17 already `HUMAN_PROVIDED / PASS`
  - applicability_condition: 이번 Task가 product/runtime source를 수정하지 않음
  - use: preserve only; do not rerun

### human_owned

- channel: `BROWSER_RUNTIME`
  - scope: Operation 8 NextAction empty/NONE truthful state
  - expected_result_format: `HUMAN_PENDING`
  - this_task: `DO_NOT_RUN`

### not_required

- channel: `DATABASE_RUNTIME`
  - reason: canonical artifact restoration only
- channel: `HTTP_RUNTIME`
  - reason: canonical artifact restoration only
- channel: `BROWSER_RUNTIME`
  - reason: current restoration action에는 실행 불필요
- channel: `UNIT_TEST / INTEGRATION_TEST`
  - reason: product source 변경 없음

### forbidden

- action_or_channel: `arbitrary SQL / fixture fabrication`
  - reason: predecessor evidence-gap contract 위반
- action_or_channel: `Git persistence`
  - reason: Browser Command Center authorization 없음
- action_or_channel: `product source mutation`
  - reason: restoration Task 비목표

### proof_non_substitution

```text
Downloads file presence
!= trusted canonical provenance

filename similarity
!= trusted original identity

Cycle/Handoff paraphrase
!= missing guide bytes

restored file hash equality
!= Operation 8 Browser PASS

Executor completion
!= P2-1E ACCEPTED
```

## conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant:
  - repository-local canonical remains authority
  - Downloads copy cannot silently substitute for canonical
  - byte-preserving restoration only
  - named blocker 이후 unrelated execution 금지
- required_actual_owner: `Browser Command Center / repository canonical governance`
- planned_vs_actual_scope: exact restoration-only scope를 보고
- rollback_or_failure_semantics:
  - source trust 미성립: destination을 만들지 않고 `BLOCKED_MISSING_ARTIFACT`
  - destination이 이미 존재하며 trusted source와 byte-identical: no-op verified restoration state
  - destination이 이미 존재하지만 trusted source와 다름: overwrite하지 말고 `POLICY_CONFLICT_INVESTIGATION_REQUIRED`
  - copy 도중 integrity mismatch: destination을 canonical success로 주장하지 말고 안전하게 중단/보고

## project context impact

architecture:
- `NONE`

orchestration_contract:
- `NONE`

security_sandbox:
- `NONE`

public_provenance:
- `TASK_AND_CYCLE_ONLY`
- Cycle 생성은 Browser Command Center 소유이며 Executor가 생성하지 않는다.

## accept 기준

아래 중 하나를 명확히 달성해야 한다.

### A. restoration completed candidate

```text
trusted original candidate:
ESTABLISHED

source path/size/SHA-256:
RECORDED

destination:
exact canonical path

copy semantics:
BYTE_PRESERVING

destination SHA-256:
MATCHES SOURCE

product/runtime mutation:
NONE

Git persistence:
NOT_RUN

fixture discovery:
NOT_RUN

Operation 8:
HUMAN_PENDING
```

### B. blocker preserved correctly

```text
trusted original candidate:
NOT_ESTABLISHED

destination mutation:
NONE

result:
BLOCKED_MISSING_ARTIFACT
```

### C. conflict stop

```text
existing destination or candidate provenance conflict:
ESTABLISHED

overwrite/reconstruction:
NOT_RUN

result:
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

## hold/reject 기준

- untrusted candidate를 canonical로 복사
- Handoff/Cycle/chat에서 guide를 재구성
- product/runtime source 변경
- fixture discovery 시작
- DB/server/browser 실행
- unrelated Downloads/source bulk-read
- forbidden Git action 실행
- source/destination hash mismatch를 success로 보고
- Operation 8 또는 P2-1E accepted를 executor가 주장

## mandatory stop 조건

- trusted original candidate를 확립할 수 없음
- candidate provenance conflict
- exact destination에 unexpected different content 존재
- policy baseline conflict
- dirty workspace collision이 exact restoration path와 충돌
- forbidden action/tool request
- security boundary uncertainty
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`

named blocker 이후에는 blocker 입증 최소 evidence, workspace inventory, report/export와 안전한 종료만 수행한다.

## 보고서 필수 항목

- 작업명 / work type / task path
- read canonical paths
- candidate discovery method와 좁은 source inventory
- source candidate path / filename / size / SHA-256
- candidate identity/provenance admission 근거
- destination pre-state
- product source changes
- governance/provenance changes
- repository configuration changes
- temporary generated artifacts
- added/modified/removed files
- source → destination byte/hash verification
- Task evidence contract와 실제 result classification
- Agent claim vs admitted evidence 구분
- Operation 17 preserved `HUMAN_PROVIDED / PASS`
- Operation 8 `HUMAN_PENDING / DO_NOT_RUN`
- fixture availability `UNKNOWN / DO_NOT_DISCOVER`
- forbidden-not-run
- mandatory stop/scope expansion
- planned-vs-actual conformance
- unverified items
- rollback/revert guide
- preserved exact paths
- next turn recommendation

## export bundle 요구

Target:

```text
.aiassistant/reports/target/20260908_0227_aiscc-p2-1e-0051-human-qa-guide-canonical-artifact-restoration-1/
```

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- restored changed governance file preserving project-relative path, restoration이 실제 수행된 경우
- `REMOVED_FILES.md` only when deletion exists

Export에는 unrelated unchanged source, private/secret data, Downloads 원본 자체를 복제하지 않는다.
필요한 source provenance는 report에 path/size/hash/identity만 기록한다.

## 사람 검증 요구

이번 Executor Task 자체에는 Browser Human QA가 없다.

```text
Human Browser verification:
NOT_REQUIRED_THIS_TASK

Operation 8:
HUMAN_PENDING / DEFERRED
```

Restoration candidate는 Browser Command Center가 target bundle/report를 판정한 뒤에만 admitted restoration이 된다.

## 후속 행동 경계

성공적으로 restoration candidate가 만들어져도 Executor가 같은 turn에서 `0208` objective를 재개하지 않는다.

Browser Command Center가 restoration을 별도로 admit한 뒤 새 timestamped Task로:

```text
QA_ONLY / EVIDENCE_GAP_CLOSURE

FIRST:
supported deterministic NextAction NONE/empty fixture authority discovery

IF FOUND:
narrow PostgreSQL/AISCC runtime preparation
→ exact runtime identity
→ Human Operation 8 only

IF NOT FOUND:
do not fabricate authority
→ EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

## 보존 artifact

최소 보존:

- `.aiassistant/tasks/done/20260908_0208_aiscc-p2-1e-nextaction-none-human-qa-evidence-completion-1.md`
- `.aiassistant/records/aiscc/cycles/20260908_0222_aiscc-p2-1e-evidence-gap-closure-blocked-missing-canonical-qa-guide-1.cycle.md`
- `.aiassistant/reports/aiscc/20260908_0222_aiscc-browser-command-center-p2-1e-missing-qa-guide-restoration-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260908_0227_aiscc-p2-1e-0051-human-qa-guide-canonical-artifact-restoration-1.md`
- restoration 성공 시:
  `.aiassistant/tasks/done/20260908_0051_aiscc-p2-1e-human-integrated-browser-qa-operation-guide-1.md`

## 최종 응답 형식

1. result: `completed / blocked / rejected-candidate`
2. target bundle path
3. trusted source candidate: path / size / SHA-256 / provenance verdict
4. destination pre/post state and SHA-256
5. changed files
6. removed files
7. human verification
8. unverified items
9. preserved exact paths
10. explicit statement:
   - fixture discovery `NOT_RUN`
   - Operation 8 `HUMAN_PENDING`
   - Git persistence `NOT_RUN`
