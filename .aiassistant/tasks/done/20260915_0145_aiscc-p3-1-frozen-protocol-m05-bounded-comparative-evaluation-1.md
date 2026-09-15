# 작업지시서: P3-1 frozen-protocol M05 bounded comparative evaluation

## meta

- task_id: `20260915_0145_aiscc-p3-1-frozen-protocol-m05-bounded-comparative-evaluation-1`
- created_at: `2026-09-15T01:45:00+09:00`
- work_type: `QA_ONLY`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `P3-1 comparative evaluation result / Browser Command Center`

## 현재 상태

- accepted protocol:
  - `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`
  - SHA-256 `a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6`
  - `HUMAN_PROVIDED / ACCEPTED`
- source audit:
  - M01-M04 `GAP_PARTIAL`
  - frozen handling remains `EX_SOURCE_MISSING / NOT_COMPARABLE`
  - no protocol amendment
- comparative result:
  - `NOT_GENERATED` before this Task
- eligible frozen row:
  - M05 only
- repository HEAD observed by predecessor:
  - `82bc047b79cf496280d1b3df6a113f652629a6f5`

## 이번 턴 목표

1. accepted protocol v1 exact bytes/hash를 검증한다.
2. M05의 exact frozen source packet을 protocol section 6 selectors와 2317 accepted archive에 대해 integrity recheck한다.
3. metric 계산 전에 `SOURCE_PACKET_MANIFEST.json`을 완성하고 hash/freeze timestamp를 기록한다.
4. `AISCC_GOVERNED`와 `EXECUTOR_REPORT_BASELINE` 두 comparator를 동일한 M05 source packet에 deterministic offline interpretation으로 적용한다.
5. protocol section 7의 primary/secondary metric을 exact scoring rule대로 계산한다.
6. M01-M04는 변경 없이 explicit exclusion rows로 결과 artifact에 포함한다.
7. protocol section 10의 reproducibility artifacts와 제한적 `RESULT_REVIEW.md`를 생성한다.
8. 결과를 Human review 대상으로 제출하되 Executor가 acceptance나 superiority를 주장하지 않는다.

## 이번 턴 비목표

- M01-M04 재탐색 또는 gap repair
- 새 scenario/run 생성
- P2 scenario rerun
- provider/LLM/network/browser/DB/runtime/deployment
- current source를 historical M05 packet 대신 사용
- competitor/vendor benchmark
- weighted composite superiority score
- protocol comparator/metric/exclusion/matrix/publication threshold 변경
- `materially better` 자동 판정
- P3-2/P3-3 documentation/release/submission
- Git index/commit/push

## 허용 범위

allowed_paths:
- `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`
- `.aiassistant/reports/target/20260914_2317_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-judgment-call-fix-retry-1.zip`
- `.aiassistant/tasks/done/20260914_2317_aiscc-p2-4-golden-agent-single-file-proof-change-4.md`
- exact accepted P2-4 acceptance anchors named by protocol
- exact files/members named by protocol section 6 for M05:
  - `GOLDEN_TASKCONTRACT.json`
  - `GOLDEN_EXTERNAL_SUBMISSION.json`
  - `GOLDEN_EVIDENCE.json`
  - `GOLDEN_JUDGMENT.json`
  - `GOLDEN_TRANSITIONS.json`
  - `GOLDEN_WORKRUN.json`
  - `GOLDEN_CYCLE.json`
  - `GOLDEN_NEXT_ACTION.json`
  - `GOLDEN_PROVENANCE_ROOT.md`
  - `GIT_RESULT_REVIEW.md`
  - `docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md`
- `.aiassistant/records/aiscc/cycles/20260915_0145_aiscc-p3-1-source-packet-audit-accepted-bounded-evaluation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_0145_aiscc-p3-1-source-packet-audit-browser-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260915_0145_aiscc-browser-command-center-p3-1-source-gap-closed-bounded-evaluation-entry-handoff-1.md`
- current Task/target bundle

allowed_actions:
- exact SHA-256/size/path/member validation
- read-only ZIP member access
- exact `git cat-file`/`git show` only for protocol-named M05 commits/blobs when needed to verify immutable deliverable identity
- deterministic local JSON/Markdown processing
- offline comparator trace derivation
- offline metric calculation
- deterministic double-run projection check using the same frozen packet/rules
- target-bundle artifact generation

## 절대 금지

forbidden_paths:
- unrelated product/runtime/test source
- M01-M04 source/history/archive paths beyond already accepted exclusion records
- private runtime storage
- credentials/env/customer/private source
- unrelated `.aiassistant` history

forbidden_actions:
- broad `git log`, broad `git grep`, archive hunting or filesystem search
- scenario execution/rerun
- AISCC DB/runtime startup
- provider/LLM/network/browser
- current source regeneration
- human-owned verification claim
- comparator redesign
- metric redesign
- exclusion-code redesign
- matrix membership change
- threshold/publication-rule change
- outcome-based exclusion
- source-excluded rows converted to FAIL/PASS/N/A
- synthetic baseline recommendation described as an executed unsafe action
- weighted composite score
- significance/confidence-interval claim implying random sampling
- product superiority/generalization claim

## 읽을 문서

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`
- `.aiassistant/records/aiscc/cycles/20260915_0145_aiscc-p3-1-source-packet-audit-accepted-bounded-evaluation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_0145_aiscc-p3-1-source-packet-audit-browser-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260915_0145_aiscc-browser-command-center-p3-1-source-gap-closed-bounded-evaluation-entry-handoff-1.md`
- exact M05 source archive/member refs from protocol section 6 only

## agent instruction transport / authority

- Task File은 이번 실행의 exact scope/evidence contract다.
- protocol SHA mismatch면 scoring 전에 `POLICY_CONFLICT_INVESTIGATION_REQUIRED`로 STOP한다.
- M05 source integrity/matched condition이 실패하면 scoring 전에 `BLOCKED_REQUIRED_EVIDENCE`로 STOP한다.
- M01-M04 exclusions는 이미 accepted source-audit result이며 다시 조사하지 않는다.
- Agent는 결과의 semantic acceptance나 public claim을 결정하지 않는다.
- Human result는 별도 Browser review 전 `HUMAN_PENDING`이다.

## M05 frozen identity

```text
row_id: M05
scenario_lineage: aiscc-p2-4-golden-cycle-3@v1
workrun: aiscc-p2-4-golden-workrun-3
matched_condition: SAME_ARTIFACT_BINDING_VERIFIED_FOR_LATER_OFFLINE_EVALUATION

Task:
.aiassistant/tasks/done/20260914_2317_aiscc-p2-4-golden-agent-single-file-proof-change-4.md
SHA-256:
b62c43537c5edc0ce99cc8c45b7fc7f73d96ad90561fe6507571c0eed86c88ce

accepted archive:
.aiassistant/reports/target/20260914_2317_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-judgment-call-fix-retry-1.zip
SHA-256:
96e64c0d8086de5ca36b747ff8157e1437b1ede53399c404c76c997d6eb5f3cb

result deliverable:
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md

result commit:
ea34a0e08912d6259c74d0cb50ade9c9b9dba77e

deliverable SHA-256:
7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
```

Preserve protocol-named body_ref/body_sha, submission/attempt ID, Evidence refs, Judgment ID, terminal transition ID, Cycle ID and NextAction selection ID exactly.

## comparator execution contract

### `AISCC_GOVERNED`

Apply accepted recorded governance semantics only.

Use:
- TaskContract authority/scope
- task-scoped evidence ownership
- candidate/admitted distinction
- type/owner/freshness/provenance/applicability
- System transition admission
- Human ownership when applicable
- Judgment
- Cycle/history
- deterministic NextAction

Do not create a new owner decision. This is interpretation of recorded admitted state.

### `EXECUTOR_REPORT_BASELINE`

Apply protocol section 4 fixed order exactly.

Requirements:
- conservative conventional report reader
- Task requirements and executor caveats preserved
- no AISCC evidence-admission outcome / transition / HumanGate admission / Cycle admission / NextAction as decision inputs
- explicit failures/pending requirements outrank generic completion
- missing support -> `UNRESOLVED`
- `REPORTED_COMPLETE` only when the fixed rule permits
- baseline next action generated by the frozen deterministic rule
- every consulted field/span logged

The baseline may tie, abstain or outperform. Do not force a difference.

## required evaluation artifacts

Create before any scoring:

1. `SOURCE_PACKET_MANIFEST.json`
   - protocol revision + SHA
   - source archive/path/member SHA/size
   - repository/execution/result commits
   - TaskContract/WorkRun/submission/attempt identity
   - decision-input refs vs reference-only refs
   - M01-M04 exclusion records
   - manifest frozen timestamp/hash

Then create:

2. `COMPARATOR_TRACES.jsonl`
   - row/arm
   - ordered comparator rule steps
   - exact consulted refs/spans/JSON pointers
   - requirement outcomes
   - decision/result
   - next action
   - reference-only fields clearly separated

3. `RAW_METRICS.jsonl`
   - M01-M05 all retained
   - arm
   - metric
   - applicability
   - PASS/FAIL/NOT_APPLICABLE or exact audit numerator/denominator
   - exact rule and provenance
   - source-excluded rows explicitly recorded but not scored

4. `EXCLUSIONS.json`
   - M01-M04
   - `EX_SOURCE_MISSING`
   - exact missing selector/reason
   - denominator effect
   - no outcome-based interpretation

5. `RECONSTRUCTION_CHECK.json`
   - two independent deterministic offline applications
   - canonical tuple comparison
   - no LLM/runtime

6. `RESULT_REVIEW.md`
   - dimension-specific M05 observations
   - ties/contrary findings
   - M01-M04 exclusions
   - limitation/confidence boundary
   - publication condition evaluation
   - Human result status `HUMAN_PENDING`
   - no public superiority wording

7. `RESULT_INTEGRITY.json`
   - hashes of all above artifacts
   - protocol hash
   - source-manifest hash
   - result-generation tool/script identity or deterministic command description

## metric contract

Use protocol section 7 exactly:

Primary:
- `TRUTHFUL_TERMINAL_OUTCOME`
- `EVIDENCE_INTEGRITY`
- `AUTHORITY_SEPARATION`
- `FAIL_CLOSED_BEHAVIOR`
- `AUDIT_RECONSTRUCTABILITY`

Secondary:
- `RESTART_RECOVERABILITY`
- `HISTORICAL_TRUTH_PRESERVATION`
- `DETERMINISTIC_PROJECTION`
- `GOVERNANCE_OVERHEAD`

Rules:
- do not invent N/A to improve rates
- source-ineligible rows are excluded before scoring
- fixed audit fields remain fixed
- publish M05 per-field audit numerator/denominator
- no weighted composite
- descriptive counts only
- no significance inference

## publication-condition evaluation

After raw results are frozen, calculate only whether the protocol's publication condition is mechanically satisfiable.

Because eligible attempts = 1 before scoring:

```text
materially_better_condition_possible = No
reason = requires at least two distinct eligible attempts spanning at least two requested classes
```

This structural fact is not outcome-derived.

Do not replace it with another threshold.

Even if all M05 metrics favor `AISCC_GOVERNED`, permitted conclusion is limited to:

```text
one eligible bounded artifact-interpretation comparison was completed;
four planned rows were source-excluded;
the corpus is insufficient for the protocol's stronger directional claim.
```

## workflow transition expectation

- initial_state: `MANUAL_COMMAND_CENTER / comparative result execution`
- expected_non_terminal_state_when_human_pending: `RESULT_CANDIDATE / HUMAN_PENDING`
- expected_terminal_candidate: `RESULT_CANDIDATE / HUMAN_PENDING`
- transition_authority: `NOT_APPLICABLE`
- Agent가 comparative acceptance를 직접 결정할 수 있는가: `No`

## evidence contract

executor_required:
- channel: `STATIC_SOURCE / PUBLIC_PROVENANCE`
  scope: M05 exact source identity and matched-condition integrity
  pass_condition: all frozen source refs/hashes/identities verify before scoring
- channel: `QA_ONLY / COMPARATIVE_EVALUATION`
  scope: deterministic comparator traces and metric outputs under frozen protocol
  pass_condition: required result artifacts complete, reproducible, and internally consistent
- channel: `CONFORMANCE`
  scope: exclusions/publication/claim boundaries
  pass_condition: M01-M04 unchanged exclusions; no forbidden claim or post-hoc protocol change

reuse_allowed:
- channel: `PUBLIC_PROVENANCE`
  predecessor: accepted P2-4 M05 packet and accepted P3-1 protocol/source audit
  provenance_condition: exact hash/identity match
  applicability_condition: evaluation input/reference truth only

human_owned:
- channel: `HUMAN_VERIFICATION`
  scope: comparative result interpretation/acceptance and any public wording
  expected_result_format: `ACCEPTED | REWORK | REJECTED`

not_required:
- channel: `DATABASE_RUNTIME / HTTP_RUNTIME / BROWSER_RUNTIME / PROVIDER / DEPLOYMENT`
  reason: offline frozen-artifact evaluation

forbidden:
- action_or_channel: runtime/rerun/new source discovery
  reason: evaluation must remain within frozen accepted corpus
- action_or_channel: protocol redesign
  reason: results phase has started
- action_or_channel: product superiority/generalization claim
  reason: current corpus cannot satisfy stronger publication threshold

proof_non_substitution:
- M05 offline interpretation != runtime re-execution
- baseline recommendation != executed side effect
- M01-M04 exclusion != comparative FAIL
- P2 acceptance != P3 comparative PASS
- one eligible attempt != materially better
- Executor result candidate != Human acceptance

## accept 기준

- protocol SHA exact match
- M05 source packet integrity exact match
- source manifest frozen before score artifacts
- both arm traces generated from same packet
- all primary/secondary metric rows generated under exact rules
- M01-M04 exclusions retained
- deterministic reconstruction check reproducible
- no runtime/provider/network/browser/DB/deployment
- no post-hoc protocol modification
- no forbidden superiority/generalization wording
- result submitted as `HUMAN_PENDING`

## hold/reject 기준

- source manifest created after score/result derivation
- M05 source mismatch or incomplete packet
- baseline reads governance-only decision fields
- governed arm invents missing owner decision
- exclusions scored as PASS/FAIL
- any protocol threshold/metric/comparator changed
- broad source discovery resumes
- runtime/provider/LLM/browser/network/DB invoked
- weighted composite or unsupported superiority claim
- Human result falsely claimed

## mandatory stop 조건

- protocol SHA mismatch
- M05 archive/member/hash/identity mismatch
- matched-condition failure
- missing required M05 source artifact
- source-manifest integrity failure
- policy conflict
- secret/private material encountered
- forbidden action request
- evidence scope expansion required

After a named blocker, perform only minimal blocker evidence, workspace inventory, report/export and safe exit.

## 보고서 필수 항목

- exact protocol hash
- source manifest freeze hash/timestamp
- M05 source integrity result
- M01-M04 exclusions
- both comparator decisions and next actions
- metric raw results
- audit numerator/denominator
- reconstruction determinism
- contrary/tie findings
- publication-condition result
- human pending
- forbidden-not-run
- product/governance/repository-config changes
- rollback/preservation
- unverified/limitations

## export bundle 요구

Target:
`.aiassistant/reports/target/20260915_0145_aiscc-p3-1-frozen-protocol-m05-bounded-comparative-evaluation-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SOURCE_PACKET_MANIFEST.json`
- `COMPARATOR_TRACES.jsonl`
- `RAW_METRICS.jsonl`
- `EXCLUSIONS.json`
- `RECONSTRUCTION_CHECK.json`
- `RESULT_REVIEW.md`
- `RESULT_INTEGRITY.json`
- `REMOVED_FILES.md` only when deletion exists

At terminal executor completion also create:
`.aiassistant/reports/target/20260915_0145_aiscc-p3-1-frozen-protocol-m05-bounded-comparative-evaluation-1.zip`

## 사람 검증 요구

- comparative result: `HUMAN_PENDING`
- Human must review M05 traces/metrics, M01-M04 exclusions, limitations and public claim boundary
- Executor may not mark P3-1 accepted/closed

## 최종 응답 형식

1. result: completed / blocked / rejected-candidate
2. protocol SHA
3. M05 source integrity
4. M05 comparator decisions
5. M05 primary metric summary
6. M01-M04 exclusions
7. publication-condition result
8. target bundle + ZIP
9. changed files
10. human verification
11. limitations/unverified
