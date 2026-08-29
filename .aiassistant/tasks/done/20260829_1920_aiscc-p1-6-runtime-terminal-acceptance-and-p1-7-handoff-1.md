# 작업지시서: P1-6 Runtime Terminal Acceptance + P1-7 Handoff

## meta

- task_id: `20260829_1920_aiscc-p1-6-runtime-terminal-acceptance-and-p1-7-handoff-1`
- created_at: `2026-08-29T19:20:00+09:00`
- phase: `P1-6 Evidence Admission`
- work_type: `COMMAND_CENTER_RECORD_UPDATE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1-6_EVIDENCE`
- expected_start_head: `192e223854a02293809cf6675e3a329e099e628d`
- accepted_design_sha256: `0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463`
- reviewed_runtime_candidate_count: `21`
- reviewed_runtime_candidate_aggregate_sha256: `a583647cc94028874aaf78727e854b537dd033a3670332737aaa7fa53d6469f9`
- human_final_result: `HUMAN_PROVIDED / ACCEPTED`
- p1_7_status_before_closure: `NOT_STARTED`
- p1_8_status_before_closure: `NOT_STARTED`
- public_bounded_live_release: `NOT_RELEASED`

---

# 1. Human terminal decision

This Task carries an explicit Human final result:

```text
Human P1-6 runtime final review
판정: ACCEPTED
```

This Human acceptance applies **only** to the exact runtime candidate reviewed by the Browser Command Center from:

```text
20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-rework-1
```

Do not reinterpret acceptance as permission to modify the candidate before persistence.

Required non-substitution:

```text
Human accepted reviewed candidate
!= Human accepted later modified candidate
```

Any candidate drift:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

---

# 2. current repository state

Expected start:

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
192e223854a02293809cf6675e3a329e099e628d
```

This HEAD is the accepted P1-6 design terminal persistence commit and MUST NOT be amended/reverted.

Expected current working tree contains the uncommitted P1-6 runtime candidate and governance provenance produced by the 1241/1513/1617 Tasks.

P1-7 and P1-8 remain:

```text
NOT_STARTED
```

until this closure completes.

---

# 3. Task goals

Perform terminal persistence in two explicit commits.

```text
Commit A
→ exact Human-accepted P1-6 runtime implementation
→ implementation Task/HOLD provenance

Commit B
→ terminal Human acceptance Cycle
→ canonical state/decision/next-action closure
→ closure Task provenance
→ P1-7 handoff
```

No new runtime behavior may be implemented in this Task.

---

# 4. Stage A0 — predecessor / candidate identity verification

Before any mutation or staging:

## 4.1 HEAD

Verify:

```text
HEAD == 192e223854a02293809cf6675e3a329e099e628d
```

Mismatch:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

## 4.2 accepted design

Verify:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

SHA-256:
0d9d4c194efda37f100c6183d1a7e88e1a09fe073dc3a37bbb5a3e1cd577e463
```

Mismatch:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

## 4.3 reviewed runtime candidate exact identity

The exact 21-path reviewed candidate is frozen below.

Canonical aggregate algorithm:

```text
1. use exactly the 21 rows below
2. sort by repository-relative path ascending
3. serialize each row as:
   <path>\t<lowercase_sha256>\n
4. SHA-256 the UTF-8 byte sequence
```

Expected aggregate:

```text
a583647cc94028874aaf78727e854b537dd033a3670332737aaa7fa53d6469f9
```

Exact reviewed candidate:

| repository-relative path | SHA-256 |
|---|---|
| `migrations/versions/20260829_0003_p1_6_evidence_admission.py` | `ff62663bc85a09ebad38f4f0e8665f2039d9c8bdbb1a46733cfb17d629d46058` |
| `src/aiscc/evidence/__init__.py` | `84dc2e6bff4cfd7fdb84f723007a6db284b4549176b709bffe2e51fdbfe558e5` |
| `src/aiscc/evidence/admission.py` | `6d4e4dcbd9617427ddd6af579805cbbe7f234b2f53c8a5bb866abc8b862e4bcd` |
| `src/aiscc/evidence/attestation.py` | `3ccfbbfafdd35ed45e6cacd696cdabc90b72937c438ae876961236600d244952` |
| `src/aiscc/evidence/checkpoints.py` | `a4fe46fdbec8b9363bf7600da76e04da1361661eeffd4dcd3ed0f712529df8b4` |
| `src/aiscc/evidence/content.py` | `ee77d1e95dea082a6a92896bf6dbdba34b5e695c36a480850a1bc38a4c17f893` |
| `src/aiscc/evidence/events.py` | `e65d9c2a5681f118449e63321faaffe494a4311f04398e03464ea5ffcb48e124` |
| `src/aiscc/evidence/issuers.py` | `63235a2bf2fb819d30364189f6dc34da33c85a72f336a6876a644af988103242` |
| `src/aiscc/evidence/models.py` | `c11c5ff5770abb41fbcd03ca9902c5a096b54833e3037626d97c571f13fd71ea` |
| `src/aiscc/evidence/ports.py` | `184b0dbb17476542e14662b03d9346a031d85a0f311e974f63257b2f411ba2d0` |
| `src/aiscc/evidence/repository.py` | `b9d10537b482b1fdac11d36bfcb06ad28e8b1267f24df9c884fb19f36d2b345b` |
| `src/aiscc/evidence/requirements.py` | `096c510b7002c4f7e1477a01dce80c15e20eba6f55457606f6fab14496aa4bcd` |
| `src/aiscc/evidence/service.py` | `8ba63e5be0eec9dd3b75df32bc72f09643d68ba1da9c94592be0e130c8c3d129` |
| `src/aiscc/evidence/set_evaluator.py` | `20a55452434ea43778cf3ee9ba7f5179c098c202a8a39e49c93fee26aa78620e` |
| `src/aiscc/persistence/models.py` | `23b4c43d7f722fb93fd2277567ad6e33e9610bb6b43e42ce7eb77b8c8572da8a` |
| `src/aiscc/persistence/repository.py` | `a307c5ee437162edbef8b75c677c485f95d00bfa1ceb873bab2b6319869153ab` |
| `src/aiscc/workflow/guards.py` | `40640a0c8a8eb04c4256d2b8db29c7121f2df5586a940da7d1de0129d7e9205e` |
| `tests/integration/evidence/test_postgres_evidence_admission.py` | `3662b34beb046a2796e4793d57521df1e2d11538ac65f57bb44bd3b8094b429f` |
| `tests/integration/workflow/test_postgres_kernel.py` | `67470936bec15e10006676af8d3fa41ab0b1e3ff757b22d09982b321e996442b` |
| `tests/unit/evidence/test_admission_domain.py` | `8e171fc2e036671be8616e310ee7691cda972109153b5a764be6184887605c0f` |
| `tests/unit/workflow/test_state_machine.py` | `15206e31da009bd719bf65330adfc48f19bb99a3b5a731382c5f979954bb50a7` |

Every path must:

```text
exist
match exact SHA-256
have no content mutation before Commit A
```

If any mismatch:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

Do not re-run implementation to “restore” acceptance silently.

## 4.4 implementation provenance artifact verification

Verify expected durable artifacts exist and have no policy conflict:

```text
.aiassistant/tasks/done/
20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1.md

.aiassistant/tasks/done/
20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1.md

.aiassistant/tasks/done/
20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-rework-1.md

.aiassistant/records/aiscc/cycles/
20260829_1513_aiscc-p1-6-evidence-admission-runtime-authority-gap-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-hold-1.cycle.md
```

The 1617 reviewed provenance hashes from the accepted review bundle are:

```text
1617 Task body SHA-256:
bc73c67a48d7c8a1ec57377a11af43e32b21f892797b71862cbc0fdda101e407

1617 HOLD Cycle SHA-256:
4c8015802f102e9b16631bc8e0cb4e77fc4095a987f088c42791f0995c0b8c9f
```

If these two differ, STOP and report provenance drift.

---

# 5. Stage A1 — minimal re-verification before acceptance commit

Human acceptance was already given after Command Center source/test review.

Do not broaden scope or redesign code.

Before Commit A, execute only narrow identity/integrity confirmation:

```text
git diff --check

exact 21-path SHA verification

UTF-8 / no secret / no forbidden artifact check

targeted smoke sufficient to show candidate did not become non-runnable
```

The full predecessor verification may be reused because current candidate bytes must be identical.

Required reused evidence:

```text
P1-6 / WorkRun freshness proof
P1-4 regression 48 PASS
P1-5 unit 43 PASS
P1-5 integration 28 PASS
unique targeted/regression total 132 PASS
PostgreSQL 17.6
empty DB → head PASS
20260828_0002 → head PASS
real provider calls 0
```

Do not run real provider/network/credential actions.

If the repository toolchain requires a deterministic local no-network targeted test to confirm environment integrity, it is allowed. Do not expand to unrelated full-suite execution.

---

# 6. Commit A — exact P1-6 runtime acceptance commit

Commit A is explicitly authorized.

## 6.1 allowed runtime paths

Exactly the 21 reviewed runtime candidate paths above.

No changed runtime byte is allowed before staging.

## 6.2 implementation provenance paths allowed in Commit A

Also include only these existing durable P1-6 implementation lineage artifacts if currently uncommitted:

```text
.aiassistant/tasks/done/
20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1.md

.aiassistant/tasks/done/
20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1.md

.aiassistant/tasks/done/
20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-rework-1.md

.aiassistant/records/aiscc/cycles/
20260829_1513_aiscc-p1-6-evidence-admission-runtime-authority-gap-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-hold-1.cycle.md
```

Do not include:

```text
terminal 1920 acceptance Cycle
canonical state updates
closure Task
unrelated handoff/report
unrelated dirty files
```

## 6.3 exact staging rule

Forbidden:

```text
git add .
git add -A
broad glob staging that captures unrelated files
```

Stage exact allowlisted paths only.

Before commit:

```text
git diff --cached --name-only
```

must be a subset of the exact Commit A allowlist.

Any unexpected staged path:

```text
STOP
→ DIRTY_WORKSPACE_MIXED
```

## 6.4 Commit A message

Recommended exact message:

```text
feat(evidence): accept P1-6 evidence admission runtime

Persist the Human-accepted P1-6 evidence admission runtime, including durable
evidence provenance, checkpoint-bound G_EVIDENCE authority, Human direct ingress,
reuse/revocation safeguards, and authoritative WorkRun freshness with the shared
P1-4 concurrency boundary.

Preserve the implementation and rework Task/Cycle lineage that led to terminal
acceptance without starting P1-7 or P1-8.
```

After Commit A:

- record exact commit hash as `P1_6_RUNTIME_ACCEPTANCE_COMMIT`
- verify the commit contains only the allowlist
- verify the 21 runtime blob contents still match the reviewed hashes

If commit fails:

```text
STOP
```

Do not proceed to canonical closure.

---

# 7. Stage B0 — terminal Cycle placement

Place the Command Center-provided terminal Cycle at:

```text
.aiassistant/records/aiscc/cycles/
20260829_1920_aiscc-p1-6-evidence-admission-runtime-final-acceptance-1.cycle.md
```

Before Commit B, replace only this placeholder:

```text
runtime acceptance commit:
TO_BE_FILLED_BY_CLOSURE_TASK_AFTER_EXACT_CANDIDATE_COMMIT
```

with the exact Commit A hash.

Do not change Human judgment semantics.

Cycle result must remain:

```text
P1-6 Evidence Admission Runtime
→ HUMAN_PROVIDED / ACCEPTED / CLOSED
```

---

# 8. Stage B1 — canonical state updates

Update exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Required state:

```text
P1-5 Provider / Tool Execution
→ ACCEPTED / CLOSED

P1-6 Evidence Admission Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Evidence Admission Runtime
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-7 Human Gate and Judgment
→ NOT_STARTED / CURRENT NEXT PHASE

P1-8 Project Memory and Cycle Admission
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

`CURRENT_STATE_SUMMARY.md` must record:

```text
P1-6 runtime acceptance commit:
<Commit A hash>

terminal P1-6 runtime Cycle:
20260829_1920_aiscc-p1-6-evidence-admission-runtime-final-acceptance-1.cycle.md
```

`DECISION_REGISTER.md` must preserve the P1-6 authority boundary, at minimum:

```text
EvidenceCandidate != AdmittedEvidence
AdmittedEvidenceRef != G_EVIDENCE
EvidenceSetSatisfactionAttestation != TransitionDecision
HUMAN_DIRECT_EVIDENCE != HUMAN_P1_7
P1-6 owns only exact G_EVIDENCE fact/attestation
```

and mark runtime implementation/verification `ACCEPTED / CLOSED`.

`NEXT_ACTIONS.md`:

- do not reorder the stable roadmap;
- promote current action from P1-6 to P1-7;
- state that P1-7 must begin with Human Gate/Judgment authority design before runtime implementation;
- do not mark P1-7 started merely because it is next.

---

# 9. durable handoff report

The following existing curated handoff must remain preserved:

```text
.aiassistant/reports/aiscc/
20260829_1227_aiscc-p1-6-design-accepted-command-center-handoff-1.md
```

If it is currently untracked, it may be included in Commit B only if:

```text
its content is unchanged from the Human-provided handoff
and
SHA-256 == a188eb64eceb297513d2e4b6e0f7626a966d51fb10c5468f1739772a19bac3ff
```

If it is already tracked/committed, do not touch it.

If local content differs, do not overwrite it; report the drift and leave it out of Commit B unless the difference is an exact filename-only copy issue that can be proven byte-identical.

---

# 10. closure Task lifecycle

This Task starts at:

```text
.aiassistant/tasks/active/
20260829_1920_aiscc-p1-6-runtime-terminal-acceptance-and-p1-7-handoff-1.md
```

After all closure work/report/export is complete, move it to:

```text
.aiassistant/tasks/done/
20260829_1920_aiscc-p1-6-runtime-terminal-acceptance-and-p1-7-handoff-1.md
```

The done Task is included in Commit B.

---

# 11. Commit B — terminal governance closure

Commit B is explicitly authorized only after Commit A succeeds.

Allowed paths:

```text
.aiassistant/records/aiscc/cycles/
20260829_1920_aiscc-p1-6-evidence-admission-runtime-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md

.aiassistant/records/aiscc/DECISION_REGISTER.md

.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/tasks/done/
20260829_1920_aiscc-p1-6-runtime-terminal-acceptance-and-p1-7-handoff-1.md
```

Conditional allowed path, only under section 9 exact hash rule:

```text
.aiassistant/reports/aiscc/
20260829_1227_aiscc-p1-6-design-accepted-command-center-handoff-1.md
```

No product/runtime source belongs in Commit B.

Recommended exact Commit B message:

```text
chore(governance): close P1-6 and hand off P1-7

Record the Human final acceptance of the exact P1-6 evidence admission runtime,
bind the accepted runtime commit into terminal Cycle provenance, update canonical
AISCC state and decision records, and advance the next phase to P1-7 Human Gate
and Judgment without starting its implementation.
```

After Commit B:

```text
P1-6:
ACCEPTED / CLOSED

P1-7:
NOT_STARTED / NEXT
```

No push is authorized.

---

# 12. forbidden actions

This closure Task MUST NOT:

```text
modify any of the 21 runtime candidate bytes
implement new runtime behavior
create P1-7 source
create P1-8 source
change WorkflowState set
change transition matrix
change accepted P1-6 design
amend/rebase/rewrite 192e2238...
git push
create/merge PR
tag/release
deploy
enable PUBLIC_BOUNDED_LIVE
call real provider
use credentialed external action
clean/reset unrelated dirty files
```

---

# 13. evidence contract

## executor_required

### CANDIDATE_IDENTITY

Pass:

```text
21/21 exact SHA match
aggregate SHA match
```

### GIT_PROVENANCE

Pass:

```text
start HEAD exact

Commit A contains exact accepted runtime/provenance allowlist only

Commit B contains exact terminal governance allowlist only

no broad staging

no push
```

### STATIC_INTEGRITY

Pass:

```text
git diff --check
UTF-8/control-character validation
secret/private scan
```

### REUSED_ACCEPTED

Reuse exact predecessor evidence because candidate bytes are frozen:

```text
132 PASS targeted/regression
PostgreSQL 17.6
empty → head migration PASS
20260828_0002 → head migration PASS
WorkRun stale proof PASS
transition/admission race proof PASS
restart proof PASS
previous four HOLD closures PASS
```

Applicability condition:

```text
21-path exact SHA identity must match
```

## human_owned

```text
P1-6 runtime final review
→ HUMAN_PROVIDED / ACCEPTED
```

No additional Human verification is required for code semantics in this closure unless candidate identity drifts.

## not_required

```text
new browser QA
new provider calls
deployment
public release
new DB environment
P1-7 verification
```

## forbidden

```text
candidate mutation
P1-7/P1-8 implementation
remote Git action
deployment
real provider
```

---

# 14. mandatory stop

Stop immediately on:

```text
BLOCKED_PREDECESSOR_HEAD_DRIFT

REVIEWED_CANDIDATE_DRIFT

accepted design SHA mismatch

1617 Task/Cycle provenance hash mismatch

unexpected staged path

unrelated dirty collision affecting allowlisted paths

secret/private material in commit candidate

Commit A failure

policy conflict
```

After stop:

- do not mutate runtime candidate;
- do not create Commit B;
- collect minimum report/export evidence.

---

# 15. report requirements

`EXECUTOR_REPORT.md` must include:

1. task path
2. start HEAD
3. accepted design SHA expected/actual
4. exact 21 candidate hash verification result
5. aggregate SHA expected/actual
6. implementation lineage artifact verification
7. reused verification evidence with provenance/applicability
8. Commit A staged exact path list
9. Commit A hash
10. Commit A committed exact path list
11. post-Commit-A candidate hash recheck
12. terminal Cycle placement and runtime commit insertion
13. canonical state changes
14. conditional handoff report handling
15. Commit B staged exact path list
16. Commit B hash
17. Commit B committed exact path list
18. final HEAD
19. final index/status
20. product source changes
21. governance/provenance changes
22. repository configuration changes
23. provider/network/credential actions
24. P1-7/P1-8 source creation check
25. secret/private scan
26. preserved exact paths
27. final phase status
28. next recommendation

---

# 16. target bundle

Create:

```text
.aiassistant/reports/target/
20260829_1920_aiscc-p1-6-runtime-terminal-acceptance-and-p1-7-handoff-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Also export changed governance files preserving repository-relative paths.

Do not export all 21 unchanged-after-Commit-A source files merely to duplicate the prior accepted review bundle unless report/export canonical rules require commit-diff copies. Their reviewed identity is already frozen by this Task and Git Commit A.

---

# 17. final state and next action

Success result:

```text
P1-6 Evidence Admission Design
→ ACCEPTED / CLOSED

P1-6 Evidence Admission Runtime
→ ACCEPTED / CLOSED

P1-7 Human Gate and Judgment
→ NOT_STARTED
→ NEXT PHASE

P1-8
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

Next Command Center action after successful closure:

```text
issue P1-7 Human Gate and Judgment design Task
```

Do not directly implement P1-7 in this closure Task.

---

# 18. preserved exact paths

Must survive cleanup:

```text
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

.aiassistant/tasks/done/
20260829_1241_aiscc-p1-6-evidence-admission-implementation-and-runtime-verification-1.md

.aiassistant/tasks/done/
20260829_1513_aiscc-p1-6-human-ingress-revocation-and-reuse-authority-rework-1.md

.aiassistant/tasks/done/
20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-rework-1.md

.aiassistant/tasks/done/
20260829_1920_aiscc-p1-6-runtime-terminal-acceptance-and-p1-7-handoff-1.md

.aiassistant/records/aiscc/cycles/
20260829_1241_aiscc-p1-6-evidence-admission-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260829_1513_aiscc-p1-6-evidence-admission-runtime-authority-gap-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260829_1617_aiscc-p1-6-authoritative-workrun-admission-freshness-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260829_1920_aiscc-p1-6-evidence-admission-runtime-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md

.aiassistant/records/aiscc/DECISION_REGISTER.md

.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/reports/aiscc/
20260829_1227_aiscc-p1-6-design-accepted-command-center-handoff-1.md
```

---

# 19. final response format

1. result
2. start HEAD
3. 21-path candidate identity result
4. aggregate SHA result
5. Commit A hash + exact files
6. terminal Cycle path
7. canonical state update summary
8. Commit B hash + exact files
9. final HEAD/index/status
10. reused verification evidence
11. provider/network/credential actions
12. P1-7/P1-8 status
13. preserved exact paths
14. next recommendation
