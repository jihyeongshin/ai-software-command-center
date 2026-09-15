# AISCC P3-3 L1 Migration Policy Block → Scope-Expanded PostgreSQL Retry Handoff

## current candidate state

```text
HEAD:
209e7534f66e9b07ce9d33742e6993370a70f4fb

Public Live prerequisite design:
HUMAN_ACCEPTED / FROZEN

L1:
NOT_IMPLEMENTED / MIGRATION_SCOPE_BLOCKED

Public Live:
NOT_RELEASED
```

## corrected authority

The next retry may create one new additive revision `20260915_0013` and minimally update the repository's existing strict-head regression assertion(s) to the new head.

The test-path discovery must happen before any source edit. If the hard-coded head appears in an ambiguous set of test files, stop instead of broadening the scope.
