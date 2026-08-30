# 작업지시서: P1-7 Terminal Handoff Future-Owner Guard List Provenance Correction

## meta

- task_id: `20260830_1844_aiscc-p1-7-terminal-handoff-future-owner-guard-list-provenance-correction-1`
- created_at: `2026-08-30T18:44:00+09:00`
- phase: `P1-7 Terminal Governance Correction`
- work_type: `COMMAND_CENTER_RECORD_UPDATE`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `AISCC_COMMAND_CENTER`
- expected_start_head: `abd5228f5d1338aa820298cc76eaf7db82b0ce4f`
- accepted_runtime_commit: `b4ba49ebaeb437d885bf22d52473c7d8a79832d1`
- accepted_runtime_aggregate_sha256: `1933e0451d101b142e099cc987babb426f87422d15338775d9d87bbf29fa2f90`
- p1_7_runtime_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- p1_8_status: `NOT_STARTED`
- public_bounded_live: `NOT_RELEASED`

---

# 1. purpose

This is a narrow additive terminal-governance correction.

Do NOT reopen P1-7 runtime.

Do NOT modify Commit A or Commit B.

The defect is limited to the P1-8 durable handoff's exact guard enumeration.

Current handoff omitted:

```text
G_SUSPENDED_HUMAN_GATE
G_RESUMABLE_HUMAN_GATE
```

from the `P1_7_HUMAN` guard list.

---

# 2. mandatory preflight

Require:

```text
HEAD ==
abd5228f5d1338aa820298cc76eaf7db82b0ce4f
```

Verify first-parent lineage:

```text
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
→ b4ba49ebaeb437d885bf22d52473c7d8a79832d1
→ abd5228f5d1338aa820298cc76eaf7db82b0ce4f
```

Verify Commit A remains:

```text
21 paths
aggregate:
1933e0451d101b142e099cc987babb426f87422d15338775d9d87bbf29fa2f90
```

Verify Commit B remains the terminal governance commit and is not amended.

Any mismatch:

```text
STOP
→ TERMINAL_PROVENANCE_DRIFT
```

No reset/rebase/clean/amend.

---

# 3. exact correction

Modify only:

```text
.aiassistant/reports/aiscc/
20260830_1712_aiscc-p1-7-runtime-accepted-p1-8-command-center-handoff-1.md
```

In section:

```text
exact P1-4 future-owner guards implemented by P1-7
```

replace the incomplete `P1_7_HUMAN` enumeration with the exact accepted set:

```text
P1_7_HUMAN:
G_HUMAN_REQUIRED
G_HUMAN_NOT_REQUIRED
G_NO_PENDING_HUMAN_GATE
G_SUSPENDED_HUMAN_GATE
G_RESUMABLE_HUMAN_GATE
G_HUMAN_APPROVED
G_HUMAN_REWORK
G_HUMAN_REJECTED
```

Preserve exact `P1_7_JUDGMENT`:

```text
P1_7_JUDGMENT:
G_JUDGMENT_ACCEPTED
G_JUDGMENT_REJECTED
G_JUDGMENT_REWORK
```

Add one concise clarification immediately after the list:

```text
G_SUSPENDED_HUMAN_GATE and G_RESUMABLE_HUMAN_GATE preserve the accepted
HumanGate suspension/resumption authority used by the P1-4 blocked/resume lifecycle;
P1-8 must not reinterpret, replace, or absorb these guards.
```

Do not otherwise rewrite the handoff.

---

# 4. preserve accepted semantics

No change to:

```text
HumanGate
HumanResult
Judgment
WorkflowState
TransitionDecision
P1-4 matrix
P1-6 evidence authority
P1-7 runtime source
accepted runtime aggregate
Human acceptance
P1-8 ownership
```

Exact accepted Human guard owner set:

```text
G_HUMAN_REQUIRED
G_HUMAN_NOT_REQUIRED
G_NO_PENDING_HUMAN_GATE
G_SUSPENDED_HUMAN_GATE
G_RESUMABLE_HUMAN_GATE
G_HUMAN_APPROVED
G_HUMAN_REWORK
G_HUMAN_REJECTED
```

Exact accepted Judgment guard owner set:

```text
G_JUDGMENT_ACCEPTED
G_JUDGMENT_REJECTED
G_JUDGMENT_REWORK
```

---

# 5. add correction Cycle

Place the Command Center-issued Cycle:

```text
.aiassistant/records/aiscc/cycles/
20260830_1844_aiscc-p1-7-terminal-handoff-future-owner-guard-list-correction-hold-1.cycle.md
```

Preserve it verbatim except repository-local line-ending normalization if required by canonical policy.

It records:

```text
runtime ACCEPTED/CLOSED remains unchanged
Commit A/B preserved
handoff exact guard-list defect
P1-8 remains NOT_STARTED until correction
```

---

# 6. Task lifecycle

Start:

```text
.aiassistant/tasks/active/
20260830_1844_aiscc-p1-7-terminal-handoff-future-owner-guard-list-provenance-correction-1.md
```

Finish:

```text
.aiassistant/tasks/done/
20260830_1844_aiscc-p1-7-terminal-handoff-future-owner-guard-list-provenance-correction-1.md
```

---

# 7. exact additive commit allowlist

Stage exactly 3 paths:

```text
.aiassistant/reports/aiscc/
20260830_1712_aiscc-p1-7-runtime-accepted-p1-8-command-center-handoff-1.md

.aiassistant/records/aiscc/cycles/
20260830_1844_aiscc-p1-7-terminal-handoff-future-owner-guard-list-correction-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_1844_aiscc-p1-7-terminal-handoff-future-owner-guard-list-provenance-correction-1.md
```

No other path.

Especially forbidden:

```text
src/**
tests/**
migrations/**
.aiassistant/rules/**
CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md
prior Cycles
prior Tasks
```

The canonical state itself is already correct and must remain unchanged.

---

# 8. Git policy

Use explicit path staging.

Forbidden:

```text
git add .
git add -A
git reset
git clean
git commit --amend
git rebase
git push
```

Recommended commit message:

```text
docs(governance): correct P1-7 handoff guard inventory

Restore the omitted suspended and resumable HumanGate guard authorities in the
P1-7-to-P1-8 durable handoff while preserving the accepted runtime, terminal
commits, canonical state, and all prior provenance unchanged.
```

Create one additive Commit C.

Do not amend:

```text
b4ba49ebaeb437d885bf22d52473c7d8a79832d1
abd5228f5d1338aa820298cc76eaf7db82b0ce4f
```

---

# 9. verification

Before Commit C:

```text
git diff --cached --name-only
```

must equal exactly the 3-path allowlist.

Verify corrected handoff contains all exact 11 owner guards:

```text
P1_7_HUMAN:
8

P1_7_JUDGMENT:
3
```

Specifically require:

```text
G_SUSPENDED_HUMAN_GATE
G_RESUMABLE_HUMAN_GATE
```

No duplicate guard IDs.

Verify:

```text
P1-7 Runtime remains ACCEPTED / CLOSED

P1-8 remains NOT_STARTED / NEXT_ACTION

PUBLIC_BOUNDED_LIVE remains NOT_RELEASED
```

UTF-8/control-character check:

```text
PASS
```

No new runtime tests are required.

---

# 10. final lineage

After Commit C require:

```text
c87cfc75f14476e10b4a02a2ab0bd295720a85a0
→ b4ba49ebaeb437d885bf22d52473c7d8a79832d1
→ abd5228f5d1338aa820298cc76eaf7db82b0ce4f
→ <Commit C>
```

Verify Commit C:

```text
changed paths:
exactly 3

runtime source/test/migration:
0
```

Final tracked worktree/index:

```text
clean
```

No push.

---

# 11. target bundle

Create:

```text
.aiassistant/reports/target/
20260830_1844_aiscc-p1-7-terminal-handoff-future-owner-guard-list-provenance-correction-1/
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
corrected handoff
1844 correction Cycle
1844 correction Task
```

Report exact Commit C SHA and final lineage.

---

# 12. final state

Successful correction:

```text
P1-7 Design:
ACCEPTED / CLOSED

P1-7 Runtime:
HUMAN_PROVIDED / ACCEPTED / CLOSED

terminal provenance:
CORRECTED / COMPLETE

P1-8:
NOT_STARTED / NEXT_ACTION

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

No additional Human P1-7 acceptance is required.

Next action after Command Center verifies Commit C:

```text
P1-8 Project Memory and Cycle Admission design Task
```

---

# 13. preserved exact paths

Preserve:

```text
.aiassistant/reports/aiscc/
20260830_1712_aiscc-p1-7-runtime-accepted-p1-8-command-center-handoff-1.md

.aiassistant/records/aiscc/cycles/
20260830_1712_aiscc-p1-7-human-gate-and-judgment-runtime-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260830_1844_aiscc-p1-7-terminal-handoff-future-owner-guard-list-correction-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_1712_aiscc-p1-7-runtime-terminal-acceptance-and-p1-8-handoff-1.md

.aiassistant/tasks/done/
20260830_1844_aiscc-p1-7-terminal-handoff-future-owner-guard-list-provenance-correction-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```
