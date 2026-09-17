# AISCC Cycle Record

## meta

- cycle_id: `20260917_0825_aiscc-p3-3-public-live-l5-start-worker-hosted-proof-substantive-rework-required-1`
- date: `2026-09-17 KST`
- owner: `Browser Command Center`
- phase: `P3-3 Public Live L5`
- predecessor_task: `20260917_0217_aiscc-p3-3-public-live-l5-start-initializer-worker-hosted-proof-implementation-resume-1`
- reviewed_result_zip_sha256: `35479a09be4edc0f946e06cc163420eb777dfcd5fd1cc506cff647e4afbca24b`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- result_status: `REWORK_REQUIRED`
- implementation_rejected: `NO`
- accepted_designs_reopened: `NO`
- l5_terminal: `OPEN`
- public_admission: `DISABLED`
- public_live: `NOT_RELEASED`

## bundle integrity / reviewability

Browser Command Center independently inspected the uploaded result ZIP.

```text
ZIP SHA-256:
35479a09be4edc0f946e06cc163420eb777dfcd5fd1cc506cff647e4afbca24b

member_count:
60

SOURCE_INVENTORY:
37

source identity:
37 / 37 exact SHA-256 + byte-size PASS

EXPORT_MANIFEST listed-member hashes:
PASS

unsafe traversal:
0

duplicate normalized source paths:
0
```

The bundle is substantively reviewable.

Packaging defect:

- source/test/migration/config archive member names were emitted with Windows `\` separators;
- after safe separator normalization the 37 source identities match exactly;
- this does not prevent this Browser review, but the next result ZIP MUST use POSIX `/` archive member paths exactly.

## Executor claim

`HOSTED_PUBLIC_LIVE_START_AND_DURABLE_WORKER_IMPLEMENTED / LOCAL_ACCEPTED_CANDIDATE`

Reported evidence:

```text
full regression:
1496 PASS
3 existing SKIP
0 FAIL
0 ERROR

focused Public Live:
109 PASS

hosted initializer/claim/fault proof:
12 PASS

PostgreSQL:
17.6

Alembic:
20260917_0020

real provider:
0

Railway/Cloudflare/Git:
0
```

The test execution itself is not rejected. However source-level review finds load-bearing production paths that the tests did not exercise.

## substantive judgment

### R1 — normal production worker remains non-runnable

Current production composition:

```text
aiscc public-live-worker
→ create_worker()
→ execute_claim = None
→ HostedPublicLiveWorker.run()
→ PUBLIC_WORKER_P1_EXECUTOR_REQUIRED
```

`create_worker()` does not wire a production claim executor.

Further, the newly added pure semantic functions:

- `plan_next_semantic_request`
- `build_public_provider_call`

have no production caller.

`execution_link_operation(...)` is created in migration 0018 but has no production caller and no runtime EXECUTE grant.

Therefore the accepted chain is still absent:

```text
durable claim
→ semantic plan
→ P1-5 operation
→ secret lease
→ final fence/freshness validation
→ DISPATCH_STARTED
→ hosted adapter
→ physical outcome
→ semantic validation / next role / terminalization
```

This is a direct failure of the normal `public-live-worker` production composition requirement.

### R2 — worker lease renewal and dispatch pin authority are not wired

Migration 0019 creates:

- 15-second claims;
- `worker_renew(...)`;
- `public_worker_dispatch_pin`;
- claim-event kinds `OPERATION_BOUND`, `PINNED`, `PIN_CLOSED`.

But the foreground worker loop:

- never calls `renew`;
- performs no 5-second renewal cadence;
- has no operation-bind/pin/close API;
- has no source path that inserts or closes `public_worker_dispatch_pin`.

The dispatch-pin table is therefore structural dead state.

The accepted final claim/fence hook is not atomically connected to canonical P1-5 `DISPATCH_STARTED`.

If exact atomic P1-5 + claim/fence composition cannot be implemented under the accepted design, STOP with `ACCEPTED_AUTHORITY_IMPLEMENTATION_CONFLICT`.

### R3 — hosted-l5-proof still substitutes static expectations for provider-double observation

`HostedProofSettings.provider_double_url` is validated but never used by the proof execution path.

`execute_provider_fault(...)` directly mutates `PipelineStore` and then returns `expectation(...)`.

`provider_receipts` is a hard-coded field of `ProofExpectation`; it is not read from a provider-double receipt source.

The sandbox fault path still raises:

`SANDBOX_TERMINATION_REQUIRES_PROCESS_SUPERVISOR`

Therefore:

- provider-double receipt counts are not observed;
- post-dispatch transport uncertainty is not produced by the private provider double;
- sandbox/process-tree termination is not executed by `hosted-l5-proof`.

The proof is not yet the accepted D9/D16 hosted executable proof.

### R4 — initializer least-privilege login is not proven executable

Migration 0020 creates:

```text
aiscc_public_live_initializer
  NOLOGIN
  NOINHERIT

aiscc_live_initializer_login
  LOGIN
  NOINHERIT

GRANT aiscc_public_live_initializer
TO aiscc_live_initializer_login
```

But the application connection path does not activate the capability role.

The functional initializer tests use the task-owner database connection, while the role test checks privilege metadata for the NOLOGIN capability role.

That does not prove:

```text
aiscc_live_initializer_login
→ accepted capability-role activation
→ start_next / P1 startup writes
```

under actual least privilege.

Production must prove the login-role session can run the initializer while remaining unable to become migration/schema owner.

### R5 — start freshness uses admitted time instead of authoritative current time

`CanonicalStartOwners.admit_start(...)` currently sets:

```text
now = candidate["admitted_at"]
```

and uses that historical timestamp to issue/consume start capabilities.

That makes the P1-3 start security check insensitive to actual elapsed wall/database time.

Also `start_next(...)` can lease a nonterminal start record without checking current Public deadline/gate before P1 genesis/start operations.

Final binding has stronger deadline/gate checks, but that is too late: READY / attempt / RUNNING side effects may already exist.

The accepted policy/gate-drift fail-closed requirement must be enforced before each new start side effect using current durable/DB time and current gate authority.

Historical `admitted_at` may remain provenance only; it must not substitute for current freshness.

## effect

This is a focused source REWORK.

The accepted designs remain closed:

```text
P1_5_PUBLIC_LIVE_SEMANTIC_LIFECYCLE_V1
PUBLIC_LIVE_DURABLE_WORKER_AUTHORITY_V1
PUBLIC_LIVE_START_AUTHORITY_V1 / TOPOLOGY_D
```

Do not redesign them merely to make tests pass.

No Git persistence, Railway mutation, real OpenAI request, key read/export, Public enablement or release is authorized.
