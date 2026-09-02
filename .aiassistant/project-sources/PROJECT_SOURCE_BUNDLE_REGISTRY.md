# AISCC Project Source Bundle Registry

## authority

```text
repository local canonical
= editable source owner after P0-4 acceptance

generated Project Source bundle
= ignored transport artifact generated from a tracked manifest

Browser Project Source
= Human-uploaded read-only mirror
```

Browser Project Source에서 직접 수정한 body는 canonical change가 아니다.

## current state

- Bootstrap Seed v1: `RETIRED / ACTIVE 0`
- current Browser Project active authority: `AISCC-PROJECT-SOURCE-MIRROR-V2 / ACTIVE / HUMAN_SYNC_CONFIRMED / 22`
- active Browser source count: `22`
- v1: `AISCC-PROJECT-SOURCE-MIRROR-V1 / RETIRED / HISTORICAL / previous active count 18`
- v1 canonical commit: `0dc4e19a6da31c22e08d144eaba24209a4476b4d`
- repository terminal canonical: `b9ed57feb595b3a670b644a213c184f958956924`
- v2 candidate commit: `2b156d8b2a43d1b908bca6aaf740eba4061fd4a1`
- v2 snapshot canonical commit: `b9ed57feb595b3a670b644a213c184f958956924`
- v2: `AISCC-PROJECT-SOURCE-MIRROR-V2 / ACTIVE / HUMAN_SYNC_CONFIRMED / 22`
- v2 Browser sync: `HUMAN_PROVIDED / CONFIRMED`
- source mirror current Browser authority: `AISCC-PROJECT-SOURCE-MIRROR-V2`

## ownership boundary

`P0-5 First Project Source Mirror v1` exclusively owns:

1. tracked manifest generation under `.aiassistant/project-sources/manifests/`;
2. ignored generated bundle under `.aiassistant/project-sources/bundles/`;
3. canonical-path, filename, file-count, SHA-256, and body mapping verification;
4. Command Center review;
5. Human complete replacement of the Browser Project active set;
6. retirement of Seed v1 only after replacement confirmation.

P0-4 does not generate a P0-5 manifest or bundle and does not upload, remove, or partially replace Browser Project Source files.

## registered bundles

| bundle_id | manifest | canonical_commit | status | browser_sync |
|---|---|---|---|---|
| `AISCC-PROJECT-SOURCE-MIRROR-V1` | `.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v1.json` | `0dc4e19a6da31c22e08d144eaba24209a4476b4d` | `RETIRED / HISTORICAL / previous active count 18` | `HISTORICAL / PREVIOUSLY_CONFIRMED` |
| `AISCC-PROJECT-SOURCE-MIRROR-V2` | `.aiassistant/project-sources/manifests/aiscc-project-source-mirror-v2.json` | `b9ed57feb595b3a670b644a213c184f958956924` | `ACTIVE / HUMAN_SYNC_CONFIRMED / 22` | `HUMAN_PROVIDED / CONFIRMED` |

Seed v1 and mirror v1 must never remain as mixed current authority.
V1 is retired and historical. V2 is the current Browser authority after Human-confirmed complete replacement.
