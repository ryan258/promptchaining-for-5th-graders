import sys
import os

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
elif sys.path[0] != project_root:
    sys.path.remove(project_root)
    sys.path.insert(0, project_root)

from chain import MinimalChainable
from main import build_models, prompt

def revealed_preference_demo():
    print("🚀 Running: Revealed Preference Detective Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Stated vs Revealed
    stated_preference = "I care deeply about my digital privacy and data security."
    revealed_behavior = "I use TikTok daily, have a Google Home in every room, and use 'password123' for my bank account because it's easy to remember."

    print(f"Analyzing Preferences:\nStated: {stated_preference}\nRevealed: {revealed_behavior}\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"stated": stated_preference, "revealed": revealed_behavior},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Identify Contradiction
            """Compare the stated preference '{{stated}}' with the revealed behavior '{{revealed}}'. 
            What is the contradiction? Respond in JSON: {"contradiction": "description", "severity": "High/Med/Low"}""",

            # Prompt 2: Decode Value Hierarchy
            """Based on the behavior, what does this person ACTUALLY value more than privacy? (e.g., Convenience, Entertainment, Social Status). Respond in JSON: {"actual_values": ["Value 1", "Value 2"], "evidence": "description"}""",

            # Prompt 3: Predict Future Choice
            """Predict their choice in this scenario: 
            Option A: A secure, encrypted messaging app that costs $2/month and has no fun filters.
            Option B: A free app that sells their data but has amazing AR face filters.
            Respond in JSON: {"predicted_choice": "Option A/B", "reasoning": "why"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "revealed_preference_prompts")
    results_file_base = os.path.join(output_dir, "revealed_preference_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("revealed_preference_detective", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from dotenv import load_dotenv
    dotenv_path = os.path.join(project_root, '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    
    if not os.getenv("OPENROUTER_API_KEY"):
        print("🚨 OPENROUTER_API_KEY not found.")
    else:
        revealed_preference_demo()
