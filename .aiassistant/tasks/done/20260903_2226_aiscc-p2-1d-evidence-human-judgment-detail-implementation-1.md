# 작업지시서: P2-1D Evidence + Human/Judgment detail implementation

## meta

- task_id: `20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1`
- created_at: `2026-09-03T22:26:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P2-1D — Evidence + Human/Judgment detail`
- work_type: `FRONTEND_IMPLEMENTATION`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `NOT_APPLICABLE`
- primary_semantic_owner: `read-only Evidence + Human/Judgment projection inside the canonical WorkRun detail page`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- current accepted HEAD: `08368eceac625c9a74b4347021ed65540cb08b3c`
- current accepted tree: `c7c601677eb2a4ca2fa7b594465ebd16ed8da9f4`
- predecessor_terminal_cycle: `.aiassistant/records/aiscc/cycles/20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle.md`
- predecessor_handoff: `.aiassistant/reports/aiscc/20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1.md`
- target_bundle: `.aiassistant/reports/target/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1/`
- fresh_chat_policy: `NEW_IDE_CHAT_REQUIRED / NEW_P2_1D_IMPLEMENTATION_SLICE`
- implementation_commit_authority: `NONE`
- success_boundary: `P2_1D_IMPLEMENTATION_CANDIDATE / COMMAND_CENTER_REVIEW_REQUIRED`

## 0. current accepted authority

Current accepted persistence lineage:

```text
P2-1A:
4ea1fe6f7cb8e11ff5ccfde70462eba931c4071e
feat(command-center): complete P2-1A read API foundation

P2-1B:
62a3c5135a12afc38ba32e4c5f651c1f1b007549
feat(command-center): complete P2-1B shell and project queue

P2-1C:
08368eceac625c9a74b4347021ed65540cb08b3c
feat(command-center): complete P2-1C work run detail
```

Current phase:

```text
P2:
STARTED / P2-1 ACTIVE

P2-1A:
ACCEPTED / PERSISTED

P2-1B:
ACCEPTED / PERSISTED

P2-1C:
HUMAN_PROVIDED / ACCEPTED / PERSISTED

P2-1D:
ENTRY_AUTHORIZED / NOT_STARTED

P2-1E:
NOT_STARTED

P2-2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

P2-1D is the only semantic slice authorized by this Task.

Do not start P2-1E or P2-2.

Accepted P2-1 frontend substrate:

```text
HTML-first
same-process FastAPI
plain CSS
minimal progressive JavaScript
no Node/npm/SPA framework
LOCAL_PRIVATE_ONLY
read-only first
```

Core semantic non-substitution:

```text
WorkflowState != ExecutionStatus
EvidenceCandidate != AdmittedEvidence
Agent claim != AdmittedEvidence

HumanGateStatus != HumanResult
HumanResult != Judgment
Judgment != TransitionDecision
Judgment != WorkflowState

EXECUTOR_COMPLETED != WorkRun ACCEPTED
tasks/done != accepted
Executor PASS != Command Center acceptance
```

## 1. exact goal

1. transport this Task plus the exact P2-1C terminal Cycle and Handoff into the repository;
2. verify exact `main` / accepted HEAD / empty index / post-P2-1C dirty-workspace provenance before any product mutation;
3. inspect the current accepted P2-1A evidence + human/judgment DTO/read-contract implementation and the current accepted P2-1C WorkRun detail page/tests before changing source;
4. extend the existing canonical WorkRun detail page:
   - `GET /command-center/work-runs/{work_run_id}`
   - do not create a competing second WorkRun detail page;
5. consume only the already accepted P2-1A read endpoints:
   - `GET /v1/command-center/work-runs/{work_run_id}/evidence`
   - `GET /v1/command-center/work-runs/{work_run_id}/human-judgment`;
6. render Evidence semantics without collapsing candidate/admission/admitted/satisfaction distinctions;
7. render Human Gate / Human Result / Judgment / Transition Effect as separate authority dimensions;
8. preserve P2-1C summary-current-authority, stale/retained data, ETag/304, polling, hidden-tab, terminal-stop and recovery behavior;
9. preserve Korean-first visible copy, safe DOM construction and responsive layout;
10. add/update focused unit/source and integration tests;
11. execute required static and local runtime evidence without expanding environment scope;
12. export the exact candidate bundle;
13. move this Task from `tasks/active` to matching `tasks/done`;
14. stop without Git staging/commit/push/deployment;
15. leave Human Browser/Visual QA as `HUMAN_PENDING` for a later Command Center gate.

## 2. explicit non-goals / forbidden product behavior

This Task is read-only UI projection work.

Do not implement or expose:

```text
HumanResult submission
approve/rework/reject buttons
Judgment mutation
evidence admission mutation
workflow mutation
Task creation/mutation
new Task authority
repository Markdown Cycle indexing
Cycle/NextAction UI implementation
P2-1E behavior
P2-2 behavior
public/shared operator exposure
```

Do not add:

```text
Node
npm
SPA framework
new frontend dependency
new Python package dependency
migration
database table
authentication package
WebSocket/SSE
```

Do not use a UI convenience requirement to change accepted P1/P2-1A semantic ownership.

If accepted P2-1A DTO/API semantics are insufficient:

```text
P2_1A_API_CONTRACT_CHANGE_REQUIRED
```

STOP before modifying backend read authority.

## 3. new IDE chat gate

This Task MUST run in a genuinely new IDE Executor chat.

Reason:

```text
new timestamped Task
new P2 semantic implementation slice
P2-1C implementation/persistence chat history must not be reused as mutation authority
```

Before source mutation report:

```text
SESSION_AUTHORITY:
NEW_P2_1D_IMPLEMENTATION_CHAT / PASS
```

Failure:

```text
BLOCKED_REQUIRED_EVIDENCE / NEW_IMPLEMENTATION_CHAT_REQUIRED
```

No product mutation after a failed session gate.

## 4. Downloads transport

Transport exactly three files after an all-or-nothing precheck.

### 4.1 current Task

```text
source:
C:\Users\oracl\Downloads\20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md

destination:
.aiassistant/tasks/active/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md
```

Task active destination must be absent before transport.

### 4.2 P2-1C terminal Cycle

```text
source:
C:\Users\oracl\Downloads\20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle(1).md

destination:
.aiassistant/records/aiscc/cycles/20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle.md

expected SHA-256:
9af3a5fbedef5478e58c06cb114997aee15558d56c8aede55a5bb9e9b670ee4c
```

### 4.3 P2-1C completion → P2-1D entry Handoff

```text
source:
C:\Users\oracl\Downloads\20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1(1).md

destination:
.aiassistant/reports/aiscc/20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1.md

expected SHA-256:
e88df2b56ad301175619baee4d4dcc0ccc8267229ebd47a6a619b76482758a9c
```

For each predecessor governance artifact:

- if canonical destination is absent:
  - exact Downloads source must exist;
  - exact SHA-256 must match;
  - move/copy only to the exact canonical destination specified above;
- if canonical destination already exists:
  - exact destination SHA-256 must match;
  - do not duplicate transport;
- any mismatch or alternate file identity:

```text
TRANSPORT_PRECONDITION_FAILED
```

Do not search or guess alternate Downloads filenames.

Do not partially transport after a failed all-or-nothing precheck.

## 5. dirty-workspace preflight — MUST run before product mutation

Before transport, and again after transport, run exact:

```text
git status --short --untracked-files=all
git branch --show-current
git rev-parse HEAD
git diff --cached --name-only
```

Required baseline:

```text
repository:
ai-software-command-center

branch:
main

HEAD:
08368eceac625c9a74b4347021ed65540cb08b3c

index:
empty
```

Post-P2-1C reported residue before this Task:

```text
133 untracked __pycache__ / .pyc paths
+
2 pre-existing untracked P2-1B governance artifacts
```

Expected P2-1B governance candidates to identify exactly:

```text
.aiassistant/records/aiscc/cycles/20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md

.aiassistant/reports/aiscc/20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md
```

Important:

- the two exact paths above are expected by Command Center inference from established lineage, but were not directly enumerated in the predecessor Executor post-commit report;
- verify their exact identities from actual `git status`;
- verify every other pre-existing untracked residue belongs only to the known Python cache class;
- after predecessor transport, the `2218` Cycle and `2220` Handoff are additional expected governance/provenance dirt;
- the active Task is ignored and should not appear as Git-visible product dirt.

If any unrelated product/source/test/config/migration/governance path exists:

```text
DIRTY_WORKSPACE_MIXED / COMMAND_CENTER_REVIEW_REQUIRED
```

STOP before product mutation.

Do not normalize status with:

```text
git clean
git restore
git checkout
git reset
git stash
```

Do not delete the known Python cache residue merely to make status look clean.

Do not stage inherited P2-1B/P2-1C governance artifacts.

For Python execution in this Task, prefer per-command:

```text
PYTHONDONTWRITEBYTECODE=1
```

or the platform-equivalent process environment so this Task does not intentionally expand visible `__pycache__/.pyc` residue.

Do not convert this into a broad cleanup task.

## 6. minimum authoritative context

Read exact canonical documents:

```text
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md
.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md

.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_EVIDENCE_ADMISSION.md

.aiassistant/records/aiscc/cycles/20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle.md
.aiassistant/reports/aiscc/20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1.md

.aiassistant/tasks/done/20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1.md
.aiassistant/tasks/done/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.md
.aiassistant/tasks/done/20260903_1949_aiscc-p2-1c-retained-detail-stale-current-authority-labeling-rework-1.md
.aiassistant/tasks/active/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md
```

If the exact P2-1A implementation Task is unavailable at the repository path above, use current accepted source as authoritative runtime evidence and record the missing historical Task as a provenance limitation.

Do not bulk-read unrelated tasks/cycles/logs.

## 7. exact source inspection before mutation

Inspect current accepted source at HEAD before mutation.

### 7.1 accepted P2-1A read authority — read-only in this Task

Read:

```text
src/aiscc/api/routes/command_center.py
src/aiscc/command_center/read_models.py
src/aiscc/command_center/queries.py
src/aiscc/command_center/postgres_queries.py
src/aiscc/command_center/privacy.py
```

These paths are protected and MUST remain byte-identical in this Task.

Confirm the actual DTO/JSON field shapes for:

```text
GET /v1/command-center/work-runs/{work_run_id}/evidence

GET /v1/command-center/work-runs/{work_run_id}/human-judgment
```

Do not infer missing field names from this Task when current accepted source already defines them.

### 7.2 accepted P2-1C page/test source

Inspect:

```text
src/aiscc/api/routes/command_center_ui.py
src/aiscc/command_center/web.py
tests/integration/command_center/test_web_ui.py
tests/unit/command_center/test_web_shell.py
```

Expected accepted P2-1C identities before mutation:

```text
src/aiscc/api/routes/command_center_ui.py
82d73e29ed5c185948ba82a5fc79083cafdb77b36b3f30760f570c295af01fd2

src/aiscc/command_center/web.py
949f548548d2a92b260e2bb56fd99f4defa1188420263cc61ede49451c05a779

tests/integration/command_center/test_web_ui.py
1eb8d100be9b64c8c2ecd1779f5b67b90862ed96c23be2861b3f809e28a2f4d4

tests/unit/command_center/test_web_shell.py
7bef092098bbf9867378a18520d051fd1c1c6f9c91e050a5d53b481c449da382
```

Accepted product/test aggregate:

```text
2e4ca49afcd074aa2eac768b6f966d3d48044067917328a35c7839e078b35af3
```

If actual clean-HEAD bytes do not match these accepted identities:

```text
ACCEPTED_BASELINE_IDENTITY_MISMATCH
```

STOP before product mutation.

### 7.3 protected app composition

Read only if needed to confirm existing route composition:

```text
src/aiscc/api/app.py
```

Expected accepted identity from the P2-1C entry contract:

```text
34b9216342dc256fd319ab5c594799b9aa6784c35bc13a8b01595d4204d572f0
```

It MUST remain byte-identical.

If P2-1D cannot be implemented without changing composition:

```text
IMPLEMENTATION_PATH_EXPANSION_REQUIRED
```

STOP before modifying `src/aiscc/api/app.py`.

## 8. allowed product/test mutation

Only these existing paths are authorized for mutation:

```text
src/aiscc/api/routes/command_center_ui.py
src/aiscc/command_center/web.py
tests/integration/command_center/test_web_ui.py
tests/unit/command_center/test_web_shell.py
```

No new product/test path is authorized.

No package/config/migration path is authorized.

Protected P2-1A read-authority files in Section 7.1 must remain byte-identical.

If implementation requires any additional path:

```text
IMPLEMENTATION_PATH_EXPANSION_REQUIRED
```

STOP before adding/modifying that path.

## 9. exact P2-1D route/read boundary

Do not add a second WorkRun detail HTML authority.

Continue using exactly:

```text
GET /command-center/work-runs/{work_run_id}
```

The existing P2-1C page already owns:

```text
WorkRun / Task reference
WorkflowState / state_version
RuntimeMode
Task / Scope
blocker safe projection

TransitionRequest
TransitionEvaluation
guards
TransitionDecision

ExecutionAttempt
ExecutionOperation
ExecutionStatus
```

P2-1D extends this same page.

P2-1D may add browser reads only to:

```text
GET /v1/command-center/work-runs/{work_run_id}/evidence
GET /v1/command-center/work-runs/{work_run_id}/human-judgment
```

Do not introduce a new backend route or alternate read owner.

## 10. Evidence rendering contract

Use the exact accepted P2-1A DTO field names discovered from current source.

The visible model MUST preserve these distinctions:

```text
checkpoint owner order
requirement-set ordered refs

EvidenceRequirement
requirement applicability

EvidenceCandidate
admission decision
AdmittedEvidence
requirement/set satisfaction

owner
profile / obligation
semantic owner
type / channel where the DTO exposes it
freshness
applicability
safe provenance
checkpoint / requirement binding
admission outcome / reason
safe content metadata only
set satisfaction / attestation separately
```

Non-substitution:

```text
EvidenceCandidate != AdmittedEvidence
admission decision != admitted evidence
AdmittedEvidence != requirement satisfied
requirement satisfied != set satisfied
Agent claim != AdmittedEvidence
```

Forbidden UI content/inference:

```text
evidence body
private producer content
private payload/body refs
admitted evidence == set satisfied inference
unsatisfied evidence == rejected Judgment inference
missing evidence == failed WorkRun inference
```

If the accepted endpoint returns no checkpoint / requirement / candidate / admitted evidence, render an explicit truthful empty/absence state.

Do not fabricate authority fields.

## 11. Human/Judgment rendering contract

The accepted P2-1A read contract exposes four independent presentation dimensions:

```text
human_gate
human_result
judgment
transition_effect
```

Render them as four visibly distinct cards/sections.

### 11.1 Human Gate

Preserve exact source fields such as, when present:

```text
presence
HumanGateStatus
HumanGateSuspensionStatus
gate identity/version
owner/applicability metadata
safe provenance
```

Do not display or reconstruct forbidden Human identity/auth authority.

### 11.2 Human Result

Preserve exact source presence and exact source result kind/outcome.

Do not infer Judgment from HumanResult.

```text
HumanResult != Judgment
```

### 11.3 Judgment

Important accepted contract:

```text
No source enum named JudgmentStatus may be invented.
```

Use:

```text
explicit presence
+
exact JudgmentKind
+
accepted safe owner policy / reason / provenance fields when present
```

Do not create a generic synthetic `status` label that collapses the model.

```text
Judgment != TransitionDecision
Judgment != WorkflowState
```

### 11.4 Transition Effect

Render the accepted read DTO's transition-effect/current effect information separately.

Do not reinterpret a Judgment as an already-admitted state transition.

### 11.5 Forbidden Human/Judgment display

Do not expose:

```text
Human principal_id
authentication/action authority refs
private comment ref/hash/body
private Human content
```

If a dimension is absent, show explicit absence/presence semantics rather than inventing a status.

## 12. P2-1C current/stale authority invariant — MUST be preserved and extended

Accepted P2-1C behavior:

```text
manual refresh:
available

automatic:
10-second visible/nonterminal polling

hidden tab:
polling stopped

terminal WorkRun:
automatic polling stopped

ETag:
endpoint-scoped / independent

304:
does not destroy last successful data
```

P2-1D adds two endpoint-scoped read states:

```text
evidence
human-judgment
```

Each endpoint MUST keep independent:

```text
ETag
last successful payload/DOM
read state
failure state
```

### 12.1 summary authority

The WorkRun summary remains authoritative for whether the page may represent dependent sections as newly current.

If the summary current authority cannot be established in a refresh cycle:

```text
do not apply concurrent fresh transition payload as current
do not apply concurrent fresh execution payload as current
do not apply concurrent fresh evidence payload as current
do not apply concurrent fresh human-judgment payload as current
```

If a last successful section DOM exists:

```text
retain it
+
downgrade its visible label to truthful retained/stale/refresh-failed semantics
+
do not call it "최신" or otherwise newly current
```

A later successful summary refresh may restore current labels only when the corresponding endpoint state is also valid for that refresh logic.

### 12.2 endpoint-local failure

If summary succeeds but one dependent endpoint fails:

- do not destroy that endpoint's last successful DOM;
- mark only that endpoint/section retained/stale/refresh-failed;
- other successful independent sections may remain/currently refresh according to accepted page authority;
- 304 preserves the last successful endpoint data and is not an error.

Do not collapse all five reads into one generic `loaded` boolean.

### 12.3 concurrency

Inspect the current P2-1C implementation and P2-1A `meta.source_revisions` / consistency contract before changing refresh coordination.

Do not blindly clone a stale/current algorithm if the evidence or human/judgment DTO has a materially different dependency.

If a trustworthy current-authority rule cannot be implemented within the four allowed UI/test paths without inventing cross-owner semantics:

```text
P2_1D_CURRENT_AUTHORITY_CONTRACT_GAP
```

STOP and report.

## 13. visible UX requirements

User-facing copy:

```text
Korean-first
```

Code/domain identifiers may remain exact English identifiers.

Required hierarchy:

1. existing WorkRun summary / Task / Scope
2. existing Transition detail
3. existing Execution detail
4. Evidence detail
5. Human / Judgment detail

Do not make evidence or judgment appear to supersede workflow/execution authority.

Responsive behavior must preserve P2-1B/P2-1C accepted layout:

```text
no horizontal-scroll-dependent primary layout
long IDs wrap inside value regions
existing <=1180 / <=720 responsive behavior preserved where applicable
```

Use compact cards/dl/rows consistent with the existing WorkRun detail design language.

Do not redesign unrelated P2-1B/P2-1C UI.

Required truthful states include:

```text
loading
empty/absent
current
retained/stale after refresh failure
error before any successful data
304 unchanged
```

No mutation buttons.

## 14. safe DOM / frontend security

API-derived content MUST use safe DOM/text construction.

Forbidden for API-derived payloads:

```text
innerHTML
outerHTML
insertAdjacentHTML
eval
new Function
document.write
```

unless current source uses a provably static literal path unrelated to API data; do not introduce new API-derived use.

Preferred:

```text
createElement
textContent
setAttribute with fixed attribute names and validated/safe values
replaceChildren
```

Do not build executable HTML from evidence/Human/Judgment fields.

## 15. validation and evidence

Use repository-local environment only.

Do not install packages or use external network.

For Python-running commands, avoid intentionally creating more visible `.pyc` residue as described in Section 5.

### 15.1 STATIC_SOURCE

Required:

- inspect exact P2-1A DTO/read source;
- inspect exact current P2-1C page/test source;
- verify protected backend read-authority paths remain byte-identical;
- verify no mutation control or new backend authority was introduced;
- verify safe DOM usage.

### 15.2 focused unit/source tests

Add/update tests proving at minimum:

1. EvidenceRequirement / EvidenceCandidate / admission decision / AdmittedEvidence / satisfaction are not collapsed.
2. admitted evidence is not rendered as automatic set satisfaction.
3. unsatisfied/missing evidence is not rendered as rejected Judgment.
4. evidence body/private producer content is not rendered.
5. Human Gate / Human Result / Judgment / Transition Effect render as four independent dimensions.
6. HumanResult does not populate Judgment.
7. no fabricated `JudgmentStatus` exists; absent Judgment uses presence semantics and present Judgment uses exact `JudgmentKind`.
8. Judgment is not rendered as TransitionDecision or WorkflowState.
9. private Human principal/comment/action-authority content is not rendered.
10. evidence and human/judgment empty states are explicit.
11. endpoint-specific 304 preserves prior successful DOM.
12. endpoint-specific failure preserves prior successful DOM with stale/retained label.
13. summary failure prevents concurrently successful evidence/human-judgment payloads from being labeled/applied as newly current.
14. later recovery can restore current labels without destroying unchanged sections.
15. existing visible/nonterminal polling behavior remains 10 seconds.
16. hidden-tab polling stop remains.
17. terminal WorkRun polling stop remains.
18. no mutation control is present.
19. API-derived content is not inserted through unsafe HTML/eval paths.
20. P2-1C transition/execution semantics remain covered.

### 15.3 affected integration tests

Run the existing affected Command Center integration tests.

Required coverage:

- canonical WorkRun detail route still serves;
- browser code references only accepted read endpoints;
- Evidence endpoint integration path is represented correctly;
- Human/Judgment endpoint integration path is represented correctly;
- unsupported/missing read states produce truthful safe UI behavior;
- P2-1C existing routes/assets remain available;
- no mutation route is added.

Use only the existing repository-local test harness.

If integration proof requires a new DB/container/image/package/network environment not already available to this implementation turn:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

STOP before creating that environment.

### 15.4 local HTTP/runtime proof

Because this Task changes browser-facing data application behavior, execute local loopback HTTP/runtime proof only if it can use the existing repository-local P2-1C/P2-1A runtime harness without new environment expansion.

Verify at minimum:

```text
GET /command-center/work-runs/{work_run_id}
200

existing assets:
200

browser read calls:
summary
transitions
execution
evidence
human-judgment

manual refresh:
available

304:
last successful data retained

summary current-authority failure:
dependent sections not newly labeled current

endpoint-local failure:
last-successful section retained with truthful stale label

recovery:
current label can be restored when authority is re-established
```

Prove no authoritative DB/event mutation from page GET/read polling if the existing harness already supports this observation.

If local HTTP runtime requires a newly created Docker DB/server environment beyond the current implementation harness:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

STOP rather than manufacturing substitute proof.

Do not create the later Human QA disposable runtime in this Task.

### 15.5 static checks

Required:

```text
Ruff on changed Python scope
mypy on changed Python scope
targeted py_compile/compileall or repository-equivalent
git diff --check
```

### 15.6 regression

After targeted checks pass, run the repository's existing unit + integration regression suite only if it requires no new package/network/environment expansion.

Report exact pass count.

If unavailable because of environment expansion:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

Do not substitute another proof type.

## 16. evidence contract

### executor_required

```text
SESSION_AUTHORITY
STATIC_SOURCE
FRONTEND_SOURCE_TEST / UNIT_TEST
affected INTEGRATION_TEST
LOCAL_HTTP_RUNTIME when available in existing accepted harness
STATIC_CHECK
PUBLIC_PROVENANCE
```

### reuse_allowed

P2-1A and P2-1C accepted evidence may be reused only for unchanged owner semantics and unchanged source identities.

It does not prove the new P2-1D rendering behavior.

### human_owned

```text
BROWSER_RUNTIME / VISUAL / USABILITY QA
```

Status in this Task:

```text
HUMAN_PENDING
```

Do not execute or claim Human Browser QA.

Human QA may be opened only after Browser Command Center substantive source/runtime acceptance.

### not_required

```text
external network
real provider call
deployment
public exposure
P2-1E Cycle/NextAction
P2-2 synthetic demo
Git commit
```

### forbidden

```text
HumanResult submission
Judgment mutation
Evidence admission mutation
Workflow mutation
new backend read authority
package install
migration
Git staging/commit/push
deployment
broad workspace cleanup
```

### proof non-substitution

```text
P2-1A endpoint exists != P2-1D UI tested
unit/source test != local HTTP runtime
local HTTP runtime != Human Browser/Visual QA
executor report != Human acceptance
EvidenceCandidate != AdmittedEvidence
HumanResult != Judgment
Judgment != TransitionDecision
Judgment != WorkflowState
```

## 17. mandatory stop conditions

STOP before additional mutation when any occurs:

```text
HEAD != 08368eceac625c9a74b4347021ed65540cb08b3c
branch != main
index not empty at preflight
accepted P2-1C source identity mismatch
unexpected product/source/test/config/migration dirt
unexpected governance dirt outside known/transported provenance
P2-1A backend read contract change required
new product/test path required
src/aiscc/api/app.py change required
new package/dependency required
migration/table required
current-authority semantics cannot be represented without inventing cross-owner authority
local integration/HTTP proof requires new environment
policy baseline conflict
secret/private data encountered
```

Classify precisely:

```text
DIRTY_WORKSPACE_MIXED
P2_1A_API_CONTRACT_CHANGE_REQUIRED
IMPLEMENTATION_PATH_EXPANSION_REQUIRED
P2_1D_CURRENT_AUTHORITY_CONTRACT_GAP
EVIDENCE_SCOPE_EXPANSION_REQUIRED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
BLOCKED_MISSING_ARTIFACT
```

After a named blocker:

- collect only minimum source/workspace evidence;
- complete report/export;
- move Task to done if executor turn is submit-ready;
- do not continue unrelated tests/runtime/environment work;
- do not clean/reset/stash.

## 18. repository / Git restrictions

Forbidden unless a later exact Task authorizes:

```text
git add
git commit
git restore
git checkout
git reset
git clean
git stash
git push
git fetch
git pull
```

Allowed read-only Git inspection:

```text
git status
git diff
git diff --check
git show
git rev-parse
git branch --show-current
git ls-files
```

No push/deployment.

## 19. required export bundle

Target:

```text
.aiassistant/reports/target/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
P2_1D_UI_CONTRACT_EVIDENCE.md
HTTP_RUNTIME_EVIDENCE.md
```

`HTTP_RUNTIME_EVIDENCE.md` may record `BLOCKED_REQUIRED_EVIDENCE / EVIDENCE_SCOPE_EXPANSION_REQUIRED` if the exact Task stop rule is triggered; do not fabricate runtime execution.

Export every changed product/test file preserving repository-relative path.

Do not export unchanged backend P2-1A source merely for convenience.

`P2_1D_UI_CONTRACT_EVIDENCE.md` must record:

- exact current P2-1A evidence DTO fields actually consumed;
- exact current P2-1A human/judgment DTO fields actually consumed;
- evidence semantic separation mapping;
- Human Gate / Human Result / Judgment / Transition Effect mapping;
- confirmation that no fabricated `JudgmentStatus` was introduced;
- endpoint ETag/read-state mapping;
- summary-current-authority and endpoint-local stale/failure behavior;
- safe DOM construction;
- mutation controls absent;
- responsive integration;
- any deviation/blocker.

`EXPORT_MANIFEST.md` must bind every payload except itself with byte count and SHA-256.

## 20. Task lifecycle

After implementation/evidence/report/export is submit-ready:

```text
.aiassistant/tasks/active/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md
→
.aiassistant/tasks/done/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md
```

Move, not Copy.

`tasks/done` means submitted executor turn, not accepted.

Do not stage/commit.

## 21. success / result boundary

Successful executor result:

```text
P2_1D_IMPLEMENTATION_CANDIDATE
/ COMMAND_CENTER_REVIEW_REQUIRED
/ HUMAN_BROWSER_QA_PENDING
```

Do not declare:

```text
P2-1D ACCEPTED
P2-1D PERSISTED
P2-1E STARTED
P2-1 ACCEPTED
P2-2 STARTED
```

Command Center must substantively review the exported candidate first.

Only after source/runtime acceptance may a later Task open Human Browser/Visual QA.

## 22. report required fields

Executor Report must include:

- task/work type/task path;
- `SESSION_AUTHORITY`;
- exact canonical paths read;
- pre-transport and post-transport Git status inventory;
- exact identification of the two inherited P2-1B governance artifacts;
- exact Python cache residue classification/count before and after;
- product source changes;
- governance/provenance changes;
- repository configuration changes;
- protected P2-1A source byte-identical result;
- P2-1C accepted source identity precheck;
- exact Evidence DTO fields consumed;
- exact Human/Judgment DTO fields consumed;
- EvidenceCandidate / admission / AdmittedEvidence / satisfaction separation;
- HumanGate / HumanResult / Judgment / transition-effect separation;
- fabricated `JudgmentStatus`: absent/present;
- current/stale authority implementation;
- ETag/304 behavior;
- polling/hidden/terminal behavior;
- safe DOM result;
- responsive integration result;
- evidence contract classifications;
- Human Browser QA: `HUMAN_PENDING`;
- mandatory stop/scope expansion;
- forbidden-not-run;
- unverified items;
- rollback/revert guide;
- preserved exact paths;
- next-turn recommendation.

## 23. preserved artifacts

Preserve after this executor turn:

```text
.aiassistant/tasks/done/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md

.aiassistant/records/aiscc/cycles/20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle.md

.aiassistant/reports/aiscc/20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1.md
```

Also preserve the two inherited P2-1B governance artifacts exactly if they are confirmed by actual preflight status.

Do not silently stage any preserved governance artifact.

The target bundle is temporary review material until Browser Command Center judgment.

## 24. final response format

1. result: completed / blocked / rejected-candidate
2. target bundle path
3. changed files
4. removed files
5. Human verification: `HUMAN_PENDING`
6. unverified items
7. exact preserved paths
