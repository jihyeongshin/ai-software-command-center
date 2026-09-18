# Final Public State

```text
RELEASE_ROLLED_BACK_TO_REPLAY_ONLY
```

- Recorded Run Replay: PUBLIC / UNCHANGED
- Bounded Live: DISABLED / NOT_RELEASED
- Human final smoke: not applicable after rollback
- public site: `https://aiscc-replay.pages.dev/`
- frontend Live config: disabled
- ingress public exposure: none
- provider request attributable to final smoke: 0
- retained smoke run: 1, failed before dispatch

The release failure is bounded to the production worker pre-dispatch path. A future retry must first add safe exception observability and prove why the canonical claim executor exits before creating an execution operation.
