# AISCC Cycle Record

## meta
- cycle_id: `20260916_1201_aiscc-p3-3-l4-durable-luna-binding-substantive-acceptance-persistence-entry-1`
- date: `2026-09-16 KST`
- primary_semantic_owner: `Browser Command Center`
- affected_areas: `P3-3 Public Live L4 durable semantic provider request compatibility + accepted Luna profile`
- work_type: `REWORK`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_task: `.aiassistant/tasks/done/20260916_1002_aiscc-p3-3-public-live-l4-durable-semantic-dispatch-compatibility-and-luna-binding-retry-1.md`
- result_status: `PARTIAL_ACCEPTED`
- reject_cause: `none`
- canonical_cycle_path: `.aiassistant/records/aiscc/cycles/20260916_1201_aiscc-p3-3-l4-durable-luna-binding-substantive-acceptance-persistence-entry-1.cycle.md`

## result integrity
- Executor ZIP SHA-256: `f558a888193ad4e708ebefb0111feb961c5e29e2c4a34f3228ce3f8e292c4738`
- sidecar: exact match
- HEAD before/after: `e287117ba021411b82560df0af61901f7a8212bb`
- index: empty
- Public admission: disabled
- provider calls: 0

## substantive acceptance

Migration topology:

```text
0016 sole pre-head
→ 0017_public_live_semantic_provider_requests
→ 0017 sole post-head
0013-0016 unchanged 4/4
```

Accepted durable invariants:

```text
physical provider request != semantic role != retry ancestry
semantic phases <=3
retry <=1
physical provider requests <=4
PRIMARY low
VERIFY low
CORRECT medium
unknown outcome => no blind retry
intermediate success != pipeline completion
server-owned COMPLETE => existing GOVERNANCE_PENDING
```

No P1 WorkflowState was added.

Historical two-dispatch rows remain legacy-compatible and are not reinterpreted.

## bounds accepted

```text
input <=8000/request
output <=2000/request
substantive output <=6000/run
stockroom_summary <=1 dispatch/run
connect/read/outer wait = 5/30/35s
run deadline = 90s
planning liability <=4400 micro-USD/request
frozen $0.20/run / $4/day / $15/campaign unchanged
```

## evidence

```text
focused:
400 PASS

final full:
1423 PASS / 3 existing Windows symlink-host SKIP / 0 FAIL / 0 ERROR

source identity:
19/19 PASS

PostgreSQL:
17.6 isolated local-cache runtime

real provider/credentials/billing/deployment:
NOT RUN
```

## hard-wall boundary

The 35-second SDK/application cutoff is accepted as conservative L4 non-paid authority behavior.

It is not accepted as proof that a hosted synchronous worker/thread is forcibly terminated at 35 seconds. The worker may finish later, but late success is not admitted, blind retry is forbidden, and conservative liability remains.

Hosted process/thread termination remains later L5/release evidence.

## exact accepted source

- `migrations/versions/20260916_0017_public_live_semantic_provider_requests.py` — `f871dc697263c0189747ca3469808783eb17db232019f1f0f1526ff488c4a137`
- `src/aiscc/providers/models.py` — `6342b0741a4b6225a586ac39cecb78c84060f1cbeefdbf3eb33690e142037cab`
- `src/aiscc/providers/openai_responses.py` — `4efaffd726ab8211670830df7986bce782268b9e78eb3a0c37b4fdd27ca9cb6b`
- `src/aiscc/providers/service.py` — `ba47efd74a5210061d1a00d7eafe3d605b64128fee0895bc71fbe18fac276a83`
- `src/aiscc/public_live/luna_profile.py` — `172007a643b6de44ba3731b5c72a7419f3f79b7893dfc215ae2f2de7c83e4819`
- `src/aiscc/public_live/provider_authority.py` — `6acf2de7d327b459245e44847210732aa13ba182c0abbf11b79850e711a1854a`
- `src/aiscc/public_live/provider_pipeline.py` — `2d97410ff8de8741799d9fdc9618e4ffc75683ee8cb31bdddbb136997748c74d`
- `src/aiscc/security/policy.py` — `e174a6684bcd92ec7c2c07e83ae86b04325f591f6739f4ac8d5d50c2f4660874`
- `tests/fixtures/providers/luna_capabilities.py` — `d93edfff06d2df30ebfecfdfa995b34167ad378d1c6768b538827ac2d331eeba`
- `tests/integration/next_action/test_genesis_bootstrap.py` — `a96f0b4972dad5eefc11b842f2ff5af8ca10b1e00f371b2f2b52b850a28c2a62`
- `tests/integration/providers/test_external_ide_execution_ingress.py` — `c560ed6472b2e8b154f6b7f2d4921450977becf4bcaeae645cc3cf7407534e66`
- `tests/integration/providers/test_external_ide_execution_start.py` — `a327d6d82cfa81a9652bc3a3875d216a07e8747bff4c535e3c8e65f04cb7a483`
- `tests/integration/public_live/test_persistence.py` — `cf922670f41e9c05adbf997ab36e6d7f472b14da28119d22987d14aacd44f1ab`
- `tests/integration/public_live/test_provider_pipeline.py` — `52ccaf90f51e0d69108bf2c2f858c52a8cb31ca2b1bd5b758e6ec8e50190d71c`
- `tests/integration/self_dogfood/test_task_ready_entry.py` — `b04fdf8cbb4e2196c761702e029c67785cb7e9e66cd2c5b0071487d02e4e2fcf`
- `tests/integration/task_authority/test_task_contract_durability.py` — `c4bd92c84f1e530d4c2c63cf0d4cad9efcc80e6572b19549f0c1c6f5d523811e`
- `tests/integration/workflow/test_postgres_kernel.py` — `ba6d0adc03efd6a0351702b597ee81c5abf331b6d6971be11bf19bc3cdca196c`
- `tests/unit/providers/test_luna_profile.py` — `7061d136da7dd5b2b5f16c9ba997ac3b4a39c0bdc414c0292752e143ecd899a2`
- `tests/unit/providers/test_luna_tool.py` — `1785230dd8dfde95d97405a17ff82db98cd383f86d62ff5d65e09fd8933c516a`

## blocker

```text
PUBLIC_LIVE_L4_CALL_ROLE_PERSISTENCE_SCOPE_CONFLICT
→ RESOLVED_CANDIDATE
```

Substantive implementation is accepted; Git persistence is pending.

## L4 status

```text
provider policy:
HUMAN_PROVIDED / ACCEPTED V1

durable compatibility:
SUBSTANTIVE ACCEPTED

Luna binding:
SUBSTANTIVE ACCEPTED

Git persistence:
PENDING

account/provider evidence:
HUMAN_PENDING

L4 terminal:
OPEN
```

Remaining Human/account evidence:
- dedicated API Project reference/isolation
- Luna model access
- effective RPM/TPM
- billing health
- $15/month project hard-spend evidence
- $10/$12 alert evidence
- scoped real credential capability/reference
- separately authorized paid-provider verification

## next action
Git persistence only. After commit review, Browser may promote the call-role persistence blocker to `RESOLVED`, while L4 remains open for account/provider evidence.
