# AISCC P3-3 Readiness Blocker → Public Replay Implementation Handoff

## authoritative state

```text
HEAD:
17fcd337a8bc1410e230a7c18195ac3d3006b417

P3-3:
ACTIVE / BLOCKED_RELEASE_PREREQUISITE

Recorded Replay corpus:
CANONICAL / PERSISTED

Public Replay deployment:
NOT_COMPLETED

Public Bounded Live:
NOT_RELEASED

Competition submission:
NOT_COMPLETED
```

## accepted deployment direction

Do not reopen hosting selection.

```text
Recorded Replay public surface:
Cloudflare Pages

optional Live API / PostgreSQL:
Railway Hobby / Singapore

optional Live model/provider:
separate OpenAI API Project
```

Only the first item is in scope now.

## implementation strategy

Create a standalone static public Replay artifact that can later be uploaded/published to Cloudflare Pages.

Recommended repository shape fixed by this handoff:

```text
scripts/build_public_replay.py
public/replay/
  index.html
  404.html
  assets/
    app.js
    styles.css
  data/
    REPLAY_CORPUS_INDEX.json
    stockroom-s1-normal.json
    stockroom-s2-missing-evidence.json
    stockroom-s3-policy-conflict.json
    stockroom-s4-human-owned-claim.json
  _headers
  health.json
  PUBLIC_REPLAY_BUILD_MANIFEST.json
docs/AISCC_PUBLIC_REPLAY_DEPLOYMENT.md
```

The corpus copies must be byte-identical to the accepted canonical source files.

The static artifact is the deployable unit. Cloudflare Pages does not need owner DB/provider/secret access for Replay.

## Human QA after implementation

Before deployment, Human should locally inspect:

- landing clarity;
- all four scenario cards/details;
- Recorded-vs-Live labels;
- evidence/Judgment/Cycle/provenance readability;
- no active Live action;
- responsive desktop presentation;
- error/404 behavior.

Deployment is a separate later Task.
