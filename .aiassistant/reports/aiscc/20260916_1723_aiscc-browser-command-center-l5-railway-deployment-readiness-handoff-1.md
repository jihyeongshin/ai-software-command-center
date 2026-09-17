# AISCC Handoff — Railway source staged, deployment-readiness audit required

## exact source

`96a4029ec3a82c9b2a88b9718732aa0f00ecad20`

GitHub:

```text
repository:
jihyeongshin/ai-software-command-center

branch:
main

remote main:
96a4029ec3a82c9b2a88b9718732aa0f00ecad20
```

## Railway current state

```text
Project:
AISCC

Environment:
production

Postgres:
Online / Singapore

aiscc-public-live-api:
Singapore / 1 replica / currently Offline

Source:
repo + main selected but staged only

Start Command:
unset

Healthcheck:
unset
```

## hold boundary

Do not click `Deploy Changes` yet.

The IDE Task must first derive and, only if necessary, implement the smallest deployment-facing entrypoint/readiness contract.

The eventual hosted deployment must be able to start without `AISCC_OPENAI_API_KEY`; missing key must keep provider execution fail-closed rather than crashing the whole API process.
