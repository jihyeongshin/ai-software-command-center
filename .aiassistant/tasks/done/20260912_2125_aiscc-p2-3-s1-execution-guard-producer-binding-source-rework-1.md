# 작업지시서: P2-3 S1 execution-guard producer binding source rework

## meta

- task_id: `20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-source-rework-1`
- created_at: `2026-09-12T21:25:13+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `SOURCE_REWORK / P1_4_EXECUTION_GUARD_PROVENANCE`
- evidence_profile: `HIGH_RISK_SOURCE`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- required_parent: `4096913e9a117bd49bfecdb1ce5ca8de2735d661`
- required_grandparent: `6d41633210f0e556dd4292ee62a8600c6b54215f`
- fresh_ide_executor_chat: `REQUIRED`
- success_ceiling: `S1_EXECUTION_GUARD_PRODUCER_BINDING_CORRECTED_CANDIDATE / BROWSER_REVIEW_PENDING`
- private_s1_execution_authorized: `No`

# 0. purpose

Fix the durable provenance gap confirmed by the 2052 static review.

Required invariant:

```text
current evidence-review authority:
ADMISSION_PENDING / current_version

immutable producer authority:
ExecutionSubmissionRef
RUNNING / producer_version
exact submission_id
exact execution_attempt_id

historical LINK:
the current ADMISSION_PENDING is the exact admitted immediate successor transition
whose G_EXECUTOR_SUBMISSION guard was issued from that exact verified producer ref
```

Do not rebind producer provenance to current state.
Do not treat the producer ref itself as evidence admission.

# 1. transport

Start in a fresh IDE Executor chat.

Verify exact delivery ZIP filename/SHA from the Short Prompt.
Require exactly three flat safe members.

Place current Task first:

```text
.aiassistant/tasks/active/20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-source-rework-1.md
```

Require byte equality and ignored status.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-rework-entry-1.cycle.md
SHA-256:
fd7877ecab06d40dcac3a36f99a5b0ad72c94a0ffb055a1dab51d79defd4327f

.aiassistant/reports/aiscc/20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-scope-expansion-judgment-1.md
SHA-256:
06cb0d64c092417d1dfd4b98279a9a9b0d8df41e169ac9a2b410f130fadfc7bc
```

Bootstrap mismatch:

```text
STOP
no source write
no tests
no report/export
```

# 2. repository baseline

Require:

```text
branch main
HEAD ee623c995cf1c24b4a362834f2d6d1fdf71a30cd
HEAD^ 4096913e9a117bd49bfecdb1ce5ca8de2735d661
HEAD^^ 6d41633210f0e556dd4292ee62a8600c6b54215f
index empty
tracked worktree clean
```

Before current delivery Git-visible untracked exactly these 12 predecessor artifacts:

- `.aiassistant/tasks/done/20260912_1749_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-1.md`  `0668ed1fb71ce57f6b87dacb91c810f7505596eb6efe835841c019f3a2d51ecd`
- `.aiassistant/records/aiscc/cycles/20260912_1749_aiscc-p2-3-cut-c-persisted-private-s1-execution-entry-1.cycle.md`  `75fe2a744d010e327ff2d549aa998e2e64e0449735d50eec69a4fd6a183044ad`
- `.aiassistant/reports/aiscc/20260912_1749_aiscc-p2-3-cut-c-persistence-final-acceptance-private-s1-authorization-judgment-1.md`  `6457922c2520c2255edf9574b1c68c3ed633c3615e80be5c95c7e04f9e5961ed`
- `.aiassistant/tasks/done/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-retry-1.md`  `f3fbe8fed5d2dfcc6ac6b4586567b410e64653f648943f162219b11648ab3819`
- `.aiassistant/records/aiscc/cycles/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocked-retry-entry-1.cycle.md`  `1bb88d04b2e567a9b11ab8fb99449571696a5e039571cef6438fa62bb3fea870`
- `.aiassistant/reports/aiscc/20260912_1954_aiscc-p2-3-private-s1-acl-query-transport-blocker-hold-judgment-1.md`  `ee9436791b8595333090eb2a06b295ef4b3b87f620894756fea0a97176ebd25d`
- `.aiassistant/tasks/done/20260912_2024_aiscc-p2-3-s1-admission-pending-evidence-state-contract-source-rework-1.md`  `c61d14d7cb8fd3ac929701550a3530577eed99ad083b0bacee29f55c27d7584c`
- `.aiassistant/records/aiscc/cycles/20260912_2024_aiscc-p2-3-s1-source-state-contract-defect-rework-entry-1.cycle.md`  `8c9ca5c06d658e9e2723ee70b2b54b999801cf17494543480caf7743840e7a44`
- `.aiassistant/reports/aiscc/20260912_2024_aiscc-p2-3-s1-source-state-contract-defect-confirmed-judgment-1.md`  `c8a921efc6112c2bbd8532ed0869e08e9c1f1eebea4121805f0c839ad3bbf0c2`
- `.aiassistant/tasks/done/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-decoupling-source-rework-1.md`  `bf1c50f34cdd21ccf14d3009aeb309df3904d8903fdbeb30063b911c4a4279f3`
- `.aiassistant/records/aiscc/cycles/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-rework-entry-1.cycle.md`  `119f40188ec87d4e98d0152f9c762a90d40f1096316beaba158cc0244b19ce5f`
- `.aiassistant/reports/aiscc/20260912_2052_aiscc-p2-3-s1-current-state-producer-provenance-conflict-judgment-1.md`  `cefcaa10a62e80779121bbf1014caa748195c48cb62d48c5e2406b99cc77bc37`

After current Cycle/Judgment placement while current Task remains active/ignored:

```text
Git-visible untracked:
14 exact

twelve predecessors
current Cycle
current Judgment
```

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `7d0c9954b87e945b8c1c3fb66bda2dd54d23d5c3319202ef9fb24aa0ac56f424`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `04ec792c5e6dd4a7c8d2d35b716d1ed1fd569e60bb557532b811bc33dd434946`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `61ae340fa06e3d87d80f3308a240dacc1e0ba132a3b241a2059757830cf6312a`

Any extra/missing path or tracked delta:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 3. source baseline

Known exact baselines:

```text
src/aiscc/scenarios/stockroom_production.py
SHA-256 685e2ec549473e167ed1fe4d7de1050d7a53a449d1d278dcdb3439a471478f1f

src/aiscc/scenarios/capture_runner.py
SHA-256 600de0a4b0e718f02ab2e1907b7be62b2c4a23756559fdf99cb4cd55fb80b3d2

tests/integration/scenarios/test_stockroom_capture_runner.py
SHA-256 373f9d5bc6f260785cdf943aa649ce99ab5826e8ae09dd2982c18db09459fbf5
```

Require them byte-equal to HEAD.

Also require these expanded owner paths are tracked and worktree byte-equal to HEAD:

```text
src/aiscc/workflow/guards.py
src/aiscc/persistence/repository.py
```

Before any edit record for both:

```text
HEAD blob ID
whole-file SHA-256
```

No hash value may be guessed by the Task.

# 4. required read scope

Read exact current implementations around:

```text
P1_4GuardAuthority.issue_from_execution_ref
required_bound_refs
GuardFact / guard-evaluation models and serialization
transition request/evaluation/decision models
historical transition persistence row serialization
_historical_evaluation_from_row
verify_historical_transition_provenance
ExecutionSubmissionRef
ExecutionReferenceAuthority.register_submission
ExecutionReferenceAuthority.verify
provider execution-completion/submission issuance
StockroomCaptureRunner.run
StockroomCaptureOwnerAdapter.transition
StockroomCaptureOwnerAdapter.submit_runtime_evidence
StockroomCaptureOwnerAdapter._current
```

Read canonical P1-4/P1-5/P1-6/security rules for:

```text
G_EXECUTOR_SUBMISSION
G_CURRENT
producer-ref non-substitution
state/version freshness
guard bound refs
ADMISSION_PENDING evidence review
```

# 5. mandatory pre-write feasibility gate

Before changing any file, mechanically answer all of the following from current source.

## 5.1 bound_refs storage

Require `GuardFact.bound_refs` or its exact current equivalent is already:

```text
part of durable guard fact identity
serialized losslessly
fingerprinted
persisted
reconstructed on restart/historical verification
```

If not:

```text
MODEL_SCHEMA_SCOPE_REQUIRED
→ STOP before source write
```

No model/schema/migration change is authorized.

## 5.2 canonical ref encoding

Find an existing canonical convention for typed immutable refs in guard `bound_refs`.

It must be sufficient to distinguish at least:

```text
execution submission identity
execution attempt identity
```

Do not invent an ad-hoc string format if no convention exists.

If no canonical encoding exists:

```text
BOUND_REF_ENCODING_UNDEFINED
→ STOP before source write
```

## 5.3 exact producer source

Require `issue_from_execution_ref` receives or obtains an **already verified issuer-backed**
`ExecutionSubmissionRef`.

The new binding must be derived from that verified authority object/result, not from arbitrary caller strings.

## 5.4 historical exposure

Require the existing persistence representation can reconstruct the bound refs and the historical verifier can
return or expose them without a model/schema change.

## 5.5 adapter predecessor identity

Determine how the exact admitted `RUNNING → ADMISSION_PENDING` transition identity can be supplied to
`submit_runtime_evidence`.

Allowed options, only if current source makes them authoritative:

```text
thread the admitted transition request/decision identity from StockroomCaptureRunner.run
or
load an exact unique predecessor identity from existing durable current projection/history API
```

Do not infer it merely from version adjacency.

If implementing the exact link requires any production path outside section 6:

```text
SOURCE_SCOPE_INSUFFICIENT
→ STOP before source write
→ name the exact additional path/API required
```

# 6. maximum allowed tracked source paths

Only these five tracked files may be modified:

```text
src/aiscc/workflow/guards.py
src/aiscc/persistence/repository.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

A subset is allowed.

No other production/test/config/state/migration path may change.

If another path is required:

```text
SOURCE_SCOPE_INSUFFICIENT
→ STOP
```

# 7. execution guard correction

Only after section 5 fully passes.

In the existing P1-4 execution guard issuance path:

```text
verify the ExecutionSubmissionRef with existing issuer authority first
then emit G_EXECUTOR_SUBMISSION using exact current canonical authority fields
```

The emitted durable guard fact must bind exactly:

```text
submission identity
execution attempt identity
```

using the existing canonical typed-ref encoding.

`required_bound_refs` or exact current equivalent must make these bindings mandatory for
`G_EXECUTOR_SUBMISSION`.

Require:

```text
missing one binding → fail closed
duplicate/conflicting binding → fail closed
wrong ref type → fail closed
```

Do not add evidence authority to this guard.

# 8. historical persistence/reconstruction correction

Ensure current persistence serialization/fingerprint/reconstruction preserves the exact execution guard bound refs.

`verify_historical_transition_provenance` or the exact current historical verifier must:

```text
validate the persisted guard binding
reject missing/malformed execution submission binding
reject missing/malformed execution attempt binding
expose the verified exact binding to the caller through existing return structures or bounded repository API
```

It must continue to verify:

```text
request/evaluation/decision fingerprints
run identity
source/target state
source/result version
admitted lineage
history membership
```

No auto-repair of older incomplete provenance.

Historical transition rows without the required new binding:

```text
fail closed for this exact producer-link proof
```

# 9. runner → adapter predecessor identity

Preserve runner semantic order:

```text
execution completes
RUNNING_TO_ADMISSION_PENDING admitted
then submit_runtime_evidence
```

If the current adapter cannot know the exact predecessor transition identity, thread only the minimum immutable
request/decision identity through the existing source-owned call boundary.

Do not pass a caller-authored claimed state/version in place of transition identity.

Runner order itself must remain unchanged.

# 10. adapter authority decoupling

At runtime-evidence submission require three independent proofs.

## CURRENT

Load authoritative WorkRun and require:

```text
WorkflowState.ADMISSION_PENDING
current state_version exact
same run/task
```

using the existing `_current` fail-closed authority.

## PRODUCER

Verify the exact `ExecutionSubmissionRef` through `ExecutionReferenceAuthority.verify`.

Expected producer context must remain:

```text
WorkflowState.RUNNING
original producer state_version
exact run
exact execution_attempt_id
```

Do not rebind to ADMISSION_PENDING/current_version.

## LINK

Use the exact predecessor transition identity and historical verifier to require:

```text
decision ADMITTED
source RUNNING / producer_version
target ADMISSION_PENDING / producer_version + 1
result == current ADMISSION_PENDING/current_version
same WorkRun
G_EXECUTOR_SUBMISSION fact contains the exact verified submission binding
G_EXECUTOR_SUBMISSION fact contains the exact verified attempt binding
```

The expected producer context for `ExecutionReferenceAuthority.verify` may use independently verified historical
predecessor values, but not unverified values copied solely from the producer ref.

Only after CURRENT + PRODUCER + LINK pass may the adapter create/submit the runtime EvidenceCandidate.

# 11. non-substitution

Preserve:

```text
ExecutionSubmissionRef
!= EvidenceCandidate
!= AdmittedEvidence
!= G_EVIDENCE
```

The new bound refs prove the historical producer used for G_EXECUTOR_SUBMISSION only.

They must not satisfy any evidence requirement by themselves.

# 12. focused regression

Use the existing integration test path:

```text
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Required cases:

```text
POSITIVE:
verified RUNNING/vN submission + attempt
→ G_EXECUTOR_SUBMISSION stores both exact bindings
→ admitted RUNNING/vN → ADMISSION_PENDING/vN+1
→ historical verifier returns exact bindings
→ current ADMISSION_PENDING + exact producer + exact link
→ runtime evidence submission proceeds

MISSING_SUBMISSION_BINDING:
deny/fail closed

MISSING_ATTEMPT_BINDING:
deny/fail closed

WRONG_SUBMISSION:
deny

WRONG_ATTEMPT:
deny

WRONG_PRODUCER_VERSION:
deny

UNRELATED_PENDING_TRANSITION:
same current ADMISSION_PENDING shape but different predecessor producer binding
→ deny

REF_ONLY_NON_SUBSTITUTION:
authentic ExecutionSubmissionRef without evidence admission
→ no AdmittedEvidence / no G_EVIDENCE
```

Also prove:

```text
runner transition order unchanged
_current remains fail closed
ExecutionReferenceAuthority.verify not weakened
```

# 13. validation

Use repository `.venv` actual Python, not WindowsApps alias.

Run compile/lint over all five bounded files as applicable:

```text
.venv\Scripts\python.exe -B -m py_compile
  src/aiscc/workflow/guards.py
  src/aiscc/persistence/repository.py
  src/aiscc/scenarios/capture_runner.py
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py

.venv\Scripts\python.exe -m ruff check
  src/aiscc/workflow/guards.py
  src/aiscc/persistence/repository.py
  src/aiscc/scenarios/capture_runner.py
  src/aiscc/scenarios/stockroom_production.py
  tests/integration/scenarios/test_stockroom_capture_runner.py
```

Run:

```text
.venv\Scripts\python.exe -B -m pytest -q
  tests/integration/scenarios/test_stockroom_capture_runner.py

.venv\Scripts\python.exe -B -m pytest -q tests/unit
```

Do not start Docker/PostgreSQL/private S1 to satisfy tests.

If repository tests require an external runtime not already represented by the bounded test scope, report the exact
requirement and STOP rather than provisioning it.

# 14. Git boundary

No staging/commit/push.

Forbidden:

```text
git add
git commit
git push
git reset
git restore
git checkout
git stash
git clean
```

At successful source candidate completion:

```text
modified tracked paths:
non-empty subset of the exact allowed five
no path outside allowed five

index:
empty
```

Move current Task byte-identically:

```text
.aiassistant/tasks/active/20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-source-rework-1.md
→
.aiassistant/tasks/done/20260912_2125_aiscc-p2-3-s1-execution-guard-producer-binding-source-rework-1.md
```

Final Git-visible untracked:

```text
15 exact

twelve predecessor artifacts
current Cycle
current Judgment
current done Task
```

# 15. runtime prohibition

Do not access or mutate:

```text
Docker
PostgreSQL
private password file
private runtime root
provider/network
prepare_capture
WorkRun
S1/S2/S3/S4
Replay
```

No canonical state mutation.

# 16. contract review

Require exactly 43 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
PREDECESSOR_12_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
KNOWN_SOURCE_BASELINES_EXACT
EXPANDED_SOURCE_PATHS_TRACKED_AT_HEAD
CURRENT_G_EXECUTOR_SUBMISSION_GAP_REPRODUCED
GUARD_FACT_BOUND_REFS_STORAGE_LOSSLESS
BOUND_REF_CANONICAL_ENCODING_EXISTS
NO_MODEL_SCHEMA_MIGRATION_REQUIRED
EXACT_PRODUCER_BINDING_DERIVED_FROM_VERIFIED_REF
G_EXECUTOR_SUBMISSION_BOUND_REFS_EXACT
HISTORICAL_RECONSTRUCTION_PRESERVES_BOUND_REFS
HISTORICAL_VERIFIER_REJECTS_MISSING_BINDING
HISTORICAL_VERIFIER_REJECTS_MALFORMED_BINDING
HISTORICAL_VERIFIER_EXPOSES_EXACT_BINDING
CURRENT_STATE_ADMISSION_PENDING_EXACT
PRODUCER_STATE_RUNNING_VERSION_IMMUTABLE
PREDECESSOR_TRANSITION_IDENTITY_THREADED
PREDECESSOR_LINK_SAME_RUN_ATTEMPT_EXACT
EXECUTION_REFERENCE_VERIFY_NOT_WEAKENED
P1_6_NON_SUBSTITUTION_PRESERVED
RUNNER_ORDER_UNCHANGED
NO_AUTHORITY_UNION_OR_FALLBACK
MODIFIED_PATHS_WITHIN_ALLOWED_5
REGRESSION_POSITIVE_LINK_PASS
REGRESSION_MISSING_BOUND_REF_DENIED
REGRESSION_WRONG_SUBMISSION_DENIED
REGRESSION_WRONG_ATTEMPT_DENIED
REGRESSION_WRONG_PRODUCER_VERSION_DENIED
REGRESSION_UNRELATED_PENDING_TRANSITION_DENIED
REGRESSION_REF_ALONE_NO_EVIDENCE_AUTHORITY
TARGETED_SCENARIO_PYTEST_PASS
UNIT_REGRESSION_PYTEST_PASS
RUFF_PASS
PY_COMPILE_PASS
NO_DOCKER_DB_PRIVATE_ACCESS
NO_S1_S4_EXECUTION
NO_CANONICAL_STATE_MUTATION
NO_GIT_COMMIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_DIFF_WITHIN_ALLOWED_5
EXPORT_INTEGRITY_PASS
```

Success:

```text
43 / 43 PASS
```

Blocked rows stay `BLOCKED_REQUIRED_EVIDENCE`.

# 17. success export

Root docs exactly 13:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
SOURCE_SCOPE_VERIFICATION.md
GUARD_PROVENANCE_VERIFICATION.md
HISTORICAL_PROVENANCE_VERIFICATION.md
ADAPTER_DECOUPLING_VERIFICATION.md
RUNNER_LINKAGE_VERIFICATION.md
TEST_VERIFICATION.md
GIT_DIFF_VERIFICATION.md
NO_RUNTIME_EXECUTION_VERIFICATION.md
CONTRACT_REVIEW.md
```

Include project-relative copies of exactly:

```text
current Cycle
current Judgment
current done Task
src/aiscc/workflow/guards.py
src/aiscc/persistence/repository.py
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

The five source copies are included even if a particular allowed path remains unchanged.

Success export:

```text
21 total members
20 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == current done Task
```

Blocked export may omit source copies that were never modified/readied as candidate evidence; never fabricate a patch.

# 18. mandatory stop

Stop before source write on:

```text
bound_refs not durably stored
no canonical typed-ref encoding
model/schema/migration change required
exact predecessor identity cannot be established within allowed five paths
additional production owner required
```

Stop after write on:

```text
unexpected modified path
test/compile/lint failure
authority weakening
runtime/private access attempt
```

Do not broaden scope.

# 19. success ceiling

```text
S1 execution-guard producer binding:
CORRECTED_CANDIDATE

current evidence-review authority:
ADMISSION_PENDING

producer provenance:
RUNNING / original version / exact submission+attempt / immutable

historical predecessor link:
DURABLY_VERIFIED

runner:
ORDER_UNCHANGED

private S1 runtime:
NOT_EXECUTED

Browser source acceptance:
HUMAN_PENDING

Git persistence:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
