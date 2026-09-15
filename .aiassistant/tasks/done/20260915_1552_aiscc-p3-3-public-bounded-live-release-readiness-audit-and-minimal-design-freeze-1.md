# 작업지시서: P3-3 Public Bounded Live release-readiness audit and minimal design freeze

## meta

- task_id: `20260915_1552_aiscc-p3-3-public-bounded-live-release-readiness-audit-and-minimal-design-freeze-1`
- created_at: `2026-09-15T15:52:21+09:00`
- work_type: `DESIGN_AUDIT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`
- primary_semantic_owner: `P3-3 Public Bounded Live release readiness`

## objective

Determine whether the current repository can safely support the smallest useful `PUBLIC_BOUNDED_LIVE` competition slice before the 2026-09-20 edit freeze.

This Task is an audit/design-freeze candidate only.

It MUST NOT:

- implement product source;
- call OpenAI;
- create/configure provider credentials;
- create Railway resources;
- deploy/redeploy Cloudflare or Railway;
- modify the submitted public Replay;
- modify the Wanted submission;
- commit/push.

## exact baseline

Require before substantive audit:

```text
branch = main
HEAD = 5e35ec0d60d84c7a05a2e58ebcc6560863879e5b
index = empty
tracked worktree = clean
Git-visible untracked = 0
```

Run:

```text
python scripts/build_public_replay.py --check
```

PASS required.

If baseline fails, STOP without cleanup/reset.

## accepted public baseline

```text
Production Replay:
https://aiscc-replay.pages.dev

Public Replay:
DEPLOYED / PUBLIC_VERIFICATION_PASSED / HUMAN_ACCEPTED

Competition submission:
COMPLETED

P3-3:
SUBMITTED / POST_SUBMISSION_IMPROVEMENT_WINDOW

Public Bounded Live:
NOT_RELEASED
```

Live is optional. A failed Live audit MUST preserve Replay-only release.

## must-read repository authority

Read the current repository canonical versions of at least:

- product thesis;
- architecture;
- orchestration;
- security/sandbox rules;
- provider/tool execution rules;
- current state summary;
- decision register;
- next actions;
- P2-3 canonical scenario/Replay records;
- P3-3 public runtime/release records;
- current submission confirmation.

Do not rely on Browser Project mirrors when repository canonical files are newer.

## source implementation audit

Locate and enumerate concrete current implementation for:

### P1-3 security/runtime safeguards

Find actual code/tests for:

- `RuntimeMode` / public permission profile;
- action/state eligibility;
- scenario/resource capability;
- public tool/command allowlist;
- arbitrary network deny;
- secret handle/non-exposure;
- filesystem/worktree isolation;
- process limits/timeout/cancel;
- idempotency;
- abuse/throttle;
- application budget reservation/charge/release;
- public cancel target authorization;
- fail-closed behavior;
- restart/recovery.

For each item classify:

```text
IMPLEMENTED_VERIFIED
IMPLEMENTED_NEEDS_RELEASE_REVERIFY
PARTIAL
MISSING
NOT_APPLICABLE_TO_MINIMAL_LIVE
```

Cite exact source/test paths and symbols.

### P1-5 provider/tool runtime

Audit:

- current OpenAI adapter;
- Responses API request shape;
- server-owned model/provider selection;
- structured output/function/tool use;
- execution loop;
- call/retry/deadline counters;
- provider failure classification;
- usage/token capture;
- evidence handoff;
- provider credential boundary;
- no direct authoritative state mutation by provider output.

### P2-3 public-safe synthetic material

Identify:

- exact synthetic repository/version;
- exact four canonical scenarios;
- which scenarios can safely execute live with current runtime;
- which scenario requires Human-owned evidence and therefore cannot truthfully auto-complete;
- whether any live execution would access non-public source/data.

## minimal Live product question

Do NOT assume all four scenarios must be live.

Select the smallest release slice that materially demonstrates AISCC mechanism while minimizing security/cost/deadline risk.

Evaluate at minimum:

### Candidate A

```text
one allowlisted normal scenario only
```

### Candidate B

```text
normal + one non-success governance scenario
```

### Candidate C

```text
all four canonical scenarios
```

Recommend exactly one, or recommend `REPLAY_ONLY_RETAIN`.

The decision must consider:

- implementation reuse;
- runtime/security complexity;
- Human gate semantics;
- cost;
- QA surface;
- remaining deadline time;
- value beyond existing Replay.

## public API/UI boundary

Design the minimal public contract without implementing it.

Required invariants:

```text
no free-form prompt/task
no repository URL
no upload
no arbitrary command
no arbitrary network destination
no user-provided provider/model/key
```

Preferred frontend/backend split unless repository evidence makes it unsafe:

```text
Cloudflare Pages static UI
→ exact Railway public API origin
→ strict origin allowlist for https://aiscc-replay.pages.dev
→ no credential-bearing browser session
```

Design:

- start-live request;
- status/result read;
- cancel if safely supported;
- idempotency key;
- opaque run identifier;
- separate run-control authorization token/capability if cancel is supported;
- truthful error schema;
- no internal stack/path/provider payload exposure.

Do not use a visible/guessable run ID alone as cancel authority.

If cross-origin/session design cannot meet the accepted security boundary without significant new infrastructure, recommend Replay-only rather than weakening controls.

## candidate provider release envelope

Browser currently proposes the following **candidate**, not yet accepted configuration.

Audit whether the existing runtime can enforce it mechanically.

```text
provider:
OpenAI

API:
Responses API

model:
gpt-5.6-terra

reasoning effort:
low

max provider calls per Live run:
2 total

provider retries:
at most 1 and included inside the 2-call total

max input tokens per provider request:
16,000

max output tokens per provider request:
3,000

max Live wall-clock:
90 seconds

max concurrent public Live runs:
2

per-run application cost reservation:
USD 0.20

daily admitted Live runs:
20 max

daily application spend:
USD 4.00 max

competition Live application budget:
USD 15.00 max through 2026-10-17

OpenAI project hard spend limit candidate:
USD 20.00 / month
```

Current Browser-verified GPT-5.6 Terra pricing input:

```text
input:
USD 2.00 / 1M tokens

cached input:
USD 0.20 / 1M tokens

output:
USD 12.00 / 1M tokens
```

Show the conservative worst-case token-cost calculation for the candidate call/token bounds.

Do not assume the provider hard spend setting exists merely from old project docs; Browser has reverified current official API support, but actual account configuration remains Human/deployment evidence.

If the repository budget ledger cannot enforce a conservative pre-call reservation from these bounds, classify release as blocked.

## abuse/idempotency candidate

Design, do not implement.

At minimum evaluate:

```text
idempotency window:
10 minutes

per client/IP start rate:
3/hour

per client/IP daily:
10/day

global concurrent:
2

global daily:
20
```

Do not treat browser-supplied session/client ID as trustworthy by itself.

Document the exact server-side identity/rate strategy feasible on Railway behind its edge.

If reliable client-IP derivation behind Railway proxy requires an explicit trusted-proxy contract not present in the code, mark it as a release prerequisite.

## Railway release boundary

Accepted provider direction:

```text
plan:
Hobby

region:
Singapore

region identifier:
asia-southeast1-eqsg3a
```

Audit the repository for:

- deployable API process;
- Dockerfile/Railpack suitability;
- health endpoint;
- PostgreSQL requirement/migrations;
- start command;
- required environment variable names only;
- secret storage boundary;
- CORS/origin policy;
- persistent DB dependency;
- migration safety;
- log sanitization.

Do not print secret values.

Do not create Railway project/service/database.

## OpenAI project boundary

Design required Human deployment steps, but do not perform them.

At minimum:

- separate API Project;
- model allowlist to chosen exact model;
- project rate limits where useful;
- hard project spend limit candidate;
- restricted project-scoped API key/service account;
- secret stored only in Railway environment;
- no API key in browser/Cloudflare static files/repository;
- no provider model selection from request.

## failure-domain proof plan

Freeze exact tests that implementation/release must pass.

Required categories:

1. Replay works with Live API completely down.
2. Replay works when OpenAI key missing.
3. Replay works when budget exhausted.
4. Live admission denies unknown scenario.
5. Live admission denies free-form input.
6. duplicate idempotency key does not create duplicate paid run.
7. concurrency cannot overspend budget.
8. provider timeout/rate-limit produces Live failure, not ACCEPTED Replay.
9. secret canary never appears in output/log/Replay.
10. arbitrary network/tool request denied.
11. cancel authorization cannot target another run.
12. restart preserves/reconciles budget/run truth.
13. exact public origin/CORS behavior.
14. output contains no host paths/internal stack/provider raw secrets.
15. Live failure leaves Recorded Replay available.

Classify which existing tests can be reused and which new tests are required.

## frontend change boundary

Audit the existing `public/replay/**` static surface and propose the smallest later modification.

Preferred concept:

- keep current Replay landing/catalog unchanged by default;
- add clearly separate `Live Demo (Beta)` area only after backend release gate passes;
- preserve explicit `Recorded Run Replay` labels;
- before Live is enabled, retain current `Live Demo is not enabled` truth;
- no hidden live call on page load/refresh;
- live start must require explicit Human click.

Do not edit any static files in this Task.

## current official provider facts supplied by Browser

Use these as current verified external facts for this audit; do not independently web-browse unless repository policy explicitly permits and requires it.

### OpenAI

As reverified 2026-09-15 from official OpenAI documentation:

- `gpt-5.6-terra` exists;
- Responses API supported;
- function calling and structured outputs supported;
- current price: $2/M input, $0.20/M cached input, $12/M output;
- project model permissions/rate limits supported;
- project-level hard spend limit supported.

### Railway

As reverified 2026-09-15 from official Railway docs:

- Hobby base price $5/month;
- Southeast Asia region is Singapore;
- region id `asia-southeast1-eqsg3a`;
- Hobby is not subject to the Free-tier peak-hour deploy restriction.

These facts support design only.
They are NOT actual deployment/configuration evidence.

## required output artifacts

Create in target export only:

- `PUBLIC_BOUNDED_LIVE_READINESS_AUDIT.md`
- `PUBLIC_BOUNDED_LIVE_MINIMAL_RELEASE_DESIGN.md`
- `PUBLIC_BOUNDED_LIVE_CHANGE_PLAN.json`
- `PUBLIC_BOUNDED_LIVE_CAPS_CANDIDATE.json`
- `PUBLIC_BOUNDED_LIVE_SECURITY_GAP_MATRIX.json`
- `PUBLIC_BOUNDED_LIVE_TEST_PLAN.md`
- `PUBLIC_BOUNDED_LIVE_DEPLOYMENT_PREREQUISITES.md`
- `SOURCE_INVENTORY.json`
- `VALIDATION.json`

No new canonical design file in repository yet.

## outcome classification

Return exactly one:

### Ready candidate

```text
LIVE_IMPLEMENTATION_READY / HUMAN_ACCEPTANCE_PENDING
```

Only if no unbounded/MISSING security primitive blocks the minimal slice.

### Retain Replay

```text
REPLAY_ONLY_RETAIN / BLOCKED_PREREQUISITE
```

Use when required isolation/budget/secret/idempotency/runtime controls cannot be safely reused before deadline.

### Rework design

```text
LIVE_DESIGN_REWORK_REQUIRED
```

Use for resolvable design gaps that need another design pass.

## repository terminal state

This Task must not mutate tracked product/governance state except inbound Task/Cycle/Judgment/Handoff transport.

No Git commit.

At terminal:

- no tracked source modification;
- no index mutation;
- no provider/deployment/network mutation;
- record exact Git-visible governance transport residue rather than cleaning it.

## evidence contract

executor_required:

- current source/symbol/test audit;
- exact implementation-vs-gap matrix;
- conservative cost calculation;
- deployment prerequisite inventory;
- minimal release design;
- test/release gate plan.

reuse_allowed:

- accepted P1-3/P1-5/P2-3 provenance when exact current source still matches;
- current static Replay acceptance;
- Browser-supplied current provider facts.

human_owned:

- acceptance of exact Live design;
- exact paid-resource/account creation;
- API project/key configuration;
- spend-limit configuration;
- Railway resource creation;
- public release decision.

forbidden:

- source implementation;
- external provider call;
- credentials;
- deploy/redeploy;
- public UI change;
- competition form edit;
- commit/push.

proof_non_substitution:

- existing unit test != release-environment security proof;
- provider documentation != configured hard spend evidence;
- architecture rule != implemented guard;
- Recorded Replay success != Live safety;
- local implementation != public release authorization.

## export

Target:

`.aiassistant/reports/target/20260915_1552_aiscc-p3-3-public-bounded-live-release-readiness-audit-and-minimal-design-freeze-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- required output artifacts listed above.

Terminal ZIP:

`.aiassistant/reports/target/20260915_1552_aiscc-p3-3-public-bounded-live-release-readiness-audit-and-minimal-design-freeze-1.zip`

## final response

1. result classification
2. minimal scenario scope recommendation
3. reusable security/runtime primitives
4. blocking gaps
5. exact source paths/symbols
6. candidate cost/budget calculation
7. Railway deployment readiness
8. OpenAI project prerequisites
9. required new tests
10. tracked workspace status
11. target bundle + ZIP
12. Human decision required
