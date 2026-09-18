# Public End-to-End Smoke

## Bounded attempt

- POST count: exactly 1
- scenario: `stockroom-s1-normal / 1.0.0`
- public API path: `/v1/public-live/runs`
- browser Origin contract: `https://aiscc-replay.pages.dev`
- response: HTTP 201, state `ADMITTED`
- sanitized run fingerprint: `d81e5324d7ee1b64`
- read capability: held only in process memory and never exported
- GET polling: the same run only; no replacement run and no admission retry

## Outcome

The projection remained `ADMITTED` through 33 bounded reads and beyond its 90-second deadline. The smoke was classified as a material failure and polling stopped.

Durable lineage after failure:

1. start request reached `BOUND`, phase version 6;
2. work run and execution attempt reached `RUNNING`;
3. worker acquired one `EXECUTE` claim;
4. claim was not renewed or operation-bound;
5. after its 15-second lease expired it was released as `LIVE_UNAVAILABLE`;
6. canonical execution operation, dispatch, and provider request counts remained 0.

Provider/send outcome was conclusively `DEFINITELY_NOT_SENT`; UNKNOWN was not recorded and no retry was made.
