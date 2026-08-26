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

- current Browser Project active authority: immutable `AISCC-BOOTSTRAP-SEED-V1` `14/14`
- repository canonical candidate: created by P0-4 rework
- first tracked mirror manifest: `NOT_CREATED`
- first generated mirror bundle: `NOT_CREATED`
- Browser complete active-set replacement: `NOT_EXECUTED / HUMAN_PENDING`
- source mirror sync status: `NOT_STARTED`

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
| none | none | pending P0-4 accepted commit | `NOT_CREATED` | `NOT_STARTED` |

Seed v1 and mirror v1 must never remain as mixed current authority.
