# AISCC Browser Command Center Judgment

## judgment

```text
2253 Executor result:
DURABLE_WORKER_COMPOSITION_DESIGN_REQUIRED

Browser judgment:
ACCEPTED MANDATORY STOP

executor fault:
NO

source mutation this turn:
0

accepted binding design:
UNCHANGED / CLOSED

Human D8:
A / UNCHANGED

L5:
OPEN

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## why the stop is correct

A worker that merely accepts a caller-supplied run ID is not a separately startable durable worker.

A production worker must have a server-owned authority chain for:

```text
discover candidate work
→ atomically claim/lease it
→ bind worker generation/fencing identity
→ revalidate current run/state/version
→ authorize exact provider dispatch
→ consume secret lease
→ dispatch
→ durably record known/unknown outcome
→ release/recover/quarantine claim
```

The repository currently has the latter run-specific authorities, but the submitted audit found no accepted owner for the first discovery/claim step.

Inventing raw `public_outbox` polling, an environment-selected run ID, or a local in-memory queue would create new execution authority outside the accepted mediated boundary.

## design requirement

The next design must decide exact:

- discoverable work state;
- atomic claim semantics;
- worker identity;
- lease duration/renewal;
- fencing token;
- concurrency and duplicate-worker handling;
- stale/expired claim recovery;
- terminal/unknown/quarantined work exclusion;
- dispatch freshness revalidation;
- interaction with existing retry/unknown-outcome authority;
- durable provenance;
- shutdown/restart behavior;
- migration requirement;
- proof hooks needed by hosted-l5-proof.

No provider or workflow semantic may be silently changed.
