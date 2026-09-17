# 작업지시서: P3-3 L5 Hosted Public Live Production Binding Design Freeze

## meta

- task_id: `20260916_2012_aiscc-p3-3-public-live-l5-hosted-production-binding-design-freeze-1`
- created_at: `2026-09-16 KST`
- work_type: `SECURITY_DEPLOYMENT_DESIGN`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- primary_semantic_owner: `P3-3 L5 hosted production composition / ingress / supervisor / egress binding`

Use the current IDE Executor conversation. No fresh chat is required.

## predecessor judgment

The predecessor mandatory stop is Browser-accepted:

`HOSTED_COMPOSITION_BINDING_DESIGN_REQUIRED`

This Task is NOT an implementation retry.

Do not change source/test/config/migrations.

## objective

Produce one exact Human-reviewable production binding design that makes the later L5 implementation and hosted QA unambiguous without weakening any accepted P1/P3 invariant.

The design must decide all previously missing production ownership boundaries.

## mandatory authority recovery

Re-read and reconcile:

1. frozen L5 sequence from commit
   `209e7534f66e9b07ce9d33742e6993370a70f4fb`;
2. current accepted `AISCC_SECURITY_SANDBOX` canonical rule;
3. current accepted provider/tool/secret execution authority;
4. current Public Replay + Bounded Live runtime boundary;
5. current L1-L4 Public Live runtime/security decisions;
6. predecessor:
   `HOSTED_L5_PROOF_BRIDGE_AUDIT.md`;
7. predecessor:
   `HOSTED_L5_HUMAN_QA_PLAN.md`;
8. current deployed source owners at HEAD `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`.

If exact authority conflicts rather than merely leaving a deferred deployment choice: STOP with the conflicting citations/paths.

## current accepted hosted state

```text
Railway Project:
AISCC

Environment:
production

deployed service:
aiscc-public-live-api

deployed ASGI app:
aiscc.api.app:app

service:
ONLINE / ACTIVE
Singapore

Postgres:
ONLINE / Singapore

AISCC_OPENAI_API_KEY:
service-local / sealed / hidden

source:
96a4029ec3a82c9b2a88b9718732aa0f00ecad20

Public admission:
DISABLED

Public Live:
NOT_RELEASED

real provider calls:
0
```

Current source fact:

- deployed trusted app has owner Command Center DB-read/UI/security routes;
- isolated `PublicLiveApp` exists separately and is not mounted.

## current external official facts — Browser-provided, reverify if network is available

Use official/current sources only for load-bearing platform facts.

### Railway

Official docs as of 2026-09-16:

- Public Networking uses Railway's global edge.
- Edge flow: user → nearest Railway edge → TLS termination/edge processing → internal routing → deployment.
- documented inbound request headers include:
  - `X-Real-IP` — client's remote IP;
  - `X-Forwarded-Proto` — `https`;
  - `X-Forwarded-Host` — original host;
  - `X-Railway-Edge` — edge POP;
  - `X-Request-Start`;
  - `X-Railway-Request-Id`.
- Edge Rules can match client IPv4, host, path, and headers; documented terminal actions are block/allow/challenge/redirect plus cache override.
- Railway private DNS is project/environment scoped; browser clients cannot directly access the private network.
- do NOT assume stable/public Railway edge CIDRs unless an official current source explicitly provides and guarantees them.
- do NOT infer generic header rewrite capability from Edge Rules.

Official source families:
- `https://docs.railway.com/networking/public-networking`
- `https://docs.railway.com/networking/public-networking/specs-and-limits`
- `https://docs.railway.com/networking/edge-networking`
- `https://docs.railway.com/networking/edge-rules`
- `https://docs.railway.com/networking/private-networking`

### Uvicorn

Official docs:

- proxy headers are supported for `X-Forwarded-Proto` / `X-Forwarded-For`;
- trust is restricted by `forwarded-allow-ips`;
- default trust is environment value or `127.0.0.1`;
- trust-all `*` is unsafe unless upstream values are conclusively trustworthy.

Official source:
- `https://www.uvicorn.org/settings/`
- `https://www.uvicorn.org/deployment/`

If current official docs differ, record the difference and use the current official fact.

## mandatory design decisions

The design must decide, not defer, the following unless an official platform fact makes the requested contract impossible.

### D1 — service/process split

Choose exactly one:

A. same Railway service/process with explicit public-vs-owner ingress partition;
B. same Railway service, separate ASGI listener/process/target port;
C. separate Railway service for anonymous Public Live, with trusted/owner app remaining non-public;
D. another exact architecture justified by accepted constraints.

For each candidate:

- analyze owner-route exposure;
- DB/secret scope;
- operational cost;
- deployment complexity;
- supervisor proofability;
- egress proofability;
- Replay independence;
- risk of accidental public owner surface.

Select exactly one recommended design.

Do not implement it.

### D2 — exact public host/path

Specify:

- public host owner;
- exact public route prefix;
- exact allowed methods/routes;
- explicit denied route families;
- relationship to Cloudflare submitted UI/Replay URL;
- whether Railway domain is directly browser-visible or only used behind another trusted ingress.

No placeholder like `<host>` unless Human must choose a DNS name; if Human choice remains, specify the exact decision field and security equivalence class.

### D3 — client identity/trusted edge

Design an exact source of public client identity.

The design must address:

- authoritative field: socket peer vs `X-Real-IP` vs another exact mechanism;
- why it is server-owned/trusted;
- how duplicate/malformed/comma/zone/port forms are handled;
- what happens if client supplies its own value;
- what happens if required Railway edge evidence is absent;
- whether `X-Railway-Edge` participates and whether it is provenance only or authorization;
- exactly who sets `direct_peer_verified`.

A documentation statement that `X-Real-IP` identifies the remote IP is not enough to assert anti-spoof overwrite. The design must require hosted positive/spoof evidence before enablement.

Do not use guessed Railway CIDRs.

### D4 — Uvicorn proxy behavior

Specify exact production flags/environment behavior:

- `--proxy-headers` or `--no-proxy-headers`;
- exact `--forwarded-allow-ips` if used;
- whether ASGI `scope["client"]` is security-authoritative;
- how the choice composes with D3.

Do not use `*` trust unless the design supplies conclusive upstream overwrite proof and Browser later accepts it.

### D5 — public owner-route exclusion

Specify how anonymous ingress cannot reach:

- `/v1/command-center/**`;
- `/command-center/**`;
- `/v1/security/**`;
- any owner/admin/debug/docs route;
- any future route not explicitly allowlisted.

Prefer structural separation over a display/header label.

Require fail-closed default-deny behavior for new routes.

### D6 — database boundary

Specify:

- whether Public Live service uses same Postgres instance;
- exact repository/service layer that Public Live may call;
- how owner Command Center repositories are unreachable from public request handling;
- whether a separate DB role is required now, later, or explicitly not required, with rationale;
- no public DB network exposure.

Do not broaden DB credentials without explicit justification.

### D7 — secret boundary

Specify:

- which service owns `AISCC_OPENAI_API_KEY`;
- whether current sealed variable moves/copies under later Human authorization;
- exact resolver owner;
- child/sandbox exclusion;
- no raw key in build/report/log/DB/Replay;
- rotation sequence.

Do not read or expose the current real key.

### D8 — service-level egress

Railway service-level outbound connectivity is broader than the Docker sandbox's `network=none`.

Design the proof/control boundary for:

- OpenAI `api.openai.com:443`;
- Postgres private-network destination;
- any required Railway/internal DNS;
- everything else.

If Railway Hobby cannot enforce an outbound allowlist, state that clearly and design an application-mediated fail-closed egress owner plus hosted proof strategy; do not falsely claim platform firewall isolation.

### D9 — supervisor/no-send/unknown hosted proof

Specify an exact hosted QA mechanism that can prove, without paid provider use:

- termination before durable dispatch => definitely not sent;
- termination after durable dispatch but before confirmed provider outcome => unknown/quarantined;
- restart => no blind resend;
- process/container tree termination/closure or explicit quarantine;
- budget/slot closure semantics.

Use fake/synthetic transport or an internal test double. No public bypass endpoint carrying secret/provider authority.

Specify who may trigger this QA and how it is unavailable in released anonymous mode.

### D10 — Replay failure-domain independence

Specify the exact relation among:

- Cloudflare public UI/Replay;
- Railway Live backend;
- provider failure;
- Railway backend failure.

Replay must remain viewable with zero inference when Railway Live is unavailable.

No Cloudflare mutation in this design Task.

### D11 — release-time public ingress proof

Produce exact later Human QA cases, including at least:

- normal allowlisted Public Live request with admission still disabled => truthful disabled result / zero provider call;
- forged `X-Real-IP`;
- duplicate `X-Real-IP`;
- comma-list `X-Real-IP`;
- forged `X-Forwarded-For`;
- forged `Forwarded`;
- forged `X-Real-IP` + Railway-generated actual identity conflict;
- forged `X-Railway-Edge`;
- missing expected edge identity;
- owner route probes;
- arbitrary unknown route;
- unsupported method;
- malformed client identity;
- direct/private path attempt where applicable.

For each case give expected HTTP/security outcome and what is safe to log.

### D12 — exact later deployment topology

Give a concrete post-design topology table:

```text
component
platform
service/process
public?
private network?
DB access?
OpenAI secret?
provider egress?
owner routes?
Public Live routes?
health route?
```

Also state what happens to the existing deployed `aiscc-public-live-api` service name and its sealed key.

## alternatives and decision record

Create:

`HOSTED_PUBLIC_LIVE_BINDING_DESIGN.md`

It must include:

- candidate A/B/C comparison;
- selected design;
- rejection reasons;
- exact trust model;
- exact route matrix;
- exact data/secret/network matrix;
- exact hosted QA matrix;
- migration/deployment sequence;
- rollback strategy;
- remaining Human-owned decisions.

Create:

`HOSTED_PUBLIC_LIVE_BINDING_DECISION.json`

with stable machine-readable keys for D1-D12.

## design acceptance constraints

The selected design MUST preserve:

- `AgentOutput != SystemState`;
- public free-form task forbidden;
- external repo/upload forbidden;
- arbitrary shell/network forbidden;
- fixed synthetic repository;
- allowlisted scenarios only;
- server-fixed provider/model;
- finite calls/retries/time/budget;
- mediated server-owned secret use;
- unknown outcome no blind retry;
- Replay zero execution;
- no public owner/private workspace access;
- no public owner DB route;
- Public admission disabled until later release;
- paid calls and deployment actions separately authorized.

## implementation authorization

NONE.

This Task may create only design/governance/report artifacts.

Forbidden:

```text
product source mutation
test mutation
migration mutation
deployment config mutation
Railway mutation
Railway deploy/restart
Railway public domain generation
Railway Edge Rule mutation
Cloudflare mutation
OpenAI call
real secret read/export
Git commit
Git push
Public enable
```

## evidence / checks

Required:

- exact HEAD verification;
- index/worktree inventory;
- current source audit;
- frozen authority recovery;
- official platform-fact register with verification date/source;
- internal consistency check against accepted P1/P3 invariants;
- no-secret scan of design/report artifacts;
- `git diff --check` for governance/design outputs where applicable.

No product tests are required because product source mutation is forbidden.

## acceptable outcome

`HOSTED_PUBLIC_LIVE_BINDING_DESIGN_CANDIDATE / HUMAN_REVIEW_REQUIRED`

This is not design acceptance.

## mandatory stop

- frozen authority mismatch;
- current source differs materially from accepted deployed HEAD;
- official current platform behavior makes every safe candidate impossible;
- a load-bearing choice requires Human product preference that cannot be reduced to security-equivalent alternatives;
- design would require weakening an accepted P1 invariant.

## export

Create:

`.aiassistant/reports/target/20260916_2012_aiscc-p3-3-public-live-l5-hosted-production-binding-design-freeze-1/`

Required:

- `EXECUTOR_REPORT.md`
- `HOSTED_PUBLIC_LIVE_BINDING_DESIGN.md`
- `HOSTED_PUBLIC_LIVE_BINDING_DECISION.json`
- `OFFICIAL_PLATFORM_FACT_REGISTER.md`
- `DESIGN_CONSISTENCY_CHECK.md`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`
- exact Task copy
- result ZIP

## final response

1. result
2. HEAD
3. frozen authority recovery
4. current source composition
5. selected topology
6. alternatives rejected
7. trusted client identity design
8. Uvicorn/proxy design
9. owner-route exclusion
10. DB boundary
11. secret boundary
12. egress boundary
13. supervisor/no-send/unknown proof design
14. Replay independence
15. hosted spoof/QA matrix
16. official platform facts
17. source/product changes
18. external actions
19. Public state
20. workspace integrity
21. Human-review status
