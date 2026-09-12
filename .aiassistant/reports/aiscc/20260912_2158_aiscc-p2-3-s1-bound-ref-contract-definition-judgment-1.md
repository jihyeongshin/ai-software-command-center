# AISCC Command Center Judgment

## meta

- judgment_id: `20260912_2158_aiscc-p2-3-s1-bound-ref-contract-definition-judgment-1`
- created_at: `2026-09-12T21:58:22+09:00`
- project: `AI Software Command Center (AISCC)`
- reviewed_task: `20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-source-rework-1`
- reviewed_result_zip_sha256: `334c6f87217be392b9633e5ab581e87b9ad12f4444627a78a29ee26a94ecca30`
- result_status: `HOLD_REWORK_REQUIRED / BOUND_REF_CONTRACT_DEFINED`
- reject_cause: `EXECUTION_BOUND_REF_SEMANTIC_ENCODING_MISSING`
- cycle_record_action: `create`
- execution_mode: `MANUAL_COMMAND_CENTER`
- source_mirror_sync: `not-required`

# Browser judgment

2125 Executor의 `BOUND_REF_ENCODING_UNDEFINED` STOP을 정당하게 입장한다.

Verified result:

```text
ZIP:
16 members / one top-level / CRC PASS

manifest:
15 / 15 exact

TASK/Cycle/Judgment:
byte exact

contract:
21 PASS / 22 BLOCKED_REQUIRED_EVIDENCE

source mutation:
none

tests:
not run

runtime/private:
not accessed
```

Static source evidence establishes:

```text
GuardFact.bound_refs storage:
LOSSLESS / existing JSONB path

fingerprint:
includes bound_refs

historical reconstruction:
preserves bound_refs

model/schema/migration expansion:
not currently required

missing item:
canonical semantic encoding for exact execution submission + attempt binding
```

# Command Center canonical bound-ref contract

This Judgment defines V1 canonical encoding for `G_EXECUTOR_SUBMISSION`.

Exactly two bound-ref strings, in this exact order:

```text
1. aiscc-bound-ref:v1:execution-submission:<BASE64URL_NOPAD_UTF8(submission_id)>
2. aiscc-bound-ref:v1:execution-attempt:<BASE64URL_NOPAD_UTF8(execution_attempt_id)>
```

`BASE64URL_NOPAD_UTF8(x)` means:

```text
x must be a non-empty Python/Unicode string
encode x as strict UTF-8 bytes
RFC 4648 URL-safe Base64 alphabet
strip all trailing "=" padding
payload must be non-empty
decoder restores only mathematically required "=" padding
decoder rejects non-base64url characters
decoded bytes must be strict UTF-8
decoded identifier must be non-empty
decode → re-encode must reproduce the exact original payload
no Unicode normalization or case folding
```

Cardinality/type rules:

```text
tuple length:
exactly 2

position 0:
execution-submission only

position 1:
execution-attempt only

extra refs:
forbidden

duplicate type:
forbidden

empty identifier:
forbidden

non-canonical encoding:
forbidden

malformed encoding:
forbidden
```

Authority rule:

```text
the encoded identifiers must be derived only from an issuer-verified ExecutionSubmissionRef;
caller strings do not become trusted by encoding them.
```

The encoding creates durable producer linkage only.
It does not create EvidenceCandidate, AdmittedEvidence, G_EVIDENCE or current WorkflowState authority.

# session/runtime correction

Continue the existing 2125 IDE Executor chat.
Do not open a new chat.

Python executable is fixed:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Do not use `python`, `py`, WindowsApps aliases or PATH discovery.
