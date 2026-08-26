# 작업지시서: P0-4 Repository Bootstrap / Canonical Authority / Git Policy — Environment Rework

## meta

- task_id: `20260826_1038_aiscc-repository-bootstrap-canonical-authority-and-git-policy-rework-1`
- created_at: `2026-08-26 10:38 KST`
- phase: `P0-4 — Repository Bootstrap / Canonical Authority / Git Policy`
- work_type: `DOC_BASELINE_UPDATE`
- repository_bootstrap_scope: `EXISTING_EMPTY_REPOSITORY_CANONICAL_BOOTSTRAP`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- task_transport: `BROWSER_CHAT_ATTACHMENT`
- predecessor_task: `20260826_0937_aiscc-repository-bootstrap-canonical-authority-and-git-policy-1`
- predecessor_result: `BLOCKED_MISSING_ARTIFACT`
- supersedes_task: `20260826_0937_aiscc-repository-bootstrap-canonical-authority-and-git-policy-1.md`
- predecessor_cycle: `20260826_1038_aiscc-p0-4-bootstrap-environment-gap-and-rework-1.cycle.md`
- P0_2_status: `ACCEPTED / CLOSED`
- P0_3_status: `HUMAN_CONFIRMED / CLOSED`
- repository_status_before: `HUMAN_CREATED_EMPTY_REMOTE_CLONE`
- primary_semantic_owner: `local repository canonical authority / Git provenance policy / P0-2 migration / stable queue initialization`
- expected_terminal_candidate: `ACCEPTED_CANDIDATE`
- P0_5_status: `NOT_STARTED`

## supersession guard

This Task is the only current P0-4 execution contract.

DO NOT execute or merge with:

```text
20260826_0937_aiscc-repository-bootstrap-canonical-authority-and-git-policy-1.md
```

The predecessor Task was correctly blocked before mutation because its repository/input preconditions did not match the Human-prepared environment.

Preserve the predecessor Task later as blocked-task provenance in `tasks/done`.

## Human-confirmed execution environment

These are Human-provided P0-4 preconditions.

### IDE

```text
IntelliJ
```

### repository root

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

### repository identity

```text
repository_name: ai-software-command-center
visibility: public
license_initialized: No
readme_initialized: No
```

### expected Git state before P0-4 rework

```text
.git: exists
branch: main
local_commits: 0
tracked_files: 0
origin:
  https://github.com/jihyeongshin/ai-software-command-center.git
```

This exact existing `.git` and exact `origin` are **EXPECTED**, not blockers.

The executor MUST NOT run `git init` unless the expected `.git` is unexpectedly absent.
If `.git` is absent, STOP with `BLOCKED_REPOSITORY_PRECONDITION_DRIFT`; do not silently recreate a different repository.

No remote network action is authorized.

Allowed read-only local inspection:

- `git status`
- `git branch --show-current`
- `git remote -v`
- `git log --oneline --all`
- `git ls-files`
- local object/ref/config inspection that does not contact the network

Forbidden:

- `git fetch`
- `git pull`
- `git push`
- GitHub API/CLI remote mutation
- remote repository settings changes

If the exact origin differs, additional remotes exist, or commit history is present, STOP with `BLOCKED_REPOSITORY_PRECONDITION_DRIFT`.

### IntelliJ-generated local metadata

Current `.idea/` is expected local IDE metadata.

It is not product source, governance provenance, or canonical authority.

P0-4 MUST ignore it:

```gitignore
.idea/
```

Do not delete/reset `.idea/` merely for repository cleanliness.

## exact temporary bootstrap input staging

Human will extract the Command Center staging package to:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center\.aiassistant\bootstrap-input\p0-4\
```

Expected structure:

```text
.aiassistant/bootstrap-input/p0-4/
├── P0_4_BOOTSTRAP_INPUT_MANIFEST.md
├── seed/
│   ├── 00_AISCC_BOOTSTRAP__SEED_INDEX.md
│   ├── 01_AISCC_BOOTSTRAP__PROJECT_BOOTSTRAP.md
│   ├── 10_AISCC_RULES__AGENT_AUTHORITY_AND_TRANSPORT.md
│   ├── 20_AISCC_COMMAND_CENTER__README.md
│   ├── 21_AISCC_COMMAND_CENTER__WORKFLOW.md
│   ├── 22_AISCC_COMMAND_CENTER__TASK_FILE_TEMPLATE.md
│   ├── 23_AISCC_COMMAND_CENTER__SHORT_EXECUTOR_PROMPT_TEMPLATE.md
│   ├── 24_AISCC_COMMAND_CENTER__JUDGMENT_RUBRIC.md
│   ├── 25_AISCC_COMMAND_CENTER__CYCLE_RECORD_TEMPLATE.md
│   ├── 26_AISCC_COMMAND_CENTER__NEXT_ACTION_SELECTION_RUBRIC.md
│   ├── 30_AISCC_RULES__IDE_EXECUTOR_REPORT_EXPORT.md
│   ├── 31_AISCC_RULES__ASSET_GIT_AND_ENCODING_POLICY.md
│   ├── 32_AISCC_RULES__PROJECT_SOURCE_MIRROR.md
│   └── 33_AISCC_RULES__DOCUMENT_LANGUAGE_POLICY.md
├── p0-2/
│   ├── AISCC_PRODUCT_THESIS.md
│   ├── AISCC_PRIOR_ART_BOUNDARY.md
│   ├── AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md
│   ├── 20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.md
│   └── 20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.cycle.md
└── p0-4-predecessor/
    ├── 20260826_0937_aiscc-repository-bootstrap-canonical-authority-and-git-policy-1.md
    └── 20260826_1038_aiscc-p0-4-bootstrap-environment-gap-and-rework-1.cycle.md
```

The staging root is temporary and non-authoritative.

P0-4 MUST add:

```gitignore
.aiassistant/bootstrap-input/
```

Do not stage or commit any file under this temporary directory.

After successful P0-4 acceptance, the Human may delete it.

## current workspace before execution

Expected Human-created paths before placing this Task:

```text
.git/
.idea/
.aiassistant/
├── records/aiscc/cycles/
│   └── 20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.cycle.md
└── tasks/active/
    └── 20260826_0937_aiscc-repository-bootstrap-canonical-authority-and-git-policy-1.md
```

Before executor execution, Human will:

1. extract the input package under `.aiassistant/bootstrap-input/p0-4/`;
2. place this rework Task at:
   `.aiassistant/tasks/active/20260826_1038_aiscc-repository-bootstrap-canonical-authority-and-git-policy-rework-1.md`;
3. remove the superseded `20260826_0937...` copy from `tasks/active` after confirming the staging package contains the exact predecessor copy.

The predecessor Task is not discarded; P0-4 migrates its staging copy into `tasks/done`.

## current accepted inputs

P0-4 MUST NOT reopen:

- one-sentence AISCC product thesis
- primary operator = hands-on software owner / tech lead
- minimum / stretch success boundary
- strict prior-art overlap and `DO-NOT-CLAIM`
- eight differentiation hypotheses
- Self-Dogfooding proof / non-proof boundary
- `AISCC-COMPETITION-PUBLIC-RUNTIME-V1`
- Replay-default / bounded-Live / fallback
- P1-2 / P2-3 / P3-3 responsibility handoff
- safeguard implementation-before-release queue correction
- `AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1`

Deployment direction remains:

```text
HUMAN_PROVIDED
ACCEPTED_PROJECT_DECISION
implementation_status: NOT_EXECUTED
provider_capability_verification: DEFERRED
```

No provider/resource/billing/deployment evidence is admitted by P0-4.

## queue invariant

Canonical `NEXT_ACTIONS.md` MUST encode:

```text
P1 security/runtime design
→ dedicated P1 security/runtime safeguard implementation + verification
→ later public Live/release/deployment verification
```

And:

```text
NO_PUBLIC_BOUNDED_LIVE_RELEASE
BEFORE
P1_SECURITY_RUNTIME_SAFEGUARD_IMPLEMENTATION_AND_VERIFICATION_ACCEPTED
```

P3-3 MUST NOT be the first safeguard implementation stage.

## 이번 턴 목표

1. Verify the accepted existing empty repository precondition without contacting the remote.
2. Create repository canonical authority and provenance structure.
3. Create minimal `.gitignore`, including:
   - `.idea/`
   - `.aiassistant/bootstrap-input/`
   - `.aiassistant/tasks/active/`
   - `.aiassistant/reports/target/`
   - `.aiassistant/project-sources/bundles/`
4. Create tracked thin `AGENTS.md`.
5. Migrate exact Bootstrap Seed v1 bodies into canonical repository owners.
6. Migrate accepted P0-2 exact Task, three baselines, and terminal P0-2 Cycle.
7. Preserve predecessor blocked P0-4 Task and this bootstrap-gap Cycle as provenance.
8. Create:
   - `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
   - `.aiassistant/records/aiscc/DECISION_REGISTER.md`
   - `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
   - `.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md`
9. Record accepted competition runtime/deployment decisions with implementation verification still deferred.
10. Produce P0-4 executor report/export bundle.
11. Move this rework Task to `tasks/done` when executor-required work is complete.
12. Create one local initial canonical commit only after all required evidence passes.
13. Do NOT execute P0-5.

## 이번 턴 비목표

- remote Git operation
- `git push`
- GitHub settings mutation
- Browser Project Source mutation/replacement
- P0-5 manifest/bundle/sync
- product runtime implementation
- state-machine implementation
- security/sandbox safeguard implementation
- security runtime verification
- frontend/backend runtime
- Cloudflare/Railway/OpenAI resource creation
- deployment
- API key/credential
- provider login
- billing/spend-limit configuration
- exact model/call/token/run cap
- exact provider feature/pricing verification
- public service URL allocation
- competition submission

## minimum authoritative context set

Read exact staged files in this order.

### staging manifest

1. `.aiassistant/bootstrap-input/p0-4/P0_4_BOOTSTRAP_INPUT_MANIFEST.md`

Validate every listed SHA-256 before using a staged file.

### Bootstrap Seed v1 — exact 14/14

2. `.aiassistant/bootstrap-input/p0-4/seed/00_AISCC_BOOTSTRAP__SEED_INDEX.md`
3. `.aiassistant/bootstrap-input/p0-4/seed/01_AISCC_BOOTSTRAP__PROJECT_BOOTSTRAP.md`
4. `.aiassistant/bootstrap-input/p0-4/seed/10_AISCC_RULES__AGENT_AUTHORITY_AND_TRANSPORT.md`
5. `.aiassistant/bootstrap-input/p0-4/seed/20_AISCC_COMMAND_CENTER__README.md`
6. `.aiassistant/bootstrap-input/p0-4/seed/21_AISCC_COMMAND_CENTER__WORKFLOW.md`
7. `.aiassistant/bootstrap-input/p0-4/seed/22_AISCC_COMMAND_CENTER__TASK_FILE_TEMPLATE.md`
8. `.aiassistant/bootstrap-input/p0-4/seed/23_AISCC_COMMAND_CENTER__SHORT_EXECUTOR_PROMPT_TEMPLATE.md`
9. `.aiassistant/bootstrap-input/p0-4/seed/24_AISCC_COMMAND_CENTER__JUDGMENT_RUBRIC.md`
10. `.aiassistant/bootstrap-input/p0-4/seed/25_AISCC_COMMAND_CENTER__CYCLE_RECORD_TEMPLATE.md`
11. `.aiassistant/bootstrap-input/p0-4/seed/26_AISCC_COMMAND_CENTER__NEXT_ACTION_SELECTION_RUBRIC.md`
12. `.aiassistant/bootstrap-input/p0-4/seed/30_AISCC_RULES__IDE_EXECUTOR_REPORT_EXPORT.md`
13. `.aiassistant/bootstrap-input/p0-4/seed/31_AISCC_RULES__ASSET_GIT_AND_ENCODING_POLICY.md`
14. `.aiassistant/bootstrap-input/p0-4/seed/32_AISCC_RULES__PROJECT_SOURCE_MIRROR.md`
15. `.aiassistant/bootstrap-input/p0-4/seed/33_AISCC_RULES__DOCUMENT_LANGUAGE_POLICY.md`

### accepted P0-2 exact inputs

16. `.aiassistant/bootstrap-input/p0-4/p0-2/AISCC_PRODUCT_THESIS.md`
17. `.aiassistant/bootstrap-input/p0-4/p0-2/AISCC_PRIOR_ART_BOUNDARY.md`
18. `.aiassistant/bootstrap-input/p0-4/p0-2/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
19. `.aiassistant/bootstrap-input/p0-4/p0-2/20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.md`
20. `.aiassistant/bootstrap-input/p0-4/p0-2/20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.cycle.md`

### P0-4 predecessor provenance

21. `.aiassistant/bootstrap-input/p0-4/p0-4-predecessor/20260826_0937_aiscc-repository-bootstrap-canonical-authority-and-git-policy-1.md`
22. `.aiassistant/bootstrap-input/p0-4/p0-4-predecessor/20260826_1038_aiscc-p0-4-bootstrap-environment-gap-and-rework-1.cycle.md`

### current active Task

23. `.aiassistant/tasks/active/20260826_1038_aiscc-repository-bootstrap-canonical-authority-and-git-policy-rework-1.md`

Do not bulk-read unrelated files.

## preflight

Before mutation verify locally, without network:

```text
repository root == C:\Users\oracl\IdeaProjects\ai-software-command-center
.git exists
branch == main
local commit count == 0
tracked file count == 0
origin fetch/push URL == https://github.com/jihyeongshin/ai-software-command-center.git
no additional remote
staging manifest and all 21 staged inputs hash-match
current active Task is this rework Task
```

Expected non-canonical existing paths:

- `.idea/**`
- `.aiassistant/bootstrap-input/p0-4/**`
- this active Task
- the Human-placed P0-2 Cycle copy may already exist at its future canonical path

If the existing P0-2 Cycle byte content is identical to staged accepted P0-2 Cycle, adopt it as the canonical target during migration.
If it differs, STOP with `BLOCKED_CANONICAL_INPUT_COLLISION`; do not overwrite silently.

If any unrelated file/source appears outside the expected paths before mutation, classify it before proceeding.
Unknown source/config must not be silently deleted or absorbed.

## canonical repository structure

At minimum:

```text
AGENTS.md
.gitignore

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
│           ├── 20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.cycle.md
│           └── 20260826_1038_aiscc-p0-4-bootstrap-environment-gap-and-rework-1.cycle.md
├── tasks/
│   ├── active/
│   └── done/
│       ├── 20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.md
│       ├── 20260826_0937_aiscc-repository-bootstrap-canonical-authority-and-git-policy-1.md
│       └── 20260826_1038_aiscc-repository-bootstrap-canonical-authority-and-git-policy-rework-1.md
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

Empty ignored directories do not require `.gitkeep`.

## canonical migration mapping

### rules

- staged `10_AISCC_RULES__AGENT_AUTHORITY_AND_TRANSPORT.md`
  → `.aiassistant/rules/AISCC_AGENTS.md`
- staged `30_AISCC_RULES__IDE_EXECUTOR_REPORT_EXPORT.md`
  → `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- staged `31_AISCC_RULES__ASSET_GIT_AND_ENCODING_POLICY.md`
  → `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- staged `32_AISCC_RULES__PROJECT_SOURCE_MIRROR.md`
  → `.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md`
- staged `33_AISCC_RULES__DOCUMENT_LANGUAGE_POLICY.md`
  → `.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md`

### command center

- staged `20...README`
  → `.aiassistant/records/command-center/README.md`
- staged `21...WORKFLOW`
  → `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
- staged `22...TASK_FILE_TEMPLATE`
  → `.aiassistant/records/command-center/TASK_FILE_TEMPLATE.md`
- staged `23...SHORT_EXECUTOR_PROMPT_TEMPLATE`
  → `.aiassistant/records/command-center/SHORT_EXECUTOR_PROMPT_TEMPLATE.md`
- staged `24...JUDGMENT_RUBRIC`
  → `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md`
- staged `25...CYCLE_RECORD_TEMPLATE`
  → `.aiassistant/records/command-center/CYCLE_RECORD_TEMPLATE.md`
- staged `26...NEXT_ACTION_SELECTION_RUBRIC`
  → `.aiassistant/records/command-center/NEXT_ACTION_SELECTION_RUBRIC.md`

### historical bootstrap

- staged `00...SEED_INDEX`
  → `.aiassistant/records/aiscc/bootstrap/AISCC_BOOTSTRAP_SEED_V1_INDEX.md`
- staged `01...PROJECT_BOOTSTRAP`
  → `.aiassistant/records/aiscc/bootstrap/AISCC_PROJECT_BOOTSTRAP_GENESIS.md`

These become historical genesis provenance after repository canonical is established, not moving policy authority.

### tasks / cycles

- staged accepted P0-2 Task
  → `.aiassistant/tasks/done/20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.md`
- staged predecessor blocked P0-4 Task
  → `.aiassistant/tasks/done/20260826_0937_aiscc-repository-bootstrap-canonical-authority-and-git-policy-1.md`
- current rework Task after executor turn complete
  → `.aiassistant/tasks/done/20260826_1038_aiscc-repository-bootstrap-canonical-authority-and-git-policy-rework-1.md`
- staged P0-2 Cycle
  → `.aiassistant/records/aiscc/cycles/20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.cycle.md`
- staged environment-gap Cycle
  → `.aiassistant/records/aiscc/cycles/20260826_1038_aiscc-p0-4-bootstrap-environment-gap-and-rework-1.cycle.md`

### accepted P0-2 baselines

- `AISCC_PRODUCT_THESIS.md`
  → `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
- `AISCC_PRIOR_ART_BOUNDARY.md`
  → `.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md`
- `AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
  → `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`

Preserve accepted substantive body.
Update candidate metadata/status to repository canonical accepted status without adding unsupported new external factual claims.

## repository-root `AGENTS.md`

Decision:

```text
TRACK
role: THIN_TRANSPORT_BOOTSTRAP
policy_authority: No
```

Do not duplicate canonical rule bodies.

## `.gitignore`

Required exact initial entries:

```gitignore
.idea/
.aiassistant/bootstrap-input/
.aiassistant/tasks/active/
.aiassistant/reports/target/
.aiassistant/project-sources/bundles/
```

Do not add broad source/build/runtime ignores without an owning Task.

## Current State requirements

`.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md` must state:

- AISCC accepted thesis reference
- P0-1 `ACCEPTED / CLOSED`
- P0-2 `ACCEPTED / CLOSED`
- P0-3 `HUMAN_CONFIRMED / CLOSED`
- P0-4 rework in execution / accepted after Command Center judgment
- repository was Human-created as an empty public remote clone before P0-4 canonicalization
- local repository canonical authority becomes editable source after P0-4 acceptance
- Browser Project Source remains Bootstrap Seed v1 until P0-5 complete replacement
- `AISCC-COMPETITION-PUBLIC-RUNTIME-V1`
- `AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1` with `NOT_EXECUTED`
- no product runtime/provider resource/deployment exists merely because repository is initialized
- next action after P0-4 acceptance = P0-5

## Decision Register requirements

At minimum:

1. custom explicit state machine / no LangGraph core
2. P0-2 product thesis acceptance
3. prior-art / `DO-NOT-CLAIM`
4. `AISCC-COMPETITION-PUBLIC-RUNTIME-V1`
5. `AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1`
6. Bootstrap Seed v1 temporary authority until P0-5 complete replacement
7. tracked thin `AGENTS.md`
8. local canonical vs Browser Project Source mirror authority split
9. P1 safeguard implementation-before-release invariant
10. P0-4 environment convention:
    - IntelliJ execution environment
    - accepted repository root
    - Human-created empty public Git remote clone
    - `.idea/` ignored local metadata
    - `.aiassistant/bootstrap-input/` temporary ignored staging

Environment convention is operational bootstrap metadata, not product architecture.

## NEXT_ACTIONS requirements

Stable beginning:

```text
P0-5 First Project Source Mirror v1
→ P1-1 Core Domain / State Machine Design
→ P1 security/runtime design
→ P1 dedicated security/runtime safeguard implementation + verification
→ remaining Governance Kernel
→ P2 Demonstration / Self-Dogfooding
→ P3 Proof / public release / submission
```

Assign stable identifiers/titles.

## Project Source registry

Create tracked:

```text
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
```

P0-5 still owns first manifest/bundle generation and Browser Project complete active-set replacement.

## Git actions authorized

Authorized local operations after preflight:

- create `.gitignore`
- create/update authorized canonical files
- `git status`
- `git diff`
- `git diff --check`
- `git ls-files`
- local hash/integrity checks
- `git add` only exact authorized P0-4 tracked files
- one local initial canonical commit

Do NOT run `git init` in the expected state because repository already exists.

Do NOT alter/remove `origin`.

No remote operation.

If Git author identity is missing:

```text
HUMAN_GIT_IDENTITY_REQUIRED
```

Do not modify global Git config or invent identity.

Recommended local initial commit:

```text
chore: bootstrap AISCC canonical governance repository

Establish the AISCC canonical authority layout in the Human-created empty
repository, migrate accepted bootstrap/P0-2 provenance, record project
decisions and queue invariants, and keep temporary staging and IDE state
outside tracked provenance.

Defer Project Source replacement to P0-5 and defer runtime, deployment,
credentials, provider resources, and billing controls to their owner tasks.
```

## evidence contract

### executor_required — `STAGING_INPUT_INTEGRITY`

- manifest exists
- staged file count = `21`
- each SHA-256 matches manifest
- no missing/reconstructed input

### executor_required — `WORKSPACE_PREFLIGHT`

- exact repository root
- `.git` exists
- `main`
- zero local commits
- zero tracked files before mutation
- exact single `origin`
- no network command executed
- expected `.idea/` classified as local metadata

### executor_required — `CANONICAL_MIGRATION`

- exact source→canonical mapping
- baseline substantive content preserved
- P0-2 accepted status canonicalized
- predecessor blocked Task + environment-gap Cycle preserved

### executor_required — `GIT_POLICY`

- required `.gitignore` entries
- ignored staging and IDE metadata
- tracked canonical paths not ignored
- `AGENTS.md` tracked/thin

### executor_required — `QUEUE_AND_DECISION_CONSISTENCY`

- runtime/deployment decisions correctly classified
- P1 safeguard implementation + verification explicit
- P3-3 not safeguard first implementation
- P0-5 next

### executor_required — `DOCUMENT_INTEGRITY`

- UTF-8
- Markdown fence parity
- no unintended control chars
- `git diff --check` or equivalent
- canonical path references valid

### executor_required — `GIT_LOCAL_PROVENANCE`

- one local initial commit
- authorized file inventory only
- commit hash recorded
- no remote operation
- if blocked only by human Git identity, classify honestly

### human_owned — `HUMAN_VERIFICATION`

After executor bundle submission, Command Center/Human accepts or requires rework.

### not_required

- product build/test
- database
- HTTP/browser runtime
- LLM inference
- security sandbox runtime
- provider verification
- deployment
- billing
- P0-5 upload

### forbidden

- remote Git action
- provider/credential/deployment action
- Browser Project Source mutation
- P0-5 execution
- product/security runtime implementation
- unrelated source/test expansion

## proof non-substitution

- expected `origin` presence != remote operation
- local commit != GitHub push/publication evidence
- staged input package != canonical authority
- canonical migration != P0-5 mirror sync
- accepted deployment direction != provider capability verification
- `.idea/` existence != source change
- P1 security design != safeguard implementation
- safeguard implementation != runtime verification
- executor report != human acceptance

## mandatory stop

Stop if:

- staging count/hash mismatch
- repository root differs
- `.git` absent
- branch not `main`
- any local commit already exists
- tracked file already exists unexpectedly
- `origin` differs or extra remote exists
- existing P0-2 canonical Cycle differs from staged accepted Cycle
- unrelated source/config collision cannot be classified
- secret/private source found
- authority conflict
- Git identity blocks required commit
- task would require network/provider/deployment
- `EVIDENCE_SCOPE_EXPANSION_REQUIRED`

After a named blocker: minimal evidence/report/export/safe stop only.

## export bundle

Target:

```text
.aiassistant/reports/target/20260826_1038_aiscc-repository-bootstrap-canonical-authority-and-git-policy-rework-1/
```

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- changed files preserving repository-relative paths
- `REMOVED_FILES.md` only when actual canonical deletion occurs

Do not include `.git/`, `.idea/`, bootstrap staging, secrets, caches, or P0-5 generated bundle.

## Task lifecycle

On executor completion:

```text
.aiassistant/tasks/active/20260826_1038_aiscc-repository-bootstrap-canonical-authority-and-git-policy-rework-1.md
→
.aiassistant/tasks/done/20260826_1038_aiscc-repository-bootstrap-canonical-authority-and-git-policy-rework-1.md
```

The predecessor blocked Task is independently preserved in `tasks/done`.

## report requirements

Include:

- exact preflight
- expected existing `.git` / `origin` classification
- staging manifest and 21-file hash verification
- explicit read inventory
- source→canonical mapping
- `.idea/` and bootstrap staging ignore treatment
- product source changes: none
- governance/provenance changes
- repository configuration changes
- added/modified/removed files
- accepted P0-2 migration
- predecessor blocked Task provenance
- Current State / Decision Register / Next Actions
- safeguard queue invariant
- local commit evidence
- no remote operation
- forbidden-not-run
- human pending
- rollback/revert
- preserved exact paths
- next = P0-5 if accepted

## accept criteria

- Human-created empty repository accepted exactly as precondition
- exact staging input integrity passes
- required canonical repository exists
- no unrelated tracked source
- `.idea/` and bootstrap staging ignored
- accepted P0-2 provenance migrated
- predecessor blocked P0-4 provenance retained
- decisions and queue correct
- local initial canonical commit created
- no remote operation
- P0-5 not executed
- target bundle complete

## hold/reject criteria

- input hash mismatch
- wrong repository/root/remote/history
- staged input committed
- `.idea/` committed
- accepted baseline substantive drift
- predecessor provenance discarded
- Browser Project Source changed
- P0-5 executed
- remote operation
- provider/deployment/credential/billing action
- P1 safeguard implementation stage omitted
- P3-3 first safeguard implementation
- secret/private source included
- false human acceptance/commit/runtime claim

## rollback

If rejected before local commit:

- revert/remove only P0-4 rework-created canonical files;
- preserve the Human-created `.git`, `origin`, `.idea/`, and unrelated Human preconditions;
- do not delete the GitHub repository.

If rejected after local initial commit:

- do not rewrite history automatically;
- report exact commit;
- Command Center chooses a corrective commit or explicit repository recreation.

## preserved artifacts after acceptance

Preserve exact canonical paths:

- `AGENTS.md`
- `.gitignore`
- `.aiassistant/rules/**`
- `.aiassistant/records/command-center/**`
- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
- `.aiassistant/records/aiscc/bootstrap/**`
- `.aiassistant/records/aiscc/cycles/20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.cycle.md`
- `.aiassistant/records/aiscc/cycles/20260826_1038_aiscc-p0-4-bootstrap-environment-gap-and-rework-1.cycle.md`
- `.aiassistant/tasks/done/20260826_0122_aiscc-product-thesis-prior-art-and-competition-public-runtime-baseline-1.md`
- `.aiassistant/tasks/done/20260826_0937_aiscc-repository-bootstrap-canonical-authority-and-git-policy-1.md`
- `.aiassistant/tasks/done/20260826_1038_aiscc-repository-bootstrap-canonical-authority-and-git-policy-rework-1.md`
- `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
- `.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md`
- `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
- `.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md`

Do not preserve after successful acceptance:

- `.aiassistant/bootstrap-input/p0-4/**`
- `20260826_0122_reports.md`
- temporary target bundle unless judgment explicitly requires it

## next action after acceptance

```text
P0-5 First Project Source Mirror v1
```
