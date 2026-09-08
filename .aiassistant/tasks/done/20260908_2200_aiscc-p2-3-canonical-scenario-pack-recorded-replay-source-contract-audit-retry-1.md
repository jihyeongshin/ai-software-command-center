# 작업지시서: P2-3 Canonical Scenario Pack and Recorded Replay source/contract audit retry

## meta

- task_id: `20260908_2200_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-1`
- created_at: `2026-09-08T22:00:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `DISCOVERY_AUDIT / DESIGN_AUDIT / REWORK`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-3 canonical scenario pack and Recorded Replay corpus contract`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `89ebcffacd9b8e74d3c598ddf6e3274a69a9bc1c`
- required_base_tree: `8c02a4f06c297ed6815fce140b8c5e1bc96e977d`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `governance persistence recovery → read-only P2-3 scenario/replay source and design authority`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260908_2200_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-1.md

CYCLE:
20260908_2200_aiscc-p2-3-entry-reconciliation-accepted-source-audit-retry-entry-1.cycle.md
SHA-256:
467cf8974c5fbc9ebb1d1becda9c8723afc0bbc0bcd0e394a4dbcfc709146116
destination:
.aiassistant/records/aiscc/cycles/20260908_2200_aiscc-p2-3-entry-reconciliation-accepted-source-audit-retry-entry-1.cycle.md

JUDGMENT:
20260908_2200_aiscc-p2-3-entry-reconciliation-final-acceptance-judgment-1.md
SHA-256:
6b205568bb4fdf3a5bdf5383749e699f0ef0ffaceeb47dfe358156b1b847aeb3
destination:
.aiassistant/reports/aiscc/20260908_2200_aiscc-p2-3-entry-reconciliation-final-acceptance-judgment-1.md

HANDOFF:
none
```

Human downloads only the delivery ZIP into `C:\Users\oracl\Downloads`.

Executor:

1. verify exact ZIP filename/SHA-256;
2. verify archive readability/CRC/member safety;
3. materialize TASK first to `.aiassistant/tasks/active/20260908_2200_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-1.md`;
4. read TASK;
5. materialize CYCLE/JUDGMENT directly to exact canonical destinations;
6. verify hashes.

If bootstrap fails before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
ask Human to re-download/reposition ZIP
```

After exact canonical transport, inbound ZIP/staging cleanup is best-effort only and is not a substantive gate.

# 1. current state

```text
P2-1:
ACCEPTED / CLOSED / PERSISTED

P2-2:
ACCEPTED / CLOSED / PERSISTED

P2-3:
NOT_STARTED / ENTRY_READY / NEXT_EXECUTABLE

1700 P2-3 source/contract audit:
BLOCKED / RETRY_REQUIRED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED

PUBLIC_RECORDED_REPLAY:
NOT_ADMITTED
```

This Task retries only the read-only P2-3 source/contract audit.

Do not create scenario source, run AISCC scenarios, generate Replay data, or mutate Git.

# 2. repository gate after current artifact placement

Require:

```text
branch:
main

HEAD:
89ebcffacd9b8e74d3c598ddf6e3274a69a9bc1c

HEAD tree:
8c02a4f06c297ed6815fce140b8c5e1bc96e977d

index:
empty
```

Expected Git-visible set:

```text
.aiassistant/records/aiscc/cycles/20260908_2200_aiscc-p2-3-entry-reconciliation-accepted-source-audit-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_2200_aiscc-p2-3-entry-reconciliation-final-acceptance-judgment-1.md
```

exact 2 paths.

Current active Task is ignored.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/ignore/absorb.

# 3. must-read canonical authority

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

.aiassistant/records/aiscc/cycles/20260908_2200_aiscc-p2-3-entry-reconciliation-accepted-source-audit-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_2200_aiscc-p2-3-entry-reconciliation-final-acceptance-judgment-1.md

examples/synthetic-stockroom/README.md
examples/synthetic-stockroom/PROVENANCE.md
```

Additional source reads are allowed only for the bounded capability inventory below.

Do not bulk-read unrelated historical Tasks/Cycles/reports.

Do not reuse 1700 placeholder GAP tables or incomplete proposals as accepted evidence.

# 4. audit goal

Independently freeze the P2-3 design contract for:

1. canonical scenario pack ownership/versioning;
2. exact Synthetic Stockroom scenario-time repository identity;
3. exact four-scenario v1 semantic pack;
4. per-scenario Task/evidence/Human ownership;
5. actual AISCC run capture;
6. authoritative durable run data vs sanitized Replay projection;
7. Replay schema/metadata/integrity/no-inference contract;
8. sanitization/IP/license/secret admission;
9. exact implementation roots/files;
10. bounded P2-3 execution sequence and blockers.

# 5. inherited semantic boundaries

Preserve:

```text
P2-2:
authors/persists the fixed synthetic candidate asset

P2-3:
owns scenario-time canonical repository/version admission,
scenario definitions/contracts,
actual AISCC executions,
recording,
Replay corpus/admission
```

Do not silently equate:

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

# 6. current Synthetic Stockroom identity

Persisted source:

```text
repository commit:
05185c57a6265a4002050ce25cdfde3dc87e9779

subroot:
examples/synthetic-stockroom/
```

Determine from current source/security/runtime whether P2-3 canonical scenario resource identity should be:

```text
A.
repository commit + exact subroot + exact 14-file identity

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
exact/aggregate identity
immutability expectation
materialization/copy boundary
scenario-version binding
```

If current runtime cannot truthfully represent the required fixed synthetic resource without implementation work, classify the exact GAP.

# 7. bounded source capability inventory

Audit only source needed to answer:

```text
RuntimeMode / PUBLIC_BOUNDED_LIVE
scenario/profile/resource identity/versioning
fixed repository/resource admission
repository materialization/copy
TaskContract evidence ownership
WorkflowState/state transition support
WorkRun events
Evidence candidate/admission
HumanGate/HumanResult
Judgment
CycleRecord
NextAction
recorded-run read model
Replay projection/schema/storage
```

Permitted targeted searches include:

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

No whole-repository dump.

For each capability report:

```text
implemented path/symbol
current semantic owner
usable as-is / extension required / absent
evidence
```

# 8. exact scenario pack v1 proposal

Define exactly four semantic scenarios.

## S1 — normal

Demonstrates a bounded task where required evidence is available and governance can reach an accepted outcome truthfully.

## S2 — missing-evidence

Demonstrates that Executor completion/claim cannot substitute for missing required proof and the workflow stops/routes truthfully.

## S3 — policy-conflict

Demonstrates fail-closed handling when an action/resource lies outside current authority, without silent permission widening.

## S4 — human-owned-claim

Demonstrates that Agent/Executor cannot complete Human-owned verification/approval and Human gate remains authoritative.

For each scenario define:

```text
scenario_id
scenario_version
purpose
canonical repository/resource version
TaskContract goal
non-goals
allowed actions
forbidden actions
bounded user-selectable parameters
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

Unsupported current behavior must be marked GAP, not fabricated.

# 9. public input/action boundary

The public scenario contract must be finite and server-defined.

Do not introduce:

```text
free-form task input
repository URL/upload
arbitrary command/shell
arbitrary network
user-selected provider/model
path input
plugin/config injection
owner/private workspace access
```

If user-selectable parameters exist, freeze exact enum/range schema.

# 10. actual AISCC run recording contract

Define what qualifies as an actual AISCC execution eligible for later Recorded Replay admission.

Address:

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

Replay projection must never become the source of workflow truth.

# 11. Recorded Replay proposal

For each admitted recorded scenario preserve at minimum:

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

Replay behavior must remain:

```text
read-only
0 LLM/provider calls on page/replay request
0 source mutation
0 process/tool/network execution
no hidden Live fallback
truthful missing/corrupt error
```

# 12. sanitization / IP / license / secret gate

Preserve current truth:

```text
Synthetic Stockroom provenance:
project-authored / synthetic-only

third-party runtime dependencies:
0

public distribution/license review:
PENDING
```

Do not promote `PENDING` to cleared.

Propose the exact gate before public Replay/Live admission, including:

```text
private/company/customer source exclusion
PII/secret scan
license/IP review
sanitized projection admission
source/run/version provenance
```

Human/public-license authority remains separate.

# 13. no-inference / integrity proof contract

Propose later executable evidence proving:

```text
Replay request provider/LLM calls:
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
matches admitted source run refs
```

Do not claim these proofs were executed in this audit.

# 14. implementation layout candidates

Provide maximum three candidate layouts and recommend exactly one.

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

The recommendation must preserve:

```text
canonical scenario definition
!=
authoritative actual run data
!=
sanitized public Replay projection
```

# 15. phased P2-3 execution proposal

Propose a bounded post-audit sequence.

For each phase state:

```text
work_type
exact mutation authority
fresh IDE session boundary
Human-owned gate
required evidence
mandatory stop conditions
```

At minimum consider whether separate phases are required for:

```text
scenario/replay contract implementation
deterministic scenario-pack static/unit verification
actual AISCC scenario execution/capture
sanitization/IP/license/secret admission
Replay projection/integrity/no-inference verification
Human/public-browser verification if applicable
final Git persistence / P2-3 closure
```

Do not start any of them in this Task.

# 16. required status matrix

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

Stop the audit only if canonical authority is internally incompatible or a security boundary cannot be resolved without policy change.

# 17. evidence contract

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

- scenario runtime execution
- tests/runtime execution
- provider calls
- Browser QA
- deployment
- Replay generation
- Git persistence

forbidden:

- source/config/test mutation
- Synthetic Stockroom mutation
- scenario run
- Replay generation
- external repository/network
- provider execution
- public release
- Git add/commit/push
- P2-4/P3 work

# 18. mandatory stop

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

# 19. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260908_2200_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-1/
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

After folder completion automatically create:

```text
.aiassistant/reports/target/20260908_2200_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-1.zip
```

Require:

```text
one top-level bundle directory
readable ZIP
CRC/integrity PASS
required root files present
folder/archive filename and byte equality
```

Keep both folder and outbound ZIP.

# 20. Task lifecycle

After audit/report/export completes:

```text
.aiassistant/tasks/active/20260908_2200_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-1.md
→
.aiassistant/tasks/done/20260908_2200_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-1.md
```

Do not stage or commit.

Final Git-visible set:

```text
.aiassistant/records/aiscc/cycles/20260908_2200_aiscc-p2-3-entry-reconciliation-accepted-source-audit-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_2200_aiscc-p2-3-entry-reconciliation-final-acceptance-judgment-1.md
.aiassistant/tasks/done/20260908_2200_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-retry-1.md
```

exact 3 paths.

# 21. inbound cleanup

After terminal outcome and outbound ZIP validation, attempt exact inbound delivery ZIP cleanup best-effort.

Any refusal:

```text
NON_BLOCKING_LOCAL_RESIDUE
```

Do not use broad Downloads cleanup.

# 22. final ceiling

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
