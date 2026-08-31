# P1-8 NEXT_ACTION_CONTEXT Accepted — Prerequisite Design Resume Handoff

## terminal status

```text
P1-8 NEXT_ACTION_CONTEXT Source Authority Design:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1-8 prerequisite owner-authority design:
BLOCKED_REQUIRED_EVIDENCE

P1-8 Runtime:
BLOCKED_REQUIRED_EVIDENCE

P2/P3:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

This handoff authorizes only a fresh prerequisite owner-authority exact-contract design Task. It does not authorize
runtime implementation or resume.

## accepted lineage

Human acceptance text:

```text
Human P1-8 NEXT_ACTION_CONTEXT source authority design final review
판정: ACCEPTED
```

Accepted source-authority design:

```text
path:
.aiassistant/rules/AISCC_NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY.md

SHA-256:
19b1d29a8f77ca5cc480a14bc9d1bdd53206951ccf8b34802316f1280dc61cb1

Commit A:
35901125cc5842734cf1e8eb3374d10e4ee866e3
```

Accepted parent P1-8 design:

```text
.aiassistant/rules/AISCC_PROJECT_MEMORY_CYCLE_ADMISSION.md
100fd21b4095b8e5df60e4073fe5e7f69fe3cc275da937161f0b9ce7e90a995a
```

Terminal acceptance Cycle:

```text
.aiassistant/records/aiscc/cycles/20260831_1619_aiscc-p1-8-next-action-context-source-authority-final-acceptance-1.cycle.md
```

## exact accepted semantics

1. Semantic owner is `EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY / NEXT_ACTION_CONTEXT_SOURCE_AUTHORITY_V1`.
2. P1-6 owns durable bytes, schema binding, admission and terminal-consumed provenance only; it does not own priority semantics.
3. `CURRENT ProjectMemoryEntry` is mandatory contextual/eligibility input and is not priority authority.
4. The exact externally enrolled `NextActionContextRefV1` owns priority classification and canonical ordinal.
5. `P1_8_NEXT_ACTION_SELECTION_POLICY_AUTHORITY_V1` owns class-to-rank mapping.
6. The accepted ranking tuple is unchanged:

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

7. Carrier owner-event H is `AUTHORING_SNAPSHOT_PROVENANCE_ONLY`; it does not prove later evidence admission or terminal currentness.
8. Terminal external-context currentness is `NOT_REQUIRED_V1`; later owner events change current applicability without rewriting historical identity.
9. `historical provenance != current applicability`.
10. P1-6 Requirement fingerprint-schema extension is `NOT_REQUIRED` for this V1 cross-owner contract.

## preserved blocked candidates

Blocked P1-8 runtime:

```text
19 source/test/migration paths
aggregate SHA-256:
84641ac35f7384e18faa086be249c36094eed1e4650550c6607ba0c57d1cfd42
```

The runtime bytes are reviewed but unaccepted and uncommitted. Do not modify, stage or infer runtime-resume authority
from this handoff.

Unaccepted prerequisite candidate:

```text
.aiassistant/rules/AISCC_P1_8_PREREQUISITE_OWNER_AUTHORITY.md
SHA-256:
556faad8a77d917fcbfc9ab7b0ba62bd65f985a6f4a1e585c08af668dd14393c
```

It is a candidate input, not accepted authority. A new exact-contract rework must incorporate the accepted source
contract without silently treating the old candidate as accepted.

## exact next-action scope

Resume prerequisite owner-authority design only:

1. Freeze `TaskConstraint` scope-specific cardinality and immutable `ISSUED/SUPERSEDED/REVOKED` event/currentness fold.
2. Freeze P1-4 blocker taxonomy, reason-specific resumability and exact durable `G_BLOCKER_RESOLVED` owner binding.
3. Incorporate exact accepted `NextActionContextRefV1` ref/hash/source-contract enrollment into `P1_8_POLICY_ACTION_CATALOG_V1`, affected descriptors and selection-policy authority.
4. Preserve CURRENT ProjectMemory as contextual/eligibility input only.
5. Preserve the accepted ranking tuple and selection-policy-owned class-to-rank mapping.
6. Recompute every affected catalog, descriptor and policy canonical fingerprint.
7. Obtain separate Human acceptance before any owner runtime or P1-8 runtime resume.

## prohibitions

- do not alter P1-4/P1-6/P1-7 accepted authority semantics;
- do not make caller/configuration/Memory/proposal priority authority;
- do not stage or commit the blocked runtime candidate under a design Task;
- do not mark P1-8 Runtime implemented, accepted or resume-authorized;
- do not start P2/P3, deployment or Public Live.
