# AISCC Repository Canonical Metadata

- canonical_owner: `AISCC_REPOSITORY`
- authority: `REPOSITORY_LOCAL_CANONICAL`
- bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
- canonicalized_by_task: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`

---


# AISCC Task File Template

## 1. 사용 목적

Task File은 Agent에게 전달하는 장문 작업 계약이다. Browser chat에 전문을 반복 출력하지 않는다.

파일명:

```text
YYYYMMDD_HHmm_<safe-slug>.md
```

## 2. template

````markdown
# 작업지시서: <작업명>

## meta

- task_id:
- created_at:
- work_type:
- evidence_profile: BASIC / STANDARD / HIGH_RISK
- execution_mode: MANUAL_COMMAND_CENTER / AISCC_SELF_DOGFOOD
- expected_orchestrator_version_or_commit: NOT_APPLICABLE / <value>
- primary_semantic_owner:
- fresh_ide_executor_chat: REQUIRED / NOT_REQUIRED
- fresh_ide_executor_chat_reason: <reason or none>
- browser_session_action: CONTINUE_CURRENT_BROWSER_SESSION / ROTATE_BROWSER_SESSION / NOT_APPLICABLE
- handoff_required: Yes / No

## 현재 상태

- current canonical baseline:
- predecessor cycle:
- known dirty workspace:
- open blocker:

## 이번 턴 목표

1.
2.
3.

## 이번 턴 비목표

-

## 허용 범위

allowed_paths:
-

allowed_actions:
-

## 절대 금지

forbidden_paths:
-

forbidden_actions:
- Git index / commit / push / deployment unless explicitly authorized
- credentialed external action unless explicitly authorized
- unrelated source or test broadening

## 읽을 문서

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- <task-specific exact canonical paths>

## agent instruction transport / authority

- repository-root instruction entrypoint는 transport bootstrap이며 policy authority가 아니다.
- Project Rules UI 또는 automatic retrieval만으로 canonical body가 Agent에 전달됐다고 가정하지 않는다.
- 위 목록은 minimum authoritative context set이다.
- unrelated rules/records/source/logs를 bulk-read하지 않는다.
- active Task File, canonical rule, current source, accepted evidence가 충돌하면 구현을 중단하고 conflict investigation으로 보고한다.
- human-owned evidence를 executor-completed로 주장하지 않는다.

## session / delivery boundary

이 section은 session 또는 issued artifact transport가 실제로 관련될 때만 채운다.

- fresh IDE chat은 explicit authority/context boundary가 있을 때만 `REQUIRED`다.
- `REQUIRED`이면 Browser response가 Short Prompt 위에서 Human에게 exact notice와 이유를 표시하고 Human이 새 chat을 연다.
- Short Prompt는 IDE Executor에게 chat을 만들거나 열라고 지시하지 않는다.
- fresh IDE session, Browser session rotation, Cycle issuance, Handoff issuance를 서로 자동 연동하지 않는다.
- issued_artifacts: NONE / TASK / CYCLE / JUDGMENT / HANDOFF 중 현재 존재하는 subset
- delivery_package: NONE / ONE_FLAT_ZIP
- source_root: `C:\Users\oracl\Downloads` / NOT_APPLICABLE
- delivery_zip_filename: <exact ZIP filename>
- bootstrap_integrity_anchor: <Browser Short Prompt의 expected delivery ZIP SHA-256>
- task_member_filename: <exact TASK filename>
- canonical_task_path: `.aiassistant/tasks/active/<TASK filename>`

## issued artifact manifest / transport contract

발행이 관련될 때 exact 상세 계약을 Task 안에 작성한다. Short Prompt에 이 section을 중복 출력하지 않는다. TASK 자신의 whole-file SHA는 요구하지 않으며 verified delivery ZIP hash를 bootstrap anchor로 사용한다.

- issued member별 type / exact filename / expected SHA-256 또는 authoritative hash source / exact canonical destination
- expected destination state와 differing bytes의 overwrite 허용 여부; differing done predecessor는 덮어쓰지 않음
- required repository branch / HEAD / tree / index / exact dirty-path set
- exact allowed actions / evidence / Git allowlist / export contract

Bootstrap: Human은 ZIP만 다운로드한다. Executor가 ZIP hash, archive readability/CRC/member safety를 검증하고 TASK member를 canonical tasks/active에 가장 먼저 직접 배치·검증하여 읽는다. 나머지는 이 manifest를 따라 archive member → exact canonical destination으로 직접 배치한다. 직접 member 배치가 불가능할 때만 package-specific staging을 사용한다.

나머지 artifact의 member 존재 → expected hash → destination 상태 → exact materialization → destination hash equality를 검증한다. member 경로 탈출과 모호한 member를 허용하지 않는다.

TASK 배치 전 ZIP missing/hash mismatch, archive failure, TASK missing/placement failure이면 STOP한다. report/export와 substantive project 작업을 하지 않고 ZIP을 보존하며 Human에게 재다운로드/재배치를 요청한다. canonical 배치 이후 required transport/repository 실패의 exact mandatory stop 규칙은 이 Task에 명시한다.

모든 artifact canonical transport PASS 이후 inbound ZIP/staging cleanup은 terminal outcome과 outbound ZIP 검증 뒤 best effort다. 거절은 `NON_BLOCKING_LOCAL_RESIDUE`로 exact 경로를 기록하고 substantive work/result를 유지한다. 같은 turn의 다른 삭제 수단 재시도와 broad Downloads cleanup은 금지한다.

## 조사할 source

- exact path / symbol / command:

## 구현/문서/감사 범위

-

## workflow transition expectation

- initial_state:
- expected_non_terminal_state_when_human_pending:
- expected_terminal_candidate:
- transition_authority: SYSTEM / NOT_APPLICABLE
- Agent가 직접 terminal state를 결정할 수 있는가: No

## evidence contract

executor_required:
- channel:
  scope:
  allowed_command_or_environment:
  pass_condition:

reuse_allowed:
- channel:
  predecessor:
  provenance_condition:
  applicability_condition:

human_owned:
- channel:
  scope:
  expected_result_format:

not_required:
- channel:
  reason:

forbidden:
- action_or_channel:
  reason:

proof_non_substitution:
- <proof A> != <proof B>

## conformance reporting

- applicability: NOT_REQUIRED / REQUIRED
- applicable policy_or_invariant:
- required_actual_owner:
- planned_vs_actual_scope:
- rollback_or_failure_semantics:

## project context impact

architecture:
- NOT_APPLICABLE / NONE / UPDATE_REQUIRED / INVESTIGATE

orchestration_contract:
- NOT_APPLICABLE / NONE / UPDATE_REQUIRED / INVESTIGATE

security_sandbox:
- NOT_APPLICABLE / NONE / UPDATE_REQUIRED / INVESTIGATE

public_provenance:
- TASK_AND_CYCLE_ONLY / CANONICAL_UPDATE_REQUIRED / INVESTIGATE

## accept 기준

-

## hold/reject 기준

-

## mandatory stop 조건

- policy baseline conflict
- missing required artifact
- dirty workspace collision
- forbidden action/tool request
- security boundary uncertainty
- EVIDENCE_SCOPE_EXPANSION_REQUIRED
- human decision required before further mutation

named blocker 이후에는 최소 source evidence, workspace inventory, report/export와 안전한 종료만 수행한다.

## 보고서 필수 항목

- 작업명 / work type / task path
- read canonical paths
- source inventory
- product source changes
- governance/provenance changes
- repository configuration changes
- evidence contract와 실제 result classification
- Agent claim vs admitted evidence 구분 when applicable
- human pending/provided
- forbidden-not-run
- mandatory stop/scope expansion
- planned-vs-actual conformance when required
- self-dogfooding transition trace when applicable
- unverified items
- rollback/revert guide
- preserved artifact exact paths

## export bundle 요구

Target:
`.aiassistant/reports/target/YYYYMMDD_HHmm_<safe-slug>/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- changed files preserving project-relative paths
- `REMOVED_FILES.md` only when deletion exists

Folder 완성 후 인접 `.aiassistant/reports/target/<bundle-name>.zip`을 자동 생성한다. 정확히 하나의 최상위 `<bundle-name>/` 아래 전체 내용과 relative layout을 보존하며 readability/CRC, required root, folder/archive 목록·내용 일치를 검증한다. 원본 folder는 보존한다. 실패는 `ZIP_EXPORT_FAILED`이며 export 완료를 주장하지 않는다. `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`를 따른다.

## 사람 검증 요구

-

## 최종 응답 형식

1. result: completed / blocked / rejected-candidate
2. target bundle folder path와 검증된 outbound ZIP path
3. changed files
4. removed files
5. human verification
6. unverified items
````

## 3. 작성 규칙

- 비적용 evidence를 채우기 위해 실행 범위를 넓히지 않는다.
- `human_owned` pending은 executor failure가 아니다.
- `not_required`는 evidence gap이 아니다.
- predecessor evidence는 provenance와 changed-path 적용 조건이 맞을 때만 재사용한다.
- 작은 task에 불필요한 owner/invariant를 강제하지 않는다.
- self-dogfooding task도 일반 accept/reject 기준을 우회하지 않는다.
- simple Task에서 의미 없는 session/delivery field를 억지로 확장하지 않고 `NOT_APPLICABLE` 또는 section 생략을 사용한다.
