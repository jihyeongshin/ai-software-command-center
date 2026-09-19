# AISCC Browser Command Center Handoff — Canonical Public Build EOL Rework

## current baseline

`3178179986975709f4acec11825fc736cd3ce7c1`

Implementation commit:

`f9bb6a5a9de35a8abd6d5b39acb17af4b6add80b`

## preserve

Do not rework the trace projection itself.

Preserve:
- migration 0028;
- safe DB function;
- ingress projection integration;
- app.js trace validator/renderer;
- styles;
- released Public Live state.

## exact problem

The builder hashes authored assets using working-tree raw bytes.

On the Windows Executor checkout, `_headers` and `live-config.json` were CRLF.

Git canonical blobs are LF.

Thus committed `PUBLIC_REPLAY_BUILD_MANIFEST.json` describes local bytes, not canonical repository bytes.

## repair direction

Prefer repository-enforced LF for the public Replay authored text surface.

A narrow `.gitattributes` addition is authorized if required.

At minimum ensure these are LF:

```text
public/replay/_headers
public/replay/live-config.json
public/replay/*.html
public/replay/assets/*.js
public/replay/assets/*.css
public/replay/*.json
```

A broader `public/replay/** text eol=lf` rule is acceptable if it does not incorrectly classify binary files. If future binary assets exist or are possible, use explicit text patterns instead.

After applying the policy:
- rewrite current working-tree target files to LF;
- regenerate manifest;
- prove clean checkout reproducibility;
- keep Live enabled.

## Human QA

Still pending.

Do not create a new Live run in this rework.

Browser will issue Human trace QA only after accepting this canonical build fix.
