# 작업지시서: P3-3 Replay-first public release readiness and submission package freeze

## meta

- task_id: `20260915_1009_aiscc-p3-3-replay-first-public-release-readiness-and-submission-package-freeze-1`
- created_at: `2026-09-15T10:09:27+09:00`
- work_type: `RELEASE_SUBMISSION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`
- primary_semantic_owner: `P3-3 Public Release and Competition Submission / Browser Command Center`

## current authority

```text
P2:
ACCEPTED / CLOSED

P3-1 Comparative Evaluation:
ACCEPTED / CLOSED

P3-2 Public Repository Documentation:
HUMAN_PROVIDED / ACCEPTED / PERSISTED / CLOSED

P3-3:
ENTRY_AUTHORIZED
```

Expected repository baseline:

```text
branch:
main

HEAD:
17fcd337a8bc1410e230a7c18195ac3d3006b417

parent:
82bc047b79cf496280d1b3df6a113f652629a6f5

tracked/index/Git-visible workspace:
clean
```

If current HEAD or workspace differs, do not silently normalize it. Apply the mandatory-stop rules below.

## official competition facts supplied by Browser re-verification

Browser Command Center re-verified the official Wanted `AI Championship 2026` landing/FAQ on `2026-09-15`.

Treat these as current Browser-supplied external facts for this Task:

```text
participant registration deadline:
2026-09-18 23:59:59 KST

final task submission deadline:
2026-09-20 23:59:59 KST

preliminary judging / voting:
2026-09-21 through 2026-10-05

submission:
final submit required; temporary save is not submission

service:
actually implemented/deployed service link required

required disclosure:
problem addressed
AI usage
major AI tools used

availability:
service link must be reachable during judging

edit freeze:
editable through 2026-09-20 deadline;
after deadline read-only / no further submission edits
```

Do not browse the competition site in this Task unless an exact contradiction in repository canonical requires a freshness recheck. Final submission Task must recheck the official page again immediately before Human final submit.

## goal

Freeze the exact release and submission package required to move from current repository state to a truthful public competition release.

This Task MUST answer:

1. What exact public application surfaces exist in current source?
2. Which of those surfaces are buildable/deployable now?
3. What deployment platform/config files already exist?
4. What is required to make `Recorded Run Replay` publicly accessible?
5. Is `PUBLIC_BOUNDED_LIVE` releasable under the accepted guard contract now?
6. If Live is not fully evidenced, what exact `DISABLED` behavior/fallback is release-safe?
7. What license/IP/data/tool/provider disclosures are required for submission?
8. What exact competition submission copy can be frozen now?
9. What credentials/Human actions are required for deployment and final submit?
10. What exact next bounded Task should perform public deployment?

## required authoritative context

Read current repository canonical:

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- `.aiassistant/records/command-center/NEXT_ACTION_SELECTION_RUBRIC.md`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
- `.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md`
- `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
- `.aiassistant/rules/AISCC_ARCHITECTURE.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_DOCUMENTATION_TRUTH_MAP.md`
- `.aiassistant/records/aiscc/cycles/20260915_1009_aiscc-p3-2-final-persistence-acceptance-p3-3-entry-authorization-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_1009_aiscc-p3-2-final-persistence-browser-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260915_1009_aiscc-browser-command-center-p3-2-closed-p3-3-release-submission-entry-handoff-1.md`
- `README.md`
- `docs/AISCC_COMPARATIVE_EVALUATION.md`
- `docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md`

Then inspect only the current-source files needed to answer release readiness:

- root build/dependency manifests;
- deployment/container/process files;
- frontend/static/public entrypoints;
- Replay API/storage/public-page implementation;
- public/runtime configuration schema;
- security/budget/provider guard configuration;
- license/NOTICE/dependency metadata;
- existing environment example files containing names only, never secret values;
- exact release docs already linked by README.

Do not bulk-read unrelated application history.

## current public-runtime boundary

The release baseline is:

```text
competition_runtime_mode:
PUBLIC_REPLAY_WITH_BOUNDED_LIVE

default public mode:
RECORDED_RUN_REPLAY

optional:
PUBLIC_BOUNDED_LIVE

public free-form task:
FORBIDDEN

external repository URL/upload:
FORBIDDEN

public arbitrary shell/network:
FORBIDDEN
```

Current release status:

```text
Recorded Replay corpus:
CANONICAL / PERSISTED

Public Replay deployment:
NOT_COMPLETED

Public Bounded Live:
NOT_RELEASED
```

Do not change those statuses in this Task.

## Replay-first invariant

`RECORDED_RUN_REPLAY` is the submission-critical baseline.

The Task must determine whether the current source can be deployed so that:

- public project/Replay pages require zero provider/LLM inference;
- Replay is read-only;
- stored event/evidence/judgment/Cycle provenance is preserved;
- Recorded Replay is visibly labeled as recorded, not current Live AI;
- failure to start/use Live cannot break Replay browsing;
- no private/company/customer source is exposed.

Missing optional Live readiness MUST NOT block a Replay-only release if Replay itself is safely deployable.

## bounded Live release gate

Classify public Live as exactly one of:

```text
ENABLE_CANDIDATE
DISABLED_FOR_INITIAL_RELEASE
BLOCKED_BY_CONTRACT_CONFLICT
```

`ENABLE_CANDIDATE` is allowed only if current implementation/config evidence proves all applicable guards:

- fixed synthetic repository;
- allowlisted scenarios;
- no free-form task;
- no external repository URL/upload;
- no arbitrary public shell/network;
- public/private permission-profile separation;
- server-fixed provider/model;
- exact call/retry/time/token caps;
- exact daily/global/currency application budget caps;
- provider hard-spend guard where supported or explicit documented absence/compensating control;
- fail-closed budget/availability admission;
- truthful Live error state;
- Replay remains available on Live failure/budget exhaustion;
- no secret/private context exposure;
- abuse/throttling/idempotency controls required by the accepted runtime boundary.

If any required guard is not evidenced, classify Live:

`DISABLED_FOR_INITIAL_RELEASE`

and specify exact UI/API behavior needed to keep it disabled truthfully.

Do not implement missing Live features in this Task.

## required outputs

### 1. Release readiness baseline

Create:

`.aiassistant/reports/aiscc/AISCC_P3_3_PUBLIC_RELEASE_READINESS.md`

Required sections:

1. status / source identity
2. competition deadline/current official-fact snapshot
3. public surface inventory
4. current build/run/deploy topology
5. Recorded Replay deployability matrix
6. public data/sanitization boundary
7. security/runtime guard matrix
8. bounded Live release classification
9. provider/budget configuration readiness
10. availability/recovery/fallback requirements
11. credentials/Human-owned action inventory
12. blockers with exact severity
13. minimum release path
14. next deployment Task contract
15. post-deployment verification requirements
16. judging-window operational obligations

Every readiness item must be one of:

```text
READY_VERIFIED
READY_WITH_HUMAN_CREDENTIAL
BLOCKED_REQUIRED
OPTIONAL_DEFERRED
NOT_APPLICABLE
```

### 2. Competition submission package

Create:

`.aiassistant/reports/aiscc/AISCC_COMPETITION_SUBMISSION_PACKAGE.md`

Draft only evidence-supported fields:

- project/service name
- one-line description
- problem
- solution
- AI usage
- major AI tools and how each was used
- public service link: `PENDING_DEPLOYMENT` unless already proven public
- public repository link: only if exact current remote/public accessibility is verified without exposing private credentials
- core differentiator
- self-dogfooding evidence
- comparative evaluation summary with one-row limitation
- current limitations
- license/IP/data provenance summary
- Recorded Replay vs Live explanation
- reviewer usage instructions
- required Human-only fields/confirmation
- final-submit checklist

Do not fabricate form fields not supported by the official facts or current repository.

### 3. License/IP/tool disclosure register

Create:

`.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_DISCLOSURE_REGISTER.md`

At minimum record:

- repository/project ownership status;
- excluded employer/company/customer materials;
- synthetic/recorded scenario source ownership;
- third-party libraries/licenses;
- copied/generated public assets and provenance;
- external API/provider terms relevant to release;
- AI tools actually used to create/develop the submitted project;
- runtime model/provider used by product, if applicable and verified;
- unresolved license/IP/terms items.

Do not include secret values or private account IDs.

### 4. Release manifest candidate

Create:

`.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_MANIFEST_CANDIDATE.json`

Include only names/identities, no secret values:

```text
source_commit
release_mode
public_surfaces
required_build_commands
required_start_commands
deployment_targets
environment_variable_names
secret_names
database/storage dependencies
Replay data dependencies
Live enabled/disabled classification
budget_guard_config names
health/readiness paths if present
rollback/fallback mode
required Human credentials/actions
blocked items
```

All commands must be verified from current source. Do not guess.

### 5. Command Center records

Because P3-2 closed and submission critical path changed, update current canonical records if their current repository bytes are stale:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`

Required target state:

```text
P3-2 = ACCEPTED / PERSISTED / CLOSED
P3-3 = ACTIVE / RELEASE_READINESS

current HEAD baseline = 17fcd337a8bc1410e230a7c18195ac3d3006b417
```

Update `DECISION_REGISTER.md` only if this Task makes a new release decision supported by evidence, for example:

- `Replay-first initial release`;
- `Live DISABLED_FOR_INITIAL_RELEASE`.

Do not add speculative decisions.

## source inspection / command allowance

Allowed:

- local repository file reads;
- bounded file inventory;
- current Git metadata / remote name inspection;
- local build/dependency/config static inspection;
- local syntax/static validation;
- local build command only if it is deterministic, credential-free, network-free or dependency-resolved without expanding scope;
- Docker/container config inspection without starting external services;
- exact environment-variable NAME extraction;
- license/dependency metadata inspection;
- exact public URL strings already present in current tracked configuration.

Not allowed by default:

- credentialed cloud login;
- deployment;
- DNS/domain mutation;
- final public endpoint publication;
- provider API call;
- paid inference;
- creating provider budgets/caps;
- database migration;
- production data access;
- final competition submission;
- Git push/tag/release;
- changing product/runtime/source merely to satisfy readiness.

If a credentialed read-only cloud check is essential to distinguish `READY_WITH_HUMAN_CREDENTIAL` from `BLOCKED_REQUIRED`, stop and request the specific Human-owned evidence rather than authenticating implicitly.

## network boundary

No general web research is required in this Executor Task.

Browser Command Center already supplied the current official competition facts.

Do not use network access except an exact public URL accessibility check that:
- requires no credentials;
- is already named by tracked current configuration;
- performs no mutation;
- is necessary to classify an already-existing public endpoint.

If no public URL is currently configured, do not search for one.

## evidence contract

executor_required:

1. `STATIC_SOURCE / RELEASE_READINESS`
   - exact current source/deploy/config inventory;
   - Replay release requirements;
   - Live guard matrix;
   - build/start command provenance;
   - environment/secret names only.

2. `PUBLIC_PROVENANCE`
   - accepted public docs/P2 Replay/P3-1 facts carried without overstatement;
   - disclosure register maps public claims to current source/provenance.

3. `SECURITY_CONFORMANCE`
   - no private source/secret/body leakage;
   - public/private profile separation;
   - Live guard requirement classification;
   - secret names may be documented; values forbidden.

4. `SUBMISSION_CONFORMANCE`
   - current official deadline/final-submit/service-link/AI-tool disclosure facts preserved;
   - submission copy contains no unsupported release claim;
   - service URL remains `PENDING_DEPLOYMENT` unless exact public accessibility is proven.

reuse_allowed:

- P2 accepted Replay corpus/provenance;
- P2-4 self-dogfooding;
- P3-1 accepted comparative evaluation;
- P3-2 accepted public documentation;
- Browser 2026-09-15 official competition re-verification.

human_owned:

- cloud/provider account access;
- secret provisioning;
- billing/budget approval;
- domain/DNS ownership;
- final Live enable decision when credentials/cost are involved;
- final public deployment approval where provider UI requires Human action;
- legal/IP resolution for ambiguous rights;
- final competition submission.

not_required:

- public deployment in this Task;
- final competition submission;
- broad end-to-end public availability test before deployment exists;
- paid provider inference.

forbidden:

- secret/token values in artifacts;
- company/client/private source;
- arbitrary runtime feature implementation;
- unbounded Live;
- Git push/deploy/submit;
- status claim `RELEASED` without external evidence.

proof_non_substitution:

- deploy config exists != deployed service;
- local build PASS != public availability;
- persisted Replay corpus != public Replay deployment;
- security design != runtime guard implementation;
- budget config name != active spend guard;
- local Git commit != public repository accessibility;
- draft submission copy != final submission;
- Human credential availability != credential use;
- optional Live readiness != submission readiness.

## required classification behavior

A missing optional Live guard:

```text
Live -> DISABLED_FOR_INITIAL_RELEASE
```

not automatically:

```text
release -> BLOCKED
```

A missing Replay/public-page deployment prerequisite:

```text
BLOCKED_REQUIRED
```

because a deployed service link is submission-critical.

A missing final Human credential:

```text
READY_WITH_HUMAN_CREDENTIAL
```

only if all non-secret technical prerequisites are otherwise proven.

## Human review focus

After Executor submission, Browser/Human must decide:

1. Is Replay technically ready for deployment?
2. Are any blockers truly release-critical?
3. Is Live safely `ENABLE_CANDIDATE` or should it be disabled initially?
4. Are IP/license/tool disclosures complete enough to proceed?
5. Is the submission copy truthful and compelling within accepted claim limits?
6. What exact credentials/provider actions must Human supply?
7. Is the next Task ready to perform deployment without mixing final submission?

## mandatory stop

Stop substantive work if:

- HEAD is not `17fcd337a8bc1410e230a7c18195ac3d3006b417` or workspace contains unexplained Git-visible dirt;
- required canonical public-runtime/security baseline is missing;
- current source contradicts accepted public docs in a way that changes a load-bearing public claim;
- private/company/customer material is encountered;
- a secret value must be read to proceed;
- deployment mutation is required to determine readiness;
- final competition submission would be required;
- scope expansion into product implementation is required.

After stop, create minimal blocker evidence/report/export only.

## scope

Allowed substantive changes:

- the four P3-3 readiness/submission/disclosure/manifest files above;
- CURRENT_STATE_SUMMARY / NEXT_ACTIONS when stale;
- DECISION_REGISTER only for evidence-supported new release decision;
- Task lifecycle/report/export.

Forbidden substantive changes:

- README/public comparative summary/truth map;
- product/runtime/test code;
- deployment source/config;
- Replay corpus;
- provider/budget config;
- DB/schema;
- security/orchestration semantics;
- P3-1 evidence;
- competition site/form.

No Git commit in this Task unless a later explicit persistence Task authorizes it.

## expected terminal candidate

One of:

```text
RELEASE_READINESS_CANDIDATE / HUMAN_PENDING
BLOCKED_RELEASE_PREREQUISITE
```

Executor must not declare:
- public deployment complete;
- final submission complete;
- P3-3 closed.

## export bundle

Target:

`.aiassistant/reports/target/20260915_1009_aiscc-p3-3-replay-first-public-release-readiness-and-submission-package-freeze-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `.aiassistant/reports/aiscc/AISCC_P3_3_PUBLIC_RELEASE_READINESS.md`
- `.aiassistant/reports/aiscc/AISCC_COMPETITION_SUBMISSION_PACKAGE.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_DISCLOSURE_REGISTER.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_MANIFEST_CANDIDATE.json`
- changed command-center current records, if any
- bounded release-readiness validation evidence
- `REMOVED_FILES.md` only if project deletion exists

Terminal ZIP:

`.aiassistant/reports/target/20260915_1009_aiscc-p3-3-replay-first-public-release-readiness-and-submission-package-freeze-1.zip`

## final response format

1. result
2. source identity
3. Replay readiness classification
4. Live release classification
5. release-critical blockers
6. deployment targets/config provenance
7. license/IP/tool disclosure status
8. competition submission package status
9. Human-owned credentials/actions
10. changed canonical records
11. target bundle + ZIP
12. human verification
13. exact next deployment Task recommendation
