# 작업지시서: P2-3 private S1 builder-reentry semantic-datetime retry

## meta

- task_id: `20260913_0036_aiscc-p2-3-private-s1-builder-reentry-semantic-datetime-retry-1`
- created_at: `2026-09-13T00:36:51+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `PRIVATE_SCENARIO_EXECUTION_RETRY`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`
- required_parent: `35cee94a92d1f12801576ef48038196922687f42`
- required_grandparent: `ee623c995cf1c24b4a362834f2d6d1fdf71a30cd`
- executor_session_action: `CONTINUE_CURRENT_CONTEXT`
- python_executable: `C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe`
- scenario_authorized: `S1 only`
- success_ceiling: `S1_EXECUTED_ACCEPTED_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. purpose

Retry the 0012 private S1 Task from the exact pre-builder point.

0012 did not invoke the builder and did not create any WorkRun/attempt.
The only admitted retry change is the executor verification harness rule for timezone-aware datetime equality.

Do not modify source/test/config/state.

Authorized exact S1 identifiers remain:

```text
scenario:
SCENARIO_IDS[0]

run_id:
aiscc-p2-3-private-s1-normal-v1-run

attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1
```

# 1. Python / transport

Use only:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.venv\Scripts\python.exe
```

Forbidden:

```text
python
py
WindowsApps Python alias
PATH Python discovery
```

Verify Short Prompt ZIP filename/SHA-256 and three flat safe members.

Place current Task first:

```text
.aiassistant/tasks/active/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-semantic-datetime-retry-1.md
```

Then place exact current Cycle/Judgment:

```text
.aiassistant/records/aiscc/cycles/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-harness-corrected-retry-entry-1.cycle.md
SHA-256:
8619cd9bfc9c3476129199c1213366a1bd26127c2f64d2156bddada7a3d97bfa

.aiassistant/reports/aiscc/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-harness-error-retry-judgment-1.md
SHA-256:
82550b3a3ed60678b1b252fe483f48003757870427ae8c1ecbefd4c35d1f0011
```

Bootstrap mismatch:

```text
STOP
no private/Docker/DB access
no report/export
```

# 2. repository baseline

Require:

```text
branch:
main

HEAD:
6cc4f988f56f5cbf32e57f4b5e9a52a180044c36

HEAD^:
35cee94a92d1f12801576ef48038196922687f42

HEAD^^:
ee623c995cf1c24b4a362834f2d6d1fdf71a30cd

index:
empty

tracked:
clean
```

Before current delivery Git-visible untracked exactly three:

- `.aiassistant/tasks/done/20260913_0012_aiscc-p2-3-private-s1-normal-scenario-execution-and-capture-retry-1.md`  `310bcfab97f13c7606bb09fc773ec6c659102e63b6ba1d33fa38b18c7cfeb034`
- `.aiassistant/records/aiscc/cycles/20260913_0012_aiscc-p2-3-private-s1-source-correction-persisted-execution-entry-1.cycle.md`  `ff0ca7f1752fd3a49306b660b1823b57b194a60b1d58c2341867e9c9b75dc702`
- `.aiassistant/reports/aiscc/20260913_0012_aiscc-p2-3-private-s1-source-correction-persisted-execution-authorization-judgment-1.md`  `568268a48fcda0145b549f9b26a5baf4287b8fb7f4937c3bfd9b2db60b5836a8`

Canonical state hashes:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `02b7a77d3f29d7ee3878157470020ab83b377ba0343867ab81ec6e82d1a9190b`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `9ca1b1a24f3f73c2f81d3342442cf0462b58fecdba2dbccc33509b0d4039ab71`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `7315a943ad4ed82757f4398d9613f3a6f773755f3496fa1e8fa816123422ea84`

Accepted source/test hashes:

- `src/aiscc/workflow/guards.py`  `e7509199bca3b901c7a04b4e5a1d8c23bab217eca5b78a3b9319d10300993cab`
- `src/aiscc/persistence/repository.py`  `ab00af3dd871477da74b83275258aa48a47ba9a7081aad0154a808b6e4f1c089`
- `src/aiscc/scenarios/capture_runner.py`  `0dab27e0ce9ce2da7953188bcb26f288b637a4ba524141be2800b08302a59b18`
- `src/aiscc/scenarios/stockroom_production.py`  `1ca58848a837e1130229c7a0e085df999d04c6041c77bb61098185d342ff14a0`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`  `02f5835a726f22d81d9d631f120c9d7c9b3c1311cc23ed93db5d3abd9a57f41e`
- `tests/unit/scenarios/test_contracts.py`  `bd56e823f4ae15e82233d2cbd50e2d20d13176dc88c0ee00c7ddab8de752b0d7`

After current Cycle/Judgment placement while Task is active/ignored:

```text
Git-visible untracked:
5 exact

0012 predecessor Task/Cycle/Judgment
current Cycle/Judgment
```

Any unexpected path/delta:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 3. reuse validated 0012 preflight facts only after exact revalidation

Revalidate before private access:

```text
canonical provenance hashes
Stockroom image identity/fingerprint
PostgreSQL image/container/volume identity/fingerprint
secret bind destination and representation class
private password-file boundary
private runtime-root boundary and entry count = 0
DB name/role/migration
authority envelope counts
exact run/attempt IDs absent
```

Do not treat the 0012 report alone as fresh current-state evidence.

# 4. corrected datetime comparison contract

For every datetime field used in builder re-entry equivalence proof:

```python
from datetime import datetime, timezone
```

Require both values:

```text
instanceof datetime
utcoffset() is not None
```

Reject naive values.

Compare semantic instants by:

```python
left == right
```

and record UTC-normalized values internally for verification:

```python
left.astimezone(timezone.utc)
right.astimezone(timezone.utc)
```

Require exact UTC instant including microseconds.

Do not use any of these as semantic equality:

```text
str(datetime)
isoformat string equality across display timezones
json.dumps(..., default=str)
locale text
timezone-name text
```

Reports may state only:

```text
timezone-aware:
PASS

semantic UTC equality:
PASS

microseconds:
equal
```

Do not export unnecessary timestamp payload detail if it creates no additional evidence value.

# 5. complete four evidence-enrollment proof

Before builder invocation, reconstruct the exact four current source-derived evidence enrollments using the same config/builder inputs that the public builder will use.

Compare each durable enrollment against PostgreSQL field-by-field.

For each of the four record:

```text
durable key:
exact

requirement-set identity:
exact

requirement identity:
exact

checkpoint identity:
exact

version/revision:
exact

fingerprint:
exact

non-datetime structured fields:
canonical structural equality

every datetime:
aware + semantic UTC instant equality
```

Require all four exact.

Also prove current repository registration behavior returns without INSERT/UPDATE/supersession/revision mutation for same identity/fingerprint.

Any unresolved field:

```text
S1_BUILDER_REENTRY_MUTATION_SCOPE_UNCERTAIN
→ STOP before builder
```

# 6. complete two judgment-policy proof

Before builder invocation, reconstruct the exact two source-derived judgment policies/projections using the same production inputs.

Compare each against PostgreSQL field-by-field:

```text
policy durable identity:
exact

policy version/revision:
exact

policy fingerprint:
exact

current projection:
exact

structured fields:
canonical structural equality

datetime fields:
aware + semantic UTC instant equality
```

Require both exact.

Prove existing registration path reuses the current identical revision/projection and returns without writes.

Any unresolved field:

```text
S1_BUILDER_REENTRY_MUTATION_SCOPE_UNCERTAIN
→ STOP before builder
```

# 7. pre-builder proof artifact

Before invoking the public builder create an in-memory/read-only verification table with exactly six logical rows:

```text
4 evidence enrollment rows
2 judgment policy rows
```

Each row must record only safe identifiers/fingerprints/revisions and PASS/FAIL comparisons.

Do not include:

```text
password
DSN
raw secret Source
normalized private paths
runtime-root absolute path
```

Builder invocation is forbidden unless all six rows are PASS.

# 8. public production builder exactly once

Only after sections 1–7 PASS, invoke exactly once:

```python
await aiscc.bootstrap.build_stockroom_production(...)
```

using the same retained private environment/canonical provenance inputs authorized in 0012.

Use exact:

```text
cancellation.run_id:
aiscc-p2-3-private-s1-normal-v1-run

cancellation.attempt_id:
aiscc-p2-3-private-s1-normal-v1-attempt-1

project_id:
aiscc-stockroom-private-capture

requester_identity:
aiscc-owner-operator

human_selector_fingerprint:
c55280095ff8bbac5ab186e44e3856e6a435da548c1c88b02b66caeba36e8f07
```

Use exact LOCAL_COMPATIBILITY secret mapping required by current production source.

No second builder call.

# 9. immediate post-builder DB proof

Immediately recount and compare the full authority envelope.

Require exact zero delta:

```text
evidence_requirement_sets:
4 → 4

evidence_requirements:
4 → 4

evidence_checkpoints:
4 → 4

judgment_policies:
2 → 2

judgment_policy_projections:
2 → 2

all revisions/fingerprints/current projections:
unchanged

all runtime/domain tables:
still zero
```

Any delta:

```text
S1_BUILDER_REENTRY_MUTATED_AUTHORITY
→ STOP before prepare_capture
```

No repair/retry/second builder.

# 10. S1 config and runner gate

Derive current S1 config from production authority.

Require:

```text
SCENARIO_IDS[0]
evidence basis = SATISFIED_ATTESTATION
expected Judgment = ACCEPTED
reason = STOCKROOM_EVIDENCE_SATISFIED
```

Read current complete `StockroomCaptureRunner`.

Require the same single source-owned full-run entrypoint as 0012:

```text
aiscc.scenarios.capture_runner.StockroomCaptureRunner.run
async def run(self, prepared: PreparedStockroomDriver) -> StockroomCaptureResult
```

Do not manually reproduce adapter calls.

# 11. prepare exactly once

Only after all prior sections PASS:

```python
capture = application.prepare_capture(
    scenario_id=SCENARIO_IDS[0],
    run_id="aiscc-p2-3-private-s1-normal-v1-run",
    attempt_id="aiscc-p2-3-private-s1-normal-v1-attempt-1",
)
```

Exactly one prepare call.

# 12. execute S1 exactly once

Invoke only:

```text
capture.runner.run(...)
```

exactly once.

Authorized sequence is source-owned:

```text
READY
→ RUNNING
→ execution completes
→ RUNNING_TO_ADMISSION_PENDING admitted
→ runtime/static evidence
→ evidence SATISFIED
→ System Judgment ACCEPTED
→ ADMISSION_PENDING_TO_ACCEPTED admitted
```

No manual transition/adapter choreography.

# 13. producer-link runtime assertion

Require runtime evidence path exercises the persisted correction:

```text
CURRENT:
ADMISSION_PENDING/current version

LINK:
exact historical predecessor transition

G_EXECUTOR_SUBMISSION bound refs:
exact canonical submission + execution-attempt pair

PRODUCER:
issuer-verified RUNNING/original producer version

linked submission:
equals verified producer submission

linked attempt:
equals verified producer attempt
```

No caller-authored state/version rebinding.
No cross-producer fallback.

# 14. security / provider assertions

Require:

```text
RuntimeMode:
OWNER_SELF_DOGFOOD

network grant:
none / false

provider/tool:
local deterministic / retained synthetic Stockroom only

secret class:
LOCAL_COMPATIBILITY only

RUNNING capability:
not reused after state change
```

Unexpected network/external provider:

```text
STOP_WITH_REPORT_EXPORT
```

# 15. terminal S1 assertions

Require:

```text
ExecutionStatus:
EXECUTOR_COMPLETED

EvidenceCheckpoint:
exact S1 checkpoint

Evidence evaluation:
SATISFIED

attestation:
genuine EvidenceSetSatisfactionAttestation

Judgment:
ACCEPTED

evidence_basis_kind:
SATISFIED_ATTESTATION

reason_code:
STOCKROOM_EVIDENCE_SATISFIED

HumanGate:
none

HumanResult:
none

WorkflowState:
ACCEPTED

S2/S3/S4:
NOT_EXECUTED
```

# 16. DB delta isolation

After terminal S1 enumerate every public application/domain table.

Require every new row is attributable to the exact S1 run/attempt or a durable ref transitively bound to it.

Require:

```text
pre-existing Cut C authority rows:
unchanged

S2/S3/S4:
no rows

unrelated Project/Task/Memory/Cycle:
no mutation
```

Report safe before/after/delta counts.

# 17. one-shot failure rule

After any durable row for exact run/attempt exists:

```text
no rerun
no alternate run/attempt
no DB repair/delete/reset
no runtime-root cleanup
no second builder
no second prepare
no second runner call
```

Preserve state and export bounded evidence.

# 18. poststate / settlement

Require:

```text
no still-running S1 transient container/process
no detached child
no external network attachment

retained PostgreSQL:
same container ID / running

migration:
unchanged

canonical provenance bytes:
unchanged

private password bytes:
unchanged
```

Do not manually clean source-owned runtime-root output.

# 19. exact private-value export scan

Before final ZIP creation keep the sensitive deny-set only in process memory:

```text
raw Docker secret Source
normalized password-file path
private runtime-root absolute path
password bytes decoded/text forms where representable
credential-bearing DB URL/DSN if constructed
```

Scan every export file byte sequence for exact sensitive values and obvious UTF-8/text escaped forms.

Do not print the matched values.

Report only:

```text
files scanned:
<count>

forbidden-value matches:
0
```

If any match:

```text
SECRET_PRIVATE_PATH_EXPORT_SCAN_FAIL
→ do not package unsafe export
```

# 20. repository / Git boundary

No tracked/source/config/state changes.

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

At terminal move current Task byte-identically:

```text
.aiassistant/tasks/active/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-semantic-datetime-retry-1.md
→
.aiassistant/tasks/done/20260913_0036_aiscc-p2-3-private-s1-builder-reentry-semantic-datetime-retry-1.md
```

Expected final Git-visible untracked exactly six:

```text
0012 predecessor Task/Cycle/Judgment
current Task/Cycle/Judgment
```

HEAD remains `6cc4f988f56f5cbf32e57f4b5e9a52a180044c36`.
Index empty.
Tracked clean.

# 21. contract review

Require exactly 45 rows:

```text
TRANSPORT_PACKAGE_EXACT
REPOSITORY_HEAD_PARENT_CLEAN
PREDECESSOR_0012_ARTIFACTS_EXACT
CURRENT_STATE_HASHES_EXACT
ACCEPTED_SOURCE6_HASHES_EXACT
PYTHON_EXECUTABLE_EXACT
RETAINED_ENVIRONMENT_IDENTITY_EXACT
SECRET_SOURCE_REPRESENTATION_EXACT
SECRET_SOURCE_PRIVATE_EXACT
PRIVATE_RUNTIME_ROOT_EXISTING_EMPTY_EXACT
PRE_BUILDER_AUTHORITY_ROWS_EXACT
PRE_BUILDER_RUNTIME_ROWS_ZERO
S1_RUN_ATTEMPT_IDS_ABSENT
DATETIME_VALUES_AWARE_EXACT
DATETIME_SEMANTIC_UTC_EQUALITY_PASS
NO_STRING_DATETIME_EQUALITY
EVIDENCE_ENROLLMENTS_4_EXACT
JUDGMENT_POLICIES_2_EXACT
BUILDER_REENTRY_IDEMPOTENCY_FULL_PROOF_PASS
PUBLIC_PRODUCTION_BUILD_ONCE_PASS
BUILDER_REENTRY_DB_UNCHANGED
S1_SCENARIO_CONFIG_EXACT
S1_ORCHESTRATION_ENTRYPOINT_UNAMBIGUOUS
S1_PREPARE_CAPTURE_EXACT
S1_SOURCE_OWNED_RUNNER_ONLY
S1_READY_RUNNING_TRANSITIONS_EXACT
S1_SECURITY_NETWORK_DENY_EXACT
S1_MATERIALIZATION_PROVENANCE_EXACT
S1_EXECUTION_COMPLETED_EXACT
S1_RUNTIME_EVIDENCE_ADMITTED
S1_EVIDENCE_SET_SATISFIED
S1_PRODUCER_LINK_EXACT
S1_CROSS_PRODUCER_SUBSTITUTION_NOT_USED
S1_JUDGMENT_ACCEPTED_EXACT
S1_FINAL_TRANSITION_ACCEPTED_EXACT
S1_NO_HUMAN_GATE_RESULT
S1_NO_OTHER_SCENARIO_EXECUTION
S1_DB_DELTA_RUN_SCOPED_EXACT
S1_DOCKER_PROCESS_SETTLED
PRIVATE_SECRET_UNCHANGED
RETAINED_ENVIRONMENT_POST_EXACT
NO_SOURCE_STATE_GIT_MUTATION
SECRET_PRIVATE_PATH_EXPORT_SCAN_PASS
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
EXPORT_INTEGRITY_PASS
```

Success:

```text
45 / 45 PASS
```

Blocked rows must remain `BLOCKED_REQUIRED_EVIDENCE`.

# 22. success export

Root docs exactly 17:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
SOURCE_BASELINE_VERIFICATION.md
RETAINED_ENVIRONMENT_VERIFICATION.md
SECRET_BOUNDARY_VERIFICATION.md
PRIVATE_RUNTIME_ROOT_VERIFICATION.md
BUILDER_REENTRY_SEMANTIC_COMPARISON.md
BUILDER_REENTRY_VERIFICATION.md
S1_ORCHESTRATION_ENTRYPOINT_VERIFICATION.md
S1_EXECUTION_VERIFICATION.md
S1_PRODUCER_LINK_VERIFICATION.md
S1_EVIDENCE_VERIFICATION.md
S1_JUDGMENT_TRANSITION_VERIFICATION.md
DATABASE_DELTA_VERIFICATION.md
CONTRACT_REVIEW.md
```

Project-relative copies exactly 5:

```text
current Cycle
current Judgment
current done Task
.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json
.aiassistant/records/aiscc/runtime/stockroom-private-postgres-provisioning.v1.json
```

Success export:

```text
22 members total
21 non-self manifest rows
one top-level directory
CRC PASS
folder/archive byte equality
TASK.md == current done Task
```

Blocked export may omit unavailable success-only reports, but must never fabricate PASS.

# 23. success ceiling

```text
private S1:
EXECUTED / ACCEPTED_CANDIDATE

WorkRun:
ACCEPTED

Evidence:
SATISFIED / admitted

Judgment:
ACCEPTED

HumanResult:
NONE

S2/S3/S4:
NOT_EXECUTED

S1 Browser admission:
HUMAN_PENDING

Git persistence:
NOT_PERFORMED

P2-3:
IN_PROGRESS
```
