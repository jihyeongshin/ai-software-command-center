# AISCC Browser Command Center Judgment

## 판정

```text
result_status: ACCEPTED / LIVE_PREREQUISITE_DESIGN_CANDIDATE
human_acceptance: PENDING
phase: P3-3 POST_SUBMISSION_IMPROVEMENT_WINDOW
head: 5e35ec0d60d84c7a05a2e58ebcc6560863879e5b
```

## accepted design evidence

1630 retry successfully produced all seven required design artifacts and passed structural/internal consistency validation.

Accepted candidate includes:

- serialized PostgreSQL public admission transaction;
- durable idempotency/tombstone;
- trusted client/IP bucket contract;
- 3/hour, 10/day client caps;
- 20/day global cap;
- global concurrency 2;
- integer micro-USD ledger;
- $0.20/run reserve;
- $4/day application budget;
- $15 campaign budget;
- separate public Live DB/credentials;
- public POST/GET only, no cancel;
- high-entropy read capability;
- exact-origin CORS;
- truth-preserving unknown-provider outcome quarantine;
- 34 deterministic security/race test designs;
- L0-L8 dependency-ordered implementation sequence.

No implementation/release authority follows automatically.

## Browser recommendations for Human decisions

Accept as proposed:

- H1 continue prerequisite work before deadline;
- H2 caps/admission/ledger contract;
- H4 IP bucketing/HMAC/NAT tradeoff;
- H6 conservative unknown-outcome quarantine;
- H7 separate public Live DB/credentials.

Amend before implementation:

### H3 campaign cutoff

Keep UTC day accounting for deterministic daily ledgers.

Change campaign close from:

`2026-10-18T00:00:00Z exclusive`

to:

`2026-10-18T00:00:00+09:00 exclusive`
(`2026-10-17T15:00:00Z`)

Reason: competition/judging operations are Korea-local; the budget window should not silently extend nine hours into 2026-10-18 KST.

### H5 read capability browser persistence

Keep:

- 24h capability expiry;
- no public cancel;
- no capability recovery if the initial successful response is never received.

Change browser retention from process-memory-only to:

`sessionStorage`

Reason: a normal page refresh should not destroy the judge's ability to observe an already-running synthetic Live run. The token remains out of URL/cookies and disappears when the tab/session ends.

This amendment requires a narrow design update before source implementation.
