# Public Recorded Replay deployment prerequisite

Status: `IMPLEMENTATION_CANDIDATE / HUMAN_QA_PENDING`. Public deployment is `NOT_COMPLETED`.

## Accepted direction

`AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1` selects **Cloudflare Pages** for public UI / Recorded Replay. Optional Live uses Railway Hobby / Singapore and a separate OpenAI API Project; neither is part of this static release. Hosting selection is not reopened.

| Setting | Source-supported value |
| --- | --- |
| Deployment unit / output directory | `public/replay` |
| Runtime | Static HTML/CSS/JS and immutable JSON only |
| Database | None |
| Provider / LLM | None |
| Replay secrets | None |
| Live | `DISABLED_FOR_INITIAL_RELEASE` |
| Account / project / public URL / domain | Pending later authorized deployment Task |
| Production branch / provider build environment | Pending later provider verification; not inferred from local branch |

## Build and verify locally

From the repository root, with Python 3.12 or newer available:

```text
python scripts/build_public_replay.py
python scripts/build_public_replay.py --check
```

The builder uses only Python's standard library. It verifies the pinned canonical index hash/size, four member hashes/sizes and corpus root before writing. It copies all five JSON files byte-for-byte, creates static health identity and a deterministic build manifest, and rejects unknown public files. `--check` performs no writes and fails on generated drift. Authored shell assets are inputs whose hashes are frozen in the manifest.

Source corpus: `.aiassistant/reports/aiscc/replay/stockroom/v1`. The public artifact includes only `public/replay`; do not upload the repository root, canonical records outside these copies, tests, owner UI or database.

The manifest's source commit is the pre-implementation baseline `17fcd337a8bc1410e230a7c18195ac3d3006b417`. A later persistence/deployment Task must bind the final committed artifact separately. No future commit or wall-clock generation time is fabricated.

## Local review only

```text
python -m http.server 8765 --bind 127.0.0.1 --directory public/replay
```

Open `http://127.0.0.1:8765/`. Stop with Ctrl+C after review. This command serves no owner app and starts no AI execution. `health.json` is a static identity document, not a dynamic health probe. The standard-library server does not apply Cloudflare `_headers`; it returns a genuine 404 for missing files. Inspect `/404.html` separately for the authored error page.

## Later deployment choices — not executed

1. Git-connected Cloudflare Pages: after authorized persistence/push and provider setup verification, use the verified repository checkout, run `python scripts/build_public_replay.py` and publish only `public/replay`. Python availability, root directory, production branch and build settings must be checked in the actual provider project.
2. Direct upload: upload the exact verified `public/replay` directory only if the later deployment Task verifies current Cloudflare support and the selected project's workflow. No CLI/authentication command is prescribed here.

No account ID, slug, domain, pricing, current provider capability, authenticated state or `pages.dev` address has been established. No deployment action is authorized by this document.

## Routing, data and failure boundary

Scenario selection uses `#scenario=<accepted-scenario-id>` on the root page. Only the five allowlisted same-origin JSON files are fetched with GET, omitted credentials and redirects rejected. There are no forms, mutation endpoints, uploads or Live controls. Unknown selectors and missing/malformed records display explicit errors with no runtime fallback.

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
