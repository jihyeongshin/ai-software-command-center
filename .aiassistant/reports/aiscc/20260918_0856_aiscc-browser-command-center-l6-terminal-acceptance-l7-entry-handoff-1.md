# AISCC Browser Command Center Handoff — L6 accepted / L7 entry

## current canonical state

- GitHub main: `5c4fa727798425a6a94c7816f661dda0aedf52c4`
- L3: `ACCEPTED / CLOSED`
- L4: `ACCEPTED / CLOSED`
- L5: `ACCEPTED / CLOSED`
- L6: `ACCEPTED / CLOSED`
- L7: `ENTRY_AUTHORIZED`
- Public Replay: deployed, Human-accepted, unchanged
- Public admission: `DISABLED`
- Public Live: `NOT_RELEASED`
- real provider calls: `0`

## L6 acceptance basis

- T01-T35: 35/35
- production owner chain + exact `stockroom-s1-normal / 1.0.0`
- multi-worker/restart/unknown-send physical bounds
- global/campaign/client/slot/provider/read/flood cap boundaries
- Replay independence
- T17/T19 exact hosted edge proof reused from accepted L5 because no affected edge path changed

## L7 product intent

Extend the existing static Replay UI with a bounded Live candidate for one fixed scenario only.

The candidate must remain inert by default and must not alter the currently deployed Cloudflare artifact in this Task.

The eventual browser behavior must satisfy H5:
- first successful 201 capability is stored in same-tab `sessionStorage`;
- same-tab refresh can continue GET;
- independent tab/session has no capability recovery;
- tab/session close loses it;
- URL/cookie/localStorage are never authority;
- an initial successful 201 response that the browser did not receive has no capability recovery;
- same-key retry may resolve admission truth but 202 does not reissue capability;
- Replay remains usable regardless of Live/API failure.

## API contract

Fixed:
- `POST /v1/public-live/runs`
- body exactly `{"scenario_id":"stockroom-s1-normal","scenario_version":"1.0.0"}`
- Idempotency-Key: 32 lowercase hex
- `GET /v1/public-live/runs/{run_id}`
- `X-Run-Read-Capability`
- credentials omitted
- exact public origin remains `https://aiscc-replay.pages.dev`

No free-form task/repository/provider/model/tool input.

## release-time origin/config boundary

The currently deployed ingress public domain was removed after hosted proof. L7 does not need to invent or create a Railway public API origin.

Implement a candidate that can be bound later to one exact release-time API origin and remains fail-closed/inert when that immutable origin/config is absent or disabled.

Do not weaken CSP to wildcard/general HTTPS merely to make local testing convenient.

## next review

After Executor result:
- Browser independently reviews source/Git;
- Human browser QA is expected for physical sessionStorage/new-tab/refresh/visual behavior;
- public deployment, provider canary and admission/release remain later explicit gates.
