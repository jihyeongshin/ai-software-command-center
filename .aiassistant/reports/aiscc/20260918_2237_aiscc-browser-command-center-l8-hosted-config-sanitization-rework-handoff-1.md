# AISCC Browser Command Center Handoff — Public fixed tool accepted / hosted configuration rework

## current canonical baseline

`232f0b7b9ad3d08ead3382e7cbebd527d17811c4`

## accepted

- Human `ACCEPT_PUBLIC_FIXED_IN_PROCESS_TOOL` amendment: implemented.
- Public fixed tool source: accepted.
- Owner/Self-Dogfood Docker non-regression: accepted.
- affected local L6 reproof: accepted.
- private worker Docker-free startup/registration: accepted.

## still blocked

Affected hosted L5 proof is not complete because ingress effective configuration currently has:

- `AISCC_OPENAI_API_KEY` present;
- `AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST` present.

Ingress public domains are still zero and DB control is disabled, so Public Live remains fail-closed.

## exact next target

Restore the pre-release hosted invariant:

```text
provider key:
worker only

ingress provider key:
absent

ingress edge trust:
absent

public domains:
0

control:
disabled

provider requests:
unchanged
```

Then repeat only no-send hosted assertions.

## provenance note

Use:

- source commit `15551972c0f402fd3e6076f01335007ec2a6f663`
- current main `232f0b7b9ad3d08ead3382e7cbebd527d17811c4`

Do not reuse the invalid target-report SHA ending in `...fb6c`.

## after successful cleanup

Next sequence remains separate:

1. Browser accepts affected L5 reproof;
2. separately reconcile the retained 1919 run as `FAILED_NOT_DISPATCHED`;
3. fresh release-readiness;
4. re-release + at most one bounded public smoke.
