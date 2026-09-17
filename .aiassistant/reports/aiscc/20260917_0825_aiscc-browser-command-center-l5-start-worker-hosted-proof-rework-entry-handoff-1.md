# AISCC Handoff — 0217 local candidate substantive rework

## current state

```text
HEAD:
96a4029ec3a82c9b2a88b9718732aa0f00ecad20

reviewed result ZIP:
35479a09be4edc0f946e06cc163420eb777dfcd5fd1cc506cff647e4afbca24b

candidate:
REWORK_REQUIRED

accepted P1-5 lifecycle design:
CLOSED

accepted durable-worker authority:
CLOSED

accepted start-authority topology:
CLOSED

Public admission:
DISABLED

Public Live:
NOT_RELEASED

L5:
OPEN
```

## preserve

Preserve working portions unless a direct dependency requires a narrow change:

- migrations 0018/0019/0020 additive ordering;
- initializer topology D;
- P1 owner separation;
- strict hosted endpoint boundary;
- exact CORS route/method pairing;
- dedicated claim persistence;
- Public/owner/Replay separation.

## fix

- real production worker executor composition;
- claim renewal + dispatch pin/fence integration;
- executable provider-double/sandbox hosted proof;
- actual initializer login-role runtime privilege path;
- current-time/current-gate start freshness;
- POSIX ZIP archive paths.

## next

Run focused PostgreSQL/runtime proof and full regression after the fixes, then submit all cumulative changed bytes for Browser source review.
