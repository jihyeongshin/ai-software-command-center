# AISCC Browser Command Center Handoff — 0102 readiness blocked → reconciler ACL compatibility

## baseline

`6e6c2198a2034664ee8ff9d85d9e78a52fa403c9`

## accepted facts

- 2344 retained 1919 settlement remains accepted and closed.
- 0102 read-only preflight is accepted as a correct stop.
- Public Live remains `NOT_RELEASED`.
- Replay remains public.
- ingress/worker domains remain 0.
- accepted fixed-tool worker deployment is unchanged.

## blocker

General hosted reconciliation is not release-ready.

`ReconciliationService` performs terminal reconciliation through the reconciler repository but calls compatibility functions whose canonical EXECUTE grants currently belong only to the runtime role.

The one-run 2344 operator adapter does not count as a permanent repair.

Fresh hosted DB readiness evidence also needs a safe operator transport path.

## next action

Repair the exact ACL compatibility boundary with least privilege, apply it through the existing migration/deployment authority, then freshly reprove settlement durability and release readiness.

One ephemeral Railway SSH key may be created solely for this Task's operator transport if needed. It must be deleted from Railway and local disk before final submission.

No Public Live release, provider call, public run, Cloudflare release, or permanent access credential is authorized.
