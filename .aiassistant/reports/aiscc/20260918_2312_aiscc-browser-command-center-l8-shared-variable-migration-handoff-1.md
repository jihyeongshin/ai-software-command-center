# AISCC Browser Command Center Handoff — shared Railway variable migration

## current canonical baseline

`3832fff7751c387b8e559cc273cf30836238d48d`

## accepted lineage

- Public fixed in-process Stockroom implementation: ACCEPTED.
- affected L6 reproof: ACCEPTED.
- private worker Docker-free proof: ACCEPTED.
- 2237 ingress-local cleanup stop: ACCEPTED.
- current remaining blocker: Railway project/environment shared variable inheritance.

## effective inheritance to remove

Shared effective variables currently reach worker, ingress, initializer and API:

- `AISCC_OPENAI_API_KEY`
- `OPENAI_API_KEY`
- `AISCC_PUBLIC_LIVE_RAILWAY_EDGE_TRUST`

No values were read.

Worker separately has a sealed service-local `AISCC_OPENAI_API_KEY` binding.

## target

Remove the broad shared bindings while preserving the worker-local sealed key.

Do not create/copy/rotate provider material.

Keep ingress private and edge trust absent.

## after success

Expected sequence:

1. Browser accepts hosted L5 variable-isolation reproof;
2. separate Task settles retained 1919 run as definitely-not-sent;
3. fresh release readiness;
4. explicit re-release;
5. at most one bounded public smoke.
