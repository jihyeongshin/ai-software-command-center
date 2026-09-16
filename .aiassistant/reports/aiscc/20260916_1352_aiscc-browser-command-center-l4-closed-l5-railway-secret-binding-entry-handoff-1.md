# AISCC Browser Command Center Handoff — L4 closed → L5 Railway secret binding

## repository identity

```text
HEAD:
04436a11adc6dd6e70b4a98568fe878cc4c9f4aa
```

## L4

```text
provider:
OpenAI

model:
gpt-5.6-luna

provider profile:
ACCEPTED V1

implementation:
ACCEPTED

account evidence:
HUMAN_ACCEPTED

L4:
CLOSED
```

## current credential

Non-secret identity only:

```text
service account:
aiscc-public-live-runtime

project:
AISCC

permission:
Restricted

Responses:
Write
```

Do not request or export the key value.

## intended deployment use

The key is intended for the Railway Bounded Live backend service only.

Recommended secret deployment contract:

```text
scope:
Railway production environment + exact backend service only

variable:
AISCC_OPENAI_API_KEY
(or existing accepted equivalent after source audit)

storage:
Railway service variable

production protection:
sealed

resolver:
trusted server-side SecretProvider / credential resolver

SDK:
explicit api_key injection from resolver result

public sandbox:
no raw key

child process env:
no raw key

frontend:
no key

database:
no key
```

Railway production target remains Singapore/Southeast Asia according to accepted deployment direction.

## rotation

Required operational sequence:

1. create replacement project-scoped restricted key;
2. update Railway sealed backend variable;
3. deploy/restart through approved release process;
4. run bounded provider canary;
5. only after canary PASS, revoke old key;
6. preserve only non-secret key identity/rotation evidence.

## next Task

Recover exact frozen L5 stage first.

Then inspect existing repository secret/runtime/deployment owners and implement only the minimum missing source/config boundary.

Do not deploy or perform real provider inference unless the exact recovered L5 authority and Task explicitly authorize it.
