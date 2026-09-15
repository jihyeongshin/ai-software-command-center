# 작업지시서: P3-3 Public Live prerequisite design output generation policy-block retry

## meta

- task_id: `20260915_1630_aiscc-p3-3-public-live-prerequisite-design-output-generation-policy-block-retry-1`
- created_at: `2026-09-15T16:30:01+09:00`
- work_type: `DESIGN_REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`

## objective

Complete the unfinished 1600 Public Live prerequisite design freeze.

The prior attempt was not rejected on design substance. It stopped because design-artifact creation was blocked by the execution environment after an earlier oversized command failed.

This retry MUST create the required design outputs using safe, ordinary editor/file-patch operations with small independent writes.

Do not use one giant command containing all design documents.

## exact baseline

Before substantive work:

```text
branch = main
HEAD = 5e35ec0d60d84c7a05a2e58ebcc6560863879e5b
index = empty
tracked worktree = clean
```

Expected Git-visible untracked governance provenance is exactly:

- `.aiassistant/records/aiscc/cycles/20260915_1552_aiscc-p3-3-encoding-restoration-accepted-post-submit-live-readiness-entry-1.cycle.md`
  - SHA-256 `2e5946bf3ad1a0a02a387b5fdddaeb76972c9fd6c325f0a3b18e19eb85a04eb9`
- `.aiassistant/records/aiscc/cycles/20260915_1600_aiscc-p3-3-live-readiness-audit-accepted-prerequisite-design-entry-1.cycle.md`
  - SHA-256 `25ef427f1646c111eb6d9d63d1c51e8f1b30c6d5ba87a086ab22aa51be8beadf`
- `.aiassistant/reports/aiscc/20260915_1552_aiscc-browser-command-center-p3-3-public-bounded-live-readiness-entry-handoff-1.md`
  - SHA-256 `5304907558a67b3edb52c2fcb92fc0ea27fd230ef7648e28acdd05a93b4d4325`
- `.aiassistant/reports/aiscc/20260915_1552_aiscc-p3-3-encoding-restoration-final-browser-acceptance-1.md`
  - SHA-256 `c13e949649ba64cc8be20b9b64099b5ac55b7c1c911a3990b1d56d9f0cbb823a`
- `.aiassistant/reports/aiscc/20260915_1600_aiscc-browser-command-center-p3-3-live-prerequisite-security-design-entry-handoff-1.md`
  - SHA-256 `ed2e7fee3fbdb76651614b7f7f8e3ef0caaf7bd80a4c9e3c90489e16bda5b166`
- `.aiassistant/reports/aiscc/20260915_1600_aiscc-p3-3-live-readiness-audit-browser-acceptance-1.md`
  - SHA-256 `2ad58a1b3f4fdef7a1edd66f055307c38940412455c8aa02369bd7b077690e6d`
- `.aiassistant/tasks/done/20260915_1552_aiscc-p3-3-public-bounded-live-release-readiness-audit-and-minimal-design-freeze-1.md`
  - SHA-256 `ab9c880eb900044c6bfb1eea57518769a956c1d1eb119abaa5f2a362a2300132`

Also require the ignored predecessor active Task:

```text
.aiassistant/tasks/active/20260915_1600_aiscc-p3-3-public-live-admission-budget-identity-security-design-freeze-1.md
SHA-256 a69889677848becb557f5acd158d8e29a9e865b68ffd8c8f912b99bcbeaf6ae4
```

Any missing/extra/hash mismatch => STOP.

Do not clean/reset/delete accepted provenance.

After transport, this retry's Cycle/Judgment/Handoff are additional authorized governance residue and its Task is active/ignored.

## predecessor Task disposition

After baseline validation, move the exact predecessor active Task:

`.aiassistant/tasks/active/20260915_1600_aiscc-p3-3-public-live-admission-budget-identity-security-design-freeze-1.md`

to:

`.aiassistant/tasks/done/20260915_1600_aiscc-p3-3-public-live-admission-budget-identity-security-design-freeze-1.md`

Preserve bytes exactly.

This marks the incomplete attempt as ended with REWORK_REQUIRED; it does not mark its design accepted.

## mandatory validation

Run:

```text
python scripts/build_public_replay.py --check
```

PASS required.

No tests need to be executed unless needed only to inspect existing behavior; this remains a design task.

## source grounding

Reuse `SOURCE_INVENTORY.json` from the 1600 result conceptually, but re-open exact current source/canonical files needed to support every design assertion.

At minimum inspect the same authority/source areas from 1600:

- architecture/orchestration/security/runtime/provider rules;
- current state/decision/next actions;
- `src/aiscc/security/limits.py`;
- `src/aiscc/security/cancel.py`;
- `src/aiscc/persistence/repository.py`;
- `src/aiscc/api/app.py`;
- `src/aiscc/api/routes/**`;
- migrations/schema;
- relevant current tests.

Do not rely on memory when exact code can be read.

## frozen design scope

Design only for future:

```text
scenario:
stockroom-s1-normal / 1.0.0

free-form public input:
FORBIDDEN

repository URL/upload:
FORBIDDEN

public cancel:
DISABLED_IN_FIRST_SLICE

provider/model choice:
SERVER_OWNED
```

## required design contract

Complete the original 1600 contract for:

1. atomic public admission transaction;
2. durable idempotency;
3. trusted client/IP derivation + rate limiting;
4. USD reservation/day/campaign ledger;
5. durable global concurrency lease;
6. read capability / public run identity;
7. public HTTP routes and exact CORS;
8. additive DB schema/migrations;
9. truth-preserving failure state machine;
10. deterministic race/security tests;
11. dependency-ordered implementation sequence;
12. unresolved Human/release decisions.

The provider dispatch MUST NOT begin before durable admission commits.

Do not weaken the accepted Replay-only fallback.

## exact candidate caps

Use the accepted candidate unless the source-grounded design proves a change is required:

```text
scenario:
stockroom-s1-normal only

idempotency replay window:
10 minutes

per client/IP:
3 starts/hour
10 starts/day

global:
20 admitted/day
2 concurrent

per-run USD reserve:
0.20

daily app budget:
4.00 USD

competition/campaign app budget:
15.00 USD through 2026-10-17

provider paid calls:
<= 2/run

OpenAI project hard spend:
defense-in-depth only, not application-ledger substitute
```

Use integer money units, not float authority.

## target-only required outputs

Create all seven, separately:

1. `PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md`
2. `PUBLIC_LIVE_DB_SCHEMA_PLAN.md`
3. `PUBLIC_LIVE_HTTP_CONTRACT.md`
4. `PUBLIC_LIVE_FAILURE_STATE_MACHINE.md`
5. `PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
6. `PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
7. `PUBLIC_LIVE_OPEN_DECISIONS.md`

Also create:

- `SOURCE_INVENTORY.json`
- `VALIDATION.json`
- normal `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `WORKSPACE_TERMINAL.json`

Target:

`.aiassistant/reports/target/20260915_1630_aiscc-p3-3-public-live-prerequisite-design-output-generation-policy-block-retry-1/`

Terminal ZIP:

`.aiassistant/reports/target/20260915_1630_aiscc-p3-3-public-live-prerequisite-design-output-generation-policy-block-retry-1.zip`

## output-writing method

The seven design files are explicitly authorized target/export-only artifacts.

Preferred behavior:

- use the Executor's ordinary patch/editor/file-edit mechanism;
- create one file at a time;
- keep each write reasonably sized;
- if needed, build a long document in multiple normal patch/edit chunks;
- validate UTF-8 after each file.

Do NOT:

- invoke a single oversized shell command carrying all document bodies;
- encode content to evade tool policy;
- use base64/obfuscation to bypass controls;
- modify tool/approval policy;
- retry through unsafe alternate mechanisms after an explicit policy denial.

If an ordinary editor/patch operation for these authorized target-only paths is explicitly blocked by platform policy, STOP:

`DESIGN_OUTPUT_POLICY_BLOCK_PERSISTENT`

and report the exact blocked operation category without attempting a bypass.

## design quality requirements

### admission transaction

Freeze exact transaction ordering, locks/constraints and atomicity for:

```text
scenario allowlist
payload bounds
trusted client bucket
hour/day rate
global daily count
global concurrency
USD hold
idempotency
run/read capability creation
dispatch eligibility marker
```

Handle multi-worker/multi-replica races, crashes and retries.

### idempotency

Define:

- format/entropy/length;
- caller binding;
- payload hash;
- same-key/same-payload;
- same-key/different-payload;
- 10-minute replay;
- tombstone retention;
- dispatch marker;
- ambiguous-send semantics;
- uniqueness constraints.

### identity/rate

Define:

- trusted proxy contract;
- forwarding header rules;
- spoof handling;
- IPv4/IPv6 normalization;
- pseudonymous/HMAC bucket;
- NAT limitations;
- fail-closed behavior if trustworthy origin IP unavailable.

Do not invent Railway edge behavior not proven by repository evidence; keep it as a release prerequisite.

### money/concurrency

Define exact integer ledger/lease state machine and conservation invariants.

No double release, negative budget, oversubscription or in-memory authoritative semaphore.

### HTTP/CORS

At minimum design:

```text
POST /v1/public-live/runs
GET /v1/public-live/runs/{run_id}
```

No cancel route first slice.

Exact frontend origin:

`https://aiscc-replay.pages.dev`

No wildcard origin and no credential cookies.

CORS is not authentication.

### DB

Prefer separate public Live DB/credentials unless current source proves safe owner sharing.

Specify additive tables, keys, indexes, isolation/locking, expiry/cleanup and migration sequence.

### failures

Define truth for:

- pre-admission reject;
- admitted-not-dispatched;
- dispatched outcome unknown;
- provider explicit failure;
- DB failure;
- budget/capacity/rate reject;
- process crash/restart.

Never convert failed Live work into successful Replay evidence.

### tests

Freeze deterministic tests for race/idempotency/rate/budget/concurrency/proxy/CORS/capability/restart/Replay-independence.

### implementation sequence

Provide small dependency-ordered future Tasks.

No implementation occurs now.

## required terminal classification

Exactly one:

```text
LIVE_PREREQUISITE_DESIGN_CANDIDATE / HUMAN_ACCEPTANCE_PENDING
```

or

```text
LIVE_PREREQUISITE_DESIGN_REWORK_REQUIRED
```

or

```text
REPLAY_ONLY_RETAIN / LIVE_PREREQUISITE_NOT_JUSTIFIED
```

`DESIGN_OUTPUT_POLICY_BLOCK_PERSISTENT` is allowed only for an actual repeated platform policy blocker.

## repository boundary

No tracked product/canonical source modification.

No Git index modification.

No commit.

No network/provider/DB/Docker/deployment/UI/Wanted action.

At terminal, report exact governance residue. Do not clean it.

## evidence contract

executor_required:

- current-source grounding;
- all seven design artifacts;
- validation of internal consistency;
- exact implementation sequence;
- open decision list.

reuse_allowed:

- accepted 1552 audit;
- 1600 source observations where current bytes still match;
- accepted Replay/submission evidence.

human_owned:

- design acceptance;
- whether to continue before deadline;
- paid resource/provider/deployment decisions.

forbidden:

- policy bypass;
- implementation;
- migration creation;
- provider call;
- deploy/redeploy;
- commit/push.

proof_non_substitution:

- source inventory != design;
- design != implementation;
- CORS != authentication;
- provider hard limit != app ledger;
- static Replay acceptance != Live release safety.

## final response

1. result classification
2. output generation method/result
3. admission transaction summary
4. schema/constraint summary
5. idempotency/identity/rate contract
6. USD/concurrency invariants
7. HTTP/CORS contract
8. failure semantics
9. implementation sequence
10. open Human decisions
11. terminal workspace
12. target bundle + ZIP
