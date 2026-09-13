# AISCC Command Center Judgment

## meta

- created_at: `2026-09-14T08:46:19+09:00`
- reviewed_result_zip: `20260914_0756_aiscc-p2-4-taskcontract-durable-body-baseline-adoption-runtime-implementation-1.zip`
- reviewed_result_zip_sha256: `114a92aa27fab1e26524371516502cd7fb1cb8a8bf84869873001f1234a7357f`
- result_status: `BLOCKED / POLICY_CONFLICT_INVESTIGATION_REQUIRED`
- executor_disposition: `ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED`
- defect_owner: `BROWSER_COMMAND_CENTER`
- defect_class: `ACCEPTED_DESIGN_COMPATIBILITY_VALIDATION_MISSED`
- human_correction_result: `ACCEPT`
- next_task_authorized: `Yes`
- fresh_ide_chat_required: `No`

## judgment

0756 correctly stopped before source mutation.

The 0319 accepted proposal combined:

```text
project_id max 96
contract_id max 96
literal body_ref containing both IDs
constraint_payload_ref = body_ref
```

with an unchanged source-owned V1 `_ID` maximum of 160 characters.

That composition is invalid for part of the accepted ID domain.

Browser Command Center failed to catch this before Human approval and owns the defect.

Existing source/runtime is not classified as regressed.

## Human-approved correction

Canonical Human correction artifact:

```text
20260914_0812_aiscc-p2-4-durable-taskcontract-body-ref-compatibility-human-correction-review-1.md
SHA-256:
4c6905734e7a48b9688257574d86b1a7215627ac8514c7112747889c6bafa318
```

Human decision:

```text
ACCEPT
```

Therefore the accepted durable-body design is superseded only for `body_ref` derivation:

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

Exact length:

```text
93
```

Content integrity remains `body_sha256`; same identity/version with different content must be denied.

## preserved authority

No authorization is given to change:

```text
TaskConstraintRefV1
existing _ID validator
unknown_fields=DENY
96-char project/contract ID domain
P1-4/P1-6/P1-7 ownership
TaskContract owner
WorkRun owner
```

## authorization

Issue one corrected implementation retry combining:

```text
baseline adoption
migration
runtime
READY integration
isolated PostgreSQL durability proof
```

No actual golden self-dogfood execution, push or deployment.

Success is only an implementation candidate for Browser review.
