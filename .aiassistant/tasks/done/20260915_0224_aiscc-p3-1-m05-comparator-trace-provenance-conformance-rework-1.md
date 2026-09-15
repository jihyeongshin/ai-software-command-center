# 작업지시서: P3-1 M05 comparator trace provenance conformance rework

## meta

- task_id: `20260915_0224_aiscc-p3-1-m05-comparator-trace-provenance-conformance-rework-1`
- created_at: `2026-09-15T02:24:00+09:00`
- work_type: `REWORK`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `P3-1 comparative result reproducibility / Browser Command Center`

## 현재 상태

- accepted protocol:
  - `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`
  - exact SHA-256 `a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6`
- predecessor M05 result Task:
  - `.aiassistant/tasks/done/20260915_0145_aiscc-p3-1-frozen-protocol-m05-bounded-comparative-evaluation-1.md`
- predecessor result target:
  - `.aiassistant/reports/target/20260915_0145_aiscc-p3-1-frozen-protocol-m05-bounded-comparative-evaluation-1/`
- predecessor outbound ZIP:
  - `.aiassistant/reports/target/20260915_0145_aiscc-p3-1-frozen-protocol-m05-bounded-comparative-evaluation-1.zip`
- submitted predecessor ZIP SHA-256:
  - `3df36f42e85ccd10e800e82d84040c86dad5a691109b106257f48749d57f59a8`
- predecessor source-manifest freeze tuple SHA:
  - `cdff08aa196d828db03ebacbdbefb05c1431b0e5b2bad3247c7c5db5d1a18cb9`
- Browser judgment:
  - `HOLD_REWORK_REQUIRED / EXPORT_ARTIFACT_INCOMPLETE`
- comparative result:
  - observed but `NOT_ACCEPTED`
- protocol amendment:
  - forbidden after result observation

## 이번 턴 목표

1. predecessor frozen source manifest and protocol hashes를 exact verify한다.
2. predecessor evaluator의 comparator trace provenance serialization defect를 수정한다.
3. 실제 evaluator가 읽는 모든 decision/reference field를 exact artifact + selector/pointer/span + role + immutable SHA-256으로 trace에 기록한다.
4. ordered comparator rule step의 source-dependent outcome마다 non-empty exact `refs`를 기록한다.
5. metric provenance가 해당 trace/source-manifest entry로 기계적으로 resolve되는지 검증한다.
6. `GOVERNANCE_OVERHEAD` artifact counts를 hard-coded constant가 아니라 emitted trace의 distinct artifact identity에서 derive한다.
7. 동일 frozen packet/protocol 아래 comparator와 metrics를 다시 deterministic regenerate한다.
8. predecessor result와 corrected result를 exact diff한다.
9. methodology 변경 없이 재현성 artifact만 고친 `RESULT_CANDIDATE / HUMAN_PENDING`을 제출한다.

## 이번 턴 비목표

- protocol 수정/amendment/revision
- comparator rule 수정
- metric definition/scoring rule 수정
- matrix/exclusion/publication threshold 변경
- M01-M04 재탐색
- M05 source discovery 확대
- scenario rerun/new run
- DB/runtime/provider/LLM/network/browser/deployment
- product/runtime/test/canonical source 변경
- 결과가 유리하도록 값 변경
- superiority/generalization claim
- Git index/commit/push

## 허용 범위

allowed_paths:
- `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md` read-only
- predecessor 0145 target folder read-only as input
- predecessor 0145 target ZIP read-only as integrity input
- exact M05 frozen packet refs already recorded in predecessor `SOURCE_PACKET_MANIFEST.json`
- current Task/target output folder
- supplied current Cycle/Judgment/Handoff

allowed_actions:
- exact file/hash/size checks
- predecessor result JSON/JSONL/Markdown parse
- exact already-frozen M05 archive/member read
- exact already-frozen result commit/blob integrity check
- edit/rewrite evaluator only inside the new temporary target bundle
- deterministic offline regeneration
- JSON/JSONL schema/integrity validation
- result-before/after diff generation

## 절대 금지

forbidden_actions:
- source manifest identity expansion
- broad Git/history/archive/filesystem search
- current source substitution
- protocol amendment
- scoring-rule/comparator/exclusion redesign
- P2 runtime/scenario execution
- any provider/LLM/network/browser/DB/runtime/deployment call
- manual outcome editing
- Human acceptance claim
- weighted composite/significance/generalization
- Git add/commit/push

## 읽을 문서

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`
- `.aiassistant/records/aiscc/cycles/20260915_0224_aiscc-p3-1-m05-result-candidate-trace-incomplete-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_0224_aiscc-p3-1-m05-result-candidate-trace-incomplete-browser-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_0224_aiscc-browser-command-center-p3-1-m05-trace-conformance-rework-entry-handoff-1.md`
- predecessor 0145:
  - `SOURCE_PACKET_MANIFEST.json`
  - `COMPARATOR_TRACES.jsonl`
  - `RAW_METRICS.jsonl`
  - `EXCLUSIONS.json`
  - `RECONSTRUCTION_CHECK.json`
  - `RESULT_REVIEW.md`
  - `RESULT_INTEGRITY.json`
  - `OFFLINE_EVALUATOR.ps1`
  - `VALIDATION.json`
  - `EXECUTOR_REPORT.md`

## exact defect assertions to reproduce before mutation

Before writing corrected artifacts, prove and record:

```text
predecessor governed consulted count = 1
predecessor governed reference_only count = 1
predecessor governed ordered-step ref counts = [1,0,1,0,0]

predecessor baseline consulted count = 1
predecessor baseline reference_only count = 1
predecessor baseline ordered-step ref counts = [1,1,0,1,1]
```

Also record that predecessor RAW_METRICS claims:
- governed decision-input artifact count = 11
- baseline decision-input artifact count = 4
- total packet artifacts consulted = 12 per arm

If the exact predecessor does not reproduce these facts, STOP `SOURCE_IDENTITY_CONFLICT`.

## corrected trace contract

Every actual evaluator-read field that contributes to comparator decision, metric, reconstruction, historical-truth, restart or overhead must be represented by an entry with at least:

```json
{
  "artifact": "<stable source identity>",
  "artifact_sha256": "<exact SHA-256>",
  "selector": "<JSON pointer / text span / whole immutable blob>",
  "role": "decision_input | executor_report | governance_fact | reference_only | comparator_rule",
  "used_by": ["<rule or metric identifiers>"]
}
```

Rules:

- archive member hash = exact member hash from frozen `SOURCE_PACKET_MANIFEST.json`
- Task hash = frozen source Task hash
- git deliverable = frozen deliverable SHA
- acceptance anchors = their exact individual frozen hashes
- protocol rule refs = protocol SHA
- do not use a container temp-copy hash as the semantic artifact identity if the frozen source identity already exists
- duplicate selectors may reference one canonical trace-source entry by stable trace source ID
- each source-dependent `ordered_rule_step.refs` must resolve to one or more trace source IDs
- every `RAW_METRICS` provenance source must resolve to trace source ID(s) or an explicit protocol-rule source
- baseline governance reference-truth used for HISTORICAL_TRUTH_PRESERVATION must be visible as `reference_only`, never baseline decision input

## artifact-count derivation

Do not hard-code:

```text
total_packet_artifacts_consulted
decision_input_artifacts
reference_only_artifacts
```

Derive from distinct immutable artifact identities actually emitted for that arm.

State the counting rule exactly, including:
- whether the two P2 acceptance anchors count as two artifacts;
- how an artifact used both as decision input and reference-only selectors is counted;
- whether protocol itself is included or excluded from `packet artifacts`;
- how git blob/deliverable identity is counted.

`RAW_METRICS` and `RESULT_REVIEW` counts must equal the machine-derived trace counts.

## result preservation / correction rule

Results have already been viewed.

Therefore:

- protocol hash must remain `a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6`;
- source-manifest frozen identities must remain unchanged;
- M01-M04 exclusions must remain unchanged;
- comparator/metric/publication rules must remain unchanged.

Expected predecessor semantic values to regression-check, not blindly force:

```text
AISCC_GOVERNED decision: ACCEPTED
EXECUTOR_REPORT_BASELINE decision: UNRESOLVED

TRUTHFUL_TERMINAL_OUTCOME: PASS / PASS
EVIDENCE_INTEGRITY: PASS / PASS
AUTHORITY_SEPARATION: PASS / PASS
FAIL_CLOSED_BEHAVIOR: N/A / N/A
AUDIT_RECONSTRUCTABILITY: 10/10 / 5/10
RESTART_RECOVERABILITY: PASS / FAIL
HISTORICAL_TRUTH_PRESERVATION: PASS / PASS
DETERMINISTIC_PROJECTION: PASS / PASS
materially_better_condition_possible: No
```

If corrected evaluator under unchanged rules produces any semantic difference:
- do not suppress it;
- emit `RESULT_VALUE_DIFF.md`;
- identify exact predecessor bug and source pointers;
- keep both before/after values;
- classify `RESULT_CANDIDATE / HUMAN_PENDING`;
- do not modify methodology to restore the old value.

If only descriptive GOVERNANCE_OVERHEAD artifact counts change because the prior hard-coded counts were wrong, report that as a provenance-count correction, not a semantic comparator-rule change.

## required output artifacts

New target bundle must contain:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SOURCE_PACKET_MANIFEST.json` — byte-identical predecessor copy preferred; exact hash must match
- `COMPARATOR_TRACES.jsonl`
- `RAW_METRICS.jsonl`
- `EXCLUSIONS.json`
- `RECONSTRUCTION_CHECK.json`
- `RESULT_REVIEW.md`
- `RESULT_INTEGRITY.json`
- `OFFLINE_EVALUATOR.ps1`
- `TRACE_CONFORMANCE.json`
- `PREDECESSOR_RESULT_DIFF.json`
- `VALIDATION.json`
- `TERMINAL_WORKSPACE.json`
- `RESULT_VALUE_DIFF.md` only if any semantic result changes
- `REMOVED_FILES.md` only if actual project deletion exists

## TRACE_CONFORMANCE.json minimum checks

```text
all_actual_evaluator_reads_traced = true
all_trace_sources_have_sha_selector_role = true
all_source_dependent_steps_have_refs = true
all_step_refs_resolve = true
all_metric_provenance_resolves = true
baseline_reference_only_governance_not_used_as_decision_input = true
trace_derived_artifact_counts_match_raw_metrics = true
trace_derived_artifact_counts_match_result_review = true
source_manifest_hash_unchanged = true
protocol_hash_unchanged = true
M01_M04_exclusions_unchanged = true
```

Include actual counts and any duplicate-artifact normalization details.

## evidence contract

executor_required:
- channel: `CONFORMANCE`
  scope: predecessor defect reproduction + complete corrected trace provenance
  pass_condition: all TRACE_CONFORMANCE checks true
- channel: `QA_ONLY / COMPARATIVE_EVALUATION`
  scope: deterministic regeneration under exact frozen protocol/source packet
  pass_condition: result artifacts regenerate consistently and any value delta is explicitly justified as mechanical bug correction
- channel: `PUBLIC_PROVENANCE`
  scope: before/after artifact hashes and semantic result diff
  pass_condition: exact predecessor/result lineage reconstructable

reuse_allowed:
- channel: `STATIC_SOURCE / PUBLIC_PROVENANCE`
  predecessor: accepted protocol and frozen M05 source packet
  provenance_condition: exact hashes unchanged
  applicability_condition: same evaluation only

human_owned:
- channel: `HUMAN_VERIFICATION`
  scope: corrected comparative result interpretation/acceptance and public wording
  expected_result_format: `ACCEPTED | REWORK | REJECTED`

not_required:
- channel: `DB / HTTP / BROWSER / PROVIDER / DEPLOYMENT`
  reason: offline result-artifact rework only

forbidden:
- protocol/methodology change
- source expansion
- scenario/runtime rerun
- Human acceptance claim

proof_non_substitution:
- trace completeness != result acceptance
- same result values != trace conformance
- source manifest != per-field comparator trace
- reference-only governance fact != baseline decision input
- deterministic regeneration != independent external validation

## accept 기준

- predecessor exact defect reproduced
- protocol/source manifest identities unchanged
- corrected trace contains every actual evaluator-read field with exact hash/selector/role
- no source-dependent comparator step has empty refs
- all metric provenance resolves
- governance overhead counts are trace-derived and reconcile everywhere
- deterministic regeneration PASS
- M01-M04 unchanged
- no forbidden execution or methodology mutation
- result remains `RESULT_CANDIDATE / HUMAN_PENDING`

## hold/reject 기준

- trace still omits evaluator-read fields
- any source-dependent rule step has unresolved/empty refs
- artifact counts remain hard-coded or disagree
- metric provenance cannot be resolved
- source/protocol/matrix changes
- result value silently changes
- source discovery/runtime/external action occurs
- Human result falsely claimed

## mandatory stop 조건

- protocol hash mismatch
- predecessor source-manifest identity mismatch
- predecessor defect cannot be reproduced
- M05 frozen source mismatch
- methodology/source expansion required
- secret/private material encountered
- forbidden action request

Named blocker 이후에는 최소 evidence, workspace inventory, report/export와 안전한 종료만 수행한다.

## export bundle

Target:
`.aiassistant/reports/target/20260915_0224_aiscc-p3-1-m05-comparator-trace-provenance-conformance-rework-1/`

Terminal ZIP:
`.aiassistant/reports/target/20260915_0224_aiscc-p3-1-m05-comparator-trace-provenance-conformance-rework-1.zip`

## 사람 검증 요구

- rework 자체의 trace conformance는 Executor + Browser가 먼저 판정
- 성공한 corrected comparative result는 다시 `HUMAN_PENDING`
- Human acceptance는 Browser가 corrected bundle을 확인한 뒤에만 요청

## 최종 응답 형식

1. result
2. predecessor defect reproduced
3. protocol/source-manifest identity
4. trace conformance summary
5. trace-derived artifact counts
6. semantic result before/after diff
7. M01-M04 exclusions
8. publication condition
9. target bundle + ZIP
10. human verification
11. limitations/unverified
