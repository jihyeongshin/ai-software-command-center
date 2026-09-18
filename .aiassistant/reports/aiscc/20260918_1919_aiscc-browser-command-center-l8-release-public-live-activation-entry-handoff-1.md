# AISCC Browser Command Center Handoff — Human RELEASE_PUBLIC_LIVE / activation entry

## current baseline

- GitHub main: `0e9feab441352816d284d095f8c3a6863b8aa6a5`
- L3-L7: ACCEPTED / CLOSED
- L8: HUMAN RELEASE AUTHORIZED / ACTIVATION PENDING
- Replay URL: `https://aiscc-replay.pages.dev/`
- Public admission: DISABLED
- Public Live: NOT_RELEASED
- campaign: ABSENT_PREACTIVATION
- ingress public domain: absent
- edge trust: absent
- frontend Live config: disabled
- provider key: worker only / sealed
- real Luna canary: ACCEPTED

## target public behavior

After successful activation:

- the existing Recorded Run Replay remains usable;
- Bounded Live is visibly enabled on the same site;
- only `stockroom-s1-normal / 1.0.0` can start;
- the browser POSTs to one exact Railway ingress origin;
- read capability remains same-tab `sessionStorage`;
- a public run executes through initializer -> worker -> real Luna provider;
- provider success is not relabeled as Human acceptance;
- accepted budget/rate/campaign controls remain active.

## safety ordering

Prefer fail-closed sequencing:

1. verify safe preflight;
2. create/configure ingress public origin while admission remains disabled;
3. verify disabled public ingress;
4. materialize exact campaign while control remains disabled;
5. prepare/deploy exact frontend origin+CSP binding;
6. enable `public_control` only as the final backend activation step;
7. perform one bounded public smoke;
8. on any material failure, disable control first and restore Replay-only frontend.

Do not delete durable release evidence during rollback.
