# 작업지시서: P3-3 L5 terminal closure / accepted-evidence reuse / missing proof completion

## meta

- task_id: `20260918_0317_aiscc-p3-3-l5-terminal-closure-evidence-reuse-and-missing-proof-completion-1`
- created_at: `2026-09-18T03:17:00+09:00`
- work_type: `L5_TERMINAL_CLOSURE_AND_MISSING_PROOF_COMPLETION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER / THIN_CC_THICK_EXECUTOR`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `Browser Command Center + Human`
- fresh_ide_executor_chat: `NOT_REQUIRED`

## 현재 상태

- current canonical code baseline: `4c3cb6dc33e47be2a3260d15134ba6b036c7f0fc`
- accepted predecessor: `20260918_0201_aiscc-p3-3-l5-hosted-public-live-success-oriented-recovery-1`
- predecessor result ZIP SHA-256: `26f8ae316d7f553001a0506d0341c60231a92f259b80b8f189960b8dc2c3fae3`
- predecessor judgment: `ACCEPTED`
- accepted sub-gate: `L5 hosted ingress / Railway edge identity / disabled-control matrix`
- hosted Live DB migration head: `20260918_0023`
- Public admission: `DISABLED`
- Public Live: `NOT_RELEASED`
- Replay: unchanged and accepted
- provider/OpenAI physical calls so far: `0`
- governance projection issue: `CURRENT_STATE_SUMMARY / NEXT_ACTIONS / DECISION_REGISTER still carry 0056 defer as current projection`

## 이번 턴 목표

1. Canonically persist the supplied 0317 Cycle/Judgment/Handoff and move the 0201 Task to `tasks/done`.
2. Reconcile current governance projection so it truthfully records:
   - 0056 defer as historical accepted decision at that time;
   - later Human reopen;
   - 0201 ACCEPTED hosted ingress/edge sub-gate;
   - L5 overall still `IN_PROGRESS` until this Task proves closure.
3. Map every L5 exit criterion to current accepted evidence.
4. Reuse existing accepted proof where its provenance and applicability remain valid.
5. For genuinely missing **non-release, non-paid-provider** L5 proof, implement/verify the shortest competition-grade solution within the existing Public Live deployment/source boundary.
6. If all L5 exit criteria become evidentially satisfied, return `L5_TERMINAL_ACCEPTANCE_CANDIDATE`.
7. If closure requires a separate Human/provider/release authority, stop at that exact boundary and report the smallest remaining gap.

## 이번 턴 비목표

- Public Live release.
- Public admission enablement.
- real OpenAI/provider request.
- L6 integrated-runtime execution.
- L7 frontend Live integration.
- L8 Human release.
- production-grade HA/DR/autoscaling/observability/RBAC/SLO work.
- architectural cleanup solely for elegance or long-term maintainability.

## Must preserve

- Replay remains available and unchanged.
- Public admission remains `DISABLED`.
- Public Live remains `NOT_RELEASED`.
- no physical provider/OpenAI call.
- existing accepted ingress least-privilege boundary is not broadened.
- no raw secret, DSN, password, HMAC, client IP, private key, or provider credential enters public provenance.
- accepted 0201 hosted ingress evidence is reused unless directly invalidated by a current change.
- release/state-transition authority stays with Browser/Human.

## Must not do

- enable admission/control for a real run.
- add a worker provider secret.
- perform a paid or real provider request.
- create a new external paid service/resource.
- change frozen scenario/model/budget/retention/client-identity semantics.
- deliberately mutate unrelated owner API behavior.
- destroy accepted hosted state/evidence to simplify testing.
- broaden ingress or worker DB roles beyond already frozen least-privilege design.
- enter L6/L7/L8.
- redo accepted hosted ingress matrix merely for reassurance when no affected path changed.

## Authority closure

This Task authorizes L5 closure work only.

The Executor may independently decide whether a remaining L5 criterion:
- is already satisfied by accepted current evidence;
- needs a new local/static proof;
- needs a bounded hosted proof;
- needs a narrow implementation correction.

Within L5, the Executor may make source/test/deployment changes necessary to satisfy already-frozen semantics.

If satisfying a criterion requires choosing a new semantic/security policy, increasing authority, inserting provider credentials, making a physical provider call, enabling admission, entering L6/L7/L8, or adding material cost, STOP and return the exact boundary.

## Allowed mutation surface

Governance/provenance:
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- supplied 0317 Cycle/Judgment/Handoff canonical paths
- 0201 Task move active -> done
- current Task/report/export files

Technical, only when required for an unresolved L5 criterion:
- existing Public Live deployment/packaging/sandbox/runtime source
- `src/aiscc/public_live/**`
- directly related provider-boundary/sandbox support already part of frozen Public Live L5 design
- forward migrations only when required by existing frozen semantics
- directly affected unit/integration/security tests
- existing Railway Public Live services and task-owned temporary proof helpers

Git:
- commit/push is authorized for in-scope changes after required verification.
- one or multiple logically scoped commits are allowed.
- passive Railway autodeploy from an authorized push is not itself a Task violation; observe unrelated services rather than manually reconfigure them.

## Executor freedom

Inside the contract, choose the implementation and proof method.

You may:
- inspect canonical history/source to find already accepted L5 proof;
- choose approved interpreter/runtime already available locally;
- use PowerShell/shell/Python/approved container helpers;
- choose fixtures and test order;
- choose local vs hosted proof when the proof type remains valid;
- choose Railway CLI/API mechanics;
- create bounded temporary private diagnostic/verifier resources and remove them;
- choose commit grouping;
- stop early when all L5 exit criteria are actually proved.

Do **not** stop merely because a command, tool, interpreter, fixture, or deployment procedure differs from an earlier CC expectation.

## L5 exit criteria to reconcile

Use canonical `AISCC_PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json` and current accepted records as authority. At minimum reconcile:

1. Railway trusted peer/header overwrite contract demonstrated with spoof cases.
2. Supervisor termination / no-send fencing / remote-unknown quarantine demonstrated.
3. No public owner DB route or secret exposure.
4. Tool/network/filesystem isolation and Replay independence proven.
5. Any actual paid resource/deployment action remains separately authorized.

Criterion 1 is already accepted by 0201 and MUST be reused unless directly invalidated.

For criteria 2-5, first locate accepted evidence before creating new work.

## evidence contract

executor_required:
- channel: `GOVERNANCE_RECONCILIATION`
  scope: `persist 0317 provenance; reconcile stale 0056 current projection without deleting its history`
  pass_condition: `current authority truthfully reflects Human reopen + 0201 acceptance + L5 current status`

- channel: `L5_EXIT_MATRIX`
  scope: `criterion-by-criterion mapping to REUSED_ACCEPTED / EXECUTED_PASS / BLOCKED_REQUIRED_EVIDENCE / HUMAN_REQUIRED`
  pass_condition: `every canonical L5 criterion has explicit provenance and applicability`

- channel: `MISSING_L5_PROOF`
  scope: `only genuinely missing criteria that remain inside current Task authority`
  pass_condition: `required proof succeeds without crossing Stop boundary, or exact named boundary is reported`

- channel: `FINAL_SAFE_STATE`
  scope: `admission disabled, Live not released, provider calls 0, Replay unchanged, temporary authority cleaned`
  pass_condition: `all preserved boundaries hold`

reuse_allowed:
- 0201 hosted ingress/edge evidence and commit `4c3cb6dc...`
- earlier accepted L5 local/security/sandbox evidence when current affected paths and deployment semantics remain applicable
- earlier accepted L1-L4 evidence when L5 criterion explicitly depends on it and provenance is exact

human_owned:
- provider secret insertion
- paid provider call authorization
- Public Live enable/release
- any new material external cost commitment
- any new frozen semantic/security choice

forbidden:
- proof substitution
- real provider call
- admission enablement
- L6/L7/L8 transition
- unrelated production hardening

proof_non_substitution:
- local/unit proof != hosted network proof when hosted behavior is the criterion
- source inspection != runtime sandbox proof
- Executor claim != Browser acceptance
- disabled ingress proof != released Live
- provider double != real provider canary

## Stop boundary

HOLD/STOP only when:

- a canonical L5 criterion cannot be satisfied without a new semantic/security decision;
- broader role/service authority is required;
- a real provider credential or physical provider request is required;
- Public admission/release must be enabled;
- L6/L7/L8 must be entered;
- a new paid external resource/service is necessary;
- accepted-state destruction/reset is necessary;
- evidence remains ambiguous enough that success cannot be distinguished from security regression.

An unexpected but equivalent implementation method is not a stop condition.

## accept 기준

Return `L5_TERMINAL_ACCEPTANCE_CANDIDATE` only if:
- every canonical L5 exit criterion has valid current evidence;
- proof types match their criteria;
- no forbidden action ran;
- final safe state is preserved;
- Git/public provenance is reconstructable.

If not all criteria can be closed:
- return the narrowest honest result, e.g. `L5_REMAINING_HUMAN_PROVIDER_BOUNDARY`, `L5_REMAINING_HOSTED_PROOF`, or another precise named blocker;
- do not mark L5 accepted yourself.

## mandatory stop semantics

A stop caused by a true semantic/security/authority/Human boundary is a valid Executor result, not implementation failure.

After such a boundary:
- preserve already admitted evidence;
- clean temporary exposure/authority;
- export the exact remaining gap;
- do not expand into a different phase.

## 보고서 필수 항목

- entry/final commits
- canonical governance files reconciled
- L5 exit matrix with exact evidence provenance
- reused vs newly executed proof distinction
- source/deployment changes, if any
- local/hosted proof actually executed
- Human/provider/release boundary, if encountered
- final Railway/public-domain/edge-trust/admission/provider state
- passive autodeploy observations, if any
- unverified items
- exact result ZIP SHA-256 / manifest integrity

## export bundle 요구

Target:
`.aiassistant/reports/target/20260918_0317_aiscc-p3-3-l5-terminal-closure-evidence-reuse-and-missing-proof-completion-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `L5_EXIT_MATRIX.md`
- `CURRENT_AUTHORITY_RECONCILIATION.md`
- changed files preserving project-relative paths

Also create:
`.aiassistant/reports/target/20260918_0317_aiscc-p3-3-l5-terminal-closure-evidence-reuse-and-missing-proof-completion-1.zip`

Verify ZIP integrity and report SHA-256.

## 최종 응답 형식

1. result
2. target ZIP path + SHA-256
3. final commit(s)
4. L5 exit matrix summary
5. changed files
6. reused accepted proof
7. new proof executed
8. Human/provider/release boundary
9. final safe state
10. unverified items
