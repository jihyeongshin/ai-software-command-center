from __future__ import annotations

from types import SimpleNamespace

from aiscc.providers.hosted_secret import SECRET_VARIABLE
from aiscc.public_live.real_luna_canary import run_real_luna_canary


def test_real_luna_canary_is_one_mediated_send(monkeypatch):
    sentinel = "synthetic-test-secret-never-exported"
    observed = []
    monkeypatch.setenv("RAILWAY_SERVICE_NAME", "aiscc-public-live-worker")
    monkeypatch.setenv("RAILWAY_ENVIRONMENT_NAME", "production")
    monkeypatch.setenv(SECRET_VARIABLE, sentinel)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    def client(**kwargs):
        assert kwargs["api_key"] == sentinel
        assert kwargs["base_url"] == "https://api.openai.com/v1"
        assert kwargs["max_retries"] == 0

        def create(**request):
            observed.append(request)
            return SimpleNamespace(
                http_response=SimpleNamespace(
                    json=lambda: {
                        "id": "synthetic-response-id",
                        "status": "completed",
                        "output": [
                            {
                                "type": "message",
                                "role": "assistant",
                                "content": [{"type": "output_text", "text": "READY"}],
                            }
                        ],
                        "output_text": "READY",
                        "usage": {"input_tokens": 20, "output_tokens": 1, "total_tokens": 21},
                    }
                )
            )

        return SimpleNamespace(
            responses=SimpleNamespace(with_raw_response=SimpleNamespace(create=create))
        )

    monkeypatch.setattr("aiscc.providers.openai_responses.OpenAI", client)
    result = dict(run_real_luna_canary())

    assert len(observed) == 1
    assert result["classification"] == "REAL_LUNA_CANARY_PASS_CANDIDATE"
    assert result["invocation_count_before"] == 0
    assert result["invocation_count_after"] == 1
    assert result["provider_call_count"] == 1
    assert result["resolver_call_count"] == 1
    assert result["lease_reusable"] is False
    assert result["output_exported"] is False
    assert result["request"] == {
        "model": "gpt-5.6-luna",
        "service_tier": "default",
        "reasoning_effort": "low",
        "store": False,
        "stream": False,
        "background": False,
        "parallel_tool_calls": False,
        "truncation": "disabled",
        "max_output_tokens": 2000,
        "tool_count": 0,
    }
    assert sentinel not in repr(result)


def test_real_luna_canary_rejects_non_worker_environment(monkeypatch):
    monkeypatch.setenv("RAILWAY_SERVICE_NAME", "aiscc-public-live-api")
    monkeypatch.setenv("RAILWAY_ENVIRONMENT_NAME", "production")
    monkeypatch.setenv(SECRET_VARIABLE, "synthetic-test-secret-never-exported")

    try:
        run_real_luna_canary()
    except RuntimeError as error:
        assert str(error) == "REAL_LUNA_CANARY_WORKER_ENVIRONMENT_DENIED"
    else:
        raise AssertionError("non-worker environment must be rejected")
