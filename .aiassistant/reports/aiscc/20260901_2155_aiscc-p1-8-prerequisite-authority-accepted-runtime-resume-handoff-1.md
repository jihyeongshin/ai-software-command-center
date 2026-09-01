# P1-8 Prerequisite Authority Accepted — Runtime Reconciliation Resume Handoff

## terminal status

```text
P1-8 Project Memory and Cycle Admission Design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 NEXT_ACTION_CONTEXT Source Authority Corrected Revision:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 Prerequisite Owner Authority Exact-Contract/Source-Enrollment Design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 Runtime:
NOT_ACCEPTED / SEPARATE_REWORK_RESUME_AUTHORIZED

P2/P3:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

This handoff authorizes only a separately reviewed P1-8 runtime reconciliation/resume Task. It does not accept the
existing runtime candidate and does not authorize P2/P3, deployment, Public Live, or Project Source mirror work.

## Human and Command Center authority

Human exact text:

```text
Accept
```

Binding and review:

```text
binding = JOINT_EXACT_BYTES
Human = HUMAN_PROVIDED / ACCEPTED
Command Center = SUBSTANTIVE_REVIEW_PERFORMED / ACCEPTED_CANDIDATE
JCS fingerprints = 22 / 22 PASS / mismatch 0
unsafe normative JSON integers = 0
```

The acceptance applies only to:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
7cf27b77bb961280becfc55ecf8e71c9406da9b7b91df0d2697132c2655108db

.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
8b19970629c55629df1560f2329b529992eceb86d5e4216baf0b7e78d3876960
```

## exact persistence lineage

```text
historical source design Commit A:
35901125cc5842734cf1e8eb3374d10e4ee866e3

historical source terminal governance Commit B:
683aaee84d1fc09e9371dd214efc3ff58b7225ee

historical final Cycle:
.aiassistant/records/aiscc/cycles/20260831_1619_aiscc-p1-8-next-action-context-source-authority-final-acceptance-1.cycle.md

new joint accepted design Commit A:
b271f98df7d53edd3d3bc418443ff192e7aa4cfb

new final acceptance Cycle:
.aiassistant/records/aiscc/cycles/20260901_2155_aiscc-p1-8-jcs-safe-integer-joint-design-final-acceptance-1.cycle.md

terminal governance Commit B:
THIS_COMMIT
resolution: git commit containing this exact handoff path
```

Historical commits and Cycles are append-only lineage and must not be amended, reset, or reinterpreted as accepting
later bytes.

## accepted contract summary

1. Every normative sequence/high-watermark JSON integer maximum is `9007199254740991` under `JCS_RFC8785`.
2. Arbitrary-precision lexical JSON hashing and custom JCS dialects are forbidden.
3. `NEXT_ACTION_CONTEXT` semantic owner is `EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY / NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY_V1`.
4. CURRENT ProjectMemory is contextual/eligibility input and is not priority authority.
5. `P1_8_NEXT_ACTION_SELECTION_POLICY_AUTHORITY_V1` owns class-to-rank mapping.
6. TaskConstraint has exact `PROJECT / TASK_CONTRACT / WORK_RUN` scopes and immutable `ISSUED / SUPERSEDED / REVOKED` events with certified complete-prefix snapshots.
7. P1-4 blocker taxonomy is closed; `SECURITY_BOUNDARY` is non-resumable; the single durable resolution authority is `P1_4BlockerResolvedAttestationV1`.
8. Concrete CYCLE_DERIVED descriptor/ActionRef count is `0`; no placeholder ActionRef is authority.
9. `NextActionSelection != TransitionDecision`; `TaskIssuanceCandidate != TaskContract`; Task issuance owner remains `EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY`.
10. P1-4/P1-6/P1-7 authority semantics and historical/current separation are consumed by reference and are not duplicated or changed.

## preserved unaccepted runtime candidate

```text
path count:
19

aggregate SHA-256:
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

Exact paths:

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

These bytes were reviewed before the accepted contracts were finalized. They are uncommitted, unaccepted, and were
not modified, staged, tested, or committed by terminal persistence. Their identity is only the start point for a new
runtime reconciliation.

## exact runtime resume scope

The fresh runtime Task must:

1. verify terminal governance HEAD, Commit A, both accepted rule blob SHA values, and the exact 19-path aggregate;
2. read the accepted rules and reconcile the existing runtime schemas, persistence, owner events, guards, capability boundaries and tests;
3. preserve P1-4/P1-6/P1-7 ownership and all non-substitution rules;
4. use current enrolled external context authority without making caller/configuration/Memory/proposal an authority;
5. generate new targeted and complete-repository evidence appropriate to the runtime delta;
6. leave the runtime candidate uncommitted until a separate terminal-acceptance Task;
7. report Human runtime verification as `HUMAN_PENDING` until Human review occurs.

Mandatory gate:

```text
runtime reconciliation completed != runtime accepted
Command Center review required
Human runtime final review required
```

## first-session preflight

Before any runtime mutation:

```text
1. verify branch and terminal governance HEAD;
2. verify Commit A b271f98df7d53edd3d3bc418443ff192e7aa4cfb and its exact two committed blobs;
3. verify both accepted rule working-tree bytes are clean against HEAD;
4. verify index is empty;
5. verify the exact 19 runtime paths and aggregate 84641ac35f...;
6. stop on any unexpected dirty path or identity mismatch;
7. do not reset or clean the preserved runtime candidate.
```

No P2/P3, Self-Dogfooding, provider/network/deployment, or Public Live work begins from this handoff.
