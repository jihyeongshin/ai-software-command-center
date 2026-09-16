import json
import sys
from dataclasses import replace
from types import SimpleNamespace

import pytest

from aiscc.providers.hosted_secret import SECRET_VARIABLE, HostedOpenAISecretResolver
from aiscc.providers.openai_responses import OpenAIResponsesAdapter
from aiscc.public_live.luna_profile import bind_call, hosted_luna_profile
from aiscc.runtime.child_environment import child_environment
from aiscc.runtime.process import BoundedProcessRunner
from tests.fixtures.providers.luna_capabilities import execution_for
from tests.unit.providers.test_luna_profile import call


def prepared():
    return bind_call(
        replace(call(), profile=hosted_luna_profile(), principal="owner", state_version=2),
        role="PRIMARY",
    )[0]


def execution(request, adapter):
    return execution_for(
        request,
        {"role": "PRIMARY", "outcome": "STARTED", "model": "gpt-5.6-luna", "effort": "low"},
        adapter,
        resolver_factory=HostedOpenAISecretResolver,
    )


def test_hosted_mediated_sdk_binding_and_no_serialization(monkeypatch, capsys):
    sentinel = "fake-sentinel-for-hosted-boundary-only"
    monkeypatch.setenv(SECRET_VARIABLE, sentinel)
    observed = []

    def client(**kwargs):
        assert kwargs["api_key"] == sentinel
        assert kwargs["base_url"] == "https://api.openai.com/v1"
        assert kwargs["max_retries"] == 0

        def create(**request):
            observed.append(request)
            return SimpleNamespace(
                http_response=SimpleNamespace(
                    json=lambda: {
                        "status": "completed",
                        "id": "synthetic-response",
                        "output": [],
                        "usage": {"input_tokens": 1, "output_tokens": 0},
                    }
                )
            )

        return SimpleNamespace(
            responses=SimpleNamespace(with_raw_response=SimpleNamespace(create=create))
        )

    monkeypatch.setattr("aiscc.providers.openai_responses.OpenAI", client)
    request = prepared()
    adapter = OpenAIResponsesAdapter(hosted=True)
    service, capabilities, selector, resolver = execution(request, adapter)
    result = service.execute_provider(request, capabilities=capabilities, secret_request=selector)
    assert len(observed) == 1
    assert observed[0]["store"] is False and observed[0]["stream"] is False
    assert observed[0]["background"] is False
    assert observed[0]["parallel_tool_calls"] is False
    assert observed[0]["truncation"] == "disabled"
    assert sentinel not in repr((request, result, selector, service.counters, adapter.last_request))
    assert sentinel not in str(capsys.readouterr())
    # Same consumed capabilities cannot yield a second resolution/send.
    service.execute_provider(request, capabilities=capabilities, secret_request=selector)
    assert len(observed) == 1
    with pytest.raises(ValueError, match="SECRET_LEASE_DENIED"):
        resolver.resolve(selector.secret_ref)


@pytest.mark.parametrize("value", [None, "", "   "])
def test_missing_secret_never_constructs_sdk(monkeypatch, value):
    monkeypatch.delenv(SECRET_VARIABLE, raising=False)
    if value is not None:
        monkeypatch.setenv(SECRET_VARIABLE, value)
    monkeypatch.setattr(
        "aiscc.providers.openai_responses.OpenAI",
        lambda **kw: pytest.fail("SDK must not be constructed"),
    )
    request = prepared()
    service, capabilities, selector, _ = execution(request, OpenAIResponsesAdapter(hosted=True))
    result = service.execute_provider(request, capabilities=capabilities, secret_request=selector)
    assert result.sanitized_error == "LIVE_UNAVAILABLE"
    assert service.counters.provider_calls == 0
    # Public HTTP/static composition does not construct a credential resolver.
    from aiscc.public_live.http import create_app

    assert create_app() is not None


def test_hosted_endpoint_stays_opt_in():
    with pytest.raises(ValueError, match="REAL_PROVIDER_ENDPOINT_FORBIDDEN"):
        OpenAIResponsesAdapter().call(prepared(), secret="fake-only")


def test_real_child_has_no_secret_or_sdk_autodiscovery(monkeypatch):
    monkeypatch.setenv(SECRET_VARIABLE, "fake-only")
    monkeypatch.setenv("OPENAI_API_KEY", "fake-autodiscovery-only")
    monkeypatch.setenv("PYTHONPATH", "fake-injection")
    result = BoundedProcessRunner._run_unchecked(
        [sys.executable, "-B", "-c", "import os,json; print(json.dumps(sorted(os.environ)))"],
        timeout_seconds=5,
        max_attempts=1,
        cancel=None,
        security_reason="SENTINEL_TEST",
        security_provenance={},
    )
    names = json.loads(result.stdout)
    assert SECRET_VARIABLE not in names and "OPENAI_API_KEY" not in names
    assert "PYTHONPATH" not in names
    assert SECRET_VARIABLE not in child_environment()


def test_docker_cli_and_git_observer_do_not_inherit_secret(monkeypatch, tmp_path):
    import subprocess

    from aiscc.providers.external_ide import LocalGitObserver
    from aiscc.runtime.docker import DockerRuntime

    monkeypatch.setenv(SECRET_VARIABLE, "fake-only")
    observed = []

    def run(argv, **kwargs):
        assert SECRET_VARIABLE not in kwargs["env"]
        assert "OPENAI_API_KEY" not in kwargs["env"]
        observed.append(argv)
        return subprocess.CompletedProcess(
            argv, 0, b"" if "env" in kwargs and not kwargs.get("text") else "", b""
        )

    monkeypatch.setattr(subprocess, "run", run)
    DockerRuntime(None).info()
    LocalGitObserver(sys.executable)._read(tmp_path, ["status"])
    assert len(observed) == 2
