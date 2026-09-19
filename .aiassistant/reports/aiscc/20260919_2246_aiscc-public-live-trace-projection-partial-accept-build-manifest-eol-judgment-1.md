# Browser Command Center Judgment

## 판정

```text
PARTIAL_ACCEPT
/
SAFE_PUBLIC_TRACE_PROJECTION_ACCEPTED
/
LIVE_TRACE_UI_SOURCE_ACCEPTED
/
PUBLIC_REPLAY_BUILD_MANIFEST_CANONICAL_EOL_DRIFT
/
NARROW_REWORK_REQUIRED
/
HUMAN_QA_HOLD
```

## integrity

Result ZIP SHA-256:

`491f9255d75e7c75e6b7a09ebaa25795f6323e196e96c72438923d97818e85fd`

Issued/result Task identity:

`BYTE_IDENTICAL`

Task SHA-256:

`f78ca3f7aa68d5af2c7c5f8d3e801a393ec5cff6064807acee6226cd9cd9f30e`

Implementation changed Git blobs:

`10/10 BYTE_EXACT`

## accepted implementation

The following are accepted and must not be reopened without new evidence:

- migration 0028 safe projection design;
- capability-scoped read integration;
- fixed instruction projection;
- provider/tool trace projection;
- Stockroom fixed-result proof gate;
- strict frontend trace schema;
- Replay-style Live trace rendering;
- Human-decision boundary;
- no raw provider/private protocol exposure;
- no provider/worker/admission/reconciliation source changes.

## blocking defect

The committed public build manifest was generated from CRLF working-tree bytes for two authored static files.

Manifest currently claims:

```text
_headers            484 bytes
live-config.json    158 bytes
```

Git canonical blobs are:

```text
_headers            477 bytes
live-config.json    153 bytes
```

Canonical Git SHA-256 values:

```text
_headers
fd3158e83462fb5db5ed3b17328bc39e5baae132e2e3f62fd01989fe9a1a7b64

live-config.json
9a14186fe2179374e25d6c198f34db2d5338cc13307558f8e2c2ef6c9c30d676
```

The committed manifest therefore cannot be reproduced from a clean canonical LF checkout.

## severity

This is not a Public Live security/runtime failure.

Do NOT:
- disable control;
- rollback 0028;
- rollback the trace UI;
- create a new run;
- call the provider.

Public Live remains released.

But Human trace QA must wait because accepting the visual result before canonical artifact provenance is repaired would leave the competition artifact internally inconsistent.

## required repair

Make authored public Replay text assets deterministic across Windows/Linux checkout.

Preferred narrow repair:

1. add/adjust Git EOL policy so the public Replay authored text assets use LF in the working tree;
2. regenerate `PUBLIC_REPLAY_BUILD_MANIFEST.json` from LF canonical bytes;
3. prove a clean/canonical checkout produces the same manifest;
4. deploy the corrected exact frontend artifact if required to align deployed bytes;
5. no backend migration or ingress change.

Do not solve this by teaching the manifest to describe CRLF-only Windows bytes.

## post-rework target

```text
TRACE_IMPLEMENTED_DEPLOYED
/
CANONICAL_PUBLIC_BUILD_REPRODUCIBLE
/
PUBLIC_LIVE_RELEASED
/
HUMAN_TRACE_QA_PENDING
/
BROWSER_REVIEW_REQUIRED
```
