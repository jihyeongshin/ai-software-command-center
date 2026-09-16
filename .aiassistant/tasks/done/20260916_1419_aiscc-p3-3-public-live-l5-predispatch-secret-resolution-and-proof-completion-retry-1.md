# 작업지시서: P3-3 L5 Pre-dispatch Secret Resolution + Proof Completion Retry

## meta

- task_id: `20260916_1419_aiscc-p3-3-public-live-l5-predispatch-secret-resolution-and-proof-completion-retry-1`
- created_at: `2026-09-16 KST`
- work_type: `REWORK`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `04436a11adc6dd6e70b4a98568fe878cc4c9f4aa`
- predecessor_task: `20260916_1412_aiscc-p3-3-public-live-l5-secret-binding-durable-missing-secret-and-proof-completion-retry-1`
- primary_semantic_owner: `P3-3 L5 hosted secret pre-dispatch compatibility + local runtime proof`

Use the current IDE Executor conversation. No fresh chat is required.

## current state

```text
HEAD:
04436a11adc6dd6e70b4a98568fe878cc4c9f4aa

L4:
ACCEPTED / CLOSED

L5:
OPEN / LOCAL REWORK

Human Railway deployment:
NOT_YET_AUTHORIZED

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## predecessor candidate

Retain the uncommitted 1352 candidate.

Authority:

`.aiassistant/reports/target/20260916_1352_aiscc-p3-3-public-live-l5-railway-secret-binding-and-deployment-contract-implementation-1/SOURCE_INVENTORY.json`

Expected:

`11/11 PASS`

Do not revert accepted secret resolver/environment/Railway contract work.

## policy-conflict resolution — controlling

The previous Task's requirement for an exact `DEFINITELY_NOT_SENT` label is superseded for the missing-hosted-secret pre-dispatch branch by this exact canonical mapping.

### hosted provider ordering

Implement:

```text
1. load/revalidate current run + execution authority
2. existing PROVIDER + SECRET security admission
3. issue exact single-use SecretResolutionLease
4. resolve AISCC_OPENAI_API_KEY
5. if present, reserve provider/round/budget bounds
6. final freshness barrier
7. start_dispatch_if_fresh
8. invoke OpenAI adapter
```

Keep the exact existing capability/selector requirements.

Do not resolve secret before security admission.

### missing or blank secret

If step 4 fails with `HostedSecretUnavailable`:

```text
provider SDK/client request:
0

provider network request:
0

durable provider-call reservation:
0

durable round reservation:
0

durable provider budget-unit reservation:
0

operation:
existing pre-dispatch terminal semantics

target:
OUTCOME_KNOWN

outcome:
CANCELLED
(or the exact current repository helper representation for SECURITY_ADMITTED pre-dispatch cancel)

sanitized reason:
LIVE_UNAVAILABLE

OUTCOME_UNKNOWN:
FORBIDDEN

automatic retry:
FORBIDDEN

secret lease:
close/revoke
```

Do not create a fake `DISPATCH_STARTED`.

Do not use `DEFINITELY_NOT_SENT` if the current protocol requires dispatch-started ancestry for that enum.

Do not add a new operation outcome.

Do not add generic negative reservation/refund support.

### public/API classification

Public-facing failure remains:

`LIVE_UNAVAILABLE`

Do not expose internal `CANCELLED` as a claim that a Human/public requester cancelled the run.

### positive secret branch

If secret resolution succeeds:

- raw material remains trusted-process-only;
- then perform the existing bound reservation;
- then final state/version freshness;
- then durable dispatch start;
- then provider adapter.

Secret presence must not bypass budget/freshness/dispatch gates.

### failure after successful secret resolution but before dispatch

Close lease.

If reservation/freshness fails before dispatch, use the current canonical pre-dispatch failure/cancel semantics.

Conservative reservation consumption after a successful reservation may remain according to current accepted runtime contract.

No generic refund feature in this Task.

### actual post-dispatch uncertainty

Once dispatch may have occurred:

```text
TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
```

must remain unchanged.

No blind retry.

## crash/restart evidence

Add/prove at least:

### A — crash/recovery at SECURITY_ADMITTED before reservation

No provider reservation, no provider send.

Recovery must not become remote unknown.

### B — missing/blank hosted secret

Pre-dispatch known terminal outcome, zero provider reservations.

### C — successful secret resolution then reservation/freshness failure

No provider send; accepted conservative bound behavior recorded truthfully.

### D — actual post-dispatch transport uncertainty

Unknown outcome retained with no blind retry.

Do not substitute unit-only phase tests for durable PostgreSQL recovery evidence.

## PostgreSQL runtime

Explicitly authorized:

```text
postgres:17.6
cached image only
network pull forbidden
task-owned container/volume
preferred bind 127.0.0.1:55432
private/pre-existing DB reuse forbidden
```

Emit:

`LOCAL_POSTGRES_RUNTIME.json`

## durable missing-secret tests

Use actual durable `AgentExecutionService.execute()`.

Test both:

- variable missing;
- variable blank.

Prove:

- secret capability/lease is the accepted one;
- zero adapter/client invocation;
- zero provider send;
- zero provider-call/round/provider-budget reservation;
- operation reaches pre-dispatch known terminal state;
- reason sanitized as LIVE_UNAVAILABLE;
- no unknown-outcome refs;
- no retry;
- attempt fails closed;
- Replay/static remains independent.

## positive fake-secret durable test

Use a synthetic sentinel value only.

Traverse:

```text
hosted Luna profile
→ PROVIDER + SECRET capability
→ single-use lease
→ HostedOpenAISecretResolver
→ bound reservation
→ final freshness + dispatch
→ fake OpenAI SDK/transport
```

No external network.

Prove exact accepted request flags/profile and lease single-use behavior.

## DB non-exposure proof

Against the task-owned PostgreSQL runtime, execute the positive fake-secret flow.

Search all relevant provider/execution/public-live durable text/JSON/provenance/protocol columns for the exact synthetic sentinel.

Required:

`exact sentinel occurrences = 0`

Record tables/columns inspected without dumping unrelated content.

## actual sandbox/container proof

Use the existing accepted/cached P1-3 sandbox runtime/image.

No image pull.

Parent trusted process may contain synthetic:

```text
AISCC_OPENAI_API_KEY=<sentinel A>
OPENAI_API_KEY=<sentinel B>
```

Using the product sandbox/container environment path, prove inside the actual child/container:

```text
AISCC_OPENAI_API_KEY:
ABSENT

OPENAI_API_KEY:
ABSENT
```

A manually sanitized Docker command alone is not sufficient.

If the accepted/cached image is unavailable:

`BLOCKED_LOCAL_SANDBOX_PREREQUISITE`

and STOP.

## child/Git/Docker environment proof

Retain and execute sentinel coverage for:

- local subprocess;
- Docker control CLI;
- Git observer;
- Python startup/proxy/dynamic-loader sensitive environment where applicable.

## Railway/build audit

Reuse the 1352 contract and audit.

Re-run narrow source search after mutation.

No:

- env dump;
- `printenv`;
- `RUN env`;
- broad environment serialization;
- `.env` commit/copy;
- secret logging.

Do not claim sealed variables are build-isolated.

## full regression — mandatory

Because the candidate changes shared provider/process/Docker/Git paths, run the repository-wide suite.

Prior accepted baseline:

`1423 PASS / 3 existing Windows symlink-host SKIP / 0 FAIL / 0 ERROR`

Requirements:

- zero FAIL;
- zero ERROR;
- no new skip/xfail;
- no assertion dilution;
- pass count not reduced by disabled/removed tests.

Also run:

- focused L5 hosted-secret tests;
- P1-5 provider persistence/runtime tests;
- P1-3 Docker/sandbox tests;
- Public Live tests affected by provider availability;
- Ruff;
- formatting check;
- mypy;
- `git diff --check`.

## secret scan

No real key may appear.

If a real credential-like value is detected:

STOP and report only path/artifact + detector class.

Synthetic test sentinels are allowed when clearly labelled.

## real external actions

Must remain:

```text
real OpenAI calls:
0

Railway mutation:
0

Railway deploy:
0

Cloudflare mutation:
0

Git commit/push:
0
```

## Public state

Before/after:

```text
Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## acceptable final outcome

If all local implementation/proof passes:

`HUMAN_RAILWAY_DEPLOYMENT_REQUIRED / LOCAL_ACCEPTED_CANDIDATE`

Do NOT claim terminal L5 acceptance.

## Human-pending after local PASS

- exact Railway project/environment/backend-service identity;
- production backend service region;
- Human secret variable entry;
- service-level scope;
- seal confirmation;
- deploy/restart;
- hosted child/sandbox non-exposure;
- trusted proxy/ingress;
- production PostgreSQL binding;
- one later explicitly authorized real Luna canary.

## mandatory stop

- HEAD mismatch;
- predecessor 11-path candidate mismatch;
- ordering change requires new WorkflowState/outcome/schema;
- current security capability contract cannot resolve secret before reservation safely;
- PostgreSQL unavailable;
- cached sandbox unavailable;
- sentinel appears in DB/log/public output;
- full regression failure;
- real credential required.

## export

Target:

`.aiassistant/reports/target/20260916_1419_aiscc-p3-3-public-live-l5-predispatch-secret-resolution-and-proof-completion-retry-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `SOURCE_INVENTORY.json`
- `LOCAL_POSTGRES_RUNTIME.json`
- `PREDISPATCH_SECRET_ORDERING_EVIDENCE.md`
- `DURABLE_MISSING_SECRET_EVIDENCE.md`
- `SECRET_DB_NON_EXPOSURE_EVIDENCE.md`
- `LOCAL_SANDBOX_SECRET_NON_EXPOSURE_EVIDENCE.md`
- `TEST_EVIDENCE.json`
- retained/updated L5 secret binding contract, build audit, rotation runbook, canary plan as needed
- workspace before/after

## final response

1. result
2. target bundle
3. resolved ordering implementation
4. missing/blank durable outcome and zero reservation evidence
5. post-dispatch unknown-outcome regression
6. crash/restart evidence
7. source/config/test inventory
8. PostgreSQL runtime
9. DB secret non-exposure
10. sandbox/container non-exposure
11. child/Git/Docker environment proof
12. build exposure audit
13. focused tests
14. full regression
15. static/type/diff
16. secret scan
17. real provider calls
18. external deployment actions
19. Public state
20. workspace integrity
21. Human Railway pending evidence
