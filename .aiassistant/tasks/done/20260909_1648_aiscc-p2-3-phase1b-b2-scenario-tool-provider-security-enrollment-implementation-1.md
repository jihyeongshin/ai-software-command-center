# 작업지시서: P2-3 Phase 1B-B2 scenario/tool/provider/security enrollment implementation

## meta

- task_id: `20260909_1648_aiscc-p2-3-phase1b-b2-scenario-tool-provider-security-enrollment-implementation-1`
- created_at: `2026-09-09T16:48:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `ORCHESTRATION_IMPLEMENTATION / SECURITY_SANDBOX_IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-3 Phase 1B-B2 scenario/tool/provider/security enrollment`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `0f5f19c8f8109e192275d1123f90ae50120be203`
- required_base_tree: `750ea4882f5d8688d1be20ea953b710a21c1052c`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `governance Git persistence → shared provider/tool/security/config/source mutation`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. inbound ZIP bootstrap

The Browser Short Prompt's exact delivery ZIP SHA-256 is the bootstrap integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260909_1648_aiscc-p2-3-phase1b-b2-scenario-tool-provider-security-enrollment-implementation-1.md

CYCLE:
20260909_1648_aiscc-p2-3-b1-state-reconciliation-accepted-b2-entry-1.cycle.md
SHA-256:
286e75593b24bf215f5c47e1339f41c5a5e3e32bdddd2cd6745cb5279db5472c
destination:
.aiassistant/records/aiscc/cycles/20260909_1648_aiscc-p2-3-b1-state-reconciliation-accepted-b2-entry-1.cycle.md

JUDGMENT:
20260909_1648_aiscc-p2-3-b1-state-reconciliation-final-acceptance-judgment-1.md
SHA-256:
643d3dbf8f8639966d78386bc632bd5645480fd7109f71f34bd179cb1807ecd6
destination:
.aiassistant/reports/aiscc/20260909_1648_aiscc-p2-3-b1-state-reconciliation-final-acceptance-judgment-1.md

HANDOFF:
none
```

Executor:

1. verify exact ZIP filename/SHA-256;
2. validate archive readability/CRC/member safety;
3. materialize TASK first to `.aiassistant/tasks/active/20260909_1648_aiscc-p2-3-phase1b-b2-scenario-tool-provider-security-enrollment-implementation-1.md`;
4. read TASK;
5. materialize CYCLE/JUDGMENT directly to exact canonical destinations;
6. verify exact hashes.

Bootstrap failure before canonical TASK placement:

```text
STOP
no report/export
no substantive project mutation
ask Human to re-download/reposition ZIP
```

After exact canonical transport, inbound cleanup refusal is `NON_BLOCKING_LOCAL_RESIDUE`.

# 1. repository gate

After current artifact placement require:

```text
branch:
main

HEAD:
0f5f19c8f8109e192275d1123f90ae50120be203

HEAD tree:
750ea4882f5d8688d1be20ea953b710a21c1052c

index:
empty
```

Expected Git-visible set excluding current active Task:

```text
.aiassistant/records/aiscc/cycles/20260909_1648_aiscc-p2-3-b1-state-reconciliation-accepted-b2-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1648_aiscc-p2-3-b1-state-reconciliation-final-acceptance-judgment-1.md
```

exact 2 paths.

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

No cleanup/restore/stash/reset/absorb.

# 2. must-read authority

Read fully:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/rules/AISCC_SECURITY_SANDBOX.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260909_1648_aiscc-p2-3-b1-state-reconciliation-accepted-b2-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1648_aiscc-p2-3-b1-state-reconciliation-final-acceptance-judgment-1.md

.aiassistant/records/aiscc/cycles/20260909_1329_aiscc-p2-3-phase1b-audit-accepted-b1-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1329_aiscc-p2-3-phase1b-runtime-integration-audit-final-acceptance-judgment-1.md

.aiassistant/records/aiscc/cycles/20260909_1435_aiscc-p2-3-phase1b-b1-accepted-persistence-entry-1.cycle.md
.aiassistant/reports/aiscc/20260909_1435_aiscc-p2-3-phase1b-b1-final-acceptance-judgment-1.md

src/aiscc/scenarios/runtime_models.py
src/aiscc/runtime/stockroom_workspace.py
src/aiscc/runtime/stockroom_materializer.py

config/scenarios/stockroom/v1/catalog.json
config/scenarios/stockroom/v1/resource.json
config/scenarios/stockroom/v1/s1-normal.json
config/scenarios/stockroom/v1/s2-missing-evidence.json
config/scenarios/stockroom/v1/s3-policy-conflict.json
config/scenarios/stockroom/v1/s4-human-owned-claim.json

src/aiscc/providers/ports.py
src/aiscc/providers/tools.py
src/aiscc/providers/service.py
src/aiscc/providers/models.py
src/aiscc/providers/profiles.py
src/aiscc/providers/authority.py

src/aiscc/runtime/docker.py

src/aiscc/security/models.py
src/aiscc/security/policy.py

config/providers/provider-profiles.v1.toml
config/providers/tool-registry.v1.toml
config/security/permission-profiles.v1.toml
config/security/resource-policy.v1.toml
config/security/limits.v1.toml
```

Read exact direct collaborators/tests only as needed for current signatures.

Do not bulk-read unrelated history.

# 3. fixed B2 boundary

The first-capture target remains:

```text
RuntimeMode:
OWNER_SELF_DOGFOOD

scenario source:
four accepted Stockroom v1 scenarios only

provider:
aiscc-local-deterministic

execution_backend_kind:
LOCAL_DETERMINISTIC_PROVIDER

external_llm_executed:
false

network:
none for local deterministic provider and Stockroom tool

PUBLIC_BOUNDED_LIVE:
NOT_AUTHORIZED / NOT_RELEASED
```

Do not add a public mode, arbitrary requester surface, external model/provider or real credential dependency.

# 4. exact mutation allowlist — 16 paths

## CREATE — 11

- `src/aiscc/scenarios/enrollment.py`
- `src/aiscc/providers/stockroom_tool.py`
- `src/aiscc/providers/local_deterministic.py`
- `src/aiscc/security/stockroom_policy.py`
- `config/providers/stockroom-owner-profiles.v1.toml`
- `config/providers/stockroom-tools.v1.toml`
- `config/security/stockroom-owner.v1.toml`
- `tests/unit/scenarios/test_runtime_enrollment.py`
- `tests/unit/providers/test_stockroom_tool.py`
- `tests/unit/providers/test_local_deterministic.py`
- `tests/unit/security/test_stockroom_policy.py`

## MODIFY — 5

- `src/aiscc/providers/ports.py`
- `src/aiscc/providers/tools.py`
- `src/aiscc/providers/service.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/security/policy.py`

Rules:

```text
all CREATE paths:
must be absent before mutation

all MODIFY paths:
must be tracked and clean at base HEAD

additional product/config/test path:
forbidden
```

If any exact CREATE path already exists or another mutation becomes necessary:

```text
UNEXPECTED_EXISTING_PATH / SCOPE_EXPANSION_REQUIRED
→ STOP
```

Do not modify B1 files, Phase 1A static scenario definitions, bootstrap.py or B3 files.

# 5. immutable enrollment compiler

Create:

```text
src/aiscc/scenarios/enrollment.py
```

Implement a pure/inert compile boundary equivalent to:

```text
compile_stockroom_selection(
    selection,
    *,
    catalog,
    owner_context
) -> StockroomEnrollment
```

Requester selection surface remains exactly:

```json
{"scenario_id":"<one exact allowed id>"}
```

No requester-supplied:

```text
task text
scenario version
resource
provider
model
command
path
tool/action
runtime mode
security profile
run/attempt authority
```

`owner_context` is private server composition only.

Compilation performs:

```text
0 DB
0 provider
0 tool/process
0 network
0 materialization
```

It must return a frozen immutable B2 enrollment envelope using the accepted `runtime_models.py` types or precise additive types inside this file.

Do not redefine Phase 1A TaskContract JSON meaning.

# 6. exact four scenario enrollment semantics

Preserve exact scenario IDs/version/resource binding.

## S1 `stockroom-s1-normal`

```text
tool:
stockroom_summary required

summary-runtime:
EXECUTOR_REQUIRED / TOOL_RUNTIME

expected terminal contract:
ACCEPTED only after later real evidence admission and deterministic Judgment

Human:
not required
```

## S2 `stockroom-s2-missing-evidence`

```text
tool:
may execute later

server fixture:
suppresses required summary-runtime evidence candidate
not the requirement and not the tool result

ACCEPTED request:
must later be denied with unchanged version

next semantic outcome:
HOLD_REWORK_REQUIRED Judgment
→ fresh bounded REWORK_REQUIRED request

automatic same-run retry:
forbidden
```

## S3 `stockroom-s3-policy-conflict`

```text
Stockroom summary tool:
forbidden

policy evidence:
STATIC_SOURCE / policy-conflict-static

blocker:
POLICY / POLICY_CONFLICT

expected:
RUNNING -> BLOCKED

authoritative capture Judgment:
none
```

## S4 `stockroom-s4-human-owned-claim`

```text
tool:
stockroom_summary required later

synthetic Agent claim:
not Human input
not HumanResult
not admissible as HUMAN_OWNED

Human browser QA:
HUMAN_OWNED / HUMAN_VERIFICATION / HUMAN_P1_7 only

PRE_HUMAN readiness:
required before HUMAN_REQUIRED

actual HumanResult:
absent/pending in first capture
```

A successful negative demonstration must not relabel S2-S4 as ACCEPTED.

# 7. evidence/Human/Judgment descriptors

Enrollment must freeze exact descriptors for later authoritative owners without issuing/admitting them now.

Use existing evidence/Human/Judgment types where possible.

Required distinction:

```text
expected contract descriptor
!=
admitted evidence
!=
HumanResult
!=
Judgment
```

Recommended runtime evidence mapping:

```text
summary-runtime:
TOOL_RUNTIME / version 1
producer:
SYSTEM_RUNTIME_OBSERVATION
with explicit ToolOutputRef lineage

policy-conflict-static:
STATIC_SOURCE / version 1
producer:
SYSTEM_STATIC_PROOF

human-browser-qa:
HUMAN_VERIFICATION / version 1
ownership:
HUMAN_OWNED
producer:
HUMAN_P1_7
```

Do not manufacture current attestations or evidence rows.

# 8. Stockroom tool registry/config

Create:

```text
config/providers/stockroom-tools.v1.toml
src/aiscc/providers/stockroom_tool.py
```

Freeze:

```text
registry_id:
aiscc-stockroom-tools

registry_version:
1

tool_id:
stockroom_summary

action:
fixed-stockroom-summary

dispatcher_version:
stockroom-summary-v1

side effect:
READ_ONLY

model-visible arguments:
empty object only
```

Allowed scenarios:

```text
S1
S2
S4
```

S3 tool dispatch is forbidden.

Public requester cannot select tool/action/argv/workdir/image/path.

The registry/config loader must be strict:

```text
unknown key:
deny

missing key:
deny

version mismatch:
deny

hidden fallback to legacy tool registry:
deny
```

Do not edit legacy `tool-registry.v1.toml`.

# 9. fixed Stockroom execution spec — descriptive construction only

B2 may construct/validate the exact structured Docker/tool spec but MUST NOT execute it.

Fixed later runtime invocation semantics:

```text
image:
server-pinned digest/config only

argv:
python -B -m stockroom summary

workdir:
/workspace

network:
none

source mount:
read-only materialized B1 workspace

shell:
none

arbitrary command:
none

non-root:
retain current secure runtime behavior

capabilities:
drop/deny according to current Docker contract
```

Output contract:

```text
exit:
0

stdout:
one ASCII JSON object + final LF
<= 4096 bytes

stderr:
empty

items:
BOX-A, BOX-B, BOX-C exact deterministic order/schema

total_available:
13
```

Expected values are test assertions only; they are not runtime evidence.

Known CLI error is a typed known failure only when exact bounded conditions prove it.
Unproven termination/transport ambiguity is `UnknownToolOutcome`.

# 10. receipt-aware consumed authority crossing

Current tool broker consumes capabilities before dispatch.
Current Docker path also consumes PROCESS capability.

B2 must prevent double consumption.

Modify only the authorized shared paths to implement a typed receipt-aware Stockroom crossing:

```text
src/aiscc/providers/ports.py
src/aiscc/providers/tools.py
src/aiscc/providers/service.py
src/aiscc/runtime/docker.py
```

Required semantics:

1. authentic consumed capability receipts are preserved in `ConsumedToolDispatch` or exact equivalent;
2. Stockroom uses a typed receipt-aware dispatcher protocol;
3. full resolved scope fingerprint includes complete resource/action/run/state/version/spec binding;
4. one authorized dispatch identity may be claimed once;
5. receipt replay, forgery, stale/cross-run/cross-state/cross-spec rebound deny;
6. Docker receipt-based entry verifies authentic consumed PROCESS receipt instead of consuming the same capability again;
7. legacy tool dispatch behavior remains backward compatible;
8. Stockroom may not fall back to capability-free legacy dispatcher;
9. unknown process termination/transport uncertainty cannot be classified as known TOOL_FAILED or TOOL_COMPLETED.

Do not weaken current capability issuance/admission semantics for non-Stockroom callers.

# 11. Docker shared modification boundary

`src/aiscc/runtime/docker.py` modification is allowed only for B2 receipt/bounded Stockroom execution support.

Required additive behavior:

```text
fixed workdir support for Stockroom:
server-owned only

finite stdout/stderr capture:
4096 bytes each for Stockroom path

finite operation timeout:
5 seconds

cleanup/reconciliation allowance:
10 seconds

attempt bound:
30 seconds

network:
none

no shell
```

On timeout/cancel:

```text
attempt exact container stop/kill using current safe owner identity
reconcile owner label/state
known settled failure:
KnownToolFailure

termination/transport not proven:
UnknownToolOutcome
quarantine/reconciliation required
no retry
```

Tests use fake/injected command/process boundaries only.

DO NOT run Docker in B2.

Do not modify generic runtime/process/network/cleanup modules.

# 12. local deterministic provider

Create:

```text
src/aiscc/providers/local_deterministic.py
config/providers/stockroom-owner-profiles.v1.toml
```

Identity:

```text
provider_id:
aiscc-local-deterministic

adapter_protocol_version:
stockroom-local-responses-v1

execution_backend_kind:
LOCAL_DETERMINISTIC_PROVIDER

external_llm_executed:
false

endpoint_ref:
local-in-process-stockroom-v1
```

Four exact owner-only profile IDs:

```text
stockroom-owner-s1-v1
stockroom-owner-s2-v1
stockroom-owner-s3-v1
stockroom-owner-s4-v1
```

Each profile version:

```text
1
```

Each binds exactly one scenario.

`model_ref` is an opaque deterministic script/schema identity, not an external model name.

If compatibility requires a `base_url`, only the accepted non-dialed loopback sentinel is allowed:

```text
http://127.0.0.1:1/v1
```

No socket/HTTP/OpenAI client may be created/imported by the local adapter.

Do not relabel `fake-openai-responses-v1`.

# 13. local provider secret-compatibility boundary

Preserve existing provider-service SECRET mediation rather than deleting it.

B2 may use only:

```text
server-owned opaque synthetic compatibility secret_ref
→ non-secret local sentinel
```

for the local deterministic adapter.

Requirements:

```text
no real credential
no external account
no secret-store provisioning
no raw secret in config/report/export
no secret in workspace/argv/output
```

The local adapter must explicitly reject use outside its owner-only local profiles.

`RESPONSES_CREATE` remains a compatibility protocol label, not an external API execution claim.

If preserving mediation requires a real credential or out-of-scope secret-owner mutation:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 14. local deterministic response protocol

For S1/S2/S4:

```text
initial local response:
exactly one stockroom_summary function call with {}

after exact correlated function_call_output:
bounded final deterministic structured disclosure
```

For S3:

```text
fixed policy-comparison response
no tool call permitted
```

Reject:

```text
wrong scenario/profile
wrong call_id
wrong version/order
unexpected continuation item
tool result mismatch
extra tool call
```

Finite bounds:

```text
S1/S2/S4:
provider calls <= 2
rounds <= 2
tool calls <= 1

S3:
provider calls <= 1
tool dispatch allowed = 0

input <= 16384 bytes
output <= 8192 bytes
continuation <= 16 items / 16384 bytes
call timeout <= 2 seconds
attempt <= 30 seconds
budget <= 4 units
```

No retrying outcome is emitted by the local adapter.

# 15. security owner policy

Create:

```text
src/aiscc/security/stockroom_policy.py
config/security/stockroom-owner.v1.toml
```

Modify:

```text
src/aiscc/security/policy.py
```

only as needed to inject mandatory Stockroom restriction into a dedicated owner policy instance.

The Stockroom restriction:

```text
does not grant capability by itself
defaults to DENY
must be present for this owner composition
```

It checks the full intersection:

```text
TaskContract/action
∩ RuntimeMode
∩ scenario_id/version
∩ provider profile/version
∩ run/attempt
∩ state/version
∩ resource_ref
∩ exact tool/process spec
∩ finite remaining limits
∩ current resource capability/lease
```

Minimum later capability domains:

```text
REPOSITORY
FILESYSTEM
PROCESS
TOOL
PROVIDER
SECRET compatibility mediation
```

NETWORK is denied.

Caller-provided `GRANTED` booleans alone never satisfy Stockroom restriction.

Do not change public profiles or hard security baselines.

Do not edit legacy security TOMLs.

# 16. exact stockroom-owner config

`config/security/stockroom-owner.v1.toml` must strictly bind:

```text
schema/version:
stockroom-owner-v1

runtime mode:
OWNER_SELF_DOGFOOD only

four scenario IDs/version 1.0.0

resource_ref:
repository:synthetic-stockroom@be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d

tool mapping:
stockroom_summary exact

profile mapping:
four exact local deterministic profile IDs/version 1

network:
DENY

finite tool/provider/process limits:
explicit

runtime-root/materialized-resource ownership:
server-issued only
```

Unknown/missing/duplicate/version mismatch denies.

No public-mode section.

# 17. provider service modification boundary

`src/aiscc/providers/service.py` may change only to support the B2 accepted crossing:

```text
sealed owner Stockroom enrollment restriction before capability issuance
receipt-aware Stockroom dispatch
typed UnknownToolOutcome handling
truthful local deterministic disclosure plumbing
```

Do not:

```text
remove existing secret mediation
change durable owner semantics
change public replay no-inference behavior
broaden provider/tool permissions
turn local profile into default
construct/execute B3 driver
```

Unknown outcome must not become a known success/failure.

# 18. strict non-execution requirement

B2 verification must perform:

```text
0 real provider calls
0 sockets/network
0 OpenAI/HTTP client construction in local adapter
0 Docker/container CLI execution
0 Stockroom Python/CLI execution
0 DB access/mutation
0 repository materialization
0 actual scenario driver execution
```

Use pure functions, temporary config fixtures and injected/fake dispatcher/process/security collaborators.

No broad runtime suite that might start Docker/DB/provider services.

# 19. required new unit tests

Create exactly:

```text
tests/unit/scenarios/test_runtime_enrollment.py
tests/unit/providers/test_stockroom_tool.py
tests/unit/providers/test_local_deterministic.py
tests/unit/security/test_stockroom_policy.py
```

## enrollment test minimum

Prove:

```text
4 exact scenario selections
scenario version/resource exact
no arbitrary input surface
owner mode exact
S1/S2/S3/S4 semantic distinctions
S3 tool denied
S4 Human ownership not replaceable
evidence descriptors frozen, not admitted
compile has zero side effects
```

## tool/broker test minimum

Prove:

```text
empty args only
exact registry/tool/action/version
full resolved fingerprint
authentic receipt required
one-use dispatch
double-consume impossible
receipt replay/forgery/stale/cross-run/cross-state/cross-spec denial
legacy path compatibility
Stockroom legacy/capability-free fallback denied
known failure vs unknown outcome
bounded stdout/stderr/timeout spec
fake process only
```

## local provider test minimum

Prove:

```text
4 exact profiles
owner mode only
no HTTP/socket/OpenAI construction
external_llm_executed=false exact
S1/S2/S4 one tool call then final response
S3 no tool
wrong call/order/profile/result denied
finite call/round/tool/input/output/budget bounds
synthetic compatibility secret only
```

## security test minimum

Independently deny every unresolved intersection dimension:

```text
wrong mode
scenario/version
profile/version
run/attempt
state/version
resource_ref
tool/action/spec fingerprint
missing/stale/forged receipt
missing/exhausted limits
network request
public mode
caller GRANTED without sealed owner context
unknown cleanup/materialization ownership
```

Prove valid exact owner context remains eligible for base policy evaluation; the Stockroom restriction itself does not grant.

# 20. required targeted regressions

Because B2 modifies shared provider/security/docker paths, also run the narrow existing regression modules that cover those owners if they exist at current HEAD.

At minimum the audit confirmed these exact files exist and should be included:

```text
tests/unit/providers/test_tools.py
tests/unit/providers/test_service.py
tests/unit/security/test_permission_policy.py
```

For `src/aiscc/runtime/docker.py`, discover only the existing directly corresponding unit test module by exact bounded filename/symbol search.

If exactly one direct Docker unit module exists, include it.
If none exists, report `NO_EXISTING_DIRECT_DOCKER_UNIT_MODULE` and rely on the new fake-boundary tool tests for the new B2 code.
If multiple plausible direct modules exist and cannot be disambiguated without widening scope:

```text
TEST_SCOPE_AMBIGUOUS
→ STOP
```

Do not run DB/Docker integration suites.

# 21. test execution discipline

Use the existing `.venv` only.

No package installation, dependency changes, network or environment provisioning.

Run:

1. four new B2 unit modules;
2. the three exact existing provider/security regression modules above;
3. the one exact direct Docker unit module if resolved;
4. Phase 1A/B1 regression modules only if a changed shared symbol directly breaks their import/contract and the exact affected module is identified.

No automatic broad suite expansion.

If the first required test command exits nonzero:

```text
TEST_FAILURE
→ STOP
```

Do not perform same-turn product/test repair after a mandatory test failure.

Return evidence to Browser Command Center for rework authorization.

# 22. static/source integrity

Require after successful tests:

```text
all 3 new TOML files parse under strict loaders

CREATE paths:
11 exact

MODIFY paths:
5 exact

other product/config/test changes:
0

B1 files:
unchanged

Phase 1A config/scenario files:
unchanged

bootstrap.py:
unchanged

dependency manifests:
unchanged

migration:
none

git diff --check:
PASS

index:
empty

Git-visible cache/pyc/pytest residue:
none
```

No Git add/commit.

# 23. expected final workspace

Before current Task lifecycle:

```text
pending governance:
2 exact current Cycle/Judgment

B2 product/config/test:
16 exact changed/created paths

Git-visible excluding active Task:
18 exact

index:
empty
```

Then move:

```text
.aiassistant/tasks/active/20260909_1648_aiscc-p2-3-phase1b-b2-scenario-tool-provider-security-enrollment-implementation-1.md
→
.aiassistant/tasks/done/20260909_1648_aiscc-p2-3-phase1b-b2-scenario-tool-provider-security-enrollment-implementation-1.md
```

Final:

```text
19 exact Git-visible paths
index empty
```

No other path.

# 24. evidence contract

executor_required:

- inbound ZIP/artifact transport
- repository gate
- exact 16-path B2 implementation
- strict config identity/binding proof
- four-scenario enrollment proof
- receipt-aware one-use tool authority proof
- local deterministic provider no-network/disclosure proof
- security intersection/deny proof
- shared provider/security/docker targeted regressions
- exact final workspace inventory
- outbound result ZIP

reuse_allowed:

- accepted Phase 1A static scenario/resource contracts
- persisted B1 materializer/workspace
- accepted 1329 Phase 1B design

human_owned:

```text
new Human QA:
NOT_REQUIRED

public distribution/license:
HUMAN_PENDING / outside B2
```

not_required:

```text
B3 composition
actual scenario execution
real provider/tool/Docker execution
DB
Replay
Browser QA
deployment
```

forbidden proof substitution:

```text
unit/local deterministic simulation
!=
actual scenario run

sealed test owner context
!=
runtime-issued security capability

Docker spec/fake runner test
!=
container execution proof

external_llm_executed=false config
!=
external LLM proof
```

# 25. explicit forbidden scope

Do NOT create/modify:

```text
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/composition.py
src/aiscc/bootstrap.py

src/aiscc/runtime/stockroom_workspace.py
src/aiscc/runtime/stockroom_materializer.py
src/aiscc/scenarios/runtime_models.py

config/scenarios/**
config/providers/provider-profiles.v1.toml
config/providers/tool-registry.v1.toml
config/security/permission-profiles.v1.toml
config/security/resource-policy.v1.toml
config/security/limits.v1.toml

src/aiscc/providers/models.py
src/aiscc/providers/profiles.py
src/aiscc/providers/authority.py
src/aiscc/providers/openai_responses.py

src/aiscc/runtime/process.py
src/aiscc/runtime/network.py
src/aiscc/runtime/cleanup.py

src/aiscc/workflow/**
src/aiscc/task_authority/**
src/aiscc/evidence/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/memory/**

src/aiscc/persistence/**
migrations/**
Replay/public/API/frontend/release code
dependency manifests
```

Do not execute:

```text
Docker
Stockroom CLI
provider network
DB
scenario driver
Git add/commit/push
P2-4/P3
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
MISSING_REQUIRED_ARTIFACT
UNEXPECTED_EXISTING_PATH
SCOPE_EXPANSION_REQUIRED
SECURITY_BOUNDARY_CONFLICT
TEST_SCOPE_AMBIGUOUS
BLOCKED_RUNTIME_PREREQUISITE
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

Inbound cleanup refusal after canonical transport is non-blocking.

# 27. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260909_1648_aiscc-p2-3-phase1b-b2-scenario-tool-provider-security-enrollment-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
ENROLLMENT_CONTRACT_VERIFICATION.md
TOOL_AUTHORITY_VERIFICATION.md
LOCAL_PROVIDER_VERIFICATION.md
SECURITY_POLICY_VERIFICATION.md
TEST_VERIFICATION.md
```

Include byte-preserving project-relative copies of:

```text
current Cycle
current Judgment
current done Task
all 16 B2 product/config/test paths
```

After bundle completion automatically create:

```text
.aiassistant/reports/target/20260909_1648_aiscc-p2-3-phase1b-b2-scenario-tool-provider-security-enrollment-implementation-1.zip
```

Require:

```text
one top-level bundle directory
readable archive
CRC PASS
required root files present
manifest coverage
folder/archive filename equality
folder/archive byte equality
```

Keep folder and outbound ZIP.

# 28. Task lifecycle

After implementation/test/report/export completes:

```text
.aiassistant/tasks/active/20260909_1648_aiscc-p2-3-phase1b-b2-scenario-tool-provider-security-enrollment-implementation-1.md
→
.aiassistant/tasks/done/20260909_1648_aiscc-p2-3-phase1b-b2-scenario-tool-provider-security-enrollment-implementation-1.md
```

Do not stage or commit.

# 29. final ceiling

Success:

```text
P2-3 Phase 1B-B2:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

P2-3 Phase 1B-B3:
NOT_STARTED

actual scenario capture:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Do not declare Phase 1B or P2-3 closed.
