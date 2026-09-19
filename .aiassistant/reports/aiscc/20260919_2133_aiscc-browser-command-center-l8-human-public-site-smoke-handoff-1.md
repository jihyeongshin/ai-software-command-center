# AISCC Browser Command Center Handoff — Human Public-Site Smoke

## current state

```text
Public Live:
RELEASED

Browser runtime judgment:
ACCEPTED

Human browser QA:
PENDING

L8:
PENDING HUMAN QA
```

## public URL

`https://aiscc-replay.pages.dev/`

## important operational rule

Do not disable control or rollback the frontend while Human QA is pending.

The current released topology is the evidence target.

## Human QA boundary

This is not an IDE Executor task.

Human should:
1. open the QA Task;
2. perform the listed public-site operations;
3. create exactly one Human Live run by clicking the button once;
4. submit PASS/FAIL results to Browser Command Center.

Do not use Retry or create a second Live run if anything fails.

Do not expose/copy read capability, idempotency key, cookies, or network secrets.

After Human QA PASS, Browser performs terminal L8 closure.
