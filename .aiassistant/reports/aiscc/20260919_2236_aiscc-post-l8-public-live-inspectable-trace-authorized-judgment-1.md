# Browser Command Center Judgment — Public Live Inspectable Trace Enhancement Authorization

## decision

```text
P3-3 / L8:
CLOSED / UNCHANGED

Public Live:
RELEASED

post-closure enhancement:
AUTHORIZED

scope:
SAFE_PUBLIC_TRACE_PROJECTION + LIVE_TRACE_UI
```

## baseline

`b821b1ed677ad6d8b93ab1d6b5090218471bd925`

Migration entry head:

`20260919_0027`

## problem statement

Current public GET projection deliberately returns no execution result body.

The current frontend therefore displays:

`No bounded public result is available yet.`

even when the public run is already `COMPLETED`.

This is safe but hides the project's core product value from a judge.

## accepted UX target

Do not create multiple Live scenario cards.

The current fixed-scenario left card remains.

The Live session right side gains a Replay-style inspectable trace:

```text
01 · INSTRUCTION
02 · PROVIDER
03 · TOOL
04 · PROVIDER
05 · EXECUTION
06 · PUBLIC PROJECTION

Human decision: NOT PERFORMED
```

The trace must be driven by durable public-safe evidence.

Frontend must never infer provider/tool success merely from final run state.

## backend authority

Core execution contracts are frozen.

Do NOT modify:
- admission POST contract;
- public-control semantics;
- provider request contract/profile;
- OpenAI adapter behavior;
- fixed tool dispatch contract;
- worker orchestration/claim renewal;
- 0025/0026/0027 reconciliation semantics;
- secret/network boundaries.

Authorized backend change is a narrow **read projection contract** only.

Expected implementation:
- additive migration `20260919_0028` if required;
- one SECURITY DEFINER safe trace projection function;
- grant only the narrow read authority needed by public ingress;
- integrate it behind the existing capability-scoped GET;
- no raw table grants.

## release authority

This Task may deploy the additive read projection and updated frontend.

It does NOT authorize:
- a new Public Live run;
- a provider call;
- a release smoke;
- control disable/enable cycle;
- model/tool mutation.

Current Public Live should remain released.

Actual trace UX proof is Human-owned and follows Browser source/runtime review.
