# AISCC Handoff — Start authority accepted → local implementation resume

## accepted authorities

```text
P1_5_PUBLIC_LIVE_SEMANTIC_LIFECYCLE_V1:
ACCEPTED / CLOSED

PUBLIC_LIVE_DURABLE_WORKER_AUTHORITY_V1:
ACCEPTED / CLOSED

PUBLIC_LIVE_START_AUTHORITY_V1 / TOPOLOGY_D:
ACCEPTED / CLOSED
```

## resume point

Resume the blocked 0032 local implementation.

Do not reset the current candidate worktree.

Preserve and retest the two partial edits made before the blocker.

## expanded local scope

Implementation may now include:

- lifecycle migration 0018;
- worker claim migration 0019;
- start-authority migration 0020;
- private initializer runtime;
- start manifest;
- narrow initializer role/grants;
- durable start queue/journal/lease;
- P1-3/P1-4/P1-5 start composition;
- immutable execution binding;
- ordinary worker visibility gate;
- real durable worker;
- executable hosted-l5-proof;
- strict hosted adapter;
- exact CORS.

## still forbidden

No Railway, OpenAI real call/key use, Cloudflare, Git persistence, Public enablement, or release.
