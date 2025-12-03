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

def regulatory_capture_demo():
    print("🚀 Running: Regulatory Capture Mapper Demo")

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Regulation Scenario
    regulation = "The 'Safe Hair Act' requires all hair braiders to complete 2,000 hours of cosmetology training and spend $15,000 on a full cosmetology license, even though they don't use chemicals or scissors."
    print(f"Analyzing Regulation: {regulation}\n")

    result, context_filled_prompts = MinimalChainable.run(
        context={"regulation": regulation},
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Identify Stated vs Actual Purpose
            """Analyze the regulation: '{{regulation}}'.
            Stated Purpose: Public Safety.
            Actual Effect: What does this actually do to the market? Respond in JSON: {"stated_purpose": "safety", "actual_effect": "description"}""",

            # Prompt 2: Identify Beneficiaries
            """Who benefits from this high barrier to entry? 
            - Existing cosmetology schools?
            - Established salons?
            - The hair braiders?
            Respond in JSON: {"beneficiaries": ["Group 1", "Group 2"], "losers": ["Group 3"]}""",

            # Prompt 3: Reveal the Protection Racket
            """Explain the 'Protection Racket' dynamic here. How is the government power being used to protect incumbents from competition? Respond in JSON: {"mechanism": "description", "economic_term": "Rent Seeking"}"""
        ],
    )

    output_dir = os.path.dirname(__file__)
    prompts_file_base = os.path.join(output_dir, "regulatory_capture_prompts")
    results_file_base = os.path.join(output_dir, "regulatory_capture_results")

    chained_prompts_text = MinimalChainable.to_delim_text_file(prompts_file_base, context_filled_prompts)
    chainable_result_text = MinimalChainable.to_delim_text_file(results_file_base, result)

    print(f"\n📖 Prompts Sent:\n{chained_prompts_text}")
    print(f"\n💡 AI Responses:\n{chainable_result_text}")
    print(f"\n✅ Results saved to {prompts_file_base}.txt and {results_file_base}.txt")

    log_file = MinimalChainable.log_to_markdown("regulatory_capture_mapper", context_filled_prompts, result)
    print(f"✅ Log saved to {log_file}")

if __name__ == "__main__":
    from demo_utils import setup_demo_env

    if setup_demo_env():
        regulatory_capture_demo()
