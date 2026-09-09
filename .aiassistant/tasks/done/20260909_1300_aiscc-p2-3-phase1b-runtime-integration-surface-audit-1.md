# 작업지시서: P2-3 Phase 1B runtime integration-surface audit

## meta

- task_id: `20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1`
- created_at: `2026-09-09T13:00:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `DISCOVERY_AUDIT / DESIGN_AUDIT`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-3 Phase 1B synthetic repository materialization + bounded runtime enrollment`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `472bd11b76dc510562e33d056d9841b6be72c12e`
- required_base_tree: `14195b914b16d5adce7db0c4093907d2af7dcac0`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `governance Git persistence → read-only runtime/provider/security/source integration audit`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1.md

CYCLE:
20260909_1300_aiscc-p2-3-phase1a-terminal-accepted-phase1b-audit-entry-1.cycle.md
SHA-256:
998d726c95165db059b697e4ce04184bead4fe50c4fa4a88c14cd5f376444c36
destination:
.aiassistant/records/aiscc/cycles/20260909_1300_aiscc-p2-3-phase1a-terminal-accepted-phase1b-audit-entry-1.cycle.md

JUDGMENT:
20260909_1300_aiscc-p2-3-phase1a-terminal-state-final-acceptance-judgment-1.md
SHA-256:
595d283e12ee27ed7cff9484c4305ccbb8760b40b34bc25374e9800618a6ed21
destination:
.aiassistant/reports/aiscc/20260909_1300_aiscc-p2-3-phase1a-terminal-state-final-acceptance-judgment-1.md

HANDOFF:
none
```

Human downloads only the ZIP to:

```text
C:\Users\oracl\Downloads
```

Executor:

1. verify exact ZIP filename/SHA-256;
2. validate archive readability/CRC/member safety;
3. materialize TASK first to `.aiassistant/tasks/active/20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1.md`;
4. read TASK;
5. materialize CYCLE/JUDGMENT directly to exact canonical destinations;
6. verify exact hashes.

Before canonical TASK placement, any ZIP/hash/archive/TASK bootstrap failure:

```text
STOP
no report/export
no substantive project mutation
ask Human to re-download/reposition ZIP
```

After exact canonical transport, inbound ZIP/staging cleanup refusal is `NON_BLOCKING_LOCAL_RESIDUE`.

# 1. repository gate

After current artifact placement require:

```text
branch:
main

HEAD:
472bd11b76dc510562e33d056d9841b6be72c12e

HEAD tree:
14195b914b16d5adce7db0c4093907d2af7dcac0

index:
empty
```

Expected Git-visible set:

```text
.aiassistant/records/aiscc/cycles/20260909_1300_aiscc-p2-3-phase1a-terminal-accepted-phase1b-audit-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1300_aiscc-p2-3-phase1a-terminal-state-final-acceptance-judgment-1.md
```

exact 2 paths.

Current active Task is ignored.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/ignore/absorb.

# 2. current authority / must-read

Read fully:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260909_1300_aiscc-p2-3-phase1a-terminal-accepted-phase1b-audit-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1300_aiscc-p2-3-phase1a-terminal-state-final-acceptance-judgment-1.md

.aiassistant/records/aiscc/cycles/20260909_1203_aiscc-p2-3-phase1a-persisted-phase1b-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1203_aiscc-p2-3-phase1a-persistence-final-acceptance-judgment-1.md

config/scenarios/stockroom/v1/catalog.json
config/scenarios/stockroom/v1/resource.json
config/scenarios/stockroom/v1/s1-normal.json
config/scenarios/stockroom/v1/s2-missing-evidence.json
config/scenarios/stockroom/v1/s3-policy-conflict.json
config/scenarios/stockroom/v1/s4-human-owned-claim.json

src/aiscc/scenarios/models.py
src/aiscc/scenarios/catalog.py
```

Read the remaining Phase 1A schemas/fixtures only as needed to resolve exact integration semantics.

# 3. audit scope and non-goals

This Task is read-only.

It must determine exact current source integration boundaries before any Phase 1B mutation.

Do NOT:

```text
create/edit source/config/test files
run scenario/provider/tool execution
materialize a repository workspace
run Docker/container
mutate DB
generate migrations
perform network/provider calls
generate Replay
Git add/commit/push
```

Read-only Git/source inspection is allowed.

Static parsing/import inspection is allowed only if it produces no source/runtime side effect.
Do not use an operation that creates Git-visible cache/build residue.

# 4. accepted Phase 1A inputs

Treat these as accepted fixed inputs:

```text
resource_id:
repository:synthetic-stockroom

resource_ref:
repository:synthetic-stockroom@be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d

source_commit:
05185c57a6265a4002050ce25cdfde3dc87e9779

subroot:
examples/synthetic-stockroom/

file_count:
14

aggregate:
AISCC-SOURCE-MANIFEST-SHA256-V1
be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d

scenario IDs/version:
stockroom-s1-normal / 1.0.0
stockroom-s2-missing-evidence / 1.0.0
stockroom-s3-policy-conflict / 1.0.0
stockroom-s4-human-owned-claim / 1.0.0
```

Do not redesign these identities in Phase 1B.

If current runtime interfaces cannot safely consume them without a policy/contract change, report the exact GAP.

# 5. first runtime target boundary

Phase 1B is preparation for the first actual capture target accepted by Command Center:

```text
RuntimeMode:
OWNER_SELF_DOGFOOD

scenario source:
fixed Synthetic Stockroom only

provider mode:
LOCAL_DETERMINISTIC_PROVIDER

external_llm_executed:
false

Stockroom summary:
actual bounded tool execution in later runtime Task
```

This target is NOT:

```text
PUBLIC_BOUNDED_LIVE
external LLM proof
general coding-agent access
public release
```

Do not widen permission/profile semantics to satisfy a future public mode.

# 6. bounded source inspection inventory

Inspect exact current paths/symbols needed for these owners.

At minimum inspect current interfaces in:

```text
src/aiscc/runtime/
src/aiscc/providers/
src/aiscc/security/
src/aiscc/workflow/
src/aiscc/task_authority/
src/aiscc/evidence/
src/aiscc/scenarios/
src/aiscc/bootstrap.py

config/providers/provider-profiles.v1.toml
config/providers/tool-registry.v1.toml
config/security/permission-profiles.v1.toml
```

Also inspect targeted tests that define current accepted behavior.

Do not recursively dump whole directories into the report.
Use symbol/path-specific reads/searches.

For each relevant symbol report:

```text
path
symbol/type/config key
semantic owner
input/output contract
current caller/composition point
usable as-is / extension required / absent
security implication
```

# 7. synthetic repository materialization audit

Determine the safest current-compatible Phase 1B materialization design.

It must satisfy:

```text
pinned resource identity
source_commit + subroot binding
14-file manifest/hash verification
no mutable latest/current-checkout assumption
no external remote fetch
no path traversal
no primary checkout direct write
per-run isolated destination only
fail closed on missing/wrong Git object or identity
deterministic destination inventory
```

Audit whether current runtime substrate can support one of:

```text
A. local Git-object/archive extraction from pinned commit into run workspace
B. prebuilt immutable snapshot derived from the accepted resource manifest
C. another already-supported pinned-resource mechanism
```

Recommend exactly one for **OWNER_SELF_DOGFOOD first capture**.

Do not actually materialize it.

Freeze proposed:

```text
materializer API
input resource_ref
resolved source identity
destination/workspace owner
verification order
failure classes
cleanup ownership
runtime evidence emitted
```

# 8. scenario enrollment / driver audit

Determine how the static `ScenarioCatalog` becomes a bounded runtime request without allowing arbitrary task input.

Freeze the proposed chain:

```text
scenario_id selection
→ exact catalog/version resolution
→ TaskContract construction
→ RuntimeMode/profile binding
→ resource_ref binding
→ expected evidence/Human/policy contract
→ driver/orchestrator request
```

Audit whether existing TaskContract/workflow types can express the four scenarios without semantic widening.

Explicitly preserve:

```text
S1 expected accepted path
S2 missing-evidence / REWORK_REQUIRED
S3 policy conflict / BLOCKED
S4 Human-required / HUMAN_REQUIRED
```

Negative demonstration success must not convert S2-S4 into ACCEPTED.

# 9. Stockroom bounded tool audit

Determine an exact adapter/enrollment design for the later actual Stockroom summary execution.

Inspect:

```text
examples/synthetic-stockroom/stockroom/inventory.py
examples/synthetic-stockroom/stockroom/cli.py
examples/synthetic-stockroom/stockroom/model.py
examples/synthetic-stockroom/stockroom/data/catalog.json

current provider/tool models/service/registry
```

Freeze:

```text
tool identity
structured action name
bounded argument schema
working/resource root handling
stdout/result schema
error schema
timeout/process contract
network requirement = none
shell/arbitrary command surface = none
source mutation = none
```

The public requester never selects a command/path/tool argument beyond the fixed scenario contract.

Do not execute the tool.

# 10. deterministic provider/profile audit

Audit current provider abstractions/config for the accepted first-capture target:

```text
LOCAL_DETERMINISTIC_PROVIDER
external_llm_executed=false
```

Determine whether this can be represented by:

```text
existing provider kind/profile
new additive server-owned profile
existing test fixture promoted into a bounded owner-only runtime adapter
other current-compatible mechanism
```

Do not mislabel a scripted/deterministic provider as an external LLM.

Freeze:

```text
provider identity/kind
profile ID/version
model field semantics if required
call/retry/time bounds
deterministic response source
execution event disclosure
external_llm_executed field/provenance
```

No actual provider call.

# 11. security permission/profile audit

Using current `AISCC_SECURITY_SANDBOX` and policy/config implementation, determine exact Phase 1B permission binding for `OWNER_SELF_DOGFOOD`.

Must preserve the effective-permission intersection:

```text
TaskContract
∩ RuntimeMode profile
∩ scenario policy
∩ state/action eligibility
∩ current resource capability
∩ finite limits
```

Audit only the minimum capabilities needed for first capture:

```text
read fixed synthetic materialized workspace
write only per-run mutable workspace if needed
execute exact Stockroom bounded tool action
no outbound network for Stockroom
local deterministic provider only
no raw secret
no primary checkout direct write
```

Determine whether existing permission-profile schema is sufficient and what exact additive config/code change would be needed.

Any required relaxation of a hard baseline:

```text
SECURITY_BOUNDARY_CONFLICT
→ audit blocker
```

# 12. bootstrap/composition audit

Determine current composition point(s) for:

```text
ScenarioCatalog
resource materializer
scenario enrollment/driver
provider service/profile
tool registry/adapter
security policy/profile
workflow kernel
evidence admission
```

Audit `src/aiscc/bootstrap.py` and only its direct relevant collaborators.

Freeze:

```text
construction order
dependency ownership
config load order
fail-closed startup behavior
whether composition is owner-only by default
how future public mode remains separate
```

Do not modify bootstrap.

# 13. persistence / migration boundary

Phase 1B does not implement actual run recording/capture.

Determine whether the materialization/enrollment implementation itself requires any DB schema change.

Report exactly:

```text
PHASE1B_DB_MIGRATION:
NOT_REQUIRED / REQUIRED / GAP
```

Preferred result is `NOT_REQUIRED` if existing durable owners can remain untouched until actual-capture Phase.

If a migration is truly required to make enrollment truthful, identify the exact reason but do not design unrelated capture tables into Phase 1B automatically.

# 14. exact implementation layout candidates

Provide maximum 3 candidate Phase 1B implementation layouts and recommend exactly one.

Each candidate must list exact proposed paths for:

```text
resource materializer
scenario enrollment/driver
Stockroom tool adapter
provider/profile config
tool registry config
security profile/policy config
bootstrap composition
tests
```

For every proposed existing-file modification, explain why a new additive file cannot avoid it.

Do not include recording/Replay/public API/migration paths unless section 13 proves they are required for Phase 1B itself.

# 15. mutation allowlist proposal

Produce a concrete candidate allowlist for the successor implementation Task.

For every proposed path classify:

```text
CREATE
MODIFY
NO_CHANGE
```

The list must be bounded and implementation-ready.

Also provide:

```text
forbidden neighboring paths
dependency-manifest changes required? YES/NO
migration required? YES/NO
runtime/environment provisioning required? YES/NO
```

Do not mutate any path now.

# 16. verification contract proposal

Define the exact evidence needed to accept Phase 1B implementation before actual scenario execution.

At minimum propose:

## unit/static

```text
pinned resource_ref resolution
wrong commit/hash/subroot fail closed
path traversal/symlink/duplicate rejection
deterministic materialization inventory
four scenario enrollment exact
no arbitrary input surface
tool argument allowlist exact
network none
deterministic provider disclosure exact
permission intersection/deny cases
bootstrap unknown/missing config fail closed
```

## integration without actual capture

Determine whether a no-provider/no-DB integration composition test can verify:

```text
catalog → enrollment → resource/profile/tool binding
```

without performing actual Stockroom process execution.

If process execution is unavoidable, defer that proof to the later actual-runtime Task rather than silently running it in implementation verification.

# 17. required status matrix

Report exactly:

```text
RESOURCE_MATERIALIZER:
READY / GAP

SCENARIO_RUNTIME_ENROLLMENT:
READY / GAP

STOCKROOM_TOOL_ADAPTER:
READY / GAP

DETERMINISTIC_PROVIDER_PROFILE:
READY / GAP

SECURITY_PROFILE_BINDING:
READY / GAP

BOOTSTRAP_COMPOSITION:
READY / GAP

PHASE1B_DB_MIGRATION:
NOT_REQUIRED / REQUIRED / GAP

PHASE1B_IMPLEMENTATION_ALLOWLIST:
READY / GAP

ACTUAL_CAPTURE_ENTRY_AFTER_PHASE1B:
READY / GAP
```

A normal implementation GAP does not block the audit.

Block only on incompatible canonical authority/security boundary or inability to define a truthful bounded implementation.

# 18. recommended Phase 1B execution split

Recommend whether implementation should be:

```text
one bounded implementation Task
```

or split into at most three cuts such as:

```text
B1 resource materializer
B2 scenario/tool/provider/security enrollment
B3 bootstrap + static/integration verification
```

For each proposed cut state:

```text
work_type
exact mutation authority
fresh IDE boundary
tests/evidence
mandatory stops
```

Recommend exactly one sequence.

Do not start it.

# 19. evidence contract

executor_required:

- `COMMAND_CENTER_ARTIFACT_TRANSPORT`
- `WORKSPACE_STATIC`
- `CANONICAL_AUTHORITY`
- `SOURCE_INTEGRATION_INVENTORY`
- `RESOURCE_MATERIALIZATION_AUDIT`
- `SCENARIO_ENROLLMENT_AUDIT`
- `PROVIDER_TOOL_AUDIT`
- `SECURITY_BOUNDARY_AUDIT`
- `BOOTSTRAP_COMPOSITION_AUDIT`
- `DESIGN_AUDIT`

reuse_allowed:

- persisted Phase 1A static contracts
- accepted P1 runtime/provider/security/evidence owners
- accepted first-capture target from P2-3 design audit

human_owned:

```text
new Human QA:
NOT_REQUIRED

public distribution/license:
HUMAN_PENDING / outside this Task
```

not_required:

```text
runtime scenario execution
provider/tool process execution
DB mutation
Replay
Browser QA
deployment
Git persistence
```

forbidden:

```text
source/config/test mutation
dependency installation
Docker/container execution
external network/provider call
repository materialization
scenario run
DB migration
Replay/public API work
Git add/commit/push
P2-4/P3
```

# 20. mandatory stop

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
MISSING_REQUIRED_ARTIFACT
CANONICAL_AUTHORITY_CONFLICT
SECURITY_BOUNDARY_CONFLICT
PROOF_TYPE_SUBSTITUTION_REQUIRED
```

After repository-level blocker: minimum evidence/report/export only.

Inbound cleanup refusal after canonical transport is non-blocking.

# 21. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
PHASE1B_SOURCE_INTEGRATION_AUDIT.md
RESOURCE_MATERIALIZATION_PROPOSAL.md
RUNTIME_ENROLLMENT_PROPOSAL.md
PHASE1B_MUTATION_ALLOWLIST_PROPOSAL.md
```

After folder completion automatically create:

```text
.aiassistant/reports/target/20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1.zip
```

Require:

```text
one top-level bundle directory
readable archive
CRC/integrity PASS
required root files present
manifest coverage
folder/archive filename and byte equality
```

Keep folder and outbound ZIP.

# 22. Task lifecycle

After audit/report/export completes:

```text
.aiassistant/tasks/active/20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1.md
→
.aiassistant/tasks/done/20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1.md
```

Do not stage or commit.

Final Git-visible set:

```text
.aiassistant/records/aiscc/cycles/20260909_1300_aiscc-p2-3-phase1a-terminal-accepted-phase1b-audit-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1300_aiscc-p2-3-phase1a-terminal-state-final-acceptance-judgment-1.md
.aiassistant/tasks/done/20260909_1300_aiscc-p2-3-phase1b-runtime-integration-surface-audit-1.md
```

exact 3 paths.

# 23. inbound cleanup

After terminal outcome and outbound ZIP validation, attempt exact inbound delivery ZIP cleanup best-effort.

Any refusal:

```text
NON_BLOCKING_LOCAL_RESIDUE
```

No broad Downloads cleanup.

# 24. final ceiling

Success:

```text
P2-3 Phase 1B source/integration-surface audit:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-3 Phase 1B implementation:
NOT_STARTED

P2-3 actual scenario capture:
NOT_STARTED

P2-3 Replay:
NOT_STARTED
```

Do not start runtime implementation or scenario execution.
