# AISCC Handoff — three-blocker narrow rework

## scope

Fix only:

1. semantic role binding overwrite;
2. physically false DEFINITELY_NOT_SENT retry proof;
3. missing stockroom_summary production dispatcher.

## testing

Do NOT run the complete repository test suite.

Reuse predecessor broad regression:

`1502 PASS / 3 existing SKIP / 0 FAIL / 0 ERROR`

for unchanged scope.

Run only direct affected tests plus new regression tests.

If broader testing becomes necessary, STOP with `EVIDENCE_SCOPE_EXPANSION_REQUIRED`.
