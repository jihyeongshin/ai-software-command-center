# 작업지시서: P2-4 first actual AISCC self-dogfood golden cycle

## meta

- task_id: `20260914_1635_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-1`
- created_at: `2026-09-14T16:35:00+09:00`
- work_type: `ACTUAL_SELF_DOGFOOD_GOLDEN_CYCLE + GOVERNANCE_RUNTIME + SINGLE_FILE_AGENT_CHANGE + GIT_PERSISTENCE`
- evidence_profile: `CRITICAL_GOLDEN`
- execution_mode: `MANUAL_COMMAND_CENTER_OUTER / AISCC_SELF_DOGFOOD_INNER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `40bc4f8e2a9e10b42531441c1a4ee92c59bef963`
- required_parent: `d6d564050deba6cbd064aaa6bf9813a55fca5dae`
- predecessor_result_zip_sha256: `c267429082a2dc5bd4e41677dc021248a18d683db1510628c7e33cb0dac7a56e`
- predecessor_done_task_sha256: `e9ca59b427856edf8324f9e1370620268cbc959938233c85d2b33125adbb03d0`
- predecessor_judgment: `ACCEPTED / P2_4_SELF_DOGFOOD_ENTRY_SOURCE_CANDIDATE`
- source_candidate_commit: `40bc4f8e2a9e10b42531441c1a4ee92c59bef963`
- fresh_IDE_chat_required: `No`
- governance_commit_authorized: `Yes / exact 3 paths / Commit A`
- real_self_dogfood_Task_authorized: `Yes / exact supplied golden Task`
- real_local_WorkRun_authorized: `Yes / exact one golden run`
- real_repository_source_change_authorized: `Yes / exact one file`
- real_evidence_judgment_cycle_nextaction_authorized: `Yes / exact golden lineage`
- result_commit_authorized: `Yes / exact one source file / Commit B`
- canonical_state_mutation_authorized: `No`
- product_source_mutation_authorized: `No`
- migration_mutation_authorized: `No`
- provider_LLM_authorized: `No`
- external_network_authorized: `No`
- retained_private_DB_authorized: `No`
- Docker_authorized: `Yes / local postgres:17.6 operational golden runtime only`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_FIRST_SELF_DOGFOOD_GOLDEN_CYCLE_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. predecessor source-candidate acceptance

Browser independently accepts 1607 as:

```text
ACCEPTED
/ P2_4_SELF_DOGFOOD_ENTRY_SOURCE_CANDIDATE
```

Verified predecessor:

```text
result ZIP:
c267429082a2dc5bd4e41677dc021248a18d683db1510628c7e33cb0dac7a56e

members:
50

manifest rows:
49

CRC:
PASS

manifest:
49/49 size + SHA exact

candidate tests:
45 PASS / 0 FAIL / 0 SKIP

direct regressions:
137 PASS / 0 FAIL / 0 SKIP

Ruff / compile / diff-check:
PASS

source Commit B:
40bc4f8e2a9e10b42531441c1a4ee92c59bef963

parent:
d6d564050deba6cbd064aaa6bf9813a55fca5dae

message:
feat(aiscc): add self dogfood task materializer

changed paths:
exact 5 allowed self_dogfood source/test paths
```

No existing semantic-owner source was changed.

# 1. exact supplied inner golden Task

Package member:

```text
20260914_1635_aiscc-p2-4-golden-agent-single-file-proof-change-1.md
```

Expected SHA-256:

```text
de5269e5587f0fe99edbeeaeafa379702cdbffc452239413c6250ffde69b7966
```

Target governed Agent source path:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

Expected target SHA-256:

```text
7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
```

The inner Task bytes are Browser/External-Task-Authority authored.
They are human-readable provenance, not a substitute for the durable TaskContract.

Any byte mismatch:

```text
BLOCKED_MISSING_ARTIFACT
```

STOP.

# 2. predecessor accepted evidence

Package hashes:

- `CONTRACT_REVIEW.md`: `05cd64a6a14a33ed1fdcb9f8d2007245b177530146cc58e8dc66c7ad17cb7a2c`
- `EXECUTOR_REPORT.md`: `5d09c0c523e7718d604e8c6a1233bba407c502894a46c69ad1f998e016ba2698`
- `POSTGRES_RUNTIME_EVIDENCE.md`: `662b66caf98af79a599d1e101ba4acc93bdb4bc518bd94cb7aca511fa0f4c311`
- `PREDECESSOR_ACCEPTANCE_VERIFICATION.md`: `04a39ad50bfe5010a593a67bada0778be5dead05d374c3cbcae85a11acd53a80`
- `READY_ENTRY_REVIEW.md`: `df300d118cce275b625a7e1a6cead62e742023ba5931bda6004319e598b3a9ab`
- `SELF_DOGFOOD_SPEC_REVIEW.md`: `6cf5d65f8847797c70285b0a776cfd9d1f80c2c0a3172ce03efc2f7d9649a281`
- `SOURCE_AUTHORITY_REVIEW.md`: `acecf31fc3f8eafa908f239a8d42b28ff81761c035d6f3874909bf19f8ff0e35`
- `STATIC_CHECKS.md`: `f0b6d06896ef8c6466df9f809dfe2ba3f6e8831ca23adb87038d7e730e8901fc`
- `TEST_RESULTS.md`: `4970c03d4db44d5ce80bd94cb851ae10656eb7e3f8eaca02f1a78dc89d5213ab`
- `WORKSPACE_VERIFICATION.md`: `4ee438fa9bfd6feeba82743d2995fea9df01db3a8dc4640235033fa6612d196f`
- `evidence/COMMIT_A.json`: `fd33369754f488c76d4b5329b1a289b8ab414ad30ba3c508bc78ad6b75fa793b`
- `evidence/COMMIT_B.json`: `3e2e7bdc3f000d7715cb3a73c7511eefb88d3e962a8a68329ba741349da089d4`
- `evidence/TERMINAL_WORKSPACE.json`: `6fcdf7567bb321525562669034d9a10fb410052591d8f60b62cb3f5ae350be7b`
- `evidence/TEST_SUMMARY.json`: `2e9f44cc8b2b919650ae6812846a8d6b73fe0712609b30065a858843142ce878`

After outer Task-first read, copy only into:

```text
.aiassistant/reports/target/20260914_1635_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-1/accepted-input/
```

Mismatch -> `BLOCKED_MISSING_ARTIFACT`.

# 3. exact repository preflight

Require:

```text
branch:
main

HEAD:
40bc4f8e2a9e10b42531441c1a4ee92c59bef963

HEAD^:
d6d564050deba6cbd064aaa6bf9813a55fca5dae

index:
empty

tracked:
clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1607_aiscc-p2-4-self-dogfood-task-materializer-ready-entry-source-candidate-1.md
```

SHA:

```text
e9ca59b427856edf8324f9e1370620268cbc959938233c85d2b33125adbb03d0
```

Target file MUST NOT already exist:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

Inner golden Task MUST NOT already exist in canonical active/done Task directories.

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
20260914_0009
```

No new migration.

Mismatch -> fail closed.

# 4. fixed executables

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

# 5. outer transport + Governance Commit A

Order:

```text
verify delivery ZIP/hash/archive/path safety
→ place OUTER current Task into .aiassistant/tasks/active
→ read OUTER Task
→ verify repository preflight
→ verify inner golden Task bytes
→ verify predecessor accepted evidence
→ place current outer Cycle/Judgment
```

Canonical outer governance artifacts:

```text
20260914_1635_aiscc-p2-4-self-dogfood-source-candidate-accepted-golden-cycle-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_1635_aiscc-p2-4-self-dogfood-source-candidate-final-acceptance-golden-cycle-authorization-1.md
-> .aiassistant/reports/aiscc/
```

Stage exactly:

```text
.aiassistant/tasks/done/20260914_1607_aiscc-p2-4-self-dogfood-task-materializer-ready-entry-source-candidate-1.md
.aiassistant/records/aiscc/cycles/20260914_1635_aiscc-p2-4-self-dogfood-source-candidate-accepted-golden-cycle-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_1635_aiscc-p2-4-self-dogfood-source-candidate-final-acceptance-golden-cycle-authorization-1.md
```

Commit exactly:

```text
docs(aiscc): accept self dogfood entry source candidate
```

Require:

```text
Commit A parent = 40bc4f8e2a9e10b42531441c1a4ee92c59bef963
changed paths = exact 3
index empty
tracked clean
Git-visible untracked = 0
```

Record Commit A as the exact repository base for the inner golden TaskContract.

# 6. actual-vs-test boundary

This golden cycle is an operational repository run, NOT pytest fixture proof.

Forbidden for golden authority construction:

```text
imports from tests.*
pytest fixtures
monkeypatch
direct INSERT/UPDATE/DELETE into owner tables
manual construction of fake owner rows
relabeling Replay as current authority
claiming test PASS as golden WorkRun
```

A Task-owned operational driver MAY be created only under:

```text
.aiassistant/reports/target/20260914_1635_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-1/runtime/
```

It is not product source and must not be committed.

The driver may use existing source-owned composition APIs, including the private external Task-authority binder solely because this Browser Task explicitly acts for `EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY`.

It may not expose or add that private writer to product APIs.

# 7. isolated actual golden runtime

First:

```text
docker image inspect postgres:17.6
```

If absent:

```text
ISOLATED_POSTGRES_IMAGE_MISSING
```

No pull.

Create exactly one Task-owned operational PostgreSQL container, e.g.:

```text
aiscc-p2-4-golden-1635-pg
```

Requirements:

```text
postgres:17.6
loopback-only
synthetic credentials
no host bind
empty DB
upgrade to 20260914_0009
```

This DB is the real local runtime for the golden operation, not a pytest database.

Do not run pytest against this DB to manufacture golden state.

# 8. bootstrap/current NextAction authority

Before TaskContract issuance, establish or load ONE genuine current P1-8 NextAction selection using existing owner APIs only.

Preferred bootstrap authority is:

```text
current Browser/Command-Center NEXT_ACTION_CONTEXT
+ existing enrolled POLICY_ACTION_CATALOG
+ existing P1-8 source/descriptor/policy authority
```

Context must bind at minimum:

```text
project = this AISCC repository
phase = P2-4 self-dogfood golden cycle
repository_root = C:\Users\oracl\IdeaProjects\ai-software-command-center
base_commit = Governance Commit A
requested action class = task issuance
```

If the exact P1-8 source requires a previously admitted real Cycle, you MAY use an existing canonical P2-3 accepted runtime Cycle/replay only through the existing owner admission/currentness APIs.

You MUST NOT treat a Markdown/replay record as current authority merely because it exists.

Require final current selection:

```text
action_ref / descriptor:
owner-recognized

selected action:
open-cycle-derived-task-issuance

current:
true by P1-8 verifier
```

If no legitimate current selection can be established from existing accepted owners:

```text
SELF_DOGFOOD_BOOTSTRAP_AUTHORITY_MISSING
```

STOP.

Do not invent a bootstrap source kind or weaken P1-8.

# 9. actual P1-6 evidence-definition authority

Before TaskContract issuance, create/register an exact P1-6 definition graph using existing owner APIs.

The golden requirement set must require owner-authenticated evidence for:

```text
inner golden Task identity/hash
golden WorkRun identity
exact governed changed path = docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
target SHA-256 = 7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
git diff --check PASS
no unauthorized source diff
```

Use an existing accepted evidence profile/checkpoint suitable for executor source-change completion.

Human evidence is NOT allowed.

The graph must be durable/current and must be verifiable by the accepted TaskContract P1-6 definition resolver.

If no existing source-owned evidence profile/producer ingress can represent a real IDE Executor source-change submission without fabricating authority:

```text
GOLDEN_EVIDENCE_INGRESS_UNAVAILABLE
```

STOP.

Do not invent a new EvidenceProfile/checkpoint/producer type.

# 10. actual judgment policy

Register existing P1-7/Judgment owner configuration for the exact golden completion path.

Required semantic intent:

```text
owner_policy:
SYSTEM_DETERMINISTIC

human:
NOT_REQUIRED

accepted outcome:
requires satisfied P1-6 evidence

target:
ACCEPTED
```

Use only existing policy fields/matrix uses.

No fake HumanResult.

If existing source does not support this exact non-Human accepted path:

```text
GOLDEN_JUDGMENT_POLICY_UNAVAILABLE
```

STOP.

# 11. actual TaskContract body

Issue exactly one durable V1 TaskContract through the existing external Task-authority writer.

Fixed Browser-authored semantic body:

```text
task_id:
20260914_1635_aiscc-p2-4-golden-agent-single-file-proof-change-1

contract_id:
aiscc-p2-4-golden-cycle-1

contract_version:
1

goal:
Create exactly docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md with the Browser-supplied exact bytes and no other Agent source change.

non_goals:
- no AISCC runtime code change
- no test change
- no migration change
- no canonical state change
- no rule change
- no provider/LLM/network
- no scope expansion

allowed_paths:
- docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md

forbidden_paths:
- every repository path except the exact allowed path for the governed Agent source change

repository_root:
C:\Users\oracl\IdeaProjects\ai-software-command-center

base_commit:
Governance Commit A

runtime_mode:
OWNER_SELF_DOGFOOD

cycle_execution_mode:
AISCC_SELF_DOGFOOD

orchestrator_commit:
40bc4f8e2a9e10b42531441c1a4ee92c59bef963
```

Dynamic owner-derived fields MUST be copied exactly from existing current authorities:

```text
project_id
source_next_action
repository_id
evidence_binding refs/fingerprints/checkpoints
Human owner selector/config
Judgment policies/config
additional authority_refs if required by current owner policy
```

No Agent choice is allowed for those fields.

TaskContract V1 must verify:

```text
cycle-derived source current
repository/base exact
P1-6 graph current
Human/Judgment config valid
```

Issue receipt must be durable and current.

Record exact:

```text
body_ref
body_sha256
constraint_ref
issuance_event_ref
snapshot ref/hash
```

# 12. deterministic Task materialization/provenance

After successful TaskContract issuance and before Agent source edit:

1. call accepted `materialize_task_spec(...)`;
2. verify every spec field equals the TaskContract body/owner claims;
3. record canonical spec bytes/hash as provenance;
4. place the supplied inner golden Task byte-exact at:

```text
.aiassistant/tasks/active/20260914_1635_aiscc-p2-4-golden-agent-single-file-proof-change-1.md
```

5. verify SHA:

```text
de5269e5587f0fe99edbeeaeafa379702cdbffc452239413c6250ffde69b7966
```

The active Markdown Task is provenance/instruction only.
The durable TaskContract remains system authority.

# 13. actual WorkRun READY

Use accepted source-candidate API:

```text
enter_ready(...)
```

with fresh explicit exact IDs and UTC created_at.

Require:

```text
DecisionOutcome.ADMITTED
WorkflowState.READY
state_version = 1
```

Record:

```text
work_run_id
transition_request_id
TransitionDecision
TaskContract ref/version
spec hash
```

No source file may be changed before READY is admitted.

# 14. actual WorkRun RUNNING

Advance the exact same WorkRun through the existing P1-4/P1-5 execution-start authority path.

Do not write WorkRun/state directly.

Require source-native transition to:

```text
RUNNING
```

with issuer-backed execution start provenance required by the current P1-4 contract.

If the current source requires a producer/execution authority that cannot truthfully represent the external IDE Executor:

```text
GOLDEN_EXECUTION_INGRESS_UNAVAILABLE
```

STOP BEFORE editing the governed source file.

Do not fabricate P1-5 provider/tool execution merely to satisfy a guard.

# 15. materialize and execute exact inner Task

Only after the WorkRun is truthfully RUNNING:

- read the canonical active inner Task;
- create exactly:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

with exact bytes from package/inner Task;
- do not change any other source/config/test/document file.

Require immediately after edit:

```text
SHA-256 = 7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
git diff --check PASS
tracked/untracked Agent source diff = exact target path only
```

This edit is the actual governed Agent source change.

Do not commit yet.

# 16. actual execution submission / evidence candidate

Use the existing source-owned external-executor/execution-reference ingress ONLY if its contract truthfully applies to this IDE Executor operation.

Required authenticated submission must bind:

```text
project_id
task_contract_id/version
work_run_id
current state/version
inner Task identity/hash
changed path
target SHA
execution owner/issuer identity
```

Then create an actual P1-6 EvidenceCandidate and admit it through existing P1-6 APIs.

Evidence content must include exact machine-verifiable facts:

```text
task_sha256 = de5269e5587f0fe99edbeeaeafa379702cdbffc452239413c6250ffde69b7966
changed_path = docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
file_sha256 = 7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
git_diff_check = PASS
unauthorized_source_diff_count = 0
```

No Agent assertion alone is evidence.

No direct DB write.

If no truthful existing ingress applies:

```text
GOLDEN_EXECUTION_INGRESS_UNAVAILABLE
```

STOP with the source edit preserved but uncommitted; do not fake evidence.

# 17. evidence satisfaction + Judgment + ACCEPTED

Use existing source-native transition/evidence/Human/Judgment owners.

Follow the exact current P1-4 transition matrix; do not guess state names/order.

Golden completion must produce:

```text
P1-6 admitted evidence
P1-6 satisfaction attestation for exact checkpoint
P1-7/System-owned Judgment = ACCEPTED
P1-4 terminal WorkRun state = ACCEPTED
```

No HumanResult.

No direct state/Judgment minting by the operational driver.

Record every transition request/evaluation/decision in order.

If the owner matrix requires a state or guard not supported by the exact registered TaskContract policy, stop truthfully.

# 18. actual Cycle admission

After terminal ACCEPTED, admit exactly one P1-8 Cycle using the real accepted lineage.

Require Cycle provenance binds:

```text
Task
TaskContract
WorkRun
execution submission
admitted evidence / satisfaction
Judgment
terminal TransitionDecision
execution_mode = AISCC_SELF_DOGFOOD
orchestrator_commit = 40bc4f8e2a9e10b42531441c1a4ee92c59bef963
```

No Markdown Cycle file alone counts as P1-8 Cycle authority.

Record immutable cycle ref/id/fingerprint/revision.

# 19. result Git commit

Only after terminal ACCEPTED + Cycle admission.

Stage EXACTLY:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

Do not stage inner/outer Task, runtime reports, DB artifacts or canonical state.

Commit message exactly:

```text
docs(aiscc): prove first self dogfood golden cycle
```

Require:

```text
Commit B parent = Governance Commit A
changed paths = exact 1
target blob SHA maps to expected file bytes
index empty
tracked clean except exact Task/report lifecycle untracked paths
```

Record result commit SHA.

If commit fails, do not invent result provenance.

# 20. resulting authoritative NextAction

After Commit B, refresh only the existing current external NEXT_ACTION_CONTEXT with:

```text
repository base_commit = Result Commit B
phase = P2-4 post-golden-cycle
source Cycle = actual golden Cycle
```

through the existing owner API.

Then select/retrieve the current authoritative P1-8 NextAction.

Require:

```text
selection current by owner verifier
selection provenance includes actual golden Cycle/current context
result base commit = Commit B
```

Preferred/expected action for continued V1 self-dogfood:

```text
open-cycle-derived-task-issuance
```

If current owner deterministically chooses another valid action, do NOT rewrite it.

For P2-4 golden success under the accepted V1 boundary, if the final current action is not cycle-derived:

```text
GOLDEN_NEXT_ACTION_UNSUPPORTED_BY_V1
```

report the actual selection and STOP before claiming complete golden-cycle candidate.

# 21. inner Task lifecycle

After terminal ACCEPTED and successful result commit:

move exact inner Task:

```text
.aiassistant/tasks/active/20260914_1635_aiscc-p2-4-golden-agent-single-file-proof-change-1.md
→
.aiassistant/tasks/done/20260914_1635_aiscc-p2-4-golden-agent-single-file-proof-change-1.md
```

Bytes/SHA unchanged:

```text
de5269e5587f0fe99edbeeaeafa379702cdbffc452239413c6250ffde69b7966
```

Do not commit the inner Task in Commit B.

It remains explicit provenance for Browser persistence in the later P2-4 final-acceptance Task.

# 22. golden provenance root

Create a sanitized machine-readable:

```text
GOLDEN_PROVENANCE.json
```

containing exact IDs/hashes/refs for:

```text
execution_mode
orchestrator_commit
source NextAction selection/ref/fingerprint
inner Task path/SHA
TaskContract body_ref/body_sha
WorkRun id + full state/version transition chain
execution submission ref
EvidenceCandidate ref
AdmittedEvidence ref(s)
Evidence satisfaction attestation ref/root
Judgment ref/kind
Cycle ref/fingerprint
result Git commit
resulting NextAction ref/selection/fingerprint
```

Then compute:

```text
golden_provenance_root =
SHA256(restricted canonical JSON bytes of GOLDEN_PROVENANCE.json excluding the root field)
```

Store the root separately in the final report.

Do not invent missing fields.

# 23. operational runtime export

Before removing the Task-owned DB, export sanitized owner-readable records sufficient for independent Browser review:

```text
GOLDEN_TASKCONTRACT.json
GOLDEN_SPEC.json
GOLDEN_WORKRUN.json
GOLDEN_TRANSITIONS.json
GOLDEN_EXECUTION_SUBMISSION.json
GOLDEN_EVIDENCE.json
GOLDEN_JUDGMENT.json
GOLDEN_CYCLE.json
GOLDEN_NEXT_ACTION.json
GOLDEN_PROVENANCE.json
```

No raw DB dump.
No credentials.
No local DB URL.
No secrets.

Each JSON must be generated from actual owner read APIs/rows after completion, not reconstructed from prose.

# 24. runtime cleanup

After all required exports are written and hashed:

- remove exact Task-owned PostgreSQL container;
- remove exact Task-owned anonymous volume(s);
- remove credential helper/env file if any.

Cleanup failure is nonblocking operational residue unless it creates a security issue.

Do not Docker prune.

# 25. prohibited

Forbidden:

```text
pytest/test fixture as golden authority
imports from tests.*
monkeypatch
direct owner-table writes
synthetic fake WorkRun relabeled real
provider/LLM/network
changing product source/tests/migrations/rules
changing canonical state
modifying any Agent source path except docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
staging any path except docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md in result Commit B
fabricating execution/evidence/Human/Judgment authority
using Replay prose as current P1-8 authority
supporting operational recovery by bypassing V1 gate
automatic push/deploy
```

# 26. final verification

Required after Commit B and final NextAction:

```text
target file SHA exact
git show Commit B contains exact one path
git diff --check PASS
index empty
tracked clean

outer current Task -> done byte-exact
inner golden Task -> done byte-exact

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1635_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-1.md
.aiassistant/tasks/done/20260914_1635_aiscc-p2-4-golden-agent-single-file-proof-change-1.md

legacy 1400 unchanged
canonical state three hashes unchanged
no Task-owned Docker container/volume
```

If report target is ignored, it does not count as Git-visible dirt.

# 27. result report/export

Target:

```text
.aiassistant/reports/target/20260914_1635_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
PREDECESSOR_ACCEPTANCE_VERIFICATION.md
GOLDEN_BOOTSTRAP_REVIEW.md
GOLDEN_TASK_MATERIALIZATION.md
GOLDEN_TASKCONTRACT.json
GOLDEN_SPEC.json
GOLDEN_WORKRUN.json
GOLDEN_TRANSITIONS.json
GOLDEN_EXECUTION_SUBMISSION.json
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

Include:

```text
outer done Task
inner done Task
current outer Cycle/Judgment
exact changed target file
operational driver source used under runtime/
```

No credential-bearing files.

Result ZIP:

```text
.aiassistant/reports/target/20260914_1635_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-1.zip
```

# 28. named blockers

```text
BLOCKED_MISSING_ARTIFACT
DIRTY_WORKSPACE_MIXED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
SELF_DOGFOOD_BOOTSTRAP_AUTHORITY_MISSING
GOLDEN_EVIDENCE_INGRESS_UNAVAILABLE
GOLDEN_EXECUTION_INGRESS_UNAVAILABLE
GOLDEN_JUDGMENT_POLICY_UNAVAILABLE
GOLDEN_NEXT_ACTION_UNSUPPORTED_BY_V1
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
MIGRATION_BASELINE_MISMATCH
ISOLATED_POSTGRES_IMAGE_MISSING
BLOCKED_REQUIRED_EVIDENCE
SECURITY_BOUNDARY_BLOCKED
```

On blocker:

- no false golden success claim;
- no fake Cycle/NextAction;
- no result Commit B unless terminal ACCEPTED + actual Cycle occurred;
- preserve truthful runtime/source evidence;
- no broad reset/clean.

# 29. success ceiling

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

After Browser accepts the golden candidate, the next Task should be the P2-4 final acceptance/persistence/state-reconciliation cut, not another implementation microtask unless a concrete blocker exists.
