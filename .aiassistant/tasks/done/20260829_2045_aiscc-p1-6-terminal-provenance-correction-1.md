# 작업지시서: P1-6 Terminal Provenance Correction

## meta

- task_id: `20260829_2045_aiscc-p1-6-terminal-provenance-correction-1`
- created_at: `2026-08-29T20:45:00+09:00`
- phase: `P1-6 Evidence Admission`
- work_type: `COMMAND_CENTER_RECORD_UPDATE`
- evidence_profile: `BASIC`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `COMMAND_CENTER_PROVENANCE`
- expected_start_head: `d80e61f65b048f3d555192ec3a13d296945feb52`
- runtime_acceptance_commit: `f36f19f5b84cef9bc1452e7cb9e9e36c4ae2873e`
- terminal_governance_commit: `d80e61f65b048f3d555192ec3a13d296945feb52`
- accepted_runtime_candidate_count: `21`
- accepted_runtime_candidate_aggregate_sha256: `a583647cc94028874aaf78727e854b537dd033a3670332737aaa7fa53d6469f9`
- p1_6_status: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- p1_7_status: `NOT_STARTED / CURRENT NEXT PHASE`

---

# 1. purpose

Correct only stale/pre-closure provenance text in the already committed P1-6 terminal Cycle.

This Task MUST NOT reopen or modify the accepted runtime implementation.

The following are already terminally valid:

```text
Commit A:
f36f19f5b84cef9bc1452e7cb9e9e36c4ae2873e

Commit B:
d80e61f65b048f3d555192ec3a13d296945feb52

P1-6 Runtime:
HUMAN_PROVIDED / ACCEPTED / CLOSED
```

This is an additive governance correction.

---

# 2. predecessor verification

Before mutation verify:

```text
HEAD ==
d80e61f65b048f3d555192ec3a13d296945feb52
```

Verify parent chain:

```text
d80e61f65b048f3d555192ec3a13d296945feb52
parent ==
f36f19f5b84cef9bc1452e7cb9e9e36c4ae2873e

f36f19f5b84cef9bc1452e7cb9e9e36c4ae2873e
parent ==
192e223854a02293809cf6675e3a329e099e628d
```

Verify current repository state has no runtime/product dirty paths.

If HEAD differs:

```text
STOP
→ BLOCKED_PREDECESSOR_HEAD_DRIFT
```

If runtime/product source is dirty:

```text
STOP
→ DIRTY_WORKSPACE_MIXED
```

Do not clean/reset it.

---

# 3. authoritative correction target

Only this existing terminal Cycle body may be semantically corrected:

```text
.aiassistant/records/aiscc/cycles/
20260829_1920_aiscc-p1-6-evidence-admission-runtime-final-acceptance-1.cycle.md
```

Also place the Command Center HOLD Cycle:

```text
.aiassistant/records/aiscc/cycles/
20260829_2045_aiscc-p1-6-terminal-provenance-incomplete-hold-1.cycle.md
```

Task lifecycle path:

```text
.aiassistant/tasks/active/
20260829_2045_aiscc-p1-6-terminal-provenance-correction-1.md

→

.aiassistant/tasks/done/
20260829_2045_aiscc-p1-6-terminal-provenance-correction-1.md
```

---

# 4. exact terminal Cycle corrections

Do not rewrite unrelated accepted content.

Perform these exact semantic corrections.

## 4.1 terminal governance commit

Change:

```text
terminal governance commit:
NOT_SELF_REFERENCED_IN_CYCLE
```

to:

```text
terminal governance commit:
d80e61f65b048f3d555192ec3a13d296945feb52
```

This does not create self-reference because Commit B already exists and this correction is persisted by a later commit.

## 4.2 public provenance completion

Change:

```text
public_provenance_satisfied:
pending terminal Git persistence by closure Task
```

to an exact equivalent of:

```text
public_provenance_satisfied:
Yes — runtime acceptance Commit A and terminal governance Commit B persisted
```

Do not change the Human acceptance result.

## 4.3 stale future conditional

Replace the section introduction:

```text
After the closure Task successfully persists the exact accepted runtime candidate and canonical terminal state:
```

with an exact post-closure statement equivalent to:

```text
With terminal persistence complete, the next phase is:
```

The resulting next action remains:

```text
P1-7 Human Gate and Judgment
→ next phase
→ NOT_STARTED
```

## 4.4 public provenance mapping runtime commit

Change:

```text
runtime implementation acceptance commit:
TO_BE_FILLED_BY_CLOSURE_TASK
```

to:

```text
runtime implementation acceptance commit:
f36f19f5b84cef9bc1452e7cb9e9e36c4ae2873e
```

## 4.5 sensitive-data check status

Change the pre-closure wording:

```text
sensitive_data_check:
required before terminal commits; no secret/private material may enter public provenance
```

to the completed fact supported by the 1920 Executor report:

```text
sensitive_data_check:
PASS — strict UTF-8/control-character and secret/private marker scan completed before terminal closure
```

Do not invent a broader security claim.

---

# 5. do not change canonical phase state

The submitted 1920 bundle already correctly states:

```text
P1-6 Design:
ACCEPTED / CLOSED

P1-6 Runtime:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-7:
NOT_STARTED / CURRENT NEXT PHASE

P1-8:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

Therefore do not modify:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

unless actual repository bytes contradict the submitted closure bundle.

If they contradict:

```text
STOP
→ POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Do not silently expand this Task.

---

# 6. runtime source immutability

This Task permits **zero** product/runtime/test/migration source modification.

Do not modify:

```text
migrations/**
src/**
tests/**
```

Verify the accepted Commit A remains reachable and no source changes are introduced.

The 21-path accepted runtime aggregate remains:

```text
a583647cc94028874aaf78727e854b537dd033a3670332737aaa7fa53d6469f9
```

A full source re-export/retest is not required.

---

# 7. allowed commit

One additive governance correction commit is explicitly authorized.

Allowed staged paths only:

```text
.aiassistant/records/aiscc/cycles/
20260829_1920_aiscc-p1-6-evidence-admission-runtime-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260829_2045_aiscc-p1-6-terminal-provenance-incomplete-hold-1.cycle.md

.aiassistant/tasks/done/
20260829_2045_aiscc-p1-6-terminal-provenance-correction-1.md
```

No other path may be staged.

Forbidden:

```text
git add .
git add -A
git commit --amend
rebase/reset/history rewrite
git push
```

Recommended commit message:

```text
chore(governance): correct P1-6 terminal provenance

Replace stale pre-closure placeholders in the P1-6 terminal acceptance Cycle with
the already-persisted runtime and governance commit provenance, record completed
public-provenance and sensitive-data checks, and preserve P1-6 as accepted/closed
before starting P1-7 design.
```

---

# 8. verification

Required executor evidence:

```text
start HEAD exact
Commit A/B parent chain exact
runtime/product dirty paths = 0
three allowed staged paths only
git diff --check PASS
UTF-8/control-character PASS
placeholder scan PASS
final terminal Cycle contains:
  f36f19f5...
  d80e61f6...
  public_provenance_satisfied completed
  sensitive_data_check PASS
and contains no:
  TO_BE_FILLED_BY_CLOSURE_TASK
  pending terminal Git persistence by closure Task
final Git index empty
no push
```

Also search the corrected terminal Cycle for stale closure-specific placeholder/status strings.

Do not count occurrences inside the historical Task File as defects; the Task itself legitimately contains instructions referring to placeholders.

---

# 9. evidence contract

executor_required:

```text
STATIC_DOCUMENT
GIT_PROVENANCE
PLACEHOLDER_SCAN
UTF8_CONTROL_CHARACTER
SECRET_PRIVATE_MARKER_SCAN
```

reuse_allowed:

```text
P1-6 runtime acceptance and 132 PASS verification
because no runtime source is modified
```

human_owned:

```text
already provided:
Human P1-6 runtime final review
판정: ACCEPTED
```

not_required:

```text
runtime tests
PostgreSQL
provider
network
browser
deployment
P1-7 verification
```

forbidden:

```text
runtime source mutation
P1-7/P1-8 implementation
remote Git action
deployment
```

---

# 10. accept criteria

All must hold:

```text
HEAD started at d80e61f65b048f3d555192ec3a13d296945feb52

Commit A/B chain verified

terminal Cycle has no unresolved closure placeholder

terminal Cycle no longer says public provenance is pending

runtime acceptance commit = f36f19f5...

terminal governance commit = d80e61f6...

sensitive_data_check reflects completed closure evidence

P1-6 remains ACCEPTED / CLOSED

P1-7 remains NOT_STARTED / CURRENT NEXT PHASE

no runtime/product source changed

one narrow governance correction commit only

final workspace/index clean
```

---

# 11. report/export

Target:

```text
.aiassistant/reports/target/
20260829_2045_aiscc-p1-6-terminal-provenance-correction-1/
```

Required:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
```

Export project-relative copies of:

```text
corrected 1920 terminal Cycle
2045 HOLD Cycle
2045 done Task
```

Report:

```text
start HEAD
Commit A/B parent chain
exact corrections
staged paths
correction commit hash
final HEAD/status
placeholder scan
runtime source mutation count
P1-6/P1-7 final state
provider/network/credential actions
preserved paths
next recommendation
```

---

# 12. final state / next action

After successful correction:

```text
P1-6:
HUMAN_PROVIDED / ACCEPTED / CLOSED

terminal provenance:
COMPLETE

P1-7:
NOT_STARTED / CURRENT NEXT PHASE
```

Next Browser Command Center action:

```text
issue P1-7 Human Gate and Judgment design Task
```

Do not implement P1-7 in this Task.

---

# 13. preserved exact paths

Must survive cleanup:

```text
.aiassistant/records/aiscc/cycles/
20260829_1920_aiscc-p1-6-evidence-admission-runtime-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260829_2045_aiscc-p1-6-terminal-provenance-incomplete-hold-1.cycle.md

.aiassistant/tasks/done/
20260829_2045_aiscc-p1-6-terminal-provenance-correction-1.md

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

.aiassistant/reports/aiscc/
20260829_1227_aiscc-p1-6-design-accepted-command-center-handoff-1.md
```
