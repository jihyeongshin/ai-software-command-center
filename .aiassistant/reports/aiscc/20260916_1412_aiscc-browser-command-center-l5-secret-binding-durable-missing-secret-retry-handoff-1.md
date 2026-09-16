# AISCC Browser Command Center Handoff — L5 local secret binding rework

## repository

```text
HEAD:
04436a11adc6dd6e70b4a98568fe878cc4c9f4aa
```

Predecessor local candidate remains uncommitted.

Expected candidate source/config/test set:

- `config/deployment/public-live-railway.v1.toml`
- `src/aiscc/providers/external_ide.py`
- `src/aiscc/providers/hosted_secret.py`
- `src/aiscc/providers/openai_responses.py`
- `src/aiscc/providers/service.py`
- `src/aiscc/public_live/luna_profile.py`
- `src/aiscc/runtime/child_environment.py`
- `src/aiscc/runtime/docker.py`
- `src/aiscc/runtime/process.py`
- `tests/fixtures/providers/luna_capabilities.py`
- `tests/unit/providers/test_hosted_secret.py`

Do not revert accepted portions merely because one semantic branch requires rework.

## reuse allowed

Reuse:

- exact L5 authority resolution;
- `AISCC_OPENAI_API_KEY`;
- `secret-ref:openai/public-live/runtime/v1`;
- service-only sealed Railway production secret contract;
- Singapore `asia-southeast1-eqsg3a`;
- build-exposure audit;
- rotation runbook;
- canary plan;
- child environment allowlist direction.

## mandatory fix

Durable execution must distinguish:

```text
HostedSecretUnavailable before SDK call
→ DEFINITELY_NOT_SENT / LIVE_UNAVAILABLE

actual transport/send uncertainty
→ TIMEOUT_OR_TRANSPORT_UNKNOWN_OUTCOME
```

Never classify missing credential as remote unknown outcome.

## mandatory proof completion

Use only fake sentinel secret values.

Required:

1. durable PostgreSQL missing-secret test;
2. DB persisted-state sentinel scan;
3. actual local sandbox/container environment sentinel proof;
4. full repository regression;
5. static/lint/type/diff checks.

No provider or Railway call.
