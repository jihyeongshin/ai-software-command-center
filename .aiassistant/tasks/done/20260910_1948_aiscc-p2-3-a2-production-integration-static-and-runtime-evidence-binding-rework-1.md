# 작업지시서: P2-3 A2 production integration static + runtime-evidence binding rework

## meta

- task_id: `20260910_1948_aiscc-p2-3-a2-production-integration-static-and-runtime-evidence-binding-rework-1`
- created_at: `2026-09-10T19:48:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `IMPLEMENTATION_REWORK / CONFIG_FROZEN / POSTGRESQL_INTEGRATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Continue the existing A2 candidate.

Close:

```text
1. five Ruff findings
2. runtime-summary evidence producer/source binding defect
3. then execute the previously blocked static + PostgreSQL + regression proof
```

Do not expand A2 into actual Stockroom execution.

# 1. inbound transport

Verify Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_1948_aiscc-p2-3-a2-production-integration-static-and-runtime-evidence-binding-rework-1.md
```

Read it fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-rework-entry-1.cycle.md
SHA-256:
2206f489bca4de6f1da211beeba932e0125da05dceeb329bef9fe19938770dd1

.aiassistant/reports/aiscc/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-judgment-1.md
SHA-256:
534a863b8df861cd96091e7678b58ed12b35eebd6272ed867ab55a1d240e58ea
```

Bootstrap failure before TASK placement:

```text
STOP
no report/export
no substantive mutation
```

# 2. repository gate

Require:

```text
branch:
main

HEAD:
876f232880e652fbf715f13c13b8cc03d27404f0

HEAD tree:
0f855b67fcad1be1cb4f635b6b4db8856c43da64

index:
empty
```

Expected Git-visible set excluding active Task is exact 14 paths:

- `.aiassistant/tasks/done/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1824_aiscc-p2-3-a2-feasibility-accepted-production-integration-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1824_aiscc-p2-3-a2-feasibility-audit-final-acceptance-judgment-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `config/evidence/stockroom-capture.v1.json`
- `config/human/stockroom-capture.v1.json`
- `config/judgment/stockroom-capture.v1.json`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `.aiassistant/records/aiscc/cycles/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Ignored target/export residue may remain non-blocking.

No reset/restore/stash/broad cleanup.

# 3. exact predecessor/candidate identity

Require exact 1738 provenance:

- `.aiassistant/tasks/done/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md`  `c8f6615b9ce5943e1bee43046d50dd2dac4efba99a96179043177530f3a96ce4`
- `.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md`  `0e6b3a12767fc3d5830726e1327d8e0d6f097271aa7aedd4157a4b86a566a782`
- `.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md`  `4df00fc71ff6603cb0703077c10c5460d3db2bdb6ec772a2b3fbd8b5983ed476`

Require exact 1824 provenance:

- `.aiassistant/tasks/done/20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1.md`  `13b3561669bfa5c9343bc0339f52bb77b06eab56e1c97369f6a4973766178997`
- `.aiassistant/records/aiscc/cycles/20260910_1824_aiscc-p2-3-a2-feasibility-accepted-production-integration-entry-1.cycle.md`  `a02818022b2c694ad2644c2222e127de87c38f360b65fc33937c42af2cdb9846`
- `.aiassistant/reports/aiscc/20260910_1824_aiscc-p2-3-a2-feasibility-audit-final-acceptance-judgment-1.md`  `743103b7e8e22c7833bd555ff8ceedd0e0f34e0ab4994f077006864fbf172a85`

Require exact starting A2 candidate:

- `src/aiscc/bootstrap.py`  `a9b391e38b851cbca744479697e7ceecc29389c40a42ce2bc2eea3eed6975950`
- `src/aiscc/scenarios/stockroom_production.py`  `ecd6b4bb4022b248b1698da7ea81279bef4e365c08b0cf39e912e959c2081f6b`
- `config/evidence/stockroom-capture.v1.json`  `70d4dbf219d54abd57877b787d8ac16d0efbe05701e7fb8bf1f84282640b31e7`
- `config/human/stockroom-capture.v1.json`  `7ec43975b8d1f30ded987d05942753dadbd93197ad86da2701514a198e797bab`
- `config/judgment/stockroom-capture.v1.json`  `31f8d08c083218d1fcc47d5ba7a8d1c151a48bbf26ea3319ac9503a666179eef`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `5043cb581e83c2a5f1696f1d0ee1cc191b426423124e8b228240e72a947e00d0`

Require accepted A1 identity still exact at HEAD:

- `src/aiscc/scenarios/capture_runner.py`  `600de0a4b0e718f02ab2e1907b7be62b2c4a23756559fdf99cb4cd55fb80b3d2`
- `src/aiscc/scenarios/driver.py`  `9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`  `a137021608ac9cb5b4c328b6bb88fd0c22cb0d9afd9b1a22054ec5bdd32f68ff`

Any mismatch:

```text
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

# 4. exact mutation authority

Only:

```text
MODIFY:
src/aiscc/bootstrap.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Frozen byte-exact throughout:

```text
config/evidence/stockroom-capture.v1.json
70d4dbf219d54abd57877b787d8ac16d0efbe05701e7fb8bf1f84282640b31e7

config/human/stockroom-capture.v1.json
7ec43975b8d1f30ded987d05942753dadbd93197ad86da2701514a198e797bab

config/judgment/stockroom-capture.v1.json
31f8d08c083218d1fcc47d5ba7a8d1c151a48bbf26ea3319ac9503a666179eef
```

Also frozen:

```text
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/enrollment.py
all migration files
```

If another path is needed:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 5. exact Ruff repair

Repair all reported Ruff findings without unrelated semantic edits.

Starting findings:

```text
src/aiscc/bootstrap.py:
UP037 x3

src/aiscc/scenarios/stockroom_production.py:
I001 x1
E501 x1
```

UP037 changes are annotation-modernization only.

I001 is import ordering only.

E501 is line wrapping only.

Do not alter behavior merely to satisfy style.

# 6. runtime-summary evidence provenance correction

Current candidate is not acceptable because `submit_runtime_evidence` can construct correct-looking runtime evidence from a valid `AgentOutputRef` while not requiring the actual Stockroom tool result.

Required invariant:

```text
Agent completion/submission provenance
!=
Stockroom runtime-summary observation provenance
```

For S1/S4 runtime-summary evidence, require all:

```text
1. execution_ref resolves to the authentic DurableExecutionResult
2. final ExecutionSubmissionRef is present and current
3. exactly one current same-attempt AgentOutputRef exists and verifies
4. exactly one current same-attempt ToolOutputRef exists and verifies
5. ToolOutputRef.content_hash equals canonical_sha256(STOCKROOM_SUMMARY)
6. tool-output provenance is retained in the evidence body
7. producer_attestation_ref binds to the authentic ToolOutputRef provenance
```

Use the current P1-5/P1-6 owner APIs; do not create a parallel authority.

The accepted Stockroom tool already proves at dispatch time:

```text
actual process stdout
→ strict JSON parse
→ exact output == STOCKROOM_SUMMARY
→ ToolOutputRef.result_hash = canonical_sha256(actual output)
→ durable ToolOutputRef persistence
```

Therefore the adapter may derive the server-owned runtime observation from `STOCKROOM_SUMMARY` **only after** authentic same-attempt ToolOutputRef verification and exact result-hash equality.

Do not simply keep literal `13` / reorder rule as unbound facts.

Prefer explicit derivation from the accepted canonical summary/policy source after ToolOutputRef verification.

Evidence body must retain enough provenance to review:

```text
scenario_id
execution_submission_ref
agent_output_ref
agent_output_hash
tool_output_ref
tool_output_hash
summary / canonical Stockroom observation
total_available derived from verified summary
reorder_rule derived from accepted Stockroom rule/source
```

Exact field naming may follow existing P1-6 schema conventions.

# 7. fail-closed runtime evidence cases

Before calling `EvidenceAdmissionService.submit_durable`, fail closed on:

```text
ToolOutputRef missing
ToolOutputRef duplicated
wrong ref kind
wrong attempt/run binding
P1-5 verify false
tool output hash != canonical_sha256(STOCKROOM_SUMMARY)
AgentOutputRef missing/duplicate/unverified
execution submission absent/stale
```

Required outcome:

```text
no durable P1-6 candidate admitted
no substitute evidence
no fallback to hard-coded correct values
```

Use existing adapter status taxonomy.

# 8. test extension for producer binding

Modify only the existing A2 integration module.

Add direct regression coverage for the runtime-evidence source-binding rule without executing Docker/provider/tool.

At minimum prove a pure/bounded helper or repository-owner boundary equivalent for:

```text
verified ToolOutputRef hash == canonical STOCKROOM_SUMMARY
→ observation derivation allowed

ToolOutputRef missing
→ denied

ToolOutputRef wrong hash
→ denied

AgentOutputRef exists but ToolOutputRef absent
→ denied

ToolOutputRef belongs to wrong attempt
→ denied
```

Do not make a fake ToolOutputRef count as actual runtime evidence.

The test is contract proof for adapter behavior only.

Any durable rows required for this test must be created through existing repository owner APIs, not direct SQL INSERT/UPDATE state fabrication.

# 9. migration gate

Re-run the static migration head check.

Expected current head:

```text
20260901_0008
```

No migration is authorized.

If source/model requirements now need schema change:

```text
MIGRATION_SCOPE_REQUIRED
→ STOP
```

# 10. full static gate — restart from beginning

Run all, even items blocked in 1824:

```text
Python compile:
src/aiscc/bootstrap.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/driver.py
tests/integration/scenarios/test_stockroom_capture_runner.py

Ruff:
same five Python paths

strict JSON parse:
config/evidence/stockroom-capture.v1.json
config/human/stockroom-capture.v1.json
config/judgment/stockroom-capture.v1.json

git diff --check
index verification
```

Require:

```text
compile:
5 / 5 PASS

Ruff:
5 / 5 path set PASS

JSON:
3 / 3 PASS

git diff --check:
PASS

index:
empty
```

If any mandatory static check fails:

```text
STATIC_CHECK_FAILURE
→ STOP
```

No same-turn second repair after the mandatory static gate.

# 11. PostgreSQL prerequisite — explicit disposable fallback

1824 reported:

```text
AISCC_TEST_DATABASE_URL:
absent
```

After static PASS, first check whether a compatible local disposable PostgreSQL environment is already available.

If not, this Task authorizes one Task-owned local prerequisite using the established repository pattern:

```text
Docker image:
postgres:17.6-alpine

pull policy:
--pull=never

container name:
aiscc-p2-3-a2-postgres

bind preference:
127.0.0.1:55442
fallback:
127.0.0.1:55443
then:
127.0.0.1:55444

storage:
temporary / disposable
prefer tmpfs when supported
```

Before creation:

```text
verify Docker availability
verify local image exists
verify container name/ports are not owned by unrelated resources
```

Forbidden:

```text
docker pull
external network
remote DB
shared production/test DB
deleting unrelated container
persistent credential file
```

If Docker or the local image is absent:

```text
POSTGRESQL_TEST_PREREQUISITE_MISSING
→ STOP
```

Set credential-bearing URL only in Task process environment:

```text
AISCC_DATABASE_URL
AISCC_TEST_DATABASE_URL
```

Do not print/export credential values.

Run existing:

```text
.venv\Scripts\python.exe -B -m alembic upgrade head
```

against the Task-owned DB and verify applied head.

# 12. mandatory A2 PostgreSQL integration

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/scenarios/test_stockroom_capture_runner.py -ra
```

Success requires:

```text
exit 0
passed >= 1
skipped == 0
failed/errors == 0
```

A no-DB skip is **not** PASS.

If prerequisite-related skip/nonexecution occurs:

```text
POSTGRESQL_TEST_PREREQUISITE_MISSING
→ STOP
```

If executed test fails:

```text
TEST_FAILURE
→ STOP
```

No same-turn repair.

# 13. A1/B3 regression

Only after A2 integration PASS:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_stockroom_capture_runner.py   tests/unit/scenarios/test_owner_composition.py   tests/integration/scenarios/test_stockroom_binding.py -ra
```

Require:

```text
failed/errors:
0

skipped:
0 unless a pre-existing accepted test contract explicitly requires it
```

# 14. bounded direct-owner regressions

Discover and run only direct existing tests for actual owners imported by `stockroom_production.py`.

Bounded domains:

```text
workflow transition
P1-6 evidence registration/admission
P1-7 Human reservation/gate
P1-7 Judgment policy/authority
Stockroom security policy
```

Do not run whole repository suite.

Record exact modules and counts.

# 15. integration proof ceiling

The A2 test may execute:

```text
real PostgreSQL schema/migrations
real NONE -> READY
real create_attempt
real READY -> RUNNING
real config registration/lookup
real in-memory security grant evaluation
```

It must not execute:

```text
Stockroom materialization
Stockroom Docker/process
provider
tool
AgentExecutionService runtime execution
network
real secret
full runner.run()
actual S1-S4
HumanResult
terminal scenario Judgment
Replay
```

Fail-on-call counters remain required for forbidden runtime edges.

# 16. contract review

Require PASS:

```text
THIN_BOOTSTRAP
NO_GLOBAL_SERVICE_LOCATOR
EXPLICIT_OPERATOR_DEPENDENCIES
SINGLE_SHARED_POSTGRES_SESSION_FACTORY
WORKFLOW_OWNER_PRESERVED
EVIDENCE_OWNER_PRESERVED
HUMAN_OWNER_PRESERVED
JUDGMENT_OWNER_PRESERVED
SECURITY_OWNER_PRESERVED
ADAPTER_DOES_NOT_MINT_AUTHORITY
NONWORKFLOW_SNAPSHOT_FROM_KERNEL
TRANSITION_CROSSCHECKS_KERNEL
EVIDENCE_CONFIG_STRICT_AND_VERSIONED
RUNTIME_EVIDENCE_REQUIRES_TOOL_OUTPUT_REF
RUNTIME_EVIDENCE_TOOL_HASH_BOUND
AGENT_OUTPUT_NOT_RUNTIME_EVIDENCE_SUBSTITUTE
S2_OMISSION_NOT_SUBSTITUTED
S3_STATIC_EVIDENCE_NOT_JUDGMENT
S4_HUMAN_RESULT_ABSENT
JUDGMENT_ONLY_S1_S2
NETWORK_DENIED
NO_DIRECT_SQL_STATE_FABRICATION
A1_RUNNER_DRIVER_UNCHANGED
NO_STOCKROOM_RUNTIME_EXECUTION
```

Require:

```text
24 / 24 PASS
```

# 17. PostgreSQL cleanup

If this Task created the disposable PostgreSQL container/database:

```text
stop/remove only that exact Task-owned container after all required test evidence is collected
```

Verify its removal.

Do not remove a pre-existing Human/unrelated container.

# 18. final workspace

Before Task lifecycle require:

```text
1738 governance:
3

1824 governance:
3

A2 candidate paths:
6

current Cycle/Judgment:
2

total excluding active Task:
14 exact

index:
empty
```

Then move active Task byte-identically to done.

Final:

```text
15 exact Git-visible paths
index empty
```

No other path.

# 19. no Git persistence

This rework Task does **not** authorize:

```text
git add
git commit
git push
```

A2 persistence is a later Browser judgment decision.

# 20. required export bundle

Folder:

```text
.aiassistant/reports/target/20260910_1948_aiscc-p2-3-a2-production-integration-static-and-runtime-evidence-binding-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
MIGRATION_COMPATIBILITY.md
IMPLEMENTATION_MANIFEST.md
RUNTIME_EVIDENCE_BINDING_VERIFICATION.md
PRODUCTION_GRAPH_VERIFICATION.md
ADAPTER_AUTHORITY_VERIFICATION.md
CONFIG_ENROLLMENT_VERIFICATION.md
POSTGRESQL_INTEGRATION_VERIFICATION.md
SECURITY_BOUNDARY_VERIFICATION.md
TEST_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
all six A2 candidate implementation/config/test paths
```

Expected:

```text
14 root docs
9 canonical/source copies
23 members total
```

`EXPORT_MANIFEST.md` covers all 22 non-self entries with relative path, byte size, SHA-256.

Require:

```text
one top-level directory
23 exact members
CRC PASS
14/14 roots
9/9 copies
manifest 22/22 exact
folder/archive byte equality
```

# 21. mandatory stop

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
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
SCOPE_EXPANSION_REQUIRED
MIGRATION_SCOPE_REQUIRED
STATIC_CHECK_FAILURE
POSTGRESQL_TEST_PREREQUISITE_MISSING
TEST_FAILURE
CONTRACT_MISMATCH
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

No same-turn repair after mandatory static/test failure.

# 22. success ceiling

Success:

```text
A2 production owner/bootstrap integration:
IMPLEMENTED_CANDIDATE / READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

PostgreSQL owner-boundary proof:
EXECUTED_PASS

runtime-summary evidence source binding:
VERIFIED_CANDIDATE

Stockroom Docker/materialization/provider/tool prerequisites:
NOT_VERIFIED

actual S1-S4:
NOT_STARTED

capture/export corpus:
NOT_STARTED

Replay:
NOT_STARTED
```
