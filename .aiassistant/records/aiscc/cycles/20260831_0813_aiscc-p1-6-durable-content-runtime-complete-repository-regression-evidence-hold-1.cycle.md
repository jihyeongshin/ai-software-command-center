# AISCC Cycle Record

## meta

- cycle_id: `20260831_0813_aiscc-p1-6-durable-content-runtime-complete-repository-regression-evidence-hold-1`
- date: `2026-08-31T08:13:00+09:00`
- phase: `P1-6 Durable Evidence Content Authority Extension Runtime`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `P1_6_EVIDENCE_CONTENT`
- result_status: `HOLD_REQUIRED_EVIDENCE`
- reject_cause: `COMPLETE_REPOSITORY_REGRESSION_NOT_RERUN_AFTER_SHARED_API_BOUNDARY_CHANGE`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260831_0813_aiscc-p1-6-durable-content-runtime-complete-repository-regression-evidence-hold-1.cycle.md`

## reviewed candidate

```text
HEAD:
bc446d9530e28f9b10602c9f1dd5232a97221a10

predecessor runtime:
13 paths /
8119fcb3ea10b3fb86e986b21ca0cd638e14b9021ac903fa007d750124392962

reworked runtime:
13 paths /
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721

reworked relative to predecessor:
7 paths
```

Independent export-byte verification:

```text
13/13 per-file SHA-256:
MATCH

runtime aggregate:
2290da92d56d47336de410fd8848177d71f3965f2556d4363cde9dfa40749721
MATCH
```

## direct 0103 findings

Source-level review closes the two direct runtime findings.

```text
configured P1-6 writer capability binding:
CLOSED

caller-selected repository writer authority parameter:
REMOVED

rogue writer authority:
DENIED

service/repository split writer configuration:
DENIED

owner-issued historical read capability:
CLOSED

forged read grant:
DENIED

foreign read authority:
DENIED

valid P1_8_STRUCTURED_RESULT_V1 grant:
PUBLIC_SAFE + INTERNAL exact read allowed

grant write/mint/export authority:
NONE
```

The accepted PostgreSQL/V1-V2/restart/security behavior remains intact in the reviewed source.

## evidence gap

The predecessor 2357 candidate reported:

```text
task-scoped full unit+integration:
174 PASS

complete repository:
194 PASS
```

The 0103 rework reports:

```text
full unit+integration:
175 PASS

P1-4 PostgreSQL:
18 PASS

P1-6 PostgreSQL:
7 PASS

P1-7 PostgreSQL:
2 PASS
```

but does not report a fresh **complete repository** test run.

The 0103 rework changes shared runtime API boundaries:

```text
PostgresEvidenceRepository.__init__

PostgresEvidenceRepository.admit
→ caller-selected durable_content_authority parameter removed

EvidenceAdmissionService.__init__
→ exact repository-bound writer authority configuration enforced

HistoricalContentAccessGrant / read-authority API
```

Therefore the predecessor complete-repository result cannot substitute for a post-rework complete-repository
regression.

Required invariant:

```text
shared public/internal API boundary changed
→ complete repository regression must be fresh
```

This is an evidence insufficiency, not a newly identified semantic/runtime defect.

## judgment

```text
P1-6 core:
ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Design:
ACCEPTED / CLOSED

P1-6 Durable Evidence Content Extension Runtime:
REWORKED_CANDIDATE / HOLD_REQUIRED_EVIDENCE

direct 0103 authority findings:
CLOSED

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE / NOT_RESUMED

P2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

No Human runtime final review until fresh complete-repository regression passes.

No runtime source mutation is requested by this HOLD.
