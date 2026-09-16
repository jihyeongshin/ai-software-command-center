# 작업지시서: P3-3 L5 Secret Binding Durable Missing-Secret + Proof Completion Retry

## meta

- task_id: `20260916_1412_aiscc-p3-3-public-live-l5-secret-binding-durable-missing-secret-and-proof-completion-retry-1`
- created_at: `2026-09-16 KST`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `04436a11adc6dd6e70b4a98568fe878cc4c9f4aa`
- predecessor_task: `20260916_1352_aiscc-p3-3-public-live-l5-railway-secret-binding-and-deployment-contract-implementation-1`
- primary_semantic_owner: `P3-3 L5 local hosted-secret runtime boundary`

Use the current IDE Executor conversation. No fresh chat is required.

## current authority

L4 remains:

`ACCEPTED / CLOSED`

L5 exact authority remains:

`Deployment packaging, ingress and sandbox proof`

The accepted hosted-secret direction remains unchanged.

Do NOT re-open Human provider/account decisions.

## expected working state

HEAD must remain:

`04436a11adc6dd6e70b4a98568fe878cc4c9f4aa`

The predecessor local candidate is expected to remain uncommitted.

Retained predecessor source authority:

`.aiassistant/reports/target/20260916_1352_aiscc-p3-3-public-live-l5-railway-secret-binding-and-deployment-contract-implementation-1/SOURCE_INVENTORY.json`

Expected predecessor candidate count:

`11`

Expected paths:

- `config/deployment/public-live-railway.v1.toml`
- `src/aiscc/providers/external_ide.py`
- `src/aiscc/providers/hosted_secret.py`
- `src/aiscc/providers/openai_responses.py`
- `src/aiscc/providers/service.py`
- `src/aiscc/public_live/luna_profile.py`
- `src/aiscc/runtime/child_environment.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/runtime/process.py`
- `tests/fixtures/providers/luna_capabilities.py`
- `tests/unit/providers/test_hosted_secret.py`

If these bytes/path identities materially differ before retry, report exact mismatch and STOP rather than guessing.

Unrelated `__pycache__`/local residue remains non-blocking and must not be broadly cleaned.

## defect to fix

### current defect

`HostedOpenAISecretResolver.resolve()` can raise `HostedSecretUnavailable` before any OpenAI SDK request exists.

The non-durable `execute_provider()` path correctly maps it to:

```text
sanitized:
LIVE_UNAVAILABLE

outcome:
DEFINITELY_NOT_SENT

provider calls:
0
```

The durable `AgentExecutionService.execute()` path currently catches this inside the generic post-dispatch exception path and persists:

```text
OUTCOME_UNKNOWN
TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
```

This is incorrect.

### required durable semantics

A missing/blank hosted secret MUST be classified as known-not-sent.

Required durable evidence:

```text
SDK/client construction or provider request:
0

operation outcome:
DEFINITELY_NOT_SENT
(or exact existing canonical known-not-sent representation)

sanitized failure:
LIVE_UNAVAILABLE

remote unknown quarantine:
NO

automatic retry:
NO

provider call counters:
0

provider usage/tokens:
0

secret value persisted:
NO
```

The execution attempt may fail closed using the existing accepted failure authority, but it must not claim a remote-unknown outcome.

Do not alter the existing semantics for a real timeout/connection exception after provider invocation could have occurred:

```text
actual send/transport uncertainty
→ TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
→ no blind retry
```

## implementation boundary

Prefer the smallest correction in the existing durable provider path.

Do not redesign:

- WorkflowState;
- ExecutionStatus;
- semantic provider-request persistence;
- L1/L2/L3/L4 contracts;
- retry ceilings;
- Luna provider profile;
- secret lease authority.

If a new helper is useful, keep it local to the existing outcome mapping.

## PostgreSQL proof — explicitly authorized

Use a task-owned isolated PostgreSQL 17.6 runtime.

```text
image:
postgres:17.6

network pull:
FORBIDDEN

reuse private/pre-existing DB:
FORBIDDEN

preferred bind:
127.0.0.1:55432
```

If the port is occupied by an unrelated process, use a clearly task-owned alternate local port and record it.

Emit:

`LOCAL_POSTGRES_RUNTIME.json`

Use this DB for the durable missing-secret and DB non-exposure proof.

Cleanup task-owned runtime best-effort after evidence.

## durable missing-secret integration test

Use the actual durable `AgentExecutionService.execute()` path and the hosted profile/resolver with a fake environment.

Test at least:

1. variable missing;
2. variable empty/blank.

For both, prove:

- no OpenAI SDK/client construction;
- no HTTP/provider send;
- known-not-sent durable outcome;
- sanitized `LIVE_UNAVAILABLE`;
- no unknown-outcome refs;
- no blind retry;
- no provider usage/call accounting;
- fail-closed execution result;
- Replay/static availability unaffected.

Do not use only the `execute_provider()` helper as substitute.

## positive fake-secret durable test

Use a sentinel secret with a fake SDK/transport.

Traverse:

```text
server-owned hosted Luna profile
→ PROVIDER + SECRET capability
→ SecretResolutionLease
→ HostedOpenAISecretResolver
→ explicit adapter api_key injection
→ fake SDK only
```

Prove:

- exactly one fake SDK request;
- sentinel reaches only constructor boundary;
- sentinel absent from durable refs/history/DB/log/output/report;
- lease cannot be reused;
- accepted Responses request flags remain exact.

No external network.

## DB sentinel non-exposure

With a distinctive fake sentinel value, execute the positive fake-provider durable flow against task-owned PostgreSQL.

After completion, query the application/provider/public-live durable tables that can contain text/JSON/provenance/protocol data.

Required:

```text
sentinel exact value occurrences in durable DB:
0
```

Record table/column scope inspected without dumping unrelated data.

Do not store the real OpenAI key.

## actual local sandbox/container sentinel proof

The predecessor only intercepted Docker CLI environment creation.

Complete a local runtime proof using an available accepted/cached sandbox image or exact existing P1-3 sandbox runtime path.

Constraints:

- fake sentinel only;
- no image pull;
- no real provider network;
- no host secret;
- no arbitrary external network;
- task-owned disposable container.

Set parent process:

```text
AISCC_OPENAI_API_KEY=<fake sentinel>
OPENAI_API_KEY=<another fake sentinel>
```

Then use the product's sandbox/container environment construction and prove inside the actual child/container:

```text
AISCC_OPENAI_API_KEY:
ABSENT

OPENAI_API_KEY:
ABSENT
```

Do not bypass the product path with a manually sanitized `docker run` command as the only evidence.

If the exact accepted sandbox image is unavailable locally and no safe cached equivalent exists, STOP with:

`BLOCKED_LOCAL_SANDBOX_PREREQUISITE`

Do not pull a new image.

## child/process/Git/Docker control proof

Retain and rerun the predecessor sentinel tests for:

- actual local subprocess;
- Docker control CLI environment;
- Git observer environment;
- Python startup/proxy/dynamic-loader sensitive env non-inheritance where applicable.

## build-exposure audit

Retain the predecessor conclusion, but re-run narrow static search after all edits.

Require no:

- `RUN env`;
- `printenv`;
- broad environment serialization;
- `.env` copy/commit;
- secret logging;
- secret variable inclusion in build report.

Railway sealed variable is still build-visible. Do not claim otherwise.

## full regression — mandatory in this retry

Because the candidate modifies shared runtime/provider/Git/Docker paths, run the broader repository suite.

Accepted prior baseline:

`1423 PASS / 3 existing Windows symlink-host SKIP / 0 FAIL / 0 ERROR`

Required final result:

- `0 FAIL`;
- `0 ERROR`;
- the same existing three skips only, unless an exact pre-existing platform reason is proven;
- pass count must not decrease due to removed/disabled tests;
- no new xfail/skip/assertion dilution.

Also run:

- focused L5 hosted-secret/provider/runtime tests;
- Ruff;
- Ruff format/check as repository convention;
- mypy;
- `git diff --check`.

Record exact commands and results.

## source-secret scan

Before export, scan changed/canonical candidate content for secret material.

Required:

- no real `sk-...` key value;
- no password-manager content;
- no environment dump;
- fake sentinel allowed only in tests/evidence expressly labeled synthetic.

Do not print any discovered real secret. If detected, STOP and report only artifact/path + detector class.

## Railway/deployment boundary

Still NOT authorized:

- Railway project/service mutation;
- entering real key into Railway;
- sealing variable;
- deployment/restart;
- public ingress;
- Cloudflare mutation;
- real provider canary.

The correct final outcome after this retry, if all local proof passes, is:

`HUMAN_RAILWAY_DEPLOYMENT_REQUIRED / LOCAL_ACCEPTED_CANDIDATE`

not terminal L5 acceptance.

## real provider calls

Must remain:

`0`

## Public state

Before/after:

```text
Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## Git

No commit/push.

## required evidence

Emit/update:

- `EXECUTOR_REPORT.md`
- `SOURCE_INVENTORY.json`
- `LOCAL_POSTGRES_RUNTIME.json`
- `DURABLE_MISSING_SECRET_EVIDENCE.md`
- `SECRET_DB_NON_EXPOSURE_EVIDENCE.md`
- `LOCAL_SANDBOX_SECRET_NON_EXPOSURE_EVIDENCE.md`
- `TEST_EVIDENCE.json`
- updated `L5_SECRET_BINDING_CONTRACT.md` only if semantics need clarification
- predecessor Railway build audit / rotation / canary plan preserved or updated only when needed
- workspace before/after

## accept criteria

All must pass:

1. exact HEAD unchanged;
2. accepted predecessor L5 authority reused;
3. missing/blank secret durable path = known not sent;
4. actual transport uncertainty remains unknown;
5. zero provider sends on missing secret;
6. sentinel absent from durable DB;
7. actual local sandbox/container does not inherit secret variables;
8. child/Git/Docker control paths do not inherit secret;
9. full regression green without dilution;
10. static/type/diff checks green;
11. source secret scan clean;
12. real provider calls 0;
13. Railway/deployment actions 0;
14. Public admission disabled;
15. no commit/push.

## mandatory stop

- HEAD mismatch;
- predecessor candidate unexpectedly missing/collided;
- durable fix requires workflow/provider semantic redesign;
- cached local sandbox prerequisite unavailable;
- PostgreSQL local runtime unavailable;
- secret sentinel appears in durable DB/log/public output;
- full regression fails;
- real credential would be required.

## export

Target:

`.aiassistant/reports/target/20260916_1412_aiscc-p3-3-public-live-l5-secret-binding-durable-missing-secret-and-proof-completion-retry-1/`

## final response

1. result
2. target bundle
3. durable missing-secret correction
4. exact known-not-sent vs unknown distinction
5. source/config/test inventory
6. PostgreSQL evidence
7. DB secret non-exposure
8. actual sandbox secret non-exposure
9. child/Git/Docker environment proof
10. build exposure audit
11. focused tests
12. full regression
13. static/type/diff
14. source secret scan
15. real provider calls
16. external actions
17. Public state
18. workspace integrity
19. Human Railway pending evidence
