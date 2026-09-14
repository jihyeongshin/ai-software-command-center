# AISCC P2-4 — External IDE execution start authority Human review

## 0. Browser Command Center judgment

1721 Executor result:

```text
P2_4_EXTERNAL_IDE_EXECUTION_INGRESS_IMPLEMENTATION_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

Browser independent judgment:

```text
ACCEPTED
/ P2_4_EXTERNAL_IDE_EXECUTION_INGRESS_IMPLEMENTATION_CANDIDATE
```

Persisted Result Commit:

```text
e9c17cbf2783669cf7f92df2399d3877e38c4816
```

The completion/submission side of external IDE self-dogfood is now accepted.

The remaining golden-cycle blocker is:

```text
EXTERNAL_IDE_START_AUTHORITY_GAP
```

This review concerns only READY -> RUNNING start authority.

## 1. Accepted 1721 evidence

Result ZIP:

```text
SHA-256:
8af53c02e445b3148788edac1cda741b3afd0e8a82e62e210a4561dda3d134df

members:
63

manifest rows:
62

CRC:
PASS

manifest:
62/62 exact
```

Final regression:

```text
351 PASS
0 FAIL
0 ERROR
0 SKIP
```

Static:

```text
Ruff PASS
compile PASS
git diff --check PASS
UTF-8/BOM/control PASS
```

Migration:

```text
20260914_0010
PASS
```

Result Commit B:

```text
e9c17cbf2783669cf7f92df2399d3877e38c4816

parent:
e0501dae9c4444891f158e9b6c5126c3866b4a8f

message:
feat(aiscc): add external ide execution ingress

changed paths:
exact 15
```

No actual golden cycle was run.

## 2. What is already solved

Accepted external IDE completion chain:

```text
RUNNING WorkRun
→ durable one-time completion lease
→ bounded local IDE edit
→ trusted direct Git observation
→ immutable external IDE submission
→ issuer-verified common ExecutionSubmissionRef
→ existing G_EXECUTOR_SUBMISSION
→ existing P1-6 live/historical producer verification
```

Durability/restart/tamper/concurrency/provider regression proof is accepted.

This review must not reopen that design.

## 3. Exact remaining gap

Current P1-5 `ExecutionReferenceAuthority` authenticates:

```text
G_EXECUTION_STARTED
→ ExecutionAttemptRef
```

The existing `ExecutionAttemptRef` path is the provider/tool execution-start path.

The first actual external IDE golden cycle needs:

```text
READY
→ truthful external IDE execution start authority
→ RUNNING
→ existing accepted external IDE completion flow
```

Using a provider execution attempt without provider execution would fabricate provenance.

Using a generic guard fact would bypass P1-5.

Therefore a bounded external IDE start authority is required.

## 4. Proposed design

Design ID:

```text
AISCC-P1-5-EXTERNAL-IDE-EXECUTION-START-V1
```

Owner:

```text
P1-5 Execution Authority
```

Producer:

```text
LOCAL_IDE_SELF_DOGFOOD_V1
```

The design is deliberately paired with, but separate from, the already accepted completion ingress.

## 5. Start semantics

Introduce a durable one-time external IDE start authorization.

Recommended logical types:

```text
ExternalIdeExecutionStartPermitV1
VerifiedExternalIdeExecutionStartV1
```

Exact names may follow existing P1-5 conventions.

A trusted control-plane adapter may issue the start permit only while the exact WorkRun is:

```text
READY
```

and only after verifying:

```text
current durable TaskContract
repository identity/root
base commit
task identity/hash
producer = LOCAL_IDE_SELF_DOGFOOD_V1
allowed/forbidden scope
```

## 6. What RUNNING means

For this producer:

```text
RUNNING
```

means:

```text
AISCC has durably authorized and opened one exact local external-IDE execution session
for this WorkRun/TaskContract/repository/base.
```

It does NOT mean:

```text
the source edit already happened
the execution completed
the Agent claim was accepted
evidence was admitted
```

The source edit may occur only after this start authority drives the existing P1-4 transition to RUNNING.

## 7. Start permit binding

Bind at minimum:

```text
project_id
start_permit_id
producer_kind = LOCAL_IDE_SELF_DOGFOOD_V1

work_run_id
expected_state = READY
expected_state_version

task_id
task_contract_id
task_contract_version
task_contract_body_ref
task_contract_body_sha256

repository_id
repository_root
base_commit

inner_task_sha256

scope_fingerprint
issued_at
expiry

opaque start capability hash / nonce hash
```

Raw capability value is never persisted.

Permit is immutable, single-use and durable.

## 8. Existing guard reuse

Preferred composition:

```text
durable verified external start permit
→ P1-5 issuer-backed external start ref
→ existing G_EXECUTION_STARTED
→ existing P1-4 TransitionRequest READY -> RUNNING
```

Do NOT create:

```text
G_EXTERNAL_IDE_STARTED
new WorkflowState
new P1-4 transition
parallel workflow engine
```

P1-4 remains the sole WorkRun/state mutation owner.

## 9. ExecutionAttemptRef non-substitution

During implementation, source audit must determine whether the existing common `ExecutionAttemptRef` can truthfully represent the external producer without false provider/tool fields.

### If YES

A verified external start permit may reconstruct/enroll the existing common start ref.

### If NO

Create a P1-5-owned external start reference type and extend only P1-5 `ExecutionReferenceAuthority.verify(...)` for:

```text
G_EXECUTION_STARTED
```

P1-4 workflow semantics remain unchanged.

Do NOT populate fake provider profile/tool registry/operation lineage merely to reuse `ExecutionAttemptRef`.

## 10. Atomic start consumption

Start transition must be fail-closed.

Required logical order:

```text
load/verify current start permit
verify capability
verify WorkRun still READY at exact version
verify TaskContract still current
verify repository/base still exact
atomically mark/represent permit consumption
create/enroll issuer-verified start ref
invoke existing P1-4 transition
```

The implementation must ensure failed/rolled-back READY -> RUNNING does not leave a reusable or falsely consumed authority state.

Prefer append-only consumption evidence rather than mutating the permit row.

## 11. Relationship to completion lease

The already accepted completion rule remains:

```text
completion lease is issued only after WorkRun is RUNNING
```

Therefore:

```text
start permit
→ RUNNING
→ completion lease
```

They are distinct authority objects.

A start permit cannot be reused as a completion lease.

A completion lease cannot authorize READY -> RUNNING.

## 12. Replay / idempotency

Must fail closed for:

```text
start permit replay
wrong capability
expired permit
wrong WorkRun
wrong state version
TaskContract revoked/superseded
repository/base drift
wrong task hash
changed retry
restart with inconsistent lineage
```

Exact retried transition may return the existing durable P1-4 decision only where existing transition idempotency already permits it.

## 13. Restart durability

After process restart, P1-5 must be able to verify:

```text
start permit identity
consumption/start lineage
producer kind
TaskContract binding
WorkRun binding
issuer authenticity
```

No in-memory-only `register_start(...)` call may be sole authority for the external producer.

## 14. Completion continuity

Once RUNNING is admitted:

```text
existing accepted 1721 completion ingress
```

must be used unchanged.

No new completion path.

No duplicate external submission authority.

## 15. Evidence boundary

External start authority is execution-start authority only.

```text
ExternalIdeExecutionStart
!= ExecutionSubmission
!= EvidenceCandidate
!= AdmittedEvidence
!= Judgment
!= Cycle
```

No P1-6/P1-7/P1-8 authority is minted by start.

## 16. Security boundary

V1 remains local and bounded.

Forbidden:

```text
generic shell execution
arbitrary command execution
generic external executor registry
remote callback/webhook
network executor
provider/tool bypass
secret access
automatic Task generation
automatic Git commit
push/deploy
arbitrary repository selection
```

The start authority opens one already-authorized local self-dogfood execution session.

It does not execute the work itself.

## 17. Expected implementation scope

After Human acceptance, Browser should first audit exact source and then issue one bounded implementation Task.

Likely P1-5-owned scope:

```text
src/aiscc/providers/authority.py
src/aiscc/providers/external_ide.py
src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py
```

Likely additive migration:

```text
20260914_0011
down_revision = 20260914_0010
```

Potential canonical updates:

```text
.aiassistant/rules/AISCC_PROVIDER_TOOL_EXECUTION.md
.aiassistant/rules/AISCC_ORCHESTRATION.md
```

P1-4 workflow source should remain read-only unless source audit proves an unavoidable semantic owner conflict.

No implementation Task should silently widen beyond source audit.

## 18. Required implementation proof

On isolated PostgreSQL and existing P1-4 owner:

```text
READY exact binding PASS
start permit issue PASS
wrong capability DENY
wrong run/version DENY
expired permit DENY
revoked TaskContract DENY
wrong repo/base DENY
single-use start PASS
READY -> RUNNING through existing P1-4 PASS
no direct WorkRun/state write
failed transition leaves no false successful start
restart verification PASS
replay/double-start deterministic
provider start regression PASS
completion lease may issue only after RUNNING
accepted 1721 completion flow regression PASS
no Evidence/Judgment/Cycle minted
```

## 19. Golden-cycle retry rule

Sequence after acceptance:

```text
A. Human accepts external IDE start design
B. bounded start-authority implementation Task
C. Browser independently accepts implementation
D. reissue actual golden-cycle Task on new repository base
E. golden flow:
   NextAction
   → TaskContract
   → READY
   → external start permit
   → RUNNING
   → IDE edit
   → completion lease/submission
   → Evidence
   → Judgment
   → ACCEPTED
   → Cycle
   → result commit
   → resulting NextAction
```

Do not combine implementation acceptance and golden-cycle success into one unreviewed step.

## 20. Alternatives rejected

### A. Fake provider ExecutionAttemptRef

Rejected.

Reason:

```text
provider provenance would be fabricated
```

### B. Generic P1-4 G_EXECUTION_STARTED issuance

Rejected.

Reason:

```text
bypasses P1-5 execution authority
```

### C. Let IDE edit while WorkRun is READY and mark RUNNING later

Rejected.

Reason:

```text
execution happened before system execution authority
```

### D. Reuse completion lease to start

Rejected.

Reason:

```text
accepted completion lease is RUNNING-bound
```

### E. Add bounded durable external start permit

Recommended.

## 21. Browser recommendation

```text
RECOMMENDATION:
ACCEPT
```

Reason:

1. 1721 has closed the completion/submission authority gap.
2. This is the final known authority gap before the first actual golden cycle can begin truthfully.
3. It preserves P1-4/P1-5 separation instead of weakening `G_EXECUTION_STARTED`.
4. It avoids fake provider execution lineage.
5. It keeps external IDE support local, bounded and self-dogfood-only.
6. It preserves the accepted rule that no governed source edit happens before WorkRun is RUNNING.

## 22. Human decision requested

Choose exactly one:

```text
ACCEPT
REWORK
REJECT
```

If ACCEPT:

Browser Command Center should issue a bounded external IDE start-authority implementation Task.

The Task must NOT perform the actual golden cycle.

After Browser accepts that implementation, reissue the golden cycle against the new repository base.
