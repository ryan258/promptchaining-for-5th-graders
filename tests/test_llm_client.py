from types import SimpleNamespace
from unittest.mock import MagicMock

from lib.core import llm_client


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
