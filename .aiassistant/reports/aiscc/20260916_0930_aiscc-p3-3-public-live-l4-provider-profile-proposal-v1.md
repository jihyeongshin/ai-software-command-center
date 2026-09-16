# P3-3 Public Live L4 Provider Profile Proposal V1

## status

```text
PROPOSED / NOT_ACCEPTED
Human approval required
```

## Browser Command Center review

The 0915 Executor proposal was reviewed against:

- exact frozen L4 authority;
- current accepted repository binding audit;
- official OpenAI model/pricing/API documentation reverified on 2026-09-16.

Browser recommendation:

`ACCEPT AS WRITTEN`

The proposal below remains a Human-owned choice until explicit approval.

---

# Public Live L4 provider profile proposal V1

Status: **PROPOSED / NOT_ACCEPTED**
Result: **HUMAN_PROVIDER_POLICY_DECISION_REQUIRED**

## One recommended bounded profile

Proposed immutable profile ID: `public-live-stockroom-s1-openai-terra-v1`, version `1`.

| Field | Proposal |
|---|---|
| Provider/model | OpenAI / `gpt-5.6-terra`, exact ID; no model/provider fallback |
| API/tier | HTTPS `https://api.openai.com/v1/responses`; `service_tier=default` |
| Mode/scenario | PUBLIC_BOUNDED_LIVE; stockroom-s1-normal / 1.0.0 only |
| Reasoning | low |
| Input | <=8000 billable tokens per request, including system text, fixed scenario, tool schema, full continuation and provider framing |
| Output | `max_output_tokens=2000` each call, reasoning included; <=4000 tokens/run |
| Calls | <=2 total, continuation and retry share this ceiling; <=2 rounds |
| Retry | SDK automatic retries 0; at most 1 policy retry only after known explicit failure and conclusive closure; never for unknown/missing response or quota/billing failure |
| Tools | Only local read-only `stockroom_summary`, <=1 dispatch/run; no hosted/built-in paid tools, MCP, images, audio, search or files |
| Transport | store/background/stream/parallel_tool_calls false; truncation disabled; server-owned local continuation; no hidden compaction/additional call |
| Time | connect 5s, read 30s, local hard call wall ceiling 35s; each also bounded by remaining admission+90s deadline |
| Concurrency | Existing 2 durable slots; sequential calls in one run; unknown remote effects retain/quarantine slot |
| Price envelope | 44000 micro-USD/call; 88000/run; immutable version and verification timestamp; validity <=24h, reverify before release and deny stale/changed pricing |
| Project defense-in-depth | Dedicated API Project; propose monthly $15 hard spend limit, alerts at $10 and $12; no automatic top-up or limit increase |
| Data policy | Synthetic fixed corpus only; standard global endpoint; no claim of Korean processing residency or ZDR |
| Credential | Human-owned project-scoped service credential represented only by an opaque reference; existing lease/capability boundary; injection/environment proof belongs to L5 |

## Rationale

Terra is the proposed middle-cost choice for the small fixed Stockroom workflow. Official documentation describes its cost/intelligence positioning; task-specific demo quality and latency have NOT been measured. Low reasoning and finite output leave a practical latency budget while keeping the price envelope well inside the frozen reservation. If the fixture cannot fit or results are incomplete, fail truthfully; do not expand tokens, choose another model, or add calls automatically. [Official Terra model](https://developers.openai.com/api/docs/models/gpt-5.6-terra)

## Worst-case inference cost (conditional on correct enforcement)

Current standard rates: $2/M input, $12/M output. Conservatively treat every input token as a cache write at 1.25x input rate; take no cache-read discount. No explicit multiple cache breakpoints, hosted paid tools or premium tier. Input 8000 stays below the documented long-context surcharge threshold. [Price basis](https://developers.openai.com/api/docs/models/gpt-5.6-terra)

```text
C_call = (8000 * 2 * 1.25 + 2000 * 12) / 1,000,000
       = $0.044 = 44000 micro-USD
C_run  <= 2 * C_call = $0.088 = 88000 micro-USD
        <= frozen $0.20 reservation
C_daily_admission_cohort <= 20 * $0.088 = $1.76 <= frozen $4
C_campaign(N,D) <= min($0.088 * N, $15), with N <= 20 * D
```

D is the number of UTC admission days actually authorized before the frozen cutoff; start time is not assumed. Campaign ledger never resets monthly. $15 remains the authoritative campaign liability limit; lower actual costs and released reservations can permit more than 75 runs. A $0.20 reservation divided into $15 is NOT a fixed lifetime run count.

These are USD model-token charges, not a bound on taxes, foreign-exchange fees, deployment or unrelated account usage. Actual above-envelope usage remains an incident, never clamped away. Unknown/missing usage conservatively consumes 44000 per possibly paid call. Unknown execution closure still holds reservation and slot; cost arithmetic alone cannot release them.

The monthly provider hard limit is extra protection, not an exact campaign cap. Documentation allows propagation overshoot and monthly reset. It does not replace application admission/reservation. [Official spend-limit behavior](https://developers.openai.com/api/docs/guides/spend-limits)

## Binding prerequisites (not implemented)

1. Pin and hash the entire approved profile, prices, validity and scenario/tool identity; bind it to each paid ordinal and fail closed when absent/stale.
2. Prove the full billable input bound. Existing byte/4 continuation estimate is insufficient. Require verified exact accounting or a proven conservative tokenizer/framing bound; no send if unknown. The documented input-count endpoint was not called and is not assumed free or authorized.
3. Enforce 2000 per-call AND 4000 run output ceiling. Existing runtime currently passes the aggregate remainder, so merely setting output_token_bound=4000 would not enforce the proposed per-call bound.
4. Add separately authorized real endpoint policy without weakening the accepted local-only fixture guard. Serialize explicit reasoning/tier and check actual tier/model evidence. Preserve usage detail, integer upward rounding, missing/unknown flags and above-bound incident truth.
5. Bind P1-5 security/credential authority to L2 DispatchAuthority/ReconciliationAuthority. Commit public marker before any send; no extra SDK retry or tool continuation outside the shared ceiling.
6. Hosted termination, source IP/TLS/network and secret-injection proof remain L5. A local timeout does not prove remote termination.

## Exact Human approval fields

Approve or revise this one profile's model, endpoint/tier, low reasoning, 8000/2000/4000 token bounds, two-call shared allocation, one known-closed retry, 5/30/35-second timeouts, single stockroom_summary tool, stateless request flags, 44000/88000 envelope, 24h freshness, global synthetic-data policy and proposed project hard-limit/alert targets. The frozen 2-slot, 90-second, $0.20/$4/$15 and campaign-cutoff rules remain unchanged.

Separately provide non-secret account evidence: dedicated project reference/isolation, effective model permission and rate limits, billing availability, hard-limit configuration and credential-reference capability binding. Do not send API key values. Proposal approval does not prove account configuration and does not authorize a paid call, deployment or admission enablement.

Stop here under the current Task. A later Task must authorize implementation and any subsequent real-provider verification separately.

