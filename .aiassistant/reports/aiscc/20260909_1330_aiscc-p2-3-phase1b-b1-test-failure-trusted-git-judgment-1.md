# AISCC Command Center Judgment

## meta

- judgment_id: `20260909_1330_aiscc-p2-3-phase1b-b1-test-failure-trusted-git-judgment-1`
- created_at: `2026-09-09T13:30:00+09:00`
- project: `AI Software Command Center (AISCC)`
- submitted_task: `.aiassistant/tasks/done/20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1.md`
- submitted_bundle: `20260909_1329_aiscc-p2-3-phase1b-b1-pinned-resource-materializer-implementation-1.zip`
- submitted_bundle_sha256: `a95cfaa7ec37abcbbac2478de26310c39580e5aa539104077e8c31c79bfc4e26`
- result_status: `HOLD_REWORK_REQUIRED`
- blocker: `TEST_FAILURE`
- root_cause: `TRUSTED_EXECUTABLE_HARDLINK_POLICY_MISAPPLIED`
- reject_cause: `none`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`

# 판정

`1329` B1 Executor의 mandatory STOP은 적합하다.

Browser Command Center direct bundle review:

```text
ZIP readability / CRC:
PASS

top-level bundle:
1 exact

bundle members:
15

EXPORT_MANIFEST payload:
14 exact

five B1 implementation files:
present / exact exported identity

final Git-visible:
11 exact

index:
empty

tracked product/config/test modification:
none

Git mutation:
NOT_RUN
```

# test result

Exact B1 suite:

```text
5 failed
95 passed
1 skipped
exit 1
```

Primary positive failure:

```text
StockroomMaterializer.materialize
→ _configuration
→ checked_absolute(git.exe)
→ HARDLINK_DENIED
```

Observed host configuration:

```text
C:\Program Files\Git\cmd\git.exe
regular file
reparse = false
st_nlink = 2
```

Four partial-publication tests failed because materialization stopped at the same pre-allocation executable guard, so their expected cleanup disposition was never produced.

# root-cause judgment

`checked_absolute()` is the B1 mutable workspace/path ownership guard.

Its regular-file rule:

```text
st_nlink == 1
```

is appropriate for mutable lease-owned workspace objects where aliasing defeats exclusive ownership.

It was reused unchanged for an operator-configured, read-only Git executable.

That reuse is over-constrained:

```text
trusted executable hardlink
!=
mutable workspace hardlink
```

A regular, non-reparse, operator-configured Git executable may legitimately have multiple hardlinks on Windows.

The fix must remain narrow:

- preserve hardlink denial for workspace/materialized mutable files;
- do not weaken `stockroom_workspace.checked_absolute`;
- add a materializer-private trusted-executable validator whose semantics are appropriate for the configured Git executable only.

# evidence admission ceiling

Admitted:

- transport/workspace/provenance PASS;
- exact five-file B1 candidate existence;
- independent workspace/path tests that actually reached their assertions;
- exact root cause above;
- final export integrity.

Not admitted:

- successful full pinned materialization;
- destination provenance/aggregate proof;
- partial-write cleanup/quarantine proof;
- broad negative materializer cases whose expected `StockroomFailure` may have been satisfied by the earlier Git executable guard.

`95 passed` must not be interpreted as 95 independently proven intended branches.

# required rework

Only these files may change:

```text
src/aiscc/runtime/stockroom_materializer.py
tests/unit/runtime/test_stockroom_materializer.py
```

The other three B1 implementation files remain byte-frozen.

## product fix

Create a materializer-private trusted Git executable check that:

```text
- requires an absolute local path;
- verifies lexical/parent path using existing safe operator-path semantics where appropriate;
- requires the final object to be a regular file;
- rejects symlink/reparse/special objects;
- requires exact git/git.exe name semantics and executable accessibility;
- requires strict resolution/case consistency;
- permits regular-file st_nlink >= 1 for this trusted executable only;
- preserves repository/runtime-root overlap denials;
- does not weaken workspace/source/destination hardlink rules.
```

Do not add requester-controlled executable selection or PATH fallback.

## test fix

Tighten materializer tests so intended failure branches are proven rather than masked by one earlier broad exception.

At minimum:

- positive real configured Git executable reaches complete materialization;
- explicit trusted-executable hardlink compatibility is proven on Windows/current host where observable;
- reparse/symlink/special/untrusted executable cases remain denied;
- static manifest mutations prove the intended resource-validation branch;
- object/list/blob mutation cases prove the intended object-source branch;
- all four partial-publication cases reach allocation and prove CLEANED/QUARANTINED disposition as designed.

Exact reason checks or equivalent branch-reach instrumentation are acceptable.

# phase state

```text
P2-3 Phase 1B-B1:
IMPLEMENTED_CANDIDATE / TEST_REWORK_REQUIRED

P2-3 Phase 1B-B2:
NOT_STARTED

P2-3 Phase 1B-B3:
NOT_STARTED

actual scenario capture:
NOT_STARTED

Replay:
NOT_STARTED
```

# session

The successor remains inside the same B1 implementation/rework authority.

```text
fresh IDE Executor chat:
NOT_REQUIRED

Browser:
CONTINUE_CURRENT_BROWSER_SESSION

Handoff:
NOT_REQUIRED
```
