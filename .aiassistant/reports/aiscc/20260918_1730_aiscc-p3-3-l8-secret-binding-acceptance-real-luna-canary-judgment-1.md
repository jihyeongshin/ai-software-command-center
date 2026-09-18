# Browser Command Center Judgment

## decision

`ACCEPTED / L8_WORKER_SECRET_BINDING`

`ONE_CALL_REAL_LUNA_CANARY_AUTHORIZED_BY_ATTACHED_TASK`

## accepted evidence

- production key exists only on `aiscc-public-live-worker`;
- worker secret is sealed according to Human evidence;
- API/initializer/ingress do not hold `AISCC_OPENAI_API_KEY`;
- cleanup redeployment of `aiscc-public-live-api` succeeded;
- OpenAI key `Last used` remains `Never`;
- project monthly spend remains `$0.00`;
- no provider call has occurred yet.

## canary boundary

The next Task authorizes one and only one physical OpenAI Responses request.

It must use the existing trusted worker credential path.

Forbidden substitutes:
- direct curl;
- raw key copied into a command/script;
- local developer environment key use;
- a second request after timeout/unknown outcome;
- public admission/campaign activation merely to create the canary.

## release effect

Canary PASS does not itself release Public Live.

After the Executor canary evidence, Human must refresh the OpenAI key/project usage page and provide non-secret post-canary confirmation before Browser finalizes the provider gate.
