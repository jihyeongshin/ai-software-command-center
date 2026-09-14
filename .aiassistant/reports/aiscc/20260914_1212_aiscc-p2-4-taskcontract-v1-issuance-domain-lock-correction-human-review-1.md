# AISCC P2-4 — TaskContract V1 issuance-domain / lock-contract correction Human review

## 0. Browser Command Center judgment

1131 Executor result:

```text
BLOCKED / POLICY_CONFLICT_INVESTIGATION_REQUIRED
```

Browser independent disposition:

```text
ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED
```

Browser classification:

```text
HUMAN_DESIGN_DECISION_REQUIRED
/ TASKCONTRACT_V1_ISSUANCE_DOMAIN_LOCK_CONFLICT
```

This is not a production/runtime regression and not an Executor defect.

It is a conflict between:

```text
Human-accepted 0319 TaskContract lock invariant
```

and:

```text
current P1-8 OPERATIONAL_RECOVERY currentness semantics
```

## 1. Result integrity

1131 Executor result ZIP:

```text
SHA-256:
56b72af5731f55ed8c171483e8113c4dbe1ab89461d46adaffd3079d985bb7bc
```

Independent verification:

```text
50 members
one top-level directory
CRC PASS
49 EXPORT_MANIFEST rows
all row sizes exact
all row SHA-256 exact
no extra unmanifested member
TASK.md == canonical done Task byte-exact
```

Current Task SHA-256:

```text
8749d2c2386a2d956215bb86a42b3858e2348ff3aa8297d28487affcd5b7b91f
```

Governance Commit A:

```text
0400c7839088c10b6530968014180ccb3f7c943a

parent:
325a9044cb0a37694409c1b8285427640d3acaec

message:
docs(aiscc): record p1-6 definition resolver blocker
```

No Result Commit B exists.

No durable TaskContract baseline adoption, migration `20260914_0009`, complete runtime, READY integration or golden cycle exists.

## 2. Partial implementation status

Seven source/test paths are preserved as an uncommitted partial candidate:

```text
src/aiscc/evidence/repository.py
src/aiscc/next_action/repository.py
src/aiscc/task_authority/contracts.py
src/aiscc/task_authority/ports.py
src/aiscc/task_authority/repository.py
tests/integration/evidence/test_requirement_definition_resolver.py
tests/integration/memory/test_postgres_project_memory_next_action.py
```

P1-6 resolver evidence:

```text
initial:
4 PASS

expanded:
5 PASS / 9 FAIL
```

The nine failures occurred while attempting corruption fixtures against existing append-only P1-6 rows, before resolver assertions. A fixture correction was preserved but not rerun.

Final static state:

```text
syntax:
PASS

git diff --check:
PASS

Ruff:
FAIL / 23 findings
```

Therefore none of this partial implementation is accepted yet.

## 3. Exact lock conflict

Human-accepted 0319 section 7 states:

```text
READY:
acquire existing WorkRun lock first
then TaskContract family lock

issuer/revoker:
never acquires WorkRun locks
```

The purpose was to prevent a reverse dependency between run authority and TaskContract family authority.

However, current P1-8 `verify_current_selection(...)` for the owner-recognized:

```text
OPERATIONAL_RECOVERY
```

path must acquire the predecessor/source WorkRun transaction lock before validating the historical P1-4 transition provenance.

Therefore a TaskContract issuer that supports OPERATIONAL_RECOVERY and performs current P1-8 verification in the same issuance transaction would necessarily acquire a WorkRun lock.

These two requirements cannot both be true:

```text
A.
issuer must verify current OPERATIONAL_RECOVERY authority in-transaction

B.
issuer must never acquire any WorkRun lock
```

The Executor correctly refused to:

```text
remove the P1-4 source-run lock
verify currentness outside the issuance transaction
silently reject OPERATIONAL_RECOVERY
silently rewrite the accepted lock contract
```

## 4. Browser preferred correction

### Decision proposed

Bound durable TaskContract V1 issuance for the P2-4 self-dogfood cut to the owner-recognized:

```text
open-cycle-derived-task-issuance
```

path only.

Explicitly declare:

```text
TaskContract Durable Body V1 supported NextAction issuance source:
open-cycle-derived-task-issuance

TaskContract Durable Body V1 unsupported source:
open-operational-recovery-task-issuance
```

This is a TaskContract V1 capability boundary.

It does NOT change P1-8.

P1-8 continues to support both catalog actions:

```text
open-cycle-derived-task-issuance
open-operational-recovery-task-issuance
```

`OPERATIONAL_RECOVERY` remains valid P1-8 authority for workflows that already own that mode.

It simply cannot be materialized into the new durable TaskContract V1 issuer in P2-4.

## 5. Lock invariant after correction

Keep 0319 lock invariant unchanged:

```text
TaskContract issuer/revoker:
never acquire WorkRun locks
```

For V1 issuance:

```text
P1-8 current selection verification
must be the cycle-derived path
and must not require predecessor WorkRun locking
```

If the selected source action requires a predecessor/source WorkRun lock:

```text
TASKCONTRACT_V1_UNSUPPORTED_NEXT_ACTION_SOURCE
```

deny before TaskContract body issuance.

READY remains:

```text
target WorkRun lock
→ TaskContract family lock
→ verify admitted TaskContract/current authorities
→ P1-4 owns READY mutation
```

No source WorkRun lock is introduced into the issuer path.

## 6. Golden-cycle gate

This correction does not assume the future authoritative current NextAction.

Before actual P2-4 golden issuance, the runtime must prove:

```text
current P1-8 selected action
== open-cycle-derived-task-issuance
```

If the authoritative selected action is instead:

```text
open-operational-recovery-task-issuance
```

or another source requiring a predecessor WorkRun lock:

```text
STOP
```

The system must not silently translate it into cycle-derived issuance.

That case would require a separate Human-reviewed lock-order extension.

## 7. Why this is preferred over changing the lock order now

Alternative design:

```text
allow TaskContract issuer to acquire predecessor/source WorkRun locks
```

would require reviewing a larger multi-owner order across:

```text
source WorkRun lock
target WorkRun lock
TaskContract family lock
P1-8 currentness locks
P1-6 requirement authority locks
```

It would also require proving no cross-run inversion for READY, revoke/replacement, recovery issuance and concurrent P1-4 transitions.

No such proof exists in 1131.

The current competition-critical P2-4 goal is bounded self-dogfood cutover, not universal recovery-task issuance.

Therefore the narrower V1 domain is the smaller and safer correction.

## 8. Non-substitution preserved

Human acceptance of this correction does NOT mean:

```text
OPERATIONAL_RECOVERY is invalid
P1-8 is narrowed globally
cycle-derived action can be fabricated
ActionDescriptor becomes TaskContract
TaskIssuanceCandidate becomes TaskContract
historical replay becomes current authority
source-run locking can be skipped for recovery
```

The following remain mandatory:

```text
current owner-backed P1-8 selection
exact recognized descriptor/action
EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY
explicit complete immutable body authorization
P1-6 definition authority
P1-7 Human/Judgment authority
P1-4 transition authority
durable body/ref/event verification
```

## 9. Existing accepted corrections unchanged

Remain accepted unchanged:

```text
0319 durable-body base:
all clauses except this exact issuance-domain correction

0812:
hashed 93-character body_ref correction

0902:
Human/Judgment binding correction

0940:
template/approval authority Outcome A correction
```

This review supersedes only the implicit 0319 assumption that every owner-recognized P1-8 issuance mode must be supported by TaskContract Durable Body V1 while simultaneously preserving the issuer-never-WorkRun-lock invariant.

## 10. Browser recommendation

```text
RECOMMENDATION:
ACCEPT
```

Reason:

1. It preserves the already accepted lock-safety invariant.
2. It does not weaken P1-4 source-run currentness protection.
3. It does not change P1-8 semantics or remove OPERATIONAL_RECOVERY.
4. It avoids introducing an unproven multi-run lock hierarchy.
5. It is sufficient for the bounded P2-4 self-dogfood objective if the authoritative golden-cycle action is cycle-derived.
6. It creates an explicit fail-closed unsupported-source boundary rather than silently dropping a mode.
7. Universal OPERATIONAL_RECOVERY TaskContract issuance can be designed later if it becomes product- or submission-critical.

## 11. Human decision requested

Choose exactly one:

```text
ACCEPT
REWORK
REJECT
```

If `ACCEPT`:

Browser Command Center should issue the next continuation Task preserving the current seven-path partial candidate and requiring:

```text
TaskContract V1 issuance:
cycle-derived source only

OPERATIONAL_RECOVERY:
explicit unsupported-source denial

0319 issuer/revoker WorkRun-lock prohibition:
unchanged

P1-6 resolver:
finish tests/currentness/concurrency

P1-8 verifier:
finish cycle-derived currentness proof

durable body:
complete implementation

migration 0009:
create and prove

READY:
complete and prove

PostgreSQL:
full isolated proof

Ruff/tests:
all PASS

Result Commit B:
only after complete PASS
```

If the future real authoritative current NextAction is not cycle-derived, execution must stop for a separate lock-order design decision.
