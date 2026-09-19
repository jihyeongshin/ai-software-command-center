# AISCC Browser Command Center Handoff — worker renewal/pin race + known-outcome settlement

## current baseline

`29ce5ce4b39958558091862c345c749584fd2d0f`

## current operating state

```text
Public Live:
NOT_RELEASED

public_control:
FALSE

frontend:
Replay-only

PARKED ingress domain:
PRESENT

release origin:
PRESENT

edge trust:
PRESENT

ingress:
HEALTHY

worker/provider secret topology:
RETAINED
```

## closed blockers

- provider HTTP request compatibility: CLOSED by real provider `PROVIDER_COMPLETED`
- fixed Stockroom runtime applicability: CLOSED by real `TOOL_COMPLETED`
- PARKED_FAIL_CLOSED topology: ACCEPTED

## new source blocker

`PUBLIC_WORKER_CLAIM_RENEWAL_DISPATCH_PIN_RACE`

Current exact-version consumers include:
- initial worker claim context;
- provider operation bind;
- provider dispatch pin.

Renewal and those consumers are not serialized against the same mutable `ActiveClaim.ref`.

The fix should synchronize only the short exact-version DB authority windows.

Do NOT hold a claim-version lock across the 35-second provider HTTP call or tool execution.

## retained third smoke

Observed identity for cross-check only:

`qhWtsIdC8l5-NypgDR4vkQ`

Do not select the mutation target by copied ID alone.

Strict facts:
- one new run from 1335;
- expired ADMITTED;
- attempt EXECUTION_FAILED / RECOVERY_CONFLICT;
- provider op 1 completed after dispatch;
- tool op 2 completed after dispatch;
- provider op 3 cancelled before dispatch;
- one physical provider send;
- retry 0;
- provider UNKNOWN 0;
- reservation HELD 200000;
- slot OCCUPIED;
- outbox BOUND;
- SETTLE 0;
- open claims/pins 0/0;
- worker work non-claimable due expiry.

## settlement direction

Audit existing mediated settlement first.

If legacy `ReconciliationService.close()` would derive zero because `public_dispatch` is empty, it is NOT valid for this P1-5 run.

Preferred canonical repair if no existing correct bridge exists:
- migration 0026;
- strict candidate predicate;
- exact P1-5 known-outcome operation/event evidence;
- conservative liability only for provider operations that actually crossed `DISPATCH_STARTED`;
- cancelled-before-dispatch operation contributes zero;
- local fixed tool contributes zero provider liability;
- idempotent settlement;
- truthful terminal projection;
- no raw-table operator mutation.

Keep PARKED topology intact throughout.
