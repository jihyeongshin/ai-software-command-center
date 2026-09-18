# AISCC Browser Command Center Handoff — release rolled back / worker pre-dispatch rework

## current state

- GitHub main: `6c5251fcfd78e01fa1a881f1bfd14b8af5d4bc9c`
- 1919 release attempt: `ROLLED_BACK`
- Replay: public / retained
- Public admission: disabled
- Public Live: not released
- ingress public domain: absent
- edge trust: absent
- frontend Live config: disabled
- worker provider secret: worker-only / sealed
- provider sends attributable to failed smoke: 0

## retained hosted evidence

The failed smoke is intentionally preserved:
- campaign exists;
- one public smoke run exists;
- reservation remains held;
- failed run did not reach provider dispatch;
- claim was eventually released `LIVE_UNAVAILABLE`.

Do not delete or rewrite that evidence.

## likely failure boundary

Source inspection strongly points to the hosted Stockroom dispatcher requiring a local Docker executable before the first execution operation is created.

This hypothesis must be confirmed safely.

## important governance cleanup

The current main accidentally tracks the temporary 1919 target export subtree. Remove it from Git tracking under the successor Task while preserving the canonical Cycle/Judgment/Handoff/done Task.

## re-release boundary

Do not reattempt Public Live release in the successor Task.

First prove/fix the worker pre-dispatch boundary. If preserving the accepted tool/network/filesystem isolation requires a new hosted runtime mechanism or security decision, return to Browser/Human instead of weakening it.
