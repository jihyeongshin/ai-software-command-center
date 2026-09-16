# P3-3 Public Live L4 OpenAI Account Evidence — Human Accepted

## status

```text
HUMAN_PROVIDED / ACCEPTED
date:
2026-09-16 KST
```

This record contains only non-secret account/project configuration evidence.

No API key secret, bearer token, payment-card data or service-account secret is stored here.

## dedicated API Project

```text
Project display name:
AISCC

non-default dedicated project:
PASS

Project default service tier:
Standard
```

## provider/model availability

```text
provider:
OpenAI

model:
gpt-5.6-luna

allowed in project:
PASS

effective current project rate limits:
500,000 TPM
500 RPM

rate-limit source:
inherited/shared Organization Tier 1
```

No project override is required for the accepted bounded demo.

## billing readiness

```text
billing:
Pay as you go

initial API credit balance after activation:
USD 5.00

auto-reload:
OFF

organization usage tier:
Tier 1

blocking billing warning:
NONE observed
```

## project spend guard

```text
monthly project spend limit:
USD 15.00

hard enforcement:
ON

current observed spend:
USD 0.00
```

Provider hard-limit enforcement is defense-in-depth only.

AISCC application budgets remain primary authority:

```text
run reservation:
USD 0.20

daily:
USD 4

campaign:
USD 15

daily starts:
20

concurrency:
2
```

## spend alerts

```text
66.666%:
USD 10.00

80%:
USD 12.00

100%:
USD 15.00
```

## runtime service account

```text
service account:
aiscc-public-live-runtime

project:
AISCC

project scoped:
PASS

organization owner:
NO

runtime dedicated:
PASS

API key status:
Active

last used at Human Gate:
Never

permission mode:
Restricted
```

Exact allowed API permission:

```text
Responses (/v1/responses):
Write
```

Observed non-required model capabilities remained:

```text
Text-to-speech:
None

Realtime:
None

Chat completions:
None

Embeddings:
None

Images:
None

Moderations:
None
```

The actual key secret was saved by the Human in a safe secret/password store and was not submitted to Browser Command Center.

A masked key representation or tracking/user identifier is not secret authority and is not persisted here.

## paid-call boundary

```text
real OpenAI Responses calls during Human account gate:
0
```

No paid provider verification occurred.

## Human Gate conclusion

```text
Operation 1 dedicated Project:
PASS

Operation 2 Luna access / current rate limits:
PASS

Operation 3 hard spend:
PASS

Operation 4 alerts:
PASS

Operation 5 billing readiness:
PASS

Operation 6 credential isolation:
PASS

Operation 7 paid calls:
0
```

Account/provider prerequisite evidence required by L4 is satisfied.

The key's deployment injection/use belongs to L5 hosted release configuration and does not require exposing its value to repository governance.
