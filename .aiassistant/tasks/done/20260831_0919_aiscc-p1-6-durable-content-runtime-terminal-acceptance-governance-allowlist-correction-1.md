# 작업지시서: P1-6 Durable Content Runtime Terminal Acceptance Governance Allowlist Correction

## meta

- task_id: `20260831_0919_aiscc-p1-6-durable-content-runtime-terminal-acceptance-governance-allowlist-correction-1`
- revision: `2`
- revision_reason: `2357 tracked active-path deletion omitted from Commit B allowlist`
- phase: `P1-6 Durable Evidence Content Runtime Terminal Persistence`
- work_type: `COMMAND_CENTER_RECORD_UPDATE_REWORK`
- expected_start_head: `8320a3c567a58bab5f728a88d5c88862392d187c`
- accepted_runtime_commit: `8320a3c567a58bab5f728a88d5c88862392d187c`
- accepted_runtime_commit_parent: `bc446d9530e28f9b10602c9f1dd5232a97221a10`
- accepted_runtime_path_count: `13`
- accepted_runtime_aggregate_sha256: `2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721`
- commit_a_status: `CREATED_AND_VERIFIED`
- commit_b_status: `NOT_CREATED`
- supersedes_instruction_revision: `revision 1 of this same Task`
- human_runtime_final_review: `HUMAN_PROVIDED / ACCEPTED`

---

# 1. purpose

Resume terminal governance persistence **after Commit A already exists**.

Do NOT recreate Commit A.

Do NOT amend/revert Commit A.

The previous revision correctly added the P1-8 2130 active→done lifecycle, but still omitted the tracked
active-path deletion for the P1-6 2357 Task.

The authoritative current lifecycle state includes:

```text
D  .aiassistant/tasks/active/
   20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md

?? .aiassistant/tasks/done/
   20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md
```

The active and done blobs are identical.

This is legitimate Task lifecycle provenance:

```text
active
→ executor turn completed
→ done
```

and must be persisted in Commit B.

---

# 2. no new correction provenance path

This is **revision 2 of the already-issued 0919 correction Task**, not a new Task ID.

Do not create an additional correction Task or additional correction Cycle merely for this allowlist correction.

Continue to preserve the already-issued Cycle:

```text
.aiassistant/records/aiscc/cycles/
20260831_0919_aiscc-p1-6-runtime-terminal-governance-p1-8-task-lifecycle-omission-correction-1.cycle.md
```

This avoids recursively changing Commit B's path count.

---

# 3. mandatory preflight

Require current HEAD:

```text
8320a3c567a58bab5f728a88d5c88862392d187c
```

Require Commit A:

```text
SHA:
8320a3c567a58bab5f728a88d5c88862392d187c

parent:
bc446d9530e28f9b10602c9f1dd5232a97221a10

changed paths:
exact 13 accepted runtime paths

runtime aggregate:
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721

.aiassistant/**:
0
```

If Commit A differs:

```text
STOP
→ TERMINAL_RUNTIME_COMMIT_MISMATCH
```

Require:

```text
Commit B:
NOT_CREATED

index:
empty
```

Do not run new runtime tests.

Do not modify source/test/migration.

---

# 4. verify both historical tracked Task lifecycle moves

## 4.1 P1-8 2130 lifecycle

Require:

```text
.aiassistant/tasks/active/
20260830_2130_aiscc-p1-8-design-terminal-persistence-and-runtime-implementation-1.md
→ deleted

.aiassistant/tasks/done/
20260830_2130_aiscc-p1-8-design-terminal-persistence-and-runtime-implementation-1.md
→ present
```

Verify old/new blob identity.

Meaning:

```text
Executor Task completed with mandatory IMPLEMENTATION_BASELINE_GAP stop.

Task done
!= P1-8 runtime completed
!= P1-8 runtime accepted
```

## 4.2 P1-6 2357 lifecycle

Require:

```text
.aiassistant/tasks/active/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md
→ deleted

.aiassistant/tasks/done/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md
→ present
```

Verify old/new blob identity.

Meaning:

```text
2357 Executor implementation turn completed and submitted a runtime candidate.

Task done
!= runtime Human acceptance by itself.

Human acceptance is separately owned by the 0912 terminal acceptance Cycle.
```

Do not restore either active path.

---

# 5. Commit B exact allowlist — 16 path entries

The final Commit B must contain **exactly 16 path entries**.

## 5.1 original terminal-governance paths

```text
1.
.aiassistant/tasks/done/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md

2.
.aiassistant/tasks/done/
20260831_0103_aiscc-p1-6-durable-content-writer-and-historical-read-capability-runtime-rework-1.md

3.
.aiassistant/tasks/done/
20260831_0813_aiscc-p1-6-durable-content-complete-repository-regression-verification-1.md

4.
.aiassistant/records/aiscc/cycles/
20260831_0103_aiscc-p1-6-durable-content-runtime-writer-and-read-capability-authority-hold-1.cycle.md

5.
.aiassistant/records/aiscc/cycles/
20260831_0813_aiscc-p1-6-durable-content-runtime-complete-repository-regression-evidence-hold-1.cycle.md

6.
.aiassistant/records/aiscc/cycles/
20260831_0912_aiscc-p1-6-durable-evidence-content-runtime-final-acceptance-1.cycle.md

7.
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md

8.
.aiassistant/records/aiscc/DECISION_REGISTER.md

9.
.aiassistant/records/aiscc/NEXT_ACTIONS.md

10.
.aiassistant/reports/aiscc/
20260831_0912_aiscc-p1-6-durable-content-accepted-p1-8-runtime-resume-handoff-1.md

11.
.aiassistant/tasks/done/
20260831_0912_aiscc-p1-6-durable-evidence-content-runtime-terminal-acceptance-and-p1-8-resume-handoff-1.md
```

## 5.2 P1-8 2130 lifecycle path entries

```text
12.
.aiassistant/tasks/active/
20260830_2130_aiscc-p1-8-design-terminal-persistence-and-runtime-implementation-1.md
→ deletion

13.
.aiassistant/tasks/done/
20260830_2130_aiscc-p1-8-design-terminal-persistence-and-runtime-implementation-1.md
→ addition
```

## 5.3 already-issued 0919 correction provenance

```text
14.
.aiassistant/tasks/done/
20260831_0919_aiscc-p1-6-durable-content-runtime-terminal-acceptance-governance-allowlist-correction-1.md

15.
.aiassistant/records/aiscc/cycles/
20260831_0919_aiscc-p1-6-runtime-terminal-governance-p1-8-task-lifecycle-omission-correction-1.cycle.md
```

## 5.4 missing P1-6 2357 active-path deletion

```text
16.
.aiassistant/tasks/active/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md
→ deletion
```

The corresponding done addition is already entry `1`.

Therefore:

```text
exact Commit B path-entry count:
16
```

---

# 6. why this is 16, not 17

For 2357:

```text
done addition
→ already counted in original terminal-governance set

active deletion
→ previously omitted
```

Therefore the new correction adds only:

```text
+1 path entry
```

to the revision-1 count of 15.

No new Task ID/Cycle is added in revision 2.

---

# 7. staging requirement

Use explicit path staging.

Do not use:

```text
git add .
git add -A
```

Stage exact deletion paths explicitly as well.

Before Commit B:

```text
git diff --cached --name-only
```

must equal the exact 16-path set above.

Also verify:

```text
src/**:
0

tests/**:
0

migrations/**:
0

.aiassistant/rules/**:
0

.aiassistant/reports/target/**:
0
```

If count != 16 or any different path appears:

```text
STOP
→ TERMINAL_GOVERNANCE_STAGED_SET_MISMATCH
```

---

# 8. 0912 final acceptance Cycle

Create/update as required by the original 0912 Task.

It must bind the actual Commit A:

```text
8320a3c567a58bab5f728a88d5c88862392d187c
```

and exact runtime:

```text
13 paths
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721
```

It must preserve:

```text
Human P1-6 durable evidence-content extension runtime final review
→ HUMAN_PROVIDED / ACCEPTED

complete repository
→ 195/195 PASS

P1-6 Durable Evidence Content Extension Runtime
→ ACCEPTED / CLOSED

P1-8 prerequisite
→ SATISFIED

P1-8 Runtime
→ NOT_STARTED / RESUME_AUTHORIZED
```

Add explicit lifecycle notes:

```text
2130 P1-8 Task active→done
→ completed by mandatory baseline-gap stop
→ does not mean P1-8 runtime accepted

2357 P1-6 durable-content implementation Task active→done
→ executor turn lifecycle completion
→ Human runtime acceptance is separately recorded by this Cycle
```

No placeholder SHA.

---

# 9. P1-8 resume handoff

Create/update:

```text
.aiassistant/reports/aiscc/
20260831_0912_aiscc-p1-6-durable-content-accepted-p1-8-runtime-resume-handoff-1.md
```

Bind exact Commit A:

```text
8320a3c567a58bab5f728a88d5c88862392d187c
```

and the accepted runtime aggregate:

```text
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721
```

Preserve original 0912 handoff requirements.

Do not start P1-8 runtime.

---

# 10. canonical state

Update exactly as original 0912 Task required:

```text
P1-6 core
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Design
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Runtime
→ HUMAN_PROVIDED / ACCEPTED / CLOSED

accepted runtime commit
→ 8320a3c567a58bab5f728a88d5c88862392d187c

accepted runtime aggregate
→ 2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721

P1-8 blocker
→ RESOLVED

P1-8 Runtime
→ NOT_STARTED / RESUME_AUTHORIZED / NEXT_ACTION

P2
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

`NEXT_ACTIONS.md`:

```text
P1-8 Runtime Resume
```

---

# 11. Commit B

Recommended message remains:

```text
chore(governance): accept durable evidence content runtime

Record Human final acceptance of the P1-6 durable evidence-content runtime,
preserve its runtime review and verification provenance, resolve the P1-8
durable-content prerequisite, and open P1-8 runtime resume without starting it.
```

Create one Commit B only.

Record:

```text
P1_6_DURABLE_CONTENT_RUNTIME_TERMINAL_COMMIT=<SHA>
```

Do not amend Commit A or Commit B.

---

# 12. final lineage

Require:

```text
bc446d9530e28f9b10602c9f1dd5232a97221a10
→ 8320a3c567a58bab5f728a88d5c88862392d187c
→ <Commit B>
```

Verify:

```text
Commit A:
13 runtime paths only
aggregate 2290da92...

Commit B:
16 governance path entries only
no source/test/migration/design rule
```

---

# 13. final workspace

After Commit B:

```text
HEAD:
Commit B

tracked worktree:
clean

index:
clean

2130 active:
absent

2130 done:
present

2357 active:
absent

2357 done:
present

0919 correction Task:
done

P1-8 runtime:
NOT_STARTED
```

Ignored target bundles may remain.

No push.

---

# 14. mandatory stop

STOP on:

```text
HEAD != Commit A

Commit A mismatch

runtime byte drift

Commit B staged count != 16

2130 old/new blob mismatch

2357 old/new blob mismatch

runtime source/test/migration appears in Commit B

P1-8 runtime implementation appears

unexpected tracked dirty path
```

Use:

```text
TERMINAL_GOVERNANCE_STAGED_SET_MISMATCH
```

or exact narrower blocker.

Do not fix source.

---

# 15. expected final state

```text
P1-6 Durable Evidence Content Extension Runtime:
HUMAN_PROVIDED / ACCEPTED / CLOSED

Commit A:
8320a3c567a58bab5f728a88d5c88862392d187c

Commit B:
<exact SHA>

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

# 16. report additions

Report exact:

```text
Commit A verification

2130:
active deletion
done addition
old/new blob identity

2357:
active deletion
done addition
old/new blob identity

Commit B exact 16-path staged set

Commit B SHA

final clean worktree/index

P1-8 runtime NOT_STARTED
```
