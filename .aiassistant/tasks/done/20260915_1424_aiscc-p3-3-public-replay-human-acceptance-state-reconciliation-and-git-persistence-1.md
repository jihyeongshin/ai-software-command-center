# 작업지시서: P3-3 Public Replay Human acceptance state reconciliation and Git persistence

## meta

- task_id: `20260915_1424_aiscc-p3-3-public-replay-human-acceptance-state-reconciliation-and-git-persistence-1`
- created_at: `2026-09-15T14:24:00+09:00`
- work_type: `GIT_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`
- primary_semantic_owner: `P3-3 verified public release persistence / Browser Command Center`

## goal

Persist the already verified/Human-accepted Public Recorded Replay release state.

This Task is NOT a deployment Task and NOT another QA Task.

It must:

1. reconcile the five stale canonical release/submission records;
2. preserve the deployed/source bytes;
3. persist all outstanding P3-3 governance provenance plus this Human acceptance lineage in one exact local Git commit;
4. generate a Human-only final disclosure confirmation guide for the next gate.

## exact public authority

```text
Production URL:
https://aiscc-replay.pages.dev

Cloudflare project:
aiscc-replay

deployment:
Dashboard Direct Upload

source commit:
d13d261eb976fc839e78ba0878080bea93ad5201

canonical corpus root:
a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e

Executor public verification:
PASS

Human production QA:
ACCEPTED

Live:
DISABLED_FOR_INITIAL_RELEASE / NOT_RELEASED

Competition final submission:
NOT_COMPLETED
```

Do not query the public URL again in this Task.

## repository preflight

Required before substantive mutation:

```text
branch = main
HEAD = d13d261eb976fc839e78ba0878080bea93ad5201
index = empty
tracked worktree = clean
Git-visible untracked = exactly 16 authorized governance paths
```

Exact 16 current untracked path/hash identities:

- `.aiassistant/records/aiscc/cycles/20260915_1239_aiscc-p3-3-public-replay-persistence-accepted-cloudflare-deployment-entry-1.cycle.md`
  - SHA-256 `6a1fa922b800574f4736893a14c6db68add28aec676aa8cedf975ca1a95eecdd`
- `.aiassistant/records/aiscc/cycles/20260915_1310_aiscc-p3-3-human-dashboard-deployment-provided-public-verification-entry-1.cycle.md`
  - SHA-256 `fad91ccc70558d70ce476057e5a3456bf619736cf73fa3e7d98574b46321ebc9`
- `.aiassistant/records/aiscc/cycles/20260915_1343_aiscc-p3-3-public-verification-baseline-contract-blocked-retry-entry-1.cycle.md`
  - SHA-256 `0c47278311fc099802d7d50ea3c2d499245fb2b9b71c801b7ea297af9d9ac279`
- `.aiassistant/records/aiscc/cycles/20260915_1358_aiscc-p3-3-public-verification-cloudflare-1010-browser-signature-retry-entry-1.cycle.md`
  - SHA-256 `b7923ae7774a94bbad570b58994b571e639b612ad1a7d98c21a5a26aa825ad2c`
- `.aiassistant/reports/aiscc/20260915_1239_aiscc-browser-command-center-p3-3-cloudflare-pages-production-deployment-entry-handoff-1.md`
  - SHA-256 `b9e8ca56bc31b6e5f8518362c0d3d06c046f5aa7b79e6f0c7fc2b0db42d50805`
- `.aiassistant/reports/aiscc/20260915_1239_aiscc-p3-3-public-replay-persistence-browser-acceptance-1.md`
  - SHA-256 `ddf7a81905e283971166be92d3d0e37b125e83f4feed1315a8956c88b91cb354`
- `.aiassistant/reports/aiscc/20260915_1310_aiscc-browser-command-center-p3-3-public-endpoint-verification-entry-handoff-1.md`
  - SHA-256 `958fe755216fd306844603a2fc35c35b3edcf247f573fc4bb0f136ed4cb45230`
- `.aiassistant/reports/aiscc/20260915_1310_aiscc-p3-3-human-dashboard-deployment-browser-admission-1.md`
  - SHA-256 `ad053e775a01705e4f7bcc183eff4b25c237869152fede5f3a71d478c7d422df`
- `.aiassistant/reports/aiscc/20260915_1343_aiscc-browser-command-center-p3-3-public-verification-baseline-corrected-retry-entry-handoff-1.md`
  - SHA-256 `20abf9b6efea4343f76ad1239d9768b20540075acb9d8624c0fba3128bdf76f8`
- `.aiassistant/reports/aiscc/20260915_1343_aiscc-p3-3-public-verification-baseline-blocker-browser-judgment-1.md`
  - SHA-256 `39a5aca6d21dec725ed85c11c931bf04d4194f3c00550edbd0255db77a7c394c`
- `.aiassistant/reports/aiscc/20260915_1358_aiscc-browser-command-center-p3-3-browser-signature-public-verification-retry-entry-handoff-1.md`
  - SHA-256 `6634987f1323e64caa55c0958f6f2a47f09d34fd491d74e9f29e707429ef3581`
- `.aiassistant/reports/aiscc/20260915_1358_aiscc-p3-3-cloudflare-1010-verification-client-browser-judgment-1.md`
  - SHA-256 `19322e17eb4d9db55e032ab5ee63f3173e5e95ff53e0b6b433c8feab78893423`
- `.aiassistant/tasks/done/20260915_1239_aiscc-p3-3-cloudflare-pages-direct-upload-production-deployment-and-public-verification-1.md`
  - SHA-256 `4e03c333ef9503754a64b5298708183efff5d9a498ea01a4ea384f5cff1fdaec`
- `.aiassistant/tasks/done/20260915_1310_aiscc-p3-3-cloudflare-public-endpoint-byte-header-and-runtime-verification-1.md`
  - SHA-256 `c97d17f66495d4e88b36d52743cd67c6deb18f46f9b4a987ec3d9a0eb17887ed`
- `.aiassistant/tasks/done/20260915_1343_aiscc-p3-3-cloudflare-public-endpoint-verification-baseline-corrected-retry-1.md`
  - SHA-256 `96061074b8638dbb9e7f4d851a868a6d76af388d87a417ca911870bbc4ebc17d`
- `.aiassistant/tasks/done/20260915_1358_aiscc-p3-3-cloudflare-public-verification-browser-signature-corrected-retry-1.md`
  - SHA-256 `216dec859fb1c04e02357f421a3b15703a02ee6bbd9c467c372cccc907a050e4`

Any missing/extra/hash mismatch => STOP.

Do not clean/reset/restore/delete to force the baseline.

## exact tracked pre-reconciliation identities

These five tracked files MUST have these exact current hashes before editing:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
  - SHA-256 `169a1a5124f5b3b29bdfa69d1f4f073ee81ec6258801a7d0deac2a32fa617427`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
  - SHA-256 `3f5ae5cd988a63e03e6e2093ef1c925502834358fd10b7e7b9da24df9bcbd27b`
- `.aiassistant/reports/aiscc/AISCC_COMPETITION_SUBMISSION_PACKAGE.md`
  - SHA-256 `74ca883ba2c27869dbd22ef35899e0f7ca5389b847865b74283530a8cf7b77ce`
- `.aiassistant/reports/aiscc/AISCC_P3_3_PUBLIC_RELEASE_READINESS.md`
  - SHA-256 `dd1348e71612c86a23628839a6858df4262af3cefd55294d22cca33ec6c627b2`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_MANIFEST_CANDIDATE.json`
  - SHA-256 `dacfb5407d0585201cd3b708a7f0d10975369b6dbe7d1949ebd9d43cb3d147cf`

Mismatch => STOP `CANONICAL_RECONCILIATION_BASE_MISMATCH`.

## immutable tracked spot-checks

At minimum verify these accepted/decision/public bytes before and after commit:

- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
  - SHA-256 `0fe1a66a09083d67b4ea812b0a910b6b445ff2b7ef89ff814944406aaee75752`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_DISCLOSURE_REGISTER.md`
  - SHA-256 `367b2e47d766b4083f9cf652e5e316bd9abfb4a3c1c65c652b9572b97189ea17`
- `public/replay/404.html`
  - SHA-256 `a79dd0637911d851467dbf249e5f0d15438cacb3a06a6080a34826f0564fb94b`
- `public/replay/PUBLIC_REPLAY_BUILD_MANIFEST.json`
  - SHA-256 `c1de1e201d77c03b14e717ea207abdfcc969c1e6f1a738c98d8866c461c497aa`
- `public/replay/_headers`
  - SHA-256 `db28487405ec9d4a57e1a438195b78b84a00aebb150ebfffbda6a91fbb699864`
- `public/replay/assets/app.js`
  - SHA-256 `a36a76a4f952935fcbc95af5949f4575d005d8e48ed16d1e41e7db929f28d100`
- `public/replay/assets/styles.css`
  - SHA-256 `323acbb0d17776cab3b96f3de4e248dda9046bd11482b5363705e337c787d0ac`
- `public/replay/data/REPLAY_CORPUS_INDEX.json`
  - SHA-256 `c92fb81c43cef9b1c379c2df8dac967aa55f4ddae73780d31f5d51c617aa38e0`
- `public/replay/data/stockroom-s1-normal.json`
  - SHA-256 `6fb493838b0158fc9a8416146e980e027fc1091ec77e0e3504f07b4b71ed26cc`
- `public/replay/data/stockroom-s2-missing-evidence.json`
  - SHA-256 `103b98776d6e79867ea1e8ecac72a619c01a9223049434239e287381e2824201`
- `public/replay/data/stockroom-s3-policy-conflict.json`
  - SHA-256 `4ad9d71814ce5301fd48b6e40547229f6b76b16c36e69d722130eb82f03b1137`
- `public/replay/data/stockroom-s4-human-owned-claim.json`
  - SHA-256 `c6197411795760844bf74b8805476c35377117fb364423ec0a4cbf62734e3034`
- `public/replay/health.json`
  - SHA-256 `7cd565fb1b3d857af2a4f59393779f655318596701c0127efc14988d78ce7ab2`
- `public/replay/index.html`
  - SHA-256 `c8b46eb20d12323f97824320b79a0a790a477a828f3723596f6687ba41d82c6c`

Mismatch => STOP.

Run before edits:

```text
python scripts/build_public_replay.py --check
```

PASS required.

No localhost/public visual QA rerun.

## inbound lineage from this delivery

After transport, additionally authorized:

- `.aiassistant/records/aiscc/cycles/20260915_1424_aiscc-p3-3-public-replay-production-human-acceptance-final-submission-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_1424_aiscc-p3-3-public-replay-production-human-acceptance-browser-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_1424_aiscc-browser-command-center-p3-3-public-release-accepted-final-submission-prep-entry-handoff-1.md`
- active Task:
  `.aiassistant/tasks/active/20260915_1424_aiscc-p3-3-public-replay-human-acceptance-state-reconciliation-and-git-persistence-1.md`

Move active Task to exact done path before final staging:

`.aiassistant/tasks/done/20260915_1424_aiscc-p3-3-public-replay-human-acceptance-state-reconciliation-and-git-persistence-1.md`

## canonical reconciliation

Edit ONLY the following five pre-existing tracked files.

### 1. `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`

Preserve history and reconcile current projection to:

```text
P3-2:
ACCEPTED / PERSISTED / CLOSED

P3-3:
ACTIVE / FINAL_SUBMISSION_PREP

Recorded Replay local implementation:
HUMAN_PROVIDED / ACCEPTED / PERSISTED

Public Replay deployment:
DEPLOYED / PUBLIC_VERIFICATION_PASSED / HUMAN_ACCEPTED

Production URL:
https://aiscc-replay.pages.dev

Cloudflare project:
aiscc-replay

deployment method:
Dashboard Direct Upload

source commit:
d13d261eb976fc839e78ba0878080bea93ad5201

canonical corpus root:
a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e

Public Bounded Live:
NOT_RELEASED / DISABLED_FOR_INITIAL_RELEASE

Competition final submission:
NOT_COMPLETED

current next gate:
Human rights/IP/tool/model disclosure confirmation
```

Record that:
- default-UA Cloudflare 1010 was a verifier-client diagnostic;
- Chromium-compatible public verification passed;
- Human production QA passed;
- no code/redeploy rework is required.

### 2. `.aiassistant/records/aiscc/NEXT_ACTIONS.md`

Exact current sequence:

```text
1. this state reconciliation + Git persistence
2. Human final rights/IP/tool/model disclosure confirmation
3. final competition schedule/form re-verification
4. Human final competition submission
5. final submission confirmation persistence
6. judging-window public Replay availability monitoring
```

Do not include another Replay visual QA unless deployed/source bytes later change.

### 3. `.aiassistant/reports/aiscc/AISCC_P3_3_PUBLIC_RELEASE_READINESS.md`

Resolve the prior Replay deployment blockers.

Record:

```text
Recorded Replay serving:
READY_VERIFIED

Cloudflare Pages deployment:
READY_VERIFIED / DEPLOYED

public byte identity:
READY_VERIFIED

effective headers:
READY_VERIFIED

public 404:
READY_VERIFIED

Human production QA:
HUMAN_PROVIDED / ACCEPTED

Public Bounded Live:
OPTIONAL_DEFERRED / DISABLED_FOR_INITIAL_RELEASE
```

Remaining release/submission blockers MUST be narrowed to actual unresolved items such as:

- Human rights/IP confirmation;
- exact AI tool/model/use roster confirmation;
- any explicit unresolved disclosure-register item;
- final official schedule/form re-verification;
- Human final submit.

Do not keep technical Replay blockers that are now proven resolved.

### 4. `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_MANIFEST_CANDIDATE.json`

Preserve existing fields and add/update only evidence-supported release identity.

At minimum:

```text
release_status = "DEPLOYED_PUBLIC_VERIFIED_HUMAN_ACCEPTED"
platform = "Cloudflare Pages"
project_name = "aiscc-replay"
deployment_method = "Dashboard Direct Upload"
production_url = "https://aiscc-replay.pages.dev"
source_commit = "d13d261eb976fc839e78ba0878080bea93ad5201"
canonical_corpus_root_sha256 = "a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e"
public_verification = "PASSED"
human_public_qa = "ACCEPTED"
live = false
public_bounded_live = "DISABLED_FOR_INITIAL_RELEASE"
competition_submission = "NOT_COMPLETED"
```

Use current schema/style; do not invent a conflicting schema.

No account IDs/tokens/credential values.

### 5. `.aiassistant/reports/aiscc/AISCC_COMPETITION_SUBMISSION_PACKAGE.md`

Replace any stale service URL/deployment-pending wording with:

```text
service URL:
https://aiscc-replay.pages.dev

service release:
DEPLOYED / PUBLIC_VERIFICATION_PASSED / HUMAN_ACCEPTED

runtime mode:
Recorded Run Replay

Live:
not released / disabled for initial release
```

Preserve:

- P3-1 single-eligible-row limitation;
- synthetic ablation disclaimer;
- no superiority claim;
- no final-submission-completed claim.

Mark final package status:

`READY_FOR_HUMAN_DISCLOSURE_CONFIRMATION / NOT_SUBMITTED`

Do not guess Human-only disclosure answers.

## disclosure register

`.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_DISCLOSURE_REGISTER.md`

MUST remain byte-identical in this Task.

Use it as the authoritative basis for the generated Human confirmation guide.

Do not resolve Human-owned rights/tool/model items on behalf of Human.

## generated Human guide

Create in target bundle only:

`FINAL_SUBMISSION_HUMAN_CONFIRMATION_GUIDE.md`

Korean, Operation-oriented.

It must inspect the current disclosure register and submission package and list ONLY actual remaining Human confirmations.

At minimum cover, when applicable:

1. project/source ownership;
2. synthetic scenario/repository ownership;
3. excluded employer/company/customer/private material;
4. third-party dependency/license status;
5. public asset provenance;
6. Cloudflare Pages terms/use disclosure if currently recorded;
7. exact AI development tools used and how each was used;
8. runtime AI provider/model disclosure — explicitly `none for public Recorded Replay` unless canonical evidence says otherwise;
9. any unresolved register item;
10. final service URL confirmation;
11. final submission button confirmation remains separate.

Do not auto-fill uncertain Human answers.

The guide's output format should allow the Human to return `CONFIRMED / REWORK` per Operation.

## exact commit candidate

Final commit must contain exactly:

- the 16 pre-existing untracked governance paths;
- the 5 reconciled tracked canonical files;
- the new Cycle/Judgment/Handoff;
- this Task at its `tasks/done` path.

Expected changed path count:

```text
25
```

Target-bundle evidence and Human guide are ignored report artifacts and MUST NOT be included in the commit.

## commit message

Use exactly:

```text
chore(aiscc): persist verified public release state
```

## allowed actions

- exact file/hash checks;
- edit the five authorized canonical files;
- read disclosure register/submission package for Human checklist derivation;
- `git diff --check`;
- exact-path staging;
- one local commit;
- commit/tree/hash/status verification;
- builder `--check`;
- target report/export generation.

## forbidden actions

- modify `public/replay/**`;
- modify builder/tests/deployment docs;
- modify canonical Replay source corpus;
- modify README/P3-1/P3-2 accepted public docs;
- modify `DECISION_REGISTER.md`;
- modify disclosure register;
- deploy/redeploy;
- Cloudflare API/Dashboard action;
- public URL network check;
- enable Live;
- Git push/tag/release;
- competition form submission;
- claim Human disclosure confirmation.

## automatic approval blocker rule

The prior 1358 Task's five canonical writes were blocked by automatic approval review before execution.

This Task is an explicit Browser/Human-authorized persistence contract for those exact five files.

If the Executor environment still blocks any exact authorized write:

```text
STOP:
AUTOMATIC_APPROVAL_BLOCK_RECONCILIATION
```

Do not bypass with alternate tools or policy changes.

Produce minimal blocker evidence/report/export only.

## staging verification

Before commit:

- initial exact 16 untracked identities PASS;
- five tracked base hashes PASS;
- immutable spot-check hashes PASS;
- builder check PASS;
- only five authorized tracked files modified;
- new 3 lineage files exact;
- Task at done path;
- staged path set exactly 25;
- `git diff --cached --check` PASS, using the project's accepted CRLF-aware procedure where needed;
- no target/export artifact staged.

## postcommit verification

Verify:

```text
parent = d13d261eb976fc839e78ba0878080bea93ad5201
changed path count = 25
changed path set = exact allowlist
public/replay hashes unchanged
DECISION_REGISTER unchanged
disclosure register unchanged
builder --check = PASS
index = empty
tracked worktree = clean
Git-visible untracked = 0
```

Record result commit SHA.

## evidence contract

executor_required:

### `STATE_RECONCILIATION`
- exact five-file before hashes;
- bounded after content;
- no overclaim.

### `GIT_PERSISTENCE`
- exact 25-path commit;
- exact parent;
- clean terminal workspace.

### `PUBLIC_RELEASE_INTEGRITY`
- Human-reviewed deployed bytes unchanged;
- builder check PASS;
- public verification reused, not rerun.

### `FINAL_SUBMISSION_PREP`
- Human guide accurately reflects unresolved disclosure items;
- no Human-owned answer invented.

reuse_allowed:

- 1358 public verification PASS;
- Human production QA ACCEPTED;
- Cloudflare Dashboard deployment evidence;
- local Human QA;
- P3-1/P3-2 accepted provenance.

human_owned:

- rights/IP/tool/model confirmations;
- official form review;
- final competition submission.

not_required:

- network;
- Cloudflare;
- visual QA;
- deployment;
- provider/DB/Live.

forbidden:

- redeploy;
- source/public artifact mutation;
- disclosure auto-acceptance;
- final submit.

proof_non_substitution:

- public verification != Human rights clearance;
- Human production QA != competition submission;
- Git persistence != public availability monitoring;
- AI tool draft roster != Human-confirmed roster;
- service URL availability != final submit confirmation.

## expected terminal candidate

```text
PERSISTENCE_CANDIDATE / FINAL_HUMAN_DISCLOSURE_GATE
```

Do not declare:

- P3-3 closed;
- competition submitted;
- disclosure confirmed.

## target bundle

`.aiassistant/reports/target/20260915_1424_aiscc-p3-3-public-replay-human-acceptance-state-reconciliation-and-git-persistence-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PRECOMMIT_INVENTORY.json`
- `PUBLIC_RELEASE_ACCEPTANCE.json`
- `RECONCILIATION_DIFF.json`
- `STAGED_COMMIT_MANIFEST.json`
- `POSTCOMMIT_VERIFICATION.json`
- `TERMINAL_WORKSPACE.json`
- `FINAL_SUBMISSION_HUMAN_CONFIRMATION_GUIDE.md`
- changed five canonical records preserving relative paths
- new Cycle/Judgment/Handoff/Task-done preserving relative paths
- `REMOVED_FILES.md` only if an actual project deletion exists; none expected.

Terminal ZIP:

`.aiassistant/reports/target/20260915_1424_aiscc-p3-3-public-replay-human-acceptance-state-reconciliation-and-git-persistence-1.zip`

## final response

1. result
2. result commit SHA / parent
3. exact changed path count
4. reconciled public state
5. immutable public artifact hashes
6. disclosure register unchanged
7. Human confirmation guide status
8. terminal workspace
9. target bundle + ZIP
10. remaining Human/final-submission actions
