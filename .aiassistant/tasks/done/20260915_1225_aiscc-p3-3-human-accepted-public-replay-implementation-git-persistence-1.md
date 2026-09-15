# 작업지시서: P3-3 Human-accepted Public Replay implementation Git persistence

## meta

- task_id: `20260915_1225_aiscc-p3-3-human-accepted-public-replay-implementation-git-persistence-1`
- created_at: `2026-09-15T12:25:36+09:00`
- work_type: `GIT_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`
- primary_semantic_owner: `P3-3 Human-accepted Public Replay persistence / Browser Command Center`

## goal

Persist the Human-accepted local Public Recorded Replay implementation and P3-3 governance state in one exact local Git commit.

Do not deploy, push, or re-author the accepted public surface.

## baseline

Required before substantive mutation:

```text
branch = main
HEAD = 17fcd337a8bc1410e230a7c18195ac3d3006b417
index = empty
tracked modified paths = exactly 3
Git-visible untracked paths = exactly 28
total Git-visible changed paths = exactly 31
```

Exact 31-path preflight inventory:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
  - SHA-256 `21e36b6381c873135fe3f622056b25a19bb2b14425ace9ab6b9fbcb3d918b302`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
  - SHA-256 `0fe1a66a09083d67b4ea812b0a910b6b445ff2b7ef89ff814944406aaee75752`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
  - SHA-256 `d899c1f76e283141e54b96c4ee9d1dbe12dc49eee315a58e6ec958532d1a5204`
- `.aiassistant/records/aiscc/cycles/20260915_1009_aiscc-p3-2-final-persistence-acceptance-p3-3-entry-authorization-1.cycle.md`
  - SHA-256 `5c54ad4d48759de1034fd1f584df08ac32bad674d0f3676fa73bf7cc5a0b65f1`
- `.aiassistant/records/aiscc/cycles/20260915_1047_aiscc-p3-3-readiness-blocked-public-replay-implementation-entry-1.cycle.md`
  - SHA-256 `3c7e6e8c68c763119d1360c9d2bf691004240aa5985278ad0031564e097f5ee6`
- `.aiassistant/reports/aiscc/20260915_1009_aiscc-browser-command-center-p3-2-closed-p3-3-release-submission-entry-handoff-1.md`
  - SHA-256 `2381e5415d08e49552cb782c53eab23be0a0241441ba74895f8f05588e90b591`
- `.aiassistant/reports/aiscc/20260915_1009_aiscc-p3-2-final-persistence-browser-acceptance-1.md`
  - SHA-256 `bf26ac731e95ab6cf8c0da8246b3b8b8e3e4e810adc131b231e533c8d0934ebc`
- `.aiassistant/reports/aiscc/20260915_1047_aiscc-browser-command-center-p3-3-public-replay-static-implementation-entry-handoff-1.md`
  - SHA-256 `f9f22d5816b1491e0be046b4d8d2e8f1fc4a455a577adc6eff8d138e3ba91d5c`
- `.aiassistant/reports/aiscc/20260915_1047_aiscc-p3-3-readiness-blocker-browser-acceptance-and-hosting-authority-correction-1.md`
  - SHA-256 `2a4c3b2c369910503efc28dc829ac9d46ea054cc58046223cb75427384c20d6c`
- `.aiassistant/reports/aiscc/AISCC_COMPETITION_SUBMISSION_PACKAGE.md`
  - SHA-256 `74ca883ba2c27869dbd22ef35899e0f7ca5389b847865b74283530a8cf7b77ce`
- `.aiassistant/reports/aiscc/AISCC_P3_3_PUBLIC_RELEASE_READINESS.md`
  - SHA-256 `dd1348e71612c86a23628839a6858df4262af3cefd55294d22cca33ec6c627b2`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_DISCLOSURE_REGISTER.md`
  - SHA-256 `367b2e47d766b4083f9cf652e5e316bd9abfb4a3c1c65c652b9572b97189ea17`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_MANIFEST_CANDIDATE.json`
  - SHA-256 `dacfb5407d0585201cd3b708a7f0d10975369b6dbe7d1949ebd9d43cb3d147cf`
- `.aiassistant/tasks/done/20260915_1009_aiscc-p3-3-replay-first-public-release-readiness-and-submission-package-freeze-1.md`
  - SHA-256 `e366225623a2e749693f6cc023a97d71a74be5de7e6943248a6e82e55a00585c`
- `.aiassistant/tasks/done/20260915_1047_aiscc-p3-3-public-recorded-replay-static-surface-and-cloudflare-pages-prerequisite-implementation-1.md`
  - SHA-256 `48b08b92c54e3a06ac4d6bc6126c4c40a57db4f5aba2fb132be08e0385e45593`
- `docs/AISCC_PUBLIC_REPLAY_DEPLOYMENT.md`
  - SHA-256 `d6bf858e445a162911d2e7bb84eee885645421a056dc0abceaaa68020bbdbdf7`
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
- `scripts/build_public_replay.py`
  - SHA-256 `c46a3739ea2a05f5a0d709f2be0f6e2801908443fa0b606904a2a89dd72b4187`
- `tests/unit/public_replay_ui.cjs`
  - SHA-256 `dc2c92076db334c0e99b447ad966fac66512aea089b720b4bcf2d27d2534aeca`
- `tests/unit/test_public_replay_build.py`
  - SHA-256 `3e0e3361e7e4a11ba6cb9a9c5b16e02e6d182cf54cde102d738044436e5e61d7`

Any path/hash mismatch, extra Git-visible dirt, staged path, branch/HEAD mismatch, or missing path => STOP.

Do not clean/reset/restore/delete to force the precondition.

## inbound lineage from this delivery

After exact delivery transport, these are additionally authorized:

- `.aiassistant/records/aiscc/cycles/20260915_1225_aiscc-p3-3-public-replay-human-qa-accepted-persistence-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_1225_aiscc-p3-3-public-replay-human-qa-browser-acceptance-1.md`
- `.aiassistant/reports/aiscc/20260915_1225_aiscc-browser-command-center-p3-3-public-replay-qa-accepted-persistence-entry-handoff-1.md`
- active Task:
  `.aiassistant/tasks/active/20260915_1225_aiscc-p3-3-human-accepted-public-replay-implementation-git-persistence-1.md`

Move the Task to:

`.aiassistant/tasks/done/20260915_1225_aiscc-p3-3-human-accepted-public-replay-implementation-git-persistence-1.md`

before final staging/commit according to project lifecycle rules.

## Human-accepted immutable existing bytes

Except for the two projection files explicitly permitted below, every pre-existing changed path MUST remain byte-identical to the preflight inventory.

Exact immutable set:

- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
  - SHA-256 `0fe1a66a09083d67b4ea812b0a910b6b445ff2b7ef89ff814944406aaee75752`
- `.aiassistant/records/aiscc/cycles/20260915_1009_aiscc-p3-2-final-persistence-acceptance-p3-3-entry-authorization-1.cycle.md`
  - SHA-256 `5c54ad4d48759de1034fd1f584df08ac32bad674d0f3676fa73bf7cc5a0b65f1`
- `.aiassistant/records/aiscc/cycles/20260915_1047_aiscc-p3-3-readiness-blocked-public-replay-implementation-entry-1.cycle.md`
  - SHA-256 `3c7e6e8c68c763119d1360c9d2bf691004240aa5985278ad0031564e097f5ee6`
- `.aiassistant/reports/aiscc/20260915_1009_aiscc-browser-command-center-p3-2-closed-p3-3-release-submission-entry-handoff-1.md`
  - SHA-256 `2381e5415d08e49552cb782c53eab23be0a0241441ba74895f8f05588e90b591`
- `.aiassistant/reports/aiscc/20260915_1009_aiscc-p3-2-final-persistence-browser-acceptance-1.md`
  - SHA-256 `bf26ac731e95ab6cf8c0da8246b3b8b8e3e4e810adc131b231e533c8d0934ebc`
- `.aiassistant/reports/aiscc/20260915_1047_aiscc-browser-command-center-p3-3-public-replay-static-implementation-entry-handoff-1.md`
  - SHA-256 `f9f22d5816b1491e0be046b4d8d2e8f1fc4a455a577adc6eff8d138e3ba91d5c`
- `.aiassistant/reports/aiscc/20260915_1047_aiscc-p3-3-readiness-blocker-browser-acceptance-and-hosting-authority-correction-1.md`
  - SHA-256 `2a4c3b2c369910503efc28dc829ac9d46ea054cc58046223cb75427384c20d6c`
- `.aiassistant/reports/aiscc/AISCC_COMPETITION_SUBMISSION_PACKAGE.md`
  - SHA-256 `74ca883ba2c27869dbd22ef35899e0f7ca5389b847865b74283530a8cf7b77ce`
- `.aiassistant/reports/aiscc/AISCC_P3_3_PUBLIC_RELEASE_READINESS.md`
  - SHA-256 `dd1348e71612c86a23628839a6858df4262af3cefd55294d22cca33ec6c627b2`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_DISCLOSURE_REGISTER.md`
  - SHA-256 `367b2e47d766b4083f9cf652e5e316bd9abfb4a3c1c65c652b9572b97189ea17`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_RELEASE_MANIFEST_CANDIDATE.json`
  - SHA-256 `dacfb5407d0585201cd3b708a7f0d10975369b6dbe7d1949ebd9d43cb3d147cf`
- `.aiassistant/tasks/done/20260915_1009_aiscc-p3-3-replay-first-public-release-readiness-and-submission-package-freeze-1.md`
  - SHA-256 `e366225623a2e749693f6cc023a97d71a74be5de7e6943248a6e82e55a00585c`
- `.aiassistant/tasks/done/20260915_1047_aiscc-p3-3-public-recorded-replay-static-surface-and-cloudflare-pages-prerequisite-implementation-1.md`
  - SHA-256 `48b08b92c54e3a06ac4d6bc6126c4c40a57db4f5aba2fb132be08e0385e45593`
- `docs/AISCC_PUBLIC_REPLAY_DEPLOYMENT.md`
  - SHA-256 `d6bf858e445a162911d2e7bb84eee885645421a056dc0abceaaa68020bbdbdf7`
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
- `scripts/build_public_replay.py`
  - SHA-256 `c46a3739ea2a05f5a0d709f2be0f6e2801908443fa0b606904a2a89dd72b4187`
- `tests/unit/public_replay_ui.cjs`
  - SHA-256 `dc2c92076db334c0e99b447ad966fac66512aea089b720b4bcf2d27d2534aeca`
- `tests/unit/test_public_replay_build.py`
  - SHA-256 `3e0e3361e7e4a11ba6cb9a9c5b16e02e6d182cf54cde102d738044436e5e61d7`

Any changed hash in that immutable set => STOP `ACCEPTED_IMPLEMENTATION_HASH_MISMATCH`.

This specifically protects the Human-reviewed:

- `public/replay/**`;
- builder;
- tests;
- deployment documentation;
- release/readiness/submission/disclosure records;
- deployment decision;
- prior 1009/1047 lineage.

## permitted projection edits

Only these two existing files may change from their preflight hashes:

### `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`

Narrowly reconcile:

```text
P3-3 = ACTIVE

Recorded Replay local implementation =
HUMAN_PROVIDED / ACCEPTED / PERSISTENCE_PENDING

Public Replay deployment =
NOT_COMPLETED

Public Bounded Live =
NOT_RELEASED / DISABLED_FOR_INITIAL_RELEASE

current action =
Git persistence of accepted local Replay implementation
```

Preserve historical records; do not rewrite old Cycle truth.

### `.aiassistant/records/aiscc/NEXT_ACTIONS.md`

Project exact order:

```text
1. accepted implementation Git persistence
2. bounded Cloudflare Pages deployment
3. public endpoint / effective header / 404 / artifact-identity verification
4. final competition submission
```

Do not start any of those later actions in this Task.

### `DECISION_REGISTER.md`

MUST remain byte-identical to preflight SHA.

No new decision is needed: Replay-first + Live-disabled release direction is already recorded.

## exact commit candidate

Commit exactly:

- all 31 preflight Git-visible paths;
- three inbound canonical Human-QA Cycle/Judgment/Handoff files;
- this Task at its `tasks/done` path.

Expected changed path count:

```text
35
```

No other path is authorized.

## commit message

Use exactly:

```text
feat(aiscc): persist accepted public replay
```

## allowed actions

- exact SHA-256 calculation;
- `git status --porcelain=v1 --untracked-files=all`;
- narrow edits to the two projection files only;
- `git diff --check`;
- `git add -- <exact allowlist>`;
- `git diff --cached --name-only`;
- `git diff --cached --check`;
- one local `git commit`;
- `git show`;
- `git diff-tree`;
- post-commit hashes/status;
- report/export generation.

## forbidden

- change `public/replay/**`;
- change builder/tests/deployment doc;
- change canonical Replay source corpus;
- change P3-3 readiness/submission/disclosure/manifest records;
- change DECISION_REGISTER;
- change README/P3-1/P3-2 accepted public docs;
- product/private Command Center changes;
- provider/Railway/OpenAI work;
- Cloudflare account/project action;
- Git push/tag/release;
- deployment;
- network/provider API call;
- final competition submission;
- reset/restore/clean/amend/rebase.

## precommit verification

Before commit verify:

1. branch/HEAD exact;
2. initial index empty;
3. exact 31-path preflight set/hash;
4. immutable existing set hash unchanged after projection edits;
5. only CURRENT_STATE_SUMMARY/NEXT_ACTIONS changed beyond preflight bytes;
6. three inbound Human-QA authority files exact;
7. Task is at exact done path;
8. staged path set exactly 35;
9. no ignored target/report artifact staged;
10. `git diff --cached --check` PASS.

## postcommit verification

After commit verify:

```text
parent = 17fcd337a8bc1410e230a7c18195ac3d3006b417
changed path count = 35
changed path set = exact authorized set
immutable accepted implementation hashes unchanged
DECISION_REGISTER hash unchanged
public/replay corpus/public assets hashes unchanged
index = empty
tracked worktree = clean
Git-visible untracked = 0
```

Also run:

```text
python scripts/build_public_replay.py --check
```

This is a no-mutation integrity check only.

Do not restart Human QA.

## evidence contract

executor_required:

- `STATIC_SOURCE / HUMAN_ACCEPTED_BYTES`
  - exact preflight hashes and immutable-set preservation;
- `GIT_PERSISTENCE`
  - exact staged/commit path set, parent, result commit and clean workspace;
- `CONFORMANCE`
  - only two permitted projection edits;
  - no deployment/push/network/provider action;
- `PUBLIC_REPLAY_INTEGRITY`
  - post-commit builder `--check` PASS;
  - accepted public implementation bytes unchanged.

reuse_allowed:

- 1047 implementation validation;
- Browser static/conformance PASS;
- Human Operation QA `ACCEPTED`.

human_owned:

- `NOT_REQUIRED` for byte-preserving persistence;
- actual Cloudflare account/project authorization remains Human-owned;
- Browser must judge the persistence result before deployment.

not_required:

- localhost visual QA rerun;
- provider/DB;
- public availability test;
- Cloudflare deployment.

forbidden:

- public deployment;
- push;
- competition submission;
- source re-authoring.

proof_non_substitution:

- Human QA acceptance != Git persistence;
- local commit != public deployment;
- clean workspace != immutable-hash proof;
- build check != public availability;
- Cloudflare target decision != Cloudflare project existence.

## expected terminal candidate

```text
PERSISTENCE_CANDIDATE / BROWSER_REVIEW_REQUIRED
```

Do not declare deployment complete, P3-3 closed, or competition submitted.

## target bundle

`.aiassistant/reports/target/20260915_1225_aiscc-p3-3-human-accepted-public-replay-implementation-git-persistence-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `PRECOMMIT_INVENTORY.json`
- `HUMAN_ACCEPTED_HASHES.json`
- `STAGED_COMMIT_MANIFEST.json`
- `POSTCOMMIT_VERIFICATION.json`
- `TERMINAL_WORKSPACE.json`
- copies of the new Cycle/Judgment/Handoff/Task-done preserving relative paths
- `REMOVED_FILES.md` only if deletion exists; none expected.

Terminal ZIP:

`.aiassistant/reports/target/20260915_1225_aiscc-p3-3-human-accepted-public-replay-implementation-git-persistence-1.zip`

## final response

1. result
2. result commit SHA
3. parent SHA
4. changed path count
5. immutable Human-accepted hash verification
6. projection edits
7. builder check
8. terminal workspace
9. target bundle + ZIP
10. Human verification
11. remaining deployment blockers
