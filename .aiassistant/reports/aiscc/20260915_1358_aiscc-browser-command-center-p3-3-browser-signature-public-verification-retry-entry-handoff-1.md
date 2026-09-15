# AISCC P3-3 Cloudflare 1010 → Browser-Compatible Verification Retry Handoff

## production origin

`https://aiscc-replay.pages.dev`

## source authority

```text
HEAD:
d13d261eb976fc839e78ba0878080bea93ad5201

corpus root:
a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e

deployment:
Human Dashboard Direct Upload

public status:
DEPLOYED_UNVERIFIED
```

## predecessor observation

```text
client:
Python urllib default User-Agent

all 11 requests:
HTTP 403

body:
error code: 1010
```

The application itself was not reached.

## retry strategy

Probe only `/` with two predefined anonymous browser-compatible request profiles.

Use the first profile that receives normal application content.

Then perform the exact byte/header/404 verification using that one profile consistently.

Do not retry with arbitrary rotating fingerprints.

Do not disable Cloudflare Browser Integrity Check in this Task.

## if both profiles fail 1010

Stop and return:

`PUBLIC_BROWSER_INTEGRITY_POLICY_BLOCK`

At that point Human should first confirm the production URL in a real browser and then decide whether any Cloudflare policy/configuration action is appropriate.
