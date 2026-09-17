# AISCC Handoff — Ingress DB boundary accepted → Git persistence

Accepted exact source:

```text
migrations/versions/20260917_0021_public_live_ingress_authority.py
ee73171fe07536bc12535e84ed00c8f23cb23e8dce9d08f88464f93b928384b1

src/aiscc/public_live/ingress.py
4df5770e759cb268eef3600bacb05e15854b35fc36ee6a3f7ba64d735ccdbf02

tests/integration/public_live/test_ingress_authority.py
a437d2e1a0d1e4662e2096032249a0942ed57f6e6cde45d5c18645bcf1b88675
```

Persist these bytes plus the accumulated unpersisted 1612 / 1652 / 2112 / current Browser governance.

Do not rerun tests and do not access Railway.

After persistence, hosted ingress deployment becomes the next candidate phase.
