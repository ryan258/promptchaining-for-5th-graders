from types import SimpleNamespace
from unittest.mock import MagicMock

import httpx
import pytest
from openai import RateLimitError

from lib.core import llm_client
from lib.core.chain import MinimalChainable
from lib.core.errors import InputError
from lib.workbench.models import Recipe, Run, Step
from lib.workbench.runner import Runner
from lib.workbench.store import Store


def test_build_models_prefers_openrouter_models_and_caches(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("OPENROUTER_MODELS", "alpha,beta")
    monkeypatch.setenv("DEFAULT_MODEL", "fallback-model")
    monkeypatch.setattr(llm_client, "load_dotenv", lambda: None)

    openai_ctor = MagicMock(return_value=object())
    monkeypatch.setattr(llm_client, "OpenAI", openai_ctor)

    client_one, models_one = llm_client.build_models()
    client_two, models_two = llm_client.build_models()

    assert client_one is client_two
    assert models_one == ("alpha", "beta")
    assert models_two == ("alpha", "beta")
    assert openai_ctor.call_count == 1


def test_build_models_falls_back_to_default_model(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.delenv("OPENROUTER_MODELS", raising=False)
    monkeypatch.setenv("DEFAULT_MODEL", "solo-model")
    monkeypatch.setattr(llm_client, "load_dotenv", lambda: None)
    monkeypatch.setattr(llm_client, "OpenAI", MagicMock(return_value=object()))

    _, models = llm_client.build_models()

    assert models == ("solo-model",)


def test_free_workbench_run_uses_the_router_and_stops_at_a_rate_limit(tmp_path, monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")
    monkeypatch.setenv("OPENROUTER_MODELS", "test/other-model")
    monkeypatch.setattr(llm_client, "load_dotenv", lambda: None)
    free_model = llm_client.OPENROUTER_FREE_MODEL
    rate_limit = RateLimitError("Test rate limit", response=httpx.Response(
        429, request=httpx.Request("POST", "https://openrouter.ai/api/v1/chat/completions"),
    ), body=None)
    create = MagicMock(side_effect=[SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="First answer"), finish_reason="stop")],
        model="test/served-model:free",
    ), rate_limit])
    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
    openai_ctor = MagicMock(return_value=client)
    monkeypatch.setattr(llm_client, "OpenAI", openai_ctor)
    store = Store(tmp_path / "workspace")
    run = store.create_run(Run(recipe=Recipe(title="Free run", steps=[
        Step(name="First", prompt="Explain {{topic}}."),
        Step(name="Second", prompt="Use {{output[-1]}}."),
    ]), topic="the Moon", model=free_model))
    runner = Runner(store)
    try:
        runner.start(run.id, run.revision).result(timeout=3)
        paused = store.get_run(run.id)
        assert paused.state == "paused" and len(paused.results) == 1
        assert paused.results[0].response_model == "test/served-model:free"
        runner.start(run.id, paused.revision).result(timeout=3)
        failed = store.get_run(run.id)
        assert failed.state == "failed" and failed.results == paused.results
        assert "rate limit" in failed.error
        assert [call.kwargs["model"] for call in create.call_args_list] == [free_model, free_model]
        assert openai_ctor.call_count == 1 and openai_ctor.call_args.kwargs["max_retries"] == 0
    finally:
        runner.close()


def test_prompt_uses_environment_settings(monkeypatch):
    monkeypatch.setenv("MAX_TOKENS", "123")
    monkeypatch.setenv("DEFAULT_TEMPERATURE", "0.25")
    monkeypatch.setenv("REQUEST_TIMEOUT_SECONDS", "9.5")
    monkeypatch.setenv("OPENROUTER_SITE_URL", "https://example.com")
    monkeypatch.setenv("OPENROUTER_APP_NAME", "Prompt Tests")
    monkeypatch.setattr(llm_client, "load_dotenv", lambda: None)

    create = MagicMock(
        return_value=SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content="ok"))],
            usage={"prompt_tokens": 1, "completion_tokens": 2},
        )
    )
    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))

    content, usage = llm_client.prompt((client, "mock-model"), "hello")

    assert content == "ok"
    assert usage == {"prompt_tokens": 1, "completion_tokens": 2}
    kwargs = create.call_args.kwargs
    assert kwargs["max_tokens"] == 123
    assert kwargs["temperature"] == 0.25
    assert kwargs["timeout"] == 9.5
    assert kwargs["extra_headers"]["HTTP-Referer"] == "https://example.com"
    assert kwargs["extra_headers"]["X-Title"] == "Prompt Tests"


def test_workbench_prompt_dispatches_once_and_preserves_truncation(monkeypatch):
    monkeypatch.setattr(llm_client, "load_dotenv", lambda: None)
    create = MagicMock(return_value=SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="A partial answer"), finish_reason="length")], usage=None))
    client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
    content, _ = llm_client.prompt_once((client, "test-model"), "hello")
    assert "configured token limit" in content
    assert create.call_count == 1
    create.side_effect = RuntimeError("provider failure")
    with pytest.raises(RuntimeError):
        llm_client.prompt_once((client, "test-model"), "hello")
    assert create.call_count == 2  # One additional call, no hidden retry.


def test_incomplete_provider_json_keeps_provenance_and_blocks_dependent_call():
    partial = llm_client.Completion('```json\n{"a": 1}\n```', {"total_tokens": 12}, "length", "id-1", "actual-model")
    request = MagicMock(return_value=partial)
    outputs, _, _, trace = MinimalChainable.run({}, None, request, ["First"], return_trace=True)
    assert outputs == [partial.text]
    assert trace["total_tokens"] == 12 and trace["usage_complete"]
    assert not trace["completion_complete"]
    assert trace["steps"][0]["response_id"] == "id-1"
    assert trace["steps"][0]["response_model"] == "actual-model"
    request.reset_mock()
    with pytest.raises(InputError, match="did not finish"):
        MinimalChainable.run({}, None, request, ["First", "Use {{output[-1].a}}"])
    assert request.call_count == 1
