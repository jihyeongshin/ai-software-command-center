# AISCC P2-4 — Human/Judgment policy binding correction Human review

## 0. Browser Command Center judgment

0902 Executor result:

```text
P2_4_HUMAN_JUDGMENT_POLICY_BINDING_CORRECTION_PROPOSAL
/ HUMAN_REVIEW_PENDING
```

Browser independent judgment:

```text
ACCEPTED_CANDIDATE / HUMAN_REVIEW_REQUIRED
```

This is a design-correction acceptance candidate only.

It does NOT mean:

```text
runtime implemented
migration created
P2-4 self-dogfood source candidate created
golden cycle performed
P2-4 accepted/closed
```

## 1. Result integrity

0902 Executor result ZIP:

```text
SHA-256:
c163fd43b325e408745796d9b751d73d31c1c8f340b501255194be503465352f
```

Independent verification:

```text
15 members
one top-level directory
CRC PASS
14 EXPORT_MANIFEST rows
all row byte sizes exact
all row SHA-256 exact
TASK.md == canonical done Task byte-exact
returned Cycle/Judgment == issued 0902 delivery bytes
```

Governance Commit A reported and internally consistent:

```text
c10f89256b88d90782c7fbdea6ff8b27655f2b46
parent:
5aaeb6f690cd9209af57a60b846ac049e89e9047

message:
docs(aiscc): record human policy binding blocker
```

No product/test source, canonical baseline, migration, DB/Docker runtime, provider/network, golden cycle, source implementation commit, push or deployment occurred.

## 2. Correction reason

The previously Human-accepted 0319 TaskContract durable-body proposal required:

```text
human_binding.policy_fingerprint
judgment_binding.policy_ref / policy_fingerprint
```

before WorkRun/owner registration.

0846 proved that this over-specified the existing owner boundary.

Current accepted source/canonical semantics instead establish:

```text
TaskContract:
selects immutable Human/Judgment policy configuration and Judgment owner policy

P1-7 Human owner:
owns actual Human gate reservation/opening,
Human principal authentication,
HumanResult,
runtime Human guard facts

P1-7 Judgment owner:
owns durable JudgmentPolicy registration/projection,
runtime policy fingerprint/currentness,
Judgment issuance,
G_JUDGMENT_* facts

P1-4:
owns TransitionDecision and WorkflowState mutation
```

Therefore TaskContract must carry owner-consumable configuration, not fabricate owner-issued runtime fingerprints/results before those owner objects exist.

## 3. Preferred Human binding correction

Supersede the old Human object:

```text
{kind, policy_ref, policy_fingerprint, ...}
```

with the closed TaskContract-issued configuration:

```text
human_binding = {
  kind,
  authority_policy_ref,
  authority_policy_version,
  required_uses,
  purpose_id,
  purpose_version,
  owner_selector_fingerprint
}
```

Exact semantics:

```text
kind:
REQUIRED | NOT_REQUIRED

NOT_REQUIRED:
required_uses = []
purpose_id = null
purpose_version = null
owner_selector_fingerprint = null

REQUIRED:
uses existing P1-7 purpose
P1_7_WORK_RESULT_REVIEW / v1
and exact existing Human-required / Human-not-required transition-use configuration
```

Important correction:

```text
NO independent Human policy-content fingerprint is added.
```

The whole immutable TaskContract `body_sha256` protects these configuration bytes, while actual P1-7 gate/reservation/result fingerprints remain owned by P1-7.

`owner_selector_fingerprint` retains the existing source parameter name, but its value is the existing server-enrolled selector key semantics. This correction does not invent a role digest algorithm and does not let TaskContract enroll roles or authenticate a Human.

READY:

```text
does not reserve/open a gate
does not authenticate a Human
does not mint G_HUMAN_* facts
```

A real later gate request continues through the existing P1-7 reservation/guard path using the actual WorkRun/request and P1-6 PRE_HUMAN authority.

## 4. Preferred Judgment binding correction

Supersede:

```text
judgment_binding = {
  policy_ref,
  policy_fingerprint,
  owner_policy
}
```

with:

```text
judgment_binding = {
  owner_policy,
  policies
}
```

where `owner_policy` remains exactly one of:

```text
SYSTEM_DETERMINISTIC
HUMAN
COMMAND_CENTER
```

and each policy entry contains the existing `JudgmentPolicyAuthority.register(...)` configuration:

```text
policy_id
policy_version
source_state
target_state
requires_human_result
requires_post_human_evidence
deterministic_kind
evidence_basis_kind
evidence_checkpoint_ref
evidence_requirement_set_ref
```

TaskContract does NOT precompute the runtime Judgment policy fingerprint.

Instead, after durable TaskContract issuance and before new READY, a trusted adapter may register the exact verified configuration through the existing `JudgmentPolicyAuthority`.

The existing owner continues to create and verify:

```text
JudgmentPolicyRow / ProjectionRow
policy fingerprint
target_use_fingerprint
authority revision/currentness
Judgment
```

Registration configuration is not a Judgment and creates no `G_JUDGMENT_*` fact.

## 5. Non-substitution preserved

The correction explicitly preserves:

```text
HumanResult != Judgment
Judgment != TransitionDecision
HumanResult/Judgment != WorkflowState
Evidence != Human guard != Judgment guard
TaskContract config != HumanResult
TaskContract config != Judgment
prepared Judgment policy != Judgment result
body_sha256 != P1-7 runtime fingerprint
```

No new:

```text
Human policy registry
Judgment policy registry
policy table
HumanGate identity before WorkRun
fake reservation
caller callback authority
policy-fingerprint algorithm
state/guard owner
```

is proposed.

## 6. Existing baseline consistency

Canonical orchestration already states:

```text
Judgment owner selected by TaskContract policy
```

and:

```text
G_HUMAN_NOT_REQUIRED =
applicable TaskContract/judgment policy does not require HumanResult
```

The accepted P1-7 baseline remains the owner of System-owned HumanGate lifecycle, authenticated immutable HumanResult, System-owned Judgment, owner-bound Human/Judgment guards, restart/anti-replay/current-effectiveness, and P1-4 handoff.

No P1-7 source or canonical baseline is replaced by this correction.

## 7. Exact proposal identities

0902 proposal artifacts:

```text
HUMAN_BINDING_CORRECTION_PROPOSAL.md
SHA-256:
7ecad09c1e151fc76e83d85d7a84c25c14f09abba7e093393a5cf73b9a1d2833

JUDGMENT_BINDING_CORRECTION_PROPOSAL.md
SHA-256:
aed8421248cc8700fd0ebc2128ae7f5808037df555fbe8e0ee61606dd0eb9693

HUMAN_JUDGMENT_POLICY_SOURCE_AUDIT.md
SHA-256:
2595ac130c12a0da3cf45dc7867e4cb6806fafc83e0c77feec51147ccc57b0a9

OWNER_NON_SUBSTITUTION_PROOF.md
SHA-256:
7f22c68055d2cb2c118aa7ca67efc01ab36c09811030362bc935d23634e70a92

BASELINE_SUPERSESSION_DELTA.md
SHA-256:
47a473ab37a9fec09dee623dc254acf7d0b726f30cbae5c251715679ff6a9448
```

The already Human-accepted 0812 hashed `body_ref` correction remains unchanged.

## 8. Browser recommendation

```text
RECOMMENDATION:
ACCEPT
```

Reason:

1. It removes the unsupported pre-WorkRun Human policy fingerprint requirement.
2. It reuses existing P1-7 HumanGateReservationAuthority and JudgmentPolicyAuthority rather than creating parallel authorities.
3. It leaves runtime fingerprints, currentness, HumanResult, Judgment and WorkflowState in their existing owners.
4. It remains fail-closed for mixed/ambiguous configuration.
5. It does not reopen unrelated durable TaskContract, P1-6, P1-7 or P1-8 semantics.

Implementation must still prove the adapter/configuration composition and all owner-currentness behavior. Human acceptance here is design approval, not runtime acceptance.

## 9. Human decision requested

Choose exactly one:

```text
ACCEPT
REWORK
REJECT
```

If `ACCEPT`, Browser Command Center may reissue the durable TaskContract implementation cut using:

- 0812 hashed body_ref correction;
- this Human binding correction;
- this Judgment binding correction;
- unchanged existing P1-4/P1-6/P1-7/P1-8 owners.

No additional design task is required unless the real implementation exposes a new exact owner conflict.
