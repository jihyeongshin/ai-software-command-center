# AISCC Command Center Judgment

## meta

- judgment_id: `20260910_1948_aiscc-p2-3-a2-static-failure-runtime-evidence-binding-judgment-1`
- created_at: `2026-09-10T19:48:00+09:00`
- project: `AI Software Command Center (AISCC)`
- submitted_task: `.aiassistant/tasks/done/20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1.md`
- submitted_bundle: `20260910_1824_aiscc-p2-3-a2-production-owner-bootstrap-integration-implementation-1.zip`
- submitted_bundle_sha256: `53fc438c5d8c5c61f8a28cdbe1680a77b03892de60e6f44e94d78d039e47e5a2`
- result_status: `HOLD_REWORK_REQUIRED`
- primary_blocker: `STATIC_CHECK_FAILURE`
- additional_browser_blocker: `RUNTIME_EVIDENCE_PRODUCER_BINDING_MISMATCH`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`

# 판정

Executor의 `STATIC_CHECK_FAILURE` STOP은 conformant하다.

Browser direct bundle verification:

```text
ZIP readability / CRC:
PASS

top-level:
1 exact

members:
22 exact

required root documents:
13 / 13

canonical/source copies:
9 / 9

manifest non-self:
21 / 21 SHA-256 + byte-size PASS

issued 1824 TASK/CYCLE/JUDGMENT:
3 / 3 exact
```

Submitted ZIP:

```text
SHA-256:
53fc438c5d8c5c61f8a28cdbe1680a77b03892de60e6f44e94d78d039e47e5a2
```

# Executor static result

```text
Python compile:
5 / 5 PASS

Ruff:
FAIL / 5 findings

bootstrap.py:
UP037 x3

stockroom_production.py:
I001 x1
E501 x1

strict JSON:
NOT_RUN

git diff --check:
NOT_RUN

PostgreSQL integration:
NOT_RUN

A1/B3 regression:
NOT_RUN

formal contract review:
NOT_RUN
```

No same-turn repair was performed, as required.

# Browser source review — additional blocker

The candidate `submit_runtime_evidence` currently verifies only the final P1-5 `AgentOutputRef` and then constructs a correct-looking evidence body with literal values:

```python
"summary": "P1_5_AGENT_OUTPUT_VERIFIED",
"total_available": 13,
"reorder_rule": "available <= reorder_level",
```

It does **not** require or verify the authentic P1-5 `ToolOutputRef` produced by the Stockroom summary tool.

That is insufficient for a `SYSTEM_RUNTIME_OBSERVATION` requirement.

Current accepted Stockroom tool semantics already provide a stronger source of truth:

```text
StockroomSummaryDispatcher
→ parses actual process stdout
→ requires exact strict JSON
→ requires output == STOCKROOM_SUMMARY
→ returns ToolOutputRef with canonical result_hash
→ P1-5 persists ToolOutputRef
```

Therefore a successful Agent completion/ref alone must not be enough to mint a runtime-summary evidence candidate.

Otherwise the evidence body can look correct even if the runtime/tool lineage needed to justify those values is absent.

This is a proof-source binding defect, not merely formatting.

# required correction

Preserve the six-path A2 boundary, but mutate only:

```text
src/aiscc/bootstrap.py
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py
```

Freeze the three versioned config files byte-exact.

For S1/S4 runtime evidence:

```text
exactly one current ToolOutputRef is required
AND
it belongs to the same attempt
AND
P1-5 output-ref verification passes
AND
its content_hash equals canonical hash of the accepted STOCKROOM_SUMMARY
```

The final AgentOutputRef/ExecutionSubmissionRef may remain additional execution provenance, but may not substitute for the tool-result source.

Only after that exact ToolOutputRef proof may the server-owned runtime observation body derive the Stockroom summary values.

Missing / duplicate / wrong-kind / wrong-hash ToolOutputRef:

```text
fail closed
no EvidenceAdmissionService.submit_durable
no admitted evidence ref
```

The `producer_attestation_ref` for the runtime summary must bind to the authentic tool-output provenance, not only the final AgentOutputRef.

# source review boundaries retained

The following candidate directions remain acceptable pending executable proof:

```text
thin bootstrap
Stockroom-specific production composition module
shared PostgreSQL session factory
real WorkflowKernel transition ownership
P1-6 evidence owner
P1-7 Human owner
P1-7 Judgment owner
Stockroom security owner
three strict versioned enrollment configs
no A1 runner/driver changes
```

# phase state

```text
P2-3 A1:
ACCEPTED / CLOSED / PERSISTED

A2 feasibility:
ACCEPTED / COMPLETE

A2 implementation:
REWORK_REQUIRED

PostgreSQL A2 proof:
NOT_RUN

Stockroom runtime prerequisites:
NOT_VERIFIED

actual S1-S4:
NOT_STARTED
```

# successor session

Same A2 implementation authority.

```text
fresh IDE Executor chat:
NOT_REQUIRED

Browser:
CONTINUE_CURRENT_BROWSER_SESSION

Handoff:
NOT_REQUIRED
```
