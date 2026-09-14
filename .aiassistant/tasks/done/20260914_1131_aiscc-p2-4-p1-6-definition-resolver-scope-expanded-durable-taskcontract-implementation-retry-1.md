# 작업지시서: P2-4 P1-6 definition resolver scope-expanded durable TaskContract implementation retry

## meta

- task_id: `20260914_1131_aiscc-p2-4-p1-6-definition-resolver-scope-expanded-durable-taskcontract-implementation-retry-1`
- created_at: `2026-09-14T11:31:06+09:00`
- work_type: `OWNER_API_NARROW_EXPANSION + CONTINUE_PARTIAL_IMPLEMENTATION + DOC_BASELINE_UPDATE + DATABASE_MIGRATION + QA_ONLY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `325a9044cb0a37694409c1b8285427640d3acaec`
- required_parent: `b5129695ad65f66b9d43ac420d09593b61464d9a`
- predecessor_result_zip_sha256: `872b8c0051c5118ad3748b07ecf70df8689e4ba26891162a5fa58b1ce0da0b22`
- predecessor_done_task_sha256: `c9b2c3d2b212014e7df017b14246c960d177f9b1964bb92504c15fb0ebd99134`
- predecessor_result: `BLOCKED / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED`
- predecessor_executor_disposition: `ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED`
- blocker_classification: `REAL_INTEGRATION_SURFACE_GAP / P1_6_OWNER_API_NARROW_EXPANSION`
- fresh_IDE_chat_required: `No`
- governance_commit_authorized: `Yes / exact 3 paths / Commit A`
- result_commit_authorized: `Yes / exact expanded allowlist / Commit B`
- p1_6_semantic_baseline_mutation_authorized: `No`
- evidence_owner_source_mutation_authorized: `Yes / repository.py + optional ports.py only`
- canonical_durable_baseline_mutation_authorized: `Yes / exact 4 paths`
- migration_creation_authorized: `Yes / exact one migration`
- isolated_PostgreSQL_authorized: `Yes / task-owned ephemeral only`
- Docker_authorized: `Yes / local postgres:17.6 only`
- external_network_authorized: `No`
- provider_LLM_authorized: `No`
- retained_private_DB_authorized: `No`
- actual_self_dogfood_golden_cycle_authorized: `No`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. Browser judgment of 1108

1108 result independently verified:

```text
ZIP SHA-256:
872b8c0051c5118ad3748b07ecf70df8689e4ba26891162a5fa58b1ce0da0b22

40 members
39 manifest rows
one top-level directory
CRC PASS
all manifest size/SHA exact
Task/Cycle/Judgment byte-exact
```

1108 result:

```text
BLOCKED / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

Executor behavior:

```text
ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED
```

Governance Commit A:

```text
325a9044cb0a37694409c1b8285427640d3acaec

parent:
b5129695ad65f66b9d43ac420d09593b61464d9a

message:
docs(aiscc): record p1-8 currentness verifier blocker
```

1108 produced a truthful five-path partial candidate, no baseline adoption, no migration 0009, no READY implementation and no Result Commit B.

This Task PRESERVES and CONTINUES the partial candidate. Do not reset it.

# 1. blocker classification

The new blocker is accepted as a real P1-6 integration-surface gap, not a P1-6 semantic redesign.

Accepted P1-6 already owns:

```text
immutable RequirementSet / EvidenceRequirement / EvidenceCheckpoint authority
checkpoint-specific applicability
revocation/supersession/correction currentness
restart durability
EvidenceSetSatisfactionAttestation
G_EVIDENCE
```

The missing surface is narrower:

```text
pre-WorkRun
read-only
caller-transaction-bound
definition-graph verification
```

for an exact existing RequirementSet/checkpoint binding.

This Task authorizes exposing EXISTING P1-6 definition/currentness semantics only.

It does NOT authorize:

```text
new evidence semantics
new requirement/checkpoint types
new evidence profile
new G_EVIDENCE semantics
new satisfaction/evaluation semantics
new P1-6 table
fake WorkRun/evaluation/attestation
```

# 2. accepted design / predecessor evidence

Package accepted design SHA-256:

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

Predecessor evidence SHA-256:

- `SOURCE_CHANGE_REVIEW.md`: `77cf2ccf7eb0220e725078ce7fa0fb63d7b8f90b4502123cacdbb4d65ff3e5e7`
- `WORKSPACE_VERIFICATION.md`: `9f162e16a2f90c894ca68988b4ea0f8c92ae386b8b3134a7e1bd2054818de02c`
- `P1_8_CURRENTNESS_API_EVIDENCE.md`: `82fca8ecce3b4d232d16851515904cb4eaae2dbfb02ebcd457c32a16b7edc099`
- `P1_8_CURRENTNESS_LOCK_ORDER_REVIEW.md`: `928a4f0b25ab69b3cc083076ca669b4b57b2a6ca57c1f0d94a5ba294b7c24e9d`

Copy these only into:

```text
.aiassistant/reports/target/20260914_1131_aiscc-p2-4-p1-6-definition-resolver-scope-expanded-durable-taskcontract-implementation-retry-1/accepted-input/
```

after reading the Task.

Predecessor reports are diagnostic evidence, not authority.

Any package/hash mismatch -> `BLOCKED_MISSING_ARTIFACT`.

# 3. exact dirty-workspace continuation preflight

This is an AUTHORIZED PARTIAL-CANDIDATE continuation.

Require:

```text
branch:
main

HEAD:
325a9044cb0a37694409c1b8285427640d3acaec

HEAD^:
b5129695ad65f66b9d43ac420d09593b61464d9a

index:
empty
```

Expected Git-visible dirt EXACTLY:

### tracked modified

```text
src/aiscc/next_action/repository.py
src/aiscc/task_authority/ports.py
src/aiscc/task_authority/repository.py
tests/integration/memory/test_postgres_project_memory_next_action.py
```

### untracked

```text
src/aiscc/task_authority/contracts.py
.aiassistant/tasks/done/20260914_1108_aiscc-p2-4-p1-8-currentness-verifier-scope-expanded-durable-taskcontract-implementation-retry-1.md
```

Expected SHA-256:

- `src/aiscc/next_action/repository.py`: `a5e4dc078e33ed34b6f2353e16d80f98e3218b9c3443eb75f81a616748afa932`
- `src/aiscc/task_authority/ports.py`: `d817eabbf0e1c6ba0b3eacde3cd196a334938734f640f90e6202efca93870be9`
- `src/aiscc/task_authority/repository.py`: `2d24617a4e2435dd674b16c6e97c6bc30b8ae4338b445eca51d7c0f46909691a`
- `src/aiscc/task_authority/contracts.py`: `27cc0d1ee39f9609724f6ae2eaa03b22158c5ff794c51468a1e2dca8cb37bf29`
- `tests/integration/memory/test_postgres_project_memory_next_action.py`: `e4be970d608aac379bf7621ce222a6c2ec5d99a30d7a2aa20f421e4e618a60bb`

Current predecessor done Task:

```text
c9b2c3d2b212014e7df017b14246c960d177f9b1964bb92504c15fb0ebd99134
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

Current read-only P1-6 source preflight:

```text
src/aiscc/evidence/repository.py
27fb4c98be3ba4dc6f472ab62dba1ee3573dbc42587fbd44152c25310aeb94d8

src/aiscc/evidence/requirements.py
e87783aba7bc1323754c27e52b95f15528a3ae35394c0edd083bb4ef84752080

src/aiscc/evidence/ports.py
6bbe62f4c87ad437db202514640de850813c64b26bafc13d19fe66eda4f9d5ed
```

Any unexpected dirt/hash mismatch -> `DIRTY_WORKSPACE_MIXED` or `POLICY_CONFLICT_INVESTIGATION_REQUIRED`; STOP.

Do NOT clean/reset the accepted partial candidate.

# 4. exact executables

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

# 5. inbound placement and Governance Commit A

Transport:

```text
verify ZIP/hash/archive/path safety
→ place current Task into .aiassistant/tasks/active
→ read Task
→ verify accepted inputs / partial workspace
→ place Cycle/Judgment
```

Canonical:

```text
20260914_1131_aiscc-p2-4-p1-6-definition-resolver-gap-scope-expanded-retry-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_1131_aiscc-p2-4-1108-p1-6-definition-resolver-scope-expansion-authorization-1.md
-> .aiassistant/reports/aiscc/
```

Before Commit A, preserve five partial source/test paths unstaged.

Stage EXACTLY:

```text
.aiassistant/tasks/done/20260914_1108_aiscc-p2-4-p1-8-currentness-verifier-scope-expanded-durable-taskcontract-implementation-retry-1.md
.aiassistant/records/aiscc/cycles/20260914_1131_aiscc-p2-4-p1-6-definition-resolver-gap-scope-expanded-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_1131_aiscc-p2-4-1108-p1-6-definition-resolver-scope-expansion-authorization-1.md
```

Commit exactly:

```text
docs(aiscc): record p1-6 definition resolver blocker
```

Require:

```text
Commit A parent = 325a9044cb0a37694409c1b8285427640d3acaec
changed paths = exact 3
index empty
```

After Commit A, the five partial source/test paths must remain byte-exact until intentionally continued.

# 6. mandatory source audit before P1-6 mutation

Read:

```text
src/aiscc/evidence/repository.py
src/aiscc/evidence/requirements.py
src/aiscc/evidence/ports.py
src/aiscc/evidence/models.py
src/aiscc/persistence/models.py
directly affected P1-6 tests
```

Confirm exact existing owner graph:

```text
RequirementSet
EvidenceRequirement
EvidenceCheckpoint
authority registration/events/snapshots
revocation/supersession/correction
historical definition graph
```

Confirm the pre-WorkRun resolver can be exposed WITHOUT:

```text
fabricating WorkRun
fabricating evaluation
fabricating attestation
using G_EVIDENCE as definition proof
changing checkpoint applicability semantics
```

If existing internals cannot support a read-only definition resolver without semantic change:

```text
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

STOP.

# 7. exact P1-6 owner API expansion

Primary authorized mutation:

```text
src/aiscc/evidence/repository.py
```

Optional only if current architecture requires an existing public protocol/port surface:

```text
src/aiscc/evidence/ports.py
```

No other `src/aiscc/evidence/**` mutation is authorized.

Expose ONE public owner API that verifies an existing exact requirement definition graph before WorkRun execution.

Naming must follow existing repository conventions; do not create a parallel repository/service.

The resolver MUST:

1. accept caller-owned `AsyncSession`;
2. require an active caller transaction;
3. not open/commit/rollback/close a separate session;
4. be non-mutating: no INSERT/UPDATE/DELETE, no repair/rebuild;
5. accept exact expected Task/RequirementSet/checkpoint identities and fingerprints as equality claims only;
6. load owner-durable requirement-set / requirement / checkpoint / authority-event/snapshot rows using existing P1-6 definitions;
7. reconstruct/verify the canonical owner definition graph using existing private/internal graph logic factored safely if needed;
8. verify exact `task_id` / requirement-set scope;
9. verify exact RequirementSet fingerprint;
10. verify every referenced Requirement fingerprint/profile/requiredness/reuse bound;
11. verify every referenced EvidenceCheckpoint identity/fingerprint/source/target-or-purpose binding;
12. verify ordered membership/completeness of the definition graph;
13. verify current authority revision and effective currentness;
14. deny revoked/superseded/corrected/stale graph;
15. deny missing/extra/wrong-fingerprint/wrong-task/wrong-checkpoint bindings;
16. verify durable restart state, not only in-memory `TaskContractEvidenceAuthority.recognizes`;
17. fail closed on historical corruption or projection/event inconsistency;
18. return only owner-derived immutable/typed data sufficient for TaskContract comparison;
19. create NO EvidenceCandidate, AdmittedEvidence, evaluation, attestation or G_EVIDENCE fact;
20. preserve all existing P1-6 owner semantics and exception taxonomy where possible.

# 8. definition authority vs satisfaction authority

The new API is ONLY:

```text
definition authority verification
```

It is NOT:

```text
evidence satisfaction
evidence admission
reuse consumption
Human evidence ingress
G_EVIDENCE
transition decision
```

TaskContract issuance may prove:

```text
this immutable evidence_binding points to a genuine current P1-6 requirement definition graph
```

It may NOT prove:

```text
requirements are already satisfied
evidence exists
a WorkRun can transition
```

READY may reverify definition currentness but still may not create `G_EVIDENCE`.

# 9. same-transaction composition

TaskContract issuance/verify must call P1-6 owner resolver with the SAME caller `AsyncSession`.

Expected composition:

```text
TaskContract issuance transaction
→ P1-8 verify_current_selection(session, ...)
→ P1-6 verify_requirement_definition_graph(session, ...)
→ durable TaskContract body/ref/event write
```

READY:

```text
P1-4 run transaction
→ TaskContract verify
→ P1-8 currentness verify
→ P1-6 requirement definition currentness verify
→ other existing owner checks
→ P1-4 alone admits READY mutation
```

Same transaction does not merge semantic owners.

# 10. lock order

Create:

```text
P1_6_DEFINITION_LOCK_ORDER_REVIEW.md
```

Inspect actual lock order across:

```text
P1-4 run/READY
TaskContract family
P1-8 project/currentness
P1-6 requirement-set/authority
```

Requirements:

- no new advisory namespace if existing P1-6 lock exists;
- no reverse lock order against current P1-6 writers/revocation/correction;
- resolver remains read-only;
- concurrent revocation/supersession/correction cannot pass stale proof;
- no deadlock-prone P1-8 <-> P1-6 inversion introduced.

If safe order cannot be established under allowed paths:

```text
LOCK_ORDER_SCOPE_REVIEW_REQUIRED
```

STOP.

# 11. authorized P1-6 tests

You may ADD these exact new test files:

```text
tests/unit/evidence/test_requirement_definition_resolver.py
tests/integration/evidence/test_requirement_definition_resolver.py
```

You may MODIFY an existing P1-6 test file only if it already directly owns repository authority/currentness behavior and the exact path is first recorded in `P1_6_TEST_INVENTORY.md`.

Maximum existing P1-6 test modifications:

```text
2 files
```

No unrelated evidence test refactor.

Required resolver tests:

```text
current exact graph PASS
wrong task_id DENY
wrong requirement-set fingerprint DENY
missing requirement DENY
extra/unbound requirement DENY
wrong requirement fingerprint/profile DENY
wrong checkpoint fingerprint DENY
wrong checkpoint source/target-purpose DENY
revoked graph DENY
superseded/corrected graph DENY
historically valid but non-current graph DENY
restart/reconstruction PASS
caller transaction identity PASS
no session creation/commit/rollback PASS
zero DML on PASS/DENY
concurrent revocation cannot pass stale proof
no evaluation/attestation/WorkRun/G_EVIDENCE created
```

# 12. preserve and complete 1108 P1-8 partial work

Do not restart P1-8 implementation from scratch.

Current partial P1-8 API is only a draft.

Complete all Task 1108 requirements:

```text
later policy revocation
later source/subject revocation as applicable
withdrawal
supersession/projection mismatch
wrong candidate/descriptor/source
historical-valid-but-not-current
caller-session reuse
zero mutation
concurrency/currentness race
lock-order proof
```

Keep:

```text
src/aiscc/next_action/repository.py
tests/integration/memory/test_postgres_project_memory_next_action.py
```

within the already-authorized 1108 scope.

The 12 PASS result is evidence only for those assertions; it is not final acceptance.

# 13. complete accepted durable TaskContract chain

After P1-6/P1-8 owner APIs are proven compatible, continue the SAME accepted design:

```text
0319 base
+ 0812 body_ref
+ 0902 Human/Judgment
+ 0940 template authority Outcome A
```

No redesign.

Implement/complete:

```text
TaskContractBodyV1
IssuedTaskContractV1
VerifiedTaskContractBindingV1
TaskContractBodyRow
issue/get/verify/revoke
current version lineage
restart verification
authority_refs
source_next_action
repository binding
evidence_binding
Human binding
Judgment binding
execution provenance
TaskContractReadyParticipant
```

Clean the 1108 partial Ruff failures as part of completing the candidate.

# 14. body_ref correction

Exact:

```text
body_ref =
task-contract-body:v1:sha256:
+ SHA256(JCS({
  "project_id": project_id,
  "contract_id": contract_id,
  "contract_version": n
}))
```

93 ASCII chars.

Content hash remains independent.

# 15. canonical baseline adoption

Create/modify only:

```text
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

Do NOT modify:

```text
AISCC_EVIDENCE_ADMISSION.md
AISCC_HUMAN_GATE_JUDGMENT.md
AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md
```

The durable-body baseline may state that it composes existing P1-6 definition authority via the public read-only resolver. It must NOT change P1-6 semantics.

# 16. exact expanded mutation allowlist

### canonical

```text
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

### P1-8

```text
src/aiscc/next_action/repository.py
tests/unit/next_action/test_next_action_domain.py
tests/integration/memory/test_postgres_project_memory_next_action.py
```

### P1-6 owner surface

```text
src/aiscc/evidence/repository.py
src/aiscc/evidence/ports.py
tests/unit/evidence/test_requirement_definition_resolver.py
tests/integration/evidence/test_requirement_definition_resolver.py
```

Plus at most two existing P1-6 direct owner tests recorded in `P1_6_TEST_INVENTORY.md`.

### TaskContract runtime

```text
src/aiscc/task_authority/contracts.py
src/aiscc/task_authority/authority.py
src/aiscc/task_authority/ports.py
src/aiscc/task_authority/repository.py
src/aiscc/task_authority/ready.py
src/aiscc/task_authority/__init__.py
src/aiscc/persistence/models.py
```

### migration

```text
migrations/versions/20260914_0009_task_contract_durable_bodies.py
```

### TaskContract tests

```text
tests/unit/task_authority/test_task_contract_body.py
tests/unit/task_authority/test_task_contract_issuance.py
tests/integration/task_authority/test_task_contract_durability.py
tests/integration/task_authority/test_task_contract_ready.py
```

READ-ONLY:

```text
src/aiscc/evidence/requirements.py
src/aiscc/evidence/models.py
src/aiscc/next_action/models.py
src/aiscc/next_action/__init__.py
src/aiscc/workflow/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/task_authority/models.py
```

If another source path is required -> `SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED`.

If P1-6/P1-8 semantics must change -> `AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED`.

# 17. migration

Require:

```text
single Alembic head = 20260901_0008
20260914_0009 absent
```

Create exactly accepted one-table additive migration:

```text
migrations/versions/20260914_0009_task_contract_durable_bodies.py
```

No evidence/next_action schema change.

# 18. isolated PostgreSQL 17.6 proof

Use local image only; no pull.

New Task-owned container example:

```text
aiscc-p2-4-taskcontract-1131-pg
```

Required complete proof includes all prior TaskContract cases PLUS:

### P1-8

```text
current exact selection PASS
revoked/withdrawn/superseded/stale DENY
same-session zero-mutation
concurrent invalidation cannot pass
```

### P1-6

```text
current exact definition graph PASS
wrong/missing/extra requirement DENY
wrong checkpoint/fingerprint/scope DENY
revoked/superseded/corrected graph DENY
restart PASS
same-session zero-mutation
concurrent revocation cannot pass stale proof
no WorkRun/evaluation/attestation/G_EVIDENCE created
```

### TaskContract

all accepted migration/body/ref/idempotency/concurrency/restart/immutability/downgrade/READY proofs from 1108 Task.

No private DB/provider/network/golden cycle.

# 19. test/static closure

All required tests PASS.

Run direct affected regressions:

```text
P1-6 evidence authority
P1-8 next-action authority
task_authority
P1-4 READY/transition
P1-7 Human/Judgment
```

Static must end:

```text
Ruff PASS
compile PASS
git diff --check PASS
UTF-8/control/fence PASS
```

The predecessor 27 Ruff findings MUST be resolved if their files remain changed.

# 20. Result Commit B

Only after complete PASS.

Commit message exactly:

```text
feat(aiscc): add durable taskcontract authority
```

Parent = Governance Commit A.

Commit all and only authorized product/canonical/migration/test paths actually changed.

No Commit B on any blocker.

# 21. report/export

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ACCEPTED_DESIGN_INPUT_VERIFICATION.md
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

Include changed project-relative files plus current Cycle/Judgment/done Task.

# 22. terminal repository boundary

Success:

```text
HEAD = Result Commit B
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1131_aiscc-p2-4-p1-6-definition-resolver-scope-expanded-durable-taskcontract-implementation-retry-1.md
```

Current Task active -> done byte-exact.

Legacy 1400 unchanged.
Canonical state hashes unchanged.

Blocked:

- no Result Commit B;
- preserve truthful partial work;
- do not broad-reset/clean.

# 23. mandatory stop

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

# 24. success ceiling

Complete PASS:

```text
P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do NOT perform/claim:

```text
actual self-dogfood golden cycle
P2_4_SELF_DOGFOOD_ENTRY_SOURCE_CANDIDATE
P2-4 ACCEPTED/CLOSED
```
