# 작업지시서: P3-3 Public Live L1 additive schema and repository transaction primitives implementation

## meta

- task_id: `20260915_1702_aiscc-p3-3-public-live-l1-schema-repository-transaction-primitives-implementation-1`
- created_at: `2026-09-15T17:02:47+09:00`
- work_type: `IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `Yes`
- primary_semantic_owner: `P3-3 Public Live L1 persistence primitives`

## objective

Implement L1 from the frozen Public Live implementation sequence:

```text
Additive schema and repository transaction primitives
```

L1 must create the durable database substrate required by later L2 atomic admission.

L1 MUST NOT implement public HTTP admission, provider dispatch, deployment, frontend, or Live enablement.

## exact baseline

Before transport/substantive work require:

```text
branch = main
HEAD = 209e7534f66e9b07ce9d33742e6993370a70f4fb
index = empty
tracked worktree = clean
Git-visible untracked = 0
```

Mismatch => STOP.

Run first:

```text
python scripts/build_public_replay.py --check
```

PASS required.

## must-read canonical authority

Read current canonical repository files, at minimum:

- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_DB_SCHEMA_PLAN.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_FAILURE_STATE_MACHINE.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_HTTP_CONTRACT.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_HUMAN_DECISIONS.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- architecture/orchestration/security/runtime/provider canonical rules.

Read current persistence implementation, migrations and tests before choosing files.

Do not guess migration framework/path conventions.

## frozen L1 contract

Implement the additive persistence substrate for a **separate Public Live PostgreSQL database / credential boundary**.

The schema must support the Human-accepted frozen design.

Required durable concepts:

```text
public_control
public_campaign
public_day
public_client
public_run
public_idempotency
public_rate_event
public_reservation
public_slot
public_outbox
public_dispatch
public_money_event
public_observation
```

Use the canonical DB schema plan for exact columns/keys/checks/indexes.

Do not invent a smaller incompatible schema.

## initial safety state

Migration/initialization MUST leave Public Live fail-closed.

Required:

```text
public_control:
admission disabled by default

public_slot:
exactly two seeded rows
slot_id = 1, 2
state = FREE

campaign:
no enabled campaign created by migration

provider:
no credentials/config values in DB migration

money:
no positive spend authority created implicitly
```

A successful migration must not make Live callable.

## money representation

Use integer micro-USD authority only.

Frozen values are design constants for later admission, not automatically enabled balances:

```text
per-run reserve:
200000 micro-USD

daily limit:
4000000 micro-USD

campaign limit:
15000000 micro-USD
```

No float/decimal arithmetic may be authoritative for public budget accounting.

Preserve invariant support for:

```text
available + held + settled = limit
```

with nonnegative components.

Do not implement L2 business decisions yet; implement constraints/primitives that make invalid states difficult or impossible.

## clock and transaction primitives

Repository primitives must provide a controlled transaction boundary compatible with later L2 A1.

At minimum support:

- begin controlled Public Live transaction;
- acquire singleton control row lock;
- read database clock after control lock;
- persist/compare monotonic `last_clock` or exact frozen equivalent;
- lock/create campaign/day/client rows in frozen lock order;
- lock both slots in ascending order;
- read idempotency binding under lock;
- create run/read-capability hash identity;
- create reservation/journal identity;
- occupy/free/quarantine slot primitives subject to explicit preconditions;
- create/read outbox identity;
- create dispatch marker for ordinal 1 or 2;
- append immutable observation;
- terminal settlement primitive with idempotent money event support.

The repository may expose lower-level methods.

Do NOT create a public admission service that orchestrates the full A1 flow; that is L2.

## lock ordering

Preserve the frozen order:

```text
control
existing idempotency
campaign
day rows sorted by date
client
slots ascending
runs ascending
dispatch ordinals ascending
```

Do not acquire owner WorkRun locks inside this Public Live transaction boundary.

If existing repository architecture cannot express this safely, STOP with:

`L1_REPOSITORY_ARCHITECTURE_CONFLICT`

and provide source evidence rather than implementing an unsafe alternative.

## DB constraints

Implement source-grounded constraints/indexes required to enforce or support:

- two-slot domain;
- one run per slot;
- one slot per run;
- unique campaign/idempotency hash;
- unique idempotency run binding;
- dispatch ordinal only 1 or 2;
- unique `(run_id, ordinal)`;
- unique read-capability hash;
- money values nonnegative;
- reservation/settlement bounds;
- one RESERVE and one SETTLE journal identity per run;
- append-only observation identity;
- no silently negative ledger;
- explicit bounded enums/states;
- UTC-aware timestamps;
- indexes needed for client rolling-hour/day and campaign/day lookups;
- retention/expiry scans.

Use exact canonical plan as authority.

## repository authority and permissions

The frozen design requires a least-privilege Public Live runtime.

Implement only what can be represented/tested locally without configuring a hosted provider.

Required design intent:

- application runtime does not receive owner/private DB credentials;
- runtime repository API is the intended mutation path;
- destructive/arbitrary DML against journals/control should not be required for normal runtime operation.

If the existing migration/test environment supports role/grant tests safely, implement and test them.

If actual hosted-role creation cannot be faithfully proven locally, represent the migration/SQL contract and classify hosted-role proof as L5/release evidence.

Do not weaken the separate DB design to share owner DB credentials.

## repository implementation quality

Prefer typed domain/repository structures consistent with current codebase.

Do not expose raw dict/string state when current persistence layer has typed patterns.

Do not duplicate existing transaction helpers if they can safely be generalized/reused.

Do not modify owner/private semantics merely to make Public Live easier.

No public API route imports should be necessary in L1.

## exact L1 tests

Implement deterministic automated tests for the L1 layer.

At minimum cover:

1. fresh migration creates required Public Live schema;
2. admission disabled by default;
3. only two FREE slot rows seeded;
4. campaign not automatically enabled;
5. duplicate idempotency binding denied;
6. same run cannot occupy two slots;
7. third slot impossible;
8. dispatch ordinal 3 denied;
9. duplicate dispatch ordinal denied;
10. negative money state denied;
11. invalid reserve/settlement relationship denied;
12. duplicate RESERVE event denied;
13. duplicate SETTLE event denied or exact idempotent repository behavior;
14. read capability hash uniqueness;
15. observation source identity uniqueness;
16. UTC timestamp behavior;
17. control row locking serializes conflicting repository transaction test where current test substrate permits;
18. transaction rollback removes all uncommitted L1 writes;
19. DB clock/last_clock primitive fails closed on regression according to frozen design;
20. migration does not alter owner/private historical rows or Replay artifacts.

Also implement focused repository tests for each newly added mutation primitive.

Do NOT pretend these tests prove:

- multi-Railway-replica behavior;
- Railway ingress identity;
- provider exactly-once;
- hosted role configuration.

Those remain later gates.

## migration compatibility

Before creating migration(s), inspect the exact migration framework and current head.

Requirements:

- additive migration only;
- no destructive owner table rewrite;
- deterministic upgrade;
- safe repository/test database creation from empty/current head;
- explicit downgrade only if project policy permits it and it can preserve unresolved audit liabilities.

If safe downgrade would destroy unresolved public financial/audit evidence, prefer documented forward-only correction consistent with canonical design rather than a dangerous drop path.

Follow repository's established migration policy.

## source scope

Changes are allowed only in the narrow persistence implementation surface discovered from current repository structure:

- migration/schema files;
- persistence/repository/domain types required by L1;
- focused L1 tests;
- minimal test fixtures/helpers required for those tests;
- task lifecycle/provenance artifacts.

Forbidden in L1:

- `public/replay/**`;
- frontend;
- public API routes;
- provider adapters/model profiles;
- Railway/Cloudflare config;
- runtime public admission service;
- owner UI;
- competition submission files;
- unrelated refactors.

If implementation requires a forbidden surface, STOP and report why.

## validation

Run all existing tests relevant to modified persistence/security code.

Also run:

```text
python scripts/build_public_replay.py --check
```

after implementation.

Run the project's normal broader automated suite if feasible within existing local environment.

Do not use external network or paid services.

## no release behavior

At terminal success, this statement must remain true:

```text
Public Live:
NOT_RELEASED

Public admission:
DISABLED

Public HTTP routes:
NOT_IMPLEMENTED_BY_L1

Provider paid calls:
IMPOSSIBLE_FROM_L1
```

## persistence / commit

This implementation Task is allowed to commit.

Before staging:

- move this Task from `.aiassistant/tasks/active/` to `.aiassistant/tasks/done/`;
- create Cycle/Judgment/Handoff canonical lineage from this delivery as already placed;
- create an Executor implementation report in target export only.

Commit message exactly:

```text
feat(aiscc): add public live persistence primitives
```

Do not push/tag/release.

## commit allowlist construction

Because exact migration/source/test filenames depend on current repository layout, the Executor MUST produce a precommit exact allowlist before staging.

The allowlist may contain only:

```text
L1 migration/schema
L1 persistence/domain/repository implementation
L1-focused tests/helpers
this Task/Cycle/Judgment/Handoff
```

No unrelated path.

Write:

`L1_CHANGED_PATH_PLAN.json`

before staging and include:

- every path;
- category;
- why required;
- pre-existing/new;
- source owner.

Then stage exactly that plan and prove staged set equality.

If unrelated working-tree dirt appears, STOP without cleanup.

## acceptance evidence

Target export must contain:

- exact baseline;
- source inventory;
- migration head before/after;
- schema object inventory;
- constraint/index inventory;
- repository primitive inventory;
- test matrix/results;
- negative-state proof;
- fail-closed initialization proof;
- changed-path plan;
- staged manifest;
- commit/postcommit verification;
- terminal workspace.

## result classification

Success:

```text
PERSISTENCE_CANDIDATE / L1_IMPLEMENTED
```

Do NOT claim L2/L3 or Live readiness.

Failure classifications include:

```text
L1_REPOSITORY_ARCHITECTURE_CONFLICT
L1_MIGRATION_POLICY_BLOCK
L1_TEST_BLOCKED
L1_IMPLEMENTATION_REWORK_REQUIRED
```

## target export

Target:

`.aiassistant/reports/target/20260915_1702_aiscc-p3-3-public-live-l1-schema-repository-transaction-primitives-implementation-1/`

Required root artifacts:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SOURCE_INVENTORY.json`
- `MIGRATION_BASELINE.json`
- `SCHEMA_INVENTORY.json`
- `CONSTRAINT_INDEX_INVENTORY.json`
- `REPOSITORY_PRIMITIVE_INVENTORY.json`
- `L1_SECURITY_TEST_MATRIX.json`
- `TEST_RESULTS.json`
- `FAIL_CLOSED_INITIALIZATION.json`
- `L1_CHANGED_PATH_PLAN.json`
- `STAGED_COMMIT_MANIFEST.json`
- `POSTCOMMIT_VERIFICATION.json`
- `TERMINAL_WORKSPACE.json`
- changed committed files preserving repository-relative paths.

Terminal ZIP:

`.aiassistant/reports/target/20260915_1702_aiscc-p3-3-public-live-l1-schema-repository-transaction-primitives-implementation-1.zip`

## final response

1. result classification
2. migration head before/after
3. schema/tables created
4. repository primitives implemented
5. constraint/index summary
6. fail-closed defaults
7. tests run/results
8. exact changed path count/list
9. commit hash/parent
10. builder/Replay invariant
11. terminal workspace
12. target bundle + ZIP
13. whether L2 is now eligible
