# AISCC Browser Command Center Handoff — Human re-release authorized

## Human decision

`RELEASE_PUBLIC_LIVE`

## current baseline

`75ffc31ac20ff37fdd50bef9c9446fe0703cadfa`

## current state before release execution

```text
Replay:
PUBLIC / UNCHANGED

Public admission:
DISABLED

Public Live:
NOT_RELEASED

ingress public domains:
0

worker public domains:
0

migration head:
20260919_0024

retained 1919 liability:
CLOSED / 0

reconciler ACL:
ACCEPTED / CLOSED

provider secret:
worker-only / sealed / service-local

fixed Public tool:
accepted deterministic in-process stockroom_summary
```

## successor execution

Perform one bounded final re-release.

Order:
1. preflight;
2. expose only existing ingress while control disabled;
3. prove fail-closed public ingress;
4. bind exact frontend API origin/CSP and deploy;
5. enable control last;
6. execute exactly one bounded public smoke;
7. verify public/release/security state;
8. on material failure, rollback immediately to Replay-only.

Do not reintroduce the old Docker dependency for Public Live.

Do not create a second smoke run after an ambiguous/UNKNOWN outcome.
