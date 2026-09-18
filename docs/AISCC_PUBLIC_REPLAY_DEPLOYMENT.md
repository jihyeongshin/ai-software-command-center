# Public Recorded Replay and bounded Live candidate

Status: Replay is deployed and Human-accepted at `https://aiscc-replay.pages.dev`. The L7 bounded Live source candidate is `RELEASE_DISABLED / BROWSER_REVIEW_REQUIRED`; this Task does not deploy it.

## Accepted direction

`AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1` selects **Cloudflare Pages** for public UI / Recorded Replay. Optional Live uses Railway Hobby / Singapore and a separate OpenAI API Project; neither is part of this static release. Hosting selection is not reopened.

| Setting | Source-supported value |
| --- | --- |
| Deployment unit / output directory | `public/replay` |
| Runtime | Static HTML/CSS/JS and immutable JSON only |
| Database | None |
| Provider / LLM | None |
| Replay secrets | None |
| Live | `DISABLED / NOT_RELEASED` |
| Exact public browser Origin | `https://aiscc-replay.pages.dev` |
| Production branch / provider build environment | Pending later provider verification; not inferred from local branch |

## Build and verify locally

From the repository root, with Python 3.12 or newer available:

```text
python scripts/build_public_replay.py
python scripts/build_public_replay.py --check
```

The builder uses only Python's standard library. It verifies the pinned canonical index hash/size, four member hashes/sizes and corpus root before writing. It copies all five JSON files byte-for-byte, creates static health identity and a deterministic build manifest, and rejects unknown public files. `--check` performs no writes and fails on generated drift. Authored shell assets are inputs whose hashes are frozen in the manifest.

Source corpus: `.aiassistant/reports/aiscc/replay/stockroom/v1`. The public artifact includes only `public/replay`; do not upload the repository root, canonical records outside these copies, tests, owner UI or database.

The manifest's source commit is the pre-implementation baseline `17fcd337a8bc1410e230a7c18195ac3d3006b417`. A later release Task must bind the final committed artifact separately. No future commit or wall-clock generation time is fabricated.

## L7 bounded Live candidate

`public/replay/live-config.json` is immutable same-origin release configuration. The repository candidate is deliberately fail-closed:

```json
{
  "api_origin": null,
  "enabled": false,
  "schema": "AISCC-PUBLIC-LIVE-FRONTEND-CONFIG-V1"
}
```

Missing, malformed or disabled configuration sends no Live API request and does not affect Replay. Enabled configuration accepts one HTTPS origin with no path, query, fragment or credentials. The browser cannot source that origin from a URL, hash, DOM field, cookie, localStorage or user input.

A later release-authorized change must bind one real exact API origin in both places in the same reviewed artifact:

1. Set `enabled` to `true` and `api_origin` to the exact origin in `live-config.json`.
2. Add that same exact origin to `_headers` `connect-src` beside `'self'`.

Never use `*`, generic `https:`, `unsafe-inline` or `unsafe-eval`. If config and CSP are not bound together, Live fails visibly while Replay remains usable. This candidate does not choose a Railway origin, enable Public admission or authorize release.

The only Live request body is fixed to `stockroom-s1-normal / 1.0.0`. A confirmed 201 stores the run ID, one-time read capability, expiry and idempotency key only in same-tab `sessionStorage`. Refresh resumes bounded GET; a separate tab cannot recover. A 202 without the original 201 capability cannot recover status, and uncertain admission retries reuse the same key. Polling uses a 3-second interval, stops after 40 reads or sooner on terminal state, expiry, explicit local stop or failure, and stays below the accepted 30-read/minute ceiling.

## Local review only

```text
python -m http.server 8765 --bind 127.0.0.1 --directory public/replay
```

Open `http://127.0.0.1:8765/`. Stop with Ctrl+C after review. This command serves no owner app and starts no AI execution. `health.json` is a static identity document, not a dynamic health probe. The standard-library server does not apply Cloudflare `_headers`; it returns a genuine 404 for missing files. Inspect `/404.html` separately for the authored error page.

## Later deployment choices — not executed

1. Git-connected Cloudflare Pages: after authorized persistence/push and provider setup verification, use the verified repository checkout, run `python scripts/build_public_replay.py` and publish only `public/replay`. Python availability, root directory, production branch and build settings must be checked in the actual provider project.
2. Direct upload: upload the exact verified `public/replay` directory only if the later deployment Task verifies current Cloudflare support and the selected project's workflow. No CLI/authentication command is prescribed here.

No Live API origin, Railway public domain, provider credential or authenticated release state is established here. No deployment action is authorized by this document.

## Routing, data and failure boundary

Scenario selection uses `#scenario=<accepted-scenario-id>` on the root page. Replay fetches only the five allowlisted same-origin corpus JSON files with GET, omitted credentials and redirects rejected. Unknown selectors and missing/malformed records display explicit errors with no runtime fallback. The separate Live surface additionally fetches only same-origin `live-config.json`; when release-disabled it sends no API request. When a later release binds exact config and CSP, its only mutation is the fixed POST described above, followed by capability-authorized GET. There are no forms, uploads, free-form inputs or public control/cancel routes.

The root-level `404.html` is intended for later Pages missing-file behavior. Do not configure a wildcard SPA rewrite. Missing URLs must not become successful Replay pages.

`_headers` restricts scripts/styles/connect to same origin, denies framing and form actions, disables sensitive browser permissions and sets nosniff/no-referrer. Effective headers and custom 404 behavior require post-deployment verification.

## Required later checks

- Human readability QA at 1080, 1280 and 1440 desktop widths and all four records.
- Exact final commit and byte inventory; public corpus remains identical to accepted source.
- Account/project authorization and rights/tool disclosure confirmation.
- Public HTTPS root, static assets, health identity and all four data records.
- Correct security response headers, genuine unknown-file 404, truthful Recorded / Live-disabled labels.
- Network trace contains no owner/private API, provider, tracker or external asset requests.
- Missing/corrupt-data errors remain errors, without hidden AI fallback.
- Verified rollback to a prior immutable artifact and assigned recovery/availability owner.

Keep Replay available during judging (Browser-supplied window: 2026-09-21 through 2026-10-05), with the accepted operational horizon through 2026-10-17. Reverify official facts before Human final submission. Local HTTP 200 and deterministic build are not public deployment or Human acceptance.
