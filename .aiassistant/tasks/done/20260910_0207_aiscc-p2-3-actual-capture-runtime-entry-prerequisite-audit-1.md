# 작업지시서: P2-3 actual-capture runtime-entry prerequisite audit

## meta

- task_id: `20260910_0207_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-1`
- created_at: `2026-09-10T02:07:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `DISCOVERY_AUDIT / DESIGN_AUDIT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-3 actual scenario capture runtime entry`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `d8fbcfa9d36a7531819149037240855cafdd088d`
- required_base_tree: `e224f31268057e400918ece352b72a0388d4091d`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `governance Git persistence → current runtime/persistence/security source authority audit`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Phase 1B is closed and persisted.

Actual scenario capture is the next work region, but B3 intentionally proved:

```text
NO_CAPTURE_ALGORITHM_IMPLEMENTED:
PASS
```

Therefore this Task does not execute Stockroom scenarios.

It audits current production source to determine the exact missing runtime/capture crossing and the smallest safe implementation/execution plan.

# 1. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260910_0207_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-1.md

CYCLE:
20260910_0207_aiscc-p2-3-phase1b-closed-actual-capture-runtime-entry-audit-1.cycle.md
SHA-256:
5a68361c98b6165cdd6fa20adf0cc6ca8df99ada519c5c51efc6123f91c0b339
destination:
.aiassistant/records/aiscc/cycles/20260910_0207_aiscc-p2-3-phase1b-closed-actual-capture-runtime-entry-audit-1.cycle.md

JUDGMENT:
20260910_0207_aiscc-p2-3-phase1b-terminal-state-reconciliation-final-acceptance-judgment-1.md
SHA-256:
e6e9266e9f6feedca478b7062d62af47c1b4442d8e719bb4e7ff8f9d59b3e6fa
destination:
.aiassistant/reports/aiscc/20260910_0207_aiscc-p2-3-phase1b-terminal-state-reconciliation-final-acceptance-judgment-1.md

HANDOFF:
none
```

Executor:

1. verify exact ZIP filename/SHA-256;
2. validate archive readability/CRC/member safety;
3. place TASK first at `.aiassistant/tasks/active/20260910_0207_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-1.md`;
4. read TASK;
5. place current Cycle/Judgment at exact canonical destinations;
6. verify exact hashes.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project work
```

After exact canonical transport, inbound cleanup is best-effort/non-blocking.

# 2. repository gate

After current artifact placement require:

```text
branch:
main

HEAD:
d8fbcfa9d36a7531819149037240855cafdd088d

HEAD tree:
e224f31268057e400918ece352b72a0388d4091d

index:
empty
```

Expected Git-visible set excluding current active Task:

```text
.aiassistant/records/aiscc/cycles/20260910_0207_aiscc-p2-3-phase1b-closed-actual-capture-runtime-entry-audit-1.cycle.md
.aiassistant/reports/aiscc/20260910_0207_aiscc-p2-3-phase1b-terminal-state-reconciliation-final-acceptance-judgment-1.md
```

exact 2 paths.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup, restore, stash, reset or absorb.

# 3. exact predecessor/current-state identity

Verify:

- `.aiassistant/tasks/done/20260910_0205_aiscc-p2-3-phase1b-terminal-state-actual-capture-entry-reconciliation-1.md`  `8608832712e93fa462a0cfae1c15e0e4eaf70fe891e378f60ae5d52f14a417ca`
- `.aiassistant/records/aiscc/cycles/20260910_0205_aiscc-p2-3-phase1b-b3-persisted-actual-capture-entry-1.cycle.md`  `4144d85cd1d6f6955466fe780798858d108037a2c67bcfe5022105165c79123b`
- `.aiassistant/reports/aiscc/20260910_0205_aiscc-p2-3-phase1b-b3-persistence-final-acceptance-judgment-1.md`  `1c80ba350cf1440ea2c9b9be25c506b861f337806369c2be5bff00805579ad13`

Also verify current committed state files:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `f57a61c324e6be91546251c864ff9dfc768db387ec9ed769de6ac7a15f24a2ab`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `c4985d610d16a42e2dd67d933ce6667026b82d0a357721fb4205ba622fa9a390`

Any mismatch:

```text
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
→ STOP
```

# 4. mutation and execution authority

Product/config/test mutation:

```text
NONE
```

Runtime side effects:

```text
NONE
```

Forbidden in this audit:

```text
DB connect/query/migration
Docker info/build/pull/run/inspect
Stockroom CLI/module execution
repository materialization
provider call
tool dispatch
security capability/grant issuance
workflow transition request
WorkRun/attempt/operation creation
evidence submission/admission
Human gate/result mutation
Judgment issuance
socket/network/HTTP/OpenAI
environment provisioning
secret resolution
Git add/commit/push
```

Static file reads, bounded symbol searches, AST/import/source inspection and existing config parsing without application side effects are allowed.

Do not import a module if import is known to create runtime side effects; source-parse it instead.

# 5. must-read governance authority

Read fully:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260910_0207_aiscc-p2-3-phase1b-closed-actual-capture-runtime-entry-audit-1.cycle.md
.aiassistant/reports/aiscc/20260910_0207_aiscc-p2-3-phase1b-terminal-state-reconciliation-final-acceptance-judgment-1.md

.aiassistant/tasks/done/20260910_0205_aiscc-p2-3-phase1b-terminal-state-actual-capture-entry-reconciliation-1.md
.aiassistant/records/aiscc/cycles/20260910_0205_aiscc-p2-3-phase1b-b3-persisted-actual-capture-entry-1.cycle.md
.aiassistant/reports/aiscc/20260910_0205_aiscc-p2-3-phase1b-b3-persistence-final-acceptance-judgment-1.md

.aiassistant/reports/aiscc/20260909_1329_aiscc-p2-3-phase1b-runtime-integration-audit-final-acceptance-judgment-1.md
.aiassistant/reports/aiscc/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-judgment-1.md
.aiassistant/reports/aiscc/20260909_1805_aiscc-p2-3-phase1b-b2-final-acceptance-judgment-1.md
.aiassistant/reports/aiscc/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-judgment-1.md
```

No recursively activating old Task must-read lists.

# 6. must-read Phase 1A/B source

Read fully:

```text
src/aiscc/bootstrap.py

src/aiscc/scenarios/models.py
src/aiscc/scenarios/catalog.py
src/aiscc/scenarios/runtime_models.py
src/aiscc/scenarios/enrollment.py
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/composition.py

src/aiscc/runtime/stockroom_workspace.py
src/aiscc/runtime/stockroom_materializer.py
src/aiscc/runtime/docker.py

src/aiscc/providers/ports.py
src/aiscc/providers/tools.py
src/aiscc/providers/service.py
src/aiscc/providers/local_deterministic.py
src/aiscc/providers/stockroom_tool.py

src/aiscc/security/policy.py
src/aiscc/security/stockroom_policy.py

src/aiscc/workflow/kernel.py
src/aiscc/contracts/workflow.py

src/aiscc/evidence/service.py
src/aiscc/human/repository.py
src/aiscc/judgment/authority.py
src/aiscc/persistence/repository.py

config/scenarios/stockroom/v1/catalog.json
config/scenarios/stockroom/v1/resource.json
config/scenarios/stockroom/v1/s1-normal.json
config/scenarios/stockroom/v1/s2-missing-evidence.json
config/scenarios/stockroom/v1/s3-policy-conflict.json
config/scenarios/stockroom/v1/s4-human-owned-claim.json

config/providers/stockroom-owner-profiles.v1.toml
config/providers/stockroom-tools.v1.toml
config/security/stockroom-owner.v1.toml
```

Read direct collaborators of the named classes/functions by bounded symbol resolution only when necessary.

# 7. bounded persistence/schema discovery

Using source search only, identify:

```text
PostgresExecutionRepository constructor/factory
WorkflowKernel constructor/factory
EvidenceAdmissionService constructor/factory
PostgresHumanAuthorityRepository constructor/factory
PostgresJudgmentAuthority constructor/factory
AgentExecutionService constructor/factory
SecurityPolicy / StockroomOwnerRestriction runtime construction
StockroomWorkspace / StockroomMaterializer runtime construction
DockerRuntime constructor/factory
```

Then bounded-search migration/schema owners required by those repositories.

Allowed search roots:

```text
src/aiscc/persistence/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/evidence/**
migrations/**
```

Do not read unrelated application trees.

Report:

```text
exact source path
constructor/factory signature
required connection/config inputs
transaction/connection ownership
whether current schema supports required capture records
whether new migration is required
```

No DB connection.

# 8. capture-algorithm gap audit

Determine exactly what executable orchestration is missing between:

```text
PreparedStockroomDriver
```

and authoritative runtime effects.

At minimum map the required call/ownership sequence for:

```text
TaskContract / WorkRun creation or lookup
attempt creation
READY -> RUNNING transition
resource grant / capability issuance
B1 materialization
provider execution
tool dispatch where allowed
runtime output persistence
execution completion
RUNNING -> ADMISSION_PENDING
evidence candidate/submission/admission
Human gate routing
Judgment issuance/admission
terminal/nonterminal workflow transition
Cycle/next-action relationship, if any
```

For every step report:

```text
authoritative owner
current callable
required input identity/version
durable mutation
idempotency/retry rule
failure/unknown-outcome behavior
whether source already supports it
```

Do not invent a new owner when a current owner exists.

# 9. S1 exact runtime sequence

Define the future actual-capture sequence for:

```text
stockroom-s1-normal
```

Target:

```text
READY
→ RUNNING
→ ADMISSION_PENDING
→ ACCEPTED
```

Required real facts to capture:

```text
resource materialization provenance
local deterministic provider disclosure
Stockroom tool output lineage
summary-runtime evidence admission
authoritative ACCEPTED Judgment
separate admitted transition
terminal WorkRun projection
```

Identify exact source APIs needed.

Do not execute them.

# 10. S2 exact runtime sequence

Define future sequence for:

```text
stockroom-s2-missing-evidence
```

Target:

```text
READY
→ RUNNING
→ ADMISSION_PENDING
→ REWORK_REQUIRED
```

Required semantics:

```text
Stockroom tool may execute
required summary-runtime evidence remains absent by server fixture behavior
no evidence substitution
HOLD_REWORK_REQUIRED Judgment
same-run automatic retry = false
new revision/attempt authority required for any later retry
```

Determine whether current source can represent the intentional evidence suppression cleanly or whether capture-runner implementation is required.

# 11. S3 exact runtime sequence

Define future sequence for:

```text
stockroom-s3-policy-conflict
```

Target:

```text
READY
→ RUNNING or admitted pre-dispatch evaluation boundary
→ BLOCKED
```

Exact accepted semantics:

```text
Stockroom tool:
MUST NOT execute

policy evidence:
STATIC_SOURCE / policy-conflict-static

blocker:
POLICY / POLICY_CONFLICT

authoritative capture Judgment:
none
```

Determine the exact current System owner/API that admits BLOCKED without manufacturing a Judgment.

If current APIs require a different valid predecessor/sequence, report the exact canonical sequence rather than forcing the target sketch.

# 12. S4 exact runtime sequence

Define future sequence for:

```text
stockroom-s4-human-owned-claim
```

Target:

```text
READY
→ RUNNING
→ ADMISSION_PENDING
→ HUMAN_REQUIRED
```

Required:

```text
Stockroom tool runtime evidence:
real

synthetic Agent claim:
not HumanResult
not HUMAN_OWNED evidence

Human gate:
PENDING / ACTIVE or exact current equivalent

actual HumanResult:
ABSENT

workflow:
HUMAN_REQUIRED and nonterminal
```

Identify the exact call that opens/persists the gate and the exact browser/Human input that will be required later.

Do not submit a HumanResult.

# 13. security grant/receipt crossing audit

Map the exact future security sequence for S1/S2/S4:

```text
sealed Stockroom owner context
→ base SecurityPolicy evaluation
→ resource grant
→ capability issuance
→ consumed receipts
→ StockroomSummaryDispatcher
→ DockerRuntime.run_consumed_stockroom
```

For each required domain:

```text
REPOSITORY
FILESYSTEM
PROCESS
TOOL
PROVIDER
SECRET compatibility mediation
```

report:

```text
issuing owner
scope fingerprint inputs
one-use consumption point
receipt handoff
double-consumption prevention
revocation/expiry path
unknown-outcome behavior
```

NETWORK must remain denied.

Determine whether the current public/general execution service can issue all required exact Stockroom scopes or whether an owner-only capture runner must compose them.

# 14. materialization/runtime-root audit

Map the B1 runtime path:

```text
source_commit:
05185c57a6265a4002050ce25cdfde3dc87e9779

resource_ref:
repository:synthetic-stockroom@be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d

subroot:
examples/synthetic-stockroom/

runtime destination:
<operator runtime root>/<run-id>/<attempt-id>/source
```

Report exact runtime-root configuration/constructor expectations.

Verify statically that future capture does not require:

```text
current checkout as source
requester destination path
remote fetch
network
```

Identify cleanup/quarantine responsibilities after each scenario.

# 15. Docker image/runtime prerequisite audit

The B2 tool config pins:

```text
aiscc-stockroom-runtime@sha256:be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
```

Audit current repository source/build assets for this exact image reference.

Bounded search roots:

```text
examples/synthetic-stockroom/**
src/aiscc/runtime/**
config/providers/stockroom-tools.v1.toml
Dockerfile*
docker/**
scripts/** only when directly referenced
```

Report one exact status:

```text
IMAGE_RUNTIME_READY
IMAGE_BUILD_PROVISIONING_REQUIRED
IMAGE_REFERENCE_CONTRACT_MISMATCH
```

Specifically determine whether the `sha256:` component is intended/valid as an OCI image digest or is merely the source resource hash reused as a symbolic pin.

Do not run Docker, inspect local images, pull, build or query a daemon.

If actual daemon/image presence must later be proven, classify it as a separate runtime prerequisite.

# 16. local deterministic provider audit

Confirm statically:

```text
provider_id:
aiscc-local-deterministic

external_llm_executed:
false

network:
none

real external credential:
none
```

Map the actual future call sequence:

```text
initial provider response
tool call for S1/S2/S4
function_call_output correlation
final response
```

and S3 no-tool branch.

Determine how the synthetic compatibility SECRET mediation is satisfied in a real capture without resolving a real credential.

# 17. evidence/Human/Judgment ownership audit

For each scenario create an exact matrix:

```text
required evidence descriptor
candidate producer
admission owner/API
admitted/not admitted target
Human requirement
Judgment owner/API
expected Judgment
workflow target
```

Maintain strict non-substitution:

```text
tool output != admitted evidence
Agent claim != HumanResult
HumanResult != Judgment
Judgment != transition
expected descriptor != admitted artifact
```

# 18. durable capture/export contract

Determine what exact immutable data must be persisted/exported from each real run so a later Recorded Replay can be built without executing provider/tool again.

At minimum consider:

```text
TaskContract identity/version
WorkRun/run/attempt IDs
state/version transition decisions
resource/materialization provenance
configuration/request fingerprints
provider disclosure
private protocol lineage
tool call/output refs
evidence admissions/rejections
Human gate state/result ref if any
Judgment
terminal/nonterminal final projection
timestamps/idempotency identities
failure/unknown-outcome records
```

Classify every field:

```text
PUBLIC_REPLAY_SAFE
PRIVATE_RUNTIME_ONLY
HUMAN_REVIEW_REQUIRED_BEFORE_PUBLICATION
```

Do not create Replay records.

# 19. exact implementation gap matrix

Produce a status matrix with at least:

```text
CAPTURE_ORCHESTRATOR
REAL_OWNER_CONSTRUCTION
WORKRUN_CREATION
TRANSITION_ROUTING
MATERIALIZER_RUNTIME
DOCKER_IMAGE_PROVISIONING
STOCKROOM_TOOL_RUNTIME
LOCAL_PROVIDER_RUNTIME
SECURITY_GRANT_RECEIPT_CHAIN
EVIDENCE_ADMISSION
HUMAN_GATE_ROUTING
JUDGMENT_ROUTING
POSTGRES_SCHEMA
CAPTURE_EXPORT
S1_EXECUTABILITY
S2_EXECUTABILITY
S3_EXECUTABILITY
S4_EXECUTABILITY
```

Allowed statuses:

```text
READY_CURRENT_SOURCE
IMPLEMENTATION_GAP
RUNTIME_PREREQUISITE
HUMAN_PREREQUISITE
NOT_REQUIRED
CONTRACT_CONFLICT
```

Each non-ready row requires exact evidence/path/reason.

# 20. exact next implementation allowlist

Based on current source only, propose the smallest exact candidate allowlist for the next mutation Task.

Separate:

```text
CREATE
MODIFY
NO_CHANGE_NEIGHBORS
```

For every proposed changed path give:

```text
why required
semantic owner
why existing owner cannot already satisfy it
```

No speculative convenience files.

If migration/dependency/config change is required, list it separately and explain.

If no source mutation is actually required and the next step can be pure runtime execution, say:

```text
IMPLEMENTATION_ALLOWLIST:
NONE
```

Do not create files in this audit.

# 21. recommended cut sequence

Choose the smallest safe sequence from the audit.

Preferred decision shape:

```text
A. capture-runner implementation/static tests
B. runtime prerequisite provisioning/verification
C. S1 actual runtime smoke/capture
D. S2/S3/S4 actual capture
E. capture corpus sanitization/export
F. Replay implementation/admission
```

Collapse cuts only if current source evidence proves doing so does not mix authorities or side-effect risk.

For each cut state:

```text
work_type
mutation scope
runtime side effects
evidence required
fresh IDE session boundary
Human gate involvement
success ceiling
```

# 22. runtime environment prerequisites

Without executing them, identify exact future prerequisites for the first real capture:

```text
Python version/interpreter
PostgreSQL requirement
DB schema/migration head
database URL/env/config
Docker daemon requirement
Stockroom image requirement
git executable requirement
operator runtime root
filesystem permissions
secret compatibility sentinel/config
network expectation
```

Do not infer environment availability from old sessions.

Mark each:

```text
SOURCE_CONFIRMED_REQUIREMENT
MUST_VERIFY_AT_RUNTIME
NOT_REQUIRED
```

# 23. no source mutation verification

Before Task lifecycle require:

```text
current Cycle/Judgment:
2 exact Git-visible paths

other Git-visible path:
0

index:
empty
```

Task lifecycle:

```text
.aiassistant/tasks/active/20260910_0207_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-1.md
→
.aiassistant/tasks/done/20260910_0207_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-1.md
```

Final:

```text
3 exact Git-visible paths
index empty
```

No source/config/test change.

No Git add/commit.

# 24. required audit bundle

Bundle folder:

```text
.aiassistant/reports/target/20260910_0207_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
RUNTIME_ENTRY_AUDIT.md
OWNER_WIRING_AUDIT.md
SCENARIO_CAPTURE_SEQUENCE.md
SECURITY_RECEIPT_AUDIT.md
RUNTIME_PREREQUISITE_MATRIX.md
CAPTURE_EXPORT_CONTRACT.md
IMPLEMENTATION_ALLOWLIST.md
CUT_SEQUENCE_RECOMMENDATION.md
```

Include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
```

Do not export broad source trees.

For exact source excerpts needed for Browser review, quote bounded symbol/path/line references in the audit documents rather than copying files unless the export rule requires a narrow source evidence file.

Create adjacent outbound ZIP automatically.

Require:

```text
one top-level bundle directory
readable / CRC PASS
required roots present
manifest coverage
folder/archive byte equality
```

# 25. evidence contract

executor_required:

- inbound ZIP/artifact transport
- exact repository gate
- 0205/state provenance identity
- current-source runtime owner audit
- four-scenario authoritative sequence
- security grant/receipt chain
- materializer/runtime-root audit
- Docker image contract audit
- durable DB/schema audit
- Replay-oriented capture export field classification
- exact implementation allowlist
- bounded cut-sequence recommendation
- runtime prerequisite inventory
- exact no-mutation final workspace
- outbound ZIP

reuse_allowed:

- persisted Phase 1A/B1/B2/B3 design and tests
- 0205 terminal state authority

human_owned:

```text
actual S4 HumanResult:
HUMAN_PENDING / not part of audit

public distribution/license:
HUMAN_PENDING
```

not_required:

```text
runtime execution
DB connection
Docker execution
provider/tool call
scenario capture
Replay generation
browser QA
deployment
```

forbidden proof substitution:

```text
source audit != runtime readiness
constructor existence != instantiated durable owner
Dockerfile/image reference != daemon/image availability
expected S1-S4 outcome != actual captured state
B3 zero-side-effect proof != capture execution proof
```

# 26. mandatory stop

```text
DOWNLOAD_ZIP_MISSING
DOWNLOAD_ZIP_HASH_MISMATCH
DOWNLOAD_ZIP_CORRUPT
DOWNLOAD_TASK_MEMBER_MISSING
DOWNLOAD_TASK_PLACEMENT_FAILED
TRANSPORT_FAILURE
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
MISSING_REQUIRED_ARTIFACT
CANONICAL_AUTHORITY_CONFLICT
AUDIT_REQUIRES_RUNTIME_EXECUTION
AUDIT_REQUIRES_SOURCE_MUTATION
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

If the answer to an audit question requires actual runtime observation, mark `MUST_VERIFY_AT_RUNTIME`; do not cross the execution boundary.

# 27. final ceiling

Success:

```text
P2-3 actual scenario capture:
ENTRY_AUDIT_COMPLETE / BROWSER_JUDGMENT_REQUIRED

actual scenario execution:
NOT_STARTED

source mutation:
NONE

runtime side effects:
NONE

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Do not declare actual capture complete or Phase P2-3 closed.
