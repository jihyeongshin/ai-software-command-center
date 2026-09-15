# AISCC Public Documentation Truth Map

## Document status

- document_id: `AISCC-P3-2-PUBLIC-DOCUMENTATION-TRUTH-MAP-V1`
- task_id: `20260915_0310_aiscc-p3-2-public-repository-truth-map-readme-and-comparative-summary-1`
- status: `DOCUMENTATION_CANDIDATE / HUMAN_PENDING`
- purpose: claim-control source for the root README and public comparative summary
- claim_count: `19`
- authority rule: later terminal Cycle/Judgment overrides older embedded phase snapshots; repository-local canonical source overrides a stale mirror

Public wording must stay within each entry's `allowed_extension`. A file's existence is not runtime proof, documentation is not implementation, and an Executor draft is not Human acceptance.

## Claim register

### `PUB-001` — product thesis and category

- topic: product thesis/category
- public_wording: AISCC is a software engineering governance control plane for AI-assisted work. It connects Task scope, evidence admission, system-owned state transitions, Judgment, curated Cycle provenance, and Next Action.
- classification: `ACCEPTED_PROJECT_DECISION`
- current_status: `CANONICAL / ACCEPTED`
- evidence_owner: Product Thesis / Human-accepted project governance
- canonical_source_paths: `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`; `.aiassistant/rules/AISCC_ARCHITECTURE.md`
- exact_supporting_artifact_hash_or_commit: Product Thesis SHA-256 `359d46cfddb10cb9efd85046383b9405869fe2a74f4e66637032915a802eeeb0`; Architecture SHA-256 `490e7fd09edc1d7d7a32357c219dc37274f32ca769261910e7274a8fc111492e`
- allowed_extension: explain AISCC as governance around coding agents and software work
- forbidden_extension: describe AISCC as a foundation model, unrestricted agent swarm, or proof of product superiority
- freshness_or_release_note: category decision is accepted; public deployment is a separate status
- target_surface: `README`

### `PUB-002` — authority drift problem

- topic: authority drift/problem statement
- public_wording: Long-running AI-assisted projects can lose track of which Task, policy, source state, and decision currently has authority.
- classification: `ACCEPTED_PROJECT_DECISION`
- current_status: `CANONICAL / ACCEPTED`
- evidence_owner: Product Thesis
- canonical_source_paths: `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`; `.aiassistant/rules/AISCC_AGENTS.md`
- exact_supporting_artifact_hash_or_commit: Product Thesis SHA-256 `359d46cfddb10cb9efd85046383b9405869fe2a74f4e66637032915a802eeeb0`
- allowed_extension: describe the governance problem and the repository authority model
- forbidden_extension: state that AISCC eliminates all authority ambiguity
- freshness_or_release_note: problem framing, not an effectiveness measurement
- target_surface: `README`

### `PUB-003` — task-scoped evidence ownership

- topic: task-scoped evidence ownership
- public_wording: A Task can separate executor-required, reusable, Human-owned, unnecessary, and forbidden evidence before execution.
- classification: `IMPLEMENTED_GOVERNANCE_MODEL / EVIDENCED_IN_ACCEPTED_RUNS`
- current_status: `IMPLEMENTED / BOUNDED_EVIDENCE`
- evidence_owner: TaskContract and evidence authorities
- canonical_source_paths: `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`; `.aiassistant/rules/AISCC_ORCHESTRATION.md`; `.aiassistant/records/aiscc/cycles/20260915_0310_aiscc-p3-1-comparative-evaluation-final-acceptance-p3-2-entry-authorization-1.cycle.md`
- exact_supporting_artifact_hash_or_commit: terminal Cycle SHA-256 `6a7011c0cd144e31879e709c9b2138a2b07c7e27cacde1b53c1542242ed87e1b`
- allowed_extension: explain the ownership classes and their role in admission
- forbidden_extension: imply that a producer may self-admit its evidence
- freshness_or_release_note: evidenced in bounded repository-local workflows; no general reliability claim
- target_surface: `README`

### `PUB-004` — proof non-substitution

- topic: proof non-substitution
- public_wording: Static source, tests, runtime observations, Browser checks, and Human decisions are distinct proof channels and are not silently interchangeable.
- classification: `ACCEPTED_GOVERNANCE_INVARIANT`
- current_status: `IMPLEMENTED / EVIDENCED_IN_BOUNDED_SCOPE`
- evidence_owner: AISCC evidence and transition authorities
- canonical_source_paths: `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`; `.aiassistant/rules/AISCC_ORCHESTRATION.md`; `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- exact_supporting_artifact_hash_or_commit: Orchestration SHA-256 `ef43a10af03f81cd6fa069d0f9e3e0b8f7c9516d7269b49ac3b2be2eef16db37`
- allowed_extension: explain why each gate names the proof type and owner it accepts
- forbidden_extension: use one proof class to claim completion of another
- freshness_or_release_note: invariant and bounded evidence do not establish security completeness
- target_surface: `README`

### `PUB-005` — Agent claim versus admitted evidence

- topic: Agent claim vs admitted evidence
- public_wording: Agent output is a proposal or evidence candidate; it becomes admitted evidence only through the applicable System-owned admission path.
- classification: `IMPLEMENTED_GOVERNANCE_INVARIANT`
- current_status: `IMPLEMENTED / GOLDEN_RUN_EVIDENCED`
- evidence_owner: Agent candidate producer and System evidence authority, separately
- canonical_source_paths: `.aiassistant/rules/AISCC_ARCHITECTURE.md`; `.aiassistant/tasks/done/20260914_2317_aiscc-p2-4-golden-agent-single-file-proof-change-4.md`; `.aiassistant/records/aiscc/cycles/20260914_2338_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-browser-accepted-state-reconciliation-entry-1.cycle.md`
- exact_supporting_artifact_hash_or_commit: golden result commit `ea34a0e08912d6259c74d0cb50ade9c9b9dba77e`; golden provenance root `b0be0299344375a74d9b9bdc7e7149aa949d98098e0a76bf9f81b13e86834e50`
- allowed_extension: state that the accepted golden chain preserved candidate/admitted separation
- forbidden_extension: treat an Agent completion statement as admitted truth
- freshness_or_release_note: one bounded accepted self-use lineage
- target_surface: `README`

### `PUB-006` — System-owned transition

- topic: System-owned transition
- public_wording: An Agent may request or propose a transition, but only the AISCC System owns transition evaluation, admission, and authoritative WorkRun state mutation.
- classification: `IMPLEMENTED_GOVERNANCE_INVARIANT`
- current_status: `IMPLEMENTED / ACCEPTED_BOUNDARY`
- evidence_owner: AISCC System transition authority
- canonical_source_paths: `.aiassistant/rules/AISCC_ARCHITECTURE.md`; `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- exact_supporting_artifact_hash_or_commit: Architecture SHA-256 `490e7fd09edc1d7d7a32357c219dc37274f32ca769261910e7274a8fc111492e`
- allowed_extension: distinguish TransitionRequest, TransitionDecision, Judgment, and WorkflowState
- forbidden_extension: imply that Agent prose mutates authoritative state
- freshness_or_release_note: implementation evidence is bounded to accepted project scenarios
- target_surface: `README`

### `PUB-007` — Human gate

- topic: Human gate
- public_wording: When a Task designates Human-owned proof or judgment, the System preserves a pending gate until the designated Human result is admitted.
- classification: `IMPLEMENTED_GOVERNANCE_INVARIANT`
- current_status: `IMPLEMENTED / ACCEPTED_BOUNDARY`
- evidence_owner: designated Human owns result content; System owns gate lifecycle and admission
- canonical_source_paths: `.aiassistant/rules/AISCC_ARCHITECTURE.md`; `.aiassistant/rules/AISCC_ORCHESTRATION.md`
- exact_supporting_artifact_hash_or_commit: Orchestration SHA-256 `ef43a10af03f81cd6fa069d0f9e3e0b8f7c9516d7269b49ac3b2be2eef16db37`
- allowed_extension: explain that HumanResult, Judgment, and transition are separate records
- forbidden_extension: state that the Executor completed Human review
- freshness_or_release_note: public wording acceptance for P3-2 remains `HUMAN_PENDING`
- target_surface: `README`

### `PUB-008` — curated Cycle and Next Action

- topic: curated Cycle/NextAction
- public_wording: Accepted Task, evidence, transition, Judgment, result, and continuation provenance can be admitted into a curated Cycle from which a stable Next Action is selected.
- classification: `IMPLEMENTED_GOVERNANCE_MODEL / GOLDEN_RUN_EVIDENCED`
- current_status: `IMPLEMENTED / BOUNDED_EVIDENCE`
- evidence_owner: Cycle admission and NextAction selection authorities
- canonical_source_paths: `.aiassistant/rules/AISCC_ARCHITECTURE.md`; `.aiassistant/records/aiscc/cycles/20260914_2338_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-browser-accepted-state-reconciliation-entry-1.cycle.md`
- exact_supporting_artifact_hash_or_commit: golden provenance root `b0be0299344375a74d9b9bdc7e7149aa949d98098e0a76bf9f81b13e86834e50`
- allowed_extension: describe Cycle as curated append-only provenance rather than raw chat memory
- forbidden_extension: present an Agent recommendation as the authoritative Next Action
- freshness_or_release_note: the accepted golden lineage ended in a `CYCLE_DERIVED` NextAction
- target_surface: `README`

### `PUB-009` — Recorded Replay corpus

- topic: P2 recorded Replay status
- public_wording: The repository contains a canonical, persisted, sanitized Recorded Replay corpus describing four previously executed workflows.
- classification: `PERSISTED_REPOSITORY_EVIDENCE`
- current_status: `CANONICAL / PERSISTED`
- evidence_owner: P2-3 Replay corpus and terminal project authority
- canonical_source_paths: `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`; `.aiassistant/reports/aiscc/replay/stockroom/v1/REPLAY_CORPUS_INDEX.json`
- exact_supporting_artifact_hash_or_commit: persistence commit `68017ed5f3d15c0512dbf04899c798352adee710`; corpus root `a870da635941d7149edbbef911e8b2d75ff6fe12e8ade80c09dddc9086df795e`; index SHA-256 `c92fb81c43cef9b1c379c2df8dac967aa55f4ddae73780d31f5d51c617aa38e0`
- allowed_extension: say that repository artifacts record previous runs and use no inference when read
- forbidden_extension: call repository artifact inspection a current Live execution
- freshness_or_release_note: persisted corpus status does not prove public deployment
- target_surface: `README`

### `PUB-010` — public Replay deployment

- topic: public Replay deployment status
- public_wording: Public Replay deployment is not completed.
- classification: `CURRENT_RELEASE_STATUS`
- current_status: `NOT_COMPLETED`
- evidence_owner: P3 release authority
- canonical_source_paths: `.aiassistant/records/aiscc/cycles/20260915_0310_aiscc-p3-1-comparative-evaluation-final-acceptance-p3-2-entry-authorization-1.cycle.md`; `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
- exact_supporting_artifact_hash_or_commit: terminal Cycle SHA-256 `6a7011c0cd144e31879e709c9b2138a2b07c7e27cacde1b53c1542242ed87e1b`
- allowed_extension: mark deployment as pending future release work
- forbidden_extension: provide a public URL or state that Replay is currently deployed
- freshness_or_release_note: P3-3 has not started
- target_surface: `README`

### `PUB-011` — public bounded Live

- topic: public bounded Live status
- public_wording: Public Bounded Live is not released. The accepted policy allows it only as an optional fixed-synthetic, allowlisted, bounded mode.
- classification: `CURRENT_RELEASE_STATUS + ACCEPTED_POLICY`
- current_status: `NOT_RELEASED`
- evidence_owner: P3 release authority and security policy
- canonical_source_paths: `.aiassistant/records/aiscc/cycles/20260915_0310_aiscc-p3-1-comparative-evaluation-final-acceptance-p3-2-entry-authorization-1.cycle.md`; `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`; `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`
- exact_supporting_artifact_hash_or_commit: Runtime Boundary SHA-256 `cc5237cd4c0adc7eba0927a36158807bd9c9e4e76b1d31e09525cdaffe093e73`
- allowed_extension: describe the intended deny-by-default boundary as policy
- forbidden_extension: imply a deployed service, general-purpose prompt, external repository upload, or arbitrary shell/network access
- freshness_or_release_note: release and deployment evidence remain future P3-3 work
- target_surface: `README`

### `PUB-012` — Self-Dogfooding golden run

- topic: Self-Dogfooding golden run
- public_wording: AISCC completed one accepted local self-use lineage that connected Genesis authority, a TaskContract, execution states, an exact repository edit, authenticated submission, admitted evidence, deterministic Judgment, an accepted WorkRun, a Cycle, a result commit, and a Cycle-derived Next Action.
- classification: `HUMAN_ACCEPTED_BOUNDED_RUNTIME_PROVENANCE`
- current_status: `ACCEPTED / CLOSED`
- evidence_owner: P2-4 owner chain and Browser/Human terminal authority
- canonical_source_paths: `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`; `.aiassistant/records/aiscc/cycles/20260914_2338_aiscc-p2-4-first-actual-self-dogfood-golden-cycle-browser-accepted-state-reconciliation-entry-1.cycle.md`; `docs/AISCC_SELF_DOGFOOD_GOLDEN_CYCLE.md`
- exact_supporting_artifact_hash_or_commit: result commit `ea34a0e08912d6259c74d0cb50ade9c9b9dba77e`; provenance root `b0be0299344375a74d9b9bdc7e7149aa949d98098e0a76bf9f81b13e86834e50`; governed file SHA-256 `7890b048be5e7c4a1c679c388b0d05267a63445a2c3558b88fce3fd8f518b368`
- allowed_extension: claim bounded actual use and inspectable provenance
- forbidden_extension: claim uniqueness, independent validation, general reliability, security completeness, or superiority
- freshness_or_release_note: local owner use is distinct from public runtime release
- target_surface: `README`

### `PUB-013` — P3-1 comparator definition

- topic: P3-1 comparator definition
- public_wording: P3-1 applied `AISCC_GOVERNED` and a conservative `EXECUTOR_REPORT_BASELINE` to the same frozen packet as `SYNTHETIC_ABLATION_ONLY`; the baseline was not a competitor product.
- classification: `HUMAN_PROVIDED / ACCEPTED_METHOD`
- current_status: `P3-1 ACCEPTED / CLOSED`
- evidence_owner: P3-1 Browser/Human authority
- canonical_source_paths: `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`; `.aiassistant/records/aiscc/cycles/20260915_0310_aiscc-p3-1-comparative-evaluation-final-acceptance-p3-2-entry-authorization-1.cycle.md`
- exact_supporting_artifact_hash_or_commit: protocol SHA-256 `a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6`; corrected result ZIP SHA-256 `2827c3b0a302caff4971090347134d3f9e37ab0e8d6cf5be4eae0fe706d42e48`
- allowed_extension: explain the same-packet logical-view comparison
- forbidden_extension: describe the baseline as a vendor, product, or industry benchmark
- freshness_or_release_note: terminal Cycle/Judgment supersedes the protocol file's embedded pre-acceptance status line
- target_surface: `README`, `docs/AISCC_COMPARATIVE_EVALUATION.md`

### `PUB-014` — M01-M04 exclusions

- topic: M01-M04 exclusions
- public_wording: M01-M04 were `EX_SOURCE_MISSING / NOT_COMPARABLE`; they were retained in the planned matrix and were not scored.
- classification: `HUMAN_ACCEPTED_COMPARATIVE_RESULT`
- current_status: `SOURCE_EXCLUDED`
- evidence_owner: P3-1 terminal authority
- canonical_source_paths: `.aiassistant/records/aiscc/cycles/20260915_0310_aiscc-p3-1-comparative-evaluation-final-acceptance-p3-2-entry-authorization-1.cycle.md`; `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`
- exact_supporting_artifact_hash_or_commit: terminal Cycle SHA-256 `6a7011c0cd144e31879e709c9b2138a2b07c7e27cacde1b53c1542242ed87e1b`
- allowed_extension: explain the missing same-attempt packet material and denominator exclusion
- forbidden_extension: relabel exclusions as PASS, FAIL, N/A, or negative samples
- freshness_or_release_note: exclusions remained unchanged through trace rework and Human acceptance
- target_surface: `README`, `docs/AISCC_COMPARATIVE_EVALUATION.md`

### `PUB-015` — M05 accepted result

- topic: M05 result
- public_wording: In the single eligible M05 packet, `AISCC_GOVERNED` resolved to `ACCEPTED` and `EXECUTOR_REPORT_BASELINE` resolved to `UNRESOLVED`; audit reconstructability was 10/10 and 5/10, and restart recoverability was PASS and FAIL.
- classification: `HUMAN_ACCEPTED_BOUNDED_COMPARATIVE_RESULT`
- current_status: `ELIGIBLE / EVALUATED / HUMAN_ACCEPTED`
- evidence_owner: P3-1 Browser/Human authority
- canonical_source_paths: `.aiassistant/records/aiscc/cycles/20260915_0310_aiscc-p3-1-comparative-evaluation-final-acceptance-p3-2-entry-authorization-1.cycle.md`; `.aiassistant/reports/aiscc/20260915_0310_aiscc-p3-1-comparative-evaluation-final-human-acceptance-browser-judgment-1.md`
- exact_supporting_artifact_hash_or_commit: corrected result ZIP SHA-256 `2827c3b0a302caff4971090347134d3f9e37ab0e8d6cf5be4eae0fe706d42e48`; terminal Judgment SHA-256 `f04bd7877be95240f9188070875f0c6d73f3ff0f01d12848f9b9ae1c9b5ddf83`
- allowed_extension: publish every metric with the single-packet scope and contrary ties
- forbidden_extension: generalize the result across products, repositories, providers, languages, cost, or operator burden
- freshness_or_release_note: Human accepted the corrected trace-complete result, not a broader claim
- target_surface: `README`, `docs/AISCC_COMPARATIVE_EVALUATION.md`

### `PUB-016` — P3-1 publication limitation

- topic: P3-1 publication-condition limitation
- public_wording: `materially_better_condition_possible = No` because the protocol requires at least two distinct eligible attempts spanning at least two requested classes, while only M05 was eligible.
- classification: `HUMAN_ACCEPTED_LIMITATION`
- current_status: `NO_STRONG_DIRECTIONAL_CLAIM`
- evidence_owner: accepted protocol and P3-1 terminal authority
- canonical_source_paths: `.aiassistant/reports/aiscc/AISCC_COMPARATIVE_EVALUATION_PROTOCOL.md`; `.aiassistant/records/aiscc/cycles/20260915_0310_aiscc-p3-1-comparative-evaluation-final-acceptance-p3-2-entry-authorization-1.cycle.md`
- exact_supporting_artifact_hash_or_commit: protocol SHA-256 `a96b1bffb1f927e97f476a923351471994d632ed0fbe40f4d96e51433b996ed6`
- allowed_extension: use the admitted conclusion that one bounded comparison completed and four rows were source-excluded
- forbidden_extension: claim materially better, superiority, statistical significance, or broad direction
- freshness_or_release_note: threshold is unchanged after viewing results
- target_surface: `README`, `docs/AISCC_COMPARATIVE_EVALUATION.md`

### `PUB-017` — prior-art overlap and novelty ceiling

- topic: prior-art overlap / novelty ceiling
- public_wording: AISCC acknowledges prior work in specification workflows, orchestration, evidence gates, permission and Human review, memory, reviewer systems, and provenance. Its product hypothesis concerns their integration into one inspectable governance chain and use on its own development.
- classification: `ACCEPTED_PROJECT_DECISION / OPEN_DIFFERENTIATION_HYPOTHESIS`
- current_status: `OVERLAP_ACKNOWLEDGED / NOVELTY_UNVERIFIED`
- evidence_owner: Prior-Art Boundary
- canonical_source_paths: `.aiassistant/reports/aiscc/AISCC_PRIOR_ART_BOUNDARY.md`; `.aiassistant/reports/aiscc/AISCC_PRODUCT_THESIS.md`
- exact_supporting_artifact_hash_or_commit: Prior-Art Boundary SHA-256 `c7cfdcaeddde8eaec384e72a56070e0924de658dbb3db14a729391d41726a0df`
- allowed_extension: position the integration as a product hypothesis
- forbidden_extension: claim first, sole, unique, invention, or absence of similar capability elsewhere
- freshness_or_release_note: no web/source freshness research occurred in P3-2
- target_surface: `README`

### `PUB-018` — public security and input boundary

- topic: public security/input boundary
- public_wording: The intended public mode is deny-by-default: no free-form task, external repository URL or upload, arbitrary shell, arbitrary network destination, public credential selection, or owner/private data.
- classification: `HUMAN_ACCEPTED_SECURITY_POLICY`
- current_status: `POLICY_ACCEPTED / PUBLIC_SERVICE_NOT_RELEASED`
- evidence_owner: Security Sandbox and Competition Public Runtime Boundary
- canonical_source_paths: `.aiassistant/rules/AISCC_SECURITY_SANDBOX.md`; `.aiassistant/reports/aiscc/AISCC_COMPETITION_PUBLIC_RUNTIME_BOUNDARY.md`
- exact_supporting_artifact_hash_or_commit: Security Sandbox SHA-256 `d11539925b3025b385dec2146dfa30193fc80dbbbd8b71ce4deccb219ba5738b`
- allowed_extension: describe accepted policy and intended fixed-synthetic allowlisted mode
- forbidden_extension: claim a deployed sandbox, complete security, or resistance to every escape/prompt attack
- freshness_or_release_note: P3-3 must verify release-environment safeguards before any launch
- target_surface: `README`

### `PUB-019` — project and competition status

- topic: competition submission status
- public_wording: P2 and P3-1 are closed; P3-2 documentation is in Human review; public release, deployment, and competition submission are not completed.
- classification: `CURRENT_PROJECT_STATUS`
- current_status: `P3-2 DOCUMENTATION_CANDIDATE / HUMAN_PENDING; P3-3 NOT_STARTED`
- evidence_owner: P3 terminal Cycle and Browser/Human authority
- canonical_source_paths: `.aiassistant/records/aiscc/cycles/20260915_0310_aiscc-p3-1-comparative-evaluation-final-acceptance-p3-2-entry-authorization-1.cycle.md`; `.aiassistant/reports/aiscc/20260915_0310_aiscc-p3-1-comparative-evaluation-final-human-acceptance-browser-judgment-1.md`
- exact_supporting_artifact_hash_or_commit: terminal Cycle SHA-256 `6a7011c0cd144e31879e709c9b2138a2b07c7e27cacde1b53c1542242ed87e1b`; terminal Judgment SHA-256 `f04bd7877be95240f9188070875f0c6d73f3ff0f01d12848f9b9ae1c9b5ddf83`
- allowed_extension: distinguish accepted work, current documentation candidate, and future release/submission work
- forbidden_extension: state that P3-2 is accepted/closed or that release, deployment, or competition submission is complete
- freshness_or_release_note: current as of the 0310 terminal P3-1 authority and this P3-2 candidate
- target_surface: `README`

## Public wording gate

Every load-bearing statement in `README.md` and `docs/AISCC_COMPARATIVE_EVALUATION.md` must resolve to one or more claim IDs above. New performance, novelty, deployment, security, or competition claims require a later canonical update and applicable evidence. Human review owns final positioning and readability.
