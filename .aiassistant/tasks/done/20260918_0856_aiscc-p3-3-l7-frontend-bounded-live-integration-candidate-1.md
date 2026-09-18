# 작업지시서: P3-3 L7 Frontend Bounded Live Integration Candidate

## meta

- task_id: `20260918_0856_aiscc-p3-3-l7-frontend-bounded-live-integration-candidate-1`
- created_at: `2026-09-18T08:56:55+09:00`
- work_type: `L7_FRONTEND_BOUNDED_LIVE_INTEGRATION_CANDIDATE`
- evidence_profile: `HIGH_RISK_FRONTEND`
- execution_mode: `MANUAL_COMMAND_CENTER / THIN_CC_THICK_EXECUTOR`
- expected_HEAD: `5c4fa727798425a6a94c7816f661dda0aedf52c4`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- public_deployment_authority: `NONE`
- public_release_authority: `NONE`
- real_provider_authority: `NONE`

## Goal

Implement and verify the L7 static frontend candidate that adds one bounded Public Live experience to the existing Human-accepted Recorded Replay surface.

Success means the source candidate can later be release-bound to one exact API origin while:

- Replay continues to work with no API;
- Live remains disabled/inert unless exact immutable release configuration enables it;
- only `stockroom-s1-normal / 1.0.0` can be started;
- H5 capability/session semantics are physically represented in frontend code and automated browser/DOM-capable proof;
- no provider, Railway, Cloudflare or release action occurs in this Task.

The Executor owns the implementation method inside the contract.

## Must preserve

- existing four Recorded Replay scenarios and corpus bytes;
- Replay remains fully functional if Live config/API is absent, disabled, malformed, unreachable or returns safe errors;
- current public Cloudflare deployment is not changed;
- Public admission remains `DISABLED`;
- Public Live remains `NOT_RELEASED`;
- exact public browser Origin remains `https://aiscc-replay.pages.dev`;
- no free-form task, repository, prompt, provider, model, endpoint, tool or secret input;
- HTML renders server/public data as text, never executable HTML;
- no raw provider output, secret or private owner data enters frontend state;
- URL/cookie/localStorage never store or convey read capability;
- release/state transition authority remains Browser/Human.

## Must not do

- deploy to Cloudflare;
- mutate Railway service/domain/variables/roles;
- create a Railway public domain;
- enable edge trust or admission;
- perform a real OpenAI/provider request;
- read/export/insert a production provider credential;
- enter L8;
- add owner/admin/cancel/free-form public routes;
- widen CSP to `*`, generic `https:`, unsafe-inline, unsafe-eval, or broad third-party origins;
- make Replay depend on Live config/API availability;
- change backend API semantics to fit frontend convenience;
- add a framework/build system solely for style or long-term elegance when the existing static stack is sufficient.

## Authority closure

This Task authorizes frontend/source/test/documentation changes required to satisfy the already-frozen L7 semantics.

The Executor may choose:
- JS module/structure;
- immutable Live config representation;
- test harness/browser/DOM simulation;
- polling strategy within existing API limits;
- UI layout and labels;
- build-script changes;
- exact static asset organization;
- commit grouping.

If the existing backend contract makes L7 impossible without a new semantic/security decision, broader backend authority, public deployment, or release action, HOLD with the exact boundary.

An implementation technique differing from Browser expectations is not a stop condition.

## Allowed mutation surface

Primary:
- `public/replay/**`
- `scripts/build_public_replay.py`
- `tests/unit/public_replay_ui.cjs`
- `tests/unit/test_public_replay_build.py`
- new narrowly scoped frontend/public-replay tests under `tests/**`
- `docs/AISCC_PUBLIC_REPLAY_DEPLOYMENT.md` when needed to describe the candidate/release binding
- current governance/provenance files and Task/report export

Conditional:
- a tiny static helper under an existing public/static frontend path if cleaner than extending `app.js`
- no backend `src/aiscc/public_live/**` mutation unless an exact frozen-contract contradiction is discovered; if contradiction exists, HOLD rather than silently redefine the backend.

Git commit/push is authorized after verification.

## Required frontend semantics

### Replay

- four existing recorded scenarios remain selectable and byte-identical;
- existing recorded truth labels remain truthful;
- Replay requests only same-origin accepted static data;
- Replay works when Live config/API is unavailable;
- missing/malformed Replay data remains an error and never falls through to Live.

### Live surface

Expose one clearly separate bounded Live section.

Allowed scenario is fixed and non-editable:

```text
scenario_id:
stockroom-s1-normal

scenario_version:
1.0.0
```

No public text/task/repository/provider/model/tool inputs.

When release config is disabled/absent/invalid:
- Start control is disabled or unavailable;
- no Live API request is sent;
- UI truthfully explains that Live is not enabled;
- Replay remains usable.

### POST

When test-only/release-configured Live is enabled, frontend POST must use:

```text
POST /v1/public-live/runs
Content-Type: application/json
Idempotency-Key: 32 lowercase hex
credentials: omit

{"scenario_id":"stockroom-s1-normal","scenario_version":"1.0.0"}
```

The API base must come from one immutable server/build-owned frontend configuration, not user input, query string, hash, localStorage or mutable DOM.

Do not invent the final Railway public API origin in this Task. The candidate may remain release-disabled with an unbound/null exact origin while tests bind a synthetic exact origin.

### H5 capability/session contract

On a confirmed 201:
- store only the minimum resumable Live session state in same-tab `sessionStorage`;
- read capability never appears in URL, hash, cookie, localStorage, rendered raw debug output or console logging;
- same-tab refresh reconstructs enough state to continue bounded GET;
- independent tab/session without that storage cannot recover;
- tab/session close naturally loses capability;
- expiry is enforced and expired capability/session state is discarded;
- idempotency key needed for same-key retry remains bounded to the current tab/session.

On 202:
- no capability is fabricated or recovered;
- if the browser never received the original 201 capability, explain that status recovery is unavailable;
- do not automatically create a replacement run with a fresh key.

On uncertain 5xx/retryable errors:
- same idempotency key may be retried according to the API contract;
- never infer rollback;
- never mint a fresh replacement run automatically.

### GET / status

Use:

```text
GET /v1/public-live/runs/{run_id}
X-Run-Read-Capability: <same-tab token>
credentials: omit
```

Render only the bounded public projection.

Provider success alone must never be labeled workflow `ACCEPTED`; show the server-returned workflow/governance state truthfully.

Polling must be bounded and stop when no longer useful (terminal state, capability expiry, explicit local stop/unmount, or equivalent). Stay within the accepted 30-read/minute limit.

### Security / CSP

The deployed Replay currently uses `connect-src 'self'`.

L7 candidate must support an eventual **single exact** release-time Live API origin without broadening to wildcard/general HTTPS.

If the candidate introduces a static config file:
- default/repository candidate is disabled;
- config is same-origin static data;
- invalid/missing config fails closed;
- changing the final API origin/enabled bit remains a later release-authorized artifact/config mutation.

No credentials/cookies.

## Evidence expected

At minimum:

1. exact source diff and final commit;
2. deterministic Replay build/check PASS;
3. existing Replay corpus identity unchanged;
4. Replay UI tests PASS;
5. Live-disabled test:
   - no API request,
   - Replay remains usable;
6. enabled synthetic-origin frontend test:
   - exact POST body/header/idempotency behavior;
   - 201 sessionStorage write;
   - same-tab reload resumes GET;
   - independent session has no recovery;
   - capability absent from URL/cookie/localStorage/log/rendered debug text;
   - 202 without prior capability cannot recover;
   - uncertain retry reuses same key;
   - no automatic replacement run;
7. GET/polling test:
   - exact capability header;
   - credentials omitted;
   - bounded polling;
   - safe terminal/expiry behavior;
8. API failure test:
   - Live visibly fails/unavailable;
   - Replay remains usable and unchanged;
9. CSP/config proof:
   - no wildcard/general network permission;
   - candidate default remains Live-disabled;
10. no backend/Railway/Cloudflare/provider mutation;
11. final Public admission `DISABLED`, Public Live `NOT_RELEASED`;
12. result ZIP manifest/hash integrity.

Human visual QA is not substituted by DOM/unit tests. Browser/Human may require a later local/browser QA gate before deployment.

## Stop boundary

HOLD only if:

- the backend contract contradicts an accepted L7/H5 semantic;
- success requires a new security/product policy;
- success requires backend authority expansion;
- an exact release API origin must be chosen before a source candidate can exist;
- Cloudflare/Railway mutation is required;
- provider credential/call is required;
- Public admission/release must be enabled;
- L8 must be entered;
- existing Replay corpus or accepted public artifact must be destructively rewritten;
- a new paid dependency/service is necessary.

Do not HOLD for:
- interpreter/shell/helper differences;
- absence of a frontend framework;
- need for a small DOM/browser fixture;
- need to refactor the static JS inside the allowed surface;
- exact test command differences.

## acceptance target

Return:

`L7_FRONTEND_INTEGRATION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

only if:
- source candidate implements all frozen frontend semantics;
- automated evidence passes;
- current deployed Replay was not mutated;
- final repository candidate remains release-disabled;
- no forbidden action ran;
- Git/public provenance is reconstructable.

Do not mark L7 accepted/closed yourself.

## export

Create:

`.aiassistant/reports/target/20260918_0856_aiscc-p3-3-l7-frontend-bounded-live-integration-candidate-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `L7_FRONTEND_CONTRACT_PROOF.md`
- `SESSION_STORAGE_CAPABILITY_PROOF.md`
- `REPLAY_INDEPENDENCE_PROOF.md`
- `LIVE_CONFIG_CSP_PROOF.md`
- `FINAL_SAFE_STATE.md`
- `WORKSPACE_STATE.md`
- changed files preserving exact project-relative paths

Also create:

`.aiassistant/reports/target/20260918_0856_aiscc-p3-3-l7-frontend-bounded-live-integration-candidate-1.zip`

Verify member integrity and report SHA-256.

## final response

1. result
2. target ZIP path + SHA-256
3. baseline/final HEAD
4. changed paths
5. Replay build/corpus result
6. Live disabled/default behavior
7. POST behavior
8. H5 sessionStorage behavior
9. GET/polling behavior
10. Replay independence
11. CSP/config result
12. tests/static checks
13. backend/Railway/Cloudflare/provider actions
14. Public admission / Public Live final state
15. Human QA pending
16. unverified items
