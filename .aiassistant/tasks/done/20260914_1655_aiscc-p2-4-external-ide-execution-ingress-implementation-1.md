# 작업지시서: P2-4 External IDE execution ingress implementation

## meta

- task_id: `20260914_1655_aiscc-p2-4-external-ide-execution-ingress-implementation-1`
- created_at: `2026-09-14T16:55:32+09:00`
- work_type: `HUMAN_ACCEPTED_AUTHORITY_IMPLEMENTATION + DATABASE_MIGRATION + INTEGRATION_QA + GIT_PERSISTENCE`
- evidence_profile: `CRITICAL_AUTHORITY_EXTENSION`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `e1b19a50fe59e00fa268c7cc67ff8603dea5a9e1`
- required_parent: `40bc4f8e2a9e10b42531441c1a4ee92c59bef963`
- predecessor_result_zip_sha256: `9a07ac4157869721b3dcceb172145d7ffae598c78ed464de506673bff5fc5aac`
- predecessor_done_task_sha256: `9af6a8939b8115bb725e9941e52d246d76587f1140b50a908e277c3c4e26d3d6`
- predecessor_result: `BLOCKED / GOLDEN_EXECUTION_INGRESS_UNAVAILABLE`
- predecessor_executor_disposition: `ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED`
- Human_design_decision: `HUMAN_PROVIDED / ACCEPTED`
- Human_review_sha256: `b15f43b046da344779ae5c7284f85f69261291ab6c46010b8fbddc085d3bbd00`
- accepted_design_id: `AISCC-P1-5-EXTERNAL-IDE-EXECUTION-INGRESS-V1`
- fresh_IDE_chat_required: `No`
- governance_commit_authorized: `Yes / exact 4 paths / Commit A`
- result_commit_authorized: `Yes / exact bounded implementation allowlist / Commit B`
- canonical_P1_5_rule_mutation_authorized: `Yes / exact bounded paths`
- database_migration_authorized: `Yes / one additive migration after 20260914_0009`
- Docker_authorized: `Yes / local postgres:17.6 task-owned isolated proof only`
- external_network_authorized: `No`
- provider_LLM_authorized: `No`
- provider_tool_execution_authorized: `No / regression only`
- retained_private_DB_authorized: `No`
- actual_self_dogfood_golden_cycle_authorized: `No`
- real_repository_Agent_change_authorized: `No`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_EXTERNAL_IDE_EXECUTION_INGRESS_IMPLEMENTATION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. Human acceptance

Human decision:

```text
ACCEPT
```

Applies exactly to:

```text
20260914_1653_aiscc-p2-4-external-ide-execution-ingress-authority-extension-human-review-1.md

SHA-256:
b15f43b046da344779ae5c7284f85f69261291ab6c46010b8fbddc085d3bbd00
```

Admit as:

```text
HUMAN_PROVIDED / ACCEPTED
```

Normative design:

```text
AISCC-P1-5-EXTERNAL-IDE-EXECUTION-INGRESS-V1
```

This Task implements that accepted design only.

It MUST NOT execute/retry the 1635 golden cycle.

# 1. predecessor blocker acceptance

1635 was independently verified:

```text
result ZIP:
9a07ac4157869721b3dcceb172145d7ffae598c78ed464de506673bff5fc5aac

45 members
44 manifest rows
one top-level
CRC PASS
44/44 manifest size/SHA exact

Governance Commit A:
e1b19a50fe59e00fa268c7cc67ff8603dea5a9e1

parent:
40bc4f8e2a9e10b42531441c1a4ee92c59bef963

Result Commit B:
NONE

Docker:
0

PostgreSQL:
0

TaskContract/WorkRun/source edit/Evidence/Judgment/Cycle:
0
```

Accepted blocker:

```text
GOLDEN_EXECUTION_INGRESS_UNAVAILABLE
```

The stop occurred before operational runtime provisioning.

No failed golden runtime identity exists.

# 2. predecessor evidence

Package hashes:

- `CONTRACT_REVIEW.md`: `4c8ad6443bef48b87614c2556a907aab1fc5207e321d8a313bcd24801eb2951d`
- `EXECUTOR_REPORT.md`: `0aad85c690642357a2d42412ff45c741b3ff67324c7f6ca21e9399e8ccd27f38`
- `GOLDEN_BOOTSTRAP_REVIEW.md`: `30064638abb587e4ee514bf5344591862341b7caac961a8c72042174517b2f19`
- `GOLDEN_TASK_MATERIALIZATION.md`: `5ef5bf568da7d8d98e0ec02d00eafa50cefb7c53ab135d21f2baab3f11f2d284`
- `WORKSPACE_VERIFICATION.md`: `6fbc8488ff30b2690d306ad5b197a0207e9c8b09fea9e1a658ad46d79d68cd3a`
- `evidence/COMMIT_A.json`: `a1e43f14cbb943bd41d0471c96804edda69e55b6d5d96891aa037685eb2a2408`
- `evidence/INGRESS_REVIEW.json`: `50f02931c0278cd309deb3793b8d6c709677011630d62d3328778973e65b4011`
- `evidence/PREFLIGHT.json`: `aaaabe64cda52623c9afbcee3496c6d77081b80b5225f36352317e4fa7cc5be4`
- `evidence/TERMINAL_WORKSPACE.json`: `0bf55d188f40839148644e988d5478984bf701816bd7705e6b3cc0454b8e41b7`
- `evidence/TRANSPORT_VERIFICATION.json`: `83449cdab3a002dcb7cd1b342452d8089c08b4ad026dd0c5af61fe4b36bb5192`

After Task-first read, copy these only under:

```text
.aiassistant/reports/target/20260914_1655_aiscc-p2-4-external-ide-execution-ingress-implementation-1/accepted-input/
```

Human review must also be copied there byte-exact for implementation evidence.

Any mismatch:

```text
BLOCKED_MISSING_ARTIFACT
```

STOP.

# 3. exact initial repository preflight

Require:

```text
branch:
main

HEAD:
e1b19a50fe59e00fa268c7cc67ff8603dea5a9e1

HEAD^:
40bc4f8e2a9e10b42531441c1a4ee92c59bef963

index:
empty

tracked:
clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1635_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-1.md
```

Prior done Task SHA:

```text
9af6a8939b8115bb725e9941e52d246d76587f1140b50a908e277c3c4e26d3d6
```

Preserve ignored legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md

SHA-256:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Canonical state remains byte-exact initially and terminally:

```text
CURRENT_STATE_SUMMARY.md
80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48

DECISION_REGISTER.md
9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5

NEXT_ACTIONS.md
050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679
```

Current migration head must be:

```text
20260914_0009
```

Exact source/rule preflight SHA-256:

- `src/aiscc/providers/authority.py`: `23507be8a8f073605dc11ac8eb7f84692b35621e1c296990fae9b2f676c535d2`
- `src/aiscc/providers/service.py`: `f21c3c29443446650e31fb0d4d0d30ceddb8956d51ad2e17221536102c6c5c18`
- `src/aiscc/providers/ports.py`: `8489359ea53c28e41bdf5e0f0d4970f567f0e763bee96f9f599cffc5a5ebfec4`
- `src/aiscc/providers/models.py`: `9641c99ca1629a7c6dbccd0ebe66922b73a7faa8ffc73ca9b278167384154e15`
- `src/aiscc/providers/events.py`: `69b0339a12630eb552ef479a819c78596a2c0094437b4458a30eebb730c18a98`
- `src/aiscc/persistence/models.py`: `fe37edea0096e848e825be5eb5664360b02d098e7870425099ff97599281dc77`
- `src/aiscc/persistence/repository.py`: `57dac018f6505468d62588761825025776d07384947424dad37b63f9f35e5e54`
- `src/aiscc/workflow/guards.py`: `e7509199bca3b901c7a04b4e5a1d8c23bab217eca5b78a3b9319d10300993cab`
- `src/aiscc/workflow/matrix.py`: `b2723c93828dd1a6b30d68ffc518e42c695a4c052acc3b3b24ca42f6c2152cd0`
- `src/aiscc/evidence/issuers.py`: `8f07c8eb14c78a77cac6b7d0400733f2c4d41fb3a7178f860e3540a575f9d9f5`
- `src/aiscc/evidence/models.py`: `df48a1c8af09c09827a2d5996e8aed19c3642e9f8b099b58e75bd855ded6c54e`
- `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`: `382433d24959827fc606592e7beb78f34934209fa2f9c34aabdeda1c6e322784`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`: `c47fcad05133139060701c08c0cb862de655839ed0d212d191ab84b830d690d5`

Any mismatch -> `POLICY_CONFLICT_INVESTIGATION_REQUIRED` or `DIRTY_WORKSPACE_MIXED`; STOP.

# 4. exact executables

Use only:

```text
Python:
<repository-root>\.venv\Scripts\python.exe

Git:
C:\Program Files\Git\cmd\git.exe

Docker:
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

Docker only for isolated PostgreSQL proof.

No PATH Python/Git substitution.
No Docker pull.

# 5. inbound placement + Governance Commit A

Order:

```text
verify ZIP/hash/archive/path safety
→ place current Task into .aiassistant/tasks/active
→ read current Task
→ exact repository preflight
→ verify Human review + predecessor evidence
→ place Cycle/Judgment/Human review canonical copies
```

Canonical placement:

```text
20260914_1655_aiscc-p2-4-external-ide-ingress-human-accepted-implementation-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_1655_aiscc-p2-4-external-ide-ingress-design-human-acceptance-implementation-authorization-1.md
-> .aiassistant/reports/aiscc/

20260914_1653_aiscc-p2-4-external-ide-execution-ingress-authority-extension-human-review-1.md
-> .aiassistant/reports/aiscc/
```

Stage EXACTLY:

```text
.aiassistant/tasks/done/20260914_1635_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-1.md
.aiassistant/records/aiscc/cycles/20260914_1655_aiscc-p2-4-external-ide-ingress-human-accepted-implementation-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_1655_aiscc-p2-4-external-ide-ingress-design-human-acceptance-implementation-authorization-1.md
.aiassistant/reports/aiscc/20260914_1653_aiscc-p2-4-external-ide-execution-ingress-authority-extension-human-review-1.md
```

Commit message exactly:

```text
docs(aiscc): accept external ide execution ingress design
```

Require:

```text
Commit A parent = e1b19a50fe59e00fa268c7cc67ff8603dea5a9e1
Commit A changed paths = exact 4
index empty
tracked clean
Git-visible untracked = 0
```

No product/canonical rule mutation before Commit A.

# 6. source audit before implementation

Read exact current source and direct tests for:

```text
src/aiscc/providers/models.py
src/aiscc/providers/authority.py
src/aiscc/providers/ports.py
src/aiscc/providers/service.py
src/aiscc/providers/events.py

src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py

src/aiscc/workflow/guards.py
src/aiscc/workflow/matrix.py

src/aiscc/evidence/issuers.py
src/aiscc/evidence/models.py

direct P1-5/P1-4/P1-6 tests
```

Create:

```text
SOURCE_AUTHORITY_AUDIT.md
```

Confirm:

1. provider/tool execution semantics remain untouched;
2. external IDE is a separate producer class;
3. current common issuer-verified execution start/submission handoff is reused where truthful;
4. no manual `register_submission(...)` call can substitute for authenticated ingress;
5. no fake provider `AgentOutputRef` is required;
6. P1-6 can resolve external submission through an immutable P1-5 producer record;
7. durable restart reconstruction is possible under allowed paths.

If current source requires changing a semantic owner outside the accepted P1-5 extension:

```text
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

STOP.

If another implementation source path is mechanically required:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

STOP.

# 7. exact producer scope

Add exactly one new producer kind:

```text
LOCAL_IDE_SELF_DOGFOOD_V1
```

Do NOT create:

```text
GENERIC_EXTERNAL_EXECUTOR
REMOTE_EXECUTOR
WEBHOOK_EXECUTOR
SHELL_EXECUTOR
```

or a plugin/registry that allows arbitrary producer enrollment.

The external IDE producer is only for local AISCC-owned self-dogfood execution.

# 8. domain model

Implement immutable typed authority for:

```text
ExternalIdeExecutionLeaseV1
ExternalIdeRepositoryObservationV1
ExternalIdeExecutionSubmissionV1
VerifiedExternalIdeExecutionSubmissionV1
```

Exact names may adapt to existing P1-5 naming conventions, but exported semantics must be equivalent.

Closed validation requirements:

```text
unknown fields denied
NFC text
safe integer semantics
lowercase SHA-256
canonical repository-relative paths
no traversal/absolute governed paths
sorted unique allowed/observed path collections
explicit producer kind
explicit schema/version
```

No mutable dict/list inside durable authority objects.

# 9. lease semantics

Trusted control-plane authority issues one lease for one exact external IDE execution.

Lease binds at minimum:

```text
project_id
lease_id
producer_kind = LOCAL_IDE_SELF_DOGFOOD_V1

work_run_id
expected_work_run_state
expected_work_run_state_version

task_id
task_contract_id
task_contract_version
task_contract_body_ref
task_contract_body_sha256

repository_id
repository_root
base_commit

inner_task_sha256

allowed_paths
forbidden_paths
scope_fingerprint

issued_at
expires_at or exact run-state-bounded expiry semantics

opaque capability token hash / nonce hash
```

The raw capability token MUST NOT be persisted.

A caller cannot choose its own lease identity as authority merely by constructing the model.

Only the trusted writer/service may issue it.

# 10. lease timing boundary

Human-accepted V1 says the completion lease is created only after the exact WorkRun is truthfully RUNNING.

Preserve that rule.

Do NOT use this Task to redesign P1-4 execution-start authority.

Implementation tests may establish a legitimate RUNNING fixture through existing accepted P1-5/P1-4 paths.

If source audit proves that future external IDE golden execution also lacks a truthful RUNNING-start ingress independent of completion:

```text
EXTERNAL_IDE_START_AUTHORITY_GAP
```

record it explicitly in `SOURCE_AUTHORITY_AUDIT.md`.

This finding alone does not permit changing the accepted design or P1-4/P1-5 start semantics in this Task.

If it prevents implementing/verifying the accepted completion ingress itself:

```text
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

STOP.

# 11. trusted repository observation

Create a bounded local Git observer under P1-5 ownership.

Preferred new source:

```text
src/aiscc/providers/external_ide.py
```

It must observe the repository directly.

Input authority:

```text
verified current lease
repository root from lease
expected base from lease
```

It must NOT trust caller-supplied values for:

```text
HEAD
changed paths
file hashes
diff-check result
unauthorized diff count
observation root
```

Compute at minimum:

```text
observed_HEAD
index status
tracked/untracked/deleted/renamed changed paths
per-observed-file SHA-256
git diff --check result
unauthorized changed paths
canonical observation root
observed_at
```

Observer must be read-only with respect to repository content/index.

No `git add`, checkout, reset, clean, commit or stash.

Git executable must be injectable/configured by trusted composition; do not hardcode the Human Executor Windows path in domain semantics.

# 12. direct observation vs caller claims

Completion request may contain only operation/control identity necessary to locate the lease/capability.

It must NOT accept caller-authored:

```text
changed_path list
file SHA list
HEAD claim
diff-check claim
observation root
```

as authoritative completion evidence.

Those values come from the trusted observer.

Agent/IDE prose remains non-authoritative.

# 13. durable persistence

Create one additive migration:

```text
migrations/versions/20260914_0010_external_ide_execution_ingress.py
```

with:

```text
revision = 20260914_0010
down_revision = 20260914_0009
```

No existing table/column semantic rewrite.

Recommended immutable tables:

```text
external_ide_execution_leases
external_ide_execution_submissions
```

Lease row is append-only.

Submission row is append-only and has a UNIQUE lease identity.

Lease consumption is represented by existence of the unique immutable submission row, not by mutating the lease row.

Persist enough canonical bytes/fingerprints to independently verify:

```text
lease identity/scope
capability token hash
repository observation
submission identity
common ExecutionSubmissionRef binding
producer kind
```

Mutation denial:

```text
UPDATE denied
DELETE denied
TRUNCATE denied
```

for both authority tables.

No pgcrypto dependency unless already accepted/current and provably required; prefer application-computed hashes.

No backfill.

Downgrade allowed only when both new tables are empty.
Nonempty downgrade must fail closed preserving schema/data/revision.

# 14. completion transaction

Completion MUST run in one caller-owned transaction and fail closed.

Required order/semantics:

```text
load exact lease
verify capability token hash
verify not expired/current
verify no existing conflicting submission
verify exact WorkRun/state/version through existing owner API
verify TaskContract/currentness through existing owner API
perform trusted repository observation
verify repository/base
verify observed paths within lease scope
verify required file hashes when TaskContract body specifies them
verify diff-check PASS
create immutable external IDE submission
create/register issuer-verified common ExecutionSubmissionRef
commit only through caller transaction owner
```

If exact same completed request is retried and current P1-5 idempotency semantics permit:

```text
return same durable submission
```

Changed replay:

```text
DENY
```

No submission row on failure.

# 15. common P1-5 handoff

The new external record is producer authority.

It must hand off to the existing common execution-submission contract used by:

```text
P1-4 G_EXECUTOR_SUBMISSION
P1-6 P1_5EvidenceIssuerAuthority
```

Preferred implementation:

```text
external durable submission
→ verified/reconstructed existing ExecutionSubmissionRef
```

Do not create:

```text
G_EXTERNAL_IDE_SUBMISSION
new WorkflowGuardFact kind
new EvidenceProfile
parallel EvidenceCandidate path
```

No fake provider AgentOutputRef.

If the current `ExecutionSubmissionRef` type cannot truthfully represent a non-provider producer without semantic extension, document the exact field conflict and STOP:

```text
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

Do not stuff false provider values into required fields.

# 16. restart reconstruction

After process restart, the runtime must be able to reconstruct/verify the external submission's issuer authenticity from PostgreSQL.

Do not rely on only:

```text
ExecutionReferenceAuthority in-memory registration
```

Acceptable pattern:

```text
durable external submission
→ owner verifier
→ exact common ExecutionSubmissionRef reconstruction
→ re-enroll/resolve in ExecutionReferenceAuthority where existing runtime composition requires it
```

Reconstruction must fail closed on tamper/missing/partial/inconsistent lineage.

# 17. P1-6 producer resolution

Modify `src/aiscc/evidence/issuers.py` only as needed to consume the new P1-5 durable producer authority.

Preserve:

```text
ExternalIdeExecutionSubmission
!= EvidenceCandidate
!= AdmittedEvidence
!= G_EVIDENCE
```

P1-6 must verify exact immutable external submission authority before creating a candidate.

No automatic evidence admission in P1-5.

# 18. security / non-capability boundary

The new ingress MUST NOT become:

```text
shell executor
command runner
provider dispatcher
tool dispatcher
secret resolver
Git commit service
Task generator
remote API
network callback
deployment service
```

It observes a repository after an already-authorized local IDE operation.

The only process execution it may perform is bounded local Git read/verification commands required for trusted observation.

No arbitrary command parameter is accepted from Agent/user input.

# 19. canonical rule adoption

Update only:

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
```

Record:

```text
AISCC-P1-5-EXTERNAL-IDE-EXECUTION-INGRESS-V1
producer = LOCAL_IDE_SELF_DOGFOOD_V1
bounded local self-dogfood only
lease + trusted observation + immutable submission
common ExecutionSubmissionRef handoff
no generic external executor framework
no Evidence/Judgment ownership
```

Do NOT modify:

```text
AISCC_EVIDENCE_ADMISSION.md
AISCC_HUMAN_GATE_JUDGMENT.md
AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md
```

# 20. exact mutation allowlist

## canonical rules

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
```

## P1-5 source

```text
src/aiscc/providers/models.py
src/aiscc/providers/authority.py
src/aiscc/providers/ports.py
src/aiscc/providers/service.py
src/aiscc/providers/external_ide.py
```

`service.py` may be left unchanged if external composition does not require it.

Do NOT modify:

```text
src/aiscc/providers/events.py
```

unless source audit proves an existing event union cannot persist/replay the new authority without it.
If required:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

STOP rather than silently modifying it.

## persistence

```text
src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py
migrations/versions/20260914_0010_external_ide_execution_ingress.py
```

## evidence adapter

```text
src/aiscc/evidence/issuers.py
```

## tests — new exact paths

```text
tests/unit/providers/test_external_ide_execution_ingress.py
tests/integration/providers/test_external_ide_execution_ingress.py
tests/integration/evidence/test_external_ide_execution_ingress.py
```

No other source/test/rule mutation is authorized.

Read-only owner paths include:

```text
src/aiscc/workflow/**
src/aiscc/evidence/models.py
src/aiscc/evidence/requirements.py
src/aiscc/task_authority/**
src/aiscc/next_action/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/self_dogfood/**
```

# 21. unit proof

`tests/unit/providers/test_external_ide_execution_ingress.py` must cover at minimum:

```text
producer kind exact
closed/NFC/hash/path validation
lease immutable
submission immutable
raw capability token not durable/serialized
wrong capability DENY
expired lease DENY
wrong run/state/version DENY
wrong TaskContract identity DENY
wrong repo/base DENY
scope overlap/traversal/absolute path DENY
changed retry DENY
exact retry deterministic
caller-supplied observation facts cannot override trusted observer
public API does not expose arbitrary command execution
public API does not expose generic external producer registration
```

# 22. isolated PostgreSQL 17.6 integration proof

Use local image only:

```text
postgres:17.6
```

No pull.

One Task-owned container, e.g.:

```text
aiscc-p2-4-external-ide-1655-pg
```

Synthetic credentials, loopback-only, no host bind.

Required migration proof:

```text
empty DB -> 0010 PASS
0009 -> 0010 PASS
0010 current head exact
UPDATE lease DENY
DELETE lease DENY
TRUNCATE lease DENY
UPDATE submission DENY
DELETE submission DENY
TRUNCATE submission DENY
empty downgrade PASS
nonempty downgrade DENY preserving schema/data/revision
```

# 23. real repository-observer integration fixture

Integration test must use a Task-owned temporary Git repository, NOT the actual AISCC repository working tree.

It must prove:

```text
trusted observer sees exact base HEAD
exact allowed untracked/modified file
exact file SHA
unauthorized path detection
deletion/rename detection
index mutation = 0
observer does not commit/add/reset/clean
git diff --check result recorded
canonical observation root stable
```

Do not use provider/network.

# 24. execution-ingress integration proof

On isolated PostgreSQL + Task-owned temp Git repo:

1. establish a legitimate RUNNING WorkRun fixture through existing accepted owner APIs;
2. bind exact TaskContract/repository/scope;
3. issue external IDE lease;
4. perform bounded file edit in temp repo;
5. complete via trusted observer;
6. persist immutable submission;
7. verify common issuer-backed `ExecutionSubmissionRef`;
8. existing P1-4 `G_EXECUTOR_SUBMISSION` accepts it;
9. existing P1-6 issuer resolves it and creates a candidate;
10. no AdmittedEvidence/G_EVIDENCE created merely by P1-5 completion.

Negative proof:

```text
manual register_submission cannot substitute for durable external ingress in the tested owner path
wrong capability DENY
wrong WorkRun DENY
wrong state_version DENY
TaskContract revoked DENY
wrong repository/base DENY
scope violation DENY
hash mismatch DENY
concurrent source mutation DENY
double completion deterministic
restart reconstruction PASS
tampered durable row -> AUTHORITY_CORRUPTION/fail closed
```

No real AISCC repository change.

# 25. provider/tool regression boundary

Existing provider/tool paths must remain byte-semantically compatible.

Run direct P1-5 regressions proving:

```text
provider execution unchanged
tool execution unchanged
secret mediation unchanged
unknown-outcome no-blind-retry unchanged
existing provider ExecutionSubmissionRef still resolves
existing P1-4 execution start/submission handoff unchanged
```

No provider/network calls.

Use mocks/fakes only in existing regression style, not as proof of external ingress authenticity.

# 26. workflow/evidence regressions

Run direct regression sets at minimum:

```text
tests/unit/providers
tests/integration/providers
tests/unit/workflow
tests/integration/workflow
tests/unit/evidence
tests/integration/evidence
tests/unit/task_authority
tests/integration/task_authority
tests/unit/self_dogfood
tests/integration/self_dogfood
```

Inventory collected node IDs/counts in report.

No xfail/skip conversion to hide failure.

# 27. static closure

Final bytes:

```text
Ruff changed Python PASS
compile changed Python PASS
git diff --check PASS
UTF-8/no BOM/control/fence checks PASS
```

No generated cache residue in Git-visible workspace.

# 28. Result Commit B

Only after complete PASS.

Commit message exactly:

```text
feat(aiscc): add external ide execution ingress
```

Commit all and only actual changed paths from section 20.

Require:

```text
Commit B parent = Governance Commit A
index empty
tracked clean
canonical state unchanged
legacy 1400 unchanged
```

No Commit B on blocker.

# 29. export

Target:

```text
.aiassistant/reports/target/20260914_1655_aiscc-p2-4-external-ide-execution-ingress-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
HUMAN_DESIGN_ACCEPTANCE_VERIFICATION.md
SOURCE_AUTHORITY_AUDIT.md
EXTERNAL_IDE_AUTHORITY_REVIEW.md
LEASE_SECURITY_REVIEW.md
REPOSITORY_OBSERVER_REVIEW.md
COMMON_SUBMISSION_HANDOFF_REVIEW.md
EVIDENCE_PRODUCER_HANDOFF_REVIEW.md
MIGRATION_REVIEW.md
POSTGRES_RUNTIME_EVIDENCE.md
TEST_RESULTS.md
STATIC_CHECKS.md
CONTRACT_REVIEW.md
```

Include changed project-relative files and current Cycle/Judgment/Human review/done Task.

No credentials, capability token, raw DB dump or private DB URL.

Result ZIP:

```text
.aiassistant/reports/target/20260914_1655_aiscc-p2-4-external-ide-execution-ingress-implementation-1.zip
```

# 30. terminal success boundary

Success:

```text
HEAD = Result Commit B
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1655_aiscc-p2-4-external-ide-execution-ingress-implementation-1.md
```

Current Task active -> done byte-exact.

Legacy 1400 unchanged.

Canonical state hashes unchanged.

No Task-owned Docker residue.

# 31. blockers

```text
BLOCKED_MISSING_ARTIFACT
DIRTY_WORKSPACE_MIXED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
EXTERNAL_IDE_START_AUTHORITY_GAP
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
MIGRATION_BASELINE_MISMATCH
ISOLATED_POSTGRES_IMAGE_MISSING
BLOCKED_REQUIRED_EVIDENCE
SECURITY_BOUNDARY_BLOCKED
```

On blocker:

- no false ingress acceptance;
- no golden-cycle retry;
- no fake provider/output authority;
- no broad reset/clean;
- preserve truthful Task-owned changes/evidence.

# 32. success ceiling

Complete PASS may report only:

```text
P2_4_EXTERNAL_IDE_EXECUTION_INGRESS_IMPLEMENTATION_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do NOT perform/claim:

```text
actual golden cycle
P2-4 ACCEPTED/CLOSED
canonical state reconciliation
Public Bounded Live
```

After Browser accepts this implementation candidate, retry the 1635 golden cycle with fresh runtime identities and a newly issued outer Task bound to the then-current repository base.
