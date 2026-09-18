# AISCC Browser Command Center Handoff — ingress composition accepted / hosted deploy

## canonical baseline

- GitHub main: `dd858cad5c7a40cc4f3968a122762b8415b40403`
- L3-L7: ACCEPTED / CLOSED
- L8: IN_PROGRESS
- ingress AdmissionService source composition: ACCEPTED
- Public admission: DISABLED
- Public Live: NOT_RELEASED
- real provider calls: 0

## next objective

Get the accepted ingress source onto the hosted ingress service and re-attest the current hosted DB/authority state without opening a public release path.

Expected safe end state:
- hosted ingress deployment healthy/private;
- DB head and ingress role known;
- control still disabled;
- public domain absent;
- edge-trust absent;
- no provider secret on ingress;
- Replay unchanged.

Campaign state is observation-only in this Task. If absent, report absent. If present, report only safe non-secret identity/digest-match facts. Do not create or modify campaign rows.
