# AISCC Task

## meta

- task_id: `20260918_1730_aiscc-p3-3-l8-one-call-real-luna-canary-1`
- phase: `P3-3 / L8`
- work_type: `ONE_CALL_REAL_PROVIDER_CANARY`
- execution_model: `THIN_CC_THICK_EXECUTOR`
- entry_commit: `0049c4e07a53571f3781f6e58f5f82a9712454af`
- fresh_ide_executor_chat: `NOT_REQUIRED`
- real_provider_call_authority: `EXACTLY_ONE_PHYSICAL_REQUEST`
- provider: `OpenAI`
- model: `gpt-5.6-luna`
- API: `Responses API`
- maximum_physical_requests: `1`
- retry_authority: `NONE`
- public_release_authority: `NONE`

## Goal

Execute one bounded production credential/provider canary from the existing `aiscc-public-live-worker` service environment and prove that the accepted hosted secret-resolution path can successfully reach the accepted Luna Responses profile.

This Task is provider-readiness proof only.

It is not a public admission/run test.

## Must preserve

- `AISCC_OPENAI_API_KEY` remains worker-service-only and sealed;
- raw key value is never printed, exported, copied into a command, Task, report, Git, log evidence or local developer environment;
- use the accepted `HostedOpenAISecretResolver`;
- use issuer-backed `SecretResolutionLeaseAuthority`; do not manually fabricate `SecretResolutionLease`;
- use `OpenAIResponsesAdapter(hosted=True)`;
- use exact `hosted_luna_profile()`;
- runtime mode: `PUBLIC_BOUNDED_LIVE`;
- scenario: `stockroom-s1-normal`;
- model: `gpt-5.6-luna`;
- Responses API;
- service tier: default;
- reasoning effort: low;
- `store=false`;
- `stream=false`;
- `background=false`;
- `parallel_tool_calls=false`;
- `truncation=disabled`;
- no provider fallback;
- Public admission remains DISABLED;
- Public Live remains NOT_RELEASED;
- campaign remains absent/disabled;
- ingress remains private/fail-closed;
- Replay unchanged.

## Exactly-one-send rule

The entire Task may cause at most **one physical request** to OpenAI.

No automatic provider retry.

No manual second attempt.

No SDK retry.

The accepted adapter already uses `max_retries=0`; preserve that.

If the single request results in:
- timeout;
- transport unknown;
- queued/in_progress ambiguity;
- malformed/unknown provider status;
- connection error;
- any uncertain send outcome;

then:

`STOP / REAL_PROVIDER_CANARY_UNKNOWN / NO_RETRY`

Do not try again in this Task.

## Spend envelope

Accepted L4 conservative per-request bound:

`<= $0.0044`

Task authorization ceiling:

`<= $0.01 total`

This Task authorizes one request only even if the monetary ceiling would technically allow more.

## Canary execution path

The physical request must originate from the existing Railway production worker environment that owns the sealed `AISCC_OPENAI_API_KEY`.

Acceptable implementation:
- a narrow task-owned one-shot canary entrypoint/command executed inside the existing worker service environment;
- an equivalent mechanism that exercises the same trusted resolver and hosted adapter.

Forbidden:
- `curl` to OpenAI;
- direct OpenAI SDK call outside `OpenAIResponsesAdapter`;
- reading `os.environ["AISCC_OPENAI_API_KEY"]` in canary code;
- copying the key to local machine or another Railway service;
- `railway run` or another mechanism that materializes the production key into an unrelated local developer process;
- public HTTP/admission as a trigger.

If a tiny source helper is necessary, it may be added under the existing Public Live/provider support surface, but:
- it must not expose a public route;
- it must not accept free-form input;
- it must not be reachable during normal worker loop execution;
- it must be fixed to this canary profile/scenario;
- it must never print secret material.

Executor owns the exact implementation mechanics.

## Provider request content

Use a minimal fixed server-owned synthetic Stockroom canary input.

It must:
- be non-sensitive;
- contain no user/private repository data;
- not require a tool dispatch;
- request a short deterministic readiness response;
- remain within the existing Luna input/output bounds.

The provider may return ordinary textual output.

Do not export raw model output unless necessary. Prefer evidence consisting of:
- provider outcome enum;
- provider status;
- model/profile identity;
- usage counters if provided;
- response-id presence classification or one-way hash;
- result hash;
- sanitized error classification.

No chain-of-thought/reasoning content may be exported.

## Secret lease proof

The canary must prove:

- a real security-policy-backed secret capability/consumption receipt was issued;
- `SecretResolutionLeaseAuthority` issued the resolver lease;
- `HostedOpenAISecretResolver` resolved the worker environment secret exactly once;
- resolver lease cannot be resolved twice;
- raw secret never appears in stdout/stderr/report/DB/Git.

Do not weaken the accepted production secret policy just to make the canary easy.

## Railway mutation authority

Allowed:
- execute the one-shot canary inside the existing worker deployment;
- if absolutely necessary, redeploy the existing worker to the same or narrow successor source commit containing a task-owned canary entrypoint;
- observe worker status/logs with secret-safe filtering.

Not allowed:
- new Railway service/resource;
- variable value read/export;
- key on another service;
- ingress/initializer/owner mutation;
- public domain;
- edge trust;
- campaign/control mutation;
- scale increase;
- database role/grant mutation.

## Hosted DB boundary

The preferred canary does not require creating a Public Live run.

Do not enable admission or create a public campaign to obtain the provider proof.

If the chosen exact trusted secret-policy path unavoidably requires a task-owned durable record, use the smallest isolated non-public canary record only if it is already supported by accepted semantics and does not require a new schema/role/policy choice.

If that is not possible without semantic expansion:

`STOP / CANARY_TRUSTED_PATH_REQUIRES_NEW_AUTHORITY`

Do not improvise a parallel authority.

## Required evidence

### A. pre-send

Prove without revealing values:
- execution is inside exact `aiscc-public-live-worker`;
- `AISCC_OPENAI_API_KEY` presence: yes;
- raw key not read/printed;
- profile = `public-live-luna-v1 / 1`;
- model = `gpt-5.6-luna`;
- adapter = hosted OpenAI Responses adapter;
- max retries = 0;
- invocation count = 0 before call.

### B. send

Prove:
- exactly one adapter invocation;
- exactly one physical OpenAI request maximum;
- exact fixed request safety flags;
- no tool dispatch required for canary;
- no fallback.

### C. result

Success requires a non-ambiguous accepted provider response through the adapter.

Record only sanitized facts.

Candidate success:

`REAL_LUNA_CANARY_EXECUTED / HUMAN_ACCOUNT_CONFIRMATION_PENDING`

Possible honest outcomes:
- `REAL_LUNA_CANARY_PASS_CANDIDATE`
- `REAL_LUNA_CANARY_PROVIDER_REJECTED`
- `REAL_LUNA_CANARY_UNKNOWN_NO_RETRY`
- `REAL_LUNA_CANARY_TRUST_PATH_BLOCKED`

Executor must not convert an unknown send into failure-safe retry.

### D. post-send

- adapter invocation count exactly `1`;
- no second provider request;
- secret lease closed/unreusable;
- Public admission disabled;
- Public Live not released;
- campaign unchanged;
- ingress domain/edge trust unchanged;
- Replay unchanged;
- worker secret still present and sealed/presence-only;
- no raw secret residue in exported evidence.

## Tests / verification

Before the real send:
- run focused unit/static proof for any added canary helper;
- run exact hosted secret/resolver and Luna binding tests directly affected;
- `git diff --check`;
- Ruff/format/narrow mypy as applicable.

Do not consume the real provider call during automated test discovery.

There must be a visibly separate, deliberate one-shot execution step.

## Stop boundary

STOP before the provider request if:
- worker secret is absent;
- another service unexpectedly holds the key;
- resolver path cannot issue a legitimate lease;
- exact profile/model differs;
- source/deployment commit is ambiguous;
- key would need to be printed/copied;
- OpenAI credential/account state is known to have changed;
- Public admission/campaign would need enabling;
- more than one physical request would be required.

After the physical send begins, unknown outcome => STOP with no retry.

## Git / persistence

- persist supplied Cycle/Judgment/Handoff;
- move this Task active -> done;
- if no source helper is needed, governance-only commit/push is expected;
- if a narrow canary helper is necessary, commit/push exact helper/tests before executing the physical canary;
- do not amend/rebase/force push.

## export

Create:

`.aiassistant/reports/target/20260918_1730_aiscc-p3-3-l8-one-call-real-luna-canary-1/`

Required root:
- `EXPORT_MANIFEST.md`
- `TASK.md`
- `EXECUTOR_REPORT.md`
- `CANARY_PRE_SEND_PROOF.md`
- `CANARY_PROVIDER_RESULT.md`
- `SECRET_PATH_PROOF.md`
- `ONE_SEND_PROOF.md`
- `FINAL_SAFE_STATE.md`
- `WORKSPACE_STATE.md`
- changed files preserving project-relative paths

Never include raw provider secret or chain-of-thought.

Also create:

`.aiassistant/reports/target/20260918_1730_aiscc-p3-3-l8-one-call-real-luna-canary-1.zip`

Verify archive integrity and report SHA-256.
