# 작업지시서: P2-4 template/approval authority binding correction design

## meta

- task_id: `20260914_0940_aiscc-p2-4-template-approval-authority-binding-correction-design-1`
- created_at: `2026-09-14T09:40:20+09:00`
- work_type: `DESIGN_AUDIT / CORRECTION_PROPOSAL`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `f0e55ecd9e65f2b10d529d5a6469452826bedffb`
- required_parent: `c10f89256b88d90782c7fbdea6ff8b27655f2b46`
- predecessor_result_zip_sha256: `d44b88b5ac65d80e826fa1ca4074f7cc80101185684074dc10cd27ee507212ca`
- predecessor_done_task_sha256: `1ebd39a8d9bd88a8309352bd13d5901d8533e03d635db4be636e9da3beb368bd`
- predecessor_result: `BLOCKED / POLICY_CONFLICT_INVESTIGATION_REQUIRED`
- predecessor_executor_disposition: `ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED`
- command_center_defect_candidate: `ACCEPTED_DESIGN_TEMPLATE_AUTHORITY_OVER-SPECIFIED_OR_OWNER_GAP`
- product_source_change_authorized: `No`
- canonical_baseline_mutation_authorized: `No`
- migration_or_DB_authorized: `No`
- Docker_authorized: `No`
- provider_network_authorized: `No`
- source_commit_authorized: `No`
- push_authorized: `No`
- fresh_IDE_chat_required: `No`
- success_ceiling: `P2_4_TEMPLATE_APPROVAL_AUTHORITY_BINDING_CORRECTION_PROPOSAL / HUMAN_REVIEW_PENDING`

# 0. Browser judgment of 0923

0923 result:

```text
BLOCKED / POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Executor behavior:

```text
ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED
```

0923 independently verified:

```text
result ZIP SHA-256:
d44b88b5ac65d80e826fa1ca4074f7cc80101185684074dc10cd27ee507212ca

27 members
26 manifest rows
one top-level directory
CRC PASS
all manifest size/SHA exact
TASK/Cycle/Judgment/Human review exact
```

Governance Commit A:

```text
f0e55ecd9e65f2b10d529d5a6469452826bedffb

parent:
c10f89256b88d90782c7fbdea6ff8b27655f2b46

message:
docs(aiscc): accept taskcontract human judgment binding correction
```

No canonical baseline/product/test/migration/runtime implementation occurred.
No Result Commit B.
Docker local image inspect only; DB/container execution 0.

The blocker is NOT a Human/Judgment regression and does NOT invalidate 0812/0902 accepted corrections.

# 1. exact issue to resolve

The accepted 0319 proposal still requires:

```text
authority_refs must include:
- approved template ref/hash
- owner approval source ref/hash

issuance requires:
- selected descriptor's exact issuance owner
- approved template/scope for P2-4
- complete body authorized against selected template/scope
```

Current owner evidence from 0923 shows:

```text
current P1-8 catalog:
exactly two entries

task_template_ref:
null

task_template_hash:
null

current owner-recognized fixed descriptor:
task_template_ref = NONE
task_template_hash = NONE
```

Current canonical P1-8 prerequisite baseline also says plain Markdown rule/roadmap path/hash/heading is:

```text
EXISTING_BUT_INSUFFICIENT
```

for TaskConstraint/descriptor authority.

The design must now determine whether the 0319 separate template/approval-source binding:

A. is actually required by accepted architecture/product invariants and therefore exposes a genuine owner gap; or

B. was an over-specified Browser design requirement and should be removed/replaced by already authoritative P1-8 selection/descriptor + Command Center TaskContract authorization semantics.

Do not assume A or B. Prove one from exact current repository.

# 2. normative inputs bundled

Package inputs:

```text
ACCEPTED_INPUT/TASKCONTRACT_DURABLE_BODY_BASELINE_PROPOSAL.md
SHA-256:
803686433f900282117a4318d8f59a14b5b5a68735775b4f1242acf544c16410

ACCEPTED_INPUT/TEMPLATE_AUTHORITY_SOURCE_EVIDENCE.json
SHA-256:
67df59d08408480ef1bb1c202f7642c1330f9f9cccb109a8f3e20b59b81f34eb
```

`TEMPLATE_AUTHORITY_SOURCE_EVIDENCE.json` is predecessor read-only source evidence, not canonical authority by itself.

0812 body_ref correction and 0902 Human/Judgment corrections remain Human ACCEPTED and are outside this audit except for compatibility/non-substitution checks.

# 3. exact repository preflight

Require:

```text
branch:
main

HEAD:
f0e55ecd9e65f2b10d529d5a6469452826bedffb

HEAD^:
c10f89256b88d90782c7fbdea6ff8b27655f2b46

index:
empty

tracked:
clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0923_aiscc-p2-4-taskcontract-durable-body-human-judgment-corrected-runtime-implementation-retry-1.md

SHA-256:
1ebd39a8d9bd88a8309352bd13d5901d8533e03d635db4be636e9da3beb368bd
```

Preserve ignored legacy Task:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md

SHA-256:
52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

Canonical state hashes must remain exact:

```text
CURRENT_STATE_SUMMARY.md
80b16f9a5fab2aa7870baeac4ec6fbf27d08bb50637ed61618573ce0bc2ded48

DECISION_REGISTER.md
9da6dde722f2552020a40085995fef062a8920e477da7656c3a176fff52142e5

NEXT_ACTIONS.md
050a93baf1740f298ec2601c08b392118b143f9838002c159b5401ccf6418679
```

Mismatch -> STOP.

# 4. governance placement + Commit A

Place current Task first in `.aiassistant/tasks/active`, read it, verify bundled inputs, then place:

```text
20260914_0940_aiscc-p2-4-template-authority-binding-blocked-correction-design-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_0940_aiscc-p2-4-0923-template-authority-binding-blocked-correction-design-authorization-1.md
-> .aiassistant/reports/aiscc/
```

Before commit Git-visible untracked exactly:

```text
.aiassistant/tasks/done/20260914_0923_aiscc-p2-4-taskcontract-durable-body-human-judgment-corrected-runtime-implementation-retry-1.md
.aiassistant/records/aiscc/cycles/20260914_0940_aiscc-p2-4-template-authority-binding-blocked-correction-design-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_0940_aiscc-p2-4-0923-template-authority-binding-blocked-correction-design-authorization-1.md
```

Commit exactly:

```text
docs(aiscc): record task template authority blocker
```

Parent must be `f0e55ecd9e65f2b10d529d5a6469452826bedffb`.
Changed paths exact 3.
No other commit authorized.

# 5. required canonical/source reads

Read at minimum:

```text
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md

src/aiscc/next_action/models.py
src/aiscc/next_action/repository.py
src/aiscc/next_action/**
src/aiscc/task_authority/models.py
src/aiscc/task_authority/authority.py
src/aiscc/task_authority/ports.py
src/aiscc/task_authority/repository.py
src/aiscc/workflow/**
```

Read directly affected P1-8/task-authority tests as needed.

No source mutation.

# 6. source questions that MUST be answered

Answer exactly from current repository:

```text
A. What semantic authority does ActionDescriptorV1 currently provide?
B. What does task_template_ref/hash mean when present?
C. Are task_template_ref/hash required for every descriptor, or only one source kind/mode?
D. Why are current POLICY_ACTION_CATALOG descriptors owner-recognized with null template fields?
E. What exact source rejects non-catalog source without enrolled external template owner proof?
F. Does P1-8 define template identity as TaskContract authority, or only descriptor/source provenance?
G. What current object fixes goal/scope for a Task issuance candidate?
H. What current object fixes action class/priority/issuance owner?
I. What exact Command Center/Human policy authority is already allowed to define a complete TaskContract body?
J. Does canonical TaskContract definition require a separately persisted template object/ref/hash?
K. Does core architecture require template approval-source hash specifically?
L. If template refs are absent, can a deterministic body still be authoritative when:
   - selection is owner-replayed/current,
   - descriptor is owner-recognized/current,
   - issuance owner is exact,
   - source_next_action is exact,
   - body scope/goal/policies are immutable and Command Center-authorized,
   - TaskConstraintRef/body persistence verifies bytes?
M. Would adding a new template owner change P1-8 semantics or merely fill an already-defined optional field?
N. Does P2-4 self-dogfood actually require such an owner to prove the core thesis?
```

# 7. two candidate outcomes

Select exactly one.

## Outcome A — correction/removal

Use only if repository proves the separate template/approval-source requirement was Browser over-specification.

Proposal must define the exact replacement authority:

```text
source_next_action:
existing authoritative P1-8 selection/descriptor/candidate lineage

issuance owner:
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY

TaskContract complete-body authorization:
Command Center/Human-accepted TaskContract policy + exact immutable body

scope/goal:
body itself, checked against source action/descriptor and repository binding

authority_refs:
only existing independently owner-verifiable refs actually required by canonical owners
```

It must explicitly explain why:

```text
task_template_ref/hash = NONE/null
```

does not authorize arbitrary task generation and does not weaken scope/goal authority.

It must preserve:

```text
no LLM/freeform NextAction selection
no Agent self-authorization
TaskIssuanceCandidate != TaskContract
source action != complete work contract
```

Define exactly which 0319 clauses are superseded and which remain.

## Outcome B — owner extension required

Use only if repository proves separate independently owner-issued template approval is semantically mandatory.

Output:

```text
P2_4_TEMPLATE_AUTHORITY_OWNER_EXTENSION_REQUIRED
```

and define the MINIMAL exact extension:

- semantic owner;
- whether it is P1-8 or EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY;
- model/API;
- persistence requirement or no-persistence rationale;
- template identity/hash/body;
- approval-source identity;
- descriptor binding;
- issuance-time verification;
- currentness/supersession;
- exact source/rule/migration/test paths;
- why current optional null fields are insufficient;
- why the extension is submission-blocking.

Do NOT implement it.

# 8. anti-authority-substitution

Both outcomes must explicitly reject:

```text
plain Markdown file hash treated as runtime authority
NONE/null treated as SHA-256
Agent-generated template approval
LLM-selected scope
caller-provided descriptor treated as owner proof
TaskIssuanceCandidate treated as TaskContract
ActionDescriptor treated as complete TaskContract without verification
body_sha256 treated as owner approval by itself
```

Also verify the correction does not weaken:

- 0812 body_ref identity correction;
- 0902 Human binding correction;
- 0902 Judgment binding correction;
- P1-6 evidence owner;
- P1-7 Human/Judgment owner;
- P1-4 transition owner.

# 9. required outputs

Produce:

```text
TEMPLATE_AUTHORITY_CANONICAL_AUDIT.md
P1_8_DESCRIPTOR_TEMPLATE_SEMANTICS_AUDIT.md
TASKCONTRACT_TEMPLATE_REQUIREMENT_CORRECTION_PROPOSAL.md
OWNER_NON_SUBSTITUTION_PROOF.md
BASELINE_SUPERSESSION_DELTA.md
IMPLEMENTATION_IMPACT_ALLOWLIST.md
CONTRACT_REVIEW.md
```

If Outcome A selected, proposal must be implementation-ready and Human-reviewable.

If Outcome B selected, owner extension design must be exact enough for Human review without another discovery task.

# 10. no product work

Forbidden:

```text
product/test source mutation
canonical rule mutation
migration creation
DB/Docker
provider/network
actual self-dogfood run
source commit
push/deploy
```

Only Governance Commit A is authorized.

# 11. report/export

Target:

```text
.aiassistant/reports/target/20260914_0940_aiscc-p2-4-template-approval-authority-binding-correction-design-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ACCEPTED_INPUT_VERIFICATION.md
TEMPLATE_AUTHORITY_CANONICAL_AUDIT.md
P1_8_DESCRIPTOR_TEMPLATE_SEMANTICS_AUDIT.md
TASKCONTRACT_TEMPLATE_REQUIREMENT_CORRECTION_PROPOSAL.md
OWNER_NON_SUBSTITUTION_PROOF.md
BASELINE_SUPERSESSION_DELTA.md
IMPLEMENTATION_IMPACT_ALLOWLIST.md
CONTRACT_REVIEW.md
```

Include canonical current Cycle/Judgment/done Task copies.

# 12. terminal boundary

Move current Task active -> done byte-identically.

Require:

```text
HEAD = Governance Commit A
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_0940_aiscc-p2-4-template-approval-authority-binding-correction-design-1.md
```

Legacy 1400 exact unchanged.
Canonical state unchanged.

# 13. success ceiling

Success:

```text
P2_4_TEMPLATE_APPROVAL_AUTHORITY_BINDING_CORRECTION_PROPOSAL
/ HUMAN_REVIEW_PENDING
```

or, when source proves extension mandatory:

```text
P2_4_TEMPLATE_AUTHORITY_OWNER_EXTENSION_REQUIRED
/ HUMAN_REVIEW_PENDING
```

Neither means runtime implementation or P2-4 acceptance.
