# AISCC Browser Command Center Handoff — pre-dispatch secret policy resolved

## repository

```text
HEAD:
04436a11adc6dd6e70b4a98568fe878cc4c9f4aa
```

Predecessor L5 candidate:

`11/11 preserved / uncommitted`

## controlling hosted-secret identity

```text
environment variable:
AISCC_OPENAI_API_KEY

opaque secret ref:
secret-ref:openai/public-live/runtime/v1
```

## resolved ordering

```text
authority freshness
→ provider + secret capability
→ SecretResolutionLease
→ resolve hosted secret
→ reserve provider/round/budget bounds
→ final freshness
→ DISPATCH_STARTED
→ SDK/provider
```

## missing secret

Use existing canonical pre-dispatch path:

```text
SECURITY_ADMITTED
→ OUTCOME_KNOWN / CANCELLED

reason:
LIVE_UNAVAILABLE
```

Required accounting:

```text
provider send:
0

provider_calls reserved/charged:
0

rounds reserved/charged:
0

provider budget units:
0
```

Do not force `DEFINITELY_NOT_SENT` through a fake dispatch marker.

## successful secret resolution

Resolution only proves credential material is available.

It does not prove:

- freshness after reservation;
- provider dispatch;
- provider success.

Close/revoke the lease on every exit.

## proof still required

- task-owned PostgreSQL 17.6;
- missing + blank secret durable integration;
- positive fake-secret durable integration;
- exact sentinel occurrence in durable DB = 0;
- actual cached sandbox/container env absence;
- child/Git/Docker env proof;
- full suite;
- static/type/diff;
- no provider/Railway call.
