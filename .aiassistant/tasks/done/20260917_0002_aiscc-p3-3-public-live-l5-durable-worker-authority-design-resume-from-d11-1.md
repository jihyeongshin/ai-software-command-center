# 작업지시서: P3-3 L5 Durable Worker Authority Design Resume from D11

## meta

- task_id: `20260917_0002_aiscc-p3-3-public-live-l5-durable-worker-authority-design-resume-from-d11-1`
- created_at: `2026-09-17 KST`
- work_type: `DESIGN_AUDIT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_HEAD: `96a4029ec3a82c9b2a88b9718732aa0f00ecad20`
- accepted_p1_5_extension: `P1_5_PUBLIC_LIVE_SEMANTIC_LIFECYCLE_V1`
- accepted_p1_5_result_zip_sha256: `dbc4258feeb474b823f077951bb0004966228f14377d2c00deb8d131d9e93826`
- implementation_authorized: `NO`

Use the current IDE Executor conversation. No fresh chat is required.

## Human-accepted prerequisite

The Browser/Human decision is final:

```text
P1_5_PUBLIC_LIVE_SEMANTIC_LIFECYCLE_V1
HUMAN_PROVIDED / ACCEPTED / CLOSED
```

Do not reopen the 2318 P1-5 lifecycle design.

## predecessor design to resume

Resume:

`20260916_2303_aiscc-p3-3-public-live-l5-durable-worker-work-source-authority-design-freeze-1`

That design stopped at D11 with:

`P1_5_PROVIDER_AUTHORITY_EXTENSION_REQUIRED`

Now that the required extension is accepted, continue from D11.

Do NOT regenerate D1-D10 from scratch.

Re-read the 2303 design artifacts and preserve their exact predecessor conclusions unless directly contradicted by the newly accepted P1-5 extension.

## accepted P1-5 facts now available to D11-D17

Use these as authority:

### lifecycle owner

`AgentExecutionService` remains sole durable physical provider lifecycle owner.

### attempt model

One RUNNING P1 attempt may contain:

```text
PRIMARY
→ optional VERIFY
→ optional CORRECT
→ at most one exact same-role retry
```

as multiple sequential immutable physical operations.

### planning

Public Live semantic planning and validation are pure.

Planning does NOT:

- reserve provider money;
- mint provider operation truth;
- resolve secret;
- mark dispatch;
- settle physical outcome.

### physical operation truth

Each physical send is one immutable P1-5 operation.

Retry creates a new operation ID/ordinal.

Canonical ambiguity marker:

`P1-5 DISPATCH_STARTED`

UNKNOWN remains no-blind-retry.

### secret

Existing issuer-backed single-use `SecretResolutionLease` remains authoritative.

Missing/blank secret:

```text
provider calls = 0
request liability = 0
dispatch marker = absent
```

### final dispatch hook

Immediately before `DISPATCH_STARTED`, P1-5 must revalidate:

- worker claim ID;
- fence;
- current claim ownership;
- WorkRun state/version;
- execution attempt identity/version;
- operation fingerprint;
- provider/profile/scenario refs;
- remaining budget/call/retry bounds;
- provider capability;
- secret capability/lease validity.

### projection relationship

Public provider request rows are linked/derived semantic projections from P1-5 physical operations for integrated V1.

They are not a second physical-send source of truth.

### unchanged

- four ExecutionStatus values unchanged;
- nine WorkflowState values unchanged;
- P1-4 remains sole workflow state authority;
- P1-3 remains security/capability/secret authority;
- Replay remains zero execution.

## required work

Complete the durable-worker authority design from D11 through D17, then perform one final compatibility pass over D1-D10.

### D11 — ProviderCall construction owner

Finalize the exact server-owned pure builder from accepted semantic plan + local private protocol history to P1-5 ProviderCall.

Required:

- hosted Luna profile only in production;
- role-specific reasoning effort;
- fixed model/provider/endpoint;
- stable operation fingerprint;
- exact output/token/tool bounds;
- no caller-selected endpoint/model/provider;
- no mutation/reservation/secret/dispatch side effects.

Specify exact module/owner and interface.

### D12 — polling / wake-up behavior

Finalize the competition-runtime worker loop.

Prefer simple PostgreSQL polling unless current canonical architecture already requires something else.

Decide exact:

- poll interval;
- batch size;
- deterministic order;
- empty-queue backoff;
- DB failure backoff;
- graceful shutdown;
- claim settling on shutdown;
- no busy loop;
- no detached background task;
- no Redis/Kafka/SQS unless authority requires it.

### D13 — schema / migration

Using exact current schema, finalize the additive persistence model for:

- work-item identity;
- claim ID;
- worker instance ID;
- fencing value;
- claimed_at;
- lease_expires_at;
- heartbeat/renewal;
- release/recovery reason;
- link to exact P1-5 operation;
- exclusion of UNKNOWN/quarantined/terminal work.

Reconcile the provisional 2303 choice among:

A. outbox row + `FOR UPDATE SKIP LOCKED`;
B. dedicated worker-claim table;
C. advisory lock only.

Choose exactly one final model.

If predecessor D1-D10 already selected B provisionally, either confirm B with the accepted P1-5 extension or explicitly revise it with a concrete contradiction.

Specify:

- exact table/column/index/constraint names consistent with current migrations;
- transaction boundaries;
- old-row fail-closed/default-safe behavior;
- whether migration `20260916_0018` or later remains appropriate given the accepted P1-5 extension schema impact.

Do not write the migration.

### D14 — mediated API surface

Freeze exact interfaces equivalent to:

```text
claim_next_work(...)
renew_claim(...)
release_claim(...)
verify_claim_for_dispatch(...)
recover_expired_claims(...)
```

Also integrate the accepted P1-5 lifecycle interfaces for:

```text
build provider call
prepare operation
authorize/final-check dispatch
commit DISPATCH_STARTED
settle physical outcome
validate semantic result
plan next role/retry
complete/fail attempt
```

For each operation specify:

- owner module;
- caller;
- inputs;
- outputs;
- transaction boundary;
- durable event;
- idempotency;
- failure codes;
- forbidden use.

Raw SQL outside the persistence owner remains forbidden.

### D15 — safe provenance / observability

Freeze safe durable fields:

- opaque work item ID;
- internal run ref;
- claim ID;
- opaque worker ID;
- fence;
- state/version observed;
- timestamps;
- result/reason codes;
- P1 operation ID;
- semantic role;
- provider destination class only;
- no raw prompt;
- no secret;
- no provider payload;
- no raw public forwarding identity.

Specify public-vs-internal visibility.

### D16 — hosted-l5-proof reuse

Finalize how `aiscc hosted-l5-proof` uses the SAME production claim/fence/operation authority with:

- private provider double;
- fake/synthetic secret class;
- Public admission disabled;
- operator-only invocation;
- no HTTP bypass.

It must deterministically prove:

1. pre-dispatch crash:
   - no `DISPATCH_STARTED`;
   - provider double receipts 0;
   - expired/released claim may be retried only if durable rules allow;

2. post-dispatch crash:
   - `DISPATCH_STARTED` durable;
   - provider double receipt 1 where applicable;
   - restart observes UNKNOWN/quarantine;
   - claim rediscovery does not produce blind resend;

3. stale fence:
   - old worker denied before secret use/send;

4. known closed failure:
   - same-role retry only under accepted one-retry ceiling;

5. worker restart:
   - recovery from durable authority, not heartbeat inference;

6. sandbox/process termination:
   - remains a separate process-supervisor proof path but is coordinated in the same operator proof campaign.

### D17 — implementation map

Produce exact path-level implementation map.

Classify each:

- existing owner extended;
- new production module;
- migration;
- unit test;
- PostgreSQL integration test;
- hosted proof test;
- CLI/entrypoint;
- unchanged reused owner.

The map must also state which 2148/2253 changed paths are retained, revised or superseded.

## final D1-D10 compatibility pass

After D11-D17 are complete, revisit the 2303 D1-D10 conclusions ONLY to answer:

```text
Does the accepted P1-5 lifecycle extension contradict any D1-D10 assumption?
```

If no:
- mark D1-D10 `RETAINED_COMPATIBLE`.

If yes:
- revise only the affected D-number(s);
- give exact contradiction;
- do not silently rewrite the whole design.

Required final design must cover D1-D17 as one coherent authority model.

## required artifacts

Update/finalize:

`DURABLE_WORKER_AUTHORITY_DESIGN.md`

Create/finalize:

`DURABLE_WORKER_AUTHORITY_DECISION.json`

Also create:

- `D11_D17_COMPLETION.md`
- `D1_D10_COMPATIBILITY_REVIEW.md`
- `CURRENT_SCHEMA_AND_OWNER_AUDIT.md`
- `DESIGN_CONSISTENCY_CHECK.md`
- `IMPLEMENTATION_MAP.md`

## final design status

Return exactly one:

### compatible final candidate

`DURABLE_WORKER_AUTHORITY_DESIGN_COMPLETE / HUMAN_REVIEW_REQUIRED`

### still blocked

`DURABLE_WORKER_AUTHORITY_DESIGN_CONFLICT`

Do not call it accepted.

## source mutation

FORBIDDEN.

No changes to:

- product source;
- tests;
- migrations;
- lockfiles;
- deployment config.

## external actions forbidden

```text
OpenAI:
0

real key read/export:
0

Railway:
0

Cloudflare:
0

Git add/commit/push:
0

Public admission enable:
0

Public Live release:
0
```

## checks

Required:

- exact HEAD verification;
- index/worktree inventory;
- predecessor design identity;
- accepted P1-5 extension identity;
- migration head inventory;
- D1-D17 consistency;
- P1-3/P1-4/P1-5/L4 consistency;
- no-secret scan;
- no source mutation.

No full test suite is required for this design-only Task.

## export

Create:

`.aiassistant/reports/target/20260917_0002_aiscc-p3-3-public-live-l5-durable-worker-authority-design-resume-from-d11-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `DURABLE_WORKER_AUTHORITY_DESIGN.md`
- `DURABLE_WORKER_AUTHORITY_DECISION.json`
- `D11_D17_COMPLETION.md`
- `D1_D10_COMPATIBILITY_REVIEW.md`
- `CURRENT_SCHEMA_AND_OWNER_AUDIT.md`
- `DESIGN_CONSISTENCY_CHECK.md`
- `IMPLEMENTATION_MAP.md`
- `WORKSPACE_BEFORE.txt`
- `WORKSPACE_AFTER.txt`
- result ZIP

## final response

1. result
2. HEAD
3. accepted P1-5 extension identity
4. predecessor D1-D10 status
5. D11 ProviderCall owner
6. D12 polling
7. D13 claim schema/model
8. D14 mediated APIs
9. D15 provenance
10. D16 hosted proof reuse
11. D17 implementation map
12. final claim model
13. D1-D10 compatibility result
14. migration impact
15. authority consistency
16. source mutations
17. external actions
18. Public state
19. workspace/index
20. Human-review status
