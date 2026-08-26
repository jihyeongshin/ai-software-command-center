# AISCC IDE Executor Bootstrap

transport_contract_id: `AISCC-AGENT-BOOTSTRAP-V1`

This file is a tracked thin transport bootstrap. It is not AISCC policy authority.

Before analysis, broad source inspection, or file changes:

1. Read `.aiassistant/rules/AISCC_AGENTS.md`.
2. Read `.aiassistant/rules/IDE_EXECUTOR_REPORT_EXPORT.md`.
3. Read `.aiassistant/rules/IDE_EXECUTOR_ASSET_GIT_AND_ENCODING_POLICY.md`.
4. Read the active Task File before broad source inspection when its path is provided.
5. Explicitly read every exact canonical path listed by that Task.
6. Treat the Task list as the minimum authoritative context set, not permission to bulk-read unrelated files.
7. Distinguish automatically discovered instructions from explicitly read sources.
8. Stop and report any conflict among instructions, the active Task, canonical rules, current source, and accepted evidence.
9. Never claim human-owned evidence as executor-completed.
10. Do not alter the Git index, commit, push, deploy, or perform credentialed external actions unless the active Task explicitly authorizes the exact action.

Canonical rule bodies remain under `.aiassistant/rules/`.
