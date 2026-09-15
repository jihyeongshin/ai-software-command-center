# AISCC Browser Command Center Handoff — accepted shared-limit policy → L3 retry

## current repository

```text
branch:
main

HEAD:
968a7164cb50cfeaee5a6f83b7455ab87f6ccbd1
```

## Human-approved amendment

Canonical accepted policy:

`.aiassistant/reports/aiscc/20260916_0135_aiscc-p3-3-public-live-shared-limit-policy-amendment-v1-accepted.md`

Status:

`HUMAN_PROVIDED / ACCEPTED`

The 0133 proposal is historical provenance only.

## exact accepted limits

```text
authenticated run GET:
30 / fixed 60s DB-clock bucket / run

source flood:
120 / fixed 60s DB-clock bucket / opaque canonical source bucket

campaign flood:
1200 / fixed 60s DB-clock bucket / campaign
```

All Public Live ingress under `/v1/public-live/*` consumes both flood dimensions before expensive request processing.

Invalid capability reads consume flood quota but not authenticated run-read quota.

## source identity boundary

- IPv4 `/32`
- IPv6 `/64`
- campaign-bound HMAC-SHA256 opaque bucket
- no raw IP persisted/logged
- raw forwarding headers are not authority
- hosted trusted-proxy derivation remains L5 proof

L3 may prove a local/server-owned normalized source identity adapter. It MUST NOT claim L5 hosted proxy proof.

## next Executor objective

One turn:

```text
shared PostgreSQL limiter
→ migration/security/concurrency proof
→ L3 HTTP composition
→ L3 HTTP/security/regression proof
```

Do not stop after the limiter prerequisite passes.

## release boundary

- provider calls = 0
- Public admission remains disabled
- no deployment
- no Git commit/push
- L4/L5/L6+ remain out of scope
