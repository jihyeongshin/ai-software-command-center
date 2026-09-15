# AISCC Browser Command Center Handoff — shared limiter prerequisite → L3 retry

## current repository

```text
branch:
main

HEAD:
968a7164cb50cfeaee5a6f83b7455ab87f6ccbd1
```

## accepted lineage

```text
frozen Public Live design:
209e7534f66e9b07ce9d33742e6993370a70f4fb

L1:
ACCEPTED / CLOSED

L2:
ACCEPTED / CLOSED

L3:
authority resolved
implementation blocked before mutation
```

## actual L3 stage

The predecessor resolved:

```text
Public-only HTTP API composition
```

Its dependency on L2 is satisfied.

The current blocker is not L3 authority ambiguity.

## actual blocker

Frozen L3 requires shared rate limiting including:

```text
per-run public read:
30 requests / minute

separate flood limiting:
required
```

Current throttle behavior is process-memory scoped.

Current accepted Public Live persistence/API does not expose a shared limiter primitive satisfying the frozen L3 exit criteria.

Therefore process-local throttle evidence is insufficient.

## retry shape

The next Executor turn combines prerequisite repair and L3:

1. re-read the exact frozen L3 HTTP/security/matrix authority;
2. extract the exact shared read/flood semantics;
3. audit existing current shared-limit primitives narrowly;
4. if none qualify, add a narrow additive PostgreSQL shared limiter migration/API;
5. prove cross-instance/concurrent shared behavior and least privilege;
6. continue immediately into L3 HTTP composition;
7. run frozen L3 HTTP/security evidence and regression.

## important non-goals

- do not weaken or reopen accepted L2 admission/budget semantics;
- do not use in-memory limiter as the sole shared authority;
- do not implement L4 provider profile;
- do not implement L5 Railway/deployment;
- do not enable Public admission;
- do not call a real paid provider;
- do not commit/push/deploy.

## PostgreSQL lifecycle

If DB work is required:

```text
postgres:17.6
local cache only
network pull forbidden
task-owned container/volume
127.0.0.1:55432
private DB reuse forbidden
```

Do not assume a predecessor runtime exists.
