# Frontend and Cloudflare Release Proof

## Release deployment

- Git commit: `918f5e8ad62038b967c982ef5aa860d1785f5742`
- Cloudflare project: `aiscc-replay`
- environment/branch: Production / `main`
- deployment ID: `0e64babf-3e44-4a58-b575-49d21e9320eb`
- deployment URL: `https://0e64babf.aiscc-replay.pages.dev`
- production alias served `enabled=true` and the exact Railway API origin
- CSP `connect-src` contained only `'self'` plus the exact ingress origin
- Replay page and all four corpus members remained available

## Rollback deployment

- Git commit: `57c20374c2c2799aa354c43309b1515a3d13fe3f`
- deployment ID: `18c72157-3c89-4cb7-bfe5-f859cd156044`
- deployment URL: `https://18c72157.aiscc-replay.pages.dev`
- production alias now serves `enabled=false`, `api_origin=null`
- CSP `connect-src` is restored to `'self'`
- public Replay URL remains HTTP 200
