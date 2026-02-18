# llm_client.py - Shared LLM client helpers
# Keep LLM wiring separate from demos and app entrypoints.

from typing import Any, List, Tuple
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import random


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


def build_models():
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

    if not openrouter_api_key:
        raise ValueError(
            "🔑 Missing API key! Please:\n"
            "   1. Copy .env.example to .env\n"
            "   2. Get your key from https://openrouter.ai/keys\n"
            "   3. Add it to your .env file as OPENROUTER_API_KEY=your_key_here"
        )

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=openrouter_api_key,
    )

    env_models = os.getenv("OPENROUTER_MODELS")
    if env_models:
        model_names = [m.strip() for m in env_models.split(",") if m.strip()]
    else:
        model_names = [
            "openai/gpt-3.5-turbo",
            "google/gemini-flash-1.5",
            "google/gemini-pro-1.5",
        ]

    if not model_names:
        raise ValueError("No models configured. Please check your model list.")

    return client, model_names


def prompt(model_info: Tuple[OpenAI, str], prompt_text: str):
    """
    Send a prompt to an AI model and return (content, usage).
    """
    client, model_name = model_info

    max_retries = 3
    base_delay = 1
    max_delay = 10

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt_text}],
                # Avoid default token limit
                max_tokens=4096,
                temperature=0.7,
                timeout=30.0,
                extra_headers={
                    "HTTP-Referer": os.getenv(
                        "OPENROUTER_SITE_URL",
                        "https://github.com/ryanjohnson/promptchaining-for-5th-graders",
                    ),
                    "X-Title": os.getenv(
                        "OPENROUTER_APP_NAME",
                        "Prompt Chaining for 5th Graders",
                    ),
                },
            )

            content = response.choices[0].message.content
            usage = response.usage

            if not content:
                raise ValueError("Received empty content from API")

            return content, usage

        except Exception as e:
            print(f"⚠️ Attempt {attempt + 1}/{max_retries} failed: {e}")

            if attempt == max_retries - 1:
                raise e

            delay = min(max_delay, base_delay * (2 ** attempt))
            jitter = random.uniform(0, 0.1 * delay)
            sleep_time = delay + jitter

            print(f"⏳ Waiting {sleep_time:.2f}s before retry...")
            time.sleep(sleep_time)
