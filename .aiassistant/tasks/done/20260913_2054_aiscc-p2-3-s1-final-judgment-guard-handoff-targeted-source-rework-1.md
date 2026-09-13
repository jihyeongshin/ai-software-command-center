# 작업지시서: P2-3 S1 final Judgment guard handoff targeted source rework

## meta

- task_id: `20260913_2054_aiscc-p2-3-s1-final-judgment-guard-handoff-targeted-source-rework-1`
- created_at: `2026-09-13T20:54:52+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `TARGETED_SOURCE_REWORK / S1_FINAL_JUDGMENT_GUARD_HANDOFF`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `15c9e975ec193526eafa0749fc97321c4d89d713`
- required_parent: `c9093e8441de230f9470313d874a33addc75423c`
- required_grandparent: `af5a9f873f11da1fdf71362abde018a2bed313a4`
- reviewed_2040_result_zip_sha256: `a2f56fca40ad570450466cd693a57e039d65211c93ace327c0ad5f20bf93c70f`
- private_runtime_access_authorized: `No`
- retained_PostgreSQL_access_authorized: `No`
- Docker_runtime_execution_authorized: `No`
- source_change_authorized: `Conditional / exact causal handoff defect only`
- targeted_test_authorized: `Yes`
- canonical_state_write_authorized: `No`
- Git_commit_push_authorized: `No`
- success_ceiling: `FINAL_JUDGMENT_GUARD_HANDOFF_SOURCE_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. accepted 2040 runtime facts

Browser accepts the 2040 result as truthful runtime evidence.

```text
result ZIP:
a2f56fca40ad570450466cd693a57e039d65211c93ace327c0ad5f20bf93c70f

contract:
49 PASS / 2 FAIL / 0 NOT_REACHED
```

Successful runtime chain:

```text
READY/v1
→ RUNNING/v2

EXECUTION_STARTED:
present before side effects

provider:
2 completed / exact grants

tool:
1 completed / exact grant

attempt:
EXECUTOR_COMPLETED/v8

RUNNING→ADMISSION_PENDING:
ADMITTED / v3

runtime evidence:
ADMITTED

evidence-set:
SATISFIED

Judgment:
ACCEPTED / one persisted
```

Failure:

```text
TO_ACCEPTED:
DENIED / JudgmentAuthorityError

WorkRun:
ADMISSION_PENDING/v3

human_guard_attestations:
0

judgment_guard_attestations:
0

final transition triplet:
0
```

The exact underlying `JudgmentAuthorityError` field/message was not captured by 2040. Do not invent it.

# 1. executable

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Python:

```text
<repository-root>\.venv\Scripts\python.exe
```

Use that fixed relative executable only.

Forbidden:

```text
python
py
WindowsApps
PATH Python discovery
repository-external Python/venv discovery
```

Git may be used read-only only.

# 2. repository baseline

Require:

```text
branch main
HEAD 15c9e975ec193526eafa0749fc97321c4d89d713
HEAD^ c9093e8441de230f9470313d874a33addc75423c
HEAD^^ af5a9f873f11da1fdf71362abde018a2bed313a4
index empty
tracked clean
Git-visible untracked before delivery exactly 6
```

The six predecessor governance artifacts are:

- `.aiassistant/records/aiscc/cycles/20260913_2019_aiscc-p2-3-provider-grant-fix-accepted-fresh-s1-v3-retry-entry-1.cycle.md`  `959ac0166ba30510172b2a5a349fab5b622ad7282d67853b8ee8de2830e3561f`
- `.aiassistant/reports/aiscc/20260913_2019_aiscc-p2-3-provider-grant-fix-source-acceptance-and-runtime-retry-authorization-1.md`  `aba7746a9febe65de59fdebc504be9ca889225d3e1e5d181249cdc51ed612d06`
- `.aiassistant/tasks/done/20260913_2019_aiscc-p2-3-provider-grant-fix-persistence-and-fresh-s1-v3-runtime-retry-1.md`  `a7e1d738a03f0a5209f9edd2349d797ef7590afc2b526a9207596c731caeeb87`
- `.aiassistant/records/aiscc/cycles/20260913_2040_aiscc-p2-3-fresh-s1-v4-runtime-retry-entry-1.cycle.md`  `0043e24a5125f12f122e7adcdac14bdca2ed0797a415ebe5ae70ba0fe666de08`
- `.aiassistant/reports/aiscc/20260913_2040_aiscc-p2-3-2019-part-a-accepted-part-b-executor-preflight-retry-judgment-1.md`  `5beb946af3bcf6c1149ac236c797a9492368e19272eb8d1441220ea2c5940c6e`
- `.aiassistant/tasks/done/20260913_2040_aiscc-p2-3-fresh-s1-v4-runtime-retry-after-executor-path-basis-correction-1.md`  `26d530e1500cbcb5347e3ee1ace4e637e71398adf898baaf41340f5d26491cdd`

Current canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Persisted provider-grant fix identities:

- `src/aiscc/scenarios/stockroom_production.py`  `335678daa9fcd4dd9a4b1a2fc4a53876086cab0d555edb7c413466c531dd6d75`
- `tests/integration/scenarios/test_stockroom_binding.py`  `9bd991b77f711a46662262e12f1471b0b78ba1cc6151b3f6a04650ea68bbf439`
- `tests/unit/providers/test_stockroom_tool.py`  `8acda82618b05364e8a7d31ee1b8f6ed28f1bbf5c6a680dda7e8ffc745466544`

Preserve ignored non-owned legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement with Task active/ignored:

```text
Git-visible untracked exactly 8
```

Mismatch → STOP before source mutation.

# 3. hard prohibitions

Do not:

```text
access retained PostgreSQL
read private secret
inspect/mutate v1/v2/v3/v4 private roots
run Stockroom Docker
invoke retained production builder
replay v4
manually transition v4
create HumanResult for v4
insert Human/Judgment guard rows directly
DB-repair v4
weaken P1-4 transition guard rules
weaken P1-7 Judgment/guard ownership
treat Judgment existence alone as final TransitionDecision
modify canonical state
commit
push
```

# 4. diagnosis objective

Trace the current source-owned S1 path from Judgment issuance through the final workflow transition.

At minimum inspect:

```text
StockroomCaptureRunner.run

StockroomCaptureOwnerAdapter:
- Judgment issue/evaluate path
- final transition path

P1-7:
- JudgmentPolicyAuthority
- Judgment repository/authority
- Human guard authority
- Judgment guard authority
- guard-attestation production APIs

P1-4:
- WorkflowKernel
- transition evaluator/repository
- G_HUMAN_* / G_JUDGMENT_* guard consumption

stockroom Judgment config/policy
```

Produce an exact call-chain table:

```text
stage
source owner
input authority/ref
durable output expected
actual current call
actual current output
mismatch
source location
```

# 5. required semantic distinction

Preserve all:

```text
Judgment != TransitionDecision
JudgmentStatus.ACCEPTED != WorkRun.ACCEPTED
HumanGate/HumanResult != Judgment
P1-7 owns Human/Judgment guard facts
P1-4 exclusively owns WorkflowState mutation
```

A valid fix must make the source-owned production path obtain the required owner-backed P1-7 guard facts before asking P1-4 for the final transition.

Do not bypass guards.

# 6. reproduce locally before correction

Using only local/non-private fixtures, reproduce the current final-transition failure or prove mechanically why the exact current call must fail.

Required evidence should distinguish:

```text
Judgment row exists
vs
Judgment guard attestation exists

Human not required
vs
Human guard attestation proving not-required/applicable outcome
```

Capture the exact local `JudgmentAuthorityError` message/failed authority field if the local supported fixture can reproduce it.

No private DB/runtime is allowed for diagnosis.

# 7. conditional modification scope

Only if one bounded causal handoff defect is proven, implement the smallest correction.

Allowed product paths:

```text
src/aiscc/scenarios/capture_runner.py
src/aiscc/scenarios/stockroom_production.py
src/aiscc/judgment/authority.py
src/aiscc/judgment/repository.py
src/aiscc/human/authority.py
src/aiscc/persistence/repository.py
src/aiscc/workflow/matrix.py
```

A listed path that does not exist is not permission to create it unless source ownership proves it is the correct new module. Prefer existing owner APIs.

Allowed test paths:

```text
tests/unit/judgment/**
tests/unit/human/**
tests/unit/scenarios/**
tests/integration/judgment/**
tests/integration/human/**
tests/integration/scenarios/test_stockroom_binding.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

If the actual causal owner is outside this allowlist:

```text
STOP / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

Report exact path/API and do not edit outside scope.

# 8. correction requirements

The correction must prove:

```text
S1 normal / Human not required:
owner-backed Human guard fact present as required by policy

ACCEPTED Judgment:
owner-backed Judgment guard fact present

final transition request:
uses those exact P1-7 guard refs

ADMISSION_PENDING→ACCEPTED:
admitted only when all current state/version/evidence/Human/Judgment guards are valid
```

Negative requirements:

```text
missing Judgment guard:
DENIED

wrong Judgment ref:
DENIED

stale state/version:
DENIED

wrong WorkRun/task/policy binding:
DENIED

Human-required policy without HumanResult:
DENIED

raw Judgment row alone:
insufficient
```

Do not write guard attestations from the scenario adapter by constructing persistence rows directly. Use P1-7 owner APIs.

# 9. targeted verification

Use repository-local Python with `-B`.

Minimum verification:

```text
changed-file py_compile
Ruff on changed Python
targeted P1-7 guard authority unit tests
targeted P1-4/P1-7 final transition integration
targeted Stockroom S1 local fake end-to-end:
READY→RUNNING→ADMISSION_PENDING→ACCEPTED
Judgment ACCEPTED
required guard attestations present
external provider/network 0
git diff --check
```

The Stockroom fake test must use local/non-private fixtures only.

Do not run full repository suite automatically. If targeted failures indicate broad regression scope is required, STOP with `EVIDENCE_SCOPE_EXPANSION_REQUIRED`.

# 10. v4 preservation

Do not access private runtime/DB in this Task.

Treat only as Browser-accepted predecessor evidence:

```text
v4 WorkRun:
ADMISSION_PENDING/v3

v4 attempt:
EXECUTOR_COMPLETED/v8

S1 admitted evidence:
1

S1 evidence-set attestation:
1

ACCEPTED Judgment:
1

Human/Judgment guard attestations:
0 / 0

provider/tool:
2 / 1 completed

v4 workspace:
retained evidence-bearing materialization
```

No replay or repair.

# 11. result classification

Success candidate:

```text
exact JudgmentAuthorityError/handoff defect diagnosed
minimal owner-correct source fix applied
P1-7 guard ownership preserved
P1-4 mutation ownership preserved
negative guard cases remain fail-closed
local fake S1 reaches ACCEPTED
private runtime retry NOT performed
```

If diagnosis is inconclusive:

```text
STOP / DIAGNOSIS_INCONCLUSIVE
```

# 12. Git boundary

No commit.

Final tracked dirt must be only allowed causal source/test paths.

Current Task active→done byte-identically.

Git-visible untracked exactly:

```text
2019 Cycle/Judgment/done Task
2040 Cycle/Judgment/done Task
current Cycle/Judgment/done Task
```

Count:

```text
9
```

Legacy 1400 remains ignored/non-owned.

# 13. contract review

Exactly 33 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_2019_2040_TRIPLES_EXACT
PREDECESSOR_2040_RESULT_SHA_EXACT
CURRENT_STATE_HASHES_EXACT
PERSISTED_SOURCE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
2040_RUNTIME_PROGRESS_ACCEPTED
2040_FINAL_TRANSITION_FAILURE_ACCEPTED
NO_PRIVATE_RUNTIME_ACCESS
NO_RETAINED_DB_ACCESS
NO_DOCKER_RUNTIME_EXECUTION
JUDGMENT_TO_GUARD_CALLCHAIN_IDENTIFIED
HUMAN_GUARD_REQUIREMENT_IDENTIFIED
JUDGMENT_GUARD_REQUIREMENT_IDENTIFIED
FINAL_TRANSITION_GUARD_INPUT_IDENTIFIED
EXACT_CAUSAL_HANDOFF_DEFECT_PROVEN
P1_7_AUTHORITY_NOT_WEAKENED
P1_4_TRANSITION_GUARDS_NOT_WEAKENED
MINIMAL_CAUSAL_CHANGE_ONLY
NO_MANUAL_V4_TRANSITION_OR_REPLAY
TARGETED_P1_7_UNIT_TESTS_PASS
TARGETED_P1_4_P1_7_INTEGRATION_PASS
TARGETED_STOCKROOM_S1_FAKE_PASS
NO_EXTERNAL_PROVIDER_NETWORK
NO_CANONICAL_STATE_MUTATION
NO_GIT_COMMIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_CHANGED_PATHS_WITHIN_ALLOWLIST
FINAL_UNTRACKED_GOVERNANCE_EXACT
DIAGNOSIS_REPORT_COMPLETE
EXPORT_INTEGRITY_PASS
```

Successful source candidate:

```text
33 / 33 PASS
```

Blocked result must not mark unexecuted correction/tests PASS.

# 14. export

Root docs:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
2040_ACCEPTANCE_VERIFICATION.md
JUDGMENT_GUARD_HANDOFF_DIAGNOSIS.md
P1_7_AUTHORITY_VERIFICATION.md
P1_4_TRANSITION_GUARD_VERIFICATION.md
SOURCE_CHANGE_SUMMARY.md
TEST_VERIFICATION.md
CONTRACT_REVIEW.md
```

Include:

```text
current Cycle
current Judgment
current done Task
all changed product/test paths
```

Generate manifest/member count from actual set.

Require:

```text
one top-level
CRC PASS
manifest SHA/size exact
TASK.md == canonical done Task
no private path/value/DB body
```

# 15. success ceiling

```text
2040 v4 runtime:
REWORK_REQUIRED / preserved

provider/tool/evidence/Judgment path:
runtime-proven through ACCEPTED Judgment

final Judgment guard handoff:
SOURCE CANDIDATE CORRECTED

private S1 retry:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
