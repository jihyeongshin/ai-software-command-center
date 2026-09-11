# 작업지시서: P2-3 A2 prepared-owner binding contract reconciliation audit

## meta

- task_id: `20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-audit-1`
- created_at: `2026-09-10T22:20:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_STATIC_AUDIT / CONTRACT_RECONCILIATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `A2 production implementation → accepted B3/A1 prepared-owner authority reconciliation`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. fresh-session Python rule

Do not assume bare:

```text
python
python3
py
```

is valid on PATH.

Do not run bare `python` as a probe.

Known interpreter candidate:

```text
C:\Users\oracl\AppData\Roaming\uv\python\cpython-3.12.14-windows-x86_64-none\python.exe
```

Use exact executable paths only.

For repository import/static probes requiring dependencies, verify and use:

```text
.venv\Scripts\python.exe
```

This Task does not run pytest.

# 1. inbound transport

Verify Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place TASK first at:

```text
.aiassistant/tasks/active/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-audit-1.md
```

Read it fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-entry-1.cycle.md
SHA-256:
fd54dd082ad71f5bf7c130efa015ec944f35bfbd6203dc96ccc6dab8aaf959cb

.aiassistant/reports/aiscc/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-mismatch-judgment-1.md
SHA-256:
c301beb57ebb85706b22df0a144225e8b608160e5cd53a788a162b8029aa48e3
```

Bootstrap failure before canonical Task placement:

```text
STOP
no report/export
no substantive project mutation
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

Expected Git-visible set excluding active Task is exact 20 paths:

- `.aiassistant/tasks/done/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1824_aiscc-p2-3-a2-feasibility-accepted-production-integration-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1824_aiscc-p2-3-a2-feasibility-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1948_aiscc-p2-3-a2-production-integration-static-and-runtime-evidence-binding-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-judgment-1.md`
- `.aiassistant/tasks/done/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_2215_aiscc-p2-3-a2-security-clock-domain-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-judgment-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `config/evidence/stockroom-capture.v1.json`
- `config/human/stockroom-capture.v1.json`
- `config/judgment/stockroom-capture.v1.json`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `.aiassistant/records/aiscc/cycles/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-mismatch-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Ignored target/export residue may remain non-blocking.

No cleanup/reset/restore/stash.

# 3. exact pending identity

Require all predecessor governance exact:

- `.aiassistant/tasks/done/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md`  `c8f6615b9ce5943e1bee43046d50dd2dac4efba99a96179043177530f3a96ce4`
- `.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md`  `0e6b3a12767fc3d5830726e1327d8e0d6f097271aa7aedd4157a4b86a566a782`
- `.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md`  `4df00fc71ff6603cb0703077c10c5460d3db2bdb6ec772a2b3fbd8b5983ed476`
- `.aiassistant/tasks/done/20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1.md`  `13b3561669bfa5c9343bc0339f52bb77b06eab56e1c97369f6a4973766178997`
- `.aiassistant/records/aiscc/cycles/20260910_1824_aiscc-p2-3-a2-feasibility-accepted-production-integration-entry-1.cycle.md`  `a02818022b2c694ad2644c2222e127de87c38f360b65fc33937c42af2cdb9846`
- `.aiassistant/reports/aiscc/20260910_1824_aiscc-p2-3-a2-feasibility-audit-final-acceptance-judgment-1.md`  `743103b7e8e22c7833bd555ff8ceedd0e0f34e0ab4994f077006864fbf172a85`
- `.aiassistant/tasks/done/20260910_1948_aiscc-p2-3-a2-production-integration-static-and-runtime-evidence-binding-rework-1.md`  `2592d9fc0635c4fc61b41929d78bab59b9de19c496fe8d98334bb14e12148e5b`
- `.aiassistant/records/aiscc/cycles/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-rework-entry-1.cycle.md`  `2206f489bca4de6f1da211beeba932e0125da05dceeb329bef9fe19938770dd1`
- `.aiassistant/reports/aiscc/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-judgment-1.md`  `534a863b8df861cd96091e7678b58ed12b35eebd6272ed867ab55a1d240e58ea`
- `.aiassistant/tasks/done/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-rework-1.md`  `50f35f57def86ab6535befafdb7022b7a0806f60f52d67a0fc9697a883834482`
- `.aiassistant/records/aiscc/cycles/20260910_2215_aiscc-p2-3-a2-security-clock-domain-rework-entry-1.cycle.md`  `dde57e4dae071826ca377b9cc32a4a34cf25dd3d368b897d695156e600022eec`
- `.aiassistant/reports/aiscc/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-judgment-1.md`  `ea62c1e759018fcc21b32e0760915c38f8c1afe092ecb550025a9021ac2ce201`

Require exact current A2 candidate:

- `src/aiscc/bootstrap.py`  `1718e596b20fd107af0cb80b6ad40e3626b7e26d8d45daa649ccf2d2ccf9fe38`
- `src/aiscc/scenarios/stockroom_production.py`  `03e3f68709b04304f1bb1e33932b97da0df6ccedfad644d62eb545fe71c9ef96`
- `config/evidence/stockroom-capture.v1.json`  `70d4dbf219d54abd57877b787d8ac16d0efbe05701e7fb8bf1f84282640b31e7`
- `config/human/stockroom-capture.v1.json`  `7ec43975b8d1f30ded987d05942753dadbd93197ad86da2701514a198e797bab`
- `config/judgment/stockroom-capture.v1.json`  `31f8d08c083218d1fcc47d5ba7a8d1c151a48bbf26ea3319ac9503a666179eef`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `938894d04935cfa0430fdf904524166073e016afb1e37b20075e0a8b94c4d24a`

Require accepted A1 committed identity:

- `src/aiscc/scenarios/capture_runner.py`  `600de0a4b0e718f02ab2e1907b7be62b2c4a23756559fdf99cb4cd55fb80b3d2`
- `src/aiscc/scenarios/driver.py`  `9871847ec0a236ef61c91518ff95764f3c2138e3854c25a4c8cab4f028503ce6`
- `tests/unit/scenarios/test_stockroom_capture_runner.py`  `a137021608ac9cb5b4c328b6bb88fd0c22cb0d9afd9b1a22054ec5bdd32f68ff`

Any mismatch:

```text
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

# 4. strict no-mutation authority

This Task may not modify:

```text
source
tests
config
migrations
state records
decision register
rules
Git index
Git commits
runtime resources
```

No pytest, PostgreSQL, Docker, materialization, provider/tool, filesystem runtime allocation, or network.

Read-only source inspection, AST/signature inspection, and byte/hash checks are allowed.

# 5. mandatory canonical reads

Read fully:

```text
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/bootstrap.py

src/aiscc/runtime/stockroom_materializer.py
src/aiscc/providers/service.py
src/aiscc/workflow/kernel.py
src/aiscc/security/policy.py

tests/unit/scenarios/test_owner_composition.py
tests/integration/scenarios/test_stockroom_binding.py
tests/unit/scenarios/test_stockroom_capture_runner.py
tests/integration/scenarios/test_stockroom_capture_runner.py

.aiassistant/records/aiscc/cycles/20260910_0102_aiscc-p2-3-phase1b-b3-final-acceptance-persistence-1.cycle.md
.aiassistant/reports/aiscc/20260910_1008_aiscc-p2-3-stockroom-settlement-persistence-final-acceptance-judgment-1.md
.aiassistant/tasks/done/20260910_1008_aiscc-p2-3-actual-capture-runtime-entry-prerequisite-audit-retry-1.md
.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md
.aiassistant/reports/aiscc/20260910_1824_aiscc-p2-3-a2-feasibility-audit-final-acceptance-judgment-1.md
.aiassistant/reports/aiscc/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-mismatch-judgment-1.md
```

If a historical filename differs only because of exact persisted naming, locate the exact canonical B3 final-acceptance Cycle by title/date/commit and report its actual path.

Do not execute historical Task instructions.

# 6. establish B3 prepared-owner semantics

From current accepted source and tests, answer with exact citations/line ranges:

```text
What does StockroomOwnerDependencies represent?

Does PreparedStockroomDriver bind the exact supplied owner object bundle?

Does prepare_stockroom_driver preserve owner object identity?

Which B3 tests assert object identity rather than only owner type?

Are AgentExecutionService and StockroomMaterializer represented as concrete instances,
factories,
ports,
or descriptors?
```

Explicitly inspect:

```text
StockroomOwnerDependencies
PreparedStockroomDriver
prepare_stockroom_driver
StockroomOwnerPreparation.prepare
bind_stockroom_owner_dependencies
```

Classify the canonical meaning:

```text
EXACT_INSTANCE_BINDING
DERIVATION_ROOT_BINDING
TYPE_ONLY_BINDING
AMBIGUOUS
```

Do not infer `TYPE_ONLY_BINDING` merely because A1 runner ignores the field.

# 7. current A2 owner identity matrix

Create a path/object-level identity matrix for every field of `StockroomOwnerDependencies`.

For each field report:

```text
prepared owner field
object constructed in prepare_capture
actual operation(s)
actual object used by StockroomCaptureOwnerAdapter
same object identity YES/NO/NOT_APPLICABLE
late replacement/derivation point
authoritative ref/handle source
```

Mandatory fields:

```text
workflow_kernel
agent_execution_service
evidence_admission_service
human_gate_owner
judgment_owner
workspace_owner
materializer
security_policy
stockroom_owner_restriction
```

For the two suspected mismatches, prove actual source identity:

```text
prepared.owners.materializer
vs
StockroomMaterializer created inside materialize()

prepared.owners.agent_execution_service
vs
AgentExecutionService created by _build_execution_service()
```

Also inspect mutations of:

```text
StockroomPreparedCapture.materializer
StockroomPreparedCapture.agent_execution_service
```

and whether those mutations update or supersede immutable `PreparedStockroomDriver.owners`.

# 8. runner consumption audit

Determine exactly which owner authority the accepted A1 runner actually consumes.

Answer:

```text
Does StockroomCaptureRunner call prepared.owners directly?
Does _validate_prepared validate prepared.owners?
Does StockroomCaptureRunner instead use a separately injected StockroomCaptureOwnerPort?
Can the port perform all operations while prepared.owners is stale/different?
```

Do not claim exploitability; classify only contract relevance.

# 9. late-bound owner feasibility

For `StockroomMaterializer` inspect constructor and authorization contract.

Determine whether the exact instance can be safely constructed before RUNNING/security admission and later receive the authentic per-attempt `MaterializationAuthority` **without private-field mutation or weakening B1**.

For `AgentExecutionService` inspect constructor/configuration contract.

Determine whether the exact instance can be safely constructed before materialization and later receive the authentic `DockerRunSpec`, `ToolRegistry`, dispatcher and attempt-scoped runtime bindings **without private-field mutation, service replacement, or weakening P1-5**.

For each classify:

```text
EXACT_INSTANCE_REUSE_SUPPORTED
EXACT_INSTANCE_REUSE_NOT_SUPPORTED
SUPPORTED_VIA_EXISTING_PUBLIC_FACTORY_OR_BINDING
UNKNOWN
```

Private attribute mutation does not count as supported.

Subclass/proxy tricks created only to defeat identity checks do not count unless an accepted canonical owner contract explicitly authorizes them.

# 10. derivation-authority audit

If current A2 intends the prepared owners to be derivation roots rather than actual side-effect owner instances, identify the canonical source that proves:

```text
a prepared AgentExecutionService may authorize creation of a different AgentExecutionService

a prepared StockroomMaterializer may authorize creation of a different StockroomMaterializer

the derived object identity is cryptographically/configurationally bound to the prepared request

the runner records enough provenance to distinguish prepared owner from derived runtime owner
```

If no such authority exists, report:

```text
DERIVATION_AUTHORITY_NOT_ESTABLISHED
```

Do not treat “constructed from the same application” as sufficient by itself.

# 11. no-owner-swapping invariant

Evaluate this proposed invariant against canonical source:

```text
For every side-effect owner represented as an exact concrete owner in PreparedStockroomDriver.owners,
the runtime operation must either:

A. execute through that exact owner instance,

or

B. execute through a separately modeled late-bound owner/factory authority
   whose identity/provenance is part of the immutable prepared binding.
```

Classify:

```text
CANONICAL_REQUIRED
COMPATIBLE_STRENGTHENING
CONFLICTS_WITH_ACCEPTED_BASELINE
NOT_SUPPORTED
```

Give source evidence.

# 12. remediation architecture

Choose exactly one result:

```text
NO_CONTRACT_MISMATCH
EXACT_BOUND_OWNER_REUSE_POSSIBLE_WITHIN_A2
PREPARED_OWNER_MODEL_RECONCILIATION_REQUIRED
CANONICAL_AUTHORITY_CONFLICT
```

If `NO_CONTRACT_MISMATCH`, prove the exact current authority that makes the different instances valid.

If `EXACT_BOUND_OWNER_REUSE_POSSIBLE_WITHIN_A2`, specify the exact public APIs and source/test paths needed; no private mutation.

If `PREPARED_OWNER_MODEL_RECONCILIATION_REQUIRED`, propose the smallest truthful model.

Preferred principles:

```text
do not keep concrete placeholder side-effect owners merely for type satisfaction
do not weaken explicit owner binding
do not make PreparedStockroomDriver ownership ornamental
distinguish stable application owners from genuinely late-bound attempt owners/factories
bind late-bound authority to request/config/run/attempt identity
preserve A1 runner fail-closed semantics
```

Do not implement in this Task.

# 13. exact future mutation allowlist

Produce one exact next-Task allowlist.

Possible paths may include only when justified:

```text
src/aiscc/scenarios/driver.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/stockroom_production.py
tests/unit/scenarios/test_owner_composition.py
tests/integration/scenarios/test_stockroom_binding.py
tests/unit/scenarios/test_stockroom_capture_runner.py
tests/integration/scenarios/test_stockroom_capture_runner.py
src/aiscc/bootstrap.py
```

The three Stockroom A2 config files should remain frozen unless the audit proves the owner model changes their semantic identity.

Do not include unrelated P1-3/P1-5/P1-6/P1-7 source without a concrete canonical reason.

No wildcard allowlist.

For every path classify:

```text
MODIFY_REQUIRED
TEST_REWORK_REQUIRED
NO_CHANGE_NEIGHBOR
FROZEN
```

# 14. required regression plan

Design the minimum next proof that would close the mismatch.

It must include identity assertions for all concrete prepared owners or the exact replacement model.

At minimum prove:

```text
prepared owner binding is not type-only
all stable owner identities match production application owners
late-bound side-effect owner authority is explicitly represented
no placeholder owner can be swapped for an unrelated instance
request/config/run/attempt fingerprints survive the binding
A1 operation/snapshot fail-closed behavior remains unchanged
A2 PostgreSQL NONE->READY->RUNNING + security prefix still passes
runtime ToolOutputRef binding still passes
no Stockroom materialization/provider/tool/process actual execution in this rework proof
```

If actual materialization is required merely to prove owner identity, explain why and classify as a later runtime prerequisite instead of silently expanding.

# 15. secondary S2 Judgment binding check

Without broadening mutation scope, inspect the current S2 path:

```text
EvidenceSetEvaluation UNSATISFIED
→ issue_judgment(HOLD_REWORK_REQUIRED, evidence_ref=None)
→ reason_code contains evaluation_id
```

Determine whether current P1-7 Judgment authority independently binds the rework Judgment to an authentic current P1-6 unsatisfied evaluation, or whether that truth exists only in adapter-local `_handles`/reason text.

Classify:

```text
P1_7_BINDING_SUFFICIENT
ADAPTER_LOCAL_BINDING_ONLY
NOT_APPLICABLE
UNKNOWN
```

If `ADAPTER_LOCAL_BINDING_ONLY`, include it as a separately named A2 rework item and exact path impact.

Do not invent a new evidence attestation for an unsatisfied set.

# 16. strict no-runtime ceiling

Do not run:

```text
pytest
PostgreSQL
Alembic upgrade
Docker
materializer
provider/tool
AgentExecutionService.execute
network
HumanResult
Judgment issuance
actual S1-S4
Git add/commit/push
```

No source/config/test edits.

# 17. final workspace

Before Task lifecycle:

```text
pending prior governance + A2 candidate:
18

current Cycle/Judgment:
2

total excluding active Task:
20 exact

index:
empty
```

Move active Task byte-identically to:

```text
.aiassistant/tasks/done/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-audit-1.md
```

Final:

```text
21 exact Git-visible paths
index empty
```

No other delta.

# 18. required export bundle

Folder:

```text
.aiassistant/reports/target/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-audit-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
PREPARED_OWNER_CONTRACT_AUDIT.md
OWNER_IDENTITY_MATRIX.md
RUNNER_CONSUMPTION_AUDIT.md
LATE_BOUND_OWNER_FEASIBILITY.md
DERIVATION_AUTHORITY_AUDIT.md
S2_JUDGMENT_BINDING_AUDIT.md
REMEDIATION_ARCHITECTURE.md
REWORK_ALLOWLIST.md
REGRESSION_PLAN.md
```

Also include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task
```

Expected:

```text
13 root docs
3 canonical copies
16 members total
```

`EXPORT_MANIFEST.md` covers all 15 non-self members with relative path, byte size and SHA-256.

Create adjacent verified ZIP.

# 19. mandatory stop

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
CANONICAL_AUTHORITY_CONFLICT
UNEXPECTED_WORKSPACE_DELTA
ZIP_EXPORT_FAILED
```

# 20. success ceiling

Success:

```text
PREPARED_OWNER_BINDING_AUDIT:
COMPLETE / BROWSER_JUDGMENT_REQUIRED

A2 implementation:
NOT_PERSISTED

exact rework architecture/allowlist:
RESOLVED

Stockroom runtime prerequisites:
NOT_VERIFIED

actual S1-S4:
NOT_STARTED
```
