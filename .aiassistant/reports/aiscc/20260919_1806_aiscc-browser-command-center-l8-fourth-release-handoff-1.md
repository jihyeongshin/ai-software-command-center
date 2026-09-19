# AISCC Browser Command Center Handoff — Fourth Public Live Release

## baseline

`b1cbb8a3c130f591b5563d4b87c109785e5adddb`

## current release assets

Already accepted and PARKED:
- Railway public ingress domain;
- exact release origin;
- accepted edge-trust binding;
- healthy ingress;
- healthy repaired worker;
- worker-only provider secret.

Do not tear down/recreate these if unchanged.

## fixed blockers from earlier attempts

Closed:
- provider HTTP 400/request schema incompatibility;
- strict zero-argument tool schema;
- worker claim sequence;
- worker claim-renewal exact-version race;
- UNKNOWN 0025 reconciliation;
- known-outcome 0026 reconciliation;
- PARKED topology durability.

## fourth attempt

Sequence:

```text
PARKED reproof
→ frontend Live binding
→ control enable LAST
→ ONE POST
→ poll same run with Origin header from first GET
→ terminal proof
```

No separate canary.

## failure handling

Disable control first.

Then restore frontend Replay-only but keep backend PARKED.

Use 0025 or 0026 only if the exact new run satisfies the accepted predicate.

No fifth attempt in this Task.
