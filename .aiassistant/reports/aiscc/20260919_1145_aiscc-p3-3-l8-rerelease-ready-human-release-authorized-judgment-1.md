# Browser Command Center Judgment

## readiness judgment

```text
ACCEPTED
/
RERELEASE_READY_CANDIDATE
/
HUMAN_RELEASE_DECISION_RECEIVED
/
RELEASE_PUBLIC_LIVE
```

## exact baseline

`ade1ccdfd6248e264dddbe98cf77371e9189a3d6`

## accepted prerequisites

- UNKNOWN lifecycle reconciliation: CLOSED
- 0125 retained liability: RECONCILED
- worker claim-sequence regression: CLOSED
- canonical persistence suite: RESTORED
- hosted fail-closed state: ACCEPTED
- migration head: 0025
- held liability: 0
- Public Live: NOT_RELEASED
- Replay: AVAILABLE / release-disabled

## Human authority

The Human has now provided a NEW explicit decision:

`RELEASE_PUBLIC_LIVE`

It applies only to the successor bounded release Task.

## release acceptance boundary

Executor success is only a release candidate.

Executor must not mark L8 closed.

After a successful single public smoke:
- preserve the released service;
- export evidence;
- return `BROWSER_REVIEW_REQUIRED / HUMAN_PUBLIC_SITE_SMOKE_PENDING`.

After UNKNOWN or any material failure:
- no resend;
- no second run;
- rollback to Replay-only;
- preserve evidence;
- return Browser review.

If an UNKNOWN run leaves conservative liability to reconcile, do not silently invoke 0025 reconciliation unless this Task explicitly authorizes it. This Task does not.
