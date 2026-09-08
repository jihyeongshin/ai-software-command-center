# 작업지시서: P2-3 Canonical Scenario Pack and Recorded Replay source/contract audit

## meta

- task_id: `20260908_1700_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-1`
- created_at: `2026-09-08T17:00:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `DISCOVERY_AUDIT / DESIGN_AUDIT`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-3 canonical scenario pack and Recorded Replay corpus contract`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `05185c57a6265a4002050ce25cdfde3dc87e9779`
- required_base_tree: `df997ec70594d0d451c7d281c975c6cbdb63e453`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `P2-2 final persistence → P2-3 scenario/replay authority and design context`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# current state

```text
P2-2:
ACCEPTED / CLOSED / PERSISTED

P2-2 commit:
05185c57a6265a4002050ce25cdfde3dc87e9779

P2-3:
ENTRY_READY

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED

PUBLIC_RECORDED_REPLAY:
NOT_ADMITTED
```

This Task begins P2-3 only as a **read-only source/contract audit**.

It does not create scenario files, execute AISCC scenarios, record runs, or admit Replay.

# Human-owned IDE session prerequisite

This Task must be executed in a Human-created fresh IDE Executor chat.

A model/reasoning change inside an existing conversation is not a fresh IDE chat.

Executor must not create/open the chat itself.

# goal

1. Verify exact current P2-3 canonical authority and repository capabilities.
2. Freeze the ownership boundary between scenario-pack definition, actual run capture, Replay admission, and later public release.
3. Determine the exact canonical Synthetic Stockroom repository/snapshot identity that P2-3 should pin.
4. Define an exact four-scenario v1 semantic pack proposal:
   - normal
   - missing-evidence
   - policy-conflict
   - human-owned-claim
5. Map each scenario to existing TaskContract, state-machine, evidence, HumanGate/Judgment, Cycle and NextAction capabilities.
6. Define the scenario manifest/versioning/input/action/expected-stop/evidence contract.
7. Define the actual-run recording boundary and durable event/evidence capture requirements.
8. Define Replay projection/corpus schema, sanitization/IP/license/secret admission and truthful-label contract.
9. Define no-inference and Replay integrity verification requirements.
10. Propose exact implementation roots/files and a bounded P2-3 execution sequence.
11. Identify exact blockers/gaps before scenario implementation or actual run generation.
12. Do not mutate source or start scenario execution.

# non-goals

- scenario source creation
- modification of Synthetic Stockroom candidate
- runtime execution
- provider call
- public Live enablement
- Replay corpus generation
- Browser QA
- deployment
- Git mutation
- Project Source sync
- P2-4 Self-Dogfooding Cutover
- P3 work

# must-read canonical source

After transport and workspace gates PASS, read:

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

.aiassistant/records/aiscc/cycles/20260908_1700_aiscc-p2-2-terminal-closure-p2-3-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1700_aiscc-p2-2-terminal-closure-judgment-1.md

examples/synthetic-stockroom/README.md
examples/synthetic-stockroom/PROVENANCE.md
```

Additional source reads are allowed only when needed for the bounded capability inventory below.

Do not bulk-read unrelated historical Tasks/Cycles/reports.

# transport / repository gate

Current Command Center package contains only:

```text
TASK:
20260908_1700_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-1.md

CYCLE:
20260908_1700_aiscc-p2-2-terminal-closure-p2-3-entry-1.cycle.md

JUDGMENT:
20260908_1700_aiscc-p2-2-terminal-closure-judgment-1.md

HANDOFF:
none
```

Transport must PASS before Task execution.

After transport require:

```text
branch:
main

HEAD:
05185c57a6265a4002050ce25cdfde3dc87e9779

HEAD tree:
df997ec70594d0d451c7d281c975c6cbdb63e453

index:
empty
```

Expected Git-visible dirt is exact two paths:

```text
.aiassistant/records/aiscc/cycles/20260908_1700_aiscc-p2-2-terminal-closure-p2-3-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1700_aiscc-p2-2-terminal-closure-judgment-1.md
```

Current active Task is ignored.

Any extra or missing path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/ignore/absorb.

# P2-3 inherited authority

The audit must preserve these accepted boundaries.

## scenario and replay owner

```text
P2-3 MUST own:
- project-owned synthetic repository/version at scenario time
- allowlisted scenario definitions
- per-scenario Task/evidence/human ownership contract
- actual AISCC execution and recorded event/evidence capture
- sanitization, IP/license review, secret scan
- Recorded Run Replay metadata and truthful UI contract
- normal / missing-evidence / policy-conflict / human-owned-claim scenarios
- replay integrity and no-inference verification candidate
```

## prohibited semantic shortcuts

```text
candidate source exists
!=
scenario repository admitted

scenario definition exists
!=
actual AISCC run

recorded event files exist
!=
Replay admitted

Replay
!=
Live

Agent/Executor claim
!=
admitted evidence/judgment

Human-owned evidence
!=
Executor-completed
```

# canonical Synthetic Stockroom identity audit

Current persisted source lives at:

```text
repository commit:
05185c57a6265a4002050ce25cdfde3dc87e9779

subroot:
examples/synthetic-stockroom/
```

The audit must decide whether P2-3 canonical scenario resource identity should be represented as:

```text
A.
AISCC repository commit + exact subroot + exact 14-file hash set

B.
an extracted/versioned immutable snapshot identity derived from that subroot

C.
another already-supported exact repository resource identity
```

Do not assume A automatically.

Evaluate against current security/runtime repository identity and per-run isolated-copy contracts.

The result must freeze:

```text
repository resource ID format
source commit/snapshot
subroot if applicable
aggregate or exact file identity
immutability expectation
copy/materialization boundary
scenario version binding
```

If current runtime cannot represent a truthful fixed synthetic resource without source changes, report the exact gap.

# bounded current-source capability inventory

Read only relevant paths needed to answer:

```text
1. Where are RuntimeMode/public permission profiles represented?
2. How is scenario/profile/resource identity represented and versioned?
3. What current code can admit fixed repository resources?
4. What TaskContract fields can encode scenario evidence ownership?
5. What current code persists WorkRun events, evidence, HumanGate, Judgment, Cycle and NextAction refs?
6. What current API/read model can expose recorded run details without mutation?
7. Is there already a Replay projection/schema/root?
8. What missing implementation is required before actual P2-3 run capture?
```

Permitted bounded searches include exact identifiers such as:

```text
RuntimeMode
PUBLIC_BOUNDED_LIVE
scenario_id
scenario_version
profile
resource
repository
TaskContract
WorkRun
Evidence
HumanGate
Judgment
CycleRecord
NextAction
event
replay
```

No whole-repository dump.

# scenario pack v1 proposal

Define exactly four semantic scenarios.

## S1 — normal

Purpose:

```text
show a bounded task whose required evidence is available and whose governance path can reach accepted outcome truthfully
```

## S2 — missing-evidence

Purpose:

```text
show that executor completion/claim cannot substitute for missing required proof and that the run stops/routes truthfully
```

## S3 — policy-conflict

Purpose:

```text
show a tool/action/resource request outside current allowed authority and fail-closed policy handling without silently widening permissions
```

## S4 — human-owned-claim

Purpose:

```text
show that an Agent/Executor cannot complete a Human-owned verification or approval and that the Human gate remains authoritative
```

For each scenario proposal provide:

```text
scenario_id
scenario_version
purpose
canonical repository/resource version
initial TaskContract goal/non-goal
allowed actions
forbidden actions
bounded user-selectable parameters, if any
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

Do not fabricate current implementation support. Mark unsupported steps as gaps.

# scenario input/action boundary

Public scenario contract must remain finite and server-defined.

The proposal must not introduce:

```text
free-form task input
repository URL/upload
arbitrary command
arbitrary shell
arbitrary network
user-selected provider/model
path input
plugin/config injection
owner/private workspace access
```

If user-selectable parameters exist, freeze their exact enum/range schema.

# actual AISCC run recording contract

Define what qualifies as an **actual AISCC execution** for Recorded Replay admission.

At minimum address:

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
HumanGate/HumanResult refs where applicable
Judgment refs/status/owner
Cycle/NextAction refs
failure/blocker/rework reasons
resource/accounting metadata when applicable
```

Distinguish:

```text
authoritative durable source
vs
sanitized Replay projection
```

Replay projection must not become the source of workflow truth.

# Recorded Replay projection/corpus contract

Propose exact metadata/content requirements for each recorded scenario.

Must preserve:

```text
Recorded Run Replay label
scenario ID/version
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

Replay must be:

```text
read-only
zero-inference on page/replay request
no mutation
no process/tool/network/provider execution
no hidden Live fallback
truthful on missing/corrupt artifact
```

# sanitization / IP / license / secret admission

The audit must explicitly classify:

```text
Synthetic Stockroom provenance:
project-authored / synthetic-only

third-party runtime dependencies:
0

public distribution/license review:
PENDING
```

Do not silently convert `PENDING` into cleared.

Define the gate required before public Replay/Live admission, including:

```text
private/company/customer source exclusion
PII/secret scan
license/IP review
sanitized public projection admission
source/run/version provenance
```

The current Task may propose the gate but may not grant license clearance.

# no-inference / replay-integrity proof contract

Propose executable evidence requirements for later implementation:

```text
Replay page/read path triggers 0 provider/LLM calls
Replay read path performs 0 source mutation
Replay read path performs 0 process/tool/network execution
stored corpus bytes/hash/version are stable
missing/corrupt Replay produces truthful error
Live/provider/budget failure does not alter stored Replay
Replay metadata matches admitted source run refs
```

Do not claim these proofs were executed in this audit.

# implementation root/layout proposal

Provide maximum three candidate layouts and recommend exactly one.

For each candidate include:

```text
scenario manifest/catalog root
scenario fixture/resource-ref root
recorded raw/admitted source reference boundary
sanitized Replay corpus root
schema/version files
tests
migration/config needs
runtime integration points
public API/read-model integration points
```

The recommendation must preserve separation between:

```text
canonical scenario definition
actual authoritative run data
sanitized public Replay projection
```

# phased P2-3 execution proposal

Propose a bounded sequence after this audit, for example:

```text
A. scenario/replay contract implementation
B. deterministic scenario-pack static/unit verification
C. actual AISCC scenario execution + capture
D. sanitization/IP/license/secret admission
E. Replay projection/integrity/no-inference verification
F. Human/public-browser verification if required
G. final Git persistence / P2-3 closure
```

This example is not mandatory if current source supports a safer decomposition.

For each proposed phase indicate:

```text
work_type
mutation authority
fresh IDE session boundary
Human-owned gate, if any
required evidence
stop conditions
```

# blocker classification

Report exact status for:

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

A GAP is not automatically a blocker for the audit. It is an implementation prerequisite.

Stop only if canonical authorities are incompatible or the security boundary cannot be resolved without policy change.

# evidence contract

## executor_required

- `COMMAND_CENTER_ARTIFACT_TRANSPORT`
- `WORKSPACE_STATIC`
- `STATIC_SOURCE / CANONICAL_AUTHORITY`
- `SOURCE_INVENTORY`
- `SCENARIO_CONTRACT_AUDIT`
- `REPLAY_CONTRACT_AUDIT`
- `SECURITY_BOUNDARY_AUDIT`
- `DESIGN_AUDIT`

## reuse_allowed

- P2-2 Synthetic Stockroom accepted/persisted identity
- accepted P1 architecture/orchestration/security contracts
- accepted public runtime baseline

Applicability must be shown; do not restate stale status as current execution evidence.

## human_owned

```text
new Human QA:
NOT_REQUIRED

public distribution/license clearance:
HUMAN_PENDING / separate authority

final P2-3 design acceptance:
Browser Command Center
```

## not_required

- scenario execution
- tests/runtime
- provider calls
- Browser QA
- deployment
- Replay generation
- Git persistence

## forbidden

- source/config/test mutation
- Synthetic Stockroom mutation
- external repository/network
- provider execution
- scenario run
- Replay generation
- public release
- Git add/commit/push
- P2-4/P3 work

# mandatory stop

```text
TRANSPORT_FAILURE
TRANSPORT_TOOL_POLICY_BLOCKED
HEAD_OR_TREE_MISMATCH
INDEX_NOT_EMPTY
DIRTY_WORKSPACE_MIXED
MISSING_REQUIRED_ARTIFACT
CANONICAL_AUTHORITY_CONFLICT
SECURITY_BOUNDARY_UNCERTAIN
PROOF_TYPE_SUBSTITUTION_REQUIRED
```

After a named blocker, perform only minimum evidence/report/export.

# export bundle

Target:

```text
.aiassistant/reports/target/20260908_1700_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-1/
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

No changed product/runtime/config files should exist.

# Task lifecycle

After audit/report/export completes:

```text
.aiassistant/tasks/active/20260908_1700_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-1.md
→
.aiassistant/tasks/done/20260908_1700_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-1.md
```

Do not stage or commit.

Final expected Git-visible set after lifecycle:

```text
.aiassistant/records/aiscc/cycles/20260908_1700_aiscc-p2-2-terminal-closure-p2-3-entry-1.cycle.md
.aiassistant/reports/aiscc/20260908_1700_aiscc-p2-2-terminal-closure-judgment-1.md
.aiassistant/tasks/done/20260908_1700_aiscc-p2-3-canonical-scenario-pack-recorded-replay-source-contract-audit-1.md
```

exact 3 paths.

# final response ceiling

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
