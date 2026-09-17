# AISCC Browser Command Center Judgment

## judgment

```text
Railway account/project:
PASS

production environment:
PASS

PostgreSQL:
PASS / ONLINE

PostgreSQL region:
PASS / SINGAPORE

backend service identity:
PASS

backend region:
PASS / SINGAPORE

backend runtime:
OFFLINE / EXPECTED_PRE_SOURCE

L5 terminal:
OPEN

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## next prerequisite

Do not connect Railway to GitHub yet.

The exact accepted source commit is local:

`96a4029ec3a82c9b2a88b9718732aa0f00ecad20`

and has not yet been proven present on the GitHub remote.

Publish only that existing commit first.

## push constraints

Allowed:

- inspect current branch/upstream/origin;
- perform remote read/fetch needed for ancestry verification;
- one ordinary fast-forward push of exact HEAD to the existing matching GitHub upstream branch;
- verify remote branch SHA after push.

Forbidden:

- source/config/test mutation;
- new commit/amend;
- force push;
- branch creation unless the Task's strict conditions already prove the existing upstream identity;
- tags/releases;
- Git config mutation;
- Railway/Cloudflare mutation;
- credential disclosure;
- OpenAI/provider calls.

If remote identity, upstream, default branch, or ancestry is ambiguous: STOP.
