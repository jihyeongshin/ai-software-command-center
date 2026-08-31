# 작업지시서: P1-8 NEXT_ACTION_CONTEXT Source Authority Terminal Acceptance Persistence

## meta

- task_id: `20260831_1619_aiscc-p1-8-next-action-context-source-authority-terminal-acceptance-persistence-1`
- created_at: `2026-08-31T16:19:00+09:00`
- phase: `P1-8 NEXT_ACTION_CONTEXT Source Authority Design`
- work_type: `HUMAN_ACCEPTANCE_TERMINAL_PERSISTENCE`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_start_head: `f4614198c2745944f7ec02639a45b0315bbc903d`
- accepted_design_path: `.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md`
- accepted_design_sha256: `19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1`
- accepted_p1_8_design_sha256: `100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a`
- blocked_runtime_path_count: `19`
- blocked_runtime_aggregate_sha256: `84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42`
- prerequisite_candidate_path: `.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md`
- prerequisite_candidate_sha256: `556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c`
- human_final_review: `HUMAN_PROVIDED / ACCEPTED`
- human_acceptance_text: `Human P1-8 NEXT_ACTION_CONTEXT source authority design final review / 판정: ACCEPTED`
- p1_8_runtime_status: `BLOCKED_REQUIRED_EVIDENCE`
- p2_status: `NOT_STARTED`
- public_bounded_live: `NOT_RELEASED`

---

# 1. purpose

Persist the Human-accepted `NEXT_ACTION_CONTEXT` source-authority design without mutating the blocked P1-8 runtime
candidate or the still-unaccepted prerequisite owner-authority candidate.

This Task closes only:

```text
P1-8 NEXT_ACTION_CONTEXT Source Authority Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED
```

It does NOT close:

```text
P1-8 prerequisite owner-authority design
P1-8 Runtime
```

---

# 2. mandatory preflight

Require:

```text
HEAD ==
f4614198c2745944f7ec02639a45b0315bbc903d
```

Require:

```text
sha256(.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md)
==
19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1
```

Require accepted parent P1-8 design:

```text
sha256(.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md)
==
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a
```

Require blocked runtime candidate unchanged:

```text
19 source/test/migration paths

aggregate:
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

Require prerequisite candidate unchanged:

```text
sha256(.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md)
==
556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c
```

Index must be empty.

If any reviewed candidate drifts:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

Do not reset/clean/checkout-overwrite/rebase/amend.

---

# 3. Human authority input

Persist exactly:

```text
Human P1-8 NEXT_ACTION_CONTEXT source authority design final review
판정: ACCEPTED
```

This Human decision applies only to the exact design SHA:

```text
19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1
```

Do not generalize acceptance to another file revision.

---

# 4. Commit A — exact accepted design only

Stage exactly:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
```

No other path.

Before commit require:

```text
git diff --cached --name-only
```

equals exactly that one path.

Create Commit A.

Commit title:

```text
docs(governance): accept next action context source authority
```

Commit body must state that it freezes the Human-accepted external Command Center source authority, P1-6 carrier
boundary, P1-8 contextual-only Memory role, accepted ranking compatibility, and authoring-snapshot/currentness
separation.

Record:

```text
P1_8_NEXT_ACTION_CONTEXT_ACCEPTED_DESIGN_COMMIT=<Commit A SHA>
```

Do not amend.

After Commit A, verify the committed blob SHA is exactly:

```text
19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1
```

---

# 5. preserve blocked/unaccepted candidate sets after Commit A

After Commit A, the following remain deliberately uncommitted and must not be staged into Commit B.

## blocked P1-8 runtime

```text
19 source/test/migration paths
aggregate:
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

## prerequisite owner-authority candidate

```text
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md

SHA:
556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c
```

Neither is accepted by this Task.

No runtime source/test/migration path may enter Commit B.

No prerequisite candidate design file may enter Commit B.

---

# 6. terminal acceptance Cycle

Create:

```text
.aiassistant/records/aiscc/cycles/
20260831_1619_aiscc-p1-8-next-action-context-source-authority-final-acceptance-1.cycle.md
```

It must bind:

```text
Human:
HUMAN_PROVIDED / ACCEPTED

accepted design file:
AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md

accepted file SHA:
19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1

accepted design Commit A:
exact actual SHA

accepted parent P1-8 design SHA:
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a
```

Record final accepted semantics:

```text
semantic owner:
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY /
NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY_V1

P1-6:
bytes / schema / admission / terminal-consumed provenance only

P1-8 ProjectMemory:
contextual eligibility input only
!= priority authority

priority source:
exact externally enrolled NextActionContextRefV1

class→rank owner:
P1_8_NEXT_ACTION_SELECTION_POLICY_AUTHORITY_V1

ranking tuple:
(
  authoritative_priority_rank,
  policy_dependency_ordinal,
  enrolled_critical_path_ordinal,
  descriptor_policy_ordinal,
  ActionRef lexical,
  proposal_id lexical
)

carrier owner-event H:
AUTHORING_SNAPSHOT_PROVENANCE_ONLY

terminal external-context currentness:
NOT_REQUIRED_V1

historical provenance:
!= current applicability

P1-6 Requirement fingerprint-schema extension:
NOT_REQUIRED
```

Record:

```text
P1-8 prerequisite owner-authority design
→ still CANDIDATE / BLOCKED_REQUIRED_EVIDENCE

P1-8 Runtime
→ BLOCKED_REQUIRED_EVIDENCE

P2
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

---

# 7. governance lineage to persist in Commit B

Persist the P1-8 runtime/prerequisite/source-authority review provenance accumulated since the last terminal
governance commit.

Expected durable paths:

```text
.aiassistant/records/aiscc/cycles/
20260831_1143_aiscc-p1-8-runtime-memory-next-action-authority-and-terminal-epoch-hold-1.cycle.md

.aiassistant/tasks/done/
20260831_1143_aiscc-p1-8-memory-next-action-authority-and-terminal-epoch-runtime-rework-1.md

.aiassistant/records/aiscc/cycles/
20260831_1332_aiscc-p1-8-runtime-historical-replay-and-system-owner-capability-hold-1.cycle.md

.aiassistant/tasks/done/
20260831_1332_aiscc-p1-8-historical-replay-and-system-owner-capability-runtime-rework-1.md

.aiassistant/records/aiscc/cycles/
20260831_1332_aiscc-p1-8-prerequisite-owner-authority-baseline-gap-hold-1.cycle.md

.aiassistant/tasks/done/
20260831_1332_aiscc-p1-8-prerequisite-owner-authority-contract-design-freeze-1.md

.aiassistant/records/aiscc/cycles/
20260831_1332_aiscc-p1-8-prerequisite-owner-authority-exact-contract-gap-hold-1.cycle.md

.aiassistant/tasks/done/
20260831_1332_aiscc-p1-8-prerequisite-owner-authority-exact-contract-design-rework-1.md

.aiassistant/records/aiscc/cycles/
20260831_1514_aiscc-p1-8-next-action-context-source-authority-baseline-gap-hold-1.cycle.md

.aiassistant/tasks/done/
20260831_1514_aiscc-p1-8-next-action-context-source-authority-design-freeze-1.md

.aiassistant/records/aiscc/cycles/
20260831_1514_aiscc-p1-8-next-action-context-ranking-authority-compatibility-hold-1.cycle.md

.aiassistant/tasks/done/
20260831_1514_aiscc-p1-8-next-action-context-ranking-authority-compatibility-design-rework-1.md

.aiassistant/records/aiscc/cycles/
20260831_1619_aiscc-p1-8-next-action-context-source-authority-human-final-review-recommendation-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260831_1619_aiscc-p1-8-next-action-context-source-authority-final-acceptance-1.cycle.md
```

If any of the historical expected paths are missing, do not fabricate their content.

Report missing exact path and STOP:

```text
TERMINAL_GOVERNANCE_PROVENANCE_MISSING
```

---

# 8. canonical state update

Update:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

Target state:

```text
P1-8 Design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 NEXT_ACTION_CONTEXT Source Authority Design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 prerequisite owner-authority design:
BLOCKED_REQUIRED_EVIDENCE
→ prerequisite exact-contract incorporation still required

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE

blocked runtime identity:
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

`NEXT_ACTIONS.md` exact next action:

```text
P1-8 prerequisite owner-authority exact-contract design resume

scope:
- TaskConstraint exact event/scope contract
- P1-4 blocker taxonomy/resumability/guard binding
- incorporate accepted NEXT_ACTION_CONTEXT source enrollment into
  P1_8_POLICY_ACTION_CATALOG_V1 / descriptor / selection-policy authority
- recompute affected catalog/descriptor/policy fingerprints
```

Do not mark P1-8 Runtime resume authorized yet.

---

# 9. durable handoff

Create:

```text
.aiassistant/reports/aiscc/
20260831_1619_aiscc-p1-8-next-action-context-accepted-prerequisite-design-resume-handoff-1.md
```

The handoff must be sufficient for a fresh Command Center/Executor session.

Bind:

```text
accepted source-authority design Commit A
accepted source-authority file SHA
accepted parent P1-8 design SHA

blocked runtime:
19 / 84641ac35f...

prerequisite candidate:
556faad8a77...

Human acceptance text

exact accepted NEXT_ACTION_CONTEXT owner/ranking/currentness semantics
```

Also include the unresolved prerequisite design work:

```text
TaskConstraint scope/event/currentness authority

P1-4 blocker taxonomy/resumability/G_BLOCKER_RESOLVED durable binding

catalog/descriptor explicit source enrollment of accepted NextActionContextRefV1

affected fingerprint recomputation
```

Do not state or imply runtime resume authorization.

---

# 10. current Task lifecycle

Move:

```text
.aiassistant/tasks/active/
20260831_1619_aiscc-p1-8-next-action-context-source-authority-terminal-acceptance-persistence-1.md
```

to:

```text
.aiassistant/tasks/done/
20260831_1619_aiscc-p1-8-next-action-context-source-authority-terminal-acceptance-persistence-1.md
```

before Commit B.

---

# 11. Commit B allowlist

Commit B must contain only terminal-governance paths.

Required paths are:

```text
14 historical/review/final acceptance Cycle+Task paths listed in section 7

3 canonical state files

1 durable handoff report

1 current terminal-persistence Task done
```

Expected path-entry count:

```text
19
```

Breakdown:

```text
14 provenance paths
3 canonical state paths
1 handoff
1 current done Task
--------------------
19
```

No accepted design path in Commit B; it belongs to Commit A.

No blocked runtime source/test/migration path.

No `.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md`.

No target export.

Before Commit B:

```text
git diff --cached --name-only
```

must equal the exact expected governance set.

If count/path differs:

```text
STOP
→ TERMINAL_GOVERNANCE_STAGED_SET_MISMATCH
```

If Git reports a legitimate tracked active→done rename for one of these Task files that was already tracked before
this Task, count both old/new path entries and STOP rather than guessing:

```text
TERMINAL_GOVERNANCE_LIFECYCLE_ALLOWLIST_REVIEW_REQUIRED
```

Report the exact old/new paths and blob equality.

Do not auto-expand the allowlist.

---

# 12. Commit B

Create one governance commit.

Commit title:

```text
chore(governance): accept next action context source authority
```

Commit body must state that it records Human final acceptance, preserves the P1-8 runtime/prerequisite review
lineage, and keeps runtime blocked pending prerequisite owner-authority exact-contract completion.

Record:

```text
P1_8_NEXT_ACTION_CONTEXT_TERMINAL_GOVERNANCE_COMMIT=<Commit B SHA>
```

Do not amend.

---

# 13. final lineage

Require:

```text
f4614198c2745944f7ec02639a45b0315bbc903d
→ <Commit A accepted source-authority design>
→ <Commit B terminal governance>
```

No commit between the base and Commit A.

---

# 14. final workspace semantics

Do NOT require a globally clean tracked worktree, because two reviewed/unaccepted candidate sets intentionally
remain uncommitted.

After Commit B require:

```text
index:
clean

accepted source-authority design:
clean/committed

terminal governance paths:
clean/committed

blocked P1-8 runtime:
still exact 19-path reviewed candidate
aggregate 84641ac35f...

prerequisite owner-authority candidate:
still uncommitted
SHA 556faad8...
```

Any additional unrelated tracked dirty path:

```text
STOP
→ DIRTY_WORKSPACE_MIXED
```

No Git push.

---

# 15. export

Target:

```text
.aiassistant/reports/target/
20260831_1619_aiscc-p1-8-next-action-context-source-authority-terminal-acceptance-persistence-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
GIT_PROVENANCE.md
```

Include copies of:

```text
final acceptance Cycle
canonical state files
durable handoff
done Task
Commit A accepted design blob/hash inventory
Commit B path inventory
residual blocked-runtime 19-path hash inventory
prerequisite candidate SHA verification
```

No need to copy all blocked runtime bytes if exact prior aggregate/per-file inventory remains available and
unchanged.

---

# 16. Executor report

Report exact:

1. start HEAD
2. Human acceptance text
3. accepted design SHA verification
4. blocked runtime identity verification
5. prerequisite candidate SHA verification
6. initial index/worktree classification
7. Commit A SHA
8. Commit A parent
9. Commit A exact changed path
10. Commit A blob SHA
11. final acceptance Cycle path
12. canonical state update
13. durable handoff path
14. historical provenance path presence
15. Commit B exact staged path set
16. Commit B path count
17. Commit B SHA
18. Commit B parent
19. final index
20. residual blocked runtime identity
21. residual prerequisite candidate identity
22. unexpected dirty paths = none
23. P1-8 Runtime status
24. P2 status
25. Public Live status
26. Git push = NOT_RUN

---

# 17. expected terminal state

```text
P1-8 NEXT_ACTION_CONTEXT Source Authority Design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 prerequisite owner-authority design:
BLOCKED_REQUIRED_EVIDENCE

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

No runtime implementation resume is authorized by this Task.
