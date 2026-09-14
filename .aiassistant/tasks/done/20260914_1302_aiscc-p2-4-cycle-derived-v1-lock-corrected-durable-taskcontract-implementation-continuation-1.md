# 작업지시서: P2-4 cycle-derived V1 lock-corrected durable TaskContract implementation continuation

## meta

- task_id: `20260914_1302_aiscc-p2-4-cycle-derived-v1-lock-corrected-durable-taskcontract-implementation-continuation-1`
- created_at: `2026-09-14T13:02:09+09:00`
- work_type: `CONTINUE_PARTIAL_IMPLEMENTATION + HUMAN_ACCEPTED_LOCK_CORRECTION + DOC_BASELINE_UPDATE + DATABASE_MIGRATION + QA_ONLY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `0400c7839088c10b6530968014180ccb3f7c943a`
- required_parent: `325a9044cb0a37694409c1b8285427640d3acaec`
- predecessor_result_zip_sha256: `56b72af5731f55ed8c171483e8113c4dbe1ab89461d46adaffd3079d985bb7bc`
- predecessor_done_task_sha256: `8749d2c2386a2d956215bb86a42b3858e2348ff3aa8297d28487affcd5b7b91f`
- predecessor_result: `BLOCKED / POLICY_CONFLICT_INVESTIGATION_REQUIRED`
- predecessor_executor_disposition: `ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED`
- Human_lock_correction_decision: `HUMAN_PROVIDED / ACCEPTED`
- Human_review_sha256: `6eb6dc79180c885f34b700c2d60a9439f986961078cb06c0f95a640f8c9f81e7`
- fresh_IDE_chat_required: `No`
- dirty_partial_candidate_continuation: `Yes / exact seven paths`
- governance_commit_authorized: `Yes / exact 4 paths / Commit A`
- result_commit_authorized: `Yes / exact allowlist / Commit B`
- canonical_durable_baseline_mutation_authorized: `Yes / exact 4 rule paths`
- P1_4_P1_6_P1_8_semantic_baseline_mutation_authorized: `No`
- migration_creation_authorized: `Yes / exact one migration`
- isolated_PostgreSQL_authorized: `Yes / task-owned ephemeral only`
- Docker_authorized: `Yes / local postgres:17.6 only`
- external_network_authorized: `No`
- provider_LLM_authorized: `No`
- retained_private_DB_authorized: `No`
- actual_self_dogfood_golden_cycle_authorized: `No`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. Human acceptance

Human decision:

```text
ACCEPT
```

Apply to:

```text
20260914_1212_aiscc-p2-4-taskcontract-v1-issuance-domain-lock-correction-human-review-1.md
SHA-256:
6eb6dc79180c885f34b700c2d60a9439f986961078cb06c0f95a640f8c9f81e7
```

Admit exactly as:

```text
HUMAN_PROVIDED / ACCEPTED
```

The accepted correction is narrow:

```text
TaskContract Durable Body V1 supported P1-8 issuance source:
open-cycle-derived-task-issuance

TaskContract Durable Body V1 unsupported P1-8 issuance source:
open-operational-recovery-task-issuance
```

This does NOT narrow P1-8 globally.

P1-8 continues to own and support OPERATIONAL_RECOVERY.

The V1 TaskContract issuer explicitly denies that source because its exact currentness proof requires a predecessor/source WorkRun lock and would violate the already accepted issuer/revoker lock invariant.

# 1. normative accepted chain

Normative chain:

```text
0319 durable-body base design
+ 0812 body_ref correction
+ 0902 Human/Judgment correction
+ 0940 template/approval authority Outcome A correction
+ 1212 V1 issuance-domain / lock correction
```

Precedence:

```text
1212 correction
> only the implicit/universal P1-8 source support assumption conflicting with the 0319 issuer lock invariant

0940
> conflicting 0319 template/approval-source clauses

0902
> conflicting 0319 Human/Judgment clauses

0812
> conflicting 0319 body_ref clause

all other 0319 requirements:
remain accepted
```

Do not redesign these accepted decisions.

# 2. accepted input verification

Package `ACCEPTED_DESIGN/**` hashes:

- `0319/TASKCONTRACT_DURABLE_BODY_BASELINE_PROPOSAL.md`: `803686433f900282117a4318d8f59a14b5b5a68735775b4f1242acf544c16410`
- `0812/20260914_0812_aiscc-p2-4-durable-taskcontract-body-ref-compatibility-human-correction-review-1.md`: `4c6905734e7a48b9688257574d86b1a7215627ac8514c7112747889c6bafa318`
- `0902/BASELINE_SUPERSESSION_DELTA.md`: `47a473ab37a9fec09dee623dc254acf7d0b726f30cbae5c251715679ff6a9448`
- `0902/HUMAN_BINDING_CORRECTION_PROPOSAL.md`: `7ecad09c1e151fc76e83d85d7a84c25c14f09abba7e093393a5cf73b9a1d2833`
- `0902/HUMAN_JUDGMENT_POLICY_SOURCE_AUDIT.md`: `2595ac130c12a0da3cf45dc7867e4cb6806fafc83e0c77feec51147ccc57b0a9`
- `0902/IMPLEMENTATION_IMPACT_ALLOWLIST.md`: `aee264ccc3aaa5aa6906c3c96ad0981d0c5aea11c68895e63dad3b3638632c6b`
- `0902/JUDGMENT_BINDING_CORRECTION_PROPOSAL.md`: `aed8421248cc8700fd0ebc2128ae7f5808037df555fbe8e0ee61606dd0eb9693`
- `0902/OWNER_NON_SUBSTITUTION_PROOF.md`: `7f22c68055d2cb2c118aa7ca67efc01ab36c09811030362bc935d23634e70a92`
- `0940/BASELINE_SUPERSESSION_DELTA.md`: `20f050403f50f9edaa9c445ba049135da896b52cc31dadf03a7912dde34d7e69`
- `0940/IMPLEMENTATION_IMPACT_ALLOWLIST.md`: `cf5a4cc5932d4ebaec1d84376bfbaff7a9c7d93cfba5379f883ebd94d3766080`
- `0940/OWNER_NON_SUBSTITUTION_PROOF.md`: `3ba78e965f88749d6805268d049154366f7bbcee1c1d77697393230c7e6aff23`
- `0940/P1_8_DESCRIPTOR_TEMPLATE_SEMANTICS_AUDIT.md`: `609d6c085b7edd2a79bbf8afd0e2461ec1919642cfdb33e333bea5c64676668c`
- `0940/TASKCONTRACT_TEMPLATE_REQUIREMENT_CORRECTION_PROPOSAL.md`: `da2bf0d59e148d6359b7e979296a7d63b01307f0500df6c2e715937527edd951`
- `0940/TEMPLATE_AUTHORITY_CANONICAL_AUDIT.md`: `2889d21300126671ee1e1b3ecc3acf3b1a96358b1e26c81e253e94413b4f5f85`

Human review:

```text
20260914_1212_aiscc-p2-4-taskcontract-v1-issuance-domain-lock-correction-human-review-1.md
6eb6dc79180c885f34b700c2d60a9439f986961078cb06c0f95a640f8c9f81e7
```

Predecessor diagnostic evidence:

- `CONTRACT_REVIEW.md`: `44927d228ca4484babef2c85db9f3ff1e6599f48d1e38b53f0612882c263904d`
- `P1_6_DEFINITION_API_EVIDENCE.md`: `31334f024427799a44e41e4b69e43a7010a5985dd356bccc86cc17291ec25617`
- `P1_6_DEFINITION_LOCK_ORDER_REVIEW.md`: `4b87e609906c8f7cbadcba2feacd27486f99cf34e437b21ae21eddd1b86ff83d`
- `P1_8_CURRENTNESS_API_EVIDENCE.md`: `d8aa41aa8ddf037fe8061ce4a0f6de37d0f5069fff51a4473066cafb08024ac0`
- `P1_8_CURRENTNESS_LOCK_ORDER_REVIEW.md`: `f3fb1acab82a4cfdfa7bc6a0218d130a2600a9b482810b9d61d8ec68078f4554`
- `SOURCE_CHANGE_REVIEW.md`: `34e33a37e802d2a532cd723d7220138679eae6286ed7d50d7ac3b9117aaa3b9c`
- `TEST_RESULTS.md`: `369b2ef87a12362ccdf4eb0de1193abc49d4714b1e77b1d0d664e642b0fd8f7a`
- `WORKSPACE_VERIFICATION.md`: `39ce9f44621ce1d1f0d159ad70db82995138567292297daa974b6d0bc7688d37`

After current Task is placed/read, copy package inputs only to:

```text
.aiassistant/reports/target/20260914_1302_aiscc-p2-4-cycle-derived-v1-lock-corrected-durable-taskcontract-implementation-continuation-1/accepted-input/
```

Any mismatch -> `BLOCKED_MISSING_ARTIFACT`.

# 3. exact dirty-workspace continuation preflight

This Task MUST continue the current partial candidate; do not reset/clean it.

Require:

```text
branch:
main

HEAD:
0400c7839088c10b6530968014180ccb3f7c943a

HEAD^:
325a9044cb0a37694409c1b8285427640d3acaec

index:
empty
```

Expected product/test dirt EXACTLY seven paths with current bytes:

- `src/aiscc/evidence/repository.py`: `1a6f208b7251ec20a145812e846e96208db159a7ffd114a10f46a9d78799f8f5`
- `src/aiscc/next_action/repository.py`: `bb0424281e8fb36f7bccffccd83d4a0caa3e9bc44a0a5c783a7ab2d538af9a02`
- `src/aiscc/task_authority/ports.py`: `d817eabbf0e1c6ba0b3eacde3cd196a334938734f640f90e6202efca93870be9`
- `src/aiscc/task_authority/repository.py`: `2d24617a4e2435dd674b16c6e97c6bc30b8ae4338b445eca51d7c0f46909691a`
- `tests/integration/memory/test_postgres_project_memory_next_action.py`: `18a66de8e00edb3069a767be7f12b530ef6dcd7ab6c2199fa473ddecc78650b2`
- `src/aiscc/task_authority/contracts.py`: `63f94f7c46eba1882b9fdf3ae4d27421f7649b56e6033672badc8c008f98a93e`
- `tests/integration/evidence/test_requirement_definition_resolver.py`: `34dc1e135cbee9ac6f7c710cd4374a6db4f5265d43a65a6d0bc40ff0e23fae74`

Expected path status:

### tracked modified

```text
src/aiscc/evidence/repository.py
src/aiscc/next_action/repository.py
src/aiscc/task_authority/ports.py
src/aiscc/task_authority/repository.py
tests/integration/memory/test_postgres_project_memory_next_action.py
```

### untracked product/test

```text
src/aiscc/task_authority/contracts.py
tests/integration/evidence/test_requirement_definition_resolver.py
```

### untracked governance

```text
.aiassistant/tasks/done/20260914_1131_aiscc-p2-4-p1-6-definition-resolver-scope-expanded-durable-taskcontract-implementation-retry-1.md
```

Done Task SHA:

```text
8749d2c2386a2d956215bb86a42b3858e2348ff3aa8297d28487affcd5b7b91f
```

Preserve ignored legacy Task:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Canonical state exact:

```text
CURRENT_STATE_SUMMARY.md
80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48

DECISION_REGISTER.md
9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5

NEXT_ACTIONS.md
050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679
```

Unexpected dirt or byte mismatch -> `DIRTY_WORKSPACE_MIXED` and STOP.

Do NOT use `git reset`, `git checkout --`, `git clean`, broad deletion, or overwrite predecessor partial work merely to satisfy preflight.

# 4. executables

Use only:

```text
Python:
<repository-root>\.venv\Scripts\python.exe

Git:
C:\Program Files\Git\cmd\git.exe

Docker:
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

Docker only for isolated PostgreSQL proof.

# 5. inbound placement + Governance Commit A

Order:

```text
verify ZIP/hash/archive/member safety
→ place current Task in .aiassistant/tasks/active
→ read Task
→ verify exact partial workspace
→ verify accepted inputs
→ place Cycle/Judgment/Human review canonical copies
```

Canonical placement:

```text
20260914_1302_aiscc-p2-4-v1-issuance-domain-human-accepted-implementation-continuation-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_1302_aiscc-p2-4-v1-issuance-domain-lock-correction-human-acceptance-reauthorization-1.md
-> .aiassistant/reports/aiscc/

20260914_1212_aiscc-p2-4-taskcontract-v1-issuance-domain-lock-correction-human-review-1.md
-> .aiassistant/reports/aiscc/
```

Before Commit A:

- preserve all seven partial product/test paths unstaged and byte-exact;
- stage EXACTLY these four governance paths:

```text
.aiassistant/tasks/done/20260914_1131_aiscc-p2-4-p1-6-definition-resolver-scope-expanded-durable-taskcontract-implementation-retry-1.md
.aiassistant/records/aiscc/cycles/20260914_1302_aiscc-p2-4-v1-issuance-domain-human-accepted-implementation-continuation-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_1302_aiscc-p2-4-v1-issuance-domain-lock-correction-human-acceptance-reauthorization-1.md
.aiassistant/reports/aiscc/20260914_1212_aiscc-p2-4-taskcontract-v1-issuance-domain-lock-correction-human-review-1.md
```

Commit message exactly:

```text
docs(aiscc): accept taskcontract v1 issuance domain lock correction
```

Require:

```text
Commit A parent = 0400c7839088c10b6530968014180ccb3f7c943a
Commit A changed paths = exact 4
index empty
seven-path product/test partial candidate preserved
```

No other commit before product completion.

# 6. exact V1 issuance-domain correction

Implement a fail-closed capability boundary in TaskContract V1.

Supported:

```text
open-cycle-derived-task-issuance
```

Unsupported:

```text
open-operational-recovery-task-issuance
```

Use existing canonical P1-8 action identity/source representation from current source.
Do not invent a duplicate enum if the existing source already provides a stable typed/constant identity.

At TaskContract issuance:

1. verify exact current P1-8 selection through existing owner API;
2. verify descriptor/action/source lineage;
3. require the selected action/source to be the supported cycle-derived issuance;
4. if OPERATIONAL_RECOVERY or any source requiring predecessor/source WorkRun locking is selected:
   deny before TaskContract body/ref/event mutation;
5. use a stable domain error/reason such as:

```text
TASKCONTRACT_V1_UNSUPPORTED_NEXT_ACTION_SOURCE
```

following existing exception conventions.

Do NOT:

```text
translate recovery -> cycle-derived
skip currentness
drop the P1-4 source-run lock from recovery verification
validate recovery outside the issuance transaction
silently support it without lock proof
```

# 7. preserve 0319 issuer/revoker lock invariant

Keep unchanged:

```text
TaskContract issuer/revoker:
never acquire WorkRun locks
```

The supported cycle-derived path must be proven not to acquire a source/predecessor WorkRun lock.

The P1-8 public verifier may still support OPERATIONAL_RECOVERY for P1-8 callers generally; TaskContract V1 must reject that source BEFORE entering any source WorkRun lock dependency.

Do not globally alter `verify_current_selection(...)` to weaken recovery semantics.

# 8. exact lock-order proof to close

Produce:

```text
TASKCONTRACT_V1_LOCK_ORDER_PROOF.md
```

Prove from actual source and PostgreSQL concurrency tests:

## issuance

Required effective order:

```text
TaskContract family serialization
→ P1-8 cycle-derived currentness locks
→ P1-6 definition-authority locks
→ durable body/ref/event writes
```

No WorkRun lock.

If current source naturally obtains owner locks before the family lock, document the exact actual order and prove there is no reverse dependency. Do not mechanically force this textual order if existing accepted owner implementation differs.

Mandatory invariants:

```text
issuer/revoker never acquire WorkRun locks
P1-8 cycle-derived currentness cannot be invalidated between verify and body issuance
P1-6 definition currentness cannot be invalidated between verify and body issuance
no P1-8/P1-6 writer acquires TaskContract family lock in reverse order
```

## READY

Preserve:

```text
target WorkRun lock first
→ TaskContract family lock
→ TaskContract body/currentness verify
→ P1-8 cycle-derived currentness verify
→ P1-6 definition-currentness verify
→ existing Human/Judgment configuration checks
→ P1-4 alone performs READY/state mutation
```

No source/predecessor WorkRun lock is permitted for V1.

If this cannot be proven without changing P1-4/P1-6/P1-8 semantic owner contracts:

```text
LOCK_ORDER_SCOPE_REVIEW_REQUIRED
```

STOP.

# 9. future golden-cycle gate

This Task does NOT perform the golden cycle.

But source and tests must expose/verify the future gate:

```text
actual authoritative current NextAction
must resolve to:
open-cycle-derived-task-issuance
```

If future golden execution resolves to:

```text
open-operational-recovery-task-issuance
```

or another unsupported source:

```text
TASKCONTRACT_V1_UNSUPPORTED_NEXT_ACTION_SOURCE
```

and the golden execution must STOP for separate lock-order design review.

No silent fallback.

# 10. complete P1-8 currentness verifier

Preserve 1131 partial bytes and finish all required proof.

Required:

```text
current exact cycle-derived selection PASS
wrong selection DENY
withdrawn DENY
superseded/current-projection mismatch DENY
later policy revocation DENY
later source/subject authority revocation DENY where source semantics apply
wrong candidate DENY
wrong descriptor/source lineage DENY
historical replay-valid but non-current DENY
caller-owned AsyncSession reused
no own session/commit/rollback
zero DML
concurrent invalidation cannot pass stale proof
```

Also prove:

```text
OPERATIONAL_RECOVERY still verifies according to existing P1-8 owner semantics
outside TaskContract V1

TaskContract V1 rejects it as unsupported source
without weakening that P1-8 owner behavior
```

# 11. complete P1-6 definition resolver

Preserve current partial implementation and corrected fault-injection fixture.

Finish final-byte tests.

Resolver remains definition authority only.

Required:

```text
current exact RequirementSet/checkpoint graph PASS
wrong task_id DENY
wrong set fingerprint DENY
missing requirement DENY
extra/unbound requirement DENY
wrong requirement fingerprint/profile/requiredness/reuse DENY
wrong checkpoint fingerprint DENY
wrong checkpoint source/target-purpose DENY
revoked graph DENY
superseded/corrected graph DENY
historical-valid-but-non-current DENY
restart/reconstruction PASS
caller session/transaction reused
no own session/commit/rollback
zero durable DML on PASS/DENY
concurrent revoke/supersede/correct cannot pass stale proof
no WorkRun/evaluation/attestation/G_EVIDENCE created
```

Do not weaken append-only P1-6 tables just to create test corruption.
Use bounded transaction-local fault injection or existing accepted test mechanisms.

# 12. complete durable TaskContract runtime

Continue existing partial files, do not rewrite as a parallel implementation.

Implement/finish:

```text
TaskContractBodyV1
IssuedTaskContractV1
VerifiedTaskContractBindingV1
TaskContractBodyRow
issue_task_contract(...)
get_task_contract(...)
verify_task_contract(...)
revoke_task_contract(...)
TaskContractReadyParticipant
```

Preserve accepted:

```text
closed immutable body
restricted canonical JSON/JCS
NFC / safe integer / path safety
1 MiB canonical body max
version lineage / predecessor
exact retry idempotency
changed same-version deny
explicit latest revoke/currentness
restart verification
missing/tampered/partial -> AUTHORITY_CORRUPTION
no auto-repair/backfill
```

# 13. body_ref — 0812 exact

```text
body_identity_bytes =
JCS({
  "project_id": project_id,
  "contract_id": contract_id,
  "contract_version": n
})

body_ref =
"task-contract-body:v1:sha256:" + SHA256(body_identity_bytes)
```

Exact length:

```text
93 ASCII
```

Content integrity remains:

```text
body_sha256 = SHA256(canonical_body)
constraint_payload_ref = body_ref
constraint_payload_fingerprint = body_sha256
```

Do not widen existing V1 ID validator and do not narrow accepted 96-char ID domain.

# 14. Human/Judgment correction

Implement exact 0902 accepted configuration.

TaskContract contains only immutable owner-consumable Human/Judgment configuration.

READY/issuance must NOT:

```text
reserve/open HumanGate
authenticate Human
create HumanResult
create Judgment
mint G_HUMAN_*
mint G_JUDGMENT_*
mint G_EVIDENCE
```

Existing P1-7/Judgment owners retain runtime fingerprints/currentness and result authority.

# 15. template/approval Outcome A

For current recognized catalog descriptor:

```text
task_template_ref/hash NONE/null
```

means absence of separate template provenance, not approval.

Complete immutable body still requires:

```text
current P1-8 cycle-derived selection/descriptor lineage
+ EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY explicit body authorization
+ P1-6 definition authority
+ durable body/ref/event verification
```

No template registry/table/resolver.

# 16. authority_refs

Preserve 0940 accepted semantics:

```text
required field
possibly empty
sorted
closed {ref, fingerprint} entries
```

Empty means:

```text
no additional independent authority ref required by applicable existing owner policy
```

not no authority.

All present/required refs verify through existing semantic owners.

Self-reference/circular TaskContract body ref denied.

# 17. canonical baseline adoption

Create/modify only:

```text
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

The durable-body baseline must explicitly record:

```text
V1 source capability:
cycle-derived only

OPERATIONAL_RECOVERY:
valid P1-8 authority
but unsupported by TaskContract Durable Body V1

issuer/revoker WorkRun-lock prohibition:
unchanged
```

Do NOT modify:

```text
AISCC_EVIDENCE_ADMISSION.md
AISCC_HUMAN_GATE_JUDGMENT.md
AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md
```

# 18. migration

Precondition:

```text
single Alembic head = 20260901_0008
20260914_0009 absent
```

Else:

```text
MIGRATION_BASELINE_MISMATCH
```

Create exactly:

```text
migrations/versions/20260914_0009_task_contract_durable_bodies.py
revision = 20260914_0009
down_revision = 20260901_0008
```

Accepted one-table additive design only:

```text
task_contract_bodies
```

No P1-6/P1-8 schema change.

Immutable UPDATE/DELETE/TRUNCATE denial.
No backfill.
No pgcrypto dependency.
Empty-only downgrade.
Nonempty downgrade fail-closed preserving data/schema/revision.

# 19. exact mutation allowlist

## canonical

```text
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

## P1-8

```text
src/aiscc/next_action/repository.py
tests/unit/next_action/test_next_action_domain.py
tests/integration/memory/test_postgres_project_memory_next_action.py
```

## P1-6

```text
src/aiscc/evidence/repository.py
src/aiscc/evidence/ports.py
tests/unit/evidence/test_requirement_definition_resolver.py
tests/integration/evidence/test_requirement_definition_resolver.py
```

Up to two existing direct P1-6 owner tests may be modified only if first named in `P1_6_TEST_INVENTORY.md`.

## TaskContract

```text
src/aiscc/task_authority/contracts.py
src/aiscc/task_authority/authority.py
src/aiscc/task_authority/ports.py
src/aiscc/task_authority/repository.py
src/aiscc/task_authority/ready.py
src/aiscc/task_authority/__init__.py
src/aiscc/persistence/models.py
```

## migration

```text
migrations/versions/20260914_0009_task_contract_durable_bodies.py
```

## TaskContract tests

```text
tests/unit/task_authority/test_task_contract_body.py
tests/unit/task_authority/test_task_contract_issuance.py
tests/integration/task_authority/test_task_contract_durability.py
tests/integration/task_authority/test_task_contract_ready.py
```

READ-ONLY:

```text
src/aiscc/next_action/models.py
src/aiscc/next_action/__init__.py
src/aiscc/evidence/requirements.py
src/aiscc/evidence/models.py
src/aiscc/workflow/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/task_authority/models.py
```

If another mutation path is genuinely necessary:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

If an existing semantic owner contract must change:

```text
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

STOP.

# 20. isolated PostgreSQL 17.6 proof

First:

```text
"C:\Program Files\Docker\Docker\resources\bin\docker.exe" image inspect postgres:17.6
```

If missing:

```text
ISOLATED_POSTGRES_IMAGE_MISSING
```

No pull.

Use one new Task-owned container, e.g.:

```text
aiscc-p2-4-taskcontract-1302-pg
```

Synthetic credentials and loopback-only port.

Required complete proof:

## migration

```text
empty DB -> head PASS
0008 -> 0009 PASS
```

## body durability

```text
restart exact body/ref/hash PASS
96/96 IDs -> exact 93-char ref PASS
exact retry idempotent PASS
changed same-version DENY
concurrent version/issuance race deterministic
transaction rollback leaves no partial body/ref/event
UPDATE/DELETE/TRUNCATE denied
empty downgrade PASS
nonempty downgrade fail-closed preserving data/schema/revision
```

## V1 source capability / locks

```text
cycle-derived current selection PASS
OPERATIONAL_RECOVERY TaskContract V1 issuance DENY
unsupported-source denial creates zero body/ref/event rows
issuer cycle-derived path acquires no WorkRun lock
concurrent P1-8 invalidation cannot pass stale issuance
concurrent P1-6 invalidation cannot pass stale issuance
no reverse family/P1-8/P1-6 lock path
READY uses target WorkRun first then family
READY never acquires source/predecessor WorkRun lock
```

## P1-6

all section 11 proof.

## P1-8

all section 10 proof.

## Human/Judgment

```text
NOT_REQUIRED reload/verify PASS
REQUIRED reload/verify PASS
Judgment config register/reload idempotent/current
READY creates no HumanResult/Judgment/G_HUMAN/G_JUDGMENT/G_EVIDENCE
```

No retained/private DB/provider/network/golden cycle.

Exact Task container cleanup best-effort; residue nonblocking.

# 21. tests/static closure

Inventory directly affected regression files/counts first.

Run required new/changed tests and direct regressions for:

```text
P1-6 evidence authority
P1-8 next-action authority
task_authority
P1-4 READY/transition
P1-7 Human/Judgment
```

Final requirements:

```text
all required pytest PASS
Ruff changed Python PASS
compile changed Python PASS
git diff --check PASS
UTF-8/control/fence checks PASS
```

The predecessor:

```text
5 PASS / 9 FAIL P1-6 expanded run
23 Ruff findings
```

must not be reported as final evidence.
Only final bytes/results count.

# 22. Result Commit B

Only after ALL required evidence PASS.

Stage all and only authorized product/canonical/migration/test paths actually changed.

Commit message exactly:

```text
feat(aiscc): add durable taskcontract authority
```

Require:

```text
Commit B parent = Governance Commit A
index empty
tracked clean
no read-only path changed
```

No Commit B on blocker/failure.

# 23. report/export

Target:

```text
.aiassistant/reports/target/20260914_1302_aiscc-p2-4-cycle-derived-v1-lock-corrected-durable-taskcontract-implementation-continuation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ACCEPTED_DESIGN_INPUT_VERIFICATION.md
V1_ISSUANCE_DOMAIN_ACCEPTANCE_VERIFICATION.md
TASKCONTRACT_V1_LOCK_ORDER_PROOF.md
P1_8_CURRENTNESS_API_EVIDENCE.md
P1_8_CURRENTNESS_LOCK_ORDER_REVIEW.md
P1_6_TEST_INVENTORY.md
P1_6_DEFINITION_API_EVIDENCE.md
P1_6_DEFINITION_LOCK_ORDER_REVIEW.md
BODY_REF_COMPATIBILITY_EVIDENCE.md
HUMAN_JUDGMENT_BINDING_EVIDENCE.md
TEMPLATE_AUTHORITY_BINDING_EVIDENCE.md
BASELINE_ADOPTION_REVIEW.md
SOURCE_CHANGE_REVIEW.md
MIGRATION_REVIEW.md
POSTGRES_RUNTIME_EVIDENCE.md
TEST_RESULTS.md
CONTRACT_REVIEW.md
```

Include changed project-relative files and canonical current Cycle/Judgment/Human review/done Task.

No credentials/raw DB dump/unrelated source.

# 24. terminal repository boundary

Success:

```text
HEAD = Result Commit B
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1302_aiscc-p2-4-cycle-derived-v1-lock-corrected-durable-taskcontract-implementation-continuation-1.md
```

Current Task active -> done byte-exact.

Legacy 1400 exact unchanged.

Canonical state hashes unchanged.

Blocked:

- no Result Commit B;
- preserve truthful partial work;
- no broad reset/cleanup.

# 25. mandatory stop

```text
BLOCKED_MISSING_ARTIFACT
DIRTY_WORKSPACE_MIXED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
LOCK_ORDER_SCOPE_REVIEW_REQUIRED
MIGRATION_BASELINE_MISMATCH
ISOLATED_POSTGRES_IMAGE_MISSING
BLOCKED_REQUIRED_EVIDENCE
SECURITY_BOUNDARY_BLOCKED
```

# 26. success ceiling

Complete PASS may report only:

```text
P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do NOT perform or claim:

```text
actual self-dogfood golden cycle
P2_4_SELF_DOGFOOD_ENTRY_SOURCE_CANDIDATE
P2-4 ACCEPTED/CLOSED
```
