# 작업지시서: P2-4 durable TaskContract full-corrected runtime implementation retry

## meta

- task_id: `20260914_1052_aiscc-p2-4-taskcontract-durable-body-full-corrected-runtime-implementation-retry-1`
- created_at: `2026-09-14T10:52:03+09:00`
- work_type: `DOC_BASELINE_UPDATE + BACKEND_IMPLEMENTATION + DATABASE_MIGRATION + QA_ONLY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `f8193d83d032fc4a0a49d3471205ac693025e4f1`
- required_parent: `f0e55ecd9e65f2b10d529d5a6469452826bedffb`
- predecessor_result_zip_sha256: `f4861616c4b883533f4df238b93218a51cb9dde82033d0b0d82bb4bb5acf9e41`
- predecessor_done_task_sha256: `81c26b4629c6460c6481a338623a19d440aaa2d6feaef279632bc264a58b0bc3`
- predecessor_result: `P2_4_TEMPLATE_APPROVAL_AUTHORITY_BINDING_CORRECTION_PROPOSAL / HUMAN_REVIEW_PENDING`
- predecessor_outcome: `OUTCOME_A`
- browser_design_judgment: `ACCEPTED_CANDIDATE`
- human_design_decision: `HUMAN_PROVIDED / ACCEPT`
- human_review_artifact_sha256: `fe066553b5df1a5a9abfda473eb09aa10d52a705ced18cf9f09ed6efd0b329d5`
- fresh_IDE_chat_required: `No`
- governance_commit_authorized: `Yes / exact 4 paths / Commit A`
- result_commit_authorized: `Yes / exact allowlist / Commit B`
- canonical_baseline_mutation_authorized: `Yes / exact 4 rule paths`
- migration_creation_authorized: `Yes / exact one migration`
- isolated_PostgreSQL_authorized: `Yes / task-owned ephemeral only`
- Docker_authorized: `Yes / local postgres:17.6 only`
- external_network_authorized: `No`
- provider_LLM_authorized: `No`
- retained_private_DB_authorized: `No`
- actual_self_dogfood_golden_cycle_authorized: `No`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. Human acceptance and normative chain

Human exact decision for the 1045 review:

```text
ACCEPT
```

Admit as:

```text
HUMAN_PROVIDED / ACCEPTED
```

Normative chain for this implementation:

```text
0319 durable-body base proposal
+ 0812 body_ref correction
+ 0902 Human binding correction
+ 0902 Judgment binding correction
+ 0940 Outcome A template/approval authority correction
```

Precedence:

```text
0940 correction
> conflicting template/approval-source clauses in 0319

0902 corrections
> conflicting Human/Judgment clauses in 0319

0812 correction
> conflicting body_ref clause in 0319

all other 0319 clauses:
remain accepted
```

Do not reinterpret these accepted artifacts into a new design.

# 1. accepted input verification

After reading this Task, copy package `ACCEPTED_DESIGN/**` only into:

```text
.aiassistant/reports/target/20260914_1052_aiscc-p2-4-taskcontract-durable-body-full-corrected-runtime-implementation-retry-1/accepted-input/
```

Expected SHA-256:

- `0319/TASKCONTRACT_DURABLE_BODY_BASELINE_PROPOSAL.md`: `803686433f900282117a4318d8f59a14b5b5a68735775b4f1242acf544c16410`
- `0812/20260914_0812_aiscc-p2-4-durable-taskcontract-body-ref-compatibility-human-correction-review-1.md`: `4c6905734e7a48b9688257574d86b1a7215627ac8514c7112747889c6bafa318`
- `0902/HUMAN_BINDING_CORRECTION_PROPOSAL.md`: `7ecad09c1e151fc76e83d85d7a84c25c14f09abba7e093393a5cf73b9a1d2833`
- `0902/JUDGMENT_BINDING_CORRECTION_PROPOSAL.md`: `aed8421248cc8700fd0ebc2128ae7f5808037df555fbe8e0ee61606dd0eb9693`
- `0902/HUMAN_JUDGMENT_POLICY_SOURCE_AUDIT.md`: `2595ac130c12a0da3cf45dc7867e4cb6806fafc83e0c77feec51147ccc57b0a9`
- `0902/OWNER_NON_SUBSTITUTION_PROOF.md`: `7f22c68055d2cb2c118aa7ca67efc01ab36c09811030362bc935d23634e70a92`
- `0902/IMPLEMENTATION_IMPACT_ALLOWLIST.md`: `aee264ccc3aaa5aa6906c3c96ad0981d0c5aea11c68895e63dad3b3638632c6b`
- `0902/BASELINE_SUPERSESSION_DELTA.md`: `47a473ab37a9fec09dee623dc254acf7d0b726f30cbae5c251715679ff6a9448`
- `0940/TASKCONTRACT_TEMPLATE_REQUIREMENT_CORRECTION_PROPOSAL.md`: `da2bf0d59e148d6359b7e979296a7d63b01307f0500df6c2e715937527edd951`
- `0940/TEMPLATE_AUTHORITY_CANONICAL_AUDIT.md`: `2889d21300126671ee1e1b3ecc3acf3b1a96358b1e26c81e253e94413b4f5f85`
- `0940/P1_8_DESCRIPTOR_TEMPLATE_SEMANTICS_AUDIT.md`: `609d6c085b7edd2a79bbf8afd0e2461ec1919642cfdb33e333bea5c64676668c`
- `0940/OWNER_NON_SUBSTITUTION_PROOF.md`: `3ba78e965f88749d6805268d049154366f7bbcee1c1d77697393230c7e6aff23`
- `0940/BASELINE_SUPERSESSION_DELTA.md`: `20f050403f50f9edaa9c445ba049135da896b52cc31dadf03a7912dde34d7e69`
- `0940/IMPLEMENTATION_IMPACT_ALLOWLIST.md`: `cf5a4cc5932d4ebaec1d84376bfbaff7a9c7d93cfba5379f883ebd94d3766080`

Human review artifact:

```text
20260914_1045_aiscc-p2-4-template-approval-authority-correction-human-review-1.md
SHA-256:
fe066553b5df1a5a9abfda473eb09aa10d52a705ced18cf9f09ed6efd0b329d5
```

Any mismatch:

```text
BLOCKED_MISSING_ARTIFACT
```

STOP before governance/product mutation.

# 2. exact initial repository preflight

Require before governance placement/mutation:

```text
branch:
main

HEAD:
f8193d83d032fc4a0a49d3471205ac693025e4f1

HEAD^:
f0e55ecd9e65f2b10d529d5a6469452826bedffb

index:
empty

tracked:
clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0940_aiscc-p2-4-template-approval-authority-binding-correction-design-1.md

SHA-256:
81c26b4629c6460c6481a338623a19d440aaa2d6feaef279632bc264a58b0bc3
```

Preserve ignored legacy Task:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md

SHA-256:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Canonical state must initially and terminally remain byte-exact:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48

.aiassistant/records/aiscc/DECISION_REGISTER.md
9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5

.aiassistant/records/aiscc/NEXT_ACTIONS.md
050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679
```

Any mismatch -> STOP before mutation.

# 3. executables

Use only:

```text
Python:
<repository-root>\.venv\Scripts\python.exe

Git:
C:\Program Files\Git\cmd\git.exe

Docker:
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

Docker is authorized only for isolated PostgreSQL verification in this Task.

Do not substitute PATH Python/Git/Docker.

# 4. inbound placement

Transport:

```text
verify ZIP/hash/archive/member safety
→ place TASK into .aiassistant/tasks/active
→ read TASK
→ verify/copy ACCEPTED_DESIGN into ignored target staging
→ place Cycle/Judgment/Human review into canonical governance paths
```

Canonical placement:

```text
20260914_1052_aiscc-p2-4-template-authority-correction-human-accepted-runtime-implementation-retry-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_1052_aiscc-p2-4-template-authority-correction-human-acceptance-runtime-implementation-reauthorization-1.md
-> .aiassistant/reports/aiscc/

20260914_1045_aiscc-p2-4-template-approval-authority-correction-human-review-1.md
-> .aiassistant/reports/aiscc/
```

Human review copy must remain byte-exact.

# 5. Governance Commit A

Before commit, Git-visible untracked exactly:

```text
.aiassistant/tasks/done/20260914_0940_aiscc-p2-4-template-approval-authority-binding-correction-design-1.md
.aiassistant/records/aiscc/cycles/20260914_1052_aiscc-p2-4-template-authority-correction-human-accepted-runtime-implementation-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_1052_aiscc-p2-4-template-authority-correction-human-acceptance-runtime-implementation-reauthorization-1.md
.aiassistant/reports/aiscc/20260914_1045_aiscc-p2-4-template-approval-authority-correction-human-review-1.md
```

Stage exactly those four.

Commit message exactly:

```text
docs(aiscc): accept taskcontract template authority correction
```

Require:

```text
Commit A parent = f8193d83d032fc4a0a49d3471205ac693025e4f1
changed paths = exact 4
index empty
tracked clean
Git-visible untracked = 0
```

No baseline/product mutation before exact Commit A.

# 6. mandatory canonical/source reads

Read at minimum:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Read directly affected current source in:

```text
src/aiscc/task_authority/**
src/aiscc/next_action/**
src/aiscc/workflow/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/persistence/models.py
```

Read-only paths remain read-only below.

If current repository disproves the accepted composition:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

STOP before mutation. Do not redesign in-place.

# 7. canonical baseline adoption

Create/modify only:

```text
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

Adopt the exact accepted chain.

The durable-body rule must preserve explicitly:

```text
TaskIssuanceCandidate != TaskContract
ActionDescriptor != TaskContract
TaskContract owner = EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY

P1-8:
owns current selection / descriptor / source-currentness lineage

EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY:
owns authorization of the exact complete immutable TaskContract body

P1-6:
owns evidence admission/checkpoint authority

P1-7:
owns HumanGate/HumanResult/Judgment/runtime fingerprints/currentness

P1-4:
owns TransitionDecision/WorkflowState mutation
```

Do NOT modify:

```text
AISCC_HUMAN_GATE_JUDGMENT.md
AISCC_EVIDENCE_ADMISSION.md
AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md
```

# 8. body identity — 0812 accepted correction

Preserve exact:

```text
body_identity_bytes =
existing restricted canonical JSON/JCS of:
{
  "project_id": project_id,
  "contract_id": contract_id,
  "contract_version": n
}

body_ref =
"task-contract-body:v1:sha256:" + SHA256(body_identity_bytes)
```

Exact length:

```text
93 ASCII characters
```

Content integrity remains separate:

```text
body_sha256 = SHA256(canonical_body)
constraint_payload_ref = body_ref
constraint_payload_fingerprint = body_sha256
```

Do not modify existing `TaskConstraintRefV1` validation or accepted 96-character project/contract ID domain.

# 9. Human/Judgment binding — 0902 accepted correction

Implement exact accepted bytes from:

```text
0902/HUMAN_BINDING_CORRECTION_PROPOSAL.md
0902/JUDGMENT_BINDING_CORRECTION_PROPOSAL.md
```

Key boundary only:

```text
TaskContract:
immutable owner-consumable Human/Judgment configuration

existing P1-7 Human owner:
actual gate reservation/opening, principal auth, HumanResult, Human guard

existing JudgmentPolicyAuthority:
runtime policy fingerprint/currentness, Judgment, Judgment guard
```

Do not add independent pre-WorkRun Human policy fingerprint.

Do not store precomputed runtime Judgment policy fingerprint in the body.

P1-7 source/rules remain read-only.

# 10. template/approval authority — 0940 accepted Outcome A

Implement exactly:

```text
0940/TASKCONTRACT_TEMPLATE_REQUIREMENT_CORRECTION_PROPOSAL.md
```

For current owner-recognized `POLICY_ACTION_CATALOG` descriptors:

```text
task_template_ref/hash = NONE/null
```

means only:

```text
no separate template provenance attached
```

It does NOT mean:

```text
template authority satisfied by NONE
arbitrary body authorized
Markdown approved
body_sha256 is approval
```

Required complete authority chain:

```text
authoritative/current P1-8 selection
+ owner-recognized/current descriptor/source lineage
+ exact EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
+ explicit authorization of exact complete immutable body
+ exact repository/base/scope/policy/evidence bindings
+ durable V1 ref/event/certified-prefix/body verification
```

No new:

```text
template registry
template table
Markdown resolver
URL resolver
approval DB
P1-8 source kind
generic approval callback
```

is authorized.

Unsupported non-catalog source kinds remain denied.

## authority_refs

Implement the accepted replacement:

```text
required field
possibly-empty sorted tuple/list representation
closed entries:
{
  "ref": <nonblank NFC 1..1024 UTF-8 bytes>,
  "fingerprint": <64 lowercase hex SHA-256>
}
```

Semantics:

```text
empty:
no ADDITIONAL independent authority ref required by applicable existing owner policy

nonempty:
every required ref present
every supplied ref independently verifiable by its existing semantic owner
```

Do not interpret opaque refs as template approval.

Unknown namespace/schema, unverifiable ref, wrong hash/scope/currentness, or inability to establish the required set must deny.

The body cannot choose its own required authority set.

The newly issued body V1 ref cannot circularly appear in `authority_refs`.

# 11. complete-body authorization

Do not infer the complete contract from:

```text
action label
Agent prose
LLM rationale
descriptor alone
TaskIssuanceCandidate alone
body hash alone
```

The complete immutable body must be explicitly authorized through the existing private `EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY` issuance surface.

The body fixes:

```text
goal/non-goals
allowed/forbidden paths
repository/base
source_next_action
evidence binding
Human binding
Judgment binding
execution provenance
additional authority_refs
all other accepted fields
```

Validate source action/parameters/project restrictions/currentness and exact repository binding against that body.

No public writer and no Agent/self_dogfood issuance capability.

# 12. durable-body implementation contract

Implement accepted:

```text
TaskContractBodyV1
IssuedTaskContractV1
VerifiedTaskContractBindingV1
TaskContractBodyRow
```

Preserve:

- closed recursive immutable body;
- exact restricted canonical JSON/JCS;
- NFC/domain/safe-integer/path safety;
- scope overlap/traversal/absolute-path denial;
- accepted source_next_action/currentness verification;
- atomic body + V1 ref + issuance event/snapshot semantics;
- exact retry idempotency;
- conflicting same-version body deny;
- additive version lineage/predecessor;
- explicit latest revoke/currentness;
- restart verification;
- missing/tampered/partial durable authority -> `AUTHORITY_CORRUPTION`;
- no auto-repair/backfill.

# 13. exact mutation allowlist

Canonical rules:

```text
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

Runtime:

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

Tests:

```text
tests/unit/task_authority/test_task_contract_body.py
tests/unit/task_authority/test_task_contract_issuance.py
tests/integration/task_authority/test_task_contract_durability.py
tests/integration/task_authority/test_task_contract_ready.py
```

READ-ONLY / MUST NOT MODIFY:

```text
src/aiscc/task_authority/models.py
src/aiscc/next_action/**
src/aiscc/workflow/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/evidence/**
AISCC_HUMAN_GATE_JUDGMENT.md
AISCC_EVIDENCE_ADMISSION.md
AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
```

If any additional mutation is truly required:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

If semantic owner extension is required:

```text
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

STOP before modifying the additional path/owner.

# 14. READY integration

Implement the accepted `TaskContractReadyParticipant` using existing P1-4 participant/kernel surfaces only.

Before READY, verify:

```text
durable body/ref/hash/currentness
source_next_action currentness
repository/base
scope
runtime mode/provenance
Human/Judgment config consistency
required additional authority_refs through existing owners
```

Human/Judgment owner composition may use only existing public owner APIs.

READY must NOT:

```text
reserve/open Human gate
authenticate Human
create HumanResult
create Judgment
mint G_HUMAN_* or G_JUDGMENT_*
satisfy G_EVIDENCE
mutate WorkflowState outside P1-4
```

Existing WorkRun schema remains unchanged.

# 15. migration

Before creation verify:

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

Implement accepted additive one-table design only.

Requirements:

```text
task_contract_bodies
canonical_body BYTEA
body_ref
body_schema_id
body_sha256
constraint_ref
issuance_event_ref
predecessor version/hash
issued_at
identity/version checks
1 MiB max canonical body
UPDATE/DELETE deny trigger
TRUNCATE deny trigger
no existing table/column mutation
no backfill
no pgcrypto requirement
empty-only downgrade
nonempty downgrade fail-closed preserving schema/row/revision
```

No template/approval table.

# 16. isolated PostgreSQL 17.6 proof

First run only:

```text
"C:\Program Files\Docker\Docker\resources\bin\docker.exe" image inspect postgres:17.6
```

If absent:

```text
ISOLATED_POSTGRES_IMAGE_MISSING
```

Do not pull.

Use one new task-owned disposable container, e.g.:

```text
aiscc-p2-4-taskcontract-1052-pg
```

Use synthetic credentials, bind only `127.0.0.1` to a free local port.

Required proof:

1. empty DB -> migration head PASS;
2. predecessor 0008 -> 0009 PASS;
3. restart/reload exact body/ref/hash;
4. 96/96 identity -> exact 93-char body_ref;
5. exact retry idempotent;
6. changed same-version body denied;
7. concurrent issuance/version race deterministic;
8. write-boundary rollback leaves no partial body/ref/event authority;
9. UPDATE/DELETE/TRUNCATE denied;
10. empty downgrade PASS;
11. nonempty downgrade FAIL-CLOSED preserving schema/row/revision;
12. reconstruction verifies without in-memory objects;
13. Human NOT_REQUIRED config restart/verify PASS;
14. Human REQUIRED config restart/verify PASS;
15. Judgment config registration via existing owner is idempotent/currentness-verified;
16. catalog descriptor with template NONE/null + explicit complete-body owner authorization PASS;
17. same catalog descriptor without explicit complete-body authorization DENY;
18. empty authority_refs only when existing trusted issuance policy requires none PASS;
19. missing/wrong-hash/wrong-scope/unverifiable required additional authority ref DENY;
20. no template/approval table/source-kind/registry created;
21. READY preparation creates no HumanResult/Judgment/Human/Judgment/Evidence guard fact.

Exact container cleanup best-effort. Cleanup failure is nonblocking residue.

No Docker prune.

# 17. tests

Required files:

```text
tests/unit/task_authority/test_task_contract_body.py
tests/unit/task_authority/test_task_contract_issuance.py
tests/integration/task_authority/test_task_contract_durability.py
tests/integration/task_authority/test_task_contract_ready.py
```

All PASS.

Must cover at minimum:

### 0812
- max 96/96 ID -> 93-char ref;
- ref recomputation/tamper/version/project/contract negatives;
- unchanged TaskConstraintRefV1 constructor PASS.

### 0902
- exact Human REQUIRED/NOT_REQUIRED closed config;
- exact Judgment config/cross-object consistency;
- no caller/runtime fingerprint injection;
- existing owner registration/idempotency/currentness;
- no gate/result/Judgment created by READY.

### 0940
- recognized current catalog descriptor + NONE/null template + explicit complete-body authorization PASS;
- NONE/null alone never authorizes issuance;
- ActionDescriptor alone deny;
- TaskIssuanceCandidate alone deny;
- caller descriptor/candidate deny;
- stale/wrong selection/descriptor/action/parameters deny;
- empty authority_refs allowed only when trusted policy requires none;
- missing required additional ref deny;
- wrong fingerprint/scope/schema/currentness deny;
- body self-ref circular authority deny;
- Markdown/hash/Agent approval/body-hash-only deny;
- unsupported non-catalog source kind deny.

### durability/READY
- accepted atomicity/restart/version/revoke/currentness cases;
- repository/base/path/scope negatives;
- existing P1-4 owner remains sole READY/workflow mutation authority.

Also run directly affected existing narrow regressions for:

```text
task_authority
P1-4 READY/transition
P1-8 selection/descriptor/currentness
P1-7 Human/Judgment
```

Inventory exact test paths/counts first. Existing tests are read/run only unless in the exact test allowlist above.

Static:

```text
Ruff changed Python
compile changed Python
git diff --check
UTF-8/control-character/Markdown checks changed canonical docs
```

# 18. forbidden

Forbidden:

```text
modify task_authority/models.py
modify next_action/**
modify workflow/**
modify human/**
modify judgment/**
modify evidence/**
new template/approval registry or table
new P1-8 source kind
new Human/Judgment registry/table/fingerprint authority
Markdown or URL runtime approval resolver
widen TaskConstraintRefV1/_ID
narrow 96-char ID domain
actual self-dogfood golden cycle
real self-dogfood Task issuance
src/aiscc/self_dogfood/** mutation
stockroom/P2-3 replay mutation
CURRENT_STATE_SUMMARY/DECISION_REGISTER/NEXT_ACTIONS mutation
retained/private PostgreSQL
external network
Docker pull
provider/LLM
push/deploy/automatic merge
```

# 19. Result Commit B

Only after all required evidence PASS.

Stage exact changed files inside section 13.

Commit message exactly:

```text
feat(aiscc): add durable taskcontract authority
```

Require:

```text
Commit B parent = Governance Commit A
changed paths subset = exact authorized allowlist
all read-only owner paths unchanged
index empty
tracked clean
```

If any required proof fails:

```text
no Commit B
```

Preserve truthful Task-owned changes/evidence; do not broad-reset simply to satisfy cleanliness.

# 20. report/export

Target:

```text
.aiassistant/reports/target/20260914_1052_aiscc-p2-4-taskcontract-durable-body-full-corrected-runtime-implementation-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ACCEPTED_DESIGN_INPUT_VERIFICATION.md
TEMPLATE_AUTHORITY_CORRECTION_ACCEPTANCE_VERIFICATION.md
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

Result ZIP:

```text
.aiassistant/reports/target/20260914_1052_aiscc-p2-4-taskcontract-durable-body-full-corrected-runtime-implementation-retry-1.zip
```

# 21. terminal repository boundary

Complete success:

```text
HEAD = Result Commit B
index = empty
tracked = clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1052_aiscc-p2-4-taskcontract-durable-body-full-corrected-runtime-implementation-retry-1.md
```

Current Task active -> done byte-identically.

Legacy 1400 Task exact unchanged.

Canonical state hashes from section 2 unchanged.

Blocked/failure:

- no Result Commit B;
- preserve truthful changed-path inventory/evidence;
- no broad cleanup/reset;
- exact Docker residue cleanup only best-effort.

# 22. mandatory stop

Named blockers:

```text
BLOCKED_MISSING_ARTIFACT
POLICY_CONFLICT_INVESTIGATION_REQUIRED
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
MIGRATION_BASELINE_MISMATCH
ISOLATED_POSTGRES_IMAGE_MISSING
BLOCKED_REQUIRED_EVIDENCE
SECURITY_BOUNDARY_BLOCKED
```

After blocker, only minimal blocker evidence/workspace report/export/safe termination.

# 23. success ceiling

Complete PASS may report only:

```text
P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do NOT claim:

```text
P2_4_SELF_DOGFOOD_ENTRY_SOURCE_CANDIDATE
golden self-dogfood complete
P2-4 ACCEPTED/CLOSED
```

State ceiling:

```text
P2-3:
ACCEPTED / CLOSED

P2-4:
IN_PROGRESS

0319 durable-body base:
HUMAN_PROVIDED / ACCEPTED

0812 body_ref correction:
HUMAN_PROVIDED / ACCEPTED

0902 Human/Judgment correction:
HUMAN_PROVIDED / ACCEPTED

0940 template/approval authority correction:
HUMAN_PROVIDED / ACCEPTED

durable TaskContract runtime:
candidate only if this Task fully passes

self-dogfood source candidate:
NOT CREATED

golden cycle:
NOT PERFORMED

P3:
NOT_STARTED

Public Bounded Live:
NOT_RELEASED
```
