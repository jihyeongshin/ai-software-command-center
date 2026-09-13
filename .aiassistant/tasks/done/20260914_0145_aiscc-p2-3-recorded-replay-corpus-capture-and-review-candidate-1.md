# 작업지시서: P2-3 Recorded Replay corpus capture and review candidate

## meta
- created_at: `2026-09-14T01:45:36+09:00`
- repository: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- branch: `main`
- required_HEAD: `a1c934ea75906a548f2bc4adc777c2a0ecc99be5`
- required_parent: `33a216f29062176ad196a567a299ba30291c3f72`
- required_grandparent: `be2489515ba7799466ffdf415b47e4d3e0a79e46`
- accepted_0118_result_zip_sha256: `45a30b525a156b7b74d98e4dec5e95a8aa772cc564dd4d6e4726a517d2ffb6f4`
- governance_commit_authorized: `Yes / exact 3 paths`
- retained_PostgreSQL_read_authorized: `Yes / read-only Replay capture only`
- scenario_execution_authorized: `No`
- source_test_config_write_authorized: `No`
- canonical_state_write_authorized: `No`
- Human_action_authorized: `No`
- push_authorized: `No`
- success_ceiling: `RECORDED_REPLAY_CORPUS_CANDIDATE / BROWSER_REVIEW_PENDING`

# 0. phase boundary

S1-S4 minimum runtime proof is complete and Browser accepted.

Do not rerun, refine, repair or replace any scenario.

This Task performs only:

```text
A. exact governance persistence
B. retained durable-state read-only capture
C. sanitization
D. four-scenario Recorded Run Replay candidate generation
E. no-inference/integrity verification
```

P2-3 terminal closure is NOT authorized in this Task.

# 1. executables

Repository:

```text
C:\Users\oracl\IdeaProjects\ai-software-command-center
```

Python:

```text
<repository-root>\.venv\Scripts\python.exe
```

Use only this interpreter.

Forbidden:

```text
python
py
WindowsApps
PATH Python discovery
repository-external Python/venv discovery
```

Docker read-only inspect executable:

```text
C:\Program Files\Docker\Docker\resources\bin\docker.exe
```

Git:

```text
C:\Program Files\Git\cmd\git.exe
```

# 2. repository baseline

Require:

```text
branch main
HEAD a1c934ea75906a548f2bc4adc777c2a0ecc99be5
HEAD^ 33a216f29062176ad196a567a299ba30291c3f72
HEAD^^ be2489515ba7799466ffdf415b47e4d3e0a79e46
index empty
tracked clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0118_aiscc-p2-3-s3-s4-source-persistence-and-fresh-private-runtime-retry-1.md

SHA-256:
860950e56d0bb65585346d41215fba2e097d90293cb97194e551702765af199a
```

Canonical state must remain:

- `.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md`  `281bd733624ac87be207f62ed59b99edf0d64cf3b8f3d00e9bc9611fe3179f8c`
- `.aiassistant/records/aiscc/DECISION_REGISTER.md`  `b55eb504c39af0134837f808eef8610b0c54505ee8c597b332f79148ad61d8bd`
- `.aiassistant/records/aiscc/NEXT_ACTIONS.md`  `1bb251b5758e8fea1ac260dcace074dcb7e2ff9adf6a96e8699d29c66bea495d`

Preserve ignored non-owned legacy:

```text
.aiassistant/tasks/active/20260912_1400_aiscc-p2-3-private-s1-cut-b-temporary-context-cleanup-and-final-proof-1.md
SHA-256 52230841817ccbbaf98b72eef1ddf05d8b438f550df45b3a73f8824cd0a7d6fb
```

After current Cycle/Judgment placement while current Task remains active/ignored:

```text
Git-visible untracked exactly three:
- 0118 done Task
- current Cycle
- current Judgment
```

Mismatch → STOP before Git/private access.

# 3. Commit A — exact governance persistence

Stage exactly:

```text
.aiassistant/tasks/done/20260914_0118_aiscc-p2-3-s3-s4-source-persistence-and-fresh-private-runtime-retry-1.md
.aiassistant/records/aiscc/cycles/20260914_0145_aiscc-p2-3-s1-s4-runtime-complete-recorded-replay-entry-1.cycle.md
.aiassistant/reports/aiscc/20260914_0145_aiscc-p2-3-0118-scenario-runtime-final-acceptance-replay-authorization-1.md
```

Commit message exactly:

```text
docs(aiscc): admit scenario runtime replay entry
```

Require:

```text
Commit A parent = a1c934ea75906a548f2bc4adc777c2a0ecc99be5
changed paths = exact 3
current active Task not staged
canonical state not staged
legacy 1400 not staged
```

After Commit A:

```text
HEAD = Commit A
index empty
tracked clean
Git-visible untracked = 0
```

Any failure → STOP before retained DB access.

# 4. exact accepted Replay subjects

The corpus contains exactly these four accepted durable runs:

- S1: `stockroom-s1-normal` / `aiscc-p2-3-private-s1-normal-v5-run` / final `ACCEPTED` / Judgment `ACCEPTED` / Human `NOT_REQUIRED` / execution commit `e7d7a44379eb0dc71f7b8d2207c6ca3719a0a211`
- S2: `stockroom-s2-missing-evidence` / `aiscc-p2-3-private-s2-missing-evidence-v6-run` / final `REWORK_REQUIRED` / Judgment `HOLD_REWORK_REQUIRED` / Human `NOT_REQUIRED` / execution commit `33a216f29062176ad196a567a299ba30291c3f72`
- S3: `stockroom-s3-policy-conflict` / `aiscc-p2-3-private-s3-policy-conflict-v9-run` / final `BLOCKED` / Judgment `NONE` / Human `NOT_REQUIRED` / execution commit `a1c934ea75906a548f2bc4adc777c2a0ecc99be5`
- S4: `stockroom-s4-human-owned-claim` / `aiscc-p2-3-private-s4-human-owned-claim-v10-run` / final `HUMAN_REQUIRED` / Judgment `NONE` / Human `PENDING` / execution commit `a1c934ea75906a548f2bc4adc777c2a0ecc99be5`

No other historical/failed/stranded run may become a public Replay member.

Especially exclude:

```text
0036 invalid history
1822 failed provider-grant run
2040 v4 partial S1
stranded S3 v7
all Task-contract blocker runs without accepted scenario semantic
```

# 5. retained PostgreSQL read-only boundary

After Commit A only, reverify exact retained PostgreSQL identity from accepted 0118 evidence.

Acquire the secret only for the DB connection without printing/exporting it.

Connection/session must be read-only:

```text
transaction:
READ ONLY

scenario application builder:
0

prepare_capture:
0

StockroomCaptureRunner:
0

provider operations created:
0

tool operations created:
0

HumanResult created:
0

Workflow transition mutation:
0

Evidence/Judgment/HumanGate mutation:
0
```

Capture before/after durable table counts/fingerprints sufficient to prove zero mutation.

Do not inspect or mutate private runtime roots. Replay comes from durable database/event/evidence authority, not workspace files.

# 6. source-owned Replay path audit

Before generating public JSON, inspect the current repository read-only for existing Replay/read-only projection APIs.

At minimum identify:

```text
Replay/read-only repository or projection types
transition provenance reader
evidence-set/admitted-evidence metadata reader
HumanGate/HumanResult reader
Judgment reader
WorkRun/ExecutionAttempt reader
```

Prefer existing source-owned read-only APIs.

If no single Replay composer exists, a Task-local read-only exporter may compose the public projection from those authoritative repositories/models.

It must not:
- fabricate missing data;
- infer a terminal state not stored;
- call production execution;
- mutate durable data.

Report exact source APIs used.

# 7. public Replay schema

Create exactly four UTF-8 JSON public candidates under the export bundle:

```text
replay/stockroom-s1-normal.json
replay/stockroom-s2-missing-evidence.json
replay/stockroom-s3-policy-conflict.json
replay/stockroom-s4-human-owned-claim.json
```

Each JSON must contain at minimum:

```text
replay_kind = RECORDED_RUN_REPLAY

display_label = Recorded Run Replay

truthful_notice =
This is a replay of a previously executed AISCC workflow.

no_inference_notice =
No LLM inference is performed while viewing this replay.

recorded_at
executed_at_start
executed_at_end_or_terminal_observation

scenario:
id
version

synthetic_repository:
name
commit = 05185c57a6265a4002050ce25cdfde3dc87e9779
source_aggregate_sha256 = be3dbe304904048b47ebe5e31d78c60a10572f7bc2931fd4058994585eba300d

orchestrator:
execution_commit

public replay_id
source_run_fingerprint_sha256

final workflow state
state version

transition trace:
ordered authoritative transitions
admission/denial reason summary

execution summary:
attempt status/version
provider/tool counts
external inference = 0 for these captured private runs as actually observed

evidence summary:
checkpoint/ref metadata
requirement-set outcome
admitted/rejected ownership summary
coverage keys when PUBLIC_SAFE
no raw body

agent_claim_vs_system_admission summary

Human:
required/not-required/pending/result status
gate state when applicable

Judgment:
kind/status or explicit NONE
```

Do not publish raw internal source run IDs. Use a stable public replay ID and SHA-256 fingerprint of the source run ID.

# 8. scenario truthfulness requirements

## S1

Public projection must truthfully show:

```text
final:
ACCEPTED

Judgment:
ACCEPTED

Human:
NOT_REQUIRED

execution:
completed

admitted evidence:
present
```

## S2

```text
final:
REWORK_REQUIRED

JudgmentKind:
HOLD_REWORK_REQUIRED

evidence set:
UNSATISFIED for missing required evidence

Human:
NOT_REQUIRED
```

Do not relabel HOLD_REWORK_REQUIRED as ACCEPTED/REJECTED.

## S3

```text
final:
BLOCKED

blocker:
POLICY / POLICY_CONFLICT

provider:
0

tool:
0

Judgment:
NONE

HumanResult:
NONE

static policy evidence:
admitted metadata only
```

Do not include the static fixture body.

## S4

```text
final:
HUMAN_REQUIRED

PRE_HUMAN evidence:
SATISFIED

HumanGate:
PENDING / durable

HumanResult:
NONE

Judgment:
NONE

Agent Human claim:
REJECTED / did not become HumanResult
```

Do not make the replay appear to contain a Human decision that never occurred.

# 9. timestamps and execution commit

For each run, read actual durable execution/transition timestamps.

Do not invent a start/end time.

`recorded_at` is this Replay-capture time and is distinct from original execution timestamps.

Execution commit must equal the commit under which that run was actually executed:

```text
S1:
e7d7a44379eb0dc71f7b8d2207c6ca3719a0a211

S2:
33a216f29062176ad196a567a299ba30291c3f72

S3:
a1c934ea75906a548f2bc4adc777c2a0ecc99be5

S4:
a1c934ea75906a548f2bc4adc777c2a0ecc99be5
```

If durable provenance cannot support the expected execution commit directly, use accepted governance plus exact workspace/source provenance and report the evidence class. Do not silently substitute current HEAD.

# 10. sanitization boundary

Public Replay JSON must exclude:

```text
password
credential
DB URL
private host path
private runtime root
Docker secret bind source
raw Docker inspect
raw ACL
company/customer/private repository material
private evidence body
private prompt/context
stack trace
internal temporary helper path
```

No source file contents are included.

Synthetic repository identity/commit/hash is allowed.

Evidence exposure is metadata-first:
- profile/kind;
- requirement/checkpoint identity if public-safe;
- coverage keys;
- result/outcome;
- content SHA if useful.

Raw durable evidence body remains excluded even when source-owned unless the Task can prove explicit PUBLIC_SAFE admission and that body is necessary. For minimum corpus, raw body is not necessary: exclude all raw bodies.

# 11. Recorded Replay labeling

Every member must include exactly truthful Replay labels:

```text
Recorded Run Replay

This is a replay of a previously executed AISCC workflow.

No LLM inference is performed while viewing this replay.
```

Forbidden public copy:

```text
Live
AI is working now
current token stream
current reasoning
running now
```

except where a field explicitly says `live=false` or explains that Replay is not Live.

# 12. integrity and corpus index

Create:

```text
REPLAY_CORPUS_INDEX.json
```

It must list exactly four members with:

```text
replay_id
scenario_id
scenario_version
final_state
member_relative_path
member_sha256
member_bytes
source_run_fingerprint_sha256
execution_commit
recorded_at
```

Create one deterministic corpus integrity root from the ordered canonical tuple:

```text
scenario_id
member_sha256
member_bytes
```

Record the algorithm unambiguously.

No duplicate scenario IDs or member paths.

# 13. no-inference verification

Prove across the Task:

```text
build_stockroom_production calls:
0

prepare_capture calls:
0

StockroomCaptureRunner calls:
0

new ExecutionAttempt:
0

new provider operation:
0

new tool operation:
0

new transition decision:
0

new admitted evidence:
0

new HumanGate/HumanResult:
0

new Judgment:
0

external provider/LLM:
0

arbitrary outbound network:
0
```

Read-only Docker inspect for retained PostgreSQL identity is not scenario execution.

# 14. replay integrity review

For all four public JSONs:

```text
parse:
PASS

UTF-8:
PASS

scenario allowlist:
exact

final semantic:
matches durable state

transition order:
matches durable transition provenance

evidence ownership:
matches durable admission/rejection

Human/Judgment:
matches durable rows and absence

member SHA/size:
matches index

private-value scan:
PASS
```

No Replay artifact is admitted as canonical/public yet. This Task produces a Browser review candidate only.

# 15. IP/license boundary

Replay contains:
- metadata/provenance for AISCC-owned workflow;
- Stockroom synthetic repository identity/version;
- system-generated state/evidence summaries.

It must contain no copied third-party source content or private/company/customer materials.

Record:

```text
synthetic repository:
project-owned / P2-2 accepted source

source code contents:
not embedded

third-party media/assets:
none

private/company/customer data:
none
```

If this cannot be established, STOP with `REPLAY_IP_SANITIZATION_BLOCKED`.

# 16. canonical-state / Git boundary

Do not modify canonical state in this Task.

Do not add Replay JSON to repository canonical paths yet.

They remain export candidate artifacts pending Browser review.

After Commit A no tracked mutation is authorized.

Move current Task active→done byte-identically.

Final:

```text
HEAD = Commit A
index empty
tracked clean

Git-visible untracked exactly one:
.aiassistant/tasks/done/20260914_0145_aiscc-p2-3-recorded-replay-corpus-capture-and-review-candidate-1.md

legacy 1400:
preserved / ignored / non-owned
```

No push.

# 17. contract review

Exactly 73 rows:

```text
TRANSPORT_PACKAGE_EXACT
BASE_HEAD_PARENT_EXACT
INITIAL_INDEX_EMPTY_TRACKED_CLEAN
INITIAL_UNTRACKED_0118_DONE_TASK_ONLY
PREDECESSOR_0118_RESULT_ACCEPTED
CURRENT_STATE_HASHES_EXACT
LEGACY_1400_ACTIVE_PRESERVED
PYTHON_REPOSITORY_VENV_EXACT
COMMIT_A_STAGE_SET_EXACT_3
COMMIT_A_PARENT_EXACT
COMMIT_A_MESSAGE_EXACT
COMMIT_A_CHANGED_PATHS_EXACT_3
POST_COMMIT_INDEX_EMPTY_TRACKED_CLEAN
POST_COMMIT_UNTRACKED_ZERO
NO_CANONICAL_STATE_MUTATION
PRIVATE_POSTGRES_IDENTITY_EXACT
PRIVATE_SECRET_BOUNDARY_EXACT
REPLAY_READ_ONLY_TRANSACTION_ENFORCED
S1_REPLAY_SOURCE_RUN_EXACT
S2_REPLAY_SOURCE_RUN_EXACT
S3_REPLAY_SOURCE_RUN_EXACT
S4_REPLAY_SOURCE_RUN_EXACT
S1_REPLAY_FINAL_SEMANTIC_EXACT
S2_REPLAY_FINAL_SEMANTIC_EXACT
S3_REPLAY_FINAL_SEMANTIC_EXACT
S4_REPLAY_FINAL_SEMANTIC_EXACT
SCENARIO_EXECUTION_COMMIT_PROVENANCE_EXACT
SYNTHETIC_REPOSITORY_PROVENANCE_EXACT
REPLAY_SOURCE_DURABLE_EVENTS_ONLY
REPLAY_NO_BUILDER_PREPARE_RUNNER
REPLAY_PROVIDER_TOOL_EXECUTION_ZERO
REPLAY_EXTERNAL_INFERENCE_ZERO
REPLAY_DB_MUTATION_ZERO
REPLAY_RUNTIME_ROOT_MUTATION_ZERO
REPLAY_LABEL_RECORDED_RUN_EXACT
REPLAY_NO_LIVE_LABELING
REPLAY_EXECUTION_AND_RECORDING_TIMESTAMPS_PRESENT
REPLAY_TRANSITION_TRACE_PRESENT
REPLAY_EVIDENCE_OWNERSHIP_SUMMARY_PRESENT
REPLAY_AGENT_CLAIM_VS_ADMISSION_PRESENT
REPLAY_HUMAN_STATE_PRESENT
REPLAY_JUDGMENT_STATE_PRESENT
S1_PUBLIC_REPLAY_JSON_VALID
S2_PUBLIC_REPLAY_JSON_VALID
S3_PUBLIC_REPLAY_JSON_VALID
S4_PUBLIC_REPLAY_JSON_VALID
S4_PENDING_HUMAN_TRUTHFUL
S3_NO_JUDGMENT_TRUTHFUL
S2_HOLD_REWORK_JUDGMENT_TRUTHFUL
S1_ACCEPTED_JUDGMENT_TRUTHFUL
PUBLIC_REPLAY_NO_RAW_EVIDENCE_BODY
PUBLIC_REPLAY_NO_PRIVATE_RUN_PATH
PUBLIC_REPLAY_NO_SECRET_CREDENTIAL_DB_URL
PUBLIC_REPLAY_NO_COMPANY_CUSTOMER_MATERIAL
PUBLIC_REPLAY_ONLY_SYNTHETIC_SOURCE_PROVENANCE
PUBLIC_REPLAY_STABLE_REPLAY_IDS_PRESENT
PUBLIC_REPLAY_SOURCE_RUN_FINGERPRINT_PRESENT
REPLAY_CORPUS_INDEX_VALID
REPLAY_CORPUS_MEMBER_HASHES_EXACT
REPLAY_CORPUS_FOUR_SCENARIOS_EXACT
REPLAY_CORPUS_NO_DUPLICATE_SCENARIO
REPLAY_CORPUS_NO_FABRICATED_TERMINAL
REPLAY_CORPUS_INTEGRITY_ROOT_PRESENT
PRIVATE_VALUE_EXPORT_SCAN_PASS
NO_S1_S2_S3_S4_RERUN
NO_HUMAN_RESULT_CREATION
NO_SOURCE_TEST_CONFIG_STATE_MUTATION
NO_GIT_PUSH
CURRENT_TASK_ACTIVE_TO_DONE_BYTE_EXACT
FINAL_HEAD_IS_COMMIT_A
FINAL_INDEX_EMPTY_TRACKED_CLEAN
FINAL_UNTRACKED_CURRENT_DONE_TASK_ONLY
EXPORT_INTEGRITY_PASS
```

Full candidate success:

```text
73 / 73 PASS
```

# 18. export

Root docs:

```text
EXPORT_MANIFEST.md
TASK.md
EXECUTOR_REPORT.md
WORKSPACE_VERIFICATION.md
0118_ACCEPTANCE_VERIFICATION.md
SOURCE_PERSISTENCE_VERIFICATION.md
PRIVATE_REPLAY_SOURCE_VERIFICATION.md
REPLAY_SOURCE_API_AUDIT.md
REPLAY_SANITIZATION_VERIFICATION.md
REPLAY_NO_INFERENCE_VERIFICATION.md
REPLAY_INTEGRITY_VERIFICATION.md
REPLAY_IP_LICENSE_VERIFICATION.md
PRIVATE_VALUE_SCAN.md
CONTRACT_REVIEW.md
REPLAY_CORPUS_INDEX.json
```

Also include:

```text
replay/stockroom-s1-normal.json
replay/stockroom-s2-missing-evidence.json
replay/stockroom-s3-policy-conflict.json
replay/stockroom-s4-human-owned-claim.json
current Cycle
current Judgment
current done Task
```

Generate export manifest/member counts from actual set.

Require:

```text
one top-level
CRC PASS
manifest SHA/size exact
TASK.md == canonical done Task
public Replay JSON scans PASS
private-value/path scan PASS
```

# 19. success ceiling

```text
S1-S4 runtime:
ACCEPTED / COMPLETE

Recorded Replay corpus:
CANDIDATE READY

Replay public admission:
PENDING BROWSER REVIEW

P2-3 terminal persistence:
NOT_STARTED

P2-3 closure:
NOT_STARTED

P2-4:
NOT_STARTED
```
