# AISCC Browser Command Center Handoff — Public Fixed Tool Amendment

## baseline

- GitHub main: `0c915f04aaf3b0b026ac6224f1c6c10d390f7075`
- Human decision: `ACCEPT_PUBLIC_FIXED_IN_PROCESS_TOOL`
- Replay: public / retained
- Public Live: not released
- admission: disabled
- ingress public domain: absent
- edge trust: absent

## implementation target

Replace only the Public Live Stockroom execution backend:

```text
before:
Tool Broker
-> TOOL + PROCESS authority
-> StockroomDockerRunner
-> docker container
-> JSON stdout
-> ToolOutputRef

after:
Tool Broker
-> TOOL authority only
-> fixed Public Live dispatcher
-> canonical STOCKROOM_SUMMARY object
-> ToolOutputRef
```

Do not alter Owner/Self-Dogfood Docker execution.

## proof target

Public Live must prove:

- no Docker executable/daemon dependency;
- no subprocess/child process;
- no filesystem access during fixed tool dispatch;
- no tool network access;
- no PROCESS/FILESYSTEM/NETWORK capability issued or consumed for the fixed tool;
- exact Tool Broker receipt path still applies;
- durable TOOL operation and provider continuation still apply;
- real provider is not called during this Task;
- private hosted worker starts cleanly on Railway without Docker.

## after this Task

If Browser accepts the candidate:
1. separately reconcile the retained 1919 definitely-not-sent run;
2. issue a fresh release-readiness/re-release Task;
3. allow at most one new bounded public smoke.
