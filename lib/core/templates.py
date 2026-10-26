"""One-pass framework handoffs: inserted user/model text is always data."""

import json
import re

from .artifact_store import resolve_artifact_references
from .errors import InputError

TOKEN = re.compile(r"\{\{\{\{([^{}]+?)\}\}\}\}|\{\{\s*([^{}]+?)\s*\}\}")
OUTPUT = re.compile(r"output\[-([1-9][0-9]*)\](?:\.([A-Za-z_][A-Za-z0-9_]*))?")


def render_template(template: str, context: dict, outputs: list, artifact_store=None) -> tuple[str, list[str]]:
    used = []

    def replace(match):
        if match[1] is not None:
            # Four braces quote a literal placeholder in a prompt-design lesson.
            return "{{" + match[1] + "}}"
        token = match[2]
        if token in context:
            value = context[token]
        elif token.startswith("artifact:"):
            if artifact_store is None:
                raise InputError("This prompt needs an artifact store.")
            value, keys = resolve_artifact_references("{{" + token + "}}", artifact_store)
            used.extend(keys)
            if not keys:
                raise InputError("A referenced artifact was not found. Check the prompt before running it.")
        else:
            reference = OUTPUT.fullmatch(token)
            if reference is None or int(reference[1]) > len(outputs):
                raise InputError("A prompt contains an unknown or unavailable placeholder. Check its inputs and earlier-answer references.")
            value = outputs[-int(reference[1])]
            if reference[2]:
                try:
                    value = json.loads(value) if isinstance(value, str) else value
                    value = value[reference[2]]
                except (ValueError, KeyError, TypeError):
                    raise InputError("An earlier answer lacks a required JSON field. Check the answer and prompt before trying again.") from None
        return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)

    rendered = TOKEN.sub(replace, template)
    if len(rendered) > 120000:
        raise InputError("The rendered prompt exceeds 120,000 characters. Reduce its inputs before running.")
    return rendered, used
