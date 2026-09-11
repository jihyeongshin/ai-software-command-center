# 작업지시서: P2-3 A2 final acceptance Git persistence + state reconciliation retry

## meta

- task_id: `20260911_1930_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-retry-1`
- created_at: `2026-09-11T19:30:00+09:00`
- project: `AI Software Command Center (AISCC)`
- work_type: `GIT_PERSISTENCE / STATE_RECONCILIATION_RETRY`
- evidence_profile: `HIGH_RISK`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `876f232880e652fbf715f13c13b8cc03d27404f0`
- required_base_tree: `0f855b67fcad1be1cb4f635b6b4db8856c43da64`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`

# 0. exact correction from 1815

Do not count `.aiassistant/tasks/active/**` as Git-visible.

Canonical repository policy is:

```text
TRACK:
.aiassistant/tasks/done/**

IGNORE:
.aiassistant/tasks/active/**
```

The active Task must exist and be byte-exact, but must be verified separately from the Git-visible count.

Do not modify `.gitignore`.

# 1. inbound transport

Verify Browser delivery ZIP exact filename/SHA-256 from the Short Prompt.

Place current TASK first at:

```text
.aiassistant/tasks/active/20260911_1930_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-retry-1.md
```

Read fully and verify its SHA-256 against this delivery.

Require:

```text
current active Task:
exists
byte-exact
git check-ignore:
ignored by .aiassistant/tasks/active/
```

Then place/hash-verify:

```text
.aiassistant/records/aiscc/cycles/20260911_1930_aiscc-p2-3-a2-persistence-blocked-active-task-ignore-contract-retry-entry-1.cycle.md
SHA-256:
a4883957aab64a04f0e3cf424423c5ceb39f3f04661e8b687e6a03e33b08c567

.aiassistant/reports/aiscc/20260911_1930_aiscc-p2-3-a2-persistence-active-task-ignore-contract-mismatch-judgment-1.md
SHA-256:
2f0a19c9ac6c15c670e530b528b50f86e28c28044e9a8861121d9c89e9af6478
```

Bootstrap failure before active Task placement:

```text
STOP
no Git mutation
no report/export
```

# 2. base Git gate

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

No reset/restore/stash/clean/checkout.

# 3. exact pre-delivery current Git-visible set

Before this delivery, require exactly 71 Git-visible paths:

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
- `.aiassistant/tasks/done/20260911_1815_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1815_aiscc-p2-3-a2-implementation-final-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1815_aiscc-p2-3-a2-implementation-final-acceptance-judgment-1.md`

No extra/missing path.

Require exact 1815 identities:

- `.aiassistant/tasks/done/20260911_1815_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-1.md`  `8a78c6e3f2bc2aa3dc1bd5eb4256837f5b3abbdac63fa0ef852c9ba3f6349ebd`
- `.aiassistant/records/aiscc/cycles/20260911_1815_aiscc-p2-3-a2-implementation-final-acceptance-persistence-entry-1.cycle.md`  `02d6500f3352620eecce150eee9ae9c675f53e37a0d6586494ef778aeed8ccd9`
- `.aiassistant/reports/aiscc/20260911_1815_aiscc-p2-3-a2-implementation-final-acceptance-judgment-1.md`  `0d4c83c4d357c1e1250f595f9148d2c3525ba7f11737d7ed00059cca27b9678d`

# 4. corrected pre-lifecycle visibility gate

After placing current Cycle/Judgment and while current Task remains active:

```text
Git-visible:
73 exact

active current Task:
exists byte-exact
ignored by canonical Git policy
not included in 73
```

Exact Git-visible set:

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
- `.aiassistant/tasks/done/20260911_1815_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1815_aiscc-p2-3-a2-implementation-final-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1815_aiscc-p2-3-a2-implementation-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1930_aiscc-p2-3-a2-persistence-blocked-active-task-ignore-contract-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1930_aiscc-p2-3-a2-persistence-active-task-ignore-contract-mismatch-judgment-1.md`

If the active Task appears in `git status --porcelain`, or if visible count/set differs:

```text
GIT_VISIBILITY_CONTRACT_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 5. accepted candidate identity

Recompute deterministic product inventory over regular files under:

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

Serialization:

```text
sorted relative-path<TAB>byte-size<TAB>sha256
LF joined
NO terminal newline
```

Require:

```text
file count:
203

aggregate SHA-256:
3aa781baaf25e09edd15f0713f7d42fc066d51092403cdc473f5030af684b4eb

tests/integration/human/test_postgres_human_gate_judgment.py:
74998881f78310ec85ac2eb500c754db6b816ae5939f9d09ac9e1d41418f666e
```

Also require current canonical state records still equal the blocked 1815 unchanged identities:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `051041381beb996eebd5ed4ef9397f7e5858d120c9fd157a6055e0dee08419c9`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `7c16fd1c9bbf9d973913e189dd86937d927a0fad8694c62cd8ab55f7144bd7cb`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `a8653da10963e0ff5cbba79b8bbca460681c28a20ac48dabd83056b115516d8e`

Any mismatch:

```text
ACCEPTED_CANDIDATE_OR_STATE_IDENTITY_MISMATCH
→ STOP_WITH_REPORT_EXPORT
```

# 6. current Task lifecycle

Move active current Task byte-identically:

```text
.aiassistant/tasks/active/20260911_1930_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-retry-1.md
→
.aiassistant/tasks/done/20260911_1930_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-retry-1.md
```

Require its SHA-256 unchanged.

After movement:

```text
Git-visible:
74 exact

index:
empty
```

Exact set:

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
- `.aiassistant/tasks/done/20260911_1815_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1815_aiscc-p2-3-a2-implementation-final-acceptance-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1815_aiscc-p2-3-a2-implementation-final-acceptance-judgment-1.md`
- `.aiassistant/records/aiscc/cycles/20260911_1930_aiscc-p2-3-a2-persistence-blocked-active-task-ignore-contract-retry-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260911_1930_aiscc-p2-3-a2-persistence-active-task-ignore-contract-mismatch-judgment-1.md`
- `.aiassistant/tasks/done/20260911_1930_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-retry-1.md`

# 7. Commit A exact scope

Commit A persists exactly the 74 paths in section 6.

Stage by exact path allowlist.

Do not use:

```text
git add .
git add -A
git add --all
```

Require before commit:

```text
staged paths:
74 exact

unstaged Git-visible:
0

unexpected staged:
0

missing staged:
0
```

# 8. Commit A

Create exactly:

```text
message:
feat(orchestration): persist P2-3 A2 production authority integration
```

Require:

```text
parent:
876f232880e652fbf715f13c13b8cc03d27404f0

diff-tree paths:
74 exact

product inventory:
203 files
aggregate 3aa781baaf25e09edd15f0713f7d42fc066d51092403cdc473f5030af684b4eb

worktree after Commit A:
clean
```

Record:

```text
COMMIT_A
COMMIT_A_TREE
COMMIT_A_PARENT
```

No push.

# 9. canonical state reconciliation

Only after Commit A succeeds, modify exactly:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
```

No other path.

Read all three files completely before editing.

Preserve document style and historical entries.

# 10. CURRENT_STATE_SUMMARY required truth

Reconcile at minimum:

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
PERSISTED AT COMMIT_A = <exact COMMIT_A>

A2 executable proof:
155 PASS / 0 skip
35 / 35 contract PASS

A2 migration head:
20260901_0008

A2 actual/public runtime:
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

# 11. NEXT_ACTIONS required truth

Set next critical action:

```text
P2-3 actual capture runtime prerequisite verification
```

It must verify before actual S1:

```text
PostgreSQL identity/readiness
Docker/image availability under accepted policy
source repository/materializer prerequisites
provider/runtime configuration availability
security/network/secret restrictions
capture output/provenance destination readiness
```

Explicitly preserve:

```text
actual S1:
NOT AUTHORIZED BY THIS PERSISTENCE TASK

actual S2-S4:
NOT AUTHORIZED

Replay:
NOT AUTHORIZED
```

Do not issue/execute the runtime-prerequisite Task here.

# 12. DECISION_REGISTER required truth

Append/reconcile an accepted A2 decision with:

```text
A2 final implementation acceptance
exact COMMIT_A identity
prepared-owner stable-seven + factory authority
materialized-output factory-issued provenance
security native TTL clock-domain fix
ToolOutputRef runtime evidence binding
P1-6 typed durable UNSATISFIED evaluation ref/currentness
P1-7 explicit positive vs negative Judgment basis
Judgment v2 additive policy + v1 compatibility
G_REWORK_SPEC independent P1-4 system authority
no migration beyond 20260901_0008
155 PASS / 35 of 35
actual runtime not executed
```

# 13. state-record validation and Commit B

After edits require:

```text
Git-visible:
3 exact

index:
empty

git diff --check:
PASS
```

Exact paths:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
```

Stage exactly those three.

Create exactly:

```text
message:
docs(command-center): reconcile P2-3 A2 persistence state
```

Require:

```text
Commit B parent == COMMIT_A
Commit B diff-tree == exact 3 state records
```

Record:

```text
COMMIT_B
COMMIT_B_TREE
COMMIT_B_PARENT
```

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

Verify:

```text
Commit A:
74 exact paths

Commit B:
3 exact paths

product:
203 files
aggregate 3aa781baaf25e09edd15f0713f7d42fc066d51092403cdc473f5030af684b4eb
```

All three state records must reference the exact COMMIT_A where required.

# 15. proof reuse

No pytest/runtime execution.

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
155 PASS / 0 skip / REUSED_ACCEPTED

contract:
35/35 / REUSED_ACCEPTED
```

# 16. forbidden execution

Do not run:

```text
pytest
PostgreSQL
Alembic upgrade
Docker
materializer
provider/tool
actual S1-S4
Replay
network
push
deployment
```

# 17. failure behavior

Before active Task placement:

```text
bootstrap failure
→ STOP / no report/export
```

After Task placement:

```text
any failure
→ STOP_WITH_REPORT_EXPORT
```

If Commit A succeeds but Commit B/state reconciliation fails:

```text
do not reset/revert Commit A
preserve exact partial persistence
report and export
```

# 18. required export

Folder:

```text
.aiassistant/reports/target/20260911_1930_aiscc-p2-3-a2-final-acceptance-git-persistence-and-state-reconciliation-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ACCEPTED_CANDIDATE_IDENTITY.md
GIT_VISIBILITY_VERIFICATION.md
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
CURRENT_STATE_SUMMARY.md
NEXT_ACTIONS.md
DECISION_REGISTER.md
```

Expected:

```text
11 root docs
6 canonical copies
17 members total
```

`EXPORT_MANIFEST.md` covers all 16 non-self entries.

Create adjacent verified ZIP with one top-level directory and CRC PASS.

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

A2 terminal persistence:
BROWSER_JUDGMENT_REQUIRED

runtime prerequisites:
NOT_VERIFIED

actual S1-S4:
NOT_STARTED
```
