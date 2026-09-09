# 작업지시서: P2-3 Canonical Scenario Pack and Recorded Replay source/contract audit retry 2

## meta

- task_id: `20260908_2330_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-2`
- created_at: `2026-09-08T23:30:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `DISCOVERY_AUDIT / DESIGN_AUDIT / REWORK`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-3 canonical scenario pack and Recorded Replay corpus contract`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `4cadcb45b44d5bb2a260d7fa9350626ce28ea875`
- required_base_tree: `7d98df6f74eba74427d1be3b0abe9a78ef91a29f`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `canonical governance persistence → read-only P2-3 scenario/replay source and design authority`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260908_2330_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-2.md

CYCLE:
20260908_2330_aiscc-p2-3-decision-register-reconciliation-accepted-source-audit-retry-entry-1.cycle.md
SHA-256:
016afc405faa85dd0725445ceb8c559130f1d4c58b3fdaf05827d806dc567f61
destination:
.aiassistant/records/aiscc/cycles/20260908_2330_aiscc-p2-3-decision-register-reconciliation-accepted-source-audit-retry-entry-1.cycle.md

JUDGMENT:
20260908_2330_aiscc-p2-3-decision-register-reconciliation-final-acceptance-judgment-1.md
SHA-256:
e93888c32e371d95961286ebe626344a3251c121aadb780c27888bff510872d0
destination:
.aiassistant/reports/aiscc/20260908_2330_aiscc-p2-3-decision-register-reconciliation-final-acceptance-judgment-1.md

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
3. materialize TASK first to `.aiassistant/tasks/active/20260908_2330_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-2.md`;
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

After canonical artifact transport succeeds, inbound ZIP/staging cleanup refusal is `NON_BLOCKING_LOCAL_RESIDUE`.

# 1. repository gate

After current artifact placement require:

```text
branch:
main

HEAD:
4cadcb45b44d5bb2a260d7fa9350626ce28ea875

HEAD tree:
7d98df6f74eba74427d1be3b0abe9a78ef91a29f

index:
empty
```

Expected Git-visible set:

```text
.aiassistant/records/aiscc/cycles/20260908_2330_aiscc-p2-3-decision-register-reconciliation-accepted-source-audit-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_2330_aiscc-p2-3-decision-register-reconciliation-final-acceptance-judgment-1.md
```

exact 2 paths.

Current active Task is ignored.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

No cleanup/restore/ignore/absorb.

# 2. current canonical authority to read

Read fully:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md
.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md

.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260908_2330_aiscc-p2-3-decision-register-reconciliation-accepted-source-audit-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_2330_aiscc-p2-3-decision-register-reconciliation-final-acceptance-judgment-1.md

examples/synthetic-stockroom/README.md
examples/synthetic-stockroom/PROVENANCE.md
```

Additional source reads are allowed only for bounded capability inspection.

Do not bulk-read unrelated historical Tasks/Cycles/reports.

Do not reuse stopped 1700/2200 GAP tables or incomplete proposals as accepted evidence.

# 3. current authority invariants

Preserve:

```text
P2-2:
authors/persists fixed synthetic candidate asset

P2-3:
owns scenario-time canonical repository/version admission
scenario definitions/contracts
actual AISCC executions
recording
Replay projection/corpus/admission
```

Also preserve:

```text
candidate source exists
!=
scenario repository admitted

scenario definition exists
!=
actual AISCC run

recorded files exist
!=
Replay admitted

Replay
!=
Live

Agent/Executor claim
!=
admitted evidence

Human-owned evidence
!=
Executor-completed
```

# 4. audit objective

Freeze a browser-reviewable exact P2-3 contract for:

1. canonical Synthetic Stockroom scenario resource identity/version;
2. exact four-scenario v1 pack;
3. per-scenario Task/evidence/Human ownership;
4. current runtime/security capability and gaps;
5. actual AISCC run capture contract;
6. authoritative run data vs sanitized Replay projection;
7. Replay schema/metadata/integrity/no-inference;
8. sanitization/IP/license/secret admission;
9. exact implementation roots/files;
10. bounded P2-3 execution phases and blockers.

No source mutation or scenario execution in this Task.

# 5. Synthetic Stockroom scenario resource identity

Current persisted candidate:

```text
repository commit:
05185c57a6265a4002050ce25cdfde3dc87e9779

subroot:
examples/synthetic-stockroom/
```

Determine from current source/security/runtime whether the canonical scenario identity should be:

```text
A.
repository commit + exact subroot + exact source identity

B.
derived immutable snapshot identity/version

C.
another already-supported fixed resource identity
```

Do not guess.

Freeze:

```text
resource ID format
source commit/snapshot
subroot if applicable
exact or aggregate identity
immutability expectation
materialization/copy boundary
scenario version binding
```

If implementation is required before truthful fixed-resource representation is possible, classify exact GAP.

# 6. bounded current-source capability inventory

Inspect only source needed to answer:

```text
RuntimeMode / PUBLIC_BOUNDED_LIVE
scenario/profile/resource identity/versioning
fixed repository/resource admission
repository materialization/copy
TaskContract evidence ownership
WorkflowState transitions
WorkRun durable events
Evidence candidate/admission
HumanGate/HumanResult
Judgment
CycleRecord
NextAction
recorded-run read model
Replay projection/schema/storage
```

Targeted searches may use:

```text
RuntimeMode
PUBLIC_BOUNDED_LIVE
scenario_id
scenario_version
profile
resource
repository
TaskContract
WorkflowState
WorkRun
Evidence
HumanGate
HumanResult
Judgment
CycleRecord
NextAction
event
replay
```

For each capability report:

```text
path/symbol
current semantic owner
usable as-is / extension required / absent
supporting evidence
```

No whole-repository dump.

# 7. exact four-scenario v1 proposal

Define exactly:

```text
S1 normal
S2 missing-evidence
S3 policy-conflict
S4 human-owned-claim
```

For each define:

```text
scenario_id
scenario_version
purpose
canonical repository/resource version
TaskContract goal
non-goals
allowed actions
forbidden actions
bounded user parameters, if any
expected WorkflowState path
expected stop/terminal condition
executor_required evidence
reuse_allowed evidence
human_owned evidence
not_required evidence
forbidden evidence
expected Judgment owner/status
expected Cycle/NextAction outcome
recording requirements
public-safe disclosure
```

Unsupported behavior must be marked GAP.

# 8. public input/action boundary

Do not introduce:

```text
free-form task input
repository URL/upload
arbitrary shell/command
arbitrary network
user-selected provider/model
path input
plugin/config injection
owner/private workspace access
```

If any public parameter is proposed, freeze exact enum/range schema.

# 9. actual AISCC run recording contract

Define an actual AISCC execution eligible for later Recorded Replay admission.

At minimum:

```text
task_id / task_version
scenario_id / scenario_version
runtime mode
synthetic repository identity/version
orchestrator version/commit
work_run_id
attempt/run lineage
original timestamps
state/version transition events
execution/provider/tool events
evidence candidate/admission refs
HumanGate/HumanResult refs
Judgment refs/status/owner
Cycle/NextAction refs
failure/blocker/rework reasons
resource/accounting metadata where applicable
```

Separate:

```text
authoritative durable workflow/run source
vs
sanitized Replay projection
```

Replay projection must not become workflow truth.

# 10. Recorded Replay proposal

Preserve:

```text
Recorded Run Replay label
scenario_id / scenario_version
synthetic repository version/commit/snapshot
original run timestamp
orchestrator version/commit
recorded/live type
state/event timeline
evidence provenance
Judgment provenance
Cycle/NextAction provenance
sanitization/admission version
integrity hash/version
```

Replay read behavior:

```text
read-only
0 provider/LLM calls
0 source mutation
0 process/tool/network execution
no hidden Live fallback
truthful missing/corrupt error
```

# 11. sanitization / IP / license / secret gate

Current truth remains:

```text
Synthetic Stockroom:
project-authored / synthetic-only

third-party runtime dependencies:
0

public distribution/license review:
PENDING
```

Do not promote PENDING to cleared.

Propose exact pre-public-admission gate:

```text
private/company/customer source exclusion
PII/secret scan
license/IP review
sanitized projection admission
source/run/version provenance
```

Human/public-license authority remains separate.

# 12. no-inference / replay-integrity proof contract

Propose later executable proof requirements:

```text
Replay page/read provider/LLM calls:
0

Replay source mutation:
0

Replay process/tool/network execution:
0

stored corpus bytes/hash/version:
stable

missing/corrupt artifact:
truthful error

Live/provider/budget failure:
does not alter stored Replay

Replay metadata:
matches admitted source-run refs
```

Do not claim these were executed now.

# 13. implementation layout candidates

Provide maximum 3 candidates and recommend exactly one.

For each include:

```text
scenario manifest/catalog root
resource-ref/fixture root
authoritative run data/reference boundary
sanitized Replay corpus root
schema/version files
tests
migration/config needs
runtime integration points
public API/read-model integration points
```

Must preserve:

```text
canonical scenario definition
!=
authoritative actual run data
!=
sanitized public Replay projection
```

# 14. bounded P2-3 execution sequence

Propose post-audit phases.

For each phase:

```text
work_type
exact mutation authority
fresh IDE session boundary
Human-owned gate
required evidence
mandatory stop conditions
```

At minimum evaluate separate phases for:

```text
scenario/replay contract implementation
scenario-pack static/unit verification
actual AISCC scenario execution/capture
sanitization/IP/license/secret admission
Replay projection/integrity/no-inference verification
Human/public-browser verification if applicable
final Git persistence / P2-3 closure
```

Do not start any phase in this Task.

# 15. required status matrix

Report exactly:

```text
SCENARIO_RESOURCE_IDENTITY:
READY / GAP

SCENARIO_CONTRACT_MODEL:
READY / GAP

ACTUAL_RUN_CAPTURE:
READY / GAP

REPLAY_PROJECTION_MODEL:
READY / GAP

SANITIZATION_ADMISSION:
READY / GAP

IP_LICENSE_PUBLIC_ADMISSION:
READY / HUMAN_PENDING / GAP

NO_INFERENCE_VERIFICATION:
READY / GAP
```

A GAP is an implementation prerequisite, not automatically an audit blocker.

Stop only for incompatible canonical authority or unresolved security boundary requiring policy change.

# 16. evidence contract

executor_required:

- `COMMAND_CENTER_ARTIFACT_TRANSPORT`
- `WORKSPACE_STATIC`
- `STATIC_SOURCE / CANONICAL_AUTHORITY`
- `SOURCE_INVENTORY`
- `SCENARIO_CONTRACT_AUDIT`
- `REPLAY_CONTRACT_AUDIT`
- `SECURITY_BOUNDARY_AUDIT`
- `DESIGN_AUDIT`

reuse_allowed:

- P2-2 Synthetic Stockroom persisted identity
- accepted architecture/orchestration/security/public-runtime baselines
- persisted artifact-delivery V2 authority

human_owned:

```text
new Human QA:
NOT_REQUIRED

public distribution/license clearance:
HUMAN_PENDING / separate authority

final P2-3 design acceptance:
Browser Command Center
```

not_required:

- scenario execution
- unit/runtime execution
- provider calls
- Browser QA
- deployment
- Replay generation
- Git persistence

forbidden:

- source/config/test mutation
- Synthetic Stockroom mutation
- external repository/network
- provider execution
- scenario run
- Replay generation
- public release
- Git add/commit/push
- P2-4/P3 work

# 17. mandatory stop

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
SECURITY_BOUNDARY_UNCERTAIN
PROOF_TYPE_SUBSTITUTION_REQUIRED
```

After repository-level blocker: minimum evidence/report/export only.

Inbound cleanup refusal after canonical transport is `NON_BLOCKING_LOCAL_RESIDUE`.

# 18. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260908_2330_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-2/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
P2_3_SOURCE_CAPABILITY_AUDIT.md
SCENARIO_PACK_V1_PROPOSAL.md
RECORDED_REPLAY_V1_PROPOSAL.md
```

Then automatically create:

```text
.aiassistant/reports/target/20260908_2330_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-2.zip
```

Require:

```text
one top-level bundle directory
readable archive
CRC/integrity PASS
required root files present
folder/archive filename and byte equality
```

Keep both folder and ZIP.

# 19. Task lifecycle

After audit/report/export completes:

```text
.aiassistant/tasks/active/20260908_2330_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-2.md
→
.aiassistant/tasks/done/20260908_2330_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-2.md
```

Do not stage or commit.

Final Git-visible set:

```text
.aiassistant/records/aiscc/cycles/20260908_2330_aiscc-p2-3-decision-register-reconciliation-accepted-source-audit-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_2330_aiscc-p2-3-decision-register-reconciliation-final-acceptance-judgment-1.md
.aiassistant/tasks/done/20260908_2330_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-2.md
```

exact 3 paths.

# 20. inbound cleanup

After terminal outcome and outbound ZIP validation, attempt exact inbound delivery ZIP cleanup best-effort.

Any refusal:

```text
NON_BLOCKING_LOCAL_RESIDUE
```

No broad Downloads cleanup.

# 21. final ceiling

Success:

```text
P2-3 source/contract audit:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-3 implementation:
NOT_STARTED

P2-4:
NOT_STARTED
```

Do not start scenario implementation or actual run generation.
