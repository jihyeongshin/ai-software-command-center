# TaskContract Durable Body Authority V1

Status: Human-accepted design adopted by Task 20260914_1302. Design ID: AISCC-TASKCONTRACT-DURABLE-BODY-V1. Accepted chain: 0319 base + 0812 body_ref + 0902 Human/Judgment binding + 0940 template/approval Outcome A + 1212 cycle-derived V1 issuance-domain/lock correction. Runtime implementation remains a candidate pending Browser review; this adoption does not close P2-4 or authorize a golden cycle. Historical proposal artifacts remain byte-preserved. This document states the corrected normative design; existing owner rules and fingerprint schemas remain unchanged.

## 1. Preferred design and ownership

Select one dedicated append-only table `task_contract_bodies` under the existing `EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY`. One row stores one complete immutable contract version as canonical bytes. Existing TaskConstraint V1 references/events/snapshots remain unchanged and authenticate the row through their existing payload ref/hash fields. No new semantic issuer, workflow state, RuntimeMode, P1-6 evidence store or general document store is introduced.

New owner types: `TaskContractBodyV1` (frozen, recursively immutable complete body), `IssuedTaskContractV1` (body plus verified V1 ref/issuance event/snapshot proof), `VerifiedTaskContractBindingV1` (read-only verified binding), and row model `TaskContractBodyRow`. These belong in `task_authority`, never in `self_dogfood`. The existing `_ExternalTaskAuthorityWriter` capability gates issuance. Read/verifier consumers cannot obtain that writer; matching an owner string or constructing a dataclass confers no authority.

## 2. Exact body shape

`TaskContractBodyV1` is a closed object: all fields below required, no extra fields. Nested objects are closed too; absence is represented only by the explicitly specified null variant. Arrays become tuples/frozen values in memory. Strings must already be NFC. No Agent prose is parsed into policy.

| Field | Exact type / constraint |
| --- | --- |
| schema_id | literal `AISCC-TASKCONTRACT-BODY-V1` |
| owner | literal `EXTERNAL_COMMAND_CENTER_TASK_AUTHORITY` |
| project_id, contract_id, task_id | ASCII local IDs `[A-Za-z0-9][A-Za-z0-9_.-]{0,95}`; nonempty; no semantic reuse across projects |
| contract_version | integer 1..9007199254740991; bool/float forbidden |
| goal | NFC nonblank string, at most 16384 UTF-8 bytes |
| non_goals | nonempty tuple of distinct NFC nonblank strings; each at most 4096 UTF-8 bytes; order authoritative |
| allowed_paths, forbidden_paths | nonempty sorted unique tuples of path selectors defined below |
| authority_refs | possibly-empty sorted tuple of `{ref: nonempty string, fingerprint: sha256}`; duplicate ref forbidden |
| evidence_binding | `{requirement_set_ref, requirement_set_fingerprint, checkpoints}`; checkpoints nonempty sorted tuple of `{ref, fingerprint}`; exact P1-6 identities, no body copies |
| human_binding | exact closed configuration in section 9; explicit REQUIRED or NOT_REQUIRED; no independent Human policy fingerprint |
| judgment_binding | `{owner_policy, policies}` as section 10; owner_policy one of existing `SYSTEM_DETERMINISTIC`, `HUMAN`, `COMMAND_CENTER` |
| source_next_action | closed object specified in section 3 |
| repository_binding | `{repository_id, repository_root, base_commit}`; exact server-enrolled identity/root and lowercase 40-hex commit |
| execution_provenance | `{runtime_mode: "OWNER_SELF_DOGFOOD", cycle_execution_mode: "AISCC_SELF_DOGFOOD", orchestrator_version, orchestrator_commit}`; version nonblank, commit lowercase 40-hex |
| predecessor | null for version 1; otherwise `{contract_version: n-1, body_sha256}` |

All unspecified ref strings are nonblank NFC UTF-8 strings of 1..1024 bytes; other unspecified identity/version strings are 1..160 bytes. repository_root alone permits 1..4096 UTF-8 bytes; its absolute path is private owner context and never public Cycle output. Fingerprints are lowercase 64 hex. authority_refs must equal the exact trusted policy-required set of independently verifiable existing owner refs. That set may be empty. No universal approved-template/approval-source pair is required for the current recognized catalog path. NONE/null is absence, never a hash or approval. Every present ref is owner-verified for exact scope/currentness; self-reference/circular body authority is denied. Public Cycle export omits the root and emits enrolled repository identity/hash only. All actual fingerprints are lowercase 64 hex; the existing Human selector-key field is the explicit section 9 exception. No omitted/default Human requirement. Human owner policy requires REQUIRED human binding; NONE and explicit NOT_REQUIRED are not interchangeable. Evidence definitions must resolve from the existing P1-6 owner for the exact task/version. Human/Judgment configurations bind this body task/version and are consumed by existing P1-7 owners; they are not independent pre-WorkRun policy records. Subject/task constraints remain in their owner objects. Existing evidence/Human/Judgment verification decides applicability; the body cannot declare those predicates satisfied.

Scope selectors are literal relative ASCII POSIX file paths or recursive directory selectors ending `/**`; no other glob syntax. Segment grammar `[A-Za-z0-9_][A-Za-z0-9_.-]*`; reject empty, dot/dot-dot, trailing dot, Windows reserved device stems, colon, backslash, absolute/drive/UNC paths, percent encoding and control characters. Reject case-fold collisions. The recursive selector includes that directory and descendants; file selectors select exact file identity. Reject any intersection between allowed and forbidden selectors by case-folded segment ancestry; ambiguous overlap is DENIED, never precedence-resolved. Actual materialization additionally resolves against the exact enrolled root and denies symlink/reparse escape. Root is not discovered from cwd or caller guess; a trusted repository binding supplies its canonical absolute representation. Root spelling and platform are fixed by that binding before hashing; mismatch rejects rather than silently normalizing.

Body byte limit is 1048576. This is a specific work-contract schema, not arbitrary JSON storage. Narrative fields cannot replace explicit scope/requirement/policy inputs. Scope, goal, policy or provenance changes require a new version.

## 3. Authoritative NextAction and issuance provenance

`source_next_action` fields: `selection_id`, `selection_version`, `selection_fingerprint`, `project_revision` (positive safe integer), `action_ref`, `descriptor_fingerprint`, `issuance_candidate_id`, `issuance_candidate_fingerprint`, `external_context`.

`external_context` is null only if the selected owner-defined mode permits no external context. Otherwise exactly `{context_ref, context_fingerprint, introduction_event_ref, introduction_event_fingerprint, snapshot_ref, snapshot_fingerprint, owner_event_high_watermark}`. The originating NextActionContext belongs to the predecessor Task/selection; it MUST NOT be rebound to the new contract ID/version. Its identity is checked against the owner selection/descriptor, not forced equal to the new TaskContract. This avoids a circular requirement to create a new contract before selecting its source action.

Issuer resolves current selection by the existing P1-8 owner (replay and projection/currentness), never accepts a caller-created NextActionSelection as proof. It requires the current recognized descriptor's exact external issuance owner and explicitly authorized complete body/scope/repository. V1 supports only open-cycle-derived-task-issuance; section 11 defines the source gate. Use existing ActionRef serialization and existing selection fingerprint. Candidate has no current fingerprint API: the proposed candidate fingerprint is JCS SHA-256 of exactly its seven current dataclass fields, ActionRef serialized and created_at in fixed UTC microsecond ISO form. It must equal the owner-replayed candidate. This new binding is additive in Task authority and does not replace P1-8 selection identity.

Before issuance, the existing private Command Center capability explicitly authorizes the exact complete body under the current recognized source descriptor and trusted repository/scope. No separate template registry or Markdown-hash authority is introduced. Agent/self_dogfood can request/read only; it cannot pass a writer capability or expand a body. Stable IDs and body fingerprint derive from explicit approved inputs; no wall-clock identity, random IDs or model choice. Issued-at is envelope provenance and separate from deterministic body identity. Retrying an issued version returns its existing envelope timestamp, never reissues it.

## 4. Canonical bytes and TaskConstraint V1 linkage

Serialize the body with existing `aiscc.contracts.canonical_json.canonical_json_bytes` (restricted RFC8785/JCS): UTF-8, no BOM/trailing LF, NFC required, safe integers only, no floats/NaN, UTF-16 key order. Exact-field validation precedes serialization. Read uses canonical-byte verification plus schema validation; noncanonical, duplicate-key, unknown-field or hash mismatch rejects. `body_sha256 = SHA256(canonical_body_bytes)`; the body contains no self-hash or envelope refs, avoiding circular hashes.

`body_identity_bytes = JCS({"project_id": project_id, "contract_id": contract_id, "contract_version": n})`.

`body_ref = "task-contract-body:v1:sha256:" + SHA256(body_identity_bytes)`, exactly 93 ASCII characters. Content integrity remains the separate SHA256(canonical_body). This preserves the full 96-character ID domain without widening TaskConstraintRefV1 validation.

For each new version issue a NEW, otherwise unchanged `TaskConstraintRefV1`:

- scope = TASK_CONTRACT with exact project_id, contract_id, task_contract_version=`v<n>`; work_run_id omitted.
- logical_constraint_id = `tc-body-` + SHA256(JCS([project_id, contract_id])); version-specific scope remains part of its existing logical key.
- constraint_ref_id = `tc-body-` + body_sha256; constraint_ref is the existing `task-constraint:v1:<id>` form.
- constraint_schema_id = `AISCC-TASKCONTRACT-BODY-V1`; constraint_schema_version = `v1`.
- constraint_payload_ref = body_ref; constraint_payload_fingerprint = body_sha256.
- Existing owner, authority IDs/version, reference schema, fingerprint formula and events stay exact.

The full body lives ONLY in the new row. No additional V1 envelope key. The row's `constraint_ref` FK and the hash/ref equality connect it to the existing issued ref. Its issuance-event FK must resolve an ISSUED event targeting that exact ref/hash/scope. Latest/original owner snapshots certify that event via the unchanged global registry sequence. No FK to one fixed snapshot is required: snapshots are independently certified prefixes and verified at read/admission time.

## 5. Issuance/read/verify APIs and transaction

Private writer methods: `issue_task_contract(body, expected_current_body_sha256, issued_at)` and `revoke_task_contract(project_id, contract_id, expected_version, expected_body_sha256, effective_at)`. Public read/verifier methods: `get_task_contract(project_id, contract_id, version)` (reference/value only) and `verify_task_contract(binding, require_current, expected_repository_binding, expected_next_action_ref)` (the issued receipt carries the original snapshot proof; current prefixes are owner-resolved) returning `VerifiedTaskContractBindingV1`. No public/default writer getter; use existing once-bound private composition capability.

Issuance in one database transaction: acquire stable family advisory lock on JCS([project_id, contract_id]); resolve/validate current selection and approved complete body; read exact family versions; enforce version/predecessor; allocate existing counter/event sequences; issue V1 ref, ISSUED event and body row atomically. For n>1 revoke previous version's current ref in that SAME transaction before issuing the new version. Commit all or none. Internal existing repository helpers must accept the caller-owned AsyncSession; do not chain current public methods that each commit independently. No body-only or ref-only partial issuance is successful. Foreign keys and uniqueness fail closed on collisions.

Within a version, same ID and exact full body bytes plus expected predecessor is idempotent, returns the existing authoritative receipt; different bytes reject. A retry after a later successor exists returns only a HISTORICAL receipt for the exact old operation, never current issuance permission. A repeated explicit revoke returns its original event only if the exact expected version/body matches; conflicting same event ID rejects. Derived event IDs bind operation, family, version and body hash. Timestamp is excluded from retry identity after first commit. Currentness is separately verified.

## 6. Version/supersession and restart

Family key = (project_id, contract_id). Version starts at 1, strictly increments by 1; gaps, duplicate version/different hash and altered predecessor deny. Task identity stays constant for a family; new task_id requires a new contract_id. Latest version is determined from immutable body rows under family lock and verified against its V1 current projection/event fold. No new mutable current table is needed.

Because V1 scope includes contract_version and existing supersede preserves scope, DO NOT use V1 SUPERSEDED to jump v1 -> v2. Proposed whole-contract replacement is atomic old-scope REVOKED plus new-scope ISSUED, with body predecessor hash linking versions. Each V1 logical key still has exactly one origin and no event after revocation. This is a new higher-level owner operation, not a change to V1 supersession. Explicit revocation of the family's latest version closes that family: later issuance under it rejects; new contract_id is required. Replacement's revoke+new issue is distinguishable because the next body with exact predecessor exists atomically.

Restart verification loads canonical bytes, validates hash and relational identity projections, resolves existing issuer/ref/event and certified complete prefix, verifies all predecessor links and current projection. Missing/tampered body, broken event FK, invalid prefix or partial issuance is AUTHORITY_CORRUPTION; no automatic repair/delete/backfill. Latest revoked with no successor is current-ineligible, not corruption. Historical verification uses the original certified H and immutable body; later revocation does not rewrite prior truth. Process capability identity is not a durability proof.

## 7. READY and future self-dogfood integration

Existing P1-4 `WorkflowKernel.request_transition` and repository decide continue to own None/0 -> READY/1. A task-authority verification participant (`TaskContractReadyParticipant` in task_authority, implementing existing TransitionTransactionParticipant) resolves the issued body and current certified prefix inside the same READY transaction. It checks exact project/contract/version, mode, repository/base, expected action and scope against trusted server context immediately before admission. It holds the family lock through the existing run transaction; no sidecar-object-only authorization.

The adapter first verifies the body through the owner read port and obtains existing P1-4-owned G_CONTRACT/G_SCOPE/G_RUNTIME_CONTEXT facts from the enrolled P1_4GuardAuthority. The participant returns only those exact preflight facts from facts(request); current repository.decide calls facts before prepare, so prepare MUST revalidate their exact body/snapshot binding and currentness under the family lock before evaluation and raise on any mismatch. No new fact is minted after the facts tuple is captured; no new guard owner or workflow transition. Preserve required_bound_refs. Existing persisted guard authority_ref carries a canonical locator `task-contract-admission:v1:<body_sha256>:<snapshot_ref>`; snapshot_ref is the full existing ref (the parser removes the exact task-contract-admission:v1: prefix, then partitions once at the next colon into the 64-char hash and the untouched full snapshot ref). Together with request project/contract/version this resolves the exact body and original H. Observation bound refs remain whatever current P1-4 requires. Event/evaluation fingerprints retain this locator using their existing fields. The verifier never treats possession of the locator as authority.

Acquire existing run lock first, then family lock in participant; issuer/revoker never acquires run locks, preventing a reverse dependency. The family lock serializes new READY with revoke/replacement. Same deterministic run/request ID replays through existing kernel idempotency; conflicting body/ref denies. Missing or legacy ref-only contract rejects this new entrypoint before run creation. Do not add a WorkRun table column or backfill old WorkRuns. Existing admitted runs retain pinned historical version; replacing a contract does not mutate a running WorkRun or automatically cancel it. Any execution-time revocation policy remains separately owned and not added here.

P1-6 definition authority is issuance-time checked. Human/Judgment exact configurations are checked at issuance and later consumed only by their existing owners as sections 9 and 10 specify. READY admission does not prove evidence satisfaction, HumanResult or Judgment. The future SelfDogfoodTaskSpec is a deterministic view of the verified issued body, not another contract or issuer. Future P2-4 golden issuance is separately authorized; no real active Task/file/run is created by this design gate.

## 8. Compatibility and acceptance

Existing V1 refs/events/snapshots/selection/evidence/WorkRun bytes remain unchanged. Old refs without a body stay valid for their existing purposes but cannot satisfy new whole-contract entry. No backfill, invented historical bodies, old-hash repair or P2-3 replay. P1-8 carrier/source equality and AUTHORING_SNAPSHOT_PROVENANCE_ONLY H remain unchanged; current READY checks do not redefine terminal P1-8 external-context currentness.

The named accepted Human chain authorizes this corrected schema, higher-level replacement/revocation/currentness semantics, owner transaction/read/verify capability and one-table additive migration 20260914_0009 (parent 20260901_0008). Immutable UPDATE/DELETE/TRUNCATE rejection and empty-only downgrade are mandatory; nonempty downgrade must preserve schema/data/revision. Isolated tests must cover restart from persisted rows, concurrent same-version issues, different-content replay denial, n+1 races, rollback at every write boundary, revoked-family denial, forged receipt/candidate, corrupted byte/hash/ref/event/prefix, scope/base/repository/action guards, and existing READY creation. Design adoption alone is not implementation/runtime acceptance.

## 9. Human binding (accepted 0902)

### Closed shape and ownership

Every field is required; unknown fields denied. Object fields:

| Field | Type / owner |
| --- | --- |
| kind | REQUIRED or NOT_REQUIRED; external TaskContract issuer's explicit requirement |
| authority_policy_ref | nonblank NFC string 1..160 UTF-8 bytes; TaskContract-issued configuration passed unchanged to HumanGateReservationAuthority |
| authority_policy_version | nonblank NFC string 1..64 bytes; same owner/configuration |
| required_uses | sorted unique array of closed {source_state, target_state}; both exact existing WorkflowState values, never null; TaskContract-issued exact transition-use configuration |
| purpose_id | REQUIRED: existing HUMAN_GATE_PURPOSE_ID literal P1_7_WORK_RESULT_REVIEW; NOT_REQUIRED: null. Existing P1-7 purpose, not an issuer-selected new purpose |
| purpose_version | REQUIRED: existing HUMAN_GATE_PURPOSE_VERSION literal v1; NOT_REQUIRED: null |
| owner_selector_fingerprint | REQUIRED: exact nonblank NFC enrolled server selector key, 1..160 bytes; NOT_REQUIRED: null. Preserve current owner key semantics; do not invent a hash of roles or require an unimplemented selector digest algorithm |

No policy_fingerprint, gate ID/ref/hash, principal identity, HumanResult, satisfied flag, WorkRun or state_version. Expiry is not part of this correction's body shape: current reserve default expires_at=None remains the bounded handoff for this version. Adding an expiry policy later requires an explicit body version/schema review; no caller expiry override.

The selector name is retained for compatibility with the owner's designated_principal_selector_fingerprint argument. Current source consumes an enrolled key through allowed_roles_by_selector (defaults reviewers-v1/reviewers-v2), not an independently recomputed 64-hex policy digest. This is an explicit correction to the old generic fingerprint rule for THIS selector field only. Other existing body hash fields remain lowercase SHA-256. Selector enrollment/role authorization stays server-owned; the body cannot enroll roles or authenticate a principal.

### Exact REQUIRED / NOT_REQUIRED meaning

NOT_REQUIRED: required_uses must be empty and purpose/selector fields null. It does not assert no runtime gate exists. Every judgment policy entry must requires_human_result=false and owner_policy must not be HUMAN. Canonical P1-6 requirements must not demand HumanResult on the corresponding completion path; a conflict rejects issuance.

REQUIRED is a whole-contract Human-result requirement for this correction. Judgment owner_policy must be HUMAN and every judgment entry requires_human_result=true. required_uses must include at least one existing fresh gate-open pair guarded by G_HUMAN_REQUIRED (ADMISSION_PENDING->HUMAN_REQUIRED or REWORK_REQUIRED->HUMAN_REQUIRED). Include only those chosen gate-open pairs plus ALL six existing G_HUMAN_NOT_REQUIRED bypass pairs: RUNNING->REWORK_REQUIRED; ADMISSION_PENDING->REWORK_REQUIRED; ADMISSION_PENDING->ACCEPTED; ADMISSION_PENDING->REJECTED; BLOCKED->REWORK_REQUIRED; REWORK_REQUIRED->REJECTED. Exact set = six pairs union chosen fresh gate-open pairs. No BLOCKED->HUMAN_REQUIRED fresh reservation: existing suspended-gate resumption owns that path. No new state or guard.

This coverage requirement prevents a TaskContract's Human requirement from being absent on a direct terminal/rework request. required_uses remains exactly the existing owner constructor's configuration, not a new predicate engine. Mixed Human/non-Human requirements across outcomes are not represented by this single-kind correction; ambiguous mixed configuration is rejected rather than silently choosing precedence. Human adoption must explicitly approve this stated domain.

### Issuance and READY

Whole-body JCS/SHA protects these exact strings/arrays/nulls. It proves bytes, not issuer authority. External Task authority verifies its existing capability, full durable body/ref/event/snapshot chain, canonical identity, current approved NextAction/scope and existing evidence binding. It validates the closed policy configuration and cross-object consistency above. It does NOT require a pre-WorkRun Human policy record, independent policy hash or reservation.

A trusted adapter in task_authority/ready.py consumes only the owner-verified binding and constructs HumanGateReservationAuthority with frozenset((body.contract_id, 'v'+str(body.contract_version), source, target) for each required_use), authority_policy_ref/version exact. No arbitrary caller factory/callback, body dict or policy singleton supplied by an Agent is trusted. Existing application ownership/capability binding must protect that adapter as it protects the verified TaskContract entry. No private attribute mutation of an already configured authority. Each immutable body version gets its own composition; reload reconstructs from verified bytes.

READY repeats owner body/ref/hash/currentness verification under the accepted family lock, validates policy mapping, and verifies enrolled selector availability without authenticating a Human. P1-4 owns READY; it mints no Human guard. Do not reserve a gate on None->READY (current reserve rejects absent source state).

### Later owner handoff

At a real fresh gate-open request, call the configured existing reserve(request, designated_principal_selector_fingerprint=body value) with no fabricated WorkRun/request. Existing owner derives gate ID and fingerprint from real run/request/state/policy/purpose/selector. Pass that real reservation to existing HumanGuardAuthority.gate_open_participant with current P1-6 PRE_HUMAN evidence. Shared-transaction prepare verifies request, reservation, checkpoint and current evidence; only an admitted P1-4 decision opens the durable gate. HumanPrincipalAuthority later authenticates roles against enrolled selector; HumanResult remains separate.

For G_HUMAN_NOT_REQUIRED, existing _policy_guard_current verifies a matching current WorkRun, no unresolved current pending gate, and not reservation_authority.requires_human(request). It does not read JudgmentPolicy directly. The trusted body-to-both-owners consistency check is therefore essential: a Judgment requires_human_result flag alone cannot configure this guard. NOT_REQUIRED is configuration, never a fabricated satisfied fact.

### Negatives / legacy

Deny omitted kind, extra policy_fingerprint, unknown states, duplicate pairs, missing six bypass pairs, gate-less REQUIRED, invalid purpose, un-enrolled selector, mismatched task/version, invalid Human/Judgment combination, changed body hash/ref, stale/revoked body, caller-created binding or adapter callback. Unresolved runtime gate must still deny G_HUMAN_NOT_REQUIRED. Reserve at READY must fail. No HumanResult can be derived from this object.

Existing P1-7 rows/refs/hashes/configuration remain untouched. Existing bodies using the superseded policy_fingerprint shape are not silently translated; no durable whole-body implementation existed at this baseline. Future incompatible historical bodies require explicit versioned handling. 0812 hashed body_ref, 96-character project/contract IDs and unchanged V1 validators remain accepted unchanged.

Canonical serialization: apply the unchanged whole-body restricted JCS routine; all strings already NFC, booleans strict, null explicit, arrays serialized in the specified deterministic order (Human required_uses by source_state then target_state). No per-policy digest is added to the body. The nested policy configs become recursively immutable with the whole body.

## 10. Judgment binding (accepted 0902)

### Closed exact shape

judgment_binding = {owner_policy, policies}. owner_policy is exactly SYSTEM_DETERMINISTIC, HUMAN or COMMAND_CENTER, selected by the TaskContract issuer. policies is a nonempty array sorted by source_state,target_state,policy_id,policy_version. Duplicate source/target use or policy identity is denied. All entries use that one owner policy, preserving the prior single owner choice.

Each entry is closed and all fields required:

| Field | Type / owner |
| --- | --- |
| policy_id | NFC ASCII local ID [A-Za-z0-9][A-Za-z0-9_.-]{0,95}; TaskContract registration identity; must be globally collision-free in existing serialized_ref namespace |
| policy_version | nonblank NFC ASCII version [A-Za-z0-9][A-Za-z0-9_.-]{0,63}; TaskContract registration identity |
| source_state, target_state | existing WorkflowState strings; source never null; TaskContract-declared existing Judgment-guarded matrix use |
| requires_human_result | strict bool; TaskContract policy consumed/validated by P1-7 |
| requires_post_human_evidence | strict bool; existing register parameter (do not reinterpret its historical name as an independent new evidence rule) |
| deterministic_kind | ACCEPTED, REJECTED, HOLD_REWORK_REQUIRED or null; configured fixed rule outcome, never an already issued Judgment |
| evidence_basis_kind | SATISFIED_ATTESTATION, UNSATISFIED_SET_EVALUATION or null; existing registration variant |
| evidence_checkpoint_ref | exact existing P1-6 ref string 1..1024 or null |
| evidence_requirement_set_ref | exact existing P1-6 set ref string 1..1024 or null |

No caller fingerprint, authority revision/token, issued_at, target_use_fingerprint, judgment ref/result or currentness boolean. Body contract_id and version supply register's task_contract_id and 'v<n>'; no duplicated task identity in entries. Runtime serialized_ref remains p1-7-judgment-policy:<policy_version>:<policy_id>, derived by existing owner. Namespace collision with another task/version denies; the adapter never repairs or aliases it. Issuer allocates disjoint policy IDs/versions for new TaskContract versions.

### Existing registration rules preserved exactly

SYSTEM_DETERMINISTIC iff deterministic_kind is nonnull; requires_human_result=false. HUMAN requires true and deterministic_kind=null. COMMAND_CENTER requires false and deterministic_kind=null. The Human correction's global REQUIRED/NOT_REQUIRED consistency rule applies.

If evidence_basis_kind=null, both evidence refs must be null (existing legacy variant); it is not a G_EVIDENCE bypass. If SATISFIED_ATTESTATION, both refs nonempty and requires_post_human_evidence=true. If UNSATISFIED_SET_EVALUATION, both refs nonempty, owner SYSTEM_DETERMINISTIC, deterministic_kind HOLD_REWORK_REQUIRED, target REWORK_REQUIRED and requires_post_human_evidence=false. Existing evidence owners retain actual set/admission checks. Policy refs must match the body's unchanged P1-6 binding; conflicting applicability denies.

For deterministic policies require the configured outcome to match the intended target's existing Judgment guard (ACCEPTED->ACCEPTED; REJECTED->REJECTED; HOLD_REWORK_REQUIRED->REWORK_REQUIRED). Only existing matrix uses requiring a Judgment guard may be configured. Human policy entries target existing Human-result transition uses; no direct pre-Human terminal shortcut. Incomplete/ambiguous completion-use coverage fails closed; no generic transition planning is added.

### Issuance / READY / runtime

TaskContract issuance validates configuration, scope, body integrity/authenticity and owner-compatible parameters. No Judgment registration or result is claimed at issuance. Whole body_sha256 authenticates immutable config only after the full owner proof; do not feed it into the runtime policy.fingerprint slot.

A trusted adapter deriving only from verified body may later call existing JudgmentPolicyAuthority.register once per declared use with EXACT listed arguments and body task identity. This existing owner already persists JudgmentPolicyRow/ProjectionRow, generates target_use_fingerprint, revision, owner fingerprint and serialized_ref. It requires no WorkRun for registration. It is the existing registry, not a newly proposed registry/table. Registration is performed only by the existing owner in the separately authorized READY preparation.

Stage registration after durable body issuance and before new READY, outside the READY run transaction; reverify exact body/currentness before admission. Registration and TaskContract issuance are NOT claimed atomic across owners. A failure leaves original rows for idempotent re-entry; never deletes or rewrites them. A successfully registered policy for a body that later becomes revoked cannot authorize a new READY; Task authority check still denies. Historical/current running-run behavior stays with existing policy/transition owners.

Restart uses the same existing register with identical configuration to retrieve its durable result; current source recomputes policy fingerprint excluding issued_at, returns existing durable value on exact match, and checks the current projection. Changed config or stale projection raises; do not auto-supersede or overwrite. Verify the returned config equals the body projection. Do not call a new adapter fingerprint algorithm. Later request-time current_in_session verifies the existing owner fingerprint, projection/ref/revision, task/version/source/target and target-use under its owner lock. JudgmentAuthority.issue and participant retain Human/evidence/Command Center authentication and durable provenance verification.

READY validates the body and exact prepared policy configuration; it does not pretend current_in_session for a future transition is a READY fact, nor fabricate a future WorkRun request to pass it. Actual future-use currentness is rechecked by P1-7 when that request exists. Prepared policy registration is not a Judgment and provides no G_JUDGMENT_* fact at READY.

### NOT_REQUIRED / REQUIRED / negatives / legacy

No new Judgment owner NONE/NOT_REQUIRED is introduced. HumanResult not required means the strict existing policy flag false; Judgment is still required when the existing transition matrix requires it. REQUIRED HumanResult uses HUMAN owner plus real current result at runtime. Command Center requires its real existing principal/action authority; it is not HumanResult substitution. A configured deterministic_kind is a rule constant, not execution evidence.

Deny unknown field/enum, unsafe bool coercion, incompatible kind/owner/human flags, partial evidence basis, wrong target/refs, duplicate uses, reused policy identity with different body config, stale projection, fake policy result, changed body/ref and manual runtime fingerprint replacement. Legacy existing policy rows/fingerprints are unchanged; legacy null evidence basis stays interpreted by existing owner. No migration/backfill. Old proposed body policy_ref/fingerprint objects are not silently accepted by the new closed schema.

Canonical serialization: apply the unchanged whole-body restricted JCS routine; all strings already NFC, booleans strict, null explicit, arrays serialized in the specified deterministic order (Human required_uses by source_state then target_state). No per-policy digest is added to the body. The nested policy configs become recursively immutable with the whole body.

## 11. Accepted 1212 V1 source capability and lock order

TaskContract Durable Body V1 supports exactly `open-cycle-derived-task-issuance` with an owner-verified `CYCLE_DERIVED` current selection. Future golden issuance must resolve that actual authoritative source; an Agent choice or historical replay is insufficient.

`open-operational-recovery-task-issuance` remains valid in P1-8. V1 issuance rejects it and every other unsupported source with `TASKCONTRACT_V1_UNSUPPORTED_NEXT_ACTION_SOURCE` before source WorkRun lock, dependent proof, or body/ref/event mutation. No conversion to cycle-derived, select retry, recovery WorkRun-lock removal, private projection repair or silent fallback is permitted. The general P1-8 currentness verifier retains its recovery source WorkRun lock.

Issuer/revoker never acquire any WorkRun lock. READY obtains the existing target WorkRun lock first, then family lock, and never a source/predecessor WorkRun lock. Family lock serializes version/revoke/READY. Issuance holds sorted existing constraint locks and snapshot serialization before owner global/currentness locks; P1-8 verifies current selection in that caller transaction, then P1-6 verifies definitions in the same transaction before body/ref/event writes. P1-8 locks its policy/descriptor, memory lineage/view and project projection using existing owner ordering; P1-6 locks task then set/definition authority. Verification does not commit, roll back, rebuild projections, create a fake WorkRun or mint evidence attestation.

Existing owner invalidation transactions must serialize with these reads. No reverse family/P1-8/P1-6 path may be introduced; additional owner/lock requirements require a separately accepted design. The source capability restriction is a V1 issuer boundary, not a P1-8 semantic redesign.

## Accepted 2010: one-time self-dogfood Genesis authority

Normative design: `AISCC-P1-8-SELF-DOGFOOD-GENESIS-BOOTSTRAP-V1`.
Human-provided design acceptance is recorded in the byte-exact 1916 Human review
(SHA-256 `09c93a9a67ca064bd269240787b8fdd5380f05693f4394dc74bba778c9f0da8a`).
This amendment extends the earlier source capability statements only as stated below;
all historical catalog JSON, fingerprints, Cycle provenance and other owner boundaries remain unchanged.

`SELF_DOGFOOD_GENESIS` is an explicit source mode with action
`open-self-dogfood-genesis-task-issuance`. It is never a fallback, recovery translation,
Cycle-derived alias, Replay import, Markdown import, or LLM action selection.
The separate Genesis catalog requires exactly one externally owner-issued authority
and one proposal. It fabricates no predecessor WorkRun, source Cycle, memory entry,
CycleMemoryReference, Human result, Evidence or Judgment.

The immutable canonical authority binds project, authority ID, source mode, action,
repository ID, absolute root, exact base commit, phase, OWNER_SELF_DOGFOOD runtime,
AISCC_SELF_DOGFOOD execution mode, external Command Center issuer identity/version,
and UTC issuance time. Its fingerprint authenticates the complete canonical body.
Only a bootstrap-bound external writer can persist it; constructing or parsing bytes
is not owner issuance. Selection and Task issuance verify the persisted authority,
exact enrolled context and currentness in the caller's database transaction.

Initial enrollment requires no operational WorkRun, no admitted operational Cycle,
no CURRENT NEXT_ACTION_CONTEXT lineage, and no conflicting current selection.
After Task binding, only that exact family's own WorkRun lineage may coexist until
its first owner-admitted Cycle. Any admitted Cycle permanently makes Genesis
non-current, even after restart, historical replay, projection rebuild or later
context withdrawal. Any CURRENT cycle-derived context also denies Genesis.
Historical reads remain possible and never confer currentness.

One operational project has at most one Genesis authority and one exact TaskContract
family/body (version 1). Exact retries return the durable result; changed body,
different family or a second distinct authority is denied. Revocation cannot free
this one-time binding. New issuance and currentness after the first Cycle fail with
GENESIS_NOT_ELIGIBLE; corrupt or partial reciprocal authority/body records fail closed.

TaskContract V1 supports exactly SELF_DOGFOOD_GENESIS and CYCLE_DERIVED.
OPERATIONAL_RECOVERY remains a valid P1-8 source but is rejected by this issuer before
any source WorkRun lock or body mutation. No general planner is introduced.

The closed Genesis source_next_action variant retains all existing source identity,
selection and candidate fields, requires external_context=null, and additionally
requires genesis_authority={authority_ref, fingerprint, phase_id}. Cycle-derived
bodies retain their exact previous schema; neither variant accepts the other's fields.
Repository/root/base and both execution modes must equal the enrolled authority.
The body/ref/owner event and immutable TASK_BOUND record are written in the same
transaction. Historical body verification checks reciprocal Genesis binding even
after source currentness has ended. A forged body hash alone is never sufficient.

Issuer/revoker acquire no WorkRun locks. Issuance keeps family, sorted independent
constraint/snapshot and existing NextAction owner lock order, adding Genesis
currentness under the NextAction project and existing Cycle memory-project advisory
locks. This serializes admission of the first Cycle with Genesis currentness reads.
New WorkRun insertion joins the same project lock after READY participant/family
checks; the target WorkRun lock remains first. No predecessor WorkRun lock exists.
