# AISCC Cycle Record

## meta

- cycle_id: `20260831_0103_aiscc-p1-6-durable-content-runtime-writer-and-read-capability-authority-hold-1`
- date: `2026-08-31T01:03:00+09:00`
- phase: `P1-6 Durable Evidence Content Authority Extension Runtime`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_6_EVIDENCE_CONTENT`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `DURABLE_CONTENT_WRITE_AND_HISTORICAL_READ_CAPABILITY_SELF_MINTABLE`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260831_0103_aiscc-p1-6-durable-content-runtime-writer-and-read-capability-authority-hold-1.cycle.md`

## reviewed candidate

```text
start HEAD:
b111f5f676e1a782de095e2f5b2a106d8b9a0207

Stage 0A:
32e88234ad7a7cbaa545e12f8c7e03b5897202cb

Stage 0B / final HEAD:
bc446d9530e28f9b10602c9f1dd5232a97221a10

accepted extension design SHA:
ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411

runtime paths:
13

runtime aggregate:
8119fcb3ea10b3fb86e986b21ca0cd638e14b9021ac903fa007d750124392962

full repository:
194 PASS

P1-4 PostgreSQL:
18 PASS

P1-6 PostgreSQL:
7 PASS

P1-7 PostgreSQL:
2 PASS

PostgreSQL:
17.6

Alembic:
20260830_0005

ruff:
PASS

mypy:
67 source files PASS

P1-8 runtime:
NOT_RESUMED
```

The 13-path aggregate was independently recomputed from the exported bytes and matches exactly.

## accepted portions

The following are accepted and should not be redesigned:

```text
PostgreSQL bytea durable canonical bodies
65,536-byte hard cap
canonical structured JSON V1
durable content-kind allowlist
PUBLIC_SAFE / INTERNAL only
PRIVATE_SENSITIVE / SECRET_FORBIDDEN durable denial
V1/V2 Requirement fingerprint compatibility
legacy RequirementSet root preservation
forward-only 20260830_0005 migration
restart-safe durable body reconstruction
legacy metadata-only P1-8 eligibility denial
append-only durable object/binding rows
historical content integrity != current evidence effectiveness
```

Stage 0A and Stage 0B are valid and must be preserved.

---

# FINDING-1 — durable writer authority can be self-minted at the repository boundary

Current source:

```text
P1_6DurableContentAuthority()
→ constructor is public and creates a new process-local writer token

PostgresEvidenceRepository.admit(
    ...,
    prepared_durable_content=prepared,
    durable_content_authority=<caller supplied authority>
)
```

Repository verification is:

```text
durable_content_authority.recognizes(prepared_durable_content)
```

Therefore the caller controls both sides of the check.

A caller can conceptually do:

```text
rogue_authority = P1_6DurableContentAuthority()
rogue_prepared = rogue_authority.prepare_structured(...)

repository.admit(
    ...,
    prepared_durable_content=rogue_prepared,
    durable_content_authority=rogue_authority,
)
```

and pass the repository's capability check.

The current negative test only proves:

```text
prepared content
+ NO durable_content_authority argument
→ ACCESS_DENIED
```

It does not prove:

```text
caller-created authority
+ caller-created prepared content
→ denied
```

This violates the accepted boundary:

```text
P1-6-only writer
P1-8/caller direct write
→ forbidden
```

Required invariant:

```text
caller-supplied capability verifier
!= P1-6 write authority
```

### required rework

Bind the repository/service runtime to exactly one bootstrap/configured P1-6 durable writer authority.

Equivalent acceptable shape:

```text
bootstrap creates P1_6DurableContentAuthority exactly once

PostgresEvidenceRepository
→ constructed/configured with the exact recognized authority/capability

EvidenceAdmissionService
→ uses the same authority

repository durable write path
→ checks only its configured authority
→ caller cannot provide/substitute an authority argument
```

A rogue/new `P1_6DurableContentAuthority` instance must not authorize writes through the already configured
repository.

The direct repository durable API should either:

```text
not accept an authority parameter at all
```

or accept only an opaque authorization object minted by the configured owner and verified against the
repository-bound capability.

Do not rely on:

```text
class name
authority_id string
caller convention
```

as authority.

Process-local opaque capability is acceptable for current write authorization because it is not historical
provenance; historical authority remains PostgreSQL content/binding provenance.

---

# FINDING-2 — historical body read authorization is caller-asserted, not owner-issued

Current model:

```text
HistoricalContentAccessGrant(
    consumer: str,
    allow_internal: bool,
    allow_public_safe_body: bool,
)
```

is freely constructible.

Current resolver checks only:

```text
consumer is non-empty
and caller-set allow_internal / allow_public_safe_body flags
```

Therefore any internal caller can self-assert:

```text
HistoricalContentAccessGrant(
    "anything",
    allow_internal=True,
)
```

and receive exact `INTERNAL` canonical body bytes.

This does not meet:

```text
authorized historical consumer
```

and makes `access_policy` an advisory convention instead of owner-backed authority.

Required invariant:

```text
caller-constructed access request
!= historical content read authority
```

### required rework

Introduce an owner-backed current-access capability equivalent to:

```text
P1_6HistoricalContentAccessAuthority
```

and owner-issued:

```text
HistoricalContentAccessGrant
```

with opaque non-caller-mintable capability identity.

Recommended exact V1 consumer:

```text
P1_8_STRUCTURED_RESULT_V1
```

The P1-6 owner decides the allowed read ceiling.

For example:

```text
P1_8_STRUCTURED_RESULT_V1
→ PUBLIC_SAFE body: allowed
→ INTERNAL body: allowed
→ PRIVATE_SENSITIVE: impossible because not durably stored
→ SECRET_FORBIDDEN: impossible
→ export permission: separate; not implied
```

The caller may request a known consumer purpose, but must not set authoritative boolean permissions itself.

Repository resolver must verify:

```text
grant issued by the configured P1-6 historical-content access authority
consumer/purpose exact
grant capability recognized
content sensitivity/access policy within owner-issued ceiling
```

A directly constructed/forged dataclass with matching visible fields must fail closed.

This access capability is current authorization and does not enter historical content/Cycle identity.

---

# DB boundary note

Existing PostgreSQL:

```text
append-only UPDATE/DELETE triggers
REVOKE INSERT/UPDATE/DELETE FROM PUBLIC
```

is useful defense-in-depth, but it does not substitute for the application authority correction above.

This HOLD does not require introducing a new DB role or external secrets system.

---

# command-center judgment

```text
P1-6 core:
ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Runtime:
HOLD_REWORK_REQUIRED / HUMAN_PENDING

P1-8 Design:
ACCEPTED / CLOSED

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE / NOT_RESUMED

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

No Human runtime final review yet.

## preserved exact paths

Preserve:

```text
.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md

.aiassistant/records/aiscc/cycles/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260831_0103_aiscc-p1-6-durable-content-runtime-writer-and-read-capability-authority-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```
