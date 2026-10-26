# llm_client.py - Shared LLM client helpers
# Keep LLM wiring separate from demos and app entrypoints.

from functools import lru_cache
from typing import Any, Dict, List, Tuple
from openai import OpenAI
from dotenv import load_dotenv
import os
import math


DEFAULT_MODELS = (
    "openai/gpt-3.5-turbo",
    "google/gemini-flash-1.5",
    "google/gemini-pro-1.5",
)


def configured_model_names() -> Tuple[str, ...]:
    """Read model names without constructing a client or making a request."""
    load_dotenv()
    env_models = os.getenv("OPENROUTER_MODELS", "")
    default_model = os.getenv("DEFAULT_MODEL", "")
    if env_models.strip():
        names = tuple(dict.fromkeys(m.strip() for m in env_models.split(",") if m.strip()))
    elif default_model.strip():
        names = (default_model.strip(),)
    else:
        names = DEFAULT_MODELS
    if not names or len(names) > 30 or any(len(name) > 200 for name in names):
        raise ValueError("Configure 1–30 model IDs in OPENROUTER_MODELS.")
    return names


def has_api_key() -> bool:
    load_dotenv()
    value = os.getenv("OPENROUTER_API_KEY", "").strip()
    return bool(value and value not in {"sk-or-your-key-here", "your_key_here"})


def get_model() -> Tuple[OpenAI, str]:
    """Return a ready-to-use (client, model_name) tuple using the first configured model."""
    client, model_names = build_models()
    return client, model_names[0]


def calculate_total_tokens(usage_list: List[Any]) -> int:
    """Sum token counts from a list of usage dicts or usage objects."""
    total = 0
    for usage in usage_list:
        if isinstance(usage, dict):
            if "total_tokens" in usage:
                total += usage["total_tokens"]
            else:
                total += usage.get("prompt_tokens", 0) + usage.get("completion_tokens", 0)
        else:
            if hasattr(usage, "total_tokens"):
                total += getattr(usage, "total_tokens", 0)
            else:
                total += getattr(usage, "prompt_tokens", 0) + getattr(usage, "completion_tokens", 0)
    return total


@lru_cache(maxsize=1)
def build_models() -> Tuple[OpenAI, Tuple[str, ...]]:
    """
    Set up AI models for OpenRouter.
    """
    load_dotenv()
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
    openrouter_site_url = os.getenv(
        "OPENROUTER_SITE_URL",
        "https://github.com/ryanjohnson/promptchaining-for-5th-graders",
    )
    openrouter_app_name = os.getenv(
        "OPENROUTER_APP_NAME",
        "Prompt Chaining for 5th Graders",
    )

    if not has_api_key():
        raise ValueError(
            "🔑 Missing API key! Please:\n"
            "   1. Copy .env.example to .env\n"
            "   2. Get your key from https://openrouter.ai/keys\n"
            "   3. Add it to your .env file as OPENROUTER_API_KEY=your_key_here"
        )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key,
        max_retries=0,
    )

    model_names = configured_model_names()

    return client, model_names


@lru_cache(maxsize=1)
def get_prompt_settings() -> Dict[str, Any]:
    """Load prompt configuration once so repeated calls don't reparse the environment."""
    load_dotenv()
    max_tokens = int(os.getenv("MAX_TOKENS", "4096"))
    temperature = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
    timeout = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30.0"))
    if not 64 <= max_tokens <= 12000:
        raise ValueError("MAX_TOKENS must be between 64 and 12000.")
    if not math.isfinite(temperature) or not 0 <= temperature <= 2:
        raise ValueError("DEFAULT_TEMPERATURE must be between 0 and 2.")
    if not math.isfinite(timeout) or not 1 <= timeout <= 120:
        raise ValueError("REQUEST_TIMEOUT_SECONDS must be between 1 and 120.")
    return {
        "max_tokens": max_tokens,
        "temperature": temperature,
        "timeout": timeout,
        "headers": {
            "HTTP-Referer": os.getenv(
                "OPENROUTER_SITE_URL",
                "https://github.com/ryanjohnson/promptchaining-for-5th-graders",
            ),
            "X-Title": os.getenv(
                "OPENROUTER_APP_NAME",
                "Prompt Chaining for 5th Graders",
            ),
        },
    }


def prompt_once(model_info: Tuple[OpenAI, str], prompt_text: str):
    """One explicit request. Resumable runs never silently retry billable work."""
    client, model_name = model_info
    settings = get_prompt_settings()
    response = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt_text}],
        max_tokens=settings["max_tokens"],
        temperature=settings["temperature"],
        timeout=settings["timeout"],
        extra_headers=settings["headers"],
    )
    content = response.choices[0].message.content
    if not content:
        raise ValueError("The provider returned no text. Try a model that supports text responses.")
    if getattr(response.choices[0], "finish_reason", None) == "length":
        # Preserve a useful partial answer instead of charging for a second call.
        content += "\n\n[Stopped at the configured token limit. Review this answer before continuing.]"
    return content, response.usage


def prompt(model_info: Tuple[OpenAI, str], prompt_text: str):
    """One explicit request for framework callers; the human owns any retry."""
    return prompt_once(model_info, prompt_text)
