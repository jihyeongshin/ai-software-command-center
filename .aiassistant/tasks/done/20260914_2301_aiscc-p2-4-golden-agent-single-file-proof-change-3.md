# AISCC Golden Agent Task — single-file proof change

## identity

- task_id: `20260914_2301_aiscc-p2-4-golden-agent-single-file-proof-change-3`
- execution_mode: `AISCC_SELF_DOGFOOD`
- task_source: `SELF_DOGFOOD_GENESIS`
- authority_owner: `EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY`
- human_gate: `NOT_REQUIRED`

## goal

Create exactly one repository artifact proving that the first successful AISCC self-dogfood golden WorkRun governed a bounded real Git change.

## allowed path

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

No other source/config/test/document path may be created, modified, deleted, renamed, staged or committed by the governed Agent operation.

The target's parent directory may be created as a filesystem prerequisite when absent. Creating the directory itself is not a second governed file.

## exact required bytes

Create `docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md` as UTF-8 without BOM and LF line endings with exactly:

```text
# AISCC Self-Dogfood Golden Cycle

This repository artifact was created as the bounded source change of AISCC's first actual self-dogfood golden cycle.

It is not authority evidence by itself. The authoritative provenance is the AISCC TaskContract, WorkRun, admitted evidence, Judgment, Cycle, result Git commit, and resulting NextAction captured by the control plane.
```

Expected SHA-256:

```text
7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
```

## required checks

```text
target SHA-256 exact
git diff --check PASS
Agent source diff contains exactly docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
unauthorized Agent source diff count = 0
```

## non-goals

Do not change AISCC runtime source, tests, migrations, rules or canonical state.
Do not call provider/LLM/network.
Do not perform another Task or expand scope.

## evidence expectation

The outer operation must produce owner-authenticated evidence for the exact Task/WorkRun/submission/path/hash/diff/scope facts.

This Markdown Task is instruction/provenance only.
The durable TaskContract is runtime authority.
