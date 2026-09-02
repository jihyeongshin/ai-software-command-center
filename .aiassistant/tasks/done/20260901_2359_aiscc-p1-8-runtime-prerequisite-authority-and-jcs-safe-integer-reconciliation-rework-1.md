# 작업지시서: P1-8 Runtime Prerequisite Authority and JCS Safe-Integer Reconciliation Rework

## meta

- task_id: `20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1`
- created_at: `2026-09-01T23:59:00+09:00`
- phase: `P1-8 Project Memory and Cycle Admission Runtime`
- work_type: `RUNTIME_REWORK / ORCHESTRATION_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_8_PROJECT_MEMORY_CYCLE / CROSS_OWNER_PREREQUISITE_RUNTIME`
- expected_start_branch: `main`
- expected_start_head: `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
- accepted_joint_design_commit: `b271f98df7d53edd3d3bc418443ff192e7aa4cfb`
- terminal_governance_commit: `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
- predecessor_runtime_path_count: `19`
- predecessor_runtime_aggregate_sha256: `84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42`
- human_p1_8_runtime_verification: `HUMAN_PENDING`
- recommended_executor_session: `NEW_CHAT_REQUIRED_BY_HUMAN`
- session_open_owner: `HUMAN`
- git_commit: `FORBIDDEN`
- git_push: `FORBIDDEN`

---

# 1. purpose

Rework the exact preserved P1-8 runtime candidate against the jointly Human-accepted prerequisite authority and
JCS-safe-integer contracts.

This Task resumes runtime implementation only after the terminal Git lineage was independently verified by:

```text
20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1

result:
STATE_A_VERIFIED
```

The start point is exact:

```text
19 runtime paths
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

The existing bytes are uncommitted and unaccepted. They may be modified only within this Task's exact mutation
allowlist. The accepted design rules, terminal governance, historical commits, Cycles and handoff remain immutable.

Successful execution produces only:

```text
P1-8 Runtime:
REWORKED_CANDIDATE / COMMAND_CENTER_REVIEW_REQUIRED / HUMAN_PENDING
```

It does not produce runtime acceptance, Git persistence, P2/P3, deployment, or Public Live.

---

# 2. session boundary

The Human opens a new IDE Executor chat before providing the short prompt.

Reason:

```text
the predecessor turn was SOURCE_EVIDENCE_EXPORT / QA_ONLY
this Task changes work type to RUNTIME_REWORK / ORCHESTRATION_IMPLEMENTATION
the runtime must consume the verified canonical result rather than retain audit-turn assumptions
```

The Executor does not create or switch chat sessions. It begins only after the Human has opened the session and
placed this Task through the declared transport prompt.

---

# 3. accepted authority identities

Require exact clean committed rules:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
SHA-256:
7cf27b77bb961280becfc55ecf8e71c9406da9b7b91df0d2697132c2655108db

.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
SHA-256:
8b19970629c55629df1560f2329b529992eceb86d5e4216baf0b7e78d3876960
```

Human exact decision:

```text
Accept
binding: JOINT_EXACT_BYTES
```

Verified terminal lineage:

```text
683aaee84d1fc09e9371dd214efc3ff58b7225ee
→ b271f98df7d53edd3d3bc418443ff192e7aa4cfb
→ 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
```

The 2311 audit independently recomputed all three commit objects, parents, messages, Commit A exact 2 paths,
Commit B exact 10 paths, and all 12 committed blob identities.

---

# 4. mandatory preflight

Before mutation require:

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a

index:
empty
```

Require:

```text
accepted rule paths clean against HEAD
terminal governance paths clean against HEAD
Commit A object and exact two blobs present
```

Require exact predecessor runtime inventory from section 7:

```text
19 paths
aggregate SHA-256:
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42

status classification:
5 modified tracked + 14 untracked runtime paths
```

Require exact uncommitted governance input:

```text
.aiassistant/tasks/done/
20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md

SHA-256:
0795bd24b5d1b9531840424dbd7ba6c788fa08df3d19a21564e82250734fc1e7
```

The current active Task and ignored target paths are excluded from tracked dirty classification.

If HEAD, index, rules, Commit A, runtime path identity/aggregate, 2311 done Task, or unexpected dirty inventory
differs, do not reset/clean/restore/checkout. Stop with:

```text
RUNTIME_RECONCILIATION_PREFLIGHT_MISMATCH
```

---

# 5. minimum authoritative context set

Read exact local paths:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260831_1332_aiscc-p1-8-runtime-historical-replay-and-system-owner-capability-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260831_1514_aiscc-p1-8-next-action-context-ranking-authority-compatibility-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260831_1514_aiscc-p1-8-next-action-context-source-authority-baseline-gap-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md

.aiassistant/reports/aiscc/20260901_2155_aiscc-p1-8-prerequisite-authority-accepted-runtime-resume-handoff-1.md

.aiassistant/tasks/done/20260831_1143_aiscc-p1-8-memory-next-action-authority-and-terminal-epoch-runtime-rework-1.md
.aiassistant/tasks/done/20260831_1332_aiscc-p1-8-historical-replay-and-system-owner-capability-runtime-rework-1.md
.aiassistant/tasks/done/20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md
.aiassistant/tasks/done/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1.md
.aiassistant/tasks/done/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1.md
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
```

Read current source/test/migrations only inside the exact runtime boundary. Do not bulk-read unrelated rules,
records, source, tests, reports, or logs.

Repository local canonical is authority. Browser Project Source files are older read-only mirrors.

---

# 6. preserved foundations and non-substitution

Do not regress or reinterpret:

```text
AgentOutput != SystemState
EvidenceCandidate != AdmittedEvidence
NextActionSelection != TransitionDecision
TaskIssuanceCandidate != TaskContract
ExecutionStatus != WorkflowState
HumanResult != Judgment
Judgment != TransitionDecision
SecurityAdmissionDecision != TransitionDecision
```

Preserve:

- P1-4 system-owned Request/Evaluation/Decision and atomic WorkRun state mutation.
- P1-6 requirement/checkpoint/content/admission/terminal-consumed ownership.
- P1-7 Human and Judgment authority without minting new Human evidence.
- P1-8 Cycle/Memory identity, terminal epoch, current vs historical separation and restart durability.
- external Command Center Task authority as the only TaskContract/Task issuance owner.
- Replay/public paths as zero provider execution unless separately authorized.

P1-8 must not acquire P1-6 write/admit/grant-mint authority, P1-7 Human/Judgment mint authority, or P1-4 terminal
transition authority.

---

# 7. exact predecessor runtime paths

The following exact 19 paths form the start candidate:

```text
migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py
migrations/versions/20260831_0007_p1_8_authority_contract_rework.py
src/aiscc/cycle/__init__.py
src/aiscc/cycle/models.py
src/aiscc/cycle/repository.py
src/aiscc/judgment/authority.py
src/aiscc/memory/__init__.py
src/aiscc/memory/models.py
src/aiscc/memory/repository.py
src/aiscc/next_action/__init__.py
src/aiscc/next_action/models.py
src/aiscc/next_action/repository.py
src/aiscc/persistence/models.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/memory/test_postgres_project_memory_next_action.py
tests/integration/workflow/test_postgres_kernel.py
tests/unit/cycle/test_project_memory_cycle_domain.py
tests/unit/next_action/test_next_action_domain.py
```

The two predecessor migration bytes are immutable in this Task:

```text
migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py
migrations/versions/20260831_0007_p1_8_authority_contract_rework.py
```

If schema changes are required, create only the additive optional migration:

```text
migrations/versions/20260901_0008_p1_8_prerequisite_authority_reconciliation.py
```

with exact down revision `20260831_0007`. Do not rewrite, squash, renumber, backfill, or delete 0006/0007.

---

# 8. mutation allowlist

Runtime mutation is limited to:

```text
src/aiscc/cycle/__init__.py
src/aiscc/cycle/models.py
src/aiscc/cycle/repository.py
src/aiscc/judgment/authority.py
src/aiscc/memory/__init__.py
src/aiscc/memory/models.py
src/aiscc/memory/repository.py
src/aiscc/next_action/__init__.py
src/aiscc/next_action/models.py
src/aiscc/next_action/repository.py
src/aiscc/persistence/models.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/memory/test_postgres_project_memory_next_action.py
tests/integration/workflow/test_postgres_kernel.py
tests/unit/cycle/test_project_memory_cycle_domain.py
tests/unit/next_action/test_next_action_domain.py
migrations/versions/20260901_0008_p1_8_prerequisite_authority_reconciliation.py
```

Lifecycle/output paths:

```text
.aiassistant/tasks/active/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
.aiassistant/tasks/done/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
.aiassistant/reports/target/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1/**
```

If a production module or test outside this allowlist is materially required, stop before creating/editing it:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED / RUNTIME_PATH_BOUNDARY_INSUFFICIENT
```

Do not shoehorn a new owner into an inappropriate module merely to avoid this stop.

---

# 9. JCS safe-integer contract

All normative JSON sequence/high-watermark fields must enforce:

```text
minimum: 0 or 1 exactly as accepted per field
maximum: 9007199254740991
canonicalization: JCS_RFC8785
```

Mandatory:

- reject bool-as-int, float, NaN/infinity, negative, zero where origin is 1, and values above the accepted maximum;
- use exact JSON integers and RFC 8785 canonical bytes;
- preserve UTF-8/NFC/no-BOM/unknown-field denial rules;
- reject custom JCS, arbitrary-precision lexical JSON hashing, or hash-only grandfathering;
- implement all 22 accepted direct/transitive fingerprint payloads exactly;
- independently recompute documented fingerprints in tests and export evidence;
- maintain mismatch count `0` and unsafe normative integer count `0`.

Do not merely update constants. Database constraints, constructors, event writers, readers, folds, snapshots,
historical replay, and test fixtures must share the same accepted bounds.

---

# 10. TaskConstraint owner runtime

Implement the accepted prospective external owner extension exactly:

```text
owner:
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY / TASK_CONSTRAINT_AUTHORITY_V1

P1-8 access:
read/verifier port only

scope variants:
PROJECT / TASK_CONTRACT / WORK_RUN
```

Required runtime:

1. immutable `TaskConstraintRefV1` with exact accepted fields and scope discrimination;
2. immutable `ISSUED / SUPERSEDED / REVOKED` authority events;
3. pure revoke without replacement object;
4. terminal revoked logical key in V1;
5. global sequence and per-key contiguous effective sequence;
6. `TaskConstraintOwnerSnapshotV1` exact certified complete global prefix `1..H`;
7. atomic event/current projection writes and restart-durable replay;
8. historical original H verification separate from latest current applicability;
9. replay idempotency and fail-closed identity/sequence/prefix conflict;
10. private opaque issue/supersede/revoke capability with no production public/default getter.

Exact schema fingerprints must equal the accepted rule:

```text
TaskConstraint ref:
c3bba5050a43a37c2563518d862a4b7fc1c3ee344cd763ab66da19d15a7126cc

TaskConstraint event:
2b4bd41b7dbf7f002f2b48aabcf816ac386d860c12c20e947843bee5390c9b00

owner snapshot:
41330e2502ae9c337a3a1e8dfc693b2fb9307bec9eb5b5138e33ad7cdd35c1aa
```

Caller path/string/config/Markdown equality is not owner authority.

---

# 11. P1-4 blocker provenance and resolution runtime

Implement additive P1-4 system-owner runtime without changing accepted P1-4 transition semantics.

Closed exact mapping:

```text
SECURITY / SECURITY_BOUNDARY / NON_RESUMABLE
POLICY / POLICY_CONFLICT / RESUMABLE
ARTIFACT / MISSING_REQUIRED_ARTIFACT / RESUMABLE
BASELINE / BASELINE_GAP / RESUMABLE
AUTHORITY / AUTHORITY_CONFLICT / RESUMABLE
EXTERNAL_DEPENDENCY / EXTERNAL_DEPENDENCY / RESUMABLE
EXECUTION / EXECUTION_BLOCKER / RESUMABLE
```

Required:

- one ACTIVE blocker per `(work_run_id, blocked_epoch)`;
- immutable `P1_4BlockerProvenanceV1` appended atomically with admission into BLOCKED;
- `SECURITY_BOUNDARY` permits only `BLOCKED → FAILED` through `G_FAILURE_TERMINAL`;
- no positive `G_BLOCKER_RESOLVED` for non-resumable blockers;
- resumable targets only `READY / HUMAN_REQUIRED / REWORK_REQUIRED`;
- the only durable positive guard authority is `P1_4BlockerResolvedAttestationV1`;
- generic GuardObservation/reason/authority string is insufficient;
- independently verify enrolled source owner before evaluation;
- atomically append admitted P1-4 decision, state mutation, and final attestation;
- denial creates no attestation;
- historical replay rederives blocker/source/attestation/resolution transition/terminal transition relation;
- P1-8 adds only its current `resolution_cycle_id` relation and never makes P1-4 depend on Cycle ID.

Accepted fingerprints:

```text
taxonomy:
ec170cd257b04e77410951abe8c7f196a88bf8f35d9e6deaec8d8889bb0e9d0c

blocker provenance:
b984abd21d657015d3b3febbe55588762ee481ea93fcfff868114b09b5943329

resolved attestation:
0d92603174460dfd59be4b5bcb7a577014e8b51dad98fe992f08c3f638c43dbd
```

---

# 12. NEXT_ACTION_CONTEXT external source runtime

Implement the exact accepted source authority graph:

```text
context owner:
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY /
NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY_V1

P1-8:
read/verifier only

supported scope:
TASK_CONTRACT only
```

Required:

1. immutable `NextActionContextRefV1` with exact ref/logical key/scope/priority/ordinal/schema/privacy/security fields;
2. immutable `ISSUED / SUPERSEDED / REVOKED` owner events and exact fold;
3. terminal pure revoke and atomic supersede replacement;
4. owner-global sequence and logical-key contiguous effective sequence;
5. latest certified owner H for new current queries;
6. original stored H and complete prefix for historical replay;
7. exact P1-6 structured result schema/carrier verification;
8. prospective P1-6 enrollment without giving P1-6 semantic priority authority;
9. exact Memory derivation and owner-derived lineage;
10. source supersede/revoke invalidates CURRENT Memory prospectively without corrupting history;
11. private issue/supersede/revoke capability inaccessible to P1-6, P1-8 and ordinary callers.

Exact six accepted source graph fingerprints:

```text
source contract:
988cdd4c71aca75e3434652044b50ffd703fb32ba4568219c56d52e498cd8698

priority-source enrollment:
f2b090057ae3f5f00ed4ef878a41664e2322988190969458e6a6544f76932f6b

context ref schema:
842ac2619a3069a0b844cbaf89d36ceb252bfe1f1ec149097727f224a6cdc307

owner event schema:
59e695623329908fdabce214a1d80be4249b4767c86844749de93094aeb7fce4

P1-6 result schema:
db08fb7cbe1b55b7c686df28ffccbaf8462dd27dea7416e9b4478ae40e6cd67f

Memory derivation:
6de3e66a0d16a1dc0038838eb58b9ca0ca6c2d790ab3a5cdcab3802b5093b508
```

Caller fields, configuration, Memory copy, proposal, static rank, raw Markdown or matching owner strings are only
locator/equality claims and cannot mint source authority.

---

# 13. policy/catalog/descriptor reconciliation

Implement the accepted immutable identities:

```text
selection policy:
4f84dbae89ee1113a2f6eeb28aa5d00100fcb65db2694b8716b52925d9bb312d

catalog:
c02290f5111608efbd3cd12edec9e066ca622133f262a1352d971fcddf02e58c

eligibility policy:
a0425bee1c2abf26c50a63ff125795e88e0b15e6f182dfbf716fc5f0217d6d03

context-bound descriptor schema:
bef330ffba29c24a76910d22c2de514235224add40b2725d4ac342a25dc4a7ed

ActionRef schema:
d173e426e651497abbf45ba4abb6f38bdc9e9d54e4b3a63e76c33aa9e7edb2a2
```

Required:

- catalog entries are owner-authored immutable V1 values, never caller-defined action arrays;
- operational descriptor remains exact accepted owner-authored descriptor;
- cycle-derived catalog entry is a template, not a selectable descriptor;
- eligibility owner may issue a context-bound descriptor only after an exact current external context exists;
- descriptor fingerprint commits all accepted source enrollment fields;
- ActionRef commits the concrete descriptor fingerprint;
- no sentinel, placeholder, template fingerprint, caller binding or Memory copy may create a selectable ActionRef;
- production concrete CYCLE_DERIVED descriptor/ActionRef baseline count remains `0` without real external owner input;
- test-only exact external owner fixtures may exercise creation but cannot be production authority API.

Selection precondition order:

```text
POLICIES_CURRENT
→ ACTION_REF_DESCRIPTOR_CURRENT
→ CURRENT_MEMORY_CONTEXT
→ DESCRIPTOR_SOURCE_ENROLLMENT
→ EXTERNAL_SOURCE_CURRENT
→ OWNER_EQUALITY
→ RANK
```

Rank tuple:

```text
(
  authoritative_priority_rank,
  policy_dependency_ordinal,
  enrolled_critical_path_ordinal,
  descriptor_policy_ordinal,
  ActionRef lexical,
  proposal_id lexical
)
```

External context owner owns class/ordinal. Selection policy owns class→rank. Memory and descriptor copies are
equality-only. Proposal/static rank cannot override them.

---

# 14. historical replay and invalidation

Reconcile the predecessor 1332 HOLD findings completely:

- historical Memory replay rederives source body, lineage and policy from the original owner graph;
- `CycleMemoryReference` preserves exact declaration/source/policy provenance;
- same-content delayed admission cannot retain a revoked stale CURRENT tip;
- independently current same-content source may remain current only through its own valid source graph;
- historical NextAction replay recomputes descriptor payload/fingerprint and ENROLLED event binding;
- CYCLE_DERIVED selection proves Memory was CURRENT at original selection H;
- later source/Memory/policy revocation preserves historical identity but denies new current selection;
- operational recovery derives priority class from exact P1-4/P1-7 owner facts;
- BEFORE_SELECTION, where applicable to retained generic runtime paths, binds actual project/TaskContract/WorkRun;
- `AFTER_TASK_ISSUANCE_P1_7` never substitutes for BEFORE_SELECTION;
- restart reconstruction produces identical historical results.

Stored local hashes alone are not proof. Every historical relation must be independently rederived from original
immutable objects and certified prefixes.

---

# 15. required test groups

At minimum add/fresh-run:

## JCS/fingerprint

```text
all 22 accepted canonical payloads writer == independent verifier
safe maximum accepted
maximum + 1 denied
bool/float/noncanonical/unknown field denied
cross-contract mismatch denied before persistence/ranking
```

## TaskConstraint

```text
all three scope variants and forbidden-field negatives
issue/supersede/revoke/current fold
certified global-prefix H completeness/gap/conflict
historical H vs latest current
concurrent issuance/event serialization
restart durability
public caller cannot obtain issuer capability
```

## P1-4 blocker

```text
all seven exact kind/reason pairs
invalid pair denied
one blocker per blocked epoch
SECURITY_BOUNDARY positive resolution denied
resumable allowed targets only
source verification + decision/state/attestation atomicity
denial/no-attestation and rollback
historical blocker-to-terminal relation replay
```

## NEXT_ACTION_CONTEXT / Memory

```text
exact ref/event/result/Memory fingerprints
issue/supersede/revoke fold and current invalidation
P1-6 carrier accepted but no priority minting
source-derived Memory lineage and same-content delayed cases
private capability inaccessible from public packages/repositories
```

## selection/catalog

```text
caller cannot define catalog
unknown ActionRef denied before ranking
template/placeholder cannot be ActionRef
exact context-bound enrollment equality
external class/ordinal → policy rank 4/5/6
proposal/static rank cannot override
complete six-field deterministic tuple
historical descriptor/source/Memory replay
production concrete CYCLE_DERIVED count 0 without owner input
```

## regressions

```text
P1-4 PostgreSQL targeted
P1-6 core + durable PostgreSQL targeted
P1-7 PostgreSQL targeted
P1-8 unit + PostgreSQL targeted
complete repository test collection
ruff
mypy src
alembic check
```

Record exact commands, collected/pass/fail/skip counts, PostgreSQL version, Alembic head, environment reuse/freshness,
and Docker residue. No hiding, deselection, broad xfail conversion, or collection reduction.

No real provider/tool/network/credential execution is required. If a required local test environment cannot be used
without new network/credential scope, stop with `EVIDENCE_SCOPE_EXPANSION_REQUIRED`.

---

# 16. mandatory stop conditions

Stop rather than weakening the accepted contracts when:

```text
TaskConstraint owner cannot be implemented within accepted private-boundary semantics
P1-4 blocker/attestation requires changing accepted P1-4 transition ownership
NEXT_ACTION_CONTEXT source owner requires caller/config/Memory priority authority
P1-6 semantic-contract extension appears necessary
P1-8 requires P1-6 write/admit authority
P1-8 requires Human/Judgment or TransitionDecision minting
required path falls outside the exact mutation allowlist
schema requires destructive predecessor migration rewrite
accepted 22-payload fingerprint cannot be reproduced under JCS_RFC8785
current runtime/history cannot be preserved without backfill or accepted-row rewrite
```

Use the narrowest exact result:

```text
IMPLEMENTATION_BASELINE_GAP
POLICY_CONFLICT_INVESTIGATION_REQUIRED
LEGACY_PROVENANCE_REGRESSION
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

After a named blocker perform only minimal read-only evidence, workspace inventory, report/export and safe stop.

---

# 17. Git and canonical policy

The final runtime candidate remains uncommitted.

```text
NO git add
NO commit
NO push/fetch/pull/remote
```

Final HEAD must remain:

```text
1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
```

Do not update:

```text
.aiassistant/rules/**
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/cycles/**
.aiassistant/reports/aiscc/**
.aiassistant/project-sources/**
```

The 2311 audit done Task remains unchanged and uncommitted. Move only the current Task active→done after report and
target evidence are complete.

Human P1-8 runtime verification remains:

```text
HUMAN_PENDING
```

---

# 18. evidence contract

executor_required:

- `STATIC_SOURCE`: exact accepted rule/commit/predecessor identities and 22 fingerprints
- `UNIT_TEST`: domain, canonicalization, owner capability and negative contract tests
- `INTEGRATION_TEST`: PostgreSQL durability, concurrency, replay, atomicity and restart
- `PUBLIC_PROVENANCE`: final runtime path/hash inventory, Task lifecycle, unchanged HEAD/index
- `SOURCE_EVIDENCE_EXPORT`: all final runtime candidate bytes in exact path structure

reuse_allowed:

- accepted joint design and 2311 Git audit only when exact SHA/object identities match preflight
- predecessor runtime bytes only as implementation start point, never as accepted evidence

human_owned:

- runtime final review: `HUMAN_PENDING`

not_required:

- provider/tool real calls
- browser/visual QA
- Project Source mirror sync
- deployment/Public Live

forbidden:

- Agent-minted Human result or runtime acceptance
- proof-channel substitution
- remote/network/credential expansion
- Git persistence

---

# 19. export bundle

Target:

```text
.aiassistant/reports/target/
20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
RUNTIME_INVENTORY.md
FINGERPRINT_EVIDENCE.md
TEST_EVIDENCE.md
```

Include path-preserved, byte-preserved copies of:

- every final runtime candidate source/test/migration path;
- the current done Task;
- the unchanged 2311 audit done Task.

`EXPORT_MANIFEST.md` must record every file path, byte length, SHA-256, source/copy identity and mismatch count.

`RUNTIME_INVENTORY.md` must record predecessor and final per-file SHA-256 values, added/modified/unchanged
classification, final path count and ordinal aggregate.

`FINGERPRINT_EVIDENCE.md` must record all 22 payload IDs, canonical byte length, documented hash, runtime writer
hash, independent verifier hash, safe-integer result and mismatch count.

`TEST_EVIDENCE.md` must record exact command/environment/freshness/collection/result for every required test group.

Do not include secrets, raw DB dumps, private Human artifacts, unrelated source/history, `.git`, credentials, or
Project Source mirrors.

---

# 20. Task lifecycle and final workspace

After implementation, tests, report and target are complete, move:

```text
.aiassistant/tasks/active/
20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
→
.aiassistant/tasks/done/
20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
```

Do not stage or commit it.

Final expected workspace:

```text
HEAD: unchanged at 1c9a3ef...
index: empty
accepted rules/governance: clean
2311 done Task: unchanged and uncommitted
current done Task: uncommitted
runtime candidate: exact final path inventory/aggregate reported
unexpected dirty paths: 0
```

---

# 21. expected outcomes

Success:

```text
P1-8 Runtime:
REWORKED_CANDIDATE / COMMAND_CENTER_REVIEW_REQUIRED / HUMAN_PENDING

P2/P3:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Blocked:

```text
P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE / <EXACT_BLOCKER>
```

No terminal runtime commit is authorized before separate Command Center substantive review and Human runtime final
review.

---

# 22. Executor report requirements

Report exact:

1. task/work type/task path/done path
2. source download path, active placement identity and Task SHA
3. repository/branch/start and final HEAD/index
4. accepted Commit A/B and rule SHA verification
5. 2311 audit done Task identity
6. predecessor 19-path status/per-file hashes/aggregate
7. exact files read and instruction conflict result
8. exact runtime files added/modified/unchanged
9. optional 0008 migration created or `NOT_REQUIRED`, down revision and Alembic result
10. TaskConstraint owner/runtime result
11. P1-4 blocker/attestation runtime result
12. NEXT_ACTION_CONTEXT source/result/Memory runtime result
13. catalog/policy/descriptor/ActionRef result
14. historical/current replay result
15. 22-payload writer/independent verifier result and unsafe integer count
16. each unit/integration/regression/static command and exact counts
17. PostgreSQL/Alembic/Docker environment and residue
18. final runtime path count/per-file SHA/aggregate
19. Human runtime verification = `HUMAN_PENDING`
20. runtime acceptance = `NOT_MINTED`
21. P2/P3/Public Live status
22. current Task active→done lifecycle
23. forbidden-not-run and unverified items
24. rollback guide without executing it
25. preserved exact paths
26. final result taxonomy

---

# 23. preserved exact paths

Preserve accepted governance unchanged:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/records/aiscc/cycles/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md
.aiassistant/reports/aiscc/20260901_2155_aiscc-p1-8-prerequisite-authority-accepted-runtime-resume-handoff-1.md
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
```

Preserve the final runtime candidate exact paths reported by `RUNTIME_INVENTORY.md` and the current done Task:

```text
.aiassistant/tasks/done/
20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
```

The target bundle is temporary and deletable only after substantive Command Center review.
