# AISCC P2-4 — External IDE execution ingress authority extension Human review

## 0. Browser Command Center judgment

1635 Executor result:

```text
BLOCKED / GOLDEN_EXECUTION_INGRESS_UNAVAILABLE
```

Browser independent disposition:

```text
ACCEPTED_AS_TRUTHFUL_FAIL_CLOSED
```

Browser classification:

```text
HUMAN_DESIGN_DECISION_REQUIRED
/ P1_5_EXTERNAL_IDE_EXECUTION_PRODUCER_AUTHORITY_EXTENSION
```

This is not a reproduced product regression and not an Executor defect.

It is a missing semantic authority needed to connect the already accepted self-dogfood TaskContract/READY source to a real external IDE Executor execution.

## 1. Result integrity

1635 result ZIP:

```text
SHA-256:
9a07ac4157869721b3dcceb172145d7ffae598c78ed464de506673bff5fc5aac

members:
45

manifest rows:
44

one top-level:
PASS

CRC:
PASS

manifest size/SHA:
44/44 exact

issued outer Task/Cycle/Judgment:
byte-exact

issued inner golden Task:
byte-exact
```

Governance Commit A:

```text
e1b19a50fe59e00fa268c7cc67ff8603dea5a9e1

parent:
40bc4f8e2a9e10b42531441c1a4ee92c59bef963

changed paths:
exact 3
```

No Result Commit B exists.

No operational PostgreSQL, TaskContract, WorkRun, source edit, execution submission, Evidence, Judgment, Cycle or resulting NextAction was created.

This is the correct fail-closed outcome.

## 2. Exact gap

Current accepted P1-5 execution authority is provider/tool centric.

Existing source can truthfully produce an issuer-verified execution submission when execution is performed through the P1-5 provider/tool causal path.

Current source does NOT provide a public authenticated ingress that can truthfully assert:

```text
this external IDE Executor
executed this exact TaskContract/WorkRun
against this exact repository/base
and produced this exact observed source diff
```

The following are NOT sufficient:

```text
ExecutionReferenceAuthority.register_submission(...)
manually assembled ExecutionSubmissionRef
generic P1-4 guard issuance
Agent prose / Executor claim
direct persistence row insertion
provider-only private completion helper reused without provider execution
```

Using any of them would collapse:

```text
Agent claim != system execution authority
```

and would make `G_EXECUTOR_SUBMISSION` forgeable.

## 3. Why this requires Human design authority

This is not merely “expose an existing private verifier.”

The accepted P1-5 semantic owner currently defines provider/tool execution and producer refs.

To support real AISCC self-dogfood through the external IDE Executor, P1-5 must recognize a second bounded producer class.

That changes the set of entities authorized to mint an issuer-verified execution submission.

Therefore Browser Command Center must not silently implement it without Human acceptance.

## 4. Proposed bounded design

Design ID:

```text
AISCC-P1-5-EXTERNAL-IDE-EXECUTION-INGRESS-V1
```

Owner:

```text
P1-5 Execution Authority
```

Supported producer:

```text
LOCAL_IDE_SELF_DOGFOOD_V1
```

This is intentionally NOT a generic external executor framework.

It exists only for AISCC-owned local self-dogfood execution.

## 5. Core authority split

Preserve:

```text
TaskContract:
what work is authorized

P1-4:
WorkRun / WorkflowState / TransitionDecision

P1-5:
whether an execution producer genuinely started/completed and which immutable producer ref resulted

P1-6:
whether submitted execution material becomes admitted evidence

P1-7:
Judgment

P1-8:
Cycle / NextAction
```

New ingress does not alter those owners.

## 6. New durable authority

Introduce an append-only external-execution session/submission authority under P1-5.

Recommended logical types:

```text
ExternalExecutorLeaseV1
ExternalExecutorSubmissionV1
VerifiedExternalExecutionSubmissionV1
```

Recommended producer kind:

```text
LOCAL_IDE_SELF_DOGFOOD_V1
```

Names may be adapted to existing P1-5 conventions during implementation, but semantics must remain exact.

## 7. Lease creation — before source edit

A trusted control-plane adapter creates a one-time execution lease only after the exact WorkRun is truthfully RUNNING.

Lease binds at minimum:

```text
project_id
work_run_id
work_run_state_version
task_id
task_contract_id
task_contract_version
task_contract_body_ref
task_contract_body_sha256

repository_id
repository_root
base_commit

inner_task_sha256

allowed_paths
forbidden_paths

execution_producer = LOCAL_IDE_SELF_DOGFOOD_V1

issued_at
lease_id
lease_nonce / opaque capability identity
```

The lease is:

```text
server/control-plane issued
single-use
short-lived or run-state-bounded
durable
non-transferable across WorkRun/TaskContract/repository/base
```

The Agent/IDE Executor cannot create its own lease.

## 8. Trusted repository observation

Completion does NOT trust caller-supplied claims for source-change facts.

A trusted local execution adapter observes the repository directly after the IDE operation.

It computes at minimum:

```text
observed_HEAD
index state
tracked/untracked changed paths
deleted/renamed paths
git diff --check result
per-governed-file SHA-256
aggregate observed source-change root
```

For the first golden cycle the exact expected observation is:

```text
changed path:
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md

expected SHA-256:
7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368

unauthorized source diff count:
0
```

Caller payload may request completion, but it cannot author these observed values.

## 9. Submission issuance

The trusted adapter verifies:

```text
lease exists/current/unconsumed
WorkRun still exact expected state/version
TaskContract still current
repository/base still exact
observed diff stays inside TaskContract scope
required output hashes exact
git diff --check PASS
```

Then P1-5 atomically:

```text
consumes lease
persists immutable ExternalExecutorSubmission
registers issuer-verified ExecutionSubmissionRef
```

The resulting `ExecutionSubmissionRef` may be consumed by existing:

```text
P1-4 G_EXECUTOR_SUBMISSION verification
P1-6 producer-ref evidence issuer
```

without generic/manual registration.

## 10. No fake AgentOutputRef

The external IDE path must NOT fabricate a provider-style `AgentOutputRef` merely because the existing provider path uses one.

Two acceptable implementation outcomes:

### Preferred

Extend P1-5 producer-ref resolution so an external IDE submission has its own immutable source record and still resolves to the existing common `ExecutionSubmissionRef` authority contract.

### Acceptable only if current model naturally supports it

Use an existing generic execution-output abstraction if it already truthfully represents non-provider execution.

Do NOT relabel repository diff bytes as provider output.

## 11. Authentication / trust boundary

V1 is local control-plane mediated.

Authentication authority is:

```text
server-issued execution lease
+
same local AISCC runtime
+
direct repository observation by trusted adapter
+
current WorkRun/TaskContract checks
```

Not:

```text
Agent self-attestation
IDE chat text
Markdown report
caller-supplied file hash
caller-supplied changed-path list
```

No external network identity provider is required for V1.

## 12. Concurrency and replay

Must fail closed for:

```text
lease replay
double completion
wrong WorkRun
wrong state_version
TaskContract revoked/superseded
repository HEAD/base changed unexpectedly
path scope violation
file hash mismatch
concurrent source mutation
concurrent WorkRun terminal transition
stale lease after restart
```

Exactly one successful immutable submission may consume one lease.

Retry of exact already-completed operation may return the same durable submission if existing P1-5 idempotency conventions allow it.

Changed retry must deny.

## 13. Durability / restart

Lease and submission must survive process restart.

After restart, P1-5 must be able to verify:

```text
lease lineage
consumption status
submission identity
repository observation root
ExecutionSubmissionRef issuer authenticity
```

No in-memory-only registration may be the sole authority.

## 14. Evidence boundary

External execution submission is producer authority only:

```text
ExternalExecutorSubmission
!= EvidenceCandidate
!= AdmittedEvidence
!= G_EVIDENCE
!= Judgment
```

P1-6 remains solely responsible for evidence admission/satisfaction.

## 15. Human boundary

This ingress does not create:

```text
HumanGate
HumanResult
G_HUMAN_*
Judgment
G_JUDGMENT_*
```

The golden cycle remains `human NOT_REQUIRED` only where the existing TaskContract/Judgment policy says so.

## 16. Security boundary

V1 explicitly forbids:

```text
arbitrary shell execution service
generic remote executor registration
network callback/webhook executor
provider/tool bypass
secret access
automatic task generation
automatic Git commit
automatic deploy/push
arbitrary repository selection
unbounded allowed paths
```

The ingress authenticates a bounded already-authorized local IDE execution.
It does not become an execution engine.

## 17. Proposed implementation surface

Expected source scope after Human acceptance, subject to exact source audit:

```text
src/aiscc/providers/authority.py
src/aiscc/providers/models.py
src/aiscc/providers/ports.py
src/aiscc/providers/service.py
src/aiscc/persistence/models.py
src/aiscc/persistence/repository.py
src/aiscc/evidence/issuers.py
```

Potential migration:

```text
one additive migration after 20260914_0009
```

Potential new bounded adapter:

```text
src/aiscc/providers/external_ide.py
```

or equivalent P1-5-owned location.

Do not mutate P1-4/P1-6/P1-7/P1-8 semantic rules merely for convenience.

Exact implementation allowlist must be produced after source audit.

## 18. Required proof before retrying golden cycle

Implementation must prove on isolated PostgreSQL 17.6:

```text
lease issue PASS
RUNNING WorkRun binding PASS
single-use consumption PASS
direct repository observation PASS
scope violation DENY
wrong hash DENY
wrong repo/base DENY
revoked TaskContract DENY
stale state_version DENY
restart verification PASS
double completion deterministic
manual register_submission cannot substitute
generic G_EXECUTOR_SUBMISSION still denied
issuer-verified external submission accepted
P1-6 producer-ref resolution accepts exact external submission
no provider/tool/secret action
no Evidence/Judgment minted by P1-5
```

Then direct P1-4/P1-5/P1-6 regressions must pass.

## 19. Golden-cycle retry rule

Do not combine ingress implementation and the actual golden cycle into one Human acceptance result.

Sequence:

```text
A. Human accepts this design
B. bounded P1-5 implementation Task
C. Browser independently accepts implementation candidate
D. retry the existing 1635 golden cycle with fresh runtime identities
```

The already persisted 1635 Governance Commit A remains historical acceptance provenance.

No failed golden runtime identity exists because 1635 stopped before DB/runtime provisioning.

## 20. Alternatives considered

### A. Manually call register_submission

Rejected.

Reason:

```text
registration != authentication
```

### B. Reuse provider completion helper without provider execution

Rejected.

Reason:

```text
would fabricate provider causal provenance
```

### C. Treat Git diff / Executor report as Evidence directly

Rejected.

Reason:

```text
Agent claim / local observation without authenticated producer
!= issuer-verified P1-5 execution submission
```

### D. Remove G_EXECUTOR_SUBMISSION requirement for self-dogfood

Rejected.

Reason:

```text
weakens P1-4/P1-5 non-substitution boundary
```

### E. Add bounded local external-IDE producer authority

Recommended.

## 21. Browser recommendation

```text
RECOMMENDATION:
ACCEPT
```

Reason:

1. The blocker is submission-critical: without this producer authority, the actual self-dogfood golden chain cannot cross RUNNING -> execution submission/evidence truthfully.
2. It preserves `Agent claim != System state/evidence`.
3. It does not weaken existing provider/tool execution authority.
4. It reuses the common issuer-verified `ExecutionSubmissionRef` handoff rather than inventing a parallel evidence path.
5. It is deliberately local and self-dogfood-specific, avoiding a generic executor framework.
6. It gives the control plane a truthful way to observe the exact repository change that the external IDE Executor actually made.
7. It can be independently tested before the golden cycle is retried.

## 22. Human decision requested

Choose exactly one:

```text
ACCEPT
REWORK
REJECT
```

If `ACCEPT`:

Browser Command Center should issue a P1-5 external IDE execution-ingress implementation Task after exact source audit.

The implementation Task must not execute the golden cycle.

After Browser accepts that implementation, retry 1635 using fresh runtime identities and the same exact one-file golden Agent change unless repository/base changes require a newly hashed inner Task.
