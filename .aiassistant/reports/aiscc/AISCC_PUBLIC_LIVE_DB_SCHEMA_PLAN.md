# Public Live additive schema plan

HUMAN_ACCEPTED / FROZEN design; no SQL migration is authored or executed. A1/I1/R1/M1 in AISCC_PUBLIC_LIVE_ADMISSION_SECURITY_DESIGN.md are normative. Current source uses SQLAlchemy models, append-only execution events, unique operation identities and PostgreSQL locking. Current migration head is `20260914_0012` (parent `20260914_0011`); this is a baseline fact, not a new revision assignment.

## Storage contract

Separate public Live DB and credentials. Owner DB is not shared and no owner/private data is copied. Existing owner semantic services may be composed against isolated synthetic public data through their production admission boundaries. Separate migration identity/schema for the new public tables must coexist with required execution schema. The future migration Task must inspect then-current head and explicitly authorize the additive revision and any strict-head fixture edits; no guessed fixture changes.

All timestamps TIMESTAMPTZ in UTC; all money BIGINT micro-USD, never floating point. IDs generated with OS CSPRNG; hash columns fixed 32-byte bytea with length checks. Foreign keys RESTRICT deletion by default. Policy and scenario pins immutable after campaign activation. Constraints below are enforced by keys/checks plus a privileged transaction API; runtime role gets EXECUTE on reviewed transaction functions, SELECT on safe projections, no direct DML. Migration role is separate. Cross-row invariants require this permissions boundary as well as A1 locking; CHECK alone is insufficient.

| Table | Columns and constraints | Indexes / mutation owner |
|---|---|---|
| public_control | singleton PK/check id=1; enabled false initially; policy_digest; last_clock; incident; active_campaign FK | Every writer locks row first. No alternate writer bypass. |
| public_campaign | campaign_id PK; start/end; limit=15000000; available/held/settled nonnegative and sum=limit; hmac_version; scenario_id/version/content_digest; policy_digest; end>start | Campaign lock; immutable settings after activation. |
| public_day | PK(campaign_id,utc_date); limit=4000000; balances as campaign; admitted_count in 0..20 | Day date derived by DB; balances persist across rollover. |
| public_client | PK(campaign_id,bucket_hash); key_version; created_at; retention_until | No raw IP; holds serialization identity, not browser identifier. |
| public_run | run_id PK 16 bytes; campaign/day/client FK; admitted_at; deadline=admitted_at+90s; state constrained; owner_binding nullable unique; version>=1; read_hash unique; read_expires=admitted_at+24h; policy/payload/scenario digests | Index(state,deadline); safe projection only. Owner binding written only after authentic composition. |
| public_idempotency | PK(campaign_id,key_hash); bucket FK; payload_hash; run_id UNIQUE FK; admitted_at; replay_until=admitted_at+600s; retention_until | Index(retention_until); key tombstone kept after response expiry. |
| public_rate_event | run_id PK FK; campaign/day/client FK; admitted_at | Index(campaign_id,bucket_hash,admitted_at), index(campaign_id,utc_date). Append-only; no decrement on run failure. |
| public_reservation | run_id PK FK; day/campaign FK; amount=200000; committed_max 0..200000; provisional>=0; settled_cost nullable 0..200000; state HELD/SETTLED/INCIDENT | One reserve and one terminal settlement per run; no silent cost clamping. Above-bound evidence separately retained and gate closed. |
| public_slot | slot_id PK/check IN(1,2); run_id UNIQUE nullable FK; generation>=1; state FREE/OCCUPIED/SUSPECT; heartbeat_at; expires_at | Two seeded rows only; FREE iff run_id null. No expired-row deletion. |
| public_outbox | run_id PK FK; state PENDING/BOUND/CLOSED; generation; owner_binding unique nullable | Index(state,run_id). Unique composition command identity maps admission to actual owner lineage. |
| public_dispatch | PK(run_id,ordinal), ordinal IN(1,2); generation; start_marker_at; max_cost; state STARTED/KNOWN_SUCCESS/KNOWN_FAILURE/UNKNOWN; usage evidence digest; provisional_cost | Check max_cost>0; sum checked under control/reservation locks before marker. No unmarked dispatch. |
| public_money_event | PK(run_id,event_kind); event_kind RESERVE/SETTLE; amount, cost, release; campaign/day FK; evidence_digest; created_at | Append-only. SETTLE requires cost+release=amount. Transaction updates both ledger projections and inserts event together. |
| public_observation | observation_id PK; run/dispatch FK; unique(source_identity); classification; evidence_digest; recorded_at | Append-only evidence, including late or above-bound usage; not permission to refund. |

Same control lock order applies to maintenance, reconciliation, counters and dispatch. Rows missing for a UTC day/client are created only while control lock is held; unique constraints still defend duplicates. Deadlock/serialization retry reuses request identity and has no external effects. DB clock regression disables new admission; replay lookup and safe reads can remain available. Reads use consistent committed projections and do not mutate admission counters.

## Lease and journal enforcement

Slot occupancy, run, reservation, rate event, idempotency and outbox creation are one commit. Functions check row counts and postconditions; exception rolls everything back. No function returns a dispatch authorization before its marker transaction commits. Dispatcher checks generation before marker; fencing cannot cancel an already granted external send, so stale generation alone never frees a slot. Settlement validates actual closure evidence and that no unspent dispatch authorization can execute, then atomically closes outbox, records settlement, updates both budgets and frees slot. Unknown send prevents automatic slot release.

## Migration and rollback sequence

1. Freeze exact schema and permission tests in a separately authorized implementation Task; verify current head and owner compatibility.
2. Add tables, indexes, constraints and transaction functions without altering historical owner rows. Seed disabled control and two FREE slots. Install separate least-privilege DB roles. No enabled campaign or secret values in migration.
3. Verify conservation, permission denial, duplicate races and rollback on a disposable authorized test DB. Existing execution ownership integration must be tested separately.
4. Deploy code with admission disabled; release verification and Human decision precede explicit activation. These actions are future Tasks, not part of this design.
5. Rollback disables new admission first, drains/proves termination, reconciles all reservations, and retains journals/tombstones. Downgrades that drop unresolved rows are forbidden. Prefer forward correction; preserve owner DB compatibility and Replay independence.

Cleanup never deletes unresolved runs, slots, money evidence or their key bindings. Resolved bucket/key/rate data may be purged only after campaign end+30 days and retained aggregate ledger/audit requirements are met; do not reopen the campaign. Read capability expires independently after 24h. Safe status projection can be removed at retention expiry with uniform 404. Retention is Human-accepted under H4, not an existing configured guarantee.
