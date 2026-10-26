"""Small deterministic bounds for explicit local framework operations."""

import re

from .errors import InputError

MAX_DEPTH = 5
MAX_ROUNDS = 5
MAX_CHAIN_STEPS = 32


def bounded_count(value: int, name: str, maximum: int = 5) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= maximum:
        raise InputError(f"{name} must be an integer from 1 to {maximum}.")
    return value


def validate_prompts(prompts, maximum: int = MAX_CHAIN_STEPS) -> None:
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= maximum:
        raise InputError(f"Choose 1–{maximum} prompts for this operation.")
    for index, text in enumerate(prompts):
        if not isinstance(text, str) or not text.strip() or len(text) > 120000:
            raise InputError(f"Prompt {index + 1} must contain 1–120,000 characters.")
        for match in re.finditer(r"(?<!\{)\{\{\s*(output\[[^}]+)\}\}(?!\})", text):
            reference = re.fullmatch(r"output\[-([1-9][0-9]*)\](?:\.[A-Za-z_][A-Za-z0-9_]*)?\s*", match[1])
            if reference is None or int(reference[1]) > index:
                raise InputError(f"Prompt {index + 1} has an unsupported or forward output reference.")
