# AISCC Bootstrap Seed Metadata

- seed_id: `AISCC-BOOTSTRAP-SEED-V1`
- generated_at: `2026-08-26 00:07 KST`
- seed_role: `PRE_REPOSITORY_BROWSER_PROJECT_BOOTSTRAP`
- authority: `TEMPORARY_BOOTSTRAP_AUTHORITY`
- immutable_after_upload: `true`
- retirement_condition: `FIRST_AISCC_REPOSITORY_CANONICAL_MIRROR_V1_SYNC_CONFIRMED`
- domain_leakage_policy: `NO_SOURCE_PROJECT_PRODUCT_OR_DOMAIN_POLICY`

---


# AISCC Command Center Records

## 1. 목적

이 문서군은 Browser Command Center가 Task File을 만들고, IDE Executor 결과를 판정하고, Cycle Record와 Next Action을 관리하기 위한 always-on playbook이다.

이 문서들은 selected coding agent에게 자동 전달되는 instruction이라고 가정하지 않는다. Browser Command Center에는 운영 기준이고, IDE Executor에는 active Task File이 명시한 경우 exact path로 전달한다.

## 2. 표준 artifact chain

```text
Task File
→ Executor Report / temporary target bundle
→ Command Center Judgment
→ Curated Cycle Record
→ Stable Next Action
```

장문 지시는 Task File에 두고 Browser chat에는 download link, active path, short prompt, 핵심 주의사항만 둔다.

## 3. 파일 역할

- `COMMAND_CENTER_WORKFLOW.md`: 표준 cycle, work type, evidence/result taxonomy
- `TASK_FILE_TEMPLATE.md`: Task Contract 형식
- `SHORT_EXECUTOR_PROMPT_TEMPLATE.md`: IDE에 붙여넣는 짧은 실행 prompt
- `JUDGMENT_RUBRIC.md`: target bundle과 evidence 판정 기준
- `CYCLE_RECORD_TEMPLATE.md`: terminal judgment와 public provenance 기록
- `NEXT_ACTION_SELECTION_RUBRIC.md`: blocker/rework/baseline/core/release 우선순위

## 4. Task-scoped evidence model

모든 task에 동일한 test/DB/HTTP/browser checklist를 강제하지 않는다.

Task File은 실행 전에 다음을 구분한다.

- `executor_required`
- `reuse_allowed`
- `human_owned`
- `not_required`
- `forbidden`

Executor Report는 실제 결과만 다음처럼 분류한다.

- `EXECUTED_PASS`
- `EXECUTED_FAIL`
- `REUSED_ACCEPTED`
- `HUMAN_PROVIDED`
- `HUMAN_PENDING`
- `NOT_REQUIRED`
- `FORBIDDEN_NOT_RUN`
- `BLOCKED_REQUIRED_EVIDENCE`

## 5. AI / System / Human boundary

Browser Command Center는 Agent의 완료 문장을 terminal truth로 받아들이지 않는다.

```text
Agent claim
→ applicable evidence 확인
→ proof type/owner 확인
→ system admission
→ judgment
→ human gate when required
```

## 6. public provenance 정책

repository 생성 후 다음은 Git으로 보존한다.

- `.aiassistant/rules/**`
- `.aiassistant/records/command-center/**`
- `.aiassistant/records/aiscc/**`
- `.aiassistant/tasks/done/**`
- `.aiassistant/reports/aiscc/**` 중 curated baseline/handoff
- `.aiassistant/project-sources/manifests/**`
- `.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md`

다음은 생성/임시 artifact로 기본 ignore한다.

- `.aiassistant/tasks/active/**`
- `.aiassistant/reports/target/**`
- `.aiassistant/project-sources/bundles/**`

`tasks/done`은 accepted task 목록이 아니다. completed, blocked, failed, rejected-candidate executor turn도 제출 준비가 끝났다면 보존될 수 있다.

`cycles`는 accepted-only 기록이 아니다. 다음 작업 선택에 영향을 주는 terminal judgment를 보존한다.

## 7. source mirror boundary

- local repository canonical이 정본이다.
- Browser Project Source는 read-only mirror다.
- generated bundle은 Git provenance가 아니라 upload staging artifact다.
- manifest/registry와 mirror-sync cycle이 어떤 active set을 업로드했는지 증명한다.
- 모든 `tasks/done`과 `cycles`를 active Project Source에 자동 업로드하지 않는다.

## 8. judgment record

Browser chat은 짧은 판정과 다음 행동만 전달한다.

장기 재사용 정보는 다음에 둔다.

```text
.aiassistant/records/aiscc/cycles/YYYYMMDD_HHmm_<safe-slug>.cycle.md
```

Cycle Record에는 task, evidence, human decision, judgment, commit mapping, next action, self-dogfooding 여부를 기록한다.

## 9. Self-Dogfooding 표시

Cycle마다 execution mode를 기록한다.

```text
MANUAL_COMMAND_CENTER
AISCC_SELF_DOGFOOD
```

Self-dogfooding mode라면 orchestrator version/commit, transition trace, evidence admission result, human gate를 기록한다.

## 10. 관련 경로

- `.aiassistant/rules/`: canonical executor/project rule
- `.aiassistant/tasks/active/`: current temporary Task File
- `.aiassistant/tasks/done/`: public task instruction provenance
- `.aiassistant/reports/target/`: ignored temporary submission bundle
- `.aiassistant/records/aiscc/cycles/`: public curated work/judgment provenance
- `.aiassistant/reports/aiscc/`: curated baseline/reference
- `.aiassistant/project-sources/manifests/`: tracked mirror definition
- `.aiassistant/project-sources/bundles/`: ignored generated upload copy
