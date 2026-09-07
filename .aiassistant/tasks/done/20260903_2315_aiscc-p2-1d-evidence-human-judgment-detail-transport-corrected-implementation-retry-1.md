# 작업지시서: P2-1D Evidence + Human/Judgment detail — transport-corrected implementation retry

## meta

- task_id: `20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1`
- created_at: `2026-09-03T23:15:00+09:00`
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
- blocked_predecessor_cycle: `.aiassistant/records/aiscc/cycles/20260903_2255_aiscc-p2-1d-predecessor-transport-blocked-missing-artifact-1.cycle.md`
- blocked_predecessor_handoff: `.aiassistant/reports/aiscc/20260903_2255_aiscc-browser-command-center-p2-1d-transport-blocked-rework-entry-handoff-1.md`
- blocked_task_done: `.aiassistant/tasks/done/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md`
- target_bundle: `.aiassistant/reports/target/20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1/`
- fresh_chat_policy: `NEW_IDE_CHAT_REQUIRED / NEW_P2_1D_RETRY_SLICE`
- implementation_commit_authority: `NONE`
- success_boundary: `P2_1D_IMPLEMENTATION_CANDIDATE / COMMAND_CENTER_REVIEW_REQUIRED`
- retry_reason: `previous 2226 turn stopped fail-closed because predecessor Browser artifacts were not locally transported; no product/test mutation occurred`
- transport_contract: `EXPLICIT_HUMAN_PLACEMENT / EXACT_DOWNLOADS_FILENAMES_CONFIRMED`

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
tree:
c7c601677eb2a4ca2fa7b594465ebd16ed8da9f4
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

latest P2-1D attempt:
BLOCKED_MISSING_ARTIFACT / NO_PRODUCT_MUTATION / NO_IMPLEMENTATION_CANDIDATE

P2-1E:
NOT_STARTED

P2-2:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

The prior `2226` Executor turn is durable blocked provenance only. It is not a P2-1D implementation candidate.

Do not move the old `2226` Task back to `tasks/active`.
Do not execute the old Task from Downloads.
This retry uses only the new `2315` Task as mutation authority.

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
AGENT_OUTPUT != SYSTEM_STATE
AGENT_CLAIM != ADMITTED_EVIDENCE
HUMAN_OWNED_EVIDENCE != EXECUTOR_COMPLETED

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

1. transport this new Task plus the exact `2218`, `2220`, and `2255` governance provenance into the repository using the corrected exact Downloads filenames in Section 4;
2. perform the transport as an all-or-nothing prechecked operation and verify every source/destination SHA-256 before product mutation;
3. verify exact `main` / accepted HEAD / empty index / inherited dirty-workspace provenance before and after governance transport;
4. preserve the old blocked `2226` Task only at its existing `tasks/done` canonical provenance path;
5. inspect the current accepted P2-1A evidence + human/judgment DTO/read-contract implementation and current accepted P2-1C WorkRun detail page/tests before changing source;
6. extend the existing canonical WorkRun detail page:
   - `GET /command-center/work-runs/{work_run_id}`
   - do not create a competing second WorkRun detail page;
7. consume only the already accepted P2-1A read endpoints:
   - `GET /v1/command-center/work-runs/{work_run_id}/evidence`
   - `GET /v1/command-center/work-runs/{work_run_id}/human-judgment`;
8. render Evidence semantics without collapsing requirement/candidate/admission/admitted/satisfaction distinctions;
9. render Human Gate / Human Result / Judgment / Transition Effect as separate authority dimensions;
10. preserve P2-1C summary-current-authority, stale/retained data, ETag/304, polling, hidden-tab, terminal-stop and recovery behavior;
11. preserve Korean-first visible copy, safe DOM construction and responsive layout;
12. add/update focused unit/source and affected integration tests;
13. execute required static and local runtime evidence without expanding environment scope;
14. export the exact candidate bundle;
15. move this new Task from `tasks/active` to matching `tasks/done`;
16. stop without Git staging/commit/push/deployment;
17. leave Human Browser/Visual/Usability QA as `HUMAN_PENDING` for a later Command Center gate.

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
prior 2226 turn is terminal blocked provenance
retry must not reuse old Task/chat as mutation authority
```

Before any product source mutation report:

```text
SESSION_AUTHORITY:
NEW_P2_1D_RETRY_IMPLEMENTATION_CHAT / PASS
```

Failure:

```text
BLOCKED_REQUIRED_EVIDENCE / NEW_IMPLEMENTATION_CHAT_REQUIRED
```

No product mutation after a failed session gate.

## 4. corrected Downloads transport — all-or-nothing

Human has explicitly placed the governance predecessors in Windows Downloads with the exact filenames below.

DO NOT append or guess `(1)`.
DO NOT search alternate filenames.
DO NOT use the old `2226` Task as the current Task.

Before copying/moving anything, precheck **all five current transport items** and the existing blocked Task provenance.

For each governance artifact:
- if exact canonical destination exists, verify destination SHA-256 and mark `DESTINATION_VALID`;
- if exact canonical destination is absent, exact Downloads source must exist and match SHA-256, then mark `SOURCE_VALID_DESTINATION_ABSENT`;
- if any item is neither valid state, stop before copying any governance artifact.

Only after every item passes the precheck may absent governance destinations be populated.

### 4.1 current retry Task

```text
source:
C:\Users\oracl\Downloads\20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1.md

destination:
.aiassistant/tasks/active/20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1.md
```

The active destination MUST be absent before transport.

Transport this Task only after governance source precheck passes.

### 4.2 P2-1C terminal Cycle

```text
source:
C:\Users\oracl\Downloads\20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle.md

destination:
.aiassistant/records/aiscc/cycles/20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle.md

expected SHA-256:
9af3a5fbedef5478e58c06cb114997aee15558d56c8aede55a5bb9e9b670ee4c
```

### 4.3 P2-1C completion → P2-1D entry Handoff

```text
source:
C:\Users\oracl\Downloads\20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1.md

destination:
.aiassistant/reports/aiscc/20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1.md

expected SHA-256:
e88df2b56ad301175619baee4d4dcc0ccc8267229ebd47a6a619b76482758a9c
```

### 4.4 blocked P2-1D Cycle

```text
source:
C:\Users\oracl\Downloads\20260903_2255_aiscc-p2-1d-predecessor-transport-blocked-missing-artifact-1.cycle.md

destination:
.aiassistant/records/aiscc/cycles/20260903_2255_aiscc-p2-1d-predecessor-transport-blocked-missing-artifact-1.cycle.md

expected SHA-256:
b31b9c9a66ef8c58e7709f4e7276ae75dc8f98cce6e1833092c0711d03db3dd8
```

### 4.5 blocked P2-1D Handoff

```text
source:
C:\Users\oracl\Downloads\20260903_2255_aiscc-browser-command-center-p2-1d-transport-blocked-rework-entry-handoff-1.md

destination:
.aiassistant/reports/aiscc/20260903_2255_aiscc-browser-command-center-p2-1d-transport-blocked-rework-entry-handoff-1.md

expected SHA-256:
afd0bb1fb5a6a52d478fadb3b6466bc453549409793b8e8cb17c9d13d4639eb5
```

### 4.6 existing old blocked Task provenance — verify only, do not re-transport

```text
canonical:
.aiassistant/tasks/done/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md

expected SHA-256:
6fba619f59b8a2a77ae0e0b684411b437525650ee431c0c014bb2094f449a881
```

This canonical path was created by the prior blocked turn and must remain in `tasks/done`.

If absent or SHA-mismatched:

```text
BLOCKED_MISSING_ARTIFACT / BLOCKED_PREDECESSOR_PROVENANCE_MISMATCH
```

STOP before product mutation.

The Downloads copy of the old `2226` Task is irrelevant to this retry and MUST NOT be executed or copied back to `tasks/active`.

### 4.7 transport failure semantics

Any mismatch, missing exact source needed for an absent destination, wrong destination identity, or inability to establish the all-or-nothing precheck:

```text
TRANSPORT_PRECONDITION_FAILED
BLOCKED_MISSING_ARTIFACT
```

Then:

- do not partially transport remaining governance artifacts;
- do not inspect/mutate product source beyond minimum blocker evidence;
- do not guess filenames;
- do not broad-search Downloads;
- complete minimal report/export;
- leave repository product/test source unchanged.

## 5. dirty-workspace preflight — MUST run before product mutation

Run before transport and again after transport:

```text
git status --short --untracked-files=all
git branch --show-current
git rev-parse HEAD
git rev-parse HEAD^{tree}
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

tree:
c7c601677eb2a4ca2fa7b594465ebd16ed8da9f4

index:
empty
```

Inherited final state from the blocked `2226` turn is provenance, not a blindly trusted current count:

```text
reported untracked:
136

classification:
133 known __pycache__ / .pyc paths
+
2 inherited P2-1B governance paths
+
1 blocked P2-1D tasks/done path
```

Exact inherited P2-1B paths:

```text
.aiassistant/records/aiscc/cycles/20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md
SHA-256:
f479952b982af8d7444494d4021db443b84135324a4e4a68f09f0b30355f2488

.aiassistant/reports/aiscc/20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md
SHA-256:
ca813f7cd5775d0a2d649bddae6800b4cc8ad114b7ac7110aed4e1d52f7c276d
```

After successful transport, expected additional Git-visible governance paths are the exact four canonical `2218`, `2220`, `2255 Cycle`, `2255 Handoff` paths if they were all absent before transport.

Do not fail merely because the numeric count differs when one or more canonical governance destinations were already valid. Classify exact paths and hashes.

No unrelated product/source/test/config/migration/governance dirt is allowed.

If any unrelated path exists:

```text
DIRTY_WORKSPACE_MIXED / COMMAND_CENTER_REVIEW_REQUIRED
```

STOP before product mutation.

Do not normalize with:

```text
git clean
git restore
git checkout
git reset
git stash
```

Do not delete known Python cache residue merely to make status look clean.
Do not stage inherited or transported governance.

For Python execution prefer per-command:

```text
PYTHONDONTWRITEBYTECODE=1
```

or platform-equivalent process environment.

Do not convert this retry into a workspace-cleanup task.

## 6. minimum authoritative context

Read exact canonical documents after transport:

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

.aiassistant/records/aiscc/cycles/20260903_2255_aiscc-p2-1d-predecessor-transport-blocked-missing-artifact-1.cycle.md
.aiassistant/reports/aiscc/20260903_2255_aiscc-browser-command-center-p2-1d-transport-blocked-rework-entry-handoff-1.md

.aiassistant/tasks/done/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md
.aiassistant/tasks/done/20260903_0910_aiscc-p2-1a-command-center-read-model-api-projection-foundation-implementation-1.md
.aiassistant/tasks/done/20260903_1759_aiscc-p2-1c-workrun-transition-execution-detail-implementation-1.md
.aiassistant/tasks/done/20260903_1949_aiscc-p2-1c-retained-detail-stale-current-authority-labeling-rework-1.md

.aiassistant/tasks/active/20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1.md
```

If the exact historical P2-1A implementation Task is unavailable, use current accepted source as authoritative runtime evidence and record the missing historical Task as a provenance limitation.

Do not bulk-read unrelated tasks/cycles/logs.

Authority precedence:

```text
local canonical repository
>
terminal-persisted accepted Cycle/rule/commit
>
latest terminal Browser judgment Cycle
>
current Handoff
>
Browser Project Source mirror
>
chat memory
```

If current accepted source conflicts with canonical rule/Cycle/Handoff, stop:

```text
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

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

Confirm actual DTO/JSON field shapes for:

```text
GET /v1/command-center/work-runs/{work_run_id}/evidence

GET /v1/command-center/work-runs/{work_run_id}/human-judgment
```

Do not infer field names from this Task when current accepted source defines them.

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

If clean-HEAD bytes do not match:

```text
ACCEPTED_BASELINE_IDENTITY_MISMATCH
```

STOP before product mutation.

### 7.3 protected app composition

Read only if needed:

```text
src/aiscc/api/app.py
```

Expected accepted identity:

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

Existing P2-1C page already owns:

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

Use exact accepted P2-1A DTO field names discovered from current source.

Visible model MUST preserve:

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
type / channel where DTO exposes it
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

If accepted endpoint returns no checkpoint / requirement / candidate / admitted evidence, render explicit truthful empty/absence state.

Do not fabricate authority fields.

## 11. Human/Judgment rendering contract

Accepted P2-1A read contract exposes four independent presentation dimensions:

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

Do not display/reconstruct forbidden Human identity/auth authority.

### 11.2 Human Result

Preserve exact source presence and exact result kind/outcome.

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

Do not create a generic synthetic `status` that collapses the model.

```text
Judgment != TransitionDecision
Judgment != WorkflowState
```

### 11.4 Transition Effect

Render accepted read DTO transition-effect/current effect information separately.

Do not reinterpret a Judgment as an already-admitted state transition.

## 12. P2-1C current/stale/refresh contract — MUST preserve

Existing accepted behavior remains:

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
preserve last successful data
```

New evidence and human-judgment reads join the same refresh coordinator without changing the semantic authority rule.

### 12.1 summary current authority

If the summary/current WorkRun request cannot establish current authority:

```text
do not apply concurrently fetched dependent payloads as newly current
```

This includes:

```text
transitions
execution
evidence
human-judgment
```

When a previously successful dependent section exists:
- retain its last successful DOM;
- mark it truthfully as retained/stale/refresh-failed;
- do not label it `최신` or equivalent current-authority language.

When no previous successful dependent section exists:
- render truthful unavailable/error state;
- do not invent empty-as-current authority.

### 12.2 endpoint-local failure

If summary remains current but only one dependent endpoint fails:
- retain that endpoint's last successful DOM when available;
- mark only that section stale/refresh-failed;
- do not invalidate successful sibling sections solely because one endpoint failed.

### 12.3 recovery

After later successful summary + endpoint refresh:
- current labels may be restored;
- unchanged successful section content may remain;
- stale markers must clear truthfully.

### 12.4 304

Endpoint-local `304`:
- preserves previous successful payload/DOM;
- does not convert another endpoint's stale data into current;
- does not collapse ETag authority across endpoints.

## 13. visible UI / Korean-first / responsive integration

User-visible copy is Korean-first.

Keep exact code/domain identifiers when useful:

```text
EvidenceRequirement
EvidenceCandidate
AdmittedEvidence
HumanGate
HumanResult
Judgment
TransitionDecision
WorkflowState
```

Integrate into the existing WorkRun detail hierarchy rather than creating a visually separate competing application.

Must remain usable at the existing accepted responsive widths.

Do not introduce horizontal page overflow as the normal layout.
Long IDs/refs/reasons must wrap or use the existing safe overflow treatment.

Do not add mutation buttons or affordances that look actionable.

## 14. safe DOM / content handling

API-derived evidence/Human/Judgment values are untrusted display data.

Preferred:

```text
createElement
textContent
setAttribute with fixed attribute names and validated/safe values
replaceChildren
```

Do not build executable HTML from API-derived fields.

Do not use:

```text
eval
new Function
unsafe innerHTML interpolation of API values
```

No private evidence body, Human principal detail, credential/secret, or raw producer payload may be exposed merely because a DTO contains a reference.

## 15. validation and evidence

Use repository-local environment only.

Do not install packages or use external network.

### 15.1 STATIC_SOURCE

Required:
- inspect exact P2-1A DTO/read source;
- inspect exact current P2-1C page/test source;
- verify protected backend read-authority paths remain byte-identical;
- verify no mutation control/new backend authority introduced;
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
15. existing visible/nonterminal polling remains 10 seconds.
16. hidden-tab polling stop remains.
17. terminal WorkRun polling stop remains.
18. no mutation control is present.
19. API-derived content is not inserted through unsafe HTML/eval paths.
20. P2-1C transition/execution semantics remain covered.

### 15.3 affected integration tests

Run existing affected Command Center integration tests.

Required coverage:
- canonical WorkRun detail route still serves;
- browser code references only accepted read endpoints;
- Evidence endpoint integration path represented correctly;
- Human/Judgment endpoint integration path represented correctly;
- unsupported/missing read states produce truthful safe UI behavior;
- P2-1C existing routes/assets remain available;
- no mutation route added.

Use only existing repository-local test harness.

If integration proof requires a new DB/container/image/package/network environment:

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

Prove no authoritative DB/event mutation from page GET/read polling only if the existing harness already supports this observation.

If local HTTP runtime requires a newly created Docker DB/server environment beyond the current harness:

```text
EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

STOP. Do not manufacture substitute proof.

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

After targeted checks pass, run repository's existing unit + integration regression suite only if it requires no new package/network/environment expansion.

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
TRANSPORT_IDENTITY
DIRTY_WORKSPACE_PROVENANCE
STATIC_SOURCE
FRONTEND_SOURCE_TEST / UNIT_TEST
affected INTEGRATION_TEST
LOCAL_HTTP_RUNTIME when available in existing accepted harness
STATIC_CHECK
PUBLIC_PROVENANCE
```

### reuse_allowed

P2-1A and P2-1C accepted evidence may be reused only for unchanged owner semantics and unchanged source identities.

The blocked `2226` result may be reused only as proof of:
- prior transport failure;
- fail-closed Executor conduct;
- no product/test mutation;
- old blocked Task provenance.

It does not prove any P2-1D rendering behavior.

### human_owned

```text
BROWSER_RUNTIME / VISUAL / USABILITY QA
```

Status:

```text
HUMAN_PENDING
```

Do not execute or claim Human Browser QA.

Human QA may open only after Browser Command Center substantive source/runtime acceptance.

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
old 2226 Task reactivation
alternate Downloads filename search
```

### proof non-substitution

```text
Browser screenshot of Downloads != SHA-256 transport proof
P2-1A endpoint exists != P2-1D UI tested
unit/source test != local HTTP runtime
local HTTP runtime != Human Browser/Visual QA
executor report != Human acceptance
EvidenceCandidate != AdmittedEvidence
HumanResult != Judgment
Judgment != TransitionDecision
Judgment != WorkflowState
blocked 2226 provenance != current implementation evidence
```

## 17. mandatory stop conditions

STOP before additional mutation when any occurs:

```text
HEAD != 08368eceac625c9a74b4347021ed65540cb08b3c
tree != c7c601677eb2a4ca2fa7b594465ebd16ed8da9f4
branch != main
index not empty at preflight

current retry Task source missing
active Task destination already exists unexpectedly

2218/2220/2255 exact source/destination identity cannot be established
old 2226 tasks/done provenance missing or SHA mismatched
partial governance transport would be required after failed all-or-nothing precheck

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
BLOCKED_MISSING_ARTIFACT
BLOCKED_PREDECESSOR_PROVENANCE_MISMATCH
DIRTY_WORKSPACE_MIXED
ACCEPTED_BASELINE_IDENTITY_MISMATCH
P2_1A_API_CONTRACT_CHANGE_REQUIRED
IMPLEMENTATION_PATH_EXPANSION_REQUIRED
P2_1D_CURRENT_AUTHORITY_CONTRACT_GAP
EVIDENCE_SCOPE_EXPANSION_REQUIRED
POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

After a named blocker:
- collect only minimum source/workspace evidence;
- complete report/export;
- move current Task to done if executor turn is submit-ready;
- do not continue unrelated tests/runtime/environment work;
- do not clean/reset/stash.

## 18. repository / Git restrictions

Forbidden:

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
.aiassistant/reports/target/20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
P2_1D_UI_CONTRACT_EVIDENCE.md
HTTP_RUNTIME_EVIDENCE.md
TRANSPORT_EVIDENCE.md
```

`TRANSPORT_EVIDENCE.md` must record:
- exact source path, destination path, expected SHA-256, actual SHA-256, and result for `2218`, `2220`, both `2255` artifacts;
- old blocked `2226` canonical done-path hash verification;
- all-or-nothing precheck result before any copy;
- which canonical destinations already existed vs were transported;
- pre/post exact Git-visible governance path inventory;
- explicit confirmation that no alternate filename search occurred.

`HTTP_RUNTIME_EVIDENCE.md` may record:

```text
BLOCKED_REQUIRED_EVIDENCE / EVIDENCE_SCOPE_EXPANSION_REQUIRED
```

if the exact stop rule is triggered. Do not fabricate runtime execution.

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
.aiassistant/tasks/active/20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1.md
→
.aiassistant/tasks/done/20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1.md
```

Move, not Copy.

`tasks/done` means submitted Executor turn, not accepted.

Do not stage/commit.

Do not alter:

```text
.aiassistant/tasks/done/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md
```

except read-only identity verification.

## 21. success / result boundary

Successful Executor result:

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
- transport contract and exact all-or-nothing precheck;
- exact canonical paths read;
- pre-transport and post-transport Git status inventory;
- exact identities of inherited P2-1B governance artifacts;
- exact old blocked `2226` tasks/done identity result;
- exact `2218` / `2220` / `2255` source/destination SHA results;
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

Preserve after this Executor turn:

```text
.aiassistant/tasks/done/20260903_2226_aiscc-p2-1d-evidence-human-judgment-detail-implementation-1.md

.aiassistant/tasks/done/20260903_2315_aiscc-p2-1d-evidence-human-judgment-detail-transport-corrected-implementation-retry-1.md

.aiassistant/records/aiscc/cycles/20260903_2218_aiscc-p2-1c-persistence-final-acceptance-p2-1d-entry-authorization-1.cycle.md

.aiassistant/reports/aiscc/20260903_2220_aiscc-browser-command-center-p2-1c-completion-p2-1d-entry-handoff-1.md

.aiassistant/records/aiscc/cycles/20260903_2255_aiscc-p2-1d-predecessor-transport-blocked-missing-artifact-1.cycle.md

.aiassistant/reports/aiscc/20260903_2255_aiscc-browser-command-center-p2-1d-transport-blocked-rework-entry-handoff-1.md
```

Also preserve the two inherited P2-1B governance artifacts exactly if confirmed by preflight:

```text
.aiassistant/records/aiscc/cycles/20260903_1718_aiscc-p2-1b-shell-queue-persistence-final-acceptance-1.cycle.md

.aiassistant/reports/aiscc/20260903_1720_aiscc-browser-command-center-p2-1b-completion-p2-1c-entry-handoff-1.md
```

Do not silently stage any preserved governance artifact.

The target bundle remains temporary review material until Browser Command Center judgment.

## 24. final response format

1. result: completed / blocked / rejected-candidate
2. target bundle path
3. changed files
4. removed files
5. transport evidence summary
6. Human verification: `HUMAN_PENDING`
7. unverified items
8. exact preserved paths
