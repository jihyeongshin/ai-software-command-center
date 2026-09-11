# 작업지시서: P2-3 A2 final acceptance Git persistence + state reconciliation

## meta

- task_id: `20260911_1815_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-1`
- created_at: `2026-09-11T18:15:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `GIT_PERSISTENCE / STATE_RECONCILIATION`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `REQUIRED`
- fresh_ide_executor_chat_reason: `accepted implementation authority → Git persistence and canonical state-record mutation`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. Python discipline

Do not assume bare:

```text
python
python3
py
```

is valid.

Do not run bare `python` as a probe.

Known interpreter candidate if file hashing/verification scripting is needed:

```text
C:\Users\oracl\AppData\Roaming\uv\python\cpython-3.12.14-windows-x86_64-none\python.exe
```

Repository test interpreter:

```text
.venv\Scripts\python.exe
```

No product tests are required unless an identity invariant fails, in which case STOP rather than rerun.

# 1. inbound transport

Verify Browser ZIP filename/SHA-256 from the Short Prompt.

Place current TASK first:

```text
.aiassistant/tasks/active/20260911_1815_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-1.md
```

Read fully.

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_1815_aiscc-p2-3-a2-implementation-final-acceptance-persistence-entry-1.cycle.md
SHA-256:
02d6500f3352620eecce150eee9ae9c675f53e37a0d6586494ef778aeed8ccd9

.aiassistant/reports/aiscc/20260911_1815_aiscc-p2-3-a2-implementation-final-acceptance-judgment-1.md
SHA-256:
0d4c83c4d357c1e1250f595f9148d2c3525ba7f11737d7ed00059cca27b9678d
```

Bootstrap failure before current Task placement:

```text
STOP
no Git mutation
no report/export
```

# 2. base repository gate

Require:

```text
branch:
main

HEAD:
876f232880e652fbf715f13c13b8cc03d27404f0

HEAD tree:
0f855b67fcad1be1cb4f635b6b4db8856c43da64

index:
empty
```

Do not reset, restore, stash, clean, checkout, or absorb unexpected dirt.

# 3. exact accepted pre-delivery dirt

Before placing this delivery, the exact Git-visible set is 68 paths:

- `.aiassistant/tasks/done/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1824_aiscc-p2-3-a2-feasibility-accepted-production-integration-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1824_aiscc-p2-3-a2-feasibility-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1948_aiscc-p2-3-a2-production-integration-static-and-runtime-evidence-binding-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-judgment-1.md`
- `.aiassistant/tasks/done/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_2215_aiscc-p2-3-a2-security-clock-domain-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-mismatch-judgment-1.md`
- `.aiassistant/tasks/done/20260910_2355_aiscc-p2-3-a2-prepared-owner-model-reconciliation-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_2355_aiscc-p2-3-a2-prepared-owner-audit-accepted-model-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2355_aiscc-p2-3-a2-prepared-owner-contract-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0105_aiscc-p2-3-a2-materialization-output-provenance-binding-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0105_aiscc-p2-3-a2-owner-model-static-failure-materialization-output-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0105_aiscc-p2-3-a2-owner-model-static-failure-materialization-output-binding-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-contract-test-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-test-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-test-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0240_aiscc-p2-3-a2-static-command-transport-and-executable-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0240_aiscc-p2-3-a2-static-command-transport-failure-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0240_aiscc-p2-3-a2-static-command-transport-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0335_aiscc-p2-3-a2-pycompile-cache-cleanup-and-proof-admission-reverification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0335_aiscc-p2-3-a2-executable-proof-complete-workspace-residue-cleanup-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0335_aiscc-p2-3-a2-executable-proof-workspace-residue-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0345_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0345_aiscc-p2-3-a2-executable-proof-admitted-s2-authority-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0345_aiscc-p2-3-a2-workspace-reconciled-executable-proof-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0920_aiscc-p2-3-a2-s2-authority-audit-accepted-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-authority-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1120_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-static-rework-and-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1120_aiscc-p2-3-a2-s2-static-failure-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1120_aiscc-p2-3-a2-s2-static-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1240_aiscc-p2-3-a2-s2-negative-basis-test-contract-rework-and-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1240_aiscc-p2-3-a2-s2-authority-test-contract-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1240_aiscc-p2-3-a2-s2-authority-test-assertion-mismatch-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1250_aiscc-p2-3-a2-s2-authority-proof-only-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1250_aiscc-p2-3-a2-s2-test-rework-admitted-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1250_aiscc-p2-3-a2-s2-static-verifier-extra-postcondition-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1500_aiscc-p2-3-a2-s2-rework-transition-denial-root-cause-diagnostic-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1500_aiscc-p2-3-a2-s2-authority-proof-failed-transition-denial-diagnostic-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1500_aiscc-p2-3-a2-s2-negative-judgment-transition-denial-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1805_aiscc-p2-3-a2-s2-rework-spec-test-input-correction-and-full-proof-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1805_aiscc-p2-3-a2-s2-denial-root-cause-accepted-test-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1805_aiscc-p2-3-a2-s2-transition-denial-diagnostic-final-acceptance-judgment-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/driver.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `src/aiscc/evidence/models.py`
- `src/aiscc/evidence/repository.py`
- `src/aiscc/judgment/models.py`
- `src/aiscc/judgment/authority.py`
- `config/evidence/stockroom-capture.v1.json`
- `config/human/stockroom-capture.v1.json`
- `config/judgment/stockroom-capture.v1.json`
- `config/judgment/stockroom-capture.v2.json`
- `tests/unit/scenarios/test_owner_composition.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `tests/integration/evidence/test_postgres_evidence_admission.py`
- `tests/integration/human/test_postgres_human_gate_judgment.py`

After current Cycle/Judgment placement, excluding active current Task:

```text
70 exact Git-visible paths
```

With current active Task present:

```text
71 exact Git-visible paths
```

Any extra/missing path:

```text
DIRTY_WORKSPACE_MIXED
→ STOP_WITH_REPORT_EXPORT
```

# 4. accepted product identity

Recompute deterministic inventory over all regular files under:

```text
src
config
tests
migrations
```

excluding:

```text
**/__pycache__/**
*.pyc
```

Use sorted records:

```text
relative-path<TAB>byte-size<TAB>sha256
```

Require:

```text
file count:
203

aggregate SHA-256:
3aa781baaf25e09edd15f0713f7d42fc066d51092403cdc473f5030af684b4eb
```

Require exact accepted 1805 test:

```text
tests/integration/human/test_postgres_human_gate_judgment.py
SHA-256:
74998881f78310ec85ac2eb500c754db6b816ae5939f9d09ac9e1d41418f666e
```

Mismatch:

```text
ACCEPTED_CANDIDATE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

Do not rerun tests to compensate for byte mismatch.

# 5. current Task lifecycle

Move current active Task byte-identically to:

```text
.aiassistant/tasks/done/20260911_1815_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-1.md
```

Verify its SHA-256 remains the Browser-issued Task SHA from this delivery.

After movement, require exact 71-path Git-visible set:

- `.aiassistant/tasks/done/20260910_1738_aiscc-p2-3-a2-production-owner-bootstrap-integration-feasibility-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1738_aiscc-p2-3-a1-terminal-persisted-a2-feasibility-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1738_aiscc-p2-3-a1-terminal-state-persistence-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1824_aiscc-p2-3-a2-feasibility-accepted-production-integration-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1824_aiscc-p2-3-a2-feasibility-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260910_1948_aiscc-p2-3-a2-production-integration-static-and-runtime-evidence-binding-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-judgment-1.md`
- `.aiassistant/tasks/done/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_2215_aiscc-p2-3-a2-security-clock-domain-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-contract-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2220_aiscc-p2-3-a2-prepared-owner-binding-mismatch-judgment-1.md`
- `.aiassistant/tasks/done/20260910_2355_aiscc-p2-3-a2-prepared-owner-model-reconciliation-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260910_2355_aiscc-p2-3-a2-prepared-owner-audit-accepted-model-reconciliation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260910_2355_aiscc-p2-3-a2-prepared-owner-contract-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0105_aiscc-p2-3-a2-materialization-output-provenance-binding-rework-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0105_aiscc-p2-3-a2-owner-model-static-failure-materialization-output-binding-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0105_aiscc-p2-3-a2-owner-model-static-failure-materialization-output-binding-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-contract-test-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-test-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0228_aiscc-p2-3-a2-materialized-workspace-fixture-test-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0240_aiscc-p2-3-a2-static-command-transport-and-executable-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0240_aiscc-p2-3-a2-static-command-transport-failure-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0240_aiscc-p2-3-a2-static-command-transport-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0335_aiscc-p2-3-a2-pycompile-cache-cleanup-and-proof-admission-reverification-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0335_aiscc-p2-3-a2-executable-proof-complete-workspace-residue-cleanup-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0335_aiscc-p2-3-a2-executable-proof-workspace-residue-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0345_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-contract-audit-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0345_aiscc-p2-3-a2-executable-proof-admitted-s2-authority-audit-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0345_aiscc-p2-3-a2-workspace-reconciled-executable-proof-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-implementation-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_0920_aiscc-p2-3-a2-s2-authority-audit-accepted-implementation-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_0920_aiscc-p2-3-a2-s2-negative-evaluation-authority-audit-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1120_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-static-rework-and-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1120_aiscc-p2-3-a2-s2-static-failure-rework-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1120_aiscc-p2-3-a2-s2-static-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1240_aiscc-p2-3-a2-s2-negative-basis-test-contract-rework-and-proof-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1240_aiscc-p2-3-a2-s2-authority-test-contract-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1240_aiscc-p2-3-a2-s2-authority-test-assertion-mismatch-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1250_aiscc-p2-3-a2-s2-authority-proof-only-retry-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1250_aiscc-p2-3-a2-s2-test-rework-admitted-proof-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1250_aiscc-p2-3-a2-s2-static-verifier-extra-postcondition-failure-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1500_aiscc-p2-3-a2-s2-rework-transition-denial-root-cause-diagnostic-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1500_aiscc-p2-3-a2-s2-authority-proof-failed-transition-denial-diagnostic-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1500_aiscc-p2-3-a2-s2-negative-judgment-transition-denial-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1805_aiscc-p2-3-a2-s2-rework-spec-test-input-correction-and-full-proof-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1805_aiscc-p2-3-a2-s2-denial-root-cause-accepted-test-rework-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1805_aiscc-p2-3-a2-s2-transition-denial-diagnostic-final-acceptance-judgment-1.md`
- `src/aiscc/bootstrap.py`
- `src/aiscc/scenarios/driver.py`
- `src/aiscc/scenarios/composition.py`
- `src/aiscc/scenarios/stockroom_production.py`
- `src/aiscc/evidence/models.py`
- `src/aiscc/evidence/repository.py`
- `src/aiscc/judgment/models.py`
- `src/aiscc/judgment/authority.py`
- `config/evidence/stockroom-capture.v1.json`
- `config/human/stockroom-capture.v1.json`
- `config/judgment/stockroom-capture.v1.json`
- `config/judgment/stockroom-capture.v2.json`
- `tests/unit/scenarios/test_owner_composition.py`
- `tests/integration/scenarios/test_stockroom_binding.py`
- `tests/integration/scenarios/test_stockroom_capture_runner.py`
- `tests/integration/evidence/test_postgres_evidence_admission.py`
- `tests/integration/human/test_postgres_human_gate_judgment.py`
- `.aiassistant/records/aiscc/cycles/20260911_1815_aiscc-p2-3-a2-implementation-final-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1815_aiscc-p2-3-a2-implementation-final-acceptance-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1815_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-1.md`

Index must still be empty before staging.

# 6. Commit A scope

Commit A persists only the exact 71 paths in section 5.

No state-record mutation yet.

Stage by exact path allowlist only.

Do not use:

```text
git add .
git add -A
git add --all
```

After staging require:

```text
staged paths:
71 exact

unstaged Git-visible paths:
0

unexpected staged:
0

missing staged:
0
```

# 7. Commit A

Create exactly one commit:

```text
message:
feat(orchestration): persist P2-3 A2 production authority integration
```

Require:

```text
parent:
876f232880e652fbf715f13c13b8cc03d27404f0

diff-tree changed paths:
71 exact

tree includes exact accepted product aggregate

worktree after Commit A:
clean
```

Record:

```text
COMMIT_A
COMMIT_A_TREE
COMMIT_A_PARENT
```

Do not push.

# 8. canonical state reconciliation

Only after Commit A succeeds, modify exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
```

No other file.

Preserve existing document style and append/reconcile rather than deleting unrelated historical context.

# 9. CURRENT_STATE_SUMMARY required truth

Update the current authoritative summary to express at minimum:

```text
P2:
IN_PROGRESS

P2-1:
CLOSED / PERSISTED

P2-2 Synthetic Stockroom:
CLOSED / PERSISTED

P2-3:
IN_PROGRESS

P2-3 A1 capture-runner core:
CLOSED / PERSISTED

P2-3 A2 production owner/bootstrap + prepared-owner/materialized-output + S2 Judgment authority:
IMPLEMENTATION ACCEPTED
PERSISTED AT COMMIT_A = <exact Commit A>

A2 executable proof:
155 PASS / 0 skip
35 / 35 contract PASS

A2 migration head:
20260901_0008

A2 public/actual runtime:
NOT_EXECUTED

runtime prerequisite verification:
NEXT

actual S1-S4:
NOT_STARTED

corpus/export:
NOT_STARTED

Recorded Replay:
NOT_ADMITTED

P2-4:
NOT_STARTED

distribution/license:
HUMAN_PENDING
```

Do not mark P2-3 complete.

# 10. NEXT_ACTIONS required truth

Set the next critical action to:

```text
P2-3 actual capture runtime prerequisite verification
```

The next action must verify, before actual S1:

```text
local/canonical runtime prerequisites
PostgreSQL identity
Docker/image availability under accepted policy
source repository/materializer prerequisites
provider/runtime configuration availability
security/network/secret restrictions
capture output destination/provenance readiness
```

It must explicitly say:

```text
actual S1 execution:
NOT AUTHORIZED BY THIS NEXT ACTION

actual S2-S4:
NOT AUTHORIZED

Replay:
NOT AUTHORIZED
```

Persistence itself must not issue or execute the runtime-prerequisite Task.

# 11. DECISION_REGISTER required truth

Add an accepted decision entry that captures:

```text
A2 implementation final acceptance
Commit A exact identity
prepared-owner stable seven + factory-authority reconciliation
materialized-output factory-issued provenance
security native TTL clock-domain fix
ToolOutputRef runtime evidence binding
P1-6 durable typed UNSATISFIED evaluation ref/currentness
P1-7 explicit positive vs negative Judgment basis
Judgment v2 additive policy / v1 compatibility
G_REWORK_SPEC remains independent P1-4 system authority
no migration beyond 20260901_0008
bounded proof 155 PASS / 35 of 35
actual runtime still not executed
```

Do not rewrite historical decisions as if they were always part of the old baseline.

# 12. state-record validation

After state edits require:

```text
Git-visible:
3 exact

paths:
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/DECISION_REGISTER.md

index:
empty
```

Run:

```text
git diff --check
```

Require PASS.

No source/config/test changes may reappear.

# 13. Commit B scope

Stage exactly the three state paths.

Require:

```text
staged:
3 exact

unstaged:
0
```

Create exactly one commit:

```text
message:
docs(command-center): reconcile P2-3 A2 persistence state
```

Commit B must:

```text
parent == COMMIT_A
diff-tree paths == exact 3 state records
```

Record:

```text
COMMIT_B
COMMIT_B_TREE
COMMIT_B_PARENT
```

No amend, rebase, squash, merge, tag, or push.

# 14. final Git verification

Require:

```text
HEAD == COMMIT_B
COMMIT_B parent == COMMIT_A
COMMIT_A parent == 876f232880e652fbf715f13c13b8cc03d27404f0

branch:
main

index:
empty

git status --porcelain:
empty
```

Verify Commit A contains exactly 71 changed paths.

Verify Commit B contains exactly 3 changed paths.

Verify current product inventory still equals:

```text
203 files
aggregate:
3aa781baaf25e09edd15f0713f7d42fc066d51092403cdc473f5030af684b4eb
```

The three state records must refer to exact `COMMIT_A`.

# 15. no runtime/test execution

Do not run:

```text
pytest
PostgreSQL
Alembic upgrade
Docker container
materializer
provider/tool
actual S1-S4
Replay
network
```

The accepted 1805 proof is reused because product bytes are unchanged.

# 16. proof reuse classification

Report:

```text
1805 static:
REUSED_ACCEPTED

P1-6/P1-7:
10 PASS / REUSED_ACCEPTED

A2 S1-S4:
2 PASS / REUSED_ACCEPTED

prepared-owner/A1:
74 PASS / REUSED_ACCEPTED

direct-owner:
49 PASS / REUSED_ACCEPTED

compatibility:
20 PASS / REUSED_ACCEPTED

aggregate:
155 PASS / REUSED_ACCEPTED

contract:
35/35 / REUSED_ACCEPTED
```

# 17. failure behavior

Before current Task placement:

```text
bootstrap failure
→ STOP / no report/export
```

After Task placement, any failure:

```text
STOP_WITH_REPORT_EXPORT
```

Do not attempt broad repair.

If Commit A succeeds but later state reconciliation/Commit B fails:

```text
DO NOT reset/revert Commit A
report exact partial persistence state
STOP_WITH_REPORT_EXPORT
```

# 18. required export

Folder:

```text
.aiassistant/reports/target/20260911_1815_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ACCEPTED_CANDIDATE_IDENTITY.md
COMMIT_A_VERIFICATION.md
STATE_RECONCILIATION_VERIFICATION.md
COMMIT_B_VERIFICATION.md
FINAL_GIT_VERIFICATION.md
PROOF_REUSE_VERIFICATION.md
```

Also include byte-preserving copies of:

```text
current Cycle
current Judgment
current done Task

.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
```

Expected:

```text
10 root docs
6 canonical copies
16 members total
```

`EXPORT_MANIFEST.md` covers all 15 non-self entries with relative path, byte size, SHA-256.

Create adjacent verified ZIP with one top-level result directory and CRC PASS.

# 19. success ceiling

Success:

```text
A2 implementation:
ACCEPTED

Commit A:
PERSISTED

canonical state:
RECONCILED / Commit B persisted

worktree:
CLEAN

A2 terminal closure:
BROWSER_JUDGMENT_REQUIRED

runtime prerequisites:
NOT_VERIFIED

actual S1-S4:
NOT_STARTED
```
