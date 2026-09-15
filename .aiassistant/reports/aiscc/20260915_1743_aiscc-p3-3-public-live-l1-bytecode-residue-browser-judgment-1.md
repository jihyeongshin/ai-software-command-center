# AISCC Browser Command Center Judgment

## 판정

```text
result_status: ACCEPTED_BLOCKER / L1_IMPLEMENTATION_REWORK_REQUIRED
cause: EXECUTOR_GENERATED_PYTHON_BYTECODE_RESIDUE
phase: P3-3 PUBLIC LIVE L1
baseline_head: 209e7534f66e9b07ce9d33742e6993370a70f4fb
```

## admitted evidence

Browser inspected the uploaded 1723 result ZIP:

`SHA-256 19f98b2798c972578f8a619ec49bbd0218d817ef7e8f737984ff8bc24694483c`

Accepted facts:

- transport manifest PASS;
- baseline HEAD/index/tracked state PASS before execution;
- Alembic head `20260914_0012` PASS;
- Replay builder PASS;
- Docker Desktop started normally under current user;
- cached official `postgres:17.6` used with no pull;
- PostgreSQL 17.6 loopback readiness PASS;
- asyncpg and repository SQLAlchemy connectivity PASS;
- isolated empty DB/table create-drop PASS;
- Task-owned PostgreSQL container and anonymous volume cleanup PASS;
- no source/migration/index/commit/provider/deployment mutation.

## blocker

Alembic/import execution generated exactly 32 Git-visible `.pyc` files outside the L1 allowlist.

The Executor preserved them because the predecessor contract said to stop without cleanup when unrelated working-tree dirt appears.

This is accepted conservative behavior.

## correction

The next Task explicitly classifies those exact 32 path+hash pairs as:

`EXECUTOR_GENERATED_PYTHON_BYTECODE`

and authorizes deletion of only those exact files after baseline verification.

The retry also requires:

- `PYTHONDONTWRITEBYTECODE=1`;
- Python `-B` on every direct Python/Alembic/pytest invocation.

No `.gitignore` change is authorized.

## transport note

1723 reported that the authenticated Task was read before substantive work, but its canonical placement occurred after companion placement.

The corrected retry requires primary Task canonical placement first, then companion placement.

This is a procedural correction only; no 1723 implementation evidence is accepted beyond the runtime/readiness gates listed above.
