# 작업지시서: P1-8 JCS Safe-Integer Joint Design Terminal Acceptance Persistence

## meta

- task_id: `20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1`
- created_at: `2026-09-01T21:55:00+09:00`
- phase: `P1-8 Runtime Prerequisite Authority Contracts`
- work_type: `HUMAN_ACCEPTANCE_TERMINAL_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `CROSS_OWNER / AISCC_COMMAND_CENTER`
- expected_start_branch: `main`
- expected_start_head: `683aaee84d1fc09e9371dd214efc3ff58b7225ee`
- historical_source_design_commit: `35901125cc5842734cf1e8eb3374d10e4ee866e3`
- prior_terminal_governance_commit: `683aaee84d1fc09e9371dd214efc3ff58b7225ee`
- accepted_source_rule_path: `.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md`
- accepted_source_rule_sha256: `7cf27b77bb961280becfc55ecf8e71c9406da9b7b91df0d2697132c2655108db`
- accepted_prerequisite_rule_path: `.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md`
- accepted_prerequisite_rule_sha256: `8b19970629c55629df1560f2329b529992eceb86d5e4216baf0b7e78d3876960`
- accepted_joint_bundle_sha256: `e36e8849782ba0fb2c3030ec642108d29881a2af198056329acaf3d32110e0fc`
- accepted_jcs_evidence_sha256: `30455e1d5facd1ffbd3d74d59854f8354a855718f947b9244e15446a49de5f2c`
- accepted_executor_report_sha256: `ad53c797a8d2b9c2643ea254c7cc5fb0c94e7ca6365ed39b6b165dac0a606da9`
- command_center_review: `SUBSTANTIVE_REVIEW_PERFORMED / ACCEPTED_CANDIDATE`
- human_joint_final_review: `HUMAN_PROVIDED / ACCEPTED`
- blocked_runtime_path_count: `19`
- blocked_runtime_aggregate_sha256: `84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42`
- git_mutation: `EXACT_TWO_COMMIT_SEQUENCE_AUTHORIZED`
- git_push: `FORBIDDEN`

---

# 1. purpose

Persist the exact Human-accepted joint design candidate produced by:

```text
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1
```

The accepted joint candidate consists of exactly two cross-bound rules:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
SHA-256:
7cf27b77bb961280becfc55ecf8e71c9406da9b7b91df0d2697132c2655108db

.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
SHA-256:
8b19970629c55629df1560f2329b529992eceb86d5e4216baf0b7e78d3876960
```

This Task closes only the design authority contracts:

```text
NEXT_ACTION_CONTEXT Source Authority corrected revision
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 prerequisite owner-authority exact contract and source enrollment design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED
```

It does not accept the existing 19-path P1-8 runtime candidate. It removes the prerequisite design blocker and
authorizes a later, separately reviewed runtime rework/resume Task.

---

# 2. Human authority input and binding

The fourth Browser Command Center session presented both exact candidate SHA values as one joint Human final review
set after an independent substantive review.

Human response, exact text:

```text
Accept
```

Contextual binding resolved by the Command Center:

```text
accepted scope:
- source candidate 7cf27b77...
- prerequisite candidate 8b199706...

decision:
HUMAN_PROVIDED / ACCEPTED

binding kind:
JOINT_EXACT_BYTES
```

Do not generalize this Human decision to:

- another revision of either rule
- the 19-path runtime candidate
- P2/P3
- public deployment or bounded Live
- Project Source mirror synchronization

If either accepted rule byte identity differs, stop before staging:

```text
REVIEWED_CANDIDATE_DRIFT
```

---

# 3. accepted review evidence

Command Center substantive review independently established:

```text
archive structure / CRC / path safety:
PASS

22 canonical JCS payloads independently recomputed:
22 / 22 PASS

documented vs recomputed fingerprint mismatch:
0

current normative unsafe JSON integer count:
0

cross-contract fingerprint mismatch:
0

predecessor semantic drift outside the authorized safe-integer correction:
0

UTF-8 / BOM / control / secret signature / Markdown fence problems:
0
```

Accepted evidence identities:

```text
1652 target Task/done Task:
4adee46da6c85e1a69cf672db755af69a38bae1dc3c342f490e06dab167fc3e7

EXECUTOR_REPORT.md:
ad53c797a8d2b9c2643ea254c7cc5fb0c94e7ca6365ed39b6b165dac0a606da9

JCS_FINGERPRINT_EVIDENCE.md:
30455e1d5facd1ffbd3d74d59854f8354a855718f947b9244e15446a49de5f2c

EXPORT_MANIFEST.md:
1949e69bd454cbe64a7dcb83831e03a1186b84c2680c726fbaffe1325737d607
```

The issued Browser Task had one additional trailing LF. The repository done Task and bundle `TASK.md` are internally
byte-identical and semantically identical. This transport normalization was independently classified as non-blocking.

---

# 4. mandatory preflight

Before any mutation, require:

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
683aaee84d1fc09e9371dd214efc3ff58b7225ee

index:
empty
```

Require exact accepted rule identities:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
7cf27b77bb961280becfc55ecf8e71c9406da9b7b91df0d2697132c2655108db

.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
8b19970629c55629df1560f2329b529992eceb86d5e4216baf0b7e78d3876960
```

Require historical immutable lineage:

```text
historical source design Commit A:
35901125cc5842734cf1e8eb3374d10e4ee866e3

Commit B predecessor / current HEAD:
683aaee84d1fc09e9371dd214efc3ff58b7225ee

.aiassistant/records/aiscc/cycles/
20260831_1619_aiscc-p1-8-next-action-context-source-authority-final-acceptance-1.cycle.md

.aiassistant/reports/aiscc/
20260831_1619_aiscc-p1-8-next-action-context-accepted-prerequisite-design-resume-handoff-1.md
```

Require exact current provenance inputs:

```text
.aiassistant/tasks/done/
20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md
SHA-256:
8d5d0e74c88a311dab41869040028aa5a4ebb7df09c556b44dc457c367fc72de

.aiassistant/tasks/done/
20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md
SHA-256:
8fe75a5a948ac73909560163cedd4debab6ac9d7be6f07755b1916eaf175fcc4

.aiassistant/tasks/done/
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1.md
SHA-256:
4adee46da6c85e1a69cf672db755af69a38bae1dc3c342f490e06dab167fc3e7

.aiassistant/records/aiscc/cycles/
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md
SHA-256:
82e3ddf378ff820479cd18625e93a0b2968d79a3162dac48ffb639aecc6bec72
```

Require the ignored 1652 target evidence when still present:

```text
.aiassistant/reports/target/
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1/
```

If the ignored target is absent but all exact accepted rule bytes, three done Tasks, HOLD Cycle, and 22-payload
recomputation can be independently reproduced locally, classify the target as regenerated evidence rather than
inventing a missing artifact. If neither exact target evidence nor reproducible 22-payload evidence is available:

```text
STOP / TERMINAL_ACCEPTANCE_EVIDENCE_MISSING
```

Require blocked runtime identity unchanged:

```text
19 paths
aggregate SHA-256:
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

Pre-lifecycle tracked dirty inventory must be exactly:

```text
19 blocked runtime paths
+ accepted corrected source rule
+ accepted prerequisite rule
+ 1527 done Task
+ 1601 done Task
+ 1652 HOLD Cycle
+ 1652 done Task
= 25 exact paths
```

Current active Task and ignored target paths are excluded from Git dirty count.

If index, HEAD, candidate bytes, runtime aggregate, expected provenance identity, or dirty inventory differs, do not
reset/clean/restore/checkout/rebase/amend. Stop with the exact mismatch:

```text
TERMINAL_ACCEPTANCE_PREFLIGHT_MISMATCH
```

---

# 5. blocked runtime exact path boundary

The following 19 paths are not accepted by this Task and must remain outside both commits:

```text
migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py
migrations/versions/20260831_0007_p1_8_authority_contract_rework.py
src/aiscc/cycle/__init__.py
src/aiscc/cycle/models.py
src/aiscc/cycle/repository.py
src/aiscc/judgment/authority.py
src/aiscc/memory/__init__.py
src/aiscc/memory/models.py
src/aiscc/memory/repository.py
src/aiscc/next_action/__init__.py
src/aiscc/next_action/models.py
src/aiscc/next_action/repository.py
src/aiscc/persistence/models.py
tests/integration/evidence/test_postgres_evidence_admission.py
tests/integration/human/test_postgres_human_gate_judgment.py
tests/integration/memory/test_postgres_project_memory_next_action.py
tests/integration/workflow/test_postgres_kernel.py
tests/unit/cycle/test_project_memory_cycle_domain.py
tests/unit/next_action/test_next_action_domain.py
```

Do not modify them in this Task. Preserve their exact aggregate before and after both commits.

---

# 6. minimum authoritative context set

Read these exact local canonical paths:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md

.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/
20260831_1619_aiscc-p1-8-next-action-context-source-authority-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md

.aiassistant/reports/aiscc/
20260831_1619_aiscc-p1-8-next-action-context-accepted-prerequisite-design-resume-handoff-1.md

.aiassistant/tasks/done/
20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md

.aiassistant/tasks/done/
20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md

.aiassistant/tasks/done/
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1.md
```

The active Task, local canonical files, exact candidate bytes, accepted evidence, and Human decision are the current
authority set. Browser Project Source snapshots can be older read-only mirrors and must not overwrite later local
canonical state.

Do not bulk-read unrelated rules, reports, source, tests, or logs.

---

# 7. allowed scope

allowed_paths:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/records/aiscc/cycles/
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md

.aiassistant/reports/aiscc/
20260901_2155_aiscc-p1-8-prerequisite-authority-accepted-runtime-resume-handoff-1.md

.aiassistant/tasks/done/
20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md

.aiassistant/tasks/done/
20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md

.aiassistant/tasks/done/
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1.md

.aiassistant/tasks/active/
20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1.md

.aiassistant/tasks/done/
20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1.md

.aiassistant/reports/target/
20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1/
```

allowed_actions:

- exact local canonical and provenance reads
- exact hash and JCS recomputation
- narrow state/Cycle/handoff authoring
- current Task active→done lifecycle
- Git staging and two exact local commits described below
- UTF-8/Markdown/control/secret scan
- ignored target bundle generation

---

# 8. forbidden scope

forbidden_paths:

```text
the 19 runtime paths in section 5

.aiassistant/records/command-center/**
.aiassistant/project-sources/**
.aiassistant/reports/aiscc/** except the one new handoff path
.aiassistant/records/aiscc/cycles/** except the existing 1652 HOLD Cycle and one new final Cycle
.aiassistant/tasks/done/** except the four exact done Task paths in section 7
```

forbidden_actions:

- runtime/source/test/migration/config mutation
- changing either accepted rule byte before Commit A
- editing or rewriting historical Commit A/B
- amend/reset/restore/clean/rebase/merge/cherry-pick
- push/fetch/pull/remote/PR/deployment action
- Project Source mirror generation or upload
- DB/browser/network/credential/provider action
- unrelated full-suite or evidence expansion
- minting another Human decision
- accepting the 19-path runtime candidate
- marking P2/P3/public bounded Live completed
- deleting old HOLD/reject Cycle or done Task provenance
- hiding unexpected dirty files with `.gitignore`

---

# 9. Commit A — exact joint accepted design

Stage exactly these two paths and no others:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
```

Before Commit A require:

```text
git diff --cached --name-only
```

to equal the exact two-path set above.

Recompute and require exact SHA-256 values before and after staging:

```text
source:
7cf27b77bb961280becfc55ecf8e71c9406da9b7b91df0d2697132c2655108db

prerequisite:
8b19970629c55629df1560f2329b529992eceb86d5e4216baf0b7e78d3876960
```

Create Commit A.

Commit title:

```text
docs(governance): accept p1-8 prerequisite authority contracts
```

Commit body must state:

- Human joint acceptance binds the two exact rule bytes.
- JCS numeric sequence/high-watermark maximum is `9007199254740991`.
- all 22 direct/transitive cross-contract fingerprints reconcile.
- historical source Commit A/B and prior final Cycle remain immutable lineage.
- runtime implementation is not accepted by this commit.

Record:

```text
P1_8_PREREQUISITE_AUTHORITY_ACCEPTED_DESIGN_COMMIT=<actual Commit A SHA>
```

Require Commit A parent:

```text
683aaee84d1fc09e9371dd214efc3ff58b7225ee
```

Verify both committed blob bytes reproduce the exact accepted SHA-256 values. Do not amend.

---

# 10. final acceptance Cycle

Create exactly:

```text
.aiassistant/records/aiscc/cycles/
20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md
```

It must record:

```text
Command Center substantive review:
PERFORMED / ACCEPTED_CANDIDATE

Human:
HUMAN_PROVIDED / ACCEPTED

Human exact text:
Accept

binding:
JOINT_EXACT_BYTES

source SHA:
7cf27b77bb961280becfc55ecf8e71c9406da9b7b91df0d2697132c2655108db

prerequisite SHA:
8b19970629c55629df1560f2329b529992eceb86d5e4216baf0b7e78d3876960

accepted design Commit A:
exact actual SHA

22-payload JCS verification:
22 / 22 PASS / mismatch 0

unsafe normative JSON integer count:
0
```

Record the accepted correction semantics:

```text
sequence/high-watermark JSON integer maximum:
9007199254740991

canonicalization:
JCS_RFC8785

arbitrary-precision lexical hashing/custom JCS:
FORBIDDEN

NEXT_ACTION_CONTEXT owner:
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY /
NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY_V1

ProjectMemory role:
CURRENT_CONTEXTUAL_ELIGIBILITY_INPUT_NOT_PRIORITY_AUTHORITY

class-to-rank owner:
P1_8_NEXT_ACTION_SELECTION_POLICY_AUTHORITY_V1

TaskConstraint scopes:
PROJECT / TASK_CONTRACT / WORK_RUN

owner history:
immutable ISSUED / SUPERSEDED / REVOKED events + certified prefix snapshot

P1-4 blocker:
closed taxonomy, SECURITY_BOUNDARY non-resumable,
single durable P1_4BlockerResolvedAttestationV1 authority

concrete CYCLE_DERIVED descriptor/ActionRef count:
0
```

Preserve and reference:

- historical 1619 final acceptance Cycle
- 1652 HOLD Cycle
- 1527/1601/1652 done Tasks
- accepted review evidence identities from section 3
- 19-path runtime aggregate

Do not claim runtime acceptance.

---

# 11. canonical state update

Update only the state transitions made true by this Human acceptance and its persistence:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Preserve all unrelated later canonical entries from the actual repository files.

Target semantic state:

```text
P1-8 Project Memory/Cycle Admission Design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 NEXT_ACTION_CONTEXT Source Authority corrected revision:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 prerequisite owner-authority exact-contract/source-enrollment design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

historical source design commit/cycle:
PRESERVED_LINEAGE

P1-8 Runtime:
NOT_ACCEPTED

P1-8 runtime prerequisite design blocker:
CLEARED_BY_HUMAN_ACCEPTED_JOINT_DESIGN

existing runtime candidate:
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42

runtime continuation:
SEPARATE_REWORK_RESUME_AUTHORIZED

P2/P3:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

`NEXT_ACTIONS.md` stable next action:

```text
P1-8 runtime prerequisite-authority and JCS-safe-integer reconciliation resume
```

Required next-action boundary:

- start from the exact preserved 19-path candidate
- read the two newly accepted rule bytes and Commit A
- reconcile runtime schemas, persistence, owner events, guards, and tests to the accepted contracts
- preserve proof ownership and system-owned transition semantics
- generate a new runtime candidate and evidence
- require Command Center review and Human runtime final review before runtime acceptance
- do not begin P2/P3 or public release

---

# 12. durable handoff

Create exactly:

```text
.aiassistant/reports/aiscc/
20260901_2155_aiscc-p1-8-prerequisite-authority-accepted-runtime-resume-handoff-1.md
```

The handoff must be sufficient for a fresh fifth Browser Command Center/IDE Executor session with no access to chat
memory, Library files, or temporary target bundles.

Include:

1. Human accepted exact two-file identity and exact text.
2. Command Center 22/22 JCS substantive review result.
3. historical source Commit A/B and 1619 final Cycle lineage.
4. new joint accepted design Commit A.
5. final acceptance Cycle and terminal governance Commit B placeholders/actual values.
6. accepted semantics listed in section 10.
7. exact 19-path runtime candidate identity and why it remains unaccepted.
8. exact runtime resume scope and mandatory Human runtime gate.
9. P2/P3/Public Live boundary.
10. exact preserved paths and first-session preflight instructions.

Do not copy the 2nd/3rd/4th Browser Command Center workflow-question answer documents into repository canonical
state in this Task. They are separate workflow-rule analysis inputs, not terminal design provenance.

---

# 13. current Task lifecycle

After all executor-required files and target report are complete, move:

```text
.aiassistant/tasks/active/
20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1.md
```

to:

```text
.aiassistant/tasks/done/
20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1.md
```

Do this before staging Commit B.

---

# 14. Commit B exact governance allowlist

Stage exactly these ten paths:

```text
.aiassistant/records/aiscc/cycles/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md
.aiassistant/tasks/done/20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md
.aiassistant/tasks/done/20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md
.aiassistant/tasks/done/20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1.md
.aiassistant/records/aiscc/cycles/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/reports/aiscc/20260901_2155_aiscc-p1-8-prerequisite-authority-accepted-runtime-resume-handoff-1.md
.aiassistant/tasks/done/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1.md
```

Expected staged path-entry count:

```text
10
```

Before Commit B, require `git diff --cached --name-only` to equal the exact ordinal-sorted set above.

Forbidden from Commit B:

- the two accepted design rules; they belong only to Commit A
- all 19 runtime paths
- ignored target evidence
- workflow questionnaire/answer documents
- any prior committed Cycle/handoff rewrite
- any Project Source mirror path

If staged count or identity differs:

```text
STOP / TERMINAL_GOVERNANCE_STAGED_SET_MISMATCH
```

Do not auto-expand the allowlist.

---

# 15. Commit B — terminal governance

Create one governance commit.

Commit title:

```text
chore(governance): close p1-8 prerequisite authority design
```

Commit body must state:

- records the fourth Command Center session Human joint acceptance
- closes the safe-integer corrected source and prerequisite authority design
- preserves 1527/1601/1652 review lineage and 1652 HOLD
- retains the 19-path runtime as an unaccepted candidate
- authorizes only a separate runtime rework/resume Task

Record:

```text
P1_8_PREREQUISITE_AUTHORITY_TERMINAL_GOVERNANCE_COMMIT=<actual Commit B SHA>
```

Commit B parent must equal actual Commit A. Do not amend.

Final lineage:

```text
683aaee84d1fc09e9371dd214efc3ff58b7225ee
→ <Commit A exact joint accepted design>
→ <Commit B terminal governance>
```

No intervening commit is allowed.

---

# 16. final workspace semantics

Do not require a globally clean worktree because the exact 19-path runtime candidate remains deliberately dirty.

After Commit B require:

```text
index:
clean

accepted joint rule paths:
clean / committed in Commit A

terminal governance paths:
clean / committed in Commit B

residual tracked dirty inventory:
exactly the 19 runtime paths in section 5

residual runtime aggregate:
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42

unexpected dirty paths:
0

Git push:
NOT_RUN
```

If residual path count, path identity, or aggregate differs:

```text
STOP / DIRTY_WORKSPACE_MIXED_OR_RUNTIME_CANDIDATE_DRIFT
```

Do not clean or reset the runtime candidate.

---

# 17. evidence contract

executor_required:

- channel: `STATIC_SOURCE`
  scope: exact preflight identities, two accepted rule SHA values, 22 canonical payload fingerprints
  allowed_command_or_environment: local read/hash/Node plus independent installed language verifier
  pass_condition: exact identities and 22/22 mismatch count 0

- channel: `PUBLIC_PROVENANCE`
  scope: Commit A, final Cycle, three canonical state files, handoff, Task lifecycle, Commit B
  allowed_command_or_environment: local repository/Git only
  pass_condition: exact two-commit lineage and exact allowlists

- channel: `STATIC_SOURCE`
  scope: UTF-8/no-BOM/control/secret/Markdown validation for all changed governance paths
  allowed_command_or_environment: local static tools
  pass_condition: violations 0

reuse_allowed:

- channel: `STATIC_SOURCE`
  predecessor: accepted 1652 Executor evidence and Command Center independent recomputation
  provenance_condition: exact candidate/evidence SHA values match sections 2 and 3
  applicability_condition: no candidate byte drift

human_owned:

- channel: `HUMAN_VERIFICATION`
  scope: exact joint design acceptance
  expected_result_format: `HUMAN_PROVIDED / ACCEPTED`; exact text `Accept`
  status: already provided; do not ask again

not_required:

- channel: `BUILD / UNIT_TEST / INTEGRATION_TEST / DATABASE_RUNTIME / HTTP_RUNTIME / BROWSER_RUNTIME`
  reason: design terminal persistence only; runtime candidate is unchanged and unaccepted

- channel: `PROJECT_SOURCE_MIRROR_SYNC`
  reason: not part of this exact terminal persistence Task

forbidden:

- action_or_channel: runtime mutation or runtime acceptance
  reason: separate future rework and Human runtime final review required

- action_or_channel: remote Git/network/deployment
  reason: local terminal provenance only

proof_non_substitution:

```text
Executor PASS != Human acceptance
Human acceptance != bytes other than the two exact SHA values
design acceptance != runtime acceptance
Commit A != terminal governance Commit B
temporary target exists != durable provenance complete
historical source acceptance != current corrected source acceptance
```

---

# 18. mandatory stop conditions

Stop before further mutation on:

- expected HEAD mismatch
- non-empty initial index
- either accepted rule SHA mismatch
- runtime path/aggregate drift
- missing or mismatched required provenance input
- 22-payload fingerprint mismatch
- unexpected dirty path
- Commit A staged-set mismatch
- final Cycle unable to bind actual Commit A
- current Task lifecycle not completed before Commit B
- Commit B staged-set mismatch
- secret/private material detection
- policy/authority conflict
- evidence scope expansion requirement

After a named blocker, perform only minimal read-only evidence, workspace inventory, report/export, and safe stop.

---

# 19. export bundle

Target:

```text
.aiassistant/reports/target/
20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
GIT_PROVENANCE.md
JCS_ACCEPTANCE_EVIDENCE.md
```

Include project-relative copies of:

- both Commit A accepted rule blobs
- 1652 HOLD Cycle
- 1527/1601/1652 done Tasks
- new final acceptance Cycle
- three canonical state files
- durable handoff
- current done Task

`JCS_ACCEPTANCE_EVIDENCE.md` must record the 22 payload IDs, accepted document hash, independently recomputed hash,
byte length, safe-integer result, and mismatch count. It may reference the full canonical payloads in the two accepted
rule blobs rather than duplicating every payload.

`GIT_PROVENANCE.md` must record both commits, parents, exact changed paths, committed blob hashes, and final residual
runtime inventory.

Do not include secrets, private raw chat history, workflow questionnaire answers, or all runtime file bytes.

---

# 20. Executor report requirements

Report exact:

1. task/work type/task path
2. start branch and HEAD
3. initial index and exact 25-path dirty classification
4. Human exact text and joint binding
5. both accepted rule SHA verifications
6. accepted 1652 evidence identity and 22/22 independent recomputation
7. blocked runtime 19-path aggregate before mutation
8. Commit A exact staged paths
9. Commit A SHA and parent
10. both Commit A committed blob SHA values
11. final acceptance Cycle path and SHA
12. canonical state semantic delta
13. durable handoff path and SHA
14. current Task active→done lifecycle
15. Commit B exact staged paths and count 10
16. Commit B SHA and parent
17. final index
18. final residual 19-path runtime inventory and aggregate
19. unexpected dirty paths = 0
20. runtime status = NOT_ACCEPTED / REWORK_RESUME_AUTHORIZED
21. P2/P3 = NOT_STARTED
22. Public bounded Live = NOT_RELEASED
23. Project Source mirror sync = NOT_RUN / NOT_REQUIRED_THIS_TASK
24. Git push = NOT_RUN
25. UTF-8/BOM/control/secret/fence validation
26. unverified items
27. rollback/revert guide without executing it
28. preserved exact paths

---

# 21. preserved exact paths

The following must survive cleanup and be committed:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md

.aiassistant/records/aiscc/cycles/
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md

.aiassistant/tasks/done/
20260901_1527_aiscc-p1-8-next-action-context-terminal-canonical-git-reconciliation-audit-1.md

.aiassistant/tasks/done/
20260901_1601_aiscc-p1-8-prerequisite-owner-authority-exact-contract-and-source-enrollment-design-rework-1.md

.aiassistant/tasks/done/
20260901_1652_aiscc-p1-8-jcs-safe-integer-cross-contract-fingerprint-reconciliation-design-rework-1.md

.aiassistant/tasks/done/
20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-terminal-acceptance-persistence-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/reports/aiscc/
20260901_2155_aiscc-p1-8-prerequisite-authority-accepted-runtime-resume-handoff-1.md
```

The target bundle is temporary and deletable after substantive Command Center review.

---

# 22. expected terminal result

```text
P1-8 NEXT_ACTION_CONTEXT Source Authority corrected revision:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 prerequisite owner-authority design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 Runtime:
NOT_ACCEPTED / REWORK_RESUME_AUTHORIZED

residual runtime candidate:
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42

P2/P3:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

No runtime implementation mutation or runtime acceptance is authorized by this Task.
