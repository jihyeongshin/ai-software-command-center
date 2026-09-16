# AISCC Browser Command Center Handoff — retention closed → L4 provider entry

## canonical repository

```text
branch:
main

HEAD:
e287117ba021411b82560df0af61901f7a8212bb
```

## closed lineage

```text
L1:
ACCEPTED / CLOSED

L2:
ACCEPTED / CLOSED

L3:
ACCEPTED / CLOSED

limiter retention/resource bound:
ACCEPTED / RESOLVED
```

Inherited current regression:

`1383 PASS / 3 existing SKIP / 0 FAIL / 0 ERROR`

## DAG

```text
L4:
SELECTED / ENTRY_AUTHORIZED

L5:
ENTRY_ELIGIBLE

L6:
BLOCKED_ON_L4_L5
```

## historical authority anchor

`209e7534f66e9b07ce9d33742e6993370a70f4fb`

The next Executor must read historical:

- `AISCC_PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
- `AISCC_PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md`
- `AISCC_PUBLIC_LIVE_HUMAN_DECISIONS.md`
- `AISCC_PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
- other L4-referenced frozen files

directly as `209e7534:<path>`.

Do not require them to exist at current HEAD.

## current OpenAI public fact seed

Browser Command Center current verification on 2026-09-16 found official OpenAI API documentation advertising GPT-5.6 Sol, Terra and Luna through the Responses API.

Current public standard token rates observed:

```text
GPT-5.6 Sol:
$4 / 1M input
$20 / 1M output

GPT-5.6 Terra:
$2 / 1M input
$12 / 1M output

GPT-5.6 Luna:
$0.20 / 1M input
$1.20 / 1M output
```

These are current external facts, not frozen design authority and not a Human provider-profile choice.

Executor should reverify official sources if it has authorized network access and record observation time/source.

## Human-owned likely fields

Do not silently choose:

- exact model/model ID;
- reasoning effort;
- max input/output tokens;
- calls/run;
- retry count;
- provider timeout;
- run/day/global caps;
- USD daily/global/provider hard limit;
- real API Project/key/credential reference;
- billing/spend guard configuration.

If the exact frozen L4 contract requires any such unfixed value, produce a concrete proposal and stop at `HUMAN_PROVIDER_POLICY_DECISION_REQUIRED`.

## prohibited in this entry

- real paid provider call;
- raw API key/credential reading/export;
- provider billing/spend mutation;
- L5 Railway/deployment;
- Public admission enablement;
- Git commit/push/deploy.
