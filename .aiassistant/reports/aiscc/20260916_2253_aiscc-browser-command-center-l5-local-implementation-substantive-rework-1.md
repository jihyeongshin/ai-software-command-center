# AISCC Browser Command Center Judgment

## judgment

```text
2148 local implementation:
REWORK_REQUIRED

replacement Browser-review ZIP:
6f38fec7898cce3016ea508d4df902490dd9d95e9d2df2c985640447d5eb2a1f

transport/export contract:
PASS

source bytes reviewed:
12/12

accepted design:
UNCHANGED / CLOSED

Public admission:
DISABLED

Public Live:
NOT_RELEASED

real provider calls:
0

L5:
OPEN
```

## accepted portions to preserve

Do not rewrite working boundaries unnecessarily:

1. dedicated ingress module;
2. owner-route structural exclusion;
3. fail-closed Railway edge identity authority;
4. `proxy_headers=False`;
5. distinct Live DB variable;
6. ingress provider-secret denial;
7. owner DB denial;
8. Replay zero-execution boundary.

## required rework

1. make the private worker a real separately startable durable worker using existing server-owned work/supervisor/dispatcher owners and `HostedOpenAISecretResolver`;
2. make `aiscc hosted-l5-proof` execute the accepted proof path instead of printing a static expectation;
3. separate production hosted OpenAI transport from fake/loopback QA transport;
4. remove proof retry-semantic contradiction;
5. tighten CORS OPTIONS to exact method/path pairing.

No accepted P1/P3 authority may be weakened to make these pass.
