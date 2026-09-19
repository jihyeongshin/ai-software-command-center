# AISCC Browser Command Center Handoff — Final Public Live re-release authorized

## exact baseline

`ade1ccdfd6248e264dddbe98cf77371e9189a3d6`

## Human decision

`RELEASE_PUBLIC_LIVE`

## current state before release

```text
Public Live:
NOT_RELEASED

Public control:
DISABLED

public ingress domains:
0

worker public domains:
0

edge trust:
ABSENT

campaign held:
0

migration head:
20260919_0025

Replay:
PUBLIC / release-disabled

worker:
claim-sequence recovery accepted / healthy

provider:
OpenAI / gpt-5.6-luna / public-live-luna-v1
```

## execution boundary

Release only the already accepted Public Live system.

Order:
1. exact preflight;
2. public ingress while control disabled;
3. frontend exact API/CSP binding while control disabled;
4. enable control last;
5. exactly one public smoke run;
6. final security/release proof.

If smoke is UNKNOWN or materially fails:
- no retry/resend;
- no second run;
- disable control first;
- restore Replay-only frontend;
- remove edge trust/domain;
- preserve evidence;
- stop for Browser review.

A successful release still requires Browser review and Human public-site smoke before L8 closure.
