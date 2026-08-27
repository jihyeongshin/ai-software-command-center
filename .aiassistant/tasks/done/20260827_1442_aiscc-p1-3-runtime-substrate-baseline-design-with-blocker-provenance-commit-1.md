# 작업지시서: P1-3 Runtime Substrate Baseline Design with Blocker Provenance Commit

## meta

- task_id: `20260827_1442_aiscc-p1-3-runtime-substrate-baseline-design-with-blocker-provenance-commit-1`
- created_at: `2026-08-27 14:42 KST`
- phase: `P1-3 precondition — Runtime Substrate Baseline`
- work_type: `DESIGN_DECISION`
- evidence_profile: `HIGH_RISK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- primary_semantic_owner: `AISCC executable application runtime / build / source-test layout / sandbox-evidence substrate`
- predecessor_p1_3_task: `20260827_1421_aiscc-p1-3-security-runtime-safeguard-implementation-with-closure-repair-commit-1`
- predecessor_result: `BLOCKED_RUNTIME_SUBSTRATE_DECISION_REQUIRED`
- predecessor_base_commit: `4ec8bf49330128f5fccb70d94a863dc57f9984d2`
- predecessor_blocker_cycle: `.aiassistant/records/aiscc/cycles/20260827_1442_aiscc-p1-3-runtime-substrate-decision-required-blocker-1.cycle.md`
- P1_3_implementation_status: `BLOCKED`
- P1_4_status: `NOT_STARTED`

## authority and objective

The repository currently has no accepted/unambiguous product runtime substrate.

This Task MUST NOT implement P1-3 safeguards.

Its purpose is to create one Human-reviewable canonical candidate:

```text
.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md
```

The candidate must establish enough executable substrate ownership that a later reissued P1-3
implementation Task can start without choosing language/framework/build/source layout by
convenience.

Human acceptance remains mandatory.

---

# Stage 0 — persist the previous P1-3 blocker provenance

## expected repository precondition

```text
repository:
C:\Users\oracl\IdeaProjects\ai-software-command-center

branch:
main

HEAD:
4ec8bf49330128f5fccb70d94a863dc57f9984d2
```

Expected tracked dirty provenance after the previous Task completed:

```text
.aiassistant/tasks/done/20260827_1421_aiscc-p1-3-security-runtime-safeguard-implementation-with-closure-repair-commit-1.md

.aiassistant/records/aiscc/cycles/20260827_1442_aiscc-p1-3-runtime-substrate-decision-required-blocker-1.cycle.md
```

The Cycle is provided by Command Center/Human before Executor start.

Ignored current active Task and target export are not tracked commit inputs.

## Stage 0 preflight

Before Git index mutation:

1. verify repository root;
2. verify branch;
3. verify HEAD exactly `4ec8bf49330128f5fccb70d94a863dc57f9984d2`;
4. inspect `git status --short`;
5. verify no tracked dirty path exists outside the exact two-path provenance set;
6. verify the done Task has exact `task_id`;
7. verify blocker Cycle has exact `cycle_id`;
8. run `git diff --check`;
9. verify no secret/private material;
10. verify current active Task is this Task.

If another tracked dirty path exists:

```text
STOP
→ BLOCKED_BLOCKER_PROVENANCE_COMMIT_COLLISION
```

Do not reset/stash/clean.

## authorized Git operations

Exactly one local provenance commit is authorized.

Stage exact changed paths only:

```text
git add -- \
  .aiassistant/tasks/done/20260827_1421_aiscc-p1-3-security-runtime-safeguard-implementation-with-closure-repair-commit-1.md \
  .aiassistant/records/aiscc/cycles/20260827_1442_aiscc-p1-3-runtime-substrate-decision-required-blocker-1.cycle.md
```

If one expected path is already clean/tracked at HEAD, stage only the actual changed member and
explain it. No unrelated path may be added.

Forbidden:

```text
git add .
git add -A
git commit -a
git amend
git reset
git stash
git clean
git fetch
git pull
git push
branch/tag/remote mutation
```

Exact commit message:

```text
docs: record P1-3 runtime substrate blocker

Persist the completed P1-3 preflight and its runtime-substrate blocker.

Record that safeguard implementation did not start and require an explicit
Human-accepted runtime substrate baseline before P1-3 resumes.
```

After commit:

```text
RUNTIME_SUBSTRATE_DESIGN_BASE_COMMIT=<full hash>
```

Verify:

- parent is `4ec8bf49330128f5fccb70d94a863dc57f9984d2`;
- commit contains only the allowed provenance path(s);
- tracked worktree clean;
- no remote operation.

After this commit:

```text
git add / commit / push
→ FORBIDDEN
```

The runtime substrate candidate remains uncommitted for Human review.

---

# Stage 1 — evidence gathering for substrate decision

## exact canonical read set

Read:

1. `.aiassistant/rules/AISCC_AGENTS.md`
2. `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`
3. `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`
4. `.aiassistant/rules/AISCC_DOCUMENT_LANGUAGE_POLICY.md`
5. `.aiassistant/records/command-center/COMMAND_CENTER_WORKFLOW.md`
6. `.aiassistant/records/command-center/JUDGMENT_RUBRIC.md`
7. `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`
8. `.aiassistant/records/aiscc/DECISION_REGISTER.md`
9. `.aiassistant/records/aiscc/NEXT_ACTIONS.md`
10. `.aiassistant/rules/AISCC_ARCHITECTURE.md`
11. `.aiassistant/rules/AISCC_ORCHESTRATION.md`
12. `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
13. `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
14. `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
15. `.aiassistant/records/aiscc/cycles/20260827_1442_aiscc-p1-3-runtime-substrate-decision-required-blocker-1.cycle.md`
16. `.aiassistant/tasks/done/20260827_1421_aiscc-p1-3-security-runtime-safeguard-implementation-with-closure-repair-commit-1.md`

Do not use Browser chat as authority.

## repository inspection allowed

Read-only inspect:

- repository root;
- tracked files/directories;
- existing scripts/utilities;
- installed runtime/tool versions available locally.

Allowed non-mutating probes include equivalent of:

```text
python --version
py --version
node --version
npm --version
java -version
javac -version
mvn -version
gradle -version
go version
docker --version
docker compose version
podman --version
git --version
```

A command being installed is evidence of local availability only.

```text
locally installed
!= selected substrate
```

Do NOT install missing tools.

No network/provider/package-registry access.

---

# Stage 2 — substrate option analysis

## required candidate families

Evaluate at least three materially different application-runtime families that can plausibly
implement AISCC under the accepted architecture/security baseline.

At minimum compare:

```text
A. Python-based typed service/runtime
B. TypeScript/Node-based service/runtime
C. JVM-based service/runtime
```

A fourth family such as Go MAY be included if it is genuinely competitive for this project.

Do not create a straw-man option.

The exact framework candidates inside each family are design decisions.

## evaluation criteria

Use project-specific criteria, not generic popularity.

At minimum:

1. implementation speed before competition deadlines;
2. direct explicit state-machine implementation clarity;
3. typed domain-model quality;
4. deterministic policy/security admission implementation;
5. subprocess/filesystem/network sandbox-control ergonomics;
6. async external API/provider integration suitability for future P1-5;
7. runtime/test tooling for P1-3 proof classes;
8. PostgreSQL integration path without prematurely designing schema;
9. HTTP API suitability for later bounded Live;
10. structured logging/provenance ergonomics;
11. dependency/lockfile/build reproducibility;
12. container execution/evidence compatibility;
13. Railway-compatible service deployment direction without claiming deployment;
14. local developer/tool availability as a secondary signal;
15. operational simplicity for a competition MVP;
16. future maintainability after the competition.

Do not use "the Human already knows language X" as a sole or decisive criterion.

## decision rule

Produce:

- option matrix;
- explicit rejected reasons;
- one primary recommended substrate;
- one fallback substrate;
- exact uncertainties/deferred decisions.

A tie is not acceptable unless there is a genuine Human policy choice that cannot be resolved by
technical evidence.

If such a policy tie remains, state exactly:

```text
HUMAN_POLICY_SELECTION_REQUIRED
```

but still narrow the choice to the smallest defensible set.

---

# Stage 3 — AISCC_RUNTIME_SUBSTRATE.md candidate

Create:

```text
.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md
```

Status:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING
```

It MUST define the recommended candidate exactly enough for P1-3 to implement after Human
acceptance.

## required decision A — application runtime

Define:

```text
language:
runtime/version policy:
framework:
framework role:
```

Avoid an unnecessary framework if a smaller runtime is better, but make the decision explicit.

Exact patch versions MAY be deferred to implementation environment verification; language/runtime
major/minor compatibility policy must be sufficiently clear.

## required decision B — package/build/reproducibility

Define:

```text
package manager / build tool
manifest filename
lockfile filename
runtime/start command convention
test command convention
lint/static/type-check command convention
```

If a tool has no conventional lockfile, state the reproducibility mechanism.

## required decision C — canonical source layout

Define exact planned roots, for example conceptually:

```text
<runtime_source_root>
<test_root>
<configuration_root if separate>
```

Choose actual repository-relative paths.

Do not create those product directories in this Task.

P1-3 implementation will create them after Human acceptance.

## required decision D — entrypoint and module ownership

Define:

- application/service entrypoint convention;
- security policy module owner;
- runtime adapter boundary;
- future state-machine kernel boundary;
- provider/tool adapter boundary;
- no circular authority between security admission and workflow mutation.

Preserve:

```text
SecurityAdmissionDecision
!= TransitionDecision
```

## required decision E — sandbox/evidence execution substrate

This is load-bearing for P1-3.

Decide exact candidate policy for producing actual security runtime evidence.

At minimum answer:

```text
Will P1-3 use container-based sandbox/evidence runtime?
If yes: Docker, Podman, or another exact substrate candidate.
If no: what OS/runtime primitive provides process/filesystem/network isolation evidence?
```

The design MUST NOT claim isolation is implemented.

Define:

- local development/evidence requirement;
- per-run sandbox process/container boundary;
- network deny/allow evidence path;
- filesystem isolation evidence path;
- cleanup/residue path;
- behavior when the required sandbox runtime is not locally available.

If Docker/Podman/etc. is selected but absent locally:

```text
implementation prerequisite
→ HUMAN_ENVIRONMENT_PREPARATION_REQUIRED
```

Do not install it in this Task.

## required decision F — persistence boundary

Define only substrate-level ownership:

```text
PostgreSQL-compatible persistence adapter direction
migration tool direction
transaction boundary ownership
```

Do NOT design tables/schema yet unless a currently accepted Task owns that decision.

In-memory/test adapter is allowed for isolated security tests, but:

```text
test adapter
!= production persistence
```

## required decision G — configuration and secret boundary

Define:

- configuration mechanism convention;
- environment/config separation;
- secret references rather than raw secret persistence;
- local test fake/opaque capability policy;
- no credentials committed to repository.

Do not choose or configure production secret manager.

## required decision H — minimum repository bootstrap to be created by P1-3

List exact files/directories P1-3 will be authorized to create after acceptance.

Examples conceptually:

```text
manifest
lockfile
runtime source root
test root
configuration/tooling files
container/evidence files if selected
```

The list must be explicit enough that P1-3 will not invent a new structure.

## required decision I — version/dependency authority

Define who may change:

- runtime major/minor;
- framework major;
- package/build tool;
- sandbox runtime strategy.

Load-bearing substrate changes require a separate Human-accepted baseline update.

Routine patch/dependency updates may be delegated only if the rule makes the boundary explicit.

## required decision J — P1-3 resume contract

State exactly:

```text
After Human accepts AISCC_RUNTIME_SUBSTRATE.md
→ P1-3 implementation Task may create the authorized runtime bootstrap
→ implement security safeguard slice
→ produce non-substitutable runtime evidence

P1-4 remains separate.
```

---

# non-goals

This Task MUST NOT:

- implement application runtime;
- create source/test product roots;
- create package/build manifests;
- install dependencies;
- generate lockfiles;
- write Dockerfile/container config;
- implement P1-3 safeguards;
- implement P1-4 state machine;
- implement P1-5 provider/tool adapters;
- access network/package registry/provider;
- create credentials;
- deploy;
- update Browser Project Source;
- claim chosen candidate is accepted before Human review.

Only `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md` plus Task/report/export may be changed after
Stage 0 commit.

---

# allowed paths after Stage 0 commit

```text
.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md

.aiassistant/reports/target/20260827_1442_aiscc-p1-3-runtime-substrate-baseline-design-with-blocker-provenance-commit-1/**

.aiassistant/tasks/active/20260827_1442_aiscc-p1-3-runtime-substrate-baseline-design-with-blocker-provenance-commit-1.md

.aiassistant/tasks/done/20260827_1442_aiscc-p1-3-runtime-substrate-baseline-design-with-blocker-provenance-commit-1.md
```

No second Git commit.

---

# evidence contract

## executor_required — BLOCKER_PROVENANCE_GIT

Pass:

- old HEAD `4ec8bf49330128f5fccb70d94a863dc57f9984d2`;
- previous P1-3 done Task + blocker Cycle only;
- one local commit;
- new full `RUNTIME_SUBSTRATE_DESIGN_BASE_COMMIT`;
- post-commit tracked tree clean;
- no remote operation.

## executor_required — REPOSITORY_RUNTIME_INVENTORY

Pass:

- tracked runtime/build/source state enumerated;
- local tool availability probed without mutation/install;
- utility scripts not confused with product runtime.

## executor_required — OPTION_ANALYSIS

Pass:

- at least Python, TypeScript/Node, JVM families evaluated;
- project-specific matrix;
- one primary recommendation;
- one fallback;
- explicit rejected reasons;
- no unsupported popularity claim.

## executor_required — SUBSTRATE_DESIGN

Pass when `AISCC_RUNTIME_SUBSTRATE.md` defines:

- application runtime;
- package/build;
- manifest/lockfile;
- source/test roots;
- entrypoint/module ownership;
- sandbox/evidence substrate;
- persistence adapter/migration direction;
- config/secret convention;
- exact P1-3 bootstrap allowlist;
- version/dependency authority;
- P1-3 resume contract.

## executor_required — P1_BASELINE_CONFORMANCE

Pass:

- P1-1 WorkflowState/authority unchanged;
- P1-2 security hard prohibitions unchanged;
- `SecurityAdmissionDecision != TransitionDecision`;
- no runtime candidate weakens public Live boundary;
- P1-3 remains first safeguard implementation stage;
- P1-4 remains separate.

## executor_required — DOCUMENT_INTEGRITY

Pass:

- strict UTF-8;
- Markdown fence parity;
- no control chars;
- no unresolved placeholder;
- `git diff --check` or equivalent.

## human_owned — HUMAN_VERIFICATION

Human reviews:

- primary runtime choice;
- fallback choice;
- package/build and repository layout;
- sandbox/evidence runtime;
- local environment prerequisite;
- persistence/config direction;
- exact P1-3 bootstrap scope;
- maintainability/competition tradeoff.

Expected:

```text
ACCEPTED
HOLD_REWORK_REQUIRED
or exact correction
```

The Agent/Executor MUST NOT mark the substrate accepted.

## not_required

- application build;
- unit/integration test execution of new product code;
- sandbox runtime proof;
- DB runtime;
- provider/network access;
- deployment;
- Browser Project Source sync.

## forbidden

- dependency install;
- package-registry/network access;
- application/source bootstrap;
- container config creation;
- P1-3/P1-4 implementation;
- second Git commit;
- Git push/remote mutation;
- provider/credential/deployment.

---

# proof non-substitution

```text
local runtime installed
!= selected product runtime

recommended substrate
!= Human-accepted substrate

design document
!= buildable application

container strategy
!= container isolation proof

test-layout decision
!= tests implemented

PostgreSQL adapter direction
!= DB schema

runtime substrate acceptance
!= P1-3 safeguard acceptance
```

---

# workflow expectation

```text
initial:
P1-3 BLOCKED_RUNTIME_SUBSTRATE_DECISION_REQUIRED

expected Executor result:
ACCEPTED_CANDIDATE / HUMAN_REVIEW_PENDING

Human accepted result:
RUNTIME_SUBSTRATE_BASELINE_ACCEPTED

then:
reissue/resume P1-3 safeguard implementation

P1-4:
still NOT_STARTED
```

---

# accept criteria for candidate

- blocker provenance commit succeeds;
- one coherent substrate recommendation;
- exact source/build/test/sandbox boundary;
- recommendation supports P1-3 evidence without redefining P1-1/P1-2;
- no speculative product implementation;
- no dependency install/network;
- Human review pending.

# hold/reject criteria

- chooses language solely because installed locally;
- no comparison;
- source/test roots still undefined;
- sandbox/evidence substrate still undefined;
- selected substrate cannot produce required P1-3 proof without another hidden architecture choice;
- framework/provider logic absorbs P1-4/P1-5 authority;
- public Live hard prohibitions weakened;
- implementation or package install occurs;
- second commit occurs;
- Agent claims Human acceptance.

---

# report required fields

- Task path/id;
- old HEAD;
- exact blocker provenance dirty set;
- Stage 0 commit message;
- `RUNTIME_SUBSTRATE_DESIGN_BASE_COMMIT`;
- post-commit clean evidence;
- exact canonical read inventory;
- repository runtime/source/build inventory;
- local tool availability probes;
- option matrix;
- primary recommendation;
- fallback;
- rejected reasons;
- `AISCC_RUNTIME_SUBSTRATE.md` path/hash;
- exact runtime/build/source/test/sandbox decision summary;
- exact future P1-3 bootstrap allowlist;
- P1-1/P1-2 conformance;
- Human pending;
- forbidden-not-run;
- rollback;
- preserved paths;
- next recommendation.

---

# export bundle

Target:

```text
.aiassistant/reports/target/20260827_1442_aiscc-p1-3-runtime-substrate-baseline-design-with-blocker-provenance-commit-1/
```

Required:

- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`

---

# Task lifecycle

```text
.aiassistant/tasks/active/20260827_1442_aiscc-p1-3-runtime-substrate-baseline-design-with-blocker-provenance-commit-1.md
→
.aiassistant/tasks/done/20260827_1442_aiscc-p1-3-runtime-substrate-baseline-design-with-blocker-provenance-commit-1.md
```

`done` means submitted, not Human accepted.

---

# preserved artifacts

Always preserve:

- `.aiassistant/tasks/done/20260827_1421_aiscc-p1-3-security-runtime-safeguard-implementation-with-closure-repair-commit-1.md`
- `.aiassistant/records/aiscc/cycles/20260827_1442_aiscc-p1-3-runtime-substrate-decision-required-blocker-1.cycle.md`
- Stage 0 blocker-provenance local commit
- `.aiassistant/tasks/done/20260827_1442_aiscc-p1-3-runtime-substrate-baseline-design-with-blocker-provenance-commit-1.md`

Until Human judgment, preserve candidate:

- `.aiassistant/rules/AISCC_RUNTIME_SUBSTRATE.md`

Temporary target bundle may be deleted after Human judgment and durable provenance persistence.

---

# next action after Human acceptance

```text
reissue P1-3 Security / Runtime Safeguard Implementation and Verification
using the accepted AISCC_RUNTIME_SUBSTRATE baseline
```

Do not execute P1-4 in this Task.
