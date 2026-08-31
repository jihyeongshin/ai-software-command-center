# 작업지시서: P1-8 NEXT_ACTION_CONTEXT Ranking Authority Compatibility Design Rework

## meta

- task_id: `20260831_1514_aiscc-p1-8-next-action-context-ranking-authority-compatibility-design-rework-1`
- phase: `P1-8 NEXT_ACTION_CONTEXT Source Authority Design`
- work_type: `DESIGN_REWORK`
- expected_start_head: `f4614198c2745944f7ec02639a45b0315bbc903d`
- predecessor_design_path: `.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md`
- predecessor_design_sha256: `7dd7274f96d6565233c65f8ade5e81acd8b53f9d7425e377df148d5337d8f4e6`
- accepted_p1_8_design_sha256: `100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a`
- blocked_runtime_path_count: `19`
- blocked_runtime_aggregate_sha256: `84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42`
- runtime_implementation: `FORBIDDEN`

## 1. purpose

Rework the same candidate source-authority rule so it is fully compatible with the already Human-accepted P1-8
ranking authority.

Do not redesign P1-8.

Do not modify runtime source/tests/migrations.

Place/preserve:

```text
.aiassistant/records/aiscc/cycles/
20260831_1514_aiscc-p1-8-next-action-context-ranking-authority-compatibility-hold-1.cycle.md
```

## 2. preflight

Require exact:

```text
HEAD:
f4614198c2745944f7ec02639a45b0315bbc903d

predecessor source-authority design:
7dd7274f96d6565233c65f8ade5e81acd8b53f9d7425e377df148d5337d8f4e6

accepted P1-8 design:
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a

blocked runtime:
19 paths /
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

Index empty.

No Git add/commit/push.

## 3. preserve the external source owner contract

Keep unless required by exact compatibility:

```text
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY /
NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY_V1

NextActionContextRefV1

TaskContract-only V1 scope

owner event model

private capability boundary

closed P1-6 carrier schema

prospective P1-6 V2 durable enrollment

P1-6 Requirement identity sufficiency decision

owner-derived Memory lineage

no legacy/backfill authority laundering
```

## 4. restore accepted ranking authority semantics

Normative accepted P1-8 rule:

```text
CURRENT ProjectMemoryEntry
→ CYCLE_DERIVED eligibility/context input

CURRENT ProjectMemoryEntry
!= priority authority by itself
```

Authoritative ranking inputs remain:

```text
versioned eligibility/selection policy mapping

exact enrolled canonical priority source ref/hash/ordinal

current P1-4/P1-7 source facts when mode requires them
```

Preserve conceptual ranking tuple:

```text
(
  authoritative_priority_rank,
  policy_dependency_ordinal,
  enrolled_critical_path_ordinal,
  descriptor_policy_ordinal,
  ActionRef lexical,
  proposal_id lexical
)
```

Do not replace it with a new source-memory ranking tuple.

## 5. exact role of NextActionContextRefV1

Freeze one exact compatible role.

Preferred:

```text
NextActionContextRefV1
→ external canonical priority/context source

P1-8 Memory
→ carries/verifies contextual relation to that source

eligibility/selection policy or descriptor
→ explicitly enrolls the exact context ref/fingerprint/source-contract fingerprint
   as priority_classification_source
```

New selection must require BOTH:

```text
A. exact CURRENT NEXT_ACTION_CONTEXT ProjectMemoryEntry

B. exact current enrolled external NextActionContextRefV1 priority source
```

The Memory entry may repeat `priority_class` and `critical_path_ordinal` for deterministic contextual equality,
but ranking must independently resolve the enrolled external source and verify equality.

If the exact context ref is not enrolled by the active policy/descriptor:

```text
NEXT_ACTION_PRIORITY_SOURCE_NOT_ENROLLED
```

or the accepted existing typed equivalent.

## 6. priority class mapping

The external owner may own:

```text
ACCEPTED_CORE_CRITICAL_PATH
OPERATIONAL_HARDENING
OPTIONAL_OPTIMIZATION
```

and their exact canonical critical-path ordinal.

But selection policy maps these owner classes to ranks:

```text
ACCEPTED_CORE_CRITICAL_PATH → 4
OPERATIONAL_HARDENING → 5
OPTIONAL_OPTIMIZATION → 6
```

Therefore:

```text
external source owns classification fact + ordinal
selection policy owns class → rank mapping
```

Do not make the Memory policy itself own either.

## 7. ordinal semantics

Restore the accepted name/meaning:

```text
enrolled_critical_path_ordinal
```

It is obtained by independently resolving the exact enrolled external priority source.

The same value copied into Memory may be equality-checked but is not the authority path.

Do not introduce `source_memory_critical_path_ordinal` as a new authoritative tuple field.

If a descriptor-local catalog tie-break is still needed, it must map to an already accepted descriptor/policy
ordinal field and must not silently add a new ranking dimension.

## 8. CYCLE_DERIVED proof

Freeze exact selection proof:

```text
1. verify ProjectMemoryEntry is CURRENT at selection high-watermark
2. verify entry is NEXT_ACTION_CONTEXT and same project/scope
3. extract its external context_ref/fingerprint as contextual source locator
4. verify active eligibility/selection policy or selected descriptor explicitly enrolled that exact source
5. resolve external NextActionContextRefV1 independently
6. verify owner payload/fingerprint/currentness
7. compare Memory contextual copy to external source
8. derive authoritative priority_class and enrolled_critical_path_ordinal from external source
9. map class to rank via selection policy
10. apply accepted ranking tuple
```

Later Memory staleness and later external context staleness withdraw current eligibility separately.

## 9. historical selection replay

Historical replay must verify:

```text
Memory was CURRENT at original selection H

exact original external context source payload/fingerprint

exact original policy/descriptor enrollment of that source

exact source class/ordinal

exact original class→rank mapping

accepted original ranking tuple
```

Later context/policy/Memory staleness is not historical corruption.

## 10. producer H boundary

Correct the current contradiction.

`context_authority_event_high_watermark` in the structured result is the owner snapshot observed when the result
was authored.

It proves:

```text
which exact external owner object/event prefix the producer/result referenced
```

It does NOT by itself prove the context remained current at later:

```text
P1-6 evidence admission
terminal transition
```

Freeze one model.

### Preferred V1

```text
historical semantic result validity
→ exact context object was valid at the body H carried by the immutable result

P1-6 historical authority
→ exact immutable result was admitted and terminal-consumed

external owner events after body H
→ current applicability only
```

Thus if the context is revoked after body generation but before Cycle admission:

```text
AdmittedCycle historical source may remain valid

ProjectMemory initial publication:
non-CURRENT

CYCLE_DERIVED current selection:
not eligible
```

This preserves:

```text
historical provenance != current applicability
```

and avoids inventing a nonexistent terminal cross-owner high-watermark.

### Alternative

If terminal-bound context currentness is required, define a separate immutable terminal observation authority.
Do not derive it from body H or cross-domain timestamps.

Choose exactly one; do not leave both.

## 11. update source contract/schema hashes

If the carrier or source contract semantics change, recompute all affected canonical hashes.

At minimum independently recompute:

```text
source contract
context ref schema if changed
event schema if changed
result schema if changed
Memory derivation contract
```

Do not retain hashes over obsolete semantic payloads.

## 12. relation to prerequisite catalog

This source-authority design must not itself mutate:

```text
P1_8_POLICY_ACTION_CATALOG_V1
NextActionSelectionPolicy
```

But it must state the exact incorporation requirement:

```text
later prerequisite design
→ descriptor/policy priority_classification_source_ref/hash
   must enroll NextActionContextRefV1 or exact allowed source-contract instance
→ recompute descriptor/policy/catalog fingerprints
```

No runtime resume until that incorporation is Human-accepted.

## 13. exact questions

Reworked candidate/report must answer:

1. Is ProjectMemory a priority authority? (`NO`)
2. What exact object is the priority classification source?
3. Who enrolls that source into eligibility/selection authority?
4. How is source enrollment bound to the selected ActionRef/descriptor?
5. What is the exact class→rank owner?
6. What exact value is `enrolled_critical_path_ordinal`?
7. Is any descriptor-local ordinal an additional ranking dimension?
8. What does CURRENT ProjectMemory prove versus external source enrollment?
9. What exact historical selection replay graph proves the original rank?
10. What exact boundary does the carrier's owner-event H prove?
11. Is external context currentness at terminal required or only current applicability later?
12. Which canonical fingerprints changed?
13. Does P1-6 Requirement identity remain unchanged?
14. Are any Human-owned semantic choices still open?

No implicit answer.

## 14. output

Update the same rule:

```text
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md
```

Successful submission:

```text
NEXT_ACTION_CONTEXT source authority design
→ CANDIDATE / HUMAN_REVIEW_REQUIRED

P1-8 prerequisite owner-authority design
→ BLOCKED until source contract is accepted/incorporated

P1-8 Runtime
→ BLOCKED_REQUIRED_EVIDENCE
```

## 15. Git/runtime policy

```text
NO runtime source/test/migration changes
NO git add
NO commit
NO push

final HEAD:
f4614198c2745944f7ec02639a45b0315bbc903d
```

Human review remains pending.
