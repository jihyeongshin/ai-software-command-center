# Stockroom runtime image build contract

Cut A defines source only. The final Stockroom image ID is born only in Cut B.
No image build, pull, execution, canonical provenance issuance, persistent database
provisioning or S1 execution is authorized by this document.

The base pin is the accepted repository distribution identity:
`python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579`.
The previously observed base local config ID has the same hexadecimal payload;
it is a different semantic identity and is not the pin authority.

The historical source aggregate is
`be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d`.
It identifies 14 source files, not an image. Read the exact resource inventory in
`config/scenarios/stockroom/v1/resource.json`.

The future assembler must use `TASK_SCOPED_GIT_OBJECT_ASSEMBLED_EXACT_CONTEXT`:
read Git objects at commit `05185c57a6265a4002050ce25cdfde3dc87e9779`,
subroot `examples/synthetic-stockroom/`, subtree
`f3d9203321ae3535abf8e92a7285da1067f6c55e`. Verify every resource member's
path, mode, size and SHA-256 and the aggregate before writing its bytes under
`source/`. Reject extra members. Do not select source from the mutable worktree.

The context has exactly 16 files: the accepted Dockerfile, `.dockerignore`, and
`source/<14 resource members>`. Dockerfile, `.dockerignore`, and this document
are excluded from the historical resource aggregate. The ignore file is only a
second defense; the assembler owns source selection.

The sole build argument `AISCC_DOCKERFILE_SHA256` must be the SHA-256 of the exact
Dockerfile bytes. It is non-secret immutable build metadata, not a credential.
The pinned Python 3.12.14 base needs no package installation or network build step.
Only historical source is copied to `/opt/aiscc/stockroom-provenance/source/`;
runtime mounts the separately admitted workspace at `/workspace`, read-only,
and uses user/group `65532:65532` with network `none`.

After a separately authorized build, Cut B must observe the final local image
config ID, required labels and selected inspect projection. This does not promise
bit-for-bit reproducible OCI manifests. Required labels and their exact values
are owned by `src/aiscc/runtime/stockroom_image.py`.

The future canonical JSON is
`.aiassistant/records/aiscc/runtime/stockroom-image-provenance.v1.json`.
It is absent in Cut A. Its strict schema, sorted-key compact Unicode JSON
fingerprint, whole-file SHA-256, accepted issuance references, source/build
bindings and inspect projection must all agree with the typed reference.
The document must not embed its own fingerprint. Production fails closed until
this canonical provenance exists and is admitted by the fixed source resolver.
Static v2 configuration and mutable discovery tags never supply image authority.
