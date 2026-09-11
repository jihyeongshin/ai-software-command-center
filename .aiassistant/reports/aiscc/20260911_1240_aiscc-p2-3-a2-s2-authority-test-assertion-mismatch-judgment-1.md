# AISCC Command Center Judgment

## meta

- judgment_id: `20260911_1240_aiscc-p2-3-a2-s2-authority-test-assertion-mismatch-judgment-1`
- created_at: `2026-09-11T12:40:00+09:00`
- project: `AI Software Command Center (AISCC)`
- submitted_task: `.aiassistant/tasks/done/20260911_1120_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-static-rework-and-proof-retry-1.md`
- submitted_bundle: `20260911_1120_aiscc-p2-3-a2-s2-negative-evaluation-judgment-authority-static-rework-and-proof-retry-1.zip`
- submitted_bundle_sha256: `550c5cd5652057af036c54f2c9788ed456eb66ce2e7e088573674ae6d1fcea89`
- result_status: `HOLD_REWORK_REQUIRED`
- blocker: `TEST_FAILURE / ASSERTION_MESSAGE_CONTRACT_MISMATCH`
- implementation_disposition: `PRESERVE_CURRENT_CANDIDATE`
- browser_session_action: `CONTINUE_CURRENT_BROWSER_SESSION`
- handoff_required: `No`
- fresh_ide_executor_chat_for_successor: `NOT_REQUIRED`

# 판정

`1120` Executor STOP is conformant and its transport/export is accepted.

Browser direct verification:

```text
ZIP readability / CRC:
PASS

one top-level directory:
PASS

members:
19 exact

required roots:
14 / 14

canonical/source copies:
5 / 5

manifest non-self:
18 / 18 SHA-256 + byte-size PASS

issued 1120 TASK/CYCLE/JUDGMENT:
3 / 3 byte exact

TASK.md == canonical done Task:
byte exact
```

Submitted ZIP SHA-256:

```text
550c5cd5652057af036c54f2c9788ed456eb66ce2e7e088573674ae6d1fcea89
```

# accepted 1120 evidence

```text
in-memory compile:
8 / 8 PASS

Ruff:
8 / 8 PASS

Judgment v1/v2 strict load:
PASS

git diff --check:
PASS

PostgreSQL/Alembic:
20260901_0008 PASS

P1-6/P1-7 mandatory module command:
9 PASS / 1 FAIL / 0 skip
```

The two authorized style-only changes are present:

```text
src/aiscc/evidence/models.py
SHA-256: df48a1c8af09c09827a2d5996e8aed19c3642e9f8b099b58e75bd855ded6c54e

src/aiscc/judgment/models.py
SHA-256: 6a1bed5dca0c0b5a73d4def8c4fdbbc500f81f7e979af312b7cfd6dfebe375c6
```

# failure classification

Failing test:

```text
tests/integration/human/test_postgres_human_gate_judgment.py::test_p1_7_postgres_runtime_proof
```

Observed assertion:

```text
expected ValueError message regex:
negative Judgment basis

actual rejection message:
negative evidence basis requires deterministic rework policy
```

The implementation rejected the invalid negative-basis/policy combination. The failure is therefore currently classified as a **test assertion-message contract mismatch**, not as proof that the rejection semantics are absent.

The next retry must verify the failing test context before changing it. If the exception arose from the intended invalid deterministic-rework-policy case and at the intended P1-7 policy-validation boundary, update only the test assertion so it checks the semantic rejection rather than one narrower wording.

If the rejection came from an unrelated earlier/later validation path, STOP with `ROOT_CAUSE_MISMATCH` and do not weaken the test.

# exact mutation

Only:

```text
tests/integration/human/test_postgres_human_gate_judgment.py
```

No production/config/model source change is authorized.

# test assertion principle

Prefer a semantic assertion equivalent to:

```text
ValueError is raised
AND
message proves:
negative basis
+ deterministic rework policy incompatibility
```

For example, a regex that admits the current canonical wording while preserving those semantic terms is acceptable.

Do not replace the assertion with an unconstrained `pytest.raises(ValueError)` if that would allow an unrelated ValueError to satisfy the test.

# proof after correction

Rerun the entire blocked 0920/1120 proof chain. No previously blocked downstream proof may be inferred from the 9 passing tests alone.

# phase

```text
A2 prepared-owner/materialized-output:
ACCEPTED_CANDIDATE / EXECUTABLE_PROOF_COMPLETE

A2 S2 P1-6/P1-7 implementation:
IMPLEMENTED_CANDIDATE / TEST-CONTRACT REWORK REQUIRED

A2 persistence:
NOT_AUTHORIZED

actual Stockroom runtime:
NOT_STARTED
```
