"""In-process ASGI transport; HTTPS/client metadata explicitly test-owned."""

import json

from aiscc.public_live.http import ORIGIN, ROOT

BODY = b'{"scenario_id":"stockroom-s1-normal","scenario_version":"1.0.0"}'


async def call(
    app,
    method="POST",
    path=ROOT,
    *,
    headers=None,
    body=BODY,
    chunks=None,
    client="8.8.8.8",
    scheme="https",
    query=b"",
):
    if headers is None:
        headers = [
            ("origin", ORIGIN),
            ("content-type", "application/json"),
            ("idempotency-key", "a" * 32),
        ]
    scope = {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": method,
        "scheme": scheme,
        "path": path,
        "raw_path": path.encode(),
        "query_string": query,
        "root_path": "",
        "server": ("127.0.0.1", 0),
        "client": (client, 12345),
        "headers": [(k.encode(), v.encode("latin-1")) for k, v in headers],
    }
    parts = list(chunks if chunks is not None else [body])
    messages, receives = [], 0

    async def receive():
        nonlocal receives
        receives += 1
        if not parts:
            return {"type": "http.disconnect"}
        return {"type": "http.request", "body": parts.pop(0), "more_body": bool(parts)}

    async def send(message):
        messages.append(message)

    await app(scope, receive, send)
    start = next(m for m in messages if m["type"] == "http.response.start")
    raw = b"".join(m.get("body", b"") for m in messages if m["type"] == "http.response.body")
    return {
        "status": start["status"],
        "headers": {k.decode(): v.decode() for k, v in start["headers"]},
        "json": json.loads(raw) if raw else None,
        "raw": raw,
        "receives": receives,
    }
