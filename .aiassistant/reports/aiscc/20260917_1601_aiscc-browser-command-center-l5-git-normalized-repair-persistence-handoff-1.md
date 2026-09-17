# AISCC Handoff — Clean-filter stop → normalized Git repair persistence

The current index already contains the correct canonical Git representation.

Do not unstage/restage the existing 18 paths unless the exact index verification fails.

Accepted relationship:

```text
raw worktree candidate
→ Git clean filter
→ CRLF_TO_LF only
→ canonical committed blob
```

Add only this retry's 3 Browser governance files plus current Task done.

Expected final staged count: 22.

No tests, source edits, Railway, Cloudflare, or OpenAI.
