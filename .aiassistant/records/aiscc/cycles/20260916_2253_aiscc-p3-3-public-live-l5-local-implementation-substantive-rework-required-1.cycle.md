# AISCC Cycle Record

## meta

- cycle_id: `20260916_2253_aiscc-p3-3-public-live-l5-local-implementation-substantive-rework-required-1`
- date: `2026-09-16 KST`
- owner: `Browser Command Center`
- phase: `P3-3 Public Live L5`
- predecessor_task: `20260916_2148_aiscc-p3-3-public-live-l5-hosted-binding-local-implementation-1`
- browser_review_export_task: `20260916_2228_aiscc-p3-3-public-live-l5-local-implementation-browser-review-export-rework-1`
- reviewed_replacement_zip_sha256: `6f38fec7898cce3016ea508d4df902490dd9d95e9d2df2c985640447d5eb2a1f`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- result_status: `REWORK_REQUIRED`
- l5_terminal: `OPEN`
- public_admission: `DISABLED`
- public_live: `NOT_RELEASED`

## transport / reviewability

The replacement Browser-review ZIP is valid:

```text
SHA-256:
6f38fec7898cce3016ea508d4df902490dd9d95e9d2df2c985640447d5eb2a1f

member_count:
27

manifest hashes:
26/26 non-self members exact

source identity:
12/12 exact

index:
empty
```

The prior export-contract blocker is CLOSED.

## substantive judgment

The candidate has several accepted/good parts:

- dedicated Public Live ingress composition is structurally separate from the owner API;
- owner route families are absent from the Public Live app;
- `RailwayEdgeIdentityAuthority` is fail-closed and release-gated;
- Uvicorn Public Live ingress sets `proxy_headers=False`;
- separate Live DB variable boundary exists;
- ingress refuses provider-secret and owner-DB variables;
- Replay architecture is unchanged;
- real provider calls remain zero.

However the candidate does not yet satisfy the accepted I4/I5/I7 implementation contract.

### blocker R1 — private worker is not a runnable durable worker

Current CLI:

```text
aiscc public-live-worker --check
```

constructs `PipelineStore` + `OpenAIResponsesAdapter` and exits.

Without `--check`, it deliberately raises:

`PUBLIC_WORKER_REQUIRES_DURABLE_SERVER_WORK_SOURCE`

The composition does not wire the accepted durable work source/supervisor/dispatcher and does not compose `HostedOpenAISecretResolver`.

Therefore `aiscc-public-live-worker` cannot yet be deployed as the accepted private durable provider worker.

### blocker R2 — `hosted-l5-proof` is only a static expectation printer

Current CLI validates environment and calls:

`expectation(FaultPoint(...))`

It does not:

- connect to the Live PostgreSQL proof state;
- call `execute_provider_fault`;
- send to the private provider double;
- observe provider-double receipts;
- restart/reconcile durable state;
- trigger sandbox/process-tree termination.

`SANDBOX_TERMINATION` is not executable through `execute_provider_fault`; it raises `SANDBOX_TERMINATION_REQUIRES_PROCESS_SUPERVISOR`.

Therefore the accepted D9 hosted QA mechanism is not implemented.

### blocker R3 — hosted OpenAI adapter still admits loopback profiles

Current provider guard permits any `http://127.0.0.1:*` profile regardless of `hosted=True`.

The accepted D8/I5 hosted worker contract requires:

```text
hosted adapter
→ exact hosted Luna profile only
→ https://api.openai.com/v1
```

Local/fake provider endpoints must use a distinct QA transport and must not be accepted by the production hosted OpenAI adapter.

### blocker R4 — proof semantics contradict durable retry behavior

`expectation(BEFORE_DISPATCH)` reports:

`retry_allowed=False`

but the durable integration test immediately proves a same-role retry is eligible after the definitely-not-sent/known-closed outcome.

The proof model and durable authority must report one consistent accepted retry semantic.

### blocker R5 — CORS preflight is broader than the exact route/method contract

The Public Live app currently accepts either requested method `POST` or `GET` on both Public Live paths and advertises both methods on each preflight.

The frozen contract is path-specific:

```text
POST /v1/public-live/runs
GET  /v1/public-live/runs/{run_id}
```

Preflight must not positively authorize the wrong method/path pair even though the actual request would later receive 405.

## effect

This is a focused implementation REWORK.

No Railway/OpenAI/Cloudflare/Git external action is authorized.

The accepted binding design remains CLOSED and is not reopened.
