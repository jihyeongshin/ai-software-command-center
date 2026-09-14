# AISCC P2-4 — Template/approval authority correction Human review

## 0. Browser Command Center judgment

0940 Executor result:

```text
P2_4_TEMPLATE_APPROVAL_AUTHORITY_BINDING_CORRECTION_PROPOSAL
/ HUMAN_REVIEW_PENDING
```

Browser independent judgment:

```text
ACCEPTED_CANDIDATE / OUTCOME_A / HUMAN_REVIEW_REQUIRED
```

Outcome A means:

```text
0319's universal mandatory approved-template / approval-source ref+hash
was over-specified for the current owner-recognized POLICY_ACTION_CATALOG path.
```

It does NOT mean:

```text
template absence is authority
NONE/null is a hash
ActionDescriptor is a TaskContract
TaskIssuanceCandidate is a TaskContract
body_sha256 alone is approval
runtime implementation exists
P2-4 is accepted/closed
```

## 1. Result integrity

0940 Executor result ZIP:

```text
SHA-256:
f4861616c4b883533f4df238b93218a51cb9dde82033d0b0d82bb4bb5acf9e41
```

Independent verification:

```text
15 members
one top-level directory
CRC PASS
14 EXPORT_MANIFEST rows
all row byte sizes exact
all row SHA-256 exact
no unmanifested member except EXPORT_MANIFEST.md
TASK.md == canonical done Task byte-exact
returned Cycle/Judgment == issued 0940 bytes
```

Governance Commit A reported:

```text
f8193d83d032fc4a0a49d3471205ac693025e4f1

parent:
f0e55ecd9e65f2b10d529d5a6469452826bedffb

message:
docs(aiscc): record task template authority blocker
```

No product/test source, canonical baseline, migration, DB/Docker runtime, provider/network, golden cycle, source implementation commit, push or deployment occurred.

## 2. Exact correction

Supersede only the 0319 clauses that universally require:

```text
approved template ref/hash
owner approval source ref/hash
```

for every complete TaskContract issuance.

For the current owner-recognized `POLICY_ACTION_CATALOG` P2-4 path, the corrected authority chain is:

```text
authoritative/current P1-8 selection
+ owner-recognized/current ActionDescriptor/source lineage
+ exact EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
+ explicit authorization of the complete immutable TaskContract body
+ exact repository/base/scope/policy/evidence bindings
+ durable TaskConstraintRef/event/certified-prefix/body verification
```

A separate approved-template object is not universally required by that chain.

## 3. What remains mandatory

The correction does NOT permit freeform task generation.

The complete body must still explicitly and immutably define:

```text
goal
non_goals
allowed_paths
forbidden_paths
repository/base
source_next_action
evidence binding
Human binding
Judgment binding
execution provenance
all other accepted durable-body fields
```

The body must still be explicitly authorized by:

```text
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
```

before issuance.

The following remain non-authoritative by themselves:

```text
Agent/LLM prose
ActionDescriptor
TaskIssuanceCandidate
body_sha256
Markdown/hash
NONE/null
caller-provided descriptor/candidate
historical replay without currentness
```

## 4. Template semantics preserved

For current owner-recognized catalog descriptors:

```text
task_template_ref = NONE/null
task_template_hash = NONE/null
```

means:

```text
no separate template provenance is attached
```

not:

```text
template validation passed
template hash equals NONE
arbitrary scope is authorized
```

A source kind that actually depends on an external template must still have genuine owner-enrolled proof. Unsupported non-catalog source kinds remain denied.

No new generic template registry, Markdown resolver, URL resolver or approval database is created.

## 5. authority_refs correction

The durable body retains:

```text
authority_refs
```

as a required field, but the universal two-pair template requirement is removed.

Corrected semantics:

```text
possibly-empty sorted tuple of closed {ref, fingerprint} entries
```

An empty tuple means only:

```text
no ADDITIONAL independent authority ref is required by the applicable owner policy
```

It never means:

```text
no TaskContract authority exists
```

Any supplied/required ref must still verify through its existing semantic owner, scope, schema, fingerprint, certified prefix and currentness. Opaque refs are not reinterpreted as template approval.

## 6. Existing accepted corrections remain unchanged

0812 body identity correction remains:

```text
body_ref =
task-contract-body:v1:sha256:
+ SHA256(JCS(project_id, contract_id, contract_version))
```

0902 Human correction remains:

```text
TaskContract immutable Human configuration
→ existing P1-7 Human owner at runtime
```

0902 Judgment correction remains:

```text
TaskContract immutable Judgment registration configuration
→ existing JudgmentPolicyAuthority at runtime
```

No P1-4, P1-6, P1-7 or P1-8 semantic owner is replaced.

## 7. Proposal identities

0940 correction proposal:

```text
TASKCONTRACT_TEMPLATE_REQUIREMENT_CORRECTION_PROPOSAL.md
SHA-256:
da2bf0d59e148d6359b7e979296a7d63b01307f0500df6c2e715937527edd951
```

Supporting audit:

```text
TEMPLATE_AUTHORITY_CANONICAL_AUDIT.md
SHA-256:
2889d21300126671ee1e1b3ecc3acf3b1a96358b1e26c81e253e94413b4f5f85

P1_8_DESCRIPTOR_TEMPLATE_SEMANTICS_AUDIT.md
SHA-256:
609d6c085b7edd2a79bbf8afd0e2461ec1919642cfdb33e333bea5c64676668c

OWNER_NON_SUBSTITUTION_PROOF.md
SHA-256:
3ba78e965f88749d6805268d049154366f7bbcee1c1d77697393230c7e6aff23

BASELINE_SUPERSESSION_DELTA.md
SHA-256:
20f050403f50f9edaa9c445ba049135da896b52cc31dadf03a7912dde34d7e69

IMPLEMENTATION_IMPACT_ALLOWLIST.md
SHA-256:
cf5a4cc5932d4ebaec1d84376bfbaff7a9c7d93cfba5379f883ebd94d3766080
```

## 8. Browser assessment

The proposal is suitable for Human approval because:

1. it removes an authority requirement that current catalog descriptors do not universally possess;
2. it does not turn template absence into authority;
3. it preserves deterministic P1-8 selection/currentness and exact external issuance ownership;
4. it requires explicit complete-body authorization rather than deriving a work contract from a descriptor;
5. it preserves unsupported-source denial and owner non-substitution;
6. it requires no new template registry/table/source-kind extension for the current P2-4 path;
7. it does not weaken the already accepted 0812 or 0902 corrections.

Browser recommendation:

```text
ACCEPT
```

Human acceptance here approves the design correction only.

It does not itself authorize or accept runtime behavior until the next implementation Task produces the required source, PostgreSQL and regression evidence.

## 9. Human decision requested

Choose exactly one:

```text
ACCEPT
REWORK
REJECT
```

If `ACCEPT`, Browser Command Center should reissue the bounded durable TaskContract implementation cut using the full accepted chain:

```text
0319 base durable-body design
+ 0812 body_ref correction
+ 0902 Human/Judgment binding correction
+ 0940 template/approval authority correction
```

No further design task is required unless actual implementation exposes a new exact owner conflict.
