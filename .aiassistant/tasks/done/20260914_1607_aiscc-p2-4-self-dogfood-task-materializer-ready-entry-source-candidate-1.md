# 작업지시서: P2-4 Self-Dogfood Task materializer + READY entry source candidate

## meta

- task_id: `20260914_1607_aiscc-p2-4-self-dogfood-task-materializer-ready-entry-source-candidate-1`
- created_at: `2026-09-14T16:07:15+09:00`
- work_type: `BACKEND_IMPLEMENTATION + INTEGRATION_QA + GIT_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `4cbe22685a1f85d232894064d39876a12f4b962c`
- required_parent: `2d659a6ee34083146624401e26b130df91ab6ef8`
- predecessor_result_zip_sha256: `c44365c71bcaaf2d8879d544a0359dd03c1aebfdbe9ac6aac1a8b50460047314`
- predecessor_done_task_sha256: `94a6227e5d69395a0c3883a6502fbac8a1040f43cddd9f7c3ae8a66d3bc6701a`
- predecessor_judgment: `ACCEPTED / P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE`
- durable_taskcontract_commit: `4cbe22685a1f85d232894064d39876a12f4b962c`
- fresh_IDE_chat_required: `No`
- governance_commit_authorized: `Yes / exact 3 paths / Commit A`
- source_commit_authorized: `Yes / exact allowlist / Commit B`
- database_migration_authorized: `No`
- canonical_state_mutation_authorized: `No`
- actual_self_dogfood_golden_cycle_authorized: `No`
- real_active_Task_materialization_authorized: `No`
- provider_LLM_authorized: `No`
- external_network_authorized: `No`
- retained_private_DB_authorized: `No`
- Docker_authorized: `Yes / local postgres:17.6 task-owned integration proof only`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_SELF_DOGFOOD_ENTRY_SOURCE_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. predecessor acceptance

Browser independently verified the 1528 result:

```text
ZIP:
c44365c71bcaaf2d8879d544a0359dd03c1aebfdbe9ac6aac1a8b50460047314

members:
80

manifest rows:
79

CRC:
PASS

manifest size/SHA:
79/79 exact

focused regression:
13 PASS / 0 FAIL / 0 SKIP

full direct regression:
191 PASS / 0 FAIL / 0 SKIP

Ruff:
PASS

compile:
PASS

diff-check:
PASS
```

Governance Commit A:

```text
2d659a6ee34083146624401e26b130df91ab6ef8
```

Result Commit B:

```text
4cbe22685a1f85d232894064d39876a12f4b962c

parent:
2d659a6ee34083146624401e26b130df91ab6ef8

message:
feat(aiscc): add durable taskcontract authority

changed paths:
exact 24 authorized paths
```

Browser judgment:

```text
ACCEPTED
/ P2_4_TASKCONTRACT_DURABLE_BODY_IMPLEMENTATION_CANDIDATE
```

This acceptance means the durable TaskContract authority/runtime candidate is the current source baseline for P2-4.

It does NOT mean:

```text
self-dogfood source exists
golden cycle executed
P2-4 closed
canonical project state reconciled
Public Bounded Live released
```

# 1. predecessor evidence verification

Package predecessor evidence SHA-256:

- `CONTRACT_REVIEW.md`: `2915b50082d383e4a13b7ee7a0ad97c0e9957c4ee33f48fad17ff020d07e56ed`
- `CRITICAL_RUNTIME_REVERIFICATION.md`: `e19c15738e13af4cfe9fb65ac7a4a40f758b71ce3cb14477c2da140285e2f956`
- `EXECUTOR_REPORT.md`: `d2bd502683ccaf67e74c8d5c379dfb87a526ceb9017d39aec8900a69ce4c40d0`
- `FINAL_REGRESSION_RESULTS.md`: `504494110699c206b808409ee8da7b1b8d76797e5bee12742ba9353dc2906db6`
- `SOURCE_CHANGE_REVIEW.md`: `4bc9815275c6072f15e037edfc55464494ea2e53a9bcf4321e10296ddae65561`
- `WORKSPACE_VERIFICATION.md`: `6bdaf7be2fc8be6f5e46a85c115503b6e056b0811b2d481178d1b1981569402c`
- `evidence/COMMIT_A.json`: `915a12cf72117ef916d4d7b9fad7075c0d24a357f013427d3e2e191135e1e5d2`
- `evidence/COMMIT_B.json`: `64a2ca6e511704642acb5909e74472c0e4c14a5d72cf16ca2baed7fcab21d526`
- `evidence/POSTGRES_PROOF.json`: `e2f9c8843fe7956ee305ba1213fdc63bf4d78b74b6fc31f5a6c816e72fcba68e`
- `evidence/STATIC_CHECKS.json`: `5d15d8c3dc01616d06b692517b3cfbd8555140b6ba3c74a51b8aababaf221a96`

After Task-first read, copy these only under:

```text
.aiassistant/reports/target/20260914_1607_aiscc-p2-4-self-dogfood-task-materializer-ready-entry-source-candidate-1/accepted-input/
```

Any mismatch:

```text
BLOCKED_MISSING_ARTIFACT
```

STOP.

# 2. exact initial repository preflight

Require:

```text
branch:
main

HEAD:
4cbe22685a1f85d232894064d39876a12f4b962c

HEAD^:
2d659a6ee34083146624401e26b130df91ab6ef8

index:
empty

tracked:
clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1528_aiscc-p2-4-regression-fixture-closure-durable-taskcontract-final-candidate-retry-1.md
```

Done Task SHA:

```text
94a6227e5d69395a0c3883a6502fbac8a1040f43cddd9f7c3ae8a66d3bc6701a
```

Preserve ignored legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md

SHA-256:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Canonical state must initially and terminally remain byte-exact:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48

.aiassistant/records/aiscc/DECISION_REGISTER.md
9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5

.aiassistant/records/aiscc/NEXT_ACTIONS.md
050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679
```

Verify current Alembic head:

```text
20260914_0009
```

No new migration is authorized.

Any mismatch -> `POLICY_CONFLICT_INVESTIGATION_REQUIRED` or `DIRTY_WORKSPACE_MIXED` and STOP.

# 3. executables

Use only:

```text
Python:
<repository-root>\.venv\Scripts\python.exe

Git:
C:\Program Files\Git\cmd\git.exe

Docker:
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

Docker only for isolated integration tests if required.

# 4. inbound placement + Governance Commit A

Order:

```text
verify ZIP/hash/archive/path safety
→ place current Task into .aiassistant/tasks/active
→ read current Task
→ exact repository preflight
→ verify predecessor evidence
→ place Cycle/Judgment
```

Canonical:

```text
20260914_1607_aiscc-p2-4-durable-taskcontract-accepted-self-dogfood-source-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_1607_aiscc-p2-4-durable-taskcontract-implementation-final-acceptance-self-dogfood-source-authorization-1.md
-> .aiassistant/reports/aiscc/
```

Stage exactly:

```text
.aiassistant/tasks/done/20260914_1528_aiscc-p2-4-regression-fixture-closure-durable-taskcontract-final-candidate-retry-1.md
.aiassistant/records/aiscc/cycles/20260914_1607_aiscc-p2-4-durable-taskcontract-accepted-self-dogfood-source-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_1607_aiscc-p2-4-durable-taskcontract-implementation-final-acceptance-self-dogfood-source-authorization-1.md
```

Commit message exactly:

```text
docs(aiscc): accept durable taskcontract implementation candidate
```

Require:

```text
Commit A parent = 4cbe22685a1f85d232894064d39876a12f4b962c
changed paths = exact 3
index empty
tracked clean
Git-visible untracked = 0
```

No source mutation before Commit A.

# 5. objective

Implement only the P2-4 self-dogfood entry source candidate:

```text
verified/current durable TaskContract
→ deterministic typed SelfDogfoodTaskSpec
→ exact READY TransitionRequest adapter
→ existing TaskContractReadyParticipant
→ existing P1-4 PostgresTransitionRepository
→ WorkRun READY
```

This Task does NOT issue a real golden Task and does NOT execute a real self-dogfood cycle.

The source candidate must prove the composition that the future golden Task will use.

# 6. source ownership

Preserve:

```text
P1-8:
current NextAction selection / descriptor / source authority

EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY:
complete immutable TaskContract issue/revoke/currentness

P1-6:
Evidence requirement/checkpoint definition + G_EVIDENCE authority

P1-7:
HumanGate/HumanResult/Judgment authority

P1-4:
WorkRun/WorkflowState/TransitionDecision mutation authority
```

`self_dogfood` owns none of those semantic authorities.

It is a deterministic orchestration adapter only.

# 7. SelfDogfoodTaskSpec

Create a frozen, recursively immutable typed projection named:

```text
SelfDogfoodTaskSpec
```

It MUST be derived only from a repository-verified CURRENT TaskContract receipt/binding.

It is:

```text
view != authority
view != TaskContract
view != TaskIssuanceCandidate
view != NextActionSelection
```

Minimum exact exposed fields:

```text
project_id
task_id
task_contract_id
task_contract_version
task_contract_body_ref
task_contract_body_sha256

source_selection_id
source_selection_version
source_action_ref
source_selection_fingerprint
source_descriptor_fingerprint

repository_id
repository_root
base_commit

goal
non_goals
allowed_paths
forbidden_paths

evidence_requirement_set_ref
evidence_requirement_set_fingerprint
evidence_checkpoints

human_requirement_kind
judgment_owner_policy

runtime_mode
cycle_execution_mode
orchestrator_version
orchestrator_commit
```

Use existing typed enums/value objects where available.
Do not create duplicate RuntimeMode/WorkflowState/owner enums.

No field may be filled from Agent prose, Markdown parsing, current working directory inference or ambient environment.

# 8. materializer authority boundary

The materializer MUST NOT trust:

```text
caller-constructed VerifiedTaskContractBindingV1
caller boolean is_current
caller TaskContract body dict without repository verification
caller ActionDescriptor/TaskIssuanceCandidate alone
```

Preferred public entry shape:

```text
materialize_task_spec(
    task_authority_repository,
    issued_receipt,
    expected_repository_binding,
    expected_next_action_ref,
) -> SelfDogfoodTaskSpec
```

or an equivalent source-native class/service.

The implementation MUST call the accepted durable repository verifier:

```text
verify_task_contract(
    receipt,
    require_current=True,
    expected_repository_binding=...,
    expected_next_action_ref=...
)
```

before constructing the spec.

No `_ExternalTaskAuthorityWriter` may be accepted, imported into the public self_dogfood API, returned, serialized or stored.

`self_dogfood` cannot issue/revoke TaskContracts.

# 9. cycle-derived V1 source gate

The TaskContract runtime already owns the V1 source boundary.

Self-dogfood MUST preserve it.

Only:

```text
open-cycle-derived-task-issuance
```

may materialize.

`OPERATIONAL_RECOVERY` or any unsupported V1 source must fail through the existing TaskContract verification/currentness contract.

Do not duplicate or reinterpret P1-8 source-selection policy in `self_dogfood`.

No fallback.

# 10. deterministic materialization

For identical verified TaskContract canonical bytes and accepted owner state:

```text
SelfDogfoodTaskSpec bytes/value:
identical
```

The spec itself contains no:

```text
wall-clock issuance identity
random UUID
provider choice
LLM output
new authority hash
mutable list/dict
```

If serialization is needed for evidence, use the existing restricted canonical JSON routine.

Do not invent a second TaskContract fingerprint.
Use the body_ref/body_sha256 already owned by TaskContract.

# 11. READY adapter

Implement a bounded adapter that prepares a new exact READY request from a materialized spec plus explicitly supplied execution identity.

Recommended source-owned API shape:

```text
build_ready_request(
    spec,
    *,
    work_run_id,
    transition_request_id,
    requester_id,
) -> TransitionRequest
```

or equivalent.

The adapter MUST set exactly:

```text
project_id = spec.project_id
task_contract_id = spec.task_contract_id
task_contract_version = spec.task_contract_version
observed_state = None
observed_state_version = 0
target_state = READY
requester_type = SYSTEM
runtime_mode = OWNER_SELF_DOGFOOD
```

Execution identity fields are operation identity, not TaskContract authority.
Do not derive WorkRun authority from spec hash.

Reject invalid/blank/noncanonical supplied IDs using existing ID conventions.

# 12. READY execution composition

Implement a source candidate entry function/service that composes only existing owners:

```text
verified receipt
→ materialize current spec
→ build exact READY TransitionRequest
→ prepare_task_contract_ready(...)
→ PostgresTransitionRepository.decide(
      request,
      (),
      transaction_participant=participant
   )
```

Require result:

```text
DecisionOutcome.ADMITTED
WorkflowState.READY
state_version = 1
```

The self_dogfood adapter MUST NOT:

```text
write WorkRun directly
write WorkflowState directly
create TransitionDecision directly
mint G_CONTRACT/G_SCOPE/G_RUNTIME_CONTEXT directly
create HumanResult
create Judgment
create G_EVIDENCE
create G_HUMAN_*
create G_JUDGMENT_*
```

P1-4 + TaskContractReadyParticipant remain the only accepted path.

# 13. idempotency and stale denial

Required source behavior:

```text
same exact READY request retry:
existing P1-4 idempotent result

same work_run_id with conflicting request identity/body:
DENY

revoked TaskContract before READY:
DENY / no WorkRun

superseded/non-current TaskContract:
DENY / no WorkRun

stale P1-8 cycle selection:
DENY / no WorkRun

stale P1-6 definition graph:
DENY / no WorkRun

repository/base mismatch:
DENY / no WorkRun

unsupported recovery V1 source:
DENY before materialization/READY
```

Do not add repair/fallback.

# 14. output boundary — no real Task file

This implementation Task may produce test fixture/spec evidence only.

Forbidden in this Task:

```text
writing a real .aiassistant/tasks/active self-dogfood Task
issuing a real TaskContract for project execution outside task-owned test DB
creating a real project WorkRun
calling an external coding agent/provider
performing an Agent source change
admitting real EvidenceCandidate
creating real Judgment/Cycle from runtime
changing NEXT_ACTIONS
```

Those belong to the future golden-cycle Task after Browser accepts this source candidate.

# 15. exact source mutation allowlist

Preferred exact source paths:

```text
src/aiscc/self_dogfood/__init__.py
src/aiscc/self_dogfood/models.py
src/aiscc/self_dogfood/materializer.py
```

Optional only if actual composition requires it:

```text
src/aiscc/bootstrap.py
```

Tests:

```text
tests/unit/self_dogfood/test_task_materializer.py
tests/integration/self_dogfood/test_task_ready_entry.py
```

If package directories do not exist, create only the above package/test directories/files.

No modification is authorized in:

```text
src/aiscc/task_authority/**
src/aiscc/next_action/**
src/aiscc/evidence/**
src/aiscc/workflow/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/persistence/**
migrations/**
```

If self_dogfood integration requires a change there:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

STOP.

# 16. bootstrap rule

Modify `src/aiscc/bootstrap.py` only if an existing bootstrap/composition root must expose the read-only self-dogfood service.

If modified:

- do not expose `_ExternalTaskAuthorityWriter`;
- do not create a default public writer getter;
- do not add provider/network behavior;
- do not change existing owner registration semantics;
- do not create singleton mutable authority state.

If the self_dogfood service can be assembled cleanly in tests/explicit composition without bootstrap mutation, leave `bootstrap.py` unchanged.

# 17. tests — unit

`tests/unit/self_dogfood/test_task_materializer.py` must cover:

```text
verified current receipt -> exact immutable spec PASS
spec deterministic equality PASS
all required fields exact
caller-created unverified binding/body cannot materialize
repository mismatch DENY
base mismatch DENY
wrong expected next-action ref DENY
unsupported V1 recovery source DENY
revoked/non-current receipt DENY
mutable input cannot mutate produced spec
no writer capability exposed/imported by public self_dogfood API
no duplicate RuntimeMode/WorkflowState definitions
```

No DB/provider required for pure shape cases where existing fakes can represent verifier failure truthfully.
Do not replace currentness verification with a fake success path in the authoritative tests.

# 18. tests — isolated PostgreSQL integration

Use local `postgres:17.6` only; no pull.

One Task-owned disposable container, e.g.:

```text
aiscc-p2-4-self-dogfood-1607-pg
```

Loopback-only, synthetic credentials, no host bind.

`tests/integration/self_dogfood/test_task_ready_entry.py` must prove on real accepted owner repositories:

1. empty DB -> migration head `20260914_0009` PASS;
2. create/enroll exact cycle-derived P1-8 authority required by TaskContract fixture;
3. register exact P1-6 definition graph;
4. issue one synthetic/test-only durable TaskContract through the existing private composition capability in the integration fixture;
5. materialize `SelfDogfoodTaskSpec`;
6. exact spec fields equal body/owner data;
7. build READY request;
8. existing `TaskContractReadyParticipant` + P1-4 admits WorkRun READY v1;
9. retry exact request idempotent;
10. TaskContract revoke before fresh READY -> DENY / no WorkRun;
11. stale/superseded P1-8 selection -> DENY / no WorkRun;
12. stale/revoked P1-6 definition -> DENY / no WorkRun;
13. repository/base mismatch -> DENY / no WorkRun;
14. operational-recovery V1 source -> DENY / zero WorkRun/body side effect attributable to self_dogfood;
15. no HumanGate/HumanResult/Judgment/evidence-set attestation created by READY;
16. WorkRun/state mutation exists only through P1-4 history/decision;
17. no provider/tool/network calls;
18. restart materialization from durable receipt produces same spec.

Tests may use the private writer only inside existing owner composition/test fixture setup.
The public `self_dogfood` surface must never expose it.

# 19. direct regressions

Inventory and run targeted existing regression sets at minimum:

```text
tests/unit/task_authority
tests/integration/task_authority
tests/unit/next_action
tests/integration/memory/test_postgres_project_memory_next_action.py
tests/integration/workflow
tests/integration/evidence
tests/integration/human
```

Do not modify those existing tests/source in this Task.

Any existing regression failure caused by the new source candidate -> product rework within self_dogfood allowlist only.

If correction requires an external owner path -> STOP.

# 20. static verification

Required:

```text
Ruff changed Python PASS
compile changed Python PASS
git diff --check PASS
UTF-8/no BOM/control checks changed files PASS
```

No broad generated cache residue.

# 21. source Commit B

Only after all source candidate tests/regressions/static checks PASS.

Stage all and only actually changed paths from section 15.

Commit message exactly:

```text
feat(aiscc): add self dogfood task materializer
```

Require:

```text
Commit B parent = Governance Commit A
no path outside source allowlist
index empty
tracked clean
```

No Commit B on blocker/failure.

# 22. export

Target:

```text
.aiassistant/reports/target/20260914_1607_aiscc-p2-4-self-dogfood-task-materializer-ready-entry-source-candidate-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
PREDECESSOR_ACCEPTANCE_VERIFICATION.md
SOURCE_AUTHORITY_REVIEW.md
SELF_DOGFOOD_SPEC_REVIEW.md
READY_ENTRY_REVIEW.md
POSTGRES_RUNTIME_EVIDENCE.md
TEST_RESULTS.md
STATIC_CHECKS.md
CONTRACT_REVIEW.md
```

Include changed project-relative files plus current Cycle/Judgment/done Task.

No credentials/raw DB dumps/private DB URL.

Result ZIP:

```text
.aiassistant/reports/target/20260914_1607_aiscc-p2-4-self-dogfood-task-materializer-ready-entry-source-candidate-1.zip
```

# 23. terminal success boundary

Success:

```text
HEAD = source Commit B
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1607_aiscc-p2-4-self-dogfood-task-materializer-ready-entry-source-candidate-1.md
```

Current Task active -> done byte-exact.

Legacy 1400 unchanged.

Canonical state hashes unchanged.

No Task-owned Docker residue.

# 24. blockers

```text
BLOCKED_MISSING_ARTIFACT
DIRTY_WORKSPACE_MIXED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
MIGRATION_BASELINE_MISMATCH
ISOLATED_POSTGRES_IMAGE_MISSING
BLOCKED_REQUIRED_EVIDENCE
SECURITY_BOUNDARY_BLOCKED
```

On blocker:

- no source Commit B;
- preserve truthful Task-owned changes/evidence;
- no broad reset/clean.

# 25. success ceiling

Complete PASS may report only:

```text
P2_4_SELF_DOGFOOD_ENTRY_SOURCE_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do NOT perform/claim:

```text
actual self-dogfood golden cycle
P2-4 ACCEPTED/CLOSED
canonical state reconciliation
Public Bounded Live
```

After Browser accepts this source candidate, the next substantive Task should normally combine:

```text
source candidate persistence confirmation
+
one actual AISCC self-dogfood golden cycle
```

without another design microtask unless a concrete blocker appears.
