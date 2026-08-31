# 작업지시서: P1-6 Durable Content Writer + Historical Read Capability Runtime Rework

## meta

- task_id: `20260831_0103_aiscc-p1-6-durable-content-writer-and-historical-read-capability-runtime-rework-1`
- created_at: `2026-08-31T01:03:00+09:00`
- phase: `P1-6 Durable Evidence Content Authority Extension Runtime`
- work_type: `RUNTIME_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_6_EVIDENCE_CONTENT`
- expected_start_head: `bc446d9530e28f9b10602c9f1dd5232a97221a10`
- predecessor_runtime_path_count: `13`
- predecessor_runtime_aggregate_sha256: `8119fcb3ea10b3fb86e986b21ca0cd638e14b9021ac903fa007d750124392962`
- accepted_extension_design_sha256: `ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411`
- p1_8_runtime_status: `BLOCKED_REQUIRED_EVIDENCE / NOT_RESUMED`

---

# 1. purpose

Close exactly two runtime authority gaps:

```text
1. caller can self-mint the durable write authority supplied to repository.admit

2. caller can self-mint HistoricalContentAccessGrant permissions
```

Preserve all other accepted 2357 runtime behavior.

Place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260831_0103_aiscc-p1-6-durable-content-runtime-writer-and-read-capability-authority-hold-1.cycle.md
```

Do not amend/revert Stage 0A/0B:

```text
32e88234ad7a7cbaa545e12f8c7e03b5897202cb
bc446d9530e28f9b10602c9f1dd5232a97221a10
```

---

# 2. mandatory preflight

Require:

```text
HEAD ==
bc446d9530e28f9b10602c9f1dd5232a97221a10

accepted extension design SHA ==
ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411
```

Verify exact predecessor 13-path candidate aggregate:

```text
8119fcb3ea10b3fb86e986b21ca0cd638e14b9021ac903fa007d750124392962
```

Any mismatch:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

Index must be empty.

No Git add/commit/push.

---

# 3. FINDING-A — bind durable writer authority to repository/service bootstrap

Current unsafe shape:

```text
repository.admit(
    ...,
    prepared_durable_content=prepared,
    durable_content_authority=<caller supplied>
)
```

Remove caller-substitutable verifier authority.

Implement one exact owner binding.

Recommended shape:

```text
content_authority = P1_6DurableContentAuthority()

repository = PostgresEvidenceRepository(
    session_factory,
    durable_content_authority=content_authority,
    historical_content_access_authority=...
)

service = EvidenceAdmissionService(
    repository,
    evaluator,
    durable_content_authority=content_authority,
)
```

Repository durable path verifies:

```text
self._durable_content_authority.recognizes(prepared)
```

not an authority object supplied per call.

If no configured authority:

```text
prepared durable write
→ DURABLE_CONTENT_ACCESS_DENIED
```

`repository.admit()` should not expose a caller-selected `durable_content_authority` parameter.

Equivalent private/internal API split is acceptable if the caller still cannot substitute the authority.

Required:

```text
rogue_authority = P1_6DurableContentAuthority()
rogue_prepared = rogue_authority.prepare_structured(...)

configured_repository.admit(... rogue_prepared ...)
→ ACCESS_DENIED
→ no durable row
→ no binding row
```

Even when all visible authority IDs/versions/refs are copied exactly.

The configured legitimate authority:

```text
→ PASS
```

---

# 4. service/repository consistency

Prevent split configuration.

If service is configured with durable authority A but repository is configured with B:

```text
startup/construction
→ fail closed
```

or the service must delegate preparation/authorization through the repository-bound owner so two independent
authority objects cannot exist for one production path.

Freeze a simple exact invariant in code/tests:

```text
one configured P1-6 durable writer capability per repository/service authority boundary
```

Do not use string equality as the only check.

---

# 5. FINDING-B — owner-issued historical read capability

Replace freely authoritative booleans with an owner-issued capability.

Implement exact equivalent of:

```text
P1_6HistoricalContentAccessAuthority
```

It owns an opaque current-read token.

`HistoricalContentAccessGrant` may retain visible metadata, but must include opaque capability identity excluded
from equality/repr/public serialization as appropriate.

Recommended owner API:

```text
issue_p1_8_structured_result_grant()
```

with fixed V1 purpose:

```text
P1_8_STRUCTURED_RESULT_V1
```

The owner, not caller, fixes allowed body classes.

V1 desired ceiling:

```text
PUBLIC_SAFE:
read allowed for internal P1-8 derivation

INTERNAL:
read allowed for internal P1-8 derivation

PRIVATE_SENSITIVE:
not durable in V1

SECRET_FORBIDDEN:
never durable
```

Public/export permission remains separate.

Do not let a generic caller do:

```text
issue(consumer="x", allow_internal=True)
```

unless the authority itself resolves a versioned allowlist and ignores caller booleans.

---

# 6. resolver recognition

Configure `PostgresEvidenceRepository` with the exact historical access authority/recognizer.

Before returning bytes:

```text
grant recognized by configured access authority
consumer/purpose exact
grant current authorization valid
content access_policy permits internal authority read
content sensitivity within grant ceiling
```

A direct dataclass construction with copied visible fields:

```text
→ DURABLE_CONTENT_ACCESS_DENIED
```

A grant from a different authority instance:

```text
→ DURABLE_CONTENT_ACCESS_DENIED
```

A valid configured P1-8 grant:

```text
→ exact historical bytes
```

The capability token is current access authorization only.

Do NOT add it to:

```text
DurableEvidenceContentObject fingerprint
EvidenceContentRef
AdmittedEvidence
Cycle identity
ProjectMemory content identity
```

---

# 7. access-policy semantics

Preserve:

```text
PRIVATE_AUTHORITY_ONLY
PUBLIC_SAFE_EXPORT
```

For internal P1-8 structured reconstruction, explicitly define that both accepted durable sensitivities can be
read only with the owner-issued P1-8 grant.

`PUBLIC_SAFE_EXPORT` does not imply anonymous/public runtime body access.

Export remains a separate owner/export policy path.

No new export implementation is required.

---

# 8. P1-8 one-way boundary

Required negative proof:

```text
P1-8-like caller has:
repository object
candidate/ref IDs
exact visible metadata

but lacks P1-6 writer capability
→ cannot write

lacks P1-6 issued historical read grant
→ cannot resolve body
```

Required positive proof:

```text
P1-8-like consumer receives exact owner-issued read grant
→ may read historical canonical bytes
→ cannot write or mint another grant
```

Do not implement actual P1-8 Cycle/Memory runtime.

---

# 9. allowed runtime mutation

Expected narrow files:

```text
src/aiscc/evidence/content.py
src/aiscc/evidence/models.py
src/aiscc/evidence/ports.py
src/aiscc/evidence/repository.py
src/aiscc/evidence/service.py
src/aiscc/evidence/__init__.py

tests/unit/evidence/test_durable_content.py
tests/integration/evidence/test_postgres_evidence_admission.py
```

Touch other current 13-path files only if strictly needed for compile/test compatibility.

No migration/schema change is expected.

If a migration is required:

```text
STOP
→ IMPLEMENTATION_BASELINE_GAP
```

unless it is purely additive and clearly required by accepted design; report before proceeding rather than
silently broadening.

Do not modify P1-8 runtime source.

---

# 10. mandatory tests

## 10.1 rogue writer

Prove:

```text
configured authority A
repository bound to A

rogue authority B
prepared by B

repository durable admission
→ ACCESS_DENIED
→ content rows unchanged
→ binding rows unchanged
```

Also:

```text
A-prepared + configured path
→ PASS
```

## 10.2 caller-selected authority substitution

If any lower-level repository method still accepts an authority parameter:

```text
passing B explicitly
→ cannot override configured A
```

Preferred:

```text
no such public parameter exists
```

## 10.3 forged read grant

```text
HistoricalContentAccessGrant(
  visible fields matching valid P1-8 grant
)
→ ACCESS_DENIED
```

## 10.4 foreign read authority

```text
grant issued by authority B
repository configured with authority A
→ ACCESS_DENIED
```

## 10.5 exact P1-8 read grant

```text
authority A issues P1_8_STRUCTURED_RESULT_V1 grant
→ PUBLIC_SAFE exact body PASS
→ INTERNAL exact body PASS
```

No public export claim.

## 10.6 restart

Restart repository/services while using the configured access authority/bootstrap pattern:

```text
durable content remains byte-identical
historical provenance remains valid
new current access capability may be reissued by bootstrap owner
```

Historical object identity must not depend on old process token.

---

# 11. regression requirements

Preserve and rerun:

```text
canonicalization/boundary tests

V1/V2 Requirement fingerprint vectors

legacy RequirementSet root

legacy P1-6 historical provenance

P1-7 historical Human/Judgment provenance

P1-8 metadata-only eligibility denial

concurrency/idempotency

corruption fail-closed

SECRET_FORBIDDEN persisted row count = 0
```

Mandatory:

```text
full unit + integration
P1-4 PostgreSQL regression
P1-6 PostgreSQL regression
P1-7 PostgreSQL regression
ruff
mypy src
alembic check
```

Report exact counts.

---

# 12. Git policy

No Stage 1 Git actions:

```text
NO git add
NO commit
NO push
```

HEAD must remain:

```text
bc446d9530e28f9b10602c9f1dd5232a97221a10
```

Move Task active→done on successful Executor submission.

That lifecycle file remains uncommitted.

---

# 13. runtime aggregate

Recompute over the final runtime source/test/migration paths only.

Do not include:

```text
Task
Cycle
canonical state
target bundle
```

Use exact existing algorithm:

```text
sort paths ordinally
<path>\t<sha256>\n
SHA-256
```

Report predecessor aggregate and final aggregate.

---

# 14. mandatory stop

STOP on:

```text
predecessor aggregate drift

fix requires changing accepted durable-content design

fix requires P1-8 implementation

fix requires DB schema/migration semantic expansion

legacy provenance regression

P1-6 core admission authority changes

PRIVATE_SENSITIVE/SECRET_FORBIDDEN storage becomes required
```

Use exact typed report.

---

# 15. evidence contract

## executor_required

```text
WRITER_CAPABILITY_BINDING
READ_CAPABILITY_BINDING
ROGUE_WRITER_NEGATIVE
FORGED_READ_GRANT_NEGATIVE
FOREIGN_AUTHORITY_NEGATIVE
VALID_P1_8_READ_POSITIVE
RESTART
LEGACY_PROVENANCE
PREDECESSOR_REGRESSION
STATIC_SOURCE
```

## human_owned

```text
P1-6 durable evidence-content runtime final acceptance
→ HUMAN_PENDING
```

---

# 16. export

Target:

```text
.aiassistant/reports/target/
20260831_0103_aiscc-p1-6-durable-content-writer-and-historical-read-capability-runtime-rework-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Include byte-preserving copies of final changed runtime paths, this HOLD Cycle, and done Task.

Manifest must include:

```text
HEAD
predecessor runtime aggregate
final runtime path count
per-file SHA
final runtime aggregate
source/copy identity
index status
Git actions
```

---

# 17. expected submission state

```text
P1-6 core:
ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Design:
ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Runtime:
REWORKED_CANDIDATE / HUMAN_PENDING

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE / NOT_RESUMED

P2:
NOT_STARTED
```

Command Center:

```text
review
→ PASS / HUMAN_FINAL_REVIEW_REQUIRED
or
→ HOLD_REWORK_REQUIRED
```

---

# 18. preserved exact paths

Preserve:

```text
.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md

.aiassistant/records/aiscc/cycles/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260831_0103_aiscc-p1-6-durable-content-runtime-writer-and-read-capability-authority-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md

.aiassistant/tasks/done/
20260831_0103_aiscc-p1-6-durable-content-writer-and-historical-read-capability-runtime-rework-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```
