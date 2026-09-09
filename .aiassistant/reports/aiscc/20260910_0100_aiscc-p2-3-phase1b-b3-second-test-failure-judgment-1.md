# AISCC Command Center Judgment

## meta

- judgment_id: `20260910_0100_aiscc-p2-3-phase1b-b3-second-test-failure-judgment-1`
- created_at: `2026-09-10T01:00:00+09:00`
- project: `AI Software Command Center (AISCC)`
- submitted_task: `.aiassistant/tasks/done/20260910_0020_aiscc-p2-3-phase1b-b3-candidate-fingerprint-zero-side-effect-rework-1.md`
- submitted_bundle: `20260910_0020_aiscc-p2-3-phase1b-b3-candidate-fingerprint-zero-side-effect-rework-1.zip`
- submitted_bundle_sha256: `400d80ca7a77363ab9c70316dfd2389b6c438c6efff25ddcfa1329a1f016d194`
- result_status: `HOLD_REWORK_REQUIRED`
- blocker: `TEST_FAILURE`
- root_cause: `STRICT_CANONICAL_JSON_TOOL_PAYLOAD_NOT_NORMALIZED`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`

# 판정

`0020` Executor의 mandatory STOP은 적합하다.

Browser Command Center direct bundle verification:

```text
ZIP readability / CRC:
PASS

top-level bundle:
1 exact

bundle members:
35

submitted ZIP SHA-256:
400d80ca7a77363ab9c70316dfd2389b6c438c6efff25ddcfa1329a1f016d194

issued 0020 TASK/CYCLE/JUDGMENT:
3 / 3 exact

authorized two-file rework:
exact

other product/config/test delta:
0

index:
empty

Git add/commit/push:
NOT_RUN
```

Static checks succeeded:

```text
Python compile:
5 / 5 PASS

Ruff:
5 / 5 PASS

git diff --check:
PASS
```

Mandatory B3 test result:

```text
12 failed
6 passed
0 errors
0 skipped
exit 1
```

All displayed failures again terminate in:

```text
build_stockroom_owner_composition
→ STOCKROOM_COMPOSITION_BINDING_DENIED
```

Per Task contract, no same-turn second repair, B2 regression, or bootstrap regression run was performed.

# admitted 0020 rework

The following fixes are accepted as source changes but not yet as executed B3 proof:

```text
provider total_timeout_seconds:
finite / positive / exact integral validation
→ integer canonical representation

integration imports:
Ruff I001 fixed

zero-call spies:
installed before owner/bootstrap construction

requested mutation/dispatch boundary map:
expanded

candidate authorship:
UNKNOWN
```

The final 0020 candidate bytes are now the frozen starting point for the next rework.

# remaining source defect

Browser source review of the final candidate identifies the next strict-canonical boundary defect in:

```text
src/aiscc/scenarios/composition.py
```

The provider fingerprint float is now normalized, but the tool fingerprint still does:

```python
tool_hash = canonical_sha256(
    {
        **asdict(tool),
        ...
    }
)
```

`StockroomToolConfig.argv` is a:

```text
tuple[str, ...]
```

and `dataclasses.asdict()` preserves that tuple.

The AISCC canonical hash boundary is a strict JSON-value boundary; the fingerprint payload must contain JSON arrays (`list`), not Python tuples or other non-JSON containers.

Therefore the direct `asdict(tool)` expansion remains an unnormalized canonical payload.

This explains why canonical owner composition still fails immediately after the provider-float repair, before fingerprint assertions or zero-side-effect milestones can complete.

# required correction

Only:

```text
src/aiscc/scenarios/composition.py
```

may change.

Construct the tool fingerprint payload explicitly in the canonical JSON subset.

At minimum:

```text
argv:
list(tool.argv)
```

All other tool fields must be explicit stable strings/integers, and the payload must include the same accepted semantic fields as the current fingerprint.

Do not modify:

```text
StockroomToolConfig
B2 config
canonical_json_bytes
canonical_sha256
tool runtime semantics
security semantics
tests
```

Also audit every `_fingerprints()` payload after the change and confirm that every leaf/container is only:

```text
dict with string keys
list
str
int
bool
None
```

No tuple/frozenset/MappingProxyType/dataclass/float may reach `canonical_sha256`.

# phase state

```text
P2-3 Phase 1B-B3:
CANDIDATE / REWORK_REQUIRED

B3 accepted:
NO

B3 persisted:
NO

actual scenario capture:
NOT_STARTED

Replay:
NOT_STARTED

PUBLIC_BOUNDED_LIVE:
NOT_RELEASED
```

# session

The successor remains inside the same B3 candidate/rework authority.

```text
fresh IDE Executor chat:
NOT_REQUIRED

Browser:
CONTINUE_CURRENT_BROWSER_SESSION

Handoff:
NOT_REQUIRED
```
