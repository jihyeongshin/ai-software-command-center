# AISCC P3-1 M05 Result Candidate → Trace Conformance Rework Handoff

## current state

```text
protocol:
HUMAN_PROVIDED / ACCEPTED
SHA-256: a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6

M01-M04:
EX_SOURCE_MISSING / NOT_COMPARABLE

M05 predecessor result:
RESULT_CANDIDATE / HUMAN_PENDING

Browser judgment:
HOLD_REWORK_REQUIRED
cause:
EXPORT_ARTIFACT_INCOMPLETE
```

## defect boundary

The defect is not the comparative methodology and is not a source-integrity failure.

It is a result-artifact provenance defect:

- emitted comparator traces omit most actual consulted/reference sources;
- multiple step refs are empty;
- per-field hashes required by protocol are absent;
- metric artifact-count claims do not reconcile with the emitted traces.

## rework boundary

Use the exact predecessor:

- protocol SHA `a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6`
- frozen source manifest tuple SHA `cdff08aa196d828db03ebacbdbefb05c1431b0e5b2bad3247c7c5db5d1a18cb9`
- same M05 source archive/task/commit identities
- same M01-M04 exclusions

Do not reopen source discovery, modify the protocol, rerun P2, or add a scenario.

Results have already been viewed. Therefore no protocol amendment or post-hoc threshold change is allowed.

## expected result

A corrected result bundle where:

```text
trace -> exact consulted fields + hashes
trace-derived counts -> RAW_METRICS
metric provenance -> resolvable to trace/source manifest
independent regeneration -> byte-identical
```

If the corrected trace still produces the same decisions/metrics, preserve them and submit them again as `RESULT_CANDIDATE / HUMAN_PENDING`.

If a mechanical evaluator defect changes a result value, report exact before/after value, code defect, frozen source evidence and why the correction follows the already-accepted protocol. Do not silently overwrite it.
