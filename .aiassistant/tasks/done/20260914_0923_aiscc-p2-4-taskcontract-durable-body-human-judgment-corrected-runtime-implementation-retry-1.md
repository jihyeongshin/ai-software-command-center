# 작업지시서: P2-4 durable TaskContract Human/Judgment-corrected runtime implementation retry

## meta

- task_id: `20260914_0923_aiscc-p2-4-taskcontract-durable-body-human-judgment-corrected-runtime-implementation-retry-1`
- created_at: `2026-09-14T09:23:56+09:00`
- work_type: `DOC_BASELINE_UPDATE + BACKEND_IMPLEMENTATION + DATABASE_MIGRATION + QA_ONLY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `c10f89256b88d90782c7fbdea6ff8b27655f2b46`
- required_parent: `5aaeb6f690cd9209af57a60b846ac049e89e9047`
- predecessor_result_zip_sha256: `c163fd43b325e408745796d9b751d73d31c1c8f340b501255194be503465352f`
- predecessor_done_task_sha256: `ab925862eb83702412036db92796237b6b5adc49fd4f8ee1cf28b5d8d34f0902`
- predecessor_result: `P2_4_HUMAN_JUDGMENT_POLICY_BINDING_CORRECTION_PROPOSAL / HUMAN_REVIEW_PENDING`
- browser_design_judgment: `ACCEPTED_CANDIDATE`
- human_design_decision: `HUMAN_PROVIDED / ACCEPT`
- human_review_artifact_sha256: `68275bcb77433c9d50b458226991d78cc56a981054fc59a81194a3a5c221fe86`
- fresh_IDE_chat_required: `No`
- governance_commit_authorized: `Yes / exact 4 paths / Commit A`
- result_commit_authorized: `Yes / exact implementation allowlist / Commit B`
- canonical_baseline_mutation_authorized: `Yes / exact 4 rule paths`
- migration_creation_authorized: `Yes / exact one migration`
- isolated_PostgreSQL_authorized: `Yes / task-owned ephemeral only`
- Docker_authorized: `Yes / local postgres:17.6 image only`
- external_network_authorized: `No`
- provider_LLM_authorized: `No`
- retained_private_DB_authorized: `No`
- actual_self_dogfood_golden_cycle_authorized: `No`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. Human decision / exact supersession chain

Human exact response to the 0902 correction review:

```text
Accept
```

Admit as:

```text
HUMAN_PROVIDED / ACCEPTED
```

Normative durable-body chain now is:

```text
0319 base proposal
+ 0812 Human-accepted body_ref correction
+ 0902 Human-accepted Human binding correction
+ 0902 Human-accepted Judgment binding correction
```

Precedence:

```text
0902 Human/Judgment corrections
> conflicting Human/Judgment clauses in 0319 base proposal

0812 body_ref correction
> conflicting body_ref clause in 0319 base proposal

all other 0319 clauses:
remain accepted unchanged
```

Do not reinterpret or silently redesign these accepted bytes.

# 1. exact accepted inputs

After reading this Task, copy package `ACCEPTED_DESIGN/` members only into:

```text
.aiassistant/reports/target/20260914_0923_aiscc-p2-4-taskcontract-durable-body-human-judgment-corrected-runtime-implementation-retry-1/accepted-input/
```

Expected SHA-256:

- `TASKCONTRACT_DURABLE_BODY_BASELINE_PROPOSAL.md`: `803686433f900282117a4318d8f59a14b5b5a68735775b4f1242acf544c16410`
- `20260914_0812_aiscc-p2-4-durable-taskcontract-body-ref-compatibility-human-correction-review-1.md`: `4c6905734e7a48b9688257574d86b1a7215627ac8514c7112747889c6bafa318`
- `HUMAN_BINDING_CORRECTION_PROPOSAL.md`: `7ecad09c1e151fc76e83d85d7a84c25c14f09abba7e093393a5cf73b9a1d2833`
- `JUDGMENT_BINDING_CORRECTION_PROPOSAL.md`: `aed8421248cc8700fd0ebc2128ae7f5808037df555fbe8e0ee61606dd0eb9693`
- `HUMAN_JUDGMENT_POLICY_SOURCE_AUDIT.md`: `2595ac130c12a0da3cf45dc7867e4cb6806fafc83e0c77feec51147ccc57b0a9`
- `OWNER_NON_SUBSTITUTION_PROOF.md`: `7f22c68055d2cb2c118aa7ca67efc01ab36c09811030362bc935d23634e70a92`
- `IMPLEMENTATION_IMPACT_ALLOWLIST.md`: `aee264ccc3aaa5aa6906c3c96ad0981d0c5aea11c68895e63dad3b3638632c6b`
- `BASELINE_SUPERSESSION_DELTA.md`: `47a473ab37a9fec09dee623dc254acf7d0b726f30cbae5c251715679ff6a9448`

Human review artifact:

```text
20260914_0902_aiscc-p2-4-human-judgment-policy-binding-correction-human-review-1.md
SHA-256:
68275bcb77433c9d50b458226991d78cc56a981054fc59a81194a3a5c221fe86
```

If any input is missing/mismatched:

```text
BLOCKED_MISSING_ARTIFACT
```

STOP before governance/source mutation.

# 2. exact initial repository preflight

Require before governance placement/mutation:

```text
branch:
main

HEAD:
c10f89256b88d90782c7fbdea6ff8b27655f2b46

HEAD^:
5aaeb6f690cd9209af57a60b846ac049e89e9047

index:
empty

tracked:
clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0902_aiscc-p2-4-human-judgment-policy-binding-correction-design-1.md

SHA-256:
ab925862eb83702412036db92796237b6b5adc49fd4f8ee1cf28b5d8d34f0902
```

Preserve ignored legacy Task:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md

SHA-256:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Canonical current state must initially and terminally remain byte-exact:

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

Docker is authorized only for section 15 isolated PostgreSQL verification.

If repository Python is absent, STOP. Do not discover another Python.

No PATH/external executable substitution.

# 4. inbound placement

Transport order:

```text
verify delivery ZIP/hash/archive/path safety
→ put current TASK into .aiassistant/tasks/active
→ read TASK
→ verify/copy accepted design inputs into ignored target staging
→ place Cycle/Judgment/Human review into canonical governance paths
```

Canonical placement:

```text
20260914_0923_aiscc-p2-4-human-judgment-binding-human-accepted-runtime-implementation-retry-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_0923_aiscc-p2-4-human-judgment-binding-human-acceptance-runtime-implementation-reauthorization-1.md
-> .aiassistant/reports/aiscc/

20260914_0902_aiscc-p2-4-human-judgment-policy-binding-correction-human-review-1.md
-> .aiassistant/reports/aiscc/
```

The Human review canonical copy must remain byte-exact.

# 5. Governance Commit A — Human correction acceptance provenance

Before commit, Git-visible untracked exactly:

```text
.aiassistant/tasks/done/20260914_0902_aiscc-p2-4-human-judgment-policy-binding-correction-design-1.md
.aiassistant/records/aiscc/cycles/20260914_0923_aiscc-p2-4-human-judgment-binding-human-accepted-runtime-implementation-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_0923_aiscc-p2-4-human-judgment-binding-human-acceptance-runtime-implementation-reauthorization-1.md
.aiassistant/reports/aiscc/20260914_0902_aiscc-p2-4-human-judgment-policy-binding-correction-human-review-1.md
```

Stage exactly those four paths.

Commit message exactly:

```text
docs(aiscc): accept taskcontract human judgment binding correction
```

Require:

```text
Commit A parent = c10f89256b88d90782c7fbdea6ff8b27655f2b46
changed paths = exact 4
index empty
tracked clean
Git-visible untracked = 0
```

No baseline/product mutation before exact Commit A.

# 6. canonical/source read authority

Read at minimum:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Read current implementation-owner source including existing P1-7 APIs, but section 9 mutation allowlist is authoritative.

If exact current repository disproves the Human-accepted composition without requiring a forbidden semantic weakening:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

STOP. Do not silently redesign again.

# 7. canonical baseline adoption — allowed rules only

Create/modify only:

```text
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

Adopt the normative chain from section 0.

The new durable-body rule must explicitly preserve:

```text
TaskIssuanceCandidate != TaskContract
TaskContract owner = EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
TaskConstraintRefV1 unchanged
existing _ID limit unchanged
unknown_fields=DENY unchanged
96-char project_id/contract_id domain unchanged

body_ref =
task-contract-body:v1:sha256:<SHA256(JCS(project_id, contract_id, contract_version))>

Human binding:
TaskContract-issued immutable configuration only

Judgment binding:
TaskContract-issued immutable registration configuration only

HumanGate / HumanResult / Human runtime guard:
existing P1-7 owner

JudgmentPolicy fingerprint/currentness / Judgment / Judgment guard:
existing P1-7 owner

TransitionDecision / WorkflowState:
existing P1-4 owner

Evidence admission/checkpoint:
existing P1-6 owner
```

Do NOT modify:

```text
AISCC_HUMAN_GATE_JUDGMENT.md
AISCC_EVIDENCE_ADMISSION.md
Security baseline
CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md
```

# 8. corrected Human binding — exact

Implement the accepted closed object:

```text
human_binding = {
  kind,
  authority_policy_ref,
  authority_policy_version,
  required_uses,
  purpose_id,
  purpose_version,
  owner_selector_fingerprint
}
```

Unknown fields denied; all keys required.

`kind`:

```text
REQUIRED | NOT_REQUIRED
```

`authority_policy_ref`:

```text
nonblank NFC string
1..160 UTF-8 bytes
TaskContract-issued immutable config
passed unchanged to existing HumanGateReservationAuthority
```

`authority_policy_version`:

```text
nonblank NFC string
1..64 UTF-8 bytes
```

`required_uses`:

```text
sorted unique closed entries:
{source_state, target_state}
using existing WorkflowState values
```

`NOT_REQUIRED` exact:

```text
required_uses = []
purpose_id = null
purpose_version = null
owner_selector_fingerprint = null

every judgment policy:
requires_human_result = false

judgment owner_policy:
must not be HUMAN
```

`REQUIRED` exact:

```text
purpose_id = P1_7_WORK_RESULT_REVIEW
purpose_version = v1
owner_selector_fingerprint = existing enrolled server selector key semantics
1..160 NFC bytes

judgment owner_policy = HUMAN
every judgment entry requires_human_result = true
```

REQUIRED `required_uses` must include:

- at least one existing fresh gate-open pair guarded by `G_HUMAN_REQUIRED`;
- all six existing `G_HUMAN_NOT_REQUIRED` bypass pairs accepted in `HUMAN_BINDING_CORRECTION_PROPOSAL.md`;
- no fresh `BLOCKED -> HUMAN_REQUIRED` reservation rule.

Do not invent an independent Human policy fingerprint.

`owner_selector_fingerprint` retains the existing source parameter name but is the existing enrolled selector-key value, NOT a newly computed role digest.

Whole `body_sha256` authenticates immutable TaskContract config bytes only. It does not replace any runtime P1-7 fingerprint.

# 9. corrected Judgment binding — exact

Implement:

```text
judgment_binding = {
  owner_policy,
  policies
}
```

`owner_policy` exactly one:

```text
SYSTEM_DETERMINISTIC
HUMAN
COMMAND_CENTER
```

`policies`:

```text
nonempty
sorted by source_state,target_state,policy_id,policy_version
duplicate source/target use denied
duplicate policy identity denied
```

Each closed entry:

```text
policy_id
policy_version
source_state
target_state
requires_human_result
requires_post_human_evidence
deterministic_kind
evidence_basis_kind
evidence_checkpoint_ref
evidence_requirement_set_ref
```

Use the exact accepted type/domain/cross-field rules in:

```text
JUDGMENT_BINDING_CORRECTION_PROPOSAL.md
```

Do NOT store in TaskContract:

```text
runtime policy fingerprint
target_use_fingerprint
authority revision/token
Judgment ref/result
runtime currentness boolean
issued_at
```

A trusted adapter may, after durable TaskContract issuance and before new READY, call existing:

```text
JudgmentPolicyAuthority.register(...)
```

with exact verified-body configuration.

Existing owner generates/persists/verifies:

```text
JudgmentPolicyRow / ProjectionRow
policy fingerprint
target_use_fingerprint
authority revision/currentness
serialized_ref
Judgment
```

No second Judgment policy registry/table/fingerprint algorithm.

Registration is not a Judgment and creates no `G_JUDGMENT_*` fact.

# 10. Human/Judgment cross-object consistency

Implement fail-closed exact consistency:

```text
human kind REQUIRED
<-> judgment owner_policy HUMAN
<-> every judgment policy requires_human_result = true

human kind NOT_REQUIRED
<-> judgment owner_policy in {SYSTEM_DETERMINISTIC, COMMAND_CENTER}
<-> every judgment policy requires_human_result = false
```

Mixed Human/non-Human outcome configuration is not represented by V1 and must be rejected.

Human required-use coverage and Judgment transition-use coverage must be exact/current existing transition uses only.

Do not infer missing coverage.

# 11. existing P1-7 owner composition only

P1-7 source/rules are READ-ONLY.

A trusted adapter inside the Task authority boundary may derive owner configuration only from an owner-verified immutable TaskContract body.

Preferred implementation location:

```text
src/aiscc/task_authority/ready.py
```

Equivalent internal decomposition within allowed `task_authority` paths is acceptable.

It must NOT accept:

```text
arbitrary caller authority factories
Agent-supplied body dicts
caller callbacks treated as authority
private-attribute mutation of configured P1-7 owners
caller-computed runtime policy fingerprints
```

Human owner composition:

- construct existing `HumanGateReservationAuthority` using verified config;
- do not reserve/open a gate at `NONE -> READY`;
- no Human principal authentication at READY;
- later real request uses existing `reserve(...)`;
- actual gate fingerprint comes from real run/request/state/policy/purpose/selector;
- existing `HumanGuardAuthority` + current P1-6 PRE_HUMAN evidence owns gate-open guard.

Judgment owner composition:

- register verified exact policies using existing `JudgmentPolicyAuthority`;
- exact registration may be idempotently replayed after restart;
- changed existing config/currentness must fail closed;
- actual request-time currentness remains existing owner responsibility;
- READY must not pretend future request currentness or mint Judgment guard facts.

# 12. durable-body implementation contract

All unchanged accepted 0319 + 0812 requirements remain.

At minimum implement:

```text
TaskContractBodyV1
IssuedTaskContractV1
VerifiedTaskContractBindingV1
TaskContractBodyRow
```

Correct deterministic identity helper:

```text
derive_task_contract_body_ref(project_id, contract_id, contract_version)
```

Semantics:

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

exact length:
93 ASCII chars
```

Content integrity:

```text
body_sha256 = SHA256(canonical_body)
constraint_payload_fingerprint = body_sha256
constraint_payload_ref = body_ref
```

Do not modify `TaskConstraintRefV1` or its validator.

Whole body closed/recursively immutable; exact restricted JCS; safe integers; NFC/domain/path validation; accepted evidence/repository/NextAction/execution-provenance bindings.

Issuance/read/revoke/verify/version/idempotency/currentness semantics remain exactly as accepted in 0319 + 0812.

# 13. exact mutation allowlist

Canonical rules:

```text
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

Product/runtime:

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
src/aiscc/human/**
src/aiscc/judgment/**
AISCC_HUMAN_GATE_JUDGMENT.md
AISCC_EVIDENCE_ADMISSION.md
```

If a different mutation path is required:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

STOP before modifying it.

If correct implementation requires semantic P1-7 source/rule changes:

```text
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

STOP.

# 14. migration

Pre-migration require:

```text
single Alembic head = 20260901_0008
20260914_0009 absent
```

Otherwise:

```text
MIGRATION_BASELINE_MISMATCH
```

Create exactly:

```text
migrations/versions/20260914_0009_task_contract_durable_bodies.py

revision = 20260914_0009
down_revision = 20260901_0008
```

Implement accepted additive design:

- one new `task_contract_bodies` table;
- no existing table alteration;
- no backfill;
- immutable UPDATE/DELETE trigger;
- no-TRUNCATE trigger;
- canonical_body BYTEA;
- identity/ref/hash/predecessor constraints;
- no pgcrypto requirement;
- empty-only downgrade;
- nonempty downgrade fail-closed preserving rows/schema/revision.

Stored V1 `body_ref` must satisfy/recompute exact 93-character hashed identity.

# 15. isolated PostgreSQL 17.6 proof

First:

```text
"C:\Program Files\Docker\Docker\resources\bin\docker.exe" image inspect postgres:17.6
```

If image absent:

```text
ISOLATED_POSTGRES_IMAGE_MISSING
```

Do NOT pull.

Use new Task-owned disposable container only, e.g.:

```text
aiscc-p2-4-taskcontract-0923-pg
```

Synthetic credentials, bind only `127.0.0.1` on a free local port.

Required DB/runtime proof:

1. empty DB -> migration head PASS;
2. predecessor 0008 -> 0009 PASS;
3. restart/reload preserves exact body/ref/hash;
4. 96/96 project/contract IDs persist with exact 93-char ref;
5. exact retry idempotent;
6. conflicting same-version body denied;
7. concurrent issuance/version race deterministic;
8. write-boundary rollback leaves no partial body/ref/event authority;
9. UPDATE/DELETE/TRUNCATE body row denied;
10. empty downgrade PASS;
11. nonempty downgrade FAIL-CLOSED preserving schema/row/revision;
12. process/service reconstruction verifies without in-memory body objects;
13. corrected Human NOT_REQUIRED config reload/verify PASS;
14. corrected Human REQUIRED config reload/verify PASS;
15. verified Judgment config registers idempotently through existing owner and reloads exact existing owner fingerprint/currentness;
16. READY preparation with REQUIRED/NOT_REQUIRED creates no HumanResult/Judgment/G_HUMAN/G_JUDGMENT fact;
17. no P1-7 table/schema/source mutation beyond its existing runtime effects through existing public owner API.

Cleanup exact Task container best-effort only; failure is nonblocking residue.

No Docker prune.

# 16. tests

Required new/updated tests:

```text
tests/unit/task_authority/test_task_contract_body.py
tests/unit/task_authority/test_task_contract_issuance.py
tests/integration/task_authority/test_task_contract_durability.py
tests/integration/task_authority/test_task_contract_ready.py
```

All PASS.

Must cover at minimum:

### body/ref

- 96/96 ID -> exact 93-char body_ref;
- same identity/version -> same ref;
- changed project/contract/version -> different ref;
- same identity/version same body -> idempotent;
- same identity/version changed body -> deny;
- tampered ref/hash/body -> deny;
- existing `TaskConstraintRefV1` constructor accepts corrected ref unchanged.

### Human config

- unknown/missing fields deny;
- REQUIRED/NOT_REQUIRED exact null/list rules;
- selector is enrolled server-key semantics, not recomputed digest;
- REQUIRED missing bypass coverage deny;
- NOT_REQUIRED with Human owner deny;
- REQUIRED with non-Human owner deny;
- reserve-at-READY absent source state remains denied/not performed;
- TaskContract config cannot create/authenticate HumanResult.

### Judgment config

- closed exact entries;
- duplicate transition use/policy identity deny;
- SYSTEM/HUMAN/COMMAND_CENTER register cross-field rules;
- deterministic_kind/target consistency;
- evidence basis/ref consistency;
- registration via existing `JudgmentPolicyAuthority` only;
- no caller runtime fingerprint injection;
- exact registration replay idempotent;
- changed config/stale current projection deny;
- policy registration != Judgment != guard fact.

### cross-owner

- REQUIRED iff Human owner / requires_human_result true;
- NOT_REQUIRED iff non-Human owner / false;
- mixed configuration deny;
- body hash authenticates config bytes but does not substitute runtime owner fingerprints;
- legacy proposed policy_fingerprint shape not silently accepted.

Run directly affected existing narrow regressions for:

```text
task_authority
P1-4 READY/transition
P1-7 HumanGate/Judgment
```

Inventory exact paths/counts before execution; do not change P1-7 tests/source unless listed as existing read/run only.

Static:

```text
Ruff changed Python
compile changed Python
git diff --check
UTF-8/control-character/Markdown checks changed canonical docs
```

# 17. forbidden

Forbidden:

```text
modify src/aiscc/task_authority/models.py
modify src/aiscc/human/**
modify src/aiscc/judgment/**
modify AISCC_HUMAN_GATE_JUDGMENT.md
modify AISCC_EVIDENCE_ADMISSION.md
new Human/Judgment policy registry/table
new P1-7 fingerprint algorithm
widen TaskConstraintRefV1/_ID
narrow 96-char body ID domain
actual self-dogfood golden cycle
real self-dogfood Task issuance
src/aiscc/self_dogfood/** mutation
stockroom/P2-3 replay mutation
CURRENT_STATE_SUMMARY/DECISION_REGISTER/NEXT_ACTIONS mutation
retained/private PostgreSQL
external network
Docker image pull
provider/LLM
push/deploy/automatic merge
```

# 18. Result Commit B

Only after all required evidence PASS.

Stage exactly changed paths within section 13.

Commit message exactly:

```text
feat(aiscc): add durable taskcontract authority
```

Require:

```text
Commit B parent = Governance Commit A
no path outside allowed mutation set
P1-7 source/rules unchanged
task_authority/models.py unchanged
index empty
tracked clean
```

If any required proof fails:

```text
no Commit B
```

Preserve truthful Task-owned work/evidence; do not broad-reset merely for cleanliness.

# 19. evidence contract

executor_required:

- inbound ZIP/hash/archive/member safety;
- all accepted design/input hashes;
- exact initial repository/state/legacy preflight;
- exact Governance Commit A;
- canonical baseline adoption;
- migration implementation;
- corrected body/Human/Judgment implementation;
- existing-owner composition proof;
- all required unit/integration and directly affected regressions;
- isolated PostgreSQL proof;
- static checks;
- exact Commit B only on complete pass;
- terminal Git/export integrity.

human_owned:

```text
already provided:
0319 durable-body design ACCEPT
0812 body_ref correction ACCEPT
0902 Human/Judgment binding correction ACCEPT

future:
runtime candidate acceptance
self-dogfood source/golden-cycle acceptance
release/submission
```

not_required:

- browser QA;
- provider/network;
- actual self-dogfood cycle;
- public deployment;
- unrelated full-suite execution solely for report padding.

# 20. mandatory stop

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

After blocker, only minimal evidence/workspace report/export/safe termination.

# 21. report/export

Target:

```text
.aiassistant/reports/target/20260914_0923_aiscc-p2-4-taskcontract-durable-body-human-judgment-corrected-runtime-implementation-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ACCEPTED_DESIGN_INPUT_VERIFICATION.md
HUMAN_JUDGMENT_CORRECTION_ACCEPTANCE_VERIFICATION.md
BODY_REF_COMPATIBILITY_EVIDENCE.md
HUMAN_JUDGMENT_BINDING_EVIDENCE.md
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
.aiassistant/reports/target/20260914_0923_aiscc-p2-4-taskcontract-durable-body-human-judgment-corrected-runtime-implementation-retry-1.zip
```

# 22. terminal repository boundary

Complete success:

```text
HEAD = Result Commit B
index = empty
tracked = clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_0923_aiscc-p2-4-taskcontract-durable-body-human-judgment-corrected-runtime-implementation-retry-1.md
```

Current Task active -> done byte-identically.

Legacy 1400 Task exact unchanged.

Canonical state hashes section 2 unchanged.

Blocked/failure:

- no Result Commit B;
- truthful changed-path inventory;
- no broad cleanup/reset;
- Docker cleanup remains best-effort housekeeping.

# 23. success ceiling

Complete PASS may report only:

```text
P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do NOT claim:

```text
P2_4_SELF_DOGFOOD_ENTRY_SOURCE_CANDIDATE
P2-4 ACCEPTED/CLOSED
golden self-dogfood complete
```

State ceiling:

```text
P2-3:
ACCEPTED / CLOSED

P2-4:
IN_PROGRESS

durable-body base design:
HUMAN_PROVIDED / ACCEPTED

0812 body_ref correction:
HUMAN_PROVIDED / ACCEPTED

0902 Human/Judgment binding correction:
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
