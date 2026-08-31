# 작업지시서: P1-6 Durable Content Complete Repository Regression Verification

## meta

- task_id: `20260831_0813_aiscc-p1-6-durable-content-complete-repository-regression-verification-1`
- created_at: `2026-08-31T08:13:00+09:00`
- phase: `P1-6 Durable Evidence Content Authority Extension Runtime`
- work_type: `VERIFICATION_ONLY`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_6_EVIDENCE_CONTENT`
- expected_start_head: `bc446d9530e28f9b10602c9f1dd5232a97221a10`
- expected_runtime_path_count: `13`
- expected_runtime_aggregate_sha256: `2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721`
- p1_8_runtime_status: `BLOCKED_REQUIRED_EVIDENCE / NOT_RESUMED`

---

# 1. purpose

Verification only.

Do not modify runtime source/tests/migration.

The 0103 direct authority findings are considered CLOSED.

This Task exists only because the rework changed shared repository/service/access APIs but did not provide a
fresh complete-repository regression run.

Place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260831_0813_aiscc-p1-6-durable-content-runtime-complete-repository-regression-evidence-hold-1.cycle.md
```

---

# 2. mandatory preflight

Require:

```text
HEAD ==
bc446d9530e28f9b10602c9f1dd5232a97221a10

runtime paths ==
13

runtime aggregate ==
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721
```

Verify exact per-file SHA from the 0103 manifest.

Any byte drift:

```text
STOP
→ REVIEWED_CANDIDATE_DRIFT
```

Index:

```text
empty
```

No Git add/commit/push.

---

# 3. verification requirement

Run the repository's actual complete automated test suite, using the same or stricter scope than the predecessor
2357 `complete repository 194 PASS` run.

Requirements:

```text
no directory subset

no marker exclusion unless the normal repository complete-suite command itself requires an explicit environment
split

no --ignore / deselection used to hide failures

no xfail conversion added

no test file mutation
```

If PostgreSQL requires a dedicated environment/setup, use the established local loopback PostgreSQL test
environment and include those tests as the repository's normal complete-suite contract requires.

Report:

```text
exact command
collected count
passed
failed
skipped
xfailed/xpassed
deselected
duration
```

---

# 4. predecessor comparison

Predecessor known complete-repository evidence:

```text
2357:
194 PASS
```

Current candidate added/changed tests, so the exact new count need not be forced to 194.

However Executor must explain any collection delta.

Required:

```text
current collected/pass count
vs predecessor 194

delta attributable to:
added/removed/renamed tests
or test-discovery configuration
```

Any unexplained decrease:

```text
STOP
→ COMPLETE_REPOSITORY_COLLECTION_REGRESSION
```

No test may be removed or skipped merely to obtain PASS.

---

# 5. no source mutation

This Task is verification-only.

Allowed tracked mutation:

```text
Task active → done
```

and placement of the already-issued 0813 HOLD Cycle according to repository governance workflow.

Forbidden:

```text
src/**
tests/**
migrations/**
pyproject/config test selection changes
canonical state files
accepted design files
```

If complete repository testing fails:

```text
STOP
→ COMPLETE_REPOSITORY_REGRESSION_FAILED
```

Do not fix source in this Task.

Report exact failing tests/trace summary so Command Center can issue a separate rework Task.

---

# 6. retain existing evidence

Do not rerun merely for repetition unless necessary to satisfy the complete-suite command:

```text
0103 writer capability binding
rogue writer negative
forged/foreign read grant negative
restart
V1/V2 fingerprint
legacy P1-6/P1-7 provenance
ruff
mypy
alembic
```

The existing 0103 evidence remains reusable because runtime bytes must be exact unchanged.

If complete-suite execution naturally reruns them, report that fact.

---

# 7. final byte identity

After verification require:

```text
runtime path count:
13

runtime aggregate:
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721

HEAD:
bc446d9530e28f9b10602c9f1dd5232a97221a10

index:
empty
```

No runtime byte may change.

---

# 8. evidence contract

## executor_required

```text
COMPLETE_REPOSITORY_REGRESSION
COLLECTION_DELTA_EXPLANATION
RUNTIME_BYTE_IDENTITY
GIT_NO_ACTION
```

## reuse_allowed

```text
0103 authority/source review
0103 PostgreSQL targeted regressions
0103 ruff/mypy/alembic/security evidence
```

only if runtime aggregate is unchanged.

## human_owned

```text
P1-6 durable evidence-content runtime final acceptance
→ HUMAN_PENDING
```

---

# 9. export

Target:

```text
.aiassistant/reports/target/
20260831_0813_aiscc-p1-6-durable-content-complete-repository-regression-verification-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

No need to re-export all 13 runtime files if exact predecessor manifest + independently recomputed aggregate is
recorded, but the export must contain enough immutable hash inventory to prove candidate identity.

Include:

```text
0813 HOLD Cycle
done Task
complete repository test evidence
runtime per-file hash inventory
```

---

# 10. expected successful submission state

```text
P1-6 Durable Evidence Content Extension Runtime:
REWORKED_CANDIDATE / HUMAN_PENDING

0103 authority findings:
CLOSED

complete repository regression:
PASS

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE / NOT_RESUMED
```

Command Center next:

```text
PASS / HUMAN_FINAL_REVIEW_REQUIRED
```

if and only if complete-repository regression passes with no unexplained collection regression.

---

# 11. preserved exact paths

Preserve:

```text
.aiassistant/rules/AISCC_DURABLE_EVIDENCE_CONTENT_AUTHORITY.md

.aiassistant/records/aiscc/cycles/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260831_0103_aiscc-p1-6-durable-content-runtime-writer-and-read-capability-authority-hold-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260831_0813_aiscc-p1-6-durable-content-runtime-complete-repository-regression-evidence-hold-1.cycle.md

.aiassistant/tasks/done/
20260830_2357_aiscc-p1-6-durable-evidence-content-design-terminal-persistence-and-runtime-implementation-1.md

.aiassistant/tasks/done/
20260831_0103_aiscc-p1-6-durable-content-writer-and-historical-read-capability-runtime-rework-1.md

.aiassistant/tasks/done/
20260831_0813_aiscc-p1-6-durable-content-complete-repository-regression-verification-1.md
```
