FROM python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579
ARG AISCC_DOCKERFILE_SHA256
LABEL io.aiscc.stockroom.build-contract="AISCC-STOCKROOM-RUNTIME-BUILD-V1"
LABEL io.aiscc.stockroom.source-commit="05185c57a6265a4002050ce25cdfde3dc87e9779"
LABEL io.aiscc.stockroom.source-subroot="examples/synthetic-stockroom/"
LABEL io.aiscc.stockroom.git-subtree="f3d9203321ae3535abf8e92a7285da1067f6c55e"
LABEL io.aiscc.stockroom.resource-ref="repository:synthetic-stockroom@be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d"
LABEL io.aiscc.stockroom.source-aggregate="be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d"
LABEL io.aiscc.stockroom.source-file-count="14"
LABEL io.aiscc.stockroom.python-version="3.12.14"
LABEL io.aiscc.stockroom.dockerfile-sha256="${AISCC_DOCKERFILE_SHA256}"
LABEL io.aiscc.stockroom.base-repodigest="python@sha256:0f5b26b9518d002b6173fd61daad821fa340635ebfec5bba471013f9ca114579"
COPY source/ /opt/aiscc/stockroom-provenance/source/
WORKDIR /workspace
USER 65532:65532
