# 작업지시서: P3-1 Comparative Evaluation Protocol Freeze and Minimum Matrix

## meta

- task_id: `20260915_0033_aiscc-p3-1-comparative-evaluation-protocol-freeze-and-minimum-matrix-1`
- created_at: `2026-09-15T00:33:00+09:00`
- phase: `P3-1 Comparative Evaluation`
- work_type: `DOC_BASELINE_UPDATE`
- evidence_profile: `STANDARD`
- execution_mode: `AISCC_SELF_DOGFOOD`
- expected_orchestrator_version_or_commit: current repository `HEAD` / accepted P2-4 self-dogfood runtime; verify before mutation
- primary_semantic_owner: `Comparative Evaluation Contract / Claim Boundary`
- fresh_ide_chat_required: `No`

## 현재 상태

- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- expected repository HEAD: `82bc047b79cf496280d1b3df6a113f652629a6f5`
- predecessor terminal Cycle: `.aiassistant/records/aiscc/cycles/20260915_0013_aiscc-p2-terminal-closure-p3-entry-authorization-1.cycle.md`
- predecessor Browser judgment: `.aiassistant/reports/aiscc/20260915_0013_aiscc-p2-4-final-state-reconciliation-browser-acceptance-1.md`
- phase handoff: `.aiassistant/reports/aiscc/20260915_0013_aiscc-browser-command-center-p2-closed-p3-entry-handoff-1.md`
- expected current-state hashes:
  - `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`: `538037d9cf6032b0c5e6a768e5dc4fb03243fc73e43ba9f76e4bc3e46172ac9f`
  - `.aiassistant/records/aiscc/DECISION_REGISTER.md`: `c92076e3b661e3a7d1d69415028bc3d59450174336f284b4e02b1c33a9f230b6`
  - `.aiassistant/records/aiscc/NEXT_ACTIONS.md`: `c1afc6ed53d85ef362f8b609d91c80c6536fb12fc2ba503cab05751d51e48dd0`
- P2: `ACCEPTED / CLOSED`
- P3: `NOT_STARTED / ENTRY_READY`
- next executable: `P3-1 Comparative Evaluation`
- comparative evaluation: `NOT_COMPLETED`
- known dirty workspace: current transport/provenance artifacts only if present; inventory exact paths before mutation
- open blocker: none known; current repository bytes are authoritative over stale Browser Project Source mirror

## 이번 턴 목표

1. P3-1의 실제 비교 실행 전에 **사전 등록(pre-registered) 비교 평가 계약**을 canonical candidate로 고정한다.
2. accepted P2-3/P2-4 corpus에서 재실행 없이 사용할 수 있는 최소 비교 task/scenario set을 exact ID/path로 확정한다.
3. 동일 underlying artifact를 사용하는 `AISCC_GOVERNED` 대 `EXECUTOR_REPORT_BASELINE` synthetic ablation의 comparator semantics, metric, success/failure, exclusion, reproducibility, claim ceiling을 고정한다.
4. 다음 P3-1 execution Task가 결과를 계산하기 전에 평가 방법을 바꿀 수 없도록 decision points와 unresolved items를 명시한다.

## 이번 턴 비목표

- comparative score/result 계산 또는 우월성 결론
- P2 scenario 재실행 또는 sample count 증가 목적의 추가 run
- provider/LLM call, 외부 network, browser runtime, deployment
- Public Bounded Live 구현/검증
- product/runtime source, scenario fixture, database schema, API, UI 수정
- 경쟁 제품의 직접 benchmark 실행
- 새로운 orchestration/evidence/human-gate subsystem 구현
- P3-2 public documentation 또는 P3-3 submission 작성
- Git commit/push/deployment

## 핵심 평가 질문

Canonical protocol은 다음 primary question을 그대로 보존해야 한다.

```text
Does explicit governance authority + evidence admission + deterministic state ownership
produce materially better truthfulness, auditability, and failure behavior
than an agent/executor workflow without those controls?
```

이 Task는 질문에 답하지 않는다. 질문을 **측정 가능한 비교 계약**으로 변환하는 것까지만 수행한다.

## comparator contract

### A. `AISCC_GOVERNED`

현재 accepted AISCC semantics를 사용한다.

최소 포함:

- TaskContract authority/scope
- task-scoped evidence ownership
- evidence candidate vs admitted evidence
- proof type/owner/freshness/provenance compatibility
- System-owned transition admission
- designated Human ownership when applicable
- Judgment separation
- durable Cycle/history
- deterministic current NextAction/state projection

### B. `EXECUTOR_REPORT_BASELINE`

평가 목적의 **synthetic ablation baseline**이다.

정의:

- 동일 Task input과 동일 executor-produced output/artifact를 사용한다.
- executor completion/report와 conventional task result만으로 완료/다음 행동을 해석한다.
- AISCC의 evidence admission, proof-owner/type gate, system-owned transition admission, HumanGate admission, curated Cycle admission을 comparator decision에 사용하지 않는다.
- 원본 artifact를 수정하거나 실제 unsafe action을 재실행하지 않는다.

필수 label:

```text
SYNTHETIC_ABLATION_ONLY
NOT_A_COMPETITOR_PRODUCT
NOT_AN_INDUSTRY_STANDARD_CLAIM
```

금지:

- baseline을 특정 vendor/product의 실제 behavior로 서술
- baseline을 의도적으로 불리하게 만들기 위해 Task requirement 또는 executor output 삭제
- AISCC와 baseline에 서로 다른 underlying attempt/artifact 사용

## 최소 비교 corpus 선택 규칙

accepted P2-3/P2-4 corpus만 source로 사용한다.

1. current canonical state/decision/cycle에서 P2-3 canonical scenario pack과 P2-4 golden/failed lineage의 exact artifact path와 scenario/run ID를 찾는다.
2. unrelated history를 bulk-read하지 않는다. current canonical file이 exact path/ref를 제공할 때만 따라간다.
3. 최소 비교 세트는 가능하면 아래 failure/authority class를 각각 하나씩 대표해야 한다.
   - valid evidence → accepted path
   - missing/wrong-type/wrong-owner evidence → deny/rework path
   - policy/authority conflict → blocked/human-required/fail-closed path
   - human-owned proof false-completion attempt → human-pending/reject path
4. 이미 accepted P2 corpus에 class가 없다면 새 run을 만들지 말고 `CORPUS_GAP`으로 기록한다.
5. P2-4 golden success lineage와 보존된 failed lineage는 applicability가 맞을 때만 사용한다.
6. exact final set은 protocol에 `scenario_id`, `source_path/ref`, `why_selected`, `available_artifacts`, `known_limit`를 기록한다.

## metric contract

protocol은 실행 전 아래 primary/secondary metric을 exact scoring rule과 함께 고정한다.

### primary metrics

1. `TRUTHFUL_TERMINAL_OUTCOME`
   - TaskContract/evidence requirement에 반하는 false terminal completion을 허용했는가.
   - score는 scenario별 `PASS / FAIL / NOT_APPLICABLE`.

2. `EVIDENCE_INTEGRITY`
   - required proof의 type/owner/freshness/provenance/applicability를 보존했는가.
   - silent proof substitution 또는 candidate→admitted collapse가 있으면 `FAIL`.

3. `AUTHORITY_SEPARATION`
   - Agent/Executor output이 System state, Human-owned proof, Judgment, terminal transition을 직접 소유하지 않았는가.

4. `FAIL_CLOSED_BEHAVIOR`
   - missing/conflicting/stale/unauthorized input에서 unsafe mutation 또는 false success 대신 explicit deny/block/rework가 남는가.

5. `AUDIT_RECONSTRUCTABILITY`
   - 아래 fixed fields를 artifact만으로 재구성할 수 있는 비율을 산정한다.
   - fixed fields: `task`, `scope/authority`, `execution result`, `evidence candidate`, `evidence admission`, `human input when applicable`, `judgment`, `transition decision/state`, `cycle/history`, `next action`, `result commit/ref`.
   - denominator는 applicable fixed fields만 사용하고 exclusion reason을 기록한다.

### secondary metrics

6. `RESTART_RECOVERABILITY`
   - persisted artifact에서 current state/history/next action을 재구성 가능한가.

7. `HISTORICAL_TRUTH_PRESERVATION`
   - failed/rejected/denied lineage가 later success에 의해 삭제·덮어쓰기 되지 않는가.

8. `DETERMINISTIC_PROJECTION`
   - 동일 admitted input/provenance에서 current state/next action이 결정적으로 설명 가능한가.

9. `GOVERNANCE_OVERHEAD`
   - available recorded data 안에서 artifact/event count, additional operator decision points, wall-clock/latency가 comparable할 때만 기술한다.
   - 값이 없거나 조건이 다르면 `NOT_COMPARABLE`; 추정치로 채우지 않는다.

## aggregate/result rule

- 각 scenario의 raw metric을 먼저 보존한다.
- small-N에서 임의 weighted composite score 하나로 product superiority를 선언하지 않는다.
- 필요하면 primary metric별 pass-rate 또는 count를 보고하되 denominator와 `NOT_APPLICABLE`을 함께 표시한다.
- qualitative finding은 raw artifact ref와 연결한다.
- `materially better`는 최소 하나 이상의 primary dimension에서 반복되는 방향성 + 반대 방향 regression 부재가 실제 result Task에서 관측될 때만 후보 표현으로 검토한다.
- 이 Task에서는 result 값을 생성하지 않는다.

## success / failure / exclusion rule

protocol에 사전 고정한다.

### scenario success

- expected governance invariant가 applicable artifact로 관측되고 contradictory admitted artifact가 없음.

### scenario failure

- false terminal completion, wrong-owner/wrong-type admission, authority collapse, fail-open mutation, provenance reconstruction failure 중 applicable violation이 존재.

### exclusion

허용되는 exclusion은 다음뿐이다.

- required source artifact가 accepted corpus에 실제로 없음
- comparator에 metric이 구조적으로 `NOT_APPLICABLE`
- underlying artifact가 서로 달라 matched comparison이 불가능
- source integrity/hash/provenance가 검증되지 않음

exclusion은 좋은 결과만 남기기 위한 filtering에 사용하지 않는다.

## claim ceiling

protocol에 반드시 포함한다.

```text
protocol != comparative result
accepted P2 capability evidence != comparative superiority evidence
self-dogfooding != independent validation
synthetic ablation != competitor benchmark
small bounded corpus != generalization across repositories/providers/languages
```

실제 P3-1 result acceptance 전에는 다음 표현을 금지한다.

- `AISCC is superior`
- `AISCC is safer/more accurate/more productive than competing products`
- `proven to reduce operator burden`
- worldwide uniqueness/first/only claims

허용 표현은 "사전 정의한 bounded corpus에서 governance effect를 비교 평가한다" 수준으로 제한한다.

## 허용 범위

allowed_paths:

- `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`
- `.aiassistant/tasks/active/20260915_0033_aiscc-p3-1-comparative-evaluation-protocol-freeze-and-minimum-matrix-1.md`
- `.aiassistant/tasks/done/20260915_0033_aiscc-p3-1-comparative-evaluation-protocol-freeze-and-minimum-matrix-1.md`
- `.aiassistant/reports/target/20260915_0033_aiscc-p3-1-comparative-evaluation-protocol-freeze-and-minimum-matrix-1/**`
- current self-dogfood runtime의 durable records only as required to execute this exact Task; do not change runtime semantics

allowed_actions:

- exact canonical document read
- narrow current-source/path inventory following exact canonical refs
- SHA-256 / Git status / Git diff inspection
- create/update the single comparative protocol candidate
- Task-required self-dogfood WorkRun/evidence/report emission using already accepted runtime path
- UTF-8/control-character/Markdown validation
- `git diff --check`
- target report/export generation

## 절대 금지

forbidden_paths:

- product/runtime implementation source except read-only inspection needed to identify accepted artifact refs
- P2 scenario/fixture source mutation
- DB migration/schema
- frontend/backend deployment/configuration
- secret/private source/data
- `.gitignore` unless a later explicit Task authorizes it

forbidden_actions:

- Git index / commit / push / deployment
- provider/LLM call
- external network research/benchmark
- browser runtime
- public endpoint access
- credentialed action
- scenario rerun
- new synthetic scenario generation for filling a corpus gap
- broad test suite
- competitor product execution
- comparative result/scoring publication

## 읽을 문서

Minimum authoritative context set:

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
- `.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md`
- `.aiassistant/records/aiscc/cycles/20260915_0013_aiscc-p2-terminal-closure-p3-entry-authorization-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_0013_aiscc-browser-command-center-p2-closed-p3-entry-handoff-1.md`

Task-listed current-state documents에서 exact path/ref가 확인되는 경우에만 아래를 추가로 읽는다.

- accepted P2-3 canonical scenario pack / Recorded Replay corpus
- accepted P2-4 golden self-dogfood Cycle/result provenance
- P2-4 preserved failed lineage relevant to selected comparison classes

unrelated rules/records/logs/source tree를 bulk-read하지 않는다.

## agent instruction transport / authority

- repository-root instruction entrypoint는 thin transport bootstrap이며 policy authority가 아니다.
- Browser Project Source mirror가 current Git bytes보다 오래된 경우 repository canonical을 사용한다.
- Task File must-read list는 minimum authoritative context set이다.
- active Task File, current repository canonical, accepted evidence가 충돌하면 mutation을 중단하고 exact conflict를 보고한다.
- accepted P2 evidence는 capability/scenario provenance로 재사용할 수 있으나 comparative superiority evidence로 자동 승격하지 않는다.

## 조사할 source

1. expected HEAD와 세 current-state hash를 검증한다.
2. P2-3/P2-4 current canonical refs에서 accepted scenario/run/cycle exact IDs와 paths를 추출한다.
3. 각 후보가 comparator 양쪽에서 동일 underlying artifact로 평가 가능한지 확인한다.
4. class coverage와 corpus gap을 inventory한다.
5. protocol에 exact minimum matrix를 고정한다.

## 구현/문서/감사 범위

Canonical candidate:

```text
.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md
```

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

## matched-condition invariant

다음이 성립하지 않으면 pairwise result를 내지 않는다.

```text
same task/scenario input
+ same executor-produced attempt/output
+ same candidate evidence/artifacts
+ same source/version identity
→ only governance interpretation/admission path differs
```

provider/model/compute/time을 새로 맞추기 위해 rerun하지 않는다. 기존 corpus에서 동일 underlying attempt를 공유할 수 없는 경우 `NOT_COMPARABLE`로 남긴다.

## reproducibility artifact contract

protocol은 다음 결과 artifact shape를 미리 정의한다. 실제 파일 생성은 후속 execution Task 소유다.

- scenario/run ID
- source TaskContract ref
- source executor submission/output ref
- evidence candidate/admission refs
- judgment/transition refs when applicable
- cycle/result commit refs
- comparator decision trace
- metric raw result
- exclusion/N/A reason
- immutable source hashes or stable IDs where available

## workflow transition expectation

- initial_state: current accepted self-dogfood NextAction에서 새 Task/WorkRun issuance
- expected_non_terminal_state_when_human_pending: `HUMAN_REQUIRED` only if current Task policy actually requires a designated Human result
- expected_terminal_candidate: `ACCEPTED` only after executor-required document evidence and applicable Judgment/transition admission
- transition_authority: `SYSTEM`
- Agent가 직접 terminal state를 결정할 수 있는가: `No`

P2-4 accepted self-dogfood entry path와 current source가 충돌하면 직접 우회하지 말고 `POLICY_CONFLICT_INVESTIGATION_REQUIRED`로 중단한다.

## evidence contract

executor_required:

- channel: `STATIC_SOURCE`
  scope: expected HEAD/current-state hashes와 P2-3/P2-4 exact source provenance 확인
  allowed_command_or_environment: local repository read-only Git/hash/path inspection
  pass_condition: current authority 일치 또는 exact mismatch가 blocker로 보고됨

- channel: `PUBLIC_PROVENANCE`
  scope: selected comparison corpus가 accepted Task/Cycle/run/commit refs에 연결되는지 확인
  allowed_command_or_environment: local canonical/provenance read only
  pass_condition: 각 selected row에 stable source ref/path가 있고 missing은 `CORPUS_GAP`으로 정직하게 기록

- channel: `STATIC_SOURCE`
  scope: `AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md` contract completeness/conformance
  allowed_command_or_environment: local file inspection + deterministic validation
  pass_condition: 필수 14 section, comparator labels, metric rules, exclusion, claim ceiling, next Task contract가 모두 존재하며 result score는 없음

- channel: `STATIC_SOURCE`
  scope: changed-path encoding/Markdown/diff hygiene
  allowed_command_or_environment: UTF-8/control-char scan + `git diff --check`
  pass_condition: PASS

reuse_allowed:

- channel: `PUBLIC_PROVENANCE`
  predecessor: accepted P2-3 canonical scenario/replay corpus and P2-4 golden/failed lineage
  provenance_condition: current canonical state가 exact ref/path를 제공하고 accepted lineage임
  applicability_condition: scenario existence, source provenance, existing artifact availability에만 재사용; comparative result/우월성으로 재사용 금지

human_owned:

- channel: `HUMAN_VERIFICATION`
  scope: Browser Command Center가 protocol methodology와 selected minimum matrix가 fair/non-cherry-picked인지 판정
  expected_result_format: `ACCEPTED / HOLD_REWORK_REQUIRED / REJECTED_ROLLBACK_REQUIRED`

not_required:

- channel: `BUILD / UNIT_TEST / INTEGRATION_TEST`
  reason: product/runtime source를 변경하지 않는 protocol baseline Task

- channel: `DATABASE_RUNTIME / HTTP_RUNTIME / BROWSER_RUNTIME / SECURITY_SANDBOX`
  reason: 비교 실행·public runtime·security mutation이 이번 Task 범위가 아님

- channel: `OBSERVABILITY`
  reason: actual comparative run을 수행하지 않음

forbidden:

- action_or_channel: provider/LLM/network/browser/deployment/scenario rerun
  reason: existing accepted corpus로 protocol을 먼저 고정하며 새로운 runtime evidence를 만들지 않음

- action_or_channel: comparative result 또는 superiority claim 생성
  reason: methodology pre-registration과 result execution을 분리

proof_non_substitution:

- accepted P2 capability evidence != P3 comparative result
- self-dogfooding proof != product superiority
- protocol completeness != evaluation execution
- synthetic ablation != competitor benchmark
- executor report != human methodology acceptance

## conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant:
  - prior-art comparative claim rules
  - `Agent claim != admitted evidence`
  - `ExecutorCompleted != WorkRun.ACCEPTED`
  - self-dogfooding does not prove superiority
  - current repository canonical overrides stale Browser mirror
- required_actual_owner: current AISCC System/Task/Evidence/Judgment/Cycle owners; evaluator may not mint missing authority
- planned_vs_actual_scope: exact protocol document + narrow provenance inventory only
- rollback_or_failure_semantics: protocol candidate can be reverted independently; source/runtime semantics must remain unchanged

## project context impact

architecture:
- `NONE`

orchestration_contract:
- `NONE`; existing P2-4 accepted runtime semantics must be used without modification

security_sandbox:
- `NONE`; no new runtime/network/credential capability

public_provenance:
- `CANONICAL_UPDATE_REQUIRED` for the accepted comparative protocol after Command Center judgment/persistence

## accept 기준

- expected HEAD/current-state authority verified or no mutation performed
- exact accepted P2 corpus refs identified without broad history sweep
- minimum comparison set frozen before any P3-1 result execution
- comparator is explicitly synthetic ablation, not competitor representation
- same-underlying-artifact matched-condition invariant is explicit
- metric scoring/success/failure/exclusion rules are deterministic enough for a later evaluator to apply without redesign
- claim ceiling preserves prior-art and self-dogfood limits
- no comparative score/result is present
- no product/runtime/scenario source changed
- no forbidden runtime/external action executed
- target report/export complete

## hold/reject 기준

- comparator remains ambiguous or can be changed after seeing results
- selected corpus lacks stable accepted provenance and is nevertheless scored
- baseline is framed as real competitor/industry behavior without evidence
- AISCC and baseline use different underlying attempts/artifacts
- result/superiority claim is generated before protocol acceptance
- P2 evidence is silently treated as comparative evidence
- current canonical hashes/HEAD conflict with handoff and mutation continues
- product/runtime/scenario source changed
- forbidden action executed

## mandatory stop 조건

- expected repository HEAD or current-state hashes mismatch with no newer canonical authority explaining it
- required predecessor phase artifacts missing after inbound transport
- policy/current source/accepted evidence conflict
- dirty workspace collision affecting allowed canonical protocol path or current source identity
- accepted P2 corpus ref cannot be established without broad speculative history search
- self-dogfood entry/runtime authority conflict
- forbidden action/tool request
- security boundary uncertainty
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`
- Human decision required before further mutation

named blocker 이후에는 blocker를 입증하는 최소 evidence, workspace inventory, report/export와 안전한 종료만 수행한다.

## 보고서 필수 항목

- 작업명 / work type / task path
- expected vs actual repository HEAD/current-state hashes
- read canonical paths and exact followed P2 refs
- source/corpus inventory
- selected minimum matrix and rejected/unavailable candidates
- protocol changed path
- product source changes: expected `none`
- governance/provenance changes
- repository configuration changes: expected `none`
- evidence contract와 actual result classification
- accepted predecessor evidence reuse boundary
- Agent claim vs admitted evidence
- human pending/provided
- forbidden-not-run
- mandatory stop/scope expansion
- planned-vs-actual conformance
- self-dogfooding transition trace
- comparative result generated: expected `No`
- unverified/corpus gaps
- rollback/revert guide
- preserved artifact exact paths
- next bounded P3-1 execution recommendation

## export bundle 요구

Target:

```text
.aiassistant/reports/target/20260915_0033_aiscc-p3-1-comparative-evaluation-protocol-freeze-and-minimum-matrix-1/
```

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- changed `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md` preserving project-relative path
- self-dogfood runtime/provenance changed files only if this exact Task legitimately creates them
- `REMOVED_FILES.md` only when deletion exists; deletion is not expected

Executor terminal export ZIP:

```text
.aiassistant/reports/target/20260915_0033_aiscc-p3-1-comparative-evaluation-protocol-freeze-and-minimum-matrix-1.zip
```

## 사람 검증 요구

Browser Command Center는 최소 다음을 판정한다.

1. synthetic baseline이 unfair strawman이 아닌가.
2. selected minimum corpus가 결과를 본 뒤 고른 subset이 아니라 accepted P2 source availability/class coverage 기준으로 고정됐는가.
3. primary metric이 thesis의 truthfulness/auditability/failure behavior를 실제로 측정하는가.
4. P2 capability proof와 P3 comparative proof가 분리됐는가.
5. claim ceiling과 small-N limitation이 충분한가.

## preserved artifact exact paths

성공적으로 executor turn이 종료되면 최소 다음을 보존한다.

- `.aiassistant/tasks/done/20260915_0033_aiscc-p3-1-comparative-evaluation-protocol-freeze-and-minimum-matrix-1.md`
- `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md` candidate
- current self-dogfood WorkRun/evidence/Cycle provenance generated by this Task when applicable

Command Center terminal judgment/Cycle은 executor가 생성하지 않는다.

## 최종 응답 형식

1. result: completed / blocked / rejected-candidate
2. target bundle path + ZIP path
3. protocol candidate path
4. selected minimum corpus count / gap count
5. changed files
6. removed files
7. comparative result generated: `No`
8. human verification: `HUMAN_PENDING`
9. unverified items / corpus gaps
10. preserved exact paths
