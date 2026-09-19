# Browser Command Center Judgment — Fourth Public Live Release Authority

## decision

```text
1501 REPAIR/SETTLEMENT:
ACCEPTED

PARKED_FAIL_CLOSED:
READY

Human decision:
RELEASE_PUBLIC_LIVE

fourth bounded release:
AUTHORIZED

public smoke:
EXACTLY ONE
```

## exact baseline

`b1cbb8a3c130f591b5563d4b87c109785e5adddb`

Migration head expected:

`20260919_0026`

## authority boundary

Authorized:
- reuse current PARKED Railway ingress topology;
- exact frontend release binding;
- control enablement LAST;
- exactly one public run;
- canonical provider/tool execution for that run only;
- canonical polling with exact browser Origin from the first GET.

Not authorized:
- private real-provider canary;
- second run;
- manual provider call;
- retry/resend outside accepted runtime semantics;
- alternate provider/model;
- fifth release attempt.

## failure policy

Ordinary execution-layer failure must rollback to `PARKED_FAIL_CLOSED`, not full teardown.

Full teardown is reserved for security-boundary failure.

If the one run reaches a state matching an already accepted mediated reconciliation:
- use 0025 for exact UNKNOWN pattern;
- use 0026 for exact known-outcome failed pattern;
- only after `public_control=false`;
- exact run identity must be re-proven;
- no second provider send caused by reconciliation.

## success result

```text
PUBLIC_LIVE_RELEASED
/
FOURTH_SINGLE_PUBLIC_SMOKE_PASS
/
BROWSER_REVIEW_REQUIRED
/
HUMAN_PUBLIC_SITE_SMOKE_PENDING
```
