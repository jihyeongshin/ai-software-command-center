# AISCC Cycle Record

## meta

- cycle_id: `20260831_0919_aiscc-p1-6-runtime-terminal-governance-p1-8-task-lifecycle-omission-correction-1`
- date: `2026-08-31T09:19:00+09:00`
- phase: `P1-6 Durable Evidence Content Runtime Terminal Persistence`
- result_status: `HOLD_REWORK_REQUIRED`
- reject_cause: `TERMINAL_GOVERNANCE_ALLOWLIST_OMITTED_EXISTING_P1_8_TASK_LIFECYCLE_MOVE`
- execution_mode: `MANUAL_COMMAND_CENTER`

## executor stop

Executor correctly stopped with:

```text
DIRTY_WORKSPACE_MIXED
```

Verified facts:

```text
HEAD:
bc446d9530e28f9b10602c9f1dd5232a97221a10

accepted design SHA:
MATCH

runtime 13-path identity:
MATCH

runtime aggregate:
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721

index:
empty

Commit A:
NOT_CREATED

Commit B:
NOT_CREATED
```

Unexpected tracked lifecycle move:

```text
D  .aiassistant/tasks/active/20260830_2130_aiscc-p1-8-design-terminal-persistence-and-runtime-implementation-1.md

?? .aiassistant/tasks/done/20260830_2130_aiscc-p1-8-design-terminal-persistence-and-runtime-implementation-1.md
```

The two blobs are identical.

## command-center finding

This is not unrelated dirty state.

The 2130 Task itself required:

```text
At Task completion move:

.aiassistant/tasks/active/
20260830_2130_aiscc-p1-8-design-terminal-persistence-and-runtime-implementation-1.md

→

.aiassistant/tasks/done/
20260830_2130_aiscc-p1-8-design-terminal-persistence-and-runtime-implementation-1.md
```

and explicitly defined that lifecycle move as part of the uncommitted review set.

The Task completed by correctly stopping P1-8 runtime on the durable-content prerequisite baseline gap.
Therefore the lifecycle transition is legitimate historical governance provenance and must be persisted.

The 0912 closure Task incorrectly omitted this existing lifecycle move from its Commit B allowlist.

## correction

Do NOT alter runtime source/test/migration.

Do NOT create a pre-Commit-A governance commit.

Preserve the intended runtime terminal lineage:

```text
bc446d9530e28f9b10602c9f1dd5232a97221a10
→ Commit A: exact accepted 13 runtime paths
→ Commit B: terminal governance
```

Correct Commit B allowlist:

```text
original 11 governance paths
+ 2130 active deletion
+ 2130 done addition
= exact 13 path entries
```

The 2130 active→done lifecycle is one logical rename but two Git path entries.

## judgment

```text
P1-6 Durable Evidence Content Extension Runtime:
HUMAN_PROVIDED / ACCEPTED
terminal persistence:
REWORK_REQUIRED / not yet closed

runtime candidate:
UNCHANGED / ACCEPTED

P1-8 Runtime:
NOT_STARTED / blocker resolution pending terminal persistence
```
