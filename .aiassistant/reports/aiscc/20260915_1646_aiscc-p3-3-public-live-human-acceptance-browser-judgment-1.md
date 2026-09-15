# AISCC Browser Command Center Judgment

## 판정

```text
result_status: HUMAN_ACCEPTED / FINAL_DESIGN_FREEZE_AUTHORIZED
phase: P3-3 POST_SUBMISSION_IMPROVEMENT_WINDOW
baseline_head: 5e35ec0d60d84c7a05a2e58ebcc6560863879e5b
```

## Human decision

Human explicitly accepted:

```text
H1 ACCEPT
H2 ACCEPT
H3 ACCEPT_BROWSER_RECOMMENDATION
H4 ACCEPT
H5 ACCEPT_BROWSER_RECOMMENDATION
H6 ACCEPT
H7 ACCEPT
```

Therefore the 1630 candidate is accepted subject to the two Browser-recommended amendments below.

## frozen amendments

### H3 — campaign cutoff

Keep UTC daily accounting.

Freeze campaign end as:

```text
2026-10-18T00:00:00+09:00 exclusive
= 2026-10-17T15:00:00Z
```

Do not use the candidate's `2026-10-18T00:00:00Z` cutoff.

### H5 — read capability persistence

Freeze:

```text
read capability:
256-bit

expiry:
24 hours

browser persistence:
sessionStorage

URL:
forbidden

cookie:
forbidden

localStorage:
forbidden

same-tab refresh:
retains access

tab/session close:
capability lost

initial successful 201 response never received:
no recovery / no automatic replacement run

public cancel:
disabled
```

## remaining accepted choices

Frozen without amendment:

- S1 only: `stockroom-s1-normal / 1.0.0`;
- 3/hour and 10/day client/IP bucket;
- 20 global admitted/day;
- 2 global concurrent;
- $0.20/run reserve;
- $4/day app budget;
- $15 campaign budget;
- IPv4 /32, IPv6 /64 pseudonymous HMAC bucket;
- conservative unknown-provider quarantine;
- separate public Live DB/credentials.

## disposition

Issue one narrow final-freeze/persistence Task.

No source implementation is authorized by this Judgment.

After successful persistence, implementation Tasks L1, L4 and L5 become eligible for separate authorization.
