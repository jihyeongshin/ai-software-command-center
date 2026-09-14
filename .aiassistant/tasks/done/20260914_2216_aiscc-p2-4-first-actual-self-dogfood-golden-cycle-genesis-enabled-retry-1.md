# 작업지시서: P2-4 first actual self-dogfood golden cycle — Genesis-enabled retry

## meta

- task_id: `20260914_2216_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-genesis-enabled-retry-1`
- created_at: `2026-09-14T22:16:21+09:00`
- work_type: `ACTUAL_SELF_DOGFOOD_GOLDEN_CYCLE + GENESIS_BOOTSTRAP + GOVERNANCE_RUNTIME + SINGLE_FILE_AGENT_CHANGE + GIT_PERSISTENCE`
- evidence_profile: `CRITICAL_GOLDEN`
- execution_mode: `MANUAL_COMMAND_CENTER_OUTER / AISCC_SELF_DOGFOOD_INNER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `621c1a374fe6ad42731c6249c68a39421eeda395`
- required_parent: `82fbc40b2e3e465d442b22ba4ba55014508fce6c`
- predecessor_result_zip_sha256: `466cde11361d85e3b592cce0c87664a5b4be3f7f0d9da96db387a7d9898ebae7`
- predecessor_done_task_sha256: `dcf15e7c3c6894c32bf270379421b67fc6fce2bf77964c9d19e5ca3a7c52fc6f`
- predecessor_judgment: `ACCEPTED / P2_4_SELF_DOGFOOD_GENESIS_AUTHORITY_IMPLEMENTATION_CANDIDATE`
- migration_head: `20260914_0012`
- fresh_IDE_chat_required: `No`
- governance_commit_authorized: `Yes / exact 3 paths / Commit A`
- real_self_dogfood_Task_authorized: `Yes / exact supplied inner Task`
- real_local_PostgreSQL_runtime_authorized: `Yes / one Task-owned postgres:17.6`
- real_TaskContract_WorkRun_authorized: `Yes / one golden lineage`
- real_repository_Agent_change_authorized: `Yes / exact one file`
- real_evidence_judgment_cycle_nextaction_authorized: `Yes / exact golden lineage`
- result_commit_authorized: `Yes / exact one governed source file / Commit B`
- canonical_state_mutation_authorized: `No`
- product_runtime_source_mutation_authorized: `No`
- test_rule_migration_mutation_authorized: `No`
- provider_LLM_external_network_authorized: `No`
- retained_private_DB_authorized: `No`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_FIRST_SELF_DOGFOOD_GOLDEN_CYCLE_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. accepted predecessor

Browser accepts 2010:

```text
ACCEPTED
/ P2_4_SELF_DOGFOOD_GENESIS_AUTHORITY_IMPLEMENTATION_CANDIDATE
```

Independent archive verification:

```text
Result ZIP SHA-256:
466cde11361d85e3b592cce0c87664a5b4be3f7f0d9da96db387a7d9898ebae7

80 members
79 manifest rows
CRC PASS
79/79 manifest size+SHA exact

Result Commit B:
621c1a374fe6ad42731c6249c68a39421eeda395

parent:
82fbc40b2e3e465d442b22ba4ba55014508fce6c

message:
feat(aiscc): add self dogfood genesis authority

migration:
20260914_0012
```

The result's separate verification record also reports terminal HEAD `621c1a374fe6ad42731c6249c68a39421eeda395`.

# 1. accepted evidence

Hashes:

- `CONTRACT_REVIEW.md`: `6495ce2353bd9a507e0a565226e6d9b57db3e562cd7c86ad3d961a74f196414f`
- `EXECUTOR_REPORT.md`: `aeefb7c5cbe8baf274139da07a35e7a9e4f758652ac9c936709f090d66be3046`
- `GENESIS_AUTHORITY_REVIEW.md`: `ec8a585ed20f2ace344ad660a42488989f243f677516d3d329720d3729d19366`
- `GENESIS_CURRENTNESS_REVIEW.md`: `be202260c50c3877f7e34da5f4724a98a0267373572b80fa7a32da44133e270d`
- `LOCK_INVARIANT_REVIEW.md`: `7f1460518b4db8f4999be00f74e7b03e20099624c0af7673173f164dc35468c9`
- `MIGRATION_REVIEW.md`: `92968a75353448d104479f41f170117910f8807319adc93239336268b528f8ce`
- `POSTGRES_RUNTIME_EVIDENCE.md`: `91cb276addfe8d98ce991746a87d63050c29ddbb056d1d040765ef0c967a014a`
- `STATIC_CHECKS.md`: `5167b84a2132a584503e19f9f7994358687596f70fa369360ace3601ba7e3300`
- `TASKCONTRACT_GENESIS_HANDOFF_REVIEW.md`: `2457a761bdb076034d114c2c7bbfa37de5c53bacf0fb7bf59bdcae09f23d9fc3`
- `TEST_RESULTS.md`: `c441b48da2115ece4011fbbd001b32593e26ff5371cc1bdcb0478f6d8f02db16`
- `WORKSPACE_VERIFICATION.md`: `128562be00e29a49336f4dcf1aaada3e4ef89263d67fc1293c3fe7e4893a4713`
- `evidence/COMMIT_A.json`: `9758ffb84059cc914fb83a0bd3ba030d65fd79b7f762580aebd3b87e6c5a66ec`
- `evidence/COMMIT_B.json`: `7ba0a9ba8a78d75ef325224a6fd27cb77ee290297d7704008e9812bedc274679`
- `evidence/FINAL_STATIC_CHECKS.json`: `1c44a02d0fd3a1e3ec7aaf5a15a5d4d2466bbabea876fb770d97032e70efb126`
- `evidence/POSTGRES_FINAL_PROOF.json`: `c5c451c835da5a53ff6f698f8046e5681390e744b6d9afeadb3bb831ab9503c5`
- `evidence/TERMINAL_WORKSPACE.json`: `02de991258a3cb66172253d42f3f47234ea706d0a70a9d4c3b9259facb56dd6d`

After Task-first read, copy these only into:

```text
.aiassistant/reports/target/20260914_2216_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-genesis-enabled-retry-1/accepted-input/
```

Mismatch -> `BLOCKED_MISSING_ARTIFACT`.

# 2. exact inner Task

Package member:

```text
20260914_2216_aiscc-p2-4-golden-agent-single-file-proof-change-2.md
```

Expected SHA-256:

```text
93600cafcade7e51495f6cea4f4797e6677b4e835231f19cced8d934ec5e8574
```

Governed path:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

Expected target SHA-256:

```text
7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
```

The inner Task is instruction/provenance.
The durable TaskContract is runtime authority.

# 3. exact repository preflight

Require before Governance Commit A:

```text
branch = main
HEAD = 621c1a374fe6ad42731c6249c68a39421eeda395
HEAD^ = 82fbc40b2e3e465d442b22ba4ba55014508fce6c
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_2010_aiscc-p2-4-self-dogfood-genesis-bootstrap-authority-implementation-1.md
```

Done Task SHA:

```text
dcf15e7c3c6894c32bf270379421b67fc6fce2bf77964c9d19e5ca3a7c52fc6f
```

Require target absent:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

Preserve legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Canonical state exact initially and terminally:

```text
CURRENT_STATE_SUMMARY.md
80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48

DECISION_REGISTER.md
9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5

NEXT_ACTIONS.md
050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679
```

Alembic code head:

```text
20260914_0012
```

No product/test/rule/migration mutation.

# 4. executables

Use only:

```text
Python:
<repository-root>\.venv\Scripts\python.exe

Git:
C:\Program Files\Git\cmd\git.exe

Docker:
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

No PATH substitution.
No Docker pull.

# 5. outer transport + Governance Commit A

Order:

```text
verify delivery ZIP/hash/archive/path safety
→ place outer Task into .aiassistant/tasks/active
→ read outer Task
→ verify preflight
→ verify inner Task bytes
→ verify predecessor accepted evidence
→ place current Cycle/Judgment
```

Canonical:

```text
20260914_2216_aiscc-p2-4-genesis-implementation-accepted-actual-golden-retry-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_2216_aiscc-p2-4-genesis-implementation-final-acceptance-golden-retry-authorization-1.md
-> .aiassistant/reports/aiscc/
```

Stage EXACTLY:

```text
.aiassistant/tasks/done/20260914_2010_aiscc-p2-4-self-dogfood-genesis-bootstrap-authority-implementation-1.md
.aiassistant/records/aiscc/cycles/20260914_2216_aiscc-p2-4-genesis-implementation-accepted-actual-golden-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_2216_aiscc-p2-4-genesis-implementation-final-acceptance-golden-retry-authorization-1.md
```

Commit message exactly:

```text
docs(aiscc): accept genesis authority and retry golden cycle
```

Require:

```text
Commit A parent = 621c1a374fe6ad42731c6249c68a39421eeda395
changed paths = exact 3
index empty
tracked clean
Git-visible untracked = 0
```

The resulting Commit A is the golden repository base.

# 6. actual-vs-test boundary

This is actual operational runtime, not pytest proof.

Forbidden as golden authority:

```text
tests.* imports
pytest fixtures
monkeypatch
direct owner-table INSERT/UPDATE/DELETE
fake owner rows
fake predecessor WorkRun/Cycle/memory
manual register_start/register_submission as authenticity
Recorded Replay relabeled current
Browser Markdown relabeled runtime authority
```

A Task-owned operational driver may exist only under:

```text
.aiassistant/reports/target/20260914_2216_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-genesis-enabled-retry-1/runtime/
```

It is never committed.

Private binders may be called only where the source deliberately exposes them as trusted composition seams for the external Command Center/P1-5/P1-8 owner.

# 7. actual local runtime

Require existing local image:

```text
postgres:17.6
```

No pull.

Create one Task-owned PostgreSQL 17.6 container:

```text
aiscc-p2-4-golden-2216-pg
```

Requirements:

```text
loopback-only
synthetic credentials
no host bind
empty operational DB
upgrade to 20260914_0012
```

This DB is the actual local golden control-plane runtime.

# 8. mandatory runtime source audit

Before creating operational authority, inspect current source-owned APIs for:

```text
SELF_DOGFOOD_GENESIS issuance/currentness
P1-8 genesis selection
P1-6 requirement-definition enrollment
P1-7 deterministic Judgment policy
TaskContract genesis issuance
SelfDogfoodTaskSpec materialization
READY entry
external IDE start
completion lease/submission
P1-6 external producer admission
structured NEXT_ACTION_CONTEXT evidence needed by Cycle
terminal Judgment/transition
Cycle admission
post-Cycle CYCLE_DERIVED selection
```

Create:

```text
GOLDEN_RUNTIME_SOURCE_AUDIT.md
```

If a real owner API is absent and would require product implementation:

```text
GOLDEN_AUTHORITY_GAP
```

STOP before crossing that boundary.

No product source fix is authorized in this Task.

# 9. exact operational identity

Use one explicit project lineage:

```text
project_id:
aiscc-self-dogfood-p2-4-golden-1

repository_id:
ai-software-command-center

repository_root:
C:\Users\oracl\IdeaProjects\ai-software-command-center

phase_id:
P2-4

runtime_mode:
OWNER_SELF_DOGFOOD

cycle_execution_mode:
AISCC_SELF_DOGFOOD

repository base:
Governance Commit A
```

Do not substitute another project identity after runtime rows are created.

# 10. P1-6 and P1-7 prerequisite owner configuration

Before TaskContract issuance, use only current owner APIs to establish the exact P1-6/P1-7 configuration needed for this TaskContract.

P1-6 must support actual admitted proof for at minimum:

```text
inner Task SHA = 93600cafcade7e51495f6cea4f4797e6677b4e835231f19cced8d934ec5e8574
WorkRun identity
external IDE submission identity
changed path = docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
target SHA = 7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
git diff --check = PASS
unauthorized Agent source diff count = 0
```

Also establish the source-owned structured-result path required for the first Cycle's durable `NEXT_ACTION_CONTEXT`.

P1-7 must configure:

```text
owner_policy = SYSTEM_DETERMINISTIC
human = NOT_REQUIRED
target outcome = ACCEPTED
requires exact satisfied P1-6 evidence
```

Do not fabricate HumanResult.

If actual P1-6 structured context cannot be produced/admitted without a test-only/fake issuer:

```text
GOLDEN_NEXT_ACTION_CONTEXT_EVIDENCE_GAP
```

STOP.

If deterministic Judgment configuration cannot be represented:

```text
GOLDEN_JUDGMENT_POLICY_UNAVAILABLE
```

STOP.

# 11. actual Genesis NextAction

Instantiate the accepted one-time genesis owner for the exact project/repository/base/phase.

Through its trusted writer, issue exactly one:

```text
SELF_DOGFOOD_GENESIS
open-self-dogfood-genesis-task-issuance
```

authority.

Require empty-project eligibility from product-owned reads:

```text
no admitted Cycle
no CURRENT NEXT_ACTION_CONTEXT memory
no pre-existing WorkRun
no conflicting current selection
```

Issue/enroll the genesis descriptor/policy through current P1-8 owner APIs.

Select exactly one current genesis NextAction.

Record:

```text
genesis authority ref/fingerprint
selection id/version/fingerprint
descriptor ref/fingerprint
candidate id/fingerprint
project revision
```

No Cycle/memory refs exist at this point.

# 12. actual genesis-backed TaskContract

Issue exactly one TaskContract V1 through the existing trusted external Task-authority writer.

Fixed semantic content:

```text
task_id:
20260914_2216_aiscc-p2-4-golden-agent-single-file-proof-change-2

contract_id:
aiscc-p2-4-golden-cycle-1

contract_version:
1

goal:
Create exactly docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md with the Browser-supplied exact bytes and no other Agent source change.

allowed_paths:
- docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md

non-goals:
- no AISCC runtime source change
- no test/rule/migration/canonical-state change
- no provider/LLM/network
- no scope expansion

repository:
exact project/repository/root/Commit-A base

execution provenance:
OWNER_SELF_DOGFOOD / AISCC_SELF_DOGFOOD
```

Dynamic bindings must come only from actual owner configuration:

```text
Genesis NextAction selection
P1-6 requirement/checkpoint refs
P1-7 Judgment policy/config
Human NOT_REQUIRED configuration
TaskConstraint/snapshot authority
```

Require TaskContract current before proceeding.

Record body ref/SHA, constraint ref, issuance event, owner snapshot.

# 13. deterministic materialization + inner Task placement

Call accepted `materialize_task_spec(...)`.

Require every materialized field equals the verified TaskContract/owner claims.

Record canonical spec bytes/hash.

Only after materialization, place the package inner Task byte-exact at:

```text
.aiassistant/tasks/active/20260914_2216_aiscc-p2-4-golden-agent-single-file-proof-change-2.md
```

Verify SHA `93600cafcade7e51495f6cea4f4797e6677b4e835231f19cced8d934ec5e8574`.

# 14. WorkRun READY

Use accepted self-dogfood READY entry.

Require:

```text
DecisionOutcome = ADMITTED
state = READY
state_version = 1
```

Record WorkRun and exact TransitionRequest/Decision.

No governed source edit before READY.

# 15. external IDE RUNNING

Use accepted external IDE start authority.

Issue one durable start permit bound to exact READY/v1, TaskContract, inner Task bytes, repository and Commit-A base.

Drive existing P1-4:

```text
READY -> RUNNING
```

Require:

```text
ADMITTED
state = RUNNING
state_version = 2
durable external start row verifies after restart/recomposition
```

No fake provider attempt.
No direct WorkRun write.
No source edit before RUNNING.

# 16. completion lease before edit

While repository is still clean at Governance Commit A and WorkRun is RUNNING/v2, issue the accepted one-time completion lease.

Bind expected hash:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
→ 7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
```

Raw capability remains private and is never exported.

Require clean exact base before editing.

# 17. execute exact governed Agent Task

Only now create exactly:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

with the inner Task's exact bytes.

Require:

```text
SHA-256 = 7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
git diff --check PASS
Agent source diff = exact one path
unauthorized Agent source diff count = 0
```

Do not commit yet.

# 18. trusted external completion

Complete through the accepted P1-5 external IDE completion repository and trusted LocalGitObserver.

Observer itself must prove:

```text
HEAD still Governance Commit A
changed path exact
target SHA exact
index expected
git diff --check PASS
no unauthorized path
stable observation
```

Persist immutable external submission and reconstruct the common issuer-verified `ExecutionSubmissionRef`.

Manual registration cannot substitute.

# 19. P1-6 actual execution evidence

Create actual EvidenceCandidate(s) only through existing owner/issuer APIs.

At minimum admitted evidence/satisfaction must bind:

```text
exact WorkRun
exact TaskContract id/version
exact external submission ref
inner Task SHA
changed path
target SHA
diff-check PASS
unauthorized count 0
checkpoint/requirement identity
```

No Agent assertion alone.

Restart/recompose once and prove historical external-producer verification.

# 20. actual structured NEXT_ACTION_CONTEXT evidence

For Cycle admission, issue an exact `NextActionContextRefV1` through the existing external Task authority for the current TaskContract.

Create/admit the required structured result through a production/source-owned P1-6 issuer path.

It must truthfully carry the exact `next_action_context` structure required by P1-8.

Forbidden:

```text
test-only issuer imported from tests.*
direct P1-6 row insert
fake admitted evidence
Browser Markdown as structured result
```

If the only available path is demonstrably test-only or fabricated, STOP with:

```text
GOLDEN_NEXT_ACTION_CONTEXT_EVIDENCE_GAP
```

# 21. deterministic Judgment + terminal ACCEPTED

Evaluate the exact evidence set through P1-6.

Require SATISFIED attestation.

Issue the configured P1-7 SYSTEM_DETERMINISTIC Judgment through owner APIs.

No HumanResult.

Drive the existing P1-4 terminal transition according to the actual transition matrix.

Golden terminal requirements:

```text
Judgment = ACCEPTED
WorkRun = ACCEPTED
all guard facts owner-issued
```

Do not guess intermediate state/version; follow source.

If another unimplemented authority is required:

```text
GOLDEN_AUTHORITY_GAP
```

STOP.

# 22. first real Cycle

After terminal WorkRun ACCEPTED, admit exactly one real P1-8 Cycle through `PostgresCycleAdmissionRepository` or the current equivalent owner API.

Cycle must bind:

```text
execution_mode = AISCC_SELF_DOGFOOD
orchestrator_commit = 621c1a374fe6ad42731c6249c68a39421eeda395
Genesis source NextAction
inner Task
TaskContract
WorkRun transition chain
external start
external submission
admitted evidence/satisfaction
Judgment
terminal TransitionDecision
structured NEXT_ACTION_CONTEXT provenance
```

No direct Cycle/memory row writes.

Require Cycle admission creates normal durable P1-8 memory/current context.

Then verify:

```text
Genesis currentness = DENY permanently
historical Genesis selection replay = PASS
```

# 23. exact result Git Commit B

Only after real Cycle admission.

Stage EXACTLY:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

Commit message exactly:

```text
docs(aiscc): prove first self dogfood golden cycle
```

Require:

```text
Commit B parent = Governance Commit A
changed paths = exact one
target SHA exact
index empty
tracked clean apart from expected Task lifecycle/report artifacts
```

Record result commit SHA.

# 24. resulting steady-state NextAction

After Commit B, use the actual owner-admitted Cycle/current memory lineage to select a new current P1-8 action.

Required mode:

```text
CYCLE_DERIVED
```

For continued TaskContract V1 self-dogfood, expected action:

```text
open-cycle-derived-task-issuance
```

Require owner verifier says current.

Do not relabel Genesis as Cycle-derived.
Do not overwrite a different valid owner-selected action.

If no truthful CYCLE_DERIVED action can be selected from the first Cycle:

```text
GOLDEN_NEXT_ACTION_UNAVAILABLE
```

STOP and do not claim golden candidate.

# 25. Task lifecycle

After complete terminal success, move inner Task active -> done byte-exact.

Move outer Task active -> done byte-exact.

Do not include either Task in result Commit B.

Expected terminal Git-visible untracked exactly:

```text
.aiassistant/tasks/done/20260914_2216_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-genesis-enabled-retry-1.md
.aiassistant/tasks/done/20260914_2216_aiscc-p2-4-golden-agent-single-file-proof-change-2.md
```

# 26. golden provenance export

Export sanitized owner-read records:

```text
GOLDEN_GENESIS.json
GOLDEN_TASKCONTRACT.json
GOLDEN_SPEC.json
GOLDEN_WORKRUN.json
GOLDEN_TRANSITIONS.json
GOLDEN_EXTERNAL_START.json
GOLDEN_EXTERNAL_SUBMISSION.json
GOLDEN_EVIDENCE.json
GOLDEN_JUDGMENT.json
GOLDEN_CYCLE.json
GOLDEN_NEXT_ACTION.json
GOLDEN_PROVENANCE.json
```

`GOLDEN_PROVENANCE.json` must bind exact IDs/hashes/refs for:

```text
SELF_DOGFOOD_GENESIS authority
source NextAction
inner Task path/SHA
TaskContract
WorkRun state/version chain
external start
completion lease/submission
EvidenceCandidate/admitted evidence/satisfaction
Judgment
first real Cycle
result Git commit
resulting CYCLE_DERIVED NextAction
```

Compute a canonical JSON SHA-256 root excluding the root field itself.

No raw capabilities, credentials or DB URL.

# 27. operational cleanup

Only after all runtime exports are written and hashed:

```text
remove exact Task-owned PostgreSQL container
remove its exact anonymous volume
remove Task-owned local credential helper if any
```

No Docker prune.

Cleanup failure is non-blocking residue unless it affects authority/security.

# 28. final verification

Require:

```text
target SHA exact
Commit B one path exact
git diff --check PASS
index empty
tracked clean

outer done Task SHA exact
inner done Task SHA exact
legacy 1400 unchanged
canonical state hashes unchanged
migration head remains 0012
Task-owned Docker residue = 0
```

# 29. prohibited

```text
product runtime source changes
test changes
migration/rule changes
canonical state changes
pytest/test fixtures as operational authority
tests.* imports
monkeypatch
direct owner-table writes
fake provider refs
fake predecessor Cycle/WorkRun/memory
Replay/Markdown current-authority substitution
source edit before RUNNING
completion lease after edit
provider/LLM/external network
push/deploy
```

# 30. export root

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
PREDECESSOR_ACCEPTANCE_VERIFICATION.md
GOLDEN_RUNTIME_SOURCE_AUDIT.md
GOLDEN_BOOTSTRAP_REVIEW.md
GOLDEN_GENESIS.json
GOLDEN_TASK_MATERIALIZATION.md
GOLDEN_TASKCONTRACT.json
GOLDEN_SPEC.json
GOLDEN_WORKRUN.json
GOLDEN_TRANSITIONS.json
GOLDEN_EXTERNAL_START.json
GOLDEN_EXTERNAL_SUBMISSION.json
GOLDEN_EVIDENCE.json
GOLDEN_JUDGMENT.json
GOLDEN_CYCLE.json
GOLDEN_NEXT_ACTION.json
GOLDEN_PROVENANCE.json
GOLDEN_PROVENANCE_ROOT.md
GIT_RESULT_REVIEW.md
POSTGRES_RUNTIME_EVIDENCE.md
CONTRACT_REVIEW.md
```

Also include current Cycle/Judgment, outer/inner done Tasks, exact target file and operational driver source.

# 31. named blockers

```text
BLOCKED_MISSING_ARTIFACT
DIRTY_WORKSPACE_MIXED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
GOLDEN_AUTHORITY_GAP
GOLDEN_EVIDENCE_INGRESS_UNAVAILABLE
GOLDEN_NEXT_ACTION_CONTEXT_EVIDENCE_GAP
GOLDEN_JUDGMENT_POLICY_UNAVAILABLE
GOLDEN_NEXT_ACTION_UNAVAILABLE
MIGRATION_BASELINE_MISMATCH
ISOLATED_POSTGRES_IMAGE_MISSING
BLOCKED_REQUIRED_EVIDENCE
SECURITY_BOUNDARY_BLOCKED
```

On blocker, preserve truthful evidence and do not create a false Cycle/NextAction/Commit B.

# 32. success ceiling

Complete PASS may report only:

```text
P2_4_FIRST_SELF_DOGFOOD_GOLDEN_CYCLE_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do NOT claim:

```text
P2-4 ACCEPTED/CLOSED
canonical state reconciled
Public Bounded Live released
competition submission complete
```

After Browser accepts the golden candidate, the next Task is P2-4 final acceptance/persistence/state reconciliation unless a concrete blocker remains.
