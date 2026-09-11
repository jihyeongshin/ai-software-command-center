# AISCC Command Center Judgment

## meta

- judgment_id: `20260910_2215_aiscc-p2-3-a2-security-clock-domain-test-failure-judgment-1`
- created_at: `2026-09-10T22:15:00+09:00`
- project: `AI Software Command Center (AISCC)`
- submitted_task: `.aiassistant/tasks/done/20260910_1948_aiscc-p2-3-a2-production-integration-static-and-runtime-evidence-binding-rework-1.md`
- submitted_bundle: `20260910_1948_aiscc-p2-3-a2-production-integration-static-and-runtime-evidence-binding-rework-1.zip`
- submitted_bundle_sha256: `918e7784f198de75a6b2cdc6178839cc73485decbd00c3f52b09bee25d867838`
- result_status: `HOLD_REWORK_REQUIRED`
- blocker: `TEST_FAILURE`
- root_cause: `SECURITY_TTL_CLOCK_DOMAIN_MISMATCH`
- runtime_evidence_binding: `VERIFIED_CANDIDATE`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`

# 판정

`1948` transport/export/static evidence is valid and the mandatory test STOP is conformant.

Direct Browser verification:

```text
ZIP readability / CRC:
PASS

top-level:
1 exact

members:
23 exact

required root docs:
14 / 14

canonical/source copies:
9 / 9

manifest non-self:
22 / 22 SHA-256 + byte-size PASS

issued 1948 TASK/CYCLE/JUDGMENT:
3 / 3 exact
```

Submitted ZIP:

```text
SHA-256:
918e7784f198de75a6b2cdc6178839cc73485decbd00c3f52b09bee25d867838
```

# executed result

```text
compile:
5 / 5 PASS

Ruff:
5-path set PASS

strict JSON:
3 / 3 PASS

git diff --check:
PASS

migration:
20260901_0008 PASS

PostgreSQL:
17.6 disposable / migration PASS

A2 integration:
1 PASS / 1 FAIL / 0 skip

failed test:
test_production_owner_graph_and_bounded_running_prefix

failure point:
authorize_runtime
expected ADMITTED
actual DENIED

A1/B3 regression:
NOT_RUN after mandatory stop

direct-owner regressions:
NOT_RUN after mandatory stop
```

The Task-owned PostgreSQL container was removed.

# accepted candidate improvement

The runtime-summary evidence binding defect from 1824 is corrected at candidate level.

The current candidate now requires:

```text
current execution submission
same-attempt AgentOutputRef
same-attempt ToolOutputRef
P1-5 verification of both output refs
ToolOutputRef hash == canonical_sha256(STOCKROOM_SUMMARY)
```

and uses the authentic ToolOutputRef as runtime observation producer provenance.

The pure binding regression passed.

This remains candidate evidence until the full A2 chain completes.

# Browser independent root-cause review

The production test supplies this application clock:

```text
2026-09-10T09:24:00Z
```

Current adapter `_issue_capability` passes that clock to:

```text
SecurityPolicy.issue_resource_grant(... now=self._app.clock())
```

`SecurityPolicy.issue_resource_grant` gives the grant a 30-second TTL relative to the supplied timestamp.

But `SecurityPolicy.evaluate(request)` has no injected `now` argument and its resource-grant validity path evaluates against the SecurityPolicy wall clock.

Therefore, when the test runs later than:

```text
2026-09-10T09:24:30Z
```

the freshly constructed grant is already expired from the evaluator's clock domain and:

```text
SG_EXACT_RESOURCE_GRANT
→ false
→ EXACT_RESOURCE_GRANT_DENIED
```

is the expected fail-closed result.

The same adapter also passes the historical application clock to:

```text
SecurityPolicy.issue_capability(... now=self._app.clock())
```

which would produce an immediately stale capability even if admission succeeded.

This is not evidence that the Stockroom security policy should be weakened.

It is an A2 composition clock-domain error.

# required correction

Do not modify P1-3 `SecurityPolicy`.

Keep durable/application timestamps on the injected application clock where current owners require them.

For TTL-bearing `SecurityPolicy` grant/capability lifecycle in the A2 adapter, use the SecurityPolicy's native clock domain consistently.

Under the current API, the minimal correction is to stop passing the application/durable clock into:

```text
_issue_capability:
SecurityPolicy.issue_resource_grant
SecurityPolicy.issue_capability
```

and the analogous denied NETWORK grant probe.

Let those methods use their native default wall clock, matching `SecurityPolicy.evaluate`.

Do not replace the security decision with a test bypass or preissued fake capability.

# regression requirement

Keep the integration test's historical application clock.

That is intentional regression pressure.

After correction, the test must prove:

```text
historical durable/application clock
does not create already-expired P1-3 security grants/capabilities

repository authorization:
ALLOW

filesystem authorization:
ALLOW

NETWORK grant:
absent

state/version:
RUNNING / 2
```

No materialization/provider/tool/process edge may execute.

# exact rework scope

```text
MODIFY:
src/aiscc/scenarios/stockroom_production.py
tests/integration/scenarios/test_stockroom_capture_runner.py

FROZEN:
src/aiscc/bootstrap.py
all three Stockroom capture config files
accepted A1 runner/driver/test
all P1-3 security source
all migrations
```

# phase state

```text
P2-3 A1:
ACCEPTED / CLOSED / PERSISTED

A2 feasibility:
ACCEPTED / COMPLETE

A2 implementation:
REWORK_REQUIRED

runtime-summary evidence binding:
VERIFIED_CANDIDATE

A2 PostgreSQL proof:
PARTIAL / TEST_FAILURE

Stockroom runtime prerequisites:
NOT_VERIFIED

actual S1-S4:
NOT_STARTED
```

# session

Same A2 implementation authority:

```text
fresh IDE Executor chat:
NOT_REQUIRED

Browser:
CONTINUE_CURRENT_BROWSER_SESSION

Handoff:
NOT_REQUIRED
```
