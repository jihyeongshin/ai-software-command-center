# AISCC Browser Command Center Judgment

## 판정

```text
L4:
ACCEPTED / CLOSED

L5:
SELECTED / ENTRY_AUTHORIZED

repository HEAD:
04436a11adc6dd6e70b4a98568fe878cc4c9f4aa

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## L4 closure basis

The Human OpenAI account gate passed.

Current actual account evidence includes:

- dedicated `AISCC` API Project;
- `gpt-5.6-luna` allowed;
- effective `500,000 TPM / 500 RPM`;
- Pay-as-you-go billing active;
- `$5` credit;
- auto-reload OFF;
- `$15/month` project hard limit with enforcement ON;
- alerts `$10`, `$12`, `$15`;
- project-scoped `aiscc-public-live-runtime` service account;
- Restricted key permissions;
- `/v1/responses` Write only;
- no paid call yet.

The frozen L4 exit does not explicitly require a real paid call, so a local call is not used as substitute for hosted deployment evidence.

## key-use decision

The key is a production/runtime credential, not a repository/local-development credential.

Target architecture:

```text
Human secret store
    ↓
Railway production backend service-level sealed variable
    ↓
trusted server-side secret resolver
    ↓ opaque secret capability / resolution lease
mediated OpenAI Responses adapter
    ↓
OpenAI API
```

Forbidden paths:

```text
Cloudflare frontend
shared/public Railway variable
PostgreSQL
run sandbox
workspace file
child environment
public input
logs
Replay
evidence
```

## variable naming rule

Prefer a non-SDK-autodiscovery deployment variable such as:

`AISCC_OPENAI_API_KEY`

The application should resolve it explicitly and pass the key to the trusted OpenAI adapter.

Do not rely on globally available `OPENAI_API_KEY` if doing so allows SDK/client construction outside the accepted secret-resolution authority.

If the current accepted repository already has an equivalent explicit secret-variable convention, the Executor must recover and reuse it rather than creating a parallel authority.

## Railway rule

Use a Railway **service-level** variable on the Bounded Live backend service, not a project shared variable.

For production, seal the secret after entry.

The production secret must not be copied to PR/preview environments.

## paid provider canary

Plan one minimal real Luna call only after the same deployed secret path is in place.

The canary must use the trusted adapter/secret resolver, not a direct curl with copied key.

Whether this belongs to L5 or L6 must be recovered from frozen stage authority before execution.
