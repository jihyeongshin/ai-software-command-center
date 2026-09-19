# Executor Report

- Result: `CANONICAL_PUBLIC_BUILD_MANIFEST_REPRODUCIBLE / TRACE_IMPLEMENTATION_UNCHANGED / PUBLIC_LIVE_RELEASED / NEW_RUN_0 / PROVIDER_CALL_0 / HUMAN_TRACE_QA_PENDING / BROWSER_REVIEW_REQUIRED`
- Baseline: `3178179986975709f4acec11825fc736cd3ce7c1`
- Preserved implementation: `f9bb6a5a9de35a8abd6d5b39acb17af4b6add80b`
- Final source/provenance commit: `5d1e3e8e9d82727e07ebd926e1cb9a99fe7fe593`
- Defect reproduced: Windows worktree `_headers` 484 bytes and `live-config.json` 158 bytes were hashed instead of canonical LF blobs.
- Fix: narrow `.gitattributes` LF policy for public Replay authored/generated JSON, assets, corpus inputs, and the manifest generator.
- Corrected: `_headers` 477 bytes / `fd3158e83462fb5db5ed3b17328bc39e5baae132e2e3f62fd01989fe9a1a7b64`; `live-config.json` 153 bytes / `9a14186fe2179374e25d6c198f34db2d5338cc13307558f8e2c2ef6c9c30d676`.
- Disposable clean worktree: build check PASS, 11 tests PASS, Node syntax PASS, manifest/blob identity PASS.
- Cloudflare: canonical LF deployment `6ab0639b`; public config and assets match canonical bytes.
- Railway: no CLI deploy/config action and worker unchanged. GitHub-linked ingress passively redeployed commit `5d1e3e8e9d82727e07ebd926e1cb9a99fe7fe593` and remained healthy; ingress functional sources were unchanged.
- New public run: 0. Provider call: 0. Human trace QA: pending.
