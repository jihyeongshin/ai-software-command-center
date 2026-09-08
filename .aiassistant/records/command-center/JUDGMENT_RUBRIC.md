# AISCC Repository Canonical Metadata

- canonical_owner: `AISCC_REPOSITORY`
- authority: `REPOSITORY_LOCAL_CANONICAL`
- bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
- canonicalized_by_task: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`

---


# AISCC Judgment Rubric

## 1. target bundle 구성

Task 기반 작업의 필수 root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`

확인:

- target path와 task timestamp/slug 대응
- changed file의 project-relative path 보존
- 삭제가 있을 때만 `REMOVED_FILES.md`
- previous target/unchanged source/private artifact 미포함

## 2. 범위 일치

- Task 목표와 actual change가 일치하는가
- allowed/forbidden path를 지켰는가
- unrelated dirty source가 섞이지 않았는가
- product source / governance provenance / repository configuration을 구분했는가
- mandatory stop 뒤 불필요한 실행이 계속되지 않았는가

## 3. instruction transport / authority

해당 task에만 적용한다.

- auto-discovered와 explicit tool-read inventory가 분리되었는가
- fresh-session evidence 없이 newly-created instruction을 auto-discovered로 소급하지 않았는가
- root instruction이 thin bootstrap인가
- Task must-read list를 minimum authoritative context set으로 사용했는가
- transport precedence를 project authority로 오해하지 않았는가
- conflict가 있을 때 implementation을 중단했는가

## 4. evidence contract

- Task 실행 전 five-way ownership이 정의되었는가
- `executor_required`가 실제 result 또는 `BLOCKED_REQUIRED_EVIDENCE`인가
- `reuse_allowed` provenance와 applicability가 맞는가
- `human_owned`가 `HUMAN_PENDING`/`HUMAN_PROVIDED`로 정직한가
- `not_required`를 gap으로 오판하지 않았는가
- `forbidden` action이 실행되지 않았는가
- Agent claim과 admitted evidence를 구분했는가
- freshness/current changed-path 조건을 확인했는가

## 5. proof non-substitution

다음 위반은 HOLD/REJECT 후보다.

- unit test를 runtime/integration proof로 주장
- generated HTTP artifact를 실제 server execution으로 주장
- source test를 browser QA로 주장
- checklist를 human verification으로 주장
- executor report를 human acceptance로 주장
- security test 하나로 sandbox runtime boundary 전체를 주장
- predecessor evidence를 current changed path proof로 무조건 대체

reject cause:

```text
PROOF_TYPE_SUBSTITUTION
HUMAN_OWNED_EVIDENCE_FALSE_CLAIM
```

## 6. state transition authority

orchestration/self-dogfooding task에 적용한다.

- Agent가 next/terminal state를 직접 확정하지 않았는가
- system transition engine이 precondition/evidence/policy를 평가했는가
- transition admission reason이 기록되었는가
- denied transition이 silent success로 바뀌지 않았는가
- human-required state를 Agent result만으로 통과하지 않았는가
- rework retry bound 또는 failure 의미가 명시되었는가

위반:

```text
STATE_TRANSITION_AUTHORITY_VIOLATION
```

## 7. security/sandbox

해당 task에 적용한다.

- host filesystem/network/process/credential 경계가 task와 baseline에 맞는가
- forbidden command 또는 remote action이 실행되지 않았는가
- secret candidate를 값까지 report/log에 노출하지 않았는가
- ambiguous permission을 fail-open하지 않았는가
- container/worktree cleanup과 residue가 확인되었는가

위반:

```text
SECURITY_BOUNDARY_VIOLATION
BLOCKED_SECURITY_RISK
```

## 8. public provenance

- Task File이 `tasks/done`으로 보존 가능한가
- Cycle Record가 terminal judgment를 충분히 재구성하는가
- commit/diff와 task/cycle mapping이 있는가
- temporary target path를 장기 evidence 정본으로만 의존하지 않는가
- self-dogfooding이면 orchestrator version/transition trace/human intervention을 기록했는가
- 민감정보/회사 기밀/credential이 공개 provenance에 없는가

## 9. Project Source mirror

- tracked manifest와 active list가 일치하는가
- generated bundle actual file count가 일치하는가
- filename/metadata/canonical path가 맞는가
- canonical body와 mirror body hash가 일치하는가
- optional/on-demand가 active set에 섞이지 않았는가
- Bootstrap Seed와 repository mirror가 동시에 active authority로 남지 않는가
- 사람이 complete active set replacement를 보고했는가

사람 업로드 전:

```text
ACCEPTED_PENDING_SOURCE_MIRROR_SYNC
```

## 10. dirty workspace

`DIRTY_WORKSPACE_MIXED` 후보:

- unrelated modified/untracked file이 current task와 섞임
- working-tree/HEAD representation이 불명확함
- `.gitignore` 변경이 task 범위 밖임
- generated target/bundle이 product change로 보고됨

## 11. successor session / Handoff decision

다음 세 field를 judgment마다 명시한다.

- `fresh_ide_executor_chat_for_successor`: `REQUIRED / NOT_REQUIRED`
- `browser_session_action`: `CONTINUE_CURRENT_BROWSER_SESSION / ROTATE_BROWSER_SESSION`
- `handoff_required`: `Yes / No`

fresh IDE decision은 successor Task의 explicit authority/context boundary로 판단한다. `REQUIRED`이면 Browser response가 Short Prompt 위에서 Human에게 exact fresh-chat notice와 이유를 표시하는지 확인한다. Human이 새 IDE chat을 열며 Short Prompt는 Executor에게 chat 생성을 지시하지 않는다.

Browser rotation과 Handoff는 실제 Browser-session boundary가 있을 때만 선택한다. Cycle 생성 자체는 Browser session termination이나 Handoff 요구의 근거가 아니다.

## 12. cycle record action

`create`:

- ACCEPTED
- ACCEPTED_PENDING_SOURCE_MIRROR_SYNC
- PARTIAL_ACCEPTED
- HOLD_REWORK_REQUIRED
- REJECTED_ROLLBACK_REQUIRED
- BLOCKED_POLICY_GAP
- BLOCKED_MISSING_ARTIFACT
- BLOCKED_SECURITY_RISK
- DOC_UPDATE_REQUIRED
- 다음 행동에 영향을 주는 terminal judgment

`update`:

- pending human verification이 terminal result로 바뀜
- mirror sync가 confirmed 됨
- rework 결과가 기존 cycle lineage를 보강함

`skip`:

- exploratory comment만 존재
- terminal judgment 전 중간 질문
- 저장할 evidence가 불충분

`cycle_record_action=create`에서 `browser_session_action` 또는 `handoff_required`를 자동 추론하지 않는다.

## 13. result 출력 template

```markdown
판정: <result_status>

work_type: <work_type>
reject_cause: <cause or none>
cycle_record_action: create / update / skip
cycle_record_path: .aiassistant/records/aiscc/cycles/<cycle>.cycle.md or none
source_mirror_sync: not-required / pending / confirmed
execution_mode: MANUAL_COMMAND_CENTER / AISCC_SELF_DOGFOOD
fresh_ide_executor_chat_for_successor: REQUIRED / NOT_REQUIRED
browser_session_action: CONTINUE_CURRENT_BROWSER_SESSION / ROTATE_BROWSER_SESSION
handoff_required: Yes / No

accepted scope:
-

required rework:
-

human verification:
-

public provenance:
-

next action:
-
```
