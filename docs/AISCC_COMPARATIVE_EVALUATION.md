# AISCC Comparative Evaluation

## Question

P3-1 asked whether explicit governance authority, evidence admission, and deterministic state ownership produced better truthfulness, auditability, and failure behavior than an agent/executor workflow without those controls. The study was an offline interpretation of frozen artifacts. It did not compare code generation, live runtime performance, or products in the market.

## Frozen comparators

The accepted protocol fixed two logical views of the same source packet before scoring:

- **`AISCC_GOVERNED`** could use accepted TaskContract scope, evidence admission, System transition, Judgment, Cycle, and Next Action records.
- **`EXECUTOR_REPORT_BASELINE`** acted as a conservative ordinary report reader. It retained the Task, output, caveats, and candidate artifacts, while governance admissions and System-owned decisions remained reference-only for its completion decision.

```text
SYNTHETIC_ABLATION_ONLY
NOT_A_COMPETITOR_PRODUCT
```

The baseline was not a commercial product, vendor system, or industry benchmark. Either arm could pass, fail, tie, or abstain under the same frozen metric rules.

## Matched condition

An eligible pair required the same Task or scenario input, executor-produced attempt/output, candidate artifacts, and source/version identity. Only the governance interpretation and admission path could differ. A Replay summary, later report, or current source could not replace missing same-attempt material.

## Planned five-row matrix

| Row | Planned class | Terminal eligibility |
| --- | --- | --- |
| M01 | valid evidence / accepted | `EX_SOURCE_MISSING / NOT_COMPARABLE` |
| M02 | missing evidence / rework | `EX_SOURCE_MISSING / NOT_COMPARABLE` |
| M03 | policy conflict / blocked | `EX_SOURCE_MISSING / NOT_COMPARABLE` |
| M04 | Human-owned claim / Human pending | `EX_SOURCE_MISSING / NOT_COMPARABLE` |
| M05 | bounded self-use document change | `ELIGIBLE / EVALUATED / HUMAN_ACCEPTED` |

M01-M04 lacked the complete original same-attempt Task/output packet required by the frozen matched-condition rule. They remained visible in the matrix but were excluded before scoring. They are not PASS, FAIL, N/A, or negative governance samples.

## M05 source identity

M05 used the accepted P2-4 self-use packet for a single exact document change. At a public-safe level, its immutable anchors are:

- scenario: `aiscc-p2-4-golden-cycle-3@v1`;
- WorkRun: `aiscc-p2-4-golden-workrun-3`;
- result commit: `ea34a0e08912d6259c74d0cb50ade9c9b9dba77e`;
- governed artifact: `docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md`;
- artifact SHA-256: `7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368`;
- golden provenance root: `b0be0299344375a74d9b9bdc7e7149aa949d98098e0a76bf9f81b13e86834e50`.

Both comparator arms interpreted this same frozen packet.

## M05 comparator decisions

| Arm | Decision | Reason at the accepted scope |
| --- | --- | --- |
| `AISCC_GOVERNED` | `ACCEPTED` | The admitted evidence, deterministic accepted Judgment, System transition, accepted WorkRun, Cycle, result commit, and Next Action resolved as one linked chain. |
| `EXECUTOR_REPORT_BASELINE` | `UNRESOLVED` | Mechanical deliverable checks were present, but the ordinary report view lacked same-attempt support for the first unresolved non-mechanical Task constraint and could not use governance admissions to fill it. |

`UNRESOLVED` is a conservative abstention, not a recorded unsafe action.

## Primary metrics

| Metric | `AISCC_GOVERNED` | `EXECUTOR_REPORT_BASELINE` |
| --- | ---: | ---: |
| Truthful terminal outcome | PASS | PASS |
| Evidence integrity | PASS | PASS |
| Authority separation | PASS | PASS |
| Fail-closed behavior | N/A | N/A |
| Audit reconstructability | 10/10 | 5/10 |

Fail-closed behavior was structurally inapplicable because the eligible packet did not demonstrate the underlying challenge required by that metric. The three binary primary metrics tied. Audit reconstructability differed under the protocol's fixed field rubric.

## Secondary results

| Metric | `AISCC_GOVERNED` | `EXECUTOR_REPORT_BASELINE` |
| --- | ---: | ---: |
| Restart recoverability | PASS | FAIL |
| Historical truth preservation | PASS | PASS |
| Deterministic projection | PASS | PASS |
| Governance overhead | descriptive only | descriptive only |
| Runtime latency | NOT_COMPARABLE | NOT_COMPARABLE |
| Cost | NOT_COMPARABLE | NOT_COMPARABLE |
| Operator burden | NOT_COMPARABLE | NOT_COMPARABLE |

Restart recoverability was an offline artifact-reconstruction measure. No process or database restart was executed or implied.

## Trace-derived artifact-count correction

The accepted trace-conformance rework derived governance-overhead counts from distinct immutable artifact identities instead of hard-coded values:

| Arm | Total consulted | Decision input | Reference-only |
| --- | ---: | ---: | ---: |
| `AISCC_GOVERNED` | 14 | 11 | 3 |
| `EXECUTOR_REPORT_BASELINE` | 14 | 4 | 10 |

The correction separately counted two frozen acceptance anchors. Comparator decisions and semantic metric values did not change. These counts are descriptive; they do not measure runtime, cost, or operator effort.

## Deterministic reproducibility

The evaluator recorded every source field it read with an immutable artifact identity, SHA-256, JSON pointer or text span, role, and rule/metric use. All source-dependent steps had nonempty, mechanically resolvable references. Both logical projections regenerated identically from the same frozen packet, and the trace/source-manifest and metric provenance resolved mechanically.

This establishes deterministic offline reconstruction for M05. It is not independent external validation or a repeated runtime experiment.

## Limitation and confidence boundary

The corpus was small, purposive, and self-produced. There was no randomization, competitor execution, independent product sample, counterfactual run, population inference, or like-for-like runtime/cost/operator-effort measurement. Four requested classes were source-excluded, leaving a single eligible attempt.

```text
materially_better_condition_possible = No
```

The frozen protocol required a strict favorable direction in at least two distinct eligible attempts spanning at least two requested classes, with no opposing primary regression. M05 was the single eligible attempt, so that publication condition could not be met regardless of its metric values.

## Admitted public conclusion

> One eligible bounded artifact-interpretation comparison was completed. Four planned rows were source-excluded. The eligible corpus is insufficient for the frozen protocol's stronger directional claim.

## Prohibited inference

This result does not establish:

- AISCC or competitor-product superiority;
- generalized safety, accuracy, or productivity improvement;
- lower runtime, cost, or operator burden;
- generalization across repositories, providers, models, languages, or teams;
- novelty or exclusive invention of governance primitives;
- independent validation;
- availability of a deployed public Replay or Live service.

## Canonical provenance

- [Accepted comparative protocol](../.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md), SHA-256 `a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6`
- [P3-1 terminal acceptance Cycle](../.aiassistant/records/aiscc/cycles/20260915_0310_aiscc-p3-1-comparative-evaluation-final-acceptance-p3-2-entry-authorization-1.cycle.md)
- [P3-1 Human acceptance Judgment](../.aiassistant/reports/aiscc/20260915_0310_aiscc-p3-1-comparative-evaluation-final-human-acceptance-browser-judgment-1.md)
- [Public documentation truth map](../.aiassistant/reports/aiscc/AISCC_PUBLIC_DOCUMENTATION_TRUTH_MAP.md)
- [Bounded self-use artifact](AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md)

The corrected result submission ZIP accepted by the terminal Cycle has SHA-256 `2827c3b0a302caff4971090347134d3f9e37ab0e8d6cf5be4eae0fe706d42e48`. The ZIP is review provenance rather than a public repository link.
