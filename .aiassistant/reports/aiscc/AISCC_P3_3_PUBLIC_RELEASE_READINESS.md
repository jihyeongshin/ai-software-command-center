# P3-3 public release readiness

## Current post-submission readiness (20260915_1527)

Competition final submission: HUMAN_PROVIDED / COMPLETED. P3-3: SUBMITTED / POST_SUBMISSION_IMPROVEMENT_WINDOW, not CLOSED.
Public Replay remains DEPLOYED / PUBLIC_VERIFICATION_PASSED / HUMAN_ACCEPTED at https://aiscc-replay.pages.dev; technical R01/R02 and Human production QA remain resolved. Human rights/source/synthetic rights, license/assets, private-material exclusion, hosting terms and actual tool disclosures are CONFIRMED under the 1527 Task authority. Actual Wanted form review and Human final submit are complete; source repository publication is not a required submission field.

Remaining work is operational: select any separately authorized pre-deadline improvement, preserve Replay, re-review materially changed submitted experience before 2026-09-20, then freeze and monitor availability through judging. Public Bounded Live remains NOT_RELEASED / DISABLED_FOR_INITIAL_RELEASE, an optional candidate only. No future uptime is claimed. Previous unresolved submission/disclosure projections below are historical and superseded by the admitted Human evidence; no independent legal finding or new QA was performed here.


## Current accepted public release (20260915_1424)

Public Replay: DEPLOYED / PUBLIC_VERIFICATION_PASSED / HUMAN_ACCEPTED at https://aiscc-replay.pages.dev. Cloudflare Pages project aiscc-replay, Dashboard Direct Upload, source commit `d13d261eb976fc839e78ba0878080bea93ad5201`. P3-3 remains ACTIVE / FINAL_SUBMISSION_PREP.

| Boundary | Accepted readiness |
| --- | --- |
| R01 Recorded Replay serving | READY_VERIFIED |
| R02 Cloudflare Pages deployment | READY_VERIFIED / DEPLOYED |
| Public byte identity | READY_VERIFIED; ten exact comparisons |
| Effective application headers | READY_VERIFIED |
| Public 404 | READY_VERIFIED |
| Human production QA | HUMAN_PROVIDED / ACCEPTED |
| Public Bounded Live | OPTIONAL_DEFERRED / DISABLED_FOR_INITIAL_RELEASE / NOT_RELEASED |

The 1424 Human acceptance lineage admits the 1358 Chromium-compatible verification and production QA. Earlier default-UA 1010 is diagnostic, not an application defect. R01/R02 are resolved; no code, redeployment or repeat visual QA is needed for unchanged bytes. All earlier technical blocker statements below retain historical meaning and are superseded by this section.

Remaining gates are Human project/source rights and release license, final notices/shipped dependency scope, exact development AI tool/model/use roster, applicable Cloudflare terms and other unresolved disclosure-register confirmations, final official schedule/form re-verification, and Human final submit. Existing synthetic-corpus provenance and private-material exclusion policy are reused evidence, not a project-wide Human legal attestation. Optional Live terms remain deferred. No rights answer is inferred. Competition final submission is NOT_COMPLETED; availability monitoring remains a future obligation.

## Current 1047 implementation candidate

Status: `IMPLEMENTATION_CANDIDATE / HUMAN_QA_PENDING`. Source baseline `17fcd337a8bc1410e230a7c18195ac3d3006b417`; no new commit or public deployment.

| Item | Current readiness / evidence |
| --- | --- |
| R01 standalone public Replay surface | READY_VERIFIED at local implementation scope: public/replay HTML/CSS/JS, five exact JSON copies, no owner runtime |
| R02 static output/deployment prerequisite | READY_VERIFIED at local implementation scope: deterministic builder/check, build manifest, health.json, _headers, deployment doc; actual Cloudflare settings remain pending |
| Hosting direction | ACCEPTED: Cloudflare Pages per AISCC-COMPETITION-DEPLOYMENT-DIRECTION-V1; not an open host selection |
| Build/check | PASS; `python scripts/build_public_replay.py`, same command with `--check`; corruption/drift tests pass |
| Local HTTP | PASS on 127.0.0.1 only; exact static bytes, genuine 404; server stopped |
| Public dependencies | No DB, owner API, provider, Railway, secret or external frontend assets |
| Corpus | Index plus four members byte-identical; canonical source unchanged |
| Live | OPTIONAL_DEFERRED / DISABLED_FOR_INITIAL_RELEASE; no active control or endpoint |
| Human visual QA | HUMAN_PENDING; required before persistence/deployment |
| R03 rights/tool disclosure | HUMAN_CONFIRMATION_REQUIRED; not resolved by code |
| Cloudflare account/project authorization | Human-owned later gate; exact configuration/URL not established |
| Public availability | NOT_COMPLETED; local evidence does not establish public deployment |

The 1009 claim that hosting selection remained open is corrected by the 1047 Browser authority. Railway Hobby / Singapore and a separate OpenAI API Project are accepted optional Live directions, NOT_EXECUTED and outside this static artifact.

Source-supported deployment instructions are in `docs/AISCC_PUBLIC_REPLAY_DEPLOYMENT.md`. The deployment unit is only `public/replay`. Manifest source_commit is the entering baseline, explicitly not a fabricated final deployment commit. Human QA → exact persistence → bounded Cloudflare Pages deployment → public header/404/data/availability verification → Human final submit is the remaining sequence.

No deployment, P3-3 closure or final submission is claimed. Official dates, judging availability obligations and claim limits below remain applicable. Earlier technical missing-surface findings are superseded only by this local candidate evidence, not by public availability evidence.

## Historical 1009 blocker record — superseded technical projection

Status: `BLOCKED_RELEASE_PREREQUISITE`. Human review remains pending.
Source: `main` at `17fcd337a8bc1410e230a7c18195ac3d3006b417`.
Task: `20260915_1009_aiscc-p3-3-replay-first-public-release-readiness-and-submission-package-freeze-1`.

This is a bounded blocker record, not a completed release freeze. The Task's mandatory stop applies because providing the missing public Replay surface requires a separately authorized product/deployment implementation. No such implementation was performed. Remaining discovery and canonical state reconciliation were stopped.

## Competition fact snapshot

Browser-supplied facts, reverified 2026-09-15 in the 1009 Task/Cycle: registration deadline 2026-09-18 23:59:59 KST; final submission deadline 2026-09-20 23:59:59 KST; judging/voting 2026-09-21 through 2026-10-05. An implemented/deployed service link, problem description, AI usage and major AI tools disclosure are required. Temporary save is not final submission. The service must remain reachable during judging. Submission edits close after the deadline. Human must recheck official facts immediately before final submission. No external verification was performed in this turn.

## Public surface and topology findings

| Item | Classification | Current-source evidence |
| --- | --- | --- |
| Python package/CLI | READY_VERIFIED | `pyproject.toml`: Python >=3.12,<3.13, Hatchling, `aiscc = aiscc.__main__:main` |
| Local CLI syntax | READY_VERIFIED | `src/aiscc/__main__.py`: `aiscc serve --host 127.0.0.1 --port 8000`; source-verified syntax only, not executed or deployment-ready |
| Public build/deploy command | BLOCKED_REQUIRED | No public release target or build script established; do not infer one from the package manifest |
| Existing Command Center UI | BLOCKED_REQUIRED for public release | `src/aiscc/command_center/web.py:18` emits `X-AISCC-Exposure: LOCAL_PRIVATE_ONLY`; landing copy is local/private/read-only |
| UI routes | READY_VERIFIED as local source | `src/aiscc/api/routes/command_center_ui.py`: `/command-center`, projects, work-runs, cycles, app.css and app.js |
| Read API | READY_VERIFIED as local source | `src/aiscc/api/routes/command_center.py`: `/v1/command-center` queue, work-run, transitions, execution, evidence, human-judgment, outcomes, Cycle and NextAction views |
| Default composition | BLOCKED_REQUIRED for public corpus | `src/aiscc/api/app.py:24`: `AISCC_DATABASE_URL` selects PostgreSQL queries; otherwise unavailable queries. No canonical Replay corpus composition |
| Health | READY_VERIFIED as liveness source only | `src/aiscc/api/routes/health.py`: `/health`; does not check Replay readiness |
| Container assets | NOT_APPLICABLE as public deployment | `containers/p1_3/compose.yaml`, `Dockerfile.evidence`, `Dockerfile.sandbox` serve evidence/sandbox fixtures; no public application target established |
| Hosting platform/public endpoint | BLOCKED_REQUIRED | Not established by inspected current release assets; no provider selected or endpoint guessed |

## Recorded Replay deployability

| Requirement | Classification | Evidence / gap |
| --- | --- | --- |
| Persisted four-member corpus | READY_VERIFIED | `.aiassistant/reports/aiscc/replay/stockroom/v1/REPLAY_CORPUS_INDEX.json`; four member hashes/sizes match |
| Recorded provenance | READY_VERIFIED | Index preserves scenario, recorded timestamp, execution commit and run fingerprint; corpus root `a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e` |
| Sanitization/IP admission | READY_VERIFIED within reused P2 evidence | Accepted truth map PUB-009 and current P2 record; no new legal attestation or public deployment test |
| Read-only/no-inference corpus labels | READY_VERIFIED as stored data | `live=false`, Recorded Run Replay and no-inference notices in index |
| Public viewer/corpus adapter | BLOCKED_REQUIRED | App composition/routes do not load the canonical corpus; existing UI is explicitly private |
| Public read-only isolation / recorded labels / fallback | BLOCKED_REQUIRED | Must be verified on the future public surface, separately from local owner projections |
| Public availability | BLOCKED_REQUIRED | Public Replay deployment remains NOT_COMPLETED |

`ReplayExecutionService` in `src/aiscc/providers/service.py:1458` is a supplied-dictionary service with missing/corrupt-record errors. Its existence does not connect the canonical corpus to public UI/API or prove deployed availability.

## Public data and security boundary

Only the accepted sanitized corpus and explicitly reviewed public assets may enter a future release. Do not publish the repository root, owner database, private source, raw evidence bodies, host paths, environment files or credentials. Existing local/private Command Center must not be relabeled or exposed as the public Replay service without a new scoped implementation and review.

## Live guard matrix

Classification: `DISABLED_FOR_INITIAL_RELEASE`. Missing optional Live guards do not cause the Replay blocker.

| Required guard | Classification | Evidence limit |
| --- | --- | --- |
| Fixed synthetic repository and scenario allowlist | OPTIONAL_DEFERRED | Public profile names fixed synthetic contexts; complete release binding not established |
| No free-form task, external repository/upload, arbitrary shell/network | OPTIONAL_DEFERRED | Accepted security policy; no released public execution ingress established |
| Public/private permission separation | OPTIONAL_DEFERRED | Separate modes in permission-profiles.v1.toml; deployment isolation unverified |
| Server-fixed real provider/model | OPTIONAL_DEFERRED | provider-profiles.v1.toml is acceptance-only, local deterministic fake |
| Calls/retries/time/tokens | OPTIONAL_DEFERRED | Fake profile contains finite limits; not evidence of actual public provider readiness |
| Daily/global/currency budgets | OPTIONAL_DEFERRED | limits.v1.toml has budget_units, not a proven release spend configuration |
| Provider hard spend or compensating control | OPTIONAL_DEFERRED | Not evidenced; no provider account inspected |
| Fail-closed availability/budget admission | OPTIONAL_DEFERRED | Release composition not established |
| Truthful errors and independent Replay fallback | OPTIONAL_DEFERRED | Public UI/API behavior unverified |
| Secret/context isolation, abuse/throttling/idempotency | OPTIONAL_DEFERRED | Public deployment controls not established before stop |

Required future disabled behavior: do not register a Live execution ingress or provision provider credentials; no active Start Live control; label "Live Demo is not enabled. Recorded Run Replay remains available." Unknown/Live execution requests must fail without starting work. Exact public route/status contract must be specified in the next implementation Task; none is invented here.

## Blockers, credentials, recovery and minimum release path

- `R01 / BLOCKED_REQUIRED`: public Replay viewer and immutable corpus composition missing from current application surfaces.
- `R02 / BLOCKED_REQUIRED`: public deployment target/config/build and Replay-aware readiness are not established.
- `R03 / BLOCKED_REQUIRED`: final project ownership/license, transitive dependency notices and provider/tool disclosure remain incomplete at the stop boundary.
- `OPTIONAL_DEFERRED`: Live release guards. Keep Live disabled.
- Hosting credentials, domain ownership, legal/IP confirmation and final deployment/submission approval are Human-owned. Credential availability alone cannot make R01/R02 ready.

Next Task recommendation: **P3-3 public Recorded Replay serving and deployment prerequisite implementation**. Require explicit source/config allowlist; serve only the exact accepted corpus; preserve hashes, timestamps and admission provenance; exclude owner DB access and provider calls; implement truthful recorded/error labels and Live-disabled behavior; select/freeze hosting/build/start/health configuration; complete rights/notices. Do not mix final submission with implementation.

Only after those prerequisites pass should a deployment Task receive exact target credentials and authorization. Its verification must cover public HTTPS access, four records, integrity and safe content, read-only routes, no inference, missing/corrupt-data errors, Live-disabled behavior, restart/rollback and recovery. Roll back to a previously verified immutable public artifact; never use owner runtime or hidden Live as fallback.

Human should assign availability monitoring and recovery ownership for 2026-09-21 through 2026-10-05 and the accepted operational horizon through 2026-10-17. None of these operational obligations is completed by this record. P3-3 is not closed.
