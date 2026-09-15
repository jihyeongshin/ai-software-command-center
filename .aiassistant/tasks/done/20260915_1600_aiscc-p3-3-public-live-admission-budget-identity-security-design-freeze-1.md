# 작업지시서: P3-3 Public Live admission/budget/identity security design freeze

## meta

- task_id: `20260915_1600_aiscc-p3-3-public-live-admission-budget-identity-security-design-freeze-1`
- created_at: `2026-09-15T16:00:00+09:00`
- work_type: `DESIGN`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`
- primary_semantic_owner: `P3-3 Public Live admission security`

## objective

Freeze the exact design contract needed to close the first Public Bounded Live blocker cluster:

```text
public admission
durable idempotency
trusted client identity / rate limiting
USD reservation + charge + release
global concurrency lease
public-only HTTP API / CORS
```

This Task is DESIGN ONLY.

Do not implement source, migration, API routes, provider profile, frontend, deployment or paid resources.

## repository baseline

Before substantive work require:

```text
branch = main
HEAD = 5e35ec0d60d84c7a05a2e58ebcc6560863879e5b
index = empty
tracked worktree = clean
```

Expected pre-existing Git-visible governance provenance is exactly:

- `.aiassistant/records/aiscc/cycles/20260915_1552_aiscc-p3-3-encoding-restoration-accepted-post-submit-live-readiness-entry-1.cycle.md`
  - SHA-256 `2e5946bf3ad1a0a02a387b5fdddaeb76972c9fd6c325f0a3b18e19eb85a04eb9`
- `.aiassistant/reports/aiscc/20260915_1552_aiscc-browser-command-center-p3-3-public-bounded-live-readiness-entry-handoff-1.md`
  - SHA-256 `5304907558a67b3edb52c2fcb92fc0ea27fd230ef7648e28acdd05a93b4d4325`
- `.aiassistant/reports/aiscc/20260915_1552_aiscc-p3-3-encoding-restoration-final-browser-acceptance-1.md`
  - SHA-256 `c13e949649ba64cc8be20b9b64099b5ac55b7c1c911a3990b1d56d9f0cbb823a`
- `.aiassistant/tasks/done/20260915_1552_aiscc-p3-3-public-bounded-live-release-readiness-audit-and-minimal-design-freeze-1.md`
  - SHA-256 `ab9c880eb900044c6bfb1eea57518769a956c1d1eb119abaa5f2a362a2300132`

After this delivery, current Cycle/Judgment/Handoff are additional authorized provenance and active Task follows normal ignored-task lifecycle.

Any extra unexplained dirt or hash mismatch => STOP.

Do not clean/reset/delete accepted provenance.

Run:

```text
python scripts/build_public_replay.py --check
```

PASS required.

## must-read exact authority

Read current repository canonical versions of:

- `.aiassistant/rules/AISCC_ARCHITECTURE.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`
- `.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`

Read current implementation relevant to:

- `src/aiscc/security/limits.py`
- `src/aiscc/security/cancel.py`
- `src/aiscc/persistence/repository.py`
- `src/aiscc/api/app.py`
- `src/aiscc/api/routes/**`
- current migrations/schema
- corresponding unit/integration/runtime security tests.

Reuse the accepted 1552 audit evidence, but verify exact source when deriving a new contract.

## frozen Live scope for this design

Design ONLY for the future smallest candidate:

```text
scenario_id:
stockroom-s1-normal

scenario_version:
1.0.0

public free-form input:
FORBIDDEN

repository URL/upload:
FORBIDDEN

public cancel:
DISABLED_IN_FIRST_SLICE

public provider/model choice:
FORBIDDEN
```

Do not design all four scenarios.

## exact admission invariant

Design one authoritative server-side transaction boundary such that a paid dispatch is eligible IFF all of the following are true:

```text
scenario exact-allowlisted
request schema valid and bounded
trusted client bucket derived
hourly/day client rate available
global day count available
global concurrency lease available
campaign/day USD reserve available
idempotency key admissible
same-key payload identity consistent
run row/capabilities durably issued
admission state committed
```

No provider dispatch may start before this transaction commits.

Define exact ordering and DB constraints/locks that prevent overspend/duplicate dispatch across:

- multiple HTTP workers;
- multiple Railway replicas;
- process crash;
- retry;
- network disconnect;
- transaction retry;
- delayed provider result.

## durable public idempotency contract

Freeze:

- key format/entropy/length bounds;
- 10-minute request replay window;
- payload fingerprint construction;
- caller scope binding;
- same key + same payload behavior;
- same key + different payload conflict;
- expiry;
- tombstone retention after expiry;
- crash/restart behavior;
- dispatch-start marker;
- ambiguous send handling;
- uniqueness constraints.

A browser-generated client ID alone MUST NOT be authority.

An idempotency key MUST NOT be treated as run-read/cancel authority.

## trusted client identity / rate limiting

Freeze a practical server-owned strategy for Railway.

Candidate caps from accepted audit:

```text
per client/IP start:
3/hour

per client/IP:
10/day

global admitted:
20/day

global concurrent:
2
```

Design:

- trusted proxy assumption;
- exact accepted forwarding header(s);
- trusted-hop count or overwrite contract;
- spoofed header handling;
- IPv4/IPv6 normalization;
- HMAC/pseudonymous stored bucket;
- retention;
- NAT/shared-IP consequences;
- failure if trusted proxy identity unavailable;
- whether Cloudflare frontend origin changes client-IP visibility.

If Railway current edge semantics cannot be proven from repository evidence alone, mark exact deployment verification as a Human/release prerequisite rather than inventing it.

## USD ledger design

Use integer micro-USD or an equally exact integer representation.

Candidate bounds:

```text
per-run pre-admission reserve:
USD 0.20

daily application spend:
USD 4.00

campaign application budget:
USD 15.00 through 2026-10-17

provider paid calls:
<= 2/run
```

Freeze tables/columns/state machine for:

- reserve;
- dispatch commitment;
- provisional usage;
- terminal settlement;
- unused release;
- ambiguous provider outcome;
- provider missing usage;
- restart recovery;
- UTC daily rollover;
- campaign lifetime;
- cross-month behavior.

The monthly provider hard limit MUST remain defense-in-depth and MUST NOT replace the application campaign ledger.

Define exact conservation invariants, e.g.:

```text
available + held + settled == configured_budget
```

or a stronger schema-appropriate equivalent.

No negative balance, double release or oversubscription is permissible.

## concurrency lease design

Freeze:

- lease row/key;
- acquisition under same admission transaction;
- max global 2;
- expiry semantics;
- heartbeat if any;
- process crash;
- stale lease reconciliation;
- provider send already happened but process died;
- release ordering;
- relationship to budget hold.

Do not use in-memory semaphores as authoritative global concurrency.

## public run capabilities

First slice has NO public cancel.

Design two separate public concepts:

1. opaque display/run identifier;
2. read capability.

Requirements:

- run ID not sufficient to read status if that would expose cross-user data;
- read capability is high entropy;
- never in URL query if avoidable;
- stored hashed server-side where feasible;
- not logged;
- not a provider credential;
- browser stores only as long as necessary;
- exact expiration/recovery UX.

If status can be safely public solely because result contains no user-specific input and scenario is fixed, explicitly compare that alternative and choose one.

## public HTTP contract

Design exact future routes, but do not implement.

At minimum consider:

```text
POST /v1/public-live/runs
GET /v1/public-live/runs/{run_id}
```

Cancel route absent.

Freeze:

- request schema;
- max body size;
- response schema;
- error codes;
- HTTP statuses;
- idempotency header;
- read capability header if selected;
- no raw stack/provider body/path;
- retryable semantics.

## strict origin/CORS

Design exact browser policy for:

`https://aiscc-replay.pages.dev`

At minimum:

- exact allow-origin;
- no wildcard;
- credentials false;
- allowed methods;
- allowed headers;
- preflight behavior;
- `Vary: Origin`;
- unexpected Origin rejection;
- requests with no Origin;
- non-browser callers.

Explicitly state that CORS is NOT authentication or abuse prevention.

## database schema / migration plan

Design additive schema only.

Produce table/index/constraint plan for:

- public admission/idempotency;
- client rate buckets;
- global/day counters if stored separately;
- campaign/day USD ledger;
- global concurrency leases;
- public run/read capability identity if required.

Specify:

- PK/unique keys;
- transaction isolation/row locking;
- timestamps/timezone;
- integer money units;
- expiry indexes;
- migration ordering;
- rollback strategy;
- compatibility with currently running owner DB.

Decide whether public Live SHOULD use a separate database from owner runtime.

Default preference: separate public Live DB/credentials unless strong evidence supports safe sharing.

## failure semantics

Design exact truth-preserving outcomes:

- rejected before admission;
- admitted but not dispatched;
- dispatch started, provider result unknown;
- provider explicit failure;
- process restart;
- DB unavailable;
- budget unavailable;
- capacity unavailable;
- rate limited.

No condition may transform Live failure into an ACCEPTED Recorded Replay.

Replay remains independently available.

## implementation work breakdown

Produce a dependency-ordered implementation plan with small Task boundaries.

At minimum separate:

1. schema/repository primitives;
2. admission service;
3. public API composition;
4. provider real-profile prerequisite;
5. deployment packaging/trusted proxy proof;
6. runtime/adversarial tests;
7. frontend Live enablement.

Identify which Tasks can be parallel and which cannot.

## exact tests to freeze

Design deterministic tests for:

- same idempotency same payload;
- same key different payload;
- key expiry/tombstone;
- two-worker duplicate race;
- 3/hour fourth deny;
- 10/day eleventh deny;
- 20/day twenty-first deny;
- global concurrency third deny;
- concurrent $0.20 reservations at budget boundary;
- crash after reserve;
- crash after dispatch marker;
- unknown provider outcome;
- double-settlement;
- UTC rollover;
- campaign exhaustion;
- spoofed forwarding header;
- IPv6 normalization;
- absent trusted proxy identity;
- cross-run read capability denial;
- unexpected/no Origin;
- DB unavailable;
- Replay independence.

No tests are executed in this Task.

## design decision outputs

Create target-export-only:

- `PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md`
- `PUBLIC_LIVE_DB_SCHEMA_PLAN.md`
- `PUBLIC_LIVE_HTTP_CONTRACT.md`
- `PUBLIC_LIVE_FAILURE_STATE_MACHINE.md`
- `PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
- `PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
- `PUBLIC_LIVE_OPEN_DECISIONS.md`
- `SOURCE_INVENTORY.json`
- `VALIDATION.json`

No canonical design file is promoted yet.

## required classification

Return exactly one:

### acceptable design candidate

```text
LIVE_PREREQUISITE_DESIGN_CANDIDATE / HUMAN_ACCEPTANCE_PENDING
```

### unresolved design

```text
LIVE_PREREQUISITE_DESIGN_REWORK_REQUIRED
```

### cannot justify before deadline

```text
REPLAY_ONLY_RETAIN / LIVE_PREREQUISITE_NOT_JUSTIFIED
```

## terminal repository boundary

No product/tracked canonical modification.

No commit.

No network/provider/DB/Docker/deployment action.

Preserve exact governance transport residue and report it.

## evidence contract

executor_required:

- exact current-source grounding;
- transaction/constraint design;
- failure state machine;
- public HTTP/CORS contract;
- database/migration plan;
- deterministic race/security test matrix;
- dependency-ordered implementation sequence.

reuse_allowed:

- accepted 1552 audit;
- accepted P1 security/runtime/provider designs where current source matches;
- accepted public Replay/submission evidence.

human_owned:

- design acceptance;
- whether to continue Live work before deadline;
- paid resources/provider configuration;
- deployment.

forbidden:

- implementation;
- migration creation;
- network/provider call;
- deployment;
- UI edit;
- commit/push;
- Wanted edit.

proof_non_substitution:

- design != implementation;
- local DB constraints != deployed proxy identity proof;
- CORS != authentication;
- provider hard limit != app campaign ledger;
- static Replay acceptance != Live release safety.

## export

Target:

`.aiassistant/reports/target/20260915_1600_aiscc-p3-3-public-live-admission-budget-identity-security-design-freeze-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- all required design outputs.

Terminal ZIP:

`.aiassistant/reports/target/20260915_1600_aiscc-p3-3-public-live-admission-budget-identity-security-design-freeze-1.zip`

## final response

1. result classification
2. exact chosen admission transaction
3. schema/constraint summary
4. idempotency contract
5. rate/client identity contract
6. USD ledger/concurrency invariants
7. HTTP/CORS contract
8. failure-state summary
9. implementation sequence
10. open Human decisions
11. repository terminal state
12. target bundle + ZIP
