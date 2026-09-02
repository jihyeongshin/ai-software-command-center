# 작업지시서: Terminal canonical Project Source mirror refresh preflight audit

## meta

- task_id: `20260903_0107_aiscc-terminal-project-source-mirror-refresh-preflight-audit-1`
- created_at: `2026-09-03T01:07:00+09:00`
- project: `AI Software Command Center (AISCC)`
- phase: `P1 terminal maintenance / P2 entry pre-step`
- work_type: `READ_ONLY_AUDIT / PROJECT_SOURCE_MIRROR_REFRESH_PREFLIGHT`
- evidence_profile: `GOVERNANCE_HIGH`
- execution_mode: `MANUAL_COMMAND_CENTER`
- predecessor_terminal_commit: `b9ed57feb595b3a670b644a213c184f958956924`
- predecessor_terminal_tree: `7886c8592669dc9d26bb339f2248d3a1c6bc03aa`
- predecessor_judgment_cycle: `.aiassistant/records/aiscc/cycles/20260903_0105_aiscc-p1-terminal-closure-persistence-substantive-acceptance-1.cycle.md`
- target_bundle: `.aiassistant/reports/target/20260903_0107_aiscc-terminal-project-source-mirror-refresh-preflight-audit-1/`
- fresh_chat_policy: `NO_NEW_CHAT_REQUIRED / READ_ONLY_AUDIT`
- success_boundary: `PROJECT_SOURCE_MIRROR_REFRESH_PREFLIGHT_AUDITED / COMMAND_CENTER_REVIEW_REQUIRED / NO_MIRROR_MUTATION`

## 0. authority and current state

Accepted terminal canonical:

```text
HEAD:
b9ed57feb595b3a670b644a213c184f958956924

P1-8:
HUMAN_PROVIDED / ACCEPTED / CLOSED

P1:
ACCEPTED / CLOSED

P2:
NOT_STARTED / ENTRY_READY

next executable roadmap item:
P2-1 Command Center Web UI
```

Browser Project Source is a read-only mirror and is currently stale relative to this terminal canonical.

This Task is **preflight only**. It does not update a manifest, generate a replacement bundle, or modify Browser
Project Source.

## 1. exact goal

1. transport the exact current Task and exact 0105 terminal-acceptance Cycle;
2. verify local repository remains exactly on the accepted terminal commit and is clean;
3. identify the exact currently active AISCC Project Source manifest through tracked canonical metadata;
4. inspect the tracked Project Source registry, mirror rule, active manifest, and generator;
5. enumerate the current active Browser Project Source mapping and its canonical source paths/hashes;
6. compare that mapping to terminal canonical and identify stale/changed/missing/obsolete active entries;
7. determine the exact tracked files that a subsequent mirror-refresh Task must modify;
8. determine the exact ignored generated bundle path/count and complete-replacement Human procedure;
9. export read-only evidence and an exact proposed refresh contract;
10. move this Task active→matching done and stop.

## 2. non-goals / forbidden

Do not:

- modify any canonical/runtime/rule/manifest/registry/generator file;
- generate or overwrite `.aiassistant/project-sources/bundles/**`;
- stage or commit;
- delete stale browser-source files;
- upload/replace Browser Project Source;
- start P2-1 implementation;
- push/fetch/pull/network/deploy.

Forbidden:

```text
git add
git commit
git restore
git checkout
git reset
git clean
git stash
```

The only repository file move authorized is current Task active→matching done after audit/export.

## 3. Downloads transport

Exactly two Downloads sources:

```text
C:\Users\oracl\Downloads\20260903_0107_aiscc-terminal-project-source-mirror-refresh-preflight-audit-1.md
C:\Users\oracl\Downloads\20260903_0105_aiscc-p1-terminal-closure-persistence-substantive-acceptance-1.cycle.md
```

Destinations:

```text
.aiassistant/tasks/active/20260903_0107_aiscc-terminal-project-source-mirror-refresh-preflight-audit-1.md
.aiassistant/records/aiscc/cycles/20260903_0105_aiscc-p1-terminal-closure-persistence-substantive-acceptance-1.cycle.md
```

0105 Cycle expected SHA-256:

```text
98654572216d2bacd4abd607ee81d652d987105984b436a5bee1550e072124c9
```

Before moving either, atomically verify:

1. both exact sources exist;
2. both exact destinations do not exist;
3. Cycle SHA-256 exact match.

Failure:

```text
move neither
do not search alternate Downloads path
do not overwrite/delete
STOP: TRANSPORT_PRECONDITION_FAILED
```

All PASS:

- Move exactly both files, not Copy;
- verify destination identity and Downloads-source absence.

## 4. repository preflight

Read-only verify:

```text
repository == ai-software-command-center
branch == main
HEAD == b9ed57feb595b3a670b644a213c184f958956924
HEAD tree == 7886c8592669dc9d26bb339f2248d3a1c6bc03aa
HEAD parent == c9004e89ae9ed961d7cabe6e3eca1100ef4a13cc
index change count == 0
runtime/source/test/migration dirt == 0
```

Before current Cycle transport, accepted terminal worktree was clean.

After current Cycle transport and while active Task is ignored, expected Git-visible dirt is only:

```text
.aiassistant/records/aiscc/cycles/20260903_0105_aiscc-p1-terminal-closure-persistence-substantive-acceptance-1.cycle.md
```

If additional drift exists, do not repair it. Record exact paths and return
`READ_ONLY_RECONCILIATION_REQUIRED`.

## 5. minimum authoritative context

Read exact:

```text
.aiassistant/rules/AISCC_PROJECT_SOURCE_MIRROR.md
.aiassistant/rules/AISCC_AGENTS.md
.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md
.aiassistant/project-sources/PROJECT_SOURCE_BUNDLE_REGISTRY.md
.aiassistant/records/aiscc/CURRENT_STATE_SUMMARY.md
.aiassistant/records/aiscc/DECISION_REGISTER.md
.aiassistant/records/aiscc/NEXT_ACTIONS.md
.aiassistant/reports/aiscc/20260902_2331_aiscc-p1-completion-p2-entry-handoff-1.md
.aiassistant/records/aiscc/cycles/20260903_0105_aiscc-p1-terminal-closure-persistence-substantive-acceptance-1.cycle.md
.aiassistant/tasks/active/20260903_0107_aiscc-terminal-project-source-mirror-refresh-preflight-audit-1.md
```

Read-only directory enumeration is explicitly authorized for:

```text
.aiassistant/project-sources/manifests/
scripts/
```

Only open files relevant to AISCC Project Source registry/manifest/generation. Do not bulk-read unrelated scripts.

If registry names the generator at another exact tracked path, read that exact file.

## 6. active manifest resolution

Use the tracked registry as the first selector.

Report:

- exact registry SHA-256/blob;
- exact active AISCC manifest path;
- manifest SHA-256/blob;
- manifest bundle ID/version;
- target GPT project;
- project scope;
- manifest canonical commit;
- generated-by task;
- expected active file count;
- upload limit/reserved slots if present;
- source-mirror sync status.

If registry has zero or multiple simultaneously active AISCC manifests, do not choose silently. Report
`PROJECT_SOURCE_ACTIVE_MANIFEST_AMBIGUOUS`.

## 7. current active-set inventory

From the resolved active manifest, enumerate every mapping row with:

```text
project_source_filename
canonical_path
group
upload_status
role
manifest canonical_sha256
current terminal-canonical SHA-256
status
```

Status must be one of:

```text
UNCHANGED
STALE_CONTENT
CANONICAL_PATH_MISSING
MANIFEST_HASH_MISSING
INVALID_MAPPING
```

Also identify duplicate Project Source filenames or duplicate active slots.

Do not mutate the manifest.

## 8. terminal-canonical coverage analysis

Evaluate whether the active set currently includes the minimum Command Center bootstrap material required after P1
closure:

- project source index/metadata;
- core rules;
- Command Center workflow/templates/rubrics;
- `CURRENT_STATE_SUMMARY.md`;
- `DECISION_REGISTER.md`;
- `NEXT_ACTIONS.md`;
- current product/architecture/orchestration/security baselines;
- terminal P1→P2 phase handoff if the active-set policy/registry design admits a current handoff.

Do not automatically add all Task/Cycle files. Mirror policy excludes bulk `tasks/done` and Cycle history from the
default active set.

For each recommended addition/removal, provide the exact policy basis.

## 9. generator preflight

Identify the exact tracked generator used by the active registry/manifest.

Read-only report:

- generator path;
- SHA-256/blob;
- expected invocation;
- required manifest argument/path;
- output bundle directory convention;
- whether output is ignored by Git;
- validations implemented:
  - source existence;
  - count;
  - duplicate filenames;
  - canonical SHA;
  - body SHA;
  - optional-file exclusion;
  - UTF-8/control-character checks;
  - secret/private-path exclusion.

Do not execute the generator in this Task.

If current generator cannot represent the terminal active set without code modification, report exact gap; do not
edit it.

## 10. exact next-refresh mutation proposal

Produce an exact proposal for the subsequent mutation/generation Task.

Separate:

```text
TRACKED_FILES_TO_MODIFY
TRACKED_FILES_TO_ADD
TRACKED_FILES_UNCHANGED
IGNORED_BUNDLE_OUTPUT
HUMAN_BROWSER_SOURCE_ACTION
```

For every proposed tracked mutation, include exact repository-relative path and why it must change.

The proposal must specify:

- future manifest canonical commit basis;
- expected active count;
- exact active mapping filenames;
- exact canonical source paths;
- expected canonical SHA-256 for each mapping;
- whether registry metadata must change;
- whether mirror rule metadata itself must change;
- exact ignored output directory;
- expected generated filenames;
- complete-replacement Human steps;
- files in current Browser Project Source that must be removed;
- files that must be uploaded;
- post-upload confirmation fields required by mirror policy.

Do not claim the proposal is authorized for mutation.

## 11. relationship to P2

Report explicitly:

```text
P1:
ACCEPTED / CLOSED

P2:
NOT_STARTED / ENTRY_READY

roadmap next executable:
P2-1 Command Center Web UI

operational pre-step:
Project Source mirror refresh
```

This audit does not start P2.

## 12. required export

Target:

```text
.aiassistant/reports/target/20260903_0107_aiscc-terminal-project-source-mirror-refresh-preflight-audit-1/
```

Required root Markdown:

```text
TASK.md
EXECUTOR_REPORT.md
MIRROR_CURRENT_STATE.md
ACTIVE_SET_RECONCILIATION.md
NEXT_REFRESH_CONTRACT.md
EXPORT_MANIFEST.md
```

Export byte-exact copies preserving repository-relative paths of:

- Project Source registry;
- resolved active manifest;
- mirror rule;
- exact generator;
- current terminal canonical three;
- P1→P2 phase handoff;
- 0105 terminal-acceptance Cycle;
- current Task after matching done lifecycle.

Do not export generated mirror bundles in this preflight.

Manifest binds every payload except itself with byte count and SHA-256.

## 13. current Task lifecycle

After audit/report/export is complete:

```text
.aiassistant/tasks/active/20260903_0107_aiscc-terminal-project-source-mirror-refresh-preflight-audit-1.md
→
.aiassistant/tasks/done/20260903_0107_aiscc-terminal-project-source-mirror-refresh-preflight-audit-1.md
```

Move, not Copy. Matching done destination must be absent.

Do not stage or commit.

After lifecycle, expected normal no-drift Git-visible provenance is:

```text
0105 Cycle
+ current 0107 Task done
```

exactly two paths.

## 14. success / stop

Success:

```text
PROJECT_SOURCE_MIRROR_REFRESH_PREFLIGHT_AUDITED
/ COMMAND_CENTER_REVIEW_REQUIRED
/ NO_MIRROR_MUTATION
```

Do not declare:

```text
SOURCE_MIRROR_SYNCED
P2_STARTED
P2-1_STARTED
```

Mandatory stop only when transport/authority/manifest resolution prevents trustworthy read-only analysis.

If repository state differs, never force it back; report exact reconciliation evidence.

## 15. preserved artifacts

Preserve:

- terminal closure commit `b9ed57feb595b3a670b644a213c184f958956924`;
- `.aiassistant/records/aiscc/cycles/20260903_0105_aiscc-p1-terminal-closure-persistence-substantive-acceptance-1.cycle.md`;
- `.aiassistant/tasks/done/20260903_0107_aiscc-terminal-project-source-mirror-refresh-preflight-audit-1.md`;
- accepted P1→P2 phase handoff;
- all tracked Project Source registry/manifest/rule/generator files.

Target bundle is temporary until Browser substantive review.
