# 작업지시서: P3-3 L6 Integrated Runtime / Adversarial Verification

## meta

- task_id: `20260918_0822_aiscc-p3-3-l6-integrated-runtime-adversarial-verification-1`
- created_at: `2026-09-18T08:22:00+09:00`
- work_type: `L6_INTEGRATED_RUNTIME_ADVERSARIAL_VERIFICATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER / THIN_CC_THICK_EXECUTOR`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `Browser Command Center + Human`
- fresh_ide_executor_chat: `NOT_REQUIRED`

## 현재 상태

- current canonical baseline before inbound Browser artifacts: `6239e4b3c8ae1b84ac4604ddf66987fb50225462`
- Browser judgment in this delivery: `L5 ACCEPTED / CLOSED`
- L3: `ACCEPTED / CLOSED` under 0445 lineage
- L4: `ACCEPTED / CLOSED` under 1352 lineage
- L5: `ACCEPTED / CLOSED` under attached 0822 Cycle/Judgment
- frozen L6 dependency join: `SATISFIED`
- Public admission: `DISABLED`
- Public Live: `NOT_RELEASED`
- Replay: `DEPLOYED / VERIFIED / HUMAN_ACCEPTED`
- frozen scenario: `stockroom-s1-normal / 1.0.0`
- hosted migration head entering L6: `20260918_0023`
- real provider/OpenAI calls authorized by this Task: `0`
- known current governance projection: still says `L5 TERMINAL_ACCEPTANCE_CANDIDATE`; update it to the attached Browser terminal acceptance before final export
- known dirty workspace before delivery: clean tracked workspace at `6239e4b3...`; delivery placement itself is expected governance dirt

## 이번 턴 목표

1. Verify the delivery ZIP SHA-256 and place the attached 0822 Cycle/Judgment/Handoff/Task at their exact canonical paths.
2. Read this Task first, then read the minimum canonical authority listed below.
3. Persist the Browser L5 terminal acceptance in `CURRENT_STATE_SUMMARY.md`, `DECISION_REGISTER.md`, and `NEXT_ACTIONS.md` without rewriting historical 0056/0317 records.
4. Execute L6 `Integrated runtime and adversarial verification` against the frozen `AISCC_PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`.
5. Produce an explicit T01-T35 result matrix using the required proof type for each case.
6. Execute the real AISCC production owner/runtime chain with the frozen synthetic provider transport and exact `stockroom-s1-normal / 1.0.0` corpus pin.
7. Demonstrate multi-worker/multi-process restart and unknown-send bounds, global-cap non-bypass, and Replay independence.
8. Reuse accepted L5 release-only hosted proof where the frozen matrix explicitly permits reuse and no affected path changed.
9. If an actual L6 matrix failure reveals a concrete implementation defect inside already-frozen semantics, make the narrowest in-scope correction, add a regression test, and rerun the affected matrix plus directly impacted regression.
10. Return `L6_TERMINAL_ACCEPTANCE_CANDIDATE` only when every frozen L6 exit criterion has current valid evidence and the final safe state is preserved.

## 이번 턴 비목표

- real OpenAI/provider canary;
- Public admission enablement;
- Public Live release;
- L7 frontend integration;
- L8 Human release;
- production-grade HA/DR/autoscaling/observability/RBAC/SLO work;
- architecture cleanup solely for elegance or long-term maintenance;
- re-running accepted hosted edge proof merely for reassurance.

## inbound canonical artifacts

Place exactly:

- `.aiassistant/records/aiscc/cycles/20260918_0822_aiscc-p3-3-l5-terminal-acceptance-l6-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260918_0822_aiscc-p3-3-l5-terminal-closure-final-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260918_0822_aiscc-browser-command-center-l5-terminal-acceptance-l6-entry-handoff-1.md`
- `.aiassistant/tasks/active/20260918_0822_aiscc-p3-3-l6-integrated-runtime-adversarial-verification-1.md`

If a destination already exists, require byte-exact identity. Mismatch => `CANONICAL_PLACEMENT_CONFLICT` and STOP.

## 허용 범위

allowed_paths:
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- attached 0822 Cycle/Judgment/Handoff canonical paths
- current Task active -> done
- `.aiassistant/reports/target/**`
- `src/aiscc/public_live/**` only if a concrete L6 failure requires an already-frozen semantic correction
- directly affected `src/aiscc/persistence/**`, `src/aiscc/runtime/**`, `src/aiscc/providers/**`, `src/aiscc/security/**` only for a proven L6 defect
- directly affected tests under `tests/**`
- existing Public Live migrations only by a new forward migration when an already-frozen invariant cannot otherwise be implemented and no new policy is introduced

allowed_actions:
- local/disposable PostgreSQL and deterministic clock harness
- multiple local worker/process instances with barriers/crash points
- synthetic provider transport/provider double
- actual AISCC production owner/runtime composition with synthetic provider
- local container/sandbox execution already supported by the repository
- read-only fetch of the deployed Replay when useful for T24; no Cloudflare mutation
- exact changed-path test/static/type/format checks
- broader repository regression only when actual changed-path blast radius or Task acceptance requires it
- Git add/commit/push after required verification
- passive observation of Railway autodeploy caused by an authorized push; no Railway configuration mutation

## 절대 금지

forbidden_paths/actions:
- real OpenAI/provider request
- reading/exporting raw provider secret
- inserting a new provider credential into worker or proof harness
- Public admission enablement
- Public Live release
- L7/L8 entry
- new Railway service/database/resource or new material paid external resource
- Railway role/domain/variable/scale/redeploy mutation solely to collect L6 evidence
- Cloudflare mutation/redeploy
- broad DB/runtime role expansion
- new frozen semantic/security policy
- destructive reset of accepted hosted state/evidence
- free-form scenario/model/provider/budget changes
- unrelated product cleanup or production hardening
- force push, rebase, history rewrite

## 읽을 문서

Minimum authoritative context:

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
- `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/cycles/20260918_0822_aiscc-p3-3-l5-terminal-acceptance-l6-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260918_0822_aiscc-p3-3-l5-terminal-closure-final-acceptance-judgment-1.md`
- `.aiassistant/reports/aiscc/20260918_0822_aiscc-browser-command-center-l5-terminal-acceptance-l6-entry-handoff-1.md`

Read additional accepted Cycle/Judgment/source only when needed to establish exact reused provenance or investigate an actual matrix failure. Do not bulk-read unrelated history.

## agent instruction transport / authority

- repository-root instruction entrypoint is transport bootstrap, not policy authority.
- automatic retrieval does not substitute for explicit Task-listed canonical reads.
- this Task and the attached Browser judgment authorize L6 entry only.
- accepted L3/L4/L5 semantics remain closed unless an exact contradiction is discovered.
- an implementation mechanism may differ from older Browser expectations if the same frozen semantic/risk boundary and proof type are preserved.
- Agent claim is not Browser acceptance.
- do not mark L6 accepted/closed yourself.

## L6 frozen exit criteria

Canonical `AISCC_PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`:

1. all `AISCC_PUBLIC_LIVE_SECURITY_TEST_MATRIX.json` cases pass in an authorized isolated environment;
2. real owner chain and synthetic corpus pin verified;
3. multi-replica restart and unknown-send limits proven;
4. no global caps bypass and no Replay coupling.

Interpretation:
- `real owner chain` means production AISCC owner/runtime composition, not a real paid provider.
- matrix deterministic/synthetic cases do not require real OpenAI.
- release-only L5 evidence may be reused only with exact provenance/applicability.

## evidence contract

executor_required:

- channel: `L5_ACCEPTANCE_PERSISTENCE`
  scope: `persist attached 0822 Browser Cycle/Judgment/Handoff and reconcile current-state projection to L5 ACCEPTED/CLOSED + L6 ACTIVE`
  allowed_command_or_environment: `repository-local governance files and Git`
  pass_condition: `historical 0056/0317 records preserved; current projection is unambiguous`

- channel: `L6_SECURITY_MATRIX`
  scope: `T01-T35 explicit case-by-case execution/admission matrix`
  allowed_command_or_environment: `authorized isolated local/disposable runtime; synthetic transport`
  pass_condition: `every case classified EXECUTED_PASS or exact REUSED_ACCEPTED where release-only reuse is semantically valid; no silent skip`

- channel: `L6_OWNER_CHAIN_CORPUS_PIN`
  scope: `production Public Live owner/runtime chain with exact frozen scenario/version and synthetic provider`
  allowed_command_or_environment: `real production composition + synthetic provider transport`
  pass_condition: `scenario/corpus/operation ownership is exact; no test-only alternate owner path substitutes`

- channel: `L6_MULTI_REPLICA_UNKNOWN_SEND`
  scope: `multiple independent worker/process connections, crash/restart, marker/send uncertainty and no-blind-resend bounds`
  allowed_command_or_environment: `PostgreSQL + barriers/processes/provider double`
  pass_condition: `frozen T10-T14/T25/T26 semantics hold with physical receipt truth`

- channel: `L6_CAPS_REPLAY_INDEPENDENCE`
  scope: `global/client/hour/day/campaign/slot/paid-call caps and Replay decoupling`
  allowed_command_or_environment: `isolated runtime + Replay read-only verification`
  pass_condition: `caps cannot be reset/bypassed by alternate client identity/time/retry path; Replay remains available/unchanged under Live failure`

- channel: `FINAL_SAFE_STATE`
  scope: `admission disabled; Live not released; Replay unchanged; zero real provider calls; no secret export; no temporary authority residue`
  pass_condition: `all preserved boundaries hold at Task exit`

reuse_allowed:

- channel: `L3_TERMINAL`
  predecessor: `20260916_0445 L3 terminal acceptance`
  provenance_condition: `exact accepted Cycle/Judgment and unchanged affected owner paths`
  applicability_condition: `reuse only for unchanged L3 semantics, not current L6 runtime behavior`

- channel: `L4_TERMINAL`
  predecessor: `20260916_1352 L4 terminal closure`
  provenance_condition: `exact accepted provider-profile/pricing compatibility record`
  applicability_condition: `does not authorize a real provider call`

- channel: `L5_RELEASE_ONLY`
  predecessor: `0822 L5 terminal acceptance; 0201 hosted ingress/edge matrix`
  provenance_condition: `exact accepted hosted proof and current affected-path applicability`
  applicability_condition: `reuse only for release-only edge/sandbox facts that the frozen matrix does not require to be re-executed in L6`

human_owned:

- channel: `REAL_PROVIDER_CANARY`
  scope: `physical paid provider request / production provider credential use`
  expected_result_format: `HUMAN_PENDING unless separately authorized later`

- channel: `PUBLIC_RELEASE`
  scope: `admission enablement / Public Live release / L8 decision`
  expected_result_format: `HUMAN_PENDING`

not_required:

- channel: `L7_FRONTEND`
  reason: `L7 is a later separately authorized phase`

- channel: `PRODUCTION_HARDENING`
  reason: `competition-grade sufficiency; not an L6 exit criterion`

forbidden:

- action_or_channel: `REAL_PROVIDER_CALL`
  reason: `not authorized by this Task`

- action_or_channel: `ADMISSION_OR_RELEASE_ENABLEMENT`
  reason: `Human/Browser later phase`

- action_or_channel: `NEW_EXTERNAL_PAID_RESOURCE`
  reason: `requires separate authorization`

proof_non_substitution:
- unit/static proof != executed concurrent/runtime case
- synthetic provider != real provider canary
- source inspection != physical receipt truth
- local matrix != hosted Railway edge proof
- accepted L5 hosted proof != L6 owner-chain/concurrency matrix when L6 requires execution
- Executor candidate != Browser acceptance
- Replay artifact presence != Replay independence under simulated Live failure

## matrix execution rules

- Use the frozen T01-T35 definitions exactly; do not weaken expected outcomes.
- Preserve the matrix distinction between deterministic synthetic cases and release-only evidence.
- T17/T19 hosted edge identity facts may reuse accepted L5 hosted proof when the relevant paths are unchanged; do not mutate Railway merely to rerun them.
- T24 must prove Replay independence without relabeling any Live failure as accepted Replay.
- T32 must preserve `AGENT_OUTPUT != SYSTEM_STATE` / provider success cannot directly imply workflow ACCEPTED.
- T35 is runtime behavior of the retained capability/session contract; do not enter L7 UI implementation.
- If a case is not runnable because a required fixture/harness is genuinely absent, build the smallest local task-owned fixture/harness when it does not change product semantics.
- If making a case runnable requires a new semantic/security decision or external release authority, STOP with the exact named boundary instead of inventing policy.

## test / verification posture

Prefer direct affected proof over broad repetition.

Minimum when no product source changes:
- T01-T35 matrix;
- direct owner-chain/corpus pin proof;
- multi-worker/restart/unknown-send proof;
- final safe-state checks;
- formatting/encoding/diff checks for governance changes.

When product source changes:
- failing case regression;
- directly impacted unit/integration/security tests;
- relevant matrix subset;
- full T01-T35 rerun before candidate success;
- changed production-owner mypy/Ruff/format as applicable;
- `git diff --check`;
- broader suite only if blast radius or repository policy makes it necessary.

## workflow transition expectation

- initial_state: `L5_ACCEPTED_CLOSED / L6_ENTRY`
- expected_non_terminal_state_when_human_pending: `L6_BLOCKED_EXACT_HUMAN_OR_AUTHORITY_BOUNDARY`
- expected_terminal_candidate: `L6_TERMINAL_ACCEPTANCE_CANDIDATE`
- transition_authority: `Browser Command Center / Human`
- Agent may mark L6 accepted/closed: `No`

## project context impact

architecture:
- `NONE unless actual contradiction discovered`

orchestration_contract:
- `NONE; T32 explicitly verifies governance non-substitution`

security_sandbox:
- `EXECUTED_VERIFICATION_REQUIRED`

public_provenance:
- `CANONICAL_UPDATE_REQUIRED`

## accept 기준

Return `L6_TERMINAL_ACCEPTANCE_CANDIDATE` only if:

- all four frozen L6 exit criteria have valid current evidence;
- T01-T35 has no unexplained fail/skip;
- actual proof types match the matrix cases;
- production owner chain uses the exact frozen scenario/version and synthetic provider transport;
- concurrency/restart/unknown-send limits are physically demonstrated;
- cap non-bypass and Replay independence are demonstrated;
- no forbidden action ran;
- final safe state is preserved;
- Git/public provenance is reconstructable.

## hold/reject 기준

Return the narrowest honest blocker if:

- a frozen case fails after bounded in-scope correction;
- a matrix case cannot be distinguished from proof substitution;
- current source contradicts accepted policy;
- a new semantic/security choice is necessary;
- a real provider call or release action becomes necessary;
- broader DB/service authority is required;
- a new paid external resource is required.

Do not reopen L5 solely because L6 finds a new integration defect unless the defect actually invalidates an accepted L5 proof owner. If it does, name the exact invalidated criterion and stop.

## mandatory stop 조건

- `POLICY_BASELINE_CONFLICT`
- `CANONICAL_PLACEMENT_CONFLICT`
- `PREDECESSOR_BASELINE_MISMATCH`
- `DIRTY_WORKSPACE_COLLISION`
- `PROOF_TYPE_SUBSTITUTION_REQUIRED`
- `NEW_SEMANTIC_SECURITY_DECISION_REQUIRED`
- `REAL_PROVIDER_AUTHORITY_REQUIRED`
- `PUBLIC_RELEASE_AUTHORITY_REQUIRED`
- `BROADER_DB_SERVICE_AUTHORITY_REQUIRED`
- `NEW_PAID_RESOURCE_REQUIRED`
- `L5_ACCEPTED_EVIDENCE_INVALIDATED`
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`

After a true stop boundary, perform only minimal blocker proof, final safe-state check, report/export and safe Git/workspace disposition.

## Git / persistence

- Before substantive execution, verify HEAD and `origin/main` both equal `6239e4b3c8ae1b84ac4604ddf66987fb50225462`.
- Enumerate Git-visible dirt after inbound placement and distinguish expected governance delivery paths from unrelated dirt.
- Do not treat the inbound Browser files themselves as accidental dirty workspace.
- At Task completion move this Task to `.aiassistant/tasks/done/20260918_0822_aiscc-p3-3-l6-integrated-runtime-adversarial-verification-1.md`.
- Git commit/push is authorized after required verification.
- Preserve exact Browser artifact bytes.
- Do not amend/rebase/force-push.
- If a source correction is committed, report exact changed paths and resulting commit SHA.
- Passive Railway autodeploy caused by an authorized Git push may be observed only; do not configure/restart/redeploy services manually.

## 보고서 필수 항목

- result classification
- Task path / baseline / final HEAD
- exact canonical files read
- inbound artifact placement proof
- L5 Browser acceptance persistence result
- T01-T35 case table with classification and proof owner
- L6 four-exit matrix
- owner-chain/corpus pin proof
- concurrency/restart/unknown-send proof
- cap non-bypass proof
- Replay independence proof
- product source changes
- governance/provenance changes
- migration changes
- local DB/runtime/container resources and cleanup
- real provider calls
- provider secret actions
- Railway/Cloudflare actions
- admission/Live final state
- tests/static/type/format
- Git commit/push and changed path inventory
- Agent claim vs admitted evidence
- Human pending/provided
- unverified items
- rollback/revert guide
- result ZIP SHA-256

## export bundle 요구

Target:
`.aiassistant/reports/target/20260918_0822_aiscc-p3-3-l6-integrated-runtime-adversarial-verification-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `L6_SECURITY_MATRIX_RESULTS.md`
- `L6_EXIT_MATRIX.md`
- `OWNER_CHAIN_CORPUS_PIN_PROOF.md`
- `MULTI_REPLICA_UNKNOWN_SEND_PROOF.md`
- `CAPS_REPLAY_INDEPENDENCE_PROOF.md`
- `FINAL_SAFE_STATE.md`
- `WORKSPACE_STATE.md`
- changed files preserving exact project-relative paths
- `REMOVED_FILES.md` only when deletion exists

The result ZIP must preserve POSIX project-relative paths and include SHA-256/byte-size inventory for every included member.

## 사람 검증 요구

None during this Task unless a mandatory Human/authority boundary is reached.

A later real-provider canary, frontend L7 and release L8 remain separate.

## 최종 응답 형식

1. result
2. target bundle path
3. baseline/final HEAD
4. L5 acceptance persistence
5. L6 four-exit result
6. T01-T35 summary
7. owner-chain/corpus pin
8. multi-replica/unknown-send
9. caps/Replay independence
10. product/governance changed paths
11. tests/static/type/format
12. external actions
13. real provider calls
14. Public admission / Public Live / Replay final state
15. Human pending
16. unverified items
17. commit/push result
18. result ZIP SHA-256
