# AISCC IDE Executor fresh-session handoff — P2-4 actual golden cycle

## 0. session instruction

This document is for a **new IDE Executor chat session**.

Reason:

```text
the prior IDE session completed the external-IDE authority implementation series;
the actual golden cycle is a different execution phase;
the old session had become slow;
a clean context boundary is now desirable.
```

Do not continue the previous IDE chat for this Task.

The new chat does not need historical conversational context beyond this delivery package and the repository itself.

## 1. current accepted repository baseline

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Branch:

```text
main
```

Persisted HEAD:

```text
6eedc50c567f552a3b9d2902c95bd71a99ca441f
```

Parent:

```text
0d53871453b20dc33bc214b213d1600cedaa8a7e
```

HEAD is Browser-accepted:

```text
ACCEPTED
/ P2_4_EXTERNAL_IDE_EXECUTION_START_IMPLEMENTATION_CANDIDATE
```

Migration head:

```text
20260914_0011
```

## 2. accepted P2-4 authority stack

Already accepted/persisted:

```text
Durable TaskContract V1
cycle-derived-only TaskContract source/currentness
SelfDogfoodTaskSpec materialization
TaskContractReadyParticipant
P1-4 READY entry

LOCAL_IDE_SELF_DOGFOOD_V1 start:
READY
→ durable one-time start permit
→ owner-verified external start ref
→ G_EXECUTION_STARTED
→ P1-4 RUNNING

LOCAL_IDE_SELF_DOGFOOD_V1 completion:
RUNNING
→ durable completion lease
→ trusted direct Git observation
→ immutable external submission
→ common ExecutionSubmissionRef
→ G_EXECUTOR_SUBMISSION
→ P1-6 live/historical producer verification
```

Do not redesign these accepted pieces during the golden Task.

## 3. 1803 final proof

```text
Result ZIP:
7fd52ec0b9267e5f3c2634910ad45c1e0f66963f2cd1440d6ae329bfc6405ab8

63 members
62 manifest rows exact
CRC PASS

405 PASS
0 FAIL
0 ERROR
0 SKIP

migration 0011:
PASS

Ruff / compile / diff-check / encoding:
PASS

Result Commit:
6eedc50c567f552a3b9d2902c95bd71a99ca441f
```

## 4. actual golden target

This next operation is the first actual local self-dogfood golden cycle.

Target chain:

```text
authoritative current NextAction
→ TaskContract
→ deterministic SelfDogfoodTaskSpec
→ WorkRun READY
→ external IDE start permit
→ WorkRun RUNNING
→ completion lease while repository is still clean
→ exact single-file Agent edit
→ trusted completion/submission
→ EvidenceCandidate
→ admitted evidence / satisfaction
→ Judgment
→ WorkRun ACCEPTED
→ Cycle
→ exact result Git commit
→ resulting current NextAction
```

No pytest fixture may substitute for actual operational runtime authority.

## 5. governed Agent change

Exact path:

```text
docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md
```

Expected SHA-256:

```text
7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368
```

The exact inner Task is included in the package:

```text
20260914_1916_aiscc-p2-4-golden-agent-single-file-proof-change-1.md

SHA-256:
c83505fcacbecea42aa769b3caac56fb84a11783205769e76347e8f515cad059
```

## 6. prohibited shortcuts

Do not use:

```text
tests.* imports
pytest fixtures as golden authority
monkeypatch
direct owner-table writes
fake provider execution
manual register_start/register_submission as authenticity
Replay prose as current authority
provider/LLM/network
automatic push/deploy
```

The outer Task contains the full operational contract.

## 7. expected result

Success ceiling:

```text
P2_4_FIRST_SELF_DOGFOOD_GOLDEN_CYCLE_CANDIDATE
/ BROWSER_REVIEW_REQUIRED
```

If a new real owner-boundary gap is discovered, stop truthfully and export the exact blocker.
