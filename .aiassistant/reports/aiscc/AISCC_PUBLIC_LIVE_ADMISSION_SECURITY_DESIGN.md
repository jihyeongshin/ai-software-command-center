# Public Live admission security design

Status: HUMAN_ACCEPTED / FROZEN under the 1646 Human decision. No implementation or release authority.

## Scope and grounding

Only `stockroom-s1-normal / 1.0.0`. No free-form input, repository URL/upload, public cancel, tool selection or model selection. Replay remains independent and Live disabled until all release prerequisites pass.

Current `src/aiscc/security/limits.py` has in-memory IdempotencyLedger, BudgetLedger and SlidingWindowThrottle. These are not multi-replica admission authority. `src/aiscc/persistence/repository.py` uses transaction-scoped advisory and row locks for execution bounds; reuse that discipline, not its per-run counters as public campaign money. `src/aiscc/api/app.py` mounts owner Command Center routes and cannot be exposed as the public composition. Exact current hashes are in the 1630 SOURCE_INVENTORY.json (historical candidate export). Contracts below are Human-accepted design, not descriptions of existing enforcement.

## Atomic admission A1

Use a separate public Live PostgreSQL database and credentials. All writers use one controlled repository transaction API; database permissions deny arbitrary application table writes. READ COMMITTED plus a singleton control row FOR UPDATE serializes admission, dispatch markers, heartbeat, settlement and recovery. The low cap makes this intentional serialization acceptable.

1. Before DB: bound body to 1024 bytes, reject duplicate JSON keys and unknown fields, validate exact scenario/version and headers; validate trusted socket/proxy identity and derive bucket. Generate random run/read candidates using OS CSPRNG; no effects yet.
2. Begin transaction, lock control row. Read DB clock after lock and load immutable policy/campaign identity. Lock order everywhere: control, existing idempotency, campaign, day rows sorted by date, client, slots ascending, runs ascending, dispatch ordinals ascending. Never nest owner WorkRun locks inside this boundary.
3. Resolve existing campaign/key identity first using its original pinned payload policy. Same bucket/payload within replay window returns existing receipt with no new counters/reserve/dispatch; conflict/expired denies. Replays are allowed after campaign admission closes or the new-admission gate is disabled. Use max(DB clock, control.last_clock) for replay expiry so clock regression cannot reopen a window. New admission requires enabled policy, non-regressing DB time and time inside campaign; update last_clock in the transaction.
4. Lock/create UTC day and client rows. Count admitted events in `(now-1 hour, now]` for client: fewer than 3; UTC day client fewer than 10; global day fewer than 20. Failed requests do not consume start counts; admitted runs never refund rate counts.
5. Lock both fixed slots. Require one FREE slot. Require day and campaign available balances each at least 200000 micro-USD.
6. In this same transaction create run and hashed read capability, campaign/key binding, immutable policy/payload fingerprints, rate event and day count, reservation and journal entry, occupy slot, and create unique dispatch outbox item. Transfer 200000 from available to held in BOTH ledgers. Persist all timestamps/deadline and owner-binding intent.
7. Commit. Only after confirmed commit return 201 and allow outbox consumption. A lost commit acknowledgement is resolved with the same idempotency key, never by creating a replacement run. Rollback means zero admission effects.

No provider send, worker start, owner mutation or network call occurs inside or before the successful admission commit. A worker must additionally pass current execution/security authority and commit a unique dispatch-start marker before each paid send. Admission is necessary, never sufficient to bypass runtime security or governance. Public run identity is not a WorkRun; outbox composition must bind one actual owner-admitted execution in the isolated public DB without fabricating owner rows.

## Idempotency I1

Idempotency-Key is exactly 32 lowercase hex characters, browser-generated 128 random bits. Hash decoded key bytes with SHA-256; unique `(campaign_id,key_hash)` globally, not per IP. Bind first admission to server-derived bucket. Never log the key. Payload digest is SHA-256 of UTF-8 canonical JSON (sorted keys, no whitespace) containing schema version 1, exact scenario/version, immutable scenario content digest and server policy digest. Client cannot supply those internal digests.

Same key/bucket/payload with DB time less than admitted_at+600s returns 202 receipt containing run_id only; no read token regeneration. Different bucket returns generic 403 without revealing the run; same bucket/different payload returns 409. At 600s or later return 410. Tombstones remain through campaign end plus 30 days and longer for any unresolved liability. Closed campaign never accepts keys again even after cleanup. Rejected uncommitted requests do not create tombstones. Transaction retry repeats identity without side effects.

Each provider ordinal (1 or 2) has exactly one durable STARTED marker; commit it before send. Crash after marker and before send is deliberately indistinguishable from a possible send. Never automatically resend that ordinal. Unknown outcome is not a retry opportunity. Only an explicit known completed failure may permit ordinal 2, subject to deadline, budget and execution policy. External exactly-once execution is not claimed.

## Trusted identity R1

Railway edge behavior is NOT proven by repository source. Required release contract: direct socket peer belongs to an explicitly verified edge CIDR set; edge strips incoming forwarding headers and overwrites a single `X-Forwarded-For` with exactly one bare client IP. No comma chain, port, zone ID, Forwarded, X-Real-IP or CF-Connecting-IP is accepted. Conflicting/additional identity headers deny. Disable framework proxy rewriting so original socket peer remains available. No guessed hop count or trust-all CIDR. If Railway cannot prove this contract, Live stays disabled pending a separately accepted ingress design.

Parse IP strictly; normalize IPv4-mapped IPv6 to IPv4; reject unspecified, loopback, private, link-local and multicast external client addresses. Bucket IPv4 /32 and IPv6 /64, canonical packed network bytes. Store HMAC-SHA256 with server secret and domain separator plus campaign ID, family and prefix; never browser client ID. Pin key version for campaign; emergency rotation pauses admission until counters can be preserved, never resets limits. No raw IP or forwarding header in logs/storage. Retain buckets and rate records through campaign+30 days, longer while unresolved; destroy HMAC key only after liability reconciliation and retention expiry. NAT users share limits; IPv6 prefix rotation and distributed IPs can evade per-client caps, so global caps remain essential. An edge request-flood limit is a release prerequisite, not supplied by these start counters.

Browser requests to Railway originate from the user's connection, not from the static Cloudflare Pages server. Origin is not client IP proof. This topology assumption must be demonstrated at release; do not trust a Cloudflare header merely because the frontend is hosted there.

## Money and concurrency M1

Integer signed BIGINT micro-USD only: run reserve 200000, UTC admission-day budget 4000000, campaign 15000000. Each ledger maintains `available + held + settled = limit`, all nonnegative. Reserve affects both ledgers atomically; journal identities prevent double release/settlement. Counts and liabilities stay charged to admission UTC day even if execution crosses midnight; daily budget means admission-cohort liability budget, not provider invoice posting date. Campaign begins only after authorized enablement and ends at 2026-10-18T00:00:00+09:00 exclusive = 2026-10-17T15:00:00Z (Human-accepted H3); spans months with no reset. Monthly provider cap is defense-in-depth only.

Dispatch authorization must prove a conservative per-call monetary maximum from a separately approved price/token envelope. Candidate 1552 arithmetic is 68000 micro-USD/call and 136000 for two calls; it is not current verified pricing. Reject dispatch if approved bounds are absent/stale or total committed maximum exceeds reservation. Retry counts within two total calls. Unknown/missing usage consumes the full authorized per-call maximum conservatively. Known trustworthy usage uses integer upward rounding. Above-bound usage disables admission as an incident; never hide it by clamping actual evidence.

Terminal settlement transfers held reservation R to settled C and releases R-C in both ledgers exactly once. For ambiguous sends use the conservative committed maximum; uncommitted capacity is releasable only after proving no worker can dispatch it. Late lower usage is annotated, not automatically refunded. Provisional usage cannot release money. No budget release solely because HTTP disconnected or a lease expired.

Two fixed durable slots (1,2), at most one run per slot and one slot per run. Heartbeat every 5s; 15s expiry marks SUSPECT, never FREE. Absolute run deadline admitted_at+90s prohibits new dispatch; it does not prove a remote call stopped. Generation fencing guards DB writes. Recovery may reclaim only after durable no-send proof and worker termination, or positive evidence that every possible send ended. A paused worker that may send later keeps the slot quarantined. Unknown provider termination may quarantine indefinitely: retain Replay and deny capacity rather than exceed two concurrent effects. Release slot after execution closure proof and atomic settlement; budget reconciliation alone is insufficient. A supervisor/process/egress termination proof is a release prerequisite.
