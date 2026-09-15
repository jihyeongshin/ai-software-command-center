# AISCC P3-3 L1 Stale Focused Count → 129-node Commit Retry Handoff

## candidate state

```text
HEAD:
209e7534f66e9b07ce9d33742e6993370a70f4fb

tracked modified:
6 exact files

Git-visible untracked:
31 exact paths

candidate total before new delivery:
37 exact paths

index:
empty

bytecode:
0
```

## corrected revalidation

The accepted L1 file has 23 tests.

The combined six strict-head + full L1 collection is 129 nodes.

Expected set:

```text
1758 accepted focused 127 node IDs
+
test_migration_paths_and_owner_preservation
+
test_trusted_reconciliation_known_cost_and_denials
```

No product edit is needed.

## persistence

After successful revalidation, the current retry quartet plus the existing 37 paths yields an expected commit path count of 41.

L2 remains Browser-pending until the commit result is judged.
