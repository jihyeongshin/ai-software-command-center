# Browser Command Center Judgment — Fifth Public Live Release Authority

## decision

```text
2027 SUCCESS CLOSURE:
ACCEPTED

PARKED_FAIL_CLOSED:
READY

Human decision:
RELEASE_PUBLIC_LIVE

fifth bounded release:
AUTHORIZED

public smoke:
EXACTLY ONE
```

## baseline

`ec2e4895b5f4d26d987a627dfb40a5b9f1451970`

Expected migration head:

`20260919_0027`

## success boundary

The fifth smoke must prove the complete hosted chain:

```text
Public ingress
→ admission
→ worker
→ provider
→ optional fixed tool
→ provider/semantic completion
→ EXECUTOR_COMPLETED
→ claim release
→ automatic success finalizer
→ public_run COMPLETED
→ SETTLED / FREE / CLOSED
```

No operator or reconciler manual success call may be required for the smoke to count as PASS.

## authority

Authorized:
- reuse current PARKED backend topology;
- exact frontend release binding;
- control enablement LAST;
- exactly one public run;
- canonical provider/tool runtime for that one run;
- exact polling from the first GET;
- normal automatic 0027 success finalization.

Not authorized:
- private provider canary;
- second run;
- manual provider send;
- blind retry/resend;
- alternate provider/model;
- sixth release attempt.

## failure

Disable control first.

Restore frontend Replay-only.

Keep backend PARKED unless a security-boundary failure is proven.

Accepted 0025/0026/0027 functions may be used after disablement only to clean the exact retained fifth run matching their predicates.

## success result

```text
PUBLIC_LIVE_RELEASED
/
FIFTH_SINGLE_PUBLIC_SMOKE_PASS
/
AUTO_SUCCESS_FINALIZATION_PASS
/
BROWSER_REVIEW_REQUIRED
/
HUMAN_PUBLIC_SITE_SMOKE_PENDING
```
