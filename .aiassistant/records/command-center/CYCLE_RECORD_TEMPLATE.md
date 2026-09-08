# AISCC Repository Canonical Metadata

- canonical_owner: `AISCC_REPOSITORY`
- authority: `REPOSITORY_LOCAL_CANONICAL`
- bootstrap_origin: `AISCC-BOOTSTRAP-SEED-V1`
- canonicalized_by_task: `20260826_1108_aiscc-p0-4-canonical-authority-metadata-and-post-bootstrap-state-normalization-rework-2`

---


# AISCC Cycle Record Template

## 1. 목적

Cycle Record는 raw chat log나 raw executor report가 아니다.

다음 AI와 사람이 재사용할 수 있도록 아래를 압축한다.

```text
무엇을 지시했는가
→ 실제 무엇이 일어났는가
→ 어떤 proof가 admitted/rejected 되었는가
→ 사람이 무엇을 판단했는가
→ 왜 accept/rework/block했는가
→ 무엇을 다음 행동으로 선택했는가
```

Cycle은 accepted-only 기록이 아니다.

권장 경로:

```text
.aiassistant/records/aiscc/cycles/YYYYMMDD_HHmm_<safe-slug>.cycle.md
```

## 2. template

```markdown
# AISCC Cycle Record

## meta

- cycle_id:
- date:
- primary_semantic_owner:
- affected_areas:
- work_type:
- execution_mode: MANUAL_COMMAND_CENTER / AISCC_SELF_DOGFOOD
- task_file:
- task_done_path:
- temporary_target_bundle:
- result_status:
- reject_cause:
- cycle_record_action:
- source_mirror_sync: not-required / pending / confirmed
- fresh_ide_executor_chat_for_successor: REQUIRED / NOT_REQUIRED
- fresh_ide_executor_chat_reason: <reason or none>
- browser_session_action: CONTINUE_CURRENT_BROWSER_SESSION / ROTATE_BROWSER_SESSION
- handoff_required: Yes / No
- canonical_cycle_path:

## product/repository snapshot

- repository:
- branch:
- base_commit:
- result_commit_or_candidate:
- workspace_before:
- workspace_after:

## command summary

## Command Center artifact transport

- applicability: NOT_APPLICABLE / REQUIRED
- issued_artifacts: <TASK / CYCLE / JUDGMENT / HANDOFF subset or none>
- flat_zip_provided: Yes / No / NOT_APPLICABLE
- source_root: `C:\Users\oracl\Downloads` / NOT_APPLICABLE
- expected_hash_verification: PASS / FAIL / NOT_APPLICABLE
- destination_hash_verification: PASS / FAIL / NOT_APPLICABLE
- downloads_flat_source_cleanup: PASS / FAIL / NOT_APPLICABLE
- zip_cleanup: NOT_RUN
- transport_result: PASS / STOP / NOT_APPLICABLE
- substantive_execution_started_after_pass: Yes / No / NOT_APPLICABLE

## task contract summary

- goal:
- non_goals:
- allowed_scope:
- forbidden_scope:
- evidence_profile:
- executor_required:
- reuse_allowed:
- human_owned:
- not_required:
- forbidden:

## executor result summary

### product source changes

- none

### governance/provenance changes

- none

### repository configuration changes

- none

## evidence results

### executed

- classification: EXECUTED_PASS / EXECUTED_FAIL
  channel:
  scope:
  result:
  artifact_or_command:

### reused

- classification: REUSED_ACCEPTED
  predecessor:
  provenance:
  applicability:

### human_pending

- classification: HUMAN_PENDING
  channel:
  scope:

### human_provided

- classification: HUMAN_PROVIDED
  result_source:
  result:

### not_required

- classification: NOT_REQUIRED
  reason:

### forbidden_not_run

- classification: FORBIDDEN_NOT_RUN
  action:

### blocked_required

- classification: BLOCKED_REQUIRED_EVIDENCE
  blocker:

## proof admission

- Agent claims:
  - none
- admitted evidence:
  - none
- rejected claims/evidence:
  - none
- proof type substitution detected: No
- freshness/provenance issue:
  - none

## state transition trace

- applicability: NOT_APPLICABLE / REQUIRED
- orchestrator_version_or_commit: NOT_APPLICABLE
- initial_state:
- transitions:
  - from:
    to:
    requested_by:
    admitted_by: SYSTEM / HUMAN / NOT_APPLICABLE
    admission_reason:
    evidence_refs:
- denied_transitions:
  - none
- retry_or_rework_count:
- manual_fallback_or_intervention:
  - none

## implemented conformance

- applicability: NOT_REQUIRED / REQUIRED
- applicable policy_or_invariant:
- actual_owner:
- architecture_conformance: MATCHED / ACCEPTABLE_DEVIATION / REWORK_REQUIRED / NOT_APPLICABLE
- planned_vs_actual_deviation:
- rollback_or_failure_semantics:
- unresolved:
  - none

## mandatory stop / scope expansion

- mandatory_stop_triggered: Yes / No
- blocker:
- minimal_evidence_after_stop:
- prohibited_follow_on_execution_absent: Yes / No
- evidence_scope_expansion: none / EVIDENCE_SCOPE_EXPANSION_REQUIRED
- follow_up:

## human verification

- owner: human
- channel:
- scope:
- status: HUMAN_PENDING / HUMAN_PROVIDED / NOT_REQUIRED
- result_source:
- notes:

## command-center judgment

- result_status:
- accepted_scope:
- required_rework:
- blocked_reason:
- evidence_contract_satisfied:
- forbidden_action_absent:
- proof_non_substitution_satisfied:
- transition_authority_satisfied:
- security_boundary_satisfied:
- public_provenance_satisfied:
- terminal_decision_reason:

## source mirror sync

- required: Yes / No
- status: not-required / pending / confirmed
- changed_canonical_files:
  - none
- manifest:
- generated_bundle:
- active_file_count:
- hash_verification:
- human_project_source_upload_confirmed: No
- confirmed_at:

## preserved artifacts

다음 turn/cleanup 이후에도 보존해야 하는 exact path만 적는다.

- `.aiassistant/tasks/done/<task>.md`
- `.aiassistant/records/aiscc/cycles/<cycle>.cycle.md`
- <canonical report/baseline if any>

명시하지 않은 temporary target/export 파일은 삭제 가능한 것으로 본다.

## public provenance mapping

- task:
- cycle:
- commits:
- pull_request_or_release:
- demo_or_submission_reference:
- sensitive_data_check:

## reusable lessons

## rule update candidates

## next action

next_action:
- work_type:
- title:
- reason:
- blocker:
- required_baseline:
- human_verification_needed:
```

## 3. 작성 원칙

- Task 전문은 `tasks/done`에 있으므로 Cycle에 불필요하게 중복하지 않는다.
- temporary target report 전문을 복사하지 않는다.
- Agent claim과 admitted evidence를 구분한다.
- human-owned result가 없으면 `HUMAN_PENDING`을 유지한다.
- rejected/blocked/hold도 다음 판단에 영향을 주면 기록한다.
- self-dogfooding은 execution mode와 transition trace를 반드시 남긴다.
- 민감정보, token, credential, private source를 public Cycle에 넣지 않는다.
- fresh IDE successor decision, Browser session action, Handoff requirement를 서로 독립적으로 기록한다.
- Cycle 생성만으로 Browser rotation 또는 Handoff를 추론하지 않는다.
