# AI Software Command Center

AISCC is a software engineering governance control plane for AI-assisted work. It places coding-agent output inside an inspectable chain of Task scope, evidence admission, system-owned state transitions, Judgment, curated Cycle provenance, and Next Action. The aim is to help a software owner distinguish what an Agent proposed, what the System admitted, and what a Human actually decided.

> **Current public status:** the repository contains implemented governance source and accepted bounded evidence, including a recorded self-use lineage and a small comparative evaluation. Public Replay deployment is **not completed**, Public Bounded Live is **not released**, and competition submission is **not completed**.

## Why this exists

Strong code generation does not by itself settle project governance. In a long-running project, authority can drift between prompts, Tasks, policy documents, source versions, and review decisions. A completion claim can be mistaken for accepted evidence; one proof type can be substituted for another; Human-owned checks can be reported as complete by the wrong actor; and raw chat history can blur failed attempts with accepted project memory.

AISCC makes those boundaries explicit. Its product hypothesis is that task-scoped evidence ownership, proof non-substitution, system-owned transition admission, Human-owned gates, and curated Cycle memory are more useful when connected as one reviewable chain.

## Governance chain

```text
Task
→ Evidence candidate
→ Evidence admission
→ Judgment
→ System transition admission
→ Curated Cycle
→ Next Action
```

A `TaskContract` fixes the goal, scope, forbidden work, evidence ownership, and stop conditions. An Agent or Executor can produce work and evidence candidates. Applicable authorities decide whether evidence is admitted and whether a transition is allowed. A `Judgment` records the semantic outcome without directly mutating workflow state. A `Cycle` preserves selected durable provenance and supports a stable next action.

The detailed domain and transition contracts are in [AISCC Architecture](.aiassistant/rules/AISCC_ARCHITECTURE.md) and [AISCC Orchestration](.aiassistant/rules/AISCC_ORCHESTRATION.md).

## Authority model

| Actor | Owns | Does not own |
| --- | --- | --- |
| Agent / Executor | reasoning, proposed changes, execution output, evidence candidates | authoritative workflow state, evidence admission, Human verification, terminal transition |
| AISCC System | state/version, transition evaluation and admission, evidence compatibility checks, durable gate projection | policy exceptions or Human acceptance |
| Human / Command Center | policy choices, designated verification, exceptional approval, business judgment, final public positioning | automatic promotion of unsupported output into project truth |

The core boundaries are:

```text
Agent output != System state
Evidence candidate != Admitted evidence
Human result != Judgment
Judgment != Transition decision
Recorded artifact != Released public service
```

## What is implemented and evidenced

- The explicit governance model separates `WorkflowState`, execution status, Human-gate status, Judgment status, and runtime mode.
- The accepted project corpus contains durable Task, evidence, transition, Judgment, Cycle, and Next Action provenance for bounded workflows.
- P2 produced a canonical, persisted, sanitized four-member Recorded Replay corpus. These are repository records of previous workflows.
- P2-4 completed an accepted local self-use lineage with an exact result commit and Cycle-derived continuation.
- P3-1 completed and received Human acceptance for one eligible offline artifact-interpretation comparison under a frozen protocol.

These statements describe repository implementation and accepted bounded evidence. They do not establish general reliability, complete security, independent validation, or public-service availability. The claim-level sources and limits are recorded in the [Public Documentation Truth Map](.aiassistant/reports/aiscc/AISCC_PUBLIC_DOCUMENTATION_TRUTH_MAP.md).

## Self-Dogfooding

The accepted self-use lineage followed this owner chain:

```text
SELF_DOGFOOD_GENESIS
→ TaskContract
→ SelfDogfoodTaskSpec
→ READY
→ RUNNING
→ exact governed edit
→ authenticated external submission
→ admitted evidence / SATISFIED
→ deterministic Judgment ACCEPTED
→ WorkRun ACCEPTED
→ Cycle
→ result Git commit
→ CYCLE_DERIVED Next Action
```

The bounded result commit is `ea34a0e08912d6259c74d0cb50ade9c9b9dba77e`, and its provenance root is `b0be0299344375a74d9b9bdc7e7149aa949d98098e0a76bf9f81b13e86834e50`. The governed document is preserved as [AISCC Self-Dogfood Golden Cycle](docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md); that document explicitly does not substitute for the owner-chain provenance.

This run shows bounded actual use and a linked Task-to-Cycle record. It does not show novelty, product superiority, independent validation, broad reliability, or security completeness.

## Comparative evaluation

P3-1 compared two interpretations of the same frozen M05 packet:

- `AISCC_GOVERNED`, using admitted governance records;
- `EXECUTOR_REPORT_BASELINE`, a conservative ordinary report reader that could not use governance records to derive its decision.

This was `SYNTHETIC_ABLATION_ONLY`, not a competitor-product benchmark. In M05 the governed arm resolved to `ACCEPTED` and the baseline to `UNRESOLVED`. Several metrics tied; audit reconstructability was 10/10 versus 5/10, and restart recoverability was PASS versus FAIL. M01-M04 remained `EX_SOURCE_MISSING / NOT_COMPARABLE` and were not scored.

Only one planned row was eligible. Therefore `materially_better_condition_possible = No`. See the [public comparative evaluation summary](docs/AISCC_COMPARATIVE_EVALUATION.md) and the [accepted frozen protocol](.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md).

## Recorded Replay vs Bounded Live

| Surface | Meaning | Current status |
| --- | --- | --- |
| Recorded Replay corpus | Sanitized, read-only records of previously executed workflows | `CANONICAL / PERSISTED` in this repository |
| Public Replay deployment | A publicly hosted viewer for admitted Replay artifacts | `NOT_COMPLETED` |
| Public Bounded Live | Optional real-time execution using a fixed synthetic repository and allowlisted scenarios | `NOT_RELEASED` |

Reading a Replay artifact performs no current model inference and is not Live execution. The intended public policy forbids free-form tasks, external repository URLs or uploads, arbitrary shell or network access, public credential selection, and owner/private data. See the [Competition Public Runtime Boundary](.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md) and [Security Sandbox policy](.aiassistant/rules/AISCC_SECURITY_SANDBOX.md).

## Repository evidence / provenance map

| Question | Repository source |
| --- | --- |
| What is the product thesis? | [AISCC Product Thesis](.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md) |
| What claims are limited by prior art? | [AISCC Prior-Art Boundary](.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md) |
| Who owns state, evidence, Judgment, and Cycle semantics? | [Architecture](.aiassistant/rules/AISCC_ARCHITECTURE.md) and [Orchestration](.aiassistant/rules/AISCC_ORCHESTRATION.md) |
| What is the current accepted P3-1 result? | [P3-1 terminal Cycle](.aiassistant/records/aiscc/cycles/20260915_0310_aiscc-p3-1-comparative-evaluation-final-acceptance-p3-2-entry-authorization-1.cycle.md) and [Human acceptance Judgment](.aiassistant/reports/aiscc/20260915_0310_aiscc-p3-1-comparative-evaluation-final-human-acceptance-browser-judgment-1.md) |
| Which public statements are admitted? | [Public Documentation Truth Map](.aiassistant/reports/aiscc/AISCC_PUBLIC_DOCUMENTATION_TRUTH_MAP.md) |
| What did the bounded comparison show? | [Comparative Evaluation Summary](docs/AISCC_COMPARATIVE_EVALUATION.md) |

## Current limitations

- The comparative corpus has one eligible row; four planned rows lack the required matched packets.
- Runtime latency, cost, and operator burden were `NOT_COMPARABLE`.
- The self-use evidence is produced within the project and is not independent validation.
- The repository's Recorded Replay corpus is not a deployed public Replay service.
- Public Bounded Live, public deployment, release verification, and competition submission remain future work.
- Public/local quick-start documentation is pending a P3-2 follow-up; this baseline does not guess at startup commands that were outside its verified scope.

## Claim boundary

AISCC acknowledges overlap with existing work in specification workflows, agent orchestration, evidence gates, permission and Human review, persistent memory, reviewer systems, and provenance. It does not claim invention of those primitives. The current product hypothesis is their integration into one inspectable governance chain and the use of that chain on AISCC's own development.

The current evidence does not support claims of AISCC or competitor superiority, broad safety or accuracy improvement, productivity or cost advantage, reduced operator burden, generalization across repositories/providers/languages, or independent validation.

## Project / competition status

- P2 implementation and bounded self-use: `ACCEPTED / CLOSED`
- P3-1 comparative evaluation: `HUMAN_PROVIDED / ACCEPTED / CLOSED`
- P3-2 public documentation: `DOCUMENTATION_CANDIDATE / HUMAN_PENDING`
- P3-3 public release and competition submission: `NOT_STARTED`
- Public Replay deployment: `NOT_COMPLETED`
- Public Bounded Live: `NOT_RELEASED`
- Competition submission: `NOT_COMPLETED`

Final public positioning and readability remain subject to Human review.
