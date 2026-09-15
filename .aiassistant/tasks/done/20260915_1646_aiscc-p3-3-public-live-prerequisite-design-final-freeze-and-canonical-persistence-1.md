# 작업지시서: P3-3 Public Live prerequisite design final freeze and canonical persistence

## meta

- task_id: `20260915_1646_aiscc-p3-3-public-live-prerequisite-design-final-freeze-and-canonical-persistence-1`
- created_at: `2026-09-15T16:46:40+09:00`
- work_type: `DESIGN_FREEZE_PERSISTENCE`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`

## objective

Finalize and persist the Human-accepted Public Bounded Live prerequisite design.

The 1630 candidate is accepted with exactly two Human-approved Browser amendments:

- H3 campaign cutoff aligned to Korea-local end of 2026-10-17;
- H5 read capability retained in `sessionStorage`.

This Task creates canonical design authority.

It does NOT implement Live.

## Human decision authority

Human explicitly provided:

```text
H1 ACCEPT
H2 ACCEPT
H3 ACCEPT_BROWSER_RECOMMENDATION
H4 ACCEPT
H5 ACCEPT_BROWSER_RECOMMENDATION
H6 ACCEPT
H7 ACCEPT
```

Treat these as `HUMAN_PROVIDED`.

Do not re-open H1/H2/H4/H6/H7.

## exact repository baseline

Before transport/substantive work require:

```text
branch = main
HEAD = 5e35ec0d60d84c7a05a2e58ebcc6560863879e5b
index = empty
tracked worktree = clean
```

Expected Git-visible untracked before this delivery is exactly 12 paths:

- `.aiassistant/records/aiscc/cycles/20260915_1552_aiscc-p3-3-encoding-restoration-accepted-post-submit-live-readiness-entry-1.cycle.md`
  - SHA-256 `2e5946bf3ad1a0a02a387b5fdddaeb76972c9fd6c325f0a3b18e19eb85a04eb9`
- `.aiassistant/records/aiscc/cycles/20260915_1600_aiscc-p3-3-live-readiness-audit-accepted-prerequisite-design-entry-1.cycle.md`
  - SHA-256 `25ef427f1646c111eb6d9d63d1c51e8f1b30c6d5ba87a086ab22aa51be8beadf`
- `.aiassistant/records/aiscc/cycles/20260915_1630_aiscc-p3-3-live-prerequisite-design-output-policy-block-retry-entry-1.cycle.md`
  - SHA-256 `e549792054215b737d056002273c7283fc59885548b4a1964b98708a6f589252`
- `.aiassistant/reports/aiscc/20260915_1552_aiscc-browser-command-center-p3-3-public-bounded-live-readiness-entry-handoff-1.md`
  - SHA-256 `5304907558a67b3edb52c2fcb92fc0ea27fd230ef7648e28acdd05a93b4d4325`
- `.aiassistant/reports/aiscc/20260915_1552_aiscc-p3-3-encoding-restoration-final-browser-acceptance-1.md`
  - SHA-256 `c13e949649ba64cc8be20b9b64099b5ac55b7c1c911a3990b1d56d9f0cbb823a`
- `.aiassistant/reports/aiscc/20260915_1600_aiscc-browser-command-center-p3-3-live-prerequisite-security-design-entry-handoff-1.md`
  - SHA-256 `ed2e7fee3fbdb76651614b7f7f8e3ef0caaf7bd80a4c9e3c90489e16bda5b166`
- `.aiassistant/reports/aiscc/20260915_1600_aiscc-p3-3-live-readiness-audit-browser-acceptance-1.md`
  - SHA-256 `2ad58a1b3f4fdef7a1edd66f055307c38940412455c8aa02369bd7b077690e6d`
- `.aiassistant/reports/aiscc/20260915_1630_aiscc-browser-command-center-p3-3-live-prerequisite-design-output-retry-entry-handoff-1.md`
  - SHA-256 `b4d0940187f836a4a714ccaa62ece9f2ebedca9e3f135cf2502f39a1ced13700`
- `.aiassistant/reports/aiscc/20260915_1630_aiscc-p3-3-live-prerequisite-design-policy-block-browser-judgment-1.md`
  - SHA-256 `8ad463b3580bfa7f683c48e46ebfe4c1622f59922bafd389068b77678f41bbbb`
- `.aiassistant/tasks/done/20260915_1552_aiscc-p3-3-public-bounded-live-release-readiness-audit-and-minimal-design-freeze-1.md`
  - SHA-256 `ab9c880eb900044c6bfb1eea57518769a956c1d1eb119abaa5f2a362a2300132`
- `.aiassistant/tasks/done/20260915_1600_aiscc-p3-3-public-live-admission-budget-identity-security-design-freeze-1.md`
  - SHA-256 `a69889677848becb557f5acd158d8e29a9e865b68ffd8c8f912b99bcbeaf6ae4`
- `.aiassistant/tasks/done/20260915_1630_aiscc-p3-3-public-live-prerequisite-design-output-generation-policy-block-retry-1.md`
  - SHA-256 `3ccf8e34188715bbc497491a55c60b38fe36a553157fec6b57ed63100678e944`

Each path/hash MUST match.

Extra/missing/hash mismatch => STOP.

Do not clean/reset/delete them.

Run:

```text
python scripts/build_public_replay.py --check
```

PASS required.

## inbound lineage from this delivery

This ZIP contains both the completed 1644 Human gate lineage and current 1646 final-freeze lineage.

Canonicalize 1644:

```text
TASK
→ .aiassistant/tasks/done/20260915_1644_aiscc-p3-3-public-live-prerequisite-design-human-acceptance-gate-1.md

CYCLE
→ .aiassistant/records/aiscc/cycles/20260915_1644_aiscc-p3-3-public-live-design-candidate-accepted-human-decision-entry-1.cycle.md

JUDGMENT
→ .aiassistant/reports/aiscc/20260915_1644_aiscc-p3-3-public-live-prerequisite-design-candidate-browser-judgment-1.md

HANDOFF
→ .aiassistant/reports/aiscc/20260915_1644_aiscc-browser-command-center-p3-3-public-live-human-acceptance-entry-handoff-1.md
```

Current 1646:

```text
TASK active first:
.aiassistant/tasks/active/20260915_1646_aiscc-p3-3-public-live-prerequisite-design-final-freeze-and-canonical-persistence-1.md

before final staging:
.aiassistant/tasks/done/20260915_1646_aiscc-p3-3-public-live-prerequisite-design-final-freeze-and-canonical-persistence-1.md

CYCLE:
.aiassistant/records/aiscc/cycles/20260915_1646_aiscc-p3-3-public-live-human-acceptance-final-design-freeze-entry-1.cycle.md

JUDGMENT:
.aiassistant/reports/aiscc/20260915_1646_aiscc-p3-3-public-live-human-acceptance-browser-judgment-1.md

HANDOFF:
.aiassistant/reports/aiscc/20260915_1646_aiscc-browser-command-center-p3-3-public-live-design-frozen-implementation-entry-handoff-1.md
```

## exact candidate input

Required candidate target root:

`.aiassistant/reports/target/20260915_1630_aiscc-p3-3-public-live-prerequisite-design-output-generation-policy-block-retry-1/`

Verify exact candidate design SHA-256:

- `PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md` → `23c17e07bdd7110a6b1dcef9401ee2c64cdeff8d36d6b2c363b16604ed7ceb03`
- `PUBLIC_LIVE_DB_SCHEMA_PLAN.md` → `65bd214539af492ef8f40f56754d924521c86af3a268a18a79959d62a34451a9`
- `PUBLIC_LIVE_HTTP_CONTRACT.md` → `193f61f194a00e8f77ab80e72042c507883bc7ed7cc0728b681ac1c599e18a43`
- `PUBLIC_LIVE_FAILURE_STATE_MACHINE.md` → `01986395171db5b3bad45603a44f9899acacabb5787af0d0755719dfa125c0af`
- `PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json` → `2c4f20eaa8a43a0cb389dfa3d92aea9a4041bfa2e07a4f66f6b1c99476736ce8`
- `PUBLIC_LIVE_SECURITY_TEST_MATRIX.json` → `6a36141d4a7198c04312bde103b72e022125c7003894a958b5ee138acf4f840c`
- `PUBLIC_LIVE_OPEN_DECISIONS.md` → `fa29f7cd16cfb1ef3bbb39a8eeb08fa5814580322dd2930d760fa25081133002`

If any candidate file is missing or hash differs:

STOP `DESIGN_CANDIDATE_INPUT_MISMATCH`.

Do not silently reconstruct from chat or general knowledge.

## final canonical design paths

Create exactly these seven curated canonical files:

1. `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md`
2. `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_DB_SCHEMA_PLAN.md`
3. `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_HTTP_CONTRACT.md`
4. `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_FAILURE_STATE_MACHINE.md`
5. `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
6. `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
7. `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_HUMAN_DECISIONS.md`

Use the 1630 candidate as the only substantive design source.

No unrelated design rewrite.

## mandatory amendment H3

Daily ledger remains:

```text
UTC day
```

Campaign close MUST become:

```text
2026-10-18T00:00:00+09:00 exclusive
2026-10-17T15:00:00Z equivalent
```

Meaning:

- 2026-10-17 Korea-local day is included;
- no new campaign admission at or after the exclusive instant;
- do not extend nine hours into 2026-10-18 KST.

Update every candidate design/test/decision reference that materially depends on the old cutoff.

Do not convert daily ledger accounting itself from UTC to KST.

## mandatory amendment H5

Read capability final contract:

```text
entropy:
256-bit

expiry:
24 hours

browser persistence:
sessionStorage

same-tab refresh:
retains capability

URL:
forbidden

cookie:
forbidden

localStorage:
forbidden

tab/session close:
capability lost

initial 201 response never received:
no recovery

automatic replacement run:
forbidden

public cancel:
disabled
```

Required semantic consequences:

- successful 201 may be stored in `sessionStorage`;
- a same-tab refresh can resume GET status;
- a new tab/session without the capability cannot recover it;
- same-key replay still does not regenerate a read capability;
- if the original successful 201 never reached the browser, no server-side recovery route is introduced;
- do not log the capability.

Update every candidate design/test/implementation reference that says `memory-only`, `refresh loses access`, or equivalent.

## security test matrix amendment

Preserve all existing test intent.

At minimum:

- update the existing lost-201 test so it remains specifically about **initial 201 not received**, not ordinary refresh;
- add a deterministic test for:
  - successful 201;
  - capability written to same-tab `sessionStorage`;
  - page refresh;
  - GET succeeds with same capability;
  - new independent tab/session has no capability;
  - no URL/cookie/localStorage persistence.
- update campaign-boundary test to assert the accepted KST exclusive cutoff while preserving UTC daily-ledger behavior.

Test design count may increase from 34.

No tests are executed in this Task.

## implementation sequence amendment

Canonical implementation sequence MUST show:

```text
status:
DESIGN_FROZEN_HUMAN_ACCEPTED

L0:
COMPLETE / HUMAN_ACCEPTED
```

Update L7 token UX from `memory-only` to `sessionStorage`.

Preserve dependency structure:

```text
parallel after L0:
L1, L4, L5

serial:
L1 -> L2 -> L3 -> L6 -> L7 -> L8

L6 requires:
L3 + L4 + L5
```

No implementation is performed.

## Human decisions canonical report

`AISCC_PUBLIC_LIVE_HUMAN_DECISIONS.md` must be Korean-first and record:

```text
H1 ACCEPT
H2 ACCEPT
H3 ACCEPT_BROWSER_RECOMMENDATION
H4 ACCEPT
H5 ACCEPT_BROWSER_RECOMMENDATION
H6 ACCEPT
H7 ACCEPT
```

Record the exact final H3/H5 contracts.

Also distinguish remaining `release prerequisites` from Human design decisions:

- Railway ingress/header overwrite proof;
- provider envelope/pricing/config proof;
- execution isolation proof;
- unknown-outcome closure proof;
- shared ingress/read abuse limits;
- migration/least-privilege proof;
- integrated release acceptance.

These are NOT unresolved H1-H7 choices.

## canonical state updates

Modify only these three existing canonical state documents:

1. `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
2. `.aiassistant/records/aiscc/DECISION_REGISTER.md`
3. `.aiassistant/records/aiscc/NEXT_ACTIONS.md`

### CURRENT_STATE_SUMMARY

Project:

```text
Competition submission:
COMPLETED

P3-3:
SUBMITTED / POST_SUBMISSION_IMPROVEMENT_WINDOW

Static Replay:
DEPLOYED / VERIFIED / HUMAN_ACCEPTED

Public Bounded Live:
NOT_RELEASED

Public Live prerequisite design:
HUMAN_ACCEPTED / FROZEN

Live implementation:
NOT_STARTED

Frozen scenario:
stockroom-s1-normal / 1.0.0
```

Do not mark Live ready/released.

### DECISION_REGISTER

Add the Human-authoritative design decision including:

- S1-only first slice;
- accepted caps;
- UTC daily accounting;
- campaign cutoff `2026-10-18T00:00:00+09:00 exclusive`;
- IPv4 /32 and IPv6 /64 HMAC bucket;
- read capability `sessionStorage`, 24h, no URL/cookie/localStorage;
- unknown-provider quarantine;
- separate public Live DB/credentials.

Do not claim deployment proof.

### NEXT_ACTIONS

Set next eligible implementation candidates:

```text
L1:
additive schema/repository transaction primitives

L4:
real provider profile prerequisite

L5:
Railway ingress/sandbox/deployment proof
```

These may proceed only by separate Tasks.

Keep:

```text
L2 blocked on L1
L3 blocked on L2
L6 blocked on L3+L4+L5
L7 blocked on L6
L8 Human release decision
```

No deployment/resource creation is authorized.

## forbidden changes

Do NOT modify:

- `public/replay/**`;
- product/runtime source;
- tests;
- migrations;
- provider adapter/profile;
- API routes;
- frontend;
- deployment config;
- README;
- P3-1/P3-2 accepted material;
- competition submission confirmation/package;
- release manifest/readiness unless explicitly listed above;
- Git config.

No network.

No OpenAI call.

No Railway/Cloudflare/Wanted action.

No paid resources.

No Live enablement.

No push/tag/release.

## expected commit candidate

Exact changed path count:

```text
30
```

Composition:

```text
12 pre-existing accepted governance provenance paths
4 completed 1644 Human-gate lineage paths
4 current 1646 lineage paths
7 new canonical final-design files
3 modified canonical state documents
```

No target/export file is staged.

## commit

Commit message exactly:

```text
docs(aiscc): freeze public live prerequisite design
```

## precommit validation

Require:

- baseline HEAD exact;
- 12 pre-existing path/hash checks exact;
- 1630 candidate seven hashes exact;
- builder `--check` PASS;
- Human H1-H7 values exact;
- old campaign cutoff absent from canonical final design except historical explanation if explicitly labeled superseded;
- `memory-only` as active read-capability policy absent;
- final H3/H5 contract present;
- canonical JSON parses;
- implementation sequence DAG preserved;
- public security test matrix parses and contains new refresh/sessionStorage test;
- only three pre-existing tracked canonical docs modified;
- exact staged path count 30;
- exact staged path allowlist;
- `git diff --cached --check` PASS.

## postcommit validation

Require:

```text
parent = 5e35ec0d60d84c7a05a2e58ebcc6560863879e5b
changed path count = 30
index = empty
tracked worktree = clean
Git-visible untracked = 0

builder --check = PASS
public/replay/** unchanged
product/runtime source unchanged
```

Reopen committed canonical design and state files.

Result classification on success:

```text
PERSISTENCE_CANDIDATE / LIVE_PREREQUISITE_DESIGN_FROZEN
```

Do NOT claim:

```text
LIVE_IMPLEMENTATION_READY
LIVE_RELEASE_READY
LIVE_ENABLED
```

## target export

Target:

`.aiassistant/reports/target/20260915_1646_aiscc-p3-3-public-live-prerequisite-design-final-freeze-and-canonical-persistence-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `HUMAN_DECISION_EVIDENCE.json`
- `CANDIDATE_INPUT_VERIFICATION.json`
- `DESIGN_AMENDMENT_VERIFICATION.json`
- `CANONICAL_DESIGN_MANIFEST.json`
- `STAGED_COMMIT_MANIFEST.json`
- `POSTCOMMIT_VERIFICATION.json`
- `TERMINAL_WORKSPACE.json`
- seven canonical final-design files preserving relative paths
- three modified state files
- current and accepted provenance needed to judge the commit

Terminal ZIP:

`.aiassistant/reports/target/20260915_1646_aiscc-p3-3-public-live-prerequisite-design-final-freeze-and-canonical-persistence-1.zip`

## final response

1. result classification
2. Human decisions applied
3. H3/H5 exact amendments
4. canonical design paths
5. state/decision/next-action updates
6. staged/committed path count
7. commit hash/parent
8. builder/public Replay invariants
9. terminal workspace
10. next eligible Tasks L1/L4/L5
11. target bundle + ZIP
