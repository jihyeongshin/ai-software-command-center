# 작업지시서: P1-8 Runtime Prerequisite Authority Expanded-Path Implementation Rework

## meta

- task_id: `20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1`
- created_at: `2026-09-02T02:32:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission Runtime`
- work_type: `RUNTIME_REWORK / ORCHESTRATION_IMPLEMENTATION / EVIDENCE_ADMISSION_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_8_PROJECT_MEMORY_CYCLE / CROSS_OWNER_PREREQUISITE_RUNTIME`
- expected_start_branch: `main`
- expected_start_head: `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
- accepted_joint_design_commit: `b271f98df7d53edd3d3bc418443ff192e7aa4cfb`
- terminal_governance_commit: `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
- predecessor_runtime_path_count: `19`
- predecessor_runtime_aggregate_sha256: `84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42`
- accepted_path_audit_task_sha256: `73b5beb16a882d391e174d2b29d8bebb36ebcf76cd95075d3313af8085bf171a`
- human_p1_8_runtime_verification: `HUMAN_PENDING`
- recommended_executor_session: `NEW_CHAT_REQUIRED_BY_HUMAN`
- session_open_owner: `HUMAN`
- git_commit: `FORBIDDEN`
- git_push: `FORBIDDEN`

---

# 1. 목적

Human이 이미 `JOINT_EXACT_BYTES`로 accept한 두 authority rule과 0050 source audit에서 확인한 실제
transaction/owner 경계를 사용하여 P1-8 runtime prerequisite authority reconciliation을 구현한다.

이번 Task는 2359에서 정확히 중단된 runtime rework를 **확장된 exact path boundary**로 재개한다.

성공 결과는 다음 candidate뿐이다.

```text
P1-8 Runtime:
REWORKED_CANDIDATE /
COMMAND_CENTER_REVIEW_REQUIRED /
HUMAN_PENDING
```

Executor는 runtime acceptance, Human acceptance, terminal judgment, Git persistence, P2/P3, deployment 또는
Public Live를 생성하지 않는다.

---

# 2. Command Center 판정과 선행 증거

0050 audit bundle에 대한 독립 검증:

```text
ZIP SHA-256:
ea3ef187632bb07f903b6283cfdc5cd10c7db09b70624be7d3fd74c26b6414c5

ZIP CRC/path/symlink safety:
PASS

manifest payload:
47 / 47 actual bytes and SHA-256 PASS

0050 Task SHA-256:
73b5beb16a882d391e174d2b29d8bebb36ebcf76cd95075d3313af8085bf171a

runtime:
19 paths
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
mutation by audit: 0
```

Command Center judgment:

```text
0050 audit:
ACCEPTED / CLOSED

PATH_BOUNDARY_AUDITED /
EXACT_EXPANDED_ALLOWLIST_APPROVED
```

The audit independently confirmed:

1. `PostgresTransitionRepository` is exported from `src/aiscc/persistence/__init__.py` and defined in
   `src/aiscc/persistence/repository.py`.
2. inherited `PostgresExecutionRepository.decide` owns one `session.begin` transaction containing request,
   evaluation, decision, owner participant, WorkRun projection, commit and rollback.
3. `WorkflowKernel` delegates and does not own persistence transaction.
4. no suitable existing production `EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY` writer owner exists.
5. P1-7 `CommandCenterAuthority` and P1-8 Cycle/Memory/NextAction are forbidden writer substitutes.
6. new `src/aiscc/task_authority/**` plus existing P1-4 transaction owner is the exact architecture direction.
7. no load-bearing alternative remains.

Command Center refinement:

```text
0050 proposal listed 35 boundary paths.
The actual mutation allowlist below contains 32 paths.

The following three paths are removed from mutation permission
and remain byte-immutable baselines:

migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py
migrations/versions/20260831_0007_p1_8_authority_contract_rework.py
src/aiscc/judgment/authority.py
```

---

# 3. session boundary

새 IDE Executor 채팅은 Human이 연다. Executor는 스스로 새 채팅을 열거나 전환할 수 없다.

새 채팅이 필요한 근거:

```text
predecessor work type:
DISCOVERY_AUDIT / SOURCE_EVIDENCE_EXPORT

current work type:
RUNTIME_REWORK /
ORCHESTRATION_IMPLEMENTATION /
EVIDENCE_ADMISSION_IMPLEMENTATION

implementation must consume the accepted audit result as a fixed boundary
without retaining read-only audit-turn assumptions
```

Human이 새 채팅을 열고 이 Task를 exact active path에 배치한 뒤에만 Executor가 시작한다.

---

# 4. authoritative identities

Accepted rules:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
SHA-256:
7cf27b77bb961280becfc55ecf8e71c9406da9b7b91df0d2697132c2655108db

.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
SHA-256:
8b19970629c55629df1560f2329b529992eceb86d5e4216baf0b7e78d3876960
```

Human decision:

```text
Accept
binding: JOINT_EXACT_BYTES
```

Verified lineage:

```text
683aaee84d1fc09e9371dd214efc3ff58b7225ee
-> b271f98df7d53edd3d3bc418443ff192e7aa4cfb
-> 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
```

Predecessor Tasks:

```text
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
SHA-256:
0795bd24b5d1b9531840424dbd7ba6c788fa08df3d19a21564e82250734fc1e7

.aiassistant/tasks/done/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
SHA-256:
ca616a7193a69aabd8d12f9e265152187e83806828edc7568f428669093a73b6

.aiassistant/tasks/done/20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1.md
SHA-256:
73b5beb16a882d391e174d2b29d8bebb36ebcf76cd95075d3313af8085bf171a
```

2359 requirements remain controlling except where this Task explicitly replaces its insufficient mutation boundary.

---

# 5. mandatory preflight

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Before mutation require:

```text
branch == main
HEAD == 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
Git index == empty

both accepted rules exact path/SHA == expected
2311 / 2359 / 0050 done Task exact path/SHA == expected

predecessor runtime:
19 paths
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42

unexpected dirty paths == 0
accepted governance dirty paths == 0
```

The following NEW paths must be absent before implementation:

```text
migrations/versions/20260901_0008_p1_8_prerequisite_authority_reconciliation.py
src/aiscc/contracts/canonical_json.py
src/aiscc/task_authority/__init__.py
src/aiscc/task_authority/authority.py
src/aiscc/task_authority/models.py
src/aiscc/task_authority/ports.py
src/aiscc/task_authority/repository.py
tests/integration/task_authority/test_postgres_external_task_authority.py
tests/unit/contracts/test_canonical_json.py
tests/unit/task_authority/test_external_task_authority_domain.py
```

If a NEW path already exists, do not overwrite or absorb it. Stop with exact inventory and:

```text
DIRTY_WORKSPACE_MIXED / UNEXPECTED_NEW_PATH_COLLISION
```

---

# 6. must read

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/records/aiscc/cycles/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md
.aiassistant/reports/aiscc/20260901_2155_aiscc-p1-8-prerequisite-authority-accepted-runtime-resume-handoff-1.md
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
.aiassistant/tasks/done/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
.aiassistant/tasks/done/20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1.md
```

Read the actual source files in section 7 before editing them. Do not bulk-read unrelated rules, records, source or logs.

---

# 7. exact mutation allowlist

Only these 32 product/test/migration paths may be created or modified.

```text
migrations/versions/20260901_0008_p1_8_prerequisite_authority_reconciliation.py
src/aiscc/contracts/canonical_json.py
src/aiscc/cycle/__init__.py
src/aiscc/cycle/models.py
src/aiscc/cycle/repository.py
src/aiscc/memory/__init__.py
src/aiscc/memory/models.py
src/aiscc/memory/repository.py
src/aiscc/next_action/__init__.py
src/aiscc/next_action/models.py
src/aiscc/next_action/repository.py
src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py
src/aiscc/task_authority/__init__.py
src/aiscc/task_authority/authority.py
src/aiscc/task_authority/models.py
src/aiscc/task_authority/ports.py
src/aiscc/task_authority/repository.py
src/aiscc/workflow/__init__.py
src/aiscc/workflow/guards.py
src/aiscc/workflow/models.py
src/aiscc/workflow/ports.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/memory/test_postgres_project_memory_next_action.py
tests/integration/task_authority/test_postgres_external_task_authority.py
tests/integration/workflow/test_postgres_kernel.py
tests/unit/contracts/test_canonical_json.py
tests/unit/cycle/test_project_memory_cycle_domain.py
tests/unit/next_action/test_next_action_domain.py
tests/unit/task_authority/test_external_task_authority_domain.py
tests/unit/workflow/test_state_machine.py
```

Current Task lifecycle and ignored target bundle are additionally allowed:

```text
.aiassistant/tasks/active/20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1.md
.aiassistant/tasks/done/20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1.md
.aiassistant/reports/target/20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1/**
```

If another production/test/migration path is materially required, stop before touching it:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED / RUNTIME_PATH_BOUNDARY_INSUFFICIENT
```

Do not shoehorn behavior into an allowed but semantically wrong owner.

---

# 8. exact immutable baselines

These paths may be read and tested but must remain byte-exact.

```text
migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py
migrations/versions/20260831_0007_p1_8_authority_contract_rework.py
src/aiscc/judgment/authority.py
src/aiscc/bootstrap.py
src/aiscc/api/app.py
src/aiscc/judgment/__init__.py
src/aiscc/judgment/models.py
src/aiscc/workflow/kernel.py
src/aiscc/workflow/evaluator.py
src/aiscc/workflow/matrix.py
src/aiscc/workflow/participants.py
src/aiscc/evidence/models.py
src/aiscc/evidence/content.py
src/aiscc/evidence/ports.py
```

Accepted rules, Cycles, handoff, predecessor done Tasks, state summary, decision register, next actions and project-source
artifacts also remain immutable.

---

# 9. implementation order

Implement in this dependency order unless an exact source dependency requires a narrower reordering.

1. shared JCS safe-integer canonicalization
2. external Task authority immutable models and read/verifier ports
3. private writer authority and PostgreSQL repository
4. persistence rows and additive 0008 migration
5. P1-4 blocker/resolved types, guards and mandatory transaction participant
6. Cycle TaskConstraint/context provenance and replay
7. Memory source derivation/current invalidation
8. NextAction catalog/descriptor/current selection/replay
9. targeted unit and PostgreSQL tests
10. complete repository regression/static/Alembic verification
11. final source inventory and export

Do not implement downstream consumers against temporary caller-provided or in-memory substitutes.

---

# 10. JCS safe-integer contract

Create `src/aiscc/contracts/canonical_json.py` as the shared lower-layer cross-contract implementation.

Required:

```text
UTF-8
NFC
JCS_RFC8785-compatible deterministic object serialization
integer-only for normative integer fields
minimum/maximum checks from each accepted schema
global normative ceiling = 9007199254740991
bool is not accepted as int
float is forbidden
NaN/Infinity are forbidden
unknown fields denied by exact schema validators
no arbitrary-precision lexical-hash dialect
no silent coercion
writer bytes == independent verifier bytes
```

A generic canonicalizer must not pretend to know schema fields. Exact model/schema validators reject unknown or
non-applicable fields before canonicalization.

Do not modify accepted P1-6 `src/aiscc/evidence/content.py` signed-64-bit carrier semantics. P1-6 carries exact bytes
and provenance; it does not own the new cross-owner semantic fingerprints.

All 22 accepted payload fingerprints from the accepted rules and 2359 Task must reproduce exactly.

---

# 11. external Task authority runtime

Create:

```text
src/aiscc/task_authority/__init__.py
src/aiscc/task_authority/models.py
src/aiscc/task_authority/ports.py
src/aiscc/task_authority/authority.py
src/aiscc/task_authority/repository.py
```

Owner:

```text
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
```

Implement both prospective owner extensions exactly:

```text
TASK_CONSTRAINT_AUTHORITY_V1
NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY_V1
```

Required properties:

- immutable refs, events, snapshots and fold results;
- exact accepted object/event/snapshot/source-contract fingerprints;
- `ISSUED / SUPERSEDED / REVOKED` exact folds;
- pure revoke has no replacement object and is terminal for the logical key in V1;
- authority-global contiguous event sequence;
- per-key contiguous effective sequence;
- certified complete global prefix `1..H` and exact ordered prefix root;
- atomic object/event/current-projection writes;
- restart-durable replay and historical original-H verification;
- latest certified-H current applicability;
- conflict/idempotency behavior from accepted rules;
- strict scope variants and forbidden/non-applicable fields;
- no caller/backfill/hash-only grandfathering.

Private boundary:

- `authority.py` owns the opaque live write capability and one repository binding;
- capability is not serialized, copied, environment-loaded, exposed by getter, default singleton or debug hook;
- `__init__.py` exports only immutable values and read/verifier protocols;
- repository/writer/capability are not re-exported;
- P1-8 receives read/verifier ports only;
- public callers cannot issue, supersede or revoke.

Durable rows/events/fingerprints/snapshots/issuer binding are historical identity; the process token is not.

---

# 12. additive persistence and migration

Create only:

```text
migrations/versions/20260901_0008_p1_8_prerequisite_authority_reconciliation.py
```

Required:

```text
revision = 20260901_0008
down_revision = 20260831_0007
single linear head
additive only
no 0006/0007 rewrite
no destructive predecessor rewrite
no synthetic historical backfill
no accepted-row mutation
```

Add exact rows, constraints, indexes and foreign/reference bindings required by:

- TaskConstraint object/event/current/snapshot;
- NextActionContext object/event/current;
- P1-4 blocker provenance/resolved attestation;
- P1-8 Cycle/Memory/NextAction external-owner bindings.

`src/aiscc/persistence/models.py` remains row mapping, not semantic authority.

---

# 13. P1-4 blocker atomic transaction

Existing ownership stays unchanged.

```text
semantic owner:
P1_4_SYSTEM_TRANSITION_AUTHORITY

canonical transaction:
src/aiscc/persistence/repository.py
PostgresExecutionRepository.decide
```

Implement exact accepted blocker taxonomy and fingerprints, including:

- one ACTIVE blocker per `(work_run_id, blocked_epoch)`;
- all seven accepted kind/reason pairs;
- invalid pair denied;
- `SECURITY_BOUNDARY` is non-resumable and permits only `BLOCKED -> FAILED` through `G_FAILURE_TERMINAL`;
- resumable target set is exactly `READY / HUMAN_REQUIRED / REWORK_REQUIRED`;
- typed `P1_4BlockerProvenanceV1` appended atomically with admission into `BLOCKED`;
- typed `P1_4BlockerResolvedAttestationV1` only for an admitted allowed resolution;
- denial produces no positive attestation;
- source object is independently verified through the blocker-enrolled verifier;
- historical blocker -> resolution transition -> later terminal relation is rederived.

The P1-4 owner-specific participant/writer must be mandatory for applicable transitions inside the repository
transaction. A public caller must not be able to omit it by passing `transaction_participant=None`.

Do not change `WorkflowKernel`, evaluator, matrix or generic composite participant semantics. Compose the built-in
owner behavior inside `src/aiscc/persistence/repository.py` using typed models/ports/guards.

Any participant, provenance, projection or failure-injector exception must roll back request/evaluation/decision,
blocker/attestation rows and WorkRun projection together.

---

# 14. Cycle / Memory / NextAction reconciliation

Implement the accepted rules and retained 2359 requirements without transferring authority.

## Cycle

- verifies original TaskConstraint ref/fingerprint and certified snapshot/H;
- verifies context introduction event/fingerprint and authoring H;
- persists exact refs/fingerprints/H and P1-8-owned relations;
- historical replay rederives original validity from original prefixes;
- latest events affect current applicability without rewriting history.

## Memory

- derives NEXT_ACTION_CONTEXT only from accepted P1-6 durable structured result plus independently resolved external owner object/event;
- equality-checks all accepted semantic fields;
- class/ordinal copies are equality-only and never Memory authority;
- verified external owner events invalidate CURRENT projection append-only and idempotently;
- same-content delayed admission cannot resurrect revoked source;
- independently valid same-content source is evaluated by its own graph.

## NextAction

- caller cannot define the catalog;
- template/placeholder is not an `ActionRef`;
- selected descriptor commits exact context ref/fingerprint/source-contract enrollment;
- external context owns `priority_class` and `critical_path_ordinal`;
- selection policy owns class-to-rank mapping `4 / 5 / 6`;
- Memory and descriptor copies are equality checks only;
- exact evaluation order from accepted rule is preserved;
- deterministic ranking tuple remains exactly six fields;
- current selection and historical replay independently resolve the owner graph;
- later staleness preserves historical identity but denies new current selection;
- `AFTER_TASK_ISSUANCE_P1_7` never substitutes for selection prerequisites.

P1-6 carrier acceptance, P1-7 Judgment and P1-4 TransitionDecision do not mint priority authority.

---

# 15. required tests

Fresh-run at minimum:

## unit

```text
tests/unit/contracts/test_canonical_json.py
tests/unit/task_authority/test_external_task_authority_domain.py
tests/unit/workflow/test_state_machine.py
tests/unit/cycle/test_project_memory_cycle_domain.py
tests/unit/next_action/test_next_action_domain.py
```

Cover:

- all 22 accepted writer/verifier fingerprints;
- safe maximum accepted, maximum+1 denied;
- bool/float/noncanonical/unknown/non-applicable fields denied;
- three TaskConstraint scopes;
- issue/supersede/revoke/snapshot/fold/gap/conflict/history;
- opaque capability inaccessible;
- blocker taxonomy/resumability/bindings;
- exact catalog/descriptor/ranking and authority non-substitution.

## PostgreSQL integration

```text
tests/integration/task_authority/test_postgres_external_task_authority.py
tests/integration/workflow/test_postgres_kernel.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/memory/test_postgres_project_memory_next_action.py
```

Cover:

- concurrency and sequence serialization;
- object/event/projection/snapshot atomicity;
- restart durability and historical replay;
- P1-4 source verification + decision/state/attestation atomicity;
- denial/no-attestation and both rollback failure cuts;
- P1-6 carrier does not mint semantic priority;
- P1-7 authority cannot issue external Task authority events;
- Cycle/Memory/NextAction currentness, invalidation and replay;
- migration upgrade, Alembic head/check.

## regression/static

```text
complete repository pytest collection
ruff
mypy src
alembic check
```

Record exact commands, collected/pass/fail/skip counts, PostgreSQL version, Alembic head, environment reuse/freshness
and Docker residue. Do not hide failures, deselect, reduce collection, or broadly convert failures to xfail.

No real provider/tool/network/credential action is required. If the required local test environment needs new
network or credential scope, stop with `EVIDENCE_SCOPE_EXPANSION_REQUIRED`.

---

# 16. mandatory stop

Stop rather than weakening the accepted contract when:

```text
required path falls outside the exact 32-path mutation allowlist
Task authority private capability cannot be enforced
P1-4 atomic behavior requires changing evaluator/matrix/kernel ownership
P1-6 semantic-contract extension appears necessary
P1-8 must mint external source semantics
P1-7 or P1-8 must receive external writer capability
accepted 22 fingerprints cannot be reproduced with JCS_RFC8785 and safe integers
migration requires predecessor rewrite/backfill/destructive change
current accepted historical bytes must be rewritten
unexpected dirty/new-path collision exists
```

Use the narrowest exact taxonomy:

```text
IMPLEMENTATION_BASELINE_GAP
POLICY_CONFLICT_INVESTIGATION_REQUIRED
LEGACY_PROVENANCE_REGRESSION
EVIDENCE_SCOPE_EXPANSION_REQUIRED
RUNTIME_PATH_BOUNDARY_INSUFFICIENT
```

After a named blocker perform only minimal evidence, final workspace inventory, report/export and safe stop.

---

# 17. Git and governance

```text
NO git add
NO commit
NO push/fetch/pull/remote
NO reset/restore/clean/checkout/rebase/merge/cherry-pick
```

Final HEAD must remain:

```text
1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
```

Do not update:

```text
.aiassistant/rules/**
.aiassistant/records/aiscc/**
.aiassistant/reports/aiscc/**
.aiassistant/project-sources/**
```

Move only the current Task active -> done after report/export completion. Human runtime verification remains
`HUMAN_PENDING`.

---

# 18. evidence contract

executor_required:

- `STATIC_SOURCE`: exact accepted identities, 22 fingerprints, owner/import boundary and final source inventory
- `UNIT_TEST`: domain/canonicalization/capability/negative contracts
- `INTEGRATION_TEST`: PostgreSQL durability/concurrency/replay/atomicity/restart
- `DATABASE_RUNTIME`: migration head/check and targeted PostgreSQL behavior
- `PUBLIC_PROVENANCE`: final candidate path/hash inventory, Task lifecycle, unchanged HEAD/index
- `SOURCE_EVIDENCE_EXPORT`: every final candidate source/test/migration path preserving repository-relative structure

reuse_allowed:

- accepted design and 2311/0050 audit only when exact path/SHA/commit identities match preflight
- predecessor 19 bytes only as implementation start point, never as proof of changed behavior

human_owned:

- P1-8 runtime final review: `HUMAN_PENDING`

not_required:

- browser/visual QA
- provider/tool real calls
- Project Source mirror
- deployment/Public Live
- P2/P3

forbidden:

- Agent-minted Human result or runtime acceptance
- proof-channel substitution
- remote/network/credential expansion
- Git persistence

---

# 19. accept criteria

All must pass:

1. exact preflight identities and no collision;
2. implementation stays within 32 exact paths;
3. all 22 accepted fingerprints reproduce writer == independent verifier;
4. external authority private writer/read-verifier boundary proven;
5. P1-4 blocker/attestation transaction atomicity proven;
6. Cycle/Memory/NextAction exact owner/currentness/replay contracts proven;
7. 0008 is additive, linear and verified;
8. targeted unit/PostgreSQL and complete regression/static verification pass;
9. no immutable baseline byte changes;
10. no unexpected final dirty path;
11. complete manifest and source export;
12. Human acceptance remains pending.

Successful executor taxonomy:

```text
P1-8 Runtime:
REWORKED_CANDIDATE /
COMMAND_CENTER_REVIEW_REQUIRED /
HUMAN_PENDING
```

Any test failure or contract mismatch is not hidden. Report the exact narrow blocker or `REWORKED_CANDIDATE_TEST_FAILED`.

---

# 20. target bundle

Target:

```text
.aiassistant/reports/target/20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
RUNTIME_INVENTORY.md
FINGERPRINT_EVIDENCE.md
TEST_EVIDENCE.md
MIGRATION_EVIDENCE.md
```

Include:

- every final candidate source/test/migration file preserving repository-relative paths;
- current done Task;
- 0050 done Task;
- exact evidence summaries.

Do not include secrets, credentials, DB dumps, `.git`, browser mirror or unrelated source.

Manifest excludes itself and lists every payload path, bytes, copy SHA-256, exact source path, source SHA-256 and
match result.

---

# 21. report required fields

1. task/result/target path
2. Task source placement, active->done lifecycle and SHA
3. branch/HEAD/index preflight and final
4. accepted rule/commit/2311/2359/0050 identities
5. predecessor and final runtime path count/aggregate
6. automatically discovered vs explicitly read instructions
7. exact files added/modified/unchanged
8. immutable baseline byte verification
9. JCS/safe-integer implementation and 22 fingerprint table
10. TaskConstraint owner/capability/event/snapshot result
11. NEXT_ACTION_CONTEXT owner/capability/event/current result
12. P1-4 blocker/attestation atomic result
13. Cycle/Memory/NextAction result
14. migration/down-revision/Alembic result
15. exact test commands and counts
16. PostgreSQL/environment/Docker residue
17. source/migration/test mutation count
18. unexpected dirty/collision result
19. Human-owned status
20. forbidden-not-run
21. unverified items
22. rollback guide without execution
23. preserved exact paths
24. final taxonomy

---

# 22. preserved exact paths

Always preserve:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/records/aiscc/cycles/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md
.aiassistant/reports/aiscc/20260901_2155_aiscc-p1-8-prerequisite-authority-accepted-runtime-resume-handoff-1.md
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
.aiassistant/tasks/done/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
.aiassistant/tasks/done/20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1.md
migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py
migrations/versions/20260831_0007_p1_8_authority_contract_rework.py
src/aiscc/judgment/authority.py
```

Preserve predecessor candidate identity before mutation:

```text
19 paths
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

After implementation, report the new exact final candidate path set and aggregate. The target bundle is temporary
and deletable only after substantive Command Center review.

---

# 23. final response format

```text
result:
target bundle path:
Task done path / SHA-256:
branch / HEAD / index:
predecessor count / aggregate:
final count / aggregate:
added paths:
modified paths:
immutable paths verified:
22 fingerprints:
Task authority:
P1-4 atomicity:
Cycle / Memory / NextAction:
migration / Alembic:
tests:
Human verification:
unverified items:
preserved exact paths:
```

