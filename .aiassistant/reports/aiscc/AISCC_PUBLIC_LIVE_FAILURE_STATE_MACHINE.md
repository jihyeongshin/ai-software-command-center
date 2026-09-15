# Public Live failure state machine

HUMAN_ACCEPTED / FROZEN design only. These are public admission/execution projections, not new canonical WorkRun states. Existing orchestration and provider authority continue to own WorkRun, evidence and Judgment. A1/I1/R1/M1 remain normative.

| State / trigger | Durable effects and next action | Public truth |
|---|---|---|
| REJECTED before commit | No run, reserve, rate event, slot or outbox. Safe rejection audit only outside paid authority. | Denied, not started. |
| ADMITTED | A1 committed all identities, rate count, reservation, slot and outbox. | Waiting, not provider executed. |
| ADMITTED, worker crash before marker | Reconcile unique outbox/owner binding. Same run may resume before deadline only after proving no prior send authorization. | Waiting/recovering. |
| ADMITTED, deadline or composition failure | Fence and prove no worker can obtain/send a marker; close owner execution truthfully, settle zero, release reserve and slot atomically. Rates remain consumed. | FAILED_NOT_DISPATCHED. |
| DISPATCH_STARTED | Unique ordinal marker and conservative maximum committed before send; reservation and slot held. | Running; result not yet known. |
| Marker committed, crash before/after network write | Mark UNKNOWN_OUTCOME; never resend ordinal; reject automatic retry. Preserve maximum charge and quarantine slot until closure proof. | Unknown; never claim provider did not run. |
| Known explicit provider failure | Retain evidence/usage. At most ordinal 2 may dispatch if policy permits, first call conclusively ended, within admitted deadline and two-call reservation. Otherwise settle after closure proof. | Running retry or FAILED_PROVIDER, not ACCEPTED. |
| Known provider success | Admit actual execution output through evidence/Judgment owners. No manufactured WorkRun/Evidence. May need second allowed call only under same caps. | GOVERNANCE_PENDING until actual authority resolves. |
| Governance concludes | Store bounded projection of admitted result. Close execution and settle before freeing slot. | COMPLETED with actual workflow_state; may be non-ACCEPTED. |
| Missing usage | Charge conservative authorized maximum for each possibly paid call; preserve missing-usage flag/evidence. | Outcome and usage certainty remain distinct. |
| Cost above authorized bound | Retain actual evidence, disable admissions, mark INCIDENT and require reconciliation. Do not falsify balances/usage. | FAILED_SAFETY; no positive safety claim. |
| DB unavailable before commit | No dispatch authorization. If commit uncertain, client resolves same key later. | Unavailable; admission outcome may be unknown. |
| DB fails after send | Worker records no unsupported terminal claim. Recover marked ordinal; no blind retry. | Last committed state then UNKNOWN_OUTCOME. |
| Lease expires / replica restarts | Mark slot SUSPECT; expiration or fencing alone cannot stop an already permitted network send. No third slot allocation. | Recovering/unknown, not cancelled. |
| Deadline 90s expires | Stop new sends, request supervisor termination of local execution; no public cancel route. Remote effect may outlive request timeout. | FAILED_TIMEOUT if closure proven; otherwise UNKNOWN_OUTCOME. |
| Late result after conservative settlement | Append immutable observation linked to original ordinal. No second settlement, automatic refund or run resurrection. Semantic correction requires actual owner evidence; preserve prior uncertainty. | Corrected evidence annotation only. |

Public state enum: ADMITTED, DISPATCH_STARTED, GOVERNANCE_PENDING, UNKNOWN_OUTCOME, COMPLETED, FAILED_NOT_DISPATCHED, FAILED_PROVIDER, FAILED_TIMEOUT, FAILED_SAFETY. Reject is an HTTP decision, not persisted run state. Recovery does not invent another WorkRun or reset provider ordinal. Current provider execution recovery contracts are input patterns, not proof of the future public adapter.

## Closure and safety order

1. Disable further outbox/dispatch authorization for the run under control lock; increment generation where needed.
2. Obtain reliable worker termination plus evidence that every authorized send either never escaped or is conclusively finished. A disconnected socket or elapsed wall clock alone is insufficient.
3. Determine cost conservatively: sum actual bounded usage when trustworthy, otherwise full committed maxima. Reserve remains held until closure proof. Unknown usage after proven execution closure can be conservatively settled; unknown execution closure cannot. This first slice deliberately has no early financial settlement of quarantined execution.
4. Under one control-locked transaction, require closure proof, insert unique SETTLE journal (or recognize identical prior settlement), update day/campaign balances, close outbox and free slot. Without closure proof keep the reservation held and slot quarantined.
5. HTTP observers read committed projections only. No in-memory callback declares ACCEPTED or releases resources.

No automatic lease stealing for a possibly live dispatcher. If provider lifecycle evidence cannot bound or conclusively terminate unknown calls, Live can exhaust both slots and remain disabled pending reconciliation. This design chooses safety over automatic availability. Release packaging must prove supervisor and dispatch fencing behavior; no Railway capability is assumed.

Provider calls <=2 includes retry. A late response never creates a third call. Per-run reservation is never released to another run before its possible spend has been conservatively charged. Daily liabilities remain in original admission day; campaign never resets across UTC day/month changes. Failure of Live, its DB, provider or supervisor does not touch static Replay deployment/corpus. Replay availability is displayed separately, never substituted as successful execution evidence.
