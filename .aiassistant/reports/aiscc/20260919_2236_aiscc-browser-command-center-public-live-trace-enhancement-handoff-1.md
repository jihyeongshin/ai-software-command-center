# AISCC Browser Command Center Handoff — Public Live Inspectable Execution Trace

## starting point

```text
main:
b821b1ed677ad6d8b93ab1d6b5090218471bd925

P3-3 / L8:
CLOSED

Public Live:
RELEASED

migration:
0027
```

## why this work exists

The production runtime already proves the complete bounded path, but the public UI hides it.

Current read projection provides only public run status and sets `result=null`.

The frontend therefore cannot show:
- the fixed instruction;
- provider role/progress;
- approved tool execution;
- synthetic Stockroom result;
- execution terminalization;
- Human-decision boundary.

## target product message

Recorded Replay answers:

`What happened in prior governed runs?`

Bounded Live should answer:

`What is happening in this actual bounded run, and what durable evidence did the system admit?`

## UI design

Keep:
- existing Fixed public scenario card on the left;
- existing Live session/status block on the right.

Add under Server status:
- `Live execution trace`;
- Replay-style step cards;
- fixed tool facts table;
- explicit Human decision boundary.

Do not turn Live into a scenario-card selector.

## deployment strategy

The new frontend must remain compatible with the old backend `result=null`.

Preferred order:
1. commit/test all source;
2. deploy backward-compatible frontend;
3. apply additive 0028;
4. deploy ingress read projection;
5. verify released state remains healthy;
6. no new run/provider call;
7. stop for Browser review and Human QA issuance.
