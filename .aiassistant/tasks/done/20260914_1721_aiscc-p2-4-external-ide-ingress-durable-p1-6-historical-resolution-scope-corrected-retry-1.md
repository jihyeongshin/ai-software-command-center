# 작업지시서: P2-4 External IDE ingress — durable P1-6 historical producer resolution scope-corrected retry

## meta

- task_id: `20260914_1721_aiscc-p2-4-external-ide-ingress-durable-p1-6-historical-resolution-scope-corrected-retry-1`
- created_at: `2026-09-14T17:21:38+09:00`
- work_type: `CONTINUE_HUMAN_ACCEPTED_AUTHORITY_IMPLEMENTATION + P1_6_HISTORICAL_RESOLUTION_INTEGRATION + MIGRATION + QA + GIT_PERSISTENCE`
- evidence_profile: `CRITICAL_AUTHORITY_EXTENSION`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `1e7c3b2cf02a7d16ee349183d1d8fb003479e6d8`
- required_parent: `2d85d15caa795cba934b5fb479e968e434bcaa56`
- predecessor_result_zip_sha256: `cd4af4cbb72b2a63b6be943922247476539f79742ccfbbc15bfdd1fd29855738`
- predecessor_done_task_sha256: `ac06c3731becfc4f17cfcec31bbd0232f8b0c33465d8245d066af4e929c5687c`
- predecessor_result: `BLOCKED / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED`
- predecessor_disposition: `ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED`
- blocker_classification: `P1_6_DURABLE_EXTERNAL_PRODUCER_RESOLUTION_SCOPE_GAP / NOT_SEMANTIC_OWNER_CHANGE`
- Human_design: `HUMAN_PROVIDED / ACCEPTED`
- Human_design_sha256: `b15f43b046da344779ae5c7284f85f69261291ab6c46010b8fbddc085d3bbd00`
- accepted_design_id: `AISCC-P1-5-EXTERNAL-IDE-EXECUTION-INGRESS-V1`
- fresh_IDE_chat_required: `No`
- governance_commit_authorized: `Yes / exact 3 paths / Commit A`
- result_commit_authorized: `Yes / bounded implementation allowlist / Commit B`
- migration_authorized: `Yes / 20260914_0010 after 0009`
- additional_P1_6_repository_mutation_authorized: `Yes / exact historical external-producer delegation`
- actual_golden_cycle_authorized: `No`
- real_AISCC_source_edit_authorized: `No`
- provider_LLM_network_authorized: `No`
- Docker_authorized: `Yes / local postgres:17.6 isolated proof only`
- success_ceiling: `P2_4_EXTERNAL_IDE_EXECUTION_INGRESS_IMPLEMENTATION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. Browser judgment of 1705

Independent result verification:

```text
ZIP SHA-256:
cd4af4cbb72b2a63b6be943922247476539f79742ccfbbc15bfdd1fd29855738

42 members
41 manifest rows
one top-level
CRC PASS
41/41 manifest size+SHA exact

issued Task/Cycle/Judgment/Human review:
byte-exact
```

Executor status:

```text
BLOCKED / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

Disposition:

```text
ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED
```

Governance Commit A:

```text
1e7c3b2cf02a7d16ee349183d1d8fb003479e6d8

parent:
2d85d15caa795cba934b5fb479e968e434bcaa56
```

Result Commit B:

```text
NONE
```

No product/rule/migration/test mutation occurred.

# 1. exact 1705 blocker

Current P1-6 historical producer verification:

```text
src/aiscc/evidence/repository.py
SHA-256:
1a6f208b7251ec20a145812e846e96208db159a7ffd114a10f46a9d78799f8f5
```

For `P1_5_*` historical candidates it directly requires:

```text
ExecutionOutputRefRow
ExecutionAttemptRow
```

and validates provider-era immutable output/attempt lineage.

`ExecutionAttemptRow` requires non-null provider/tool registry identity.
`ExecutionOutputRefRow` requires an attempt FK.

The Human-accepted external IDE design intentionally forbids:

```text
fake provider profile/tool registry values
fake AgentOutputRef
provider completion without provider execution
historical verification bypass
```

Therefore a new durable external IDE submission can be recognized live by the P1-6 issuer adapter but cannot survive/reconstruct the existing historical verification path unless P1-6 delegates the external producer branch to the P1-5 durable external-submission owner verifier.

The common `ExecutionSubmissionRef` itself has no mandatory provider-profile fields.
No common-ref structural blocker is established.

This retry authorizes that exact integration.

# 2. Human design remains unchanged

Normative design:

```text
AISCC-P1-5-EXTERNAL-IDE-EXECUTION-INGRESS-V1
producer = LOCAL_IDE_SELF_DOGFOOD_V1
```

Core:

```text
RUNNING WorkRun
→ durable one-time lease
→ bounded local IDE operation
→ trusted direct Git observation
→ immutable durable external submission
→ issuer-verified common ExecutionSubmissionRef
→ existing P1-4 G_EXECUTOR_SUBMISSION
→ existing P1-6 EvidenceCandidate handoff
```

No generic external executor framework.

# 3. predecessor evidence

Hashes:

- `COMMON_SUBMISSION_HANDOFF_REVIEW.md`: `0b2f239471e6fa977f4a199c48ee5df24420b5ae41162bce8ee6ce9106969c37`
- `CONTRACT_REVIEW.md`: `64f225fb433f9301eed2fbbdc277b14d9136b53ce9cc84451617a6f267d421f9`
- `EVIDENCE_PRODUCER_HANDOFF_REVIEW.md`: `7e9388df703efdf23dd64fe7d4235199d6479667a34fdab7cd1af5bf431e1166`
- `EXECUTOR_REPORT.md`: `658a8a506d875e94e6a39167f4ec485ff4f25db8e0125ae54a5b424bef4d9e4b`
- `SOURCE_AUTHORITY_AUDIT.md`: `f57c1beef0d556026bdb4eb6a8a4c0685939055507831c76bb96df6ccc948470`
- `WORKSPACE_VERIFICATION.md`: `2dcee692d3aafedd5b128d21a22f2130ab17fdc14c28205e3490ec3a3e1ac769`
- `evidence/COMMIT_A.json`: `5d00121fd3869dee6148b4a0715ce8969fa6537e9a4b048fe4abfc9b5a2b6075`
- `evidence/PREFLIGHT.json`: `7bbca694d780879d9eba4488369263a6cd458110da45dcdff8267be50c52d989`
- `evidence/SCOPE_BLOCKER.json`: `04b851cc40148a0d33587c1e4d4254aab05e22524256b3109f6b83fae23b865e`
- `evidence/SOURCE_EXCERPTS.md`: `1dfb9953d96b458e62396ea597db994c7067a9d6ed0b512281f452e573062689`
- `evidence/TERMINAL_WORKSPACE.json`: `2c99927ea1eb83c7bd90cde361502187cca0b47da1ce80a41021b4ce05fec2fb`

Human review:

```text
20260914_1653_aiscc-p2-4-external-ide-execution-ingress-authority-extension-human-review-1.md
b15f43b046da344779ae5c7284f85f69261291ab6c46010b8fbddc085d3bbd00
```

After Task-first read copy only under:

```text
.aiassistant/reports/target/20260914_1721_aiscc-p2-4-external-ide-ingress-durable-p1-6-historical-resolution-scope-corrected-retry-1/accepted-input/
```

Mismatch -> `BLOCKED_MISSING_ARTIFACT`.

# 4. exact repository preflight

Require:

```text
branch = main
HEAD = 1e7c3b2cf02a7d16ee349183d1d8fb003479e6d8
HEAD^ = 2d85d15caa795cba934b5fb479e968e434bcaa56
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1705_aiscc-p2-4-external-ide-execution-ingress-implementation-regression-scope-corrected-retry-1.md
```

Done Task SHA:

```text
ac06c3731becfc4f17cfcec31bbd0232f8b0c33465d8245d066af4e929c5687c
```

Require exact unchanged P1-6 repository baseline:

```text
src/aiscc/evidence/repository.py
1a6f208b7251ec20a145812e846e96208db159a7ffd114a10f46a9d78799f8f5
```

Preserve legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Canonical state exact:

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
20260914_0009
```

`20260914_0010` must be absent initially.

Any mismatch -> fail closed.

# 5. executables

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

# 6. Governance Commit A

After Task-first read and preflight, place:

```text
20260914_1721_aiscc-p2-4-external-ide-ingress-p1-6-historical-resolver-scope-corrected-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_1721_aiscc-p2-4-1705-p1-6-historical-producer-resolver-scope-expansion-authorization-1.md
-> .aiassistant/reports/aiscc/
```

Stage EXACTLY:

```text
.aiassistant/tasks/done/20260914_1705_aiscc-p2-4-external-ide-execution-ingress-implementation-regression-scope-corrected-retry-1.md
.aiassistant/records/aiscc/cycles/20260914_1721_aiscc-p2-4-external-ide-ingress-p1-6-historical-resolver-scope-corrected-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_1721_aiscc-p2-4-1705-p1-6-historical-producer-resolver-scope-expansion-authorization-1.md
```

Commit message exactly:

```text
docs(aiscc): record external ide historical resolver scope blocker
```

Require:

```text
Commit A parent = 1e7c3b2cf02a7d16ee349183d1d8fb003479e6d8
changed paths = exact 3
index empty
tracked clean
```

No product/test/rule mutation before Commit A.

# 7. P1-6 historical resolver scope expansion — exact semantics

Newly authorize:

```text
src/aiscc/evidence/repository.py
```

for ONE semantic change only:

```text
historical P1_5_EXECUTION_SUBMISSION candidate
whose producer lineage identifies LOCAL_IDE_SELF_DOGFOOD_V1
→ delegate immutable producer verification to the durable P1-5 external IDE submission verifier
```

Preserve existing provider branches byte-semantically:

```text
P1_5_AGENT_OUTPUT
P1_5_TOOL_OUTPUT
P1_5_EXECUTION_ARTIFACT
provider-backed P1_5_EXECUTION_SUBMISSION
```

Do NOT weaken their:

```text
ExecutionOutputRefRow
ExecutionAttemptRow
work_run_id
task_contract_id/version
content hash
storage ref
issuer authority
requirement profile
```

checks.

Do NOT create a second EvidenceIssuerType.

Do NOT treat “external” merely from caller input.
The branch discriminator must come from durable owner-verifiable P1-5 producer authority / canonical common-ref lineage.

# 8. conditional P1-6 interface path

Conditionally authorize:

```text
src/aiscc/evidence/ports.py
```

ONLY if required to inject/call a P1-5 durable historical producer verifier without importing persistence implementation details into P1-6 domain code.

If modified, it may add only a narrow verifier protocol/value contract needed by the external historical branch.

It must NOT:

```text
change evidence admission semantics
add new EvidenceProfile
add new EvidenceIssuerType
mint Evidence/G_EVIDENCE
change requirement/checkpoint semantics
```

If another P1-6 source file is required:

```text
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

STOP.

# 9. Human-accepted ingress implementation

Resume the full ingress implementation from the 1653 design.

Required producer only:

```text
LOCAL_IDE_SELF_DOGFOOD_V1
```

Required authority:

```text
durable External IDE execution lease
trusted direct Git repository observation
immutable durable external IDE execution submission
common issuer-verified ExecutionSubmissionRef
restart reconstruction
P1-6 live + historical producer verification
```

Do not create generic remote/shell/webhook executor support.

# 10. lease authority

Implement immutable typed lease binding:

```text
project_id
lease_id
producer_kind
work_run_id/state/version
task_id
task_contract_id/version/body_ref/body_sha256
repository_id/root/base_commit
inner_task_sha256
allowed/forbidden paths
scope fingerprint
issued/expiry semantics
capability token hash
```

Raw capability token is never durable/exported.

One lease -> at most one immutable submission.

# 11. trusted Git observer

Preferred:

```text
src/aiscc/providers/external_ide.py
```

Directly compute, never trust caller claims:

```text
HEAD
index state
tracked/untracked/deleted/renamed changed paths
file SHA-256
git diff --check
unauthorized path set
canonical observation root
```

Observer is read-only.

No add/commit/reset/clean/checkout/stash.
No arbitrary command API.

# 12. migration

Create exactly:

```text
migrations/versions/20260914_0010_external_ide_execution_ingress.py

revision = 20260914_0010
down_revision = 20260914_0009
```

Additive immutable tables only for external IDE ingress authority.

Lease and submission tables:
UPDATE/DELETE/TRUNCATE denied.

Lease is not mutated to mark consumed; unique immutable submission existence represents consumption.

Empty downgrade PASS.
Nonempty downgrade fail-closed preserving data/schema/revision.
No backfill.

# 13. completion transaction

One transaction:

```text
verify lease/capability
verify current/unconsumed
verify exact WorkRun/state/version through owner
verify TaskContract/currentness
trusted repository observation
verify base/scope/hashes/diff-check
persist immutable external submission
produce/reconstruct issuer-verified common ExecutionSubmissionRef
```

Failure leaves no submission.

Exact completed retry deterministic.
Changed retry DENY.

# 14. P1-6 live + historical handoff

Live:

```text
src/aiscc/evidence/issuers.py
```

may verify external submission through the P1-5 durable owner and create the existing P1-5 execution-submission EvidenceCandidate form.

Historical/restart:

```text
src/aiscc/evidence/repository.py
```

must verify the same producer lineage through the P1-5 durable owner branch rather than fabricated provider rows.

Require exact consistency across:

```text
candidate issuer
candidate content_ref
producer_work_run_id
producer_attestation_ref
execution_attempt_id / external execution identity mapping
task_contract_id/version
submission content hash
common ExecutionSubmissionRef
external submission durable row
```

If current `EvidenceCandidate.execution_attempt_id` cannot truthfully bind an external execution identity without semantic model change, STOP:

```text
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

Do not stuff a fake provider attempt ID into it.

# 15. restart authority

After process restart:

```text
durable external submission
→ P1-5 owner verifier
→ common ExecutionSubmissionRef reconstruction
→ P1-6 live/historical verification
```

must remain valid.

In-memory-only `ExecutionReferenceAuthority` registration cannot be sole authority.

Tamper/missing/partial/inconsistent durable lineage -> fail closed.

# 16. external start boundary

The source audit also notes:

```text
EXTERNAL_IDE_START_AUTHORITY_GAP
```

may remain for the future golden composition because accepted self_dogfood entry currently ends at READY and provider P1-5 start uses provider-bound ExecutionAttemptRef.

This Task does NOT redesign start authority.

If ingress completion implementation/tests can be completed using legitimate existing RUNNING fixtures, finish this Task and report the start gap separately.

If the absence of truthful external start authority prevents proving completion ingress itself:

```text
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

STOP.

Do not fake provider start provenance.

# 17. canonical rule adoption

Modify only:

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
```

to record Human-accepted external IDE producer semantics.

Do NOT modify:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md
CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md
```

The P1-6 repository branch is implementation of existing evidence non-substitution/restart semantics, not a new canonical Evidence design.

# 18. complete mutation allowlist

Canonical:
```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
```

P1-5:
```text
src/aiscc/providers/models.py
src/aiscc/providers/authority.py
src/aiscc/providers/ports.py
src/aiscc/providers/service.py
src/aiscc/providers/external_ide.py
```

Persistence:
```text
src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py
migrations/versions/20260914_0010_external_ide_execution_ingress.py
```

P1-6:
```text
src/aiscc/evidence/issuers.py
src/aiscc/evidence/repository.py
src/aiscc/evidence/ports.py   # conditional as section 8
```

New tests:
```text
tests/unit/providers/test_external_ide_execution_ingress.py
tests/integration/providers/test_external_ide_execution_ingress.py
tests/integration/evidence/test_external_ide_execution_ingress.py
tests/unit/evidence/test_external_ide_historical_resolution.py
```

Existing strict migration-head fixtures:
```text
tests/integration/workflow/test_postgres_kernel.py
tests/integration/task_authority/test_task_contract_durability.py
tests/integration/self_dogfood/test_task_ready_entry.py
```

Those three existing tests may change only their strict current-head expectation `0009 -> 0010`.

Read-only:
```text
src/aiscc/providers/events.py
src/aiscc/workflow/**
src/aiscc/evidence/models.py
src/aiscc/evidence/requirements.py
src/aiscc/task_authority/**
src/aiscc/next_action/**
src/aiscc/human/**
src/aiscc/judgment/**
src/aiscc/self_dogfood/**
```

Any additional mutation path -> STOP.

# 19. isolated PostgreSQL 17.6 proof

No pull.

Use one Task-owned isolated PostgreSQL 17.6 container and Task-owned temporary Git repository.

Required migration proof:

```text
empty -> 0010 PASS
0009 -> 0010 PASS
strict current head 0010 PASS
lease/submission UPDATE DELETE TRUNCATE denied
empty downgrade PASS
nonempty downgrade DENY preserving state
```

Required ingress proof:

```text
lease issue PASS
RUNNING binding PASS with legitimate existing fixture
single-use completion PASS
direct Git observation PASS
wrong capability DENY
expired/stale DENY
wrong run/state/version DENY
TaskContract revoked DENY
wrong repo/base DENY
scope violation DENY
hash mismatch DENY
concurrent source mutation DENY
double completion deterministic
restart reconstruction PASS
tamper DENY
common ExecutionSubmissionRef verified
manual register_submission cannot substitute
```

Required P1-6 proof:

```text
live external producer candidate PASS
restart/historical external producer verification PASS
provider-backed historical branch regression PASS
wrong external submission ref DENY
wrong content hash DENY
wrong run DENY
wrong task contract DENY
missing/tampered durable external submission DENY
no AdmittedEvidence/G_EVIDENCE minted by P1-5
```

# 20. regressions

Run exact direct affected sets at minimum:

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

Inventory collected node IDs/count.

No skip/xfail substitution.

Provider/tool/secret existing execution semantics must remain unchanged.

# 21. static closure

Final bytes:

```text
Ruff changed Python PASS
compile changed Python PASS
git diff --check PASS
UTF-8/BOM/control checks PASS
```

# 22. Result Commit B

Only after all required proof PASS.

Commit message exactly:

```text
feat(aiscc): add external ide execution ingress
```

Stage only actual changed paths from section 18.

Require:

```text
Commit B parent = current Governance Commit A
index empty
tracked clean
canonical state unchanged
legacy 1400 unchanged
```

# 23. export

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
HUMAN_DESIGN_ACCEPTANCE_VERIFICATION.md
SOURCE_AUTHORITY_AUDIT.md
P1_6_HISTORICAL_RESOLUTION_REVIEW.md
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

Include changed project-relative files, current Cycle/Judgment/done Task.

No raw capability token/credentials/raw DB dump/private DB URL.

# 24. terminal success

```text
HEAD = Result Commit B
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1721_aiscc-p2-4-external-ide-ingress-durable-p1-6-historical-resolution-scope-corrected-retry-1.md
```

No Task-owned Docker residue.

# 25. blockers

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

# 26. success ceiling

Only:

```text
P2_4_EXTERNAL_IDE_EXECUTION_INGRESS_IMPLEMENTATION_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do NOT retry the golden cycle in this Task.
