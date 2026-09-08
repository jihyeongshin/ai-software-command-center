# AISCC Repository Canonical Metadata

- canonical_owner: `AISCC_REPOSITORY`
- authority: `REPOSITORY_LOCAL_CANONICAL`
- bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
- canonicalized_by_task: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`

---


# AISCC Command Center Workflow

## 1. 목적

Browser Command Center가 장문 chat instruction에 의존하지 않고 Task Contract 기반으로 IDE Executor를 지시하고, proof ownership과 judgment를 관리하며, 공개 가능한 Cycle Record를 생성하는 표준 workflow를 정의한다.

## 2. 표준 cycle

```text
사람 토의 / 요구 정리
→ Command Center가 work type과 authority gap 분류
→ Task File 생성
→ Command Center가 현재 발행 artifact만 담은 flat ZIP과 Short Prompt 제공
→ 사람이 ZIP을 `C:\Users\oracl\Downloads`에 flat 압축해제
→ fresh IDE chat이 요구되면 사람이 새 IDE chat을 엶
→ Executor가 issued artifact를 canonical destination으로 transport하고 hash 검증
→ transport PASS 뒤 Task File을 읽음
→ IDE Executor가 task-listed canonical source를 읽음
→ source 변경 / 검증 / report / temporary target bundle 생성
→ Task File을 `.aiassistant/tasks/done/`으로 이동
→ 사람이 target bundle을 Browser Command Center에 제출
→ Task / Report / changed files / evidence / human result 판정
→ terminal judgment 생성
→ Cycle Record 생성 또는 갱신
→ 필요 시 canonical baseline / Project Source mirror 판정
→ Next Action 선택
```

Self-dogfooding cutover 뒤에는 일부 단계가 AISCC runtime으로 자동화될 수 있지만, authority/evidence/human ownership 의미는 동일하게 유지한다.

## 3. task-generation output contract

Command Center가 Task File을 발행하면 Browser chat에는 기본적으로 다음을 제공한다.

1. 현재 발행 artifact만 포함한 flat ZIP download link
2. issued artifact별 exact filename과 SHA-256
3. source root와 exact canonical destination
4. transport-first Short Prompt와 substantive Task path
5. 중요한 주의사항 1~3줄

Task 전문은 `.md` artifact에 둔다. 사용자가 전문 출력을 명시적으로 요구한 경우에만 chat에 출력한다.

### 3.1 IDE Executor fresh-session decision

fresh IDE Executor chat은 task-scoped decision이다. Command Center는 explicit authority/context boundary가 있을 때만 `REQUIRED`를 선택하고 이유를 남긴다. 모든 Task transition에서 freshness를 자동 추론하지 않는다.

`REQUIRED`이면 Browser response는 Short Prompt 위에 다음 Human-visible 문장과 짧은 이유를 표시한다.

```text
이번 작업은 IDE Executor에서 새 채팅세션을 열고 시작해야 합니다.
```

Human이 새 IDE chat을 연다. Short Prompt는 IDE Executor에게 chat을 만들거나 열라고 지시해서는 안 된다.

### 3.2 Browser session과 Handoff boundary

```text
fresh IDE Executor session != fresh Browser Command Center session
Cycle issuance != Browser session termination
Handoff issuance != mandatory after every substantive judgment
```

다음 generalized rule은 `SUPERSEDED / INVALID_GENERALIZATION`이다.

```text
every substantive Executor-bundle judgment
→ Cycle + Handoff
→ mandatory new Browser Command Center session
```

Browser Handoff/session migration은 explicit Human request, phase/context migration으로 인한 authority ambiguity, material context exhaustion/unsafe continuation, 또는 Human/Command Center가 선택한 다른 explicit Browser-session boundary가 실제로 있을 때만 사용한다. 일반 standard cycle과 `cycle_record_action=create`는 Browser rotation을 자동 발생시키지 않는다.

### 3.3 artifact delivery와 Executor transport

Command Center가 `TASK / CYCLE / JUDGMENT / HANDOFF` 중 어떤 subset을 발행하든, 같은 Browser turn은 존재하는 issued artifact만 담은 하나의 flat ZIP을 제공한다. absent artifact type은 생성하지 않는다.

Human은 ZIP을 내려받아 `C:\Users\oracl\Downloads`에 flat 압축해제하고, 필요한 경우 새 IDE chat을 연 뒤 Short Prompt를 전달한다. Short Prompt는 artifact별 exact filename, expected SHA-256, source root, exact canonical destination, 아래 algorithm, stop semantics, transport PASS 후 읽을 substantive Task path를 포함한다.

Canonical destination:

```text
TASK     → C:\Users\oracl\IdeaProjects\ai-software-command-center\.aiassistant\tasks\active\
CYCLE    → C:\Users\oracl\IdeaProjects\ai-software-command-center\.aiassistant\records\aiscc\cycles\
JUDGMENT → C:\Users\oracl\IdeaProjects\ai-software-command-center\.aiassistant\reports\aiscc\
HANDOFF  → C:\Users\oracl\IdeaProjects\ai-software-command-center\.aiassistant\reports\aiscc\
```

Executor는 issued artifact마다 source 존재와 expected SHA-256을 먼저 확인하고 canonical destination을 검사한다. destination이 없으면 byte-preserving copy 후 source/destination hash equality를 요구한다. destination이 있으면 기존 hash를 먼저 계산하여 같을 때 overwrite하지 않고, 다를 때만 current issued source로 overwrite한 뒤 equality를 다시 요구한다. equality가 확인된 artifact의 flat Downloads source만 제거하며 ZIP은 제거하지 않는다.

이 hash-aware overwrite는 current package가 exact하게 발행한 파일에만 적용한다. source missing, expected hash mismatch, destination/copy/overwrite failure, post-copy hash mismatch, ambiguous result가 하나라도 있으면 substantive Task 실행 전에 STOP한다. 목적은 Human의 canonical file 배치 실수가 missing-artifact 또는 wrong-path blocker를 만드는 것을 방지하는 것이다.

## 4. instruction transport contract

```text
automatically discovered agent instructions
→ task-listed canonical sources explicitly read
→ current Task File
```

위 순서는 transport를 설명하며 project authority를 자동 변경하지 않는다.

- Task File must-read list는 minimum authoritative context set이다.
- unrelated source/log/rule bulk-read를 금지한다.
- conflict가 있으면 implementation을 중단한다.
- fresh-session verification이 없는 instruction transport를 final accepted로 과장하지 않는다.

## 5. work type taxonomy

- `DISCOVERY_AUDIT`: current source/product/prior-art/ownership 탐색
- `DESIGN_AUDIT`: architecture, state machine, policy, security 설계
- `DOC_BASELINE_UPDATE`: canonical baseline 생성/보강
- `ORCHESTRATION_IMPLEMENTATION`: state machine/transition/runtime 구현
- `EVIDENCE_ADMISSION_IMPLEMENTATION`: evidence type/owner/gate 구현
- `SECURITY_SANDBOX_IMPLEMENTATION`: sandbox/tool/network/secret boundary 구현
- `BACKEND_IMPLEMENTATION`: API/application/persistence 구현
- `FRONTEND_IMPLEMENTATION`: Command Center UI 구현
- `REWORK`: HOLD/REJECT 이후 보정
- `QA_ONLY`: 검증 중심 작업
- `DEMO_SCENARIO`: synthetic demo/replay 작성
- `SELF_DOGFOOD_CUTOVER`: AISCC가 자신의 개발 workflow를 실행하기 위한 전환
- `WORKFLOW_RULE_UPDATE`: Task/Evidence/Judgment/Cycle rule 보강
- `COMMAND_CENTER_RECORD_UPDATE`: current state/decision/next-action 갱신
- `PROJECT_SOURCE_MIRROR_SYNC`: canonical active set을 Browser Project Source mirror로 생성
- `SOURCE_EVIDENCE_EXPORT`: exact allowlist의 unchanged source를 review용으로 read-only export
- `RELEASE_SUBMISSION`: public release/competition submission artifact 작성

## 6. evidence channel taxonomy

가능한 channel 예:

```text
STATIC_SOURCE
BUILD
UNIT_TEST
INTEGRATION_TEST
DATABASE_RUNTIME
HTTP_ARTIFACT
HTTP_RUNTIME
FRONTEND_SOURCE_TEST
BROWSER_RUNTIME
SECURITY_SANDBOX
OBSERVABILITY
HUMAN_VERIFICATION
PUBLIC_PROVENANCE
```

모든 task에 모든 channel을 넣지 않는다.

## 7. evidence profile

- `BASIC`: 문서·명칭·작은 저위험 변경
- `STANDARD`: 일반 backend/frontend/orchestration 구현
- `HIGH_RISK`: sandbox, tool permission, secret/network, transition authority, persistence integrity, concurrency, deployment/recovery

어떤 profile도 고정 full checklist를 자동 요구하지 않는다.

## 8. Task File evidence ownership

- `executor_required`: 이번 task에서 executor가 직접 만들어야 하는 proof
- `reuse_allowed`: accepted predecessor proof를 조건부 재사용할 범위
- `human_owned`: executor가 수행 또는 완료 주장할 수 없는 proof
- `not_required`: 누락이 아닌 비적용 proof
- `forbidden`: 수행 자체가 workflow/security 위반인 action

## 9. Executor result classification

```text
EXECUTED_PASS
EXECUTED_FAIL
REUSED_ACCEPTED
HUMAN_PROVIDED
HUMAN_PENDING
NOT_REQUIRED
FORBIDDEN_NOT_RUN
BLOCKED_REQUIRED_EVIDENCE
```

빈 report field를 채우기 위해 새 evidence를 수집하지 않는다.

## 10. proof type non-substitution

다음은 서로를 과장해 대체하지 않는다.

```text
unit test != integration/runtime proof
mock/in-memory DB != target database proof
HTTP artifact updated != HTTP runtime executed
frontend source test != browser QA
browser checklist created != browser QA passed
security unit test != sandbox escape/runtime proof
executor report != human acceptance
Agent claim != evidence admission
accepted predecessor proof != current changed-path proof
```

재사용은 Task File의 `reuse_allowed`, provenance, 적용 조건이 모두 맞을 때만 허용한다.

## 11. human-owned evidence

Task File이 달리 정하지 않는 한 다음은 사람 소유 후보다.

- 실제 browser/visual/useability QA
- 실제 credential/account/permission 확인
- public release/publish/competition submit
- business/product acceptance
- policy 선택
- production/test environment 관측
- 예외 security approval

Executor는 안전한 절차와 checklist를 만들 수 있지만, 사람 결과가 없으면 `HUMAN_PENDING`이다.

## 12. evidence scope expansion

Task와 같은 환경의 narrow syntax/static check, changed-path targeted test, `git diff --check`는 일반적으로 허용할 수 있다.

다음은 명시 없이 수행하지 않는다.

- 새 DB/runtime harness
- 다른 module 전체 suite
- 외부 server/network
- browser runtime
- credentialed account
- production/test infrastructure
- broad benchmark
- 비목표 영역 검증

필요하면:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

로 중단한다.

## 13. mandatory stop

다음 blocker 이후에는 blocker 입증 최소 evidence, workspace inventory, report/export, 안전한 종료만 수행한다.

```text
BLOCKED_MISSING_ARTIFACT
BLOCKED_POLICY_GAP
POLICY_CONFLICT_INVESTIGATION_REQUIRED
HOLD_REWORK_REQUIRED
EVIDENCE_SCOPE_EXPANSION_REQUIRED
SECURITY_BOUNDARY_BLOCKED
COMMAND_PREREQUISITE_REACHED
```

report 완성을 위해 unrelated suite, network, browser, benchmark를 계속하지 않는다.

## 14. result status taxonomy

- `ACCEPTED`
- `ACCEPTED_PENDING_SOURCE_MIRROR_SYNC`
- `ACCEPTED_CANDIDATE`
- `PARTIAL_ACCEPTED`
- `HOLD_REWORK_REQUIRED`
- `REJECTED_ROLLBACK_REQUIRED`
- `BLOCKED_POLICY_GAP`
- `BLOCKED_MISSING_ARTIFACT`
- `BLOCKED_SECURITY_RISK`
- `DOC_UPDATE_REQUIRED`
- `CLOSED`

`ACCEPTED_CANDIDATE`와 `ACCEPTED_PENDING_SOURCE_MIRROR_SYNC`는 terminal closed가 아니다.

## 15. reject cause taxonomy

- `COMMAND_AMBIGUOUS`
- `COMMAND_OVERBROAD`
- `EXECUTOR_SCOPE_CREEP`
- `EXECUTOR_MISREAD_BASELINE`
- `EXECUTOR_REPORT_INCOMPLETE`
- `EXPORT_ARTIFACT_INCOMPLETE`
- `HUMAN_QA_RUNTIME_GAP`
- `POLICY_BASELINE_MISSING`
- `POLICY_BASELINE_CONFLICT`
- `DIRTY_WORKSPACE_MIXED`
- `SOURCE_MIRROR_SYNC_MISSING`
- `SOURCE_MIRROR_METADATA_INVALID`
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`
- `PROOF_TYPE_SUBSTITUTION`
- `HUMAN_OWNED_EVIDENCE_FALSE_CLAIM`
- `FORBIDDEN_ACTION_EXECUTED`
- `SECURITY_BOUNDARY_VIOLATION`
- `STATE_TRANSITION_AUTHORITY_VIOLATION`
- `PUBLIC_PROVENANCE_INCOMPLETE`

## 16. judgment persistence

- Browser chat: 짧은 판정과 다음 행동
- `tasks/done`: AI에게 준 exact instruction
- `records/aiscc/cycles`: 실행·evidence·human·judgment·next action
- Git commit/diff: 실제 변경

Cycle Record는 accepted-only가 아니다.

`NEXT_ACTIONS.md`는 per-turn log가 아니라 stable roadmap이다. 매 turn 결과는 Cycle에 남긴다.

## 17. source mirror sync

```text
canonical 변경
→ tracked manifest 갱신
→ ignored bundle 생성
→ hash/file-count 검증
→ temporary target 제출
→ Command Center 판정
→ ACCEPTED_PENDING_SOURCE_MIRROR_SYNC
→ 사람 complete active set replacement
→ 사람 sync 완료 보고
→ cycle 갱신
→ ACCEPTED / CLOSED
```

## 18. Self-Dogfooding mode

Self-dogfooding task는 다음을 추가 기록한다.

- orchestrator version/commit
- initial state
- transition trace
- transition admission reason
- Agent claim과 admitted evidence 구분
- human gate
- fallback/manual intervention
- final Cycle/commit mapping

AISCC가 자신의 workflow를 실행했다는 이유만으로 자동 accepted하지 않는다. 일반 Task/Evidence/Judgment 기준을 동일하게 적용한다.
