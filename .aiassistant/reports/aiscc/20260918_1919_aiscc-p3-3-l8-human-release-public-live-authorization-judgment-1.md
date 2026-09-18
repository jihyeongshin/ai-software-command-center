# Browser Command Center Judgment

## decision

`HUMAN RELEASE DECISION ACCEPTED: RELEASE_PUBLIC_LIVE`

## meaning

The Human authorizes final activation of the already accepted bounded Public Live implementation.

This means the existing public Replay page may be changed from:

```text
Recorded Run Replay:
AVAILABLE

Bounded Live:
DISABLED
```

to:

```text
Recorded Run Replay:
AVAILABLE

Bounded Live:
ENABLED for stockroom-s1-normal / 1.0.0 only
```

## authorized release surface

- existing Railway Public Live services only;
- one Railway-generated HTTPS domain for `aiscc-public-live-ingress`;
- exact accepted Railway edge-trust variable;
- exact `public-live-v1` campaign/control activation;
- exact frontend `live-config.json` binding;
- exact CSP `connect-src` binding to the one ingress origin;
- Cloudflare Pages deployment of the accepted Replay + Live static artifact;
- one bounded end-to-end release smoke run;
- rollback actions when a release check fails.

## not authorized

- free-form tasks/repositories/prompts;
- more scenarios;
- new provider/model;
- new persistent paid service/resource;
- owner/private DB exposure;
- API/admin/cancel routes;
- broad CSP;
- project/shared OpenAI key;
- provider key on ingress/API/initializer;
- production hardening unrelated to release;
- destructive deletion of run/campaign evidence.

## state

Human authorization is admitted.

Actual Public Live state remains `NOT_RELEASED` until the successor activation Task proves completion.
