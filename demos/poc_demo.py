#!/usr/bin/env python3
# poc_demo.py - Proof of Concept demos for MinimalChainable and FusionChain
# Run: python demos/poc_demo.py

import sys
import os
import json
from typing import List

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.core.chain import MinimalChainable, FusionChain
from lib.core.llm_client import build_models, prompt


def prompt_chainable_poc():
    """
    POC means "Proof of Concept" - we're proving that our idea works!

    We're going to:
    1. Ask AI to create a blog post title about AI Agents
    2. Ask AI to create a hook for that title
    3. Ask AI to write the first paragraph using the title and hook

    Each step builds on the previous one, like building with blocks!
    """

    client, model_names = build_models()
    model_info = (client, model_names[0])

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context={"topic": "AI Agents"},
        model=model_info,
        llm_callable=prompt,
        prompts=[
            # PROMPT #1: Create a blog title
            # {{topic}} gets replaced with "AI Agents"
            "Generate one blog post title about: {{topic}}. Respond in strictly in JSON in this format: {\"title\": \"<title>\"}",

            # PROMPT #2: Create a hook for that title
            # {{output[-1].title}} gets the title from the previous response
            "Generate one hook for the blog post title: {{output[-1].title}}",

            # PROMPT #3: Write the first paragraph
            # {{output[-2].title}} gets the title from 2 prompts ago
            # {{output[-1]}} gets the hook from the last prompt
            """Based on the BLOG_TITLE and BLOG_HOOK, generate the first paragraph of the blog post.
BLOG_TITLE:
{{output[-2].title}}
BLOG_HOOK:
{{output[-1]}}""",
        ],
        return_usage=True,
    )

    chained_prompts = MinimalChainable.to_delim_text_file(
        "poc_context_filled_prompts",
        context_filled_prompts
    )

    chainable_result = MinimalChainable.to_delim_text_file(
        "poc_prompt_results",
        result
    )

    print(f"\n\n📖 Prompts~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n\n{chained_prompts}")
    print(f"\n\n📊 Results~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n\n{chainable_result}")

    MinimalChainable.log_to_markdown("poc_demo", context_filled_prompts, result, usage_stats)


def fusion_chain_poc():
    """
    This function shows how to use FusionChain to make AI models compete!

    Instead of using just one AI model, we use three different ones
    and make them all answer the same questions. Then we pick the best answer!
    """

    client, model_names = build_models()
    all_models = [(client, name) for name in model_names]

    def evaluator(outputs: List[str]) -> tuple:
        scores = [len(output) for output in outputs]
        max_score = max(scores) if scores else 0
        normalized_scores = [(score / max_score) if max_score > 0 else 0 for score in scores]
        if not outputs:
            return "No output to evaluate.", []
        top_response = outputs[scores.index(max_score)] if scores else "No output to evaluate."
        return top_response, normalized_scores

    result = FusionChain.run(
        context={"topic": "AI Agents"},
        models=all_models,
        llm_callable=prompt,
        prompts=[
            "Generate one blog post title about: {{topic}}. Respond in strictly in JSON in this format: {'title': '<title>'}",
            "Generate one hook for the blog post title: {{output[-1].title}}",
            """Based on the BLOG_TITLE and BLOG_HOOK, generate the first paragraph of the blog post.
BLOG_TITLE:
{{output[-2].title}}
BLOG_HOOK:
{{output[-1]}}""",
        ],
        evaluator=evaluator,
        get_model_name=lambda model_info: model_info[1],
    )

    result_dump = result.model_dump()

    print("\n\n📊 FusionChain Results~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(json.dumps(result_dump, indent=4))

    with open("poc_fusion_chain_result.json", "w") as json_file:
        json.dump(result_dump, json_file, indent=4)


def verify_setup():
    """Test that the API connection and model config are working."""
    print("🔧 Testing your AI setup...")

    try:
        client, model_names = build_models()
        test_model_info = (client, model_names[0])
        test_response = prompt(test_model_info, "Say 'Hello, young builder!' if you can hear me.")

        if isinstance(test_response, tuple):
            content, usage = test_response
        else:
            content, usage = test_response, None

        if isinstance(content, str) and content.startswith("Error:"):
            raise Exception(f"Prompt failed: {content}")

        print("✅ Success! Your AI is ready to chain prompts!")
        print(f"🤖 AI says: {content}")
        return True

    except Exception as e:
        print("❌ Setup test failed!")
        print(f"🐛 Error: {str(e)}")
        print("\n🔍 Troubleshooting tips:")
        print("   1. Check that you have a .env file with your OPENROUTER_API_KEY")
        print("   2. Make sure you copied your key correctly from OpenRouter")
        print("   3. Verify you have internet connection")
        print("   4. Try running: pip install -r requirements.txt")
        return False


def main():
    if not verify_setup():
        print("\n🚫 Please fix the setup issues above before continuing.")
        return

    print("\n" + "="*60)
    print("🎪 Welcome to the Prompt Chaining Carnival!")
    print("="*60)

    prompt_chainable_poc()

    run_fusion = os.getenv("RUN_FUSION_CHAIN", "").lower() in ("1", "true", "yes")
    if run_fusion:
        print("\n" + "="*60)
        print("🔥 Now for the FusionChain Competition!")
        print("="*60)
        fusion_chain_poc()
    else:
        print("\n💡 Skipping FusionChain by default to save cost. Set RUN_FUSION_CHAIN=1 to enable.")


if __name__ == "__main__":
    main()
