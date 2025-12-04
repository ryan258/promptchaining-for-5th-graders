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
            """You are an Orwellian Scholar and Plain Language Advocate. Decode "Doublespeak" and "Sanitized Language".

Identify terms that obscure reality or minimize impact.
Tone: {{tone}}

Text:
{{speech}}

Perspective Framework:
- Softening: Making bad things sound neutral (e.g., "Kinetic action" vs "Bombing").
- Abstraction: Removing human agency (e.g., "Mistakes were made").

Constraints:
- Identify exactly 5 euphemisms.
- "Literal": The brutal, unvarnished truth (max 5 words).
- "Evidence": Quote the exact snippet.

Respond in JSON:
{
  "euphemisms": [
    {"term": "Euphemism used", "literal": "Plain meaning", "evidence": "Quote snippet"}
  ]
}""",
            # Translate to plain English
            """Rewrite the text in "Radical Candor" style. Remove all obfuscation.

Mappings: {{output[-1].euphemisms}}

Constraints:
- Rewrite the entire text.
- Must be shorter than the original.
- Tone: Blunt, factual, and direct.

Respond in JSON:
{
  "plain_english": "The rewritten text."
}""",
            # Reveal intent
            """Analyze the "Political Utility" of this language. Why hide the truth?

Plain text: {{output[-1].plain_english}}
Mappings: {{output[-2].euphemisms}}

Constraints:
- "Hidden Reality": What specific fact is being hidden? (Max 1 sentence).
- "Intended Effect": How does this manipulate the audience's feelings? (Max 1 sentence).
- "Who Benefits": Exactly 2 actors.

Respond in JSON:
{
  "hidden_reality": "The specific ugly truth.",
  "intended_effect": "To prevent outrage/panic.",
  "who_benefits": ["Actor 1", "Actor 2"]
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
