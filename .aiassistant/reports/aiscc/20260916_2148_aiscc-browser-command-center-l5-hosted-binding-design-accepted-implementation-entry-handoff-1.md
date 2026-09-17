# AISCC Handoff — Hosted binding design accepted → local implementation

## accepted decision

`A — ACCEPT_APPLICATION_MEDIATED_EGRESS`

## accepted design identity

```text
source HEAD:
96a4029ec3a82c9b2a88b9718732aa0f00ecad20

predecessor design result ZIP SHA:
4b40a040e9ec764926dedd1a46e09d93fb0472694baddae49ccfcea7b35d9b0a

design:
HOSTED_PUBLIC_LIVE_BINDING_DESIGN
ACCEPTED / CLOSED
```

## next boundary

Implement only the local source/test/package/runtime pieces needed to realize the accepted C topology and hosted L5 proof machinery.

Do not create Railway resources, domains, databases, secrets, Edge Rules, Cloudflare changes, provider calls, commits or pushes.

Public admission remains disabled and Public Live remains not released.
