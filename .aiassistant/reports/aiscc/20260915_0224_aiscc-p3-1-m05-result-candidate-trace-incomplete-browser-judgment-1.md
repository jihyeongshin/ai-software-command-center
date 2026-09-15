# AISCC Browser Command Center Judgment

## 판정

```text
result_status: HOLD_REWORK_REQUIRED
work_type: QA_ONLY -> REWORK
reject_cause: EXPORT_ARTIFACT_INCOMPLETE
cycle_record_action: create
cycle_record_path: .aiassistant/records/aiscc/cycles/20260915_0224_aiscc-p3-1-m05-result-candidate-trace-incomplete-rework-entry-1.cycle.md
source_mirror_sync: not-required
execution_mode: MANUAL_COMMAND_CENTER
```

## accepted predecessor facts

The following 0145 facts are accepted for rework entry:

- accepted protocol SHA-256 remains `a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6`
- source manifest freeze occurred before score artifact generation
- M05 immutable packet/matched-condition integrity reported PASS
- M01-M04 stayed `EX_SOURCE_MISSING / NOT_COMPARABLE`
- no runtime/provider/LLM/network/browser/DB/deployment execution
- no protocol amendment
- no product superiority claim
- one eligible row means `materially_better_condition_possible = No`

These facts do not equal acceptance of the comparative result.

## blocking defect

`COMPARATOR_TRACES.jsonl` does not satisfy the frozen protocol's reproducibility contract.

Observed from submitted ZIP SHA `3df36f42e85ccd10e800e82d84040c86dad5a691109b106257f48749d57f59a8`:

```text
AISCC_GOVERNED consulted = 1
AISCC_GOVERNED reference_only = 1
AISCC_GOVERNED step ref counts = 1,0,1,0,0

EXECUTOR_REPORT_BASELINE consulted = 1
EXECUTOR_REPORT_BASELINE reference_only = 1
EXECUTOR_REPORT_BASELINE step ref counts = 1,1,0,1,1
```

However the same result candidate claims:
- governed decision inputs: many owner/evidence/judgment/transition/Cycle/NextAction/result refs;
- baseline decision inputs: Task, TaskContract body, executor submission, ordinary candidate evidence;
- audit reconstructability: `10/10` vs `5/10`;
- historical truth and restart results;
- governance overhead: multiple decision/reference artifacts.

The trace therefore cannot currently reproduce those claims.

Additionally, protocol section 4 requires every consulted field to carry a pointer/span, role and hash. The submitted trace does not provide this for every actual evaluator read.

## required rework

Do not change methodology or outcome to repair this.

1. Fix trace construction so every actual evaluator-read decision field is present.
2. Log exact artifact, selector/JSON pointer/text span, semantic role and immutable SHA-256 for each consulted/reference field.
3. Populate every rule-step `refs` from those exact entries; no empty refs for a step whose outcome depends on source data.
4. Make baseline `reference_only` include every reference-truth artifact actually consulted for metrics such as historical preservation.
5. Derive governance-overhead distinct artifact counts from emitted trace entries rather than hard-coded constants.
6. Add validation that fails if:
   - an evaluator field read is absent from trace;
   - trace artifact counts and RAW_METRICS counts disagree;
   - a trace source lacks hash/selector/role;
   - a metric cites a source not represented in trace/reference provenance.
7. Regenerate result artifacts from the same frozen source manifest and same protocol.
8. Preserve raw comparative findings unless the exact same frozen rules deterministically show the predecessor value was mechanically wrong. Any changed result must be explicitly diffed and justified as bug correction, not methodology change.

## Human boundary

Do not ask Human to accept the M05 result yet.

Successful rework should return a new `RESULT_CANDIDATE / HUMAN_PENDING` for Browser review. Only after Browser verifies trace completeness should Human result acceptance be requested.
