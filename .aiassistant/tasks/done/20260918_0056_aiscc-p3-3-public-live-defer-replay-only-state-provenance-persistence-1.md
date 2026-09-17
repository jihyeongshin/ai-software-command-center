# 작업지시서: P3-3 Public Live defer / Replay-only state and provenance persistence

## meta

- task_id: `20260918_0056_aiscc-p3-3-public-live-defer-replay-only-state-provenance-persistence-1`
- created_at: `2026-09-18T00:56:00+09:00`
- work_type: `GOVERNANCE_STATE_PERSISTENCE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `Browser Command Center`

## 현재 상태

- current canonical baseline: GitHub `main` / local expected HEAD `87ea39167c18508177db9577d66a5bdfd0a8366b`.
- predecessor cycle: `.aiassistant/records/aiscc/cycles/20260918_0056_aiscc-p3-3-public-live-bounded-rework-mandatory-stop-replay-only-defer-1.cycle.md`.
- predecessor result ZIP: `d933e5f582d7ff9605ad13cb2de7ce405d25f271e44522b52397793aa15a22d3` (`11/11` manifest integrity independently verified by Browser).
- known dirty workspace before delivery: predecessor reported `index empty / tracked diff none`; temporary source/test changes reverted.
- expected Git-visible inbound governance dirt after this delivery is exactly the following seven canonical tracked targets, subject to an already-present byte-identical file being represented equivalently by Git:
  - `{pre_task_done_rel}`
  - `{pre_cycle_rel}`
  - `{pre_judgment_rel}`
  - `{pre_handoff_rel}`
  - `{cycle_rel}`
  - `{judgment_rel}`
  - `{handoff_rel}`
- the new active Task is under ignored `tasks/active` and is not expected as Git-visible dirt until moved to `tasks/done`.
- unrelated pre-existing governance/cache residue may be preserved only if it does not collide with an authorized path; do not clean it.
- open blocker: none for this persistence Task. Public Live is intentionally deferred for the competition path.

## 이번 턴 목표

1. Persist the accepted mandatory-stop provenance for the final bounded Public Live rework.
2. Preserve the earlier 0025 partial-acceptance Cycle/Judgment/Handoff that were delivered before the rework but were not committed because the rework matrix failed.
3. Canonically mark the bounded rework Task as done; `done` means execution submission/provenance preserved, not positive feature acceptance.
4. Update current project authority so it no longer says Live implementation is `NOT_STARTED` or implies another L5 retry is current:
   - competition submission `COMPLETED`;
   - Replay `DEPLOYED / VERIFIED / HUMAN_ACCEPTED`;
   - Public Live `NOT_RELEASED / DEFERRED_FOR_COMPETITION`;
   - Public admission `DISABLED`;
   - L5 positive release gate `INCOMPLETE / TERMINALLY_DEFERRED_FOR_COMPETITION`;
   - L6/L7/L8 Live path not entered for the competition critical path;
   - next operational priority is Replay availability/freeze, not additional Live implementation.
5. Add a current decision entry recording `DEFER_PUBLIC_LIVE / KEEP_REPLAY_PUBLIC` as Browser Command Center terminal competition disposition after the final bounded retry.
6. Create one scoped governance-only Git commit and push `main` after exact remote fast-forward safety checks.

## 이번 턴 비목표

- diagnose or fix `LIVE_UNAVAILABLE`.
- modify edge identity, limiter, DB functions, migrations, runtime, tests, frontend, Replay source, or provider code.
- change Railway service variables, replicas, domains, deployments, databases, roles, or resource count.
- delete/suspend Railway resources for cost control.
- mutate Cloudflare or OpenAI.
- enable Public Live or Public admission.
- rerun hosted/runtime/browser/provider evidence.

## 허용 범위

allowed_paths:
- `.aiassistant/tasks/done/20260918_0025_aiscc-p3-3-l5-railway-edge-identity-bounded-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260918_0025_aiscc-p3-3-l5-hosted-ingress-edge-proof-partial-acceptance-mandatory-rollback-1.cycle.md`
- `.aiassistant/reports/aiscc/20260918_0025_aiscc-p3-3-l5-hosted-ingress-edge-proof-partial-acceptance-mandatory-rollback-judgment-1.md`
- `.aiassistant/reports/aiscc/20260918_0025_aiscc-browser-command-center-p3-3-l5-edge-identity-bounded-rework-entry-handoff-1.md`
- `.aiassistant/records/aiscc/cycles/20260918_0056_aiscc-p3-3-public-live-bounded-rework-mandatory-stop-replay-only-defer-1.cycle.md`
- `.aiassistant/reports/aiscc/20260918_0056_aiscc-p3-3-public-live-bounded-rework-mandatory-stop-replay-only-defer-judgment-1.md`
- `.aiassistant/reports/aiscc/20260918_0056_aiscc-browser-command-center-public-live-defer-replay-only-persistence-entry-handoff-1.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/tasks/done/20260918_0056_aiscc-p3-3-public-live-defer-replay-only-state-provenance-persistence-1.md`
- `.aiassistant/reports/target/20260918_0056_aiscc-p3-3-public-live-defer-replay-only-state-provenance-persistence-1/**` (temporary ignored export only)

allowed_actions:
- verify exact canonical/transport artifacts and hashes.
- if `.aiassistant/tasks/active/20260918_0025_aiscc-p3-3-l5-railway-edge-identity-bounded-rework-1.md` exists, compare it byte-for-byte with `.aiassistant/tasks/done/20260918_0025_aiscc-p3-3-l5-railway-edge-identity-bounded-rework-1.md` then remove only the active copy; mismatch => STOP.
- update only the three current governance projection documents listed above.
- move this Task from active to done at successful completion.
- `git add` only exact tracked governance/provenance paths authorized above.
- one commit with message `docs: defer public live for competition`.
- `git fetch`/remote-head verification and `git push origin main` only after proving local parent/remote fast-forward safety and exact staged inventory.
- produce standard target report/export ZIP.

## 절대 금지

forbidden_paths:
- `src/**`
- `tests/**`
- `migrations/**`
- frontend/public Replay implementation paths
- `.gitignore`
- build/CI/runtime configuration not listed in allowed paths

forbidden_actions:
- Railway CLI/API mutation, service restart/redeploy, domain generation/removal, scale/delete, variable read/write, DB access.
- Cloudflare mutation or redeploy.
- OpenAI API call or key/account inspection.
- browser/runtime/HTTP proof collection.
- product source/test formatting or cleanup.
- unrelated dirty file cleanup/reset.
- broad Git staging (`git add -A`, `git add .`) or unrelated commit inclusion.
- force push/rebase/history rewrite.
- resource teardown merely because Live is deferred.

## 읽을 문서

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md`
- `.aiassistant/records/command-center/NEXT_ACTION_SELECTION_RUBRIC.md`
- `.aiassistant/records/aiscc/cycles/20260918_0025_aiscc-p3-3-l5-hosted-ingress-edge-proof-partial-acceptance-mandatory-rollback-1.cycle.md`
- `.aiassistant/reports/aiscc/20260918_0025_aiscc-p3-3-l5-hosted-ingress-edge-proof-partial-acceptance-mandatory-rollback-judgment-1.md`
- `.aiassistant/reports/aiscc/20260918_0025_aiscc-browser-command-center-p3-3-l5-edge-identity-bounded-rework-entry-handoff-1.md`
- `.aiassistant/records/aiscc/cycles/20260918_0056_aiscc-p3-3-public-live-bounded-rework-mandatory-stop-replay-only-defer-1.cycle.md`
- `.aiassistant/reports/aiscc/20260918_0056_aiscc-p3-3-public-live-bounded-rework-mandatory-stop-replay-only-defer-judgment-1.md`
- `.aiassistant/reports/aiscc/20260918_0056_aiscc-browser-command-center-public-live-defer-replay-only-persistence-entry-handoff-1.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`

## agent instruction transport / authority

- repository-root instruction entrypoint는 transport bootstrap이며 policy authority가 아니다.
- Project Rules UI 또는 automatic retrieval만으로 canonical body가 Agent에 전달됐다고 가정하지 않는다.
- 위 목록은 minimum authoritative context set이다.
- unrelated rules/records/source/logs를 bulk-read하지 않는다.
- active Task File, canonical rule, Browser-delivered judgment/cycle/handoff, current repository state가 충돌하면 mutation 전에 중단하고 conflict investigation으로 보고한다.
- Human-owned evidence를 executor-completed로 주장하지 않는다.
- Browser terminal decision을 Executor가 재판정하거나 `Live retry`로 바꾸지 않는다.

## 조사할 source

No product source investigation is required or authorized.

Exact repository commands may inspect only:
- HEAD / origin-main relationship;
- status/index/scoped diff;
- exact allowed governance paths;
- commit/push result.

## 구현/문서/감사 범위

### A. canonical provenance placement

- Delivery ZIP에서 제공된 prior/current Cycle/Judgment/Handoff 및 predecessor done Task를 exact canonical path에 둔다.
- 같은 canonical file이 이미 존재하면 byte-exact 동일성을 확인한다. 다르면 `DOCUMENT_CONTRACT_MISMATCH`로 STOP한다.
- predecessor active Task가 남아 있으면 done copy와 exact 동일할 때만 active copy를 제거한다.

### B. `CURRENT_STATE_SUMMARY.md`

문서 최상단의 기존 authority section보다 위에 새 current-authority section을 추가한다. 최소 의미:

```text
Current authority (20260918_0056)
Competition submission: COMPLETED / HUMAN_PROVIDED
Public Replay: DEPLOYED / VERIFIED / HUMAN_ACCEPTED
Public Live: NOT_RELEASED / DEFERRED_FOR_COMPETITION
Public admission: DISABLED
L5: bounded implementation/proof attempted; positive hosted release gate INCOMPLETE; competition retry queue CLOSED
L6/L7/L8 Live path: NOT_ENTERED_FOR_COMPETITION
Current competition surface: Replay-only
Next operational obligation: preserve Replay availability; after deadline freeze submitted experience
```

Historical earlier sections remain byte-preserved below the new section; do not rewrite history.

### C. `NEXT_ACTIONS.md`

Add a new current sequence above 1646. It must make explicit:

1. no additional Public Live implementation/rework is selected before the competition deadline;
2. Replay availability is the current operational obligation;
3. after the submission deadline, do not mutate the submitted experience under the existing freeze rule;
4. private Railway resources are not part of the competition public surface and are unchanged by this decision;
5. any post-competition Live continuation or Railway resource cleanup is a separately authorized future selection, not an implicit queue item.

Do not delete the historical L1-L8 plan; mark its competition execution path superseded by the defer decision while preserving design history.

### D. `DECISION_REGISTER.md`

Add a new top decision entry:

```text
AISCC-P3-3-PUBLIC-LIVE-COMPETITION-DEFER-V1
Decision: DEFER_PUBLIC_LIVE / KEEP_REPLAY_PUBLIC
Status: BROWSER_COMMAND_CENTER_ACCEPTED / PERSISTENCE_PENDING -> PERSISTED after this Task
Reason: final bounded 0025 rework consumed its one narrow correction and still failed the LIVE_DISABLED acceptance gate at downstream LIVE_UNAVAILABLE; additional scope is not selected for the competition critical path.
Preserves: Replay production/submission authority, frozen Live design, accepted hosted least-privilege foundation, Public admission DISABLED, Public Live NOT_RELEASED.
Does not authorize: resource teardown, post-competition abandonment, or Live release.
```

Reference the exact 0056 Cycle/Judgment.

### E. Git persistence

Before staging:
- expected HEAD is exactly `87ea39167c18508177db9577d66a5bdfd0a8366b`; placement of delivery files changes the working tree, not HEAD. Any different HEAD requires STOP unless a separately admitted canonical commit is explicitly present in the supplied Browser artifacts.
- enumerate Git-visible dirt before editing. The seven inbound governance paths listed in `현재 상태` are expected/owned by this Task.
- confirm there is no additional product-source/test/runtime tracked diff.
- preserve unrelated pre-existing residue; do not use broad cleanup.
- if an authorized inbound canonical path already existed, verify its bytes are exact before treating it as satisfied.

At successful completion, the intended staged set is the seven inbound tracked governance paths plus:
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `{task_done_rel}`

Thus the maximum intended staged inventory is eleven exact paths. A path may be absent from the diff only when the canonical file already existed byte-exact at HEAD, but no unrelated path may appear. Use exact-path staging only. Commit once. Fetch/verify remote. Push only fast-forward. Record resulting commit SHA and origin/main equality.

## workflow transition expectation

- initial_state: `DEFER_PUBLIC_LIVE / KEEP_REPLAY_PUBLIC / PERSISTENCE_PENDING`
- expected_non_terminal_state_when_human_pending: `NOT_APPLICABLE`
- expected_terminal_candidate: `P3_3_REPLAY_ONLY_COMPETITION_BASELINE_PERSISTED`
- transition_authority: `Browser Command Center`; Executor only persists the admitted transition.
- Agent가 직접 terminal state를 결정할 수 있는가: `No`

## evidence contract

executor_required:
- channel: `STATIC_REPOSITORY / GOVERNANCE`
  scope: exact canonical placement and three current-authority document updates
  allowed_command_or_environment: local repository only
  pass_condition: no product/runtime diff; exact Browser decision semantics preserved; `git diff --check` PASS.
- channel: `GIT_PERSISTENCE`
  scope: one exact governance commit + fast-forward push
  allowed_command_or_environment: Git/GitHub remote only
  pass_condition: staged inventory exact; commit succeeds; origin/main equals resulting commit.

reuse_allowed:
- channel: `BROWSER_JUDGMENT`
  predecessor: `20260918_0056` Cycle/Judgment
  provenance_condition: submitted Executor ZIP SHA `d933e5f582d7ff9605ad13cb2de7ce405d25f271e44522b52397793aa15a22d3`
  applicability_condition: no product/runtime mutation occurs in this persistence Task.

human_owned:
- channel: `PUBLIC_RELEASE / POST_COMPETITION_RESOURCE_DECISION`
  scope: any future Live release or separate resource-cleanup decision
  expected_result_format: `not part of this Task; do not claim completed`

not_required:
- channel: `HTTP_RUNTIME / RAILWAY / OPENAI / CLOUDFLARE / BROWSER_QA`
  reason: Browser has already terminally selected the Replay-only competition fallback; this Task only persists governance state.

forbidden:
- action_or_channel: `PRODUCT_SOURCE / RUNTIME / DEPLOYMENT / RESOURCE_MUTATION`
  reason: out of scope and would reopen the bounded Live path.

proof_non_substitution:
- `Executor persistence report != Browser terminal judgment`.
- `Git commit != runtime proof`.
- `Replay availability statement != new browser QA`; reuse only prior accepted public Replay authority.

## conformance reporting

- applicability: `REQUIRED`
- applicable policy_or_invariant: `AgentOutput != SystemState; tasks/done may preserve blocked work; terminal Browser judgment owns next action; public provenance tracked, target export ignored`
- required_actual_owner: `Browser Command Center for defer decision; Executor for exact persistence only`
- planned_vs_actual_scope: governance-only
- rollback_or_failure_semantics: on any mismatch/non-fast-forward/dirty collision, do not broaden cleanup or runtime work; export blocker and stop.

## project context impact

architecture:
- `NONE` — frozen Live design is preserved, not rewritten.

orchestration_contract:
- `UPDATE_REQUIRED` — current state/queue must reflect terminal defer rather than stale NOT_STARTED/current-L5 language.

security_sandbox:
- `NONE` — final fail-closed hosted state is preserved; no runtime access.

public_provenance:
- `CANONICAL_UPDATE_REQUIRED`.

## accept 기준

All:
- all provided Browser governance artifacts placed/verified exact;
- predecessor 0025 Task preserved under tasks/done and no conflicting active duplicate remains;
- new 0056 authority is top/current in CURRENT_STATE_SUMMARY, NEXT_ACTIONS, DECISION_REGISTER;
- historical content preserved rather than rewritten;
- no `src/**`, `tests/**`, migrations, runtime/config/deployment changes;
- no Railway/Cloudflare/OpenAI action;
- exact staged inventory only;
- `git diff --check` PASS;
- one governance commit;
- push is fast-forward and origin/main equals resulting commit;
- this Task ends in tasks/done;
- standard target report/export created.

## hold/reject 기준

- Browser judgment wording is weakened into `maybe retry Live` or incorrectly claims L5 accepted.
- historical design/accepted hosted foundation is deleted instead of preserved.
- product/runtime path changes.
- any resource teardown/redeploy.
- staged scope contains unrelated paths.
- remote changed in a way that requires rebase/force-push/manual conflict resolution outside exact scope.

## mandatory stop 조건

- `DOCUMENT_CONTRACT_MISMATCH`
- expected baseline/remote lineage mismatch not explainable solely by exact current delivery placement
- unrelated dirty workspace collision with authorized paths
- forbidden product/runtime mutation required
- Git staged inventory mismatch
- non-fast-forward push condition
- secret/private material detected in any tracked governance artifact
- policy baseline conflict

Named blocker 이후에는 최소 source evidence, workspace inventory, report/export와 안전한 종료만 수행한다. Runtime/network/deployment investigation을 추가하지 않는다.

## 보고서 필수 항목

- task path / work type
- exact read canonical paths
- before/after HEAD and origin/main
- placed/verified Browser artifact inventory + SHA where available
- predecessor active->done disposition
- exact changes to CURRENT_STATE_SUMMARY / NEXT_ACTIONS / DECISION_REGISTER
- product source changes: must be none
- governance/provenance changes
- repository configuration changes: must be none
- staged path inventory
- commit SHA / push result
- forbidden-not-run: Railway, Cloudflare, OpenAI, runtime, product source
- human pending: any future Live release/resource cleanup only
- mandatory stop/scope expansion if any
- unverified items

## export bundle 요구

Target:
`.aiassistant/reports/target/20260918_0056_aiscc-p3-3-public-live-defer-replay-only-state-provenance-persistence-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- changed tracked governance files preserving project-relative paths
- `REMOVED_FILES.md` only if the predecessor active Task removal must be represented by the export policy

At completion create:
`.aiassistant/reports/target/20260918_0056_aiscc-p3-3-public-live-defer-replay-only-state-provenance-persistence-1.zip`

## 사람 검증 요구

- none during Executor work.
- no Human Live release/resource-cleanup decision is requested by this Task.

## 최종 응답 형식

1. result: completed / blocked / rejected-candidate
2. canonical authority updates
3. exact staged paths
4. commit SHA + push result
5. product/runtime/infra actions: must be none
6. target ZIP path + SHA-256
7. unverified items
