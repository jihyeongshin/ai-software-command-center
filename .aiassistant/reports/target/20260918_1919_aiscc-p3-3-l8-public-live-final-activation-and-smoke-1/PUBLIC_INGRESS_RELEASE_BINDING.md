# Public Ingress Release Binding

## Temporary release binding

- Railway service: `aiscc-public-live-ingress`
- service ID: `fd09a9f2-1bf8-4a48-8af8-d1536866fa1d`
- generated HTTPS origin: `https://aiscc-public-live-ingress-production.up.railway.app`
- domain ID: `5ee3fb7e-5f07-4f93-a2b1-69a2b7b372ab`
- edge-trust value: `HOSTED_OVERWRITE_PROOF_ACCEPTED_V1`
- release deployment: `32f6e97a-6f4a-44d8-8677-0dcc6f06c2e4`, SUCCESS
- `/health`: HTTP 200
- invalid Origin: HTTP 403 `ORIGIN_DENIED`
- before campaign materialization, a valid-origin request failed closed as `POLICY_UNAVAILABLE` with zero durable side effects
- after materialization while disabled, a valid-origin request returned HTTP 503 `LIVE_DISABLED` with zero durable side effects

## Final binding after rollback

- edge-trust variable: removed
- public domain: removed
- domain count: 0
- final private ingress deployment: `07e983d8-8493-4384-afad-bc044e4e8ebe`, SUCCESS
- final deployed commit: `57c20374c2c2799aa354c43309b1515a3d13fe3f`
