# llm_client.py - Shared LLM client helpers
# Keep LLM wiring separate from demos and app entrypoints.

from dataclasses import dataclass
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
OPENROUTER_FREE_MODEL = "openrouter/free"


def configured_model_names(*, for_workbench: bool = False) -> Tuple[str, ...]:
    """Read model names without constructing a client or making a request."""
    load_dotenv()
    env_models = os.getenv("OPENROUTER_MODELS", "")
    default_model = os.getenv("DEFAULT_MODEL", "")
    if env_models.strip():
        names = tuple(dict.fromkeys(m.strip() for m in env_models.split(",") if m.strip()))
    elif default_model.strip():
        names = (default_model.strip(),)
    else:
        names = (OPENROUTER_FREE_MODEL,) if for_workbench else DEFAULT_MODELS
    if not names or len(names) > 30 or any(len(name) > 200 for name in names):
        raise ValueError("Configure 1–30 model IDs in OPENROUTER_MODELS.")
    if for_workbench and OPENROUTER_FREE_MODEL not in names:
        names += (OPENROUTER_FREE_MODEL,)
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
    """Sum reported totals. The caller may check completeness separately."""
    return sum(normalize_usage(usage).get("total_tokens", 0) for usage in usage_list)


def normalize_usage(usage: Any) -> dict[str, int]:
    """Keep available nonnegative counts, preserving the distinction from zero."""
    counts = {}
    for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
        value = usage.get(key) if isinstance(usage, dict) else getattr(usage, key, None)
        if type(value) is int and value >= 0:
            counts[key] = value
    if "total_tokens" not in counts and {"prompt_tokens", "completion_tokens"} <= counts.keys():
        counts["total_tokens"] = counts["prompt_tokens"] + counts["completion_tokens"]
    return counts


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


def build_workbench_models() -> Tuple[OpenAI, Tuple[str, ...]]:
    client, _ = build_models()
    return client, configured_model_names(for_workbench=True)


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


@dataclass(frozen=True)
class Completion:
    text: str
    usage: Any = None
    finish_reason: str | None = None
    response_id: str | None = None
    response_model: str | None = None


def request_completion(model_info: Tuple[OpenAI, str], prompt_text: str) -> Completion:
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
    choice = response.choices[0] if response.choices else None
    content = choice.message.content if choice is not None else None
    if not isinstance(content, str) or not content.strip():
        raise ValueError("The provider returned no text. Try a model that supports text responses.")
    return Completion(content, getattr(response, "usage", None), getattr(choice, "finish_reason", None),
                      getattr(response, "id", None), getattr(response, "model", None))


def prompt_once(model_info: Tuple[OpenAI, str], prompt_text: str):
    """Compatibility API returning answer text and the original usage object."""
    completion = request_completion(model_info, prompt_text)
    content = completion.text
    if completion.finish_reason == "length":
        # Preserve a useful partial answer instead of charging for a second call.
        content += "\n\n[Stopped at the configured token limit. Review this answer before continuing.]"
    return content, completion.usage


def prompt(model_info: Tuple[OpenAI, str], prompt_text: str):
    """One explicit request for framework callers; the human owns any retry."""
    return prompt_once(model_info, prompt_text)
