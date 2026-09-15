# 작업지시서: P3-3 public Recorded Replay static surface and Cloudflare Pages prerequisite implementation

## meta

- task_id: `20260915_1047_aiscc-p3-3-public-recorded-replay-static-surface-and-cloudflare-pages-prerequisite-implementation-1`
- created_at: `2026-09-15T10:47:25+09:00`
- work_type: `IMPLEMENTATION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`
- primary_semantic_owner: `P3-3 public Recorded Replay release prerequisite / Browser Command Center`

## current authority

```text
P3-3:
ACTIVE / BLOCKED_RELEASE_PREREQUISITE

branch:
main

HEAD:
17fcd337a8bc1410e230a7c18195ac3d3006b417

Recorded Replay corpus:
CANONICAL / PERSISTED

Public Replay deployment:
NOT_COMPLETED

Public Bounded Live:
NOT_RELEASED
```

Accepted deployment direction:

```text
decision id:
AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1

Recorded Replay / public UI:
Cloudflare Pages

optional bounded Live API/PostgreSQL:
Railway Hobby / Singapore

optional Live LLM:
separate OpenAI API Project
```

This direction is already Human-accepted but `NOT_EXECUTED`.

Do not reopen host/provider selection.

## predecessor workspace identity

Before inbound transport, current expected Git-visible untracked set is exactly these 8 files:

- `.aiassistant/records/aiscc/cycles/20260915_1009_aiscc-p3-2-final-persistence-acceptance-p3-3-entry-authorization-1.cycle.md`
  - SHA-256 `5c54ad4d48759de1034fd1f584df08ac32bad674d0f3676fa73bf7cc5a0b65f1`
- `.aiassistant/reports/aiscc/20260915_1009_aiscc-browser-command-center-p3-2-closed-p3-3-release-submission-entry-handoff-1.md`
  - SHA-256 `2381e5415d08e49552cb782c53eab23be0a0241441ba74895f8f05588e90b591`
- `.aiassistant/reports/aiscc/20260915_1009_aiscc-p3-2-final-persistence-browser-acceptance-1.md`
  - SHA-256 `bf26ac731e95ab6cf8c0da8246b3b8b8e3e4e810adc131b231e533c8d0934ebc`
- `.aiassistant/reports/aiscc/AISCC_COMPETITION_SUBMISSION_PACKAGE.md`
  - SHA-256 `2b0fc969c1271e345fc85859b0108f756d994a70ee82972b89352bcefc419664`
- `.aiassistant/reports/aiscc/AISCC_P3_3_PUBLIC_RELEASE_READINESS.md`
  - SHA-256 `2420037bf702a6403774a5fac6204956ee0e960285892168701606c5c5e6419e`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_DISCLOSURE_REGISTER.md`
  - SHA-256 `e9df845451b198ee983cf4f52ed89cf6c41cefee33d497b1fb6f4ec30d65eafa`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_MANIFEST_CANDIDATE.json`
  - SHA-256 `f0f4c37b0748b20d3a69bad784b72d7d38d216fb77f5708d5b2ea8a2c9423305`
- `.aiassistant/tasks/done/20260915_1009_aiscc-p3-3-replay-first-public-release-readiness-and-submission-package-freeze-1.md`
  - SHA-256 `e366225623a2e749693f6cc023a97d71a74be5de7e6943248a6e82e55a00585c`

Required tracked/index baseline before substantive mutation:

```text
HEAD = 17fcd337a8bc1410e230a7c18195ac3d3006b417
branch = main
index = empty
tracked worktree = clean
```

After this delivery, the supplied Cycle/Judgment/Handoff are additionally authorized untracked governance artifacts and the active Task is ignored according to project policy.

If predecessor identity differs, STOP without cleanup.

## objective

Implement the smallest truthful, zero-inference public Recorded Replay surface that can be deployed as a static Cloudflare Pages site.

The implementation must close technical blockers R01/R02 while keeping Live disabled and owner/private runtime isolated.

This Task performs implementation + local verification only.

Actual public deployment is forbidden.

## architecture invariant

The public Replay site is a standalone static artifact.

It SHALL NOT depend on:

- PostgreSQL;
- `AISCC_DATABASE_URL`;
- the owner/private Command Center API;
- FastAPI at request time;
- OpenAI/provider inference;
- provider keys;
- Railway;
- a writable backend;
- external repository URLs/uploads;
- shell/network execution;
- user-provided task execution.

Page viewing must generate zero LLM/provider calls by construction.

## exact source corpus

Source of truth:

`.aiassistant/reports/aiscc/replay/stockroom/v1/`

Required source files:

- `REPLAY_CORPUS_INDEX.json`
- `stockroom-s1-normal.json`
- `stockroom-s2-missing-evidence.json`
- `stockroom-s3-policy-conflict.json`
- `stockroom-s4-human-owned-claim.json`

Accepted corpus root:

`a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e`

Source member hashes/sizes MUST be verified against the canonical index before generating public output.

The public data copies must be byte-identical to source.

Do not transform, summarize, redact again, or regenerate recorded run bodies in this Task.

If any accepted source hash/size conflicts, STOP `CORPUS_IDENTITY_CONFLICT`.

## required repository shape

Create:

```text
scripts/build_public_replay.py

public/replay/
  index.html
  404.html
  assets/
    app.js
    styles.css
  data/
    REPLAY_CORPUS_INDEX.json
    stockroom-s1-normal.json
    stockroom-s2-missing-evidence.json
    stockroom-s3-policy-conflict.json
    stockroom-s4-human-owned-claim.json
  _headers
  health.json
  PUBLIC_REPLAY_BUILD_MANIFEST.json

docs/AISCC_PUBLIC_REPLAY_DEPLOYMENT.md
```

You may add narrowly scoped tests under the repository's existing test convention if needed.

Do not add a third-party frontend framework or package manager solely for this surface.

Prefer plain HTML/CSS/JS and Python standard library generation/validation.

## build generator contract

`scripts/build_public_replay.py` MUST:

1. resolve repository root deterministically;
2. read only the exact canonical corpus directory and static source/templates defined by this implementation;
3. validate index/member identity before copy;
4. copy all five JSON files byte-for-byte into `public/replay/data/`;
5. generate/verify static shell assets;
6. generate `health.json`;
7. generate `PUBLIC_REPLAY_BUILD_MANIFEST.json`;
8. support a write/build mode;
9. support a check mode that exits non-zero on drift;
10. require no network and no secret/env value;
11. produce deterministic output for identical repository bytes.

Do not include current wall-clock timestamps in generated files if they would make identical-source builds non-deterministic.

`PUBLIC_REPLAY_BUILD_MANIFEST.json` MUST include at least:

```text
schema/version
mode = RECORDED_RUN_REPLAY
live = false
source_commit
canonical_corpus_root_sha256
source index path/hash
each source member path/hash/bytes
each public copied member path/hash/bytes
static asset hashes
health file hash
owner_db_dependency = false
provider_dependency = false
secret_dependency = false
```

Source commit should be the implementation's pre-commit source baseline plus an explicit note that the final deployment commit will be filled/verified by the later persistence/deployment step if self-reference would make deterministic generation impossible. Do not fabricate a future Git SHA.

## public UX contract

`public/replay/index.html` must be understandable without internal AISCC workflow knowledge.

Required visible elements:

### landing header

- `AI Software Command Center`
- prominent `Recorded Run Replay` label
- explicit copy equivalent to:

`This is a recorded historical run. Viewing it does not execute AI.`

- explicit Live state:

`Live Demo is not enabled. Recorded Run Replay remains available.`

Do not use wording that implies current AI execution.

### scenario catalog

Show exactly the four accepted scenarios.

At minimum expose from the corpus/index where present:

- scenario identity/version;
- human-readable scenario name/title;
- recorded timestamp;
- execution commit / run fingerprint;
- recorded/live type;
- terminal/result summary.

### scenario detail

For a selected scenario, render the recorded information needed to inspect the governance chain, using only fields actually present in the exact corpus.

Where present, expose:

- Task/scope;
- execution/work-run identity;
- transition/timeline;
- evidence candidate/admission;
- Human-owned evidence/gate status;
- Judgment;
- Cycle/history;
- NextAction;
- provenance identifiers/hashes/commit;
- recorded timestamp.

Do not invent missing values.

Use explicit `Not recorded in this public artifact` or equivalent when a field is legitimately absent.

### security rendering

Corpus-derived text MUST be inserted as text, not executable HTML.

Do not use unsafe `innerHTML`/template injection for corpus-controlled values.

No external JS/CSS/font/image CDN.

No third-party analytics/tracker.

No forms or mutation controls.

No upload/repository/task input.

No active Live button or start endpoint.

### errors

Provide truthful user-visible states for:

- corpus index unavailable;
- selected scenario missing;
- malformed JSON;
- unknown scenario selector;
- static 404.

Never fall back to owner API, provider call, or Live execution.

## URL/navigation contract

Static hosting must work without server-side route rewriting.

Use query/hash-based static navigation or another mechanism that requires only static file serving.

Do not require a SPA fallback that converts arbitrary missing URLs into a false success response.

All links must work under the Cloudflare Pages root output directory.

## Cloudflare Pages static security headers

Create `public/replay/_headers` with a bounded static-site policy.

At minimum:

- `X-Content-Type-Options: nosniff`
- `Referrer-Policy: no-referrer`
- frame embedding denied
- restrictive `Permissions-Policy`
- restrictive CSP allowing only same-origin static resources required by the implementation
- no permissive remote `connect-src`
- no need for inline script if avoidable

Do not claim headers are publicly effective until post-deployment verification.

## health/readiness artifact

Create `public/replay/health.json`.

It is a static release identity document, not a dynamic application health probe.

Required fields:

```text
status = "ok"
mode = "RECORDED_RUN_REPLAY"
live = false
corpus_root_sha256
scenario_count = 4
owner_database = false
provider_inference = false
```

Do not include secret/account/host-local data.

## Cloudflare Pages deployment documentation

Create `docs/AISCC_PUBLIC_REPLAY_DEPLOYMENT.md`.

It must preserve the accepted provider direction and document only source-supported settings.

Required:

```text
target:
Cloudflare Pages

deployment unit:
public/replay

runtime:
static files only

database:
none

provider/LLM:
none

secrets required by Replay:
none

Live:
disabled
```

Document both later supported deployment choices without executing them:

- Git-connected Pages project serving `public/replay`;
- direct upload of the exact verified static directory, only if later provider verification confirms the current product supports it.

Do not invent:
- account ID;
- project slug;
- pages.dev URL;
- custom domain;
- CLI auth state;
- production branch setting;
- current Cloudflare pricing/capabilities.

Those are verified in the actual deployment Task.

## Live-disabled release contract

Initial release classification is fixed:

`DISABLED_FOR_INITIAL_RELEASE`

The static surface SHALL:

- contain no executable Live ingress;
- not load provider code;
- not require provider secrets;
- clearly state that Live is not enabled;
- keep all Replay content usable independently.

Do not implement Railway/OpenAI in this Task.

## current-state reconciliation

The 1009 Executor correctly stopped before canonical projection updates.

This Task MUST reconcile current command-center state if current bytes are still stale:

### CURRENT_STATE_SUMMARY

Record:

```text
P3-2 = ACCEPTED / PERSISTED / CLOSED
P3-3 = ACTIVE
current technical blocker = public Replay serving/deployment prerequisite implementation
baseline HEAD entering implementation = 17fcd337a8bc1410e230a7c18195ac3d3006b417
Live initial release = DISABLED_FOR_INITIAL_RELEASE
Replay deployment target direction = Cloudflare Pages / NOT_DEPLOYED
```

### NEXT_ACTIONS

Project the exact current implementation Task and post-implementation sequence:

```text
implementation
→ local/Human QA
→ persistence
→ Cloudflare Pages deployment
→ public availability verification
→ final competition submission
```

### DECISION_REGISTER

First locate exact decision id:

`AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1`

If it exists and matches Cloudflare Pages / Railway Singapore / separate OpenAI API Project, do not duplicate it.

If absent or materially conflicting, STOP `DECISION_AUTHORITY_CONFLICT`.

You may record the new evidence-supported release decision:

`Initial competition release keeps PUBLIC_BOUNDED_LIVE disabled and ships Recorded Replay first`

only if that decision is not already represented.

## release/readiness documents

Update predecessor blocked records to reflect implementation candidate state:

- `.aiassistant/reports/aiscc/AISCC_P3_3_PUBLIC_RELEASE_READINESS.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_MANIFEST_CANDIDATE.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_DISCLOSURE_REGISTER.md`
- `.aiassistant/reports/aiscc/AISCC_COMPETITION_SUBMISSION_PACKAGE.md`

Rules:

- do not mark public deployment complete;
- service URL stays `PENDING_DEPLOYMENT`;
- public repository accessibility stays unverified unless separately proven;
- Human rights/tool roster confirmation remains pending;
- narrow R01/R02 from blocker to implementation/local-readiness status only when evidence passes;
- note that the public static release contains no external frontend dependencies/assets unless the implementation actually introduces some.

## local verification

Required deterministic validation:

1. `python ... build_public_replay.py` build/write PASS;
2. second build/check demonstrates deterministic/no-drift output;
3. source corpus hashes/sizes == canonical index;
4. public copied corpus bytes == source bytes;
5. generated manifest hashes reconcile;
6. all local static links resolve;
7. no external URLs in executable JS/CSS/HTML except inert documentation text if unavoidable;
8. no secret/token/host-path/private-data patterns;
9. no mutation forms/actions;
10. no Live execution control;
11. no owner API/DB/provider endpoint reference in executable public assets;
12. security header file syntax/content check;
13. `git diff --check` PASS.

### local HTTP smoke

Serve only the static directory on loopback, for example with a standard-library static server.

Verify over `127.0.0.1`:

- `/` -> 200
- `/health.json` -> 200 and exact release identity
- `/data/REPLAY_CORPUS_INDEX.json` -> 200
- four member JSON files -> 200
- static assets -> 200
- unknown file -> 404
- no request is made to owner API/provider/network

A localhost test does not count as deployment.

Do not bind local QA server to `0.0.0.0`.

## visual Human QA package

Create in target bundle:

`PUBLIC_REPLAY_HUMAN_QA_GUIDE.md`

It must provide exact local setup/URL and operations for Human:

1. landing/Recorded label;
2. four scenario catalog;
3. each scenario detail;
4. Task → Evidence → Judgment → Cycle → NextAction comprehension;
5. Live-disabled wording/control absence;
6. 404/error state;
7. 1080 / 1280 / 1440 desktop widths;
8. no host/private/internal data visible.

Human QA is not performed by Executor.

## scope

### allowed substantive changes

- `scripts/build_public_replay.py`
- `public/replay/**`
- `docs/AISCC_PUBLIC_REPLAY_DEPLOYMENT.md`
- narrowly scoped tests for this feature
- current P3-3 readiness/submission/disclosure/manifest records
- CURRENT_STATE_SUMMARY / NEXT_ACTIONS
- DECISION_REGISTER only as allowed above
- Task/report/export artifacts

### forbidden substantive changes

- owner/private Command Center UI/API semantics except no changes are expected;
- PostgreSQL owner projections;
- Replay canonical source corpus;
- P3-1 evidence/protocol;
- accepted README/public comparative summary/truth map;
- provider profiles/budget config;
- Railway/OpenAI setup;
- DB schema/migrations;
- unrelated product/runtime behavior;
- Cloudflare account/project configuration;
- Git push/deploy;
- competition form.

No Git commit in this Task.

## evidence contract

executor_required:

### `STATIC_SOURCE / IMPLEMENTATION`
- standalone public Replay surface exists;
- build generator deterministic;
- exact corpus identity preserved;
- no DB/provider/secret runtime dependency.

### `LOCAL_HTTP_RUNTIME`
- loopback static smoke as specified;
- no external network;
- truthful 404/error behavior.

### `SECURITY_CONFORMANCE`
- static headers;
- safe text rendering;
- no mutation/input/Live control;
- no owner API/provider endpoint use;
- public data limited to accepted corpus/static assets.

### `PUBLIC_PROVENANCE`
- public build manifest ties output to exact canonical corpus and source baseline;
- state/readiness docs are truthful.

reuse_allowed:
- accepted P2 Replay sanitization/provenance;
- accepted deployment direction `AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1`;
- P3-1/P3-2 accepted records.

human_owned:
- visual/readability QA;
- project/source ownership/legal confirmation;
- exact AI tool/model roster disclosure;
- Cloudflare account/project authorization;
- actual public deployment;
- final submit.

not_required:
- provider inference;
- PostgreSQL;
- Railway;
- OpenAI API;
- paid API;
- external network;
- public URL check before deployment.

forbidden:
- public deployment;
- Git push;
- provider/account login;
- Live execution;
- competition submission;
- canonical corpus mutation.

proof_non_substitution:
- local static 200 != public deployment;
- Cloudflare-targeted artifact != Cloudflare project;
- build determinism != Human UX acceptance;
- persisted corpus != public availability;
- Live-disabled copy != Live security implementation;
- Human legal confirmation pending != legal clearance.

## accept criteria

- exact predecessor source/workspace identity passes;
- accepted deployment decision exact match passes;
- canonical corpus unchanged;
- standalone `public/replay` artifact generated;
- all four corpus public copies byte-identical;
- page browsing requires no DB/provider/secret;
- local HTTP smoke PASS;
- static error behavior PASS;
- no active Live ingress;
- Cloudflare deployment doc/manifest exact enough for a later deployment Task;
- state projection reconciled;
- release docs remain truthful;
- Human QA guide created;
- no forbidden action.

## hold/reject criteria

- reuses/exposes LOCAL_PRIVATE_ONLY owner app publicly;
- connects public site to owner DB/API;
- modifies Replay source corpus;
- introduces provider/Live dependency;
- cannot prove byte-identical public corpus;
- unsafe corpus HTML injection;
- external CDN/analytics dependency added without authority;
- deployment or account mutation performed;
- accepted host decision contradicted;
- public release status falsely upgraded.

## mandatory stop

STOP if:

- HEAD or exact predecessor untracked inventory differs;
- `AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1` is absent or materially conflicts with the accepted direction;
- corpus identity conflicts;
- required implementation would expose private/customer/company material;
- a secret value/account login is required;
- task scope must expand into owner runtime, provider, Railway or DB;
- external network is required for implementation/local validation.

After STOP, produce only blocker evidence/report/export.

## expected terminal candidate

```text
IMPLEMENTATION_CANDIDATE / HUMAN_QA_PENDING
```

Executor must not declare:
- public deployment complete;
- P3-3 closed;
- competition submitted.

## export bundle

Target:

`.aiassistant/reports/target/20260915_1047_aiscc-p3-3-public-recorded-replay-static-surface-and-cloudflare-pages-prerequisite-implementation-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PUBLIC_REPLAY_IMPLEMENTATION_EVIDENCE.json`
- `PUBLIC_REPLAY_LOCAL_HTTP_EVIDENCE.json`
- `PUBLIC_REPLAY_SECURITY_VALIDATION.json`
- `PUBLIC_REPLAY_HUMAN_QA_GUIDE.md`
- changed project files preserving relative paths
- `TERMINAL_WORKSPACE.json`
- `VALIDATION.json`
- `REMOVED_FILES.md` only if an actual project file was deleted

Terminal ZIP:

`.aiassistant/reports/target/20260915_1047_aiscc-p3-3-public-recorded-replay-static-surface-and-cloudflare-pages-prerequisite-implementation-1.zip`

## final response

1. result
2. source/decision/corpus identity
3. implemented public surface
4. deterministic build result
5. local HTTP smoke
6. security/no-inference validation
7. Live-disabled result
8. state/readiness reconciliation
9. changed files
10. target bundle + ZIP
11. Human QA
12. remaining Human/deployment blockers
