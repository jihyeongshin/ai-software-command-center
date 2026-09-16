# P3-3 Public Live L4 Provider Profile V1

## status

```text
HUMAN_PROVIDED / ACCEPTED
version:
V1
accepted_at:
2026-09-16 KST
```

Human decision:

Use Luna with adaptive reasoning and an explicit four-call run ceiling.

This policy supersedes the prior L4 proposal that selected Terra and also explicitly supersedes the frozen L4 `<=2 total calls including retry` limit for this Public Live scenario only.

All other frozen Public Live monetary, deadline, security, provider-isolation and no-fallback boundaries remain unchanged unless explicitly amended below.

## provenance

Historical frozen design:

`209e7534f66e9b07ce9d33742e6993370a70f4fb`

Historical Human-decision package:

`.aiassistant/reports/aiscc/20260916_0930_aiscc-p3-3-public-live-l4-provider-profile-proposal-v1.md`

That 0930 proposal is NOT controlling policy.

This document is the controlling L4 provider-profile authority.

## exact provider/profile

```text
provider:
OpenAI

model:
gpt-5.6-luna

API family:
Responses API

service tier:
default / standard

provider/model fallback:
FORBIDDEN
```

Public/user input cannot choose provider, model, reasoning level, endpoint, credential, retry policy or tool profile.

## adaptive reasoning policy

### call role 1 — primary solution

```text
reasoning.effort:
low
```

Purpose:
- normal bounded scenario execution;
- expected happy path.

### call role 2 — conditional semantic verification

```text
reasoning.effort:
low
```

This call is NOT automatic.

It may occur only when deterministic/application validation indicates that model-level semantic verification is required.

### call role 3 — bounded correction

```text
reasoning.effort:
medium
```

This call is NOT automatic.

It may occur only when prior validation/verification identifies an exact correctable semantic defect.

Correction input must be bounded to the server-owned scenario context plus the exact defect/correction contract. It must not become a free-form public prompt.

### call role 4 — provider retry reserve

This is not a fourth independent semantic reasoning phase.

It is a single provider retry reserve for one logical call.

```text
retry count:
<=1 / run

reasoning.effort:
inherit the retried logical call's effort
```

Retry is allowed only after a provider/transport attempt is known conclusively not to have produced the side effect/outcome whose duplication would matter.

Unknown-outcome blind retry remains forbidden.

## exact call ceilings

```text
maximum substantive semantic calls / run:
3

maximum provider retries / run:
1

maximum provider requests total / run:
4
```

Normal happy path target:

`1 provider request`

The implementation must not intentionally consume all four calls merely because the ceiling exists.

## tool boundary

```text
allowed tool:
stockroom_summary

maximum tool dispatches / run:
1
```

No arbitrary function/tool selection.

## token envelope

Per provider request:

```text
billable input bound:
<=8000 tokens

max output tokens:
<=2000
```

Per run:

```text
aggregate visible/output envelope:
<=6000 tokens across substantive calls
```

Provider retry reuses the logical-call output ceiling; it does not expand the accepted semantic output budget.

Implementation must preserve the provider/API meaning that reasoning tokens are included in applicable output-token ceilings.

## timeout envelope

```text
connect timeout:
5 seconds

read timeout:
30 seconds

local hard provider-call wall:
35 seconds

frozen run deadline:
90 seconds
```

A new provider call may not start if its admitted worst-case local wall would violate the run deadline.

## price envelope

Current accepted planning rates for `gpt-5.6-luna`:

```text
standard input:
$0.20 / 1M tokens

standard output:
$1.20 / 1M tokens
```

For conservative planning, input may use the previously adopted 1.25x cache-write envelope when applicable.

Per-call conservative envelope:

```text
8000 * ($0.20/M * 1.25)
+
2000 * ($1.20/M)
=
$0.0044
```

Four-request absolute ceiling:

```text
$0.0176 / run
```

This is an application reservation calculation, not evidence that provider-side billing controls are configured.

Price/configuration facts expire after:

`24 hours`

before a real-provider verification/release action.

## frozen budgets retained unchanged

```text
application run reservation:
$0.20

application daily budget:
$4

application campaign budget:
$15

daily starts:
20

concurrent slots:
2

campaign cutoff:
2026-10-17T15:00:00Z
```

The lower Luna cost does NOT automatically increase daily starts, concurrency slots, campaign run count or any other frozen admission limit.

## provider account target

Dedicated API Project target:

```text
project hard spend limit:
$15/month

alerts:
$10
$12
```

These values are accepted target policy.

They are NOT proven configured account state until Human/account evidence confirms them.

## credential/account boundary

Required eventually:

- dedicated/non-secret API Project reference;
- scoped credential capability reference;
- actual model access;
- billing healthy;
- effective account/project RPM/TPM evidence;
- provider project hard-spend setting evidence when supported.

Raw API key/token must never be emitted into Task/Cycle/report/export/public provenance.

## paid-call boundary

This policy does NOT authorize a paid provider call.

Any real provider request requires a later Task that explicitly authorizes:

- exact provider profile/version;
- exact account/credential capability reference;
- exact request purpose;
- exact maximum provider spend;
- exact evidence to capture.

## release effect

Human acceptance authorizes non-paid profile binding implementation.

It does NOT itself complete L4.

L4 terminal acceptance still requires:

- implementation/binding proof;
- current official provider fact freshness;
- account/project/credential evidence where required by L4;
- later explicitly authorized provider verification if required by final release judgment;
- Browser Command Center acceptance;
- Git persistence.
