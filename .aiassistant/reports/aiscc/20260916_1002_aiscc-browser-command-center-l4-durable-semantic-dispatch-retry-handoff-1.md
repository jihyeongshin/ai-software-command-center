# AISCC Browser Command Center Handoff — L4 durable semantic dispatch compatibility retry

## repository

```text
HEAD:
e287117ba021411b82560df0af61901f7a8212bb
```

## accepted Human policy

Unchanged:

`.aiassistant/reports/aiscc/20260916_0950_aiscc-p3-3-public-live-l4-provider-profile-v1-accepted.md`

```text
OpenAI / gpt-5.6-luna

PRIMARY:
low

VERIFY:
low, conditional

CORRECT:
medium, conditional

semantic calls:
<=3

retry:
<=1 known-closed only

physical requests:
<=4
```

## blocker source

The current accepted `public_dispatch` model encodes a maximum two-request retry topology:

- ordinal 1 or 2 only;
- request 2 is retry-after-known-failure;
- successful request 1 cannot be followed by a semantic verifier through the same authority.

This is incompatible with the Human-approved profile.

## required semantic model

The implementation must durably distinguish:

```text
logical semantic phase:
PRIMARY | VERIFY | CORRECT

physical provider request:
unique request identity / physical ordinal <=4

retry:
optional retry_of physical request
same semantic phase
same reasoning effort
<=1 per run
known-closed only
```

Required call progression:

```text
PRIMARY attempt
→ durable outcome + deterministic validation

if verification_required:
    VERIFY attempt
    → durable outcome + validation

if exact_correctable_defect:
    CORRECT attempt
    → durable outcome + validation

known-closed failure:
    optional one retry of that same semantic role
```

Public input cannot trigger VERIFY/CORRECT/MEDIUM directly.

## compatibility boundary

Prefer a narrow additive relation/API if it preserves accepted `public_dispatch` meaning more cleanly than broad alteration.

If existing table/function extension is chosen, it must remain backward-compatible with existing rows and tests.

Do not rewrite accepted migrations.

## next turn

Compatibility substrate and profile binding should complete in the same Executor turn if evidence passes.

No paid provider request.
