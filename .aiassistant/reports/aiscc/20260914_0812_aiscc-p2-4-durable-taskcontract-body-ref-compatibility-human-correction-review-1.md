# AISCC P2-4 — Durable TaskContract body_ref compatibility correction

## 0. Browser Command Center judgment

0756 Executor result:

```text
BLOCKED / POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Executor behavior:

```text
ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED
```

Defect classification:

```text
Executor defect:
NO

existing product/runtime regression:
NO

Command Center accepted-design verification defect:
YES
```

0756 implementation candidate:

```text
NOT_CREATED
```

Governance Commit A is preserved. No canonical baseline, migration, product/test source, Result Commit B, private DB, provider/network, golden self-dogfood run, push or deployment occurred.

## 1. Exact incompatibility

Human-accepted `AISCC-TASKCONTRACT-DURABLE-BODY-V1` currently states:

```text
project_id, contract_id:
[A-Za-z0-9][A-Za-z0-9_.-]{0,95}

body_ref:
task-contract-body:v1:<project_id>:<contract_id>:v<n>

TaskConstraintRefV1.constraint_payload_ref:
body_ref
```

Current source-owned `TaskConstraintRefV1` constructor applies the existing `_ID` bound:

```text
constraint_payload_ref length <= 160
```

Observed exact probe:

```text
each ID length 67 -> body_ref length 160 -> PASS
each ID length 68 -> body_ref length 162 -> DENY
each ID length 96 -> body_ref length 218 -> DENY
```

Therefore the accepted proposal is internally incompatible with the current unchanged V1 constructor for otherwise valid body IDs.

## 2. Rejected correction options

Do NOT:

```text
widen the existing TaskConstraintRefV1/_ID limit
narrow project_id or contract_id from the accepted 96-character domain
bypass __post_init__
truncate either ID
use caller-chosen aliases
put extra fields into TaskConstraintRefV1
change unknown_fields=DENY
```

Those options either change existing V1 semantics or unnecessarily narrow the newly accepted body domain.

## 3. Preferred superseding correction

Supersede only the `body_ref` derivation in section 4 of the accepted proposal.

Old:

```text
body_ref = task-contract-body:v1:<project_id>:<contract_id>:v<n>
```

New:

```text
body_identity_bytes =
JCS({
  "project_id": project_id,
  "contract_id": contract_id,
  "contract_version": n
})

body_identity_sha256 =
SHA256(body_identity_bytes)

body_ref =
task-contract-body:v1:sha256:<body_identity_sha256>
```

Exact resulting `body_ref` length:

```text
93 ASCII characters
```

The digest is over contract-version identity only, not body content.

Content integrity remains independently bound by:

```text
constraint_payload_fingerprint = body_sha256
```

and the durable row continues to store:

```text
project_id
contract_id
contract_version
body_ref
body_sha256
canonical_body
```

## 4. Semantic effect

Preserved unchanged:

```text
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
TaskConstraintRefV1 schema
TaskConstraintRefV1 unknown_fields=DENY
existing _ID validator
project_id max length 96
contract_id max length 96
contract version semantics
body canonical bytes / body_sha256
append-only task_contract_bodies design
issuance idempotency
same-version conflicting-content denial
P1-4 / P1-6 / P1-7 / P1-8 ownership
```

The new `body_ref` is deterministic and stable for the exact `(project_id, contract_id, contract_version)` identity.

Because body content is not part of `body_ref`, retrying the same version with different bytes produces the same identity ref but a different `body_sha256`; existing issuance rules must reject that as conflicting content rather than treating it as a second version identity.

## 5. Required implementation negatives

The next implementation Task must prove:

```text
96-char project_id + 96-char contract_id -> valid 93-char body_ref
same identity + same body -> idempotent
same identity + different body_sha256 -> deny
different version -> different body_ref
project/contract identity change -> different body_ref
tampered ref digest -> deny
body_ref digest and persisted identity columns must recompute exact
TaskConstraintRefV1 existing constructor accepts the new ref without modification
```

## 6. Human decision requested

This is a narrow superseding correction to the already Human-accepted `AISCC-TASKCONTRACT-DURABLE-BODY-V1`.

Choose exactly one:

```text
ACCEPT
REWORK
REJECT
```

If `ACCEPT`, Browser Command Center will issue the corrected bounded implementation package. No additional IDE design Task is required.
