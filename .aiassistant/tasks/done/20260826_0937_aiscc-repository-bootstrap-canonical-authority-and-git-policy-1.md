# 작업지시서: P0-4 Repository Bootstrap / Canonical Authority / Git Policy

## meta

- task_id: `20260826_0937_aiscc-repository-bootstrap-canonical-authority-and-git-policy-1`
- created_at: `2026-08-26 09:37 KST`
- phase: `P0-4 — Repository Bootstrap / Canonical Authority / Git Policy`
- work_type: `DOC_BASELINE_UPDATE`
- repository_bootstrap_scope: `LOCAL_REPOSITORY_BOOTSTRAP`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- task_transport: `BROWSER_CHAT_ATTACHMENT`
- predecessor_cycle: `20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1`
- predecessor_result: `ACCEPTED / CLOSED`
- P0_3_status: `HUMAN_CONFIRMED / CLOSED`
- repository_status_before: `NOT_CREATED`
- primary_semantic_owner: `local repository bootstrap / canonical authority / Git provenance policy / canonical decision and queue initialization`
- expected_terminal_candidate: `ACCEPTED_CANDIDATE` only when the Task's required local evidence is satisfied; P0-5 owns mirror-sync status
- browser_project_source_status: `AISCC-BOOTSTRAP-SEED-V1 active 14/14; immutable temporary authority`
- P0_5_status: `NOT_STARTED`

## current accepted inputs

P0-4 MUST treat the following as accepted project input and MUST NOT reopen them as product-design questions.

### A. P0-2 accepted baselines

1. `AISCC_PRODUCT_THESIS.md`
2. `AISCC_PRIOR_ART_BOUNDARY.md`
3. `AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
4. exact accepted P0-2 Task Contract:
   `20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.md`
5. terminal Cycle:
   `20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.cycle.md`

Accepted substantive decisions include:

- one-sentence AISCC product thesis
- primary operator = hands-on software owner / tech lead
- minimum success / stretch success boundary
- prior-art overlap and strict `DO-NOT-CLAIM`
- eight differentiation hypotheses
- Self-Dogfooding proof / non-proof boundary
- `AISCC-COMPETITION-PUBLIC-RUNTIME-V1`
- Replay-default / bounded-Live / fallback
- P1-2 / P2-3 / P3-3 responsibility handoff

The three P0-2 baseline files were generated pre-repository and still contain candidate-status metadata. P0-4 MUST preserve their accepted substantive bodies while canonicalizing document status to human-accepted repository canonical form.

### B. Human queue correction

The canonical queue MUST enforce:

```text
P1 security/runtime design
→ dedicated P1 security/runtime safeguard implementation + verification
→ later public Live/release/deployment verification
```

Invariant:

```text
P3-3 MUST NOT be the first safeguard implementation stage.
```

P0-4 MUST encode a dedicated P1 security/runtime safeguard implementation + verification Task in `NEXT_ACTIONS.md` after the security/runtime design baseline and before any public Live/release Task that depends on those safeguards.

The exact P1 task ordinal may be selected while canonicalizing the queue, but it MUST be explicit and stable in the resulting `NEXT_ACTIONS.md`.

### C. Human Project Decision — competition deployment direction

Record the following as an accepted project decision, not as deployment evidence.

Recommended canonical decision ID:

```text
AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1
```

Accepted direction:

- Public UI / Recorded Replay: `Cloudflare Pages`
- representative submission URL shape: `https://<project-slug>.pages.dev/`
- Bounded Live API / PostgreSQL: `Railway Hobby`
- Railway region: `Singapore`
- LLM: separate `OpenAI API Project`
- public page / Recorded Replay: LLM inference `0`
- Live: bounded / allowlisted only
- Live failure or budget exhaustion: Recorded Replay remains available
- operating-cost target: approximately `USD 30`
- absolute operating-cost cap plan: `USD 50`

Required classification:

```text
HUMAN_PROVIDED
ACCEPTED_PROJECT_DECISION
implementation_status: NOT_EXECUTED
provider_capability_verification: DEFERRED
```

P0-4 MUST NOT create provider resources or claim that any provider plan, region, pricing, hard-spend guard, service URL, model, call cap, token cap, or budget configuration has been verified/configured.

## prerequisite / mandatory preflight

Before any mutation:

1. Confirm the human intentionally opened the intended AISCC local workspace.
2. Confirm the workspace is not already inside an unrelated Git repository.
3. Inventory existing files before `git init`.
4. The only preexisting work artifacts allowed without further investigation are:
   - this active Task File;
   - explicitly staged Bootstrap Seed v1 source files;
   - explicitly staged accepted P0-2 baseline/cycle input files.
5. If unrelated source, existing `.git`, unexpected Git history, or ambiguous workspace ownership is found, STOP with:
   - `DIRTY_WORKSPACE_MIXED`, or
   - `BLOCKED_REPOSITORY_ROOT_AMBIGUOUS`.
6. If any required accepted input or Bootstrap Seed source body is unavailable locally, STOP with:
   - `BLOCKED_MISSING_ARTIFACT`.
7. Do not reconstruct missing accepted baseline text from memory, chat summaries, or general knowledge.

The human may stage the required pre-repository inputs in a temporary local location. P0-4 MUST record the exact input paths and SHA-256 values used for migration. Temporary input copies are not canonical repository authority.

## 이번 턴 목표

1. Create the AISCC local Git repository in the human-designated workspace.
2. Establish repository canonical authority and tracked/ignored provenance boundaries.
3. Create the canonical `.aiassistant` structure required for normal AISCC workflow.
4. Migrate the immutable Bootstrap Seed v1 rules/playbooks into repository canonical owners without modifying Browser Project Source.
5. Migrate the human-accepted P0-2 three baselines and terminal P0-2 Cycle.
6. Create canonical:
   - `CURRENT_STATE_SUMMARY.md`
   - `DECISION_REGISTER.md`
   - `NEXT_ACTIONS.md`
7. Record `AISCC-COMPETITION-PUBLIC-RUNTIME-V1` and `AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1` in the Decision Register with correct evidence/status boundaries.
8. Encode the P1 security/runtime safeguard implementation + verification queue invariant.
9. Establish minimal Git ignore/tracking policy and a thin repository-root `AGENTS.md`.
10. Produce executor evidence/export and, if all required local checks pass, create the initial local canonical commit.
11. Prepare the repository so that P0-5 can create the first Project Source mirror v1; DO NOT perform P0-5.

## 이번 턴 비목표

- product runtime source implementation
- state-machine implementation
- security/sandbox safeguard implementation
- security runtime verification
- frontend/backend application implementation
- public Live implementation
- Cloudflare/Railway/OpenAI account or resource creation
- provider login or credentialed action
- deployment
- API key or secret creation/storage
- billing/spend-limit configuration
- exact provider feature/pricing validation
- exact model/call/token/run cap selection
- final public service URL allocation
- Browser Project Source replacement or upload
- P0-5 mirror generation/sync
- competition submission
- remote Git repository creation
- `git push`, PR, release, package publish

## authority / source rule

Bootstrap Seed v1 remains the temporary Browser authority until P0-5 complete replacement is human-confirmed.

During P0-4:

```text
pre-repository Bootstrap Seed v1
→ read-only migration source

new local repository canonical
→ editable local canonical after created and verified

Browser Project Source
→ MUST remain unchanged during P0-4
```

P0-4 MUST NOT claim Browser Project Source is synchronized with the new repository.

## 읽을 문서 — minimum authoritative context set

Read exact staged/local copies of all 14 Bootstrap Seed v1 active sources before migration:

1. `00_AISCC_BOOTSTRAP__SEED_INDEX.md`
2. `01_AISCC_BOOTSTRAP__PROJECT_BOOTSTRAP.md`
3. `10_AISCC_RULES__AGENT_AUTHORITY_AND_TRANSPORT.md`
4. `20_AISCC_COMMAND_CENTER__README.md`
5. `21_AISCC_COMMAND_CENTER__WORKFLOW.md`
6. `22_AISCC_COMMAND_CENTER__TASK_FILE_TEMPLATE.md`
7. `23_AISCC_COMMAND_CENTER__SHORT_EXECUTOR_PROMPT_TEMPLATE.md`
8. `24_AISCC_COMMAND_CENTER__JUDGMENT_RUBRIC.md`
9. `25_AISCC_COMMAND_CENTER__CYCLE_RECORD_TEMPLATE.md`
10. `26_AISCC_COMMAND_CENTER__NEXT_ACTION_SELECTION_RUBRIC.md`
11. `30_AISCC_RULES__IDE_EXECUTOR_REPORT_EXPORT.md`
12. `31_AISCC_RULES__ASSET_GIT_AND_ENCODING_POLICY.md`
13. `32_AISCC_RULES__PROJECT_SOURCE_MIRROR.md`
14. `33_AISCC_RULES__DOCUMENT_LANGUAGE_POLICY.md`

Then read the accepted P0-2 input set:

15. `AISCC_PRODUCT_THESIS.md`
16. `AISCC_PRIOR_ART_BOUNDARY.md`
17. `AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
18. `20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.md`
19. `20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.cycle.md`

Do not bulk-read unrelated files.

## canonical repository structure to establish

At minimum:

```text
AGENTS.md

.aiassistant/
├── rules/
│   ├── AISCC_AGENTS.md
│   ├── IDE_EXECUTOR_REPORT_EXPORT.md
│   ├── IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
│   ├── AISCC_PROJECT_SOURCE_MIRROR.md
│   └── AISCC_DOCUMENT_LANGUAGE_POLICY.md
├── records/
│   ├── command-center/
│   │   ├── README.md
│   │   ├── COMMAND_CENTER_WORKFLOW.md
│   │   ├── TASK_FILE_TEMPLATE.md
│   │   ├── SHORT_EXECUTOR_PROMPT_TEMPLATE.md
│   │   ├── JUDGMENT_RUBRIC.md
│   │   ├── CYCLE_RECORD_TEMPLATE.md
│   │   └── NEXT_ACTION_SELECTION_RUBRIC.md
│   └── aiscc/
│       ├── CURRENT_STATE_SUMMARY.md
│       ├── DECISION_REGISTER.md
│       ├── NEXT_ACTIONS.md
│       ├── bootstrap/
│       │   ├── AISCC_BOOTSTRAP_SEED_V1_INDEX.md
│       │   └── AISCC_PROJECT_BOOTSTRAP_GENESIS.md
│       └── cycles/
│           └── 20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.cycle.md
├── tasks/
│   ├── active/
│   └── done/
│       └── 20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.md
├── reports/
│   ├── target/
│   └── aiscc/
│       ├── AISCC_PRODUCT_THESIS.md
│       ├── AISCC_PRIOR_ART_BOUNDARY.md
│       └── AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md
└── project-sources/
    ├── PROJECT_SOURCE_BUNDLE_REGISTRY.md
    ├── manifests/
    └── bundles/
```

Empty ignored directories need not be committed. Use `.gitkeep` only when a committed empty directory has an explicit workflow need; do not add decorative placeholders.

## canonical migration mapping

### rules

- `10_AISCC_RULES__AGENT_AUTHORITY_AND_TRANSPORT.md`
  → `.aiassistant/rules/AISCC_AGENTS.md`
- `30_AISCC_RULES__IDE_EXECUTOR_REPORT_EXPORT.md`
  → `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `31_AISCC_RULES__ASSET_GIT_AND_ENCODING_POLICY.md`
  → `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `32_AISCC_RULES__PROJECT_SOURCE_MIRROR.md`
  → `.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md`
- `33_AISCC_RULES__DOCUMENT_LANGUAGE_POLICY.md`
  → `.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md`

### command-center records

- `20_AISCC_COMMAND_CENTER__README.md`
  → `.aiassistant/records/command-center/README.md`
- `21_AISCC_COMMAND_CENTER__WORKFLOW.md`
  → `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- `22_AISCC_COMMAND_CENTER__TASK_FILE_TEMPLATE.md`
  → `.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md`
- `23_AISCC_COMMAND_CENTER__SHORT_EXECUTOR_PROMPT_TEMPLATE.md`
  → `.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md`
- `24_AISCC_COMMAND_CENTER__JUDGMENT_RUBRIC.md`
  → `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md`
- `25_AISCC_COMMAND_CENTER__CYCLE_RECORD_TEMPLATE.md`
  → `.aiassistant/records/command-center/CYCLE_RECORD_TEMPLATE.md`
- `26_AISCC_COMMAND_CENTER__NEXT_ACTION_SELECTION_RUBRIC.md`
  → `.aiassistant/records/command-center/NEXT_ACTION_SELECTION_RUBRIC.md`

### historical bootstrap provenance

- `00_AISCC_BOOTSTRAP__SEED_INDEX.md`
  → `.aiassistant/records/aiscc/bootstrap/AISCC_BOOTSTRAP_SEED_V1_INDEX.md`
- `01_AISCC_BOOTSTRAP__PROJECT_BOOTSTRAP.md`
  → `.aiassistant/records/aiscc/bootstrap/AISCC_PROJECT_BOOTSTRAP_GENESIS.md`

These two files are historical genesis provenance after repository canonical becomes active; they MUST NOT be treated as an editable moving canonical baseline.

### accepted P0-2 canonical migration

- exact P0-2 Task Contract
  → `.aiassistant/tasks/done/20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.md`
- `AISCC_PRODUCT_THESIS.md`
  → `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
- `AISCC_PRIOR_ART_BOUNDARY.md`
  → `.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md`
- `AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
  → `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
- accepted P0-2 Cycle
  → `.aiassistant/records/aiscc/cycles/20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.cycle.md`

For the three accepted baselines:

- preserve accepted substantive body;
- update pre-repository candidate metadata/status to repository canonical `ACCEPTED`;
- record human acceptance provenance and canonicalization task;
- do not change substantive thesis, prior-art boundary, or public runtime policy unless needed only to reflect the already-provided human decisions;
- do not silently introduce new external factual claims.

## repository-root `AGENTS.md` policy

P0-4 decision:

```text
AGENTS.md: TRACK
role: THIN_TRANSPORT_BOOTSTRAP
policy_authority: No
```

Use the Seed v1 proposed bootstrap semantics:

- read `.aiassistant/rules/AISCC_AGENTS.md`
- read executor report/export and asset/Git/encoding rules
- read active Task before broad source inspection
- read task-listed exact canonical paths
- distinguish auto-discovered vs explicitly read source
- stop on policy/source/evidence conflict
- never claim human-owned evidence as executor-completed
- no Git index/commit/push/deployment/credentialed external actions unless Task explicitly authorizes them

Do not duplicate long canonical rule bodies into `AGENTS.md`.

## Git tracking / ignore policy

### TRACK

```text
AGENTS.md
.aiassistant/rules/**
.aiassistant/records/command-center/**
.aiassistant/records/aiscc/**
.aiassistant/tasks/done/**
.aiassistant/reports/aiscc/**
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
.aiassistant/project-sources/manifests/**
```

### IGNORE

Initial `.gitignore` MUST include:

```gitignore
.aiassistant/tasks/active/
.aiassistant/reports/target/
.aiassistant/project-sources/bundles/
```

Do not add broad runtime/sandbox/build ignore patterns before those paths exist and their owner Task defines them.

P0-4 may additionally ignore local temporary bootstrap input staging only when its exact local path is known and the pattern cannot hide future canonical files. Record that pattern and reason in the report.

## canonical Current State requirements

Create:

```text
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
```

Minimum content:

- project name and accepted one-sentence thesis reference
- current phase = P0-4 in execution / P0-5 next after acceptance
- P0-1 `ACCEPTED / CLOSED`
- P0-2 `ACCEPTED / CLOSED`
- P0-3 `HUMAN_CONFIRMED / CLOSED`
- repository canonical authority status
- Browser Project Source still Bootstrap Seed v1 until P0-5 replacement
- accepted competition public runtime mode
- accepted deployment direction with `NOT_EXECUTED` status
- current blockers
- current next action
- explicit statement that no product runtime/deployment/provider resource exists merely because P0-4 created the repository

## canonical Decision Register requirements

Create:

```text
.aiassistant/records/aiscc/DECISION_REGISTER.md
```

At minimum record:

1. custom explicit state machine core / no LangGraph core
2. P0-2 product thesis acceptance
3. P0-2 prior-art / `DO-NOT-CLAIM` boundary
4. `AISCC-COMPETITION-PUBLIC-RUNTIME-V1`
5. `AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1`
6. Bootstrap Seed v1 immutable temporary authority until P0-5 complete replacement
7. repository-root `AGENTS.md` tracked thin transport bootstrap
8. canonical repository vs Browser Project Source read-only mirror authority split
9. P1 safeguard implementation-before-release queue invariant

Every entry MUST distinguish:

- decision status
- human/source provenance
- implementation status
- verification status
- owner / future task
- supersession rule when applicable

For `AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1`, implementation and provider verification MUST remain deferred.

## canonical Next Actions requirements

Create:

```text
.aiassistant/records/aiscc/NEXT_ACTIONS.md
```

This is a stable roadmap, not a per-turn log.

Required beginning:

```text
P0-5 First Project Source Mirror v1
→ P1-1 Core Domain / State Machine Design
→ P1 security/runtime design
→ P1 dedicated security/runtime safeguard implementation + verification
→ remaining Governance Kernel implementation tasks
→ P2 Demonstration / scenario / Self-Dogfooding
→ P3 Proof / public release / submission
```

The canonical queue MUST assign stable task identifiers/titles so that the safeguard implementation + verification stage is unambiguous.

Required invariant:

```text
NO_PUBLIC_BOUNDED_LIVE_RELEASE
BEFORE
P1_SECURITY_RUNTIME_SAFEGUARD_IMPLEMENTATION_AND_VERIFICATION_ACCEPTED
```

P3 release/submission responsibility includes re-verifying/configuring already-designed and already-implemented safeguards; it MUST NOT be the first implementation point for:

- public/private permission-profile isolation
- synthetic repository isolation
- command/network deny-by-default
- secret/credential boundary
- timeout/retry/cancel failure semantics
- idempotency/abuse/throttling guard
- application budget guard
- provider spend-guard capability/configuration when supported
- Replay fallback under Live/provider/budget failure

## Project Source registry boundary

Create a tracked registry baseline:

```text
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
```

P0-4 scope:

- define repository canonical as source owner;
- define future mirror bundle as generated/ignored;
- define Browser Project Source as read-only human-uploaded mirror;
- record that current Browser Project still has Bootstrap Seed v1;
- state that P0-5 owns first manifest/bundle generation and complete active-set replacement.

P0-4 MUST NOT generate/upload the first active mirror bundle unless separately authorized by a future P0-5 Task.

## local Git actions explicitly authorized for P0-4

Allowed only after preflight passes:

1. `git init` for the intended AISCC workspace.
2. Establish initial branch `main`.
3. Create/modify only P0-4-authorized repository/canonical files.
4. `git status`, `git diff`, `git diff --check`, `git ls-files`, hash/integrity commands.
5. Stage only the exact P0-4 accepted canonical/bootstrap files.
6. Create one local initial commit after all required evidence passes.

No remote operation is authorized.

If Git author identity is missing:

- DO NOT modify global Git config.
- DO NOT invent identity.
- report `HUMAN_GIT_IDENTITY_REQUIRED`.
- local file/canonical work may be complete, but no commit may be falsely reported.

Recommended initial commit message:

```text
chore: bootstrap AISCC canonical governance repository

Establish the local AISCC repository, canonical authority layout, tracked
governance provenance, accepted P0-2 baselines, decision register, and
stable next-action queue.

Keep Browser Project Bootstrap Seed v1 unchanged until the P0-5 complete
mirror replacement and defer runtime, deployment, credentials, and
provider configuration to their owning tasks.
```

## 절대 금지

- Browser Project Source active file mutation/add/remove/partial replacement
- P0-5 mirror sync execution
- product runtime/state-machine/security safeguard implementation
- Cloudflare, Railway, OpenAI resource/account/project creation
- provider login
- credential/API key/token generation or printing
- billing/spend-limit configuration
- deployment/network call requiring credentials
- remote Git repository creation
- `git push`
- public URL claim
- exact provider feature/pricing/capability claim without future verification
- treating the accepted deployment direction as configured runtime evidence
- changing the substantive accepted P0-2 thesis/prior-art/public-runtime decisions
- introducing private company/customer source or secrets
- broad source/test exploration unrelated to P0-4

## workflow transition expectation

- initial_state: `P0_4_READY`
- expected_non_terminal_state_when_human_pending: `HUMAN_REQUIRED`
- expected_terminal_candidate: `ACCEPTED_CANDIDATE` as reported by Executor; Command Center owns final P0-4 judgment
- transition_authority: `SYSTEM / COMMAND_CENTER`, human gate where Task assigns it
- Agent may directly decide terminal accepted state: `No`
- P0-5 source mirror replacement is a separate future transition and MUST remain unexecuted

## evidence contract

### executor_required

#### channel: `STATIC_SOURCE`

scope:

- exact 14 Bootstrap Seed v1 sources
- accepted P0-2 exact Task Contract
- accepted P0-2 three baselines
- terminal accepted P0-2 Cycle

pass condition:

- exact read inventory + SHA-256
- no missing source
- no memory reconstruction of missing source
- accepted vs historical vs temporary authority correctly classified

#### channel: `WORKSPACE_PREFLIGHT`

scope:

- intended repository root
- existing `.git`
- existing files
- initial dirty/unrelated state

pass condition:

- no unrelated repository/history/source collision
- before-state recorded

#### channel: `REPOSITORY_STRUCTURE`

scope:

- required canonical paths
- source→canonical migration mapping

pass condition:

- required files exist at exact paths
- no duplicate competing canonical owners
- historical Seed files are not left as moving authority

#### channel: `CANONICAL_AUTHORITY`

scope:

- `AGENTS.md`
- canonical rules
- command-center records
- Current State
- Decision Register
- Next Actions
- three accepted reports
- terminal P0-2 Cycle

pass condition:

- transport vs authority split preserved
- accepted P0-2 substantive decisions preserved
- deployment direction recorded as decision only
- safeguard queue invariant present
- P3-3 not modeled as first safeguard implementation stage

#### channel: `GIT_POLICY`

scope:

- TRACK/IGNORE policy
- `.gitignore`
- tracked file inventory

pass condition:

- active tasks / target reports / generated mirror bundles ignored
- canonical rules/records/reports/tasks-done/manifest-registry paths are not accidentally ignored
- `AGENTS.md` tracked
- no broad ignore hides future provenance

#### channel: `DOCUMENT_INTEGRITY`

scope:

- all new/modified Markdown and `.gitignore`

pass condition:

- UTF-8
- Markdown fence parity
- no unintended control characters
- no broken placeholder/template residue
- internal canonical paths resolve where expected
- `git diff --check` or equivalent passes

#### channel: `GIT_LOCAL_PROVENANCE`

scope:

- local repository initialization and initial commit

pass condition:

- `main` branch established
- commit contains only authorized P0-4 files
- commit hash recorded
- no remote configured/used unless it preexisted unexpectedly, in which case stop and report
- if Git identity blocks commit, classify honestly rather than substituting file existence for commit evidence

#### channel: `PUBLIC_PROVENANCE`

scope:

- P0-2 exact Task/Cycle/canonical migration mapping
- P0-4 Task lifecycle plan
- Decision Register / Next Actions provenance

pass condition:

- public provenance does not contain secret/private source
- candidate→human accepted→canonical migration is reconstructible
- deployment direction remains `NOT_EXECUTED`

### reuse_allowed

- predecessor: `20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1`
  - reusable_scope: accepted P0-2 substantive baseline bodies and prior official-source verification
  - condition: P0-4 does not add new external factual claims that require fresh verification

- predecessor: `AISCC-BOOTSTRAP-SEED-V1`
  - reusable_scope: bootstrap rule/playbook bodies and authority lifecycle
  - condition: immutable source; migration and canonicalization only

- predecessor: P0-3 human confirmation
  - reusable_scope: Browser Project bootstrap existence/status
  - condition: do not infer P0-5 mirror sync from it

### human_owned

#### channel: `HUMAN_REPOSITORY_ROOT_CONFIRMATION`

scope:

- the local workspace opened for P0-4 is the intended AISCC repository root

expected result:

```text
HUMAN_PROVIDED or precondition explicitly established by the human opening/placing the Task in the workspace
```

If ambiguous, stop.

#### channel: `HUMAN_GIT_IDENTITY`

scope:

- Git author identity when local commit cannot be created without configuration

expected result:

- human configures identity outside Agent action, then reruns/reworks as needed

#### channel: `HUMAN_VERIFICATION`

scope:

- Command Center review of P0-4 target bundle, canonical layout, migration, queue, and commit mapping

expected result:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

### not_required

- product source build/test
- database
- HTTP runtime
- browser runtime
- LLM inference
- Cloudflare/Railway/OpenAI provider verification
- public service link
- deployment
- billing configuration
- security sandbox runtime proof
- P0-5 Browser Project Source upload

### forbidden

- provider/credential/deployment actions
- Browser Project Source mutation
- public runtime implementation
- security safeguard implementation
- Git remote/push
- unrelated source/test broadening

## proof non-substitution

- local repository files != Browser Project Source mirror sync
- candidate baseline file existence != human acceptance
- human deployment-direction decision != provider capability verification
- provider choice != provider resource creation
- cost target/cap plan != billing/spend guard configuration
- `.gitignore` text != tracked-file inventory proof
- local commit != remote publication
- `AGENTS.md` transport != canonical policy authority
- P1 security design != safeguard implementation
- safeguard implementation != safeguard runtime/security verification
- P3 release checklist != first safeguard implementation
- Project Source registry != P0-5 manifest/bundle/sync
- executor report != human acceptance

## mandatory stop conditions

Stop before further mutation when any applies:

- missing required accepted input artifact
- ambiguous repository root
- existing unrelated Git repository/history
- unrelated dirty/source collision
- Bootstrap Seed body mismatch or incomplete 14/14 set
- accepted P0-2 input cannot be traced
- secret/private source detected
- authority mapping conflict
- broad `.gitignore` would hide canonical/provenance files
- task requires provider/network/credential action
- Git remote unexpectedly exists before bootstrap
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`

Named blocker 이후에는 최소 source/workspace evidence, report/export, safe stop only.

## report requirements

The executor report MUST include:

- task/work type/task path
- preflight repository root and before-state
- exact read source inventory and SHA-256
- auto-discovered instruction inventory vs explicitly read canonical source
- source→canonical migration mapping
- product source changes: `none`
- governance/provenance changes
- repository configuration changes
- added/modified/removed files
- `.gitignore` policy and tracked inventory
- `AGENTS.md` tracked transport decision
- accepted P0-2 migration status
- Decision Register entries created
- `NEXT_ACTIONS.md` queue and safeguard invariant
- deployment direction classification:
  `HUMAN_PROVIDED / ACCEPTED_PROJECT_DECISION / NOT_EXECUTED`
- evidence contract actual classifications
- forbidden-not-run
- mandatory stop/scope expansion
- Git initialization/branch/commit evidence
- remote operation evidence: must be absent
- UTF-8/Markdown/control-character checks
- unverified/deferred items
- rollback/revert guide
- preserved exact paths
- next turn recommendation = P0-5 if accepted

## export bundle

Target:

```text
.aiassistant/reports/target/20260826_0937_aiscc-repository-bootstrap-canonical-authority-and-git-policy-1/
```

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- changed files preserving repository-relative paths
- `REMOVED_FILES.md` only if deletion exists

Do not include `.git/`, secrets, cache, unrelated files, or generated P0-5 bundles.

## Task lifecycle

When executor-required work/report/export is complete:

```text
.aiassistant/tasks/active/20260826_0937_aiscc-repository-bootstrap-canonical-authority-and-git-policy-1.md
→
.aiassistant/tasks/done/20260826_0937_aiscc-repository-bootstrap-canonical-authority-and-git-policy-1.md
```

`done` means executor turn submitted, not accepted.

Because `tasks/active/**` is ignored and `tasks/done/**` is tracked, moving the Task to `done` is part of the final local provenance before the initial canonical commit only if the Task lifecycle can be completed without a human-owned blocker. If a required human precondition blocks completion, report the blocker and do not falsify the lifecycle.

## accept criteria

- intended AISCC repository root is unambiguous
- local Git repository created with `main`
- required canonical structure exists
- 14 Seed sources were exact-read and mapped
- Bootstrap Seed Browser source remains unchanged
- accepted P0-2 exact Task, baselines, and terminal Cycle are migrated
- baseline metadata/status reflects human acceptance without substantive drift
- Current State, Decision Register, Next Actions are present
- deployment direction is recorded as accepted decision with `NOT_EXECUTED`
- P1 safeguard implementation + verification Task is explicit in canonical queue
- P3-3 is not the first safeguard implementation stage
- `AGENTS.md` is tracked and thin
- Git TRACK/IGNORE rules match policy
- no product/runtime/deployment/provider action occurred
- document integrity passes
- local commit exists, or commit is honestly blocked only by human Git identity with all other work complete
- target bundle is complete

## hold / reject criteria

- missing accepted baseline or Cycle
- P0-2 substantive decisions silently rewritten
- deployment direction treated as configured runtime evidence
- P1 safeguard implementation/verification queue omitted
- P3-3 remains first safeguard implementation point
- Browser Project Source modified
- P0-5 executed
- provider/resource/API key/billing/deployment action performed
- existing unrelated repo/history overwritten
- `.gitignore` hides tracked provenance
- `AGENTS.md` becomes a duplicate long policy authority
- remote Git operation performed
- private/company/customer source or secret enters public provenance
- Agent claims human acceptance
- proof-type substitution
- required local commit falsely claimed

## rollback

If rejected before commit:

- remove only P0-4-created repository/canonical files;
- do not touch unrelated preexisting files;
- remove `.git/` only if P0-4 created it in an otherwise confirmed empty AISCC workspace and rollback is explicitly required by judgment.

If rejected after initial local commit:

- do not rewrite history automatically;
- report exact commit and changed paths;
- Command Center decides whether rework commit or repository recreation is appropriate.

No provider/deployment rollback should be necessary because those actions are forbidden.

## preserved artifacts after acceptance

Expected canonical paths to preserve:

- `AGENTS.md`
- `.gitignore`
- `.aiassistant/rules/**`
- `.aiassistant/records/command-center/**`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/records/aiscc/bootstrap/**`
- `.aiassistant/records/aiscc/cycles/20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.cycle.md`
- `.aiassistant/tasks/done/20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.md`
- `.aiassistant/tasks/done/20260826_0937_aiscc-repository-bootstrap-canonical-authority-and-git-policy-1.md`
- `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
- `.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md`
- `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
- `.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md`

P0-4 target bundle is temporary after Command Center judgment unless the judgment explicitly says otherwise.

## next action after P0-4 acceptance

```text
P0-5 First Project Source Mirror v1
```

P0-5 must:

- generate a tracked manifest from repository canonical;
- generate ignored mirror bundle;
- verify file count/hash/body mapping;
- wait for human complete Browser Project Source replacement;
- remove the Bootstrap Seed v1 active set only as part of the complete replacement;
- never leave Seed + mirror v1 as mixed current authority.
