# 작업지시서: P3-3 Public Live L4 Provider Authority + Profile Decision Preparation

## meta

- task_id: `20260916_0915_aiscc-p3-3-public-live-l4-provider-authority-and-profile-decision-preparation-1`
- created_at: `2026-09-16 KST`
- work_type: `DISCOVERY_AUDIT / DESIGN_AUDIT`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- expected_orchestrator_version_or_commit: `e287117ba021411b82560df0af61901f7a8212bb`
- primary_semantic_owner: `P3-3 Public Live frozen L4 provider stage`

## current state

- branch: `main`
- expected HEAD: `e287117ba021411b82560df0af61901f7a8212bb`
- L1/L2/L3: `ACCEPTED / CLOSED`
- limiter retention release blocker: `RESOLVED`
- L4: `SELECTED / ENTRY_AUTHORIZED / NOT_STARTED`
- L5: `ENTRY_ELIGIBLE / SEPARATE`
- Public admission: `DISABLED`
- Public Live: `NOT_RELEASED`

Use the current IDE Executor conversation. No fresh chat is required.

## goal

Resolve the exact frozen L4 contract and prepare the exact current provider profile/release prerequisite decision surface.

This Task does NOT authorize a real paid provider request.

If all exact L4 inputs are already frozen and implementation can proceed without paid/provider-account mutation, continue only within the exact non-paid scope proven by L4.

If Human-owned provider/profile values are required, stop with:

`HUMAN_PROVIDER_POLICY_DECISION_REQUIRED`

and provide one concrete proposal.

## frozen authority

Accepted/frozen design commit:

`209e7534f66e9b07ce9d33742e6993370a70f4fb`

Read historical objects directly:

- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_IMPLEMENTATION_SEQUENCE.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_HUMAN_DECISIONS.md`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_SECURITY_TEST_MATRIX.json`
- `.aiassistant/reports/aiscc/AISCC_PUBLIC_LIVE_FAILURE_STATE_MACHINE.md`
- any exact historical path referenced by the L4 object

Do not reconstruct L4 from Browser shorthand or memory.

## current canonical must-read

- `.aiassistant/rules/AISCC_AGENTS.md`
- `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
- `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
- `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- `.aiassistant/records/aiscc/cycles/20260916_0915_aiscc-p3-3-limiter-retention-terminal-closure-l4-entry-1.cycle.md`
- `.aiassistant/reports/aiscc/20260916_0915_aiscc-browser-command-center-limiter-retention-terminal-closure-l4-selection-1.md`
- `.aiassistant/reports/aiscc/20260916_0915_aiscc-browser-command-center-retention-closed-l4-entry-handoff-1.md`

Inspect accepted provider/runtime source only after exact L4 authority is resolved.

Likely current owners include P1-5 ProviderProfile/selector/runtime, but actual paths/symbols must be discovered narrowly.

## Phase A — exact L4 authority

Before any product/config mutation, emit:

`RESOLVED_L4_AUTHORITY.json`

Required:

- exact L4 stage object;
- exact title;
- dependencies;
- entry criteria;
- exit criteria;
- non-goals;
- exact historical refs/hashes;
- applicable security matrix case IDs;
- provider/account/release values frozen vs deferred;
- whether a real provider call is an L4 exit requirement;
- whether deployment/hosted evidence belongs to L5 and is excluded;
- ambiguity flag.

If L4 is missing or ambiguous:

`POLICY_CONFLICT_INVESTIGATION_REQUIRED` and STOP.

## Phase B — current provider official-fact verification

Current provider direction is OpenAI API, separate API Project, but current release facts must be reverified.

When authorized network access is available, use only official OpenAI sources.

Record:

`CURRENT_PROVIDER_FACTS.json`

At minimum, when relevant to exact L4:

- verification timestamp;
- source URLs/doc identities;
- current Responses API availability;
- exact candidate model IDs;
- current standard token pricing;
- relevant context/output limits;
- relevant tool/function-calling availability;
- current documented rate-limit/account-tier semantics when officially discoverable;
- current supported-country/region/data-residency constraints relevant to deployment;
- current provider spend/hard-limit capability documentation when officially discoverable.

Do not use community posts as authority.

Do not infer account-specific quotas from public docs.

If network access is unavailable, do not guess. Mark current external verification blocked and preserve Browser-provided seed as non-Executor evidence only.

## Browser-provided current public seed — NOT a Human decision

As of 2026-09-16, Browser Command Center observed official OpenAI documentation indicating:

```text
gpt-5.6-sol:
Responses API supported
standard public price observed:
$4 / 1M input
$20 / 1M output

gpt-5.6-terra:
Responses API supported
standard public price observed:
$2 / 1M input
$12 / 1M output

gpt-5.6-luna:
Responses API supported
standard public price observed:
$0.20 / 1M input
$1.20 / 1M output
```

Treat this as current external seed requiring Executor reverification where possible.

Do NOT convert it into provider-profile selection.

## Phase C — current repository/provider binding audit

Narrowly inspect the accepted current implementation for:

- ProviderProfile/registry owner;
- current OpenAI Responses adapter;
- server-fixed model/profile binding;
- budget/call/token/time limits;
- secret capability/credential resolution boundary;
- provider availability checks;
- unknown-outcome/retry semantics;
- usage/token accounting;
- fake/local provider evidence versus real provider evidence;
- Public Live integration point.

Emit:

`L4_CURRENT_BINDING_AUDIT.md`

Do not mutate source in this phase.

## Phase D — exact decision surface

Emit:

`L4_PROVIDER_DECISION_SURFACE.md`

Classify every relevant value as exactly one:

```text
FROZEN_HISTORICAL
CURRENT_OFFICIAL_FACT
CURRENT_REPOSITORY_FACT
HUMAN_DECISION_REQUIRED
ACCOUNT_EVIDENCE_REQUIRED
L5_OWNED
NOT_REQUIRED
```

Potential decision fields include, only when L4 requires them:

- provider;
- exact model/model ID;
- API endpoint/API family;
- reasoning effort;
- max input tokens;
- max output tokens;
- provider calls/run;
- retry count;
- timeout;
- max concurrent provider work;
- per-run USD cap;
- daily USD cap;
- global competition USD cap;
- provider hard-spend/project budget setting;
- API Project identity;
- credential reference/capability;
- rate-limit/account-tier evidence;
- region/data-residency choice.

Do not silently fill a HUMAN_DECISION_REQUIRED field.

## concrete proposal rule

If Human decisions are required, emit:

`L4_PROVIDER_PROFILE_PROPOSAL.md`

It must contain:

- one recommended bounded profile;
- rationale tied to competition demo quality, accepted product boundary and current official pricing;
- worst-case cost formula under proposed token/call/run caps;
- no secret values;
- exact fields Human must approve;
- alternatives only when materially different.

Status:

`PROPOSED / NOT_ACCEPTED`

Then STOP before product/provider-account mutation.

Final result:

`HUMAN_PROVIDER_POLICY_DECISION_REQUIRED`

## no-human-decision continuation

Only if the frozen L4 authority and current accepted decisions already fix every mutation-critical field may the Executor continue to a non-paid L4 implementation step.

Even then forbidden:

- real provider paid request;
- credential secret retrieval/export;
- billing/project-budget mutation;
- public admission enablement;
- L5 deployment;
- Git commit/push.

Any real-provider request requires a later explicitly authorized Task.

## secret/account boundary

Never print/store:

- API key/token;
- credential value;
- billing secret;
- private account identifiers beyond an opaque/non-secret reference needed for governance.

A missing provider credential/project/billing state is Human/account evidence, not permission to inspect arbitrary local files or environment.

Do not search broad home/config directories for secrets.

## evidence contract

### executor_required — `L4_AUTHORITY`

Exact frozen L4 object, refs, dependencies, exit/non-goals, ambiguity false.

### executor_required — `CURRENT_PROVIDER_FACTS`

Official current provider facts when network available; otherwise explicit blocked classification.

### executor_required — `STATIC_SOURCE`

Current accepted provider/profile/runtime binding audit; no mutation unless exact L4 + no-Human-decision path authorizes it.

### executor_required — `DECISION_SURFACE`

Every L4 field classified by owner/source.

### executor_required — `COST_BOUND`

If a profile proposal is required:
- exact token/call/run caps;
- current price source;
- worst-case per-run and bounded campaign cost calculations;
- no claim that provider-side hard cap is configured without account evidence.

### executor_required — `WORKSPACE_INTEGRITY`

HEAD/index/worktree before/after; no unrelated mutation; no commit/push/deploy.

## reuse_allowed

- accepted P1-5 provider/tool runtime for unchanged architecture;
- L1/L2/L3 and retention terminal acceptance;
- Browser current provider seed only as externally sourced seed, not accepted provider policy.

## human_owned

- provider/model/profile selection when not frozen;
- API Project/credential/account evidence;
- provider billing/spend/hard-limit configuration;
- authorization for any paid provider call;
- L4 terminal acceptance;
- Git persistence;
- Public Live release.

## L5-owned

Do not claim:

- Railway trusted proxy;
- hosted ingress IP derivation;
- deployed TLS;
- deployment/runtime URL;
- production environment secret injection;
- hosted network isolation.

## forbidden

- paid provider call;
- provider billing mutation;
- raw credential read/export;
- public enablement;
- L5 work;
- deployment;
- Git commit/push;
- model/provider auto-fallback;
- changing accepted L1/L2/L3 semantics.

## accept/stop outcomes

Allowed final outcomes:

1. `HUMAN_PROVIDER_POLICY_DECISION_REQUIRED`
   - exact L4 authority resolved;
   - current provider facts/binding audited;
   - concrete proposal emitted;
   - no provider/account mutation.

2. `BLOCKED_CURRENT_PROVIDER_VERIFICATION`
   - exact L4 requires current fact that cannot be verified;
   - no guessing.

3. `COMPLETED / ACCEPTED_CANDIDATE`
   - only if exact L4 can be completed without Human-unfixed values and without paid/account/deployment actions.

Executor must not claim terminal L4 acceptance.

## mandatory stop

- HEAD mismatch;
- L4 authority ambiguous;
- current official provider fact required but unavailable;
- Human-unfixed provider value needed;
- account evidence/credential needed;
- real paid call required;
- L5 hosted/deployment dependency required;
- unrelated dirty collision;
- source mutation outside exact non-paid L4 scope.

## export bundle

Target:

`.aiassistant/reports/target/20260916_0915_aiscc-p3-3-public-live-l4-provider-authority-and-profile-decision-preparation-1/`

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `RESOLVED_L4_AUTHORITY.json`
- `CURRENT_PROVIDER_FACTS.json`
- `L4_CURRENT_BINDING_AUDIT.md`
- `L4_PROVIDER_DECISION_SURFACE.md`
- `L4_PROVIDER_PROFILE_PROPOSAL.md` when Human decision required
- concise source/provider verification evidence
- `REMOVED_FILES.md` only if actual deletion exists

## Task lifecycle

active:

`.aiassistant/tasks/active/20260916_0915_aiscc-p3-3-public-live-l4-provider-authority-and-profile-decision-preparation-1.md`

done after executor-required audit/report/export:

`.aiassistant/tasks/done/20260916_0915_aiscc-p3-3-public-live-l4-provider-authority-and-profile-decision-preparation-1.md`

## final response

1. result
2. target bundle
3. exact L4 title/dependencies/exit
4. current official provider facts
5. current provider binding
6. field-by-field ownership classification
7. provider profile proposal if required
8. cost bound
9. account/Human evidence required
10. Public admission before/after
11. provider calls
12. workspace integrity
13. human verification
14. unverified
15. preserved paths
