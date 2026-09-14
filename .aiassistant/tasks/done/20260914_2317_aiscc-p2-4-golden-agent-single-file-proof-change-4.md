# AISCC Golden Agent Task — single-file proof change

## identity
- task_id: `20260914_2317_aiscc-p2-4-golden-agent-single-file-proof-change-4`
- execution_mode: `AISCC_SELF_DOGFOOD`
- task_source: `SELF_DOGFOOD_GENESIS`
- authority_owner: `EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY`
- human_gate: `NOT_REQUIRED`

## goal
Create exactly one governed repository artifact.

## allowed path
`docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md`

The target parent directory may be created when absent; it is not a second governed file.

## exact bytes
```text
# AISCC Self-Dogfood Golden Cycle

This repository artifact was created as the bounded source change of AISCC's first actual self-dogfood golden cycle.

It is not authority evidence by itself. The authoritative provenance is the AISCC TaskContract, WorkRun, admitted evidence, Judgment, Cycle, result Git commit, and resulting NextAction captured by the control plane.
```

Expected SHA-256:
`7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368`

## required checks
- target SHA exact
- `git diff --check` PASS
- governed source diff contains exactly `docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md`
- unauthorized governed source diff count = 0

## non-goals
No AISCC runtime/test/rule/migration/canonical-state change.
No provider/LLM/network.
No scope expansion.

This Markdown Task is instruction/provenance only; the durable TaskContract is runtime authority.
