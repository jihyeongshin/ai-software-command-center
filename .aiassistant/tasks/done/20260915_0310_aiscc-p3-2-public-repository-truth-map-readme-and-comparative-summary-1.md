# 작업지시서: P3-2 Public Repository Truth Map, README, and Comparative Summary

## meta

- task_id: `20260915_0310_aiscc-p3-2-public-repository-truth-map-readme-and-comparative-summary-1`
- created_at: `2026-09-15T03:10:50+09:00`
- work_type: `DOC_BASELINE_UPDATE`
- evidence_profile: `STANDARD`
- execution_mode: `MANUAL_COMMAND_CENTER`
- fresh_ide_chat_required: `No`
- primary_semantic_owner: `P3-2 Public Repository Documentation / Browser Command Center`

## current authority

```text
P2:
ACCEPTED / CLOSED

P3-1 Comparative Evaluation:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P3-2:
ENTRY_AUTHORIZED

P3-3:
NOT_STARTED
```

P3-1 terminal authority:

- `.aiassistant/records/aiscc/cycles/20260915_0310_aiscc-p3-1-comparative-evaluation-final-acceptance-p3-2-entry-authorization-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_0310_aiscc-p3-1-comparative-evaluation-final-human-acceptance-browser-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_0310_aiscc-browser-command-center-p3-1-closed-p3-2-public-documentation-entry-handoff-1.md`

Accepted comparative protocol SHA-256:

`a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6`

Corrected comparative-result submission ZIP SHA-256:

`2827c3b0a302caff4971090347134d3f9e37ab0e8d6cf5be4eae0fe706d42e48`

Repository HEAD most recently observed before terminal documentation entry:

`82bc047b79cf496280d1b3df6a113f652629a6f5`

Do not treat that HEAD as proof of a clean workspace. Perform the normal bounded workspace inventory required by project rules.

## goal

Create the first truthful public repository documentation baseline for P3-2.

The result must let a technically competent reviewer answer, from the public repository:

1. What is AISCC?
2. What governance problem does it target?
3. What is actually implemented/evidenced now?
4. What is Agent-owned, System-owned, and Human-owned?
5. What does the Task → Evidence → Judgment → Cycle → Next Action chain look like?
6. What does the accepted Self-Dogfooding run prove and not prove?
7. What did P3-1 comparative evaluation observe and what could it not establish?
8. What is Recorded Replay versus bounded Live?
9. What public runtime is actually released now?
10. Where can a reviewer inspect durable repository provenance?
11. What claims are intentionally not made?

## required outputs

### 1. canonical public documentation truth map

Create:

`.aiassistant/reports/aiscc/AISCC_PUBLIC_DOCUMENTATION_TRUTH_MAP.md`

This is the claim-control source for P3-2.

For every public-facing load-bearing claim used in README/comparative summary, record:

```text
claim_id
topic
public_wording
classification
current_status
evidence_owner
canonical_source_paths
exact supporting artifact/hash/commit when applicable
allowed_extension
forbidden_extension
freshness_or_release_note
target_surface
```

At minimum cover:

- product thesis/category
- authority drift/problem statement
- task-scoped evidence ownership
- proof non-substitution
- Agent claim vs admitted evidence
- System-owned transition
- Human gate
- curated Cycle/NextAction
- P2 recorded Replay status
- public Replay deployment status
- public bounded Live status
- Self-Dogfooding golden run
- P3-1 comparator definition
- M01-M04 exclusions
- M05 result
- P3-1 publication-condition limitation
- prior-art overlap / novelty ceiling
- public security/input boundary
- competition submission status

### 2. root public landing page

Update/create:

`README.md`

README must be written for an external technical reviewer, not for the internal Command Center operator.

Required sections:

1. `AI Software Command Center`
2. one-paragraph product thesis
3. `Why this exists`
4. `Governance chain`
5. `Authority model`
6. `What is implemented and evidenced`
7. `Self-Dogfooding`
8. `Comparative evaluation`
9. `Recorded Replay vs Bounded Live`
10. `Repository evidence / provenance map`
11. `Current limitations`
12. `Claim boundary`
13. `Project / competition status`

Optional:
- verified local quick-start or architecture links, but only if exact current repository commands/files are verified in this Task.

README must not include internal Browser/Downloads workflow instructions.

### 3. public comparative evaluation summary

Create:

`docs/AISCC_COMPARATIVE_EVALUATION.md`

This document is a public-safe summary of P3-1.

Required contents:

- question
- frozen comparator definitions
- explicit `SYNTHETIC_ABLATION_ONLY`
- matched-condition concept
- five-row planned matrix
- M01-M04 exclusions
- M05 source identity at a safe public level
- M05 comparator decisions
- all primary metric results
- relevant secondary results
- trace-derived artifact-count correction
- deterministic reproducibility statement
- limitation/confidence boundary
- exact reason `materially_better_condition_possible = No`
- admitted public conclusion
- prohibited inference section
- exact canonical protocol/result provenance links that actually exist in repository

Do not call the baseline a competitor product.

## minimum authoritative context

Read these current repository canonical files:

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
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
- `.aiassistant/records/aiscc/cycles/20260915_0310_aiscc-p3-1-comparative-evaluation-final-acceptance-p3-2-entry-authorization-1.cycle.md`
- `.aiassistant/reports/aiscc/20260915_0310_aiscc-p3-1-comparative-evaluation-final-human-acceptance-browser-judgment-1.md`
- `.aiassistant/reports/aiscc/20260915_0310_aiscc-browser-command-center-p3-1-closed-p3-2-public-documentation-entry-handoff-1.md`
- `.aiassistant/tasks/done/20260914_2317_aiscc-p2-4-golden-agent-single-file-proof-change-4.md`
- `docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md` if it exists at current HEAD

Also inspect:

- current `README.md` if present;
- `docs/` filename inventory;
- only exact documentation files linked from current README or required above.

Do not bulk-read unrelated history.

## source authority rules

- repository-local canonical beats stale Browser Project Source mirror;
- later terminal Cycle/Judgment beats embedded historical phase text in older baseline docs;
- a path mentioned in an old document does not prove the path exists now;
- public wording must be supported by current source plus applicable accepted evidence;
- no current public deployment capability may be inferred from planned P3-3 ownership.

## exact P3-1 public facts

These may be used as accepted facts:

```text
protocol:
HUMAN_PROVIDED / ACCEPTED
SHA-256:
a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6

planned rows:
5

M01-M04:
EX_SOURCE_MISSING / NOT_COMPARABLE

M05:
ELIGIBLE / EVALUATED / HUMAN_ACCEPTED

AISCC_GOVERNED:
ACCEPTED

EXECUTOR_REPORT_BASELINE:
UNRESOLVED

primary:
TRUTHFUL_TERMINAL_OUTCOME       PASS / PASS
EVIDENCE_INTEGRITY              PASS / PASS
AUTHORITY_SEPARATION            PASS / PASS
FAIL_CLOSED_BEHAVIOR            N/A  / N/A
AUDIT_RECONSTRUCTABILITY        10/10 / 5/10

secondary:
RESTART_RECOVERABILITY          PASS / FAIL
HISTORICAL_TRUTH_PRESERVATION   PASS / PASS
DETERMINISTIC_PROJECTION        PASS / PASS
GOVERNANCE_OVERHEAD             descriptive only
runtime latency                 NOT_COMPARABLE
cost                            NOT_COMPARABLE
operator burden                 NOT_COMPARABLE

trace-derived artifact counts:
AISCC_GOVERNED                  14 total / 11 decision / 3 reference-only
EXECUTOR_REPORT_BASELINE        14 total / 4 decision / 10 reference-only

materially_better_condition_possible:
No
```

Admitted conclusion:

> One eligible bounded artifact-interpretation comparison was completed. Four planned rows were source-excluded. The eligible corpus is insufficient for the frozen protocol's stronger directional claim.

## exact self-dogfooding facts

These may be stated only within their accepted scope:

```text
golden result commit:
ea34a0e08912d6259c74d0cb50ade9c9b9dba77e

golden provenance root:
b0be0299344375a74d9b9bdc7e7149aa949d98098e0a76bf9f81b13e86834e50

accepted chain:
SELF_DOGFOOD_GENESIS
→ TaskContract
→ SelfDogfoodTaskSpec
→ READY
→ RUNNING
→ exact governed source edit
→ authenticated external submission
→ admitted evidence
→ SATISFIED
→ deterministic Judgment ACCEPTED
→ WorkRun ACCEPTED
→ first real Cycle
→ result Git commit
→ CYCLE_DERIVED NextAction
```

This proves bounded actual use/provenance, not uniqueness, superiority, independent validation, general reliability, or security completeness.

## public runtime facts

Use:

```text
Recorded Replay corpus:
CANONICAL / PERSISTED

Public Replay deployment:
NOT_COMPLETED

Public Bounded Live:
NOT_RELEASED
```

Public architecture policy remains:

```text
default intended public mode:
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

Do not write as if the optional public Live service is currently launched.

## prior-art / claim ceiling

Public docs MUST acknowledge overlap with existing specification/orchestration/evidence gate/permission/memory/reviewer/provenance work.

Forbidden language includes:

- first / only / unique / nobody else
- invented evidence-gated lifecycle
- proven safer
- proven more accurate
- proven more productive
- proven cheaper
- superior to competing products
- self-dogfooding proves novelty
- recorded replay described as current Live execution

Permitted high-level positioning:

> AISCC does not claim invention of the underlying primitives. Its product hypothesis is to combine task-scoped evidence ownership, proof non-substitution, system-owned transition admission, Human-owned gates, and curated Cycle memory into one inspectable governance chain and use that chain on its own development.

Use this as a ceiling, not mandatory verbatim copy.

## public-safety rules

Do not expose in README/public docs:

- `C:\Users\...` host paths
- Downloads transport
- secrets/tokens/credentials
- private/company/customer data
- internal stack traces
- local-only credentials/config values
- Browser Project implementation mechanics that are irrelevant to the public product thesis

A Windows repository root path may remain in internal truth-map provenance only if project policy explicitly permits it; prefer repository-relative paths everywhere.

## local quick-start rule

Do not invent installation/run commands.

A README quick-start is allowed only when all used commands are verified against current repository files in this Task.

If exact public-ready startup instructions cannot be verified without expanding scope:

- omit the quick-start;
- state `public/local quick-start documentation pending P3-2 follow-up`;
- do not guess.

## link integrity rule

Every public repository link added by this Task must target an exact file that exists in the current working tree after the Task.

No dead placeholder links.

If a desired evidence artifact exists only inside ignored `.aiassistant/reports/target/**`:

- do not link to the ignored target path from public README;
- summarize accepted facts in `docs/AISCC_COMPARATIVE_EVALUATION.md`;
- link to tracked canonical Cycle/protocol artifacts only if they actually exist.

## scope

Allowed substantive edits:

- `README.md`
- `docs/AISCC_COMPARATIVE_EVALUATION.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_DOCUMENTATION_TRUTH_MAP.md`

Allowed task/report/export paths according to project rules.

Forbidden substantive edits:

- application/runtime/test source
- DB/schema/migration
- deployment/config
- provider/budget config
- Replay runtime/corpus mutation
- security policy semantics
- orchestration/state-machine semantics
- P3-1 protocol/result semantics
- competition submission form
- Git ignore policy

No Git add/commit/push in this Task.

## evidence contract

executor_required:

1. `STATIC_SOURCE / PUBLIC_PROVENANCE`
   - verify all load-bearing README/public-summary claims against exact current canonical sources;
   - every truth-map claim has source path/evidence;
   - P3-1 facts match terminal acceptance.

2. `DOC_CONFORMANCE`
   - README required sections present;
   - public comparative summary required sections present;
   - no forbidden claim language;
   - no Replay/Live mislabel;
   - no public deployment overstatement;
   - no ignored-target link;
   - every relative Markdown link resolves.

3. `PUBLIC_SAFETY`
   - scan changed public docs for host paths, secrets, token-like values, private/company/customer identifiers, internal stack traces;
   - UTF-8/control-character validation;
   - `git diff --check`.

4. `CURRENT_IMPLEMENTATION_TRUTH`
   - any `implemented`, `runtime-proven`, `released`, `available`, `live`, `deployed` wording must map to exact current evidence/status;
   - planned/deferred items remain explicitly planned/deferred.

reuse_allowed:

- accepted Product Thesis / Prior-Art / Runtime Boundary;
- accepted P2-4 self-dogfooding provenance;
- accepted P3-1 protocol/result;
- existing current public documentation when its claims verify.

human_owned:

- final public positioning/readability;
- whether the README tells the product story clearly enough for competition review;
- acceptance of public wording for P3-2.

not_required:

- unit/integration test suite
- DB/runtime/HTTP/browser
- provider/LLM/network
- deployment
- public availability test

forbidden:

- web/source freshness research in this Executor Task;
- product/runtime code changes;
- public service launch;
- competition submission;
- comparative re-analysis;
- stronger claim generation.

proof_non_substitution:

- documentation != implementation;
- current source existence != runtime proof;
- P3-1 one-row result != general superiority;
- Self-Dogfooding != independent validation;
- Replay persisted != public deployment;
- public runtime policy != released Live service;
- Executor-written public copy != Human public-positioning acceptance.

## deterministic checks

At minimum produce evidence for:

- all three substantive output files exist;
- every root README relative link resolves;
- every `docs/AISCC_COMPARATIVE_EVALUATION.md` relative link resolves;
- banned claim phrase scan;
- `Recorded Run Replay` / `Live` terminology scan;
- host-path/private-token pattern scan;
- protocol SHA literal matches terminal accepted value;
- M01-M04 exclusion text appears and is not scored;
- `materially_better_condition_possible = No` or equivalent explicit limitation appears;
- `Public Replay deployment: NOT_COMPLETED` and `Public Bounded Live: NOT_RELEASED` are not contradicted;
- `git diff --check` PASS.

## Human review focus

After Executor submission Browser/Human should review:

1. Is AISCC understandable within the first README screen/section?
2. Does the README explain the governance chain without internal workflow noise?
3. Are implemented/evidenced/planned/released states clearly distinguishable?
4. Is the self-dogfooding story strong but bounded?
5. Is the comparative result legible without implying superiority?
6. Are Replay and Live truthful?
7. Are prior-art overlap and limitations candid without burying the product thesis?
8. Are all links useful and valid?
9. Is any competition/public status overstated?

## mandatory stop

Stop without substantive mutation if:

- accepted P3-1 protocol/result identity conflicts;
- required terminal P3-1 artifacts are missing;
- current repository canonical contradicts a load-bearing claim and cannot be resolved within the stated authority chain;
- public docs would require unreleased/deployment facts not supported by evidence;
- secret/private material is encountered;
- scope expansion into runtime/deployment/research is required.

After named blocker, only minimal blocker evidence, report/export, and safe exit.

## export bundle

Target:

`.aiassistant/reports/target/20260915_0310_aiscc-p3-2-public-repository-truth-map-readme-and-comparative-summary-1/`

Required root:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- changed `README.md`
- changed `docs/AISCC_COMPARATIVE_EVALUATION.md`
- changed `.aiassistant/reports/aiscc/AISCC_PUBLIC_DOCUMENTATION_TRUTH_MAP.md`
- deterministic documentation validation evidence
- `REMOVED_FILES.md` only if actual project deletion exists

Terminal ZIP:

`.aiassistant/reports/target/20260915_0310_aiscc-p3-2-public-repository-truth-map-readme-and-comparative-summary-1.zip`

## expected terminal candidate

```text
DOCUMENTATION_CANDIDATE / HUMAN_PENDING
```

Executor must not mark P3-2 accepted/closed.

## final response format

1. result
2. protocol/result identity check
3. changed public docs
4. truth-map claim count
5. link validation
6. forbidden-claim/public-safety scan
7. runtime/released-state wording check
8. target bundle + ZIP
9. human verification
10. limitations/unverified
