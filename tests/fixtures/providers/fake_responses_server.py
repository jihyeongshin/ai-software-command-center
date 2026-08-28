from __future__ import annotations

import json
import threading
from collections import deque
from collections.abc import Callable
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from types import TracebackType
from typing import Any


def response_body(status: str, output: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "id": f"resp_fake_{status}",
        "object": "response",
        "created_at": 1,
        "status": status,
        "error": {"code": "fake_failure", "message": "sanitized"} if status == "failed" else None,
        "incomplete_details": {"reason": "max_output_tokens"} if status == "incomplete" else None,
        "instructions": None,
        "max_output_tokens": 256,
        "model": "fake-responses-model-v1",
        "output": output or [],
        "parallel_tool_calls": False,
        "previous_response_id": None,
        "reasoning": {"effort": None, "summary": None},
        "store": False,
        "temperature": 1.0,
        "text": {"format": {"type": "text"}},
        "tool_choice": "auto",
        "tools": [],
        "top_p": 1.0,
        "truncation": "disabled",
        "usage": {
            "input_tokens": 1,
            "input_tokens_details": {"cached_tokens": 0},
            "output_tokens": 1,
            "output_tokens_details": {"reasoning_tokens": 0},
            "total_tokens": 2,
        },
    }


def final_message(text: str = "AISCC_FAKE_FINAL") -> dict[str, Any]:
    return {
        "id": "msg_fake_1",
        "type": "message",
        "status": "completed",
        "role": "assistant",
        "content": [{"type": "output_text", "text": text, "annotations": []}],
    }


class _Server(ThreadingHTTPServer):
    responses: deque[dict[str, Any]]
    requests: list[dict[str, Any]]
    before_response_callbacks: deque[Callable[[], None] | None]


class _Handler(BaseHTTPRequestHandler):
    server: _Server

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/v1/responses":
            self.send_error(404)
            return
        length = int(self.headers.get("content-length", "0"))
        body = json.loads(self.rfile.read(length))
        self.server.requests.append(body)
        callback = self.server.before_response_callbacks.popleft()
        if callback is not None:
            callback()
        response = self.server.responses.popleft()
        payload = json.dumps(response, separators=(",", ":")).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        del format, args


class FakeResponsesServer:
    def __init__(self) -> None:
        self._server = _Server(("127.0.0.1", 18085), _Handler)
        self._server.responses = deque()
        self._server.requests = []
        self._server.before_response_callbacks = deque()
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    @property
    def requests(self) -> list[dict[str, Any]]:
        return self._server.requests

    def enqueue(
        self,
        body: dict[str, Any],
        *,
        before_response: Callable[[], None] | None = None,
    ) -> None:
        self._server.responses.append(body)
        self._server.before_response_callbacks.append(before_response)

    def __enter__(self) -> FakeResponsesServer:
        self._thread.start()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        del exc_type, exc, traceback
        self._server.shutdown()
        self._server.server_close()
        self._thread.join(timeout=5)
