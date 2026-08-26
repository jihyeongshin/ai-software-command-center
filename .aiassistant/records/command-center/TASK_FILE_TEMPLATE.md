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

```markdown
# 작업지시서: <작업명>

## meta

- task_id:
- created_at:
- work_type:
- evidence_profile: BASIC / STANDARD / HIGH_RISK
- execution_mode: MANUAL_COMMAND_CENTER / AISCC_SELF_DOGFOOD
- expected_orchestrator_version_or_commit: NOT_APPLICABLE / <value>
- primary_semantic_owner:

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

## 사람 검증 요구

-

## 최종 응답 형식

1. result: completed / blocked / rejected-candidate
2. target bundle path
3. changed files
4. removed files
5. human verification
6. unverified items
```

## 3. 작성 규칙

- 비적용 evidence를 채우기 위해 실행 범위를 넓히지 않는다.
- `human_owned` pending은 executor failure가 아니다.
- `not_required`는 evidence gap이 아니다.
- predecessor evidence는 provenance와 changed-path 적용 조건이 맞을 때만 재사용한다.
- 작은 task에 불필요한 owner/invariant를 강제하지 않는다.
- self-dogfooding task도 일반 accept/reject 기준을 우회하지 않는다.
