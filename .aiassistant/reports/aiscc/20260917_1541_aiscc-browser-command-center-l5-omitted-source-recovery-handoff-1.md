# AISCC Handoff — Omitted source recovery

Do not restore these two files:

```text
src/aiscc/public_live/luna_profile.py
src/aiscc/public_live/provider_authority.py
```

They were created/changed during the 1030 narrow rework but omitted from its SOURCE_INVENTORY/export.

Current exact candidate hashes:

```text
luna_profile.py
e7dfbf5fac42b8fdff4766a7e09a8a4c1cda6a52cf6e4a3c0827d0fbb30196cb

provider_authority.py
98f3e83662a410e1dae15e7dfe487bb15830f4be80920031c8bf12b43b5e5d0d
```

Next action is narrow exact-byte validation only.

No Railway.
No Git staging/commit/push.
No full regression.
