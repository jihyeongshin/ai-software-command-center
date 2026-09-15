# Human Task: P3-3 Public Live prerequisite design acceptance gate

## current candidate

1630 design candidate status:

```text
LIVE_PREREQUISITE_DESIGN_CANDIDATE / HUMAN_ACCEPTANCE_PENDING
```

No implementation has occurred.

This is a Human decision gate only.

## Decision H1 — continue before deadline

Candidate:

```text
Continue the single-scenario Public Bounded Live prerequisite work before the submission edit deadline.
```

Browser recommendation:

```text
ACCEPT
```

Reason:
Static Replay is already safely submitted, so Live work can proceed as an optional improvement without putting the submission critical path at risk.

Answer:

```text
H1: ACCEPT / REJECT
```

## Decision H2 — admission and budget caps

Candidate:

```text
scenario:
stockroom-s1-normal only

client:
3 starts/hour
10 starts/day

global:
20 admitted/day
2 concurrent

per-run reserve:
$0.20

daily application budget:
$4.00

campaign application budget:
$15.00
```

Browser recommendation:

```text
ACCEPT
```

The caps are intentionally conservative and the $0.20 reserve exceeds the provisional two-call $0.136 worst-case calculation.

Answer:

```text
H2: ACCEPT / REJECT / MODIFY
```

## Decision H3 — accounting/campaign time boundary

Candidate design currently says:

```text
daily ledger:
UTC day

campaign end:
2026-10-18T00:00:00Z exclusive
```

Browser recommendation:

```text
MODIFY
```

Recommended final contract:

```text
daily ledger:
UTC day

campaign end:
2026-10-18T00:00:00+09:00 exclusive
= 2026-10-17T15:00:00Z
```

Reason:
Keep UTC day arithmetic simple, but align the competition campaign cutoff to Korea-local end-of-day on 2026-10-17 rather than extending into the next KST morning.

Answer:

```text
H3: ACCEPT_BROWSER_RECOMMENDATION / KEEP_CANDIDATE / OTHER
```

## Decision H4 — public client identity/privacy tradeoff

Candidate:

```text
IPv4:
/32 bucket

IPv6:
/64 bucket

stored identity:
HMAC pseudonymous bucket only

raw IP:
not persisted/logged

NAT:
shared limit accepted

retention:
campaign end + 30 days
longer only for unresolved liability
```

Browser recommendation:

```text
ACCEPT
```

This is not strong user identity; it is only an abuse bucket combined with global limits.

Answer:

```text
H4: ACCEPT / REJECT / MODIFY
```

## Decision H5 — read capability UX/security

Candidate currently:

```text
read token:
256-bit

expiry:
24 hours

public cancel:
none

browser persistence:
memory only

page refresh:
read access lost
```

Browser recommendation:

```text
MODIFY
```

Recommended final contract:

```text
read token:
256-bit

expiry:
24 hours

public cancel:
none

browser persistence:
sessionStorage

URL/cookie:
forbidden

tab/session closed:
token lost

initial 201 response never received:
no recovery and no automatic replacement run
```

Reason:
A normal refresh should not make a judge lose access to a run already consuming budget. `sessionStorage` preserves refresh UX without putting the capability in URL or cookies.

Answer:

```text
H5: ACCEPT_BROWSER_RECOMMENDATION / KEEP_CANDIDATE / OTHER
```

## Decision H6 — unknown provider outcome

Candidate:

If a paid dispatch may have escaped but its terminal effect cannot be proven:

```text
- no automatic resend
- conservative charge
- slot remains quarantined
- no automatic refund
- Replay remains available
```

In the worst case, both slots can become quarantined and Live disables itself until reconciliation.

Browser recommendation:

```text
ACCEPT
```

This favors safety/cost truth over Live availability.

Answer:

```text
H6: ACCEPT / REJECT
```

## Decision H7 — database isolation

Candidate:

```text
Public Live:
separate PostgreSQL DB/credentials

Owner/private runtime:
not shared with public ingress

public runtime role:
least privilege / no arbitrary direct DML
```

Browser recommendation:

```text
ACCEPT
```

Answer:

```text
H7: ACCEPT / REJECT
```

# Recommended Human response

If all Browser recommendations are acceptable, replying exactly this is sufficient:

```text
H1 ACCEPT
H2 ACCEPT
H3 ACCEPT_BROWSER_RECOMMENDATION
H4 ACCEPT
H5 ACCEPT_BROWSER_RECOMMENDATION
H6 ACCEPT
H7 ACCEPT
```

## effect of acceptance

This Human acceptance does NOT enable Live and does NOT authorize paid resources.

Because H3/H5 are recommended amendments, acceptance will first cause Browser Command Center to issue one narrow design-finalization Task.

Only after that design is frozen will implementation Tasks be issued.
