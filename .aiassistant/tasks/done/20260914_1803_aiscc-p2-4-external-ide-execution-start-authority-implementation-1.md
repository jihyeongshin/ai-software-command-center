# 작업지시서: P2-4 External IDE execution start authority implementation

## meta

- task_id: `20260914_1803_aiscc-p2-4-external-ide-execution-start-authority-implementation-1`
- created_at: `2026-09-14T18:03:27+09:00`
- work_type: `HUMAN_ACCEPTED_AUTHORITY_IMPLEMENTATION + DATABASE_MIGRATION + INTEGRATION_QA + GIT_PERSISTENCE`
- evidence_profile: `CRITICAL_AUTHORITY_EXTENSION`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `e9c17cbf2783669cf7f92df2399d3877e38c4816`
- required_parent: `e0501dae9c4444891f158e9b6c5126c3866b4a8f`
- predecessor_result_zip_sha256: `8af53c02e445b3148788edac1cda741b3afd0e8a82e62e210a4561dda3d134df`
- predecessor_done_task_sha256: `0303aa179eb927b2d6b1157e79049e54c912849e5716ea4b788a7408d8b29dcb`
- predecessor_judgment: `ACCEPTED / P2_4_EXTERNAL_IDE_EXECUTION_INGRESS_IMPLEMENTATION_CANDIDATE`
- Human_design_decision: `HUMAN_PROVIDED / ACCEPTED`
- Human_review_sha256: `ca4ab0a60b1c05a52befd4e2012934c42b8d6076602b1e7c21c9bdc8e20406a0`
- accepted_design_id: `AISCC-P1-5-EXTERNAL-IDE-EXECUTION-START-V1`
- fresh_IDE_chat_required: `No`
- governance_commit_authorized: `Yes / exact 4 paths / Commit A`
- result_commit_authorized: `Yes / exact bounded start-authority allowlist / Commit B`
- migration_authorized: `Yes / 20260914_0011 after 0010`
- canonical_rule_mutation_authorized: `Yes / exact 2 P1-5/orchestration paths`
- actual_golden_cycle_authorized: `No`
- real_repository_Agent_change_authorized: `No`
- provider_LLM_network_authorized: `No`
- retained_private_DB_authorized: `No`
- Docker_authorized: `Yes / local postgres:17.6 isolated proof only`
- push_deploy_authorized: `No`
- success_ceiling: `P2_4_EXTERNAL_IDE_EXECUTION_START_IMPLEMENTATION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. Human acceptance

Human decision:

```text
ACCEPT
```

Applies to:

```text
20260914_1800_aiscc-p2-4-external-ide-execution-start-authority-human-review-1.md
SHA-256:
ca4ab0a60b1c05a52befd4e2012934c42b8d6076602b1e7c21c9bdc8e20406a0
```

Admit exactly as:

```text
HUMAN_PROVIDED / ACCEPTED
```

Normative design:

```text
AISCC-P1-5-EXTERNAL-IDE-EXECUTION-START-V1
producer = LOCAL_IDE_SELF_DOGFOOD_V1
```

This Task implements start authority only.

It MUST NOT run the actual golden cycle.

# 1. predecessor acceptance

1721 is Browser-accepted:

```text
ACCEPTED
/ P2_4_EXTERNAL_IDE_EXECUTION_INGRESS_IMPLEMENTATION_CANDIDATE
```

Independent result:

```text
ZIP:
8af53c02e445b3148788edac1cda741b3afd0e8a82e62e210a4561dda3d134df

63 members
62 manifest rows
CRC PASS
62/62 size+SHA exact

tests:
351 PASS / 0 FAIL / 0 ERROR / 0 SKIP

migration:
20260914_0010 PASS

Result Commit B:
e9c17cbf2783669cf7f92df2399d3877e38c4816

parent:
e0501dae9c4444891f158e9b6c5126c3866b4a8f

message:
feat(aiscc): add external ide execution ingress

changed paths:
exact 15
```

Completion/submission ingress is accepted and must not be redesigned.

# 2. remaining exact gap

Current external IDE flow is:

```text
TaskContract current
→ WorkRun READY
→ [MISSING truthful external IDE start authority]
→ WorkRun RUNNING
→ accepted 1721 completion lease/submission ingress
```

Current P1-5 start authority authenticates provider-era `ExecutionAttemptRef`.

A fake provider attempt is forbidden.

A generic P1-4 `G_EXECUTION_STARTED` issuance is forbidden.

Source edit while READY and retroactive RUNNING is forbidden.

# 3. predecessor accepted evidence

Package evidence hashes:

- `CONTRACT_REVIEW.md`: `edaba187be9a42fdbd074abd22ba5caeabba190d227c9324297a05e8f4b12fde`
- `EXECUTOR_REPORT.md`: `8e88a47572bf06867190e2d08da7b59fe0e8f50c7629a736d955459429ba3107`
- `EXTERNAL_IDE_AUTHORITY_REVIEW.md`: `96422621a7134d6ba552d009f2216a499507fd00ff5e10040b1d7879e37a5bd8`
- `MIGRATION_REVIEW.md`: `4be940f05523f24ab39e7e7ce02b25295981d048c84e8a55790415cbc8ec9545`
- `POSTGRES_RUNTIME_EVIDENCE.md`: `7b40927c969be2c24eebdaa2d882fb7fa931c1d2f0926fa31d605448f49b37b4`
- `SOURCE_AUTHORITY_AUDIT.md`: `691bba40f061e5aec91fe162eda7cc124ae1655a0c122d07a3c723912a5253bd`
- `TEST_RESULTS.md`: `bb31b30aec0f3bad2370044696819130983a63fa40a1478df4adebc97b361517`
- `WORKSPACE_VERIFICATION.md`: `e782d37443d1030b5d6b6678fc62f23406a7fd6c9c0c206b0c65880b5f2f3c6b`
- `evidence/COMMIT_A.json`: `b61f292ff15d2f18b37c6eddde00089ffcdb3a270bb07d0dc0c76350503bf15f`
- `evidence/COMMIT_B.json`: `32b7c56ebe48d61e26eb0571b70eeae9460cb4bf6ad631000bae558278afa558`
- `evidence/FINAL_BYTE_STATIC.json`: `aaccc03c3c5147cf583f8da9b3a16a35b37f21099d566f200d83017ab982ecb2`
- `evidence/TERMINAL_WORKSPACE.json`: `5a54a04287f0317652d69d859725e8a285b573642b0b7097dc3278a758247175`
- `evidence/TEST_SUMMARY.json`: `600682a7587402fc577fd11a2836d54a07a54662bf4a99a1c4b498c47e928b23`

After Task-first read copy only under:

```text
.aiassistant/reports/target/20260914_1803_aiscc-p2-4-external-ide-execution-start-authority-implementation-1/accepted-input/
```

Human review must also be copied there byte-exact.

Mismatch -> `BLOCKED_MISSING_ARTIFACT`.

# 4. exact initial repository preflight

Require:

```text
branch:
main

HEAD:
e9c17cbf2783669cf7f92df2399d3877e38c4816

HEAD^:
e0501dae9c4444891f158e9b6c5126c3866b4a8f

index:
empty

tracked:
clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1721_aiscc-p2-4-external-ide-ingress-durable-p1-6-historical-resolution-scope-corrected-retry-1.md
```

Done Task SHA:

```text
0303aa179eb927b2d6b1157e79049e54c912849e5716ea4b788a7408d8b29dcb
```

Preserve ignored legacy:

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

Migration current head:

```text
20260914_0010
```

`20260914_0011` must be absent initially.

Current protected/target hashes:

- `.aiassistant/rules/AISCC_ORCHESTRATION.md`: `489bc66d5792a93e7013dfee02e89c602f6ea3c37351d0a862aca78cc599c009`
- `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`: `c512de61f119e274b964ab9b314cf89c4da40037ce5b1c6f10f2358620045262`
- `migrations/versions/20260914_0010_external_ide_execution_ingress.py`: `ee286d44823d9ced8c90398b101156bda2471820209e3e1e1569c991caf73aa0`
- `src/aiscc/evidence/issuers.py`: `a9c29149aa69c5d6fd3f18d30ac635fe0c1214d0ab4712ed23f13a7179af9bb3`
- `src/aiscc/evidence/repository.py`: `cb3eac5e55316ce901db8ec912308f44d45e46ea6a0fced83aba793ab442b5da`
- `src/aiscc/persistence/models.py`: `0f7a55c5571527e427d654d86ec1a90ab176b83cfe8ec6714e0cec5a1f9080e7`
- `src/aiscc/persistence/repository.py`: `57dac018f6505468d62588761825025776d07384947424dad37b63f9f35e5e54`
- `src/aiscc/providers/authority.py`: `3f1ac7c48e13d34f3152efc249c5f22a62dacefde729bf6326ddbf8144c767f2`
- `src/aiscc/providers/external_ide.py`: `aa24078e73e33b19e1a11b5af3a1ffc6e4da3f5c838b54392a782220fc7c4585`
- `src/aiscc/providers/models.py`: `9641c99ca1629a7c6dbccd0ebe66922b73a7faa8ffc73ca9b278167384154e15`
- `src/aiscc/workflow/guards.py`: `e7509199bca3b901c7a04b4e5a1d8c23bab217eca5b78a3b9319d10300993cab`
- `src/aiscc/workflow/matrix.py`: `b2723c93828dd1a6b30d68ffc518e42c695a4c052acc3b3b24ca42f6c2152cd0`
- `tests/integration/providers/test_external_ide_execution_ingress.py`: `efaba56e642b57917b49f3fa8e4f4008a7bdee3d3b5ff688871da471d3e8290c`
- `tests/integration/self_dogfood/test_task_ready_entry.py`: `8782dfb9c5fd430574109a831624f125e70b6229f4c445aba29c8a9752a93e66`
- `tests/integration/task_authority/test_task_contract_durability.py`: `b6c58a59cb5600c493a05eb125e9dd282f9cda47addeb2b92aa09c19e1f84248`
- `tests/integration/workflow/test_postgres_kernel.py`: `7a24971207e89543ea7c92a329f2c3dc9f5afb929fa27362b237da15c7378ec9`

Any mismatch -> fail closed.

# 5. source audit before mutation

Before editing, search the repository for:

```text
ExecutionAttemptRef
register_start
G_EXECUTION_STARTED
READY -> RUNNING
20260914_0010
```

Create:

```text
START_AUTHORITY_SOURCE_AUDIT.md
```

The audit must enumerate:

1. every direct caller/fixture of `register_start`;
2. every verifier branch for `G_EXECUTION_STARTED`;
3. every exact migration-head assertion pinned to `0010`;
4. whether existing `ExecutionAttemptRef` can truthfully represent `LOCAL_IDE_SELF_DOGFOOD_V1` without provider/tool falsehood;
5. restart/persistence path required for external start authenticity.

Known strict-head test paths already authorized:

```text
tests/integration/workflow/test_postgres_kernel.py
tests/integration/task_authority/test_task_contract_durability.py
tests/integration/self_dogfood/test_task_ready_entry.py
tests/integration/providers/test_external_ide_execution_ingress.py
```

If another existing path contains a mandatory exact-head `0010` assertion requiring mutation:

```text
MIGRATION_HEAD_TEST_SCOPE_EXPANSION_REQUIRED
```

STOP before source mutation.

Do not silently add it.

# 6. Governance Commit A

After Task-first read + exact preflight, place canonical:

```text
20260914_1803_aiscc-p2-4-external-ide-start-human-accepted-implementation-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_1803_aiscc-p2-4-external-ide-start-design-human-acceptance-implementation-authorization-1.md
-> .aiassistant/reports/aiscc/

20260914_1800_aiscc-p2-4-external-ide-execution-start-authority-human-review-1.md
-> .aiassistant/reports/aiscc/
```

Stage EXACTLY:

```text
.aiassistant/tasks/done/20260914_1721_aiscc-p2-4-external-ide-ingress-durable-p1-6-historical-resolution-scope-corrected-retry-1.md
.aiassistant/records/aiscc/cycles/20260914_1803_aiscc-p2-4-external-ide-start-human-accepted-implementation-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_1803_aiscc-p2-4-external-ide-start-design-human-acceptance-implementation-authorization-1.md
.aiassistant/reports/aiscc/20260914_1800_aiscc-p2-4-external-ide-execution-start-authority-human-review-1.md
```

Commit message exactly:

```text
docs(aiscc): accept external ide execution start design
```

Require:

```text
Commit A parent = e9c17cbf2783669cf7f92df2399d3877e38c4816
changed paths = exact 4
index empty
tracked clean
```

No product/test/rule mutation before Commit A.

# 7. exact authority goal

Implement one bounded durable start authority:

```text
READY WorkRun
→ external IDE start permit
→ issuer-backed verified external start ref
→ existing G_EXECUTION_STARTED
→ existing P1-4 READY -> RUNNING
```

Only producer:

```text
LOCAL_IDE_SELF_DOGFOOD_V1
```

No generic executor framework.

# 8. start domain model

Implement immutable typed authority equivalent to:

```text
ExternalIdeExecutionStartPermitV1
VerifiedExternalIdeExecutionStartV1
```

Exact names may follow current P1-5 conventions.

Permit binds at minimum:

```text
project_id
start_permit_id
producer_kind

work_run_id
expected_state = READY
expected_state_version

task_id
task_contract_id
task_contract_version
task_contract_body_ref
task_contract_body_sha256

repository_id
repository_root
base_commit

inner_task_sha256
scope_fingerprint

issued_at
expires_at

opaque capability token hash / nonce hash
```

Raw capability is not persisted or exported.

Closed validation:
NFC, canonical IDs/paths, lowercase SHA-256, UTC-aware timestamps, safe integers, unknown fields denied.

# 9. permit issue

Trusted P1-5 owner may issue a permit only after verifying:

```text
exact WorkRun exists
state = READY
state_version exact
TaskContract current
repository identity/root/base exact
producer exact
task hash/scope exact
```

Caller model construction is not authority.

No permit for RUNNING/terminal/nonexistent WorkRun.

# 10. common start reference decision

Audit current `ExecutionAttemptRef`.

## If it can truthfully represent external producer

Reuse it only when no provider/tool identity is fabricated.

## If it cannot

Add a P1-5-owned immutable external start ref, e.g.:

```text
ExternalIdeExecutionStartRef
```

and extend only:

```text
ExecutionReferenceAuthority.verify(..., G_EXECUTION_STARTED)
```

to accept a durable-owner verified external start receipt/ref.

Do NOT change P1-4 guard semantics.

Do NOT add `G_EXTERNAL_IDE_STARTED`.

Do NOT fill fake provider/tool fields.

# 11. durable persistence

Create exactly one additive migration:

```text
migrations/versions/20260914_0011_external_ide_execution_start.py

revision = 20260914_0011
down_revision = 20260914_0010
```

Recommended append-only authority tables:

```text
external_ide_execution_start_permits
external_ide_execution_starts
```

or equivalent exact current naming.

Permit immutable.
Start/consumption represented by a unique immutable start row, not permit UPDATE.

Both authority tables:

```text
UPDATE denied
DELETE denied
TRUNCATE denied
```

No backfill.

Empty downgrade PASS.
Nonempty downgrade fail-closed preserving schema/data/revision.

# 12. atomic READY -> RUNNING start

Start operation must be one fail-closed composition.

Required semantics:

```text
load/verify permit
verify capability
verify unconsumed/current
verify WorkRun still READY/version exact
verify TaskContract current
verify repository/base exact
persist immutable start consumption/authority
create/enroll issuer-backed start ref
invoke existing P1-4 READY -> RUNNING
```

Transaction/rollback design must guarantee:

```text
failed P1-4 transition
→ no committed successful external start authority
```

No direct WorkRun/state writes.

If exact transition ordering requires a transaction participant or owner callback, use an existing P1-4 extension seam; do not alter workflow semantics.

If no existing seam can make start consumption atomic with transition without modifying P1-4 owner source:

```text
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

STOP.

# 13. restart authority

After process restart:

```text
durable start permit/start row
→ P1-5 owner verifier
→ issuer-backed external start ref reconstruction
→ existing G_EXECUTION_STARTED verification
```

must work.

In-memory `register_start(...)` alone is not authority for the external producer.

Tamper/missing/partial/inconsistent lineage -> fail closed.

# 14. replay/idempotency

Required:

```text
wrong capability DENY
expired permit DENY
wrong WorkRun DENY
wrong state_version DENY
revoked/superseded TaskContract DENY
repository/base drift DENY
wrong task hash DENY
double-start deterministic
changed retry DENY
start permit replay DENY
concurrent RUNNING/terminal transition cannot produce stale PASS
```

Exact P1-4 request retry may return existing durable transition decision only under existing P1-4 idempotency.

# 15. completion continuity

Accepted 1721 completion semantics remain unchanged:

```text
external start
→ RUNNING
→ completion lease
→ trusted Git observation
→ external submission
→ common ExecutionSubmissionRef
```

Proof must establish:

```text
completion lease issuance before RUNNING DENY
completion lease issuance after accepted external RUNNING PASS
```

Do not alter completion domain/persistence semantics except minimal wiring required to consume the accepted RUNNING state.

# 16. authority boundaries

Start authority MUST NOT create:

```text
ExecutionSubmission
EvidenceCandidate
AdmittedEvidence
G_EVIDENCE
HumanGate
HumanResult
Judgment
Cycle
NextAction
```

No source edit is performed in this Task.

No provider/tool/secret call.

# 17. canonical adoption

Modify only:

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
```

Record:

```text
AISCC-P1-5-EXTERNAL-IDE-EXECUTION-START-V1
producer LOCAL_IDE_SELF_DOGFOOD_V1
READY-bound durable one-time start permit
issuer-backed G_EXECUTION_STARTED reuse
P1-4 sole state mutation owner
start != completion
no fake provider attempt
```

No canonical state mutation.

# 18. exact mutation allowlist

## canonical

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
```

## P1-5 start

```text
src/aiscc/providers/authority.py
src/aiscc/providers/external_ide.py
src/aiscc/providers/models.py
```

`providers/models.py` only if a common/external start ref type belongs there; otherwise leave unchanged.

## persistence

```text
src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py
migrations/versions/20260914_0011_external_ide_execution_start.py
```

## new tests

```text
tests/unit/providers/test_external_ide_execution_start.py
tests/integration/providers/test_external_ide_execution_start.py
tests/integration/self_dogfood/test_external_ide_running_entry.py
```

## strict migration-head fixtures

```text
tests/integration/workflow/test_postgres_kernel.py
tests/integration/task_authority/test_task_contract_durability.py
tests/integration/self_dogfood/test_task_ready_entry.py
tests/integration/providers/test_external_ide_execution_ingress.py
```

These existing files may change only strict current-head expectations from:

```text
20260914_0010
```

to:

```text
20260914_0011
```

unless `test_external_ide_execution_ingress.py` requires additive migration-chain coverage for 0011; any such extra change must remain migration-only and be documented.

## read-only

```text
src/aiscc/workflow/**
src/aiscc/evidence/**
src/aiscc/task_authority/**
src/aiscc/next_action/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/self_dogfood/**
```

If source implementation requires mutation outside the allowlist:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

STOP.

# 19. isolated PostgreSQL 17.6 proof

Use local `postgres:17.6` only; no pull.

Task-owned isolated container, loopback-only, synthetic credentials, no host bind.

Migration proof:

```text
empty -> 0011 PASS
0010 -> 0011 PASS
strict current head 0011 PASS
start permit/start UPDATE DELETE TRUNCATE denied
empty downgrade PASS
nonempty downgrade DENY preserving data/schema/revision
```

# 20. start integration proof

On isolated PostgreSQL:

1. establish exact TaskContract and WorkRun READY through existing accepted owners;
2. issue external start permit;
3. verify raw capability not persisted;
4. start exact WorkRun;
5. existing P1-4 admits READY -> RUNNING;
6. WorkRun state/version exact;
7. no direct WorkRun mutation;
8. start row durable;
9. restart verifier reconstructs valid start authority;
10. existing `G_EXECUTION_STARTED` accepts only owner-backed external start;
11. generic/manual start registration cannot substitute;
12. wrong token/run/version/base/hash/task/revoked contract deny;
13. replay/double start deterministic;
14. rollback/denied transition leaves no false committed start;
15. concurrent state change cannot pass stale start;
16. completion lease before RUNNING deny;
17. completion lease after RUNNING pass;
18. accepted 1721 completion ingress direct regression passes unchanged;
19. no Evidence/Judgment/Cycle created.

# 21. provider regression

Existing provider/tool start path must remain valid.

Prove:

```text
provider ExecutionAttemptRef start PASS
provider/tool/secret regressions PASS
external start does not register as provider attempt
provider start historical/current semantics unchanged
```

No provider/network calls.

# 22. direct regressions

Run at minimum:

```text
tests/unit/providers
tests/integration/providers
tests/unit/workflow
tests/integration/workflow
tests/unit/task_authority
tests/integration/task_authority
tests/unit/self_dogfood
tests/integration/self_dogfood
tests/unit/evidence
tests/integration/evidence
```

Inventory exact collected node IDs/count.

No skip/xfail substitution.

# 23. static closure

Final bytes:

```text
Ruff changed Python PASS
compile changed Python PASS
git diff --check PASS
UTF-8/BOM/control checks PASS
```

# 24. Result Commit B

Only after complete PASS.

Commit message exactly:

```text
feat(aiscc): add external ide execution start authority
```

Stage only allowlisted actual changed paths.

Require:

```text
Commit B parent = Governance Commit A
index empty
tracked clean
canonical state unchanged
legacy 1400 unchanged
```

# 25. export

Target:

```text
.aiassistant/reports/target/20260914_1803_aiscc-p2-4-external-ide-execution-start-authority-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
HUMAN_DESIGN_ACCEPTANCE_VERIFICATION.md
START_AUTHORITY_SOURCE_AUDIT.md
EXTERNAL_IDE_START_AUTHORITY_REVIEW.md
START_SECURITY_REVIEW.md
P1_4_START_HANDOFF_REVIEW.md
COMPLETION_CONTINUITY_REVIEW.md
MIGRATION_REVIEW.md
POSTGRES_RUNTIME_EVIDENCE.md
TEST_RESULTS.md
STATIC_CHECKS.md
CONTRACT_REVIEW.md
```

Include changed project-relative files and current Cycle/Judgment/Human review/done Task.

No raw capability token/credentials/raw DB dump/private DB URL.

# 26. terminal success

```text
HEAD = Result Commit B
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1803_aiscc-p2-4-external-ide-execution-start-authority-implementation-1.md
```

Current Task active -> done byte-exact.
Legacy 1400 unchanged.
Canonical state hashes unchanged.
No Task-owned Docker residue.

# 27. blockers

```text
BLOCKED_MISSING_ARTIFACT
DIRTY_WORKSPACE_MIXED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
MIGRATION_HEAD_TEST_SCOPE_EXPANSION_REQUIRED
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
MIGRATION_BASELINE_MISMATCH
ISOLATED_POSTGRES_IMAGE_MISSING
BLOCKED_REQUIRED_EVIDENCE
SECURITY_BOUNDARY_BLOCKED
```

# 28. success ceiling

Complete PASS may report only:

```text
P2_4_EXTERNAL_IDE_EXECUTION_START_IMPLEMENTATION_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do NOT run or claim the actual golden cycle.

After Browser acceptance, reissue the golden cycle against the new repository base using fresh runtime identities.
