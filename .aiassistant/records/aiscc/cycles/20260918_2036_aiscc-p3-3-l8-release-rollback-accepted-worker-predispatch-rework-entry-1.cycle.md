# AISCC Cycle Record

## meta

- cycle_id: `20260918_2036_aiscc-p3-3-l8-release-rollback-accepted-worker-predispatch-rework-entry-1`
- date: `2026-09-18T20:36:00+09:00`
- primary_semantic_owner: `Browser Command Center`
- affected_areas: `P3-3 / L8 / failed release smoke / worker pre-dispatch`
- work_type: `L8_RELEASE_ROLLBACK_ACCEPTANCE_REWORK_ENTRY`
- predecessor_task: `20260918_1919_aiscc-p3-3-l8-public-live-final-activation-and-smoke-1`
- reviewed_result_zip_sha256: `962dcf3cc9129fd218ca9ff8d5057d1bff3e61859e0645c94c6df42bf1e78d4d`
- repository_main_at_review: `6c5251fcfd78e01fa1a881f1bfd14b8af5d4bc9c`
- result_status: `ACCEPTED_SAFE_ROLLBACK / RELEASE_NOT_ACCEPTED`
- public_admission: `DISABLED`
- public_live: `NOT_RELEASED`
- replay: `PUBLIC / RETAINED`

## independent result-bundle review

Browser independently verified:

- ZIP integrity: PASS;
- archive entries: 22 including root directory;
- inventory rows: 20;
- all 20 inventory SHA-256 and byte counts: PASS;
- `TASK.md` == canonical done Task == originally issued 1919 Task bytes: PASS;
- bounded scan found no OpenAI key, PostgreSQL DSN, private key, read capability or HMAC secret;
- release result: `RELEASE_ROLLED_BACK_TO_REPLAY_ONLY`.

## GitHub review

GitHub `main` independently resolves to:

`6c5251fcfd78e01fa1a881f1bfd14b8af5d4bc9c`

Verified lineage:
- release frontend commit: `918f5e8ad62038b967c982ef5aa860d1785f5742`
- rollback frontend commit: `57c20374c2c2799aa354c43309b1515a3d13fe3f`
- governance/export commit: `6c5251fcfd78e01fa1a881f1bfd14b8af5d4bc9c`

Comparison of entry `0e9feab...` to rollback `57c20374...` has no remaining product-file diff. Current repository frontend is back to:
- `live-config.json`: enabled false / api_origin null
- CSP `connect-src 'self'`
- Replay corpus root unchanged.

## accepted runtime finding

The release sequence correctly proceeded fail-closed through ingress, campaign, frontend deploy and final enablement, then executed exactly one public smoke run.

Smoke facts admitted:
- one POST only;
- HTTP 201 `ADMITTED`;
- one retained public run;
- start request reached `BOUND`;
- WorkRun/execution attempt reached `RUNNING`;
- worker acquired one claim;
- no execution operation was created;
- no public dispatch/provider-request row was created;
- real provider sends attributable to the smoke: 0;
- no UNKNOWN provider/send outcome;
- claim expired and was recovered/released `LIVE_UNAVAILABLE`;
- no replacement run or retry was created.

The smoke failed materially because the run remained `ADMITTED` beyond its 90-second deadline. The authorized rollback was therefore the correct terminal behavior for the 1919 Task.

## final safety state admitted

- control disabled;
- Public Live not released;
- ingress public domain removed;
- edge-trust removed;
- Cloudflare restored to Replay-only;
- worker provider key retained worker-only/sealed;
- Replay four scenarios unchanged.

The retained failed run/campaign/reservation/slot accounting is evidence and was not destructively erased.

## Browser source finding / root-cause hypothesis

Independent current-source review found a strong pre-dispatch hypothesis matching the durable evidence:

`_execute_production_claim()` constructs the Stockroom dispatcher before `AgentExecutionService.execute()` creates the first execution operation.

`PublicStockroomComposition.dispatcher()` does this when no runner is injected:

```text
shutil.which("docker")
-> if absent:
PUBLIC_LIVE_STOCKROOM_DOCKER_REQUIRED
```

The Railway worker composition supplies `stockroom_runner=None`.

Therefore a Docker-unavailable hosted worker would fail exactly at the observed boundary:
claim acquired -> no operation -> no provider send.

This is a **high-confidence hypothesis, not yet admitted runtime root-cause fact**, because the 1919 worker loop swallowed the exception and retained logs do not expose a safe exact failure code.

## governance finding

Current GitHub main also tracks the 1919 `.aiassistant/reports/target/...` export subtree in commit `6c5251fc...`.

That conflicts with:
- `.gitignore`: `.aiassistant/reports/target/`
- `IDE_EXECUTOR_REPORT_EXPORT.md`: target bundles are temporary / Git ignored.

The result evidence remains valid, but the tracked target subtree must be removed from canonical Git tracking in the successor Task.

## judgment

```text
1919 release attempt:
NOT_ACCEPTED

1919 rollback/safety handling:
ACCEPTED

Public Live:
NOT_RELEASED

Replay:
PUBLIC / RETAINED

Next action:
worker pre-dispatch root-cause confirmation + narrow rework
```
