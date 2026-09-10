# 작업지시서: P2-3 actual-capture runtime-entry prerequisite audit retry

## meta

- task_id: `20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1`
- created_at: `2026-09-10T10:08:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `DISCOVERY_AUDIT / DESIGN_AUDIT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-3 actual scenario capture runtime entry`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf`
- required_base_tree: `992a15a33e8b34cc3da35f44bd846ceddccb2526`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `Git persistence → current runtime/persistence/security source audit`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. fresh-session Windows Python bootstrap

This Task begins in a fresh IDE Executor chat.

Do NOT assume the following are valid through PATH:

```text
python
python3
py
```

Do NOT execute bare `python` as a probe.

Known current interpreter candidate:

```text
C:\Users\oracl\AppData\Roaming\uv\python\cpython-3.12.14-windows-x86_64-none\python.exe
```

If Python is needed for ZIP/hash/source-static verification:

1. verify this exact executable path first;
2. if valid, use it by exact path;
3. if unavailable, discover an actually executable Python interpreter;
4. invoke only the exact discovered executable path.

The known path being absent is not itself a STOP condition.

If no required Python interpreter can be found after discovery:

```text
PYTHON_INTERPRETER_REQUIRED_BUT_NOT_FOUND
→ STOP
```

Repository-owned tests are not authorized in this audit.

# 1. purpose

The original 0207 actual-capture entry audit stopped on a canonical process-settlement conflict.

That conflict is now fixed and persisted at:

```text
HEAD:
04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf

commit:
fix(runtime): quarantine unsettled Stockroom process
```

Restart the audit from current source.

Do not merely resume from the old stopping line.

Partial 0207 findings may be used only as historical hints; every final conclusion must be independently validated against current committed source.

# 2. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md

CYCLE:
20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md
SHA-256:
3cc310ccfe052307a906fe2524db6176f7af0d38ba53616096df6ece0ff581a0
destination:
.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md

JUDGMENT:
20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md
SHA-256:
6cb059aa4206ac5e1f00789e8adbc955f574bf84c71b2e551c4f23a414e51ff0
destination:
.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md

HANDOFF:
none
```

Executor:

1. verify exact ZIP filename/SHA-256;
2. validate archive readability/CRC/member safety;
3. place TASK first at `.aiassistant/tasks/active/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md`;
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

# 3. repository gate

After current artifact placement require:

```text
branch:
main

HEAD:
04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf

HEAD tree:
992a15a33e8b34cc3da35f44bd846ceddccb2526

index:
empty
```

Expected Git-visible set excluding current active Task:

```text
.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md
.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md
```

exact 2 paths.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup, restore, stash, reset or absorb.

# 4. exact predecessor/runtime identity

Verify current 0943 provenance:

- `.aiassistant/tasks/done/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-git-persistence-1.md`  `97a8660cafef0b4e188a519d3991c9a3cabde2254ac26db24c8ba988044f3b60`
- `.aiassistant/records/aiscc/cycles/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-accepted-persistence-entry-1.cycle.md`  `a8f03c599f71b4f945f54e2e9a263192053b16ae9eb74d198b884ae3de88af25`
- `.aiassistant/reports/aiscc/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-judgment-1.md`  `c20a28836d6c7cb898ccc4d5bf6fc76e0acfa9fe9dfc5eb2e6b2f4624e2b722b`

Verify committed runtime fix:

- `src/aiscc/runtime/docker.py`  `f338225c13195d69c41f69f00a47fc1d00c616c94458ef361e32b97f7fde96fa`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`  `ebfb54d92dc446d2afe6bbe51ce261dbdabff92fa4650833f1d576fde6a755c6`

Any mismatch:

```text
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
→ STOP
```

# 5. mutation / execution authority

Product/config/test mutation:

```text
NONE
```

Git staging/commit:

```text
NONE
```

Runtime side effects:

```text
NONE
```

Forbidden:

```text
DB connect/query/migration
Docker info/version/build/pull/run/inspect
Stockroom CLI/process
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
secret resolution
environment provisioning
Git add/commit/push/fetch/pull
```

Static source/config reads, bounded symbol search, AST parsing and side-effect-free config parsing are allowed.

# 6. governance reads must precede source audit

Read fully, in this order, before broad source inspection:

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

.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md
.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md

.aiassistant/tasks/done/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-git-persistence-1.md
.aiassistant/records/aiscc/cycles/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-accepted-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-judgment-1.md

.aiassistant/reports/aiscc/20260910_0205_aiscc-p2-3-phase1b-b3-persistence-final-acceptance-judgment-1.md
.aiassistant/reports/aiscc/20260910_0207_aiscc-p2-3-phase1b-terminal-state-reconciliation-final-acceptance-judgment-1.md
.aiassistant/reports/aiscc/20260910_0918_aiscc-p2-3-runtime-settlement-canonical-conflict-judgment-1.md
.aiassistant/reports/aiscc/20260910_0935_aiscc-p2-3-stockroom-docker-settlement-static-failure-judgment-1.md
```

Do not recursively activate historical Task must-read lists.

If a required canonical path is absent:

```text
MISSING_REQUIRED_ARTIFACT
→ STOP
```

# 7. core current-source reads

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

Use bounded direct-symbol discovery for collaborators only as necessary.

Do not bulk-read unrelated trees.

# 8. canonical-conflict rule during audit

If current source conflicts with an accepted canonical governance/security/runtime rule:

1. identify the exact rule and exact source path/symbol;
2. determine whether the conflict blocks safe actual-capture entry;
3. record bounded evidence;
4. STOP immediately with:

```text
CANONICAL_AUTHORITY_CONFLICT
```

Do not continue a broad audit past a safety-critical canonical conflict.

Non-blocking implementation gaps are not conflicts; continue the audit and classify them as `IMPLEMENTATION_GAP`.

# 9. durable owner construction audit

Using source search only, identify exact construction/factory contracts for:

```text
PostgresExecutionRepository
WorkflowKernel
EvidenceAdmissionService
PostgresHumanAuthorityRepository
PostgresJudgmentAuthority
AgentExecutionService
SecurityPolicy
StockroomOwnerRestriction
StockroomWorkspace
StockroomMaterializer
DockerRuntime
LocalDeterministicProvider
StockroomSummaryDispatcher
PreparedStockroomDriver / B3 owner composition
```

For each report:

```text
source path
class/function
constructor/factory signature
required dependencies/config
durable/in-memory ownership
transaction/connection owner
production-ready under current source: yes/no
missing dependency/wiring
```

Do not instantiate them against live resources.

# 10. bounded DB/schema audit

Search only:

```text
src/aiscc/persistence/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/evidence/**
migrations/**
```

Determine exact schema support needed for actual capture:

```text
TaskContract/WorkRun
attempts
operations
private protocol items
execution bounds/output refs
evidence submissions/admissions
Human gates/results/producer refs
Judgments
transition/version state
capture/export provenance if already present
```

Report:

```text
existing migration/table owner
required schema version/migration head
current source support
new migration required: YES/NO
```

No DB connection.

If runtime availability cannot be known statically:

```text
MUST_VERIFY_AT_RUNTIME
```

# 11. capture orchestrator gap

Map the missing executable crossing between the inert B3 preparation object and authoritative runtime owners.

At minimum determine current-source support for:

```text
TaskContract / WorkRun creation or lookup
attempt creation
READY -> RUNNING transition
security grant/capability issuance
B1 materialization
provider call
Stockroom tool dispatch
Docker consumed-process crossing
private protocol persistence
execution result settlement
RUNNING -> ADMISSION_PENDING
evidence submission/admission
Human gate routing
Judgment issuance/admission
terminal/nonterminal transition
capture/export record production
```

For each step report:

```text
authoritative owner
exact callable
required identifiers/versions
durable mutation
idempotency key / retry rule
unknown/failure behavior
READY_CURRENT_SOURCE or IMPLEMENTATION_GAP
```

Do not invent a new owner when current source already owns the responsibility.

# 12. S1 authoritative future sequence

Scenario:

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

Map exact future current-source calls needed to produce:

```text
materialization provenance
local deterministic provider disclosure
real Stockroom tool output lineage
summary-runtime evidence admission
authoritative ACCEPTED Judgment
separate admitted transition
terminal WorkRun projection
capture/export provenance
```

If current source requires a different valid intermediate state, report the actual canonical sequence.

Do not execute it.

# 13. S2 authoritative future sequence

Scenario:

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
tool may execute
summary-runtime evidence intentionally absent
no evidence substitution
REWORK_REQUIRED nonterminal result
same-run automatic retry=false
later retry requires new revision/attempt authority
```

Determine exactly where intentional evidence absence is implemented or must be implemented.

# 14. S3 authoritative future sequence

Scenario:

```text
stockroom-s3-policy-conflict
```

Accepted semantics:

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

Determine exact current owner/API for a BLOCKED outcome without fabricating a Judgment.

Map the exact canonical transition sequence from READY.

If the actual current kernel requires a different predecessor state, report it.

# 15. S4 authoritative future sequence

Scenario:

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
real Stockroom runtime evidence
synthetic Agent claim is not HumanResult
synthetic Agent claim is not HUMAN_OWNED evidence
Human gate persisted ACTIVE/PENDING or exact current equivalent
actual HumanResult ABSENT
workflow nonterminal
```

Identify:

```text
exact gate-opening owner/call
gate authority identity
what Human input is later required
what state resumes after Human input
```

Do not create/submit a HumanResult.

# 16. security grant/receipt chain

Map exact future sequence for S1/S2/S4:

```text
sealed Stockroom owner context
→ base SecurityPolicy
→ StockroomOwnerRestriction
→ resource/capability issuance
→ consumed receipts
→ dispatcher
→ DockerRuntime.run_consumed_stockroom
```

For each domain:

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
run/attempt/state/version binding
one-use consumption point
receipt handoff
double-consumption prevention
revocation/expiry path
unknown-outcome behavior
```

NETWORK remains denied.

Confirm that the now-persisted Docker settlement invariant closes process-ownership uncertainty at the consumed-process boundary.

Determine whether an owner-only capture runner is required to compose the exact grants.

# 17. materialization/runtime-root audit

Verify current source for:

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

Report:

```text
runtime-root constructor/config requirement
source provenance verification
requester path influence: yes/no
network fetch required: yes/no
current checkout used as source: yes/no
cleanup/quarantine owner
retry/new-attempt behavior
```

No materialization.

# 18. Docker image contract audit

B2 tool config pins:

```text
aiscc-stockroom-runtime@sha256:be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d
```

Search only:

```text
examples/synthetic-stockroom/**
src/aiscc/runtime/**
config/providers/stockroom-tools.v1.toml
Dockerfile*
docker/**
scripts/** only when directly referenced
```

Choose exactly one source-level status:

```text
IMAGE_RUNTIME_READY_BY_SOURCE_CONTRACT
IMAGE_BUILD_PROVISIONING_REQUIRED
IMAGE_REFERENCE_CONTRACT_MISMATCH
```

Determine whether the `sha256:` suffix is:

```text
actual OCI image digest contract
or
source-resource symbolic pin
```

Do not run Docker or inspect local daemon/images.

Runtime daemon/image presence must be separately labeled:

```text
MUST_VERIFY_AT_RUNTIME
```

# 19. local deterministic provider audit

Confirm statically:

```text
provider_id:
aiscc-local-deterministic

execution_backend_kind:
LOCAL_DETERMINISTIC_PROVIDER

external_llm_executed:
false

network:
none

real external credential:
none
```

Map:

```text
initial provider response
function/tool call request
function_call_output correlation
final provider response
```

for S1/S2/S4 and no-tool S3.

Determine exactly how synthetic compatibility SECRET mediation is satisfied without resolving a real credential.

# 20. evidence/Human/Judgment matrix

For S1-S4 produce a matrix with:

```text
scenario_id
required evidence descriptor
runtime producer
admission owner/API
expected admitted/rejected/absent status
Human requirement
Human gate/result owner
Judgment owner/API
expected Judgment or none
workflow target
```

Maintain:

```text
tool output != admitted evidence
Agent claim != HumanResult
HumanResult != Judgment
Judgment != workflow transition
expected descriptor != admitted artifact
```

# 21. capture/export contract for future Replay

Determine exact immutable data that a real capture must durably persist/export so Recorded Replay can later run without provider/tool execution.

At minimum classify:

```text
TaskContract identity/version
WorkRun ID
attempt ID
operation IDs
state/version transitions
resource/source/materialization provenance
config/request fingerprints
provider disclosure
private protocol lineage
tool call/output refs
receipt/capability provenance safe for export
evidence submissions/admissions/rejections
Human gate state/result ref if present
Judgment
final projection
timestamps/idempotency identities
failure/unknown/quarantine records
```

Each field must be classified:

```text
PUBLIC_REPLAY_SAFE
PRIVATE_RUNTIME_ONLY
HUMAN_REVIEW_REQUIRED_BEFORE_PUBLICATION
```

No Replay record generation.

# 22. implementation gap matrix

Produce at least these rows:

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
PROCESS_SETTLEMENT
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

Each non-ready status requires exact source/path/reason.

If any `CONTRACT_CONFLICT` is safety-critical, Task should already have stopped under section 8.

# 23. exact next mutation allowlist

Based only on current source, propose the smallest exact next implementation set.

Separate:

```text
CREATE
MODIFY
NO_CHANGE_NEIGHBORS
MIGRATION_IF_REQUIRED
CONFIG_IF_REQUIRED
```

For every proposed mutation:

```text
exact path
semantic owner
why required
why an existing owner cannot satisfy it
```

No convenience files.

If source mutation is unnecessary:

```text
IMPLEMENTATION_ALLOWLIST:
NONE
```

Do not mutate anything in this audit.

# 24. recommended bounded cut sequence

Choose the smallest safe path to first real capture.

Evaluate this default decomposition:

```text
A. capture-runner/orchestrator implementation + static/unit tests
B. runtime prerequisite provisioning/verification
C. S1 actual runtime smoke/capture
D. S2/S3/S4 actual capture
E. capture corpus sanitization/export
F. Replay implementation/admission
```

For each cut report:

```text
work_type
exact mutation scope
runtime side effects
evidence required
fresh IDE session boundary
Human involvement
success ceiling
```

Collapse cuts only when current evidence demonstrates no authority/risk mixing.

# 25. runtime prerequisite inventory

Without executing anything, enumerate exact future prerequisites:

```text
Python interpreter/version
PostgreSQL runtime
DB URL/config
required migration/schema head
Docker daemon
pinned Stockroom image
git executable
operator runtime root
filesystem permissions
secret compatibility sentinel/config
network expectation
```

Classify each:

```text
SOURCE_CONFIRMED_REQUIREMENT
MUST_VERIFY_AT_RUNTIME
NOT_REQUIRED
```

For Python, do not confuse the IDE audit interpreter with future AISCC runtime interpreter requirements.

# 26. final no-mutation verification

Before Task lifecycle require:

```text
current Cycle/Judgment:
2 exact Git-visible paths

other Git-visible paths:
0

index:
empty
```

Then move:

```text
.aiassistant/tasks/active/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md
→
.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md
```

Final:

```text
3 exact Git-visible paths
index empty
```

No Git add/commit.

# 27. required audit bundle

Bundle folder:

```text
.aiassistant/reports/target/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1/
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

Do not copy broad source trees.

Use bounded path/symbol/line references in audit documents.

Create adjacent outbound ZIP automatically.

Use Windows extended-length path handling from the outset if needed for export packaging.

Require:

```text
one top-level bundle directory
readable / CRC PASS
required roots present
manifest coverage
folder/archive byte equality
```

# 28. evidence contract

executor_required:

- fresh-session Python discovery discipline
- inbound transport
- exact repository gate
- 0943/runtime-fix identity
- governance-first read ordering
- complete current-source runtime owner audit
- complete S1-S4 authoritative sequence
- security grant/receipt chain
- materializer/runtime-root audit
- Docker image contract audit
- DB/schema audit
- capture export classification
- exact implementation allowlist
- bounded cut recommendation
- runtime prerequisite inventory
- exact no-mutation workspace
- outbound ZIP

reuse_allowed:

- persisted Phase 1A/B1/B2/B3 evidence
- persisted 0943 settlement fix
- 0207 partial findings only as non-authoritative hints

human_owned:

```text
S4 HumanResult:
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
Replay
deployment
```

forbidden proof substitution:

```text
source audit != runtime readiness
constructor existence != instantiated durable owner
Docker source assets != daemon/image availability
expected S1-S4 sequence != actual capture
unit settlement proof != real process settlement proof
```

# 29. mandatory stop

```text
DOWNLOAD_ZIP_MISSING
DOWNLOAD_ZIP_HASH_MISMATCH
DOWNLOAD_ZIP_CORRUPT
DOWNLOAD_TASK_MEMBER_MISSING
DOWNLOAD_TASK_PLACEMENT_FAILED
PYTHON_INTERPRETER_REQUIRED_BUT_NOT_FOUND
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

If an audit answer requires runtime observation, record `MUST_VERIFY_AT_RUNTIME`; do not cross the side-effect boundary.

# 30. final ceiling

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

Do not declare actual capture complete or P2-3 closed.
