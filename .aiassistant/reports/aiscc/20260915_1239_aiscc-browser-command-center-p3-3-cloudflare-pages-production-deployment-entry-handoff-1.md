# AISCC P3-3 Public Replay Persistence Accepted → Cloudflare Pages Deployment Handoff

## authoritative repository state

```text
branch:
main

HEAD:
d13d261eb976fc839e78ba0878080bea93ad5201

workspace:
clean

public replay build:
HUMAN_ACCEPTED / PERSISTED
```

## deployable artifact

```text
directory:
public/replay

mode:
RECORDED_RUN_REPLAY

live:
false

canonical corpus root:
a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e

database:
none

provider inference:
none

Replay secrets:
none
```

Do not rebuild the artifact before deployment except running the existing `--check` verification.

## Cloudflare release path

```text
platform:
Cloudflare Pages

mode:
Direct Upload

requested project:
aiscc-replay

production branch:
main
```

Current Cloudflare documentation supports Direct Upload of a prebuilt static directory using Wrangler.

The project-mode limitation is accepted for the competition path: Direct Upload cannot later be converted to Git integration on the same Pages project.

## auth boundary

The Executor may perform read-only:

```text
npx wrangler whoami --json
npx wrangler pages project list --json
```

If not authenticated:

```text
STOP:
HUMAN_CLOUDFLARE_AUTH_REQUIRED
```

Do not invoke `wrangler login` automatically and do not read/output token values.

## after deploy

The Executor must derive the production URL from Cloudflare command/API output, never guess it.

Then verify over the public network:

- landing 200;
- health 200 / exact identity;
- index + four Replay JSON bytes;
- JS/CSS;
- unknown path true 404;
- effective static security headers;
- Recorded/Live wording;
- no redirect to owner/private service;
- no external provider/Live call.

Human final public-URL visual QA follows a successful Executor deployment/verification.
