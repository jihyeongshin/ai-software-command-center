# AISCC Handoff — L5 local implementation substantive rework

## current accepted state

```text
base HEAD:
96a4029ec3a82c9b2a88b9718732aa0f00ecad20

reviewed candidate ZIP:
6f38fec7898cce3016ea508d4df902490dd9d95e9d2df2c985640447d5eb2a1f

design:
HOSTED_PUBLIC_LIVE_BINDING_DESIGN
ACCEPTED / CLOSED

candidate:
REWORK_REQUIRED

Public admission:
DISABLED

Public Live:
NOT_RELEASED

provider calls:
0
```

## preserve

The ingress/identity/DB/Replay structural work is broadly accepted and should remain stable unless a direct dependency requires a narrow correction.

## fix only

- durable private worker execution composition;
- real operator-only hosted proof driver;
- strict hosted provider destination/profile boundary;
- proof retry semantic consistency;
- exact CORS preflight method/path pairing.

After rework, export all changed source/test files under project-relative paths in the same result ZIP.
