from dataclasses import replace

import pytest
from fake_responses_server import FakeResponsesServer, final_message, response_body

from aiscc.contracts.workflow import RuntimeMode
from aiscc.providers.openai_responses import OpenAIResponsesAdapter
from aiscc.public_live.luna_profile import (
    bind_call,
    conservative_request_liability_micro,
    hosted_luna_profile,
    luna_profile,
)
from tests.unit.providers.test_openai_responses import _call


def call():
    return replace(
        _call(),
        profile=luna_profile(),
        runtime_mode=RuntimeMode.PUBLIC_BOUNDED_LIVE,
        scenario_id="stockroom-s1-normal",
        tools=(),
    )


@pytest.mark.parametrize(
    "role,effort", [("PRIMARY", "low"), ("VERIFY", "low"), ("CORRECT", "medium")]
)
def test_luna_exact_sdk_wire_and_bounds(role, effort):
    request, bound = bind_call(call(), role=role)
    assert bound <= 8000 and request.output_token_maximum == 2000
    assert request.profile.output_token_bound == 6000
    with FakeResponsesServer() as server:
        server.enqueue(response_body("completed", [final_message()]))
        result = OpenAIResponsesAdapter().call(request, secret="synthetic-local-only")
    assert result.output_text == "AISCC_FAKE_FINAL"
    assert server.requests[0]["model"] == "gpt-5.6-luna"
    assert server.requests[0]["reasoning"] == {"effort": effort}
    assert server.requests[0]["service_tier"] == "default"
    assert server.requests[0]["max_output_tokens"] == 2000


@pytest.mark.parametrize(
    "field,value",
    [
        ("model_ref", "other"),
        ("provider_id", "other"),
        ("provider_call_maximum", 5),
        ("output_token_bound", 6001),
        ("tool_call_maximum", 2),
        ("provider_retry_maximum", 2),
        ("connect_timeout_seconds", 6),
        ("read_timeout_seconds", 31),
        ("total_timeout_seconds", 36),
        ("version", "2"),
    ],
)
def test_profile_cannot_be_overridden(field, value):
    with pytest.raises(ValueError, match="LUNA_PROFILE"):
        bind_call(
            replace(call(), profile=replace(luna_profile(), **{field: value})), role="PRIMARY"
        )


@pytest.mark.parametrize(
    "url",
    ["https://api.openai.com/v1", "http://127.0.0.1.evil:80/v1", "http://user@127.0.0.1:80/v1"],
)
def test_real_endpoint_forbidden(url):
    with pytest.raises(ValueError, match="LOCAL_PROVIDER_ONLY"):
        luna_profile(url)


def test_input_tools_and_role_fail_closed():
    with pytest.raises(ValueError, match="INPUT_LIMIT"):
        bind_call(
            replace(call(), input_items=({"role": "user", "content": "x" * 8000},)), role="PRIMARY"
        )
    with pytest.raises(ValueError, match="SERVER_TEXT"):
        bind_call(
            replace(call(), input_items=({"type": "input_image", "image_url": "private"},)),
            role="PRIMARY",
        )
    with pytest.raises(ValueError, match="TOOL_SCOPE"):
        bind_call(replace(call(), tools=({"name": "shell"},)), role="PRIMARY")
    with pytest.raises(ValueError, match="LUNA_PROFILE"):
        bind_call(call(), role="user-selected")


def test_conservative_liability_is_derived_from_accepted_luna_envelope():
    assert conservative_request_liability_micro(hosted_luna_profile()) == 4400
    with pytest.raises(ValueError, match="LUNA_PROFILE"):
        conservative_request_liability_micro(replace(hosted_luna_profile(), version="2"))
