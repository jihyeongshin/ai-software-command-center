# AISCC Browser Command Center Session HANDOFF
## Fourth Command Center → Fifth Command Center: P1-8 Runtime Commit A Fresh-IDE-Session Resume

## 0. 문서 메타데이터

- document_type: `COMMAND_CENTER_SESSION_HANDOFF`
- project: `AI Software Command Center (AISCC)`
- generated_at: `2026-09-02T16:21:00+09:00`
- source_session_role: `fourth Browser Command Center`
- intended_next_session_role: `fifth Browser Command Center`
- continuation_mode: `GPT Project / Work mode`
- transfer_reason: `The 1400 submitted bundle has received substantive judgment; current workflow now requires Cycle-only judgment persistence plus Browser-session migration before any next Task issuance.`
- repository_canonical_root: `C:\Users\oracl\IdeaProjects\ai-software-command-center`
- repository_remote: `https://github.com/jihyeongshin/ai-software-command-center.git`
- repository_branch_reported_by_latest_executor: `main`
- repository_HEAD_reported_by_latest_executor: `1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a`
- competition: `Wanted AI Championship 2026`
- competition_deadline: `2026-09-20`
- canonical_handoff_target: `.aiassistant/reports/aiscc/20260902_1621_aiscc-browser-command-center-session-handoff-p1-8-runtime-commit-a-fresh-chat-resume-1.md`
- judgment_cycle: `.aiassistant/records/aiscc/cycles/20260902_1621_aiscc-p1-8-runtime-commit-a-fresh-chat-precondition-blocked-1.cycle.md`
- judgment_cycle_sha256: `0c3f2b98ed7deb96956cf2ef4e93e747870c94d20f4adf9b20fbc07228f80952`
- next_Task_issued_by_source_session: `No`

### Intended next-session context assumptions

The fifth Browser Command Center must assume:

```text
old Browser chat memory: unavailable
old IDE Executor chat history: unavailable to Browser
File Library continuity: unavailable as authority
GPT Project Source: available but possibly stale
this HANDOFF: available and required
repository local canonical: ultimate authority, accessible only through a new Task/Executor result
```

This document is deliberately more than a next-action note. It is the fourth session's complete continuation
anchor at the level of the `20260901_1444` bootstrap Handoff received when this session began.

---

# 1. 이 HANDOFF의 사용 규칙

The fifth Browser Command Center must be able to reconstruct all of the following from this document and Project
Source without relying on hidden chat history:

1. the product thesis and authority model;
2. the accepted predecessor state through P1-8 runtime Human acceptance;
3. the exact Git/runtime state reported by the latest Executor;
4. why the 1400 Task did not perform restore or Commit A;
5. which Human decisions remain valid;
6. what the next Browser session may issue and what this fourth session intentionally did not issue;
7. how Browser, Human and IDE Executor responsibilities are separated;
8. what must never be promoted to P1-8 closure or P2 entry.

## 1.1 Authority precedence

```text
local AISCC repository canonical
> terminally persisted accepted Cycle / accepted rule / accepted commit
> this HANDOFF continuation anchor
> GPT Project Source read-only mirror
> Browser/IDE chat memory
```

The attached Project Source files are a read-only P0-era mirror. In particular, their phase tables can still say
`P1-1 NOT_STARTED`. That snapshot must not cause a fifth-session restart of P0 or early P1 work.

When this Handoff and Project Source differ only because Project Source is older:

```text
do not rerun old phases
do not overwrite newer canonical state from the old mirror
first verify exact paths/hashes/HEAD through the local repository
```

This Handoff does not replace local canonical Git facts. It tells the next Command Center exactly what must be
reconciled before it creates new execution authority.

---

# 2. 프로젝트 목적과 고정된 제품 baseline

AISCC's accepted one-sentence thesis is:

```text
AISCC는 Coding Agent 자체가 아니라, AI가 수행한 software work를
Task Contract, authority, task-scoped evidence ownership, proof admission,
system-owned state transition, Human judgment, durable Cycle provenance 아래에서 통제하는
Software Engineering Governance Control Plane이다.
```

The orchestration core is a directly implemented explicit state machine. LangGraph is not used as the
orchestration core. This is a product/competition differentiation decision, not a temporary implementation detail.

The primary operator is a software technical lead who must control work performed by one or more coding agents,
determine which proof is admissible, distinguish Agent output from system state, preserve Human-owned decisions,
and retain durable public provenance.

The default public competition surface is Replay-first with bounded Live capability. Public release, deployment,
provider billing and competition submission are not part of the current P1-8 terminal-persistence work.

---

# 3. 반드시 유지할 non-substitution invariants

```text
AGENT_OUTPUT != SYSTEM_STATE
AGENT_CLAIM != ADMITTED_EVIDENCE
HUMAN_OWNED_EVIDENCE != EXECUTOR_COMPLETED

ExecutionStatus != WorkflowState
EXECUTOR_COMPLETED != ACCEPTED
EXECUTION_FAILED != FAILED

EvidenceCandidate != AdmittedEvidence
AdmittedEvidence != Judgment
AdmittedEvidence != TransitionDecision
AdmittedEvidence != WorkflowState

HumanResult != Judgment
Command Center recommendation != Human acceptance

CommandCenterCycleRecord != AdmittedCycle
raw session != ProjectMemory

ProjectMemoryEntry != canonical policy authority
ProjectMemoryEntry != TaskContract

MemoryRetrievalResult != AdmittedEvidence
MemoryRetrievalResult != Judgment

NextActionProposal != NextActionSelection
NextActionSelection != TransitionDecision

TaskIssuanceCandidate != TaskContract
tasks/done != accepted
Executor PASS != Command Center acceptance
ACCEPTED_CANDIDATE != CLOSED
```

Terminal workflow remains:

```text
TERMINAL_TRANSITION
→ SYSTEM_ADMISSION
→ HUMAN_GATE_WHEN_REQUIRED
```

P1-8 runtime Human acceptance has occurred. It does not by itself prove Git persistence, canonical state update,
Commit B, P1 closure, mirror sync or P2 entry.

---

# 4. Browser Command Center ↔ Human ↔ IDE Executor workflow

## 4.1 Responsibility boundary

### Browser Command Center

- classifies work and authority gaps;
- issues detailed Task files only when the current Browser session is allowed to issue one;
- substantively reviews submitted bundles;
- admits/rejects evidence by owner and proof type;
- persists judgment in Cycle records;
- requests Human gates without self-minting Human results;
- creates a detailed Handoff when migrating Browser sessions.

### Human

- downloads and transports Task/Cycle artifacts;
- opens a new Browser or IDE chat when there is a stated reason;
- performs Human-only acceptance, policy, visual/runtime and release gates;
- supplies exact decision codes such as `ACCEPTED` or `RESTORE_SIX_TO_EXACT_HEAD`;
- must not be told that an IDE Executor can open its own chat.

### IDE Executor

- cannot open a new chat session by itself;
- reads the Task-listed canonical context;
- acts only within exact path/action authority;
- stops before mutation when a prerequisite, identity or authority condition fails;
- moves Task active→done only as lifecycle provenance;
- exports the exact report/evidence bundle for Browser judgment.

## 4.2 New Browser-session rule established at this handoff

After a submitted Executor bundle receives substantive judgment:

```text
do not issue the next Task in that same Browser Command Center session
→ issue the judgment Cycle
→ issue a bootstrap-level Handoff
→ Human opens the next Browser Command Center session
→ the next Browser session owns any next Task issuance
```

This fourth session therefore issues no successor Task after judging the 1400 bundle.

## 4.3 IDE new-chat rule

`새로운 채팅세션을 열어라` is a Human action, not an Executor command. A new IDE chat requires a concrete ground.

For the pending work, that ground is already established:

```text
1300 work type: read-only dirty-baseline audit
next work type: destructive exact-path restore + Git Commit A
authority change: read-only → destructive worktree/index/commit authority
```

The next Browser session must state this ground when it instructs the Human to open the new IDE chat.

## 4.4 Downloads transport rule

When a Task and Cycle must be delivered together, the short prompt must specify:

```text
Task Downloads source → exact .aiassistant/tasks/active destination
Cycle Downloads source → exact .aiassistant/records/aiscc/cycles destination
Move, not Copy
```

Before moving either file, verify atomically that:

1. both exact Downloads source files exist; and
2. both exact destination filenames do not exist.

If any source is missing or any destination collision exists:

```text
move neither file
do not search another path
stop immediately
```

The short prompt transports placement and execution only. The Task file contains the long authority/evidence
contract.

---

# 5. Browser Command Center session lineage

- first Command Center: early AISCC design/orchestration/product baseline and P0/P1 initiation;
- second Command Center: continued P1 execution and accumulated extensive context;
- third Command Center: continued P1-8 work and supplied its workflow-accounting answer;
- fourth Command Center: the current session; bootstrapped from the `20260901_1444` Handoff, reconciled P1-8
  authority/runtime/Git lineage, judged 1619→1400 successors, captured Human workflow corrections, and now ends
  after the 1400 bundle judgment;
- fifth Command Center: must bootstrap from this Handoff and the 1621 Cycle, then own the next Task issuance.

The `20260901_1444` received Handoff identity is:

```text
20260901_1444_aiscc-p1-8-command-center-session-handoff-next-action-context-acceptance-and-prerequisite-resume-1.md
SHA-256: a44d5336d23a689e4a48a74ce87bbc89216e573e0793fe30178e115c11663700
```

It described an earlier state around 1619 source-authority terminal persistence. The current Handoff supersedes its
next-action state while preserving its thesis, authority and non-substitution baseline.

---

# 6. Phase state at this handoff

The following state reflects the fourth-session accepted lineage, not the stale Project Source table:

```text
P0
→ accepted/closed bootstrap, product thesis, canonical authority and source-mirror foundation

P1-1 through P1-5
→ accepted predecessor work

P1-6 core and durable evidence-content extension
→ design/runtime accepted and closed

P1-7
→ design/runtime accepted and closed

P1-8 design and prerequisite/source-authority design lineage
→ accepted predecessors

P1-8 runtime exact 36 bytes
→ Human final review ACCEPTED
→ terminal Git persistence NOT completed

P1-8 dirty-baseline disposition
→ Human selected RESTORE_SIX_TO_EXACT_HEAD
→ authority remains valid and unused

P1-8 Runtime Commit A
→ NOT_CREATED

P1-8 canonical governance Commit B / final closure
→ NOT_STARTED for this terminal sequence

P1 overall
→ NOT_CLOSED

P2
→ NOT_STARTED

PUBLIC_BOUNDED_LIVE
→ NOT_RELEASED
```

No future session may promote the Human-accepted runtime candidate into `P1-8 CLOSED` until exact Commit A,
substantive Commit A review, terminal governance/canonical persistence and any required Human gate are all proven.

---

# 7. Important fourth-session Human decisions

## Decision A — P1-8 runtime acceptance

Human supplied:

```text
Human P1-8 runtime final review
판정: ACCEPTED
```

Scope is only the exact accepted 36 runtime bytes identified below. It does not accept six unrelated tracked
formatting-shaped diffs and does not accept later mutation.

## Decision B — dirty-file disposition

After the 1300 audit isolated exact six unaccepted tracked diffs, Human selected:

```text
RESTORE_SIX_TO_EXACT_HEAD
```

This permits discarding only those six exact current byte states and restoring only those six exact repository
paths from exact expected HEAD. It is not broad cleanup authority.

## Decision C — short prompt transport

Human corrected the workflow so that the short prompt must not make them alternate unpredictably between leaving
Task files in Downloads and placing them manually in active. It now consistently directs the Executor to Move the
exact Downloads files into the exact repository paths, with all-or-nothing prechecks and no alternate search.

## Decision D — chat creation authority

Human established that an IDE Executor cannot open a new chat. Human performs chat creation, and a new chat must be
justified by an explicit authority/context boundary.

## Decision E — post-judgment Browser migration

Human established for this continuation:

```text
after bundle judgment: no next Task from the same Browser session
issue Cycle only for judgment persistence
issue detailed Handoff
migrate to a new Browser Command Center session
```

---

# 8. 1300 dirty-baseline audit result

The 1300 submitted ZIP was independently reviewed in this fourth session.

```text
bundle:
20260902_1300_aiscc-p1-8-terminal-dirty-baseline-provenance-reconciliation-audit-1.zip

SHA-256:
e7b74a6b685071ad7cbe43d165d36cee9946f42e9195b2e83fd05274a47e164a

Command Center result:
DIRTY_BASELINE_AUDITED / COMMAND_CENTER_REVIEW_REQUIRED / TERMINAL_COMMIT_PLAN_BLOCKED
```

Admitted findings:

- 19 manifest rows and 19 payload files matched; no hash/UTF-8 failure;
- exact accepted 36 current byte identities passed `36/36`;
- corrected ordinal aggregate:
  `a82d94c1d607bc379c12d0768ff54d0cd481467eb731e0884f63176bd1207f3c`;
- legacy provider-last identifier:
  `a1d5e9d24eabae3fec13e24cfb9d94e744e6687ca4c00889e85972fb5a633590`;
- current runtime dirty 42 = accepted 36 + exact six unrelated tracked formatting-shaped diffs;
- seven of the earlier thirteen extras were accepted predecessor runtime and belong in the accepted 36;
- the six exact diffs were not accepted and required Human disposition before Commit A staging.

The Human's `RESTORE_SIX_TO_EXACT_HEAD` decision resolved the disposition choice but did not itself perform the
restore.

---

# 9. 1400 Task and submitted bundle judgment

## 9.1 Task identity

```text
.aiassistant/tasks/done/
20260902_1400_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-1.md

SHA-256:
b19b51eed1935cf0144038eb7c6b68c9ec0b71eff82d01c7a0c083dd02d18c76
```

Its intended goal was:

```text
verify exact current state
→ verify six AST/token equivalence
→ restore exact six to exact HEAD
→ verify runtime dirty 42→36
→ stage exact accepted 36 only
→ create one exact Commit A
→ export Commit A tree proof
→ stop for Command Center review
```

Its explicit session condition was:

```text
fresh_chat_policy: NEW_CHAT_REQUIRED_BY_HUMAN
reason: read-only 1300 audit → destructive restore and Git commit authority
```

## 9.2 Submitted ZIP identity and integrity

```text
20260902_1400_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-1.zip
SHA-256: e0eb6bbdd42a1fc00a7dfa2a619bd89421d88acc164f4f4dbb6763ac5cb2f9f8
```

Independent Browser Command Center verification:

- archive contains one root and six Markdown files;
- `EXPORT_MANIFEST.md` declares five payloads excluding itself;
- all five declared payload rows match file presence, exact byte count, copy SHA-256 and source SHA-256;
- `TASK.md` exactly matches the issued Task hash;
- all six Markdown files decode as UTF-8 without BOM;
- no forbidden control characters or trailing whitespace;
- zero Commit A source copies is consistent with the pre-mutation blocker because Commit A does not exist.

## 9.3 Executor outcome

```text
BLOCKED_REQUIRED_EVIDENCE / FRESH_CHAT_PRECONDITION_NOT_SATISFIED
restore performed: No
staged paths: 0
Commit A: NOT_CREATED
```

The Task was delivered in the IDE Executor thread that had completed the 1300 audit. The Executor correctly
recognized that this was not a Human-opened new IDE chat and stopped before destructive work.

## 9.4 Command Center judgment

```text
ACCEPTED_AS_ACCURATE_BLOCKED_RESULT
/ TASK_NOT_COMPLETED
/ FRESH_CHAT_PRECONDITION_NOT_SATISFIED
```

Accepted scope:

- correctness of mandatory-stop behavior;
- preservation of source/index/HEAD;
- read-only preflight evidence;
- exact blocked-result report/export integrity.

Not accepted or completed:

- AST/token equivalence gate;
- six restoration;
- post-restore 36-path state;
- Ruff/mypy/diff checks;
- staging;
- Commit A;
- canonical update or Commit B;
- P1-8/P1 closure;
- P2 entry or release.

The exact judgment Cycle is:

```text
.aiassistant/records/aiscc/cycles/
20260902_1621_aiscc-p1-8-runtime-commit-a-fresh-chat-precondition-blocked-1.cycle.md

SHA-256:
0c3f2b98ed7deb96956cf2ef4e93e747870c94d20f4adf9b20fbc07228f80952
```

---

# 10. Exact reported repository state after 1400

These facts come from the internally consistent 1400 Executor export and must be revalidated in the next genuine
IDE session before any mutation:

```text
repository: ai-software-command-center
branch: main
HEAD: 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
index entries: 0
runtime dirty paths: 42
accepted runtime paths: 36
unaccepted tracked restore candidates: 6
governance dirty before 1400 Task lifecycle: 11
governance dirty after 1400 Task lifecycle: 12
Commit A: NOT_CREATED
canonical state: unchanged
Commit B: NOT_CREATED
```

The accepted 36 aggregate remains:

```text
a82d94c1d607bc379c12d0768ff54d0cd481467eb731e0884f63176bd1207f3c
```

The six current bytes remain present exactly as they were before the 1400 attempt. No rollback is required because
no restore, staging or commit occurred.

---

# 11. Exact six Human-authorized restore paths

The next Task may preserve the same Human authority only if every current identity and expected HEAD object is
revalidated exactly. Any mismatch requires a pre-mutation stop and a new Command Center judgment.

| path | current SHA-256 authorized to discard | expected HEAD blob SHA-1 |
|---|---|---|
| `src/aiscc/evidence/content.py` | `86fec26a717ec99878d0cd2b69860d2e27aeb30d1a76f1f1e53d1d773611f804` | `63f0334f55aee58297a9bc357493bef4c5dacc50` |
| `src/aiscc/evidence/models.py` | `7617ad5e9ba531df0ff2b673dff30312889838f61db53395ea344d1ecdd083aa` | `ad72df4dd84a6a5a4863fc3f28a5af1b115b09f1` |
| `src/aiscc/evidence/repository.py` | `db235bb078befbc5afdd5a042410f126e61493ea7818d5adf0e3f223fd9cd9bb` | `c8caa06b12248e27b6b0f345632544302711c81f` |
| `src/aiscc/evidence/requirements.py` | `7fa93582e21bad5bcedbd1c4eed70e3330d8943610891b625e44f028049c0f79` | `a0be7227377853c0cabb12108e74faaa83fba618` |
| `src/aiscc/evidence/service.py` | `0b25caf58eda7b5ae5eb2662b113371e400f82f8bbaa36c1454f26679edcd0b0` | `1d29c39531af55678611b84a4f7f7c4b6df2785e` |
| `src/aiscc/human/repository.py` | `1ed1d466ec056562433c347bbe903356badd5999656e15118fa8d6ef048e51ea` | `75dfaa00a315696a5b5bd08f0128b290fda7a66b` |

The 1400 report also recorded the current worktree blob SHA-1 values:

```text
src/aiscc/evidence/content.py       806633d46d13e4cfac54cec7d9e0e19ca91a4e45
src/aiscc/evidence/models.py        d932babe2097a06139eef9d7aefa2468dab8041c
src/aiscc/evidence/repository.py    9b5e9361a263049afbc4c211471cd30f2dfc0c93
src/aiscc/evidence/requirements.py  8ded3c9599b26d2c870d35f56f73e768738bd2a1
src/aiscc/evidence/service.py       fb1fa979903cf8a2adfa744203fb020567cc0544
src/aiscc/human/repository.py       0f98badc2ea52eb887a81e8623ff55a8e482252f
```

The next Executor must verify Python AST equivalence and normalized token/comment equivalence between each current
file and its expected HEAD bytes before restoring anything. The 1400 Executor did not run that gate because the
session blocker occurred first.

---

# 12. Accepted 36 runtime identity

The exact post-restore Commit A candidate is the following case-sensitive ordinal path/hash set:

```text
migrations/versions/20260831_0006_p1_8_project_memory_cycle_admission.py e0072031ffc8be030bfa265d329196b67aad6774df240904fa01d8fdccf8766c
migrations/versions/20260831_0007_p1_8_authority_contract_rework.py 544aef28e3f36d5cff322afa9401b96f45fb050d03c7d41ea7d673e597815e0e
migrations/versions/20260901_0008_p1_8_prerequisite_authority_reconciliation.py c270e10f7d0763e4f5fee1d298ad9d41abb83510a07864cd4d3919afe4362d27
src/aiscc/contracts/canonical_json.py 9e235fff10aea51a44f8b1c6830d8ce724476339239a2d6d245dcdc94094a442
src/aiscc/cycle/__init__.py f9631ca9338109cbcd7a2aa07340a001b742fe4af0b129ca136c1078c4b62fed
src/aiscc/cycle/models.py e5aaa9a84c5d0cf8231c86d2efd300e8b1fa011697642d7d6ee395f46f0e1cf4
src/aiscc/cycle/repository.py d0a11d869ba94383eb35bf98f546968da28e3d2c56f872ad9de77728b9dc357d
src/aiscc/judgment/authority.py 0013e4a2ae6f84aba7341d1e58657ce0973ce7a7d5841d8fb69f7403f15a3941
src/aiscc/memory/__init__.py 842060c4e15da581c17f573e1e4a465592f486947e34eeaaa3cd589d1525fe79
src/aiscc/memory/models.py ba8c0fe2cb2802298b445718f2ae2fa0681b8f2983dec5064d9141fe38b8d308
src/aiscc/memory/repository.py b93856e50e1c5d5a74f7d49e1839bb2a2766a37fe3318fb49c2a2ec065f62ac4
src/aiscc/next_action/__init__.py c1e8cadee709b6ba289fa9f92ed2eeaa04e51444e3a9ff85f2fc97138c42172d
src/aiscc/next_action/models.py 09d5c13d73f2bb1cd4ef05433f73f40eedcb670353dcfae9cdbf480420af1ea6
src/aiscc/next_action/repository.py 51a44c9d28a374aea1359e41752e5ff02fdb21f89844ae61e082707906e213f7
src/aiscc/persistence/models.py 60518bd1ab916a07118de0e2bd6a507565a0fc0dc48d8cc003cd521b3018ca48
src/aiscc/persistence/repository.py 74a497fd32eb42176afd19b2ba621da04364b847b0130f52966bcb3001159dd1
src/aiscc/task_authority/__init__.py eb5c7e78bb891002d4bcbb81bf35ac121b9cbf8f4e2bab0c64b1232422d141d6
src/aiscc/task_authority/authority.py 76fe0027ca2d652efd8a9fe204408d23751aa23175c369a5bc6ce389ba3af165
src/aiscc/task_authority/models.py 101ec23cbf5197ec62e8a9c4b58e5fefa2296eeae43d75053f318cf66e05abd0
src/aiscc/task_authority/ports.py 991ad83420947a35021d6acfcc4ef0bc150d5112582e69b740698374eb8b68e8
src/aiscc/task_authority/repository.py 5de5faf4a7d60c83b181588d691ce36006469095b3e16aa449881ad14143f745
src/aiscc/workflow/__init__.py 3c4cdb62a49cb53c61705e705b77cd9fee14702671690c128076c9c9f7cdc5a1
src/aiscc/workflow/guards.py 0ad7c75e22755ecd2132805e6c143b99489eea8d7807a505f3798736a0364ba2
src/aiscc/workflow/models.py f69e813dea6c35f65c8eb28cfe118b36091dd8cf5225241396e254f6ea0ff99c
src/aiscc/workflow/ports.py afb4b105a4bf55a8dcfc2abb7bc110b7b7262a50851ae3cda6734489ebbc863f
tests/integration/evidence/test_postgres_evidence_admission.py 9f56ced27bdcca3c010240f7d8736a21ff4fe94a97d5330571c584b1cba3f545
tests/integration/human/test_postgres_human_gate_judgment.py 142020f3a81221944e6eb0001160b83aa897662a324c9e89963e4226079a02b5
tests/integration/memory/test_postgres_project_memory_next_action.py 6881eaebbb8c25f34e1589e552b044d4072aebda3e2a06d40f942f2526254bd1
tests/integration/providers/test_execution_persistence.py 717a40b9323d0c42560ef34a8f39634777be0929d3eeaea5b447c9e4e4de1214
tests/integration/task_authority/test_postgres_external_task_authority.py 15dfa7e90807aa02c60cec13f03ca64d24cce56a23049c6043cc9aff554234a5
tests/integration/workflow/test_postgres_kernel.py 10be51d5d7b43b4dbd2df8a19900ac4c116990a42860ffe8a015170cff877240
tests/unit/contracts/test_canonical_json.py 33095e18666620a4b504c719ebdabfd302e8be2bbc9b6f10e0013453964de7d3
tests/unit/cycle/test_project_memory_cycle_domain.py 783aef1e86191a68481f818b333a47e8a1da17affe7d2791d3824fbd12e4031d
tests/unit/next_action/test_next_action_domain.py 1a1525c4509302b6f5aaa4ff19965cd4e1680b5e3543db571af38c7067261449
tests/unit/task_authority/test_external_task_authority_domain.py f1b83cd299ac8f6bef239f18aa6206da5034a04ae2d9a5693ff760c1325e0ffd
tests/unit/workflow/test_state_machine.py 7f0501684a30211ab43b7bb9bdae389934c3558a28da266c94254f0fdb867752
```

Serialization for the corrected aggregate is UTF-8 without BOM, one row each:

```text
<case-sensitive repository-relative path>\t<lowercase_sha256>\n
```

All 36 rows are sorted in ordinal case-sensitive path order, including the final newline. Required aggregate:

```text
path count: 36
SHA-256: a82d94c1d607bc379c12d0768ff54d0cd481467eb731e0884f63176bd1207f3c
```

The legacy provider-last value `a1d5e9d2...` is historical provenance only and must not replace the corrected
ordinal aggregate.

---

# 13. Future Commit A contract

The fifth Browser Command Center must not execute Git itself. It should issue a new timestamped rework Task that
reuses the Human decision only after binding the then-current repository identities.

Expected Commit A contract if all preconditions still match:

```text
expected parent: 1c9a3ef2893c10cd12a1b6ba287ef8e42349d37a
commit count: exactly one
merge parent count: zero
message: feat(runtime): complete P1-8 project memory and cycle admission
changed path count: exactly 36
changed paths: exact accepted-36 manifest above
six restore paths in Commit A diff: zero
governance/configuration paths in Commit A: zero
index after commit: empty
```

Required sequence:

```text
new IDE chat identity established by Human
→ exact branch/HEAD/index/governance/runtime preflight
→ exact six current hash/blob verification
→ AST and normalized token/comment equivalence
→ exact worktree-only restore from expected HEAD
→ six clean / index still empty / runtime dirty exact 36
→ git diff --check and repository-local Ruff/mypy
→ stage exact accepted 36 only
→ verify staged path/blob set
→ one Commit A
→ verify commit message/parent/tree/path/blob/merge-parent count
→ export exact 36 files from Commit A tree
→ stop for Browser Command Center review
```

The 1100 full test evidence (`231 passed` plus accepted targeted/database evidence) may be reused only if all exact
accepted bytes remain unchanged and six return to their expected clean HEAD bytes. A new database/container or
broad suite must not be created merely to fill a report field.

Do not configure Git author identity globally or invent credentials. If author identity is unavailable and commit
requires configuration mutation, stop before commit.

---

# 14. Exact governance inventory expected at the next start

The 1400 Task expected 11 Git-visible governance paths before its lifecycle. Since the Task moved to done, the next
start should expect exactly 12 if no other repository change has occurred:

```text
.aiassistant/tasks/done/20260901_2311_aiscc-p1-8-joint-design-terminal-git-object-reconciliation-audit-1.md
.aiassistant/tasks/done/20260901_2359_aiscc-p1-8-runtime-prerequisite-authority-and-jcs-safe-integer-reconciliation-rework-1.md
.aiassistant/tasks/done/20260902_0050_aiscc-p1-8-runtime-owner-boundary-canonical-path-audit-1.md
.aiassistant/tasks/done/20260902_0232_aiscc-p1-8-runtime-prerequisite-authority-expanded-path-implementation-rework-1.md
.aiassistant/tasks/done/20260902_1100_aiscc-p1-8-runtime-provider-regression-and-metadata-parity-rework-1.md
.aiassistant/tasks/done/20260902_1222_aiscc-p1-8-runtime-final-acceptance-terminal-persistence-1.md
.aiassistant/tasks/done/20260902_1300_aiscc-p1-8-terminal-dirty-baseline-provenance-reconciliation-audit-1.md
.aiassistant/tasks/done/20260902_1400_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-1.md
.aiassistant/records/aiscc/cycles/20260902_1100_aiscc-p1-8-runtime-expanded-path-implementation-hold-1.cycle.md
.aiassistant/records/aiscc/cycles/20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md
.aiassistant/records/aiscc/cycles/20260902_1300_aiscc-p1-8-terminal-persistence-precondition-blocked-1.cycle.md
.aiassistant/records/aiscc/cycles/20260902_1355_aiscc-p1-8-terminal-dirty-baseline-audit-acceptance-human-disposition-gate-1.cycle.md
```

The Human must later place the new 1621 Cycle at its exact cycles path. Once placed, the actual governance set will
grow. Therefore the fifth-session Task must not blindly require “exact 12” after transport. It must distinguish:

```text
repository state before new Cycle placement
vs
state after new Cycle placement
vs
state after new Task active/done lifecycle
```

Do not auto-expand an allowlist. If unexpected governance paths exist, stop and report their exact identities.

---

# 15. Fifth Browser Command Center opening sequence

The next Browser session should follow this order.

## Step 1 — Read and classify sources

Read:

1. this Handoff in full;
2. the attached Project Source as a possibly stale read-only mirror;
3. the 1621 judgment Cycle;
4. any newly submitted local-canonical audit result, if the Human supplies one.

Answer the bootstrap questions explicitly before issuing work:

- project purpose;
- current phase and current blocking state;
- accepted vs unaccepted layers;
- Human decisions already supplied;
- insufficient guidance, if any;
- questions that truly require the prior session rather than repository evidence.

## Step 2 — Do not reinterpret 1400 as reusable active authority

The 1400 Task is a completed blocked-result provenance artifact under tasks/done. Do not tell the Executor to rerun
it as if it were still active. Issue a new timestamped Task that names 1400 as a predecessor and carries a current
preflight.

## Step 3 — Reconcile current local canonical before destructive authority

The new Task must verify before mutation:

```text
branch and HEAD
empty index
exact runtime dirty set
exact governance set with transport/lifecycle distinctions
1222 Human acceptance Cycle identity
1300 blocker Cycle identity
1355 RESTORE_SIX decision Cycle identity
1621 blocked-result Cycle identity
1400 done Task identity
exact six current SHA-256/current blob/HEAD blob
exact accepted 36 hashes and corrected aggregate
```

If local canonical advanced after this Handoff, do not force it back to `1c9a3ef...`. Stop and issue a reconciliation
Task or adjust the new Task only from admitted exact evidence.

## Step 4 — Issue one new timestamped rework Task

The next Task's conceptual title is:

```text
P1-8 restore six and runtime Commit A persistence fresh-IDE-session retry
```

The fifth Browser session must choose the actual timestamp and exact Task filename. This fourth session deliberately
does not pre-issue that Task.

The new Task must preserve:

- `RESTORE_SIX_TO_EXACT_HEAD` exact-path scope;
- exact accepted 36 content/aggregate;
- exact one-Commit-A contract;
- no canonical update/Commit B/P1 closure/P2/mirror/push/release;
- mandatory stop on any identity, semantic-equivalence or scope mismatch;
- success end state `COMMIT_A_CREATED / COMMAND_CENTER_REVIEW_REQUIRED`.

## Step 5 — Human opens the new IDE Executor chat

After the next Task and required Cycle transport artifact are ready, instruct the Human to open a genuinely new IDE
Executor chat. State the ground:

```text
the preceding 1300 thread was read-only audit context;
the next Task grants destructive restore and Git commit authority;
1400 proved that continuing the prior IDE thread is invalid.
```

## Step 6 — Use the fixed Move short prompt

The short prompt must use exact Downloads filenames and exact repository destinations. It must require Move, not
Copy, and atomic all-or-nothing prechecks. It must not tell the Executor to open the new chat.

---

# 16. What happens after a successful future Commit A bundle

When a future Executor submits a Commit A result:

1. substantively verify bundle integrity and all exact source copies;
2. independently verify the reported commit hash, one parent, exact expected parent, exact message, exact 36 paths,
   exact committed bytes and absence of six/governance paths from the diff;
3. distinguish successful Executor execution from Command Center acceptance;
4. persist the judgment in a new Cycle;
5. under the new Browser-session rule, do not issue Commit B Task in that same Browser session;
6. issue a new detailed Handoff and migrate to the next Browser Command Center session;
7. only the subsequent Browser session may issue a narrow terminal governance/Commit B Task.

Future Commit B must remain governance-only and must bind the actual accepted Commit A. It may persist terminal
Cycle/canonical state/decision/next-action/handoff/task-done provenance under an exact allowlist. It must never use
`git add .` or `git add -A`, and must not absorb unrelated runtime/configuration/target-bundle paths.

After Commit B, any required Human gate and Project Source mirror replacement remain separate evidence/authority
steps. P1-8 and P1 close only after those terminal conditions are proven.

---

# 17. Human gates still relevant

Already provided:

```text
P1-8 runtime exact-36 acceptance
RESTORE_SIX_TO_EXACT_HEAD exact-path decision
```

Pending or future:

```text
Human opens the genuinely new IDE Executor chat
Command Center/Human review of the actual Commit A object as required by the future Task
later terminal governance/Commit B review
Project Source complete replacement confirmation if mirror sync becomes required
public release/deployment/competition submission Human actions
```

The next Executor must never report a pending Human action as completed merely because it created a checklist or
because a Task moved to done.

---

# 18. Exact artifacts to preserve across cleanup and migration

The following fourth-session terminal artifacts must survive:

```text
.aiassistant/tasks/done/
20260902_1400_aiscc-p1-8-restore-six-and-runtime-commit-a-persistence-1.md

.aiassistant/records/aiscc/cycles/
20260902_1222_aiscc-p1-8-runtime-human-final-acceptance-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260902_1300_aiscc-p1-8-terminal-persistence-precondition-blocked-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260902_1355_aiscc-p1-8-terminal-dirty-baseline-audit-acceptance-human-disposition-gate-1.cycle.md

.aiassistant/records/aiscc/cycles/
20260902_1621_aiscc-p1-8-runtime-commit-a-fresh-chat-precondition-blocked-1.cycle.md

.aiassistant/reports/aiscc/
20260902_1621_aiscc-browser-command-center-session-handoff-p1-8-runtime-commit-a-fresh-chat-resume-1.md
```

Relevant identities:

```text
1355 decision Cycle SHA-256:
a7ae3c92d3feba97e835a8962c6da0dd6cd66dea72732ae018cae056830e7116

1400 done Task SHA-256:
b19b51eed1935cf0144038eb7c6b68c9ec0b71eff82d01c7a0c083dd02d18c76

1621 blocked-result Cycle SHA-256:
0c3f2b98ed7deb96956cf2ef4e93e747870c94d20f4adf9b20fbc07228f80952
```

The 1400 target directory and submitted ZIP are ignored temporary review evidence once the Cycle/Handoff have been
consumed. Do not confuse them with canonical public provenance.

---

# 19. What not to do in the fifth session

Do not:

```text
issue a successor Task from the fourth session retroactively
rerun 1400 as an active Task
assume a new Browser chat is also a new IDE chat
ask the IDE Executor to open its own chat
perform restore/commit in Browser
restore any path outside exact six
use broad restore/reset/checkout/clean/stash
change accepted 36 bytes
stage governance with runtime Commit A
use git add . or git add -A
auto-expand governance allowlists
create more than one Commit A
amend/rebase/merge/cherry-pick/push/release/deploy
treat 1400 blocked-result acceptance as Task-goal acceptance
treat tasks/done as accepted
treat Human runtime acceptance as Git persistence
claim Commit A, Commit B, P1-8 CLOSED, P1 CLOSED or P2 STARTED without exact proof
trust the stale Project Source phase table over verified local canonical
start P2
release PUBLIC_BOUNDED_LIVE
```

---

# 20. Recommended opening prompt for the fifth Browser Command Center

The Human can open the next Browser Command Center with this conceptual prompt:

```text
이 문서를 먼저 전부 읽어라.

이 채팅은 AISCC의 5번째 Browser Command Center다.
이전 채팅 메모리나 File Library를 authority로 사용하지 말고,
GPT Project Source는 오래된 read-only mirror일 수 있다고 간주하라.

먼저 다음을 답하라.
1. 프로젝트 목적
2. 현재 P1-8 상태와 완료되지 않은 terminal persistence
3. 이미 제공된 Human decisions
4. 1400 bundle judgment와 fresh IDE chat blocker
5. 부족한 guidance가 있는지

그 다음 이 HANDOFF와 1621 Cycle에 따라 현재 local canonical identity를 bind하는
새 timestamp의 P1-8 restore-six / runtime Commit A retry Task를 발행하라.

1400 done Task를 active Task처럼 재사용하지 마라.
Human이 새 IDE Executor 채팅을 열며, 그 근거는 read-only 1300 audit에서
destructive restore/Commit A authority로 전환되기 때문이다.
```

The fifth session may refine the Task after reconciling newer exact evidence, but it must not weaken any authority,
scope, proof or Human boundary recorded here.

---

# 21. Handoff terminal statement

At the end of the fourth Browser Command Center session:

```text
P1-8 runtime exact 36: HUMAN_PROVIDED / ACCEPTED
six dirty-file disposition: HUMAN_PROVIDED / RESTORE_SIX_TO_EXACT_HEAD
1400 Executor behavior: accepted as an accurate mandatory-stop result
1400 Task goal: NOT_COMPLETED
six restored: No
Commit A: NOT_CREATED
Commit B: NOT_CREATED
P1-8 terminal closure: NOT_REACHED
P1 closure: NOT_REACHED
P2: NOT_STARTED
next Task from fourth session: NOT_ISSUED
next owner: fifth Browser Command Center
```

The next Browser Command Center must issue fresh execution authority; the Human must then open a genuinely new IDE
Executor chat. Until that happens, the correct stable state is:

```text
P1-8_RUNTIME_HUMAN_ACCEPTED
/ RESTORE_SIX_AUTHORIZED
/ COMMIT_A_PENDING
/ FRESH_IDE_SESSION_REQUIRED
```
