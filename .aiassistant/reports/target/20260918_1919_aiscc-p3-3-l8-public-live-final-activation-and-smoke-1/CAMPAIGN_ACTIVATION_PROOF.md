# Campaign Activation Proof

The campaign was inserted once while control was disabled. Canonical digests were derived at execution time from `StartContract.load().digest` and `hosted_luna_profile().public_repository_version`.

## Immutable campaign pins

- campaign: `public-live-v1`
- starts at, DB clock: `2026-09-18T10:53:56.287991+00:00`
- exclusive cutoff: `2026-10-17T15:00:00+00:00`
- limit: 15,000,000 micro-USD
- HMAC version: `v1`
- scenario: `stockroom-s1-normal / 1.0.0`
- content digest: `be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d`
- policy digest: `63c4238ff9691c9a463c72199e38466bbf6ce5db4565c2691e6e2c933995bf1a`

## Final retained accounting

- available: 14,800,000 micro-USD
- held: 200,000 micro-USD
- settled: 0
- control enabled: false
- active campaign: `public-live-v1`
- incident: null

The held reservation and occupied slot belong to the preserved failed smoke evidence. They were not deleted or rewritten during rollback.
