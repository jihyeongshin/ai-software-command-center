# 작업지시서: P2-3 A2 S2 G_REWORK_SPEC test-input correction + full proof

## meta

- task_id: `20260911_1805_aiscc-p2-3-a2-s2-rework-spec-test-input-correction-and-full-proof-1`
- created_at: `2026-09-11T18:05:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `TEST_REWORK / FULL_AUTHORITY_PROOF`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. purpose

Implement only the accepted diagnostic correction.

Current failure is not a P1-4/P1-6/P1-7 authority defect.

It is an incomplete integration-test transition input:

```text
ADMISSION_PENDING v3
→ REWORK_REQUIRED

required:
G_HUMAN_NOT_REQUIRED
G_JUDGMENT_REWORK
G_REWORK_SPEC

current test:
facts=()
```

Correct only the test harness, then rerun the full authority proof.

# 1. inbound transport

Verify the Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place this TASK first at:

```text
.aiassistant/tasks/active/20260911_1805_aiscc-p2-3-a2-s2-rework-spec-test-input-correction-and-full-proof-1.md
```

Read fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_1805_aiscc-p2-3-a2-s2-denial-root-cause-accepted-test-rework-entry-1.cycle.md
SHA-256:
3f8b1b0fbe8ff4b0aaf3733f943911c377de038a4ce7bab7a697f486f4a12db3

.aiassistant/reports/aiscc/20260911_1805_aiscc-p2-3-a2-s2-transition-denial-diagnostic-final-acceptance-judgment-1.md
SHA-256:
1ef9b697c4d3fb909544d1b4d38de459c25b218bc6014cc64b48578a4028a0e0
```

Bootstrap failure before current Task placement:

```text
STOP
no project mutation
no report/export
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

Canonical predecessor Task:

```text
.aiassistant/tasks/done/20260911_1500_aiscc-p2-3-a2-s2-rework-transition-denial-root-cause-diagnostic-1.md
SHA-256:
2978df347f4042d60606a7a4da1fd4fd4181b1a28eac432a91c4fc6b7044df43
```

That Task section 2 contains the exact predecessor 64-path inventory.

Current expected Git-visible set before this delivery is:

```text
that exact 64-path predecessor inventory
+
the predecessor 1500 done Task
=
65 exact paths
```

After placing current Cycle/Judgment and excluding active current Task:

```text
67 exact paths
```

Any extra/missing path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 3. exact predecessor identity

Require:

- `.aiassistant/tasks/done/20260911_1500_aiscc-p2-3-a2-s2-rework-transition-denial-root-cause-diagnostic-1.md`  `2978df347f4042d60606a7a4da1fd4fd4181b1a28eac432a91c4fc6b7044df43`
- `.aiassistant/records/aiscc/cycles/20260911_1500_aiscc-p2-3-a2-s2-authority-proof-failed-transition-denial-diagnostic-entry-1.cycle.md`  `1219d6b5cd5b2cd3dcfdbb209e0a996f988a98df915b93a68957b272924e9d32`
- `.aiassistant/reports/aiscc/20260911_1500_aiscc-p2-3-a2-s2-negative-judgment-transition-denial-judgment-1.md`  `cde6eea9e492b135ba3442dbc6761b92a441341b8daa0c37f8fd9102c75ee332`

Require current test identity before mutation:

```text
tests/integration/human/test_postgres_human_gate_judgment.py
SHA-256:
5fbcc635948906250b2795b6f31b9e5a849ab8991e203dcbcad661a571d67058
```

Any mismatch:

```text
PREDECESSOR_OR_SOURCE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 4. exact mutation allowlist

Only:

```text
MODIFY
tests/integration/human/test_postgres_human_gate_judgment.py
```

Frozen:

```text
src/**
config/**
migrations/**
all other tests/**
```

Especially frozen:

```text
src/aiscc/workflow/kernel.py
src/aiscc/workflow/matrix.py
src/aiscc/workflow/guards.py
src/aiscc/workflow/evaluator.py
src/aiscc/workflow/participants.py
src/aiscc/human/authority.py
src/aiscc/judgment/authority.py
src/aiscc/judgment/models.py
src/aiscc/evidence/repository.py
src/aiscc/evidence/models.py
src/aiscc/scenarios/stockroom_production.py
config/judgment/stockroom-capture.v1.json
config/judgment/stockroom-capture.v2.json
```

If another path appears necessary:

```text
SCOPE_EXPANSION_REQUIRED
→ STOP_WITH_REPORT_EXPORT
```

# 5. before-mutation invariant snapshot

Before editing, build a deterministic SHA-256 inventory over:

```text
src/**
config/**
tests/**
migrations/**
```

excluding:

```text
**/__pycache__/**
*.pyc
```

Record it.

At final verification every path except:

```text
tests/integration/human/test_postgres_human_gate_judgment.py
```

must remain byte-identical.

# 6. preserve incomplete-input denial regression

In:

```text
test_p1_7_postgres_runtime_proof
```

retain the current incomplete negative transition using:

```text
facts=()
```

and assert exactly:

```text
DecisionOutcome.DENIED
reason == MISSING_GUARD
missing_guards == (G_REWORK_SPEC,) or exact canonical equivalent

G_CURRENT satisfied
G_HUMAN_NOT_REQUIRED satisfied
G_JUDGMENT_REWORK satisfied
G_REWORK_SPEC unsatisfied/missing

WorkRun remains:
ADMISSION_PENDING
state_version == 3
```

Do not reinterpret this decision as a P1-7 failure.

# 7. immutable request identity

Do not reuse the denied request ID with changed facts.

Create a distinct corrected `TransitionRequest` with:

```text
new transition_request_id
same authoritative WorkRun
observed_state = ADMISSION_PENDING
observed_state_version = 3
target = REWORK_REQUIRED
same authentic P1-6 negative evaluation ref
same authentic P1-7 Judgment ref
```

Any helper used to create it must preserve canonical request semantics.

# 8. fresh request-bound participants

Create fresh participants bound to the corrected request:

```text
Human:
G_HUMAN_NOT_REQUIRED participant

Judgment:
exact current negative Judgment participant
```

Do not reuse participant instances bound to the denied request ID.

Compose them in the same accepted order used by the canonical test:

```text
Human
→ Judgment
```

# 9. complete P1-4 system facts

For the corrected request, use the existing test helper:

```text
system_facts(system, corrected_negative_request)
```

Do not manually construct or forge `G_REWORK_SPEC`.

The helper must produce the same P1-4 system-owned fact mechanism used by existing valid transitions.

Require the corrected transition to contain a valid:

```text
G_REWORK_SPEC
```

fact.

# 10. corrected transition expectation

Execute the corrected request through the real kernel.

Require:

```text
DecisionOutcome.ADMITTED

source:
ADMISSION_PENDING v3

target/result:
REWORK_REQUIRED v4
```

Guard evidence must show:

```text
G_CURRENT:
satisfied

G_HUMAN_NOT_REQUIRED:
satisfied

G_JUDGMENT_REWORK:
satisfied

G_REWORK_SPEC:
satisfied
```

No other guard may substitute for `G_REWORK_SPEC`.

# 11. stale negative control

Preserve the existing stale negative-evaluation control.

Tighten only as needed to distinguish it from the missing-guard case.

Require its primary durable reason to remain:

```text
STALE_REQUEST
```

when authoritative state/version is stale.

Do not allow a missing unrelated system fact to be presented as the authority proof for staleness.

# 12. existing invalid-input coverage

Preserve current negative-basis coverage for:

```text
wrong run
wrong state/version
wrong checkpoint
wrong requirement set
fabricated ref
missing negative ref
positive ref in negative slot
both positive+negative refs
incompatible target/policy
stale evaluation/currentness
legacy v1 compatibility
```

Do not weaken any existing assertion merely to pass the corrected path.

# 13. no authority semantic change

This Task must preserve:

```text
authentic negative Judgment is necessary but not sufficient

G_REWORK_SPEC remains independent P1-4 system authority

P1-7 Judgment participant does not mint G_REWORK_SPEC

P1-6 UNSATISFIED evaluation does not become positive admitted evidence

reason text is not authority

adapter-local handles are not authority
```

# 14. static gate

Do not use repository `py_compile`.

Create an external temporary verifier and compile changed/relevant Python source text in memory.

At minimum compile:

```text
tests/integration/human/test_postgres_human_gate_judgment.py
src/aiscc/evidence/models.py
src/aiscc/evidence/repository.py
src/aiscc/judgment/models.py
src/aiscc/judgment/authority.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Strict-load:

```text
config/judgment/stockroom-capture.v2.json
config/judgment/stockroom-capture.v1.json
```

Run Ruff on the same eight Python paths.

Require:

```text
in-memory compile:
8 / 8 PASS

Ruff:
8 / 8 PASS

Judgment v2 loader:
PASS

Judgment v1 loader:
PASS

git diff --check:
PASS

index:
empty

new repo-visible .pyc:
0
```

Failure:

```text
STATIC_CHECK_FAILURE
→ STOP_WITH_REPORT_EXPORT
```

No same-turn repair after mandatory static failure.

# 15. PostgreSQL prerequisite

Use the existing bounded local pattern.

Allowed fallback:

```text
postgres:17.6-alpine
--pull=never
loopback only
Task-owned container
temporary storage
```

No remote DB, pull, or unrelated Docker mutation.

Require Alembic:

```text
20260901_0008 (head)
```

No migration creation.

# 16. P1-6/P1-7 authority proof

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/evidence/test_postgres_evidence_admission.py   tests/integration/human/test_postgres_human_gate_judgment.py -ra
```

Require:

```text
all collected PASS
0 fail
0 error
0 skip
```

The corrected Human/Judgment module must prove both:

```text
incomplete facts:
DENIED / MISSING_GUARD / G_REWORK_SPEC

complete facts with new request:
ADMITTED / REWORK_REQUIRED
```

# 17. A2 S1-S4 authority proof

Then run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/integration/scenarios/test_stockroom_capture_runner.py -ra
```

Require all collected PASS / zero skip.

Must cover:

```text
S1 positive SATISFIED path
S2 authentic negative ref -> Judgment -> complete rework transition
S3 no Judgment
S4 no premature Judgment
prepared/materialized-output binding
```

No actual Stockroom runtime.

# 18. prepared-owner / A1 regression

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider   tests/unit/scenarios/test_owner_composition.py   tests/integration/scenarios/test_stockroom_binding.py   tests/unit/scenarios/test_stockroom_capture_runner.py -ra
```

Historical expected combined baseline:

```text
74 PASS
```

Require all collected PASS.

# 19. bounded direct-owner regression

Run:

```text
tests/integration/workflow/test_postgres_kernel.py
tests/unit/security/test_stockroom_policy.py
```

Require all collected PASS / zero prerequisite skip.

No workflow semantics changed; this is preservation proof only.

# 20. compatibility regression

Run:

```text
tests/unit/human/test_human_judgment_domain.py
tests/unit/evidence/test_admission_domain.py
tests/unit/evidence/test_durable_content.py
```

and any directly imported P1-6/P1-7 unit module proven necessary by the changed test path.

Do not run the whole repository suite.

Record exact modules and counts.

# 21. contract review

Require all prior 31 invariants plus four diagnostic-specific invariants:

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

INCOMPLETE_REWORK_FACTS_DENIED
G_REWORK_SPEC_INDEPENDENT
CORRECTED_REWORK_FACTS_ADMITTED
TRANSITION_REQUEST_ID_NOT_REUSED
```

Require:

```text
35 / 35 PASS
```

# 22. runtime ceiling

Allowed:

```text
PostgreSQL/Alembic
P1-6 evaluation persistence/resolution
P1-7 Judgment issue/participant preparation
bounded WorkflowKernel transitions
A2 production owner construction used by tests
config loading
```

Forbidden:

```text
real Stockroom filesystem materialization
Stockroom Docker/process runtime
provider/tool dispatch
AgentExecutionService runtime execution
network
real secrets
actual S1-S4 capture
HumanResult fabrication
Replay
Git add/commit/push
```

# 23. failure handling

After Task placement, any mandatory failure must:

```text
stop further product execution
move current Task byte-identically to done
produce failure report/evidence
produce verified export ZIP
```

Only bootstrap failure before current Task placement uses no report/export.

# 24. cleanup

Remove only exact Task-owned:

```text
PostgreSQL container
external static verifier
other external diagnostic temp file if created
```

No broad cleanup.

# 25. final workspace

Before this delivery:

```text
65 exact Git-visible paths
```

With current Cycle/Judgment and excluding active Task:

```text
67 exact
```

The authorized test is already Git-visible, so its byte change does not add a path.

Move current active Task byte-identically to:

```text
.aiassistant/tasks/done/20260911_1805_aiscc-p2-3-a2-s2-rework-spec-test-input-correction-and-full-proof-1.md
```

Final expected:

```text
68 exact Git-visible paths
index empty
```

Verify the pre/post source inventory:

```text
all src/config/tests/migrations paths except
tests/integration/human/test_postgres_human_gate_judgment.py
remain byte-identical
```

# 26. no Git persistence

Do not run:

```text
git add
git commit
git push
git reset
git restore
git stash
```

# 27. required export

Folder:

```text
.aiassistant/reports/target/20260911_1805_aiscc-p2-3-a2-s2-rework-spec-test-input-correction-and-full-proof-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ROOT_CAUSE_ADMISSION.md
IMPLEMENTATION_MANIFEST.md
STATIC_VERIFICATION.md
P1_6_NEGATIVE_REF_VERIFICATION.md
P1_6_CURRENTNESS_VERIFICATION.md
P1_7_NEGATIVE_BASIS_VERIFICATION.md
REWORK_SPEC_GUARD_VERIFICATION.md
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
tests/integration/human/test_postgres_human_gate_judgment.py
```

Expected:

```text
16 root docs
4 canonical/test copies
20 members total
```

`EXPORT_MANIFEST.md` covers all 19 non-self entries with relative path, byte size, SHA-256.

Require one top-level directory, CRC PASS, exact member set, manifest exact.

# 28. success ceiling

Success:

```text
P1-6 negative evaluation authority:
IMPLEMENTED_CANDIDATE / EXECUTED_PASS

P1-7 negative Judgment authority:
IMPLEMENTED_CANDIDATE / EXECUTED_PASS

S2 G_REWORK_SPEC:
COMPLETE / EXECUTED_PASS

A2 S1-S4 bounded authority proof:
EXECUTED_PASS

A2 prepared-owner/materialized-output:
PRESERVED

A2:
READY_FOR_BROWSER FINAL IMPLEMENTATION JUDGMENT

A2 persistence:
NOT_AUTHORIZED

actual Stockroom runtime capture:
NOT_STARTED
```
