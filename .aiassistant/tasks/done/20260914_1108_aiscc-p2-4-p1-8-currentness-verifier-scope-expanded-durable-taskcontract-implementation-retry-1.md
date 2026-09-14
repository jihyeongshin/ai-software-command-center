# 작업지시서: P2-4 P1-8 currentness verifier scope-expanded durable TaskContract implementation retry

## meta

- task_id: `20260914_1108_aiscc-p2-4-p1-8-currentness-verifier-scope-expanded-durable-taskcontract-implementation-retry-1`
- created_at: `2026-09-14T11:08:12+09:00`
- work_type: `OWNER_API_NARROW_EXPANSION + DOC_BASELINE_UPDATE + BACKEND_IMPLEMENTATION + DATABASE_MIGRATION + QA_ONLY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `b5129695ad65f66b9d43ac420d09593b61464d9a`
- required_parent: `f8193d83d032fc4a0a49d3471205ac693025e4f1`
- predecessor_result_zip_sha256: `590e1f55e56a7ee88a124935a0c5b3c0bdfafc78222236fe21d66764265651ef`
- predecessor_done_task_sha256: `cb3fbd3e3c2c52a00ed3702654d1d8763fa028bbfbc347f38775e96a5a268c85`
- predecessor_result: `BLOCKED / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED`
- predecessor_executor_disposition: `ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED`
- blocker_classification: `REAL_INTEGRATION_SURFACE_GAP / NOT_SEMANTIC_OWNER_CHANGE`
- fresh_IDE_chat_required: `No`
- governance_commit_authorized: `Yes / exact 3 paths / Commit A`
- result_commit_authorized: `Yes / exact expanded allowlist / Commit B`
- canonical_baseline_mutation_authorized: `Yes / exact 4 durable-body rule paths`
- p1_8_semantic_baseline_mutation_authorized: `No`
- next_action_owner_source_mutation_authorized: `Yes / repository.py only`
- migration_creation_authorized: `Yes / exact one migration`
- isolated_PostgreSQL_authorized: `Yes / task-owned ephemeral only`
- Docker_authorized: `Yes / local postgres:17.6 only`
- external_network_authorized: `No`
- provider_LLM_authorized: `No`
- retained_private_DB_authorized: `No`
- actual_self_dogfood_golden_cycle_authorized: `No`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. Browser judgment of 1052

1052 independently verified result:

```text
ZIP SHA-256:
590e1f55e56a7ee88a124935a0c5b3c0bdfafc78222236fe21d66764265651ef

33 members
32 manifest rows
one top-level directory
CRC PASS
all manifest row byte sizes/SHA exact
TASK byte-exact
```

1052 result:

```text
BLOCKED / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

Executor behavior:

```text
ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED
```

Governance Commit A:

```text
b5129695ad65f66b9d43ac420d09593b61464d9a
parent:
f8193d83d032fc4a0a49d3471205ac693025e4f1

message:
docs(aiscc): accept taskcontract template authority correction
```

No canonical durable-body adoption, migration, product/test implementation, PostgreSQL proof or Result Commit B occurred.

The blocker is accepted as a real implementation-surface gap:

```text
current P1-8 repository has no public,
non-mutating,
caller-transaction-bound verifier for an exact
current selection/candidate/descriptor/source lineage.
```

This does NOT reopen:

```text
0319 base durable-body design
0812 body_ref correction
0902 Human/Judgment correction
0940 template/approval Outcome A correction
```

It does NOT authorize changing P1-8 semantics.

# 1. accepted design and predecessor evidence

After reading this Task, stage package inputs only under:

```text
.aiassistant/reports/target/20260914_1108_aiscc-p2-4-p1-8-currentness-verifier-scope-expanded-durable-taskcontract-implementation-retry-1/accepted-input/
```

Accepted design SHA-256:

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

Predecessor diagnostic evidence:

```text
PREDECESSOR_EVIDENCE/SOURCE_CHANGE_REVIEW.md
SHA-256:
94069a1d4e1bdd8b2acd5b537542b847f6c8af34c26d34b3d6ed38e6de6e12bf

PREDECESSOR_EVIDENCE/WORKSPACE_VERIFICATION.md
SHA-256:
a66470b2859cf74bd178b64bb422b10712ece78c55596dd5a61b32681347111a
```

Predecessor reports are diagnostic evidence, not canonical authority.

Any package member/hash mismatch:

```text
BLOCKED_MISSING_ARTIFACT
```

STOP before governance/product mutation.

# 2. exact initial repository preflight

Require before governance mutation:

```text
branch:
main

HEAD:
b5129695ad65f66b9d43ac420d09593b61464d9a

HEAD^:
f8193d83d032fc4a0a49d3471205ac693025e4f1

index:
empty

tracked:
clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_1052_aiscc-p2-4-taskcontract-durable-body-full-corrected-runtime-implementation-retry-1.md

SHA-256:
cb3fbd3e3c2c52a00ed3702654d1d8763fa028bbfbc347f38775e96a5a268c85
```

Preserve ignored legacy Task:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md

SHA-256:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Canonical state initially and terminally exact:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48

.aiassistant/records/aiscc/DECISION_REGISTER.md
9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5

.aiassistant/records/aiscc/NEXT_ACTIONS.md
050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679
```

Required unchanged source hashes at preflight:

```text
src/aiscc/next_action/models.py
09d5c13d73f2bb1cd4ef05433f73f40eedcb670353dcfae9cdbf480420af1ea6

src/aiscc/next_action/repository.py
51a44c9d28a374aea1359e41752e5ff02fdb21f89844ae61e082707906e213f7

src/aiscc/next_action/__init__.py
c1e8cadee709b6ba289fa9f92ed2eeaa04e51444e3a9ff85f2fc97138c42172d

src/aiscc/task_authority/authority.py
76fe0027ca2d652efd8a9fe204408d23751aa23175c369a5bc6ce389ba3af165

src/aiscc/task_authority/ports.py
991ad83420947a35021d6acfcc4ef0bc150d5112582e69b740698374eb8b68e8

src/aiscc/task_authority/repository.py
5de5faf4a7d60c83b181588d691ce36006469095b3e16aa449881ad14143f745

src/aiscc/workflow/participants.py
23f565bc4aaf006868aa27fc7726844d03461d59062c59b385c19f80811d116c
```

Mismatch -> `POLICY_CONFLICT_INVESTIGATION_REQUIRED` and STOP.

# 3. exact executables

Use only:

```text
Python:
<repository-root>\.venv\Scripts\python.exe

Git:
C:\Program Files\Git\cmd\git.exe

Docker:
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

Docker only for section 17 isolated PostgreSQL proof.

# 4. inbound placement

Order:

```text
verify ZIP/hash/archive/member safety
→ place current Task into .aiassistant/tasks/active
→ read Task
→ verify/stage accepted design + predecessor evidence
→ place Cycle/Judgment canonical governance artifacts
```

Canonical placement:

```text
20260914_1108_aiscc-p2-4-p1-8-currentness-verifier-gap-scope-expanded-retry-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_1108_aiscc-p2-4-1052-currentness-verifier-scope-expansion-authorization-1.md
-> .aiassistant/reports/aiscc/
```

# 5. Governance Commit A

Before Commit A Git-visible untracked exactly:

```text
.aiassistant/tasks/done/20260914_1052_aiscc-p2-4-taskcontract-durable-body-full-corrected-runtime-implementation-retry-1.md
.aiassistant/records/aiscc/cycles/20260914_1108_aiscc-p2-4-p1-8-currentness-verifier-gap-scope-expanded-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_1108_aiscc-p2-4-1052-currentness-verifier-scope-expansion-authorization-1.md
```

Stage exactly those three.

Commit message exactly:

```text
docs(aiscc): record p1-8 currentness verifier blocker
```

Require:

```text
Commit A parent = b5129695ad65f66b9d43ac420d09593b61464d9a
changed paths = exact 3
index empty
tracked clean
Git-visible untracked = 0
```

No product/canonical mutation before this commit.

# 6. current source fact admitted from 1052

Current public P1-8 repository methods include:

```text
enroll_configured_authority
select
apply_owner_event
reconcile_external_context_event
replay
rebuild_projection
```

1052 established:

```text
replay:
historical replay only; owns its own session

select existing-ID retry:
can return historical pair before fresh current-policy checks

rebuild_projection:
mutating repair/projection operation

recognizes_descriptor:
descriptor identity recognition only, not durable current selection proof

private current-policy/current-subject helpers:
not a complete public cross-owner currentness contract
```

Do NOT use any of these as a semantic substitute for the missing owner API.

# 7. exact P1-8 owner API expansion — authorized

Modify only:

```text
src/aiscc/next_action/repository.py
```

within the P1-8 owner domain to expose ONE public, non-mutating verifier for an exact already-existing selection lineage.

Do not modify `models.py` or add a new semantic owner/model.

Method name/signature should reuse existing repository/domain types and current naming conventions. Do not create a parallel repository.

The new public owner method MUST:

1. accept/use the caller-owned `AsyncSession`;
2. never open, commit, rollback, or close a separate session;
3. never call `select(...)` to create/reselect authority;
4. never call `rebuild_projection(...)`;
5. never insert/update/delete owner rows;
6. verify historical event/replay integrity using existing owner logic;
7. verify the durable current projection identifies the expected current selection;
8. verify exact selected candidate/action/descriptor/source lineage matches the caller's expected existing identity;
9. verify current policy/config/source/subject/descriptor enrollment/revocation/currentness at the current owner state, not only at original issuance high-watermark;
10. fail closed for later revocation, withdrawal, supersession, projection mismatch, stale selection, wrong candidate/descriptor/source, or authority corruption;
11. reuse existing owner lock/currentness primitives and existing exception taxonomy where possible;
12. not expose private DB rows as caller authority;
13. not mint a new selection/candidate/descriptor/ref;
14. not accept caller booleans such as `is_current=True`;
15. return only existing typed/owner-derived data sufficient for TaskContract issuance/READY comparison.

No new:

```text
RuntimeMode
ActionDescriptor kind
source kind
TaskIssuanceCandidate semantic
template owner
selection policy
currentness definition
projection semantics
```

is authorized.

# 8. same-transaction composition

The P1-8 verifier exists specifically so:

```text
TaskContract issuance
and
TaskContractReadyParticipant.prepare(...)
```

can verify current P1-8 authority in the same caller transaction as their own admission work.

At READY:

```text
P1-4 participant receives caller AsyncSession
→ durable TaskContract verifier
→ P1-8 public current-selection verifier using same session
→ owner-backed comparisons
→ P1-4 remains sole WorkflowState mutation owner
```

Do not claim that same transaction means same semantic owner.

P1-8 remains the only owner of NextAction currentness.

# 9. lock/concurrency boundary

Before implementation, inspect exact existing lock order used by:

```text
P1-4 READY
TaskContract family issuance/verification
P1-8 selection/current projection
```

Document the chosen composition in:

```text
P1_8_CURRENTNESS_LOCK_ORDER_REVIEW.md
```

Required:

- no new cross-domain advisory-lock namespace;
- reuse existing owner lock primitives;
- no inverse lock acquisition path introduced by the new verifier;
- verifier must be read-only even when locks are acquired;
- concurrency test must prove stale/withdrawn/revoked/superseded selection cannot pass.

If exact current owner lock order cannot be composed safely within allowed paths:

```text
LOCK_ORDER_SCOPE_REVIEW_REQUIRED
```

STOP before semantic workaround.

# 10. P1-8 tests — newly authorized exact paths

Mutation allowed:

```text
tests/unit/next_action/test_next_action_domain.py
tests/integration/memory/test_postgres_project_memory_next_action.py
```

These existing owner-focused tests are authorized only for the new verifier/currentness composition.

Do not refactor unrelated P1-8 tests.

Required P1-8 API proofs:

```text
current exact selection PASS
wrong selection DENY
withdrawn selection DENY
superseded/current projection mismatch DENY
later policy revocation DENY
later source/subject authority revocation DENY where current source semantics apply
wrong candidate DENY
wrong descriptor/source lineage DENY
historical replay-valid but not current DENY
caller-owned transaction reused
no commit/rollback/session creation by verifier
zero row mutation on verification PASS/DENY
concurrent owner change cannot be admitted as current
```

# 11. canonical durable-body baseline adoption

After P1-8 owner API design/static proof is compatible, create/modify only:

```text
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

Do NOT change P1-8 semantic rules.

The baseline may document only that durable TaskContract issuance/READY composes the existing P1-8 currentness owner through its public non-mutating verifier.

Do NOT modify:

```text
AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
AISCC_HUMAN_GATE_JUDGMENT.md
AISCC_EVIDENCE_ADMISSION.md
CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md
```

# 12. full accepted design chain

Implement without redesign:

```text
0319 durable-body base
+ 0812 body_ref correction
+ 0902 Human/Judgment correction
+ 0940 template/approval Outcome A correction
```

Key non-substitution remains:

```text
P1-8 current selection/descriptor != TaskContract
TaskIssuanceCandidate != TaskContract
TaskContract config != HumanResult/Judgment
body_sha256 != owner approval
NONE/null != authority
Judgment != TransitionDecision
```

# 13. body identity / durable authority

Preserve exact 0812 identity:

```text
body_ref =
task-contract-body:v1:sha256:
+ SHA256(JCS({
    "project_id": project_id,
    "contract_id": contract_id,
    "contract_version": n
  }))
```

Exact 93 ASCII chars.

Content fingerprint separate:

```text
body_sha256 = SHA256(canonical_body)
constraint_payload_ref = body_ref
constraint_payload_fingerprint = body_sha256
```

Implement:

```text
TaskContractBodyV1
IssuedTaskContractV1
VerifiedTaskContractBindingV1
TaskContractBodyRow
```

with all accepted validation/version/revoke/idempotency/restart/corruption semantics.

# 14. Human/Judgment/template authority corrections

Human/Judgment:

```text
TaskContract stores immutable owner-consumable config only.
Existing P1-7/Judgment owner creates runtime fingerprints/gates/results/Judgments.
```

Template Outcome A:

```text
catalog task_template_ref/hash NONE/null
= no separate template provenance
!= authorization
```

Complete body still requires explicit authorization by:

```text
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
```

and current P1-8 verifier from section 7.

`authority_refs` corrected semantics remain exactly the 0940 accepted proposal.

# 15. exact expanded mutation allowlist

Canonical:

```text
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

P1-8 owner API:

```text
src/aiscc/next_action/repository.py
```

Durable TaskContract runtime:

```text
src/aiscc/task_authority/contracts.py
src/aiscc/task_authority/authority.py
src/aiscc/task_authority/ports.py
src/aiscc/task_authority/repository.py
src/aiscc/task_authority/ready.py
src/aiscc/task_authority/__init__.py
src/aiscc/persistence/models.py
```

Migration:

```text
migrations/versions/20260914_0009_task_contract_durable_bodies.py
```

TaskContract tests:

```text
tests/unit/task_authority/test_task_contract_body.py
tests/unit/task_authority/test_task_contract_issuance.py
tests/integration/task_authority/test_task_contract_durability.py
tests/integration/task_authority/test_task_contract_ready.py
```

P1-8 verifier tests:

```text
tests/unit/next_action/test_next_action_domain.py
tests/integration/memory/test_postgres_project_memory_next_action.py
```

READ-ONLY / MUST NOT MODIFY:

```text
src/aiscc/next_action/models.py
src/aiscc/next_action/__init__.py
src/aiscc/workflow/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/evidence/**
src/aiscc/task_authority/models.py
```

If another mutation path is genuinely required:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

If P1-8 semantics/authority definition must change rather than expose existing semantics:

```text
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

STOP.

# 16. migration

Require before creation:

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

Use the already accepted additive one-table immutable design.

No P1-8 schema/table migration is authorized.

# 17. isolated PostgreSQL 17.6 proof

First:

```text
"C:\Program Files\Docker\Docker\resources\bin\docker.exe" image inspect postgres:17.6
```

If absent: `ISOLATED_POSTGRES_IMAGE_MISSING`, no pull.

Use one new Task-owned disposable container only, e.g.:

```text
aiscc-p2-4-taskcontract-1108-pg
```

Synthetic credentials; bind `127.0.0.1` only.

Run all previously required durable-body proofs plus:

```text
P1-8 current selection verifier on real PostgreSQL owner rows
same AsyncSession/transaction composition
current selection PASS
historical-but-withdrawn DENY
later policy/source authority revocation DENY as applicable
projection mismatch DENY
zero mutation by verifier
concurrent currentness change cannot pass stale proof
READY transaction uses owner verifier without rebuilding/reselecting
```

No retained/private DB, network/provider.

Cleanup exact Task container best-effort only.

# 18. tests/static

All modified/new tests PASS.

Run affected existing regressions for:

```text
next_action/P1-8
task_authority
P1-4 READY/transition
P1-7 Human/Judgment
```

No unrelated broad suite solely for padding.

Static:

```text
Ruff changed Python
compile changed Python
git diff --check
UTF-8/control/fence checks changed canonical docs
```

# 19. forbidden

Forbidden:

```text
modify next_action/models.py
modify next_action/__init__.py
modify workflow/**
modify human/**
modify judgment/**
modify evidence/**
modify task_authority/models.py
change P1-8 currentness semantics
new P1-8 source kind/descriptor type/selection policy
new template/approval registry/table
use rebuild_projection as verification
use select retry as verification
use historical replay alone as currentness
copy P1-8 currentness SQL/logic into task_authority
caller-provided currentness boolean
actual self-dogfood golden cycle
src/aiscc/self_dogfood/** mutation
CURRENT_STATE_SUMMARY/DECISION_REGISTER/NEXT_ACTIONS mutation
external network/provider
Docker pull
retained/private DB
push/deploy/automatic merge
```

# 20. Result Commit B

Only after complete PASS.

Stage exact changed paths within section 15.

Commit message exactly:

```text
feat(aiscc): add durable taskcontract authority
```

Require:

```text
Commit B parent = Governance Commit A
no path outside expanded allowlist
index empty
tracked clean
```

No Commit B on blocker/failure.

# 21. report/export

Target:

```text
.aiassistant/reports/target/20260914_1108_aiscc-p2-4-p1-8-currentness-verifier-scope-expanded-durable-taskcontract-implementation-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ACCEPTED_DESIGN_INPUT_VERIFICATION.md
P1_8_CURRENTNESS_API_EVIDENCE.md
P1_8_CURRENTNESS_LOCK_ORDER_REVIEW.md
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

Include changed project-relative files plus canonical current Cycle/Judgment/done Task.

No raw DB dump/credentials/unrelated source.

# 22. terminal repository boundary

Success:

```text
HEAD = Result Commit B
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1108_aiscc-p2-4-p1-8-currentness-verifier-scope-expanded-durable-taskcontract-implementation-retry-1.md
```

Current Task active -> done byte-identical.

Legacy 1400 exact unchanged.

Canonical state hashes unchanged.

Blocked/failure:

- no Result Commit B;
- preserve truthful Task-owned evidence/changes;
- no broad reset/cleanup.

# 23. mandatory stop

Named blockers:

```text
BLOCKED_MISSING_ARTIFACT
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

Complete PASS may report only:

```text
P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do NOT perform or claim actual self-dogfood golden cycle or P2-4 closure.
