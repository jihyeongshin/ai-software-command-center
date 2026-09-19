# AISCC Cycle Record

## meta

- cycle_id: `20260919_1501_aiscc-p3-3-l8-third-release-parked-accepted-worker-race-entry-1`
- date: `2026-09-19 KST`
- primary_semantic_owner: `Browser Command Center`
- phase: `P3-3 / L8`
- predecessor_task: `20260919_1335_aiscc-p3-3-l8-parked-fail-closed-topology-and-third-public-release-1`
- predecessor_result_zip_sha256: `09968b78cb3168acea3151e075c061dd8d0bb3c506d328a711021839282dc307`
- result_status: `PARKED_ACCEPTED / THIRD_RELEASE_FAILED / WORKER_RACE_REWORK_REQUIRED`
- Public_Live: `NOT_RELEASED`
- rollback_state: `PARKED_FAIL_CLOSED`
- release_authority: `NONE`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260919_1501_aiscc-p3-3-l8-third-release-parked-accepted-worker-race-entry-1.cycle.md`

## Browser bundle verification

- result ZIP SHA-256: `09968b78cb3168acea3151e075c061dd8d0bb3c506d328a711021839282dc307`
- ZIP integrity: `PASS`
- archive members: `28`
- manifest rows: `27/27 hash+size PASS`
- issued Task ↔ result `TASK.md` ↔ `tasks/done`: `BYTE_IDENTICAL`
- Task SHA-256: `a23b111be5313e4c8834c5b99b1eddb3221500a85a544dddc459fbc3a18a0575`
- obvious provider/DB/SSH private secret material: `NOT DETECTED`

## accepted release infrastructure result

The new rollback policy is accepted.

`PARKED_FAIL_CLOSED` was actually established and survived repeated deployment:

```text
ingress public domain:
PRESENT / one exact Railway HTTPS domain

release origin:
PRESENT / exact ingress origin

edge trust:
PRESENT / accepted exact binding

ingress:
HEALTHY

public_control.enabled:
FALSE after rollback

frontend:
Replay-only

valid parked admission:
503 LIVE_DISABLED

invalid Origin:
403 ORIGIN_DENIED

owner /docs:
404 NOT_FOUND

new run while parked:
0
```

Therefore the default ordinary-failure rollback remains:

`PARKED_FAIL_CLOSED`

Full teardown is still reserved for security-boundary failure.

## provider/request-contract blocker closure

The third release supplied the first real-provider proof after request-contract hardening.

Exact operation chain:

```text
PROVIDER ordinal 1:
DISPATCH_STARTED
→ OUTCOME_KNOWN / PROVIDER_COMPLETED

TOOL ordinal 2:
DISPATCH_STARTED
→ OUTCOME_KNOWN / TOOL_COMPLETED

PROVIDER ordinal 3:
SECURITY_ADMITTED
→ OUTCOME_KNOWN / CANCELLED
(no DISPATCH_STARTED)
```

Physical provider sends:

`1`

Provider retry/resend:

`0`

Tool operations:

`1`

This closes the prior provider request compatibility blocker in the actual hosted path.

The fixed Stockroom tool also executed successfully in the actual hosted path.

## third-release failure

The run was admitted exactly once and no second run was created.

Observed final facts:

```text
public projection:
ADMITTED / expired

execution attempt:
EXECUTION_FAILED

failure class:
RECOVERY_CONFLICT

worker log:
CLAIM_EXECUTION / PUBLIC_WORKER_FAILURE_UNCLASSIFIED

provider UNKNOWN:
NONE
```

The strongest source-level cause is a claim-renewal/dispatch-pin version race.

Current code facts independently verified by Browser:

1. `ActiveClaim.current()` returns `active.ref` without synchronization.
2. `_renew_claim()` independently replaces `active.ref` every 5 seconds.
3. exact-version DB consumers take a claim snapshot before an awaited DB transaction.
4. `start_dispatch_if_fresh()` passes that snapshot to `worker_pin_dispatch(... claim_version ...)`.
5. the DB pin requires the exact current claim version.
6. if renewal commits between snapshot and pin, the pin rejects the stale version and the whole dispatch transaction rolls back.
7. the observed claim advanced from version 1 to 2 while the next provider operation remained at `SECURITY_ADMITTED`, then recovery cancelled it.

This is a high-confidence defect hypothesis but must be deterministically reproduced before source repair is accepted.

Exact blocker:

`PUBLIC_WORKER_CLAIM_RENEWAL_DISPATCH_PIN_RACE`

## retained third-smoke settlement gap

The third smoke is not UNKNOWN and therefore migration 0025 correctly does not match it.

Final retained accounting:

```text
reservation:
HELD 200000 micro-USD

settled_cost:
NULL

slot:
OCCUPIED

outbox:
BOUND

money events:
RESERVE 1 / SETTLE 0

campaign:
available 14791200
held 200000
settled 8800
```

Claims/pins are closed after recovery, and the worker-work row is non-claimable due deadline expiry, but the public run remains unsettled.

The old `ReconciliationService.close()` computes cost from legacy `public_dispatch` rows. This P1-5 integrated execution did not use that legacy dispatch accounting path. A zero-cost close would therefore be incorrect because one real provider dispatch completed.

Exact blocker:

`P1_5_KNOWN_OUTCOME_FAILED_EXECUTION_SETTLEMENT_GAP`

## Browser judgment

```text
PARKED_FAIL_CLOSED:
ACCEPTED / CLOSED

provider request contract:
REAL-HOSTED PASS / CLOSED

fixed Stockroom tool path:
REAL-HOSTED PASS / CLOSED

third release:
FAILED / NOT_RELEASED

worker claim-renewal race:
REWORK REQUIRED

third smoke known-outcome settlement:
REWORK REQUIRED

Public Live:
NOT_RELEASED

next release authority:
NONE
```

## procedural note

The smoke client initially issued 10 GET reads without the required browser Origin and received expected 403 responses before correcting the header.

This did not create another run or provider send and is not the release blocker.

Future release smoke tooling must send the exact Origin from the first GET.

## next action

One combined repair/cleanup Task:

1. deterministically reproduce and fix the claim-renewal exact-version race;
2. add the narrow canonical P1-5 known-outcome failed-execution settlement bridge only if existing mediated authority cannot settle it correctly;
3. reconcile exactly the retained third smoke;
4. deploy the corrected worker;
5. leave backend topology PARKED and healthy;
6. reprove readiness without a provider call.

After Browser acceptance, request a NEW Human release decision.
