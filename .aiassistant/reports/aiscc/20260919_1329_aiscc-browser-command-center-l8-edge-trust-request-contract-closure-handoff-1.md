# AISCC Browser Command Center Handoff — edge-trust cleanup + provider request contract hardening

## current Git baseline

`f3f8acd5af11c56de2dacba2777aa3e0e9b85cb7`

## closed work

```text
1145 retained UNKNOWN:
RECONCILED / CLOSED

1145 conservative liability:
4400 micro-USD

repeated UNKNOWN diagnostic gap:
CLOSED at durable classification level

provider calls during 1225:
0
```

## current public state

```text
Public control:
DISABLED

Public Live:
NOT_RELEASED

public ingress domains:
0

worker domains:
0

frontend:
Replay-only
```

## blocker 1

`INGRESS_EDGE_TRUST_ROLLBACK_RESIDUE`

Remove/detach only the ingress service's stale `AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST` binding and prove healthy startup with no public domain and no release origin.

## blocker 2

`REPEATED_PROVIDER_BAD_REQUEST_COMPATIBILITY_UNPROVED`

Both real release provider attempts produced durable evidence equivalent to HTTP 400 bad request.

Do not make a third provider call yet.

Audit the exact current Responses request against official API contract and canonicalize the zero-argument strict function schema.

Likely safe hardening target:

```json
{
  "type": "object",
  "properties": {},
  "required": [],
  "additionalProperties": false
}
```

Treat this as compatibility hardening, not as a proven historical root cause unless evidence supports that conclusion.

## next stage after success

Browser review → exact tool-bearing private canary decision → fresh readiness → NEW Human release decision → only then a third public release.
