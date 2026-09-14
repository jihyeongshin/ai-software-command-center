# AISCC P2-4 — Self-Dogfood Genesis Bootstrap Authority Human Review

## 0. Browser Command Center judgment

1916 Executor result:

```text
BLOCKED
/ SELF_DOGFOOD_BOOTSTRAP_AUTHORITY_MISSING
/ BROWSER_REVIEW_REQUIRED
```

Browser independent disposition:

```text
ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED
```

Browser classification:

```text
HUMAN_DESIGN_DECISION_REQUIRED
/ P1_8_SELF_DOGFOOD_GENESIS_BOOTSTRAP_AUTHORITY
```

This is not an Executor defect.

It is not a regression of the accepted external-IDE start/completion implementation.

It is a missing genesis authority required to create the first real TaskContract/WorkRun in a brand-new operational database while preserving the accepted cycle-derived steady-state model.

## 1. Independent 1916 archive verification

Result ZIP:

```text
SHA-256:
6d55681e007a4039d26747aa351a9317fd389d35efb140e824ebb2d4f1d922e1

members:
49

manifest rows:
48

one top-level directory:
PASS

CRC:
PASS

manifest size/SHA:
48/48 exact
```

Issued governance artifacts are exact:

```text
1916 Cycle:
fc6d544dced0dfb6eaead86ba8ebd5aef71407e49dd41db7361232bad3d24f70

1916 Judgment:
1c06d227f6e70e48eefeb8290a61a466323340ea6c13f4380baf0d1f768ae611

1916 HANDOFF:
6938b4b3ba741d3c5ea1982f5135051a60d48ba8b9799f0032d39a13a86ba16d

1916 outer Task:
9d8964eaa9ca5fbbb9de5e7ea013a9d36f2184bed3e216a1cc31c0e7d4fe8905

1803 done Task:
3dfab04006828711694baee32ece5628eec513ca39a6b4ccd6cf5e42f29d5816
```

Governance Commit A:

```text
e9b38c0c60e940241ec0221136a41481ddc8e1a5

parent:
6eedc50c567f552a3b9d2902c95bd71a99ca441f

message:
docs(aiscc): accept external ide start and enter golden cycle

changed paths:
exact 4
```

No Result Commit B exists.

## 2. Correct fail-closed boundary

1916 stopped before operational authority creation.

Verified absent:

```text
operational PostgreSQL database
TaskContract
SelfDogfoodTaskSpec
WorkRun
READY transition
external IDE start permit
RUNNING transition
completion lease
governed source edit
external submission
EvidenceCandidate
AdmittedEvidence
Judgment
runtime Cycle
result Git commit
resulting NextAction
```

The governed target file was not created.

No provider/LLM/network action occurred.

Therefore no partial golden lineage must be repaired or deleted.

## 3. Exact bootstrap recursion

Current TaskContract V1 is intentionally steady-state cycle-derived only.

Current P1-8 cycle-derived selection requires:

```text
CURRENT NEXT_ACTION_CONTEXT ProjectMemory
+
Cycle provenance
```

Current Cycle admission requires real existing runtime provenance including:

```text
WorkRun
terminal transition
Judgment
satisfied P1-6 evidence
```

But the first golden WorkRun requires:

```text
current NextAction
→ TaskContract
→ WorkRun
```

Therefore an empty operational DB has the recursion:

```text
first NextAction
requires prior Cycle

prior Cycle
requires prior WorkRun

first WorkRun
requires first NextAction
```

No current accepted owner resolves the genesis edge.

## 4. Existing boundaries that must remain true

Preserve all accepted facts:

```text
steady-state TaskContract issuance:
cycle-derived

operational recovery:
valid P1-8 capability globally
but NOT a TaskContract Durable Body V1 source

Replay:
historical/read-only evidence
not current authority

Browser Markdown:
governance provenance
not runtime Cycle authority

canonical state Markdown:
project governance state
not an owner-admitted runtime WorkRun/Cycle
```

The fix must not silently reinterpret any of these.

## 5. Proposed design

Design ID:

```text
AISCC-P1-8-SELF-DOGFOOD-GENESIS-BOOTSTRAP-V1
```

Purpose:

```text
provide exactly one truthful initial NextAction authority
for a project with no operational Cycle/ProjectMemory lineage,
so the first self-dogfood TaskContract can be issued.
```

This is a genesis mechanism, not operational recovery.

## 6. New source mode

Introduce one explicit source/selection mode:

```text
SELF_DOGFOOD_GENESIS
```

It is semantically distinct from:

```text
CYCLE_DERIVED
OPERATIONAL_RECOVERY
```

Do not label genesis as cycle-derived.

Do not relabel operational recovery as genesis.

## 7. New action descriptor

Introduce one exact bounded P1-8 action:

```text
open-self-dogfood-genesis-task-issuance
```

It exists only for the genesis source mode.

It may not become a generic freeform Task generator.

Steady state remains:

```text
open-cycle-derived-task-issuance
```

after a real Cycle exists.

## 8. Genesis authority owner

Owner:

```text
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
/ SELF_DOGFOOD_GENESIS_AUTHORITY_V1
```

The Browser/Command Center may issue the genesis authority only when exact runtime preconditions are verified by product-owned read APIs.

Browser prose itself is not the durable authority.

## 9. Exact genesis eligibility

Genesis issuance is allowed only when all are true for the exact project:

```text
no admitted operational Cycle exists
no CURRENT NEXT_ACTION_CONTEXT ProjectMemory entry exists
no prior genesis authority has completed the project bootstrap
no conflicting current NextAction selection exists
repository identity/root are exact
repository base commit is exact
canonical project/phase identity is exact
requested runtime mode is OWNER_SELF_DOGFOOD
requested public execution mode is AISCC_SELF_DOGFOOD
```

If historical WorkRuns/Cycles already exist in that operational database:

```text
GENESIS_NOT_ELIGIBLE
```

The mechanism is not recovery for a non-empty project.

## 10. Durable GenesisNextActionAuthority

Create an immutable owner-issued genesis authority record equivalent to:

```text
GenesisNextActionAuthorityV1
```

It binds at minimum:

```text
project_id
genesis_authority_id
source_mode = SELF_DOGFOOD_GENESIS
action_id = open-self-dogfood-genesis-task-issuance

repository_id
repository_root
base_commit

phase_id
runtime_mode = OWNER_SELF_DOGFOOD
cycle_execution_mode = AISCC_SELF_DOGFOOD

canonical state refs/fingerprints needed by current Command Center policy

issued_at
issuer identity/version
canonical authority fingerprint
```

No WorkRun identity exists yet.

That absence is explicit and valid only for genesis.

## 11. Currentness

A genesis authority is current only while:

```text
project still has no admitted operational Cycle
and
no cycle-derived CURRENT NEXT_ACTION_CONTEXT exists
and
its repository/base/context remain exact
```

The first admitted real Cycle permanently ends genesis currentness.

After that:

```text
SELF_DOGFOOD_GENESIS
→ non-current forever for this operational project lineage
```

Steady-state selection must become cycle-derived.

## 12. TaskContract V1 extension

Revise TaskContract Durable Body V1 source support from:

```text
SUPPORTED:
CYCLE_DERIVED only
```

to:

```text
SUPPORTED:
SELF_DOGFOOD_GENESIS
CYCLE_DERIVED

UNSUPPORTED:
OPERATIONAL_RECOVERY
```

For genesis, TaskContract body binds the exact genesis authority ref/fingerprint/action/currentness proof.

Do not use the cycle-derived action ID for genesis.

## 13. Lock invariant preservation

The accepted 1212 lock correction remains:

```text
TaskContract issuer/revoker never acquire WorkRun locks
```

Genesis source verification must not acquire a predecessor WorkRun lock because no predecessor WorkRun exists.

Allowed lock shape:

```text
TaskContract family lock
+
genesis authority/currentness lock
```

No source/predecessor WorkRun lock.

READY later still follows the accepted target-WorkRun-first lock order.

## 14. Single-project bootstrap semantics

Genesis authority is not a repeatable Task source.

Recommended rule:

```text
one operational project lineage
→ at most one genesis TaskContract family
```

Exact same TaskContract issuance retry may be idempotent.

Changed TaskContract bytes under the same genesis authority:

```text
DENY
```

After the first actual Cycle is admitted:

```text
new genesis issuance:
DENY
```

## 15. Failure before first Cycle

If the first genesis-backed TaskContract/WorkRun fails before any Cycle can be admitted:

- do not issue a second different genesis Task;
- preserve the same genesis-bound TaskContract family where exact retry semantics permit;
- use fresh WorkRun identity only if current WorkRun semantics allow retry;
- do not silently switch to operational recovery.

If product semantics require a changed Task after such a failure, that is a separate future recovery design question and is not part of V1.

This keeps genesis narrow.

## 16. First golden provenance

The first actual golden cycle may truthfully begin with:

```text
source NextAction mode:
SELF_DOGFOOD_GENESIS
```

It must then produce a real Cycle.

The resulting NextAction after that real Cycle must be:

```text
CYCLE_DERIVED
```

and, for current TaskContract V1 continuation:

```text
open-cycle-derived-task-issuance
```

This transition is part of the golden proof:

```text
GENESIS
→ first actual governed Cycle
→ steady-state CYCLE_DERIVED
```

## 17. ProjectMemory behavior

Do NOT fabricate a fake predecessor CycleMemoryReference.

Preferred:

```text
genesis selection has its own explicit currentness path
without pretending to have Cycle provenance
```

The first actual Cycle admission then creates normal durable ProjectMemory/Cycle-derived context through existing P1-8 rules.

Do not create a special fake `CURRENT NEXT_ACTION_CONTEXT` row whose source claims Cycle provenance when none exists.

## 18. No Replay import

Do not bootstrap by importing Recorded Replay as current runtime authority.

Reason:

```text
Replay is historical/read-only/sanitized
and is not the current operational database lineage.
```

Replay may remain comparison/demo evidence only.

## 19. No canonical-Markdown substitution

Do not convert:

```text
CURRENT_STATE_SUMMARY.md
DECISION_REGISTER.md
NEXT_ACTIONS.md
Browser Cycle/Judgment Markdown
```

directly into WorkRun/Judgment/Cycle runtime rows.

They may bind external Command Center genesis policy/context fingerprints where appropriate, but are not substituted for missing runtime owner objects.

## 20. No operational-recovery substitution

Keep:

```text
open-operational-recovery-task-issuance
```

globally valid where current P1-8 defines it.

But TaskContract Durable Body V1 continues to reject it.

Genesis is a separate supported source because:

```text
empty project initialization
!=
recovery of an existing operational project
```

## 21. Human boundary

This Human decision approves the genesis authority design.

Runtime genesis issuance itself remains a system/Command-Center authority operation.

Do not create:

```text
HumanGate
HumanResult
G_HUMAN_*
```

merely to bootstrap the first Task.

The golden Task's existing `human = NOT_REQUIRED` policy remains separate.

## 22. Evidence/Judgment boundary

Genesis authority owns only initial Task planning/currentness.

It does NOT mint:

```text
EvidenceCandidate
AdmittedEvidence
G_EVIDENCE
Judgment
G_JUDGMENT
Cycle
```

The first golden WorkRun must still earn those through the normal owners.

## 23. Security boundary

Genesis must not become:

```text
generic Task generator
generic planner
LLM NextAction selector
remote executor
provider/tool bypass
direct WorkRun creator
direct Evidence/Judgment creator
automatic deploy/merge/push
```

It issues one bounded initial NextAction authority only.

## 24. Persistence/restart

Genesis authority must be durable.

After restart the system must verify:

```text
authority bytes/fingerprint
issuer
repository/base
project/phase
currentness
whether an actual Cycle now supersedes genesis
TaskContract family binding if issued
```

Missing/tampered/partial lineage:

```text
AUTHORITY_CORRUPTION
```

No silent repair/backfill.

## 25. Migration posture

Prefer additive persistence only if the current P1-8 authority tables cannot represent genesis without false Cycle fields.

Do not overload nullable Cycle fields if doing so makes historical semantics ambiguous.

If a new table is required, use one additive append-only genesis authority table with immutable rows and empty-only downgrade semantics.

Exact migration number must be determined from current HEAD after source audit.

## 26. Expected canonical design updates after Human acceptance

Likely owner documents:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/rules/AISCC_TASKCONTRACT_DURABLE_BODY_AUTHORITY.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
```

Do not mutate unrelated P1-4/P1-5/P1-6/P1-7 owner rules.

## 27. Expected implementation source areas

Subject to exact source audit:

```text
src/aiscc/next_action/models.py
src/aiscc/next_action/repository.py

src/aiscc/task_authority/contracts.py
src/aiscc/task_authority/repository.py

src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py

possibly one additive migration
```

`src/aiscc/cycle/**` and `src/aiscc/memory/**` should remain read-only unless source audit proves an unavoidable integration requirement.

## 28. Required proof before golden retry

Implementation must prove:

```text
empty operational project -> genesis eligible PASS
non-empty Cycle lineage -> genesis DENY
existing current cycle-derived memory -> genesis DENY
wrong repo/base -> DENY
wrong runtime/phase -> DENY
genesis authority durable/restart PASS
tamper -> DENY
genesis NextAction currentness PASS
genesis TaskContract issuance PASS
TaskContract issuer acquires no WorkRun lock
operational recovery still rejected by TaskContract V1
changed genesis TaskContract retry DENY
exact retry idempotent
first actual Cycle supersedes genesis currentness
post-Cycle selection becomes CYCLE_DERIVED
existing cycle-derived regressions PASS
operational-recovery P1-8 regressions PASS
no fake Cycle/Memory/WorkRun/Judgment/Evidence created by genesis
```

## 29. Golden retry after implementation acceptance

After Browser accepts implementation:

```text
fresh empty operational DB
→ genesis NextAction authority
→ genesis-backed TaskContract
→ SelfDogfoodTaskSpec
→ READY
→ external IDE start
→ RUNNING
→ completion lease
→ exact Agent edit
→ external submission
→ Evidence
→ Judgment
→ ACCEPTED
→ first actual Cycle
→ result Git commit
→ resulting CYCLE_DERIVED NextAction
```

That is the correct first-run control-plane story.

## 30. Alternatives considered

### A. Treat Browser Markdown Cycle as runtime Cycle

Rejected.

```text
provenance document != owner-admitted runtime authority
```

### B. Import Recorded Replay into current DB

Rejected for V1.

```text
historical sanitized replay != current operational lineage
```

### C. Use operational recovery for first TaskContract

Rejected.

```text
violates accepted TaskContract V1 source boundary
and conflates initialization with recovery
```

### D. Fabricate predecessor WorkRun/Cycle

Rejected.

```text
would destroy the core governance thesis
```

### E. Add explicit one-time self-dogfood genesis authority

Recommended.

## 31. Browser recommendation

```text
RECOMMENDATION:
ACCEPT
```

Reasons:

1. Every state machine needs a truthful genesis edge; requiring a prior Cycle for the first Cycle is structurally recursive.
2. It keeps steady-state cycle-derived behavior unchanged.
3. It preserves the 1212 no-predecessor-WorkRun-lock rationale.
4. It does not weaken operational recovery restrictions.
5. It makes first-run provenance explicit instead of pretending genesis was cycle-derived.
6. It produces a strong golden demonstration: genesis -> governed execution -> first real Cycle -> steady-state cycle-derived NextAction.
7. It is narrower and more truthful than Replay import or synthetic predecessor creation.

## 32. Human decision requested

Choose exactly one:

```text
ACCEPT
REWORK
REJECT
```

If `ACCEPT`:

Browser Command Center should issue one bounded genesis-authority implementation Task after exact source audit.

That implementation Task must NOT execute the actual golden cycle.

After Browser accepts the genesis implementation, reissue the golden cycle against the then-current repository base.

The current fresh IDE Executor chat may continue for the bounded genesis implementation; a second fresh-chat migration is not required unless a concrete new contamination/performance reason appears.
