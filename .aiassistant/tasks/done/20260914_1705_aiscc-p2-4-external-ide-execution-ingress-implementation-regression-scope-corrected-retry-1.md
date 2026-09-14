# 작업지시서: P2-4 External IDE execution ingress implementation — regression scope corrected retry

## meta

- task_id: `20260914_1705_aiscc-p2-4-external-ide-execution-ingress-implementation-regression-scope-corrected-retry-1`
- created_at: `2026-09-14T17:05:13+09:00`
- work_type: `CONTINUE_HUMAN_ACCEPTED_AUTHORITY_IMPLEMENTATION + TEST_SCOPE_CORRECTION + MIGRATION + QA + GIT_PERSISTENCE`
- evidence_profile: `CRITICAL_AUTHORITY_EXTENSION`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `2d85d15caa795cba934b5fb479e968e434bcaa56`
- required_parent: `e1b19a50fe59e00fa268c7cc67ff8603dea5a9e1`
- predecessor_result_zip_sha256: `77e70f63a906df863dfc427ddc677e11602d8efe2890a07bd8aa1be0ebd63947`
- predecessor_done_task_sha256: `d76c556aba2935bb58766dce4b20418e236accf421eb6278f71a3523b09d5cbb`
- predecessor_result: `BLOCKED / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED`
- predecessor_disposition: `ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED`
- blocker_classification: `MIGRATION_EXACT_HEAD_REGRESSION_FIXTURE_SCOPE_GAP`
- Human_design: `HUMAN_PROVIDED / ACCEPTED`
- Human_design_sha256: `b15f43b046da344779ae5c7284f85f69261291ab6c46010b8fbddc085d3bbd00`
- fresh_IDE_chat_required: `No`
- governance_commit_authorized: `Yes / exact 3 paths / Commit A`
- result_commit_authorized: `Yes / bounded implementation allowlist / Commit B`
- migration_authorized: `Yes / 20260914_0010 after 0009`
- additional_existing_test_mutation_authorized: `Yes / exact 3 head-fixture paths`
- actual_golden_cycle_authorized: `No`
- real_AISCC_source_edit_authorized: `No`
- provider_LLM_network_authorized: `No`
- Docker_authorized: `Yes / local postgres:17.6 isolated proof only`
- success_ceiling: `P2_4_EXTERNAL_IDE_EXECUTION_INGRESS_IMPLEMENTATION_CANDIDATE / BROWSER_REVIEW_REQUIRED`

# 0. predecessor judgment

1655 result is accepted as truthful fail-closed.

Independent archive verification:

```text
ZIP SHA-256:
77e70f63a906df863dfc427ddc677e11602d8efe2890a07bd8aa1be0ebd63947

37 members
36 manifest rows
CRC PASS
36/36 size+SHA exact
```

Executor status:

```text
BLOCKED / SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
```

Reason:

```text
authorized migration 0010
conflicts with three mandatory existing exact-head tests pinned to 0009
but those tests were outside section 20 mutation allowlist
```

No implementation was started:

```text
source writes 0
rule writes 0
migration writes 0
test runs 0
Docker calls 0
DB calls 0
```

This is a Command Center test-scope omission, not a rejection of the Human-accepted ingress design.

# 1. Human-accepted design remains unchanged

Normative:

```text
AISCC-P1-5-EXTERNAL-IDE-EXECUTION-INGRESS-V1

producer:
LOCAL_IDE_SELF_DOGFOOD_V1
```

Authority chain:

```text
RUNNING WorkRun
→ durable one-time local execution lease
→ bounded external IDE edit
→ trusted direct Git observation
→ immutable external IDE execution submission
→ existing issuer-verified ExecutionSubmissionRef
→ existing P1-4 G_EXECUTOR_SUBMISSION
→ existing P1-6 producer handoff
```

No generic external executor framework.
No fake provider AgentOutputRef.
No manual register_submission substitution.

# 2. predecessor evidence

Hashes:

- `CONTRACT_REVIEW.md`: `4bbffb658f6c58565efd8fb77d6912e499497b33b3082839f3793451a8518386`
- `EXECUTOR_REPORT.md`: `10abe9c7264b257cc6428dfa55b2c0e9b5711bf1d2b5349277f2fc041f193db1`
- `MIGRATION_REVIEW.md`: `30609e27a112a48c170c8412d2fb335954e2a89e7db83b36104f28bdace96cea`
- `POSTGRES_RUNTIME_EVIDENCE.md`: `e328dc4fe732abaa048c6dbb7efd1a7d6e5ba799a751ca564973622c5ecfd7ba`
- `SOURCE_AUTHORITY_AUDIT.md`: `29534f03d2b80d875e0369c5f0052124f1abcdd108382bc786a8193db23ba2a9`
- `TEST_RESULTS.md`: `d21f0b8225b87a09d4e8ec6c9e637f345d4383cebddb0301496e98a24ab67b4f`
- `WORKSPACE_VERIFICATION.md`: `675cb0e20e66c60efc3f8038c7e89c23a2d369f57982869e0bb3c50de003f96a`
- `evidence/COMMIT_A.json`: `19b9330ea16c2c88706475c7ba394339ce7459f3e8be3fc5578cfca8d5ef1ff0`
- `evidence/PREFLIGHT.json`: `45eaa84eae9bb153302d23ade27016ed844e7bb63eb179cb7a68b5d1195a3d12`
- `evidence/SCOPE_BLOCKER.json`: `af9ff27196372833dd3e656afa3bbad370a8f375662b55b829bf9efc1192c9c7`
- `evidence/TERMINAL_WORKSPACE.json`: `7f97f3bbed4f8c617005a30836b9d26dec22e6c9084b668c2349903b7a728044`

Human review:

```text
20260914_1653_aiscc-p2-4-external-ide-execution-ingress-authority-extension-human-review-1.md
b15f43b046da344779ae5c7284f85f69261291ab6c46010b8fbddc085d3bbd00
```

Copy after Task-first read only into:

```text
.aiassistant/reports/target/20260914_1705_aiscc-p2-4-external-ide-execution-ingress-implementation-regression-scope-corrected-retry-1/accepted-input/
```

Mismatch -> `BLOCKED_MISSING_ARTIFACT`.

# 3. exact repository preflight

Require:

```text
branch = main
HEAD = 2d85d15caa795cba934b5fb479e968e434bcaa56
HEAD^ = e1b19a50fe59e00fa268c7cc67ff8603dea5a9e1
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1655_aiscc-p2-4-external-ide-execution-ingress-implementation-1.md
```

Done Task SHA:

```text
d76c556aba2935bb58766dce4b20418e236accf421eb6278f71a3523b09d5cbb
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

Current migration head must be `20260914_0009`; migration `0010` absent.

Protected source/rule hashes:

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

Newly authorized existing test initial hashes:

- `tests/integration/workflow/test_postgres_kernel.py`: `19f71d7aba69f0755ca011a0bdc5d214ec9b84a750c0e22baca778c5470e7a90`
- `tests/integration/task_authority/test_task_contract_durability.py`: `786c8d6472f558e6b7db59319115f27548cefe244eba51e202d018493febe04b`
- `tests/integration/self_dogfood/test_task_ready_entry.py`: `e3497729a95d58044925a51d512a80ee149c5a6de0946d79d359a4ad98dce684`

Any mismatch -> STOP.

# 4. Governance Commit A

Place current Cycle/Judgment after exact preflight.

Stage EXACTLY:

```text
.aiassistant/tasks/done/20260914_1655_aiscc-p2-4-external-ide-execution-ingress-implementation-1.md
.aiassistant/records/aiscc/cycles/20260914_1705_aiscc-p2-4-external-ide-ingress-regression-scope-corrected-retry-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_1705_aiscc-p2-4-1655-regression-head-fixture-scope-expansion-authorization-1.md
```

Commit message exactly:

```text
docs(aiscc): record external ide ingress regression scope blocker
```

Require:

```text
Commit A parent = 2d85d15caa795cba934b5fb479e968e434bcaa56
exact 3 paths
index empty
tracked clean
```

No product/test mutation before Commit A.

# 5. exact scope correction

In addition to the previously accepted implementation allowlist, this retry authorizes mutation of EXACTLY:

```text
tests/integration/workflow/test_postgres_kernel.py
tests/integration/task_authority/test_task_contract_durability.py
tests/integration/self_dogfood/test_task_ready_entry.py
```

Purpose ONLY:

```text
update exact migration-head assertions/fixtures from 20260914_0009
to authorized new current head 20260914_0010
while preserving strict equality and existing downgrade/data-preservation semantics
```

Do not weaken assertions to non-null/startswith/latest-like logic.
Do not skip/xfail/monkeypatch migration resolution.

If those files require unrelated semantic changes, STOP with `TEST_FIXTURE_SCOPE_EXPANSION_REQUIRED`.

# 6. implementation contract

Implement the Human-accepted ingress exactly as 1653/1655 specified.

Required domain:

```text
ExternalIdeExecutionLeaseV1
ExternalIdeRepositoryObservationV1
ExternalIdeExecutionSubmissionV1
VerifiedExternalIdeExecutionSubmissionV1
```

Names may follow existing P1-5 naming conventions but semantics must match.

Only producer:

```text
LOCAL_IDE_SELF_DOGFOOD_V1
```

No generic registry/remote/webhook/shell executor.

# 7. lease

Trusted owner issues a single-use durable lease only for an exact RUNNING WorkRun.

Bind:

```text
project_id
lease_id
producer kind
work_run_id/state/version
task_id
task_contract_id/version/body_ref/body_sha256
repository_id/root/base_commit
inner_task_sha256
allowed/forbidden paths
scope fingerprint
issued/expiry semantics
raw capability token hash only
```

Never persist raw token.

Caller model construction is not authority.

# 8. trusted Git observation

Preferred new source:

```text
src/aiscc/providers/external_ide.py
```

Observer reads repository directly and computes:

```text
HEAD
index state
tracked/untracked/deleted/renamed paths
per-file SHA-256
git diff --check
unauthorized path set
canonical observation root
```

Caller cannot author those facts.

Observer is read-only:
no add/commit/reset/clean/checkout/stash.

Only bounded Git read/verification subprocess commands; no arbitrary command API.

# 9. persistence + migration

Create:

```text
migrations/versions/20260914_0010_external_ide_execution_ingress.py

revision = 20260914_0010
down_revision = 20260914_0009
```

Additive immutable authority tables, recommended:

```text
external_ide_execution_leases
external_ide_execution_submissions
```

Lease remains immutable; consumption is represented by unique immutable submission existence.

UPDATE/DELETE/TRUNCATE deny on both.
No backfill.
Empty-only downgrade.
Nonempty downgrade fail-closed preserving data/schema/revision.

# 10. completion transaction

In one owner/caller transaction:

```text
verify lease + capability
verify unconsumed/current
verify exact WorkRun/state/version via owner
verify TaskContract/currentness via owner
trusted repo observation
verify base/scope/hashes/diff-check
persist immutable submission
bind/register existing issuer-verified ExecutionSubmissionRef
```

Failure => no submission.

Exact completed retry may return same durable result if compatible with existing P1-5 idempotency.
Changed retry DENY.

# 11. common handoff

Must reuse existing common contract.

Forbidden:

```text
new G_EXTERNAL_IDE_*
new EvidenceProfile
parallel EvidenceCandidate path
fake provider AgentOutputRef
manual register_submission as authenticity proof
```

P1-4 and P1-6 receive the new producer only through a truthfully issuer-backed common `ExecutionSubmissionRef`.

If current common ref structurally requires false provider-only fields:

```text
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

STOP.

# 12. restart

PostgreSQL durable external submission must reconstruct issuer authenticity after process restart.

In-memory `ExecutionReferenceAuthority` alone is insufficient.

Tamper/missing/partial lineage => fail closed / authority corruption.

# 13. P1-6 handoff

`src/aiscc/evidence/issuers.py` may be modified only as needed to verify the P1-5 durable external submission before creating a candidate.

Preserve:

```text
External submission != EvidenceCandidate
!= AdmittedEvidence
!= G_EVIDENCE
```

P1-5 creates no Evidence/Judgment.

# 14. execution-start boundary

Do not redesign start authority in this Task.

If complete source audit shows future external IDE golden execution cannot truthfully reach RUNNING independently of completion ingress, report:

```text
EXTERNAL_IDE_START_AUTHORITY_GAP
```

If that prevents implementing/testing completion ingress itself, STOP.
Otherwise finish completion ingress and record the future blocker separately.

# 15. canonical adoption

Modify only:

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
```

Record bounded local self-dogfood producer, lease, trusted observation, immutable submission and common handoff.

Do not modify canonical state or other semantic-owner rules.

# 16. mutation allowlist

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

P1-6 adapter:
```text
src/aiscc/evidence/issuers.py
```

New tests:
```text
tests/unit/providers/test_external_ide_execution_ingress.py
tests/integration/providers/test_external_ide_execution_ingress.py
tests/integration/evidence/test_external_ide_execution_ingress.py
```

Newly authorized existing regression fixtures:
```text
tests/integration/workflow/test_postgres_kernel.py
tests/integration/task_authority/test_task_contract_durability.py
tests/integration/self_dogfood/test_task_ready_entry.py
```

Read-only unless new scope approved:
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

If another mutation path is necessary -> `SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED`.

# 17. PostgreSQL 17.6 proof

No image pull.

Use Task-owned isolated container.

Required migration proof:

```text
empty -> 0010 PASS
0009 -> 0010 PASS
current head exact 0010
immutable UPDATE/DELETE/TRUNCATE denied
empty downgrade PASS
nonempty downgrade DENY preserving schema/data/revision
```

Required ingress proof:

```text
lease issue PASS
RUNNING binding PASS
single-use completion PASS
trusted direct Git observation PASS
wrong token DENY
expired/stale lease DENY
wrong run/state/version DENY
TaskContract revoked DENY
wrong repo/base DENY
scope violation DENY
hash mismatch DENY
concurrent source mutation DENY
double completion deterministic
restart reconstruction PASS
tamper DENY
common ExecutionSubmissionRef accepted
manual register_submission not substitute
P1-6 issuer resolves exact durable external submission
no Evidence/Judgment minted by P1-5
```

Use Task-owned temporary Git repo, not real AISCC worktree.

# 18. regression contract

Run direct affected sets at minimum:

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

Inventory exact collected node IDs/count.

Three migration-head tests must remain strict and PASS at `0010`.

No xfail/skip substitution.

# 19. static

Final bytes:

```text
Ruff changed Python PASS
compile changed Python PASS
git diff --check PASS
UTF-8/BOM/control checks PASS
```

# 20. Result Commit B

Only after all required proof PASS.

Message exactly:

```text
feat(aiscc): add external ide execution ingress
```

Commit only allowlisted actual changed paths.

Require:

```text
parent = current Governance Commit A
index empty
tracked clean
canonical state unchanged
legacy 1400 unchanged
```

# 21. export

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

Also include current Cycle/Judgment/done Task and changed project-relative files.

No secret/raw token/DB dump/private DB URL.

# 22. terminal success

```text
HEAD = Result Commit B
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_1705_aiscc-p2-4-external-ide-execution-ingress-implementation-regression-scope-corrected-retry-1.md
```

No Task-owned Docker residue.

# 23. blockers

```text
BLOCKED_MISSING_ARTIFACT
DIRTY_WORKSPACE_MIXED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
TEST_FIXTURE_SCOPE_EXPANSION_REQUIRED
EXTERNAL_IDE_START_AUTHORITY_GAP
SOURCE_REWORK_SCOPE_EXPANSION_REQUIRED
AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
MIGRATION_BASELINE_MISMATCH
ISOLATED_POSTGRES_IMAGE_MISSING
BLOCKED_REQUIRED_EVIDENCE
SECURITY_BOUNDARY_BLOCKED
```

# 24. success ceiling

Only:

```text
P2_4_EXTERNAL_IDE_EXECUTION_INGRESS_IMPLEMENTATION_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Do NOT retry golden cycle in this Task.
