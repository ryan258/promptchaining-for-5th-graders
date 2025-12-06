#!/usr/bin/env python3
"""
🧭 Concept Simplifier (adult mode)

Break complex topics into digestible parts with analogies, examples, and a short explainer.

Usage:
    python tools/learning/concept_simplifier.py "Diffusion models in AI"
    python tools/learning/concept_simplifier.py "Topic" --context "Audience, constraints, tone"
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

from src.core.chain import MinimalChainable
from src.core.main import build_models, prompt
from src.core.artifact_store import ArtifactStore


def concept_simplifier(topic: str, additional_context: str = ""):
    print("🧭 Concept Simplifier")
    print(f"Topic: {topic}")
    if additional_context:
        print(f"Context: {additional_context}")
    print()

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Clear and direct")
    audience = user_profile.get("learning_profile", {}).get("audience", "Curious adult")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    # Create artifact store for persistent knowledge
    artifact_store = ArtifactStore()

    context_data = {
        "topic": topic,
        "tone": tone,
        "audience": audience,
        "additional_context": additional_context,
    }

    result, context_filled_prompts, usage_stats, execution_trace = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        return_trace=True,
        artifact_store=artifact_store,
        topic=topic,
        prompts=[
            # Prompt 1: Decompose with expert educator lens
            """You are an expert educator specializing in making complex topics accessible to {{audience}}.

Decompose '{{topic}}' into exactly 3 essential components using this framework:
1. **Core mechanism/process** - What actually happens?
2. **Key inputs/requirements** - What's needed?
3. **Outputs/results** - What's produced?
4. **Why it matters** - Real-world significance
5-6. **Critical nuances** (optional) - Important subtleties

For each component, explain in 1-2 clear sentences. Avoid jargon unless you immediately define it.

❌ BAD: "Utilizes enzymatic catalysis via chloroplastic mechanisms"
✅ GOOD: "Uses special molecules (enzymes) to speed up chemical reactions inside plant cells"

Example for "Machine Learning":
{
  "components": [
    {"name": "Pattern Recognition from Data", "why_it_matters": "The system finds patterns humans might miss in large datasets"},
    {"name": "Training Process", "why_it_matters": "The model learns by seeing thousands of examples and adjusting its internal rules"},
    {"name": "Prediction Output", "why_it_matters": "Once trained, it can make decisions on new data it's never seen"}
  ]
}

Respond **ONLY** with raw JSON (no markdown, no prose):
{
  "components": [
    {"name": "Component name (3-8 words)", "why_it_matters": "Practical significance in 1-2 sentences (max 40 words)"}
  ]
}

Provide exactly 3 components for '{{topic}}'. Keep the entire JSON under 140 words. Do not add explanations, commentary, or code fences.""",

            # Prompt 2: Create high-quality analogies
            """You are a master communicator who excels at creating memorable analogies.

For each component of '{{topic}}', create ONE powerful analogy from everyday experience.

Components to work with:
{{output[-1].components}}

Analogy quality criteria:
- Draw from common experiences (cooking, driving, sports, household tasks)
- Make the mapping explicit ("X is like Y because...")
- Identify where the analogy breaks down (builds credibility)
- Avoid overused analogies (brain = computer, data = oil, etc.)

Example for "Neural Networks - Weighted Connections":
✅ GOOD:
"Like a recipe where you can adjust ingredient amounts (weights) to change the final taste. More sugar = sweeter, more salt = saltier. The network adjusts these 'amounts' to improve its output."
When it breaks down: "Unlike recipes, neural networks adjust thousands of 'ingredients' simultaneously using math, not taste tests."

❌ BAD (too vague): "It's like a brain"
❌ BAD (too technical): "It's like a tensor operation"

Respond **ONLY** with raw JSON (no markdown, no prose):
{
  "analogies": [
    {
      "component": "Exact component name from previous step",
      "analogy": "Detailed analogy (2-4 sentences showing the mapping)",
      "when_it_breaks_down": "One sentence explaining the limitation"
    }
  ]
}

Create exactly one analogy per component from the previous step. Keep each analogy + breakdown to 40 words max and keep the entire JSON under 150 words. Do not add explanations, commentary, or code fences.""",

            # Prompt 3: Provide concrete, testable examples
            """You are a learning designer who creates practical exercises to verify understanding.

For each component of '{{topic}}', provide a concrete example and a self-check question.

Components and analogies:
{{output[-1].analogies}}

For each, create:
1. **Concrete example** (2-3 sentences): A specific scenario showing the concept in action
2. **Self-check question**: Tests understanding without just repeating the definition

Example format for "Encryption":
✅ GOOD example: "When you send a message through WhatsApp, it scrambles the text like putting it through a paper shredder, then reassembles it only on your friend's phone. Even if someone intercepts it mid-transit, they just see gibberish."

✅ GOOD self-check: "If someone hacks the WiFi at a coffee shop, can they read your WhatsApp messages? Why or why not?"

❌ BAD self-check (too easy): "What is encryption?" (just asks for definition)
❌ BAD self-check (too hard): "Explain the mathematics of RSA cryptography" (too technical)

Respond **ONLY** with raw JSON (no markdown, no prose):
{
  "examples": [
    {
      "component": "Component name from step 1",
      "example": "2-3 sentence concrete scenario showing this in real use",
      "check_yourself": "Single question starting with 'What would happen if...', 'Why does...', 'How would you...', or 'Can you explain why...'"
    }
  ]
}

Provide exactly one example per component. Keep each example + question to 40 words max and keep the entire JSON under 150 words. Do not add explanations, commentary, or code fences.""",

            # Prompt 4: Synthesize into cohesive explainer
            """You are a skilled technical writer creating a concise yet complete explanation.

Write a 6-10 sentence explainer for '{{topic}}' that synthesizes everything we've built.

Audience: {{audience}}
Tone: {{tone}}
Additional context: {{additional_context}}

Use these building blocks:
- Components: {{output[-3].components}}
- Analogies: {{output[-2].analogies}}
- Examples: {{output[-1].examples}}

Structure your explainer:
1. Opening (1 sentence): What is {{topic}} in simplest terms?
2. Core mechanism (2-3 sentences): How does it work? Weave in your best analogy.
3. Why it matters (1-2 sentences): Real-world impact or application
4. Common pitfall (1 sentence): What do people misunderstand?
5. Practical takeaway (1 sentence): What should the reader remember?

Example opening for "Blockchain":
✅ GOOD: "A blockchain is a shared record book that many people keep copies of, making it nearly impossible to cheat because everyone can verify what's written."
❌ BAD: "Blockchain is a distributed ledger technology utilizing cryptographic hashing." (too technical)

Respond **ONLY** with raw JSON (no markdown, no prose):
{
 "explainer": "Your 6-10 sentence explanation as a single continuous text (no bullet points)",
 "pitfalls": ["Common misunderstanding #1 (max 20 words)", "Common misunderstanding #2 (max 20 words)"],
 "next_steps": ["Actionable next step #1 (max 15 words)", "Actionable next step #2 (max 15 words)"]
}

Keep explainer to 120-150 words total. Provide 2-3 pitfalls and 2-3 next_steps. If any input is missing or unclear, still return valid JSON with your best effort; never return empty output. Do not add explanations, commentary, or code fences."""
        ],
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "learning", "concept_simplifier")
    os.makedirs(output_dir, exist_ok=True)

    # Save the execution trace (includes full chain visualization data)
    output_path = os.path.join(output_dir, f"{timestamp}-{topic[:50].replace(' ', '_')}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(execution_trace, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("concept_simplifier", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")
    print()
    print(artifact_store.visualize())


def main():
    topic, context = get_input_from_args(
        description="Break complex topics into digestible parts with analogies and a short explainer"
    )
    concept_simplifier(topic, context)


if __name__ == "__main__":
    main()
