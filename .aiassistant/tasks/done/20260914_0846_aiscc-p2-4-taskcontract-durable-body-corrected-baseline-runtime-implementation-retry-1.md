# 작업지시서: P2-4 corrected durable TaskContract baseline + runtime implementation retry

## meta

- task_id: `20260914_0846_aiscc-p2-4-taskcontract-durable-body-corrected-baseline-runtime-implementation-retry-1`
- created_at: `2026-09-14T08:46:19+09:00`
- work_type: `DOC_BASELINE_UPDATE + BACKEND_IMPLEMENTATION + DATABASE_MIGRATION + QA_ONLY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `4685cff66a0ff42f53db66567f6f5a2340ccbef8`
- required_parent: `4c61beec858777a78b88af5f8fbd51148968febe`
- predecessor_result_zip: `20260914_0756_aiscc-p2-4-taskcontract-durable-body-baseline-adoption-runtime-implementation-1.zip`
- predecessor_result_zip_sha256: `114a92aa27fab1e26524371516502cd7fb1cb8a8bf84869873001f1234a7357f`
- predecessor_done_task_sha256: `ac07fba6d774e0e54d4a60e129bb03f3b3c0af1980d1dc78f7d06fc1e3caebee`
- predecessor_result: `BLOCKED / POLICY_CONFLICT_INVESTIGATION_REQUIRED`
- predecessor_executor_disposition: `ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED`
- command_center_defect: `ACCEPTED_DESIGN_COMPATIBILITY_VALIDATION_MISSED`
- human_correction_decision: `HUMAN_PROVIDED / ACCEPT`
- human_correction_artifact_sha256: `4c6905734e7a48b9688257574d86b1a7215627ac8514c7112747889c6bafa318`
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

# 0. predecessor judgment and Human correction

0756 stopped before implementation because the Human-accepted proposal contained an exact compatibility defect:

```text
project_id / contract_id:
each allowed up to 96 characters

old body_ref:
task-contract-body:v1:<project_id>:<contract_id>:v<n>

TaskConstraintRefV1.constraint_payload_ref:
existing _ID max length = 160
```

Observed probe:

```text
67-char + 67-char IDs -> body_ref length 160 -> PASS
68-char + 68-char IDs -> body_ref length 162 -> DENY
96-char + 96-char IDs -> body_ref length 218 -> DENY
```

Browser Command Center owns this missed compatibility validation. It is not an Executor or existing-product regression.

Human then approved the exact correction artifact:

```text
20260914_0812_aiscc-p2-4-durable-taskcontract-body-ref-compatibility-human-correction-review-1.md
SHA-256:
4c6905734e7a48b9688257574d86b1a7215627ac8514c7112747889c6bafa318

Human decision:
ACCEPT
```

Therefore the existing durable-body design remains accepted except for the superseded `body_ref` derivation below.

# 1. normative accepted inputs

After reading this Task, place package design inputs only in:

```text
.aiassistant/reports/target/20260914_0846_aiscc-p2-4-taskcontract-durable-body-corrected-baseline-runtime-implementation-retry-1/accepted-input/
```

Do not put raw design inputs into tracked canonical paths.

Base accepted design files:

- `TASKCONTRACT_DURABLE_BODY_BASELINE_PROPOSAL.md`: `803686433f900282117a4318d8f59a14b5b5a68735775b4f1242acf544c16410`
- `BASELINE_SUPERSESSION_MAP.md`: `8c0ee1a8b320dc8789092d027350f097b288468893b02571fa26ca4ed5d57824`
- `MIGRATION_DESIGN.md`: `6a41b8a58616950d74fb5f0d1acb4b9ca869fc43cbbc9f919262f95922a4f4f1`
- `IMPLEMENTATION_PATH_ALLOWLIST.md`: `b5c8ccc8e646982605e700bfe4783f79d30bcb6dab6bd1ed17cb1a22b2c14956`
- `RISK_AND_ROLLBACK.md`: `9604a77e2f55c53661d239bfeb32ebe3c7ec11007553527c9518c745a25fa32e`
- `SOURCE_AUTHORITY_AUDIT.md`: `4fde5c38e1dc0e8b6e4860fbf1a6560e88e3a61644f6da48da6cde2ff03293f8`
- `CURRENT_SCHEMA_AUDIT.md`: `bf0402c9249dfb302175b2d9805ce1b87cf2236cd6541a14d115746e4319576d`

Superseding correction:

```text
20260914_0812_aiscc-p2-4-durable-taskcontract-body-ref-compatibility-human-correction-review-1.md
SHA-256:
4c6905734e7a48b9688257574d86b1a7215627ac8514c7112747889c6bafa318
```

Precedence:

```text
0812 correction artifact
> old body_ref derivation in the 0319 accepted proposal

all other 0319 Human-accepted proposal semantics:
unchanged
```

If any input is missing/mismatched -> `BLOCKED_MISSING_ARTIFACT` and STOP before governance/source mutation.

# 2. corrected body_ref contract — exact

Preserve unchanged:

```text
project_id:
[A-Za-z0-9][A-Za-z0-9_.-]{0,95}

contract_id:
[A-Za-z0-9][A-Za-z0-9_.-]{0,95}

TaskConstraintRefV1:
unchanged

existing _ID validator:
unchanged

unknown_fields=DENY:
unchanged
```

Superseding body identity:

```text
body_identity_object = {
  "project_id": project_id,
  "contract_id": contract_id,
  "contract_version": n
}

body_identity_bytes =
existing canonical JSON/JCS encoding of body_identity_object

body_identity_sha256 =
lowercase SHA-256 hex of body_identity_bytes

body_ref =
"task-contract-body:v1:sha256:" + body_identity_sha256
```

Exact valid result:

```text
ASCII length = 93
pattern = task-contract-body:v1:sha256:<64 lowercase hex>
```

The body identity digest is NOT the body-content digest.

Content integrity remains independently:

```text
body_sha256 = SHA256(canonical_body)

constraint_payload_fingerprint = body_sha256
constraint_payload_ref = body_ref
```

Same `(project_id, contract_id, contract_version)` must recompute the same `body_ref`.

Same identity + different body content:

```text
same body_ref
different body_sha256
=> conflicting same-version content
=> DENY
```

Do not:

```text
widen _ID
edit TaskConstraintRefV1 validation
truncate IDs
narrow the accepted 96-character ID domain
bypass __post_init__
introduce caller aliases
put identity/body fields into the V1 envelope
```

# 3. executables

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Use only:

```text
Python:
<repository-root>\.venv\Scripts\python.exe

Git:
C:\Program Files\Git\cmd\git.exe

Docker:
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

Docker is authorized only for the exact isolated PostgreSQL proof in section 14.

Forbidden discovery/use:

```text
python
py
WindowsApps
PATH/external Python
alternate Git/Docker
```

If repository `.venv\Scripts\python.exe` is absent, STOP.

# 4. exact initial repository preflight

Require before governance placement/mutation:

```text
branch:
main

HEAD:
4685cff66a0ff42f53db66567f6f5a2340ccbef8

HEAD^:
4c61beec858777a78b88af5f8fbd51148968febe

index:
empty

tracked:
clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0756_aiscc-p2-4-taskcontract-durable-body-baseline-adoption-runtime-implementation-1.md

SHA-256:
ac07fba6d774e0e54d4a60e129bb03f3b3c0af1980d1dc78f7d06fc1e3caebee
```

Preserve ignored legacy Task:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Canonical state initially and terminally byte-exact:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48

.aiassistant/records/aiscc/DECISION_REGISTER.md
9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5

.aiassistant/records/aiscc/NEXT_ACTIONS.md
050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679
```

Any mismatch -> STOP before mutation.

# 5. inbound governance placement

Delivery contains:

```text
20260914_0846_aiscc-p2-4-taskcontract-durable-body-corrected-baseline-runtime-implementation-retry-1.md
20260914_0846_aiscc-p2-4-body-ref-compatibility-human-accepted-implementation-retry-entry-1.cycle.md
20260914_0846_aiscc-p2-4-body-ref-compatibility-human-acceptance-implementation-reauthorization-1.md
20260914_0812_aiscc-p2-4-durable-taskcontract-body-ref-compatibility-human-correction-review-1.md
ACCEPTED_DESIGN/<7 exact files>
```

Transport:

```text
verify ZIP/hash/archive/path safety
→ put TASK into .aiassistant/tasks/active
→ read TASK
→ verify accepted input/correction hashes
→ stage raw design inputs in ignored target only
→ place Cycle/Judgment/correction review into canonical governance paths
```

Canonical governance placement:

```text
20260914_0846_aiscc-p2-4-body-ref-compatibility-human-accepted-implementation-retry-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_0846_aiscc-p2-4-body-ref-compatibility-human-acceptance-implementation-reauthorization-1.md
-> .aiassistant/reports/aiscc/

20260914_0812_aiscc-p2-4-durable-taskcontract-body-ref-compatibility-human-correction-review-1.md
-> .aiassistant/reports/aiscc/
```

The canonical correction review copy must remain byte-exact to the Human-approved artifact.

# 6. Governance Commit A — blocker + Human correction provenance

After placement, Git-visible untracked exactly:

```text
.aiassistant/tasks/done/20260914_0756_aiscc-p2-4-taskcontract-durable-body-baseline-adoption-runtime-implementation-1.md
.aiassistant/records/aiscc/cycles/20260914_0846_aiscc-p2-4-body-ref-compatibility-human-accepted-implementation-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_0846_aiscc-p2-4-body-ref-compatibility-human-acceptance-implementation-reauthorization-1.md
.aiassistant/reports/aiscc/20260914_0812_aiscc-p2-4-durable-taskcontract-body-ref-compatibility-human-correction-review-1.md
```

Stage exactly those four.

Commit message exactly:

```text
docs(aiscc): correct durable taskcontract body ref
```

Require:

```text
Commit A parent = 4685cff66a0ff42f53db66567f6f5a2340ccbef8
changed paths = exact 4
index empty after commit
tracked clean after commit
Git-visible untracked = 0
```

No product/baseline mutation before this exact commit.

# 7. minimum authoritative reads

Read exact:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Read current `src/aiscc/task_authority/models.py` but do not modify it.

Verify before implementation that the corrected 93-char body_ref passes the existing constructor without validator change.

If it does not -> `CORRECTION_COMPATIBILITY_FAILED` and STOP.

# 8. canonical baseline adoption — exact allowed rule paths

Create/modify only:

```text
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

Promote the 0319 accepted design plus 0812 correction.

New canonical rule must explicitly define the corrected hashed `body_ref`.

Preserve exactly:

```text
TaskIssuanceCandidate != TaskContract
TaskContract owner = EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
TaskConstraintRefV1 unchanged
existing _ID limit unchanged
unknown_fields=DENY unchanged
project_id/contract_id 96-char accepted domain unchanged
WorkRun/System ownership unchanged
P1-6 evidence/checkpoint ownership unchanged
P1-7 Human/Judgment ownership unchanged
P1-4 Transition/WorkflowState ownership unchanged
```

Do not mutate:

```text
AISCC_EVIDENCE_ADMISSION.md
Security baseline
CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md
```

# 9. exact source/migration/test allowlist

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

`src/aiscc/task_authority/models.py` is READ-ONLY evidence, not mutation scope.

Any additional required mutation -> `SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED` and STOP before modifying it.

# 10. implementation contract

Implement the Human-accepted durable-body design with the corrected identity ref.

At minimum:

```text
TaskContractBodyV1
IssuedTaskContractV1
VerifiedTaskContractBindingV1
TaskContractBodyRow
```

Body:

- closed schema;
- recursively immutable;
- deterministic canonical JSON/JCS;
- exact integer safety;
- SHA-256 body fingerprint;
- all accepted repository/NextAction/scope/evidence/Human/Judgment/execution provenance bindings;
- no default/ambiguous Human requirement.

Required deterministic helper semantics:

```text
derive_task_contract_body_ref(project_id, contract_id, contract_version)
```

Equivalent naming is allowed only inside the accepted public owner surface.

It MUST:

1. validate the existing accepted ID/version domain;
2. canonicalize exactly the three identity fields;
3. SHA-256 the canonical identity bytes;
4. return the exact 93-character `task-contract-body:v1:sha256:<hex>` ref;
5. be recomputed on read/verify from persisted identity columns;
6. deny persisted/ref mismatch.

TaskConstraint V1 linkage:

```text
constraint_schema_id = AISCC-TASKCONTRACT-BODY-V1
constraint_schema_version = v1
constraint_payload_ref = corrected body_ref
constraint_payload_fingerprint = body_sha256
```

Do not modify the V1 envelope/model validator.

Issuance/read/revoke/verify API and transaction/version/idempotency semantics remain exactly those in the 0319 accepted proposal.

# 11. corrected compatibility proof — required before broader runtime proof

Required unit negatives/positives:

```text
96-char project_id + 96-char contract_id
-> exact 93-char body_ref
-> existing TaskConstraintRefV1 constructor PASS without modification

67/68/96-character boundary examples
-> all corrected refs length 93

same identity/version
-> same body_ref

different project
-> different body_ref

different contract
-> different body_ref

different version
-> different body_ref

same identity/version + same body
-> exact idempotent retry

same identity/version + different body_sha256
-> DENY conflicting content

tampered body_ref digest
-> DENY

persisted identity columns whose recomputed body_ref != stored body_ref
-> DENY
```

Hash collision handling remains SHA-256 identity semantics; do not introduce collision recovery aliases.

# 12. P1-6 / Human / Judgment non-substitution

Preserve accepted 0756 Task section semantics:

```text
READY does not satisfy G_EVIDENCE
READY does not create HumanResult
READY does not create Judgment
EvidenceCheckpoint remains existing P1-6 authority
Human/Judgment references are bindings only
P1-4 remains sole transition mutation owner
```

If implementation needs P1-6/P1-7 semantic changes -> `AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED` and STOP.

# 13. READY integration

Implement `TaskContractReadyParticipant` through existing P1-4 participant/kernel surfaces only.

Must verify the corrected body_ref by recomputation as part of durable binding verification.

Still require:

- current issued body/prefix under family lock;
- exact project/contract/version/repository/base/NextAction/scope bindings;
- stale/revoked deny;
- legacy ref-only contracts denied for the new entrypoint;
- no WorkRun schema/backfill;
- no new state/guard authority.

Authority locator remains:

```text
task-contract-admission:v1:<body_sha256>:<snapshot_ref>
```

and is not itself authority.

# 14. migration + isolated PostgreSQL proof

Pre-migration require:

```text
Alembic single head = 20260901_0008
20260914_0009 absent
```

Create only:

```text
migrations/versions/20260914_0009_task_contract_durable_bodies.py

revision = 20260914_0009
down_revision = 20260901_0008
```

Implement the accepted additive table/immutability/no-backfill/empty-only-downgrade design.

The `body_ref` column may retain the accepted 512-character storage bound; stored values for V1 must nevertheless satisfy the corrected exact 93-character format and recomputation rule.

Isolated PostgreSQL:

```text
Docker image:
postgres:17.6

Docker executable:
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

First local image inspect only. If image absent, do not pull; STOP `ISOLATED_POSTGRES_IMAGE_MISSING`.

Use one new task-owned disposable container, for example:

```text
aiscc-p2-4-taskcontract-0846-pg
```

Bind only `127.0.0.1` with synthetic credentials.

Required runtime proof:

1. empty DB -> head PASS;
2. predecessor 0008 -> 0009 PASS;
3. restart/reload exact body/ref/hash PASS;
4. 96/96 identity persisted and verified through unchanged V1 constructor;
5. exact retry idempotent;
6. conflicting same-version content deny;
7. concurrent issue/version race deterministic;
8. rollback at write boundaries leaves no partial authority;
9. UPDATE/DELETE/TRUNCATE denied;
10. empty downgrade PASS;
11. nonempty downgrade FAIL-CLOSED preserving schema/row/revision;
12. reconstruction without in-memory objects verifies exact body + recomputed identity ref.

No retained/private DB, external network, provider or secrets.

# 15. tests/static

Required new test files:

```text
tests/unit/task_authority/test_task_contract_body.py
tests/unit/task_authority/test_task_contract_issuance.py
tests/integration/task_authority/test_task_contract_durability.py
tests/integration/task_authority/test_task_contract_ready.py
```

All PASS.

Also run directly affected existing narrow task-authority/P1-4 owner regressions discovered from current source. Record exact paths/counts.

Required negatives from 0756 remain, plus all corrected identity-ref tests in section 11.

Static:

```text
Ruff changed Python
compile changed Python
git diff --check
UTF-8/control-character/Markdown checks for changed canonical docs
```

# 16. forbidden

Forbidden:

```text
modify src/aiscc/task_authority/models.py
widen existing _ID limit
narrow project/contract ID domain
actual self-dogfood golden cycle
real active self-dogfood Task issuance
src/aiscc/self_dogfood/** mutation
stockroom/P2-3 Replay mutation
CURRENT_STATE_SUMMARY/DECISION_REGISTER/NEXT_ACTIONS mutation
P1-6/P1-7 semantic baseline mutation
retained/private PostgreSQL
external network
Docker image pull
provider/LLM
public deployment
push
automatic merge
```

# 17. Result Commit B

Only on complete PASS.

Stage exactly changed files within sections 8, 9 and 14.

Commit message exactly:

```text
feat(aiscc): add corrected durable taskcontract authority
```

Require:

```text
Commit B parent = Governance Commit A
changed paths subset = exact authorized allowlist
src/aiscc/task_authority/models.py unchanged
index empty
tracked clean
```

On any required failure: no Commit B.

# 18. report/export

Target:

```text
.aiassistant/reports/target/20260914_0846_aiscc-p2-4-taskcontract-durable-body-corrected-baseline-runtime-implementation-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ACCEPTED_DESIGN_INPUT_VERIFICATION.md
CORRECTION_ACCEPTANCE_VERIFICATION.md
BODY_REF_COMPATIBILITY_EVIDENCE.md
BASELINE_ADOPTION_REVIEW.md
SOURCE_CHANGE_REVIEW.md
MIGRATION_REVIEW.md
POSTGRES_RUNTIME_EVIDENCE.md
TEST_RESULTS.md
CONTRACT_REVIEW.md
```

Include changed project-relative files plus canonical current Cycle/Judgment/correction review/done Task.

No credentials/raw DB dumps/unrelated source.

Result ZIP:

```text
.aiassistant/reports/target/20260914_0846_aiscc-p2-4-taskcontract-durable-body-corrected-baseline-runtime-implementation-retry-1.zip
```

# 19. terminal repository boundary

Complete success:

```text
HEAD = Result Commit B
index = empty
tracked = clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_0846_aiscc-p2-4-taskcontract-durable-body-corrected-baseline-runtime-implementation-retry-1.md
```

Current Task active -> done byte-identically.

Legacy 1400 Task unchanged.

Canonical state hashes unchanged.

Blocked/failure:

- no Result Commit B;
- preserve truthful Task-owned working changes/evidence;
- no broad cleanup/reset.

# 20. success ceiling

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
