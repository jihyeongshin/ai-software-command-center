# AISCC Browser Command Center Judgment

## judgment

```text
Railway repo/main selection:
HUMAN_PROVIDED / STAGED

Railway source deploy:
HOLD

reason:
EXACT_DEPLOYMENT_ENTRYPOINT_AND_HEALTH_CONTRACT_NOT_YET_PROVEN

executor_fault:
NO

Public admission:
DISABLED

Public Live:
NOT_RELEASED
```

## required proof before Railway Deploy

The repository must establish exact current behavior for:

1. production HTTP server entrypoint;
2. Railway `$PORT` / `0.0.0.0` binding;
3. side-effect-free health/readiness path;
4. PostgreSQL runtime variable/binding contract;
5. Alembic migration execution point;
6. missing OpenAI secret startup behavior;
7. no provider call during startup/health;
8. exact Railway UI values to configure before first deploy.

Do not guess these values in the Browser UI.

## current Human instruction

Leave the current Railway `Repo + Branch` staged changes unapplied.

Do not enter the OpenAI key.

Do not modify Postgres Public Access.
