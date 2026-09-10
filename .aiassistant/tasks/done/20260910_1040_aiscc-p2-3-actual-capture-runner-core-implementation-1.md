# 작업지시서: P2-3 actual-capture runner core implementation

## meta

- task_id: `20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1`
- created_at: `2026-09-10T10:40:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `ORCHESTRATION_IMPLEMENTATION / UNIT_REGRESSION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P2-3 owner-only actual-capture runner core`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `04343b8518c76c3fb7ed3f0afaf92bc7e79cbdcf`
- required_base_tree: `992a15a33e8b34cc3da35f44bd846ceddccb2526`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `source/static audit → capture orchestration source/test mutation`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. fresh-session Windows Python bootstrap

This Task begins in a fresh IDE Executor chat.

Do NOT assume any of these are valid through PATH:

```text
python
python3
py
```

Do NOT run bare `python` as a probe.

Known current interpreter candidate:

```text
C:\Users\oracl\AppData\Roaming\uv\python\cpython-3.12.14-windows-x86_64-none\python.exe
```

If Python is required for transport/static checks:

1. verify this exact executable exists and is executable;
2. if valid, use that exact path;
3. if unavailable, discover another actually executable Python interpreter;
4. invoke only its exact executable path.

The known path being absent is not itself a blocker.

For repository tests use the repository-owned exact executable:

```text
.venv\Scripts\python.exe
```

only after verifying it exists.

If a required interpreter cannot be found after discovery:

```text
PYTHON_INTERPRETER_REQUIRED_BUT_NOT_FOUND
→ STOP
```

# 1. purpose

Implement only the **owner-only capture runner core**.

The runner coordinates existing semantic owners in the accepted S1-S4 sequence but does not become the owner of:

```text
workflow transition admission
evidence admission
Human result
Judgment
security grant semantics
provider/tool execution semantics
process settlement
```

Production bootstrap/DB wiring and actual runtime execution are later cuts.

# 2. inbound ZIP bootstrap

The Browser Short Prompt's exact ZIP SHA-256 is the transport integrity anchor.

Current delivery ZIP contains only:

```text
TASK:
20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md

CYCLE:
20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md
SHA-256:
6a6195c8c430a9d292c765f6a044992970b945518c25a12e506737873999bbbb
destination:
.aiassistant/records/aiscc/cycles/20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md

JUDGMENT:
20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md
SHA-256:
48e84d88626bcd5804ff4f3f9c580c7f9d4efa28ea974adb5f69498afa8555c3
destination:
.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md

HANDOFF:
none
```

Executor:

1. verify exact ZIP filename/SHA-256;
2. validate archive readability/CRC/member safety;
3. place TASK first at `.aiassistant/tasks/active/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md`;
4. read TASK;
5. place Cycle/Judgment at exact canonical destinations;
6. verify exact hashes.

Bootstrap failure before TASK placement:

```text
STOP
no report/export
no substantive project mutation
```

After canonical transport, inbound cleanup refusal is non-blocking.

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

Expected Git-visible set excluding current active Task is exact 5 paths:

- `.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Do not cleanup/restore/stash/reset/absorb.

# 4. exact predecessor/runtime identity

Verify 1008 governance identity:

- `.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md`  `11db99ba9b22ed8e6dddab96d49d1a9207b928b846c93e53bcd88e48a8d10f52`
- `.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md`  `3cc310ccfe052307a906fe2524db6176f7af0d38ba53616096df6ece0ff581a0`
- `.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md`  `6cb059aa4206ac5e1f00789e8adbc955f574bf84c71b2e551c4f23a414e51ff0`

Verify persisted settlement source/test:

- `src/aiscc/runtime/docker.py`  `f338225c13195d69c41f69f00a47fc1d00c616c94458ef361e32b97f7fde96fa`
- `tests/unit/runtime/test_stockroom_docker_settlement.py`  `ebfb54d92dc446d2afe6bbe51ce261dbdabff92fa4650833f1d576fde6a755c6`

Any mismatch:

```text
PREDECESSOR_PROVENANCE_IDENTITY_MISMATCH
→ STOP
```

# 5. governance reads before mutation

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

.aiassistant/records/aiscc/cycles/20260910_1040_aiscc-p2-3-runtime-entry-audit-accepted-capture-runner-core-entry-1.cycle.md
.aiassistant/reports/aiscc/20260910_1040_aiscc-p2-3-actual-capture-runtime-entry-audit-final-acceptance-judgment-1.md

.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md
.aiassistant/records/aiscc/cycles/20260910_1008_aiscc-p2-3-stockroom-settlement-persisted-runtime-entry-audit-retry-1.cycle.md
.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md

.aiassistant/reports/aiscc/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-judgment-1.md
.aiassistant/reports/aiscc/20260910_0918_aiscc-p2-3-runtime-settlement-canonical-conflict-judgment-1.md
.aiassistant/reports/aiscc/20260910_0943_aiscc-p2-3-stockroom-docker-settlement-final-acceptance-judgment-1.md
```

Do not recursively activate old Task must-read lists.

# 6. source reads

Read fully before mutation:

```text
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/runtime_models.py
src/aiscc/scenarios/enrollment.py
src/aiscc/scenarios/composition.py

src/aiscc/workflow/kernel.py
src/aiscc/workflow/models.py
src/aiscc/workflow/matrix.py

src/aiscc/persistence/repository.py
src/aiscc/providers/service.py
src/aiscc/providers/stockroom_tool.py
src/aiscc/providers/local_deterministic.py
src/aiscc/security/policy.py
src/aiscc/security/stockroom_policy.py
src/aiscc/runtime/stockroom_materializer.py
src/aiscc/runtime/docker.py
src/aiscc/evidence/service.py
src/aiscc/human/authority.py
src/aiscc/human/repository.py
src/aiscc/judgment/authority.py

config/scenarios/stockroom/v1/s1-normal.json
config/scenarios/stockroom/v1/s2-missing-evidence.json
config/scenarios/stockroom/v1/s3-policy-conflict.json
config/scenarios/stockroom/v1/s4-human-owned-claim.json
```

Read direct imported types/call signatures only as needed.

# 7. pre-mutation exact-scope feasibility gate

Before editing, establish that the core runner can be implemented using only:

```text
src/aiscc/scenarios/capture_runner.py
tests/unit/scenarios/test_stockroom_capture_runner.py
src/aiscc/scenarios/driver.py
```

This A1 Task does not authorize production policy/config enrollment.

If implementation requires any change to:

```text
bootstrap.py
config/evidence/**
config/human/**
config/judgment/**
provider/security/runtime/evidence/Human/Judgment owners
migration/schema
```

STOP before product mutation with:

```text
SCOPE_EXPANSION_REQUIRED
```

and report the exact required path/reason.

Do not partially implement then request expansion.

# 8. exact mutation allowlist — 3 paths

## CREATE

- `src/aiscc/scenarios/capture_runner.py`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`

Both must be absent before mutation.

## MODIFY

```text
src/aiscc/scenarios/driver.py
```

It must be tracked/clean at required base HEAD.

No other source/config/test path may change.

If either CREATE path exists:

```text
UNEXPECTED_EXISTING_PATH
→ STOP
```

# 9. capture runner semantic ownership

Create:

```text
src/aiscc/scenarios/capture_runner.py
```

Use repository naming/types and existing owners.

The runner is an orchestration coordinator only.

It may:

```text
read immutable PreparedStockroomDriver/request/enrollment
call explicit injected authoritative owners
sequence owner calls
carry stable refs/IDs between owners
return immutable orchestration result/progress refs
stop fail-closed on denied/unknown owner results
```

It must NOT:

```text
directly mutate DB tables
manufacture TransitionDecision
manufacture AdmittedEvidenceRef
manufacture HumanResult
manufacture authoritative Judgment
mint security authority outside SecurityPolicy
call subprocess/Docker directly
bypass AgentExecutionService/Stockroom dispatcher
silently retry unknown process/tool outcome
translate Agent claim into Human-owned evidence/result
```

# 10. driver.py modification boundary

Modify:

```text
src/aiscc/scenarios/driver.py
```

Only add the minimal immutable runner-facing input/result/progress contract needed by `capture_runner.py`, consistent with existing naming.

Preserve:

```text
PreparedStockroomDriver inert construction
existing B3 APIs
existing dependency bundle semantics
zero implicit execution
```

Do not add an automatically executing method to `PreparedStockroomDriver`.

Do not move semantic authority from existing owners into driver dataclasses.

# 11. runner entry contract

Expose one explicit owner-only entry point consistent with current style, semantically equivalent to:

```text
StockroomCaptureRunner.run(prepared_driver, ...)
```

or a function with the same explicit semantics.

It must require:

```text
PreparedStockroomDriver
explicit run/attempt identity from the prepared request
exact scenario enrollment
explicit existing owner dependencies
```

No requester-controlled runtime mode/config/source path.

Only:

```text
OWNER_SELF_DOGFOOD
```

is accepted.

Unknown scenario/mode/binding mismatch:

```text
fail closed before side effects
```

# 12. common orchestration contract

For execution-bearing scenarios S1/S2/S4, the runner sequence must preserve owner boundaries equivalent to:

```text
1. authoritative initial READY creation/lookup
2. create attempt
3. request READY -> RUNNING
4. seal/validate Stockroom owner context
5. request bounded security grants/capabilities through SecurityPolicy
6. invoke StockroomMaterializer through its owner
7. invoke AgentExecutionService using local deterministic provider path
8. preserve execution/private-protocol/output refs through existing execution owner
9. request RUNNING -> ADMISSION_PENDING
10. scenario-specific evidence/Human/Judgment routing
11. request scenario-specific final/nonterminal transition
```

If a current API combines/reorders specific substeps canonically, follow the current API and record the exact mapping in tests/report.

The runner must not fake successful owner outputs.

# 13. S1 behavior

For:

```text
stockroom-s1-normal
```

core orchestration target:

```text
READY
→ RUNNING
→ ADMISSION_PENDING
→ ACCEPTED
```

Required owner calls:

```text
runtime execution path
summary-runtime evidence candidate/submission/admission owner
evidence-set/checkpoint evaluation
System deterministic ACCEPTED Judgment owner
separate ACCEPTED transition request
```

The runner may only carry returned evidence/Judgment refs.

It must never construct them as authoritative records itself.

# 14. S2 behavior

For:

```text
stockroom-s2-missing-evidence
```

runtime path may execute.

Then exact fixture directive:

```text
OMIT_REQUIRED_EVIDENCE_CANDIDATE
```

must result in:

```text
summary-runtime candidate:
NOT_SUBMITTED

requirement:
UNSATISFIED

evidence substitution:
NONE

Judgment:
HOLD_REWORK_REQUIRED via authoritative owner

workflow:
REWORK_REQUIRED
```

No same-run automatic retry.

The runner result must expose that later retry requires new revision/attempt authority.

# 15. S3 behavior

For:

```text
stockroom-s3-policy-conflict
```

Required:

```text
READY -> RUNNING
```

then local fixed policy-conflict branch.

Must NOT call:

```text
StockroomMaterializer.materialize
AgentExecutionService.execute
LocalDeterministicProvider.call
StockroomSummaryDispatcher dispatch
DockerRuntime
```

Produce/submit only the exact current-authorized static policy evidence path through evidence owner APIs.

Create/use the current blocker claim mechanism with:

```text
type:
POLICY

reason:
POLICY_CONFLICT
```

Then request:

```text
RUNNING -> BLOCKED
```

No Judgment is issued.

If current P1-4/P1-6 APIs cannot express this without new config/shared-owner mutation, trigger `SCOPE_EXPANSION_REQUIRED` under section 7.

# 16. S4 behavior

For:

```text
stockroom-s4-human-owned-claim
```

Execute the common runtime path and summary evidence admission.

The synthetic Agent Human-QA claim must remain:

```text
not HumanResult
not HUMAN_OWNED admitted evidence
```

Open/reserve the exact Human gate through current Human owner APIs.

Then request:

```text
ADMISSION_PENDING -> HUMAN_REQUIRED
```

Result must show:

```text
gate:
PENDING/ACTIVE or exact current projection

HumanResult:
ABSENT

Judgment:
ABSENT

automatic continuation:
NO
```

Do not create/submit any HumanResult.

# 17. failure / unknown behavior

For any owner call yielding:

```text
DENIED
stale
version mismatch
unknown tool/process outcome
unsettled/quarantine-required process
evidence admission rejection
gate reservation denial
Judgment issuance denial
```

the runner must:

```text
stop deterministic forward orchestration
preserve returned refs/reason
not retry automatically
not synthesize replacement evidence/Human/Judgment
not request a success/rework terminal transition that lacks its guard
```

Exact failure projection/result should use existing current-domain result types where available.

No blanket exception swallowing.

# 18. idempotency/reentry

Runner core must not create a hidden same-run retry loop.

Unit tests must prove at least:

```text
same invocation identity is carried to owner calls
duplicate/denied owner response is not bypassed
unknown process outcome does not trigger second execution
S2 does not retry to fill omitted evidence
S4 stops at Human boundary
```

Do not invent a new durable idempotency store in A1.

# 19. unit test owner

Create:

```text
tests/unit/scenarios/test_stockroom_capture_runner.py
```

Use explicit recording/never-call fake owners satisfying the current interfaces.

No DB, Docker, filesystem materialization, subprocess, network or real provider/tool execution.

Minimum successful-path proofs:

```text
S1 exact owner-call order and ACCEPTED target
S2 exact owner-call order, omitted evidence, REWORK_REQUIRED, no retry
S3 exact no-runtime/no-tool branch and BLOCKED target, no Judgment
S4 exact Human gate boundary and HUMAN_REQUIRED target, no HumanResult/Judgment
```

Minimum authority proofs:

```text
TransitionDecision not fabricated
AdmittedEvidenceRef not fabricated
HumanResult not fabricated
Judgment not fabricated
Agent claim not substituted
tool output not treated as admitted evidence
Judgment ref not treated as transition
```

Minimum failure proofs:

```text
transition denied
security/grant denied
materializer failure
provider/tool unknown outcome
quarantine-required outcome
evidence admission rejected
Human gate denial
Judgment denial
```

For each prove:

```text
no later owner calls after fail-closed boundary
no automatic retry
```

# 20. no-side-effect unit tripwires

Patch/guard real executable boundaries so the unit module fails immediately if it accidentally reaches:

```text
Postgres/session/DB connection
DockerRuntime real runner
subprocess
socket/network/HTTP/OpenAI
real StockroomMaterializer filesystem/git path
real LocalDeterministicProvider execution
real StockroomSummaryDispatcher execution
```

The test should exercise only recording fakes.

# 21. static checks

After implementation run non-mutating checks on exact 3 paths:

```text
Python compile:
3 / 3

Ruff:
3 / 3

git diff --check:
PASS

index:
empty
```

No auto-fix.

If static check fails:

```text
STATIC_CHECK_FAILURE
→ STOP
```

No same-turn repair after this mandatory gate.

# 22. mandatory A1 unit command

Only after static PASS, run exactly:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider tests/unit/scenarios/test_stockroom_capture_runner.py -ra
```

Require:

```text
exit 0
failed 0
errors 0
```

If failure:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair.

# 23. mandatory B3 regression

Only after new unit PASS, run exactly:

```text
.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_owner_composition.py   tests/integration/scenarios/test_stockroom_binding.py -ra
```

Require exit 0.

This is allowed because the existing B3 integration module is zero-side-effect/fake-boundary proof and requires no DB/Docker/network.

If failure:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair.

# 24. bounded driver regression discovery

Search only:

```text
tests/unit/scenarios/**
tests/integration/scenarios/**
```

for direct imports/calls of:

```text
PreparedStockroomDriver
StockroomOwnerDependencies
StockroomDriverRequest
```

Run additional direct modules only if the bounded set is unambiguous and does not require DB/Docker/network.

If none beyond section 23:

```text
NO_ADDITIONAL_DIRECT_DRIVER_REGRESSION
```

If ambiguity requires broad expansion:

```text
TEST_SCOPE_AMBIGUOUS
→ STOP
```

# 25. final source contract review

Require PASS for:

```text
RUNNER_ORCHESTRATION_ONLY
EXISTING_OWNER_AUTHORITY_PRESERVED
S1_ACCEPT_PATH
S2_CONTROLLED_EVIDENCE_OMISSION
S3_NO_TOOL_BLOCKED_PATH
S4_HUMAN_PENDING_PATH
NO_PROOF_SUBSTITUTION
NO_AUTOMATIC_RETRY
UNKNOWN_FAIL_CLOSED
PREPARED_DRIVER_REMAINS_INERT
NO_PRODUCTION_OWNER_CONSTRUCTION
NO_PUBLIC_MODE
```

# 26. strict no-runtime ceiling

This Task must perform:

```text
DB:
NOT_RUN

Docker CLI/daemon/image:
NOT_RUN

real Stockroom process:
NOT_RUN

real materialization:
NOT_RUN

real provider/tool:
NOT_RUN

network:
NOT_RUN

HumanResult:
NOT_CREATED

real Judgment:
NOT_CREATED

actual scenario:
NOT_RUN

Git add/commit/push:
NOT_RUN
```

Unit/fake owner calls are not runtime evidence.

# 27. final workspace

Before current Task lifecycle require:

```text
1008 governance:
3

current Cycle/Judgment:
2

A1 source/test:
3

total excluding active Task:
8 exact

index:
empty
```

Then move:

```text
.aiassistant/tasks/active/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md
→
.aiassistant/tasks/done/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1.md
```

Final:

```text
9 exact Git-visible paths
index empty
```

No other path.

# 28. evidence contract

executor_required:

- fresh-session interpreter discovery discipline
- inbound transport
- exact five-path preflight
- predecessor/runtime identity
- pre-mutation three-path feasibility gate
- exact three-path implementation
- static checks PASS
- A1 unit tests PASS
- B3 regression PASS
- bounded direct driver regression result
- 12-item source contract review
- strict no-runtime proof
- exact final workspace
- outbound result ZIP

reuse_allowed:

- accepted 1008 runtime-entry audit
- persisted B1/B2/B3
- persisted Stockroom settlement fix

human_owned:

```text
S4 HumanResult:
HUMAN_PENDING / not part of A1

public distribution/license:
HUMAN_PENDING
```

not_required:

```text
production bootstrap construction
PostgreSQL integration
Docker image provisioning
actual runtime/capture
capture/export schema
Replay
deployment
```

forbidden:

```text
bootstrap.py mutation
config/** mutation
provider/security/runtime/evidence/Human/Judgment shared-owner mutation
migration
real runtime execution
Git staging/commit/push
P2-4/P3
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
UNEXPECTED_EXISTING_PATH
SCOPE_EXPANSION_REQUIRED
STATIC_CHECK_FAILURE
TEST_SCOPE_AMBIGUOUS
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

After any mandatory implementation/test STOP, do not perform same-turn source/test repair unless a future Command Center Task explicitly authorizes it.

Inbound cleanup refusal after canonical transport is non-blocking.

# 30. export bundle + outbound ZIP

Bundle folder:

```text
.aiassistant/reports/target/20260910_1040_aiscc-p2-3-actual-capture-runner-core-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
RUNNER_CONTRACT_VERIFICATION.md
SCENARIO_SEQUENCE_VERIFICATION.md
AUTHORITY_NON_SUBSTITUTION_VERIFICATION.md
TEST_VERIFICATION.md
```

Include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
all three A1 source/test paths
```

Create adjacent outbound ZIP automatically.

Use Windows extended-length path handling from the outset if needed.

Require:

```text
one top-level bundle directory
readable / CRC PASS
required roots present
manifest coverage
folder/archive byte equality
```

# 31. final ceiling

Success:

```text
P2-3 actual-capture runner core:
READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

production owner/bootstrap integration:
NOT_STARTED

runtime prerequisites:
NOT_VERIFIED

actual scenario execution:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Do not start A2/runtime provisioning/actual capture in this Task.
