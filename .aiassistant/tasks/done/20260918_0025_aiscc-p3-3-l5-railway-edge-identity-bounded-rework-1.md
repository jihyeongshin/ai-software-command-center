# 작업지시서: P3-3 L5 Railway Edge Identity Bounded Rework

## meta

- task_id: `20260918_0025_aiscc-p3-3-l5-railway-edge-identity-bounded-rework-1`
- created_at: `2026-09-18T00:25:00+09:00`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `Browser Command Center / Public Live hosted edge identity`
- timebox: `ONE_BOUNDED_REWORK_CYCLE`

## 현재 상태

- canonical repository/main expected at entry: `87ea39167c18508177db9577d66a5bdfd0a8366b`
- predecessor Task: `.aiassistant/tasks/done/20260917_2236_aiscc-p3-3-public-live-l5-hosted-public-ingress-edge-proof-1.md`
- predecessor Browser Cycle: `.aiassistant/records/aiscc/cycles/20260918_0025_aiscc-p3-3-l5-hosted-ingress-edge-proof-partial-acceptance-mandatory-rollback-1.cycle.md`
- predecessor result ZIP SHA-256: `ae087d11277c52a94fc2dc929536659c8e5afc1f4a102544f2d2aac65a37dfe8`
- accepted retained hosted foundation:
  - DB migration `20260917_0021`
  - dedicated ingress capability/login
  - ingress service `fd09a9f2-1bf8-4a48-8af8-d1536866fa1d`
- final retained safe state:
  - edge trust absent
  - public ingress domain absent
  - Public admission `DISABLED`
  - Public Live `NOT_RELEASED`
  - provider/OpenAI effects `0`
- open blocker: `RAILWAY_EDGE_OVERWRITE_PROOF_FAILED`

## 이번 턴 목표

1. Opaque `IDENTITY_UNAVAILABLE`의 hosted control-request 원인을 raw identity/secret 노출 없이 safe diagnostic category로 확정한다.
2. 원인이 현재 Railway public-request contract와의 좁은 mismatch이고 authority를 약화시키지 않는 경우에만 최소 source correction을 한다.
3. 동일 ingress service에서 hosted overwrite/spoof matrix를 재실행한다.
4. PASS여도 edge trust는 다시 제거한 상태로 종료하며 Public admission/Public Live를 release하지 않는다.
5. broad redesign이 필요해지면 즉시 STOP하고 Replay-only fallback을 Browser에 반환한다.

## 이번 턴 비목표

- migration 0021 재실행 또는 새 migration
- ingress login/role 재생성 또는 privilege 확대
- 새 Railway service/database/proxy/CDN 생성
- owner API / initializer / worker 변경
- worker provider secret cutover
- OpenAI 호출 또는 paid canary
- Cloudflare 변경
- Public admission enablement
- Public Live release
- production-grade proxy trust framework, HA/DR, generalized observability 구축

## 허용 범위

allowed_paths:
- `src/aiscc/public_live/edge_identity.py`
- `src/aiscc/public_live/ingress.py` — safe diagnostic plumbing이 반드시 필요한 경우에만
- `tests/unit/public_live/test_edge_identity.py`
- `tests/unit/public_live/test_hosted_binding.py` — 직접 영향이 있을 때만
- `tests/unit/public_live/test_http.py` — 직접 영향이 있을 때만
- `.aiassistant/tasks/active/20260918_0025_aiscc-p3-3-l5-railway-edge-identity-bounded-rework-1.md` -> completion 시 matching `tasks/done`
- delivery package가 배치한 predecessor Cycle/Judgment/Handoff exact paths

allowed_hosted_actions:
- existing `aiscc-public-live-ingress` service의 배포/변수/temporary public domain QA
- ingress에만 QA-only edge trust switch temporary enable/disable
- safe non-secret deployment/runtime logs 조회
- exact public HTTP QA matrix
- final domain removal on failure or retention on PASS as specified below

allowed_git_actions:
- local diff/test only until hosted matrix PASS
- hosted matrix PASS인 경우에만 exact changed source/test + this Task moved to done + supplied predecessor Cycle/Judgment/Handoff를 one bounded commit으로 stage/commit/push 가능
- matrix FAIL/BLOCKED이면 source/test Git commit/push 금지; temporary diagnostic change는 revert하여 canonical source HEAD representation을 보존

## 절대 금지

forbidden_actions:
- migration 0021 rerun as substantive work
- DB role/login capability 변경 또는 privilege 확대
- 새 Railway service/database 생성
- owner/initializer/worker mutation
- OpenAI/provider call
- Cloudflare mutation
- Public admission/release enable
- raw client IP, raw `X-Real-IP`, raw `X-Railway-Edge`, forwarding-header value, DSN, password, HMAC key 출력/파일 저장
- caller-controlled `X-Forwarded-For`, `Forwarded`, `CF-Connecting-IP`를 trusted identity source로 사용
- CIDR/hop/proxy chain 추측
- unrelated source/test broadening
- full test suite
- broad architecture redesign

## 읽을 문서

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
- `.aiassistant/tasks/done/20260917_2236_aiscc-p3-3-public-live-l5-hosted-public-ingress-edge-proof-1.md`
- `.aiassistant/records/aiscc/cycles/20260918_0025_aiscc-p3-3-l5-hosted-ingress-edge-proof-partial-acceptance-mandatory-rollback-1.cycle.md`
- `src/aiscc/public_live/edge_identity.py`
- `src/aiscc/public_live/ingress.py`
- `tests/unit/public_live/test_edge_identity.py`

External primary references permitted for this Task:
- `https://docs.railway.com/networking/public-networking/specs-and-limits`
- `https://docs.railway.com/networking/edge-networking`

Do not treat documentation alone as overwrite proof; hosted behavior remains required.

## Step 0 — entry preflight

1. Verify HEAD and `origin/main` equal `87ea39167c18508177db9577d66a5bdfd0a8366b` unless the only intervening commit is an exact Browser-delivery provenance placement already authorized by this package.
2. Verify no mixed product-source dirt. Preserve known unrelated untracked governance/cache residue without cleanup broadening.
3. Observe only that retained ingress service exists and is fail-closed. Do not recreate it.
4. Confirm edge trust absent and public domain absent before mutation.
5. If retained DB/login/service foundation materially differs from predecessor evidence, STOP `HOSTED_EDGE_REWORK_PRECONDITION_MISMATCH`.

## Step 1 — safe diagnostic classification

The public response MUST continue to expose only the existing safe external code `IDENTITY_UNAVAILABLE`.

Add the smallest internal diagnostic mechanism needed to classify why `RailwayEdgeIdentityAuthority` rejects a request. It MUST NOT capture or emit raw identity/header/secret values.

Allowed safe categories are structural only, for example:
- trust disabled
- required header missing/duplicate
- host mismatch
- proto mismatch
- edge format mismatch
- real-IP syntax/non-global mismatch
- conflicting non-authority forwarding header present
- configuration mismatch

Do not include the actual host, IP, edge POP, header value, DSN, token, key, or secret in diagnostics.

Prefer an internal enum/reason and QA-only structured log or equivalent narrow mechanism. Do not add a public debug endpoint.

## Step 2 — targeted local proof

Before hosted deployment:

- changed edge-identity unit tests PASS;
- directly affected hosted-binding/http tests only when changed behavior requires them;
- Ruff on changed Python paths;
- formatter check on changed Python paths;
- narrow mypy if the repository's current targeted convention supports it;
- `git diff --check`.

Do not run the full repository suite.

Mandatory local invariants:

- `overwrite_proof_accepted=False` still fail-closes.
- exactly one valid Railway-owned identity source is required.
- duplicate/comma/invalid `X-Real-IP` remains denied locally.
- untrusted forwarding headers are never consumed as identity.
- raw secret/identity values are not logged.

## Step 3 — diagnostic hosted control request

Use ONLY existing `aiscc-public-live-ingress`.

1. deploy the diagnostic candidate;
2. create a temporary Railway public domain for the ingress if absent;
3. set exact `PUBLIC_LIVE_API_ORIGIN` to that domain;
4. temporarily set `AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST=HOSTED_OVERWRITE_PROOF_ACCEPTED_V1`;
5. keep `admission=None`; worker key remains absent;
6. send exactly one known-valid control POST from the same bounded client discipline as predecessor 2236;
7. record only status, safe external code, and safe diagnostic category.

If the control reaches `503 LIVE_DISABLED`, proceed directly to Step 5 without weakening the identity contract.

## Step 4 — one conditional minimal correction

A functional trust change is authorized only if Step 3 gives a narrow, explainable current Railway request-contract mismatch.

Allowed minimal correction classes:

A. **Non-authority forwarding-header presence**

If the only blocker is presence of `X-Forwarded-For`, `Forwarded`, or `CF-Connecting-IP`, these headers may be changed from "mere presence denies" to "completely ignored / never consumed". They MUST NOT contribute to identity, precedence, hop selection, or source bucketing. Add tests proving the derived source is unchanged by hostile values in these ignored headers.

B. **Documented Railway edge syntax mismatch**

If and only if the observed safe shape and current official Railway documentation disagree with the parser, minimally align the edge-format parser to the documented POP identifier contract. Do not widen it beyond the documented syntax.

C. **Configuration-only mismatch**

An exact public-origin/config typo may be corrected without changing trust semantics.

All other causes — missing/duplicate authoritative headers, inability to establish a single overwritten `X-Real-IP`, non-global/ambiguous identity, undocumented proxy chain, or any need to infer trusted hops/CIDRs — MUST STOP as:

`HOSTED_EDGE_IDENTITY_REWORK_NEEDS_BROAD_TRUST_CHANGE`

Do not invent a second trust model in this Task.

After an allowed correction, rerun Step 2 targeted checks before hosted QA.

## Step 5 — hosted overwrite/spoof matrix

With QA edge trust temporarily enabled, run:

1. `GET /health` -> `200`.
2. valid control POST -> `503 LIVE_DISABLED`.
3. forged single `X-Real-IP` containing an invalid non-IP sentinel -> MUST still reach `LIVE_DISABLED` only if Railway overwrites/collapses it to the platform-owned value; otherwise FAIL.
4. duplicate hostile `X-Real-IP` -> Railway overwrite/collapse to a single valid value OR application fail-closed; never select a hop/list element.
5. comma-list hostile `X-Real-IP` -> same safe rule.
6. forged malformed `X-Railway-Edge` -> must not create authority; overwritten valid provenance or fail-closed.
7. hostile `X-Forwarded-For`, `Forwarded`, `CF-Connecting-IP` -> may be ignored, but MUST NOT change derived source authority. Static/unit proof plus hosted zero-effect response is sufficient; do not require these non-authority headers to become identity blockers.
8. owner/security/docs/UI/admin/debug/arbitrary route probes -> `404 NOT_FOUND`.
9. unsupported method on collection -> `405 METHOD_NOT_ALLOWED` after identity succeeds.
10. exact CORS preflight from `https://aiscc-replay.pages.dev` -> `204`, exact allow-origin, no wildcard.
11. private/direct attempt -> no public edge identity authority.

Acceptance-critical hosted rule:

- normal control reaches `LIVE_DISABLED`;
- forged invalid single `X-Real-IP` also reaches `LIVE_DISABLED`, proving caller value did not survive as identity;
- no hostile header creates authority;
- admission/start/provider effects remain zero.

Do not record raw identity values.

## Step 6 — final safe state

On PASS:

1. remove `AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST` again;
2. redeploy fail-closed;
3. keep the ingress public domain PRESENT for the next Browser-gated phase;
4. prove `/health=200`;
5. prove valid POST is again `503 IDENTITY_UNAVAILABLE`;
6. Public admission remains `DISABLED`;
7. Public Live remains `NOT_RELEASED`;
8. provider/OpenAI effects remain `0`.

On FAIL/BLOCKED:

1. remove edge trust;
2. redeploy fail-closed;
3. remove public domain;
4. revert temporary source/test diagnostic changes to the entry HEAD unless the failure occurs after an already-authorized final PASS commit;
5. verify zero admission/start/provider effect;
6. STOP.

## Step 7 — conditional Git persistence

Only when the hosted matrix PASSes:

- move this Task from `tasks/active` to matching `tasks/done`;
- stage only:
  - final allowed source/test changes actually required for the PASS;
  - `.aiassistant/tasks/done/20260918_0025_aiscc-p3-3-l5-railway-edge-identity-bounded-rework-1.md`;
  - `.aiassistant/records/aiscc/cycles/20260918_0025_aiscc-p3-3-l5-hosted-ingress-edge-proof-partial-acceptance-mandatory-rollback-1.cycle.md`;
  - `.aiassistant/reports/aiscc/20260918_0025_aiscc-p3-3-l5-hosted-ingress-edge-proof-partial-acceptance-mandatory-rollback-judgment-1.md`;
  - `.aiassistant/reports/aiscc/20260918_0025_aiscc-browser-command-center-p3-3-l5-edge-identity-bounded-rework-entry-handoff-1.md`;
- one bounded commit;
- push `main` only if remote fast-forward safety is proven.

Do not commit temporary diagnostic-only artifacts, logs, raw evidence, or target bundle.

If matrix FAIL/BLOCKED, do not commit/push source/test changes under this Task. The completed Task/report may remain local for Browser review according to the standard export lifecycle.

## workflow transition expectation

- initial_state: `L5_HOSTED_PHASE_C_PARTIAL_ACCEPTED_EDGE_PROOF_BLOCKED`
- expected_terminal_candidate: `L5_HOSTED_PHASE_C_EDGE_PROOF_ACCEPTED_CANDIDATE`
- failure_state: `PUBLIC_LIVE_DEFER_CANDIDATE` when broad trust redesign would be required
- transition_authority: `SYSTEM / Browser Command Center`
- Agent가 직접 terminal state를 결정할 수 있는가: `No`

## evidence contract

executor_required:
- channel: `STATIC_SOURCE / UNIT_TEST`
  scope: safe diagnostic + any minimal final correction
  pass_condition: targeted checks pass and no raw identity/secret exposure
- channel: `HTTP_RUNTIME / HOSTED_RAILWAY`
  scope: control + overwrite/spoof matrix
  pass_condition: critical control and forged-single-X-Real-IP cases reach `LIVE_DISABLED`, zero release/provider effects
- channel: `SECURITY_SANDBOX`
  scope: final rollback/safe-state and secret non-exposure
  pass_condition: edge trust absent at end, provider effects zero, no residual temporary authority

reuse_allowed:
- channel: `DATABASE_RUNTIME`
  predecessor: `20260917_2236`
  provenance_condition: submitted ZIP SHA `ae087d11277c52a94fc2dc929536659c8e5afc1f4a102544f2d2aac65a37dfe8`
  applicability_condition: migration 0021/login/ingress service remain unchanged

human_owned:
- channel: `PUBLIC_RELEASE`
  scope: final Public Live release
  expected_result_format: `HUMAN_PENDING`; forbidden in this Task

not_required:
- channel: `OPENAI_PROVIDER`
  reason: provider proof/canary is later and no provider call is needed here
- channel: `CLOUDFLARE`
  reason: Replay must remain untouched

forbidden:
- action_or_channel: `BROAD_TRUST_REDESIGN / NEW_INFRA / OPENAI_CALL / PUBLIC_RELEASE`
  reason: competition timebox and current task scope

proof_non_substitution:
- Railway documentation != hosted overwrite proof
- unit source test != hosted edge behavior
- safe diagnostic category != authority acceptance
- Executor result != Browser acceptance

## accept 기준

All of the following:

- hosted control reaches `503 LIVE_DISABLED` under temporary edge trust;
- deliberately invalid single forged `X-Real-IP` cannot survive as caller identity and request still reaches `LIVE_DISABLED`;
- no hostile header creates trusted authority;
- route/method/CORS surface passes after identity succeeds;
- zero admission/start/provider effect;
- final edge trust absent;
- final public admission `DISABLED` and Public Live `NOT_RELEASED`;
- no secret/raw identity evidence leak;
- if source changed, exact targeted tests/static checks pass;
- no unauthorized resource expansion.

## hold/reject 기준

- any broad proxy/CIDR/hop trust inference required;
- control remains `IDENTITY_UNAVAILABLE` after the one authorized narrow correction;
- forged single `X-Real-IP` survives to application authority or can alter source identity;
- source change broadens identity authority beyond Railway-overwritten `X-Real-IP` + Railway edge provenance;
- side effect becomes nonzero;
- owner/worker/initializer or provider boundary changes;
- secret/raw identity exposure.

## mandatory stop 조건

- `HOSTED_EDGE_REWORK_PRECONDITION_MISMATCH`
- `HOSTED_EDGE_IDENTITY_REWORK_NEEDS_BROAD_TRUST_CHANGE`
- hosted control remains blocked after one narrow correction
- forged single `X-Real-IP` overwrite proof fails
- side-effect leak
- secret exposure risk
- unrelated dirty workspace collision
- policy conflict
- evidence scope expansion beyond this Task

After a named blocker: collect only minimal blocker evidence, restore fail-closed state, export report, and STOP.

## competition fallback rule

This is the final authorized bounded edge-identity rework cycle before Browser reevaluates whether Public Live is worth continuing for the competition.

If safe proof still requires broader architecture work, recommend:

`DEFER_PUBLIC_LIVE / KEEP_REPLAY_PUBLIC`

Do not propose production-grade proxy redesign from this Task.

## 보고서 필수 항목

- exact diagnostic category without raw values
- changed source/test inventory
- targeted local test/static results
- Railway service/deployment IDs used
- public domain lifecycle
- QA edge-trust lifecycle
- matrix result per case
- zero side-effect counts
- secret non-exposure
- final safe state
- conditional Git commit/push result or explicit not-run
- preserved predecessor accepted foundation
- fallback recommendation if blocked

## export bundle 요구

Target:
`.aiassistant/reports/target/20260918_0025_aiscc-p3-3-l5-railway-edge-identity-bounded-rework-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- safe hosted proof artifacts
- changed source/test files preserving project-relative paths when applicable
- no raw secret/identity artifacts

At completion create:
`.aiassistant/reports/target/20260918_0025_aiscc-p3-3-l5-railway-edge-identity-bounded-rework-1.zip`

## 사람 검증 요구

- none during Executor work.
- Browser Command Center will judge the returned result bundle.
- final Public Live release remains Human-owned and out of scope.

## 최종 응답 형식

1. result: completed / blocked / rejected-candidate
2. diagnostic category
3. hosted matrix outcome
4. final safe state
5. Git persistence result
6. target ZIP path + SHA-256
7. unverified items
