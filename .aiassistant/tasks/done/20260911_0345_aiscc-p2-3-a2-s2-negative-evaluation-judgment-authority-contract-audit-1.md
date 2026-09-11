# 작업지시서: P2-3 A2 S2 negative-evaluation → Judgment authority contract audit

## meta

- task_id: `20260911_0345_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-contract-audit-1`
- created_at: `2026-09-11T03:45:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_STATIC_AUDIT / P1_6_P1_7_CONTRACT_RECONCILIATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `A2 proof/cleanup authority → accepted P1-6/P1-7 semantic authority audit`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. fresh-session Python discipline

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

For repository import/static inspection requiring dependencies, verify and use exact:

```text
.venv\Scripts\python.exe
```

This Task does not run pytest or PostgreSQL.

# 1. inbound transport

Verify Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place TASK first at:

```text
.aiassistant/tasks/active/20260911_0345_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-contract-audit-1.md
```

Read it fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_0345_aiscc-p2-3-a2-executable-proof-admitted-s2-authority-audit-entry-1.cycle.md
SHA-256:
d8ab4adf3d97c43bcd717957cf821b11359c7568d458515506505a7bfc43c0f4

.aiassistant/reports/aiscc/20260911_0345_aiscc-p2-3-a2-workspace-reconciled-executable-proof-acceptance-judgment-1.md
SHA-256:
2c0f637a5995eac6ef3933d350cc592d74af98c3d12a502f4c3dd1b6e54c52ea
```

Bootstrap failure before canonical Task placement:

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

Expected Git-visible set excluding active Task is exact 42 paths:

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
- `.aiassistant/tasks/done/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-mismatch-judgment-1.md`
- `.aiassistant/tasks/done/20260910_2355_aiscc-p2-3-a2-prepared-owner-model-reconciliation-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_2355_aiscc-p2-3-a2-prepared-owner-audit-accepted-model-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2355_aiscc-p2-3-a2-prepared-owner-contract-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0105_aiscc-p2-3-a2-materialization-output-provenance-binding-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0105_aiscc-p2-3-a2-owner-model-static-failure-materialization-output-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0105_aiscc-p2-3-a2-owner-model-static-failure-materialization-output-binding-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-contract-test-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-test-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-test-failure-judgment-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/driver.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `config/evidence/stockroom-capture.v1.json`
- `config/human/stockroom-capture.v1.json`
- `config/judgment/stockroom-capture.v1.json`
- `tests/unit/scenarios/test_owner_composition.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `.aiassistant/tasks/done/20260911_0240_aiscc-p2-3-a2-static-command-transport-and-executable-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0240_aiscc-p2-3-a2-static-command-transport-failure-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0240_aiscc-p2-3-a2-static-command-transport-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0335_aiscc-p2-3-a2-pycompile-cache-cleanup-and-proof-admission-reverification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0335_aiscc-p2-3-a2-executable-proof-complete-workspace-residue-cleanup-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0335_aiscc-p2-3-a2-executable-proof-workspace-residue-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0345_aiscc-p2-3-a2-executable-proof-admitted-s2-authority-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0345_aiscc-p2-3-a2-workspace-reconciled-executable-proof-acceptance-judgment-1.md`

Any extra/missing path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Ignored target/export residue is non-blocking.

No reset/restore/stash/cleanup.

# 3. exact current candidate / predecessor identity

Require 0335 identities:

- `.aiassistant/tasks/done/20260911_0335_aiscc-p2-3-a2-pycompile-cache-cleanup-and-proof-admission-reverification-1.md`  `b13d50e21951be43a24700733bde50337d4204843a2f7b47d72df2d1c15be943`
- `.aiassistant/records/aiscc/cycles/20260911_0335_aiscc-p2-3-a2-executable-proof-complete-workspace-residue-cleanup-entry-1.cycle.md`  `5417303643829f0a8853e62ceac53b115a55f34fc831c12e13e6ecd4bc15df70`
- `.aiassistant/reports/aiscc/20260911_0335_aiscc-p2-3-a2-executable-proof-workspace-residue-judgment-1.md`  `3b15a6c0ffc0fc81faefbbd345249e010a00388fbe60da264b636f89829ef1f0`

Require 0240 identities:

- `.aiassistant/tasks/done/20260911_0240_aiscc-p2-3-a2-static-command-transport-and-executable-proof-retry-1.md`  `fe3f99839dd5eff9929f5ac9decea33005c067979fb5c2e76267bec71004c4b9`
- `.aiassistant/records/aiscc/cycles/20260911_0240_aiscc-p2-3-a2-static-command-transport-failure-proof-retry-entry-1.cycle.md`  `4ffd1e8fe6b2cc84d8ed095085e4e658caabfc2656c06cdac96479562f32a2f9`
- `.aiassistant/reports/aiscc/20260911_0240_aiscc-p2-3-a2-static-command-transport-failure-judgment-1.md`  `0098771b51375b373c53364df7e5f4e4a4db4159f5cb688110e7c671290a56c8`

Require current A2/B3 candidate exact:

- `src/aiscc/bootstrap.py`  `1718e596b20fd107af0cb80b6ad40e3626b7e26d8d45daa649ccf2d2ccf9fe38`
- `src/aiscc/scenarios/driver.py`  `c83792b0d84d07d584e4b5b32b1925a42a8be25cc0a872f19b92cffa2150a44c`
- `src/aiscc/scenarios/composition.py`  `2017a18175e0e227fe1514d3d9e85c7d0d64d391ec94649912d9749699b7edfc`
- `src/aiscc/scenarios/stockroom_production.py`  `742ffd8122507de941e93b9e721a97335afa9acf475ff8fd01d50fdacbf8137a`
- `config/evidence/stockroom-capture.v1.json`  `70d4dbf219d54abd57877b787d8ac16d0efbe05701e7fb8bf1f84282640b31e7`
- `config/human/stockroom-capture.v1.json`  `7ec43975b8d1f30ded987d05942753dadbd93197ad86da2701514a198e797bab`
- `config/judgment/stockroom-capture.v1.json`  `31f8d08c083218d1fcc47d5ba7a8d1c151a48bbf26ea3319ac9503a666179eef`
- `tests/unit/scenarios/test_owner_composition.py`  `68cf0561e482e1ded6f6bddaa8b91da1fea753b430527e27fe66bf7cf0cb4d12`
- `tests/integration/scenarios/test_stockroom_binding.py`  `063e2b65eb229b5849bc3df61294d72f3f656783ac1257a4dbcaa82bb2d70b34`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `016114dbd2ae1fe14476efec862948bf8e1682f8541cd518654dc5769f5dcf13`

Any mismatch:

```text
PREDECESSOR_OR_CANDIDATE_IDENTITY_MISMATCH
→ STOP
```

# 4. strict no-mutation audit ceiling

This Task may not modify:

```text
src/**
tests/**
config/**
migrations/**
CURRENT_STATE_SUMMARY
NEXT_ACTIONS
DECISION_REGISTER
rules
Git index/commit
```

No:

```text
pytest
PostgreSQL
Alembic upgrade
Docker
materializer
provider/tool
network
HumanResult
Judgment issuance
actual scenario execution
```

Read-only source/config/schema inspection and static imports/signature introspection are allowed.

# 5. mandatory canonical rule reads

Read fully:

```text
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/20260911_0345_aiscc-p2-3-a2-executable-proof-admitted-s2-authority-audit-entry-1.cycle.md
.aiassistant/reports/aiscc/20260911_0345_aiscc-p2-3-a2-workspace-reconciled-executable-proof-acceptance-judgment-1.md

.aiassistant/reports/aiscc/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-mismatch-judgment-1.md
.aiassistant/reports/aiscc/20260910_2355_aiscc-p2-3-a2-prepared-owner-contract-audit-final-acceptance-judgment-1.md
.aiassistant/reports/aiscc/20260911_0335_aiscc-p2-3-a2-executable-proof-workspace-residue-judgment-1.md
```

Do not execute historical Task instructions.

# 6. mandatory P1-6 source reads

Read fully and follow direct imports where required:

```text
src/aiscc/evidence/models.py
src/aiscc/evidence/repository.py
src/aiscc/evidence/set_evaluator.py
src/aiscc/evidence/attestation.py
src/aiscc/evidence/service.py
src/aiscc/evidence/requirements.py
src/aiscc/evidence/admission.py
src/aiscc/evidence/content.py

src/aiscc/persistence/models.py
```

Determine the exact canonical owner and persistence shape of:

```text
EvidenceSetEvaluation
EvidenceSetOutcome.UNSATISFIED
EvidenceSetAttestation / positive-set attestation equivalent
EvidenceCheckpoint
EvidenceRequirementSet
```

# 7. mandatory P1-7 Judgment source reads

Read fully and follow direct imports:

```text
src/aiscc/judgment/models.py
src/aiscc/judgment/authority.py

src/aiscc/workflow/kernel.py
src/aiscc/workflow/models.py
```

Also inspect exact transition/guard authority used by Judgment participants.

Determine current model/repository/API contract for:

```text
Judgment
JudgmentPolicy
PostgresJudgmentAuthority.issue
PostgresJudgmentAuthority.participant
evidence_attestation_ref
human_result_ref
current state/version verification
policy applicability
Judgment persistence row/schema
```

# 8. mandatory current A2 S2 source read

Read:

```text
src/aiscc/scenarios/stockroom_production.py
config/evidence/stockroom-capture.v1.json
config/judgment/stockroom-capture.v1.json
tests/integration/scenarios/test_stockroom_capture_runner.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/evidence/test_postgres_evidence_admission.py
```

Map the exact S2 chain:

```text
candidate omitted
→ EvidenceSetEvaluator.evaluate
→ EvidenceSetEvaluation.UNSATISFIED
→ adapter retained ref/handle
→ issue_judgment(HOLD_REWORK_REQUIRED, evidence_ref=None)
→ JudgmentAuthority.issue
→ Judgment participant
→ ADMISSION_PENDING -> REWORK_REQUIRED
```

# 9. P1-6 negative evaluation durability audit

Answer exactly:

```text
Is EvidenceSetEvaluation persisted durably?
Which table/model owns it?
What fields bind:
  work_run_id
  source_state
  state_version
  checkpoint_ref
  requirement-set identity
  outcome
  evaluated_at
  evaluation_id?

Is there a canonical serialized/typed ref for an evaluation?
If not, what exact existing identifier is durable?

Can PostgresEvidenceRepository load one evaluation by exact id/ref?
Can it prove current work_run/state_version/checkpoint applicability?

Can one evaluation be superseded or become stale?
What source/currentness rule applies?
```

Classify:

```text
DURABLE_TYPED_REF_ALREADY_AVAILABLE
DURABLE_ID_BUT_NO_TYPED_REF
NOT_DURABLE
AMBIGUOUS
```

# 10. positive attestation vs negative evaluation boundary

Prove from current P1-6 source that:

```text
SATISFIED attestation
!=
UNSATISFIED evaluation
```

Determine whether `EvidenceSetAttestation` or equivalent is intentionally only emitted for SATISFIED outcomes.

If yes, state explicitly:

```text
Do not manufacture an EvidenceSetAttestation for S2.
```

Determine the correct semantic artifact class for negative evidence-set truth.

# 11. P1-7 current Judgment evidence contract audit

Answer:

```text
Does Judgment currently have only evidence_attestation_ref?
Is that field semantically positive/admitted evidence only?
Can it legally reference a negative EvidenceSetEvaluation today?
Would doing so violate its schema/name/current tests?

Does PostgresJudgmentAuthority.issue independently resolve the evidence ref,
or merely persist a supplied opaque string?

Does participant() independently reverify the bound evidence authority/currentness?

For REWORK_REQUIRED policy, what evidence/guard facts are required?
```

Classify the current S2 state:

```text
CURRENT_API_ALREADY_SUFFICIENT
MODEL_REFERENCE_EXTENSION_REQUIRED
AUTHORITY_VERIFICATION_EXTENSION_REQUIRED
MODEL_AND_AUTHORITY_EXTENSION_REQUIRED
CANONICAL_CONFLICT
```

# 12. canonical typed binding design

If current API is insufficient, design the smallest truthful P1-7 binding.

Preferred semantic principle:

```text
Judgment may depend on different typed decision inputs.

Positive success:
EvidenceSetAttestation / admitted positive authority.

Negative rework:
EvidenceSetEvaluation with outcome UNSATISFIED.

These must remain distinct typed provenance.
```

Evaluate possible designs such as:

```text
evidence_evaluation_ref: str | None

or

typed JudgmentEvidenceBasisRef(
  kind = SATISFIED_ATTESTATION | UNSATISFIED_SET_EVALUATION,
  ref = ...
)
```

Choose exactly one architecture based on current source compatibility.

Do not introduce a generic untyped `reason_ref` merely to bypass authority checks.

# 13. P1-7 issue-time verification design

The chosen design must require P1-7 to independently verify, through P1-6 durable authority:

```text
evaluation exists
evaluation.work_run_id == request.work_run_id
evaluation.source_state == request.current_state
evaluation.state_version == request.expected_state_version
evaluation.checkpoint_ref matches policy-enrolled evidence checkpoint
evaluation.outcome == UNSATISFIED
evaluation belongs to current requirement-set identity
evaluation is not stale/superseded
target == REWORK_REQUIRED
Judgment policy explicitly allows this negative basis kind
```

Adapter-local `_handles` and reason text are not authority.

# 14. transition-time/currentness verification design

Determine whether issue-time verification alone is sufficient under current transaction/version semantics.

If the Judgment participant executes during transition, determine what it must reverify:

```text
Judgment still exists/current
negative evaluation ref still resolves
work_run/state/version unchanged
policy applicability unchanged
checkpoint/requirement identity unchanged
```

Do not duplicate P1-6 evaluation logic inside P1-7; P1-7 should consume authentic P1-6 authority.

# 15. S1/S4/non-S2 compatibility

The design must preserve:

```text
S1:
positive SATISFIED attestation -> ACCEPTED

S2:
negative UNSATISFIED evaluation -> REWORK_REQUIRED

S3:
no Judgment

S4:
Human gate / no Judgment before Human result
```

Determine whether any existing Judgment serialization or tests need compatibility handling.

No public runtime semantics may be widened.

# 16. persistence/migration audit

Inspect current migration head and persistence model **statically only**.

Expected accepted head:

```text
20260901_0008
```

Determine whether chosen architecture requires:

```text
NO_MIGRATION
NEW_NULLABLE_COLUMN
NEW_TYPED_BASIS_COLUMNS
NEW_TABLE
OTHER
```

If a migration is required, name the exact new migration responsibility and affected table/constraints/indexes.

Do not create a migration.

Do not assign a new revision ID in this audit unless repository policy requires the audit to name the next deterministic revision; otherwise mark revision `TO_BE_ISSUED_BY_IMPLEMENTATION_TASK`.

# 17. config impact audit

Determine whether this existing file must change:

```text
config/judgment/stockroom-capture.v1.json
```

Questions:

```text
Does the policy need an explicit allowed evidence-basis kind?
Does the checkpoint/requirement-set identity need to be enrolled into Judgment policy?
Can the current config remain sufficient if P1-7 resolves policy semantics elsewhere?
```

Classify exact config disposition:

```text
FROZEN
MODIFY_REQUIRED
VERSION_BUMP_REQUIRED
```

Do not edit it.

# 18. exact implementation allowlist

Produce one exact next mutation allowlist.

Candidate path families may include only if source proves they are required:

```text
src/aiscc/evidence/models.py
src/aiscc/evidence/repository.py
src/aiscc/evidence/set_evaluator.py

src/aiscc/judgment/models.py
src/aiscc/judgment/authority.py

src/aiscc/persistence/models.py
alembic/versions/<new exact migration if required>

src/aiscc/scenarios/stockroom_production.py
config/judgment/stockroom-capture.v1.json

tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

For every relevant path classify:

```text
MODIFY_REQUIRED
MIGRATION_CREATE_REQUIRED
TEST_MODIFY_REQUIRED
CONFIG_MODIFY_REQUIRED
FROZEN
NO_CHANGE_NEIGHBOR
```

No wildcard mutation scopes.

# 19. implementation cut decision

Choose exactly one:

```text
A. P1-6 durable negative-ref support + P1-7 typed Judgment binding in one atomic Task

B. P1-6 prerequisite Task first, then P1-7/A2 Task

C. P1-7-only implementation; P1-6 current API already sufficient

D. no code change; current contract already sufficient

E. canonical conflict requiring Human/design decision
```

Prefer the smallest authority-consistent cut, not the smallest line count.

Explain transaction/migration reasons.

# 20. regression plan

Design mandatory future proof covering at least:

```text
P1-6 UNSATISFIED evaluation durable round-trip

wrong work_run ref denied
wrong state/version denied
wrong checkpoint denied
SATISFIED/UNSATISFIED kind confusion denied
stale evaluation denied

P1-7 REWORK_REQUIRED Judgment accepts authentic current UNSATISFIED evaluation
P1-7 refuses adapter-local/fabricated evaluation ref
P1-7 refuses positive attestation in negative-basis slot
S1 positive ACCEPTED remains unchanged
S3 remains no-Judgment
S4 remains Human-required/no premature Judgment

A2 S2 flow reaches REWORK_REQUIRED through real owners
prepared-owner/materialized-output 134-PASS applicability preserved or rerun as required
```

Determine exact test modules.

# 21. conflict classification

For each gap classify:

```text
READY_CURRENT_SOURCE
MODEL_GAP
PERSISTENCE_GAP
AUTHORITY_VERIFICATION_GAP
CONFIG_GAP
TEST_GAP
MIGRATION_REQUIRED
CANONICAL_AUTHORITY_CONFLICT
```

A real `CANONICAL_AUTHORITY_CONFLICT` is a mandatory STOP after sufficient evidence.

Ordinary implementation gaps are audit success, not blockers.

# 22. final workspace

Before Task lifecycle:

```text
existing Git-visible:
40

current Cycle/Judgment:
2

excluding active Task:
42 exact

index:
empty
```

No source/test/config change.

Move active Task byte-identically to:

```text
.aiassistant/tasks/done/20260911_0345_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-contract-audit-1.md
```

Final expected:

```text
43 exact Git-visible paths
index empty
```

No other delta.

# 23. required export

Bundle:

```text
.aiassistant/reports/target/20260911_0345_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-contract-audit-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
S2_JUDGMENT_BINDING_AUDIT.md
P1_6_NEGATIVE_EVALUATION_AUTHORITY.md
P1_7_JUDGMENT_EVIDENCE_CONTRACT.md
NEGATIVE_BASIS_ARCHITECTURE.md
MIGRATION_IMPACT_AUDIT.md
CONFIG_IMPACT_AUDIT.md
IMPLEMENTATION_ALLOWLIST.md
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
12 root docs
3 canonical copies
15 members total
```

`EXPORT_MANIFEST.md` covers all 14 non-self entries with relative path, size, SHA-256.

Create adjacent verified ZIP.

# 24. mandatory stop

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

# 25. success ceiling

Success:

```text
S2 negative-evaluation Judgment authority audit:
COMPLETE / BROWSER_JUDGMENT_REQUIRED

exact architecture:
RESOLVED

migration/config impact:
RESOLVED

next implementation allowlist:
RESOLVED

A2 persistence:
NOT_AUTHORIZED

actual S1-S4:
NOT_STARTED
```
