# 작업지시서: P2-4 TaskContract durable-body baseline adoption + runtime implementation

## meta

- task_id: `20260914_0756_aiscc-p2-4-taskcontract-durable-body-baseline-adoption-runtime-implementation-1`
- created_at: `2026-09-14T07:56:00+09:00`
- work_type: `DOC_BASELINE_UPDATE + BACKEND_IMPLEMENTATION + DATABASE_MIGRATION + QA_ONLY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `4c61beec858777a78b88af5f8fbd51148968febe`
- required_parent: `04b5dda84c7bdb975cd4a4e74b7ccf3eb7f5eb6d`
- predecessor_result_zip: `20260914_0319_aiscc-p2-4-taskcontract-durable-body-authority-baseline-design-1.zip`
- predecessor_result_zip_sha256: `1e14f5819ab16a920933ee36721c1bfaca3f7b0b601e31bfd4f91a2fade2c119`
- human_design_decision: `HUMAN_PROVIDED / ACCEPT`
- human_design_decision_at: `2026-09-14T07:56:00+09:00`
- fresh_IDE_chat_required: `No`
- governance_commit_authorized: `Yes / exact 3 paths / Commit A`
- result_commit_authorized: `Yes / exact implementation allowlist / Commit B`
- canonical_baseline_mutation_authorized: `Yes / exact 4 rule paths`
- migration_creation_authorized: `Yes / exact one migration`
- isolated_PostgreSQL_authorized: `Yes / task-owned ephemeral only`
- Docker_authorized: `Yes / exact docker executable / local postgres:17.6 image only`
- external_network_authorized: `No`
- provider_LLM_authorized: `No`
- retained_private_DB_authorized: `No`
- golden_self_dogfood_run_authorized: `No`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. Human decision / predecessor judgment

Human exact decision:

```text
ACCEPT
```

Browser Command Center interpretation:

```text
0319 durable-body proposal:
HUMAN_PROVIDED / ACCEPTED

canonical adoption:
AUTHORIZED IN THIS TASK

runtime implementation + migration:
AUTHORIZED IN THIS TASK

P2-4 self-dogfood source candidate:
NOT YET CREATED

actual golden self-dogfood cycle:
NOT AUTHORIZED IN THIS TASK
```

The accepted proposal is not an Executor suggestion anymore. Its exact bytes are bundled under `ACCEPTED_DESIGN/` and are the normative implementation input for this Task, subject only to current repository/canonical conflict stop.

# 1. exact accepted-design inputs

After reading this Task, copy/extract the following package members into the ignored target staging area only:

```text
.aiassistant/reports/target/20260914_0756_aiscc-p2-4-taskcontract-durable-body-baseline-adoption-runtime-implementation-1/accepted-input/
```

Do NOT place these raw proposal files into tracked canonical paths.

Expected SHA-256:

- `TASKCONTRACT_DURABLE_BODY_BASELINE_PROPOSAL.md`: `803686433f900282117a4318d8f59a14b5b5a68735775b4f1242acf544c16410`
- `BASELINE_SUPERSESSION_MAP.md`: `8c0ee1a8b320dc8789092d027350f097b288468893b02571fa26ca4ed5d57824`
- `MIGRATION_DESIGN.md`: `6a41b8a58616950d74fb5f0d1acb4b9ca869fc43cbbc9f919262f95922a4f4f1`
- `IMPLEMENTATION_PATH_ALLOWLIST.md`: `b5c8ccc8e646982605e700bfe4783f79d30bcb6dab6bd1ed17cb1a22b2c14956`
- `RISK_AND_ROLLBACK.md`: `9604a77e2f55c53661d239bfeb32ebe3c7ec11007553527c9518c745a25fa32e`
- `SOURCE_AUTHORITY_AUDIT.md`: `4fde5c38e1dc0e8b6e4860fbf1a6560e88e3a61644f6da48da6cde2ff03293f8`
- `CURRENT_SCHEMA_AUDIT.md`: `bf0402c9249dfb302175b2d9805ce1b87cf2236cd6541a14d115746e4319576d`

If any accepted input is missing or mismatched -> `BLOCKED_MISSING_ARTIFACT` and STOP before governance/source mutation.

Accepted design ID:

```text
AISCC-TASKCONTRACT-DURABLE-BODY-V1
```

Key accepted decision:

```text
existing owner:
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY

TaskConstraintRefV1:
unchanged
unknown_fields=DENY remains exact

whole TaskContract body:
new immutable/versioned restart-surviving dedicated authority

preferred persistence:
append-only task_contract_bodies table

legacy rows:
no backfill

P1-4/P1-6/P1-7/P1-8 semantic owners:
unchanged
```

# 2. executables

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Python — only:

```text
<repository-root>\.venv\Scripts\python.exe
```

Git — only:

```text
C:\Program Files\Git\cmd\git.exe
```

Docker — only for the isolated PostgreSQL proof in section 13:

```text
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

Forbidden discovery/use:

```text
python
py
WindowsApps aliases
PATH/external Python discovery
another Git executable
another Docker executable
```

If repository Python is absent, STOP. Do not search for another interpreter.

# 3. exact initial repository preflight

Before governance placement or mutation require:

```text
branch:
main

HEAD:
4c61beec858777a78b88af5f8fbd51148968febe

HEAD^:
04b5dda84c7bdb975cd4a4e74b7ccf3eb7f5eb6d

index:
empty

tracked worktree:
clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0319_aiscc-p2-4-taskcontract-durable-body-authority-baseline-design-1.md

SHA-256:
439f37d13868b5ac30ee0ae40d5bfdaf4517f168010fc01df4963475132397b1
```

Ignored legacy active Task must remain byte-exact:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md

SHA-256:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Current canonical state files must initially be byte-exact and remain unchanged in this Task:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48

.aiassistant/records/aiscc/DECISION_REGISTER.md
9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5

.aiassistant/records/aiscc/NEXT_ACTIONS.md
050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679
```

Any mismatch -> STOP before source mutation and report exact actual state.

# 4. inbound governance placement

Delivery package contains:

```text
20260914_0756_aiscc-p2-4-taskcontract-durable-body-baseline-adoption-runtime-implementation-1.md
20260914_0756_aiscc-p2-4-taskcontract-durable-body-design-human-accepted-implementation-entry-1.cycle.md
20260914_0756_aiscc-p2-4-taskcontract-durable-body-design-human-acceptance-implementation-authorization-1.md
ACCEPTED_DESIGN/<7 exact accepted input files>
```

Transport order:

```text
verify ZIP SHA/archive/member safety
→ place current Task into .aiassistant/tasks/active
→ read current Task
→ hash/stage accepted-design inputs in ignored reports/target staging
→ place Cycle/Judgment into canonical paths
```

Canonical placement:

```text
20260914_0756_aiscc-p2-4-taskcontract-durable-body-design-human-accepted-implementation-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_0756_aiscc-p2-4-taskcontract-durable-body-design-human-acceptance-implementation-authorization-1.md
-> .aiassistant/reports/aiscc/
```

Do not place accepted-design raw input files into tracked repository paths.

# 5. Governance Commit A — Human acceptance provenance

After exact preflight and governance placement, Git-visible untracked must be exactly:

```text
.aiassistant/tasks/done/20260914_0319_aiscc-p2-4-taskcontract-durable-body-authority-baseline-design-1.md
.aiassistant/records/aiscc/cycles/20260914_0756_aiscc-p2-4-taskcontract-durable-body-design-human-accepted-implementation-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_0756_aiscc-p2-4-taskcontract-durable-body-design-human-acceptance-implementation-authorization-1.md
```

Stage exactly those three paths.

Commit message exactly:

```text
docs(aiscc): accept durable taskcontract authority
```

Require:

```text
Commit A parent = 4c61beec858777a78b88af5f8fbd51148968febe
changed paths = exact 3
index empty after commit
tracked clean after commit
Git-visible untracked = 0
```

Current active Task remains ignored.

If exact set cannot be established, STOP before product/baseline mutation.

# 6. minimum authoritative context

Read exact canonical files:

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

Then inspect only implementation-owner source required by the accepted input and exact allowed paths.

Conflict rule:

```text
accepted proposal + Human ACCEPT
!= permission to override contradictory current canonical/source facts
```

If a current canonical/source fact proves the accepted proposal cannot be implemented without changing an unapproved semantic owner, STOP with:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not silently redesign.

# 7. canonical baseline adoption — exact allowed rule paths

Create/modify only:

```text
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

Requirements:

1. New `AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md` must promote the Human-accepted normative semantics of `TASKCONTRACT_DURABLE_BODY_BASELINE_PROPOSAL.md` without semantic omission or expansion.
2. Architecture update is a bounded cross-reference + complete-body durability clarification only.
3. Orchestration update is a prospective body-backed READY verification cross-reference only. Do NOT change the nine-state set or existing transition/guard ownership.
4. P1-8 prerequisite authority update is additive whole-body payload schema / higher-level issuance-currentness reference only. Do NOT change V1 schema/hash/event/carrier/source equality.
5. Do NOT modify `AISCC_EVIDENCE_ADMISSION.md`, Human/Judgment rules, Security baseline, current state files or Decision Register in this Task.
6. Korean-first document policy applies; identifiers/types remain exact English.

The new canonical rule must explicitly preserve:

```text
TaskIssuanceCandidate != TaskContract
TaskContract owner = EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
TaskConstraintRefV1 semantics unchanged
unknown_fields=DENY unchanged
WorkRun owner = System
EvidenceCheckpoint / Evidence admission = existing P1-6 owner
HumanGate/HumanResult/Judgment = existing P1-7 owner
TransitionDecision/WorkflowState = existing P1-4 owner
```

# 8. exact product/migration/test mutation allowlist

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

No other source/test/migration/config path may be modified.

If safe implementation genuinely requires another path:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

STOP before modifying it.

Read-only inspection of directly imported owner code/tests is allowed as needed; modification is not.

# 9. implementation contract

Implement the accepted proposal exactly, including at minimum:

```text
TaskContractBodyV1
IssuedTaskContractV1
VerifiedTaskContractBindingV1
TaskContractBodyRow
```

Whole body:

- closed schema, recursively immutable;
- deterministic canonical bytes through existing canonical JSON/JCS machinery;
- SHA-256 body fingerprint;
- exact IDs/version/body refs;
- explicit evidence/Human/Judgment/repository/NextAction/execution-provenance bindings;
- no default/omitted Human requirement;
- scope path validation and overlap denial exactly as accepted proposal specifies.

TaskConstraint V1 linkage:

```text
constraint_schema_id = AISCC-TASKCONTRACT-BODY-V1
constraint_schema_version = v1
constraint_payload_ref = body_ref
constraint_payload_fingerprint = body_sha256
```

Do not add fields to the V1 envelope.

Writer/read boundary:

```text
issue_task_contract(...)
revoke_task_contract(...)
get_task_contract(...)
verify_task_contract(...)
```

Exact names may match accepted proposal naming; do not introduce a competing public writer.

Issuance:

- same owner capability as existing external authority;
- one transaction for V1 ref/event + body row;
- version family serialized;
- exact idempotency;
- conflicting same-version bytes reject;
- n>1 replacement = old version REVOKED + new version ISSUED atomically;
- explicit latest-family revoke closes family;
- no V1 SUPERSEDED cross-version shortcut.

Restart/read verification must reject tamper/missing/ref-event-prefix mismatch and must never auto-repair/backfill.

# 10. P1-6 / Human / Judgment non-substitution

The accepted design binds existing references; it does not create their semantic results.

Implementation MUST preserve:

```text
EvidenceCheckpoint:
existing System/TaskContract-owned P1-6 identity

RequirementSet/checkpoint applicability:
existing P1-6 authority

READY:
does NOT satisfy G_EVIDENCE
does NOT create HumanResult
does NOT create Judgment

Human binding:
policy/requirement reference only

Judgment binding:
owner policy/reference only
```

If implementation would require changing P1-6 schema/runtime semantics or P1-7 Human/Judgment semantics, STOP:

```text
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

# 11. READY integration

Implement `TaskContractReadyParticipant` using existing P1-4 transaction participant/kernel interfaces.

Must preserve:

```text
WorkflowKernel / repository:
sole state mutation owner

P1_4GuardAuthority:
sole owner of existing G_CONTRACT/G_SCOPE/G_RUNTIME_CONTEXT facts

TaskContractReadyParticipant:
verification participant only
```

Requirements:

- verify exact issued body/current certified prefix under family lock;
- revalidate immediately before READY evaluation/admission;
- preserve exact bound refs;
- reject stale/revoked/wrong project/contract/version/repository/base/action/scope;
- missing legacy ref-only body cannot use this new entrypoint;
- no WorkRun column/backfill;
- no duplicate state machine;
- no new guard type/owner.

Accepted authority locator semantics:

```text
task-contract-admission:v1:<body_sha256>:<snapshot_ref>
```

Possession of the locator is not authority.

# 12. migration

Before creating migration verify:

```text
current Alembic head = 20260901_0008
20260914_0009 absent
single head
```

Otherwise STOP:

```text
MIGRATION_BASELINE_MISMATCH
```

Create exactly:

```text
migrations/versions/20260914_0009_task_contract_durable_bodies.py
revision = 20260914_0009
down_revision = 20260901_0008
```

Implement the Human-accepted `MIGRATION_DESIGN.md`:

- one new `task_contract_bodies` table;
- no existing table alteration;
- no backfill;
- exact identity/ref/hash/predecessor constraints;
- `canonical_body BYTEA`;
- immutable UPDATE/DELETE trigger;
- no-TRUNCATE trigger;
- no pgcrypto extension;
- empty-only downgrade;
- nonempty downgrade fails closed and preserves rows/schema/revision.

Do not broaden the migration.

# 13. isolated PostgreSQL verification

This Task explicitly authorizes an isolated ephemeral PostgreSQL 17.6 proof.

First:

```text
"C:\Program Files\Docker\Docker\resources\bin\docker.exe" image inspect postgres:17.6
```

If the image is not already local:

```text
ISOLATED_POSTGRES_IMAGE_MISSING
```

STOP. Do NOT pull an image and do NOT access external network.

Use a Task-owned container only, e.g.:

```text
aiscc-p2-4-taskcontract-0756-pg
```

Requirements:

- new disposable container;
- synthetic test-only credentials;
- bind only to `127.0.0.1` on a task-chosen free local port;
- never reuse retained/private project PostgreSQL;
- no production/test secrets;
- no external network dependency;
- only this Task's migration/tests may access it.

Required DB proof:

1. empty DB -> migration head PASS;
2. existing predecessor `20260901_0008` -> `20260914_0009` PASS;
3. restart/reload preserves exact body bytes/hash/ref;
4. same-version exact retry idempotent;
5. same-version different-content deny;
6. concurrent issue/version race bounded deterministically;
7. rollback at every write boundary leaves no partial body/ref/event authority;
8. row UPDATE/DELETE/TRUNCATE denied;
9. empty-store downgrade PASS;
10. nonempty-store downgrade FAIL-CLOSED while preserving schema/row/Alembic revision;
11. re-open after process/service reconstruction verifies body independently of in-memory objects.

Cleanup after evidence collection is best-effort housekeeping:

```text
stop/remove exact Task-owned container only
```

Cleanup failure does not invalidate passed proof; report exact residue. No broad Docker prune.

# 14. required test/static evidence

At minimum:

```text
tests/unit/task_authority/test_task_contract_body.py
tests/unit/task_authority/test_task_contract_issuance.py
tests/integration/task_authority/test_task_contract_durability.py
tests/integration/task_authority/test_task_contract_ready.py
```

All must PASS.

Also run the existing narrow owner regressions that are directly affected by changed `task_authority`/READY behavior. Inventory exact existing test paths first and report them; do not run an unrelated full suite solely to fill a report field.

Required negatives include:

- unknown body fields;
- bool/float unsafe integer;
- noncanonical/tampered body;
- forged body/ref/event/snapshot/candidate;
- wrong repository/base/NextAction;
- scope overlap/traversal/absolute/reparse escape;
- missing/ambiguous Human binding;
- wrong/missing evidence binding;
- stale/revoked version;
- conflicting request/content;
- legacy ref-only new READY entry;
- authority locator treated as data, not authority.

Required static:

```text
Ruff: changed Python paths
compile: changed Python paths
git diff --check
UTF-8/control-character/Markdown checks for changed canonical docs
```

No test may claim provider/network/browser/golden-cycle proof.

# 15. forbidden actions

Forbidden:

```text
actual P2-4 self-dogfood golden cycle
real active self-dogfood Task issuance
src/aiscc/self_dogfood/** mutation
stockroom/replay mutation
P2-3 rerun
CURRENT_STATE_SUMMARY / DECISION_REGISTER / NEXT_ACTIONS mutation
P1-6/P1-7 semantic baseline mutation
retained/private PostgreSQL
external network
Docker image pull
provider/LLM call
public deployment
push
automatic merge
```

# 16. Result Commit B

Only after all required source/static/isolated-PostgreSQL evidence passes.

Stage exactly the changed paths from sections 7, 8 and 12.

Commit message exactly:

```text
feat(aiscc): add durable taskcontract authority
```

Require:

```text
Commit B parent = Governance Commit A
changed paths subset = exact authorized mutation allowlist
no unrelated path
index empty after commit
tracked clean after commit
```

If a required test fails, do NOT create Commit B. Preserve working changes and export truthful failure evidence.

# 17. evidence contract

executor_required:

- inbound package/hash/member/input hashes;
- initial repository/state/legacy exact preflight;
- Governance Commit A;
- exact canonical baseline adoption;
- exact migration creation;
- product implementation within allowlist;
- four required targeted test files;
- directly affected narrow owner regressions;
- isolated PostgreSQL 17.6 durability/migration/restart/concurrency/downgrade proof;
- Ruff/compile/diff-check/document formatting;
- exact Result Commit B only on complete pass;
- final repository inventory/export integrity.

reuse_allowed:

- 0319 source/schema audit and Human-accepted proposal bytes only when SHA-exact;
- accepted P1-4/P1-6/P1-7/P1-8 predecessor authority semantics for unchanged owners.

human_owned:

- already provided: durable-body design adoption `ACCEPT`;
- future P2-4 implementation candidate acceptance;
- future actual self-dogfood golden-cycle acceptance;
- release/submission.

not_required:

- browser QA;
- provider/network;
- actual golden self-dogfood run;
- public deployment;
- full unrelated suite.

forbidden:

- actions in section 15.

# 18. mandatory stop

After a named blocker, perform only minimal blocker evidence, workspace inventory, report/export and safe termination.

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

Do not "helpfully" widen scope.

# 19. report/export

Target:

```text
.aiassistant/reports/target/20260914_0756_aiscc-p2-4-taskcontract-durable-body-baseline-adoption-runtime-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ACCEPTED_DESIGN_INPUT_VERIFICATION.md
BASELINE_ADOPTION_REVIEW.md
SOURCE_CHANGE_REVIEW.md
MIGRATION_REVIEW.md
POSTGRES_RUNTIME_EVIDENCE.md
TEST_RESULTS.md
CONTRACT_REVIEW.md
```

Include changed files preserving project-relative paths.

Include current Cycle/Judgment/done Task canonical copies.

Do not include credentials, raw DB dumps or unrelated source.

Result ZIP:

```text
.aiassistant/reports/target/20260914_0756_aiscc-p2-4-taskcontract-durable-body-baseline-adoption-runtime-implementation-1.zip
```

# 20. terminal repository boundary

On successful complete candidate:

```text
HEAD = Result Commit B
index = empty
tracked = clean
Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_0756_aiscc-p2-4-taskcontract-durable-body-baseline-adoption-runtime-implementation-1.md
```

Current Task active -> done byte-identically after execution/report completion.

Legacy 1400 ignored Task must remain byte-exact.

Canonical state files remain exact original hashes from section 3.

On failed/blocked implementation:

- no Result Commit B;
- report exact working-tree changes/residue;
- do not reset unrelated or Task-owned evidence merely to make status clean;
- no broad cleanup.

# 21. success criteria / state ceiling

Success candidate requires ALL:

```text
Human-accepted proposal bytes exact
Governance Commit A exact
canonical baseline adopted without owner drift
TaskConstraintRefV1 unchanged
migration exact and additive
whole body durable/restart-surviving
issuance atomic/idempotent
READY integration uses existing P1-4 authority
P1-6/P1-7 non-substitution preserved
isolated PostgreSQL proof complete
all required tests PASS
Ruff/compile/diff-check PASS
Result Commit B exact
no forbidden action
export exact
```

Success status ceiling:

```text
P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do NOT claim:

```text
P2_4_SELF_DOGFOOD_ENTRY_SOURCE_CANDIDATE
P2-4 ACCEPTED/CLOSED
golden cycle complete
```

Project state remains:

```text
P2-3:
ACCEPTED / CLOSED

P2-4:
IN_PROGRESS

durable TaskContract design:
HUMAN_PROVIDED / ACCEPTED

durable TaskContract runtime:
candidate only if this Task passes

self-dogfood source candidate:
NOT CREATED

golden cycle:
NOT PERFORMED

P3:
NOT_STARTED

Public Bounded Live:
NOT_RELEASED
```
