# Browser Command Center Judgment

## decision

`HUMAN_ACCEPTED / PUBLIC_FIXED_IN_PROCESS_TOOL_AMENDMENT_AUTHORIZED`

## exact amendment

For `PUBLIC_BOUNDED_LIVE / stockroom-s1-normal / 1.0.0` only:

- preserve actual Tool Broker and capability flow;
- preserve durable TOOL operation/evidence semantics;
- require exact empty-object arguments;
- return only canonical server-owned synthetic Stockroom output;
- remove Public Live PROCESS requirement;
- do not grant Public Live filesystem capability for this tool;
- do not grant Public Live tool-network capability;
- do not grant a tool secret;
- keep real OpenAI provider network/secret authority separate and unchanged.

## explicitly preserved

- `OWNER_SELF_DOGFOOD` Docker path;
- Stockroom Docker image provenance;
- process timeout/termination/unknown semantics for owner execution;
- provider authority and one-use secret resolution;
- admission/rate/budget/campaign limits;
- fixed scenario/model/repository identity;
- Human/Browser state-transition ownership.

## truthful evidence boundary

After this amendment AISCC may state:

- Owner/Self-Dogfood Stockroom uses Docker-backed isolated process execution.
- Public Bounded Live S1 uses a brokered fixed deterministic in-process tool with no process/filesystem/tool-network capability.

AISCC must not state that the amended Public Live Stockroom tool executes inside Docker.

## authorization

The successor Executor Task may:
- implement the amendment narrowly;
- update directly affected Public Live security authority;
- update focused tests;
- privately redeploy only the existing Railway worker for no-send hosted proof;
- re-prove affected L5/L6 assertions.

It may not:
- enable admission;
- expose ingress;
- create a public run;
- call OpenAI;
- settle the failed 1919 run;
- deploy enabled frontend/Cloudflare Live.
