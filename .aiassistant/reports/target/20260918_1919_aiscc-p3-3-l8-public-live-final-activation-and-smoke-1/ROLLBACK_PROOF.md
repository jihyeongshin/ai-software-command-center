# Rollback Proof

The authorized rollback was executed after the single smoke run exceeded its deadline in `ADMITTED`.

Order and evidence:

1. DB `public_control.enabled=false` was committed first.
2. Frontend config was restored to `enabled=false`, `api_origin=null`.
3. CSP was restored to `connect-src 'self'`.
4. Rollback commit `57c20374c2c2799aa354c43309b1515a3d13fe3f` was pushed to `origin/main`.
5. Cloudflare production deployment `18c72157-3c89-4cb7-bfe5-f859cd156044` restored Replay-only.
6. Railway edge-trust variable was removed.
7. Railway domain `5ee3fb7e-5f07-4f93-a2b1-69a2b7b372ab` was deleted.
8. Ingress was successfully redeployed privately as `07e983d8-8493-4384-afad-bc044e4e8ebe`.
9. Campaign/run/claim evidence was preserved.
10. Worker provider key remained sealed on the worker.

Final public verification:

- `https://aiscc-replay.pages.dev/`: HTTP 200
- `live-config.json`: disabled/null
- CSP: self-only connect
- Replay scenario count: 4
- Railway ingress domain list: empty
