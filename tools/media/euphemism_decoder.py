#!/usr/bin/env python3
"""
🧹 Euphemism Decoder (adult mode)

Turn sanitized language into plain English, expose intent, and flag manipulation.

Usage:
    python tools/media/euphemism_decoder.py "Quoted text"
    cat speech.txt | python tools/media/euphemism_decoder.py
"""

import os
import json
from datetime import datetime

try:
    from tools.tool_utils import setup_project_root, load_user_context, get_input_from_args
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from tools.tool_utils import setup_project_root, load_user_context, get_input_from_args

project_root = setup_project_root(__file__)

from chain import MinimalChainable
from main import build_models, prompt


def euphemism_decoder(text: str):
    print("🧹 Euphemism Decoder")
    print(f"Input text: {text[:140]}{'...' if len(text) > 140 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Blunt clarity")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "speech": text,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Identify euphemisms
            """You are a plain-language editor. Identify euphemisms/softeners and map them to literal meanings.
Tone: {{tone}}

Text:
{{speech}}

Keep 5 entries max; include evidence snippet for each.

Respond in JSON:
{
  "euphemisms": [
    {"term": "euphemism", "literal": "plain meaning", "evidence": "snippet"}
  ]
}""",
            # Translate to plain English
            """Rewrite the text in plain English, replacing euphemisms with literal meanings.

Mappings: {{output[-1].euphemisms}}

Respond in JSON:
{
  "plain_english": "rewritten text"
}""",
            # Reveal intent
            """Explain why this language was chosen and what reactions it tries to avoid or provoke.
Give one GOOD vs BAD intent note:
GOOD: "Avoids admitting civilian casualties; aims to maintain domestic support"
BAD: "They want to sound nice" (too vague)

Plain text: {{output[-1].plain_english}}
Mappings: {{output[-2].euphemisms}}

Respond in JSON:
{
  "hidden_reality": "what's actually happening",
  "intended_effect": "emotional/cognitive outcome",
  "who_benefits": ["actor1", "actor2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "media", "euphemism_decoder")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-euphemism_decoder.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("euphemism_decoder", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    speech, _ = get_input_from_args(
        description="Decode euphemistic language into plain English and expose intent",
        default_context_help="(unused)"
    )
    euphemism_decoder(speech)


if __name__ == "__main__":
    main()
