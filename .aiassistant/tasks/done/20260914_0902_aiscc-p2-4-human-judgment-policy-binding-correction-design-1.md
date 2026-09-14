# 작업지시서: P2-4 Human/Judgment policy binding correction design

## meta

- task_id: `20260914_0902_aiscc-p2-4-human-judgment-policy-binding-correction-design-1`
- created_at: `2026-09-14T09:02:00+09:00`
- work_type: `DESIGN_AUDIT / CORRECTION_PROPOSAL`
- execution_mode: `MANUAL_COMMAND_CENTER`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_base_HEAD: `5aaeb6f690cd9209af57a60b846ac049e89e9047`
- required_parent: `4685cff66a0ff42f53db66567f6f5a2340ccbef8`
- predecessor_result_zip_sha256: `568ae78f1ff7f0b491eb9f1617de7be750589d86a7759830be5882cd3b244679`
- predecessor_done_task_sha256: `62d9f9ebe3a4221b773ef4c6b9983cd68606752324e6dcd008e8808631fef3fe`
- predecessor_result: `BLOCKED / AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED`
- predecessor_executor_disposition: `ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED`
- command_center_defect: `ACCEPTED_DESIGN_HUMAN_POLICY_BINDING_OVER-SPECIFIED`
- product_source_change_authorized: `No`
- canonical_baseline_mutation_authorized: `No`
- migration_or_DB_authorized: `No`
- Docker_authorized: `No`
- provider_network_authorized: `No`
- source_commit_authorized: `No`
- push_authorized: `No`
- fresh_IDE_chat_required: `No`
- success_ceiling: `P2_4_HUMAN_JUDGMENT_POLICY_BINDING_CORRECTION_PROPOSAL / HUMAN_REVIEW_PENDING`

# 0. current Browser judgment

0846 result is classified:

```text
BLOCKED / AUTHORITY_OWNER_SCOPE_EXPANSION_REQUIRED
```

Executor behavior:

```text
ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED
```

This is NOT an existing P1-7 runtime regression.

Browser Command Center owns the accepted-design defect:

```text
0319 proposal required:
human_binding.policy_fingerprint
and independent pre-WorkRun Human policy resolution

current P1-7 owner surface:
authority_policy_ref / authority_policy_version / required_uses
+ request/gate-time owner semantics
without an established independent policy-content fingerprint resolver
```

0846 correctly refused to invent a fingerprint, reuse gate_fingerprint, or add a new Human policy issuer outside Task scope.

# 1. normative predecessor inputs

Package contains exact copies:

```text
ACCEPTED_INPUT/TASKCONTRACT_DURABLE_BODY_BASELINE_PROPOSAL.md
SHA-256:
803686433f900282117a4318d8f59a14b5b5a68735775b4f1242acf544c16410

ACCEPTED_INPUT/20260914_0812_aiscc-p2-4-durable-taskcontract-body-ref-compatibility-human-correction-review-1.md
SHA-256:
4c6905734e7a48b9688257574d86b1a7215627ac8514c7112747889c6bafa318
```

The 0812 body_ref correction remains Human ACCEPTED and is NOT under review.

The only design area reopened here is:

```text
human_binding
judgment_binding
their issuance-time owner verification semantics
```

Do not redesign other accepted durable-body semantics.

# 2. exact repository preflight

Require before governance mutation:

```text
branch:
main

HEAD:
5aaeb6f690cd9209af57a60b846ac049e89e9047

HEAD^:
4685cff66a0ff42f53db66567f6f5a2340ccbef8

index:
empty

tracked:
clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0846_aiscc-p2-4-taskcontract-durable-body-corrected-baseline-runtime-implementation-retry-1.md

SHA-256:
62d9f9ebe3a4221b773ef4c6b9983cd68606752324e6dcd008e8808631fef3fe
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

# 3. governance placement + Commit A

Place current Task first in `.aiassistant/tasks/active` and read it.

Then place:

```text
20260914_0902_aiscc-p2-4-human-policy-owner-binding-blocked-correction-design-entry-1.cycle.md
-> .aiassistant/records/aiscc/cycles/

20260914_0902_aiscc-p2-4-0846-human-policy-binding-blocked-correction-design-authorization-1.md
-> .aiassistant/reports/aiscc/
```

Before commit, Git-visible untracked exactly:

```text
.aiassistant/tasks/done/20260914_0846_aiscc-p2-4-taskcontract-durable-body-corrected-baseline-runtime-implementation-retry-1.md
.aiassistant/records/aiscc/cycles/20260914_0902_aiscc-p2-4-human-policy-owner-binding-blocked-correction-design-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_0902_aiscc-p2-4-0846-human-policy-binding-blocked-correction-design-authorization-1.md
```

Commit exactly:

```text
docs(aiscc): record human policy binding blocker
```

Commit parent must be `5aaeb6f690cd9209af57a60b846ac049e89e9047` and changed paths exact 3.

No other commit authorized.

# 4. required canonical/source reads

At minimum read:

```text
.aiassistant/rules/AISCC_ARCHITECTURE.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
.aiassistant/rules/AISCC_HUMAN_GATE_JUDGMENT.md
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md

src/aiscc/human/models.py
src/aiscc/human/authority.py
src/aiscc/human/repository.py
src/aiscc/judgment/**
src/aiscc/workflow/**
src/aiscc/persistence/models.py
```

Read exact directly affected tests as needed.

No source mutation.

# 5. source-owned facts that must be preserved

Treat these as invariants unless exact current repository disproves them:

```text
G_HUMAN_NOT_REQUIRED:
applicable TaskContract/judgment policy says HumanResult is not required

Human policy:
TaskContract/System-issued policy, not caller metadata

HumanGateReservationAuthority:
current P1-7 owner

HumanGate/HumanResult/Judgment:
P1-7 authority remains unchanged

Judgment owner policy:
SYSTEM_DETERMINISTIC / HUMAN / COMMAND_CENTER

TaskContract body:
may bind policy identity/configuration
but must not claim a Human gate/result/Judgment already exists or is satisfied
```

Do not create an external Human policy authority merely because the 0319 proposal invented `policy_fingerprint`.

# 6. substantive goal

Produce one exact implementation-ready correction for BOTH:

```text
human_binding
judgment_binding
```

The correction must use existing P1-7 / Judgment owner semantics wherever possible.

First answer from source:

```text
A. What exact pre-WorkRun policy identity/configuration can an immutable TaskContract legitimately carry today?
B. Which fields are owned by TaskContract itself vs P1-7 runtime?
C. What exact fields does HumanGateReservationAuthority require to later reserve/open a gate?
D. How is G_HUMAN_NOT_REQUIRED established from TaskContract/judgment policy without a gate?
E. What exact judgment owner-policy identity/configuration is required before WorkRun?
F. Does current source expose an independent Human policy fingerprint or Judgment policy fingerprint authority?
G. If not, is such a fingerprint actually required by canonical baseline?
H. Can body_sha256 itself provide immutable integrity for TaskContract-owned policy configuration without creating a second policy authority?
```

# 7. preferred correction principle

Prefer, if supported by exact source/canonical semantics:

```text
TaskContract-owned policy binding fields
that mirror existing owner-consumed identity/configuration

instead of:
new independent policy-content fingerprint authority
```

A valid correction may remove `policy_fingerprint` from Human/Judgment binding if and only if exact current canonical/source semantics show that:

1. the policy configuration is legitimately TaskContract-owned;
2. the whole immutable body hash already protects those exact fields;
3. current P1-7/Judgment owners can consume/verify the binding without trusting caller metadata;
4. no semantic owner is weakened.

Do NOT assume this conclusion; prove or reject it from source.

# 8. required exact output

Produce:

```text
HUMAN_JUDGMENT_POLICY_SOURCE_AUDIT.md
HUMAN_BINDING_CORRECTION_PROPOSAL.md
JUDGMENT_BINDING_CORRECTION_PROPOSAL.md
OWNER_NON_SUBSTITUTION_PROOF.md
IMPLEMENTATION_IMPACT_ALLOWLIST.md
BASELINE_SUPERSESSION_DELTA.md
CONTRACT_REVIEW.md
```

The proposal must select ONE preferred correction.

For each corrected object specify:

```text
closed exact field set
field types
owner of every field
canonicalization/hash behavior
issuance-time verification
READY-time verification
runtime handoff to existing owner
NOT_REQUIRED semantics
REQUIRED semantics
negative cases
backward/legacy behavior
```

# 9. anti-recursion / no-new-authority gate

Explicitly test whether the proposed correction accidentally requires:

```text
a new Human policy registry
a new Judgment policy registry
a new persistent policy table
a new HumanGate identity before WorkRun
a fake reservation
a caller callback treated as authority
gate_fingerprint reused as policy identity
agent/Command Center prose treated as runtime truth
```

If the exact current owner semantics truly require one of those, do not invent it.

Instead output:

```text
P2_4_HUMAN_POLICY_OWNER_EXTENSION_REQUIRED
```

with exact minimal owner extension and exact source/rule paths that would require Human approval.

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

Only Governance Commit A is allowed.

# 11. report/export

Target:

```text
.aiassistant/reports/target/20260914_0902_aiscc-p2-4-human-judgment-policy-binding-correction-design-1/
```

Required root:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
ACCEPTED_INPUT_VERIFICATION.md
HUMAN_JUDGMENT_POLICY_SOURCE_AUDIT.md
HUMAN_BINDING_CORRECTION_PROPOSAL.md
JUDGMENT_BINDING_CORRECTION_PROPOSAL.md
OWNER_NON_SUBSTITUTION_PROOF.md
IMPLEMENTATION_IMPACT_ALLOWLIST.md
BASELINE_SUPERSESSION_DELTA.md
CONTRACT_REVIEW.md
```

Include canonical current Cycle/Judgment/done Task copies.

No unrelated source copies.

# 12. terminal boundary

Move current Task active -> done byte-identically.

Require terminal:

```text
HEAD = Governance Commit A
index empty
tracked clean

Git-visible untracked exactly:
.aiassistant/tasks/done/20260914_0902_aiscc-p2-4-human-judgment-policy-binding-correction-design-1.md
```

Canonical state unchanged.
Legacy 1400 ignored Task unchanged.

# 13. success ceiling

Success:

```text
P2_4_HUMAN_JUDGMENT_POLICY_BINDING_CORRECTION_PROPOSAL
/ HUMAN_REVIEW_PENDING
```

This does NOT mean:

```text
runtime implemented
migration created
self-dogfood source candidate created
golden cycle performed
P2-4 accepted
```
