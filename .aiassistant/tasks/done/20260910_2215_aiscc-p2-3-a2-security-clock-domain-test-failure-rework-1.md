# 작업지시서: P2-3 A2 security clock-domain test-failure rework

## meta

- task_id: `20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-rework-1`
- created_at: `2026-09-10T22:15:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `IMPLEMENTATION_REWORK / POSTGRESQL_INTEGRATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Continue the exact A2 candidate.

Fix only the security TTL clock-domain mismatch demonstrated by the 1948 PostgreSQL test, then complete the previously blocked evidence chain.

Do not weaken P1-3 SecurityPolicy.

# 1. inbound transport

Verify Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-rework-1.md
```

Read it fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260910_2215_aiscc-p2-3-a2-security-clock-domain-rework-entry-1.cycle.md
SHA-256:
dde57e4dae071826ca377b9cc32a4a34cf25dd3d368b897d695156e600022eec

.aiassistant/reports/aiscc/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-judgment-1.md
SHA-256:
ea62c1e759018fcc21b32e0760915c38f8c1afe092ecb550025a9021ac2ce201
```

Bootstrap failure before Task placement:

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

Expected Git-visible set excluding active Task is exact 17 paths:

- `.aiassistant/tasks/done/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1824_aiscc-p2-3-a2-feasibility-accepted-production-integration-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1824_aiscc-p2-3-a2-feasibility-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1948_aiscc-p2-3-a2-production-integration-static-and-runtime-evidence-binding-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-judgment-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `config/evidence/stockroom-capture.v1.json`
- `config/human/stockroom-capture.v1.json`
- `config/judgment/stockroom-capture.v1.json`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `.aiassistant/records/aiscc/cycles/20260910_2215_aiscc-p2-3-a2-security-clock-domain-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-judgment-1.md`

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

Require exact 1948 provenance:

- `.aiassistant/tasks/done/20260910_1948_aiscc-p2-3-a2-production-integration-static-and-runtime-evidence-binding-rework-1.md`  `2592d9fc0635c4fc61b41929d78bab59b9de19c496fe8d98334bb14e12148e5b`
- `.aiassistant/records/aiscc/cycles/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-rework-entry-1.cycle.md`  `2206f489bca4de6f1da211beeba932e0125da05dceeb329bef9fe19938770dd1`
- `.aiassistant/reports/aiscc/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-judgment-1.md`  `534a863b8df861cd96091e7678b58ed12b35eebd6272ed867ab55a1d240e58ea`

Require exact current A2 candidate:

- `src/aiscc/bootstrap.py`  `1718e596b20fd107af0cb80b6ad40e3626b7e26d8d45daa649ccf2d2ccf9fe38`
- `src/aiscc/scenarios/stockroom_production.py`  `971f4657dac3ad93b8e6f2e4a54201f03ccdf1a98b120fe5ab10ba67ca016c11`
- `config/evidence/stockroom-capture.v1.json`  `70d4dbf219d54abd57877b787d8ac16d0efbe05701e7fb8bf1f84282640b31e7`
- `config/human/stockroom-capture.v1.json`  `7ec43975b8d1f30ded987d05942753dadbd93197ad86da2701514a198e797bab`
- `config/judgment/stockroom-capture.v1.json`  `31f8d08c083218d1fcc47d5ba7a8d1c151a48bbf26ea3319ac9503a666179eef`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `938894d04935cfa0430fdf904524166073e016afb1e37b20075e0a8b94c4d24a`

Require accepted A1 identity:

- `src/aiscc/scenarios/capture_runner.py`  `600de0a4b0e718f02ab2e1907b7be62b2c4a23756559fdf99cb4cd55fb80b3d2`
- `src/aiscc/scenarios/driver.py`  `9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`  `a137021608ac9cb5b4c328b6bb88fd0c22cb0d9afd9b1a22054ec5bdd32f68ff`

Mismatch:

```text
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

# 4. exact mutation authority

Only:

```text
MODIFY:
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Frozen byte-exact:

```text
src/aiscc/bootstrap.py
1718e596b20fd107af0cb80b6ad40e3626b7e26d8d45daa649ccf2d2ccf9fe38

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
src/aiscc/security/policy.py
src/aiscc/security/stockroom_policy.py
all migration files
```

If another path is required:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 5. verify the 1948 denial root cause before mutation

Read current source and verify all of these facts:

```text
integration test application clock:
2026-09-10T09:24:00Z

SecurityPolicy.issue_resource_grant:
TTL is calculated from supplied `now` when provided

SecurityPolicy.evaluate:
has no caller-supplied `now`

SecurityPolicy resource-grant validation during evaluate:
uses SecurityPolicy/native current wall clock

current A2 _issue_capability:
passes self._app.clock() to grant issuance

current A2 _issue_capability:
passes self._app.clock() to capability issuance
```

If any premise is false, do not apply the prescribed fix blindly.

Instead:

```text
ROOT_CAUSE_MISMATCH
→ STOP
```

and report the actual security denial cause.

# 6. security clock-domain correction

Current architecture contains two conceptually different time domains:

```text
application/durable business timestamps
security TTL/lease validity timestamps
```

Do not force the historical/deterministic application timestamp into a SecurityPolicy lifecycle whose evaluator uses the native wall clock.

Under the current P1-3 API, apply the smallest correction:

```text
StockroomCaptureOwnerAdapter._issue_capability:
- issue_resource_grant without `now=self._app.clock()`
- issue_capability without `now=self._app.clock()`

authorize_runtime NETWORK denied probe:
- issue_resource_grant without `now=self._app.clock()`
```

Equivalent source shape is allowed only if it produces the same invariant without modifying P1-3 source.

Keep application clock usage for existing durable evidence/Human/Judgment/application timestamps where those owners explicitly accept it.

Do not globally replace `self._app.clock()`.

Do not call `datetime.now()` in business/durable evidence code merely to make tests pass.

# 7. security semantics must remain unchanged

The correction must preserve:

```text
profile:
OWNER_SELF_DOGFOOD / p1-3-v2

action:
RUN_EXECUTION_SIDE_EFFECT

REPOSITORY:
Stockroom context required

FILESYSTEM:
Stockroom context required

NETWORK:
no context / grant must remain absent

requester/task/limit/budget/idempotency:
GRANTED

target-control:
NOT_APPLICABLE

SecurityPolicy.evaluate:
unchanged

StockroomOwnerRestriction:
unchanged
```

No fake `SecurityDecision`, `ResourceGrant`, or `Capability`.

# 8. regression pressure — keep historical application clock

Do not “fix” the integration test by replacing the historical application clock with live current time.

Keep:

```text
clock=lambda: datetime(2026, 9, 10, 9, 24, tzinfo=UTC)
```

or byte/semantic equivalent.

The test must prove that a historical/deterministic application clock does not accidentally pre-expire P1-3 security TTL objects.

After `RUNNING v2` require:

```text
seal_security_context:
ADMITTED

authorize_runtime:
ADMITTED

repository SecurityDecision:
ALLOW

filesystem SecurityDecision:
ALLOW

repository capability:
RUNNING v2 bound

filesystem capability:
RUNNING v2 bound

NETWORK grant issued:
False
```

# 9. preserve runtime-evidence binding candidate

Do not weaken the 1948 ToolOutputRef correction.

Require source/test retention of:

```text
execution submission verification
exactly one same-attempt AgentOutputRef
exactly one same-attempt ToolOutputRef
P1-5 verification
ToolOutputRef.content_hash == canonical_sha256(STOCKROOM_SUMMARY)
authentic ToolOutputRef producer provenance
missing/wrong/duplicate/stale output fail-closed
```

The pure provenance regression must remain.

# 10. migration gate

Reverify static migration head.

Expected current head:

```text
20260901_0008
```

No migration is authorized.

If schema change becomes necessary:

```text
MIGRATION_SCOPE_REQUIRED
→ STOP
```

# 11. full static gate

Run:

```text
Python compile:
src/aiscc/bootstrap.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/driver.py
tests/integration/scenarios/test_stockroom_capture_runner.py

Ruff:
same five Python paths

strict JSON:
config/evidence/stockroom-capture.v1.json
config/human/stockroom-capture.v1.json
config/judgment/stockroom-capture.v1.json

git diff --check
index verification
```

Require:

```text
compile 5/5 PASS
Ruff PASS
JSON 3/3 PASS
git diff --check PASS
index empty
```

Mandatory static failure:

```text
STATIC_CHECK_FAILURE
→ STOP
```

No same-turn second repair after this gate.

# 12. PostgreSQL prerequisite

After static PASS, use an existing compatible local PostgreSQL test environment if available.

Otherwise the same bounded Task-owned fallback remains authorized:

```text
image:
postgres:17.6-alpine

pull:
--pull=never

container:
aiscc-p2-3-a2-postgres

bind preference:
127.0.0.1:55442
then 55443
then 55444

storage:
disposable / tmpfs preferred
```

Do not pull, use remote DB, or remove unrelated containers.

Set DB credentials only in Task process environment and do not export them.

Run Alembic upgrade/current and require head:

```text
20260901_0008
```

# 13. mandatory A2 PostgreSQL module

Run once:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/scenarios/test_stockroom_capture_runner.py -ra
```

Expected current module test count:

```text
2 tests
```

Require:

```text
2 passed
0 failed
0 errors
0 skipped
```

If test inventory legitimately changed only by a narrow regression for the same two-file scope, report exact count and require all executed PASS.

Failure:

```text
TEST_FAILURE
→ STOP
```

No same-turn source repair or second test attempt.

# 14. mandatory A1/B3 regression

Only after A2 integration PASS:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_stockroom_capture_runner.py   tests/unit/scenarios/test_owner_composition.py   tests/integration/scenarios/test_stockroom_binding.py -ra
```

Expected accepted baseline:

```text
69 passed
```

Require exit 0 and no unexpected skip/failure/error.

# 15. direct-owner regressions

Then run this bounded direct-owner set against the same prerequisite as applicable:

```text
tests/integration/workflow/test_postgres_kernel.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/unit/security/test_stockroom_policy.py
```

Run only these modules.

Require exit 0.

Report exact pass/skip counts per module or aggregate with module mapping.

A PostgreSQL-backed module skipping due missing DB is not PASS.

# 16. security clock-domain verification artifact

Explicitly record:

```text
historical application clock:
retained

grant TTL clock:
SecurityPolicy native

evaluate validity clock:
SecurityPolicy native

capability TTL clock:
SecurityPolicy native

P1-3 source changed:
NO

repository authorization:
ALLOW

filesystem authorization:
ALLOW

network grant:
ABSENT
```

If source still mixes the historical app clock into this grant/evaluate/capability chain:

```text
CONTRACT_MISMATCH
→ STOP
```

# 17. contract review

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
SECURITY_TTL_CLOCK_DOMAIN_CONSISTENT
HISTORICAL_APP_CLOCK_REGRESSION_PASS
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
26 / 26 PASS
```

# 18. runtime ceiling

Allowed:

```text
PostgreSQL disposable integration
Alembic
real NONE->READY
real attempt creation
real READY->RUNNING
in-memory P1-3 security authorization
config registration/lookup
```

Forbidden:

```text
Stockroom materialization
Stockroom Docker/process
provider
tool dispatch
AgentExecutionService execution edge
network
real secret resolution
full runner.run()
actual S1-S4
HumanResult
terminal scenario Judgment
capture corpus
Replay
```

Fail-on-call counters remain required for forbidden runtime edges.

# 19. cleanup

If a Task-owned PostgreSQL container was created, remove only that exact container after evidence collection.

Verify absence.

No broad Docker cleanup.

# 20. final workspace

Before Task lifecycle:

```text
existing Git-visible:
15

current Cycle/Judgment:
2

total excluding active Task:
17 exact

index:
empty
```

Only two existing candidate files may have different bytes; path count stays unchanged.

Move active Task byte-identically to:

```text
.aiassistant/tasks/done/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-rework-1.md
```

Final:

```text
18 exact Git-visible paths
index empty
```

No other path.

# 21. no Git persistence

Do not run:

```text
git add
git commit
git push
```

Persistence is a later Browser decision.

# 22. export

Bundle:

```text
.aiassistant/reports/target/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-rework-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
MIGRATION_COMPATIBILITY.md
IMPLEMENTATION_MANIFEST.md
SECURITY_CLOCK_DOMAIN_VERIFICATION.md
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
all six A2 candidate paths
```

Expected:

```text
15 root docs
9 canonical/source copies
24 members total
```

`EXPORT_MANIFEST.md` covers all 23 non-self entries with size + SHA-256.

Require one top-level directory, CRC PASS, exact members, and folder/archive byte equality.

# 23. mandatory stop

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
ROOT_CAUSE_MISMATCH
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

# 24. success ceiling

Success:

```text
A2 production owner/bootstrap integration:
IMPLEMENTED_CANDIDATE / READY_FOR_BROWSER_COMMAND_CENTER_JUDGMENT

PostgreSQL owner/security proof:
EXECUTED_PASS

runtime-summary evidence binding:
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
