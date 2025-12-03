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

def platform_lock_in_demo():
    print("🚀 Running: Platform Lock-In Forensics Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Feature Analysis
    feature = "PhotoCloud's 'Memories' feature automatically organizes all your photos by face and location, but the metadata is stored in a proprietary format that cannot be exported."
    print(f"Analyzing Feature: {feature}\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"feature": feature},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Analyze Convenience vs Trap
            """Analyze the feature: '{{feature}}'.
            What is the convenience offered? What is the trap hidden inside? Respond in JSON: {"convenience": "description", "trap": "description"}""",

            # Prompt 2: Calculate Switching Cost
            """If a user has 10 years of photos organized this way, what is the 'Switching Cost' to leave? 
            (Time, Data Loss, Effort). Respond in JSON: {"switching_cost": "High/Med/Low", "description": "details"}""",

            # Prompt 3: Predict Extraction Phase
            """Now that the user is locked in, predict the next move by the company. 
            - Price increase?
            - Ads?
            - Reduced free storage?
            Respond in JSON: {"prediction": "move", "rationale": "why"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "platform_lock_in_prompts")
    results_file_base = os.path.join(output_dir, "platform_lock_in_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("platform_lock_in_forensics", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        platform_lock_in_demo()
