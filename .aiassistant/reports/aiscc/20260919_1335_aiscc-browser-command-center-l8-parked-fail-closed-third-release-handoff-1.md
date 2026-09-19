# AISCC Browser Command Center Handoff — PARKED_FAIL_CLOSED + third release

## current baseline

`684de919fd62ef9ecc04bceec8548ee9834458b0`

Request-contract hardening:

`9ddbc6da753d5af1d8e14354f608d101dff2b2e0`

## accepted provider request shape

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

The fixed tool remains:
- one tool only;
- strict true;
- zero user arguments;
- PROCESS 0;
- FILESYSTEM 0;
- NETWORK 0;
- SECRET 0.

## current safe state

```text
Public control:
DISABLED

Public Live:
NOT_RELEASED

public ingress domains:
0

current Railway edge/origin metadata:
ABSENT

Replay:
PUBLIC / Live disabled

provider calls since 1145:
0
```

## important ingress finding

No-origin current-source ingress is not a valid healthy composition.

Do not add an originless disabled composition just to preserve the old teardown model.

Instead reconstruct the real ingress topology while `public_control=false`, prove it fail-closed, and keep it as `PARKED_FAIL_CLOSED`.

## parked backend topology

Keep across ordinary execution-layer failures:
- Railway public ingress domain;
- exact release origin;
- exact edge-trust proof;
- healthy ingress service;
- worker;
- worker-only provider secret.

Safety switch:
- `public_control.enabled=false`.

Frontend may remain Replay-only while parked.

## third release

After parked proof, perform the actual public release in the same Task and exactly one public smoke.

No separate real-provider canary.

On UNKNOWN:
- disable control first;
- no resend/second run;
- frontend back to Replay-only;
- keep backend topology parked;
- reconcile only the exact new UNKNOWN smoke through accepted 0025 authority;
- stop for Browser review.
