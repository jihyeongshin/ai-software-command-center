# 작업지시서: P3-1 M01-M04 pre-result source-packet gap closure and protocol amendment

## meta

- task_id: `20260915_0124_aiscc-p3-1-pre-result-source-packet-gap-closure-and-protocol-amendment-1`
- created_at: `2026-09-15T01:24:14+09:00`
- work_type: `DISCOVERY_AUDIT`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `P3-1 comparative source eligibility / Browser Command Center`

## 현재 상태

- current canonical baseline:
  - `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`
  - accepted SHA-256: `a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6`
  - Human result: `HUMAN_PROVIDED / ACCEPTED`
- repository HEAD observed by predecessor: `82bc047b79cf496280d1b3df6a113f652629a6f5`
- predecessor cycle:
  - `.aiassistant/records/aiscc/cycles/20260915_0124_aiscc-p3-1-comparative-protocol-human-acceptance-source-gap-entry-1.cycle.md`
- known dirty workspace:
  - preserve predecessor-reported untracked governance/provenance; do not clean or mix unrelated dirt
- open blocker:
  - M01-M04 are frozen planned rows but `CORPUS_GAP / EX_SOURCE_MISSING / NOT_COMPARABLE`
  - comparative result has not been generated or viewed

## 이번 턴 목표

1. M01-M04 각각에 대해 frozen protocol이 요구하는 full same-attempt source packet의 존재 여부를 exact accepted P2 provenance 안에서만 read-only로 조사한다.
2. 각 row를 `GAP_RESOLVED_EXACT`, `GAP_PARTIAL`, `GAP_UNRESOLVED` 중 하나로 분류하고 exact source path/object/ref/SHA-256/bytes를 기록한다.
3. 비교 결과를 보지 않은 상태에서 source packet이 exact하게 회수된 row만 protocol amendment candidate로 반영한다.
4. source eligibility가 바뀌면 accepted v1 protocol bytes/hash와 before/after matrix를 보존하고 새 revision을 `HUMAN_PENDING` candidate로 제출한다.
5. 어떤 gap도 exact하게 해소되지 않으면 protocol을 수정하지 않고 gap audit 결과만 제출한다.

## 이번 턴 비목표

- comparative trace, metric, score, aggregate 또는 result 생성
- M05 scoring
- scenario rerun 또는 새 synthetic scenario 작성
- provider/LLM/network/browser/DB/runtime/deployment
- competitor/vendor benchmark
- product/runtime/test source 변경
- P3-2/P3-3 작업
- outcome을 본 뒤 comparator/metric/exclusion/publication threshold 변경

## 허용 범위

allowed_paths:
- `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`
- `.aiassistant/reports/aiscc/replay/stockroom/v1/**`
- `.aiassistant/tasks/done/20260914_0145_aiscc-p2-3-recorded-replay-corpus-capture-and-review-candidate-1.md`
- `.aiassistant/reports/aiscc/20260914_0205_aiscc-p2-3-0145-recorded-replay-corpus-final-acceptance-closure-authorization-1.md`
- `.aiassistant/records/aiscc/cycles/**` only when reached by exact P2 refs or exact M01-M04 run/fingerprint identity
- `.aiassistant/tasks/done/**` only for exact M01-M04 identifiers/run IDs/fingerprints or exact paths discovered from accepted P2 refs
- `.aiassistant/reports/aiscc/**` only for exact M01-M04 identifiers/run IDs/fingerprints or exact paths discovered from accepted P2 refs
- current Task/report/target bundle paths

exact frozen row identities:
- M01:
  - scenario: `stockroom-s1-normal@1.0.0`
  - run: `aiscc-p2-3-private-s1-normal-v5-run`
  - replay fingerprint: `a58d3a54a1c58a32d4fbca51d32e8e0a7536e52f6bd197a54f87741ab8478e34`
  - execution commit: `e7d7a44379eb0dc71f7b8d2207c6ca3719a0a211`
- M02:
  - scenario: `stockroom-s2-missing-evidence@1.0.0`
  - run: `aiscc-p2-3-private-s2-missing-evidence-v6-run`
  - replay fingerprint: `9338b5a87d0d1d7bf7f8b624b055271de152fc94b048fbabac15c1bbb9c75e5b`
  - execution commit: `33a216f29062176ad196a567a299ba30291c3f72`
- M03:
  - scenario: `stockroom-s3-policy-conflict@1.0.0`
  - run: `aiscc-p2-3-private-s3-policy-conflict-v9-run`
  - replay fingerprint: `1cbcf87ed3a94f32e1988883002805d315937a8f050538a5c1c286feddd8e9fa`
  - execution commit: `a1c934ea75906a548f2bc4adc777c2a0ecc99be5`
- M04:
  - scenario: `stockroom-s4-human-owned-claim@1.0.0`
  - run: `aiscc-p2-3-private-s4-human-owned-claim-v10-run`
  - replay fingerprint: `96d4c2601306e2fdb9f5119538f198d77e0a0e3765f46a4aa2c39419bd3de422`
  - execution commit: `a1c934ea75906a548f2bc4adc777c2a0ecc99be5`

allowed_actions:
- exact file read/hash/size checks
- bounded literal search for the exact run IDs/scenario IDs/fingerprints above inside allowed governance paths
- read-only Git object inspection at the three exact execution commits:
  - `git show`
  - `git ls-tree`
  - `git cat-file`
  - `git grep <exact-id> <exact-commit> -- <allowed governance paths>`
  - `git rev-parse`
- inspect an exact historical artifact/archive path only when that exact path is named by an accepted P2 canonical record reached through the bounded chain above
- deterministic JSON/Markdown validation
- protocol amendment candidate only under the amendment rules below

## 절대 금지

forbidden_paths:
- product/runtime/test source except path names/hashes already embedded in accepted provenance
- credentials, env files, private/customer source
- unrelated `.aiassistant` history
- arbitrary Downloads/archive inventory beyond this delivery ZIP
- broad `.git` history/object enumeration

forbidden_actions:
- `git log --all`, broad `git grep` without exact frozen identifiers, repository-wide history mining
- checkout/reset/restore/clean
- Git index / commit / push / deployment
- DB/container/runtime startup or reconstruction
- provider/LLM/network/browser/credentialed access
- scenario replay/rerun or source regeneration
- current source or a similar run used as substitute for the exact historical packet
- summaries/hashes used as substitute for missing body bytes
- comparative score/result/decision generation
- comparator/metric/exclusion/publication-threshold redesign
- Human acceptance claim by Executor

## 읽을 문서

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`
- `.aiassistant/records/aiscc/cycles/20260915_0124_aiscc-p3-1-comparative-protocol-human-acceptance-source-gap-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_0124_aiscc-p3-1-comparative-protocol-human-acceptance-browser-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_0124_aiscc-browser-command-center-p3-1-protocol-accepted-source-gap-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260914_0145_aiscc-p2-3-recorded-replay-corpus-capture-and-review-candidate-1.md`
- `.aiassistant/reports/aiscc/20260914_0205_aiscc-p2-3-0145-recorded-replay-corpus-final-acceptance-closure-authorization-1.md`
- `.aiassistant/reports/aiscc/replay/stockroom/v1/REPLAY_CORPUS_INDEX.json`
- four exact Replay members for S1-S4

## agent instruction transport / authority

- repository-root instruction entrypoint는 thin transport bootstrap이며 policy authority가 아니다.
- Task File 목록은 minimum authoritative context set이다.
- unrelated source/log/history를 bulk-read하지 않는다.
- accepted protocol SHA가 `a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6`와 다르면 mutation 없이 `POLICY_CONFLICT_INVESTIGATION_REQUIRED`로 STOP한다.
- comparative result 파일/trace/metric이 이미 생성되었거나 본 Task 수행 중 우연히 발견되어 결과를 관측했다면 amendment를 중단하고 `RESULT_ACCESS_BEFORE_AMENDMENT`로 보고한다.
- Human-owned methodology acceptance를 Executor가 대신하지 않는다.

## 조사할 source

Exact bounded chain only:

1. accepted protocol section 5/6/9/14/15
2. P2-3 0145 Task exact mapping
3. P2-3 0205 acceptance exact refs
4. current canonical Replay index + S1-S4 exact members
5. exact frozen execution commit for each row
6. exact literal run/scenario/fingerprint search inside allowed governance paths/tree
7. only exact paths reached from 1-6

Do not branch into speculative neighboring tasks/runs.

## 구현/문서/감사 범위

### Required target evidence

Create in target bundle:

- `SOURCE_PACKET_GAP_AUDIT.md`
- `evidence/SOURCE_PACKET_STATUS.json`
- `evidence/RESULT_ACCESS_DECLARATION.json`
- `evidence/BOUNDED_SEARCH_TRACE.json`
- `evidence/SOURCE_PACKET_HASHES.json` when any candidate body exists

For each M01-M04 record:

```text
row_id
frozen_run_id
frozen_execution_commit
status = GAP_RESOLVED_EXACT | GAP_PARTIAL | GAP_UNRESOLVED
task_input_ref/path/object + sha256 + bytes or MISSING
executor_output_ref/path/object + sha256 + bytes or MISSING / STRUCTURALLY_NONE
candidate_body_ref/path/object + sha256 + bytes or MISSING / STRUCTURALLY_NONE
same_attempt_binding_evidence
accepted_provenance_chain
why exact matched-condition is or is not satisfied
```

`STRUCTURALLY_NONE` is permitted only where the original Task/attempt semantics prove no such output/body should exist; absence must not be invented from Replay summary alone.

### Amendment rule

Amend the canonical protocol only if all are true:

1. no comparative result/metric/trace has been generated or viewed;
2. an exact previously missing original packet body/ref is recovered from authorized accepted P2 provenance;
3. immutable identity/hash/bytes and same-attempt binding are verified;
4. the change affects source identity/eligibility only;
5. comparator, metric, exclusion codes, publication rule and thresholds are unchanged.

If amendment occurs:

- preserve the accepted v1 exact bytes as:
  `.aiassistant/reports/aiscc/20260915_0124_AISCC_COMPARATIVE_EVALUATION_PROTOCOL_V1_ACCEPTED.md`
- verify its SHA-256 is exactly `a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6`
- update `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`
- revision must become a new explicit pre-result amendment revision
- record accepted-v1 SHA, candidate-v2 SHA, exact before/after rows and discovery reason
- keep M01-M04 membership fixed; only source refs/eligibility may change
- mark methodology result `HUMAN_PENDING`
- DO NOT score any row after amendment

If no exact gap is resolved:

- do not change the canonical protocol
- do not create the accepted-v1 preservation copy solely for ceremony
- report the four statuses and recommend the next action without scoring

## workflow transition expectation

- initial_state: `MANUAL_COMMAND_CENTER / protocol accepted / pre-result source audit`
- expected_non_terminal_state_when_human_pending: `protocol amendment candidate / HUMAN_PENDING`
- expected_terminal_candidate:
  - `AUDIT_COMPLETE_NO_AMENDMENT`, or
  - `AMENDMENT_CANDIDATE_HUMAN_PENDING`
- transition_authority: `NOT_APPLICABLE`
- Agent가 직접 terminal comparative state를 결정할 수 있는가: `No`

## evidence contract

executor_required:
- channel: `STATIC_SOURCE / PUBLIC_PROVENANCE`
  scope: exact source-packet discovery and immutable binding for M01-M04
  allowed_command_or_environment: local read-only repository/Git object inspection bounded above
  pass_condition: every row receives one exact gap status with reproducible refs/hashes and no broad search
- channel: `CONFORMANCE`
  scope: no result access, no scoring, no metric/comparator mutation
  allowed_command_or_environment: deterministic text/JSON/hash checks
  pass_condition: all frozen methodology rules remain unchanged except permitted source-eligibility amendment

reuse_allowed:
- channel: `PUBLIC_PROVENANCE`
  predecessor: accepted P2-3/P2-4 corpus and accepted 0054 protocol
  provenance_condition: exact accepted refs/hash match
  applicability_condition: source identity/binding only, not comparative outcome

human_owned:
- channel: `HUMAN_VERIFICATION`
  scope: any amended protocol revision/source eligibility
  expected_result_format: `ACCEPTED | REWORK | REJECTED`
  note: if no protocol amendment occurs, methodology Human re-review is not automatically required

not_required:
- channel: `DATABASE_RUNTIME / HTTP_RUNTIME / BROWSER_RUNTIME / PROVIDER / DEPLOYMENT`
  reason: source-gap audit is offline read-only provenance work

forbidden:
- action_or_channel: comparative result/score generation
  reason: pre-result amendment gate must close first
- action_or_channel: scenario rerun/new scenario
  reason: frozen matrix cannot be repaired by new execution
- action_or_channel: broad history/archive/private-runtime search
  reason: violates bounded source-integrity contract

proof_non_substitution:
- Replay summary/hash != missing original Task/output/candidate body
- current source != historical same-attempt packet
- similar run != frozen row
- source availability != comparative PASS/FAIL
- protocol amendment candidate != Human acceptance
- Human acceptance of v1 != automatic acceptance of amended v2

## conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant: accepted protocol sections 4, 6, 8, 9, 13, 14, 15
- required_actual_owner: `Browser Command Center / Human for amended methodology`
- planned_vs_actual_scope: exact frozen four-row source audit only
- rollback_or_failure_semantics: if mutation preconditions fail, preserve v1 unchanged and submit audit only

## project context impact

architecture:
- `NONE`

orchestration_contract:
- `NONE`

security_sandbox:
- `NONE`

public_provenance:
- `CANONICAL_UPDATE_REQUIRED` only if protocol amendment candidate is produced; otherwise Task/Cycle only

## accept 기준

- exact accepted protocol SHA verified before audit
- comparative result access declaration = `NOT_VIEWED / NOT_GENERATED`
- bounded search trace contains only authorized exact refs/commits/identifiers
- M01-M04 each has a reproducible gap status
- no synthesized/current/similar-run substitution
- protocol changes, if any, are source-identity/eligibility-only and preserve v1 exact bytes/hash
- no comparative metric/score/result generated

## hold/reject 기준

- broad history/archive/private runtime search used
- result or metric observed before amendment completion
- protocol metric/comparator/exclusion/publication rule changed
- missing body inferred from summaries as if exact
- new run/scenario used to fill a frozen gap
- current source/similar run substituted for same-attempt source
- Human acceptance falsely claimed

## mandatory stop 조건

- accepted protocol SHA mismatch
- required accepted P2 artifact missing
- `RESULT_ACCESS_BEFORE_AMENDMENT`
- source identity conflict
- secret/private material encountered
- dirty workspace collision affecting allowed governance paths
- forbidden action/tool request
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`
- Human decision required before further mutation

Named blocker 이후에는 blocker를 입증하는 최소 evidence, workspace inventory, report/export와 안전한 종료만 수행한다.

## 보고서 필수 항목

- 작업명 / work type / task path
- read canonical paths
- exact bounded search commands/objects
- source inventory
- M01-M04 per-row gap status
- result-access declaration
- protocol v1 hash verification
- protocol amendment 여부와 before/after hash
- product source changes
- governance/provenance changes
- repository configuration changes
- evidence contract와 실제 result classification
- Agent claim vs admitted evidence
- human pending/provided
- forbidden-not-run
- mandatory stop/scope expansion
- unverified items
- rollback/revert guide
- preserved artifact exact paths
- next bounded recommendation

## export bundle 요구

Target:
`.aiassistant/reports/target/20260915_0124_aiscc-p3-1-pre-result-source-packet-gap-closure-and-protocol-amendment-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- required target evidence listed above
- changed canonical files preserving project-relative paths
- `REMOVED_FILES.md` only when actual project deletion exists

At terminal executor completion also create:
`.aiassistant/reports/target/20260915_0124_aiscc-p3-1-pre-result-source-packet-gap-closure-and-protocol-amendment-1.zip`

## 사람 검증 요구

- protocol amendment가 발생하면: `HUMAN_PENDING`
- protocol amendment가 없고 audit-only이면: separate methodology re-acceptance is not required by this Task
- comparative result acceptance: not applicable / not yet generated

## 최종 응답 형식

1. result: completed / blocked / rejected-candidate
2. M01-M04 gap statuses
3. protocol changed: yes/no
4. accepted-v1 SHA and candidate-v2 SHA if applicable
5. target bundle path + ZIP path
6. changed files
7. removed files
8. human verification
9. unverified items
10. preserved exact paths
