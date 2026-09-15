# AISCC Browser Command Center Handoff — L3 shared-limit policy decision

## current canonical state

```text
HEAD:
968a7164cb50cfeaee5a6f83b7455ab87f6ccbd1

L1:
ACCEPTED / CLOSED

L2:
ACCEPTED / CLOSED

L3:
authority resolved
implementation blocked on Human-owned shared-limit policy

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## frozen historical authority

Design commit:

`209e7534f66e9b07ce9d33742e6993370a70f4fb`

Frozen L3:

`Public-only HTTP API composition`

Known exact read rule:

`30 authenticated GET reads / minute / run`

Known requirement:

`separate shared ingress flood control`

## unresolved policy

The historical design does not choose a complete flood limiter contract and does not fully specify the read-window boundary algorithm.

Do not send this back to Executor as another discovery Task.

A Human versioned decision is required.

## proposal status

The accompanying amendment proposal is:

`PROPOSED / NOT_ACCEPTED`

It is intentionally not an implementation Task and not a canonical policy until Human approves it.

After approval, issue a new timestamped rework Task that:

- records the accepted amendment as authority;
- authorizes narrow shared PostgreSQL limiter substrate if still needed;
- continues in the same turn to L3 HTTP composition and proof.
