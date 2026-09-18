# AISCC Browser Command Center Handoff — L7 narrow release-label rework

## baseline

- GitHub main: `6950fe9047dbff9d0752fd63958e359a48414f0b`
- L6: `ACCEPTED / CLOSED`
- L7: `SOURCE CANDIDATE / NARROW REWORK REQUIRED`
- Public admission: `DISABLED`
- Public Live: `NOT_RELEASED`
- deployed Replay: unchanged
- real provider calls: `0`

## what remains accepted

Keep the 0856 frontend implementation and automated evidence intact unless directly affected.

There is one Browser-found source defect: an unconditional top-level `Live Demo is not enabled` notice remains visible even when the later exact enabled config would make the bounded Live Start control available.

## rework principle

The UI must never simultaneously communicate both:
- `Live is not enabled`, and
- `Live is configured/startable`.

Fix only that truthfulness boundary.

Do not choose a Railway API origin and do not deploy.

Human physical browser QA remains pending after source rework.
