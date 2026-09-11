# 작업지시서: P2-3 A2 S2 negative-evaluation → Judgment authority implementation

## meta

- task_id: `20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-implementation-1`
- created_at: `2026-09-11T09:20:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `IMPLEMENTATION / P1_6_P1_7_AUTHORITY / POSTGRESQL_INTEGRATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `P1-6/P1-7 read-only audit → accepted evidence/Judgment authority source implementation`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. fresh-session Python discipline

Do not assume bare:

```text
python
python3
py
```

is valid on PATH.

Do not run bare `python` as an interpreter probe.

Known interpreter candidate:

```text
C:\Users\oracl\AppData\Roaming\uv\python\cpython-3.12.14-windows-x86_64-none\python.exe
```

For repository imports/tests, verify and use exact:

```text
.venv\Scripts\python.exe
```

Use exact executable paths only.

# 1. inbound transport

Verify Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place TASK first at:

```text
.aiassistant/tasks/active/20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-implementation-1.md
```

Read it fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_0920_aiscc-p2-3-a2-s2-authority-audit-accepted-implementation-entry-1.cycle.md
SHA-256:
a769f39a3b1a7c1596d4288b5f6371c7bcebff9101fe8b176033ef269e94d717

.aiassistant/reports/aiscc/20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-authority-audit-final-acceptance-judgment-1.md
SHA-256:
9cc84eb27055924043b1ac9fad8357b14d153a8cfbd842636625b082957bb9ba
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

Expected Git-visible set excluding active Task is exact 45 paths:

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
- `.aiassistant/tasks/done/20260911_0240_aiscc-p2-3-a2-static-command-transport-and-executable-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0240_aiscc-p2-3-a2-static-command-transport-failure-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0240_aiscc-p2-3-a2-static-command-transport-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0335_aiscc-p2-3-a2-pycompile-cache-cleanup-and-proof-admission-reverification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0335_aiscc-p2-3-a2-executable-proof-complete-workspace-residue-cleanup-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0335_aiscc-p2-3-a2-executable-proof-workspace-residue-judgment-1.md`
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
- `.aiassistant/tasks/done/20260911_0345_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0345_aiscc-p2-3-a2-executable-proof-admitted-s2-authority-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0345_aiscc-p2-3-a2-workspace-reconciled-executable-proof-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0920_aiscc-p2-3-a2-s2-authority-audit-accepted-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-authority-audit-final-acceptance-judgment-1.md`

Any extra/missing:

```text
DIRTY_WORKSPACE_MIXED
→ STOP
```

Ignored target/export residue is non-blocking.

No reset/restore/stash/broad cleanup.

# 3. exact accepted predecessor identity

Require exact 0345 provenance:

- `.aiassistant/tasks/done/20260911_0345_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-contract-audit-1.md`  `2f778de4db9cc1f31b924b7570002b2ab87283e742cdf7f970c87b529cb2769a`
- `.aiassistant/records/aiscc/cycles/20260911_0345_aiscc-p2-3-a2-executable-proof-admitted-s2-authority-audit-entry-1.cycle.md`  `d8ab4adf3d97c43bcd717957cf821b11359c7568d458515506505a7bfc43c0f4`
- `.aiassistant/reports/aiscc/20260911_0345_aiscc-p2-3-a2-workspace-reconciled-executable-proof-acceptance-judgment-1.md`  `2c0f637a5995eac6ef3933d350cc592d74af98c3d12a502f4c3dd1b6e54c52ea`

Require exact current accepted-candidate identities:

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

# 4. exact mutation allowlist

Only these nine paths may change:

- `src/aiscc/evidence/models.py`
- `src/aiscc/evidence/repository.py`
- `src/aiscc/judgment/models.py`
- `src/aiscc/judgment/authority.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `config/judgment/stockroom-capture.v2.json`
- `tests/integration/evidence/test_postgres_evidence_admission.py`
- `tests/integration/human/test_postgres_human_gate_judgment.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`

Classification:

```text
MODIFY:
src/aiscc/evidence/models.py
src/aiscc/evidence/repository.py
src/aiscc/judgment/models.py
src/aiscc/judgment/authority.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/scenarios/test_stockroom_capture_runner.py

CREATE:
config/judgment/stockroom-capture.v2.json
```

Frozen:

```text
config/judgment/stockroom-capture.v1.json
config/evidence/stockroom-capture.v1.json
config/human/stockroom-capture.v1.json

src/aiscc/evidence/set_evaluator.py
src/aiscc/evidence/attestation.py
src/aiscc/evidence/requirements.py
src/aiscc/persistence/models.py

src/aiscc/workflow/**
src/aiscc/security/**
src/aiscc/providers/**
src/aiscc/runtime/**

src/aiscc/scenarios/driver.py
src/aiscc/scenarios/composition.py
src/aiscc/scenarios/capture_runner.py

tests/unit/scenarios/test_owner_composition.py
tests/integration/scenarios/test_stockroom_binding.py
tests/unit/scenarios/test_stockroom_capture_runner.py

all migrations
```

If another path is necessary:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP
```

# 5. migration pre-mutation gate

Statically verify the repository migration graph.

Expected accepted head:

```text
20260901_0008
```

Confirm current persistence models still provide:

```text
EvidenceSetEvaluationRow
evaluation_id primary key
full evaluation payload/currentness inputs

Judgment JSON/JSONB persistence capable of additive optional fields
```

If the chosen implementation cannot persist/round-trip the new Judgment contract without schema change:

```text
MIGRATION_SCOPE_REQUIRED
→ STOP
```

Do not create a migration.

# 6. P1-6 canonical negative evaluation ref

In:

```text
src/aiscc/evidence/models.py
```

add a P1-6-owned immutable typed ref for `EvidenceSetEvaluation`.

Semantic contract:

```text
type:
EvidenceSetEvaluationRef or equivalent exact P1-6 name

contains:
evaluation contract/version
evaluation_id

canonical serialization:
strict, deterministic, round-trippable

recommended audited shape:
p1-6-set-evaluation:<evaluation-version>:<evaluation_id>
```

If the existing P1-6 ref grammar has a stricter canonical pattern, conform to that exact existing pattern and document the resolved serialization.

Parser must reject:

```text
wrong prefix
unknown version
empty/malformed evaluation id
extra segments
non-canonical serialization
positive attestation ref supplied as evaluation ref
adapter-local `p1-6-evidence-set-evaluation:*` pseudo-ref
```

No generic untyped reason/ref.

# 7. P1-6 evaluation reconstruction

In:

```text
src/aiscc/evidence/repository.py
```

add the smallest exact row-to-domain reconstruction and ref resolver needed for P1-7.

The resolver must:

```text
accept the caller's current AsyncSession / transaction
parse the canonical P1-6 evaluation ref
load exact EvidenceSetEvaluationRow
reconstruct the full EvidenceSetEvaluation domain value
verify row/payload equality and deterministic evaluation_id
verify evaluation authority revision/version contract
```

It must not open a separate transaction when P1-7 supplies the transition transaction.

# 8. P1-6 currentness authority

The resolver must be able to prove that the referenced evaluation is the **current applicable evaluation**, not merely that a historical row exists.

For an expected S2 negative basis require:

```text
work_run_id exact
source_state exact
state_version exact
checkpoint_ref exact
requirement_set_ref exact
outcome == UNSATISFIED
evaluation version supported
evidence authority compatible/current
```

Then recompute the current effective set from existing P1-6 authorities using the existing pure evaluation logic and current durable inputs.

Currentness comparison must cover the canonical set snapshot/fingerprint inputs already owned by P1-6, including as applicable:

```text
active requirement-set identity/version
checkpoint applicability
requirement/root identities
effective admissions
full/root/subset/admitted fingerprints
authority revision
recomputed outcome
```

Do not write a new evaluation row merely to resolve currentness.

A formerly valid evaluation that no longer equals the current effective evaluation must be rejected as stale.

Do not copy P1-6 evaluation semantics into P1-7.

# 9. positive/negative artifact separation

Preserve:

```text
EvidenceSetSatisfactionAttestation:
SATISFIED only

EvidenceSetEvaluation:
may be UNSATISFIED
```

For S2:

```text
no satisfaction attestation
no positive attestation ref
no fake admitted evidence ref
```

The canonical `EvidenceSetEvaluationRef` is the negative decision authority.

# 10. P1-7 Judgment basis model

In:

```text
src/aiscc/judgment/models.py
```

add an explicit evidence-basis discriminator.

Required semantic values:

```text
SATISFIED_ATTESTATION
UNSATISFIED_SET_EVALUATION
```

Add a dedicated negative evaluation ref and the minimum verified metadata required by the current Judgment persistence/fingerprint contract.

At minimum the new Judgment representation must preserve:

```text
evidence_basis_kind
evidence_evaluation_ref
evidence_evaluation_authority_revision or equivalent verified authority marker
evidence checkpoint ref
evidence requirement-set ref
```

Keep existing:

```text
evidence_attestation_ref
```

for the positive path.

# 11. model validation invariant

Where a policy requires evidence, the Judgment model/request must reject ambiguous basis combinations.

Required:

```text
SATISFIED_ATTESTATION:
positive attestation ref required
negative evaluation ref absent

UNSATISFIED_SET_EVALUATION:
negative evaluation ref required
positive attestation ref absent
```

Reject:

```text
both refs
neither ref when policy requires one
basis kind/ref kind mismatch
unknown basis kind
negative basis for incompatible target
positive basis in negative-only slot
```

Do not broaden this into a generic arbitrary evidence basis.

# 12. legacy serialization/fingerprint compatibility

Historical v1 Judgment policies and Judgment rows must remain valid.

For legacy objects whose new optional keys are absent:

```text
deserialize as legacy/None state
retain old semantic fingerprint
do not inject new null keys into canonical fingerprint material if that would change old identity
```

Add explicit regression proving a pre-change legacy Judgment/policy fixture retains its accepted canonical fingerprint/serialization behavior.

New v2 policy/Judgment objects include the new basis metadata in their identity.

# 13. P1-7 policy model and v2 enrollment

Create:

```text
config/judgment/stockroom-capture.v2.json
```

Keep v1 byte-exact.

The v2 Stockroom policy must explicitly enroll:

```text
S1 / ACCEPTED:
allowed evidence basis = SATISFIED_ATTESTATION

S2 / REWORK_REQUIRED:
allowed evidence basis = UNSATISFIED_SET_EVALUATION

P1-6 checkpoint ref:
exact enrolled value

P1-6 requirement-set ref:
exact enrolled value
```

Use the current config loader/schema conventions.

Unknown/missing keys fail closed.

Do not put a Human selector, secret, runtime path, or environment-specific value in config.

# 14. P1-7 issue-time negative verification

In:

```text
src/aiscc/judgment/authority.py
```

extend `PostgresJudgmentAuthority` only as needed to consume the P1-6 resolver.

For a v2 S2 REWORK_REQUIRED request, before persisting Judgment, independently verify:

```text
canonical evaluation ref parses
row exists
same work_run
same observed/current source state
same expected state_version
same policy-enrolled checkpoint
same policy-enrolled requirement set
outcome == UNSATISFIED
evaluation is current, not stale
policy allows UNSATISFIED_SET_EVALUATION
requested/issued target == REWORK_REQUIRED
```

Adapter-local handles/reason strings are not consulted as authority.

A fabricated but syntactically valid ref must fail closed.

# 15. P1-7 transition-participant reverification

Issue-time verification alone is insufficient.

Inside the existing Judgment transition participant:

```text
after the current WorkRun lock is established
using the same transaction/session
```

reverify:

```text
stored Judgment basis kind/ref
current WorkRun/state/version
current Judgment/policy applicability
checkpoint/requirement-set enrollment
P1-6 negative evaluation currentness
UNSATISFIED outcome
```

Any mismatch:

```text
participant preparation DENIED
no state transition
```

Do not create a second P1-6 evaluator implementation in Judgment.

# 16. constructor/backward compatibility

Do not break unrelated existing P1-7 construction.

If `PostgresJudgmentAuthority` requires a new P1-6 resolver dependency:

```text
legacy/v1 construction:
may omit it only when no enrolled policy requires negative evaluation basis

v2 negative policy:
must fail closed if resolver dependency is unavailable
```

The A2 production graph must inject the real P1-6 resolver/authority.

Do not use a global singleton/service locator.

# 17. A2 Stockroom handoff

In:

```text
src/aiscc/scenarios/stockroom_production.py
```

replace the S2 adapter-local pseudo-ref authority path.

After authentic:

```text
EvidenceSetEvaluation(outcome=UNSATISFIED)
```

obtain/retain its canonical P1-6 `EvidenceSetEvaluationRef`.

When issuing S2 Judgment pass:

```text
basis kind:
UNSATISFIED_SET_EVALUATION

evidence_evaluation_ref:
authentic canonical P1-6 ref

evidence_attestation_ref:
None
```

Switch Stockroom production Judgment policy enrollment from v1 to v2.

Do not change evidence or Human config versions.

# 18. S1/S3/S4 preservation

Require:

```text
S1:
SATISFIED attestation
→ positive P1-7 basis
→ ACCEPTED semantics unchanged

S2:
UNSATISFIED evaluation ref
→ negative P1-7 basis
→ REWORK_REQUIRED

S3:
no Judgment

S4:
Human-required
no premature Judgment before Human result
```

Do not widen public modes or actual runtime authority.

# 19. modified P1-6 integration tests

In:

```text
tests/integration/evidence/test_postgres_evidence_admission.py
```

add real PostgreSQL proof for:

```text
UNSATISFIED evaluation persisted
canonical ref round-trip exact
resolver returns authentic reconstructed evaluation
wrong WorkRun denied
wrong state denied
wrong state_version denied
wrong checkpoint denied
wrong requirement set denied
SATISFIED evaluation denied when UNSATISFIED required
positive attestation ref denied as negative ref
malformed/unknown-version ref denied
adapter-local pseudo-ref denied
previously authentic evaluation denied after current evidence/requirements make it stale
staleness case not detectable by authority revision alone is still denied
```

Do not use direct SQL state fabrication.

# 20. modified P1-7 integration tests

In:

```text
tests/integration/human/test_postgres_human_gate_judgment.py
```

prove with real PostgreSQL owners:

```text
authentic current UNSATISFIED ref issues REWORK_REQUIRED Judgment
negative basis persists/round-trips
participant re-verifies and prepares valid transition
fabricated ref denied
wrong WorkRun/state/version denied
wrong checkpoint/requirement set denied
stale evaluation denied
positive attestation in negative slot denied
both positive+negative refs denied
negative basis for incompatible target/policy denied
transition-time staleness after issue denies participant
legacy v1 positive path still works
legacy fingerprint/serialization compatibility retained
Human-gate behavior unchanged
```

# 21. modified A2 scenario integration

In:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py
```

extend the bounded production-style scenario proof.

Required:

```text
S1 positive basis remains valid

S2:
candidate omission
→ durable P1-6 UNSATISFIED evaluation
→ canonical P1-6 evaluation ref
→ P1-7 Judgment stores that ref
→ real participant accepts current ref
→ REWORK_REQUIRED through real owners

S3:
no Judgment

S4:
no premature Judgment / Human remains distinct
```

Assert:

```text
adapter-local `_handles` text is not P1-7 evidence authority
reason text is not evidence authority
stockroom production uses judgment v2
judgment v1 remains unchanged
```

Do not require actual Docker/materializer/provider/tool/process execution.

# 22. static gate without pyc residue

Do not use `py_compile` in the repository.

Create one temporary verifier script outside the repository, for example:

```text
%TEMP%\aiscc_p2_3_a2_s2_static_verify.py
```

Use it to:

```text
read all changed Python files as UTF-8 strict
compile(source_text, path, "exec") in memory
load the v2 Judgment config through the production strict loader
optionally load frozen v1 for compatibility
```

No `.pyc` should be created.

Then run Ruff with exact project Python.

Changed Python path set:

```text
src/aiscc/evidence/models.py
src/aiscc/evidence/repository.py
src/aiscc/judgment/models.py
src/aiscc/judgment/authority.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Require:

```text
in-memory compile:
8 / 8 PASS

Ruff:
8 / 8 PASS

judgment v2 strict load:
PASS

judgment v1 compatibility load:
PASS

git diff --check:
PASS

index:
empty

new untracked pyc:
0
```

Failure:

```text
STATIC_CHECK_FAILURE
→ STOP
```

No same-turn source repair after mandatory static failure.

# 23. PostgreSQL prerequisite

After static PASS use an existing compatible local repository test PostgreSQL if available.

Otherwise Task-owned disposable fallback is authorized:

```text
image:
postgres:17.6-alpine

pull:
--pull=never

local loopback only

temporary storage

Task-owned unique container
```

No remote DB, image pull, or unrelated container mutation.

Set DB URLs only in Task process environment and do not print credentials.

Run:

```text
alembic upgrade head
alembic current
```

Require applied head:

```text
20260901_0008
```

No new migration.

# 24. mandatory P1-6/P1-7 proof

First run the two modified authority modules:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/evidence/test_postgres_evidence_admission.py   tests/integration/human/test_postgres_human_gate_judgment.py -ra
```

Require:

```text
all collected tests executed
0 fail
0 error
0 skip
```

No same-turn source repair after failure.

# 25. mandatory A2 S1-S4 authority proof

Then run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/scenarios/test_stockroom_capture_runner.py -ra
```

Require all collected tests PASS / zero skip.

This is bounded owner/authority integration, not actual Stockroom runtime capture.

# 26. prepared-owner/A1 regression

Rerun:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_owner_composition.py   tests/integration/scenarios/test_stockroom_binding.py   tests/unit/scenarios/test_stockroom_capture_runner.py -ra
```

Require all PASS.

Accepted pre-change count was:

```text
23 + 51 = 74
```

If inventory is unchanged, expect 74 PASS.

# 27. broader direct-owner regression

Run the exact bounded owner set:

```text
tests/integration/workflow/test_postgres_kernel.py
tests/unit/security/test_stockroom_policy.py
```

The modified evidence/Human-Judgment modules were already run in section 24 and must not be counted twice as fresh distinct proof.

Require all collected tests PASS / zero prerequisite skip.

# 28. compatibility regression

Run any direct existing Judgment/evidence unit tests imported or referenced by the modified source that are not already covered above, but keep the set bounded to:

```text
P1-6 evidence ref/model/repository
P1-7 Judgment model/policy/authority
```

Do not run the entire repository suite.

Record exact modules and counts.

# 29. no-runtime ceiling

Allowed:

```text
PostgreSQL/Alembic
real P1-6 evaluation persistence/resolution
real P1-7 Judgment issue/participant preparation
bounded WorkflowKernel transitions used by tests
A2 production owner construction
config loading
```

Forbidden:

```text
real Stockroom filesystem materialization
Stockroom Docker/process
provider
tool dispatch
AgentExecutionService runtime execution
network
real secret resolution
full actual S1-S4 capture
HumanResult fabrication
public deployment
Replay
Git add/commit/push
```

# 30. contract review

Require PASS:

```text
P1_6_NEGATIVE_REF_TYPED
P1_6_REF_STRICT_CANONICAL
P1_6_NEGATIVE_ROW_ROUNDTRIP
P1_6_CURRENTNESS_RECOMPUTED
P1_6_STALE_EVALUATION_DENIED
P1_6_NO_SATISFACTION_ATTESTATION_FOR_S2
P1_7_EXPLICIT_BASIS_KIND
P1_7_POSITIVE_NEGATIVE_MUTUAL_EXCLUSION
P1_7_ISSUE_TIME_NEGATIVE_AUTHORITY_VERIFIED
P1_7_PARTICIPANT_NEGATIVE_AUTHORITY_REVERIFIED
P1_7_POLICY_CHECKPOINT_BOUND
P1_7_POLICY_REQUIREMENT_SET_BOUND
P1_7_WRONG_TARGET_BASIS_DENIED
P1_7_FABRICATED_REF_DENIED
P1_7_LEGACY_V1_COMPATIBLE
P1_7_LEGACY_FINGERPRINT_STABLE
JUDGMENT_V1_CONFIG_FROZEN
JUDGMENT_V2_STRICT_ENROLLMENT
A2_S1_POSITIVE_PATH_PRESERVED
A2_S2_AUTHENTIC_NEGATIVE_REF_BOUND
A2_S3_NO_JUDGMENT
A2_S4_NO_PREMATURE_JUDGMENT
ADAPTER_LOCAL_HANDLE_NOT_AUTHORITY
REASON_TEXT_NOT_AUTHORITY
PREPARED_OWNER_MODEL_PRESERVED
MATERIALIZED_OUTPUT_BINDING_PRESERVED
SECURITY_CLOCK_FIX_PRESERVED
TOOL_OUTPUT_RUNTIME_EVIDENCE_BINDING_PRESERVED
NO_WORKFLOW_GUARD_CHANGE
NO_MIGRATION
NO_REAL_STOCKROOM_RUNTIME
```

Require:

```text
31 / 31 PASS
```

# 31. cleanup

If Task-owned PostgreSQL was created:

```text
remove only that exact container after evidence collection
```

Delete only the exact temporary verifier file if created.

Do not broad-clean caches or Docker.

# 32. final workspace

Before mutation and Task lifecycle:

```text
existing Git-visible:
43

current Cycle/Judgment:
2

excluding active Task:
45 exact

index:
empty
```

Of the nine mutation paths, two are already Git-visible:

```text
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Seven paths newly become Git-visible:

```text
src/aiscc/evidence/models.py
src/aiscc/evidence/repository.py
src/aiscc/judgment/models.py
src/aiscc/judgment/authority.py
config/judgment/stockroom-capture.v2.json
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
```

Before Task movement expected:

```text
52 exact Git-visible
index empty
```

Move active Task byte-identically to:

```text
.aiassistant/tasks/done/20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-implementation-1.md
```

Final expected:

```text
53 exact Git-visible
index empty
```

No other path.

# 33. no Git persistence

Do not run:

```text
git add
git commit
git push
git reset
git restore
git stash
```

A2 persistence is a later Browser decision.

# 34. required export

Folder:

```text
.aiassistant/reports/target/20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
IMPLEMENTATION_MANIFEST.md
MIGRATION_COMPATIBILITY.md
P1_6_NEGATIVE_REF_VERIFICATION.md
P1_6_CURRENTNESS_VERIFICATION.md
P1_7_NEGATIVE_BASIS_VERIFICATION.md
JUDGMENT_POLICY_V2_VERIFICATION.md
S2_AUTHORITY_VERIFICATION.md
POSTGRESQL_INTEGRATION_VERIFICATION.md
REGRESSION_VERIFICATION.md
COMPATIBILITY_VERIFICATION.md
CONTRACT_REVIEW.md
```

Also include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task

all nine mutation paths
```

Expected:

```text
15 root docs
12 canonical/source/config/test copies
27 members total
```

`EXPORT_MANIFEST.md` covers all 26 non-self entries with relative path, byte size, SHA-256.

Require:

```text
one top-level directory
27 exact members
CRC PASS
15/15 roots
12/12 copies
manifest 26/26
folder/archive byte equality
```

# 35. mandatory stop

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

# 36. success ceiling

Success:

```text
P1-6 negative evaluation authority:
IMPLEMENTED_CANDIDATE / EXECUTED_PASS

P1-7 negative Judgment basis:
IMPLEMENTED_CANDIDATE / EXECUTED_PASS

A2 S2:
AUTHORITY_BINDING_EXECUTED_PASS

A2 prepared-owner/materialized-output:
PRESERVED

A2:
READY_FOR_BROWSER FINAL IMPLEMENTATION JUDGMENT

A2 persistence:
NOT_AUTHORIZED

Stockroom runtime prerequisites:
NOT_VERIFIED

actual S1-S4 capture:
NOT_STARTED
```
