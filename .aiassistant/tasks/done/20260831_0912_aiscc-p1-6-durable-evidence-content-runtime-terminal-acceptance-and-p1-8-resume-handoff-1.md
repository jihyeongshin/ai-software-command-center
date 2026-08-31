# 작업지시서: P1-6 Durable Evidence Content Runtime Terminal Acceptance + P1-8 Resume Handoff

## meta

- task_id: `20260831_0912_aiscc-p1-6-durable-evidence-content-runtime-terminal-acceptance-and-p1-8-resume-handoff-1`
- created_at: `2026-08-31T09:12:00+09:00`
- phase: `P1-6 Durable Evidence Content Authority Extension Runtime`
- work_type: `COMMAND_CENTER_RECORD_UPDATE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_6_EVIDENCE_CONTENT / AISCC_COMMAND_CENTER`
- expected_start_head: `bc446d9530e28f9b10602c9f1dd5232a97221a10`
- accepted_extension_design_commit: `32e88234ad7a7cbaa545e12f8c7e03b5897202cb`
- extension_design_terminal_governance_commit: `bc446d9530e28f9b10602c9f1dd5232a97221a10`
- accepted_extension_design_sha256: `ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411`
- accepted_runtime_path_count: `13`
- accepted_runtime_aggregate_sha256: `2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721`
- human_runtime_final_review: `HUMAN_PROVIDED / ACCEPTED`
- p1_8_design_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- p1_8_runtime_status_before_task: `BLOCKED_REQUIRED_EVIDENCE / NOT_RESUMED`
- p2_status: `NOT_STARTED`
- public_bounded_live: `NOT_RELEASED`

---

# 1. Human final runtime judgment

Human final review is complete.

Exact Human decision:

```text
Human P1-6 durable evidence-content extension runtime final review
판정: ACCEPTED
```

Do not ask for Human acceptance again.

Do not reinterpret this as permission to change the accepted runtime candidate.

This Task exists only to:

```text
1. verify the exact Human-accepted 13-path runtime candidate has not drifted;
2. commit that exact runtime candidate as Commit A;
3. create terminal Human acceptance provenance bound to actual Commit A;
4. persist the complete durable-content runtime HOLD/verification lineage and canonical state as Commit B;
5. create a durable P1-8 runtime-resume handoff bound to the accepted extension runtime commit;
6. leave P1-8 runtime NOT_STARTED until Command Center verifies this closure.
```

---

# 2. terminal target state

After successful completion:

```text
P1-6 core
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Runtime
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 Runtime blocker:
BLOCKED_REQUIRED_EVIDENCE
→ RESOLVED

P1-8 Runtime
→ NOT_STARTED / RESUME_AUTHORIZED / NEXT_ACTION

P2
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

Do NOT implement or resume P1-8 runtime in this Task.

---

# 3. mandatory preflight

Before any Git index/commit action:

## 3.1 HEAD

Require:

```text
HEAD ==
bc446d9530e28f9b10602c9f1dd5232a97221a10
```

Mismatch:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

Do not reset, rebase, checkout-overwrite, clean, or amend.

## 3.2 accepted extension design

Require:

```text
sha256(.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md)
==
ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411
```

Require design commits remain exact:

```text
Stage 0A:
32e88234ad7a7cbaa545e12f8c7e03b5897202cb

Stage 0B:
bc446d9530e28f9b10602c9f1dd5232a97221a10
```

Do not amend/revert/squash them.

## 3.3 exact accepted runtime identity

The exact Human-accepted runtime candidate is the following 13 paths.

Compute SHA-256 from current working-tree bytes and require exact match.

| Path | Accepted SHA-256 |
|---|---|
| `migrations/versions/20260830_0005_p1_6_durable_evidence_content.py` | `08457a5d5081440fdd7f3645209124f62656a9e3e1e736a15641b3e664b24742` |
| `src/aiscc/evidence/__init__.py` | `1d7a9fab82f0ef44a022939dea605b233dd13233c8294d1723072cebb8ec8951` |
| `src/aiscc/evidence/admission.py` | `0a259b0e1b93a69c63f88bbe9df788bf0348b9ace5a572afab539ee6d1589fc1` |
| `src/aiscc/evidence/content.py` | `22c9f94c82df3689f04c301363fddee9e5f626723f372737e452e40e0f5d2e3d` |
| `src/aiscc/evidence/models.py` | `9185887c7d6457447c299fb5839a36005a171a51a3214d528baee2e028ef1869` |
| `src/aiscc/evidence/ports.py` | `6bbe62f4c87ad437db202514640de850813c64b26bafc13d19fe66eda4f9d5ed` |
| `src/aiscc/evidence/repository.py` | `0daedf705980d4d800d114539ac0e4f428193b481206ff78b0b7e2bc600482d6` |
| `src/aiscc/evidence/requirements.py` | `e87783aba7bc1323754c27e52b95f15528a3ae35394c0edd083bb4ef84752080` |
| `src/aiscc/evidence/service.py` | `0055cd721bb61310b352b514ed4d2476062768d77d118a947fe9feb498d566e2` |
| `src/aiscc/persistence/models.py` | `3869e98c79ed3bc03afa00e1a6d81557e2547d74ed0e73927455d5a6495dbddd` |
| `tests/integration/evidence/test_postgres_evidence_admission.py` | `d9e4ccb470d0a484a64dbf64f8d887bc27039bdacb9a306c73eddad561ce1f0d` |
| `tests/integration/workflow/test_postgres_kernel.py` | `ef4c27672c6cc0d3d20bcf3eda4b5bb1841062d8922f771f5a8065f0bc29d825` |
| `tests/unit/evidence/test_durable_content.py` | `0fc71453328f0470ddd3323a7d262c7f55a6dc2b609c05deb7445621568ec9af` |

Recompute aggregate exactly:

```text
sort the 13 repository-relative paths ordinally

serialize UTF-8:
<path>\t<lowercase_sha256>\n

SHA-256 of the concatenated bytes
```

Require:

```text
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721
```

Any per-file or aggregate mismatch:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

No source/test/migration mutation is permitted after this check.

## 3.4 workspace inventory

Record:

```text
git status --short
git diff --name-only
git diff --cached --name-only
```

Index must be empty before Commit A.

Expected tracked dirty content consists of:

```text
exact 13 accepted runtime paths

plus uncommitted runtime governance lineage listed for Commit B

plus this Task while active
```

Unrelated tracked dirty path:

```text
STOP
→ DIRTY_WORKSPACE_MIXED
```

Ignored `.aiassistant/reports/target/**` bundles are review-only and must not be staged.

Never use:

```text
git add .
git add -A
git reset
git clean
```

---

# 4. accepted/reused verification evidence

Human acceptance is based on the exact candidate above.

Reuse exact final evidence:

## 4.1 complete repository

```text
command:
.\.venv\Scripts\pytest.exe -ra

collected:
195

passed:
195

failed:
0

skipped:
0

xfailed:
0

xpassed:
0

deselected:
0

duration:
65.57s
```

Collection delta:

```text
2357 predecessor:
194 PASS

current:
195 PASS

delta:
+1

added test:
tests/unit/evidence/test_durable_content.py
::test_historical_access_capability_is_owner_issued_and_purpose_fixed

removed tests:
0

test-discovery config change:
0
```

## 4.2 accepted targeted evidence

Reuse because the runtime bytes are unchanged:

```text
configured P1-6 writer capability binding:
PASS

rogue writer authority:
DENIED

service/repository split writer configuration:
DENIED

owner-issued historical read capability:
PASS

forged read grant:
DENIED

foreign read authority:
DENIED

valid P1_8_STRUCTURED_RESULT_V1 grant:
PUBLIC_SAFE + INTERNAL exact read PASS

V1 Requirement fingerprint:
legacy exact preserved

V2 durable Requirement:
explicit persisted schema

RequirementSet root:
legacy exact preserved

PostgreSQL durable content:
PASS

restart without process-local cache authority:
PASS

legacy P1-6 historical provenance:
PASS

legacy P1-7 Human/Judgment historical provenance:
PASS

legacy metadata-only P1-8 structured-source eligibility:
DENY

SECRET_FORBIDDEN durable rows:
0

P1-4 PostgreSQL regression:
18 PASS

P1-6 PostgreSQL regression:
7 PASS

P1-7 PostgreSQL regression:
2 PASS

PostgreSQL:
17.6

Alembic:
20260830_0005

ruff:
PASS

mypy:
67 source files PASS

provider/network/credential/deployment:
0
```

No new runtime tests are required for this terminal persistence Task.

Permitted verification:

```text
hashing
Git index/path-set inspection
commit blob verification
Markdown/UTF-8 validation
secret-pattern scan without printing values
```

If source bytes must change:

```text
STOP
→ ACCEPTED_RUNTIME_DRIFT
```

---

# 5. Commit A — exact accepted runtime

Stage exactly and only the 13 runtime paths in §3.3.

No `.aiassistant/**` path belongs in Commit A.

Use explicit path-based staging only.

Before commit:

```text
git diff --cached --name-only
```

must equal the exact 13-path set.

Compute the staged per-file SHA and aggregate.

Require:

```text
staged runtime aggregate
==
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721
```

Mismatch:

```text
STOP
→ STAGED_ACCEPTED_CANDIDATE_MISMATCH
```

Recommended exact commit message:

```text
feat(evidence): persist durable structured evidence content

Add the Human-accepted P1-6 durable evidence-content extension with bounded
PostgreSQL canonical bodies, restart-safe historical resolution, exact V1/V2
Requirement fingerprint compatibility, owner-bound write/read capabilities,
and legacy provenance preservation required by P1-8 structured sources.
```

Create Commit A.

Record:

```text
P1_6_DURABLE_CONTENT_RUNTIME_ACCEPTANCE_COMMIT=<40-char SHA>
```

Verify after commit:

```text
parent ==
bc446d9530e28f9b10602c9f1dd5232a97221a10

changed paths ==
exact 13 accepted runtime paths

.aiassistant/** in Commit A:
0
```

Recompute from Commit A blobs:

```text
13 paths /
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721
```

Failure:

```text
STOP
→ TERMINAL_RUNTIME_COMMIT_MISMATCH
```

Do not amend Commit A.

---

# 6. Commit B — terminal runtime governance + P1-8 resume handoff

Only begin after Commit A is verified and its exact SHA is known.

## 6.1 create runtime final acceptance Cycle

Create:

```text
.aiassistant/records/aiscc/cycles/
20260831_0912_aiscc-p1-6-durable-evidence-content-runtime-final-acceptance-1.cycle.md
```

The Cycle MUST contain the actual Commit A SHA.

No placeholder values.

Record at minimum:

```text
Human final review:
HUMAN_PROVIDED / ACCEPTED

P1-6 core:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 durable-content design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

accepted extension design commit:
32e88234ad7a7cbaa545e12f8c7e03b5897202cb

accepted extension design SHA:
ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411

accepted durable-content runtime Commit A:
<exact P1_6_DURABLE_CONTENT_RUNTIME_ACCEPTANCE_COMMIT>

accepted runtime:
13 paths
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721

complete repository:
195/195 PASS

P1-4 PostgreSQL:
18 PASS

P1-6 PostgreSQL:
7 PASS

P1-7 PostgreSQL:
2 PASS

PostgreSQL:
17.6

Alembic:
20260830_0005

ruff:
PASS

mypy:
67 source files PASS

provider/network/credential/deployment:
0

P1-8 runtime prerequisite:
SATISFIED

P1-8 Runtime:
NOT_STARTED / RESUME_AUTHORIZED / NEXT_ACTION

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Preserve exact runtime review lineage:

```text
2357 implementation candidate

0103 HOLD
→ writer capability self-mint
→ historical read grant self-mint

0103 rework
→ both authority findings CLOSED

0813 HOLD_REQUIRED_EVIDENCE
→ fresh complete-repository regression required after shared API boundary change

0813 verification
→ complete repository 195/195 PASS
→ candidate bytes unchanged

Human runtime final acceptance
```

## 6.2 persist runtime governance lineage

The following uncommitted runtime governance artifacts must be included in Commit B.

### implementation Task lifecycle

```text
.aiassistant/tasks/done/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md
```

### runtime rework Task

```text
.aiassistant/tasks/done/
20260831_0103_aiscc-p1-6-durable-content-writer-and-historical-read-capability-runtime-rework-1.md
```

### verification Task

```text
.aiassistant/tasks/done/
20260831_0813_aiscc-p1-6-durable-content-complete-repository-regression-verification-1.md
```

### runtime HOLD Cycle

```text
.aiassistant/records/aiscc/cycles/
20260831_0103_aiscc-p1-6-durable-content-runtime-writer-and-read-capability-authority-hold-1.cycle.md
```

### evidence HOLD Cycle

```text
.aiassistant/records/aiscc/cycles/
20260831_0813_aiscc-p1-6-durable-content-runtime-complete-repository-regression-evidence-hold-1.cycle.md
```

Do not rewrite these historical artifacts.

## 6.3 canonical state updates

Update exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Required canonical state:

```text
P1-6 core
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Runtime
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

accepted durable-content runtime commit
→ <exact Commit A SHA>

accepted durable-content runtime aggregate
→ 2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721

P1-8 Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 Runtime blocker
→ RESOLVED

P1-8 Runtime
→ NOT_STARTED / RESUME_AUTHORIZED

P2
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

`NEXT_ACTIONS.md` must advance the active priority to:

```text
P1-8 Runtime Resume
```

Do NOT mark P1-8 runtime implementation started.

## 6.4 create durable P1-8 resume handoff

Create:

```text
.aiassistant/reports/aiscc/
20260831_0912_aiscc-p1-6-durable-content-accepted-p1-8-runtime-resume-handoff-1.md
```

Purpose:

```text
allow a fresh Browser Command Center / Executor session to resume the already-Human-accepted P1-8 runtime
without relying on chat memory, File Library, or stale Project Source mirrors
```

The handoff must contain exact accepted predecessor facts only.

At minimum:

```text
P1-8 accepted design commit:
c108e9c02f222cf51ce833e311465584447b3571

P1-8 accepted design SHA:
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a

P1-8 design terminal governance:
b111f5f676e1a782de095e2f5b2a106d8b9a0207

P1-6 durable-content accepted design commit:
32e88234ad7a7cbaa545e12f8c7e03b5897202cb

P1-6 durable-content accepted design SHA:
ab54948fb8c253309d5a8c228e31fca1b9afb9e19f0faf9be9cda8d14b735411

P1-6 durable-content accepted runtime commit:
<exact Commit A SHA>

P1-6 durable-content runtime aggregate:
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721

P1-6 durable historical-content API boundary:
P1-6 owner write only
P1-8 owner-issued historical read grant only
P1_8_STRUCTURED_RESULT_V1 purpose
PUBLIC_SAFE + INTERNAL internal derivation read
no write/export authority

Requirement compatibility:
V1 exact historical fingerprints/root preserved
V2 durable-capable Requirements only prospectively

legacy metadata-only evidence:
P1-6 historical valid
P1-8 structured-source NOT eligible

P1-8 runtime blocker:
RESOLVED
```

Also restate the load-bearing P1-8 accepted invariants necessary for resume:

```text
CommandCenterCycleRecord != AdmittedCycle

raw session != ProjectMemory

Judgment != CycleAdmissionDecision

TransitionDecision != CycleAdmissionDecision

historical source provenance
!= current source effectiveness
!= current ProjectMemory applicability

historical policy validity
!= current policy applicability

ProjectMemoryEntryId != MemoryLineageKey

one CURRENT tip per lineage

EXPLICIT_SUPERSESSION_ONLY

LESSON
→ NOT_SUPPORTED

NextActionProposal
!= NextActionSelection
!= TransitionDecision

enrolled ActionRef eligibility
→ before ranking

TaskIssuanceCandidate
!= TaskContract

Task authority:
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
```

Do not redesign P1-8 in the handoff.

## 6.5 closure Task lifecycle

Move this Task:

```text
.aiassistant/tasks/active/
20260831_0912_aiscc-p1-6-durable-evidence-content-runtime-terminal-acceptance-and-p1-8-resume-handoff-1.md
```

to:

```text
.aiassistant/tasks/done/
20260831_0912_aiscc-p1-6-durable-evidence-content-runtime-terminal-acceptance-and-p1-8-resume-handoff-1.md
```

before Commit B.

---

# 7. Commit B exact allowlist

Stage exactly 11 governance/provenance paths:

```text
1. 2357 implementation Task done
2. 0103 runtime rework Task done
3. 0813 verification Task done
4. 0103 runtime HOLD Cycle
5. 0813 evidence HOLD Cycle
6. new 0912 runtime final acceptance Cycle
7. CURRENT_STATE_SUMMARY.md
8. DECISION_REGISTER.md
9. NEXT_ACTIONS.md
10. new P1-8 runtime resume handoff
11. current 0912 closure Task done
```

Exact paths:

```text
.aiassistant/tasks/done/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md

.aiassistant/tasks/done/
20260831_0103_aiscc-p1-6-durable-content-writer-and-historical-read-capability-runtime-rework-1.md

.aiassistant/tasks/done/
20260831_0813_aiscc-p1-6-durable-content-complete-repository-regression-verification-1.md

.aiassistant/records/aiscc/cycles/
20260831_0103_aiscc-p1-6-durable-content-runtime-writer-and-read-capability-authority-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260831_0813_aiscc-p1-6-durable-content-runtime-complete-repository-regression-evidence-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260831_0912_aiscc-p1-6-durable-evidence-content-runtime-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md

.aiassistant/records/aiscc/DECISION_REGISTER.md

.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/reports/aiscc/
20260831_0912_aiscc-p1-6-durable-content-accepted-p1-8-runtime-resume-handoff-1.md

.aiassistant/tasks/done/
20260831_0912_aiscc-p1-6-durable-evidence-content-runtime-terminal-acceptance-and-p1-8-resume-handoff-1.md
```

No source/test/migration path belongs in Commit B.

No accepted design rule belongs in Commit B.

No `.aiassistant/reports/target/**`.

No Project Source mirror sync.

Before commit:

```text
git diff --cached --name-only
```

must equal exact 11-path set.

Verify:

```text
src/**:
0

tests/**:
0

migrations/**:
0
```

Verify final acceptance Cycle and P1-8 resume handoff contain the actual Commit A SHA.

Verify no placeholder commit IDs.

UTF-8/control-character checks:

```text
PASS
```

Secret scan without printing values:

```text
PASS
```

---

# 8. Commit B

Recommended exact commit message:

```text
chore(governance): accept durable evidence content runtime

Record Human final acceptance of the P1-6 durable evidence-content runtime,
preserve its runtime review and verification provenance, resolve the P1-8
durable-content prerequisite, and open P1-8 runtime resume without starting it.
```

Create Commit B.

Record:

```text
P1_6_DURABLE_CONTENT_RUNTIME_TERMINAL_COMMIT=<40-char SHA>
```

Do not amend Commit A or B.

---

# 9. terminal lineage verification

Require exact first-parent lineage:

```text
32e88234ad7a7cbaa545e12f8c7e03b5897202cb
→ bc446d9530e28f9b10602c9f1dd5232a97221a10
→ P1_6_DURABLE_CONTENT_RUNTIME_ACCEPTANCE_COMMIT
→ P1_6_DURABLE_CONTENT_RUNTIME_TERMINAL_COMMIT
```

Equivalently, from current HEAD:

```text
bc446d9530e28f9b10602c9f1dd5232a97221a10
→ Commit A
→ Commit B
```

Verify:

```text
Commit A:
exact 13 runtime paths
aggregate 2290da92...
no governance

Commit B:
exact 11 governance paths
no runtime source/test/migration
terminal Cycle binds exact Commit A
resume handoff binds exact Commit A
canonical state says extension runtime ACCEPTED/CLOSED
P1-8 runtime says NOT_STARTED / RESUME_AUTHORIZED
```

Final HEAD must equal Commit B.

Tracked worktree/index after Commit B:

```text
clean
```

Ignored target bundles may remain.

No push.

No remote action.

---

# 10. mandatory stop conditions

STOP before Commit A on:

```text
HEAD drift

accepted design SHA drift

accepted runtime per-file SHA drift

accepted runtime aggregate drift

unexpected tracked dirty file

runtime candidate already partially committed

index not empty
```

After Commit A exists, if Commit B is blocked:

```text
do not amend/revert Commit A

STOP
→ TERMINAL_GOVERNANCE_PERSISTENCE_BLOCKED

report exact Commit A SHA
and exact blocker
```

STOP on Commit B staged mismatch:

```text
TERMINAL_GOVERNANCE_STAGED_SET_MISMATCH
```

Do not use reset/clean/amend as workaround.

---

# 11. evidence contract

## executor_required

### RUNTIME_IDENTITY

```text
13 per-file SHA
working-tree aggregate
staged aggregate
Commit A blob aggregate

all:
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721
```

### GIT_PROVENANCE

```text
Commit A exact 13 paths
Commit B exact 11 paths
first-parent lineage
no amend
no push
```

### GOVERNANCE_PROVENANCE

```text
Human runtime acceptance
actual Commit A binding
0103/0813 lineage
canonical state
P1-8 resume handoff
```

### STATIC_GOVERNANCE

```text
UTF-8
Markdown
control-character scan
secret-pattern scan
```

## reuse_allowed

```text
complete repository:
195/195 PASS

0103 targeted authority evidence

P1-4/P1-6/P1-7 regressions

PostgreSQL 17.6

Alembic 20260830_0005

ruff PASS

mypy PASS / 67 files

Human final runtime acceptance:
HUMAN_PROVIDED / ACCEPTED
```

## human_owned

```text
none remaining for P1-6 durable-content extension closure
```

## not_required

```text
new runtime test
new migration
P1-8 implementation
browser QA
deployment
provider/network
```

## forbidden

```text
runtime source mutation
P1-8 runtime implementation
P2/P3
git add .
git add -A
git reset
git clean
git amend
git rebase
git push
deployment/Public Live
```

---

# 12. export

Target:

```text
.aiassistant/reports/target/
20260831_0912_aiscc-p1-6-durable-evidence-content-runtime-terminal-acceptance-and-p1-8-resume-handoff-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
GIT_PROVENANCE.md
```

Include byte-preserving copies of:

```text
0912 runtime final acceptance Cycle

CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md

P1-8 resume handoff

0912 closure Task done
```

Include exact runtime 13-path hash inventory.

No need to duplicate all runtime source files if Commit A blob/per-file identity is fully recorded.

Manifest must report:

```text
start HEAD

Commit A
Commit B
final HEAD

Commit A exact 13 paths
Commit B exact 11 paths

accepted runtime aggregate

terminal Cycle path/SHA
resume handoff path/SHA

canonical state paths/SHA

source/copy identity
```

---

# 13. Executor report required fields

Report exact:

1. Task path
2. start HEAD
3. accepted extension design SHA
4. accepted runtime 13 per-file SHA verification
5. accepted runtime aggregate verification
6. preflight workspace inventory
7. Commit A staged exact 13 paths
8. Commit A staged aggregate
9. Commit A SHA
10. Commit A parent
11. Commit A changed-path set
12. Commit A blob aggregate
13. Human runtime final acceptance
14. runtime final acceptance Cycle path
15. Cycle actual Commit A binding
16. 0103 HOLD/rework provenance persisted
17. 0813 evidence HOLD/verification provenance persisted
18. complete repository 195/195 reused
19. canonical CURRENT_STATE_SUMMARY update
20. canonical DECISION_REGISTER update
21. canonical NEXT_ACTIONS update
22. P1-8 resume handoff path
23. P1-8 resume handoff actual Commit A binding
24. closure Task active→done
25. Commit B staged exact 11 paths
26. Commit B SHA
27. Commit B parent
28. Commit B changed-path set
29. final first-parent lineage
30. final HEAD
31. final tracked worktree/index
32. P1-6 durable-content extension runtime status
33. P1-8 blocker status
34. P1-8 runtime status
35. P2 status
36. PUBLIC_BOUNDED_LIVE status
37. Git push = NOT_RUN
38. preserved exact paths
39. next recommendation

---

# 14. expected final response

Return:

```text
result:
COMPLETED

P1-6 Durable Evidence Content Extension Runtime:
HUMAN_PROVIDED / ACCEPTED / CLOSED

Commit A:
<exact SHA>

Commit B:
<exact SHA>

lineage:
bc446d9530e28f9b10602c9f1dd5232a97221a10
→ <Commit A>
→ <Commit B>

runtime:
13 paths /
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721

P1-8 prerequisite:
SATISFIED

P1-8 Runtime:
NOT_STARTED / RESUME_AUTHORIZED

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED

Git push:
NOT_RUN
```

---

# 15. preserved exact paths after successful closure

Explicitly preserve:

```text
.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md

.aiassistant/records/aiscc/cycles/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260831_0103_aiscc-p1-6-durable-content-runtime-writer-and-read-capability-authority-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260831_0813_aiscc-p1-6-durable-content-runtime-complete-repository-regression-evidence-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260831_0912_aiscc-p1-6-durable-evidence-content-runtime-final-acceptance-1.cycle.md

.aiassistant/tasks/done/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md

.aiassistant/tasks/done/
20260831_0103_aiscc-p1-6-durable-content-writer-and-historical-read-capability-runtime-rework-1.md

.aiassistant/tasks/done/
20260831_0813_aiscc-p1-6-durable-content-complete-repository-regression-verification-1.md

.aiassistant/tasks/done/
20260831_0912_aiscc-p1-6-durable-evidence-content-runtime-terminal-acceptance-and-p1-8-resume-handoff-1.md

.aiassistant/reports/aiscc/
20260831_0912_aiscc-p1-6-durable-content-accepted-p1-8-runtime-resume-handoff-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

The target export bundle remains review-only and deletable after Command Center judgment unless explicitly
preserved later.
