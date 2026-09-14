# 작업지시서: P2-4 first actual AISCC self-dogfood golden cycle — fresh IDE session

## meta

- task_id: `20260914_1916_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-fresh-ide-1`
- created_at: `2026-09-14T19:16:30+09:00`
- work_type: `ACTUAL_SELF_DOGFOOD_GOLDEN_CYCLE + GOVERNANCE_RUNTIME + SINGLE_FILE_AGENT_CHANGE + GIT_PERSISTENCE`
- evidence_profile: `CRITICAL_GOLDEN`
- execution_mode: `MANUAL_COMMAND_CENTER_OUTER / AISCC_SELF_DOGFOOD_INNER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `6eedc50c567f552a3b9d2902c95bd71a99ca441f`
- required_parent: `0d53871453b20dc33bc214b213d1600cedaa8a7e`
- predecessor_result_zip_sha256: `7fd52ec0b9267e5f3c2634910ad45c1e0f66963f2cd1440d6ae329bfc6405ab8`
- predecessor_done_task_sha256: `3dfab04006828711694baee32ece5628eec513ca39a6b4ccd6cf5e42f29d5816`
- predecessor_judgment: `ACCEPTED / P2_4_EXTERNAL_IDE_EXECUTION_START_IMPLEMENTATION_CANDIDATE`
- migration_head: `20260914_0011`
- fresh_IDE_chat_required: `Yes`
- governance_commit_authorized: `Yes / exact 4 paths / Commit A`
- real_self_dogfood_Task_authorized: `Yes / exact supplied inner Task`
- real_local_WorkRun_authorized: `Yes / exact one golden run`
- real_repository_Agent_change_authorized: `Yes / exact one file`
- real_evidence_judgment_cycle_nextaction_authorized: `Yes / exact golden lineage`
- result_commit_authorized: `Yes / exact one source file / Commit B`
- canonical_state_mutation_authorized: `No`
- product_runtime_source_mutation_authorized: `No`
- migration_mutation_authorized: `No`
- provider_LLM_authorized: `No`
- external_network_authorized: `No`
- retained_private_DB_authorized: `No`
- Docker_authorized: `Yes / local postgres:17.6 operational golden runtime only`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_FIRST_SELF_DOGFOOD_GOLDEN_CYCLE_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. fresh IDE session

This Task MUST begin in a new IDE Executor chat.

Read:

```text
20260914_1916_aiscc-ide-executor-fresh-session-p2-4-actual-golden-cycle-handoff-1.md
```

after the outer Task-first transport step.

Do not rely on the old IDE chat's conversational memory.

Repository/source/canonical artifacts and this package are authority.

# 1. predecessor acceptance

Browser accepts 1803:

```text
ACCEPTED
/ P2_4_EXTERNAL_IDE_EXECUTION_START_IMPLEMENTATION_CANDIDATE
```

Independent verified result:

```text
ZIP SHA-256:
7fd52ec0b9267e5f3c2634910ad45c1e0f66963f2cd1440d6ae329bfc6405ab8

63 members
62 manifest rows
CRC PASS
62/62 size+SHA exact

tests:
405 PASS / 0 FAIL / 0 ERROR / 0 SKIP

migration:
20260914_0011 PASS

Result Commit:
6eedc50c567f552a3b9d2902c95bd71a99ca441f

parent:
0d53871453b20dc33bc214b213d1600cedaa8a7e

message:
feat(aiscc): add external ide execution start authority

changed paths:
exact 13
```

Accepted external IDE chain:

```text
READY
→ durable start permit
→ G_EXECUTION_STARTED
→ RUNNING
→ durable completion lease
→ trusted Git observation
→ durable external submission
→ G_EXECUTOR_SUBMISSION
→ P1-6 producer verification
```

# 2. accepted evidence

Package hashes:

- `COMPLETION_CONTINUITY_REVIEW.md`: `c850219a347e2fc098d1add4a4dc1f7c702f485ca09bf9fe7d49f4466198e88b`
- `CONTRACT_REVIEW.md`: `494e1f8db0009ee79021010433af52fc062c46afc2417e2aa6d8263f081f72d6`
- `EXECUTOR_REPORT.md`: `d9704d6811d347251e7b4ddf4eb6b3e7106bb838888d6928a0e8b9b2cbaeda14`
- `EXTERNAL_IDE_START_AUTHORITY_REVIEW.md`: `30caa00079b61e5cda27ab66c6c6c3206a1c663f2f457f006f341b2d4c3cd891`
- `MIGRATION_REVIEW.md`: `8c9575892ce69ad562a47f1b5b11e367c88630c46390d8f0187b184a0a33c05c`
- `P1_4_START_HANDOFF_REVIEW.md`: `7002582c2abfee34dad9928757c0edb0718d13738afe0de48ecedc0cec67220b`
- `POSTGRES_RUNTIME_EVIDENCE.md`: `6e21edcea3d726767ab575262b00d364110f90cd092fa55fc8f3d51b36c7fcfc`
- `START_AUTHORITY_SOURCE_AUDIT.md`: `ec5f672910b620b08dae0a085fb2bb9f039f7a2146bbbe4082111fa383187b5f`
- `STATIC_CHECKS.md`: `17ceb9753bdb3555df39e53631908ac04174d89a768ed0929759f836ff5dfeb3`
- `TEST_RESULTS.md`: `71bc77b0bb0a2bab2d3bfd060ed96772aa8aa105d7d07c0f7ad26115672d02dc`
- `WORKSPACE_VERIFICATION.md`: `89cfc2f4f003caaf046a14a24dd361491565f05cf8264c40b918fdd1313f68c6`
- `evidence/COMMIT_A.json`: `e718276fff1793f29bb0b7b5064582346d3dcb4c98d3853bfe7f6cf211945da4`
- `evidence/COMMIT_B.json`: `837521b3287ecd8fcb6a0a1a0785efcd9a72d1e40c50b78d2ed8c232e124193f`
- `evidence/FINAL_BYTE_STATIC.json`: `9d5b4c8cee4c97d42cc70e26d5387eabe345e75c9322ad25161921d29cb596b7`
- `evidence/TERMINAL_WORKSPACE.json`: `91222dd85865a4fa2b1dec6c1afbe7e8f6653a2b1c75cd919bcbdb581623e733`
- `evidence/TEST_SUMMARY.json`: `689ba1dab5ba6e62dc296d01772f935be4b11077684f670b8e6d705382c3c37e`

After outer Task-first read, copy these only into:

```text
.aiassistant/reports/target/20260914_1916_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-fresh-ide-1/accepted-input/
```

Any mismatch:

```text
BLOCKED_MISSING_ARTIFACT
```

STOP.

# 3. exact inner golden Task

Package member:

```text
20260914_1916_aiscc-p2-4-golden-agent-single-file-proof-change-1.md
```

Expected SHA-256:

```text
c83505fcacbecea42aa769b3caac56fb84a11783205769e76347e8f515cad059
```

Governed Agent source path:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

Expected target SHA-256:

```text
7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
```

The inner Task is Browser/External-Task-Authority authored provenance/instruction.
The durable TaskContract remains system authority.

Any byte mismatch -> STOP.

# 4. exact repository preflight

Require before Governance Commit A:

```text
branch:
main

HEAD:
6eedc50c567f552a3b9d2902c95bd71a99ca441f

HEAD^:
0d53871453b20dc33bc214b213d1600cedaa8a7e

index:
empty

tracked:
clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1803_aiscc-p2-4-external-ide-execution-start-authority-implementation-1.md
```

Done Task SHA:

```text
3dfab04006828711694baee32ece5628eec513ca39a6b4ccd6cf5e42f29d5816
```

Target file MUST NOT exist:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

Inner golden Task MUST NOT exist in canonical active/done Task directories.

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
20260914_0011
```

No migration mutation.

Mismatch -> fail closed.

# 5. fixed executables

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

# 6. outer transport + Governance Commit A

Order:

```text
verify delivery ZIP/hash/archive/path safety
→ place OUTER current Task into .aiassistant/tasks/active
→ read OUTER Task
→ read fresh-session HANDOFF
→ verify repository preflight
→ verify inner golden Task bytes
→ verify predecessor accepted evidence
→ place current Cycle/Judgment/Handoff
```

Canonical outer artifacts:

```text
20260914_1916_aiscc-p2-4-external-ide-start-accepted-actual-golden-cycle-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_1916_aiscc-p2-4-external-ide-start-final-acceptance-golden-cycle-authorization-1.md
-> .aiassistant/reports/aiscc/

20260914_1916_aiscc-ide-executor-fresh-session-p2-4-actual-golden-cycle-handoff-1.md
-> .aiassistant/reports/aiscc/
```

Stage EXACTLY:

```text
.aiassistant/tasks/done/20260914_1803_aiscc-p2-4-external-ide-execution-start-authority-implementation-1.md
.aiassistant/records/aiscc/cycles/20260914_1916_aiscc-p2-4-external-ide-start-accepted-actual-golden-cycle-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_1916_aiscc-p2-4-external-ide-start-final-acceptance-golden-cycle-authorization-1.md
.aiassistant/reports/aiscc/20260914_1916_aiscc-ide-executor-fresh-session-p2-4-actual-golden-cycle-handoff-1.md
```

Commit message exactly:

```text
docs(aiscc): accept external ide start and enter golden cycle
```

Require:

```text
Commit A parent = 6eedc50c567f552a3b9d2902c95bd71a99ca441f
changed paths = exact 4
index empty
tracked clean
Git-visible untracked = 0
```

Record Commit A as exact `repository_binding.base_commit` for the golden TaskContract.

# 7. actual-vs-test boundary

This is operational runtime, NOT pytest proof.

Forbidden for golden authority construction:

```text
imports from tests.*
pytest fixtures
monkeypatch
direct INSERT/UPDATE/DELETE into owner tables
manual construction of fake owner rows
manual register_start/register_submission as external authenticity
Replay relabeled current
test PASS relabeled actual WorkRun
```

A Task-owned operational driver MAY exist only under:

```text
.aiassistant/reports/target/20260914_1916_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-fresh-ide-1/runtime/
```

It must not be committed.

The driver may call private binders only where this Browser Task explicitly acts for the trusted external Command Center/P1-5 composition owner.

It may not expose those private writers in product APIs.

# 8. isolated actual runtime

Require local image:

```text
postgres:17.6
```

No pull.

Create exactly one Task-owned operational PostgreSQL container, e.g.:

```text
aiscc-p2-4-golden-1916-pg
```

Requirements:

```text
PostgreSQL 17.6
loopback-only
synthetic credentials
no host bind
empty operational DB
upgrade to 20260914_0011
```

This is the actual local golden runtime, not a pytest database.

Do not run pytest against this DB to manufacture authority.

# 9. source audit before authority creation

Before creating operational rows, inspect current source-owned APIs for:

```text
P1-8 project/current NextAction bootstrap
cycle-derived selection/currentness
P1-6 requirement-definition registration
P1-7 deterministic Judgment policy registration
TaskContract issuance
SelfDogfoodTaskSpec materialization
READY entry
ExternalIdeExecutionStartRepository
ExternalIdeExecutionRepository completion
EvidenceCandidate admission/satisfaction
terminal P1-4 transition
Cycle admission
resulting NextAction refresh/selection
```

Create:

```text
GOLDEN_RUNTIME_SOURCE_AUDIT.md
```

If a required real golden owner API does not exist or would require fabricated authority:

```text
GOLDEN_AUTHORITY_GAP
```

STOP truthfully before crossing that boundary.

Do not implement new product source in this Task.

# 10. authoritative current NextAction bootstrap

Establish/load exactly one genuine current P1-8 selection using existing owner APIs only.

Required selected action for TaskContract Durable Body V1:

```text
open-cycle-derived-task-issuance
```

The source must be a genuine cycle-derived owner lineage.

Use current Command Center NEXT_ACTION_CONTEXT plus existing P1-8 owner APIs to bind:

```text
project = this AISCC repository
phase = P2-4 actual self-dogfood golden cycle
repository_root = C:\Users\oracl\IdeaProjects\ai-software-command-center
base_commit = Governance Commit A
requested action class = task issuance
execution_mode = AISCC_SELF_DOGFOOD
```

Historical Replay/Markdown alone is not current authority.

If the exact owner requires a current admitted predecessor Cycle, use only an actual owner-admitted accepted Cycle through existing P1-8 APIs.

No silent operational-recovery translation.

Require:

```text
selected action = open-cycle-derived-task-issuance
current by P1-8 verifier
owner-recognized descriptor/source/policy
```

Otherwise:

```text
SELF_DOGFOOD_BOOTSTRAP_AUTHORITY_MISSING
```

STOP.

# 11. P1-6 requirement definition

Register/create exact current P1-6 requirement graph using existing owner APIs.

The golden evidence must prove at minimum:

```text
inner Task SHA = c83505fcacbecea42aa769b3caac56fb84a11783205769e76347e8f515cad059
WorkRun identity
changed path = docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
target file SHA = 7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
git diff --check = PASS
unauthorized Agent source diff count = 0
execution submission belongs to exact external IDE WorkRun/TaskContract
```

Use an existing accepted EvidenceProfile/checkpoint and producer contract.

Human evidence is NOT allowed.

Graph must be durable/current and TaskContract-resolvable.

If current owner APIs cannot express the exact requirements:

```text
GOLDEN_EVIDENCE_INGRESS_UNAVAILABLE
```

STOP.

# 12. P1-7 deterministic Judgment policy

Register existing Judgment owner configuration for the exact golden accepted path.

Required intent:

```text
owner_policy = SYSTEM_DETERMINISTIC
human = NOT_REQUIRED
accepted outcome requires satisfied P1-6 evidence
target = ACCEPTED
```

Use existing policy fields and deterministic/evidence basis refs.

No fake HumanResult.

If current source cannot represent this path:

```text
GOLDEN_JUDGMENT_POLICY_UNAVAILABLE
```

STOP.

# 13. actual durable TaskContract

Issue exactly one V1 TaskContract through the existing trusted external Task-authority writer.

Fixed semantic content:

```text
task_id:
20260914_1916_aiscc-p2-4-golden-agent-single-file-proof-change-1

contract_id:
aiscc-p2-4-golden-cycle-1

contract_version:
1

goal:
Create exactly docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md with the Browser-supplied exact bytes and no other Agent source change.

non_goals:
- no AISCC runtime source change
- no test change
- no migration change
- no canonical state change
- no rule change
- no provider/LLM/network
- no scope expansion

allowed_paths:
- docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md

repository_root:
C:\Users\oracl\IdeaProjects\ai-software-command-center

base_commit:
Governance Commit A

runtime_mode:
OWNER_SELF_DOGFOOD

cycle_execution_mode:
AISCC_SELF_DOGFOOD

orchestrator_commit:
6eedc50c567f552a3b9d2902c95bd71a99ca441f
```

Dynamic owner-derived fields must come exactly from current owner authorities:

```text
project_id
source_next_action
repository_id
evidence binding
Human config/selector
Judgment policies/config
additional authority_refs if required
```

No Agent choice for those fields.

Verify current TaskContract before proceeding.

Record:

```text
body_ref
body_sha256
constraint_ref
issuance event
snapshot ref/hash
```

# 14. deterministic materialization + inner Task provenance

Call accepted:

```text
materialize_task_spec(...)
```

Require every spec field equals the verified current TaskContract/body/owner claims.

Record canonical spec bytes/hash.

Then place the package inner Task byte-exact at:

```text
.aiassistant/tasks/active/20260914_1916_aiscc-p2-4-golden-agent-single-file-proof-change-1.md
```

Verify SHA:

```text
c83505fcacbecea42aa769b3caac56fb84a11783205769e76347e8f515cad059
```

Markdown Task remains provenance/instruction only.

# 15. WorkRun READY

Use accepted self-dogfood READY entry.

Require:

```text
DecisionOutcome.ADMITTED
state = READY
state_version = 1
```

Record exact:

```text
work_run_id
READY transition_request_id
TransitionDecision
TaskContract identity/version
spec hash
```

No Agent source edit before READY.

# 16. external IDE start permit + RUNNING

Use accepted `ExternalIdeExecutionStartRepository`.

Issue one durable start permit in a caller-owned transaction for exact READY/v1:

```text
receipt = current TaskContract receipt
work_run_id = golden WorkRun
state_version = 1
ready_transition_id = actual READY transition
inner_task_bytes = exact package Task bytes
```

Raw start capability must remain private and never enter exported evidence.

Build the exact existing P1-4 READY→RUNNING request required by current source.

Call accepted external start composition.

Require:

```text
P1-4 decision ADMITTED
state = RUNNING
state_version = 2
durable external start row exists
restart resolver verifies it
```

No direct WorkRun write.

No provider attempt.

No source edit before RUNNING.

# 17. issue completion lease BEFORE Agent edit

While repository still clean at Governance Commit A and WorkRun is RUNNING/v2, use accepted `ExternalIdeExecutionRepository` trusted writer to issue the one-time completion lease.

Bind:

```text
current TaskContract
golden work_run_id
state_version = 2
actual start_transition_id
exact inner_task_bytes
expected_hashes:
  docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md = 7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
```

Require:

```text
clean exact base = Governance Commit A
lease durable/current
raw completion capability private
```

Do not edit the governed file before lease issuance.

# 18. execute exact governed Agent Task

Only now:

- read canonical active inner Task;
- create exactly:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

with exact bytes in the package;
- do not change any other source/config/test/document path.

Require:

```text
SHA-256 = 7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
git diff --check PASS
Agent source diff = exact one path
unauthorized Agent source diff count = 0
```

Do not commit.

# 19. trusted external completion

Complete through accepted P1-5 external IDE repository using:

```text
durable lease
private capability
trusted LocalGitObserver
```

Require the trusted observer itself proves:

```text
HEAD still Governance Commit A
changed paths exact
target SHA exact
index exact expected
git diff --check PASS
no unauthorized path
stable double observation
```

Persist immutable external submission.

Resolve/reconstruct issuer-verified common `ExecutionSubmissionRef`.

Manual `register_submission` is not authenticity.

# 20. P1-6 EvidenceCandidate + admission/satisfaction

Use existing P1-6 external-producer issuer path.

Create actual EvidenceCandidate from the verified durable external submission.

Admit through existing P1-6 owner APIs.

Required admitted evidence/satisfaction must bind:

```text
exact work_run_id
TaskContract id/version
execution submission ref
Task SHA
changed path
target SHA
diff-check PASS
unauthorized count 0
requirement/checkpoint identity
```

No direct DB writes.

No Agent assertion alone.

Use historical verifier once after restart/recomposition as part of golden proof.

# 21. Judgment and terminal WorkRun

Follow exact current P1-4/P1-7 transition matrix.

Do not guess state sequence.

Golden terminal requirements:

```text
P1-6 admitted evidence
P1-6 requirement/checkpoint satisfaction
SYSTEM_DETERMINISTIC Judgment = ACCEPTED
P1-4 terminal WorkRun state = ACCEPTED
no HumanResult
```

Every transition must use existing owner facts.

Record requests/evaluations/decisions in order.

If an unimplemented/fabricated authority would be needed:

```text
GOLDEN_AUTHORITY_GAP
```

STOP; preserve uncommitted target if already edited.

# 22. actual Cycle admission

After terminal WorkRun ACCEPTED, admit exactly one P1-8 Cycle through existing owner APIs.

Cycle provenance must bind at minimum:

```text
execution_mode = AISCC_SELF_DOGFOOD
orchestrator_commit = 6eedc50c567f552a3b9d2902c95bd71a99ca441f
source NextAction
Task
TaskContract
WorkRun
external start
external submission
admitted evidence/satisfaction
Judgment
terminal TransitionDecision
```

Markdown Cycle files are not P1-8 Cycle authority.

Record durable Cycle id/ref/fingerprint/revision.

# 23. exact result Git Commit B

Only after terminal ACCEPTED + actual Cycle admission.

Stage EXACTLY:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

Do not stage:

```text
inner/outer Task
runtime reports
DB artifacts
canonical state
governance files already committed in Commit A
```

Commit message exactly:

```text
docs(aiscc): prove first self dogfood golden cycle
```

Require:

```text
Commit B parent = Governance Commit A
changed paths = exact one
target content SHA exact
index empty
tracked clean except explicit Task lifecycle/report artifacts
```

Record result commit SHA.

# 24. resulting authoritative NextAction

After Commit B, update/refresh only through existing P1-8 owner APIs with actual golden Cycle and result base commit.

Require resulting current selection provenance includes:

```text
actual golden Cycle
repository base_commit = Commit B
current context
```

For continued V1 self-dogfood, expected supported selected action is:

```text
open-cycle-derived-task-issuance
```

Do not overwrite a different valid owner-selected action.

If final current action is not supported by TaskContract V1:

```text
GOLDEN_NEXT_ACTION_UNSUPPORTED_BY_V1
```

report truthfully and do not claim complete candidate.

# 25. inner/outer Task lifecycle

After successful terminal ACCEPTED, Cycle, Commit B and resulting NextAction:

move inner Task byte-exact:

```text
.aiassistant/tasks/active/20260914_1916_aiscc-p2-4-golden-agent-single-file-proof-change-1.md
→ .aiassistant/tasks/done/20260914_1916_aiscc-p2-4-golden-agent-single-file-proof-change-1.md
```

Move current outer Task active→done byte-exact.

Do not commit either in Commit B.

Expected terminal Git-visible untracked exactly:

```text
.aiassistant/tasks/done/20260914_1916_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-fresh-ide-1.md
.aiassistant/tasks/done/20260914_1916_aiscc-p2-4-golden-agent-single-file-proof-change-1.md
```

# 26. golden provenance export

Export sanitized actual owner-read records:

```text
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

`GOLDEN_PROVENANCE.json` must contain exact IDs/hashes/refs for:

```text
execution_mode
orchestrator_commit
source NextAction
inner Task path/SHA
TaskContract
WorkRun full state/version chain
external start permit/start ref
completion lease/submission ref
EvidenceCandidate / admitted evidence / satisfaction
Judgment
Cycle
result Git commit
resulting NextAction
```

Compute:

```text
golden_provenance_root =
SHA256(canonical JSON bytes of GOLDEN_PROVENANCE.json excluding the root field)
```

No invented fields.

No secrets/capability tokens.

# 27. operational DB cleanup

Only after all required runtime exports are written and hashed:

```text
remove exact Task-owned PostgreSQL container
remove exact Task-owned anonymous volume
remove credential helper/env file if any
```

No Docker prune.

Cleanup failure is nonblocking residue unless security/correctness is affected.

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
migration head remains 0011
Task-owned Docker residue = 0
```

# 29. prohibited

```text
product runtime source changes
test changes
migration changes
rule changes
canonical state changes
pytest/test fixture as actual authority
tests.* imports in operational driver
monkeypatch
direct owner-table writes
fake provider refs
manual start/submission registration as authenticity
source edit before RUNNING
completion lease after edit
provider/LLM/network
push/deploy
```

# 30. result export

Target:

```text
.aiassistant/reports/target/20260914_1916_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-fresh-ide-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
PREDECESSOR_ACCEPTANCE_VERIFICATION.md
GOLDEN_RUNTIME_SOURCE_AUDIT.md
GOLDEN_BOOTSTRAP_REVIEW.md
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

Also include:

```text
outer done Task
inner done Task
current Cycle/Judgment/Handoff
exact target file
operational driver source under runtime/
```

No credentials/capability token/raw DB dump/private DB URL.

Result ZIP:

```text
.aiassistant/reports/target/20260914_1916_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-fresh-ide-1.zip
```

# 31. named blockers

```text
BLOCKED_MISSING_ARTIFACT
DIRTY_WORKSPACE_MIXED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
SELF_DOGFOOD_BOOTSTRAP_AUTHORITY_MISSING
GOLDEN_AUTHORITY_GAP
GOLDEN_EVIDENCE_INGRESS_UNAVAILABLE
GOLDEN_JUDGMENT_POLICY_UNAVAILABLE
GOLDEN_NEXT_ACTION_UNSUPPORTED_BY_V1
MIGRATION_BASELINE_MISMATCH
ISOLATED_POSTGRES_IMAGE_MISSING
BLOCKED_REQUIRED_EVIDENCE
SECURITY_BOUNDARY_BLOCKED
```

On blocker:

- no false golden success claim;
- no fake Cycle/NextAction;
- no Result Commit B unless actual terminal ACCEPTED + Cycle occurred;
- preserve truthful runtime/source evidence;
- no broad reset/clean.

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
