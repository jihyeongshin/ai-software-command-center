# AISCC Cycle Record

## meta

- cycle_id: `20260916_2148_aiscc-p3-3-public-live-l5-hosted-binding-design-final-acceptance-implementation-entry-1`
- date: `2026-09-16 KST`
- owner: `Browser Command Center`
- phase: `P3-3 Public Live L5`
- predecessor_design_task: `20260916_2012_aiscc-p3-3-public-live-l5-hosted-production-binding-design-freeze-1`
- predecessor_result_zip_sha256: `4b40a040e9ec764926dedd1a46e09d93fb0472694baddae49ccfcea7b35d9b0a`
- accepted_source_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- result_status: `HUMAN_PROVIDED / HOSTED_PUBLIC_LIVE_BINDING_DESIGN_ACCEPTED / IMPLEMENTATION_ENTRY`
- l5_terminal: `OPEN`
- public_admission: `DISABLED`
- public_live: `NOT_RELEASED`

## Human decision

Human selected:

`A — ACCEPT_APPLICATION_MEDIATED_EGRESS`

The selected D8 residual-risk posture is accepted for this bounded competition runtime.

Human rationale recorded:

- this is a competition runtime, not a production customer workload;
- the service is intentionally bounded and structurally separated;
- even if the trusted provider worker itself were fully compromised, OpenAI account/project controls provide an independent financial blast-radius backstop;
- current OpenAI project hard spend limit remains `$15`, in addition to accepted application call/run/day/campaign ceilings.

## precision / non-overclaim

The OpenAI hard-spend limit bounds provider-spend exposure. It does NOT prove or bound every consequence of a compromised trusted process, including availability impact or mutation of the separate Live database.

Therefore acceptance of D8 does not replace:

- structural public/owner service separation;
- separate Live database;
- worker-only secret ownership;
- no public arbitrary-network input;
- fixed provider transport;
- sandbox/tool child `network=none`;
- hosted secret non-exposure proof;
- hosted egress observation/proof;
- supervisor no-send/unknown quarantine proof.

## accepted hosted binding design

The entire 2012 candidate is accepted with D8 Option A:

```text
Cloudflare Pages
  = public UI + static Recorded Replay

aiscc-public-live-ingress
  = sole anonymous Railway Public Live HTTP service
  = no OpenAI key
  = no owner routes
  = Live DB only

aiscc-public-live-worker
  = private provider worker
  = sole AISCC_OPENAI_API_KEY owner
  = application-mediated OpenAI transport
  = Live DB only

aiscc-trusted-api
  = existing owner/Command Center API
  = no anonymous public domain after later cutover
  = owner DB only
  = no OpenAI key after later cutover

aiscc-public-live-postgres
  = separate Live durable store
  = no public TCP exposure

aiscc-public-live-provider-double
  = temporary private QA-only fake provider
```

Additional accepted design facts:

- Public Live path prefix: `/v1/public-live`
- exact public route allowlist remains the accepted 2012 matrix;
- default-deny all non-allowlisted routes;
- Uvicorn Public Live ingress uses `--no-proxy-headers`;
- `scope["client"]` is not end-user security authority;
- Railway `X-Real-IP` is not trusted until hosted overwrite/spoof proof succeeds;
- `RailwayEdgeIdentityAuthority` alone may set `direct_peer_verified`;
- `X-Railway-Edge` is provenance only;
- no Railway CIDR/hop-count guess;
- missing/conflicting/ambiguous identity fails closed;
- hosted supervisor proof uses operator-only non-HTTP QA CLI and private provider double;
- Replay remains static/zero-inference and independent of Railway/provider failure.

## next action

Implement the accepted design locally only.

No Railway, Cloudflare, OpenAI, Git commit/push, paid canary, or Public enablement is authorized.
