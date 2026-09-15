# 작업지시서: P3-1 Comparative Evaluation Protocol Freeze — Manual Rework

## meta

- task_id: `20260915_0054_aiscc-p3-1-comparative-evaluation-protocol-freeze-manual-rework-1`
- created_at: `2026-09-15T00:54:00+09:00`
- phase: `P3-1 Comparative Evaluation`
- work_type: `REWORK`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `Comparative Evaluation Contract / Claim Boundary`
- fresh_ide_chat_required: `No`

## 현재 상태

- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- expected repository HEAD: `82bc047b79cf496280d1b3df6a113f652629a6f5`
- predecessor blocked Task: `.aiassistant/tasks/done/20260915_0033_aiscc-p3-1-comparative-evaluation-protocol-freeze-and-minimum-matrix-1.md`
- predecessor blocked Cycle: `.aiassistant/records/aiscc/cycles/20260915_0054_aiscc-p3-1-protocol-freeze-entry-contract-blocked-rework-authorization-1.cycle.md`
- predecessor Browser judgment: `.aiassistant/reports/aiscc/20260915_0054_aiscc-p3-1-protocol-freeze-entry-contract-blocked-browser-judgment-1.md`
- rework handoff: `.aiassistant/reports/aiscc/20260915_0054_aiscc-browser-command-center-p3-1-protocol-freeze-manual-rework-entry-handoff-1.md`
- P2-4/P2: `ACCEPTED / CLOSED`; do not reopen
- P3-1 comparative evaluation: `NOT_COMPLETED`
- open blocker: none after this corrected execution-mode contract

## 0033 correction boundary

0033의 comparative methodology 자체는 유지한다.

수정하는 것은 오직 다음 entry contract다.

```text
BEFORE:
execution_mode = AISCC_SELF_DOGFOOD
+ current owner-backed WorkRun issuance required
+ no current runtime continuation contract supplied

AFTER:
execution_mode = MANUAL_COMMAND_CENTER
+ protocol pre-registration/document audit only
+ no self-dogfood WorkRun issuance required
```

이 manual execution은 다음을 의미하지 않는다.

```text
manual protocol authoring != comparative result
manual protocol authoring != P2 self-dogfood invalidation
manual protocol authoring != proof that AISCC is superior
```

## 이번 턴 목표

1. 실제 P3-1 comparative result 실행 전에 canonical comparative evaluation protocol candidate를 고정한다.
2. accepted P2-3/P2-4 corpus에서 재실행 없이 사용할 최소 comparison matrix를 exact scenario/run/path/ref로 고정한다.
3. `AISCC_GOVERNED` 대 `EXECUTOR_REPORT_BASELINE` synthetic ablation의 comparator semantics, metrics, success/failure/exclusion, matched-condition, reproducibility, claim ceiling을 고정한다.
4. accepted corpus에 요구 class가 없으면 새 run을 만들지 않고 `CORPUS_GAP`으로 기록한다.
5. 다음 comparative execution Task가 결과를 보기 전 이 protocol을 변경하지 못하도록 unresolved item과 amendment rule을 명시한다.

## 이번 턴 비목표

- comparative score/result 계산
- P2 scenario 재실행
- provider/LLM/network/browser/deployment/credentialed action
- DB/runtime harness 생성 또는 self-dogfood WorkRun issuance
- competitor direct benchmark
- product/runtime/scenario fixture/API/UI/schema 수정
- P3-2/P3-3 작성
- Git add/commit/push

## primary evaluation question

```text
Does explicit governance authority + evidence admission + deterministic state ownership
produce materially better truthfulness, auditability, and failure behavior
than an agent/executor workflow without those controls?
```

이번 Task는 답을 계산하지 않는다. 측정 계약만 freeze한다.

## comparator contract

### `AISCC_GOVERNED`

accepted AISCC semantics를 그대로 사용한다.

최소 요소:
- TaskContract authority/scope
- task-scoped evidence ownership
- EvidenceCandidate vs AdmittedEvidence
- proof type/owner/freshness/provenance/applicability
- System-owned transition admission
- designated Human ownership when applicable
- Judgment separation
- durable Cycle/history
- deterministic current NextAction/state projection

### `EXECUTOR_REPORT_BASELINE`

평가용 synthetic ablation이다.

- 동일 Task/scenario input과 동일 executor-produced attempt/output/artifact를 사용한다.
- executor completion/report와 conventional task result만으로 완료/다음 행동을 해석한다.
- AISCC evidence admission, proof-owner/type gate, system transition admission, HumanGate admission, curated Cycle admission을 comparator decision에는 사용하지 않는다.
- source artifact를 수정하거나 unsafe action을 재실행하지 않는다.

필수 label:

```text
SYNTHETIC_ABLATION_ONLY
NOT_A_COMPETITOR_PRODUCT
NOT_AN_INDUSTRY_STANDARD_CLAIM
```

baseline을 특정 vendor behavior로 서술하거나 AISCC에 유리하도록 source Task/output을 삭제·변형하지 않는다.

## accepted corpus selection

accepted P2-3/P2-4 corpus만 사용한다.

current canonical state/decision/cycle에서 exact ref를 따라 다음 class를 가능한 범위에서 각각 하나씩 선택한다.

- valid evidence → accepted
- missing/wrong-type/wrong-owner evidence → deny/rework
- policy/authority conflict → blocked/human-required/fail-closed
- human-owned proof false-completion attempt → human-pending/reject

accepted corpus에 class가 없으면 `CORPUS_GAP`으로 기록한다. 새 run으로 채우지 않는다.

각 frozen row:
- `scenario_id`
- source Task/WorkRun/Cycle/result ref
- source path/hash/stable ID where available
- why selected
- available artifacts
- comparator matched-condition status
- known limitation

## matched-condition invariant

pairwise result를 허용하려면:

```text
same task/scenario input
+ same executor-produced attempt/output
+ same candidate evidence/artifacts
+ same source/version identity
→ only governance interpretation/admission path differs
```

동일 underlying attempt가 아니면 `NOT_COMPARABLE`.

## metric contract

### primary

1. `TRUTHFUL_TERMINAL_OUTCOME` — `PASS / FAIL / NOT_APPLICABLE`
2. `EVIDENCE_INTEGRITY` — wrong type/owner/freshness/provenance/applicability 또는 silent substitution이면 `FAIL`
3. `AUTHORITY_SEPARATION` — Agent/Executor output이 System state/Human proof/Judgment/terminal transition을 직접 소유하면 `FAIL`
4. `FAIL_CLOSED_BEHAVIOR` — missing/conflicting/stale/unauthorized input에서 false success/unsafe mutation 대신 deny/block/rework가 남는지
5. `AUDIT_RECONSTRUCTABILITY` — applicable fixed fields 재구성 비율

fixed fields:
`task`, `scope/authority`, `execution result`, `evidence candidate`, `evidence admission`, `human input when applicable`, `judgment`, `transition decision/state`, `cycle/history`, `next action`, `result commit/ref`.

### secondary

6. `RESTART_RECOVERABILITY`
7. `HISTORICAL_TRUTH_PRESERVATION`
8. `DETERMINISTIC_PROJECTION`
9. `GOVERNANCE_OVERHEAD` — recorded comparable data만; 아니면 `NOT_COMPARABLE`

## aggregate/result rule

- raw scenario metric 먼저 보존
- small-N weighted composite superiority score 금지
- metric별 pass-rate/count 사용 시 denominator/N/A 병기
- qualitative finding은 exact artifact ref 필요
- `materially better` 후보 표현은 후속 result Task에서 반복 방향성 + 반대 regression 부재가 실제 관측될 때만 검토
- 이번 Task에서 result 값 생성 금지

## success/failure/exclusion

scenario success:
- expected invariant가 applicable artifact로 관측되고 contradictory admitted artifact가 없음

scenario failure:
- false terminal completion
- wrong-owner/wrong-type admission
- authority collapse
- fail-open mutation
- applicable provenance reconstruction failure

허용 exclusion만:
- required accepted source artifact 없음
- metric structurally N/A
- matched underlying artifact 불가
- source integrity/hash/provenance 검증 불가

outcome filtering 목적 exclusion 금지.

## claim ceiling

protocol에 exact 포함:

```text
protocol != comparative result
accepted P2 capability evidence != comparative superiority evidence
self-dogfooding != independent validation
synthetic ablation != competitor benchmark
small bounded corpus != generalization across repositories/providers/languages
```

P3-1 result acceptance 전 금지:
- `AISCC is superior`
- `AISCC is safer/more accurate/more productive than competing products`
- `proven to reduce operator burden`
- worldwide first/only/unique claim

## amendment rule

Protocol freeze 뒤 metric/comparator/exclusion/matrix를 바꾸려면:

- result를 보기 전 발견된 source-integrity defect 또는 명백한 contract bug여야 한다.
- exact reason과 before/after를 별도 Cycle에 남긴다.
- result를 유리하게 만드는 post-hoc 변경은 금지한다.

## 허용 범위

allowed_paths:
- `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`
- `.aiassistant/tasks/active/20260915_0054_aiscc-p3-1-comparative-evaluation-protocol-freeze-manual-rework-1.md`
- `.aiassistant/tasks/done/20260915_0054_aiscc-p3-1-comparative-evaluation-protocol-freeze-manual-rework-1.md`
- `.aiassistant/reports/target/20260915_0054_aiscc-p3-1-comparative-evaluation-protocol-freeze-manual-rework-1/**`

allowed_actions:
- exact canonical read
- current canonical refs를 따라 narrow P2 corpus inventory
- SHA-256/Git status/Git diff inspection
- single protocol candidate create/update
- UTF-8/control-character/Markdown validation
- `git diff --check`
- report/export

## 절대 금지

forbidden_paths:
- product/runtime implementation source mutation
- P2 scenario/fixture mutation
- DB migration/schema
- deployment/config
- secret/private data
- `.gitignore`

forbidden_actions:
- AISCC self-dogfood TaskContract/WorkRun issuance for this Task
- DB/runtime harness start/recovery/reconstruction
- provider/LLM/external network/browser/deployment/credentialed action
- scenario rerun
- competitor benchmark
- comparative scoring/result/superiority claim
- Git add/commit/push
- broad cleanup/reset

## 읽을 문서

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
- `.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md`
- `.aiassistant/tasks/done/20260915_0033_aiscc-p3-1-comparative-evaluation-protocol-freeze-and-minimum-matrix-1.md`
- `.aiassistant/records/aiscc/cycles/20260915_0054_aiscc-p3-1-protocol-freeze-entry-contract-blocked-rework-authorization-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_0054_aiscc-p3-1-protocol-freeze-entry-contract-blocked-browser-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_0054_aiscc-browser-command-center-p3-1-protocol-freeze-manual-rework-entry-handoff-1.md`

Task-listed current canonical refs가 exact P2-3/P2-4 artifact를 가리킬 때만 해당 exact path를 추가로 읽는다. unrelated history/source/log bulk-read 금지.

## canonical candidate

`.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`

필수 section:
1. document status / scope
2. primary evaluation question
3. non-goals and claim ceiling
4. comparator definitions and synthetic-ablation disclaimer
5. accepted corpus inventory
6. frozen minimum comparison matrix
7. primary/secondary metrics with exact scoring rules
8. success/failure/exclusion rules
9. matched-condition rule
10. reproducibility artifact contract
11. limitation / confidence boundary
12. result-publication rule
13. next bounded execution Task contract
14. unresolved corpus gaps
15. amendment rule

## workflow transition expectation

- applicability: `NOT_APPLICABLE for AISCC runtime`
- executor lifecycle remains Task active → report/export → Task done
- Browser Command Center owns acceptance
- Agent가 protocol acceptance를 직접 결정할 수 있는가: `No`

## evidence contract

executor_required:
- `STATIC_SOURCE`: expected HEAD/current canonical identity and exact P2 refs
- `PUBLIC_PROVENANCE`: every frozen matrix row has stable accepted source ref or explicit `CORPUS_GAP`
- `STATIC_SOURCE`: protocol required sections/labels/metric/exclusion/amendment completeness
- `STATIC_SOURCE`: UTF-8/Markdown/`git diff --check`

reuse_allowed:
- accepted P2-3 canonical scenario/replay corpus and P2-4 golden/failed lineage for existence/provenance only
- never as comparative superiority result

human_owned:
- Browser methodology judgment on fairness/non-cherry-picking/claim ceiling after protocol candidate

not_required:
- BUILD / UNIT_TEST / INTEGRATION_TEST
- DATABASE_RUNTIME / HTTP_RUNTIME / BROWSER_RUNTIME / SECURITY_SANDBOX / OBSERVABILITY
- AISCC self-dogfood runtime transition trace for this Task

forbidden:
- all runtime/external/scoring actions listed above

proof_non_substitution:
- accepted P2 capability evidence != P3 comparative result
- protocol completeness != evaluation execution
- synthetic ablation != competitor benchmark
- manual Command Center authoring != self-dogfood evidence
- executor report != Human methodology acceptance

## accept 기준

- expected HEAD/current authority verified or mutation absent on mismatch
- accepted P2 exact refs selected without speculative broad history
- minimum matrix frozen or honest `CORPUS_GAP` recorded
- synthetic baseline labels exact
- matched-condition rule explicit
- metric scoring/success/failure/exclusion deterministic enough for later evaluation without redesign
- 15 required protocol sections present
- claim ceiling and amendment rule present
- comparative result generated: `No`
- product/runtime/scenario source changes: `none`
- forbidden actions absent
- target report/export complete

## hold/reject 기준

- corpus selection depends on observed comparative outcome
- comparator is allowed to drift after freeze
- baseline is represented as a real competitor/industry standard
- matched-condition is violated
- metric lacks deterministic scoring rule
- result/score/superiority wording appears
- product/runtime/source mutation occurs
- required source can only be obtained by broad speculative search or runtime rerun

## mandatory stop 조건

- HEAD/current authority mismatch without newer canonical explanation
- predecessor blocked Cycle/Judgment/Handoff missing
- policy/source/evidence conflict
- dirty collision on protocol path
- P2 corpus ref cannot be established without broad speculative history search
- forbidden action/tool request
- security/private-data uncertainty
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`

named blocker 뒤에는 최소 evidence, workspace inventory, report/export만 수행한다.

## 보고서 필수 항목

- task/work type/path
- predecessor block correction statement
- repository HEAD/current-state verification
- read paths/source inventory
- accepted corpus inventory
- frozen matrix + `CORPUS_GAP` rows
- protocol path/hash
- product/governance/config changes separated
- evidence classification
- forbidden-not-run
- comparative result generated: `No`
- Human verification: `HUMAN_PENDING`
- unverified/gaps
- rollback
- preserved paths
- next bounded comparative execution recommendation

## export bundle 요구

Target:
`.aiassistant/reports/target/20260915_0054_aiscc-p3-1-comparative-evaluation-protocol-freeze-manual-rework-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- changed `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md` preserving project-relative path
- `REMOVED_FILES.md` only when actual project deletion exists

Executor ZIP:
`.aiassistant/reports/target/20260915_0054_aiscc-p3-1-comparative-evaluation-protocol-freeze-manual-rework-1.zip`

## 사람 검증 요구

Browser Command Center는 protocol candidate가 나오면 다음을 판정한다.

1. synthetic baseline이 strawman이 아닌가
2. corpus가 result 관측 전에 source availability/class coverage로 고정됐는가
3. primary metrics가 truthfulness/auditability/failure behavior를 직접 측정하는가
4. P2 capability proof와 P3 comparative proof가 분리됐는가
5. claim ceiling, small-N limitation, amendment rule이 충분한가

## preserved artifact exact paths

- `.aiassistant/tasks/done/20260915_0054_aiscc-p3-1-comparative-evaluation-protocol-freeze-manual-rework-1.md`
- `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md` candidate
- predecessor blocked Task/Cycle/Judgment

## 최종 응답 형식

1. result: completed / blocked / rejected-candidate
2. target bundle + ZIP path
3. protocol candidate path/hash
4. selected minimum corpus count / gap count
5. changed files
6. removed files
7. comparative result generated: `No`
8. human verification: `HUMAN_PENDING`
9. unverified/corpus gaps
10. preserved exact paths
